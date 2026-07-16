// Blizzard loadout string codec — encode/decode the import/export strings the
// in-game talent UI produces, so a build made here pastes straight into WoW and
// a real in-game string renders here. Pure TypeScript, no DOM, no Svelte.
//
// Format (v2, confirmed end-to-end against a live Wowhead string — see
// codec.test.ts ORACLE). The string is a *bitstream* emitted 6 bits per base64
// char, LSB-first within each char, standard charset `A-Za-z0-9+/`, the final
// char zero-padded. There is no byte alignment.
//
//   Header:  version(8)=2 · specId(16) · treeHash(128, all-zero — the game
//            accepts a zeroed hash from third-party strings).
//   Body:    one entry per node slot, walked in the class-wide serial order
//            (ascending node id over EVERY node in the tree — all specs, every
//            hero sub-tree, and the type-3 selector/grant nodes). `serialCount`
//            slots total, NOT just this spec's slice.
//            Per slot:
//              isSelected(1)
//              if selected: isPurchased(1)
//                if purchased: isPartiallyRanked(1) [ranksPurchased(6) if partial]
//                              isChoice(1)          [choiceIndex(2)    if choice]
//
// Slots the game fills automatically (so the encoder must reproduce them):
//   * granted nodes (spec.grantedSerials): selected-but-not-purchased free
//     talents — emitted as isSelected=1, isPurchased=0 (2 bits, nothing more).
//   * the hero selector (spec.heroSelector): a purchased choice node whose
//     2-bit index picks the active hero tree.
// Both come from the static spec data, not from the user's build, which keeps
// the user `Build` clean (no phantom granted/selector entries) while still
// round-tripping byte-for-byte.
import type { HeroSelector, SpecData, TalentNode } from "./types";
import { type Build, maxRank } from "./validate";

const CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const CHAR_TO_VAL = new Map([...CHARSET].map((c, i) => [c, i]));
const LOADOUT_VERSION = 2;
const HASH_BYTES = 16; // 128-bit tree hash, emitted as zeros

// --- Error types (UI-facing in M5) ---
export class LoadoutError extends Error {}
/** The string is not a parseable v2 loadout (bad charset, truncated header). */
export class MalformedLoadoutError extends LoadoutError {}
/** The string's specId doesn't match the spec it's being decoded against. */
export class WrongSpecError extends LoadoutError {
  constructor(
    readonly expected: number,
    readonly actual: number,
  ) {
    super(`loadout is for spec ${actual}, expected ${expected}`);
  }
}
/** The string's version byte isn't one this codec understands. */
export class VersionMismatchError extends LoadoutError {
  constructor(readonly version: number) {
    super(`unsupported loadout version ${version} (expected ${LOADOUT_VERSION})`);
  }
}

// --- Bit IO (LSB-first, 6 bits per base64 char) ---

class BitReader {
  private bits: Uint8Array;
  private pos = 0;
  constructor(code: string) {
    const out = new Uint8Array(code.length * 6);
    let i = 0;
    for (const ch of code) {
      const v = CHAR_TO_VAL.get(ch);
      if (v === undefined) {
        throw new MalformedLoadoutError(`invalid base64 char ${JSON.stringify(ch)}`);
      }
      for (let b = 0; b < 6; b++) out[i++] = (v >> b) & 1;
    }
    this.bits = out;
  }
  /** Read `n` bits LSB-first as an unsigned int. Throws if the stream is short. */
  read(n: number): number {
    if (this.pos + n > this.bits.length) {
      throw new MalformedLoadoutError("unexpected end of loadout bitstream");
    }
    let val = 0;
    for (let i = 0; i < n; i++) val |= this.bits[this.pos++] << i;
    return val >>> 0;
  }
  readBit(): number {
    return this.read(1);
  }
  remaining(): number {
    return this.bits.length - this.pos;
  }
}

class BitWriter {
  private bits: number[] = [];
  /** Append the low `n` bits of `val`, LSB-first. */
  write(val: number, n: number): void {
    for (let i = 0; i < n; i++) this.bits.push((val >> i) & 1);
  }
  /** Emit base64, 6 bits per char, zero-padding the final char. */
  toBase64(): string {
    let out = "";
    for (let i = 0; i < this.bits.length; i += 6) {
      let v = 0;
      for (let b = 0; b < 6 && i + b < this.bits.length; b++) v |= this.bits[i + b] << b;
      out += CHARSET[v];
    }
    return out;
  }
}

// --- Serial → node index ---

/** Every node in a spec's data keyed by its class-wide serial slot. */
function serialIndex(spec: SpecData): Map<number, TalentNode> {
  const bySerial = new Map<number, TalentNode>();
  const add = (nodes: TalentNode[]) => {
    for (const n of nodes) if (n.serial != null) bySerial.set(n.serial, n);
  };
  add(spec.trees.class.nodes);
  add(spec.trees.spec.nodes);
  for (const sub of Object.values(spec.trees.hero)) add(sub.nodes);
  return bySerial;
}

// --- Public API ---

export interface DecodedLoadout {
  version: number;
  specId: number;
  build: Build;
  /** Active hero tree, from the selector node (null if none / no selector). */
  heroName: string | null;
  /** Selected serials with no node in the spec data (logged, tolerated). */
  unknownSerials: number[];
}

/**
 * Read just the header — enough to route a pasted string to the right spec
 * before its data is fetched (M5). Does not validate the body.
 */
export function peekHeader(code: string): { version: number; specId: number } {
  const r = new BitReader(code);
  const version = r.read(8);
  const specId = r.read(16);
  return { version, specId };
}

/**
 * Decode a loadout string against its spec. Selected node slots become a
 * `Build` keyed by node id (ready for BuildController); granted and selector
 * slots are interpreted but kept out of the user build. Unknown selected serials
 * are tolerated and reported in `unknownSerials`.
 */
export function decodeLoadout(code: string, spec: SpecData): DecodedLoadout {
  const r = new BitReader(code);
  const version = r.read(8);
  if (version !== LOADOUT_VERSION) throw new VersionMismatchError(version);
  const specId = r.read(16);
  if (specId !== spec.specId) throw new WrongSpecError(spec.specId, specId);
  for (let i = 0; i < HASH_BYTES; i++) r.read(8); // tree hash — ignored

  const bySerial = serialIndex(spec);
  const granted = new Set(spec.grantedSerials);
  const selectorSerial = spec.heroSelector?.serial ?? null;
  // serialCount is authoritative; fall back to draining the stream if absent.
  const slots = spec.serialCount && spec.serialCount > 0 ? spec.serialCount : Infinity;

  const build: Build = new Map();
  const unknownSerials: number[] = [];
  let heroName: string | null = null;

  for (let serial = 0; serial < slots; serial++) {
    if (slots === Infinity && r.remaining() < 1) break;
    if (!r.readBit()) continue; // unselected
    const purchased = r.readBit();
    if (!purchased) continue; // granted (selected, not purchased) — data, not build
    const partial = r.readBit();
    const ranks = partial ? r.read(6) : 0;
    const isChoice = r.readBit();
    const choice = isChoice ? r.read(2) : 0;

    if (serial === selectorSerial) {
      heroName = spec.heroSelector?.choices[choice] ?? null;
      continue;
    }
    const node = bySerial.get(serial);
    if (!node) {
      unknownSerials.push(serial);
      continue;
    }
    if (granted.has(serial)) continue; // free node that also has purchased data
    build.set(node.id, { rank: partial ? ranks : maxRank(node), choice });
  }

  if (unknownSerials.length) {
    console.warn(
      `decodeLoadout: ${unknownSerials.length} selected serial(s) absent from ` +
        `${spec.class}/${spec.spec} data: ${unknownSerials.join(", ")}`,
    );
  }
  return { version, specId, build, heroName, unknownSerials };
}

export interface EncodeOptions {
  /** Active hero tree (drives the selector). Falls back to inferring from the build. */
  heroName?: string | null;
}

/**
 * Encode a build to a Blizzard loadout string. Walks all `serialCount` slots,
 * emitting the user's purchased nodes plus the auto-filled granted and selector
 * slots from the spec data. The result pastes straight into the game.
 */
export function encodeLoadout(spec: SpecData, build: Build, opts: EncodeOptions = {}): string {
  const bySerial = serialIndex(spec);
  const granted = new Set(spec.grantedSerials);
  const selector = spec.heroSelector;
  const heroName = opts.heroName ?? inferHero(spec, build);
  const slots = spec.serialCount ?? 0;

  const w = new BitWriter();
  w.write(LOADOUT_VERSION, 8);
  w.write(spec.specId, 16);
  for (let i = 0; i < HASH_BYTES; i++) w.write(0, 8); // zeroed tree hash

  for (let serial = 0; serial < slots; serial++) {
    if (granted.has(serial)) {
      w.write(1, 1); // selected
      w.write(0, 1); // not purchased (auto-granted)
      continue;
    }
    if (selector && serial === selector.serial) {
      const idx = heroName ? selector.choices.indexOf(heroName) : -1;
      if (idx < 0) {
        w.write(0, 1); // no hero chosen → unselected
      } else {
        w.write(1, 1); // selected
        w.write(1, 1); // purchased
        w.write(0, 1); // not partial
        w.write(1, 1); // is choice
        w.write(idx, 2); // hero index
      }
      continue;
    }
    const node = bySerial.get(serial);
    const state = node ? build.get(node.id) : undefined;
    if (!node || !state || state.rank <= 0) {
      w.write(0, 1); // unselected
      continue;
    }
    w.write(1, 1); // selected
    w.write(1, 1); // purchased
    if (state.rank < maxRank(node)) {
      w.write(1, 1); // partially ranked
      w.write(state.rank, 6);
    } else {
      w.write(0, 1); // fully ranked
    }
    if (node.type === "CHOICE") {
      w.write(1, 1); // is choice
      w.write(state.choice & 0b11, 2);
    } else {
      w.write(0, 1); // not a choice
    }
  }
  return w.toBase64();
}

/** Infer the active hero tree from which hero sub-tree the build has nodes in. */
function inferHero(spec: SpecData, build: Build): string | null {
  for (const [name, sub] of Object.entries(spec.trees.hero)) {
    if (sub.nodes.some((n) => (build.get(n.id)?.rank ?? 0) > 0)) return name;
  }
  return null;
}

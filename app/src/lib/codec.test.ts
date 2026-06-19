import { describe, expect, test } from "bun:test";
import {
  MalformedLoadoutError,
  VersionMismatchError,
  WrongSpecError,
  decodeLoadout,
  encodeLoadout,
  peekHeader,
} from "./codec";
import type { Build } from "./validate";
import { maxRank, pointsSpent } from "./validate";
import type { SpecData } from "./types";

// Compact spec data the codec consumes (Stage B output). Imported straight from
// the committed runtime assets so the tests exercise real serial walks.
import affliction from "../../static/data/warlock/affliction.json";
import arcane from "../../static/data/mage/arcane.json";
import feral from "../../static/data/druid/feral.json";
import shadow from "../../static/data/priest/shadow.json";
import windwalker from "../../static/data/monk/windwalker.json";
import devastation from "../../static/data/evoker/devastation.json";

const aff = affliction as unknown as SpecData;

// Ground truth: Affliction / Soul Harvester, Wowhead, Midnight 12.0.7. Decodes
// to v2 / spec 265 / zero hash / 202 slots / 77 selected (73 purchased + 3
// granted + 1 hero selector) / 11 choice / 0 partial.
const ORACLE =
  "CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNbmx2MzYWGAAwMzsMbmZWGDAM22GYATwMsFYYbAAAYGAAAzMjZMzsNGzYMzMzYYmZGAgBMA";

describe("header (LSB-first bit layout)", () => {
  test("peekHeader reads version + specId", () => {
    expect(peekHeader(ORACLE)).toEqual({ version: 2, specId: 265 });
  });

  test("the 152-bit header is build-independent", () => {
    // First 25 base64 chars = 150 bits = pure header (version, specId, zero
    // hash); identical for any Affliction string regardless of the body.
    const empty = encodeLoadout(aff, new Map());
    expect(empty.slice(0, 25)).toBe(ORACLE.slice(0, 25));
  });
});

describe("decode the oracle", () => {
  const decoded = decodeLoadout(ORACLE, aff);

  test("header fields", () => {
    expect(decoded.version).toBe(2);
    expect(decoded.specId).toBe(265);
  });

  test("active hero tree comes from the selector node", () => {
    expect(decoded.heroName).toBe("Soul Harvester");
  });

  test("73 purchased nodes, no unrepresented serials", () => {
    // 77 selected − 3 granted − 1 selector = 73 user-purchased nodes.
    expect(decoded.build.size).toBe(73);
    expect(decoded.unknownSerials).toEqual([]);
  });

  test("Soul Harvester hero nodes are present", () => {
    const heroIds = new Set(aff.trees.hero["Soul Harvester"].nodes.map((n) => n.id));
    const picked = [...decoded.build.keys()].filter((id) => heroIds.has(id));
    expect(picked.length).toBeGreaterThan(5);
  });

  test("per-tree purchased points", () => {
    const cls = pointsSpent(aff.trees.class.nodes, decoded.build);
    const spc = pointsSpent(aff.trees.spec.nodes, decoded.build);
    const hero = pointsSpent(aff.trees.hero[decoded.heroName!].nodes, decoded.build);
    expect([cls, spc, hero]).toEqual([34, 31, 13]);
  });
});

describe("oracle acceptance test (the gate)", () => {
  test("encode(decode(ORACLE)) === ORACLE, byte-identical", () => {
    const d = decodeLoadout(ORACLE, aff);
    expect(encodeLoadout(aff, d.build, { heroName: d.heroName })).toBe(ORACLE);
  });

  test("hero inference reproduces the string without an explicit heroName", () => {
    const d = decodeLoadout(ORACLE, aff);
    expect(encodeLoadout(aff, d.build)).toBe(ORACLE);
  });
});

// Build a deterministic, codec-legal sample selection for a spec: a slice of
// nodes from each tree (skipping granted/selector slots, which the encoder fills
// itself), one deliberately partial multi-rank node, and choices on CHOICE nodes.
function sampleBuild(spec: SpecData): { build: Build; heroName: string | null } {
  const build: Build = new Map();
  const granted = new Set(spec.grantedSerials);
  const selector = spec.heroSelector?.serial ?? null;
  const heroName = Object.keys(spec.trees.hero)[0] ?? null;
  const pickable = [
    ...spec.trees.class.nodes,
    ...spec.trees.spec.nodes,
    ...(heroName ? spec.trees.hero[heroName].nodes : []),
  ].filter((n) => n.serial == null || (!granted.has(n.serial) && n.serial !== selector));

  let madePartial = false;
  for (const node of pickable.slice(0, 14)) {
    const mr = maxRank(node);
    let rank = mr;
    if (!madePartial && mr > 1) {
      rank = mr - 1; // exercise the isPartial + ranksPurchased path
      madePartial = true;
    }
    const choice = node.type === "CHOICE" ? 1 : 0;
    build.set(node.id, { rank, choice });
  }
  return { build, heroName };
}

describe("structural round-trips (one per class, choice + multi-rank)", () => {
  const specs: [string, SpecData][] = [
    ["warlock/affliction", aff],
    ["mage/arcane", arcane as unknown as SpecData],
    ["druid/feral", feral as unknown as SpecData],
    ["priest/shadow", shadow as unknown as SpecData],
    ["monk/windwalker", windwalker as unknown as SpecData],
    ["evoker/devastation", devastation as unknown as SpecData],
  ];

  for (const [name, spec] of specs) {
    test(`${name}: encode → decode === build`, () => {
      const { build, heroName } = sampleBuild(spec);
      const code = encodeLoadout(spec, build, { heroName });
      const d = decodeLoadout(code, spec);

      expect(d.specId).toBe(spec.specId);
      expect(d.heroName).toBe(heroName);
      expect(d.unknownSerials).toEqual([]);
      // Same node ids and the same {rank, choice} for each.
      expect([...d.build.keys()].sort((a, b) => a - b)).toEqual(
        [...build.keys()].sort((a, b) => a - b),
      );
      for (const [id, st] of build) expect(d.build.get(id)).toEqual(st);
    });

    test(`${name}: encode walks exactly serialCount slots (idempotent)`, () => {
      const { build, heroName } = sampleBuild(spec);
      const code = encodeLoadout(spec, build, { heroName });
      // Re-encoding the decoded build is stable → the slot walk is aligned at N.
      const again = encodeLoadout(spec, decodeLoadout(code, spec).build, { heroName });
      expect(again).toBe(code);
      expect(spec.serialCount).toBeGreaterThan(0);
    });
  }
});

describe("malformed / mismatched input", () => {
  test("invalid base64 char → MalformedLoadoutError", () => {
    expect(() => decodeLoadout("Ck-not-base64-!!!", aff)).toThrow(MalformedLoadoutError);
  });

  test("truncated header → MalformedLoadoutError", () => {
    expect(() => decodeLoadout("Ck", aff)).toThrow(MalformedLoadoutError);
  });

  test("version byte mismatch → VersionMismatchError", () => {
    // Flip the version: char 0 = 'C' (version low bits). 'D' (idx 3) → version 3.
    const bad = "D" + ORACLE.slice(1);
    expect(() => decodeLoadout(bad, aff)).toThrow(VersionMismatchError);
  });

  test("wrong spec → WrongSpecError", () => {
    expect(() => decodeLoadout(ORACLE, arcane as unknown as SpecData)).toThrow(WrongSpecError);
  });
});

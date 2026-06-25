/**
 * session.js — builds the drill queue.
 *
 * Draws due cards through the active filters and *interleaves dungeons* so the
 * player never drills one dungeon at a time (harder in the moment, better
 * retention, and it fights the "eight dungeons blur together" problem). New
 * (unseen) cards are prioritised lightly so a fresh profile starts learning.
 */
import { cardsForFilters } from "./content.js";
import { isDue } from "./srs.js";

/** Cheap deterministic-ish shuffle seeded by `now` for per-session variety. */
function shuffle(arr, seed) {
  const a = arr.slice();
  let s = seed >>> 0;
  for (let i = a.length - 1; i > 0; i--) {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Round-robin merge of per-dungeon lists so consecutive cards differ in dungeon
 * wherever possible. Never blocks one dungeon: we drain one card per dungeon per
 * pass, cycling until every list is empty.
 */
function interleaveByDungeon(cards, seed) {
  const byDgn = new Map();
  for (const c of cards) {
    const k = c.cue.dungeonSlug;
    if (!byDgn.has(k)) byDgn.set(k, []);
    byDgn.get(k).push(c);
  }
  // Shuffle each dungeon's cards and the dungeon order for variety.
  const lists = shuffle([...byDgn.values()], seed).map((l) => shuffle(l, seed + l.length));
  const out = [];
  let drained = false;
  while (!drained) {
    drained = true;
    for (const list of lists) {
      const next = list.shift();
      if (next) {
        out.push(next);
        drained = false;
      }
    }
  }
  return out;
}

/**
 * Build an interleaved queue of due cards.
 * @param {Object} opts
 * @param {Record<string, import("./srs.js").CardState>} opts.schedule
 * @param {{ role?: string, enabledDungeons?: string[] }} opts.filters
 * @param {number} [opts.now]
 * @param {number} [opts.limit] cap the session length (0/undefined = no cap)
 * @returns {Array} card objects, interleaved across dungeons
 */
export function buildQueue({ schedule, filters, now = Date.now(), limit = 0 }) {
  const pool = cardsForFilters(filters).filter((c) => isDue(schedule[c.id], now));
  const queue = interleaveByDungeon(pool, now);
  return limit > 0 ? queue.slice(0, limit) : queue;
}

/** Count of due cards under filters (for the header "n / total" readout). */
export function dueCount({ schedule, filters, now = Date.now() }) {
  return cardsForFilters(filters).filter((c) => isDue(schedule[c.id], now)).length;
}

/**
 * Build a one-shot Test/intro queue for a single dungeon.
 *
 * Order is deliberately *definition order* — `content.json` emits a dungeon's
 * cards bosses-in-encounter-order, each boss's casts in table order, then trash
 * by wing, and `cardsForFilters` preserves that array order. No `isDue` filter,
 * no shuffle, no dungeon-interleave (Test is a blocked, in-order pass, the
 * opposite of Drill's interleaving by intent).
 * @param {Object} opts
 * @param {string} opts.dungeonSlug the single dungeon to walk
 * @param {{ role?: string }} [opts.filters] role filter (enabledDungeons is forced)
 * @returns {Array} card objects in definition order
 */
export function buildTestQueue({ dungeonSlug, filters = {} }) {
  return cardsForFilters({ ...filters, enabledDungeons: [dungeonSlug] });
}

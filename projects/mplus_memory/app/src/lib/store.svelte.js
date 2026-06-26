/**
 * store.svelte.js — the persistence layer.
 *
 * One versioned localStorage key holds the entire trainer state: SM-2 schedule,
 * settings (role + enabled dungeons + active mode) and lifetime stats. A runes
 * `$state` proxy is mirrored to storage via an `$effect`, so every mutation in
 * the app auto-persists. Reload restores it.
 */
import { allDungeonSlugs } from "./content.js";
import { freshState, review } from "./srs.js";

const KEY = "mplus.trainer.v1";

function defaults() {
  return {
    version: 1,
    schedule: /** @type {Record<string, import("./srs.js").CardState>} */ ({}),
    settings: {
      role: "dps", // player is DPS; "all" widens the pool (healer/tank = filter flip)
      enabledDungeons: [...allDungeonSlugs],
      scope: "both", // "both" | "boss" | "trash" — boss kits vs trash, or all
      tierFloor: "all", // "all" | tier slug — priority floor (keep that tier + above)
      mode: "drill",
    },
    stats: { reviews: 0, correct: 0, lastReviewDay: null, streakDays: 0 },
  };
}

function load() {
  const base = defaults();
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return base;
    const saved = JSON.parse(raw);
    if (saved?.version !== base.version) return base; // future migrations live here
    return {
      ...base,
      ...saved,
      settings: { ...base.settings, ...saved.settings },
      stats: { ...base.stats, ...saved.stats },
      schedule: saved.schedule ?? {},
    };
  } catch {
    return base;
  }
}

/** The single reactive store object. Mutate its fields directly — it persists. */
export const store = $state(load());

// Mirror to localStorage on any change. $effect.root keeps it alive outside a
// component lifecycle (this module is imported once, app-wide).
$effect.root(() => {
  $effect(() => {
    try {
      localStorage.setItem(KEY, JSON.stringify(store));
    } catch {
      /* storage full / disabled — non-fatal */
    }
  });
});

const dayStamp = (now) => new Date(now).toISOString().slice(0, 10);

/**
 * Record a grade for a card: advance its SM-2 state and update lifetime stats
 * (including a simple day-streak).
 * @param {string} cardId
 * @param {import("./srs.js").Grade} grade
 * @param {boolean} wasCorrect whether the classify answer was right first try
 */
export function recordReview(cardId, grade, wasCorrect, now = Date.now()) {
  store.schedule[cardId] = review(store.schedule[cardId] ?? freshState(now), grade, now);
  store.stats.reviews += 1;
  if (wasCorrect) store.stats.correct += 1;

  const today = dayStamp(now);
  const last = store.stats.lastReviewDay;
  if (last !== today) {
    const yesterday = dayStamp(now - 86_400_000);
    store.stats.streakDays = last === yesterday ? store.stats.streakDays + 1 : 1;
    store.stats.lastReviewDay = today;
  }
}

export function setRole(role) {
  store.settings.role = role;
}

/** Boss/trash scope: "both" | "boss" | "trash". */
export function setScope(scope) {
  store.settings.scope = scope;
}

/** Priority floor: "all" | tier slug ("job" | "death" | "wipe"). */
export function setTierFloor(tier) {
  store.settings.tierFloor = tier;
}

export function toggleDungeon(slug) {
  const set = new Set(store.settings.enabledDungeons);
  if (set.has(slug)) set.delete(slug);
  else set.add(slug);
  // never allow an empty pool — keep at least one dungeon on
  if (set.size === 0) set.add(slug);
  store.settings.enabledDungeons = [...set];
}

export function setMode(mode) {
  store.settings.mode = mode;
}

/** Wipe all progress (settings kept). */
export function resetProgress() {
  store.schedule = {};
  store.stats = defaults().stats;
}

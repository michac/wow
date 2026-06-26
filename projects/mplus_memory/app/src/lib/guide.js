/**
 * guide.js — the content layer for Guide Mode.
 *
 * Imports the bundled, journal-only `adventure-guide.json` (8 dungeons, 29
 * bosses: lore, role tips, ability tree, loot) and exposes plain selectors over
 * it. Kept deliberately separate from `content.js` so the read-only Adventure
 * Guide and the spaced-repetition trainer never entangle.
 */
import data from "../adventure-guide.json";

// Per-dungeon hue, mirrored from content.json / the --color-dgn-* token ramp.
// The guide JSON is journal-only and carries no presentation, so the hue lives
// here keyed by slug (drives the `--dgn` knob, same as content's `d.hue`).
const DUNGEON_HUE = {
  "magisters-terrace": "oklch(0.70 0.16 320)",
  "maisara-caverns": "oklch(0.72 0.13 175)",
  "nexus-point-xenas": "oklch(0.70 0.15 275)",
  "windrunner-spire": "oklch(0.74 0.14 150)",
  "algethar-academy": "oklch(0.78 0.13 85)",
  "seat-of-the-triumvirate": "oklch(0.64 0.17 300)",
  "skyreach": "oklch(0.80 0.11 215)",
  "pit-of-saron": "oklch(0.83 0.06 250)",
};

export const guidePatch = data.patch;

/** The 8 dungeons, each decorated with its `hue`. Source order is journal order. */
export const guideDungeons = data.dungeons.map((d) => ({
  ...d,
  hue: DUNGEON_HUE[d.slug] ?? "var(--color-dgn-mt)",
}));

const bySlug = new Map(guideDungeons.map((d) => [d.slug, d]));

/** @param {string} slug */
export const guideDungeon = (slug) => bySlug.get(slug);

// store.settings.role ("dps" | "healer" | "tank") → the journal roleTips key.
export const ROLE_TIP_KEY = {
  dps: "Damage Dealers",
  healer: "Healers",
  tank: "Tanks",
};

/**
 * Split journal text on `[Ability]` hyperlink markers into renderable segments.
 * The Adventure Guide uses square brackets to mark cross-referenced spells; we
 * strip the brackets and flag those runs so the view can bold them.
 * @param {string} text → [{ t: string, bold: boolean }]
 */
export function bracketSegments(text) {
  const out = [];
  const re = /\[([^\]]+)\]/g;
  let last = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push({ t: text.slice(last, m.index), bold: false });
    out.push({ t: m[1], bold: true });
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ t: text.slice(last), bold: false });
  return out;
}

/**
 * content.js — the content layer.
 *
 * Imports the generated content.json (boss + trash ability cards, the 21
 * archetypes, dungeon metadata) and exposes plain selectors over it. No engine
 * or view logic lives here.
 */
import data from "../content.json";

export const archetypes = data.archetypes;
export const dungeons = data.dungeons;
export const cards = data.cards;
export const meta = data.meta;

const archetypeBySlug = new Map(archetypes.map((a) => [a.slug, a]));
const dungeonBySlug = new Map(dungeons.map((d) => [d.slug, d]));
const cardById = new Map(cards.map((c) => [c.id, c]));

/** @param {string} slug */
export const archetype = (slug) => archetypeBySlug.get(slug);
/** @param {string} slug */
export const dungeon = (slug) => dungeonBySlug.get(slug);
/** @param {string} id */
export const card = (id) => cardById.get(id);

export const dungeonName = (slug) => dungeonBySlug.get(slug)?.name ?? slug;

export const allDungeonSlugs = dungeons.map((d) => d.slug);

/**
 * Cards passing the active filters.
 * @param {{ role?: string, enabledDungeons?: string[] }} filters
 *   role: "all" keeps everything; otherwise keep cards whose role is "all",
 *   null, or names the chosen role. enabledDungeons: slugs to keep (all if absent).
 */
export function cardsForFilters({ role = "all", enabledDungeons } = {}) {
  const dgnSet = enabledDungeons ? new Set(enabledDungeons) : null;
  return cards.filter((c) => {
    if (dgnSet && !dgnSet.has(c.cue.dungeonSlug)) return false;
    if (role !== "all") {
      const r = (c.reveal.role || "").toLowerCase();
      // A card is in-scope for a role if it's universal or names that role.
      if (r && r !== "all" && !r.includes(role)) return false;
    }
    return true;
  });
}

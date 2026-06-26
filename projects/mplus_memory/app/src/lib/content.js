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
 * Consequence ranking — the spec's tiering, ordered low→high stakes. Drives the
 * "priority floor" filter: keep cards at or above the chosen tier. Severity is
 * the priority lever (not role) because every card carries exactly one tier,
 * whereas role is a coarser lever (most cards are "all"). Anything off this map
 * sinks to 0.
 */
export const TIER_RANK = { flavor: 0, job: 1, death: 2, wipe: 3 };

/**
 * Cards passing the active filters.
 * @param {{ role?: string, enabledDungeons?: string[], scope?: string, tierFloor?: string }} filters
 *   role: "all" keeps everything; otherwise keep cards that are universal
 *   ("all") or list the chosen role in their resolved `reveal.roles`.
 *   enabledDungeons: slugs to keep (all if absent).
 *   scope: "both" (default) | "boss" | "trash" — matched against cue.casterKind.
 *   tierFloor: "all" (default) | a tier slug — keep that tier and everything
 *   above it in consequence (e.g. "death" keeps death + wipe).
 */
export function cardsForFilters({ role = "all", enabledDungeons, scope = "both", tierFloor = "all" } = {}) {
  const dgnSet = enabledDungeons ? new Set(enabledDungeons) : null;
  const floor = tierFloor === "all" ? -1 : (TIER_RANK[tierFloor] ?? -1);
  return cards.filter((c) => {
    if (dgnSet && !dgnSet.has(c.cue.dungeonSlug)) return false;
    if (scope !== "both" && c.cue.casterKind !== scope) return false;
    if (floor >= 0 && (TIER_RANK[c.reveal.tier] ?? 0) < floor) return false;
    if (role !== "all") {
      // Always-resolved roles (build guarantees the enum). A card is in-scope if
      // it's universal ("all") or lists the chosen role among its roles.
      const roles = c.reveal.roles || [c.reveal.role];
      if (!roles.includes("all") && !roles.includes(role)) return false;
    }
    return true;
  });
}

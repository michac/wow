/** ui.js — small presentation helpers shared across components. */

export const TIER_META = {
  wipe: { label: "group wipe", emoji: "🔴", cls: "tier-wipe" },
  death: { label: "your death", emoji: "🟠", cls: "tier-death" },
  job: { label: "your job", emoji: "🔵", cls: "tier-job" },
  flavor: { label: "flavor", emoji: "⚪", cls: "tier-flavor" },
};

export const tierClass = (tier) => TIER_META[tier]?.cls ?? "tier-flavor";

/** archetype slug → drill label, e.g. "ground-void-zone" → "ground void zone" */
export const humanizeSlug = (slug) => (slug || "").replace(/-/g, " ");

/** Map a caster kind + segment into the small subtitle under the boss name. */
export function cueSubtitle(cue) {
  if (cue.casterKind === "boss") return "boss";
  return `trash · ${cue.segment}`;
}

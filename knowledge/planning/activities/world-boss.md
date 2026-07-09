---
id: world-boss
name: Weekly world boss
goal: [gearing, collectibles]
venue: world
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: world_boss_weekly }
reward: { type: [power, collectible], detail: "weekly loot roll + mount/transmog chance" }
yields:
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # Hero drop LANDS at 259 (1/6, dawncrests.md), not the 276 ceiling; chance carried for Phase-3 EV, unused in 2a
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - knowledge/endgame/world-events.md
  - knowledge/planning/candidates.json
confidence: high
---
The rotating weekly world boss — one loot roll for gear, plus a chance at its
mount/transmog (hence `collectibles`). Fast, group-tagged only because you tag along
with whoever's there. Gate resolves from the dump's world-boss lockout.

**Grouping is easy — the quest carries an LFG hook** (in-game, 2026-07-09): the world-boss
quest shows a little **LFG icon** that opens the free-form group finder pre-seeded with a
search term, so finding a group is very likely. This is why a world boss shouldn't take the
full `group`-content solo penalty (a future `--solo` down-rank, Phase 4) — it's `group` to
*fight* but trivially puggable via the hook.

**No `yields.currencies` (needs-first Phase 1).** The boss itself yields a Hero-track
**gear** roll (Warbound Heroic cache on Heroic WT) — valued by `reward_ilvl_max: 276`
via `slot_target_R`, *not* a crest currency (crests come from the surrounding rares,
folded into `val-naigtal`). Its warbound-cache-for-alts value is a Phase-4 flow.

---
id: void-assault
name: Void Assault weekly
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: void_assault }
reward: { type: [power, collectible], detail: "weekly gear/voidcore drops + cosmetics; 12.0.7 doubled its XP (leveler-only) and drops" }
time_blocks: 1
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - knowledge/planning/candidates.json
  - knowledge/systems/void-incursions.md
confidence: high
---
The Void Assault weekly event — gear, rep, and cosmetic drops. Gate resolves from the
dump's weekly-quest state.

**XP is leveler-only (Phase 0, needs-first redesign).** 12.0.7 doubled both XP *and* drop
rates. The **doubled XP is worthless at level cap** — it's only value on a sub-cap roster
member (strong alt-leveling fodder). At cap the draw is the **gear/voidcore drops +
cosmetics**, nothing else; don't credit the XP toward the geared main's value. When
XP-bearing needs land (Phase 4 roster/leveler synergy) the XP weight applies *only* to
roster members below cap; here `goal:gearing` scores the at-cap drop value and the
runtime slot-target R deflates it once every slot is Hero-capped.

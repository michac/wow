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
reward_ilvl_max: 279   # Hero-track weekly roll
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-06
sources: [knowledge/planning/candidates.json, knowledge/endgame/world-events.md]
confidence: high
---
The rotating weekly world boss — one loot roll for gear, plus a chance at its
mount/transmog (hence `collectibles`). Fast, group-tagged only because you tag along
with whoever's there. Gate resolves from the dump's world-boss lockout.

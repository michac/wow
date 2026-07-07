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
reward_ilvl_max: 276   # Hero-track ceiling (259 1/6 → 276 6/6)
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

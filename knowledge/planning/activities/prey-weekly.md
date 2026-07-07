---
id: prey-weekly
name: 3 Nightmare Prey hunts
goal: [gearing]
venue: world
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: prey_weekly }
reward: { type: [power], detail: "weekly objective; overlaps Liadrin" }
reward_ilvl_max: 279   # random Hero map piece — low value once Hero-capped (run it for the Voidshard unlock)
time_blocks: 1.5
enjoyment: 1.1
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources:
  - knowledge/planning/candidates.json
  - knowledge/endgame/prey.md
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
confidence: high
---
Track and kill 3 Nightmare Prey for the weekly objective. Wired to quest 94446 with
`have/need` progress in the dump (shows e.g. "at 1/3"). Overlaps the Liadrin world-event
weekly, so they often clear together.

**Why run it (terminal reward, not the random hero).** The forced bounty-map hero piece
is a Hero-track roll (`reward_ilvl_max: 279`) — **low value once you're Hero-geared**, so
the slot-target R deflates it for a geared main. The durable reason to keep running Prey
is the **Nightmare-difficulty unlock → Ascendant Voidshards** (weapon/trinket overcap mats,
`../../systems/void-forge.md`) plus the Preyseeker's Journey ranks and the 12.0.7 XP/Renown
buff — not the weekly gear roll. Chase Prey for the Voidshard/journey terminal, not the map.

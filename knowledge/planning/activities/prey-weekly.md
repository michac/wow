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
yields:
  currencies: { hero_crest: 20 }   # Nightmare Prey weekly = 20 Hero crests (dawncrests.md)
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # random Hero map piece LANDS at 259 (1/6, dawncrests.md), not the 276 ceiling; chance carried for Phase-3 EV, unused in 2a
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

**Prerequisite the gate doesn't check yet:** this weekly needs **Nightmare** unlocked
(Preyseeker's Journey **rank 4**). The `weekly_quest` gate only reads whether the quest is
in progress/complete — it does **not** verify the character has Nightmare unlocked, and the
Journey may be **per-character** (unconfirmed — see `../../endgame/prey.md`). So the planner
can surface this for an alt that can't actually run it. Until the addon dumps a
`nightmare_unlocked` / Journey-rank signal, treat it as a soft assumption for a fresh alt.
@verify-ingame

**Why run it (terminal reward, not the random hero).** The forced bounty-map hero piece
is a Hero-track roll (`reward_ilvl_max: 276`) — **low value once you're Hero-geared**, so
the slot-target R deflates it for a geared main. The durable reason to keep running Prey
is the **Nightmare-difficulty unlock → Ascendant Voidshards** (weapon/trinket overcap mats,
`../../systems/void-forge.md`) plus the Preyseeker's Journey ranks and the 12.0.7 XP/Renown
buff — not the weekly gear roll. Chase Prey for the Voidshard/journey terminal, not the map.

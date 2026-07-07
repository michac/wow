---
id: renown-dungeon-weekly
name: Dungeon weekly (1500 choice-rep → renown)
goal: [gearing]
venue: dungeon
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: dungeon_weekly }
reward: { type: [currency], detail: "1500 choice-rep; point at The Singularity for the gear unlock (one-time — renown maintenance once claimed)" }
reward_base: 1   # Phase 0: the gear payoff is a one-time Singularity renown unlock. Past that rank it's renown maintenance, NOT gearing — so don't ride the flat goal:gearing R=3. Restore the pre-unlock value once renown rank is in state (Phase 4).
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources: [knowledge/planning/candidates.json, knowledge/factions/]
confidence: medium
---
The weekly dungeon quest paying 1500 choosable renown. **Renown is instrumental**
(see `_facets.md`): the intended unlock here is the Singularity gear piece — retag if
you're chasing a recipe (`professions`) or mount (`collectibles`) instead.

**Phase 0 down-value (needs-first redesign).** The Singularity gear reward is a
**one-time renown milestone**, not ongoing power. On the geared main (`Encomplete`,
already past that rank — see the redesign worked example: "dungeon-weekly renown
drops off, past the trinket") the weekly 1500 renown is just **maintenance**, so the
flat `goal:gearing` R=3 over-valued it. Pinned `reward_base: 1` to reflect the
past-unlock reality. This should become **conditional** (full gearing value *only*
below the unlock rank) once renown rank lands in planner state — that's Phase 4;
until then a fresh alt chasing the unlock is under-valued by this pin (accepted
trade-off, the planner currently models the past-unlock main).
**Gate TODO:** quest ID needed — read the live log when picked up.

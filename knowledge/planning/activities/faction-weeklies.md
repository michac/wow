---
id: faction-weeklies
name: Faction world events (renown + champion gear)
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: faction_events }
reward: { type: [power, currency, collectible], detail: "champion ilvl-246 slot pieces (renown-gated) + pinnacle/apex caches + renown; housing decor" }
reward_ilvl_max: 246   # Champion slot pieces — a sidegrade for anyone Hero-geared
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-06
sources: ["yt:cpbQXd04ehI", "yt:kUP8oqI7Ekc", "knowledge/endgame/world-events.md"]
confidence: medium
---
The rotating **per-faction weekly events** — **Saltheril's Soiree** (Silvermoon Court),
**Abundance** (Amani), **Legends of the Harndar** (Harathi), **Storm's Wake Assault** (The
Singularity), each culminating in a pinnacle/apex cache. Renown is **instrumental** here
(`_facets.md`): the payoff is a **renown-gated champion-track ilvl-246 slot piece** from each
quartermaster — helm (Silvermoon Court, renown 9, *Courting Success*), necklace (Amani 9),
belt (Harathi 9), trinket (Singularity 7) — hence `goal:gearing`, plus housing-decor and
mount collectibles.

Completing **all** faction events also finishes the **Midnight World Tour** quest → a second
Spark. **Overlap note (for the future ranker-wiring pass):** `liadrin-spark` picks *one* of
these to satisfy its weekly, and `void-assault` is a Singularity-adjacent event — don't
double-count the shared clears. This row exists for the champion-gear + pinnacle-cache reward
those two don't capture.

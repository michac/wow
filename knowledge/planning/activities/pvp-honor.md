---
id: pvp-honor
name: Honor gear + weekly PvP quests
goal: [gearing]
venue: pvp
group: flex
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [power, currency], detail: "Honor → full honor set (~10K honor); weekly PvP quests → rep/honor" }
time_blocks: 1
patch: 12.0.7
fetched: 2026-07-06
sources: ["yt:6OkVWEdttZ0", "yt:cpbQXd04ehI", "https://www.icy-veins.com/wow/midnight-pvp-gearing-guide"]
confidence: low
---
The entry-level PvP floor: random BGs / Solo Shuffle for **Honor**, which buys a full honor
set (~10K honor for a complete kit; **training grounds** vs bots is the fast farm).
`cadence: repeatable` — no reset, always available (`gate: always`, low urgency). War-mode
gear is currently the **same ilvl** as honor gear in Midnight, so bloody tokens are optional
min-max only.

Also the home of the two **weekly PvP quests** from Zaralla (Silvermoon) — one pays Honor +
faction rep (collect Sparks of War in the active zone / War Supply Crates), one pays Marks
of Honor + Honor. Those are a modest weekly rep/gear top-up folded here rather than split out.
`gate: always` keeps it as fill-time; the rated push lives in `pvp-conquest`.

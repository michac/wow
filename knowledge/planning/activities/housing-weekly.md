---
id: housing-weekly
name: Housing weekly (Vaeli)
goal: [collectibles]
venue: housing
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: housing_weekly }
reward: { type: [currency], detail: "housing decor currency; flavor" }
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources: [knowledge/planning/candidates.json, knowledge/systems/housing.md]
confidence: low
---
Vaeli's rotating housing weekly — decor currency, pure flavor (low R). **Gate is a
likely-gap:** the quest-of-the-week rotates IDs, so `housing_weekly` may not resolve;
low value means it's fine to leave as best-effort until the addon tracks it.

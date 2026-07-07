---
id: delve-bountiful
name: 6 keyed Bountiful delves
goal: [gearing]
venue: delve
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: delve_weekly_cache }
breakpoint: { type: vault, track: world, thresholds: [1, 4, 8] }
reward: { type: [power], detail: "weekly cache + catalyst; also fills the Vault's world column" }
reward_ilvl_max: 279   # Hero ceiling — slot-target R drops this for a Hero-capped char
time_blocks: 1
enjoyment: 1.4
patch: 12.0.7
fetched: 2026-07-06
sources: [knowledge/planning/candidates.json, knowledge/endgame/delves/overview.md]
confidence: high
---
The core solo loop — key 6 Bountiful delves for the weekly cache and catalyst charges.
Running them **also fills the world/delve column of the single Great Vault** (slots at
1/4/8), so that vault progress is a `breakpoint` here rather than its own row (merged the
old `delve-world-vault`).
**Gate TODO (roadmap):** the weekly cap sits on the Restored Coffer Key economy, not
the shard currency (dump shows shards `weeklyMax=0`); resolve the key signal in-game.

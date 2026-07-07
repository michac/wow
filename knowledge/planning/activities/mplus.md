---
id: mplus
name: Mythic+ dungeons
goal: [gearing, rating]
venue: dungeon
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: mplus_weekly_lt, n: 8 }
breakpoint: { type: vault, track: mplus, thresholds: [1, 4, 8] }
reward: { type: [power], detail: "per-run loot + crests + IO; fills the Vault's M+ column" }
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-06
sources: [knowledge/planning/candidates.json, knowledge/endgame/mythic-plus/]
confidence: high
---
Run keys for per-run loot, crests, and IO score. Running them **also fills the Mythic+
column of the single Great Vault** (slots at 1/4/8 runs) — that vault contribution is a
`breakpoint` here, **not** a separate activity. `goal` spans `gearing` and `rating`:
above ~+10 the loot flattens but IO keeps climbing, so completionists push past the gear
breakpoint. `breakpoint_R()` boosts the run that crosses the next threshold; R→0 once capped.

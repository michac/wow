---
id: sporefall-raid
name: Sporefall raid (Rotmire) — weekly boss kill
goal: [gearing]
venue: raid
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: raid_weekly, boss: rotmire }
breakpoint: { type: vault, track: raid, thresholds: [2, 4, 6] }
reward: { type: [power], detail: "Rotmire loot per difficulty (ilvl 259–298); fills the Vault's raid column" }
reward_ilvl_max: 285   # realistic pug ceiling (Heroic); Mythic 298 needs a guild
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-06
sources: ["yt:0asUDe1lUPE", "yt:bCgLtZrd5gQ", "https://www.wowhead.com/guide/midnight/raids/sporefall-overview-location-rewards-boss", "knowledge/endgame/raids/sporefall.md"]
confidence: medium
---
The 12.0.7 raid: a **single-boss** encounter vs **Rotmire**, in Harandar near the Grudge
Pit delve (/way 73.7, 66.5). RF → Mythic, ilvl **259–298**. Notable as WoW's first
**Mythic Flex** raid — Mythic scales for 15–25 players.

Because it's one boss, weekly kills come from re-killing Rotmire across difficulties
(LFR/Normal/Heroic/Mythic), and those kills **fill the raid column of the single Great
Vault** — expressed here as a `breakpoint`, not a separate row. The raid column's **first
vault slot needs 2 boss kills** (thresholds 2/4/6), so a single Sporefall kill does *not*
unlock a slot — you need it dead on **two different difficulties**. With one boss the
weekly kill ceiling is the number of difficulties you can clear (LFR→Mythic ≈ 4), so
realistically **≤2 raid vault slots** are achievable via multi-difficulty. The fight is one repeating
phase (add-cleave → Fungal Bloom → bursting-shroom soak); see `endgame/raids/sporefall.md`
for the mechanics distilled from the RCP/Tactyks guides. `group`-gated (E 0.7) so it sits
below solo weeklies at equal urgency unless a vault slot is on the line.

**Difficulty is a within-activity axis, not a facet.** This catalog is one row per activity
(like `mplus`, which spans key levels), so difficulty stays *inside* the row — the front
matter carries only the ilvl *span* (259–298). The per-difficulty reward map lives in the
reference file (`endgame/raids/sporefall.md`): **RF 259 · Normal 272 · Heroic 285 · Mythic
298**. When the ranker is wired later, "which difficulty is worth my time" becomes a live
call from breakpoint proximity (next vault slot / next ilvl upgrade) against your current
gear — it's a scoring input, not another catalog entry.

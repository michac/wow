---
title: Midnight Weekly To-Do Checklist (Level 90 Endgame)
patch: 12.0.7
fetched: 2026-06-19
sources:
  - https://www.icy-veins.com/wow/weekly-to-do-list
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://wago.tools/db2/QuestV2?build=12.0.7.68367   # planner quest-ID verification (2026-07-02)
  - https://www.wowhead.com/quest=94446                 # prey_weekly title/objective
  - https://www.wowhead.com/quest=94385                 # void_assault (Eversong)
confidence: high
---

# Weekly Checklist — Midnight Season 1 (12.0.7, level 90)

Weekly reset: **Tuesday** (US). This is the anchor doc for "what should I do
this week?" questions.

## Every week, in rough priority order

1. **Open last week's Great Vault** (see `great-vault.md`).
2. **Buy bonus rolls from Decimus** — 2× Nebulous Voidcores per week, each
   costing 5,000 gold, 2,000 Voidlight Marl, or 80 Veteran Dawncrests.
   Requires the 12.0.5 Voidforge questline (Decimus, The Voidstorm 51.2 68.4),
   which also unlocks Ascendant Voidcore looting.
3. **Raid**: The Voidspire (6 bosses), The Dreamrift (1), and/or March on
   Quel'Danas (2) on your difficulty of choice (see `raids/overview.md`).
   World boss — weekly rotation of Lu'ashal / Thorm'belan / Predaxas /
   Cragpine.
4. **Mythic+**: farm keys up to **+10** for maximum Great Vault ilvl (272);
   higher keys are score/push only. Dungeon pool and affixes in
   `mythic-plus/season-1-overview.md`.
5. **Delves**: complete **at least one Tier 11** delve (weekly objective) and
   **4 Bountiful delves** for the weekly cache (ilvl 235–245). Pool of 10 in
   `delves/`.
6. **Prey hunts**: **3 Nightmare Prey hunts** for the weekly objective.
   Unlocked via Astalor Bloodsworn, Murder Row, Silvermoon (see `prey.md`).
   **12.0.7**: once you hit Preyseeker rank 10, the "Preferential Killing"
   once-per-week cap is **removed** — Custom Hunts become repeatable, so
   post-rank-10 farming is no longer throttled at 4/week. Prey also gives
   **more XP** now, and there's a new **"Big Prey Hunter (Season 1)" Feat
   of Strength**.
7. **Housing weekly** — quest from **Vaeli**, outside the Silvermoon bank.
8. **World event weekly** — quest from **Lady Liadrin**, rewards spark
   currency (gear crafting).
9. **Void Assault weekly** — rotates between Eversong Woods and Zul'Aman.
   Requires the Void Incursion intro questline once. **12.0.7**: XP from
   Void Assault wrapper quests, Strikes, and Incursions is **doubled**,
   drop rates for **Dark Particles** and **Bulging Satchels** are higher,
   and there are **new cosmetic vendors that take Dark Particles**.
10. **Renown**: work the 5 factions — Silvermoon Court, Amani Tribe,
    The Hara'ti, The Singularity, Slayer's Rise (see `../factions/`).
11. **Trading Post**: check the month's offerings / complete traveler's log.

> **12.0.7 catch-up XP buff**: XP is significantly increased for first-time
> delve completions (Delver's Call), Midnight dungeon quests, Prey hunts, and
> weekly Renown activities — alts level the season tracks much faster than they
> did on 12.0.5. Season 1 crest/Conquest **accumulation caps were also removed**
> (5/19 hotfix), so banked currency no longer wastes weekly progress.

## Rotating world events (check which is up)

- Saltheril's Soiree
- Abundance
- Stormarion Assault
- Harandar Relic

## Open-world extras (not strictly weekly, but currency-gated)

- **Ritual Sites** → Field Accolades (housing decor, mounts, pets, transmog).
  **12.0.7** adds a new **Tier 6** difficulty (6 challenges, UI-recommended
  ilvl ~274) rewarding **5 Mythic + 10 Heroic Dawncrests** per run, plus
  **new ritual-site weekly quests with bonus rolls** (notably on Weeks 3 and
  6 of the cycle) and the achievements *Advanced Ritual Site Studies* and
  *Pinnacle Ritual Work* (Ritual Breaker title). See `../systems/ritual-sites.md`
  and `dawncrests.md`.
- **Void Incursions / Void Strikes** (weekly quests after intro)
- **Abyss Anglers** — Depthdiver Jeju, off the Zul'Aman coast (68.2, 20.0)
- **Decor Duels** — hide-and-seek PvP queue in Silvermoon City

## Currencies cheat sheet

| Currency | Use |
|----------|-----|
| Nebulous Voidcores | Bonus rolls (raid) |
| Ascendant Voidcores | Higher-tier bonus rolls / upgrades (12.0.5) |
| Veteran Dawncrests | Gear upgrades; can buy Voidcores |
| Voidlight Marl | Catch-all 12.0.5 currency; can buy Voidcores |
| Field Accolades | Ritual Site cosmetics |

## Planner quest IDs (for PlannerState `ns.WEEKLY_QUESTS`)

Quest IDs the session planner gates on. Verified 2026-07-02 against **QuestV2 in
build 12.0.7.68367** (wago.tools) + Wowhead title/objective. Only confident IDs are
wired in the addon — a wrong/stale ID false-reports "done", which is worse than a gap.

| slug | quest | questID | confidence |
|------|-------|---------|------------|
| `prey_weekly` | "A Nightmarish Task" — obj *Nightmare Hunts completed (3)* | **94446** | high |
| `void_assault` | "Void Assaults: Eversong Woods" / "Zul'Aman" (rotates weekly) | **94385 / 94386** | high |

**Not yet resolved** (still show `(?)` in the planner — do NOT guess an ID):
- `delve_weekly_cache` — 93909 "Midnight: Delves" is a spark-**pillar** meta, not the bountiful-cache quest.
- `housing_weekly` — 93769 "Midnight: Housing" is the spark-pillar wrapper; the Vaeli quest-of-the-week rotates.
- `delve_tier_objective` — no discrete quest; Tier 11 is Great Vault progression, not a quest flag.
- `dungeon_weekly` — Halduron Brightwing's 1500-rep weekly; name/ID not exposed by any source.
- `liadrin_spark` — several Liadrin spark weeklies (93744 / 95245 / pillars); couldn't confirm which.

> Note: the spark-pillar metas each grant a *Spark of Radiance* and several stack per
> week, so a single `IsQuestFlaggedCompleted` check wouldn't cleanly mean "did that
> reward-specific weekly" — another reason those stay unwired.

## Verification note

Snapshot of the week of 2026-06-02 additionally showed: Legion Timewalking
active, Darkmoon Faire June 7–14, Thousand Boat Bash June 7–9. Event-of-the-
week data is volatile — **always re-check the Icy Veins page or in-game
calendar for "this week" specifics** rather than trusting this file.

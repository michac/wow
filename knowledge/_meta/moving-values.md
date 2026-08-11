---
title: Moving Values — flattened stale-data catcher
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1  # world-boss loot + rare/crest changes (hotfix 6/26–30)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Curse of Ula'tek content update notes
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 information (pre-season rules)
  - https://worldofwarcraft.com/en-us/news/24295085   # Lairs preview (Tidebound Grotto reward table)
confidence: high
---

# Moving Values Registry

**A flattened, latest-value-wins list of the facts that change patch-over-patch
*and* are commonly mislabeled on the web.** This is *not* a mirror of the KB —
the `knowledge/` topic files remain the full flattened current state. This file
is a narrow, high-signal oracle for one job:

> When a web source (or your own memory) says "the world boss drops Veteran
> gear," check here first. If the row says the current value is something else,
> the source is **stale** — reject or re-verify it.

## Scope — what belongs here

Only facts that (a) get **re-tuned across patches** and (b) are **frequently
wrong on Wowhead / Reddit / SEO sites** because the internet remembers an older
value. Typical rows:

- reward **quality/track** and **item level** of specific loot (world bosses,
  event vendors, catch-up currencies, raid drops)
- structural counts that keep changing (site rotations, tier counts, caps)
- tuning that **superseded** an earlier published value

**Does NOT belong here:** anything stable across patches, class rotation minutiae
(lives in `classes/`), or volatile *live* data like AH/token prices (never
cached — fetch live). If a fact stops moving, it can graduate out of this file.

## How to read a row

- **Current value** wins. **Was** records the immediately-prior value so you can
  recognize the stale version when you see it in the wild.
- **Set by** is the patch/hotfix that established the current value — the anchor
  for provenance.
- **KB home** is the topic file that carries the full claim + citation. This
  registry defers to it; if they ever disagree, the topic file wins and this
  row is stale.

## Registry

Legend: WT = World Tier · ilvl ranges are the drop/purchase band, not upgrades.

> ⚠ **12.1 shipped 2026-08-11 into a PRE-SEASON week; Midnight Season 2 opens
> 2026-08-18.** Rows below marked **(pre-season)** are true *only* for the week of
> Aug 11 and change on Aug 18 — they are the rows most likely to be mis-stated by
> a source written a week either side of the patch.

| Fact | Current value | Was | Set by | KB home |
|---|---|---|---|---|
| **Season 2 crests + upgrade bands** | **Mistcrests**, all five tiers confirmed from game data (`CurrencyTypes` DB2 @ 12.1.0.69214, currency IDs 3437–3441): **Adventurer Mistcrest** → ilvl **269–282** · **Veteran Mistcrest** → **282–295** · **Champion Mistcrest** → **295–308** · **Hero Mistcrest** → **308–321** · **Myth Mistcrest** → **321–334** | **Dawncrests** (Season 1): Adventurer 224–237 · Veteran 237–250 · Champion 250–263 · Hero 263–276 · Myth 276–289 | 12.1 | endgame/dawncrests.md |
| **Season 2 item level ceiling** | Season 2 gear runs **269 → 334** across the five tracks (from the Mistcrest upgrade bands above) | Season 1 ran **224 → 289** | 12.1 | endgame/dawncrests.md |
| **Delve rewards (pre-season)** | Tiers **1–11** + "?" Nemesis only; **no Bountiful Delves**; max reward **Adventurer 3/6 gear + Veteran crests**; **no Coffer Keys** | S1: full tiers, Bountiful, keys | 12.1 (pre-season week only) | endgame/delves/overview.md |
| **Mythic 0 lockout & loot (pre-season)** | **Weekly** lockout, drops **Champion 1/6 (ilvl 292)** — this week only; returns to **daily** on 2026-08-18 | Daily lockout (S1) | 12.1 (pre-season week only) | endgame/mythic-plus/keystones.md |
| **Mythic+ keystones** | **Do not drop until 2026-08-18** | Dropped throughout S1 | 12.1 | endgame/mythic-plus/keystones.md |
| **Raid Great Vault track** | LFR/Normal/Heroic vault rewards come in at the **first step of the next harder difficulty's track** (Heroic → **Myth 1/6**); Mythic vault at **Myth 6/6**, except Very Rare items and penultimate/final-boss loot which are **Myth 9** from either source | Vault matched the difficulty's own track | 12.1 | endgame/great-vault.md |
| **Great Vault World row (Season 2)** | **Champion 3/6** max in the *first* S2 vault; **Hero 1/6** max in every vault after | — | 12.1 | endgame/great-vault.md |
| **Nebulous Voidcore raid re-roll cost** | **1** | 2 | 12.1 | planning/activities/voidcores.md |
| **Nebulous Voidcores — availability** | S1 Voidcores **convert to gold** at S1 end and are unusable in S1 content; from S2 they are a **Great Vault reward**; bonus rolls are **absent from the first S2 vault** and arrive the week of **2026-08-25**, requiring **≥3 panes** unlocked; Orin Straylight (now near the Catalyst) grants **+1 per week from week 8 of S2** | S1: earned from Voidforge weeklies, 2/roll | 12.1 | planning/activities/voidcores.md |
| **Catalyst conversion** | Converted class-set armor now **inherits secondary and tertiary stats plus certain special cantrip effects** of the source item | Converted to base set stats | 12.1 | endgame/catalyst.md |
| **Class-set vendor Kirana** | **Near the Catalyst in Silvermoon**; stocks **Season 2** class sets for **Slumbering Coil Curios** | Near the March on Quel'danas raid entrance, S1 sets | 12.1 | endgame/catalyst.md |
| **Ritual Sites — recommended ilvl** | **T4 259 · T5 268 · T6 275**; T1–3 unchanged from S1. Tier 1–6 vault rewards + crests now match **Season 2 Delve** tiers 1–6 | T4 257 · T5 264 · T6 274; S1 Dawncrests | 12.1 | systems/ritual-sites.md |
| **Ritual Sites T6 bonus roll** | **Removed** — Advanced Ritual Studies quests no longer give a Nebulous Voidcore bonus roll (still completable for the achievement) | Gave a Voidcore bonus roll | 12.1 | systems/ritual-sites.md |
| **Void-Touched Caches (Field Accolades)** | **S2 Adventurer Warbound = 200** · **S2 Veteran BoP = 500** (random slot) / **750** (slot-specific). **The Season 1 caches were removed** | S1 caches at 100/750 | 12.1 | systems/void-incursions.md |
| **Val/Naigtal rewards** | World quests / rares / elites give **S2 Adventurer crests** (both World Tiers); rare gear stays Warbound-until-Equipped at **S2 Adventurer 1/6** (Normal) / **4/6** (Heroic); World Boss + weeklies give **S2 Adventurer** (Normal) / **S2 Veteran** (Heroic) crests | S1 crests; Heroic Warbound-until-equipped gear | 12.1 | endgame/world-events.md |
| World boss loot (Val/Naigtal "Midnight" rotation) | ⚠ **Frozen at Season 1 and no longer upgradeable** as of 12.1. (S1 values, historical: Warbound Heroic 1/6 Normal WT / Heroic 4/6 Heroic WT, + per-character Soulbound Champion 4/6 / Heroic 1/6.) The **"Knocking off the Top (Heroic)"** Mythic quest rewards are likewise frozen at S1 | Live, upgradeable S1 loot | 12.1 | endgame/world-events.md |
| **Lairs — Tidebound Grotto rewards** | **World** rec 273 → drops **279 (Veteran 1/6)** + Veteran Mistcrest · **Normal** 286 → **292 (Champion 1/6)** + Champion Mistcrest · **Heroic** 299 → **305 (Hero 1/6)** + Hero Mistcrest · **Mythic** 312 → **318 (Myth 1/6)** + Myth Mistcrest. BoP, **weekly lockout**, one Voidcore per week per lair | — (new format) | 12.1 | endgame/lairs.md |
| **Lair availability (pre-season)** | **World difficulty only** this week; Normal / Heroic / Mythic (flex 15–25) open **2026-08-18** | — | 12.1 (pre-season week only) | endgame/lairs.md |
| **Venomous Abyss — LFR minimum ilvl** | **273** | — (new raid) | 12.1 | endgame/raids/venomous-abyss.md |
| **Prey — Anguish housing prices** | **Substantially reduced**, for both Season 1 and Season 2 items | Higher S1 pricing | 12.1 | endgame/prey.md |
| **Prey — Nightmare rewards** | **Season 2 Champion** gear; Nightmare Mode is **not available until 2026-08-18** (Hard Prey drops **S2 Veteran** during the pre-season) | Champion-track (~ilvl 259–279) + Veteran Dawncrests | 12.1 | endgame/prey.md |
| **Gladiator's Distinction (PvP trinket set bonus)** | Tank/DPS **+15% primary** and **+5% Stamina**; healer **+10% Stamina** | Tank/DPS +12% primary, +10% Stam; healer +15% Stam | 12.1 | factions/slayers-rise.md |
| **Battleground healing received** | **−20%** | Unreduced | 12.1 | factions/slayers-rise.md |
| **Spoils of War Conquest bonus** | **+50%** once Conquest is uncapped for the season | +30% | 12.1 | planning/activities/pvp-conquest.md |
| **Max-level player health & creature damage** | **+25%** at max level; health-consumable values rescaled to match. Several DPS/Tank healing and absorb spells retuned to keep relative impact | Pre-12.1 baseline | 12.1 | changelog-12.1.md (Classes preamble) |
| **Diminishing-return reset timer** | **20 seconds** | 16 seconds | 12.1 | factions/slayers-rise.md |
| **Earthen zone-exploration XP** | Baseline exploration XP **−60%**; **low-level zones no longer reduced**; Ingest Minerals' Well Fed **+30%** | Full baseline exploration XP | 12.1 | systems/leveling-notes.md |
| **Houses — max level** | **12** | 10 | 12.1 | systems/housing.md |
| **Mythic+ dungeon pool** | **Season 2 (8):** Altar of Fangs · Murder Row · Den of Nalorakk · The Blinding Vale · Voidscar Arena · Ruby Life Pools · Kings' Rest · Temple of Sethraliss | S1 (8): Algeth'ar Academy · Magisters' Terrace · Maisara Caverns · Nexus-Point Xenas · Pit of Saron · Seat of the Triumvirate · Skyreach · Windrunner Spire | 12.1 | endgame/mythic-plus/season-2-overview.md |
| **Midnight S1 M+ title cutoffs (US, FINAL)** | Umbral Champion (top 1%) **3960** · Umbral Hero (top 0.1%) **4211** — historical, season closed | earlier in-season estimates | 12.1 (posted 8/4, updated 8/10) | endgame/mythic-plus/season-1-overview.md |
| **Turbulent Timeways** | **Ended 2026-08-11** | Ran Jun 30 – Aug 11 | 12.1 | planning/activities/turbulent-timeways.md |
| **Cooldown Manager tracked types** | Now also tracks **trinkets, potions, and racial ability cooldowns/durations** | Spells/abilities only | 12.1 | addon-dev/cooldown-manager.md |
| **Delve Coffer Key Shards** | Amounts **retuned across multiple sources**, weighted toward Coiled Isle content. ⚠ Blizzard calls this **ongoing / a work in progress** — treat any specific number as volatile | S1 shard rates | 12.1 | endgame/delves/overview.md |
| Field Accolades — Maren Silverwing vendor | Sells **slot-targeted Hero-track gear (~ilvl 259)** | Accolades = transmog/decor **only** | 12.0.7 | endgame/world-events.md |
| Val/Naigtal rares & Dark Particles | Rares drop **2× crests**; **Dark Particles** drop in Val/Naigtal, **stack to 1000** | pre-6/26 (1× crests, caches Soulbound) | 12.0.7 hotfix (6/26) | endgame/world-events.md |
| Prey — "Preferential Killing" weekly cap | **Removed** after rank 10 (Custom Hunts repeatable) | Once-per-week cap | 12.0.7 | endgame/prey.md |
| Sporefall raid — gear ilvl band | **259–298** (RF→Mythic) — previous tier as of 12.1 | — (new raid) | 12.0.7 | endgame/raids/sporefall.md |
| Ritual Sites — rotation & tiers | **3-site rotation, 6 tiers** | 2-site rotation, 5 tiers | 12.0.7 | systems/ritual-sites.md |
| Durability | Gear takes **no** durability damage from combat | Combat damaged durability | 12.0.7 | systems/professions.md |
| PvP gear item level | **+9** over previous season baseline | prior baseline | 12.0.7 | factions/slayers-rise.md |
| Crest / Conquest accumulation caps (Season 1) | **Removed** | Weekly accumulation caps | 12.0.7 hotfix (5/19) | endgame/weekly-checklist.md |

> **Maintenance:** `/update` (quick step 4 / full step F5) refreshes this file each patch —
> for every reward/tuning change in the ledger, either update an existing row's
> **Current value** (moving its old value into **Was**) or add a new row. Keep
> it short; prune rows whose value has been stable for two+ patches.

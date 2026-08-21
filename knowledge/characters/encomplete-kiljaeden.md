---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.1
fetched: 2026-08-20
reviewed: 2026-08-20
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
  - PlannerState /ps dump + Syndicator (currencies + items), 2026-08-20
confidence: high
---

# Encomplete – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). Re-fetch
> before answering gear/progress questions; this file is for context, not
> live state. Raw JSON: `raw/blizzard/encomplete-*.json`.
>
> ⚠ For **sims**, item IDs below are not enough — SimC needs the full
> `bonus_id` strings. Use the in-game **SimulationCraft addon** (`/simc`,
> or `/simc [item link]` for a single piece) and paste the export.
>
> **Δ since 2026-07-19 — this is the first post-12.1 / post-season-turnover
> snapshot, so most numbers moved for structural reasons, not just play.**
> **Patch 12.1 shipped 08-11 and Midnight Season 2 opened 08-18**; the crest
> currency changed (**Dawncrest → Mistcrest**), the upgrade-achievement ladder
> changed (**"…of the Dawn" → "…of the Mist"**), and the M+ season reset.
> Headlines: **equipped ilvl 279 → 294** (API avg 297) on a mostly-new S2 kit
> (Pyrewalker's head/waist/wrist at 295, **Anguine Gyre** ring at 305, both
> trinkets replaced with **305 S-tier** pieces, weapon **295 → 318**).
> **M+ rating 1723.7 → 794.0** is a *season reset*, not a fall — 11 S2 runs
> already logged including a **timed +11**. **★ The S1 "Hero of the Dawn"
> discount is now inert** (Dawncrests are dead currency) and Encomplete has
> **not** earned any "…of the Mist" rung — see *Mist ladder* below.
> Gold **14,575 → 30,072**. Currencies fresh (last login 2026-08-20 05:56 UTC).

**The user's current main.**

## Identity

- Gnome **Warlock**, active spec **Demonology** (hero tree **Diabolist**)
  — unchanged since 07-19. Affliction + Destruction loadouts still saved.
- Level **90** (cap), Alliance, guild **Dungeon Dojo**
- Titles: *Encomplete, Champion of the Frozen Wastes* · 8,725 achievement
  points (+540 since 07-19)
- Last login at fetch: 2026-08-20 05:56 UTC (fresh)

## Gear (equipped ilvl 294, API avg 297 — 2026-08-20)

**Season-2 turnover.** Eleven of the fifteen gear slots are new or re-tracked
since 07-19. The four that are **not** are the S1 **Abyssal Immolator's** tier
pieces, still sitting at **276 with no upgrade track** — they are the only thing
below 282 and they cannot be crested, only replaced (see *Mist ladder*).

| Slot | ilvl | Track | id | Item | Ench |
|---|---|---|---|---|---|
| Head | 295 | Champion 2/6 | 272234 | Pyrewalker's Miter | — |
| Neck | 292 | Champion 1/6 | 251142 | Pendant of Malefic Fury | *(n/a)* |
| Shoulders | **276** | — | 250040 | Abyssal Immolator's Fury *(S1 tier)* | — |
| Chest | **276** | — | 250045 | Abyssal Immolator's Dreadrobe *(S1 tier)* | Mark of the Worldsoul |
| Waist | 295 | Champion 2/6 | 272237 | Pyrewalker's Obi | *(n/a)* |
| Legs | **276** | — | 250041 | Abyssal Immolator's Pillars *(S1 tier)* | +41 Int & +4% Mana |
| Feet | 285 | — | 258584 | Lightbinder Treads | — |
| Wrist | 295 | Champion 2/6 | 272238 | Pyrewalker's Wraps | *(n/a)* |
| Hands | **276** | — | 250043 | Abyssal Immolator's Grasps *(S1 tier)* | *(n/a)* |
| Ring 1 | 295 | Champion 2/6 | 275528 | Preyhunter's Ring | — |
| Ring 2 | 305 | Hero 1/6 | 272148 | Anguine Gyre | — |
| Trinket 1 | 305 | Champion 5/6 | 250215 | Freightrunner's Flask | *(n/a)* |
| Trinket 2 | 305 | Champion 5/6 | 273649 | Stormbound Emblem of Dazar | *(n/a)* |
| Back | 292 | Champion 1/6 | 275524 | Preyhunter's Rugged Stole | — |
| Main Hand | 318 | — | 245770 | Aln'hara Cane | Acuity of the Ren'dorei |

*(Shirt 6097 and Tabard 43157 are cosmetic and excluded from every count here.)*

**Trinkets are now both S-tier for Demonology.** *Freightrunner's Flask* (250215)
and *Stormbound Emblem of Dazar* (273649) are both on the S-tier line of
`../classes/warlock/demonology/gearing.md`; the previous pair included
*Sylvan Wakrapuku*, which that same table rates **Junkyard**. This is the single
biggest quality jump in the kit and it is already done.

**Enchants — 3 of 9 enchantable slots filled.** Filled: **chest, legs, weapon**.
**Bare (6): head, shoulders, feet, cloak, ring 1, ring 2.** (Enchantable slots in
Midnight: helm, shoulders, cloak, chest, legs, feet, both rings, weapon. Neck
takes a gem, not an enchant; wrist takes an added socket.) Encomplete has
**Midnight Enchanting 25/100**, so these are self-craftable as recipes unlock —
still the cheapest gains on the character.

**Gems/sockets: none detected, and the S1 socketed pieces are all gone.** The API
item data returned no gems on any slot; the three socketed S1 items (Preyseeker's
Signet, Void-Laced Pendant, Void-Laced Ring) have all been replaced. Whether the
new neck/rings carry prismatic sockets is **not visible in this data** —
@verify-ingame: check the neck (251142), Ring 1 (275528) and Ring 2 (272148)
tooltips for empty sockets.

### Mist ladder — nothing earned yet (2026-08-20)

⚠ **The S1 "…of the Dawn" achievements are still on the account (Adventurer ✓ ·
Veteran ✓ · Champion ✓ · Hero ✓ · Myth ✗) but they are now INERT.** The discount
is per-crest-currency and Dawncrests are dead from S2 onward — see
`../endgame/dawncrests.md` § *The "…of the Mist" achievements*. The ladder reset
to zero for everybody on 08-18.

⚠ **`wowkb.character` still prints the S1 ladder.** Its digest reports
*"Champion 50% discount: LIVE — every slot ≥ 263"*, which is the hardcoded S1
gate (263 / achievement 42768) in `tools/wowkb/character.py:494`. **That line is
stale for Season 2 and must not be quoted.** Filed in `../_meta/kb-inbox.md`.

The live S2 ladder, and where Encomplete stands:

| Rung | Needs (high watermark, every slot) | Status |
|---|---|---|
| Adventurer of the Mist | **282** | ✗ — **4 slots short** |
| Veteran of the Mist | **295** | ✗ |
| Champion of the Mist | **308** | ✗ |
| Hero of the Mist | **321** | ✗ |
| Myth of the Mist | **331** average | ✗ |

**The only blockers on the first rung are the four S1 tier pieces**
(Shoulders / Chest / Legs / Hands, all **276**, all **no track**). They cannot be
crested — a trackless S1 piece has to be **replaced**. Any 282+ drop or a
Season-2 class-set piece in those four slots clears *Adventurer of the Mist* and
turns on the 50% warband Adventurer-Mistcrest discount.

**Encomplete has ZERO Season 2 class-set pieces.** The four *(tier)*-flagged
items above are the **Season 1** *Abyssal Immolator's* set, whose bonuses are
historical as of 12.1. The S2 Demonology set (2pc: Wild Imp +10% / Implosion
+20%; 4pc: imp self-detonation) is bought from **Kirana**, who moved to **next to
the Catalyst in Silvermoon** and sells it for **Slumbering Coil Curios**. So the
same four slots are simultaneously the Mist-ladder blocker *and* the missing 4pc
— they are the whole gearing story right now.

## Season 2 progress

- **Mythic+**: **Season 17 rating 794.0**, 11 runs on record. *(The 1723.7 in the
  prior snapshot was Season 1 and does not carry — this is a fresh ladder, and
  794 after two days is a strong start, not a regression.)*
  Best runs: **+11 Seat of the Triumvirate (timed, 28.7m)**, +10 Skyreach (timed),
  +9 Nexus-Point Xenas (timed), +8 Maisara Caverns (timed), +7 Windrunner Spire
  (timed). Untimed: +10 Algeth'ar Academy, +6 Magisters' Terrace, +6 Skyreach.
- **Raids**: **Sporefall [Normal] 1/1**. The Venomous Abyss (S2 raid) shows **no
  progress** — it opened 08-18. Naxx / Obsidian Sanctum entries are Wrath-era.

### Renown (API, 2026-08-20)

Midnight-relevant factions (older-expansion renowns omitted):

| Faction | Renown | Δ since 07-19 |
|---|---|---|
| Silvermoon Court | 15 (1357/2500) | **+1** |
| The Singularity | 10 (812/2500) | **+1** |
| Amani Tribe | 10 (295/2500) | **+1** |
| Hara'ti | 10 (5/2500) | **+2** |
| Ritual Sites | 5 (515/2500) | **+1** |
| Zul'jarra's Forces | 5 (130/2500) | **new to this snapshot** |
| Flame's Radiance | 1 (0/2500) | **new to this snapshot** |
| Gallagio Loyalty Rewards Club | 1 (0/2500) | new to this snapshot |
| The K'aresh Trust | 1 (0/2500) | — |

Maxed (25): The Severed Threads, The Assembly of the Deeps, Hallowfall Arathi,
Council of Dornogal. Cartels of Undermine **20**.
Companions: **Valeera Sanguinar lvl 56** (was 52 — continued delve activity),
**Brann Bronzebeard lvl 45** (unchanged).

### Currencies (Syndicator SavedVariables, snapshot 2026-08-20)

> Source: the **Syndicator** addon writes a per-character `currencyID → amount`
> table to disk; IDs resolved to names via wago.tools `CurrencyTypes` DB2
> (Tier-1). Reflects the character's last in-game `/reload` or logout — **fresh**
> (last login 2026-08-20 05:56 UTC). Deltas are vs the 2026-07-19 snapshot.

- **Mistcrests (the Season 2 currency): Adventurer 186 · Veteran 169 ·
  Champion 140 · Hero 28 · Myth 20.** These are a *new* currency, not a
  continuation — the S1 Dawncrest balances are gone and are not comparable.
  **No "…of the Mist" discount is active**, so upgrades cost the full **20 crests
  per rank** (`../endgame/dawncrests.md`). Champion 140 is the useful stock: the
  295 Champion 2/6 pieces cost 20/rank to push toward the 308 ceiling.
- **Field Accolade 1,235** (was 11 — **+1,224**, fully rebuilt after the S1
  Void-Laced spend).
- **Voidlight Marl 40,208** (was 25,179) · **Remnant of Anguish 4,341**
  (was 3,384) · **Undercoin 2,829** (was 21,757 — **−18.9k**, a large delve-vendor
  spend) · **Coffer Key Shards 298** (was 99) · Brimming Arcana 590 ·
  Shard of Dundun 8 · **Corrosive Coin 471** (new) · **Tidal Spark Dust 4** (new,
  the S2 spark-dust line) · **Venomblight Manaflux 1** (new — the S2 Catalyst
  charge currency, replacing Dawnlight Manaflux)
- Artisan Tailor's Moxie **925** (was 700) · Artisan Enchanter's Moxie **70**
  (was 55) · Artisan Skinner's Moxie 15
- Community Coupons **484** (was 211) · Trader's Tender 4,200 ·
  Resonance Crystals 380 · Dragon Isles Supplies 133 · Garrison Resources 140 ·
  Champion's Seal 35
- Gold **30,072g** (was 14,575 — **+15.5k**)
- **Crafting mats (from Syndicator items):** Sparks of Radiance **13** (was 12) ·
  Ascendant Voidshards **1** (unchanged). *(Items, read from Syndicator's
  bag/bank/warband inventory — not currencies.)*
- ⚠ **Absent from this dump vs 07-19:** Dawnlight Manaflux, Untainted
  Mana-Crystals, Nebulous Voidcore, Restored Coffer Key, Radiant Spark Dust.
  These are S1 currencies; the dump reports no balance, which may mean *zero* or
  *retired*. Do not plan spends against them.

### This reset (PlannerState, 2026-08-20)

- **Great Vault columns filled:** dungeon **3/3**, world **0/3**, raid **2/3**.
  *(The dump also emits a fourth column keyed `5` at `1/2` — unidentified; the
  vault doc doesn't name it. @verify-ingame: open the vault and record what the
  fourth row is.)*
- **World bosses killed this reset:** 0. **World vault row is empty (0/3)** —
  the cheapest unfilled vault progress on the character.
- **Active events:** PvP Brawl: Warsong Scramble · The Venomous Abyss ·
  Battleground Bonus Event.
- **Turbulent Timeways: ✓ complete** (Spawn of Vyranoth mount).
- ★ **Important quests flagged (purple-!):** Feathering the Nest ·
  Midnight: World Tour · Prismatic Potential · Veteran Symposium.
- Weeklies still open include prey_weekly, void_assault ×2, ritual_sites_weekly,
  delve_call_weekly, nalorakk_weekly, several special_assignments, and the
  Midnight world-tour chains (full list in the `/ps` dump).

### Season journeys — ⚠ SEASON 1 DATA, SUPERSEDED

The figures below were read from the in-game Journeys UI on **2026-06-03**, in
**Season 1**. Season 2 opened 2026-08-18 and reset these tracks. They are kept
only as a historical calibration point and must not be quoted as current.

- *(S1)* Prey rank 3, 0/4000 to rank 4 · Delves rank 3 "Treasure Hunter",
  1160/4200 to rank 4.
- *(S1, user-reported 2026-06-03)* cleared T9 delves solo at ~236 ilvl, some
  pulls rough — the only datapoint we have on solo-delve tuning for this
  character.

## Professions (API 2026-08-20)

- **Tailoring — Midnight tier MAXED (100/100)** (all older tiers maxed too).
  Self-crafts Midnight spark gear + both embellishments; no crafting orders
  needed.
- **Enchanting — Midnight 25/100** (was 21). Self-enchanting the six bare slots
  is gated on this leveling.
- Cooking 214/300, Fishing 135/300 (Classic tiers).

## Implications for advice

- **Gearing phase: equipped ilvl 294** on a fresh S2 kit with **both trinkets
  already S-tier** and a **318 weapon**. The kit is in good shape *except* for
  one cluster.
- **★ The one thing to fix: the four S1 tier slots (shoulders/chest/legs/hands,
  276, trackless).** They are simultaneously (a) the only slots below 282, so
  they alone block *Adventurer of the Mist* and its 50% warband discount, and
  (b) the reason there is **no Season 2 set bonus**. Route: Kirana (next to the
  Catalyst in Silvermoon) for **Slumbering Coil Curios**, the Catalyst, or any
  282+ drop in those slots. ⚠ The Catalyst now **preserves the source item's
  secondaries**, so *which* piece is fed to it is a real choice.
- **Cheap gains, in order:** the **six bare enchants**
  (head/shoulders/feet/cloak/ring1/ring2 — self-craftable), the **empty world
  vault row (0/3)**, and confirming whether the new neck/rings have sockets.
- **Crest stock:** Champion Mistcrest **140** is the spendable pile — enough to
  take a 295 Champion 2/6 piece to its **308** ceiling twice over at 20/rank.
  Hero **28** and Myth **20** are thin; Hero/Myth crests come from **M+ +4–8 /
  +9 and up** and **Heroic/Mythic Venomous Abyss** respectively.
- Spec context for KB lookups: `knowledge/classes/warlock/demonology/`
  (**active spec, Diabolist hero tree**; Affliction + Destruction loadouts also
  saved).

> **Active plan moved to `encomplete-plan.md`** (priority checklist,
> weekly rotation, spend rules, milestones). Section below kept as the
> 2026-06-03 reasoning record.

## Gearing plan (sketched 2026-06-03, ilvl 236 baseline)

Rationale: base spark crafts hit **259 at max quality with zero crests**
— 23 ilvls over current average. Tier slots (head/shoulders/chest/legs/
hands) are reserved for the Catalyst — **VERIFIED 2026-06-03: crafted
gear cannot be catalyzed in 12.0** (Icy Veins/Wowhead catalyst guides).
Craft crestless at 259 now; recraft to 285 with Myth Dawncrests later
(recrafts don't refund crests, so skip the Hero-crest detour).

Revised 2026-06-03 after digesting SignsOfKelani 12.0.5 gearing video —
**ritual sites are now the primary solo engine** (see
`../systems/ritual-sites.md`, `../systems/void-forge.md`):

1. Spark-craft (~10 sparks): belt 214→259, wrist 233→259, boots 227→259,
   and 2H staff 246→259 (4 sparks) — carries both embellishments.
   Recraft to 285 later with Myth Dawncrests (20/wk from 4× T11
   bountiful delves, or M+9s).
2. **Ritual sites** (start at whatever tier is comfortable at 236; T5 =
   100+ accolades + 20 Hero crests/run): T4–5 push the vault world row
   to 269; do the Silvermoon challenge-unlock quests early.
   ⚠ The 500-accolade hero piece is a **random slot** (video comments,
   unverified) — strong value *now* at zero hero pieces (any roll likely
   upgrades), decaying as slots fill. Front-load purchases early; once
   ~half the slots are hero-track, accolade runs are mainly for crests +
   vault and sparks/vault/M+ take over for targeting.
3. **Voidforge**: run Decimus's 6-quest line → 2 Nebulous Void Cores/wk
   (bonus-roll hero gear from delves/prey). Start Ascendant Nilhammer
   weekly chain now — 4 weeks to unlock weapon/trinket overcap
   (285 craft → 295).
4. Catalyst (6 charges): catalyze highest-ilvl non-tier drops in tier
   slots for 2pc→4pc; legs (214) and shoulders (224) most urgent —
   accolade champion/hero vendor pieces work as catalyst fodder
   (vendor gear ≠ crafted; verify once in-game). @verify-ingame
5. Champion crests (100+): upgrade champion-track drops; don't
   over-invest — hero pieces from accolades/delve renown 9 supersede.
6. Enchants on everything (zero detected at the 2026-06-03 snapshot;
   **partially done by the 2026-06-23 fetch** — chest/legs/ring1/weapon
   now enchanted, see the Gear table; neck/wrist/feet/ring2/back still
   open).
7. Tailoring: commission first crafts via crafting orders now; level
   Midnight Tailoring in background for self-crafting later.
8. Prey: **exactly 4 hunts/week** until Preyseeker rank 4 (first 4 =
   1,000 pts each, then 50 — never grind past 4) → Nightmare unlock
   questline → then beacon-only. Nightmare hunts drop Ascendant
   Voidshards. (Slayer's Rise: cosmetics-only PvP rep — deprioritized.)
9. Delves: **6 keyed bountifuls + the weekly quest item ≈ 1.3 Delver's
   Journey ranks/week** → rank 5 gear vendor ("nightcoin"/Untainted
   Mana Crystals — name unconfirmed), rank 9 = 276 hero vendor gear.
   Extra unkeyed runs = 125 rep, skip unless near a rank breakpoint.

API-tracked progress 2026-06-03: Ritual Sites renown 1, Valeera lvl 20.

## Talent audit (2026-06-03)

Active Affliction loadout simmed **−12.7% ST / −3.9% @4T** vs the simc
MID1 reference string on identical gear — 5 spec points in ≤3/50-usage
nodes (Withering Bolt ×2, Xavius' Gambit ×2, Improved Shadow Bolt) at
the cost of Improved Haunt / Patient Zero / Sow the Seeds / Drain Soul /
Cunning Cruelty, plus fringe defensive class picks over Demonic Circle /
Empowered Healthstone / Improved Mortal Coil. Details:
`../classes/warlock/affliction/builds.md` + `sims.md`.

## How to refresh currencies (no screenshots needed)

Currencies aren't in the Blizzard profile API, but the **Syndicator** addon
(already installed; it's the Baganator backend) logs them to disk. The WoW
install is readable from WSL, so the loop is fully local:

1. In-game on the character, type `/reload` (or just log out) — Syndicator
   flushes current values to its SavedVariables.
2. File: `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/WTF/Account/
   LLOYDCHRISTMAS/SavedVariables/Syndicator.lua` — per-character
   `["currencies"] = { [id] = amount }` map (+ `money` in copper).
3. Resolve IDs → names with wago.tools (tier-1):
   `uv run python -m wowkb.wago CurrencyTypes` → `raw/wago/CurrencyTypes.csv`
   (`ID`, `Name_lang`). New Midnight currencies 404 on the Blizzard Game
   Data API, so wago is the name source.

Note (updated 2026-07-11): **Sparks of Radiance / Ascendant Voidshards** are
items, not currencies — `wowkb.character` now reads them from Syndicator's
full bag/bank/warband inventory (`item_counts`), so they're no longer a gap.
**Catalyst charges = Dawnlight Manaflux** (currency 3378), also in the table.

## TODO

- [ ] Re-snapshot after gearing sessions (or just fetch live per doctrine)
- [ ] Re-audit talents after they respec (and re-sim with enchants on)
- [ ] Add WCL character parses subcommand to `wowkb.wcl` for this character
- [x] Verified 2026-06-03: crafted gear CANNOT be catalyzed in 12.0
- [x] Crest names confirmed: **Dawncrests** (Adventurer/Veteran/Champion/
      Hero/Myth tiers)
- [ ] Midnight Tailoring leveling cost (knowledge points, recipe access)
- [ ] Fix Demo `gearing.md` gem list: it prints "Flawless Versatile Garnet"
      but Demo's stat priority is Mastery≈Crit>>Vers — Vers is Demo's worst
      secondary. Should be a Crit (Deadly) / Mastery (Masterful) cut + the
      unique Eversong Diamond.

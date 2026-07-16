---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.0.7
fetched: 2026-07-16
reviewed: 2026-07-16
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
  - PlannerState /ps dump + Syndicator (currencies), 2026-07-16
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
> **Δ since 2026-07-11 (re-sync 07-16):** ★ **Two slots from HERO OF THE DAWN.**
> Equipped ilvl **274 → 276**; **14 of 16 slots are now ≥ 276**, leaving only
> **Neck (263, Champion 6/6)** and **Ring 2 (263, Champion 6/6)** below the Hero
> ceiling. Upgrades this week: **Ring 1** crested **266 → 276 Hero 6/6**; **Waist**
> swapped to *Archmage's Cord of Light* **276 Myth 2/6** (from the 263 Sprawling
> Rhizomecord); **Feet** swapped to *Lightbinder Treads* **276 Myth 2/6** (from the
> 263 Voidwind Boots) — first two **Myth-track** slots. **Spec swapped
> Demonology → Affliction** (hero tree **Diabolist → Soul Harvester**; Demo +
> Destro loadouts still saved). **Crests rebuilt hard** (a week of farming):
> **Hero 26 → 97**, **Myth 34 → 64**, **Champion 56 → 84**; **Field Accolade
> 219 → 911** (the stockpile is back). Gold **10,188 → 12,386**. M+ rating
> unchanged at **1434.5** (no new runs). Currencies fresh (last login 2026-07-16
> 19:28 UTC). See the **Hero of the Dawn** section below for the exact gap.

**The user's current main.**

## Identity

- Gnome **Warlock**, active spec **Affliction** (hero tree **Soul Harvester**)
  — **swapped from Demonology/Diabolist since the 07-11 snapshot**. Demonology
  + Destruction loadouts still saved (all three present via API).
- Level **90** (cap), Alliance, guild **Dungeon Dojo** (was The Soggy
  Bottom Boys)
- Title: Champion of the Frozen Wastes · 8,100 achievement points
- Last login at fetch: 2026-07-16 19:28 UTC (fresh)

## Gear (equipped ilvl 276, API 2026-07-16)

**2026-07-16 update:** **Ring 1** crested **266 → 276 Hero 6/6**; **Waist** and
**Feet** both swapped to fresh **Myth 2/6 (276)** pieces (*Archmage's Cord of
Light*, *Lightbinder Treads*). Equipped ilvl **274 → 276**. **14 of 16 slots
are now ≥ 276** — only **Neck (263)** and **Ring 2 (263)**, both Champion 6/6
and track-capped, still sit below the Hero ceiling (see **Hero of the Dawn**
below). 4pc tier **Abyssal Immolator's** + 285 weapon + 285 crafted back unchanged.

| Slot | ilvl | Track | id | Item |
|---|---|---|---|---|
| Head | 276 | Hero 6/6 | 250042 | Abyssal Immolator's Smoldering Flames *(tier)* |
| Neck | **263** | **Champion 6/6** | 249626 | Nocturnal Thorncharm (gem: Flawless Quick Garnet) — **below Hero ceiling** |
| Shoulders | 276 | Hero 6/6 | 250040 | Abyssal Immolator's Fury *(tier)* |
| Chest | 276 | Hero 6/6 | 250045 | Abyssal Immolator's Dreadrobe *(tier)* — ench: Mark of the Worldsoul |
| Waist | 276 | Myth 2/6 | 276794 | **Archmage's Cord of Light** *(new — was 263 Sprawling Rhizomecord)* |
| Legs | 276 | Hero 6/6 | 250041 | Abyssal Immolator's Pillars *(tier)* — ench: +41 Int |
| Feet | 276 | Myth 2/6 | 258584 | **Lightbinder Treads** *(new — was 263 Voidwind Boots)* |
| Wrist | 276 | Hero 6/6 | 263849 | Void Nemesis' Bracers |
| Hands | 276 | Hero 6/6 | 263813 | Handguards of Voidcendence |
| Ring 1 | 276 | Hero 6/6 | 259912 | Preyseeker's Signet *(266 → 276)* — ench: Eyes of the Eagle (gem: Flawless Quick Garnet) |
| Ring 2 | **263** | **Champion 6/6** | 249620 | Vibrant Wilderloop (gem: Eversong Diamond) — **below Hero ceiling** |
| Trinket 1 | 276 | Hero 6/6 | 248583 | Drum of Renewed Bonds |
| Trinket 2 | 276 | Hero 6/6 | 251784 | Sylvan Wakrapuku |
| Back | 285 | — | 239656 | Adherent's Silken Shroud *(crafted)* |
| Main Hand | 285 | — | 245770 | Aln'hara Cane — ench: Acuity of the Ren'dorei |

Enchanted slots: chest, legs, ring1, weapon. **Missing enchants:** neck,
wrist, feet, ring2, back (the 285 cloak — enchant it). With 14/16 slots at
276+, the remaining gains are **Myth-track upgrades (waist/feet 2/6 → 285) and
vault/M+**, plus closing the five bare enchants. (Encomplete leveled
**Enchanting** — see Professions — so those enchants are self-craftable.)

### Hero of the Dawn — how close (2026-07-16)

**Two slots away.** *Hero of the Dawn* (achievement **42769**) fires when
**every slot is ≥ 276** (the Hero-track ceiling); it then grants a **50%
Hero-Dawncrest discount warband-wide** + unlocks the Vaskarn **Hero → Myth**
trade (see `../endgame/dawncrests.md`). Encomplete has **14/16 at 276+** — the
only holdouts are:

| Slot | Now | Item | Why stuck | Fix |
|---|---|---|---|---|
| **Neck** | 263 (Champion 6/6) | Nocturnal Thorncharm | Champion track **caps at 263** — can't crest higher | **Replace** with a Hero/Myth neck, crest to 276 |
| **Ring 2** | 263 (Champion 6/6) | Vibrant Wilderloop | Champion track **caps at 263** | **Replace** with a Hero/Myth ring, crest to 276 |

- **It's a replace, not a crest-up** — both are already Champion 6/6 (ceiling),
  so upgrading in place is impossible; Encomplete needs a **Hero-track (or Myth)
  neck and ring**, then crest each to 276 (6/6).
- **Sources for a ≥276 neck + ring:** Great Vault Hero/Myth pick (M+ 1434 rating
  → the +11 row can offer them), **Heroic Sporefall** bosses, **T6 ritual sites**
  (Myth crests), or the **Vaskarn Champion → Hero** trade (unlocked; Encomplete
  holds 84 Champion + 289/55 lower crests to convert 3:1 in a pinch).
- **Crest math:** a *fresh* Hero drop (259, 1/6) → 276 costs **~150 Hero
  crests**; Encomplete holds **97 Hero + 64 Myth** — roughly one full piece now,
  the second after a bit more farming (or free if either lands at 276 from a
  Myth vault). **No Hero-crest discount applies yet** (that's the reward for
  *this* achievement — chicken-and-egg, pay full for these two).
- **Bottom line:** Encomplete is the account's closest to the next Dawn rung —
  land any Hero/Myth **neck and ring** and crest them out, and *Hero of the Dawn*
  (and the warband 50% Hero discount) is done.

## Season 1 progress

- **Mythic+**: **rating 1434.5 — unchanged since 07-11** (no new runs this
  sync). 7 runs on record: **+11 Seat of the Triumvirate (timed)**, +7 Skyreach
  (timed), +6 Skyreach (over time), +5 Algeth'ar Academy, +5 Maisara Caverns,
  +4 Magisters' Terrace, +4 Nexus-Point Xenas.
- **Raids**: **Sporefall [Normal] 1/1** (first Midnight raid kill on the API —
  Rotmire down on Normal). Older Naxx/Obsidian entries are Wrath-era.

### Renown (API, 2026-07-16)

Midnight-relevant factions (older-expansion renowns omitted):

| Faction | Renown | Δ since 07-11 |
|---|---|---|
| Silvermoon Court | 14 (870/2500) | +1 |
| The Singularity | 9 (937/2500) | +1 |
| Amani Tribe | 9 (1995/2500) | +1200 pts |
| Hara'ti | 8 (2180/2500) | +1500 pts |
| Ritual Sites | 4 (467/2500) | — |
| The K'aresh Trust | 1 (0/2500) | — |

Maxed (25): The Severed Threads, The Assembly of the Deeps, Hallowfall Arathi,
Council of Dornogal. Cartels of Undermine **20**.
Companion/delve tracks: **Brann Bronzebeard lvl 45**, **Valeera Sanguinar
lvl 49** (was 46 on 07-11 — continued delve activity).

### Currencies (Syndicator SavedVariables, snapshot 2026-07-16)

> Source: the **Syndicator** addon writes a per-character `currencyID →
> amount` table to disk; IDs resolved to names via wago.tools
> `CurrencyTypes` DB2 (tier-1). Reflects the character's last in-game
> `/reload` or logout (fresh — last login 2026-07-16 19:28 UTC).
> Deltas below are vs the 2026-07-11 snapshot.

- **Dawncrests: Adventurer 289 · Veteran 55 · Champion 84 · Hero 97 ·
  Myth 64.** A big rebuild week (opposite of the 07-11 spend): **Hero 26 → 97**
  (+71), **Myth 34 → 64** (+30), **Champion 56 → 84** (+28). This is the
  **Hero/Myth stockpile Encomplete needs for the last two Hero-of-the-Dawn slots**
  (neck/ring — see the Gear section). The **50% Champion discount stays LIVE**
  (Champion of the Dawn 42768 earned) — that's the *Champion* tier, unaffected by
  the pending Hero rung. See `../endgame/dawncrests.md`.
- **Field Accolade 911** (was 219 — **+692 rebuilt**; the stockpile drained into
  Uncomplete's warbound caches is back).
- Coffer Key Shards **96** (was 58) · Restored Coffer Key **4** ·
  Nebulous Voidcore **10**
- Undercoin **19,889** · Voidlight Marl **22,711** · Remnant of Anguish
  **3,384** · Brimming Arcana **590** · Radiant Spark Dust **18** ·
  Dawnlight Manaflux **7** · Untainted Mana-Crystals **340** (was 160) ·
  Shard of Dundun **8**
- Artisan Tailor's Moxie **600** · Artisan Enchanter's Moxie **40** ·
  Artisan Skinner's Moxie **15**
- Community Coupons **182** · Trader's Tender 4,200 · Resonance Crystals 380
- Gold **12,386g** (was 10,188 — **+2.2k**)
- **Crafting mats (from Syndicator items):** Sparks of Radiance **10** ·
  Ascendant Voidshards **1**. *(Items, read from Syndicator's bag/bank/warband
  inventory. Catalyst charges = Dawnlight Manaflux, currency 3378, listed above.)*

### Season journeys (in-game Journeys UI, 2026-06-03 — STALE; delve/prey ranks have almost certainly advanced, cf. Brann 45 / Valeera 43 above)

- **Prey: Season 1 — rank 3, progress 0/4000 to rank 4.** Rank 4 rewards:
  **Prey: Nightmare Mode** + "A Plinth Above the Rest I" — confirms the
  plan's Preyseeker-rank-4 → Nightmare unlock. 4,000 pts = exactly this
  week's 4× 1,000-pt hunts → **rank 4 is reachable this week**.
- **Delves: Season 1 — rank 3 ("Treasure Hunter"), 1160/4200 to rank 4
  ("Gilded Jackpot"** — the Myth-crest gilded stashes). Rank 5 = "An
  Ethereal and a Golem walk into a Delve" (Valeera shown on the pane),
  rank 6 = "Keys and Coffers".

Delve tier / Brann level: not exposed by API.
User-reported 2026-06-03: **clears T9 delves solo at ~236, but some
pulls are rough** — calibration point for content recommendations.

## Professions (API 2026-07-16 — unchanged since 07-11)

- **Tailoring — Midnight tier MAXED (100/100)** (all older tiers maxed
  too). Big shift: on 2026-06-03 there was no Midnight tailoring tier at
  all. Can now **self-craft Midnight spark gear** (belt/wrist/boots/cloak
  + the 2H staff, both embellishments) instead of using crafting orders.
- **Enchanting — Midnight 21/100** (replaces the old Skinning slot).
  Encomplete can now **self-enchant** the missing slots (neck/wrist/feet/
  ring2/back) as the profession levels — closes the enchant gap noted above.
- Cooking 214/300, Fishing 135/300 (Classic tiers).

## Implications for advice

- **Gearing phase: equipped ilvl 276** (was 236 on 06-03), 4pc tier + 285
  weapon + 285 crafted back, **14/16 slots ≥ 276**. Upgrades now come from
  **Myth-track (waist/feet at 2/6 → 285), M+ vault, and Heroic raid/ritual-site
  Hero+ gear**.
- **Priority target = the two Hero-of-the-Dawn holdouts, Neck + Ring 2 (both
  263, Champion-capped).** Landing a Hero/Myth neck and ring and cresting them
  to 276 clears *Hero of the Dawn* (42769) → **50% Hero-Dawncrest discount
  warband-wide** (see the Gear section's Hero-of-the-Dawn table). Encomplete has
  rebuilt the crest bank for exactly this (**Hero 97 / Myth 64**). After that,
  the Myth-track waist/feet (2/6) toward 285 and the five bare enchants
  (neck/wrist/feet/ring2/back — self-craftable via Enchanting) are the next gains.
- **Enchants are now self-served** — Encomplete leveled Enchanting; the
  five bare slots (neck/wrist/feet/ring2/back) are the cheapest gains left.
- **Tailoring is maxed (Midnight 100/100)** — self-crafts spark gear and
  both embellishments; no longer needs crafting orders.
- Spec context for KB lookups: `knowledge/classes/warlock/affliction/`
  (**active spec as of 2026-07-16, Soul Harvester hero tree** — swapped from
  Demonology/Diabolist; Demonology + Destruction loadouts also saved, see the
  other `warlock/*` dirs).

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

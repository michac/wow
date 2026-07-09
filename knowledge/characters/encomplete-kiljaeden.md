---
title: Encomplete – Kil'jaeden (US) — main character snapshot
patch: 12.0.7
fetched: 2026-07-09
reviewed: 2026-07-09
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
  - PlannerState /ps dump + Syndicator (currencies), 2026-07-09
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

**The user's current main.**

## Identity

- Gnome **Warlock**, active spec **Demonology** (hero tree **Diabolist**:
  Diabolic Ritual, Infernal Machine, Abyssal Dominion, Ruination).
  Destruction + Affliction loadouts also saved (all three now confirmed
  present via API).
- Level **90** (cap), Alliance, guild **Dungeon Dojo** (was The Soggy
  Bottom Boys)
- Title: Champion of the Frozen Wastes · 8,025 achievement points
- Last login at fetch: 2026-07-09

## Gear (equipped ilvl 272, API 2026-07-07)

**2026-07-07 update:** crafted the **Adherent's Silken Shroud** cloak (285) —
fills the old **back (250)** hole, which had been the standout weak slot.
Equipped ilvl **270 → 272**. Everything else unchanged since 07-02: 4pc tier
**Abyssal Immolator's** (head/shoulders/chest/legs, 276) + 285 weapon, now + a
285 back.

| Slot | ilvl | id | Item |
|---|---|---|---|
| Head | 276 | 250042 | Abyssal Immolator's Smoldering Flames *(tier)* |
| Neck | 263 | 249626 | Nocturnal Thorncharm (gem: Quick Garnet) |
| Shoulders | 276 | 250040 | Abyssal Immolator's Fury *(tier)* |
| Chest | 276 | 250045 | Abyssal Immolator's Dreadrobe *(tier)* — ench: Mark of the Worldsoul |
| Waist | 259 | 239649 | Martyr's Waistwrap |
| Legs | 276 | 250041 | Abyssal Immolator's Pillars *(tier)* — ench: +41 Int |
| Feet | 276 | 263783 | Voidwind Boots |
| Wrist | 266 | 263849 | Void Nemesis' Bracers |
| Hands | 276 | 263813 | Handguards of Voidcendence |
| Ring 1 | 266 | 259912 | Preyseeker's Signet — ench: Eyes of the Eagle (gem: Quick Garnet) |
| Ring 2 | 259 | 249620 | Vibrant Wilderloop (gem: Eversong Diamond) |
| Trinket 1 | 276 | 248583 | Drum of Renewed Bonds |
| Trinket 2 | 259 | 251784 | Sylvan Wakrapuku |
| Back | 285 | 239656 | **Adherent's Silken Shroud** *(crafted 2026-07-07)* |
| Main Hand | 285 | 245770 | Aln'hara Cane — ench: Acuity of the Ren'dorei |

Enchanted slots: chest, legs, ring1, weapon. **Missing enchants:** neck,
wrist, feet, ring2, back (the new 285 cloak — enchant it). Weakest slots vs
the 276 tier are now **waist / ring2 / trinket2 (all 259)** — the back hole is
closed. (Note: Encomplete leveled **Enchanting** — see Professions — so the
missing enchants are now self-craftable.)

## Season 1 progress

- **Mythic+**: **now rated — 1093 IO (Season 1).** 5 timed runs on record:
  +7 Skyreach, +5 Maisara Caverns, +5 Algeth'ar Academy, +4 Magisters'
  Terrace, +4 Nexus-Point Xenas. No runs logged this reset period yet.
  (Was zero rated runs on 2026-06-23 — has since started keying.)
- **Raids**: **Sporefall [Normal] 1/1** now recorded (first Midnight raid
  kill on the API — Rotmire down on Normal). Older Naxx/Obsidian entries are
  Wrath-era.

### Renown (API, 2026-07-02)

| Faction | Renown | Δ since 06-03 |
|---|---|---|
| Silvermoon Court | 12 | +2 |
| The Singularity | 8 | +3 |
| Amani Tribe | 8 | +2 |
| Hara'ti | 7 | +2 |
| Ritual Sites | 4 | +3 |
| Slayer's Duellum | Neutral (300/3000) | now unlocked (was no standing) |

Companion/delve tracks: **Brann Bronzebeard lvl 45**, **Valeera Sanguinar
lvl 43** (was Valeera 20 on 06-03 — heavy delve activity since).

### Currencies (Syndicator SavedVariables, snapshot 2026-07-09)

> Source: the **Syndicator** addon writes a per-character `currencyID →
> amount` table to disk; IDs resolved to names via wago.tools
> `CurrencyTypes` DB2 (tier-1). Reflects the character's last in-game
> `/reload` or logout. See "How to refresh currencies" at the bottom.
> Deltas below are vs the 2026-07-07 snapshot.

- **Dawncrests: Adventurer 289 · Veteran 55 · Champion 96 · Hero 176 ·
  Myth 20.** Unchanged since 07-07 — plenty of Hero/Myth on hand for slot
  upgrades and the next recraft-to-285. (Champion 96 could bankroll a chunk
  of Uncomplete's Champion cap via the *free same-slot warband upgrade*, not
  a raw-crest transfer — see `../endgame/dawncrests.md`.)
- **Field Accolade 219** (was **1,309** on 07-07 — **−1,090**, deliberately
  drained: spent on **Warbound Champion/Heroic caches mailed to Uncomplete**
  to gear the alt). Now below the 750 Heroic-cache threshold; the stockpile
  was routed into the warband rather than his own already-Hero slots (which
  Accolade boxes can't upgrade anyway).
- Coffer Key Shards **58** · Nebulous Voidcore **11**
- Undercoin **21,610** · Voidlight Marl **20,176** · Remnant of Anguish
  **3,384** · Brimming Arcana **590** · Radiant Spark Dust **17** ·
  Dawnlight Manaflux **5** · Untainted Mana-Crystals **160** ·
  Shard of Dundun **8**
- Artisan Tailor's Moxie **580** (Midnight Tailoring knowledge currency)
- Community Coupons **182** · Trader's Tender 4,000 · Resonance Crystals 380
- Gold **~11,829g** (was ~42,252 — **−30k**, spent on the cloak
  craft / mats and gear this week)
- **Not in Syndicator's currency table:** Sparks of Radiance and Catalyst
  charges (Sparks is an item, Catalyst charges are tracked separately) —
  still need eyeballs in-game for those two.

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

## Professions (API 2026-07-02 — changed since 06-23)

- **Tailoring — Midnight tier MAXED (100/100)** (all older tiers maxed
  too). Big shift: on 2026-06-03 there was no Midnight tailoring tier at
  all. Can now **self-craft Midnight spark gear** (belt/wrist/boots/cloak
  + the 2H staff, both embellishments) instead of using crafting orders.
- **Enchanting — Midnight 21/100** (replaces the old Skinning slot).
  Encomplete can now **self-enchant** the missing slots (neck/wrist/feet/
  ring2/back) as the profession levels — closes the enchant gap noted above.
- Cooking 214/300, Fishing 135/300 (Classic tiers).

## Implications for advice

- **Gearing phase has moved up: equipped ilvl 272** (was 236 on 06-03),
  4pc tier + 285 weapon + 285 crafted back. Base spark crafts (259) no
  longer upgrade any slot — upgrades now come from **Myth-track recrafts
  (285), M+ vault, and delve/ritual-site hero+ gear**. The old "spark-craft
  the 214/224 slots" advice is done.
- **Weakest slots to target: waist / ring2 / trinket2 (all 259)** — the
  back (250) hole is closed by the crafted 285 cloak. His own upgrades now
  come from **crest-ups (Hero 176 / Myth 20) and M+/vault**, not Accolades:
  he **spent his ~1,090-Accolade stockpile (down to 219) funding Uncomplete's
  gear** (warbound caches), which is the right call — Accolade slot-boxes
  land at 259 and can't beat his 259 slots anyway. Enchant the new back too.
- **Enchants are now self-served** — Encomplete leveled Enchanting; the
  five bare slots (neck/wrist/feet/ring2/back) are the cheapest gains left.
- **Tailoring is maxed (Midnight 100/100)** — self-crafts spark gear and
  both embellishments; no longer needs crafting orders.
- Spec context for KB lookups: `knowledge/classes/warlock/demonology/`
  (active spec, Diabolist hero tree, confirmed 2026-07-02; Destruction +
  Affliction loadouts also saved, see the other `warlock/*` dirs).

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

Gaps: **Sparks of Radiance** (an item, not a currency) and **Catalyst
charges** aren't in Syndicator's currency table — read those in-game.
A tiny purpose-built dump addon could close even those (see chat).

## TODO

- [ ] Re-snapshot after gearing sessions (or just fetch live per doctrine)
- [ ] Re-audit talents after they respec (and re-sim with enchants on)
- [ ] Add WCL character parses subcommand to `wowkb.wcl` for this character
- [x] Verified 2026-06-03: crafted gear CANNOT be catalyzed in 12.0
- [x] Crest names confirmed: **Dawncrests** (Adventurer/Veteran/Champion/
      Hero/Myth tiers)
- [ ] Midnight Tailoring leveling cost (knowledge points, recipe access)

---
title: Professions & Spark Crafting (Midnight)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963   # Coiled Isle — Zul'jarra renown recipes, Tokka's Crew, Er'inye vendor (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281            # 12.1 Content Update Notes — dye streamline (Tier 1)
  - https://news.blizzard.com/en-us/article/24295090           # 12.1 pre-season details — "Crafting Sparks will also begin dropping" (Tier 1)
  - https://www.wowhead.com/ptr/item=274476/spark-of-tides      # Spark of Tides, the S2 spark (game data)
  - https://www.wowhead.com/news/quality-of-life-improvements-coming-in-curse-of-ulatek-profession-knowledge-382059  # one-time KP reset (Tier 3 relaying a blue post)
  - https://www.method.gg/guides/all-profession-changes-and-new-recipes-in-wow-midnight-patch-12-1  # new mats/embellishments (Tier 3)
  - https://www.icy-veins.com/wow/spark-crafting-guide
  - https://www.method.gg/guides/how-to-gear-fast-and-reach-item-level-289-for-midnight-season-1
  - https://www.wowhead.com/news/sparks-of-radiance-for-crafting-now-available-in-midnight-easiest-spark-quest-380617
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://www.wowhead.com/news/save-gold-on-repairs-with-weapon-durability-changes-in-patch-12-0-7-381744
confidence: medium
---

# Professions (Midnight)

Crafting orders, spark crafting, knowledge points.

> ⚠ **12.1 shipped 2026-08-11; Midnight Season 2 does not open until 2026-08-18.**
> The week between is an official **pre-season week**. Crafting Sparks *do* drop
> during it (Tier 1, pre-season blue post) — so spark accrual starts today even
> though the season does not. The **Coiled Isle profession content below is live
> now**, since the zone and Zul'jarra's Forces renown are pre-season content.

## Season 2 spark crafting (12.1) — Spark of Tides

**Spark of Tides** (item **274476**) is the **Season 2** crafting spark,
replacing Season 1's Spark of Radiance. Confirmed by name + id from game data;
Icy Veins' spark guide was restamped "updated for Midnight Season 2 launch" on
2026-08-11.

- **Sparks begin dropping during the pre-season week** (Tier 1: *"Crafting
  Sparks will also begin dropping during the pre-season."*). Acquisition is
  otherwise the same shape as S1 — a capped weekly from **Lady Liadrin** plus
  catch-up — but the exact S2 quest list is **not** in the Tier-1 notes.
  @verify-ingame: read Liadrin's weekly options and the seasonal spark cap on
  or after 2026-08-18.
- **Season 2 gear runs ilvl 269 → 334** across the five tracks — this is the
  Tier-1 floor, derived from the `CurrencyTypes` DB2 Mistcrest upgrade bands at
  build 12.1.0.69214 (`_meta/moving-values.md`). ⚠ Icy Veins' S2 item-level
  chart says "+46, ending at 344"; **we keep the game-data number** and treat
  344 as unverified editorial.
- **Where crafted gear lands inside that ladder is not published at Tier 1.**
  Tier-3/4 guides say Champion-range crafts consume **Sparks of Tides only**,
  while **Hero and Myth crafts need Sparks *plus* the matching Mistcrest** —
  i.e. the S1 "80 crests as an optional reagent" shape carried forward with the
  crest renamed. **Do not quote a crafted ilvl bracket for S2 until it's
  measured.** @verify-ingame: open a spark recipe and read the optional-reagent
  slots + the quality ilvl ladder.

Everything below about **orders, order types, missives, recrafting,
embellishments and the 2-embellishment cap** is *system* mechanics and carries
forward unchanged into Season 2; only the spark item, the crest name and the
ilvl numbers moved.

## Coiled Isle profession content (12.1)

The Coiled Isle is the patch's profession hub. Three vendors matter, and all
three price profession goods in **profession-specific Artisan Moxies** (the
same Artisan \<Profession\>'s Moxie currency the Hara'ti and Silvermoon Court
vendors already use) on top of a zone currency.

### Jan'sari the Watchful — Zul'jarra's Forces quartermaster

At **Tokka's Landing**. Zone currency **Voidlight Marl**; profession items also
cost **Artisan Moxies**. Faction track: `../factions/zuljarras-forces.md`.

- **Renown 5 — "Coiled Isle Crafting"** unlocks nine recipes for purchase:

  | Recipe | Item id |
  |---|---|
  | Recipe: Loa's Gathering | 275300 |
  | Recipe: Concentrated Silvermoon Health Potion | 271885 |
  | Formula: Rite of the Hash'ey | 273073 |
  | Technique: Vantus Rune: Tides | 272196 |
  | Technique: Contract: Zul'jarra's Forces | 277967 |
  | Schematic: Coiled Amani Hookshot | 275316 |
  | Formula: Keen Hex Mask | 275310 |
  | Pattern: Flat Snakeskin Canopy | 275332 |
  | Plans: Amani Forgemaster's Workbench | 275304 |

  (Blizzard's article prints the hookshot as "Schematic: Coiled Hookshot"; the
  item's real name in game data is **Coiled Amani Hookshot** — name resolved via
  the Wowhead item DB, not the prose.)

- **Renown 5 — "Gone Cursed Fishin'"**: a **Fishing** recipe for the
  **Ula'tek Snakehead Lure** (item 277821), also from Jan'sari.
- **Renown 6 — "Demystifyin' Professions"**: **profession knowledge tomes** go
  on sale at Jan'sari. Tier-4 guides quote **750 Voidlight Marl + 75 or 150 of
  the matching Artisan Moxie** per tome; the Tier-1 article gives no price.
  @verify-ingame: read the tome prices off Jan'sari at R6.

**Renown 6 is therefore the profession-relevant breakpoint on this track** —
R5 is recipes you may or may not want, R6 is knowledge points, which are
permanent power for every crafter.

### Second Mate Sluggs — Captain Tokka's Crew (fishing)

At **Tokka's Folly**. Tokka is the tortollan sea captain behind **Venom
Fishing**; his crew is a **5-rank friendship faction** (Stranger → Doomed
Sailor → Cursed Angler → Venom Trawler → Bloodsworn Crew) fed by dailies,
fishing up artifacts, and killing his old crew. Killing a **Curse Surge** rare
elite opens a cursed fishing pool at that location.

Currencies here: **Coiled Filament** (the fishing currency), Voidlight Marl,
gold, and Artisan Moxies. Profession-relevant stock:

| Item | Cost |
|---|---|
| Recipe: Tokka's Multi-Ward (275012) | 1,500 Voidlight Marl · Venom Trawler+ |
| Recipe: Alluring Nostrum (271891) — Alchemy | 150 Artisan Alchemist's Moxie · Cursed Angler+ |
| Schematic: Proudmoore Ship-in-a-Bottle (275318) — Engineering decor | 150 Artisan Engineer's Moxie · Cursed Angler+ |
| Pattern: Mounted Moby (275336) — Leatherworking decor | 150 Artisan Leatherworker's Moxie · Cursed Angler+ |
| Design: Opalescent Amani Peridot (275693) — Jewelcrafting decor | 150 Artisan Jewelcrafter's Moxie · Cursed Angler+ |
| Recipe: Coiled Stargorger Lure (275018) | 1,500 Voidlight Marl · Cursed Angler+ |
| Recipe: Puffer Plate (278332) — Midnight Cooking | 1,500 Voidlight Marl |
| Recipe: Feast of Knowledge (275301) — Midnight Cooking | 1,500 Voidlight Marl · Venom Trawler+ |

Also new: an **Epic Fishing Rod** with interchangeable boons, and a Midnight
**Anglin' Score** (each fish worth up to 100 points; **2,500 score** →
*The Briny Best* achievement + the **"Briny"** title). Purely cosmetic.

### Skull of Er'inye — Vaults of Atal'Utek

Deals in **Corrosive Coins** (dropped by Amani spirits inside the Vaults).
Mostly mounts/pets/ensembles/decor, but it carries at least one crafting
recipe: **Recipe: Liquid Luster** (271888, Midnight Alchemy 50) for
**2,500 Corrosive Coins + 150 Artisan Alchemist's Moxie**.

### New reagents and embellishments (Tier 3)

Not in the Tier-1 notes — sourced from Method's 12.1 profession round-up, so
treat as corroborate-before-quoting:

- **Neutralized Venom Clot** — from *Venom Infused* Mining and Herbalism nodes.
- **Cursebound Globe** — from *cursebound* Mining and Herbalism nodes.
- New embellishments, one per crafting profession: **Hunter's Ritual Stone**
  (Blacksmithing) · **Coiled Snake-Eye** (Engineering) · **Polished Ammolite**
  (Jewelcrafting) · **Snakeskin Lining** (Tailoring) · **Adorned Fang**
  (Leatherworking). The **2-embellishment equipped cap is unchanged.**
- New Blacksmithing alloy **Odious Alloy** (Umbral Tin Ore + Luminant Flux +
  Refulgent Copper Ingot); Enchanting's **Enchant Weapon — Rite of the Hash'ey**
  is the enchant behind the R5 formula above.

## Profession knowledge reset (12.1)

12.1 ships a **one-time Knowledge Point reset, once per Midnight profession**:
every KP spent inside that profession's specialization trees is refunded and can
be re-assigned from scratch.

- ⚠ **Recipes you unlocked by spending those points are unlearned** by the
  reset. Re-spending gets them back; a half-finished respec does not.
- Base skill, **Artisan Moxie balances**, and knowledge already banked from
  treasures / Darkmoon Faire are **not** touched.
- **Once per profession, permanently** — spend it on a real mistake, not on a
  season-opening whim.

This is not in the official content-update notes (12.1 has **no PROFESSIONS
section**); it comes from a Blizzard quality-of-life announcement relayed by
Wowhead and corroborated by Method. @verify-ingame: confirm the reset button
exists in the specialization UI and that it is per-profession.

## Dye crafting (12.1)

**Dye crafting has been streamlined**, "considerably freeing up bag space taken
up by dyes" (Tier 1, housing notes). New dye colors were added, **including ones
that replicate the darker appearances from before the 12.0.5 content update**.
Housing detail lives in `housing.md`; the crafting-side consequence is that any
older guidance about stockpiling individual dye items is obsolete.

## Spark of Radiance crafting (Season 1 — historical)

> Season 1 ended with the week of 2026-08-11 maintenance. This section is kept
> because the **mechanics** carry forward; the **item names and ilvl numbers in
> it are Season 1** and no longer describe current crafts.

**Spark of Radiance** (item 232875) was the Season 1 crafting spark — the
gating reagent for max-level crafted epics.

### Acquisition (1/week, capped)

- Repeatable weekly quest from **Lady Liadrin** (expansion hub): choose one
  of four objectives — 6 World Quests, 3 Stormarion Assault Waves, 3 Prey
  Hunts, or 1 Battleground — for 1 spark.
- One-time-stackable early quests: **Midnight: World Tour**, **Unity
  Against the Void** (could yield 2 sparks in one week early in season).
- **Sparks of War** (War Mode): rotating-zone weekly (Voidstorm, Zul'Aman,
  Harandar) — collect 100 Sparks of War for an extra spark.
- **Catch-up**: if below the seasonal cap, most content randomly awards
  sparks.

### Costs & item levels (Season 1 values)

- **2 sparks** per armor piece / one-hand weapon; **4 sparks** for
  two-handed weapons. *(Ratio is expected to hold in S2 — unverified.)*
- Base spark epic: **ilvl 246–259** by craft quality (max quality = 259).
- Optional crest reagent raised the bracket: **80 Runed/Hero Dawncrests →
  259–272**; **80 Gilded/Myth Dawncrests → 272–285** (2H weapons need double:
  160 crests).
- Non-spark rare crafts: 220–233 base, up to 246 with Veteran crests.

⚠ **All five numbers above are Season 1.** S2 crests are **Mistcrests** and the
whole gear ladder shifted **+45** (269 → 334) — see the S2 section at the top of
this file. Do not scale these brackets by hand; the crafted bands are not
published and the S2 optional-reagent shape may have changed.

### Crafting orders

- Order via **Mar'nah \<Crafting Orders\>** in Silvermoon, **The Bazaar**
  district (same district as the AH; corroborated 2026-06-03 by Wowhead
  NPC db 243279 + user in-game). Customer supplies sparks + optional
  reagents; commission paid to crafter (historically ~500–20k gold).

### Optional reagent slots (the "special slots" in the crafting UI)

Below the required mats, spark recipes take optional reagents — these set
the item's power and customization; quality of the craft sets where in
the ilvl bracket it lands:

| Optional reagent | Effect |
|---|---|
| **80 Hero Dawncrests** (S1) | raises bracket to 259–272 |
| **80 Myth Dawncrests** (S1) | raises bracket to 272–285 (2H: 160) |
| **Missive** (Inscription-made) | choose the 2 secondary stats; tiered |
| **Embellishment reagent** | adds an embellishment effect (see below) |
| **Lucky Keychain** | recraft-only: strips an old embellishment (→ +1 Sparkle) |

In Season 2 the crest rows become **Mistcrests** — Tier-3/4 guides describe
Hero/Myth-range crafts as needing **Spark of Tides + the matching Mistcrest**,
but the counts are unconfirmed. The missive / embellishment / keychain rows are
system mechanics and are unchanged.

Missive quality: tier changes **recipe difficulty only** (+15 low /
**+5 high — verified in-game tooltip 2026-06-03**: "Guarantee
[stat] and [stat]" is identical across tiers), never the finished
item's stats. Two quality tiers observed on the AH (Midnight
simplified from TWW's three). Defense: place a **Personal Order with
minimum quality rank 5** — guaranteed result regardless of missive
tier; the crafter either hits it or can't fulfill. High-tier missives
are usually cheap enough to be the default buy.

### Order types & quality risk (verified in-game UI 2026-06-03)

- **Public**: no minimum-quality option; customer supplies ALL reagents
  (required + optional). 0g commission attracts skill-levelers who fill
  at low rank — quality ranks ≈ 246/250/253/256/259 in the base
  bracket, so a bad fill on a 4-spark weapon ≈ sidegrade. Commission
  doesn't repel levelers (their profit is the skillup) — it adds maxed
  order-snipers to the race; 300–1,000g + q3 reagents makes a rank-5
  fill *likely*, not guaranteed.
- **Guild / Personal**: can set **minimum quality** (rank 5) — the
  guaranteed path. Personal orders need a character name only — trade
  chat "r5 guaranteed" advertisers exist for this; no whisper needed
  (**shift-click their chat name into the recipient field** to handle
  special-character names). Vet a candidate via Blizzard API character
  professions endpoint (known recipes + skill — `wowkb.blizzard get
  /profile/wow/character/<realm>/<name>/professions`); quality stats
  aren't exposed, but maxed-skill + knows-recipe filters levelers.
- Rule of thumb: gamble tolerance ∝ 1/sparks — public OK for 2-spark
  armor, guild/personal only for 4-spark weapons.
- The S1 staff (Aln'hara Cane) is an **Inscription** recipe; the cloth
  pieces are Tailoring — may need two different crafters.

### Recrafting

- Crafted items can be **recrafted later** for fewer mats than a fresh
  craft: raise quality, add/swap optional reagents — this is how a 259
  crestless craft becomes 285 with Myth crests later.
- **Quality-only recrafts confirmed** (Icy Veins recrafting guide,
  fetched 2026-06-06): a recraft with no other changes raises quality
  if the recrafter's skill beats the original. Cost = **the item + "a
  small fraction of the original tradeable reagents"** + commission if
  ordered. Sparks are not tradeable reagents → **not re-consumed**
  (inference from the guide's wording + the plan's recraft-to-285
  assumption; sanity-check the recraft UI's reagent list once).
- ⚠ **Original reagent quality stays weighted into every future
  recraft** (Icy Veins) — cheap q1 mats in the original craft
  permanently drag the item's recraft math. **Always supply gold (q3)
  mats on the original order — especially public orders** (where the
  customer supplies everything anyway): then a bad fill is purely a
  skill problem, fully fixable by one recraft.
- Recraft orders go through the same order system (public/personal/
  guild) or self-recraft. Unverified: whether a recraft can come back
  *lower* quality — use min-quality (personal/guild) or self-recraft
  with concentration for the fix-up pass.
- **Replaced/removed optional reagents are destroyed, not refunded.**
  Spending 80 Hero crests on a piece you'll Myth-recraft wastes them —
  craft at 259 crestless, go straight to Myth on the recraft (wowcarry).

### Embellishments & strategy

- Embellishments are added **at crafting time** (or via recraft): either
  an embellishment optional reagent, or recipes that are inherently
  pre-embellished. Crafted gear is the **only** embellishment source in S1.
- **Hard limit of 2 embellished items equipped.** Check class Discords /
  Method's embellishment list for which are worth it.
- Recrafting can swap an embellishment (old reagent destroyed).
- **12.1 adds one new embellishment per crafting profession** (Hunter's Ritual
  Stone, Coiled Snake-Eye, Polished Ammolite, Snakeskin Lining, Adorned Fang —
  see the Coiled Isle section above). The **cap is still 2**, so S2 is a
  re-pick, not an expansion.
- Two common opening lines (Method) — **written with Season 1 ilvls**; the
  shape holds, the numbers do not:
  - **Early power**: max-bracket 2H weapon immediately (delays 2nd
    embellishment, weapon locked below the mythic-raid drop ceiling).
  - **Long-term**: max-bracket pieces in weak slots (bracers/belt/cloak),
    leave weapon open for mythic drops.
- After opening weeks, sparks are bad-luck protection: spend on slots that
  refuse to drop.
- **Crafted gear cannot be catalyzed** — never spark-craft tier slots
  (head/shoulders/chest/hands/legs). See `../endgame/catalyst.md`.

## Durability & repair economy (12.0.7 "Revelations")

As of patch **12.0.7** (live 2026-06-16), **weapons and armor no longer take
durability damage from combat events** (attacking, blocking, etc.). Blizzard's
stated rationale: combat durability loss hit specs asymmetrically, so the
removal flattens it — **all** players see less wear, but **shield users and
fast-weapon specs** (which racked up the most hits) see the largest drop.
Practical effect: **tanks and melee**, historically the heaviest repair bills
in a tier, get the biggest relief.

What this does **not** change:

- **Death still costs durability** — dying (releasing/wiping) remains the
  primary remaining durability sink. The patch notes only removed the
  per-hit combat wear, not the on-death penalty. So repairs aren't gone,
  just much cheaper for active play between deaths.
- No change to repair vendor mechanics, repair-mount access, or guild-bank
  repair funds; repair *cost per point* is unchanged — players simply lose
  far fewer points.

Profession-relevant takeaway: there is **no durability/repair crafting
profession** in Midnight (repairs are vendor/mount-based, not crafted), so
this is an indirect economy effect — lower routine gold drain on geared
characters, modestly more disposable gold for crafted-gear commissions and
reagents. It does not touch Blacksmithing/Engineering recipes.

## TODO

- [x] Mar'nah location corroborated 2026-06-03: The Bazaar, Silvermoon
      (Wowhead NPC db + in-game)
- [ ] Knowledge-point weekly sources (Icy Veins system guide + Signs of
      Kelani explainer) — **partially answered 2026-08-11**: the Coiled Isle
      adds **Jan'sari's knowledge tomes at Zul'jarra's Forces R6**; the
      recurring weekly KP sources (treasures, Kelani, profession weeklies) are
      still uncatalogued here. See `../planning/activities/profession-weekly.md`.
- [x] Midnight Tailoring leveling → dedicated file
      `tailoring-leveling.md` (2026-06-03)
- [x] Midnight Enchanting leveling → dedicated file
      `enchanting-leveling.md` (2026-08-29)
- [ ] **S2 crafted-gear ilvl brackets + Spark of Tides costs** — not published
      at Tier 1. Open a spark recipe after 2026-08-18 and read the optional
      reagents + quality ladder. (Also: Liadrin's S2 weekly spark options and
      the seasonal cap.)
- [ ] **Jan'sari knowledge-tome prices** — Tier-4 quote is 750 Voidlight Marl
      + 75/150 matching Artisan Moxie; confirm at the vendor at R6.
- [ ] **Profession knowledge reset** — confirm the reset control exists in the
      specialization UI and is genuinely once-per-profession.

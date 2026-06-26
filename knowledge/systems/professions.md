---
title: Professions & Spark Crafting (Midnight)
patch: 12.0.7
fetched: 2026-06-19
sources:
  - https://www.icy-veins.com/wow/spark-crafting-guide
  - https://www.method.gg/guides/how-to-gear-fast-and-reach-item-level-289-for-midnight-season-1
  - https://www.wowhead.com/news/sparks-of-radiance-for-crafting-now-available-in-midnight-easiest-spark-quest-380617
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://www.wowhead.com/news/save-gold-on-repairs-with-weapon-durability-changes-in-patch-12-0-7-381744
confidence: medium
---

# Professions (Midnight)

Crafting orders, spark crafting, knowledge points.

## Spark of Radiance crafting (Season 1)

**Spark of Radiance** (item 232875) is the Season 1 crafting spark — the
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

### Costs & item levels

- **2 sparks** per armor piece / one-hand weapon; **4 sparks** for
  two-handed weapons.
- Base spark epic: **ilvl 246–259** by craft quality (max quality = 259).
- Optional crest reagent raises the bracket: **80 Runed/Hero crests →
  259–272**; **80 Gilded/Myth crests → 272–285** (2H weapons need double:
  160 crests).
- Non-spark rare crafts: 220–233 base, up to 246 with Veteran crests.

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
| **80 Hero Dawncrests** | raises bracket to 259–272 |
| **80 Myth Dawncrests** | raises bracket to 272–285 (2H: 160) |
| **Missive** (Inscription-made) | choose the 2 secondary stats; tiered |

Missive quality: tier changes **recipe difficulty only** (+15 low /
**+5 high — verified in-game tooltip 2026-06-03**: "Guarantee
[stat] and [stat]" is identical across tiers), never the finished
item's stats. Two quality tiers observed on the AH (Midnight
simplified from TWW's three). Defense: place a **Personal Order with
minimum quality rank 5** — guaranteed result regardless of missive
tier; the crafter either hits it or can't fulfill. High-tier missives
are usually cheap enough to be the default buy.
| **Embellishment reagent** | adds an embellishment effect (see below) |
| **Lucky Keychain** | recraft-only: strips an old embellishment (→ +1 Sparkle) |

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
- Two common opening lines (Method):
  - **Early power**: 285 2H weapon immediately (delays 2nd embellishment,
    weapon locked at 285 vs 289 mythic-raid drops).
  - **Long-term**: 285 pieces in weak slots (bracers/belt/cloak), leave
    weapon open for mythic drops.
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
      Kelani explainer)
- [x] Midnight Tailoring leveling → dedicated file
      `tailoring-leveling.md` (2026-06-03)

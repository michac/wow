---
title: Affliction Warlock — gearing (stats, trinkets, tier set, consumables) (Midnight S2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes, Tier 1
  - https://maxroll.gg/wow/class-guides/affliction-warlock-raid-guide  # maxroll.gg, Tier 3, recaptured 2026-08-11 (S2 gear content)
  - https://maxroll.gg/wow/class-guides/affliction-warlock-mythic-plus-guide  # maxroll.gg, Tier 3, recaptured 2026-08-11 (S2 gear content)
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-gems-enchants-consumables  # tier 3 — Season 1 read, NOT re-fetched for 12.1
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-stat-priority  # tier 3 — Season 1 read, NOT re-fetched for 12.1
  - https://www.archon.gg/wow/builds/affliction/warlock/mythic-plus/trinkets/10/all-dungeons/this-week  # tier 2 — S1 usage data only; no S2 M+ data exists until 2026-08-18
  - https://www.method.gg/guides/midnight-missives-for-crafted-gear-profession-equipment  # tier 3, 2026-03-04
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1
confidence: medium
---

# Affliction — gearing (Midnight Season 2, 12.1)

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set percentages, stat weights) are largely **Tier-3 maxroll captures —
> sim-verify on Bloodmallet/Raidbots before trusting them**. Trinkets are the one
> slot where **effect > ilvl**.

## ⚠ 12.1 shipped into a pre-season week — what you can actually gear from

**12.1 went live 2026-08-11; Midnight Season 2 opens 2026-08-18.** Nearly every
item table below is a **Season 2** table, and most of it is **not obtainable
yet**:

| | Week of Aug 11 (now) | From Aug 18 |
|---|---|---|
| Venomous Abyss raid (Ula'tek, Sszorak, The Coiled Altar drops) | not open | Normal/Heroic/Mythic + LFR wings |
| Altar of Fangs / S2 dungeon pool | Heroic + **Mythic 0 on a weekly lockout**, Champion 1/6 (292) | Mythic+ opens, M0 back to daily |
| Tidebound Grotto (Lair) | **World difficulty only** → 279 (Veteran 1/6) | Normal/Heroic/Mythic → up to 318 |
| Delves | Tiers 1–11, no Bountiful → max **Adventurer 3/6** | Bountiful + Coffer Keys |
| Crafting | **Sparks drop now** — crafted pieces are the best pre-season slot filler | — |

So this week the realistic gearing plan is **crafted pieces (Martyr's Bindings /
Waistwrap, Adherent's Silken Shroud), M0 dungeon drops, the Tidebound Grotto
World lockout, and delves**. Treat the raid BiS rows as a target, not a plan.

## Stat priority

Sources differ slightly (Icy Veins: **Crit > Haste > Mastery**; others lean
Mastery/Crit). Secondaries are **flat** — ilvl > stats; avoid hard stacking.
Sim on Raidbots when it matters. **Unchanged in 12.1** — no Affliction stat-scaling
mechanic was touched.

- **Universal rule (both maxroll guides):** **avoid Versatility** — it is your
  worst stat; every other secondary is good.
- **Raid / single-target:** all non-Vers secondaries are close; treat the
  "priority" as a starting point that shifts with your gear (maxroll, sim-verify).
- **M+ / AoE:** **Mastery is very valuable on AoE and any cleave** — lean into
  it over the raid weighting when the content is multi-target (maxroll,
  sim-verify).
- **Tertiaries** (maxroll): **Leech** (all your damage is self-cast, so it
  heals you — great), **Avoidance** (reduces AoE intake), **Speed** (niche but
  proven, eases mechanics).
- All secondaries are subject to **diminishing returns** — another reason not
  to hard-stack a single stat.

> **12.1 global tuning that lands here (Tier 1):** player health **+25%** and
> creature damage **+25%** at max level, with health consumables rescaled to
> match. Our read (**inference, not sourced**): that raises the practical value
> of the survival tertiaries — **Avoidance** against the bigger incoming hits and
> **Leech**, which 12.1 also made strictly better for you by fixing **Unstable
> Affliction and Malefic Grasp to grant Soul Leech** (they previously did not).
> It does **not** move the secondary priority.

### Upgrade decision rules (ilvl vs stats)

- **Tier set pieces: take/upgrade regardless of secondaries** — 2pc/4pc are
  worth several ilvls each; bad stats never outweigh them.
- ⚠ **New in 12.1: the Catalyst now inherits the source item's secondary AND
  tertiary stats, plus certain special cantrip effects** (Tier 1). So converting
  is no longer a stat lottery — **pick a good-statted, Leech/Avoidance-carrying
  non-set item as your conversion source** and the set piece keeps it.
- **Most armor: higher ilvl wins** (int + stam scale with ilvl and dominate the
  budget; secondaries are flat for Affliction anyway).
- **Vers is lowest-throughput but not worthless** — flat damage + damage
  reduction; fine on a solo/delve-leaning character.
- **Be stat-picky only on**: rings (no primary stat — secondaries are the whole
  item), trinkets (effect > ilvl; sim), and near-ties (≤~6 ilvl gaps). Crafted
  pieces get exact stats via missive.

## Tier set — Midnight Season 2

Season 2 class-set armor is bought from **Kirana**, who **moved in 12.1** from
near the March on Quel'danas raid entrance to **beside the Catalyst in
Silvermoon**; her S2 stock costs **Slumbering Coil Curios** (Tier 1).

**Season 2 bonuses (Tier 3 — maxroll, both guides, captured 2026-08-11;
not yet corroborated against game data):**

- **2-Set:** [Corruption](https://www.wowhead.com/spell=172) damage increased by
  **25%**; [Agony](https://www.wowhead.com/spell=980) damage increased by **15%**.
- **4-Set:** each active [Unstable Affliction](https://www.wowhead.com/spell=30108)
  increases your spell/ability damage by **2%, up to 6%**, and
  [Seed of Corruption](https://www.wowhead.com/spell=27243) applies Unstable
  Affliction at **20% effectiveness**.

Set pieces come from Venomous Abyss (Aug 18+) or the Catalyst — see the BiS table.
Take/upgrade the four-piece over off-piece secondaries.

> **Season 1 set (historical, no longer the live tier):** 2pc = Unstable
> Affliction + Seed of Corruption **+10%**; 4pc = Agony starts at **2 extra
> stacks** and deals **+20%**. Recorded so a guide quoting it is recognizable as
> pre-12.1.

## Trinkets

> Trinkets are the one slot where **effect > ilvl** — sim rather than
> auto-equip the higher number. Choice is routinely **10%+ throughput**, far
> more than the ~6–7 ilvl between trinket ranks — it matters at any ilvl.
> **12.1 also lets the Cooldown Manager track trinket and potion cooldowns
> natively** (Tier 1), so lining an on-use trinket up with Darkglare no longer
> needs an addon.

### Where the tier lists live

- **Bloodmallet** — sims scaled by ilvl; the "does it beat mine at *my* ilvl"
  tool. **Tier 1.** (No S2 data on patch day — it needs sim profiles first.)
- **Archon / u.gg** — what top M+ players equip (usage %). **Tier 2.** ⚠ **No
  Season 2 usage data exists until keys go live 2026-08-18** — anything Archon
  shows this week is Season 1 history.
- **Icy Veins / Wowhead / maxroll** BiS pages — editorial + drop sources.
  **Tier 3.**

### Season 2 ranked list (maxroll raid + M+, identical, sim-verify)

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796) (Altar of Fangs), [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) (The Lost Explorers), [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649) (Kings' Rest), [Freightrunner's Flask](https://www.wowhead.com/item=250215) |
| **A-Tier** | [Wavecaller's Seastone](https://www.wowhead.com/item=270167), [Font of Venomous Rage](https://www.wowhead.com/item=270168), [Hex Lord's Dooming Idol](https://www.wowhead.com/item=270169) |
| **B-Tier** | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794), [Vexhul's Everflowing Gland](https://www.wowhead.com/item=270170), [Fang of Umbral Malignance](https://www.wowhead.com/item=270161) |
| **C-Tier** | [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Lightspire Core](https://www.wowhead.com/item=250214), [Mindpiercer's Sigil](https://www.wowhead.com/item=250224), [Sethraliss' Defiled Relic](https://www.wowhead.com/item=158368), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) |
| **Junkyard** | [Sealed Chaos Urn](https://www.wowhead.com/item=251787), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Void-Reaper's Libram](https://www.wowhead.com/item=251785), [Sylvan Wakrapuku](https://www.wowhead.com/item=251784) |

**Accessible this week:** the S-Tier pair from the S2 dungeon pool
(**Vile Vial of Volatile Venom** — Altar of Fangs; **Stormbound Emblem of
Dazar** — Kings' Rest) drops on Heroic/M0 already. Gebbo's Bottomless Bag is a
raid drop (Aug 18).

**Snapshot rule (unchanged):** on-use stat trinkets snapshot Darkglare — press
them **right before** Summon Darkglare, not after (maxroll). Darkglare re-reads
stats only slowly once it is already out.

> **Season 1 trinket read (historical):** Emberwing Feather + Gaze of the Alnseer
> was the dominant pair (81.5% / 47.7% Archon usage at +10), with Heart of Wind
> the open-world-farmable alternative and Vaelgor's Final Stare a maxroll S-Tier
> the usage data disagreed with. All of it is previous-season and none of those
> items appear on the S2 list.

### Delve / catch-up trinkets — ⚠ Season 1 data, stale

The Zah'ran vendor table this file carried (Astalor's Anguish Agitator,
Void-Reaper's Libram, Sylvan Wakrapuku, Tangle of Vibrant Vines, Glorious
Crusader's Keepsake — ~4000 Undercoin, ilvl 250) is a **Season 1 catch-up**
read. Season 2 delve gear starts at **ilvl 269** and the pre-season week caps
delve rewards at **Adventurer 3/6**, so ilvl-250 vendor trinkets are outclassed
by anything current; maxroll's S2 list already files Void-Reaper's Libram and
Sylvan Wakrapuku in **Junkyard**. The S2 delve/Undercoin vendor stock has not
been checked. @verify-ingame

⚠ No SimulationCraft binary in this toolkit. For exact deltas: in-game `/simc`
export → Raidbots **Top Gear**. Paste the export and the agent can read it.

## Best in Slot & farmable alternatives

From maxroll (raid + M+ BiS tables are identical, captured 2026-08-11). Farmable
list is open-world/dungeon gear obtainable outside the weekly lockout — immediate
power while you chase the BiS drops. **Most BiS rows are raid drops that are not
obtainable until 2026-08-18.**

### Best in Slot (maxroll, sim-verify)

| Slot | Item | Location |
|---|---|---|
| Head | [Venomkeeper's Horrific Cowl](https://www.wowhead.com/item=271874) | Ula'tek (raid) |
| Neck | [Aqirbane Reliquary](https://www.wowhead.com/item=268265) | Ula'tek (raid) |
| Shoulder | [Brood Cleanser's Amice](https://www.wowhead.com/item=239031) → convert to [Spires of the Damned Necrolyte](https://www.wowhead.com/item=271544) | Temple of Sethraliss / Catalyst |
| Cloak | [Silken Voodoo Drape](https://www.wowhead.com/item=268253) | The Coiled Altar (raid) |
| Chest | [Damned Necrolyte's Rattling Robes](https://www.wowhead.com/item=271549) | Tier / Catalyst |
| Wrist | [Martyr's Bindings](https://www.wowhead.com/item=239648) | Crafting |
| Gloves | [Grasps of the Eternal Shadow](https://www.wowhead.com/item=268243) → convert to [Damned Necrolyte's Charred Grasps](https://www.wowhead.com/item=271547) | The Coiled Altar / Catalyst |
| Belt | [Martyr's Waistwrap](https://www.wowhead.com/item=239649) | Crafting |
| Legs | [Damned Necrolyte's Leg Bindings](https://www.wowhead.com/item=271545) | Tier / Catalyst |
| Boots | [Cackling Soultreads](https://www.wowhead.com/item=268255) | The Coiled Altar (raid) |
| Ring 1 | [Apex Brute's Claw Ring](https://www.wowhead.com/item=268252) | Sszorak (raid) |
| Ring 2 | [Band of the Amani Warlord](https://www.wowhead.com/item=273792) | Altar of Fangs |
| Trinket 1 | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796) | Altar of Fangs |
| Trinket 2 | [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) | The Lost Explorers (raid) |
| Weapon | [Jan'thrazet, the Soul Fang](https://www.wowhead.com/item=271092) | Ula'tek (raid) |
| Off-hand | [Nocuous Focal Fang](https://www.wowhead.com/item=273779) | Altar of Fangs |

Note the two crafted BiS pieces (**Martyr's Bindings**, **Martyr's Waistwrap**)
— both craftable *now*, and Crafting Sparks already drop in the pre-season week.

### Farmable alternatives (maxroll, sim-verify)

| Slot | Item | Location |
|---|---|---|
| Head | [Worldroot Canopy](https://www.wowhead.com/item=251199) | The Blinding Vale |
| Neck | [Strand of Warding Fangs](https://www.wowhead.com/item=273781) | Altar of Fangs |
| Shoulder | [Spires of the Damned Necrolyte](https://www.wowhead.com/item=271544) | Tier / Catalyst |
| Cloak | [Adherent's Silken Shroud](https://www.wowhead.com/item=239656) | Crafting |
| Chest | [Damned Necrolyte's Rattling Robes](https://www.wowhead.com/item=271549) | Tier / Catalyst |
| Wrist | [Martyr's Bindings](https://www.wowhead.com/item=239648) | Crafting |
| Gloves | [Damned Necrolyte's Charred Grasps](https://www.wowhead.com/item=271547) | Tier / Catalyst |
| Belt | [Ethereal Netherwrap](https://www.wowhead.com/item=251222) | Voidscar Arena |
| Legs | [Damned Necrolyte's Leg Bindings](https://www.wowhead.com/item=271545) | Tier / Catalyst |
| Boots | [Sandswept Sandals](https://www.wowhead.com/item=159259) | Temple of Sethraliss |
| Ring 1 | [Signet of Snarling Servitude](https://www.wowhead.com/item=251136) | Murder Row |
| Ring 2 | [Band of the Amani Warlord](https://www.wowhead.com/item=273792) | Altar of Fangs |
| Trinket 1 | [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649) | Kings' Rest |
| Trinket 2 | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794) | Altar of Fangs |
| Weapon | [Nibbles' Training Rod](https://www.wowhead.com/item=251123) | Murder Row |

**Gear-track ilvl ranges (Season 2 — Tier 1, `CurrencyTypes` DB2 @ 12.1.0.69214):**
Adventurer **269–282** · Veteran **282–295** · Champion **295–308** · Hero
**308–321** · Myth **321–334**. Upgrade currency is now **Mistcrests** (Season 1's
Dawncrests are dead). *(Season 1, historical: Adventurer 224–237 · Veteran
237–250 · Champion 250–263 · Hero 263–276 · Myth 276–289 — the whole ladder
shifted +45.)*

## Embellishments & crafted gear

**maxroll embellishment options (sim-verify)** — listed as alternatives, pick one:

- **2× [Darkmoon Sigil: Hunt](https://www.wowhead.com/item=245876)** on main-hand
  + off-hand weapon (maxroll default). Craft on main hand for early power, off-hand
  for long-term BiS; when you loot/upgrade a Mythic weapon, keep the off-hand Sigil.
- **[Darkmoon Sigil: Hunt](https://www.wowhead.com/item=245876) (off-hand) +
  [Prismatic Focusing Iris](https://www.wowhead.com/item=251488) (ring)**.
- **M+ only:** [Prismatic Focusing Iris](https://www.wowhead.com/item=251488) (ring)
  + [Stabilizing Gemstone Bandolier](https://www.wowhead.com/item=251490)
  (**wrist or belt**) — the Bandolier doubles the Iris effect.
- **2× [Arcanoweave Lining](https://www.wowhead.com/item=240167)** — raid guide
  says Wrist + Cloak, M+ guide says Wrist + **Belt**.

Crafted staples: **Martyr's Bindings** (wrist) and **Martyr's Waistwrap** (belt)
are both S2 BiS, and **Adherent's Silken Shroud** (cloak) is the farmable cloak —
all three are the fastest pre-season power.

> The old Icy Veins/Method "Arcanoweave ×2 by default" read is a **Season 1**
> position that has not been re-fetched for 12.1; maxroll's current capture leans
> **Darkmoon Sigil: Hunt** on weapons. Sim to break the tie.

### Missives (Method 2026-03-04 — not re-verified for 12.1)

Midnight combat missives are **Thalassian Missives** (Inscription, AH-buyable;
dual-stat, equal split). Customer slots them in the **work order request window**
as an optional reagent — buy before placing the order. The six: Aurora
(Vers/Haste), Feverflare (Mastery/Haste), **Fireflash (Crit/Haste)**, Harmonious
(Vers/Mastery), **Peerless (Crit/Mastery)**, Quickblade (Vers/Crit).

**Affliction order: Thalassian Missive of the Peerless** (Crit/Mastery, default)
or **of the Fireflash** (Crit/Haste) — stats are flat, either is fine; never the
Vers trio.

## Enchants

maxroll's Season 2 table (raid + M+ identical, captured 2026-08-11):

| Slot | Enchant | Note |
|---|---|---|
| Helm | Empowered Blessing of Speed | + socket via Miasmic Jewelbinder |
| Cloak | Chant of Winged Grace | |
| Chest | Mark of the Worldsoul | |
| Wrist | — | socket via Miasmic Jewelbinder |
| Waist | — | socket via Miasmic Jewelbinder |
| Legs | Sunfire Silk Spellthread | |
| Feet | Farstrider's Hunt | |
| Rings | Eyes of the Eagle | both rings |
| Weapon | Acuity of the Ren'dorei | |
| Weapon oil | Thalassian Phoenix Oil | consumable, not an enchant slot |

**Sockets via enchant — new item for Season 2:** buy
**[Miasmic Jewelbinder](https://www.wowhead.com/item=275707)** from the Great
Vault Vendor to add sockets to **Helm, Wrists & Waist** (Season 1's equivalent
was Radiant Jewelbinder), then gem them.

All player-crafted → **all buyable on the AH**. Quality tiers exist; quality 1–2
is much cheaper for most of the effect (budget-friendly). *(Icy Veins' S1 table
also listed a shoulder enchant, Akil'zon's Swiftness; maxroll lists no shoulder
enchant and Icy Veins has not been re-fetched for 12.1.)*

## Gems

**maxroll (sim-verify, unchanged from S1):** unique
**[Powerful Eversong Diamond](https://www.wowhead.com/item=240967)** (use one of
each color to enhance it), then
[Flawless Quick Amethyst](https://www.wowhead.com/item=240900),
[Flawless Masterful Peridot](https://www.wowhead.com/item=240892),
[Flawless Quick Lapis](https://www.wowhead.com/item=240916),
[Flawless Quick Garnet](https://www.wowhead.com/item=240906) — **haste-leaning**
("Quick" = Haste).

> The Icy Veins **crit-leaning** alternative (Deadly Peridot / Lapis / Amethyst +
> Masterful Garnet, with Indecipherable Eversong Diamond until myth-track gear) is
> a **Season 1** read, not re-fetched for 12.1. Secondaries are close/flat for
> Affliction — sim, or just match your stat weighting.

## Consumables

maxroll Season 2 list (captured 2026-08-11):

- **Flask: Flask of the Shattered Sun** (maxroll default). Alternative:
  **Flask of the Blood Knights**. *(Season 1's Flask of the Magisters is the
  previous default — a guide still naming it is pre-12.1.)*
- **Combat potion: Light's Potential** (no drawback; maxroll's default).
- **Health potion: Concentrated Silvermoon Health Potion** — a big burst heal.
  ⚠ **12.1 rescaled every health consumable** to match the +25% max-level health
  pool, so any absolute "heals for N" number written before 2026-08-11 is wrong.
- **Food:** Harandar Celebration feast.
- **Weapon oil:** Thalassian Phoenix Oil.
- **Rune:** **Void-Touched Augment Rune**.

## 12.1 spec changes that touch gearing

Full detail lives in `builds.md` / `rotation.md`; only the gearing-relevant
consequences are here.

- **Haunt now +16% damage for 18s (was 12%)** — the burst window you line
  on-use trinkets and Darkglare into got stronger, which favours **on-use over
  passive** trinkets slightly more than in S1. Sim-verify.
- **New talents Hedonic Gorging** (Drain Life +10%; Siphon Life adds +10%
  Corruption damage; Dark Harvest channels 10% faster, +15% damage) and
  **Impetuous Wrath** (Shadow Bolt / Drain Soul / Malefic Grasp / Dark Harvest
  +10%, **+20% into a Haunted target**). Neither changes the stat priority.
- **Shard Instability redesigned** — Shadow Bolt or Drain Soul damage has a
  **20% chance** to make the next Unstable Affliction or Seed of Corruption
  **free and instant** (it absorbed the removed Nocturnal Yield's free-Seed
  feel). **Nocturnal Yield and Patient Zero are removed from the tree** — a gear
  or build guide still naming either is pre-12.1.
- **Unstable Affliction and Malefic Grasp now grant Soul Leech** (bug fix), and
  **Drain Life's health drain is +25%** — both raise the practical value of
  **Leech** as a tertiary and of Drain Life as a survival tool in delves/solo.
- **Summon Demonic Gateway is now a Utility spell by default in the Cooldown
  Manager**, and the CDM now tracks **trinkets, potions and racials**.

## TODO

- [ ] Sim-verify the S2 trinket order + the S2 tier-set values on
      Bloodmallet/Raidbots once profiles exist (currently Tier-3 maxroll only,
      captured on patch day). The tier-set bonuses in particular have **no
      Tier-1 corroboration** yet.
- [ ] Re-pull Archon/u.gg trinket + embellishment usage **after 2026-08-18**,
      when Mythic+ Season 2 actually generates data.
- [ ] Check the Season 2 delve/Undercoin catch-up vendor stock in game and
      replace the retired S1 table (@verify-ingame above).
- [ ] Re-fetch Icy Veins (stat priority, gems/enchants/consumables) once it is
      updated for 12.1 — the crit-vs-haste gem lean and the shoulder-enchant
      disagreement are both currently backed only by a Season 1 read.

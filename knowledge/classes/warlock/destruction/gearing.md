---
title: Destruction Warlock — gearing (stats, trinkets, tier set, consumables) (Midnight S1)
patch: 12.0.7
fetched: 2026-07-14
reviewed: 2026-07-14
sources:
  - https://maxroll.gg/wow/class-guides/destruction-warlock-raid-guide  # maxroll.gg, Tier 3
  - https://maxroll.gg/wow/class-guides/destruction-warlock-mythic-plus-guide  # maxroll.gg, Tier 3
confidence: medium
---

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set percentages, stat weights) are largely **Tier-3 maxroll captures —
> sim-verify on Bloodmallet/Raidbots before trusting them**. Trinkets are the one
> slot where **effect > ilvl**.

## Stat priority

The maxroll captures deliver the ordered stat priority only as an encoded
in-page widget (`Maxroll priority import`), **not as plain text**, so the exact
secondary-stat order (Crit / Haste / Mastery / Versatility) could not be
extracted verbatim. @verify-ingame — decode the maxroll priority widget or
sim on Raidbots to confirm the order for raid vs M+.

- Raw priority-import tokens (differ between raid and M+, so the two content
  types do NOT share the same order):
  - Raid: `IoAJFUAIkEDKBMgAEA`
  - Mythic+: `HoAJFUAJgEDKBEwABA`
- maxroll caveat (verbatim): a static stat priority is just a starting point and
  shifts with your current gear; **all secondary stats have diminishing
  returns** — sim your own character rather than trusting a fixed order.

### Tertiary stats (raid + M+, identical text in both captures)

- **Avoidance** — reduces AoE damage intake.
- **Leech** — extra healing from your damage; strong for Destro since almost all
  your damage is your own spells (pet damage does not leech).
- **Speed** — niche but repeatedly useful for handling mechanics.

## Tier set — Midnight Season 1

Identical in the raid and M+ captures (verbatim):

- **2-Set:** [Chaos Bolt](https://www.wowhead.com/spell=136835) and [Rain of Fire](https://www.wowhead.com/spell=91592) damage increased by 5%.
- **4-Set:** [Conflagrate](https://www.wowhead.com/spell=91591) generates 2 additional [Soul Shard Fragments](https://www.wowhead.com/spell=246985) and its damage is increased by 10%.

Full set list: [Midnight Season 1 Tier Sets](https://maxroll.gg/wow/resources/midnight-season-1-tier-sets).
BiS tier pieces (see table below): Head, Gloves, Legs from the tier set; Chest via
[Rotmire Catalyst](https://www.wowhead.com/item=250045).

## Trinkets

**Effect > ilvl for trinkets** — a lower-ilvl trinket with the right effect can
beat a higher-ilvl one, so do not just equip the highest number. maxroll's list
below is Tier-3; cross-check the actual DPS ordering on **Bloodmallet** /
Raidbots for your gear (maxroll, sim-verify). BiS pairing is
[Vaelgor's Final Stare](https://www.wowhead.com/item=249346) +
[Gaze of the Alnseer](https://www.wowhead.com/item=249343).

**Raid ranking** (maxroll, sim-verify):

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Gaze of the Alnseer](https://www.wowhead.com/item=249343), [Vaelgor's Final Stare](https://www.wowhead.com/item=249346) |
| **A-Tier** | [Locus-Walker's Ribbon](https://www.wowhead.com/item=249809), [Shadow of the Empyrean Requiem](https://www.wowhead.com/item=249810), [Emberwing Feather](https://www.wowhead.com/item=250144), [Heart of Wind](https://www.wowhead.com/item=250256) |
| **B-Tier** | [Soulcatcher's Charm](https://www.wowhead.com/item=250223), [Wraps of Cosmic Madness](https://www.wowhead.com/item=249340) |
| **C-Tier** | [Eye of the Drowning Void](https://www.wowhead.com/item=250257), [Reality Breacher](https://www.wowhead.com/item=151310) |
| **Junkyard** | [Vessel of Tortured Souls](https://www.wowhead.com/item=250258), [Nevermelting Ice Crystal](https://www.wowhead.com/item=50259), [Sealed Chaos Urn](https://www.wowhead.com/item=251787), [Void-Reaper's Libram](https://www.wowhead.com/item=251785), [Sylvan Wakrapuku](https://www.wowhead.com/item=251784), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Ever-Collapsing Void Fissure](https://www.wowhead.com/item=251786) |

**Mythic+ ranking** (maxroll, sim-verify) — orders differ slightly from raid
(note Locus-Walker's Ribbon drops to B, and Vessel of Tortured Souls is B not
Junkyard):

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Gaze of the Alnseer](https://www.wowhead.com/item=249343), [Vaelgor's Final Stare](https://www.wowhead.com/item=249346) |
| **A-Tier** | [Emberwing Feather](https://www.wowhead.com/item=250144), [Shadow of the Empyrean Requiem](https://www.wowhead.com/item=249810), [Heart of Wind](https://www.wowhead.com/item=250256) |
| **B-Tier** | [Locus-Walker's Ribbon](https://www.wowhead.com/item=249809), [Soulcatcher's Charm](https://www.wowhead.com/item=250223), [Vessel of Tortured Souls](https://www.wowhead.com/item=250258), [Wraps of Cosmic Madness](https://www.wowhead.com/item=249340) |
| **C-Tier** | [Eye of the Drowning Void](https://www.wowhead.com/item=250257), [Reality Breacher](https://www.wowhead.com/item=151310) |
| **Junkyard** | [Nevermelting Ice Crystal](https://www.wowhead.com/item=50259), [Sealed Chaos Urn](https://www.wowhead.com/item=251787), [Void-Reaper's Libram](https://www.wowhead.com/item=251785), [Sylvan Wakrapuku](https://www.wowhead.com/item=251784), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Ever-Collapsing Void Fissure](https://www.wowhead.com/item=251786) |

## Best in Slot & farmable alternatives

The raid and M+ captures give an **identical BiS table** (maxroll, sim-verify):

| Slot | Item | Location |
|---|---|---|
| Head | [Abyssal Immolator's Smoldering Flames](https://www.wowhead.com/item=250042) | Tier Set |
| Neck | [Rotmire's Sporeheart](https://www.wowhead.com/item=268291) | Rotmire |
| Shoulder | [Mantle of Dark Devotion](https://www.wowhead.com/item=251085) | Windrunner Spire |
| Cloak | [Adherent's Silken Shroud](https://www.wowhead.com/item=239656) | Crafting |
| Chest | [Abyssal Immolator's Dreadrobe](https://www.wowhead.com/item=250045) | Rotmire Catalyst |
| Wrist | [Martyr's Bindings](https://www.wowhead.com/item=239648) | Crafting |
| Gloves | [Abyssal Immolator's Grasps](https://www.wowhead.com/item=250043) | Tier Set |
| Belt | [Endless March Waistwrap](https://www.wowhead.com/item=249319) | Imperator Averzian |
| Legs | [Abyssal Immolator's Pillars](https://www.wowhead.com/item=250041) | Tier Set |
| Boots | [Luxurious Loamstriders](https://www.wowhead.com/item=268282) | Rotmire |
| Ring 1 | [Sporecaller's Blooming Loop](https://www.wowhead.com/item=268290) | Rotmire |
| Ring 2 | [Sin'dorei Band of Hope](https://www.wowhead.com/item=249919) | Belo'ren |
| Trinket 1 | [Vaelgor's Final Stare](https://www.wowhead.com/item=249346) | Vaelgor & Ezzorak |
| Trinket 2 | [Gaze of the Alnseer](https://www.wowhead.com/item=249343) | Chimaerus |
| Weapon | [Spire of the Furious Construct](https://www.wowhead.com/item=258047) | Skyreach |

**Farmable alternatives** — obtainable outside the weekly lockout, for immediate
character power while you chase BiS (identical in both captures):

| Slot | Item | Location |
|---|---|---|
| Head | [Shadow-Weaver's Crown](https://www.wowhead.com/item=151337) | Seat of the Triumvirate |
| Neck | [Barbed Ymirheim Choker](https://www.wowhead.com/item=50228) | Pit of Saron |
| Shoulder | [Lightbinder Shoulderguards](https://www.wowhead.com/item=258578) | Skyreach |
| Cloak | [Rigid Scale Greatcloak](https://www.wowhead.com/item=258575) | Skyreach |
| Chest | [Voidbender Robe](https://www.wowhead.com/item=151303) | Seat of the Triumvirate |
| Wrist | [Entropic Wristwraps](https://www.wowhead.com/item=151305) | Seat of the Triumvirate |
| Gloves | [Handwraps of the Ascended](https://www.wowhead.com/item=151300) | Seat of the Triumvirate |
| Belt | [Cord of Unraveling Reality](https://www.wowhead.com/item=151302) | Seat of the Triumvirate |
| Legs | [Legwraps of Swirling Light](https://www.wowhead.com/item=258574) | Skyreach |
| Boots | [Lightbinder Treads](https://www.wowhead.com/item=258584) | Skyreach |
| Ring 1 | [Occulsion of Void](https://www.wowhead.com/item=251217) | Nexus-Point Xenas |
| Ring 2 | [Omission of Light](https://www.wowhead.com/item=251093) | Nexus-Point Xenas |
| Trinket 1 | [Nevermelting Ice Crystal](https://www.wowhead.com/item=50259) | Pit of Saron |
| Trinket 2 | [Heart of Wind](https://www.wowhead.com/item=250256) | Windrunner Spire |
| Weapon | [Surgeon's Needle](https://www.wowhead.com/item=50227) | Pit of Saron |
| Offhand | [Vexamus' Expulsion Rod](https://www.wowhead.com/item=193709) | Algeth'ar Academy |
| Two-Hand | [Spire of the Furious Construct](https://www.wowhead.com/item=258047) | Skyreach |

## Embellishments & crafted gear

Two Spark slots. Options (maxroll, sim-verify):

- **1x** [Darkmoon Sigil: Hunt](https://www.wowhead.com/item=245875) — crafted
  only on your main-hand or off-hand weapon. Main hand = more power early; off
  hand = long-term BiS.
- **1x** [Arcanoweave Lining](https://www.wowhead.com/item=240167) — best crafted
  on **Wrists**, **Cloak**, **Boots** or **Waist** depending on your gear.

**or 2x** [Arcanoweave Lining](https://www.wowhead.com/item=240167) (same slot
guidance). The M+ capture additionally lists a pre-embellished 2x variant:
[Arcanoweave Bracers](https://www.wowhead.com/item=239660) /
[Arcanoweave Cloak](https://www.wowhead.com/item=239661) /
[Arcanoweave Treads](https://www.wowhead.com/item=239662) (craft on Cloak + Wrists).

**Remaining Sparks:** crafted items are 285 ilvl vs 289 for regular items on max
ilvl, so it is **not** worth equipping crafted gear beyond your 2x embellishments
unless you lack a higher-ilvl piece for that slot (maxroll).

## Enchants

maxroll enchant sheet (identical in both captures; maxroll, sim-verify). Note the
[Radiant Jewelbinder](https://www.wowhead.com/item=263897) is a socket-adder
bought from the Great Vault Vendor — use it to add sockets to **Helm**, **Wrists**
& **Waist** (it appears alongside the stat enchant on those slots).

| Slot | Enchant |
|---|---|
| Head | [Radiant Jewelbinder](https://www.wowhead.com/item=263897) (adds socket) + [Enchant Helm - Empowered Rune of Avoidance](https://www.wowhead.com/item=244007) |
| Shoulder | [Enchant Shoulders - Amirdrassil's Grace](https://www.wowhead.com/item=243991) |
| Chest | [Enchant Chest - Mark of the Worldsoul](https://www.wowhead.com/item=243977) |
| Wrist | [Enchant Bracer - Chant of Armored Avoidance](https://www.wowhead.com/item=223713) + [Radiant Jewelbinder](https://www.wowhead.com/item=263897) (adds socket) |
| Waist | [Radiant Jewelbinder](https://www.wowhead.com/item=263897) (adds socket) |
| Legs | [Sunfire Silk Spellthread](https://www.wowhead.com/item=240133) |
| Boots | [Enchant Boots - Farstrider's Hunt](https://www.wowhead.com/item=244009) |
| Ring 1 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Ring 2 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Weapon | [Enchant Weapon - Acuity of the Ren'dorei](https://www.wowhead.com/item=244029) |

## Gems

Sockets (maxroll, sim-verify):

- [Powerful Eversong Diamond](https://www.wowhead.com/item=240967) — **Unique** (one only).
- Then fill remaining sockets with:
  - [Flawless Deadly Peridot](https://www.wowhead.com/item=240890)
  - [Flawless Deadly Amethyst](https://www.wowhead.com/item=240898)
  - [Flawless Quick Garnet](https://www.wowhead.com/item=240906)
  - [Flawless Deadly Lapis](https://www.wowhead.com/item=240914)

The capture lists these gems as a set but does **not** specify how many of each /
which secondary to weight toward — @verify-ingame / sim to pick the right gem
colors for your stat balance.

## Consumables

Identical in both captures (maxroll, sim-verify):

- **Flask:** [Flask of the Shattered Sun](https://www.wowhead.com/item=241326) (max DPS)
  or [Flask of Thalassian Resistance](https://www.wowhead.com/item=241320) (less
  DPS, more survivability).
- **Combat Potion:** [Potion of Recklessness](https://www.wowhead.com/item=241288)
  (used after [Summon Infernal](https://www.wowhead.com/spell=1122) per the opener).
- **Health Potion:** [Silvermoon Health Potion](https://www.wowhead.com/item=241304) (big burst heal).
- **Food:** [Quel'dorei Medley](https://www.wowhead.com/item=242272) or
  [Silvermoon Parade](https://www.wowhead.com/item=255845).
- **Weapon Oil:** [Thalassian Phoenix Oil](https://www.wowhead.com/item=243734)
  (default) or [Smuggler's Enchanted Edge](https://www.wowhead.com/item=243738).
- **Augment Rune:** [Void-Touched Augment Rune](https://www.wowhead.com/item=259085).

## TODO

- [ ] sim-verify trinket order + tier-set values on Bloodmallet/Raidbots (currently Tier-3 maxroll)
- [ ] decode/confirm the secondary stat priority order (raid vs M+) — captures only ship it as an encoded widget, not text

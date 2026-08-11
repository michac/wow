---
title: Destruction Warlock — gearing (stats, trinkets, tier set, consumables) (Midnight S2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes (Tier 1)
  - https://maxroll.gg/wow/class-guides/destruction-warlock-raid-guide  # maxroll.gg, Tier 3 (recaptured 2026-08-11)
  - https://maxroll.gg/wow/class-guides/destruction-warlock-mythic-plus-guide  # maxroll.gg, Tier 3 (recaptured 2026-08-11)
confidence: medium
---

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set percentages, stat weights) are largely **Tier-3 maxroll captures —
> sim-verify on Bloodmallet/Raidbots before trusting them**. Trinkets are the one
> slot where **effect > ilvl**.

> ⚠ **12.1 rewrite (2026-08-11): this file is now Season 2 gear.** Every list
> below (BiS, farmable, trinkets, enchants, consumables, tier set) was replaced
> from the maxroll captures re-fetched on 12.1 patch day. The Season 1 lists it
> used to carry (Abyssal Immolator tier, Gaze of the Alnseer / Vaelgor's Final
> Stare, Radiant Jewelbinder, Silvermoon Health Potion) are **historical** — S1
> ended with the week of Aug 11 maintenance.
>
> ⚠ **And almost none of it is obtainable yet.** 12.1 went live **2026-08-11**
> but **Season 2 does not open until 2026-08-18**: no Venomous Abyss, no
> Mythic+ keys, no Bountiful Delves this week. This week you can gear from
> **Mythic 0** (weekly lockout this week only, drops Champion 1/6 = **292**),
> Delve tiers 1–11 (max Adventurer 3/6 + Veteran crests), Hard Prey and the
> Tidebound Grotto lair on World difficulty (both Veteran). Read the tables
> below as **the target you build toward from Aug 18**, not as this week's plan.

## What 12.1 changed for gearing

Tier-1 (content update notes) unless marked:

- **Season 2 ladder shifted +45**: S2 gear spans **ilvl 269 → 334** (S1 was
  224 → 289), upgraded with **Mistcrests** (Adventurer 269–282 · Veteran
  282–295 · Champion 295–308 · Hero 308–321 · Myth 321–334). Any "max ilvl 289"
  reasoning in older notes is dead.
- **Player health and creature damage +25% at max level, and health-consumable
  values were rescaled to match.** So any absolute "heals for N" number written
  before today is wrong — including for health potions and Soul Leech shields.
- **The Catalyst now inherits the secondary and tertiary stats — plus certain
  special cantrip effects — of the item you convert.** This is the big one:
  which item you feed the Catalyst now *matters*, so pick the conversion source
  for its stats, not just for the slot. (maxroll's S2 BiS table is written this
  way: it names the exact item to convert.)
- **Class-set vendor Kirana relocated** from the March on Quel'danas entrance to
  **beside the Catalyst in Silvermoon**, and now stocks **Midnight Season 2 class
  set armor for Slumbering Coil Curios**.
- **The Cooldown Manager now tracks trinkets, potions and racial cooldowns**
  (and they can be pinged) — you no longer need an addon to see trinket ICDs.
- **Crafting Sparks begin dropping during the pre-season**, so the two
  embellishment slots are buildable before the season opens.
- Spec-side, the one change that touches *stats* is
  **Conflagration of Chaos redesigned** — see the stat-priority note below.

## Stat priority

The maxroll captures still deliver the ordered stat priority only as an encoded
in-page widget (`Maxroll priority import`), **not as plain text**, so the exact
secondary-stat order (Crit / Haste / Mastery / Versatility) could not be
extracted verbatim. @verify-ingame — decode the maxroll priority widget or
sim on Raidbots to confirm the order for raid vs M+.

- Raw priority-import tokens (differ between raid and M+, so the two content
  types do NOT share the same order) — **unchanged between the S1 and the
  12.1 captures**, i.e. maxroll re-published the same priority for S2:
  - Raid: `IoAJFUAIkEDKBMgAEA`
  - Mythic+: `HoAJFUAJgEDKBEwABA`
- maxroll caveat (verbatim): a static stat priority is just a starting point and
  shifts with your current gear; **all secondary stats have diminishing
  returns** — sim your own character rather than trusting a fixed order.

### ⚠ 12.1: Crit's role changed, and the captures do not reflect it

**Conflagration of Chaos was redesigned** (Tier 1): *"Conflagrate and Shadowburn
have a 100% chance to critically strike, and their damage is increased by your
critical strike chance."* Two consequences the unchanged priority token cannot
be capturing:

- On those two spells crit rating no longer buys *chance to crit* — they always
  crit — it buys **flat damage**, so crit keeps scaling them but through a
  different (and un-diminished-looking) channel, on top of **Ruin**'s crit-damage
  multiplier which now applies to 100% of their casts.
- Everything else in the kit (Incinerate, Chaos Bolt, Immolate, Rain of Fire)
  still values crit the ordinary way, so the net weight depends on how much of
  your damage is Conflagrate + Shadowburn — which is exactly what a sim answers
  and a static priority does not.

**Do not re-order the stat priority off this paragraph** — treat it as the reason
to re-sim rather than as a new order. (Also in 12.1: all Destro damage **+4.5%**,
Soul Fire **+45%**, Chaos Bolt **+5%**, and **Havoc now copies 50%** of damage to
the marked target, was 60% — the last one lowers the value of anything that spikes
your two-target burst.)

### Tertiary stats (raid + M+, identical text in both captures)

- **Avoidance** — reduces AoE damage intake.
- **Leech** — extra healing from your damage; strong for Destro since almost all
  your damage is your own spells (pet damage does not leech).
- **Speed** — niche but repeatedly useful for handling mechanics.

**12.1 self-sustain note** (Tier 1, class-wide Warlock): **Drain Life +25%**, and
a Soul Leech correctness pass changed which casts feed the shield — **Infernal
Bolt, Avatar of Destruction's Chaos Bolt and Wicked Reaping now grant Soul
Leech**, while **Channel Demonfire no longer erroneously does**. Combined with the
+25% health pool, your effective self-healing profile moved even though the Leech
tertiary itself is unchanged.

## Tier set — Midnight Season 2

The Season 2 Warlock set is the **Damned Necrolyte** set (item names confirmed
Tier-1 via the Blizzard item API: *Damned Necrolyte's Rattling Robes* `271549`,
*Damned Necrolyte's Leg Bindings* `271545`, *Damned Necrolyte's Charred Grasps*
`271547`, *Spires of the Damned Necrolyte* `271544`). Bought from **Kirana, now
next to the Catalyst in Silvermoon, for Slumbering Coil Curios**, or converted at
the Catalyst.

Bonuses, identical in the raid and M+ captures (maxroll, Tier 3):

- **2-Set:** [Incinerate](https://www.wowhead.com/spell=29722) damage increased by 25%, and Incinerate has a 10% increased chance to evoke an **Echo of Sargeras**.
- **4-Set:** targets damaged by **Echo of Sargeras** take 6% increased damage from your spells and abilities for 6 seconds.

The 4-set is **Tier-1 corroborated**: the effect exists in game data as
**Dark Titan's Mark** `1305711` — *"Targets damaged by Echo of Sargeras take
$1305711s1% increased damage from your spells and abilities for $1305711d"* —
see `ability-inventory.md` (regenerated from 12.1 DB2). Echo of Sargeras itself
is the Apex talent **Embers of Nihilam** `1265770` proc (10% base chance off
Incinerate), so **this set is an Embers-of-Nihilam amplifier** — it is worth
markedly less on a build that does not take that Apex talent.

⚠ **maxroll's own spell links are junk and remain junk in the 12.1 capture** —
its renderer emitted `spell=91591` for Conflagrate, `spell=91592` for Rain of
Fire, `spell=136835` for Chaos Bolt and `spell=91582` for Shadowburn, none of
which are those spells. Every id in this file is hand-resolved against the
Blizzard API / DB2 instead: Incinerate `29722`, Conflagrate `17962`, Chaos Bolt
`116858`, Rain of Fire `5740`.

*(Season 1, historical: the Abyssal Immolator set gave Chaos Bolt + Rain of Fire
+5% (2p) and Conflagrate +2 Soul Shard Fragments and +10% damage (4p).)*

## Trinkets

**Effect > ilvl for trinkets** — a lower-ilvl trinket with the right effect can
beat a higher-ilvl one, so do not just equip the highest number. maxroll's list
below is Tier-3; cross-check the actual DPS ordering on **Bloodmallet** /
Raidbots for your gear (maxroll, sim-verify). ⚠ It is also a **patch-day** list
for a season that has not started: nobody has logged the raid yet, so treat the
tiering as a prior, not a result. BiS pairing is
[Freightrunner's Flask](https://www.wowhead.com/item=250215) +
[Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164).

**Raid ranking** (maxroll, sim-verify):

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164), [Freightrunner's Flask](https://www.wowhead.com/item=250215), [Wavecaller's Seastone](https://www.wowhead.com/item=270167) |
| **A-Tier** | [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649), [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796), [Font of Venomous Rage](https://www.wowhead.com/item=270168), [Hex Lord's Dooming Idol](https://www.wowhead.com/item=270169), [Fang of Umbral Malignance](https://www.wowhead.com/item=270161) |
| **B-Tier** | [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Mindpiercer's Sigil](https://www.wowhead.com/item=250224), [Vexhul's Everflowing Gland](https://www.wowhead.com/item=270170), [Knot of Writhing Serpents](https://www.wowhead.com/item=273794), [Lightspire Core](https://www.wowhead.com/item=250214) |
| **C-Tier** | [Drum of Renewed Bonds](https://www.wowhead.com/item=248583), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Effigy of Ula'tek's Faithful](https://www.wowhead.com/item=274493) |
| **Junkyard** | [Sethraliss' Defiled Relic](https://www.wowhead.com/item=158368), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) |

**Mythic+ ranking** (maxroll, sim-verify) — same pool, slightly different order
(note **Fang of Umbral Malignance** rises to S, and Stormbound Emblem /
Vile Vial swap within A):

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Freightrunner's Flask](https://www.wowhead.com/item=250215), [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164), [Fang of Umbral Malignance](https://www.wowhead.com/item=270161), [Wavecaller's Seastone](https://www.wowhead.com/item=270167) |
| **A-Tier** | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796), [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649), [Hex Lord's Dooming Idol](https://www.wowhead.com/item=270169), [Font of Venomous Rage](https://www.wowhead.com/item=270168) |
| **B-Tier** | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794), [Vexhul's Everflowing Gland](https://www.wowhead.com/item=270170), [Lightspire Core](https://www.wowhead.com/item=250214), [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Mindpiercer's Sigil](https://www.wowhead.com/item=250224) |
| **C-Tier** | [Drum of Renewed Bonds](https://www.wowhead.com/item=248583), [Effigy of Ula'tek's Faithful](https://www.wowhead.com/item=274493), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792) |
| **Junkyard** | [Sethraliss' Defiled Relic](https://www.wowhead.com/item=158368), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) |

12.1 also makes the **Cooldown Manager track trinkets and potions** natively, so
an on-use trinket's cooldown is visible without an addon.

## Best in Slot & farmable alternatives

The raid and M+ captures again give an **identical BiS table** (maxroll,
sim-verify). Sources are the Venomous Abyss raid (Ula'tek, Vashnik, Sszorak,
The Coiled Altar, Entombed Sentinels, The Lost Explorers) and the S2 M+ pool —
**none of which open before 2026-08-18**.

| Slot | Item | Location |
|---|---|---|
| Head | [Venomkeeper's Horrific Cowl](https://www.wowhead.com/item=271874) | Ula'tek |
| Neck | [Aqirbane Reliquary](https://www.wowhead.com/item=268265) | Ula'tek |
| Shoulder | Convert [Brood Cleanser's Amice](https://www.wowhead.com/item=239031) → [Spires of the Damned Necrolyte](https://www.wowhead.com/item=271544) | Catalyst (source: Temple of Sethraliss) |
| Cloak | [Silken Voodoo Drape](https://www.wowhead.com/item=268253) | The Coiled Altar |
| Chest | [Damned Necrolyte's Rattling Robes](https://www.wowhead.com/item=271549) | Vashnik |
| Wrist | [Martyr's Bindings](https://www.wowhead.com/item=239648) | Crafting |
| Gloves | Convert [Grasps of the Eternal Shadow](https://www.wowhead.com/item=268243) → [Damned Necrolyte's Charred Grasps](https://www.wowhead.com/item=271547) | Catalyst (source: The Coiled Altar) |
| Belt | [Martyr's Waistwrap](https://www.wowhead.com/item=239649) | Crafting |
| Legs | [Damned Necrolyte's Leg Bindings](https://www.wowhead.com/item=271545) | Sszorak |
| Boots | [Cackling Soultreads](https://www.wowhead.com/item=268255) | The Coiled Altar |
| Ring 1 | [Apex Brute's Claw Ring](https://www.wowhead.com/item=268252) | Sszorak |
| Ring 2 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Trinket 1 | [Freightrunner's Flask](https://www.wowhead.com/item=250215) | Murder Row |
| Trinket 2 | [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) | The Lost Explorers |
| Weapon | [Jan'thrazet, the Soul Fang](https://www.wowhead.com/item=271092) | Ula'tek |
| Offhand | [Spine of the Hissing Abyss](https://www.wowhead.com/item=268197) | Entombed Sentinels |

Note the two **Catalyst rows**: with 12.1's inheritance change, the named source
item is part of the recommendation — convert *that* piece, not whatever spare
token-slot item you have.

**Farmable alternatives** — obtainable outside the weekly lockout, for immediate
character power while you chase BiS (identical in both captures). Every source
here is an **S2 M+ pool** dungeon (Altar of Fangs, Murder Row, Den of Nalorakk,
The Blinding Vale, Voidscar Arena, Ruby Life Pools, Kings' Rest, Temple of
Sethraliss) — the S1 dungeons that used to fill this table (Seat of the
Triumvirate, Skyreach, Pit of Saron, Nexus-Point Xenas, Algeth'ar Academy,
Windrunner Spire) rotated out.

| Slot | Item | Location |
|---|---|---|
| Head | [Worldroot Canopy](https://www.wowhead.com/item=251199) | The Blinding Vale |
| Neck | [Graft of the Domanaar](https://www.wowhead.com/item=251234) | Voidscar Arena |
| Shoulder | [Brood Cleanser's Amice](https://www.wowhead.com/item=239031) | Temple of Sethraliss |
| Cloak | [Fireproof Drape](https://www.wowhead.com/item=193763) | Ruby Life Pools |
| Chest | [Robes of the Reborn Serpent](https://www.wowhead.com/item=239032) | Temple of Sethraliss |
| Wrist | [Winter's Embrace Bracers](https://www.wowhead.com/item=251154) | Den of Nalorakk |
| Gloves | [Handwraps of Blasphemous Rites](https://www.wowhead.com/item=273773) | Altar of Fangs |
| Belt | [Ethereal Netherwrap](https://www.wowhead.com/item=251222) | Voidscar Arena |
| Legs | [Wind Soarer's Breeches](https://www.wowhead.com/item=193750) | Ruby Life Pools |
| Boots | [Sandswept Sandals](https://www.wowhead.com/item=159259) | Temple of Sethraliss |
| Ring 1 | [Signet of Snarling Servitude](https://www.wowhead.com/item=251136) | Murder Row |
| Ring 2 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Trinket 1 | [Freightrunner's Flask](https://www.wowhead.com/item=250215) | Murder Row |
| Trinket 2 | [Lightspire Core](https://www.wowhead.com/item=250214) | The Blinding Vale |
| Weapon | [Crackling Jade Kilij](https://www.wowhead.com/item=160216) | Kings' Rest |
| Offhand | [Nocuous Focal Fang](https://www.wowhead.com/item=273779) | Altar of Fangs |
| Two-Hand | [Chillworn's Infusion Staff](https://www.wowhead.com/item=193761) | Ruby Life Pools |

⚠ This table is the *farmable* one and it still needs Mythic+ to farm — **keys do
not drop until Aug 18**. This week the same dungeons are runnable on Heroic and
**Mythic 0 (weekly lockout, Champion 1/6 = 292)** only.

## Embellishments & crafted gear

Two Spark slots; **Crafting Sparks start dropping during the pre-season**, so this
is buildable now. Options (maxroll, sim-verify):

- **1x** [Darkmoon Sigil: Hunt](https://www.wowhead.com/item=245875) — crafted
  only on your main-hand or off-hand weapon. Main hand / two-hand = more power
  early.
- **1x** [Arcanoweave Lining](https://www.wowhead.com/item=240167) — best crafted
  on **Wrists**, **Cloak**, **Boots** or **Waist** depending on your gear.

**or 2x** [Arcanoweave Lining](https://www.wowhead.com/item=240167) (same slot
guidance). *(The pre-embellished Arcanoweave Bracers/Cloak/Treads variant the S1
M+ capture listed is no longer in either 12.1 capture.)*

**Remaining Sparks:** crafted items cap at **331** vs **334** for regular items at
max ilvl (S1 numbers were 285 / 289), so it is **not** worth equipping crafted
gear beyond your 2x embellishments unless you lack a higher-ilvl piece for that
slot (maxroll).

## Enchants

maxroll enchant sheet (identical in both captures; maxroll, sim-verify). The
socket-adder for Season 2 is [Miasmic Jewelbinder](https://www.wowhead.com/item=275707)
(replacing S1's Radiant Jewelbinder), still bought from the **Great Vault Vendor**
and still used on **Helm**, **Wrists** & **Waist**.

| Slot | Enchant |
|---|---|
| Head | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (adds socket) + [Enchant Helm - Empowered Rune of Avoidance](https://www.wowhead.com/item=244007) |
| Shoulder | [Enchant Shoulders - Amirdrassil's Grace](https://www.wowhead.com/item=243991) |
| Chest | [Enchant Chest - Mark of the Worldsoul](https://www.wowhead.com/item=243977) |
| Wrist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (adds socket) |
| Waist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (adds socket) |
| Legs | [Sunfire Silk Spellthread](https://www.wowhead.com/item=240133) |
| Boots | [Enchant Boots - Farstrider's Hunt](https://www.wowhead.com/item=244009) |
| Ring 1 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Ring 2 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Weapon | [Enchant Weapon - Arcane Mastery](https://www.wowhead.com/item=244031) |

⚠ **Two changes vs the S1 sheet**: the weapon enchant is now
**Arcane Mastery** `244031` (was *Acuity of the Ren'dorei* `244029`), and the
Wrist row no longer pairs the socket-adder with *Chant of Armored Avoidance* —
the capture lists the Jewelbinder alone.

## Gems

Sockets (maxroll, sim-verify):

- [Powerful Eversong Diamond](https://www.wowhead.com/item=240967) — **Unique** (one only).
- Then fill remaining sockets with:
  - [Flawless Deadly Peridot](https://www.wowhead.com/item=240890)
  - [Flawless Deadly Amethyst](https://www.wowhead.com/item=240898)
  - [Flawless Quick Amethyst](https://www.wowhead.com/item=240900)
  - [Flawless Quick Garnet](https://www.wowhead.com/item=240906)
  - [Flawless Deadly Lapis](https://www.wowhead.com/item=240914)

The capture lists these gems as a set but does **not** specify how many of each /
which secondary to weight toward — @verify-ingame / sim to pick the right gem
colors for your stat balance. (Same gem list as S1 plus *Flawless Quick
Amethyst*; the Midnight gem tier itself did not change in 12.1.)

## Consumables

Identical in both captures (maxroll, sim-verify) — **three of the five lines
changed for Season 2**:

- **Flask:** [Flask of the Shattered Sun](https://www.wowhead.com/item=241326) (max DPS)
  or [Flask of Thalassian Resistance](https://www.wowhead.com/item=241320) (less
  DPS, more survivability). *(unchanged)*
- **Combat Potion:** [Light's Potential](https://www.wowhead.com/item=241309) —
  **new**, replaces S1's Potion of Recklessness. ⚠ The captures are internally
  inconsistent: their opener text still says to pop *Potion of Recklessness*
  after [Summon Infernal](https://www.wowhead.com/spell=1122) while the
  consumables list says *Light's Potential*. Sim before committing a stack.
- **Health Potion:** [Concentrated Silvermoon Health Potion](https://www.wowhead.com/item=271884)
  (big burst heal) — **new**, replaces Silvermoon Health Potion. Note the Tier-1
  global change: **health-consumable values were rescaled** alongside the +25%
  max-level health pool, so any older "heals for N" figure is void.
- **Food:** [Hearty Harandar Celebration](https://www.wowhead.com/item=266996),
  [Hearty Quel'dorei Medley](https://www.wowhead.com/item=242744) or
  [Hearty Silvermoon Parade](https://www.wowhead.com/item=266985) — the S2
  "Hearty" tier replaces the S1 Quel'dorei Medley / Silvermoon Parade.
- **Weapon Oil:** [Thalassian Phoenix Oil](https://www.wowhead.com/item=243734)
  (default) or [Smuggler's Enchanted Edge](https://www.wowhead.com/item=243738). *(unchanged)*
- **Augment Rune:** [Void-Touched Augment Rune](https://www.wowhead.com/item=259085). *(unchanged)*

Potions and healthstones are now trackable on (and pingable from) the **Cooldown
Manager** — 12.1, Tier 1.

## TODO

- [ ] sim-verify the S2 trinket order + tier-set value on Bloodmallet/Raidbots — the maxroll tiering is a **patch-day prior** for a season nobody has played
- [ ] decode/confirm the secondary stat priority order (raid vs M+) — captures still ship it only as an encoded widget, and the token is unchanged from S1 despite the Conflagration of Chaos redesign
- [ ] re-sim crit weight specifically after the Conflagration of Chaos redesign (always-crit + damage scaled by crit chance on Conflagrate/Shadowburn)
- [ ] confirm the S2 Damned Necrolyte 2-set text against game data — only the 4-set (Dark Titan's Mark `1305711`) is Tier-1 corroborated so far
- [ ] re-check the whole file after **2026-08-18** when Season 2 actually opens and real logs exist

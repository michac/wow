---
title: Demonology Warlock — gearing (stats, trinkets, tier set, consumables) (Midnight S2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-20
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes, Tier 1
  - https://worldofwarcraft.com/en-us/news/24294369  # Midnight Season 2 overview, Tier 1
  - https://maxroll.gg/wow/class-guides/demonology-warlock-raid-guide  # maxroll.gg, Tier 3, updated 2026-08-11
  - https://maxroll.gg/wow/class-guides/demonology-warlock-mythic-plus-guide  # maxroll.gg, Tier 3, updated 2026-08-11
  - https://murlok.io/warlock/demonology/diabolist/m+  # top-player secondary distribution, Tier 2 — Season 1 data
  - https://www.wowhead.com/item=273796  # item-name resolution (Wowhead item DB)
  - https://www.wowhead.com/item=271884  # item-name resolution (Wowhead item DB)
  - IN-GAME 2026-08-20 (Encomplete) — S1 "Reign of the Abyssal Immolator" set bonuses confirmed STILL ACTIVE in Season 2
  - simc @ a9c5673 (2026-08-20) engine/dbc/generated/item_set_bonus.inc:1104-1109 — S1 set modelled for specs 265/266/267; :1208-1211 — S2 Demo set "Abyssal Doomhound's Pursuit" (items 271535-271540)
confidence: medium
---

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set percentages, stat weights) are largely **Tier-3 maxroll captures —
> sim-verify on Bloodmallet/Raidbots before trusting them**. Trinkets are the one
> slot where **effect > ilvl**.

## ⚠ 12.1 shipped in two steps — read this before shopping

**12.1 went live 2026-08-11; Midnight Season 2 does not open until 2026-08-18.**
Everything below describes the **Season 2** gear picture. In the pre-season week
you can actually reach:

- the **new S2 dungeon pool on Heroic and Mythic 0** — M0 is on a **weekly**
  lockout this week only and drops **Champion 1/6 (292)**; keystones do not drop
  until Aug 18. That covers most of the **farmable alternatives** table.
- **Tidebound Grotto** (lair) on **World difficulty**, and **Crafting Sparks**,
  which begin dropping in pre-season.

You cannot yet reach: **The Venomous Abyss** (opens Aug 18) — so every raid-drop
row in the BiS table below is *upcoming*, not shoppable — nor Mythic+ keys,
Bountiful Delves, or Coffer Keys.

**The Season 2 ladder is ilvl 269 → 334** and its crests are **Mistcrests**
(Adventurer 269–282 · Veteran 282–295 · Champion 295–308 · Hero 308–321 · Myth
321–334). That is Tier-1 game data (`CurrencyTypes` DB2 @ 12.1.0.69214) and is
the **floor** — a +45 shift of the whole Season 1 ladder.

## ⚠ 12.1 retuned this spec — old sims are void

Tier-1 class notes for Demonology: **Shadow Bolt +45%**, **Demonbolt +55%**,
**Summon Gloomhound +35%**; and **Diabolist was nerfed** — Chaos Salvo,
Felseeker, Wicked Cleave and Eye Explosion all **−20%**, and **Flames of Xoroth
now increases Fire damage and demon damage by 3% (was 4%)**. Net: damage moved
*off* the Diabolist demon/Fire package and *onto* your own hard-cast Shadow
spells.

Class-wide (Tier 1): **Drain Life +25%**; a large **Soul Leech** correctness pass
now makes **Wild Imp / Imp Gang Boss Fel Firebolt, Imp Lord's Greater Felbolt,
Demonic Tyrant's Demonfire, Vilefiend's Headbutt and Bile Spit, and Gloomhound's
Gloom Slash** grant Soul Leech; and **Summon Demonic Gateway is now a Utility
spell by default in the Cooldown Manager**. Game-wide: **player health and
creature damage +25% at max level**, with health-consumable values rescaled to
match.

**Consequence for this file:** any stat weight, trinket ranking, or tier-set
valuation simmed before 2026-08-11 is describing a different spec. Re-sim.

---

The maxroll raid and M+ captures (both re-pulled 2026-08-11) ship **identical**
gear recommendations — same BiS/farmable tables, trinket ranking, embellishments,
enchants, gems and consumables — and both use the **same stat-priority import**,
so there is still no raid-vs-M+ gear split below.

## Stat priority

**Mastery ≈ Crit > Haste >> Versatility.** Both S2 captures ship the *same*
priority import (`HoAJFUAJgEDKBEgABA`) they shipped for Season 1 — maxroll did
not move the priority across the season boundary. Secondaries are fairly flat —
**ilvl and tier pieces win**; sim on Raidbots for close calls.

- maxroll's standing caution: "Higher item-level items are better in most
  scenarios… a static Stat Priority is just a starting point and can easily shift
  depending on your gear." All secondaries are subject to **diminishing returns**.
- ⚠ The murlok top-player distribution previously quoted here (Crit ~30% /
  Mastery ~34% / Haste ~22% / Vers ~1%) is **Season 1** data — nobody has played
  S2 yet. Treat it as a prior, not a reading, and refresh once S2 logs exist.

### Tertiary (maxroll)
- **Avoidance** — great for reducing AoE damage taken.
- **Leech** — still rated a **bad** tertiary here: your pets do most of your
  damage and pet damage does not leech. ⚠ Do not read 12.1's Soul Leech fix as
  rehabilitating this — **Soul Leech** (the absorb shield) and the **Leech**
  tertiary stat are different mechanics, and only the former changed. But the
  Shadow Bolt / Demonbolt buffs *do* raise the share of damage you deal yourself,
  so this ranking is worth re-checking once S2 sims land.
- **Speed** — niche but occasionally useful for mechanics.

## Tier set — Midnight Season 2

Verbatim from maxroll (sim-verify):

- **2-Set:** [Wild Imp](https://www.wowhead.com/spell=104317) damage increased by 10%. [Implosion](https://www.wowhead.com/spell=196277) damage increased by 20%.
- **4-Set:** When their energy depletes, [Wild Imps](https://www.wowhead.com/spell=104317) have a 20% chance to fling themselves at their target and [Implode](https://www.wowhead.com/spell=196277) at 250% effectiveness to their main target and 225% effectiveness to other targets.

See [Midnight Season 2 Tier Sets](https://maxroll.gg/wow/resources/midnight-season-2-tier-sets).
### ⚠ The Season 1 set bonuses are STILL ACTIVE in Season 2

**Season 1 set (Abyssal Immolator's):** 2pc = Hand of Gul'dan +15% · 4pc =
Dreadstalkers +10% and +3s duration.

**These bonuses continue to function in Season 2** — confirmed **in-game
2026-08-20** (Encomplete, 4pc equipped, bonuses reading as active on the
character sheet). They are no longer the set to *chase*, but they are **not
switched off**, and this changes gearing decisions materially:

> **Dropping below 4pc / 2pc of the S1 set costs you real throughput.** A
> higher-ilvl non-tier piece in a tier slot (head/shoulders/chest/hands/legs) is
> **not** automatically an upgrade — it is an ilvl gain weighed against a set
> bonus loss, and needs a sim to resolve. Do not treat old-tier slots as free
> upgrade targets.

Corroborating Tier-1 evidence: the 12.1 notes **retune** Midnight Season 1
2-set bonuses for other specs (Augmentation `_meta/patch-notes/12.1.md:611`,
Restoration Shaman `:1148`, Arms `:1254`) — Blizzard does not retune a bonus it
has deactivated. No line in the 12.1 notes disables S1 set bonuses.

*(Corrected 2026-08-20. This file previously said the S1 set was "historical as
of 12.1", which read as "inactive" and was wrong — it was an inference from the
arrival of the S2 set, not a sourced claim.)*

**Acquisition changed in 12.1 (Tier 1):**

- Class-set vendor **Kirana** has moved from the March on Quel'danas raid
  entrance to **near the Catalyst in Silvermoon**, and now stocks **Midnight
  Season 2 class set armor** for **Slumbering Coil Curios**.
- **The Catalyst now preserves your stats:** converted class-set armor
  **inherits the secondary and tertiary stats, plus certain special cantrip
  effects, of the source item**. Choosing *which* piece you feed the Catalyst is
  now a real decision — it never used to matter.

## Trinkets

Trinkets are the one slot where **effect > ilvl** — a lower-ilvl trinket with a
strong effect can beat a higher-ilvl one. maxroll ranking of Season 2 endgame
trinkets from Dungeons/Raids/Delves (maxroll, sim-verify — check
[Bloodmallet](https://bloodmallet.com/) for your ilvl/scenario):

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796), [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164), [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649), [Freightrunner's Flask](https://www.wowhead.com/item=250215) |
| **A-Tier** | [Wavecaller's Seastone](https://www.wowhead.com/item=270167), [Font of Venomous Rage](https://www.wowhead.com/item=270168), [Hex Lord's Dooming Idol](https://www.wowhead.com/item=270169) |
| **B-Tier** | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794), [Vexhul's Everflowing Gland](https://www.wowhead.com/item=270170), [Fang of Umbral Malignance](https://www.wowhead.com/item=270161) |
| **C-Tier** | [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Lightspire Core](https://www.wowhead.com/item=250214), [Mindpiercer's Sigil](https://www.wowhead.com/item=250224), [Sethraliss' Defiled Relic](https://www.wowhead.com/item=158368), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) |
| **Junkyard** | [Sealed Chaos Urn](https://www.wowhead.com/item=251787), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Void-Reaper's Libram](https://www.wowhead.com/item=251785), [Sylvan Wakrapuku](https://www.wowhead.com/item=251784) |

**"Low chance" in a trinket tooltip is a real proc rate, not flavour.** The five
base-ilvl-197 world/delve trinkets (items 251783/251784/251785/251787/251792,
spells 1253111–1253120 — one design batch) all proc off RPPM, and the wording
tracks `SpellProcsPerMinute.BaseProcRate` exactly:

| Trinket | Tooltip says | RPPM | ICD |
|---|---|---|---|
| [Lost Idol of the Hash'ey](https://www.wowhead.com/item=251783) | **"low chance"** | **1** | 5s |
| [Sylvan Wakrapuku](https://www.wowhead.com/item=251784) | "a chance" | 2 | — |
| [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792) | "a chance" | 2 | — |
| [Void-Reaper's Libram](https://www.wowhead.com/item=251785) | "a chance" | 3 | 5s |

So **Lost Idol is the weakest proc config in its own batch** — half to a third the
rate of its siblings *and* carrying a 5s internal cooldown — on top of granting a
**random** buff, which cannot be aimed at a Tyrant/Diabolist window. Read it as
Junkyard alongside the other four. *[Tier 1: wago DB2 `SpellAuraOptions` +
`SpellProcsPerMinute` @ 12.1.0; `ProcChance=101` is the use-RPPM sentinel.]*
⚠ Verified across this batch only — not tested as a game-wide tooltip convention.

⚠ **What the Lost Idol proc is WORTH is unmeasured, so the "half rate = half value"
reading is not established.** A lower rate paying a larger payload is a real design
pattern and has not been ruled out here. DB2 cannot settle it: 1253111 carries a proc
aura plus three dummy effects with **every base-points field 0**, and the Loa selection
is script-driven, so no magnitude exists in the tables; the buff resolves through a
**summon** (`Support of the Hash'ey` 1249259, `Effect=28`), not a stat aura. Wowhead's
item page is JS-rendered, so `wowkb.fetch` returns navigation only.
**To settle it:** note the buff name in the buff bar on a live proc, then look that spell
up — or sim the trinket on [Bloodmallet](https://bloodmallet.com/)/Raidbots at your ilvl.
@verify-ingame Lost Idol of the Hash'ey: capture the proc's buff name + magnitude, and
whether any Loa outcome is defensive/movement rather than throughput.

⚠ The ranking above is a day-one Tier-3 ranking for a season nobody has raided.
Expect it to move. Also note (Tier 1, 12.1): the **Cooldown Manager now tracks trinkets,
potions and racial cooldowns/durations**, and trinkets, health potions, combat
potions and healthstones can be **pinged** from it — so on-use trinket timers no
longer need an addon.

## Best in Slot & farmable alternatives

**BiS** (maxroll, sim-verify) — ⚠ raid rows are not obtainable until 2026-08-18:

| Slot | Item | Location |
|---|---|---|
| Head | [Venomkeeper's Horrific Cowl](https://www.wowhead.com/item=271874) | Ula'tek |
| Neck | [Aqirbane Reliquary](https://www.wowhead.com/item=268265) | Ula'tek |
| Shoulder | [Spires of the Damned Necrolyte](https://www.wowhead.com/item=271544) | Tier |
| Cloak | [Silken Voodoo Drape](https://www.wowhead.com/item=268253) | The Coiled Altar |
| Chest | [Damned Necrolyte's Rattling Robes](https://www.wowhead.com/item=271549) | Tier |
| Wrist | [Martyr's Bindings](https://www.wowhead.com/item=239648) | Crafting |
| Gloves | Convert [Grasps of the Eternal Shadow](https://www.wowhead.com/item=268243) → [Damned Necrolyte's Charred Grasps](https://www.wowhead.com/item=271547) | Catalyst (The Coiled Altar drop) |
| Belt | [Martyr's Waistwrap](https://www.wowhead.com/item=239649) | Crafting |
| Legs | [Damned Necrolyte's Leg Bindings](https://www.wowhead.com/item=271545) | Tier |
| Boots | [Cackling Soultreads](https://www.wowhead.com/item=268255) | The Coiled Altar |
| Ring 1 | [Apex Brute's Claw Ring](https://www.wowhead.com/item=268252) | Sszorak |
| Ring 2 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Trinket 1 | [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) | The Lost Explorers |
| Trinket 2 | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796) | Altar of Fangs |
| Weapon | [Jan'thrazet, the Soul Fang](https://www.wowhead.com/item=271092) | Ula'tek |
| Offhand | [Spine of the Hissing Abyss](https://www.wowhead.com/item=268197) | Entombed Sentinels |

**Farmable alternatives** (obtainable outside the weekly lockout — immediate
character power, replaced over time; maxroll). Unlike the Season 1 version of
this table, **these are reachable in the pre-season week**: every source is a
Season 2 dungeon, live now on Heroic and Mythic 0.

| Slot | Item | Location |
|---|---|---|
| Head | [Worldroot Canopy](https://www.wowhead.com/item=251199) | The Blinding Vale |
| Neck | [Strand of Warding Fangs](https://www.wowhead.com/item=273781) | Altar of Fangs |
| Shoulder | [Brood Cleanser's Amice](https://www.wowhead.com/item=239031) | Temple of Sethraliss |
| Cloak | [Speakeasy Shroud](https://www.wowhead.com/item=251132) | Murder Row |
| Chest | [Summoner's Searing Shirt](https://www.wowhead.com/item=251139) | Murder Row |
| Wrist | [Nibbling Armbands](https://www.wowhead.com/item=251127) | Murder Row |
| Gloves | [Handwraps of Oscillating Polarity](https://www.wowhead.com/item=159247) | Temple of Sethraliss |
| Belt | [Ethereal Netherwrap](https://www.wowhead.com/item=251222) | Voidscar Arena |
| Legs | [Forest Dream Leg-guards](https://www.wowhead.com/item=251160) | Den of Nalorakk |
| Boots | [Sandswept Sandals](https://www.wowhead.com/item=159259) | Temple of Sethraliss |
| Ring 1 | [Signet of Snarling Servitude](https://www.wowhead.com/item=251136) | Murder Row |
| Ring 2 | [Band of the Amani Warlord](https://www.wowhead.com/item=273792) | Altar of Fangs |
| Trinket 1 | [Stormbound Emblem of Dazar](https://www.wowhead.com/item=273649) | Kings' Rest |
| Trinket 2 | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794) | Altar of Fangs |
| Weapon | [Nibbles' Training Rod](https://www.wowhead.com/item=251123) | Murder Row |

## Embellishments & crafted gear

- **2x [Arcanoweave Lining](https://www.wowhead.com/item=240166)** — proc that
  increases your primary stat, plus a small ally buff. (maxroll — unchanged from S1.)
- **Remaining Sparks:** at Season 2 max ilvl, crafted items land at **331** while
  regular items land higher, so it is **not** worth equipping crafted pieces
  outside your 2x embellishments unless you lack a higher-ilvl item in that slot.
  (maxroll.) **Crafting Sparks begin dropping during the pre-season week**, so
  this is worth planning now.
  - ⚠ **Numbers conflict:** maxroll writes "regular items are 334–344 at max item
    level". Tier-1 game data caps the **Myth Mistcrest upgrade band at 334**, so
    anything above that is not crest-upgradeable — most likely Very Rare / Myth-9
    drops from the last two Venomous Abyss bosses, which sit outside the crest
    ladder. **334 is the Tier-1 floor; treat 344 as unverified maxroll editorial.**

## Enchants

maxroll (sim-verify):

| Slot | Enchant |
|---|---|
| Head | [Enchant Helm - Empowered Rune of Avoidance](https://www.wowhead.com/item=244007) + [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Shoulders | [Enchant Shoulders - Amirdrassil's Grace](https://www.wowhead.com/item=243991) |
| Chest | [Enchant Chest - Mark of the Worldsoul](https://www.wowhead.com/item=243977) |
| Wrist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Waist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Legs | [Sunfire Silk Spellthread](https://www.wowhead.com/item=240133) |
| Boots | [Enchant Boots - Lynx's Dexterity](https://www.wowhead.com/item=243953) |
| Ring 1 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Ring 2 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Weapon | [Enchant Weapon - Acuity of the Ren'dorei](https://www.wowhead.com/item=244029) |

> **Season 2 changed the socket-adder:** [Miasmic Jewelbinder](https://www.wowhead.com/item=275707)
> replaces Season 1's Radiant Jewelbinder. Bought from the Great Vault Vendor to
> add sockets to your **Helm**, **Wrists** & **Waist**. The enchants themselves
> are unchanged from Season 1.

## Gems

maxroll (sim-verify):

- [Flawless Quick Amethyst](https://www.wowhead.com/item=240900) — ⚠ **changed**;
  Season 1's pick was the Versatility gem (Flawless Versatile Garnet). A Haste
  gem sits oddly against a Mastery ≈ Crit > Haste priority, so this is a prime
  sim-verify candidate.
- [Indecipherable Eversong Diamond](https://www.wowhead.com/item=240983) — Unique. (Unchanged.)

## Consumables

maxroll (sim-verify) — three of the six moved for Season 2:

- **Flask:** [Flask of the Shattered Sun](https://www.wowhead.com/item=241326) — ⚠ **changed** (was Flask of the Magisters)
- **Food:** [Harandar Celebration](https://www.wowhead.com/item=255846)
- **Combat Potion:** [Potion of Recklessness](https://www.wowhead.com/item=241288)
- **Health Potion:** [Concentrated Silvermoon Health Potion](https://www.wowhead.com/item=271884) — ⚠ **changed** (was Silvermoon Health Potion); a big burst of healing
- **Weapon Oil:** [Thalassian Phoenix Oil](https://www.wowhead.com/item=243734)
- **Augment Rune:** [Void-Touched Augment Rune](https://www.wowhead.com/item=259085)

⚠ **Do not quote absolute healing numbers for any health consumable.** 12.1
raised **player health and creature damage by 25% at max level** and **rescaled
health-consumable values to match** (Tier 1), so every pre-2026-08-11 absolute HP
figure is wrong. Think in fractions of the new pool. Healthstones, health potions
and combat potions are also now trackable and pingable on the Cooldown Manager.

## TODO

- [ ] sim-verify the Season 2 trinket order, tier-set values, and the Haste-gem
      pick on Bloodmallet/Raidbots (currently day-one Tier-3 maxroll, on a spec
      12.1 retuned hard). **Cannot be resolved before S2 opens 2026-08-18** — the
      raid the BiS table draws from is not open.
- [ ] refresh the murlok top-player secondary distribution once Season 2 logs
      exist; the figures removed from "Stat priority" above were Season 1.

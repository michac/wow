---
title: Devourer Demon Hunter — gearing (stats, weapons, trinkets, tier set, consumables) (Midnight S2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes (Tier 1 — daggers, Mastery rescale)
  - https://maxroll.gg/wow/class-guides/devourer-demon-hunter-raid-guide  # maxroll.gg, Tier 3 — re-captured 2026-08-11, author-updated for 12.1
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-stat-priority  # Icy Veins, Tier 3 — updated 2026-08-10 for 12.1
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-gear-best-in-slot  # Icy Veins, Tier 3 — 12.1 weapon pool + craft order
  - https://maxroll.gg/wow/class-guides/devourer-demon-hunter-mythic-guide  # maxroll.gg, Tier 3 — ⚠ STALE, last author update 2026-06-22 (pre-12.1)
confidence: medium
---

# Devourer Demon Hunter — gearing (Midnight S2)

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set text, stat order) are largely **Tier-3 captures — sim-verify on
> Bloodmallet/Raidbots before trusting them**. Trinkets are the one slot where
> **effect > ilvl**.

> ⚠ **Two dates.** 12.1 went live **2026-08-11**; **Midnight Season 2 opens
> 2026-08-18**. The class changes below are live **now** — and so is a large part
> of the gear. **The pre-season week is a Season-2 gearing week, not a Season-1
> holding pattern.** Live right now:
>
> - the **Season 2 dungeon pool on Heroic + Mythic 0** — M0 drops **Champion 1/6
>   (ilvl 292)**, on a **weekly** lockout this week only (it returns to daily on
>   Aug 18);
> - the **Tidebound Grotto** lair on **World difficulty**, dropping **S2 Veteran
>   (ilvl 279, Veteran 1/6)**;
> - **Hard Prey** and **Pinnacle Caches**, both paying **S2 Veteran**;
> - **Delves** tiers 1–11 (no Bountiful), capped at **Adventurer 3/6**;
> - **Crafting Sparks**, which began dropping this week.
>
> What is genuinely gated to **Aug 18**: the **Venomous Abyss** raid (so every
> "Ula'tek"/"Coiled Altar" row in the BiS table below), **Mythic+ and keystones**,
> Bountiful Delves, and rated PvP. Season 2 *dungeon access* is not gated —
> only keys are.
>
> ⚠ **Everything Season-1 in this file was replaced.** The old ilvl ceiling (289),
> the Devouring Reaver's tier set, the S1 trinket ranking and the S1 dungeon
> farmables are gone — Season 2 runs **ilvl 269 → 334** (Mistcrests; Tier-1 DB2,
> `_meta/moving-values.md`) and the M+ pool rotated. Prior contents are recoverable
> from git history if you need the S1 record.

## What 12.1 changed for gearing

Tier 1 ([12.1 notes](https://worldofwarcraft.com/en-us/news/24293281)):

- **Demon Hunters can now equip daggers.** Blizzard's stated reason is Devourer
  specifically: *"This will allow Devourer Demon Hunters to acquire and use
  daggers with Intelligence on them."* See **Weapons** below — this is the single
  biggest slot-level change.
- **Mastery: Monster Within bonus damage during Void Metamorphosis reduced by
  66%**, compensated by **all ability damage +32%**. Blizzard's dev note:
  *"We're reducing the scaling of Devourer's Mastery: Monster Within to help
  other stats to compete."* **That is a gearing change, not just a tuning one** —
  it is why Haste now sits ahead of Mastery (below), and why any pre-12.1 stat
  weight or Pawn string is dead.
- Downstream damage moves that shift where secondary value lands: Collapsing Star
  +12%; Eradicate −6% (secondary target −15%); Consume +60% (not Devour); Void
  Metamorphosis now +40% Void Ray damage (was 67%); **Annihilator** Otherworldly
  Focus +30% single-target (was 35%), Final Hour persists 6s (was 8s).
- **Global:** player health and creature damage **+25% at max level**, with
  **health-consumable values rescaled to match** — the health potion below is a
  new item, not a rename. Several DPS healing/absorb effects were retuned to keep
  their relative impact.
- **Global:** the Catalyst now makes converted class-set armor **inherit the
  source item's secondary and tertiary stats plus certain cantrip effects**
  (`endgame/catalyst.md`) — so the piece you feed it now matters for stats, not
  just for the slot.

## Weapons — new in 12.1

Devourer is **Intellect**-based and shares weapons with casters. The equippable
pool is now **Warglaives, Fist Weapons, Axes, Daggers and Swords** (Icy Veins,
12.1). Two consequences:

- **Daggers are new and they are real BiS candidates.** maxroll's Season 2 raid
  BiS main-hand is **[Jan'thrazet, the Soul Fang](https://www.wowhead.com/item=271092)**
  — a one-hand **dagger** with Intellect (confirmed against the Wowhead item
  record, not editorial prose) — paired with
  **[Baleful Hexblade](https://www.wowhead.com/item=268211)**, a one-hand **sword**.
  The practical effect is that Devourer now competes for the ordinary Intellect
  one-hander drops the casters roll on, instead of waiting on a much thinner pool.
- **Warglaives remain special**: they **convert their primary stat to Intellect
  when you are playing Devourer** (Icy Veins). That makes a crafted warglaive the
  flexible choice if you also play Havoc/Vengeance — Icy Veins' crafting order is
  **Spellbreaker's Warglaive → [Silvermoon Agent's Deflectors](https://www.wowhead.com/item=244576)
  → [Silvermoon Agent's Sneakers](https://www.wowhead.com/item=244569)**.
  ⚠ Havoc's 12.1 weapon requirement (Warglaives/Axes/Swords/Fist) is a **Havoc**
  rule and does not constrain Devourer.
- **The warglaive is the first craft, not the endgame weapon.** Icy Veins: craft a
  weapon first because it "provides a lot of power out of the gate", but since
  Devourer now has access to **two higher-ilvl weapons this season** the crafted
  warglaive is **not** in the BiS setup — it's a gearing-journey piece, or the
  answer if you don't expect to kill the last two bosses on Mythic.
- ⚠ **Ula'tek is a double-edged roll.** Jan'thrazet is the strongest item on that
  boss's table, but the same boss drops **Font of Venomous Rage**, a poor trinket,
  and unlike Havoc you **cannot loot-spec away from it** (Jan'thrazet is not
  available to Vengeance). Icy Veins still rates bonus-rolling even Heroic Ula'tek
  worth it. *(From Aug 18.)*

## Stat priority

**Intellect > Haste > Mastery > Crit > Versatility** for **Annihilator**
(Icy Veins, updated 2026-08-10 for 12.1). Haste ramps Void Metamorphosis to
leverage Emptiness; Mastery sits close behind for the Cosmic damage multiplier.
⚠ **In AoE this flips** — Mastery becomes the dominant secondary (same source).
Crit rose sharply *because* of the Mastery nerf (via Calamitous) and lands on a
few pieces once Haste is high.

**Void-Scarred** wants **Intellect > Haste to 18% > Crit > Mastery > Versatility
> (further Haste)** — i.e. a Haste breakpoint then a pivot to Crit. The
breakpoint is **~800 Haste (17–20%)**, to smuggle Hunt and cycle Void
Metamorphosis faster; **above it Haste becomes your worst stat**, so cap it and
split the rest evenly between Crit and Mastery. Icy Veins' own FAQ notes Mastery
overtakes Crit once you hold **Aqirbane Reliquary** + **Freightrunner's Flask**,
which is why geared players look Mastery-heavy.

> **This reverses the pre-12.1 ordering.** The 12.0.7 KB carried Method's
> *"Mastery > Haste; prioritize Mastery into Haste"*. The 66% Mastery-scaling cut
> is exactly what killed that, and Blizzard said so in the dev note. **Do not
> restore the old order from a cached guide.** Method's Devourer pages were still
> stamped 12.0.7 at the time of this sweep.
>
> *Provenance:* both Icy Veins pages were captured to disk on 2026-08-11 —
> `raw/pages/www-icy-veins-com-wow-devourer-demon-hunter-pve-dps-stat-priority.md`
> (its own changelog reads "10 Aug. 2026: Updated for Patch 12.1") and
> `…-pve-dps-gear-best-in-slot.md` — so the flip is re-checkable without a refetch.
> It is still **Tier 3**: no Tier-1 stat weights exist, only the dev-note intent.

- **Higher item level wins in most slots** — a static priority is a starting
  point; sim your own gear on Raidbots for close calls (maxroll, sim-verify).
- All secondary stats are subject to **diminishing returns** (maxroll). Note the
  12.1 global change to **crowd-control** diminishing returns (20s reset, was 16s)
  is unrelated to stat DR — don't conflate them.
- ⚠ **The two Tier-3 guides disagree about AoE.** maxroll: Haste "sims pretty
  poorly on paper" but is a great stat for **multi-target** because it smooths the
  rotation a lot. Icy Veins: in AoE the priority **flips to Mastery**. Neither is
  Tier-1 and no 12.1 sim exists yet — treat single-target as the settled case
  (Haste first) and **sim your own AoE profile** rather than picking a side. The
  maxroll line also predates the Mastery cut.
- **Tertiaries** (maxroll): **Avoidance** (reduces AoE damage taken), **Leech**
  (self-healing), **Speed** (niche but useful for mechanics).

## Tier set — Midnight Season 2

**Abyssal Doomhound's** set (verbatim from maxroll). Tier pieces drop from the
**Venomous Abyss**, so the raid route opens **Aug 18**:

- **2-Set:** Harvesting 4 or more Soul Fragments with **Reap** has a 20% chance to
  make your next **Consume** instant-cast and explode in a **Soulburst**, dealing
  Cosmic damage to nearby enemies.
- **4-Set:** **Soulburst** generates 8 Soul Fragments and grants **Moment of
  Craving**. **Reap** deals 20% increased damage.

Tier pieces in the S2 BiS below: **Shoulder, Chest, Gloves, Legs**. See maxroll's
[Midnight Season 2 Tier Sets](https://maxroll.gg/wow/resources/midnight-season-2-tier-sets).
Class-set vendor **Kirana** has moved **next to the Catalyst in Silvermoon** and
stocks S2 sets for **Slumbering Coil Curios** — the non-raid route to the set.
⚠ Nothing in the 12.1 notes says whether Curios or S2 Catalyst charges accrue
during the pre-season week, so don't plan around either; see `endgame/catalyst.md`.
Note the Catalyst itself changed in 12.1: converted class-set armor now
**inherits the source item's secondaries/tertiaries and certain cantrips**, so
feed it a well-itemised piece.

## Trinkets

Trinkets are the slot where **effect can beat item level** — rank by effect, then
use **Bloodmallet** for ilvl-scaled sims. ⚠ On patch day no sim site has 12.1
Devourer data yet; this ranking is the guide author's, unsimmed.

maxroll's Season 2 endgame trinket ranking (Dungeons / Raids / Delves) (maxroll,
sim-verify):

| Tier | Trinkets |
|---|---|
| **S-Tier** | [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796), [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164), [Freightrunner's Flask](https://www.wowhead.com/item=250215) |
| **A-Tier** | [Wavecaller's Seastone](https://www.wowhead.com/item=270167), [Font of Venomous Rage](https://www.wowhead.com/item=270168), [Hex Lord's Dooming Idol](https://www.wowhead.com/item=270169) |
| **B-Tier** | [Knot of Writhing Serpents](https://www.wowhead.com/item=273794), [Vexhul's Everflowing Gland](https://www.wowhead.com/item=270170), [Fang of Umbral Malignance](https://www.wowhead.com/item=270161) |
| **C-Tier** | [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Lightspire Core](https://www.wowhead.com/item=250214), [Mindpiercer's Sigil](https://www.wowhead.com/item=250224), [Sethraliss' Defiled Relic](https://www.wowhead.com/item=158368), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) |
| **Junkyard** | [Sealed Chaos Urn](https://www.wowhead.com/item=251787), [Glorious Crusader's Keepsake](https://www.wowhead.com/item=251792), [Void-Reaper's Libram](https://www.wowhead.com/item=251785), [Sylvan Wakrapuku](https://www.wowhead.com/item=251784) |

**Freightrunner's Flask** (Murder Row) is the one S-Tier trinket that is a
**dungeon** drop and therefore the realistic pre-raid target.

## Best in Slot & farmable alternatives

**Best in Slot — Season 2** (maxroll raid guide, re-captured 2026-08-11)
(maxroll, sim-verify). ⚠ Raid drops are **not obtainable until 2026-08-18**;
Ula'tek is the **final** boss, so treat the top of this list as an end-of-tier
target, not a checklist:

| Slot | Item | Location |
|---|---|---|
| Head | [Gaze of the Coiled Watcher](https://www.wowhead.com/item=271875) | Ula'tek |
| Neck | [Aqirbane Reliquary](https://www.wowhead.com/item=268265) | Ula'tek |
| Shoulder | [Abyssal Doomhound's Jaws](https://www.wowhead.com/item=271535) | Tier |
| Cloak | [Silken Voodoo Drape](https://www.wowhead.com/item=268253) | The Coiled Altar |
| Chest | [Abyssal Doomhound's Coreguard](https://www.wowhead.com/item=271540) | Tier |
| Wrist | [Silvermoon Agent's Deflectors](https://www.wowhead.com/item=244576) | Crafting |
| Gloves | [Abyssal Doomhound's Studded Gauntlets](https://www.wowhead.com/item=271538) | Tier |
| Belt | [Sash of the Forlorn Vessel](https://www.wowhead.com/item=268256) | The Coiled Altar |
| Legs | [Abyssal Doomhound's Legwraps](https://www.wowhead.com/item=271536) | Tier |
| Boots | [Silvermoon Agent's Sneakers](https://www.wowhead.com/item=244569) | Crafting |
| Ring 1 | [Vile Alchemist's Band](https://www.wowhead.com/item=268249) | Vashnik |
| Ring 2 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Trinket 1 | [Freightrunner's Flask](https://www.wowhead.com/item=250215) | Murder Row |
| Trinket 2 | [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) | The Lost Explorers |
| Weapon | [Jan'thrazet, the Soul Fang](https://www.wowhead.com/item=271092) (1H **dagger**) & [Baleful Hexblade](https://www.wowhead.com/item=268211) (1H sword) | Ula'tek & The Coiled Altar |

**Farmable alternatives** (outside the weekly lockout — immediate character power)
(maxroll). Every source below is in the **Season 2 dungeon pool**, and that pool
is **already playable this week on Heroic and Mythic 0** — M0 at **Champion 1/6
(292)** but on a **weekly** lockout until Aug 18, when keys open and M0 returns to
daily. So these are obtainable now; they only become *farmable* on Aug 18:

| Slot | Item | Location |
|---|---|---|
| Head | [Vilefiend's Guise](https://www.wowhead.com/item=251140) | Murder Row |
| Neck | [Yoke of the Charging Bear](https://www.wowhead.com/item=251173) | Den of Nalorakk |
| Shoulder | [Somber Spaulders](https://www.wowhead.com/item=251223) | Voidscar Arena |
| Cloak | [Speakeasy Shroud](https://www.wowhead.com/item=251132) | Murder Row |
| Chest | [War Trial Vestments](https://www.wowhead.com/item=251159) | Den of Nalorakk |
| Wrist | [Fury-fletched Armlets](https://www.wowhead.com/item=251135) | Murder Row |
| Gloves | [Gauntlets of Fevered Defense](https://www.wowhead.com/item=251124) | Murder Row |
| Belt | [Whirling Dervish Sash](https://www.wowhead.com/item=159317) | Temple of Sethraliss |
| Legs | [Breeches of Deft Deals](https://www.wowhead.com/item=251130) | Murder Row |
| Boots | [Sand-Shined Snakeskin Sandals](https://www.wowhead.com/item=159327) | Temple of Sethraliss |
| Ring 1 | [Band of the Amani Warlord](https://www.wowhead.com/item=273792) | Altar of Fangs |
| Ring 2 | [Sickening Signet of Atroxus](https://www.wowhead.com/item=252258) | Voidscar Arena |
| Trinket 1 | [Freightrunner's Flask](https://www.wowhead.com/item=250215) | Murder Row |
| Trinket 2 | [Sapling of the Dawnroot](https://www.wowhead.com/item=250259) | The Blinding Vale |
| Weapon | 2x [Polished Lightwood Channeler](https://www.wowhead.com/item=273778) | Altar of Fangs |

*(maxroll's capture spells "Voidscar Arena" as "Voidcar Arena" in one row; the
dungeon name is **Voidscar Arena** per the S2 pool.)*

⚠ **The Mythic+ capture is stale.** `maxroll-mplus.md` was last updated by its
author **2026-06-22** — it predates 12.1 entirely and still lists Season 1 gear
from dungeons (Seat of the Triumvirate, Pit of Saron, Magisters' Terrace,
Nexus-Point Xenas, Algeth'ar Academy, Skyreach, Windrunner Spire, Maisara
Caverns) that **rotated out of the pool**. Use the raid capture's farmables above
for M+ until that guide updates; the two guides historically shared one gear list.

## Embellishments & crafted gear

- **1x [Loa Worshiper's Band](https://www.wowhead.com/item=251513)** — best overall
  choice of stat budget (maxroll).
- **[Arcanoweave Lining](https://www.wowhead.com/item=240166)** as the second
  embellishment (maxroll; replaces the S1 Stabilizing Gemstone Bandolier pick).
- **Remaining Sparks:** crafted items cap at **331 ilvl** vs regular items at
  **334** at max ilvl, so it's a small loss to equip crafted items outside your 2x
  embellishments unless you lack high-ilvl gear in that slot (maxroll). *(The
  334 ceiling is corroborated by Tier-1 game data — Myth Mistcrest tops out at
  334, `_meta/moving-values.md`.)*
- **Crafting Sparks began dropping in the pre-season week**, so crafted slots are
  bankable S2 power *now*. They are not the **only** such place, though — Mythic 0
  (Champion 1/6, 292), the Tidebound Grotto lair (Veteran 1/6, 279), Hard Prey and
  Pinnacle Caches all pay Season 2 tracks this week too. Crafting is simply the
  one that isn't on a lockout.

## Enchants

(maxroll raid capture, 12.1.) Buy **[Miasmic Jewelbinder](https://www.wowhead.com/item=275707)**
from the Great Vault Vendor to add sockets to **Helm, Wrists & Waist** — this is
the Season 2 replacement for S1's Radiant Jewelbinder.

| Slot | Enchant |
|---|---|
| Head | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) + [Empowered Rune of Avoidance](https://www.wowhead.com/item=244007) |
| Shoulder | [Amirdrassil's Grace](https://www.wowhead.com/item=243991) |
| Chest | [Mark of the Worldsoul](https://www.wowhead.com/item=243977) |
| Wrist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Waist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Legs | [Sunfire Silk Spellthread](https://www.wowhead.com/item=240133) |
| Boots | [Farstrider's Hunt](https://www.wowhead.com/item=244009) |
| Ring 1 | [Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Ring 2 | [Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Weapon | [Arcane Mastery](https://www.wowhead.com/item=244031) |

Changed from S1: the ring enchant moved from **Silvermoon's Alacrity** (Haste) to
**Eyes of the Eagle** (Crit), the wrist **Chant of Armored Avoidance** is no
longer listed alongside the socket, and only **Arcane Mastery** is named for the
weapon (S1 also carried Berserker's Rage on the off-hand). ⚠ These three are
capture-omissions as much as they are recommendations — verify at the enchanter
before assuming Berserker's Rage is a downgrade.

## Gems

(maxroll sockets list — unchanged from S1.)

- **[Powerful Eversong Diamond](https://www.wowhead.com/item=240967)** — Unique (one only).
- [Flawless Masterful Peridot](https://www.wowhead.com/item=240890) (Mastery)
- [Flawless Quick Amethyst](https://www.wowhead.com/item=240898) / [Quick Garnet](https://www.wowhead.com/item=240906) / [Quick Lapis](https://www.wowhead.com/item=240914) (Haste)

⚠ The gem list still leans Mastery even though the stat priority moved Haste
ahead of it in 12.1. Prefer the **Haste** gems until a 12.1 sim says otherwise.

## Consumables

(maxroll raid capture, 12.1.)

- **Flask/Phial:** [Flask of the Magisters](https://www.wowhead.com/item=241322) (max DPS) — **changed from S1's Flask of the Shattered Sun** — or [Flask of Thalassian Resistance](https://www.wowhead.com/item=241320) (less DPS, more survivability).
- **Food:** [Quel'dorei Medley](https://www.wowhead.com/item=242272) or [Silvermoon Parade](https://www.wowhead.com/item=255845).
- **Combat Potion:** [Potion of Recklessness](https://www.wowhead.com/item=241288).
- **Health Potion:** [Concentrated Silvermoon Health Potion](https://www.wowhead.com/item=271884) (big burst of healing) — **new in 12.1**; health consumables were rescaled for the +25% max-level health pool, so the S1 Silvermoon Health Potion no longer keeps up.
- **Weapon Oil:** [Thalassian Phoenix Oil](https://www.wowhead.com/item=243734) (default) or [Smuggler's Enchanted Edge](https://www.wowhead.com/item=243738).
- **Augment Rune:** [Void-Touched Augment Rune](https://www.wowhead.com/item=259085).

## TODO

- [ ] **sim-verify the 12.1 stat order and trinket ranking** on Bloodmallet /
      Raidbots once 12.1 Devourer sim data exists. Both are Tier-3 and were
      published within a day of the Mastery rescale; the Haste-over-Mastery flip
      is directionally backed by Blizzard's own dev note but the *magnitudes* are
      unverified.
- [ ] **Re-capture `maxroll-mplus.md`** (`wowkb.maxroll --kb`) once its author
      updates past 2026-06-22, then reconcile any M+ / raid gear divergence here.
- [ ] **Confirm the dagger BiS in practice from Aug 18** — whether an Intellect
      dagger genuinely beats a crafted Spellbreaker's Warglaive once the warglaive
      keeps spec-swap flexibility.
- [ ] **Resolve the three enchant deltas** left open above — the ring enchant
      (Silvermoon's Alacrity → Eyes of the Eagle), the missing wrist **Chant of
      Armored Avoidance**, and the missing off-hand **Berserker's Rage**. Each is
      equally explainable as a capture-omission or as a real 12.1 recommendation
      change; check the enchanter list in game / a second Tier-3 guide, and note
      that the ring move Haste→Crit is at least *consistent* with the new stat
      order for Void-Scarred but not for Annihilator.
- [ ] **Re-check the gem list against a 12.1 sim.** It is carried forward from S1
      unchanged and still leans Mastery, which the file's own stat priority now
      contradicts. No ledger row covers gems, so this is a genuine open question,
      not known drift.

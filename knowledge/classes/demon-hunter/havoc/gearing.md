---
title: Havoc Demon Hunter — gearing (stats, weapons, trinkets, tier set, consumables) (Midnight S2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes (Tier 1 — weapon requirement, Fury retune, daggers)
  - https://maxroll.gg/wow/class-guides/havoc-demon-hunter-raid-guide  # maxroll.gg, Tier 3 — re-captured 2026-08-11, gear sections are Season 2
  - https://maxroll.gg/wow/class-guides/havoc-demon-hunter-mythic-plus-guide  # maxroll.gg, Tier 3 — re-captured 2026-08-11, same gear list as raid
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-stat-priority  # Icy Veins, Tier 3 — updated 2026-08-10 for 12.1 (readable stat order)
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-gear-best-in-slot  # Icy Veins, Tier 3 — updated 2026-08-10 for 12.1 (weapon + trinket corroboration)
confidence: medium
---

# Havoc Demon Hunter — gearing (Midnight S2)

> **Split out of `builds.md` (2026-07-14).** Talents/loadouts/hero-tree live in
> `builds.md`; rotation in `rotation.md`. Exact gear NUMBERS here (trinket order,
> tier-set text, stat order) are largely **Tier-3 captures — sim-verify on
> Bloodmallet/Raidbots before trusting them**. Trinkets are the one slot where
> **effect > ilvl**.

> ⚠ **Two dates.** 12.1 went live **2026-08-11**; **Midnight Season 2 opens
> 2026-08-18**. The class changes below are live **now**. The Season 2 gear
> targets below (raid BiS, S2 tier set, S2 trinkets, the new M+ pool) are **not
> obtainable until Aug 18** — the Venomous Abyss raid and Mythic+ S2 both start
> that week. During the pre-season week you are still wearing Season 1 gear.
>
> ⚠ **Everything Season-1 in this file was replaced.** The old ilvl ceiling (289),
> the Devouring Reaver's tier set, the S1 trinket ranking, the S1 enchant/gem
> picks and the S1 dungeon farmables are gone — Season 2 runs **ilvl 269 → 334**
> (Mistcrests; Tier-1 DB2, `_meta/moving-values.md`) and the M+ pool rotated.
> Prior contents are recoverable from git history if you need the S1 record.

Raid and M+ maxroll captures still give **identical** gearing (same BiS, farmables,
trinket ranking, tier set, embellishments, enchants, gems, consumables) — re-checked
against both 2026-08-11 captures — so this page covers both; differences are called
out where they exist.

## What 12.1 changed for gearing

Tier 1 ([12.1 notes](https://worldofwarcraft.com/en-us/news/24293281)):

- ⚠ **Havoc now has a weapon-type requirement.** *"Demon Blades, Blade Dance, and
  Chaos Strike now require equipped Warglaives, Axes, Swords, and Fist Weapons."*
  Three of Havoc's core buttons — its Fury generator, its AoE and its Chaos Strike
  spender — simply do not work off an illegal weapon. **This is a hard gearing
  constraint, not a preference.**
- **Demon Hunters can now equip daggers**, and Blizzard's stated reason is
  Devourer (*"…acquire and use daggers with Intelligence on them"*). **For Havoc a
  dagger is a trap**: it is equippable, it will show up in your loot, and equipping
  it turns off the abilities above. Never take a dagger as a Havoc upgrade on
  item level alone.
  - The Season 2 BiS main-hand **[Aman'muso, Warlord's Vengeance](https://www.wowhead.com/item=268209)
    is a one-hand axe** (verified against the Wowhead item record, not editorial
    prose) and the off-hand is a warglaive — both legal.
- **Fury retune**, with Blizzard's dev note: *"a small overall increase, paced more
  smoothly and relying less heavily on Immolation Aura's talent effects."*
  Burning Hatred now gives Immolation Aura **+30 Fury** (was 40); Demon Blades
  **10–16 per attack** (was 8–15); Blind Fury **10/20 Fury per second** (was
  15/30). **Immolation Aura damage −8%.** See the Haste caveat under
  [Stat priority](#stat-priority) — the old "Haste is good because it makes
  Immolation Aura your Fury engine" argument is deliberately weaker now, while the
  Demon Blades buff moves Fury generation onto **auto-attacks**, which Haste still
  scales.
- **Damage moves that compound with the S2 tier set:** Blade Dance / Death Sweep /
  Chaos Strike / Annihilation all **+6%**; Essence Break initial **+49%**;
  The Hunt **+12%**. The S2 2-set buffs *Blade Dance, Chaos Strike and Essence
  Break* — the same three the tuning pass raised.
- **New talent [Never Say Die](https://www.wowhead.com/spell=427794)** — +3% damage
  above 50% health, **+5% Leech below 50%**. It is a talent, not gear, but it is
  the one 12.1 change that touches the **Leech** tertiary discussion below.
- **Removed: Dash of Chaos.** **Inner Demon** moved to a choice node with Chaos
  Theory. Trail of Ruin now applies its damage **immediately** (was a 4s DoT);
  Serrated Glaive is now a **12s buff on you** (was a 15s debuff on the target).
  These are `builds.md` / `rotation.md` facts — listed here only so a stale gear
  guide recommending Dash of Chaos is recognisably stale.
- **Global:** player health and creature damage **+25% at max level**, with
  **health-consumable values rescaled to match** — the health potion below is a
  **new item**, not a rename. Several DPS healing/absorb effects were retuned.
- **Global:** the Catalyst now makes converted class-set armor **inherit the source
  item's secondary and tertiary stats plus certain cantrip effects**
  (`endgame/catalyst.md`) — so *which* piece you feed it now matters for stats,
  not just for the slot. maxroll's S2 BiS leans on this (three of the four tier
  slots below are Catalyst conversions).

## Stat priority

**Agility > Critical Strike > Mastery > Haste > Versatility** (Icy Veins, updated
**2026-08-10 for 12.1**). Icy Veins is explicit that **Havoc has no significant
variance between Hero Talents or target counts** — one order covers Aldrachi
Reaver and Fel-Scarred, single-target and AoE.

> **This resolves the old S1 gap.** The 12.0.7 KB carried no readable order at all
> because maxroll ships the priority only as an opaque embed
> (`IoAJFMAIxQCKBEQABA` — *unchanged* between the S1 and the 2026-08-11 S2
> captures, which is itself a reason not to trust it as a 12.1 re-derivation).
> The order above is **Tier 3 and unsimmed on 12.1** — see the TODO.
>
> ⚠ **Conflicting Tier-3 read:** Wowhead's Havoc stat page gives
> **Crit ≈ Mastery > Vers > Haste** and claims Fel-Scarred leans Mastery while
> Aldrachi Reaver leans Crit. That page is stamped "Patch 12.1.0" but its content
> is dated **2026/02/25** — months before this patch — so it does not corroborate
> anything about 12.1. Both sources agree Crit and Mastery lead; **Haste vs
> Versatility for the third slot is genuinely unsettled** until someone sims it.

- **Higher item level wins in most slots** — a static priority is a starting point;
  sim your own gear on Raidbots for close calls (maxroll, sim-verify).
- All secondary stats are subject to **diminishing returns** (maxroll). Note the
  12.1 global change to **crowd-control** diminishing returns (20s reset, was 16s)
  is unrelated to stat DR — don't conflate them.
- **Haste caveat (maxroll):** Haste "sims pretty poorly on paper" but is a great
  stat for **multi-target** because it smooths gameplay a lot — it adds
  [Immolation Aura](https://www.wowhead.com/spell=258920) charges (shorter
  recharge), aids Fury generation, and fits more abilities into
  [Demonic](https://www.wowhead.com/spell=213410) windows. ⚠ **This text predates
  the 12.1 Fury retune** and was written when Immolation Aura was the Fury engine;
  Burning Hatred was cut 40 → 30 and Immolation Aura's damage by 8% precisely to
  reduce that dependence. Treat the Immolation-Aura half of the argument as
  weakened and the auto-attack half (Demon Blades 10–16) as strengthened.

### Tertiary stats
- **Avoidance** — great for reducing AoE damage intake.
- **Leech** — extra self-healing through damage dealt. **Worth more in 12.1 if you
  talent Never Say Die** (+5% Leech below 50% health) and generally worth more now
  that creature damage is up 25% at max level.
- **Speed** — niche but proven useful; eases certain mechanics.

## Tier set — Midnight Season 2

**Abyssal Doomhound's** set (verbatim from maxroll; available from **Aug 18**, or
earlier via the Catalyst once S2 charges accrue). See
[Midnight Season 2 Tier Sets](https://maxroll.gg/wow/resources/midnight-season-2-tier-sets).

- **2-Set:** [Blade Dance](https://www.wowhead.com/spell=188499),
  [Chaos Strike](https://www.wowhead.com/spell=162794) and
  [Essence Break](https://www.wowhead.com/spell=258860) deal **12% increased damage**.
- **4-Set:** **Essence Break** now applies and benefits from the effects of
  [Cycle of Hatred](https://www.wowhead.com/spell=258887), has **25% increased
  initial strike damage**, and has **2 seconds of increased duration**.

Tier slots in the S2 BiS below: **Shoulder, Chest, Gloves, Legs**. Class-set vendor
**Kirana** has moved **next to the Catalyst in Silvermoon** and stocks S2 sets for
**Slumbering Coil Curios**. Note how the 4-set stacks with the +49% Essence Break
initial-damage buff — Essence Break is where both the tier and the tuning landed.

## Trinkets

Trinkets are the slot where **effect can beat item level** — rank by effect, then
use **Bloodmallet** for ilvl-scaled sims. ⚠ On patch day no sim site has 12.1 Havoc
data; this ranking is the guide author's, unsimmed. Identical in both captures.

| Rank | Trinkets |
|---|---|
| **S-Tier** | [Voracious Heart of Ula'tek](https://www.wowhead.com/item=270175), [Zul'jin's Guillotine Technique](https://www.wowhead.com/item=270173), [Font of Venomous Rage](https://www.wowhead.com/item=270168), [Gebbo's Bottomless Bag](https://www.wowhead.com/item=270164) |
| **A-Tier** | [Freightrunner's Flask](https://www.wowhead.com/item=250215), [Vashnik's Sanguine Rancor](https://www.wowhead.com/item=270166), [Keeper's Seething Core](https://www.wowhead.com/item=270165) |
| **B-Tier** | [Lustrous Golden Plumage](https://www.wowhead.com/item=159617), [Sapling of the Dawnroot](https://www.wowhead.com/item=250259), [Resonant Bellowstone](https://www.wowhead.com/item=250228), [Void Execution Mandate](https://www.wowhead.com/item=250225), [Ruby Whelp Shell](https://www.wowhead.com/item=193757) (Trained) |
| **C-Tier** | [Lightspire Core](https://www.wowhead.com/item=250214), [Vile Vial of Volatile Venom](https://www.wowhead.com/item=273796), [Tiny Electromental in a Jar](https://www.wowhead.com/item=158374), [Tattered Amani War Banner](https://www.wowhead.com/item=273797) |
| **Junkyard** | [Ruby Whelp Shell](https://www.wowhead.com/item=193757) (Untrained) |

**[Freightrunner's Flask](https://www.wowhead.com/item=250215)** (Murder Row) is the
highest-ranked trinket that is a **dungeon** drop, and therefore the realistic
pre-raid target. Icy Veins (12.1) independently pairs the on-use
**Voracious Heart of Ula'tek** with the passive **Zul'jin's Guillotine Technique**
(or Gebbo's Bottomless Bag), which corroborates the top of this table.

## Best in Slot & farmable alternatives

**Best in Slot — Season 2** (maxroll raid + M+ captures, re-captured 2026-08-11;
weapons and trinkets corroborated by Icy Veins 12.1) (maxroll, sim-verify).
⚠ Raid drops are **not obtainable until 2026-08-18**; Ula'tek is the **final**
boss, so treat the top of this list as an end-of-tier target, not a checklist:

| Slot | Item | Location |
|---|---|---|
| Head | [Gaze of the Coiled Watcher](https://www.wowhead.com/item=271875) | Ula'tek |
| Neck | [Aqirbane Reliquary](https://www.wowhead.com/item=268265) | Ula'tek |
| Shoulder | [Abyssal Doomhound's Jaws](https://www.wowhead.com/item=271535) | Catalyst — convert [Frothing Venom Spaulders](https://www.wowhead.com/item=268246) (Vashnik) |
| Cloak | [Silken Voodoo Drape](https://www.wowhead.com/item=268253) | The Coiled Altar |
| Chest | [Abyssal Doomhound's Coreguard](https://www.wowhead.com/item=271540) | Catalyst — convert [Vest of Reverent Adoration](https://www.wowhead.com/item=239048) (Kings' Rest) |
| Wrist | [Silvermoon Agent's Deflectors](https://www.wowhead.com/item=244576) | Crafted |
| Gloves | [Abyssal Doomhound's Studded Gauntlets](https://www.wowhead.com/item=271538) | Entombed Sentinels (tier) |
| Belt | [Sash of the Forlorn Vessel](https://www.wowhead.com/item=268256) | The Coiled Altar |
| Legs | [Abyssal Doomhound's Legwraps](https://www.wowhead.com/item=271536) | Catalyst — convert [Coiled Hex Legguards](https://www.wowhead.com/item=268225) (The Coiled Altar) |
| Boots | [Sand-Shined Snakeskin Sandals](https://www.wowhead.com/item=159327) | Temple of Sethraliss |
| Ring 1 | [Vile Alchemist's Band](https://www.wowhead.com/item=268249) | Vashnik |
| Ring 2 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Trinket 1 | [Voracious Heart of Ula'tek](https://www.wowhead.com/item=270175) | Ula'tek |
| Trinket 2 | [Zul'jin's Guillotine Technique](https://www.wowhead.com/item=270173) | The Coiled Altar |
| Weapon | [Aman'muso, Warlord's Vengeance](https://www.wowhead.com/item=268209) (1H **axe**) & [Spellbreaker's Warglaive](https://www.wowhead.com/item=237840) (warglaive) | The Coiled Altar & Crafted |

> Three of the four tier slots are **Catalyst conversions** in this list, which is
> exactly why the 12.1 Catalyst change (inherits secondaries/tertiaries + cantrips)
> matters — pick the *best-statted* source piece to feed it, not just any piece of
> the right slot.

**Farmable alternatives** — obtainable outside the weekly lockout; immediate
character power, replaced over time as you progress (maxroll). Every source below
is in the **Season 2 Mythic+ pool**, so these become farmable when keys open
**Aug 18**; Mythic 0 is available in the pre-season week but on a **weekly** lockout.

| Slot | Item | Location |
|---|---|---|
| Head | [Hood of the Slithering Loa](https://www.wowhead.com/item=239033) | Temple of Sethraliss |
| Neck | [Graft of the Domanaar](https://www.wowhead.com/item=251234) | Voidscar Arena |
| Shoulder | [Somber Spaulders](https://www.wowhead.com/item=251223) | Voidscar Arena |
| Cloak | [Speakeasy Shroud](https://www.wowhead.com/item=251132) | Murder Row |
| Chest | [Vest of Reverent Adoration](https://www.wowhead.com/item=239048) | Kings' Rest |
| Wrist | [Rootwarden Wraps](https://www.wowhead.com/item=251183) | The Blinding Vale |
| Gloves | [Desiccator's Blessed Gloves](https://www.wowhead.com/item=159312) | Kings' Rest |
| Belt | [Whirling Dervish Sash](https://www.wowhead.com/item=159317) | Temple of Sethraliss |
| Legs | [Breeches of Deft Deals](https://www.wowhead.com/item=251130) | Murder Row |
| Boots | [Sand-Shined Snakeskin Sandals](https://www.wowhead.com/item=159327) | Temple of Sethraliss |
| Ring 1 | [Charged Sandstone Band](https://www.wowhead.com/item=158366) | Temple of Sethraliss |
| Ring 2 | [Signet of Snarling Servitude](https://www.wowhead.com/item=251136) | Murder Row |
| Trinket 1 | [Freightrunner's Flask](https://www.wowhead.com/item=250215) | Murder Row |
| Trinket 2 | [Resonant Bellowstone](https://www.wowhead.com/item=250228) | Murder Row |
| Weapon | [Thorntalon Edge](https://www.wowhead.com/item=251186) & [Singularity Slicer](https://www.wowhead.com/item=251231) | The Blinding Vale & Voidscar Arena |

⚠ **Check the weapon type on every weapon drop before equipping it** — see the
12.1 requirement above. This is new; there was no wrong answer in Season 1.

## Embellishments & crafted gear

- **[Hunter's Ritual Stone](https://www.wowhead.com/item=273060)** is the most
  powerful embellishment, but it **can only be crafted on weapons** — so crafting
  1–2 weapons with it is usually the best use (maxroll). *(Replaces S1's
  Darkmoon Sigil: Hunt in the same weapon-only role.)*
- **[Adorned Fang](https://www.wowhead.com/item=273069)** is the second strongest
  and **goes on any armor slot**, which makes it the flexible pick.
- **[Arcanoweave Lining](https://www.wowhead.com/item=240167)** is similar to
  Adorned Fang but "seems to output slightly lower DPS numbers" — so the S1
  advice of **2x Arcanoweave Lining is dead**; it is now the fallback, not the
  recommendation.
- **Remaining Sparks:** crafted items cap at **331 ilvl** vs regular items at
  **334** at max ilvl, so it's a small loss to equip crafted items outside your 2x
  embellishments unless you lack high-ilvl gear in that slot (maxroll). *(The 334
  ceiling is corroborated by Tier-1 game data — Myth Mistcrest tops out at 334,
  `_meta/moving-values.md`.)*
- **Crafting Sparks began dropping in the pre-season week**, so the crafted slots
  (wrist BiS + your embellishment carriers) are the one place you can bank real S2
  power before Aug 18.

## Enchants

Buy **[Miasmic Jewelbinder](https://www.wowhead.com/item=275707)** from the Great
Vault Vendor to add sockets to your **Helm**, **Wrists** & **Waist** — this is the
Season 2 replacement for S1's Radiant Jewelbinder.

| Slot | Enchant |
|---|---|
| Head | [Enchant Helm - Empowered Rune of Avoidance](https://www.wowhead.com/item=244007) & [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Shoulder | [Enchant Shoulders - Amirdrassil's Grace](https://www.wowhead.com/item=243991) |
| Chest | [Enchant Chest - Mark of the Worldsoul](https://www.wowhead.com/item=243977) |
| Wrist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Waist | [Miasmic Jewelbinder](https://www.wowhead.com/item=275707) (socket) |
| Legs | [Forest Hunter's Armor Kit](https://www.wowhead.com/item=244641) |
| Boots | [Enchant Boots - Lynx's Dexterity](https://www.wowhead.com/item=243953) |
| Ring 1 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Ring 2 | [Enchant Ring - Eyes of the Eagle](https://www.wowhead.com/item=243957) |
| Weapon | 2x [Enchant Weapon - Jan'alai's Precision](https://www.wowhead.com/item=243971) |

Changed from S1: the ring enchant moved from **Nature's Fury** to **Eyes of the
Eagle** (Crit), consistent with Crit leading the 12.1 stat order; the socket item
changed to Miasmic Jewelbinder. Everything else is unchanged.

## Gems

Unchanged from Season 1 in the captures.

- [Flawless Masterful Garnet](https://www.wowhead.com/item=240908) — main filler gem.
- [Powerful Eversong Diamond](https://www.wowhead.com/item=240967) — Unique; use
  one of each gem color to enhance it:
  - [Flawless Deadly Amethyst](https://www.wowhead.com/item=240898)
  - [Flawless Deadly Lapis](https://www.wowhead.com/item=240914)
  - [Flawless Deadly Peridot](https://www.wowhead.com/item=240890)

⚠ The filler gem is **Mastery** while the 12.1 stat order leads with **Crit**.
maxroll lists both together without comment; prefer Crit gems if a 12.1 sim
confirms the Icy Veins order.

## Consumables

- **Flask (Phial):** [Flask of the Shattered Sun](https://www.wowhead.com/item=241326)
  (maximum DPS) — or [Flask of Thalassian Resistance](https://www.wowhead.com/item=241320)
  (less DPS, more survivability). *(Unchanged from S1.)*
- **Combat Potion:** [Potion of Recklessness](https://www.wowhead.com/item=241288).
- **Health Potion:** [Concentrated Silvermoon Health Potion](https://www.wowhead.com/item=271884)
  (big burst of healing) — **new in 12.1**; health consumables were rescaled for
  the +25% max-level health pool, so the S1 Silvermoon Health Potion no longer
  keeps up. ⚠ Any pre-2026-08-11 health-potion number in your notes is wrong.
- **Food:** [Blooming Feast](https://www.wowhead.com/item=242273).
- **Weapon oil:** [Thalassian Phoenix Oil](https://www.wowhead.com/item=243734).
- **Augment Rune:** [Void-Touched Augment Rune](https://www.wowhead.com/item=259085).

New in 12.1 and relevant here: the **Cooldown Manager now tracks trinkets and
potions** (and racials), and trinkets / health potions / combat potions /
healthstones can be **pinged** from it — so on-use trinket and potion timing no
longer needs an addon (`endgame/`, `systems/macros.md`).

## TODO

- [ ] **sim-verify the 12.1 stat order and trinket ranking** on Bloodmallet /
      Raidbots once 12.1 Havoc sim data exists. Icy Veins' Crit > Mastery > Haste >
      Vers is Tier 3, published the day before the patch; Wowhead disagrees on the
      Haste/Vers tail with content dated 2026/02/25. The Fury retune is the reason
      to expect Haste's value to have moved — resolve it with a sim, not prose.
- [ ] **Re-check the gem and enchant picks against the settled stat order** — the
      captures still recommend a Mastery filler gem alongside a Crit ring enchant.
- [ ] **Confirm the S2 tier 4-set text in game from Aug 18** (Essence Break +
      Cycle of Hatred interaction) — it is a maxroll transcription of a set bonus
      no one has worn yet. @verify-ingame

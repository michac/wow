---
title: Protection Paladin — Talents & Builds (Midnight)
patch: 12.1
fetched: 2026-08-23
reviewed: 2026-08-23
sources:
  - knowledge/_meta/patch-notes/12.1.md  # tier 1, verbatim 12.1 notes, Paladin ▶ Protection block
  - knowledge/classes/paladin/protection/talents.md  # tier 1 tree structure (Blizzard API + wago @ 12.1.0.68914)
  - knowledge/classes/paladin/protection/ability-inventory.tsv  # tier 1 @ 12.1.0.69214 (hero_tree + live tooltips)
  - knowledge/classes/paladin/protection/simc-apl.md  # tier 1, simc APL, commit 0132642 (2026-08-18)
  - https://www.method.gg/guides/protection-paladin/talents  # tier 3, upd. 2026-07-09, describes 12.0.7
  - https://www.icy-veins.com/wow/protection-paladin-midnight-guide  # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/protection-paladin-raid-guide  # tier 3, 12.0.7
  - https://github.com/simulationcraft/simc/tree/midnight/profiles/MID1  # tier 1, MID1_Paladin_Protection.simc talent string (build 12.0.7.67808 — stale)
confidence: medium
---

# Protection Paladin — talents & builds (Midnight, 12.1)

Layer this over `talents.md` / `talents.json` (the full Tier-1 tree). This file
is the **narrative**: which hero tree, which loadout, and why.

⚠ **The priority list is not here.** `simc-apl.md` in this directory is the
Tier-1 12.1 priority source (simc commit `0132642`, 2026-08-18). Nothing below
states or reorders a rotation priority — read that file instead.

## Hero tree

**The pick for Mythic+ / dungeons is Lightsmith.**

**How strong that is, plainly:** it rests on **method.gg — Tier 3, updated
2026-07-09, describing patch 12.0.7, not re-verified at 12.1.** No Tier-1 or
Tier-2 12.1 source in this repo ranks the two hero trees against each other.
Treat it as the Season-1 default carried forward, not a measured 12.1 result.

**What the 12.1 APL does and does not settle.** `simc-apl.md` is Tier 1 and
current, but it is written for **both** hero trees and so cannot pick between
them: three `holy_armaments` rungs gated on `next_armament` are **Lightsmith**,
while the `hammer_of_light` rung and the `buff.undisputed_ruling.up` condition
are **Templar** *(Undisputed Ruling = Templar node, `talents.md` Hero: Templar
4,23)*. It carries **no profileset results and no `talents=` string** — it is a
priority list, not a comparison — so it is not evidence for either tree.

**⚠ Reopening condition.** Season 1 has **ended** and Season 2 opened
**2026-08-18** (`knowledge/_meta/game-version.md`), so every source behind this
pick predates the season it will be used in — and 12.1 retuned Protection
heavily (below). **Re-check the pick against a Season-2 source**: a post-12.1
guide revision, Warcraft Logs / Archon M+ hero-tree splits, or a profileset sim.
Any of those putting **Templar** ahead in M+ overrides this line; until one
exists, Lightsmith stands on Tier-3 Season-1 evidence.

The two trees, for context:

- **Lightsmith — Mythic+ / dungeons.** Adds the **Holy Armaments** system
  (**Sacred Weapon** damage buff + **Holy Bulwark** absorb, 15% max-health shield
  +2% every 2s for 20s, generating 3 Holy Power *[T1 tooltip @ 12.1.0.69214]*),
  the **Rite of Sanctification / Rite of Adjuration** choice, and
  **Blessing of the Forge** as the capstone. Absorb-heavy and forgiving.
- **Templar — raid / single-target.** Converts **Divine Toll** into a **Hammer
  of Light** burst button and layers **Shake the Heavens**, extended by **Higher
  Calling**. Excels on single-target. ⚠ 12.1 cut **Hammer of Light −33%** and
  **Empyrean Hammer −33%** *[T1 12.1 notes]*, so its 12.0.7 single-target edge
  is itself unverified at 12.1.

## What 12.1 changed for this spec

*All from `knowledge/_meta/patch-notes/12.1.md`, Paladin ▶ Protection (Tier 1).*

- **Power moved out of cooldown windows into baseline throughput** — the
  developers' note says so outright, and the numbers follow it: **Judgment
  +51%**, **Consecration +100%**, **Shield of the Righteous +150%**, **Hammer of
  the Righteous +50%**, **Avenger's Shield +30%**, **Lesser Weapon +50%**;
  against **Hammer of Light −33%**, **Empyrean Hammer −33%**, **Hammer and Anvil
  −20%**, **Bulwark of Righteous Fury 10%/stack (was 20%)**, **Divine Exaction's
  Divine Toll 80% (was 150%)**. ⚠ **Do not frame this spec as burst-window-shaped
  any more** — that framing described 12.0.7.
- **Avenging Wrath now gives +10% damage and healing and +10% critical strike**
  (was +20% damage/healing). ⚠ The **12.1.0.69214 spell tooltip in
  `ability-inventory.tsv` still reads 20%** for all three — that is the generic
  spell text without the Protection aura; the per-spec patch note is Tier 1 and
  wins.
- **Sanctified Wrath has been removed.** *(Verified absent from `talents.json` /
  `talents.md` / `ability-inventory.tsv` — nothing in this file ever referenced
  it.)*
- **Many talents have changed position in the talent tree.** Every position and
  pairing below was re-read off `talents.md` @ 12.1.0.68914; older prose about
  pathing is not trustworthy.
- **Guardian of Ancient Kings now has an 8 second initial cooldown.** This is a
  two-stage cooldown — our tooling reporting **`cd=8`** (`ability-inventory.tsv`)
  instead of 180s is **correct data, not a bug**.
- **Sentinel duration increased to 20 seconds** and it **now inherits Avenging
  Wrath's critical strike bonus**; **Righteous Protector** reduces its cooldown
  too *(see below)*.
- **Improved Ardent Defender redesigned** — now +20% maximum health while active,
  and it no longer cancels when fatal damage is sustained (a debuff marks that it
  did).
- **Seal of Reprisal redesigned** — Blessed Hammer / Crusader Strike now makes
  enemies deal **10% less damage to you for 8s**.
- **Bulwark of Order absorb raised to 75%** of Avenger's Shield damage (was 60%).
- **New talent: Blessed Word** — Word of Glory can no longer crit; its healing is
  increased by your crit chance and 80% of overhealing becomes an absorb. It is
  the **choice partner of Valiant Crusade** (spec 4,16).
- **Lightsmith's changes:** **Blessed Assurance now +100%** (was +200%) to the
  next Blessed Hammer / Hammer of the Righteous; **Divine Guidance redesigned**;
  **Masterwork updated**; **Sacred Weapon and Holy Bulwark now extend their
  duration when reapplied by the same caster**; **Reflection of Radiance's
  activation chance significantly reduced**; Rite of Adjuration healing +25%.

## Class + spec tree — the load-bearing talents

*Positions and choice pairings from `talents.md` @ 12.1.0.68914 (Tier 1).*

- **Righteous Protector** (spec 11,21) — **Avenging Wrath *and Sentinel* have 50%
  reduced cooldown and 40% reduced duration** *[T1 tooltip @ 12.1.0.69214]*. This
  is what makes the short-Wings cadence possible, and it is also what pays for
  Sentinel. Near-mandatory.
- **Solace / Instrument of the Divine** (spec 6,20, **choice**) — Instrument lets
  Shield of the Righteous consume up to 2 extra Holy Power for +50% damage per
  extra point; Solace makes Consecration heal you for 375% of its damage (raised
  from 300% in 12.1). With SotR at +150% baseline, this choice is worth re-testing
  rather than assumed.
- **Grand Crusader** (spec 4,18) + **Bulwark of Order** (spec 6,17) — Avenger's
  Shield resets (15% on avoid / Crusader Strike) and a 75%-of-damage absorb.
- **Improved Ardent Defender / Seal of Reprisal** (spec 7,18, **choice**) — ⚠ this
  pairing changed: Improved Ardent Defender is **no longer paired with Blessing of
  Spellwarding**, and both halves were redesigned in 12.1 (above). Big personal
  cooldown vs a constant 10% damage-taken reduction.
- **Blessing of Spellwarding / Uther's Counsel** (class 5,17, **choice**) — the
  magic-immunity wall now sits here.
- **Avenging Wrath** (spec 6,18) and **Sentinel** (spec 10,18) are **separate
  nodes, not a choice pair** — a 12.0.7 claim that they are is wrong. 12.1
  deliberately "reduce[s] the opportunity cost associated with taking Sentinel".
- **Sanctified Plates** (class 6,6) / **Holy Aegis** (class 8,2) / **Faith's
  Armor** (class 10,1) — passive mitigation floor.
- **Consecration in Flame** (spec 7,21) / **Sanctuary** (spec 8,20) /
  **Consecrated Ground** (class 7,7) — reward staying in Consecration; bigger
  after the +100% Consecration retune.
- **Final Stand** (spec 11,19) — makes Divine Shield also **taunt**; situational.
- **Valiant Crusade / Blessed Word** (spec 4,16, **choice**) — Blessed Word is the
  new 12.1 option; Valiant Crusade no longer cancels on death.

## Hero-tree specifics

**Lightsmith** — the Holy Armaments loop:
- **Holy Armaments** (7,11) grants alternating **Holy Bulwark / Sacred Weapon**
  charges. ⚠ 12.1: reapplying either **by the same caster extends its duration**
  rather than clipping it.
- **Rite of Sanctification / Rite of Adjuration** (8,9, choice) — Sanctification
  is +5% armor / +2% primary for an hour; Adjuration is the healing option
  (+25% in 12.1).
- **Divine Guidance / Blessed Assurance** (8,11, choice) — ⚠ **this is a
  Lightsmith hero choice, not a spec-tree one**, and both halves changed in 12.1.
  **Divine Guidance** (redesigned): each Holy Power ability cast makes your next
  Consecration deal immediate Holy damage split across all enemies, healing up to
  3 nearby allies for 30% of it — the old "5-stack → empowered
  Consecration/Shield of the Righteous" description is dead, though the stacking
  buff itself still exists (`simc-apl.md` reads it). **Blessed Assurance** is now
  **+100%** (was +200%) to the next Blessed Hammer / Hammer of the Righteous.
- **Masterwork** (8,12) — 12.1: after a Holy Armament, your next **3** casts of
  Hammer of the Righteous / Blessed Hammer / Crusader Strike bestow a **Lesser
  Armament** of the same kind on a nearby ally. **Lesser Weapon damage +50%.**
- **Solidarity** (8,10) — bestowing an Armament on an ally also gives you its
  benefit, and vice versa.
- **Hammer and Anvil** (9,12) — Judgment crits heal up to 5 injured allies
  (damage **−20%** in 12.1).
- **Reflection of Radiance** (10,11) — ⚠ **re-check before building around it.**
  Its 12.1 tooltip reads "chance to gain **Awakening**" when Holy Bulwark absorbs
  or Sacred Weapon acts, and 12.1 "significantly reduced" that chance. The
  12.0.7 claim that it feeds extra **Grand Crusader** procs / Avenger's Shields
  is **not what the live tooltip says**, and **Awakening does not appear anywhere
  in Protection's 12.1 ability inventory**, so what it actually grants this spec
  is **unverified**. @verify-ingame
- **Blessing of the Forge** (11,11) capstone — Avenging Wrath summons an extra
  Sacred Weapon which echoes your Holy Power abilities during Wings.

**Templar** — the Divine Toll → Hammer of Light loop:
- **Light's Guidance** (1,23) / **Light's Judicator** (3,24) wire Hammer of Light
  onto Divine Toll.
- **Shake the Heavens** (2,22) upkeep is the skill test; **Higher Calling** (3,22)
  extends it.
- **Undisputed Ruling** (4,23), **Endless Wrath / Sanctification** (4,21),
  **Hammerfall** (4,22), **Wrathful Descent** (2,23) shape the burst;
  **Light's Deliverance** (5,23) is the capstone.
- **Divine Exaction / Seal of the Templar** (4,24, choice) — Divine Exaction's
  Divine Toll effectiveness was cut to **80%** (was 150%) in 12.1.

## Build variants

⚠ **Tier 3, method.gg, 2026-07-09, describing 12.0.7 — not re-verified at 12.1.**
Kept because no Season-2 source has replaced it; the talent *names* below were
re-checked against `talents.md` @ 12.1.0.68914 and all still exist, but the
*recommendations* have not been re-derived after the 12.1 retune.

- **Mythic+ (Lightsmith):** Divine Toll + **Divine Resonance** (class 7,4 choice
  vs Quickened Invocation) for interrupt coverage, **Blessed Hammer** over Hammer
  of the Righteous (spec 3,19 choice) for AoE, **Punishment** (class 6,7) for
  bonus casts on interrupt, **Divine Guidance** over Blessed Assurance on the
  Lightsmith choice node.
- **Raid single-target (Templar):** **Shake the Heavens** maintenance, **Hammer
  of Light** windows, **Blessed Assurance** for the empowered Hammer of the
  Righteous. ⚠ Both of that build's payoffs were nerfed in 12.1 (Hammer of Light
  −33%, Blessed Assurance 200%→100%).

## Talent string (reference only)

From the SimC **MID1_Paladin_Protection** profile, build **12.0.7.67808**:

```
CIEAAAAAAAAAAAAAAAAAAAAAAsMzAzyMLmZMDLLDzYmFbzYAAAAAAAAg0MziZMmxYmt2AgBADsNAAwMTbzMbzAEYzADWMzMAzMAALzAMzAG
```

> ⚠ **This is a 12.0.7 string and is expected to be wrong at 12.1.** Import
> strings are tree-version-sensitive and 12.1 states "many talents have changed
> position in the talent tree" *and* removed Sanctified Wrath, so this may fail
> to import or silently land on different nodes. The 12.1 APL source
> (`simc-apl.md`) is the class module, which **carries no `talents=` string at
> all**, so there is no Tier-1 12.1 loadout in this repo yet. Verify node-by-node
> on import, and confirm which hero tree loads. @verify-ingame

## TODO

- [ ] Capture a verified **12.1** Lightsmith (M+) and Templar (raid) import
      string — the 12.0.7 string above is the only one we have.
- [ ] Re-sim the ST/AoE hero-tree gap on 12.1 (profilesets), which is what would
      actually settle the Lightsmith pick above.
- [ ] Resolve what **Reflection of Radiance**'s "Awakening" grants Protection.

## Changelog

- **2026-08-23** — brought to 12.1. Corrected four claims that were wrong even
  before 12.1 or were invalidated by it: Divine Guidance / Blessed Assurance are
  a **Lightsmith hero** choice (was filed under the spec tree) and Divine
  Guidance was redesigned; Improved Ardent Defender pairs with **Seal of
  Reprisal**, not Blessing of Spellwarding; Avenging Wrath and Sentinel are
  **separate nodes**, not a choice pair; Reflection of Radiance grants
  **Awakening**, not Grand Crusader procs. Removed the burst-window framing
  (12.1 moved power into baseline throughput) and the blanket
  "NOT RE-VERIFIED FOR 12.1" banner, replaced by per-claim warnings.

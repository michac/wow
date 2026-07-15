---
title: Retribution Paladin — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/retribution-paladin/talents  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Paladin_Retribution.simc  # tier 1 talent string + APL, 2026-07-11
  - https://www.icy-veins.com/wow/retribution-paladin-pve-dps-guide  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Retribution Paladin — Talents & Builds (Midnight Season 1)

Layer this on top of the generated `talents.md` / `talents.json` (the full
node tables). This file records the **hero-tree choice, recommended loadouts,
and the key interactions** that drive the rotation in `rotation.md`.

## Hero tree: Templar (everything)

**Templar is the S1 default for all content** — raid, M+, and delves —
"slightly edging out Herald of the Sun" (method.gg). Its identity:

- **Wake of Ashes → Hammer of Light.** For 20s after Wake of Ashes, your Holy
  Power spender is replaced by **Hammer of Light** (a 5-HP nuke). This is the
  centerpiece the rest of the tree feeds.
- **Light's Deliverance** — after enough Hammer of Light / Holy Power activity,
  grants *free* Hammer of Light procs to dump inside your burst window.
- **Divine Hammer** — after **Divine Toll**, summons **Empyrean Hammers**
  around you for area holy damage.
- **Shake the Heavens** / **Wrathful Descent** / **Undisputed Ruling** —
  amplify the Hammer of Light window and Empyrean Hammer output.
- **Sacrosanct Crusade** — Wake of Ashes also heals/shields, so WoA doubles as
  a defensive.

**Herald of the Sun** remains viable but delivers a "less impactful"
experience: it builds around **Dawnlight**, **Eternal Flame**, and the
**Sun's Avatar** window rather than Hammer of Light. Take it only if you
specifically prefer that playstyle or a fight rewards its sustained model.

## The core split: Avenging Wrath vs Radiant Glory

Both recommended Templar builds share the same skeleton; they differ in how
the burst window is triggered:

- **Standard (Execution Sentence + manual Avenging Wrath):** you press
  Avenging Wrath on cooldown and pair Execution Sentence into it. This is the
  simc profile default and the method single-target build.
- **Radiant Glory variant:** **Radiant Glory** removes Avenging Wrath from
  your bars — **Wake of Ashes** and **Execution Sentence** auto-trigger the
  wings. It's one fewer button and tighter alignment; method notes you can
  "swap Execution Sentence for Radiant Glory and reallocate one point from
  Heart of the Crusader into Sanctify to amplify the 30-second burst window."
  Roughly even in sims — a comfort / consistency choice.

**Crusade** (spec-tree row 11) is the alternative to Avenging Wrath: a
stacking haste/damage ramp built by spending Holy Power (up to ~20% haste),
peaking higher but slower. method pairs Avenging Wrath + Execution Sentence as
the S1 default.

## Recommended loadouts (method.gg 12.0.7)

**Single-target / Raid (Templar):**
```
CYEAAAAAAAAAAAAAAAAAAAAAAAAAAMAgRz22MzsMMzAAAAAAwoMLGmZsNMbDzsNjxYmhZsx2wAAQmZabmZbGAwGgBAjZYgZMmNsMDGGDDG
```
- Execution Sentence as the primary cooldown spender.
- Alt: swap Execution Sentence → **Radiant Glory**, move one point from Heart
  of the Crusader into **Sanctify** to fatten the 30s burst.

**Raid Cleave & Mythic+ (Templar):**
```
CYEAAAAAAAAAAAAAAAAAAAAAAAAAAMAAa22mZmlxYmBAAAAAwMlZxwMjthZbYmtZMGzMMjF2GGwsMbzMzWDCAAYBwAgxMMDmxYWAmZGGDDG
```
- Includes **Tempest of the Lightbringer** (enables the 2-target Divine Storm
  threshold when Jurisdiction is dropped) for cleave.
- Substitute **Jurisdiction** back in for stronger single target if a key
  doesn't need the cleave.

**simc profile talent string (Tier 1, for reference / import check):**
```
CYEAAAAAAAAAAAAAAAAAAAAAAAAAAAAQz22MzsMMzAAAAAAwoMmhZGbDz2wMbzYMmZYGbsNMAAkZm2mZ2mBAsBYAwYGmBzYMbYZGMMmxgB
```

> Import strings are tree-version-sensitive — confirm each loads as **Templar**
> in-game before trusting (one bad character breaks an import). @verify-ingame

## Key talent interactions

- **Final Verdict** (spec tree) upgrades Templar's Verdict into the primary
  single-target spender (bigger hit, ranged component). The APL's
  `templars_verdict` action *is* Final Verdict in these builds.
- **Empyrean Power** — Divine Storm periodically becomes a **free instant**;
  it's a gain even on single target when it procs (see rotation step 11).
- **Art of War** / **Righteous Cause** (choice node) — reset/proc **Blade of
  Justice** for free instant casts; high priority to spend. **Light Within**
  (apex) amplifies the Art of War proc (Blade of Justice +150%) and adds +20%
  Divine Storm / Final Verdict during Avenging Wrath.
- **Holy Flames + Expurgation** — Blade of Justice applies the Expurgation fire
  DoT; the APL front-loads a Blade of Justice in the opener specifically to get
  Expurgation ticking before Wake of Ashes / potion.
- **Templar Strikes vs Crusading Strikes** (choice node) — Templar Strikes is
  the active two-hit filler builder; **Crusading Strikes** instead makes
  auto-attacks passively generate Holy Power (track the pending auto so
  finishers fire at effectively 4 HP without overcapping).
- **Tempest of the Lightbringer** + **Jurisdiction** together set the AoE/ST
  Divine Storm threshold: with Tempest and *without* Jurisdiction, cleave the
  Divine Storm rotation at **2+** targets instead of 3+.
- **Divine Toll → Divine Hammer** — Divine Toll isn't just Holy Power; with
  Divine Hammer it seeds the Empyrean Hammer area damage that carries Templar's
  AoE.

## Class-tree utility flex

The spec tree has little room to move; the class tree is where you adjust per
encounter: **Cleanse Toxins** (dispel duty), **Empyreal Ward** / **Faith's
Armor** / **Sanctified Plates** (mitigation), **Righteous Protection** /
**Blessing of Sacrifice** (external defense), **Blinding Light** /
**Hammer of Justice** (CC), and the **Divine Steed** / **Cavalier** mobility
node. Keep **Rebuke** and an interrupt-adjacent kit slotted for group content.

## Open items

- Stat priority, enchants, gems, consumables, and crafted/embellishment meta
  not yet captured — pull from Icy Veins/method gearing pages on next pass.
- Confirm exact secondary-stat priority (Ret has historically wanted Haste →
  Crit/Mastery; sim on Raidbots). @verify-ingame
- Re-verify import strings + hero-tree edge (Templar vs Herald) if a later
  hotfix retunes the trees.

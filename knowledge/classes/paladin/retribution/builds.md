---
title: Retribution Paladin — Talents & Builds (Midnight S1)
patch: 12.1
fetched: 2026-08-17
reviewed: 2026-08-19
sources:
  - knowledge/classes/paladin/retribution/simc-apl.md  # tier 1, 12.1 priority list @ commit 91e711b (2026-08-11) — hero-tree corroboration, choice-node reading
  - knowledge/classes/paladin/retribution/ability-inventory.tsv  # tier 1, DB2 @ 12.1.0.69214 — tree/hero placement, node+entry ids, resolved descriptions
  - https://www.method.gg/guides/retribution-paladin/talents  # tier 3, Midnight 12.0.7, 2026-07-11 — the hero-tree recommendation and the loadouts, NOT re-verified at 12.1
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Paladin_Retribution.simc  # tier 1 talent string, 2026-07-11 (12.0.7 profile)
  - https://www.icy-veins.com/wow/retribution-paladin-pve-dps-guide  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

> ⚠ **PARTIALLY RE-VERIFIED FOR 12.1 (2026-08-17). Read which half.**
>
> **Re-verified against Tier-1 12.1 data:** every talent named below exists at
> **12.1.0.69214** with the tree and hero placement stated (`ability-inventory.tsv`),
> and every rotational interaction below is corroborated by the 12.1 priority list
> (`simc-apl.md` @ commit `91e711b`, 2026-08-11) or by a resolved 12.1 spell
> description. Three claims were **wrong and are rewritten**, not annotated — see the
> Changelog.
>
> **NOT re-verified:** the **hero-tree recommendation** and all **three talent import
> strings** are still 2026-07-11's from **2026-07-11 / 12.0.7**. No Tier-1 or Tier-3
> 12.1 source was consulted for either. Import strings are tree-version-sensitive and
> a 12.0.7 string may not load at 12.1; they are kept, clearly dated, rather than
> re-stamped as current.
>
> **Not covered at all:** stat priority, enchants, gems, consumables and
> embellishments — see *Open items*.
>
> Season 1 has ended (`_meta/game-version.md`); Season 2 opens 2026-08-18, so every
> "S1 default" below is a statement about a season that is over.

# Retribution Paladin — Talents & Builds (Midnight Season 1)

Layer this on top of the generated `talents.md` / `talents.json` (the full
node tables). This file records the **hero-tree choice, recommended loadouts,
and the key interactions** that drive the rotation in `rotation.md`.

## Hero tree: Templar (everything)

**Templar is the S1 default for all content** — raid, M+, and delves —
"slightly edging out Herald of the Sun" (method.gg, **Tier 3, 2026-07-11, 12.0.7,
not re-verified at 12.1**). Its identity:

- **Wake of Ashes → Hammer of Light.** For 20s after Wake of Ashes is cast, **the
  Wake of Ashes button itself** is replaced by **Hammer of Light** (a 3-Holy-Power
  finisher, same cost as every other spender) — Light's Guidance 427445,
  *"Wake of Ashes is replaced with Hammer of Light for 20 sec after it is cast"*
  *[T1: resolved spell description @ 12.1.0.69214]*. This is the centerpiece the rest
  of the tree feeds. ⚠ It is the **Wake of Ashes** button that is replaced, not your
  Holy Power spender *[T1]*.
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

### How much the 12.1 APL corroborates this — less than it looks

The 12.1 priority list is **written for both hero trees**, so it is weak evidence for
the pick and must not be quoted as strong evidence:

- **For Templar:** the body of `actions.finishers` is the Hammer of Light loop —
  `hammer_of_light` is the top finisher, and both spender lines are guarded on
  `buff.hammer_of_light_ready` / `buff.hammer_of_light_free`. `buff.undisputed_ruling`
  (Templar, node 95186) gates a clip condition. Remove Templar and a third of the
  finisher list stops meaning anything.
- **For Herald:** `talent.walk_into_light` appears on **two** lines
  (`hammer_of_wrath,if=talent.walk_into_light` and the Art of War / Righteous Cause
  Blade of Justice line). It is a **Herald of the Sun** hero talent — node 95094,
  entry 117691, spell 1263782 *[T1: `ability-inventory.tsv` @ 12.1.0.69214]*.

⚠ **`templar_strike` and `templar_slash` are not Templar-hero evidence.** They come
from **Templar Strikes** 406646, a **spec-tree** talent (node 109374), available on
either hero tree *[T1: `ability-inventory.tsv` @ 12.1.0.69214]* — so their presence in
the APL says nothing about which hero tree it was generated for.

So the hero-tree call still rests entirely on the Tier-3 method.gg recommendation
above, which describes 12.0.7. Re-check it rather than treating the APL's Templar
density as confirmation:

- Retribution hero tree — is Templar still ahead of Herald of the Sun at 12.1 / Season 2? The only source is method.gg @ 12.0.7 / 2026-07-11 and the 12.1 APL is written for both trees. @verify-ingame

## The core split: Avenging Wrath vs Radiant Glory

Both recommended Templar builds share the same skeleton; they differ in how
the burst window is triggered:

- **Standard (Execution Sentence + manual Avenging Wrath):** you press
  Avenging Wrath on cooldown and pair Execution Sentence into it. This is the
  simc profile default and the method single-target build.
- **Radiant Glory variant:** **Radiant Glory** removes Avenging Wrath from
  your bars — *"Avenging Wrath is replaced with Radiant Glory. Wake of Ashes
  activates Avenging Wrath for 8 sec"* (458359, node 81549, entry 102525)
  *[T1: resolved spell description @ 12.1.0.69214]*. It's one fewer button and
  tighter alignment; method notes you can
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

> ⚠ **All three strings above are 12.0.7 (2026-07-11) and none has been loaded at
> 12.1.** Import strings are tree-version-sensitive and one bad character breaks an
> import; a string that no longer parses will fail loudly, but one that parses into a
> *different* build will not.
>
> - Retribution talent import strings — do all three 12.0.7 strings above still load at 12.1, and does each resolve to Templar with the talents this file names? @verify-ingame

## Key talent interactions

- **Final Verdict** (spec tree) upgrades Templar's Verdict into the primary
  single-target spender (bigger hit, ranged component). The APL's
  `templars_verdict` action *is* Final Verdict in these builds.
- **Empyrean Power** (326732, node 92860) — *"Crusader Strike has a 15% chance to
  make your next Divine Storm free and deal 15% additional damage"*
  *[T1 @ 12.1.0.69214]*. It's a gain even on single target when it procs: the APL's
  `ds_castable` variable lets `buff.empyrean_power.up` satisfy the Divine Storm gate
  on its own, with no target-count term. ⚠ On a **Crusading Strikes** build Crusader
  Strike is the auto-attack, so the proc source is passive.
- **Art of War** / **Righteous Cause** (choice node) — reset/proc **Blade of
  Justice** for free instant casts; high priority to spend. **Light Within**
  (apex) amplifies the Art of War proc (Blade of Justice +150%) and adds +20%
  Divine Storm / Final Verdict during Avenging Wrath.
- **Holy Flames + Expurgation** — Blade of Justice applies the Expurgation fire
  DoT; the APL front-loads a Blade of Justice in the opener specifically to get
  Expurgation ticking before Wake of Ashes / potion. ⚠ **Two spells are named
  Expurgation and they are not interchangeable:** `383344` is the passive talent node,
  and the DoT that actually lands on the target is **`383346`** — confirmed in client
  2026-08-19 by filtering a display to a candidate id set and matching the icon
  (`383346` shares Blade of Justice's `SpellIconFileDataID` 1360757; the talent's is
  1394971). Anything keying on the target debuff wants 383346.
- **Templar Strikes vs Crusading Strikes** (choice node) — **Templar Strikes**
  (406646, node 109374) keeps the button: *"Crusader Strike loses a charge but is now
  a combo ability"*, Templar Strike followed by Templar Slash.
  **Crusading Strikes** (404542) **deletes it**: *"Crusader Strike replaces your
  auto-attacks"*, so there is no filler button at all and the priority ends at
  Judgment. *[T1: resolved spell descriptions @ 12.1.0.69214]* Track the pending auto
  so finishers fire at effectively 4 HP without overcapping.
- **Tempest of the Lightbringer** + **Jurisdiction** together set the AoE/ST
  Divine Storm threshold: with Tempest and *without* Jurisdiction, cleave the
  Divine Storm rotation at **2+** targets instead of 3+.
- **Divine Toll → Divine Hammer** — Divine Toll isn't just Holy Power; with
  Divine Hammer it seeds the Empyrean Hammer area damage that carries Templar's
  AoE.
- **Improved Blade of Justice** (403745) — *"Blade of Justice now has 2 charges"*
  *[T1 @ 12.1.0.69214]*. Without it Blade of Justice is a single-charge button. ⚠ The
  generated inventory's `cooldown` column reads `—` / sub-1s for it, which is the
  charge-ability artifact `abilities.md` warns about, not a real recharge.
- **Empyrean Legacy** (387170, node 93173) — the APL treats it as a **single-target
  spender** empowerment: `ds_castable` carries `&!buff.empyrean_legacy.up`, i.e. do not
  Divine Storm while it is up. ⚠ The resolved 12.1 description for 387170 reads
  *"Avenging Wrath empowers your next Word of Glory to automatically activate Light of
  Dawn…"*, which is a **healing** effect and describes something else entirely. One of
  the two is wrong and the tooltip is the more likely bleed (`abilities.md` records the
  same failure mode on Shield of Vengeance). Trust the APL's usage until the in-game
  tooltip settles it.
  - Empyrean Legacy 387170 — does the in-game tooltip describe a spender empowerment (as the APL uses it) or a Word of Glory / Light of Dawn healing effect (as the resolved 12.1 description says)? @verify-ingame

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
- Confirm exact secondary-stat priority (Ret has historically wanted Haste → Crit/Mastery; sim on Raidbots). @verify-ingame
- Re-verify the hero-tree edge against a Season 2 source after 2026-08-18 — see the *How much the 12.1 APL corroborates this* section, where the marker for it lives.
- Load all three import strings at 12.1 — marker in *Recommended loadouts*.
- Settle Empyrean Legacy 387170's description — marker in *Key talent interactions*.

## Changelog

**2026-08-19 — two retrospective notes moved off the claims.** Two rows carried their own
correction history in the body: the Wake of Ashes / Hammer of Light row said the old
"your Holy Power spender is replaced" claim "stood here and was wrong", and the
`templar_strike` note said "an earlier reading counted them for Templar". Both claims are
now stated once, in the present tense, with their evidence. What the notes were recording:
**Hammer of Light replaces the Wake of Ashes button, not the spender**, and **Templar
Strikes is a spec-tree talent on either hero tree**, so APL density of `templar_strike` is
not hero-tree evidence and the hero-tree call still rests on the Tier-3 method.gg reading.

**2026-08-17 — partial 12.1 re-verification.** The whole file was carrying a
"NOT RE-VERIFIED FOR 12.1" banner; the banner is now split so a reader can tell which
claims were checked. Every talent, id, tree placement and rotational interaction below
was re-checked against `ability-inventory.tsv` @ 12.1.0.69214 and `simc-apl.md`
@ commit `91e711b`. **The hero-tree recommendation and the three import strings were
not** and are still 12.0.7 / method.gg / 2026-07-11.

Three claims were wrong and are **rewritten, not annotated**:

- **"your Holy Power spender is replaced by Hammer of Light"** — it is **Wake of
  Ashes** that is replaced (Light's Guidance 427445).
- **"Crusading Strikes makes auto-attacks passively generate Holy Power"** was written
  as if the filler button survived. It does not: Crusader Strike *becomes* the
  auto-attack, and the build has no filler button.
- The APL was treated as corroborating Templar. It is written for **both** hero trees
  — `talent.walk_into_light` is Herald of the Sun — so it corroborates far less than it
  appeared to, and `templar_strike` / `templar_slash` are spec-tree, not hero-tree,
  evidence.

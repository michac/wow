---
title: Devastation Evoker — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/evoker/devastation/ability-inventory.tsv  # tier 1, DB2 @ 12.0.7.67808 — names, spellIDs, origin, cooldowns
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Evoker_Devastation.simc  # tier 1 APL + talent string, 2026-07-11
  - https://wago.tools/db2 SpellName @ 12.0.7  # tier 1 game-data name reconcile, 2026-07-11
  - https://www.method.gg/guides/devastation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/devastation-evoker-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
confidence: medium
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Devastation Evoker — Abilities (Midnight S1)

## Overview

Devastation is Evoker's ranged-caster DPS spec — a mid-range (25 yd) "empower"
caster built around two resources:

- **Essence** — a passively-regenerating point pool (base **5**, or **6** with
  *Power Nexus*). Spent on **Disintegrate** (single-target channel) and **Pyre**
  (instant AoE). **Essence Burst** is the key proc: it makes the next Essence
  spender **free**, and stacks to 2 with *Essence Attunement*. Empowered casts
  and Living Flame (via *Ruby/Azure Essence Burst* and *Leaping Flames*) generate
  it.
- **Empowerment** — **Fire Breath**, **Eternity Surge**, and **Deep Breath** are
  *empower* spells: you hold the cast to raise its rank (I–IV), trading cast time
  for more targets / more damage. In practice Devastation casts **Fire Breath and
  Eternity Surge at Rank 1** (short cast, on cooldown) and only pushes higher
  ranks when *Tip the Scales* makes the cast instant or for wide AoE.

Playstyle: keep the two short empower cooldowns rolling, pool them into
**Dragonrage** (the 2-minute burst window), and chain **Disintegrate** to spend
Essence without gaps. Mobility is skill-expressed through **Hover**, which lets
you cast and channel while moving (weave it right after an instant so it hides
inside the GCD).

**Hero trees (Midnight S1):**
- **Scalecommander** — the meta pick across most content. Empower casts grant
  **Mass Disintegrate** charges that turn Disintegrate into a multi-target cleave,
  and **Deep Breath** becomes a rotational damage button (via *Imminent
  Destruction* / *Onyx Legacy* / *Bombardments*).
- **Flameshaper** — a concentrated-AoE / DoT-focused alternative. Grants a
  **second Fire Breath charge**, and **Consume Flame** detonates the remaining
  Fire Breath DoT for a burst. Weaker on target swaps. Its actives at 12.0.7 are
  **Fire Torrent** and **Consume Flame** — *not* Engulf, which no longer exists
  (see the note at the foot of this file).

## Ability inventory

> **Where the numbers come from.** `ability-inventory.tsv` in this folder is the
> Tier-1 record for **name, spellID, origin and cooldown** (DB2 @ 12.0.7.67808) —
> read it rather than trusting a number restated here. A `[T1]` stamp marks a
> cooldown taken from it; a `~` value is a Tier-3 approximation from simc / Icy
> Veins / method.gg that nobody has measured, and the `@verify-ingame` markers
> that remain ask about cast times, charges and mechanics, which that file has no
> column for.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.0.7.67808).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Living Flame | Rotational-builder (filler) | — | 1.9s cast (instant while Hover/Burnout) | Baseline filler; deals Fire dmg (heals when cast on an ally). Chance to grant Essence Burst; with *Leaping Flames* bounces to extra targets after an empower. |
| Azure Strike | Rotational-builder (filler) | — | Instant | Instant Spellfrost bolt hitting the target + 1 nearby enemy (2 total). Low-priority filler / movement filler. |
| Disintegrate | Rotational-spender (ST) | 3 Essence | ~3s channel (3 ticks) | Primary single-target spender. **Chain-cast** it (recast just before the channel ends) to avoid tick gaps. *Mass Disintegrate* (Scalecommander) makes it cleave. |
| Pyre | Rotational-spender (AoE) | 3 Essence | Instant | Instant AoE Fire nova at the target. Preferred spender at 3–4+ stacked targets; builds *Charged Blast*. |
| Fire Breath | Major cooldown / DoT | — | Empower (hold), ~30s CD | Frontal cone: burst on cast + a Fire DoT. Cast at **Rank 1** on cooldown; generates Essence Burst. Flameshaper gets a **2nd charge**. @verify-ingame (exact CD) |
| Eternity Surge | Major cooldown (burst, talent) | — | Empower (hold), 30s `[T1]` | Focused Spellfrost burst; higher ranks split across more targets (with *Eternity's Span* it hits 2× targets per rank). Cast on cooldown, Rank 1 in ST — at 30s it is a rotational button, not a saved cooldown, and it should land four times inside a Dragonrage cycle. |
| Dragonrage | Major cooldown | — | Instant, 120s CD | The burst window: buffs damage, fires Pyre volleys, and (with *Animosity*) is **extended** each time you empower during it. Line Fire Breath + Eternity Surge inside it. |
| Deep Breath | Major cooldown / Movement | — | ~120s CD (reduced by *Onyx Legacy* / *Imminent Destruction*) | Fly across the target area dealing Fire damage along the path. Doubles as a gap-closer. Core rotational button for **Scalecommander**. |
| Tip the Scales | Major cooldown (utility) | — | Instant, 120s CD | Makes your next empower spell cast **instantly at max rank**. Usually spent on Eternity Surge (or Fire Breath) inside Dragonrage. |
| **Shattering Stars** | Passive (spec talent) | — | — | Spec talent **1265802**, and a **passive** in Midnight — not a pressed button. The War Within's active *Shattering Star* (instant, ~20s CD, 2 charges) is gone; what survives is the plural-named passive. |
| Azure Sweep | Rotational (Midnight-new, spec talent) | — | Passive/triggered | Midnight addition: empower/Eternity-Surge casts unleash a Spellfrost sweep on nearby enemies; appears in the APL as its own priority entry (`azure_sweep`). @verify-ingame |
| Mass Disintegrate | Passive (Scalecommander hero) | — | Passive | Empower casts grant charges that make the next Disintegrate(s) hit all nearby enemies. Defining Scalecommander mechanic. |
| Unravel | Rotational (talent, situational) | 1 Essence | Instant | Shatters an enemy absorb shield for Spellfrost damage; listed PASSIVE in the 12.0.7 tree — may be reworked from the old active. @verify-ingame |
| Rising Fury | Apex (talent, active) | — | during Dragonrage | Midnight apex: active/effect tied to Dragonrage granting stacking haste and Essence Burst. Listed ACTIVE row 14,18 in the tree. @verify-ingame |
| Obsidian Scales | Defensive | — | Instant, ~150s CD (2 charges w/ *Obsidian Bulwark*) | Reduces damage taken (~30%). Core survival cooldown. @verify-ingame (value/CD) |
| Renewing Blaze | Defensive / self-heal (talent) | — | Instant, ~90s CD | Heals a % of damage taken over the following seconds — a self-heal-over-time. @verify-ingame |
| Zephyr | Defensive (raid, talent) | — | Instant, 120s `[T1]` | Grants you + nearby allies a burst of movement speed and damage reduction. |
| Verdant Embrace | Movement / heal | — | Instant, ~24s CD | Fly to an ally (or pull them) and heal them. Doubles as mobility; triggers *Ancient Flame*. @verify-ingame |
| Emerald Blossom | Self-heal / AoE heal | Essence (or free proc) | Instant / **30s** `[T1]` | Ground heal at the target area; used off *Ancient Flame*/green procs for damage builds. |
| Rescue | Movement / utility (talent) | — | Instant, 60s `[T1]` | Grip a friendly target to your location (intervene-style save). |
| Cauterizing Flame | Dispel / heal (talent) | — | Instant, 60s `[T1]` | Removes a Bleed/Poison/Curse/Disease and heals the target. A minute between uses is what makes this a chosen dispel, not a reflex one. |
| Expunge | Dispel (talent) | — | Instant, 8s `[T1]` | Removes a Poison effect from a friendly target. Effectively always available. |
| Quell | Interrupt | — | Instant / **20s** `[T1]` | Spell interrupt (kick) + short school lock. The APL fires it off-GCD on `target.debuff.casting.react`. |
| Sleep Walk | CC | — | ~1.5s cast, ~15s CD | Puts an enemy to sleep (incapacitate), broken by damage. Single-target CC. @verify-ingame |
| Oppressing Roar | CC (talent) | — | Instant, 120s `[T1]` | Roar that increases the duration of crowd-control on nearby enemies; AoE CC utility. |
| Landslide | CC (talent) | — | ~2s cast, 90s `[T1]` | Roots enemies in a line. (The cast time is still a Tier-3 figure — Augmentation's file calls it instant, so treat the `~2s` here as unsettled.) |
| Tail Swipe | CC | — | Instant, 180s `[T1]` | Knock-back / stagger the enemies behind you. **Class-baseline `[T1]`** — no talent point, but a 3-minute cooldown means it is a scripted answer, not a kiting tool. |
| Hover | Movement | — | Instant, ~35s CD (2 charges) | Lets you cast and channel while moving for its duration; not on the GCD. Central to Devastation mobility. @verify-ingame |
| Spatial Paradox | Major cooldown (utility, **choice node** `[T1]`) | — | Instant, 180s `[T1]` | External: grants you or an ally a large haste/empower burst (allows empowers to cast instantly). Choice-node vs *Time Spiral*. **3 minutes** — it will not pair with every Dragonrage, so decide which window gets it. |
| Source of Magic | Utility (mana) | — | Instant | Buffs a healer/ally, returning mana when you deal damage. Assign to a mana user. |
| Blessing of the Bronze | Utility (raid buff) | — | Instant / **15s** `[T1]` | Raid buff: movement-speed / snare component (the Evoker raid-wide buff). |
| Fury of the Aspects | Utility (Bloodlust) | — | Instant, 300s CD | Evoker's Bloodlust/Heroism-equivalent 30% haste raid cooldown (Exhaustion applies). |
| Time Spiral | Utility (**choice node** `[T1]`) | — | Instant, 120s `[T1]` | Lets you + nearby allies cast while moving briefly. Choice-node vs *Spatial Paradox* — and a full minute shorter than it, which is the real argument for taking it in movement-heavy fights. |
| Return | Utility (teleport) | — | Cast, ~long CD | Bronze teleport back to a stored location; out-of-combat travel utility. @verify-ingame |
| Swoop Up | Utility (PvP talent) | — | Instant / **90s** `[T1]` | **PvP talent** — grab an ally/enemy into the air. Not part of the PvE kit. @verify-ingame |
| Chrono Loop | CC (PvP talent) | — | Instant / **45s** `[T1]` | **PvP talent** — traps a target, returning them to their earlier position/health. Not part of the PvE kit. @verify-ingame |
| Time Stop | CC / utility (PvP talent) | — | Instant / **45s** `[T1]` | **PvP talent** (Preservation-flavored) — freezes a target in time. Not part of the Devastation PvE kit. @verify-ingame |

> Name-reconcile notes (Tier-1 game data, SpellName @ 12.0.7):
> - **Azure Sweep** (1265867) and **Mass Disintegrate** are Midnight-relevant spec/hero
>   additions confirmed in the live spell table. ⚠ Mass Disintegrate is **436335** —
>   the `talent-passive` row this spec's `ability-inventory.tsv` carries. 401642 is a
>   `SpellName` hit with no acquisition row for this spec and should not be restated.
> - **Sleep Walk** (360806) is the current name for the old "Sleep" CC.
> - **Swoop Up** (370388), **Chrono Loop** (383005), **Time Stop** are Evoker
>   **PvP talents** — the seed list carried them, but they are not PvE
>   rotational/utility buttons; flagged accordingly.

**Not acquirable at 12.0.7:** **Engulf** — there is no such Flameshaper button.
No spell named Engulf attaches to any trait node, `SkillLineAbility`
row, `SpecializationSpells` or `PvpTalent` at 12.0.7.67808, and no Midnight-range ID of that
name was ever minted. The **Flameshaper** subtree (37) *is* live on the Evoker tree (872) —
its actives are **Fire Torrent** (1265992) and **Consume Flame**. Do **not** file Fire Torrent
as a rename of Engulf; nothing measured says the two are the same button.
*[Tier 1: reconcile-ledger.md §4, DB2 @ 12.0.7.67808.]*

**Not on the Midnight Devastation tree:** **Firestorm** — it appears on no class, spec or
hero tree for any of the 40 specs — it is a War Within-era name with no Midnight
acquisition row, and Devastation has no "AoE-lean talent" of that name. The nearest live names are **Engulfing Blaze** (370837, spec
passive) and **Shattering Stars** (1265802, spec passive), neither of which is Firestorm.
*[Tier 1: `all-talents.tsv` @ 12.0.7.67808, all 40 specs.]*

## Changelog

2026-08-17 — Spatial Paradox is 180s (was 2 min); Mass Disintegrate is 436335 (401642 was wrong); Engulf and Firestorm rows removed as War Within-era carry-overs.

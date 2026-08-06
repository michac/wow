---
title: Havoc Demon Hunter — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/demon-hunter/havoc/ability-inventory.tsv  # tier 1, DB2 @ 12.0.7.67808 — names, spellIDs, origin, cooldowns
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1, simc midnight branch APL + default profile (Fel-Scarred), 2026-07-11
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1 game data, name canonicalization, 2026-07-11
confidence: high
---

# Havoc Demon Hunter — Ability Inventory (Midnight S1)

## Overview

Havoc is the melee-DPS Demon Hunter spec. Its resource is **Fury** (0–120+),
generated mostly passively (auto-attacks via **Demon Blades**, plus **Immolation
Aura** ticks) and spent on **Chaos Strike** (single-target) and **Blade Dance**
(AoE). The whole spec is built around the **demon-form (Demonic) window**:
casting **Eye Beam** briefly transforms you, and while transformed Chaos Strike
and Blade Dance are replaced by the stronger **Annihilation** and **Death Sweep**.
**Metamorphosis** is the big transform on a ~2-min cadence. High mobility
(Fel Rush, Vengeful Retreat, Felblade, The Hunt) is core to both damage and
positioning.

Two hero trees in S1:

- **Fel-Scarred** — the S1 default (the simc profile is `..._Fel-Scarred`).
  Adds **Demonsurge** (Eye Beam/Meta empower next Annihilation + Death Sweep) and,
  via **Demonic Intensity**, the empowered forms **Abyssal Gaze** (Eye Beam) and
  **Consuming Fire** (Immolation Aura). Frontloads burst inside Metamorphosis.
- **Aldrachi Reaver** — collect 6 soul fragments (via **Art of the Glaive**) to
  turn Throw Glaive into **Reaver's Glaive**, which applies **Reaver's Mark** and
  empowers the next Chaos Strike (**Rending Strike**) and Blade Dance
  (**Glaive Flurry** → **Fury of the Aldrachi** slashes). Strong funnel/cleave.

> Midnight note: a **third** Demon Hunter spec, **Devourer**, exists in 12.0.7
> game data (separate simc profile). This file is Havoc only.

## Inventory

> **Where the numbers come from.** `ability-inventory.tsv` in this folder is the
> Tier-1 record for **name, spellID, origin and cooldown** (DB2 @ 12.0.7.67808) —
> read it rather than trusting a number restated here. A `[T1]` stamp marks a
> cooldown taken from it; a `~` value is Tier-3 colour from simc / Icy Veins /
> method.gg. The remaining `@verify-ingame` markers all ask about **Fury cost**,
> which that file has no column for.
>
> **The demon-form buttons are invisible to Tier 1.** **Annihilation**,
> **Death Sweep**, **Abyssal Gaze**, **Consuming Fire** and **Reaver's Glaive**
> are runtime *overrides* of Chaos Strike / Blade Dance / Eye Beam / Immolation
> Aura / Throw Glaive. They attach to no acquisition table, so they appear in no
> generated inventory — that is a hole in the generator, not evidence they are
> gone. Each parent, and each hero subtree that grants the override, is live on
> tree 854. *[Tier 1: reconcile-ledger.md §4 + §5 G2 @ 12.0.7.67808.]*

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
| **Chaos Strike** | Rotational-spender | ~40 Fury | Instant | Core single-target spender; a crit refunds ~20 Fury. Replaced by Annihilation in demon form. @verify-ingame (exact Fury cost) |
| **Annihilation** | Rotational-spender | ~40 Fury | Instant | Demon-form (Metamorphosis/Demonic) version of Chaos Strike; higher damage. Consumes **Demonsurge** for Fel-Scarred. |
| **Blade Dance** | Rotational-spender (AoE) | ~35 Fury | Instant, 15s `[T1]` | Spin dealing AoE around you; triggers **Glaive Tempest** passive at 3+ targets. Replaced by Death Sweep in demon form. **Class-baseline `[T1]`.** The base cooldown is 15s, not the ~9s this file used to carry — the shorter number people quote is the *hasted* value, so treat 15s as the floor when planning AoE cadence. @verify-ingame (exact Fury cost) |
| **Death Sweep** | Rotational-spender (AoE) | ~35 Fury | Instant, shares Blade Dance's CD | Demon-form version of Blade Dance; higher damage. Consumes **Demonsurge** for Fel-Scarred. |
| **Eye Beam** | Rotational-builder / burst (talent) | ~30 Fury | ~2s channel, 30s `[T1]` | Channel that triggers the **Demonic** demon-form window; primary damage cooldown. **Chaotic Transformation** resets its CD on Meta; **Cycle of Hatred** lowers it. At a 30s base — not the ~40s previously written here — it comes back four times per Metamorphosis, so the Demonic window is the *frequent* one and Meta is what you plan around. @verify-ingame (exact Fury cost) |
| **Immolation Aura** | Rotational-builder | Free (generates Fury) | Instant, ~30s CD (2 charges w/ **A Fire Inside**) | AoE fire aura + steady Fury generation; **Ragefire** stores its damage to detonate. |
| **Felblade** | Movement / builder | Free (generates Fury) | Instant / **12s** `[T1]` | Gap-closer that generates Fury; used to trigger **Inertia** before burst windows. |
| **Demon's Bite** | Rotational-builder | Generates Fury | Instant | Baseline Fury builder — **replaced by the passive Demon Blades** in the S1 build, so rarely a manual press. |
| **Essence Break** | Rotational (burst amp) | Free | Instant, ~40s CD | Short window (~4s) that hugely amplifies Chaos Strike / Blade Dance damage; filled with Death Sweep + Annihilation. |
| **Metamorphosis** | Major cooldown | Free | Instant, ~2 min | Leap to target (stuns on land), transform: +Haste, empowers Chaos Strike/Blade Dance, and (w/ Chaotic Transformation) resets Eye Beam + Blade Dance. Core 2-min burst. |
| **The Hunt** | Major cooldown | Free | ~1.5s cast, ~90s CD | Charge dealing heavy nature damage + DoT; central burst button, reduced CD via **Eternal Hunt**. For Aldrachi Reaver, guarantees a Reaver's Glaive proc. |
| **Throw Glaive** | Rotational / ranged | Free (charges) | Instant, ~9s recharge | Ranged glaive throw; becomes a rotational button with **Soulscar** / **Furious Throws**. Turns into **Reaver's Glaive** for Aldrachi Reaver. |
| **Reaver's Glaive** | Rotational-spender enabler (AR) | Free | Instant | Aldrachi Reaver: replaces Throw Glaive after 6 soul fragments; applies **Reaver's Mark** and empowers the next Chaos Strike + Blade Dance. |
| **Abyssal Gaze** | Major cooldown (FS) | ~30 Fury | ~2s channel | Fel-Scarred **Demonic Intensity** empowered Eye Beam during Metamorphosis. |
| **Consuming Fire** | Rotational-builder (FS) | Free | Instant | Fel-Scarred **Demonic Intensity** empowered Immolation Aura during Metamorphosis. |
| **Demonsurge** | Passive/proc (FS) | — | — | Fel-Scarred proc from Eye Beam/Meta; makes the next Annihilation + Death Sweep hit harder (tracked as "demonsurge available"). |
| **Glaive Tempest** | Passive | — | — | S1 talent: Blade Dance/Death Sweep at 3+ targets releases spinning glaives for AoE (a passive, not a pressed button). |
| **Fel Rush** | Movement | Free (2 charges) | Instant, ~10s recharge | Dash forward dealing damage; mobility + an **Inertia** trigger / filler. |
| **Vengeful Retreat** | Movement | Free | Instant / **25s** `[T1]` | Backflip away, slows nearby enemies; procs **Initiative** / **Tactical Retreat**; woven before Eye Beam windows. |
| **Blur** | Defensive | Free | Instant, ~1 min CD | +50% dodge and −20% damage taken for a short time; core personal defensive. |
| **Darkness** | Defensive (raid) | Free | Instant, ~5 min CD | Ground AoE giving allies a chance to avoid incoming attacks; group cooldown. |
| **Disrupt** | Interrupt | Free | Instant, ~15s CD | Kick/interrupt a spellcast; the primary interrupt. |
| **Consume Magic** | Dispel (talent) | Free | Instant, 10s `[T1]` | Consumes a beneficial magic effect from the target (offensive dispel). At 10s it is effectively always available — treat it as a free purge on any enrage/absorb buff, not a saved cooldown. |
| **Chaos Nova** | CC (AoE stun) | ~Free | Instant, ~45s CD | Burst of fel energy stunning nearby enemies (~2s). |
| **Sigil of Misery** | CC (AoE) | Free | Instant, ~90s CD | Places a delayed sigil that causes enemies in its area to cower/disorient. |
| **Imprison** | CC | Free | Instant, ~45s CD | Incapacitates a target (Demon/Beast/Humanoid/Undead) for the duration. |
| **Torment** | Utility (taunt) | Free | Instant, ~8s CD | Taunts the target to attack you; single-target threat/utility. |
| **Spectral Sight** | Utility | Free | Instant, ~30s CD | See hidden/stealthed enemies and through obstacles; reduced movement speed while active. |
| **Rain from Above** | CC / utility (PvP talent) | Free | Instant / **90s** `[T1]` | PvP talent: lift into the air, immune to melee, rain glaives; not a PvE button. |
| **Illidan's Grasp** | CC (PvP talent) | Free | Channel / **60s** `[T1]` | PvP talent: seize a target, then throw or slam them. |
| **Reverse Magic** | Dispel (PvP talent) | Free | Instant, ~1 min CD | PvP talent: remove harmful magic from party/raid and send it back to enemies. |

**Not on the Midnight Havoc tree:** **Sigil of Spite** (390163) is a **Vengeance** spec
talent and appears on no Havoc tree — class, spec or hero. *[Tier 1: `all-talents.tsv`
@ 12.0.7.67808, all 40 specs.]*

**Not acquirable at 12.0.7:** **Fel Barrage** — deleted from this file. Twenty-one spells
carry the name in `SpellName`, and **none** of them attaches to a trait node, a
`SkillLineAbility` row, `SpecializationSpells` or `PvpTalent`; the live Demon Hunter tree
(854) has no Fel Barrage node and no Midnight-range ID was ever minted for it (highest is
400185, a War Within-era leftover). It is not an off-meta talent you could pick up — there
is no button. Do not re-add it from a guide that predates Midnight.
*[Tier 1: reconcile-ledger.md §4, DB2 @ 12.0.7.67808.]*

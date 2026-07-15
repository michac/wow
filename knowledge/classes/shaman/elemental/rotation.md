---
title: Elemental Shaman — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight profiles/MID1/MID1_Shaman_Elemental.simc   # tier 1, APL fetched 2026-07-11
  - https://www.method.gg/guides/elemental-shaman/playstyle-and-rotation   # tier 3, upd 2026-06-16
  - https://www.icy-veins.com/wow/elemental-shaman-pve-dps-rotation-cooldowns-abilities   # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/elemental-shaman-mythic-plus-guide   # tier 3, 12.0.7
confidence: high
---

# Elemental Shaman — Rotation (Midnight S1, 12.0.7)

Distilled from the **SimulationCraft default APL** (Tier 1,
`MID1_Shaman_Elemental.simc`) and corroborated against method.gg /
icy-veins 12.0.7 guides. The APL runs the **AoE** list at
`spell_targets.chain_lightning >= 3` and the **single-target** list
otherwise. Both builds (Stormbringer / Farseer) share one action list;
the branching is via talent conditions (`talent.master_of_the_elements`,
`talent.call_of_the_ancestors`, `buff.tempest`, etc.).

The spec's spine: **keep Flame Shock up → cast Lava Burst only on Lava
Surge → build Maelstrom with Lightning Bolt / Chain Lightning → dump it
with Earth Shock / Elemental Blast (ST) or Earthquake (AoE) → spend
Tempest procs (Stormbringer) → stack cooldowns into one window.** Mastery
(Elemental Overload) doubles casts for free, so the goal is cast volume
during the burst window, not overcapping Maelstrom.

## Pre-combat

- Maintain **Lightning Shield**; **Flametongue Weapon** and
  **Thunderstrike Ward** if talented.
- Buff the group with **Skyfury**.
- ~3s before pull: **Stormkeeper**. ~1.5s before pull:
  **Lava Burst** (lands right as the fight starts).

## Cooldown rules

- **Stormkeeper on cooldown**, but hold it to line up with **Ascendance**
  (the APL guards `stormkeeper` on `cooldown.ascendance.remains>10 |
  <gcd | fight_remains<20`) and to catch incoming AoE. On Stormbringer it
  has a shorter CD / stacks; on Farseer it also summons an ancestor.
- **Ascendance always right after Stormkeeper** (APL: cast when
  `cooldown.stormkeeper.remains>15`). Sync with **Heroism/Bloodlust**,
  on-use trinkets, and a potion. Don't open Ascendance into a movement
  phase — pair with **Spiritwalker's Grace** if you must move.
- **Ancestral Swiftness** (Farseer) on cooldown — the summoned ancestor
  is a big chunk of its value; follow the instant with a **cast-time**
  spell so its cooldown recovers optimally, not with instant Earth Shock.
- **Fire/Storm Elemental** on cooldown, folded into or near the burst
  window.
- **< 20s fight remaining**: the APL frees Stormkeeper and Ascendance to
  dump immediately regardless of pairing.

## Single-target priority

Following the Tier-1 APL `actions.single_target`:

1. **Ancestral Swiftness** (on cooldown).
2. **Flame Shock** if Master of the Elements is **not** up and it's
   refreshable (and Ascendance isn't imminent) — keep the DoT alive.
3. **Voltaic Blaze** (if talented) under the same "no MotE / refresh"
   condition — the instant Flame Shock applicator.
4. **Ascendance** (when Stormkeeper is >15s away — i.e. just after using
   Stormkeeper).
5. **Lava Burst** when Maelstrom deficit is healthy and you have a
   **Lava Surge** proc / Master of the Elements setup (never hardcast it
   just to fill).
6. **Tempest** when Master of the Elements is up (or you don't run MotE) —
   the Stormbringer proc spender.
7. **Lightning Bolt** if **Stormkeeper** is up (spend the empowered/instant
   charges) and MotE is up.
8. **Elemental Blast** (or **Earth Shock**), target the lowest
   **Lightning Rod** remaining — the Maelstrom dump.
9. **Tempest** (remaining charge, if not already spent above).
10. **Lightning Bolt** — the baseline filler / Maelstrom builder.
11. While moving: **Flame Shock → Voltaic Blaze → Frost Shock** (instants).

> **Power of the Maelstrom caps at 2** — cast a Lightning Bolt over Lava
> Burst at 2 stacks so you don't waste the next proc (method.gg).
> **Master of the Elements**: Lava Burst/Voltaic Blaze build the buff,
> then Tempest / Elemental Blast / empowered Lightning Bolt consume it —
> the APL's `buff.master_of_the_elements.up` gates are this loop.

## Cleave / AoE (3+ targets)

Following `actions.aoe`:

1. **Stormkeeper** (same Ascendance-pairing guard).
2. **Ancestral Swiftness**.
3. **Flame Shock** (only in the narrow MotE + Inferno Arc + exactly-3
   case) to keep a DoT rolling.
4. **Voltaic Blaze** — spreads Flame Shock to up to 5 targets; cast on
   cooldown in AoE.
5. **Ascendance**.
6. **Elemental Blast** (lowest Lightning Rod target) when Tempest < 2
   stacks and you have no Elemental Blast stat-buff yet.
7. **Earthquake** when Tempest < 2 stacks and target count is high enough
   — the primary AoE Maelstrom dump (soft-caps ~20 targets).
8. **Lava Burst** on **Purging Flames** + Lava Surge (and the Tempest/MotE
   3-target line).
9. **Tempest** (lowest Lightning Rod) when MotE is up, or to avoid
   overcapping at 2 stacks.
10. **Chain Lightning** under Stormkeeper (spends empowered charges) when
    Maelstrom has room.
11. **Earthquake** / **Elemental Blast** / **Tempest** / **Chain
    Lightning** as the sustained fillers.
12. While moving: **Flame Shock → Voltaic Blaze → Frost Shock**.

> Worth-it thresholds: **Chain Lightning over Lightning Bolt at ~3 targets
> (Stormbringer) / 2 (Farseer)**; **Stormkeeper is far stronger at 5+
> targets** (guaranteed overloads on Chain Lightning). With a priority
> target + Stormkeeper up, still spend the buff on **Lightning Bolt**.

## Hero-tree branches

- **Stormbringer (raid / low target count):** built around **Tempest** and
  **Lightning Rod**. Spend Maelstrom to charge Tempest, supercharge
  Lightning Bolt (2 stacks), keep Lightning Rod spread by Tempest/Elemental
  Blast for the burst multiplier. Stormkeeper has the shorter CD / stacks
  here.
- **Farseer (cleave / Mythic+):** **Call of the Ancestors** — Stormkeeper
  and **Ancestral Swiftness** summon ancestors that copy your casts, so the
  APL leans on those two on cooldown and adds the extra `chain_lightning`
  line at 2 targets (`talent.call_of_the_ancestors&spell_targets=2`).
  Best in 2–3 target cleave and dungeons.

## TODO

- [x] Single-target + AoE priority from Tier-1 simc APL (fetched 2026-07-11)
- [x] Cooldown pairing (Stormkeeper→Ascendance, Heroism sync) — APL + method
- [ ] Sanity-check opener against a top WCL Elemental log (`wowkb.wcl`)
- [ ] Confirm exact Maelstrom generation/spend numbers in-game
      (Swelling Maelstrom cap, Earth Shock/Earthquake cost) @verify-ingame

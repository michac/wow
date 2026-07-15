---
title: Havoc Demon Hunter — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1 APL, simc midnight branch (default = Fel-Scarred), 2026-07-11
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Havoc Demon Hunter — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1) with method.gg /
Icy Veins (Tier 3) for framing. The simc default profile is **Fel-Scarred**
(`talents=...Fel-Scarred`), but the single APL carries both hero trees'
lines (Aldrachi Reaver's `reavers_glaive` / `rending_strike` / `glaive_flurry`
and Fel-Scarred's `demonsurge` / `abyssal_gaze`). Fel-Scarred is the
recommended S1 pick for nearly all content; Aldrachi Reaver is the funnel/
cleave alternative (see `builds.md`).

**The core loop:** everything orbits the **demon-form window**. Eye Beam (and
Metamorphosis) put you in demon form; while transformed your Chaos Strike →
**Annihilation** and Blade Dance → **Death Sweep** hit far harder. The job is
to keep Eye Beam and Metamorphosis rolling, weave **Vengeful Retreat** (for
Initiative/Inertia) right before each Eye Beam, dump **Essence Break** windows
into Death Sweep + Annihilation, and never Fury-starve your spenders or let
Blade Dance / Immolation Aura charges cap.

## Pre-combat

- **Immolation Aura** ~1s before the pull (Fel-Scarred: spend **both** charges,
  2–3s out — `A Fire Inside`).
- Snapshot stats; pot on the pull (see cooldowns).

## Cooldown rules

- **Potion of Recklessness + on-use trinket** on the pull, then aligned to Eye
  Beam / Metamorphosis windows (the APL gates trinkets on `cooldown.eye_beam.up`
  and Meta being active). Don't bank a use past its cooldown.
- **Metamorphosis** every ~2 min, held to line up with an Eye Beam window
  (**Chaotic Transformation** resets Eye Beam + Blade Dance on cast) and **not**
  while a Demonsurge Annihilation/Death Sweep is still pending.
- **The Hunt** on cooldown, kept **out of** Essence Break windows and (with
  **Eternal Hunt**) synced so its cooldown reduction feeds the next Eye Beam.
  Fel-Scarred sends The Hunt + Meta before the next Eye Beam for trinket value.
- **Essence Break** is a ~4s amp window — open it with Fury banked (≥35) and
  immediately fill it with **Death Sweep** and **Annihilation** (Chaos Strike
  outside meta). Don't cast anything weak inside it.
- **Vengeful Retreat**: press it just before Eye Beam to proc **Initiative**
  (crit) / trigger **Inertia**; the APL cancels its movement when it's used to
  reposition into Metamorphosis.

## Single target (Fel-Scarred)

Opener (method.gg): Immolation Aura (pre-pull ×2) → pot+trinket → **Eye Beam**
→ **The Hunt** → **Felblade** (triggers Inertia) → **Death Sweep** ×2 →
**Annihilation** → **Vengeful Retreat + Metamorphosis** → Death Sweep →
Annihilation → **Consuming Fire** → Felblade (Inertia) → **Abyssal Gaze** →
Death Sweep ×2 → Annihilation.

Sustained priority:

1. **Felblade** when the **Inertia** trigger is up (Fel Rush as the backup
   consumer) — do this right before an Eye Beam / burst window.
2. **The Hunt** on cooldown (outside Essence Break).
3. **Death Sweep** (in demon form) / **Blade Dance** — on cooldown when it's
   worth pressing (see AoE thresholds; in ST it's still a spender when talented
   into First Blood).
4. **Immolation Aura** if sitting on 2 charges (don't cap).
5. **Vengeful Retreat** paired with **Eye Beam**.
6. **Eye Beam** on cooldown, aligned (`eb_aligned`) so you don't clip a Vengeful
   Retreat / Inertia window.
7. **Essence Break** inside/around the Meta window, then flood it with spenders.
8. **Metamorphosis** with Eye Beam (Chaotic Transformation reset).
9. **Annihilation once** to consume the **Demonsurge** proc, then Meta's
   Abyssal Gaze / Consuming Fire empowered casts.
10. **Annihilation / Chaos Strike** as the Fury dump (don't overcap Fury).
11. **Felblade** for Fury when low.
12. **Throw Glaive** only as a last-resort filler (or actively with Soulscar /
    Furious Throws talents).

## Cleave / AoE (3+)

Largely the single-target loop with these shifts (APL `use_blade_dance` triggers
at **3+ targets**, or 2+ with **Trail of Ruin**, or always with First Blood):

1. **Immolation Aura** early and kept rolling — it's a top AoE source with
   **Ragefire** / **A Fire Inside**; the APL fires extra Immolation Auras at
   `active_enemies>2`.
2. **Blade Dance / Death Sweep** become primary — they trigger the **Glaive
   Tempest** passive at 3+ targets. Keep them on cooldown.
3. **Eye Beam** — at 5+ targets its raw AoE outweighs alignment; the APL drops
   the `eb_aligned` gate at `active_enemies>=5` and just casts it.
4. **The Hunt** on cooldown (higher relative value in AoE).
5. **De-emphasize Chaos Strike / Annihilation** as single-target Fury dumps —
   spend into Blade Dance instead.
6. With **Burning Wound**, tab-target to spread the debuff (the APL's
   `retarget_auto_attack` keeps ~4 wounds up).
7. **Metamorphosis** + Essence Break as the AoE burst, same rules.

## Hero-tree branches

### Fel-Scarred (default)

- Each demon-form entry should spend the **Demonsurge** empowerment: two
  **Death Sweep** (via Eternal Hunt) and one **Annihilation** per window.
- **Demonic Intensity** during Meta gives the empowered **Abyssal Gaze**
  (Eye Beam) and **Consuming Fire** (Immolation Aura) — spend Immolation charges
  before Meta so Demonic Intensity refreshes them.
- **Inertia** (via Felblade / Fel Rush / Vengeful Retreat) is the amp to line up
  before every Eye Beam and burst window.

### Aldrachi Reaver

- Build 6 soul fragments (**Art of the Glaive**) → Throw Glaive becomes
  **Reaver's Glaive**. Cast it to apply **Reaver's Mark** on the priority target
  early, then spend the **Rending Strike** (empowered Chaos Strike/Annihilation)
  and **Glaive Flurry** (empowered Blade Dance/Death Sweep → **Fury of the
  Aldrachi** slashes) it grants.
- **The Hunt every ~min** guarantees a Reaver's Glaive proc.
- Funnel comes from **Wounded Quarry** repeat Death Sweeps into the Reaver's
  Mark target; in AoE, tab-target to keep **Burning Wound** spread.
- Priority (method.gg): Reaver's Glaive → Vengeful Retreat → The Hunt (if
  Reaver's Glaive unavailable) → Death Sweep → Eye Beam → Metamorphosis →
  Annihilation → Blade Dance → Chaos Strike → Immolation Aura → Felblade.

## TODO

- [x] ST + AoE priority from simc midnight APL (2026-07-11) + method.gg
- [x] Both hero-tree branches captured (Fel-Scarred default, Aldrachi Reaver)
- [ ] Sanity-check the opener against a top WCL Havoc log (`wowkb.wcl`)
- [ ] Re-distill if the simc midnight branch publishes a retuned 12.0.7 APL

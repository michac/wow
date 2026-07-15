---
title: Restoration Druid — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/restoration-druid/playstyle-and-rotation  # tier 3, 12.0.7 (upd 2026-06-16) — PRIMARY
  - https://www.icy-veins.com/wow/restoration-druid-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7 (upd 2026-06-15)
  - https://www.wowhead.com/guide/classes/druid/restoration/rotation-cooldowns-pve-healer  # tier 4, 12.0.7 (Voulk, 2026-06-12)
  - https://maxroll.gg/wow/class-guides/restoration-druid-mythic-plus-guide  # tier 3, 12.0.7
confidence: medium
---

# Restoration Druid — Rotation (Midnight Season 1)

> **No Tier-1 SimulationCraft APL exists for this spec** — SimC's `midnight`
> branch ships DPS/tank Druid profiles (Balance/Feral/Guardian) but **no
> healer profile** (`profiles/MID1/` has no `MID1_Druid_Restoration.simc`).
> So unlike a DPS spec, there is no authoritative priority string to cite;
> this page is distilled from **method.gg's Playstyle & Rotation (Tier 3,
> primary)** and corroborated against Icy Veins + Wowhead + Maxroll. Healing
> is reactive by nature — treat the lists below as *maintenance skeletons* you
> layer spot-healing on top of, not a fixed button loop. Confidence: **medium.**

Restoration doesn't "rotate" so much as **ramp and maintain**. The core loop
is: build a wide bed of Rejuvenations to power *Abundance*, keep Lifebloom +
Efflorescence + Wild Growth rolling, spend **Swiftmend on cooldown** to fire
*Soul of the Forest* / *Power of the Archdruid* / Grove Guardians, then convert
*Abundance* and *Clearcasting* into cheap Regrowth spot heals — spending a major
cooldown (Convoke / Tree of Life / Tranquility) into known damage windows.

## Pre-combat

- **Mark of the Wild** on the group.
- **Symbiotic Relationship** on the tank.
- Lay initial HoT coverage before pull: **Lifebloom** on tank, a few
  **Rejuvenations** on likely-damage targets, drop **Efflorescence** under
  the melee stack.

## Cooldown rules

- **Innervate** during the ramp / any expensive Efflorescence-heavy window —
  it makes the ramp free. Can be cast on a co-healer.
- **Incarnation: Tree of Life** (Keeper default) or **Convoke the Spirits**
  (choice-node; Wildstalker default) into scripted heavy-damage phases.
  *Cenarius' Guidance* drops Convoke to ~1 min, so it can be spent aggressively
  and proactively rather than saved.
- **Tranquility** for unavoidable raid-wide AoE / M+ AoE checks — in 12.0 it
  also applies **Flourish**, so casting it extends every active HoT.
- **Nature's Swiftness → Regrowth** and **Swiftmend → Regrowth** are the
  emergency single-target burst answers; keep them off cooldown as insurance.
- **Ironbark** on whoever is taking a targeted hit; **Barkskin** for yourself.
- Grove Guardians (Keeper): try to have Wild Growth / Swiftmend / Convoke
  spawn them **before** a damage window so the +5%-each (to +25%) healing buff
  is already up.

## Single-target / sustained maintenance

The maintenance skeleton (covers ~75% of a dungeon, per Icy Veins), highest
maintenance-priority first:

1. **Lifebloom** — keep it on the tank (and often self). Refresh only in the
   last ~4.5s so the bloom isn't wasted; stacks to 3 via *Everbloom*.
2. **Efflorescence** — keep the ground zone down under the stacked group;
   refresh when it expires (it's your cheapest AoE-per-mana once placed).
3. **Swiftmend on cooldown** → immediately follow the *Soul of the Forest*
   proc with **Rejuvenation** (or Wild Growth) to bank the empowered HoT and
   trigger *Power of the Archdruid* spread + Grove Guardians.
4. **Wild Growth** on cooldown whenever ≥2–3 allies are hurt.
5. **Rejuvenation** to widen the *Abundance* bed toward ~10–12 active.
6. **Regrowth** to spend: prefer **Clearcasting** procs and high *Abundance*
   stacks (near-guaranteed crit, cheap). This is your reactive spot heal.
7. Downtime: **Wrath / Moonfire / Sunfire** for *Master Shapeshifter* mana
   and chip DPS (do **not** cast at the expense of a needed heal).

## AoE / raid healing

1. **Pre-ramp** before the hit: blanket **Rejuvenation**, drop
   **Efflorescence**, keep **Lifebloom** rolling.
2. As damage lands: **Swiftmend** → **Wild Growth** (spawns Grove Guardians /
   Symbiotic Blooms) → **Regrowth** spam on the *Abundance*/Clearcasting
   economy.
3. **Major cooldown** into the peak — **Tranquility** for the biggest checks;
   **Convoke** / **Tree of Life** for sustained pressure.
4. **Flourish** (if talented over *Inner Peace*) right after a big HoT ramp to
   stretch every HoT through the damage; strongest when *Reforestation* /
   Dryad Tranquility procs are also out.
5. Keep **Efflorescence** positioned on the melee; use **Ironbark** /
   **Barkskin** / **Bear Form** to cover yourself and soak.

## Hero-tree branches

### Keeper of the Grove
- **Grove Guardians** are welded to **Swiftmend** and **Wild Growth** — using
  them on cooldown is now also your damage/healing-buff generator (+5% per
  guardian, to +25%).
- **Convoke** with Keeper can summon up to **5 Grove Guardians** at once — a
  +25% healing window; pair with Tree of Life form when possible.
- **Cenarius' Guidance** cuts Convoke's cooldown (fading guardians refund it),
  so the loop is Swiftmend/Wild-Growth-heavy and Convoke comes up ~every min.
- Lower APM, more forgiving — the reliable raid engine.

### Wildstalker (cat-weaving)
- **Symbiotic Blooms** applied by **Wild Growth / Regrowth / Efflorescence**
  amplify your *regular* healing; keep those three flowing to fuel *Vigorous
  Creepers* and *Bursting Growth*.
- When healing is under control, **weave damage**: apply **Moonfire/Sunfire**,
  auto-shift to **Cat Form** via *Fluid Form* (Rake/Shred), spread **Rake**,
  **Rip** → **Ferocious Bite** at 5 combo points; **Heart of the Wild** opens
  an empowered **Feral Frenzy** burst window; **Convoke** after the first
  Ferocious Bite for fast combo points.
- Higher personal DPS ceiling, higher APM. Healing still comes first — only
  weave when the group is topped.

## Notes / gaps

- Cooldown values for Swiftmend, Wild Growth, Ironbark, Barkskin, Incarnation,
  Stampeding Roar, and Heart of the Wild are drawn from Tier-3 guide tables,
  not a Tier-1 tooltip pull — see the `@verify-ingame` markers in
  `abilities.md`.
- Hero-tree raid-vs-M+ assignment is **contested across sources** — see
  `builds.md`. The mechanics above hold regardless of which content you run
  each tree in.

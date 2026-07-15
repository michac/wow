---
title: Destruction Warlock — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-14
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warlock_Destruction.simc  # tier 1, simc midnight APL, 2026-07-11
  - wago.tools DB2 SpellCooldowns, spell 1122 Summon Infernal  # tier 1, RecoveryTime 120000ms — corrects base CD to 120s (Inferno → 90s)
  - https://www.method.gg/guides/destruction-warlock/playstyle-and-rotation  # tier 3, upd. 2026-06-16, 2026-07-11
  - https://www.method.gg/guides/destruction-warlock  # tier 3, 2026-07-11
confidence: high
---

# Destruction Warlock — Rotation (Midnight S1)

Distilled from the **SimulationCraft midnight-branch APL** (tier 1) with
method.gg (tier 3) for colour. The APL branches by **hero tree** — `aoe_dia`
(Diabolist / Diabolic Ritual) and `aoe_hc` (Hellcaller / Wither) — and by enemy
count. Destruction is a **Soul Shard economy**: keep your fire DoT up, never
overcap shards, and pour shards into **Chaos Bolt** (single target) or **Rain of
Fire** (big AoE), timed around **Summon Infernal**.

> **12.0.7 "Revelations" (live 2026-06-16).** Both hero trees are viable:
> **Diabolist** is the default (best ST, competitive stacked cleave — it cycles
> Diabolic Ritual → Demonic Art → a free **Ruination**, so it presses Chaos Bolt
> even into moderate AoE). **Hellcaller** trades Immolate for **Wither** and adds
> the **Malevolence** burst CD; it is the sustained-AoE / long-fight pick. See
> `builds.md`.

## Pre-combat (opener)

APL precombat: `summon_pet` → set trinket-sync variables →
`grimoire_of_sacrifice` (if talented) → `snapshot_stats` → **Cataclysm** (if 2+
targets) → **Soul Fire** (pre-cast at ~4s on the pull timer) → Cataclysm →
Immolate (if 2+ & Roaring Blaze) → **Incinerate**.

- **Diabolist opener:** pre-cast Soul Fire → **Summon Infernal + trinket +
  potion + racial** → Conflagrate → resume.
- **Hellcaller opener:** pre-cast Soul Fire → Summon Infernal → Conflagrate →
  **Malevolence + trinket + potion + racial** → resume.
- No Soul Fire talented: open with 2× Incinerate into Immolate/Wither.

## Cooldown rules

- **Summon Infernal is the burst window** — everything syncs to it. Potion,
  racials (Berserking/Blood Fury/Fireblood/Ancestral Call), and external buffs
  (Power Infusion) fire *only* while the Infernal is active (`variable.infernal_active`),
  and trinkets are sync-scored to the **120s base (or 90s w/ Inferno)** Infernal cadence.
- **Malevolence (Hellcaller, 60s)** does **not** naturally align with Infernal
  (120s base, 90s w/ Inferno) — only line them up on the final casts of a fight; otherwise use
  Malevolence on cooldown and spend maximum shards inside its window.
- **Pool for adds:** if important adds are about to spawn, pool Soul Shards and
  delay Infernal/Malevolence to that point — a large gain over blind on-CD use.

## Single target — Diabolist (APL `default`)

1. **Soul Fire** if `soul_shard<=4` (fits without overcapping)
2. **Chaos Bolt** to spend a **Demonic Art** proc or restart Diabolic Ritual
   (`demonic_art` up, or ritual short, and target >20% HP)
3. **Conflagrate** to build if `soul_shard<=4.2` and no Backdraft stacked
4. **Summon Infernal**
5. **Incinerate** if **Chaotic Inferno** buff up and `soul_shard<=4.6`
6. **Shadowburn** with **Fiendish Cruelty** up / Conflagration of Chaos, or when
   **target ≤20%** (execute)
7. **Immolate** — refresh in the pandemic window (<30% duration / refreshable)
8. **Ruination** (free proc — press it)
9. **Cataclysm** if **Lake of Fire** talented
10. **Chaos Bolt** as the main shard dump (ritual length >4)
11. **Infernal Bolt** if `soul_shard<=3` (shard refill)
12. **Incinerate** (filler)

Method's shorthand: **Chaos Bolt (spend Demonic Art / restart ritual) →
maintain Immolate → Summon Infernal → Shadowburn (Fiendish Cruelty / anti-cap) →
Chaos Bolt (anti-cap) → Soul Fire (with Backdraft) → Conflagrate (don't sit on 2
charges) → Incinerate.**

## Single target — Hellcaller

1. Maintain **Wither** (re-apply in the pandemic window)
2. **Summon Infernal**
3. **Malevolence**, then maximize shard spenders inside the window
4. **Shadowburn** (Fiendish Cruelty, or anti-cap; the APL also gates on
   `soul_shard>=4` / Malevolence up / Infernal active / fight ending)
5. **Chaos Bolt** — spend when `soul_shard>=4`, or Malevolence up, or Infernal
   active, or fight_remains ≤15 (otherwise pool)
6. **Soul Fire** (with Backdraft)
7. **Conflagrate** (don't sit on 2 charges)
8. **Incinerate** (filler)

## Cleave (2 targets) — Havoc

- **Havoc** the second target; single-target casts (Chaos Bolt, Shadowburn, Soul
  Fire) are duplicated onto it. The APL `target_if` logic points Havoc at the
  add with the most time-to-die that isn't your current target, gated so it
  isn't wasted right before Summon Infernal (or Malevolence, Hellcaller).
- Otherwise run the single-target list; keep Immolate/Wither on both, and dump
  duplicated **Chaos Bolt** through the Havoc window.

## AoE (3+)

**Diabolist (`aoe_dia`):**
1. **Summon Infernal**
2. **Chaos Bolt** for Demonic Art / short ritual at `active_enemies<=4` (Diabolist
   keeps pressing Chaos Bolt into moderate AoE)
3. **Rain of Fire** at **4+ targets** when `soul_shard>=~3.5` or Alythess's Ire up
4. **Conflagrate** to refresh Immolate across targets (`target_if` most Immolate
   remaining)
5. **Shadowburn** on low-HP targets (Fiendish Cruelty / Conflagration of Chaos)
6. **Ruination**
7. **Cataclysm** (Lake of Fire, or when no adds incoming)
8. **Havoc** on the longest-living off-target
9. **Infernal Bolt** if `soul_shard<3`
10. **Chaos Bolt** at ≤3 targets with long ritual
11. **Soul Fire** (Avatar of Destruction extends the target cap to 10)
12. **Immolate** to spread (refreshable, ≤5 Immolates, no Cataclysm)
13. **Conflagrate** (Backdraft <2) → **Incinerate**

> Diabolist AoE note (method): **don't cast Rain of Fire until ~8+ targets** —
> Chaos Bolt stays more efficient for priority damage because it feeds Diabolic
> Ritual. Only true stacked AoE flips to Rain of Fire.

**Hellcaller (`aoe_hc`):**
1. **Summon Infernal** → **Malevolence**
2. **Rain of Fire** at `soul_shard>=~4` and **5+ targets** (−1 with Destructive
   Rapidity) — Rain of Fire is the Hellcaller spender much sooner than Diabolist
3. **Conflagrate** to refresh Wither across targets
4. **Shadowburn** (Fiendish Cruelty / Conflagration of Chaos)
5. **Cataclysm** (no adds incoming)
6. **Havoc** on the longest-living off-target
7. **Rain of Fire** (5+ targets) → **Chaos Bolt** (≤4 targets) → **Soul Fire**
8. **Wither** to spread → **Incinerate** (Fire and Brimstone + Backdraft) →
   **Conflagrate** → **Incinerate**

## Hero-tree summary

- **Diabolist** — Immolate DoT; Chaos Bolt-centric even into AoE via Diabolic
  Ritual → Demonic Art → **Ruination**; **Infernal Bolt** as the shard-refill
  builder. Rain of Fire only at very high target counts. Best single target.
- **Hellcaller** — **Wither** replaces Immolate; **Malevolence** is the extra
  ~60s burst CD; **Rain of Fire** comes online earlier as the AoE spender. The
  long-fight / sustained-AoE choice.

## TODO

- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once S1 logs settle.
- [ ] Re-distill if the simc midnight branch publishes a retuned 12.0.7 APL
      (this distill is off the current midnight-branch profile).

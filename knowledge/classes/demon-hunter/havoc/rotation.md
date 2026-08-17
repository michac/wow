---
title: Havoc Demon Hunter — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-17
reviewed: 2026-08-17
augments: simc-apl.md @5f916c6
sources:
  - knowledge/classes/demon-hunter/havoc/simc-apl.md  # tier 1, the generated 12.1 priority list this file explains
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — CLASSES ▶ DEMON HUNTER ▶ Havoc
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.1 page — read from the INTERACTIVE build tool (Fel-Scarred tab); the static HTML is a 24-item both-hero union the JS filters
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7 framing
confidence: medium
---

# Havoc Demon Hunter — Rotation (Midnight 12.1)

**The priority list is `simc-apl.md` in this folder. This file is why each rung sits
where it does, and what the sim does not model.** It does not restate the list; open
that file for the order and the exact conditions.

Everything orbits the **demon-form window**. Eye Beam and Metamorphosis put you in
demon form, where Chaos Strike becomes **Annihilation** and Blade Dance becomes
**Death Sweep** and both hit far harder. The job is to keep Eye Beam and Metamorphosis
rolling, press **Vengeful Retreat** on cooldown (it holds **Exergy** and refreshes
**Initiative**), open **Essence Break** away from Eye Beam and flood its short amp
window with Death Sweep + Annihilation, and — on an **A Fire Inside** build — never let
**Immolation Aura** sit at two charges. Fury is generated mostly by **Demon Blades** off your auto-attacks; max Fury
on a talented Havoc is **170**, not the 120 class base.

**Never equip a dagger.** Demon Hunters can equip daggers as of 12.1, but Demon
Blades, Blade Dance and Chaos Strike require Warglaives, Axes, Swords or Fist Weapons
— a dagger switches off your Fury generator, your AoE button and your Fury dump at
once. Death Sweep and Annihilation are the demon-form forms and go with them.

Open with **Immolation Aura** pre-pull, and pot + on-use trinket on the pull.

## Why each rung is there

- **Immolation Aura, the pre-Meta rung** (`immolation_aura`)
  — spend a charge in the last ~3 GCDs before Metamorphosis. Violent Transformation
  resets Immolation Aura when you transform, so a charge spent just before Meta costs
  nothing.
- **Metamorphosis** (`metamorphosis`) — with **Chaotic Transformation** it resets Eye
  Beam and Blade Dance, so it is held until both are genuinely spent; casting it while
  Blade Dance is still up throws the reset away. The two `demonsurge_available` terms
  stop you re-entering demon form with an empowered Death Sweep or Annihilation from
  the previous window unspent.
- **The Hunt** (`the_hunt`) — **Eternal Hunt makes The Hunt empower your next Eye
  Beam**, so the sync is to *Eye Beam*, not to Metamorphosis. Meta matters only as a
  scheduler, because Chaotic Transformation resets Eye Beam.
  - No Eternal Hunt → cast on cooldown.
  - Aldrachi Reaver → cast on cooldown; it guarantees a Reaver's Glaive proc.
  - Eye Beam less than 10s out **and** Meta more than 15s away → cast; spend the
    empower on that Eye Beam.
  - Eye Beam on cooldown **and Meta ready** → cast, then press Meta; the empower lands
    on the Eye Beam that Meta resets.
  - The gap those leave is the hold: **Meta within 15s but not yet ready** → hold, and
    release the moment Meta comes up.
- **Vengeful Retreat** (`vengeful_retreat`) — **pressed on cooldown**, weaved into the
  next Eye Beam. It is off the GCD, so it costs no press; it refreshes **Initiative**
  crit and triggers your mover talent. The APL never fires it merely because it is
  available — both of its branches require an alignment. Its `!buff.initiative.up`
  term is an anti-waste guard on that weave, **not** a prohibition: Initiative being up
  does not block the press.
- **Trinkets** (`use_items`)
  — one line, gated on Metamorphosis being **ready**, not active. There is no
  per-trinket special-casing in 12.1.
- **Immolation Aura at 2 charges** (`immolation_aura`)
  — this rung carries **no target condition**, so on a single target it outranks Death
  Sweep, Eye Beam, Essence Break, Blade Dance and every spender. A capped charge is
  unrecoverable; a delayed Eye Beam is not, so waste-avoidance beats a cooldown that is
  not decaying. **A Fire Inside** adds the second charge and cuts the recharge, which
  is what makes capping possible at all. ⚠ Inference, not Tier 1: the rung also
  requires **Burning Wound**, and the likely reason is that capping risks letting the
  debuff lapse — the APL states priority, not reasons.
- **Death Sweep inside Essence Break** (`death_sweep`)
  — the amp window is only a few seconds; the empowered spender is what fills it. Cast
  nothing weak inside it.
- **Eye Beam** (`eye_beam`) — unconditional. There is no alignment gate and no target
  gate on it in 12.1.
- **Felblade on Inertia** (`felblade`) — Vengeful Retreat
  and The Hunt arm the Inertia amp and Felblade cashes it. On an **Exergy** build the
  buff never exists and this line is inert.
- **Essence Break** (`essence_break`) — cast when Eye
  Beam is more than 4s from ready. Opening the amp window while Eye Beam is about to
  come up clips it. Its initial hit is a real chunk of the ability in 12.1, so the
  press matters as much as the window.
- **Blade Dance / Death Sweep as the baseline spender** — unconditional. The
  `use_blade_dance` variable that used to gate them on target count was deleted in
  12.1.
- **Immolation Aura, the AoE rung** (`immolation_aura`) — sits
  far below the 2-charge rung, and `active_enemies>1` is the **only** target-count
  term in the entire 25-line priority.
- **The tail** — the unconditional spender-and-generator floor, plus one Fel-Scarred
  Felblade rung that fires below a Fury threshold. **Fel Rush and Throw Glaive are no
  longer in the damage priority at all** — that is a real 12.1 change, not an
  omission. Demon's Bite is absent because **Demon Blades** replaces it with a passive.

## What the sim doesn't model

- **Burning Wound's spread.** Your auto-attacks apply it — the tooltip reads *"Demon's
  Bite and Throw Glaive leave open wounds"*, and under Demon Blades the Demon's Bite
  effect arrives through auto-attacks — so **switching target is what moves the
  wound**. 12.1's APL dropped the `retarget_auto_attack` line that used to model this,
  and the `tab_target_burning_wound` variable it declares in precombat is never read by
  any combat line. Simc no longer models the spread; that is not the same as the spread
  ceasing to matter. Tab-target in AoE.
- **Movement and positioning.** Vengeful Retreat moves you backwards and Fel Rush
  forwards; the sim assumes you are always in melee. Every retreat costs some
  auto-attacks, which the priority list is silent about.
- **Target swaps.** Serrated Glaive is a buff on you in 12.1 rather than a debuff on
  the target, so it survives a swap — but Burning Wound, Reaver's Mark and Essence
  Break do not, and the APL is written against a single stable target set.
- **Reaction time and perfect information.** The sim knows exactly when a proc lands
  and when the fight ends; `fight_remains` gates have no human equivalent. Treat the
  end-of-fight trinket and potion lines as "burn it if the pull is nearly over".

## Talent gates that change the priority

- **Chaotic Transformation** — without it, Metamorphosis' entire hold is vacuous and
  Meta is pressed on cooldown. With it, Meta holds while Blade Dance is ready or Eye
  Beam is 8s or less from ready.
- **A Fire Inside + Burning Wound** — both are required for Immolation Aura's high
  rung. Without A Fire Inside there is one charge on a long recharge and the rung
  vanishes entirely.
- **Eternal Hunt** — without it, The Hunt is cast on cooldown with no sync at all.
- **Hero tree** — `hero_tree.felscarred` gates the Felblade-at-Fury-≤100 line. Aldrachi
  Reaver casts The Hunt on cooldown.
- **Mover choice node** — **Exergy** (+5% for 20s, applied directly by The Hunt and
  Vengeful Retreat, no follow-up needed) is the Season 2 recommendation; **Inertia**
  (+12% for 6s, cashed by a Fel Rush or Felblade after a retreat) remains a live
  alternative and is what the `inertia_trigger` rung exists for. ⚠ Tier-3 consensus,
  unsimmed — Season 2 opens 2026-08-18.
- **Dancing with Fate** is the sanctioned fallback for a player who does not want to
  weave movers precisely: a flat passive on Blade Dance's final slash that asks nothing
  of timing.

## Hero-tree branches

### Fel-Scarred

Each demon-form entry should spend its **Demonsurge** empowerments — the
`demonsurge_available` terms on Metamorphosis, Death Sweep and Annihilation exist to
enforce that. **Demonic Intensity** during Meta upgrades Eye Beam to **Abyssal Gaze**
and Immolation Aura to **Consuming Fire**.

### Aldrachi Reaver

Build soul fragments with **Art of the Glaive** until Throw Glaive becomes **Reaver's
Glaive**; casting it applies **Reaver's Mark** and grants **Rending Strike** (an
empowered Chaos Strike / Annihilation) and **Glaive Flurry** (an empowered Blade Dance
/ Death Sweep, which fires **Fury of the Aldrachi** slashes). The APL's `reavers_glaive`
and `rending_strike` rungs exist to spend those two before they expire. The Hunt is
cast on cooldown here because it guarantees the next Reaver's Glaive. Funnel damage
comes from **Wounded Quarry** repeat Death Sweeps into the Reaver's Mark target.

## Changelog

2026-08-17 — rewritten as a supplement to the generated `simc-apl.md`; the transcribed
priority lists, the 12.1 delta table and the 12.0.7 log measurements moved to
`_meta/changelog-12.1.md` and `_meta/kb-inbox.md`. Ten claims were wrong against the
12.1 APL, notably The Hunt's hold (it syncs to Eye Beam, not Metamorphosis), Essence
Break's non-existent Fury gate, Immolation Aura's rung being single-target too, and
Fel Rush having left the damage priority.

2026-08-17 — Icy Veins carries one hero-filtered priority tool, not an
Aldrachi-Reaver-led list; earlier drafts transcribed the static page's 24-item
both-hero union.

2026-08-12 — Exergy is the Season 2 mover pick over Inertia, and Vengeful Retreat is a
press-on-cooldown button in either build.

---
title: Feral Druid — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Druid_Feral.simc  # tier 1 simc APL + talent string, 2026-07-11
  - https://www.method.gg/guides/feral-druid/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/feral-druid-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1 name canonicalization, 2026-07-11
confidence: high
---

# Feral Druid — abilities (Midnight S1)

## Overview

Feral is a melee bleed/combo-point DPS spec. **Resource system:** two
resources at once — **Energy** (0–100, regenerates passively; builders cost
it) and **Combo Points** (0–5, up to 8 during Berserk via Overflowing Power;
builders generate them, finishers spend them). The loop is builder→spender:
generate combo points with **Shred / Rake / Swipe**, then spend 5 CP on
**Rip / Ferocious Bite / Primal Wrath**. The spec lives and dies by **bleed
uptime** (Rake + Rip) and by **snapshotting** — a bleed applied while
**Tiger's Fury** is active is locked in at the buffed damage for its whole
duration, so DoTs are refreshed inside cooldown windows.

**Hero trees (Midnight):**
- **Wildstalker** — DoT-centric; Rake/Rip ticks grow **Bloodseeker Vines**
  that add bleed damage and amplify finishers. Best single-target / raid.
- **Druid of the Claw** — auto-attacks and Berserk build **Ravage** procs
  (a cone-AoE empowered Ferocious Bite via **Claw Rampage**); stronger
  cleave/AoE and defensives. Preferred in Mythic+.

> **Midnight-new / renamed (flagged):** **Ravage** (Druid of the Claw
> empowered Bite), **Chomp** (new builder/finisher, choice node vs Lunar
> Inspiration), **Unseen Predator** (new spec-tree capstone — a Tiger's Fury
> proc buff that amplifies finishers / Rip), **Panther's Guile** (proc that
> grants extra Ferocious Bites mid-builder), **Frantic Frenzy / Focused
> Frenzy** (Feral Frenzy choice node), **Hunger for Battle** (between-pull
> energy sustain). **Brutal Slash** and **Thrash** were removed from the
> Feral kit this patch (per method.gg 12.0.7). @verify-ingame

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Cat Form | Utility (form) | — | Instant | The DPS form; enables all Feral combat abilities and Energy/CP. |
| Prowl | Utility (stealth) | — | Instant | Stealth; enables opener (Rake from stealth hits harder / Sudden Ambush). |
| Shred | Rotational-builder | 40 Energy | Instant | Primary single-target CP builder; bonus damage/crit from stealth or Sudden Ambush. |
| Rake | Rotational-builder | 35 Energy | Instant | CP builder that applies a bleed; maintain on all targets. Snapshots Tiger's Fury. |
| Swipe | Rotational-builder (AoE) | 35 Energy | Instant | AoE CP builder hitting all nearby enemies; primary builder above the Rake target cap. |
| Rip | Rotational-spender | 5 CP (20 Energy) | Instant | Single-target finisher bleed; core sustained damage. Snapshots Tiger's Fury; keep up 100%. |
| Ferocious Bite | Rotational-spender | 25 + up to 25 Energy | Instant | Direct-damage finisher; consumes up to 50 Energy total for extra damage. Extends Rip (Sabertooth). |
| Primal Wrath | Rotational-spender (AoE) | 5 CP (20 Energy) | Instant | AoE finisher that applies/refreshes Rip on all targets in range. |
| Maim | CC / finisher | 5 CP (30 Energy) | Instant | Finisher that stuns the target; damage scales with CP. |
| Tiger's Fury | Major cooldown | — (grants 50 Energy) | 30s CD | Instant Energy + all Feral damage +15% for ~10s; **snapshots bleeds**. Core rhythm CD. |
| Feral Frenzy | Major cooldown / builder | 25 Energy | 45s CD | 5-hit frontal bleed; generates 5 CP and a strong bleed. Sync to Tiger's Fury. |
| Berserk | Major cooldown | — | 3 min (2 min talented) | ~15s window: +damage, reduced costs, 1 CP/1.5s, up to 8 CP (Overflowing Power). |
| Incarnation: Avatar of Ashamane | Major cooldown | — | 3 min | Choice-node alternative to Convoke; a stronger, longer Berserk (Cat Form incarnation). |
| Convoke the Spirits | Major cooldown | — | 2 min (1 min w/ Ashamane's Guidance) | Channels ~16 free Druid spells over ~4s; huge burst. Always under Berserk + Tiger's Fury. |
| Ravage | Rotational-spender (proc, AoE) | 5 CP | Proc | Druid of the Claw: empowered cone-AoE Ferocious Bite from Claw Rampage/auto-attack procs. @verify-ingame |
| Chomp | Rotational-builder/finisher | Energy | — | Midnight-new; choice-node builder/finisher (buffed by Tear Down the Mighty). Off-meta pick. @verify-ingame |
| Moonfire | Rotational-builder (DoT) | 30 Energy | Instant | Via **Lunar Inspiration** talent: a ranged Arcane DoT that also builds a CP; a third bleed layer. |
| Unseen Predator | Passive/proc (spec capstone) | — | Proc | Midnight-new spec capstone; Tiger's Fury grants a buff that amplifies finishers / +Rip damage. @verify-ingame |
| Skull Bash | Interrupt | — | 15s CD | Charges and interrupts a spellcast (from Cat/Bear). The Feral kick. |
| Barkskin | Defensive | — | 1 min CD | −20% damage taken for 12s; usable in any form, incl. while stunned. |
| Survival Instincts | Defensive | — | 3 min CD, 2 charges | −50% damage taken for ~6s; the big personal cooldown. |
| Frenzied Regeneration | Defensive (heal) | — | Bear Form, ~36s CD, 2 charges | Bear-Form self-heal over 3s scaling with recent damage taken. |
| Bear Form | Defensive (form) | — | Instant | Tank form; +armor/stamina, enables Frenzied Regeneration / Ironfur for emergencies. |
| Regrowth | Utility (heal) | Mana | 1.5s cast (instant w/ proc) | Direct + HoT heal; Wildstalker gets instant/free Regrowths (Symbiotic Bloom). |
| Renewal | Defensive (heal) | — | ~1.5 min CD | Instantly heals a chunk of max health (class talent). @verify-ingame |
| Stampeding Roar | Movement (raid utility) | — | 2 min CD | +60% movement speed to nearby allies for 8s; also shifts them to a run-capable form. |
| Dash | Movement | — | Cat Form, ~1.5 min CD | Instant burst of movement speed in Cat Form. |
| Wild Charge / Tiger Dash | Movement | — | Choice, ~15–45s CD | Form-dependent gap-closer (Wild Charge) or a speed burst (Tiger Dash), choice node. |
| Skull Bash | Interrupt | — | 15s CD | (Listed above.) The interrupt. |
| Mighty Bash / Incapacitating Roar | CC | — | Choice, 50s / 30s CD | Single-target stun (Mighty Bash) or AoE incapacitate (Incapacitating Roar), choice node. |
| Typhoon | CC (knockback) | — | ~30s CD | Cone knockback + daze; class-tree pick. |
| Mass Entanglement / Ursol's Vortex | CC | — | Choice, ~30s CD | AoE root (Mass Entanglement) or pull-in vortex (Ursol's Vortex), choice node. |
| Entangling Roots | CC (root) | Mana | 1.7s cast | Single-target root. |
| Hibernate | CC | Mana | 1.5s cast | Sleeps a Beast or Dragonkin. |
| Cyclone | CC | Mana | 1.7s cast | Banishes a target (immune, can't act) — choice vs Soothe. |
| Soothe | Dispel (offensive) | Mana | Instant | Removes an Enrage from an enemy — choice vs Cyclone. |
| Remove Corruption | Dispel | Mana | Instant | Removes Curse + Poison from a friendly target. |
| Rebirth | Utility (combat res) | Mana | 2s cast | Battle resurrection of a dead ally in combat. |
| Revive | Utility (res) | Mana | ~2s cast | Out-of-combat resurrection. |
| Innervate | Utility (mana) | — | 3 min CD | Grants an ally free spellcasting for 8s (support healers/casters). |
| Heart of the Wild | Major cooldown (hybrid) | — | ~5 min CD | Empowers off-spec casting for 45s; Feral use is minor burst/utility. |
| Mark of the Wild | Utility (buff) | Mana | Instant | Raid-wide Versatility buff. |
| Symbiotic Relationship | Utility (link) | — | Instant, long CD | Links you to an ally, sharing healing/leech (Midnight talent). |
| Travel Form | Movement (form) | — | Instant | Faster travel form (auto-adapts to terrain/flight). |
| Moonkin Form | Utility (form) | — | Instant | Caster form (via class tree), for off-spec Starfire/Starsurge lines. |
| Ironfur | Defensive | — | Bear Form, Rage | Bear armor buff for emergency mitigation via Bear Form. |
| Regrowth / Rejuvenation / Wild Growth | Utility (heal) | Mana | Instant/cast | Off-spec heals available via the class tree; emergency/solo healing. |

> CD and Energy/CP values are the standard Feral values; several were not
> pulled from a Tier-1 tooltip dump this pass and carry @verify-ingame where
> Midnight may have retuned them. Bleed snapshotting and the builder/spender
> economy are corroborated across the simc APL and both guides.

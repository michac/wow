---
title: Fire Mage — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Mage_Fire.simc  # tier 1 APL (Sunfury default + Frostfire lists), WoW 12.0.x
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Fire.simc  # tier 1
  - https://www.method.gg/guides/fire-mage/playstyle-and-rotation  # tier 3, 12.0.7
  - https://www.method.gg/guides/fire-mage  # tier 3, 12.0.7, upd. 2026-06-16
  - https://www.wowhead.com/guide/classes/mage/fire/rotation-cooldowns-pve-dps  # tier 4, Midnight (corroboration)
confidence: high
---

# Fire Mage — Rotation (Sunfury, Midnight S1)

Distilled from the SimulationCraft default APL (tier 1) — the profile is
`MID1_Mage_Fire_Sunfury`, and the APL carries both **Sunfury** (`sf_*`) and
**Frostfire** (`ff_*`) action lists. Sunfury is the S1 build everywhere (see
`builds.md`); the Sunfury lists are distilled below with Frostfire deltas noted.

The engine is the **Hot Streak loop**: cast a fire spell → it crits → **Heating
Up** → convert it to **Hot Streak** with **Fire Blast** (guaranteed crit, off the
GCD, so you fire it *mid-cast*) → spend Hot Streak on an instant **Pyroblast**
(single target) or **Flamestrike** (AoE). The textbook single-target beat is
**Fireball → (Fire Blast mid-cast) → instant Pyroblast on the Fireball's
landing**, so both crits and the Pyro Ignite deposit land together. Everything
else is Combustion timing.

## Pre-combat

- **Arcane Intellect** (group buff), **Mirror Image**, **snapshot**.
- Precast a spender/opener: **Pyroblast** (Sunfury), or **Frostfire Bolt**
  (Frostfire), or **Meteor** if talented Sunfury Execution without Firestarter.
- Chip the target with **Fire Blast → Pyroblast** Hot Streaks until it's at
  ~90–91% HP so Combustion / Firestarter open cleanly.

## Cooldown rules

- **Combustion on cooldown** (~1-min CD via Kindling; ~10s window, extended by
  Fired Up). Only delay for a fight damage-amp phase or a planned big M+ pull.
  With **Firestarter**, the APL delays the pull Combustion ~18s (until the boss
  is <90% HP) so Firestarter's free crits aren't wasted.
- **Bank Fire Blast** starting when Combustion is ~12s out — enter the window
  with **3 charges** (2 acceptable). During the window, alternate
  **Fire Blast → spender → Fire Blast → spender** and empty all charges before it
  ends.
- **Potion + Bloodlust/Time Warp + racials + steroid trinkets** all sync to
  Combustion (`buff.combustion.remains>6`). Sunfury+Firestarter delays the pull
  potion ~8s. Non-"steroid" trinkets are used off-cooldown, outside Combustion.
- **Meteor** is timed to land *inside* Combustion (or, with Burnout, late in the
  window to bank the biggest Ignite for the Burnout AoE when Combustion drops).

## Single target (Sunfury)

Filler priority when Combustion is **down** (`sf_filler`):

1. **Meteor** — in AoE/setup, as a Combustion pre-cast (ST: fire it to land in
   the upcoming window per the cooldown rule above).
2. **Pyroblast** on **Hot Streak** — spend it (hold only if Combustion is <~5s
   away, or bank a Pyroclasm stack that will survive to Combustion; spend
   immediately at **2 Pyroclasm stacks**).
3. **Pyroblast** on **Pyroclasm** (hardcast) when 2 stacks / no risk of losing it.
4. **Scorch** — in **execute** (<30%, with Scald) or on a **Heat Shimmer** proc.
5. **Fireball** — the default hardcast filler (generates Heating Up).
6. **Fire Blast** (the `fireblast` sub-list) — off-GCD, woven *into* the above:
   press it **mid-cast** the instant you have Heating Up and no Hot Streak
   (never overcap charges; keep ~1 in reserve outside the banking window).

During **Combustion / Hyperthermia** (`sf_combustion`): every cast crits, so the
loop tightens to **Fire Blast (convert) → instant Pyroblast**, weaving hardcast
**Scorch/Fireball** only to bridge Fire Blast charges. Spend Fire Blast whenever
you have Heating Up and no Hot Streak; still convert during **Hyperthermia** even
though its casts auto-crit, because Hot Streak Pyroblast applies far more Ignite.

## Cleave / AoE (4+ targets)

Same proc loop, but the **spender flips to Flamestrike**:

1. **Meteor** on cooldown (with Blast Zone) / into Combustion.
2. **Flamestrike** on **Hot Streak** at **≥4 targets** (`fuel_the_fire` gates the
   count; the APL's `flamestriking` variable). Below the threshold, Pyroblast.
3. **Flamestrike** on **Pyroclasm** for the AoE burst (Sun King's Blessing is now
   folded into Pyroclasm and empowers hardcast Flamestrike).
4. **Scorch** on Heat Shimmer / in execute.
5. **Fireball** filler → **Fire Blast** woven in (don't Fire Blast during a
   hardcast Flamestrike unless it won't clip it).
6. **Combustion**: convert Heating Up with Fire Blast and dump **Flamestrike**
   Hot Streaks; **Burnout** turns the leftover Ignite into an AoE detonation when
   Combustion expires.

## Hero-tree branches

- **Sunfury (S1 default):** the lists above. Spellfire Spheres generate
  **Meteorites** (buffed to 20% proc), **Arcane Phoenix** grants a Haste buff on
  expiry and feeds Fire Blast CDR; Sunfury Execution / Blast Zone shape Meteor
  timing. Pyroclasm is the AoE-burst enabler.
- **Frostfire (`ff_*` lists — undertuned in S1):** **Frostfire Bolt** replaces
  Fireball as the filler; Combustion entry keys off Fireball/Meteor/Pyroblast
  executing (the `ff_combustion` gate). In **execute**, Frostfire *ignores* Hot
  Streak Pyroblast and instead dumps Fire Blast freely (`target.health.pct<30`).
  Meteor is timed late in Combustion for Burnout. Play only if you specifically
  want it (see `builds.md`).

## End of fight

- `fight_remains<1`: dump **all** remaining Fire Blast charges.
- Trinkets/racials fire if `fight_remains<20` even outside a Combustion window.

## TODO

- [x] Single-target + AoE priority — from simc midnight `MID1_Mage_Fire.simc` APL
- [x] Combustion / cooldown / trinket sync rules — from APL `cds` + `sf_combustion`
- [x] Hero-tree split (Sunfury default, Frostfire deltas) — from APL `ff_*`/`sf_*`
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Confirm exact Combustion duration / Fire Blast charge count in-game

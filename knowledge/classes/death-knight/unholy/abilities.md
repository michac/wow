---
title: Unholy Death Knight — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/death-knight/unholy/ability-inventory.tsv  # tier 1, DB2 @ 12.0.7.67808 — names, spellIDs, origin, cooldowns
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Unholy.simc  # tier 1 APL + talent hash, 2026-07-11
  - https://wago.tools/db2 SpellName @ 12.0.7.67808 (raw/wago/SpellName.csv)  # tier 1 name canonicalization, 2026-07-11
  - https://www.method.gg/guides/unholy-death-knight/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 (upd. 2026-07-08), 2026-07-11
confidence: high
---

# Unholy Death Knight — Abilities (Midnight S1)

## Overview

**Hero trees (S1):** **Rider of the Apocalypse** (the simc default and Method's
raid/single-target pick) and **San'layn** (the sustained-cleave / Essence-of-the-
Blood-Queen alternative). See `builds.md`.

**Resource system:** two resources — **Runes** (6, each recharging on a
Haste-scaled ~10s timer) and **Runic Power**. Rune-spenders (Festering Strike,
Scourge Strike) generate Runic Power; Runic-Power spenders (Death Coil, Epidemic)
proc **Runic Corruption** to recharge Runes faster, so the two feed each other in
a loop.

**Midnight rework — read this before the table.** Unholy was reworked for
Midnight around a minion loop:
- **Festering Wounds are gone.** Festering Strike now applies **Lesser Ghoul**
  stacks (game data confirms `Lesser Ghoul`, not `Festering Wound`, as the live
  maintenance mechanic); Scourge Strike consumes them.
- **Putrefy** is a new core rotational button that summons and sacrifices a
  Lesser Ghoul to strike the target and explode for AoE. It runs on charges.
- **Dread Plague** is a new pure single-target disease; **Virulent Plague** is
  the multi-target disease. Both are applied by **Outbreak** (and spread
  passively via Superstrain / Scourge Strike).
- **Death Coil** is the baseline RP spender. The apex talent **Forbidden
  Knowledge** transforms it (and Epidemic) into **Necrotic Coil** for 30s after
  Army of the Dead. Both `Death Coil` and `Necrotic Coil` are distinct live
  spells in game data.
- Removed since The War Within: **Apocalypse** (standalone), **Vile Contagion**,
  **Unholy Assault**, **Defile**, and the seed name **"Zombify"** — none appear
  in the 12.0.7 spec tree (`talents.md`); "Zombify" is not a live spell name.
  `Apocalypse Now` survives only as a Rider hero capstone.

## Ability inventory

> **Where the numbers come from.** `ability-inventory.tsv` in this folder is the
> Tier-1 record for **name, spellID, origin and cooldown** (DB2 @ 12.0.7.67808) —
> read it rather than trusting a number restated here. A `[T1]` stamp marks a
> cooldown taken from it; a `~` value is Tier-3 colour, and the rows still marked
> `@verify-ingame` are the ones asking about resource cost or charge recharge,
> which no Tier-1 column in that file can answer.

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
| Festering Strike | Rotational-builder | 2 Runes | Instant | Strikes for physical damage and applies **Lesser Ghoul** stacks (the maintenance resource). Generates Runic Power. |
| Scourge Strike | Rotational-builder | 1 Rune | Instant | Shadow/physical strike that **consumes a Lesser Ghoul** stack for a burst; applies Virulent Plague to unaffected targets (Superstrain). *Clawing Shadows* talent converts it to ranged shadow damage. |
| Outbreak | Rotational-builder (disease apply) | 1 Rune | Instant, no CD | Applies **Dread Plague** (single-target) / **Virulent Plague** (spreads to nearby) diseases. Refresh only when a plague is missing. |
| Death Coil | Rotational-spender | ~30 Runic Power | Instant | Primary RP spender at ≤2 targets. **Sudden Doom** procs make it free and boost it. Becomes **Necrotic Coil** during Forbidden Knowledge windows. @verify-ingame (exact RP cost) |
| Epidemic | Rotational-spender (AoE) | ~30 Runic Power | Instant | RP spender at 3+ targets — hits every enemy afflicted by Virulent Plague. Replaces Death Coil in AoE. @verify-ingame (exact RP cost) |
| Putrefy | Rotational-spender / summon | Charges (2 max) | Instant, charge recharge | Summons and sacrifices a **Lesser Ghoul** to strike the target then explode for AoE. Press on cooldown; concentrate charges inside Dark Transformation. *Cycle of Death* makes it reduce Death and Decay's CD. @verify-ingame (rune cost / recharge time) |
| Dark Transformation | Major cooldown (pet) | — | Instant / ~45s | Transforms your ghoul for 15s: +200% Ghoul damage and its Claw cleaves (Sweeping Claws). Enables **Commander of the Dead** and a free Soul Reaper (Reaping). Core damage cooldown. |
| Army of the Dead | Major cooldown (summon, talent) | — | Instant / 90s `[T1]` | Summons a ghoul army for ~15s. Triggers **Forbidden Knowledge** (Death Coil → Necrotic Coil for 30s) and, with Commander of the Dead, buffs your minions. At 90s it lines up 2:1 against Dark Transformation, so the Forbidden Knowledge window is every *other* Dark Transformation, not every one. |
| Raise Abomination | Major cooldown (summon) | — | Instant / ~90s | Choice-node replacement for Army of the Dead: summons an Abomination that increases damage enemies take from your minions. @verify-ingame (CD) |
| Summon Gargoyle | Major cooldown (summon) | — | Instant / CD | Choice-node alternative to Raise Abomination: a Gargoyle that casts empowered bolts for its duration. |
| Soul Reaper | Rotational-spender (execute) | 1 Rune | Instant / **15s** `[T1]` | Strikes and marks the target; if it dies or is below 35% HP after 5s, detonates for heavy damage. **Reaping / Dark Transformation** grant free casts; used as a burst button, not only in execute range. |
| Death and Decay | Rotational-AoE / utility | 1 Rune | Instant / ~30s | Ground AoE; primary AoE-tool button when *Desecrate*/*Cycle of Death* is talented (mainly for cooldown reduction, not raw damage). Empowers strikes standing in it. |
| Raise Dead | Pet | — | Instant / **120s** `[T1]` | Summons your permanent **Ghoul** (Unholy's core pet — kept out at all times). |
| Vampiric Strike | Rotational (San'layn hero) | replaces Scourge Strike | Instant (proc) | San'layn: replaces some Scourge Strikes, builds **Essence of the Blood Queen** stacks for sustained passive damage and healing. |
| Gift of the San'layn | Major cooldown (San'layn hero) | — | window | San'layn burst window layered onto Dark Transformation / cooldown stacking. |
| Rider's Champion | Passive (Rider hero) | — | — | Passively summons the Four Horsemen (Trollbane, Whitemane, Nazgrim, Mograine) during combat for extra damage/utility. |
| Apocalypse Now | Major cooldown (Rider hero capstone) | — | CD | Summons all four Horsemen at once for a burst window. |
| Death Strike | Defensive / heal | ~35 Runic Power | Instant | Strikes and self-heals based on recent damage taken — the spec's main active self-heal. @verify-ingame (RP cost) |
| Death Pact | Defensive | — | Instant / ~2 min | Heals for a large % of max HP; you take increased damage briefly after. Talent. |
| Icebound Fortitude | Defensive | — | Instant / **120s** `[T1]` | −30% damage taken and stun immunity for a short duration. |
| Anti-Magic Shell | Defensive | generates RP | Instant / ~1 min | Absorbs magic damage and generates Runic Power from absorbed hits. |
| Anti-Magic Zone | Defensive (group) | — | Instant / **240s** `[T1]` | Ground zone reducing magic damage for the party/raid. Talent. |
| Lichborne | Defensive / anti-CC | — | Instant / **120s** `[T1]` | Turn Undead: immune to Charm/Fear/Sleep; lets Death Coil heal you. |
| Death Grip | Utility / CC | — | Instant / ~25s | Grips the target to you (taunts in a tanking context); primary ranged pull. |
| Death's Advance | Movement | — | passive + active | Passive movement-speed floor plus an active sprint; snare resistance. |
| Wraith Walk | Movement | — | Instant / **60s** `[T1]` | Channelled +movement speed with snare immunity (choice vs March of Darkness). |
| Path of Frost | Utility | — | Instant | Water-walking / fall-damage utility. |
| Chains of Ice | CC (slow) | 1 Rune | Instant | Heavy slow on the target; applies Frost debuffs (Proliferating Chill etc.). |
| Mind Freeze | Interrupt | — | Instant / 15s | Melee-range spell interrupt + brief school lockout. |
| Asphyxiate | CC (stun) | — | Instant / **45s** `[T1]` | Stuns the target (choice vs Death's Reach). Talent. |
| Blinding Sleet | CC (AoE disorient) | — | Instant / **60s** `[T1]` | Disorients enemies in front of you. Talent. |
| Dark Command | Utility (taunt) | — | Instant / ~8s | Forces the target to attack you (PvE taunt / threat tool). |
| Dark Simulacrum | Utility (**PvP talent**) | — | Instant / 20s `[T1]` | Places a rune that copies the next enemy spell for you to cast back. It lives in the **PvP talent** pool, so it is not selectable in raid or Mythic+. |
| Control Undead | Utility / CC | — | Cast / CD | Enslaves an undead target as a temporary pet. Talent. |
| Raise Ally | Utility (combat rez) | — | Cast / **600s** `[T1]` | Battle-resurrects a dead ally. |
| Magus of the Dead | Passive (summon) | — | — | Talent: your cooldowns/Putrefy summon a spellcasting Magus that assists (Menacing Magus adds cleave). |
| Sudden Doom | Passive (proc) | — | — | Random chance to make the next Death Coil / Epidemic free and empowered. |
| Commander of the Dead | Passive | — | — | Dark Transformation (near Army/Raise Abomination) buffs the damage of your undead minions. |
| Forbidden Knowledge | Passive → transform | — | — | Apex talent: Army of the Dead transforms Death Coil → **Necrotic Coil** (and empowers Epidemic) for 30s and raises the target-count breakpoints. |

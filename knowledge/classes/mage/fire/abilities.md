---
title: Fire Mage — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Mage_Fire.simc  # tier 1 APL + talent string, WoW 12.0.x
  - https://www.method.gg/guides/fire-mage  # tier 3, 12.0.7, upd. 2026-06-16 (intro / removed abilities)
  - https://www.method.gg/guides/fire-mage/playstyle-and-rotation  # tier 3, 12.0.7
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Fire.simc  # tier 1
  - https://www.wowhead.com/spell=1257349/fired-up  # tier 4, Fired Up apex proc
confidence: high
---

# Fire Mage — Abilities (Midnight S1)

## Overview

Fire is a **crit-and-proc burst caster**. The whole spec is a loop around two
buffs: **Heating Up** (gained when a direct-damage fire spell crits) and
**Hot Streak** (a second crit — or a **Fire Blast**, which is a guaranteed crit
off the GCD — upgrades Heating Up into Hot Streak, making the next **Pyroblast**
or **Flamestrike** instant and guaranteed-crit). Mastery is **Ignite**, a rolling
burn that pools crit damage on the target. Damage is heavily front-loaded into
the **Combustion** window (guarantees crits, so every spell feeds Hot Streak),
which Kindling reduces to a ~1-minute cooldown.

- **Resource:** Mana (rarely a constraint) drives casts; the *rotational* economy
  is **Fire Blast charges** (the Hot Streak converter) plus the Heating Up / Hot
  Streak proc chain. During Combustion/**Hyperthermia** every cast crits, so Fire
  Blast is spent purely to convert Heating Up.
- **Hero trees:** **Sunfury** (recommended everywhere S1 — Spellfire Spheres +
  Arcane Phoenix drive extra Meteorites, Haste, and Fire Blast CDR) and
  **Frostfire** (Frostfire Bolt replaces Fireball; undertuned in S1). See
  `builds.md`.
- **Midnight removals (were baseline/rotational in prior expansions):**
  **Phoenix Flames removed** (its Fire Blast-refund role is now covered by the
  **Fired Up** apex proc), **Shifting Power removed**, and **Sun King's Blessing
  folded into Pyroclasm**. Do not author these as live buttons.

> Seed-list note: the seed listed **Prismatic Barrier** — that is *Arcane's*
> baseline barrier. Fire's absorb is **Blazing Barrier** (class-tree, from the
> talents.md), which is what appears below.

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Fireball** | Rotational-builder | Mana | ~2.25s cast | Primary single-target filler; crits grant **Heating Up**. Everything is cast to chase Fireball crits. |
| **Frostfire Bolt** | Rotational-builder | Mana | ~2.25s cast | **Frostfire** hero-tree filler that *replaces* Fireball (deals Fire+Frost, feeds both schools). Talent; not used on the Sunfury build. |
| **Fire Blast** | Rotational-builder (proc converter) | ~2 charges, off-GCD | Instant · ~12s recharge/charge | **Guaranteed crit, off the GCD.** Converts **Heating Up → Hot Streak** — the single most-pressed button. Bank 2–3 charges before Combustion. Flame On adds a charge + faster recharge. @verify-ingame (exact charges/recharge) |
| **Pyroblast** | Rotational-spender | Mana | 3.5s cast · instant w/ **Hot Streak** | Single-target Hot Streak spender; the big Ignite deposit. Hardcast only when forced (e.g. Pyroclasm). |
| **Scorch** | Rotational-builder / execute filler | Mana | 1.5s cast (castable while moving) | Movement filler and **execute** (empowered/guaranteed-crit under ~30% via Scald). **Heat Shimmer** proc makes it hit harder / instant. |
| **Flamestrike** | Rotational-spender (AoE) | Mana | ~4s cast · instant w/ **Hot Streak** | Ground-targeted **AoE** Hot Streak spender (4+ targets). Replaces Pyroblast as the spender in AoE. |
| **Meteor** | Major cooldown / AoE burst | Mana | Instant cast · ~45s CD | Ground-targeted burst + a burning DoT; **synced into Combustion**. Talent. @verify-ingame (CD) |
| **Combustion** | Major cooldown | Mana | Instant · ~1 min CD (Kindling) | Guarantees critical strikes for ~10s (extended by **Fired Up** during the window). The burst window — use on cooldown. |
| **Fired Up** | Passive (apex proc) | — | — | Consuming Hot Streak has a chance (much higher during Combustion) to grant **Fired Up**: +fire damage stacking buff **and −Fire Blast CD**; extends Combustion by 1s while it's up. Covers the removed Phoenix Flames refund. (talents.md flags row-11 as ACTIVE — @verify-ingame whether there is a pressable component.) |
| **Arcane Explosion** | Rotational (off-spec AoE) | Mana | Instant | Baseline point-blank AoE; rarely used by Fire (Flamestrike is the AoE spender). |
| **Counterspell** | Interrupt | Mana | Instant · 24s CD | Kick + 4s school lock. |
| **Blazing Barrier** | Defensive (absorb) | Mana | Instant · ~25s CD | Fire's damage-absorb shield; knocks back / burns melee attackers. Pre-cast before damage. |
| **Ice Block** | Defensive (immunity) | Mana | Instant · 4 min CD | Full immunity + clears magic; **Ice Cold** talent turns it into a big damage-reduction "cheat" and **Cauterize** links to it. Last-resort. |
| **Cauterize** | Defensive (passive cheat-death) | — | Passive · ~1 min ICD | Fatal blow instead leaves you at low HP with a burning heal-over-time; talent. |
| **Alter Time** | Defensive / utility | Mana | Instant · ~1 min CD | Snapshots HP/position; re-press within the window to rewind to it. Panic-button + positional reset. |
| **Mirror Image** | Defensive / utility | Mana | Instant · 2 min CD | Summons 3 decoys, threat drop + damage reduction; also a small DPS/pre-pull cooldown. |
| **Blink** / **Shimmer** | Movement | Mana | Instant · 15s CD (Shimmer 2 charges, off-GCD, castable while casting) | Short teleport. **Shimmer** (choice) is the DPS/mobility pick — off-GCD, usable mid-cast. |
| **Frost Nova** | CC (root) | Mana | Instant · ~25s CD | PBAoE root; kiting + Combustion setup. |
| **Cone of Cold** | CC / AoE | Mana | Instant · ~12s CD | Frontal slow + minor damage. |
| **Dragon's Breath** / **Supernova** | CC | Mana | Instant · ~45s / ~25s CD | Choice node: **Dragon's Breath** frontal disorient (also fire damage); **Supernova** knock-up/AoE. |
| **Polymorph** | CC | Mana | 1.7s cast | Single-target sheep; the mage crowd-control staple. |
| **Mass Polymorph** | CC (AoE) | Mana | Cast · CD | Sheeps multiple targets; choice node vs Ring of Frost. |
| **Spellsteal** | Utility (offensive dispel) | Mana | 1.5s cast | Steals a beneficial magic buff off an enemy. |
| **Remove Curse** | Dispel | Mana | Instant · 8s CD | Removes a Curse from a friendly target. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Cast | Group Intellect buff; cast once, pre-pull. |
| **Time Warp** | Major cooldown (Bloodlust) | Mana | Instant · 5 min CD | Group +30% Haste (Bloodlust effect). |
| **Blazing Barrier / Blink / etc. movement & utility** | — | — | — | (see rows above) |
| **Slow Fall** | Utility | Mana / reagent | Instant | Slow-fall on a friendly target. |
| **Invisibility** / **Greater Invisibility** / **Mass Invisibility** | Utility / defensive | Mana | Instant · long CD | Threat drop / escape (Greater = self, big DR; Mass = whole group). |
| **Mass Barrier** | REMOVED in Midnight | — | — | Not a live button (per method.gg). |

> Cast times/cooldowns are baseline values (haste and talents shorten many);
> the load-bearing detail for button priority is the **Function** column and the
> Fireball → Fire Blast → Pyroblast proc loop, not the exact seconds. Entries
> marked @verify-ingame carry the least certainty on their numeric CD.

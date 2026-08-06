---
title: Fire Mage — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/mage/fire/ability-inventory.tsv  # tier 1 — wago DB2 pinned @ build 12.0.7.67808; the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file, 2026-08-06
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

> **Tier-1 floor.** `ability-inventory.tsv` in this folder — generated from wago DB2
> pinned to build `12.0.7.67808` — is authoritative for **name, spellID, origin and
> cooldown**, and wins wherever it and the prose below disagree. Cooldowns tagged
> `[T1]` were read off it this pass; a `~` value is prose that has **not** been
> measured. Note the tsv's `cooldown` column returns the **GCD** for charge-based
> abilities (Fire Blast reads `0.5`), so it cannot answer Fire Blast's recharge. This
> table is for **function, role and rotational context**.

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
| **Fireball** | Rotational-builder | Mana | ~2.25s cast | Primary single-target filler; crits grant **Heating Up**. Everything is cast to chase Fireball crits. |
| **Frostfire Bolt** | Rotational-builder | Mana | ~2.25s cast | **Frostfire** hero-tree filler that *replaces* Fireball (deals Fire+Frost, feeds both schools). Talent; not used on the Sunfury build. |
| **Fire Blast** | Rotational-builder (proc converter) | ~2 charges, off-GCD | Instant · ~12s recharge/charge | **Guaranteed crit, off the GCD.** Converts **Heating Up → Hot Streak** — the single most-pressed button. Bank 2–3 charges before Combustion. Flame On adds a charge + faster recharge. @verify-ingame (exact charges/recharge) |
| **Pyroblast** | Rotational-spender | Mana | 3.5s cast · instant w/ **Hot Streak** | Single-target Hot Streak spender; the big Ignite deposit. Hardcast only when forced (e.g. Pyroclasm). |
| **Scorch** | Rotational-builder / execute filler | Mana | 1.5s cast (castable while moving) | Movement filler and **execute** (empowered/guaranteed-crit under ~30% via Scald). **Heat Shimmer** proc makes it hit harder / instant. |
| **Flamestrike** | Rotational-spender (AoE) | Mana | ~4s cast · instant w/ **Hot Streak** | Ground-targeted **AoE** Hot Streak spender (4+ targets). Replaces Pyroblast as the spender in AoE. |
| **Meteor** | Major cooldown / AoE burst | Mana | Instant cast · 45s [T1] | Ground-targeted burst + a burning DoT; **synced into Combustion**. Talent. At 45s it comes back inside every Kindling-shortened Combustion, so it is a paired button, not an independent one. |
| **Combustion** | Major cooldown | Mana | Instant / **120s** `[T1]` (Kindling) | Guarantees critical strikes for ~10s (extended by **Fired Up** during the window). The burst window — use on cooldown. |
| **Fired Up** | Passive (apex proc) | — | — | Consuming Hot Streak has a chance (much higher during Combustion) to grant **Fired Up**: +fire damage stacking buff **and −Fire Blast CD**; extends Combustion by 1s while it's up. Covers the removed Phoenix Flames refund. (talents.md flags row-11 as ACTIVE — @verify-ingame whether there is a pressable component.) |
| **Arcane Explosion** | Rotational (off-spec AoE) | Mana | Instant | Baseline point-blank AoE; rarely used by Fire (Flamestrike is the AoE spender). |
| **Counterspell** | Interrupt | Mana | Instant / **25s** `[T1]` | Kick + 4s school lock. |
| **Blazing Barrier** | Defensive (absorb) | Mana | Instant · 30s [T1] | Fire's entry of the shared class barrier node; damage-absorb shield that knocks back / burns melee attackers. Pre-cast before damage. |
| **Ice Block** | Defensive (immunity) | Mana | Instant · 4 min CD | Full immunity + clears magic; **Ice Cold** talent turns it into a big damage-reduction "cheat" and **Cauterize** links to it. Last-resort. |
| **Cauterize** | Defensive (passive cheat-death) | — | Passive · ~1 min ICD | Fatal blow instead leaves you at low HP with a burning heal-over-time; talent. |
| **Alter Time** | Defensive / utility | Mana | Instant · ~1 min CD | Snapshots HP/position; re-press within the window to rewind to it. Panic-button + positional reset. |
| **Mirror Image** | Defensive / utility | Mana | Instant · 2 min CD | Summons 3 decoys, threat drop + damage reduction; also a small DPS/pre-pull cooldown. |
| **Blink** / **Shimmer** | Movement | Mana | Instant · 15s CD (Shimmer 2 charges, off-GCD, castable while casting) | Short teleport. **Shimmer** (choice) is the DPS/mobility pick — off-GCD, usable mid-cast. |
| **Frost Nova** | CC (root) | Mana | Instant · ~25s CD | PBAoE root; kiting + Combustion setup. |
| **Cone of Cold** | CC / AoE | Mana | Instant · 25s [T1] | Frontal slow + minor damage. Class-baseline. Roughly double the cooldown the older prose claimed — not an AoE filler you can lean on. |
| **Dragon's Breath** / **Supernova** | CC | Mana | Instant · ~45s / ~25s CD | Choice node: **Dragon's Breath** frontal disorient (also fire damage); **Supernova** knock-up/AoE. |
| **Polymorph** | CC | Mana | 1.7s cast | Single-target sheep; the mage crowd-control staple. |
| **Mass Polymorph** | CC (AoE) | Mana | Cast / **60s** `[T1]` | Sheeps multiple targets; choice node vs Ring of Frost. |
| **Spellsteal** | Utility (offensive dispel) | Mana | 1.5s cast | Steals a beneficial magic buff off an enemy. |
| **Remove Curse** | Dispel | Mana | Instant · 8s CD | Removes a Curse from a friendly target. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Cast | Group Intellect buff; cast once, pre-pull. |
| **Time Warp** | Major cooldown (Bloodlust) | Mana | Instant · 5 min CD | Group +30% Haste (Bloodlust effect). |
| **Blazing Barrier / Blink / etc. movement & utility** | — | — | — | (see rows above) |
| **Slow Fall** | Utility | Mana / reagent | Instant | Slow-fall on a friendly target. |
| **Invisibility** / **Greater Invisibility** / **Mass Invisibility** | Utility / defensive | Mana | Instant · long CD | Threat drop / escape (Greater = self, big DR; Mass = whole group). |

> Cast times/cooldowns are baseline values (haste and talents shorten many);
> the load-bearing detail for button priority is the **Function** column and the
> Fireball → Fire Blast → Pyroblast proc loop, not the exact seconds. Entries
> marked `@verify-ingame` carry the least certainty on their numeric CD.

### Not on the Midnight Fire tree

- **Mass Barrier** — not acquirable at 12.0.7, and the row is deleted rather than kept as
  a tombstone. Spell 414660 attaches to no trait node, SkillLineAbility,
  SpecializationSpells or PvpTalent entry. (It survives as a Cooldown-Manager set entry,
  which is why it can still surface in `mage/frost`'s inventory as `cdm-only` — a
  CooldownSet row is *not* an acquisition row and does not mean a spec can cast it.)
  Fire's only barrier is **Blazing Barrier**.
  *[Tier 1: DB2 @ 12.0.7.67808, `_abilities/reconcile-ledger.md`.]*

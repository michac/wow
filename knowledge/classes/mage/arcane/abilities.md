---
title: Arcane Mage — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/mage/arcane/ability-inventory.tsv  # tier 1 — wago DB2 pinned @ build 12.0.7.67808; the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file, 2026-08-06
  - simc midnight branch profiles/MID1/MID1_Mage_Arcane.simc  # tier 1 APL, action/spell names
  - https://www.method.gg/guides/arcane-mage  # tier 3, upd. 2026-06-29 (12.0.7)
  - https://www.method.gg/guides/arcane-mage/playstyle-and-rotation  # tier 3, upd. 2026-06-29
  - https://www.icy-veins.com/wow/arcane-mage-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - raw/wago/SpellName.csv  # tier 1, spell-name canonicalization
confidence: high
---

# Arcane Mage — Abilities (Midnight Season 1)

## Overview

- **Hero trees:** **Spellslinger** (gateway talent *Splintering Sorcery*) and
  **Sunfury** (gateway *Spellfire Spheres*). Both are viable in S1; the APL
  branches on which you pick (see `rotation.md` / `builds.md`).
- **Resource system:** **Mana** plus **Arcane Charges** (0→4). Each Arcane
  Charge amplifies Arcane Blast / Arcane Barrage damage and raises their mana
  cost. **Arcane Blast** builds charges; **Arcane Barrage** spends *all* charges
  (resets to 0) for a burst scaled by how much you've built up.
- **The Midnight core loop is buff-stacking, not charge-cycling.** The central
  resource is now the **Arcane Salvo** stacking buff (fed by Arcane Missiles
  waves, or Arcane Orb with *Orb Mastery*). You stack Salvo toward the 20-stack
  (25 for Sunfury) threshold, then dump an empowered **Arcane Barrage** during a
  burst window built from **Arcane Surge + Touch of the Magi**. **Clearcasting**
  (free Arcane Missiles / Orb) drives the stacking.
- **Midnight removed *Nether Precision*** — the old Arcane Missiles → Arcane
  Blast empowerment mechanic is gone; base Arcane Missiles damage was raised to
  compensate. Do not treat Nether Precision as a live buff. @verify-ingame

## Inventory

> **Tier-1 floor.** `ability-inventory.tsv` in this folder — generated from wago DB2
> pinned to build `12.0.7.67808` — is authoritative for **name, spellID, origin and
> cooldown**, and wins wherever it and the prose below disagree. Cooldowns tagged
> `[T1]` were read off it this pass; a `~` value is prose that has **not** been
> measured. This table is for **function, role and rotational context** — read it for
> judgement, read the tsv for numbers.

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
| **Arcane Blast** | Rotational-builder | Mana | ~2.25s cast (haste) | Primary builder / filler. Generates an **Arcane Charge** (to 4), raising its own damage & mana cost. Main Clearcasting-fishing button. |
| **Arcane Barrage** | Rotational-spender | Mana | Instant | Core spender. Consumes **all Arcane Charges** (resets to 0); damage scales hard with current **Arcane Salvo** stacks. Dumped at the 20/25-stack threshold and during the Touch of the Magi window. |
| **Arcane Missiles** | Rotational-builder | Mana (free w/ Clearcasting) | ~2.2s channel | Channels a burst of waves; each wave grants **Arcane Salvo** stacks (and Arcane Charges). Cast on **Clearcasting** procs. *Orb Mastery* builds make it obsolete (Orb replaces it). |
| **Arcane Orb** | Rotational-builder | Mana (free w/ Clearcasting) | Instant, charge-based CD | Fires an orb through enemies dealing AoE and granting Arcane Charges + Salvo. Spellslinger/Orb-Mastery main builder; a Clearcasting Orb fires **three** orbs. @verify-ingame |
| **Arcane Pulse** | Rotational-builder (AoE) | Mana | Instant | Talent. AoE nova used on 3+ targets (`pulse_aoe_count`); can build Arcane Charges when talented (*Expanded Mind*). @verify-ingame |
| **Arcane Explosion** | Rotational-builder (AoE) | Mana | Instant | Baseline PBAoE; niche filler at 4+ targets on Sunfury when not talented into *Impetus*. |
| **Touch of the Magi** | Major cooldown | — | Off-GCD, 45s CD | Applies a debuff that accumulates **20% of damage dealt**, then detonates (~12s). Grants **4 Arcane Charges** on cast. The "Miniburn"; on Sunfury delayed so it carries into the Arcane Soul window. |
| **Arcane Surge** | Major cooldown | Drains all Mana | ~2s cast, 90s CD | Empowered nuke that **drains all current mana** for damage, then grants **~35% spell damage for ~15s** (and regenerates mana over the window). The "Big Burn," paired with Touch of the Magi. |
| **Touch of the Archmage** | Major cooldown | — | Active, spec capstone | Capstone active (spec row 11). Follow-up strike tied to the Touch of the Magi burst. @verify-ingame |
| **Evocation** | Utility (mana) | — | Channel, ~90s CD | Now an **optional talent** (choice vs *Mana Adept*) that only **restores mana**; APL uses it under ~10% mana outside burst. |
| **Presence of Mind** | Utility / burst enabler | — | Off-GCD, 45s [T1] | Makes the next **2 Arcane Blasts instant**. Choice-node vs *Slipstream*. Used to squeeze instant builders into movement / burst — at 45s it lines up roughly every other Touch of the Magi. |
| **Supernova** | CC / burst | Mana | 45s [T1] | Choice-node vs *Dragon's Breath*. AoE that knocks enemies up and deals Arcane damage. Nearly twice the cooldown the older prose claimed — treat it as a planned peel, not a spammable one. |
| **Mirror Image** | Defensive / Utility | — | ~120s CD | Summons 3 images that taunt-free absorb aggro and add damage; threat drop + defensive. Pre-pulled in the APL precombat. |
| **Alter Time** | Defensive / Movement | — | 60s [T1] (re-press window ~10s) | Snapshots position & health; re-press within the window to return to both — an escape / effective heal. The 60s is the *cooldown*; the short timer people quote is the re-press window, which is a different thing and the reason this row used to read as a 10s ability. |
| **Prismatic Barrier** | Defensive | Mana | 30s CD (25s talented) | Absorb shield (the strongest Mage barrier); most spammable defensive, reduces magic damage. |
| **Ice Block** | Defensive | — | 180s CD (150s talented) | Full immunity; cancels your own casting. *Ice Cold* variant instead gives ~70% DR while still able to cast. |
| **Blink** | Movement | — | ~15s CD | Teleport ~20yd forward, breaks roots. *Shimmer* replaces it with a **2-charge** off-GCD blink; *Improved Blink* is the alt choice. |
| **Counterspell** | Interrupt | — | **25s** `[T1]` | Interrupts + locks the target's school for a few seconds. |
| **Frost Nova** | CC | — | ~25s CD (2 charges w/ talent) | Roots nearby enemies in place; kiting / peel tool. **Class-baseline** — the talent adds only the second charge, so every Arcane build has the root. |
| **Cone of Cold** | CC / AoE | Mana | 25s [T1] | Frontal cone dealing Frost damage and slowing. Class-baseline. Roughly double the cooldown the older prose claimed — not an AoE filler you can lean on. |
| **Polymorph** | CC | Mana | 1.5s cast | Long single-target sheep (Beast); breaks on damage, regenerates the target. |
| **Mass Polymorph** | CC | Mana | Cast / **60s** `[T1]` | Talent. AoE Polymorph — sheeps multiple enemies at once. |
| **Slow Fall** | Utility | Reagent-free | Instant | Levitate/slow-fall on a friendly target. |
| **Spellsteal** | Dispel / Utility | Mana | Instant | Steals a beneficial magic effect from an enemy onto yourself. |
| **Remove Curse** | Dispel | — | Instant | Removes a Curse from a friendly target. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Instant | Raid-wide **Intellect** buff; precombat maintenance cast. |
| **Time Warp** | Major cooldown (raid) | — | 300s CD | Raid **30% Haste for 40s** (Bloodlust equivalent; personal Temporal Displacement lockout). |
| **Greater Invisibility** | Defensive / Utility | — | ~90s CD, 2 charges | Instant invisibility + strong damage reduction while fading; a hard-reset defensive and threat drop. |
| **Mass Invisibility** | Utility | — | **300s** `[T1]` | Turns the whole party/raid invisible — skip/reset trash. |
| **Ice Cold** | Defensive | — | (replaces Ice Block) | Talent: Ice Block becomes ~70% DR you can act through instead of a full stop. |

> Utility/defensive cast times and cooldowns are standard Mage values reconciled
> against the 12.0.7 talent tree (`talents.md`); rows marked `@verify-ingame`
> carry small uncertainty on exact CD/charges and should be confirmed live.

**Not on the Midnight Arcane tree:** **Ice Barrier**. The class barrier node resolves to
one spell per spec — Arcane **Prismatic Barrier** (235450, listed above), Fire **Blazing
Barrier**, Frost **Ice Barrier** — so Arcane cannot take the Frost entry.
*[Tier 1: `all-talents.tsv` @ 12.0.7.67808.]*

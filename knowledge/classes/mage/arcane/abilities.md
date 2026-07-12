---
title: Arcane Mage — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
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
| **Presence of Mind** | Utility / burst enabler | — | Off-GCD, ~60s CD | Makes the next **2 Arcane Blasts instant**. Choice-node vs *Slipstream*. Used to squeeze instant builders into movement / burst. @verify-ingame |
| **Supernova** | CC / burst | Mana | ~25s CD | Choice-node vs *Dragon's Breath*. AoE that knocks enemies up and deals Arcane damage. @verify-ingame |
| **Mirror Image** | Defensive / Utility | — | ~120s CD | Summons 3 images that taunt-free absorb aggro and add damage; threat drop + defensive. Pre-pulled in the APL precombat. |
| **Alter Time** | Defensive / Movement | — | ~10s CD (re-press) | Snapshots position & health; re-press within the window to return to both — an escape / effective heal. @verify-ingame |
| **Prismatic Barrier** | Defensive | Mana | 30s CD (25s talented) | Absorb shield (the strongest Mage barrier); most spammable defensive, reduces magic damage. |
| **Ice Block** | Defensive | — | 180s CD (150s talented) | Full immunity; cancels your own casting. *Ice Cold* variant instead gives ~70% DR while still able to cast. |
| **Ice Barrier** | Defensive | Mana | — | (If talented) frost absorb shield; operates on a shorter GCD in Midnight. @verify-ingame |
| **Blink** | Movement | — | ~15s CD | Teleport ~20yd forward, breaks roots. *Shimmer* replaces it with a **2-charge** off-GCD blink; *Improved Blink* is the alt choice. |
| **Counterspell** | Interrupt | — | 24s CD | Interrupts + locks the target's school for a few seconds. |
| **Frost Nova** | CC | — | ~25s CD (2 charges w/ talent) | Roots nearby enemies in place; kiting / peel tool. |
| **Cone of Cold** | CC / AoE | Mana | ~12s CD | Frontal cone dealing Frost damage and slowing. |
| **Polymorph** | CC | Mana | 1.5s cast | Long single-target sheep (Beast); breaks on damage, regenerates the target. |
| **Mass Polymorph** | CC | Mana | Cast | Talent. AoE Polymorph — sheeps multiple enemies at once. |
| **Slow Fall** | Utility | Reagent-free | Instant | Levitate/slow-fall on a friendly target. |
| **Spellsteal** | Dispel / Utility | Mana | Instant | Steals a beneficial magic effect from an enemy onto yourself. |
| **Remove Curse** | Dispel | — | Instant | Removes a Curse from a friendly target. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Instant | Raid-wide **Intellect** buff; precombat maintenance cast. |
| **Time Warp** | Major cooldown (raid) | — | 300s CD | Raid **30% Haste for 40s** (Bloodlust equivalent; personal Temporal Displacement lockout). |
| **Greater Invisibility** | Defensive / Utility | — | ~90s CD, 2 charges | Instant invisibility + strong damage reduction while fading; a hard-reset defensive and threat drop. |
| **Mass Invisibility** | Utility | — | Talent CD | Turns the whole party/raid invisible — skip/reset trash. |
| **Ice Cold** | Defensive | — | (replaces Ice Block) | Talent: Ice Block becomes ~70% DR you can act through instead of a full stop. |

> Utility/defensive cast times and cooldowns are standard Mage values reconciled
> against the 12.0.7 talent tree (`talents.md`); rows marked `@verify-ingame`
> carry small uncertainty on exact CD/charges and should be confirmed live.

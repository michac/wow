---
title: Frost Death Knight — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/death-knight/frost/ability-inventory.tsv  # tier 1, DB2 @ 12.0.7.67808 — names, spellIDs, origin, cooldowns
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Frost.simc  # tier 1 APL + talent string, 2026-07-11
  - https://www.method.gg/guides/frost-death-knight/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/frost-death-knight-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - raw/wago/SpellName.csv  # tier 1 game-data name reconciliation, 2026-07-11
confidence: high
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Frost Death Knight — Abilities (Midnight S1)

## Overview

Frost Death Knight is a melee physical (Frost-school) DPS. **Resources: Runes
(6, regenerate over time) + Runic Power (0–100+).** Spending runes builds Runic
Power; spending Runic Power has a chance to refund runes (Runic Attenuation /
Runic Overflow). The whole spec is a **proc-management loop** on top of that
economy:

- **Killing Machine** — auto-attack crits grant a stack that makes the next
  **Obliterate** (or **Frostscythe**) a guaranteed crit. The core "spend now"
  proc; can bank to 2 stacks.
- **Rime** — Frost Strike / Glacial Advance have a chance to make the next
  **Howling Blast** free and empowered.
- **Razorice** — the mainhand/offhand runeforge debuff stacks on the target to
  5; at 5 stacks **Frost Strike** (with **Shattering Blade**) becomes a burst
  spender.

Two hero trees split the playstyle: **Deathbringer** (Reaper's Mark → Exterminate
burst windows, the raid/single-target default) and **Rider of the Apocalypse**
(summons the Four Horsemen, favored for AoE / Mythic+). Two rune-spending engines
layer on top: **Breath of Sindragosa** (Runic-Power-fueled sustained cone) or
**Obliteration** (a burst "weave" window tied to Pillar of Frost). See
`rotation.md` and `builds.md`.

## Inventory

> **Where the numbers come from.** `ability-inventory.tsv` in this folder is the
> Tier-1 record for **name, spellID, origin and cooldown** (DB2 @ 12.0.7.67808) —
> read it rather than trusting a number restated here. A `[T1]` stamp marks a
> cooldown taken from it; everything else is Tier-3 colour from the simc APL /
> method.gg / Icy Veins.

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
| Obliterate | Rotational-spender | 2 Runes | Instant / — | Main single-target rune spender; guaranteed crit and empowered when it consumes a Killing Machine stack. |
| Frost Strike | Rotational-spender | 25 Runic Power | Instant / — | Runic Power dump; applies/refreshes Razorice. Becomes a burst button at 5 Razorice with Shattering Blade. |
| Howling Blast | Rotational-builder | 1 Rune (free w/ Rime) | Instant / — | Applies **Frost Fever** disease; AoE around the target. Free + empowered when it consumes a Rime proc. |
| Frostscythe | Rotational-spender | 1 Rune | Instant / — | AoE cone that consumes Killing Machine (the AoE stand-in for Obliterate). Talent. |
| Glacial Advance | Rotational-spender | 30 Runic Power | Instant / — | Line AoE that applies Razorice; the AoE Runic Power dump (replaces Frost Strike at 3+ targets). **Class-baseline `[T1]`, not a talent** — it costs you no tree point, so there is no build in which the AoE dump is unavailable. |
| Remorseless Winter | Rotational-builder / AoE | 1 Rune | Instant / 20s | PBAoE around you; feeds Gathering Storm stacks. Cornerstone of AoE and a Gathering Storm buff source. |
| Pillar of Frost | Major cooldown (talent) | 1 Rune | Instant / 45s `[T1]` | Strength buff window; the anchor all other cooldowns sync to. At 45s it is the **fast** cooldown in the kit — it lands three times per Breath of Sindragosa cycle and twice per Frostwyrm's Fury, so plan the alignment around Pillar coming back, not the other way round. |
| Empower Rune Weapon | Major cooldown | — | Instant / 2 min (charges) | Instantly refills runes, floods Runic Power, and grants Haste. Used to fuel Obliteration/Breath windows and prevent overcap. |
| Frostwyrm's Fury | Major cooldown | — | Instant / **90s** `[T1]` | Frontal cone burst that applies a slow; with Rider/Chosen of Frostbrood it also summons/buffs the Horsemen. Talent. |
| Breath of Sindragosa | Major cooldown | 60 Runic Power + drain | Channel-style / **90s** `[T1]` | Sustained frontal AoE that drains Runic Power; extends (up to ~30s) by consuming Killing Machine/Rime. Talent, build-defining. |
| Reaper's Mark | Major cooldown / Rotational | 1 Rune | Instant / ~45s | **Deathbringer** hero ability. Applies a mark that detonates for burst, granting **Exterminate** charges (empowered, cheaper Obliterate/Frostscythe). |
| Raise Dead | Pet | — | Instant / ~2 min (or passive) | Summons a ghoul (permanent-style pet for Frost). With Rider of the Apocalypse the toolkit adds the Horsemen. |
| Chosen of Frostbrood | Major cooldown | — | Instant / — | Midnight-era Frost capstone that ties Frostwyrm's Fury into the burst window. @verify-ingame exact effect |
| Death and Decay | Utility / AoE | 1 Rune | Instant / 15s | Ground-target damage zone. Rarely used by Frost (Blood/Unholy staple); baseline class ability. |
| Death Strike | Defensive | 35 Runic Power | Instant / — | Heals based on recent damage taken; the primary self-heal / Runic-Power defensive dump. |
| Death Coil | Utility | 30 Runic Power | Instant / — | Unholy's spender; on Frost it is off-rotation (Lichborne self-heal / niche). Baseline. |
| Icebound Fortitude | Defensive | — | Instant / **120s** `[T1]` | −30% damage taken and stun immunity for ~8s. Core survivability cooldown. |
| Anti-Magic Shell | Defensive | — | Instant / 1 min | Absorbs magic damage and generates Runic Power; usable for magic-damage soaks. |
| Anti-Magic Zone | Defensive / Utility | — | Instant / **240s** `[T1]` | Ground bubble reducing magic damage for the group. Talent (raid CD). |
| Lichborne | Defensive | — | Instant / 2 min | Turns you undead: immune to Charm/Fear/Sleep; enables Death Coil self-heal. |
| Death Pact | Defensive | — | Instant / 2 min | Heals ~50% max health with a short healing-taken debuff drawback. Talent. |
| Death Strike (see above) | Defensive | 35 RP | — | (Primary active mitigation — listed once above.) |
| Mind Freeze | Interrupt | — | Instant / 15s | Melee-range kick; interrupts and locks the school. The spec's interrupt. |
| Asphyxiate | CC | — | Instant / 45s | Ranged stun. Talent (choice vs Death's Reach). |
| Blinding Sleet | CC | — | Instant / 1 min | Cone disorient around you. Talent. |
| Chains of Ice | CC / Utility | 1 Rune | Instant / — | Heavy target slow; with Rider adds Trollbane's Icy Fury damage. |
| Death Grip | Utility / CC | — | Instant / 25s | Pulls the target to you (taunt in tank spec); a gap-closer/control tool. |
| Dark Command | Utility (taunt) | — | Instant / 8s | Forces the target to attack you. Baseline taunt. |
| Death's Advance | Movement (passive) | — | Passive | Reduces movement-impairing effects and grants passive speed. |
| Wraith Walk | Movement | — | Channel / **60s** `[T1]` | Channel for a burst of +70% movement speed, immune to slows. Talent (choice vs March of Darkness). |
| Path of Frost | Movement / Utility | 1 Rune | Instant / — | Lets you (and allies) walk on water. Out-of-combat utility. |
| Raise Ally | Utility (combat rez) | 30 Runic Power | Instant / 10 min | Battle resurrection of a fallen ally. |
| Control Undead | Utility | 1 Rune | 1.5s cast / — | Enslaves an undead target as a temporary pet. |
| Dark Simulacrum | Utility (**PvP talent**) | — | Instant / 20s `[T1]` | Copies the next spell an enemy casts so you can cast it back. It sits in the **PvP talent** pool, so it is not selectable in raid or Mythic+ — carried here for completeness, not as a PvE button. |

> Reconciliation note: every seed ability name matches current Tier-1 game data
> (`raw/wago/SpellName.csv`) — no renames. Frost-relevant Midnight-era additions
> flagged above: **Chosen of Frostbrood** (Frost capstone) and **Frostbane** (M+
> cleave talent, see `builds.md`). Frost does **not** use Death and Decay / Death
> Coil in its damage rotation; they are baseline class abilities carried for
> completeness. **Soul Reaper** and **Chill Streak** exist in the class/spec kit
> but are off-meta talents for S1 and are not core buttons.

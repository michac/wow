---
title: Subtlety Rogue — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Rogue_Subtlety.simc  # tier 1 APL — action list + talent string, WoW 12.0.x
  - https://www.method.gg/guides/subtlety-rogue/playstyle-and-rotation  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/subtlety-rogue-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 — ability numbers
  - https://us.api.blizzard.com/data/wow/search/spell  # tier 1 game-data name reconcile (raw/wago/SpellName.csv)
confidence: medium
---

# Subtlety Rogue — Abilities (Midnight Season 1)

## Overview

Subtlety is the shadow/stealth melee-assassin Rogue spec. **Resource:
Energy** (0–100+, regenerates continuously) fuels **combo-point builders**;
builders bank up to a max of **combo points** (7 with Deeper Stratagem +
Secret Stratagem) that **finishers** spend. The whole spec is built around
**Shadow Dance** — a short stealth-like window that turns on Stealth-only
abilities (Shadowstrike, Find Weakness) and is where nearly all burst
damage happens. You alternate builder → finisher, cramming **Secret
Technique** and big finishers into every Shadow Dance, and line the
**Shadow Blades** major cooldown up with a pair of Shadow Dance charges.

**Hero trees (S1):** **Trickster** (recommended, well-rounded — Unseen
Blade applies *Fazed*, feeds the **Coup de Grace** finisher via Flawless
Form stacks) and **Deathstalker** (single-target-leaning — **Shadowstrike**
applies *Deathstalker's Mark*, and consuming it grants **Darkest Night**
which empowers the next **Eviscerate**). See `builds.md` / `rotation.md`.

> **Midnight note:** the S1 core rotation drops several long-standing
> Subtlety buttons. **Rupture** and **Symbols of Death** are **not** active
> abilities in the S1 APL, and **Slice and Dice** appears only as a
> maintained buff (kept up passively via Shadow Dance / talents, not spammed
> as a cast). **Deepening Shadows** was reworked: it no longer grants Shadow
> Dance cooldown reduction per combo point — it now extends Shadow Dance
> **duration** scaling with Haste. @verify-ingame (confirm Rupture/SnD/Symbols
> are truly off the bars and exact reworked numbers)

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Shadowstrike** | Rotational-builder | 40 Energy | instant | Stealth/Shadow Dance-only. Teleports behind the target, high damage, builds combo points, grants Find Weakness. In Deathstalker, the first cast applies **Deathstalker's Mark**. The premier Shadow Dance builder. |
| **Backstab** | Rotational-builder | 35 Energy | instant | Non-stealth single-target builder; bonus damage/crit from behind. Replaced by **Gloomblade** if talented. |
| **Gloomblade** | Rotational-builder | 35 Energy | instant | Talent replacement for Backstab — pure Shadow damage, no positional requirement, builds combo points. |
| **Shuriken Storm** | Rotational-builder | 35 Energy | instant | AoE builder; hits all nearby enemies and builds a combo point per target. Empowered during Stealth/Shadow Dance (Silent Storm / Improved Shuriken Storm). Primary 2+ target builder. |
| **Goremaw's Bite** | Rotational-builder / cooldown | ~45 Energy | ~45s CD (charges) | Talent active; a big shadow bite that generates a burst of combo points (and energy). Woven in on cooldown when combo-point deficit allows. @verify-ingame (exact cost/CD/CP) |
| **Shuriken Toss** | Rotational-builder (ranged) | 40 Energy | instant, 30 yd | Ranged combo-point builder for when melee range isn't possible. |
| **Eviscerate** | Rotational-spender | 35 Energy | instant | Baseline single-target finisher; spends combo points for Shadow damage. Empowered by **Darkest Night** (Deathstalker) — the priority finisher while that buff is up. |
| **Secret Technique** | Rotational-spender / cooldown | 30 Energy | ~45s CD | Combo-point finisher summoning shadow clones for a large burst; short, Haste-reduced cooldown. Highest-priority finisher inside Shadow Dance. |
| **Coup de Grace** | Rotational-spender | (finisher) | — | Trickster capstone finisher — after building Unseen Blade / Flawless Form stacks it delivers a large empowered strike. Prioritized over Eviscerate when up. |
| **Black Powder** | Rotational-spender (AoE) | 35 Energy | instant | AoE finisher; Shadow damage to all nearby enemies and applies Find Weakness in AoE. Used on 3+ targets. |
| **Shadow Dance** | Major cooldown | — | recharge, 2 charges | Grants a Stealth-like window (~6s, extended by Haste via Deepening Shadows) enabling Shadowstrike/Find Weakness and buffing shadow abilities. **The core damage window** — Double Dance gives 2 charges. @verify-ingame (exact recharge) |
| **Shadow Blades** | Major cooldown | — | ~90s CD | Empowers autoattacks/abilities with Shadow damage and boosts combo-point generation for its duration. Lined up with Shadow Dance windows. |
| **Symbols of Death** | (legacy) | — | — | Historically a 1-min damage cooldown; **not present in the S1 APL** — appears removed/reworked in Midnight for Subtlety. @verify-ingame |
| **Vanish** | Major cooldown / Utility | — | ~2 min CD (charges) | Re-enters Stealth mid-combat (drops threat), re-enabling Shadowstrike and stealth openers; also an aggro/threat drop. |
| **Stealth** | Utility (opener) | — | out of combat | Enter stealth before a pull to open with Shadowstrike + full Find Weakness. |
| **Kick** | Interrupt | — | 15s CD | Melee interrupt — kicks a spellcast and briefly locks that school. |
| **Kidney Shot** | CC (finisher) | 25 Energy | 20s CD | Combo-point finisher stun; duration scales with combo points spent. |
| **Cheap Shot** | CC (opener) | 40 Energy | — | Stealth/Shadow Dance-only opener stun (~4s); builds a combo point. |
| **Gouge** | CC | 25 Energy | 15s CD | Frontal incapacitate (~4s), breaks on damage. Choice node with Airborne Irritant. |
| **Blind** | CC | — | ~2 min CD | Disorients the target for up to 1 min (breaks on damage). |
| **Sap** | CC (opener) | — | — | Stealth-only; incapacitates a non-combat target long-term. |
| **Shadowstep** | Movement | — | ~30s CD (charges) | Teleports behind the target and boosts movement speed briefly — gap-closer + repositioner. |
| **Sprint** | Movement | — | ~2 min CD | Large short-duration movement-speed boost. @verify-ingame (CD) |
| **Grappling Hook** | Movement | — | ~1 min CD | Pull-to-location mobility (baseline Rogue). @verify-ingame (spec access) |
| **Evasion** | Defensive | — | ~2 min CD | +Dodge vs melee/ranged for ~10s. |
| **Feint** | Defensive | 35 Energy | 15s CD | Reduces AoE damage taken for ~6s — the main scheduled raid-damage mitigation. |
| **Cloak of Shadows** | Defensive / Dispel | — | ~2 min CD | Brief immunity to magic damage/effects and removes existing magic debuffs (self-dispel). |
| **Crimson Vial** | Defensive (self-heal) | 20–30 Energy | ~30s CD | Instant self-heal over a few seconds — the spammable personal heal. |
| **Thistle Tea** | Defensive / Utility (resource) | — | charges, ~1s | Restores a large chunk of Energy (and buffs Mastery); auto-used at low energy in the sim. |
| **Cloak of Shadows** *(dispel role)* | Dispel | — | ~2 min CD | (see above) removes harmful magic effects on self. |
| **Shiv** | Utility / Dispel | 20 Energy | ~25s CD (charges) | Applies a nonlethal poison, dispels an enrage, and (talented) applies a damage-taken debuff / slows. |
| **Tricks of the Trade** | Utility | — | 30s CD | Redirects your threat to an ally for a few seconds (choice node with Blackjack). |
| **Distract** | Utility | — | 30s CD | Draws mob attention to a spot — pull/pathing tool. |
| **Shroud of Concealment** | Utility (raid) | — | ~6 min CD | Group stealth — sneaks the party/raid past trash. |
| **Poisons** | Utility (prep) | — | out of combat | Applied pre-combat: a **lethal** poison (Instant/Wound) plus a **nonlethal** utility poison (Crippling/Numbing/Atrophic). Passive damage/utility once applied. |
| **Find Weakness** | Passive | — | — | Applied by Shadowstrike/openers — grants a window of increased damage (armor-ignoring); a core part of Shadow Dance value. |
| **Deathstalker's Mark** | Passive (Deathstalker) | — | — | Applied by Shadowstrike; stacking mark whose consumption grants **Darkest Night** to empower the next Eviscerate. |
| **Darkest Night** | Passive (Deathstalker) | — | — | Buff from consuming Deathstalker's Mark — makes the next Eviscerate the top-priority, empowered finisher. |
| **Unseen Blade** | Passive (Trickster) | — | — | Randomly strikes for extra damage and applies **Fazed** (+damage-taken, can't be parried); builds toward **Coup de Grace** via Flawless Form stacks. |
| **Ancient Arts** | Passive (apex) | — | — | Apex talent — spending Shadow Techniques stacks triggers shadow-clone strikes / combo-point refunds; gates a few opener lines in the APL. |

---
title: Retribution Paladin — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Paladin_Retribution.simc  # tier 1 APL + talent string, 2026-07-11
  - https://www.method.gg/guides/retribution-paladin/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.method.gg/guides/retribution-paladin/talents  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/retribution-paladin-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1 name canonicalization, 2026-07-11
confidence: medium
---

# Retribution Paladin — Ability Inventory (Midnight S1)

## Overview

Retribution is a melee plate DPS spec that spends **Holy Power** (0–5), a
discrete secondary resource built by melee builders and burned by finishers.
Mana is a background pool used only for the paladin utility/blessing kit, not
the damage rotation. The loop is: generate Holy Power with builders
(Templar Strike/Slash or Crusading Strikes auto-attacks, Judgment, Blade of
Justice, Wake of Ashes, Divine Toll) and spend it on a finisher (**Final
Verdict** single-target / **Divine Storm** AoE), while weaving proc-driven
instant hits (Art of War → Blade of Justice, Empyrean Power → free Divine
Storm) and the big cooldowns (Avenging Wrath, Wake of Ashes, Execution
Sentence, Divine Toll).

**Hero trees:** **Templar** (S1 default, all content) and **Herald of the
Sun** (viable alternative). Templar reshapes the rotation — after **Wake of
Ashes**, your Holy Power spender is replaced by **Hammer of Light** for 20s,
and **Light's Deliverance** later grants free Hammer of Light casts. Herald
of the Sun instead builds around **Dawnlight** / **Eternal Flame** and the
**Sun's Avatar** window (not the Hammer of Light gameplay).

Names below are canonicalized against Blizzard game data
(`SpellName.csv` @ 12.0.7.67808). Cooldown/cost values are talent- and
haste-dependent; low-confidence numbers are marked `@verify-ingame`.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Crusader Strike** | Rotational-builder | — | instant / ~4.5s recharge (haste) | Baseline melee Holy Power builder (+1 HP). Often replaced in the tree by the Templar Strike / Crusading Strikes choice node. |
| **Templar Strike** / **Templar Slash** | Rotational-builder | — | instant / shared recharge | Two-part builder combo (Templar hero synergy path via the Templar Strikes talent). Templar Strike then Templar Slash; each grants Holy Power. Replaces Crusader Strike as the filler builder when talented. @verify-ingame |
| **Crusading Strikes** (passive) | Rotational-builder | — | passive | Alternative to Templar Strikes: auto-attacks generate Holy Power (1 HP roughly every other swing) and turn autos into a resource stream. Track it so finishers don't overcap. |
| **Judgment** | Rotational-builder | — | instant / ~6s (haste/talents) | 30yd builder; applies the Judgment debuff (amplifies your next holy damage) and generates Holy Power (with Boundless/Improved Judgment). Becomes empowered by Hammer of Wrath uptime during wings. |
| **Blade of Justice** | Rotational-builder | — | instant / ~12s (2 charges w/ Improved BoJ) | Strong ranged-ish builder (+2 HP), applies **Expurgation** (fire DoT) with Holy Flames. Resets/procs off **Art of War** and **Righteous Cause** for free instant casts. High priority. |
| **Final Verdict** | Rotational-spender | 3–5 Holy Power | instant / — | Primary single-target finisher (talent that upgrades Templar's Verdict). Big single-target hit; buffed +20% during Avenging Wrath via the Light Within apex. Spend at 5 HP (or 4 with a pending Crusading Strikes auto). |
| **Templar's Verdict** | Rotational-spender | 3 Holy Power | instant / — | Baseline single-target finisher; upgraded to Final Verdict when talented. The simc APL's `templars_verdict` action is Final Verdict in the recommended build. |
| **Divine Storm** | Rotational-spender | 3–5 Holy Power | instant / — | AoE finisher; hits all nearby enemies. Free instant cast on an **Empyrean Power** proc. Primary spender at 3+ targets (2+ with Tempest of the Lightbringer, no Jurisdiction). |
| **Hammer of Light** | Rotational-spender | 5 Holy Power | instant / — | **Templar** signature. Replaces Wake of Ashes for 20s after WoA; a 5-HP nuke that fuels Shake the Heavens / Empyrean Hammer / Light's Deliverance. **Light's Deliverance** later grants *free* Hammer of Light procs. Top spend priority when available. |
| **Wake of Ashes** | Major cooldown / builder | — | instant / ~30s (talent) | Cone burst that generates a chunk of Holy Power, applies a truesilver/holy debuff, and (Templar) enables **Hammer of Light** for 20s. With **Sacrosanct Crusade** it also heals/shields — doubles as a defensive. |
| **Execution Sentence** | Major cooldown | — | instant / ~30s (talent) | Marks the target; after a delay (~8–10s) detonates for accumulated holy damage. Line up with Avenging Wrath. Cast just before wings. @verify-ingame |
| **Divine Toll** | Major cooldown / builder | — | instant / ~60s (Quickened Invocation reduces) | Fires up to 5 Judgments across nearby enemies, generating a burst of Holy Power. With **Divine Hammer** (Templar) it summons Empyrean Hammers around you afterward. Strong AoE Holy Power injection. |
| **Avenging Wrath** | Major cooldown | — | instant / ~60s, ~20s duration | Core burst window: increased damage and crit. Converts Judgment into a Hammer of Wrath enabler and lets Hammer of Wrath be used on any-health targets. **Crusade** replaces it (builds stacks). **Radiant Glory** removes it as a button — Wake of Ashes/Execution Sentence auto-trigger the wings window. |
| **Crusade** (passive/replaces AW) | Major cooldown | — | ~in place of Avenging Wrath | Talent that swaps Avenging Wrath for a stacking haste/damage buff built by Holy Power spending; ramps to a stronger peak. |
| **Hammer of Wrath** | Rotational-builder (conditional) | — | instant / ~7.5s | Ranged finisher-adjacent builder usable on targets below ~20% HP, or on any target while Avenging Wrath/wings are active. Free/priority with **Walk Into Light**. |
| **Divine Hammer** (Templar passive) | Passive (AoE) | — | passive | Summons **Empyrean Hammers** around you after Divine Toll (and Hammer of Light activity), dealing area holy damage. |
| **Shield of Vengeance** | Defensive | — | instant / ~1.5–2min | Absorb shield that also reflects a portion of absorbed damage back as holy damage. Class-tree talent, minor DPS + mitigation. @verify-ingame |
| **Divine Protection** | Defensive | — | instant / ~1min | Reduces damage taken (~20%) for a short duration. Cheap, frequent personal defensive. @verify-ingame |
| **Shield of the Righteous** | Defensive | Holy Power | instant | Not a Ret core button, but the shared Holy Power self-mitigation; Ret rarely uses it (spends HP on damage). |
| **Divine Shield** | Defensive (immunity) | — | instant / 5min (Unbreakable Spirit reduces) | Full immunity to all damage/debuffs for 8s; drops threat. The paladin "bubble". Can be cancelled early. |
| **Lay on Hands** | Defensive (emergency) | high mana | instant / ~10min (reduced by Unbreakable Spirit) | Heals the target to full HP. Panic-button full heal (self or ally). |
| **Word of Glory** | Defensive / self-heal | 3 Holy Power | instant / — | Spends Holy Power to heal self/ally. Competes with damage spenders — situational off-heal. |
| **Flash of Light** | Utility (heal) | mana | ~1.5s cast | Fast direct heal; out-of-combat or downtime topping. |
| **Blessing of Freedom** | Utility (movement) | mana | instant / ~25s | Grants immunity to movement-impairing effects to the target. |
| **Blessing of Protection** | Defensive (external) | mana | instant / ~5min | Physical-damage immunity + removes physical debuffs on an ally (can't attack while active). |
| **Blessing of Sacrifice** | Defensive (external) | mana | instant / ~1–2.5min | Redirects a portion (~30%) of an ally's incoming damage to you. |
| **Divine Steed** | Movement | — | instant / ~45s, 2 charges (Cavalier) | Mounted sprint (+100% speed) for a few seconds; the main mobility cooldown. |
| **Rebuke** | Interrupt | — | instant / 15s | Melee kick; interrupts and locks out the school. The spec's only true interrupt. |
| **Hammer of Justice** | CC (stun) | mana | instant / ~60s (Fist of Justice reduces) | Ranged single-target stun (~6s). |
| **Blinding Light** | CC (AoE) | mana | instant / ~90s | Disorients all nearby enemies for a few seconds. |
| **Turn Evil** | CC (situational) | mana | ~1.5s cast / — | Fears an Undead/Demon/Aberration target. |
| **Hand of Reckoning** | Utility (taunt) | mana | instant / 8s | Ranged taunt; forces a target to attack you (minor threat/utility). |
| **Cleanse Toxins** | Dispel | mana | instant / ~8s | Removes Poison and Disease effects from the target. |
| **Intercession** | Utility (combat rez) | mana | ~ cast / — | Battle resurrection — revives a dead ally in combat (shares the raid rez pool). |
| **Redemption** | Utility (out-of-combat rez) | mana | ~10s cast | Revives a dead ally out of combat. |
| **Devotion Aura** | Utility (aura) | — | passive toggle | Party/raid armor & minor damage-reduction aura. |
| **Concentration Aura** | Utility (aura) | — | passive toggle | Reduces silence/interrupt/knockback effects for the group. |
| **Crusader Aura** | Utility (aura) | — | passive toggle | Increases mounted movement speed for the group (out-of-combat travel). |
| **Light Within** (apex) | Passive (major) | — | passive | Ret apex talent: amplifies Art of War — Blade of Justice +150% on proc, and +20% Divine Storm/Final Verdict during Avenging Wrath. |

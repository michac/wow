---
title: Protection Paladin — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/protection-paladin/playstyle-and-rotation  # tier 3, upd. 2026-07-09
  - https://www.icy-veins.com/wow/protection-paladin-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/protection-paladin-pve-tank-spell-summary  # tier 3, 12.0.7
  - raw/wago/SpellName.csv  # tier 1, name reconciliation @ build 12.0.7.67808
  - knowledge/classes/paladin/protection/talents.md  # tier 1 talent tree (Blizzard API + wago)
confidence: high
---

# Protection Paladin — abilities (Midnight S1)

## Overview

Protection Paladin is a plate melee tank built on the **Holy Power** resource
(0–5). Short-cooldown builders (Judgment, Blessed Hammer / Hammer of the
Righteous, Avenger's Shield) generate Holy Power in ones and twos; you spend it
in blocks of **3** on **Shield of the Righteous** (the mitigation button — armor
+ block/avoidance buff, off-GCD) or **Word of Glory** (a Holy-Power heal). The
active-mitigation loop is: never Holy-Power-cap, keep **Consecration** down under
you, and keep **Shield of the Righteous** rolling. The two hero trees fork the
kit: **Templar** turns **Divine Toll** into a 12-second **Hammer of Light** burst
window and layers **Shake the Heavens**; **Lightsmith** adds the **Holy
Armaments** buffs (**Sacred Weapon** / **Holy Bulwark**) via a rechargeable
charge system.

> **Midnight changes worth flagging (12.0.x):**
> - **Hammer of Wrath is no longer its own button** — it is now a *transform of
>   Judgment* that is only castable during **Avenging Wrath** (and, baseline, on
>   enemies below the execute threshold). During Wings, press Judgment and it
>   fires Hammer of Wrath. This simplifies the bar and shifts the Holy-Power
>   economy. @verify-ingame (exact charge/HP behaviour of the Judgment→HoW swap)
> - **Eye of Tyr, Moment of Glory, and Bastion of Light were removed** in
>   Midnight. Eye of Tyr is effectively replaced in the Templar kit by the
>   Divine Toll → Hammer of Light flow. (Eye of Tyr was not in the current spec
>   kit — do not author it as a live button.)

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Shield of the Righteous | Rotational-spender (Defensive) | 3 Holy Power | Instant / off-GCD (no CD) | Core active mitigation. Deals Holy AoE damage in front and grants the SotR buff (armor + block/avoidance) for ~4.5s. Your primary Holy-Power sink; keep the buff rolling and never HP-cap. |
| Judgment | Rotational-builder | Generates Holy Power | Instant / ~6s (Crusader's Judgment adds a charge) | Ranged builder; applies Judgment debuff (Greater Judgment). **During Avenging Wrath it becomes Hammer of Wrath.** |
| Blessed Hammer | Rotational-builder | Generates 1 Holy Power | Instant / ~3 charges, ~4.5s recharge | Choice-node builder (vs Hammer of the Righteous). Throws hammers that damage and briefly reduce enemy damage. Default M+/AoE builder. |
| Hammer of the Righteous | Rotational-builder | Generates Holy Power | Instant / charges | Choice-node alternative to Blessed Hammer; melee builder, favored in some single-target/Templar setups (Blessed Assurance empowerment). |
| Avenger's Shield | Rotational-builder / Interrupt / Utility | Generates Holy Power (up to 3 w/ Glory of the Vanguard) | Instant, ranged / ~15s (reset by Grand Crusader) | Throws shield at up to 3 targets (more with Bulwark of Order/Soaring Shield), **interrupts and silences** the first for 3s, applies a small absorb. Grand Crusader procs reset it. |
| Consecration | Rotational / Utility | — | Instant / ~9s (or by charge) | Ground effect (~12s) that deals Holy damage and enables/boosts several talents; stay standing in it. Refresh when it drops or when moving off it. |
| Hammer of Wrath | Rotational-builder (execute) | Generates Holy Power | Instant, ranged / usable during Avenging Wrath or on low-HP targets | Now a **Judgment transform** during Avenging Wrath; also usable baseline on enemies below the execute HP threshold. High-priority builder when available. |
| Divine Toll | Major cooldown / Rotational-builder | Generates Holy Power | Instant / ~1 min | Casts Avenger's Shield at up to 5 nearby enemies, generating a burst of Holy Power. **Templar:** casting it grants **Hammer of Light** for 12s. Synced with the Avenging Wrath window. |
| Hammer of Light | Rotational-spender (Templar) | 3 Holy Power | Instant / available 12s after Divine Toll | Templar-only. Big Holy AoE nuke that replaces Divine Toll for 12s after it is cast; top priority while active. Sustains Shake the Heavens. |
| Word of Glory | Rotational-spender (Self-heal) | 3 Holy Power | Instant / no CD | Holy-Power heal scaling with missing health; **free/empowered with Shining Light** procs (and, for Templar, cheaper with Shake the Heavens active). |
| Sacred Weapon | Utility buff (Lightsmith) | Holy Armaments charge | Instant / rechargeable charges | Lightsmith armament: a weapon buff that adds Holy damage/healing. Refresh when the buff drops below ~5s; use while Avenging Wrath is unavailable. |
| Holy Bulwark | Defensive (Lightsmith) | Holy Armaments charge | Instant / rechargeable charges | Lightsmith armament: a personal absorb shield. Shares the Holy Armaments charge pool with Sacred Weapon; spend outside the Wings window. |
| Avenging Wrath | Major cooldown (offensive) | — | Instant / ~2 min (≈1 min with Righteous Protector) | "Wings." +20% damage/healing (and crit when talented) for the burst window; converts Judgment to Hammer of Wrath. Choice node vs Sentinel. |
| Sentinel | Major cooldown (defensive) | — | Instant / ~2 min | Choice-node alternative to Avenging Wrath: a stacking damage-and-mitigation buff that ramps over its duration. Defensive-leaning burst pick. |
| Ardent Defender | Defensive | — | Instant / ~1.5 min | ~20% damage reduction + absorb for ~8s; the cheat-death floor (prevents one lethal hit and heals if it would kill you). Shortest-CD major wall. |
| Guardian of Ancient Kings | Major defensive | — | Instant / ~3–5 min | Large damage reduction (~50%) for ~8s; a second charge is possible via Empyrean Authority. @verify-ingame (exact cooldown 3 vs 5 min) |
| Divine Shield | Defensive (immunity) | — | Instant / ~5 min | Full immunity for 8s. With **Final Stand** it also taunts nearby enemies (keeps aggro instead of dropping it). Drops threat otherwise. |
| Lay on Hands | Defensive (emergency heal) | — | Instant / ~10 min | Heals the target to full (self or ally). Emergency button. |
| Blessing of Freedom | Utility (movement) | — | Instant / ~25s | Removes and grants immunity to movement-impairing effects for a short time. |
| Blessing of Protection | Defensive (external) | — | Instant / ~5 min | Physical-damage immunity on an ally (or self); causes a threat drop without Hand of Reckoning follow-up. |
| Blessing of Spellwarding | Defensive (external) | — | Instant / ~3 min | Choice/talent replacing BoP: magic-damage immunity, no threat concern. Usable on self as a magic wall. |
| Blessing of Sacrifice | Defensive (external) | — | Instant / ~1 min | Redirects a portion of an ally's incoming damage to you; core cooldown for guarding a co-tank or squishy. |
| Divine Steed | Movement | — | Instant / 2 charges (Cavalier) | Temporary mounted speed boost; two charges with Cavalier for chaining gaps. |
| Hand of Reckoning | Taunt | — | Instant, ranged / ~8s | Single-target taunt; forces the enemy to attack you. |
| Rebuke | Interrupt | — | Instant / ~15s | Melee kick; interrupts a spellcast. Your on-demand interrupt (Avenger's Shield is the ranged one). |
| Hammer of Justice | CC (stun) | — | Instant / ~60s (less w/ Fist of Justice) | Ranged stun. |
| Blinding Light | CC (disorient) | — | Instant / ~90s | AoE disorient around you. |
| Turn Evil | CC (fear) | — | Cast / ~15s | Fears an Undead/Demon/Aberration target (instant with Wrench Evil). |
| Cleanse Toxins | Dispel | — | Instant / ~8s | Removes Poison and Disease from an ally. |
| Flash of Light | Utility (heal) | Mana | ~1.5s cast / — | Mana heal cast; slow off-Holy-Power topping tool. |
| Intercession | Utility (combat rez) | Mana | Cast / — | Battle resurrection (in-combat rez). |
| Redemption | Utility (rez) | Mana | Cast / — | Out-of-combat resurrection. |
| Rite of Sanctification | Utility buff (Lightsmith) | — | Cast (precombat) / — | Lightsmith raid buff (choice with Rite of Adjuration); set before pull. |
| Devotion Aura | Passive/Utility (aura) | — | Instant / — | Group armor aura; set-and-forget (one aura active). |
| Concentration Aura | Passive/Utility (aura) | — | Instant / — | Reduces silence/interrupt duration; situational aura swap. |
| Crusader Aura | Passive/Utility (aura) | — | Instant / — | Mounted movement-speed aura; travel only. |
| Guardian's/Empyrean absorbs (Bulwark of Order) | Passive | — | — | Avenger's Shield grants an absorb shield (Bulwark of Order); part of the passive EHP layer. |

> Auras are mutually exclusive (one active at a time) — Devotion is the default,
> swapped to Concentration for heavy silence/interrupt fights and Crusader only
> while traveling.

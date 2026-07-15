---
title: Guardian Druid — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/guardian-druid/playstyle-and-rotation  # tier 3, 12.0.7 upd. 2026-06-16
  - https://www.icy-veins.com/wow/guardian-druid-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - simc midnight branch profiles/MID1/MID1_Druid_Guardian.simc  # tier 1 APL + talents=, WoW 12.0.x
  - raw/wago/SpellName.csv  # tier 1 game data, name reconciliation
confidence: high
---

# Guardian Druid — Ability Inventory (Midnight S1)

## Overview

Guardian is the Druid **bear-form tank**. Its resource is **Rage** (0–100 by
default), built by short-cooldown generators (**Mangle**, **Thrash**) and by
auto-attacking / taking hits, and spent on **active mitigation** (**Ironfur**,
**Frenzied Regeneration**) and **offense** (**Maul** / **Raze**). The core loop:
keep Mangle and Thrash on cooldown, hold Thrash at max stacks, maintain
**Moonfire**, and dump rage on Ironfur when taking physical damage or on
Maul/Raze when defensively safe — never rage-capping. Almost all mitigation is
off the GCD, so bear can pump damage and stay defended simultaneously.

**Hero trees (Midnight):**
- **Elune's Chosen** — Arcane/lunar theme built around **Lunar Beam** and
  **Moonfire**; the **Lunation** talent turns Lunar Beam into a near-on-cooldown
  button (Thrash + Moonfire reduce its CD). Favored for M+ in S1 thanks to
  Thrash synergy.
- **Druid of the Claw** — physical/bleed theme; adds the **Ravage** proc that
  empowers Maul/Swipe and enables optional **catweaving / ripweaving** (shift to
  Cat Form for Rip/Ferocious Bite via **Feline Potential**). Higher ceiling,
  more complexity; roughly on par with Elune's Chosen in raid (within ~2–3%).

> **Midnight note:** the row-12 spec capstone active is now **Wild Guardian**
> (spell 1269614) — a burst cooldown that replaces the old **Rage of the
> Sleeper** for Guardian in this tree. **Red Moon** and **Sundering Roar** are
> Midnight talent additions. @verify-ingame (confirm Rage of the Sleeper is no
> longer on the bar and Wild Guardian occupies the capstone)

## Inventory

Rage costs marked @verify-ingame where sources disagree on the exact number;
the *function* is solid. "off-GCD" = does not trigger/consume the global.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Mangle** | Rotational-builder | Generates ~8 Rage | ~6s CD (hasted) | Core single-target rage generator; **Gore** can reset its CD for a free extra cast. Press on cooldown. |
| **Thrash** (Bear) | Rotational-builder | Generates ~5 Rage | ~6s CD (hasted) | AoE bleed that **stacks** (up to 3, more with Flashing Claws); keep at max stacks. Fuels Elune's Chosen (Lunar Beam CDR) and Sundering Roar. |
| **Moonfire** | Rotational-builder / DoT | Free (or free instant on proc) | Instant | Arcane DoT, maintained on the primary target. **Galactic Guardian** procs a free hard-hitting instant; **Lunation** makes Moonfire a filler that cuts Lunar Beam's CD. |
| **Swipe** (Bear) | Rotational-filler | Free | Instant | Low-priority AoE filler when nothing else is available (Druid of the Claw). |
| **Maul** | Rotational-spender | ~40 Rage @verify-ingame | Instant, on-GCD | Single-target rage dump; primary *offensive* spender. **Ravage** (Druid of the Claw) empowers it. |
| **Raze** | Rotational-spender | ~30–40 Rage @verify-ingame | Instant, on-GCD | Frontal-cone Maul replacement (talent); the AoE rage dump. Hits all enemies in front. |
| **Ravage** | Passive / proc (Druid of the Claw) | — | Proc buff | Empowers the next Maul/Swipe into **Ravage**; consuming procs is a core Druid of the Claw priority. |
| **Ironfur** | Defensive (active mitigation) | ~40 Rage @verify-ingame | Instant, **off-GCD** | Big **armor** buff (~112% Agility as armor) for ~6s; **stacks** for more armor but stacks don't refresh each other. Keep ≥1 stack while taking physical damage. |
| **Frenzied Regeneration** | Defensive (self-heal) | No rage @verify-ingame (charge-based) | Instant, ~36s recharge, 1–2 charges | Strong short-CD self-heal over 3s; with **Natural Resilience** overhealing converts to an absorb shield. Press *before* incoming damage. |
| **Barkskin** | Defensive | Free | **Off-GCD**, ~1 min CD | 20% damage reduction for ~8–12s; usable in any form and while stunned. |
| **Survival Instincts** | Major defensive | Free | **Off-GCD**, ~3 min recharge, 2 charges | ~50% damage reduction for a short window; the panic button. Don't overlap with Barkskin (multiplicative — wastes coverage). |
| **Bristling Fur** | Defensive / rage-gen | Free | ~40s CD | Generates rage from damage taken for a few seconds; used to refill rage during heavy incoming damage. |
| **Rage of the Sleeper** | (Historical — replaced) | — | — | Old Guardian defensive/offensive CD; **superseded by Wild Guardian** in the Midnight spec tree. @verify-ingame |
| **Lunar Beam** | Major cooldown / Rotational (Elune's Chosen) | Free | ~1 min CD | Ground-target beam: heavy Arcane damage + healing/mitigation while standing in it. With **Lunation** it's pressed near-on-cooldown (Thrash/Moonfire reduce its CD). Also a strong defensive. |
| **Wild Guardian** | Major cooldown (capstone active) | Free | On CD | Midnight-new burst active (spell 1269614); big damage, best fired at max Thrash stacks and/or during a Ravage/Lunar Beam window. |
| **Berserk** | Major cooldown | Free | **Off-GCD**, ~3 min | Throughput/CDR window (haste + reduced generator CDs). Choice node vs **Incarnation** / Convoke. |
| **Incarnation: Guardian of Ursoc** | Major cooldown | Free | **Off-GCD**, ~3 min | Empowered bear meta: big offensive + defensive uptime. Choice-node capstone (vs Convoke). Use on CD unless banking for a known hit. |
| **Convoke the Spirits** | Major cooldown | Free | ~2 min | Channels a burst of random druid spells; talent choice vs Incarnation. |
| **Sundering Roar** | Rotational cooldown / debuff | Free | On CD | Midnight-new roar (spell 1253799): damage + armor shred, fired at high Thrash stacks. |
| **Heart of the Wild** | Major cooldown (utility/throughput) | Free | ~2 min | Reworked: form-dependent bonus — bear grants an instant heal, cat empowers physical, moonkin a DoT burst. Enables the catweave/ripweave window. |
| **Growl** | Taunt (Utility) | Free | ~8s CD | Forces the target to attack you; the tank taunt. |
| **Skull Bash** | Interrupt | Free | ~15s CD | Bear-form kick / interrupt with a short gap-close. |
| **Stampeding Roar** | Movement (group) | Free | ~2 min (1 min w/ Improved) | AoE movement-speed burst for the group. |
| **Incapacitating Roar / Mighty Bash** | CC | Free | Choice node | Roar = short AoE incapacitate; Mighty Bash = single-target stun. |
| **Typhoon** | CC / knockback | Free | ~30s CD | Frontal knockback + daze (talent). |
| **Mass Entanglement / Ursol's Vortex** | CC | Free | Choice node | Mass Entanglement = AoE root; Ursol's Vortex = pull-in/leash zone. |
| **Entangling Roots** | CC (root) | — | Cast | Single-target root. |
| **Hibernate** | CC | — | Cast | Incapacitates a Beast or Dragonkin. |
| **Soothe** | Dispel (Enrage) | Free | ~10s CD | Removes an Enrage effect from an enemy. |
| **Remove Corruption** | Dispel | Free | Instant | Removes Curse and Poison from a friendly target. |
| **Rebirth** | Utility (combat rez) | — | Cast | Battle resurrection. |
| **Revive** | Utility (rez) | — | Cast | Out-of-combat resurrection. |
| **Innervate** | Utility (mana) | Free | ~3 min | Grants a healer free-mana casting for a few seconds. |
| **Mark of the Wild** | Utility (raid buff) | — | Instant | Party/raid Versatility buff. |
| **Symbiotic Relationship** | Utility | — | Cast | Links with an ally to share healing/leech benefits (talent). |
| **Regrowth** | Utility (heal) | — | Cast | Direct heal + HoT; used out of bear for off-healing (Dream of Cenarius). |
| **Barkskin / Survival Instincts** | *(listed above under Defensive)* | | | |
| **Dash** | Movement | Free | ~1.5 min | Cat-form sprint. |
| **Wild Charge / Tiger Dash** | Movement | Free | Choice node | Form-based gap-closer (bear charge / cat leap) or a sprint. |
| **Prowl** | Utility (stealth) | Free | — | Cat-form stealth (used to set up catweave openers). |
| **Bear Form** | Form | Free (grants 25 Rage on shift) | Instant | The tank form; all mitigation lives here. |
| **Cat Form** | Form | Free | Instant | Damage/movement form; entered for catweave/ripweave and Heart of the Wild. |
| **Travel Form** | Movement (form) | Free | Instant | Out-of-combat travel/flight/aquatic. |
| **Moonkin Form** | Form | Free | Instant | Caster form; used with Heart of the Wild for AoE Moonfire spread (6+ targets). |

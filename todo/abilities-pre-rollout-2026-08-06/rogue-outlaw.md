---
title: Outlaw Rogue — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/rogue/outlaw/ability-inventory.tsv  # tier 1, generated from DB2 @ 12.0.7.67808 — name/spellID/origin/cooldown source of record
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the 12.0.7.67808 adjudication behind this pass
  - raw/wago/SpellName.csv (Blizzard game data, Tier 1)   # tier 1, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Rogue_Outlaw.simc  # tier 1 APL (ability names / usage), 2026-07-11
  - https://www.method.gg/guides/outlaw-rogue  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-rotation-cooldowns-abilities  # tier 3, 2026-07-11
confidence: medium
---

# Outlaw Rogue — Abilities (Midnight S1)

## Overview

Outlaw is the swashbuckler melee-DPS Rogue spec: dual-wielding, pistol-toting,
buff-juggling. **Resource system:** **Energy** (0–100+, regenerates passively;
the primary spender fuel) plus **Combo Points** (build 0→6/7, spent by
finishers). Builders (Sinister Strike, Ambush, Pistol Shot) generate combo
points; finishers (Dispatch, Between the Eyes, Roll the Bones, Slice and Dice,
Kidney Shot) spend them.

**Hero trees.** `builds.md` owns the pick. In kit terms: **Trickster** adds
**Unseen Blade** procs and the **Coup de Grace** finisher; **Fatebound**'s
**Hand of Fate → Lucky Coin** chain is a passive coin-flip that adds no button.
Both slot into the same core spec shell.

**Playstyle:** keep **Roll the Bones** and **Slice and Dice** rolling, keep
**Adrenaline Rush** and **Blade Flurry** up, then loop builder → finisher while
**Restless Blades** (passive) refunds cooldowns for every combo point spent —
so spending finishers *is* your cooldown-reduction engine. Opportunity procs
turn Pistol Shot into a free empowered builder.

> **Midnight rework flags:** **Roll the Bones** changed from a random-buff slot
> machine to a deterministic **staged buff (stages 1–4)** — see the table.
> **Killing Spree** is now used as a high-combo-point finisher in the APL rather
> than a standalone burst channel. Old Underhanded/Crackshot Adrenaline-Rush-
> extension play was removed. @verify-ingame (exact energy costs and whether
> Killing Spree consumes combo points)

## Inventory

> **Tier-1 floor.** `ability-inventory.tsv` beside this file is authoritative for
> name, spellID, origin and cooldown; where it and the prose below disagree, it
> wins. What is here is the judgement layer — function, role, rotational context.
> Notation (`[T1]` vs `~`), the charge-cooldown caveat and the section-3/4
> pointers: **`../../_abilities/prose-conventions.md`**.

**Energy costs** below reflect commonly-cited Midnight values and are **not** readable
from DB2 — they stay approximate; **verify in-game** (Restless Blades and haste also
shorten most listed cooldowns dynamically). @verify-ingame (energy costs)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Sinister Strike | Rotational-builder | ~45 Energy, +1 CP | Instant / — | Bread-and-butter builder. Can strike twice / proc **Opportunity** (free Pistol Shot); Roll the Bones stage 2 gives it a bonus combo point. |
| Ambush | Rotational-builder | ~50 Energy, +CP | Instant / — | Stealth/Vanish opener; hits harder and gives more CP than Sinister Strike. With **Hidden Opportunity / Audacity** it becomes usable outside stealth on proc. |
| Pistol Shot | Rotational-builder | 25 Energy (free w/ Opportunity), +1 CP | Instant / — | Ranged builder. **Opportunity** procs make it free and empowered; **Fan the Hammer** fires extra shots for extra combo points. |
| Dispatch | Rotational-spender (finisher) | ~35 Energy, spends CP | Instant / — | Primary single-target finisher — highest direct damage per combo point. |
| Between the Eyes | Rotational-spender (finisher) | ~25 Energy, spends CP | Instant / **45s** `[T1]` | Ranged finisher; applies **Ruthless Precision** stacking crit/damage buff (each cast its own duration, can stack). Stuns in PvP. **Gravedigger** empowers it. Cooldown cut by Restless Blades. |
| Roll the Bones | Rotational-spender (buff) | spends CP | Instant / **45s** `[T1]` | **Midnight staged rework:** applies/advances a combat buff by stage — **1:** ↑Opportunity proc chance · **2:** Sinister Strike gives +1 CP · **3:** stronger Restless Blades · **4:** ↑Critical Strike. Reroll to climb stages; **Loaded Dice** guarantees a higher roll. @verify-ingame |
| Slice and Dice | Rotational-spender (buff) | spends CP | Instant / — | Self haste buff. Maintained in **Improved Adrenaline Rush** builds (pre-cast in the opener). |
| Keep It Rolling | Major cooldown | — | Instant / ~6min (Restless Blades ≈1min effective) | Extends **all** active Roll the Bones buffs by 30s — used to bank a strong (stage 3+) roll. |
| Adrenaline Rush | Major cooldown | — | Instant / 3min | Signature DPS cooldown: big energy-regen + attack-speed boost (~20s). Cut heavily by Restless Blades (~40% uptime). |
| Blade Flurry | Rotational (cleave) / offensive CD | Energy | Instant / 30s (12s duration) | Echoes a share of single-target damage onto nearby enemies — the core AoE engine. **Deft Maneuvers** lets it also build combo points at 3+ targets. |
| Blade Rush | Movement / rotational CD | — (grants energy) | Instant / **60s** `[T1]` | Charge to target dealing AoE and briefly boosting energy regen; gap-closer used near on-cooldown. Cut by Restless Blades. |
| Killing Spree | Major cooldown (finisher) | high CP | Channel ~2s / **180s** | **Tier-1 origin: `talent-active`** (spell 51690), base cooldown **180s** — *not* the ~60s this file previously carried from Tier 3. (Restless Blades reduces it in play; see its row.) Teleporting flurry of strikes across targets; APL fires it at high combo points as a finisher-tier burst. |
| Coup de Grace | Rotational (Trickster) | — | Instant / — | **Trickster** capstone (via Unseen Blade / Disorienting Strikes) — an empowered strike used in both builder and finisher windows when guaranteed. |
| Gravedigger | Passive (spec apex) | — | — | Apex talent: Between the Eyes gains a double-stack chance, Dispatch procs bonus damage at high CP, and a bullet-stack system grants free high-impact Between the Eyes. |
| Restless Blades | Passive (core) — `SpecializationSpells` → Outlaw | — | — | Each combo point spent by a finisher reduces the cooldown of Adrenaline Rush, Between the Eyes, Blade Flurry, Blade Rush, Killing Spree, Keep It Rolling, Vanish, Sprint and Grappling Hook. **Absent from `ability-inventory.tsv` by generator design, not by removal** — spell 79096 is Tier-1 attached to Outlaw but passive, and the generator drops passive `SpecializationSpells` rows (`_abilities/reconcile-ledger.md` §5 G1). It is carried in `../../_abilities/section-3-corroborated.md`, confirmed live by `GET /data/wow/spell/79096` → 200. Do not "correct" this row away. |
| Opportunity | Passive (proc) | — | — | Sinister Strike can proc a free, empowered Pistol Shot; central to the builder loop. |
| Preparation | Major cooldown (reset) | — | Instant / **240s** `[T1]` | Resets the cooldown of Adrenaline Rush, Between the Eyes, Blade Flurry, Blade Rush and Killing Spree — press once all are down. |
| Vanish | Utility / stealth (defensive) | — | Instant / ~2min | Enter Stealth mid-combat, drop threat. Hidden Opportunity builds use it for an extra empowered Ambush. |
| Stealth | Utility (stealth) | — | Instant / — | Out-of-combat stealth; enables openers (Ambush / Cheap Shot / Sap). |
| Crimson Vial | Defensive (self-heal) | ~20 Energy | Instant / 30s | Heal-over-time on self; the spammable panic heal. |
| Evasion | Defensive | — | Instant / ~2min | Large dodge boost vs melee/ranged for its duration. |
| Feint | Defensive | 35 Energy | Instant / — | Reduces AoE damage taken (and threat); pressed pre-emptively for big raid hits. |
| Cloak of Shadows | Defensive (magic immunity) | — | Instant / ~2min | Removes and briefly grants immunity to magic effects/debuffs. |
| Thistle Tea | Defensive / resource | — | Instant / (charges) | Restores a chunk of energy and boosts Mastery; energy-panic + small throughput. |
| Kick | Interrupt | — | Instant / 15s | Melee interrupt. |
| Kidney Shot | CC (stun) | spends CP | Instant / **30s** `[T1]` | Combo-point finisher stun. |
| Cheap Shot | CC (stun) | 40 Energy, +CP | Instant / — | Stealth-opener stun. |
| Gouge | CC (incapacitate) | ~25 Energy | Instant / **25s** `[T1]` | Frontal incapacitate (choice node with Airborne Irritant). |
| Blind | CC (disorient) | — | Instant / ~2min | Disorients the target. |
| Sap | CC (out-of-combat) | — | Instant / — | Incapacitate a non-combat target from stealth. |
| Sprint | Movement | — | Instant / **120s** `[T1]` | Burst of movement speed. |
| Grappling Hook | Movement | — | Instant / see tsv | **Tier-1 origin: `class-baseline`** (spell 195457, `SpecializationSpells` → **Outlaw**) — it is an Outlaw-only spell, not a shared Rogue button and not a PvP talent (it is absent from `PvpTalent` entirely). Pull yourself to a location; core Outlaw mobility, and one of the cooldowns Restless Blades refunds. Read the cooldown from the tsv — its `0.8` there is the GCD, not the recharge. |
| Shroud of Concealment | Utility (group stealth) | — | Instant / **360s** `[T1]` | Cloaks the party/raid in stealth for skips. |
| Tricks of the Trade | Utility (threat) | — | Instant / **30s** `[T1]` | Redirects your threat to a party member (choice node with Blackjack). |
| Distract | Utility | — | Instant / 30s | Diverts NPC attention to a location. |
| Shiv | Utility / dispel | ~20 Energy | Instant / CD | Applies nonlethal poison effect; can strip enrages / enable poison utility. |
| Deadly Poison | Weapon imbue (lethal) — `class-baseline` | — | Cast out of combat | Default lethal imbue; stacking nature damage once applied. |
| Instant Poison | Weapon imbue (lethal) — `class-baseline` | — | Cast out of combat | Non-stacking direct-damage lethal imbue. |
| Wound Poison | Weapon imbue (lethal) — `class-baseline` | — | Cast out of combat | Lethal imbue that reduces target healing; mostly PvP/utility. |
| Crippling Poison | Weapon imbue (non-lethal) — `class-baseline` | — | Cast out of combat | Non-lethal slow — the kiting pick. |
| Numbing Poison | Weapon imbue (non-lethal) — `talent-choice` | — | Cast out of combat | Non-lethal; reduces target attack/cast speed. Choice node with Atrophic Poison. |
| Atrophic Poison | Weapon imbue (non-lethal) — `talent-choice` | — | Cast out of combat | Non-lethal; reduces target damage dealt. Choice node with Numbing Poison. |

> **`Poisons` is not a spell.** There is no ability of that name at 12.0.7.67808 — the
> single catch-all row this file used to carry has been split into the six concrete
> imbues above, each with its own Tier-1 origin. *[Tier 1: `ability-inventory.tsv`,
> DB2 @ 12.0.7.67808.]*

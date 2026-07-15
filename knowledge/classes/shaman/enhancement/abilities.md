---
title: Enhancement Shaman — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://wago.tools/db2 SpellName @ 12.0.7 (Blizzard game data, Tier 1 — canonical names/IDs)  # tier 1, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Shaman_Enhancement.simc  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/enhancement-shaman/playstyle-and-rotation  # tier 3, 12.0.7 upd. 2026-06-16, 2026-07-11
  - https://www.icy-veins.com/wow/enhancement-shaman-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - knowledge/classes/shaman/enhancement/talents.md  # sibling tier-1 talent inventory
confidence: high
---

# Enhancement Shaman — Ability Inventory (Midnight S1)

## Overview

Enhancement is the melee-caster hybrid: you weave instant Stormstrike / Lava
Lash / Crash Lightning melee strikes with **Maelstrom Weapon**-empowered
Lightning/Fire spells (Lightning Bolt, Chain Lightning, Tempest, Primordial
Storm). Damage is fast, proc-driven, and swing-timer-aware — you juggle two
weapon imbues, several short-CD strikes, and a bank of Maelstrom Weapon stacks
that you spend "as late as possible without wasting any."

**Resources.** Two: **Mana** (a non-constraint for DPS — only heals/totems cost
it) and **Maelstrom Weapon** (the real economy). Maelstrom Weapon is a **0–10
stack buff** built by melee autos and abilities; at 5+ stacks it makes Lightning
Bolt / Chain Lightning / Tempest / Primordial Storm / Elemental Blast / Healing
Surge / Chain Heal **instant-cast**, and each stack consumed adds ~20% damage
(so 10-stack casts are the payoff). The core loop is: build stacks with strikes,
spend at 9–10 (or 5+ when nothing else to press) into a lightning/fire nuke.
(See `rotation.md` for the priority; `talents.md`/`talents.json` for the tree.)

**Hero trees.** **Stormbringer** (Tempest-centric, lightning burst — flexible,
common in M+) and **Totemic** (Surging Totem + Lava Lash/Sundering, raid-leaning,
spends via **Primordial Storm**). The rotation branches by tree; abilities unique
to one tree are flagged in the tables. (See `builds.md`.)

**Interrupt.** Enhancement has a strong **baseline** kick — **Wind Shear** (12s
CD, ranged), unlike some casters. It also brings a full totem utility kit
(tremor/capacitor/wind rush) and Heroism/Bloodlust.

## Rotational core (strikes, spenders, maintenance)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Stormstrike | Rotational-builder (strike) | — | Instant · ~7.5s recharge, 2 charges | Primary instant melee strike; builds Maelstrom Weapon and does big physical/nature burst, especially inside Doom Winds. Recharge reduced by Elemental Tempo when you spend Maelstrom. Becomes **Windstrike** during Ascendance. @verify-ingame (exact charges/recharge in 12.0.7) |
| Lava Lash | Rotational-builder (strike) | — | Instant · ~18s recharge (hasted) | Fire melee strike; hugely amplified by **Hot Hand** procs (near-free during Doom Winds/Surging Totem for Totemic) and by Lashing Flames. Core Totemic builder. @verify-ingame (recharge in 12.0.7) |
| Crash Lightning | Rotational-builder / AoE buff | — | Instant · ~9s CD (hasted) | Frontal cone strike; applies the **Crash Lightning buff** (empowers Stormstrike/Lava Lash cleave). Kept up in ST, spammed in AoE; central to the Storm Unleashed apex loop. @verify-ingame (CD in 12.0.7) |
| Voltaic Blaze | Rotational-builder / Flame Shock refresh (talent) | Maelstrom-adjacent proc | Instant · proc/charge-gated | Fire nova-style button that **applies/refreshes Flame Shock** and builds Maelstrom Weapon — used to keep Flame Shock up without hard-casting it. Midnight-relevant Enhance ability (spell 470057). @verify-ingame (exact trigger/cost) |
| Flame Shock | Rotational-builder (DoT) | Mana | Instant · no CD | Maintained Fire DoT — the trigger for Lashing Flames / Hot Hand / Molten Assault synergies and Lightning Rod funnel. Usually kept up via Voltaic Blaze rather than hard-cast. |
| Lightning Bolt | Rotational-spender (Maelstrom) | Maelstrom Weapon | Instant at 5+ stacks (else ~2s cast) | Single-target Maelstrom spender; instant + ~20%/stack when consuming stacks. The default ST spender for Stormbringer at 10 stacks. |
| Chain Lightning | Rotational-spender (AoE Maelstrom) | Maelstrom Weapon | Instant at 5+ stacks (else ~2s cast) | Multi-target Maelstrom spender — **replaces Lightning Bolt at 2+ targets**. Hits up to 3+ (more with talents); primary AoE spender. |
| Tempest | Rotational-spender (Stormbringer) | Maelstrom Weapon | Instant (Maelstrom) · charge/proc-built | **Stormbringer** hero spender — a "massive nuke" replacing a Lightning Bolt/Chain Lightning cast, charged by casting Maelstrom spenders. Spend at 10 stacks. |
| Primordial Storm | Rotational-spender (Totemic) | Maelstrom Weapon | Instant (Maelstrom) · proc-gated | **Totemic** hero spender — big fire/lightning strike consumed at 10 Maelstrom (or when the buff is about to expire at 5+). Replaces the lightning nuke in the Totemic loop. |
| Elemental Blast | Rotational-spender (talent, optional) | Maelstrom Weapon | Instant at 5+ stacks | Optional hard-hitting Maelstrom spender that also grants a random secondary-stat buff; build-dependent alternative/supplement to Lightning Bolt. @verify-ingame (talented in the S1 build?) |
| Windstrike | Rotational-builder (Ascendance form) | — | Instant · Ascendance only | Stormstrike **transforms into Windstrike** during Ascendance — no CD, spammable, and (with Thorim's Invocation) auto-fires a Maelstrom spender. |
| Sundering | Rotational-builder / burst | — | Instant · ~40s CD | Slams the ground in a line for heavy up-front damage + a brief incapacitate; a burst button lined up with Doom Winds/Surging Totem. @verify-ingame (CD in 12.0.7 — sources vary 30–40s) |
| Surging Totem | Major cooldown / builder (Totemic) | Mana | Instant · ~60s CD | **Totemic** hero totem — pulses AoE damage, enables Hot Hand/Lava Lash synergy, and is the pivot the Totemic burst window is built around. |

## Weapon imbues & self-buffs (maintained)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Windfury Weapon | Passive buff (imbue) | Mana | ~instant · no CD | Main-hand imbue — melee autos get a chance to trigger extra Windfury attacks (amplified by Doom Winds). Maintained out of combat; a core DPS enabler. |
| Flametongue Weapon | Passive buff (imbue) | Mana | ~instant · no CD | Off-hand imbue — adds Fire damage to autos and feeds fire synergies. Maintained alongside Windfury Weapon. |
| Lightning Shield | Passive buff (self) | Mana | Instant · no CD | Maintained self-buff that adds Nature damage/procs on being hit and to some abilities; part of the precombat setup. |
| Skyfury | Utility (group buff) | Mana | Instant · no CD | The Shaman **party/raid buff** (Mastery + a bonus on melee/ranged) — cast once, maintained. Provides the class's group contribution. @verify-ingame (exact bonus in 12.0.7) |

## Major cooldowns

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Doom Winds | Major cooldown | — | Instant · ~60s CD | Primary 1-min burst: hugely raises Windfury proc chance and pulses damage, spiking Maelstrom generation (Static Accumulation) and enabling Hot Hand. Sync trinkets/potion/racials to it. **Replaced by Ascendance** if that talent is taken (then the burst is on a 2-min cadence). |
| Ascendance | Major cooldown | — | Instant · ~120s CD (or proc via Deeply Rooted Elements) | Transforms Stormstrike into **Windstrike** and turbo-charges the burst window; with Thorim's Invocation it auto-fires Maelstrom spenders. As an active talent it replaces Doom Winds' slot; **Deeply Rooted Elements** instead makes it a random proc. |
| Feral Spirit | Major cooldown / pet (talent) | — | Instant · ~for-duration | Summons spirit wolves that attack and buff you (Maelstrom generation / haste via talents). In the Midnight tree it appears as a passive-granted summon tied to the burst loop. @verify-ingame (active vs passive trigger in 12.0.7) |
| Heroism / Bloodlust | Major cooldown (group) | Mana | Instant · 5 min CD | Raid-wide **+30% haste for 40s** (Bloodlust Horde / Heroism Alliance visual). Sated debuff prevents reuse. The Shaman's signature group cooldown. |

## Defensives & self-sustain

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Astral Shift | Defensive (DR) | — | Instant · ~90s CD | Reduces damage taken for a short window — the main active defensive. Midnight left Enhance thin defensively (Stone Bulwark Totem was removed), so this is the primary planned mitigation. @verify-ingame (exact % / duration post-Midnight) |
| Earth Elemental | Defensive / pet | Mana | Instant · ~5 min CD | Summons a tanky earth elemental to soak/taunt — an emergency threat/defensive tool; **nerfed in Midnight**. @verify-ingame (current health/taunt behavior) |
| Healing Surge | Defensive / heal | Mana (instant w/ Maelstrom) | Instant at 5+ Maelstrom (else ~2s) | Big single-target heal — **instant when you spend Maelstrom Weapon**, so it doubles as an emergency self-heal you can weave into the rotation. |
| Chain Heal | Heal (Maelstrom) | Mana (instant w/ Maelstrom) | Instant at 5+ Maelstrom (else ~2.5s) | Smart multi-target heal; also instant off Maelstrom. Off-role utility for group sustain. |
| Healing Stream Totem | Heal (totem) | Mana | Instant · ~30s CD | Drops a totem that trickle-heals the lowest party member — passive sustain you can set and forget. |
| Earth Shield | Defensive (buff) | Mana | Instant · charge-based | Places absorb/heal-on-hit charges on a target (self via Elemental Orbit talent) — reduces damage taken and heals when struck. |
| Nature's Swiftness | Utility (empower) | — | Instant · ~1 min CD | Makes your next Nature spell (typically Healing Surge) **instant** — an emergency instant heal enabler. @verify-ingame (CD/interaction in 12.0.7) |

## Movement

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Ghost Wolf | Movement | Mana | Instant · no CD | Wolf form — travel speed increase; core mobility toggle (Spirit Wolf/Thunderous Paws talents add DR/snare-break). |
| Spirit Walk | Movement | — | Instant · ~60s CD | Removes movement-impairing effects and grants a burst of speed — the reposition/escape button (choice vs Gust of Wind). |
| Feral Lunge | Movement (gap-closer) | — | Instant · ~30s CD | Leaps to a target and strikes — the melee gap-closer. @verify-ingame (CD in 12.0.7) |
| Totemic Projection | Utility (relocate totems) | — | Instant · short CD | Instantly relocates your active totems to a new spot — repositions Surging/utility totems without recasting. @verify-ingame (CD) |

## Crowd control & interrupt

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Wind Shear | **Interrupt** | — | Instant · **12s CD**, ranged | Baseline kick — short CD and ranged, one of the better interrupts in the game. Enhance's dedicated interrupt (no pet needed). @verify-ingame (exact CD in 12.0.7) |
| Hex | CC (single) | Mana | ~1.5s cast · ~30s CD | Polymorph-style transform of a single target (breaks on damage). Primary hard CC. @verify-ingame (CD) |
| Capacitor Totem | CC (AoE stun) | Mana | Instant · ~60s CD | Totem that stuns nearby enemies after a ~3s charge — AoE stop (Static Charge talent lowers CD per target hit). |
| Earthgrab Totem | CC (AoE root) | Mana | Instant · ~30s CD | Roots enemies near the totem, then snares — AoE control/kite tool. @verify-ingame (CD) |
| Tremor Totem | Utility / CC-break | Mana | Instant · ~60s CD | Breaks and prevents fear/sleep/charm for the party — anti-CC totem (choice vs Poison Cleansing Totem). |
| Thunderstorm | CC (knockback) | Mana | Instant · ~30–45s CD | Knocks back nearby enemies and slows them — a peel/reposition tool. @verify-ingame (CD / whether baseline for Enhance) |
| Frost Shock | Utility / slow | Mana | Instant · no CD | Ranged Frost hit that snares the target — a cheap slow/range filler. |
| Capacitor/Earthgrab/Tremor/Wind Rush | Utility totems | Mana | see rows | The totem utility suite — drop-and-forget group tools. |

## Utility & totems

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Wind Rush Totem | Utility (group speed) | Mana | Instant · ~2 min CD | Totem that repeatedly grants nearby allies a movement-speed burst — group mobility (skips, mechanics). @verify-ingame (CD) |
| Purge | Dispel (offensive) | Mana | Instant · no CD | Removes a beneficial magic effect (and enrage-adjacent) from an enemy — offensive dispel (Greater Purge choice removes two). |
| Cleanse Spirit | Dispel (friendly) | Mana | Instant · ~8s CD | Removes a Curse from a friendly target (talent). Party dispel utility. @verify-ingame (CD / school in 12.0.7) |
| Ancestral Spirit | Utility (res) | Mana | ~10s cast · no CD | Out-of-combat resurrection. |
| Ghost Wolf / Spirit Walk / Feral Lunge | Movement | — | see Movement | Listed above. |

## Notable passives (context for the buttons above)

- **Maelstrom Weapon** — the resource: melee autos/abilities build 0–10 stacks
  that make Lightning Bolt / Chain Lightning / Tempest / Primordial Storm /
  Elemental Blast (and heals) instant and empowered. Drives the entire "build
  with strikes, spend the bank" gameplan.
- **Hot Hand** — Flame Shock ticks (with active Flame Shock) proc a big **Lava
  Lash** empowerment and recharge. Reworked in Midnight to give *less* CD
  reduction unless Elemental Tempo is talented (two GCDs between Lava Lashes
  instead of one). Core to the Totemic loop.
- **Elemental Tempo** — **spending Maelstrom Weapon refunds Stormstrike/Lava
  Lash cooldown**, which is why you hold spenders to 9–10 stacks rather than
  dumping at 5.
- **Static Accumulation** — Doom Winds/burst windows passively pour Maelstrom
  Weapon stacks in, accelerating the spend loop during cooldowns.
- **Thorim's Invocation** — during Ascendance/burst, **Windstrike auto-fires a
  Maelstrom spender** (Lightning Bolt/Chain Lightning), so the burst window
  spends for you.
- **Storm Unleashed** (spec apex) — first point buffs Crash Lightning stacking
  and gives a per-Maelstrom-spent chance to reset Crash Lightning; further
  points add damage and auto-attack-speed scaling.
- **Deeply Rooted Elements** vs **Ascendance** (choice) — DRE makes Ascendance a
  random proc off spender casts; taking Ascendance as an active turns Doom Winds
  into a 2-min burst instead.

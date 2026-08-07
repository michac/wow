---
title: Enhancement Shaman — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/shaman/enhancement/ability-inventory.tsv  # tier 1, generated from DB2 @ 12.0.7.67808 — name/spellID/origin/cooldown source of record
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the 12.0.7.67808 adjudication behind this pass
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
Bolt / Chain Lightning / Tempest / Primordial Storm / Healing Surge / Chain
Heal **instant-cast**, and each stack consumed adds ~20% damage
(so 10-stack casts are the payoff). The core loop is: build stacks with strikes,
spend at 9–10 (or 5+ when nothing else to press) into a lightning/fire nuke.
(See `rotation.md` for the priority; `talents.md`/`talents.json` for the tree.)

**Hero trees.** `builds.md` owns the pick. In kit terms: **Stormbringer** adds
periodic **Tempest** procs; **Totemic** adds **Surging Totem** and spends
Maelstrom via **Primordial Storm**. The rotation branches by tree; abilities
unique to one tree are flagged in the tables.

**Interrupt.** Enhancement has a strong kick — **Wind Shear** (12s CD, ranged), unlike
some casters. It is a **class-tree talent**, not baseline (Tier 1 origin `talent-active`),
so a build has to actually take it. It also brings a full totem utility kit
(tremor/capacitor/wind rush) and Heroism/Bloodlust.

## Rotational core (strikes, spenders, maintenance)

> **Tier-1 floor.** `ability-inventory.tsv` beside this file is authoritative for
> name, spellID, origin and cooldown; where it and the prose below disagree, it
> wins. What is here is the judgement layer — function, role, rotational context.
> Notation (`[T1]` vs `~`), the charge-cooldown caveat and the section-3/4
> pointers: **`../../_abilities/prose-conventions.md`**.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Stormstrike | Rotational-builder (strike) | — | Instant · ~7.5s recharge, 2 charges | Primary instant melee strike; builds Maelstrom Weapon and does big physical/nature burst, especially inside Doom Winds. Recharge reduced by Elemental Tempo when you spend Maelstrom. Becomes **Windstrike** during Ascendance. @verify-ingame (exact charges/recharge in 12.0.7) |
| Lava Lash | Rotational-builder (strike) | — | Instant · **18s** (hasted) | **Tier-1 origin: `talent-active`** (spell 60103, class tree), cooldown **18s** — the file's earlier "~18s" was right. Fire melee strike; hugely amplified by **Hot Hand** procs (near-free during Doom Winds/Surging Totem for Totemic) and by Lashing Flames. Core Totemic builder. |
| Crash Lightning | Rotational-builder / AoE buff | — | Instant · ~9s CD (hasted) | Frontal cone strike; applies the **Crash Lightning buff** (empowers Stormstrike/Lava Lash cleave). Kept up in ST, spammed in AoE; central to the Storm Unleashed apex loop. @verify-ingame (CD in 12.0.7) |
| Voltaic Blaze | Rotational-builder / Flame Shock refresh (talent) | Maelstrom-adjacent proc | Instant · proc/charge-gated | Fire nova-style button that **applies/refreshes Flame Shock** and builds Maelstrom Weapon — used to keep Flame Shock up without hard-casting it. Midnight-relevant Enhance ability (spell 470057). @verify-ingame (exact trigger/cost) |
| Flame Shock | Rotational-builder (DoT) | Mana | Instant · no CD | Maintained Fire DoT — the trigger for Lashing Flames / Hot Hand / Molten Assault synergies and Lightning Rod funnel. Usually kept up via Voltaic Blaze rather than hard-cast. |
| Lightning Bolt | Rotational-spender (Maelstrom) | Maelstrom Weapon | Instant at 5+ stacks (else ~2s cast) | Single-target Maelstrom spender; instant + ~20%/stack when consuming stacks. The default ST spender for Stormbringer at 10 stacks. |
| Chain Lightning | Rotational-spender (AoE Maelstrom) | Maelstrom Weapon | Instant at 5+ stacks (else ~2s cast) | Multi-target Maelstrom spender — **replaces Lightning Bolt at 2+ targets**. Hits up to 3+ (more with talents); primary AoE spender. |
| Tempest | Rotational-spender (Stormbringer) | Maelstrom Weapon | Instant (Maelstrom) · charge/proc-built | **Stormbringer** hero spender — a "massive nuke" replacing a Lightning Bolt/Chain Lightning cast, charged by casting Maelstrom spenders. Spend at 10 stacks. |
| Primordial Storm | Rotational-spender (Totemic) | Maelstrom Weapon | Instant (Maelstrom) · proc-gated | **Totemic** hero spender — big fire/lightning strike consumed at 10 Maelstrom (or when the buff is about to expire at 5+). Replaces the lightning nuke in the Totemic loop. |
| Windstrike | Rotational-builder (Ascendance form) | — | Instant · Ascendance only | Stormstrike **transforms into Windstrike** during Ascendance — no CD, spammable, and (with Thorim's Invocation) auto-fires a Maelstrom spender. |
| Sundering | Rotational-builder / burst | — | Instant · **30s** | **Tier-1 origin: `talent-active`** (spell 197214, spec tree), cooldown **30s** — the Tier-3 guides that said 40s are wrong; the low end of the 30–40s spread this file used to hedge over is the measured value. Slams the ground in a line for heavy up-front damage + a brief incapacitate; a burst button lined up with Doom Winds/Surging Totem. |
| Surging Totem | Major cooldown / builder (Totemic) | Mana | Instant / **25s** `[T1]` | **Totemic** hero totem — pulses AoE damage, enables Hot Hand/Lava Lash synergy, and is the pivot the Totemic burst window is built around. |

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
| Ascendance | Major cooldown | — | Instant / **180s** `[T1]` (or proc via Deeply Rooted Elements) | Transforms Stormstrike into **Windstrike** and turbo-charges the burst window; with Thorim's Invocation it auto-fires Maelstrom spenders. As an active talent it replaces Doom Winds' slot; **Deeply Rooted Elements** instead makes it a random proc. |
| Feral Spirit | Major cooldown / pet (talent) | — | Instant · ~for-duration | Summons spirit wolves that attack and buff you (Maelstrom generation / haste via talents). In the Midnight tree it appears as a passive-granted summon tied to the burst loop. @verify-ingame (active vs passive trigger in 12.0.7) |
| Heroism / Bloodlust | Major cooldown (group) | Mana | Instant · 5 min CD | Raid-wide **+30% haste for 40s** (Bloodlust Horde / Heroism Alliance visual). Sated debuff prevents reuse. The Shaman's signature group cooldown. |

## Defensives & self-sustain

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Astral Shift | Defensive (DR) | — | Instant · **120s** | **Tier-1 origin: `talent-active`** (spell 108271, class tree), cooldown **120s** — not the ~90s this file previously carried from Tier 3. The main active defensive; Midnight left Enhance thin defensively (Stone Bulwark Totem was removed), so this is the primary planned mitigation. Its damage-reduction **percentage and duration are not readable from DB2** — treat any number for those as Tier 3 until someone reads a tooltip. |
| Earth Elemental | Defensive / pet | Mana | Instant · **180s** | **Tier-1 origin: `talent-active`** (spell 198103, class tree), cooldown **180s** — not the ~5 min this file previously carried. Summons a tanky earth elemental to soak/taunt — an emergency threat/defensive tool. Its health and taunt behaviour are not readable from DB2. |
| Healing Surge | Defensive / heal | Mana (instant w/ Maelstrom) | Instant at 5+ Maelstrom (else ~2s) | Big single-target heal — **instant when you spend Maelstrom Weapon**, so it doubles as an emergency self-heal you can weave into the rotation. |
| Chain Heal | Heal (Maelstrom) | Mana (instant w/ Maelstrom) | Instant at 5+ Maelstrom (else ~2.5s) | Smart multi-target heal; also instant off Maelstrom. Off-role utility for group sustain. |
| Healing Stream Totem | Heal (totem) | Mana | Instant · ~30s CD | Drops a totem that trickle-heals the lowest party member — passive sustain you can set and forget. |
| Earth Shield | Defensive (buff) | Mana | Instant · charge-based | Places absorb/heal-on-hit charges on a target (self via Elemental Orbit talent) — reduces damage taken and heals when struck. |
| Nature's Swiftness | Utility (empower) | — | Instant · **60s** | **Tier-1 origin: `talent-active`** (spell 378081, class tree), cooldown **60s**. Makes your next Nature spell (typically Healing Surge) **instant** — an emergency instant heal enabler. |

## Movement

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Ghost Wolf | Movement | Mana | Instant · no CD | Wolf form — travel speed increase; core mobility toggle (Spirit Wolf/Thunderous Paws talents add DR/snare-break). |
| Spirit Walk | Movement | — | Instant · ~60s CD | Removes movement-impairing effects and grants a burst of speed — the reposition/escape button (choice vs Gust of Wind). |
| Feral Lunge | Movement (gap-closer) | — | Instant · **30s** | **Tier-1 origin: `class-baseline`** (spell 196884, `SpecializationSpells` → Enhancement — spec-defining, not a talent pick), cooldown **30s**. Leaps to a target and strikes — the melee gap-closer. |
| Totemic Projection | Utility (relocate totems) | — | Instant · **10s** | **Tier-1 origin: `talent-active`** (spell 108287, class tree), cooldown **10s**. Instantly relocates your active totems to a new spot — repositions Surging/utility totems without recasting. |

## Crowd control & interrupt

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Wind Shear | **Interrupt** | — | Instant · **12s**, ranged | **Tier-1 origin: `talent-active`** (spell 57994, class tree), cooldown **12s** — a **talent, not baseline**, which this file previously got wrong; a build that skips the node has no kick. Short CD and ranged, one of the better interrupts in the game (no pet needed). |
| Hex | CC (single) | Mana | ~1.5s cast · **30s** | **Tier-1 origin: `talent-active`** (spell 51514, class tree; also reachable as `class-baseline` via `SkillLineAbility` 924), cooldown **30s**. Polymorph-style transform of a single target (breaks on damage). Primary hard CC. |
| Capacitor Totem | CC (AoE stun) | Mana | Instant · **60s** | **Tier-1 origin: `talent-active`** (spell 192058, class tree), cooldown **60s**. Totem that stuns nearby enemies after a ~3s charge — AoE stop (Static Charge talent lowers CD per target hit). |
| Earthgrab Totem | CC (AoE root) | Mana | Instant · **30s** | **Tier-1 origin: `talent-active`** (spell 51485, class tree), cooldown **30s**. Roots enemies near the totem, then snares — AoE control/kite tool. |
| Tremor Totem | Utility / CC-break | Mana | Instant · **60s** | **Tier-1 origin: `talent-choice`** (spell 8143, class tree — the choice node with Poison Cleansing Totem), cooldown **60s**. Breaks and prevents fear/sleep/charm for the party. |
| Frost Shock | Utility / slow | Mana | Instant · no CD | Ranged Frost hit that snares the target — a cheap slow/range filler. |

## Utility & totems

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Wind Rush Totem | Utility (group speed) | Mana | Instant · **120s** | **Tier-1 origin: `talent-active`** (spell 192077, class tree), cooldown **120s**. Totem that repeatedly grants nearby allies a movement-speed burst — group mobility (skips, mechanics). |
| Purge | Dispel (offensive) | Mana | Instant · no CD | Removes a beneficial magic effect (and enrage-adjacent) from an enemy — offensive dispel (Greater Purge choice removes two). |
| Cleanse Spirit | Dispel (friendly) | Mana | Instant · **8s** | **Tier-1 origin: `talent-active`** (spell 51886, class tree), cooldown **8s**. Removes a Curse from a friendly target. Party dispel utility. |
| Ancestral Spirit | Utility (res) | Mana | ~10s cast · no CD | Out-of-combat resurrection. |
| Ghost Wolf / Spirit Walk / Feral Lunge | Movement | — | see Movement | Listed above. |

## Notable passives (context for the buttons above)

- **Maelstrom Weapon** — the resource: melee autos/abilities build 0–10 stacks
  that make Lightning Bolt / Chain Lightning / Tempest / Primordial Storm (and
  heals) instant and empowered. Drives the entire "build with strikes, spend the
  bank" gameplan. (Elemental Blast used to be on this list and is not — see
  "Not on the Midnight Enhancement tree" below.)
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

**Not on the Midnight Enhancement tree:** **Elemental Blast** (117014) is an **Elemental**
spec choice-node talent and appears on no Enhancement tree — class, spec or hero.
*[Tier 1: `all-talents.tsv` @ 12.0.7.67808, all 40 specs.]*

**Not on the Midnight Enhancement tree:** **Thunderstorm** (51490) is
`SpecializationSpells` → **Shaman / Elemental** (class-baseline there, 30s) and belongs in
that spec's file — see `knowledge/classes/shaman/elemental/abilities.md`. It is **absent
from `PvpTalent` entirely**, so the "whether baseline for Enhance" hedge this file used to
carry had no route to a yes: its only trait attachment is the **legacy** Shaman trees
1033/1034, not the live tree 786. Enhancement's Tier-1 crowd-control rows are Capacitor
Totem, Earthgrab Totem, Tremor Totem and Hex — plan peels off those, not off a knockback.
*[Tier 1: DB2 @ 12.0.7.67808, via `_abilities/reconcile-ledger.md`.]*

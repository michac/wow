---
title: Affliction Warlock — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://wago.tools/db2 SpellName @ 12.0.7 (Blizzard game data, Tier 1 — canonical names/IDs)  # tier 1, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1 APL, 2026-07-11
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.wowhead.com/spell=48181/haunt  # tier 4 (exact cast/CD/cost), 2026-07-11
  - https://www.wowhead.com/spell=205180/summon-darkglare  # tier 4, 2026-07-11
  - https://www.wowhead.com/spell=1257052/dark-harvest  # tier 4, 2026-07-11
  - knowledge/classes/warlock/affliction/talents.md  # sibling tier-1 talent inventory
confidence: high
---

# Affliction Warlock — Ability Inventory (Midnight S1)

## Overview

Affliction is the DoT-and-drain Warlock spec: you paint every target with
stacking damage-over-time effects (Agony, Corruption, Unstable Affliction,
Seed of Corruption), amplify them, and let them tick while you channel a
filler. Damage is back-loaded and multi-target-friendly — the strength is
spreading and *snapshotting* DoTs, not bursting one target with hard-casts.

**Resources.** Two: **Mana** (effectively a non-constraint — spell costs are
~2% base mana) and **Soul Shards** (0–5, the real economy). **Agony** ticks are
the steady shard generator (each tick has a chance to award a Soul Shard
Fragment; 10 fragments = 1 shard); **Drain Soul** and **Dark Harvest** add
more. Shards are spent on **Unstable Affliction** (single-target spender) and
**Seed of Corruption** (AoE spender). Overcapping shards is a throughput loss,
so the rotation is a constant generate→spend loop. (See `rotation.md` for the
priority; `talents.md`/`talents.json` for the full tree.)

**Hero trees.** **Soul Harvester** is the live S1 meta for all content (ST,
cleave, AoE) — it adds Demonic Soul stacking off shard spends and recycles
**Dark Harvest**. **Hellcaller** (near-dead in S1) swaps Corruption for
**Wither** and adds **Malevolence** as a 1-min cooldown. Where an ability
belongs to one hero tree it is flagged in the table.

**Interrupt.** Affliction has **no baseline personal interrupt** — its kick is
the **pet's Spell Lock** (Felhunter), which is why Felhunter is the group-content
pet. Plan interrupts around the pet ability, not a self-cast.

## Rotational core (DoTs, builders, spenders, fillers)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Agony | Rotational-builder (DoT) | Mana | Instant · no CD | Stacking Shadow DoT and the spec's steady **Soul Shard generator** (ticks chance to award a fragment). Maintain on all targets, up to ~5 in AoE; ramps in damage as stacks build, so refresh rather than reapply. |
| Corruption | Rotational-builder (DoT) | Mana | Instant · no CD | Maintained Shadow DoT; its ticks feed **Nightfall** procs (empowered instant fillers). Spread to many targets via Seed of Corruption. Replaced by **Wither** under Hellcaller. |
| Unstable Affliction | Rotational-spender (DoT) | **1 Soul Shard** | ~1.5s cast · no CD | Primary **single-target shard spender** — a big single DoT (one instance per target, refreshable). Feeds Soul Harvester's Demonic Soul. Since 12.0.7 consumes only one **Shard Instability** stack per cast. |
| Seed of Corruption | Rotational-spender (AoE) | **1 Soul Shard** | ~2s cast · no CD | Plants a seed that **detonates to apply Corruption** to nearby enemies — the **AoE shard spender** (weaponized by Sow the Seeds / Seeds of Destruction). Don't double-sow a target. |
| Haunt | Rotational-spender (amp debuff) | 2% mana (**no shard**) | 1.5s cast · **15s CD** | Damage-amplification debuff **cast on cooldown**, not just to maintain. Improved Haunt + apex points make it a hard-hitting button; cleaves with talents. |
| Drain Soul | Rotational-filler (channel) | Mana | Channeled · no CD | Default **filler channel**; generates shards and scales in execute. Buffed by **Nightfall** (empowered + ~50% faster). Choice-node vs Improved Shadow Bolt. |
| Shadow Bolt | Rotational-filler | Mana | ~2s cast (instant w/ Nightfall) | Alternative hard-cast filler; **instant and +damage when a Nightfall proc is up**. With the Malefic Grasp talent it **becomes Malefic Grasp while Darkglare is active**. |
| Malefic Grasp | Rotational-filler (channel; talent) | Mana | Channeled | The filler channel used **during Summon Darkglare** — amplifies your DoT ticks while channeled. Enabled by the Malefic Grasp talent (Shadow Bolt transforms into it in the Darkglare window). |
| Shadow of Nathreza | Rotational cooldown (spec apex, active) | Soul Shards | ~instant · CD | Apex spec active — empowers your next spells / DoT burst (top point adds a meteor-style proc). Fit into the Darkglare burst window. @verify-ingame (exact cost/effect) |

## Major cooldowns

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Summon Darkglare | Major cooldown (pet) | 2% mana | Instant · **2 min CD** | Summons the Darkglare, which **extends all your active DoTs** and adds burst — the core burst window. Sync trinkets, potion, and racials to it; cast after Dark Harvest is on CD. |
| Dark Harvest | Major cooldown / builder (channel) | Generates **~3 Soul Shards** | Channeled · **1 min CD** (~40–45s effective w/ Cull the Weak) | Channel that damages scaling with your active DoTs and **refills shards** — cast when **<3 shards** right before Darkglare, so the pair opens the burst window. |
| Malevolence | Major cooldown (Hellcaller only) | — | ~instant · **1 min CD** | Hellcaller hero cooldown — burst that synergizes with the Wither/Darkglare window. Only relevant on the near-dead Hellcaller build. @verify-ingame |

## Curses & applied debuffs (utility / CC)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Curse of Tongues | Utility (debuff) | Mana | Instant · no CD | Slows the target's **cast speed** (class talent). Only one Curse per target at a time. |
| Curse of Exhaustion | Utility / slow | Mana | Instant · no CD | Slows the target's **movement speed** (class talent) — kiting tool. |
| Curse of Weakness | Utility (debuff) | Mana | Instant · no CD | Reduces the target's **physical damage dealt**. @verify-ingame (baseline vs talent availability in 12.0.7) |
| Blight of Weakness | Utility (curse upgrade, DoT) | Mana | Instant · no CD | Choice talent: **Curse of Weakness becomes Blight of Weakness**, adding a damaging/effect component (alt: Blight of Tongues). |

## Defensives & self-sustain

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Unending Resolve | Defensive (DR) | 2% mana | Instant · **3 min CD** | **−25% damage taken for 8s** (−40% with Strength of Will) and immunity to interrupt/silence. Main planned defensive. |
| Dark Pact | Defensive (absorb) | Sacrifices HP | Instant · **1 min CD** (−15s w/ Frequent Donor) | Sacrifices health for a **large absorb (~200%+ of sacrificed HP)**; **usable while CC'd**. Ichor of Devils drops the HP cost to 5%. |
| Drain Life | Defensive / heal (channel) | Mana | Channeled · no CD | Channel that **damages and self-heals** (heals a % of damage done); Soulburn adds an absorb. Emergency sustain, not a rotational filler. |
| Mortal Coil | Defensive / CC | Mana | Instant · **45s CD** | **Horrifies** the target 3s and heals you **20% max HP** (25% w/ Improved Mortal Coil) — panic heal + single-target CC. |
| Healthstone | Defensive (item) | — | Instant · item | Consumes a conjured Healthstone to restore **25% HP** (30% w/ Empowered). **Pact of Gluttony** makes it reusable in combat; Soulburn/Gorebound inflate it. |
| Soulstone | Utility (battle-rez) | Mana | Instant · **10 min CD** | Places a self- or ally-**resurrection** buff (combat rez). Pre-place before pulls. |
| Soulburn | Utility (empower) | **1 Soul Shard** | Instant · no CD | Empowers your **next** Healthstone / Drain Life / Demonic Circle / Demonic Gateway / Fel Domination — the enabler for the `Soulburn → Healthstone → Dark Pact` defensive combo. |

## Movement

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Burning Rush | Movement | **Health drain** | Instant · toggle | Toggle **+50% movement speed** while draining your health each second. Core mobility; watch the HP drain with Soul Leech. |
| Demonic Circle | Movement (place) | Mana | Instant · no CD | Places a teleport anchor on the ground (class talent). |
| Demonic Circle: Teleport | Movement | Mana | Instant · short CD | **Teleports to your placed circle** and breaks snares/roots — the reposition/escape button. |
| Demonic Gateway | Movement / utility (group) | Mana | ~2s cast · CD | Places a **two-portal gateway** the party can click to teleport between two points — big skip/repositioning tool. |
| Fel Domination | Utility (pet) | 2% mana | Instant · **3 min CD** | Makes your next pet summon **instant and free** — fast re-summon after a pet dies. |

## Crowd control

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Fear | CC (single) | Mana | ~1.5s cast · no CD | Fears one target (breaks on damage). Single-target soft CC. |
| Shadowfury | CC (AoE stun) | Mana | Instant · **30s CD** | **Stuns all enemies** in a target area ~3s (choice vs Howl of Terror). AoE stop. |
| Howl of Terror | CC (AoE fear) | 2% mana | Instant · **40s CD** | **Fears nearby enemies** ~8s (choice vs Shadowfury). AoE panic. |
| Banish | CC (single) | Mana | ~1.5s cast · no CD | Banishes a **demon or elemental**, making it untargetable/unable to act. |
| Mortal Coil | CC (single) | Mana | Instant · 45s CD | Also a CC — see Defensives (horror + heal). |

## Pet & interrupt

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Spell Lock | **Interrupt** (Felhunter pet) | — | Instant · **~24s CD** | The Felhunter's interrupt (can also be specced to silence) — **Affliction's only kick**. Commanded via the pet. @verify-ingame (exact CD in 12.0.7) |
| Summon Felhunter | Pet | 2% mana | ~2.5s cast (instant w/ Fel Domination) | Summons the Felhunter — the group-content pet for **Spell Lock + Devour Magic** purge. Other pets (Imp/Voidwalker/Sayaad/Felguard) sim within noise; pick on utility. |
| Subjugate Demon | CC / utility | Mana | ~2.6s cast · no CD | **Enslaves a demon** target for temporary control. Situational world/utility. |
| Grimoire of Sacrifice | Passive / utility (talent) | — | Instant · toggle | Choice vs Summoner's Embrace: **sacrifices your pet** for a personal damage/utility buff (S1 meta keeps the pet out with Summoner's Embrace instead). |

## Notable passives (context for the buttons above)

- **Nightfall** — Corruption ticks build stacks (to 2) that empower the next
  filler *started* while up (instant Shadow Bolt; faster/stronger Drain Soul /
  Malefic Grasp). Drives the "start/restart the channel to consume the proc" rule.
- **Demonic Soul** (Soul Harvester) — shard spends (UA) stack an amp that pays
  off the aggressive spend-to-recycle-Dark-Harvest gameplan.
- **Shard Instability** — banked stacks grant free/discounted UAs; since 12.0.7
  each UA consumes only one stack.
- **Soul Leech** (baseline) — damage grants an absorb shield; **Demon Skin /
  Fel Armor / Fortified Soul** grow and recharge it (passive EHP floor).
</content>

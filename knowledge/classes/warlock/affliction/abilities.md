---
title: Affliction Warlock — Ability Inventory (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes — the Warlock/Affliction class section, 2026-08-11
  - knowledge/_meta/patch-notes/12.1.md  # tier 1 verbatim archive of the above (▶ WARLOCK → Affliction), 2026-08-11
  - knowledge/classes/warlock/affliction/ability-inventory.md  # tier 1, generated @ 12.1.0.69214 — resolved Blizzard API spell descriptions, 2026-08-11
  - knowledge/classes/warlock/affliction/talents.md  # tier 1, generated talent tree @ 12.1.0.68914 — what exists in the tree, 2026-08-11
  - knowledge/classes/warlock/affliction/ability-inventory.tsv  # tier 1, generated DB2 inventory — the name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1, pet skill lines, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1 APL, 2026-07-11
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7-era, 2026-07-11
  - https://www.wowhead.com/spell=48181/haunt  # tier 4 (exact cast/CD/cost), 2026-07-11
confidence: high
---

# Affliction Warlock — Ability Inventory (Midnight 12.1)

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

**Hero trees.** **Soul Harvester** was the Season 1 meta for all content (ST,
cleave, AoE) — it adds Demonic Soul stacking off shard spends and recycles
**Dark Harvest**. **Hellcaller** (near-dead in S1) swaps Corruption for
**Wither** and adds **Malevolence** as a 1-min cooldown; 12.1 handed it a real
buff pass (**Blackened Soul redesigned + damage +45%**, **Wither damage +25%**,
**Mark of Peroth'arn redesigned**), so the S1 verdict is **not** safe to carry
into Season 2. Which tree wins in S2 is **unmeasured as of 2026-08-11** — S2
opens 2026-08-18 and no post-patch sim or log data exists yet. Where an ability
belongs to one hero tree it is flagged in the table.

**Interrupt.** Affliction has **no baseline personal interrupt** — its kick is
the **pet's Spell Lock** (Felhunter), which is why Felhunter is the group-content
pet. Plan interrupts around the pet ability, not a self-cast.

> **Tier-1 floor.** Canonical **name, spellID, acquisition origin and base
> cooldown** for everything below live in `ability-inventory.tsv` / the generated
> `ability-inventory.md` (Blizzard API + wago DB2 @ `12.1.0.69214`), and what
> exists in the tree at all lives in `talents.md` (@ `12.1.0.68914`) — look them
> up there rather than trusting a restated number here. This file exists for
> **function, role and rotational context**; where its prose disagrees with the
> generated siblings, **the generated siblings win**.

> **12.1 game-wide tuning that colours every row below.** Player health **and**
> creature damage were both raised **25%** at max level, with health consumables
> rescaled and a pass over DPS/tank healing + absorb spells to keep their relative
> impact — so any *absolute* HP or healing number from before 2026-08-11 is stale
> (the **percentage-of-max-health** values in this file, e.g. Healthstone 25%,
> Mortal Coil 20%, are not). Major DPS cooldowns were lowered and steady-state
> damage raised across several specs, so burst-vs-sustained splits have moved.
> Interrupts (including the pet's Spell Lock) now show a **"missed" visual and
> sound** when fired at a target that was not casting. **Diminishing-return
> categories now reset after 20s** (was 16) — that lengthens the usable re-CC
> window on Fear / Howl of Terror / Shadowfury / Mortal Coil.

## Rotational core (DoTs, builders, spenders, fillers)

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.1.0.69214).
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
| Agony | Rotational-builder (DoT) | Mana | Instant · no CD | Stacking Shadow DoT and the spec's steady **Soul Shard generator** (ticks chance to award a fragment). Maintain on all targets, up to ~5 in AoE; ramps in damage as stacks build, so refresh rather than reapply. |
| Corruption | Rotational-builder (DoT) | Mana | Instant · no CD | Maintained Shadow DoT; its ticks feed **Nightfall** procs (empowered instant fillers). Spread to many targets via Seed of Corruption. Replaced by **Wither** under Hellcaller. |
| Unstable Affliction | Rotational-spender (DoT) | **1 Soul Shard** | ~1.5s cast · no CD | Primary **single-target shard spender** — a big single DoT; **multiple uses may overlap** on one target *[Tier 1, 12.1]*, so it is not a strict one-instance refresh. Dispelling it damages and silences the dispeller (scaling **+15% per stack**). Feeds Soul Harvester's Demonic Soul. **12.1: now correctly grants Soul Leech**, and a **Shard Instability** proc can make it **free and instant** (see passives). |
| Seed of Corruption | Rotational-spender (AoE) | **1 Soul Shard** | ~2s cast · no CD | Plants a seed that **detonates to apply Corruption** to nearby enemies — the **AoE shard spender** (weaponized by Sow the Seeds / Seeds of Destruction). Don't double-sow a target. **12.1: the free-and-instant Seed now comes from the redesigned Shard Instability**, not from Nightfall — *Nocturnal Yield*, which used to grant it, **was removed** and *Patient Zero* with it. |
| Haunt | Rotational-spender (amp debuff) | 2% mana (**no shard**) | 1.5s cast · **15s CD** `[T1]` | Damage-amplification debuff **cast on cooldown**, not just to maintain: **+16% damage dealt to the target for 18s** *(12.1 buff — was 12%)*. Its **cooldown resets if the target dies** *[Tier 1]*. Improved Haunt (+35% damage, −0.3s cast) and the apex point make it a hard-hitting button. **12.1 raises its rotational weight further** — Impetuous Wrath pays **+20% instead of +10%** on Shadow Bolt / Drain Soul / Malefic Grasp / Dark Harvest **while the target is Haunted**, so Haunt uptime now gates filler damage, not just DoT damage. |
| Drain Soul | Rotational-filler (channel) | Mana | Channeled · no CD | Default **filler channel** (**replaces Shadow Bolt** when taken); generates shards and **+100% damage below 20% health**. Buffed by **Nightfall** and by **Impetuous Wrath** (+10%, **+20% on a Haunted target**). **12.1: its damage is one of the two rolls for Shard Instability's free-and-instant spender proc.** Choice-node vs Improved Shadow Bolt. |
| Shadow Bolt | Rotational-filler | Mana | ~2s cast (instant w/ Nightfall) | **Class-baseline, not a talent** — you always have it *[Tier 1]*; the choice node is over *Improved Shadow Bolt*, which only tunes it. Alternative hard-cast filler; **instant and +25% damage when a Nightfall proc is up** *[Tier 1, 12.1]*. Also buffed by **Impetuous Wrath** (+10% / **+20% on a Haunted target**) and is the other roll for **Shard Instability**. With the Malefic Grasp talent it **becomes Malefic Grasp while Darkglare is active**. |
| Malefic Grasp | Rotational-filler (channel; talent) | Mana | Channeled | The filler channel used **during Summon Darkglare** — Shadow Bolt transforms into it in the Darkglare window. **12.1: now correctly grants Soul Leech**, and it takes **Impetuous Wrath**'s +10% / **+20% on a Haunted target**. **Nightfall** makes it channel **50% faster** for +25% damage. |
| Shadow of Nathreza | Spec apex (Haunt modifier) | — | passive | Apex spec point — **Haunt now calls a demonic soul** that deals Shadow damage to its host **and to 3 nearby enemies afflicted by your Corruption** over its duration *[Tier 1, 12.1]*, i.e. it turns Haunt into cleave rather than adding a button. ⚠ The two generated siblings disagree on its kind: `talents.md` types it **ACTIVE**, `ability-inventory.md` types it **talent-passive**, and the resolved 12.1 description is passive-shaped. @verify-ingame (does it appear as a castable button, or purely as a Haunt modifier?) |

## Major cooldowns

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Summon Darkglare | Major cooldown (pet) | 2% mana | Instant · **2 min CD** | Summons the Darkglare, which **extends all your active DoTs** and adds burst — the core burst window. Sync trinkets, potion, and racials to it; cast after Dark Harvest is on CD. |
| Dark Harvest | Major cooldown / builder (channel) | Generates **~3 Soul Shards** | Channeled · **1 min CD** `[T1]` (~40–45s effective w/ Cull the Weak, which cuts **1.5s per UA/Seed cast** *[Tier 1]*) | Channel that consumes the life force of every target afflicted by your DoTs and **refills shards**; it **heals you for 50% of damage done** *[Tier 1]*. Cast when **<3 shards** right before Darkglare, so the pair opens the burst window. **12.1 buffs it from two directions**: **Hedonic Gorging** (channels **10% faster**, **+15% damage**) and **Impetuous Wrath** (**+10%**, **+20% on a Haunted target**) — so Haunt-before-Dark-Harvest matters more than it did in S1. |
| Malevolence | Major cooldown (Hellcaller only) | — | ~instant · **60s CD** *[Tier 1]* | Hellcaller hero cooldown (a **talent**, not baseline) — burst that synergizes with the Wither/Darkglare window. **12.1 left Malevolence itself deliberately unchanged** while buffing the rest of Hellcaller (Wither +25%, Blackened Soul redesigned +45%), so "only relevant on the near-dead Hellcaller build" is an **S1 verdict that has not been re-tested** post-patch. |

## Curses & applied debuffs (utility / CC)

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Curse of Tongues | Utility (debuff) | Mana | Instant · no CD | Slows the target's **cast speed** (class talent). Only one Curse per target at a time. |
| Curse of Exhaustion | Utility / slow | Mana | Instant · no CD | Slows the target's **movement speed** (class talent) — kiting tool. |
| Curse of Weakness | Utility (debuff) | Mana | Instant · no CD | Reduces the target's **physical damage dealt**. **Class-baseline, not a talent** — `SkillLineAbility` 849, spell `702` *[Tier 1, 12.1.0.69214]* (this resolves the old "baseline vs talent" question). |
| Blight of Weakness | Utility (curse upgrade, DoT) | Mana | Instant / **120s** `[T1]` | Choice talent: **Curse of Weakness becomes Blight of Weakness**, adding a damaging/effect component (alt: Blight of Tongues). |

## Defensives & self-sustain

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Unending Resolve | Defensive (DR) | 2% mana | Instant · **3 min CD** | **−25% damage taken for 8s** (−40% with Strength of Will) and immunity to interrupt/silence. Main planned defensive. |
| Dark Pact | Defensive (absorb) | Sacrifices **20% of current HP** | Instant · **1 min CD** (−15s w/ Frequent Donor) | Shields you for **200% of the sacrificed health** for 20s *[Tier 1, 12.1]*; **usable while CC'd**. Ichor of Devils drops the HP cost to 5%. Both sides scale off the pool, which 12.1 grew by 25%. |
| Drain Life | Defensive / heal (channel) | Mana | Channeled · no CD | Channel that **damages and heals you for 500% of the damage done** *[Tier 1, 12.1]* — **12.1 raised the health drain 25% class-wide**, making it a materially better emergency button than in S1. Soulburn adds an absorb (capped at 30% max HP); **Empowered Drain Life** adds +200% healing and grants Soul Leech. **Hedonic Gorging** (new in 12.1) adds **+10% Drain Life damage**. Still emergency sustain, not a rotational filler. |
| Mortal Coil | Defensive / CC | Mana | Instant · **45s CD** | **Horrifies** the target 3s and heals you **20% max HP** (25% w/ Improved Mortal Coil) — panic heal + single-target CC. |
| Create Healthstone | Defensive (conjure → item heal) | Mana | Instant · no CD | The **player ability** is `Create Healthstone` (class-baseline); the heal is the *item* use of the stone it conjures. This row was filed under the bare name "Healthstone" until *[Tier 1, 2026-08-06]* — that name belongs to the item-use spell, which is not something you learn. Conjure out of combat; using the stone restores **25% HP** (30% w/ Empowered). **Pact of Gluttony** makes it reusable in combat; Soulburn/Gorebound inflate it. |
| Soulstone | Utility (battle-rez) | Mana | Instant · **10 min CD** | Places a self- or ally-**resurrection** buff (combat rez). Pre-place before pulls. |
| Soulburn | Utility (empower) | **1 Soul Shard** | Instant · no CD | Empowers your **next** Healthstone / Drain Life / Demonic Circle / Demonic Gateway / Fel Domination — the enabler for the `Soulburn → Healthstone → Dark Pact` defensive combo. |

## Movement

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Burning Rush | Movement | **Health drain** | Instant · toggle | Toggle **+50% movement speed** while draining your health each second. Core mobility; watch the HP drain with Soul Leech. |
| Demonic Circle | Movement (place) | Mana | Instant · no CD | Places a teleport anchor on the ground (class talent). |
| Demonic Circle: Teleport | Movement | Mana | Instant / **30s** `[T1]` | **Teleports to your placed circle** and breaks snares/roots — the reposition/escape button. |
| Demonic Gateway | Movement / utility (group) | Mana | ~2s cast / **10s** `[T1]` | Places a **two-portal gateway** the party can click to teleport between two points — big skip/repositioning tool; each player may take it **once per 90s** *[Tier 1]* (Gateway Mastery, a PvP talent, cuts that by 30s and adds range). **12.1: Summon Demonic Gateway is now a Utility spell by default in the Cooldown Manager**, so it shows in the CDM's utility category out of the box. |
| Fel Domination | Utility (pet) | 2% mana | Instant · **3 min CD** | Makes your next pet summon **instant and free** — fast re-summon after a pet dies. |

## Crowd control

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Fear | CC (single) | Mana | ~1.5s cast · no CD | Fears one target (breaks on damage). Single-target soft CC. |
| Shadowfury | CC (AoE stun) | Mana | Instant / **60s** `[T1]` | **Stuns all enemies** in a target area ~3s (choice vs Howl of Terror). AoE stop. |
| Howl of Terror | CC (AoE fear) | 2% mana | Instant · **40s CD** | **Fears nearby enemies** ~8s (choice vs Shadowfury). AoE panic. |
| Banish | CC (single) | Mana | ~1.5s cast · no CD | Banishes a **demon or elemental**, making it untargetable/unable to act. |
| Mortal Coil | CC (single) | Mana | Instant · 45s CD | Also a CC — see Defensives (horror + heal). |

## Pet & interrupt

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Spell Lock | **Interrupt** (Felhunter pet) | — | Instant · **24s CD** *[Tier 1]* | A **pet ability, not a player spell** — it is learned on the Felhunter's own skill line, so it never appears in this spec's `ability-inventory.tsv`; it lives in `_abilities/pet-family-annex.tsv` instead. Still **Affliction's only kick** (can be specced to silence); commanded via the pet, so it is gated on having the Felhunter out and alive. **12.1: like every class interrupt it now shows a "missed" visual over the target's head plus a distinct sound** when fired while the target was not casting — a free feedback signal for pet-kick timing. |
| Summon Felhunter | Pet | 2% mana | ~2.5s cast (instant w/ Fel Domination) | Summons the Felhunter — the group-content pet for **Spell Lock + Devour Magic** purge. Other pets (Imp/Voidwalker/Sayaad/Felguard) sim within noise; pick on utility. |
| Subjugate Demon | CC / utility | Mana | ~2.6s cast · no CD | **Enslaves a demon** target for temporary control. Situational world/utility. |
| Grimoire of Sacrifice | Passive / utility (talent) | — | Instant / toggle / **30s** `[T1]` | Choice vs Summoner's Embrace: **sacrifices your pet** for a personal damage/utility buff (S1 meta keeps the pet out with Summoner's Embrace instead). |

## Notable passives (context for the buttons above)

- **Nightfall** — Corruption damage has a chance to empower the next filler
  *started* while up: **+25% damage**, Shadow Bolt **instant**, Malefic Grasp
  channels **50% faster** *[Tier 1, 12.1]*. Drives the "start/restart the channel
  to consume the proc" rule. ⚠ **12.1 narrowed what Nightfall pays for** — the
  talent that turned a Nightfall proc into a free instant Seed of Corruption
  (*Nocturnal Yield*) **was removed**, and Blizzard folded that feel into Shard
  Instability instead. Any pre-12.1 guidance that says "dump Nightfall into Seed"
  is describing a talent that no longer exists.
- **Demonic Soul** (Soul Harvester) — shard spends (UA) stack an amp that pays
  off the aggressive spend-to-recycle-Dark-Harvest gameplan.
- **Shard Instability** — **redesigned in 12.1**. It is no longer a banked-stack
  discount on Unstable Affliction: **damage dealt by Shadow Bolt or Drain Soul now
  has a 20% chance to make your next Unstable Affliction *or* Seed of Corruption
  cost no Soul Shards and cast instantly.** So the filler now feeds the spender
  economy directly, and the proc is spendable into either the ST or the AoE
  button. (Hellcaller's *Seeds of Their Demise* can also grant it off Blackened
  Soul damage.) ⚠ The resolved 12.1 spell text names only Shadow Bolt, because
  Drain Soul *replaces* Shadow Bolt when talented; the patch notes name both, and
  the notes are the floor here.
- **Impetuous Wrath** *(new, 12.1)* — **Shadow Bolt / Drain Soul / Malefic Grasp
  and Dark Harvest deal +10% damage, or +20% against a target affected by Haunt.**
  It is the replacement Blizzard shipped for Nocturnal Yield, and it is the reason
  Haunt uptime now buys filler throughput on top of its own +16% amp.
- **Hedonic Gorging** *(new, 12.1)* — **Drain Life +10% damage; Siphon Life
  additionally increases Corruption damage by 10%; Dark Harvest channels 10%
  faster and deals +15%.** The stated design intent is that most of the throughput
  sits in **Siphon Life and Dark Harvest**, with the Drain Life line as flavour —
  which also means the talent is worth much less on an **Absolute Corruption**
  build, since Siphon Life is the other half of that choice node.
- **Removed in 12.1: Nocturnal Yield and Patient Zero.** Both are **gone from the
  live tree** (verified against the regenerated `talents.md` @ `12.1.0.68914`). Any
  build or rotation text still listing them — including the `maxroll-*.md` captures
  in this directory — is describing 12.0.7.
- **Soul Leech** (baseline) — single-target damage from you and your minions grants
  an absorb of **3% of the damage dealt** for 15s, capped at **5% of max health**
  *[Tier 1, 12.1]*; **Demon Skin / Fel Armor / Fortified Soul** grow and recharge it
  (passive EHP floor). **12.1 fixed which abilities feed it**: **Unstable Affliction
  and Malefic Grasp now correctly grant it** (as do Soul Anathema and Wicked Reaping
  on Soul Harvester, and Wither / Blackened Soul on Hellcaller), while **Cunning
  Cruelty no longer erroneously does**. Net for Affliction: the shield now refills
  off your spender and your Darkglare-window filler.
</content>

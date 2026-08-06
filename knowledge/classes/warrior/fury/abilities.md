---
title: Fury Warrior — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/warrior/fury/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.0.7.67808 — the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://wago.tools/db2 SpellName @ 12.0.7 (Blizzard game data, Tier 1 — canonical names/IDs)  # tier 1, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Warrior_Fury.simc  # tier 1 APL (ability set), 2026-07-11
  - https://www.method.gg/guides/fury-warrior/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/fury-warrior-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - knowledge/classes/warrior/fury/talents.md  # sibling tier-1 talent inventory (the tree is the ability floor)
confidence: high
---

# Fury Warrior — Ability Inventory (Midnight S1)

## Overview

Fury is the dual-wielding, Rage-fueled melee Warrior spec. The whole engine is
one feedback loop: build **Rage** with your strikes, spend it on **Rampage** to
trigger **Enrage** (a damage/haste buff), and hammer your empowered abilities
while Enrage is up — which builds more Rage. Damage is front-loaded and burst-
heavy, tied to keeping Enrage on and lining up **Recklessness** windows.

**Resource — Rage.** 0–100 (raised to 0–120 by **Overwhelming Rage**). Generated
by auto-attacks (Fury dual-wields, so two weapons feed Rage), **Bloodthirst**,
**Raging Blow**, **Whirlwind**, **Thunder Clap**, **Charge**, and **Champion's
Spear**. Spent almost entirely on **Rampage** (80 Rage) and **Execute**.
Overcapping Rage is a throughput loss, so the rotation is a constant
generate → spend loop.

**Enrage** is the central buff: crits from **Bloodthirst** (via **Fresh Meat**),
casting **Rampage**, and **Odyn's Fury** apply Enrage, which increases your
damage and attack speed for a few seconds. Keeping Enrage up (never letting it
drop for a filler you could have delayed) is the core skill of the spec —
Rampage is the primary Enrage refresher (see `rotation.md`).

**Hero trees.** Two viable picks in S1:
- **Slayer** — burst/Execute-window build. Adds **Slayer's Dominance** stacks
  and **Sudden Death** interplay; **Bloodthirst → Bloodbath** and
  **Raging Blow → Crushing Blow** during its windows (via **Reckless Abandon**),
  and feeds **Bladestorm** cooldown reduction through **Unrelenting Onslaught**.
  Ahead on single target and burst AoE.
- **Mountain Thane** — sustained/lightning build. Replaces **Whirlwind** with
  **Thunder Clap** in the rotation, adds **Lightning Strikes** procs and
  **Thunder Blast** (an empowered Thunder Clap that extends Avatar). Pulls ahead
  in most sustained-AoE situations.

Abilities that belong to one hero tree are flagged in the table.

**Tier-1 floor.** Canonical **name, spellID, acquisition origin and base cooldown**
live in `ability-inventory.tsv` (generated from wago DB2 @ 12.0.7.67808) — read
them there rather than trusting a restated number here. This file is for
**function, role and rotational context**; on any disagreement the tsv wins.
**One** row — `Crushing Blow` — is an Enrage-window *override* button with no
acquisition row of its own and is expected to be missing from it; it is
catalogued in `../../_abilities/section-4-catalogue.md`. ⚠ `Bloodbath` is **not**
in that situation and an earlier version of this note wrongly said it was:
`ability-inventory.tsv` carries `Bloodbath 113344 class-baseline
SkillLineAbility:840 castable=true`. It has a real acquisition row — do not read
its presence as an anomaly.

**Reconciliation note (game-data floor).** The sibling `talents.md` (Blizzard
game data) is authoritative for what Fury actually has in 12.0.7. **Thunderous
Roar, Ravager, and Onslaught are NOT in the Fury tree** and are excluded here
despite appearing on some cross-spec lists. **Protection Stance is tank-only** —
Fury's defensive stance is **Defensive Stance** (the seed's "Protection Stance"
is a mislabel). **Berserker Rage** is the fear/Enrage tool, delivered in
Midnight through the **Berserker Shout / Fearless** choice node.

## Rotational core (builders, spenders, fillers)

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
| Bloodthirst | Rotational-builder | Generates Rage | Instant · **4.5s CD** *[Tier 1]*, haste-reduced | Core Rage generator and heal; its crits trigger **Enrage** (via **Fresh Meat**). Kept on cooldown for damage and Enrage upkeep. Becomes **Bloodbath** during Slayer/Reckless Abandon windows. |
| Raging Blow | Rotational-builder | Generates Rage | Instant · 2 charges (~8s recharge, haste-reduced) | Dual-wield strike, 2 charges. Generates Rage and (with Improved Raging Blow / Surge of Adrenaline) resets/empowers. Becomes **Crushing Blow** during Slayer/Reckless Abandon windows. |
| Rampage | Rotational-spender | **80 Rage** | Instant · no CD | Primary Rage spender and the main **Enrage** trigger — a multi-hit finisher. Often delayed slightly past 80 Rage to pool, as long as Enrage doesn't fall off. Empowered by **Rampaging Berserker**. |
| Execute | Rotational-spender (execute) | Rage (variable) | Instant · no CD | Big finisher usable below 20% target HP (35% with **Massacre**), or any time a **Sudden Death** proc makes it free/usable. Highest-priority spender in execute range. |
| Whirlwind | Rotational-builder / cleave-enabler | Generates Rage | Instant · no CD | AoE spin; applies the **Whirlwind buff** that makes your next single-target abilities cleave (Meat Cleaver / Improved Whirlwind). The AoE opener/maintainer — **replaced by Thunder Clap under Mountain Thane**. |
| Rend | Rotational-builder (DoT; talent) | ~10 Rage | Instant · no CD | Bleed DoT (class talent). Maintain when talented (single-target priority keeps it up; refresh when <~5s remain). Minor throughput, optional in some builds. |
| Bloodbath | Rotational-builder (empowered) | Generates Rage | Instant · shares Bloodthirst | Empowered **Bloodthirst** during Recklessness / **Reckless Abandon** windows — bigger hit, stronger Enrage/bleed interaction. |
| Crushing Blow | Rotational-builder (empowered) | Generates Rage | Instant · shares Raging Blow | Empowered **Raging Blow** during Recklessness / **Reckless Abandon** windows. ⚠ A runtime override with no acquisition row — expect it to be **absent from `ability-inventory.tsv`**; what Tier 1 confirms is that its parent `Raging Blow` is live on the Midnight Warrior tree *[Tier 1, 12.0.7.67808]*. Its absence there is not evidence against this row. Recorded in `../../_abilities/section-4-catalogue.md` (`prose-only`) — that catalogue, not a marker, is where this unknown lives. |
| Thunder Clap | Rotational-builder (AoE; Mountain Thane) | Generates Rage | Instant · ~6s CD | AoE strike + slow; under **Mountain Thane** it **replaces Whirlwind** in the rotation and is empowered by Avatar. Also a class-tree ability (Rend/Thunder Clap seed). |
| Thunder Blast | Rotational-builder (AoE; Mountain Thane) | Generates Rage | Instant · charge-based | Empowered Thunder Clap proc (Mountain Thane). Similar direct damage to Thunder Clap but **extends Avatar** and always triggers a **Lightning Strike** — press at 2 stacks / during Avatar. |

## Major cooldowns

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Recklessness | Major cooldown | — (generates Rage passively while up) | Instant (off GCD) · ~90s base, ~45s effective w/ Anger Management | The core burst window — boosts crit and Rage generation, letting Rampage fire more often. **Reckless Abandon** empowers it (Bloodbath/Crushing Blow). Line trinkets/potion/racials to it. |
| Avatar | Major cooldown (choice: Avatar / Bladestorm) | — | Instant (off GCD) · ~90s | Damage/size buff; shares the slot with Bladestorm on the spec choice node. The **Mountain Thane** pick — empowers Thunder Clap and is extended by Thunder Blast. |
| Bladestorm | Major cooldown (choice: Avatar / Bladestorm) | — | Channeled · ~90s | Spinning whirlwind channel — the **Slayer** signature cooldown. Use while Enraged, ideally right after Rampage; can be held ≤15s to line up with Recklessness. Storm Bolt is usable during it. |
| Odyn's Fury | Major cooldown (short) | Generates Rage | Instant · ~45s (Fury talent, spell 385059) | Frontal burst that **immediately triggers Enrage** and applies a bleed. High priority, pressed early in its window. S1 **tier set reduces its cooldown**. |
| Champion's Spear | Major cooldown (ranged) | Generates Rage on cast — amount is Tier-3 only *(see note)* @verify-ingame (Rage generated on cast) | ~30yd throw · **90s CD** *[Tier 1]* | Throws a spear that roots/tethers and bursts the area (**class** talent, shared with Arms and Protection). Sync with your burst window. |
| Rampaging Berserker | Capstone (empower/active) | — | — · capstone talent | Spec capstone (spell 1269308). Boosts **Rampage** damage and extends **Recklessness** duration (~18s). Talent tree marks it ACTIVE; exact active component vs passive empower is uncertain. @verify-ingame |

> **On `Champion's Spear`'s Rage-on-cast.** The generated inventory has no resource
> column, so Tier 1 can settle the **cooldown** (90s) but not the Rage yield. This row
> previously asserted "+10 Rage on cast (was 20)" as though it were measured; it was a
> Tier-3 guide reading. Left unstated rather than restated — don't build a Rage-pooling
> plan on a number nothing here measured.

## Utility, ranged & shouts

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Battle Shout | Utility (raid buff) | — | Instant · no CD | Raid-wide **+Attack Power** buff. Pre-cast; maintain. |
| Heroic Throw | Utility (ranged) | — | ~30yd · short CD | Ranged thrown-weapon hit — pull/tag or hit an out-of-melee target. |
| Wrecking Throw | Utility (ranged; choice: Wrecking / Shattering Throw) | — | ~30yd · **45s CD** *[Tier 1]* | Big ranged physical hit (a genuine **choice node** vs **Shattering Throw**, which strips immunities/absorbs — you get one or the other, never both). Appears low in the ST filler priority. |
| Hamstring | Utility (slow) | ~10 Rage | Instant · no CD | Single-target movement slow. |
| Piercing Howl | CC (AoE slow; choice: Piercing Howl / Intimidating Shout) | — | Instant / **90s** `[T1]` | AoE movement slow around you (choice vs **Intimidating Shout**, an AoE fear). |
| Berserker Shout | Utility / CC-break (choice: Berserker Shout / Fearless) | — | Instant · **60s CD** *[Tier 1]* | Removes fear/incapacitate and can Enrage (the Midnight delivery of **Berserker Rage**). A **choice node** vs **Fearless**, so taking it costs you Fearless. |

## Crowd control & interrupt

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Pummel | **Interrupt** | — | Instant · **15s CD** | The kick — interrupts the target's cast. Fury's only baseline interrupt. |
| Storm Bolt | CC (stun) | — | ~20yd · **30s CD** | Throws your weapon to **stun** the target ~4s (class talent). Usable during Bladestorm. |
| Shockwave | CC (AoE stun) | — | Instant · **40s CD** | Cone **AoE stun** ~2s (class talent); CD reduced by **Rumbling Earth** when it hits 3+ targets. |
| Intimidating Shout | CC (AoE fear; choice) | — | Instant / **90s** `[T1]` | AoE **fear** (choice vs Piercing Howl). |
| Taunt | Utility (threat) | — | Instant · **8s CD** | Forces a target to attack you (off-tank/utility). |

## Defensives & self-sustain

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Enraged Regeneration | Defensive (heal + DR) | — | Instant · **120s CD** *[Tier 1]* | Heals over time and **reduces damage taken** while active (spec talent) — the main personal survival cooldown. ⚠ This row said "~3 min" until Tier-1 corrected it to **2 min**; it comes up more often than the old text implied, so stop hoarding it. Heal % and DR % are not carried by the generated inventory — treat any number you see for those as Tier 3. @verify-ingame (heal % and DR %) |
| Rallying Cry | Defensive (raid) | — | Instant · **3 min CD** | Grants the party **+max health** for 10s — a raid-wide "oh no" button. |
| Enrage (buff) | Passive (damage/haste) | — | — | The spec's signature buff (see Overview): +damage & +attack speed while up. Triggered by Rampage, Bloodthirst crits (Fresh Meat), and Odyn's Fury. |
| Impending Victory | Defensive (heal) | ~10 Rage | Instant · ~25s CD | Instant strike that **heals you** ~30% (class talent) — cheap self-heal on a short CD. |
| Spell Reflection | Defensive (reflect) | — | Instant · ~25s CD | Reflects the next spell/incoming magic for a short window. |
| Enraged Regeneration / Second Wind | Passive sustain | — | — | **Second Wind** (class talent) heals you when out of combat damage / at low health; **Leeching Strikes** adds leech. Passive EHP floor. |
| Defensive Stance | Defensive (stance) | — | Instant · toggle | Stance that **reduces damage taken** (at a damage cost) — toggle on for heavy hits, off to DPS. (NOT "Protection Stance," which is tank-only.) |
| Berserker Stance | Utility (stance) | — | Instant · toggle | The DPS stance (precombat `berserker_stance,toggle=on` in the APL); the default Fury stance. |

## Movement

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Charge | Movement (gap-close) | +Rage on hit | ~20s recharge (2 charges w/ Double Time) · 8–25yd | Rush to a target, generate Rage, and root/slow it. Primary engage; opener uses it at range. |
| Heroic Leap | Movement (leap) | — | ~45s CD (w/ Bounding Stride) · targeted | Leap to a location — reposition/gap-close; **Bounding Stride** adds a speed burst on landing. |
| Intervene | Movement / defensive (choice: Intervene / Interpose) | — | ~30s CD | Charge to an ally and **intercept the next hit** for them (choice vs **Interpose**). Also a mobility hop to a friendly target. |
| Bounding Stride / Double Time | Passive (movement) | — | — | Speed and extra Charge/Leap charges — mobility passives that make the kit fluid. |

## Notable passives (context for the buttons above)

- **Enrage / Fresh Meat** — the loop's heartbeat: Bloodthirst crits and Rampage
  apply Enrage; **Frenzied Enrage / Powerful Enrage** and **Warpaint** tune its
  strength/effect. Never drop Enrage for a filler.
- **Sudden Death** — random procs that make **Execute** usable at any health and
  free; a proc jumps Execute up the priority (especially under Slayer).
- **Anger Management** — Rage spent reduces the cooldowns of Recklessness/Avatar/
  Bladestorm, which is why they come up roughly every ~45s instead of 90s.
- **Meat Cleaver / Improved Whirlwind** — Whirlwind's buff makes single-target
  strikes cleave; the backbone of Fury AoE (Mountain Thane routes this through
  Thunder Clap instead).
- **Slayer's Dominance / Unrelenting Onslaught** (Slayer) — stack a debuff and
  feed Bladestorm CD reduction; **Lightning Strikes / Thunder Blast** (Mountain
  Thane) — Avatar-empowered lightning procs.
- **Reckless Abandon** — turns Recklessness into the Bloodbath/Crushing Blow
  empowered window (the burst backbone for Slayer).

---
title: Protection Warrior — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/warrior/protection/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.0.7.67808 — the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warrior_Protection.simc  # tier 1 APL, 2026-07-11
  - https://www.icy-veins.com/wow/protection-warrior-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/protection-warrior/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1 name reconciliation, 2026-07-11
confidence: high
---

# Protection Warrior — Abilities (Midnight S1)

## Overview

Protection is Warrior's tank spec: sword-and-board, plate armor, **Rage**
resource (0–100, or higher with talents). Rage is *generated* by auto-attacks,
`Shield Slam`, `Thunder Clap`, `Charge`/`Shield Charge`, `Champion's Spear`,
`Ravager`, and (with `Booming Voice`) `Demoralizing Shout`; it is *spent* on
active mitigation (`Shield Block`, `Ignore Pain`) and on `Revenge` / `Execute`.
Unlike most tanks the spec has **no separate "power" bar** — offense and
defense compete for the same Rage, so the core skill is spending it on
mitigation without starving the damage rotation (or overcapping).

**Active mitigation** is two-pronged: `Shield Block` (blocks melee for a window
and buffs `Shield Slam` +30%) and `Ignore Pain` (a rolling absorb that also acts
as the rage-overflow dump). Damage comes from a tight `Shield Slam` → `Revenge` /
`Thunder Clap` builder/spender loop that recycles fast via cooldown-reset procs.

**Hero trees (Midnight S1):**
- **Mountain Thane** — the storm/lightning tree; converts `Thunder Clap` into
  empowered **`Thunder Blast`** procs and adds `Burst of Power` (free
  `Shield Slam`s), `Lightning Strikes`, and `Avatar of the Storm`. **Meta pick
  for 12.0.7** (leads Colossus in raid and M+, ST and AoE).
- **Colossus** — the raw-strength tree; adds the channeled nuke **`Demolish`**
  and `Colossal Might` stacking, leaning on `Revenge` over `Thunder Clap`.

> **Name reconciliation (Tier-1 game data):** the tanking stance is
> **`Defensive Stance`** (spell 386208) — an older "Protection Stance" name is
> **not** in current game data. **`Berserker Shout`** (384100) is the current
> name for the fear-immunity shout (older "Berserker Rage"). `Champion's Spear`
> (376079), `Thunder Blast` (435607), `Violent Outburst`, `Seeing Red`, and
> `Demolish` (436358) all confirmed against `SpellName.csv @ 12.0.7.67808`.

## Ability inventory

> **Tier-1 floor.** Canonical **name, spellID, acquisition origin and base
> cooldown** live in `ability-inventory.tsv` (generated from wago DB2 @
> 12.0.7.67808) — read them there rather than trusting a restated number here.
> This table is for **role and rotational context**; on any disagreement the tsv wins.

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
| **Shield Slam** | Rotational-builder | Generates ~15–20 Rage | Instant / ~9s (hasted) | Primary single-target hit and top rage generator; `Shield Block` buffs it +30%, `Devastator`/procs reset its CD. Press on cooldown. |
| **Thunder Clap** | Rotational-builder (AoE) | ~5 Rage (or free) | Instant / ~6s (hasted) | Frontal AoE, applies Rend/Deep Wounds and does most of the AoE threat. As Mountain Thane it periodically becomes **Thunder Blast**. |
| **Thunder Blast** | Rotational-builder (Mountain Thane) | Free | Instant / proc (stacks to 2) | Empowered `Thunder Clap` from Lightning Strikes; top AoE priority under Avatar (Capacitance). Replaces Thunder Clap when a stack is up. |
| **Revenge** | Rotational-spender | ~30 Rage (free with proc) | Instant / no CD | Main rage dump and cleave; free/discounted after a dodge/parry proc. Colossus's primary spender. |
| **Execute** | Rotational-spender | 20+ Rage (scales) | Instant / no CD | Execute-phase spender (target <20%, or <35% with `Massacre`); `Sudden Death` procs make it free/usable anytime. |
| **Demolish** | Major cooldown (Colossus) | Free | Channel / ~45s | Colossus-only channeled nuke; spend `Colossal Might` stacks (≥3). Heavy burst + Deep Wounds. |
| **Devastate** | Rotational filler | Free | Instant / no CD | Low-priority filler when nothing else is available (usually replaced by the `Devastator` passive). |
| **Shield Block** | Defensive (active mitigation) | 30 Rage | Instant / 2 charges, ~16s recharge | Blocks incoming melee for ~6s **and** buffs `Shield Slam` +30% — keep near-permanent uptime while actively tanking. |
| **Ignore Pain** | Defensive (active mitigation) | ~35 Rage | Instant / no CD | Rolling damage absorb (caps ~30% max HP); doubles as the **rage-overflow dump** — cast before a builder would overcap Rage. |
| **Avatar** | Major cooldown | Free | Instant / ~90s (Anger Management) | +20% damage for 20s, the core offensive window; as Mountain Thane grants 2 `Thunder Blast` stacks (Avatar of the Storm). Press on cooldown. |
| **Shield Charge** | Major cooldown / Movement | Free (generates Rage) | Instant / ~45s | Gap-closing charge dealing AoE damage with a short stun; grants a `Shield Block`-like buff. On cooldown offensively. |
| **Champion's Spear** | Major cooldown | Free (generates Rage — amount is Tier-3 only) @verify-ingame (Rage generated on cast) | Instant / **90s CD** *[Tier 1]* | Thrown spear that tethers/roots and deals burst; press on cooldown. A **class** talent, so Arms and Fury get the identical button. |
| **Ravager** | Major cooldown (AoE) | Free (generates Rage) | Instant / **90s** `[T1]` | Whirling AoE DoT at a location, big rage generator; Colossus choice-node alt of Whirling Blade. |
| **Demoralizing Shout** | Defensive / Cooldown | Free (+20 Rage with Booming Voice) | Instant / ~45s | −20% enemy damage for the raid-frame and (with `Booming Voice`) a rage burst + damage amp; on cooldown. |
| **Last Stand** | Defensive (major) | Free | Instant / ~180s | Temporary +30% max health; big emergency EHP button. |
| **Shield Wall** | Defensive (major) | Free | Instant / ~3.5min | −40% damage taken for 8s — the largest personal cooldown. |
| **Rallying Cry** | Defensive (raid) | Free | Instant / ~3min | +15% max health to the party/raid; group save. |
| **Spell Reflection** | Defensive (reactive) | Free | Instant / ~25s | Reflects the next spell and reduces magic damage for the window. |
| **Taunt** | Utility (threat) | Free | Instant / ~8s | Forces target to attack you; core tank-swap tool. |
| **Challenging Shout** | Utility / CC | Free | Instant / **120s** `[T1]` | AoE taunt — grabs all nearby enemies. |
| **Heroic Throw** | Utility (ranged threat) | Free | Instant / short CD | Ranged pull / threat on a distant enemy. |
| **Wrecking Throw / Shattering Throw** | Utility | Free | Instant / CD | Ranged strike (choice node) — shreds absorbs / boss shields; used in the APL with `Javelineer`. |
| **Charge** | Movement | Free (generates 20 Rage) | Instant / ~20s | Opener gap-close and rage seed; roots the target briefly. |
| **Heroic Leap** | Movement | Free | Instant / ~45s | Leap to a target area; primary repositioning/escape. |
| **Intervene** | Movement / Defensive | Free | Instant / ~30s (2 charges) | Jump to an ally and intercept an attack; co-tank/positioning tool. |
| **Pummel** | Interrupt | Free | Instant / ~15s | The kick — core interrupt. |
| **Storm Bolt** | CC (stun) | Free | Instant / ~30s | Single-target stun (talent). |
| **Shockwave** | CC (AoE stun) | Free | Instant / ~40s | Frontal-cone AoE stun; CD reduced vs 3+ targets with Rumbling Earth. |
| **Piercing Howl** | CC (AoE slow) | Free | Instant / **90s** `[T1]` | AoE slow (choice node vs Intimidating Shout). |
| **Intimidating Shout** | CC (fear) | Free | Instant / ~90s | AoE fear (choice node vs Piercing Howl). |
| **Berserker Shout** | Utility (fear/CC break) | Free | Instant / ~60s | Breaks and prevents fear/sleep/incapacitate on self (choice node vs Fearless). Formerly "Berserker Rage". |
| **Impending Victory** | Self-heal | ~10 Rage | Instant / ~25s | Small self-heal on use; resets on kill. |
| **Hamstring** | Utility (slow) | Rage | Instant / no CD | Single-target slow. |
| **Battle Shout** | Utility (raid buff) | Free | Instant / no CD | +Attack Power party buff; maintain out of combat. |
| **Defensive Stance** | Utility (stance) | Free | Instant / toggle (3s between swaps) | The tanking stance — reduces damage taken. ⚠ **It is a talent, not baseline** *[Tier 1]* — this row claimed baseline until 12.0.7 data said otherwise, so an untalented Protection build genuinely does not have it and you cannot assume it on a fresh character or a borrowed loadout. (Seed's "Protection Stance" = this.) |
| **Battle Stance** | Utility (stance) | Free | Instant / toggle | Offensive stance toggle (talent); APL opens in it. |
| **Rend** | Passive/DoT (Colossus) | Rage | Instant / — | Bleed applied via Thunder Clap (Colossus); the APL refreshes it when it falls off. |
| **Devastator** | Passive | — | — | Auto-attacks periodically cast `Shield Slam` for free — smooths the builder loop. |
| **Booming Voice** | Passive | — | — | `Demoralizing Shout` also generates 20 Rage and amps damage — makes Demo Shout a rotational button. |
| **Violent Outburst** | Passive | — | — | Shield Slam/Revenge stacking empowers the next Shield Slam/Thunder Clap; watch the buff. `Violent Outburst` 386477 is the Tier-1 name *[Tier 1]*. ⚠ **`Seeing Red` is not in any Warrior `ability-inventory.tsv`** and has no ledger verdict — the stacking-buff name is carried here from Tier-3 guides only, so the Tier-1 floor above does **not** cover it. |
| **Burst of Power** | Passive (Mountain Thane) | — | — | Procs that make the next 2 `Shield Slam`s cost no cooldown — react to the buff. |

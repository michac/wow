---
title: Protection Warrior — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/warrior/protection/ability-inventory.md  # tier 1, generated from DB2 @ 12.0.7.67808 + Blizzard spell API — name/spellID/origin/cooldown/tooltip
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1 name reconciliation, 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warrior_Protection.simc  # tier 1 APL — backs which buttons are rotationally live, 2026-07-11
  - https://www.icy-veins.com/wow/protection-warrior-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/protection-warrior/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
confidence: high
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Protection Warrior — Abilities (Midnight S1)

> **This file carries no per-spell facts.** Canonical name, spellID, acquisition
> origin, baseline cooldown, talent/hero placement and the **in-game tooltip
> text** for every ability the spec can have live in **`ability-inventory.md`**
> beside this file — generated from wago DB2 + the Blizzard spell API @
> 12.0.7.67808 and regenerated on patch day.
>
> | Question | Read |
> |---|---|
> | What does X do? Its spellID, cooldown, tooltip? | `ability-inventory.md` |
> | When do I press X? | `rotation.md` |
> | Do I take X? Which hero tree? | `builds.md`, `talents.md` |
> | Why is X missing from the inventory? | `../../_abilities/section-3-corroborated.md`, `section-4-catalogue.md` |
>
> This file is the editorial layer: the resource model, which inventory rows are
> actually buttons, and the judgements game data cannot make.

## Resource model

Protection is Warrior's tank spec: sword-and-board, plate armor, **Rage** (0–100,
higher with talents). **Unlike most tanks there is no separate "power" bar** —
offense and defense compete for the same Rage, and that single fact is the spec.
The skill is funding active mitigation without starving the damage loop, and
never overcapping.

Rage is *generated* by auto-attacks, Shield Slam, Thunder Clap, Charge / Shield
Charge, Champion's Spear, Ravager and (with Booming Voice) Demoralizing Shout.
It is *spent* on Shield Block and Ignore Pain, and on Revenge / Execute.
⚠ **The generated inventory has no cost column** — its tooltips state what a
spell *generates* and never what it *costs*, so the spend side is recorded only
in prose: Shield Block 30, Ignore Pain ~35, Revenge ~30 (free on proc), Execute
20+ scaling.

**Active mitigation is two-pronged and both halves double as something else.**
Shield Block buffs Shield Slam +30%, so it is offense as well as defense; Ignore
Pain is the **rage-overflow valve** as well as an absorb. Neither is a pure
defensive and neither should be treated as one.

**Hero trees.** `builds.md` owns the pick. In kit terms: **Mountain Thane** adds
a proc button (**Thunder Blast**, which replaces Thunder Clap while a stack is
up) and turns the bar proc-reactive; **Colossus** adds one real button
(**Demolish**, channelled) and shifts the AoE spender from Thunder Clap to
Revenge.

## Inventory

The curated subset: which of the generated inventory's rows are buttons you
actually press, and what each is *for*. **Role only** — no spellID, cooldown,
cast time or mechanics, because all four regenerate one file over. ⚠ This table
is also a **machine input**: `wowkb.gen_abilities` reads its first column to
build the `prose-only` leg of `../../_abilities/section-4-catalogue.md`, so a
name deleted from here silently disappears from that catalogue.

| Ability | Role |
|---|---|
| **Shield Slam** | Damage core + top Rage generator; Shield Block buffs it, so the two are coupled |
| **Thunder Clap** | AoE damage core + Rage; most of the AoE threat |
| **Thunder Blast** | AoE damage core (Mountain Thane) — a proc that *replaces* Thunder Clap while a stack is up |
| **Revenge** | Rage spender / cleave; Colossus's primary spender |
| **Execute** | Rage spender — execute phase, or any time on a Sudden Death proc |
| **Demolish** | Offensive cooldown (Colossus) — the one button that tree adds |
| **Devastate** | Last-resort filler; usually retired by the Devastator passive |
| **Shield Block** | Active mitigation — **and** an offensive buff, so not a pure defensive |
| **Ignore Pain** | Active mitigation — **and** the Rage-overflow valve, so not a pure defensive |
| **Avatar** | Offensive cooldown — the burst window |
| **Shield Charge** | Offensive cooldown + gap closer + Rage |
| **Champion's Spear** | Offensive cooldown + Rage. A **class** talent, so Arms and Fury get the identical button |
| **Ravager** | Offensive cooldown (AoE) + Rage; Colossus choice-node alternative to Whirling Blade |
| **Demoralizing Shout** | Raid-frame defensive — and, with Booming Voice, an offensive cooldown and Rage burst |
| **Last Stand** | Major defensive — EHP |
| **Shield Wall** | Major defensive — the largest personal |
| **Rallying Cry** | Major defensive — group |
| **Spell Reflection** | Major defensive — magic, reactive |
| **Taunt** | Threat — the tank-swap tool |
| **Challenging Shout** | Threat — AoE taunt |
| **Heroic Throw** | Threat — ranged pull |
| **Wrecking Throw** / **Shattering Throw** | Utility (choice node); the APL uses it with Javelineer |
| **Charge** | Movement + the opener's Rage seed |
| **Heroic Leap** | Movement — repositioning |
| **Intervene** | Movement + co-tank defensive |
| **Pummel** | **The spec's only interrupt** |
| **Storm Bolt** | Control — single-target stun |
| **Shockwave** | Control — AoE stun |
| **Piercing Howl** | Control — AoE slow (choice node vs Intimidating Shout; you get one) |
| **Intimidating Shout** | Control — AoE fear (the other side of that choice node) |
| **Berserker Shout** | Control — self fear/sleep/incapacitate break |
| **Impending Victory** | Self-heal |
| **Hamstring** | Control — single-target slow |
| **Battle Shout** | Group buff — maintain out of combat |
| **Defensive Stance** | Stance — the tanking one. ⚠ **A talent, not baseline** |
| **Battle Stance** | Stance — offensive; the APL opens in it |
| **Rend** | Bleed (Colossus) — applied via Thunder Clap, refreshed by the APL |
| **Devastator** | Passive — smooths the builder loop |
| **Booming Voice** | Passive — promotes Demoralizing Shout into a rotational button |
| **Violent Outburst** | Passive — a stacking empowerment you watch the buff for |
| **Burst of Power** | Passive (Mountain Thane) — a proc you react to |

## Notes the generated layer cannot make

- **`Defensive Stance` is a talent, not baseline** *[Tier 1]*. This file claimed
  baseline until 12.0.7 data said otherwise. An untalented Protection build
  genuinely does not have it — you cannot assume it on a fresh character or a
  borrowed loadout.
- **Name reconciliation.** The tanking stance is **`Defensive Stance`** (386208);
  no "Protection Stance" exists in current game data (the BucketBinds seed's
  "Protection Stance" is this). The fear-immunity shout is **`Berserker Shout`**
  (384100), formerly "Berserker Rage". `Champion's Spear` (376079), `Thunder
  Blast` (435607), `Violent Outburst` (386477) and `Demolish` (436358) all
  confirmed against `SpellName.csv @ 12.0.7.67808`.
- **`Seeing Red` is in no Warrior `ability-inventory.tsv`** and has no ledger
  verdict. Tier-3 guides still name it as the stacking buff that feeds Violent
  Outburst; the Tier-1 floor does not cover it. Treat "Seeing Red" in a guide as
  a nickname for Violent Outburst's stack until something Tier-1 says otherwise.
- ⚠ **Two Mountain Thane tooltips in `ability-inventory.md` render the wrong
  spec's branch.** `Burst of Power` 437118 resolves to "…make your next 2
  **Bloodthirsts** have no cooldown" and `Thunder Blast` 435607 to "**Shield Slam
  and Bloodthirst** have a 35% chance…" — Bloodthirst is Fury's builder. These
  are class-shared hero-tree spells whose `$?spec[…][…]` conditional the spell
  API resolved without spec context. For Protection the trigger and the payoff
  are Shield Slam. This is a **generated-layer wart, not a data correction**;
  do not "fix" the tsv.
  - Burst of Power + Thunder Blast — read both tooltips in the Protection spellbook: do they say Shield Slam or Bloodthirst? @verify-ingame
- **Champion's Spear is a class talent**, so Arms and Fury get the identical
  button — a cross-spec fact no per-spec inventory states.
- **Charge/recharge times are in neither layer.** The inventory's `cooldown` is
  `SpellCooldowns` at DifficultyID 0, which returns the **GCD** for a charge
  ability — Shield Block and Ignore Pain both read ~1s there. The real recharge
  lives in `SpellCategory.ChargeRecoveryTime`, unreachable without breaking the
  build pin (`reconcile-ledger.md` §5 G6). Shield Block is 2 charges on a ~16s
  recharge; Intervene is 2 charges *(Tier 3)*.

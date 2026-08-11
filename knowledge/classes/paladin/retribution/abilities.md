---
title: Retribution Paladin — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/paladin/retribution/ability-inventory.md  # tier 1, generated from DB2 @ 12.0.7.67808 + Blizzard spell API — name/spellID/origin/cooldown/tooltip
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - raw/wago/SpellPower.csv @ 12.0.7  # tier 1, Holy Power costs (no column for these in the generated inventory)
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Paladin_Retribution.simc  # tier 1 APL — backs which buttons are rotationally live, 2026-07-11
  - https://www.method.gg/guides/retribution-paladin/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/retribution-paladin-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
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


# Retribution Paladin — Abilities (Midnight S1)

> **This file carries no per-spell facts.** Canonical name, spellID, acquisition
> origin, baseline cooldown, talent/hero placement and the **in-game tooltip
> text** for every ability the spec can have live in **`ability-inventory.md`**
> beside this file — generated from wago DB2 + the Blizzard spell API @
> 12.0.7.67808 and regenerated on patch day. Anything restated here would go
> stale the moment that file did not.
>
> | Question | Read |
> |---|---|
> | What does X do? Its spellID, cooldown, tooltip? | `ability-inventory.md` |
> | When do I press X? | `rotation.md` |
> | Do I take X? Which hero tree? | `builds.md`, `talents.md` |
> | Why is X missing from the inventory? | `../../_abilities/section-3-corroborated.md`, `section-4-catalogue.md` |
>
> This file is the editorial layer: the resource model, which of the inventory's
> 187 rows are actually buttons, and the judgements game data cannot make.

## Resource model

Retribution is a melee plate DPS spec that spends **Holy Power** (0–5), a
discrete secondary resource built by melee builders and burned by finishers.
Mana is a background pool used only for the paladin utility/blessing kit, never
for the damage rotation. The loop is **build → spend**, with proc-driven
instants (Art of War, Empyrean Power) jumping the queue and a burst window
(Avenging Wrath, or its replacements) to align everything into.

**Every Retribution finisher costs 3 Holy Power** — Templar's Verdict 85256,
Divine Storm 53385, Final Verdict 383328 and Hammer of Light 427453 all read
`PowerType 9, cost 3` *[T1 DB2: SpellPower @ 12.0.7]*. "Spend at 5" is a
**pooling** rule, not a cost; see `rotation.md`. ⚠ **The generated inventory has
no cost column at all** — its descriptions state what a spell *generates*
("Generates 3 Holy Power") and never what it *costs*, so this paragraph is the
only Tier-1 record of the cost side.

**Hero trees.** `builds.md` owns the pick and the talent detail. In kit terms:
**Templar** swaps your spender for **Hammer of Light** for 20s after Wake of
Ashes (and later hands out free ones), so the Templar bar has a button the
inventory does not list; **Herald of the Sun** changes no spender and adds
Dawnlight / Eternal Flame / Sun's Avatar instead.

## Inventory

The curated subset: which of the generated inventory's rows are buttons you
actually press, and what each is *for*. **Role only** — no spellID, cooldown,
cast time or mechanics, because all four regenerate one file over. ⚠ This table
is also a **machine input**: `wowkb.gen_abilities` reads its first column to
build the `prose-only` leg of `../../_abilities/section-4-catalogue.md`, so a
name deleted from here silently disappears from that catalogue.

| Ability | Role |
|---|---|
| **Crusader Strike** | Holy Power builder — baseline filler, retired by both choice-node alternatives below |
| **Templar Strike** / **Templar Slash** | Holy Power builder — the two-part combo Templar Strikes turns Crusader Strike into |
| **Crusading Strikes** | Holy Power builder (passive) — the other alternative: generation moves onto auto-attacks, so there is no filler button at all |
| **Judgment** | Holy Power builder — ranged, and the debuff the burst window is built around |
| **Blade of Justice** | Holy Power builder — the high-priority one; Art of War / Righteous Cause make it free |
| **Final Verdict** | Holy Power spender — single target. The talented upgrade to Templar's Verdict, and what the simc APL's `templars_verdict` action really fires |
| **Templar's Verdict** | Holy Power spender — the baseline single-target finisher it upgrades from |
| **Divine Storm** | Holy Power spender — AoE |
| **Hammer of Light** | Holy Power spender — **Templar only**, and it replaces the others rather than joining them |
| **Wake of Ashes** | Burst cooldown + builder; the Templar spender swap starts here, and Sacrosanct Crusade makes it a defensive too |
| **Execution Sentence** | Burst cooldown — delayed detonation, so it is cast *into* the window rather than during it |
| **Divine Toll** | Burst cooldown + AoE Holy Power injection |
| **Avenging Wrath** | Burst cooldown — the window everything else aligns to |
| **Crusade** | Burst cooldown — a talent that *replaces* Avenging Wrath, not an addition |
| **Hammer of Wrath** | Holy Power builder, conditional — an execute outside the burst window, unconditional inside it |
| **Divine Hammer** | Passive (Templar) — turns Divine Toll into sustained area damage |
| **Shield of Vengeance** | Personal defensive — **status contested, see below** |
| **Divine Protection** | Personal defensive — the cheap, frequent one |
| **Shield of the Righteous** | On the class line and pressable, but Ret spends Holy Power on damage; treat as a non-button |
| **Divine Shield** | Personal defensive — full immunity, the paladin bubble |
| **Lay on Hands** | Personal defensive — emergency full heal, self or ally |
| **Word of Glory** | Holy Power spender (heal) — competes directly with damage spenders |
| **Flash of Light** | Off-heal, downtime only |
| **Blessing of Freedom** | Group utility — external |
| **Blessing of Protection** | Group utility — external defensive |
| **Blessing of Sacrifice** | Group utility — external defensive |
| **Divine Steed** | Movement — the spec's only mobility cooldown |
| **Rebuke** | **The spec's only interrupt** |
| **Hammer of Justice** | Control — single-target stun |
| **Blinding Light** | Control — AoE disorient |
| **Turn Evil** | Control — creature-type gated, situational |
| **Hand of Reckoning** | Threat — ranged taunt |
| **Cleanse Toxins** | Dispel |
| **Intercession** | Battle resurrection (shares the raid pool) |
| **Redemption** | Out-of-combat resurrection |
| **Devotion Aura** | Group utility — raid aura |
| **Crusader Aura** | Group utility — travel aura |
| **Light Within** | Passive (apex) — amplifies the Art of War proc and the burst window |

⚠ **Shield of Vengeance may no longer be its own button at 12.0.7.** The
inventory row is a *new* spellID (1261562, not the historical 184662) whose
resolved tooltip reads "Divine Protection … **casts Shield of Vengeance**" —
i.e. an augment on Divine Protection rather than a cooldown of its own. But the
same row is flagged `castable` and is tracked by the Cooldown Manager, which
points the other way. One of those two signals is wrong and only the spellbook
settles it:

- Shield of Vengeance — is it a pressable button on the Ret bar, or does Divine Protection cast it? @verify-ingame

### What this table is protecting you from

`ability-inventory.md`'s **44 `class-baseline` rows are the whole Paladin skill
line, not Retribution's bar.** Eleven of them are mounts (Summon Charger,
Crusader's Direhorn, Summon Exarch's Elekk…); eight are Holy's (Beacon of Light,
Holy Shock, Holy Prism, Light's Hammer, Tyr's Deliverance, Protector of the
Innocent, Light of the Ancient Kings, Ancient Fury); two are Protection's
(Ardent Defender, Eye of Tyr); and Sense Undead, Contemplation, Jailer's
Judgment and Single-Button Assistant are not abilities in any useful sense.
`SkillLineAbility:800` is a **class** attachment and the generator is right to
emit it — but nothing in the generated layer says which of those Ret actually
uses, and that is this section's job.

## Reconciliation notes — Tier 1 @ 12.0.7.67808

Full adjudication history is in `../../_abilities/reconcile-ledger.md`. What is
still a live trap:

- **Concentration Aura is not acquirable at 12.0.7.** No spell of that name
  attaches to any acquisition table. Devotion and Crusader Aura are unaffected.
  A negative claim like this exists nowhere in the generated layer — a generated
  inventory lists what *is*, never what stopped being.
- **Templar Strike, Templar Slash and Hammer of Light are real pressed buttons
  with no acquisition row for this spec.** `Templar Strike` 407480 is *reached*
  — `section-3-corroborated.md` carries it `spec-exclusive` off an
  `EffectAura 332` row on `Templar Strikes` 406648. `Templar Slash` and `Hammer
  of Light` are in `section-4-catalogue.md`. ⚠ That catalogue is **not a
  backlog** and these are not scheduled. Their mechanics are not lost: the
  parent talent's own tooltip in `ability-inventory.md` (**Templar Strikes**
  406646) describes the full two-part combo, and Hammer of Light 427441 is
  literally `$@spelldesc427453`.
  ⚠ Absent from the join is **not** absent from game data — Hammer of Light has
  eight `SpellName` entries at 12.0.7.67808, is reached from **Light's Guidance
  427445** via `SpellEffect.EffectTriggerSpell`, and **Protection Paladin
  already carries it** as `Hammer of Light 1246643 cdm-only`, because
  `CooldownSetSpell` set 637 belongs to ChrSpecialization **66 (Protection)**.
  Templar is shared between Protection and Retribution, so the open question is
  narrow and checkable: **why does the mining place it for one spec and not the
  other?**
  *[Tier 1: DB2 @ 12.0.7.67808 — SpellName, SpellEffect, CooldownSet/CooldownSetSpell,
  ChrSpecialization.]*
- **Charge/recharge times are in neither layer.** The inventory's `cooldown` is
  `SpellCooldowns` at DifficultyID 0, which returns the **GCD** for a charge
  ability — Blade of Justice, Crusader Strike and Divine Steed all read 0 or
  sub-1s there. The real recharge lives in `SpellCategory.ChargeRecoveryTime`,
  unreachable without breaking the build pin (`reconcile-ledger.md` §5 G6). Do
  not read a sub-10s `cooldown` on a charge ability as the recharge.

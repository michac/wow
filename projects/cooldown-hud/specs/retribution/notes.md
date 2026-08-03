# Retribution Paladin — spec facts

Companion to `rotation.md` (the priority list of record). This file is the
**ability roster, the procs, and the resource mechanics** — the facts the list
assumes. Reference only; nothing here is a decision.

> **⚠ DESK-DERIVED, NOT FLOWN.** Every ID below is **Tier-1** (wago DB2 @ 12.0.7,
> fetched 2026-08-02: `CooldownSet` / `CooldownSetSpell` for the tracked set,
> `TraitNode`→`TraitDefinition` for talents, `SpellPower` for costs,
> `SpellCooldowns` + `SpellCategories` + `SpellCategory` for cooldowns).
> They are **not guesses**. What is unconfirmed is which of them the live Cooldown
> Manager actually tracks for a given build — `/cdmp hud layout` on a real
> Retribution character is the one-time check.

## Class + spec

- **Paladin**, `ChrClasses` 2, `SkillLine` 800.
- **Retribution**, `ChrSpecialization` **70**. One `CooldownSet`: **901**.
- Hero trees (`TraitSubTree`, tree 790): **Templar 48** (v1 profile),
  **Lightsmith 49** (Protection/Holy), **Herald of the Sun 50**.

## The tracked set — exactly what the CDM carries

Sourced from `CooldownSetSpell` where `CooldownSetID = 901`. Categories are
Blizzard's own (`Essential` / `Utility` / `TrackedBuff` / `TrackedBar`).

### Essential — the rotation buttons (9)

| Ability | ID | Cooldown | Source |
|---|---:|---|---|
| Templar's Verdict | 85256 | — | the ST spender, 3 Holy Power |
| Divine Storm | 53385 | — | the AoE spender, 3 Holy Power |
| Judgment | 20271 | 11s | charge category 1663, **1 charge** |
| Crusader Strike | 35395 | 6s | charge category 1627, **2 charges** |
| Blade of Justice | 184575 | 12s | charge category 2128, **1 charge** |
| Wake of Ashes | 255937 | 30s | charge category 2285, **1 charge** |
| Execution Sentence | 343527 | 60s | `RecoveryTime` |
| Divine Toll | 375576 | 60s | `RecoveryTime` |
| Avenging Wrath | 31884 | 120s | `CategoryRecoveryTime` |

⚠ **Four of the nine keep their cooldown on a CHARGE CATEGORY** (Judgment 1663,
Crusader Strike 1627, Blade of Justice 2128, Wake of Ashes 2285), so
`SpellCooldowns.RecoveryTime` is 0 and `GetSpellBaseCooldown` yields nothing for
`HudNapkin` to count down from.

⚠ **This said "six" until 2026-08-03.** Avenging Wrath is not one — it carries
`CategoryRecoveryTime = 120000` on the spell row. Templar's Verdict and Divine Storm read 0
because they have no cooldown *at all*. And the earlier list named Hammer of Wrath, which is
not among the nine.

⚠ **And the consequence is narrower than the old wording claimed.** Readiness for those four
does **not** rest on the napkin — it comes from the **charge count**, seeded out of combat
and maintained in combat off the `ChargeGained` alert, with the charge-category recovery as
its **gain floor** (`ns.ReadCharges`' third return → `State.chargeGain`, already wired). What
is genuinely lost is the **`SOON`** decoration and **`Escalate`'s overdue** signal, which need
a positive `remaining`. Destruction has shipped this exact shape for Conflagrate (category
672, 2 charges, `RecoveryTime` 0) since field-fix C2 — Retribution differs only in count.

### TrackedBar (7)

Blessing of An'she 445206 · Execution Sentence 343527 · Shake the Heavens 431536 ·
Divine Hammer 432929 · Avenging Wrath 31884 · Divine Resonance 384029 ·
Crusading Strikes 404542.

### TrackedBuff — the procs (the ones the list reads in **bold**)

**Art of War 406064** · **Righteous Cause 402912** · **Empyrean Power 326732** ·
**Empyrean Legacy 387170** · **Light's Deliverance 433674** · Divine Purpose 408459 ·
Expurgation 383344 · Undisputed Ruling 432626 · Dawnlight 431377 · Sun Sear 431413 ·
Greater Judgment 231663 · Judge, Jury and Executioner 406157 · Rush of Light 407067 ·
Sacrosanct Crusade 431730 · Sanctification 432977 · Sanctify 382536 ·
Shield of Vengeance 1261562 · Will of the Dawn 431406 · Judgment of Justice 403495 ·
Templar Strikes 406646 · the 12.1 class-set 2pc/4pc 1296660 / 1296661.

### Utility (15)

Divine Steed 190784 · Divine Protection 403876 · Rebuke 96231 ·
Hammer of Justice 853 · Blinding Light 115750 · Cleanse Toxins 213644 ·
Turn Evil 10326 · Divine Shield 642 · Lay on Hands 633 · Blessing of Freedom 1044 ·
Blessing of Sacrifice 6940 · Blessing of Protection 1022 ·
Blessing of Spellwarding 204018 · Blessing of Sanctuary 210256 · Intercession 391054.

Utilities are never scored, never cued, and excluded from the SOON decoration.

## The overrides — abilities with no icon of their own

This is the spec's structural signature and the reason the Templar profile is
readable at all. Four rotation abilities are **spell overrides that ride a tracked
frame**, the same channel Demonology's Ruination and Destruction's Infernal Bolt
use (`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` + live-identity divergence).

| Override | ID | Rides | Comes from |
|---|---:|---|---|
| **Hammer of Light** | 427453 | the spender frame | Templar (Wake of Ashes arms it) |
| **Final Verdict** | 383328 | Templar's Verdict 85256 | a class talent |
| **Templar Strike** | 407480 | Crusader Strike 35395 | Templar Strikes 406646 |
| **Templar Slash** | 406647 | Crusader Strike 35395 | the follow-up to Templar Strike |
| **Templar Sweep** | 406661 | Crusader Strike 35395 | the AoE member of the same chain |

⚠ **Hammer of Light 427453 was discriminated Tier-1, not guessed.** `SpellName`
carries **eight** "Hammer of Light" rows (160420, 160426, 427441, 427453, 429826,
1217116, 1235934, 1246643) and nothing in the name tells them apart. `SpellPower`
does: **exactly one of them costs Holy Power** (`PowerType 9, cost 3`), the same
signature Templar's Verdict, Divine Storm and Final Verdict carry. That is the
Paladin spender. Recording the *method* here because the next spec will hit the
same wall — a homonym is resolved by a **property only the real spell has**, never
by picking the plausible-looking number.

Templar Strike 407480 corroborates independently: it shares Crusader Strike's
**charge category 1627**, which is what an override of Crusader Strike must do.
⚠ Only *Strike* shares it — **Slash and Sweep have `ChargeCategory 0`**, because they are
chain follow-ups rather than independent presses. That is precisely why the brain presses the
**frame** and lets the game choose.

**Herald's spender is missing from the tracked set too.** **Eternal Flame 156322** is a real
3-Holy-Power finisher `[T1 DB2: SpellPower @ 12.0.7; the KB's talents.md marks it ACTIVE]`
with no icon of its own. Registered with `expect = false` — which keeps it out of
`State.virtualCandidates`, because a self-drawn button no priority line ever cues would be
worse than none at all.

## Holy Power

- `Enum.PowerType.HolyPower` = **9** (offline-confirmed,
  `BlizzardInterfaceResources/Resources/LuaEnum.lua:5691`).
- Range **0–5**, `modifier` **1** — so the exact rail (`unmodified`) and the display
  rail are the same integer. **None of Destruction's fragment arithmetic applies.**
- **Every spender costs 3** `[T1 DB2: SpellPower @ 12.0.7]`. The KB's "spend at 5"
  is a pooling rule, not a cost.
- Generators: Judgment, Crusader Strike (and its Templar overrides), Blade of
  Justice, Hammer of Wrath, Wake of Ashes, Divine Toll. Exact yields are talent-
  modified and are **deliberately not projected** — see `SpecRetribution.lua`'s
  `SpecPowerDelta`, which projects **spenders only**, for the same reason
  Destruction's builder half waited for a measurement: an over-credited generator
  promises a spender you cannot cast.

## Procs, and what each one actually gates

| Proc | ID | What it does | Read as |
|---|---:|---|---|
| Art of War | 406064 | free instant Blade of Justice | presence (L7) |
| Righteous Cause | 402912 | same slot as Art of War | presence (L7) |
| Empyrean Power | 326732 | next Divine Storm is free | presence (spender choice) |
| Empyrean Legacy | 387170 | next Templar's Verdict cleaves | presence (**suppresses** DS) |
| Light's Deliverance | 433674 | a **free** Hammer of Light | presence (parked — see below) |
| Divine Purpose | 408459 | next spender is free | registered, **not gated on** |
| Undisputed Ruling | 432626 | Templar window buff | registered, not gated on |
| **Crusade** | **1253598** | the Avenging Wrath **alternative** | presence, **ORed into `wingsUp`** (L9) |

⚠ **Every one of these is presence-only.** Stack counts and durations are Secret
Values in combat, which is what kills all four of simc's free-Hammer-of-Light
timing clauses (rotation.md Deviation 1).

⚠ **Only ONE of them actually stacks, and it is the one that matters.**
`SpellAuraOptions.CumulativeAura` @ 12.0.7 over the whole tracked set: **Light's Deliverance
= 60**, Blessing of An'she = 2 (Herald, not gated on), and **every other proc = 0**, i.e.
binary. So presence genuinely *is* the whole signal for Art of War, Righteous Cause, Empyrean
Power, Empyrean Legacy and Divine Purpose — those gates are sound.
Light's Deliverance at **60 stacks** is present for essentially the whole fight and only its
60th stack grants the free hammer. That makes `RET_HOL_FROM_BUFF` a switch that can never
safely be turned on: the count is a Secret Value in combat, so the alternative reading is not
merely risky, it is unreachable. Kept as a documented dead end rather than deleted, because
the *reason* is the useful artefact.

## Hammer of Wrath — the one button with no home

**Not in the tracked set at all.** Three Paladin-side IDs exist and they are not
interchangeable:

- **24275** — the class skill-line spell (`SkillLineAbility`, `SkillLine` 800,
  `ClassMask` 2). Charge category **1895**, 7.5s, 1 charge.
- **326730** — a second skill-line row, same class mask.
- **1241288** — the Midnight **talent-node** spell (Paladin tree 790, base subtree).

`SpecRetribution.lua` registers **24275** as primary — it is the one carrying the charge
category and the cooldown data, and the KB's `talents.md` marks 1241288 `PASSIVE`, i.e. the
node that *grants* the ability rather than the castable. The other two are `expect = false`
aliases, so only one virtual icon can ever be drawn.

⚠ **"Whichever the client surfaces resolves the same cue" was a claim with nothing behind it
until 2026-08-03.** The brain asked for 24275 alone. `CoachRetribution:Context` now walks the
three candidates and publishes `ctx.howKey` (the `ctx.dotID` pattern), so the sentence is
finally true. Which id is live is still `@verify-ingame`.

## What is deliberately absent

- **The nine dormant Tier-3 tables** (`SpecGroups` / `SpecColor` / `SpecPole` /
  `SpecGhost` / `SpecNoCue` / `SpecProcGlow` / `SpecStacks` / `SpecOpener` /
  `SpecBurst`). None has a live consumer in v1. `SpecDestruction.lua` omitted all
  nine and nothing broke; this file follows it, not Demonology.
- **A defensive channel.** Divine Shield, Lay on Hands, Divine Protection and Word
  of Glory are registered as utilities and never cued. A health-gated defensive
  cue would need a new emphasis token — a `guidance-contract.json` change — and is
  explicitly out of scope.
- **A burst-window staging block.** Retribution holds nothing for Avenging Wrath
  the way Demonology holds demons for Tyrant, so there is no `tct`, no `stage`, no
  go-gate and no window suppression in `Escalate` — structurally Destruction, not
  Demonology.

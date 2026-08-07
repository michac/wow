---
title: Retribution Paladin — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — resolved Blizzard spell-API tooltips, fetched 2026-08-06
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — reached-but-not-joined names
  - ../../_abilities/section-4-catalogue.tsv  # tier 1 derived — the unreached-name catalogue
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's earlier claims
confidence: high
---

# Retribution Paladin — off-inventory abilities

**Everything about a Retribution ability is in `ability-inventory.md`** — 187
rows, one row each carrying spellID, cooldown, cast time, origin, talent/hero
placement and the full tooltip. It is generated, Tier-1, DB2-pinned to
`12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Retribution ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation, priority and Holy-Power costs
> → `rotation.md`. Talents/hero pick → `builds.md`, `talents.md`. Both sections
> here are **closed lists, not backlogs.**

⚠ One caveat the inventory cannot flag: its **44 `class-baseline` rows are the
whole Paladin skill line, not Retribution's bar** — eleven mounts, eight of
Holy's (Beacon of Light, Holy Shock, Holy Prism, Light's Hammer, Tyr's
Deliverance …), Protection's Ardent Defender and Eye of Tyr, plus Sense Undead
and Contemplation. `SkillLineAbility:800` is a *class* attachment and the
generator is right to emit it; nothing generated filters it to a spec.

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.** All three Templar rows below are the same phenomenon: a hero
tree whose buttons are *replacements*, granted by a passive rather than learned.

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `407480` | Templar Strike | The first half of the combo `Templar Strikes` `406646` turns Crusader Strike into; that parent talent's Tier-1 tooltip describes it in full. Already catalogued in `section-3-corroborated.tsv` as `override-aura` / `spec-exclusive`, reached via `SpellEffect.EffectAura 332` on `Templar Strikes` 406648 — **reached, but never joined**, so it has no inventory row. |
| — | Templar Slash | The second half of the same combo — *"Templar Strike … gets followed up by Templar Slash that deals 51 Radiant damage. Templar Slash always critically strikes"* (`Templar Strikes` 406646, Tier-1 resolved tooltip). No acquisition row of its own at 12.0.7.67808; catalogued `prose-only` in `section-4-catalogue.tsv`. ⚠ Its spell endpoint returned no 200 — **not** evidence of absence. |
| `427441` | Hammer of Light | **The Templar spender.** Granted by `Light's Guidance` `427445` (talent-passive, Templar, in this spec's inventory) — *"Wake of Ashes is replaced with Hammer of Light for 20 sec after it is cast"* — and reached from it via `SpellEffect.EffectTriggerSpell`, which is how `section-4-catalogue.tsv` carries it as `trigger-effect`. It is a *replacement*, so no acquisition table ever names it. Five more Templar passives in the inventory (Light's Deliverance, Sacrosanct Crusade, Shake the Heavens, Undisputed Ruling, Zealous Vindication) describe its behaviour. ⚠ 427441 and 427453 both 404 on the spell endpoint and are demonstrably live. ⚠ **Cost conflict: read `rotation.md`, not the tooltip** — Light's Guidance renders *"Costs 5 Holy Power"* while DB2 `SpellPower` reads `PowerType 9, cost 3` for 427453. Shared hero-tree passives resolve without spec context (`prose-conventions.md` §7), so the 5 is likely Protection's. |
| — | Concentration Aura | **Granted by the class-tree talent `Auras of the Resolute` `385633`** (node 102587, all three Paladin specs in `all-talents.tsv`), whose Tier-1 resolved tooltip reads *"**Learn Concentration Aura**, Devotion Aura, and Crusader Aura … Concentration Aura: Interrupt and Silence effects on party and raid members within 40 yds are 30% shorter."* `Aura Mastery` `31821` still carries a *"Concentration Aura: Affected allies immune to interrupts and silences"* clause. The aura has **no acquisition row of its own** (79963 / 81455 / 317920 / 344220 attach to nothing) — Devotion, Crusader and Retribution Aura each have a `class-baseline SkillLineAbility:800` row and this one does not. **This reverses the old "not acquirable" verdict — see Corrections.** |

⚠ **The open oddity, recorded not resolved:** Templar is shared between Protection
and Retribution, yet **Protection's inventory already carries Hammer of Light** as
`1246643 cdm-only`, because `CooldownSetSpell` set 637 belongs to
ChrSpecialization **66 (Protection)**. Retribution gets nothing. Same hero tree,
same button, one-sided mining. *Why the mining places it for one spec and not the
other is unanswered — do not "fix" it here.*
*[Tier 1: DB2 @ 12.0.7.67808 — SpellName, SpellEffect, CooldownSet/CooldownSetSpell,
ChrSpecialization.]*

## §B — Encountered, and we believe not valid

_None recorded for this spec._ The only negative claim this file used to carry —
*"Concentration Aura is not acquirable at 12.0.7"* — is **wrong**, and the name
has moved to §A.

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Concentration Aura` is acquirable at 12.0.7 — the old verdict was wrong.**
  Every Paladin `abilities.md`, `reconcile-ledger.md` and
  `../../_abilities/prose-conventions.md` §6 currently state the opposite —
  prose-conventions even uses it as its worked example of a negative claim. The
  measurement behind it is sound (no spell of that name attaches to anything) but
  the **conclusion does not follow**: the aura is granted by a *talent*. See §A.
- **The Holy-Power cost paragraph moved, it was not deleted.** *Every* Retribution
  finisher costs **3** Holy Power — Templar's Verdict 85256, Divine Storm 53385,
  Final Verdict 383328, Hammer of Light 427453 all read `PowerType 9, cost 3`
  *[T1 DB2: SpellPower @ 12.0.7]*, and "spend at 5" is a **pooling** rule, not a
  cost. That now lives in `rotation.md` (its ⚠ COST vs POOLING block). The
  generated inventory has **no cost column at all**, so `rotation.md` is the only
  record — do not re-derive it from a tooltip.

## Open in-game questions

One, and it needs the spellbook — no table settles it:

- Is `Shield of Vengeance` 1261562 a pressable button on the Ret bar, or does Divine Protection cast it? Its inventory row is `talent-active` + `castable` and the Cooldown Manager tracks it, but its own resolved tooltip reads *"Divine Protection reduces damage taken by an additional 10% **and casts Shield of Vengeance**"*. The two signals disagree; only the spellbook decides. @verify-ingame

---
title: Holy Priest — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's earlier claims @ 12.0.7.67808
confidence: high
---

# Holy Priest — off-inventory abilities

**Everything about a Holy ability is in `ability-inventory.md`** — 162 rows, one
row each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Holy ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist, but no spec-keyed acquisition table names them, so they will
never appear in `ability-inventory.tsv`. **Absence there is not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `77485` | Mastery: Echo of Light | ⚠ **This name looks like a harvest artifact and is reproduced verbatim anyway.** It is a **mastery — a passive, not a pressed button** — so it does not belong in a section headed "real buttons"; a separate deliberate pass owns fixing that, and not-losing-data and improving-data are different jobs. The row is still *true*: `77485` **is** attached (`SpecializationSpells` → Holy), but `wowkb.gen_abilities` drops passive `SpecializationSpells` rows, so neither the row nor its tooltip reaches the inventory. **Tool gap, not absence.** What *is* in the inventory is the downstream HoT `Echo of Light` `77489` (`class-baseline`, *"Heals every 2 sec for 4 sec."*) and `Prismatic Echoes` `390967`, whose tooltip names the mastery outright. |

**This category is real and measured, not an edge case.** Across all 40 specs,
runtime override / proc-replacement buttons live in no spec-keyed DB2 table:
`Devour`, `Pierce the Veil`, `Templar Slash`, `Void Volley` and `Heroic Strike`
are all real pressed buttons whose *only* record anywhere is a hand-written row
like this one. Holy's single entry is the odd one out — a passive caught by the
same generator gap rather than an override button.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Heal | **not acquirable — the button is gone** | `2060` attaches to no trait node, `SkillLineAbility` (Priest line **804**), `SpecializationSpells` or `PvpTalent` @ 12.0.7.67808, and none of the other 112 spells named "Heal" attaches either. It survives only as a *trigger effect* reached from `Lightweaver` `390993` (catalogued `trigger-effect` in `section-4-catalogue.tsv`) — and Lightweaver's live 12.0.7 tooltip is about **Flash Heal → Prayer of Healing**, not Heal. Not a button. |
| Renew | **not acquirable as a button** | `139` attaches to nothing: not on SkillLine 804, not on tree **795** (which has `Renewed Faith`, not Renew). ⚠ **The buff still exists and is still applied to you** — `Lasting Words` puts *"12 sec of Renew"* on a Serenity target and 6 sec on Sanctify targets, and `Prismatic Echoes` boosts *"your Renew by 13%"*. So a tooltip naming Renew is **not** evidence you can cast it. **You cannot pre-apply it.** |
| Circle of Healing | **not acquirable** | `204883` and the other 5 IDs attach to nothing; no node on tree 795; the name appears in **zero** tooltips across all three Priest inventories. Not a talent, not a hidden pick. |
| Silence | **Shadow's, not Holy's** | `15487` appears in **`priest/shadow/ability-inventory.tsv` only** (`class-baseline`), in neither Holy's nor Discipline's. **Holy has no interrupt and no school lockout.** `Holy Word: Chastise` `88625` is the nearest thing — which is why the BucketBinds seed files it under `Interrupt` — but it is an incapacitate, not a lockout, and does not answer a "kick this cast" call. |
| battle rez (Rebirth / Raise Ally / Intercession / Soulstone) | **Priest has none, in any spec** | zero rows matching those four names across all three Priest inventories. `Resurrection` `2006` and `Mass Resurrection` `212036` are both out-of-combat; `Spirit of Redemption` `215769` is a self-effect, not a rez of someone else. |

⚠ **The last two rows are absences, and they matter for group composition** — no
kick, no combat rez. A generated inventory structurally *cannot* say this: it
lists what a spec learns, never what it lacks. If this section is lost, the KB
silently re-acquires The War Within's kit the next time someone reads a guide.

*[Tier 1: `all-talents.tsv` + the three Priest `ability-inventory.tsv` files, both
@ 12.0.7.67808; adjudicated in `../../_abilities/reconcile-ledger.md`.]*

## Open in-game questions

Both are genuinely unreachable from Tier-1 data — not "the guide's number looks
uncertain", but "no table we can read carries this at all".

- Holy Word: Serenity `2050`, Holy Word: Sanctify `34861`, Prayer of Mending `33076`, Shadow Word: Death `32379`, Leap of Faith `73325` — the inventory reads their cooldown as 0/~1.5s because `SpellCooldowns`@Difficulty 0 returns the **GCD** for a charge ability; the real recharge is `SpellCategory.ChargeRecoveryTime`, unreachable without breaking the build pin. Read baseline cooldown + charge count off each spellbook tooltip. **For a healer this is the most load-bearing missing number in the KB — Holy Word charge cadence *is* the rotation.** @verify-ingame
- Mastery: Echo of Light `77485` — the generator drops it, so no tooltip exists in either layer. Read the % of the heal it echoes and the HoT duration off the spellbook. @verify-ingame

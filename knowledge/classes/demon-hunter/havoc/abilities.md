---
title: Havoc Demon Hunter — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the DH verdicts, §4 + §5 G1/G2
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec acquisition union
  - ./maxroll-raid.md  # tier 3 verbatim capture, maxroll_updated 2026-06-19 — Midnight removal list + spellIDs
confidence: high
---

# Havoc Demon Hunter — off-inventory abilities

**Everything about a Havoc ability is in `ability-inventory.md`** — 149 rows, each
carrying spellID, cooldown, cast time, origin, talent/hero placement and the full
tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Havoc ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Havoc is the worst-affected spec in the class: its whole demon-form kit is runtime
**overrides**, and an override has no acquisition row, so it can never appear in
`ability-inventory.tsv`. **Absence there is not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `452497` | Abyssal Gaze | Fel-Scarred's **Demonic Intensity** override of **Eye Beam** inside Metamorphosis. Subtree 34 Fel-Scarred is live on tree 854 with `Demonsurge` `452402` + `Demonic Intensity` `452415`, and `Eye Beam` `198013` is `talent-active` in the tsv. The override button itself has no acquisition row. Tool gap **G2**. |
| — | Annihilation | **The demon-form replacement of Chaos Strike.** `Metamorphosis` `191427` and `Chaos Strike` `344862` are both `class-baseline` in the tsv; the replacement is a pure runtime override with no acquisition row. Tool gap **G2**. ⚠ The maxroll capture links `201427`; that is Tier-3 and no Tier-1 read has confirmed it. **This prose is the only record of the button anywhere.** |
| `452487` | Consuming Fire | Same Fel-Scarred path — the Demonic Intensity override of **Immolation Aura** `258920` (`class-baseline`, present). Also minted as `456640`. Tool gap **G2**. |
| — | Death Sweep | **The demon-form replacement of Blade Dance** `188499` (`class-baseline`, present); shares Blade Dance's cooldown. Tool gap **G2**. ⚠ maxroll links `210152` — Tier-3, unconfirmed. **This prose is the only record of the button anywhere.** |
| `1283344` | Reaver's Glaive | Aldrachi Reaver's proc button: **Art of the Glaive** `442290` (subtree 35, live on tree 854) converts your next Throw Glaive into it. `1283344` is a Midnight-range `SpellName` ID with no acquisition row. ⚠ The maxroll capture links `442294`, a War Within-era ID — **Tier 1 is the floor, so `1283344` is the one to carry.** |
| `203555` | Demon Blades | **Not a mandatory row — added by this pass.** Passive Fury-from-auto-attacks that *overrides* `Demon's Bite` `344859`. It is absent from `ability-inventory.tsv`, `all-talents.tsv` and `all-abilities.tsv` for **all 40 specs**, i.e. both the **G1** passive-drop and the **G2** override holes at once. The 12.0.7 maxroll capture (Tier 3) states the Demon's Bite / Demon Blades choice node "is removed entirely, and Demon Blades is now baseline". Asserted here so it is tracked, not so it is trusted. |

## §B — Encountered, and we believe not valid

Checked, and believed **not** part of this spec at 12.0.7. Listed so the next
reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Fel Barrage | **removed from the game at 12.0.7** | 21 spells carry the name in `SpellName` @ `67808` and **none** attaches to a trait node, `SkillLineAbility`, `SpecializationSpells` or `PvpTalent`. Max ID is `400185`, a War Within leftover — no Midnight-range ID was ever minted, and tree 854 has no node. The Tier-3 12.0.7 capture agrees ("now removed"). There is no button; do not re-add it from a pre-Midnight guide. |
| Sigil of Spite | **Vengeance-only** | `all-talents.tsv` @ `67808`: `Sigil of Spite` `390163` reaches demon-hunter/**vengeance** node `90978` and nothing else. Havoc's tsv carries Sigil of Misery and Sigil of Flame, no Sigil of Spite. ⚠ Havoc's *generated* Art of the Glaive tooltip does say "casting Sigil of Spite" — that is shared hero-tree tooltip text, not a Havoc button. |
| Fel Eruption | **removed at 12.0.7** | Zero rows in `all-talents.tsv` and `all-abilities.tsv` across all 40 specs. The capture names its replacement: `Focused Ire` `1266296`, a class-tree passive that is present for all three DH specs and adds 2s to Chaos Nova's stun on the primary target. |
| Shear | **retired name that still appears in a live tooltip** | Zero rows in `all-talents.tsv` and `all-abilities.tsv` for any spec @ `67808`. It survives only inside the Aldrachi Reaver tooltip text both DH specs inherit ("enhancing your next Shear and Soul Cleave"). Havoc's empowered casts are Chaos Strike and Blade Dance. |

*[Tier 1: `all-talents.tsv` + `all-abilities.tsv` @ `12.0.7.67808`, plus
reconcile-ledger §4.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **Havoc still has `Sigil of Flame` `204596`** — `class-baseline` for all three DH
  specs in `all-abilities.tsv` @ `67808`. The maxroll capture sitting in this
  folder says it "has been made unique to the Vengeance spec"; that is Tier 3 and
  Tier 1 contradicts it. Do not delete the Havoc row on the strength of the guide.
- **Blade Dance's base cooldown is 15s**, not the ~9s guides quote — the shorter
  figure is the *hasted* value. Eye Beam is **30s**, not ~40s. Both are in the
  generated inventory; an earlier revision of this file guessed and marked them.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact Fury cost is
uncertain"* is **not** one; and the five override buttons above are settled as
*tool gaps*, not as unknowns.

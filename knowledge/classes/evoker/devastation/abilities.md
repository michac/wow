---
title: Devastation Evoker — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — spells reached indirectly
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the verdicts applied 2026-08-06
confidence: high
---

# Devastation Evoker — off-inventory abilities

**Everything about a Devastation ability is in `ability-inventory.md`** — 150
rows (specID 1467), each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Devastation ability is not named below, do not research it — read its
> row in `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero
> pick → `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is
not absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the
> `name` column of the table below — the heading is matched on the word
> **`inventory`** — and feeds it to the `prose-only` leg of
> `section-4-catalogue`. Rename this heading or drop the `name` column header
> and these rows **silently vanish from the catalogue**, with no marker and no
> warning. §B is deliberately *not* harvested: it asserts the opposite.

_None known for this spec._

Every ability name the previous hand-written prose listed resolves to a row in
this spec's `ability-inventory.tsv`. The two override-reached spells
(**Breath of Eons** `403631` off *Maneuverability*, **Upheaval** `396286` /
**Dream Breath** `355936` off *Font of Magic*) are already recorded in
`../../_abilities/section-3-corroborated.tsv` and do not belong here.

## §B — Encountered, and we believe not valid

Names that appear in guides, older builds or other people's notes, which we have
checked and believe are **not** pressable buttons for this spec at 12.0.7.
Listed so the next reader stops here instead of re-running the check.

| name | verdict | evidence |
|---|---|---|
| Engulf | **does not exist at 12.0.7** | Zero rows named Engulf in `all-talents.tsv` across **all 40 specs**, in any of the three Evoker `ability-inventory.tsv`, or in `section-3-corroborated.tsv` / `section-4-catalogue.tsv`. The **Flameshaper** subtree *is* live on the Evoker tree (872): its 17 Devastation entries enumerate in full as Legacy of the Lifebinder · Trailblazer/Shape of Flame · Ashes in Motion · Enkindle/Expanded Lungs · Essence Well · Conduit of Flame · Burning Adrenaline · Fulminous Roar · Twin Flame · Titanic Precision · Deep Exhalation · Lifecinders/Draconic Instincts · **Fire Torrent** `1265992` · **Consume Flame** `444088` — no Engulf. Nearest live name is **Engulfing Blaze** `370837` (`talent-passive`), which is not it. ⚠ **Do not file Fire Torrent as a rename of Engulf** — nothing measured says the two are the same button. ⚠ And note both replacements are `talent-passive` / `castable=false` / `node_type=PASSIVE`: the Devastation Flameshaper subtree has **zero ACTIVE nodes** at 12.0.7, so the common phrasing "Flameshaper's actives are Fire Torrent and Consume Flame" overstates what the data says. |
| Firestorm | **not a talent — a triggered sub-spell** | Zero rows named Firestorm in `all-talents.tsv` across all 40 specs, so the "AoE-lean talent" it used to be listed as is a War Within-era carry-over. What survives is inside **Feed the Flames** `369846` (`talent-passive`): *"After casting 6 Pyres, your next Pyre will explode into a Firestorm."* It is an effect of pressing Pyre, not its own button. |
| Shattering Star | **retired active; the survivor is a passive** | The War Within's instant ~20s-CD *Shattering Star* is gone. Live is **Shattering Stars** `1265802` — `all-talents.tsv` devastation node 93316 `node_type=PASSIVE`, entry 115627, and the spec tsv agrees (`talent-passive`, `castable=false`). ⚠ Worth stating both signals: `node_type` is an **independent** check from the `castable` column, and 45 rows elsewhere read passive wrongly on `castable` alone — this verdict does not rest on that column. |
| Mass Disintegrate `401642` | **wrong ID; the mechanic is real** | `401642` is a bare `SpellName` hit with **no acquisition row for this spec** — and a `SpellName` hit is not evidence a spec can cast anything, that table keeps retired spells indefinitely. The live row is **Mass Disintegrate** `436335`, `talent-passive`, Scalecommander node 94939 (`node_type=PASSIVE`). Not a button either way: empowers grant charges that upgrade your next Disintegrate. |

*[Tier 1: `all-talents.tsv` + `ability-inventory.tsv` @ 12.0.7.67808;
reconcile-ledger.md §4.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Return` `361227` is the Evoker battle res, not a teleport.** Tooltip:
  *"Brings a dead party member back to life with 35% health and mana. Cannot be
  cast when in combat."* — `class-baseline`, 10s cast. An earlier revision
  described it as a "bronze teleport back to a stored location". The same wrong
  line was carried by all three Evoker specs.
- **`Unravel` `1264378` is a PASSIVE in Midnight** — `talent-passive`,
  `castable=false`, class tree. Its tooltip is *"Direct damage from Fire Breath
  consumes absorb shields from enemies"*, i.e. it is no longer the old
  1-Essence instant shield-shatter you press. Do not re-add it as an active.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cast
time is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number.

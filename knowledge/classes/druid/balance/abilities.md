---
title: Balance Druid — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree @ 12.0.7.67808
  - ../../_abilities/all-abilities.tsv  # tier 1 — the 40-spec union, for absence checks
  - ../../_abilities/spell-descriptions.tsv  # tier 1 — resolved English tooltips via /data/wow/spell/{id}
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file
confidence: high
---

# Balance Druid — off-inventory abilities

**Everything about a Balance ability is in `ability-inventory.md`** — 197 rows
(specID 102), one row each carrying spellID, cooldown, cast time, origin,
talent/hero placement and the full tooltip. It is generated, Tier-1, DB2-pinned
to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Balance ability is not named below, do not research it — read its row
> in `ability-inventory.md` and go.** Rotation, Eclipse handling and the Moon
> chain's place in the priority → `rotation.md`. Talents/hero pick → `builds.md`.
> Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue.md`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

All three are **sequential override buttons** — a spell that replaces another
spell on the bar. An override has no acquisition row of its own; only its parent
does. That is the whole reason the join misses them.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `` | Half Moon | The parent **New Moon** `274281` is a real talent-choice row, and its own Tier-1 tooltip says it *"empowers New Moon to become **Half Moon**"*. **Radiant Moonlight** `394121` names all three: *"New Moon, Half Moon, and Full Moon deal 25% increased damage."* The chain is real; only step 1 is acquirable. |
| `` | Full Moon | Same chain, step 3. Named in **Radiant Moonlight** `394121`, **Orbit Breaker** `383197` (*"calls down a Full Moon"*) and **Boundless Moonlight** `424058` / **The Eternal Moon** `424113`, which have Full-Moon-specific clauses. |
| `` | Lunar Eclipse | **Eclipse** `1239669` is one talent whose tooltip states the two modes *"share a button and 32 sec cooldown"*. Its **Solar** half squeaks into the inventory as a `cdm-only` row (`Solar Eclipse` `1233346`, via CooldownSetSpell); the Lunar half has no such row and so vanishes. Both are named as real cooldown-bearing things by **Sculpt the Stars** `1240188` and **Improved Eclipse** `1240906`. |

Catalogued `prose-only` in `../../_abilities/section-4-catalogue.md`. ⚠ That
catalogue is **not a backlog** — these are not scheduled for investigation, and
logging in cannot answer a question about which DB2 table carries an acquisition
row.

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Renewal | **removed from the class tree** | Zero rows in `all-talents.tsv` for **any** of the 40 specs, and zero in `all-abilities.tsv`. The only surviving near-match is the unrelated passive **Aessina's Renewal** `474678` (class tree, row 7). Personal healing is Barkskin, Regrowth and Frenzied Regeneration in Bear. |

*[Tier 1: DB2 @ 12.0.7.67808 via `all-talents.tsv` + `all-abilities.tsv`;
`_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **`Sunseeker Mushroom` `468936` is a PASSIVE proc, not a pressed spender.**
  Tier-1 tooltip: *"Sunfire damage has a chance to grow a magical mushroom…
  detonates… Generates up to 20 Astral Power based on targets hit."* An earlier
  revision listed it as a *"choice-node variant of Wild Mushroom"* costing Astral
  Power with charges — i.e. as a keybind. It is `talent-passive`,
  `castable=false`. **Wild Mushroom** `88747` is the pressed one.
- **`Ascendant Eclipses` `1261564` is a PASSIVE.** Its tooltip is entirely
  conditional (*"Activating an Eclipse makes your next Wrath or Starfire
  instant…"*). ⚠ Worth stating because `all-talents.tsv` records this node's
  `node_type` as **`ACTIVE`** — that column describes the *node*, not the granted
  spell, and is **not evidence of a button**. Don't keybind it.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown / cast
time is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number (Eclipse's real cooldown, for instance, is **32s**, not the ~40s an
earlier revision guessed at).

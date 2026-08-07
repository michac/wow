---
title: Frost Mage — off-inventory abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - ./ability-inventory.md  # tier 1 — the generated inventory this file supplements, DB2 @ 12.0.7.67808
  - ../../_abilities/pet-family-annex.tsv  # tier 1 — pet skill lines @ 12.0.7.67808
  - ../../_talents/all-talents.tsv  # tier 1 — every spec's talent tree
  - ../../_abilities/reconcile-ledger.md  # tier 1 derived — per-row verdicts
  - ../../_abilities/section-3-corroborated.tsv  # tier 1 derived — indirect reaches
confidence: high
---

# Frost Mage — off-inventory abilities

**Everything about a Frost ability is in `ability-inventory.md`** — 211 rows, one
row each carrying spellID, cooldown, cast time, origin, talent/hero placement and
the full tooltip. It is generated, Tier-1, DB2-pinned to `12.0.7.67808`.

**This file holds only the two things that generated file structurally cannot
say**, because it is a *join*: a row exists there because a Tier-1 acquisition
table says this spec **learns** the spell. It can only ever list what **is**.

> ⛔ **If a Frost ability is not named below, do not research it — read its row in
> `ability-inventory.md` and go.** Rotation → `rotation.md`. Talents/hero pick →
> `builds.md`. Both sections here are **closed lists, not backlogs.**

## §A — Real buttons the inventory cannot see

Confirmed to exist and be pressable, but no spec-keyed acquisition table names
them, so they will never appear in `ability-inventory.tsv`. **Absence there is not
absence in game.**

> ⚠ **This section is a machine input.** `wowkb.gen_abilities` harvests the `name`
> column of the table below — the heading is matched on the word **`inventory`** —
> and feeds it to the `prose-only` leg of `section-4-catalogue`. Rename this
> heading or drop the `name` column header and these rows **silently vanish from
> the catalogue**, with no marker and no warning. §B is deliberately *not*
> harvested: it asserts the opposite.

| spellID | name | how we know, and why the join misses it |
|---|---|---|
| `33395` | Freeze | **Your Water Elemental's AoE root**, the Shatter/kite setup. It is on the **Pet - Water Elemental** skill line (805), not yours — the pet path has no spec granularity in any DB2 table, so no row can attribute it to Frost. In `../../_abilities/pet-family-annex.tsv`. ⚠ **Only exists while the elemental is out**, i.e. *Summon Water Elemental* `31687` over *Lonely Winter*. Also reached independently in `section-3-corroborated.tsv` via a spell-endpoint probe, but under a **different spellID (`27867`)** — treat `33395`/SkillLine 805 as the pet button; the discrepancy is unresolved and deliberately not "fixed" here. |
| | Splinters | ⚠ **Looks like a harvest artifact and is kept anyway** — the previous prose had a row literally titled *"Frozen Orb / Splinters"*, and the machine-tracked `prose-only` catalogue entry inherited the bare word. There is no spell named `Splinters`; the real objects are **Arcane Splinter** projectiles conjured by Spellslinger passives (*Splintering Sorcery* `443739`, *Splintering Orbs* `444256`, *Infused Splinters* `1261080`, *Splinterstorm* `443783` — all `talent-passive` in `ability-inventory.tsv`, none pressed). **Not corrected here on purpose**: a separate deliberate pass owns renaming/retiring artifact rows, and losing data and improving data are different jobs. |

## §B — Encountered, and we believe not valid

| name | verdict | evidence |
|---|---|---|
| Icy Veins | **gone — no Frost haste burst at 12.0.7** | absent from `all-talents.tsv` for **every spec of every class** (the whole file was grepped, not just Frost — zero hits), absent from Frost's `ability-inventory.tsv` under any origin, and no Icy Veins node exists on the Mage tree. Frost's cooldown-band castables are Frozen Orb, Cold Snap, Ray of Frost, Comet Storm, Alter Time and Mirror Image; **none of them is a haste cooldown**, which is a real change to how the spec ramps. ⚠ `rotation.md` and `builds.md` still describe pressing it — see the correction below. |
| Shifting Power | **not acquirable by any Mage spec** | absent from `all-talents.tsv` for every spec. Its only DB2 attachment is a SkillLineAbility row on the dead Shadowlands *Night Fae* covenant line, which is not a live acquisition path. The M+ cooldown-cycling tool is not in the Midnight kit. |
| Ice Floes | **not acquirable at 12.0.7** | appears on no class, spec or hero tree for any spec in `all-talents.tsv`, and on no acquisition row in Frost's inventory. |
| Mass Barrier `414660` | **shows in Frost's inventory as `cdm-only` — still not castable** | attaches to no trait node, SkillLineAbility, SpecializationSpells or PvpTalent entry (`reconcile-ledger.md`). Its `cdm-only` / `CooldownSetSpell` row is a **Cooldown-Manager set entry, not an acquisition row.** |
| Blazing Barrier `235313` | **belongs to Fire — also a `cdm-only` false friend here** | Frost's inventory carries a `Blazing Barrier` row at origin `cdm-only`. Same trap: CooldownSet leakage. `all-talents.tsv` gates the class barrier node one spell per spec — node `62117`→**Ice Barrier** `11426` for Frost, `62119`→Blazing Barrier for Fire, `62121`→Prismatic Barrier for Arcane. |
| Prismatic Barrier `235450` | **belongs to Arcane, not on this tree** | same node, same table. Frost has **one** barrier and it is **Ice Barrier**. |

*[Tier 1: `all-talents.tsv` across all 40 specs + per-spec `ability-inventory.tsv`,
DB2 @ 12.0.7.67808; `_abilities/reconcile-ledger.md`.]*

## Corrections this file has already made

Kept only because re-asserting them is the likely failure mode:

- **The spell's real name is `Glacial Spike!`, with the trailing exclamation
  mark.** `ability-inventory.tsv` carries it as `Glacial Spike!` `1222865`
  (`cdm-only` / `CooldownSetSpell`, `castable=true`); a plain **"Glacial Spike"
  matches no spell-name row at all** — it occurs only inside *other* spells'
  tooltip text (*Icicles* `1246832`, *Flash Freeze*, *Glacial Chill*,
  *Glacial Shatter*, *Duality*, *Rimecaster*). This matters for **macros,
  WeakAuras and any name lookup**: drop the `!` and the lookup fails silently.
  Its only DB2 attachment being a CooldownSet entry does *not* make it
  uncastable — Icicles upgrades your next Frostbolt into it.
- **`Thermal Void` `1247729` does not extend anything, and never gets held
  against.** Its 12.0.7 tooltip is: *"Consuming Brain Freeze has a 100% chance to
  cause your next Ice Lance to Shatter 4 additional stacks of Freezing."* An
  earlier revision of this file said *"what it extends is unknown … cannot be read
  at a pinned build"* and carried the file's only `@verify-ingame` on it. That was
  never an in-game question — the generated inventory row answers it. The old
  *"hold Flurry while the Thermal Void buff is up"* guidance rests on the
  pre-Midnight Icy Veins version of the talent and is **not** supported by this
  tooltip.
- **A `SpellName.csv` hit is not evidence a spec can cast something.** A previous
  revision justified rows that way; `SpellName` keeps retired spells indefinitely.
  Only an acquisition table (trait node, SkillLineAbility, SpecializationSpells,
  PvpTalent) settles it — which is what `ability-inventory.tsv` is built from.

## Open in-game questions

**None.** A question belongs here only if it genuinely cannot be answered from
game data — you must be logged in and looking at it. *"The exact cooldown /
charges is uncertain"* is **not** one: `ability-inventory.md` carries the Tier-1
number.

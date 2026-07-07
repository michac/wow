---
title: Session Planner — Roadmap & Open Decisions
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources:
  - knowledge/planning/scoring-model.md
  - knowledge/planning/README.md
confidence: high     # methodology/roadmap doc, not a fetched game fact
---

# Planner roadmap & what's on the table

> **Fresh session? Read this after `README.md`.** It captures the work parked
> mid-thread on 2026-07-06 so nothing is lost across a context clear. The
> plumbing (state capture, gating, equipment, quest IDs) is **done and verified
> live**; what remains is **scoring quality** (does the ranking give *good*
> advice) plus a few coverage gaps. The scoring items are **user-knob decisions**
> — propose, don't silently pick (scoring-model.md is the contract).

## Shipped 2026-07-06 (context for the below)

- **Addon → v0.4.1** (`michac/wow-planner-state`): per-slot equipment ilvls
  (schema 4, cached in-world so the logout write is good — fixed `equippedIlvl=0`);
  `ns.GENERATED_QUESTS` merge; weekly-quest objective progress `have/need`
  (schema 5, e.g. prey 1/3).
- **Tool** (`wowkb`): `gen_addon_quests` (auto-wire quest IDs from the scraper
  catalog); `plan.py --include-repeatables`; weakest-slot context line;
  per-column vault thresholds read from the dump; `vault_track` gate; `delve-tier11`
  re-modelled onto it; `quest_progress_note`.

Verified against the live `Encomplete` dump: gates subtract done work, world-boss
+ Void Assault resolve, "Open the Vault" correctly hides when empty, weakest slots
print `back 250, trinket2 259, waist 259`.

## On the table — scoring quality (NOT started; needs user sign-off on the knobs)

Full detail + proposed numbers were drafted in the plan file
`~/.claude/plans/enumerated-forging-bee.md` (machine-local, won't travel — this
section is the durable copy). Order matters: A → B → C (each scores through A).

### A. Rebalance the formula  · `scoring-model.md`, `plan.py:score()`
**Problem (live):** `(R×U×E)/T` lets trivial-time chores beat real power — on the
90-min plan **Trading Post (5.0) and Housing (4.0) outrank the M+ key (3.0)** that
feeds gear+vault.
**Proposal:** real-reward items `score = (R×U×E)/sqrt(T)`; floored-R collectibles
`/max(T,1)` (a quick cosmetic can't ride tiny T). → M+ 3.0 **→ 4.24**, Trading
Post 5.0 **→ 2.74**. Power moves forward.
**Decision:** approve sqrt(T)+floor-cap, or prefer value-first (rank by R×U×E,
time only gates what fits).

### B. Slot-targeting v2b  · `plan.py`, `candidates.json`, `scoring-model.md`
**Problem:** the planner *prints* the weak slot (`back 250`, 20 ilvl below avg) but
nothing *acts* on it.
**Proposal:** `slot_boost(cand, state)` mirroring `breakpoint_R()`: if a candidate
is tagged `fills_slot` AND gap `= avg − weakest ≥ 15`, override `R → 4`. Tag only
the aim-able candidates — `liadrin-spark` (craft the exact slot), `voidcores`
(catalyst/bonus-roll). Random-drop gear (delves/M+) stays untagged. Precedence:
`max()` of breakpoint and slot overrides. Add `check_slot.py`.
**Decision:** gap threshold (≥15), boost magnitude (R→4).

### C. De-noise repeatables  · `repeatables.py`, `plan.py`/`gen_addon_quests.py`
**Problem:** `--include-repeatables` floods — every scraped quest has placeholder
`T=1 / E=chore`, and overlaps curated items (Ritual Site Studies vs Ritual sites,
Showdowns vs Weekly world boss).
**Proposal:** per-type `T`/`E` map in `repeatables.py` (regenerate, don't hand-edit
the JSON); extend `CURATED_QUEST_IDS` into an activity-overlap map so dupes collapse
and only net-new surfaces by default.
**Decision:** the per-type `E` values are the personal preference table.

## On the table — coverage (the five weekly slugs)

Each activity has a *different* authoritative signal; match the gate type to it
rather than forcing `weekly_quest`.

| Slug / activity | Status | Signal / next step |
|---|---|---|
| `delve_tier_objective` | ✅ fixed | `vault_track` on the world column (done) |
| `prey_weekly` (94446) | ✅ wired + 1/3 progress | quest objective |
| `delve_weekly_cache` (6 bountiful) | ⏳ pending | **In-game check:** does the weekly cap sit on the *Restored Coffer Key* item or on *Coffer Key Shards*? Dump shows shards `weeklyMax=0`, so the ceiling is elsewhere. Then gate on key economy. |
| `dungeon_weekly` (Halduron 1500-rep) | ⏳ needs ID | read the live quest log when it's picked up |
| `liadrin_spark` | ⏳ needs ID | ditto (candidates: 93744 / 95245 / pillar quests) |
| `housing_weekly` (Vaeli) | 🔸 likely-gap | quest-of-week rotates IDs; low value (R=1) |

## Separate track (goal 4, untouched)

Parse-critique: extend `wowkb.wcl` with a character-parse fetch + diff vs the KB
rotation / simc APL. Note: `characters/encomplete-plan.md` is written for
Affliction; the main now plays **Demonology** — reconcile before critiquing.

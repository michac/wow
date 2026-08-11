---
title: Session Planner — Roadmap & Open Decisions
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/scoring-model.md
  - knowledge/planning/README.md
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Content Update Notes (Tier 1) — pre-season Delve rules
  - https://worldofwarcraft.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1) — Aug 18 unlocks
  - knowledge/_meta/patch-notes/12.1.md               # verbatim archive — pre-season dungeon pool (L1619), Bountiful/Coffer Keys (L1611,1615), Nightmare Prey (L1615)
  - knowledge/_meta/moving-values.md                  # Tier-1 floor — Mythic 0 pre-season lockout, S2 Great Vault World-row caps
  - knowledge/planning/activities/prey-weekly.md      # the S1→S2 Prey gate re-wiring this file tracks
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
**Problem (observed 2026-07-06, Season 1):** `(R×U×E)/T` lets trivial-time chores beat
real power — on the 90-min plan **Trading Post (5.0) and Housing (4.0) outranked the M+
key (3.0)** that feeds gear+vault. ⚠ **Not reproducible during the 2026-08-11 pre-season
week:** `activities/mplus.md` is `status: invalidated` until keystones return
**2026-08-18**, so the M+ key isn't rankable at all right now. The formula defect is
unchanged; only the worked example has to wait for Season 2 to be re-run.
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
Showdowns vs Weekly world boss). ⚠ **12.1 moved where the live overlap risk sits:**
`world-boss.md` is still `status: active` but is now *"Weekly world boss (legacy
Val/Naigtal open-world)"* — **superseded by Lairs**, with its drops frozen at Season 1
and no longer upgradeable. Build the overlap map against the new `lair-tidebound-grotto`
and `coiled-isle` rows too, not just the legacy pair.
**Proposal:** per-type `T`/`E` map in `repeatables.py` (regenerate, don't hand-edit
the JSON); extend `CURATED_QUEST_IDS` into an activity-overlap map so dupes collapse
and only net-new surfaces by default.
**Decision:** the per-type `E` values are the personal preference table.

## On the table — coverage (weekly slugs; NOT exhaustive as of 12.1)

Each activity has a *different* authoritative signal; match the gate type to it
rather than forcing `weekly_quest`.

> **Follow-up (2026-08-11): this table is no longer the whole gap list.** 12.1 added
> three activity files — `lair-tidebound-grotto`, `coiled-isle`, `zuljarra-renown` —
> each a new weekly-signal surface with no row here. Audit their gate types before
> treating the table as exhaustive again (the lair is a weekly *lockout*, not a weekly
> *quest*, so `weekly_quest` is the wrong shape for it).

| Slug / activity | Status | Signal / next step |
|---|---|---|
| `delve_tier_objective` | ✅ fixed (gate) | `vault_track` on the world column (done). ⚠ The *thresholds* it reads move in S2: the World row caps at **Champion 3/6** in the first Season 2 vault and **Hero 1/6** in every vault after (`../_meta/moving-values.md`) — the mechanism is fine, the numbers need a re-read |
| `prey_weekly` | ⛔ **REOPENED — gate needs re-wiring** | S1 quest **94446** ("A Nightmarish Task") is what this slug maps to; it is dormant during the pre-season and **nothing published says it survives Aug 18**. The Season 2 weekly is *"A Slithering Threat"* under a separate reserved slug **`prey_s2_weekly`, ID unknown**. **Read the S2 ID off the live quest log on/after 2026-08-18 and re-wire `gate.quest` before `activities/prey-weekly.md` flips back to `status: active`** — otherwise the ranker reads a dead quest as permanently "not done" |
| `delve_weekly_cache` (6 bountiful) | ⏳ pending | **In-game check:** does the weekly cap sit on the *Restored Coffer Key* item or on *Coffer Key Shards*? Dump shows shards `weeklyMax=0`, so the ceiling is elsewhere. Then gate on key economy. |
| `dungeon_weekly` (Halduron choice-rep) | ⏳ needs ID · pickable now | read the live quest log — the quest is available **this** week (any-difficulty dungeon), so no need to wait for Aug 18. ⚠ Rep amount: KB record is **1500**, disputed by two Tier-3 12.1 guides claiming 1000 — unverified, see `activities/renown-dungeon-weekly.md` |
| `liadrin_spark` | ⏳ needs ID | ditto (candidates: 93744 / 95245 / pillar quests) |
| `housing_weekly` (Vaeli) | 🔸 likely-gap | quest-of-week rotates IDs; low value (R=1) |

> **12.1 note (2026-08-11).** 12.1 "Curse of Ula'tek" shipped into a **pre-season
> week**; Midnight Season 2 does not open until **2026-08-18**. Three rows above move:
>
> - **`delve_weekly_cache` — blocked until Aug 18.** **Bountiful Delves do not appear
>   during the pre-season**, and **Coffer Keys begin dropping with maintenance the week
>   of Aug 18**, so the key-economy in-game check can't be run until then
>   (`activities/delve-bountiful.md` is `status: invalidated` for the same reason).
> - **`dungeon_weekly` — read the ID *this* week; it is NOT blocked.** The Season 2
>   dungeon pool went live **with the patch**, on Heroic and Mythic 0 — only Mythic+
>   keystones wait for Aug 18 — and Halduron's quest completes on a Midnight dungeon at
>   **any difficulty**, so it's pickable now and its quest ID is readable off the live
>   log today (`activities/renown-dungeon-weekly.md` is `status: active`). Mythic 0 sits
>   on a **one-week-only weekly lockout dropping Champion 1/6 (ilvl 292)** this week, so
>   this is the cheapest week to capture it.
> - **`prey_weekly` — coverage gap reopened, not just unavailable.** Nightmare Prey doesn't
>   return until the week of **Aug 18**, so `activities/prey-weekly.md` is
>   `status: invalidated` Aug 11–17 — but the *wiring* is the real problem: the slug still
>   points at the Season 1 quest, and the Season 2 weekly has a different name and an
>   unknown ID. Treat this as an open slug again, not a closed one.
>
> The scoring work above is otherwise 12.1-agnostic — except that **A**'s worked example
> can't be re-run until M+ is rankable again.

## Separate track (goal 4, untouched)

Parse-critique: extend `wowkb.wcl` with a character-parse fetch + diff vs the KB
rotation / simc APL. Note: `characters/encomplete-plan.md` is written for
Affliction; the main now plays **Demonology** — reconcile before critiquing.

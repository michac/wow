---
title: Session Planner — Needs-First Redesign (design doc)
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - knowledge/planning/scoring-model.md
  - knowledge/planning/roadmap.md
  - tools/wowkb/plan.py
  - knowledge/systems/void-incursions.md
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://www.icy-veins.com/wow/news/showdown-reward-changes-higher-level-gear-faster-rare-spawns-and-more/
confidence: high     # design/methodology doc, not a fetched game fact
---

# Needs-first redesign

> **Status: proposal, not yet built.** This supersedes the parked "scoring
> quality A/B/C" items in [`roadmap.md`](roadmap.md) with a single architectural
> pivot they were each groping toward. Read `roadmap.md` and
> `scoring-model.md` first — this doc assumes them.

## TL;DR

The planner today is **activity-first**: it walks the ~30 activities and asks
"is this one worth doing?" in isolation. That produces three failure modes we've
now confirmed both in the code and against a live character (`Encomplete`):

1. **One weak slot inflates many activities.** `score()` computes
   `weakest = min(slots)` once, then compares it to a scalar `reward_ilvl_max`
   that **7 activities all set to `279`** (`candidates.json`). A single 259 slot
   lifts all seven Hero-ceiling activities to R≈4.33 at once — even though the
   character only needs *one* piece, and even though most of those activities
   can't fill *that* slot.
2. **Gear "ceiling" ≠ "upgrade."** `reward_ilvl_max` is the top ilvl an item
   *could* reach, treated as guaranteed and as an upgrade. But a Hero drop at
   259 does **not** improve a slot already at 259 — and every one of Encomplete's
   slots is already Hero-track-or-crafted. His upgrades come from **crests**
   (upgrade existing Hero 259→276) and **Myth crests** (recraft the crafted
   waist), *not* from new drops. The model can't see this because it has no
   currency inventory and no per-slot upgrade path.
3. **No sense of "enough."** Nothing decrements after a need is met, no
   deterministic-vs-RNG distinction, no cross-character economy.

The fix is to **invert the pipeline**: scan the character(s) → derive *what they
actually need* → work backward to the cheapest/surest activities that satisfy
those needs → stop pulling an activity once its need is met.

## Why the current model can't get there (code-grounded)

| Gap | Where | Consequence |
|---|---|---|
| Gear value = `min(slots)` vs scalar ceiling | `plan.py:slot_target_R()` (354-378) | one weak slot inflates every Hero-ceiling activity; no per-slot targeting |
| No currency inventory in state | `plan.py` state = equipment ilvls only (no `state.currencies`) | can't reason "you have 176 Hero / 20 Myth crests, Myth is the bottleneck" |
| No deterministic-vs-RNG field | candidate schema (`gen_candidates.py:build_candidate` 111-124) | a guaranteed 100-accolade cache scores identically to a 1/12 boss drop |
| No currency-quantity yield | candidate schema | "yields 20 Hero + 5 Myth crests" can't be expressed; all gearing collapses to `reward_base=3` |
| Single-character only | `load_state()` (156-181) reads one dump; `scope`/roster unimplemented | no "Encomplete farms Accolades → gears the alts"; no leveler synergy |
| No dedup / diminishing returns | greedy walk in `plan()` (431-451) | filling one need doesn't lower any other activity's score |

Roadmap items **A (formula rebalance)**, **B (slot-targeting v2b)**, and
**C (de-noise repeatables)** are each a local patch on one of these. Needs-first
subsumes B entirely and reframes A and C as tuning that happens *inside* the new
scoring loop.

## The pivot: needs-first pipeline

```
scan state ─▶ derive needs ─▶ rank needs ─▶ map needs→activities ─▶ greedy select w/ dedup
(equip +      (structured    (bottleneck   (each activity yields    (decrement needs as
 currencies +  need objects)  first)        toward >=1 need)          they're satisfied)
 roster)
```

### 1. Scan state (per character)

Extend planner state beyond equipment ilvls to include:

```
state.equipment[slot] = { ilvl, track, upgrade_level, is_crafted, ceiling }
state.currencies       = { hero_crest, myth_crest, field_accolade,
                           nebulous_voidcore, ascendant_voidshard, ... }
state.roster           = [ {name, level, role: main|gearing|leveling, focus} ]
state.unlocks          = { renown[faction], omnium_rows, professions, ... }
```

**Currency source.** The Syndicator snapshot in `knowledge/characters/*.md`
already carries these (Encomplete: Hero 176, Myth 20, Field Accolade 1,309,
Nebulous Voidcore 11, Coffer Shards 58). Either pipe that snapshot into planner
state, or extend the PlannerState addon to dump currencies (the addon already
dumps some). **Known gaps** (neither Syndicator nor the addon sees them): Sparks
of Radiance, Catalyst charges, Ascendant Voidshards → keep these on the manual
(`todo.md`) tier until captured.

### 2. Derive needs (the new core object)

A **need** is a structured, character-scoped want with a value weight. Types:

- `slot_upgrade{char, slot, from_ilvl, to_ilvl, via: crest|drop|vendor|craft, cost}`
- `currency_accumulate{char, currency, have, target, purpose}` — e.g. *Myth crests
  to recraft the waist 259→285*; this is where bottleneck logic lives.
- `power_unlock{char, system}` — Omnium Folio rows, embellishments, Nilhammer chain.
- `alt_gearing{char, via_source}` — Champion/Heroic **warbound** caches, drops.
- `maintenance{char, kind}` — vault fill, weekly-capped chunks, weekly profession KP.
- `collectible{item, source, effort, novelty}` — mounts/pets/toys (the "fun" axis).

Deriving them is deterministic from state: any slot below its track ceiling with
a known upgrade path → a `slot_upgrade`; any bottleneck currency short of a named
target → a `currency_accumulate`; any roster member below cap or under-geared →
`alt_gearing`/leveling needs.

### 3. Rank needs (bottleneck-first)

Weight each need. The **binding constraint** dominates: for Encomplete that's
**Myth crests** (only 20, gate the waist recraft and staff overcap), not the
already-Hero-geared slots. For an alt it's **raw Champion/Heroic gear**. A
`collectible` gets a novelty × time-scarcity weight so a "cool mount in 30 min"
can surface without out-ranking real power (the `--mood` dial scales this).

### 4. Map needs → activities

Each activity advertises **what it yields** (see schema below). An activity's
session value becomes:

```
value(c) = Σ_over_needs_n  marginal(c, n) · w(n) · p(c, n)
score(c) = value(c) / time(c)
```

- `marginal(c, n)` = how much of need *n* **one run** of *c* closes, **capped by
  the remaining need and the remaining weekly cap**. (This is what makes Ritual
  Sites T6 — 5 Myth + 10 Hero crests/run — beat a world-boss drop for Encomplete.)
- `w(n)` = need priority from step 3.
- `p(c, n)` = probability / expected-value factor: **1.0 for a deterministic
  exchange**, `chance × affordable_attempts` for an RNG drop. This is the
  deterministic-vs-RNG fix.

### 5. Greedy select with dedup

Pack activities into the time budget as today, **but re-derive/decrement the
need-set after each pick**. Once one activity fills the "ring2 slot" need, that
need stops pulling every other Hero-ceiling activity — killing failure mode #1.

## Data-model changes

### Activity front-matter (and mirrored candidate fields)

```yaml
yields:
  currencies: { hero_crest: 20, myth_crest: 5, field_accolade: 100 }   # per run
  slots:                                                                # gear rewards
    - { track: hero, ilvl: 259, chance: 0.5, slots: [ring, trinket] }   # RNG drop
  vault: { track: world, count: 1 }
deterministic: true            # or per-yield `chance`
weekly_cap: { runs: 6 }        # e.g. bountiful coffers; caps marginal()
scope: character               # character | account
warbound: true                 # yield usable cross-character (drives alt_gearing)
```

`gen_candidates.py:build_candidate()` emits these into `candidates.json` (today
it drops `scope`, `goal`, `venue` entirely — start by carrying them through).

### `slot_target_R()` rewrite

Replace `weakest = min(slots)` + scalar ceiling with per-slot logic: an activity
only advances a `slot_upgrade` need if it can fill **that** slot **and** its
yield ilvl/track exceeds the slot's *current* ilvl (not just any weak slot).
Roadmap item **B** is the first increment of this.

## Cross-character model (the biggest payoff)

Wire the `scope`/roster machinery that `active-characters.md` already documents
but no code reads:

- Read the roster (main / gearing / leveling + `focus`) from `active-characters.md`.
- `scope: account` activities scored once; `scope: character` scored **per active
  roster member, competing in one global ranking**.
- **Model warbound flows.** A purchase/drop on char A that yields *warbound* gear
  counts toward char B's `alt_gearing` need. Worked case (verified 2026-07-07):
  Encomplete holds **1,309 Field Accolades**; his own slots are already Hero, so
  a BoP Hero cache doesn't upgrade him — but **Warbound Champion caches (100 ea)
  and now Warbound Heroic caches (750 ea, flipped BoP→Warbound in the June 26/30
  hotfixes)** turn that stockpile into ~13 Champion or ~1 Heroic alt piece(s).
  The planner should surface "spend Accolades → warbound caches → Uncomplete/
  Hallick" as a **top-of-roster** play.
- **Leveler synergy.** XP-bearing activities (Turbulent Timeways, Void Assault's
  12.0.7-doubled XP) are valued **only for roster members below cap** — worthless
  on the 90 main, high for the leveler.

## Fun / collectibles

Model `collectible` needs explicitly: `value = novelty · scarcity / effort`, so a
limited-time mount or a "shoots rainbows" toy competes on its own axis instead of
riding the crude U-floor. `--mood fun` raises the collectible weight; `efficiency`
lowers it. This is the concrete version of README goal #2 ("don't let efficiency
crowd out rare/limited events").

## Staged implementation plan

Order is chosen so each stage ships value and de-risks the next.

- **Phase 0 — data corrections (cheap, no architecture).** Fix the `279`→`276`
  placeholder across the 7 activity files; drop the Singularity renown gate when
  the character is already past the unlock rank; stop valuing Void Assault XP at
  cap; promote Ritual Sites T6 (Myth-crest source) out of the backlog; handle the
  `raid_weekly` / `campaign_incomplete` gates that currently fall through to
  `unknown`. Also correct `void-incursions.md` (Heroic caches are now Warbound).
- **Phase 1 — currency inventory into state.** Pipe Syndicator currencies into
  planner state; add `currency_accumulate` needs. First real needs-first scoring:
  crests over drops for an already-geared main.
- **Phase 2 — per-slot reward vectors + `slot_target_R` rewrite + dedup**
  (subsumes roadmap **B**). Kills the one-weak-slot inflation.
- **Phase 3 — deterministic-vs-RNG EV.** Sure exchanges beat lotteries.
- **Phase 4 — cross-character roster + warbound flows + `scope`.** The big payoff.
- **Phase 5 — collectible/fun needs; `todo.md` auto-population; (long-term) the
  PlannerState in-game checklist UI** so manual-tier items are ticked in-game.

Roadmap **A** (formula rebalance, `sqrt(T)`) and **C** (de-noise repeatables)
fold in as tuning of the Phase 1–2 scoring loop.

## Open questions / to verify in-game or via patch notes

- **Warbound Heroic cache** — confirmed via the June 26/30 2026 hotfixes
  (Icy Veins / Wowhead); `void-incursions.md` is stale and needs updating. Confirm
  the exact price stayed 750.
- **Weekly caps** — the bountiful-delve crest counts and the Restored-Coffer-Key
  vs Coffer-Shard cap location are still unresolved (`roadmap.md` coverage table).
- **Val/Naigtal "4× world boss → Myth track"** and "Val gives Myth crests" — the
  user recalls these; **not in the KB**. Verify before modeling.
- **Omnium Folio** — is row progression warband-wide or per-character? Affects
  whether it's an account or character need.
- **Currency capture gaps** — Sparks, Catalyst charges, Ascendant Voidshards are
  invisible to Syndicator; decide addon-dump vs manual tier.

## Worked example — Encomplete (why the output changes)

*Old ranking* (activity-first): world boss 19.1, Voidcores 17.3, delves 12.1,
dungeon-weekly-renown 12.0 — all inflated by his three 259 slots via the `279`
ceiling.

*Needs-first ranking:* his binding need is **Myth crests** (20; gate the crafted
waist + staff), then **Hero crests** (176 ≈ 1.2 upgrades toward 276), then
**dump 1,309 Accolades into warbound caches for the alts**. So **Ritual Sites T6**
(Myth + Hero crests + Accolades, repeatable) rises to the top; **dungeon-weekly
renown drops off** (already renown 8, past the trinket); **world-boss/delve random
drops fall** (a 259 Hero piece doesn't beat his 259s); **Voidcores** are re-valued
as "spend at end of M+10+ → Myth," not a standalone errand. Same character, same
night — a materially better plan, because the model started from what he *needs*.

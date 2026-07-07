---
title: Activity Facets — the tag vocabulary & priority-inheritance contract
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources:
  - knowledge/planning/scoring-model.md
confidence: high     # methodology/contract doc, not a fetched game fact
---

# Activity facets — how an activity is described, and how tags become priority

> **Read this before adding activities.** Every activity file in
> `activities/` is just a set of **facet tags** plus prose. There is **no
> single taxonomy tree** — a dungeon serves *gearing* and *rating* and
> *collectibles*, so one tree would lose the others. Facets are orthogonal
> axes; priority is inferred from the **intersection** of an activity's tags,
> not from where it sits in a folder.
>
> This doc is the contract. The planner (`plan.py`) and the generated TOC read
> these tags; tune the priors here, not in code.

## Design stance

- **Include by default.** An activity is surfaced unless `status: invalidated`.
  `confidence` is a *property you can see*, never a filter — a `low`-confidence
  entry still ranks (tier-1 WoW sources are sparse; we don't hide things waiting
  for confirmation).
- **Tags, not a hierarchy.** Files live flat in `activities/`. The browsable
  "outline" (`README.md`) is a *generated projection* over tags — you can view
  by goal, by venue, or by cadence without re-filing anything.
- **Location is metadata.** Because event-ness / solo-ness / time-boxing are
  facets (not buried in a goal-bucket), each one can feed the score directly.

## The six facets

| Facet | Card. | Values | Drives |
|---|---|---|---|
| **goal** | multi | `gearing` · `leveling` · `professions` · `collectibles` · `story` · `rating` | R tendency; the "what am I working on" view |
| **venue** | 1–2 | `world` · `dungeon` · `raid` · `pvp` · `delve` · `quest` · `profession` · `housing` · `meta` | E (with group); the gather axis (a "dungeon video" → `venue:dungeon`) |
| **group** | 1 | `solo` · `group` · `flex` | E; group-gating risk |
| **cadence** | 1 | `one-time` · `daily` · `weekly` · `monthly` · `repeatable` · `event` | reset frequency (`repeatable` = farmable, no reset) |
| **time** | 1 | `standing` · `time-boxed` | **U** — time-boxed = FOMO |
| **scope** | 1 | `account` · `character` | counted once vs per-active-char |

Notes on values:
- `goal:rating` — pushing keys/score for its own sake (3k / 3.4k IO, PvP rating).
  No loot payoff, so it is *not* `gearing`; it exists precisely so completionist
  pushes score above their gear value.
- **No `reputation` goal — renown is instrumental, not terminal.** You don't grind
  renown for its own sake; you grind it for the mount (`collectibles`), recipe
  (`professions`), gear (`gearing`), or story beat (`story`) on the vendor behind
  it. So a renown activity is tagged by *what its next unlock is*, and its R rides
  the "renown level that unlocks a specific reward" breakpoint (`scoring-model.md`).
  Same treatment as crests/gold — intermediate currencies are never goals. (That
  terminal-vs-instrumental test is also why `rating` *is* a goal: the score is the want.)
- `venue:meta` — non-content tasks with no place to *go*: opening the Great Vault,
  Trading Post buy-in, currency spends.
- Vocab **grows from the YouTube starter data** — add values as real activities
  demand them, then record the addition here.
- **Aggregators are one reward, not many activities.** The Great Vault is a single
  weekly pick; the things that fill its columns (M+, delves, raid, PvP) stay as their
  own activities and express the slot-fill as a `breakpoint`, never a per-column entry.
  Don't mint an activity per slot/track.

## How tags become priors (R, U, E)

A per-activity file **overrides** any prior it disagrees with (set `reward`,
`urgency`, or `enjoyment` explicitly). Otherwise it **inherits** from its tags:

### R — from `goal` + `reward.type`
- `goal:gearing` / `rating` → high R tendency (real power / score toward a breakpoint).
- `goal:collectibles` → R = 0, floored to **1 only when U ≥ 1.5** (the scoring-model
  fun-floor). Cosmetics never outrank power at equal urgency.
- `goal:story` / `leveling` → one-time power/XP; R set per activity.
- Breakpoint proximity (`breakpoint:` block) still overrides R live — unchanged
  from `scoring-model.md`.

### `yields.currencies` — declared currency drops (needs-first Phase 1)

An activity that hands out crests/accolades declares them so the planner can value
the currency by whether the character still has a **consumer** for it (a geared main
farms crests, not drops; a crest source falls to ~0 once every slot is track-capped).
Only the `currencies` sub-key ships this phase (the redesign doc's `slots`/`vault`/
`weekly_cap`/`warbound` sub-blocks are later phases).

```yaml
yields:
  currencies: { hero_crest: 10, myth_crest: 5, field_accolade: 100 }   # per run
```

- **Canonical keys** (not scraped names): `hero_crest`, `myth_crest`,
  `champion_crest`, `veteran_crest`, `field_accolade`, `spark`,
  `radiant_spark_dust`, `voidcore`, `coffer_key_shard`. The consumer test +
  goal-tag map live in `tools/wowkb/rewards.py` (`CURRENCY_CONSUMERS`,
  `CANONICAL_CURRENCY_NAME`); add a key there when you add one here.
- **Amounts** are carried into `candidates.json` but **unused in Phase 1** (the
  consumer R is headroom/gate-based, not quantity-scaled) — they're for the
  marginal-value math in later phases. Source them from the file's prose +
  `endgame/dawncrests.md`; don't fabricate.
- **Gear, not currency:** an activity whose reward is a gear *drop* (world boss,
  voidcore bonus-roll) declares no `yields.currencies` — its value comes from
  `yields.slots` via `slot_target_R` (below). Only a genuine crest/accolade
  currency goes here. An activity may declare **both** (Bountiful delves yield
  crests *and* a gear cache).
- `plan.py:currency_R()` feeds this into the R override as
  `max(breakpoint, slot-target, currency)`; a source with no pending consumer
  contributes `0`, a source with no `yields.currencies` keeps `reward_base`.

### `yields.slots` — declared gear drops (needs-first Phase 2a)

An activity whose reward is a gear *drop* declares the drop's **landing ilvl** and
which equipped slots it can fill, so the planner values it against **this** char's
per-slot ilvls: a drop is only an upgrade if its landing ilvl beats a slot it can
actually fill. This replaced the old scalar `reward_ilvl_max` on migrated
activities (`plan.py:slot_target_R` still falls back to `reward_ilvl_max` for
un-migrated ones — e.g. `sporefall-raid`'s per-difficulty ceiling).

```yaml
yields:
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # LANDING ilvl, not the ceiling
```

- **`ilvl` is the LANDING ilvl, not the crested ceiling.** A Hero drop *lands* at
  **259** (1/6, `endgame/dawncrests.md`) — it climbs to 276 only via crests, which
  is the *currency* path, not the drop. A faction champion piece lands at **246**.
  This is the semantic correction at the heart of 2a: a fresh 259 drop is a
  **sidegrade** to a 259 slot, so it scores 0 for a geared main. Never put the 276
  ceiling here.
- **`slots`** = which equipped slots the drop can fill. `[all]` for a random
  open-world drop (any slot); an explicit list for a targeted source (faction
  champion gear; later catalyst/craft). **Canonical slot names** match the dump's
  lowercase form: `head neck shoulder chest waist legs feet wrist hands back
  finger1 finger2 trinket1 trinket2 mainhand offhand` (matched case-insensitively).
- **`chance`** is **carried but NOT applied in Phase 2a** — the deterministic-vs-RNG
  expected-value math is Phase 3. Keeping the field now means Phase 3 plugs in with
  no data migration. Set a coarse per-run estimate; it does not affect 2a scoring.
- **`track`** is descriptive (which upgrade track the drop rides); 2a values off
  `ilvl`/`slots` only.
- `plan.py:slot_target_R()` reads it via `rewards.best_slot_delta` — the best
  positive `landing_ilvl − current_slot_ilvl` across every fillable slot, `R =
  min(5, 1 + Δ/6)`; no positive delta anywhere → `0`. No `yields.slots` and no
  `reward_ilvl_max`, or a pre-schema-4 dump → no override, keep `reward_base`.

### U — from `time` + `cadence`
| Condition | U |
|---|---|
| `time:time-boxed` + annual/one-time | 3 |
| `time:time-boxed` recurring (Timewalking, Darkmoon) | 1.5 |
| `cadence:weekly`/`monthly`, `time:standing` (expires this reset) | 2 |
| `cadence:daily`/`standing`, always available | 1 |
| actively better to wait | 0.5 |

### E — from `(venue, group)`, with per-activity override
Default table (reuses the `scoring-model.md` E values, keyed by combo). Set
`enjoyment: <n>` on an activity to override when it's special:

| venue + group | E | note |
|---|---|---|
| `delve` + `solo` | 1.4 | core loop |
| `world` + `solo` | 1.1 | baseline solo world (ritual sites override → 1.2) |
| `dungeon` + `group` | 1.0 | M+ neutral |
| `profession` + `solo` | 0.9 | means-to-an-end |
| `housing` + `solo` | 1.0 | flavor |
| `meta` + any | 1.0 | UI/vendor, low time keeps it viable |
| `raid` + `group` | 0.7 | group-gated |
| `pvp` + any | 0.4 | deprioritized |

E stays capped at 1.5 (bends, never inverts, the ranking) — still the single
personal knob.

## Cross-character scoring (v2)

`scope:account` activities are counted **once** across the active roster
(`../active-characters.md`); `scope:character` activities are scored **per active
character** and compete globally. That is what lets "1 hour, Timeways is up →
level Uncomplete" outrank a grindy weekly on an already-geared Encomplete.

## Activity file template

```yaml
---
id: <slug>
name: <human name>
goal: [<...>]
venue: <...>
group: <solo|group|flex>
cadence: <one-time|daily|weekly|monthly|event>
time: <standing|time-boxed>
scope: <account|character>
status: active            # active | invalidated
gate: { type: ..., ... }  # how the planner detects "already done this reset"
reward: { type: [...], detail: "..." }
time_blocks: <n>          # 15-min blocks
enjoyment: <n>            # OPTIONAL — override the (venue,group) default
breakpoint: { ... }       # OPTIONAL — live R override (see scoring-model.md)
patch: 12.0.7
fetched: 2026-07-06
sources: ["yt:<id>", "https://..."]
confidence: high|medium|low   # a property, not a filter
---
Prose: what it is, where, what it rewards *this patch*, any nuance.
```

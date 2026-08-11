---
title: Activity Facets — the tag vocabulary & priority-inheritance contract
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/scoring-model.md
  - knowledge/planning/active-characters.md   # the roster the cross-character example is read off
  - knowledge/planning/activities/lair-tidebound-grotto.md   # the scope:character activity that example uses
  - knowledge/endgame/dawncrests.md           # S1/S2 crest landing ilvls quoted in the yields sections
  - https://worldofwarcraft.blizzard.com/en-us/news/24295085   # 12.1 Lairs preview (Tier 1) — the new content shape the venue vocab was tested against
  - https://worldofwarcraft.com/en-us/news/24293281            # 12.1 "Curse of Ula'tek" Content Update Notes (Tier 1)
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
- ⚠ **A new `venue` value is a code change, not just a doc edit.** Every value must
  have a matching entry in `gen_candidates.VENUE_E_KEY` → `plan.E_TABLE`; an unmapped
  venue silently falls through to the `chore` E of 1.0. That cost is the reason we
  re-use an existing value unless a shape genuinely scores wrong (see Lairs below).
- Vocab **grows from the YouTube starter data** — add values as real activities
  demand them, then record the addition here.
- **Aggregators are one reward, not many activities.** The Great Vault is a single
  weekly pick; the things that fill its columns (M+, delves, raid, PvP) stay as their
  own activities and express the slot-fill as a `breakpoint`, never a per-column entry.
  Don't mint an activity per slot/track.

### ⚠ Open vocabulary question — **Lairs** (new in 12.1, unresolved)

12.1 shipped **Lairs** (`endgame/lairs.md`; first one:
`lair-tidebound-grotto.md`), an **instanced world boss** that does not cleanly fit
any existing `venue` value — it is a fixed outdoor entrance with a summoning stone
like a Delve, a scenario + boss you can **queue into solo** at World difficulty
while the instance fills around you (the boss scales 5–40), and from **2026-08-18**
also a **Normal / Heroic / Mythic** premade activity (Mythic is the **flexible 15–25**
difficulty; Normal and Heroic are not stated as 15–25) on a raid-style
reward track with a weekly lockout and BoP loot.

**No new tag has been minted.** `lair-tidebound-grotto` is filed
`venue:world` + `group:flex`, and that is a deliberate placement, not an oversight:
the row is rankable **today only at World difficulty**, which is a solo-queue world
experience and must not eat the `raid` E-penalty (0.7 vs `world` 1.1).

The gap is real and is recorded here rather than papered over:

- **The one activity file cannot carry both halves.** From Aug 18 the same lair is
  simultaneously a solo-queue world kill *and* a Normal/Heroic/Mythic premade (up to
  25 players at Mythic) — one `venue`/`group` pair, two E values. `group:flex` splits
  the difference and neither half is right.
- **Options, none chosen:** (a) keep `venue:world` and set an explicit
  `enjoyment:` override once Normal+ is the point; (b) mint **`venue:lair`** with its
  own E (between `world` 1.1 and `raid` 0.7) — which requires the `VENUE_E_KEY` /
  `E_TABLE` entries above; (c) split into two activity rows (World vs Normal+) with
  different venues and a shared lockout gate.
- **Decide after Aug 18, on evidence** — once we know whether the harder difficulties
  are what people actually run and whether a lair clear fills a Great Vault row (also
  unconfirmed). Until then: **do not invent `venue:lair` in an activity file**; the
  ranker would score it as a `chore`.

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
`currencies` shipped in Phase 1 and **`slots` shipped in Phase 2a** (documented in the
next section); the redesign doc's `vault` / `weekly_cap` / `warbound` sub-blocks are
still later phases.

```yaml
yields:
  currencies: { hero_crest: 10, myth_crest: 5, field_accolade: 100 }   # per run
```

- **Canonical keys** (not scraped names): `hero_crest`, `myth_crest`,
  `champion_crest`, `veteran_crest`, `field_accolade`, `spark`,
  `radiant_spark_dust`, `voidcore`, `coffer_key_shard`. The consumer test +
  goal-tag map live in `tools/wowkb/rewards.py` (`CURRENCY_CONSUMERS`,
  `CANONICAL_CURRENCY_NAME`); add a key there when you add one here.
  ⚠ **A canonical key is not automatically scored.** `veteran_crest`, `voidcore` and
  `coffer_key_shard` exist in `CANONICAL_CURRENCY_NAME` but have **no
  `CURRENCY_CONSUMERS` entry**, so declaring them contributes **0 R** today — the
  declaration is recorded, not valued. Write them anyway (they're true, and the later
  marginal-value phases will read them), but don't expect a ranking change until the
  consumer test exists.
- **The keys are tier-named on purpose and survive a season rename.** Season 2's
  crests are **Mistcrests** (S1's were Dawncrests — `endgame/dawncrests.md`), but
  `veteran_crest` / `champion_crest` / … are unchanged: an activity file never
  spells the season's brand name into a key. *(The human-readable strings in
  `rewards.CANONICAL_CURRENCY_NAME` — and the scrape-matching `CURRENCY_RULES` — were
  re-pointed to "… Mistcrest" in the 12.1 sweep, with the Dawncrest rules kept as
  Season-1 fallbacks. Those strings are display/matching only; the canonical keys did
  not move, so no activity file needed an edit.)*
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
    - { track: hero, ilvl: 305, chance: 1.0, slots: [all] }   # LANDING ilvl, not the ceiling
```

- **`ilvl` is the LANDING ilvl, not the crested ceiling.** In **Season 2** a Hero
  drop *lands* at **305** (1/6, `endgame/dawncrests.md`) — it climbs to **321** only
  via crests, which is the *currency* path, not the drop. A slot-specific
  Void-Touched Cache buy lands at **279** (Veteran 1/6). This is the semantic
  correction at the heart of 2a: a fresh 305 drop is a **sidegrade** to a 305 slot,
  so it scores 0 for a geared main. Never put the 321 ceiling here.
- ⚠ **These numbers move every season.** The whole ladder shifted upward from S1 to
  S2 (S1 Hero landed at **263**, ceiling 276; S2's lands at **305**, ceiling 321 —
  `endgame/dawncrests.md`), so **every migrated `yields.slots` ilvl in
  `activities/` is season-scoped and must be re-read against `endgame/dawncrests.md`
  at each season rollover** — a stale S1 landing ilvl makes a dead activity look like
  a live upgrade.
- **`slots`** = which equipped slots the drop can fill. `[all]` for a random
  open-world drop (any slot); an explicit list for a targeted source (faction
  champion gear; later catalyst/craft). **Canonical slot names** match the dump's
  lowercase form: `head neck shoulder chest waist legs feet wrist hands back
  finger1 finger2 trinket1 trinket2 mainhand offhand` (matched case-insensitively).
- **`chance`** — **drop probability only** (Phase 3 effect *a*): the chance the activity
  yields a piece at all, applied as a straight EV multiplier (`effective_delta = chance ×
  value`). Guaranteed drops — bonus rolls, vendor buys — are `1.0` (the default when
  omitted); a chance-to-drop world-boss piece is `< 1`.
- **`targeted`** *(optional, default `false`)* — **slot determinism** (Phase 3 effect *b*).
  `true` = YOU choose which slot the piece fills (a vendor pick like Maren, a catalyst), so
  it's valued at the best fillable slot even over `[all]`. `false`/omitted = the game picks
  the slot: an `[all]` (or multi-slot) roll is valued at the **expected** upgrade across its
  fillable slots (mean of positive per-slot deltas), NOT the max — so a guaranteed *random*
  roll no longer inflates to your single best slot. (`plan.py:best_slot_delta`; a targeted
  Champion-292 buy beats a random Hero-305 roll for closing one specific gap.)
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
| `time:time-boxed` recurring (e.g. Darkmoon Faire) | 1.5 |
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
| `quest` + any | 1.0 | routed to the same `chore` E as `meta` in `VENUE_E_KEY` |
| `raid` + `group` | 0.7 | group-gated |
| `pvp` + any | 0.4 | deprioritized |

E stays capped at 1.5 (bends, never inverts, the ranking) — still the single
personal knob.

## Cross-character scoring (v2)

`scope:account` activities are counted **once** across the active roster
(`../active-characters.md`); `scope:character` activities are scored **per active
character** and compete globally. That is what lets "1 hour → run the Tidebound
Grotto on Uncomplete" outrank a capped weekly on an already-geared Encomplete:
`lair-tidebound-grotto` is `scope:character` with a per-character weekly lockout,
so it scores once per active row and is still unclaimed on the gearing alt.
`../active-characters.md` ("Why the roster is a first-class input") works the same
example from the roster side.

⚠ **Pick a live activity when you copy this example.** An example naming a dead
event teaches the wrong shape — e.g. Turbulent Timeways, which ended 2026-08-11
(`../../endgame/world-events.md`), and Darkmoon Faire, which is `scope:account` and
so is exactly *not* what the per-character half illustrates.

## Activity file template

```yaml
---
id: <slug>
name: <human name>
goal: [<...>]
venue: <...>
group: <solo|group|flex>
cadence: <one-time|daily|weekly|monthly|repeatable|event>
time: <standing|time-boxed>
scope: <account|character>
status: active            # active | invalidated
gate: { type: ..., ... }  # how the planner detects "already done this reset"
reward: { type: [...], detail: "..." }
yields: { ... }           # OPTIONAL — declared currency/slot drops (see above)
time_blocks: <n>          # 15-min blocks
enjoyment: <n>            # OPTIONAL — override the (venue,group) default
breakpoint: { ... }       # OPTIONAL — live R override (see scoring-model.md)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources: ["yt:<id>", "https://..."]
confidence: high|medium|low   # a property, not a filter
---
Prose: what it is, where, what it rewards *this patch*, any nuance.
```

⚠ **An activity that is announced but not yet live is not rankable.** 12.1 went live
**2026-08-11** in a **pre-season** state; **Midnight Season 2 opens 2026-08-18**. A row
whose content unlocks on Aug 18 (Mythic+ keystones, the Venomous Abyss raid, Nightmare
Prey, Bountiful Delves, rated PvP, Normal+ Lairs) must say so as *upcoming, dated* prose
and must not carry live `yields` for content nobody can enter yet — bump it when the
week turns. `status: invalidated` is for content that is **gone** (e.g. Turbulent
Timeways, ended 2026-08-11), not for content that has not arrived.

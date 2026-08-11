---
title: Session Planner — Needs-First Redesign (design doc)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/scoring-model.md
  - knowledge/planning/roadmap.md
  - tools/wowkb/plan.py
  - tools/wowkb/rewards.py
  - knowledge/systems/void-incursions.md
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://www.icy-veins.com/wow/news/showdown-reward-changes-higher-level-gear-faster-rare-spawns-and-more/
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Content Update Notes (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - knowledge/_meta/moving-values.md                  # Tier-1 floor: rows 62-64, 73-75, 77, 92, 94
  - knowledge/_meta/patch-notes/12.1.md               # verbatim archive: VOID-TOUCHED CACHES / VAL AND NAIGTAL / RITUAL SITES / Season 2 pre-season
confidence: high     # design/methodology doc, not a fetched game fact
---

# Needs-first redesign

> **Status: building — Phases 0–1 + 2a shipped (2026-07-07).** Phase 0 (data
> corrections), **Phase 1 (currency inventory + pending-consumer valuation)**, and
> **Phase 2a (per-slot reward vectors + `slot_target_R` rewrite)** are live in
> `plan.py`/`rewards.py`; Phase 2b (dedup) / 2c (crafting-as-gear) and Phases 3–5
> remain. The modeling questions
> this design depended on are **resolved** (verified 2026-07-07 — see
> [Resolved questions](#resolved-questions-verified-2026-07-07)), so nothing
> factual is left to discover before building. This supersedes the parked
> "scoring quality A/B/C" items in [`roadmap.md`](roadmap.md) with a single
> architectural pivot they were each groping toward. Read `roadmap.md` and
> `scoring-model.md` first — this doc assumes them.

> ⚠ **12.1 re-base owed before Phase 2b (noted 2026-08-11; the architecture is
> unaffected, the constants are not).** Everything numeric below is **Season 1**:
> it was written against Encomplete's 2026-07-07 state and the S1 ladder. 12.1
> went live 2026-08-11 and **Season 2 opens 2026-08-18**, which moves three
> things this design hardcodes:
> - **Crests renamed and the whole ladder shifted +45.** S1 *Dawncrests* → S2
>   **Mistcrests**; S2 gear runs **269 → 334** (Adventurer 269–282 · Veteran
>   282–295 · Champion 295–308 · Hero **308–321** · Myth 321–334) against S1's
>   224 → 289. So every "Hero **276** ceiling", "259 slot" and "285 recraft" in
>   this doc — and `rewards.py:CREST_CEILING = {Champion 263, Hero 276, Myth 285}`
>   plus the `dawncrest` keys in `CURRENCY_RULES` / `CURRENCY_CONSUMERS` — is
>   **S1-era and wrong for a character gearing today**. The *shapes* (currency
>   scores by its pending consumer; a drop scores by `landing − current_slot`)
>   are unchanged; only the tables move. Re-base off
>   [`_meta/moving-values.md`](../_meta/moving-values.md), which is the Tier-1
>   floor here (currency IDs 3437–3441, `CurrencyTypes` DB2 @ 12.1.0.69214).
> - **The equipment-track gap Phase 1 works around is now worth closing properly.**
>   The ilvl→track approximation is exactly the thing a +45 shift breaks silently;
>   PlannerState schema ≥ 8 reads `track`/step off the item tooltip, so the
>   [resolved-Q5](#resolved-questions-verified-2026-07-07) "extend the addon" path
>   has partly shipped — wire the ranker to it rather than re-tuning the ceiling
>   constants.
> - **Two named activities are gone.** **Turbulent Timeways ended 2026-08-11**
>   (dropped from the leveler-synergy and expiring-windows examples below), and Ritual
>   Sites T6 — this doc's headline winner — **no longer offers a Voidcore bonus
>   roll** and now pays **S2** crests at S2 Delve-equivalent rates.
> - **Three reward *sources* below no longer exist** — structural, so the "it's all
>   Season 1 numbers" scoping above does **not** cover them:
>   - **Void-Touched Caches:** 12.1 **removed the Season 1 gear caches outright**.
>     The replacements are an **S2 Adventurer *Warbound* cache for 200 Field
>     Accolades** and **S2 Veteran *BoP* caches for 500 (random slot) / 750
>     (slot-specific)**. So the Cross-character-model play below — "Warbound
>     Champion caches (100) / Warbound Heroic caches (750)" — names two things that
>     are gone, and the *only* warbound cache today is the 200-Accolade Adventurer
>     one. ([`moving-values.md` row 75](../_meta/moving-values.md); `patch-notes/12.1.md`,
>     VOID-TOUCHED CACHES.) The accolade→alt **shape** survives; the tier and price
>     do not.
>   - **Nebulous Voidcores:** S1 Voidcores **convert to gold** at S1's end and can no
>     longer be spent on S1 content; from S2 they are a **Great Vault reward** (raid
>     re-roll cost **1**, was 2), and they are **absent from the first S2 vault** —
>     bonus rolls return the **week of Aug 25** and need ≥3 vault panes unlocked. So
>     "Nebulous Voidcore 11" in Scan-state, and Voidcores as a spendable resource in
>     Phase 1 / the worked example, describe a dead balance.
>   - **"Knocking Off the Top (Heroic)":** its Mythic quest reward now **stays a
>     Season 1 item and can no longer be upgraded** (`moving-values.md` row 77). That
>     retires the Phase-3 chain built on it as a *design instruction*, not just as a
>     stale ilvl.
>
> The Phase 0–2a ✅ claims stand as *shipped code*; treat their scores and worked
> numbers as a 2026-07-07 snapshot, not a current ranking.

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
| ~~Gear value = `min(slots)` vs scalar ceiling~~ **(Phase 2a ✅)** | `plan.py:slot_target_R()` now reads `yields.slots` (landing ilvl + fillable slots) via `rewards.best_slot_delta`; scalar `reward_ilvl_max` kept as fallback | per-slot: a 259 drop can't upgrade a 259 slot, so drops fall to R=0 for a geared main; one weak slot no longer inflates every activity |
| ~~No currency inventory in state~~ **(Phase 1 ✅)** | `plan.py:_char_state()` now maps the dump's `currencies` + `equipment`; a crest/bottleneck context line surfaces the balances | can now reason "176 Hero / 20 Myth crests, Myth is the bottleneck" |
| No deterministic-vs-RNG field | candidate schema (`gen_candidates.py:build_candidate`) | a guaranteed 100-accolade cache scores identically to a 1/12 boss drop |
| ~~No currency-quantity yield~~ **(Phase 1 ✅)** | `yields.currencies` on the activity front matter, carried into `candidates.json` | "yields 10 Hero + 5 Myth crests" is expressed; `currency_R` values it by pending consumer instead of a flat `reward_base=3` |
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

**Currency source (corrected — read the dump, not Syndicator).** The PlannerState
dump is already the source: **schema 4 dumps `currencies` (via `scanCurrencies`)
AND per-slot `equipment` directly** (verified on Encomplete's live dump), so the
planner needs no Syndicator round-trip (Syndicator is only for the `wowkb.character`
KB snapshots). Encomplete's balances (Hero 176, Myth 20, Field Accolade 1,309,
Nebulous Voidcore 11, Coffer Shards 58) come straight off the dump — a 2026-07-07
S1 reading, and note the **Voidcore line is now a dead balance**: S1 Voidcores
convert to gold at S1's end (see the 12.1 callout above), so treat that key as
present-but-unspendable until S2 restores Voidcores as a vault reward. **Two real gaps
remain:** (1) `equipment` carries `itemID` + `ilvl` but **not the upgrade track/level**
("Hero 3/6") — needed to read a slot's remaining crest headroom; (2) **Sparks of
Radiance, Catalyst charges, Ascendant Voidshards** aren't dumped yet (note: *Radiant
Spark Dust* — a distinct currency — **is** in the dump, and Phase 1's spark consumer
already keys off it). Per [resolved-Q5](#resolved-questions-verified-2026-07-07) the
fix for both is to **extend the PlannerState addon** (dump the missing IDs + gear
track via `C_Item.GetItemUpgradeInfo`, bump to schema 5); until then, Phase 1
approximates gear headroom from `ilvl` vs the track ceiling (Hero **276**) and keeps
the uncaptured currencies at R=0 / the manual (`todo.md`) tier.

### 2. Derive needs (the new core object)

A **need** is a structured, character-scoped want with a value weight. Types:

- `slot_upgrade{char, slot, from_ilvl, to_ilvl, via: crest|drop|vendor|craft, cost}`
- `currency_accumulate{char, currency, have, target, purpose}` — e.g. *Myth crests
  to recraft the waist 259→285*; this is where bottleneck logic lives.
- `power_unlock{char, system}` — Omnium Folio rows, embellishments, Nilhammer chain.
- `alt_gearing{char, via_source}` — **warbound** caches, drops. ⚠ The S1
  Champion/Heroic caches this example was written against were **removed in 12.1**;
  the only warbound cache today is the **S2 Adventurer** one at 200 Field Accolades
  (see the 12.1 callout above). The `warbound: true` flag is what the model keys off,
  and that survives.
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
  the remaining need and the remaining weekly cap**. (This is what made Ritual
  Sites T6 — 5 Myth + 10 Hero Dawncrests/run — beat a world-boss drop for
  Encomplete **in Season 1**. ⚠ **12.1 removed that yield:** Ritual Site tiers 1–6
  now pay **Season 2 crests at Delve-equivalent rates**, i.e. only up to **Veteran
  Mistcrests** — see `systems/ritual-sites.md`. The example still illustrates how
  `marginal()` works; it is no longer a live recommendation.)
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
weekly_cap: { runs: 6 }        # illustrative only; caps marginal()
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
  a BoP Hero cache doesn't upgrade him — but a **warbound** cache turns that
  stockpile into alt pieces. The planner should surface "spend Accolades →
  warbound caches → Uncomplete/Hallick" as a **top-of-roster** play.
  ⚠ **The cache table this was written against is gone (12.1).** The S1 caches
  (Warbound Champion 100 · Warbound Heroic 750, the latter flipped BoP→Warbound in
  the June 26/30 hotfixes) were **removed**; today it is **S2 Adventurer *Warbound*
  200** and **S2 Veteran *BoP* 500 (random) / 750 (slot-specific)**
  ([`moving-values.md` row 75](../_meta/moving-values.md)). Note the flip: the
  warbound tier is now the *lowest* one, so the alt-feeding math is 1,309 → ~6
  Adventurer pieces, and the Veteran caches feed **nobody but the buyer**. Re-derive
  the numbers when Phase 4 lands; the `warbound: true` yield flag is what the model
  actually keys off, and that survives.
- **Leveler synergy.** XP-bearing activities (e.g. Void Assault's 12.0.7-doubled
  XP) are valued **only for roster members below cap** — worthless on the 90 main,
  high for the leveler. (Turbulent Timeways was the other example here; the event
  **ended 2026-08-11**, so it is out of the ranking entirely.)

## Fun / collectibles

Model `collectible` needs explicitly: `value = novelty · scarcity / effort`, so a
limited-time mount or a "shoots rainbows" toy competes on its own axis instead of
riding the crude U-floor. `--mood fun` raises the collectible weight; `efficiency`
lowers it. This is the concrete version of README goal #2 ("don't let efficiency
crowd out rare/limited events").

## Infrastructure already built (build on it, don't rebuild)

Distilled from the earlier `scratchpad/phase2-plan.md` (2026-07-06, superseded by
this doc) and re-checked against the live code 2026-07-07. Two things already exist
that the phases below plug into rather than reinvent:

- **`tools/wowkb/rewards.py` — the valuation layer (built + unit-tested; the
  currency branch is now WIRED to `plan.py`, Phase 1).** `value_quest(descriptor,
  char_state)` carries a **character-relative branch** (`_value_char_relative`): gear
  scores by `reward_ilvl − your weakest slot`, currency by whether it advances an
  *uncapped* track. Its `char_state` schema — `{ilvl_by_slot, track_caps, renown,
  currencies}` — is the needs-first "scan state" object under another name. **Phase 1
  extended it** with the currency→consumer layer (`CREST_CEILING`/`track_of_ilvl`,
  `CURRENCY_CONSUMERS`, `currency_yield_R`) and wired that into `plan.py:score()` via
  `currency_R` (the `max(breakpoint, slot-target, currency)` override) — so it's now
  **called with a real dump** (Encomplete), not just synthetic `char_state`. Still
  unwired for Phase 2: the gear-drop (`_value_char_relative` items path) and the
  recipe/craft table. Plus `classify_currency`/`CURRENCY_RULES`, `classify_cache`,
  `TRACK_R`/`TRACK_ORDER`. Prefer extending `rewards.py` (stdlib, offline-testable)
  over inlining valuation in `plan.py`. Exercised by `check_rewards.py` (synthetic)
  **and now `check_currency.py`** (Phase 1's consumer rules).

- **The PlannerState dump (schema 4) already carries the raw state** — `currencies`
  + per-slot `equipment` + `vault`/`weeklyQuests`/`mythicPlus`/`lockouts`/`calendar`.
  The one equipment gap is the missing upgrade **track/level** (see Scan-state's
  "Currency source" note above): fix by extending the addon (schema 5) or approximate
  from `ilvl` vs the Hero **276** ceiling (what Phase 1 does).

- **Verification discipline (carry it into every phase).** Each scoring change gets
  an offline `.lua` fixture + a stdlib-only `tools/tests/check_*.py` mirroring the
  existing suites; keep the whole suite green; after any `activities/*.md` edit run
  `gen_candidates` + `--check`; and keep the contracts (`scoring-model.md`,
  `activities/_facets.md`) in sync **in the same commit** as the code.

## Staged implementation plan

Order is chosen so each stage ships value and de-risks the next.

- **Phase 0 — data corrections (cheap, no architecture). ✅ DONE (2026-07-07).**
  Fixed the `279`→`276` placeholder across the activity files (world-boss, prey-weekly,
  delve-bountiful, val-naigtal, showdown-weekly, voidcores + the `plan.py:slot_target_R`
  docstring); dropped the Singularity renown value once past the unlock rank
  (`renown-dungeon-weekly` pinned `reward_base: 1`; make it conditional-on-renown in
  Phase 4); stopped valuing Void Assault XP at cap (`void-assault` reward detail flags
  the doubled XP as leveler-only); promoted Ritual Sites T6 out of the backlog
  (`ritual-sites` surfaced the 5 Myth + 10 Heroic Dawncrests/run — **in Season 1**
  the only repeatable solo Myth-crest farm; ⚠ **12.1 removed that yield entirely**,
  and there is currently **no repeatable solo Myth-crest source** — Myth Mistcrests
  come only from Mythic Venomous Abyss and +9 keys); handled the `raid_weekly` (lockout match) / `campaign_incomplete`
  (level-cap proxy) gates that fell through to `unknown` (`plan.py:gate_status`).
  `void-incursions.md` was corrected in the hotfix sweep (the S1 Heroic cache had
  flipped BoP→Warbound). ⚠ **That cache no longer exists:** 12.1 removed the Season 1
  gear caches outright ([`moving-values.md` row 75](../_meta/moving-values.md);
  `patch-notes/12.1.md`, VOID-TOUCHED CACHES) — read this bullet as a record of what
  Phase 0 fixed, not as a current cache fact. `candidates.json` regenerated; the `@verify-ingame` on the Sporefall lockout
  name is on the generated checklist.
- **Phase 1 — currency inventory + pending-consumer valuation. ✅ DONE (2026-07-07).**
  Read `currencies` off the dump (already there — no Syndicator). Implemented as a
  per-candidate **scoring override** (not yet the formal `Need` object — that lands
  in Phase 2 when dedup needs it), consistent with "each stage ships value." The
  sharp rule (phase2's 2.1): a currency scores by the **marginal value of the best
  unlock it enables *right now*, → 0 when there's no pending consumer** — crests → 0
  once every equipped slot is track-capped; Field Accolades → the `slot_target`-shape
  R of the ~259 Hero box they'd buy, → 0 when weakest ≥ 259; Sparks → 0 with no craft
  queued. Pure valuation lives in `rewards.py` (`CREST_CEILING`/`track_of_ilvl`,
  `CURRENCY_CONSUMERS`, `currency_yield_R`), thin orchestration in
  `plan.py:currency_R()` — folded into the existing
  `max(breakpoint, slot-target, currency)` override; genuine crest/accolade sources
  declare `yields.currencies` (canonical keys) in their activity front matter, carried
  through `gen_candidates`. A crest/bottleneck context line now surfaces the balances
  (Myth flagged as Encomplete's binding constraint). **Headline test met:**
  `ritual-sites` (crest/accolade source, no direct `reward_ilvl_max`) scores 4.8 for
  Encomplete (Myth-crest consumer) and falls to **0** for a fully-276 main — verified
  end-to-end on the live dump + `tools/tests/check_currency.py` (18 checks). Track/level
  on equipment is still approximated from ilvl vs the Hero **276** ceiling (addon dump
  deferred). First real needs-first scoring: crests over drops for a geared main.
- **Phase 2 — per-slot reward vectors + `slot_target_R` rewrite + dedup**
  (subsumes roadmap **B**). Kills the one-weak-slot inflation.
  - **2a — per-slot reward vectors + `slot_target_R` rewrite. ✅ DONE (2026-07-07).**
    Gear-drop activities declare `yields.slots` (`{track, ilvl, chance, slots}`,
    where `ilvl` is the drop's **landing** ilvl — Hero 259, faction champion 246 —
    **not** the crested ceiling); `plan.py:slot_target_R()` values the best positive
    `landing − current_slot` delta across the slots the drop can fill (helper
    `rewards.best_slot_delta`), scalar `reward_ilvl_max` kept as the fallback
    (raid). Fixes both failure modes #1 (one weak slot inflating many activities)
    and #2 (ceiling ≠ upgrade). `chance` is carried but unapplied (Phase 3 EV).
    Headline realized: for the geared main every gear drop falls to R=0 on the slot
    term while the Phase-1 currency winners (Ritual Sites Myth crests) stay on top;
    a fresh 90 still sees the drops as big upgrades. Verified with
    `tools/tests/check_slot_vector.py` + `fixtures/equipment-encomplete.lua` and
    end-to-end on the live dump. **2b/2c below still pending.**
  - **2b — dedup / diminishing returns** (deferred). Re-derive/decrement the
    need-set after each greedy pick so filling one slot stops pulling every other.
  - **2c — crafting as a gear source** (deferred). **Add crafting as a
  gear source** (phase2's 2.2): from a recipe→(slot, ilvl, reagents) table seeded off
  `systems/tailoring-recipes.md` (88 entries) + the char's profession/skill,
  synthesize `craft-<slot>` candidates that compete through the same per-slot logic —
  a craftable 285 Back beats most drops for a geared main, and a *queued craft is the
  pending consumer* that makes a Spark reward worth > 0 (closes the loop with Phase 1).
- **Phase 3 — deterministic-vs-RNG EV + prerequisite chains.** Sure exchanges beat
  lotteries. **Value multi-step chains by their discounted terminal** (phase2's 2.3):
  score the terminal via `slot_target_R`, apply a per-step discount, and surface "next
  step in chain X" — so a Myth chain ranks high *because* its terminal exceeds 276,
  not for its cheap early steps. Chains to encode (facts already in KB):
  **Nilhammer/Ascendant → weapon 295** (`systems/void-forge.md`), ~~**Val/Naigtal
  heroic → Void Commander's Emblems → Myth belt quest**~~ ([resolved-Q3](#resolved-questions-verified-2026-07-07))
  — ⚠ **do not encode this one**: as of 12.1 the "Knocking Off the Top (Heroic)"
  reward **stays a Season 1 item and can no longer be upgraded**
  ([`moving-values.md` row 77](../_meta/moving-values.md)), so its terminal no longer
  clears the S2 ladder and the chain is dead as an instruction, not merely re-numbered —
  **Prey → Nightmare unlock → Ascendant Voidshards** (`activities/prey-weekly.md`).
  The chain *mechanism* (discounted terminal) still needs ≥2 live examples; find a
  Season-2 replacement before building it.
- **Phase 4 — cross-character roster + warbound flows + `scope`.** The big payoff.
  Add a **`--solo` coordination-cost penalty** — down-rank M+/raid when you can't
  field a group — so group content stops out-ranking solo plays on a solo night.
- **Phase 5 — collectible/fun needs; an "expiring windows" output block** (Darkmoon
  Faire and other limited-window event deadlines surfaced independently of reset
  gating, so a closing window isn't buried); `todo.md` auto-population; (long-term) the PlannerState in-game checklist UI
  so manual-tier items are ticked in-game.

Roadmap **A** (formula rebalance, `sqrt(T)`) and **C** (de-noise repeatables)
fold in as tuning of the Phase 1–2 scoring loop.

## Resolved questions (verified 2026-07-07)

All five were resolved — four via web verification against Tier-1/3 sources,
one as a design decision. **Four of the five (1, 2, 3 and 4) have since been
overtaken by 12.1** and are struck below; read those as the Season 1 record plus the
transferable lesson, never as buildable instructions. Findings were pushed to the topic files of record
(this doc defers to them; citations live there). The handful of residual
*in-game* spot-confirmations these surfaced (e.g. the Omnium rune-effect scope)
are no longer loose ends: they carry `@verify-ingame` markers and appear on the
generated checklist at `_meta/verify-in-game.md`, which `/sync-characters` shows
while you're logged in.

1. ~~**Warbound Heroic cache — price is 750**~~ **(SEASON 1 — HISTORICAL, the
   caches were removed in 12.1.)** *S1 finding, retained for the reasoning only:*
   Warbound Heroic cache 750 (Champion cache 100), unchanged by the June 26/30
   Showdown hotfixes; the conflation trap was that the *slot-specific* Heroic cache
   was 750 while a separate *random-slot* Heroic cache was discounted to 100.
   **None of those caches exist now** — 12.1 removed the S1 gear caches and replaced
   them with **S2 Adventurer Warbound 200** / **S2 Veteran BoP 500 (random) / 750
   (slot-specific)** ([`moving-values.md` row 75](../_meta/moving-values.md)). The
   *transferable* lesson is the trap itself: price alone does not identify a cache —
   always pin **tier + warbound/BoP + random/slot-specific** together.
   Home: `systems/void-incursions.md`, `systems/ritual-sites.md`.

2. ~~**Weekly caps — resolved.**~~ **(SEASON 1 — SUSPENDED IN 12.1; the numbers are
   deleted, not re-hedged.)** The S1 finding was a Restored-Coffer-Key weekly hard cap
   plus a Delver's-Journey-gated Myth gilded stash, and it closed the delve TODO. **None
   of that is a current fact.** In the 12.1 pre-season week there are **no Coffer Keys
   and no Bountiful Delves at all**, and Delves cap at **Adventurer 3/6 gear + Veteran
   crests**; keys begin dropping again with maintenance the **week of Aug 18**
   ([`moving-values.md` row 64](../_meta/moving-values.md); `patch-notes/12.1.md`,
   Season 2 pre-season). 12.1 separately **retuned Coffer Key Shard amounts across
   multiple sources**, and Blizzard calls that tuning **ongoing / a work in progress**
   ([row 94](../_meta/moving-values.md)) — so no shard or weekly-Myth-output number is
   carried forward here. This is a **structural** suspension, not a numeric drift, so
   the "everything numeric below is Season 1" scoping does **not** cover it: a delve
   activity's `weekly_cap` and Myth-crest yield have **no S2 value to fill in yet**.
   Re-derive from `endgame/delves/overview.md` once Season 2 proper is running.

3. **Val/Naigtal Myth claims — both literal claims FALSE, but they map to a real
   mechanic the KB was missing.** World-boss loot never escalates to Myth (caps at
   Warbound Heroic) and Val/Naigtal crests cap at Heroic (no Myth crests) — the KB
   was already right on both. The "4× world boss → Myth" memory is really the quest
   **"Knocking Off the Top (Heroic)"**: collect **4 Void Commander's Emblems** (one
   per weekly lockout from the Heroic-WT world bosses) → **one Myth 1/6 item, ilvl
   272, choice of Cloak / Belt / Bracers** — the only Myth-track reward from
   open-world content. **Now documented in `endgame/world-events.md`.**
   **Planner impact (S1 — NO LONGER BUILDABLE):** it *was* a deterministic ~4-week
   path to a **Myth belt** satisfying Encomplete's waist need without the Myth-crest
   recraft. ⚠ **12.1 froze it:** the "Knocking Off the Top (Heroic)" reward stays a
   **Season 1 item and can no longer be upgraded**
   ([`moving-values.md` row 77](../_meta/moving-values.md)), so it is not a
   competitive `slot_upgrade` on the S2 ladder and **must not be encoded in Phase 3**.
   The *mechanic* finding (both literal claims false; world-boss loot caps at Warbound
   Heroic; Val/Naigtal crests capped at Heroic) stands as the S1 record.

4. **Omnium Folio — row progression is ACCOUNT-WIDE.** Earning a Mote of Omnial
   Inquiry on any one character unlocks that row for the whole warband; the only
   per-character step is the one-time **Sunstrider Omnium intro questline**. So the
   planner models it as an **account need** (run the ~5 weekly "Seeking Knowledge"
   quests once, on any character) **+ a one-time per-character unlock-questline
   task** — *not* a weekly per-alt repeat. Rune effect/config is per-character
   (low-med confidence, unverified vs Tier-1). Home: `systems/omnium-folio.md`.
   ⚠ **OVERTAKEN BY 12.1 (2026-08-11):** the intro questline "can now be skipped
   across characters on the account once it has been completed by at least one
   character" (Tier 1, 12.1 notes → QUESTS). So the "+ a one-time per-character
   unlock-questline task" half of this instruction is **dead** — the planner should
   model Omnium Folio as a **pure account need** with no per-character step, which
   is how `systems/omnium-folio.md` now describes it. Do not build the two-part
   model above.

5. **Currency capture gaps — decision: addon-dump, not manual tier.** The premise
   ("invisible to Syndicator") holds but doesn't force a manual tier: PlannerState
   is *our* addon and all three are reachable from the WoW API — **Catalyst charges**
   and **Ascendant Voidshards** are currencies (`C_CurrencyInfo.GetCurrencyInfo` by
   ID), **Sparks of Radiance** is an item (`GetItemCount` by ID). Extend
   PlannerState to dump those three IDs explicitly (resolve IDs via the wago
   `CurrencyTypes` DB2, as `wowkb.character` already does). Keep the manual
   (`todo.md`) tier only as the stopgap until that dump ships — it folds into
   **Phase 5**. Leaving them permanently manual defeats the deterministic-scan
   premise of the whole redesign.

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

> **Realized so far (Phases 1 + 2a, 2026-07-07):** both halves of the worked
> example are now live. **Currency half (Phase 1):** Ritual Sites is lifted by its
> Myth-crest consumer (`reward_base 3 → currency_R 4`, score 3.6 → **4.8**) and the
> crest/bottleneck line surfaces "Myth 20 (bottleneck)." **Gear-drop half (Phase
> 2a):** ⚠ *(Season 1 worked example — `timeways` has since ended, `world-boss` is
> superseded by Lairs and frozen at S1, and S1 `voidcores` converted to gold; the
> mechanism holds, the list does not.)* world-boss / voidcores / prey / delve /
> showdown / timeways / faction drops
> now fall to **R=0 on the slot term** for Encomplete (a 259 Hero drop can't beat his
> 259 slots — "no slot upgrade — drop lands ≤ your slots"), landing at the bottom of
> the list, while the same drops still score 20+ for the fresh alt Uncomplete — the
> value is finally character-relative. Not yet: **dedup (2b)** so filling one slot
> stops pulling the others; **crafting-as-gear (2c)**; and the Accolade→warbound-alt
> flow (**Phase 4**).

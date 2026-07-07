---
title: Session Planning — Scoring Model (efficiency-first)
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - knowledge/endgame/weekly-checklist.md          # the candidate-task universe
  - knowledge/characters/encomplete-plan.md         # a hand-scored instance of this model
confidence: high     # this is a methodology doc, not a fetched game fact — "high" = we endorse the framework
---

# Session Planning — Scoring Model

> **What this is.** The explicit, tunable heuristic that turns "~100 things I
> *could* do" into "the 3–5 things worth doing **this** session." It is the
> scoring function behind three separate deliverables that don't exist yet:
> the **state-aware weekly planner** (efficiency), the **fun radar** (novelty/
> FOMO), and any future auto-ranker. Those are *implementations*; this doc is
> the *contract*. Tune the numbers here, not in the code.
>
> **Default stance: efficiency-first** (user call, 2026-07-02). Power/progress
> per minute wins. Fun is not force-slotted — it surfaces through the *urgency*
> term (rare/expiring things score up) and as explicit callouts, never by
> displacing a higher-value power task. See [[fun-radar]] for the counterweight.

## The candidate-task model

Every doable thing is a **candidate** with these fields. The planner enumerates
candidates from `weekly-checklist.md` + live calendar + character state, then
scores each one.

| Field | Symbol | Range | Meaning |
|---|---|---|---|
| Reward | **R** | 0–5 | Power/progress toward a breakpoint *you care about* |
| Urgency | **U** | 0.5–3 | Expiry pressure — resets Tuesday? one-time? rare event? |
| Enjoyment | **E** | 0.2–1.5 | Personal per-activity multiplier (see table below) |
| Time cost | **T** | blocks | Wall-clock in 15-min blocks (a delve ≈ 1, a raid night ≈ 8) |
| Gate | — | pass/fail | Hard filter: locked, capped, or needs a group you lack |

### Score

```
score = (R × U × E) / T          # if Gate passes; else score = 0
```

Then: **filter out gated/capped → sort by score → walk the list top-down,
taking items until the session time budget is spent.** That greedy walk is the
"narrow 100 → a few" step. Present each pick with a one-line *why* (the
dominant term — "resets tonight," "closes your weakest slot," "rare, don't own
the mount").

## Scoring the terms

### R — Reward (0–5), efficiency-first's heavy hitter

Not raw item level — **marginal value to a breakpoint you actually care
about.** Two multipliers stack inside R:

- **Slot targeting.** An upgrade to your *weakest* slot is worth more than one
  to an already-strong slot. A sidegrade or vendor-trash reward is R≈0.
  **Per-slot vectors (needs-first Phase 2a, 2026-07-07):** a gear-drop activity
  declares `yields.slots` — a vector of `{track, ilvl, chance, slots}` where
  **`ilvl` is the drop's LANDING ilvl, not the crested ceiling** (a Hero drop
  *lands* at **259** (1/6), climbing to 276 only via crests — the currency path;
  a faction champion piece lands at **246**). `plan.py:slot_target_R()` reads the
  dump's per-slot ilvls (schema≥4) and values the drop **per slot it can fill**
  (`[all]` = any equipped slot): the best positive `landing_ilvl − current_slot`
  delta, `R = min(5, 1 + Δ/6)`; no fillable slot upgraded → R=0. This **replaced**
  the old "scalar `reward_ilvl_max` vs the single weakest slot," which let one weak
  slot inflate every Hero-ceiling activity at once (redesign failure mode #1) and
  mistook the 276 ceiling for a guaranteed upgrade (failure mode #2). Un-migrated
  activities (e.g. `sporefall-raid`'s per-difficulty ceiling) still fall back to
  the scalar `reward_ilvl_max` path. No `yields.slots`/`reward_ilvl_max`, or a
  pre-schema-4 dump → no override, keep `reward_base`. **Headline (Encomplete,
  geared main):** world-boss/voidcore/prey/delve/showdown/timeways/faction drops
  all fall to R=0 on the slot term (a 259 drop can't beat his 259 slots), while a
  fresh 90 still sees them as big upgrades — the value is now character-relative.
- **Currency consumer (needs-first Phase 1, 2026-07-07).** A currency is worth
  farming only while the character still has something to **spend** it on — "crests
  over drops for a geared main," but a crest source drops to ~0 once every slot is
  track-capped. An activity declares its per-run `yields.currencies` (canonical
  keys, `activities/_facets.md`); `rewards.currency_yield_R()` values the **best
  pending consumer** across them and `plan.py:currency_R()` feeds it into the same
  `max(breakpoint, slot-target, currency)` override. The rules:
  - **Hero crest** → consumer iff any equipped slot `< 276` (Hero cap); R scales
    with the weakest sub-cap slot's headroom (same `1 + Δ/6` shape as slot-target).
  - **Myth crest** → the binding constraint: high flat R (**4**) while a consumer
    is pending, `0` once Myth-capped. Phase-1 approximation of "not Myth-capped":
    still holding sub-276 slots (real per-slot track needs the addon dump).
  - **Field Accolade** → values the ~259 Hero box Maren sells → `0` once the
    weakest slot ≥ 259 (own-char only; the warbound-cache-for-alts value of a big
    Accolade stockpile is Phase 4).
  - **Spark / spark dust** → `0` this phase (no craft is queued until the Phase-2
    crafting model supplies the consumer).
  No `yields.currencies`, or no equipment in the dump → no override, keep
  `reward_base`. **Headline:** ritual-sites (Myth+Hero crest source, no
  `reward_ilvl_max`) stays high for a weak-slot main yet falls to ~0 for a
  fully-276 one — the first real needs-first behavior.
- **Breakpoint proximity.** Progress is worth more the closer it sits to a
  discrete payoff. Examples of breakpoints, not smooth curves:
  - **Great Vault**: 1 / 4 / 8 M+ runs (or delve/raid equivalents) unlock
    slots — the run that *crosses* a threshold is R≈4; a run past 8 is R≈0.
  - **Delver's Journey rank-up** (Gilded Jackpot = Myth crests): the last run
    into a rank is high R; mid-rank grinding is low.
  - **Renown level** that unlocks a specific gear/recipe reward.
  - **Currency cap** you're about to waste (or a craft you can finally afford).

| R | Meaning |
|---|---|
| 5 | Crosses a breakpoint **and** lands in your weakest slot / unblocks a system |
| 4 | Crosses a Vault/journey/renown breakpoint, or targeted weak-slot upgrade |
| 3 | Solid power/currency toward a breakpoint you'll hit soon |
| 2 | Generic progress, no near breakpoint |
| 1 | Marginal (5th ilvl on a strong slot, trickle currency) |
| 0 | Cosmetic-only / capped / sidegrade — R contributes nothing to *efficiency* |

> Cosmetic and collectible rewards score **R=0 on purpose** — efficiency-first
> deliberately blinds R to fun. Their value re-enters through **U** (a rare
> event is urgent) so they can still surface, but never outrank real power at
> equal urgency. That is the whole efficiency-vs-fun dial: it's the R-vs-U
> balance, not a separate system.

### U — Urgency (0.5–3), the FOMO/expiry term

| U | Meaning |
|---|---|
| 3 | **One-time or annual** — won't come back for a long time (holiday-exclusive mount, a Feat of Strength, a first-time catch-up bonus) |
| 2 | **Expires this reset** — the weekly you haven't done; Vault fills tonight |
| 1.5 | Limited-time event live *now* but recurring (Timewalking week, Darkmoon Faire) |
| 1 | Standing content, always available (ritual sites, delve farming) |
| 0.5 | Actively *worse* to do now than later (a tier you'll faceroll in 2 weeks) |

Urgency is how fun gets its foot in the door under an efficiency-first regime:
a rare collectible is R=0 but U=3, so `0 × 3 = 0`… which means **pure-cosmetic
rare rewards still need a nonzero R to surface.** Resolution: give
collectible/novelty rewards a floor of **R=1** *only when the U is ≥1.5* (rare
and live). That keeps a genuinely rare mount in the shortlist's tail without
letting routine cosmetics compete with gear. This floor is the one deliberate
crack in "efficiency-first" — widen it if the plans feel joyless.

### E — Enjoyment (0.2–1.5), personal and tunable

Your per-activity multiplier. **Capped at 1.5 so it can bend the ranking but
not invert it** — a beloved activity can't leapfrog a much higher-R task, only
break ties and win among equals. Seeded from observed play (solo-leaning,
delve/ritual-site heavy, PvP deprioritized); **tune these as you learn your own
preferences** — this table is the single knob for "make the plans feel more
like me."

| Activity | E | Note |
|---|---|---|
| Delves (solo) | 1.4 | Core loop; you clear T9+ solo |
| Ritual sites | 1.2 | Solo-friendly power engine |
| Prey hunts | 1.1 | Capped/quick, tolerated |
| Mythic+ | 1.0 | Now engaging it (1093 IO), neutral baseline |
| Housing / Trading Post | 1.0 | Flavor; low time cost keeps them viable anyway |
| Crafting / professions | 0.9 | Means-to-an-end |
| Raid (group) | 0.7 | No Midnight kills logged; group-gated |
| PvP (Slayer's, Decor Duels) | 0.4 | Cosmetics-only, deprioritized |

### T — Time cost (blocks of ~15 min)

Normalizes everything to per-minute value — the crux of "limited playtime."
Rough table: prey hunt 0.5 · delve 1 · ritual site 1 · M+ key 2 · weekly quest
0.5 · raid night 8. **A high-R task that eats the whole session can still lose
to two medium-R tasks that fit** — that's the greedy walk doing its job.

### Gate — hard filters (score → 0)

Drop before scoring, don't rank: already done/capped this reset · locked behind
an unfinished questline · needs a group/key you don't have right now · below the
ilvl to survive · currency you can't yet afford. **This is where state-awareness
lives** — the planner must know what you've *already done this reset* to zero
out completed weeklies (that's the gap between a static checklist and a real
planner; it needs the profile API + likely an addon dump).

## The session-planning algorithm

```
INPUT:  character state, live calendar, time budget (minutes), mood (default: efficiency)
1. ENUMERATE candidates  ← weekly-checklist.md + calendar events + open plan items
2. GATE                  ← drop done/capped/locked/group-gated/can't-afford
3. SCORE each            ← (R × U × E) / T,  with the U≥1.5 collectible R-floor
4. SORT desc by score
5. GREEDY WALK           ← take items top-down until time budget spent
6. PRESENT               ← 3–5 picks, each with its dominant-term "why"
```

Mood = efficiency (default) uses the weights above. A future "fun mode" would
just lift the E cap and raise the collectible R-floor — **same model, retuned**,
which is why we're not building a second one.

## Worked example (Encomplete, 2026-07-02, ~60 min = 4 blocks)

Illustrative — real R/U depend on live reset state:

| Candidate | R | U | E | T | Score | Why it ranks there |
|---|---|---|---|---|---|---|
| Open Great Vault | 4 | 2 | 1.0 | 0.3 | **26.7** | Free power, expires, trivial time |
| Delve targeting **back (250)** | 4 | 1 | 1.4 | 1 | **5.6** | Closes the weakest slot |
| M+ run crossing a Vault threshold | 4 | 2 | 1.0 | 2 | **4.0** | Breakpoint + resets tonight |
| Ritual site (Hero crests) | 3 | 1 | 1.2 | 1 | **3.6** | Steady power engine |
| Prey weekly (3 hunts) | 2 | 2 | 1.1 | 1.5 | **2.9** | Resets, but low marginal power |
| Turbulent Timeways (rare mount you lack) | 1* | 3 | 1.0 | 2 | **1.5** | *R-floored — the fun that survives efficiency-first |
| Decor Duels (PvP cosmetic) | 0 | 1 | 0.4 | 1 | **0** | Gated out by efficiency-first |

Greedy walk at 4 blocks → **Vault → back-targeted delve → the threshold M+**,
with the rare-mount Timeway as the "if you've got 30 more min and want a treat"
tail. That last line is exactly how efficiency-first still leaves room for fun
without letting it drive.

## How this gets tuned (the KB grows through use)

- After sessions that felt bad, adjust: too grindy → raise the E cap / the
  collectible floor; too scattered → the T normalization or budget is off;
  wrong things surfaced → an R breakpoint is mis-set.
- The **E table is the main knob** — it's the only fully-personal input.
- Record notable retunes inline so the reasoning survives, same as the plans do.

## TODO / open questions

- [ ] Nail down the **state-awareness source** for the Gate step: which weeklies
      the profile API exposes as done vs. what needs an addon SavedVariables dump.
- [x] **Breakpoint proximity (vault track) — implemented (2026-07-02).**
      `plan.py:breakpoint_R()` reads live M+ progress from the PlannerState dump and
      overrides R→4 for the run that *crosses* the next Great Vault threshold (1/4/8),
      R→0 once the track is capped. Verified offline against `tools/tests/fixtures/
      vault-*.lua` (`tools/tests/check_breakpoint.py`). Still open: journey rank-ups /
      non-vault breakpoints.
- [x] **Slot-targeting (ilvl-relative R) — implemented (2026-07-06).**
      `plan.py:slot_target_R()` reads the dump's per-slot `equipment` ilvls (schema≥4)
      and an activity's `reward_ilvl_max` ceiling; R→0 when the ceiling can't beat your
      weakest slot, scales up when it can. `score()` composes it with breakpoint
      proximity as **R = max(breakpoint, slot-target)**, falling back to `reward_base`
      when neither has data. Verified offline against `tools/tests/fixtures/equipment-*.lua`
      (`tools/tests/check_slot_target.py`).
- [x] **Per-slot reward vectors (v2b slot-targeting) — implemented (2026-07-07,
      needs-first Phase 2a).** Replaced the scalar-ceiling-vs-weakest-slot with a
      per-slot vector: gear-drop activities declare `yields.slots`
      (`{track, ilvl (LANDING, not ceiling), chance, slots}`), and
      `plan.py:slot_target_R()` (via `rewards.best_slot_delta`) values the best
      positive delta across the slots the drop can actually fill — killing the
      one-weak-slot inflation and the "ceiling = upgrade" error. A Hero drop lands
      at 259, so it's a sidegrade for a Hero-geared main (R=0) yet a big upgrade for
      a fresh 90. `reward_ilvl_max` remains as the fallback for un-migrated
      activities (raid). Verified offline against
      `tools/tests/fixtures/equipment-encomplete.lua` (`tools/tests/check_slot_vector.py`)
      and end-to-end on the live dump. **Deferred to later Phase 2 units:** dedup
      (2b) and crafting-as-gear (2c).
- [ ] Validate the E cap (1.5) and collectible R-floor (1 @ U≥1.5) against a few
      real sessions; these two numbers control the whole efficiency↔fun balance.
- [ ] `[[fun-radar]]` doc: the "events live now ∩ rewards I don't own" feed that
      supplies U=3 candidates to this model.

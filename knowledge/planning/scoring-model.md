---
title: Session Planning — Scoring Model (efficiency-first)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/endgame/weekly-checklist.md          # the candidate-task universe
  - knowledge/characters/encomplete-plan.md         # a hand-scored instance of this model
  - https://worldofwarcraft.com/en-us/news/24293281       # 12.1 "Curse of Ula'tek" content update notes (Tier 1) — S2 reward/crest changes
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 information (Tier 1) — the pre-season week rules
confidence: medium   # the FRAMEWORK is endorsed (high); the ilvl/crest constants baked into it are Season-1 and awaiting the S2 retune, and THREE coded rules point at content 12.1 REMOVED (Field Accolade → Maren box; the S1 Voidcore flow; the ritual-site Myth+Hero crest payout) — see the 12.1 note below
---

# Session Planning — Scoring Model

> ⏭ **Proposed successor:** `goal-model.md` (2026-07-10) reframes this activity-centric
> multiplier scorer as a **goal-centric** pipeline (per-slot upgrade graph → goals →
> rank → TODO steps). This doc remains the live model until that's built.

> ⚠ **12.1 status (2026-08-11) — the model is intact, its NUMBERS are Season 1.**
> The scoring *contract* below (terms, shapes, gate semantics, the greedy walk)
> survives 12.1 unchanged. But every absolute ilvl in it — the crest ceilings
> `Champion 263 · Hero 276 · Myth 285`†, the "Hero drop lands at 259," the
> "fully-276 main," the 246 faction piece — is a **Season 1** value, and Season 1
> ended with the week of Aug 11 maintenance. Season 2 crests are **Mistcrests**
> and the whole ladder shifted **+45**: Adventurer **269–282** · Veteran
> **282–295** · Champion **295–308** · Hero **308–321** · Myth **321–334**
> (`CurrencyTypes` DB2 @ 12.1.0.69214, IDs 3437–3441 — Tier-1 game data, the
> floor; see `_meta/moving-values.md`). Those numbers are also **hardcoded in the
> ranker** (`tools/wowkb/rewards.py:CREST_CEILING`, and the landing-ilvl prose in
> `plan.py`), so **until that retune lands the crest/slot terms score against a
> dead ladder** — an S2 269-ilvl drop reads as a downgrade against S1 slots, and a
> Hero Mistcrest's headroom is computed to 276 instead of 321. Treat every R
> produced by `wowkb.plan` as suspect until the retune is done (tracked in TODO
> below). The numbers are left in place in the prose *as a description of what the
> code currently does*, not as current game facts.
>
> † ⚠ **`Myth 285` is a pre-existing CODE BUG, not a Season-1 game fact.** The S1
> Myth Dawncrest band was **276–289**, so the true S1 ceiling was **289**
> (`_meta/moving-values.md`; `CurrencyTypes` DB2). `rewards.py:214`'s
> `CREST_CEILING` has carried **285** since it was written and this doc has been
> repeating it. Consequence for the retune below: set the constant to the S2 value
> **334** outright — do **not** add +45 to a wrong number. The same bad 285 also
> appears in the `CREST_FLOOR` craft-band prose further down, flagged there.
>
> ⚠ **Pre-season week (Aug 11–18) breaks one real assumption: the Gate step has no
> concept of "not available yet."** Gate filters *done / capped / locked / no group
> / can't afford* — all character-state predicates. It cannot express "this
> activity does not exist until 2026-08-18," which this week is true of Mythic+
> keystones, Bountiful Delves, the Venomous Abyss raid, Nightmare Prey and rated
> PvP — and **Voidcore bonus rolls** are on a *later* date still: they arrive the
> **week of Aug 25**, and then only for a character with **≥3 vault panes**
> unlocked. Without a date gate those rank normally and get recommended for a
> session in which they cannot be started. See the Gate section and TODO.

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
  declares `yields.slots` — a vector of `{track, ilvl, chance, targeted, slots}`
  where **`ilvl` is the drop's LANDING ilvl, not the crested ceiling** (⚠ *Season 1
  illustration, unretuned:* a Hero drop *lands* at **259** (1/6), climbing to 276 only
  via crests — the currency path; a faction champion piece lands at **246**. The Season 2
  shape is identical, 45 ilvl higher: e.g. Tidebound Grotto Heroic drops **Hero 1/6 = 305**,
  crestable to 321). `plan.py:slot_target_R()` reads the
  dump's per-slot ilvls (schema≥4) and values the drop **per slot it can fill**
  (`[all]` = any equipped slot): the best positive `landing_ilvl − current_slot`
  delta, `R = min(5, 1 + Δ/6)`; no fillable slot upgraded → R=0. This **replaced**
  the old "scalar `reward_ilvl_max` vs the single weakest slot," which let one weak
  slot inflate every Hero-ceiling activity at once (redesign failure mode #1) and
  mistook the 276 ceiling for a guaranteed upgrade (failure mode #2). Un-migrated
  activities (e.g. `sporefall-raid`'s per-difficulty ceiling) still fall back to
  the scalar `reward_ilvl_max` path. No `yields.slots`/`reward_ilvl_max`, or a
  pre-schema-4 dump → no override, keep `reward_base`.
  **Deterministic-vs-RNG EV (needs-first Phase 3, 2026-07-09):** the delta above is
  now an *effective* delta — `chance` (drop probability) multiplies it, and a
  **random-slot** roll (`[all]`, no `targeted`) is valued at the **expected** upgrade
  across its fillable slots (mean of positive deltas), not the best. A `targeted:
  true` vector (you pick the slot) keeps the exact best-slot value, so a targeted buy
  out-ranks a *guaranteed but random* roll for closing one specific gap. (⚠ The S1
  example of a targeted buy was the Field-Accolade → Maren Hero-259 box, which 12.1
  **removed**; the S2 stand-in is the **750-Accolade slot-specific Veteran cache** —
  its **500** sibling is random-slot and takes the EV treatment instead. See the
  Field Accolade bullet below.) **Headline (Encomplete, geared main):**
  world-boss/prey/delve/showdown/timeways/faction/val-naigtal/voidcore drops all fall to
  R=0 on the slot term (a 259 drop can't beat his 259 slots). A fresh 90 still sees every
  drop as a big upgrade — the value is character-relative.
  ⚠ **That enumeration is the Season 1 worked example and three of its entries no
  longer exist as written (12.1, 2026-08-11):** **timeways** — Turbulent Timeways
  **ended 2026-08-11** and is no longer rankable at all; **world-boss** — superseded
  by **Lairs**, and the old open-world drop is **frozen at Season 1 and can no longer
  be upgraded**, so it fails on more than the slot term; **voidcore** — Season 1
  Voidcores **converted to gold**, and bonus rolls do not return until the week of
  **2026-08-25**. The *mechanism* the example demonstrates (a drop at or below your
  slots scores 0) is unchanged and still correct; the *list* is not a current
  inventory. See `_meta/moving-values.md` and `_meta/changelog-12.1.md`. **Known gap:** R cannot tell
  whether a character can actually *reach* the content a reward's best roll comes from, so
  **content-capability gating** (Phase 4) is still owed — otherwise a currency ranks #1 for
  a fresh alt who can't run the key that makes it good.
  ⚠ **Do not illustrate that gap with Voidcores** — 12.1 **restructured them outright**,
  so the blanket "the numbers are S1" caveat does not cover them; the *mechanism* moved.
  S1 Voidcores **convert to gold** and are unusable in S1 content; from S2 they are a
  **Great Vault reward** (absent from the *first* S2 vault, arriving the **week of Aug 25**
  with **≥3 panes** unlocked); the raid re-roll cost drops to **1** (was 2); Orin
  Straylight grants **+1/week from week 8 of S2**. Derive a fresh illustration against the
  S2 Voidcore-as-vault-reward flow when Phase 4 lands.
- **Currency consumer (needs-first Phase 1, 2026-07-07).** A currency is worth
  farming only while the character still has something to **spend** it on — "crests
  over drops for a geared main," but a crest source drops to ~0 once every slot is
  track-capped. An activity declares its per-run `yields.currencies` (canonical
  keys, `activities/_facets.md`); `rewards.currency_yield_R()` values the **best
  pending consumer** across them and `plan.py:currency_R()` feeds it into the same
  `max(breakpoint, slot-target, currency)` override. The rules:
  - **Crests (Champion / Hero / Myth)** — *Phase B, 2026-07-10, track-aware.* Valued as
    `max(current upgrade headroom, future-material floor)` per tier:
    - **Upgrade headroom** uses the **real per-slot track/step** from the addon dump
      (schema≥8): across equipped slots *on that track below cap*, the largest ilvl gap to
      the crest ceiling (**Champion 263 · Hero 276 · Myth 285†** — ⚠ **what the code uses**;
      263/276 were the real Season 1 ceilings, **285 is a bug — the S1 Myth ceiling was
      289**, see † above. The Season 2 Mistcrest ceilings are **Champion 308 · Hero 321 ·
      Myth 334**), same `1 + Δ/6` shape.
      Falls back to the weakest-slot-ilvl approximation on a pre-schema-8 dump.
    - **Future-material floor** (`CREST_FLOOR`): a crest above current need is **never 0** —
      it banks toward later upgrades/crafts (80 Hero → a 259–272 craft, 80 Myth → 272–285
      — ⚠ that **285 is the same bad constant**, see †; the S1 Myth band topped out at 289) —
      but floors **below** the `1.0` foot-in-door of a real need, rarity-scaled
      (**Champion 0.25 · Hero 0.5 · Myth 0.75**). So a needed Hero crest (headroom ~3.8)
      outranks banked Myth (0.75), which still shows in value counts without pulling focus.
    - This **retires** the old flat "Myth = binding constraint, R=4" rule and finally
      **values Champion crests** (previously no consumer → 0, which under-served cappers).
    - ⏳ A *precise* craft-reagent term is deferred until Spark counts are dumped; the floor
      is its stand-in. (The overloaded `TRACK_CEILING`/`track_of_ilvl` band map still feeds
      the ilvl-band gear-*drop* fallback and is separately stale — see `_meta/kb-inbox.md`.)
  - **Field Accolade** → ⚠ **the consumer this rule is written against no longer
    exists** (2026-08-11). The coded rule — *value the ~259 Hero box Maren sells → `0`
    once the weakest slot ≥ 259* — describes **removed content**, not just a stale
    number: 12.1 **removed the Season 1 gear caches** and replaced them with a **Season 2
    Adventurer Warbound cache (200 Accolades)** and **Season 2 Veteran BoP caches (500
    random slot / 750 slot-specific)** (`_meta/patch-notes/12.1.md`,
    `_meta/moving-values.md` — Tier-1). Both the item **and its track** moved
    (Hero → Adventurer/Veteran), so the blanket "every absolute ilvl here is Season 1"
    caveat above does not cover it. Re-point at the S2 caches in the retune below:
    headroom against the **Adventurer 269–282** / **Veteran 282–295** bands, with
    `targeted: true` valuation only for the **750** slot-specific tier (500 is a random
    slot, so it takes the expected-upgrade treatment, per the RNG-EV rule above).
    Own-char only either way — and the new cache being **Warbound** makes the
    stockpile-for-alts value (Phase 4) larger, not smaller.
    *(Upstream ambiguity to be aware of: `_meta/moving-values.md` still carries the
    un-retired 12.0.7 "Maren sells slot-targeted Hero ~259" row alongside the 12.1
    removal row. The 12.1 row is the current one.)*
  - **Spark / spark dust** → `0` this phase (no craft is queued until the Phase-2
    crafting model supplies the consumer).
  No `yields.currencies`, or no equipment in the dump → no override, keep
  `reward_base`.
  ⚠ **Its headline illustration is Season-1-dead, mechanism and number both**
  (2026-08-11). It read: *"ritual-sites (Myth+Hero crest source, no
  `reward_ilvl_max`) stays high for a weak-slot main yet falls to ~0 for a
  fully-276 one — the first real needs-first behavior."* **12.1 removed the payout
  that rule was written against**: Ritual Site tiers 1–6 vault rewards now match
  the **Season 2 Delve** tiers 1–6, and the sites *"reward Season 2 crests
  equivalent to Delves at these tiers"* (`_meta/patch-notes/12.1.md:1302–1303`;
  `_meta/moving-values.md` — Tier-1). The T6 Myth+Hero Dawncrest payout is gone
  outright, so ritual sites are **not a Myth-crest source at all** in Season 2
  (`activities/ritual-sites.md`). Downstream in the code: that activity now
  declares `veteran_crest`, and `rewards.py`'s `CURRENCY_CONSUMERS` has **no
  `veteran_crest` entry**, so the row's crest yield currently values at **0** —
  the headline is wrong both as a game fact and as a description of what the
  ranker does. Like the Field Accolade rule above, this is *removed content*, not
  a stale number, so the blanket "the numbers are S1" caveat does not cover it:
  it needs a re-point in the retune below, not a +45 shift.
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
| Mythic+ | 1.0 | Now engaging it (1093 IO **at S1 close** — ratings reset for S2), neutral baseline |
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

**Missing gate class: availability window (found 2026-08-11, pre-season week).**
Every gate above is a *character-state* predicate. None of them can say **"this
activity does not exist yet"** — a calendar fact about the world, identical for
every character. The 12.1 pre-season week (Aug 11 → 18) is the first time this
bit hard: Mythic+ keystones, Bountiful Delves, the Venomous Abyss raid, Nightmare
Prey and rated PvP are all in the catalog and all unstartable until
**2026-08-18**, while Turbulent Timeways went the other way and **ended
2026-08-11**. **Voidcore bonus rolls are the case that proves one date is not
enough:** they do not arrive with Season 2 at all — they open the **week of Aug
25**, and then only for a character who has unlocked **≥3 vault panes**
(`_meta/patch-notes/12.1.md`, `_meta/moving-values.md`). So a real window is
per-activity, has its own `from`, and can carry a character-state predicate on
top of it. The fix is a declared window on the activity
(`available: {from: <date>, until: <date>}` in `activities/_facets.md`), gated
before scoring — *not* an E or U nudge, because a thing you cannot start has no
rank, it has no row. Until that ships, the pre-season catalog must be corrected
per-activity (`status: invalidated` / prose), which is what the 12.1 sweep did.
Note the near-miss too: **U=2 "expires this reset"** is still *correct* this week
for anything live, but the Great Vault's own R is not — this week's vault pays out
your **final Season 1** week while Season 2 credit starts accruing underneath it,
so `breakpoint_R()`'s 1/4/8 thresholds are counting toward *next* week's reward.

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

Illustrative — real R/U depend on live reset state. ⚠ **Kept as a historical
Season-1 worked example, not a menu for today:** the ilvls are S1, Turbulent
Timeways **ended 2026-08-11**, and during the pre-season week the M+ row is not
runnable at all (no keystones until Aug 18). The *arithmetic* is the point.

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

- [ ] **🔴 Season 2 ilvl retune (blocks trusting any `wowkb.plan` R, opened
      2026-08-11).** Every absolute ilvl in this model and in the ranker is Season 1.
      Move `rewards.py:CREST_CEILING` to the Mistcrest ceilings (**Champion 308 ·
      Hero 321 · Myth 334**), the `CREST_FLOOR` craft-band comments to the S2 bands
      (Adventurer 269–282 · Veteran 282–295 · Champion 295–308 · Hero 308–321 ·
      Myth 321–334), and re-declare every activity's `yields.slots` landing ilvls at
      S2 values. Source of truth: `_meta/moving-values.md` (Tier-1 `CurrencyTypes`
      DB2 @ 12.1.0.69214, IDs 3437–3441) — do **not** take these off editorial prose.
      ⚠ **Set `CREST_CEILING` to the S2 values outright; do not shift the old ones by
      +45.** The existing Myth entry is **285**, which was never correct (S1 Myth topped
      at **289**) — see † in the 12.1 note above. Also in scope: **re-point the Field
      Accolade consumer**, whose S1 target (Maren's ~259 Hero box) was *removed*, not
      renumbered — value the S2 **Adventurer Warbound (200)** and **Veteran BoP (500
      random / 750 slot-specific)** caches instead, `targeted` only for the 750.
      ⚠ **Also re-point the ritual-site crest tier, which is the same removed-content
      class, not a rebase:** 12.1 realigned Ritual Sites T1–6 to the Season 2 Delve
      tiers, so the T6 **Myth+Hero** payout no longer exists — the activity now yields
      Adventurer/Veteran Mistcrests, and `CURRENCY_CONSUMERS` needs **`veteran_crest`
      and `adventurer_crest` entries it does not have** (today the row values at 0).
      Rebasing the old Myth/Hero payout to S2 numbers would carry a dead reward
      forward. Also stale in the same sweep: the `TRACK_CEILING`/`track_of_ilvl` band
      map already flagged in `_meta/kb-inbox.md`.
- [ ] **🔴 Availability-window gate** (see the Gate section): declare
      `available: {from, until}` on activities and filter on it before scoring, so
      content that has not opened (S2, Aug 18) or has ended (Turbulent Timeways,
      Aug 11) is never rankable. Pre-season 12.1 is the forcing case. ⚠ **One global
      "Season 2 opens" date is not sufficient** — Voidcore bonus rolls open a week
      later (**Aug 25**) *and* require **≥3 vault panes**, so the window must be
      per-activity and must compose with a character-state predicate.
- [ ] **Pre-season Great Vault semantics**: this week `breakpoint_R()`'s 1/4/8
      thresholds accrue toward the *first S2* vault, not a claimable one; and the
      first S2 vault's World row caps at **Champion 3/6** (**Hero 1/6** thereafter).
      Decide whether crossing a threshold for a *next-week* payout still deserves
      R≈4 (probably yes — but the "expires tonight" *why* string is wrong).
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

## Changelog

2026-08-17 — dropped the Voidcore worked illustration of the content-capability gap: 12.1 restructured Voidcores into a Great Vault reward, and the quoted Myth 272 / +10 key figure was never an S1 Myth value.

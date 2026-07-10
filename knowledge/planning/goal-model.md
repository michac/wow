---
title: Session Planning — Goal Model (upgrade-graph, proposed)
patch: 12.0.7
fetched: 2026-07-10
reviewed: 2026-07-10
sources:
  - knowledge/planning/scoring-model.md        # the CURRENT activity-centric scorer this would replace
  - knowledge/planning/redesign-needs-first.md  # the per-slot/currency "needs-first" half-step
  - knowledge/endgame/dawncrests.md             # crest/craft/track upgrade rules
  - knowledge/systems/professions.md            # craft costs (80 Hero → 272, 80 Myth → 285; 2 sparks/piece)
  - knowledge/endgame/catalyst.md               # tier slots can't be crafted; catalyst converts non-tier → tier
confidence: high     # methodology proposal we endorse — NOT a fetched game fact
---

# Session Planning — Goal Model (proposed)

> **STATUS: DESIGN PROPOSAL — not built.** The live planner is the activity-centric
> scorer in `scoring-model.md` (`wowkb.plan`). This doc is the agreed *direction* to
> replace it. Nothing here runs yet. Written 2026-07-10 from a design conversation.

## Why replace the current scorer

The current model is **activity-centric**: each activity carries a `reward_base`, and
character-relative *multipliers* (`slot_target_R`, `currency_R`) nudge it. It answers
"what should I do this session?" by collapsing everything to one number per activity.

That number is a **lossy proxy** for how gearing actually works. When you (or the agent)
reason about upgrades, you don't think in multipliers — you think **per slot**: *this
belt could go crest-to-6/6, or a Hero piece from Maren, or a craft with 80 Hero + 2
sparks, or a catalyzed drop* — then you **pare down by what's in your bags**. That
per-slot candidate list is the real object; the scalar throws its structure away. It
can't natively say "the belt's best move is a craft I'm 8 Hero crests short of," and it
has nowhere to put "which M+ boss drops which slot."

## The model: one pipeline, not two

```
per-slot upgrade CANDIDATES  ──►  GOALS  ──►  rank(value, steps)  ──►  select to time  ──►  TODO steps
   (the upgrade graph)          (pared)      (coarse is fine)        (fit the session)     (= the plan)
```

The session ranking is **not** a separate activity-scorer — it's just ranking the
**goals** that fall out of the graph. There is one system.

1. **Candidates (the upgrade graph).** For every slot, enumerate the upgrade *paths*:
   each `{source, yields:{ilvl, track}, requires:[reagents/crests/access], attainability}`.
   Sources are multi-dimensional (crest-up / craft / catalyst / vendor / each drop
   source), so a slot has several candidates.
2. **Goals.** Pare each slot to its best actionable candidate(s) → a **goal**. Goals
   also include cross-cutting targets that aren't one slot — "cap Champion everywhere →
   the 50% warband discount," "unlock Mythic+" — they enter the same list.
3. **Rank goals** coarsely by **value ÷ effort**, where effort ≈ **how many steps** to
   get there (mats-in-hand = ~0 extra steps; short-but-attainable = the farming steps;
   far-off = many). A one-step "crest the belt, mats in bag" beats a ten-step "farm a
   Hero belt from the vault" of similar ilvl.
4. **Select** the top goals that fit the session's time budget.
5. **Decompose to TODOs.** Multistep goals expand into their steps; that expansion *is*
   the session plan.

### The load-bearing insight: steps are SHARED across goals

"Run 6 delves" advances the belt-crest goal **and** the ring-crest goal **and** vault
progress **and** the coffer — all at once. So when selected goals expand to TODOs, the
steps **dedupe**, and a single step that serves several high-value goals is where the
real session efficiency lives. This is exactly what the old scorer fumbled toward with
"this activity yields crests lots of slots want" — but derived correctly (goals first,
steps pooled) instead of faked with a multiplier.

## Objects (sketch schema)

- **UpgradeCandidate** `{slot, source, yields:{ilvl, track}, requires:{crests, sparks,
  gold, access}, attainability}` — attainability ∈ {`have` (mats in bags now),
  `soon` (short but farmable this reset), `gated` (needs content access / rank / RNG)}.
- **UpgradeSource catalog** — the KB the graph reads (see below).
- **Goal** `{target (slot-upgrade | cross-cutting), value, steps:[Step], enables:[Goal]}`.
- **Step** — a concrete action that maps to an activity (the current `candidates.json`
  becomes the **step library**). Steps carry which goals they advance (via their
  `yields`), so one step attaches to many goals.

## UpgradeSource catalog (what feeds candidates)

Most of these we can already compute from the consolidated character state (real
per-slot track/step, crest + item counts, tier flags — all landed 2026-07-10):

| Source | Fills | Requires | Notes |
|---|---|---|---|
| **Crest-up** (existing piece) | that slot, +steps toward its track ceiling (Champ 263 / Hero 276 / Myth 285) | N crests of its track | deterministic; per-slot |
| **Craft** (spark) | any **non-tier** slot → Hero 272 / Myth 285 | 80 Hero or 80 Myth crests + 2 sparks (4 for 2H) + gold | tier slots excluded (catalyst.md) |
| **Catalyst** | convert a non-tier drop → a **tier** slot | catalyst charge (= *Dawnlight Manaflux*) | the tier-slot path |
| **Vendor — Maren** | a **targeted** slot, Hero ~259 | Field Accolades | you pick the slot (deterministic) |
| **Vendor — Decimus** | bonus-roll (voidcore) | gold + Voidlight Marl + Veteran crests | Myth on a +10 key, else Hero |
| **Vendor — renown** | specific slots (e.g. Hara'ti belt, Silvermoon helm) | renown rank | one-time per slot |
| **Drop — world boss / delve bounty / vault** | random or world-row slot, Hero 259+ | weekly lockout / RNG | `gated`/`soon` |
| **Drop — Mythic+ (per boss) / raid (per boss)** | **specific slots by dungeon/boss**, track by key level | content access + RNG | *the loot-table KB to build when M+ starts* |
| **Ritual sites** | crests + accolades (feeds crest-up/craft/Maren goals) | tier access | a step, not a slot-filler |

**Value** of a goal = the power gain (Δilvl, or the enabling value of a cross-cutting
goal) — plus, for now folded in coarsely, **enabling value**: a goal that makes *other*
goals cheaper (the 50% discount; the M+ unlock that turns banked voidcores Myth and
opens the Myth vault) is worth more than its local ilvl. **Effort** = step count +
attainability. Coarse `value ÷ effort` is the v1 ranking; the enabling/dependency
structure can be made explicit later (goals that `enable` others).

## Worked sketch — Uncomplete (live data, 2026-07-10)

Equipped 251. Crests: Champion 10 · Hero 72 · Myth 20. Sparks 8 · Voidshards 2 ·
Field Accolades 395 · Voidlight Marl 3,399. Cracked Keystone in bags; no M+ yet;
vault dungeon 2/3, raid 1/3.

**Per-slot candidates (a few representative slots):**

- **Waist 246 · Champion 1/6 (non-tier)** — candidates:
  - Maren Hero **259**, targeted → `have` (395 accolades) · **1 step** (buy).
  - Craft Hero **272** → `soon` (needs 80 Hero crests; has 72 — short 8 + 2 sparks ✓).
  - Crest-up current to Champion **263** → `soon` (needs Champion crests; has 10).
  - → **Primary goal:** *Maren belt 259 now* (instantly actionable), with *craft 272*
    as the better target once Hero crests clear 80. (This is the exact "have mats →
    primary, short-but-attainable → strong" reasoning.)
- **Chest 259 · Hero 1/6 (TIER)** — can't craft. Candidates: crest-up toward 276 (Hero
  crests) · catalyze a non-tier Hero drop into the tier chest · vault/raid tier drop.
  → **Primary:** crest-up as Hero crests allow; watch for a tier drop.
- **Main Hand 266 · Hero 3/6** — crest-up to 276 (has crests) · craft (marginal: 272 <
  current-ish) · M+/vault drop. → **Primary:** crest-up.
- **The Champion 1/6 cluster** (head/neck/waist/legs/feet/hands/rings/trinket2/back, all
  246) — each has a crest-up-to-263 candidate; collectively they're the **"cap Champion"**
  cross-cutting goal.

**Pared goal list (ranked, coarse):**

| # | Goal | Value | Steps (effort) |
|---|---|---|---|
| 1 | **Unlock M+** (Cracked Keystone → +2) | high — opens Myth vault, voidcore→Myth, crest farm | 1 (pug a +2; keystone in hand) |
| 2 | **Belt → Maren Hero 259** | med (246→259) | 1 (buy; 395 accolades) |
| 3 | **Cap Champion cluster → ~263** (+ *Champion of the Dawn* on the main → 50% discount) | high (survivability + warband discount) | many (farm Champion crests) |
| 4 | **Crest-up Hero slots** (chest / MH / OH toward 276) | med | many (farm Hero crests) |
| 5 | **Craft belt → Hero 272** | med (beats #2's 259) | soon (8 more Hero crests, then 1 craft) |

**Decompose to TODOs (note the shared steps):**
- *Pug a Mythic +2* → satisfies **#1**, and the run also drops crests/vault credit that
  feed **#3/#4**.
- *Run 6 Bountiful delves* → one step feeding **#3** (Champion crests) **+ #4** (Hero
  crests) **+ #5** (Hero crests toward the 80) **+** vault world column **+** coffer.
- *Buy the belt from Maren* → **#2** (1 step).
- Prey / ritual sites → more crest/accolade flow into **#3/#4/#5**.

The session plan is those deduped steps, ordered — and "run 6 delves" ranks high because
it's **one step under five goals**, which the goal model derives instead of guessing.

## What carries over (this isn't a restart)

- **Substrate already built (2026-07-10):** real per-slot track/step (`track_by_slot`),
  crest + `item_counts` (sparks/voidshards), tier flags, `dawn_achievements`. That's the
  full input the candidate graph needs.
- **`--gear`** is already a half-step toward per-slot candidates — it becomes a *view* of
  the graph.
- **`candidates.json` / `activities/*.md`** don't die — they become the **step library**
  goals decompose onto; their `yields` are how a step attaches to goals.
- The **needs-first** work (per-slot `best_slot_delta`, crest headroom/floor) is the
  per-slot valuation logic the graph reuses.

## Open questions / v1 scope

- **v1 build order:** (a) candidate graph from the deterministic sources we already have
  data for (crest-up, craft, catalyst, Maren, renown) → per-char goal list; (b) goal
  ranking (value ÷ steps); (c) TODO expansion with shared-step dedup off `candidates.json`.
  Drop-source goals (M+/raid/vault loot tables) come later — they need a **loot-table KB**
  (per dungeon/boss → slots/track), a real build to start when M+ begins.
- **Enabling value:** v1 folds it into `value` by hand (mark the discount / M+-unlock
  goals high); a later pass can model `enables` edges explicitly.
- **Where it plugs in:** does `wowkb.plan` grow a `--goals` mode first (read-only goal
  list, no scoring change), then flip the session plan to derive from goals once trusted?
  (Mirrors how the ingest shipped scoring-neutral first.)
- **Supersedes:** on adoption, this replaces `scoring-model.md` as the planner's core;
  keep that doc as the historical activity-centric design.

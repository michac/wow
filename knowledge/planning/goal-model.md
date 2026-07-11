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
2. **Goals.** Pare each slot to **one** goal (its best actionable path); the other
   candidate paths for that slot are ranked *alternatives inside* the goal, **not**
   separate goals — you fill a slot once. Two pare-down rules:
   - **One slot → one goal.** "Belt via Maren 259" and "belt via craft 272" are two paths
     of the *same* goal (upgrade the belt), sequenced/chosen, never both.
   - **Cluster same-path slots.** When many slots share the *same generic* best path
     (e.g. a dozen 246 slots all "crest-up via delves"), they're **one** goal ("cap
     Champion across the board"), not a dozen. A slot earns its *own* goal only when it
     has a **distinctive** path (a tier slot needing catalyst; a slot worth Maren-targeting
     or crafting for a jump). This is the goal-side mirror of shared-step dedup.
   Goals also include cross-cutting targets that aren't one slot — "cap Champion → the
   50% warband discount," "unlock Mythic+" — in the same list.
3. **Rank goals** coarsely by **value ÷ effort**, where effort ≈ **how many steps** to
   get there (mats-in-hand = ~0 extra steps; short-but-attainable = the farming steps;
   far-off = many). A one-step "crest a slot, mats in bag" beats a ten-step "farm a Hero
   piece from the vault" of similar ilvl. (Ranking is **derived**, not hand-ordered.)
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

**Value** of a goal = the power gain (Δilvl) — and, crucially, its **enabling value**.
**Effort** = step count + attainability. Coarse `value ÷ effort` is the v1 ranking.

### Goal gates / dependencies (v1, not "later")

Goals aren't independent — some **gate** others, and this changes sequencing, so it's
core, not a nicety:

- **Hard gate** — B is impossible until A. *Unlock M+* gates *+10 keys* (which gate the
  Myth vault row + voidcore→Myth). You literally can't do B first.
- **Economic gate** — B is possible but **costs more** until A. The big one:
  **"Encomplete earns *Champion of the Dawn*" (263 in every slot → 50% warband-wide
  Champion discount) gates the *cost* of every alt's "cap Champion" goal** — each
  Champion upgrade on Uncomplete/Hallick costs **2× the crests** until it's live. The
  enabler is **cheap** (Encomplete: 2 crest-ups + a belt recraft) and it **halves a big
  recurring warband cost**, so it ranks *ahead* of the alt-capping goals it discounts.
  Efficient play: do the enabler first; **bank** the alt's Champion crests and **hold the
  upgrades** until the discount is live (farming isn't discounted, only spending is).

These edges are **warband-level** — an enabler on one character reweights goals on
others (the "Encomplete-gears-the-alts" synergy). v1 needs at least the economic gate on
the Champion discount and the hard gate on M+; a fuller dependency graph can come later.

## Worked sketch — Uncomplete (live data, 2026-07-10)

Equipped 251. Crests: Champion 10 · Hero 72 · Myth 20. Sparks 8 · Voidshards 2 ·
Field Accolades 395 · Voidlight Marl 3,399. Cracked Keystone in bags; no M+ yet;
vault dungeon 2/3, raid 1/3.

**The slots cluster — most aren't distinctive.** Eleven slots are **246 · Champion 1/6**
(head, neck, waist, legs, feet, hands, both rings, trinket2, back) — same generic best
path (crest-up via delve/M0 crest farm), so they collapse into **one** "cap Champion"
goal, not eleven. (The belt is just a member here — nothing special about it.) Only the
slots with a *distinctive* path split out:

- **Chest 259 · Hero 1/6 (TIER)** — can't craft; path is crest-up toward 276 or a
  catalyzed/vault tier drop. → its own goal (different track + tier handling).
- **Main Hand 266 · Hero 3/6 / Off Hand 269 · Hero 4/6** — Hero crest-up toward 276.
- **A targeted quick win:** Maren sells a **Hero 259** into a slot *you pick* for Field
  Accolades (395 in hand) — so one 246 slot can jump to 259 in a single buy. Which slot?
  the highest-value weak one — *not* inherently the belt.
- **A craft, once affordable:** any non-tier slot → Hero 272 for 80 Hero crests + 2 sparks
  (has 72 crests / 8 sparks → `soon`). Again slot-agnostic: craft whichever non-tier slot
  gains most.

**Pared goal list (ranked coarse by value ÷ steps — illustrative, would be derived):**

| # | Goal | Value | Steps (effort) |
|---|---|---|---|
| **W** | **[Warband] Encomplete → *Champion of the Dawn*** (crest Ring2 + Trinket2 to 263, recraft the belt) ⇒ **50% warband Champion discount** | high — **halves every alt's Champion-cap cost** | few, on Encomplete (2 crest-ups + 1 recraft) |
| 1 | **Unlock M+** (Cracked Keystone → +2) | high — opens Myth vault, voidcore→Myth, crest farm | 1 (pug a +2; keystone in hand) |
| 2 | **Cap Champion cluster → 263** (the eleven 246 slots) — ⚠ **economic-gated on W: farm Champion crests now, but hold the *upgrades* until the discount is live** | high — broad ilvl + survivability | many (farm now; spend after W → half the crests) |
| 3 | **Crest-up the Hero slots** (chest / MH / OH → 276) | med | many (farm Hero crests) |
| 4 | **Maren quick-win**: Hero 259 into the single weakest slot | low-med — one fast jump | 1 (buy; 395 accolades) |
| 5 | **Craft** a non-tier slot → 272, once Hero crests ≥ 80 | med — beats crest-only for that slot | soon (8 more Hero crests, then 1 craft) |

Note **W** outranks **#2** despite being on a *different character* — a cheap enabler that
halves a big downstream cost. This is the warband dependency the flat scorer can't see.

**Decompose to TODOs (note the shared steps):**
- *On Encomplete: crest Ring2 + Trinket2 to 263, recraft the belt* → satisfies **W** →
  unlocks the discount that makes **#2** half price. Do this before bulk-spending on #2.
- *Pug a Mythic +2* → satisfies **#1**; the run also drops crests/vault credit for **#2/#3**.
- *Run 6 Bountiful delves* → one step feeding **#2** (Champion crests — bank them until W)
  **+ #3/#5** (Hero crests, incl. toward the craft's 80) **+** vault world column **+** coffer.
- *Buy a Hero 259 from Maren for your weakest slot* → **#4** (1 step).
- Prey / ritual sites → more crest/accolade flow into **#2/#3/#5**.

The session plan is those deduped steps, ordered — and "run 6 delves" ranks high because
it's **one step under four goals**, which the goal model derives instead of guessing.

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
  ranking (value ÷ steps) **with the two gates wired** (economic: Champion discount; hard:
  M+ unlock) since they change sequencing; (c) TODO expansion with shared-step dedup off
  `candidates.json`. Drop-source goals (M+/raid/vault loot tables) come later — they need a
  **loot-table KB** (per dungeon/boss → slots/track), a real build to start when M+ begins.
- **Gates/enabling — v1, not later** (see "Goal gates" above): at minimum the economic
  Champion-discount gate and the hard M+ gate, including their **cross-character** form
  (an enabler on Encomplete reweighting Uncomplete's goals). A fuller `enables` dependency
  graph (arbitrary edges, auto-derived) can come later, but the planner is wrong without
  these two.
- **Warband scope:** the graph is account-wide — goals live on characters, and some
  characters exist to *enable* others (Encomplete → the alts). v1 needs at least the
  cross-character discount edge; full multi-char orchestration (who farms what for whom)
  is the bigger warband question the old `redesign-needs-first.md` flagged.
- **Where it plugs in:** does `wowkb.plan` grow a `--goals` mode first (read-only goal
  list, no scoring change), then flip the session plan to derive from goals once trusted?
  (Mirrors how the ingest shipped scoring-neutral first.)
- **Supersedes:** on adoption, this replaces `scoring-model.md` as the planner's core;
  keep that doc as the historical activity-centric design.

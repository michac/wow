# Cooldown HUD — field-fixes plan (what the first live session found)

> **STATUS: ✅ DONE — shipped, flown, and closed out (2026-07-30, v0.32.28–31).** All four
> phases implemented, gated, and validated against a live Hellcaller dummy pull. The pass
> confirmed A/B/C, exposed two further defects that are also fixed (a same-frame refresh tie,
> v0.32.30; charged-ability readiness, v0.32.31), and answered the Incinerate question. See
> *The live pass* below. **This document is now history — nothing here is outstanding.**
> The one thing it did NOT prove is called out there (the charge napkin's estimate path is
> receiving events but has still never changed a decision), and the work it promoted is the
> **virtual CDM panel** (`virtual-cdm-plan.md`), not anything in this plan. Written 2026-07-30 after the **first session in which the HUD actually
> rendered** (the v0.32.25 outage fix) and the **first in-client alert capture**
> (v0.32.26/27). Both produced findings that invalidate parts of the shipped Destruction
> brain. **What is owed is the live confirmation** — see *Verification* at the bottom; the
> pass/fail signal is sharp (216 `SF:ROT×` today → **0** dropped cues, and `Imm` appearing
> as a winner at least once).
>
> **Doc map:** the rotation of record is `specs/destruction/rotation.md`; the pipeline is
> `architecture.md`; the live worklist is `status.md` (this plan is its Active-work item).
> The alert-channel facts this plan builds on are in
> `knowledge/addon-dev/api-events-and-discovery.md` §2.8 — **confirmed in-client**, not
> desk-derived.

---

## Why — the field session invalidated four assumptions

| Assumption | What actually happened |
|---|---|
| The tracked set from DB2 ≈ what loads | **Incinerate has no CDM icon at all.** The live Essential set is 9 entries; Incinerate, Soul Fire, Havoc and Channel Demonfire are absent. |
| `state.abilities` holds pressable abilities | It holds the **enumerated DB set** (`allowUnlearned = true`). Untalented spells read `ready` forever and win the rotation. **216 dropped Soul Fire cues** in one session. |
| Immolate is keyed on the DoT aura `157736` | The **pressable** row is `348`; `157736` lives on the Buff-bar viewer and never enters `abilities[]`. So L8 can never fire. |
| A tracked Wither means Hellcaller | A live Hellcaller build tracked **Malevolence but Immolate**. The inference picked Diabolist. |

Plus one capability gain the capture handed us: **the alert channel carries more than we
consume.** `PandemicTime` and `ChargeGained` both fire in combat, on the choke point State
already hooks — while the corresponding *state* reads are secret.

## Decisions locked before starting

1. **Filter in `State`, not in the Coach.** `abilities` is documented as "the PRESSABLE
   representative row"; an ability with no icon is not pressable. Filtering there fixes both
   specs at once and needs no spec/Coach edits.
2. **`displayable` is the primary gate, `isKnown` the secondary.** `isKnown` alone does not
   cover Incinerate (known, but untracked by the layout). Gating on "can the Binder draw
   it?" covers both causes.
3. **Dropped rows are logged, never silent.** A filter that silently removes a real ability
   would be the same class of bug as the nil-guard outage. The decision log records what was
   dropped and why.
4. **The state is secret; the edge is not.** Pandemic and charges are both solved as
   **edge latches over a seeded baseline**, never as state polls. `IsInPandemicTime` throws,
   and `GetSpellCharges` is secret — measured, not assumed.
5. **The napkin honesty rule extends to charges.** Overcount claims a charge you do not
   have; undercount only under-presses. Bias to undercount, clamp to `[0, max]`, and let an
   exact OOC read always win.
6. **No rotation re-shaping in this plan.** The `hero × mode` four-list split is real work
   and is **backlogged separately** — four lists are worthless while phantom abilities win
   and the DoT line cannot fire.

---

## Phases

Existing gates are the regression net: **luacheck clean + 209 busted tests**, which must
stay green throughout. One release at the end of C2.

| Phase | Work | Gate |
|---|---|---|
| **A** | **Stop phantom abilities winning.** In `State.Build`'s domain-view fold, mark each row `displayable` (an item frame exists in `itemFrameMap()`) and carry `isKnown`; filter `abilities` on them. Raw `cooldowns` keeps everything (it is the diagnostic view). Record drops in the decision log. | New `state_domainview_spec`: an unknown row and an undisplayable row never reach `abilities`; the raw view still has both. A Coach test proves the winner falls through to the next line instead of vanishing. 209 stay green. |
| **B** | **Fix identity.** (1) `ctx.dotID` resolves to whichever id is actually in `ctx.facts` — Wither → Immolate-aura `157736` → Immolate-cast `348`. (2) Hero detection: try a real API (`C_ClassTalents` / `TraitSubTree`) first; fall back to **multi-signal** inference (Malevolence **or** Wither ⇒ Hellcaller; Ruination / Infernal Bolt / Diabolic Ritual ⇒ Diabolist), ambiguity defaults to Diabolist **and says so in the log**. | `coach_destruction_apl_spec` gains the **live configuration as a fixture** (Malevolence + Immolate-as-`348`): asserts hero = Hellcaller and L8 targets `348`. |
| **C** | **Pandemic edge latch.** State grows `dotEdge` beside `readyEdge`, fed by the alert hook that already sees all six types: `PandemicTime` ⇒ latch set, `OnAuraRemoved` ⇒ cleared+absent, `OnAuraApplied` ⇒ cleared+fresh. Surfaced on the domain-view row so the brain reads `ctx.dotRefreshable` and never sees a cooldownID. **Delete** `DOT_REFRESH_LEAD` and the speculative `uptime` read. | ⚠ The latch keys on **cooldownID**, and Immolate has **two** (`133441` aura + `164597` cast) that BOTH fired `PandemicTime` — either must set one latch on one base spellID. Spec covers the two-cid case. |
| **C2** | **Charge napkin** — same seam. Seed exact from `ReadCharges` OOC; `−1` on `UNIT_SPELLCAST_SUCCEEDED`; `+1` on `ChargeGained` (which also captures **cooldown-reset procs**, since it fires on any upward move of Blizzard's cached count); clamp `[0,max]`; exact re-read wins OOC. Surfaced as `charge.cur` with `source = "napkin"` so the brain can tell an estimate from a measurement. | Spec drives the full loop off synthetic pulses incl. clamping and the OOC re-seed. Only Conflagrate consumes it today — Shadowburn has **no charges** (DB2 `ChargeCategory = 0`). |

## What shipped (2026-07-30) — and where it deviated from the plan

All four phases landed, released as **v0.32.28** (+ **v0.32.29**, a review follow-up) and
deployed. Gates: **luacheck clean, 268 busted** (209 baseline + 59 new), and every phase
mutation-checked. Commits: the State half (A + the C/C2 stores, which share one file), the
Coach half (B + the C/C2 consumers), a docs/data correction, and the review follow-up.

**Things the plan did not anticipate, in rough order of how much they mattered:**

1. **`isKnown` could never read `false`.** It was built as
   `info and (info.isKnown and true or false) or nil` — a Lua and/or trap whose *false*
   middle term falls straight through to the `or nil`. So the field only ever held `true` or
   `nil`, and Phase A's secondary signal was inert. It shipped that way since W4 Phase 1 and
   nothing noticed, because the field had **no consumer** until this plan gave it one. Now
   built with an `if`, and the three values are load-bearing: `false` = unlearned (a drop),
   `nil` = unreadable (never a drop).
2. **An empty frame map must not filter.** Not in the plan, and it is the highest-blast-
   radius line in the change: if the viewers are not up (login, CDM off, relayout mid-pulse),
   `itemFrameMap()` is empty and gating on it would empty `abilities` outright — the exact
   shape of the v0.32.25 total outage. The displayable filter is skipped wholesale when the
   map is empty. **This was the mutation that first got away** (see below).
3. **`dotEdges` needed to be a pulse-level map, not only a row field.** The plan said "surface
   it on the domain-view row". That is necessary but not sufficient: Immolate's *aura* row
   (`157736`, Buff-bar) raises `PandemicTime` and **never enters `abilities`**, so a row-only
   surface would lose half the signal. State carries `pulse.dotEdges` (base-spellID keyed) as
   well, and the Coach folds across the DoT's candidate ids, newest edge wins.
4. **The latch has to OUTRANK the aura read**, not merely supplement it. The latch is the
   only channel that works in combat; when the two disagree there, the observed edge wins,
   because the alternative is trusting a read that has gone dark.
5. **C2 needed a Coach edit after all.** `chargeBanked()` short-circuited on
   `ch.readable == false`, which is exactly what an estimate reports — so the napkin would
   have been computed and then ignored. It now reads `cur` whatever the source and leans on
   the undercount fence; an *absent* count is still not a press.
6. **Hero-cache invalidation wanted a generic seam.** `SpecRegistry` grew
   `ns.InvalidateSpecCaches()` (drops every registered spec's cache, not just the active one,
   so swapping away and back cannot resurrect a stale answer) and a **`TRAIT_CONFIG_UPDATED`
   registration** — the event that actually fires for a hero swap, since changing hero tree
   does not change the spec.
7. **Only the API answer is cached.** The multi-signal inference is re-run every pulse: it
   reads the tracked set, which is empty on the first pulses after a login, so caching it
   there would freeze the wrong answer for the session — the very failure being fixed.
8. **A wrong `charges` fact fell out of the review.** `SpecDestruction` gave Shadowburn
   `charges = 2` and three docs called it the project's second charged tracked ability. DB2 @
   12.0.7 disagrees — `SpellCategories.ChargeCategory` is **0** for Shadowburn `17877` (and
   Chaos Bolt), against Conflagrate `17962`'s **672** — and the live capture agrees, since
   Conflagrate raised `ChargeGained` and Shadowburn never did. Conflagrate is the only
   charged ability, and therefore C2's only consumer. Corrected in the data and the docs.
9. **Two cheap-shot bug classes caught on review, both the same shape as the ones being
   fixed:** the hero chat line re-printed on every `TRAIT_CONFIG_UPDATED` re-fire (the latch
   now survives cache invalidation, so it announces real *changes*), and the DoT candidate
   list was a value literal — `{ S.WITHER, S.IMMOLATE, S.IMMOLATE_CAST }` has a **hole** if
   any id is nil, and `ipairs` stops at the first hole, so one missing constant would have
   silently dropped every candidate after it. Keyed by name now.

**Harness/config changes:** `mock_ns` gained the real `Enum.CooldownViewerAlertEventType`
values and `ns.Print`/`Printf` (provided by the harness rather than nil-guarded at the call
site — guarding our own symbols is the idiom that caused the outage); `C_ClassTalents` went
into `.luacheckrc`'s std per the curate-the-config doctrine.

### Mutation checks (the `viewers_spec` discipline)

Eight mutations run; **six went red immediately, two did not** — and the two that survived
were real coverage holes, both now closed:

| Mutation | Result |
|---|---|
| A: filter disabled entirely | ✅ red |
| A: `displayable` signal removed (isKnown only) | ✅ red |
| A: empty-frame-map safety removed | ❌ **green** → added a Build-level test (a pure-function test of the flag proves nothing about how `Build` computes it) |
| B: `dotID` back to the `157736` constant | ✅ red (6 failures) |
| B: hero back to the single-signal inference | ✅ red |
| C: latch never records | ✅ red |
| C: Coach ignores `dotEdges` | ✅ red |
| C: first edge wins instead of newest | ❌ **green** → added a both-ids-latched-at-different-times test |
| C2: brain refuses the napkin estimate | ❌ **green** → added an in-combat banked-charge test |

## The live pass (2026-07-30, v0.32.29, Hellcaller, ~190 s dummy pull)

Both instruments extracted: `wowkb.cdmp decisionlog` (194 lines / 3 sessions) and
`wowkb.cdmp alerttape`. The capture spans the OLD build (v0.32.27, 10:38) and the fixed one
(v0.32.29, 13:29), which makes it a genuine before/after rather than an assertion.

**A — phantom abilities: ✅ FIXED, and the bug is on tape.** The two `×` (Binder-dropped cue)
lines in the whole capture are both in the **v0.32.27** session and both read `SF:ROT×` — the
phantom Soul Fire winning the list, caught in the act. The v0.32.29 sessions have **zero
`×`**. The tracked set went from 12 codes to 8; the four that left are exactly what the new
`DR:` field reports, and the drop list is stable (one distinct `DR:` string across 191
lines). Every drop checks out by name — Soul Fire, Havoc and Channel Demonfire untalented;
Shadow Bolt (`686`), Nether Ward, Shadow Rift, Bonds of Fel, Soul Rip, Howl of Terror and a
second Rain of Fire id unlearned; Blight of Tongues and Demonic Circle: Teleport `no-icon`
(owned, just not on the player's CDM layout). **Nothing real was removed.**

**B + C — the DoT line: ✅ FIRES, for the first time ever.** Five wins, all carrying the note
`pandemic_refresh`. Both halves are load-bearing and both are visible in the tape:
- The Essential row is `cid 164597 → spellID 348`. `factsByBase` therefore has no `445468`
  and no `157736`, so the OLD `dotID` resolution landed on `157736` and `key()` yielded nil —
  **L8 could not fire, confirmed by construction.** The candidate walk lands on `348`.
- **Both** Immolate cooldownIDs raised `PandemicTime` at the *identical* timestamp
  (`133441` and `164597`, both `131182.959`) — exactly the two-cid case C was designed for —
  and the fold resolved them to one answer.
- The cue held ~1.65 s and stopped, matching `OnAuraRemoved`/`OnAuraApplied` at
  `131184.611`. The mechanism works end to end.
- `FLD` rows re-confirm the premise on this build: `pStart=SECRET pEnd=SECRET isIn=threw`.
  Deleting `DOT_REFRESH_LEAD` was correct — there was never going to be a number.

⚠ It renders as **`Wth`, not `Imm`**, and that is right: Wither *replaces* Immolate on the
button for Hellcaller, so the row's `liveSpellID` is `445468` while its base stays `348`. The
plan's "`Imm` must appear as a winner" acceptance test was written for a Diabolist build.

**C2 — charges: the pull found a REAL BUG, and it was not in the napkin (fixed in
v0.32.31).** Conflagrate was recommended at **zero charges** with seconds left on the
recharge — the unsafe direction the honesty rule exists to prevent. The napkin was innocent;
the readiness model was wrong:
- **A charged ability never raises `OnCooldown`.** `cid 18860` advertises
  `Available, OnCooldown, ChargeGained` and raised **`Available` ×7, `OnCooldown` ×0**,
  while four non-charged entries in the same capture raised `OnCooldown` normally.
  `Available` fires **once per charge restored**. So the ready-edge latches true on the
  first charge and is never cleared — `Conf=R` on 190 of 194 lines — and `usable()`
  short-circuited on `probablyUp` before ever consulting charges.
- **The napkin could not rescue it.** Conflagrate's `RecoveryTime` is **0** in DB2 (the
  recharge lives on `ChargeCategory 672`), so `GetSpellBaseCooldown` gives nothing to count
  down and the just-cast guard never fires.
- **Fix:** when we have a count for a charge pool, it **decides**; only a total absence of a
  count falls back to the cooldown read. The struct's `charges` flag no longer gates the
  read either — that made the whole napkin depend on one flag being right *with no symptom*
  if it was not. `charged` is now measured (a live `max > 1`).
- **The instrument was blind, which is its own defect.** The trace could not show this at
  all; every line just said `Conf=R`. The log gained a **`CH:`** field (`Conf=1/2` exact,
  `Conf~1/2` napkin). *(Generalised into `knowledge/addon-dev/api-events-and-discovery.md`
  §2.8 — it is a client fact, not a Destruction fact.)*

**C2 — the napkin itself: wired and receiving, still NOT exercised.** `ChargeGained` fired **11× in
combat** on Conflagrate (`cid 18860`), so the channel is live and the hook sees it. But
Conflagrate read `R` on 190 of 194 lines — it was essentially never in the "on cooldown with
a charge banked" state the napkin exists for, so it never changed a decision. **Not
confirmed; needs a pull that actually drains both charges.**

**A bug the capture exposed (fixed in v0.32.30).** A DoT *refresh* raises `OnAuraRemoved`
**and** `OnAuraApplied` with the identical timestamp. Last-write-wins meant Blizzard's
dispatch order decided whether the HUD thought the DoT was up or gone. It landed the right
way round in this capture — which is why it was worth pinning rather than leaving to luck. A
re-application now supersedes the removal it replaces.

### What the pass did NOT settle

1. **31 % of decisions have no winner.** 59 of 191 lines are `w:-`, every one of them at
   **0–2 shards** — the untracked-Incinerate hole, exactly as predicted. Below Chaos Bolt's
   2-shard cost there is no floor press, so the HUD goes blank for roughly a third of the
   pull. Correct behaviour, bad experience: this is the strongest possible argument for the
   **artificial CDM icons** backlog item, which is now the single highest-value open work.
2. ~~**Incinerate's enumeration is an open discrepancy.**~~ ✅ **SOLVED** — and the answer
   matters for the artificial-icons work. A fresh `CooldownSetSpell` pull (the cached copy
   was an unpinned older fetch, so it was re-fetched before trusting) shows **Incinerate
   `29722` is not in the table at all**, for any cooldown set. What *is* in Destruction's
   set 884 at OrderIndex 0 is **Shadow Bolt `686`, `cid 66181`, Essential** — and the client
   overrides that entry's display to Incinerate for a Destruction warlock, which is why the
   Cooldown Settings panel shows an **Incinerate tooltip on a greyed icon**, and why the old
   pre-filter session listed `Inc` in `tracked:` (its `liveSpellID` resolved to `29722`,
   while its base stayed `686`). The entry reads `isKnown = false` — hence
   **`686:unlearned`** in `DR:`, hence greyed, hence no frame is ever created, hence "even if
   I add it to my list it's never displayed".
   - So the user's hypothesis was right in shape: the filler *is* reached through another
     spell's CDM slot. The mechanism is an **override on the Shadow Bolt entry**, not a
     talent promoting Incinerate.
   - **`cid 66181` is therefore the handle** the artificial-icons item should use — it is a
     real cooldownID whose live identity already resolves to Incinerate. That is a much
     better starting point than synthesising an entry from nothing.
   - ⚠ **Open question it raises for the filter:** should a row whose *base* is unlearned but
     whose *live override* is a known, pressable spell be dropped? Today it is dropped twice
     over (`unlearned` and no frame), so nothing changes — but the reason we report is
     arguably the less useful of the two.
3. **Hero detection reported `hellcaller`, which is correct** — but the pull could not
   *discriminate*: Wither is tracked on this build, so the old single-signal inference would
   have answered Hellcaller too. Proving the API path beats the inference needs a build where
   the two disagree (the original failing configuration).

## Risks, and what makes each safe

- **A drops a real ability.** The whole point is removing rows, so a wrong signal removes a
  real button. Mitigated by gating primarily on `displayable` (a frame either exists or it
  does not — no inference), and by logging every drop so it is visible on the next capture
  rather than silent.
- **B's hero API may not exist.** If there is no clean read, the multi-signal fallback is
  strictly better than today's single-signal inference, which has already been observed
  failing. Ambiguity resolves to Diabolist (the KB's default profile) and is logged.
- **C latches stale.** A DoT ticking on a target that died, or a target swap, could leave
  the latch set. `OnAuraRemoved` should cover it; if not, the latch needs a target-change
  reset — which is the first thing to check on the next capture.
- **C2 drifts.** Every napkin drifts; this one is fenced so drift can only *under*-press,
  and it re-seeds exactly on every combat exit.

## Out of scope — backlogged in `status.md`

- **`hero × mode` four-list rotation split** (the real rotation work; do it after this).
- **Artificial CDM icons** — a HUD-owned panel for Incinerate / Shadow Bolt, which is the
  actual fix for "the floor press has no icon". Phase A only stops it corrupting the
  *decision*; it does not make Incinerate visible.
- **Branch fallback** — "we cannot decide, because X" instead of always offering a runner-up.
- **Command consolidation** — one sectioned `/cdmp dump` behind a section registry.

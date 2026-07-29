# W4 Phase 7 — the cooldown-state model redesign (3 states + real edges)

*(Dated 2026-07-27. A fresh-context handoff + build plan. Read this top-to-bottom in a fresh
context; it is self-contained. It plans **option (b)**: collapse State's 4-value cooldown model
to **3 honest states** and make in-combat readiness **observed, not guessed**, by subscribing
State to the Cooldown Manager's alert edges. Supersedes nothing already shipped — it refactors
the `cd` contract the whole pipeline reads.)*

---

## 0. The overall project (context for a fresh reader)

**Cooldown HUD** is a spec-specific overlay (v1: **Demonology Warlock**, Midnight 12.0) that
skins Blizzard's built-in **Cooldown Manager** (CDM). It's a standalone companion app beside
the WoW knowledge base, not part of the KB. The addon is **CDMProbe** (`michac/CDMProbe`), a
**separate gitignored git root** at `projects/cooldown-hud/addon/`; goldens, docs, and tools
live in the parent wow repo. Design docs live in `projects/cooldown-hud/docs/` (start at that
folder's `CLAUDE.md` doc-map). Current released addon version: run `wowkb.addon list` (as of
this doc, **v0.32.3**).

**The W4 pipeline.** The guidance engine is a testable, spec-agnostic pipeline:

```
State → Coach → Guidance → Binder → DrawList → Renderer   (docs/architecture.md)
```

- **`State.lua`** (pipeline Stage 1) is the ONE stage that touches the game API. It distills
  the client into a spec-agnostic **pulse** table: cooldowns, power, auras, cast history. It
  decides no cue and knows no rotation (invariant #3, enforced by `wowkb.cdmp`'s statelog
  denylist). It DOES consult a few injected `ns.Spec*` readers (base cooldowns, signed shard
  deltas) — game-fact inputs, not rotation logic.
- **`Coach.lua`** (Stage 2) is a pure `Compute(state) → Guidance` ranked cascade: exactly one
  top press. Arbitrated **off-game** against `corpus/goldens/*` — each golden is a hand-authored
  `state.json` (a pulse) + an oracle `guidance.json`, reasoned from
  `knowledge/classes/warlock/demonology/{rotation,diabolist-sequences}.md`, never from code.
- The gate is `busted CDMProbe/tests/spec` (+ `luacheck`, + a luaparser syntax check on
  release). Live behind `/cdmp hud2`.

**The napkin (`HudNapkin.lua`).** The only DRIFTING input in the design. When the client won't
report a live cooldown (in combat — see below), the napkin supplies an ESTIMATE from the last
observed cast + the base cooldown length. It is fenced by an **honesty rule**: an observed
ready edge always wins, and an expired estimate says "should be up, unconfirmed" — it never
promotes itself to a hard "ready."

---

## 1. How we got here (the road to this redesign)

1. **W4 Phase 6 — the TCT redesign** (`docs/w4-phase6-tct-redesign.md`). In-game testing of
   v0.32.2 surfaced two Coach bugs (HoG not clearing mid-cast; a wrong opener). The fix unified
   the four burst phases into one **Tyrant Condition (TCT)** walk and made all shard reads
   **projected** (value + signed incoming). Shipped as **Part 1** (Coach + goldens) and
   **Part 2** (`State.lua` signed `incoming` so an in-flight Hand of Gul'dan projects −3 and
   clears itself). Released as **v0.32.3**.

2. **A new in-game bug (the trigger for THIS doc).** At ~5s into a fresh pull, with **Summon
   Demonic Tyrant off cooldown AND Call Dreadstalkers off cooldown**, the overlay recommended
   **Summon Tyrant** instead of staging **Dreadstalkers** first — and just before that, during a
   Demonbolt cast, it recommended **Hand of Gul'dan**. The burst walk is supposed to go
   `cap shards → Dreadstalkers → Grimoire → Summon Tyrant`.

3. **First (wrong) diagnosis — a Coach special-case.** The burst walk's "never cast this pull =
   available" rule (`cdSource == "none"`) was applied only to **Tyrant** (`Coach.lua:284`), not
   to Dreadstalkers/Grimoire (`:299`/`:303`). So at pull start Dreadstalkers read not-up and the
   walk skipped to Tyrant. A tempting fix was to extend the special-case to the other summons.

4. **The RIGHT diagnosis — a State bug (the user's call).** *Out of combat nothing is secret*,
   so State can read **precise** cooldowns from the API. We should therefore have **more**
   information at a pull's start than the napkin's guesswork, not less. The real defect: State
   reads the true cooldown OOC but **throws that truth away on combat entry**, so a never-cast
   ability collapses to `source: none` ("no data") the instant combat hides it — even though we
   knew seconds earlier that it was ready. The Coach was being asked to paper over a State that
   had *dropped* information it genuinely had. Fix belongs in State, not the Coach.

5. **The mechanism, confirmed in code:**
   - `ns.ReadCooldown` (`Util.lua:219`) hard-returns `nil` in combat (`if InCombatLockdown()
     then return nil end`, `:226`). So `readCd` (`State.lua:166`) can only use the napkin in
     combat.
   - The old HUD's OOC seeding (`HudState.SeedFromReads`, `:848`) **clears** the napkin for a
     *ready* ability (`HudNapkin.Clear`, `:874`) and records readiness only in the old HUD's own
     `S.readyAt`/`HudChrome` — structures `State.lua` deliberately does not read (clean-room
     separation). It seeds the napkin only for *cooling* abilities (`:881`). So **cooling
     survives combat entry; ready does not** → `source: none`.

6. **The discovery that reframes everything — the edges already exist.** The reason the napkin
   has to *guess* the ready moment in combat is stated in `State.lua:471` as "a later alert-hook
   upgrade." But the upgrade is already built and proven — just not wired into State:
   - `Enum.CooldownViewerAlertEventType.Available` (**ready rising** edge, "cooldown finished")
     and `.OnCooldown` (**ready falling** edge, "went on cooldown"), captured via
     `hooksecurefunc(item, "TriggerAlertEvent", …)` on each CDM item (`HudState.lua:688–758`).
   - These **fire in combat** — they come off the item's own alert choke point, not a
     secret-guarded API read. The **old HUD consumes them** (`S.readyAt`,
     `HudNapkin.Available/Clear`). The **new `State.lua` never subscribes** — it registers only
     `UNIT_SPELLCAST_START/SUCCEEDED` (the *into*-cooldown edge, via your own cast) and, since
     Phase 6 Part 2, the terminal cast events. It has **no ready-edge subscription at all**.

   So "in-combat readiness, determined without guessing" is not aspirational — it is *port the
   alert hook into State*.

7. **Which exposes the deeper question (the user's, that this doc answers):** the current 4-value
   cooldown model over-models a distinction the edges + `source` already carry. See §2.

---

## 2. The current `cd` model and why it's over-modeled

`readCd(live, base)` returns a fresh `cd` table each pulse (then `stampCd` adds `changedAt`):

| field | type | domain |
|---|---|---|
| `state` | string | `ready` \| `cooling` \| `anticipated` \| `unknown` |
| `remaining` | number / `"<secret>"` | present on ready(0)/cooling/anticipated; absent on unknown |
| `readable` | bool | live API read (true) vs derived/absent (false) |
| `source` | string | `live` \| `napkin` \| `none` |
| `changedAt` | number | GetTime() when `state` last flipped (added by `stampCd`) |

The five concrete returns today:

```lua
{ state="ready",       remaining=0,     readable=true,  source="live"   }  -- OOC ready
{ state="cooling",     remaining=<sec>, readable=true,  source="live"   }  -- OOC on cd
{ state="anticipated", remaining=<sec>, readable=false, source="napkin" }  -- combat, napkin countdown
{ state="unknown",                      readable=false, source="napkin" }  -- combat, napkin elapsed
{ state="unknown",                      readable=false, source="none"   }  -- nothing known  (THE BUG lands here)
```

**Why this is redundant (the three "why"s that motivated Phase 7):**

- **`cooling` vs `anticipated`** encode only *"is `remaining` precise or an estimate?"* — which
  `source` (`live`/`napkin`) + `readable` already carry. The state split adds nothing.
- **napkin-elapsed → `unknown`** is the honesty rule wearing an ambiguous label: "don't assert
  ready from a drifting estimate." A cleaner encoding is "still **on cooldown**, estimate
  exhausted, unconfirmed" — positive, not mushy.
- **there is no `probablyUp` state** — it's a Coach-derived flag (`napkinProbablyUp =
  state=="unknown" && source=="napkin"`, `Coach.lua:201`) born from overloading `unknown`.

**Coach consumers of the current model** (`Coach.lua` Classify, `:201–206`):

```lua
rec.napkinProbablyUp = (c.state == "unknown" and c.source == "napkin")   -- "probably up"
rec.anticipated      = (c.state == "anticipated")
rec.remaining        = num(c.remaining)
rec.cooling          = (c.state == "cooling")
rec.cdSource         = c.source
```
plus the Tyrant-only special-case `ctx.tyrantProbablyUp = ty.napkinProbablyUp or ty.cdSource ==
"none"` (`:284`) and the SOON-lead reads (`ctx.tyrantAnticipated`/`tyrantRemaining`, `:285–286`).

---

## 3. The target model (Phase 7)

**Three states. `source` becomes a trust annotation on `remaining`, not a second state axis.
Readiness is OBSERVED (OOC read + alert edges), estimated only for the *remaining seconds* while
on cooldown.**

| `state` | how State knows it — WITHOUT guessing | `remaining` | `source` |
|---|---|---|---|
| **`ready`** | OOC baseline read == ready, **or** an observed `Available` edge — and no cast / `OnCooldown` since | `0` | `live` (a read or an edge) |
| **`on-cooldown`** | OOC baseline == cooling, **or** an observed `OnCooldown`/`SUCCEEDED` | precise while OOC-readable; napkin estimate in combat; **`0` when the estimate has run out but no `Available` edge yet** ("napkin says zero, unconfirmed") | `live` when the number is a read; `napkin` when it's an estimate |
| **`unknown`** | no baseline **and** never observed | absent | `none` |

Notes:
- **`ready` is honest in combat** because it rests on observed truth: the OOC baseline (no cast
  since) or an `Available` edge — never on a bare estimate. The only fuzzy moment left is the gap
  between an `OnCooldown` edge and the next `Available` where the estimate has hit zero; the model
  names that **`on-cooldown, remaining 0, source napkin`**, not `ready`. The Coach decides whether
  that's recommendable (it is — "probably up"), as a *derivation*, not a laundered state.
- **`source` no longer distinguishes states.** `on-cooldown/source:live` (precise OOC remaining)
  and `on-cooldown/source:napkin` (estimate) are the same state with different trust — exactly
  what `source` is for.
- **The Tyrant `source=="none"` special-case disappears.** A never-cast Tyrant now reads `ready`
  from the baseline, like every other never-cast summon; the Coach needs no per-ability carve-out.

**Derivations the Coach computes (replacing the old flags):**
```lua
rec.ready        = (c.state == "ready")
rec.onCd         = (c.state == "on-cooldown")
rec.remaining    = num(c.remaining)
-- "probably up" = ready, OR on-cooldown with the estimate exhausted:
rec.probablyUp   = rec.ready or (rec.onCd and c.source == "napkin" and (rec.remaining or 0) <= 0)
-- SOON lead: on-cooldown with a positive remaining within the lead window
rec.anticipated  = rec.onCd and (rec.remaining or 0) > 0
```

---

## 4. Build plan (option b)

Bottom-up: land State first (it produces the new contract), re-encode the goldens to the new
contract, then simplify the Coach to consume it, verifying the gate green at each seam. Every
change is off-game-testable except the alert-hook wiring (live-only, like all of State).

### Phase 7a — State: the OOC-readiness baseline (no new events yet)
The minimal information-preserving fix, as a foundation.
- In `readCd`, on every live (OOC) read, stash a module-local `cdBaseline[base] = { ready,
  duration, startTime, at }`. (`ns.ReadCooldown` already returns `duration`/`startTime`; `readCd`
  currently discards them — capture them here.)
- Add a combat fall-through **after** the napkin miss and **before** `source:"none"`: project the
  baseline forward — `ready` baseline (no napkin estimate = not cast since) → still `ready`;
  `cooling` baseline → `remaining = startTime + duration - now`, `on-cooldown` (or `ready` when
  elapsed). Emit it under the NEW 3-state contract (see 7c) — or, if landing 7a alone first,
  under the existing enum as `{state=unknown, source=napkin}` so it flows through the Coach's
  current `napkinProbablyUp` with no Coach change. **Recommendation: land 7a directly in the new
  contract as part of 7c to avoid encoding it twice.**
- **This alone fixes the Dreadstalkers-at-pull-start bug** (a never-cast summon reads ready/
  probably-up instead of `none`).

### Phase 7b — State: subscribe to the CDM alert edges (readiness becomes observed)
- Port the alert-hook pattern from `HudState.lua:688–758` into State's own event layer
  (clean-room — State must not read the old HUD's `S.readyAt`): `hooksecurefunc(item,
  "TriggerAlertEvent", …)` per CDM item, keyed by `cooldownID`, handling
  `Enum.CooldownViewerAlertEventType.Available` (→ ready) and `.OnCooldown` (→ on-cooldown).
  Re-hook on `RefreshLayout` / `COOLDOWN_VIEWER_DATA_LOADED` like the layout binding does.
- Maintain a State-owned `readyEdge[cooldownID/base]` truth: `Available` → ready-at now;
  `OnCooldown`/observed `SUCCEEDED` → on-cooldown-at now. `readCd`'s combat path consults this
  FIRST (observed edge = ground truth), then the napkin (for the *remaining* estimate only), then
  the OOC baseline, then `unknown`.
- Guard secrecy: an alert whose spellID reads secret is dropped, not assumed (same discipline as
  the existing readers).

### Phase 7c — the contract flip: `{ready, cooling, anticipated, unknown}` → `{ready, on-cooldown, unknown}`
- `readCd` emits the 3-state table (§3). `source` = trust annotation; `remaining` always
  meaningful on `on-cooldown`.
- Update `probe-baseline.json`'s `statelog-enum-domain` check to the new `state` domain (and keep
  `source ∈ {live, napkin, none}`).

### Phase 7d — Coach `Classify` simplification
- Replace `napkinProbablyUp`/`anticipated`/`cooling` (`Coach.lua:201–206`) with the §3
  derivations. Point `ctx.dreadProbablyUp`/`grimoireProbablyUp`/`tyrantProbablyUp` at
  `rec.probablyUp`. **Delete the Tyrant `cdSource == "none"` special-case** (`:284`) — the
  baseline makes never-cast read `ready`. Keep the SOON-lead reads on `rec.anticipated` +
  `rec.remaining`.
- No change to the burst walk's ORDER or to any RankWinner/Emit logic — only the availability
  inputs change.

### Phase 7e — goldens: re-encode all 30 to the new contract
- Mechanically rewrite every `cd` block: `cooling → on-cooldown` (keep `remaining`, `source`);
  `anticipated → on-cooldown` (`source: napkin`, positive `remaining`); napkin-elapsed `unknown/
  napkin → on-cooldown` with `remaining: 0`, `source: napkin`; true-nothing `unknown/none`
  stays `unknown`.
- **Add the pull-start goldens this whole investigation was missing** (they now read *right*
  because State supplies the truth):
  - `tyrant-pullstart-dread` — combat ~3s, 5 shards capped, Tyrant + Dreadstalkers + Grimoire all
    **ready** (baseline, never cast) → oracle **Dreadstalkers ROTATION + Tyrant SOON**.
  - `tyrant-pullstart-dbcast` — mid-Demonbolt-cast, incoming +2 → projected cap, Tyrant ~2s
    (`on-cooldown` remaining 2), demons **ready** → oracle **Dreadstalkers ROTATION + Tyrant
    SOON** (NOT HoG).
  - `ready-edge-observed` — combat, a summon flipped to `ready` via an observed `Available` edge
    (`source: live` in combat) → it's a hard press, not a napkin guess.
  These are the fix-validation pins; add them to `SCENARIOS` and `coverage.md`.
- Update `coverage.md` (state-domain table, the new scenarios, the sign/edge coverage notes).

### Phase 7f — verify + release
- **Off-game:** `luacheck CDMProbe/` clean · `busted CDMProbe/tests/spec` green (30 + 3 new =
  33 goldens, plus the unit specs) · luaparser OK.
- **State contract** (`wowkb.cdmp`): add/repoint assertions in `probe-baseline.json` — the
  enum-domain flip, and a "never-cast-but-OOC-readable summon reads `ready`/probably-up in combat,
  not `source:none`" coverage check + a "ready via observed `Available` edge in combat" check.
  Assert-only, no release (governing rule `docs/m4.5-t3-plan.md`).
- **Live** (`/cdmp hud2` on a dummy): OOC `/cdmp probe` (reads precise) → pull → in-combat
  `/cdmp probe`: a never-cast summon reads `ready`/probably-up (not `none`); cast it → `on-cooldown`
  via `OnCooldown` edge; watch it flip back to `ready` on the `Available` edge (not merely via the
  napkin estimate). At pull start the overlay stages **Dreadstalkers**, not Tyrant/HoG.
- **Release:** commit the addon work, then `wowkb.addon release cdmp --patch` (bump/luacheck/
  push/GitHub release/ghaddons-deploy). **Ask-first.**

---

## 5. Risks / notes
- **Missed edge → stale state.** A missed `SUCCEEDED`/`OnCooldown` could leave a stale `ready`
  from the baseline; a missed `Available` leaves a stale `on-cooldown, remaining 0` (which the
  Coach still treats as probably-up — safe). The `Available`/`OnCooldown` pair is self-healing:
  the next edge corrects it. This is strictly better than today's "collapse to `none`."
- **Secrecy of the alert spellID.** If an alert's spellID reads secret, drop it (no assumption).
  The napkin honesty rule and the OOC baseline still cover that ability.
- **Clean-room.** State must NOT read the old HUD's `S.readyAt`/`HudChrome`. It ports the *hook
  pattern* and owns its own edge store. `wowkb.cdmp`'s statelog denylist enforces the separation.
- **Golden churn is the bulk of the diff** but mechanical; the contract flip is a
  find-and-re-encode across 30 files + 3 new. Re-verify each against the rotation source, not the
  old value.
- **Backward-compat:** nothing outside the pipeline consumes `cd.state`; the old HUD keeps its own
  independent readiness path. No cross-impact.

## 6. Critical files
- `addon/CDMProbe/State.lua` — `readCd` (~166), `ReadCooldown` caller, event registrations
  (~848–851, the START/SUCCEEDED/terminal block), `Build` cd assembly (~683). Add `cdBaseline` +
  the alert hook + the 3-state emit.
- `addon/CDMProbe/Util.lua` — `ns.ReadCooldown` (~219) returns `duration`/`startTime` (already);
  `InCombatLockdown → nil` at ~226 (the reason the edges are needed).
- `addon/CDMProbe/HudState.lua:688–758` — the REFERENCE alert-hook implementation to port
  (`onAlert`, `TriggerAlertEvent` hooksecurefunc, `Enum.CooldownViewerAlertEventType`).
- `addon/CDMProbe/Coach.lua` — Classify (~201–206), the Tyrant special-case (~284), the
  `*ProbablyUp` context (~299–310).
- `corpus/goldens/*/state.json` (all 30 `cd` blocks) + the 3 new scenarios + `coverage.md`;
  `addon/CDMProbe/tests/spec/coach_golden_spec.lua` SCENARIOS.
- `projects/cooldown-hud/probe-baseline.json` — `statelog-enum-domain` + the two new coverage
  checks; `tools/wowkb/cdmp.py` checker fns.

## 7. State of the tree at this doc
- Released: **v0.32.3** (Phase 6 Part 1+2). Addon feature work for Phase 6 is committed + pushed;
  the Phase 6 goldens/coverage/cdmp/docs in the parent wow repo are uncommitted (normal resting
  state). Two symptom-only goldens (`tyrant-pullstart-*`) were created and then **deleted** during
  the Phase 7 diagnosis — Phase 7e re-creates them correctly.

## 8. Progress — Phase 7 implemented off-game (2026-07-27)
**7a–7e + the off-game half of 7f are DONE and green; only the live capture + the ask-first
release remain.** All addon changes are uncommitted in the CDMProbe repo (normal resting state).

- **7a/7b/7c — `State.lua`** ✓ `readCd(live, base, cooldownID)` emits the 3-state table
  (`ready | on-cooldown | unknown`; `source` = trust annotation). Added `cdBaseline` (OOC-readiness
  carried across combat entry), `readyEdge` + a clean-room `TriggerAlertEvent` hook
  (`onAlert`/`installAlertHook(s)`, gated on `St.consumers`, keyed by cooldownID, re-installed each
  `Build`), and `napkinRemaining`. Combat ordering: live napkin countdown (>0) → observed edge →
  napkin-exhausted → OOC-baseline projection → `unknown`. `clearStatelog` wipes the two new stores.
  luacheck + luaparser clean.
- **7d — `Coach.lua`** ✓ `Classify` now derives `ready`/`onCd`/`probablyUp`/`anticipated` off
  `state`+`source`+`remaining`; `dread/grimoire/tyrant/implosion ProbablyUp` and `transientFor`
  re-pointed at `rec.probablyUp`; **Tyrant `cdSource=="none"` special-case deleted**. One extra
  correctness edge the fix exposed: the Dreadstalkers overdue→**LATE** escalation is now guarded
  `not ctx.tct and not ctx.tyrantWindowActive` (a baseline-ready summon has an OOC-old `changedAt`,
  so an unguarded burst-staged Dreadstalkers would read LATE — mirrors the HoG-at-cap guard).
- **7e — goldens** ✓ all 30 `cd` blocks mechanically re-encoded; `opener-midflight`'s never-cast
  Tyrant flipped `unknown/none → ready/live` (it relied on the deleted special-case). Added
  `tyrant-pullstart-dread`, `tyrant-pullstart-dbcast`, `ready-edge-observed` + SCENARIOS +
  `coverage.md` (new cd-state-domain section). **`busted` 33/33 (160 assertions) green.**
- **7c/7f checkers** ✓ `probe-baseline.json` `statelog-enum-domain` flipped to the 3-state domain;
  `statelog-napkin-honesty` re-pointed; added `statelog-coverage-ready-combat` +
  `statelog-coverage-ready-edge`. `cdmp.py` `_CD_STATES`, `_check_sl_napkin`, the two new coverage
  fns, and the golden secrecy-gate (`ready/live` in combat now allowed; only precise
  `on-cooldown/live` is a cheat). `cdmp goldens` = 32 pass / 1 pre-existing sanctioned
  (`opener-ooc`). `cdmp check` correctly FAILs only the **stale pre-Phase-7 capture** (v0.25.0/
  0.28.1, still `anticipated`) — resolved by a fresh capture.
- **7f live + release — REMAINING (ask-first):** deploy the Phase-7 build, pull a dummy, capture,
  confirm `statelog-coverage-ready-combat` + `-ready-edge` flip PASS and the enum/napkin FAILs clear,
  and eyeball `/cdmp hud2` (pull start stages Dreadstalkers, not Tyrant/HoG; a never-cast summon
  reads ready in combat; edge flips ready↔on-cooldown). Then `wowkb.addon release cdmp --patch`.

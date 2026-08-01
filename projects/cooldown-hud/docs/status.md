# Cooldown HUD — status & worklist

**The live worklist.** Current state, what's done, and the improvement backlog. Vision +
design language live in `design.md`; the pipeline in `architecture.md`; the Secret-Values
reality in `notes.md`; the rotation in `specs/demonology/rotation.md`. Historical
milestone provenance is in `archive/milestones.md` (frozen log) and `docs/archive/`.

## Current state

- **Addon:** CDMProbe (`michac/CDMProbe`). The **W4-cutover release shipped** and the live
  build is in sync (multi-spec Phase 5 released as v0.32.22). Run `wowkb.addon list` for the
  live version — never hardcode it.
- **The HUD is the W4 pipeline.** `/cdmp hud` runs `State → Coach → Binder → Renderer`
  (see `architecture.md` → "Live wiring"). The old
  HudChrome/HudBoard/HudScore engine + the opener/burst/pane widgets were **deleted at
  the W4 cutover**; the pipeline is the sole engine.
- **Registered specs: Demonology (266) and Destruction (267).** Both plug into the one
  spec-agnostic pipeline: `Spec<Name>.lua` (data) + `Coach<Name>.lua` (the rotation brain).
  Every other spec resolves passive by design. Demonology is play-settled; **Destruction has
  now flown** (first live pass 2026-07-30) — see the Destruction item below for what that
  settled and what it left.
- **Instrument:** the **decision log** — `CDMProbeDB.decisionlog`, one `S{…} G{…} B{…}`
  line per pipeline decision change, extracted by `wowkb.cdmp decisionlog`. The old-engine `statelog`/`pulls` recorders were retired at the
  cutover; the `/cdmp probe` + `probe-baseline.json` assertion suite was retired 2026-07-29
  (settled readability rules + DB2-sourced tracked set made per-spec re-measurement moot).
- **Gates:** `luaparser` (release) + `luacheck CDMProbe/` + `busted CDMProbe/tests/spec`
  (**562 tests / 4 pending**, luacheck 0 warnings). All three are **hard** release gates —
  `wowkb.addon release` aborts the cut on any non-zero exit.
  ⚠ All three are **source** gates: none of them runs the game, and the v0.32.25 outage
  below is what that blind spot looks like in practice.
- **✅ DONE — `field-fixes-plan.md` (v0.32.28–31), shipped and flown.** The four correctness
  fixes the first rendering session demanded, all confirmed against a live Hellcaller dummy
  pull: phantom unlearned/undrawable abilities no longer win the rotation (**216 → 0** dropped
  cues; the only `SF:ROT×` lines in the capture are in the pre-fix build), the DoT line fires
  for the first time ever off the `PandemicTime` alert latch, and hero tree comes from
  `C_ClassTalents`. The pass also flushed out two further defects, both fixed: a same-frame
  refresh tie, and **charged-ability readiness** — a charged ability raises `Available` per
  charge restored and *never* raises `OnCooldown`, so the ready-edge latched true forever and
  Conflagrate was cued at zero charges. That doc holds the evidence and the two things the
  pass left unproven. **Nothing in it is outstanding.**
- **Active work: `roster-state-plan.md` — ▶ PHASE 4 (the roster coverage probe). Phases 1,
  2 and 3 are all DONE (2026-07-31).**
  Phase 4 asks the cheap out-of-combat question the in-combat maintenance layer cannot: *does
  the CDM cover every id the spec's roster declares?* Its one API prerequisite already landed
  — `ns.ReadValidAlertTypes` was promoted into `Util.lua` in Phase 3, out of the doomed
  `AlertTape.lua`. ⚠ **That API under-reports**, so the report must say "not reported
  eligible", never "cannot fire". Read the plan's §5 before starting. (§10 also permits
  **Phase 6** — cast-results → Coach — to jump the queue; it is independently shippable and
  touches nothing else.)
  ⏳ **One flight is owed first, and it needs you in-game, not code**: a single live pass
  discharges **three** things — Phase 3's own acceptance (Hellcaller's key hint), Phase 2's
  live pass, and v0.32.47's `ChargeGained` re-fly. Checklist under *Owed: the v0.32.36
  re-fly* below.
- **✅ DONE — `roster-state-plan.md` Phase 3 (v0.32.48): the keybind left the cue channel.**
  The DrawList gained a **`keybinds[]` channel**, so `cues[]` means *decisions* again. The
  layering had been inverted: `HudBinds.lua`'s header says a keybind is "identity chrome,
  deliberately OUTSIDE the cue contract", and the Binder was emitting an **empty cue** (a
  keybind with no emphasis) for every displayed icon so the hint could ride every button —
  a display concern travelling the decision channel, a cue count that included chrome, and a
  "cue with no dot" special case in two more files. All three are gone.
  - **And a real user-visible bug rode along.** The keybind resolved off the **base** id
    only. On Hellcaller the row's base is Immolate 348 while the bar holds Wither, so that
    icon got **no key hint at all**. `ns.HudBinds.Resolve` now walks the rung ladder —
    `overrideTooltipSpellID → overrideSpellID → base`, first id with a real binding wins.
    ⚠ **Rung 2 came *out* of the ladder**, not into it: the 2026-07-31 capture found the
    elected `linkedSpellID` on 0 of 72 rows and `GetLinkedSpell()` nil on every frame.
  - ⚠ **The ladder deliberately carries NO spec fences**, unlike `ns.DisplayIdentity`. It
    asks the action bar, so a wrong candidate simply has no binding and falls through. Don't
    "align" the three ladders — the plan's §4.1 and the file header say why at length.
  - **The one real trap was the holder cull**, and the plan called it: both channels ride one
    holder frame per icon, so `R:Draw` culls holders on the **union** of the two active sets.
    Three `renderer_spec` tests pin it in both directions.
  - **Two housekeeping items rode the same cut:** `GetValidAlertTypes` promoted into
    `Util.lua` (Phase 4's prerequisite, rescued from `AlertTape.lua` before that file dies),
    and **`Census.lua` deleted** — all six of its questions answered and consumed.
  - **The plan's §4.2 is the record**, including six places the implementation deliberately
    diverged. ⚠ **Expect the live cue count to DROP** on `/cdmp hud status` and in the
    decision log's `B{}` field: it counts decisions now, not decisions + chrome. That is the
    phase working — confirm it is the *only* thing that moved.
- **✅ DONE — `roster-state-plan.md` Phase 2 (v0.32.46): all ten correctness fixes.** The DoT
  read finally has a channel that **self-clears**. Before this, a whole Destruction pull
  produced **169 `pandemic_refresh` cues and 0 `not_up`**: the HUD could tell you to refresh the
  DoT and structurally could not tell you to apply it. §3.1 (`IsActive()` is a constant `true`
  on tab 1, so the buff-item read jammed to "up") and §3.10 (`PandemicTime` is a one-shot
  notification that never re-arms) had to land together — §3.1 alone would have removed the
  false "up" and left the read with nothing. The other eight are the smaller correctness debts
  the Phase-1 inventory pinned. **The plan's §3.11 is the record**, including ten places the
  implementation deliberately diverged from what was planned.
  <details><summary>Phase 1, the capture, and Phase 2, for the record</summary>

  **Phase 2 (2026-07-31, commits C1–C10, released v0.32.46).** Corpus **0 `pinned-defect` /
  19 `fixed`** — every pin Phase 1 planted was cleared, and `fixed` is the permanent record that
  the case once failed (a meta-test floors `#pinned + #fixed`, so the history cannot be quietly
  deleted; it replaced Phase 1's "≥ 5 failing today", which would have had to be *removed* the
  moment the phase succeeded). Suite **498 → 567 / 0 failures / 4 pending**, 87 → 96 cases,
  luacheck 0 warnings.
  - **The new channel:** `item.auraDataUnit` (is the aura up, and on which side) +
    `item.PandemicIcon` (is it in the refresh window). Blizzard recomputes both every frame off
    secrets we cannot read, so unlike an edge they **self-clear** — which is the only way the
    HUD can ever say "apply it". Both are widget internals, so they carry a bind-time capability
    check and fall back to the edge latch
    (`security-taint-and-restricted-data.md` §4.11 **rule 17b**).
  - **The DoT read is now three channels in trust order:** the per-frame aura verdict → the
    alert latch (demoted to a fast path — still the whole answer on an incapable row) → the
    buff-item presence read (OOC fallback, and gone entirely for a tab-1 row).
  - **New observability:** `/cdmp hud status` grew an `aura-frame read: N/N auraDataUnit, N/N
    pandemic writers` line, and the decision log's `DOT:` field is now two-sided
    (`Imm=tgt+p/pandemic@43.8` — frame verdict / edge latch). `off` is the MISSING answer that
    was previously unreachable.
  - ⚠ **Three deviations a future reader will otherwise "fix" back:** `hasAura`/`selfAura`/
    `charges` stay **truthy on a secret** on purpose (only `isKnown`, which *removes* a row,
    refuses to launder a refusal); `readInfo` uses a batch pcall with a **per-field salvage**
    fallback, because one pcall around the whole copy would lose every field after the one that
    threw; and a tab-2 row still carries a `cd`, shaped
    `{ state = "unknown", readable = false, source = "none" }`, because a uniform shape beats a
    `nil` every consumer would have to guard.
  - **§3.8 was billed "least urgent" and wasn't.** Skipping `readCd` on tab-2 rows meant
    hoisting the `foldBase` write into `St.Build`'s loop, where it now fires whenever `base` is
    readable — strictly wider than before. The smallest-looking fix had the largest knock-on.
  - ✅ **THE LIVE PASS IS FLOWN (2026-07-31, v0.32.46), and it passed.** `not_up` DoT cues
    went **0 → 319** on Diabolist (against 27 `pandemic_refresh`), and Hellcaller fired 15
    `Wth:not_up`, so the `overrideSpellID = 445468` fold is good on both trees.
    `/cdmp hud status` reported **`aura-frame read: 26/26 auraDataUnit, 26/26 pandemic
    writers`** — no row fell back to the edge latch, so channel 1 is live everywhere and the
    rule-17b fence never fired. This pass also discharges the owed **v0.32.36 re-fly**.
  - 🐛 **And it surfaced a separate live bug, now fixed in v0.32.47 — see the ChargeGained
    item below.** Conflagrate won **702 of 1272 decisions** and was cued while genuinely on
    cooldown. Unrelated to Phase 2; the charge napkin has been wrong since field-fix C2.

  **Phase 1 + the capture:**
  
  The **CDM edge inventory**: `tests/fixtures/cdm-cases.lua` + `tests/spec/cdm_cases_spec.lua`,
  **87 declarative cases across 7 axes** authored from `knowledge/addon-dev/cooldown-manager.md`
  (the client study, whose §8 carries nine numbered audit rules), driven by one parametrised
  spec. Suite **384 → 498**, luacheck clean. **Test-only, deliberately no release cut** —
  Phase 2 cut once at the end instead (§3.1 without §3.10 is a regression, so no intermediate
  build was meaningfully flyable).
  - **11 cases were `pinned-defect`: they assert the CONTRACT answer, run INVERTED, and FAILED
    ON PURPOSE.** That is the point of the phase — a suite 100 % green against the current code
    is by construction a snapshot. Phase 2 cleared all 11; each fix's named case went red and
    the fix commit flipped it to `green` + `fixed` in its own diff. 4 more are `unreachable`
    pendings and remain so (identity rungs 1–2, and the dual-category cid — encoded pending rather than green
    *because green would be flaky*, and `busted` is a hard release gate).
  - **A sixth defect, §3.9, was found AND settled while writing it.** `St.Build` bare-indexes
    the CDM struct outside any pcall while `rawCooldown` pcalls the equivalent access on a
    table that passed the same two guards — so either the guard is superstition or Build has a
    crash path. `H.poison` makes **`St.Build` throw**, at both fields tested: the crash path is
    real. Whether the client ever hands us such a table is still `@verify-ingame`.
  - **The harness grew four knobs** (`tests/mock_ns.lua` + a new `harness_spec.lua`, 22 tests):
    table-driven `issecrettable` (it was hardcoded `false`, making six real refusal branches
    unreachable while every suite stayed green — the v0.32.25 shape), `H.throws`/`H.guard`,
    `H.poison`, and `H.installGlobals()` called from `H.fresh()` (the `_G` fakes were installed
    at *file* scope, so a mutation during one test outlived the file that made it). Plus **real
    client fakes** — `GetSpellCooldown`/`GetSpellCharges`/`ForEachAura`/`GetPlayerAuraBySpellID`/
    `IsSpellOverlayed`, default-inert — so `Util.lua`'s guard ladder, the combat short-circuit
    and the GCD trap are all inside the code under test.
  - **⏳ BLOCKED ON ONE CAPTURE, and the instrument is now deployed (v0.32.42).** Three of
    the six findings are *wrong by construction with an unconfirmed trigger* — we know the
    code is wrong, not whether the client produces the input. `/cdmp census` (Census.lua,
    **TEMPORARY**, AlertTape model) walks every cooldownID in every category set and dumps
    the raw struct + the frame reads, each field through its own pcall, classified five ways
    (`num`/`bool`/`SECRET`/`SECRET-TABLE`/`nil`/`threw` — collapsing the last three is how
    you conclude "Blizzard doesn't populate this" when the truth is "we may not read it").
    **The protocol is two captures**, because half the questions are *only* about the
    combat difference: `/cdmp census` standing still, then `/cdmp census arm` + pull, then
    `/reload`, then `uv run python -m wowkb.cdmp census`. The extractor prints the verdict
    per question and warns if only one of OOC/CMB is present.
    **Every capture is labelled PER BUILD** — wall clock, `specID`, the hero tree read
    **fresh** (not through State's cache), and the talent config id — and the extractor
    groups verdicts by build rather than pooling them, because the CDM's tracked set changes
    wholesale on a spec swap and the OOC/CMB pairing is only meaningful *within* one build.
    ⚠ **A `heroStale` capture is a live bug report, not a census artefact** — it means the
    pipeline was deciding on the wrong hero tree at capture time.
    | Q | Decides |
    |---|---|
    | Q1 any **tab-1** row with `hasAura`/`selfAura`? | §3.1 live or latent |
    | Q2 any row with **both** override fields? | §3.5 reachable or not |
    | Q3 does a **fresh** read carry the elected `linkedSpellID`? | **blocks Phase 3** |
    | Q4 does a struct field's **index** ever throw? | §3.9's trigger |
    | Q5 any cid in **two** category sets? | the 4th pending |
    | Q6 do `wasSetFrom*`/`auraDataUnit` survive combat? | `cooldown-manager.md` §7 `[gap]` |
  - **✅ THE CAPTURE IS DONE (2026-07-31, v0.32.44/45).** All six questions answered, plus a
    seventh nobody asked. Headlines: **§3.1 is LIVE** — 17 tab-1 rows carry an aura flag
    including Immolate, and it jams the DoT read to "up" on both hero trees (all **169** DoT
    cues in the trace say `pandemic_refresh`, **zero** say `not_up`). **§3.9's trigger is
    absent** (0 fields raised across 72 cids × 2 trees × in/out of combat) so it drops to
    last. **Phase 3 loses rung 2** — the elected `linkedSpellID` is never set, on the frame
    or in a fresh read, and Hellcaller's Wither arrives via `overrideSpellID` instead.
    **Phase 4 needs rewording** — `GetValidAlertTypes` under-reports.
  - **NEW §3.10, and it is the one you feel:** `PandemicTime` is a one-shot notification,
    and a re-application of a live aura raises **nothing** — 41 Immolate casts produced 1
    `OnAuraApplied`, 1 `PandemicTime`, 0 `OnAuraRemoved`. The DoT cue fired for exactly one
    5.8 s window (`t92.5→t98.3`) and was silent for the rest of the pull. The fix is a new
    capability, not a repair: `item.auraDataUnit` (is it up) and `item.PandemicIcon` (is it
    in the window), both measured readable in combat and both self-clearing. Mechanism +
    preconditions: `knowledge/addon-dev/security-taint-and-restricted-data.md` **§4.11**.
  - **The "what we cannot know" ledger** (2026-07-31, pressure-tested): after Phase 2 the
    remaining blind spots are **not** just aura stack counts. (a) A declared aura with **no
    CDM row** has no channel at all — no `IsActive()`, no `auraDataUnit`, no edges, and
    `COMBAT_LOG_EVENT_UNFILTERED` **errors on registration** in 12.0 — though the one
    suspected instance, Crashing Chaos, turns out to be redundant and should leave the
    roster. (b) **Pandemic never arms for a player-side aura** (`CooldownViewer.lua:515`),
    which is Blizzard's own scoping and matters only for HoTs, i.e. not until healers.
    (c) **Target-side facts** (health, TTD, count) stay absent — but execute windows are
    reachable *without* health, via the ability becoming usable (`SPELL_UPDATE_USABLE` is a
    tab-1 event driving icon desaturation — a §4.11-shaped proxy worth probing).
    On stacks: the **count** is a stored copy of a secret and stays intractable, but
    Blizzard already computes `applications > 1` and renders it as empty-vs-non-empty text
    (`CooldownViewer.lua:1235-1242`), so the *is-it-stacked* boolean may be observable via
    the `Applications` FontString's width. One probe; decisive for 2-stack procs like
    Backdraft, useless for Wither's 8-stack.
  </details>
- **⏳ Awaiting a live pass (needs you in-game, no code owed): `virtual-cdm-plan.md` — the
  virtual CDM panel. ✅ Phases 1, 1b and 2 all SHIPPED + FLOWN.** The HUD draws its own icons
  for the abilities Blizzard's Cooldown Manager will not display, so a spec's floor press stops
  being invisible. **The two-hero-tree pass flew 2026-07-30** (v0.32.35): Hellcaller is
  confirmed (`w:-` 31 % → **0.0 %**), Diabolist exposed a separate display-identity bug now
  fixed in **v0.32.36**. ⏳ **The only thing left on this plan is the v0.32.36 re-fly** — see
  *The 2026-07-30 two-hero-tree pass* below for the checklist.
  - ✅ **Phase 1b — the display-identity fence** (`St.DisplayedIdentities`). The `absent`
    test now asks the identities the CDM is *displaying* (base ∪ `liveSpellID` ∪
    `overrideSpellID` ∪ `overrideTooltipSpellID`), not the `abilities` keys. Unioning the two
    STATIC override fields is load-bearing: with the Demonic Art armed that row's
    `liveSpellID` becomes Infernal Bolt `433891`, so a `liveSpellID`-only check would let the
    duplicate flicker back mid-combat. Mutation-checked both ways.
  - ✅ **Phase 2 — the moveable panel.** `V.root` has real extents (row width, floored at 3
    icons so a zero-row spec is still grabbable), drag + saved position in
    `ns.db.virtualPanel` (BucketBinds' `Console.lua` shape verbatim, relativeTo discarded on
    restore), and `/cdmp panel unlock | lock | reset` (bare toggles). Mouse is enabled only
    while unlocked, so the panel never eats a click in play; the unlock affordance is a
    terminal-green edge + `CDMProbe` caption with the icons held lit.
  - ✅ **The two-hero-tree pass is FLOWN (2026-07-30) — see *The 2026-07-30 two-hero-tree
    pass* below.** Hellcaller is confirmed good (`w:-` **0.0 %** over 265 decisions, zero
    `×`, Incinerate drawn 50×). **Diabolist was NOT** — it exposed a real bug (the HUD was
    blind to Incinerate there), fixed in **v0.32.36** and awaiting its re-fly. L12 Infernal
    Bolt is still unexercised, and could not have fired: it needs an Incinerate the brain
    can pick, which is exactly what was broken.
  - ✅ **It worked: `w:-` went 59/191 (31 %) → 0/258 (0 %)**, zero Binder drops, `Inc` cued
    and drawn 89 times. Nothing regressed.
  - ✅ **The override channel fires for an untracked display id** — the plan's one
    `@verify-ingame`, closed on the Diabolist run and written up in the addon-dev KB
    (`api-events-and-discovery.md` §2.8). ⚠ L12 (Infernal Bolt) is still **untested, not
    broken** — Conflagrate won at L4 on every armed line, above it.
  - 🐛 **The bug Phase 1b fixed — DUPLICATE icon on Diabolist.** Blizzard's Incinerate row is
    keyed **Shadow Bolt `686`** (display overridden), and its `isKnown` is **hero-tree
    dependent** — false on Hellcaller, true on Diabolist. So `abilities[29722]` was nil even
    while Blizzard was drawing it, and the `absent` fence synthesised a second icon. The
    lesson worth keeping: the plan *rejected building on* `cid 66181` because its identity is
    split, recorded the hazard, and then wrote a fence that compared base identities anyway.
  - **The approach changed at implementation, for the better:** virtual rows are **detected
    from the spec's own ability table**, not declared per ability. **Phase 3 came free** —
    Demonology's Shadow Bolt needed zero edits. See the plan's *§ The reframe*.
  - **It reverses half of field-fix A, deliberately.** A's `unlearned` fence was
    *correctness* and survives; its `no-icon` fence was a *display* limit enforced at the
    *decision* layer, correct only while the product was strictly a CDM overlay.
  - ✅ **Follow-up DONE: `design.md` no longer describes the product as strictly a CDM
    overlay.** The elevator pitch now reads "a rotation helper that displays on the CDM when
    it can, and on its own icons when it cannot", with an amendment note recording why the
    virtual panel does not violate pillar 3 — it is **additive only**, existing solely for
    abilities Blizzard displays *nowhere*, so nothing native is replaced, re-skinned or
    moved. "Enhance, don't replace" was never a promise to stay silent where Blizzard says
    nothing.
- ✅ **The finding that set the agenda — 31 % of decisions had no winner — is FIXED.** The
  virtual panel took Hellcaller to **0.0 %** (265 decisions, 2026-07-30) and v0.32.36 closes
  the Diabolist half. The diagnosis that follows is kept because it explains *why* the fix
  had to read the spec's ability table rather than infer from what is missing.
  59 of 191 decision
  changes are `w:-`, every one at **0–2 shards** — below Chaos Bolt's cost there is no floor
  press, because Incinerate has no CDM icon. The HUD is blank for roughly a third of a pull.
  Correct behaviour, bad experience. Incinerate `29722` is **not in `CooldownSetSpell` at
  all** — so it never enters `enumerate()`, never reaches `cooldowns`, and is not even
  reported in `dropped`. There is **no runtime signal for it whatsoever**, which is why the
  fix reads the spec's own ability table rather than inferring from what is missing.
  - ⚠ **`cid 66181` is NOT the handle, despite looking like one.** Destruction's set carries
    Shadow Bolt `686` there with its display overridden to Incinerate (which is why the
    settings panel shows an Incinerate tooltip on a greyed icon, and why it surfaces in
    `dropped` under `686` as *unlearned* — the wrong spell). It is an override on an entry
    the client considers unlearned, it is Destruction-specific, and Demonology's Shadow Bolt
    hole has no analogue. **Synthetic negative handles generalise; this does not.**
- **Destruction Warlock — ✅ FLOWN (2026-07-30).** `SpecDestruction.lua` +
  `CoachDestruction.lua` implement `specs/destruction/rotation.md` L1–L13 through the
  `adding-a-spec.md` recipe (no pipeline edits, no Renderer edits, no contract edit). The
  first live pass settled the big DB2-predicted unknowns — Incinerate is genuinely untracked,
  Immolate rides its **cast** id `348` on Essential, and both of its cooldownIDs raise
  `PandemicTime` — and cost four code fixes. **A second pass on 2026-07-30 flew all three
  configurations** (Hellcaller / Diabolist / Demonology) and settled `ART_FROM_RITUAL`
  (**stays `false`** — the ritual container is up 88 % of the time), confirmed the charge
  napkin, and found the Diabolist display-identity bug — see *The 2026-07-30 two-hero-tree
  pass* below. **Still open on this spec:** which Art override id actually surfaces
  (`433891` vs `434506` — the log could not tell them apart, fixed for the next capture).
- The **multi-spec refactor is complete**
  (`multispec-plan.md`, all 6 phases done 2026-07-29, shipped v0.32.22). The framework is
  one spec-agnostic pipeline + a per-spec brain that plugs in: registry + resolver
  (`SpecRegistry.lua`), per-spec Coach brain (`CoachDemonology.lua`), array-of-powers
  resources (`resourceBars[]` + N stacked meters), the decision-log seam (`DecisionLog`),
  and live spec detection (login + `PLAYER_SPECIALIZATION_CHANGED`, registered-or-passive).
  Phase 6 (docs) synced `architecture.md`/`notes.md`/addon `CLAUDE.md` to the code; the
  contract needed no edit. **Destruction is the proof the seam works** — it was added as a
  pure sibling (two Lua files, a `.toc` line pair, a test) with zero pipeline edits, which
  is what the refactor was for. ✅ **The owed in-game Demo smoke is DONE (2026-07-30):**
  225 clean Demonology decisions, zero `w:-`, zero `×`, and the respec in/out showed no
  stale cue — closing the item deferred since v0.32.22.

## The 2026-07-30 two-hero-tree pass (v0.32.35)

The verification session the virtual-CDM plan was waiting on: one character, flown across
**three configurations** in a single afternoon. It confirmed the panel works, found **one
real bug**, and closed four of the open questions below. Fixes shipped in **v0.32.36**.

Extract the evidence with `cd tools && uv run python -m wowkb.cdmp decisionlog` →
`raw/cdmp-decision.log`.

| Configuration | lines | `w:-` | `×` | Inc won | Inc drawn | `PR:art` |
|---|---|---|---|---|---|---|
| Destro / Hellcaller | 265 | **0.0 %** | 0 | 10 | 50 | 0 % |
| Destro / Diabolist | 225 | **6.2 %** | 0 | **0** | **0** | **88 %** |
| Demonology | 225 | 0.0 % | 0 | — | — | 0 % |

> ⚠ **Two traps in reading that log — both cost time, both are now fixed in code.**
> 1. **Do NOT trust a session's `tracked:` header for hero tree.** It is stamped at the
>    session's *first* record, and the respec happened ~15 s *after* login — so every
>    session is labelled with the configuration the player was **leaving** (a Hellcaller
>    run filed as `tracked:Imm`). **Segment by content instead:** `Mal=` in `CD:` ⇒
>    Hellcaller, `HoG=` ⇒ Demonology, else Diabolist. v0.32.36 makes this self-describing —
>    `DecisionLog` now emits a `t… # config <spec> tracked:<codes>` marker whenever the
>    tracked set **changes**, so a mid-session respec announces itself.
> 2. **Scope to the build under test.** The ring holds 6 sessions (raised 3 → 6 in
>    v0.32.35) and the two oldest here are **v0.32.32**. Counting all 1110 lines instead of
>    the 715 from v0.32.35 roughly doubles the Hellcaller sample and changes every rate.

### 🐛 The bug: Diabolist was blind to Incinerate — FIXED v0.32.36

**Incinerate won 0 of 225 Diabolist decisions and was drawn 0 times**, while the same
character on Hellcaller drew it 50×. The virtual panel was *not* at fault — the opposite:
Hellcaller works precisely *because* Incinerate goes down the virtual path, and Diabolist
does not, so it took the real-CDM path and fell in a hole nobody had walked.

**Root cause — one cause, two symptoms.** On Diabolist, Blizzard's Incinerate row is keyed
**Shadow Bolt `686`** with its display overridden to `29722` (`686` reads `isKnown` only on
Diabolist — the hero-tree split Phase 1b already documented). Every producer keyed the
**raw base**, so:

- `State` keyed `abilities[686]`, and `CoachDestruction.lua` gates on `ctx.facts[base]` and
  asks `facts[29722]` — so the Incinerate line **could never win**;
- `HudLayout` published `spellID = 686`, so the Binder's cue join (`cues[entry.spellID]`)
  **missed**, *and* the keybind was looked up for Shadow Bolt — which is not on the bars.

That is exactly the "no overlay, no keybind" the player saw on a button they press
constantly. The `6.2 %` `w:-` is the visible residue; the other 93.8 % is worse-hidden —
the HUD confidently showed a *different* press because the floor press was unreachable.

**The fix (v0.32.36): one rule, one place — `ns.DisplayIdentity(base, ov, ovTooltip)`.**
Both producers call it, so State's keys and the Layout's `spellID` cannot drift apart.
It adopts an override only when the **active spec declares it** as `kind == "button"` with
`expect ~= false` — so a *transform* never becomes the identity of the frame it merely
rides. Three fences worth keeping in mind before touching it:

- ⚠ **It reads the STATIC override fields, never `liveSpellID`.** `liveSpellID` moves to
  Infernal Bolt `433891` while the Art is armed, so keying on it would make Incinerate's
  identity **vanish mid-combat** — precisely when the ability is most active. (Same
  reasoning as Phase 1b's `DisplayedIdentities` fence, which unions both static fields.)
- ⚠ **State re-keys only rows that SURVIVED the filter.** Re-keying a *dropped* row would
  make `virtualCandidates`' "not dropped-unlearned" fence refuse to synthesise our
  Hellcaller Incinerate icon — killing the path that already works. A drop keeps its raw
  base.
- ⚠ **The re-key is a deterministic second pass** (a `claimed` list sorted by base), so
  `pairs` order can never decide a contested identity.

### What the pass settled

1. ✅ **The Hellcaller virtual panel works.** `w:-` **31 % → 0.0 %**, zero Binder drops.
   Phases 1 / 1b / 2 confirmed in the field. This is the headline result.
2. ✅ **Destruction open item 3 — ANSWERED: NO.** Diabolic Ritual `428514` is up on **88 %**
   of Diabolist decisions, so it can **never** mean "Art armed" — treating it as such would
   jam Chaos Bolt above Conflagrate and Summon Infernal for most of a pull, exactly as the
   design note feared. **`ART_FROM_RITUAL = false` stays, now on evidence rather than
   caution.** It is 0 % outside Diabolist, i.e. genuinely Diabolist-exclusive.
3. ⏳ **Destruction open item 4 — HALF answered, and the log could not answer the rest.**
   The Art transform fires (`IB` on 9 Diabolist lines), but `SpecDestruction`'s log table
   mapped **both** `433891` and `434506` to the single code `IB`, so *which numeric id
   surfaced is unknowable from the capture*. `RU` never appeared on Destruction at all.
   **Fixed for the next capture (v0.32.36):** the ids now carry distinct display codes
   (`IB`/`IB2`, `RU`/`RU2`/`RU3`). ⚠ That required splitting a field that was doing double
   duty — the brain branched on `abbr`, so a per-id code would have broken Art detection.
   Semantics moved to a dedicated **`art = "infernal" | "ruination"`** field; `abbr` is now
   display-only. **Never branch rotation logic on `abbr` again.**
4. ✅ **The charge napkin never over-counted.** It stayed inside `[0, 2]` all pass, and both
   exact-vs-napkin checkpoints agreed (`=1/2` → `~1/2` at t39; `~2/2` → `=2/2` at t120).
   This closes the confirmation owed by field-fix C2.
5. ✅ **Demonology smoke + respec-with-no-stale-cue.** 225 clean Demonology decisions, zero
   `w:-`, zero `×` — closing the v0.32.22 multi-spec item owed since 2026-07-29, and
   Destruction open item 5 with it.
6. ⏳ **L12 Infernal Bolt is still unexercised** — and *could not* have fired, since it
   needs an Incinerate the brain can pick. It should come free with the v0.32.36 fix.

### ⏳ Owed: the v0.32.36 re-fly

**One flight discharges four owed things** — this re-fly, Phase 2's live pass, Phase 3's
acceptance, and v0.32.47's `ChargeGained` re-fly. Nothing below is verified in the field
yet. `/reload` first, then:

- **`/cdmp rt states`** — three visual questions in one card: (a) is the dot a clean
  borderless circle that blends into its glow? (b) does LATE read as an *escalated*
  rotation cue rather than a different instruction? (c) does the violet FALLBACK still
  separate from the shard pips? Plus the Phase-3 one: does the **IDLE** square still read
  "key hint, no dot"? It is the only square now emitted on the keybinds channel alone.
- **Phase 3 — `/cdmp hud layout` on Hellcaller.** Every displayed row shows a key, and the
  Immolate/Wither row now shows **Wither's** key where it previously showed none. Switch to
  Diabolist and confirm it still shows Immolate's. Screen otherwise unchanged: key hints on
  every displayed icon, dots only where cued, `/cdmp hud` off leaves Blizzard's UI
  pixel-clean. ⚠ **The cue count WILL drop** on `/cdmp hud status` and in the decision log's
  `B{}` field — it counts decisions now, not decisions + chrome. Confirm that is the only
  thing that moved.
- **Phase 2 — the DoT read.** The acceptance signal is the **`not_up` cue appearing at all**
  in `wowkb.cdmp decisionlog` (baseline: 169 `pandemic_refresh` / 0 `not_up` across a whole
  pull), the DoT cue firing across the *whole* pull rather than one 5.8 s window, `Imm=off/…`
  in the `DOT:` field, and `aura-frame read: N/N` non-zero on `/cdmp hud status`.
- **v0.32.47 — the `ChargeGained` gain floor.** Pull a dummy as **Destruction**, then
  `/reload` + `wowkb.cdmp decisionlog`: Conflagrate's share of decisions should fall well
  below its **702-of-1272** baseline, and it must not be cued at zero charges.
- **Diabolist dummy pull — the decisive one.** Does Blizzard's Incinerate icon now carry
  **a keybind and a cue**? Then `/reload` + re-extract: expect `w:-` ≈ 0 % (was 6.2 %),
  `Inc` winning and drawing, `# config` marker lines, and an `IB` vs `IB2` answer.
- **Regression check — one Hellcaller pull.** Incinerate must **still** draw on *our* panel
  with `w:-` at 0 %. Fix 1 deliberately does not touch dropped rows; this is the assertion
  that proves it in the field. ⚠ **This is the one that matters most** — the fix changes
  the key of `abilities` entries, the pipeline's most delicate seam.
- Watch for an **L12 Infernal Bolt** cue if the Art arms while Conflagrate is at 0 charges.

## The 2026-07-30 comment-trim + layering pass (v0.32.38 — cut + deployed)

Not a bug fix — readability and layer hygiene, following two code reviews whose
defect-class findings already shipped in v0.32.37. Six commits, gates green at each.

**Layering**

- **Hero resolution moved into State and rides the pulse** (the one substantive change).
  `CoachDestruction` was calling `C_ClassTalents.GetActiveHeroTalentSpec()` and `ns.Printf`
  from inside `spec:Context`, which `Coach:Compute` runs at 10 Hz — breaking
  `architecture.md` Stage 1 and `Coach.lua`'s own purity claim. State now owns the read on
  the same discipline as `knownCache` (pcall + IsSecret guarded, cached, wiped on
  `SPELLS_CHANGED`), and the pulse carries `hero` + the raw `heroSubTreeID`. **A captured
  pulse can now reproduce a hero-gated decision** — the stated payoff of the seam. The
  brain keeps `heroFromSignals` as the fallback for a refused API read; the announcement
  moved to `HudDriver`'s one-shot notice, latch semantics preserved.
  Mutation-checked four ways (swapped SubTreeID map / hero dropped from the pulse /
  invalidation removed / brain ignores `state.hero`) — all four fail the suite, the last
  through the branch oracle rather than only the new tests.
  - 📌 **Recorded while doing it:** `ctx.hellcaller` has **no consumer** in `RankWinner`
    today. L5b Malevolence fires because Malevolence is in `facts` at all, and L8's DoT id
    resolves from whichever candidate the pulse carries — both are *tracked-set* facts.
    That is the independence the field-fix bought, and it means this move could not change
    which lines fire. Commented at the assignment so it is not re-derived.
- **Verified-dead code deleted:** `ns.DumpViewers`, `ns.ItemSpellID`, `B.GetForItem`,
  `B.Explain`, `B.Stop`, `Renderer:Root`, `N.Stop`/`N.PrintStatus`/`N.StatusText` — all
  orphans of the retired `/cdmp probe` and the old HUD engine.
- **`JUDGE` and `SEQUENCE` retired end to end.** `guidance-contract.json` has called both
  RETIRED since W4 Phase 8 / the TCT redesign and no production code emits either; what
  kept them alive was a closed loop — two render fixtures existed to display the tokens,
  and the tokens were kept because the fixtures displayed them. Theme entries, the
  `inventory` and `burst-hold` fixtures, and their tests are gone. Tests that used JUDGE
  merely as "a token with no `GLOW_SPEC` entry" now use a deliberately unknown token, so
  they assert the contract rule (**no entry ⇒ no circle, no ring**) rather than one retired
  token's continued existence. The fallback-violet rationale is re-anchored to the shard
  pips, which are the real constraint.
- **`ns.DisplayIdentity` moved `Util.lua` → `Viewers.lua`.** It reads `ns.SpecInfo`, so the
  bottom-of-stack utility file (loaded 3rd) was depending on the spec registry loaded six
  files later. Pure move; `mock_ns` now loads the real `Viewers.lua` and `viewers_spec`'s
  shipped-symbol gate covers it.
- **The `/cdmp rt` rig split out into `RenderTest.lua`.** `Renderer.lua` was 822 lines:
  519 of pure Stage-4 renderer and 300 of impure rig (placeholder frames, a `C_Timer`
  ticker, direct `ActionButtonSpellAlertManager` calls). Now 512. Pure file move.
- **Stale prose that had gone wrong:** the passive-spec notice and `SpecRegistry` both said
  "only Demonology is supported", two specs after that stopped being true — the notice now
  counts `ns.Specs` instead of restating it. `Mode.lua` no longer names one spec's spell
  from a spec-agnostic module, and no longer claims the Coach never branches on mode
  (`CoachDestruction`'s L10 Rain of Fire does).

**The comment trim** — 7,532 → 7,218 lines, 3,254 → 3,090 comment lines (43% → 41%).

Volume was never the defect; narrating history was. The largest single win was
`SpecDemonology`'s five per-table essays explaining the behaviour of modules deleted at the
W4 cutover, replaced by one DORMANT banner that names the tables, states they have no live
reader, and says *why they are kept* (revival surface + the `ns.SpecFields` rebind
contract). Also: `Coach.lua`'s header (30 of 47 lines argued with the old engine), the
`role`-enum post-mortem about a table that never existed in that file, `HudNapkin`'s 54-line
preamble, and `Renderer`'s `HudChrome.lua:1051`-style colour provenance (values kept,
addresses dropped).

⚠ **Three comments actively misdirected a debugger** — `HudNapkin` said `HudState` calls
`Clear`; the caller is `State.lua`. Corrected, not deleted.

Duplicated rationale now lives **where it can be violated**, with a pointer elsewhere: the
static-overrides-never-`liveSpellID` fence in full at State's `displayedIdentities`, the
keybind-off-the-base rule at `HudBinds`' header, the AlertTape "delete me" end date in
`AlertTape.lua` only. Incident transcripts reduced to the rule they taught (both Renderer
dot API facts kept; the capture numbers dropped — they live here). Bare section refs into
`docs/archive/` (`§0.5.x`, `§7.2`, `M3c`, `M4.5`) stripped, prose claim kept.

**Deliberately NOT done:** separator/banner normalisation (~74 rules → ~148 lines). It is a
line-count trick that does not touch prose volume and would add mechanical noise to
`git blame` across nearly every file. Separators aid navigation in the large files and stay.

**Also not done:** the two D1 "pointer" sites (`HudLayout.Build`, `State.enumerate`). Both
are already single six-word parentheticals *at the call site where the rule can be
violated*, so replacing them with a cross-reference would degrade them for zero lines.

⏳ **In-game verification owed** — this pass rides on top of v0.32.37's own owed re-fly, so
fly that first. Then: a **Hellcaller dummy pull** (Malevolence/Wither lines fire, `w:-` ~0 %,
Incinerate still draws on our virtual panel) and a **Diabolist pull** across a respec in and
out (the hero tree announces once and only once — the `heroSaid`-style latch is the thing
most likely to have regressed). Plus `/cdmp rt states` — the card must still draw all five
states over real icon art after the file split.

## Phase ledger (the W4 build)

| Phase | What | Status |
|---|---|---|
| 0 | Audit + baseline (dead-code strip W4a) | ✅ done |
| 1 | State — the reduced client picture (`State.lua`) | ✅ done |
| 2 | Coach → Guidance + the independent test corpus | ✅ done |
| 3 | Renderer (semantic tokens → pixels) | ✅ done |
| 4 | Binder (spellID cue → display cooldownID) | ✅ done |
| 5 | Live driver (`HudDriver`), flag-gated parallel run | ✅ done |
| 6 | TCT redesign (one-press cue walk; sequence panel retired) | ✅ done |
| 7 | 3-state CD model (`ready`/`on-cooldown`/`unknown`) | ✅ done |
| 8 | Ranked-winner guidance (winner + `ROTATION_FALLBACK` + `SOON`) | ✅ done |
| — | **Cutover & cleanup** — reclaim `/cdmp hud`, delete old engine + statelog, consolidate docs | ✅ done (released) |

## Open items (verify / close)

- **Release the W4 cutover** — ✅ **shipped.** The cutover build released and the live addon
  is in sync (`wowkb.addon list`): `/cdmp hud` is the default and draws (summon cues
  included), `/cdmp reset` clean, toggle off ⇒ Blizzard UI pixel-clean, migration folds a
  prior `hud2` flag into `hud`.
- **In-game verification of the pipeline output** — the domain-view re-layer and the
  ranked-winner guidance want an eyeball pass at a dummy + a read of the decision log.
  ⚠ **This being deferred cost us a two-day total outage.** `ns.ItemCooldownID` was deleted
  with `HudCore.lua` at the W4 cutover while `HudLayout.Scan` still called it behind an
  `ns.X and ns.X(item)` nil guard — so it silently returned nil for every icon, the Layout
  came back empty, the Binder dropped every cue, and **the HUD drew nothing on any spec
  while still reporting ON**. Every release from the cutover through v0.32.24 was dead.
  Fixed in v0.32.25. **Treat "no in-game smoke since the last structural change" as a real
  risk, not paperwork.**
- **Doctrine that came out of that outage** (both now enforced in code):
  1. **No `ns.X and ns.X(...)` nil guards on our own modules.** A guard on a symbol *we*
     ship converts a deleted definition into a silent no-op. Call it directly and let a
     missing definition throw. Guards are for genuinely optional collaborators only.
  2. **A stub proves the caller works GIVEN the collaborator — never that the collaborator
     EXISTS.** `hudlayout_spec` stubbed `ns.ItemCooldownID`, so busted stayed green against
     a function the addon no longer shipped, and luacheck could not see it either (the
     guard is valid Lua). Every heavily-stubbed seam wants one companion test that loads
     the **real** module and stubs only what needs a live client —
     `tests/spec/viewers_spec.lua` is the pattern.
- **`charge` half of the full-database read** — **closed by field-fix C2 (2026-07-30), with
  an in-game confirmation owed.** Conflagrate and Shadowburn are the project's first charged
  tracked abilities. `ns.ReadCharges` is combat-gated (`C_Spell.GetSpellCharges` reads secret
  in restricted combat), which used to mean both degraded to binary off-cooldown for the
  whole pull. There **was** a channel we were missing: `ChargeGained` fires in combat off the
  alert choke point, on any upward move of Blizzard's cached count — so cooldown-reset procs
  land there too (observed ×10 across ~80 s on Conflagrate, against a ~13 s recharge). State
  now keeps a **napkin**: exact OOC seed → −1 on `SUCCEEDED` → +1 on `ChargeGained` → clamp
  `[0, max]`, exact re-read wins on combat exit, biased to **undercount**, tagged
  `source:"napkin"`. ⏳ **Still the one thing the live pass could not prove.** The channel is
  confirmed live (`ChargeGained` ×11 in combat), but the estimate never changed a decision,
  because readiness was broken in a way that masked it: a charged ability raises `Available`
  per charge restored and **never raises `OnCooldown`**, so the ready-edge latched true and
  `Conf=R` on 190 of 194 lines. That is fixed (the count is now authoritative, v0.32.31) and
  the decision log gained a **`CH:`** field.
  ✅ **CLOSED 2026-07-30 — the napkin never over-counted.** Every `CH:` value across the
  pass sat inside `[0, 2]` (not one `~3/2`), and both exact-vs-napkin checkpoints agreed: an
  exact `=1/2` at t39.0 handed off to `~1/2` at t39.1, and the napkin's `~2/2` was vindicated
  by the exact combat-exit read `=2/2` at t120.2 (and again at t126.3). The undercount bias
  held. **Nothing is outstanding on this item.**
  ⚠ Shadowburn has **no** charges (DB2 `ChargeCategory = 0`), so it is not a consumer.
- **Destruction in-game confirmation** (the `adding-a-spec.md` Step-8/10 pass) — **all six
  ANSWERED after the second 2026-07-30 pass; only half of item 4 survives.**
  1. ~~`/cdmp hud status` → `spec: Destruction (profile active)`.~~ ✅ the pipeline ran and
     the Destruction brain drove it for a full pull.
  2. ~~`/cdmp hud layout` → **does Incinerate appear?**~~ ✅ **ANSWERED 2026-07-30: NO.** The
     live Essential set is 9 entries and Incinerate, Soul Fire, Havoc and Channel Demonfire
     are all absent. So the floor press has no icon *and* the Infernal Bolt transform is
     blind. Field-fix A stops that corrupting the *decision* (an undrawable row no longer
     wins the list); it does **not** make Incinerate visible — that is the *artificial CDM
     icons* item below, which this answer promotes from speculative to concrete.
  3. ~~**Is the Diabolic Ritual container (`428514`) a usable "Art armed" signal?**~~
     ✅ **ANSWERED 2026-07-30 on the Diabolist pull: NO.** It is up on **88 %** of Diabolist
     decisions (198 of 225) — a container that is almost always present cannot mean "the Art
     is armed". Reading it that way would have jammed Chaos Bolt above Conflagrate and
     Summon Infernal for most of a pull, which is exactly what the design note feared.
     **`spec.ART_FROM_RITUAL` stays `false`, now on evidence rather than caution.** It reads
     0 % outside Diabolist, confirming it is genuinely hero-tree-exclusive.
  4. ⏳ **Do the Art override IDs resolve to `433885` / `433891`?** **HALF answered.** The
     transform demonstrably fires (`IB` on 9 Diabolist lines; `RU` never appeared on
     Destruction) — but `SpecDestruction`'s log table mapped **both** `433891` *and* `434506`
     to the one code `IB`, so the capture cannot say which id surfaced. **The instrument was
     the limitation, and it is fixed (v0.32.36):** the ids now carry distinct display codes
     (`IB`/`IB2`, `RU`/`RU2`/`RU3`), so the next capture answers this outright. All pairs
     stay mapped meanwhile. *(The set-884 dump lists both `433885` and `433891` at cids
     `171413`/`171412`, so the Destruction-side pair is at least the one the data carries.)*
  5. ~~Respec in and out: the HUD toggles between active and passive with no stale cue.~~
     ✅ **DONE 2026-07-30** — three configurations flown in one session (Hellcaller →
     Diabolist → Demonology), no stale cue at any handover.
  6. ~~Dummy pull → `wowkb.cdmp decisionlog`, grep `w:-` / `×`.~~ ✅ **DONE.** `×` is **zero**
     on the fixed build (the only two in the capture are in the pre-fix session, both
     `SF:ROT×`); `DR:` is stable and every dropped row checks out by name; `w:-` at 0–2
     shards is the untracked-Incinerate signature, quantified at **31 %** of decisions —
     which is what promoted the virtual CDM panel to Active work.

## Improvements / backlog

The container for what's next. The old engine is gone, so this is where feature/quality
work lands now — the user drives the list; a few already-surfaced items are seeded:

- **📋 `roster-state-plan.md` — anchor State on the spec roster, not the CDM database.**
  A written plan (2026-07-31), six phases. **Phases 1 and 2 are DONE; Phase 3 is now the
  Active work (see above). Phases 4–6 are not started.** Grew out of the `wow-developer`
  client-correctness review of `State.lua` (same date), which found three source-verified
  defects in the CDM→State mapping: `item:IsActive()` read uniformly across families (it is
  **constant `true`** on Essential/Utility rows — `CooldownViewer.lua:362-364` — and feeds
  `buffs`, so a burst window can read permanently open), charges read off the display
  identity instead of `overrideSpellID or spellID` (`CooldownViewerItemData.lua:283-288`),
  and the identity ladder skipping rung 2 (`linkedSpellID`). **Phase 1 was the net, and it is
  built**: a *fixture inventory* of the edges the CDM can hand us, because the ~90
  `state_domainview_spec` tests are **regression-shaped** — every `describe` is named after a
  past bug, so coverage tracked what has bitten us rather than the input space. Still to do: separating the keybind
  back out of the cue channel (`Binder.lua:87`'s empty-cue trick), a roster **coverage
  probe** via `GetValidAlertTypes` (Crashing Chaos 417234 is declared but has **zero** CDM
  rows — no combat-readable channel at all), and moving cast-*results* out of State into
  the Coach (deletes ~270 lines and both `SoulShards` hardwires). Phase 2.3 (hoist the
  per-entry GCD read, ~128 redundant calls/tick) and Phase 6 are shippable today.
  - **Revised 2026-07-31 by a Phase-1 design pass**, which did the thing the phase exists for
    and found **five more defects** before a line of it was written — all verified in v0.32.41,
    all filed as `§3.4–§3.8` — **all now fixed in Phase 2 (v0.32.46); this is the diagnosis, the
    plan's §3.11 is the record**: a **SECRET `isKnown` reads as `true`**
    (`State.lua:1363` — a refusal laundered into an assertion, failing in the over-show
    direction field-fix A closed); **`DisplayIdentity` inverts Blizzard's rungs 3 and 4**
    (`Viewers.lua:153-154`, while `liveSpellID` gets the same order right — so the two ladders
    disagree, in the very seam the v0.32.36 bug lived in); one throwing aura read **aborts the
    remaining ids** and condemns the whole row (`State.lua:468`); `readCharge` reports
    `readable = true` on a read it never made (`:394` — the common case *in combat*, where
    `ns.ReadCharges` short-circuits); and `readCd` runs for tab-2 rows, which
    `cooldown-manager.md` §3.2 says structurally cannot carry a cooldown. (§3.4 turned out to
    be **two-sided** once it had a case: a secret `isKnown` reads `true` — over-show — and a
    struct that *answers but omits the field* reads `false`, which is a **drop** — under-show.
    So "we don't know" is only reachable when the whole struct is missing.) The pass also
    **corrected two of the plan's own premises**: `IsInPandemicTime` is not in State's path at
    all (only `AlertTape.lua`), and `isKnown` is an all-or-nothing *struct* axis rather than
    the per-field three-valued one §6.1 was designed around.
    A **sixth** defect, **§3.9**, landed while the cases were being *written*, and is the only
    one already settled empirically: `St.Build` bare-indexes the CDM struct outside any pcall
    while `rawCooldown` pcalls the equivalent access on a table that cleared the same two
    guards — a contradiction, and `H.poison` resolves it in favour of the guard by making
    **`St.Build` throw**. A live crash path, not a stylistic inconsistency; the trigger (does
    the client ever hand us such a table?) stays `@verify-ingame` — the census measured **zero**
    raising fields across 72 cids × 2 trees × in/out of combat, so it is real but unreached.
    Fixed anyway, folded into the same commit as §3.4 since both touch the one struct read.
  - **✅ Phase 1 shipped test-only, with no release cut** (nothing in `tests/` is in the
    `.toc`, so there is nothing to `/reload` and nothing to eyeball — the standing auto-deploy
    exception does not apply, and a cut would tag a no-op into the version history the
    field-fix notes cross-reference). **Phase 2 cut once at the end instead**, as v0.32.46 —
    §3.1 without §3.10 is a regression, so no intermediate build was worth flying. ⚠ `busted`
    **is** a hard
    release gate (`tools/wowkb/addon.py:373-385`), which is why the dual-category hazard is
    encoded `pending` rather than green — green would be flaky, and one flaky case blocks
    every future cut.

- **✅ FIXED 2026-07-31 (v0.32.43) — build caches were tied to the HUD's lifecycle.**
  `knownCache` and `heroCache` were invalidated only from State's **Acquire-gated** event
  frame, so with the HUD **off** a respec left the hero tree holding the previous answer —
  and turning the HUD back on did not clear it, because re-registering an event cannot
  replay the one that was missed. The Coach then gated Destruction's rotation lines on the
  wrong tree, and the decision log's `# config … hero:…` re-stamp reads the same cache, so
  **the trace agreed with the bug instead of exposing it**. `SpecRegistry.lua:55` already
  claimed this was handled; it was not. Worse, `TRAIT_CONFIG_UPDATED` is the only event a
  *hero-tree* swap is guaranteed to fire, and State did not listen for it at all.
  Fix: `St.InvalidateBuildCaches()` + an always-on `cacheFrame`.
  - ⚠ **The harness could not express the bug**, so the first version of the new test passed
    against the unfixed code: `RegisterEvent` was a chainable no-op in `mock_ns`, making
    "State never listens for this event" indistinguishable from "State handles it".
    Registration is now modelled and `Fire` honours it. Mutation-checked. *(Same lesson as
    `issecrettable` hardcoded `false` — see Doctrine.)*

- **✅ FIXED v0.32.47 — `ChargeGained` is a queue drain, not a charge.** Found by the
  v0.32.46 live pass: Conflagrate won **702 of 1272 decisions** and was cued while genuinely
  on cooldown. The napkin's `+1 per ChargeGained` was unsound at the root, and the root is in
  Blizzard's source, not ours. `AddChargeGainedAlertTime(count, time)`
  (`CooldownViewer.lua:591-594`) writes a table **keyed by predicted charge count**; **two**
  producers write it — a *predictor* (`:886`, registering `currentCharges + 1` at a future
  timestamp on every refresh while a recharge runs) and an *observer* (`:992-993`, registering
  the new count at `GetTime()` when the cached count rose) — and
  `ShouldTriggerChargeGainedAlert` (`:596-605`) drains **at most one due entry per call**,
  polled once per frame. A backlog of two therefore fires as two alerts on consecutive frames,
  so **one real restore raises the alert twice**. Measured: a `0 → 1 → 2` climb in **200 ms**,
  plus credits 1.9 s and 4.0 s apart on an ability whose recharge is several seconds.
  Crediting +1 per alert **overcounts**, which is the one direction the napkin's own honesty
  rule forbids — it cues a press that will fail, which is exactly what was felt in play.
  - **The fix is a gain floor**, not a smarter counter. `ns.ReadCharges` now returns
    `cooldownDuration` (the per-charge recharge) as a third value, and a credit inside **half**
    that duration is refused. Half rather than all, because haste and CDR make genuine restores
    land early; the cases it still gets wrong (a true cooldown-reset proc) bias **down**, which
    is allowed. The OOC read is the *only* source for that number — a charged spell's cooldown
    sits on its charge category, so Conflagrate `17962` is `RecoveryTime = 0` /
    `ChargeCategory = 672` and `GetSpellBaseCooldown` yields nothing to count down from.
  - Two non-obvious details: a refusal deliberately does **not** advance `lastGain`, so a burst
    of drains cannot ratchet the window forward and starve a real later gain (trading an
    overcount for an unbounded undercount); and a seed carrying no duration **keeps** the last
    positive one, because `cooldownDuration` reads 0 at full charges — exactly where the OOC
    re-seed usually happens.
  - ⚠ **A test was asserting the bug.** `state_domainview_spec`'s "full loop" fired both gains
    with no clock advance between them — the duplicate shape itself. It now advances a recharge.
    Five new domain-view tests + two fixture cases, mutation-checked by disabling the floor.
  - ⏳ **Needs a live re-fly** to confirm Conflagrate's share of decisions drops and the cue
    stops appearing at zero charges. Nothing else is owed. **Folded into the one owed flight**
    (*Owed: the v0.32.36 re-fly* above) rather than costing its own trip.
- **~~Measure the CDM's frame-cached state in combat — `wasSetFrom*` and `auraDataUnit`.~~
  ✅ DONE 2026-07-31 — measured by the census, and `auraDataUnit` is now CONSUMED.** The
  `/cdmp census` capture answered this as its Q6: both survive combat, exactly as the
  hypothesis below predicted. `auraDataUnit` (plus `item.PandemicIcon`, which the capture
  turned up alongside it) became the **primary channel of the DoT read** in roster-state-plan
  §3.10 / v0.32.46 — the self-clearing channel the pandemic latch could never be. `wasSetFrom*`
  was measured readable but is **not consumed**: the "which source won this refresh" meaning
  axis described below is still an open, and still worth having. The rest of this item is kept
  because that half of it is live, and because the reasoning about *why* these fields are
  readable is the reusable part. The `@verify-ingame` markers in
  `cooldown-manager.md` §7 are discharged.

  <sub>Original text follows.</sub> Two fields Blizzard's **untainted** code derives and
  parks on the item frame:
  - **`item.wasSetFromCharges` / `wasSetFromCooldown` / `wasSetFromAura`** (tab-1 rows
    only) — plain booleans recording **which of the four value sources won this refresh**,
    i.e. what the swipe currently *means*. This is the prize. `CacheCooldownValues` runs
    all four in order and lets later ones **overwrite** earlier ones, so the same dial
    silently switches between *cooldown-remaining*, *charge-recharge* and
    *aura-remaining* mid-fight. Today `State.lua`'s `cd.source` (`live | napkin | none`)
    is a **trust** axis only — how much to believe the number. These flags would give us
    the orthogonal **meaning** axis, observed rather than inferred. A trustworthy number
    whose meaning we guessed wrong is still a wrong cue.
  - **`item.auraDataUnit`** — a plain `"player"` / `"target"` string, the only thing that
    says **which side a bound aura is on**. Nothing in the readable struct carries it, and
    it is exactly the question a DoT row raises. Would also let the pandemic latch key on
    the same fact Blizzard gates its own alert on (`GetAuraDataUnit() == "target"`).

  **Why they might survive combat:** neither is a copied secret. `wasSetFrom*` is set by
  bare assignment (`AddVisualDataSource_*`), and `auraDataUnit` is a literal from
  `scanUnits` — same shape as `item:IsActive()`, which we have **already measured
  readable**. Contrast `cooldownStartTime`/`cooldownDuration`, which are copied straight
  out of `C_Spell.GetSpellCooldown` and therefore inherit its secrecy. So the hypothesis
  is well-founded — but it *is* a hypothesis, and the standing rule applies: **measure
  first, then consume.** An unverified channel must not silently start driving cues.

  **Method:** a targeted read, not a resurrected probe (per the addon `CLAUDE.md` note on
  the retired `/cdmp probe` — add a narrow command, don't rebuild the kitchen sink). Read
  the three flags + `auraDataUnit` per item frame each pulse, `ns.IsSecret`-guarded,
  record OOC and in-combat samples to SavedVariables, `/reload` to flush, then diff the
  two. The existing decision-log extractor is the obvious place to surface it. Worth
  pairing with the **v0.32.36 re-fly** already owed above rather than as its own trip.

- **The napkin's ready-edge precedence — let a genuine cooldown-reset proc through.**
  `State.lua`'s readiness fold returns the napkin's `on-cooldown` verdict **before**
  consulting `readyEdge`. That ordering is deliberate and it wins the just-cast race: right
  after you press something, the observed `Available` edge from the *previous* cycle is
  still latched, and honouring it would flash the ability ready again for a frame.
  But it also means a **genuine mid-cooldown reset proc** is held back for as long as the
  base-cooldown estimate says — the napkin, our only drifting input, outranking a real
  observation. The honest fix is to compare `edge.at` against the napkin record's `start`
  so a **fresh** edge wins and only a **stale** one loses.
  ⚠ **Deliberately deferred from the 2026-07-30 layering pass** (docs-only there — the
  comment at `HudNapkin.lua`'s fence #1 now states the caveat instead of claiming the edge
  always wins). A readiness change would muddy v0.32.37's owed re-fly; land it after.

- **The cue dot should be a CIRCLE.** ✅ **SOLVED — two cuts, and the answer is now a KB
  fact.** The hypothesis list below was right to suspect the mask; the resolution was
  hypothesis 1 in its strongest form.
  - **v0.32.35 (partial):** swapped the masked fill for the `WhiteCircle-RaidBlips` atlas.
    Genuinely round, but it ships a **baked dark outline** (blips must read against a map)
    and `SetVertexColor` *multiplies*, so black stays black — the dot gained a hard edge
    against its own glow instead of blending into it. Round, still wrong.
  - **v0.32.36 (the fix):** a solid `SetColorTexture` fill clipped by a real **MaskTexture
    object** (`CreateMaskTexture` + `AddMaskTexture`) — the idiom
    `RingedFrameTemplate.lua:103-117` actually uses. Borderless by construction: the shape
    comes from the mask's alpha, the colour from our own fill. The mask tracks the fill's
    rect each draw (it does **not** inherit size/position).
  - ✅ **The KB finding this was supposed to produce is written:** `SetMask(path)` +
    `SetColorTexture` **does not clip** — the mask has no effect at all, silently, drawing
    an unmasked rectangle rather than erroring. That settles the interaction
    `addon-dev/frames-textures-animation.md` §5.7 flagged as *uncited at every tier*; the
    measurement and the working idiom are now recorded there. ⚠ It settles **one**
    combination — `SetMask(path)` with `SetTexture`/`SetAtlas` may well work and remains
    `@verify-ingame`.
  - ⏳ **Eyeball still owed:** `/cdmp rt states` on v0.32.36 — is the dot now a clean
    borderless circle that blends into its glow?
- **Fallback cue → PURPLE.** ✅ **SHIPPED v0.32.35** — `ROTATION_FALLBACK` no longer borrows
  ROTATION's green; it resolves its own violet theme entry, pushed off the `SOUL_SHARDS`
  pip hue so it does not read as "resource" at a glance. It stays **static** (no spin), so
  motion remains the primary primary-vs-backup tell and the hue is a second, weaker channel
  rather than a replacement. ⏳ **Eyeball owed on the same `/cdmp rt states` card:** does the
  violet still separate cleanly from the shard pips? The original reasoning follows.
  `ROTATION_FALLBACK` used to borrow ROTATION's green
  (`GLOW_SPEC.ROTATION_FALLBACK.color = "ROTATION"`, `Renderer.lua:77`) and distinguishes
  itself by its ring being **static** rather than spinning — the v0.32.17 "motion, not
  colour" decision. This adds hue back *on top of* motion rather than replacing it: drop the
  `color` override and repoint the theme's `ROTATION_FALLBACK` entry (`:56`, currently a dim
  green marked *superseded, unused*) at a violet. ⚠ **Pick the hue against the shard bar,
  not in isolation:** `SOUL_SHARDS` pips are already violet `{0.690, 0.420, 1.000}` and the
  retired `SEQUENCE` token was `{0.64, 0.42, 1.00}` — near-identical. A fallback cue in that
  exact hue would read as "resource" at a glance, so it wants to be pushed somewhere the
  pips are not (bluer, or darker/more saturated). `/cdmp rt` shows FALLBACK and the bar in
  the same frame, which is the comparison that matters.
- **LATE should read as URGENCY, not as a different instruction.** ✅ **SHIPPED v0.32.36,
  eyeball owed.** LATE is not a different *kind* of press — it is the same press, overdue —
  so it is now the rotation cue **escalated**: ROTATION's green, with a bigger ring spinning
  ~2.5× faster (`ringScale = 5.0`, `spinSecs = 1.6` against defaults 3.6 / 4.0). `GLOW_SPEC`
  grew the two knobs; `setDotGlow` re-times the rotation **only when the value changes**,
  because `SetDuration` on a playing group restarts it and would stutter the ring at 10 Hz.
  - ⚠ **This partly reverses the 2026-07-26 dial-in, deliberately** — the one that pulled
    LATE *off* green onto hot amber because green **shades** were indistinguishable. That
    finding stands and is not being contradicted: this is not a second shade of green, it is
    the *same* green **moving differently**. In play the amber read as a distinct
    *instruction* rather than an urgent one, and it collided with SOON's yellow. The code
    comment carries this reasoning so it is not re-reverted blind. **Do not restore the amber
    without re-testing the motion channel first.**
  - ⏳ **Eyeball owed** (same `/cdmp rt states` card): does LATE now read as an *escalated*
    rotation cue rather than a different instruction?
- **Show the AoE / single-target state on the panel.** `/cdmp single|multi|aoe` sets a mode
  the Coach reads, but the only feedback is a chat line — so mid-pull you cannot tell which
  mode you are in without pressing something. The virtual panel is now the natural home:
  it is ours, always on screen while the HUD is, and (since v0.32.33) has a caption slot and
  real extents. Ingredients are already in hand: `ns.Mode.aoe` is the live flag, State
  forwards it as `pulse.mode` (`"st"` | `"aoe"`), and `HudVirtual.Sync` sees the pulse every
  tick. Open questions for whoever picks it up: **glyph vs word** (a tiny `ST` / `AOE` tag
  reads at a glance; an icon needs learning), **where** (the caption position is taken by the
  unlock affordance — probably the row's left or right edge), and whether it should be
  **quiet in single-target** (show only when AoE is armed, so the default state adds no
  pixels) or always visible so its absence is never ambiguous. ⚠ It must survive a spec with
  **zero** virtual rows — the panel exists there (min-width floor) but has no icons, so the
  tag has to anchor to the root, not to a button.
- **Partial shards (fragments) for Destruction — read power UNMODIFIED.** Today
  `State.lua` reads `UnitPower` in **whole shards**, so the pipeline cannot see a fragment.
  ⚠ **Promoted out of a ✅ item, where it was hiding.** This gap existed only as one
  sentence inside the *shipped* "Warlock Destruction" entry below ("Restoring simc's
  `<= 4.2` / `<= 4.6` still wants the unmodified-power read") — a real hole filed under a
  done heading, which is how it stayed invisible for a month. It is now its own item.
  - **What is correct today and must stay that way:** `SpecPowerDelta` projects **spenders
    only** (CB −2 / RoF −3 / Shadowburn −1) and carries **no `generates` field at all**.
    That was deliberate: Destruction builds in **fragments** (10 per shard) into a bar we
    read in whole shards, so authoring integer yields for fragment builders would make the
    in-flight projection lie by up to a shard per filler cast. Do not "fix" that by adding
    fake `generates` — the fix is to read the real number.
  - **The path is known and is NOT a Secret-Values wall:** `UnitPower(unit, powerType,
    true)` returns the unmodified value in fragments. @verify-ingame — confirm the third
    arg's behaviour for `SoulShards` under 12.0.7, and whether it reads secret in combat
    the way the modified read does *not*.
  - **Why it matters:** the KB's simc distillation gates Destruction lines on **fractional**
    shard thresholds (`<= 4.2`, `<= 4.6`); we currently round them away, so those lines
    fire at the wrong moment. This is rotation *quality*, not correctness — the HUD is not
    wrong today, it is imprecise.
  - **Scope warning:** this touches the Coach's shard gates and `resourceDisplay`. The
    Renderer stays `discrete` (whole pips) unless we decide to render fragments, which is a
    separate design question — a partial-fill pip advertises precision the *display* may not
    want even once the *decision* has it. Do the decision half first.
- **Proc-glow obscures our chrome — subdue or replace it.** ✅ **Shipped v0.32.17 (dim,
  not replace):** `HudProcGlow.lua` post-hooks each CDM item's `RefreshOverlayGlow` and
  sets `item.SpellActivationAlert:SetAlpha(0.5)` while the HUD is on (gated on
  `ns.HudOn()`; restored to full on toggle-off). Frame-level alpha multiplies the whole
  glow without fighting the proc animation. *In-game eyeball still owed:* confirm 0.5 is
  the right level (the `DIM` constant is a dial) — recolor+dim remains available if
  dim-alone isn't enough.
- **Main-choice vs backup-choice distinction is too subtle.** ✅ **Shipped v0.32.17
  (motion, not colour):** every cue now shows a solid circle **+ a spinning glow ring**;
  the winner (`ROTATION`) and softer cues spin+pulse, while the runner-up
  (`ROTATION_FALLBACK`) shows a **static** ring in ROTATION's green — so primary vs backup
  reads by *movement*, not a dim-vs-bright hue. Driven by `GLOW_SPEC` in the Renderer
  (`guidance-contract.json` is authoritative for the `emphasis` set); this was a
  Renderer treatment change, the Guidance already carries the two distinct tokens.
- **Imp napkin count** — a rough running **minimum** Wild-Imp count, in the napkin
  spirit (honest under the Secret-Values wall, where the real `Applications` stack is
  secret). Ingredients: seed an initial count OOC (readable there), then keep a running
  tally off `State.history` (the bounded cast window it already carries — start+succeeded,
  `architecture.md`): **+shards-spent** per Hand of Gul'dan, **−all** on Implosion,
  **−2** on Power Siphon, and **decay** each imp after its lifespan. ⚠ **Lifespan is a
  research sub-task** — the KB has the mechanics (imps are **energy-limited**: they cast
  Fel Firebolt until out of energy; Tyrant **extends every active demon ~15 s**; a
  passive summons one every 12 s) but **no clean seconds figure**; pin it (Wowhead /
  wago / an in-game test) before trusting the decay. Note `State.history` is a **bounded window**,
  so spanning a full imp lifetime likely needs a dedicated accumulator, not just the
  window. Explicitly a *minimum* (secret refunds/procs can only add imps we didn't count).
- **~~`abilities[base].uptime`~~ — ✅ SOLVED DIFFERENTLY, and the field killed the original
  design (field-fix C, 2026-07-30).** The item was "surface a DoT uptime off the TrackedBar
  duration so the Coach can reason about pandemic refresh", and `CoachDestruction` L8 was
  written against a `row.uptime` field it expected State to grow. **That field can never
  arrive:** `pandemicStartTime`/`EndTime` read `SECRET` in combat and `IsInPandemicTime`
  *throws*. What does work is the **edge** — `TriggerAlertEvent(PandemicTime)` fires normally
  — so State latches it (`pulse.dotEdges`) and the brain reads `ctx.dotRefreshable`. That is
  strictly better than the plan: Blizzard derives the window from the duration a recast would
  really carry over, per spell, rather than any lead we could tune. `DOT_REFRESH_LEAD` and
  the speculative `row.uptime` read are deleted. *(A generic buff/DoT **duration** readout —
  seconds on screen — remains unavailable and unbacklogged; the edge covers the decision, not
  the display.)*
  > ⚠ **AMENDED 2026-07-31 — "strictly better than the plan" was wrong, and the capture is
  > what refuted it.** The edge *is* derived from Blizzard's own per-spell pandemic window, so
  > that half stands. But it is a **one-shot notification, not a state**: `TriggerPandemicAlert`
  > sets `nextAvailableTimeToPlayPandemicAlert` so it cannot fire twice for one aura instance,
  > and re-applying a *live* aura raises nothing at all. Measured: **41 Immolate casts → 1
  > `OnAuraApplied`, 1 `PandemicTime`, 0 `OnAuraRemoved`**, and the DoT cue fired for exactly
  > one 5.8 s window in a whole pull. A channel that cannot clear itself is not strictly better
  > than one that reports state; it is a different, weaker thing. **roster-state-plan §3.10
  > fixed it (v0.32.46):** `item.auraDataUnit` + `item.PandemicIcon` are recomputed every frame
  > and therefore self-clear, so they are now channel 1 and the edge is demoted to a fast path.
  > The original item's *conclusion* — that a readable `row.uptime` can never arrive — is still
  > correct; what was wrong was calling the replacement an upgrade.
- **Roll the domain view to other specs** — ✅ **framework complete** (`multispec-plan.md`,
  all 6 phases done 2026-07-29, shipped v0.32.22): registry + resolver + per-spec Coach
  brain + array-of-powers resources + live spec detection, Demo the sole registered spec.
  ✅ **A real 2nd spec landed 2026-07-29: Destruction (267)** — `specs/destruction/` docs +
  `SpecDestruction.lua` + `CoachDestruction.lua` + a 57-test branch oracle, wired through
  `adding-a-spec.md` with **no pipeline edit, no Renderer edit and no contract edit**. The
  recipe held: the only surprises were spec *data* questions, not framework ones. ⏳ The
  framework's own in-game Demo smoke (v0.32.22) is still owed — see Active work above.
- **Warlock Destruction** — ✅ **SHIPPED 2026-07-29** (docs 2026-07-28, code + tests
  2026-07-29). `specs/destruction/` carries the four spec docs; `SpecDestruction.lua` +
  `CoachDestruction.lua` + `tests/spec/coach_destruction_apl_spec.lua` (57 tests) implement
  them. v1 profile **Diabolist**, with the Hellcaller delta handled inline (Wither/
  Malevolence are read *structurally* — a tracked Wither is the hero-tree tell, so there is
  no talent-API branch). How the draft's four open questions actually resolved:
  - **Fragments did NOT force a contract edit.** The draft expected `resourceDisplay` to
    need a segments-with-partial-fill member. It does not: `State.lua`'s `UnitPower` read
    returns whole shards, so a partial-fill enum member would advertise precision we do not
    have. Destruction renders `discrete` on the same `SOUL_SHARDS` token as Demonology —
    which also means it hits **neither** Renderer generalization point. What we did instead:
    `SpecPowerDelta` projects **spenders only** (clean whole numbers: CB −2 / RoF −3 /
    Shadowburn −1) and carries no `generates` field at all, rather than authoring fake
    integer yields for fragment builders. The rounded shard gates in `rotation.md` stand.
    Restoring simc's `<= 4.2` / `<= 4.6` still wants the unmodified-power read.
  - **`dot_refreshable` is half-live, not dead.** The draft assumed L8 could not fire at
    all. It can fire on the *presence* read — the DoT positively reading absent via the
    tracked-aura/buff-item channel — which covers "it fell off". The **pandemic-refresh**
    half is still blocked on `abilities[base].uptime` (above), and the brain already reads
    that field so it needs no edit when it lands. ⚠ The three-way `up`/`missing`/`unknown`
    guard is load-bearing: a *refused* read must never become "the DoT is down", or the HUD
    spams the refresh press every GCD.
  - **The `charge` open item is half-closed** — see Open items above (OOC only; combat-gated).
  - **A NEW open question the draft did not have: what actually means "Art armed"?**
    `observability-map.md` #4 proposes the Diabolic Ritual aura `428514` "and/or the CB
    override edge". Those are not equivalent — `428514` is the ritual **container**, and the
    KB's simc distillation gates the line on a separate `demonic_art` buff. If the container
    is up for most of the cycle, treating it as "Art armed" would jam Chaos Bolt above
    Conflagrate and Summon Infernal permanently. So L3 defaults to **transform-only**
    (`spec.ART_FROM_RITUAL = false`) and the in-game pass decides. One boolean, one place.
  - **Still to do:** the live pass (Open items above). Nothing else is blocking.
- **Four rotations, not one: branch the Coach on `hero × mode`.** The current Destruction
  brain is ONE flat list with two patches (a `mode == "aoe"` gate on Rain of Fire, and
  Malevolence/Wither bolted on for Hellcaller). That under-builds what the KB actually
  documents: `knowledge/classes/warlock/destruction/rotation.md` carries **four distinct
  lists** — {Diabolist, Hellcaller} × {ST, AoE} — and the ST↔AoE difference is a **re-order,
  not a tweak**: Summon Infernal goes #4 → **#1**, Soul Fire #1 → #11, Rain of Fire appears,
  and Conflagrate changes job from "build" to "spread the DoT". No amount of `if aoe` on one
  list expresses that.
  - **The two axes are not alike and should be resolved differently.** Hero tree is
    **stable** (respec-only) — resolve once and cache. Mode is **per-pulse** (the manual
    toggle) — read every tick.
  - ✅ **Hero detection is DONE (field-fix B)** — this axis is no longer blocking. It reads
    `C_ClassTalents.GetActiveHeroTalentSpec()` → SubTreeID (TraitSubTree @ 12.0.7:
    **Hellcaller 58, Diabolist 59**), cached (respec-scoped, invalidated on
    `PLAYER_SPECIALIZATION_CHANGED` **and** `TRAIT_CONFIG_UPDATED`), with a multi-signal
    inference behind it and an announced Diabolist default. `ctx.hero` is ready for the
    dispatch to consume.
  - **Shape:** `RankWinner` dispatches to four small flat cascades with shared line-helpers,
    each diffing by eye against its KB list — rather than one cascade accumulating
    conditionals. Docs drive code here, so `specs/destruction/rotation.md` grows to four
    lists FIRST; then the brain; then 4× branch-oracle coverage.
  - **Do this AFTER the correctness fixes** — four lists are worthless while phantom
    abilities win the rotation and the DoT line cannot fire.
- **Artificial CDM icons — a HUD-owned panel for abilities Blizzard does not track.**
  📄 **PLANNED — `virtual-cdm-plan.md`, and it is the current Active work.** Three phases,
  the key insight being that this is a **decision problem before a drawing one**: the Coach
  cannot even pick Incinerate today, because `RankWinner` gates on `ctx.facts[base]` and an
  untracked ability never enters `state.abilities`. So the unit of work is a **virtual CDM
  entry** (a synthetic domain-view row, fenced four ways) of which the panel is the visible
  half. Binder, Renderer and the contract are all deliberately untouched — if they need
  edits, the seam is wrong.
  Destruction's floor press (Incinerate) has **no CDM icon** (confirmed live 2026-07-30), so
  every cue for it is dropped and the most-pressed button in the spec is invisible.
  ⚠ **Field-fix A raised the stakes here.** An undrawable Incinerate is no longer merely
  invisible — it is now *excluded from the decision entirely*, so at low shards Destruction
  has no floor and the Coach honestly returns no press (`w:-`). That is correct behaviour and
  a worse user experience than before; this item is what fixes it properly.
  Demonology has the same hole at Shadow Bolt. Rather than fighting the tracked set, the HUD
  draws **its own icon** for such abilities on a small repositionable panel it owns, and
  registers it into the Layout as a synthetic entry so the Binder and Renderer treat it like
  any other target.
  - ✅ **DELIVERED.** The first 2026-07-30 pass quantified the cost — `w:-` on **31 %** of
    decision changes (59 of 191), every one at 0–2 shards — and the second pass, after the
    panel shipped, measured **0.0 %** across 265 Hellcaller decisions with Incinerate drawn
    50 times and zero Binder drops. The Diabolist half took a further fix (v0.32.36, the
    display-identity bug) and is awaiting its re-fly.
  - **Why this may beat the curated-layout override** (the other parked option): no
    enforcement UX at all. The curated layout has an unresolved "auto-apply → import-and-
    verify → nag" question and breaks if the player customises their layout; a panel we own
    is unconditional and survives any layout the player chooses.
  - **Design tension to settle first:** `design.md` pillar 1 is *enhance, don't replace* —
    Blizzard's icons stay native and untouched. An artificial icon is **ours**. The
    defensible line is that it is **additive only** — it exists solely for abilities
    Blizzard displays nowhere, so nothing is being replaced or re-skinned.
  - ✅ **There may be no need to synthesise a handle at all (2026-07-30).** Incinerate
    `29722` is not in `CooldownSetSpell` for any set, but Destruction's set 884 carries
    **Shadow Bolt `686` at `cid 66181`, Essential, OrderIndex 0**, and the client overrides
    that entry's display to Incinerate (which is why the settings panel shows an Incinerate
    tooltip on a greyed icon). It reads `isKnown = false`, so Blizzard never creates a frame
    — but it is a **real cooldownID whose live identity already resolves to Incinerate**.
    Start there rather than inventing synthetic handles.
  - **Pieces:** icon texture off the spellID, a saved position, keybind via the existing
    `HudBinds` base-spellID lookup, and synthetic Layout/registry handles that do not
    collide with real cooldownIDs.
- **"Branch fallback" — say WHY we cannot decide, instead of always offering a runner-up.**
  Today the Coach always computes a second place and shows it whenever castable. That is
  naive: it presents a confident-looking alternative even when the real situation is *"we
  genuinely cannot tell what to press from what we can read."* Three concrete cases:
  waiting on a stack count that is secret (Backdraft 1-vs-2, Wild Imps for Implosion);
  holding a cooldown for encounter timing the HUD cannot know (pool shards and delay
  Infernal for incoming adds); and two lines that are genuinely tied under our information.
  - **This partially reverses a settled decision.** `guidance-contract.json` RETIRED the
    `JUDGE` emphasis in W4 Phase 8 on the reasoning that "the runner-up now carries the
    uncertainty the hedge used to." Field use says the runner-up carries the *choice* but
    not the *reason*. Reviving an explicit "your call, because X" token is a **contract
    change**, so it wants a contract edit, not just a Coach edit.
  - **Half the machinery already exists and is dormant:** the spec bucket carries
    `judgeable = false` + `secretGate` (Havoc and Implosion both declare one) and **nothing
    reads them today**. This feature is what those fields were designed for.
  - This is "inform, don't instruct" made mechanical — the same doctrine that caps an
    unreadable gate at AVAILABLE rather than faking a call.
  - ⚠ **The dead JUDGE render path was removed on 2026-07-30** (theme entry, both fixtures,
    their tests). That is not an obstacle: a revival arrives through `guidance-contract.json`
    as a contract change with a **fresh treatment decision** anyway, and git history holds
    the old RGBA. Keeping a dead render path alive on the chance of a revival is exactly the
    archaeology that pass existed to remove.
- **Consolidate the report commands into one sectioned dump.** `/cdmp hud status`,
  `/cdmp hud layout`, `/cdmp alerts probe|dump` are four chat-only, point-in-time reports.
  Chat has no copy/paste, so every one of them is hard to get off the client — the flaw
  that made the first AlertTape cut useless. Replace with a **single `/cdmp dump`** that
  writes a sectioned snapshot to SavedVariables (`wowkb.cdmp dump` flattens it), printing
  only a short receipt in chat. Split by **data shape, not topic**: *actions*
  (`hud on/off`, `alerts on/off`, `reset`, mode) stay verbs; *snapshots* merge; *recorders*
  (`decisionlog`, `alerttape`) stay separate because their lifetimes differ — one is
  permanent, one is scheduled for deletion, and merging would make the temporary one hard
  to remove.
  ⚠ **This is what `/cdmp probe` was, and why it died.** The probe was ONE function with
  hardcoded sections, so nobody could safely prune it and it only grew. The difference has
  to be structural: a **section registry** (`ns.RegisterDump(name, fn)`, mirroring
  `ns.RegisterCommand`) where each module owns its own section — so deleting `AlertTape.lua`
  removes its section with it, with no edit to a central function. Two rules to bake in:
  file is the record / chat is the receipt, and a section that cannot read its subject
  emits `<unavailable: reason>` rather than nothing.
- **Coach rotation logic** — any real rotation-quality tuning (the cutover was
  behaviour-preserving; the flat priority list is the place to iterate).
- **Layer-① curated Cooldown Layout override (deferred).** v1 ships no profile and binds
  by `GetCooldownID()` to the active layout (`design.md` pillar 1). If the DB2 defaults
  prove insufficient — the noisy Utility default, or the per-stage Diabolic Ritual auras a
  predictive Art tracker needs (only the `428514` container is tracked today) — this
  returns as a curated layout string, where enforcement strength (auto-apply →
  import-and-verify → nag) becomes the UX question. Binding-by-ID gives determinism
  without it, so it stays parked until a concrete need forces it.

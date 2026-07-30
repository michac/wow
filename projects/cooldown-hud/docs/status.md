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
  (**353 tests** — 141 pipeline/Demonology + 89 Destruction branch oracle + 11 `viewers_spec`
  + 73 `state_domainview_spec` + 39 `hudvirtual_spec`).
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
- **Active work: `virtual-cdm-plan.md` — the virtual CDM panel. ✅ Phase 1 SHIPPED + FLOWN
  (v0.32.32). ✅ Phase 1b + Phase 2 BUILT (v0.32.33) — awaiting the two-hero-tree in-game
  pass.** The HUD draws its own icons for the abilities Blizzard's Cooldown Manager will
  not display, so a spec's floor press stops being invisible.
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
  - ⏳ **The in-game pass this needs:** a dummy pull on **both** hero trees — Diabolist
    (exactly one Incinerate icon, Blizzard's; `686` present in `abilities`, no virtual row)
    and Hellcaller (exactly one, ours; `w:-` still 0 %, no `×`) — plus drag → `/reload` →
    the panel comes back where you left it. L12 Infernal Bolt is still unexercised.
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
  - ⚠ **Follow-up: `design.md` still describes the product as a CDM overlay.** It is now
    "a rotation helper that displays on the CDM when it can, and on its own icons when it
    cannot". Worth a pass before Phase 2 dials in the visual line.
- ⚠ **The finding that set the agenda: 31 % of decisions have no winner.** 59 of 191 decision
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
  `PandemicTime` — and cost four code fixes. **Still open on this spec:** `ART_FROM_RITUAL`
  (never observed, because no Ruination transform appeared in the capture) and which Art
  override ids actually surface; both are in *Open items* below.
- The **multi-spec refactor is complete**
  (`multispec-plan.md`, all 6 phases done 2026-07-29, shipped v0.32.22). The framework is
  one spec-agnostic pipeline + a per-spec brain that plugs in: registry + resolver
  (`SpecRegistry.lua`), per-spec Coach brain (`CoachDemonology.lua`), array-of-powers
  resources (`resourceBars[]` + N stacked meters), the decision-log seam (`DecisionLog`),
  and live spec detection (login + `PLAYER_SPECIALIZATION_CHANGED`, registered-or-passive).
  Phase 6 (docs) synced `architecture.md`/`notes.md`/addon `CLAUDE.md` to the code; the
  contract needed no edit. **Destruction is the proof the seam works** — it was added as a
  pure sibling (two Lua files, a `.toc` line pair, a test) with zero pipeline edits, which
  is what the refactor was for. **⏳ One follow-up owed: the in-game Demo smoke on v0.32.22**
  (deferred — no game access at completion; the checklist is in `multispec-plan.md`'s
  Phase-6 row / Verification, and mirrors the "In-game verification of the pipeline output"
  open item below).

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
  the decision log gained a **`CH:`** field, so the next pull should show `CH:Conf~n/2` lines
  tracking the real count — **read them and confirm the napkin never over-counts.**
  ⚠ Shadowburn has **no** charges (DB2 `ChargeCategory = 0`), so it is not a consumer.
- **Destruction in-game confirmation** (the `adding-a-spec.md` Step-8/10 pass) — **mostly
  ANSWERED by the 2026-07-30 pass; items 3 and 4 remain.**
  1. ~~`/cdmp hud status` → `spec: Destruction (profile active)`.~~ ✅ the pipeline ran and
     the Destruction brain drove it for a full pull.
  2. ~~`/cdmp hud layout` → **does Incinerate appear?**~~ ✅ **ANSWERED 2026-07-30: NO.** The
     live Essential set is 9 entries and Incinerate, Soul Fire, Havoc and Channel Demonfire
     are all absent. So the floor press has no icon *and* the Infernal Bolt transform is
     blind. Field-fix A stops that corrupting the *decision* (an undrawable row no longer
     wins the list); it does **not** make Incinerate visible — that is the *artificial CDM
     icons* item below, which this answer promotes from speculative to concrete.
  3. ⏳ **Is the Diabolic Ritual container (`428514`) a usable "Art armed" signal?** **Still
     open, and this pass could not answer it** — the character is Hellcaller, so no Demonic
     Art exists to observe. Needs a Diabolist pull. `spec.ART_FROM_RITUAL` stays `false`.
  4. ⏳ **Do the Art override IDs resolve to `433885` / `433891`?** Same: unanswerable on a
     Hellcaller build. Both pairs stay mapped. *(The set-884 dump does list both `433885` and
     `433891` at cids `171413`/`171412`, so the Destruction-side pair is at least the one the
     data carries.)*
  5. Respec in and out: the HUD toggles between active and passive with no stale cue.
  6. ~~Dummy pull → `wowkb.cdmp decisionlog`, grep `w:-` / `×`.~~ ✅ **DONE.** `×` is **zero**
     on the fixed build (the only two in the capture are in the pre-fix session, both
     `SF:ROT×`); `DR:` is stable and every dropped row checks out by name; `w:-` at 0–2
     shards is the untracked-Incinerate signature, quantified at **31 %** of decisions —
     which is what promoted the virtual CDM panel to Active work.

## Improvements / backlog

The container for what's next. The old engine is gone, so this is where feature/quality
work lands now — the user drives the list; a few already-surfaced items are seeded:

- **The cue dot should be a CIRCLE — find out why it isn't reading as one.** Observed in
  play (2026-07-30): the cue reads as a square next to its own glow, which is round. ⚠ The
  code already *intends* a disc — `Renderer.lua:216-224` creates the dot as a `WHITE8X8`
  fill and calls `SetMask("Interface\CharacterFrame\TempPortraitAlphaMask")` once at
  creation, Blizzard's own solid-fill→circle idiom (`RingedFrameTemplate.lua:103-117`). So
  this is **not "add a mask"; it is "the mask is not taking effect"**, and the fix depends
  on which of these it is:
  1. **The mask is lost by `SetColorTexture`.** It is applied once at creation, but
     `:226` calls `SetColorTexture` on *every* redraw. `addon-dev/frames-textures-animation.md`
     §5.7 says `SetMask` is orthogonal to the base-image writers and should survive —
     but that same file flags "exactly one is in force" as **uncited at every tier**, so
     the interaction is not actually pinned. Cheapest probe: move the `SetMask` call to
     after the `SetColorTexture`, i.e. re-apply per draw, and see if the corners go.
  2. **The mask never applied at all** — wrong path for 12.0.x, or the mask needs a
     `SetSize` before it (the dot is sized at `:227`, *after* creation).
  3. **It is a circle and 12 px is just too small to read as one.** Then the answer is
     size/AA, not masking.
  Settle it with `/cdmp rt` (the `states` card draws all five at once, over real icon art)
  before changing anything — and whatever it turns out to be, write the answer back into
  `addon-dev/frames-textures-animation.md`, since §5.7's mask/base-writer interaction is
  exactly the open question this would close.
- **Fallback cue → PURPLE.** `ROTATION_FALLBACK` currently borrows ROTATION's green
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
  - ⚠ **The 2026-07-30 live pass quantified the cost: `w:-` on 31 % of decision changes**
    (59 of 191), every one at 0–2 shards. Field-fix A stopped an undrawable Incinerate
    corrupting the decision; the consequence is that below Chaos Bolt's 2-shard cost the list
    has no floor at all and the HUD shows nothing. **This is now the highest-value open item
    for Destruction.**
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

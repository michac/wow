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
  (see `architecture.md` → "Live wiring"). `/cdmp hud2` is a transitional alias. The old
  HudChrome/HudBoard/HudScore engine + the opener/burst/pane widgets were **deleted at
  the W4 cutover**; the pipeline is the sole engine.
- **Registered specs: Demonology (266) and Destruction (267).** Both plug into the one
  spec-agnostic pipeline: `Spec<Name>.lua` (data) + `Coach<Name>.lua` (the rotation brain).
  Every other spec resolves passive by design. Demonology is play-settled; **Destruction is
  code-complete but not yet flown** — see the Destruction item below.
- **Instrument:** the **decision log** — `CDMProbeDB.decisionlog`, one `S{…} G{…} B{…}`
  line per pipeline decision change, extracted by `wowkb.cdmp decisionlog` (`hud2log` is a
  back-compat alias). The old-engine `statelog`/`pulls` recorders were retired at the
  cutover; the `/cdmp probe` + `probe-baseline.json` assertion suite was retired 2026-07-29
  (settled readability rules + DB2-sourced tracked set made per-spec re-measurement moot).
- **Gates:** `luaparser` (release) + `luacheck CDMProbe/` + `busted CDMProbe/tests/spec`
  (**209 tests** — 141 pipeline/Demonology + 57 Destruction branch oracle + 11 `viewers_spec`).
  ⚠ All three are **source** gates: none of them runs the game, and the v0.32.25 outage
  below is what that blind spot looks like in practice.
- **Active work: `field-fixes-plan.md` — Phase A (not started).** Four phases (A/B/C/C2)
  fixing what the **first live session** found once the HUD actually rendered: phantom
  unlearned/undisplayable abilities winning the rotation (216 dropped Soul Fire cues), the
  DoT keyed on the wrong Immolate id, hero detection inferring the wrong tree, and the
  pandemic + charge signals now known to be **edge-readable but state-secret**. Gates:
  luacheck + the 209 busted tests stay green; one release at the end of C2. The `hero × mode`
  rotation split is deliberately **out of scope** — see Improvements below.
- **Destruction Warlock — code shipped, in-game confirmation owed.**
  `SpecDestruction.lua` + `CoachDestruction.lua` implement `specs/destruction/rotation.md`
  L1–L13 through the `adding-a-spec.md` recipe (no pipeline edits, no Renderer edits, no
  contract edit). Gates green. **What is owed is the live pass** — the tracked set is still
  DB2-predicted, so run the Step-8/10 checklist under *Open items* below on a real
  Destruction character. Two answers there feed straight back into the code: whether
  Incinerate is tracked, and whether the Diabolic Ritual container is a usable "Art armed"
  signal (`ART_FROM_RITUAL`).
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
- **`charge` half of the full-database read** — **half-closed by Destruction.** Conflagrate
  and Shadowburn are the project's first charged tracked abilities, and
  `CoachDestruction`'s `chargeBanked()` now consumes `abilities[base].charge`: an ability
  with a charge banked reads usable even while its recharge timer runs. But `ns.ReadCharges`
  is **combat-gated** (`C_Spell.GetSpellCharges` reads secret in restricted combat), so this
  only bites **out of combat**; in a pull both abilities degrade to binary off-cooldown and
  the list under-presses rather than dumping a second charge. Still `@verify-ingame`: confirm
  the OOC read populates and that the in-combat refusal is the whole story (i.e. that there
  is no readable charge channel we are missing). See `architecture.md` open Qs.
- **Destruction in-game confirmation** (the `adding-a-spec.md` Step-8/10 pass — the code is
  shipped, this is what it is waiting on). On a real Destruction character:
  1. `/cdmp hud status` → `spec: Destruction (profile active)`.
  2. `/cdmp hud layout` → **does Incinerate appear?** The whole tracked set is DB2-predicted
     and Incinerate is absent from the union entirely. If it is genuinely untracked, the
     floor press has no icon *and* the Infernal Bolt transform is blind — which is the
     concrete need that un-parks the curated layout override at the bottom of this file.
  3. **Is the Diabolic Ritual container (`428514`) a usable "Art armed" signal?** If it is
     up most of the cycle it is not, and `spec.ART_FROM_RITUAL` stays `false` (today's
     default, so L3 fires only on a visible Ruination transform). If it tracks the Art
     honestly, flip that one boolean.
  4. **Do the Art override IDs resolve to `433885` / `433891`** (the Destruction-side
     residue) rather than Demo's confirmed `434635` / `434506`? Both pairs are mapped, so
     either works — the point is to record which.
  5. Respec in and out: the HUD toggles between active and passive with no stale cue.
  6. Dummy pull, then `wowkb.cdmp decisionlog` and grep for `w:-` (no winner) / `×`
     (dropped cue) — `w:-` at low shards is the expected signature of an untracked
     Incinerate, not a bug.

## Improvements / backlog

The container for what's next. The old engine is gone, so this is where feature/quality
work lands now — the user drives the list; a few already-surfaced items are seeded:

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
- **`abilities[base].uptime`** — surface a buff/DoT uptime off the TrackedBar duration in
  the domain view, so the Coach can reason about "keep this up" abilities. **Now has a
  waiting consumer:** `CoachDestruction`'s L8 reads `abilities[base].uptime` already, so the
  day State populates it the DoT **pandemic-refresh** half comes alive with no brain edit.
  Until then L8 fires only on the *presence* read — the DoT positively reading absent — which
  covers "it fell off" but not "refresh it early". This is the single highest-value
  outstanding item for Destruction: DoT maintenance is the spec's spine.
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
  - ⚠ **Detect hero properly.** Today it is inferred structurally ("a tracked Wither means
    Hellcaller"), and that has already been observed WRONG in the field — a live Hellcaller
    build tracked Malevolence but Immolate, so the inference picked Diabolist. Look for a
    real hero-talent API (`C_ClassTalents` / `TraitSubTree`) before inferring from the
    tracked set again.
  - **Shape:** `RankWinner` dispatches to four small flat cascades with shared line-helpers,
    each diffing by eye against its KB list — rather than one cascade accumulating
    conditionals. Docs drive code here, so `specs/destruction/rotation.md` grows to four
    lists FIRST; then the brain; then 4× branch-oracle coverage.
  - **Do this AFTER the correctness fixes** — four lists are worthless while phantom
    abilities win the rotation and the DoT line cannot fire.
- **Artificial CDM icons — a HUD-owned panel for abilities Blizzard does not track.**
  Destruction's floor press (Incinerate) has **no CDM icon** (confirmed live 2026-07-30), so
  every cue for it is dropped and the most-pressed button in the spec is invisible.
  Demonology has the same hole at Shadow Bolt. Rather than fighting the tracked set, the HUD
  draws **its own icon** for such abilities on a small repositionable panel it owns, and
  registers it into the Layout as a synthetic entry so the Binder and Renderer treat it like
  any other target.
  - **Why this may beat the curated-layout override** (the other parked option): no
    enforcement UX at all. The curated layout has an unresolved "auto-apply → import-and-
    verify → nag" question and breaks if the player customises their layout; a panel we own
    is unconditional and survives any layout the player chooses.
  - **Design tension to settle first:** `design.md` pillar 1 is *enhance, don't replace* —
    Blizzard's icons stay native and untouched. An artificial icon is **ours**. The
    defensible line is that it is **additive only** — it exists solely for abilities
    Blizzard displays nowhere, so nothing is being replaced or re-skinned.
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

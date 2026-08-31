# Plan — cap's CDM row becomes a 6×2 panel EllesmereUI can move

**Status: an approved plan, not an authority.** A temporary migration artifact in the sense
`CLAUDE.md` gives that phrase, alongside `simplification-plan.md`. As each phase lands its
outcome goes to `backlog.md` → `## Status` and its promises to `spec.md`; this file is deleted
when the last one does.

Client facts cited below belong in `knowledge/addon-dev/`, where the KB's gates apply — this
plan is not their home, and step 34 is what moves them.

---

## Context

**The goal is to anchor EllesmereUI's power bars and cast bar to cap's CDM row.** That needs the
row to be a frame with a stable, honest rect a mover can address.

`/cap` re-anchors the Essential Cooldown Manager viewer's item frames into its catalog's authored
order. It used to do that onto a nameless 1×1 `UIParent` child whose position was re-derived from
Blizzard's measured geometry on every pass — so the row had no position of its own and nothing
could be anchored to it. **Phases 0 and 1 fixed that and are shipped.** The row is now
`CombatAssistPlusRow`, a named 6×2 panel with a saved per-character position.

**Nothing has been flown.** Five releases went out on 2026-08-31 (v0.15.0 → v0.18.1), all
deployed via `ghaddons`, none yet run in a client. **One flight covers all of them** — it is the
single outstanding gate, and it is what the next session should start with.

⚠ **What is BUILT is recorded in `projects/combat-assist/specs/backlog.md` → `## Status`**, in
detail, and is deliberately not restated here. This file is the forward plan; that one is the
record.

---

## Status

| | | Ships as | State |
| --- | --- | --- | --- |
| **Phase 0** | Stand down beside another CDM rider | v0.15.0 | built, **unflown** |
| **Phase 1** | The named 6×2 panel, `/cap move`, `Place.lua` | v0.16.0 | built, **unflown** |
| — | **Principle (c)**: no order ⇒ cap draws nothing | v0.17.0 | built, **unflown** |
| — | Placement per-character; opinions per-account | v0.18.0 | built, **unflown** |
| — | Rescale no longer moves the panel | v0.18.1 | built, **unflown** |
| — | **cap owns the icon size**, not Edit Mode | v0.19.0 | built, **unflown** |
| — | One icon-size knob: client nominal split, virtual row derived | v0.19.1 | built, **unflown** |
| **Phase 2** | Two rows | — | **next**, after the flight |
| **Phase 3** | EllesmereUI mover registration | — | the actual goal |
| **Phase 4** | Reading model, only if two rows carry a scan claim | — | needs a product decision |
| **Phase 5** | Scale-to-fit resize; `RegisterSkin` | — | parked, deliberately |

⚠ **Step 7 changed meaning on 2026-08-31 and the row above it is why.** The old step asked
whether the panel *moved* when Blizzard's icon-size slider changed — a question that only made
sense while cap followed that slider. It never did answer cleanly: at the default position the
error is `0 x anything = 0` horizontally and reads as growth vertically, so the test was close to
unfalsifiable. The premise was then examined and found never to have been decided — it arrived
inside the Phase 1 commit as an implementation default and `spec.md` never stated it. **Authority
is inverted: cap declares the icon size, the CDM's frames are scaled to fit it** (`spec.md` §3.9,
eighth property; `row.icon_px` in `render-tokens.json`). The v0.18.1 fix is kept as a guard but is
no longer load-bearing, and the step now asks a question with a crisp answer.

The four middle rows were **not in the original plan**. They came out of the session and two of
them are corrections to Phases 0–1, not additions:

- **Principle (c)** — `spec.md` §1 gained a third principle: the order and the augments are one
  product. Measured first: *nothing outside `Anchor.lua` consulted ordering at all*, so
  `/cap anchor off` and the rider stand-down both drew the full overlay onto a row in Blizzard's
  arbitrary saved order. Enforced in one place, `Sense.Verdicts`.
- **Per-character placement** — Phase 1 made `placed` load-bearing, and it was one account-wide
  boolean, so only the first character to ever arm would seed its row. A regression Phase 1
  introduced; `CombatAssistPlusCharDB` closes it.
- **The rescale jump** — `resizeAnchor` set the panel's scale without re-applying its position.
  Found by trying to write the flight procedure down, not by a test.

---

## THE FLIGHT — the one outstanding gate

Everything above is behind this. Run it before Phase 2. A defect is fixed forward with a patch
bump, not unpicked.

The two acceptance sets do not confound each other **by construction**: with EllesmereUI's CDM
module on, cap orders nothing, so there is no panel behaviour to observe; with it off there is no
rider. The only shared observation is "ordering arms".

| # | Do | Expect |
| --- | --- | --- |
| 1 | EUI Cooldown Manager module **on**, `/reload` | Single-OK modal; **no overlay at all**; `/cap status` says `DARK — NOT ORDERING` naming the rider |
| 2 | `/reload` again | Modal returns — it is deliberately not persisted |
| 3 | Module **off**, `/reload` | No modal; ordering arms; overlay draws |
| 4 | `/cap move`, drag the row, `/cap move` to lock, `/reload` | Unlocks **two** frames; row is where you left it |
| 5 | `/cap anchor off` → `on` | Overlay vanishes, then comes back |
| 6 | Spec swap, `/reload` | Panel has not drifted; icons evenly spaced |
| 7 | Ordering **on**, then nudge Edit Mode's CDM icon-size slider | **Nothing about cap's row changes** — not its size, not its position, not the icons in it. cap owns the size now |
| 7b | `/cap anchor off` after step 7 | The row returns to Blizzard's order **and to the slider's size** — `disarm` owes both back |
| 8 | Second character whose CDM sits elsewhere | Its row seeds to **its own** CDM, not the first character's |

⚠ **Not reachable by any of these:** the re-entry depth guard in `onFramePoint`. It only fires if
a rider claims the row *after* cap armed. It stays unexercised until it isn't.

⚠ **Dropped from the earlier list, deliberately.** "Panel does not resize below the cell floor" is
not observable in-game — the floor is `max(cell_px, cell_floor_px)`, a guard against a bad
`render-tokens.json` edit. And "does the panel grow about its centre or its top-left on an
icon-size change" was withdrawn as premature: under Phase 5's scale-to-fit the question stops
existing, so it should not be adjudicated now.

---

## How to run this plan

**Stop at the end of every phase and wait.** Each phase ends with a `PAUSE` naming what should be
true before the next starts. Do not begin a phase because the previous one compiled — begin it
because the pause condition was checked.

⚠ **Releasing is no longer ask-first** (changed 2026-08-31). The standing authorization and its
three gates live in `projects/combat-assist/CLAUDE.md` § Releasing. The gate that matters here:
**the grant retires *may I release?*, never *did the last flight pass?*** Cutting a release
begins a flight; it does not end one.

Before touching the addon checkout: `uv run python -m wowkb.addon pull --all` from `tools/`.
Every release note must say **what it has not exercised** — that is the flight request.

---

## Corrections this session made to the original plan

Carry these forward; they are why the phases below differ from the first draft.

1. **Step 12's `50 × iconScale` cell double-counts.** `SetScale` does not change what `GetWidth`
   returns, so an item frame reads **50** wide at every icon-size setting — the setting appears
   only in `GetEffectiveScale`, which the panel already matches. Every length in `tokens.row` is
   in the panel's own coordinate space. `anchor_spec` asserts the grid does not vary with
   `iconScale`, so this cannot come back quietly.
2. **Step 20 landed in Phase 1, not Phase 2.** Once pitch came from tokens, `metrics()`'s gap
   derivation was already dead. `metrics()` is now `origin()` and returns only the seed corner;
   `DEFAULT_GAP` is gone. Blizzard's real padding is `iconPadding + GetAdditionalPaddingOffset()`
   = 5 + (−4) = **1**.
3. **The whole `P.foreign` origin-adoption path had to go**, which the plan did not enumerate.
   Following the CDM's placement is exactly what a row with a saved position must not do. This is
   a **behaviour change**, recorded in `spec.md` §3.9: an Edit Mode move of the viewer no longer
   drags cap's row.
4. **Step 7 is dropped.** Read back plainly it was: ask the busy maintainer of a top-tier addon
   to support an unreleased one-user addon. Its premise was also wrong — `SKINNING_API.md`
   documents `RegisterSkin` and never mentions conflicts. Revisit only if cap ever has a public
   release. `_G._CAP_IsOrderingEnabled` is published anyway; it costs one line.
5. **Phase 1 chose `Place.lua` over parameterising `Frame.lua` in place**, because `Anchor.lua`
   loads before `Frame.lua`. Both frames register with it. It takes `Window.lua`'s keying and
   `Frame.lua`'s scale arithmetic — `Window.lua`'s own maths is unusable here, as it may skip
   normalisation only because a window is never scaled.

---

## Phase 2 — Two rows

All citations re-resolved against the post-Phase-1 file (`Anchor.lua` is now 1260 lines).

15. Add an authored **`break_before = "<entry id>"` per catalog** — one break point, named once,
    which is what makes step 16's fallthrough rule read naturally. Validated by `Catalog.Check`
    (`Catalog.lua:183`) at **top level**, beside the existing `bar must name one enhanced entry`
    check at `Catalog.lua:586`, since it is a catalog-level key naming an entry rather than an
    entry-shape rule. Refuse an id that is not declared, and refuse the first entry.
    *(A per-entry `break_before = true` boolean is the alternative and would validate in the
    entry-shape loop after `Catalog.lua:245-247`. The catalog-level form was the original
    decision; do not change it without a reason.)*
16. A break entry that is not talented falls through to the next present entry in authored order.
    `Catalog.Resolve` (`Catalog.lua:600`) is what knows which entries resolved to a row.
17. Teach `apply()` the second axis. The whole placement loop is `Anchor.lua:662-668`, and it is
    single-axis in exactly two places: `local x = (i - 1) * pitch` at **:663** and the hardcoded
    `y = 0` in the `want` table at **:664**. Pitch is already token-derived (`:656-657`). Entries
    before the break to row 0, the rest to row 1, **left-aligned in both**, so the scan's starting
    x never moves with roster length.
18. `Catalog.Check` fails a catalog whose live roster cannot fit twelve cells.
    ⚠ **This is immediately load-bearing, not theoretical: Havoc authors exactly 12 entries** —
    `vengeful_retreat · metamorphosis · the_hunt · eye_beam · essence_break · blade_dance ·
    immolation_aura · chaos_strike · felblade · demons_bite · fel_rush · throw_glaive`. Zero
    headroom. Demonology, Protection and Retribution are at 9; Devourer 7; Destruction 1.
19. **Fix `Anchor.Drawn()`** (`Anchor.lua:467-485`) to sort by `(top, left)` rather than `left`
    alone. The comparator is `Anchor.lua:475-478` and is purely one-dimensional — two rows would
    column-interleave and every capture would read `X{MISMATCH}` forever.
20. ~~Delete `metrics()`'s gap derivation~~ — **done in Phase 1**, see correction 2.
21. Add a row-break token to the **anchor** stream's wire. `Anchor.Render` is `Anchor.lua:120-143`
    and emits `A{} P{} D{} X{} S{}` at `:138-142`; `P{}`/`D{}` are cooldownID orders built by the
    `list()` helper at `:112-117`. Document it in `specs/flight-reading.md` — ⚠ that file
    describes **two** different `P{}`/`D{}` groups and only the second is this one:
    - `## Draw surface`, **lines 135–183** — `P{}` there is `id:scan[+cue,…]`, a per-entry
      treatment, and its `D{}` is a counts group. **Not this.**
    - `## Anchor order`, **lines 185–267** — the orders. The defining bullet is **213–215**;
      `X{STALE:<n>}` precedence at 216–219. Note :214 states the `GetLeft()` assumption that
      step 19 is changing.

**PAUSE.** A capture (`wowkb.capture cap anchor`) shows the authored two-row order drawn correctly
with `X{}` reporting a match, across a talent change that removes the break entry.

---

## Phase 3 — EllesmereUI — **the actual goal**

⚠ **The mined clone is GONE and that is correct.** `raw/addon-research/ELLESMEREUI-REMOVED.md`
records it: deleted per the `mine-addon` skill because EllesmereUI is All Rights Reserved and the
KB carries the facts. Re-clone recipe is in that note (tag v8.7.5, commit `c4eba58`) **but you
should not need it** — the citations below came from the **live install**, which is still readable
at `…/_retail_/Interface/AddOns/EllesmereUI/EUI_UnlockMode.lua`, currently **9.0.8**, and carries
the whole mover API. ⚠ A live install is updatable, so its line numbers are volatile in a way a
pinned clone's are not: **re-resolve by symbol before relying on any number here.**

22. Add `Ellesmere.lua`, loaded after `Anchor.lua`, entirely behind
    `if EllesmereUI and EllesmereUI.RegisterUnlockElements`. Add `## OptionalDeps: EllesmereUI`
    to the `.toc` so the base addon loads first.
23. Register one element via `EllesmereUI.MakeUnlockElement`:
    - Registration is a **colon** call taking an **array** — `EllesmereUI:RegisterUnlockElements({elem}, "cap")`; it uses `self`.
    - `getSize` is **effectively required**: it feeds mover geometry and the cog's Width/Height
      boxes. Without it plus `noResize = true` the cog shows size inputs that silently do nothing.
    - `key` is a single global namespace across every addon — prefix it (`CAP_ROW`).
    - `getFrame` side-effect-free. `isHidden` is called with **no arguments**; return true whenever
      `Anchor.Ordering()` is false — which after principle (c) is exactly when cap draws nothing.
    - `noResize = true`; `noAnchorTarget` and `noAnchorTo` both omitted — that is what lets the
      power bars anchor to us.
24. Point `savePos` / `loadPos` / `clearPos` / `applyPos` at **Phase 1's `Place` store**, which is
    why Phase 1 was a prerequisite. Mandatory, and proven: `SaveBarPosition`/`LoadBarPosition`/
    `ClearBarPosition` delegate to the element's own functions and fall through to
    `GetPositionDB()` only when no element is registered — and that fallback is the
    EllesmereUIActionBars profile table, `nil` in the base addon. Omit them and drags are silently
    lost. Expected shape from `loadPos` is `{point, relPoint, x, y}`, canonically `CENTER`/`CENTER`
    with offsets from UIParent's centre — **already `Place`'s convention**, so it fits without
    translation.
25. Call `EllesmereUI.NotifyElementResized(key)` (**dot** call) when the panel's size changes
    *without* a real `SetSize` on the registered frame. EUI installs its own `OnSizeChanged` hook,
    so a genuine resize notifies itself. In practice this is `resizeAnchor` (`Anchor.lua`).
26. Register at `PLAYER_LOGIN` + `C_Timer.After(0.5, …)`, then call
    `EllesmereUI.ReapplyOwnAnchor(key)` deferred. EUI's login pass runs ~1 s after
    `PLAYER_ENTERING_WORLD` and re-applies everything registered by then; registering later is
    supported but nothing re-applies for you.

⚠ `noResize = true` costs one thing and it is **not** anchoring. `ValidateStoredLinks` prunes a
stored width/height **match** when either endpoint declares `noResize`, so nobody can size-match
to us. **Anchors are pruned only for a missing endpoint and never consult `noResize`** — confirmed,
so the goal is unaffected.

**PAUSE.** The power bars and cast bar are anchored to the row in `/eui` unlock mode and hold
across a reload, a spec swap and an icon-size change. **This is the goal of the whole plan**, and
the point at which it is worth asking whether anything below is wanted at all.

---

## Phase 4 — The reading model, only if two rows carry a scan claim

27. **Decide the product question first:** is the bottom row **the** scan with the top row a shelf
    you glance at, or is the scan row-major, top then bottom? Deliberately left to the pause after
    Phase 3 — easier to answer with a two-row panel on screen.
28. ⚠ **Bigger than the earlier draft said.** It is not only the gate: `capart.py`'s row grammar
    is one-dimensional at its root.
    - `parse_row` (`capart.py:600`) returns a flat `list[dict]`, and the comment at **594-596**
      states the model outright — *"The composed reading order is the authored left-to-right
      order… the seam changes how the entry is DRAWN, never its rank."* Seams are constrained to
      exactly 0 or 2 (**613-619**). **There is no notion of a row break or wrap.**
    - `elimination_gate` (`capart.py:4783`, body to 4849) walks that flat list — `for e in
      sc["row"]` at **4817**, `first = e` / `break` at **4831-4832**.
    - `density_gate` slices a flat prefix at **4919** ("between the left edge and the press").
    - All are driven by `reading_gate` (`capart.py:4931`, calling them at **4963-4965**), whose
      only caller is `_check_one` at **5323**.
    Until this is taught the traversal it will keep certifying a one-dimensional reading order the
    screen has stopped drawing.
29. Amend `render-shelf.md` **Part 0.5** and re-judge the treatments below it. Part 0.5 already
    names itself as the thing to edit: *"If a flight says scanning left-to-right is too hard,
    **this is the thing that gets edited** — and every treatment below is then re-judged."*

**PAUSE.** This changes the product's reading model, not its plumbing. It needs a decision and a
flight, not a merge.

---

## Phase 5 — Parked, deliberately

30. **Scale-to-fit resize** — drop `noResize` and snap `setWidth` to whole cells, so dragging the
    panel's edge in a mover picks the icon size. ⚠ **Half of this shipped early, on 2026-08-31**,
    as the icon-size inversion: cap already `SetScale`s each item frame on the re-apply path, and
    the re-pool hazard below is already handled. What is left is only the *mover-driven* half —
    letting a drag write `icon_px` instead of it being authored in `render-tokens.json`.
    - ✅ **Blizzard applies `iconScale` only at pool acquire** (`CooldownViewer.lua:1996`,
      `OnAcquireItemFrame`), so cap's `SetScale` on an item frame is undefended — a re-pool
      silently reverts it, and re-pools happen on talent changes and roster churn. **Handled:**
      the `SetScale` rides `place`, the single door every write to an item frame goes through, so
      it re-asserts on every pass. Same reassert seam `Anchor` already owns for position.
    - Phase 4's "grow about centre or top-left" question has **already dissolved** — the panel is
      no longer a function of Blizzard's icon-size setting.
31. `RegisterSkin` for cap's own windows (`Window.lua`, `StylePanel.lua`) — a genuinely separate,
    documented API, touches no CDM frame, ships any time or never.

---

## Docs, as each phase lands

32. `spec.md` — §3.9 is at **seven** properties. Keep the count sentence true.
33. `specs/backlog.md` → `## Status` — the only implementation-status block.
34. Client facts to `knowledge/addon-dev/`. Already landed: §4.6.1 (two-riders hazard), §2.6
    (StaticPopup shapes), §4.7 (viewer layout fields, the real gap of 1, the 50px template, the
    `iconScale` double-count). Still unwritten: `ResizeLayoutMixin` self-sizing, and managed-frame
    ownership of a viewer in its default position — **neither has been verified**, so write them
    only when measured.
35. EllesmereUI's mover surface as `[T3 obs]` facts with provenance per the `mine-addon` doctrine
    — facts and our own illustrations, **never copied code**. All rights reserved. Cite the live
    install with its version (9.0.8), since the pinned clone is gone.

---

## Verification

- `busted` and `luacheck CombatAssistPlus` from the addon root. Current baseline: **320 passing**,
  0 failures, 2 pending (both "the lab is empty, by design").
- `uv run python -m wowkb.capart check --all` for any `render-tokens.json` change, and
  `capart export lua` to regenerate `Style.lua` — `check` gates the committed Lua against the
  tokens exactly as it gates the HTML.
- `uv run python -m wowkb.kblint` and `wowkb.citecheck` for any `knowledge/addon-dev/` edit.
  Write new citations **symbol-anchored**; `citecheck` fails a symbol that no longer resolves.
- Phase 2: extend `tests/spec/engine/anchor_spec.lua` with the partition and the `(top, left)`
  ordering; read the result with `uv run python -m wowkb.capture cap anchor`.

---

## Open questions

- **Step 27** (which row is the scan) — a product call, left to the pause after Phase 3.
- **Overflow is the thread that got dropped.** The original discussion was *how to handle icons
  not fitting if the panel could resize*; when anchoring turned out not to need resize, the
  thread was abandoned rather than answered. Step 18 makes it an authoring error, but Havoc is at
  exactly 12 of 12 cells, so it is one entry from being a real problem — and a talent change
  cannot add authored entries, but a **13th authored entry** would need either a 3rd row, a
  smaller cell, or Phase 5. Decide this when Phase 2 is written, not after.
- **`norow` conflates three causes** in `Bind.lua:242` — API absent, info missing-or-secret, and
  no readable spell ID. Unrelated to this plan; worth splitting so the status line says which.
  A CDM entry can be item-backed (`equipSlot` is a nilable field on `CooldownViewerCooldown`),
  which is the benign explanation for Utility rows that will never bind.

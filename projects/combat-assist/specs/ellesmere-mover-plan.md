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
row to be a frame with a stable, honest rect a mover can address. Everything before Phase 3 is
groundwork for that; Phase 3 *is* the goal.

`/cap` (Combat Assist Plus) re-anchors the Essential Cooldown Manager viewer's item frames into
its catalog's authored priority order. It used to do that onto a nameless 1×1 `UIParent` child
whose position was re-derived from Blizzard's measured geometry every pass — so the row had no
position of its own and nothing could be anchored to it.

**That is fixed, shipped, and — as of 2026-08-31 — flown.** The row is `CombatAssistPlusRow`, a
named 6×2 panel with a saved per-character position, drawn at an icon size cap owns.

⚠ **What is BUILT is recorded in `projects/combat-assist/specs/backlog.md` → `## Status`**, in
detail, and is deliberately not restated here. This file is the forward plan; that one is the
record. `spec.md` §3.9 carries the promises (now **eight** properties — keep the count sentence
true).

---

## Status

| | | Ships as | State |
| --- | --- | --- | --- |
| **Phase 0** | Stand down beside another CDM rider | v0.15.0 | ✅ flown |
| **Phase 1** | The named 6×2 panel, `/cap move`, `Place.lua` | v0.16.0 | ✅ flown |
| — | **Principle (c)**: no order ⇒ cap draws nothing | v0.17.0 | ✅ flown |
| — | Placement per-character; opinions per-account | v0.18.0 | ✅ flown |
| — | Rescale no longer moves the panel | v0.18.1 | ✅ flown |
| — | **cap owns the icon size**, not Edit Mode | v0.19.0 | ✅ flown |
| — | One icon-size knob: client nominal split, virtual row derived | v0.19.1 | ✅ flown |
| **Phase 2** | Two rows | — | **START HERE** |
| **Phase 3** | EllesmereUI mover registration | — | **the actual goal** |
| **Phase 4** | Reading model, only if two rows carry a scan claim | — | needs a product decision |
| **Phase 5** | Scale-to-fit resize; `RegisterSkin` | — | half shipped, rest parked |

**The flight is CLOSED** (2026-08-31): acceptance steps 1–8 ran on v0.19.0 and again on v0.19.1,
`/cap band`'s readout included. Nothing is pending a client. Phase 2 starts clean.

⚠ **The five middle rows were not in the original plan.** Three are corrections to Phases 0–1 and
two are a premise that turned out never to have been decided. They are why the phases below differ
from the first draft — see *Corrections*.

---

## How to run this plan

**Stop at the end of every phase and wait.** Each phase ends with a `PAUSE` naming what should be
true before the next starts. Do not begin a phase because the previous one compiled — begin it
because the pause condition was checked.

⚠ **Releasing is not ask-first.** The standing authorization and its three gates are in
`projects/combat-assist/CLAUDE.md` § Releasing. The gate that matters here: **the grant retires
*may I release?*, never *did the last flight pass?*** Cutting a release begins a flight; it does
not end one. Every release note must say **what it has not exercised** — that is the flight
request.

Before touching the addon checkout: `uv run python -m wowkb.addon pull --all` from `tools/`.
⚠ The addon is a separate gitignored repo, and each worktree carries its own clone.

---

## Corrections carried forward

Why the phases below differ from the first draft. Do not re-litigate these.

1. **`50 × iconScale` double-counts.** `SetScale` does not change what `GetWidth` returns, so an
   item frame reads **50** wide at every setting. Every length in `tokens.row` is in the panel's
   own coordinate space. `anchor_spec` asserts this, so it cannot come back quietly.
2. **`metrics()`'s gap derivation is gone** (landed in Phase 1, not 2). `metrics()` is now
   `origin()` and returns only the seed corner. Blizzard's real padding is
   `iconPadding + GetAdditionalPaddingOffset()` = 5 + (−4) = **1**.
3. **The `P.foreign` origin-adoption path was deleted.** Following the CDM's placement is exactly
   what a row with a saved position must not do. Behaviour change, recorded in `spec.md` §3.9: an
   Edit Mode move of the viewer no longer drags cap's row.
4. **Asking EllesmereUI's maintainer to support cap is dropped.** Read back plainly it was: ask
   the busy maintainer of a top-tier addon to support an unreleased one-user addon. Its premise
   was also wrong — `SKINNING_API.md` documents `RegisterSkin` and never mentions conflicts.
   `_G._CAP_IsOrderingEnabled` is published anyway and is **already shipped**
   (`Anchor.lua:1035`, aliasing `Anchor.Ordering` at `:1032`) — nothing to do.
5. **`Place.lua` over parameterising `Frame.lua`**, because `Anchor.lua` loads before `Frame.lua`.
   Both frames register with it.
6. ⚠ **cap owns the icon size; Blizzard's Edit Mode slider does not reach it.** This was never a
   decision — it arrived inside the Phase 1 commit as an implementation default and `spec.md`
   never stated it. It cost the v0.18.1 rescale jump and it stalled a backlog item. `row.icon_px`
   (default 50) is the one authored knob; the panel wears `icon_px / 50` and cap re-asserts that
   effective scale onto every claimed frame from inside `place()` — the single door every write
   goes through, because Blizzard applies `iconScale` at **pool acquire** and a one-shot would
   revert on the first spec swap. `disarm()` hands the slider's value back.
7. ⚠ **One icon-size knob, not three.** Two duplicated constants agreed at 50 by coincidence and
   so were invisible: the client's paint fallback was the *preview's* nominal 56 (12% over — the
   measured cause of an overhang defect already recorded in `Paint.lua`), and the virtual row had
   its own `panel.icon_px`. Now `surfaces.host_nominal_px` = 50 is the client's, `surfaces.icon_px`
   = 56 stays the preview's, and `panel.icon_px` is **deleted** — `Panel.lua` derives from
   `row.icon_px`. **The lesson generalises: a duplicated constant is not caught by a test that
   only ever runs at the value where the duplicates match.** Both now assert *distinct or absent*.

---

## Phase 2 — Two rows

The panel is **already** 6×2 (`row.cols` = 6, `row.rows` = 2). Phase 2 does not resize anything —
it *uses* the second row of cells, which placement currently ignores. All citations re-resolved
2026-08-31 against the current file (**`Anchor.lua` is now 1329 lines**; `apply()` is at `:674`).

⚠ **A design pressure-test on 2026-08-31 found five holes in the steps below, one of which would
have shipped a phase with no instrument for its own novelty.** Its findings are folded in as
**15a–15e** and the steps are amended in place. Do not read a step without its amendment.

15. Add an authored **`break_before = "<entry id>"` per catalog** — one break point, named once,
    which is what makes step 16's fallthrough rule read naturally. Validate in `Catalog.Check`
    (`Catalog.lua:183`, body to `:588`) at **top level**, beside the existing
    `bar must name one enhanced entry` check at **`Catalog.lua:586`**, since it is a catalog-level
    key naming an entry rather than an entry-shape rule. Refuse an id that is not declared, and
    refuse the first entry.
    *(A per-entry `break_before = true` boolean is the alternative and would validate in the
    entry-shape loop opening at `Catalog.lua:232`. The catalog-level form was the original
    decision; do not change it without a reason.)*

    **15a — refuse a break on a VIRTUAL entry.** A virtual entry (`Devourer.lua:321`, `consume`)
    never reaches `byEntry` by construction (`Catalog.lua:632-637`), so the break would fall
    through on every build and the key would silently do nothing. A permanent no-op is worse than
    an error. Refuse it alongside *not declared* and *first entry*.

16. A break entry that is not talented falls through to the next present entry in authored order.
    ⚠ **Resolve it in PLAN space, not in `Catalog.Resolve`.** `Resolve` knows `byEntry`
    (`Catalog.lua:640`) — "this entry bound to a row" — but it does not know `Anchor.Plan`'s dedup
    (`Anchor.lua:93`; `anchor_spec.lua:77` covers it: two entries naming one row means the second
    is *missing* even though `byEntry` holds it), and it does not know about `extra` rows. So pass
    `breakBefore` into **`Anchor.Plan`** and have it return `plan.breakAt` — the 1-based index in
    `order` of the first item at-or-after the authored break. `Catalog.Resolve` stays untouched.
    ⚠ **Name the degenerate cases explicitly and test them** — every one is reachable by a talent
    change, which is exactly when nobody is looking:

    | Case | Behaviour |
    | --- | --- |
    | No `break_before` authored (Destruction, any opt-out) | `breakAt = nil` → single row, byte-identical to today. **The default, not an error.** |
    | Break entry untalented, later entries present | `breakAt` = first present later entry. The nominal case. |
    | Every entry from the break onward absent | `breakAt = #order + 1` → row 1 empty, all on row 0. **Must not error.** |
    | Break is the last authored entry, present | 1 icon on row 1. Legal but poor authoring — do **not** refuse it; talent variance means "last" is not stable. |
    | Break entry present, but its row already claimed by an earlier entry (Plan dedup) | Not in `order`; falls through to the next present item. Free, in plan space. |
    | Break names a virtual entry | Refused in `Check` — see 15a. |
    | Break names entry 1 | Refused in `Check`. |
    | Extras (`Anchor.lua:101-107`) | Index > `breakAt`, so they land on row 1's tail; they join row 0 when the break fell off the end. Say so in the docs. |
    | Zero tracked frames | Already handled — `apply()` bails at `Anchor.lua:678`. |

17. Teach `apply()` the second axis. The placement loop is **`Anchor.lua:714-719`**, single-axis in
    exactly two places — `local x = (i - 1) * pitch` at **`:715`** and the hardcoded `y = 0` in the
    `want` table at **`:716`**. Pitch is already token-derived at **`:706-707`** and is correct for
    **both** axes (`cell_px` is one square number; `gridSize()` already multiplies `rows` at
    `:305`). Entries before the break to row 0, the rest to row 1, **left-aligned in both**, so the
    scan's starting x never moves with roster length.

    **17a — `apply()` cannot see entry ids.** `P.tracked`'s elements are `{ cooldownID, frame }`
    only; `adopt` (`Anchor.lua:945`) drops the `item.entry` that `Anchor.Plan` carried
    (`Anchor.lua:95`). The break must arrive as an **index**: `adopt` copies `plan.breakAt` to
    `P.breakAt`.

    **17b — the sign, and the exact `want`.** `SetPoint("TOPLEFT", P.anchor, "TOPLEFT", x, y)` with
    WoW's y axis pointing **up**, so descending a row is **negative**:

    ```
    local row  = (breakAt and i >= breakAt) and 1 or 0
    local col  = (row == 1) and (i - breakAt) or (i - 1)
    local x, y = col * pitch, -(row * pitch)
    local want = { x = x, y = y, left = left + x, top = top + y }
    ```

    `want.top` is `top + y` — an absolute the drift auditor compares against `frame:GetTop()` at
    **`:812`** — **not** `top - y` and not `top`. ⚠ A positive `y` would draw row 1 *above* row 0
    and `want.top` would be wrong in the same direction, so **the auditor would report zero drift
    for a sign error**. Assert the sign in a test.

    **17c — clamp, do not just split.** Treat `break_before` as a *minimum* wrap point: row 0 ends
    at the break **or** at `cols`, whichever comes first, same for row 1's tail. Without this the
    extras of 17a/step 18 spill off the panel with no diagnostic, and a break authored at entry 9
    of 12 runs row 0 two cells past the right edge.

18. `Catalog.Check` fails a catalog whose authored roster cannot fit the panel.
    ⚠ **Immediately load-bearing, not theoretical: Havoc authors exactly 12 entries** (verified
    2026-08-31 — `Catalogs/Havoc.lua`, `entries` opens at `:60`). Zero headroom. Demonology,
    Protection and Retribution are at 9; Devourer 7; Destruction 1.

    **18a — the predicate, stated correctly.** Three corrections:
    - Count **non-virtual** entries only. A virtual entry has no CDM row by construction, so
      Devourer is 7 authored / 6 cells and would fail a naive count.
    - Validate the **partition**, not the total: `breakIndex - 1 <= cols` **and**
      `n - breakIndex + 1 <= cols`. "Fits 12" is not sufficient — the break decides the split.
    - Read `cols`/`rows` from `ns.Style.row`, **never a hardcoded 12** (see *Open questions*).
      `Catalog.Check` **cannot** call `Anchor.Grid()` — `tests/check_catalog.lua` loads only
      `Catalog.lua`, `Style.lua` and the catalog, and `Anchor.lua` builds a frame at file scope
      (`Anchor.lua:1234`). Read the two token values and **do not** re-derive cell pitch there
      (`Anchor.lua:310` forbids exactly that).

    **18b — it is a tripwire, not a safety net.** `Anchor.Plan` appends every viewer row the
    catalog does *not* name after the named ones (`Anchor.lua:101-107`; `A{extra}` counts them),
    so a player enabling one extra ability in the Essential viewer overflows Havoc from outside
    the catalog's control, invisibly to any static check. 17c's clamp is what actually holds.

19. **Fix `Anchor.Drawn()`** (**`Anchor.lua:505-523`**) to sort by `(top, left)` rather than `left`
    alone. The comparator is **`:513-516`** and is purely one-dimensional — two rows would
    column-interleave and every capture would read `X{MISMATCH}` forever.
    ⚠ **Two traps.** `geometry()` returns `left, top` but `:511` captures only `left` — the top is
    available and thrown away. And the sort is **`top` DESCENDING, `left` ascending**: a higher
    `GetTop()` is higher on screen, so reading order is the *larger* top first. Sorting both
    ascending silently reverses the rows.

    **19a — do NOT write a tolerance comparator.** `math.abs(a.top - b.top) > TOL` is not
    transitive and Lua's `table.sort` raises `invalid order function for sorting` on a large
    enough shuffled input. Use an integer bucket, which stays transitive:

    ```
    local ta, tb = math.floor(a.top + 0.5), math.floor(b.top + 0.5)
    if ta ~= tb then return ta > tb end          -- higher top first
    if a.left ~= b.left then return a.left < b.left end
    return a.cooldownID < b.cooldownID
    ```

    Row pitch is ≥ 51 panel units at any sane `icon_px`, so 1-unit buckets can never merge rows.

    **19b — parked frames must stay out of the sort.** `parkWant` (`Anchor.lua:598-600`) is
    anchor-relative and unaffected, and parked frames live in `P.wantOf`/`P.parked` but **not** in
    `P.tracked`, so `Drawn()` never sees them — which is load-bearing, because at `top + 10000`
    they would sort ahead of row 0 and corrupt every capture. Add an explicit test so a future
    edit that walks `claimed` instead of `tracked` fails loudly.

    **19c — ⚠ THE CORRECTNESS HOLE: the verdict is still single-axis.** `Drawn()` returns an id
    sequence and `match` compares it elementwise to `P.planned` (**`Anchor.lua:517-521`**). Once
    the sort is two-dimensional, a run that put **all 12 icons on row 0** yields the *identical*
    id sequence and reads `X{ok}` forever — the row assignment is not in the comparison at all.
    **`Drawn()` must also return a measured `breakAt`** (the count of items in the highest-top
    bucket) and **`match` must require `drawnBreak == plannedBreak`.** Without this the phase
    ships with no instrument for the only thing it added.

    *(Everything else is already two-axis and needs no change: `sample()` compares `top` against
    `want.top` at `:812`, `gridSize()` multiplies `rows` at `:305`, `origin()` takes max-top at
    `:666`, `resizeAnchor()` re-sizes on height, and `onFramePoint` at `:609` only replays
    `P.wantOf[frame]` through `place()`, so it is axis-agnostic.)*

20. ~~Delete `metrics()`'s gap derivation~~ — **done in Phase 1**, see correction 2.
21. Add a row-break token to the **anchor** stream's wire. `Anchor.Render` is
    **`Anchor.lua:126-149`** and emits `A{} P{} D{} X{} S{}` at **`:144-148`**; `P{}`/`D{}` are
    cooldownID orders built by the `list()` helper at **`:118-123`**.
    ⚠ **Put the break in BOTH `P{}` and `D{}` as a `|` separator at the boundary**, and fold the
    measured-vs-planned break into `match` per 19c. A `brk:<n>` field in `A{}` alone is the plan's
    own number restated and **cannot fail** — it would be decoration, not an instrument.
    Document it in `specs/flight-reading.md` — ⚠ that file describes **two** different `P{}`/`D{}`
    groups and only the second is this one:
    - `## Draw surface`, **lines 135–183** — `P{}` there is `id:scan[+cue,…]`, a per-entry
      treatment, and its `D{}` is a counts group. **Not this.**
    - `## Anchor order`, **lines 185–266** — the orders. The defining bullet is **213–215**;
      `X{STALE:<n>}` precedence at **216–219**. ⚠ **`:214` states the `GetLeft()` assumption that
      step 19 is changing** — amend it in the same edit, or the doc certifies the old model.

**PAUSE.** A capture (`wowkb.capture cap anchor`) shows the authored two-row order drawn correctly
with `X{}` reporting a match, across a talent change that removes the break entry.

---

## Phase 3 — EllesmereUI — **the actual goal**

⚠ **The mined clone is GONE and that is correct.** `raw/addon-research/ELLESMEREUI-REMOVED.md`
records it: deleted per the `mine-addon` skill because EllesmereUI is All Rights Reserved and the
KB carries the facts. Re-clone recipe is in that note (tag v8.7.5, commit `c4eba58`) **but you
should not need it** — the facts below came from the **live install**, still present and confirmed
**9.0.8** on 2026-08-31. ⚠ A live install updates itself, so its line numbers are volatile in a way
a pinned clone's are not: **re-resolve by symbol before relying on any number.**

⚠ **The API spans TWO files, not one.** Verified 2026-08-31 by symbol presence:
- `…/AddOns/EllesmereUI/EUI_UnlockMode.lua` — `RegisterUnlockElements`, `NotifyElementResized`,
  `ReapplyOwnAnchor`, `ValidateStoredLinks`, `SaveBarPosition`, `LoadBarPosition`,
  `ClearBarPosition`.
- `…/AddOns/EllesmereUI/EllesmereUI.lua` — **`MakeUnlockElement`**, which is *not* in
  `EUI_UnlockMode.lua` at 9.0.8 despite being the constructor step 23 starts from.

⚠ EllesmereUI is **All Rights Reserved**. Per the `mine-addon` doctrine: record facts and our own
illustrations with provenance, **never copied code**.

22. Add `Ellesmere.lua`, loaded after `Anchor.lua`, entirely behind
    `if EllesmereUI and EllesmereUI.RegisterUnlockElements`. Add `## OptionalDeps: EllesmereUI`
    to the `.toc` so the base addon loads first.
23. Register one element via `EllesmereUI.MakeUnlockElement`:
    - Registration is a **colon** call taking an **array** —
      `EllesmereUI:RegisterUnlockElements({elem}, "cap")`; it uses `self`.
    - `getSize` is **effectively required**: it feeds mover geometry and the cog's Width/Height
      boxes. Without it plus `noResize = true` the cog shows size inputs that silently do nothing.
    - `key` is a single global namespace across every addon — prefix it (`CAP_ROW`).
    - `getFrame` side-effect-free. `isHidden` takes **no arguments**; return true whenever
      `Anchor.Ordering()` is false — which after principle (c) is exactly when cap draws nothing.
    - `noResize = true`; `noAnchorTarget` and `noAnchorTo` both omitted — that is what lets the
      power bars anchor to us.
24. Point `savePos` / `loadPos` / `clearPos` / `applyPos` at **Phase 1's `Place` store**, which is
    why Phase 1 was a prerequisite. Mandatory, and proven: `SaveBarPosition` / `LoadBarPosition` /
    `ClearBarPosition` delegate to the element's own functions and fall through to
    `GetPositionDB()` only when no element is registered — and that fallback is the
    EllesmereUIActionBars profile table, `nil` in the base addon. Omit them and drags are silently
    lost. `loadPos` returns `{point, relPoint, x, y}`, canonically `CENTER`/`CENTER` with offsets
    from UIParent's centre — **already `Place`'s convention**, so it fits without translation.
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
across a reload, a spec swap, and a change to `row.icon_px`. **This is the goal of the whole
plan**, and the point at which it is worth asking whether anything below is wanted at all.

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
      exactly 0 or 2 (test at **:614**). **There is no notion of a row break or wrap.**
    - `elimination_gate` (`capart.py:4783`, body to 4849) walks that flat list — `for e in
      sc["row"]` at **:4817**, `first = e` / `break` at **:4831-4832**.
    - `density_gate` slices a flat prefix at **:4919**.
    - All are driven by `reading_gate` (`capart.py:4931`, calling them at **:4963-4965**), whose
      only caller is **`_check_one` at `capart.py:5138`** (the call itself is at `:5323` — the old
      plan cited the call site as the definition).
    Until this is taught the traversal it will keep certifying a one-dimensional reading order the
    screen has stopped drawing.
29. Amend `render-shelf.md` **Part 0.5** and re-judge the treatments below it. Part 0.5 already
    names itself as the thing to edit: *"If a flight says scanning left-to-right is too hard,
    **this is the thing that gets edited** — and every treatment below is then re-judged."*

**PAUSE.** This changes the product's reading model, not its plumbing. It needs a decision and a
flight, not a merge.

---

## Phase 5 — Half shipped, rest parked

30. **Scale-to-fit resize** — drop `noResize` and snap `setWidth` to whole cells, so dragging the
    panel's edge in a mover picks the icon size. ⚠ **Half of this shipped early on 2026-08-31** as
    the icon-size inversion: cap already `SetScale`s each item frame on the re-apply path, and the
    re-pool hazard is handled. What is left is only the *mover-driven* half — letting a drag write
    `row.icon_px` instead of it being authored in `render-tokens.json`.
    - ✅ **Blizzard applies `iconScale` only at pool acquire** (`CooldownViewer.lua:1996`,
      `OnAcquireItemFrame`), so a rider's `SetScale` is undefended and a re-pool reverts it.
      **Handled:** the `SetScale` rides `place()`, the single door, so it re-asserts every pass.
    - Phase 4's "grow about centre or top-left" question has **already dissolved** — the panel is
      no longer a function of Blizzard's icon-size setting.
    ⚠ **The pressure-test recommends against reaching for this to solve overflow** — deriving
    `icon_px` from the live roster re-makes icon size an *input* cap has to chase (the exact
    authority inversion undone on 2026-08-31, `Anchor.lua:317-324`) and makes the panel's rect
    roster-dependent, destroying "the rect is known at login, so a mover can address it"
    (`Anchor.lua:292-293`). See *Open questions*.
31. `RegisterSkin` for cap's own windows (`Window.lua`, `StylePanel.lua`) — a genuinely separate,
    documented API, touches no CDM frame, ships any time or never.

---

## Docs, as each phase lands

32. `spec.md` §3.9 is at **eight** properties. Keep the count sentence true.
33. `specs/backlog.md` → `## Status` — the only implementation-status block.
34. Client facts to `knowledge/addon-dev/`, where the KB's gates apply — this plan is not their
    home. Already landed: §4.6.1 (two-riders hazard), §2.6 (StaticPopup shapes), §4.7 (viewer
    layout fields, the real gap of 1, the 50px template, the `iconScale` double-count). Still
    unwritten: `ResizeLayoutMixin` self-sizing, and managed-frame ownership of a viewer in its
    default position — **neither has been verified**, so write them only when measured.
35. EllesmereUI's mover surface as `[T3 obs]` facts with provenance per the `mine-addon` doctrine
    — facts and our own illustrations, **never copied code**. All rights reserved. Cite the live
    install with its version (9.0.8), since the pinned clone is gone.

---

## Verification

- `busted` and `luacheck CombatAssistPlus` from the addon root. **Current baseline: 329 passing**,
  0 failures, 2 pending (both "the lab is empty, by design").
- `uv run python -m wowkb.capart check --all` for any `render-tokens.json` change, and
  `capart export lua` to regenerate `Style.lua` — `check` gates the committed Lua against the
  tokens exactly as it gates the HTML. ⚠ A token edit also makes every preview stale; run
  `capart build --all` before `check`.
- `uv run python -m wowkb.kblint` and `wowkb.citecheck` for any `knowledge/addon-dev/` edit.
  Write new citations **symbol-anchored**; `citecheck` fails a symbol that no longer resolves.
- `uv run python -m wowkb.obs check` gates a `--minor` / `--major` release.
- Read a flight result with `uv run python -m wowkb.capture cap anchor`.
- **Phase 2 specifically** — three pure functions must be **extracted first**, because none of
  step 17/19 is reachable from `busted` today (`anchor_spec.lua:1-2` — pure functions only, house
  rule 6), and without the extraction the y sign of 17b is untestable:
  1. `Anchor.Plan(rows, entries, breakBefore)` → adds `plan.breakAt`.
  2. `Anchor.Cells(n, breakAt, cols, pitch)` → array of `{x, y}`; `apply()` consumes it at `:714`.
  3. `Anchor.ReadOrder(seen)` → the pure `(top desc, left asc, cooldownID)` sort; `Anchor.Drawn()`
     calls it and derives the measured break from the first bucket.

  Then extend `tests/spec/engine/anchor_spec.lua` with: every degenerate row of step 16's table;
  **the y sign asserted by sign, not magnitude**; x resetting to 0 at `breakAt`; `breakAt = nil`
  reproducing `(i-1)*pitch, 0` exactly; the 17c clamp; a **±0.4-jitter** input that must **not**
  raise `invalid order function for sorting` (the 19a guard); a shuffled two-row input that would
  pass under an all-ascending sort, so the sign is pinned; parked frames absent from the sort
  (19b); and **the measured break differing from the planned one on a flattened 12/0 layout with
  identical id sequences** — the test that proves 19c is closed. For `Catalog.Check`: undeclared
  id, entry 1, a virtual entry, a non-string value, absent key, and a partition exceeding `cols`;
  plus all six shipped catalogs still returning `{}` (`catalog_spec.lua:9` and
  `tests/check_catalog.lua`'s gate).
  ⚠ The suite has no `UIParent` — stub it, as the icon-size tests do.

---

## Open questions

- **Step 27** (which row is the scan) — a product call, left to the pause after Phase 3.
- **Overflow, and the thread that got dropped.** The original discussion was *how to handle icons
  not fitting if the panel could resize*; when anchoring turned out not to need resize, the thread
  was abandoned rather than answered. Step 18 makes it an authoring error — but **Havoc is at
  exactly 12 of 12**, so it is one entry from being real, and a 13th authored entry needs a third
  row, a smaller cell, or Phase 5.
  ⚠ **Owning the icon size opened a fourth option the old plan could not have.** `cols` and `rows`
  are themselves tokens, so 7×2 = 14 cells is a `render-tokens.json` edit — and shrinking
  `row.icon_px` keeps the panel the same *screen* width while doing it, which was impossible while
  Blizzard owned the size. The pressure-test scored the four and **recommends this one**: a third
  row costs a second wrap and stops the row reading as a scan; a smaller `cell_px` is structurally
  impossible (`cell_floor_px` = 50 is the item template's own size, floored at `Anchor.lua:299` —
  shrinking icons is `icon_px`'s job); Phase 5 destroys the static rect. Its honest cost: the
  shelf is global, so every catalog's icons shrink for Havoc's 13th entry — acceptable, because a
  scan of peers at one size is what the tokens already insist on.
  **Therefore: write step 18's check against `cols × rows` read from the tokens, never a hardcoded
  12.** That is the whole decision — it turns overflow from a code change into a token change, and
  it is free to do now versus expensive to retrofit. Decide the *layout* question only when a 13th
  entry actually exists.
- **`norow` conflates three causes** in `Bind.lua:242` — API absent, info missing-or-secret, and
  no readable spell ID. Unrelated to this plan; worth splitting so the status line says which.
  A CDM entry can be item-backed (`equipSlot` is a nilable field on `CooldownViewerCooldown`),
  which is the benign explanation for Utility rows that will never bind.

# Plan — cap's CDM row becomes a 6×2 panel EllesmereUI can move

**Status: an approved plan, not an authority.** A temporary migration artifact in the sense
`CLAUDE.md` gives that phrase, alongside `simplification-plan.md`. It supersedes the earlier
proposal of the same name, which predated the 6×2 grid and the conflict guard. As each phase
lands its outcome goes to `backlog.md` → `## Status` and its promises to `spec.md`; this file
is deleted when the last one does.

Client facts cited below belong in `knowledge/addon-dev/`, where the KB's gates apply — this
plan is not their home, and step 34 is what moves them.

---

## Context

`/cap` (Combat Assist Plus) re-anchors the Essential Cooldown Manager viewer's item frames into
its catalog's authored order. It does that onto `P.anchor` — a nameless 1×1 `UIParent` child
whose position is **slaved to Blizzard's measured geometry** on every pass: `metrics()` reads the
drawn row's top-left and `apply()` plants the anchor there. The row therefore has no position of
its own, and nothing else can be anchored to it.

**The goal is to anchor the power bars and cast bar to the CDM row.** That needs the row to be a
frame with a stable, honest rect that EllesmereUI's mover can address. Two things follow: the
anchor becomes a real named panel with a saved position, and its size becomes a fixed 6×2 grid of
cells rather than a width derived from Blizzard's stride — which also means it never has to wait
for the Cooldown Manager to draw before it knows how big it is.

**One thing must ship first, and it is not optional.** EllesmereUI's Cooldown Manager module
holds the same item frames with the same technique cap uses — a `hooksecurefunc` on each frame's
own `SetPoint` that recognises its own writes by `relativeTo` and otherwise forces the frame back.
Two such hooks on one frame is unbounded mutual recursion inside a single call stack. This is not
a prediction: EllesmereUI carries a hardcoded "EMERGENCY CONFLICT GUARD" for exactly this class of
addon, whose comment reads *"hooks the same Blizzard frames we do; running both **crashes the
client on the loading screen**"*. cap is in that class.

---

## How to run this plan

**Stop at the end of every phase and wait.** Each phase ends with a `PAUSE` line naming what
should be true before the next one starts. Phase 0 is releasable on its own and should be released
on its own. Do not begin a phase because the previous one compiled — begin it because the pause
condition was checked.

Before touching the addon checkout at all: `uv run python -m wowkb.addon pull --all` from `tools/`
(the addon is a gitignored sub-repo and each worktree carries its own clone). Releasing is
ask-first, always.

---

## Phase 0 — Stand down beside another CDM rider — **BUILT, awaiting its flight**

1. Add a known-CDM-riders table to cap, seeded with `EllesmereUICooldownManager` plus the five
   already named in EllesmereUI's own conflict list — `BetterCooldownManager`,
   `CooldownManagerCentered`, `SkironCooldownManager`, `ArcUI`, `Ayije_CDM`.
2. Detect in two stages: `C_AddOns.IsAddOnLoaded` on the folder name decides **who to name**, and
   a positional test at arm time — an Essential item frame anchored to neither the viewer nor
   cap's own frame — decides **whether it is actually managing the row**.
3. On detection, refuse to arm ordering and raise a modal with a **single OK button** naming the
   addon and saying cap's row ordering is off because two addons cannot order the same icons.
4. **Deliberately do not remember the acknowledgement** — the modal fires on every login and
   `/reload` for as long as both are enabled, because the nag is the feature and the fix is one
   toggle away.
5. Fire it only when cap **would otherwise have ordered**, so a player who has turned
   `/cap anchor off` themselves is never nagged, and defer it out of combat exactly as
   `Anchor.ask()` already defers its contention popup.
6. Expose `_G._CAP_IsOrderingEnabled` so EllesmereUI's conflict table can gate its own popup on
   cap actually ordering, following the `_ERF_IsHoverCastEnabled` precedent their Clique entry
   uses.
7. Ask Ellesmere on Discord for a conflict entry targeting `EllesmereUICooldownManager`, with a
   coexistence `message` and that `moduleCheck` — their skinning doc invites exactly this.
   **Still to do; it is a message to a person, not a code change.**

⚠ **One thing was added that the phase did not list, and it is load-bearing.** The arm-time
positional test cannot see a rider that claims the row *after* cap has armed, and that race ends
in the crash the phase exists to prevent. `onFramePoint` therefore carries a re-entry depth
guard that stands cap down instead of recursing. It latches for the session; `/cap anchor retry`
releases it.

**PAUSE.** Do not continue until this is released and a login with EllesmereUI's CDM module
enabled has produced the modal and a cap that does not order, and a login without it has produced
neither.

---

## Phase 1 — The panel, with EllesmereUI absent

8. Promote `P.anchor` to a named frame, `CombatAssistPlusRow`.
9. Give it a saved position at `db.row.x/.y/.placed`, reusing `Frame.lua:52-105`'s store shape,
   UIParent-scale normalisation and its re-apply events verbatim.
10. Invert the origin so `apply()` reads its position from that store, seeding it once from
    Blizzard's measured geometry so an upgrading player sees no jump.
11. Add a `tokens.row` group to `specs/render-tokens.json` declaring the grid — 6 across, 2 down,
    cell size, gap — which is the CDM-row geometry `render-shelf.md` currently does not own.
12. Treat `50 × viewer.iconScale` as a **floor** under the cell rather than as the cell, so the
    panel stays fixed in pixels across a range of Edit Mode icon sizes.
13. Compute size and position at login from `viewer.iconScale` alone and refresh on the
    `CooldownViewerSettings.OnDataChanged` callback cap already hooks, so nothing waits for
    Blizzard to draw.
14. Add `/cap move` support for the row panel, which is also the whole answer to "what happens
    without EllesmereUI" — everything except snapping and anchor links.

⚠ The trap in this phase is scale: `apply()` sets the anchor's scale to
`itemEffectiveScale / UIParentEffectiveScale`, so a stored offset must be normalised against the
**panel's own** scale, not `UIParent`'s.

**PAUSE.** Do not continue until the row can be dragged with `/cap move` and holds its position
across `/reload`, a spec swap and an Edit Mode icon-size change.

---

## Phase 2 — Two rows

15. Add an authored `break_before = "<entry id>"` to each catalog, validated by `Catalog.Check`
    against the ids it already cross-references.
16. Rule that a break entry which is not talented falls through to the next present entry in
    authored order.
17. Teach `apply()` the second axis — entries before the break to row 0, the rest to row 1,
    left-aligned in both so the scan's starting x never moves with roster length.
18. Make `Catalog.Check` fail a catalog whose live roster cannot fit twelve cells, so overflow is
    an authoring error at write time rather than a surprise mid-pull.
19. Fix `Anchor.Drawn()` to sort by `(top, left)` rather than `left` alone, or two rows
    column-interleave and every capture reads `X{MISMATCH}` forever.
20. Delete `metrics()`'s gap derivation rather than repairing its cross-row interleave, since the
    gap is now ours — which also removes the `DEFAULT_GAP = 4` fallback that silently disagrees
    with Blizzard's real default of 1.
21. Add a row-break token to the `P{}` / `D{}` capture wire and document it in
    `specs/flight-reading.md`.

**PAUSE.** Do not continue until a capture shows the authored two-row order drawn correctly, with
`X{}` reporting a match rather than a mismatch, across a talent change that removes the break
entry.

---

## Phase 3 — EllesmereUI

22. Add `Ellesmere.lua`, loaded after `Anchor.lua` in the `.toc`, entirely behind
    `if EllesmereUI and EllesmereUI.RegisterUnlockElements`.
23. Register one element built by `EllesmereUI.MakeUnlockElement` with `noResize = true`,
    `noAnchorTarget` and `noAnchorTo` both omitted, a **side-effect-free** `getFrame`, and
    `isHidden` true whenever ordering is off or stood down.
24. Point `savePos` / `loadPos` / `clearPos` / `applyPos` at Phase 1's store, because EllesmereUI
    keeps no position for us — that is why Phase 1 is a prerequisite rather than a convenience.
25. Call `EllesmereUI.NotifyElementResized` on the rare occasions the cell floor changes the
    panel's size.
26. Call `EllesmereUI.ReapplyOwnAnchor` at login so a user's anchor link survives EllesmereUI's own
    load order.

⚠ `noResize = true` costs one thing and it is not anchoring: `ValidateStoredLinks` prunes a stored
width/height **match** whose target declares `noResize`, so nobody can size-match to us. Anchors
are validated separately and are unaffected.

**PAUSE.** Do not continue until the power bars and cast bar are anchored to the row in `/eui`
unlock mode and hold across a reload, a spec swap and an icon-size change — which is the goal of
the whole plan, and the point at which it is worth asking whether anything below is wanted.

---

## Phase 4 — The reading model, only if two rows carry a scan claim

27. Decide the product question first: is the bottom row **the** scan with the top row a shelf you
    glance at, or is the scan row-major, top then bottom?
28. Add a row-break token to `scenarios.md`'s CDM-row grammar and teach `capart`'s elimination gate
    the traversal, which today reads document list order and would otherwise keep certifying a
    one-dimensional reading order the screen has stopped drawing.
29. Amend `render-shelf.md` Part 0.5 and re-judge the treatments below it, which that file states
    outright is the cost of editing it.

**PAUSE.** This phase changes the product's reading model, not its plumbing; it needs a decision
and a flight, not a merge.

---

## Phase 5 — Optional, later

30. Add scale-to-fit resize — drop `noResize`, have `setWidth` snap to whole cells, and `SetScale`
    each item frame on the same re-apply path (Blizzard applies `iconScale` only at pool acquire,
    so the guard is weak) — if being a width-match target turns out to matter more than being
    fixed.
31. `RegisterSkin` for cap's own windows (`Window.lua`, `StylePanel.lua`), which touches no CDM
    frame and can ship at any time or never.

---

## Docs, as each phase lands

32. Make `spec.md` §3.9's `/cap move` sentence true and amend §4 for the row having a position of
    its own — this closes an existing gap, since §3.9 already promises a control the code never
    wired up.
33. Record outcomes in `specs/backlog.md` → `## Status`, which is the project's only
    implementation-status source.
34. Put the client facts into `knowledge/addon-dev/`, where the KB's gates apply: the Edit Mode
    layout fields and their defaults, `ResizeLayoutMixin` self-sizing, managed-frame ownership of
    a viewer in its default position, and the two-riders-one-frame recursion hazard in
    `cdm-rider-patterns.md` §4.6.1, which currently reads as though only one addon ever applies
    that technique.
35. Record EllesmereUI's extension surface as `[T3 obs]` facts with `file:line` provenance per the
    `mine-addon` doctrine — facts and our own illustrations, never copied code.

**Landed with Phase 0:** §3.9 gained a sixth property (spec.md), the Status block gained the
stand-down entry (backlog.md), `cdm-rider-patterns.md` §4.6.1 gained the two-riders hazard, the
two-stage detection shape and the conflict-table surface, and
`frames-textures-animation.md` §2.6 gained the StaticPopup dialog-shape facts a one-button modal
needs. Steps 32 and 34 are otherwise still open for Phases 1–3.

---

## Verification

- **Phase 0, in game.** With EllesmereUI's CDM module enabled: `/reload` produces the modal, cap
  does not order, and a second `/reload` produces it again. With the module disabled: no modal,
  ordering arms normally. With `/cap anchor off` set by hand and the module enabled: no modal.
- **Phase 1, in game.** `/cap move`, drag, `/reload`; the row is where it was left. Repeat after a
  spec swap and after changing Edit Mode's Cooldown Manager icon size — the panel must not drift,
  and within the cell floor it must not resize either.
- **Phase 2, by capture.** `uv run python -m wowkb.capture cap <stream>` after a pull; the drawn
  order must match the authored order with the break honoured, and `X{}` must report a match.
  Extend `tests/spec/engine/anchor_spec.lua` with the partition and the `(top, left)` ordering.
- **Phase 3, in game.** `/eui` unlock mode shows a "Combat Assist Plus" mover on the row; dragging
  it moves the row; anchoring the power bars and cast bar to it survives `/reload`.
- **Throughout.** `uv run python -m wowkb.capart check` must pass for any `render-tokens.json`
  change (it gates the committed `Style.lua` against the tokens), and the Lua must pass the
  luaparser check that `wowkb.addon release` runs.

---

## Open decisions

- **Step 27** is a product call and is deliberately left to the pause after Phase 3 — it is a
  readability question, and it is easier to answer with a two-row panel on screen than in advance.
- **Step 30** is parked until the fixed panel has been lived with; both behaviours go through the
  same size accessor, so choosing later costs no rework.

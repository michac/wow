# Plan — anchor EllesmereUI to cap's row

**An approved plan, not an authority.** A temporary migration artifact in the sense
`projects/combat-assist/CLAUDE.md` gives that phrase. As each phase lands, its outcome goes to
`specs/backlog.md` → `## Status` and its promises to `spec.md`; **this file is deleted when the
last phase does.**

> ⚠ **THIS FILE IS SPENT AND CAN BE DELETED.** Its goal is reached, Phases 1–3 are recorded in
> `backlog.md` → `## Status`, Phases 4 and 5 have moved to their own documents, and the arguments
> behind every correction below live in `specs/archive/ellesmere-mover-plan-2026-09-01.md`.
> Nothing points here. It is kept only because it is untracked, so deleting it is not undoable by
> git — that is the author's call, not a thing to do while tidying.

**Where this stands: PHASE 3 IS DONE. The goal is reached — the bars hold against the row across
a reload, a spec swap and a `/cap grid` change (flown 2026-09-01, v0.23.1). Phases 4 and 5 are
optional and neither has started.**

---

## Context

**The goal is to anchor EllesmereUI's power bars and cast bar to cap's Cooldown Manager row.**
That is Phase 3. Everything before it was groundwork; everything after it is optional.

The row is `CombatAssistPlusRow` — a named panel, saved position per character, drawn at an icon
size cap owns, with a rect known at login rather than measured. Eight phases of work went into
making it a thing another addon's mover can point at. **What is left is to point one at it.**

### What this session did (2026-09-01)

- **Phase 1 landed.** Four catalogs author a row break. `specs/backlog.md` → `## Status` →
  *The four breaks are authored* is the record.
- **Havoc was corrected after `cap-conscience` caught it**, and the correction settled a product
  question: **the top row is the cooldowns, the bottom row is the rotation presses.** See
  correction 9.
- **Two releases were cut and deployed — v0.22.0 and v0.22.1. Neither has been flown.**
- **Phase 2's pause was waived as a blocker by the author**, so its acceptance set merges into
  Phase 3's flight. See Phase 2.

⚠ **What is BUILT is in `specs/backlog.md` → `## Status`**, in detail, and is deliberately not
restated here. This file is the forward plan; that one is the record.

### Renumbering

An earlier plan grew decimal phases (`2.5a`–`2.5e`), so its numbers recorded *when we thought of
something* rather than *what order to do it in*. **Phases are numbered 1–5** and nothing
renumbers again — new work appends or goes to `backlog.md` → `## Now`.

**History is `specs/archive/ellesmere-mover-plan-2026-09-01.md`.** Read it for the *arguments*,
which this file cites rather than restates: the Protection reorder refusal, the Destruction
retired-pilot correction, and the discovery that the catalogs are generated.

---

## Phases

| | | Gate | State |
| --- | --- | --- | --- |
| **1** | **Author the breaks** — four catalogs, one key each | `busted` + `capart check --all` green | ✅ **landed 2026-09-01** |
| **2** | **Fly the panel** | a capture answering the acceptance set | ✅ released (v0.22.1, deployed) · **flight merged into Phase 3's** |
| **3** | **EllesmereUI** — register the row as a mover element | **THE GOAL**; bars hold across reload / spec swap / regrid | ✅ **landed 2026-09-01 (v0.23.1) — PAUSE checked** |
| **4** | **The reading model** — only if two rows carry a scan claim | a product decision, then a flight | |
| **5** | **Parked** — Destruction, Devourer, mover-resize, `RegisterSkin` | nothing; these wait | |

**Stop at the end of every phase.** Each ends with a `PAUSE` naming what should be true before
the next starts. Begin a phase because its predecessor's pause was *checked*, never because it
compiled.

⚠ **Releasing is not ask-first** — `projects/combat-assist/CLAUDE.md` § Releasing carries the
standing authorization and its three gates. The gate that matters here: **the grant retires *may
I release?*, never *did the last flight pass?*** Cutting a release begins a flight; it does not
end one, and every release note must say what it has **not** exercised.

Before touching the addon checkout: `uv run python -m wowkb.addon pull --all` from `tools/`.
The addon is a separate gitignored repo and each worktree carries its own clone.

---

## Corrections that still bind

Do not re-litigate these. Items 1–7 came from the archive; 8 and 9 were learned on 2026-09-01.

1. **`50 × iconScale` double-counts.** `SetScale` does not change `GetWidth`, so an item frame
   reads **50** wide at every setting. Every length in `tokens.row` is in the panel's own
   coordinate space; `anchor_spec` asserts it.
2. **cap owns the icon size.** Blizzard's Edit Mode slider does not reach it; `disarm()` hands
   the slider's value back.
3. **The `P.foreign` origin-adoption path was deleted.** An Edit Mode move of the viewer no
   longer drags cap's row.
4. **Asking EllesmereUI's maintainer to support cap is dropped.** `_G._CAP_IsOrderingEnabled` is
   published anyway and already ships (`Anchor.lua:1321`, aliasing `Anchor.Ordering`).
5. **A duplicated constant is not caught by a test that only runs where the duplicates match.**
   This cost two invisible defects; both now assert *distinct or absent*.
6. ⚠ **Reordering a catalog is allowed, merely expensive — but the APL binds.** Moving an entry
   may need new cues to keep elimination reaching the right press. Treat "no reorder" as a
   cheapness preference, not a rule. **But** `authoring.md` makes `simc-apl.md` Tier 1, so a
   reorder that puts a high rung below a low one contradicts the source. ⚠ **Do NOT say "a
   catalog's entry order IS the flattened `actions.default`"** — that is false for at least two
   specs (Havoc's `vengeful_retreat` is entry 1 at rung 5; Retribution puts `templars_verdict`,
   rung 54, above `divine_storm`, rung 53). The flatten is where a catalog STARTS, not an
   invariant it holds. What is true is narrower: **a cut preserves whatever order the catalog
   already authored**, so it cannot introduce a contradiction that was not already there.
7. ⚠ **The overflow clamp is `cols` AND `rows`.** Clamping columns alone rotates the bug — the
   row stops running off the right edge and starts running off the bottom, still outside the rect
   other UI anchors to.
8. ⚠ **ESSENTIAL vs UTILITY IS THE PLAYER'S LAYOUT, NOT A PROPERTY OF THE SPELL** — a catalog may
   never assert it. Four Tier-1 12.1.0 facts, written up symbol-anchored in
   `knowledge/addon-dev/cooldown-manager.md` §1.1: the two viewer mixins are identical
   method-for-method, both item mixins are bare
   `CreateFromMixins(CooldownViewerCooldownItemMixin)`, the two item templates differ in four
   cosmetic values (`50×50` vs `30×30` plus three font/inset numbers that follow from the size),
   and `legalOriginalSourceCategoryToTargetCategory` permits Essential ⇄ Utility ⇄ HiddenActive
   while `GetCooldownCategoryChangeStatus` declines to police it in Blizzard's own comment.
   **So a `viewer` field must NOT be built** — it would encode a user setting as authored data —
   and `Catalog.Check` counting every declared non-virtual entry is **correct**: an
   authoring-time upper bound against the panel the catalog ships. `Catalog.lua`'s comment says
   so. ⚠ Do not re-derive placement from `wowkb.spec_inventory`'s `Blizz cat` column; it is the
   DB2 default and reads convincingly like an answer.
9. ⚠ **A FORCED CHOICE IS NOT A VALIDATED ONE.** Havoc shipped in v0.22.0 with its fold in the
   only place a six-column panel allowed — and that place was wrong on both sides: `blade_dance`
   (`actions.default` rung 19, a 9-second rotational press) rode the cooldown row while
   `immolation_aura` (highest rung **2**, above Metamorphosis) headed the rotation row. It was
   forced by arithmetic and then **described as though it had been chosen**. The description was
   the defect. **When an authoring decision has exactly one legal answer, that is the moment to
   ask whether the CONSTRAINT is right**, not to record the answer as a choice. Fixed in v0.22.1
   by `grid = { cols = 7 }` + `break_before = blade_dance` (5 + 7).
10. ✅ **THE FOLD MEANS: top row = the cooldowns, bottom row = the rotation presses.** Decided
    2026-09-01, because three documents had given it three readings and they disagreed on Havoc.
    ⚠ **This is now a constraint, not a description** — a future break has to put the cooldowns
    above the line; it may not land wherever the partition rule leaves room.

---

## Phase 1 — Author the breaks ✅ LANDED 2026-09-01

Four catalogs author a break. Authored through `specs/<spec>/catalog.json`, never the generated
`Catalogs/<Spec>.lua`: `capart export catalog <spec>` → `capart build --all` →
`capart check --all`; a `catalog_gate_lua` byte-compares the Lua against the JSON.

| Spec | Placed | `break_before` | Split |
| --- | --- | --- | --- |
| Retribution | 9 | `templars_verdict` | 4 + 5 |
| Demonology | 9 | `implosion` | 5 + 4 |
| Protection | 9 | `avengers_shield` | 4 + 5 |
| Havoc | 12 | `blade_dance` | 5 + 7, on an authored `grid = { cols = 7 }` |

Devourer (6 placed + 1 virtual) and Destruction (1 shipped entry) fit one row and get no break.
All four are clean cuts — no reordering, no cue changes, no scenario churn.

**Protection's `shield_of_the_righteous` rides the top row and that is correct.** It is **rung 9**
of the Tier-1 APL, above `avengers_shield` (13/18), `consecration` (15/19/24/29) and `judgment`
(16/17/22). Moving it down would put a rung-9 action beneath rung-13 ones. The three further costs
of a reorder — a badge `catalog.md` argues would be dishonest, a partition that pins SotR to the
top row under every legal break, and ~78 positional references across four files — are in the
archive, §2.5c. Protection is the spec that makes correction 10 visible: SotR is a charged, held,
active-mitigation press that genuinely outranks the filler.

**PAUSE — CHECKED.** `busted` 392 passing / 0 failures / 2 pending, `luacheck` clean,
`capart check --all` exit 0, `check_capart_catalog_lua.py` 13/13, `kblint` 0, `citecheck` 57/57.

---

## Phase 2 — Fly the panel ✅ RELEASED; flight merged into Phase 3's, which passed

**v0.22.0** shipped the four breaks; **v0.22.1** corrected Havoc. Both are deployed via
`ghaddons`. **No client has drawn any of it.**

**PAUSE — WAIVED AS A BLOCKER 2026-09-01, by the author.** Phase 3 may be written before the
flight happens; the two flights merge into one.

**Why that is safe, and it is not a judgement call.** Phase 3 anchors other UI to the panel's
**rect**, and `gridSize()` (`Anchor.lua:459-462`) is pure arithmetic over `cols`, `rows`,
`cell_px` and `gap_px` — it never reads a placed frame, an icon position, or the roster's length.
So a wrong second-row y-offset draws icons misplaced *inside* a correctly-anchored panel, which
is visibly separable rather than confounded. Havoc's catalog-declared 7 columns is likewise
unit-tested (`anchor_spec.lua:717`), so the catalog tier is proven without a client.

### The merged acceptance set — answer these in the Phase 3 flight

Read with `uv run python -m wowkb.capture cap anchor`. ⚠ SavedVariables flush only on `/reload`
or logout.

1. **The second row draws BELOW the first.** Y points up, so descending a row is negative; a sign
   error draws row two *above* row one and the drift auditor reports zero drift either way.
   **Look at it.**
2. **The reading sort is top-descending, left-ascending.** `X{MISMATCH}` with matching ids either
   side of a differing `|` means right order, wrong number of rows.
3. ⚠ **The authored break holds across a talent change that REMOVES the break entry** — the
   fallthrough to the next present entry. **This is the oldest debt in the project** and was
   unexerciseable until Phase 1.
4. **`/cap grid` re-draws without a re-arm.** Set `7 2`, then `6 1`, and watch the row change.
5. **`/cap grid` reads back the tier.** Havoc should say **`7 (catalog)`** for cols — the first
   time the catalog tier has had a subject in a real client. `(yours)` / `(default)` for
   `icon_px`; `/cap grid reset` drops to the catalog's.
6. **A spec swap picks up that spec's own grid** — Havoc 7, everything else 6.
7. **Overflow leaves the row rather than stacking at its corner.** Force it: `/cap grid 3 1` on a
   9-entry spec should report `over:6`. In ordinary play `over:<n>` should be 0 — a steady
   non-zero usually means extra abilities enabled in the Essential viewer the catalog does not
   name.
8. **Parked frames stay out of the reading sort.** They sit at `+10000` above the panel and would
   sort ahead of row one.
9. **`icon_px` set at runtime** has never flown; only the token path has.

**PAUSE.** The set is answered from a capture and the answer written into `backlog.md`.

---

## Phase 3 — EllesmereUI — THE GOAL ✅ LANDED 2026-09-01 (v0.23.1)

**What landed.** `CombatAssistPlus/Ellesmere.lua` (new) registers `CAP_ROW`; `.toc` gained
`## OptionalDeps: EllesmereUI` and the file; `Anchor.lua` gained `Anchor.Row()` and notifies from
`resizeAnchor` and `regrid`; `Place.lua` gained `Handle:Place`, the one public way to record a
position handed in from outside. `tests/spec/engine/ellesmere_spec.lua` is 15 new assertions —
**407 passing**, 0 failures, 2 pending. The mover surface is written up as
`knowledge/addon-dev/cdm-rider-patterns.md` §4.8, off the 9.1.3 live install.

**Two decisions the steps below left open, now made and measured, not guessed:**

- **`getSize` returns UIParent units** — `Anchor.GridSize() × Anchor.Scale()`. Where a live frame
  exists the host computes `GetWidth() × GetEffectiveScale() / UIParent:GetEffectiveScale()`, and
  `getSize` fills that same slot. `ellesmere_spec` pins it.
- **`regrid` notifies while UNARMED too**, rather than inheriting its `P.armed` guard: `/cap grid`
  is legal with cap drawing nothing, and a mover anchored to an unarmed panel is anchored to a
  rect that just moved.

**The steps as approved, kept for the record:**


⚠ **The mined clone is gone and that is correct** (`raw/addon-research/ELLESMEREUI-REMOVED.md`) —
EllesmereUI is **All Rights Reserved** and the KB carries the facts. Per the `mine-addon`
doctrine: record facts and our own illustrations with provenance, **never copied code.**

⚠ **Facts below are from the live install at 9.1.3.** A live install updates itself, so
**re-resolve by symbol before relying on any line number.**

**The API spans two files.** `MakeUnlockElement` is in `EllesmereUI.lua:5066`; everything else
(`RegisterUnlockElements`, `NotifyElementResized`, `ReapplyOwnAnchor`, `ValidateStoredLinks`,
`SaveBarPosition` / `LoadBarPosition` / `ClearBarPosition`, `GetPositionDB`) is in
`EUI_UnlockMode.lua`.

1. **Add `Ellesmere.lua`**, loaded after `Anchor.lua`, entirely behind
   `if EllesmereUI and EllesmereUI.RegisterUnlockElements`. Add `## OptionalDeps: EllesmereUI` to
   the `.toc` so the base addon loads first.
2. **Register one element.** `MakeUnlockElement` is a **dot** call taking one options table, and
   it is **optional** — it only renames `savePos`/`loadPos`/`clearPos`/`applyPos` to the
   `…Position` forms, and `RegisterUnlockElements` applies the same aliases itself. Registration
   is a **colon** call taking an **array**: `EllesmereUI:RegisterUnlockElements({elem}, "cap")`.
   - `key` is a **single flat global namespace** across every addon — prefix it (`CAP_ROW`). Two
     addons using one key silently clobber each other.
   - `getFrame(key)` side-effect-free; every call site guards on its presence.
   - `getSize(key)` is **effectively required**: it feeds mover geometry and the cog's
     Width/Height boxes, and a returned `w < 10` is forced to 100, `h < 10` to 30. It may return
     a third value, a centre-Y offset. `Anchor.GridSize()` is the answer and needs no measurement.
     ⚠ **Decide which coordinate space it wants.** `gridSize()` returns **panel-local** units
     while the panel wears `icon_px / 50` as its scale (`Anchor.lua:794`), so effective screen
     size is `gridSize() × Anchor.Scale()`. Read the live install; do not guess.
   - `isHidden` takes **no arguments**. Return true whenever `Anchor.Ordering()` is false —
     which after principle (c) is exactly when cap draws nothing.
   - `isAnchored` is called **both with and without a key** in the shipped code. Tolerate both.
   - `noResize = true`; **omit `noAnchorTarget` and `noAnchorTo`** — that is what lets the power
     bars anchor to us.
3. **Point `savePos` / `loadPos` / `clearPos` / `applyPos` at `Place`'s store.** Mandatory:
   `SaveBarPosition` / `LoadBarPosition` / `ClearBarPosition` delegate to the element's own
   function and fall through to `GetPositionDB()` only when none is registered — and that fallback
   is the EllesmereUIActionBars profile table, `nil` in the base addon. Omit them and drags are
   silently lost.
   - ⚠ **`savePos` receives SEVEN arguments**, not four: `(key, cx, cy … )` — the CENTER/CENTER
     converted coordinates *plus* the pre-conversion point and relPoint as args 6 and 7.
     `ConvertToCenterPos` runs **before** the delegation check, so a registered element always
     gets centre-normalised values.
   - ⚠ **`loadPos` returns a single TABLE**, not four values: `{point, relPoint, x, y}`, and the
     resize path honours it only when both are `CENTER`.
   - **This is already `Place`'s convention** — `Handle:Capture` stores the frame's centre offset
     from UIParent's in UIParent units at scale 1.0, and `Place.lua:126-128` says so in as many
     words. Map `applyPos` → `Handle:Apply`, `clearPos` → `Handle:Reset`.
4. **Call `EllesmereUI.NotifyElementResized(key)`** (a **dot** call) when the panel changes size
   without a real `SetSize` on the registered frame. ⚠ `regrid()` in `Anchor.lua:1605-1608` is
   where this goes — it is already marked `@pending Phase 3` — and `resizeAnchor` (`:809`) is the
   other site. ⚠ `regrid` is guarded by `if not P.armed then return end`, so an unarmed build
   notifies nothing; acceptance items 4 and 6 are what prove this hook is live.
5. **Register early, then re-apply deferred.** ⚠ **The archive's "PLAYER_ENTERING_WORLD + 1 s"
   is conditional and does not hold on this machine.** That listener is created only
   `if not EAB` — and **EllesmereUIActionBars is installed here**, so `ApplySavedPositions` is
   driven from EAB's hooks instead (`OnInitialize` synchronously, `ApplyAll` after 0.6 s).
   Register at `PLAYER_LOGIN` and then call `EllesmereUI.ReapplyOwnAnchor(key)` deferred yourself;
   that is what makes the timing gate not matter either way.

⚠ **`noResize = true` costs one thing and it is not anchoring.** `ValidateStoredLinks`
(`EUI_UnlockMode.lua:1157-1215`) prunes stored width/height **matches** — and the rule is
**asymmetric**: a *child* with `noResize` is pruned unless it also declares `allowMatchSource`,
while a *target* with `noResize` is pruned unconditionally. **Anchors are pruned only for a
missing endpoint and never consult `noResize`**, so the goal is unaffected. It also runs on
unlock-mode *open*, not at login, despite its own comment.

**Write the EllesmereUI mover surface to `knowledge/addon-dev/`** as `[T3 obs]` facts with
provenance — facts and our own illustrations, **never copied code**. Cite the live install with
its version (**9.1.3**), since the pinned clone is gone.

### Flight 1 — 2026-09-01, v0.23.0

**It did not reach the goal, and the reason was cap's.** Registering the row gave the panel a
second writer, which exposed an absolute screen-space expectation in the drift auditor that had
been latent for as long as cap was the only one. `backlog.md` → `## Status` carries the
diagnosis; the short version is `stomp:0 reassert:0 contended:9` with `X{ok}` throughout, and
the fix is in v0.23.1.

| | Item | Result |
| --- | --- | --- |
| A | bars anchored, holding across reload / spec swap / regrid | ⛔ **blocked** by the loop — not answered |
| 1 | second row draws below the first | ✅ **passes** — looked at, confirmed |
| 5 | `/cap grid` reads back the tier | ➖ read on Protection, which declares no grid, so `(default)` was correct. **Needs a Havoc login** |
| 7 | overflow leaves the row | ⚠ **`over:1` in ordinary play** — the fold, not a bug in overflow. Protection now ships seven columns |
| 9 | `icon_px` at runtime | ✅ **passes** |
| 2, 3, 6, 8 | reading sort · break across a talent change · per-spec grid on a swap · parked frames | ➖ **not reached** |

### Flight 2 — 2026-09-01, v0.23.1 — the goal

**Part A passes.** The power bars and cast bar hold against the row across a reload, a spec swap
and a `/cap grid` change. Four capture sessions across Retribution, Protection and Havoc, every
header `contended:0`, `disp:0 cont:0` throughout with `reassert` climbing to 11 and 12 — the
healthy signature, not merely the absent one.

| Item | Result |
| --- | --- |
| A — the goal | ✅ **passes** |
| 1 second row below the first · 9 `icon_px` at runtime | ✅ passed on flight 1 |
| 2 reading sort · 4 regrid without re-arm · 6 per-spec grid on a swap · 8 parked frames | ✅ **pass** |
| 7 overflow | ✅ ordinary play reads `over:0` · ➖ forced case (`/cap grid 3 1`) not run |
| 5 tier readback | ✅ **closed** — Protection drew **4+7**, which only seven declared columns allow. The shape is proven; Havoc's chat line is another instance of it |
| 3 break across a talent change | ✅ **withdrawn — it was never a flight item.** `Anchor.Plan` is pure and `anchor_spec` has covered it since Phase 2 |

⚠ **Item 3 was carried across three releases as *the oldest debt in the project* and it was not
a debt at all** — `Anchor.Plan` is pure, `anchor_spec` had covered the fallthrough since Phase 2,
and the flight was being held open for something a unit test already answered. It survived
because this document kept restating it. **An item earns a place on a flight card only when the
CLIENT is the only thing that can answer it**; that is the test to apply before writing the next
one. `backlog.md` carries the full retirement, including the wrong prediction it produced.

**PAUSE — CHECKED.** The goal of the whole plan is reached. This is the point the plan named as
worth asking whether anything below is wanted at all: Phase 4 is a product decision, Phase 5 is
parked, and **neither is needed for the row to be anchorable.**

---

## Phases 4 and 5 — MOVED, 2026-09-01

Both are follow-up clean-up now, and each has its own document. **Read those, not this** — what
stood here has been deleted rather than duplicated, because two copies of a plan is how one of
them goes stale without anyone noticing.

- **Phase 4 → `backlog/fold-reading-model.md`**, and `backlog.md` → `## Now` points at it. It is
  a committed item blocked on one author decision, with a live gap behind it: no gate models the
  fold.
- **Phase 5 → `backlog/parked-work.md`**, and `backlog.md` → `## Ideas` points at it. Four
  unrelated parked items, none blocking anything.

---

## Open questions — ROUTED, 2026-09-01

All six have homes now and are **deleted rather than duplicated here**:

| Question | Where it lives |
| --- | --- |
| No gate models the fold | `backlog/fold-reading-model.md` → step 3 |
| `render-shelf.md` has no entry for the break; `havoc/catalog.md:10` says "single-row" | `backlog/fold-reading-model.md` → step 2 |
| Two elimination arguments cross the row boundary (Retribution, Protection) | `backlog/fold-reading-model.md` → *Why this is not cosmetic* |
| The break sits in front of a gold positive cue in two specs | `backlog/fold-reading-model.md` → step 1, third observation |
| Is the hatch alone worth binding a row outside the scanned line? | `discussion.md` → *Devourer*; `backlog/parked-work.md` §2 |
| `norow` conflates three causes | `backlog/parked-work.md` §5 |

Two KB gaps the plan carried — `ResizeLayoutMixin` self-sizing, and managed-frame ownership of a
viewer in its default position — went to `knowledge/_meta/kb-inbox.md`, which is the parking lot
for exactly that. **Both are unverified: write them only when measured.**

---

## Verification

- `busted` and `luacheck CombatAssistPlus` from the addon root. **Baseline: 407 passing**, 0
  failures, 2 pending (both "the lab is empty, by design").
- `uv run python -m wowkb.capart check --all` for any token **or scenario** change — **never a
  single spec name**. A token edit also makes every preview stale: run `capart build --all` first.
- `uv run python tests/check_capart_catalog_lua.py` from `tools/` — the emitter round-trip, the
  only thing covering a key no shipped catalog declares yet.
- `uv run python -m wowkb.kblint` and `wowkb.citecheck` for any `knowledge/addon-dev/` edit.
- `uv run python -m wowkb.obs check` gates a `--minor` / `--major` release.
- Read a flight with `uv run python -m wowkb.capture cap anchor`. ⚠ SavedVariables flush only on
  `/reload` or logout.

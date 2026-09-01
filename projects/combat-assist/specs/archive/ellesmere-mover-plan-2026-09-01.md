# Plan — breakpoints, a per-spec grid authors can ship, and then EllesmereUI

> Archived after its first phase executed. The three-tier grid it calls "Phase 2.5a" shipped;
> what remained was carried into a replacement plan at `../ellesmere-mover-plan.md`, which
> renumbers the phases and drops the `2.5x` decimals this file accumulated. **Read this one for
> the ARGUMENTS** — the Protection reorder refusal, the Destruction pilot correction, the
> generated-catalog discovery — which the replacement cites rather than restates.

**Status: an approved plan, not an authority.** A temporary migration artifact in the sense
`CLAUDE.md` gives that phrase, alongside `simplification-plan.md`. As each phase lands its
outcome goes to `backlog.md` → `## Status` and its promises to `spec.md`; this file is deleted
when the last one does.

---

## Context

**The goal is still to anchor EllesmereUI's power bars and cast bar to cap's CDM row** (Phase 3).
Everything else is groundwork. The row is `CombatAssistPlusRow`, a named panel with a saved
per-character position, drawn at an icon size cap owns.

**Phase 2 shipped on 2026-08-31 (v0.20.0, v0.21.0) and is unflown.** The panel's second row is
real: placement is two-dimensional, a catalog may name one `break_before`, the row split is part
of the capture's verdict, and a roster longer than the grid is held off the row rather than drawn
outside it. The grid — `cols` × `rows` × `icon_px` — became a player setting keyed on spec and
hero tree.

**What this plan adds** is the layer that turned out to be missing underneath all of it: **an
author cannot ship a grid.** The only per-spec knob is a player setting in SavedVariables, so a
catalog that needs seven columns has no way to say so, and a fresh install gets six and refuses
the break. Fixing that is what makes breakpoint authoring a free choice rather than an arithmetic
puzzle — the difference between Havoc's break being *right* and merely being *legal*.

⚠ **And one thing the earlier plan simply did not know: the catalogs are GENERATED.** Five of the
six come out of `specs/<spec>/catalog.json` via `wowkb.capart export catalog`, byte-gated. So
"author a `break_before`" is not a Lua edit — it is a JSON key plus exporter work in `capart.py`.
That is the single biggest correction here, and it gates every breakpoint below.

⚠ **What is BUILT is recorded in `projects/combat-assist/specs/backlog.md` → `## Status`**, in
detail, and is deliberately not restated here. This file is the forward plan; that one is the
record. `spec.md` §3.9 carries the promises (now **nine** properties — keep the count sentence
true).

---

## Status

| | | Ships as | State |
| --- | --- | --- | --- |
| **Phase 0** | Stand down beside another CDM rider | v0.15.0 | ✅ flown |
| **Phase 1** | The named panel, `/cap move`, `Place.lua` | v0.16.0 | ✅ flown |
| — | **Principle (c)**: no order ⇒ cap draws nothing | v0.17.0 | ✅ flown |
| — | Placement per-character; opinions per-account | v0.18.0 | ✅ flown |
| — | Rescale no longer moves the panel | v0.18.1 | ✅ flown |
| — | **cap owns the icon size**, not Edit Mode | v0.19.0 | ✅ flown |
| — | One icon-size knob | v0.19.1 | ✅ flown |
| **Phase 2** | Two rows; `break_before`; the split enters the verdict | v0.20.0 | **built, UNFLOWN** |
| — | Grid settable per spec; overflow held off the row | v0.21.0 | **built, UNFLOWN** |
| **Phase 2.5** | **Authored grid + breakpoints** | — | **START HERE** |
| **Phase 3** | EllesmereUI mover registration | — | **the actual goal** |
| **Phase 4** | Reading model, only if two rows carry a scan claim | — | needs a product decision |
| **Phase 5** | Mover-driven resize; `RegisterSkin` | — | half shipped, rest parked |

⚠ **Two releases are deployed and unflown.** That is not a blocker for Phase 2.5 — it is code
that compiles and is gated — but the acceptance sets in the v0.20.0 and v0.21.0 release notes are
the flight request, and **Phase 2's PAUSE is still not met**: it asks for the authored two-row
order across a talent change that removes the break entry, and no catalog authors a break to
remove. Phase 2.5 is what makes that flight possible.

---

## How to run this plan

**Stop at the end of every phase and wait.** Each phase ends with a `PAUSE` naming what should be
true before the next starts. Do not begin a phase because the previous one compiled — begin it
because the pause condition was checked.

⚠ **Releasing is not ask-first.** The standing authorization and its three gates are in
`projects/combat-assist/CLAUDE.md` § Releasing. The gate that matters: **the grant retires
*may I release?*, never *did the last flight pass?*** Cutting a release begins a flight; it does
not end one. Every release note must say **what it has not exercised**.

Before touching the addon checkout: `uv run python -m wowkb.addon pull --all` from `tools/`.
⚠ The addon is a separate gitignored repo, and each worktree carries its own clone.

---

## Corrections carried forward

Do not re-litigate these.

1. **`50 × iconScale` double-counts.** `SetScale` does not change `GetWidth`, so an item frame
   reads **50** wide at every setting. Every length in `tokens.row` is in the panel's own
   coordinate space. `anchor_spec` asserts it.
2. **cap owns the icon size**; Blizzard's Edit Mode slider does not reach it. `disarm()` hands the
   slider's value back.
3. **The `P.foreign` origin-adoption path was deleted.** An Edit Mode move of the viewer no longer
   drags cap's row.
4. **Asking EllesmereUI's maintainer to support cap is dropped.** `_G._CAP_IsOrderingEnabled` is
   published anyway and is already shipped (`Anchor.lua`, aliasing `Anchor.Ordering`).
5. **A duplicated constant is not caught by a test that only ever runs at the value where the
   duplicates match.** This cost two invisible defects; both now assert *distinct or absent*.
6. ⚠ **REORDERING A CATALOG IS NOT FORBIDDEN.** An earlier pass treated entry order as immutable
   and bucketed the specs on that assumption. That was wrong: a reorder is *allowed*, merely
   **bigger** than a cut, because moving an entry may require adding cues to keep the elimination
   model reaching the right press. Treat "no reorder" as a cheapness preference, never a rule.
   ⚠ **But the priority source still binds.** `authoring.md` makes `simc-apl.md` Tier 1 and a
   catalog's entry order *is* the flattened `actions.default`. A reorder that moves a high rung
   below a low one is not a layout choice, it is a contradiction of the source — which is exactly
   what killed the Protection reorder (2.5c). Reorder freely *within* what the APL leaves open;
   never across it.
7. ⚠ **The overflow clamp is `cols` AND `rows`.** Clamping on columns alone rotates the bug rather
   than fixing it — the row stops running off the right edge and starts running off the bottom,
   still outside the rect other UI anchors to. Both halves, always.

---

## Phase 2.5 — an authored grid, then the breakpoints

### 2.5a — A catalog can declare its own grid

⚠ **This is the prerequisite and it is not optional.** Today `Anchor.Grid()` resolves from exactly
two places (`Anchor.lua`, `grid()` ≈`:428`): the **global token** `ns.Style.row` and the
**player's** per-spec override in `ns.cdb.grid`. A catalog declares `abilities`, `entries`,
`hero`, `name`, `power`, `spec`, `talents`, `bar`, `break_before` — and no geometry. So a spec
whose roster wants seven columns cannot ship that way; only a player can set it, per character,
and a fresh install refuses the break that depends on it.

1. **Add an optional `grid = { cols = <n>, rows = <n> }` to the catalog schema.** Validate it in
   `Catalog.Check` beside `break_before` (`Catalog.lua`, the top-level block after the `bar`
   check): both fields optional, whole numbers, within `Anchor.Limits`.
   ⚠ **`icon_px` is deliberately NOT declarable, and `Catalog.Check` must reject it by name.** A
   catalog declaring geometry is fitting its *roster* — twelve entries need twelve cells — which
   is the author's business. Icon size is taste, and taste is the player's; a catalog shipping
   40px icons is imposing a preference rather than fitting anything. Letting an author set it
   would also re-open the authority inversion v0.19.0 spent a release closing, one level up.
   Reject it with a message that says which knob to use instead (`/cap grid`).
2. **Make resolution three-tier, in this order:** the **player's** override (`ns.cdb.grid`, set by
   `/cap grid`) → the **catalog's** declaration → the **token** `ns.Style.row`. The player must
   still win: they set it deliberately and per spec, and a catalog update must not silently move
   a row they placed. ⚠ `Anchor.Grid()` is a file-local `grid()` read by `gridSize()`,
   `rowScale()` and `apply()`; add the tier there so every consumer gets it, and do **not**
   re-derive geometry at any call site (`Anchor.lua` already forbids this in a comment).
   ⚠ `rowScale()` reads `icon_px` and must keep resolving it from **player → token only**, with
   no catalog tier, per the refusal above.
3. **`Catalog.Check` must validate the partition against the CATALOG's own grid**, not the token —
   otherwise a catalog that ships `cols = 7` is still refused a 7-wide row. It reads `ns.Style.row`
   today and must prefer `cat.grid`. It cannot call `Anchor.Grid()`: `tests/check_catalog.lua`
   loads `Catalog.lua` without `Anchor.lua`, which builds a frame at file scope.
4. **`/cap grid` reads back which tier each number came from.** It already prints `(yours)` vs
   `(default)`; add `(catalog)` so a player can tell a spec that ships a wide row from one they
   widened. `/cap grid reset` clears the player tier and falls back to the catalog's.
5. ⚠ **Say the tier out loud in `spec.md` §3.9's ninth property**, which currently says the grid
   is the player's with the token as default. It becomes: **the catalog proposes the shape, the
   player disposes, the token is the floor — and the icon size is the player's alone.**
6. **Teach `capart.py`'s catalog exporter to emit `grid`** into the generated Lua, alongside
   `break_before` (2.5c-bis). Both are new top-level keys and both must survive the
   `catalog_gate_lua` byte-compare.

**PAUSE.** `busted` green, `capart check --all` green, and `/cap grid` on a spec whose catalog
declares a grid shows `(catalog)` for `cols`/`rows` and `(yours)`/`(default)` for `icon_px`.

### 2.5b — Author the breakpoints

The bucketing pass (2026-08-31) classified all six catalogs. **Its arithmetic was done against a
fixed 6-wide row, so every "forced" or "refused" verdict in it is provisional on 2.5a** — with an
authored grid the constraint mostly dissolves. Re-derive rather than trusting the split.

| Spec | Placed | Recommended `break_before` | Split | Note |
| --- | --- | --- | --- | --- |
| **Retribution** | 9 | `templars_verdict` | 4 + 5 | Clean. 4/4 cooldowns over 5/5 rotation. **Do this one first** — it is the control. |
| **Demonology** | 9 | `implosion` | 5 + 4 | Clean. Implosion is on no timer; it is an imp-count spender. |
| **Havoc** | 12 | `immolation_aura` | 6 + 6 | Categorically right. Was *forced* by 6-wide arithmetic; after 2.5a re-check whether `blade_dance` (5 + 7, needs `cols = 7`) reads better. |
| **Protection** | 9 | `avengers_shield` | 4 + 5 | ⚠ `shield_of_the_righteous` rides the top row and **that is correct** — it is APL rung 9, above every rotation button. Do **not** reorder. See 2.5c. |
| **Devourer** | 5 placed | — | one row | ⚠ Blocked on a client action — see below. |
| **Destruction** | 10 *authored*, 1 *shipped* | — | — | ⚠ The shipped Lua is a **retired pilot**. Real design interleaves cooldowns; no clean cut, and blocked behind stage-6 transcription. See below. |

**All four of the specs with breaks are clean cuts** — no reordering, no cue changes, no scenario
churn. Ship Retribution first as the control (it is the one with no argument attached), then
Demonology, Havoc and Protection. Every one is a two-line change to a `catalog.json` plus a
regenerate, and reverting is the same change backwards.

### 2.5c — Protection: **do not reorder.** The "impurity" is the APL being right

⚠ **This reverses the earlier recommendation, on evidence.** `shield_of_the_righteous` sits at
index 3 between two cooldowns, and an earlier pass called that a compromise worth fixing by
reordering. It is not a compromise. **SotR is rung 9 of the Tier-1 APL**
(`knowledge/classes/paladin/protection/simc-apl.md`, `actions.default`), which is **above**
`avengers_shield` (13/18), `consecration` (15/19/24/29) and `judgment` (16/17/22). The catalog's
order matches the APL exactly, and `catalog.md`'s own table maps position 3 → rung 9.

**Moving SotR below those rows would place a rung-9 action beneath rung-13 actions** — i.e. the
reorder does not fix a layout wart, it contradicts the priority source. `authoring.md` makes
`simc-apl.md` the Tier-1 priority source and a live-patch copy of it a Stage-0 exit criterion.

Three further costs, each independently sufficient:

1. **It would force a dishonest badge.** `catalog.md` argues that SotR's current position is what
   makes the *absence* of an overcap cue on the generators correct — *"every generator sits below
   Shield of the Righteous at position 3, so at cap the walk stops on the spender and never
   reaches them."* Move it down and that mechanism is gone; `catalog.md` explicitly argues the
   replacement badge would be dishonest.
2. **The partition pins it to the top row anyway.** With 9 placed entries and 6 columns the legal
   break indices are 4–7, so `break_before` ∈ {`holy_armaments`, `avengers_shield`, `consecration`,
   `judgment`} and SotR is on the top row under **every** legal break.
3. **The evidence cost is large and entirely outside the Lua.** A reorder touches
   `specs/protection/catalog.json`'s `entries` order, **all 20** scenario row arrays in
   `scenarios.json` (each a positional 9-element array the elimination gate reads as authored),
   ~58 positional references in `scenarios.md`'s walk prose, 16 in `catalog.md` including four
   load-bearing arguments, and 4 in `fact-classification.md`.

**Therefore: author `break_before = "avengers_shield"` (4 + 5) and accept SotR on the top row.**
It is a charged, held, active-mitigation press that genuinely outranks the filler — the top row is
"what outranks the rotation", not literally "things on a timer", and Protection is the spec that
makes that distinction visible.

⚠ **Do not spend a `fable` agent on a reorder changeset.** If a later pass still wants one, the
prerequisite is a decision that the panel's rows may contradict the APL — a `spec.md` §3.1
question, not an authoring one.

### 2.5c-bis — Two facts that change how every break gets authored

⚠ **THE CATALOGS ARE GENERATED. Do not hand-edit `Catalogs/<Spec>.lua`.** Five of the six
(Demonology, Havoc, Protection, Retribution, Devourer) are produced from
`specs/<spec>/catalog.json` by `wowkb.capart export catalog <spec>`, and `Protection.lua:1-2` says
"Do not edit this file". A `catalog_gate_lua` byte-compares the generated Lua against the JSON. So
authoring a break means:

1. Add `break_before` to `specs/<spec>/catalog.json`.
2. Teach `capart.py`'s catalog exporter to emit it into the Lua.
3. Regenerate (`capart export catalog <spec>`), rebuild (`capart build --all`), re-check
   (`capart check --all`).

**This is a real chunk of work in `capart.py` that the earlier plan did not account for**, and it
must land before any break is authored for the five generated specs. Destruction is the exception
and is hand-written — and is parked anyway (2.5e).

⚠ **The addon computes no press at all**, which is why a reorder is cheap in Lua and expensive in
evidence. `Sense`/`Signal`/`Track` evaluate each entry's markers independently; `Anchor.Plan` walks
`entries` in array order and nothing keys off a specific index; `Catalog.OrderCheck` is a pure
diagnostic that *"never says what to press"*. The press is what the player's eye does, and it is
mechanised only in `capart.py`'s `reading_gate` → `elimination_gate` / `density_gate`. **The
authored scenarios are the only place the reading order is asserted**, so they are what any order
change has to pay for.

### 2.5d — Devourer is blocked on a client action, not on code

Devourer places **5** icons, not 6: `vengeful_retreat` lives in the **Utility** viewer, and
`Anchor.lua` re-anchors Essential only, so cap skins and hatches it but never gives it a cell
(`Catalogs/Devourer.lua`, the entry-6 comment). Five fit one row, and the catalog has exactly one
cooldown, so there is nothing to build a cooldown row out of.

**The fix is in Blizzard's UI, not here:** move Vengeful Retreat into the Essential viewer via
Edit Mode. Then Devourer is 6 placed with 2 cooldowns and a break becomes meaningful.

1. Write that down as a **setup instruction** wherever cap tells a player how to configure the
   Cooldown Manager, and in `Catalogs/Devourer.lua`'s header.
2. ⚠ **`Catalog.Check` over-counts by one per Utility-viewer entry** and cannot currently know —
   which viewer an entry lands in is a *comment*, not a field. Add an optional `viewer` to the
   ability declaration so the count is exact and the fact becomes machine-readable. The error is
   in the safe direction today (stricter, never looser), so this is latent, not urgent — but it
   is the same class of defect as the duplicated constants in correction 5.
3. Only author Devourer's break **after** the viewer move is confirmed in a client.

### 2.5e — Destruction: decidable on paper, not authorable in Lua. Mark it and move on

⚠ **The "one entry" reading was wrong and the correction matters.** `Catalogs/Destruction.lua` is
a **superseded 47-line pilot** — its own header says *"the minimal Destruction / Diabolist
authoring proof"* — and `specs/destruction/catalog.md` carries a **fully authored 10-entry
design** that explicitly retires it (*"It is gone, not deprecated"*). `backlog.md` names this as
*"the one place left in the project where a shipped catalog and its document disagree"* and says
**do not read the `.lua` as the design.**

The authored row order is: Soul Fire · Conflagrate · Summon Infernal · Immolate · Cataclysm ·
Chaos Bolt/Ruination · Shadowburn · Incinerate/Infernal Bolt · Rain of Fire · Havoc.

**On that real design Destruction is still a genuine (b).** Its press-on-sight abilities are Soul
Fire (1), Summon Infernal (3), Cataclysm (5) and Havoc (10) — scattered through the order, not
grouped — so no cut separates cooldowns from rotation, and the obstruction is real interleaving
rather than a short roster.

**Do not author Destruction's break as part of this plan.** Getting a break into the addon needs
stage-6 transcription first, and that is blocked on two things that are nothing to do with
breakpoints: the **scenario↔state gate refused** the transcription (three scenarios draw cues —
`capped`, `blocked`, `overcap` — that the pilot does not declare, and declaring them *is*
authoring), and Destruction is **the only spec never catalog-reviewed** (the 2026-08-25 pass
skipped it), which `backlog.md` says must happen **before** stage 6 runs. There is also an open
sidecar defect: `capart check destruction` compares the sidecar against itself and never reads
`scenarios.md`.

Mark it in `backlog.md` as **"break undecided — the shipped Lua is the retired pilot; the authored
10-entry order interleaves cooldowns, so no clean cut exists; blocked behind stage-6 transcription
anyway"** and move on.

**PAUSE.** A capture (`wowkb.capture cap anchor`) shows the authored two-row order drawn correctly
with `X{}` reporting a match, on at least one spec, **across a talent change that removes the
break entry** — which is Phase 2's outstanding PAUSE and the thing that closes it.

---

## Phase 3 — EllesmereUI — **the actual goal**

⚠ **The mined clone is GONE and that is correct.** `raw/addon-research/ELLESMEREUI-REMOVED.md`
records it: deleted per the `mine-addon` skill because EllesmereUI is All Rights Reserved and the
KB carries the facts. The facts below came from the **live install**, confirmed **9.0.8** on
2026-08-31. ⚠ A live install updates itself, so **re-resolve by symbol before relying on any line
number.**

⚠ **The API spans TWO files.** Verified by symbol presence:
- `…/AddOns/EllesmereUI/EUI_UnlockMode.lua` — `RegisterUnlockElements`, `NotifyElementResized`,
  `ReapplyOwnAnchor`, `ValidateStoredLinks`, `SaveBarPosition`, `LoadBarPosition`,
  `ClearBarPosition`.
- `…/AddOns/EllesmereUI/EllesmereUI.lua` — **`MakeUnlockElement`**, which is *not* in
  `EUI_UnlockMode.lua` despite being the constructor step 2 starts from.

⚠ EllesmereUI is **All Rights Reserved**. Per the `mine-addon` doctrine: record facts and our own
illustrations with provenance, **never copied code**.

1. Add `Ellesmere.lua`, loaded after `Anchor.lua`, entirely behind
   `if EllesmereUI and EllesmereUI.RegisterUnlockElements`. Add `## OptionalDeps: EllesmereUI`
   to the `.toc` so the base addon loads first.
2. Register one element via `EllesmereUI.MakeUnlockElement`:
   - Registration is a **colon** call taking an **array** —
     `EllesmereUI:RegisterUnlockElements({elem}, "cap")`; it uses `self`.
   - `getSize` is **effectively required**: it feeds mover geometry and the cog's Width/Height
     boxes. Without it plus `noResize = true` the cog shows size inputs that silently do nothing.
   - `key` is a single global namespace across every addon — prefix it (`CAP_ROW`).
   - `getFrame` side-effect-free. `isHidden` takes **no arguments**; return true whenever
     `Anchor.Ordering()` is false — which after principle (c) is exactly when cap draws nothing.
   - `noResize = true`; `noAnchorTarget` and `noAnchorTo` both omitted — that is what lets the
     power bars anchor to us.
3. Point `savePos` / `loadPos` / `clearPos` / `applyPos` at **Phase 1's `Place` store**. Mandatory,
   and proven: `SaveBarPosition` / `LoadBarPosition` / `ClearBarPosition` delegate to the element's
   own functions and fall through to `GetPositionDB()` only when no element is registered — and
   that fallback is the EllesmereUIActionBars profile table, `nil` in the base addon. Omit them and
   drags are silently lost. `loadPos` returns `{point, relPoint, x, y}`, canonically
   `CENTER`/`CENTER` from UIParent's centre — **already `Place`'s convention**.
4. Call `EllesmereUI.NotifyElementResized(key)` (**dot** call) when the panel's size changes
   *without* a real `SetSize` on the registered frame. ⚠ **`regrid()` in `Anchor.lua` is where this
   goes** — it is already marked `@pending Phase 3` — and `resizeAnchor` is the other site.
5. Register at `PLAYER_LOGIN` + `C_Timer.After(0.5, …)`, then call
   `EllesmereUI.ReapplyOwnAnchor(key)` deferred. EUI's login pass runs ~1 s after
   `PLAYER_ENTERING_WORLD` and re-applies everything registered by then; registering later is
   supported but nothing re-applies for you.

⚠ `noResize = true` costs one thing and it is **not** anchoring. `ValidateStoredLinks` prunes a
stored width/height **match** when either endpoint declares `noResize`. **Anchors are pruned only
for a missing endpoint and never consult `noResize`** — confirmed, so the goal is unaffected.

**PAUSE.** The power bars and cast bar are anchored to the row in `/eui` unlock mode and hold
across a reload, a spec swap, and a `/cap grid` change. **This is the goal of the whole plan**,
and the point at which it is worth asking whether anything below is wanted at all.

---

## Phase 4 — The reading model, only if two rows carry a scan claim

1. **Decide the product question first:** is the bottom row **the** scan with the top row a shelf
   you glance at, or is the scan row-major, top then bottom? Left to the pause after Phase 3 —
   easier to answer with a two-row panel on screen. ⚠ `spec.md` §3.9 already states this is open.
2. ⚠ **Bigger than it looks: `capart.py`'s row grammar is one-dimensional at its root.**
   - `parse_row` returns a flat `list[dict]`, and its comment states the model outright — *"the
     seam changes how the entry is DRAWN, never its rank."* **There is no notion of a row break.**
   - `elimination_gate` walks that flat list; `density_gate` slices a flat prefix; both are driven
     by `reading_gate`, whose only caller is `_check_one`.
   Until this is taught the traversal it will keep certifying a one-dimensional reading order the
   screen has stopped drawing.
3. Amend `render-shelf.md` **Part 0.5** and re-judge the treatments below it. Part 0.5 already
   names itself as the thing to edit.

**PAUSE.** This changes the product's reading model, not its plumbing. It needs a decision and a
flight, not a merge.

---

## Phase 5 — Half shipped, rest parked

1. **Mover-driven resize** — drop `noResize` and snap `setWidth` to whole cells so a drag picks the
   grid. The addon half is done: `/cap grid` writes the numbers and `regrid` re-applies. What is
   left is only letting a mover drag write them. ⚠ **Do not reach for this to solve overflow** —
   deriving the grid from the live roster re-makes it an *input* cap has to chase and makes the
   panel's rect roster-dependent, destroying "the rect is known at login", which is what Phase 3
   depends on.
2. `RegisterSkin` for cap's own windows (`Window.lua`, `StylePanel.lua`) — a separate documented
   API, touches no CDM frame, ships any time or never.

---

## Docs, as each phase lands

- `spec.md` §3.9 is at **nine** properties. Keep the count sentence true.
- `specs/backlog.md` → `## Status` — the only implementation-status block.
- Client facts to `knowledge/addon-dev/`, where the KB's gates apply. Still unwritten:
  `ResizeLayoutMixin` self-sizing, and managed-frame ownership of a viewer in its default
  position — **neither has been verified**, so write them only when measured.
- EllesmereUI's mover surface as `[T3 obs]` facts with provenance per the `mine-addon` doctrine —
  facts and our own illustrations, **never copied code**. Cite the live install with its version
  (9.0.8), since the pinned clone is gone.

---

## Verification

- `busted` and `luacheck CombatAssistPlus` from the addon root. **Current baseline: 377 passing**,
  0 failures, 2 pending (both "the lab is empty, by design").
- `uv run python -m wowkb.capart check --all` for any `render-tokens.json` **or scenario** change,
  and `capart export lua` to regenerate `Style.lua`. ⚠ A token edit also makes every preview stale;
  run `capart build --all` before `check`.
- `uv run python -m wowkb.kblint` and `wowkb.citecheck` for any `knowledge/addon-dev/` edit.
  Write new citations **symbol-anchored**.
- `uv run python -m wowkb.obs check` gates a `--minor` / `--major` release.
- Read a flight result with `uv run python -m wowkb.capture cap anchor`.
- **Phase 2.5 specifically:**
  - `tests/spec/engine/catalog_spec.lua` — the `grid` schema (both fields optional, bounds
    enforced, **`icon_px` rejected by name**), and the partition validated against the catalog's
    own grid rather than the token, so a catalog shipping `cols = 7` gets a 7-wide row.
  - `tests/spec/engine/anchor_spec.lua` — the three tiers: catalog-only, player-over-catalog,
    token fallback, and **`icon_px` ignoring the catalog tier entirely**. ⚠ The engine suite has
    no `UIParent` — stub it, as the existing grid tests do.
  - `catalog_spec`'s "validates every catalog the addon actually registers" must still return
    `{}` for all six after the breaks are authored.
  - `capart` — the exporter round-trip for `break_before` and `grid`, and `catalog_gate_lua` still
    byte-matching. ⚠ **Run `capart check --all`, never a single spec name.**

---

## Open questions

- **Which row is the scan** (Phase 4) — a product call, left to the pause after Phase 3.
- **Havoc's break after an authored grid.** At 6 wide the partition rule admits exactly one index
  (7, `immolation_aura`) so the break is forced. With `cols = 7` authorable, `blade_dance` (5 + 7)
  becomes legal and may read better — five cooldowns over seven rotation presses. Decide it with
  the panel on screen, not on paper.
- **Devourer's `viewer` field.** The optional `viewer` on an ability (2.5d) would make
  `Catalog.Check`'s count exact. Worth doing before any catalog approaches its grid's capacity;
  latent until then.
- **Does the top row mean "on a timer" or "outranks the filler"?** Protection forced this question
  (2.5c) and the plan answers *outranks the filler*, because that is what preserves the APL. If
  Phase 4 decides the two rows are a shelf plus a scan rather than one continuous scan, revisit —
  a shelf of "big cooldowns" is a different claim from a top half of "higher priority".
- **`norow` conflates three causes** in `Bind.lua` — API absent, info missing-or-secret, and no
  readable spell ID. Unrelated to this plan; worth splitting so the status line says which.

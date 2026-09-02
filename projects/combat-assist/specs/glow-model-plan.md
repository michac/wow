# The one-positive-cue model — prototype plan

**Status: a plan, not an authority.** Nothing here is declared. `spec.md` still owns the shipped
reading model, `render-shelf.md` still declares the shipped style, and this file is a temporary
artifact in the sense of `simplification-plan.md` — it is deleted when the prototype is either
adopted or discarded.

---

## Context — why this exists

Demonology shipped and was play-tested, and the author's read afterwards was that the row is
**too busy**, specifically in the number of negative cues it ended up carrying. The question is
whether a much simpler *output* reads better in combat, even if it conveys less.

The proposed model draws four primitives and nothing else:

- **keybind** (unchanged — V15 chrome)
- **one positive proc glow**, Blizzard's own square action-bar proc loop, the one Demonic Core
  puts on Demonbolt, repurposed and used far more widely
- **two hairline bars** along the bottom edge of the icon — one cooldown, one aura/summon duration

The reading rule inverts. Today it is *scan left to right and press the first button not ruled
out*. Under this model it is **press the leftmost lit button**. Cap orders the CDM row as best it
can so left-to-right is mostly right, and binds one or more glow conditions to each row; a row ORs
its conditions, a condition is an AND of terms, and the only thing a state can do is light or not.

A worked prototype of all twelve authored Demonology states in this vocabulary, with the real icon
art, the real flipbook and the real keybinds, is published at:

<https://claude.ai/code/artifact/05cdd4c8-c7d8-4ba7-a298-1edbfbea2c69>

It is a sketch of the model, **not the design of the catalog** — see "Author decisions" below.

### Why the author prefers it, in his own terms

1. It does not try as hard to tell you what you *can't* do. If the goal is to guide rather than
   instruct — and to support deliberately going off the primary APL rails, banking a cooldown —
   this does that better.
2. It is simpler visually. No tinkering with getting primitives right, and no new primitive each
   time a new kind of state shows up.
3. This proc is *known* to draw the eye in combat. That is not a guess.
4. As an extension of (1): it can be ignored.
5. It can be extended later with a little more aura metadata — a stack-count readout — and is
   functional without it.

### What it costs, recorded honestly

- **The row stops saying why.** A banked summon and a summon on cooldown are both dark, separated
  only by the absence of a swipe.
- **Rank is gone.** Two lit buttons say "both are fine"; the order is row order, and row order is
  now doing work the badges used to do. Cap can no longer recover from a wrong CDM order the way
  Retribution's promoted opener does today.
- **Every band needs a threshold.** A badge can hold at a boundary; a glow must pick a moment to
  switch on, and a wrong threshold is invisible — nothing on screen looks broken.
- **Glow inflation is the live risk.** If too many rows light, the cue stops meaning *now* and
  starts meaning *off cooldown*, which the swipe already said.

---

## Grounding — checked after the 2026-09-02 sync

This plan was first drafted against a checkout that was 73 commits behind `origin/main`, which
made several parts of the pipeline look missing when they were only absent locally. That is
resolved; what follows was re-checked against the synced tree and the shipped addon (v0.23.6,
`207db86`), and the earlier "this doesn't exist yet" claims are deleted rather than annotated.

What the sync settled:

- **The tokens do not live in `render-shelf.md` any more.** They are `specs/render-tokens.json`
  (Part 7's in `specs/render-lab.json`, the primitives page's in `specs/render-primitives.json`);
  Part 6 now documents what each group *means* and the JSON carries the numbers. **Edit the JSON,
  not the shelf prose.**
- **The nine cues reconcile.** `render-tokens.json` and the shipped `Style.lua` both declare
  `aoe_only · blocked · building · capped · noproc · overcap · priority · st_only · starved`.
- **`Catalogs/<Spec>.lua` is generated**, by `uv run python -m wowkb.capart export catalog <spec>`.
  It is not hand-transcribed; the catalog is authored in `specs/<spec>/catalog.md` and exported.
- **There are six catalogs now**, not five — Protection shipped and has flown.
- **The positive-cue budget is gone** (backlog, DONE 2026-09-01). A second, third or tenth
  positive cue is allowed; the invariant `check` actually asserts is that **no single entry wears
  more than one positive cue**, so "scan for a positive cue" always has one answer.

Still true, and still the reason Phase 0 exists: **the addon sub-repos sync independently of this
one.** Run `wowkb.addon pull --all` in whatever worktree you release from before touching Lua.

---

## Author decisions already made

These are settled; do not reopen them while executing.

1. **The glow catalog is authored FROM THE APL**, following `authoring.md` stage 1, *not* by
   mechanically inverting the 17 markers in the shipped `Catalogs/Demonology.lua`. Inverting the
   markers would bake in the badge model's decomposition of the rotation and inherit its blind
   spots. The shipped catalog is a **cross-check**, not the input.
2. **Blizzard's own proc glow is suppressed on rows cap has an opinion about**, so there is
   exactly one glow on the row and cap owns it. This costs Blizzard's proc information on those
   buttons and that is accepted.
3. **No variant toggle, no `Variant.lua`, no second registered catalog.** This is a personal-use
   addon; a throwaway release cut from a branch of the **addon repo only** is an acceptable way to
   fly it, and reverting afterwards is cheap. The outer repo stays on its normal single line of
   history — a shelf edit that loses is one `git revert`.

---

## The seams — verified against the shipped addon

| Seam | Where | What it does today |
| --- | --- | --- |
| Which catalog loads | `Catalog.lua:147` `Catalog.ForBuild(specID, subTreeID)` | First registry match on spec+hero; an unheroed catalog is the loose fallback. |
| **What a verdict draws** | `Treatment.lua:76` `Treatment.For(verdict)` | Pure, ~30 lines, no client API. Returns `{scan, cues, hatch, skip, winner, badges}` and `Overlay.paint` (`Overlay.lua:415`) drives Show/Hide straight off it. **This is the render branch point.** |
| Hatch derivation | `Treatment.lua:88-96` | `hatch` comes from `verdict.oncd` (or, on a virtual row, the complement of `member`); `scan` from `verdict.member`. Neither is catalog-declared, so both must be suppressed explicitly. |
| Negative-by-default | `Treatment.lua:78-81` | `skip = true` for any cue whose polarity is not `positive`, and `skip` draws the red ruled-out hatch. **A new cue that forgets `polarity = "positive"` will draw a proc glow and a red hatch on the same button.** |
| Flipbook animation | `Paint.lua:386-395` `Paint.FlipBook` | A real `FlipBook` AnimationGroup (`SetFlipBookColumns/Rows/Frames`), not a Lua texcoord walk. **Host-agnostic — it takes a texture, so it drives a full-rect texture unchanged.** Requires an unpadded sheet. |
| The closest existing thing | `Paint.lua:411-449` `Paint.PromotionRing` | V14. Same `FlipBook` helper over `Media/procring.tga`, `spread` 2.0, 32 frames at 30 fps, `SetBlendMode("ADD")`, frame 0 set by hand so `Show()` never flashes the sheet. But it is **corner-anchored to the winning badge** (`Overlay.lua:464-476`), not to the icon rect. |
| Z-banding | `Paint.lua:86` `Paint.Z` | `{edge=1, skip=2, corner=3, positive=14, negative=24, ranks=10}`. `Paint.CueLevel(polarity, rank)` = band + (ranks − rank). The row overlay frame *is* the icon rect (`Overlay.lua:309-316`), so anything `SetAllPoints` on it is full-icon. |
| Blizzard's glow | `Glow.lua` (65 lines) | `hooksecurefunc(frame, "RefreshOverlayGlow")` per item frame, weak-keyed, writes `frame.SpellActivationAlert:SetAlpha(ns.Style.surfaces.proc_glow_alpha)` (0.5). Global `live` flag; `Glow.Restore()` writes 1 back to every frame ever hooked. Driven off `ns.Sense.OnVerdicts`. **Suppression is a value change, not new plumbing.** |
| The gallery | `StylePanel.lua:136-162` | Enumerates `ns.Style.cues` automatically — a new cue key appears in `/cap style` for free. Draws through the same `ns.Paint.Badge` the live overlay uses. |
| The lab | `StylePanel.lua:200-211`, `:320-329`; `Lab.lua` | `ns.LabStyle` may be named by `Lab.lua` and `StylePanel.lua` and nothing else; the reach gate enforces it. The `DRAWS` handler table currently holds only `count-glyph` and `duration` — a new lab entry shape needs a new handler. |

**There is no existing cap-owned animated full-icon-rect primitive.** The only full-rect cap
textures are the two static stripe hatches (`Paint.Hatch`, `Paint.lua:296-372`); the only animated
ones are `Paint.FlipBook` (badge sprites and the promo ring, both corner-anchored) and the
`Paint.Breathe`/`Paint.Glow` alpha loops. This is the one genuinely new primitive.

---

## A defect found on the way — fix it first

`StylePanel.lua:141`, `:152` and `:174` read `ns.Style.cues[key].slot`. **`Style.lua` carries no
`slot` field** — it was removed when the badge stack began to flow (`git log -S'slot = 3'`,
`88bff54`); badges are positioned by `Paint.CueLevel` / `Paint.StackOffset` now.

- `:141` is harmless (`nil ~= nil` is false, the sort falls through to alphabetical).
- `:152` `key .. " · " .. cue.slot` — **concatenates nil, throws.**
- `:174` `filled[slot] = true` — **nil table index, throws.**

`buildStyle` (`:480-494`) calls `buildCues` and `buildSlots` with no `pcall`, so **`/cap style` on
the Style tab errors today.** Nothing caught it because `tests/spec/engine/window_spec.lua:1-2`
records that nothing in the repo has ever called `CreateFrame`, so only `RowWidth` / `TabIndex` /
`CanDraw` are covered.

This matters here because the gallery is the cheap first look at the new treatment. Fix the three
sites and the two section captions that still say "each in its own slot" / "all three slots".

---

## Open questions to settle on the desktop

**Q1 — where does the glow art come from?** Three candidates, in the order they should be tried:

- **Use the client's own atlas at runtime.** `texture:SetAtlas("ui-hud-actionbar-proc-loop-flipbook")`
  and drive `Paint.FlipBook` over it. Ships zero art, is exactly Blizzard's, and cannot drift.
  Needs verifying in-client that the atlas resolves and that a `FlipBook` animation composes with
  `SetAtlas` — that is an `addon-lab` question, which is the documented instrument for it.
- **Re-author it, the way the ring was.** `previews/assets/vfx/procring.png` is *generated* by
  `wowkb.procring`, modelled on this same flipbook, whose radial profile and per-frame energy were
  measured; it is white-RGB with the shape in alpha only, so `SetVertexColor` reaches any hue —
  "the one way it beats the original, which is baked gold". A `wowkb.procloop` doing the same for
  the square form would be reproducible, tintable and unambiguously ours.
- **Ship `procloop.png` as a `.tga`.** Simplest, and probably wrong: it carries a baked hue, and
  `previews/assets/vfx/README.md` records the vfx sheets as being for measurement and the preview,
  **not** for the addon's `Media/`.

**Recommendation: try the atlas first, fall back to re-authoring.** Do not ship the measured sheet.

**Q2 — should the glow be a cue key at all, or its own token group?** A cue entry in
`render-tokens.json` is shaped like a corner badge: `frames` is a list of Kenney sprite names
resolved against `badges.asset_root`, with `duration_s`, `loop`, `rank` and an optional `glow`.
A full-icon flipbook is none of those. **The strongest in-tree precedent says take the group:**
V19's pandemic badge and V20's proc bar were *not* added as cue keys — each became its own
top-level group beside `promotion`, which is itself a flipbook group (`cols`/`rows`/`cell`/
`frames`/`fps`/`spread`/`tint`) and is the exact shape this wants. Settle this before writing
anything, because it decides whether Q4's rank gates apply at all.

**Q3 — which `Paint.Z` band?** The glow must sit above the icon art and the swipe (automatic — the
overlay frame is already lifted +10 above the item's highest child) and, under the declared reading
model, **below the negative band (24)** so an eliminating mark still wins. There is no band
reserved between `skip = 2` and `corner = 3`. `presentation_spec.lua` asserts against `Paint.Z`, so
adding a band is a test-visible change.

**Q4 — the gates, if Q2 lands on "cue key".** Ranks must be unique integers, and every positive
must rank numerically above every negative — `priority` is 1, `capped` is 2, `blocked` is 3, so a
new positive needs rank **0**. And **every declared cue must be worn by some scenario row in some
built spec** (the union of all six, not just the one being checked), so a cue key added with no
scenario wearing it fails the build — which means the shelf edit and the Demonology scenarios walk
have to land together. If Q2 lands on "own token group", none of this applies.

---

## The work, in order

**Phase 0 — land on the desktop.** `wowkb.addon pull --all` in the worktree you will release
from. Read `specs/backlog.md` → `## Status` for what has flown since this was written, and settle
**Q1 and Q2** — they decide the shape of everything after. There is also a remote branch
`wt-cap-demonology` worth a look before starting.

**Phase 1 — ground the rotation.** `authoring.md` stage 1, from the Tier-1 APL:
`uv run python -m wowkb.simc warlock demonology`. Author the glow conditions from the APL's rungs
directly. Cross-check against the shipped catalog's 17 markers *afterwards*, and record anything
the APL pass missed that the badge model caught — that list is the real evidence about whether the
model loses information.

**Phase 2 — the treatment.** Resolve Q1, then add the glow to `specs/render-tokens.json` — as its
own group if Q2 lands that way — document what the group means in `render-shelf.md` Part 6, and put
the reasoning and the rejected alternatives in `render-rationale.md`. Fix the `/cap style` slot
defect. `capart export lua` (plus whatever art target the answer to Q1 implies), then look at it:
`previews/primitives.html` for the primitive in isolation, `/cap style` for it at real size on
cap-owned frames in the client. Do this before writing any catalog.

**Phase 3 — the catalog.** `specs/demonology/catalog.md` rewritten to the positive vocabulary, a
new `scenarios.md` walk, `fact-classification.md` updated, then
`capart export catalog demonology` — the Lua is generated, never hand-edited — note that two of the catalog's
recorded **defeats** (Power Siphon's sealed Core-stack gate, Dreadstalkers' two-sided Reign band)
may become expressible, because a glow needs no branch to choose a glyph the way a badge does. If
so that is a real change to the safety case and gets written as one.

**Phase 4 — the renderer.** The `Treatment.For` branch (suppress `scan`, `hatch`, `skip`; return
the glow), driven by a catalog-level declaration rather than a global mode so the other five specs
are untouched. The new `Paint` builder. `Glow.lua`'s suppression per decision 2 above.

**Phase 5 — tests.** `presentation_spec.lua` for `Treatment.For` under both shapes;
`catalog_spec.lua` for the new declaration; an `OWNER` entry in `surface_spec.lua` for the new
Paint object, or it is unguarded. Note `style_spec.lua` asserts `Paint.lua` contains no
`C_Timer.NewTicker` — the FlipBook AnimationGroup satisfies that, a Lua frame-stepper would not.

**Phase 6 — fly it.** Branch the addon repo. `uv run python -m wowkb.addon release cap` (which
gates on luacheck → busted → luaparser), deploy, play. Read the flight with
`wowkb.capture cap draw`; `specs/flight-reading.md` says what the stream can and cannot prove.
**Releasing is ask-first, every time.**

**Phase 7 — keep or revert.** If it wins: merge the addon branch, and consider collapsing the new
key with `priority`, which would then mean nearly the same thing. If it loses: revert the shelf
commit in the outer repo, cut a release from addon `main`, and record the reasoning in
`render-rationale.md` — the displaced model belongs there, not deleted.

---

## Verification

- `uv run python -m wowkb.capart check --all` — the shelf gates, the reading chain, asset equality.
- `uv run python -m wowkb.capart build --all` then look at the served preview; the preview is the
  only thing that can tell you the row *looks* right, and `check` says so itself.
- `busted CombatAssistPlus/tests/spec` from the addon repo root (config in `addon/.busted`).
- `/cap style` in the client for the treatment at real size on cap-owned frames.
- In-game: `/cap` on Demonology, pull something, `/reload` to flush SavedVariables, then
  `uv run python -m wowkb.capture cap draw`.

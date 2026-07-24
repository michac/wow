# Addon engineering program — lab, KB, skill, and the Cooldown HUD refactor

> **STATUS: PLANNED, not started (2026-07-23).** This is the driving document for a
> multi-session effort. Nothing in W1–W4 has been built. Read §"Where things stand"
> before picking anything up — a fair amount of groundwork already exists and you
> should not redo it.
>
> **Cooldown HUD feature work is FROZEN** until W4's audit lands. Bug fixes are fine;
> new indicators are not. The freeze is deliberate: the defects that triggered this
> program were structural, and adding surface area before fixing structure just makes
> the audit bigger.
>
> Doc map: `knowledge/addon-dev/README.md` = the addon-dev KB this program feeds and
> consumes · `projects/cooldown-hud/docs/` = the HUD's own design docs ·
> `knowledge/_meta/kb-inbox.md` = the parking lot that points here.

## Why this exists

The Cooldown HUD reached a point where **every defect was a seam defect, not a logic
defect**: the same fact stored in two places, two consumers of one cache with only one
refreshed, decisions smeared across three modules, and a render bug nobody could
diagnose because nothing was instrumented to see it. Grinding out more features
against that structure was the wrong move.

Underneath that sat a deeper problem: we were developing by trial and error against an
API we had no reference for. So the program has two halves that feed each other —
**build the reference** (W1–W3), then **use it to fix the code** (W4).

## Workstreams

Dependencies: W1 → W2 → W3, and W2 → W4. W3 is not a hard blocker for W4 but makes it
much cheaper. Do not start W4 before W2, or the audit will be measured against
unverified rules.

---

### W1 — The lab addon

**A long-lived scratch addon that exists to answer questions about the client.** Not a
product, never shipped to anyone, never released.

Its whole point is to be the place where experimental API-poking lives, so it stops
accreting inside real addons. Today CDMProbe carries `skin`, `resource`, `single`,
`multi`, `aoe` and `gradtest` alongside its actual product, plus **458 lines of code
documented as "retired direction" / "DORMANT — unwired"** (`Skin.lua`, `Resource.lua`,
`HudTint.lua`).

> **Correction (2026-07-23, from the W1 exploration).** An earlier draft of this
> paragraph also claimed **three competing `reset` registrations** (`HudCore.lua:690`,
> `Probe.lua:664`, `Resource.lua:282`) "of which two are dead by load order". The line
> numbers are right; the reading is wrong. It is a deliberate **decorator chain**:
> `Probe.lua` defines the base, and `Resource.lua` + `HudCore.lua` each capture
> `ns.commands.reset.fn` as `prevReset` and call it, so `.toc` load order *is* the
> composition order and all three run. `ns.RegisterCommand` (`Core.lua:76-79`) only
> appends to `commandOrder` on first registration, so one help entry results. **Nothing
> is dead.** Likewise the "458 retired lines": only **`HudTint.lua` (72)** is genuinely
> dormant — `Skin.lua` (90) and `Resource.lua` (296) are retired *directions* but are
> loaded and reachable from four call sites. W4a is scoped from this paragraph, so it
> inherits the corrected figures: **72 provably dead lines**, not 458, and no dead
> command registrations.

**Rules that keep it safe:**
- Never released through `ghaddons`; copied straight into `Interface/AddOns/`.
- **Not** in the `wowkb.addon` registry — it is not one of the three product addons.
- No version discipline, no release checklist, no deploy ceremony.
- **Nothing in a product addon may ever depend on it.** This is the invariant that
  makes it safe to leave junk lying around in there.
- Source lives in this repo so runs are reproducible.

**Populate it from the KB's open questions.** `knowledge/addon-dev/` carries ~68
`@verify-ingame` hits; roughly 11 are per-file "nothing here has been run in the
client" banners rather than real questions. The genuine ones sort by mechanism:

| Mechanism | Examples |
|---|---|
| **Call-and-record** | `type(require/os/io)`; `table.freeze` / `isfrozen` / `removemulti`; `strsplittable`; whether `string.rtgsub` is callable by addons; `C_AddOns.DoesAddOnExist("LibStub")`; `geterrorhandler`; `C_EventUtils.IsCallbackEvent` on flagged vs unflagged; whether SecureOnly globals resolve to nil for addons; whether deprecated `UIDropDownMenu_*` still work |
| **Scratch-frame behaviour** | frame levels 0–10000, the +1 child default and clamping; draw-layer ordering; whether texture sources are mutually exclusive (`GetTexture` after `SetAtlas`); `CreateFontString` 4th argument; `SetTextColor` semantics |
| **Animation semantics** | what an alpha/vertex animation leaves behind when it stops **without** `setToFinalAlpha` — directly load-bearing for the HUD's cue |
| **Event mechanics** | `RegisterUnitEvent` four-unit cap; `RegisterAllEvents` + `UnregisterEvent` interaction; unregistering an unregistered event; whether hiding a frame blocks dispatch; the unhookable list |
| **Lifecycle observation** | `ADDON_LOADED` ordering; `PLAYER_ENTERING_WORLD` flags on reload vs login; `ADDONS_UNLOADING` |
| **XML surface** | what `<Color>` compiles to; addon-declared `intrinsic`; `<ScopedModifier>` |

⚠ **The container questions need a generator, not the lab itself.** TOC-tag legality
(`AllowLoad`, `AllowLoadGameType`, `AllowLoadTextLocale`, `Secure`, undocumented tags),
load order, load-error semantics, missing `OptionalDeps`, dependency transitivity and
nested-`.toc` libraries are all tests **on the addon container**. The lab cannot test
them in its own `.toc` — malforming it would break the lab. These need small generated
sibling addons written into `AddOns/` per test.

**Stays in CDMProbe, does NOT move to the lab:** anything that observes the HUD itself
(cue watchdog, pull recorder, `hud status`/`log`/`binds`) and the Cooldown-Manager /
secret-value seam. That last one is a working regression harness — `probe` +
`probe-baseline.json` + `wowkb.cdmp` — and breaking it up would lose a safety net.

**Not answerable by any addon, so don't try:** the visual `SetVertexColor` /
`SetGradient` composition question (no pixel readback exists — the player is the only
sensor), and adoption/popularity data (CurseForge 403s).

---

### W2 — Run the lab, read its output, update the KB

1. Run it in-game once; it writes SavedVariables.
2. A local reader (a `wowkb` module, alongside `wowkb.cdmp`) parses that file.
3. Resolve `@verify-ingame` markers: **edit the claim, drop the marker, re-verify.**
   The KB's own `[gap]` markers get upgraded to facts, or stay gaps with better
   evidence about *why*.

**Doctrine, inherited from `projects/cooldown-hud/docs/m4.5-t3-plan.md` and it holds
here too:** *collect* a new observation → addon change; *assert / interpret /
re-verify* → local tooling, no addon change. So the lab collects raw answers and the
expectations live in local JSON, not in shipped Lua.

Every corpus count in the KB is **build-pinned to 12.0.7.68887**. Re-check after any
`git pull` of `raw/addon-research/wow-ui-source`.

---

### W3 — A `wow-developer` skill

A skill that knows to consult `knowledge/addon-dev/` for addon-development questions,
and the main game KB for game questions — and knows the difference. Note that
**"Tier 1" means different things in the two subtrees** (`_meta/sources.md` vs
`addon-dev/sources.md`); the skill must not conflate them.

Should trigger on addon work in any of the three product addons plus the lab.

---

### W4 — Audit and refactor the Cooldown HUD

**4a — Remove test code.** Move what belongs in the lab, delete what is dead. Start
with **`HudTint.lua` (72 lines)** — per the W1 correction above, that is the only
provably dead code in the addon; the `reset` chain is a live decorator chain and
`Skin.lua` / `Resource.lua` are reachable, so removing them is a *scope* decision
("we no longer want this direction"), not a dead-code sweep, and each has to be
unwired from its call sites first. "Kept as reference" is still not a justification —
git history is the reference — but the two cases need different arguments.

**4b — The three-layer split.** This is the core of the refactor:

- **Game-state abstraction** — one place that unions everything readable with the
  napkin math. Today state reads are scattered and the napkin is a separate module
  consulted ad hoc.
- **Rotation engine** — class/spec specific. Takes the state abstraction, emits
  **well-defined cues and sequence-state**. Pure data in, data out, **no API calls**.
- **Display engine** — renders cues and sequences. **No decisions.** Today `SetCue`
  still maps level→palette key, turns emphasis into a fill fraction and picks a side,
  while `HudState` makes further decisions immediately before calling it.

The KB's `module-architecture.md` documents Blizzard's own precedent for this
(data mixin with zero widget calls vs display mixin with an idempotent refresh), though
that file is `confidence: medium` — the platform mandates little here, so most of it is
Tier-3 pattern reporting. Treat it as corroboration, not as a spec.

**4c — A test mode.** Once the display engine is purely data-driven, feed it dummy
cue/sequence data so the UI can be refined without triggering real game state. This is
the payoff that makes 4b worth doing: today every visual change needs a dummy pull.

**4d — Unit tests for the rotation engine.** It takes data and emits data and touches
no API, so it is fully testable under `busted`. The existing harness
(`CDMProbe/tests/mock_ns.lua`, 33 tests) is the starting point.

**4e — Independent code reviews.** Several, deliberately not one:
- against the addon-dev KB's ~200 audit rules;
- general architecture / separation of concerns;
- code duplication (the keybind lookup being queried from several places is the known
  example; there will be others).

These are a good fit for a workflow with one agent per lens plus adversarial
verification — the pattern that produced the KB.

## Where things stand (2026-07-23)

**Already done, do not redo:**
- **`knowledge/addon-dev/` exists** — 9 files, ~10,400 lines, ~200 numbered audit
  rules, anchored to `wow-ui-source @ 4383ced` (build 12.0.7.68887) with `file:line`.
  Built by a 3-phase workflow (source registry → per-topic research → adversarial
  verification). **124 of 438 claims were refuted and corrected in verification** —
  a 28% error rate in careful first-pass research, which is the number to remember
  before trusting any unverified agent output.
- **Two tools were built and are untracked**: `tools/wowkb/uiapi.py`, `tools/wowkb/wiki.py`.
- **Reference clones** in gitignored `raw/addon-research/`: `wow-ui-source` (12.0.7.68887),
  WeakAuras2, BigWigs, Plater, Details, Ace3, Bagnon.
- **`/cdmp gradtest` facts, measured on 12.0.7 and recorded in
  `projects/cooldown-hud/probe-baseline.json`:** `SetColorTexture` does **not** write
  the vertex colour; `SetGradient` **resets** it to white; `SetVertexColor` works and
  is readable back. A `gradient-clobbers-vertex-colour` assumption is seeded so a
  Blizzard change surfaces as a diff.
- **CDMProbe is at v0.28.1.**
- **A discarded first attempt at the KB** is parked on branch
  `archive/addon-dev-research-v1` (commit `a177464`). It was scoped too narrowly around
  our own bugs. Do not restore it; the lesson is recorded below.

**Still open:**
- The intermittent white cue is **not solved**. A sufficient mechanism exists (white
  base + hue living only in the vertex channel + any neutral rewrite of that channel),
  but it is unconfirmed, and the KB independently records the composition question as
  unestablished at every tier. Needs human eyes.
- `cooldown-read-combat-seam` has never been confirmed from a **single session** —
  `wowkb.cdmp` now refuses to assert it across mixed captures.
- Grimoire shows a JUDGE cue despite `ns.SpecNoCue`; observed, not diagnosed.
- Whether to rename CDMProbe (its product is a HUD; the name is a fossil). Costs a repo
  rename, a `ghaddons` config change and a SavedVariables key migration. Not now.

## Lessons worth not relearning

- **A concrete list of questions in an agent prompt becomes the outline**, whatever the
  surrounding prose says about scope. The first KB attempt was scoped to seven of our
  bugs and came back organised around them; a mid-flight correction could not undo the
  anchoring. Derive a topic map from the domain *before* mentioning current problems.
- **Verify agent output before relaying it.** Two results this session were confidently
  wrong and caught only by spot-checking citations against the source.
- **Do not assert a mechanism from a screenshot, or from an instrument you have not
  validated.** Both happened; both produced confident wrong answers that cost releases.
- **An instrument that cannot observe its subject must say so**, not emit a number. The
  first cue watchdog read `GetVertexColor` — a channel the paint path never writes —
  and reported white for every level including ones that render green.
- **Long background work dies when the machine sleeps.** A workflow resume recovers
  *completed* agents only; in-flight work is lost.

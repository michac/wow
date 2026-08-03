# Cooldown HUD — the virtual CDM panel

> **STATUS: PHASE 1 SHIPPED (2026-07-30) — awaiting its in-game pass.** Written 2026-07-30
> straight out of the first Destruction live pass, which quantified the hole this closes:
> **31 % of decision changes had no winner** (59 of 191, every one at 0–2 shards).
>
> ⚠ **The approach changed at implementation, and it is a better one — see
> *§ The reframe* below.** Virtual rows are **DETECTED from the spec's own ability table**,
> not declared with a per-ability flag, and the justification for the fences changed with it.
> Phases 1 and 3 collapsed into one as a result: Demonology's Shadow Bolt needed **zero**
> edits, which is the sharpest possible proof that the seam is per-spec *data*.
>
> **Doc map:** the design pillars this has to answer to are `design.md`; the pipeline is
> `architecture.md`; the live worklist is `status.md` (this plan is its Active-work item).
> The field evidence is in `field-fixes-plan.md` → *The live pass*.

---

## The reframe (2026-07-30, at implementation)

The plan as first written treated a virtual row as a **fenced exception** to field-fix A's
filter: the filter is right in general, and Incinerate is smuggled back past it under four
guards. The framing that replaced it is simpler and truer:

**Field-fix A conflated two fences that make different kinds of claim.**

- **`unlearned`** (`isKnown == false`) — the character does not have this spell. A
  **correctness** fence. It is what actually killed the 216-dropped-Soul-Fire-cues bug, and
  it survives here as the `known` fence (read from the spellbook, since an untracked ability
  has no CDM struct to carry `isKnown`).
- **`no-icon`** (no item frame) — the character *has* it and presses it constantly; we simply
  could not draw it. That is a **display** limit that was being enforced at the **decision**
  layer. Correct only while the product was strictly a CDM overlay; wrong the moment the HUD
  can draw its own icons.

So this is not an exception to field-fix A. It is separating the half of field-fix A that was
load-bearing from the half that was an artefact of the old product definition.

**The product statement moves with it:** from *a CDM overlay* to **a rotation helper that
displays on the CDM when it can, and on its own icons when it cannot**. `design.md` still
says the former; that is a follow-up (`status.md` backlog).

### Why this is safe by construction, not by vigilance

The worry is that admitting abilities State cannot observe re-creates phantom abilities.
It cannot, and the reason is already in the pipeline:

```lua
-- Coach.lua
rec.probablyUp = rec.ready
  or (rec.onCd and c.source == "napkin" and (rec.remaining or 0) <= 0)
  or false
```

Every cooldown-bearing line in `RankWinner` gates on `usable()`, which needs `probablyUp` or
a banked charge. An ability admitted with **no observation** reads `unknown` — neither ready
nor on-cooldown — so `probablyUp` is **false** and it can never win a line.

That changes what the zero-cooldown fence *is*. It is not a prohibition on faking readiness;
it is a **description** of the only case where we can honestly rank without an observation,
because for a 0-cooldown spell `ready` is a statement about the spell's **nature** rather
than a reading of its state. Same rule, derived instead of imposed.

### Why detection beats declaration

`ns.Spec` **already is** the spec's ability library — every rotation button with its `kind`,
`cadence` and `expect`. A `virtual = true` flag would restate what that table already says
and have to be maintained per spec forever. The walk asks the table directly, so **adding a
spec adds nothing**. The cost is one genuine wrinkle, now fixed:

**Cast-id aliases.** `[348]` is Immolate's cast id (the CDM tracks the DoT aura `157736`);
`[136726]` is Grimoire: Imp Lord's talent entry-id. Both are `kind = "button"` entries that
are *aliases*, not second abilities. Immolate has no base cooldown, so without a fence `348`
would have been drawn as a **second Immolate icon** beside the real one. Both now carry
`expect = false` — the spec table's **existing** field for "never bound to a CDM icon of its
own", which was already true of them and merely unstated. (Imp Lord was previously excluded
only by *accident*, via its 120s cooldown; the test deliberately zeroes that cooldown so only
the fence can keep it out.)

---

## Why

Blizzard's Cooldown Manager does not track every ability a rotation needs. Destruction's
**Incinerate** is the sharp case: it is the spec's floor press — the thing you hit when
nothing else is available — and it has **no CDM entry at all**. Demonology has the same hole
at Shadow Bolt.

The consequence is not cosmetic, and the live pass measured it:

- **31 % of decisions produced no winner.** Below Chaos Bolt's 2-shard cost the priority list
  has no floor, so the Coach honestly returns nothing and the HUD goes blank. On a spec whose
  filler is most of the button presses, the HUD is dark for roughly a third of a pull.
- **L12 (Infernal Bolt) can never light.** The Diabolist shard-refill transform *rides the
  Incinerate frame*. No frame, no transform, no cue — a whole priority line is dead.

⚠ **This is a decision problem before it is a drawing problem**, and that distinction shapes
the whole design. `RankWinner`'s `key(base)` gates on `ctx.facts[base]`, which is built from
`state.abilities`. Incinerate is not in the CDM database, so it never enters `abilities`,
so **the Coach cannot pick it in the first place**. Drawing an icon for a cue that is never
emitted would achieve nothing. What is needed is a **virtual CDM entry** — a synthetic row in
the domain view — of which the panel is merely the visible half.

### What the live pass handed us

Incinerate `29722` is **not in `CooldownSetSpell`** for any set (fresh Tier-1 pull, 12.0.7).
But Destruction's set 884 carries **Shadow Bolt `686` at `cid 66181`, Essential, OrderIndex
0**, and the client overrides that entry's *display* to Incinerate — which is why the
Cooldown Settings panel shows an **Incinerate tooltip on a greyed icon**, and why the
pre-filter build listed `Inc` in `tracked:` (its `liveSpellID` resolved to `29722` while its
base stayed `686`). The entry reads `isKnown = false`, so Blizzard never creates a frame for
it, and adding it to the displayed list cannot help.

**We are deliberately NOT building on `cid 66181`.** It is a real cooldownID whose live
identity already resolves to Incinerate, which is tempting — but it is an override on an
entry the client considers unlearned, it is Destruction-specific, and Demonology's Shadow
Bolt hole has no analogous entry. Synthetic handles generalise; this one does not. It is
recorded here because it is the reason the tooltip looks the way it does, not as the seam.

---

## Decisions locked before starting

> ⚠ **Items 4 and 5 were re-motivated by *§ The reframe* above, and item 4's "spec-declared"
> fence became "spec-*detected*".** The fences themselves are unchanged in effect; what
> changed is why they exist — 4 is no longer "an exception to field-fix A" but "the half of
> field-fix A that was load-bearing", and 5 is no longer a prohibition but a description.
> Read the reframe first; the list below is kept for the reasoning it records.

1. **A virtual entry is a State concern, not a Coach concern.** State owns the domain view
   and already consults injected `ns.Spec*` readers. Synthesising there fixes **both**
   registered specs with no Coach edit, no spec-brain edit, and no rotation-oracle churn —
   the same reasoning that put field-fix A's filter in State.
2. **The Binder and Renderer must not change.** A virtual entry that needs a new pipeline
   stage, a new DrawList channel or a contract edit is the wrong design. It should arrive as
   *just another Layout entry plus a frame in the registry*, and every existing stage should
   handle it without knowing. **If either file needs edits, the seam is wrong — stop and
   re-think rather than widening the contract.**
3. **Additive only — the pillar-1 line.** `design.md` pillar 3 is *enhance, don't replace*,
   and the aesthetic commitment is "icons kept, untouched — we own the chrome around them".
   An artificial icon is **ours**, so the defensible boundary is that it exists **solely for
   abilities Blizzard displays nowhere**. A virtual entry must never shadow, duplicate or
   restyle an ability the CDM already shows, and the panel must be visibly ours rather than a
   forgery of a Blizzard row.
4. **Fenced hard, because this re-opens the exact hole field-fix A just closed.** A synthetic
   row is by construction an ability State cannot observe — which is what phantom abilities
   were. Four fences, all required together:
   - **spec-declared** — never inferred from "what's missing";
   - **known** — `C_SpellBook.IsSpellKnown` says the player actually has it;
   - **no cooldown** — `ns.BaseCooldown(id) == 0`, so "ready" is *structurally* true rather
     than a guess (see 5);
   - **absent** — it is genuinely not already in `abilities`.
5. **Only zero-cooldown fillers, in v1.** This is the fence that makes the readiness claim
   honest. A 0-cooldown spell has no cooldown to be unsure about, so `ready` is a statement
   about the spell's nature, not an observation we are faking. The moment a virtual entry has
   a real cooldown we would be inventing readiness for an ability with no alert channel, no
   OOC baseline and no napkin — precisely the thing this project refuses to do. It also
   happens to cover the entire actual need: Incinerate and Shadow Bolt are both 0-cooldown.
6. **Synthetic handles are negative.** `-spellID`. Real cooldownIDs are positive, so
   collision is impossible by construction rather than by luck, and the handle is reversible
   by eye when reading a decision log.

---

## Phases

Gates throughout: **luacheck clean + the full busted suite green** (279 at plan time, **353**
after Phase 2), count growing only by new specs. One release at the end of Phase 1 (it is
independently useful), another after Phase 2.

| Phase | Work | Gate |
|---|---|---|
| **1 — the seam, end to end** ✅ **SHIPPED** | State detects virtual candidates from `ns.Spec` behind the fences and synthesises a domain-view row (`virtual = true`, handle `-spellID`, `cd.source = "static"`); new `HudVirtual.lua` pools a button frame per row and emits `(layout, registry)` fragments via `HudLayout.Build`; `HudDriver` merges them. `Binder.lua` / `Renderer.lua` / `guidance-contract.json` / `Coach*.lua` / both oracles **untouched**. Fixed position. **Phase 3 came free** — see below. | ✅ `luacheck` clean, **323 tests** (279 → +18 `hudvirtual_spec`, +23 State fences, +3 Coach before/after). ✅ **Every fence mutation-checked** — all 7 walk fences plus both alias fences and both negative handles go red when dropped. ⏳ In-game: `w:-` collapses from 31 %, `B{Inc:ROT}` with **no `×`**. |
| **1b — fence on DISPLAY identity** ✅ **BUILT** (v0.32.33) | The Diabolist duplicate: Blizzard's row is Shadow Bolt `686` *displaying* Incinerate `29722`, so `abilities[29722] == nil` stayed true while Blizzard was drawing it. New `St.DisplayedIdentities` unions base ∪ `liveSpellID` ∪ `overrideSpellID` ∪ `overrideTooltipSpellID`; the walk's `absent` fence asks that set. | ✅ `luacheck` clean, **353 tests**. ✅ Mutation-checked both ways: drop the static-override union ⇒ the flicker test reddens; drop the lookup ⇒ the duplicate tests redden. ⏳ In-game: exactly one Incinerate icon on **both** hero trees. |
| **2 — placement & the visual line** ✅ **BUILT** (v0.32.33) | `V.root` grew real extents (row width, floored at 3 icons so a zero-row spec stays grabbable), drag wiring + a saved position in `ns.db.virtualPanel`, and `/cdmp panel unlock \| lock \| reset` (bare toggles). Mouse enabled **only** while unlocked; the affordance is a terminal-green edge + `CDMProbe` caption with the icons held lit. Shape copied from BucketBinds' `Console.lua` verbatim, relativeTo discarded on restore. | ✅ **+21 `hudvirtual_spec` tests** (save/restore round-trip, default fallback, `reset`, lock/unlock over mouse + chrome + alpha, the combat refusal, and the extents floor). ⏳ In-game: drag → `/reload` → it comes back where you left it. No new decision logic, so no oracle change. |
| **3 — generalise** ✅ **FREE** | Demonology's Shadow Bolt needed **zero edits** — detection reads the spec table, and Shadow Bolt was already in it. The payoff case (L12 Infernal Bolt riding the now-drawable Incinerate frame) is covered by a Coach test. | ✅ The Demonology oracle stayed green untouched; `state_domainview_spec` asserts the walk yields **exactly** Shadow Bolt for Demonology and **exactly** Incinerate for Destruction. |

### What shipped in Phase 1

| File | Change |
|---|---|
| `State.lua` | the detection walk (`St.VirtualCandidates`) + row synthesis (`St.VirtualRow`) + `pulse.virtual`; `knownCache` wiped on `SPELLS_CHANGED` |
| `HudVirtual.lua` **(new)** | pooled button per virtual row; `Build` delegates to `HudLayout.Build` so the fragment shape agrees *by construction* |
| `HudDriver.lua` | merge the fragments; `Reflect(drawList)` for the dim/lit alpha; `Clear()` on HUD off |
| `SpecDestruction.lua` · `SpecDemonology.lua` | `expect = false` on the two cast-id aliases (348, 136726) |
| `CDMProbe.toc` · `.luacheckrc` | load `HudVirtual.lua`; `C_SpellBook` in the globals std |

### What shipped in Phase 1b + 2 (v0.32.33)

| File | Change |
|---|---|
| `State.lua` | `displayedIdentities` (exposed as `St.DisplayedIdentities`); the walk's `absent` fence reads that set instead of `abilities[spellID] == nil` |
| `HudVirtual.lua` | root extents + `V.RootSize`, drag wiring, `SavePosition`/`RestorePosition`/`ResetPosition`, `V.SetUnlocked` + the green edge/caption chrome, `/cdmp panel`; buttons lay out from the root's `LEFT` (padded, so a lone icon stays centred on the anchor exactly where Phase 1 put it) |
| `Core.lua` | `virtualPanel = {}` in `DEFAULTS` — an empty table means "no saved position", which `RestorePosition` detects via the absent `point` |
| `tests/mock_ns.lua` | `SetMovable`/`RegisterForDrag`/`StartMoving`/`StopMovingOrSizing`/`SetClampedToScreen` no-ops, a **recording** `GetPoint` + `EnableMouse`, and a recording `ns.RegisterCommand` (+ `H.run`) so a spec can drive a slash verb through the real handler |

**The lesson from the duplicate, recorded because the plan half-saw it coming:** decision 7
rejected *building on* `cid 66181` because its identity is split — and then the fence it wrote
compared base identities anyway. Knowing a hazard is not the same as fencing against it.

**One real bug caught by the gates, worth recording:** `knownCache` was first declared beside
the walk that reads it — *below* the `SPELLS_CHANGED` handler that wipes it. luacheck flagged
the undefined global. The cache would never have invalidated across a respec, and `wipe(nil)`
would have thrown inside an event handler. Declaration hoisted above the event frame.

### Phase 1 in detail — the pieces

- **`Spec<Name>.lua`** — `virtual = true` on the ability's existing bucket entry. No new
  table, no new registry; it sits beside `expect = false` as another statement about how the
  ability relates to the CDM.
- **`State.lua`** — after the domain-view fold, walk the active spec's virtual declarations
  and synthesise a row for each that passes the four fences:
  - keyed by base spellID, like every other `abilities` row;
  - `display = { cooldownID = -spellID, category = "Virtual" }`;
  - `cd = { state = "ready", readable = true, source = "static" }` — a **new `source`
    value**, because laundering this as `"live"` would claim an observation we did not make.
    `architecture.md`'s `source ∈ live|napkin|none` grows a fourth member; nothing branches
    on it today except the decision log, which renders `state` only.
  - `virtual = true` on the row, so every downstream consumer can tell.
  - The knownness read is `pcall`-guarded and cached (it is respec-scoped, and its
    `SecretArguments = "AllowedWhenUntainted"` means it can refuse); a refusal means **no
    virtual entry**, which is the under-show direction.
- **`HudVirtual.lua` (new)** — the only new module. Pools one button frame per virtual row,
  sets the icon from `C_Spell.GetSpellTexture(spellID)`, and returns layout/registry
  fragments in exactly `HudLayout.Build`'s shape. Frames are created **out of combat** and
  pooled thereafter, per the project's standing frame discipline.
- **`HudDriver.lua`** — three lines: call `HudVirtual.Sync(pulse)`, merge its fragments into
  the scanned layout/registry, done. The existing keybind stitch already works, because
  `HudBinds` resolves off the base spellID and never consulted the CDM.

**What is NOT touched:** `Binder.lua`, `Renderer.lua`, `guidance-contract.json`,
`Coach.lua`, either `Coach<Spec>.lua`, and either rotation oracle. That list is the design's
own success criterion.

---

## Design — what it should look like

Deferred to Phase 2, but the constraints are already fixed by `design.md`:

- **It rides the column, it does not float.** Pillar 2 anchors our overlay to the viewer so
  it moves when the user moves the CDM and vanishes cleanly when the HUD is off. A virtual
  row should read as a continuation of the Essential column, not a second widget in a
  different place on screen.
- **Native icon art, our chrome.** The icon texture is Blizzard's own (`GetSpellTexture`),
  because pillar-1's whole argument is that the native art is the strongest non-colour
  signifier we have. What we add around it is the terminal/CRT chrome we already own, which
  is also what keeps it honest — it should be *apparent* that this row is the HUD's.
- **No swipe, no countdown, and that is fine.** A 0-cooldown filler has nothing to sweep.
  This is another reason the v1 fence lands where it does: the one thing our own icon
  genuinely cannot reproduce is exactly the thing these abilities do not need.

### Two decisions — SETTLED at approval

1. **Always visible while the HUD is on**, dimmed when uncued (`DIM = 0.40` / `LIT = 1.00`).
   A floor press that appears and disappears is worse than a constant one — the whole point
   is that the player's eye has somewhere to land when nothing else is up. The cost, accepted
   knowingly, is a permanent addition to the screen: the sharpest form of the pillar-1
   tension. Shipped in Phase 1; `HudVirtual.Reflect` reads the same DrawList the Renderer
   drew, so the two can never disagree.
2. **Free-floating with a saved position** — *not* anchored to the Essential viewer. Phase 1
   ships a fixed default (below the resource bar, so the HUD's own chrome reads as one
   group); the saved, draggable position + `/cdmp panel` is Phase 2.

---

## Risks, and what makes each safe

- **We re-create phantom abilities.** The honest reading of this feature is "put back a row
  State cannot see" — which is what we just spent a plan removing. The four fences are the
  answer, and the 0-cooldown fence is the load-bearing one: it is what makes `ready` a fact
  about the spell rather than a guess about its state. Every fence gets a mutation check.
- **The seam leaks into the Binder/Renderer.** If a virtual entry needs special handling
  downstream, the abstraction is wrong. Decision 2 makes that a stop condition, not a
  patch-and-continue.
- **It stops being additive.** Scope creep here looks like "while we own a panel, let's also
  show X" — at which point we are building a replacement UI and pillar 1 is gone. The fence
  is that a virtual entry may only exist for an ability with **no CDM entry at all**.
- **Frame churn in combat.** Creating frames mid-combat is legal but avoidable; pool them and
  build out of combat, as the Renderer already does.
- **A spec declares a virtual entry for something Blizzard later starts tracking.** The
  "absent" fence handles it silently: the entry simply stops being synthesised.

## Out of scope

- **The curated Cooldown Layout override** — the other parked answer to "the tracked set is
  not what we need". This plan is deliberately the one that needs *no* enforcement UX and
  survives any layout the player chooses (`status.md`).
- **Virtual entries for cooldown-bearing abilities.** Fence 5. Revisit only if a real need
  appears, and only with an honest readiness story.
- **`hero × mode` rotation split**, branch fallback, command consolidation — all still
  backlogged separately.

## The live pass — v0.32.32, 2026-07-30 (two runs, one per hero tree)

**The primary signal landed exactly as predicted.** Hellcaller run, 258 decision changes:

| Signal | Before (v0.32.29) | After (v0.32.32) |
|---|---|---|
| `w:-` — Coach found no winner | **59 of 191 (31 %)** | **0 of 258 (0 %)** |
| `×` — Binder dropped a cue | — | **0** |
| `Inc` in `tracked:` | absent | **present** |
| `Inc` in `B{…}` | never | **89 lines** (`Inc:ROT` winning, `Inc:RFB` runner-up) |

Incinerate won **23 times**, at `0/+0` and at `2/-2` / `3/-2` (shards in hand but a Chaos
Bolt in flight, so *projected* is below its cost) — precisely the states that used to be
`w:-`. Nothing regressed: `DR:` unchanged, no duplicate icon, and Conflagrate won 144 times
**never once at zero charges** (`~2/2` ×116, `~1/2` ×27), so field-fix C2 is still holding.

### ✅ Resolved: the override channel DOES fire for an untracked display id

The Diabolist run answered the plan's one `@verify-ingame`. An armed Demonic Art appeared on
**114 of 137 lines**, `IB` on 6. `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` fires for
`cid 66181` even though its displayed spell has no `CooldownSetSpell` row.
Written up in `knowledge/addon-dev/api-events-and-discovery.md` §2.8.

⚠ **L12 is still UNTESTED, not broken.** Infernal Bolt never won — but on all 6 armed lines
shards were 1–2 with no Backdraft, so **Conflagrate won at L4**, which sits above L12. The
line was never reached. (An early reading of this — that the Coach could not classify a
transform riding base `686` — was **wrong**: `Classify` resolves `rec.info` off the **live**
id (`Coach.lua:149`), so a transformed row gets the Infernal Bolt bucket whatever its base.)

### ❌ The bug it found: a DUPLICATE icon on Diabolist

Blizzard drew its own Incinerate icon **and** we drew ours. The `absent` fence is asking the
wrong question:

```lua
and abilities[spellID] == nil        -- "is 29722 a key in abilities?"
```

Blizzard's row is **not keyed 29722**. It is `cid 66181`, whose base is **Shadow Bolt `686`**
with its display overridden to Incinerate. On Diabolist that entry reads `isKnown = true`, so
it enters `abilities` under `686` — and `abilities[29722]` is *still* nil. Both conditions
hold at once, so we synthesise a second icon. The log shows the transition cleanly:
`686:unlearned` sits in `DR:` for 4 lines, then vanishes for the remaining 133.

**The hero-tree dependence is the part nobody predicted:** the same character reads that
entry unlearned on Hellcaller and learned on Diabolist. So the Hellcaller run — where the
virtual row is genuinely needed and produced the 31 % → 0 % win — could never have surfaced
this.

⚠ **This is decision 7 biting from the other side.** The plan rejected *building on*
`cid 66181` because its identity is split (base `686`, display `29722`), recorded the hazard
— and then wrote a fence that compares base identities. Documenting a hazard is not the same
as applying it.

**The fix** is to test **display** identity: union each `abilities` row's `spellID`,
`liveSpellID`, `overrideSpellID` and `overrideTooltipSpellID` into an "already on the board"
set, and fence on that. Unioning the *static* override fields (not just `liveSpellID`) is
load-bearing: while the Art is armed the live id becomes `433891`, so a live-only check would
let our icon flicker back in mid-combat exactly when the ability is most active.

Net behaviour after the fix — **Hellcaller:** `686` is dropped `unlearned`, never enters
`abilities`, we draw ours (the 31 % → 0 % win is preserved). **Diabolist:** Blizzard draws it,
we stand down, and the transform rides Blizzard's row where it belongs.

---

## Verification

Per phase, the gates above. The **in-game** signal for Phase 1 is as sharp as field-fix A's:

```bash
uv run python -m wowkb.cdmp decisionlog
```

- `w:-` lines should fall from **59 of 191 (31 %)** to near zero — every one of them was a
  low-shard state where Incinerate was the right answer and could not be named.
- `Inc` should appear in the session header's `tracked:` list again, and in `B{…}` as
  `Inc:ROT` **without** a `×` — cued *and* drawn, which has never happened.
- Nothing else should regress: `DR:` unchanged, no new `×` on any other ability.

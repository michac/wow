# Cooldown HUD — target-state architecture (the data → display pipeline)

> **STATUS: DESIGN, agreed 2026-07-24.** This is the architecture **W4b/W4c build
> toward** — not what the addon is today. It supersedes nothing that ships; it is
> the shape the W4 refactor (`todo/addon-engineering.md` W4, worklist
> `todo/w4-hud-audit.md`) is converging on. Where today's code differs, that is a
> *gap to close*, noted per-section under "Where the code is today".
>
> **Doc map:** this is a **standalone design doc**, NOT part of the §0–§9 set shared
> across `spec.md`/`guidance-model.md`/`notes.md`/`milestones.md`. It owns the
> *component architecture*; those own vision/guidance/findings/roadmap. `milestones.md`
> §6 (W4 entries) tracks the *build* against this design.

## Why this doc exists

The cue/board logic has been smeared across `HudScore` → `HudState.Recompute` →
`HudChrome.SetCue`, and every recent regression (Tyrant-yellow-with-no-shards, the
churn gate, Grimoire double-voice) lived in the middle layer with no test coverage
(`w4-hud-audit.md` A1). W4b started the fix (`HudBoard`, a pure cue-descriptor
engine). This doc generalizes that one slice into a whole-pipeline contract, so the
rest of the UI (sequences, resource bar, combat text, animations) rides the same
seam and becomes **test-fixturable without the game**.

## Vocabulary note ("module" is loaded)

Avoid "module" for our components: in **Ace3**, `AceAddon:NewModule()` is a formal
concept (a sub-addon with its own lifecycle; errors on duplicate names —
`knowledge/addon-dev/module-architecture.md:437`). CDMProbe uses neither Ace nor
Blizzard's `<Thing>Mixin` "module" sense — it is hand-rolled `local ADDON, ns = ...`
files. So we define our own words: **layer / stage**, and the specific names below.

### Component names (locked 2026-07-24)

The five stages and the words we use. Some are renamed from the code's `Hud*` files —
those "was" entries are **forwarding addresses to dead code**, not live modules to rename
in place (the old HUD is deleted at the Phase-5 cutover, not groomed).

| Stage / concept | Name | Was | Note |
|---|---|---|---|
| Reduced client picture | **State** | `HudState` core | spec-agnostic; secrecy first-class |
| The spec-specific brain | **Coach** | "Engine" / `HudScore`+`HudBoard` | the only consumer of State; knows Demonology |
| Rough cooldown anticipation | **Napkin** | `HudNapkin` | *deliberately* informal — NOT a haste/Lust-aware sim (see Decisions) |
| The Coach's output | **Guidance** | "ViewModel" | presentation-generic: resolved RGBA, no class tokens |
| One per-icon signal | **Cue** | (same) | the attention atom |
| Concept → geometry merge | **Binder** | (new) | Layout in, DrawList out |
| Pixels | **Renderer** | `HudChrome` draw paths | pure coords + style |

Chain: **State → Coach → Guidance → Binder → DrawList → Renderer.** Read it as a
sentence: *the Coach reads the State and gives you Guidance; Cues are what it points at.*

## The pipeline

```
 State   →   Coach   →  [Guidance]  →  Binder  →  [DrawList]  →  Renderer
(reads      (decides     logical,       merges      positioned,   pure: coords
 the API)   everything)  no geometry    geometry    ready to draw + style → pixels)
```

Four data shapes flow between five stages. Two of them — **Guidance** and
**DrawList** — are hand-authorable fixtures; that is the whole payoff (W4c test mode).

### The invariants (violate these and the design is gone)

1. **The View binds to the Guidance and nothing else. Ever.** It never reads State,
   never sees the event stream, never learns *why*. If the View needs a fact to
   decide something, that decision belongs in the Coach.
2. **The Coach is the ONLY consumer of State.** The event stream never escapes it.
3. **State is spec-agnostic.** It reports the client's own facts (CDM metadata,
   readable/secret live values, power, keybinds). It does **not** know it is
   Demonology — no rotation groups, no "builder/spender". That meaning is Coach-only.
   *(Consequence, accepted: the Coach is largely NOT generalizable across specs, and
   that is fine — it is the spec-specific brain. The second-spec seam is the Coach's
   spec table, as `SpecDemonology` is today.)*
4. **Secrecy is first-class in State.** Under Midnight 12.0, many combat reads return
   Secret Values that cannot be compared/formatted/keyed without erroring. A State
   field is therefore a value **or** a marked absence (`readable:false` + null) —
   never a raw secret. This is why the napkin (anticipation math) exists: it fills
   what we are not allowed to read live.
5. **The Guidance is presentation-generic.** Resolved colours (RGBA), generic
   display enums, real spellIDs — **no** class-specific tokens (no `colorKey:"TYRANT"`),
   **no** class vocabulary except as pass-through display strings the Coach authored.
6. **Positioning is the Binder's job, via opaque handles.** The DrawList references
   position by handle (a cooldownID, or a root token), never a live frame. The
   Renderer's `handle → frame` registry is the *single* impure line in the draw path.

---

## Stage 1 — State (the reduced client picture)

The only stage that touches the game API. Anchors on the **CDM cooldown database**:
`C_CooldownViewer.GetCooldownViewerCategorySet(category, allowUnlearned=true)`
enumerates the full trackable set (incl. unlearned/undisplayed);
`GetCooldownViewerCooldownInfo(cooldownID)` returns structural metadata per entry
(`spellID / overrideSpellID / linkedSpellIDs / hasAura / charges / isKnown /
category / flags`). That metadata is **structural, not rotational** — exactly the
right split.

```jsonc
{
  "at": 12345.6,
  "combat": true,
  "cooldowns": {
    // keyed by cooldownID — the CDM database anchor
    "42": {
      // structural metadata, from GetCooldownViewerCooldownInfo:
      "cooldownID": 42, "spellID": 105174, "overrideSpellID": null,
      "overrideTooltipSpellID": null,   // added W4 P1 — a rung of the effective-id ladder
      "liveSpellID": 105174,            // added W4 P1 — the resolved display identity (B1)
      "linkedSpellIDs": [], "category": "Essential",
      "selfAura": false,                // added W4 P1 — the aura is a self-buff
      "hasAura": false, "charges": false, "isKnown": true,
      "flags": 0,                       // added W4 P1 — Enum.CooldownSetSpellFlags bitfield

      // live facts — secrecy FIRST-CLASS (value OR null + readable flag):
      "cd":     { "state": "ready|cooling|anticipated|unknown",
                  "remaining": 4.2, "readable": true, "source": "live|napkin|none" },
      "charge": { "cur": null, "max": 0, "readable": true },
      "aura":   { "active": false, "readable": true },

      "keybind": "S-3"          // mostly-static, from HudBinds, OOC-resolved off the BASE id
    }
  },
  "power": {
    // keyed by the REAL power-type (game vocabulary); Coach decides what matters
    "soulShards": { "value": 3, "max": 5, "readable": true }
  },
  "events": [ // DELTA SINCE LAST PULSE — observed only; see "Events" below
    { "kind": "cast_succeeded", "cooldownID": 42, "spellID": 105174, "at": 12345.5 },
    { "kind": "aura_gained",    "spellID": 264173, "at": 12345.4 },
    { "kind": "became_ready",   "cooldownID": 71, "source": "napkin", "at": 12345.3 },
    { "kind": "transform",      "cooldownID": 42, "from": 105174, "to": 196416, "at": 12345.2 }
  ]
}
```

- Keys: **both spellID and cooldownID** are present (State keys on cooldownID, the CDM
  anchor, and carries spellID + overrideSpellID). They diverge on transforms — the
  live identity is `overrideSpellID or spellID`. State owns that resolution (today's
  B1 bug is three copies of it — `w4-hud-audit.md` B1).
- `cd.state:"anticipated"` + `source:"napkin"` is how the napkin enters *without*
  masquerading as an observed read; an expired estimate stays `"unknown"`, never
  `"ready"` (the napkin's honesty rule).
- **Where the code is today:** `HudState.lua` is the de-facto State layer but 1,254
  lines that also score and paint (`w4-hud-audit.md` A4). Napkin (`HudNapkin`) and
  keybind cache (`HudBinds`) are the anticipation and static inputs, consulted
  ad-hoc rather than unified. Event ingest is split across three frames
  (`Probe`/`HudNapkin`/`HudState` — A3) that this design collapses to one.
- **W4 Phase 1 landed (2026-07-24):** `State.lua` is the clean-room Stage-1
  extraction to exactly this shape — CDM-database-anchored, secrecy first-class, one
  identity resolver (`liveSpellID`) + its inverse (`BaseOfCast`), the napkin/keybinds
  consulted *through* it, one event-ingest frame, a ~10 Hz change-detecting poll. It
  **coexists** with `HudState` as parallel observation (the old frames are deleted at
  the Phase-5 cutover, not now). `/cdmp statelog` records its pulses to
  `CDMProbeDB.statelog`, asserted by `wowkb.cdmp`'s `statelog` baseline block — the
  independent corpus Phase 2's Coach is tested against.

### Events — semantics

- **Window:** the delta **since the last pulse**, not a rolling time window and not a
  durable log (the pull recorder is a separate concern, `HudLog`).
- **Consumed by the Coach, not the View.** Events are *causal inputs*:
  `cast_succeeded` advances a sequence, `transform` re-resolves identity,
  `aura_gained` (a proc) changes cue decisions. The View never sees them — anything
  they should produce visually comes back out as a steady-state descriptor or an
  **effect** (see Guidance).
- **Observed only.** Derived thresholds like "napkin getting close" are **not** events
  here — State exposes the countdown (`cd.remaining` + `source:"napkin"`) and the
  **Coach** decides when "close" crosses into a cue. "How close is close" is a
  rotation decision, not a State one.
- **`at` earns its keep** three ways: ordering within a pulse, ttl/decay of effects,
  and the pull recorder later.

### Eval gating — a State-internal, swappable policy

**The trigger policy lives entirely in State; nothing downstream cares what caused a
pulse.** So it is not committed here. Start with the simplest thing that matches
today (a modest poll, ~10 Hz); evolve to **event-driven + scheduled wakeups** with no
change to Coach/View — the natural scheduler is the napkin, which already knows the
exact time it next expects something ready ("wake me at t=X"). The format must support
**change-detection at each seam** (diff State, diff Guidance) so a no-change pulse is
a near-noop and no strings are built (the E1 hot-path concern — `w4-hud-audit.md` E1).

---

## Stage 2 — Coach → Guidance (spec-agnostic, presentation-generic)

The Coach is spec-specific (it knows Demonology). Its **output** is not: resolved
colours, generic enums, real spellIDs, pass-through strings.

```jsonc
{
  // was a leaky "mode" — now a GENERIC resource bar the Coach fully resolved:
  "resourceBar": {
    "value": 3, "max": 5, "incoming": 1,
    "display": "discrete",              // "discrete" | "percentage"
    "color": [0.55, 0.35, 0.9, 1.0]      // resolved RGBA — no class token
  },
  "chrome": { "accent": [0.55, 0.35, 0.9, 1.0] },   // any mode-driven tint, made generic

  "cues": {
    // keyed by cooldownID (real); View MAY fetch an icon from spellID if we draw our own
    "42": {
      "draw": true,
      "color": [0.2, 0.8, 0.4, 1.0],     // Coach-resolved; no "TYRANT" key reaches the View
      "fill": 0.6,                        // emphasis as a fraction
      "pulse": false,                     // SUSTAINED animation state (see effects contrast)
      "width": "narrow",                  // "narrow" | "wide"
      "note": null                        // optional PASS-THROUGH display string only
    }
  },

  "sequence": {
    "show": true, "title": "OPENER", "cursor": 1,
    "steps": [
      { "spellID": 193331, "label": "Dreadstalkers", "keybind": "4", "state": "done" },
      { "spellID": 265187, "label": "Tyrant", "keybind": "6", "state": "blocked",
        "note": "Need 5 shards" }         // "shards" appears ONLY as pass-through display text
    ]
  },

  // TRANSIENT / impulse channel — one-shot animations AND combat text (folded together).
  // Modelled as a KEYED DECLARATIVE LIST: a new `id` = start; a re-seen `id` = no-op.
  // Idempotent (re-applying the same Guidance never re-fires) and fixture-authorable.
  "effects": [
    { "id": "ready-71@12345.3",   // stable identity is the whole trick
      "kind": "flash",             // generic vocab: flash | pulse | shake | sparkle | float-text
      "target": 71,                // handle (cooldownID) | "resourceBar" | "SCREEN"
      "text": null,                // set for kind:"float-text" (this SUBSUMES the old callouts)
      "color": [0.2, 0.8, 0.4, 1.0],
      "ttl": 0.4 }                 // View ages it out; or omit and let the anim decide
  ]
}
```

Design rules baked in here:

- **`mode` → `resourceBar` + `chrome.accent`.** The Coach's builder/spender/burst
  state never reaches the View; only its *visual consequences* (a generic bar and an
  accent colour) do.
- **`colorKey:"TYRANT"` → `color:[rgba]`.** The Coach resolves the palette; the View
  is class-blind. (Theming, if ever wanted, is an Coach input, not a View table.)
- **Real spellIDs** as keys/step ids — keeps the "draw our own icons" door open.
- **Class vocabulary only as pass-through strings** (`label`, `note`) the Coach
  authored for display — never as tokens the View must interpret.
- **Effects vs `pulse` — do not blur them.** *Stateful/sustained* animation is a field
  on the steady descriptor (`pulse:true` while the cue is in that state).
  *Impulse/one-shot* animation is an `effects` entry. Blur them and you get flashes
  that never stop and pulses that fire once.
- **Effects answer "what/where" without a View leak:** the Coach (the only place that
  knows a proc *means* "sparkle Demonbolt") sets `kind`+`color`; `target` is a handle
  the Binder resolves to geometry, same as a cue. The View plays the animation at the
  resolved rect and never touches the event stream.
- **Where the code is today:** W4b's `HudBoard.Compute` is a working first slice of
  this — a pure fn emitting per-key cue descriptors that `HudChrome.DrawCue` renders
  verbatim. It covers `cues` only; `resourceBar`, `sequence`, and `effects` are still
  decided inline in `HudState`/`HudChrome` and are the remaining W4b/W4c work.

---

## Stage 3 — Binder (position decoration) → DrawList

The Binder merges the Coach's logical `cues`/`effects` with a **Layout** (geometry,
keyed the same way), producing the DrawList the Renderer draws verbatim.

```jsonc
// Layout (Binder input): geometry per handle. Live: from the CDM RefreshLayout hook.
// Test: a fixture supplies it directly — this is what unties the test from real icons.
{ "42": { "anchorTo": 42, "point": "CENTER", "relPoint": "CENTER", "dx": 0, "dy": 0, "w": 48, "h": 48 } }
```
```jsonc
// DrawList (Binder output): "anchorTo" is an opaque HANDLE or a root token.
{
  "cues": [
    { "anchorTo": 42, "point": "CENTER", "relPoint": "CENTER", "dx": 0, "dy": 0, "w": 48, "h": 48,
      "color": [0.2,0.8,0.4,1.0], "fill": 0.6, "pulse": false, "width": "narrow" }
  ],
  "panel":       { "anchorTo": "UIPARENT", "point": "TOP", "dx": 0, "dy": -200, "title": "OPENER", "steps": [/*…*/] },
  "resourceBar": { "anchorTo": "UIPARENT", "value": 3, "max": 5, "color": [0.55,0.35,0.9,1.0] },
  "effects":     [ { "anchorTo": 42, "kind": "flash", "color": [0.2,0.8,0.4,1.0], "ttl": 0.4 } ]
}
```

- `anchorTo: 42` = "the frame registered under handle 42" — the CDM icon frame in-game
  (free ride-along on Edit-Mode drags), a placeholder square in a test. `anchorTo:
  "UIPARENT"/"SCREEN"` = our own roots.
- **Geometry-source tradeoff (decide per widget, format supports both):** *handle +
  anchor-to-frame* preserves free ride-along (cues, which ride Blizzard's foreign
  frames); *absolute rects* (`{x,y,w,h}`, no registry) is the "pure draw tool" extreme,
  fine for our own widgets (panel, resource bar, callouts) that we position ourselves.
  Recommended: handle-anchor for cues, self-anchored for the rest.
- **Where the code is today:** there is no Binder — `HudChrome` reaches into the live
  CDM layout itself. Extracting it is the step that makes W4c's fixture test possible.

---

## Stage 4 — Renderer (pure: coords + style → pixels)

Owns a pool of frames/textures and a `handle → frame` **registry** — the one impure
thing in the draw path. Live mode registers `cooldownID → Blizzard item frame`; test
mode registers `"fake1" → a placeholder icon frame the test drew`. Given a DrawList it
does `frame:SetPoint(d.point, registry[d.anchorTo], d.relPoint, d.dx, d.dy)` and
applies colour/fill/animation. **No decisions.** Diffs by key so only changed frames
are touched; starts an effect animation when a new effect `id` appears, owns its clock
thereafter.

---

## The test-mode payoff (W4c) — why the seams are shaped this way

Because Guidance and DrawList are pure data with no frame refs and no secrets, a test
can:
1. Draw N placeholder "cooldown icons" and register them under fake handles.
2. Hand-author a Guidance + Layout for any state ("mid-opener, 3 shards, Tyrant SOON,
   Core proc'd, flashing HoG").
3. Drive the Binder + Renderer with them and screenshot the real pixels — no game, no
   dummy, no RNG, no CDM.

This is the same fence the pure modules (`HudScore`/`HudQueue`/`HudNapkin`/`HudBoard`)
already sit inside, extended around the whole UI.

## Open questions (ClientLab / in-game answerable — do not assume)

- **Do non-displayed CDM entries return live `cd`/`charge` VALUES**, or only structural
  metadata? `GetCooldownViewerCooldownInfo` is `MayReturnNothing=true`. If values are
  absent for untracked entries, State can still anchor on the full set but must mark
  those `readable:false`. *(A ClientLab call-and-record test.)*
  — **✅ ANSWERED (W4 P1, 2026-07-24, measured not assumed).** `State.lua` enumerates
  the *full* category set (`allowUnlearned=true`) and does a **separate** `C_Spell` live
  read per entry (`ns.ReadCooldown` — the info struct carries no live fields). A real
  `/cdmp statelog` capture (v0.29.2, Demonology, 64 enumerated entries) settles it:
  **YES — the `C_Spell.GetSpellCooldown` read returns live `cd` VALUES for undisplayed
  AND unlearned entries out of combat.** Out of combat all 64 entries read
  `cd.readable=true` (44 `isKnown=true` + **20 `isKnown=false`/unlearned**, every one
  with a real `ready`/`remaining` value). So State can trust the live read across the
  whole database OOC, not just the tracked/displayed subset — the read is NOT gated on
  CDM display or on the spell being learned. *(Charge values were not exercised — this
  character's Demo set has no charged tracked ability, so the `charge` half stays
  `@verify-ingame` until a charged spec is captured.)*
- **Do those reads go secret in combat the same way tracked ones do?** The seam is
  proven for the tracked set (`probe-baseline.json cooldown-read-combat-seam`); the
  full-database read is not.
  — **✅ ANSWERED (W4 P1, 2026-07-24).** Same v0.29.2 capture, combat pulses: **all 64
  entries read `cd.readable=false`** (known and unlearned alike). The combat secret-gate
  applies **uniformly to the whole database read**, exactly as it does to the tracked
  set — there is no undisplayed-entry loophole that stays readable in combat. State's
  secrecy-first-class handling (value OR `readable:false`, fall to the napkin) is
  therefore the correct and only design for the full-set anchor.

- **How do we read PROC / BUFF PRESENCE (e.g. Demonic Core) in combat?**
  — **✅ ANSWERED, measured & cross-validated (W4 P1, 2026-07-24, CDMProbe v0.29.5).**
  This is a load-bearing result — the Coach's proc decisions hinge on it.
  - **`C_UnitAuras` is DEAD in combat.** Combat-applied auras are Secret Values:
    `AuraUtil.ForEachAura` returns them as secret tables (6–16/pulse) and
    `GetPlayerAuraBySpellID` returns `nil`. So `State.aura` is honest OOC and
    `readable:false` in combat — it is **not** the proc source.
  - **The buff-tracking item's `IsActive()` IS readable in combat** — a plain bool
    Blizzard's trusted code derives from the (secret) aura and stores on the frame
    (`CooldownViewer.lua` `SetIsActive`/`ShouldBeActive`). For Demonic Core (cd 777)
    it tracked the proc **exactly**: `false` before, `true` across every proc window,
    clearing with the buff. **This is the canonical per-buff presence signal.**
  - **`C_SpellActivationOverlay.IsSpellOverlayed(spellID)` is also readable in combat**
    — the glow lands on the *empowered* spell (Demonbolt lit whenever Core was up),
    the actionable "press this now" signal. It matched `buff.isActive` on **all 32
    pulses**, a perfect independent cross-check.
  - **Caveat:** `item:IsShown()` equalled `isActive` here only because
    `hideWhenInactive=true` for that buff; **`IsActive()` is the robust read**
    (independent of the hide setting). Duration/stacks stay secret (unread).
  - **Design consequence:** State sources buff/proc presence from the **buff-item
    `IsActive`** (bridged via the item frame, like the napkin/keybinds are inputs) and
    carries the **`glow`** as the complementary empowered-spell signal; the C_UnitAuras
    `aura` field is OOC enrichment only. The Coach reads `buff.isActive` ("Core is up")
    and `glow` ("Demonbolt is the actionable press").
- **Anchor-to-frame ride-along vs absolute rects** under an Edit-Mode drag — does
  `RefreshLayout` fire often enough that absolute would not lag? (Decides the cue
  geometry source above.)
- **Combat-text nameplate anchoring** (`float-text` effects) — secret-propagation /
  taint exposure is Tier-2 in the KB (`w4-hud-audit.md` C4); treat as
  `@verify-ingame`-class and never measure those FontStrings.

## Decisions locked this session (2026-07-24)

Keys = **both** spellID + cooldownID (State keys on cooldownID) · State carries the
**keybind** · State carries **no spec metadata** · resource bar is **generic**
(value/max/display/color), not "shards" · cue colour is **resolved RGBA**, not a class
key · **real** spellIDs (icon door open) · class words only as **pass-through** strings
· `events` = **delta since pulse**, **Coach-only** consumer, observed-only, `at` kept ·
**effects** channel generalizes one-shot animation **and** combat text, as a **keyed
declarative list** · eval trigger is **State-internal and swappable**.

**Component names:** the five stages are **State → Coach → Guidance → Binder →
Renderer** (Coach = the spec brain, was "Engine"; Guidance = its presentation-generic
output, was "ViewModel"). The rough cooldown-anticipation input keeps the name **Napkin
by design**: a formal name ("Forecast", "Estimator") would imply a haste/Bloodlust-aware
model — i.e. reconstructing the Secret Values Blizzard deliberately blocks. Napkin stays
honestly back-of-envelope (its honesty rule already says an expired estimate is
`unknown`, never `ready`); the name is a scope fence, not a placeholder.

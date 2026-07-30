# Cooldown HUD — recipe: adding a new spec

> **What this is.** A step-by-step pattern for teaching the HUD a second (third, …) spec,
> now that the multi-spec refactor is complete (`multispec-plan.md`, all 6 phases done
> 2026-07-29). The framework is one spec-agnostic pipeline + a per-spec brain that plugs
> in; adding a spec is **additive** — a docs folder, two Lua files, a `.toc` line pair, and
> a test. **You do not touch the pipeline** (State / Coach shell / Binder / Renderer /
> DecisionLog).
>
> **Status: reference pattern, not yet a skill.** Derived from how Demonology (266) is
> wired (`SpecDemonology.lua` + `CoachDemonology.lua`) and verified against the live code
> 2026-07-29. May be converted into a skill later — keep it faithful to the code so the
> conversion is mechanical.
>
> **Doc map:** the technical contract is `architecture.md` (invariant #3 + "Settled
> decisions → Spec resolution"); the design + phasing that built the seam is
> `multispec-plan.md`; the live worklist is `status.md`. This recipe is the *how-to* those
> three imply.

---

## Source the data offline — the readability rules are already settled

The Secret-Values / cooldown-readability rules are settled **game-wide invariants** — they
are properties of the API + Secret-Values model, not of the spell, so a new spec obeys them
exactly as Demonology does. (These were discovered by the old `/cdmp probe`, retired
2026-07-29 once they were nailed down.) Do **not** re-verify them per spec:

| Settled rule (never re-check per spec) | Consequence for spec data |
|---|---|
| `C_Spell.GetSpellCooldown` reads **secret in combat**, real OOC (full DB incl. unlearned) | The napkin fills combat readiness; nothing to measure. |
| `UNIT_SPELLCAST_START` / `SUCCEEDED` spellIDs are **readable in combat** | The history/napkin inputs work; nothing to measure. |
| `item:IsActive()` is a **readable bool in combat** (the canonical proc/buff-presence signal) | If it worked for Demo it works for your spec. |
| `IsSpellOverlayed` glow **readable in combat**; `C_UnitAuras` **dead in combat** | Proc source = `buff.isActive` + glow, OOC aura = enrichment. |
| Override/transform fires via `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` + live-identity divergence | The transform channel works; you only need the *IDs*. |

The genuinely **spec-specific** data all comes from **offline sources**:

- **The tracked set (Essential / Utility / TrackedBuff / TrackedBar)** —
  `wowkb.spec_inventory --spec <spec>`, which reads it from the wago `CooldownSet` /
  `CooldownSetSpell` DB2 tables (the Cooldown Manager's own per-spec tracking config, keyed
  by `ChrSpecialization`). That is where per-spec CDM membership lives.
  - ⚠ **There is no per-spec table in Blizzard's CDM *Lua* source.** `Blizzard_CooldownViewer`
    hardcodes only the four *categories* (`cooldownCategories = { Essential, Utility,
    TrackedBuff, TrackedBar }`, `CooldownViewerSettingsDataProvider.lua:40`) and fetches the
    current spec's spells at runtime via `C_CooldownViewer.GetCooldownViewerCategorySet(category,
    allowAll)` (`:85`) — the same C-API our `State.lua` uses. So the offline door is DB2
    (`spec_inventory`); the runtime door is that API (current spec only). Don't go hunting the
    Lua source for a per-spec spell list — it isn't there.
  - **The data *shape*** each entry returns is the `CooldownViewerCooldown` struct in
    `Blizzard_APIDocumentationGenerated/CooldownViewerDocumentation.lua` (`cooldownID`,
    `spellID`, `overrideSpellID`, `overrideTooltipSpellID`, `linkedSpellIDs`, `selfAura`,
    `hasAura`, `charges`, `isKnown`, `flags`, `category`) — mirrored in `architecture.md`'s raw
    `cooldowns` shape. (Grep the source clone — see `knowledge/addon-dev/sources.md` §1.1.)
- **The rotation / APL** — `wowkb.simc <class> <spec>` (the Tier-1 default APL).
- **Named IDs, override/transform pairs, proc IDs** — simc + wago DB2 (`spec_inventory`
  surfaces the cdm-only residue and annotations).

So author from `spec_inventory` + `simc`, not from a capture. Demonology's data scars (the
Singe Magic pet-override hole, the Imp Lord entry-id-vs-cast-id bug) came from guessing IDs
*before* those tools existed — the tools are the fix.

**One in-game confirmation is still worth it (a check, not a gate):** the *default* tracked
set from DB2 can differ from what actually loads for a build — the Destruction draft's open
worry is exactly this ("Incinerate appears untracked"). A single **`/cdmp hud layout`** on a
real character of the spec lists the live tracked icons + resolved keybinds, **confirming the
predicted set** and catching a build-surprise. That is a one-time sanity check, not a
prerequisite. If a spec ever *violates* an established contract (something that worked for
Demo doesn't for it), that is a genuine surprise worth a new testing layer **at that point** —
don't pre-build one.

---

## Mental model — generic vs per-spec

The pipeline reads a **small, fixed surface** off the active spec object and nothing else.
Everything a spec provides falls into three tiers:

### Tier 1 — the surface the generic pipeline actually reads (REQUIRED)

| Symbol | Read by | Contract |
|---|---|---|
| `spec.SpecInfo(spellID) → info, known` | Coach shell (`Classify`), `DecisionLog` | Never errors, never keys on a secret; returns a neutral fallback + `false` for unknown/secret IDs. |
| `spec.SpecIDs` | your brain, `Probe` (diagnostics) | Named-ID table (`{ TYRANT = 265187, … }`). |
| `spec.SpecPowerDelta(spellID) → { power, delta }` | `State` (the in-flight `incoming` projection) | Signed net power delta of an in-flight cast + which named power it moves; `{ power = nil, delta = 0 }` for a no-op. |
| `spec.powers` (ARRAY) | `State`, Coach shell, `DecisionLog`, your brain | `{ { name, display, incoming, token } }` — one entry per rendered power. Read off `ns.ActiveSpec.powers` (an object read, **not** a rebound global). |
| `spec.log` (table) | `DecisionLog` | `{ cdOrder, procOrder, procBuffs, … }` — the decision-log vocabulary (below). Read off `ns.ActiveSpec.log`. |
| **`spec.Spec` bucket fields** the shell reads: `emphasis`, `kind`, `cadence`, `label`, `abbr`, `transform` | Coach shell `Emit`/`Classify`, `DecisionLog` | Every other bucket field is **your brain's private convention**. |
| `spec.SpecBindAlias` | `HudBinds` | **Optional** — only if a cast/tracked ID differs from the action-bar ID (Imp Lord's case). |

### Tier 2 — the brain (REQUIRED, attached by `Coach<Name>.lua`)

Three methods hung on the same spec object, plus tunables as `self.*`:

- `spec:Context(state, env) → ctx` — fold the pulse into whole-board facts.
- `spec:RankWinner(ctx, excluded) → winnerKey, level, note` — the flat priority list.
- `spec:Escalate(winnerKey, level, ctx) → level` — `ROTATION → LATE` from *readable*
  overdue-ness only.

### Tier 3 — carried but dormant (SKIP unless a feature revives it)

`ns.SpecFields` (in `SpecRegistry.lua`) rebinds a longer list of globals for back-compat,
but several have **no live consumer in the v1 pipeline**: `SpecGroups`, `SpecColor`,
`SpecPole`, `SpecGhost`, `SpecNoCue`, `SpecProcGlow`, `SpecStacks`, `SpecOpener`,
`SpecBurst` (the last five are old-engine render/sequence data; v1 colours cues by
`emphasis`, not group hue, and has no sequence panel). **A new spec can omit them.** Don't
copy Demonology's `SpecGroups`/`SpecOpener`/`SpecBurst` wholesale thinking the HUD needs
them — it doesn't today. (Some *bucket* fields like `spends`/`generates` look dormant to
the pipeline but are read by the Demo *brain* — those are Tier-2 private, keep whatever
your brain reads.)

---

## The recipe

### Step 0 — source the data
Have `wowkb.spec_inventory --spec <spec>` (the tracked set + IDs) and `wowkb.simc <class>
<spec>` (the APL) output for the target spec in hand — see the offline-sourcing section above.

### Step 1 — author the spec docs (`specs/<spec>/`)
Clone the four-file set every spec carries (see `demonology/` and the `destruction/`
draft):
- `rotation.md` — the flat priority list (the APL your `RankWinner` implements), distilled
  from the Tier-1 simc APL (`wowkb.simc <class> <spec>`).
- `notes.md` — ability roster, procs, resource mechanics, blind spots.
- `input-contract.md` — the evaluator's inputs.
- `observability-map.md` — what the game exposes vs. hides for this spec.

Mark them **DRAFT** with a status banner until the live capture confirms them (the
Destruction folder is the template for honest draft banners).

### Step 2 — the data file `Spec<Name>.lua`
Clone `SpecDemonology.lua`'s shape. Fill:
- `local spec = {}`.
- `spec.SpecIDs` — named IDs, **from `spec_inventory` + simc** (real cast/tracked IDs, real
  override/transform IDs — not maxroll guesses).
- `spec.powers` — the ordered power array. **`token`** is the game `Enum.PowerType` name
  (e.g. `"SOUL_SHARDS"`, `"BURNING_EMBERS"`); **`display`** is a `resourceDisplay` enum
  member from `guidance-contract.json` (`discrete` | `percentage` | `continuous`). List
  two entries for a dual-resource spec (energy+combo, runes+runic power).
- `spec.log` — the decision-log vocab (see Step 6).
- `spec.Spec` — the per-ability bucket table. Carry the six shell-read fields (`emphasis`,
  `kind`, `cadence`, `label`, `abbr`, `transform`) plus whatever your brain reads.
- `spec.SpecInfo` / `spec.SpecPowerDelta` — clone Demo's helpers; they're the two
  functions the pipeline calls. Keep `SpecInfo`'s secret-guard (`ns.IsSecret`) and neutral
  fallback verbatim — that guard is load-bearing (a Secret Value used as a table key
  taints).
- `spec.SpecBindAlias` — only if needed.
- **Self-register at the bottom:** `ns.RegisterSpec(<specID> --[[ <SpecName> ]], spec)`.
  **Registration is static; activation is the resolver's job** — do **not** call
  `SetActiveSpec`.

### Step 3 — the brain file `Coach<Name>.lua`
Clone `CoachDemonology.lua`'s shape:
```lua
local ADDON, ns = ...
local spec = ns.Specs[<specID>]   -- the object registered by Spec<Name>.lua
spec.<TUNABLE> = …                -- seconds/resource tunables as fields on the object
function spec:Context(state, env) … return ctx end
function spec:RankWinner(ctx, excluded) … return winnerKey, level, note end
function spec:Escalate(winnerKey, level, ctx) … return level end
```
Rules the Demo brain follows and yours must too:
- **Decide in BASE spellIDs** (the domain view keys `state.abilities`/`buffs`/`power` by
  base spellID). cooldownID is transport the Binder owns — it never appears in your brain.
- **Build `ctx.powers`** from `self.powers × state.power[name]` (copy Demo's loop) so the
  shell's `ResourceBars` can emit `resourceBars[]`.
- **`RankWinner` is a flat cascade**: top-to-bottom, first usable line wins; honour
  `excluded` at every line that names it (so the shell can recompute the honest runner-up).
- **`Escalate` only from readable state** — never escalate on a secret-gated quantity.
- Resolve live costs through `env.shardCostFn` (the injected reader), with a fallback
  constant on the object — never hardcode a talent-dependent cost.

Load-order safety: the `ns.Coach.*` references inside your methods are runtime-only, so the
brain file may load before `Coach.lua`.

### Step 4 — wire the `.toc`
Add the two files to `CDMProbe/CDMProbe.toc` **after `SpecRegistry.lua`**, data before
brain, both before `Coach.lua` (matching the Demo ordering):
```
SpecRegistry.lua
SpecDemonology.lua
CoachDemonology.lua
Spec<Name>.lua          ← new
Coach<Name>.lua         ← new
…
Coach.lua
```

### Step 5 — resources: mind the two Renderer generalization points
The Renderer is ~95% agnostic, with two **known** edges (`status.md` audit / multispec-plan
§4). Hitting either is a **Renderer code change** (→ release), not just spec data:
- **Power colour** — the Renderer still hardcodes the `SOUL_SHARDS` violet. A new `token`
  should resolve generically via Blizzard's `PowerBarColor[token]` (the sanctioned
  power-token exception); wiring that lookup is the generalization point, deferred until a
  spec needs it.
- **`continuous` fill** — the discrete (pips) pixel path is built; `continuous` is a
  contract-only **stub** (a continuous bar currently draws nothing). A spec whose resource
  is a continuous fill (energy/mana/fury) forces building that path.

If your spec is discrete pips on a token already coloured, you touch no Renderer code.

### Step 6 — decision-log vocabulary (`spec.log`)
`DecisionLog.lua` holds no spec constants. Provide:
- `cdOrder` — the `S{CD:…}` readiness render order, by `abbr`.
- `procOrder` — the `S{PR:…}` proc/buff render order, by code.
- `procBuffs` — `buff spellID → PR code` (the domain view's `buffs` is spellID-keyed).
- Optional spec-specific bits Demo carries (`artArmed`, `coreGlowID`) if your brain needs
  them.
Per-ability short codes ride the `abbr` field on each `spec.Spec` entry (one edit site per
ability), **not** in `spec.log`.

### Step 7 — tests (the regression gate)
- **Branch oracle:** clone `tests/spec/coach_apl_spec.lua` → `coach_<spec>_apl_spec.lua`:
  minimal hand-built `State` pulses that assert winner + `ROTATION_FALLBACK` + `SOON` per
  branch of your flat list, authored from your `rotation.md`. This is the independent
  oracle — write it from the APL, not from your own `RankWinner`.
- **Harness:** `tests/mock_ns.lua` loads `Util → SpecRegistry → SpecDemonology →
  CoachDemonology` and activates via the real resolver. Add `Spec<Name>.lua` +
  `Coach<Name>.lua` to that load list, and register the specID in `H.specByIndex`
  (Affliction 265 / Destruction 267 are already stubbed there for the passive/swap paths).
  Drive your spec by setting `H.setSpecIndex(<idx>)` before `ns.ResolveActiveSpec()`.
- The existing specs must **stay green** — the Demo brain and pipeline are untouched, so
  any red is a wiring bug in your new files.

### Step 8 — confirm the tracked set in-game (one check, optional)
On a real character of the spec, `/cdmp hud layout` lists the live tracked icons + resolved
keybinds — confirm it matches the DB2-predicted set from Step 0 (catches the "default set ≠
what loads for this build" surprise, e.g. Destruction's suspected untracked Incinerate).
There is no assertion baseline to maintain (the probe + `probe-baseline.json` were retired);
this is a one-time eyeball, and `wowkb.cdmp decisionlog` is the trace to grep if a cue
misbehaves.

### Step 9 — gates
From `addon/`:
```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck CDMProbe/ && busted CDMProbe/tests/spec
```
Clean luacheck + all specs green (the count grows by your new oracle).

### Step 10 — release + in-game smoke
New Lua ships, so this **does** need a release (unlike the docs-only Phase 6):
`wowkb.addon release cdmp --patch`, then `/reload` and smoke on a real character:
- **Target spec:** HUD binds and draws; `/cdmp hud status` → `spec: <Name> (profile
  active)`; `/cdmp hud layout` lists the tracked icons with resolved keybinds.
- **Swap to it / away from it:** respec toggles the HUD between active and passive
  (overlay clears + "no profile" line for an unregistered spec) with no stale napkin cue
  carried across (the resolver's `HudNapkin.Reset`).
- **Rotation eyeball:** the winner/runner-up/SOON cues match your `rotation.md` at the
  dummy.

---

## What you must NOT do

- **Don't edit the pipeline** — `State.lua`, `Coach.lua` (the shell), `Binder.lua`,
  `Renderer.lua`, `DecisionLog.lua`, `SpecRegistry.lua` are spec-agnostic. The only
  sanctioned pipeline edits are the two Renderer generalization points in Step 5, and only
  when your spec actually needs them.
- **Don't call `SetActiveSpec`** in a spec file — registration is static, activation is
  `ns.ResolveActiveSpec`'s job (login + `PLAYER_SPECIALIZATION_CHANGED`).
- **Don't guess IDs or the tracked set** — source them from `spec_inventory` + simc (Step 0);
  guessing is how Demo accrued its override/transform bugs.
- **Don't copy Demo's dormant Tier-3 tables** (`SpecGroups`/`SpecOpener`/`SpecBurst`/…)
  expecting them to do something — they have no live consumer in v1.
- **Don't add a rebindable global** to `ns.SpecFields` unless a live pipeline module needs
  to read it through the legacy `ns.Spec*` name; prefer an object read off
  `ns.ActiveSpec.<field>` (the pattern `powers` and `log` use).

## If this becomes a skill

The mechanical spine (Steps 1–4, 6–9) is skill-shaped. The judgement that can't be
automated: the APL distillation into `rotation.md` + the branch oracle (Steps 1, 7), and
deciding whether a spec's resource forces the Renderer edges (Step 5). A skill should
scaffold the clone + wiring + test stub from `spec_inventory` + `simc` output, then hand
those judgement calls back to a human.

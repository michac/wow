# Cooldown HUD — multi-spec plan (the second-spec seam, made real)

> **STATUS: COMPLETE — all 6 phases done (2026-07-29).** The multi-spec refactor is
> finished: the pipeline is one spec-agnostic framework + a per-spec brain that plugs in,
> shipped as v0.32.22, with docs now matching the code (Phase 6). ⏳ One follow-up owed:
> the in-game Demo smoke on v0.32.22 (deferred — no game access at flip time; see the
> Phase-6 row). This is the agreed plan for turning the pipeline from "Demonology
> hardcoded" into "one spec-agnostic pipeline + a per-spec brain that plugs in." Phase 1 (the registry seam) shipped: `SpecRegistry.lua`
> holds `ns.Specs` / `ns.RegisterSpec` / `ns.SetActiveSpec`, `SpecDemonology.lua`
> self-registers spec 266 and statically activates it, and the resolver derives the legacy
> `ns.Spec*` globals from the active spec. Phase 2 (the Coach shell/impl split) shipped:
> `Coach.lua` is now a generic shell (Classify / Emit / ResourceBars / Sequence + a
> delegating `Compute` + `EmptyGuidance`) and the Demo brain (`Context` / `RankWinner` /
> `Escalate` + tunables) lives in `CoachDemonology.lua`, attached to the active spec object.
> Phase 3 (the resource seam) shipped: a spec declares `spec.powers` (an ARRAY of named
> powers), State projects `incoming` **per power** via a renamed `SpecPowerDelta → {power,
> delta}`, the Coach emits `resourceBars[]`, and the Binder/Renderer bind + draw N stacked
> meters — proved dual-resource-capable by `resource_multipower_spec` while Demo renders the
> identical single shard meter. Phase 4 (the decision-log seam) shipped: `Hud2Log` →
> `DecisionLog` (module, `CDMProbeDB.decisionlog`, `wowkb.cdmp decisionlog` + a `hud2log`
> alias and a one-shot login migration), the log's short-codes parameterized via per-ability
> `abbr` + a `spec.log` table, and the vestigial `resources.shards` alias dropped — Demo log
> lines stay byte-identical, the proof the parameterization preserved behaviour.
> Phase 5 (live spec detection) shipped: `ns.ResolveActiveSpec` in `SpecRegistry.lua` reads
> `GetSpecialization`/`GetSpecializationInfo` on login (folded into the `ns.OnLogin` chain)
> and on `PLAYER_SPECIALIZATION_CHANGED` (its own event frame), activates the matching
> registered spec or goes passive (ActiveSpec = nil + a `/cdmp hud status` "no profile" line
> + a one-shot chat notice) when none is registered; the static `SetActiveSpec(266)` in
> `SpecDemonology.lua` is gone. On an actual change it clears the napkin (new public
> `HudNapkin.Reset`) — HudBinds already self-invalidates on the same event. **Deviation from
> the plan:** no Coach rebuild is needed — the Coach instance is generic and reads
> `ns.ActiveSpec` live each tick, so `Coach:Compute` already returns `EmptyGuidance` when
> passive. Only Demonology (266) is registered, so every other spec resolves passive
> (intended). `spec_detect_spec` covers known/unsupported/swap/no-spec; 141 tests green.
> The live worklist is `status.md`; this is the design + phasing for one
> backlog item ("Roll the domain view to other specs"). `architecture.md` is the
> technical contract this plan makes good on — its invariant #3 now describes this
> realized seam in present tense (registry + resolver + per-spec brain).

## Decisions (locked with the user, 2026-07-29)

- **Scope: refactor-to-seam only.** Build the multi-spec *framework*; keep **Demonology
  as the sole registered/live spec**, verified against no regression. A real second spec
  (Destruction) is a later, additive task — it is blocked on a live probe capture anyway
  (`status.md`), so it is deliberately out of scope here.
- **Coach model: per-spec Lua brain (pragmatic), not a declarative APL engine.** Each
  spec ships its own `Context` + `RankWinner` + `Escalate` + power declaration; the
  pipeline *shell* keeps `Classify` + `transient` + `Emit`-assembly + change-dedup
  generic. This matches `architecture.md` invariant #3 ("the Coach is largely NOT
  generalizable across specs, and that is fine").
- **Resources: an ARRAY of named powers per spec.** Not a single "primary power" — a
  spec declares `powers = { … }` so a dual-resource spec (energy + combo points, runes +
  runic power, energy + chi) is expressible. Demo declares just `SoulShards`.

## Where the spec-coupling actually lives (audit, 2026-07-29)

| Stage | Coupling today | Verdict |
|---|---|---|
| **State** (`State.lua`) | **Fully agnostic (Phase 3 + Phase 4).** Power keyed by real `Enum.PowerType` name; the in-flight `incoming` projection walks `ns.ActiveSpec.powers` and sums per-power via `ns.SpecPowerDelta(base) → {power, delta}` (`projectIncoming`). The Demo-only `resources.shards` alias was dropped in Phase 4 (its sole consumer `DecisionLog` now reads `pulse.power`). | ✅ |
| **Coach** (`Coach.lua`) | **Shell/impl split done (Phase 2); resource array done (Phase 3).** `Coach.lua` is the generic shell (Classify / Emit / **ResourceBars** / Sequence / `Compute` delegation / `EmptyGuidance`), now emitting `resourceBars[]` off `ctx.powers`; the Demo brain lives in `CoachDemonology.lua` on the active spec (it fills `ctx.powers` from `spec.powers`). `SHARD_CAP`/`POWER_TOKEN` are pure fallbacks now. | ✅ |
| **DecisionLog** (`DecisionLog.lua`) | **Parameterized + renamed (Phase 4).** Was `Hud2Log.lua` with hardcoded Demo tables (`SHORT`/`ART`/`DEMONBOLT`/`CD_ORDER`/`PR_ORDER`/`PR_SHORT`) reading `pulse.resources.shards`. Now reads short-codes off per-ability `abbr` + the non-per-ability vocab off `ns.ActiveSpec.log`, and the power bar off `pulse.power`. `EMPH` + the `S{}/G{}/B{}` format stay generic. | ✅ |
| **Binder** (`Binder.lua`) | spellID→cooldownID via live Layout, cfg-injected seams. Binds `resourceBars[]` → N stacked meters (Phase 3). | already agnostic ✅ |
| **Renderer** (`Renderer.lua`) | v1 colours cues by `emphasis` token (agnostic). Draws **N stacked** pip rows from `drawList.resourceBars` (per-bar pool; Phase 3). Remaining: one hardcoded `SOUL_SHARDS` powerColor — the token lookup is the generalization point (a 2nd token/`continuous` fill lands when a spec needs it). | ~95% agnostic |
| **Spec data** (`SpecDemonology.lua`) | **Registered, not activated (Phase 1 + Phase 5).** `RegisterSpec(266, spec)` into `ns.Specs`; the legacy `ns.Spec*` globals derive from whichever spec the resolver activates. The static `SetActiveSpec(266)` is gone (Phase 5). | ✅ |
| **Spec detection** | **Live (Phase 5).** `ns.ResolveActiveSpec` reads `GetSpecialization`/`GetSpecializationInfo` on login (`ns.OnLogin` chain) + `PLAYER_SPECIALIZATION_CHANGED` (own event frame), activates the registered spec or goes passive; clears the napkin (`HudNapkin.Reset`) on change (HudBinds self-invalidates). | ✅ |

Honest picture: State / Binder / Renderer are nearly there; the **Coach** and the
**spec-data namespace** are where the framework is built, and **spec detection** is new.

## The core abstraction — registry + active-spec dispatch

Every `SpecDemonology.lua`-style file **self-registers** instead of setting globals:

```lua
ns.Specs = {}                          -- registry, keyed by numeric specID
ns.RegisterSpec(266 --[[Demonology]], {
  name    = "Demonology",
  data    = { ids=…, info=…, groups=…, bindAlias=… },   -- was ns.SpecIDs + the bucket table
  powers  = { { name="SoulShards", display="discrete", incoming=true } },  -- ARRAY
  log     = { … } or derived from an `abbr` field on each ability bucket,
  Context   = function(self, state) … end,           -- the Demo-specific facts
  RankWinner= function(self, ctx, excluded) … end,   -- the flat-priority cascade
  Escalate  = function(self, winnerKey, level, ctx) … end,
})
```

An **active-spec resolver** (new, tiny) reads `GetSpecializationInfo(GetSpecialization())`
on login / `PLAYER_SPECIALIZATION_CHANGED`, sets `ns.ActiveSpec = ns.Specs[specID]`, and
**re-binds the legacy globals** (`ns.SpecIDs = active.data.ids`, `ns.SpecInfo` dispatches
through `ns.ActiveSpec`, …). That re-bind is the minimal-churn trick: State / Util /
HudBinds / Probe — every existing `ns.Spec*` call site — keep working untouched; only the
resolver knows a swap happened. **Unsupported spec** → `ns.ActiveSpec = nil` → HUD stays
passive with a status line (recommended default; a generic passthrough-skin is a later
option).

## Seam-by-seam work

1. **State — finish agnostic (small).** Drop the Demo-only `resources.shards` alias.
   Generalize the `incoming` projection from hardwired `SoulShards` to *walk `spec.powers`*
   and apply a renamed `SpecPowerDelta(base) → {power, delta}` (today's `SpecShardDelta`).
   A combo-point builder then projects onto `ComboPoints`, a shard builder onto
   `SoulShards`, through one loop.

2. **Coach — the real work (shell/impl split).** `Coach.lua` becomes the **generic shell**:
   `New` · `Classify` (raw candidate facts: ready/onCd/probablyUp/anticipated/glow/
   `transformed=(live≠base)`) · `transientFor` · `Emit` assembly (winner + `ROTATION_FALLBACK`
   + `SOON`) · a `ResourceBar` that walks `spec.powers` · `Compute` as pure orchestration:

   ```
   ctx = spec:Context(state); w,lv,note = spec:RankWinner(ctx)
   lv = spec:Escalate(w,lv,ctx); fb = spec:RankWinner(ctx, w)
   return shell:Emit(state, ctx, w, lv, note, fb)
   ```

   Everything Demo — `Context`, `RankWinner`, `Escalate`, the tunables (`TCT_LEAD`,
   `LATE_LEAD`, `SHARD_CAP`), `hogCost`, the `SOUL_SHARDS` power token — **moves into the
   Demo spec object**. Behaviour-preserving: `coach_apl_spec` (the Tier-1 branch oracle) is
   the regression gate and stays green through the move.

3. **Decision log — rename + parameterize the DSL. ✅ (Phase 4).** `Hud2Log.lua` →
   **`DecisionLog.lua`** (`ns.DecisionLog`, `CDMProbeDB.decisionlog` with a one-shot login
   migration folding old `hud2log`, and a `wowkb.cdmp decisionlog` subcommand keeping
   `hud2log` as an alias + a read-fallback for un-migrated captures). The
   `S{CD|PR|PW|CS} G{} B{}` **format stays generic**; the per-ability short-codes ride an
   `abbr` field on each ability's spec bucket (one edit site per ability), and the
   non-per-ability vocabulary (`cdOrder`/`procOrder`/`procBuffs`/`artArmed`/`coreGlowID`)
   lives in `spec.log`, read off `ns.ActiveSpec.log`. `EMPH` (emphasis→token) stays generic.

4. **Renderer — nearly done.** Replace the single hardcoded `SOUL_SHARDS` powerColor with
   generic resolution from Blizzard's `PowerBarColor[token]` (the sanctioned power-token
   exception), keeping the tuned violet as an override. Draw **N stacked meters** from the
   Guidance `resourceBars[]` array.

5. **Contract (`guidance-contract.json`).** `resourceBar` (singular) → `resourceBars[]`;
   add `segmented` and `continuous` to the `resourceDisplay` enum (the Destruction draft
   already flagged segmented). Our own contract → no back-compat cost.

## Sequencing — each phase `busted`-gated, Demo-behaviour-preserving

The existing specs (`coach_apl_spec`, `coach_classify_spec`, `binder_spec`,
`renderer_spec`, `hudlayout_spec`, `decisionlog_spec`, `hudnapkin_spec`, `specdelta_spec`)
are the regression gate — they must stay green throughout.

| Phase | Work | Gate |
|---|---|---|
| 1 ✅ | Registry + `RegisterSpec` + `ActiveSpec` + reader shims; Demo self-registers, ActiveSpec set statically | **done 2026-07-29** — `SpecRegistry.lua` + Demo self-register/activate; `mock_ns` loads it; new `spec_registry_spec`; 8 existing specs green unchanged |
| 2 ✅ | Coach shell/impl split (pure move of Context/RankWinner/Escalate/tunables → Demo spec) | **done 2026-07-29** — new `CoachDemonology.lua` attaches the brain to spec 266; `Coach.lua` is the shell (delegating `Compute` + `EmptyGuidance`); `coach_apl_spec` + `coach_classify_spec` green **unchanged** (all 128 tests) |
| 3 ✅ | Resource array: `spec.powers`, per-power projection (`SpecPowerDelta → {power,delta}`), `resourceBars[]`, N stacked meters, contract edit (`resourceBars[]` + `continuous` enum) | **done 2026-07-29** — `resource_multipower_spec` proves a synthetic 2-power spec; `specdelta_spec`/`renderer_spec`/`binder_spec` reshaped, `coach_apl_spec`/`coach_classify_spec` green **unchanged**; 137 tests green. **Deviation:** `resources.shards` removal deferred to Phase 4 (its only consumer is `Hud2Log`, reworked there — touching it twice is the wrong boundary). Renderer keeps its `SOUL_SHARDS` powerColor + only the discrete pixel path (continuous is a contract-only stub). |
| 4 ✅ | `Hud2Log`→`DecisionLog` rename + `spec.log`/`abbr` parameterization + DB migration + Python subcommand + **drop the `resources.shards` alias** (folded in from Phase 3) | **done 2026-07-29** — `git mv`'d module + `decisionlog_spec` green against per-spec `abbr`/`spec.log` (Demo lines byte-identical); one-shot login migration + `hud2log` Python alias/read-fallback; `resources.shards` dropped from State; luacheck clean, 137 tests green |
| 5 ✅ | Spec-detection resolver (login/spec-change), rebind + napkin/keybind cache clear, unsupported-spec status + notice | **done 2026-07-29** — `ns.ResolveActiveSpec` in `SpecRegistry.lua` (OnLogin chain + `PLAYER_SPECIALIZATION_CHANGED` frame); static `SetActiveSpec(266)` dropped; public `HudNapkin.Reset`; `/cdmp hud status` spec line + one-shot unsupported-spec notice; `spec_detect_spec` (+4 → 141 green). **Deviation:** no Coach rebuild (the generic Coach reads `ns.ActiveSpec` live); HudBinds already self-invalidates. |
| 6 ✅ | Doc/contract consolidation: `architecture.md` (seam real, not aspirational; dead `HudState`/`HudScore`/`HudBoard` refs trimmed, `HudNapkin` mislabel fixed, `resourceBar`→`resourceBars[]` prose), `notes.md` (HudTint deleted), addon `CLAUDE.md` (file map + test list synced). Contract needed no edit (already `resourceBars[]`). No runtime Lua change ⇒ **no release** | **done 2026-07-29** — docs match code; luacheck clean + 141 tests green as a safety net. ⏳ **In-game Demo smoke on the shipped v0.32.22 still owed** (no game access at flip time) — see below |

## Flags / decide-later (not blockers)

- **Unsupported-spec behaviour** — ✅ Phase 5: *HUD passive (overlay clears via
  `EmptyGuidance`) + a `/cdmp hud status` "no profile for <spec>" line + a one-shot chat
  notice, latched per specID*. The generic-passthrough-skin alternative stays deferred.
- **Log-rename ripple** — ✅ resolved in Phase 4: one-shot login DB-key migration folds
  `hud2log` → `decisionlog`; the `wowkb.cdmp decisionlog` subcommand keeps `hud2log` as an
  alias (and reads the old key as a fallback) so scripts/muscle-memory survive.
- **Spec-change in combat** — ✅ Phase 5, **not deferred**: `PLAYER_SPECIALIZATION_CHANGED`
  mid-fight is fine because the rebind is pure Lua (taint-free); the resolver clears the
  napkin (`HudNapkin.Reset`) and HudBinds self-invalidates on the same event.
- **`architecture.md` cleanup** — a couple of references point at the deleted `HudBoard`;
  fix while making the seam real (Phase 6).

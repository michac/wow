# Cooldown HUD — milestones & status

> Roadmap, milestone log, and the "confirm while logged in" queue.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> §0.5 Guidance model → `guidance-model.md` · §1–§2, §4–§5, §9 → `notes.md` ·
> §6 Milestones + §7 Open questions → **this doc** · superseded work →
> `notes-archive.md`.

## Status

**Current: M3a shipped (2026-07-20, CDMProbe v0.6.0) — the first product code.**
After four decision/prototype milestones, `/cdmp hud` exists: it binds per item by
`GetCooldownID()` to the **live** CDM layout and draws terminal chrome around
**native, untouched** Blizzard icons. Covers §0.5.8.3 row **#4** (group colour map
+ generator/consumer batch tint) plus keybinds and both deferred M1 perf cleanups.
`/cdmp crt` is **retired and `CRT.lua` deleted**; its leaf-method icon-tint
machinery survives **dormant and unwired in `HudTint.lua`** (`notes.md` §9). New
modules: `SpecDemonology.lua` (the one per-spec data table — the seam M7's second
spec plugs into), `HudCore` / `HudChrome` / `HudBinds` / `HudTint`.
⏳ **The in-game test pass is still outstanding** (see §6 M3a) — most importantly
whether dropping the 2 s ticker holds. `notes.md` §5 gets the binding-by-`cooldownID`
registry write-up **once that's confirmed**, not before. Next after it: **M3b —
readiness + procs.**

**Prior: M2.5 done** (2026-07-19, docs-only — no addon code) — the **committed v1
indicator set** is written as **`guidance-model.md` §0.5.8**: the cut principle
(Own + P0/P1 → Core), the three cross-cutting dimensions (pre-pull affordance,
anticipation layer, escalating burst telegraph + short-CD napkin pings for Tyrant /
Dreadstalkers / Implosion), the **18-row committed indicator table** (Core / Stretch
/ Defer per milestone), rough per-signal logic (§0.5.8.4), and the resolved
decisions (§0.5.8.5). Checked against a real #1 Demo parse and a Fable-model
fidelity review that caught + fixed three blocking errors (§0.5.8.6); the AoE
readout (#17 Wild Imp text) was promoted into v1.

**M3 scoping history.** Since M2.5 it picked up an
**aesthetic revision** (2026-07-19: icons left native, no tint, 4-letter labels
dropped, green-monochrome relaxed) and was **staged into M3a/b/c** (see §6). A
doc-consistency pass (**2026-07-20**) took `guidance-model.md` as the authority and
re-synced `spec.md` §0/§3 + this doc against it — propagating the two §0.5.8.6
blocking-error fixes that had never left the guidance doc (the Tyrant+Dreadstalkers
go-gate; the ~5 s not ~15 s HOLD lead), giving M4/M5/M7 their missing §0.5.8 rows,
and closing the cast-read verify **as an assumption** (§7) — which retires the
`Core*` asterisks. `notes.md` was then **split** (2026-07-20): current framing
stays, and the superseded material — the green-phosphor icon-tint era, the
curated-layout machinery, the wrong assumptions — moved to **`notes-archive.md`**.
All four live docs now agree. **M3a then built against that settled scope** — see
the Status block above and §6.

(Prior: M0.5 shipped the guidance model §0.5 — archetype + mode model, salience
moments, attention research, signal map, blind spots, backlog seed; M2/M1/M0 done.)

Platform facts: **v1 target = Demonology Warlock**; live client **12.0.7**
(source-grounded @ build 68453). Addon repo: `michac/CDMProbe` (at `addon/`).

---

## 6. Milestone log

Ordering rationale (2026-07-17): **prove the rendering stack works before wiring
real config.** The overlay is authored *against* an imported layout (§0 pillar
1), so it's tempting to build config first — but the open risk was whether we can
skin + anchor at all. So M1 was a throwaway-content prototype that answered that;
only then do we author the real config (M2) and re-point the skin at it (M3).

Refinement (2026-07-19): **M0.5 defined the guidance model; M2.5 commits it to a
concrete, scoped v1 indicator list *before* M3 turns it into code** — so M3 builds
against a settled *what*, not a menu of candidates. (Same shape as M2: a
decision/spec milestone that de-risks the build that follows.)

- **M0 — feasibility probe (done, CDMProbe v0.1–v0.2.2).** `dump` / `skin` /
  `shards` / `secret` / `log` / `casts`. Confirmed the §1 capability map;
  hardened against Secret-Values taint; reports persist to SavedVariables (read
  off disk). Deep-dive source research on item skinning (§1 skinning specifics)
  and the §5 three-layer config model.

- **M1 — Prototype skin (feasibility, dummy content) — ✅ DONE (v0.5.2).** Built
  `/cdmp crt`: keep-and-tint the Essential/Utility icons (green phosphor), dummy
  chrome (label / keybind / block-char meter), scanline/vignette overlay, a
  viewer-anchored shard rail, and a `DEMONOLOGY.SYS` terminal frame. **All five
  feasibility questions pass** (full write-up + corrections in `notes.md` §9):
  - **F1** keep + `SetDesaturated`/`SetVertexColor` the real icon in place — ✅.
  - **F2** draw our regions over a secure item, no taint — ✅.
  - **F3** scanline/vignette overlay on the viewer — ✅.
  - **F4** custom rail anchored to the viewer **rides along** on CDM move — ✅.
  - **F5** persist across Blizzard's repaints — ✅, but via **per-item leaf-method
    hooks** (`RefreshIconColor` / `RefreshIconDesaturation` / `RefreshSpellTexture`),
    **not** the `RefreshData`/`RefreshLayout` hook first assumed (that missed the
    `SPELL_UPDATE_USABLE`/range recolor paths and still flashed white).
  Also learned: nothing clips our overlay (draw per-icon readouts freely); the
  terminal banner must be compact on a narrow vertical column. Two perf cleanups
  deferred to M3 (event-driven re-hook; tiled scanline texture).

- **M2 — Config foundation — ✅ DONE (2026-07-18, decision-only, no new code).**
  The milestone **collapsed to a scoping decision** once three things became
  clear (this session):
  1. **Don't author/apply a Cooldown Layout string (layer ①).** Instead of
     shipping a curated tracked-set, the overlay binds to whatever layout is
     **currently active**, keyed per item by `GetCooldownID()` on the
     `RefreshLayout` hook (source-verified, `notes.md` §5/§9). Reorder-safety and
     missing-spell-skip come **free** from binding-by-ID + iterating only live
     frames. Baseline we design against = the **real DB2-default filtered set**
     (`CooldownSet`/`CooldownSetSpell`, spec 266 = set 60), not the customized
     old §2 list. Curated layer-① override → deferred to **M7**, only if defaults
     prove insufficient (the noisy 13-spell Utility default is the likely trigger).
  2. **Don't reposition the CDM frames.** They're Edit Mode system frames
     (protected, manager-owned position); no clean runtime/auto-reverting move
     exists, and forcing one desyncs Edit Mode (`notes.md` §5, source-grounded).
     The addon **never moves the CDM**; the user positions it once and our
     overlay flanks it (anchored to the viewer, vanishes cleanly when off).
  3. **Assume a vertical layout** (opinionated personal mod) rather than staying
     orientation-agnostic. User sets orientation/position once in Edit Mode.
  So M2 ships **no code** — labels/colours/keybinds/overlays now key to the live
  layout (not a frozen import), which is what M3 builds on. **Deferred out of M2:**
  a programmatic first-run "flank" setter + save-for-undo via LibEditModeOverride
  (the only unproven feasibility piece) → optional **M7** polish; a SavedVariables
  store for *our* settings → whenever M3+ produces the first real user toggle
  (none defined yet — YAGNI).

- **M0.5 — Purpose & guidance design — ✅ DONE (2026-07-18, docs-only).**
  Shipped **`guidance-model.md` (§0.5)**: the builder/spender archetype + a
  computable **generate/spend/burst mode model** (§0.5.1), a **ranked salience-moment
  list** (§0.5.2), a fresh deep-research **attention-mechanism digest** (§0.5.3,
  cited), the **moment→readable-signal map** (own/borrow/can't, §0.5.4), the honest
  **blind-spot list** (§0.5.5), and the **M3–M6 widget backlog seed** (§0.5.6).
  `spec.md` §0/§3 now point at it as the rotation-helper contract. No addon code.
  A research/design milestone — **no addon code**, output is a written proposal that
  becomes the M3–M6 widget backlog and updates `spec.md` §0/§3. The realization
  (2026-07-18): the overlay's real job is to be a **rotation helper**, not just a
  themed skin. So before adding widgets, decide *what to signal, when, and how*.
  Three phases:
  1. **Source first — distill the rotation into moment-to-moment decisions.** From
     `knowledge/classes/warlock/demonology/rotation.md` (Diabolist, 12.0.7) +
     `notes.md` §2, extract the actual *"what do I press next and why"* — the
     priority gates, the Tyrant burst-window setup, the shard build/spend loop,
     the proc reactions. Output = a ranked list of **salience-worthy moments**
     (the instants where a good player changes what they do).
  2. **Research attention mechanisms — visual + audio.** How to grab a player's
     eye without them *reading* (preattentive features: motion, luminance,
     colour, size, flicker; glanceability; peripheral vs foveal) and ear (earcons,
     pitch/urgency, distinctness, non-annoyance/accessibility limits). Grounded in
     real sources (HUD/glanceable-UI design, game-feel, WA/rotation-helper prior
     art), not vibes.
  3. **Map moments → our readable signals, within the §1 limits.** Cross each
     salience moment against the capability map (`notes.md` §1): what we can
     **read & branch** (Soul Shards, proc *presence* via `IsShown`, player-cast
     napkin timers) vs only **display/borrow** (cooldown swipe, buff bars, native
     alerts) vs **can't help** (secret timers/counts — imp count ≥6, exact CD
     remaining). Propose, per moment: the readable trigger → the attention
     mechanism (visual and/or audio). **Explicitly flag the moments we cannot
     assist** so the design is honest about its blind spots.
  Deliverable: a "guidance model" section (spec.md §0.5 or a new doc) — the
  contract M3+ widgets implement, so we build salience *for the rotation*, not
  decoration.

- **M2.5 — v1 indicator set — ✅ DONE (2026-07-19, docs-only, no addon code).**
  Distilled the §0.5.4 signal map + §0.5.6 backlog into the **committed v1 indicator
  list** — the ***what*, not the *how*** — shipped as **`guidance-model.md` §0.5.8**:
  an 18-row table tagged own/borrow + Core/Stretch/Defer per milestone, rough
  per-signal logic (§0.5.8.4), and resolved decisions (§0.5.8.5). Two things
  sharpened it past the raw §0.5.6 list: a **cut principle** (Own + P0/P1 → Core;
  pure-Borrow / P2–P3 / needs-layer-①-override → Stretch/Defer), and three
  **cross-cutting dimensions** the design session surfaced — a **pre-pull affordance**
  (PREP chrome + scripted opener queue + fill-to marker), an **anticipation layer**
  (ghost incoming-shard + predictive SPEND pre-flip during a cast), and an
  **escalating burst telegraph + short-CD napkin pings** (one `GetSpellBaseCooldown`
  engine → Tyrant 60 s telegraph, Dreadstalkers ~20 s, Implosion ~15 s). Validated
  against a real #1 Demo parse (Inphected) + a **Fable-model fidelity review** that
  caught three blocking errors — all fixed (§0.5.8.6). **Open sub-questions —
  resolved:** mode indicator → **split** (GENERATE↔SPEND chrome in M3, BURST folds
  into M4); borrowed Core/Dominion bars → **Stretch (M5)**; Wild Imp/AoE text →
  **promoted to Core (M5)** so v1 covers AoE; predictive ritual tracker → **Defer
  (M7)**; audio → **Stretch**, shard-cap earcon the one near-essential. Like M2, a
  decision milestone that de-risks M3 by settling scope before code.

- **M3 — First real skin.** *Builds the committed M2.5 v1 indicator set.* Re-point
  the M1 prototype at the **live layout** (bind per item by `GetCooldownID()` on
  the `RefreshLayout` hook — reorder-safe, skips absent spells; see the M2 decision
  + `notes.md` §5/§9).

  **Aesthetic revision (2026-07-19).** Keep the **terminal / TUI feel** (monospace,
  scanline chrome, block-char meters) but **relax the hard green-monochrome
  constraint** — colour may now carry meaning (group / mode / readiness), and we
  **stop tinting the Blizzard cooldown icons for now**: desaturating + green-tinting
  them measurably *hurt* cooldown legibility (native swipe + countdown read worse),
  which defeats the point of keeping the icons at all. v1 therefore leaves the icons
  **native and untouched** and builds the value-add in the **terminal chrome around
  them**; the leaf-method tint hooks (§9) go **dormant** (kept, not deleted — they
  gate a future optional solid-colour mode). Also **drop the per-icon 4-letter
  ability labels** — noise that obscured the swipe / countdown and only pays off in a
  solid-colour skin. Keybinds stay as small corner chrome. The §3 group **colour
  map** + **generator-vs-consumer batch tint** move onto **our** icon-adjacent
  accents (borders / ticks / burst-lane backdrop / rail + mode hues), not the icon
  art. *(Doc sync **done 2026-07-20**: `spec.md` §0/§3 rewritten to match — pitch,
  pillars, aesthetic block, layout sketch, colour language, encoding table, and new
  design language for the mode spine + cross-cutting dimensions. `notes.md` §4 —
  which lives in `notes.md`, not `spec.md` — was swept in the same pass, and the
  superseded green-phosphor exploration moved to `notes-archive.md`.)*

  Staged into three independently-deployable sub-builds:
  Coverage against §0.5.8.3: **M3a** = #4 · **M3b** = #5, #2, #3 · **M3c** = #1,
  #6, #7, #8. All eight M3-assigned rows land. *(Keybinds are the one M3 deliverable
  **not** in the §0.5.8 indicator table — they're identity **chrome**, not a
  rotation signal, and sit outside the indicator contract by design.)*

  - **M3a — identity + chrome (no icon tint) — ✅ SHIPPED (2026-07-20, v0.6.0);
    in-game pass outstanding.** `/cdmp hud`: real **keybinds** per tracked spell
    (180-slot action-bar scan → binding, cached, **out-of-combat only**; unbound →
    blank, never a placeholder), the §3 group colour map + generator/consumer batch
    tint on **our** accents, and the `DEMO.SYS` terminal frame + scanline overlay.
    Both deferred perf cleanups folded in (`notes.md` §9).

    **What the build decided (things the plan left open):**
    - **`CRT.lua` deleted, `/cdmp crt` retired.** Its still-valuable parts moved:
      terminal frame + scanline/vignette → `HudChrome.lua`, the viewer-anchoring
      idiom → `HudCore.lua`, and the **leaf-method icon-tint machinery →
      `HudTint.lua`, dormant and unwired** (`notes.md` §9 explicitly wants it kept).
    - **Per-spec data is one table**, `SpecDemonology.lua` — spellID → group / role
      / ghost yield / base CD, hues reused verbatim from `Resource.lua`. The render
      modules now hold **no spell constants at all**, which is the seam M7's second
      spec plugs into. `baseCD` is filled in only where the docs actually assert it;
      elsewhere it's nil on purpose (M4 reads `GetSpellBaseCooldown` at runtime —
      this table is the sanity check, not a guess). Unknown spellIDs → neutral
      accent; a **Secret Value is never used as a table key**, so an unreadable ID
      is treated as unknown rather than guessed.
    - **Encoding split, so M3b can't collide with M3a.** Hue carries **group only**;
      the builder/spender batch tint rides on **saturation + edge thickness + alpha**
      and deliberately leaves **luminance** alone — luminance is reserved for
      readiness (M3b). Edge thickness doubles as the redundant non-colour signifier
      ([X1]).
    - **Scanline: took the named fallback, not the tiled texture.** A fixed,
      hard-capped pool re-anchored on reflow rather than a bundled power-of-two art
      file — same O(1)-allocation property, no binary asset whose in-game load we
      can't verify from here (`notes.md` §9).
    - **Settings store opened early.** `ns.db.hud = { on, opener }` exists now
      (M3a only uses `on`); the real user choice — `opener` — lands in M3c. No
      config UI, slash args only.

    **Outstanding in-game pass** (the reason this is "shipped", not "done"):
    native art/swipe/countdown survive · accents match §3 · keybinds match the real
    bars and update on rebind · frame + scanlines don't clip the narrow column ·
    Edit Mode drag rides along · Orientation/#Rows change increments the
    `/cdmp hud status` fire count with **nothing detaching and no ticker running** ·
    tracked-set change gives new items chrome · off → pixel-clean, `/reload`
    restores. **Dropping the ticker is the one real regression risk** — if items
    detach, the fix is another *event*, not the ticker back, and which event was
    missing gets recorded in `notes.md`.
  - **M3b — readiness + procs.** Icons left native ⇒ Blizzard's on-cooldown dimming
    is preserved for free, which **resolves the §9 "ready vs on-cooldown" decision by
    dissolving it** (we no longer own that pixel): we *add* a ready accent (off the
    observed ready edge — hook `OnCooldownDone` / `TriggerAvailableAlert`, no secret
    read) + **empty-board recede**, and the **Demonic Core proc-glow on Demonbolt** +
    **Demonic Art proc-glow on the transformed button** (`IsShown`), as styled glow
    overlays.
  - **M3c — resource + mode + anticipation.** The owned **shard rail** (segmented
    fill, cap flip + one-shot glitter + earcon), **GENERATE↔SPEND mode chrome tint**
    (pure shard threshold), the **anticipation layer** (ghost incoming-shard during an
    in-flight builder cast + predictive SPEND pre-flip — `UNIT_SPELLCAST_START` /
    `SUCCEEDED` spellIDs assumed readable, see §7), and the **pre-pull opener queue** +
    fill-to marker.

- **M4 — Burst window + the napkin engine.** Builds §0.5.8.3 rows **#9, #10, #11,
  #12**. Our overlay frames **beside** the vertical CDM group the burst lane
  (**Tyrant · Dreadstalkers · the tracked Grimoire summon**); shared lane tint
  (common region) — the horizontal "line Tyrant up with what it buffs" grouping,
  realized in *our* overlay, not the CDM's layout.
  - **#9 Burst lane + common-fate brighten.** The **go-gate is Tyrant +
    Dreadstalkers only**; the Grimoire **brightens if up but is never a gate**
    (~2-min CD, absent ~half the windows — 21 casts vs 48 Tyrant). *(§0.5.8.6
    blocking error #2.)*
  - **#10 BURST mode activation** — the spine's hot state, folded into the lane
    rather than shipped as a separate widget (§0.5.8.5-A).
  - **#11 Tyrant telegraph — two leads, do not conflate.** `WARMUP_LEAD ≈ 15 s` =
    **awareness only, non-instructional** (a low-salience "approaching" glow; does
    **not** stop the player dumping, never overrides the P0 overcap cue).
    `HOLD_LEAD ≈ 5 s` (≤2 GCDs) = **instructional** HOLD/BANK + stage, crescendo
    into a motion onset at ~0. The short hold is load-bearing: a 15 s freeze
    **force-overcaps** (Cores proc ~every 3.6 s, Demonbolt refunds +2).
    *(§0.5.8.6 blocking error #1 — the lead was 3× too long.)*
  - **#12 Short-CD approach pings** — Dreadstalkers ~20 s, Implosion 15 s, ~1 GCD
    out, off the same `GetSpellBaseCooldown` engine. The **Dreadstalkers ping
    suppresses when Tyrant is imminent** and becomes a "stage for Tyrant"
    treatment: one Dreadstalkers per cycle is held so the dogs are fresh *inside*
    the window. Implosion's ping is gated on `in_aoe` (§7) and says "it's
    available", never "it's worth it" — the ≥6-imp value gate stays a **Can't**.
  - Ground truth always wins: every napkin cue rounds down / fires early and yields
    to the native ready-alert.

- **M5 — AoE readout + borrowed bars.**
  - **#17 Wild Imp stack text + static "/6" — Core.** Enlarge Blizzard's own
    stack-count text and append our static "/6". This is M5's **only Core row** and
    the **sole v1 assist for Demo's central AoE decision** (≥6 imps → Implosion,
    the 4th-most-pressed rotational button). Promoted from Defer specifically so v1
    covers AoE, not just single-target (§0.5.8.5-C) — do not let it fall out with
    the Stretch rows below.
  - **#13/#14 Borrowed Demonic Core + Dominion of Argus bars — Stretch.** Restyle
    the secure BuffBar viewer to match the skin. Pure Borrow: the Own proc-glows
    (#2, #3) already carry the *decisions*, so these are duration prettiness —
    **cut without shame** under time pressure.

- **M6 — Audio — Stretch (§0.5.8.5-D).** Wire the §3 earcon set: our shard-cap
  (#15, the one near-essential sound — it pairs with the P0 anchor and reads as
  **"spend or waste"**, not a fanfare) + proc-gained ding, native ready / pandemic
  alerts (#16); LibSharedMedia registration + per-event toggles + global mute.

- **M7 — Post-v1: enforcement + predictive tracker + second spec + polish.**
  (v1 = the M3→M6 arc for Demo; everything here is explicitly after it.)
  - **#18 Predictive Diabolic Ritual tracker — Defer/M7.** Surface which Demonic
    Art arms next from the active ritual stage (the wheel turns Overlord → Mother
    of Chaos → Pit Lord in fixed order). **Gated on the curated layout override**:
    it needs the per-stage ritual auras in the tracked set, and only the `428514`
    container is tracked today (`notes.md` §2).
  - **Curated layer-① Cooldown Layout string + enforcement-strength UX**
    (auto-apply → import-and-verify → nag) — the M2-deferred profile question, and
    the enabler #18 depends on.
  - Prove the pattern on a **second spec**; **cyberpunk-skin stretch** art pass
    over the block / rail / bar styling; the deferred first-run "flank" setter via
    LibEditModeOverride.

---

## 7. Open questions / verify-in-game

- [x] **`/cdmp casts`** — player-cast spellIDs readable in restricted combat:
      **CLOSED as a design assumption (2026-07-20).** `SUCCEEDED` confirmed in a
      delve; **`START` confirmed at an open-world target dummy (2026-07-19)**;
      v0.5.3 logs START/SUCCEEDED/STOP/INTERRUPTED per-phase. A raid-boss
      confirmation was never obtained and **we are no longer waiting on one** — the
      design now **assumes both events carry a readable spellID in all combat
      contexts**. Consequence: the §0.5.8 `Core*` asterisks are **retired** (rows
      #7/#8/#10/#11/#12 are plain **Core**), and the reactive/borrowed fallback is
      demoted from a planned degradation path to a contingency we'd only build if
      the assumption is ever falsified in play.
      *Note — no separate `UnitCastingInfo` verify is needed:* "cast in flight" is
      derived from our own `START` → `SUCCEEDED`/`STOP`/`INTERRUPTED` bookkeeping
      (already logged), so the anticipation layer rides on the same assumption
      rather than on a second, untested API.
- [ ] **`in_aoe` predicate** — can we cheaply determine multi-target context
      (target count / recent multi-hit) to gate the Implosion approach ping (#12)
      and the Wild Imp "/6" readout (#17)? Flagged in §0.5.8.2(c) / §0.5.8.3; the
      AoE cues have no honest trigger until this is answered. Nameplate-count and
      recent-multi-hit heuristics are the candidates.
- [ ] Buff-vs-cooldown: can we access the self-buff remaining AND the
      cooldown-to-recast as **two** durations, or only Blizzard's one sequenced
      display? (e.g. Summon Demonic Tyrant — verify a spell can live in both
      Essential + BuffBar categories at once.)
- [ ] Pandemic/ready **replacement**: confirm the `PandemicIcon` (and `Available`
      alert / `CooldownFlash`) shown-state is observable so we can hide Blizzard's
      and drive our own arbitrary indicator (offset arrow) — verify-in-game.
- [~] Which profile do we standardize on (Kalamazi Demo CDM vs a curated set)?
      **DEFERRED to M7** (2026-07-18): v1 binds to the **active** layout, not a
      shipped one (see M2 decision). If the DB2 defaults prove insufficient, this
      re-opens as a curated **Cooldown Layout string** (system ①). Baseline for
      design = the DB2-default filtered set (`CooldownSet`/`CooldownSetSpell`).
- [x] **Icon-tint persistence / repaint choke point** — RESOLVED (M1, v0.5.2):
      hook the per-item **leaf** methods `RefreshIconColor` /
      `RefreshIconDesaturation` / `RefreshSpellTexture` and re-force our color
      after Blizzard. `RefreshData`/`RefreshLayout` alone is insufficient — see
      `notes.md` §9.
- [x] **Do our overlays get clipped to the CDM pane?** — RESOLVED (M1, source):
      **NO** `clipsChildren` in the CDM templates; the `MaskTexture` masks only
      the `Icon`. Draw per-icon readouts in any direction (`notes.md` §9).
- [x] **`SetLayoutData` writability** — RESOLVED (2026-07-17, `/cdmp layout write`,
      out of combat): the call is **permitted from addon code, no blocked-action
      error** → **auto-apply is viable** (program the layout, don't just ask for a
      paste). Two caveats for *how*: (a) `SetLayoutData(str)` replaces the **whole**
      data store (every spec's layouts) — don't clobber; (b) the clean single-layout
      **merge** is `CooldownViewerSettings:GetLayoutManager():ImportLayout(str, info)`
      (what the Import button calls). Follow-up sub-probe: is `ImportLayout`
      addon-callable too? In-combat writability still expected-blocked (untested).
- [x] **Does the export string carry position/orientation?** RESOLVED
      (2026-07-17, source): **NO** — the Cooldown Layout string is only
      `COOLDOWN_ORDER` + `CATEGORY_OVERRIDES` + `ALERT_OVERRIDES`. Orientation /
      size / position are Edit Mode (a *separate* string). Hence the three-layer
      model + anchoring in §5; we do **not** reposition secure CDM frames — we
      anchor our overlay to them and use `LibEditModeOverride` only to set the
      Orientation default out of combat.
- [x] **Alerts in the layout string?** RESOLVED (2026-07-17, source): **YES** —
      `ALERT_OVERRIDES` serializes per-cooldown sound/visual alert config, so
      native alerts ship *inside* the import string (secure, combat-safe). Still
      open: whether an addon can **inject/override** alerts *outside* the string
      programmatically, and whether a custom `.ogg` can substitute a built-in.
- [x] **Wild Imp count** — RESOLVED: `Applications` is Blizzard-displayed but
      **secret** to us. The gate that matters is **≥6 imps → Implosion**, so the
      readout is "[X]**/6**": enlarge Blizzard's X and append our static **"/6"**
      (§0.5.8 #17). We cannot compute "≥6" ourselves.
- [x] **Demonic Core count** — RESOLVED, same mechanism, **different constant**:
      cap is **4**, so any borrowed readout is "[X]**/4**". We surface Core
      *presence* only (moment #2) — the near-cap-4 overcap gate is invisible to us
      (§0.5.5). *(Corrected 2026-07-20: these two were previously one entry using
      "/4" for both, which would have shipped the wrong denominator on the imp
      readout.)*

# Cooldown HUD — milestones & status

> Roadmap, milestone log, and the "confirm while logged in" queue.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> §0.5 Guidance model → `guidance-model.md` · §1–§2, §4–§5, §9 → `notes.md` ·
> §6 Milestones + §7 Open questions → **this doc**.

## Status

**Current: M0.5 done** (2026-07-18, docs-only — no addon code) — the overlay's job
is a **rotation helper**, not just a skin; *what to signal, when, and how* is now a
written contract in **`guidance-model.md` (§0.5)**: the builder/spender archetype +
generate/spend/burst mode model (§0.5.1), the ranked salience moments (§0.5.2), the
attention-mechanism research digest (§0.5.3), the moment→readable-signal map
(§0.5.4), the honest blind-spot list (§0.5.5), and the M3–M6 widget backlog seed
(§0.5.6). **M3–M6 now build against §0.5.** **Next: M2.5 — commit the v1 indicator
set** (turn the §0.5.4/§0.5.6 candidates into the definitive prioritized v1 list —
the *what*, not the *how*), **then M3 — first real skin.**

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

- **M2.5 — v1 indicator set (the widget spec; next — no addon code).** A short
  planning/decision milestone: distill the §0.5.4 signal map + §0.5.6 backlog seed
  into the **committed v1 indicator list** — exactly which indicators v1 ships, each
  tagged **own / borrow**, in **priority order**, with an explicit **in-v1 vs
  deferred** cut line (e.g. is the mode indicator in v1 or a candidate? does the
  predictive Diabolic-Ritual tracker wait?). The ***what*, not the *how*** — no Lua,
  no pixel layout, no colour hex. Output: a concise **"v1 indicator set" section**
  (a new §0.5.8 in `guidance-model.md`, distilled from §0.5.4/§0.5.6) that M3+ builds
  against 1:1. Like M2, this is a decision milestone that de-risks M3 by settling
  scope before code. **Open sub-questions to resolve here:** which indicators are
  v1-essential vs nice-to-have; whether any "own" signal is deferred for effort;
  whether any "borrow" bar (Demonic Core / Dominion) is v1 or M5; where the mode
  indicator lands (M3 chrome tint vs M4).

- **M3 — First real skin.** *Builds the committed M2.5 v1 indicator set.* Re-point
  the M1 prototype at the **live layout**
  (bind per item by `GetCooldownID()` on the `RefreshLayout` hook — reorder-safe,
  skips absent spells; see the M2 decision + `notes.md` §5/§9): real
  4-letter labels + **real keybinds** (read the binding per tracked spell), the
  §3 group **colour map**, **generator-vs-consumer** batch tint (build→spend axis
  reads preattentively), and the **Demonic Core proc-glow on Demonbolt**
  (`IsShown`). Real shard rail (readable + branchable) with cap glitter + sound.
  Fold in the deferred perf cleanups (event-driven re-hook, tiled scanlines) and
  decide the "ready vs on-cooldown" re-encoding now that we own the icon color
  (`notes.md` §9).

- **M4 — Burst-window overlay.** Our overlay frames **beside** the vertical CDM
  group **Tyrant · Dreadstalkers · Grimoire: Fel Ravager**; shared lane tint
  (common region) + common-fate brighten when all are up. The **napkin-math
  timer** (§1: player-cast → `GetSpellBaseCooldown` countdown, fixed-CD only)
  drives a salience pop as Tyrant nears ready. This is the horizontal "line
  Tyrant up with what it buffs" grouping — realized in *our* overlay, not the
  CDM's layout.

- **M5 — Borrowed DoT/proc bars.** Restyle the secure BuffBar viewer (Demonic
  Core, Dominion of Argus) to match the skin.

- **M6 — Audio.** Wire the §3 earcon set: our shard-cap + proc-gained, native
  ready / pandemic alerts; LibSharedMedia registration + per-event toggles +
  global mute.

- **M7 — Profile enforcement + second spec + polish.** Choose enforcement-strength
  UX (auto-apply → import-and-verify → nag); prove the pattern on a second spec;
  **cyberpunk-skin stretch** art pass over the block / rail / bar styling.

---

## 7. Open questions / verify-in-game

- [ ] **`/cdmp casts`**: is `UNIT_SPELLCAST_SUCCEEDED`'s spellID readable in
      restricted combat? Prototype built + works in a delve; **verify a live `==`
      in a raid** (decides the roll-your-own Tyrant timer — §1).
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
- [x] Wild Imp / Demonic Core **count** — RESOLVED: `Applications` count is
      Blizzard-displayed but **secret** to us. For "[X]/4", enlarge Blizzard's X
      and append a static "/4"; we cannot reliably count procs ourselves.

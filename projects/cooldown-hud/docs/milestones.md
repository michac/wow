# Cooldown HUD — milestones & status

> Roadmap, milestone log, and the "confirm while logged in" queue.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> §1–§2, §4–§5, §9 → `notes.md` · §6 Milestones + §7 Open questions → **this doc**.

## Status

**Current: M1 done** (CDMProbe **v0.5.2**) — the prototype skin is validated
in-game; F1–F5 all pass (see `notes.md` §9 for the verdicts + the leaf-method
persistence fix). **Next: M2 — config foundation** (author + auto-apply the
per-spec Cooldown Layout string, set Orientation=Vertical, confirm anchor-follow
against the real tracked set).

Platform facts: **v1 target = Demonology Warlock**; live client **12.0.7**
(source-grounded @ build 68453). Addon repo: `michac/CDMProbe` (at `addon/`).

---

## 6. Milestone log

Ordering rationale (2026-07-17): **prove the rendering stack works before wiring
real config.** The overlay is authored *against* an imported layout (§0 pillar
1), so it's tempting to build config first — but the open risk was whether we can
skin + anchor at all. So M1 was a throwaway-content prototype that answered that;
only then do we author the real config (M2) and re-point the skin at it (M3).

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

- **M2 — Config foundation.** Make it real underneath. Author the per-spec
  **Cooldown Layout string** (system ①, §5) for Demo; **auto-apply** it via
  `CooldownViewerSettings:GetLayoutManager():ImportLayout(str)` (OOC — confirmed
  viable, §7); set **Orientation=Vertical** default (system ②, LibEditModeOverride,
  OOC); confirm anchor-follow against the real tracked set + order. After M2 the
  layout is **fixed and known**, so labels / colours / keybinds / positions have
  a deterministic thing to key to.

- **M3 — First real skin.** Re-point the M1 prototype at the M2 layout: real
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
- [ ] Which profile do we standardize on (Kalamazi Demo CDM vs a curated set)?
      Whichever it is, it's authored as the per-spec **Cooldown Layout string**
      (system ①) — export a real one in-game as the baseline (M2 input).
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

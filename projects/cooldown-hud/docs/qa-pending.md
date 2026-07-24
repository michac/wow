# Cooldown HUD — pending QA (in-game verification of shipped code)

> **These are QA / clean-up items, NOT roadmap blockers.** Every item is **code
> already shipped** (CDMProbe ≥ v0.13.0) that wants a confirming pass at a target
> dummy / in real content. The roadmap (M4+) does **not** wait on them — they're
> "confirm when convenient", batched into one play session. The **how** (exact
> commands, expected output) lives in `verify-runbook.md`; this is the **what + why**
> and the checkbox of record. `milestones.md` keeps the full design history.

When you do sit down for a session they build on each other, so run them in order:
**§7.6 → §7.3 → §7.4 → §7.5**. §7.7 (opener) is board-independent and can go any time.

- [ ] **§7.6 — M3e pull recorder** *(self-verifying)*. Play a dummy pull; confirm
      `CDMProbeDB.pulls` captured the lit-count histogram + peak set + transition tail.
      It succeeds when it produces the evidence the other passes need.
- [ ] **§7.3 — M3c-b strictness / truth pass.** The real test: `lit now` names **1–2**
      abilities (not 4–5) and each stated reason is one you agree with. Exit criterion the
      others inherit.
- [ ] **§7.4 — M3d out-of-combat seeding.** A `/reload` mid-cooldown shows
      `~42.1s (read)`, not `NEVER · no edge seen yet`; seed-vs-edge provenance correct in
      `hud status`.
- [ ] **§7.5 — M3c-c1 shard rail + mode spine.** Rail not clipped; GENERATE↔SPEND↔PREP
      reads; mode chrome on rail + terminal only, never an icon.
- [ ] **§7.7 — M3c-c2 opener** *(board-independent)*. ⚠ **Reworked in M4** — re-verify
      against the new behavior (own positionable pane, prereqs row, start-on-first-key),
      not the v0.17.0 strip. See the opener redesign in `milestones.md`.
- [ ] **M4-1 — desync fix (the reason M4 exists).** OOC, target dummy, `/cdmp hud
      opener on`. Cast SB/DB to cap shards → the pane **must NOT advance** (stays primed
      on Dreadstalkers). Press Dreadstalkers → it un-primes and drains correctly.
- [ ] **M4-2 — the pane persists.** `/cdmp hud pane unlock`, drag it over your head,
      `/reload` → position holds (`ns.db.hud.sequence`). Locked = click-through (no
      mouse capture over the world/units).
- [ ] **M4-3 — build-to-cap for the Tyrant window** *(revised — burst-prep tuning)*.
      Tyrant far / mid-sustain: HoG greenlights at **3** shards, unchanged. Tyrant
      within ~5 s / ready + low shards: the **builder (SB) reads ROTATION "cap for
      Tyrant"** and **HoG reads AVAILABLE "build to cap for Tyrant"** while shards < 5;
      **at 5 shards HoG greenlights again** (spend/sustain, never overcap sitting at 5).
      Cast Tyrant → BURST ends → HoG dumps. (`/cdmp hud status` + `hud debug` reasons.)
- [ ] **M4-4 — the burst window + Dreadstalkers stage-hold** *(revised)*. Pull; reach a
      Tyrant window → mode flips **BURST** (rail amber `[*]`), the pane re-arms with the
      burn sequence. In the window, **Dreadstalkers reads AVAILABLE "stage for Tyrant"**,
      not "use on cooldown"; outside the window it greenlights on cooldown as before.
      Dissolves on window close. ⚠ **Tune `HOLD_LEAD` (5 s)** off the recorded `/cdmp hud
      log` transitions — the one knob for both the build-to-5 and the stage-hold; only
      ever holds, so the safe direction.
- [ ] **M4-5 — juice.** Correct key flashes; completing the sequence flourishes; a miss
      only dims gently (never a scold). Confirm no `PlaySound` (audio is M6).
- [ ] **Folded in:** M3a relayout check (Edit Mode reorder → nothing detaches) + M3b
      readiness / procs.

**Tuning is downstream, not here.** If §7.3's histogram shows a fat 4+ tail, tightening
`HudScore` is the *next* milestone's work on that evidence — measuring and tuning in one
session tunes against a number the same session invented (the M3e doctrine).

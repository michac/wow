# Combat Assist Plus — backlog

**What this file is for:** the list of work items. One line per item, newest
thinking at the top of its section. An item here is *agreed work not yet done* —
if it's speculative, it goes under **Ideas**; if it's done, it leaves this file
and the outcome is recorded in `notes.md`.

Keep items small enough to finish in a session. An item that needs a paragraph to
explain is a sign the answer belongs in `spec.md` first.

Items carry the `spec.md` section they implement. A milestone is done when all of
its items are.

## Now

**⚠ M2 is code-complete and NOTHING HAS BEEN FLOWN.** The deployed build is **v0.1.1,
the scaffold** — the game folder holds `.toc` + `Core.lua` only. `Bind.lua` and
`Frame.lua` are working-tree-only, and `ghaddons` installs from the latest *release*.
Code-complete is not done.

**M2a is done** (2026-08-06 — see below and `notes.md`); M2b/M2c/M2d remain.

**The four milestones below run in order and gate M2.** They exist because the first
build put a lab inside the product: cap grew slash-command dumps that print to chat,
and chat has no copy/paste, so the one output that has to reach the analysis machine
was the one that could not leave the client (house rule 4). The correction is a
separation — **client behaviour is a ClientLab question; cap's own state is a capture
log** — and cap ends up needing almost no diagnostics of its own.

### M2a — Lab the four client questions, and fly the lab ✅ DONE 2026-08-06

All four measured in one session and drained (OBS-056…059); the four tests are deleted
and the lab is back to 7 built ids. Session log + what each result costs cap: `notes.md`.

- [x] **`item.cooldownID` — can it read secret, and when?** → **it never did.** 26 rows,
      all four viewers, 4 OOC runs + 13 in-pull samples, zero secret reads on the field
      or the accessor. `cooldown-manager.md:740` `[client 2026-08-06]`.
- [x] **Does `GetItemFrames()` on a HIDDEN viewer return children?** → **yes, all of
      them.** Every item template sets `includeAsLayoutChildWhenHidden`, so the
      `IsShown` leg of the layout filter never binds on a CDM row.
      `cooldown-manager.md:857` `[client 2026-08-06]`.
- [x] **Is an ordinary addon frame parented to UIParent `IsProtected() == false`?** →
      **yes, and re-anchoring it to a protected frame does not change that**; in combat
      SetPoint / SetScale / Show / Hide all succeeded.
      `security-taint-and-restricted-data.md:127` `[client 2026-08-06]`.
- [x] **Does re-anchoring re-clamp after a UI-scale change?** → **the clamp is
      continuous and applied inline**, so nothing needs re-anchoring for that reason.
      `frames-textures-animation.md:467` (new §3.6) `[client 2026-08-06]`.
- [x] **The catalog's silences are sound.** `abilities.md`'s `@verify-ingame` on
      "Demonic Strength / Bilescourge Bombers / Guillotine / Nether Portal are not on
      the Midnight Demo tree" is resolved — and it was never an in-game question:
      the Blizzard Game Data API tree (720 / 266) is Tier 1 for exactly this, and its
      147 talent names contain none of the four, with Hand of Gul'dan / Implosion /
      Summon Demonic Tyrant / Doom present as controls. They are absent from
      `all-talents.tsv` for every spec. Marker dropped, `gen_verify` re-run.

### M2b — Strip cap's diagnostic surface

- [ ] Remove the remaining diagnostic code from `Bind.lua` and `Frame.lua` — the dense
      `ns.RegisterStatus` reporters and the helpers that exist only to render them
      (`specLabel`, `breakdown`, `ago`, Frame's status line). `/cap bind` and its chat
      dumps are already gone. What survives is the read API (`ns.Bind.*`,
      `ns.Frame.*`), which is M3's input and not a diagnostic.
- [ ] Decide `/cap status`'s fate and **write it into `spec.md` §2**, which currently
      lists "checking status" as a permitted setup affordance. Either it keeps a plain
      one-line "loaded, spec, on/off" and all diagnostics move to the log, or it goes
      entirely. Don't leave the spec saying one thing and the code another.
- [ ] `/cap move` stays — a placement affordance required by §3.4, not a diagnostic.
- [ ] **Delete `Bind.lua`'s stale-retention branch.** M2a measured `item.cooldownID`
      plain on every read, so retaining a stale id "because the new one is unreadable"
      guards a case never observed — with it go the `unreadable` counters that only feed
      it. ⚠ The field is not *annotated* non-secret, so the class-check on read stays;
      what goes is the branch built on the class coming back secret.
- [ ] **Fix the `hidden` health verdict, or drop it.** `evaluate()` infers `hidden` from
      `state.frames == 0`, and M2a measured that a hidden viewer enumerates in full — so
      zero rows means the pool is empty, nothing else. Read the viewer's own `IsShown()`
      for hidden and let the row count mean *configured*; if that is more than the health
      report is worth, collapse `hidden` into `empty` and say so in `spec.md`.
- [ ] **Trim `Frame.lua:317-320`.** The `--@unverified` comment goes: the engine
      re-clamps continuously and inline, so the re-`SetPoint` on `UI_SCALE_CHANGED` /
      `DISPLAY_SIZE_CHANGED` re-asserts the *saved* position and is not what keeps the
      panel on screen. Keep the call, correct the reason.

### M2c — Give cap the standard capture log

The contract is `.claude/skills/wow-developer/references/capture-and-dump-standard.md`.
cap has **none of it today**: no `ns.Capture`, no `ns.Dumps`, no `captures` key.

- [ ] `Capture.lua` — `ns.Capture.Open(name, {sessions, cap, dedup})`, writing
      `CombatAssistPlusDB.captures.<stream>`. `sessions` and `cap` are **required**;
      nothing is unbounded. `:Line` for a greppable trace, `:Row` for a grader,
      `:Mark` for an edge.
- [ ] **Register `cap` in `wowkb.capture`'s `ADDONS` map** (`tools/wowkb/capture.py`) —
      it is currently `bb / cdmp / clab / ps` only, so `wowkb.capture cap <stream>`
      fails today. Without this the log cannot be read and the milestone is a no-op.
- [ ] Emit the binding state **on load and on every change of answer** — everything
      `/cap status` would have printed: rows resolved, per-viewer split, spec + hero
      tree, complete vs PARTIAL, unreadable/stale counts, generation, CDM health kind,
      the reason that triggered the pass. This replaces the slash command rather than
      supplementing it.
- [ ] ⚠ **Pre-rendered lines are a one-way door.** Anything a reader might later slice
      by — combat state, spec, hero tree, whether the pass was complete — must be a
      `:Mark` **now**. No extractor change can add it to a capture already on disk, and
      that exact omission cost the HUD a re-fly.
- [ ] ⚠ No game value reaches a line except through `Capture.Safe()`, which returns a
      readability class and never a raw secret. No `|cff` colour escapes inside a line.

### M2d — Fly cap and read the log

- [ ] Cut a release (**ask first** — no auto-deploy exception here) and `/reload`.
- [ ] Play normally: a pull, combat entry and exit, a hero-tree swap, a spec swap, and
      the Cooldown Manager toggled off and back on. **No typing mid-pull** — the log
      records it.
- [ ] `/reload` (SavedVariables only flush then), and read it:
      `uv run python -m wowkb.capture cap <stream>`.
- [ ] Judge against the things M2 was built to guarantee: the row count is **stable and
      non-decreasing across combat entry**; a swap produces exactly one rebind; the CDM
      going away leaves rows **retained and stale**, never dropped; missing-CDM states
      announce **once** per transition. ⚠ A `PARTIAL` out of combat is a **KB finding**
      (see M2a's first item), not merely a bug.
- [ ] Frame: drag, `/reload`, confirm it stayed; locked+empty must not eat mouse input.

## Next

**M3 — §3.1 the tier signal + §3.2 procs.** The catalog is authored; this is the
engine that reads it. The core of the addon.

- [ ] The catalog **loader + the six load-time checks** §3.5 specifies: coverage
      (every CDM-tracked row is an entry or a declared silence), breadth (≥3
      HIGH-capable entries, counting HIGH cues), no verdicts as inputs, register
      legality, **cue honesty** (a HIGH cue must carry a gate precondition), a named
      floor. These are what make the format's guarantees real rather than aspirational.
- [ ] The graded register: continuous emphasis (brightness / colour / saturation)
      driven by a quantity cap may read or hand to the engine. Soul Shards first —
      readable *and* branchable in instanced combat, so it needs no indirection.
- [ ] The threshold register: a glowing count that appears at its threshold, for
      stack-gated cues. Implosion at 6+ Wild Imps is the case that defines it.
      ⚠ **The count is drawn in the HIGH treatment** — same colour and styling as a HIGH
      icon — so Implosion *reads* HIGH without cap branching on the sealed count (§3.1).
      The engine must therefore share one treatment table between icon emphasis and cue
      text; two colour sources that drift apart is the defect to design against.
      ⚠ The FontString must be a **leaf**, and must **not** be parented to the CDM
      item — the same aura is tracked on two viewers at once and a first-match
      anchor flip-flops (`security-taint-and-restricted-data.md` §4.8.2).
      ⚠ Sequencing: the cue's gate (`ready`) is cap's, the threshold is the client's.
      Build the gate first — a cue offered unconditionally is permanently lit.
- [ ] Cooldown readiness in combat, via the out-of-combat baseline + observed alert
      edges. ⚠ Never build readiness for a **charged** ability out of Available +
      OnCooldown — the "on" edge never arrives (`cooldown-manager.md` rule 13).
- [ ] Suppress the stock CDM proc treatment and route procs into the tier instead.
      §3.2 is a replacement, not an overlay; if suppression proves impossible, that
      changes the spec.
- [ ] Demonbolt demotion at high shards — the case the whole feature exists for.
- [ ] **Honesty check**: instrument how often more than one ability is emphasised.
      §3.1's third rule (if exactly one thing is ever HIGH, the tiering is wrong) is
      the one that erodes silently, and §6 flags it as the risk to measure.

**M4 — §3.4 smart cooldowns.** The container exists (`ns.Frame.Attach(region, height)`);
the roster is in the Demonology catalog. This is the bars themselves.

- [ ] Render a bar per roster entry off a duration object — legible, accurate, **in
      combat**. ⚠ `SetMinMaxValues(0,1)` *before* `SetTimerDuration`, and
      `SetToTargetValue()` on first show or it interpolates from a stale value
      (`security-taint-and-restricted-data.md` §4.8.1 findings 3, 5).
- [ ] Time-remaining text on each bar, in combat. ⚠ `SetText` with a secret poisons
      anchoring — the FontString must be a leaf; `DurationTextBinding` is the only
      anchor-safe text route (finding 10).
- [ ] Apply the §3.1 tier signal to the bars — ready-and-HIGH emphasised,
      ready-but-hold not. Same engine as M3, second surface.

**M5 — §3.3 sequences.**

- [ ] **Author the Demonology opener** — deliberately left unwritten by the catalog
      pass rather than transcribed, because the sources describe it starting with Power
      Siphon, which needs Wild Imps you don't have at a pull. Needs a real answer, not a
      copied one. (The Tyrant burst window IS drafted, at medium confidence.)
- [ ] The detector — recognise a sequence from combat entry and your own casts, with
      no input from you.
- [ ] Primary + secondary hints on the CDM, layered over the tier signal and
      visually distinct from it.
- [ ] Drop the sequence silently and instantly when you cast off-script. No nagging,
      no correction, no resume.

**Cross-cutting.**

- [ ] Decide the fate of the `assisted-combat-next-cast-varies` lab test now that
      §3.1 no longer consumes the oracle. It is already built and deployed, so it
      costs nothing further to let it answer — and a working oracle would make a
      useful *development-time* falsification check against our own tiers. Park it
      or keep it, but don't leave it undecided.
- [ ] `/mine-addon` pass for prior art on graded emphasis under 12.0 restrictions.
- [ ] **Is target count readable, and may cap branch on it?** (`spec.md` §6.) Until the
      client fact is established the catalog cannot tell single-target from AoE, and
      every AoE opinion on Demonology — Implosion above all — is unsayable. This is a
      lab question, not a design one.
- [ ] **What does cap show when the right answer has no icon?** (`spec.md` §6.)
      Demonology's filler isn't CDM-tracked, so LOW has nothing to draw on. Either
      "nothing lit means go build" is taught and accepted, or cap draws its own icons —
      which is new surface and a different addon from one that rides the CDM. Cooldown
      HUD measured Destruction blank for 31 % of a pull, so this is not hypothetical.
- [ ] Six KB findings from this session are parked in `knowledge/_meta/kb-inbox.md`
      (four on `cooldown-manager.md`, two on `frames-textures-animation.md`) plus a
      Demonology transform spell-ID conflict. Route them; none blocks cap.

## Ideas

*(unfiltered — no commitment implied)*

- Napkin the Wild-Imp count from your own casts (readable in combat; Hand of Gul'dan
  makes three) to get a *smooth* Implosion signal, with the C-side quantiser
  underneath as the ground-truth gate. Deferred: §3.1 accepts a binary threshold cue
  as sufficient signal, and this drifts (imps expire, Tyrant extends, Implosion
  consumes).
- Sound on an ability crossing into HIGH — the moment it *becomes* right is the one
  easiest to miss visually.
- A practice/verify mode: replay a recorded pull against the sequence detector to
  see where it lost the thread, instead of eyeballing it mid-fight.
- Sequence catalogs drafted from the in-client Assisted Combat priority lists rather
  than hand-authored from guides. ⚠ On Demonology that list is thin — worth checking
  per spec before trusting it as a starting point.

## Done

*(move items here with a date, or delete them — `notes.md` carries the story)*

⚠ The four **M2 code** items below are `[code]` — written, parsed, reviewed against the
KB, and **never executed in the client**. They are not flown. See `Now`.

- [code] Bind to the CDM — `Bind.lua`: four viewers → rows keyed by `cooldownID`,
      rule-15 spellID union, rebind on spec/talent/hero-tree/`SPELLS_CHANGED`, refused
      in combat and queued. A read is **three-way** (plain / empty / unreadable), and an
      unreadable pass retains the previous rows flagged `stale` — 2026-08-05
- [code] CDM off/unconfigured detected — five states, announced **once on transition**,
      re-armed when cleared, capped at 3/session, deferred 5s past login — 2026-08-05
- [code] The free-floating movable frame — `Frame.lua`, UIParent-anchored, `/cap move`,
      position persisted as a scale-1.0-normalised centre offset (Edit Mode's own form),
      deliberately **non-secure** so M4 can relayout bars mid-pull — 2026-08-05
- [code] `/cap status` reports what's bound — and `Core.lua` gained `ns.RegisterStatus`
      so each module contributes its own line without editing Core — 2026-08-05
- [x] **The catalog's shape** (`spec.md` §3.5) — entries cannot see each other, band
      conditions are positive, cross-ability reasoning only in ≤6 named windows, and a
      closed vocabulary split into branchable **gates** vs display-only **channels**.
      §3.1's third rule is now structural, not author discipline — 2026-08-05
- [x] **The Demonology catalog** (`specs/demonology/catalog.md`) — 9 entries, 5 windows,
      4 bars, 11 declared silences, harvested from Cooldown HUD's rotation research.
      Power Siphon tiered; Demonic Strength / Bilescourge Bombers / Guillotine silenced
      as **not on the Midnight spec**; Doom silenced as a **passive** — 2026-08-05
- [x] Mark Cooldown HUD superseded — banners on its `CLAUDE.md`, `docs/status.md` and
      `docs/multi-class-rollout.md`; both root `CLAUDE.md` entries rewritten; its
      routing rule revoked and its auto-deploy exception declared dead — 2026-08-05
- [x] Visual vocabulary settled: graded where the quantity allows it, glowing
      threshold text where it's a stack count (`spec.md` §3.1) — 2026-08-05
- [x] Tier model adopted, replacing the relocated Assisted Combat recommendation
      entirely (`spec.md` §3.1, §4) — 2026-08-05
- [x] **M1** — `spec.md` §1–§5 written: what cap is, who for, the four features,
      the boundary, the constraints — 2026-08-05
- [x] Scope boundary decided against Cooldown HUD (cap supersedes it) and
      BucketBinds (`spec.md` §4) — 2026-08-05
- [x] M0 scaffold: repo `michac/cap`, `.toc`, `/cap` router, registered in
      `wowkb.addon` + `ghaddons` — 2026-08-05

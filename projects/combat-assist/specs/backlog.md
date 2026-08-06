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

- [ ] **Cut a release and fly M2.** Ask first — this project has no auto-deploy
      exception. `wowkb.addon release cap --minor` (the tree is dirty; commit the
      feature work first — `release` refuses a dirty tree), `/reload`, then work the
      acceptance list below. Everything in `Next` is built on unflown code.
- [ ] M2 acceptance, out of combat: `/cap status` shows `cdm: bound` with a plausible
      per-viewer row split; `/cap bind rows` shows sane id unions; a two-cooldownID
      ability appears as **two** rows. ⚠ `PARTIAL` out of combat means
      `item:GetCooldownID()` is unreadable somewhere we assumed it wasn't — that's a
      KB finding, not just a bug.
- [ ] M2 acceptance, combat + swaps: entering combat queues the rebind and the row
      count stays **stable and non-decreasing**; a hero-tree swap then a spec swap
      each cause exactly one rebind with no warning printed; the CDM turned off prints
      exactly one message, then silence — including across a spec change.
- [ ] M2 acceptance, frame: `/cap move` → drag → `/cap move` → `/reload` and confirm
      it stayed. Locked+empty must not eat mouse input. `/framestack` must report
      `IsProtected() = false` — if it doesn't, the non-secure argument needs revisiting.
      ⚠ The one `--@unverified` path: park it against a screen edge, change UI Scale,
      confirm it's still fully on screen.
- [ ] **STOP: ask** — the catalog's "not on the Demonology spec" silences (Demonic
      Strength, Bilescourge Bombers, Guillotine) rest on
      `knowledge/classes/warlock/demonology/abilities.md:89-91`, which still carries an
      open **`@verify-ingame`** marker. Two sources agree and the DB2 talent table backs
      it, but the marker is unresolved and the rule is that a marked claim you build on
      is a stop. Resolve it in game → edit the claim + drop the marker + `wowkb.gen_verify`.
- [ ] `hidden` vs `empty` CDM health may not discriminate — unsettled from source
      whether `GetItemFrames()` on a hidden viewer still returns children. Cosmetic;
      confirm or collapse the two verdicts.

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

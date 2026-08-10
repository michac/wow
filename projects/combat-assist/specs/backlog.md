# Combat Assist Plus — backlog

**What this file is for:** the list of work items. One line per item, newest
thinking at the top of its section. An item here is *agreed work not yet done* —
if it's speculative, it goes under **Ideas**; if it's done, it leaves this file
and the outcome is recorded in `notes.md`.

Keep items small enough to finish in a session. An item that needs a paragraph to
explain is a sign the answer belongs in `spec.md` first.

Items carry the `spec.md` section they implement. A milestone is done when all of
its items are.

**Naming: there is exactly one code, and it is the milestone.** `M0`…`M5` and their
lettered rungs (`M3a`…`M3e`) come from `spec.md`'s milestone table — they are an *ordered
ladder*, which is what earns them a code. **Everything else is a section named in plain
words** ("the rule cull", "the window migration"). ⚠ This is a rule because it already went
wrong once: work clusters were being labelled `M3-F` / `M3-W` / `M3-C` / `M3-R` / `M3-S`,
which look like siblings of `M3a` but are not ordered, not milestones, and whose letters
were private mnemonics nobody could decode a week later. Renamed 2026-08-07. If a new
cluster needs a name, describe it — don't mint a code.

## Now

⚠ **The order is `simplify → draw → add detail as play tells us to`.** The window
migration is **done** (2026-08-08; the record is in `## Reference` → *The window
migration*), so the code and `catalog.md` now speak the vocabulary `spec.md` §3.1/§3.5
describes, and what goes on screen next is the model we are keeping. The queue runs
**M3c/M3d/M3e** (something on screen), then the M3b leftovers, then the hidden-row
surface, then **the stale artifacts**, with M2's two loose decisions at the back.

⚠ **"Simplify" meant the code catching up, NOT another design round.** `spec.md` §3 is
**not** re-opened — the rule cull of 2026-08-08 was its simplification pass, and re-arguing
§3.1/§3.5 now would be the fifth re-run of the argument `discussion.md` already carries. The
detail that gets added from here comes from **playing**, not from authoring.

**The sections below are in queue order and `Now` holds only open work** — the done ladders
are in `## Reference`. Reasoning: `notes.md` 2026-08-08 (migration) and (the reorder); what
the cull changed: `notes.md` 2026-08-08; why drawing was moved up: `notes.md` 2026-08-07.

### The drawing rungs — M3c, M3d, M3e

**M3 — the tier signal. In progress.** Full plan and its reasoning: `notes.md`
(2026-08-06, M3 planning). The ladder is M3a…M3e, each rung flyable, and `--patch`
release + deploy is **pre-authorised for M3 flights** (nothing else).

⚠ **These rungs are unblocked** — the window migration landed, so what goes on screen is
the model we are keeping and the tuning done while playing survives. Detail gets added back
from what playing actually says.

- [x] ~~**M3c** — the graded register, on **cap's own overlay**~~ — **BUILT 2026-08-08.**
      Static only; nothing flown, no release cut. What it draws and what a flight should
      read: `## Reference` → *M3c*.
- [ ] **Fly M3c and M3d together — the first pixels.** **v0.2.3 is released and deployed**
      (2026-08-08); what is owed is the pull. `/reload`, a Demonology pull, then
      `wowkb.capture cap draw`. ⚠ **The only oracle for a pixel is an eyeball**
      — the `draw` stream exists so a flight that sees *nothing* can still tell a
      treatment bug from an anchoring bug (`anch:`/`conf:` vs the `P{}` cells). Read both
      before concluding anything. The acceptance table is in `## Reference` → *M3c*.
      A one-page card for running it, derived from that table:
      [the flight card](https://claude.ai/code/artifact/9dc3a713-5cbf-42e4-a7f7-8af576edfde7)
      — ⚠ a **view**, not a source; where it and the acceptance tables disagree, they win.
- [x] ~~**M3d** — the cues, drawn by the client~~ — **BUILT 2026-08-08.** Static only;
      nothing flown, no release cut. What it draws, and the sharp limit on what a flight
      can prove about it: `## Reference` → *M3d*.
- [ ] **Give the unmarked channel forms markers, driven by a catalog that wants one** — the
      table below is the current coverage. Nothing authors `auraRemaining(x) ≤ t` or
      `active(x)` today, so building their markers now would be inventing a visual language
      against no evidence; the trigger is a catalog entry that needs one.
- [ ] **M3e** — procs and the Demonbolt demotion. ⚠ The "honesty measurement" that used to
      close this rung is gone — deleted by the rule cull, 2026-08-08. The HIGH distribution
      is reported, not graded. What
      replaces it as M3e's acceptance is **playing with it** — the point of drawing early is
      that the next spec's rules get reverse-engineered from a thing that felt good, rather
      than authored in advance against no evidence.

**Which of `spec.md` §3.5's channel forms are actually drawn.** `Overlay.lua`'s `slotFor`
owns this and implements **two** of the six that table's `Draws` column promises. A form
with no marker is still **legal** — it loads, passes every check, and reports `nodraw` in
`C{}` — so an author reading only `spec.md` gets silence rather than an error. This is
milestone scoping, not a spec change; `spec.md` §3.5 points here for it.

| §3.5 form | `Draws` | Today |
| --- | --- | --- |
| `stacks(x) ≥ n` | count | ✅ **drawn**, on a **positive** cue — the `count` slot |
| `cooldownRemaining(x) ≤ t` | marker | ✅ **drawn**, on a **negative** cue — the `hold` slot |
| `auraRemaining(x) ≤ t` | marker | ❌ not yet. ⚠ **check 4 admits it as a negative cue's channel**, so it is the form a catalog author is likeliest to write and get nothing from |
| `cooldownRemaining(x)` · `auraRemaining(x)` | countdown | ❌ not yet — the bare forms are §3.4's bars, and the bar panel is a rung of its own |
| `active(x)` | pip | ❌ not yet |

⚠ **A slot is claimed by a (polarity, channel) pair, not by a channel alone.** A *positive*
`cooldownRemaining ≤ t` and a *negative* `stacks ≥ n` both read `nodraw` today even though
both channels sit in the drawn rows above — the renderer has a marker for each of the two
live pairings and for nothing else. Which marker a future pairing should get is open
(`discussion.md`, *how polarity is drawn*).

### The M3b leftovers — what the flight did not settle

- [ ] ⚠ **The `refused:` criterion was mis-specified and is not checkable.** 33 refused
      against 19 landed reads alarming and is almost certainly correct: the hook is on
      all 21 rows, 13 of which are silences, so refusals are the expected case. But
      **refused edges are counted and never logged with their cid**, so the instrument
      cannot tell "correctly ignoring silences" from "resolving the wrong cid" — which
      is the exact failure the criterion exists to catch. Log the cid on refusal, and
      restate the criterion as *every refused cid is a declared silence*.
- [ ] ⚠ **Three things the flight never exercised, and a criterion nobody exercised must
      not read as a pass.** (a) the **event-driven settle arm** — this was a login, so
      the generation never moved past its initial value and only the quiet arm can fire;
      it needs a real spec or hero swap. (b) the **dark-for-the-fight rule** — cap
      settled 19 s before the pull. Needs a `/reload` mid-combat or a swap immediately
      before one. (c) **`/cap aoe`** — `mode:single` on all 50 samples, never toggled.
### The hidden-row surface — rows that exist but are switched off, found 2026-08-07

⚠ **Relabelled.** These were filed as "coverage defects" and neither of the first two is
one. Coverage check 1 is measured against the rows cap actually **binds** (21 on this
build), and both of these are rows that are *not* bound — so check 1 is passing correctly
and what is missing is the reporting around it.

- [ ] **E4 Summon Doomguard drops at bind, and that is already recorded** — `catalog.md`
      O3 settled it on 2026-08-06: `1276672` appears in no row of the 21-row capture, so
      the entry is authored and dropped, which is the designed behaviour. It is not a
      coverage failure; E4 *has* an entry. What is owed is only that the drop be
      **visible** (the item below) — the "don't count it toward breadth" half of this is
      moot: check 2 was deleted on 2026-08-08.
- [ ] **Summon Vilefiend (cid 763, spell `1251781`) is not a tracked row on this build** —
      it is in DB2's `CooldownSetID 60` carrying `HideByDefault`, and it is not in the live
      bind, so it is not a row coverage check 1 can see. It therefore needs **no** silence
      today. ⚠ It would need one on a build that un-hides it, which is exactly the "in the
      data, not displayed" state below.
- [ ] **"Available, not displayed"** — implement `spec.md` §3.5's state. cap can enumerate
      the spec's candidate rows from game data; a row that exists but is switched off must
      be named in the capture log rather than dropped silently, **for a band's subject as
      well as a cue's**.
- [ ] **Enable cid 84224** (the `HideByDefault` Summon Demonic Tyrant bar) on the reference
      character and confirm it binds — an exact Tyrant-active duration, currently unused.
      ⚠ That it *can* be enabled is an inference off Blizzard's saved-layout path
      (`cooldown-manager.md` §1.2), not a measurement; this item is the measurement.

### The stale artifacts — re-derive the two published references

- [ ] **Re-derive both artifacts** — [Architecture](https://claude.ai/code/artifact/2de40ee9-5457-4ca3-b46e-77178e021207)
      and the [Demonology reference](https://claude.ai/code/artifact/46bb78b6-7c41-4210-a9b0-3b1707678569).
      They are linked from the project `CLAUDE.md`, which described them as **current at
      v0.2.1** — now false: both describe **windows**, the **six-window cap** and
      **stack-count-only cues**, none of which exist. `CLAUDE.md` carries a STALE warning
      in the meantime; replace it when they are re-derived. ⚠ Derive them by *running the
      code against the capture*, as the originals were — that is what found the `alt`
      defect. The window migration has landed, so this is unblocked.

### Loose decisions carried out of M2

Both were parked inside M2 rungs that are otherwise complete, and they are the only open
work M2 has left.

- [ ] ⚠ **M3 decision, deferred not dropped:** `spec.md` §3.5 still says cap "says so
      plainly once" when no catalog claims the spec — the same class of user-facing
      announcement just deferred out of `Bind.lua`. Either M3 gives it exactly one
      player-facing line at load for a state the player can fix, or it goes to the log and
      cap is silently inert. Don't let it ship by default.
- [ ] ⚠ **Deferred past M2d on purpose: no busted suite.** `Log.Render` is written pure so
      one *can* exist, but a suite written against a format the first flight is about to
      change is a change-detector. Revisit once the format has survived a flight.

## Next

*(M3's own items moved to `Now`. What follows is what M3 hands on.)*

### The claim-reliability revision — KB process, not cap code

**Plan: [`todo/kb-claim-reliability.md`](../../../todo/kb-claim-reliability.md). Execute it
in a fresh context; it is written to be self-contained.** Tracked here because cap is the
consumer that gets hurt — the Dreadstalkers line is a cap question, and cap's catalogs are
authored straight off `knowledge/addon-dev/`.

**The problem:** a negative result is recorded with a positive's evidence class, and every
follow-up is then framed by it, so the KB reinforces its own wrong answers instead of
testing them. cid `760` read "a summon binds no aura, so there is nothing to read" for days
— while the row was **totem-backed** the whole time and Blizzard's own source said so
(`GetCooldownValues` checks totems before auras). Two aura instruments came back empty; the
record could not distinguish *searched and absent* from *never examined*.

**The fix, in four parts:** split `[client]` (a value was observed) from
`[searched: <instruments>]` (we looked here and found nothing, and here is where we looked);
gate both that and the citation circle in `wowkb.kblint`; strip claim→`OBS-nnn`/`projects/**`
pointers so an observation cannot be cited as support for the claim that framed it; and make
a claim whose capture has rolled off say so. 64 negatives and ~334 pointers to triage, once.

⚠ **Not the sourcing ban** floated 2026-08-09 and rejected — wago/DB2, `UI.xsd`, blue posts
and the wiki stay admissible. An audit put the strict version at ~52% of the subtree.

**Done when** `kblint` is clean on the two new gates and a cold read of
`cooldown-manager.md` §7 can answer *"can I track a summon's duration?"* without a fresh
reader reaching "impossible" off a headline.

**Carried into M3's rungs, recorded here because they are easy to lose:**

- **The readiness latch leaks its hook.** `hooksecurefunc` cannot be removed and item
  frames are pooled (`Bind.lua:393` exists because of it), so re-hooking per rebind
  stacks N hooks on one frame and grows every spec swap. One weak-keyed `hooked[frame]`
  table, hook once per frame object ever, and resolve the cooldownID **inside** the
  callback via `self:GetCooldownID()`.
- **The GCD contaminates the out-of-combat baseline.** `GetSpellCooldown` reports it as
  a cooldown, so a baseline read in the 1.5 s after any cast records the whole roster as
  "on cooldown". Use `ignoreGCD = true`, or discard durations ≤ 1.5.
- **Readiness must be three-state.** A `/reload` mid-combat has no seeded baseline and
  both defaults are wrong — default-ready lights six entries for the whole pull,
  default-not-ready blanks them. `unknown` fails every band and its per-evaluation count
  goes to the log, or a flight cannot tell "the catalog is quiet" from "the latch never
  seeded". ⚠ **Now that negation is legal, "unknown fails the band" is a rule about the
  *band*, not about the term** — `not ready(X)` on an unknown `ready(X)` must also fail,
  never succeed by negating an absence. Get this wrong and a blind cap reads confident.
- **Rule 13 does not bite on Demonology** — nothing on the roster has charges — but the
  structural guard still goes in: seed `maxCharges` out of combat, refuse to latch >1.

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
- [ ] ⚠ **Sequence triggers are not checked at all.** `Catalog.Check` never inspects
      `cat.sequences`, so `spec.md` §3.5's *"a trigger naming a channel, or naming a term
      outside this set, does not load"* is unenforced. That matters more than it sounds:
      the trigger is the **one** place `casts` is legal, so it is exactly where new trigger
      vocabulary gets written — and today a trigger could name a channel, or a word in
      neither column, and load silently. Check it as a band-legal condition plus
      `casts == n` when the machinery lands. (Found in review, 2026-08-08.)

**Cross-cutting.**

- [ ] Decide the fate of the `assisted-combat-next-cast-varies` lab test now that
      §3.1 no longer consumes the oracle. It is already built and deployed, so it
      costs nothing further to let it answer — and a working oracle would make a
      useful *development-time* falsification check against our own tiers. Park it
      or keep it, but don't leave it undecided.
- [ ] ⚠ **`talent(x)` is in the spec's gate table and nothing answers it.**
      `Sense.buildReads` returns `affordable` / `proc` / `identity` / `resource` /
      `resourceMax` / `mode` and never `talent`, and `talent` is not in `Sense`'s
      `GATE_ORDER` either — so a band using it reads **unknown for the life of the build**
      and nothing tallies the refusal, which is the one shape of failure gate health exists
      to make visible. Nothing uses it today, which is why this is a backlog line and not a
      fix. **Either wire it or delete the gate from `spec.md` §3.5** — decide when something
      needs it, not before. (Found in review, 2026-08-08; `Catalog.GATES.talent` carries the
      same warning in code.)
- [ ] `/mine-addon` pass for prior art on graded emphasis under 12.0 restrictions.
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

⚠ The four `[code]` lines below are the dated record of M2's code as it stood on
2026-08-05 — written, parsed, reviewed against the KB, and not yet executed in the client.
**M2 has since been flown** (M2d, 2026-08-06; the reading is in `## Reference`), so "they
are not flown" no longer describes cap. ⚠ And `/cap status` was **removed again by M2b**,
so the fourth line describes a command that no longer exists. The four lines stay as the
dated record they are.

- [x] **The rule cull** — `spec.md` §1 gains the three principles; §3.1's third rule,
      §3.5's checks 2/3/8/9, §4's two justifications, §5's Legitimacy veto and §6's
      honesty question all cut back to them. `Catalog.lua` loses breadth, the floor
      finding and `HighCapable`, and its comments now cite `spec.md`'s new checks 1–5;
      three tests deleted (busted 95 → 92); `catalog.md` O7/O3/E10 lose the breadth and
      check-9 bookkeeping; all **three** `CLAUDE.md` pointers repointed — 2026-08-08
- [x] **The document defects** — F3 (E10's `identity` grammar), F4 (check 4 now really
      does refuse an un-thresholded negative cue), F5 (§3.1's two un-thresholded
      countdowns), **F6** (`cooldown-manager.md` §1.2's aura-alert cites, re-read against
      the Blizzard source and made *stronger*), F7 (E6's stale `@pending-test`), F8 (E2 vs
      §2), F9 ("known false after negation settles the band"), plus the unknown-cue-gate
      rule and §3.0's `Cue` glossary row. F1/F2/D5 were struck by the cull, not fixed
      — 2026-08-08
- [x] ~~**Is target count readable, and may cap branch on it?**~~ **Struck — answered by
      design, not by measurement.** AoE is a manual toggle (`/cap aoe`, macroable,
      persisted, shown on the panel); `mode(x)` is cap's own state and is always
      branchable. Every AoE opinion in a catalog is sayable without reading anything
      sealed — 2026-08-07.
- [x] ~~**What does cap show when the right answer has no icon?**~~ **Not a Demonology
      question after all** — Shadow Bolt `686` is an Essential CDM row (cid `34990` in
      cap's own capture), so the floor is drawable and is now catalog entry E10 at an
      unconditional LOW. The general question survives in `spec.md` §6 for a spec whose
      floor genuinely has no row — 2026-08-06.

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

## Reference — done, and the reasoning still binds

**The M2 ladder below is done.** It is kept because its reasoning still binds: the first
build put a lab inside the product, and chat has no copy/paste, so the one output that
had to reach the analysis machine was the one that could not leave the client (house
rule 4). The separation it established — **client behaviour is a ClientLab question;
cap's own state is a capture log** — is what M3a is built on.

**M3a and M3b sit under the same heading for the same reason:** the measurements they
made and the acceptance table's reading are what the open work in `Now` is argued
against, so they are kept as the record rather than deleted. **The window migration is
here because two of its decisions still bind** — the `t = 20` imprecision and what E5
lost — and because a reader meeting `catalog.md`'s O1 or O8 needs to know they were
chosen rather than overlooked.

### M3d — ✅ BUILT 2026-08-08. Static only; nothing flown, no release cut.

**The half cap is not allowed to compute.** cap offers a cue, the client decides whether it
appears, and cap never learns the answer — `spec.md` §1 principle (a) as running code
rather than as a design claim. Both mechanisms are `knowledge/addon-dev/`'s, unchanged:
the three-way quantiser (`security-taint-and-restricted-data.md` §4.8.2) and a Step curve
thresholding a secret duration (§4.8.1 finding 4). Reasoning: `notes.md` 2026-08-08 (M3d).

- [x] **`Channel.lua`** — new, impure, and the only place either mechanism lives.
      `Channel.StackText(auraSpellID, min)` and `Channel.Threshold(spellID, t, on)`. Every
      read `pcall`-guarded and class-checked; **could-not-arm returns nil and nil draws
      nothing**. ⚠ `type(r) == "number"` is refused as a guard on the Step result — it is
      *supposed* to be secret, and that guard rejects exactly the in-combat case.
- [x] **The two-viewer tie-break, written down:** one aura can sit on a bar *and* an icon
      (Demonic Core does), so the read picks the **lowest cooldownID among the `auras`
      rows**. It is a read-side rule only — the *draw* is on the entry that owns the cue,
      never on the aura's row, so the flip-flop cannot reach a pixel.
      ⚠ **The family filter is part of the rule, not an optimisation.** Check 3's aura set
      holds every entry's own spell id, so `stacks(<a castable ability>) ≥ n` is legal — and
      on a spec whose buff is also a press, the `spells` row can hold the lower cooldownID
      while carrying no bound aura at all. Unfiltered, that cue reads `refused` for the life
      of the build, deterministically, so it never even looks flaky.
- [x] **`Treatment.Ink`** — the one field the renderer lacked: a tier's ring or the hold
      slate, and **nil for a veil-only tier**, which is what makes an un-inkable positive
      cue a refusal rather than an invented colour. 3 tests, both mutations caught.
- [x] **`Overlay.lua`** — two marker slots per row, claimed in sorted entry order. Setup is
      keyed on the **offer**; the channel write runs every pass, because a count and a
      countdown both move and cap cannot dedup on an answer it may not read.
- [x] **The `draw` stream gains `C{}`** plus `cue:`/`arm:` in `D{}`.
- [x] **busted 138 → 141, luacheck 0/0 in 20 files.**

**What the `draw` line says now.**
`D{n: rows: anch: conf: off: nf: cue: arm:} P{…} C{E8:+stacks:armed E2:-cooldownRemaining:refused}`

| `C{}` state | Means |
| --- | --- |
| `armed` | cap resolved the inputs and handed the client the comparison. **Not** "it appeared" |
| `refused` | cap tried and could not — no live `auraInstanceID`, no duration, no curve, no ink |
| `nodraw` | the cue's shape has no marker in the vocabulary; cap never asked the client |
| `taken` | a second cue wanted a slot another entry already holds on that row |

⚠ **`arm:` is the only number this rung adds that means anything, and it means less than it
looks.** `arm: = cue:` says the mechanism is wired end to end; `arm:` short of `cue:` with
`C{}` naming `refused` says cap could not reach the client. **Neither says a pixel moved.**

⚠ **E8's cue will flap `armed` ↔ `refused` through a pull, and that is the PASS case.** Its
`auraInstanceID` comes off the Wild Imp row, which binds no aura when no imps are out — so
`refused` there is *"there are no imps"*, which is the same thing the quantiser would have
drawn (nothing) had it been asked. A cue that reads `refused` for a whole pull with imps
visibly out is the failure.

### M3c — ✅ BUILT 2026-08-08. Static only; nothing flown, no release cut.

**Every CDM icon cap has an opinion about now gets an emphasis drawn by cap, on cap's own
frames, recomputed on Sense's clock.** The visual vocabulary it settles is in `spec.md`
§3.1 → *What a treatment looks like*, which is the normative copy — the numbers live once,
in `Treatment.lua`, and are transcribed there. Reasoning: `notes.md` 2026-08-08 (M3c).

- [x] **`Treatment.lua`** — pure. Tier → look, the grade band, the hold treatment,
      `Brightness` (the one scalar the ladder is ordered by). 25 tests.
- [x] **`Overlay.lua`** — impure. One frame per bound row, pooled by `cooldownID`,
      parented to `UIParent`, **anchored** to the item frame and never parented to it.
- [x] **`Sense.OnVerdicts`** — the surface rides cap's one clock. Fires on the early
      return too, so a spec swap into a catalog-less build puts the lights out.
- [x] **The `draw` stream** — `wowkb.capture cap draw`, no Python change needed.

**What a flight has to separate, and how.** The `draw` line is
`D{n: rows: anch: conf: off: nf:} P{E1:HIGH/a91t3* E7:LOW/v31* …}`. Combat start and end
are `#`-marked on this stream carrying the full body, so a pull whose drawn set never
changes still emits its numbers at both edges; `:Meta` carries the catalog, cap's version
and the line count.

| Reading | Means |
| --- | --- |
| `P{}` cells move, screen blank | **anchoring** — check `anch:`/`conf:` and the `!`/`?` suffixes |
| `anch:` = `rows:`, `conf:` = `rows:`, screen blank | **treatment** — the paint ran on a real frame and produced nothing visible |
| `anch:` = `rows:`, an overlay visibly **on the wrong icon** after a repool | ⚠ **not a treatment bug** — the §1.1 secret-anchor gap. `anchor()` calls `SetPoint` mid-pull when the item-frame pool hands a cooldownID a new frame, and a CDM item frame in combat carries a *secret* anchor; whether a dependent of one still moves is **unmeasured**. A silent no-op leaves the overlay on its previous position while `Bind.ItemFrame` succeeded, so every number in `D{}` reads healthy |
| cells carry `!` | `Bind.ItemFrame` refused; a rebind is already scheduled |
| cells carry `?` | anchored to an **unconfirmed** frame — drawn anyway, possibly on the wrong row |
| a cell has no `*` | that entry LOST its row to a brighter sibling — its treatment is on no icon |
| `off:` > 0 | the item frame is not visible; the overlay is correctly hidden |
| `nf:` > 0 | ⚠ **no item frame at all** — anchoring failed. `nf:` = `rows:` is a total failure, not a quiet overlay |
| no `draw` lines at all | the paint path never ran — check `tier` for a `# listener-error` mark |

⚠ **What must not read as a pass.** The **`# listener-error`** mark on `tier` means a
listener threw and was reported once; the `draw` stream after it is not evidence of
anything. Cues are M3d's and are read out of `C{}`, not out of `P{}` — a `P{}` cell says
nothing at all about whether a marker was drawn on that icon. And the wrong-icon row above
is the one failure **no number in the log can show**: the gap is
`knowledge/addon-dev/security-taint-and-restricted-data.md` §1.1 (registry
`secret-anchor-dependent-geometry`), and only an eyeball on a repool can catch it.

⚠ **One thing for the eyeball, not the log:** the *none* veil sits at **0.62 alpha over
the CDM's own cooldown swipe and number**, which is the only timer the player has until
§3.4's bars ship. Judge on screen whether an un-opinionated icon is still readable as a
timer; if it isn't, the number to move is `NONE` in `Treatment.lua` (and `spec.md` §3.1's
transcription of it).

**Not a hazard, and the reason is worth keeping.** An overlay cannot first be created
mid-pull: `Bind.resolve` early-returns in combat so the bound set never changes, and a
settle happens out of combat only (`trySettle` returns in combat, and a `/reload` mid-pull
never has `snapshot.complete`), so every frame in the pool was created and layered before
the pull. `SetFrameStrata` is protected and unmeasured in combat; the out-of-combat guard
on it is belt-and-braces rather than the thing holding the guarantee.

### The window migration — ✅ DONE 2026-08-08. Static only; nothing flown, no release cut.

**The code caught up to `spec.md` §3.1/§3.5.** It added no capability — every fact the
window-era catalog knew, the migrated one knows — and what it bought is that the thing
M3c/M3d put on screen is the model we are keeping. The four shape decisions and their
reasoning: `notes.md` 2026-08-08 (the window migration). Kept here because two of them
still bind.

- [x] **`catalog.md` §2 deleted** and the document renumbered (§1 roster · §2 entries ·
      §3 silence · §4 bars · §5 sequences · §6 open questions). O-numbers are unchanged;
      O2 is struck as moot and O8 is new.
- [x] **`dogs_out` → a band, not a cue.** E1 band 1 is `ready(this) and not ready(E2)`,
      plus a negative cue at `cooldownRemaining(E2) ≤ 8`. The band reads long (20 s
      cooldown against a ~12 s pet lifetime); the cue trims exactly the tail. Both halves
      are **exact**, which is what deleting an `elapsed` estimate is worth.
- [x] **`tyrant_setup` / `tyrant_far` → E2 keeps ONE HIGH band, plus a hold cue.**
      `ready(this) and affordable(this)` → HIGH; negative cue, precondition adds
      `not ready(E1)`, channel `cooldownRemaining(E1) ≤ 20`. E3/E4 band 1 became
      `ready(E1)` verbatim. ⚠ **`not ready(E1)` in the precondition is load-bearing** — a
      ready Tyrant reads zero remaining, which clears any `≤ t` and would pin the marker on.
- [x] ⚠ **`t = 20` is imprecise and is filed, not hidden** — `catalog.md` **O8**. The real
      hold zone is `12 < remaining < 20`; the channel table offers one upper threshold.
- [x] **`tyrant_active` → E5 band 2 DELETED, applies-to NOT narrowed.** Adding the apex
      talent to applies-to would make cap draw *nothing at all* on a build without it,
      which is far worse than E5 losing a band. On an un-apexed build band 1 simply never
      holds. ⚠ **What it cost is recorded in O1:** "spend the Tyrant window on Hand of
      Gul'dan" is unexpressible until cid `84224` is enabled and yields a duration.
- [x] **`cores_dry` → E9 band 1 is `ready(this) and not proc(E7)`**, and `opener` deleted —
      `catalog.md` §5's two triggers are rewritten in the §3.5 sequence-trigger form
      (`ready(E1)`; `combat and casts == 0`).
- [x] **`Catalog.lua`** — window vocabulary, `remaining`, `MAX_WINDOWS` and the
      window-count shape check gone. Subjects legal on every gate term except `elapsed`
      (`this` only, refused in both `Check` and `Tier`); `combat` moved into the gate set;
      `casts` refused in a band and named as sequence-trigger vocabulary; negation legal;
      `e.cue` → `e.cues = {…}` with polarity, tier and a channel term. The checks are the
      five, and **check 3 (declared subjects) is new** — with the `talent` / subject-less /
      `mode`-literal exemptions. **Check 5 is a second return value**, because it cannot fail.
- [x] **`Catalog.Reads` keys `byEntry` by SUBJECT**, and `Track`'s health tally with it —
      `not ready(E2)` inside E1's band is a read of E2, and tallying it against E1 reports
      a working catalog as blind.
- [x] **`Catalog.Resolve`'s `alt` defect fixed** — `match()` tries `alt` after `spell`, so
      a Fel Ravager build binds E3 instead of dropping it silently. Test added; it was
      found by reading, not by a test, and no case covered a build cap has never run on.
- [x] **`Track.lua`** — `windowTerms`, `windowHolds`, `remaining`, `SeedCooldown`, the `cd`
      field and `health.windows` gone; `Track.New()` no longer takes the catalog. The
      readiness latch, three-state, `castAt`/`elapsed`, the charge guard and the `casts`
      counter (unread until M5) all stay.
- [x] **`Sense.lua`** — mechanical only: `win:` out of `Render`, `hold:` in, `e.cues`
      adapted, `winKnown`/`winUnknown` off the `Row`. Not restructured; the drawing work
      lands on it next.
- [x] **busted 92 → 104, luacheck 0/0.** New cases: a band naming another entry, negation
      in a band, `not <unknown>` staying unknown, check 3 catching an undeclared subject,
      check 4 refusing an un-thresholded negative cue, `casts` refused in a band, `elapsed`
      refused on a non-`this` subject, and `Resolve` binding E3 through `alt`.

### M3a — ✅ DONE 2026-08-07. Lab flown and drained, pure core built and green.

- [x] **`duration-predicate-secret-in-combat`** → **secret booleans**, all four. The
      readiness latch stands. First boolean secret this workspace has obtained.
- [x] **`cdm-identity-readable-in-combat`** → `info.overrideSpellID` **plain on 21/21
      rows in combat**. E6 Ruination is saved.
- [x] ~~`cdm-summon-row-auradataunit`~~ **DELETED — a malformed question.** A summon
      binds no aura. Replaced by the `dogs_out` window.
- [x] `Catalog.lua` — vocabulary, registry, `Check` (load-time 2–6) + `CheckBound`
      (coverage **and breadth re-run** on the post-drop set — the breadth re-run it
      carried was deleted on 2026-08-08 with check 2; coverage stands).
- [x] `Catalogs/Demonology.lua` — 10 entries, 6 windows, 14 silences.
- [x] `Tier.lua` — first-match bands, three-state gates, **keyed by entry**.
- [x] The busted harness — 44 tests, mutation-checked, plus the 21-row capture as a
      client-authored fixture. The refused-read meta-test has already refused a new
      vocabulary term twice.
- [x] **`Track.lua`** — an **edge listener**, not a poller: `Available`/`OnCooldown` give
      readiness, `OnAuraApplied`/`OnAuraRemoved` give aura presence. Three-state
      throughout, `elapsed`/`remaining` arithmetic, the six windows evaluated, and a
      **gate-health tally** beside the world it returns. Seven mutations caught.
- [x] **The window rule form**, which the catalog declared by name only and no code could
      read. `spec.md` §3.5 gains a window vocabulary — the gate terms plus `remaining`,
      `combat` and `casts`, with negation legal here and nowhere else — and
      `catalog.md` §2 gains the transcribed rule per window. Five mutations caught.
- [x] **`Catalog.Reads`** — which gate is asked of which entry. It tells Sense what to
      read and, more importantly, tells the health tally which gates an entry was ever
      meant to answer: counting a gate nobody asks for reports a working catalog as blind.
- [x] **`/cap aoe`** (`Mode.lua`) — toggle plus explicit `on`/`off` so a macro is
      deterministic, persisted, and the live mode drawn on the panel. Registered from its
      own module through `ns.RegisterCommand`; `Core.lua` untouched.
- [x] Both answered lab cells drained, **their tests deleted in the same edit**, and
      §4.2 row 8 flipped off `blocked` — `LuaDurationObject:HasExpired` is the
      boolean-secret source it always lacked, and `secretDuration()` was promoted out of
      the dying test rather than deleted with it.

### M3b — ✅ FLOWN 2026-08-07

- [x] **M3b code** — `Sense.lua`: the alert hooks (weak-keyed, once per frame object ever,
      cooldownID resolved *inside* the callback), the out-of-combat baseline with the GCD
      floor, the four client reads, both streams (`tier`, `edge`), the two-armed settle,
      the dark-for-the-fight rule, and the health marks. Nothing drawn.
- [x] **M3b flight — FLOWN 2026-08-07, v0.2.1.** 76 s dummy pull, Demonology/Diabolist,
      53 tier lines + 58 edge lines. **6 criteria PASS, 3 never exercised, 1 criterion
      was itself wrong.** Full reading in `notes.md`; the short version:
      `hooks:21` (every row), both alert edges landed, `ready` and every client read
      `n/n` in combat, windows `4/6 → 6/6`, `# dropped` exactly E4 + E9, and **E6
      Ruination fired** — the in-combat identity read works end to end, so the entry
      that was dead code before M3a is live.

**The acceptance table, written before the flight and now carrying its result.**

| Read | Passes when | Measured 2026-08-07 |
| --- | --- | --- |
| `edge` stream, `hooks:` | > 0, matching the bound row set | ✅ **21** — every CDM row hooked once |
| `edge` stream, `Available` / `OnCooldown` | both appear in a pull | ✅ 9 and 8, on E1/E2/E3/E8 — the cooldown entries, and only those |
| `edge` stream, `refused:` | small | ⚠ **33 vs 19 landed — criterion not checkable**, see above |
| `G{ready:…}` | reaches `n/n` in a pull | ✅ **4/4** from the first sample, never regressed |
| `G{affordable} {proc} {identity} {resource}` | each `n/n` **in combat** | ✅ 2/2 · 1/1 · 1/1 · 1/1 — **no read refused once, all pull** |
| ~~`G{win:…}`~~ | ~~`6/6` once underway~~ | **VOID** — windows no longer exist. What replaces it is the HIGH-at-once distribution below, **reported, never pass/fail** |
| `# settle by:` | fires once, naming the arm | ⚠ **`by:quiet`** — correct for a login; the event arm is untested |
| `# combat start` while unsettled | `S{… DARK}` | ⚠ **never exercised** — settled 19 s before the pull |
| `S{mode:…}` | follows `/cap aoe` | ⚠ **never exercised** — `mode:single` throughout |
| `# dropped` marks | E4 and E9, nothing else | ✅ exactly those two |

**And the thing no criterion asked for: E6 Ruination fired.** `E6:HIGH/1`, six samples.
The in-combat `overrideSpellID` read works end to end, so the entry that would have
passed every unit test and never lit once is live. E5 hit **all four** of its bands
(apex buff, `tyrant_active`, 5 shards, plain affordable) and `dogs_out` promoted Tyrant
to HIGH within 2 s of the Dreadstalkers cast — the catalog's centrepiece, working.

**The HIGH distribution, for the record:** 50 in-combat samples, **0 HIGH on 54 %, exactly
one on 30 %, two or more on 16 %**. ⚠ **This is a statistic, not a verdict** — the rule cull deletes
the rule that read "usually exactly one HIGH" as a failure. It is worth re-reading once
something is drawn, because it is the instrument for explaining *why* a moment felt wrong;
it is not a bar to clear. Caveat it carried and still deserves: 76 s of mostly steady state,
one Tyrant window, and neither the Implosion cue nor the proc demotion existed.

### The two inputs the M2d flight handed M3

**The M2d flight handed M3 two inputs, and both are now decided:**

- **cap's passive health channel → assume healthy, log problems.** No `CVAR_UPDATE`
  work, no user-facing warning; the verdict rides every `tier` line and a `# health`
  mark fires on any change of `kind`. §3.5's "says so plainly once" is now **log-only**
  and `spec.md` is edited to say so — the deferred M2b item is closed, decided rather
  than defaulted. ⚠ Written down honestly: that mark covers spec-swap transitions and
  **not** the Options-toggle case, which raises none of the nine events. Building it is
  fine; believing it covers the disable case is not.
- **The hero-tree swap → an event-driven settle, not a timer.** On a label change cap
  goes unsettled and paints nothing; it commits on the first **complete, out-of-combat**
  resolve whose reason is `SPELLS_CHANGED` *and* whose generation moved. ⚠ A quiet-timer
  settle commits at exactly the wrong moment — in the first seconds the generation is
  quiet **because the rebuild has not started**, which is the state the settle exists to
  survive. One quiet-window fallback remains for the identical-row-set case, and **both
  arms are logged** so a flight says which fires. Unsettled + combat entry ⇒ dark for
  the fight.

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

### M2b — Strip cap's diagnostic surface ✅ DONE 2026-08-06

Static-only: nothing here was flyable, and no release was cut. Session log + the three
decisions: `notes.md`.

- [x] The `ns.RegisterStatus` reporters are gone from `Bind.lua` and `Frame.lua`, with the
      helpers that existed only to render them (`specLabel`, `breakdown`, `ago`). The read
      API (`ns.Bind.*`, `ns.Frame.*`) survives untouched — M3's input, not a diagnostic.
- [x] **`/cap status` goes entirely** — the command, `cmdStatus`, the `ns.RegisterStatus`
      registry and both reporters. Bare `/cap` is now help. `spec.md` §2's "checking
      status" affordance is dropped, and §3.5's four references now name the capture log.
- [x] **The chat-announcement mechanism goes with it** — `MESSAGES`, `announce()`, the
      3-per-session cap, the login-grace arming, `state.armed`. User-facing warnings are out
      of scope for the first pass; developer output is M2c's log. ⚠ The health **verdict
      survives as internal state** — M2c logs it, M2d judges it.
- [x] `/cap move` stays — a placement affordance required by §3.4, not a diagnostic.
- [x] **`Bind.lua`'s stale-retention branch deleted**, with `row.stale` and its readers.
      ⚠ **This item was wrong about the counters.** `state.unreadable` / `state.complete` do
      **not** only feed that branch — `complete = false` is set independently, and the
      counters' only reader was the status text. Both are **kept**, deliberately
      written-but-unread until M2c logs them. The class-check on read (`readField`) stays.
- [x] **The `hidden` verdict is fixed, not collapsed** — it now reads the **viewer's** own
      `IsShown()` through `readField`, stored as `state.viewersShown` and carried into the
      health table. ⚠ Not the item frame's, which is constant-true when hide-when-inactive
      is off. Row count now means *configured*.
- [x] **`Frame.lua`'s `--@unverified` comment trimmed.** The engine re-clamps continuously
      and inline, so the re-`SetPoint` on `UI_SCALE_CHANGED` / `DISPLAY_SIZE_CHANGED`
      re-asserts the *saved* position and is not what keeps the panel on screen. Call kept,
      reason corrected.
- ⚠ **Not fully closed:** this rung's one deferred item now lives in `Now` → *Loose
      decisions carried out of M2*.

### M2c — Give cap the standard capture log ✅ DONE 2026-08-06

Static-only: no release cut, nothing flown. Stream is `bind`, read with
`wowkb.capture cap bind`. Session log + the scope decision: `notes.md`.

- [x] `Capture.lua` — **vendored byte-identical** from CDMProbe below the header (the
      three copies now diff clean, which is what the standard exists to preserve).
      `ns.Capture.Open("bind", { sessions = 8, cap = 2000, dedup = false })`.
      ⚠ `dedup = false` is deliberate: `Stream:Mark` neither reads nor writes the
      stream's own `last`, so `Line(x) → Mark(edge) → Line(x)` swallows the second line.
      cap owns the dedup so a Mark can move the baseline.
- [x] **`cap` registered in `wowkb.capture`'s `ADDONS` map** — plus the five stale
      enumerations of the addon set in `capture-and-dump-standard.md` and the workspace
      `CLAUDE.md`. `wowkb.capture cap --list` resolves, which proves the reader path
      **before** the flight rather than after it.
- [x] `Log.lua` emits the binding state on every evaluation. `Log.Render(snapshot)` is
      **pure and IS the dedup key**; `why`/`d`/`age` sit outside it, because a monotonic
      field inside the key makes every line unique and floods the ring. Fields group by
      *freshness*: `B{}` last resolve · `H{}` verdict · `C{}` spec + hero.
- [x] ⚠ **Both combat marks carry the FULL body** — a bare marker against an unchanged
      state emits no numbers, and unchanged is the PASS case. Combat comes from the
      **event name**, never `InCombatLockdown()`. No `# config` mark: spec and hero ride
      inside the dedup key, so a swap always moves the body.
- [x] **`Bind.RowDigest()` → one `:Row` per bound ability** (`rec=bind`: cooldownID, viewer,
      slot, primary/base/override/tooltip/live, isKnown, pool), emitted when the
      **generation** changes so a resolve that moved nothing does not repeat the set. The
      summary line says *how many* rows; without this nothing says *which*, so the binding
      could be verified populous but never **correct** — and identity is what M3's catalog
      keys on. ⚠ Added because lines are pre-rendered: wanting it after the flight is a
      re-fly. The summary row is now `rec=state`, so the two are greppable apart.
- [x] ⚠ `Capture.Safe()` is **necessary but not sufficient** for a space-delimited line —
      it leaves internal whitespace ("Beast Mastery") and braces, which split a field or
      forge a group boundary. A local `token()` sits over it, and every value goes in as
      one pre-built string with no varargs.
- [x] **Plumbing the log could not work without:** `ns.version` + `ns.db` (a stream drops
      every write silently while `ns.db` is unset — a whole flight would read back
      `(no captures)`), `ns.db` assigned **before** `applyDefaults`, `Frame.lua` no longer
      owning the root table, and the `.toc` order `Core · Capture · Bind · Log · Frame`.
- [x] **`.luacheckrc` at the addon repo root** — this makes the linter a **live release
      gate** (`wowkb.addon release cap` aborts the cut on a hit; its absence is what
      silently switched the gate off). Green across all five files.
- [x] **Corrections M2c had to make, neither of them planned** — see `notes.md`:
      `health.kind` was **nil on the healthy path**, so the first healthy sample would
      have thrown inside an event handler; and a clean pull produced **no resolve at
      either combat edge**, so `PLAYER_REGEN_ENABLED` now schedules unconditionally.
      ⚠ The second is a **behaviour change**, and it is what makes M2d's row-count
      criterion a measurement instead of a tautology.
- [x] **Scope cut, deliberate:** cap's health verdict is not provable — an Edit Mode hide
      moves no row and fires no event cap registers, so `hidden` is effectively
      unreachable. Not fixed: if the CDM is off, cap does nothing, which is correct and
      does not need proving. Also cut: the heartbeat ticker, a viewers-unreadable
      counter, refusing `hidden` on an unreadable read, splitting `empty` into
      `empty`/`no-rows`, evaluate-time visibility sampling, per-cause `unreadable`
      counters, a CDM-data-loaded flag.
- ⚠ **Not fully closed:** this rung's one deferred item now lives in `Now` → *Loose
      decisions carried out of M2*.

### M2d — Fly cap and read the log ✅ DONE 2026-08-06

v0.2.0 released + deployed, one pass flown. **M2 is done.** 4 sessions, 224 entries,
accounting exact and nothing trimmed. Full record: `notes.md`.

- [x] **The binding is CORRECT, not merely populous** — 200 identity rows, 3 specs,
      2 classes, and five display overrides resolved right (Shadow Bolt→Incinerate,
      Immolate→Wither, Templar's Verdict→Final Verdict, Crusader Strike→Crusading
      Strikes, Avenging Wrath→462048). Right on **Retribution Paladin**, a class cap was
      never designed against — the project's first non-Warlock evidence.
- [x] Row set **byte-identical across a 183 s pull**; generation moved **exactly once**
      per real change (1→5 for four changes); `d:0` throughout.
- [x] **No `PARTIAL`, `u:0` on all 12 samples.** The "a PARTIAL out of combat is a KB
      finding" trapdoor never opened — the reads are clean on every spec.
- [x] Frame position survived the reload (`0,-160,false` → `-927,-158,true`); locked and
      empty, it ate no mouse input.
- [x] **`--@unverified` discharged** — the Paladin logged `hero:-`, a genuine nil through
      `pcall`. Marker out of `Log.lua`, confirmation added at `kb-inbox.md:140`.
- [x] **Four facts drained to `knowledge/addon-dev/cooldown-manager.md`**:
      `overrideSpellID` is **always populated** (200/200 — `~= nil` never means
      "overridden"; rung 5 of `GetSpellID()` is unreachable), the category set is a
      **superset**, `TRAIT_CONFIG_UPDATED` **precedes** the CDM rebuild by ~5 s, and
      disabling the CDM in Options **fires none of the nine** CDM/talent events.
- [x] ⚠ **`n:` against `set:` was a WRONG criterion** and is struck. They never agree
      (26/45, 25/42, 21/44, 25/38) — the category set is the spec's full candidate set
      even with `allowUnlearned = false`. The real invariant is `rows ≤ set`.
- [x] ⚠ **The `hidden` cut was right in outcome, wrong in mechanism.** M2c called it
      unreachable; the flight (Options checkbox, not Edit Mode) shows the verdict was
      **fully computable** and simply **never sampled** — 5.7 minutes, off and back on,
      zero samples. **A sampling failure, not a detection failure**, which changes the
      fix: cap's health channel is passive and no better verdict helps without a trigger.

# Cooldown HUD — milestones & status

> Roadmap, milestone log, and the "confirm while logged in" queue.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> §0.5 Guidance model → `guidance-model.md` · §1–§2, §4–§5, §9 → `notes.md` ·
> §6 Milestones + §7 Open questions → **this doc** · superseded work →
> `notes-archive.md`.

## Status

**Current: M3c-c2 CODE SHIPPED — the sequence queue + the opener (2026-07-21,
CDMProbe v0.17.0). In-game pass §7.7 outstanding; it is board-independent, so it
can be run before the strictness session, but everything else still waits on
§7.6 → §7.3 → §7.4 → §7.5.**

The milestone the "split, share the widget" decision produced. M3c-c2's opener and
M4's burst-window queue are the **same shape** — a mode-scoped fixed sequence,
shown, advanced by cast-match, dissolved — so rather than build the opener bespoke
and bend it into M4, the reusable **`HudQueue`** widget ships now wired to **one**
consumer (the opener). M4's burn queue becomes its second consumer as *data + a
trigger*, not new machinery — the same seam `SpecDemonology` is for a second spec.

**Scope: one opener.** `ns.SpecOpener` was lifted from — and re-verified
against — the live #1 Demo parse (Inphected, WCL bracket **291**, newer than the
KB's data): `Dreadstalkers → Imp Lord → Tyrant @ t≈3.4s → HoG HoG → Implosion →
SB×3`, matching `diabolist-sequences.md` SEQUENCE 1a. *(There is deliberately no
alternate/variant machinery — the old "1a vs 1b" split, and its 1b-only fill-to
marker, was speculative and is scrubbed. If the opener ever needs revising, we
revise this one table.)*

⚠ **The opener is the only instructional widget in the project** and §0.5.8.7 §0
put it on notice, so it ships **default OFF** (`/cdmp hud opener on` to enable) and
renders as a **draining ghost** of the sequence (a **left-to-right strip of
keybinds, above the panel**) — it informs the *shape* of the opening, it never
says "press this now".

*(Prior line:)* **M3e CODE SHIPPED — the pull recorder (2026-07-21, CDMProbe v0.16.0).
Run §7.6 first, then §7.3 → §7.4 → §7.5 *with the recorder on*. That is the
whole point of this build.**

**Four in-game passes are queued and three of them have been queued for three
builds.** M3e is the admission that this is a **tooling gap, not a scheduling
accident**: §7.3 item 6 — *"`lit now` names 1–2 abilities, and if it sits at 4+
tighten the RULES, not a colour"* — is the exit criterion §7.4 and §7.5 both
inherit, and `lit now` was **a snapshot you had to type mid-pull**. Strictness is
a property of the moments you were *busiest*, which are exactly the moments you
were not typing. So the HUD now **records every pull without being asked** — a
histogram of the lit count, the peak set with its reasons, and a timestamped
transition log — and writes it to `CDMProbeDB.pulls`. §7.6 is *self-verifying*:
it succeeds when it produces the evidence the other three passes have been
waiting on.

⚠ **M3e deliberately does NOT tune `HudScore`.** If the histogram comes back with
a fat 4+ tail, tightening the rules is the **next** milestone's work, on evidence.
Measuring and acting in one session means tuning against a number invented by the
same session.

*(Prior line:)* **M3c-c1 CODE SHIPPED — the shard rail + mode spine (2026-07-21,
CDMProbe v0.15.0). Three in-game passes are now queued, and they run in order:
§7.3 → §7.4 → §7.5.**

**M3c-c is split.** **M3c-c1** (this build) is the *ambient resource layer*: the
owned **shard rail**, the **GENERATE↔SPEND↔PREP mode spine**, and the mode
chrome on the rail + the DEMO.SYS terminal. **M3c-c2** is the **pre-pull opener
queue** and is *not* in this build. The split is deliberate: the opener is the
only **instructional** widget in the whole project ("press this next"), it needs
a new `ns.SpecOpener` table and a real pull to verify, and §0.5.8.7 §0 put it
explicitly *on notice*. Bundling it with an always-on ambient widget is how one
in-game pass ends up measuring two things and settling neither — the M3c-b + M3d
double-up already showed that cost.

⚠ **§7.3 and §7.4 are prerequisites, not suggestions.** Everything in M3c-c
renders *on top of* the scored board, so shipping it over an unverified board
**decorates a board that lies**. M3d's seeding is also what makes the rail
honest at a cold start. Do not run §7.5 first.

Two decisions taken this build, both against a real conflict in the docs, and
both written up in **`guidance-model.md` §0.5.8.8**: mode lands on the **rail +
terminal chrome only, never on an icon** (the icon channel budget is full —
§0.5.8.7 §1), and the **cap earcon stays in M6** (three committed statements
against one). The cap glitter also ships **throttled** — the M1 prototype's
`fireGlitter` re-fires within a couple of GCDs at cap, which [X2] forbids.

*(Prior line:)* **M3c-b + M3d CODE SHIPPED — one combined in-game pass is
outstanding and IS the milestone (2026-07-21, CDMProbe v0.14.0).**

**M3d — out-of-combat seeding** rides on top of M3c-b in a single **v0.14.0**
release (v0.13.0 was committed but never cut). The cold start is gone: readiness
and the countdown are now **seeded from the client's own numbers** at bind time
and on leaving combat, so a `/reload` mid-cooldown shows `~42.1s (read)` instead
of `NEVER · no edge seen yet`. This is **reading, not guessing** — the M3b
doctrine stands unchanged *inside* combat, where reads go secret and the board
falls back to edges. Two milestones in one release is deliberate; the mitigation
is per-item **seed-vs-edge provenance** in `hud status`. Run **§7.3 first, then
§7.4** — see §7.4's preamble for why the order matters.

M3c-b's exit criterion is a **measurement, not a diff**: a dummy pass where every
lit dot survives being argued with — `lit now` names **1–2** abilities and each
stated reason is one you agree with. **That number is still unmeasured**, and it
was unmeasurable before this build because one of the two lit dots was the
phantom Grimoire. Run **§7.3** before treating anything below as confirmed, and
in particular before starting M3c-c, which renders on top of this board.

*(Prior line:)* **M3c-a shipped; feedback pass + instrumentation pass done. NEXT
IS M3c-b, THE TRUTH PASS (2026-07-21, CDMProbe v0.12.0).**

**The v0.12.0 probe run answered four open questions in one dummy session** — the
argument for consolidating six toggled probes into one always-recording command
paid for itself immediately (§7.2 item 16). Headlines, all written up in
`notes.md` §1:

- ✅ **M3d is GO.** Cooldown state is **13/13 readable out of combat, 0/13 in
  combat**. Open-world both runs, so the gate is **combat**, not instancing.
  *(One residual: every OOC read was `duration=0`. Fields readable ≠ mid-cooldown
  value correct — confirm before coding.)*
- ✅ **V1(c) closed.** Demonic Art **observed for the first time**, 12 override
  events. Ruination = `434635`, Infernal Bolt = `434506`, both ambiguities
  resolved. Shadow Bolt's half of the wheel fires an event **even though SB isn't
  tracked** — §0.5.5's blind spot is now about *where to draw*, not what we know.
- 🐛 **The Grimoire complaint is real and reproduced.** `1276467 → 388215 Devour
  Magic`, and `lit now` was advertising *"Grimoire · up — use on cooldown ·
  waiting 18s"* on a button that had become a purge.
- 🐛 **New: `type(secret) == "number"` is TRUE**, so `ItemSpellID` returns Secret
  Values straight into the registry (buff-viewer IDs go secret in combat). Every
  downstream `==` then compares a secret. Suspected cause of **47 swallowed
  handler errors** hiding in the `other` counter.
- ✅ **Cast events readable in all four phases**, 0 secret across 178 events —
  START included, which unblocks spend-side anticipation.
- ❌ **The imp-count side channel is closed.** `GetStringWidth()`/`GetText()` both
  error, so the dot-glyph font has no rescue.

**M3c-b adds no new signal.** It makes the existing one true, and it is
deliberately ahead of the shard rail / mode chrome / opener queue because all
three render on top of the scored board.

*(Prior line:)* **M3c-a shipped; FIRST FEEDBACK PASS IN (2026-07-21, v0.10.0).**
The v0.10.0 in-game review below is no longer pending — it happened, and it
produced eleven items now parked as **§7.2**. The headline is a **live defect that
invalidates half the board**: `ns.PowerCost` returns the first non-zero cost of
*any* power type, so **mana costs are being read as shard gates** (Demonbolt
"shards 3<500" = a 5000-mana cost through the fragment heuristic; Mortal Coil,
Shadowfury and the defensives likewise). Demonbolt therefore **can never be
recommended**, and every costed utility ability sits at NEVER on a gate it should
never have been asked about. This is exactly what **V1(a)** predicted — "if the
cost column reads wrong the dots are wrong" — arriving through a cause the queue
didn't anticipate (power *type*, not shards-vs-fragments).

⚠ **Consequence for the strictness check (outstanding item 2): it is NOT yet
measured.** The on-screen summary read `lit 2`, which is inside the 1–2 target —
but with the gates falsely closed on a chunk of the board that number is
meaningless. **Re-run strictness after the cost fix**, and do not read the
pre-fix `lit` count as evidence the rules are tight.

Other findings, in §7.2: a transformed button is still scored as its base spell
(the Grimoire reads as a rotational summon while it's a pet command); the score
has no *spend*-side anticipation, so it reasons about shards you're already
committing; **"ready but unaffordable" collapses into NEVER**, so a ready Tyrant
at 3 shards reads as *nothing to do* when the instruction is the opposite; a
keybind remap wasn't picked up; and out-of-combat seeding (**M3d**) would remove
the "no edge seen yet" cold start entirely.

*(As originally shipped:)* The dot score. M3b's five in-game passes said the colour encoding doesn't read —
*"yellow, purple etc. don't really have any meaning in isolation"* — which is
correct and structural: hue carries **group**, which is ambient identity, not
instruction, and §0.5.8.7 established there is **no free visual channel** left to
re-encode into (hue = group, saturation = resource pole, luminance = readiness,
alpha = recede). So actionability gets a **new object**: a per-ability **dot**
carrying a level (NEVER / AVAILABLE / ROTATION / LATE), and a **row beside it
saying why**. Implements §7.1 **C1 + C2 + C3 + C5** plus the **napkin engine
pulled forward from M4**; C6 (terminal view) stays deferred.

- **`HudScore.lua`** (new) — a pure function of readable state → `(level,
  reasons)`. The reasons are what the row prints, so the score is **auditable,
  not an oracle**. `judgeable = false` **caps at AVAILABLE** where the true gate
  is a Secret Value (Implosion's ≥6 imps) — "inform, don't instruct" made
  mechanical.
- **`HudNapkin.lua`** (new) — anticipation, promoted from the `casts` probe.
  Rationale, in the user's words: *"firing cooldown abilities as soon as they are
  up is probably going to be the biggest win — I believe that requires signalling
  me early."* Without it the dot flips NEVER → ROTATION at the *instant* the
  cooldown lands, which mid-GCD is already too late. **The lead time is the
  feature.**
- **`SpecDemonology.lua`** — `role` replaced by the per-ability **signal bucket**
  (`kind` / `spends` / `generates` / `cadence` / `burstAlign` / `goGate` /
  `primary` / `judgeable`). `goGate` is a separate bit from `burstAlign` on
  purpose. Demonbolt moved to the **consumer** pole (C2).
- **`HudChrome.lua`** — the dot (**colour carries LEVEL, not group**), and the
  accent promoted from a border **on** Blizzard's icon art to a **bracket**
  spanning icon + dot + text — which was the original legibility complaint.
- **`HudRow.lua`** — was `HudDebug.lua`; **default-on** and part of the HUD now.
  `/cdmp hud debug` is a verbose flag on the same row builder, not a second
  renderer.

⚠ **This build takes on two costs the earlier scoping wrongly said it wouldn't.**
It **inherits §7's standing assumption** that `UNIT_SPELLCAST_SUCCEEDED` carries a
readable spellID in *all* combat contexts — confirmed in a delve and at an
open-world dummy, **never confirmed in a raid**. And the napkin is **the only
drifting input in the design**. Both are fenced structurally rather than hopefully:
the napkin can only make the HUD *early*, it can never promote a dot to ROTATION
(only an observed `Available` edge does that), it renders **hollow** so an
estimate never looks like an observation, and `hud status` **reports whether it is
live at all** rather than silently tracking nothing.

⏳ **Outstanding — the in-game pass, and it is the real test:**
1. **Carry the V1 queue over first** (§7.1) — **costs are now load-bearing**, not
   curiosity: the gate rule is `shards >= cost`, so if the cost column reads wrong
   the dots are wrong. Plus imp-stack survival and the still-unproven #3.
2. **Strictness before visuals.** Expect **1–2 ROTATION dots, not 4–5**;
   `hud status` prints a `levels:` count and a `lit now:` line naming each lit dot
   with its reason, and the on-screen summary carries a live `lit N` counter that
   turns amber above 2. **If it sits at 4+, tighten the rules — don't touch a
   colour.**
3. **Anticipation** — cast Dreadstalkers (~20 s) and watch the dot brighten ~3 s
   out with a live countdown *before* it lands. If 3 s isn't enough lead to change
   the next GCD, `SOON_LEAD` is the number to tune.
4. **`hud status` inside a raid or M+**, not just at a dummy — that's the untested
   context, and the one where the whole early-warning feature would silently go
   dark.
5. **Every lit dot's reason legible and true.** A dot whose reason you disagree
   with is a scoring bug; a dot with no reason is a design failure.

**Known-unknown to expect on the first enable:** every cooldown-bearing ability
reads `NEVER · no edge seen yet` until it has been cast once. That is the design
holding (readiness comes only from observed edges; we refuse to guess), not a bug
— but whether it's *tolerable* is exactly the kind of thing only the pass can say.

*(A pre-deploy adversarial review found seven defects, all fixed and re-verified.
The two that would have cost a pass: a false `on CD` reason on every unobserved
cooldown, and a `gated` ROTATION path that could light permanently with an
**empty** reason list if the cost read unreadable — `ns.PowerCost` reports
"genuinely free" and "unreadable" identically.)*

**Prior: M3b shipped and iterated (2026-07-20, CDMProbe v0.7.0 → v0.9.1).**
Five in-game passes turned M3b from "shipped" into "shipped and understood", and
the findings reshaped the roadmap — see **§0.5.8.7**, the amendment they produced,
and **§7.1**, the working backlog. Headlines:

- ✅ **The M3b design risk is closed.** `TriggerAlertEvent` is confirmed live —
  20 hooks, `Available`/`OnCooldown`/`OnAuraApplied`/`OnAuraRemoved` all firing,
  `secret=0`. The layered `IsShown` fallback was never needed (but stays built).
- ✅ **M3a's outstanding relayout check passed** in the same pass —
  `RefreshLayout=8`, all 20 items still bound, no ticker. The one real regression
  risk from dropping the 2 s ticker is retired.
- ✅ **#2 confirmed** — Demonbolt lights on a Demonic Core proc.
- ❌ **#3 has never once been observed** — `spell-override events: 0` in every
  pass. The Demonic Art glow is still entirely unproven (§7.1 V1c).
- 🐛 **The recede never worked as shipped.** `Wake()` cancelled the sleep timer
  and brightened but nothing re-armed it, and `Wake` fires on every ready edge and
  every proc — so the *first* edge killed the recede permanently. Fixed v0.7.1
  (arm/disarm; instant wake, debounced sleep). Also, at 1–2px accents the recede
  was invisible even when correct, so the DEMO.SYS frame and scanlines now follow
  it as a unit.
- 🔎 **Finding: readiness-as-cooldown covers only a MINORITY of the board.** Hand
  of Gul'dan and Demonbolt have **no cooldown**, so they never fire a ready edge
  and sit at "unknown" forever — and they are the two most-pressed buttons.
  Measured: 3–4 cooldown edges vs 19+ aura edges in one session. This falsifies
  §0.5.8.4's board-wide luminance promise (§0.5.8.7 §2) and is the single most
  consequential thing M3b taught us.
- 🔎 **Finding: the ambient colour encoding is not legible on its own** —
  *"yellow, purple etc. don't really have any meaning in isolation."* Correct, and
  a property of the design: hue carries **group**, which is identity, not
  instruction. Prompted the **LOUD pass** (v0.7.2 — every state signal cranked
  past legibility, explicitly *not* final values, all in one TUNING block) and
  then the **words-first readout** (`/cdmp hud debug`, v0.8.0–v0.8.2), which is
  now promoted into the default view (§0.5.8.7 §3).
- 📦 **Shipped alongside:** bundled JetBrains Mono; the Utility column's text runs
  leftward so the two columns bracket the character; **#17 (Wild Imp stack + "/6")
  pulled forward from M5 into M3**; power costs read at runtime rather than
  authored into the spec table.

**M3b as originally scoped (v0.7.0) — the first STATE signals.**
*(Superseded in emphasis by M3c-a: the colour/luminance/thickness encoding below
is still shipped and still carries identity, but it is no longer what the player
is expected to read for an instruction — the dot is.)*
`/cdmp hud` now says not just who each icon is but what it's *doing*: a **ready
accent** off the observed ready edge (+ a one-shot settle, the one place motion is
allowed), the **Demonic Core proc-glow** on Demonbolt (softening at ≥4 shards), the
**Demonic Art proc-glow** on the transformed button, and the **empty-board recede**.
Covers §0.5.8.3 rows **#5, #2, #3**. New module `HudState.lua`; `HudChrome` refactored
to a **composed accent** with a single writer. Details + the four source findings that
reshaped it: §6 M3b and `notes.md` §1. **In-game pass outstanding** (this one also
carries M3a's untested relayout check).

**Prior: M3a shipped (2026-07-20, CDMProbe v0.6.1) — the first product code.**
After four decision/prototype milestones, `/cdmp hud` exists: it binds per item by
`GetCooldownID()` to the **live** CDM layout and draws terminal chrome around
**native, untouched** Blizzard icons. Covers §0.5.8.3 row **#4** (group colour map
+ generator/consumer batch tint) plus keybinds and both deferred M1 perf cleanups.
`/cdmp crt` is **retired and `CRT.lua` deleted**; its leaf-method icon-tint
machinery survives **dormant and unwired in `HudTint.lua`** (`notes.md` §9). New
modules: `SpecDemonology.lua` (the one per-spec data table — the seam M7's second
spec plugs into), `HudCore` / `HudChrome` / `HudBinds` / `HudTint`.
**First in-game run (2026-07-20)** confirmed the identity layer — all 20 items bind,
group/role assignment matches §3, keybind shortening works — and produced three
findings, two of them fixed in **v0.6.1**:

1. **Defect: the keybind cache thrashed** — 2085 full 180-slot scans in one city
   session, because `ACTIONBAR_SLOT_CHANGED` fires per-slot and the handler
   rescanned synchronously on each. Exactly the hot-path rescan the §6 risk list
   forbade. **Fixed:** debounced + coalesced, and the chrome re-attach is skipped
   unless the resolved map actually changed.
2. **The tracked set had drifted from the docs** — Utility is **7** spells, not 13,
   and carries **Command Demon `119898`** rather than Axe Toss `119914`. Fixed in
   `SpecDemonology`; `notes.md` §2 corrected. This weakens the stated case for the
   M7 curated layer-① override (§7).
3. **`428514` is tracked twice** under two cooldownIDs — direct validation of the
   M2 decision to key on `cooldownID` rather than `spellID` (`notes.md` §2/§5).

⏳ **Still outstanding: the relayout test** — the run logged `RefreshLayout=0`, so
the one real regression risk (dropping the 2 s ticker) is **untested**. `notes.md`
§5's rebinding-event bullet is written but explicitly marked unconfirmed until it
passes. **This check rolls forward into the M3b pass** — it is the first item on
that checklist, ahead of any new-feature verification.

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
  - **M3b — readiness + procs — ✅ SHIPPED (2026-07-20, v0.7.0); in-game pass
    outstanding.** Icons left native ⇒ Blizzard's on-cooldown dimming is preserved
    for free, which **resolves the §9 "ready vs on-cooldown" decision by dissolving
    it** (we no longer own that pixel): we *add* a ready accent off the observed
    ready edge + **empty-board recede** (#5), the **Demonic Core proc-glow on
    Demonbolt** (#2) and the **Demonic Art proc-glow on the transformed button**
    (#3), as our own styled overlays.

    **Source research changed the approach on all three rows.** Re-reading
    `Blizzard_CooldownViewer/CooldownViewer.lua` @ 68453 before writing any code
    produced four findings — a better mechanism than the plan assumed, and two
    traps that would otherwise have shipped as **silent no-ops**. They are written
    up in full in **`notes.md` §1** (`TriggerAlertEvent` choke point · the
    `GenerateClosure`/`OnCooldownDone` trap · the override-spellID behaviour · the
    `IsShown`/`hideWhenInactive` caveat). In short:

    - **`TriggerAlertEvent` is one choke point for every edge we want** — ready
      rising *and* falling, proc applied *and* removed — and it fires
      **unconditionally**, because the user's alert configuration is checked inside
      the body rather than before the call. One hook per item instance replaced the
      planned `IsShown()` polling for #2/#3 and made #5's falling edge free.
    - **`OnCooldownDone` is unhookable via `hooksecurefunc`** — `OnLoad` captures
      the function reference in a `GenerateClosure`, so the hook never runs. Would
      have been a no-op nobody noticed. (`item.Cooldown:HookScript` is the way, if
      ever needed. It isn't.)
    - **The Demonic Art transform is directly observable** via
      `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED(base, override)` — so #3 knows
      exactly *which* button transformed. Driving it off the override event rather
      than Diabolic Ritual's presence also avoids a near-permanent false positive:
      the Ritual buff is up through most of the accumulation, not just once an Art
      is armed. Presence is still tracked and reported as **corroboration**.
    - **That same override behaviour was a live M3a defect** — `item:GetSpellID()`
      prefers the override, so the M3a keybind lookup missed and **the keybind
      blanked out** for the whole transform. Fixed: identity now resolves off
      `GetBaseSpellID()`.
    - **`IsShown()` presence is conditional on a user setting** —
      `ShouldBeShown()` short-circuits to true unless the viewer hides inactive
      items, so a glow driven off it would **latch on permanently**. It's now
      capability-checked, and `notes.md` §1's previously unqualified claim is
      corrected.

    **What the build decided (things the plan left open):**
    - **`HudChrome` refactored to a COMPOSED accent with a single writer.** M3a
      wrote edge colours straight out of group+role in `Attach`, and `HudBinds`
      calls `Attach` on every keybind change — which would have stomped readiness.
      Now `identity` × `ready` × `recede` compose through one `H.Apply`, so state
      survives a re-attach. This is the M3a encoding split finally paying out:
      **hue = group, saturation = role, luminance = readiness, alpha = recede** —
      four independent channels that can never fight.
    - **`ready = nil` is a real state, not a default.** At bind time we cannot know
      whether a cooldown is up without a secret read, so accents sit at **base**
      luminance until an edge is observed. Unknown ≠ ready and unknown ≠ on-cooldown;
      `hud status` prints all three.
    - **Layered presence, honestly reported.** Edges are primary; the `IsShown`
      *level* read is used for initial sync and a throttled ~10 Hz backstop **only
      where the setting makes it meaningful**. `hud status` says which layers are
      live rather than pretending, and probes whether `item.isActive` reads
      non-secret — if it does it's a strictly better level source and M3c upgrades.
    - **The proc glow is ours, not `LibCustomGlow`** (no new dependency) and not
      Blizzard's spell-activation overlay — which stays untouched *underneath*, so
      a native glow and ours coexist instead of one hiding the other.
    - **Recede counts out-of-combat as quiet.** "Shards low + nothing glowing" alone
      would rarely fire while idling at 3+ shards, and out of combat there is
      genuinely nothing to press. Sleep is debounced ~0.5 s; **wake is instant** on
      any proc or ready edge, so it cannot strobe between GCDs.
    - **Only the HoG half of #3 is glowable** — Shadow Bolt isn't in the tracked
      set, so SB → Infernal Bolt has no icon. Flagged as a blind spot in
      `guidance-model.md` §0.5.5, not faked; re-opens only with an M7 curated
      layout override.

    **Outstanding in-game pass:** **M3a's relayout check first** (Edit Mode →
    Orientation / # Rows → `RefreshLayout` increments, nothing detaches; and the
    keybind cache reads a handful of scans with a `coalesced` count, not thousands).
    Then at a dummy: Demonbolt lights on a Core proc and **softens** at ≥4 shards ·
    HoG lights when Demonic Art arms it and its **keybind stays visible** through the
    transform · Dreadstalkers coming off CD settles **exactly once** then holds a
    steady bright accent, and accents start at base luminance after `/reload` ·
    the board dims after ~0.5 s idle and wakes on the first edge without strobing ·
    `hud status`'s state block reports the right glow states and says whether level
    reads are available · off → pixel-clean, `/reload` restores.

    **Known risk — ✅ CLOSED (2026-07-20).** `TriggerAlertEvent` was the whole
    design, and it holds: confirmed live at 20 hooks with all four edge types
    firing and `secret=0`. The layered `IsShown` fallback was never needed; it
    stays built as the documented contingency.
  - **M3c-a — the dot score — ✅ SHIPPED (2026-07-20, v0.10.0), in-game review
    pending.** The milestone M3b's findings *created*. Implements §0.5.8.7 via
    §7.1 **C1 + C2 + C3 + C5**, plus the **napkin engine pulled forward from M4**;
    **C6 (terminal view) deferred**.

    **Why it exists.** M3b encoded state as colour, luminance, thickness and glow,
    and five passes returned one verdict: the encoding doesn't read in isolation.
    That is not a tuning failure — hue carries **group**, ambient identity, and the
    review established there is no free channel left. Two findings reframed the
    work: **readiness-as-cooldown covers only a minority of the board** (HoG and
    Demonbolt have no cooldown, never fire a ready edge, sat at "unknown" forever —
    and they are the #1/#2 most-pressed buttons, 729/541 pooled casts; measured
    3–4 cooldown edges vs 19+ aura edges in a session), and the governing principle
    **"inform, don't instruct"** — *"pick between 2-3 abilities instead of 5."*

    **What shipped.**
    - **`HudScore.lua`** — level + reasons, pure function of readable state, owns
      no frames. Four levels: **NEVER / AVAILABLE / ROTATION / LATE**. `SOON` is a
      **treatment on NEVER, not a fifth level** (§0.5.8.7 §1) — an anticipating dot
      never claims pressability, so it never needs filtering out.
      **`judgeable = false` caps at AVAILABLE** where the true gate is a Secret
      Value and says so (Implosion: *"≥6 imps — count is secret, your call"*).
      Strictness is **strict by decision**: 1–2 lit, not 4–5.
    - **`HudNapkin.lua`** — `SUCCEEDED` cast → `ns.BaseCooldown` countdown. Three
      rules keep it honest: **the observed edge is ground truth and always wins**
      (an `Available` edge clears the estimate outright); **expiry never claims
      readiness** (it reads *"should be up, unconfirmed"*); **readability is
      checked, not assumed** (reported in `hud status`).
    - **`SpecDemonology.lua`** — the signal bucket. `role` conflated three
      concepts; the tell was that `spender` and `burst` carried **identical** tint
      values, so `burst` never encoded anything — it only smuggled burst-lane
      membership through the tint field. `goGate` kept **separate** from
      `burstAlign` so nobody re-derives the go-gate lane and re-ships §0.5.8.6
      blocking error #2. Demonbolt → consumer pole (C2, a live defect in shipped
      code: it rendered at the opposite pole from HoG, its most common partner).
    - **`HudChrome.lua`** — the dot (masked circle, square fallback; **colour
      carries LEVEL**; hollow = estimate-or-not-a-call, solid = asserted), and the
      accent → **bracket** spanning icon + dot + text, width from
      `GetStringWidth()` *after* `SetText` (the order-of-attach hazard, avoided by
      measuring rather than predicting).
    - **`HudRow.lua`** — was `HudDebug.lua`, now default-on. One row builder, a
      verbose flag — deliberately not two renderers to drift.

    **The cost, stated plainly.** The original scoping claimed this work had "no
    dependency on cast-spellID readability and no drift." **Both were false.** It
    takes on §7's standing assumption (never confirmed in a raid) and introduces
    the design's only drifting input — now carrying the feature the user rates
    highest. Mitigations are structural, not hopeful: early-never-wrong, no
    promotion on an estimate, hollow rendering, and honest reporting. The failure
    mode to watch for is the opposite of the obvious one — **an estimate that
    reads as confident.**

    **Outstanding in-game pass:** see the Status block — V1 queue first (costs are
    now load-bearing), then **strictness before visuals**, anticipation lead time,
    a **raid/M+ `hud status`** check for napkin readability, and reason legibility.

    **Known risks.** Strictness is the whole UX and cannot be validated from here.
    The rules encode a **rotation opinion** derived from
    `knowledge/classes/warlock/demonology/` — a wrong ROTATION is worse than no
    dot (§0.5.8.2(c) forbids confidently-wrong), and the `why` text is the
    mitigation: a bad call is arguable rather than silent. `judgeable = false` is a
    **growth area** — Implosion is the known case; others with secret gates need
    the same cap, not a guess.

  - **M3c-b — the truth pass. ✅ CODE SHIPPED (2026-07-21, v0.13.0) —
    IN-GAME PASS OUTSTANDING, and the in-game pass *is* the milestone.** Every
    item below is implemented and luaparser-clean; none of it is confirmed. The
    exit criterion is a **measurement taken at a dummy**, not a diff, so this
    entry does not close until §7.3's checklist is run.

    **What landed, in the order it was written (B2 → B1 → B6 → B3 → B4, B7
    alongside):** the secret guard at the identity source + last-known-good
    identity across rebinds; live-identity scoring with an unrecognised override
    scoring **no dot**; LATE gated on `InCombatLockdown()` with the candidate
    clocks wiped on `PLAYER_REGEN_ENABLED`; the `other`/`errors` counter split;
    spend-side projection off `UNIT_SPELLCAST_START` with the double-deduction
    guard and hollow rendering; and **B7**, the expected-vs-bound warning.

    **B5 was considered and DEFERRED to M4** — its "go build shards" half has no
    icon to land on today, so it belongs with the burst lane where the go-gate
    and telegraph already live.

    *(The plan of record follows.)* *The milestone the
    v0.12.0 probe created.* M3c-a gave the board an opinion; the first feedback
    pass plus the probe show that in specific, enumerated ways **the opinion is
    false** — and a false dot is worse than no dot (§0.5.8.2(c)). So this
    milestone adds **no new signal at all**. It makes the existing one true, and
    it is deliberately sequenced ahead of the shard rail, mode chrome and opener
    queue: every one of those renders *on top of* the scored board, so shipping
    them first would decorate a board that lies.

    **The exit criterion is a measurement, not a feature list:** a dummy pass
    where **every lit dot survives being argued with** — `lit now` names 1–2, and
    each named reason is one you agree with. That number is currently
    unmeasurable (see B1 below).

    - **B1 — Score the LIVE identity, not the base spell.** `HudScore.For` reads
      `e.baseSpellID or e.spellID` unconditionally, so a transformed button is
      judged as the ability underneath it. **Observed live:** `lit now` advertised
      *"Grimoire: Fel Ravager · up — use on cooldown · waiting 18s"* while that
      button was **Devour Magic** (`1276467 → 388215`) — a LATE dot nagging for a
      cooldown that isn't there. Resolve through the override, and give an
      unrecognised override **no dot** rather than letting it inherit `cadence`.
      Add the four confirmed pairs to `SpecDemonology` (`notes.md` §1).
      ⚠ Deliberately the **opposite** convention from keybinds, which resolve off
      the *base* precisely because the override is on no action bar (the v0.7.0
      finding-3 fix). The two must not be "unified" later.
      ⚠ And the event alone is **not** sufficient — the override is set when the
      pet is summoned, i.e. **before we start listening** (login / `/reload` / HUD
      enabled mid-session). So identity must be **polled at bind time**, with the
      event as the fast path that keeps it current. *(This corrects the first read
      of the evidence: a zero event count was taken as "the event never fires for
      this button"; a later run caught it firing 4 times. The conclusion holds —
      a missed event and an absent event are indistinguishable — but the reason is
      general, not a per-button quirk. `notes.md` §1.)*
    - **B2 — The secret-ID guard.** `type(secret) == "number"` is **true**, so
      `ns.ItemSpellID` / `ns.ItemBaseSpellID` currently *return* a Secret Value
      into the registry, and every downstream `e.baseSpellID == spellID` compares
      one. Guard at the source with `ns.IsSecret`, and make an unreadable ID mean
      **"keep what you had"**, never "update". Suspected cause of the `other=47`
      swallowed handler errors. Full write-up: `notes.md` §1.
    - **B3 — Split the `other` alert counter** into *unhandled alert type* vs
      *handler threw*. They are the same number today, which is how 47 errors
      hid in plain sight in a readout we've been reading for five passes.
    - **B4 — Spend-side anticipation.** Project `−ShardCost` / `+generates` on
      `UNIT_SPELLCAST_START` and score against the projected figure until
      `SUCCEEDED`/`STOP` reconciles. *"As soon as I start casting HoG it should
      assume those shards are consumed."* **Unblocked** — the probe read START at
      52/52 readable, 0 secret.
    - **B5 — "Ready but unaffordable" is not NEVER.** A ready Tyrant at 3 shards
      reads as "nothing to do" when the instruction is **go build**. First
      consumer of `goGate` / `burstAlign`, which nothing reads today.
      **➜ DEFERRED TO M4 (2026-07-21).** Not dropped, and not deferred for cost:
      the half that matters is *"go build shards"*, and there is **no icon for
      that instruction** — it is a statement about the resource, not about any
      button, so it wants the shard rail (M3c-c) or the burst lane (M4) to render
      on. Shipping only the "don't call this NEVER" half would soften a dot
      without ever saying what to do instead, which is the noise M3c-b exists to
      remove.
    - **B6 — LATE must not accrue out of combat.** The OOC probe caught Hand of
      Gul'dan sitting at *"LATE · waiting 7s"* while standing in a city. LATE is
      a nag; a nag with nothing to nag about is noise that trains you to ignore
      the channel.
    - **B7 — Warn when an expected icon isn't there to bind to.** *(Added at the
      user's request, generalised from the Shadow Bolt case.)* M2 decided we bind
      to whatever layout is **currently active** and ship no layout string, so the
      tracked set is the *user's*, not ours — which makes a missing spell
      **completely invisible**: `ns.Spec` describes an ability, no item ever
      appears for it, and the HUD never mentions it again. Every signal keyed to
      it goes quiet **with no error**. That is precisely how Shadow Bolt's absence
      hid the SB → Infernal Bolt blind spot for four milestones, and it is the
      risk knowingly accepted by adding Shadow Bolt by hand.
      Implemented as an expected-vs-bound diff after `rebind()`, filtered by
      `IsPlayerSpell` (without it it cries wolf on every untalented alternative —
      Imp Lord vs Fel Ravager, Axe Toss vs Command Demon) and by a new
      `expect = false` flag on entries that exist only as a live override (the
      Art transforms, Devour Magic). **Warned once per resolved set** — `rebind()`
      fires on every `RefreshLayout`, so an unconditional print would spam the
      chat frame on every Edit Mode nudge — and listed **every time** in
      `/cdmp hud status`, which is the persistent home and what `/cdmp probe`
      captures to disk. The message says what is **lost**, not just what is
      absent: *"Shadow Bolt — not tracked; SB → Infernal Bolt cannot light"*.

  - **M3c-c1 — the shard rail + the mode spine. ✅ CODE SHIPPED (2026-07-21,
    v0.15.0; in-game pass §7.5 outstanding).** *The ambient resource layer, and
    the first surface on the HUD for a sentence that isn't about a button.*

    **Why the rail was the right next thing.** §0.5.2 makes shard-cap the anchor:
    *"if exactly one cue survives every accessibility/mute ceiling, it is
    shard-cap."* It is moment **#1**, **P0** (inaction there is strictly wrong),
    and it rides our single strongest capability — Soul Shards are readable **and
    branchable** even in restricted combat. Until this build nothing on the HUD
    said it. The board judges **buttons**; overcap is a statement about the
    **resource**, which is exactly why B5 / §7.2 item 8 was deferred with the note
    that its missing half — *"go build shards"* — **"wants the shard rail to
    render on"**.

    **What landed, in dependency order:**

    - **R1 — `S.Mode()`, the mode spine.** One computation beside
      `S.ProjectedShards()`, returning `(mode, projected, isProjected)` over
      §0.5.8.4:713-716's ladder **minus BURST**: `nil` when shards are
      unreadable (unknown is first-class and never guessed) → **PREP** when out
      of combat (§0.5.8.2(a)'s fourth resting state, and explicitly *not*
      GENERATE) → **SPEND** on `projected >= SPEND_AT`, **projected not live**,
      because the predictive pre-flip is the point → **GENERATE** otherwise.
      BURST is left as a **named vacancy** citing `HOLD_LEAD ≈ 5 s`
      (§0.5.8.6 correction 1 — *not* §0.5.1's stale `~15 s`), so M4 inserts a
      branch rather than rewriting the ladder. `LOW_SHARDS` is now **derived from
      `SPEND_AT`** — it was the same threshold under another name, and its own
      comment already said so, so board-quiet and the mode can no longer drift.
    - **R2 — the rail widget.** `H.ShowRail` / `H.PaintRail` / `H.HideRail`,
      memoised on `viewer.__hudRail`, a **viewer-anchored child** so it rides
      Edit Mode drags and orientation changes for free and needs no saved
      position. Four traps handled, all already documented in the file it copies:
      the **clipping hazard** (single centre anchor + explicit width — two
      horizontal points fix the width to the ~28 px icon column and clip), never
      `EnableMouse`, `receders[f]` so board-quiet dims it with everything else,
      and **recede vs. animation** — the cap flash and sparks live on a
      **sibling** frame, because a child would inherit the receded alpha and the
      P0 cue would be dimmest exactly when the board was quietest.
      Geometry + animation **ported** from the M1 prototype (`Resource.lua`
      :132-243), which is proven but UIParent-anchored and self-eventing — a
      reference to port, never to call. `Resource.lua` is untouched. Segment
      count reads **`ns.SHARD_CAP`**, never a literal 5.
      - **Fill + the ghost head.** Whole shards stay the **gate**;
        `readFragments()` (`UnitPower(..., true)`, 0..50) smooths **only** the
        partial segment, and if fragments read unreadable the rail draws whole
        segments and nothing else changes. *(Unrelated to the unproven fragment
        heuristic in `ns.ShardCost` — that is about a spell's reported **cost**;
        this reads the player's power directly.)* The **incoming** segment comes
        from `S.ProjectedShards()` and renders **hollow** — the same
        "hollow = estimate" convention the dots use. The projection engine
        shipped in M3c-b B4, so this is a render, not new logic.
    - **R3 — the cap treatment (the P0 anchor).** Alert colour + a
      `SPEND — CAP (5/5) act or waste` label, framed per **[B1]** as a
      **warning, not a trophy** — overcap is an opportunity-cost loss, and §3's
      celebratory framing is explicitly nuanced by this. One-shot glitter on the
      **false→true edge only**, `Stop()` before `Play()` so a re-fire restarts
      rather than stacks. ⚠ **Throttled**, because the prototype has a real
      defect here: `fireGlitter` fires on every `prevCapped` transition, so at cap
      a HoG (−3) plus a refill re-fires within a couple of GCDs — [X2] is WCAG's
      three-flashes-in-one-second guidance. **~2 s re-arm, and the suppressions
      are counted in `hud status`** so the throttle can prove it is working
      rather than looking like the edge never happened.
      `rail.hold_treatment()` (§0.5.8.4:723) is BURST-gated → **M4**.
    - **R4 — mode chrome on two non-icon surfaces.** The rail's fill colour
      (GENERATE / SPEND / CAP + a distinct calm **PREP** tint) and the DEMO.SYS
      terminal chrome (`TERM`/`TERM_MID`/`TERM_DIM` — header, sub, rules, footer;
      never an icon), plus the **redundant glyph + label** [X1] makes mandatory.
      Steady-state carries **no motion and locked positions** ([V3][V7]); the cap
      glitter is the rail's only sanctioned movement. Written up as
      **`guidance-model.md` §0.5.8.8**, which also records that PREP is a fourth
      mode §0.5.1's three-mode table never mentions.
    - **R5 — wiring.** Redraw rides the tail of `S.Recompute()` — the one tail
      that sees every input the mode reads, including `beginCast`/`endCast`,
      which is what makes the predictive flip land **during** the cast. **No new
      ticker** (`HudCore.lua`'s header rule stands). ⚠ The power branch's
      `if n ~= S.shards` early-out **swallowed fragment-only changes**, which
      would have frozen the partial fill between whole steps; both values are now
      compared, on **different paths** — a whole-shard step moves gates, a
      fragment tick moves one texture's width and must not drag a board
      re-evaluation behind it. Lifecycle from `rebind()` (which *is* the
      `RefreshLayout` callback, so a relayout re-shows it) and `SetHud(false)` /
      `S.Stop()`. `rail = true` in `HUD_DEFAULTS` — default-on, because the cue
      §0.5.2 ranks first is not an opt-in — with `/cdmp hud rail` to toggle.

    **What the in-game pass has to settle (§7.5):** that the rail is not clipped
    to the icon column, that the partial segment actually *moves* (or that
    `hud status` says fragments are unreadable here — **that is an answer, not a
    failure**), that the ghost head reads as an estimate, that the SPEND flip
    lands mid-cast, and that cap does **not strobe**.

  - **M3c-c2 — the sequence queue + the opener. ✅ CODE SHIPPED (2026-07-21,
    v0.17.0; in-game pass §7.7 outstanding).** *(Split out of M3c-c, 2026-07-21;
    the reusable-widget re-scope taken 2026-07-21 with the user — see the Status
    block and `guidance-model.md` §0.5.8.10.)*

    **The decision that shaped it.** M3c-c2's opener and M4's burst-window queue
    are the same shape (§0.5.8.2(a) and M4's own entry already call the burn queue
    *"mostly reuse rather than new invention"*). Rather than build the opener
    bespoke and bend it into M4, the milestone was re-scoped to **build the shared
    widget and ship one consumer.** The two milestones stay split — PREP is shipped
    while BURST is a whole sub-project, and only one of M4's five parts is
    sequence-shaped — but the reuse is now a *designed seam*, not a hope.

    **What landed, in dependency order:**

    - **`HudQueue.lua` (new) — the reusable widget.** A viewer-anchored child
      (memoised on `viewer.__hudQueue`, rides Edit Mode like the rail; one centre
      point + explicit width, the §9 clipping rule), spec-agnostic, holding no
      spell constants. Two rules baked in because **M4 needs them too**: **advance
      = drop-through, never jam** (a matching press consumes that step *and* drops
      every earlier un-pressed one, so pressing out of order tracks where you are
      instead of freezing — the §0.5.8.7 §0 failure mode), and **`count`** (HoG×2,
      SB×3; the Tyrant block is HoG HoG too — the field belongs to the widget). It
      renders as a **draining ghost** in the DEMO.SYS terminal idiom: whole script
      dim, current step bright, consumed steps fall off; no motion, positions
      locked ([V3][V7]).
    - **`ns.SpecOpener` in `SpecDemonology.lua`** — the data, **re-verified
      against the live #1 parse** (Inphected, WCL bracket 291): `Dreadstalkers →
      Imp Lord → Tyrant t≈3.4s → SB/DB → HoG×2 → Implosion → SB×3`. The pre-pull
      casts are a **shown-not-tracked preamble** (WCL can't see them, we can't
      cast-verify them); `alt` matches the first spend as DB-or-SB; `optional`
      steps (Imp Lord, Implosion) drop without stalling. *(One opener, no variant
      machinery — the old "1a/1b" split is scrubbed.)*
    - **`HudOpener.lua` (new) — the consumer glue.** Owns arm/advance/dissolve:
      arms out of combat (the pre-pull affordance), advances off our own casts
      **resolved to the base identity** (a transformed Ruination press still ticks
      the HoG step — the reverse of the keybind convention, the same split B1
      made), dissolves on the **first Tyrant window close** read off `HudNapkin`'s
      fixed-60s clock as a plain elapsed-time compare, and re-arms next pull. No
      secret reads, no new events. M4's burst window is the **second consumer** and
      is a sibling of this file.
    - **Wiring** — three one-line calls in `HudState` (advance on `SUCCEEDED`,
      re-arm on `PLAYER_REGEN_ENABLED`, the dissolve clock on the `S.Recompute`
      tail — no new ticker), arm in `HudCore`'s `rebind()` tail, hide on
      `SetHud(false)`, a **`queue`** transition kind in `HudLog` (armed / advanced
      / dissolved, captured to disk), and `/cdmp hud opener on|off` + a status line.

    **Default OFF** — it is the only instructional widget and §0.5.8.7 §0 put it on
    notice, so it must be opted into; PREP chrome (M3c-c1) is on regardless.

    ⚠ **Gate.** Board-*independent* (it reads casts, not the dot score), so §7.7
    can run before the strictness session. But **do not cut the release trusting
    the board** — the rest of the roadmap still waits on §7.6 → §7.3 → §7.4 → §7.5.

    *(The three scoring corrections that briefly lived here moved to **M3c-b**; the
    **anticipation engine** shipped early, in M3c-a/M3c-b. The **fill-to marker**
    moved out with 1b.)*

- **M3d — out-of-combat seeding — ✅ CODE SHIPPED (2026-07-21, v0.14.0; in-game
  pass §7.4 outstanding).** *The cold-start fix.* Today
  every cooldown-bearing ability reads `NEVER · no edge seen yet` until it has
  been cast once in the session, because readiness comes **only** from an observed
  `Available` edge. That was accepted as "the design holding, not a bug" when
  M3c-a shipped — and the premise it rested on is now **measured false**.

  **✅ THE GATE IS OPEN (2026-07-21, v0.12.0 probe).** `notes.md` §1's
  `GetSpellCooldown().duration` = `<secret>` row was captured **in a delve, in
  combat**, and generalised too far. Measured: **13/13 tracked spells readable out
  of combat, 0/13 in combat.** Open-world both runs, so the gate is **combat**,
  not instancing. Therefore:
  - readiness can be **seeded at bind time** instead of waiting for an edge,
  - the napkin can be **seeded mid-cooldown** on enable / `/reload` / zone-in,
  - and we cross into combat from truth rather than from nothing.

  **This is reading, not guessing** — the M3b doctrine ("readiness comes only from
  observed edges; we refuse to guess") is about *inferring* a secret, and stands
  unchanged inside combat. The seam is the combat boundary: seed OOC, fall back to
  edges the moment reads go secret, and **never let a stale seed outlive an
  observation** — same precedence rule the napkin already obeys.

  ✅ **RESIDUAL CLOSED (2026-07-21).** The worry was that `duration=0` on every
  spell meant the OOC read was a *"not on cooldown" constant* rather than a real
  value — a milestone that looks alive and isn't. Confirmed real:

      Summon Demonic Tyrant        duration=60 startTime=126156.254

  A genuine mid-cooldown read, out of combat, with `startTime` in `GetTime()`
  units — so `startTime + duration - GetTime()` seeds both readiness **and** the
  napkin directly. Every other spell read 0 because it was genuinely ready.
  **M3d is fully unblocked.**

  **Ordering: after M3c-b, before M3c-c.** The cold start costs trust on *every*
  pull, and a seeded board is what makes M3c-c's pre-pull affordance mean
  anything — an opener queue over a board of `no edge seen yet` is decoration.

  ⚠ **Numbering:** slotted as **M3d** rather than taking the M5 number the request
  floated — M5/M6/M7 are already spoken for and cross-referenced from three other
  docs, so inserting a new M5 means renumbering all of them. It also belongs to
  the M3 state-layer family (M3b readiness → M3c-a the dot → M3d where readiness
  *starts*). Say the word if you'd rather pay the renumber.

  **What shipped (v0.14.0).** Four pieces, in dependency order:

  - **D1 — one read door.** `ns.ReadCooldown(spellID)` in `Util.lua` →
    `(ready, remaining, duration, startTime)` or **`nil`** when unreadable, so no
    caller re-derives the guards. Guards in order because each is a *different*
    failure: `pcall` the call → `ns.IsSecretTable(info)` → `ns.IsSecret` on **each
    field** (the probe's `<secret table>` and `<secret fields>` verdicts are
    distinct and **both were observed**). `secretTable` was a **duplicate local**
    in `Probe.lua`; it is now `ns.IsSecretTable` beside `ns.IsSecret`, one
    definition.
    - ⚠ **The GCD trap, load-bearing.** `GetSpellCooldown` reports the **global
      cooldown** for a spell that is genuinely ready, so a naive `duration > 0`
      reads *every* ability as on-cooldown for 1.5 s after any cast. Resolved
      against the **live GCD** (`61304`) rather than a magic number — a matching
      `(startTime, duration)` pair is the GCD, not this spell — with a
      `duration <= 1.5` backstop for when the GCD read itself is unavailable.
    - **Charges.** For a charged ability the call reports the *recharge of the
      next charge*, so a banked charge would seed as on-cooldown. `GetSpellCharges
      > 0` (secret-guarded) means **pressable → ready**. No tracked Demo ability
      has charges today; this is pre-emptive, and it is exactly the one-line miss
      that would read as "seeding just doesn't work on that button".
  - **D2 — seed readiness *and* the countdown.** `HudState.SeedFromReads()` walks
    the icon-viewer items, resolves the **live identity** the way B1 established
    it (`override[base]` → `e.spellID` → `base` — not re-derived a second way),
    and: ready → `SetReady(true)` + `Napkin.Clear`; on cooldown → `SetReady(false)`
    + **`Napkin.Seed(startTime, duration)`**; **unreadable → touches nothing** (an
    unreadable read is not evidence of anything — overwriting a known state with
    it is the B2-shaped mistake). `HudNapkin` gained `N.Seed` / `N.SourceOf` and a
    `source = "read"|"cast"` field; `N.Remaining` and the SOON treatment are
    **unchanged** — one countdown store, two ways to fill it.
    - **Precedence, three sources now:** (1) an **observed alert edge** always
      wins and clears both; (2) a **seed** overwrites a cast-derived estimate — it
      is the client's own number, not our arithmetic; (3) an **estimate** fills
      only what neither has.
  - **D3 — the combat boundary is the seam.** Seeded in the `rebind()` tail
    (login / `/reload` / zone-in / layout change — *the* cold-start fix) and on
    **`PLAYER_REGEN_ENABLED`**, which re-truths the whole board and is the free
    fix for `"should be up, unconfirmed"`. **Never in combat**, gated at the call
    site *and* inside `ns.ReadCooldown` because a caller added later will not
    remember. **No ticker** — a finishing cooldown still fires its `Available`
    edge out of combat, so the event path covers the tail.
  - **D4 — provenance: solid readiness, hollow SOON.** A seeded ready/on-CD
    boolean renders **SOLID** (a direct observation, same standing as an edge);
    **SOON stays HOLLOW whatever the source**, because it is a claim about the
    *future* and how it was sourced doesn't change that. The row names the source
    — `~42.1s (read)` vs `~1.8s (est)` — and `hud status` reports whether OOC
    reads work **in this context** plus per-item `ready=yes(seed)` / `ready=no(edge)`.
    The `"no edge seen yet"` wording **stays**: still correct for a cold start
    that began *in* combat, it will simply fire far less.

  **Shipped in one release with M3c-b (v0.13.0 was committed but never cut).**
  Accepted deliberately; the mitigation is the per-item **seed-vs-edge
  provenance** in `hud status`, which keeps the two milestones separable in the
  readout. §7.3 and §7.4 are run as **one combined dummy pass, §7.3 first** — so
  M3c-b's strictness criterion is measured on a board whose cold start is
  already gone.

  ⚠ **Standing risk, same standing as the napkin's.** The OOC read has only been
  measured **open-world**. If it also goes secret in some other out-of-combat
  context (an instance lobby, a raid between pulls) seeding silently does less.
  Contained by design — unreadable touches nothing, the board falls back to edges
  — but it is **reported** in `hud status`, not inferred later from a shrug.

- **M3e — close the loop: the pull recorder — ✅ CODE SHIPPED (2026-07-21,
  v0.16.0; in-game pass §7.6 outstanding, and it is *self-verifying*).**
  *Six milestones of code are shipped and three in-game passes are stacked
  unclosed. That is not a scheduling accident, it is a tooling gap.*

  **The gate is one measurement the tooling cannot take.** M3c-b's entry says
  outright that it *"does not close until §7.3's checklist is run"*, and §7.3
  item 6 is the criterion §7.4 and §7.5 both inherit: *"In combat, `lit now`
  names **1–2** abilities and every reason holds up. If it sits at 4+, tighten
  the RULES in `HudScore` — do not touch a colour."* But `lit now` is a
  **snapshot you have to type mid-pull**, and `/cdmp probe` recorded capability
  facts (secrets, cast phases, overrides) with **no dot-score history at all**.
  So the exit criterion of three milestones was being answered from memory,
  after the fight, about a line nobody could read while it mattered.

  **This is the shape §7.2 item 16 already diagnosed and fixed once.** Six probe
  commands collapsed into one always-recording report because *"each had to be
  toggled BEFORE the interesting thing happened — the wrong shape, because
  procs, transforms and secret reads cannot be scheduled"* (`Probe.lua`'s
  header). Strictness is the same class of thing: it is a property of the
  **moments you were busiest**, which are precisely the moments you were not
  typing. **The same fix, pointed at the score.**

  **What shipped (v0.16.0):**

  - **R1 — `HudLog.lua`, the recorder.** Two structures, and the split is the
    whole design. **`events`** is a ring of ~256 **TRANSITIONS**, written only
    when something *changes* (`{ t, kind, text }`, kind ∈ `dot` `ready` `mode`
    `cap` `cast` `seed` `combat`). **`hist`** is a **HISTOGRAM of the lit
    count**, bumped on every `S.Recompute` while in combat.
    - ⚠ **A histogram, not an average, and that is the point.** §7.3 item 6 asks
      whether the board *sits* at 4+. A mean hides a board that is quiet 90 % of
      the time and lights five dots during every Tyrant window — the exact
      failure mode "strictness" is about. The distribution answers it; one number
      does not. The readout states the verdict rather than leaving it to a
      feeling.
    - ⚠ **Sampling and transitions do not share a path.** A transition costs a
      `table.concat` of the reasons; a sample costs one integer increment, and
      `Recompute` runs at 4 Hz *plus* every edge. `HudLog.Sample` returns true
      only on a **new peak** — and only then does the caller pay to build the
      peak set's reason strings.
  - **R2 — the hook is inside `S.Recompute`, not a new ticker.** The per-item
    transition compares against `S.score[key]` *before* the assignment (that
    slot still holds the previous score), and fires on a move of the level or of
    `soon`/`projected` — the last two change what the dot *claims* even when the
    level doesn't. Losing a dot entirely is logged too: that is what an
    unrecognised override looks like. Every name goes through **one** live-identity
    resolver (`S.LiveName`, shared with `PrintStatus`) — ⚠ naming the base here
    is what printed *"Grimoire: Fel Ravager — use on cooldown"* over a Devour
    Magic button (B1), and **a log written to measure that bug must not
    re-introduce it**. Six more one-liners on paths that already existed:
    `combat` (the `PLAYER_REGEN_*` branch — pull boundaries), `mode` (in
    `S.PaintRail`, **above** the `rail = false` early-out, because mode is state
    and turning the widget off must not turn the measurement off — §7.5 item 4),
    `cap` (the glitter edge, now reporting **edge vs. glitter vs. suppressed** —
    §7.5 item 5), `cast` (`shards N ->~M` with a real timestamp — §7.3 item 5),
    `seed` (what a `/reload` or a combat exit actually seeded — §7.4 items 1/3),
    and `ready` (the `Available` / `OnCooldown` arms — **the GCD trap**, §7.4
    item 2, which is a *timing* defect and needs timestamps to see at all).
  - **R3 — auto-capture at pull end.** On `PLAYER_REGEN_ENABLED` the pull closes
    and its summary is appended to a ring of the last **5 pulls** in
    SavedVariables. **Nothing is typed and nothing is printed** — that *is* the
    milestone; a recorder you have to ask for is the problem, not the fix.
    Closed **last** in the handler, after seeding and the PREP repaint, so the
    combat-exit seed and the flip out of SPEND land inside the pull they belong
    to. ⚠ **Stored STRUCTURED, not through the capture buffer**: `ns.Print`
    writes to `DEFAULT_CHAT_FRAME` unconditionally, so driving
    `BeginCapture`/`EndCapture` at every pull end would dump the whole report
    into chat every time you left combat. A table goes into `ns.db.pulls`, so
    `CDMProbeDB.pulls[3].hist` reads perfectly off disk. ⚠ **The `/reload` flush
    trap is unchanged and is restated in the readout every time** — a stale file
    looks exactly like a recorder that silently did nothing.
  - **R4 — the readout.** `/cdmp hud log` (`hud log all` for the ring) renders
    duration, the histogram as a line (`lit 0:41% 1:33% 2:19% 3:6% 4:1%`, with
    4+ buckets coloured), the **peak set with its reasons**, and the event tail.
    Folded into `/cdmp probe` beside `PrintStatus`, so one report still has
    everything and the OOC-then-combat workflow is unchanged.
  - **R5 — §7.2 item 5, made diagnosable off disk.** `B.Explain()` already built
    the full slot → command → key reverse index and `hud binds` already rendered
    it; it was simply **never in the captured report**. Now `/cdmp probe` section
    **E**. ⚠ **A fourth failure mode, found in source this session:**
    `GetBindingKey(cmd)` returns **two** keys (primary *and* secondary) and both
    `scan()` and `B.Explain()` only ever took the first — so a player who
    remapped the **secondary** binding saw no change and there was **no row that
    said why**. Both are recorded now. Whether the resolver should ever *prefer*
    the second is a separate question: this makes the loser visible, it does not
    change the winner.
  - **R6 — docs.** `guidance-model.md` **§0.5.8.9** closes §7.1's P2 residual as
    **one dated amendment rather than 18 edits**: `IsShown()` reads as the
    primary mechanism at ~18 sites and it is not — the primary is the **aura
    edge**, and `IsShown` is a capability-checked backstop that is *constant-true*
    when the viewer isn't set to hide inactive items. Same pattern §0.5.8.6 /
    §0.5.8.7 / §0.5.8.8 already use for this exact class of problem.

  **Deliberately NOT in scope: C6's on-screen scrolling terminal** (§7.1 C6,
  §0.5.8.7 §5). `BucketBinds`' `Console.lua` solves the hard parts and remains
  the reference — but **you cannot read a scrolling log while playing either**,
  so it would be a second widget needing a second in-game pass. That is the
  M3c-c1/c2 lesson applied again. **The target is disk.**

  **Also not in scope: tuning `HudScore`.** M3e produces the measurement; acting
  on it is the next milestone's work, **on evidence**. Doing both at once would
  mean tuning the rules against a number produced by the same session that
  invented it.

  ⚠ **Numbering:** **M3e**, continuing the M3 state-layer family (M3b readiness
  → M3c-a the dot → M3d where readiness *starts* → **M3e whether any of it is
  true**). M5/M6/M7 stay spoken for.

- **M4 — Burst window.** *(Was "Burst window + the napkin engine". **The napkin
  engine shipped early, in M3c-a (v0.10.0)** — `HudNapkin.lua`, one uniform
  `SOON_LEAD ≈ 3 s`, because anticipation turned out to be load-bearing for the
  dot score rather than a burst-only concern. What remains here is the burst
  **framing** and the **two-lead Tyrant telegraph** (#11), which the uniform lead
  deliberately does not cover.)* Builds §0.5.8.3 rows **#9, #10, #11,
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
    out, off the same `GetSpellBaseCooldown` engine — **which is now built**
    (`HudNapkin.lua`, M3c-a); what's left is the per-ability lead tuning and the
    suppression rule below, not the engine. The **Dreadstalkers ping
    suppresses when Tyrant is imminent** and becomes a "stage for Tyrant"
    treatment: one Dreadstalkers per cycle is held so the dogs are fresh *inside*
    the window. Implosion's ping is gated on `in_aoe` (§7) and says "it's
    available", never "it's worth it" — the ≥6-imp value gate stays a **Can't**.
  - **Burn-phase sequence queue (NEW, 2026-07-21 — §7.2 item 9).** A staged hint
    for the Tyrant window that **drops abilities as they're pressed**. The
    consumed-as-you-press queue is currently specced **only for the opener** (#8,
    M3c); this is the same machinery pointed at the burst window, so it is mostly
    reuse rather than new invention. Keep it on the right side of "inform, don't
    instruct" — it shows the *shape* of the window, it does not become a
    press-this-next oracle (§0.5.8.7).
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
      ⚠ **RE-OPENED IN PRACTICE (2026-07-20, v0.10.0) — this assumption is now
      LOAD-BEARING, not background.** `HudNapkin` rides on it, and the napkin
      carries the feature the user rates highest ("firing cooldown abilities as
      soon as they are up is probably going to be the biggest win"). If `SUCCEEDED`
      spellIDs read secret in a raid, **anticipation degrades to nothing in exactly
      the content it matters most in.** The assumption is not re-opened as a
      *blocker* — the code degrades honestly rather than faking — but it is now
      **instrumented**: `HudNapkin` records readability and `/cdmp hud status`
      prints `napkin: live | unavailable | not probed`. **Check it inside a raid or
      M+**, not just at a dummy. Closing this for real needs one raid pull, and it
      is the cheapest high-value verification left on the board.
- [ ] **`in_aoe` predicate** — can we cheaply determine multi-target context
      (target count / recent multi-hit) to gate the Implosion approach ping (#12)
      and the Wild Imp "/6" readout (#17)? Flagged in §0.5.8.2(c) / §0.5.8.3; the
      AoE cues have no honest trigger until this is answered. Nameplate-count and
      recent-multi-hit heuristics are the candidates.
- [x] **Is cooldown state readable OUT OF COMBAT?** — **ANSWERED YES
      (2026-07-21, v0.12.0 probe): 13/13 tracked spells readable out of combat,
      0/13 in combat (`<secret fields>`).** Open-world both runs, so the gate is
      **combat**, not instancing. This is the M3d green light. ⚠ **Residual:**
      every OOC read was `duration=0` because nothing was on cooldown, so we have
      proven the fields are *readable*, not that a **mid-cooldown value is
      correct**. Confirm with one cast → leave combat → probe before building the
      seed. *(Original item:)* The §1
      capability table was captured **in combat, in a delve**, so the
      `GetSpellCooldown().duration` = `<secret>` row has never been checked in an
      unrestricted context. `/cdmp secret` in a city vs in combat answers it. This
      is the **entire gate on M3d** — a "yes" removes the `no edge seen yet` cold
      start; a "no" closes the milestone for free.
- [x] **Does the Wild Imp stack count exceed 9?** — **YES, ANSWERED
      2026-07-21: 10 observed directly, 11–12 reported anecdotally.** Combined
      with probe D below, this **closes the dot-glyph font for good** (§7.2 item
      11): the count routinely reaches exactly the values that render as one or
      two dots, at the moment the player is most past the ≥6 gate. There is no
      variant of the idea that survives. *(Prior framing:)*
      ⚠ **Half-answered and the OTHER half went away (2026-07-21).** Probe D
      settled the mechanism question first: `Applications:GetStringWidth()` and
      `GetText()` **both error**, so there is no side channel to the digit count
      and the dot-glyph font (§7.2 item 11) has no rescue. The cap question now
      only matters if the cap is **≤9**; the player reports not exceeding 10 but
      it is unclear whether 10 was actually reached. *(Original item:)*
      (2026-07-21.) Cheap to eyeball on an AoE dummy pull. Two consequences: the
      dot-glyph font idea (§7.2 item 11) is **un-parked only if the count caps
      below 10**, and if Blizzard hides the text at 1 then the "/6" readout
      silently starts at 2, which we should know rather than discover.
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
- [x] **Should the opener ever ship a second variant (build-to-5)?** — CLOSED
      (2026-07-21, feedback pass): **scrubbed.** There is one opener. The old
      "1a/1b" split was a speculative contingency WCL structurally can't show
      (logs start at the pull, hiding a pre-stack), never authored, and the naming
      leaked into the code + docs as if two openers existed. If the opener ever
      needs revising, we revise the one `ns.SpecOpener` table — no variant
      machinery, no fill-to marker (the opener enters shard-poor by design).
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

---

## 7.1 Working backlog — the M3b → M3c carry-over (2026-07-20)

> **Why this block exists.** Between shipping v0.8.2 and v0.9.1 a design
> conversation, a Fable fidelity review, and three in-game passes produced more
> decisions and corrections than any one of the four docs owns. Parked here so
> nothing evaporates. **Items D1–D3 are user decisions that gate the code below
> them** — do not "use best judgement" and proceed on them.

### Decisions pending (these gate the rest)

- [x] **D1 — RESOLVED (2026-07-20): SHELVED in favour of the dot.** The dot
      addresses the same need without loading a fifth meaning onto a contested
      channel. ⚠ **But the overclaim must still be fixed** — §0.5.8.3 #5 is
      re-scoped to CD-bearing buttons and `spec.md` §3's "bright = ready/actionable"
      is wrong as written. Shelving the fix is not permission to keep the promise.
      Reasoning preserved below as the reopening path. *(Original item:)*
      **Adopt cadence-routed luminance?** *(Fable blocking error B1.)*
      §0.5.8.4 commits `block.luminance = BRIGHT if ready else DIM` board-wide and
      `spec.md` §3 promises "bright = ready/actionable". Finding #5 falsifies it:
      HoG and Demonbolt have **no cooldown**, never fire a ready edge, and sit at
      base luminance forever — and they are the **#1/#2 most-pressed** buttons
      (729/541 pooled casts). So the top of the [V3] salience hierarchy is mute on
      the buttons the rotation is actually about. Proposed fix: **cadence routes
      which actionability source feeds luminance** — `oncd` → observed ready edge
      (shipped), `gated` → readable resource gate (HoG bright at shards ≥ cost),
      `reactive` → proc presence. Restores one board-wide meaning: *bright =
      actionable now*. Also rescues §0.5.4 **moment #5**, which currently has no
      home in the §0.5.8.3 table. **New committed behaviour → M3c.**
- [x] **D2 — RESOLVED (2026-07-20): a four-level threshold ladder**, NEVER /
      AVAILABLE / ROTATION / LATE. **All four are precise** — LATE is *measured*
      from the observed `Available` edge with `GetTime()`, not estimated, so it
      does not inherit the napkin's drift. **Anticipation is orthogonal, not a
      fifth level**: the dot stays at NEVER and fills as the napkin approaches, so
      it never claims pressability and never needs filtering out. Full model in
      §0.5.8.7 §1. *(Original item:)* **Candidate scorer: shape and inputs.**
      (a) **stack-rank** the candidates (more useful, and wrong ordering erodes
      trust faster than no ordering) or just **threshold** them into a live set?
      (b) may the score consume **napkin timers**? They give burst awareness but
      drift on haste/CDR, and would be the least reliable input in the mix.
      Recommendation on file: build on the four *precise* inputs first (shards,
      runtime cost, Core presence, observed ready edges), ship, and add
      napkin-derived urgency only if it doesn't already narrow to 2–3.
      ⚙ **That staging was OVERRIDDEN at build time (v0.10.0), on the user's
      call:** *"firing cooldown abilities as soon as they are up is probably going
      to be the biggest win from this tool. I believe that requires signaling me
      early that they're going to be ready."* Correct — without anticipation the
      dot flips NEVER → ROTATION at the *instant* the cooldown lands, which
      mid-GCD is already too late to weave. So the napkin shipped **in** M3c-a
      rather than being held for a second pass. **The four levels stay precise**:
      the napkin drives only the anticipation *treatment*, which never claims
      pressability, so a wrong estimate makes the HUD early — never wrong about
      what you can press. Implemented as `HudNapkin.lua`; its three honesty rules
      are in the §6 M3c-a entry.
- [x] **D3 — RESOLVED (2026-07-20): YES, conservatively.** Not the full ability
      name; compact tokens; row reads **dot first, then the reason for the dot**.
      Text carries identity/reference, preattentive channels carry urgency
      (§0.5.8.7 §3). *(Original item:)* **Promote the debug words into the default view?** The terminal
      aesthetic and a text readout are complementary, and always-on identity text
      makes the colour map self-teaching (the direct answer to "yellow and purple
      don't mean anything in isolation"). But §0.5.8 currently **excludes** text
      from the indicator contract (`HudDebug.lua` header says so explicitly), so
      this is a scope change, not a tweak. Standing recommendation: **text carries
      identity/reference, preattentive channels carry urgency** (§0.5.3 — reading
      is serial and slow; a P0 cue must land without a saccade).

### Code

- [x] **C1 — ✅ DONE (v0.10.0). `SpecDemonology` two-axis rewrite** — and the framing is
      confirmed: this *is* the per-ability **signal bucket** the dot score reads. Replace the single `role` enum
      with `spends` / `generates` / `cadence` / `burstAlign` / `goGate` / `kind`,
      per the corrected table in the Fable review. Key corrections to the original
      proposal: `cadence ∈ {oncd, gated, reactive, filler, utility}` — **`burst`
      is dropped** (redundant with `burstAlign`) and **`filler` is added** (Shadow
      Bolt is the else-branch and classifies as nothing else); **Grimoire also
      needs `burstAlign`**; **`goGate` is a separate bit** because the go-gate is
      Tyrant + Dreadstalkers *only* and without it someone re-derives the lane from
      `burstAlign` and re-ships §0.5.8.6 blocking error #2; **`generates` subsumes
      the existing `ghost` field** rather than duplicating it; buff-viewer rows get
      `kind = "aura"` instead of a magic `role = "proc"`. **Costs are NOT authored
      here** — they are talent-dependent and read at runtime (v0.9.1).
- [x] **C2 — ✅ DONE (v0.10.0). DOWNGRADED (dot-led world makes the tint less load-bearing), but
      still a live contradiction and a one-line data fix. Fix the Demonbolt tint pole** *(Fable blocking error B2 — a live
      defect in shipped code).* §0.5.1 calls Demonbolt a bucket-2 **spender**;
      `SpecDemonology.lua:66` says `role = "builder"` and renders it at the
      cool/dim generator pole. So `HoG ↔ Demonbolt` — the most common pattern in
      the parse data (313 + 313 two-grams) — renders as **opposite tint poles**, as
      if they were opposite kinds of action when both are "dump a bucket". Related
      tell: `HudChrome.lua:53-54` gives `spender` and `burst` **identical** tint
      values, i.e. `burst` never affected the tint at all and existed only to
      smuggle burst-lane membership through the tint field.
- [x] **C3 — ✅ DONE (v0.10.0), pending in-game review. Candidate scorer +
      standalone dot.** *(D2 resolved — build to the four-level ladder.)* A per-ability
      score from readable inputs, surfaced as a **standalone pulsing dot** beside
      the icon. Architecturally the dot is the right call: the review established
      there is **no free visual channel** (hue = group, saturation = resource,
      luminance = actionability, alpha = recede), and a dot is a *new object*
      rather than a new channel on a crowded one. It can also carry its own
      **confidence** (solid = precise inputs only; hollow/dim = leaning on a
      drifting napkin), which a border cannot express.
      ⚠ **One of the proposed inputs is not available:** "almost capped on Demonic
      Core" is a **secret** (§0.5.5 — count is displayed but unreadable, "cannot
      signal near cap 4"). Same wall as imp count: we get *presence*, never
      *quantity*. A score that treated "has a Core" as "about to overcap" would be
      confidently wrong, which §0.5.8.2(c) forbids. Five of the six proposed
      buckets survive.

- [x] **C4 — Monospace font + larger text — ALREADY SHIPPED (v0.8.2).** JetBrains
      Mono bundled (OFL included) with a stock-font fallback; size 11 → 14. If it
      still reads small, bump `SIZE` in `HudRow.lua` (renamed from `HudDebug.lua`
      in v0.10.0) — worth making a setting.
- [x] **C5 — ✅ DONE (v0.10.0). The per-icon row becomes `DOT + why`.** The row states the bucket
      facts that *determined* the dot's level, so the score is **auditable rather
      than an oracle** — which is what keeps it on the right side of "inform,
      don't instruct". Supersedes the current debug row format.
- [ ] **C6 — Scrolling terminal view below the column.** Still deferred — explicitly
      out of scope for M3c-a, recorded so it isn't lost (§0.5.8.7 §5). Practical readout *and* period flavour, and the
      natural home for log-shaped data the per-icon rows can't hold.
      `BucketBinds`' `Console.lua` already solves scrollback + geometry + font.

### Docs

- [x] **P1 — DONE (2026-07-20): §0.5.8.7 written.** Covers the governing
      principle, the dot score + level ladder, the #5 shelving, text promotion, the
      signal-bucket rewrite, and the deferred terminal view. *(Original item:)*
      **Write §0.5.8.7, a dated amendment block** (in the pattern of
      §0.5.8.6, so the committed table stays the single contract). Contents: the
      `role` → two-axis split; **#5 re-scoped** to "ready accent on **CD-bearing
      buttons**" (it structurally cannot cover the board); the Demonbolt tint-pole
      flip; **cadence routes, it does not paint**; the tri-state `ready = nil` (the
      committed pseudocode still says binary `BRIGHT if ready else DIM`, which the
      shipped M3b contradicts); and the governing principle below.
      **New governing principle to record — "inform, don't instruct":** the HUD
      narrows the field rather than choosing. *"There will still be decision
      making, but it will be focused decision making — pick between 2-3 abilities
      instead of 5."* This resolves several open tensions at once and should be
      checked against the instructional rows (#8 opener queue, #11 HOLD/BANK, #12
      "stage for Tyrant"), re-framing them as information rather than dropping them.
- [x] **P2 — FULLY DONE (residual closed 2026-07-21, M3e).** The load-bearing
      citations were fixed inline on 2026-07-20 (`spec.md` §3 Ready row + proc
      rows; §0.5.2 #8; §0.5.4 #8). The residual — the ~18 `IsShown()` mentions in
      §0.5.2 #2/#6/#7/#10, the §0.5.4 rows and §0.5.8.4's pseudocode, all reading
      as though `IsShown` were the **primary** mechanism — is closed by
      **`guidance-model.md` §0.5.8.9**, as **one dated amendment rather than 18
      edits**: the primary is the **aura edge** (`TriggerAlertEvent`), and
      `IsShown` is a capability-checked backstop that is *constant-true* whenever
      the viewer isn't set to hide inactive items. Same pattern §0.5.8.6/7/8
      already use for this class of problem, and it keeps the rows legible rather
      than silently rewritten. *(Original item:)* **Sweep the dead-mechanism citations** *(Fable blocking error B4).*
      `spec.md` §3's "Ready" row and `guidance-model.md` §0.5.2 #8 / §0.5.4 #8 all
      still name **`OnCooldownDone` / `TriggerAvailableAlert`** — and
      `hooksecurefunc` on `OnCooldownDone` is a **proven silent no-op** (`notes.md`
      §1, the `GenerateClosure` trap). Anyone implementing from the authority docs
      reproduces the exact trap M3b dodged. Same sweep: §0.5.2 #2/#6/#7/#10,
      §0.5.4's rows, and §0.5.8.4's `DemonicCore.IsShown()` all cite unqualified
      `IsShown()`, which is a **conditional, capability-checked backstop**, not the
      primary — the primary is the aura edge.
- [x] **P3 — DONE (2026-07-20):** Status block rewritten with the v0.7.0→v0.9.1
      arc and the M3b known-risk closed. *(Original item:)* **Milestone-log catch-up.** The Status block and M3b
      entry stop at v0.7.0 while citing results from passes after it. Record: the
      **recede `Wake` dead-end** (v0.7.0 shipped it so the first ready edge or proc
      killed the recede permanently — nothing re-armed the sleep); the **LOUD pass**
      (explicitly *not* considered-final values, all in one TUNING block); the
      **`/cdmp hud debug` words-first readout** and what prompted it; **#17 pulled
      forward from M5 into M3** and why; **runtime power costs** (v0.9.1); and
      **close the M3b "Known risk"** — `TriggerAlertEvent` is confirmed live (20
      hooks, edges firing, `secret=0`). Also fold in finding #5 (readiness covers
      only a minority of buttons) as a first-class scoping fact.

### Verify in-game

- [ ] **V1 — Open verification queue. Carry this over BEFORE anything M3c-a —
      it is cheap and (a) now gates trust in the whole dot score.** (a) **Costs** —
      read the `cost` column (v0.10.0 prints both the normalised shard figure and
      the raw one, e.g. `cost 1 shard(s) [raw 10]`) and settle Dreadstalkers /
      Tyrant / Grimoire; the docs, the review and the player disagree, and all
      three are talent-dependent. The units caveat (shards vs fragments) stopped
      being trivia in v0.10.0: **the gate rule is `shards >= cost`, so if costs
      read wrong, the gate logic is wrong** and every dot derived from it is wrong.
      `ns.ShardCost` normalises a clean multiple of 10 down to whole shards (the
      cap is 5, so nothing can legitimately cost ten) — this line confirms or
      falsifies that heuristic.
      ✅ **(a) ANSWERED 2026-07-21, and the answer was a defect** — see the Status
      block and §7.2 item 1. Costs read wrong, but **not** for the reason this
      item was watching: `ns.PowerCost` never filtered by power *type*, so mana
      costs were being compared against the shard count. The fragment heuristic
      itself is still **unproven for real shard costs** — it has only ever been
      exercised on mana figures, where it silently "worked" (5000 → 500) and
      produced the bug's signature numbers. Re-check the raw column for
      Dreadstalkers / Tyrant / Grimoire after the type filter lands; (b), (c) and
      (d) remain open. (b) **Imp stack emphasis** (v0.9.0) restyles a
      Blizzard `FontString`, and Blizzard re-applies text/position from several
      paths — the same problem that forced the leaf-method hooks now dormant in
      `HudTint.lua`. If the number snaps back mid-combat, that's why. (c) ✅ **CLOSED 2026-07-21** — #3 Demonic Art
      **observed for the first time**: 12 override events in one dummy session,
      the HoG glow lit at strength 1.00, and the pairs disambiguated Ruination
      (`434635`) and Infernal Bolt (`434506`). See `notes.md` §1. (d) The recede
      actually receding, post-fix.

> **Outside this project (KB bugs surfaced by the review, not HUD work):**
> `knowledge/classes/warlock/demonology/rotation.md` still opens with Power Siphon
> (#1) and Summon Doomguard on cooldown (#4) — `diabolist-sequences.md` explicitly
> queued that correction and it was never applied, so the priority list a reader
> hits first is the stale one. And `abilities.md`'s Infernal Bolt **+2** shards
> conflicts with `maxroll-raid.md`, `diabolist-sequences.md` and the parse counts,
> which all say **+3** — the ghost math and the SPEND pre-flip threshold ride on it.

---

## 7.2 Working backlog — the v0.10.0 feedback pass (2026-07-21)

> **Why this block exists.** The first real in-game review of the dot score, in
> the user's words, at a Silvermoon dummy. Same purpose as §7.1: park everything
> so nothing evaporates between a play session and a build. Items 6–10 are already
> written into their milestones above (M3c / M3d / M4); they are restated here in
> one list so the pass is legible as a pass.
>
> **The through-line:** every finding here is the dot **stating something false**
> rather than something incomplete. That ordering is deliberate — a HUD that says
> "I don't know" is within contract (§0.5.8.7); one that says `NEVER` about a
> ready Tyrant is not.

### Small — just do

*(Items 1–4 shipped in **CDMProbe v0.11.0**, 2026-07-21 — not yet run in-game.
Item 5 is deliberately still open: it is *diagnosed by* item 4, not fixed by it.)*

- [x] **1 — Filter `ns.PowerCost` to Soul Shards** (`Util.lua:98`). It returns the
      first non-zero cost of **any** power type, so mana costs land in the shard
      gate. Root cause of *both* "Demonbolt is never recommended" and "why is
      Mortal Coil counting shards". Hand of Gul'dan works today only by luck of
      list ordering. Treat "no shard-cost entry" as free — and keep §0.5.8.7's
      distinction intact: `ns.PowerCost` still reports "genuinely free" and
      "unreadable" identically, which `HudScore`'s gated branch already guards.
- [x] **2 — Short-circuit `cadence == "utility"` before the resource gate** in
      `HudScore.For`. The gate is evaluated first, so a costed utility ability
      exits at `NEVER` and never reaches "utility — your call". Ship with item 1:
      the type filter alone would leave the ordering bug latent behind it.
- [x] **3 — Imp-count typography.** Point **both** `Applications` and our `/6`
      suffix at the bundled JetBrains Mono (they currently match only because both
      read Blizzard's saved `st.font` — change one and you get a mismatched
      `4/6`), bump `STACK_SIZE` 22 → ~30, and hoist `HudRow`'s font-load fallback
      into `Util.lua` so both callers share it. `SetFont` returns false on a failed
      load and the stack path has **no** guard today, i.e. a font miss renders the
      count *invisible* — strictly worse than ugly. Monospace is the right call
      independent of taste: a fixed-width digit stops the number jittering
      horizontally as imps come and go.
- [x] **4 — Add `/cdmp hud binds`** — per tracked spell: slot → binding command →
      raw key → shortened string. Gates item 5. ⚠ **Its output still had to be read
      LIVE**, which is the same scheduling problem `/cdmp probe` exists to delete —
      closed in v0.16.0 by putting the reverse index into the captured report.
- [x] **5 — DIAGNOSABLE OFF DISK (2026-07-21, v0.16.0).** Not *fixed* — it can't
      be, it depends on your actual bars — but the evidence now lands in the
      captured report as `/cdmp probe` **section E**, so it is answerable after the
      fact instead of having to be read live. ⚠ **A fourth candidate was found in
      source:** `GetBindingKey(cmd)` returns **two** keys and both `scan()` and
      `B.Explain()` only ever took the first, so remapping the **secondary**
      binding changed nothing and no row said why. Both are recorded now (the
      *winner* is unchanged — that needs the evidence first). Read one of four
      answers off the report: two slots with the lower marked `<-- used`, a
      `cmd=none` row, no rows at all, or a populated `2nd=`. *(Original item:)*
      **Keybind remap not picked up.** Not diagnosable from source; the wiring
      (`UPDATE_BINDINGS` → debounce → rescan → `RefreshKeybinds`) reads correct.
      Three candidates: **first-bound-slot-wins** (a spell on two bars keeps bar
      1's key regardless of what you remapped elsewhere); the **unmapped slot
      ranges** 13–24 and 109–180, absent from `SLOT_BARS` by design and therefore
      invisible to us; and **macro slots**, where `GetMacroSpell` returns nothing
      for conditional/modifier macros. Diagnose with item 4 rather than guessing.

### Milestone edits (already written into §6)

- [ ] **6 — Score the live identity, not the base spell** → **M3c**. The Grimoire
      reads as a rotational summon while a spell override has it transformed into
      a pet command. Opposite convention from keybinds, on purpose.
- [ ] **7 — Spend-side anticipation** → **M3c**. Project the cost on
      `UNIT_SPELLCAST_START`; the shipped layer only ghosts *incoming* shards.
- [ ] **8 — "Ready but unaffordable" ≠ NEVER** → **M3c**. First consumer of
      `goGate` / `burstAlign`, which nothing reads today.
- [ ] **9 — Burn-phase sequence queue** → **M4**. The opener queue's machinery
      pointed at the Tyrant window.
- [ ] **10 — Out-of-combat seeding** → **M3d (new)**. Probe before code; the probe
      is the §7 open question added the same day.

### Parked

- [x] **11 — A dot-glyph font for the imp count — ❌ CLOSED, NOT PARKED
      (2026-07-21).** Both escape hatches are gone: probe D found
      `GetStringWidth()`/`GetText()` **error**, so there is no side channel to the
      digit count; and the count **does exceed 9** (10 observed, 11–12 reported).
      The reopening condition written below — "reopens if the cap is below 10" —
      is therefore falsified rather than pending. Do not re-propose this; the idea
      is sound and the game will not cooperate. *(The design, preserved because
      the TECHNIQUE generalises to any secret count that happens to be small:)* Author a .ttf where each digit
      renders as N dots **and** carries an advance width of N × a fixed pitch
      (that second half is load-bearing — it is what makes dot *k* of `4` land on
      dot *k* of `6`); draw a static 6-dot backdrop in an unlit colour and let
      Blizzard's own `Applications` fontstring overlay it in a lit one. Full
      coverage = gate met. **Genuinely the only way to convert a Secret Value into
      an analog readout** — the count never enters Lua, the *glyph* carries the
      meaning, so it is display-side and taint-free — and it generalises to any
      secret count (Demonic Core's cap of 4 is the obvious second customer). The
      signal is **coverage, not hue**, so it survives colour-blindness where a
      red/green pair would not.
      **Parked on three things:** (a) **double digits misread low** — `10` renders
      as `1`+`0` = one dot, and WoW's font path does no OpenType shaping, so a
      `10` → ten-dot ligature cannot save it; 7–9 degrade *gracefully* by
      overflowing the backdrop, so the failure is specifically 10+ and it fails
      **toward "not ready" while sitting on a huge pile** — a false negative on the
      exact decision the readout exists for, which §0.5.8.2(c) forbids; (b) it is
      unproven that WoW's FreeType loads a hand-built TTF at all (cheap to detect
      — `SetFont` returns false — but the fallback must actually be wired, cf.
      item 3); (c) it **promotes the `Applications` leaf-method hooks from optional
      to required**, since two overlaid fontstrings only register if they share an
      origin and Blizzard re-applies position from several paths (V1(b)).
      **Reopens if** the Wild Imp aura turns out to cap below 10 (§7).

### Instrumentation — `/cdmp probe` (v0.12.0, 2026-07-21)

- [x] **16 — Six probe commands collapsed into one, and it writes to disk.**
      `dump` / `secret` / `casts` / `log` / `layout` / `shards` each answered one
      question and each had to be **toggled before the interesting thing
      happened** — the wrong shape, because procs, transforms and secret reads
      cannot be scheduled. Now everything passive records **from load** (counters
      + short ring buffers, no printing) and `/cdmp probe` renders the lot into a
      **captured report**, read off disk at
      `…/WTF/Account/<ACCT>/SavedVariables/CDMProbe.lua` → `CDMProbeDB.reports`.
      No more screenshots or paste. `Layout.lua` and `Probes.lua` deleted (the
      layout question is long resolved; the rest moved). ⚠ **SavedVariables only
      flush on `/reload`** — skipping it leaves the *previous* session's text on
      disk, which is indistinguishable from a probe that did nothing.
- [x] **17 — ✅ ANSWERED (M3d is GO). Probe A: cooldown readability per tracked spell.** The **entire M3d
      gate**, and printed per spell rather than for a sample of three, because
      "readable for some spells" is a real possible answer (the GCD is
      whitelisted) and a small sample can't tell that apart from "readable for
      all". Diff the OOC report against the in-combat one.
- [x] **18 — ✅ ANSWERED (and it found the Grimoire). Probe B: override / transform capture.** Two *independent* reads of
      the same question, because they can disagree and **the disagreement is the
      finding**: the passive event count, and the live base-vs-`GetSpellID()`
      divergence. If a button is visibly transformed while the event count is 0,
      then the override event is **not** the mechanism for it and §7.2 item 6 must
      poll identity rather than trust the event — which is exactly the Grimoire
      case. Also finally distinguishes V1(c)'s "never observed" from "never
      watched": `HudState` only listens while the HUD is **on**.
- [x] **19 — ✅ ANSWERED (all four phases readable). Probe C: cast readability PER PHASE.** `SUCCEEDED` carries the
      shipped napkin; `START` carries the spend-side anticipation (item 7) and has
      **never been counted separately** — the status block only ever reported
      SUCCEEDED. A phase reading secret while the other doesn't is the most
      consequential thing a raid run can turn up.
- [x] **20 — ✅ ANSWERED: CLOSED. Probe D: the imp-count side channel.** Does
      `Applications:GetStringWidth()` read non-secret? If so it exposes the
      **digit count** (not the number) — and "2 digits ⇒ ≥10 imps ⇒
      unambiguously past the ≥6 gate" is precisely the fact that parked the
      dot-glyph font (item 11). ⚠ **Probe only.** If it reads real, do **not**
      build on it before a deliberate review: a width derived from a secret may
      still taint on comparison, and Blizzard may treat it as a leak to close.
      Record the fact, don't spend it.

### Work items the probe ADDED (all land in M3c-b)

- [ ] **21 — The secret-ID guard (B2).** `type()` does not reject a Secret Value,
      so identity resolution poisons the registry. Guard at the source; an
      unreadable ID means "keep what you had". `notes.md` §1.
- [ ] **22 — Split the `other` alert counter (B3)** into *unhandled type* vs
      *handler threw*. 47 errors hid in a readout we have been reading for five
      passes.
- [ ] **23 — LATE must not accrue out of combat (B6).** Caught live: Hand of
      Gul'dan at *"LATE · waiting 7s"* in a city. A nag with nothing to nag about
      trains you to ignore the channel.
- [ ] **24 — Identity must be POLLED, not just evented (B1).** The override is
      set before we start listening (login / `/reload` / mid-session enable), so a
      missed event and an absent event are indistinguishable. Bind-time polling is
      the floor; the event is the fast path. *(Corrected — the first reading of
      this evidence blamed the button, not the window. `notes.md` §1.)*
- [~] **25 — Reopen the Shadow Bolt → Infernal Bolt blind spot** (§0.5.5,
      M5/M7 scope, **not** M3c-b). The override event fires for SB even though SB
      is not in the tracked set, so we *know* when that Art arms — we just have no
      icon to light. Previously recorded as a permanent Can't; it is now a
      layout/curation question, which is exactly what M7's curated layer-①
      override exists for.

### Verify in-game

- [ ] **12 —** V1(a) is answered; the **fragment heuristic is still unproven for
      real shard costs**. See the §7.1 annotation.
- [ ] **13 —** Does the imp count exceed 9, and does it display at 1? (§7.)
- [ ] **14 —** Napkin readability **in a raid** — unchanged, and still the highest-
      value open check on the board (§7).
- [ ] **15 — Re-measure strictness after the cost fix.** The pre-fix `lit 2` is not
      evidence: gates were falsely closed across a chunk of the board, so the
      count was suppressed by a bug rather than by tight rules.

## 7.3 Verify in-game — the M3c-b truth pass (v0.13.0, 2026-07-21)

**This checklist is the milestone.** M3c-b shipped no new signal, so there is
nothing to look at and admire; the only thing that closes it is a dummy pass
where the board's opinion survives being argued with. Run it in order — the last
item depends on the ones above it being true.

Deploy first (a push does **not** reach the game): commit → `gh release create
v0.13.0` → `ghaddons update michac/CDMProbe` → `/reload`. Then `/cdmp probe` +
**`/reload`** so the report is readable off disk at
`…/WTF/Account/LLOYDCHRISTMAS/SavedVariables/CDMProbe.lua`.

- [ ] **1 — B1, the headline.** Let a Grimoire go on cooldown so the button
      becomes **Devour Magic**. Its dot must go dark/dotless while it reads Devour
      Magic, and `lit now` must **not** name it. This is the defect that motivated
      the whole milestone; if it still fires, nothing else here matters.
- [ ] **2 — B1, the other half.** Proc a Demonic Art. The transformed Hand of
      Gul'dan must score as **Ruination** (`434635`) — a real rotational press —
      not as Hand of Gul'dan. The row should carry a `now Ruination` reason.
- [ ] **3 — B2/B3.** `other` and `errors` are reported separately, and **`errors`
      is 0**. A non-zero errors count after this milestone is a **bug, not a
      curiosity** — it was 47 hiding inside `other` before the split.
- [ ] **4 — B6.** Stand in a city with 3+ shards. **Nothing** promotes to LATE.
      Then pull: the clocks start fresh rather than carrying a stale timestamp
      into the opener.
      ⚠ **FOUND BROKEN by the M3e recorder, fixed in v0.16.1 (2026-07-21).** Both
      recorded pulls opened with every "use on cooldown" button at LATE on frame 1
      — peak set at +0.08s reading *"waiting 43s"* / *"waiting 19s"*, matching the
      idle time before each pull. Root cause: B6 gated the LATE *promotion* on
      `InCombatLockdown()` but not the `candidateSince` **stamp**, so the clock ran
      out of combat and the always-on `scoreTicker` re-armed it 0.25s after B6's
      combat-exit `wipe`. The stamp now shares the promotion's combat gate; the
      clock starts fresh from the first in-combat frame. **Re-run this AND item 6
      on v0.16.1** — the pre-fix strictness histograms are contaminated by the
      phantom LATE and don't count. This is the recorder catching a shipping bug a
      mid-pull snapshot never would (you'd have to type in the first 3s of a pull).
- [ ] **5 — B4.** Start a Hand of Gul'dan cast and watch the board **mid-cast**:
      the dots must reflect the **post-cast** shard state, the summary line should
      show `shards N ->~M`, and anything lit *because of* the projection must
      render **hollow** (and carry `~est` on its row). If the projection reads
      *low* rather than high, that is the documented residual — `atStart` sampled
      after the client already deducted; see the `HudState.ProjectedShards` header.
- [ ] **6 — THE EXIT CRITERION.** In combat, `lit now` names **1–2** abilities and
      **every reason holds up**. If it sits at 4+, tighten the RULES in
      `HudScore` — **do not touch a colour.**
- [ ] **7 — B7.** *Before* touching the CDM, `/cdmp hud` must warn that Shadow
      Bolt is untracked and say what that costs. Then nudge the CDM in Edit Mode a
      few times and confirm the warning does **not** re-spam. Then add Shadow Bolt
      manually: the warning clears, and **SB → Infernal Bolt should now light with
      no code change** (the `transform` rule resolves to wherever the override
      lands, and `ns.Spec` already carries a Shadow Bolt entry). Worth confirming
      rather than assuming.
- [ ] **8 — The standing raid check, unchanged.** All probe data is still
      open-world. **Cast readability is B4's entire foundation and has never been
      confirmed in a raid.** `hud status` reports it honestly; that report is the
      first thing to read if anticipation ever goes quiet in real content.

---

## 7.4 Verify in-game — M3d out-of-combat seeding (v0.14.0, 2026-07-21)

**One combined pass with §7.3, and §7.3 runs FIRST** — its exit criterion is a
strictness measurement, and a seeded board raises the number of abilities
eligible to be judged, so measuring it on the pre-seed board would flatter the
rules. Deploy once for both (a push does **not** reach the game): commit →
`gh release create v0.14.0` → `ghaddons update michac/CDMProbe` → `/reload`.

- [ ] **1 — THE HEADLINE.** Cast Summon Demonic Tyrant, then `/reload` while it
      is on cooldown. Its dot must show a **real countdown immediately** —
      `~42.1s (read)`, **solid** — instead of `NEVER · no edge seen yet`. This is
      the entire milestone; if it fails, nothing below it matters.
- [ ] **2 — The GCD trap.** Press any instant, then immediately look at the
      board. **Nothing that is genuinely ready may flip to on-cooldown** for the
      1.5 s global. This is the one bug that would look like the feature working
      while quietly lying about every button.
- [ ] **3 — The combat seam.** Pull. Reads go secret; the board must **keep** its
      seeded state rather than blanking, and `hud status` must say reads are
      *unavailable here* rather than implying the feature is on. Then leave
      combat: the board re-seeds, and anything sitting at
      `"should be up, unconfirmed"` resolves to a real number.
- [ ] **4 — Provenance is legible.** `hud status` distinguishes `(seed)` from
      `(edge)` per item, and the seeding block reports a live/unreadable verdict
      plus last-pass counts. This is also what keeps M3c-b and M3d separable
      inside one release.
- [ ] **5 — Re-run §7.3 item 6 on the now-seeded board.** `lit now` names **1–2**
      abilities and every reason holds up. **This is the honest place to measure
      strictness.** If it sits at 4+, tighten the rules in `HudScore` — **not a
      colour.**
- [ ] **6 — The context risk.** Reads are measured **open-world only**. Check the
      `hud status` seeding verdict in an **instance lobby** and in a **raid
      between pulls**. An `unreadable here` verdict is not a failure — it is the
      answer the line exists to give — but it tells us where seeding silently
      does less.

---

## 7.5 Verify in-game — M3c-c1, the shard rail + mode spine (v0.15.0, 2026-07-21)

⚠ **§7.3 and §7.4 must already have passed.** Every item here renders *on top of*
the scored board, so running this first measures decoration on a board that may
still lie — and M3d's seeding is what makes the rail honest at a cold start.

Deploy first (a push does **not** reach the game): commit → `gh release create
v0.15.0` → `ghaddons update michac/CDMProbe` → `/reload`.

- [ ] **1 — The rail exists and rides.** It sits under the `C:\>_` footer, at its
      own full width, **not clipped to the icon column**. Drag the CDM in Edit
      Mode and change Orientation / # Rows: the rail follows and nothing detaches.
      (This is the documented clipping hazard from `notes.md` §9 — one centre
      anchor, explicit width. If it comes out ~28 px wide, that's the trap.)
- [ ] **2 — Fill is honest.** Spend and generate: segments track shards, and the
      partial segment moves *between* whole shards — **or** `hud status` says
      fragments are unreadable here, which is an **answer, not a failure**. Whole
      shards remain the gate either way.
- [ ] **3 — The ghost head.** Start a Shadow Bolt / Infernal Bolt hardcast: an
      incoming segment appears **hollow** during the cast's dead air and
      solidifies on landing. Hollow must read the same here as it does on the
      dots — if the two treatments don't match, the confidence marker is broken,
      not the rail.
- [ ] **4 — The predictive flip.** A cast that will cross 3 shards flips the mode
      to **SPEND during the cast**, not a beat after it. This is `projected`, not
      `shards`, doing its job (§0.5.8.4:715).
- [ ] **5 — Cap is a warning, and it does not strobe.** Hit 5: the flip plus
      **one** glitter, reading "spend or waste". Then cap → HoG → cap quickly: the
      second glitter is **suppressed** by the ~2 s re-arm, and `hud status` counts
      the suppression while still counting the **edge**. If suppressions stay 0
      through that sequence, the throttle isn't wired.
- [ ] **6 — PREP is distinct.** Out of combat the rail and the terminal wear the
      calm resting tint — visibly **not** GENERATE. This is M3c-c2's foundation,
      shipped a milestone early so it gets exercised before anything depends on it.
- [ ] **7 — Mode is legible without colour.** Read the label alone, ignoring hue
      entirely: the mode is still unambiguous ([X1] — never colour-alone).
- [ ] **8 — Common fate.** Let the board go quiet: the rail recedes **with** it,
      and a proc wakes both together. Then hit cap while receded — **the flash
      must still be visible.** That is the frame-alpha trap; if the glitter is
      dim, the fx frame has become a child of the receded rail.
- [ ] **9 — Unreadable degrades honestly.** If shards ever read secret, the rail
      says **UNKNOWN** rather than drawing an empty bar. An empty bar is a *claim*
      ("you have no shards") and we would not know that.


## 7.6 Verify in-game — M3e, the pull recorder (v0.16.0, 2026-07-21)

> 📋 **`verify-runbook.md` is this checklist and §7.3–§7.5 re-ordered into the
> sequence you'd actually play them**, with exact commands, expected output and
> what a failure means. Read that while logged in; tick the boxes **here**.

**Run this FIRST, then §7.3 → §7.4 → §7.5 with the recorder on.** Unlike the
other three, this pass is **self-verifying**: it succeeds when it produces the
evidence they have been waiting on. Nothing here needs you to type anything
mid-fight — if it does, the milestone has failed at the one thing it exists to
fix.

Deploy first (a push does **not** reach the game): commit → `gh release create
v0.16.0` → `ghaddons update michac/CDMProbe` → `/reload`.

- [ ] **1 — It records without being asked.** Pull a dummy, kill it, **type
      nothing**, then `/cdmp hud log` — the pull is there, with a duration and a
      histogram. This is the milestone. If you had to toggle something first, it
      is the six-commands problem again.
- [ ] **2 — The histogram is the answer to §7.3 item 6.** Read the
      **distribution**, not a feeling. **1–2 dominant = the rules are right; a fat
      4+ tail = tighten `HudScore`, not a colour** — and that is the *next*
      milestone's work, deliberately not this one's.
- [ ] **3 — The peak set is arguable.** The worst moment names its abilities
      **with their reasons**, under the **live identity** — a transformed Grimoire
      must appear as Devour Magic or not at all (B1). A dot you disagree with is a
      scoring bug you can argue with; a dot with no reason is a design failure.
- [ ] **4 — Timestamps expose the GCD trap (§7.4 item 2).** Press an instant, then
      read the `ready` transitions around it: **nothing genuinely ready may flip to
      on-cooldown inside the 1.5 s global.** This is a *timing* defect — it is
      invisible in a snapshot and obvious in two timestamps.
- [ ] **5 — The mode + cap lines close §7.5 items 4 and 5.** The SPEND flip is
      timestamped **inside** the cast, not a beat after it; and a fast cap → HoG →
      cap shows **two `cap` edges and one suppression**.
- [ ] **6 — It survives the disk round-trip.** `/reload`, then read
      `…/WTF/Account/<ACCT>/SavedVariables/CDMProbe.lua` → `CDMProbeDB.pulls`
      (last 5, structured — `pulls[3].hist` indexes directly). ⚠ **No reload means
      you are reading the previous session's data, which is indistinguishable from
      a recorder that did nothing.**
- [ ] **7 — Cost is invisible.** Several pulls with the HUD on and no stutter. The
      sample path does one integer increment and no string work; only transitions
      and a *new peak* pay for `HudScore.Why`.
- [ ] **8 — §7.2 item 5 finally has evidence.** Remap a key the HUD didn't pick
      up, then read section **E** off disk. The spell shows one of exactly four
      things: two slots with the lower one marked `<-- used` (first-bound-slot-
      wins), a `cmd=none` row (unbindable 13–24 / 109–180), **no** rows at all (a
      macro `GetMacroSpell` can't resolve), or a populated **`2nd=`** (the
      secondary binding was the one you moved). One of those four is the answer.

**Then run §7.3, §7.4 and §7.5 — in that order — with the recorder on.** That is
the actual point of this milestone.

---

## 7.7 Verify in-game — M3c-c2, the sequence queue + opener (v0.17.0, 2026-07-21)

**Board-independent — run it whenever.** Unlike §7.3–§7.5 this reads your own
casts, not the dot score, so it does **not** wait on the strictness session. It
does want a **real opening** (a pre-stacked pull), which a target dummy provides.

Deploy first (a push does **not** reach the game): commit → `gh release create
v0.17.0` → `ghaddons update michac/CDMProbe` → `/reload`. Then `/cdmp hud opener
on` (it is **default off**).

- [ ] **1 — It arms.** Out of combat with the opener on, the ghost shows as a
      **left-to-right strip of keybinds above the panel** — an `OPENER` header —
      beside the PREP chrome from M3c-c1. `/cdmp hud status` shows `opener … armed`.
- [ ] **2 — It rides.** Drag the CDM in Edit Mode; change Orientation / # Rows.
      The queue follows and stays at its **own full width** — not clipped to the
      ~28px icon column (the `notes.md` §9 hazard; one centre anchor + explicit
      width).
- [ ] **3 — Advance + drop-through.** Pull and run the opener; steps cross off as
      pressed. Deliberately press one **out of order** (e.g. HoG before Imp Lord):
      Imp Lord drops silently and the queue does **not** jam.
- [ ] **4 — `count`.** HoG needs **two** presses to clear; the rebuild SB needs
      **three**. The count shows as `HoG x2` and decrements.
- [ ] **5 — `optional`.** Skip Imp Lord (on CD): it drops without stalling. Skip
      Implosion (single-target): same.
- [ ] **6 — Identity.** If a Demonic Art transforms a HoG into **Ruination**
      mid-opener, that press must still tick the **HoG** step — the consumer
      resolves the override back to the base (the opposite of the keybind rule, on
      purpose — B1).
- [ ] **7 — Dissolve + re-arm.** ~15s after Tyrant the whole queue **vanishes**
      (first window close → handoff to sustain); drop combat and it **re-arms** for
      the next pull. Draining the whole script early also dissolves it.
- [ ] **8 — It's in the recorder.** `/cdmp hud log` shows `queue` transitions
      (`opener armed` / `advanced … -> …` / `opener dissolved`) in the event tail,
      captured to disk like everything else (M3e). Nothing had to be typed
      mid-pull.
- [ ] **9 — Off is clean.** `/cdmp hud opener off` → the ghost disappears; `/cdmp
      hud` off → pixel-clean. No stutter across pulls (the widget only redraws on
      arm/advance, not per frame).

**What a failure means.** A queue that jams on an out-of-order press (item 3) or
mis-identifies a transform (item 6) is a **widget bug that M4 would inherit** —
those two rules exist specifically because the burst queue reuses them. A queue
that reads as a nag rather than a ghost is the §0.5.8.7 §0 line being crossed.

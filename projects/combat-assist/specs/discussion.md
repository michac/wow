# Combat Assist Plus — open questions

**What this file is for:** product questions that still require an author decision. It holds
the smallest live options and what would decide between them. Approved behavior belongs in
`spec.md`; agreed work in `backlog.md`; completed reasoning in `notes.md`.

D22–D26 came out of the **first Havoc flight, 2026-08-15** (Uncomplete, Kil'jaeden, cap v0.4.0,
Fel-Scarred). **D22 was resolved 2026-08-15** and **D18–D21 retired the same day** — both at the
foot of this file, and **D25 was retired 2026-08-16** when its subject was deleted. D23, D24 and
D26 remain open below.

## D23 — What should The Hunt's hold gate on?

**The finding.** 90 of ~95 draws this flight were `COOLDOWN/veil+blocked` from
`hunt_awaits_meta`. The authored rule — *hold The Hunt while Metamorphosis is available* — is
right in principle (save it to buff Abyssal Gaze inside the Meta window) and useless at this
breadth, because Meta is a ~2-minute cooldown the player is usually sitting on. The engine is
doing exactly what the catalog says.

Smallest options:

- **Gate on intent, not availability** — hold only when Meta is available *and* something says
  the window is imminent (Eye Beam or Death Sweep on cooldown, the same reset relationship
  Metamorphosis's own C1 mark already reads).
- **Gate on a time band** — a sealed range curve, so the hold appears only inside the last N
  seconds of Meta's cooldown. Reuses the C2 mechanism already shipped for Essence Break.
- **Drop the hold** and let The Hunt be directed by elimination alone.

What would decide it: whether a hold that fires this often is read as information or as
furniture. The player's report this flight was the latter.

**Note 2026-08-15 — the premise is in doubt, and the three options are premature.** The player
reports casting Metamorphosis close to on-cooldown, which means `ready(metamorphosis)` — the sole
gate on the hold (`Catalogs/Havoc.lua`, `hunt_awaits_meta`) — should read *false* most of the
fight and the hold should be *rare*, not near-constant. Reading the flown v0.4.0 code, the engine
gates the hold correctly (readiness is the alert-edge latch, unknown never fires it), so "Meta is
usually available" is not a live explanation. Two survive: the readiness latch for Meta is stuck
`true` (a bug, plausibly the demon-form override-id flip — R7), or the "90 of ~95 draws" ratio was
over-read (draws are transitions, not a duty cycle). **The old capture could not tell these apart —
it logged the marker fired, not the readiness that fired it.** v0.5.0 adds `W{}` to the `tier`
stream (`flight-reading.md`), which records each marker's decision and the term values behind it.
**Re-fly Havoc, then read `the_hunt:hunt_awaits_meta` in `W{}` before choosing among the three
options above** — if Meta reads stuck `true`, D23 is a bug ticket, not a gate-design question.

## D24 — What does cap say about a charge spell it cannot count?

**The finding, in two halves.** `C_Spell.GetSpellCharges().isActive` only means "a recharge is
running", so it cannot tell **1/2 from 0/2** — and the catalog reads *not capped* as `blocked`,
badging a perfectly castable Immolation Aura as skipped for most of a fight. Separately, this player's
**active** loadout has no *A Fire Inside*, so Immolation Aura is a **one-charge** spell where the
treatment should not appear at all — yet the capture shows `capped`/`recharging` 98 times. Either
a different loadout was flown, or the `maxCharges > 1` guard at `Sense.lua:104-105` is not
holding. That split is a test, not a decision, and is filed in `backlog.md`.

The decision is what the cue means once the count is unknowable.

Smallest options:

- **Positive-only.** Draw the gold `capped` badge at max and draw *nothing* below it. Loses the
  "recharging" statement, which `isActive` cannot make honestly anyway.
- **Keep both, and make this `blocked` non-eliminating.** Let `blocked` say "a recharge is running"
  without ruling the button out, since it may well be castable. **Re-stated 2026-08-16:** its old
  cost — losing Part 2.5's veil derivation — is gone with the veil, and the remaining cost is
  larger and more exact. The negative badge is now cap's **only** eliminating mark, so a `blocked`
  that does not eliminate makes one red badge mean two different things depending on which fact
  produced it, and the reader cannot tell which. It also breaks the premise `elimination_gate`
  runs on (a negative badge rules its button out), so taking this option means saying in Part 0.5
  what a non-eliminating negative *is* and teaching the gate to see it — a reading-model change,
  not a token edit.
- **Build the napkin estimator** (R6) so the count is real. The most work, and Immolation Aura is
  its named worst case because of the demon-form id flip.

What would decide it: whether a button marked skipped while it is castable is worse than no signal
at all. On this flight it was — the player read the row as quieter than it should have been.

## D26 — Which source decides Immolation Aura's rank against Chaos Strike?

**The finding.** The catalog puts Chaos Strike above Immolation Aura, following the Icy Veins 12.1
Fel-Scarred list (#10 Annihilation/Chaos Strike → #11 Immolation Aura → #12 Felblade). **Maxroll
and the Tier-1 simc APL both put Immolation Aura above the spenders.** The KB records the conflict
and does not resolve it; the practical reconciliation on offer is *"press Chaos Strike over
Immolation Aura unless IA is at 2 charges or about to be."*

This matters to cap because the row order is the argument. If Immolation Aura outranks the
spenders, the gold `capped` badge is not an exception to elimination — it is the rank, and the
positive-cue justification changes shape.

Smallest options:

- **Keep Icy Veins' order** and treat the `capped` badge as the documented exception. Status quo.
- **Follow simc/maxroll** and re-rank Immolation Aura above the spenders, which removes the need
  for a positive cue to carry it.
- **Wait.** The simc APL is pre-12.1 (commit `6e14948`, 2026-03-13) and 12.1 nerfed Immolation
  Aura 8 % while buffing the spenders 6 %. Season 2 opens 2026-08-18 and a re-pulled APL at a
  12.1 SHA is already the KB's named highest-value follow-up.

What would decide it: a 12.1 APL. Until then any answer is editorial.

---

## Retired 2026-08-16

- **D25 — should Blizzard's swipe carry more weight than cap's veil?** **The subject was
  retired, not weighed.** The question asked how loud cap's dim should be relative to the stock
  swipe; on 2026-08-16 the author deleted the veil outright (`render-shelf.md` V4, now a retired
  stub; `backlog.md` → *Retire the veil — one condition, one surface*), so there is no cap dim left
  to rank against Blizzard's. **No veil weight was chosen** — none of the three options
  (quieten it / veil the `cd` row too / leave it) was taken, and none is available. The finding
  behind it stands and was part of the argument for removal: cap's 60 % veil read *louder* than the
  stock swipe, so a button cap merely had an opinion against looked more unavailable than one that
  was genuinely down (Vengeful Retreat, this flight). What is now the only cap-drawn "ruled out"
  mark is the red badge, and whether **it** over- or under-reads against the swipe is a live
  question the next flight answers — it is not this one, and it returns in its own right under the
  striped-overlay work rather than as D25 reopened.

## Resolved 2026-08-15

- **D22 — the reading model's ordering, resolved by re-anchoring the vanilla frames.** cap takes
  over the CDM's *layout* without owning the row or rewriting the player's saved settings: out of
  combat it re-anchors Blizzard's own item frames into the authored priority order and sets the
  row to **always-show**, so the grid is static and the positions **persist through combat** while
  the CDM keeps doing every hard thing (cooldown data, swipes, charges, glow, desaturation). In
  combat cap only overlays, exactly as it already does. This is downstream of §3.6's
  **two-execution-context** principle: positioning is *setup-path* work, so the combat restrictions
  never applied to it — which is what made the original three options (read-the-drawn-order /
  own-the-row / narrow-the-claim) the wrong menu. The frames are not protected templates
  (`Blizzard_CooldownViewer` declares no `protected="true"`; item frames inherit a plain virtual
  `CooldownViewerBaseItemTemplate`), so the re-anchor is legal even in combat — though cap does not
  need it to be.
  - **Ordering** is solved by pure repositioning, with no settings write at all.
  - **Inserting a missing spell** splits: a spell the CDM *can* track but hides gets a one-time,
    surgical out-of-combat **un-hide** (flip the hidden flag only, order and cosmetics preserved) so
    the CDM pools a frame, then reposition; a spell the CDM cannot track at all is **self-drawn**
    (rare in a rotational roster). Both keep the CDM doing the rendering wherever it can.
  - **Unchanged constraint:** a CDM re-skin that also re-anchors these frames (EllesmereUI's
    Cooldown Manager module) fights cap for position. "Requires no reordering CDM module" stands;
    cap detects and warns rather than silently mislead.
  - **Gated on** the in-game verification now at the front of `backlog.md` → *Now* (control the
    positioning, don't break the CDM, confirm persistence through combat). If that fails, D22
    reopens.

## Retired 2026-08-15

- **D18 — what static tier treatments survive real icon art?** Settled by the lab promotion of
  **V2** on 2026-08-13: a solid per-lane border with a one-shot arrival snap, four lanes, every
  number in `render-shelf.md` Part 6. The question also predated the tier rename — it was written
  in ASAP / SOON / FALLBACK, which stopped being the vocabulary on 2026-08-12.
- **D19 — how should stock proc glow coexist with Demonbolt emphasis?** No longer an author
  decision: the shelf declares one answer (`tokens.surfaces.proc_glow_alpha`, applied through
  `hooksecurefunc(frame, "RefreshOverlayGlow")`) and says outright that it is a dial for an
  eyeball. Changing it is a shelf edit. With V1's ring retired there is no cap animation competing
  with the stock glow, which was most of the original tension.
- **D20 — what should the two Tyrant setup markers look like?** Premise gone. The Dreadstalkers
  and Grimoire dots **stopped drawing on 2026-08-14** — they were ad-hoc markers with their own
  hues, and the cue vocabulary is now a closed set of four. They are still evaluated and still
  reported in the `draw` capture's `M{}`. Re-authoring them as cues is `authoring.md` stages 1–5
  work on a spec that has never flown, tracked in `backlog.md`.
- **D21 — does the Tyrant bar earn its surface?** Not retired as answered — retired as *not yet
  askable*. Demonology has never flown, so there is no play to judge it against, and the question
  was sitting here as though a decision were pending. It returns when Demonology flies.

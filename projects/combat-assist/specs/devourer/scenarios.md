# Devourer Demon Hunter — the scenario catalog

**What this file is for.** The **proof** that the catalog's lanes and cues reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. Devourer's walk also has to say how two surfaces compose, which is why it carries more structure than a single row would need.

⚠ **Section numbers are preserved from the single-file catalog they were split out of
(2026-08-19), so a `§7.x` citation anywhere still resolves here.** They are not renumbered
precisely so those citations keep working.

**Cross-links.** `catalog.md` beside this file is the definition — roster, lanes, cues, contract
boundary. `../spec.md` §3.6 owns the readable/sealed boundary, `../pattern-shelf.md` the recipes,
`../render-shelf.md` every pixel. **Three files per spec** (`../authoring.md` §0): a definition,
its proof, and its safety case.

---

## 7. The state walk

The model is `../render-shelf.md` Part 0.5's, and that file is the authority for it. Two passes,
in a chain: **pass 1**, if any entry wears a positive cue the leftmost such entry must be the
press; **pass 2, otherwise**, the leftmost entry that is neither swiped nor wearing a negative
badge must be the press. **This catalog declares no positive cue**, so every scenario below is
judged by pass 2 alone.

### 7.1 The row, and the order the two surfaces are read in

**The virtual panel (V12), left to right:**

```
 Collapsing Star (gated) · Consume (standing)
```

**The Essential line, in cap's authored order (five icons in this build):**

```
 Void Metamorphosis · Reap · Void Ray · Soul Immolation · Voidblade
```

**The two surfaces interleave, and the two kinds of virtual row interleave at different points.**
The panel is physically separate from the Cooldown Manager, so the walk has to say how they
compose, and the answer follows from what each kind of row *is* rather than from where the frames
sit. The composed reading order is:

```
 [a cleared GATED row] → [the Essential line, left to right] → [the STANDING row]
```

- **A cleared gated row is pre-emptive.** Collapsing Star is hatched by default, so in the
  ordinary case it is a dead icon the eye ignores; when it clears it is a **change** in an
  otherwise-static panel, and it arrives as an appearance event rather than as a scan position.
  That is structurally the pre-emptive role Part 0.5 gives pass 1. **It is only sound because a
  cleared gated row is always the press** — which is what §6.1's readable gate buys, and removing
  the gate would make this composition wrong.
- **The standing row is the terminus.** Consume never changes, so it never attracts attention; it
  is furniture the player learns to read as *the floor*. Elimination reaches it only once
  everything to its left is gone, which is precisely V12's *"its position already encodes its
  rank."*

So the player's procedure is: *did something appear in the panel? press it. No? sweep the CDM row.
Row exhausted? the standing icon is still sitting there, and it is the answer.* Every row bullet
below is written in that composed order, with `‖` marking the two seams.

**Why that Essential order, when the APL's rung order is not it.** Four of the five rows sort by
rung and stay sorted in both phases: Void Metamorphosis (2) · Reap (6) · Void Ray (8) · Soul
Immolation (13). **Voidblade is the exception and it is placed last deliberately.**

Its rung is **1** outside Meta and **11–12** inside, and no single position serves both. Rung
number is not press frequency: rung 1 fires in exactly one narrow state — the last global before a
transform, and only with *Devourer's Bite* — while outside that state **this branch never presses
Voidblade at all**, because rung 1 is its only out-of-Meta line. Placed first, the leftmost icon
would stop the scan on every build-phase global where Voidblade happened to be off its ~30 s
cooldown; placed last, it is wrong only for rung 1 (misordering 2) and nearly right inside Meta,
where 11–12 sit just above Soul Immolation's 13. **Last is the best single position**, and it stays
last: `Catalog.ForBuild` selects on spec and hero tree only, so a row cannot move at runtime and a
reordering fact can never be a badge.

⚠ **Position 1 rests on the client's own usability channel.** Void Metamorphosis is uncastable
below a full bank, and `../render-shelf.md` Part 1 records that the CDM desaturates and re-tints
its icons continuously off `SPELL_UPDATE_USABLE` — *"the client's built-in 'you cannot cast this'
channel"* — which cap deliberately does not duplicate. Every walk below assumes a below-bank Void
Metamorphosis reads as ruled out for that reason, and writes it `cd`. **If it does not, position 1
is wrong and Meta needs a readable hold from the same open fact** (§8, item 3).

### 7.2 Verdicts

The nine-verdict vocabulary is `../render-shelf.md`'s `tokens.verdicts` and this file adds none.
Four notes on how it maps here:

- A **hatched gated virtual row** is written `cd` — the one verdict carrying both `swipe` and
  `hatch`, and the one the elimination gate skips. Mechanically right (a hatched row is ruled out)
  and semantically loose (Collapsing Star has no cooldown; it is *not granted*). Flagged rather
  than solved with a new verdict.
- A **cleared gated row** is `press` when the walk reaches it and `below` otherwise.
- The **standing row** is never `cd`. It is `press` when the sweep terminates on it and `below`
  when the sweep stopped earlier — which is the ordinary case.
- A below-bank **Void Metamorphosis** is written `cd`, per §7.1's ⚠.

### 7.3 Build phase — outside Void Metamorphosis

**B-1 · The clean build global.** *State:* single target, bank mid, Reap on cooldown, Fury ≥ 100,
Soul Immolation's effect running, Voidblade on cooldown, nothing procced.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Reap `cd` · **Void Ray `press`** ·
  Soul Immolation `below` · Voidblade `below` ‖ Consume `below`
- **Walk.** The gated row is hatched, so nothing appeared → sweep the line. Void Metamorphosis —
  uncastable below a full bank, ruled out by the client's own desaturation → skip. Reap — on
  cooldown → skip. **Void Ray** — available, affordable, nothing rules it out → **press.** Rung 8,
  and the channel that creates the Eradicate upgrade. The sweep stops before the terminus.
- **Eye-direction.** Elimination alone; no cue fires.

**B-2 · Fury-starved.** *State:* as B-1 but Fury under 100, Reap ready.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · **Reap `press`** · Void Ray `starved` ·
  Soul Immolation `below` · Voidblade `below` ‖ Consume `below`
- **Walk.** Panel and Meta skipped as B-1. **Reap** — ready, nothing rules it out → **press**
  (rungs 6–7). Had Reap been on cooldown the walk would reach Void Ray, find cue **A**'s `starved`
  badge, and carry on — which is B-3.
- **Cue set.** A (readable) → **have**.

**B-3 · The sweep runs out of row, and terminates on the floor.** *State:* Reap on cooldown, Fury
under 100, Soul Immolation on cooldown, Voidblade on its ~30 s cooldown, no procs, bank mid.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Reap `cd` · Void Ray `starved` ·
  Soul Immolation `cd` · Voidblade `cd` ‖ **Consume `press`**
- **Walk.** Nothing appeared in the panel → sweep. Every Essential icon is swiped except Void Ray,
  which wears cue **A**'s `starved` badge → skip. The sweep reaches the terminus: **Consume** —
  rungs 14–15, the unconditional floor, and the press.
- **This is the scenario the standing row exists for.** Consume is the most-pressed button in the
  branch and it has no Cooldown Manager frame in any category (§3). Without a standing virtual row
  the sweep would end in silence here and the answer would be reachable only from memory; with one
  it ends where the priority list ends. Note the row wears **no cue and needs none** — its rank is
  its position, and the eye is directed to it by the absence of everything else, which is
  `../spec.md` §3.1's eye-direction-by-elimination in its plainest form.

**B-4 · The bank fills.** *State:* soul bank at 50, single target, *Devourer's Bite* talented,
Voidblade off cooldown.
- **Row.** Collapsing Star `cd` ‖ **Void Metamorphosis `press`** · Reap `below` · Void Ray `below` ·
  Soul Immolation `below` · Voidblade `below` ‖ Consume `below`
- **Walk.** Nothing appeared in the panel → sweep. Void Metamorphosis is castable, the client stops
  desaturating it, and it is leftmost with nothing ruling it out → **press.** Rung 2 is
  unconditional at a single target.
- **Cue C is doing its work here and nowhere else in the walk**: the bank's count has been climbing
  beside this icon for the whole build phase, so the transform arrives as something the player
  watched coming rather than as an icon that lit up.
- ⚠ **Misordering 2 fires here**: the APL would spend this global on **Voidblade** (rung 1) to land
  *Devourer's Bite* on the window and press Meta next. Voidblade sits at position 5 and the walk
  never reaches it.

**B-5 · AoE, bank full, no Reap-family glow.** *State:* `/cap aoe` on, bank at 50, *Eradicate*
talented, neither Eradicate nor Moment of Craving up, Reap on cooldown.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `hold-readable` {cues: blocked} · Reap `cd` ·
  **Void Ray `press`** · Soul Immolation `below` · Voidblade `below` ‖ Consume `below`
- **Walk.** Void Metamorphosis is castable but wears the red `blocked` badge (cue **D**) — at 2+
  targets rung 2 requires the Eradicate upgrade banked first → skip. Reap on cooldown → skip.
  **Void Ray** → **press**: channelling it in full is exactly what turns Reap into Eradicate, so
  the badge and the press point at the same plan.
- ⚠ **Cue D is a sound slice, not the literal condition.** The APL holds when
  `!eradicate.up & talent.eradicate & !single_target`; cap draws `!proc & talent(eradicate) & aoe`.
  Because `proc(reap)` is the **OR** of Eradicate and Moment of Craving (§4.2), `!proc ⇒
  !eradicate.up` always, so the badge never fires where the APL would cast. It can *miss* a hold —
  Moment of Craving up while Eradicate is down keeps the glow on and the badge off — and missing a
  hold is the safe direction.

### 7.4 Window phase — inside Void Metamorphosis

The row re-skins across the transform (R7): **Reap → Cull**, **Voidblade → Pierce the Veil** (or
**Reaper's Toll** while Hungering Slash is the live form), **Consume → Devour** on the standing
virtual row, and the Void Metamorphosis row shows the form as active. The bank is **empty and
cannot refill** (`sc_demon_hunter.cpp:9179`), so rungs 1–2 are structurally dead for the whole
window — which is what lets Collapsing Star's gated row carry a single gate (§6.1).

**M-1 · Early window, Fury high.** *State:* transformed, Fury well above the drain, harvest counter
under 30, Cull on cooldown, no Soulburst.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Cull `cd` · **Void Ray `press`** ·
  Soul Immolation `hold-sealed` {cues: blocked} · Pierce the Veil `below` ‖ Devour `below`
- **Walk.** Panel hatched → sweep. The form is active → skip. Cull on cooldown → skip. **Void Ray**
  — free inside Meta, reduces the drain, +40 % damage → **press** (rung 8). Soul Immolation is not
  reached, and would have been skipped anyway: cue **B** has it badged, because Fury is nowhere
  near the drain and spending the save now means not having it at the end.
- **Cue set.** B (sealed) → **sealed**; the badge is `offered`, and only an eyeball proves it lit.

**M-2 · A Collapsing Star is granted, in AoE.** *State:* transformed, `/cap aoe` on, the harvest
counter has crossed 30, Cull and Void Ray on their in-Meta cooldowns, no Soulburst.
- **Row.** **Collapsing Star `press`** ‖ Void Metamorphosis `cd` · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `hold-sealed` {cues: blocked} · Pierce the Veil `below` ‖ Devour `below`
- **Walk.** The gated row **clears**: Collapsing Star is castable, and `!proc` says rungs 3–4 are
  not live. One icon changes in a static panel; the eye takes it pre-emptively and the Essential
  line is never swept. Rung 9, unconditional at 2+ targets — **and the press the five-icon line
  could never have pointed at, which is the whole reason V12 exists.**
- ⚠ **This row waits** (§8, item 3): what clears it is the open `isUsable` read.

**M-3 · Single target, counter between 30 and 34.** As M-2 with `/cap aoe` off.
- The gated row still clears, because *castable* is the only readable verdict available and rung
  5's `stack>=35` is a **sealed** threshold with no surface on a virtual row (§6).
- **Misordering 1**: the APL would bank to 35 first and press Cull or Void Ray here. The cost is
  one to five harvests of a shorter *Impending Apocalypse* chain — the Collapsing Star is not
  wasted, only slightly early. Named, small, and the alternative was a count tile on a surface V12
  does not give a virtual row.

**M-4 · The window is ending.** *State:* transformed, Fury under one tick of drain, Cull and Void
Ray both on their in-Meta cooldowns, Soul Immolation ready, the Voidsurge already spent.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Cull `cd` · Void Ray `cd` ·
  **Soul Immolation `press`** · Pierce the Veil `below` ‖ Devour `below`
- **Walk.** Cull and Void Ray are both swiped → skip. The sweep reaches **Soul Immolation**, and
  **cue B's badge has cleared** — the client's curve has crossed the drain break point — so nothing
  rules it out → **press.** Rung 13, and the 30 Fury that buys another few seconds of form.
- ⚠ **The state is chosen so Void Ray is genuinely unavailable, and that matters.** Void Ray is free
  inside Meta and sits at rung 8, above Soul Immolation's 13, so while it is up it is the press and
  the sweep stops there — correctly. Cue B is only ever *reached* on a global Void Ray cannot take,
  which is exactly when the Fury save is the question.
- **This is the cue that justifies the row.** A `blocked` badge lit for most of a window that clears
  at the moment the save is worth spending is a single-state marker doing precisely one job. ⚠ Its
  break point is authored off simc's fitted drain curve — ≈16.4 Fury/s at window start, rising — so
  a static threshold under-fires late in the window, which is when it matters most. Flown, not
  assumed (§8, item 4).

**M-5 · A Voidsurge is owed.** *State:* transformed, the window's first Pierce the Veil uncast, Cull
and Void Ray on cooldown, Fury still high, harvest counter under 30.
- **Row.** Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `hold-sealed` {cues: blocked} · **Pierce the Veil `press`** ‖ Devour `below`
- **Walk.** Everything above is swiped or badged, so the sweep reaches **Pierce the Veil** and
  presses it — the right answer, reached by elimination rather than by any cue, and one position
  before the terminus.
- ⚠ **cap cannot see the owed cast** (§4.2: `buff.voidsurge_*` are simc placeholders with no game
  aura), so this walk is right by position rather than by knowledge. In the state where the
  Voidsurge has **already** been spent, the sweep presses Pierce the Veil again where the APL would
  press Devour — a real, undrawn gap, and the same open fact as Havoc's `demonsurge_available`
  (§8, item 2).

### 7.5 Documented misorderings — what is left after the cues

1. **Single target, Collapsing Star granted below 35 harvests** (M-3). The gated row clears at 30
   where the APL waits for 35. Cost: a marginally shorter *Impending Apocalypse* chain.
2. **Voidblade carries no hold, and that costs twice.** Rung 1 is the branch's **only** out-of-Meta
   Voidblade line, so outside the pre-transform moment this button is never pressed — and cap
   cannot see the sealed fact (a full bank) that says which moment that is. Two symptoms, opposite
   in direction:
   - **The sweep stops on it** whenever everything above is swiped or badged and Voidblade is off
     its ~30 s cooldown, where the correct press is Consume. This is why the row is authored
     **last**: at position 5 it absorbs only states that already fell through, instead of stopping
     the sweep on every build global.
   - **The sweep never reaches it** at a full bank (B-4), where the APL spends the global on
     Voidblade for *Devourer's Bite*. Cost: one window without the +12 % amp applied in advance.

   **Both are fixed by the same measurement.** `!usable(void_metamorphosis)` is exactly *"the bank
   is not full"* (§8, item 3): it would let Voidblade carry a `blocked` hold — killing the first
   symptom outright — and, with the hold in place, let a later revision move it to position 1 and
   kill the second.
   ⚠ That badge would be **lit across the whole build phase and correct**, which reads at first like
   Havoc's deleted `immolation_recharging`. It is not the same case: that badge's negation was
   *false* — the button is genuinely pressed at one charge — so it was lit **and wrong**.
   Lit-and-true is a noise question a flight settles; lit-and-false is a defect. Not built this pass
   either way.
3. **A spent Voidsurge** (M-5). The Voidblade row keeps reading pressable after its once-per-window
   empowerment is gone.
4. **Void Ray's rung-8 hold** (§4.2). Two auras share one overlay channel, so the AND the hold needs
   cannot be formed. Void Ray is never *held* by cap; at worst it is channelled while both upgrades
   are already banked and no 4-piece is equipped. ⚠ This one does **not** resolve by measuring — it
   is an expressiveness gap, not an open fact.
5. **Soulburst promotes Consume to rung 4 and cap's sweep does not follow it.** With the Season 2
   2-piece up, Consume outranks Collapsing Star, Reap, Void Ray and everything below; the sweep
   still stops at whichever Essential icon it reaches first. **Nothing is authored for it by
   design** (§6.1): Soulburst is a Tier-1 registered overlay on Consume and Devour, so the client
   already glows the promotion on the button the player presses, and cap does not draw a second
   mark for a fact Blizzard marks — the same argument that deleted cue E. Whether a cap-owned
   virtual row should mirror the client's glow is a `../render-shelf.md` question.

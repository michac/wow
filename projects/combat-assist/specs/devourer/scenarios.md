# Devourer Demon Hunter — the scenario catalog

**What this file is for.** The **proof** that the catalog's lanes and cues reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. Devourer's walk also has to say how two surfaces compose, which is why it carries more structure than a single row would need.

⚠ **Section numbers are preserved from the single-file catalog they were split out of
(2026-08-19), so a `§7.x` citation anywhere still resolves here.** They are not renumbered
precisely so those citations keep working.

⚠ **`## 7.x` is a level-2 heading on purpose and must stay one.** `capart`'s scraper ends a
scenario's body at the next scenario **or the next level-2 heading**, and until 2026-08-27 these
were `###` — so M-5's last bullet had silently swallowed the whole of §7.5 and rendered it on the
page, which is the failure `_scenario_bodies` documents and every other spec avoids by having
`##` sections. The numbers are unchanged; only the level is.

**Cross-links.** `catalog.md` beside this file is the definition — roster, lanes, cues, contract
boundary. `../spec.md` §3.6 owns the readable/sealed boundary, `../authoring.md`'s recipe index the recipe IDs,
`../render-shelf.md` every pixel. **Three files per spec** (`../authoring.md` §0): a definition,
its proof, and its safety case.

---

## 7. The state walk

The model is `../render-shelf.md` Part 0.5's, and that file is the authority for it. Two passes,
in a chain: **pass 1**, if any entry wears a positive cue the leftmost such entry must be the
press; **pass 2, otherwise**, the leftmost entry that is neither swiped nor wearing a negative
badge must be the press. **This catalog declares no positive cue**, so every scenario below is
judged by pass 2 alone.

## 7.1 The row, and the order the two surfaces are read in

**The virtual panel (V12): one row, and it is the standing one.**

```
 Consume (standing)
```

**The Essential line, in cap's authored order (five icons in this build):**

```
 Void Metamorphosis · Reap · Void Ray · Soul Immolation · Voidblade
```

⚠ **Inside Void Metamorphosis the first icon is Collapsing Star** — the same row, overridden
(`catalog.md` §3, measured in game 2026-08-27). It is not a sixth icon and it is not on cap's
panel; the line is five icons in both phases and only the first one's *face* changes. Until
2026-08-27 this walk drew Collapsing Star as a gated virtual row outside the left seam, i.e.
leftmost of everything, on the inference that a spell absent from `CooldownSetSpell` has no icon
anywhere. An override needs no row of its own.

⚠ **Vengeful Retreat is a seventh bound row and it is not on that line.** It lives in the
**Utility** viewer, which `Anchor.lua` does not re-anchor, so cap skins it, hatches it and gives
it the scan edge but takes no position for it — where it sits on screen is Edit Mode's business.
It appears in exactly one row below (**DEV-11**), drawn at the place its rung implies so the walk
can say what the priority list wants; that place is a statement about **rank**, not about pixels.
Every other row omits it because in every other state it is either swiped or not the press, and
listing an icon the reader cannot locate would be worse than leaving it out.

**The two surfaces interleave, and the composed reading order is now short.** The panel is
physically separate from the Cooldown Manager, so the walk still has to say how they compose:

```
 [the Essential line, left to right] → [the STANDING row]
```

- **The standing row is the terminus.** Consume never changes, so it never attracts attention; it
  is furniture the player learns to read as *the floor*. Elimination reaches it only once
  everything to its left is gone, which is precisely V12's *"its position already encodes its
  rank."*
- **The left panel is empty**, and stays written. `parse_row` takes exactly two seams or none
  (`capart.py`), and the shape it authorises is `[gated panel] ‖ [the Essential line] ‖ [standing
  panel]` with **either panel possibly empty** — so every row below opens with a bare `‖`. That is
  the parser's own documented shape, not a workaround.

So the player's procedure is: *sweep the CDM row left to right; if it is exhausted, the standing
icon is still sitting there and it is the answer.* Every row bullet below is written in that
composed order, with `‖` marking the two seams.

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

⚠ **And position 1's rung changes with its FACE, which is where the window phase's misordering
comes from.** Out of the form it is Void Metamorphosis's rung 2 and position 1 is right. Inside
the form it is Collapsing Star's — rung **5** at a single target with the counter at 35+, where
position 1 is right again, but rung **9** in AoE, *below* Void Ray's 8. The row is authored to its
out-of-form rung, and inside the form it is one band early (`catalog.md` §3; §7.5 item 1). The same
"a row cannot move at runtime" rule that fixes Voidblade last fixes this one first.

⚠ **Position 1 rests on a sealed count band cap authors, not on the client's usability channel.**
Void Metamorphosis is uncastable below the bank threshold, and this walk once wrote that
below-bank row `cd` on the premise that the CDM desaturates what cannot be cast. **It does not.**
`cooldownDesaturated` is assigned either the literal `false` or `self.isOnActualCooldown` at every
one of its six assignments, so a greyed CDM icon is a statement about **cooldown and nothing
else**; usability rides an entirely separate channel — a vertex-colour tint, `ITEM_NOT_USABLE_COLOR`
at `0.4, 0.4, 0.4` — and a tint is not a hatch *[T1 src @12.1.0:
`knowledge/addon-dev/cooldown-manager.md` §3.4, `CooldownViewer.lua:1195-1233`]*. Void
Metamorphosis is fragment-gated and has no timer at all, so **no swipe will ever be drawn on that
row**, and `cd` — the one verdict asserting both a swipe and a hatch — was describing pixels the
client never puts there.

A below-bank Void Metamorphosis is therefore written **`ruled-sealed`**. The soul bank is a sealed
count and V17 is precisely the primitive for it: the marks draw *below* the catalog's threshold and
the band above clears them, so the client evaluates cap's own rule against the secret and hatches
the row itself (`../render-shelf.md` V17). The elimination is genuine —
`tokens.verdicts["ruled-sealed"]` declares `eliminates: true`, which is what lets the sweep skip
position 1 — and it belongs to cap, so the first icon of the Essential line no longer rests on a
measurement of somebody else's channel. **Cue C is authored** as of 2026-08-27
(`catalog.json`, markers `meta_bank_glutton` / `meta_bank_deep`), so the band exists in the
shipped roster — what is left is that **nothing has flown**: cap reports that it offered the
rule and never learns whether the client drew it.

## 7.2 Verdicts

The five-verdict vocabulary is `../render-shelf.md`'s `tokens.verdicts` and this file adds none.
Three notes on how it maps here:

- The **standing row** is never `cd`. It is `press` when the sweep terminates on it and `open`
  when the sweep stopped earlier — which is the ordinary case.
- A below-bank **Void Metamorphosis** is written `ruled-sealed`, per §7.1's ⚠ — its own bank
  band rules it out, and no swipe is ever drawn there.
- A **Collapsing Star face below the grant** is written `ruled-sealed` for the same reason and off
  the same cue. ⚠ **This is the one place the correction cost something, and it is stated rather
  than hidden.** Blizzard *does* draw the face's unavailability, as a usability **vertex-colour
  tint** (`catalog.md` §8, item 8) — so the player can see it. But a tint is **not** one of cap's
  three eliminating signals (Blizzard's swipe, cap's negative badge, `ruled-sealed`), and the row
  has no cooldown, so `cd` would be a false statement about pixels the client never draws. What
  eliminates it in the walk is the same machinery §7.1 uses one phase earlier: cue **C**'s count
  band, pointed at `collapsing_star_stacking` instead of the bank — which is exactly the *"one row
  with two counts, selected by identity"* wrinkle `catalog.md` §6 records. **That second count is
  authored** (`catalog.json`, marker `star_counter`, threshold 30), so every in-form row below
  inherits §7.1's caveat in its weaker form: the band ships, and no eye has seen it draw.
  ⚠ **This is the second spec to hit the same wall, which makes it a shelf question rather than a
  Devourer one.** Destruction's Shadowburn reaches it from the other side — out of execute the
  client paints the button `ITEM_NOT_USABLE_COLOR` and the *player* is not stranded, but the
  reading model is, because Part 0.5 counts eliminating signals and the usability tint is not one
  of them (`../destruction/fact-classification.md` §5.4). Devourer routes around it with a count
  band it happens to have; Destruction cannot, and neither should have to.

## 7.3 Build phase — outside Void Metamorphosis

### B-1 · The clean build global

- **State.** Single target, bank mid, Reap on cooldown, Fury ≥ 100, Soul Immolation's effect
  running, Voidblade on cooldown, nothing procced.
- **CDM row.** ‖ Void Metamorphosis `ruled-sealed` {sealed: count-bands} · Reap `cd` · Void Ray `press` ·
  Soul Immolation `open` · Voidblade `open` ‖ Consume `open`
- **Walk.**
  1. **Void Metamorphosis** — below the bank threshold, so its own count band hatches the row and
     rules it out → skip. Out of the form this row is Void Metamorphosis and nothing else; the
     Collapsing Star face exists only inside the window (§7.1).
  2. **Reap** — on cooldown → skip.
  3. **Void Ray** — available, affordable, nothing rules it out → **press.** Rung 8, and the
     channel that creates the Eradicate upgrade.
  4. **Soul Immolation / Voidblade / Consume** — below the press; the sweep stops before the
     terminus.
- **Eye-direction.** Elimination alone; no cue fires.
- **⚠ Position 1 is cue C's band, and the band is now authored.** The `ruled-sealed` verdict here
  is correct by construction — the band is cap's own rule, evaluated by the client against the
  sealed bank — and as of 2026-08-27 it is declared in `catalog.json` and generated into
  `Catalogs/Devourer.lua`, so the same is true in B-2 and B-3. What is left is a flight: cap
  reports `offered`, never whether the numeral and the hatch appeared (`catalog.md` §8.2).
- **⚠ UNSURE — the bank is drawn TWICE on screen, and that is a design call, not a finding.**
  Blizzard already draws the collected count, on the shipped `DemonHunterSoulFragmentsBar`
  (`fact-classification.md` §4.1), so cue **C**'s numeral is a second mark for a fact the client
  already marks — the standing rule that deleted cue E. It was kept on the **independent-context**
  argument, precedent Backdraft (`../spec.md` §3.5): the count sits **beside the row it governs**,
  so the sweep never leaves the Cooldown Manager line to read it, and a bar elsewhere on the screen
  costs an eye movement elimination does not budget for. **The alternative was to draw no numeral
  and keep only the hatch** — the elimination would be identical and the readout would be gone.
  What settles it is looking at the two together in a pull: if the eye goes to Blizzard's bar
  anyway, the numeral is noise and the band should drop to `draw: "none"` below the threshold with
  the hatch alone.

### B-2 · Fury-starved

- **State.** As B-1 but Fury under 100, Reap ready.
- **CDM row.** ‖ Void Metamorphosis `ruled-sealed` {sealed: count-bands} · Reap `press` · Void Ray `open` {cues: starved} ·
  Soul Immolation `open` · Voidblade `open` ‖ Consume `open`
- **Walk.**
  1. **Void Metamorphosis** — below the bank threshold, hatched by its own band → skip.
  2. **Reap** — ready, nothing rules it out → **press** (rungs 6–7).
  3. **Void Ray** — wears cue **A**'s `starved` badge. Had Reap been on cooldown the sweep would
     reach it, skip it, and carry on — which is B-3.
  4. **Soul Immolation / Voidblade / Consume** — below the press.
- **Cue set.** A (readable) → **have**.
- **⚠ Position 1.** As B-1: the `ruled-sealed` verdict is sound, and it draws only once cue **C**
  ships (`catalog.md` §8.2).

### B-3 · The sweep runs out of row, and terminates on the floor

- **State.** Reap on cooldown, Fury under 100, Soul Immolation on cooldown, Voidblade on its
  ~30 s cooldown, no procs, bank mid.
- **CDM row.** ‖ Void Metamorphosis `ruled-sealed` {sealed: count-bands} · Reap `cd` · Void Ray `open` {cues: starved} ·
  Soul Immolation `cd` · Voidblade `cd` ‖ Consume `press`
- **Walk.**
  1. **Void Metamorphosis / Reap** — hatched by its own bank band, and on cooldown → skip. Note the
     two skips come from two different eliminators: Meta's is cap's sealed band, Reap's is
     Blizzard's swipe.
  2. **Void Ray** — castable but wears cue **A**'s `starved` badge → skip.
  3. **Soul Immolation / Voidblade** — both swiped → skip.
  4. **Consume** — the sweep reaches the terminus: rungs 14–15, the unconditional floor →
     **press.**
- **Why the standing row exists.** Consume is the most-pressed button in the branch and it is now
  the **only** press in the branch with no Cooldown Manager frame in any category (`catalog.md`
  §3). Without a standing virtual row the
  sweep would end in **silence** here and the answer would be reachable only from memory; with one
  it ends where the priority list ends. Note the row wears **no cue and needs none** — its rank is
  its position, and the eye is directed to it by the absence of everything else, which is
  `../spec.md` §3.1's eye-direction-by-elimination in its plainest form.
- **⚠ Position 1.** As B-1: the `ruled-sealed` verdict is sound, and it draws only once cue **C**
  ships (`catalog.md` §8.2).

### B-4 · The bank fills

- **State.** Soul bank at the transform threshold — **35 on the *Soul Glutton* build the live
  guides publish, 50 without it** (`catalog.md` §1c) — single target, *Devourer's Bite* talented,
  Voidblade off cooldown.
- **CDM row.** ‖ Void Metamorphosis `press` · Reap `open` · Void Ray `open` ·
  Soul Immolation `open` · Voidblade `open` ‖ Consume `open`
- **Walk.**
  1. **Void Metamorphosis** — the bank has reached the threshold, so the band above it clears the
     hatch, and the row is leftmost with nothing ruling it out → **press.** Rung 2 is
     unconditional at a single target.
  2. **Reap / Void Ray / Soul Immolation / Voidblade / Consume** — below the press.
- **Cue C.** Doing its work here and nowhere else in the walk: the bank's count has been climbing
  beside this icon for the whole build phase, so the transform arrives as something the player
  **watched coming** rather than as an icon that lit up.
- **⚠ UNSURE — the threshold is TWO authored numbers, and only one of them draws on any build.**
  The bank fork is written as two mutually-exclusive `when` gates on `talent(soul_glutton)` —
  `meta_bank_glutton` clears at **35**, `meta_bank_deep` at **50** (`catalog.md` §1c). **The
  alternative was one table with one number**, and it is wrong on one build or the other in
  directions that are not symmetric: 35 on a deep-bank build clears a row the game will not cast
  (a wasted global), while 50 on a *Soul Glutton* build **hatches a row the game will** —
  eliminating the correct press, which is the class of defect Protection's `as_guidance_capped`
  was. The cost of the fork is a **third ceded corner** on this row: `CORNER_DISPLAYS` claims a
  stack slot per marker by declaration, so with the in-form counter there are three claims, two of
  them permanently blank, and cue **D**'s badge begins three steps down the right edge. What
  settles it is looking at the row with cue D lit: if the blank steps read as a fault, the fork has
  to move to a build-time selection the engine does not have today.
- **⚠ UNSURE — misordering 2.** The APL would spend this global on **Voidblade** (rung 1) to land
  *Devourer's Bite* on the window, and press Meta on the next one. Voidblade sits at position 5
  and this walk never reaches it, so cap presses Meta a global early and the window runs without
  the +12 % amp applied in advance. **This is a known cost, not an oversight** (§7.5 item 2) — and
  it is fixed by the same measurement as everything else here: `!usable(void_metamorphosis)` is
  exactly *"the bank is below the transform threshold"* (`catalog.md` §8 item 3, §1c).

### B-5 · AoE, bank full, no Reap-family glow

- **State.** `/cap aoe` on, bank at the transform threshold (§1c), *Eradicate* talented, neither Eradicate nor Moment of
  Craving up, Reap on cooldown.
- **CDM row.** ‖ Void Metamorphosis `open` {cues: blocked} · Reap `cd` ·
  Void Ray `press` · Soul Immolation `open` · Voidblade `open` ‖ Consume `open`
- **Walk.**
  1. **Void Metamorphosis** — castable, but wears the red `blocked` badge (cue **D**): at 2+
     targets rung 2 requires the Eradicate upgrade banked first → skip.
  2. **Reap** — on cooldown → skip.
  3. **Void Ray** — → **press.** Channelling it in full is exactly what turns Reap into Eradicate,
     so the badge and the press point at the same plan.
  4. **Soul Immolation / Voidblade / Consume** — below the press.
- **Cue set.** D (readable) → **have**. Note the bank is full here, so §7.1's count band has
  cleared and is not what eliminates — the skip is cap's own badge, on a readable fact.
- **⚠ UNSURE — cue D is a sound slice, not the literal condition.** The APL holds when
  `!eradicate.up & talent.eradicate & !single_target`; cap draws `!proc & talent(eradicate) & aoe`.
  Because `proc(reap)` is the **OR** of Eradicate and Moment of Craving (`fact-classification.md`
  §4.2), `!proc ⇒ !eradicate.up` always, so the badge never fires where the APL would cast. It can
  *miss* a hold — Moment of Craving up while Eradicate is down keeps the glow on and the badge off
  — and missing a hold is the safe direction. **Unverified either way: nothing has flown.**

### DEV-11 · Voidstep, on a row the ordered scan does not reach

⚠ **Its id is deliberately outside the `B` / `M` families**, because the row it is about is
outside both phases' Essential line: Vengeful Retreat is in the **Utility** viewer and
`Anchor.lua` re-anchors Essential only (§7.1). It is written as a build-phase state because
Voidstep is granted by **Hungering Slash**, the out-of-form Voidblade face.

- **State.** Out of the form, bank mid, **Voidstep up**. Reap on its cooldown, Void Ray on its
  cooldown, Soul Immolation on its cooldown, Voidblade on its ~30 s cooldown.
- **CDM row.** ‖ Void Metamorphosis `ruled-sealed` {sealed: count-bands} · Reap `cd` ·
  Void Ray `cd` · Soul Immolation `cd` · Voidblade `cd` · Vengeful Retreat `press` ‖ Consume `open`
- **Walk.**
  1. **Void Metamorphosis** — below the bank threshold, hatched by its own band → skip.
  2. **Reap / Void Ray / Soul Immolation / Voidblade** — every Essential row swiped → skip.
  3. **Vengeful Retreat** — Voidstep is up, so rung **10** is live: the retreat releases a Cosmic
     explosion and is a damage press rather than a mobility one → **press.**
  4. **Consume** — the terminus, not reached. This is the point of writing the scenario down: it
     is B-3's state with one aura added, and the correct answer moves off the terminus.
- **Why the row exists at all.** Rung 10 is real, it outranks the floor, and a roster row no
  scenario reaches is a hole in the proof rather than a surplus row. Without this walk the
  catalog's only claim about Vengeful Retreat was that it wears no cue.
- **⚠ UNSURE — the POSITION in that row is a claim about rank, not about pixels.** `Anchor.lua`
  re-anchors the Essential viewer only, so cap does not put Vengeful Retreat sixth or anywhere
  else; the player's Edit Mode does. It is drawn here at the place rung 10 implies so the walk can
  be judged, and the honest reading is *"once the Essential line is exhausted, the Utility row is
  the answer and Blizzard's own Voidstep glow is what carries the eye to it"* — the glow is a
  Tier-1 registered spell-activation overlay on `198793` (`fact-classification.md` §4.2) and cap
  deliberately leaves it intact. **The alternative was to delete the row from the catalog** and
  let Blizzard's swipe carry it, which is still an open author decision in `../discussion.md`.
  What this walk settles is only that deleting it would lose a press the priority list makes.
- **⚠ UNSURE — nothing has measured that `IsSpellOverlayed` answers for Voidstep in combat.**
  §4.2 resolves from Tier-1 DB2 *which* auras Blizzard registers as icon-highlight overlays; it
  does not prove the read fires in an instance. cap draws no badge here, so the exposure is the
  player's eye rather than cap's, but the walk's step 3 rests on the glow. `@verify-ingame`.

## 7.4 Window phase — inside Void Metamorphosis

The row re-skins across the transform (R7), on **three** chains: **Void Metamorphosis →
Collapsing Star** at position 1, **Reap → Cull**, **Voidblade → Pierce the Veil** (or **Reaper's
Toll** while Hungering Slash is the live form), plus **Consume → Devour** on the standing virtual
row. The bank is **empty and cannot refill** (`sc_demon_hunter.cpp:9179`), so rungs 1–2 are
structurally dead for the whole window — which is why a scan that starts at position 1 is not
stepping past anything (`catalog.md` §6.1).

⚠ **Position 1 is the press-or-not question for the entire window**, and it is where the
correction lands. The row is Collapsing Star from the moment the form opens and it draws unusable
until 30 fragments have been harvested inside it; below that it is written `ruled-sealed` off the
counter's own band, and above it, it is castable and leftmost. §7.2's third note is the whole of
the reasoning and every row below rests on it.

### M-1 · Early window, Fury high

- **State.** Transformed, Fury well above the drain, harvest counter under 30, Cull on cooldown,
  no Soulburst.
- **CDM row.** ‖ Collapsing Star `ruled-sealed` {sealed: count-bands} · Cull `cd` · Void Ray `press` ·
  Soul Immolation `open` {cues: blocked} · Pierce the Veil `open` ‖ Devour `open`
- **Walk.**
  1. **Collapsing Star** — position 1 wears the form's face. The harvest counter is under 30, so
     no Star has been granted; the counter's own band hatches the row and rules it out → skip.
  2. **Cull** — on cooldown → skip.
  3. **Void Ray** — free inside Meta, reduces the drain, +40 % damage → **press** (rung 8).
  4. **Soul Immolation** — not reached, and would have been skipped anyway: cue **B** has it
     badged, because Fury is nowhere near the drain and spending the save now means not having it
     at the end.
  5. **Pierce the Veil / Devour** — below the press.
- **Cue set.** B (sealed) → **sealed**; the badge is `offered`, and only an eyeball proves it lit.
- **⚠ UNSURE — the standing row says `Devour` here, and the catalog is not what makes it.**
  `Catalog.Check` **refuses** any subject predicate naming a virtual ability, so cap may not
  declare Consume → Devour at all: the ability has no Cooldown Manager row, the read would be
  UNKNOWN for life, and V12's inverted unknown would hatch the terminus forever. The face is
  therefore resolved on the **draw**, by `Panel.Face` off `C_Spell.GetOverrideSpell` (guarded:
  a secret or refused answer, `0` — which is truthy in Lua — and an override equal to its input
  all fall back to Consume's own id). **The alternative was to write `Consume` in M-1…M-5 and
  accept that the row shows the wrong button for a whole window.** What settles it is one look at
  the panel inside the form; nothing here has run in the client.
- **Position 1.** Inside the window the row is **Collapsing Star**, not Void Metamorphosis, and
  what rules it out is the **harvest counter's** band rather than the bank's — a different count on
  the same row, selected by identity (`catalog.md` §6). The form being active is readable and true
  but is not what draws anything here: the row is not showing Void Metamorphosis at all.
- **⚠ UNSURE — cue B is sealed, and its break point is fitted.** Nothing here proves the badge is
  lit in this state. Cap hands the client a curve and never learns the answer (S1 / V9), so only an
  eyeball in game can say whether Soul Immolation is actually wearing the badge — and the threshold
  under it is authored off simc's fitted drain curve (≈16.4 Fury/s at window start, **rising** —
  and a quarter faster again on a *Soul Glutton* build, so the number is per-build), which M-4
  spells out. **The badge drawn above is what cap intends, not what has been observed.**

### M-2 · A Collapsing Star is granted, in AoE

- **State.** Transformed, `/cap aoe` on, the harvest counter has crossed 30, Cull and Void Ray on
  their in-Meta cooldowns, no Soulburst.
- **CDM row.** ‖ Collapsing Star `press` · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `open` {cues: blocked} · Pierce the Veil `open` ‖ Devour `open`
- **Walk.**
  1. **Collapsing Star** — the counter has crossed 30, so a Star is granted and the band above the
     threshold clears the row. It is position 1 with nothing ruling it out → **press.** Rung 9,
     unconditional at 2+ targets.
  2. **Cull / Void Ray / Soul Immolation / Pierce the Veil / Devour** — below the press.
- **Position 1.** As M-1, cleared rather than hatched: the counter is above the band.
- **⚠ UNSURE — the press is right here for the same reason a badge would have given it.** Rung 9
  sits **below** Void Ray's rung 8, so in AoE the APL wants Void Ray first, and this row reads
  correctly because Void Ray is on its in-Meta cooldown. The state one step away — Void Ray **up**,
  a Star granted, AoE — is where position 1 used to stop the scan a rung early, and it is now held:
  `star_yields_to_void_ray` wears `blocked` on
  `identity(transformed) ∧ aoe ∧ ready(void_ray) ∧ !proc(reap)`. The `ready` term keeps the badge
  off rows where the outranker is swiped — without it the badge would eliminate the correct press
  in exactly this scenario. **The alternative was to leave the over-rank documented and undrawn**,
  which is what §7.5 item 1 said until 2026-08-27.
- **⚠ UNSURE — the fourth term is an APPROXIMATION of rung 8, and it under-fires on purpose.**
  Added 2026-08-27, after a post-release review found the cue wrong without it. Rung 8 is
  `!eradicate|!moment_of_craving|4pc`, so **Void Ray being READY is not the same as Void Ray being
  the press**: with both procs banked and no 4-piece the APL skips it and rung 9 is correct — and
  the hold, on readiness alone, badged that correct press `blocked`. That is the one direction this
  catalog refuses, and cue D is argued on exactly the opposite standard. cap cannot express rung
  8's AND, because the overlay channel gives Eradicate and Moment of Craving **one row**, so
  `proc(reap)` is their OR (§7.5, misordering 4). `!proc(reap)` is the strongest thing cap can say
  that stays safe: neither proc up implies `!eradicate`, which implies rung 8 fires. **The
  alternative was to delete cue H** and accept the over-rank as documented-and-undrawn again. What
  is unsure is the residue: with exactly **one** proc banked the hold is now missing and Collapsing
  Star over-ranks by a rung. That is a missed hold rather than a wrong press, which is the right
  direction — but nobody has judged how often that state occurs in play, and a hold that is absent
  in half its window may not be worth its corner. **A flight is what settles it.**
- **⚠ UNSURE — no scenario in this walk exercises cue H, and that is how it shipped wrong.** Every
  scenario that reaches Collapsing Star has Void Ray on cooldown, so the hold never arms in the
  proof. The elimination gate therefore could not have caught the defect above: a gate reasons over
  the states a walk reaches. The honest fix is a scenario in which Void Ray is **ready** and the
  Star is granted; it is not written here, because the state it needs to argue about is the one the
  fourth term was just added to settle, and authoring the walk and the rule in one pass is how the
  first version got through. What is unsure is whether cue H earns its corner at all. Nothing has
  flown. The split also rests on cap's own `/cap aoe` toggle, not on a game read of enemy count.

### M-3 · Single target, counter between 30 and 34

- **State.** As M-2 with `/cap aoe` **off**: transformed, single target, the harvest counter has
  crossed 30 but is under 35, Cull and Void Ray on their in-Meta cooldowns, no Soulburst.
- **CDM row.** ‖ Collapsing Star `press` · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `open` {cues: blocked} · Pierce the Veil `open` ‖ Devour `open`
- **Walk.**
  1. **Collapsing Star** — the counter is above the grant at 30, so the row clears and is position
     1 with nothing ruling it out → **press.**
  2. **Cull / Void Ray / Soul Immolation / Pierce the Veil / Devour** — below the press.
- **Misordering 1.** The APL would bank to 35 first and press Cull or Void Ray here. The cost is
  one to five harvests of a shorter *Impending Apocalypse* chain — the Collapsing Star is not
  wasted, only slightly early. Named and small.
- **⚠ UNSURE — the in-form band is authored at 30, the grant, and not at rung 5's 35.** A band at
  **35** would fix this row outright and would **hatch a row rung 9 wants pressed** in AoE, where
  the rung carries no counter term at all — eliminating a correct press to correct an early one.
  A band at **30** is one band early in single target and never late anywhere. Early beats absent,
  so 30 is what `star_counter` declares, with no `aoe` term on it: the safe direction is the same
  in both modes, and a target-dependent threshold would need a fourth corner claim on a row that
  already cedes three. **The alternative — two `aoe`-gated bands at 30 and 35 — is expressible and
  was declined on that cost.** What settles it is whether the blank corner steps read acceptably
  at all.
- **Position 1.** As M-1, cleared rather than hatched: the counter is above the grant.
- **⚠ UNSURE — this row is DERIVED, not authored.** M-3 was written as a prose delta (*"as M-2
  with `/cap aoe` off"*) with **no row of its own**; the row above was derived by turning the
  toggle off, which is a judgement about the rotation rather than a transcription. It comes out
  **byte-identical to M-2's** — which is the claim to check: the counter's band carries no target
  term, cue **D** is the only AoE-conditioned cue and it sits on a row whose face is Collapsing
  Star here anyway, and Devourer declares no `st_only` / `aoe_only` cue. **The elimination gate
  confirms this row is self-consistent. Nothing confirms it is right.** ⚠ And the two rows being
  identical is now itself the misordering: rung 5 (35+) and rung 9 (AoE) want *different* answers
  from the same pixels.

### M-4 · The window is ending

- **State.** Transformed, Fury under one tick of drain, the harvest counter under 30, Cull and
  Void Ray both on their in-Meta cooldowns, Soul Immolation ready, the Voidsurge already spent.
- **CDM row.** ‖ Collapsing Star `ruled-sealed` {sealed: count-bands} · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `press` · Pierce the Veil `open` ‖ Devour `open`
- **Walk.**
  1. **Collapsing Star** — no Star granted at this counter; the band hatches position 1 → skip.
  2. **Cull / Void Ray** — both spenders swiped → skip.
  3. **Soul Immolation** — reached, and **cue B's badge has cleared**: the client's curve has
     crossed the drain break point, so nothing rules it out → **press.** Rung 13, and the 30 Fury
     that buys another few seconds of form.
  4. **Pierce the Veil / Devour** — below the press.
- **Position 1.** As M-1: the row's face is Collapsing Star and the counter's band is what rules
  it out.
- **Why the state is chosen this way.** Void Ray is free inside Meta and sits at rung 8, above Soul
  Immolation's 13, so while it is up it is the press and the sweep stops there — correctly. Cue B
  is only ever *reached* on a global Void Ray cannot take, which is exactly when the Fury save is
  the question.
- **This is the cue that justifies the row.** A `blocked` badge lit for most of a window that
  clears at the moment the save is worth spending is a single-state marker doing precisely one job.
- **⚠ UNSURE — cue B's break point is fitted, not measured.** It is authored off simc's fitted
  drain curve — ≈16.4 Fury/s at window start, **rising**, and 25 % faster still with *Soul
  Glutton* (`catalog.md` §1c), so the break point is one number per build — and a static threshold
  under-fires late in the window, which is when it matters most. That is the direction that costs the player the
  window. Flown, not assumed (`catalog.md` §8 item 4) — and nothing has flown.

### M-5 · A Voidsurge is owed

- **State.** Transformed, the window's first Pierce the Veil uncast, Cull and Void Ray on cooldown,
  Fury still high, harvest counter under 30.
- **CDM row.** ‖ Collapsing Star `ruled-sealed` {sealed: count-bands} · Cull `cd` · Void Ray `cd` ·
  Soul Immolation `open` {cues: blocked} · Pierce the Veil `press` ‖ Devour `open`
- **Walk.**
  1. **Collapsing Star** — the counter is under 30, so the band hatches position 1 → skip.
  2. **Cull / Void Ray** — both spenders swiped → skip.
  3. **Soul Immolation** — cue **B** has it badged: Fury is still high, so the save is not the
     question yet → skip.
  4. **Pierce the Veil** — the sweep reaches it and presses it → **press.** The right answer,
     reached by elimination rather than by any cue, and one position before the terminus.
  5. **Devour** — the terminus, not reached.
- **Position 1.** As M-1: the row's face is Collapsing Star and the counter's band is what rules
  it out.
- **⚠ UNSURE — the step-3 skip is load-bearing and it is a fitted number.** Unlike M-1, cue B's
  badge here is what lets the sweep *reach* Pierce the Veil. If the badge is dark in this state —
  the fitted break point under-fires late in a window (M-4) — the sweep stops on Soul Immolation
  instead, and the press on the page is not the press the player gets.
- **⚠ UNSURE — cap cannot see the owed cast.** `buff.voidsurge_*` are simc placeholders with no
  game aura (`fact-classification.md` §4.2), so this walk is right **by position rather than by
  knowledge**. In the state where the Voidsurge has **already** been spent, the sweep presses
  Pierce the Veil again where the APL would press Devour — a real, undrawn gap, and the same open
  fact as Havoc's `demonsurge_available` (`catalog.md` §8 item 2). **That state is not on this
  page**, because cap's row for it is identical and only the correct answer differs.


## 7.5 Documented misorderings — what is left after the cues

1. **Position 1 over-ranks Collapsing Star inside the window in ONE direction now, not two**
   (M-3). The face clears the moment a Star is granted at 30 harvests, and it is the leftmost icon
   on the line, so the scan takes it as soon as it is castable:
   - **Single target — still open.** The APL waits for **35** (rung 5) and `star_counter`'s band
     clears at **30**. Cost: a marginally shorter *Impending Apocalypse* chain — the Star is early,
     not wasted. The band is authored at the grant deliberately (M-3's ⚠): a band at 35 would hatch
     a row rung 9 wants pressed, and eliminating a correct press is the worse direction.
   - **AoE — CLOSED 2026-08-27.** The APL puts it at rung **9**, below Void Ray's rung 8, and
     `star_yields_to_void_ray` now wears `blocked` on `identity(transformed) ∧ aoe ∧
     ready(void_ray)`. The `ready` term is what keeps the badge off the rows where Void Ray cannot
     go — M-2 is exactly such a row, and it still presses Collapsing Star.

   ⚠ **This is the shape the 2026-08-27 correction left behind**, and it is the opposite of the
   problem the section it replaced described: the press was not unreachable, it was reachable too
   early. The fix is a **hold** rather than a promotion — nothing needs promoting when the face is
   already the leftmost icon — and it was newly possible because the face has a Cooldown Manager
   frame (`catalog.md` §3, §6). ⚠ The hold's target split rests on cap's own `/cap aoe` toggle and
   on no game read, which is the residual (M-2's ⚠).
2. **Voidblade carries no hold, and that costs twice.** Rung 1 is the branch's **only** out-of-Meta
   Voidblade line, so outside the pre-transform moment this button is never pressed — and cap
   cannot see the sealed fact (the bank at its transform threshold) that says which moment that
   is. Two symptoms, opposite
   in direction:
   - **The sweep stops on it** whenever everything above is swiped or badged and Voidblade is off
     its ~30 s cooldown, where the correct press is Consume. This is why the row is authored
     **last**: at position 5 it absorbs only states that already fell through, instead of stopping
     the sweep on every build global.
   - **The sweep never reaches it** at the transform threshold (B-4), where the APL spends the global on
     Voidblade for *Devourer's Bite*. Cost: one window without the +12 % amp applied in advance.

   **Both are fixed by the same measurement.** `!usable(void_metamorphosis)` is exactly *"the bank
   is below the transform threshold"* (§8, item 3): it would let Voidblade carry a `blocked` hold — killing the first
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
   2-piece up, Consume outranks Collapsing Star's rung 5, Reap, Void Ray and everything below; the sweep
   still stops at whichever Essential icon it reaches first. **Nothing is authored for it by
   design** (§6.1): Soulburst is a Tier-1 registered overlay on Consume and Devour, so the client
   already glows the promotion on the button the player presses, and cap does not draw a second
   mark for a fact Blizzard marks — the same argument that deleted cue E. Whether a cap-owned
   virtual row should mirror the client's glow is a `../render-shelf.md` question.

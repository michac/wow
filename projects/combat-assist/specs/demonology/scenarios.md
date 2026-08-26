---
title: Demonology Warlock — the scenario catalog
spec: Demonology Warlock (Diabolist) — specID 266, hero tree 59, Midnight 12.1
---

# Demonology Warlock (Diabolist) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the cues. This file is the **proof** that lane + cues actually reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. It is what `capart check`'s reading gate mechanises, and it is where this design gets falsified.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/warlock/demonology/simc-apl.md` (Tier 1,
generated, commit `51d49d5`), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## The state walk

Fourteen states, each naming the press, and for **every button that is available and skipped**,
the reason. Buttons the Cooldown Manager has already swiped need no explanation. The walk reads the
authored row order left to right and must satisfy the shape `capart check`'s **elimination gate**
enforces: *the leftmost entry that is neither swiped nor wearing a negative badge is the press.*

Shorthand: "shards" = Soul Shards, "Core" = Demonic Core, "Tyrant" = Summon Demonic Tyrant.
Rungs are positions in `actions.diabolist`.

### The rows are `scenarios.json`; this file is the walk

**The CDM row for every scenario below lives in `scenarios.json` beside this file, which is
canonical and hand-edited.** This document carries the *walk* — what the eye does and why — keyed
by the same ids, and it no longer restates the row. Until this split the row was a
` · `-separated bullet here that a regex scraped into a cache under `previews/data/`; the doc led
and the JSON followed. Now the JSON leads and `capart check` cross-references the two **by id in
both directions**, so a walk with no row and a row with no walk are each a named failure.

**To see a row, look at it** — `previews/demonology-stepper.html` draws every scenario, and the
*Per-ability states* section on the same page draws every state `catalog.json` declares,
including the ones no walk reaches. Reading a row out of a text bullet was always the worse
option; it was only ever there because nothing else held the data.

In the JSON, the ability name is whatever the Cooldown Manager would *display* in that state —
`Ruination`, not `Hand of Gul'dan`, while row 7 is transformed — because that is the identity the
client draws and the swipe follows.

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `open` = shown, in the
scan, with every badge it wears named explicitly in `{cues: …}` — `blocked` from a readable
Lua term or from a sealed band the client paints, `starved` the red affordability badge,
`overcap` the red waste badge, `aoe_only` the mode pawn, `building`/`noproc` the two cards.
`press` = the button an unobstructed scan reaches. ⚠ `press` and `open` render identically, by
design — the press is not something cap draws.

⚠ **`ruled-sealed` is the THIRD eliminating signal, and it is new here.** Until 2026-08-22 there
were exactly two — Blizzard's swipe and cap's negative badge. This is neither: the client
evaluated a **band table cap authored** against an aura count cap never saw, and drew V11's
stripe sheet and a negative mark out of the one FontString the count sink owns. The row reads as
ruled out and wears no cue at all, because a cue is a badge *cap* shows. `capart check`'s
elimination gate knows about it explicitly (`tokens.verdicts.ruled-sealed.eliminates`); nothing
about it is inferred.

⚠ **`{sealed: …}` is an annotation channel, not a cue**, and it names the SINK rather than the
picture: `count-bands` (V16/V17), `count-bar` (V18), `pandemic` (V19). It appears on a row
exactly where that display is **drawing something in that state** — so a band at a resting value,
or an aura that is not up at all (in which case the client hides the whole button and no sink on
it draws anything), carries no annotation. What VALUE the client found is deliberately nowhere in
this file: that is the one thing cap cannot know.

⚠ **No entry in this catalog wears a positive cue**, so every scenario here is judged by pass 2
of `../render-shelf.md` Part 0.5, elimination. Why Demonology declines both positive cues is
argued in `catalog.md` (*Why this catalog does not spend a positive cue*).

⚠ **Three states were once structurally absent from this walk**, and each entered it the day
the vocabulary it needed was promoted: DEM-13 and DEM-14 on 2026-08-22 (V16/V17), and DEM-15 on
2026-08-24 (the two-sided band, `catalog.md` → *Defeats*, item 1 — closed). The section at the
end keeps the history, because "cap could not draw this and said so" is the discipline the walk
is built on.

### DEM-1 · Opener, everything ready, 3 shards, no Core

- **State.** Pull timer at zero, every cooldown up, **3 Soul Shards** from the precombat sequence,
  **no Demonic Core**, single-target mode. Reign of Tyranny talented.
- **Walk.**
  1. **Power Siphon** — ready, nothing rules it out → **press.** Rung 1, whose condition is
     `buff.demonic_core.stack<=1`, and at zero Cores that is true.
  2. Everything else is read only if the eye goes looking — and what it finds is the ramp
     stated: the whole summon block and Hand of Gul'dan wear the `building` card (Tyrant is
     ready, shards are 3), Implosion wears `blocked` from `implosion_no_imps` (cue H — no Wild
     Imp is out yet, so its sealed band has no button to draw on), and Demonbolt wears the
     `noproc` empty card at zero Cores.
- **Eye-direction.** ⚠ **The opener's press is still position 1, and everything behind it now
  says why it is not the press.** Until 2026-08-24 this read "cap draws nothing at all"; the
  ramp holds (cue I, `catalog.md` changelog) changed that deliberately — the pilot's reading is
  that the held summons SHOULD look held, the whole block hatched red as one statement, while
  the board is built. Retribution had to promote its opener because its rung-1 press sat
  seventh from the left; Demonology's sits first, so the cards cost the walk nothing.
  ⚠ This is also the first scenario to wear cue **H** — the one state Implosion's sealed band
  structurally cannot reach (no aura, no button), covered by the readable `aura` latch.
- **Density.** No budgeted hold before the press (the press is first); `building` and `noproc`
  are unbudgeted (Part 0.5 — one fact, a block of subjects).
- **Cue set.** Ramp hold (I) → **have**, five subjects. No-imps (H) → **have**. Core hold (C) →
  **have**, as the `noproc` card. Nothing else fires.

### DEM-2 · Power Siphon spent, the summon block

- **State.** One global later. Power Siphon is on cooldown and **granted two Demonic Cores**;
  Grimoire, Summon Doomguard and Call Dreadstalkers are all up, Tyrant is up, shards still 3.
  No Wild Imp is out yet.
- **Walk.**
  1. **Power Siphon** — on cooldown → skip.
  2. **Grimoire: Imp Lord … Summon Demonic Tyrant** — every summon wears the `building` card
     over a red hatch: Tyrant is READY and shards are 3, so the ramp holds the whole block
     while the board is built to five → skip.
  3. **Implosion** — `blocked` from cue H, no imps out → skip.
  4. **Hand of Gul'dan** — the `building` card: rung 11's `remains>5` is false with Tyrant
     ready, so the shards belong to the window → skip.
  5. **Demonbolt** — **press.** Power Siphon's two Cores are up (the `noproc` card is dark),
     shards are below four — rung 14, and each cast banks two shards toward the five Tyrant
     wants. The V18 bar shows the two Cores; the V20 proc bar above it is the older Core's
     remaining lifetime, drained by the client — this many banked, this long to use one.
- **Eye-direction.** ⚠ **This scenario is the ramp reading, stated — and it is authored PAST
  the APL.** Rungs 3–6 would press Grimoire here; the pilot holds the summons and builds to
  five instead (`catalog.md` changelog 2026-08-24, playtest-gated). The earlier stance — skips
  for half the row are the wrong tool, promote the press instead — is relaxed, not repealed:
  five cards are ONE statement (*the board is below five shards*) worn by a block, and the gate
  to a `priority` on the builder stays open if the hatched block reads as noise in a pull.
  ⚠ **The row shows whichever Grimoire is talented, and cap binds both ids as one entry.** This
  is a **choice node**, not an R7 transform — the two have separate Essential rows (OrderIndex
  6 and 36) and the catalog's `alt` field covers it. A build with Fel Ravager reads this
  scenario with `Grimoire: Fel Ravager` in the same position.
- **Density.** No budgeted hold — every card here is unbudgeted `building`, one fact worn by a
  block (Part 0.5).
- **Cue set.** Ramp hold (I) → **have**, five subjects. No-imps (H) → **have**. The Core bar
  (V18) and the Core proc bar (V20) → **drawing**, stacked on the press itself.

### DEM-3 · Dreadstalkers ready, Tyrant 30 s out — the window is open

- **State.** Mid-fight, single target, DEM-4's build (To Hell and Back not talented). Power
  Siphon, Grimoire and Summon Doomguard are on cooldown. Call Dreadstalkers is ready and
  **Tyrant has ~30 s left**. Reign of Tyranny talented, 3 shards, no Demonic Core, three Wild
  Imps out.
- **Walk.**
  1. **Power Siphon … Summon Doomguard** — on cooldown → skip.
  2. **Call Dreadstalkers** — ready, and rung 6's first clause holds: 30 s is at least
     `20 + gcd` → **press.** Right of it, the row keeps stating what it knows: Implosion wears
     the pawn and its red imp count, Demonbolt the empty card at zero Cores — none of which
     the walk has to read, because the press came first.
- **Eye-direction.** ⚠ **The dogs' two-sided band (cue J) is authored now, and here it is
  correctly SILENT.** 30 s is past the band's upper edge (`within = 21.5`), which is rung 6's
  own press condition — so the row is right by cap's arithmetic rather than, as this note used
  to say, by luck of position. The state at 16 s — inside the dead zone — is **DEM-15**.
  ⚠ Both of the band's edges are sealed: cap authors `(10.5, 21.5)` and never learns where the
  clock is, so this silence is confirmed by eye in game, not by a capture.
- **Cue set.** Dogs' window (J) → correctly **dark**, past the upper edge. Ramp hold (I) →
  dark — Tyrant is not ready. Single-target skip (G) → **have**. Core hold (C) → **have**, the
  `noproc` card. The imp band (V16) → **drawing** its red `3` on Implosion. (⚠ All three were
  missing from this row until 2026-08-25 — it predates the band-everywhere sweep and was the
  one mid-fight scenario the sweep skipped.)

### DEM-4 · Tyrant ready at 2 shards — the readable hold, and the filler underneath

- **State.** Mid-fight, single target. Every summon is on cooldown. **Tyrant is ready and Soul
  Shards are 2.** No Demonic Core. Implosion is up and **three Wild Imps are out**. **To Hell
  and Back is not talented** — on a build that takes it, Implosion is a single-target press and
  row 6 wears no pawn.
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — ready, and the `building` card lights on the exact readable
     predicate `resource < 5`. Rung 8 is `soul_shard=5`; pressing a one-minute cooldown at two
     shards spends the window on a half-built board → skip.
  3. **Implosion** — available, and the `aoe_only` pawn lights from `implosion_st_only`: the AoE
     toggle is off and To Hell and Back is not talented → skip. ⚠ **Not `blocked`** — nothing is
     held and nothing would be wasted; the imps are simply worth more attacking.
  4. **Hand of Gul'dan** — `starved`. It costs three shards and there are two, which Blizzard has
     already tinted the icon for → skip. (Its `building` card needs affordability and stays
     dark — a starved row does not also wear the ramp's card.)
  5. **Demonbolt** — the `noproc` empty card from `db_awaits_core`: no Demonic Core, and
     Demonbolt appears in the APL only gated on one → skip.
  6. **Shadow Bolt** — **press.** Rung 15, the filler, reached entirely by subtraction.
     Implosion, back at row 6, is also carrying its imp band — the client's `3` on the corner
     plate over the gold hatch: three of the six imps rung 9 wants.
- **Eye-direction.** ⚠ **This is the state the whole catalog is built around, and the card on
  row 5 is the point of it.** Holding a *ready* one-minute cooldown is the strongest claim cap
  makes anywhere in this spec, and it is safe to make because Soul Shards are **never-secret** —
  the term is `{ "resource", "<=", 4 }`, an exact Lua comparison, not a curve handed to the
  client. Havoc's equivalent decision rests on a sealed Fury readout and can only be *shown*;
  this one can be *reasoned about*.
- **Density.** No budgeted hold at all since the 2026-08-24 re-badges: row 5 wears unbudgeted
  `building` and row 8 unbudgeted `noproc`; `starved` and `aoe_only` were never budgeted. The
  walk still steps over four marks to reach the press, which is the reading Part 0.5's budget
  deliberately does not count — each restates a fact the player already has.
- **Cue set.** Five-shard hold (A) → **have**, as the `building` card. Single-target skip (G) →
  **have**. Starved (E) → **have**. Core hold (C) → **have**, as the `noproc` card. The imp
  band (V16) → **drawing** its numeral on Implosion.

### DEM-5 · Tyrant ready at 5 shards — press it

- **State.** As DEM-4, but **Soul Shards are 5**. A Demonic Core is up; the three imps still are.
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — `tyrant_awaits_shards` requires `resource < 5`, which is false
     here, so the badge is dark → **press.** Rung 8.
- **Eye-direction.** The badge going *out* is what says "now". Row 5 is the only row in this
  catalog whose hold releases on a resource the player is actively building, so the transition is
  the signal and cap needs no second mark for it.
- **Cue set.** Nothing fires on the press — the `building` cards all released at five, which is
  the transition doing the talking. Demonbolt still wears `overcap` at five shards (cue B),
  which is correct and which the walk never reaches; its two bars draw with the Core.

### DEM-6 · 4 shards, Core up, Tyrant far — Hand of Gul'dan, and the Core waits

- **State.** Mid-fight, single target, DEM-4's build (no To Hell and Back). Every summon on
  cooldown, **Tyrant ~40 s out**, **4 Soul
  Shards**, a **Demonic Core up**, four Wild Imps out.
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Hand of Gul'dan** — affordable at four shards, and `hog_awaits_tyrant`'s sealed band is
     nowhere near range at 40 s → **press.** Rung 11:
     `soul_shard>=3&cooldown.summon_demonic_tyrant.remains>5`.
  4. **Demonbolt** — wearing `overcap` at four shards, and it never gets the chance to compete.
- **Eye-direction.** ⚠ **This is the pilot's hypothesis, corrected.** `../spec.md` §3.4 proposed
  dimming a live Demonic Core "above three shards"; the APL's term is `soul_shard<4`, so the
  badge belongs at **four**. At three shards a Demonbolt leaves five, which is exactly full and
  is not waste — and DEM-8 is that state, where the badge is correctly dark.
- **Cue set.** Overcap (B) → **have**, readable, and gated on `proc(demonbolt)` so it never lands
  on a Demonbolt that has no Core to spend. The Core bar (V18) and proc bar (V20) → **drawing**;
  the imp band (V16) → **drawing** its `4` on Implosion.

### DEM-7 · 3 shards, Tyrant 4 s out — bank for the window

- **State.** As DEM-6, but **Tyrant's cooldown has ~4 s left** and shards are **3**. A Demonic
  Core is up.
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Hand of Gul'dan** — affordable, but `blocked` lights from `hog_awaits_tyrant`: Tyrant's
     cooldown ends within 5 s and shards are below five, so rung 11's
     `cooldown.summon_demonic_tyrant.remains>5` is false and the shards belong to the window →
     skip.
  4. **Demonbolt** — a Core is up and shards are below four, so both of its readable badges are
     dark → **press.** Rung 14, which also generates two shards toward the five Tyrant wants.
- **Eye-direction.** ⚠ **Cues A and F are one rule read from two sides**, and this is the half
  that has to be sealed. Tyrant holds *itself* below five shards, which cap can compare exactly;
  Hand of Gul'dan holds *itself* while Tyrant is nearly here, which cap can only hand to the
  client as a five-second window. ⚠ The band is **sealed** — cap authors the window and never
  learns where inside it the value fell — so this is confirmed by eye in game, not by a capture.
  ⚠ It reads nothing at zero remaining, which is correct: at zero, Tyrant is ready and row 5 is
  the press.
- **Density.** One budgeted hold before the press. Well inside Part 0.5.
- **Cue set.** Tyrant bank (F) → **sealed**. Overcap (B) → dark, at three shards. The Core bar
  (V18) and proc bar (V20) → **drawing**, on the press itself.

### DEM-8 · 1 shard, Core up — the Core is the press

- **State.** Single target, everything on cooldown, **1 Soul Shard**, a **Demonic Core up**,
  Tyrant far away, two Wild Imps out. **Doom is talented and the target's Doom is inside its
  pandemic window.**
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Hand of Gul'dan** — `starved` at one shard against a cost of three → skip.
  4. **Demonbolt** — **press.** Rung 14. All three of its markers are dark: a Core is up
     (cue C), shards are below four (cue B), and row 9 is not transformed (cue D).
- **Eye-direction.** The plainest state in the catalog, and it is worth having in the walk
  precisely because **three markers are simultaneously off**. A row whose badges only ever light
  is a row nobody can read.
  ⚠ **This is also the densest row in the catalog, and it is here on purpose.** Demonbolt is
  wearing **three sealed displays at once** — V18's segmented bar on the bottom edge (how many
  Cores are banked; red across its whole width at four: stop banking), V20's proc bar directly
  above it (the Core's own remaining lifetime, drained by the client), and V19's refresh badge
  on the corner (the client saying that refreshing Doom now clips nothing). None of them share
  a pixel — the two bars stack on the bottom edge by V20's static lift rule, and the corner
  belongs to the window badge alone since the dial re-formed onto the edge (2026-08-25) — so
  the question the flight is for is whether the three together read as one statement, not
  whether they collide; nothing else in this walk puts three client-drawn things on one row.
  ⚠ **The window badge is GATED ON THE TALENT, not on the aura.** Without Doom talented the fact
  does not exist, and a display armed for it would sit dark forever with no way to tell that from
  a client refusal. The gate is readable and contributes no cue — it decides only whether the
  client is allowed to paint the sealed display at all.
  ⚠ **cap authors NO threshold for the window.** The client computes
  `GetRefreshExtendedDuration − GetAuraBaseDuration` itself, per spell, which is Blizzard's real
  pandemic rather than the community's 30 %. Reproducing the same picture from a duration band
  would be cap's guess wearing the same pixels.
- **Cue set.** Starved (E) → **have**. Nothing else fires. Three sealed displays draw on one
  row (V18, V19, V20), and the imp band (V16) draws its `2` on Implosion.

### DEM-9 · Ruination armed — row 7 is a different button

- **State.** Diabolic Ritual has cycled to **Pit Lord** and its Art is armed, so **row 7 is
  displaying Ruination**. Single target, **2 Soul Shards**, a Demonic Core up, three Wild Imps
  out, Tyrant on cooldown.
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Ruination** — **press.** Rung 10, which sits above the ordinary Hand of Gul'dan and below
     everything else — exactly where row 7 already is, so the identity needs no cue to carry it.
- **Eye-direction.** ⚠ **`hog_starved` stays dark at two shards, and that is the whole reason it
  reads the live id.** `Sense.buildReads` asks affordability of `info.override or row.primary`,
  so on the transformed row this is **Ruination's** cost, which is none. Read on the base id it
  would light at two shards against Hand of Gul'dan's three, and the walk would step past a free
  press. One marker covers both lives of the row correctly.
  ⚠ **Which row Ruination rides is Tier-2 evidence and is marked.** The Tier-1 hero-talent string
  says "Chaos Bolt", which Demonology does not have; six Warcraft Logs parses say Hand of Gul'dan
  with 1:1 cast counts (`fact-classification.md` §3). If that is wrong, this scenario does not
  merely mis-order — Ruination is drawn on no row at all. @verify-ingame
- **Cue set.** Identity (R7) → **have**. Nothing else fires.

### DEM-10 · Infernal Bolt armed at 2 shards — the filler outranks the proc

- **State.** Diabolic Ritual has cycled to **Mother of Chaos** and its Art is armed, so **row 9
  is displaying Infernal Bolt**. Single target, **2 Soul Shards**, a **Demonic Core up**, three
  Wild Imps out, Tyrant ready.
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — the `building` card at two shards, cue A → skip.
  3. **Implosion** — the `aoe_only` pawn → skip.
  4. **Hand of Gul'dan** — `starved` at two shards → skip.
  5. **Demonbolt** — `blocked` from `db_yields_to_infernal_bolt`: row 9 reads
     `identity == transformed` **and** shards are below three, which is rung 12 outranking rung
     14 exactly → skip.
  6. **Infernal Bolt** — row 9 reads `identity == transformed`, so band 1 gives it **ROTATION**
     instead of FALLBACK → **press.** Rung 12, and it generates three shards, which is the whole
     reason it outranks a Demonbolt here.
- **Eye-direction.** ⚠ **This is the scenario the row order is built for, and it is the first
  marker in any catalog that reads a different row's identity.** Read as flat rungs the order is
  Infernal Bolt (12) → Demonbolt (13, 14) → Shadow Bolt (15) — one row above, then below, the
  same neighbour — and a fixed row order cannot say that. cue **D** says it instead, and both of
  its terms are readable: `identity` is R7 and Soul Shards are never-secret. **No sealed
  vocabulary is spent on the hardest ordering decision in the spec.**
  ⚠ **This is also V20's first consumer, and the state it earns its pixels in.** Demonbolt is
  HELD (cue D's clock badge, red-only in the corner) while the proc bar above its charge bar
  drains the Core's remaining lifetime — *not now* and *but the proc expires* are two facts,
  the badge column carrying the verdict and the edge carrying the quantity. (The corner-dial
  form of this display lasted one day: gold in the badge column beside the red hold read as
  two verdicts arguing — the stepper-feedback finding that re-formed V20 onto the edge.) And
  row 9 wears its own proc bar: the armed Art's remaining lifetime under the press itself
  — ⚠ its aura id is Tier-3-sourced and dies silent if wrong; flight question.
- **Density.** One budgeted hold (row 8's `blocked`, cue D) before the press — row 5's card is
  unbudgeted `building`. Under budget.
- **Cue set.** Infernal-Bolt yield (D) → **have**. Five-shard hold (A) → **have**, as the
  `building` card. Starved (E) → **have**. The Core bar (V18) and proc bar (V20) →
  **drawing**, stacked on Demonbolt's bottom edge; the Art's proc bar (V20) → **drawing** on
  Infernal Bolt.

### DEM-11 · Infernal Bolt armed at 4 shards — and it loses

- **State.** As DEM-10, but **4 Soul Shards** and Tyrant on cooldown. Row 9 is still displaying
  Infernal Bolt; a Demonic Core is up, the three imps still out.
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Hand of Gul'dan** — affordable, Tyrant far → **press.** Rung 11.
  4. **Demonbolt** — `overcap` at four shards; it never competes.
- **Eye-direction.** ⚠ **The transform does not promote by itself, and this is the scenario that
  proves it.** Rung 12 is `infernal_bolt,if=soul_shard<3`; at four shards it does not fire, and
  the armed Infernal Bolt is simply a better filler waiting its turn. Cue D carries the
  `resource < 3` term for exactly this reason — without it, Demonbolt would be held here too and
  the walk would run off the right edge of the row to a button the APL does not want.
- **Cue set.** Overcap (B) → **have**. Cue D → correctly **dark**.

### DEM-12 · AoE mode on, 4 targets, imps banked — Implosion

- **State.** The player has flipped cap's AoE toggle; four targets, **six or more Wild Imps out**
  after a Hand of Gul'dan chain, **3 Soul Shards**, Tyrant ready, To Hell and Back **not**
  talented, and **no Demonic Core up**.
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — the `building` card at three shards, cue A → skip.
  3. **Implosion** — the `aoe_only` pawn requires the toggle to be **off**, and it is on, so the
     badge is dark → **press.** Rung 9, which outranks both Ruination and the ordinary Hand of
     Gul'dan. (Hand of Gul'dan, one row right, wears the ramp's card — Tyrant is ready at three
     shards — which the walk never reaches; the imps are already banked and Implosion outranks
     the spend either way.)
- **Eye-direction.** ⚠ **The 3-target threshold is the player's, not cap's.** Rung 9 reads
  `active_enemies>2`, and **cap models no enemy count** — the toggle is the whole interface, as
  it is on Havoc and Retribution. This scenario says what the badge does once the toggle is on,
  not when to flip it.
  ⚠ **Whether there are six imps is still a fact cap does not have — and it no longer has to.**
  The rung's other half, `buff.wild_imps.stack>=6`, is a sealed count, and cap hands the client a
  band table rather than reading it: at six or more the upper band draws the count in **gold**
  (2026-08-25 — it used to emit nothing, and a loaded Implosion looked identical to an
  unremarkable one): *six banked, the press is loaded*. No hatch — a positive band may not
  wear one. **DEM-13 is the state below six**, which this walk could not contain until
  2026-08-22.
- **Cue set.** Single-target skip (G) → correctly **dark**. Five-shard hold (A) → **have**, as
  the `building` card; ramp hold (I) → **have**, on Hand of Gul'dan. The imp band → **drawing
  its gold `6`** on the press itself.

### DEM-13 · AoE mode on, three imps out — the count rules the row out

- **State.** As DEM-12 — AoE toggle on, four targets, **3 Soul Shards**, To Hell and Back not
  talented, no Demonic Core up — except that a Hand of Gul'dan chain has **not** landed, only **three Wild Imps**
  are out, and **Tyrant is ~40 s out**. (⚠ Until 2026-08-24 this line inherited "Tyrant ready"
  from DEM-12 while the walk below said "Tyrant far" — the walk was always the truth: rung 11
  does not fire with Tyrant ready at three shards, so a ready Tyrant would make Hand of
  Gul'dan a held row, not the press. The ramp cues made the contradiction visible.)
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn is dark, because the toggle is on. What rules the row out
     instead is the **client**: cap handed it a two-band table over the Wild Imp application
     count, and below six the lower band draws V11's stripe sheet, a plate and the numeral out
     of one FontString → skip. Rung 9's `buff.wild_imps.stack>=6` is false and the row says so.
  3. **Hand of Gul'dan** — affordable at three shards, Tyrant far → **press.** Rung 11, and it is
     also the button that builds the imps Implosion is waiting for.
- **Eye-direction.** ⚠ **This is the state DEM-12 could not contain, and it is the first time a
  SEALED fact eliminates rather than merely decorates.** Every eliminating signal before it was
  Blizzard's swipe or a badge cap decided to show; this one is a rule cap wrote, evaluated by the
  client against a number cap never receives. The walk is unchanged in shape and the row is
  legible for the first time in this state.
  ⚠ **It is the COMPLEMENT, and that direction is not free.** A red mark on a *rising* count
  inverts a fact the player experiences as progress, so it would be a lie on Demonic Core. Here it
  is literally true — below six imps Implosion is a damage loss, which is exactly what the rung
  says — and that is the whole test for whether a complement belongs on a row.
  ⚠ **The boundary is at six and takes the UPPER band.** `threshold` is documented as the minimum
  input a rule applies to, so at exactly six imps the hatch clears and the numeral turns gold
  (DEM-12) — the row becomes a candidate wearing its own ammunition count. An off-by-one here
  is invisible until it is wrong in a pull.
  ⚠ **At ZERO imps there is no aura and therefore no button, so no sink on it draws at all.** That
  state is covered by a readable marker instead (`implosion_no_imps`, on the `aura` latch), which
  is the one thing a sealed display structurally cannot reach.
- **Density.** One client-drawn elimination before the press; no budgeted hold.
- **Cue set.** Five-shard hold (A) → **dark** — Tyrant is on cooldown, and the 2026-08-24 state
  correction removed the hold this line used to claim. Single-target skip (G) → correctly
  **dark**. The imp band (V17) → **drawing**, and it is what makes this scenario expressible.

### DEM-14 · Two Cores banked — Power Siphon rules itself out

- **State.** Mid-fight, single target, DEM-4's build. **Power Siphon is ready** and **two Demonic
  Cores are banked**. 4 Soul Shards, Tyrant ~40 s out, three Wild Imps out, Grimoire and Summon
  Doomguard on cooldown.
- **Walk.**
  1. **Power Siphon** — ready, and the client rules it out: the band table over the Demonic Core
     count is silent below two and hatches at two → skip. Rung 1's `buff.demonic_core.stack<=1` is
     false, and pressing it here converts two imps into Cores you are already holding.
  2. **Grimoire … Summon Demonic Tyrant** — on cooldown → skip.
  3. **Implosion** — the `aoe_only` pawn → skip.
  4. **Hand of Gul'dan** — affordable at four shards, Tyrant far → **press.** Rung 11.
- **Eye-direction.** ⚠ **This is the worst place in the row for an un-ruled-out entry, and it was
  un-ruled-out until 2026-08-22.** Power Siphon is position 1: a walk that stops on it stops
  immediately, so `catalog.md`'s second defeat cost the reading model more than any other gap in
  the spec. It is closed by the ORDINARY direction of the same primitive DEM-13 uses inverted —
  silent while the row is a candidate, marked when it is not.
  ⚠ **Demonbolt's arc is drawing here at two of four Cores**, and this is the scenario to judge
  V18's real cost against: a bar has **no blank state**, so the track is on the row at every value
  the aura is up for. It says *how many more*, continuously, which nothing else in this catalog
  answers — and it is a permanent mark on a row that also wears `overcap`.
- **Density.** One client-drawn elimination and one mode pawn before the press. No budgeted hold
  at all.
- **Cue set.** Overcap (B) → **have**. Single-target skip (G) → **have**. The Core band (V16) →
  **drawing**, on Power Siphon; the imp band (V16) → **drawing**, on Implosion. The Core bar
  (V18) and proc bar (V20) → **drawing**, on Demonbolt.

### DEM-15 · Dreadstalkers in the dead zone — waiting on Tyrant's cooldown

- **State.** Reign of Tyranny build, mid-fight, single target. **Call Dreadstalkers is ready
  and Summon Demonic Tyrant's cooldown has ~16 s left** — inside rung 6's hold zone. 3 Soul
  Shards, no Demonic Core, two Wild Imps out; Power Siphon, Grimoire and Summon Doomguard on
  cooldown.
- **Walk.**
  1. **Power Siphon … Summon Doomguard** — on cooldown → skip.
  2. **Call Dreadstalkers** — `blocked` from `dreadstalkers_awaits_tyrant`: 16 s is inside the
     two-sided band `(10.5, 21.5)`, so recast dogs would come back too late for the window and
     casting now wastes the extension → skip. (Its `building` card is dark — Tyrant is not
     ready.)
  3. **Summon Demonic Tyrant** — on cooldown → skip.
  4. **Implosion** — the `aoe_only` pawn → skip.
  5. **Hand of Gul'dan** — affordable at three shards, and rung 11's `remains>5` holds at 16 s
     → **press.**
- **Eye-direction.** ⚠ **This is the state the walk deliberately did not contain from
  2026-08-19 to 2026-08-24** — *The states this walk once could not contain*, item 1 — and it
  enters the walk the day its band was buildable, not a day earlier. The hold is rung 6's own
  dead zone read as elimination: both edges are cap's authored numbers (the unhasted 1.5 s
  floor, because `UnitSpellHaste` is sealed in instanced combat) and **both edges are sealed in
  evaluation** — cap never learns where the clock is, so this scenario is confirmed by eye in
  game, not by a capture. At 5 s or at 30 s the band is silent and the dogs are the press
  (DEM-3 is the far half).
  ⚠ **The two-sided curve itself is unflown** — the one-sided senses are, severally, the same
  measured machinery, but no client has evaluated a three-point band. `catalog.md` → *Defeats*,
  item 1 carries the closure.
- **Density.** One budgeted hold (the dogs' `blocked`, cue J) before the press. Under budget.
- **Cue set.** Dogs' window (J) → **sealed**, drawing. Core hold (C) → **have**, the `noproc`
  card on a row right of the press. Ramp hold (I) → dark everywhere — Tyrant is not ready.

### DEM-16 · Ruination armed during the ramp

- **State.** Diabolist build, mid-fight, single target. **Ruination is armed, so row 7 is
  showing Ruination rather than Hand of Gul'dan**. Summon Demonic Tyrant is READY at 3 Soul
  Shards — the ramp — with no Demonic Core and two Wild Imps out; Power Siphon on cooldown.
- **Walk.**
  1. **Power Siphon** — on cooldown → skip.
  2. **Grimoire: Imp Lord … Summon Demonic Tyrant** — four `building` cards, one statement: the
     ramp is open and the board is not built, so nothing here is spent below five shards → skip.
  3. **Implosion** — the `aoe_only` pawn on a single target → skip.
  4. **Hand of Gul'dan** — showing **Ruination**, and it wears nothing at all → **press.**
- **Eye-direction.** ⚠ **This is the walk that proves the identity gate on the two window
  holds.** Both `hog_awaits_tyrant` and `hog_awaits_shards` are derived from **rung 11**, the
  conditional Hand of Gul'dan spend. Rung 10 — Ruination — sits *above* it and carries **no
  condition of any kind**, the only rung in `actions.diabolist` that does not. Until
  2026-08-26 neither hold said which life it belonged to, so in exactly this state the row wore
  `building` (Tyrant ready, three shards) and the reader was told to hold a button the priority
  list presses unconditionally. `identity(hand_of_guldan, "base")` on both holds is the fix, and
  this row is what it looks like from the player's side: five holds to the left, and the one
  transformed row clean.
  ⚠ **Cue E cannot fire here either, and not because it is gated.** Ruination costs no shards,
  and `hog_starved` asks affordability of the LIVE id — so on the transformed row it is
  structurally false rather than suppressed.
- **Density.** Four `building` cards and one `aoe_only` pawn before the press — but the four are
  the ramp block saying one thing (`../render-shelf.md` Part 0.5 deliberately does not count a
  block as four holds). Under budget.
- **Cue set.** Ramp hold (I) → **drawing**, on the four rows the ramp gates. Window hold (F) →
  dark, gated out by identity. Core hold (C) → **have**, right of the press. Starved (E) → dark.

---

## The states this walk once could not contain

⚠ **All three are in the walk now, and the section stays because the discipline is the
point.** `capart check`'s elimination gate requires the leftmost un-ruled-out entry to be the
press; while a state's ruling-out could not be drawn, writing it as a scenario would have meant
asserting a reading the player cannot perform — so it was named here instead, with the rung it
died on and what would reopen it. Each entered the walk the day its vocabulary existed and not
a day earlier:

1. **Call Dreadstalkers in the Tyrant dead zone** — the two-sided band `Catalog.Check` used to
   refuse outright. Reopened 2026-08-24 by exactly the named recipe (`Channel.BandPoints`, a
   three-point Step list) and now **DEM-15**.
2. **Power Siphon with Cores banked** — closed 2026-08-22 as **DEM-14**, by V16's promotion out
   of the lab (a catalog may not cite a lab entry, so the fact was expressible and unusable at
   the same time).
3. **Implosion below six imps** — the same primitive inverted, closed the same day as
   **DEM-13**.

**None was ever a client limit.** The secrets are numbers, `../spec.md` §3.6 says a threshold
on a secret is expressible as a rule the client evaluates, and in each case the missing thing
was authored vocabulary with a named shape — which is a different and much better thing than
"cap cannot do this".

**What the walk did not have to explain.** No state above required cap to know a target count, an
aura duration, a cooldown's remaining *value*, an aura stack count, or which Demonic Art was
armed. Every skip is a readable Lua term, a sealed band on one cooldown (DEM-7's one-sided,
DEM-15's two-sided), or a band table the client evaluated against a count cap never received
(DEM-13, DEM-14).

**Sixteen states, no promotion.** Retribution spends its one positive cue on an opener whose
press sits seventh from the left; Demonology's rung-1 press sits **first**, and no state in this
walk stands more than two budgeted holds between the left edge and the press (the ramp's
`building` cards are one statement worn by a block, and Part 0.5 deliberately does not count
them). A vocabulary where
the positive cue is reached often has stopped being a reading model and become a pointer
(`../render-shelf.md` Part 0.5).

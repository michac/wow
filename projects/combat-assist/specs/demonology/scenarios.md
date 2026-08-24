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

### The **CDM row** bullet is machine-read

Every scenario below carries a `- **CDM row.**` bullet in a fixed grammar — nine entries in
authored order, separated by ` · `, each `<Ability> \`<verdict>\``.
`wowkb.capart import scenarios demonology` scrapes it into the preview's sidecar and
`wowkb.capart check demonology` re-scrapes it and fails if the two disagree, so **this document
leads and the preview follows**. The ability name is whatever the Cooldown Manager would
*display* in that state — `Ruination`, not `Hand of Gul'dan`, while row 7 is transformed —
because that is the identity the client draws and the swipe follows.

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `hold-readable` /
`hold-sealed` = the red `blocked` badge, from a readable Lua term or from a sealed band the
client paints. `starved` = the red affordability badge. `overcap` = the red waste badge.
`off-mode` = the mode pawn. `press` = the button an unobstructed scan reaches. `below` = shown,
but the walk never got there. ⚠ `press` and `below` render identically, by design — the press is
not something cap draws.

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

⚠ **One state is deliberately absent from this walk**, and its absence is the finding rather than
an omission — see *The state this walk does not contain*, at the end. Two others were absent until
2026-08-22 and are now DEM-13 and DEM-14, which is what V16/V17 bought.

### DEM-1 · Opener, everything ready, 3 shards, no Core

- **State.** Pull timer at zero, every cooldown up, **3 Soul Shards** from the precombat sequence,
  **no Demonic Core**, single-target mode. Reign of Tyranny talented.
- **CDM row.** Power Siphon `press` · Grimoire: Imp Lord `below` · Summon Doomguard `below` ·
  Call Dreadstalkers `below` · Summon Demonic Tyrant `below` · Implosion `below` ·
  Hand of Gul'dan `below` · Demonbolt `below` · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon** — ready, nothing rules it out → **press.** Rung 1, whose condition is
     `buff.demonic_core.stack<=1`, and at zero Cores that is true.
  2. Everything else is read only if the eye goes looking. The whole COOLDOWN block is up and
     the two spenders are affordable; none of that has to be interpreted to find the press,
     because the press is the leftmost entry.
- **Eye-direction.** ⚠ **The opener is the one state where a fixed row order is free.** Every
  rung above the fillers is simultaneously live, so left-to-right *is* the APL, and cap draws
  nothing at all. Retribution had to promote its opener because its rung-1 press sat seventh from
  the left; Demonology's sits first.
- **Cue set.** Nothing fires.

### DEM-2 · Power Siphon spent, the summon block

- **State.** One global later. Power Siphon is on cooldown; Grimoire, Summon Doomguard and Call
  Dreadstalkers are all up, Tyrant is up, shards still 3.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `press` · Summon Doomguard `below` ·
  Call Dreadstalkers `below` · Summon Demonic Tyrant `below` · Implosion `below` ·
  Hand of Gul'dan `below` · Demonbolt `below` · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon** — on cooldown → skip.
  2. **Grimoire: Imp Lord** — ready, nothing rules it out → **press.** Rungs 3 and 4, which the
     APL lists unconditionally because exactly one of the two exists on any build.
- **Eye-direction.** ⚠ **The row shows whichever Grimoire is talented, and cap binds both ids as
  one entry.** This is a **choice node**, not an R7 transform — the two have separate Essential
  rows (OrderIndex 6 and 36) and the catalog's `alt` field covers it. A build with Fel Ravager
  reads this scenario with `Grimoire: Fel Ravager` in the same position.
- **Cue set.** Nothing fires.

### DEM-3 · Dreadstalkers ready, Tyrant 30 s out — the window is open

- **State.** Mid-fight. Power Siphon, Grimoire and Summon Doomguard are on cooldown. Call
  Dreadstalkers is ready and **Tyrant has ~30 s left**. Reign of Tyranny talented, 3 shards.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `press` · Summon Demonic Tyrant `cd` · Implosion `below` ·
  Hand of Gul'dan `below` · Demonbolt `below` · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon … Summon Doomguard** — on cooldown → skip.
  2. **Call Dreadstalkers** — ready, and rung 6's first clause holds: 30 s is at least
     `20 + gcd` → **press.**
- **Eye-direction.** ⚠ **This scenario is the *good half* of a condition cap cannot draw.** Rung
  6 is a two-sided window and cap authors neither side (`catalog.md` → *Defeats*, item 1), so at
  30 s out the row is right by luck of position rather than by anything cap concluded. At 16 s
  out it would be wrong and cap would still say nothing — which is why the state at 16 s is not
  in this walk.
- **Cue set.** Nothing fires.

### DEM-4 · Tyrant ready at 2 shards — the readable hold, and the filler underneath

- **State.** Mid-fight, single target. Every summon is on cooldown. **Tyrant is ready and Soul
  Shards are 2.** No Demonic Core. Implosion is up. **To Hell and Back is not talented** —
  on a build that takes it, Implosion is a single-target press and row 6 wears nothing.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `hold-readable` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `starved` {client: not-enough-power} · Demonbolt `hold-readable` · Shadow Bolt `press`
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — ready, and `blocked` lights on the exact readable predicate
     `resource < 5`. Rung 8 is `soul_shard=5`; pressing a one-minute cooldown at two shards
     spends the window on a half-built board → skip.
  3. **Implosion** — available, and the `aoe_only` pawn lights from `implosion_st_only`: the AoE
     toggle is off and To Hell and Back is not talented → skip. ⚠ **Not `blocked`** — nothing is
     held and nothing would be wasted; the imps are simply worth more attacking.
  4. **Hand of Gul'dan** — `starved`. It costs three shards and there are two, which Blizzard has
     already tinted the icon for → skip.
  5. **Demonbolt** — `blocked` from `db_awaits_core`: no Demonic Core, and Demonbolt appears in
     the APL only gated on one → skip.
  6. **Shadow Bolt** — **press.** Rung 15, the filler, reached entirely by subtraction.
- **Eye-direction.** ⚠ **This is the state the whole catalog is built around, and the badge on
  row 5 is the point of it.** Holding a *ready* one-minute cooldown is the strongest claim cap
  makes anywhere in this spec, and it is safe to make because Soul Shards are **never-secret** —
  the term is `{ "resource", "<", 5 }`, an exact Lua comparison, not a curve handed to the
  client. Havoc's equivalent decision rests on a sealed Fury readout and can only be *shown*;
  this one can be *reasoned about*.
- **Density.** Two `blocked` holds stand between the left edge and the press (rows 5 and 8),
  which is Part 0.5's budget exactly. `starved` and `aoe_only` are not budgeted — they restate a
  resource already on the player's own bar and a mode the player set themselves.
- **Cue set.** Five-shard hold (A) → **have**, readable. Single-target skip (G) → **have**.
  Starved (E) → **have**. Core hold (C) → **have**.

### DEM-5 · Tyrant ready at 5 shards — press it

- **State.** As DEM-4, but **Soul Shards are 5**. A Demonic Core is up.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `press` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `below` · Demonbolt `overcap` {sealed: count-bar} · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — `tyrant_awaits_shards` requires `resource < 5`, which is false
     here, so the badge is dark → **press.** Rung 8.
- **Eye-direction.** The badge going *out* is what says "now". Row 5 is the only row in this
  catalog whose hold releases on a resource the player is actively building, so the transition is
  the signal and cap needs no second mark for it.
- **Cue set.** Nothing fires on the press. Demonbolt still wears `overcap` at five shards
  (cue B), which is correct and which the walk never reaches.

### DEM-6 · 4 shards, Core up, Tyrant far — Hand of Gul'dan, and the Core waits

- **State.** Mid-fight, single target, DEM-4's build (no To Hell and Back). Every summon on
  cooldown, **Tyrant ~40 s out**, **4 Soul
  Shards**, a **Demonic Core up**.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `press` · Demonbolt `overcap` {sealed: count-bar} · Shadow Bolt `below`
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
  on a Demonbolt that has no Core to spend.

### DEM-7 · 3 shards, Tyrant 4 s out — bank for the window

- **State.** As DEM-6, but **Tyrant's cooldown has ~4 s left** and shards are **3**. A Demonic
  Core is up.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `hold-sealed` · Demonbolt `press` {sealed: count-bar} · Shadow Bolt `below`
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
- **Cue set.** Tyrant bank (F) → **sealed**. Overcap (B) → dark, at three shards.

### DEM-8 · 1 shard, Core up — the Core is the press

- **State.** Single target, everything on cooldown, **1 Soul Shard**, a **Demonic Core up**,
  Tyrant far away. **Doom is talented and the target's Doom is inside its pandemic window.**
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `starved` {client: not-enough-power} ·
  Demonbolt `press` {sealed: count-bar, pandemic} · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon … Summon Demonic Tyrant** — on cooldown → skip.
  2. **Implosion** — the `aoe_only` pawn → skip.
  3. **Hand of Gul'dan** — `starved` at one shard against a cost of three → skip.
  4. **Demonbolt** — **press.** Rung 14. All three of its markers are dark: a Core is up
     (cue C), shards are below four (cue B), and row 9 is not transformed (cue D).
- **Eye-direction.** The plainest state in the catalog, and it is worth having in the walk
  precisely because **three markers are simultaneously off**. A row whose badges only ever light
  is a row nobody can read.
  ⚠ **This is also the densest corner in the catalog, and it is here on purpose.** Demonbolt is
  wearing **two sealed displays at once** — V18's arc, which is how many Cores are banked, and
  V19's refresh badge, which is the client saying that refreshing Doom now clips nothing. Both
  land in the badge stack's own pixel. Whether that reads as one statement or as a mess is the
  question the flight is for; nothing else in this walk stacks two client-drawn things on one
  corner.
  ⚠ **The window badge is GATED ON THE TALENT, not on the aura.** Without Doom talented the fact
  does not exist, and a display armed for it would sit dark forever with no way to tell that from
  a client refusal. The gate is readable and contributes no cue — it decides only whether the
  client is allowed to paint the sealed display at all.
  ⚠ **cap authors NO threshold for the window.** The client computes
  `GetRefreshExtendedDuration − GetAuraBaseDuration` itself, per spell, which is Blizzard's real
  pandemic rather than the community's 30 %. Reproducing the same picture from a duration band
  would be cap's guess wearing the same pixels.
- **Cue set.** Starved (E) → **have**. Nothing else fires. Two sealed displays draw (V18, V19).

### DEM-9 · Ruination armed — row 7 is a different button

- **State.** Diabolic Ritual has cycled to **Pit Lord** and its Art is armed, so **row 7 is
  displaying Ruination**. Single target, **2 Soul Shards**, a Demonic Core up, Tyrant on
  cooldown.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` · Implosion `off-mode` {cues: aoe_only} ·
  Ruination `press` · Demonbolt `below` · Shadow Bolt `below`
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
  is displaying Infernal Bolt**. Single target, **2 Soul Shards**, a **Demonic Core up**, Tyrant
  ready.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `hold-readable` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `starved` {client: not-enough-power} ·
  Demonbolt `hold-readable` {sealed: count-bar} · Infernal Bolt `press`
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — `blocked` at two shards, cue A → skip.
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
- **Density.** Two budgeted holds (rows 5 and 8) before the press. At budget, not over.
- **Cue set.** Infernal-Bolt yield (D) → **have**. Five-shard hold (A) → **have**. Starved (E) →
  **have**.

### DEM-11 · Infernal Bolt armed at 4 shards — and it loses

- **State.** As DEM-10, but **4 Soul Shards** and Tyrant on cooldown. Row 9 is still displaying
  Infernal Bolt; a Demonic Core is up.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` · Implosion `off-mode` {cues: aoe_only} ·
  Hand of Gul'dan `press` · Demonbolt `overcap` {sealed: count-bar} · Infernal Bolt `below`
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
  talented.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `hold-readable` · Implosion `press` ·
  Hand of Gul'dan `below` · Demonbolt `below` · Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — `blocked` at three shards, cue A → skip.
  3. **Implosion** — the `aoe_only` pawn requires the toggle to be **off**, and it is on, so the
     badge is dark → **press.** Rung 9, which outranks both Ruination and the ordinary Hand of
     Gul'dan.
- **Eye-direction.** ⚠ **The 3-target threshold is the player's, not cap's.** Rung 9 reads
  `active_enemies>2`, and **cap models no enemy count** — the toggle is the whole interface, as
  it is on Havoc and Retribution. This scenario says what the badge does once the toggle is on,
  not when to flip it.
  ⚠ **Whether there are six imps is still a fact cap does not have — and it no longer has to.**
  The rung's other half, `buff.wild_imps.stack>=6`, is a sealed count, and cap hands the client a
  band table rather than reading it: at six or more the upper band emits nothing, so the row is
  clean and the press is right. **DEM-13 is the state below six**, which this walk could not
  contain until 2026-08-22.
- **Cue set.** Single-target skip (G) → correctly **dark**. Five-shard hold (A) → **have**. The
  imp band (V17) draws nothing, which is the state it is in when the row is a live candidate.

### DEM-13 · AoE mode on, three imps out — the count rules the row out

- **State.** As DEM-12 — AoE toggle on, four targets, **3 Soul Shards**, Tyrant ready, To Hell and
  Back not talented — except that a Hand of Gul'dan chain has **not** landed and only **three Wild
  Imps** are out.
- **CDM row.** Power Siphon `cd` · Grimoire: Imp Lord `cd` · Summon Doomguard `cd` ·
  Call Dreadstalkers `cd` · Summon Demonic Tyrant `hold-readable` ·
  Implosion `ruled-sealed` {sealed: count-bands} · Hand of Gul'dan `press` · Demonbolt `below` ·
  Shadow Bolt `below`
- **Walk.**
  1. **Power Siphon … Call Dreadstalkers** — on cooldown → skip.
  2. **Summon Demonic Tyrant** — `blocked` at three shards, cue A → skip.
  3. **Implosion** — the `aoe_only` pawn is dark, because the toggle is on. What rules the row out
     instead is the **client**: cap handed it a two-band table over the Wild Imp application
     count, and below six the lower band draws V11's stripe sheet, a plate and a red mark out of
     one FontString → skip. Rung 9's `buff.wild_imps.stack>=6` is false and the row says so.
  4. **Hand of Gul'dan** — affordable at three shards, Tyrant far → **press.** Rung 11, and it is
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
  input a rule applies to, so at exactly six imps every mark clears and the row becomes a
  candidate. An off-by-one here is invisible until it is wrong in a pull.
  ⚠ **At ZERO imps there is no aura and therefore no button, so no sink on it draws at all.** That
  state is covered by a readable marker instead (`implosion_no_imps`, on the `aura` latch), which
  is the one thing a sealed display structurally cannot reach.
- **Density.** One budgeted hold (row 5) plus one client-drawn elimination before the press.
- **Cue set.** Five-shard hold (A) → **have**. Single-target skip (G) → correctly **dark**. The
  imp band (V17) → **drawing**, and it is what makes this scenario expressible.

### DEM-14 · Two Cores banked — Power Siphon rules itself out

- **State.** Mid-fight, single target, DEM-4's build. **Power Siphon is ready** and **two Demonic
  Cores are banked**. 4 Soul Shards, Tyrant ~40 s out, Grimoire and Summon Doomguard on cooldown.
- **CDM row.** Power Siphon `ruled-sealed` {sealed: count-bands} · Grimoire: Imp Lord `cd` ·
  Summon Doomguard `cd` · Call Dreadstalkers `cd` · Summon Demonic Tyrant `cd` ·
  Implosion `off-mode` {cues: aoe_only} · Hand of Gul'dan `press` ·
  Demonbolt `overcap` {sealed: count-bar} · Shadow Bolt `below`
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
  **drawing**, on Power Siphon. The Core arc (V18) → **drawing**, on Demonbolt.

---

## The state this walk does not contain

⚠ **This is the finding, not an omission.** `capart check`'s elimination gate requires the
leftmost un-ruled-out entry to be the press. In the state below it is not, and **cap draws nothing
that would rule the wrong row out** — so writing it as a scenario would mean asserting a reading
the player cannot perform. It is argued in full at `catalog.md` → *Defeats*, item 1.

1. **Call Dreadstalkers, ready, with Tyrant between ~10.5 s and ~21.5 s out**, on a Reign of
   Tyranny build. The APL holds the dogs; the walk stops on them at position 4. The hold is a
   **two-sided** sealed band, which `Catalog.Check` refuses outright and which no union of
   one-sided markers can express — a union is an OR and this condition is an AND. Reopened by a
   `Channel.BandPoints`, which is a five-point curve list and nothing more.

**It is not a client limit.** The secret is a number, `../spec.md` §3.6 says a threshold on a
secret is expressible as a rule the client evaluates, and the curve has simply never been written.
That is a shelf gap with a named shape, which is a different and much better thing than "cap
cannot do this".

⚠ **There were TWO such states until 2026-08-22**, and the second — Power Siphon with Cores banked
— is now **DEM-14**. It was never a client limit either, and the thing that closed it was not new
platform knowledge but a treatment being **promoted out of the lab** into `../render-shelf.md`
Parts 1–6: a catalog may not cite a lab entry, so the fact was expressible and unusable at the
same time. The same primitive, inverted, closed the state below six imps as **DEM-13**.

**What the walk did not have to explain.** No state above required cap to know a target count, an
aura duration, a cooldown's remaining *value*, an aura stack count, or which Demonic Art was
armed. Every skip is a readable Lua term, one sealed band on one cooldown (DEM-7), or a band table
the client evaluated against a count cap never received (DEM-13, DEM-14).

**Fourteen states, no promotion.** Retribution spends its one positive cue on an opener whose
press sits seventh from the left; Demonology's rung-1 press sits **first**, and no state in this
walk stands more than two `blocked` holds between the left edge and the press. A vocabulary where
the positive cue is reached often has stopped being a reading model and become a pointer
(`../render-shelf.md` Part 0.5).

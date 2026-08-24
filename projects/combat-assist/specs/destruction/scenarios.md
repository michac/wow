---
title: Destruction Warlock — the scenario catalog
spec: Destruction Warlock (Diabolist) — specID 267, hero tree 59, Midnight 12.1
---

# Destruction Warlock (Diabolist) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the cues. This file is the **proof** that lane + cues actually reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. It is what `capart check`'s reading gate mechanises, and it is where this design gets falsified.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/warlock/destruction/simc-apl.md` (Tier 1,
generated, commit `8ec56ea`), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## The build this walk is authored on

⚠ **A walk is only as specific as its build, and this one has to say so**, because two cues are
talent-gated and one of them decides whether a row is readable at all.

**Diabolist**, with **Lake of Fire**, **Fiendish Cruelty**, **Backdraft**, **Soul Fire**,
**Inferno** and **Havoc** (rather than Mayhem) talented, and **Conflagration of Chaos NOT
talented**.

- Lake of Fire keeps cue **F** dark, so Cataclysm is drawn plainly at position 5 — which is where
  `actions.default` rung 12 puts it, between Immolate and the Chaos Bolt dump.
- **Conflagration of Chaos is the load-bearing one.** With it talented, cue **H** is gated off and
  Shadowburn is lit, un-badged and un-promoted in every state where no Fiendish Cruelty proc is
  up — which is a state this walk therefore **cannot contain**. That is `catalog.md` →
  *Defeats*, item 3, and it is the catalog's largest named exposure. On the build above, cue H
  lights and the walk reads.
- Mayhem instead of Havoc simply deletes row 10; the walk is nine entries wide and nothing else
  changes.

---

## The state walk

Twelve states, each naming the press, and for **every button that is available and skipped**, the
reason. Buttons the Cooldown Manager has already swiped need no explanation. The walk reads the
authored row order left to right and must satisfy the shape `capart check`'s **elimination gate**
enforces: *the leftmost entry that is neither swiped nor wearing a negative badge is the press* —
except where a **positive** cue is present, in which case pass 1 presses that instead.

Shorthand: "shards" = Soul Shards, "Art" = a Demonic Art armed by a completed Diabolic Ritual
stage. Rungs are positions in `actions.default` unless the scenario says `aoe_dia`.

### The **CDM row** bullet is machine-read

Every scenario below carries a `- **CDM row.**` bullet in a fixed grammar — ten entries in
authored order, separated by ` · `, each `<Ability> \`<verdict>\``.
`wowkb.capart import scenarios destruction` scrapes it into the preview's sidecar and
`wowkb.capart check destruction` re-scrapes it and fails if the two disagree, so **this document
leads and the preview follows**. The ability name is whatever the Cooldown Manager would
*display* in that state — `Ruination`, not `Chaos Bolt`, while row 6 is transformed, and
`Incinerate`, never `Shadow Bolt`, because that override is permanent and spec-wide.

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `hold-readable` = the red
`blocked` badge from a readable Lua term. `starved` = the red affordability badge. `overcap` =
the red waste badge. `off-mode` = the mode pawn. `press` = the button an unobstructed scan
reaches. `press-promoted` = the button a positive cue points at. `below` = shown, but the walk
never got there.

⚠ **`{client: unusable}` appears on Shadowburn in most states, and it is not a cap opinion.**
Shadowburn is *"only usable on enemies that have less than 20 % health"* *[T1 @ 12.1.0.69214]*,
so outside execute and without a Fiendish Cruelty proc the client itself paints it with
`ITEM_NOT_USABLE_COLOR` (`knowledge/addon-dev/cooldown-manager.md` §3.4). It is drawn so a reader
can see what the row actually looks like — and so the argument in
*The states this walk does not contain* can be checked by eye.

### DES-1 · Opener — Conflagrate at two charges

- **State.** The pull. Soul Fire was pre-cast and is on cooldown; **Conflagrate is at 2/2
  charges**; Summon Infernal, Cataclysm and Havoc are all up. Immolate is not yet on the target.
  Single-target mode.
- **CDM row.** Soul Fire `cd` · Conflagrate `press-promoted` {cues: capped} · Summon Infernal `below` ·
  Immolate `below` · Cataclysm `below` · Chaos Bolt `below` · Shadowburn `below` {client: unusable} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.** ⚠ **This scenario is read by pass 1, not by elimination.**
  1. **Conflagrate** wears the gold `capped` badge → **press.** Rung 2,
     `conflagrate,if=action.conflagrate.charges>=2`, which sits second in the whole priority and
     carries no other term.
  2. Everything else is read only if the eye goes looking.
- **Eye-direction.** ⚠ **This is the cleanest `capped` in any catalog, and the reason is a
  measurement.** R6 says `C_Spell.GetSpellCharges` is readable **only at full** — OBS-066 measured
  Conflagrate specifically, and below 2/2 the count seals and `isActive` cannot tell castable-1
  from dead-0. The one state cap can read exactly is the one state this rung asks about. The
  positive cue is not being stretched here; it is being spent on the case it was defined for.
- **Cue set.** Banked charge (B) → **have**, readable. Single-target skip (J) → **have**, on both
  AoE buttons.

### DES-2 · Summon Infernal — the burst window

- **State.** One global later. **Conflagrate is at 1/2 and Backdraft is up** from the cast. Soul
  Fire still on cooldown. Summon Infernal is ready, 4 shards.
- **CDM row.** Soul Fire `cd` · Conflagrate `hold-readable` · Summon Infernal `press` ·
  Immolate `below` · Cataclysm `below` · Chaos Bolt `below` · Shadowburn `below` {client: unusable} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire** — on cooldown → skip.
  2. **Conflagrate** — available at 1/2, but `blocked` lights from `conflag_backdraft`: Backdraft
     is up, so rungs 4 and 10's `buff.backdraft.stack<1` is false and a second Conflagrate would
     stack a buff you have not spent. The `capped` gate is off at 1/2, so the two cues do not
     collide → skip.
  3. **Summon Infernal** — ready, nothing rules it out → **press.** Rung 5.
- **Eye-direction.** ⚠ **The Backdraft rung asks `stack<1` — absent — and that is why this cue is
  readable at all.** The Destruction pilot sealed Backdraft as a *count* at two stacks
  (`../spec.md` §3.5), which is the right shape for `aoe_dia` rung 13 and the wrong question for
  the single-target list. A plain `aura` latch answers *absent*, and the sealed count is not
  needed anywhere in this catalog.
- **Cue set.** Backdraft hold (C) → **have**, readable.

### DES-3 · Immolate is not on the target

- **State.** Mid-fight. Soul Fire, Conflagrate (0 charges) and Summon Infernal are all on
  cooldown. **Immolate has fallen off the target.** 3 shards.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `press` ·
  Cataclysm `below` · Chaos Bolt `below` · Shadowburn `below` {client: unusable} · Incinerate `below` ·
  Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `immolate_up` requires the DoT to be **on** the target and it is not, so the
     badge is dark → **press.** Rung 9.
- **Eye-direction.** The badge going *out* is what says "now", the same shape as Demonology's
  five-shard Tyrant hold. Row 4 is the only row in this catalog whose hold releases on a fact the
  fight changes for you rather than one you spend.
- **Cue set.** DoT hold (E) → correctly **dark**.

### DES-4 · Immolate up, Cataclysm ready

- **State.** As DES-3, but **Immolate is ticking** and **Cataclysm is ready**. Lake of Fire is
  talented.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `press` · Chaos Bolt `below` · Shadowburn `below` {client: unusable} · Incinerate `below` ·
  Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `blocked` from `immolate_up`: the DoT is on the target → skip.
  3. **Cataclysm** — ready, and `cata_awaits_talent` is never authored on a Lake of Fire build →
     **press.** Rung 12.
- **Eye-direction.** ⚠ **Cue F is a marker that exists to *not* be there.** On a Lake of Fire
  build rung 12 is unconditional and position 5 is simply right; on a build without it, Cataclysm
  is not in the single-target priority at all and the row would otherwise stop the walk. A
  talent-gated marker is the cheapest way to say "this row belongs to a different build", and it
  is the same shape as Retribution's cue F.
- **Density.** One `blocked` hold before the press, well inside Part 0.5's budget of two.
- **Cue set.** DoT hold (E) → **have**. Talent gate (F) → correctly **not authored**.

### DES-5 · 4 shards, Immolate up — Chaos Bolt is the dump

- **State.** Mid-fight, single target. **4 shards**, Immolate ticking, **Conflagrate at 1/2 with
  Backdraft up**, Cataclysm on cooldown, no Art armed, no proc.
- **CDM row.** Soul Fire `cd` · Conflagrate `hold-readable` · Summon Infernal `cd` ·
  Immolate `hold-readable` · Cataclysm `cd` · Chaos Bolt `press` · Shadowburn `hold-readable` {client: unusable} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire** — on cooldown → skip.
  2. **Conflagrate** — `blocked`, Backdraft up → skip.
  3. **Summon Infernal** — on cooldown → skip.
  4. **Immolate** — `blocked`, the DoT is up → skip.
  5. **Cataclysm** — on cooldown → skip.
  6. **Chaos Bolt** — affordable at four shards against a cost of two, and nothing rules it out →
     **press.** Rung 13, the ordinary shard dump.
- **Eye-direction.** ⚠ **Rung 13's real condition is `variable.ritual_length>4`, and cap cannot
  see it.** That is a **sum of three sealed aura remaining times** and there is no aura-remaining
  band on the shelf (`catalog.md` → *Defeats*, item 2). What makes position 6 defensible anyway is
  that the ritual wheel is continuous — exactly one Diabolic Ritual stage is always up — so
  `ritual_length` is only in the dead zone between the cast time (~2.5 s) and 4 s for a sliver of
  each ~13 s stage. **A documented misordering with a bounded cost**, not an un-eliminable row.
- **Density.** Two `blocked` holds before the press (rows 2 and 4), which is Part 0.5's budget
  exactly.
- **Cue set.** Backdraft hold (C) → **have**. DoT hold (E) → **have**. Shadowburn hold (H) →
  **have**, and note it is to the *right* of the press so it costs the reader nothing here.

### DES-6 · 5 shards — two generators stand down at once

- **State.** As DES-5, but **5 shards** (capped) and **Backdraft is down**, with Conflagrate at
  1/2. **Soul Fire is ready.**
- **CDM row.** Soul Fire `overcap` · Conflagrate `overcap` · Summon Infernal `cd` ·
  Immolate `hold-readable` · Cataclysm `cd` · Chaos Bolt `press` · Shadowburn `hold-readable` {client: unusable} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire** — ready, and `overcap` lights on the exact readable predicate `resource >= 5`.
     Rung 1 is `soul_fire,if=soul_shard<=4`, and pressing a generator at cap throws its whole
     shard yield away → skip.
  2. **Conflagrate** — Backdraft is down, so cue C is dark, but `overcap` lights for the same
     reason: rungs 4 and 10 read `soul_shard<=4.2` / `<=4.4` → skip. ⚠ The `capped` gate is off
     at 1/2, which is what lets the red badge appear at all.
  3. **Summon Infernal** — on cooldown → skip.
  4. **Immolate** — `blocked`, the DoT is up → skip.
  5. **Cataclysm** — on cooldown → skip.
  6. **Chaos Bolt** — the spender, and the only row on the board that *reduces* the shard count →
     **press.**
- **Eye-direction.** ⚠ **This is the state five shards actually is, and it is why `capped` is not
  spent on it.** Two rows going red says *"stop building"* in the negative voice the vocabulary
  is built around; a gold badge on Chaos Bolt would say *"spend"*, which is a **rank** claim the
  left-to-right scan already carries. Retribution makes the same argument about five Holy Power
  and it holds here unchanged.
- **Density.** One budgeted hold (row 4). `overcap` is not budgeted — it restates a resource
  already on the player's own bar, on rows that were not worth pressing anyway.
- **Cue set.** Soul Fire overcap (A) → **have**. Conflagrate overcap (D) → **have**. DoT hold (E)
  → **have**.

### DES-7 · Ruination armed — row 6 is a different button

- **State.** Diabolic Ritual has cycled to **Pit Lord** and its Art is armed, so **row 6 is
  displaying Ruination**. Single target, **1 shard**, Immolate ticking, Conflagrate at 0 charges.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `cd` · Ruination `press` · Shadowburn `starved` {client: not-enough-power} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `blocked`, the DoT is up → skip.
  3. **Cataclysm** — on cooldown → skip.
  4. **Ruination** — **press.** Rung 11, above the ordinary Chaos Bolt dump and below everything
     else, which is where row 6 already sits — so the identity carries it with no cue.
- **Eye-direction.** ⚠ **`cb_starved` stays dark at one shard, and that is the whole reason it
  reads the live id.** `Sense.buildReads` asks affordability of `info.override or row.primary`,
  so on the transformed row this is **Ruination's** cost, which is none. Read on the base id it
  would light at one shard against Chaos Bolt's two, and the walk would step past a free press
  onto a Shadowburn it cannot afford. One marker covers both lives of the row correctly, and it
  is the same argument Retribution makes about Hammer of Light.
- **Cue set.** Identity (R7) → **have**. Starved (G) → **have**, on Shadowburn, and correctly
  **dark** on row 6.

### DES-8 · Fiendish Cruelty proc — Shadowburn jumps the queue

- **State.** Mid-fight, single target. A **Fiendish Cruelty proc is up**, so the next Shadowburn
  is free and usable on any target regardless of health. Immolate is ticking, Conflagrate is on
  cooldown, 3 shards, no Art armed.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `cd` · Chaos Bolt `below` · Shadowburn `press-promoted` {cues: priority} ·
  Incinerate `below` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.** ⚠ **This scenario is read by pass 1, not by elimination.**
  1. **Shadowburn** wears the gold `priority` badge → **press.** Rung 7, whose second conjunct
     `(buff.fiendish_cruelty.up|talent.conflagration_of_chaos)` is satisfied by the proc.
  2. Elimination alone would stop at **Chaos Bolt**, position 6 — rung 13 — which is a real
     press and the wrong one.
- **Eye-direction.** ⚠ **This is a `priority` spent on rank a fixed row order genuinely cannot
  carry, and it is the position that pays for it.** Shadowburn's rung is above Immolate (9) and
  both Chaos Bolt rungs (3 and 13), but *reaching* that rung needs either this proc or something
  cap cannot see, so in every other state position 7 is right. The alternative — hoisting
  Shadowburn to position 4 and badging Immolate, Cataclysm and Chaos Bolt down in the common case
  — would add three markers to remove one. Part 0.5's test for a promotion is that it should
  **remove** authored vocabulary; this one does.
  ⚠ **The proc is readable through one plain boolean.** `SpellActivationOverlay` row 4888 has
  Fiendish Cruelty `1245664` highlighting Shadowburn `17877` by class mask *[T1 DB2 @
  12.1.0.69214]*, so `IsSpellOverlayed(17877)` is the whole term. Blizzard is already glowing this
  button; cap's badge says the glow **outranks the rows to its left**, which is the part the glow
  does not say.
  ⚠ **Conflagrate must not be at 2/2 here**, and it is not. Two positive cues on one row is what
  pass 1 forbids; two on *different* rows is fine, but the leftmost wins — so a banked Conflagrate
  charge would correctly take precedence, and this scenario is authored after it was spent.
- **Cue set.** Shadowburn promotion (I) → **have**. DoT hold (E) → **have**, and it costs nothing
  under pass 1.

### DES-9 · Infernal Bolt armed at 1 shard — the filler row is a builder

- **State.** Diabolic Ritual has cycled to **Mother of Chaos** and its Art is armed, so **row 8 is
  displaying Infernal Bolt**. Single target, **1 shard**, Immolate ticking, Conflagrate at 0
  charges, no Fiendish Cruelty proc.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `cd` · Chaos Bolt `starved` {client: not-enough-power} · Shadowburn `hold-readable` {client: unusable} ·
  Infernal Bolt `press` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `blocked`, the DoT is up → skip.
  3. **Cataclysm** — on cooldown → skip.
  4. **Chaos Bolt** — `starved`: one shard against a cost of two, which Blizzard has already
     tinted the icon for → skip.
  5. **Shadowburn** — `blocked` from `sb_awaits_proc`: no Fiendish Cruelty proc and Conflagration
     of Chaos is not talented, so rung 7's second conjunct is false and the rung cannot fire →
     skip. ⚠ Note the client has **also** greyed it, for a different and stricter reason.
  6. **Infernal Bolt** — row 8 reads `identity == transformed`, so band 1 gives it **ROTATION**
     instead of FALLBACK → **press.** Rung 14, and it generates three shards, which is exactly
     what a one-shard board needs.
- **Eye-direction.** ⚠ **This transform costs no marker, and Demonology's costs one — the
  difference is position.** There, Infernal Bolt rides the *rightmost* row and outranks its
  left-hand neighbour, so Demonbolt has to be stood down by a cross-row `identity` marker. Here,
  rungs 14 and 15 are adjacent and the row is last, so the identity changes the row's **kind**
  and nothing about the order. The two Warlock catalogs share a transform and spend different
  vocabulary on it.
  ⚠ **The row's base name is one no Destruction warlock ever sees.** Its `cooldownID` binds
  Shadow Bolt `686`; Incinerate permanently overrides it (`SpecializationSpells` 7291,
  `OverridesSpellID = 686`, T1 DB2); Infernal Bolt overrides that. **Three deep**, and the
  catalog binds a stable id union rather than any live id.
- **Density.** Two budgeted holds (rows 4 and 7) before the press. At budget, not over.
- **Cue set.** Starved (G) → **have**. Shadowburn hold (H) → **have**. DoT hold (E) → **have**.

### DES-10 · Zero shards — everything demotes itself

- **State.** Single target, **0 shards**, Immolate ticking, every cooldown down, no Art armed, no
  proc. Row 8 is Incinerate.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `cd` · Chaos Bolt `starved` {client: not-enough-power} · Shadowburn `starved` {client: not-enough-power} ·
  Incinerate `press` · Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `blocked`, the DoT is up → skip.
  3. **Cataclysm** — on cooldown → skip.
  4. **Chaos Bolt / Shadowburn** — both `starved` at zero shards → skip.
  5. **Incinerate** — **press.** Rung 15, the filler, reached entirely by subtraction.
- **Eye-direction.** ⚠ **Shadowburn wears `starved` rather than `blocked` here, and that is not a
  cosmetic choice.** `sb_awaits_proc` would also be true — no proc, no Conflagration of Chaos —
  but a row already unaffordable is a row the player cannot press for a reason they can see on
  their own bar. Slot 2 carries it; naming the hold as well would put two red badges on one icon
  to say one thing. `Catalog.Check`'s one-cue-per-slot rule keeps them apart and the walk reads
  the outer one.
- **Density.** One budgeted hold (row 4). `starved` is not budgeted.
- **Cue set.** Starved (G) → **have**, twice. DoT hold (E) → **have**.

### DES-11 · Conflagrate as the builder — Backdraft down

- **State.** Single target, **2 shards**, Immolate ticking, **Conflagrate at 1/2 and Backdraft is
  down**. Soul Fire and Summon Infernal on cooldown.
- **CDM row.** Soul Fire `cd` · Conflagrate `press` · Summon Infernal `cd` · Immolate `below` ·
  Cataclysm `below` · Chaos Bolt `below` · Shadowburn `below` {client: unusable} · Incinerate `below` ·
  Rain of Fire `off-mode` {cues: aoe_only} · Havoc `off-mode` {cues: aoe_only}
- **Walk.**
  1. **Soul Fire** — on cooldown → skip.
  2. **Conflagrate** — all three of its cues are dark: charges are not full (B), Backdraft is
     absent (C), and two shards is under the cap (D) → **press.** Rung 4,
     `conflagrate,if=soul_shard<=4.2&buff.backdraft.stack<1`.
- **Eye-direction.** ⚠ **This is the row with the most vocabulary in the catalog and the point of
  the scenario is that all of it is off.** Three cues, three different facts — a charge count, an
  aura's presence, a resource level — and a row whose badges only ever light is a row nobody can
  read. The gating structure is what makes them a ladder rather than a pile: cues C and D are both
  gated on `!capped(conflagrate)`, so the gold badge and the red ones can never contradict each
  other on one icon.
- **Cue set.** Nothing fires.

### DES-12 · AoE mode on, 4 targets — Chaos Bolt, still

- **State.** The player has flipped cap's AoE toggle; **four targets**, an Art armed, **3
  shards**, Immolate on the current target, one Immolate out. Conflagrate on cooldown, Summon
  Infernal on cooldown.
- **CDM row.** Soul Fire `cd` · Conflagrate `cd` · Summon Infernal `cd` · Immolate `hold-readable` ·
  Cataclysm `cd` · Chaos Bolt `press` · Shadowburn `below` {client: unusable} · Incinerate `below` ·
  Rain of Fire `below` · Havoc `below`
- **Walk.**
  1. **Soul Fire … Summon Infernal** — on cooldown → skip.
  2. **Immolate** — `blocked`, the DoT is on the current target → skip.
  3. **Cataclysm** — on cooldown → skip.
  4. **Chaos Bolt** — **press.** `aoe_dia` rung 2,
     `chaos_bolt,if=talent.diabolic_ritual&(demonic_art|…)&(active_enemies<=(10-2*talent.destructive_rapidity))`
     — **Diabolist keeps pressing Chaos Bolt a long way into AoE**, which is the whole reason the
     two hero trees have different AoE lists.
  5. **Rain of Fire** — the `aoe_only` pawn is dark now the toggle is on, and it never gets the
     chance to compete because the press is three positions to its left.
- **Eye-direction.** ⚠ **The target-count threshold is the player's, not cap's.** `aoe_dia` is
  entered at `active_enemies>=2` and its Rain of Fire rung wants 3 with a pooling term, and **cap
  models no enemy count** — the toggle is the whole interface, as it is on Havoc and Retribution.
  This scenario says what the badges do once the toggle is on, not when to flip it.
  ⚠ **Rain of Fire at position 9 is a documented misordering**, and it is deliberate. `aoe_dia`
  ranks it 3; at *very* high target counts it genuinely outranks Chaos Bolt, and position 9 cannot
  say so. `rotation.md`'s Tier-3 colour is the reason the row order takes the Diabolist side —
  *"don't cast Rain of Fire until ~8+ targets"*, because Chaos Bolt feeds the ritual — and cap
  could not take the other side anyway without an enemy count.
  ⚠ **The `3.5` in that rung is not Rain of Fire's cost**, which is three whole shards on both
  ids. `3.5 - 0.1 × active_dot.immolate` is a hand-tuned pooling heuristic with no stated
  rationale (`rotation.md` carries the full note), and no marker in this catalog reads it.
- **Density.** One budgeted hold. **Cue set.** Single-target skip (J) → correctly **dark** on both
  AoE rows. DoT hold (E) → **have**.

---

## The states this walk does not contain

⚠ **These are the finding, not an omission.** `capart check`'s elimination gate requires the
leftmost un-ruled-out entry to be the press. In each state below it is not, and **cap draws
nothing that would rule the wrong row out** — so writing them as scenarios would mean asserting a
reading the player cannot perform. They are argued in full at `catalog.md` → *Defeats*.

1. **Shadowburn in execute range on a Conflagration of Chaos build.** The target is below 20 %
   health, no proc is up, and the talent satisfies rung 7's second conjunct by itself. Cue H is
   gated off by the talent and cue I needs the proc, so cap says nothing and the walk points at
   Chaos Bolt. The gate is `C_Spell.IsSpellUsable`'s **first** return on an access-gated spell,
   which is unmeasured — and it is the **same** open fact Devourer's Collapsing Star row waits on.
   ⚠ **The player is not stranded here; the reading model is.** In execute range Blizzard
   *un-greys* the icon, and that transition is the strongest signal on the row — which is why
   `{client: unusable}` is drawn on Shadowburn throughout this walk. Part 0.5 counts two
   eliminating signals, the swipe and cap's badge; the client's unusable tint is a third, and
   admitting it is a shelf decision this pass does not take.
2. **The DoT pandemic window.** Immolate has 4 s left on an 18 s DoT; rung 9 wants it refreshed and
   cue E is still holding row 4, so the walk points at Chaos Bolt and the refresh is late. **The
   fact is readable and never secret** — R8's `item.PandemicIcon ~= nil` mirrors
   `IsInPandemicTime` exactly `[client 2026-07-31]` — and what is missing is a `pandemic` entry in
   `Catalog.PREDICATES`. This is the cheapest reopening in any catalog and it is deliberately not
   prebuilt.
3. **The ritual dead zone.** `variable.ritual_length` between the Chaos Bolt cast time and 4 s:
   neither rung 3 nor rung 13 fires, and cap points at Chaos Bolt anyway. Bounded by the wheel's
   own cadence to a sliver of each ~13 s stage, and reopened by an aura-remaining band.
4. **Very high target counts**, where `aoe_dia` rung 3 puts Rain of Fire above Chaos Bolt.
   cap models no enemy count and the toggle is one bit, so there is no state for this to be
   expressed in. Not a defeat so much as a scope boundary.

**What the walk did not have to explain.** No state above required cap to know an enemy count, an
aura duration, a cooldown's remaining value, a target's health, or an aura's stack count. **Every
skip in every scenario is a readable Lua term** — this catalog authors no sealed cue at all, which
is a first.

**Twelve states, two promotions.** Both are spent on rank a fixed row order cannot carry — a
banked Conflagrate charge that is being lost right now (DES-1), and a proc that lifts Shadowburn
five rungs (DES-8) — and no row wears both, which is the invariant pass 1 rests on. Ten of the
twelve states are read by elimination.

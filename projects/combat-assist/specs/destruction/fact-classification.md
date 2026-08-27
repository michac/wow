---
title: Destruction Warlock — fact classification
spec: Destruction Warlock (Diabolist) — specID 267, hero tree 59, Midnight 12.1
---

# Destruction Warlock (Diabolist) — fact classification

**What this file is for.** The **safety case**: every fact this catalog consumes, sorted readable / sealed-display / open, with its recipe and its evidence. It is separate so it can be read without reading the roster — the question *"does anything here branch on a sealed value?"* must be answerable on its own.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/warlock/destruction/simc-apl.md` (Tier 1,
generated, commit `8ec56ea`), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## 1. The answer, first — and it is stronger than usual

**No sealed fact appears in any proposed Lua condition, in either polarity, and no sealed fact
reaches a sink either.** This is the **first catalog with an empty sealed lane**: no
`sealed-cooldown-range`, no `sealed-power-percent`, no `player-aura-stacks`. Every one of the ten
markers is a readable Lua condition over `ready`, `affordable`, `identity`, `capped`, `resource`,
`proc`, `aura`, `talent` or `aoe`.

That is not a virtue and it is not a policy — it is a **consequence of the rungs**, and the price
is paid in section 5. Three of Destruction's ordering reasons are sealed durations (a DoT's
remaining, a ritual buff's remaining) and one is a target-health gate, and none of them has an
authored form. So the catalog draws nothing for them rather than approximating them, and the
sealed lane is empty because the sealed facts got **no** treatment, not because there were none.

---

## 2. Facts, classified

Every fact the catalog consumes, tagged **readable** / **sealed-display** / **open**, with its
recipe and evidence (`../spec.md` §3.6 is the boundary; `../authoring.md`'s recipe index owns the
recipes).

| Fact | Lane | Recipe | Evidence | Consumed by |
| --- | --- | --- | --- | --- |
| **Soul Shard current value** | **readable** | R3 | one of the seven never-secret secondaries; `power = "SoulShards"` has shipped since the Demonology pilot. T1 blue *Midnight Public Alpha Addon API Changes, 2025-11-24*; `security-taint-and-restricted-data.md` §4.12 | cues **A**, **D** |
| Readiness of a cooldown row | **readable** | R2 | CDM `Available` / `OnCooldown` alert-edge latch; `security-…` §4.8 | every lit row, and cues A / F / J's gates |
| Affordability of a spender | **readable** | R1 | `C_Spell.IsSpellUsable` **second** return, no `SecretWhen*` predicate | cue **G** on Chaos Bolt / Ruination and on Shadowburn |
| **Conflagrate at maximum charges** | **readable** | R6 | `C_Spell.GetSpellCharges` — `maxCharges` and `isActive` are `NeverSecret`; `currentCharges` seals **below full**. OBS-066 measured **this exact spell**: at 2/2 all readable, at 1/2 and 0/2 the count is secret and `isActive` is `true` in both (`observations.md:1177`) | cue **B**, and the gates on cues **C** and **D** |
| Spell identity across an override | **readable** | R7 | `overrideSpellID` readable in combat on 21/21 rows (`cooldown-manager.md`); all three override paths here are established from spell data — §3 | rows 6 and 8's bands, and cue G's live-id read |
| **Fiendish Cruelty proc** | **readable** | overlay `proc` | `SpellActivationOverlay` @ 12.1.0.69214 row **4888**: trigger **Fiendish Cruelty `1245664`**, `IconHighlightSpellClassMask_0 = 128`, which matches **Shadowburn `17877`**'s `SpellClassOptions` mask `[128, 131072, 0, 4194304]` *[T1 DB2]*. So `IsSpellOverlayed(17877)` is true exactly while the free Shadowburn is owed | cues **H**, **I** |
| **Backdraft present on the player** | **readable** | the `aura` latch | Backdraft `117828` is a Category-2 (TrackedBuff) row in set 884, OrderIndex 32 *[T1 DB2]*; the latch rides its `OnAuraApplied` / `OnAuraRemoved` alert edges (`Track.lua`; `cdm-rider-patterns.md` §6.2). ⚠ **The rung asks `stack<1`** — absent — which is exactly what a boolean answers | cue **C** |
| **Immolate present on the target** | **readable** | the `aura` latch, `unit = "target"` | Immolate's DoT `157736` is a Category-2 row in set 884, OrderIndex 49 *[T1 DB2]*. Same recipe as Retribution's cue G, which was flown in combat on a hostile target `[client 2026-08-19]` (`cdm-rider-patterns.md` §6.2) | cue **E** |
| AoE / single-target intent | **readable, not a game read** | cap's own `/cap aoe` toggle | n/a — cap owns the value | cue **J** |
| Whether Lake of Fire is taken | **readable** | the `talent` predicate | node 102427 / entry 126493 (`ability-inventory.tsv` @ 12.1.0.69214); ⚠ the `C_Traits` call shape is `[gap]` — Havoc's *Open facts* 7 | cue **F** |
| Whether Conflagration of Chaos is taken | **readable** | the `talent` predicate | node 71965 / entry 91478 | cue **H** |
| A related ability's **cooldown remaining** | **sealed-display** | S4 | `C_Spell.GetSpellCooldown` is `SecretWhenCooldownsRestricted` | **nothing.** No rung in `actions.default` reads another ability's `cooldown.X.remains`. Havoc's most-used sealed form has **zero consumers here**, exactly as on Devourer |
| **Backdraft application count** | **sealed-display** | S2 → `player-aura-stacks` | OBS-065 (`observations.md:1161`) measured this aura: 1 stack = icon and swipe only, 2 = the number "2". ⚠ `Catalog.Check` limits `min = 2`, which is the threshold `aoe_dia` rung 13 wants | **nothing in this catalog.** The single-target rungs ask `stack<1`, which the boolean answers. Kept here because a Hellcaller or AoE-deep catalog will want it |
| `dot.immolate.remains` — the **pandemic window** | **readable as a BOOLEAN, sealed as a number** | R8 | `item.PandemicIcon ~= nil` on a tab-1 row mirrors `IsInPandemicTime` exactly, recomputed every frame, **never secret** (`cooldown-manager.md:1303-1309`, `[client 2026-07-31]`). The *numbers* — `pandemicStartTime` / `pandemicEndTime` — are secret and `IsInPandemicTime(timeNow)` **throws** | **nothing yet.** R8 records *"no cap consumer yet"* and this is that consumer; the predicate does not exist. §5.1 |
| `variable.ritual_length` | **sealed, no authored form** | — | a sum of three Diabolic Ritual auras' remaining times. S5 can *display* an aura duration (it renders in combat) but there is no aura-remaining **band** — no display kind turns one into a badge | rungs 3 and 13. **No hint.** §5.2 |
| `demonic_art` — an Art is armed | **partly readable** | R7 | Art: Pit Lord ⇒ row 6 reads `transformed` (Ruination); Art: Mother of Chaos ⇒ row 8 reads `transformed` (Infernal Bolt); **Art: Overlord changes no button.** Diabolic Ritual `428514` holds two Category-2 rows in set 884 (OrderIndex 28, 29) and which is the armed Art is unmeasured | rung 3's first disjunct — **two thirds visible, and not authored as a marker.** §5.3 |
| `target.health.pct<=20` — execute range | **open** | R1's **first** return, unmeasured | Shadowburn's own Tier-1 description is *"Only usable on enemies that have less than 20% health"* @ 12.1.0.69214, so the gate **is** `isUsable`. R1 warns against the first return **because it is true for a spell on cooldown** — a warning about cooldowns, not about access gates. `[searched 2026-08-19: SpellActivationOverlay @ 12.1.0.69214 (no execute overlay), CooldownSetSpell @ 12.1.0.69214 (no execute-form row for 17877), the ability-inventory tooltip, and R1's measured set — four Fury-gated Havoc spells, none access-gated]` | rung 7's first disjunct. **No hint.** §5.4 |
| `target_if` — which enemy | **not expressible** — and not for a data reason | — | eight of `aoe_dia`'s fourteen rungs carry one. The **facts** are largely routable; what has nowhere to go is the **instruction**: a CDM row is a button, not a target | §5.5 |
| `active_enemies` | **not modelled** | — | replaced by the `/cap aoe` toggle, as on Havoc and Retribution | the `aoe_dia` entry gate, and rung 3's `>=3` |
| `raid_event.adds`, `fight_remains`, `target.time_to_die` | **not facts** | — | simulation state. cap does not model the encounter | six rungs. Deliberately unmodelled |

---

## 3. The three transforms, in full

`../authoring.md`'s recipe index R7 names "Shadow Bolt↔Infernal Bolt" as the canonical case; this spec has
that one plus two more, and **one of them is the best-established override in any catalog.**

| Transform | Established by | Confidence |
| --- | --- | --- |
| Shadow Bolt `686` → **Incinerate `29722`** (permanent, spec-wide) | `SpecializationSpells` @ 12.1.0.69214, row **7291**: `SpecID 267, SpellID 29722, OverridesSpellID 686` *[T1 DB2]*. This is a table whose entire purpose is to declare spec overrides, read directly | **Tier 1, direct** |
| Incinerate `29722` → **Infernal Bolt `433891`** | the aura's own Tier-1 description, spec-conditional: *"Mother of Chaos empowers your next `$?s137044[Shadow Bolt][Incinerate]` to become Infernal Bolt."* `137044` is the **Demonology Warlock** spec aura, so the string resolves to **Incinerate** here | **Tier 1** |
| Chaos Bolt `116858` → **Ruination `433885`** | its talent's Tier-1 description: *"Summoning a Pit Lord causes your next Chaos Bolt to become Ruination."* ⚠ Note this is the **same unbranched string** that names a spell Demonology does not have — here it is right, and there it had to be replaced by log evidence | **Tier 1** |

Neither `433885` nor `433891` holds a Category-0 (Essential) row in any `CooldownSet` at
12.1.0.69214 — both are Category-2 rows in set 884 (OrderIndex 62 and 61) *[T1 DB2]*.
`29722` holds **no `CooldownSetSpell` row at all, in any set**, verified directly. So an override
on a row that *does* have one is the only way any of the three reaches the Cooldown Manager.

⚠ **The filler row is three deep**, which is the deepest chain outside Devourer's Voidblade.
`Bind.lua`'s rule applies unchanged: bind a **static** identity with a stable `spellIDs` union
(`{686, 29722, 433891}`) and never carry state across a flip. `identity == transformed` is
`overrideSpellID ~= spellID`, and because Incinerate's override is *permanent*, the base row reads
`transformed` at all times against `686`. **The catalog's `identity` term therefore compares
against Incinerate, not against Shadow Bolt** — the entry's `primary` is `override or base`
resolved at bind (R7), which is Incinerate out of combat and every time nothing further overrides
it. @verify-ingame — this is a real subtlety and it is the one place the three-deep chain could
bite.

### The proc measurement

cap's `proc` predicate is `C_SpellActivationOverlay.IsSpellOverlayed(spellID)` (`Sense.lua`'s
`readProc`), a plain boolean keyed on the **highlighted spell**, wholly independent of the aura
API and measured readable in combat (`knowledge/addon-dev/cooldown-manager.md`). Which spells glow
is `SpellActivationOverlay.db2`: each row names a trigger aura and an
`IconHighlightSpellClassMask` matched against the highlighted spell's `SpellClassOptions` mask.

At **12.1.0.69214**, for Destruction *[T1 DB2]*:

| Trigger aura | Highlight mask | Matches | So `proc(x)` is true when |
| --- | --- | --- | --- |
| **Fiendish Cruelty** `1245664` | mask₀ `128` | Shadowburn `17877` (mask₀ `128`) | `proc(shadowburn)` — **used, cues H and I** |
| **Infernal Bolt** `433891` | mask₀ `1`, mask₁ `64` | Shadow Bolt `686`, **Incinerate `29722`** (mask₁ bit 6) | `proc(incinerate)` — **not used; see below** |
| **Ruination** `433885` | all four masks **zero** | nothing | never |
| Backlash `387385` | mask₁ `64` | Incinerate `29722` | — not authored; Backlash is a throughput passive with no rung |
| Soul Fire aura `335004` | mask₁ `64` | Incinerate `29722` | — legacy; no 12.1 rung |
| Chaotic Inferno `279673` | mask₁ `64` | Incinerate `29722` | — ⚠ **legacy ID.** The live 12.1 aura is `1244860` (a Category-2 row in set 884, OrderIndex 50) and it has **no overlay row**. The rung that read it was deleted from the module at `8ec56ea` anyway |
| Ritual of Ruin `364349` / `387157` | mask₃ `268435456` | Rain of Fire `5740` / `1214467` | — absent from the 12.1 Destruction inventory |
| Alythess's Ire `1244947` | mask₃ `268435456` | Rain of Fire | — the only rung reading it is `aoe_dia` 3's pooling heuristic, which is not authored |

Three consequences the design leans on:

1. **Fiendish Cruelty reads through one plain boolean**, which is what makes cues H and I cost no
   new mechanism — and cue H's *talent* half means the marker is true by construction whenever it
   lights.
2. **`proc(incinerate)` is a genuine second route to the Infernal Bolt state** and the catalog
   deliberately does not take it, for the same reason Demonology declines `proc(shadow_bolt)`:
   row 8's `identity` says the same thing about the row rather than about an aura, so the
   two-band design rests on one fact rather than two that could disagree.
   ⚠ Note the mask collision: **four different auras all highlight Incinerate**. A `proc` term on
   that row would be true under Backlash and the legacy Chaotic Inferno as well, which is a
   second reason to use `identity`.
3. **Ruination's overlay is useless**, as Hammer of Light's is for Retribution and as it is on
   Demonology: the row exists with an all-zero highlight mask, so it can highlight nothing. Row
   6's `identity` says everything the overlay would.

⚠ **Malevolence `442726`, Infernal Bolt `433891` and Ruination `433885` all carry all-zero
`SpellClassOptions` masks**, so no overlay can ever match them by mask. Any future proc rule about
those spells has to come from a trigger/aura route, not from `proc`.

---

## 4. Why there is nothing in the sealed lane

Worth stating explicitly, because an empty section reads like an omission.

- **`sealed-cooldown-range` has no subject.** Not one rung in `actions.default` or `actions.aoe_dia`
  reads `cooldown.X.remains` for a *different* ability. Havoc holds Metamorphosis for Eye Beam and
  Retribution holds Execution Sentence for Avenging Wrath; Destruction's cooldowns are pressed on
  cooldown and the alignment is done by the player's potion habits, which cap does not model.
- **`sealed-power-percent` has no subject.** Soul Shards are readable, so there is no graded
  resource curve to author. This is the same reason Retribution declares none.
- **`player-aura-stacks` has no subject *in single target*.** Backdraft's rungs in
  `actions.default` ask `stack<1`, which is a boolean. It reappears in `aoe_dia` rung 13
  (`buff.backdraft.stack<2`), which this catalog does not author because the AoE walk is one
  state and Conflagrate is not the press in it. **A Hellcaller catalog, or a deeper AoE pass, will
  want it**, and OBS-065 already verified it on this exact aura.

So: cap **offers** nothing to a client sink for this spec, **arms** nothing, and has nothing to
report as `refused`. The whole *"accepted is not drawn"* caution (`../authoring.md` → *Accepted is not drawn*)
has no application here, and every claim this catalog makes is one cap can check in a capture.

---

## 5. The open facts, routed

Each becomes an `@verify-ingame` marker on the claim, or a ClientLab `@pending-test` once a test
exists (`../authoring.md` stage 5; `projects/addon-lab/docs/lab-process.md`). **An unknown is a
marker on the claim, never a line in a tool and never a TODO here.**

### 5.1 The pandemic window — one predicate, and it is measured

Rung 9's real content. Full argument at `catalog.md` → *Defeats*, item 1. The safety point is that
this fact is **readable and never secret** — R8 measured it — so it is not an open fact in the
usual sense at all. It is an **unbuilt predicate**: `Catalog.PREDICATES` has no `pandemic` and
`Sense.lua` has no `readPandemic`. Cue E ships as `aura(immolate)` alone, holding the row for the
whole DoT, and the refresh is late by up to the pandemic window every cycle.

⚠ **A load-bearing open fact is a stop-and-ask** (`../spec.md` §3.6). This one is load-bearing on
*quality* rather than on correctness — the hold is never wrong, only conservative — so the row
ships and the predicate is named rather than built (`../authoring.md`'s standing rule against
prebuilding vocabulary). **It is the highest-value unbuilt thing for this spec and it is a
boolean.**

### 5.2 The ritual clock

Rungs 3 and 13. `catalog.md` → *Defeats*, item 2. Nothing sealed is compared, because nothing is
authored. The reopening — an S-form running S4's step curve on a duration object from
`C_UnitAuras.GetAuraDuration` rather than from `GetSpellCooldownDuration` — rests on an
assumption (that exactly one Diabolic Ritual stage is live at a time, so a band on the live stage
equals a band on the sum) that is Tier-2 and would need checking. @verify-ingame

### 5.3 Which of the two Diabolic Ritual rows is the armed Art

`428514` holds two Category-2 rows in set 884 (OrderIndex 28 and 29, cooldownIDs 18822 and
18823), and the same pair exists in Demonology's set 60. If one is the armed **Demonic Art**,
`aura(demonic_art)` is a readable boolean, rung 3's first disjunct closes, and Art: Overlord — the
one Art that changes no button — becomes visible. **One measurement serves both Warlock
catalogs.** @verify-ingame

### 5.4 Shadowburn's execute gate — and it is Devourer's open fact

Rung 7. `catalog.md` → *Defeats*, item 3. The safety point is that cap draws **nothing** here
rather than approximating: cue H carries the APL's second conjunct exactly and is gated off by
`talent(conflagration_of_chaos)`, so it never claims a hold the APL would not make. The exposure
is a **missing** hint on a Conflagration of Chaos build, not a wrong one.

⚠ **This is a stop-and-ask, and it is being asked rather than answered.** Reading the gate means
`C_Spell.IsSpellUsable`'s **first** return on an access-gated spell. Adding a predicate for it is
an engine change nobody asked for, and it is not made here. @verify-ingame / @pending-test

⚠ **This used to be framed as a measurement shared with Devourer, and it is not one any more.**
Devourer named the same read as *its* most load-bearing open fact, for Collapsing Star. That
consumer is gone: Collapsing Star was measured in game on 2026-08-27 to be a spell **override**
on the Void Metamorphosis row rather than an access-granted row of its own, so R7 draws it and
nothing there waits on `IsSpellUsable`. Shadowburn's own consumer is untouched — the execute gate
is still an unmeasured first return — but it is Destruction's alone to carry, and a measurement
here buys one spec rather than two.

⚠ **And note that the client is not silent.** Out of execute without the proc, Shadowburn is not
castable and the Cooldown Manager paints it with `ITEM_NOT_USABLE_COLOR`
(`knowledge/addon-dev/cooldown-manager.md` §3.4). The **player** is not stranded; the **reading
model** is, because the tint eliminates a row and `../render-shelf.md` Part 0.5's three signals
do not include it — it is neither the swipe, nor cap's badge, nor a band cap authored. Admitting
it is a Part 0.5 decision and belongs to whoever owns the shelf; it now has **two** consumers,
this row and Devourer's in-form position 1 (`../backlog.md` → *Now*).

### 5.5 Target selection

Eight `aoe_dia` rungs. `catalog.md` → *Defeats*, item 4. The **facts** are largely routable —
`dot.immolate.remains` per target is sealed but `debuff.havoc.remains` is cap's own Havoc row and
`time_to_die` is simulation state — and what has no surface is the **instruction**. Nothing is
waiting on a measurement.

### 5.6 The three-deep identity chain

§3's note. One in-game observation: on a Destruction warlock out of combat, does the Essential row
whose `cooldownID` is 66181 report `spellID = 686` with `overrideSpellID = 29722`, and does
`overrideSpellID` become `433891` while Mother of Chaos's Art is armed? The catalog's row 8 bands
and cue G's live-id read both depend on it. Failure direction if the chain resolves differently:
row 8 draws under the wrong band and the filler is lit as ROTATION at all times — visible
immediately, and harmless. @verify-ingame

### 5.7 `C_Traits.GetNodeInfo`

`[gap]` — inherited unchanged from Havoc's *Open facts* 7. The `talent` predicate is shipping and
`knowledge/addon-dev/` records nothing about the call's shape or its combat behaviour. **This
catalog is the most exposed of any to it**, because a refused `talent` read affects two cues in
opposite directions: cue F would badge Cataclysm on a Lake of Fire build (a *wrong* hold), and
cue H would badge Shadowburn on a Conflagration of Chaos build (also a wrong hold). ⚠ Both markers
must therefore withhold on UNKNOWN rather than treat a refused read as "not talented". §6.
@verify-ingame

### 5.8 Backdraft's row, and Immolate's

Both cues **C** and **E** rest on the `aura` latch, which needs the Cooldown-Manager row **bound**
— the player must have enabled that tracked row. An unbound row has no `cooldownID`, nothing is
ever written, and `World` reports UNKNOWN, so the marker goes dark. **The enablement detector is a
correctness requirement**, exactly as it is for Retribution's cue G, and it matters more here:
Retribution's latch gates an opener, and cue E fires every twenty seconds for the whole fight.
@verify-ingame

---

## 6. Unknown never becomes confidence

Every predicate above returns **UNKNOWN** rather than `false` when the client refuses it, and
every marker withholds on UNKNOWN. Four places in this catalog where that is doing real work:

1. **Cue H is a double negation** — `!proc(shadowburn)` **and** `!talent(conflagration_of_chaos)`.
   Either refused read must leave the badge dark. A refused `talent` that read as "not talented"
   would badge Shadowburn on exactly the build where the APL presses it.
2. **Cue F is a negation of a talent** — the same failure in the other direction. Cataclysm would
   wear a permanent hold on a Lake of Fire build.
3. **Cues C and E rest on a latch with no third supplier and no timeout** (`Track.lua`). §5.8.
4. **Cue B rests on `capped`, whose underlying read seals below full** (R6). A refused `capped`
   must read as "not at maximum" — which is both the safe direction *and*, per OBS-066, the
   truth: the count is only readable when it is at maximum, so a refusal **is** the answer.
   ⚠ That is a happy accident of this one predicate and it does not generalise. It is written
   down because `capped` is the only readable term in any catalog whose refusal carries
   information, and someone will eventually be tempted to reason that way about a different one.

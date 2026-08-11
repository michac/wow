# Demonology Warlock — catalog

**What this file is for:** the tier rules, cues, cooldown roster and sequences cap uses
on Demonology. It is the normative form of the catalog defined in `../spec.md` §3.5 —
the addon's Lua table is a transcription of this document, and if the two disagree the
table is wrong.

Present tense, like `spec.md`. Rationale for a rule goes in the ⚠ note beside it, not
in a history section; how the catalog got here is `../notes.md`.

**Applies to:** Warlock / Demonology (specID 266), hero tree **Diabolist**, Midnight
12.0.7. Soul Harvester is not authored — a Soul Harvester build binds nothing (`spec.md` §3.5,
no catalog, nothing at all).

---

## 1. The roster

Bound by observation, never by a hardcoded id where an id can move: a transforming
row is resolved through its **base** spell, and cap follows the override rather than
matching a literal override id.

| Ability | ID | CD | Cost | Entry |
| --- | --- | ---: | --- | --- |
| Summon Demonic Tyrant | `265187` | 60s | none | E1 |
| Call Dreadstalkers | `104316` | 20s | 2 shards (free w/ Demonic Calling) | E2 |
| Grimoire: Fel Ravager / Imp Lord | `1276467` / `1276452` | 120s | shards | E3 |
| Summon Doomguard | `1276672` | 120s | shards | E4 |
| Hand of Gul'dan | `105174` | — | 3 shards | E5 |
| — transforms to **Ruination** | (observed) | — | free | E6 |
| Demonbolt | `264178` | — | a Demonic Core | E7 |
| Implosion | `196277` | 15s | consumes Wild Imps | E8 |
| Power Siphon | `264130` | 30s | consumes ≤2 Wild Imps | E9 |
| Shadow Bolt | `686` | — | free, generates | E10 |
| — transforms to **Infernal Bolt** | (observed) | — | — | E10 |

**Which of these earn a cooldown bar is §4, and §4 is the only place it is declared.** The
roster is one ordered list because a panel stacks, so neither a column here nor a per-entry
field can carry it — and two declarations of one fact drift.

⚠ **Implosion and Power Siphon are two halves of one choice node** (spec tree row 5).
Exactly one of them exists on any build; the other's entry is dropped at bind time.
Grimoire is the same shape at row 10 — one entry (E3) covering both halves, which is what
its `alt` id is for: the row is matched on the base spell first and on `alt` after, so a
Fel Ravager build binds E3 rather than dropping it.

**Sources read but never graded, and given no entry:**

| Row | ID | Read by |
| --- | --- | --- |
| Wild Imp | `296553` | Implosion's positive cue (E8), as a `stacks` channel |
| Demonic Core | `264173` | Demonbolt's proc gate (E7), and E7's positive cue |
| Dominion of Argus | `1276166` (buff) | Hand of Gul'dan's apex band (E5), via `auraUp` |

⚠ **Call Dreadstalkers occupies two rows and only one of them is read.** The Essential row
is the press E2 grades and E1 names; the BuffBar row (cid `760`) is the pets' bar, and **cap's
aura gate gets no answer out of it** — `auraUp` is driven by the alert channel plus
`auraDataUnit`, and both are empty on that row on this build (see E1). The row is bound all
the same, and cap has never tried its widgets. Binding is keyed by `{spellID, family}`,
because a roster that binds one row per spellID picks whichever it walks first and would give
E2 the wrong one.

`shards` below is this spec's instance of `spec.md` §3.5's `resource` gate — Soul
Shards are a secondary resource, so cap may both read and branch on the count.

Costs and cooldowns above are Tier-1 (`wowkb.spec_inventory`, DB2 @ 12.0.7 —
`knowledge/classes/warlock/demonology/`). ⚠ **Summon Demonic Tyrant costs nothing**;
older project docs that say 1 shard are stale. ⚠ **The CD column is reference, not a
declaration cap counts down from.** No rule here rests on it: every remaining time is a
`cooldownRemaining` channel the client evaluates exactly.

---

## 2. Entries

Bands are first-match **within one entry**. Entries never see each other's *verdicts* —
a band names abilities, never tiers (`spec.md` §3.5).

### E1 — Summon Demonic Tyrant `265187`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `not ready(E2)` |
| 2 | **MEDIUM** | `ready(this)` |

- **grade:** `cooldownRemaining(this)` — the icon warms as the window approaches.
  This is the contextualising half of the spec's centrepiece: you should be able to
  see a burst window coming without reading a number.
- **cue:** **negative** · gate `ready(this)` and `not ready(E2)` → channel
  `cooldownRemaining(E2) ≤ 8` → **hold**.

⚠ Band 1 is "the board is staged", read through the one piece of the board cap can
account for: **the Dreadstalkers are on cooldown, so you cast them.** Wild Imps and the
Grimoire demon are not observable at all, so band 1 is *necessary but not sufficient* for
a good Tyrant — and that is fine. It grades the press's value; it does not grant
permission to press.

⚠ **There is no aura to read, and that is settled rather than unmeasured.** A summon
creates units in the world; it applies no aura, so no CDM row carries a bound one for
it and `auraUp` cannot express "the dogs are out" on any spec. (Measured alongside: 13
in-combat samples on the Dreadstalkers BuffBar row, never bound, while five genuine
aura rows on the same viewers bound normally.)

⚠ **The band reads long and the cue trims the tail, and that division is the point.**
Dreadstalkers' cooldown is 20 s against a ~12 s pet lifetime, so `not ready(E2)` stays
true for about eight seconds after the pets have gone. The cue is exactly that tail:
`cooldownRemaining(E2) ≤ 8` ⟺ the pets have expired. The band says the board is staged; the cue
says it has gone stale, and **both halves are exact** — the client owns the countdown and
cap never estimates one.

### E2 — Call Dreadstalkers `104316`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `affordable(this)` |

- **grade:** `cooldownRemaining(this)`.
- **cue:** **negative** · gate `ready(this)` and `affordable(this)` and `not ready(E1)`
  → channel `cooldownRemaining(E1) ≤ 20` → **hold**.

⚠ **A ready Dreadstalkers is HIGH, full stop, and the hold is a cue.** Dreadstalkers last
~12 s and Tyrant extends what is already out, so firing them shortly before the window
wastes the pair — but that is a reason to *wait*, not a lower tier (`spec.md` §3.4). One
band and one negative cue say it more honestly than three bands did, and the threshold is
evaluated inside the client rather than counted down by cap.

⚠ **`not ready(E1)` in the precondition is load-bearing.** A ready Tyrant has a
zero-remaining cooldown, which clears any `≤ t` and would pin the hold marker on
permanently — during the setup, which is precisely when Dreadstalkers should be pressed.

⚠ **`t = 20` is imprecise, and it is imprecise in a known direction — see O8.** The
rotation's real hold zone is `12 < cooldownRemaining(E1) < 20`: below 12 s the dogs pressed now are
still out when Tyrant lands and get extended, so pressing is right and the marker is
wrong there. The channel vocabulary offers a single upper threshold and cannot express a
band, so the marker over-fires in the last twelve seconds.

### E3 — Grimoire: Fel Ravager `1276467` / Imp Lord `1276452`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `ready(E1)` |
| 2 | **MEDIUM** | `ready(this)` |

⚠ A 2-minute cooldown is absent from roughly half of all Tyrant windows, so it is
staged into the window when it is up and **never gates it**. Band 2 exists because a
Grimoire pressed outside a window is still a summon, not a waste.

⚠ `ready(E1)` is exact, off the `Available` alert edge — cap does not anticipate a window
and never asks how far out one is. Being ready is the whole condition.

### E4 — Summon Doomguard `1276672`

Same shape as E3, and it declares **no talent term** — it is dropped at bind whenever no
CDM row tracks it, which is what an untalented Doomguard looks like from cap's side.
O3 settled that this build is exactly that case.

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `ready(E1)` |
| 2 | **MEDIUM** | `ready(this)` |

### E5 — Hand of Gul'dan `105174`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `auraUp(Dominion of Argus)` and `affordable(this)` |
| 2 | **HIGH** | `shards ≥ 5` and `affordable(this)` |
| 3 | **MEDIUM** | `affordable(this)` |

- **grade:** `shards` — within band 3, four shards reads brighter than three. Shards
  are readable, so cap computes this itself rather than handing it to a curve.

⚠ Two separate reasons to press it, and they are genuinely different situations: the apex
proc makes it free, and 5 shards makes it spend-or-waste. Band 3 is the ordinary case and
is true for most of a pull — which is correct. Hand of Gul'dan being usually-worth-pressing
is what a Demonology field should look like.

⚠ **"Spend the Tyrant window on Hand of Gul'dan" is currently unexpressible, and that is
recorded rather than approximated — see O1.** It would need "a Tyrant is active", which
nothing in the tracked set carries: no row holds the Tyrant buff, so there is no
`auraUp` and no `auraRemaining` channel to reach for. The route back is enabling the
hidden Tyrant bar (cid `84224`), not a re-derived fixed duration.

⚠ There is no band for "hold shards because Tyrant is near". The rotation's pooling
is **emergent** — E1's and E2's own rules plus the builder floor produce it — and
encoding it here would be an ordering, not a value.

### E6 — Ruination, the Hand of Gul'dan transform

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `identity(this) ≠ base` |

Free, large, and it replaces the button you were already going to press. There is no
band below it: when it is armed it is worth pressing, full stop.

⚠ **The band names no id, and that is the point.** "Hand of Gul'dan is currently
showing something other than Hand of Gul'dan" is the whole condition — structurally the
same rule the client facts give for the row itself, where `overrideSpellID ~= nil` never
means "overridden" and the only honest test is `overrideSpellID ~= spellID`. Writing it
as `identity(…) == Ruination` would need a literal, which makes O4's id disagreement
blocking for no gain.

⚠ **cap can evaluate this, and it has.** `info.overrideSpellID` reads **plain on 21/21
rows in combat** (ClientLab, 2026-08-06) `[client 2026-08-06]`, and E6 fired live in the
M3b flight — `E6:HIGH/1`, six samples, 2026-08-07. The in-combat identity route is real
end to end.

### E7 — Demonbolt `264178`

| | Band | Condition |
| --- | --- | --- |
| 1 | **MEDIUM** | `proc(this)` and `shards ≤ 3` |
| 2 | **LOW** | `proc(this)` |

- **grade:** `shards`, inverted — within band 2, 5 shards reads dimmer than 4.
- **cue:** **positive, HIGH** · gate `proc(this)` → channel `stacks(Demonic Core) ≥ 4`.
- No band without a proc: unprocced it is a ~4.5s hardcast and cap has no opinion
  about it.

⚠ **This is the case `spec.md` §3.2 exists for.** Demonbolt refunds 2 shards, so
pressing it at 4 or 5 throws them away; Blizzard's proc glow says PRESS ME at exactly
the moment the answer is "not yet". Band 2 plus the grade is the demotion, and the
floor is deliberately LOW rather than none — losing the proc entirely is worse than
an over-loud one.

⚠ **The overcap hole is closed by the cue, not by a band.** The rotation's real gate
is "spend cores before they overcap at 4", which needs the Core **stack count** —
sealed, so no band may test it. But a stack count is exactly what the threshold
register is *for*: the client quantises it and draws the number, cap never learns it,
and the number is drawn in the HIGH treatment. So at 4 cores a lit "4" appears on
Demonbolt and it reads HIGH, while the band underneath stays MEDIUM or LOW on shards.

This is the same device as E8's, pointed at a different sealed count, and it produces
the one thing the shard grade cannot say: *spend this now or lose one*. The two signals
compose rather than fight — the band says "how much is this worth against your shard
bar", the cue says "the core bar is full". Neither required cap to see a count.

### E8 — Implosion `196277`

| | Band | Condition |
| --- | --- | --- |
| 1 | **MEDIUM** | `ready(this)` |

- **cue:** **positive, HIGH** · gate `ready(this)` → channel `stacks(Wild Imp) ≥ 6`.

⚠ **Implosion is the catalog's defining constraint case, and it is where the two
registers meet.** Its true gate is a Wild Imp count, which is sealed and has no
continuous channel at all — so the client quantises it and draws a number, and cap
never learns the value. **The number is drawn in the HIGH treatment**, so at 6+ imps
with the button up, Implosion reads HIGH like anything else that is worth pressing.
What cannot be done is *computing* that HIGH: no band may test the count, which is why
the entry's own bands stop at MEDIUM and the HIGH lives in the cue (`spec.md` §3.1).

⚠ **The band stops at MEDIUM for a second reason.** A 15s cooldown means `ready(this)`
is true most of a pull, so a HIGH *band* here would be permanently lit — the same
failure as a HIGH that never fires. The cue does not have that problem: the imp count
crosses 6 in bursts, so the HIGH-styled number arrives and leaves with the actual
opportunity. This is the case that shows a cue is not a weaker signal than a band, only
a differently-computed one.

⚠ On single target without **To Hell and Back**, imploding is a loss — and cap cannot
see target count (`spec.md` §6). So the cue is the entire signal, and on a build
without that talent the entry is honest but thin.

### E9 — Power Siphon `264130`

| | Band | Condition |
| --- | --- | --- |
| 1 | **MEDIUM** | `ready(this)` and `not proc(E7)` |
| 2 | **LOW** | `ready(this)` |

⚠ The rotation gate is "Demonic Core stacks ≤1", and the count is sealed. `not proc(E7)`
— *no* core lit on Demonbolt — is the readable proxy and is strictly stricter than the
real gate, so band 1 under-fires rather than over-fires. Band 2 keeps it visible in
the ≤1-core case cap cannot see.

⚠ **Negation is doing real work here, not standing in for an ordering.** "No core is lit"
is a fact about the fight, and it is E9's own reason to press rather than a statement
about what E7 came out as. A positive cue on E7 would say nothing: both of E7's bands
already require `proc(this)`, so the inverse has no band to decorate.

⚠ It also needs 2 Wild Imps out to do anything, which cap cannot check. A press at
zero imps is wasted; the same sealed count that limits Implosion limits this.

### E10 — Shadow Bolt `686` (the floor)

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `identity(this) ≠ base` and `shards ≤ 2` |
| 2 | **LOW** | `identity(this) ≠ base` |
| 3 | **LOW** | *(unconditional)* |

This catalog's named **floor** (`spec.md` §3.0), and it **has a CDM row** — Essential,
alongside the rest of the kit. So the floor is drawable, and "press it if nothing above it
is lit" is a thing cap can show rather than a convention the player has to learn.

⚠ **Band 3 is deliberate and is not a HIGH in disguise.** Plain Shadow Bolt is always a
legal press and never the best one; LOW is precisely that statement. Without it the floor
would be drawn at the *no-opinion* treatment, i.e. dimmer than everything cap has an
opinion about — actively backwards, because when nothing else is lit Shadow Bolt is the
answer.

⚠ **Infernal Bolt is not "strictly better and equally unconditional", and treating it that
way was the mistake bands 1 and 2 correct.** It rides this row as a display override under
Diabolist, armed by Art: Mother of Chaos, and it **grants 3 shards**
(`knowledge/classes/warlock/demonology/diabolist-sequences.md`). Against a 5-shard cap that
makes it structurally the same case as E7's Demonbolt: at 3 or more shards, pressing it
throws shards away. `shards ≤ 2` is the exact line — 2 + 3 fits, 3 + 3 does not.

⚠ **Band 2 keeps it visible while wasting**, for E7's reason: an armed Art is a real
opportunity and hiding it is worse than an over-loud one. LOW says *press it if nothing
else is lit, and know you are leaking a shard.*

⚠ **`identity` is the route because the aura route is not available.** Infernal Bolt has a
tracked-buff row of its own — cid `172289`, aura `433891`, `flags = 2` (`HideByDefault`) —
and it is **hidden**, so it binds nothing and `auraUp` cannot see it. The transform is
readable on the Shadow Bolt row's own display identity, in combat, which is the same route
E6 uses. ⚠ Like E6, the honest test is "this row is showing something other than its base
spell" — which is exactly what bands 1 and 2 say, and it names no spell id. ⚠ The subject
is `this`: the grammar is `identity(this) ≠ base` on the Shadow Bolt row, never
`identity(Infernal Bolt)`.

---

## 3. Silence — the deliberate no-opinion list

Every row the Cooldown Manager tracks on this spec appears above or here
(`spec.md` §3.5, coverage check).

**A line here names an ability and covers every row carrying that base spellID**, unless
an entry claims a specific row. That is what lets one line cover Unending Resolve's two
rows and Diabolic Ritual's two; it is also why Call Dreadstalkers needs a line *despite*
having an entry — E2 claims the Essential press row and nothing claims the BuffBar one.

⚠ **A silence is still nameable as a subject** (`spec.md` §3.0). Demonic Core, Wild Imp
and Dominion of Argus are all read by a band, a grade or a cue; being silent means cap has
no opinion about *pressing* them, not that it cannot see them.

| Row | Why cap has no opinion |
| --- | --- |
| Demonic Core `264173` | A proc, not a press. Read by E7's band and E7's cue. |
| Wild Imp `296553` | A count, not a press. Read by E8's cue. |
| Call Dreadstalkers `104316` — **the BuffBar row only** | The pets' own aura bar, not the press. E2 grades the Essential row; a summon binds no aura, so this row carries none and nothing reads it. |
| Diabolic Ritual `428514` (two rows) | A progress container. Its payoff is Ruination, which E6 grades; the per-stage auras are not tracked. |
| Dominion of Argus `1276166` | Read by E5 as a buff. Whether it is a press at all is unsettled — see O5. |
| Unending Resolve `104773`, Dark Pact `108416` | Defensives. cap has no read on incoming damage and will not guess when you need one. |
| Shadowfury `30283`, Mortal Coil `6789`, Blight of Tongues `1271802`, Command Demon `119898` | Situational CC and interrupt. The trigger is the fight, not the rotation. |
| Demonic Circle: Teleport `48020` | Movement. Same reason. |
| Summon Felguard `30146` | Pre-pull. |
| Doom `460551` | **Passive** — applied by Demonbolt, not pressed. |
| Demonic Strength, Bilescourge Bombers, Guillotine | **Not on the Midnight Demonology tree.** They appear in no row of the 12.0.7 talent data, on this spec or any other. Listed here because older guides still name them and their absence should read as a decision. |

---

## 4. Cooldown roster (`spec.md` §3.4)

Four bars, in this order:

1. **Summon Demonic Tyrant** — the spec's clock. Everything else is timed against it.
2. **Call Dreadstalkers** — the one you have to plan against Tyrant.
3. **Grimoire** (whichever is talented) — staged into the window when it is up.
4. **Implosion** — the press whose limiting factor is its cooldown for most of a pull.

**The order is part of the declaration**, because a panel stacks. **This list, and the
addon's `bars` list transcribing it, are the only declaration of the roster** — §1's table
carries no bar column and no entry in §2 carries a `bar` field, because a per-entry flag
carries no order and two declarations of one fact drift. The addon enforces its half: an
entry declaring `bar` is a load-time finding, as is a `bars` id that is not a declared entry.

Each bar carries `spec.md` §3.1's tier signal, **and its entry's cues with it**. E2's bar
is the clearest case: it stays HIGH while the hold cue is lit, and the hold marker is what
says *wait* — a ready cooldown you should pool is still ready (`spec.md` §3.4).

⚠ **The bar is the roomier surface, and E1's and E2's holds are the reason that matters
here.** Both are cross-ability countdowns, which is exactly the kind of cue an icon has no
room for — see `spec.md` §6's cue-budget question.

⚠ **Implosion earns a bar because the cooldown is what gates it in steady state.** Once the
rotation is rolling you almost always have 6+ Wild Imps up, so the count is **saturated** and
stops discriminating; what decides whether you may press is the **15 s cooldown**. The count
is the limiting factor at the start of a pull and the cooldown is the limiting factor for the
rest of it — and the rest of it is most of it. ⚠ **The same argument bears on E8's own cue**,
which this section does not settle: `../discussion.md` **D12**.

⚠ **Summon Doomguard gets no bar, because on this build it would draw nothing at all.** O3
settled it: `1276672` appears in no row of the 21-row capture, so E4 is authored and dropped
at bind. The **entry** stays — a build that talents it gets it back for free — but a bar for
a row that never binds is a hole in the panel rather than a spare.

⚠ **Power Siphon gets no bar, and the cooldown is not the reason.**
Its 30 s cooldown is not what gates it: the gate is "Demonic Core stacks ≤ 1", which cap
cannot see (E9). On this build it also drops at bind, alongside E4.

⚠ **A bar whose entry holds no tier still counts down.** Every one of E1/E2/E3's bands needs
`ready(this)`, so the roster is tier-less for exactly the stretch its bar has something to
show; the fill recedes to `spec.md` §3.4's resting slate and the countdown carries on. Whether
that stretch should also be *graded* is `../discussion.md` **D7**, which M4's drawn bars were
always the thing meant to decide.

---

## 5. Sequences (`spec.md` §3.3)

⚠ **This section is the least settled part of the catalog.** M5 is the last milestone
and nothing here has been flown. Treat the steps as a first draft to be checked
against a real pull, not as researched fact.

A trigger is **a band-legal condition** plus `casts == n`, which is legal here and nowhere
else (`spec.md` §3.5).

### The Tyrant window — confidence: medium

- **enter:** `ready(E1)`
- **steps:** Call Dreadstalkers → Grimoire → Summon Doomguard → Summon Demonic Tyrant
  → Hand of Gul'dan
- **drop:** any cast that is not the current or next step.

⚠ The build-to-shards phase that precedes this in the rotation is **not** in the
sequence: it is one button pressed repeatedly, which the tier field already carries as
E10's LOW. A sequence hint adds nothing to "keep pressing the filler".

⚠ Steps 2 and 3 are skipped when the ability is on cooldown or untalented, which is
the common case. A sequence whose steps mostly do not apply is a bad hint — whether
this reads as helpful or as noise is the thing the first flight decides.

### The opener — confidence: LOW, drafted only

- **enter:** `combat` and `casts == 0`
- **steps:** unsettled.

⚠ The rotation sources describe the opener as Power Siphon → Hand of Gul'dan on the
apex proc → Grimoire → Doomguard → Dreadstalkers → Tyrant, but that list starts with
an ability that needs Wild Imps already out, which at a pull you do not have. Do not
transcribe it into the addon until it has been checked against the simc opener or a
real pull.

---

## 6. Open questions

- **O1 — "spend the Tyrant window on Hand of Gul'dan" has no expressible form.**
  Nothing in the tracked set carries the Tyrant buff, so there is neither an `auraUp`
  gate nor an `auraRemaining` channel for "a Tyrant is active", and E5 has no band for
  it. ⚠ **The route back is a read, not an estimate:** enable the `HideByDefault`
  Summon Demonic Tyrant bar (cid `84224`) and confirm it binds and yields a duration —
  that turns the missing band into an exact channel. A fixed duration off our own cast is
  not the fallback; it is the thing that was deleted.
- **O2 — ~~the estimate under cooldown reduction~~ MOOT.** It asked whether anything on
  the live build shortens Tyrant's cooldown and silently broke cap's own count-down from a
  declared base cooldown. **cap no longer counts anything down** — every remaining time is
  a `cooldownRemaining` channel the client evaluates — so the arithmetic the question
  worried about does not exist.
- **O3 — is Summon Doomguard in the build? SETTLED: no.** `1276672` appears in no row
  of cap's 21-row Demonology capture, so **E4 drops at bind** on this build. The entry
  stays authored — a build that talents it gets it back for free. Power Siphon `264130` is absent for
  the same kind of reason and **E9 drops too**: Implosion `196277` is the talented half
  of their choice node. The authored catalog has ten entries; this build runs eight.
- **O4 — the transform ids disagree.** Ruination reads `433885` from DB2 and `434635`
  in older project notes; Infernal Bolt reads `433891` and `434506` the same way.
  E6 binds by observation so this does not block, but the discrepancy should be
  resolved in `knowledge/addon-dev/` rather than left in two docs.
- **O5 — what is Dominion of Argus? PARTLY SETTLED.** The live capture puts it on the
  **BuffBar** viewer (cid `169561`, base `1276166`) — the aura family, not a press — so
  E5's "it is a buff" assumption holds and it needs no entry of its own. What it does
  *not* settle is whether `auraUp` fires on it, which the E5 apex band depends on.
  ⚠ **The id is `1276166` and the Game Data API will tell you otherwise.** It resolves
  a *different* spell of the same name at `1276163` and errors on `1276166` — but
  `1276163` matches no CDM row. When a static namespace and the running client disagree
  about an id, the client wins.
- **O6 — Tyrant with an empty shard bar.** E1 grades Tyrant on the Dreadstalkers
  being spent, not on having shards to spend during the window. The rotation says to
  enter at 5 shards. Whether shards belong in band 1 is a play question — decide it
  from a flown pull, not from the APL.
- **O7 — how much of this catalog is lit at once, desk-checked.** Walking the bands by
  hand: a Tyrant setup lights **three** HIGH at once (Dreadstalkers, Grimoire, Hand of
  Gul'dan at 5 shards). Steady state between windows lights **none** — HIGH here is
  reserved for cooldowns, overcap and Ruination. Neither is dishonest, and both are what
  the rotation actually is. Whether long no-HIGH stretches read as "nothing is urgent" or
  as "the addon is asleep" is a play question, and it is answered by playing: `spec.md`
  §3.5's HIGH-at-once distribution is the instrument for explaining what a moment felt
  like, not a number that decides whether the catalog is good.
  ⚠ **E10 softens the no-HIGH stretches.** With the floor graded LOW, a no-HIGH stretch is
  not a dark field — Shadow Bolt is lit at the bottom tier, which is the readable form of
  "keep building", and "the addon is asleep" is a much weaker reading when something is
  always lit. E10's HIGH is also the only one that fires in steady state: an armed Art:
  Mother of Chaos at low shards lights the floor row HIGH between Tyrant windows, where
  previously nothing was HIGH at all.
- **O8 — E2's hold threshold is a single point where the rotation wants a band.** The real
  hold zone is `12 < cooldownRemaining(E1) < 20`; the channel vocabulary offers only
  `≤ t`, so `t = 20` over-fires through the last twelve seconds, where the dogs pressed now
  are still out when Tyrant lands and get extended. ⚠ **A fix exists and it is a spec
  change, deliberately not made here:** a multi-point `Step` curve thresholds a secret
  duration into a *band* entirely C-side
  (`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1 finding 4, measured),
  which would be a `cooldownRemaining(x) ∈ [lo,hi]` channel form. Decide it against a flown
  pull — the marker being over-eager may or may not read badly in play.

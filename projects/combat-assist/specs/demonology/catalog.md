# Demonology Warlock — catalog

**What this file is for:** the tier rules, windows, cues, cooldown roster and
sequences cap uses on Demonology. It is the normative form of the catalog defined in
`../spec.md` §3.5 — the addon's Lua table is a transcription of this document, and if
the two disagree the table is wrong.

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

| Ability | ID | CD | Cost | Entry | Bar |
| --- | --- | ---: | --- | --- | --- |
| Summon Demonic Tyrant | `265187` | 60s | none | E1 | ✅ |
| Call Dreadstalkers | `104316` | 20s | 2 shards (free w/ Demonic Calling) | E2 | ✅ |
| Grimoire: Fel Ravager / Imp Lord | `1276467` / `1276452` | 120s | shards | E3 | ✅ |
| Summon Doomguard | `1276672` | 120s | shards | E4 | ✅ |
| Hand of Gul'dan | `105174` | — | 3 shards | E5 | — |
| — transforms to **Ruination** | (observed) | — | free | E6 | — |
| Demonbolt | `264178` | — | a Demonic Core | E7 | — |
| Implosion | `196277` | 15s | consumes Wild Imps | E8 | — |
| Power Siphon | `264130` | 30s | consumes ≤2 Wild Imps | E9 | — |
| Shadow Bolt | `686` | — | free, generates | E10 | — |
| — transforms to **Infernal Bolt** | (observed) | — | — | E10 | — |

⚠ **Implosion and Power Siphon are two halves of one choice node** (spec tree row 5).
Exactly one of them exists on any build; the other's entry is dropped at bind time.
Grimoire is the same shape at row 10.

**Cue and window sources — read, never graded, never given an entry:**

| Row | ID | Used by |
| --- | --- | --- |
| Wild Imp | `296553` | Implosion's threshold cue (E8) |
| Demonic Core | `264173` | Demonbolt's proc gate, and `cores_dry` |
| Dominion of Argus | `1276166` (buff) | Hand of Gul'dan's apex band (E5) |
| Call Dreadstalkers — the **BuffBar** row | `104316` | Tyrant's staged band (E1), via `auraUp` |

⚠ **Call Dreadstalkers occupies two rows and they mean different things.** The
Essential row is the press E2 grades; the BuffBar row is the pets' aura and is E1's
`auraUp` source. A roster that binds one row per spellID picks whichever it walks first
and is wrong for one of the two gates — so binding is keyed by `{spellID, family}`.

`shards` below is this spec's instance of `spec.md` §3.5's `resource` gate — Soul
Shards are a secondary resource, so cap may both read and branch on the count.

Costs and cooldowns above are Tier-1 (`wowkb.spec_inventory`, DB2 @ 12.0.7 —
`knowledge/classes/warlock/demonology/`). ⚠ **Summon Demonic Tyrant costs nothing**;
older project docs that say 1 shard are stale.

---

## 2. Windows

**All six of the six allowed — the cap is now reached.** Each is a situation in the
fight, and each is the only place a negation or a cross-ability read is permitted.

| Window | Rule | Holds when | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `tyrant_setup` | `ready(E1)` | Tyrant is **ready** | the `Available` alert edge — exact, not an estimate | **high** |
| `tyrant_far` | `not ready(E1)` and `remaining(E1) > 20` | Tyrant is **not ready** and cap's own count says it is >20s out | readiness edge + our arithmetic over our own cast | **medium** — the estimate half can be wrong; it degrades to holding Dreadstalkers a beat too long, never to a false release |
| `tyrant_active` | `elapsed(E1) ≤ 15` | within ~15s of an observed Tyrant cast | our own cast + a fixed duration | **low** — see open question O1 |
| `dogs_out` | `elapsed(E2) ≤ 12` | within ~12s of an observed Call Dreadstalkers cast | our own cast + a fixed duration | **medium** — the pets' real lifetime is extended by a Tyrant cast, so this reads *short*; it closes while they are still up, never opens while they are not |
| `cores_dry` | `not proc(E7)` | no Demonic Core proc is lit on Demonbolt | overlay glow, readable in combat | **high** for "zero cores"; it cannot mean "one core" |
| `opener` | `combat` and `casts == 0` | in combat, before the first observed rotational cast | combat entry + cast history | **high** |

⚠ **`elapsed` is stamped by the `OnCooldown` alert edge, not by a cast we watched for.**
The client raising "this went on cooldown" is the same instant as the press for every
ability that has one, and it needs no second instrument. `casts` is the exception and is
counted from observed presses, because the floor has no cooldown to announce.

⚠ **`remaining` rests on a declared base cooldown** (§1's CD column, Tier-1 from DB2),
corrected from the client whenever it will say — which is out of combat only. That single
declared number is where O2 bites: anything that shortens Tyrant's cooldown makes
`tyrant_far` late, and it is late in one place rather than smeared across two bands.

⚠ **`dogs_out` is a window and not a gate, and that is forced.** "Are the Dreadstalkers
out" is a fact about a *different* ability than the entry that reads it (E1 grades
Tyrant), and cross-ability reasoning is legal only inside a window. It is also the only
form available: **a summon has no aura to read.** The pets are units in the world, so
there is no bound aura on any row and `auraUp` cannot express it — see the note under
E1 and `knowledge/addon-dev/cooldown-manager.md`.

⚠ **`tyrant_setup` and `tyrant_far` deliberately leave a gap** — from Tyrant going on
cooldown until it is >20s out. That gap is the hold zone, and it is expressed by
*neither* window being true, so no band has to say "not". This is the shape `spec.md`
§3.5 asks for: name the situations where a press is right, and let the absence of them
demote.

⚠ **cap does not anticipate — a window opens when the ability is actually ready, never
before.** `tyrant_setup` used to try "≤3s out", which needed a cooldown-remaining number
that is sealed in combat and would have been our own drifting arithmetic. Dropping it
costs a few seconds of pre-warning and buys an **exact** window off the `Available` edge.
The one estimate left is `tyrant_far`'s ">20s", where being wrong means holding
Dreadstalkers slightly too long rather than releasing them into a window that is not
coming.

---

## 3. Entries

Bands are first-match **within one entry**. Entries never see each other.

### E1 — Summon Demonic Tyrant `265187`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `window(dogs_out)` |
| 2 | **MEDIUM** | `ready(this)` |

- **grade:** `cooldownRemaining(this)` — the icon warms as the window approaches.
  This is the contextualising half of the spec's centrepiece: you should be able to
  see a burst window coming without reading a number.
- **bar:** yes.

⚠ Band 1 is "the board is staged", read through the one piece of the board cap can
account for: it saw you cast the Dreadstalkers and they last about twelve seconds.
Wild Imps and the Grimoire demon are not observable at all, so band 1 is *necessary
but not sufficient* for a good Tyrant — and that is fine. It grades the press's value;
it does not grant permission to press.

⚠ **There is no aura to read, and that is settled rather than unmeasured.** A summon
creates units in the world; it applies no aura, so no CDM row carries a bound one for
it and `auraUp` cannot express "the dogs are out" on any spec. The window is not a
fallback from a better read — it is the only shape available. (Measured alongside: 13
in-combat samples on the Dreadstalkers BuffBar row, never bound, while five genuine
aura rows on the same viewers bound normally.)

⚠ The consequence for band 1 is that it reads **short**, not wrong: a Tyrant cast
extends pets already out, so the window can close while the dogs are still up. cap then
demotes Tyrant to MEDIUM slightly early, which understates a good press rather than
inventing one.

### E2 — Call Dreadstalkers `104316`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `affordable(this)` and `window(tyrant_setup)` |
| 2 | **HIGH** | `ready(this)` and `affordable(this)` and `window(tyrant_far)` |
| 3 | **MEDIUM** | `ready(this)` and `affordable(this)` |

- **grade:** `cooldownRemaining(this)`.
- **bar:** yes.

⚠ Band 3 is the hold: Dreadstalkers last ~12s and Tyrant extends what is already out,
so firing them 15s before the window wastes the pair. cap demotes rather than hides —
`spec.md` §3.1's LOW/MEDIUM distinction earns its keep here, and pressing anyway is a small
loss, not a mistake. The rotation source gates on "Tyrant ≥20s away or ≤12s away"; this
catalog releases on `ready(E1)` instead, which is exact off the `Available` edge — see §2's
last ⚠ for why the ≤3s form was dropped. ⚠ Both bands 1 and 2 rest on an estimate (see O2).

### E3 — Grimoire: Fel Ravager `1276467` / Imp Lord `1276452`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `window(tyrant_setup)` |
| 2 | **MEDIUM** | `ready(this)` |

- **bar:** yes.

⚠ A 2-minute cooldown is absent from roughly half of all Tyrant windows, so it is
staged into the window when it is up and **never gates it**. Band 2 exists because a
Grimoire pressed outside a window is still a summon, not a waste.

### E4 — Summon Doomguard `1276672`

Same shape as E3. `talent(Summon Doomguard)`-gated; dropped when untalented or when
no CDM row tracks it.

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `window(tyrant_setup)` |
| 2 | **MEDIUM** | `ready(this)` |

- **bar:** yes.

⚠ See open question O3 — the sources disagree about whether this is part of the live
build at all.

### E5 — Hand of Gul'dan `105174`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `auraUp(Dominion of Argus)` and `affordable(this)` |
| 2 | **HIGH** | `window(tyrant_active)` and `affordable(this)` |
| 3 | **HIGH** | `shards ≥ 5` and `affordable(this)` |
| 4 | **MEDIUM** | `affordable(this)` |

- **grade:** `shards` — within band 4, four shards reads brighter than three. Shards
  are readable, so cap computes this itself rather than handing it to a curve.

⚠ Three separate reasons to press it, and they are genuinely different situations:
the apex proc makes it free, the Tyrant window makes it the thing you spend the
window on, and 5 shards makes it spend-or-waste. Band 4 is the ordinary case and is
true for most of a pull — which is correct. Hand of Gul'dan being usually-worth-
pressing is what a Demonology field should look like.

⚠ There is no band for "hold shards because Tyrant is near". The rotation's pooling
is **emergent** — the window's own bands and the builder floor produce it — and
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
- **cue:** gate `proc(this)` → threshold `stacks(Demonic Core) ≥ 4` → drawn **HIGH**.
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

- **cue:** gate `ready(this)` → threshold `stacks(Wild Imp) ≥ 6` → drawn **HIGH**.

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
| 1 | **MEDIUM** | `ready(this)` and `window(cores_dry)` |
| 2 | **LOW** | `ready(this)` |

⚠ The rotation gate is "Demonic Core stacks ≤1", and the count is sealed.
`cores_dry` — *no* core lit — is the readable proxy and is strictly stricter than the
real gate, so band 1 under-fires rather than over-fires. Band 2 keeps it visible in
the ≤1-core case cap cannot see.

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
spell" — which is exactly what bands 1 and 2 say, and it names no spell id.

---

## 4. Silence — the deliberate no-opinion list

Every row the Cooldown Manager tracks on this spec appears above or here
(`spec.md` §3.5, coverage check).

**A line here names an ability and covers every row carrying that base spellID**, unless
an entry claims a specific row. That is what lets one line cover Unending Resolve's two
rows and Diabolic Ritual's two; it is also why Call Dreadstalkers needs a line *despite*
having an entry — E2 claims the Essential press row and nothing claims the BuffBar one.

| Row | Why cap has no opinion |
| --- | --- |
| Demonic Core `264173` | A proc, not a press. Feeds E7 and `cores_dry`. |
| Wild Imp `296553` | A count, not a press. Feeds E8's cue. |
| Call Dreadstalkers `104316` — **the BuffBar row only** | The pets' own aura bar, not the press. E2 grades the Essential row; this one is E1's `auraUp` source and is read, never graded. |
| Diabolic Ritual `428514` (two rows) | A progress container. Its payoff is Ruination, which E6 grades; the per-stage auras are not tracked. |
| Dominion of Argus `1276166` | Feeds E5 as a buff. Whether it is a press at all is unsettled — see O5. |
| Unending Resolve `104773`, Dark Pact `108416` | Defensives. cap has no read on incoming damage and will not guess when you need one. |
| Shadowfury `30283`, Mortal Coil `6789`, Blight of Tongues `1271802`, Command Demon `119898` | Situational CC and interrupt. The trigger is the fight, not the rotation. |
| Demonic Circle: Teleport `48020` | Movement. Same reason. |
| Summon Felguard `30146` | Pre-pull. |
| Doom `460551` | **Passive** — applied by Demonbolt, not pressed. |
| Demonic Strength, Bilescourge Bombers, Guillotine | **Not on the Midnight Demonology tree.** They appear in no row of the 12.0.7 talent data, on this spec or any other. Listed here because older guides still name them and their absence should read as a decision. |

---

## 5. Cooldown roster (`spec.md` §3.4)

Four bars, in this order:

1. **Summon Demonic Tyrant** — the spec's clock. Everything else is timed against it.
2. **Call Dreadstalkers** — the one you have to plan against Tyrant.
3. **Grimoire** (whichever is talented) — staged into the window when it is up.
4. **Summon Doomguard** — same, when the build has it.

Each bar carries `spec.md` §3.1's tier signal, so E2's hold zone reads as a visibly
different bar from a ready-and-go one.

⚠ **Implosion and Power Siphon get no bar** despite having cooldowns. A 15s bar is
noise, and neither ability's decision is about time remaining — it is about a count
cap cannot see.

---

## 6. Sequences (`spec.md` §3.3)

⚠ **This section is the least settled part of the catalog.** M5 is the last milestone
and nothing here has been flown. Treat the steps as a first draft to be checked
against a real pull, not as researched fact.

### The Tyrant window — confidence: medium

- **enter:** `window(tyrant_setup)`
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

- **enter:** `window(opener)`
- **steps:** unsettled.

⚠ The rotation sources describe the opener as Power Siphon → Hand of Gul'dan on the
apex proc → Grimoire → Doomguard → Dreadstalkers → Tyrant, but that list starts with
an ability that needs Wild Imps already out, which at a pull you do not have. Do not
transcribe it into the addon until it has been checked against the simc opener or a
real pull.

---

## 7. Open questions

- **O1 — `tyrant_active` has no observable source.** Nothing in the tracked set
  carries the Tyrant buff, so the window is our own cast plus a fixed duration.
  Confirm the buff's real duration, and check whether a CDM row can be made to track
  it — a bound aura would turn a guess into a read.
- **O2 — the estimate under cooldown reduction.** `tyrant_setup` / `tyrant_far` count
  down from our own observation of our own cast. Anything that shortens Tyrant's
  cooldown silently breaks both. Confirm nothing on the live build does.
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
  being out, not on having shards to spend during the window. The rotation says to
  enter at 5 shards. Whether shards belong in band 1 is a play question — decide it
  from a flown pull, not from the APL.
- **O7 — how much of this catalog is lit at once, desk-checked.** Walking the bands by
  hand: a Tyrant setup lights **three** HIGH at once (Dreadstalkers, Grimoire, Hand of
  Gul'dan at 5 shards). But steady state between windows lights **none** — HIGH here is
  reserved for cooldowns, overcap and Ruination — and the Tyrant window itself lights
  exactly **one** (Hand of Gul'dan). Neither is dishonest, and both are what the rotation
  actually is. Whether long no-HIGH stretches read as "nothing is urgent" or as "the addon
  is asleep" is a play question, and it is answered by playing: `spec.md` §3.5's
  HIGH-at-once distribution is the instrument for explaining what a moment felt like, not
  a number that decides whether the catalog is good.
  ⚠ **E10 softens the no-HIGH stretches.** With the floor graded LOW, a no-HIGH stretch is
  not a dark field — Shadow Bolt is lit at the bottom tier, which is the readable form of
  "keep building", and "the addon is asleep" is a much weaker reading when something is
  always lit. E10's HIGH is also the only one that fires in steady state: an armed Art:
  Mother of Chaos at low shards lights the floor row HIGH between Tyrant windows, where
  previously nothing was HIGH at all.

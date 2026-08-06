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

⚠ **Implosion and Power Siphon are two halves of one choice node** (spec tree row 5).
Exactly one of them exists on any build; the other's entry is dropped at bind time.
Grimoire is the same shape at row 10.

**Cue and window sources — read, never graded, never given an entry:**

| Row | ID | Used by |
| --- | --- | --- |
| Wild Imp | `296553` | Implosion's threshold cue (E8) |
| Demonic Core | `264173` | Demonbolt's proc gate, and `cores_dry` |
| Dominion of Argus | `1276166` (buff) | Hand of Gul'dan's apex band (E5) |

`shards` below is this spec's instance of `spec.md` §3.5's `resource` gate — Soul
Shards are a secondary resource, so cap may both read and branch on the count.

Costs and cooldowns above are Tier-1 (`wowkb.spec_inventory`, DB2 @ 12.0.7 —
`knowledge/classes/warlock/demonology/`). ⚠ **Summon Demonic Tyrant costs nothing**;
older project docs that say 1 shard are stale.

---

## 2. Windows

Five of the six allowed. Each is a situation in the fight, and each is the only place
a negation or a cross-ability read is permitted.

| Window | Holds when | Evidence | Confidence |
| --- | --- | --- | --- |
| `tyrant_setup` | Tyrant is ready, **or** cap's own count says it is ≤3s out | readiness edges + baseline; the "≤3s" half is cap's arithmetic over its own observed cast | **medium** — the estimate half can be wrong; it degrades to "the window opens a beat late", never to a false open |
| `tyrant_far` | Tyrant is >20s out by the same count, or has not been cast this fight and is not ready | same | **medium** |
| `tyrant_active` | within ~15s of an observed Tyrant cast | our own cast + a fixed duration | **low** — see open question O1 |
| `cores_dry` | no Demonic Core proc is lit on Demonbolt | overlay glow, readable in combat | **high** for "zero cores"; it cannot mean "one core" |
| `opener` | in combat, before the first observed rotational cast | combat entry + cast history | **high** |

⚠ **`tyrant_setup` and `tyrant_far` deliberately leave a gap** — roughly 3s to 20s
before Tyrant. That gap is the hold zone, and it is expressed by *neither* window
being true, so no band has to say "not". This is the shape `spec.md` §3.5 asks for: name the
situations where a press is right, and let the absence of them demote.

---

## 3. Entries

Bands are first-match **within one entry**. Entries never see each other.

### E1 — Summon Demonic Tyrant `265187`

| | Band | Condition |
| --- | --- | --- |
| 1 | **HIGH** | `ready(this)` and `auraUp(Call Dreadstalkers)` |
| 2 | **MEDIUM** | `ready(this)` |

- **grade:** `cooldownRemaining(this)` — the icon warms as the window approaches.
  This is the contextualising half of the spec's centrepiece: you should be able to
  see a burst window coming without reading a number.
- **bar:** yes.

⚠ Band 1 is "the board is staged", read through the one piece of the board that is
actually observable in combat: the Dreadstalkers row carries a live bound aura while
the dogs are out. Wild Imps and the Grimoire demon are not readable that way, so band
1 is *necessary but not sufficient* for a good Tyrant — and that is fine. It is a
grade of the press's value, not permission to press.

⚠ **Confidence: medium on the read itself.** That the Dreadstalkers buff-bar row
carries a live bound aura for the pair's duration is an inference from the row
existing and from bound-aura presence being readable in combat generally. Confirm it
before E1 band 1 ships; if it does not hold, Tyrant collapses to one band and the
entry loses its whole point.

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
loss, not a mistake. The rotation source gates on "Tyrant ≥20s away or ≤12s away";
this catalog uses ≤3s for the release because that is the edge cap can see most
reliably. ⚠ Both bands 1 and 2 rest on an estimate (see O2).

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
| 1 | **HIGH** | `identity(Hand of Gul'dan) == Ruination` |

Free, large, and it replaces the button you were already going to press. There is no
band below it: when it is armed it is worth pressing, full stop.

⚠ **Bind by following the override, not by matching an id.** The project's sources
disagree on Ruination's spell id, which is itself the argument for observing the
transform (see O4).

### E7 — Demonbolt `264178`

| | Band | Condition |
| --- | --- | --- |
| 1 | **MEDIUM** | `proc(this)` and `shards ≤ 3` |
| 2 | **LOW** | `proc(this)` |

- **grade:** `shards`, inverted — within band 2, 5 shards reads dimmer than 4.
- No band without a proc: unprocced it is a ~4.5s hardcast and cap has no opinion
  about it.

⚠ **This is the case `spec.md` §3.2 exists for.** Demonbolt refunds 2 shards, so
pressing it at 4 or 5 throws them away; Blizzard's proc glow says PRESS ME at exactly
the moment the answer is "not yet". Band 2 plus the grade is the demotion, and the
floor is deliberately LOW rather than none — losing the proc entirely is worse than
an over-loud one.

⚠ The rotation's real gate is "spend cores before they overcap at 4", which needs the
Core **stack count** — sealed. cap grades on shards instead, which is the other side
of the same decision and is readable. It will therefore be quiet about a core about
to overcap. That is a known, accepted hole, not an oversight.

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

---

## 4. Silence — the deliberate no-opinion list

Every row the Cooldown Manager tracks on this spec appears above or here
(`spec.md` §3.5, coverage check).

| Row | Why cap has no opinion |
| --- | --- |
| **Shadow Bolt** `686` / **Infernal Bolt** `433891` | **The named floor.** The right press whenever nothing else is lit. Not tracked by the CDM, so there is no icon to dim — on Demonology "the field is dark" *means* go build shards. See `spec.md` §6. |
| Demonic Core `264173` | A proc, not a press. Feeds E7 and `cores_dry`. |
| Wild Imp `296553` | A count, not a press. Feeds E8's cue. |
| Diabolic Ritual `428514` (two rows) | A progress container. Its payoff is Ruination, which E6 grades; the per-stage auras are not tracked. |
| Dominion of Argus `1276163` | Feeds E5 as a buff. Whether it is a press at all is unsettled — see O5. |
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
sequence, because its steps are Infernal Bolt and Shadow Bolt, which have no CDM
icons to hint on. The tier field carries that phase instead.

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
- **O3 — is Summon Doomguard in the build?** The rotation KB puts it fourth in the
  single-target priority as a ~2-min demon cooldown; the last live capture of the
  tracked set does not contain it. Settle whether it is talented, tracked, and cast
  before E4 ships.
- **O4 — the transform ids disagree.** Ruination reads `433885` from DB2 and `434635`
  in older project notes; Infernal Bolt reads `433891` and `434506` the same way.
  E6 binds by observation so this does not block, but the discrepancy should be
  resolved in `knowledge/addon-dev/` rather than left in two docs.
- **O5 — what is Dominion of Argus?** Talent data marks it ACTIVE with no cooldown;
  the ability KB carries an unresolved in-game marker on it. E5's band 1 assumes it
  is a *buff* that empowers Hand of Gul'dan. If it is a pressed cooldown it needs its
  own entry and probably a bar.
- **O6 — Tyrant with an empty shard bar.** E1 grades Tyrant on the Dreadstalkers
  being out, not on having shards to spend during the window. The rotation says to
  enter at 5 shards. Whether shards belong in band 1 is a play question — decide it
  from a flown pull, not from the APL.
- **O7 — the breadth of this catalog, desk-checked.** Walking the bands by hand: a
  Tyrant setup lights **three** HIGH at once (Dreadstalkers, Grimoire, Hand of
  Gul'dan at 5 shards), which is what `spec.md` §3.1 wants. But steady state between
  windows lights **none** — HIGH here is reserved for cooldowns, overcap and
  Ruination — and the Tyrant window itself lights exactly **one** (Hand of Gul'dan).
  Neither is dishonest, and both are what the rotation actually is. Whether long
  no-HIGH stretches read as "nothing is urgent" or as "the addon is asleep" is a play
  question the breadth measure should answer with real numbers.

---
title: Protection Paladin — fact classification
spec: Protection Paladin (Lightsmith) — specID 66, Midnight 12.1
---

# Protection Paladin (Lightsmith) — fact classification

**What this file is for.** The **safety case**: every fact this catalog consumes, sorted readable / sealed-display / open, with its recipe and its evidence. It is separate so it can be read without reading the roster — the question *"does anything here branch on a sealed value?"* must be answerable on its own.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors;
`../render-shelf.md` owns every pixel and this file describes none. Priority source:
`knowledge/classes/paladin/protection/simc-apl.md` (Tier 1, generated, commit `0132642`,
2026-08-18); its prose supplement `rotation.md` is a deliberate pointer stub. Neither is restated
here.

**Three files per spec** (`../authoring.md` §0): a definition, its proof, and its safety case.
Demonology is the model this file follows.

---

## 1. The answer, first

**No sealed fact appears in any Lua condition, in either polarity.** The catalog uses **eight**
sealed values — three cooldown remainings, two readings of one aura count, one aura's remaining
seconds, one client-computed refresh window and one aura's bare existence — and every one of them
goes straight to a client-owned sink:

| Sealed value | Sink | Where |
| --- | --- | --- |
| Divine Toll's cooldown *remaining* | `sealed-cooldown-range`, `beyond = 10` | cue **A**, on Avenging Wrath |
| Avenging Wrath's cooldown *remaining* | `sealed-cooldown-range`, `within = 30` | cue **B**, on Divine Toll |
| Avenging Wrath's cooldown *remaining* | `sealed-cooldown-range`, `beyond = 5` | cue **D**, on Holy Armaments |
| Divine Guidance's application count | `sealed-count-bands`, one breakpoint at five (V16 — silent below, hatch plus negative mark at five) | `as_guidance_capped`, on **Avenger's Shield** |
| Divine Guidance's application count | `sealed-count-bands`, the **complement** (V17 — hatch plus negative mark below five, clean at five) | `cons_awaits_hammer`, on Consecration |
| The Sacred Weapon buff's **remaining seconds** | `sealed-pandemic`'s `outside_s = 6` (V19 — the gold do-not-refresh hatch, off `SetDurationText` breakpoints) | `ha_weapon_healthy`, on Holy Armaments |
| Blizzard's own **refresh window** for that buff | `sealed-pandemic`'s region (V19 — the badge, and cap authors no threshold at all) | `ha_weapon_healthy`, on Holy Armaments |
| Whether the Consecration **player aura** exists | `sealed-count-bands`, a **presence** band (V16 — one band at threshold 0, and the client's own blank as the other state) | `cons_field_up`, on Consecration |

Every other term in every marker is `ready`, `affordable`, `identity`, `talent` or `aura`. Three of
the nine predicates in `Catalog.PREDICATES` go unused — `proc`, `resource`, `aoe` — and two of the
six sealed display kinds go unused (`sealed-count-bar`, `sealed-proc-bar`).
⚠ **`capped` is unused and it is NOT unavailable**, which is a correction rather than a count: it
needs no `charged` declaration (`catalog.md` → *The Charges column*), so it has a subject on every
row here. It goes unspent for a reason about the priority list — see §5.4.
⚠ **Two of the eight subjects hold no Cooldown-Manager row at all**, and that is legal and
load-bearing. A **latch** needs a row, because it rides that row's alert edges; a **display** needs
none, because a sealed container is cap's own frame — `Channel.Arm` builds an `AuraContainer` on
cap's overlay, filters it with `includeSpellIDs`, picks HELPFUL/HARMFUL from `plan.unit` and binds
it with `SetUnit(plan.unit)`. Sacred Weapon's buff `432502` has **zero** `CooldownSetSpell` rows
anywhere *[searched 2026-08-26: whole file, exact `SpellID` match @ 12.1.0.69214]*, and the
Consecration player aura `188370` has none either.
⚠ **`188370` carries `Duration = -1`**, so the only available form on it is a **presence** band —
V19 and V20 are structurally impossible, and the 12 s clock belongs to the cast `26573`.

⚠ **Two of the eight are the same secret read twice, in opposite directions, and the catalog is
correct only because each is gated.** Divine Guidance's count arms V16 on Avenger's Shield and V17
on Consecration; the two tables disagree at every value by construction. Neither is a comparison
cap performs: cap hands the client a table of whole numbers and what to draw at each, the client
evaluates it against the count, and **cap never receives the count, never compares it, and never
learns which band fired.**

⚠ **One of them is armed on a row the aura does not belong to.** `as_guidance_capped` puts Divine
Guidance's count on Avenger's Shield and says *"the row to your right outranks this one."* That is
new — every shipped sealed display before it was a self-test — and it is the reason §4 exists in
this file rather than being a footnote in the roster.

⚠ **The `aura` predicate reads a boolean, and Divine Guidance is read BOTH ways.**
`aura(divine_guidance)` is the CDM alert-edge latch's *is there one at all*, which is **readable**.
*How many* is the sealed count above. They are two different facts about one aura, they answer
two different questions, and §2 keeps them on separate rows deliberately: substituting the boolean
for the count would badge a row in states the APL presses it, and substituting the count for the
boolean is impossible — a band cannot rule out a row whose subject does not exist.

**No sealed marker shares an entry with another sealed marker.** `spec.md` §3.6's union rule (two
sealed markers naming one cue write the same badge from two curves, so each owns an instance) is
not exercised here: Avenger's Shield and Consecration each carry one sealed display beside one
**readable** marker, and readable markers union in Lua.
⚠ **Consecration now declares two sealed displays and they can never both arm** — `cons_awaits_hammer`
requires `talent(divine_guidance)` and `cons_field_up` requires `talent(blessed_assurance)`, the two
halves of choice node `95235`. That is a property of the node rather than of an argument, which is
why the gate is read positively. Holy Armaments' two markers are exclusive the same way: cue **D**
gates on `identity == base` and `ha_weapon_healthy` on `identity == transformed`.
⚠ **Both new markers carry no cue**, so the badge vocabulary is unchanged and the density budget —
which counts only `blocked` — is untouched by either.

---

## 2. Facts, classified

Every fact the catalog consumes — and every fact it names and declines — tagged **readable** /
**sealed-display** / **open** / **not expressible** / **not modelled**, with its recipe and
evidence (`../spec.md` §3.6 is the boundary; `../authoring.md`'s recipe index owns the recipes).

| Fact | Lane | Recipe | Evidence | Consumed by |
| --- | --- | --- | --- | --- |
| Readiness of a cooldown row | **readable** | R2 | CDM `Available` / `OnCooldown` alert-edge latch, `cooldown-manager.md` §5.1; `security-taint-and-restricted-data.md` §4.8 | every lit row, and the `ready` gate on cues **A**, **B**, **D**, **E**, **F** and both sealed count tables |
| Affordability of Shield of the Righteous | **readable** | R1 | `C_Spell.IsSpellUsable` **second** return, no `SecretWhen*` predicate; `security-…` §4.12 | cue **C** (`!affordable`) — the catalog's only `starved` |
| Spell identity across an override | **readable** | R7 | `overrideSpellID` is always populated, so the honest test is `overrideSpellID ~= spellID` (`cooldown-manager.md` §2 rung 4); the cooldown branch resolves it **before** reading the dial (§3.1.1, settled 2026-08-18 on Retribution) | the Holy Armaments row (cue **D**'s gate), the Judgment row (cues **E** and **F**), the Crusader Strike row (no cue) |
| **`next_armament`** — which armament the Holy Armaments row is displaying | **readable** | R7 | Sacred Weapon `432472` holds **zero** `CooldownSetSpell` rows anywhere in the file, so an override on Holy Bulwark `432459` (637 / cat0 / ord 23) is the only route it can take *[T1 DB2: `CooldownSet` / `CooldownSetSpell` @ 12.1.0.69214]*. ⚠ The **direction** of the identity is unverified — §3, §5.1 | cue **D**'s gate. What reads like sim-internal state is the only free fact on row 4 |
| Whether the Judgment row is displaying **Hammer of Wrath** | **readable** *(on a Tier-2 pairing — see the next row)* | R7 | as above; `24275` holds zero rows anywhere *[T1 DB2 @ 12.1.0.69214]* | cue **E** on Avenger's Shield and Consecration; cue **F**'s base-life gate |
| **Which row Hammer of Wrath rides** | **open — Tier 2, marked** | — | `knowledge/classes/paladin/protection/abilities.md:62`, itself carrying `@verify-ingame`, in a file whose front matter reads **patch 12.0.7**. Game data proves only the absence, never the pairing. Retribution authors the same pairing on the same evidence | cues **E** and **F** rest on it. §3, §5.3 @verify-ingame |
| Whether **Glory of the Vanguard** is up | **readable** | R2's alert edges → the `aura` latch | `1267203` is a **Category-2 (TrackedBuff)** row in set 637, OrderIndex 59 *[T1 DB2 @ 12.1.0.69214]* — the latch's home ground | cue **E**'s Avenger's Shield half (`!aura(vanguard)`), and the readable gate on `as_guidance_capped` |
| Whether **Blessed Assurance** is up | **readable** | R2's alert edges → the `aura` latch | `433015`, Category-2 in set 637, OrderIndex 39 *[T1 DB2]* | cue **F** |
| **Whether any Divine Guidance stack exists at all** | **readable** | R2's alert edges → the `aura` latch | `433106`, Category-2 in set 637, OrderIndex 40 *[T1 DB2]*. ⚠ This is the latch's **boolean** — *is there one* — and is a categorically different fact from the count two rows below | **Nothing, since 2026-08-23.** `cons_no_guidance` read it and was deleted for density (`catalog.md` → *Defeats* 7). The state it covered — no aura at all, so no button and no sink — is now **uncovered**: on a Blessed Assurance build Consecration is not eliminated while Hammer of Wrath is armed |
| Whether **Shining Light** is up | **readable** | R2's alert edges → the `aura` latch | `321136`, Category-2 in set 637, OrderIndex 30 *[T1 DB2]* | cue **G** (`!aura(shining_light)`) — the whole of Word of Glory's treatment |
| Whether **Righteous Protector** is taken | **readable** | the `talent` predicate | node `81477` / entry `102440`, spec 11,21 (`ability-inventory.tsv` @ 12.1.0.69214, node + entry read directly). ⚠ the `C_Traits` call shape is `[gap]` — Havoc's *Open facts* 7 | cue **H**, which withholds cue **B** |
| Whether **Divine Guidance** is taken | **readable** | the `talent` predicate | node `95235` / entry `117884`, Lightsmith hero 8,11 — a **choice node** shared with Blessed Assurance | the readable gate on **both** sealed count tables |
| Whether **Blessed Assurance** is taken | **readable** | the `talent` predicate | node `95235` / entry `117883`, the other half of the same choice node | cue **F**'s belt-and-braces gate (the aura could not exist on a Divine Guidance build, so the latch would withhold anyway; the gate makes the reason legible) |
| **Holy Power current value** | **readable, and deliberately unread** | R3 | one of the seven never-secret secondaries (`security-…` §4.12); Retribution declares `power = "HolyPower"` on it | **nothing.** The 12.1 `actions.default` contains no `holy_power` term of any kind, so the catalog declares no `power` field and authors no `resource` term — the first catalog of any spec whose primary resource is readable and goes unread |
| `prev_gcd.1.divine_toll` | **readable in principle** | R10 | the press ring is readable; the confirmed-cast ring is not (`cdm-rider-patterns.md` §9.2) | **nothing.** It is the last disjunct of rung 9, which is trivially true on Lightsmith — see the next row |
| Whether rung 9 has a press gate at all | **not a read — a derivation** | — | every term in rung 9's condition is Templar's (`buff.hammer_of_light_ready`, `buff.undisputed_ruling`, `buff.hammer_of_light_free`). With no Hammer of Light on the build the first disjunct is permanently true | the placement of Shield of the Righteous at position 3 by **position alone**. State it as a derivation, not a reading |
| **Divine Toll's cooldown remaining** | **sealed-display** | S4 → `sealed-cooldown-range` | `C_Spell.GetSpellCooldown` is `SecretWhenCooldownsRestricted`; the duration object carries the secrecy (`cdm-rider-patterns.md` §2.2) | cue **A** (`beyond = 10`), gated on `ready(avenging_wrath)`. **Not a condition** |
| **Avenging Wrath's cooldown remaining** | **sealed-display** | S4 → `sealed-cooldown-range`, twice, in opposite senses | as above | cue **B** (`within = 30`, on Divine Toll) and cue **D** (`beyond = 5`, on Holy Armaments). Different entries, so no union. **Not a condition** |
| **Divine Guidance's application count** | **sealed-display** | S7 + S11 → `sealed-count-bands` (V16) | the managed AuraContainer owns the display; a tainted-created `NumericRuleFormatter` is honoured `[client 2026-08-21]` and a band's `format` may carry a texture escape (`security-…` §3.5, §3.5.2, §3.5.3) | `as_guidance_capped` on **Avenger's Shield** — rung 15 read as an elimination of the row it outranks. **Not a condition** |
| **Divine Guidance's application count**, the complement | **sealed-display** | S7 + S11 → `sealed-count-bands` (V17) | as above | `cons_awaits_hammer` on Consecration, under four readable gates. **Not a condition** |
| `buff.avenging_wrath.up` | **open** | the `aura` latch, unmeasured on this row class | `31884`'s buff is a Category-**3** (TrackedBar) row in set 637, OrderIndex 27 *[T1 DB2 @ 12.1.0.69214]*; the latch is built on TrackedBuff `OnAuraApplied` / `OnAuraRemoved` edges and no measurement covers TrackedBar (`cooldown-manager.md` §5.1) | rung 7's **first** disjunct. **Not authored.** `catalog.md` → *Defeats*, item 1; §5.2 @verify-ingame |
| `!consecration.up` — the ground effect | **sealed-display** on a Blessed Assurance build; **open** on a Divine Guidance one | a V16 **presence** band on the player aura `188370` | `188370` is the *"Standing in Consecration"* buff — three `Effect=6` rows at `ImplicitTarget=1` (caster), and *Strength of Conviction* `379008` triggers exactly it *[T1 DB2 @ 12.1.0.69214]*. `26573` is the cast (the 12 s field and the Category-3 row), `81297` the periodic damage, `204242` the enemy snare. It holds **no** CDM row and needs none — a sealed container is cap's own frame. ⚠ `Duration = -1`, so it is present/absent only | `cons_field_up`. **Gated on `talent(blessed_assurance)`**, because rung 15 carries no `!consecration.up` term and its count is sealed. *Defeats*, item 2, narrowed — and it **no longer shares a blocker with item 1** |
| Which way round the **Sacred Weapon** identity reads | **open** | R7 supplies the read; the mapping is unverified | the exhaustive absence establishes *that* there is a transform and says nothing about which of `base` / `transformed` is which armament | cue **D**'s gate reads `identity(holy_armaments) == base`. §5.1 @verify-ingame |
| `!buff.sacred_weapon.up` | **sealed-display** | the V19 pair's own absence | no matching aura yields no button and no sink, so the row draws nothing and is a live candidate. ⚠ It needs **no** Category-2 row, and the census question this was filed under was the wrong question: a **latch** needs a row, a **display** does not | rung 10's second half. Authored, as `ha_weapon_healthy`. *Defeats*, item 3, **closed** |
| `buff.sacred_weapon.remains < 6` | **sealed-display** | `sealed-pandemic`'s `outside_s` (V19) → `SetDurationText` breakpoints | the band shipped **2026-08-24** and this is its first consumer anywhere. The buff is `432502` — the only "Sacred Weapon" id with `Effect=6` aura rows (five, `ImplicitTarget=21`, including `EffectAura=468` → *Tempered in Battle*), `Duration = 20000` *[T1 DB2 @ 12.1.0.69214]*. `6` is the APL's own number and 30 % of 20 s, so the catalog's hatch edge and the client's window edge very nearly coincide — the **seam** is the residue | rung 10's first half. Authored. *Defeats*, item 3, **closed**; the seam is @verify-ingame |
| **Whether Holy Armaments is AT max charges** | **readable** | `capped` (R6) — `Sense.readCapped` | ⚠ **It needs no `charged` and no authored count.** `C_Spell.GetSpellCharges` is called on the live id every tick, `maxCharges` is read off the **client**, and the read returns UNKNOWN — never `false` — at `maxCharges <= 1` or on refusal; `Track.lua` records that `capped` deliberately bypasses the charge ledger. The old row here said this fact was absent from Tier-1 data, which was looking in the wrong place | rung 23's charge half. **Available and deliberately unspent**: rung 23 sits below three rows to this one's right, so neither releasing cue **D** on it nor badging the row is honest. *Defeats*, item 4, rewritten; §5.4 |
| **Judgment's recharge REMAINING** | **not readable, and not the same fact as `capped`** | — | rung 17 is `full_recharge_time<=gcd*2` — *about to cap* — where `capped` answers *already at max*. Nothing readable carries a recharge remaining. ⚠ The talent-conditional count is **not** a blocker: without **Crusader's Judgment `204023`** `maxCharges` is 1 and `readCapped` self-withholds, which is the conditional behaviour `charged` could not have | rung 17. **Not authored**, and expressing it would also mean **promoting** Judgment past two rows to its left, whose rank turns on the sealed Divine Guidance count. *Defeats*, item 5, rewritten |
| Charge counts for **Shield of the Righteous** and **Crusader Strike** | **open** | — | neither carries a Tier-1 charge count in this repo | nothing — the APL puts no charge term on either, so the ⚠ in the Charges column is a refusal to invent a number rather than a lost rung |
| Target health / execute range | **not expressible, and not needed** | — | subsumed by the Hammer of Wrath override: **the button's existence is the gate**, so the identity read answers a target-health question with no target-health vocabulary | nothing. The same call Retribution makes |
| `apex.3` | **not modelled** | — | not a talent, not a buff; absent from `talents.json`, `ability-inventory.tsv` and the whole repo. A **sim-side Apex rank** — simulation state, not a player fact, exactly as Retribution treats `raid_event.adds` | rung 13's second disjunct. The `buff.vanguard.up` half of the same rung is authored. *Defeats*, item 6 |
| `active_enemies` / target count | **not modelled** | — | Protection's target-count decision is the Blessed Hammer / Hammer of the Righteous **choice node**, made in the talent tree and not per pull; the two hammer rungs are gated on Blessed Assurance, not on enemy count | nothing. There is nothing for `/cap aoe` to switch, so **no row wears `aoe_only` or `st_only`** and `aoe` is never named — the first catalog where the toggle has no subject |

**Lane counts, over 31 rows.** **14 readable** (two of them consumed by nothing) plus one row that
is a *derivation* rather than a read; **4 sealed-display**, plus one sealed fact with **no authored
form** (the aura-remaining band); **7 open**; **2 not expressible**; **2 not modelled**.

**The shape of that distribution is the catalog.** Every readable fact is a boolean or an identity
— there is not one readable *number* in the list, because the 12.1 priority list contains no
resource term, no target-count term and no charge term that survives. And seven open facts is the
most of any catalog so far, of which **five are one measurement each** and two share one (§5.2).

---

## 3. The three transforms, in full — and they are not equally established

`../authoring.md`'s recipe index R7 is the whole of the readable side; what differs between the
three is the argument that the transform **exists at all**, and that argument comes from game data
in two cases and from a Tier-2 prose claim in the third.

The structural spine is one measurement, made across the whole `CooldownSetSpell` file at
12.1.0.69214: **four of Protection's pressed buttons hold zero rows anywhere, in any set, for any
spec.** A spell with no row of its own cannot reach the Cooldown Manager except as an override on
a row that has one. That is an exhaustive absence, and it is Tier 1.

| Transform | Established by | Confidence |
| --- | --- | --- |
| Holy Bulwark `432459` → **Sacred Weapon `432472`** | `432472` holds **zero** `CooldownSetSpell` rows anywhere in the file, and the only candidate row is Holy Bulwark's (637 / cat0 / ord 23) — the same button in the game's own terms: one talent, alternating charges *[T1 DB2: `CooldownSet` / `CooldownSetSpell` @ 12.1.0.69214]* | **Tier 1** for the transform's existence. ⚠ **Tier 0 for its DIRECTION** — marked, §5.1 @verify-ingame |
| Crusader Strike `35395` → **Hammer of the Righteous `53595`** / **Blessed Hammer `204019`** | both hold **zero** rows anywhere *[T1 DB2 @ 12.1.0.69214]*, both are a spec **choice node** (3,19), and the APL never names Crusader Strike at all | **Tier 1**, and see below — it is a *replacement*, not a live transform |
| Judgment `275779` → **Hammer of Wrath `24275`** | `24275` holds zero rows anywhere *[T1 DB2]* — but the **pairing** comes from `knowledge/classes/paladin/protection/abilities.md:62`, *"Hammer of Wrath is no longer its own button — it is now a transform of Judgment"*, which itself carries an `@verify-ingame` and sits in a file whose front matter reads **patch 12.0.7** | ⚠ **Tier 2 — marked** @verify-ingame |

### Sacred Weapon is the strongest structural claim here, and the direction is still open

This is the same call Demonology made for Ruination, and the evidence is a different *kind*.
Ruination rested on Tier-2 log behaviour because its Tier-1 tooltip was written for the wrong spec;
this rests on a Tier-1 exhaustive absence. **An absence is stronger about *whether* and says
nothing about *which way round*.** The catalog authors `identity(holy_armaments) == base` as cue
D's gate, and if `base` turns out to name Sacred Weapon rather than Holy Bulwark, the hold lands on
exactly the wrong life of the button: the Sacred Weapon life, whose rung is **10** and whose
correct press is *now*. That is a wrong hint, not a missing one, which is why it is the first entry
in §5.

### The Crusader Strike pair is a permanent replacement, and the distinction matters

Hammer of the Righteous and Blessed Hammer are a **choice node**: exactly one exists on any build,
from the moment the build is chosen, and it never changes mid-combat. So `identity` on that row
reads `transformed` on **every** build, permanently — which is why the row **declares no band on
`identity`** even though it is a transform. A band would encode a distinction that never varies
within a session.

**This is the opposite end of the same axis as Demonology's Grimoire `alt` field.** There, an
override that is a *build fact* was declared statically so the catalog could name the button the
player actually has; here, the build fact is already carried by the row's own live override, and
the catalog's job is to *not* spend vocabulary on it. Compare an R7 transform proper — Sacred
Weapon, Hammer of Wrath — where the override flips inside a pull and the identity read is the whole
signal. **A permanent replacement is a naming problem; a live transform is a state problem.**
Reading the first as the second is how a catalog grows a two-band entry whose second band never
fires. Retribution's Final Verdict is the same shape and is handled the same way.

### Two specs now rest on one unverified claim

The Hammer of Wrath pairing is the load-bearing Tier-2 fact in this catalog, and **the Retribution
catalog authors the same pairing on the same single source**. That is worth stating plainly rather
than marking twice: it is not two independent Tier-2 claims that might corroborate each other, it
is **one sentence in one 12.0.7 file, cited by two catalogs**. One in-game observation retires the
marker in both. Failure direction if the pairing is wrong: cue **E** never fires (Avenger's Shield
and Consecration stop yielding — a missed skip), and cue **F**'s `identity(judgment) == base` gate
is permanently true, so Judgment could stand itself down in the one state where it is the press.
§5.3.

---

## 4. The sealed displays, and why they are in the safety case at all

**Eight sealed values on six sinks.** Three `sealed-cooldown-range` curves (cues **A**, **B**,
**D**), three `sealed-count-bands` tables — two on Divine Guidance's count (`as_guidance_capped` on
Avenger's Shield, `cons_awaits_hammer` on Consecration) and one **presence** band on the
Consecration player aura (`cons_field_up`) — and one `sealed-pandemic` **pair** on the Sacred
Weapon buff (`ha_weapon_healthy`), which is two sinks and two facts under one marker. They are in
this file because they are the one place a reader might reasonably suspect a branch, and they are
not one:

- **A band table is a rule, not a comparison.** cap builds a list of `{ threshold, format }` out of
  whole numbers it authored and hands it to a `NumericRuleFormatter`. The client calls
  `FormatNumber(applications)` and `SetText`. cap never receives the count, never compares it, and
  never learns which band fired. `FormatNumber` is documented `ConstSecretAccessor` precisely so the
  client may do this on cap's behalf.
- **A range curve is the same shape on a duration.** cap authors a number of seconds and a sense;
  the client evaluates the step curve against a sealed remaining-duration and drives a texture's
  visibility. `within` and `beyond` are the same curve read at a different point, and in both a
  dependency that is **ready** reads nothing — which is not a caveat here but the correct
  behaviour: a ready Divine Toll must not hold Avenging Wrath.
- **The managed AuraContainer owns the whole display.** cap registers a slot with
  `candidateFilters.includeSpellIDs = { [auraSpellID] = true }`, styles it inside `initializeFrame`,
  and never touches the subtree again — a **forbidden object** after that window, for reads as well
  as writes.
- **A duration band is the count table's shape on seconds.** `outside_s` builds
  `{ threshold 0 → blank, threshold 6 → the gold hatch }` and hands it to `SetDurationText`; the
  client compares the aura's remaining seconds and writes a FontString. Cap authors `6` and reads
  nothing. **This is the one number in the catalog authored against a duration rather than a
  count**, and it is not an exception to the boundary — no Lua branch anywhere depends on those
  seconds.
- **The pandemic region is the one sealed display with no authored threshold at all.** The client
  computes `GetRefreshExtendedDuration − GetAuraBaseDuration` per spell and calls `SetShown` on a
  Region cap registered. There is nothing here to get wrong, which is exactly what makes it good.
- cap reports `offered` / `armed` / `refused` and never `drew`. **Accepted is not drawn**
  (`../authoring.md` → *Accepted is not drawn*) — whether any of it ever appears is an eyeball, not
  a capture.

⚠ **The sense of a range curve is a correctness fact, not a styling one.** Cue A's `beyond = 10` is
the *complement* of rung 5's `cooldown.divine_toll.remains<=10`. `within = 10` would hold Avenging
Wrath in the one window the APL presses it — a confident, permanent, exactly-wrong badge. There is
no runtime signal that would catch it, because cap never learns which side of the curve the value
fell on. **An authored threshold is a thing to get wrong**, and the two count tables carry the same
exposure at the breakpoint: `threshold` is the *minimum* input a rule applies to, so a value **on**
it takes the upper band.

### The two count tables, which are the new thing

⚠ **One of them rules out a row the aura does not belong to, and that had never shipped.**
Demonology's two count tables both sat on the row whose own press the count gated — Power Siphon's
Cores, Implosion's imps. Here the count belongs to **Divine Guidance**, the entry is **Avenger's
Shield**, and the statement is *"the row to your right outranks this one right now."*

The mechanism needs nothing new: `Channel.Plan` has always bound `display.ability` independently of
`entry.ability`, and the sink is an AuraContainer slot on **this entry's own button** filtered to
that aura. What is new is the *statement*: `../spec.md` §3.1's readable-relationship rule reaching a
fact cap may not read. **Nothing about the boundary moves** — the relationship is expressed by
where cap *puts* the sink, which is ordinary readable logic, and the value that decides whether it
paints is still evaluated entirely inside the client.

⚠ **The two tables run in opposite directions and both are honest, for different reasons.**

- **V16 on Avenger's Shield** — silent below five, hatch plus a negative mark at five. Drawn the
  other way it would say *"Avenger's Shield is ruled out until Divine Guidance is capped"*, which is
  false: rung 18 is the ordinary press for the whole rest of the fight. A complement is only correct
  where the **low band is a real elimination**, and here the low band is the resting state.
- **V17 on Consecration** — hatch plus a negative mark below five, nothing at five. This *is* the
  complement, and Demonology's warning says a complement on a rising count is usually a lie. What
  makes it true is its **readable gate**: under `identity(judgment) == transformed` **and**
  `ready(judgment)`, rung 16 outranks rung 19, so only rung 15 could put Consecration back on top —
  and below five, rung 15 is false. Under that gate both bands are exactly right. Outside it the
  client is never asked to paint anything.

**A readable gate can turn a dishonest complement into an honest one.** That is the design finding
of this pass and it belongs in the safety case rather than only in the roster, because the
alternative reading — *complements are unsafe on rising counts* — would have closed the route for
every future catalog.

### The two displays with no Cooldown-Manager row, and the asymmetry they expose

**`ha_weapon_healthy` (V19) and `cons_field_up` (V16) both name a subject the Cooldown Manager does
not carry**, and neither needs one. `Channel.Arm` builds an `AuraContainer` on **cap's own frame**,
filters it with `candidateFilters.includeSpellIDs`, chooses HELPFUL or HARMFUL from `plan.unit` and
binds it with `container:SetUnit(plan.unit)`. Nothing in that path consults a Cooldown-Manager row.
A **latch** needs a row, because it rides that row's alert edges; a **display** does not.

⚠ **That line is why one defeat closed and another did not, and it is the general statement worth
carrying.** `cons_field_up` says *the Consecration field is under you* — an aura's **presence** —
which a container filtered to that aura draws by **existing**. Divine Toll's hold wants
*Avenging Wrath's buff is not up* — an aura's **absence** — and a sealed display can never say
that: absence draws **nothing**, and nothing is indistinguishable from a client refusal, a wrong
id, or a display that was never armed. **A sealed display may assert an aura's presence and may
never assert its absence.** Absence has to enter a Lua condition, which is the `aura` latch, which
is §5.2's unmeasured alert edge.

⚠ **V19 is the one sealed display in this catalog with no authored threshold on one of its halves.**
The badge rides Blizzard's own `GetRefreshExtendedDuration − GetAuraBaseDuration`, computed per
spell, so there is nothing there to get wrong. The **other** half is the catalog's number —
`outside_s = 6`, compared by the client against the aura's remaining seconds — and the two edges
are different facts about one aura. Six seconds is 30 % of the buff's 20 s, so they should very
nearly coincide; *"very nearly"* is a flight observation and is marked as one.

⚠ **`188370` allows nothing but a presence band.** `Duration = -1` means the player buff carries no
remaining time at all, so V19 and V20 are structurally impossible on it and the 12 s clock belongs
to the cast `26573`. This is a game fact constraining the design, not a shelf gap.

### A readable gate licenses a paint without contributing a cue

`as_guidance_capped`'s gates are `!aura(vanguard)`, `talent(divine_guidance)`,
`ready(avengers_shield)` and `ready(consecration)`. **None of them draws anything.** They decide whether the sealed display is
offered at all, and they carry no cue key, no badge and no slot of their own. That is the
`when`-beside-`display` shape (armed 2026-08-22), and it is worth naming here because it is the one
place in the file where **readable logic is load-bearing for a sealed display's correctness**:
without the Vanguard term the hatch would rule out Avenger's Shield in the one state where rung 13
puts it first, and without `ready(consecration)` it would rule it out in every state where rung 15's
own button is swiped and rung 18 is therefore the press. `../spec.md` §3.6's rule is the licence — *one secret per curve; readable gates
without limit* — and the practical consequence is its diagnosis: a graded cue that fires too
eagerly is usually missing a readable gate, not a better curve.

⚠ **A band cannot rule out a row whose subject does not exist, and that state is now UNCOVERED.**
With no Divine Guidance aura there is no aura button, so no sink on it draws anything. Until
2026-08-23 the readable `aura` latch (`cons_no_guidance`) covered it — a **different fact answering
a different question**, *is the subject present* rather than *how many*. `scenarios.md` deleted that
marker for density (`catalog.md` → *Defeats* 7): it was the common term of both overflowing trios,
and it was the only marker in the catalog that converted a free client-drawn elimination into a
budgeted one. **What that costs is a real hole and belongs in this file rather than only in the
walk:** on a Blessed Assurance build, and for one global after a five-stack Consecration on a Divine
Guidance build, Consecration is not eliminated while Hammer of Wrath is armed, so the walk presses
rung 19 where the priority is at rung 16. The hole is a **throughput loss, never a wrong button**,
and a readable substitute for the count closes it and restores the marker for free.

⚠ **What did NOT happen is a weaker-fact substitution.** Substituting `aura(divine_guidance)` — *is
there one* — for the count would be exactly that, and the catalog does not do it. It dropped the
hint rather than drawing a cheaper one, which is §3.6's rule for an open fact applied to a fact that
is merely out of budget.

⚠ **`cons_field_up` is gated the same way and for the same class of reason** (2026-08-26). Rung 15,
`consecration,if=buff.divine_guidance.stack>=5`, carries **no** `!consecration.up` term — so on a
Divine Guidance build a capped count presses Consecration with the field still under the player,
and a presence band drawn there would eliminate the correct button. Cap may not compare that count,
so the display is gated to the other half of choice node `95235` with `talent(blessed_assurance)`.
Read **positively** rather than as `!talent(divine_guidance)` deliberately: identical coverage, one
fewer negation in §6's count, and the mutual exclusion with `cons_awaits_hammer` becomes a property
of the node rather than of an argument. `ready(crusader_strike)` is beside it as the outranker term,
because rung 29 is an unconditional Consecration and with the rest of the row unavailable a
field-up Consecration **is** the press.

---

## 5. The open facts, routed

Each becomes an `@verify-ingame` marker on the claim (`../authoring.md` stage 5). **An unknown is
recorded as a marker on the claim, never as a line in a tool and never as a TODO here.** A
load-bearing open fact is a stop-and-ask (`../spec.md` §3.6).

⚠ **Every marker below is `@verify-ingame` and none is `@pending-test`.** No ClientLab test exists
for any of these; `@pending-test: <id>` asserts that one does, and writing it would be a false
claim (`projects/addon-lab/docs/lab-process.md`).

**One of the four can cause a wrong hint rather than a missing one** — 5.1 — and it is first for
that reason. The other three cost a hint and none of them causes a wrong one.
⚠ **§5.1's stake DOUBLED on 2026-08-26.** Two treatments now hang on the direction of the Sacred
Weapon identity rather than one: cue **D** gates on the Bulwark life, `ha_weapon_healthy` on the
Sacred Weapon life. If the polarity is inverted, **both** land on the wrong life at once. Same
single observation, twice the value and twice the exposure.
⚠ **§5.5 was retired on the same date** — the question it asked (does Sacred Weapon's buff hold a
Category-2 row?) was the wrong question. A **latch** needs a Cooldown-Manager row; a **display**
does not, because a sealed container is cap's own frame. Its subject is now settled Tier-1 game
data instead: `432502`, with **zero** `CooldownSetSpell` rows anywhere
`[searched 2026-08-26: whole file, exact SpellID match @ 12.1.0.69214]`, which **agrees** with
§5.1's finding rather than contradicting it.

### 5.1 The direction of the Sacred Weapon identity

**What is unknown:** whether `identity(holy_armaments) == base` means *the row is displaying Holy
Bulwark* or *the row is displaying Sacred Weapon*. The transform's **existence** is Tier 1 (§3); its
polarity is not.

**What it blocks:** nothing — cue **D** ships. That is precisely the exposure. If the polarity is
inverted, cue D's hold lands on the Sacred Weapon life, where rung 10 wants the press *now*, and
the Holy Bulwark life carries nothing where the bank is wanted. Both halves fail together and the
badge looks confident throughout.

**What would settle it:** one observation — with the next armament being Holy Bulwark, does row 4's
`overrideSpellID` differ from `432459`? A single reading of the live row answers it, and it is
cheap because the row is on screen for the whole fight. @verify-ingame

### 5.2 Does a Category-3 (TrackedBar) row raise the alert edges?

**What is unknown:** whether a Category-3 (TrackedBar) Cooldown-Manager row raises the `aura`
latch's `OnAuraApplied` / `OnAuraRemoved` edges. The latch is built on TrackedBuff edges and no
measurement in `knowledge/addon-dev/` covers TrackedBar (`cooldown-manager.md` §5.1)
`[searched 2026-08-23: CooldownSetSpell @ 12.1.0.69214, Track.lua's edge table, cdm-rider-patterns.md §6]`.

**What it blocks, here:** `buff.avenging_wrath.up` — Avenging Wrath's buff is Category-3 in set
637, OrderIndex 27 — is rung 7's first disjunct, so **Divine Toll wears nothing on a Righteous
Protector build**, which is the build almost everyone plays (*Defeats*, item 1).

⚠ **It no longer blocks `!consecration.up`, and the claim that both close together was WRONG**
(corrected 2026-08-26). They were filed as one because both facts live on a Category-3 row, but
they are different *kinds* of need and only one of them is a latch question:

- **`!consecration.up` needs PRESENCE** — *the field is under you, so do not press this* — and a
  sealed container draws presence by **existing**. `cons_field_up` arms an `AuraContainer` on the
  player aura `188370`, which holds no Cooldown-Manager row at all, and no alert edge is consulted
  anywhere in that path. The measurement is **bypassed**, not made.
- **`buff.avenging_wrath.up` needs ABSENCE** — *the buff is not up, so Divine Toll waits* — and a
  sealed display can never say that. Absence draws **nothing**, and nothing is indistinguishable
  from a client refusal, a wrong id, or a display that was never armed. Absence has to enter a
  **Lua condition**, which is the `aura` latch, which is this measurement.

**So item 2 is narrowed by a display and item 1 stands, whole.** The asymmetry is the finding, and
it generalises: *a sealed display may assert an aura's presence and may never assert its absence.*

⚠ **This is the SAME unmeasured fact as Demonology's Defeat 5** (Dominion of Argus `1276166`,
Category-3 in set 60, OrderIndex 50 — that spec's `fact-classification.md` §5.4). Different aura,
different spec, identical question. **One measurement closes it for both specs**, which is worth
knowing because it changes the cost calculus: this is not a Protection errand, it is a platform
measurement two catalogs are already waiting on, and a third will want it.

**Why it is not authored anyway:** a latch built on an edge that may never fire is a hold that may
never release — a confident badge that is wrong for the whole fight. Silence is the correct failure.

**What would settle it:** enable a Category-3 row, apply and drop the aura, and watch whether the
latch transitions. If it does, `aura(avenging_wrath)` becomes a readable boolean, cue **B** is
replaced by a marker correct on **both** builds, and the talent gate **H** is deleted with it.
@verify-ingame

### 5.3 Hammer of Wrath riding Judgment

**What is unknown:** the pairing itself. Tier 2, from
`knowledge/classes/paladin/protection/abilities.md:62`, which carries its own `@verify-ingame` and
describes 12.0.7 (§3).

**What it blocks:** nothing today — cues **E** and **F** both ship on it. If the pairing is wrong,
`identity(judgment)` never reads `transformed`, cue E stops firing on Avenger's Shield and
Consecration (a missed skip on two rows), and cue F's base-life gate is permanently true. The
game-data half — that `24275` has no row of its own and *must* ride something — is Tier 1 and
survives either way; only the choice of host is at risk.

⚠ **Two specs rest on this one claim.** Retribution's catalog authors the same pairing from the same
sentence. Measuring it once retires both markers; measuring it twice is the waste.

**What would settle it:** during Avenging Wrath, or against a sub-execute target, read the Judgment
row's `overrideSpellID`. @verify-ingame

### 5.4 Holy Armaments' charge count — RETIRED as an open fact, 2026-08-26

**It was never open.** This section said the `capped` cue had no subject in this catalog because no
row declares `charged` and no Tier-1 charge count for Holy Armaments exists. **`capped` does not
consult `charged`.** `Sense.readCapped` calls `C_Spell.GetSpellCharges` on the **live** id every
tick, reads `maxCharges` off the client, and returns UNKNOWN — never `false` — at
`maxCharges <= 1` or on any refusal; `Track.lua` records that it deliberately bypasses the charge
ledger, because a napkin count cannot survive an override flip. `charged` is a declaration about
**readiness tracking** (`Sense.seedBaseline`) and about nothing else. So the number this file said
had to be measured is a number the **client** owns, and a one-charge row self-withholds instead of
lying.

**What that changes, and what it does not.** `capped(holy_armaments)` is readable today, so the
`capped` **cue** has a subject and the *"no subject"* half of `catalog.md`'s positive-cue argument
is deleted. **The conclusion survives on a different ground**: rung 23
(`holy_armaments,if=next_armament=holy_bulwark&charges=2`) sits **below** rungs 15, 16, 18 and
20–22 while Holy Armaments is **position 4**, so at two banked charges the press is usually
Avenger's Shield at rung 18. A positive cue is a **promotion**, judged by pass 1 against every row
to its left — badging this row would promote one the priority does not press. And releasing cue
**D** on `!capped` fails for the same reason from the other side: the row becomes leftmost-clean
where the APL is at rung 18 (`scenarios.md` → *PROT-20*).

⚠ **The honest residue is `catalog.md` → *Defeats*, item 4**, whose blocker is now the **row order**
plus the absence of an OR in the marker grammar — neither a measurement nor a client question.
A seven-term positive `capped` marker gated on all three outrankers being unavailable *is*
expressible with today's vocabulary; it is left unauthored as an author's call.

⚠ **The same correction retires §5.5's premise and half of Defeat 5's.** Judgment's
talent-conditional charge count needed a *"talent-conditional `charged`"* that does not exist —
and does not need to: without **Crusader's Judgment `204023`** `maxCharges` is 1 and `readCapped`
self-withholds, which is exactly the conditional behaviour. What still blocks rung 17 is that
`capped` is the **wrong fact** for it (*already at max* versus *two globals from full*) and that
expressing it would require a promotion whose gate is a sealed comparison.

### 5.5 Whether Sacred Weapon's buff holds a Category-2 row — RETIRED as the WRONG QUESTION, 2026-08-26

**The census answer is settled and it is "no rows at all".** An exact-`SpellID` filter of
`CooldownSetSpell` over `{432472, 432502, 432616, 432757, 441590}` returns **zero rows**
`[searched 2026-08-26: whole file, exact column match @ 12.1.0.69214]` — the Protection set 637
carries `432459` Holy Bulwark and nothing else from the armament pair. That **agrees with** §5.1's
finding that Sacred Weapon reaches the Cooldown Manager only as an override on the Bulwark row; it
does not contradict it, and nothing needs correcting there.

**And the row was never needed.** A Cooldown-Manager row is what the `aura` **latch** requires,
because the latch rides that row's alert edges. A **sealed display** requires none: `Channel.Arm`
builds an `AuraContainer` on cap's own overlay, filters it with `includeSpellIDs`, chooses the
filter from `plan.unit` and binds it with `SetUnit(plan.unit)`. So `ha_weapon_healthy` arms on the
buff `432502` with no row anywhere, and rung 10's `!buff.sacred_weapon.up` half is expressed by the
display's **own absence** — no aura, no button, no sink, so the row draws nothing and is a live
candidate. Demonology's `ib_art_clock` is the shipped precedent for the shape.

**What is left is not this question.** The residue on rung 10 is the **seam** between the catalog's
`outside_s = 6` and Blizzard's own per-spell refresh window — two different facts about one aura,
expected to very nearly coincide at 30 % of a 20 s buff, and only watchable in a flight.
@verify-ingame

---

## 6. Unknown never becomes confidence

Every predicate above returns **UNKNOWN** rather than `false` when the client refuses it, and every
marker withholds on UNKNOWN. `Signal`'s unknown-safe evaluation is what makes a **negated** readable
term safe to author at all — and this catalog is unusually exposed there, because **its readable
vocabulary is almost entirely negative**.

⚠ **Load-bearing three times over, and every instance is a negation.** The catalog's contract
boundary names them:

1. **Cue G is nothing but a negation.** `!aura(shining_light)` is the *whole* of Word of Glory's
   treatment. If the Shining Light row is unbound — a player who never enabled that tracked buff in
   their Cooldown Manager — the latch has no `cooldownID`, nothing is ever written for it, and
   `World` reports UNKNOWN (`Track.lua`; the latch has **no third supplier and no timeout**). Were
   UNKNOWN to read as `false`, `!false` would be true and Word of Glory would wear `blocked` for the
   entire fight, including in the one state the APL presses it.
2. **Cue E's Avenger's Shield half turns on `!aura(vanguard)`.** An unbound Glory of the Vanguard
   row would, under a false-for-unknown reading, make the Hammer of Wrath yield fire even while rung
   13 puts Avenger's Shield first — a held press in the exact state the term exists to carve out.
3. **Cue H is `!talent(righteous_protector)`.** The `C_Traits` call shape is itself `[gap]`
   (Havoc's *Open facts* 7), so a refused read here is not hypothetical. False-for-unknown would
   arm cue **B** on a Righteous Protector build, where Avenging Wrath's cooldown is halved and a
   30-second band covers half the cycle — a hold the priority does not contain, drawn confidently.

⚠ **The 2026-08-26 pass added no fourth.** `ha_weapon_healthy` and `cons_field_up` between them
name `identity(holy_armaments, "transformed")`, `ready(holy_armaments)`, `talent(blessed_assurance)`,
`ready(consecration)` and `ready(crusader_strike)` — **every one of them positive**. The
`talent(blessed_assurance)` gate was chosen over the equivalent `!talent(divine_guidance)` partly
for that reason: identical coverage, one fewer negation to defend.

⚠ **There was a fourth until 2026-08-23 and it is gone.** `cons_no_guidance` was
`!aura(divine_guidance)` and read the same way. It was deleted for density, not because the
unknown-safety argument failed — so a reader counting negations on the `aura` and `talent` latches
should find **three**, and the deleted fourth is recorded here only so that restoring the marker
restores its entry rather than rediscovering it.

**And cue C is a negation of a different predicate.** `!affordable(shield_of_the_righteous)` reads
`C_Spell.IsSpellUsable`'s second return, and R1's own trap applies: *"0 charges" from
`IsSpellUsable` is not a fact* — it is unusable for many reasons and a refused read leaves the
answer genuinely unknown. The marker withholds; it does not assert affordability either way.

**Why a refused read must not flip a negation true.** A positive marker that goes dark on UNKNOWN
costs a hint the player did not have anyway. A **negative** marker that lights on UNKNOWN *adds* a
statement the player did not have, and the statement is *"do not press this"* — the one thing a
combat-assistance overlay must never say wrongly. The asymmetry is the whole argument: an absent
badge is silence, and silence is always survivable; a badge drawn from nothing is a hint that
outranks the player's own judgment while resting on none. Because this catalog's vocabulary is
**negative by default** — `blocked` and `starved` are the only two cue keys it spends
(`../render-shelf.md` V5.1) — the unknown-safe path is not one guard among many here. It is the
condition under which the catalog is safe at all.

⚠ **The enablement question is therefore a correctness requirement wherever a latch is authored.**
Four `aura` latches ship in this catalog, three of them read in negation. `rows ≤ set` is the only
bound the Cooldown Manager gives us — a player lays out whichever rows they chose — so an unbound
row is the ordinary case, not the edge case, and every one of these markers must be correct in it.

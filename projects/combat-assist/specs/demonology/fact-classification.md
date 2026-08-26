---
title: Demonology Warlock — fact classification
spec: Demonology Warlock (Diabolist) — specID 266, hero tree 59, Midnight 12.1
---

# Demonology Warlock (Diabolist) — fact classification

**What this file is for.** The **safety case**: every fact this catalog consumes, sorted readable / sealed-display / open, with its recipe and its evidence. It is separate so it can be read without reading the roster — the question *"does anything here branch on a sealed value?"* must be answerable on its own.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/warlock/demonology/simc-apl.md` (Tier 1,
generated, commit `51d49d5`), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## 1. The answer, first

**No sealed fact appears in any Lua condition, in either polarity.** The catalog reads **six**
sealed values, drawn through **eight** sinks, and every one of them goes straight to a
client-owned surface:

| Sealed value | Sink | Where |
| --- | --- | --- |
| Summon Demonic Tyrant's cooldown *remaining* | `sealed-cooldown-range`, `within = 5` | cue **F**, on Hand of Gul'dan |
| Summon Demonic Tyrant's cooldown *remaining* | `sealed-cooldown-range`, **two-sided** `beyond = 10.5` / `within = 21.5` | cue **J**, on Call Dreadstalkers |
| Demonic Core application count | `sealed-count-bands`, two breakpoints | Power Siphon |
| Wild Imp application count | `sealed-count-bands`, two breakpoints (the complement) | Implosion |
| Demonic Core application count | `sealed-count-bar`, `max = 4` | Demonbolt |
| Demonic Core's own remaining | `sealed-proc-bar` | Demonbolt |
| Doom's pandemic window | `sealed-pandemic` — **the client's own predicate** | Demonbolt |
| Demonic Art (Mother of Chaos) remaining | `sealed-proc-bar` | Shadow Bolt / Infernal Bolt |

Every other term in every marker is `ready`, `affordable`, `identity`, `resource`, `proc`,
`talent`, `aura` or `aoe`.

⚠ **Three of those five are new since 2026-08-22, and two of them ELIMINATE**, which is the one
thing a sealed display had never done before: below six imps Implosion draws V11's hatch and a
negative mark, and at two Cores so does Power Siphon. **The boundary is unchanged and this is why
it holds:** cap hands the client a *band table* — whole numbers and what to draw at each — and the
client evaluates it against the count. cap never receives the count, never compares it, and never
learns which band fired. What changed is not what cap reads; it is what the client is willing to
draw on cap's behalf.

⚠ **The fifth authors no threshold at all.** `AddPandemicRegion` computes
`GetRefreshExtendedDuration − GetAuraBaseDuration` per spell inside the client, so cap does not
even supply the number — which makes it the *safest* sealed display in the catalog and not the
riskiest.

Two optional **count displays** (Demonic Core, Wild Imps) are sealed and are also sink-only. They
are context, not conditions: cap hands the AuraContainer a filter and a threshold and never reads
back. They are the reason this file has a section 4.

---

## 2. Facts, classified

Every fact the catalog consumes, tagged **readable** / **sealed-display** / **open**, with its
recipe and evidence (`../spec.md` §3.6 is the boundary; `../authoring.md`'s recipe index owns the
recipes).

| Fact | Lane | Recipe | Evidence | Consumed by |
| --- | --- | --- | --- | --- |
| **Soul Shard current value** | **readable** | R3 | one of the seven never-secret secondaries; `power = "SoulShards"` has shipped since the pilot (`Catalogs/Demonology.lua`, resolved `Enum.PowerType[name]` at `Sense.lua`). T1 blue *Midnight Public Alpha Addon API Changes, 2025-11-24*; `security-taint-and-restricted-data.md` §4.12 | cues **A**, **B**, **D**, **F**'s gate |
| Readiness of a cooldown row | **readable** | R2 | CDM `Available` / `OnCooldown` alert-edge latch; `security-…` §4.8 | every lit row, and cue A's gate |
| Affordability of a spender | **readable** | R1 | `C_Spell.IsSpellUsable` **second** return, no `SecretWhen*` predicate | cue **E** on Hand of Gul'dan / Ruination |
| Spell identity across an override | **readable** | R7 | `overrideSpellID` readable in combat on 21/21 rows (`cooldown-manager.md`); the two override paths here are established from spell data and logs, not observed in the client — §3 | row 9's two bands, cue **D**, and cue E's live-id read |
| **Demonic Core proc** | **readable** | overlay `proc` | `SpellActivationOverlay` @ 12.1.0.69214 row **3697**: trigger **Demonic Core `264173`**, `IconHighlightSpellClassMask_2 = 64`, which matches **Demonbolt `264178`**'s `SpellClassOptions` mask `[0, 131072, 64, 0]` *[T1 DB2]*. So `IsSpellOverlayed(264178)` is true exactly while a Core is up | cues **B**, **C** |
| AoE / single-target intent | **readable, not a game read** | cap's own `/cap aoe` toggle | n/a — cap owns the value | cue **G** |
| Whether To Hell and Back is taken | **readable** | the `talent` predicate | node 110199 / entry 136728 (`ability-inventory.tsv` @ 12.1.0.69214); ⚠ the `C_Traits` call shape is `[gap]` — Havoc's *Open facts* 7 | cue **G** |
| Whether Reign of Tyranny is taken | **readable** | the `talent` predicate | node 110201 / entry 136730 | nothing yet — it gates a band that is not authored (§5.1) |
| **Summon Demonic Tyrant cooldown remaining** | **sealed-display** | S4 → `sealed-cooldown-range`, one-sided **and** two-sided | `C_Spell.GetSpellCooldown` is `SecretWhenCooldownsRestricted`; the duration object carries the secrecy | cue **F** (`within = 5`) and cue **J** (`beyond = 10.5`, `within = 21.5`) |
| **Demonic Core application count** | **sealed-display** | S7 + S11 → `sealed-count-bands`; S10 → `sealed-count-bar` | the managed AuraContainer owns the display; a tainted-created `NumericRuleFormatter` is honoured `[client 2026-08-21]` and a band's `format` may carry a texture escape | Power Siphon's eliminating band **and** Demonbolt's segmented Core bar. **Not a condition** |
| **Wild Imp application count** | **sealed-display** | S7 + S8 + S11 → `sealed-count-bands` (complement) | as above; Wild Imp `296553` is a Category-2 row in set 60 (OrderIndex 47) *[T1 DB2]* | Implosion's eliminating band. **Not a condition** |
| **Doom's pandemic window** | **sealed-display** | S9 → `sealed-pandemic` | `AddPandemicRegion` seals a Region's `Shown` and drives it from the client's own `GetRefreshExtendedDuration − GetAuraBaseDuration`, per spell — cap authors no threshold | Demonbolt, gated on `talent(doom)`. **Not a condition** |
| `buff.demonic_core.stack <= 1` **as a hold** | **sealed-display** | S7 + S11 | two breakpoints: silent below two, hatch plus a negative mark at two. §5.2 | rung 1, drawn. DEM-14 |
| `buff.wild_imps.stack >= 6` **as a hold** | **sealed-display** | S7 + S8 + S11 | the same table run the other way: drawn below six, cleared at six. §5.2 | rung 9, drawn. DEM-13 |
| **Whether any Wild Imp is out at all** | **readable** | R2's alert edges → the `aura` latch | a Category-2 row raises `OnAuraApplied` / `OnAuraRemoved`; an unbound row reads UNKNOWN, never false | cue **H** — the one state a sealed display structurally cannot reach, because with no aura there is no button |
| **Whether Doom is taken** | **readable** | the `talent` predicate | node 110200 / entry 136729 (`talents.json` @ 12.1) | the readable gate on Demonbolt's pandemic display |
| `buff.dominion_of_argus.up` | **open** | the `aura` latch, unmeasured on this row class | `1276166` is a Category-**3** (TrackedBar) row in set 60, OrderIndex 50 *[T1 DB2]*; the latch is built on TrackedBuff `OnAuraApplied` / `OnAuraRemoved` edges and no measurement covers TrackedBar. `[searched 2026-08-19: CooldownSetSpell @ 12.1.0.69214, SpellActivationOverlay @ 12.1.0.69214, Track.lua's edge table, cdm-rider-patterns.md §6]` | rung 2. **No hint.** |
| **Which Demonic Art is armed**, when it is Overlord | **open** | — | Pit Lord and Mother of Chaos are visible through R7 (they change a button); Overlord changes none. `428514` holds two Category-2 rows in set 60 and which is the armed Art is unmeasured | nothing — noted because it is one measurement from closing |
| `cooldown.summon_demonic_tyrant.remains` as a **two-sided band** | **sealed-display** | S4, both bounds — `Channel.BandPoints(beyond, within)` is a three-point curve, and `Catalog.Check` accepts the pair provided `beyond < within` | shipped 2026-08-24; `Catalog.lua`'s exactly-one assertion was relaxed in the same change | rungs 6 / 7, **drawn**: `dreadstalkers_awaits_tyrant`, cue **J**, scenario DEM-15. §5.1 |
| `target_if=(!debuff.doom.up)` | **not expressible** — and not for a data reason | — | `debuff.doom.up` *is* routable (`460553` is a Category-2 row in set 60 and the `aura` predicate takes a `unit`, as Retribution's Expurgation does). What has nowhere to go is the **instruction**: a CDM row is a button, not a target | rung 13. §5.3 |
| `gcd.max` | **sealed, and floored rather than read** | S4's guard | `UnitSpellHaste` is sealed in instanced combat, so any band derived from it is authored at the **unhasted 1.5** and never computed | the unwritten Dreadstalkers band's bounds |
| `fight_remains` | **open (and out of scope)** | — | perfect information; no human equivalent. cap does not model the encounter | rung 1's `|fight_remains<10`. Deliberately unmodelled |
| `active_enemies` | **not modelled** | — | replaced by the `/cap aoe` toggle, as on Havoc and Retribution | rung 9 |

---

## 3. The two transforms, in full — they are what makes this catalog small

`../authoring.md`'s recipe index R7 names "Shadow Bolt↔Infernal Bolt" as the canonical case, and this is
the catalog it was named for. Both transforms are established from **spell data**, not from a
secrecy argument, and they are not equally well established.

| Transform | Established by | Confidence |
| --- | --- | --- |
| Shadow Bolt `686` → **Infernal Bolt `433891`** | the aura's own Tier-1 description, spec-conditional: *"Mother of Chaos empowers your next `$?s137044[Shadow Bolt][Incinerate]` to become Infernal Bolt."* `137044` is the **Demonology Warlock** spec aura *[T1 DB2: `SpecializationSpells` @ 12.1.0.69214]*, so the string itself picks Shadow Bolt here | **Tier 1** |
| Hand of Gul'dan `105174` → **Ruination `433885`** | ⚠ **Tier 2.** The Tier-1 description on `428522` says *"your next **Chaos Bolt** to become Ruination"* — Destruction's spell, in an unbranched hero-tree string. `knowledge/classes/warlock/demonology/diabolist-sequences.md` reads the transform off six top Warcraft Logs parses (Ruination cast count matches the Diabolic Ritual: Pit Lord count 1:1 — 13 = 13 on one parse, 77 vs 76 pooled) and reports **Hand of Gul'dan** | **Tier 2 — marked** @verify-ingame |

Neither `433885` nor `433891` holds a Category-0 (Essential) row in any `CooldownSet` at
12.1.0.69214; both are Category-2 rows in set 60 (OrderIndex 58 and 59) *[T1 DB2]*. So an
override on a row that *does* have one is the only way either reaches the Cooldown Manager, which
is what makes the transform argument necessary rather than merely convenient.

**Neither transform has a cooldown of its own**, so the "does the row keep drawing the base
spell's swipe" question that nearly broke Retribution's row 3 does not arise here — the dial
resolves `overrideSpellID` before reading (`knowledge/addon-dev/cooldown-manager.md` §3.1.1) and
finds no cooldown either way.

### The proc measurement

`../authoring.md`'s recipe index has no row for *"is this proc readable"*, and the honest answer is that
it is a question about **spell data**, not about the secrecy rules. Under 12.1's wholesale aura
secrecy a buff is sealed — but cap's `proc` predicate is
`C_SpellActivationOverlay.IsSpellOverlayed(spellID)` (`Sense.lua`'s `readProc`), a plain boolean
keyed on the **highlighted spell**, wholly independent of the aura API and measured readable in
combat (`knowledge/addon-dev/cooldown-manager.md`). Blizzard's own Cooldown Manager calls it the
same way *[T1 src @ 12.1.0]*.

At 12.1.0.69214, for Demonology *[T1 DB2: `SpellActivationOverlay` × `SpellClassOptions`]*:

| Trigger aura | Highlight mask | Matches | So `proc(x)` is true when |
| --- | --- | --- | --- |
| **Demonic Core** `264173` | mask₂ `64` | Demonbolt `264178` (mask₂ `64`) | `proc(demonbolt)` — **used, cues B and C** |
| **Infernal Bolt** `433891` | mask₀ `1`, mask₁ `64` | Shadow Bolt `686` (mask₀ bit 0) and Incinerate `29722` | `proc(shadow_bolt)` — **not used; see below** |
| **Ruination** `433885` | all four masks **zero** | nothing | never |
| Blazing Meteor `394776` | mask₀ `2097152` | Hand of Gul'dan `105174` | — the trigger aura is absent from Demonology's 12.1 inventory |
| Demonic Calling `205146` | mask₀ `33554432` | Call Dreadstalkers `104316` | — likewise absent at 12.1 |
| Shadowy Inspiration `196606` | mask₀ `1`, mask₂ `64` | Shadow Bolt and Demonbolt | — likewise absent at 12.1 |

Three consequences the design leans on:

1. **Demonic Core reads through one plain boolean**, which is why cues B and C cost no new
   mechanism and why the pilot's Demonbolt hypothesis was routable in the first place.
2. **`proc(shadow_bolt)` is a genuine second route to the Infernal Bolt state** and the catalog
   deliberately does not take it. Row 9's `identity` says the same thing and says it about the
   row rather than about an aura, so the two-band design and cue D rest on one fact instead of
   two that could disagree. Recorded because it is a *live* alternative, not an absence.
3. **Ruination's overlay is useless**, exactly as Hammer of Light's is for Retribution: the row
   exists with an all-zero highlight mask, so it can highlight nothing. Row 7's `identity` says
   everything the overlay would.

⚠ **`proc` names the button, not the buff.** `proc(demonbolt)` is Demonic Core's, and it is used
both to *release* Demonbolt (cue C) and to *gate* its overcap badge (cue B) — the same predicate
in both polarities on one row.

---

## 4. The sealed displays, and why they are in the safety case at all

**Four rows-worth of display, on three sinks.** Power Siphon (`sealed-count-bands` on Demonic Core
`264173`), Implosion (`sealed-count-bands` on Wild Imp `296553`, the complement), Demonbolt
(`sealed-count-bar` on Demonic Core, `max = 4`, **and** `sealed-pandemic` on Doom `460553`).
They are in this file because they are the one place a reader might reasonably suspect a branch,
and they are not one:

- The managed AuraContainer owns the **whole** display. cap registers a slot with
  `candidateFilters.includeSpellIDs = { [auraSpellID] = true }`, styles it inside
  `initializeFrame`, and never touches the subtree again — it is a **forbidden object**
  after that window, for reads as well as writes.
- **A band table is a rule, not a comparison.** cap builds a list of `{ threshold, format }` out
  of whole numbers it authored and hands it to a `NumericRuleFormatter`. The client calls
  `FormatNumber(applications)` and `SetText`. cap never receives the count, never compares it, and
  never learns which band fired. `FormatNumber` is documented `ConstSecretAccessor` precisely so
  the client may do this on cap's behalf.
- **The bar seals only its VALUE.** `SetApplicationBar` adds `Enum.SecretAspect.BarValue` to the
  StatusBar's value, so the texture, size, orientation, colour and render mode stay ordinary cap
  calls made at setup — and none of them is a function of the count.
- **The pandemic window seals only `Shown`, and cap authors no threshold for it at all.** The
  client computes `GetRefreshExtendedDuration − GetAuraBaseDuration` itself, per spell.
- cap reports `offered` / `armed` / `refused` and never `drew`. **Accepted is not drawn**
  (`../authoring.md` → *Accepted is not drawn*) — whether any of it ever appears is an eyeball,
  not a capture.

⚠ **TWO OF THEM ELIMINATE, and that is genuinely new.** `../render-shelf.md` Part 0.5's reading
model had two eliminating signals — Blizzard's swipe and cap's negative badge — and since
2026-08-22 it has three: a **band the client evaluated**. Power Siphon at two Cores and Implosion
below six imps both wear V11's hatch and a negative mark, drawn out of the one FontString the
count sink owns, and `scenarios.md` writes states that step past them (DEM-13, DEM-14).

**Why that does not move the boundary.** The eliminating decision is *the client's*, made against
a value cap never sees, from a rule cap wrote in whole numbers. The alternative — cap reading the
count and deciding — is what §3.6 forbids and what nothing here does. The thing to watch is not
safety but **truthfulness**: a band table is an authored threshold, and an authored threshold is a
thing to get wrong. The boundary case is documented (`threshold` is the *minimum* input a rule
applies to, so a value on it takes the upper band) and pinned in a test, because an off-by-one
here is invisible until it is wrong in a pull.

⚠ **A band cannot rule out a row whose subject does not exist.** With no aura there is no aura
button, so no sink on it draws anything. That state is covered by the readable `aura` latch (cue
**H** on Implosion) and by the readable `proc` (Demonbolt), which is a different fact answering a
different question — *is the subject present*, not *how many* — and is the correct tool for it.

---

## 5. The open facts, routed

Each becomes an `@verify-ingame` marker on the claim, or a ClientLab `@pending-test` once a test
exists (`../authoring.md` stage 5; `projects/addon-lab/docs/lab-process.md`). **An unknown is a
marker on the claim, never a line in a tool and never a TODO here.** A load-bearing open fact is
a stop-and-ask (`../spec.md` §3.6); none below is load-bearing on a *press* — every one of them
costs a hint and none of them causes a wrong one.

### 5.1 The two-sided cooldown band — CLOSED 2026-08-24

Rungs 6 / 7's Reign-of-Tyranny window. It was never an open fact and never a client limit — it
was a shelf gap, and the shelf closed it: `Channel.BandPoints(beyond, within)` draws the
three-point curve and `Catalog.Check` now accepts both bounds together. The hold is authored as
`dreadstalkers_awaits_tyrant` (cue **J**), walked in DEM-15, and the full history is at
`catalog.md` → *Defeats*, item 1. The safety case is unchanged by it, which is the point worth
recording here: cap hands the client three points and a curve, compares nothing, and still never
learns how long Tyrant has left. ⚠ It has **not flown** — no client has evaluated a three-point
band.

### 5.2 The aura stack count as a hold — CLOSED 2026-08-22

Rungs 1 and 9. Full history at `catalog.md` → *Defeats*, item 2. Both gates are **numbers**, and
what changed is that cap now has a route to a number: it hands the client a **band table** and the
client evaluates it. So the catalog draws these facts rather than drawing nothing, and it still
performs no comparison.

⚠ **The old defeat's reasoning is preserved because it is still the right reasoning.** It was:
*cap holds no route to a number, so the catalog draws nothing rather than substituting the boolean
the `aura` latch could give it — `aura(demonic_core)` is true at one Core and at three, and
substituting it would badge Power Siphon in a state where the APL presses it.* **A weaker true
fact is not a substitute for a stronger one**, and that rule is unchanged. What changed is that
the stronger fact is now reachable, so the substitution is not even tempting.

⚠ **The `aura` latch is still used, and for exactly the state the band cannot reach.** With **no
aura at all** there is no aura button, so no sink on it draws anything — a band cannot rule out a
row whose subject does not exist. Implosion at zero Wild Imps is covered by cue **H**, a readable
`!aura(wild_imp)`, and Demonbolt at zero Cores by the readable `proc` it already had. That is not
the weaker-fact substitution above: it is a *different fact* (is there one at all) answering a
*different question* (is the subject present), and it is the correct tool for it.

⚠ **`min = 2` is gone.** It was `Catalog.Check`'s guard and it is retired, because it was never a
platform limit: `applications > 1` is what the client does when **no formatter is passed**.
Implosion's threshold of 6 was recorded here as inexpressible; it is expressed as a breakpoint at
6 and DEM-13 is the scenario.

### 5.3 Target selection

Rung 13's `target_if`. `catalog.md` → *Defeats*, item 3. The **fact** is readable (Doom `460553`
is a Category-2 row and the `aura` predicate takes a `unit`); the **instruction** has no surface.
Nothing is waiting on a measurement.

### 5.4 Dominion of Argus

Rung 2. One measurement: **does a Category-3 (TrackedBar) Cooldown-Manager row raise
`OnAuraApplied` / `OnAuraRemoved` alert edges?** If it does, `aura(dominion_of_argus)` is a
readable boolean and rung 2 authors itself as a `priority` promotion on Hand of Gul'dan with no
new vocabulary. If it does not, the row has no route and the catalog is already correct.
Failure direction today: a Hand of Gul'dan pressed one rung late inside a 15-second window.
@verify-ingame

### 5.5 Which of the two Diabolic Ritual rows is the armed Art

`428514` holds two Category-2 rows in set 60 (OrderIndex 16 and 17, cooldownIDs 9472 and 9426).
If one is the armed **Demonic Art**, `aura(demonic_art)` is readable and Art: Overlord — the one
Art that changes no button — becomes visible. Nothing in this catalog depends on it; it is
recorded because the same measurement closes a **Destruction** rung that does. @verify-ingame

### 5.6 The Ruination transform target

§3's Tier-2 claim. One in-game observation: with Diabolic Ritual: Pit Lord's Art armed, does the
**Hand of Gul'dan** row display Ruination? Failure direction if wrong: row 7's `identity` never
fires, cue E reads the wrong cost, and Ruination is drawn on no row at all. **This is the single
most load-bearing unverified claim in the catalog.** @verify-ingame

### 5.7 `C_Traits.GetNodeInfo`

`[gap]` — inherited unchanged from Havoc's *Open facts* 7. The `talent` predicate is shipping and
`knowledge/addon-dev/` records nothing about the call's shape or its combat behaviour. A refused
read draws nothing, so this catalog's only exposure is cue G staying dark on a build without To
Hell and Back — a missed skip, not a wrong press. @verify-ingame

### 5.8 The five-shard maximum

Cue A compares against the constant 5, authored from the APL's `soul_shard=5`. `UnitPowerMax` is
readable (a different predicate from `UnitPower`), so a build with a different maximum could in
principle be detected — but nothing in the 12.1 Demonology tree changes it and the catalog does
not read it. Failure direction: a hold that never releases, which is visible immediately.
@verify-ingame

---

## 6. Unknown never becomes confidence

Every predicate above returns **UNKNOWN** rather than `false` when the client refuses it, and
every marker withholds on UNKNOWN. Three places in this catalog where that is doing real work:

1. **Cue C is a negation.** `!proc(demonbolt)` must not light because `IsSpellOverlayed` refused
   — that would hold Demonbolt for the whole fight while looking certain. `Signal`'s
   unknown-safe evaluation is what makes a negated readable term safe to author at all.
2. **Cue D reads a different row.** `identity(shadow_bolt)` is UNKNOWN if row 9 is not bound —
   the player never enabled Shadow Bolt in their Cooldown Manager — and the marker must go dark,
   not assert "not transformed".
3. **The `aura` latch has no third supplier and no timeout** (`Track.lua`). A row the player
   never enabled has no `cooldownID`, nothing is ever written for it, and `World` reports
   UNKNOWN. That is why §5.4's unmeasured edge is a missing *hint* rather than a wrong one — but
   it is also why the enablement question is a correctness requirement wherever a latch is
   authored, exactly as it is for Retribution's cue G. **This catalog authors exactly one `aura`
   marker** — `implosion_no_imps`, cue **H**, the one state Implosion's count band structurally
   cannot reach, because with no Wild Imp there is no aura and every sink on that button draws
   nothing. So the exposure is real and it is small, and it is worth naming rather than denying:
   **cue H depends on the player having the Wild Imp tracked-buff row enabled.** With the row
   disabled the latch reads UNKNOWN, the marker goes dark, and Implosion is offered as an
   ordinary candidate with no imps out — a **missed skip**, never a wrong press. That is the
   direction this catalog accepts everywhere else too, and accepting it here is a decision, not
   an oversight. It is also why the two *count* facts stayed displays: a display needs no latch
   and therefore has no enablement exposure at all.

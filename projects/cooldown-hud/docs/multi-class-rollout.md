# Cooldown HUD — the multi-class rollout (Retribution + Havoc + Protection + Vengeance + Devourer)

> **STATUS: Phase 0 + Phase 1 + Phase 2 shipped. THE HAVOC FLIGHT RAN 2026-08-03 AND FAILED;
> the Phase-1 remediation has shipped and a RE-FLY is the outstanding deliverable.**
> Phases 3–5 (Protection, Vengeance, Devourer) remain blocked **behind the Havoc in-game
> pass**, not behind Retribution's.
>
> ⚠⚠ **THE FLIGHT FOUND A GAME-API FACT NOBODY IN THIS PROJECT KNEW, AND IT IS NOT A HAVOC
> FACT.** `UnitPower` secrecy is **per power type**, and the rule is **primary vs. secondary
> resource** — primary resources are secret **forever**, in a city and mid-pull alike. The
> first four specs shipped were **lucky** (Soul Shards ×2, Holy Power ×1 are all
> never-secret); **most specs in the game behave like Havoc**. Read
> **§ FLIGHT RECORD — PHASE 2** before touching any remaining phase. ⚠ **Vengeance and
> Devourer are both Fury specs and inherit all of it.**
>
> This file is the forward plan as it was handed to the 2026-08-03 session, **plus** two
> sessions' findings and one flight record. Read **§ FLIGHT RECORD — PHASE 2** first (it is
> the current state), then **§ SESSION LOG — PHASE 2**, then **§ SESSION LOG — PHASE 1** (it
> corrects several claims in the plan body and records five shipped fixes, four in-game
> measurements, and the architectural finding — which has since **shipped**, as
> `roster-state-plan.md` Phase 5 / v0.32.92).

---

# § FLIGHT RECORD — PHASE 2 (2026-08-03): Havoc flew, and failed

Max-level Demon Hunter, Fel-Scarred, single-target and AoE at a dummy, on **v0.32.93**.
`wowkb.cdmp flight` + `wowkb.cdmp decisionlog` produced **2380 Havoc decision-log lines,
2374 of them in combat**. The user's summary was *"hints felt all over the place."*

## What the log said

| Winner | count | why it won |
|---|---:|---|
| Throw Glaive | 770 | L15 — its Fury cost resolved to **0** |
| Vengeful Retreat | 480 | L5 — no Fury gate |
| Felblade | 414 | L11 — `deficit = 120 - 0 = 120`, always ≥ 40 |
| Immolation Aura (+CFire/CFire2) | 385 | L12 — same |
| The Hunt | 41 | L3 — no Fury gate |
| **Chaos Strike / Annihilation** | **0** | L8/L13 — `projected >= cost` never true |
| **Eye Beam** | **0** | L9 — same |
| **Blade Dance / Death Sweep** | **0** | L7/L10 — same |
| **Metamorphosis** | **0** | L2 — vetoed by `not bladeDanceUsable` |

**`PW:0/+0` on all 2380 lines. The entire core rotation was unreachable.**

⚠ **The in-combat `w:-` ratio was 0.0 %** — a perfect score, and *because of* the bug: the
generator lines were jammed on, so something always won. **Read the winner distribution, not
the ratio.** That lesson is now criterion 11 in `specs/havoc/observability-map.md` and a
banner in `wowkb.cdmp decisionlog`'s consumers.

## Root cause — two coercions over a secret rail

`UnitPower("player", Enum.PowerType.Fury)` returns a **Secret Value**, so `readOnePower`
correctly dropped the `value` field. Two separate coercions then turned *"we could not read
it"* into *"you have zero"*:

- `Coach:ResourceBars` — `value = p.value or 0`
- `CoachHavoc:RankWinner` — `local live = ctx.fury or 0`

**Zero is the worst possible degradation** for a resource: every spender becomes unaffordable
and every generator maximally urgent, which is exactly the distribution above. This is the
project's own **absent-is-never-zero** rule broken in the one place nothing tested. ⚠ And
100 green oracle cases did not catch it, because the fixture **supplied the number the client
refuses** — a harness that can hand the code a resource value cannot reproduce the only state
the game ever produces.

## The game fact — and it generalises to most of the game

> "We have relaxed restrictions around `UnitPower` so the player's **secondary** resources are
> no longer secret (**primary resources remain secret**). Affected resources: Combo Points,
> Runes, Soul Shards, Holy Power, Chi, Arcane Charges, Essence."
>
> — `[T1]` Blizzard blue post, *Midnight Public Alpha Addon API Changes*, 2025-11-24

| probe | Fury (17) | Holy Power (9), the control |
|---|---|---|
| `C_Secrets.GetPowerTypeSecrecy` | **2** (`ContextuallySecret`) | **0** (`NeverSecret`) |
| `C_Secrets.ShouldUnitPowerBeSecret("player", …)` | **true**, city *and* mid-pull | false |

⚠ **`ContextuallySecret`'s "context" is the UNIT, not combat** — the predicate reads *"…unless
the subject unit does not have a power of this type."* You always have Fury. **There is no
out-of-combat window and no seed value.** ⚠ `UnitPowerMax` is a **different predicate**
(`SecretWhenUnitPowerMaxRestricted`, non-player-controlled units only), so **the max is
readable** — 170 on the test character, not the 120 `SpecHavoc.powers` declared.

⚠ **This invalidated `roster-state-plan.md` §7.2**, which measured Soul Shards, concluded
*"the flagged read WORKS IN COMBAT"*, and generalised to every power. That section now carries
a correction box. The claim is true for Soul Shards and false for every primary resource.

## The remediation, in two phases (user's decision, 2026-08-03)

**Phase 1 — shipped.** Affordability moves to `C_Spell.IsSpellUsable`'s second return,
`insufficientPower`, attached per-ability by State so it is loggable, fixture-testable and
visible in the decision log. The deficit gates are dropped in favour of Blizzard's own
ordering-and-repetition shape. The absent-rail coercions die.
`specs/havoc/rotation.md` → *Fury is SECRET* is the full write-up;
`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.12 is the game-wide rule.

**Phase 2 — designed, NOT built.** `IsSpellUsable` is binary (false at 40 Fury and at 170
alike), so **overcap avoidance is unrecoverable through it** and Havoc will overcap without a
warning. Phase 2 keeps the deficit gates as an explicit **hypothetical** and runs the cascade
twice — once assuming Fury has room, once assuming it is capped. Identical winners → one cue
(the common case, because any ready cooldown wins in both). Different winners → both are
drawn and a **`LuaCurveObject`, forwarded through the pipeline as an opaque draw parameter**,
decides in C which one the player sees. No Lua ever compares Fury. See § *Phase 2 design*
below. **Staged behind a clean Phase-1 flight** because its visible outcome is
**unobservable to the decision log** — a permanent blind spot in the one instrument that has
found every bug in this project, including this one.

## What Blizzard's own rotation does

`ActionPriorityLists/assisted_combat/demonhunter_havoc.simc` — the in-client Assisted Combat
list — contains **zero** Fury references, and handles the resource purely by **ordering and
repetition**:

```
chaos_strike,if=buff.metamorphosis.up
felblade                              <- bare, no deficit gate
chaos_strike                          <- again
immolation_aura,if=active_enemies>1   <- enemy count only
throw_glaive
chaos_strike                          <- and again, as the floor
```

⚠ **Do not over-read this as "Blizzard avoids secret resources."** Their other
assisted-combat lists branch on energy / rage / focus / runic_power freely — that engine runs
in C and sees everything. The finding is narrower and still load-bearing: **a competent Havoc
rotation is expressible with no Fury threshold at all.**

## Phase 2 design — the two-branch cascade + the Fury curve

> ### ⚠⚠ RECOMMENDED AGAINST, 2026-08-03 — MEASURE FIRST, THE MEASUREMENT IS IN
>
> This design exists to recover **overcap avoidance**, which Phase 1 gives up. WCL data says
> that is not worth recovering. Fury overcap across the top-100 Mythic parses on Imperator
> Averzian (12.0.7, `resourcechange` `waste` vs `resourceChange`, type 17):
>
> | player | gained | wasted | waste |
> |---|---:|---:|---:|
> | Paprzdh | 4,119 | 311 | 7.6 % |
> | Yunadh | 4,345 | 482 | 11.1 % |
> | Bibussy | 5,612 | 708 | 12.6 % |
> | Chezzar | 5,386 | 1,237 | 23.0 % |
> | **pooled** | **19,462** | **2,738** | **14.1 %** |
>
> **The best players in the world waste one Fury in seven**, and the dominant source is
> **Demon Blades** — a passive off autoattacks that no rotation decision can gate. maxroll's
> only Fury sentence for the spec is *"Cast Immolation Aura if you won't overcap on fury"*
> (one line, one button), and **that** piece is already recovered by L12's readable
> charge-cap gate (shipped v0.32.95).
>
> So this would be elaborate machinery — a doubled cascade, a new contract invariant, an
> opaque draw parameter, and a **permanent blind spot in the decision log**, the one
> instrument that has found every bug in this project — to chase a behaviour top parses do
> not practise. **Essence Break's pooling gate (rotation.md Deviation 13) is the only Fury
> loss still worth calling real**, and it is one line rather than an architecture.
>
> Kept below because the `LuaCurveObject` technique is correct and will be the right answer
> for some future problem. It is not the right answer for this one.


`UnitPowerPercent(unitToken, powerType, unmodified, curve)`
(`UnitDocumentation.lua:2716`) returns *"the result of evaluating the curve with the
percentage as the input"*, evaluated **in C**. Build the curve with
`C_CurveUtil.CreateCurve()` / `CreateColorCurve()`. The result stays secret (it carries both
`SecretWhenUnitPowerRestricted` and `SecretWhenCurveSecret`) but can be handed straight to
`SetAlpha` / `SetVertexColor` / `SetStatusBarColor`, all on the 120-member
`SecretArguments = "AllowedWhenTainted"` list. **Shipping precedent: oUF does exactly this**
(`elements/power.lua`, colour via `UnitPowerPercent(unit, nil, true, color:GetCurve())`).

⚠ The curve must be applied **inside the same call that sets the alpha** — `setDotGlow`
re-asserts alpha at ~10 Hz, so an externally-mutated alpha would be clobbered (the trap the
`R.BURST` header documents).

⚠ **When the branches differ, the Fury-variant REPLACES `ROTATION_FALLBACK`** (user's
decision) — it is a strictly more informative runner-up, so the on-screen dot count never
grows.

**Contract changes** (`guidance-contract.json`), to be made deliberately rather than smuggled
in: `vocabularies.emphasis.invariant_singleTopPress` currently reads *"Exactly ONE cue holds
the 'press now' emphasis"*; Phase 2 makes that **two, mutually resolved in C**. And
`channels.cues.<cooldownID>` gains a `curve` field (opaque handle, pass-through only, never
inspected by the Coach or the Binder).

## ⚠ What every remaining phase inherits

**Check `C_Secrets.GetPowerTypeSecrecy` for the spec's resource during Step 0**, before a line
of rotation doc is written. A primary-resource spec **cannot use resource-threshold gates at
all**, and that changes the rotation model rather than being a detail to degrade later.

| # | Spec | Resource | Secrecy |
|---|---|---|---|
| 3 | Protection Paladin | Holy Power | ✅ **never secret** — safe, thresholds work |
| 4 | Vengeance DH | **Fury** + Soul Fragments | ⚠ **Fury is SECRET.** Inherits all of Phase 1. Soul Fragments ride `GetSpellCastCount`, a different channel |
| 5 | Devourer DH | **Fury** + Souls (aura stacks) | ⚠ **Fury is SECRET.** Same |

⚠ **Do not start either DH spec until the Havoc re-fly is clean** — that is exactly what the
rollout gate is for, and this flight is the reason it exists.

---

# § SESSION LOG — PHASE 2 (2026-08-03): Havoc DH shipped, and the gate inverted

## The gate did not pass. It moved.

The Phase-1 gate read *"Phases 2–5 remain blocked. Do not start a new spec"*, and its stated
reason was that a **max-level Retribution flight** had never happened. Two things changed and
the user ruled on a third:

1. **The architectural precondition is satisfied.** The gate's deeper justification was the
   *ARCHITECTURAL FINDING* below — three of Retribution's five flight defects came from
   deriving an ability's facts through a **CDM row's identity**. That fix,
   `roster-state-plan.md` Phase 5 (the roster anchor), **shipped 2026-08-03 as v0.32.92**.
   The RECOMMENDATION in that section is **done**, and in its full form rather than the
   narrow one.
2. **The flight requirement cannot be satisfied.** The user has **no max-level Paladin**. The
   level-37 pass could not exercise the hero-tree branch, the burst lines, or Phase 5's
   acceptance at all, and no amount of waiting changes that.
3. **User decision (2026-08-03): proceed to Havoc and discharge the gate from the DEMON
   HUNTER side.** The user *does* have a max-level Demon Hunter. This **inverts** the gate
   rather than skipping it — the pattern still gets a max-level flight, just not on the spec
   that first raised the question.

⚠ **So the Havoc in-game pass is a HARD DELIVERABLE, not a smoke test.** It carries two sets
of criteria: Havoc's own, and Retribution's **orphaned Phase-5 acceptance**, which now has
nowhere else to run. Both live in `specs/havoc/observability-map.md` → *THE FLIGHT'S JOB*.
**The accepted cost:** if that flight finds a pattern defect, the defect is in **two** shipped
specs rather than one. The mitigation is that the flight happens **before** Protection,
Vengeance and Devourer — not after.

## What shipped

`specs/havoc/` — four docs, 987 lines (`rotation.md` 431 · `notes.md` 270 ·
`observability-map.md` 174 · `input-contract.md` 112) — plus `SpecHavoc.lua` (538) and
`CoachHavoc.lua` (642) implementing **L1–L15**, wired into the `.toc` after the Retribution
pair, and `tests/spec/coach_havoc_apl_spec.lua` (**100 cases**) as the independent oracle.
Tests **883 → 983**, luacheck 0, and the two Warlock oracles + the Retribution oracle stayed
green **unchanged** (the standing regression guard held).

**Zero pipeline generalisations were needed**, against the plan's budget of one or two — see
the corrections below for why.

## ⚠ Corrections this phase makes to the plan body and the DB2 appendix

Each was resolved **by property** from Tier-1 DB2 @ 12.0.7, never by name (Demon Hunter has
the Hammer-of-Light homonym problem twice over — `SpellName` carries 76 rows called
"Annihilation" and 19 called "Chaos Strike"). The durable write-up is `specs/havoc/notes.md`.

1. **THREE lying base cooldowns, not one.** The appendix's *"+1 (Fel Rush)"* row is wrong.
   **Immolation Aura 258920** (`CategoryRecoveryTime 1500` vs 30 s on charge category 1676)
   and **Vengeful Retreat 198793** (`RecoveryTime 500` vs 25 s on 1601) have the identical
   shape — a short **shared-category lockout** on the spell row masking the real charge
   recovery. (`ns.BaseCooldown` returns `CategoryRecoveryTime` when `RecoveryTime` is 0.)
2. **…and the risk inverts in our favour.** All three are **ONE-charge** categories, so
   `usable()`'s one-charge rule (`cur >= 1 AND probablyUp`, shipped for Retribution flight
   defect #5) makes the **charge count veto the early cooldown read for the whole real
   duration**. **The press is protected; only the decoration lies.** The generalised napkin
   fix was therefore **deliberately not shipped** — the exact one-line shape it should take
   is recorded in `rotation.md` → *The two lying cooldowns*, for the flight to arbitrate.
   Residual hole: an **absent** charge count falls through to the early napkin (flight
   question #1).
3. **THREE rotational presses are CDM-Utility, not two** — Felblade 232893, Vengeful Retreat
   198793, **and Fel Rush 195072, which has TWO rows (one Essential, one Utility)**. And the
   appendix's implied worry — *"which Retribution's model never scores"* — **dissolved**:
   both fences that could have blocked them (the SOON fence `Coach.lua:501` and the
   virtual-row fence `State.lua:1941`) test the **spec-authored `cadence`**, never the CDM's
   category. Declaring them `"filler"` / `"oncd"` is the whole fix. **No pipeline edit.**
   ⚠ The next **tank** spec will meet the same shape — this is the finding to carry forward.
4. **The meta fork is cleaner than "two complete priority lists" suggests.** Metamorphosis
   **162264** (the *aura*, not the tracked 191427 cast) carries two `EffectAura 332` effects →
   Annihilation 201427 and Death Sweep 210152. Both are **1:1 display overrides riding their
   own base's frame**, which is the channel Demonology's Ruination and Retribution's Hammer of
   Light already use — so the Coach cues the **base** spellID and the icon supplies the label
   for free. Modelled as **one cascade** with `ctx.inMeta` on exactly **two** lines (L6 is
   meta-only; L7-vs-L10 is the Blade Dance / Eye Beam inversion). Unlike Retribution, **no
   semantic discriminator is needed anywhere** — every Havoc override replaces exactly one
   named base.
5. **The Reaver's Glaive sequence is a DATA WALL, not a modelling problem** — and therefore
   **not** a parked switch. `Rending Strike` 442442, `Glaive Flurry` 442435 and
   `buff.reavers_glaive` 442294 have **no `CooldownSetSpell` row** in set 1599, so six APL
   lines (:56–61) are dark with no channel to light them. A parked `spec.X = false` switch
   waits on a question a *flight can settle*; this one already has an answer. The parked
   switch became **`HAVOC_RG_FROM_BUFF = false`** instead — whether Art of the Glaive 442290
   may count as "a glaive is armed" beside the transform, which is the `RET_HOL_FROM_BUFF`
   shape exactly and *is* flight-settleable.
6. **`SpecBindAlias` was needed, and the plan did not anticipate it.** SkillLine 1848 teaches
   **wrapper** spells: Chaos Strike **344862** → the CDM tracks **162794**; Fel Rush **344865**
   → the CDM tracks **195072**. The rung ladder asks the action bar about the *tracked* id and
   finds nothing, so both would silently lose their keybind hint. The Imp Lord case exactly.
7. **The TrackedBuff `CumulativeAura = 0` trap is real and costs nothing.** Art of the Glaive
   442290 reads 0 against its real aura 444661's **80**; Demonsurge 452402 vs 452416's **4**.
   But `state.buffs` is keyed by the **CDM row's** spellID and the channel is `IsActive()` — a
   **bool** — so a stack count was never reachable whichever id we keyed on. Declaring the
   *real* aura instead would create a roster entry with no CDM row, which Coverage reports as
   BLIND. Key on the tracked id; the real aura ids are documentation.
8. **New vocabulary, flagged as such:** L5 (Vengeful Retreat) reads **Eye Beam's napkin
   `remaining`** — the first cross-ability timing gate in any brain. Licensed because Eye
   Beam's 30 s lives on the spell row so the napkin counts it honestly. The rule that
   separates it from the handshake Retribution *dropped*: **a cross-ability timing gate is
   allowed when the other ability's cooldown is one the napkin can honestly count.** First
   suspect if VR misbehaves in the flight.
9. **`essence_break` is META-ONLY because the APL says so** — simc's top-level line at :87
   sits inside a `#` comment. Possibly an authoring accident; taking the file literally is the
   Tier-1-faithful call and it fails safe (a missed press, never a wrong one). **Re-check on
   the next simc pull.**

## What Phase 2 owes forward

1. **THE HAVOC FLIGHT** — the whole gate. Procedure + both acceptance sets in
   `specs/havoc/observability-map.md`. ⚠ Do the **out-of-combat `C_Spell.GetSpellCharges`
   sweep** (195072 / 258920 / 198793 / 185123, with 198013 as the control) *before* arming:
   it is the only way to check the three lying base cooldowns against the truth, and it is the
   read that caught Retribution's wrong `chargeCD = 12`.
2. Everything in *Still open* below that Phase 1 left, minus the architectural finding.

---

# § SESSION LOG — PHASE 1, 2026-08-03 (the first Retribution flight, and what it cost)

Retribution was flown for the first time on a **level 37** Paladin. Five defects were found
and fixed across **v0.32.88 → v0.32.91**. Tests went **827 → 849**, luacheck stayed at 0,
and both Warlock oracles stayed green **unchanged** throughout (the standing regression
guard held).

⚠ **The gate is not passed.** See *Still open*, below.

## The character matters — read this before interpreting anything

The test character is **level 37 of 90**. Consequences, all of which limit what this flight
could settle:

- **No hero tree** (they unlock at 71). Every `# config` line reads `hero:?`. The
  Templar / Herald-of-the-Sun branch is **untested and untestable** on this character.
- **Wake of Ashes and Execution Sentence are unlearned** (`DR:…ES:unlearned,WoA:unlearned`),
  so **L1, L2 and L4 never fired**. The burst half of the cascade is unflown.
- Talent-gated procs (Art of War, Righteous Cause, Empyrean Power/Legacy, Light's
  Deliverance) are mostly absent, so the proc lines are unexercised.
- **Observability-map questions 1 and 5 cannot be answered at this level.**

**A max-level pass is still required before Retribution can be called settled.**
⚠ **SUPERSEDED as a GATE (2026-08-03):** the user has no max-level Paladin, so this pass
cannot happen. The gate was **inverted onto Havoc** — see *§ SESSION LOG — PHASE 2*. The
requirement itself stands; it simply no longer blocks the rollout, and Retribution's
acceptance criteria are carried by the Havoc flight instead.

## The five defects

Each was mutation-checked; the note in parentheses is what turns red if the fix is reverted.

### 1 · v0.32.88 — the cost seam was Warlock-shaped (spenders cued at 0 Holy Power)

**Symptom:** Final Verdict — a 3-Holy-Power spender — cued at **0** Holy Power on 95 log
lines, 274 more at 1, 429 at 2.

Two halves, neither fatal alone:

- `ns.ShardCost` filters to `Enum.PowerType.SoulShards`, and it was the **only** cost seam,
  wired by the driver for every spec. No Paladin spender ever matched it.
- `ns.PowerCost` returned **0** for both *"no entry for that resource"* and *"genuinely
  free"* — its own comment told callers to guard the ambiguity, and `costOf` did the
  opposite. `spenderCost = 0` made L7's `projected >= cost` the tautology `projected >= 0`.

The `c > 0` guard removed earlier that day (correct in itself, for real free finishers) had
been *accidentally* rejecting the bad zero.

**Fix:** the resource became an **argument the spec supplies**. `ns.Coach.CostPowerType(spec)`
resolves it from `spec.powers`; `cfg.powerCost` is the general seam; `ns.PowerCost` is now
three-valued (`nil` unreadable / `0` explicitly free / `n` cost). `shardCost` survives only
so the Warlock brains and their oracles stay untouched — **folding them onto `powerCost` is
a mechanical follow-up.**

**Second site of the same bug:** `SpecRetribution.SpecPowerDelta` also read `ns.ShardCost`,
so the **in-flight Holy Power projection had been dead code for the life of the spec.** It
failed in the safe direction, which is why nobody saw it.

**Why 76 green oracle cases missed it:** `mock_ns.lua` *replaces* `ns.ShardCost` with a
fixture lookup that has no type filter and returns `nil` where the shipping reader returned
`0`, so the production path was unreachable — and the oracle's comment claiming it exercised
"the REAL cost path" was false. `Enum.PowerType` also had no `HolyPower` member. Both fixed;
the oracle now drives `fx.powerCost` (the client-level fake) through the shipping ladder.
*(Reverting the tri-state → 31 red.)*

### 2 · v0.32.89 — the napkin could not count down a charge-category cooldown

`GetSpellBaseCooldown` returns 0 for a charge-category spell, so `N.Record` stored nothing.
`chargeCD` (already authored, previously read by nothing) became the fallback, filed with
`source = "declared"` — never `"live"`. **Superseded in practice by fix #4**, which supplies
a measured, haste-scaled number; the fallback remains for rows the live read never covered.
*(Reverting → 2 red.)*

### 3 · v0.32.89 — a PARTIAL action-bar scan was cached as final

The retry only fired on **zero** bindings, so a scan that resolved most spells cleared
`dirty` and was cached forever. On login the bars populate over several frames and
`B.Start` registers the bar events *after* the client already fired them during load.
Generalisation: **an empty scan is a special case of a scan that is still changing.**
`scan()` already returned that signal; it is now the fence, capped and convergent.
*(Reverting → 3 red.)* ⚠ **This did not fix the reported symptom** — see *Still open*.

### 4 · v0.32.90 — a 1-charge charge category IS a charge pool

`readCharge` gated `charged` on **`max > 1`**. A 1-charge category renders like an ordinary
cooldown in the CDM, so the assumption looked right; the cost was the entire readiness model
on those rows. With `charged = false`, `usable()` fell through to the cooldown read — which
for a charge-category ability **latches ready forever** (the CDM raises `Available` on every
charge restore and never `OnCooldown`). Blade of Justice read ready on **4419** lines and
starved every line below it, which is why **Crusader Strike was never recommended**.
Those rows were never even wired into the charge napkin (State only binds for cast-decrement
`if charge.charged`).

**Why the fixture said otherwise, and this is worth remembering.** `cdm-cases` pinned "a max
of 1 is not a charge pool" against `cooldown-manager.md` §3.3. That rule is real but governs
the **rendered `ChargeCount` font string**, which falls back to `GetSpellCastCount` when
`maxCharges <= 1` because drawing "1/1" on an icon is useless. It says nothing about what
`GetSpellCharges` *returns*. **The case generalised a display rule into a data rule.**
Rewritten against the measurement, plus a new **control** case pinning that an ordinary
cooldown is excluded by the API *refusing* — the property that makes `>= 1` safe.
*(Reverting → 2 red.)*

### 5 · v0.32.91 — a 1-charge pool must agree with its own cooldown

**Symptom:** Judgment cued while on cooldown, on **191 of 226** disagreeing lines:

```
CD: ... Judg=c10 ...        CH: ... Judg~1/1
```

**Cause — the two-ladder hazard, and it is a genuine design flaw, not a typo.** The
**cooldown** is read on the *display identity*; **charges** use `overrideSpellID or spellID`
(rungs 4+5, because that is what Blizzard reads, `ItemData.lua:283-288`). On a row whose
identity flips, those ladders resolve to **different spells**. Judgment's row does flip — the
decision log's `# config` line alternates `…,FV,Judg` and `…,FV,HoW` all session. We were
comparing one ability's cooldown against another's charges.

**Invariant applied:** for a pool of **one**, "you have a charge" and "it is off cooldown"
are the same fact and cannot legitimately disagree; require both. For a pool of **two** they
legitimately differ (one banked, second recharging) — the Conflagrate rule, kept verbatim,
with a test that goes red if it is ever over-generalised. *(Reverting → 1 red.)*

## In-game measurements (fold into `knowledge/addon-dev/api-events-and-discovery.md` §2 — ⚠ NOT YET WRITTEN UP)

All taken 2026-08-03 with a validated control (`C_Spell.GetSpellCooldown` reading `SECRET`
in combat, proving restrictions were active).

| Channel | Verdict |
|---|---|
| `C_Spell.IsSpellUsable` | **Readable through combat, but IGNORES COOLDOWN.** Returned `true` while Blade of Justice was on cooldown and visibly swiping. Answers "enough resources", not "castable now". **Useless for readiness.** |
| `GetActionCooldown(slot)` | **SECRET in combat.** The action-bar surface is closed exactly like `C_Spell.GetSpellCooldown`. This was the promising lead — it would have given a real remaining duration — and it is dead. |
| `IsUsableAction(slot)` | Readable, same cooldown-blindness as `IsSpellUsable`. |
| `C_Spell.GetSpellCharges` (OOC) | **The good channel.** A 1-charge category answers `1/1` **with a haste-scaled recharge**; an ordinary cooldown **refuses (nil)**; no cooldown → nil. So *the client itself* draws the charge/no-charge line — `cur ~= nil` is the real predicate and `max` was never the question. |

Raw, out of combat, Retribution:

```
184575 Blade of Justice  1/1  rc=9.312     <- 1-charge CATEGORY
20271  Judgment          1/1  rc=10.243    <- 1-charge CATEGORY
35395  Crusader Strike   2/2  rc=5.587     <- 2-charge category
85256  Templar's Verdict nil               <- no cooldown at all
31884  Avenging Wrath    nil               <- ORDINARY cooldown (the control)
```

**A bonus method worth reusing.** Judgment `10.243/11` and Crusader Strike `5.587/6` both
give **0.931** — one haste factor, derived twice. Applying it to Blade of Justice:
`9.312/0.931 = 10.00`. So **BoJ's base recharge is 10 s and the declared `chargeCD = 12` was
simply wrong** — it held the button back two seconds too long every cast. Corrected.
*Live reads beat authored constants; this is the evidence.*

**Also measured, from the decision log:** every ability that ever reported charges had
`max = 2` (seven distinct spellIDs). Not one 1-charge ability ever appeared. The CDM's charge
display is **multi-charge only**.

## What Blizzard's Assisted Combat does (asked because of the charge case)

From `raw/addon-research/simc/ActionPriorityLists/assisted_combat/paladin_retribution.simc`:

```
blade_of_justice,if=talent.expurgation&!dot.expurgation.ticking
blade_of_justice,if=holy_power<=3
```

**Nothing about cooldown or charges.** Across all 34 assisted-combat lists the pattern holds:
every *self-referential* cooldown condition is absent. The cooldown conditions that do exist
are about a **different** ability (`pillar_of_frost,if=cooldown.frost_strike.ready` —
alignment), and the only self-referential ones are `charges>=2`, which is **pooling**, not
castability. `conflagrate,if=charges>=2` is literally in that list.

**Implication:** the engine **filters castability before the rules run**, in C, where the
values are not secret. The DBC rules only express what the engine cannot infer.

⚠ `C_AssistedCombat.GetNextCastSpell` is **measured readable in combat**, so that filtered
knowledge is reachable — but it returns **one spell**, the engine's top pick, not a per-spell
castability oracle. It can *falsify* (if the engine filters, it should never return BoJ while
BoJ is down) but cannot directly replace the napkin. **Untested.** And per the plan body,
assisted combat is a *suboptimal rotation* — usable as a castability signal only, never as a
priority source.

## ⚠ THE ARCHITECTURAL FINDING — ✅ FIXED (v0.32.92), history from here down

Three of the five defects (#1's second site, #4, #5) are the same shape: **an ability's facts
were derived through a CDM row's identity rather than asked about the ability itself.**
Defect #5 is the clearest — nothing about "what are Judgment's charges" needs a CDM row, yet
we answered it by resolving a *row's* identity ladder, which pointed at Hammer of Wrath.

The current fixes are **guards against contradictions the data model still permits**. That is
three patches in one bug family in one day.

**This is already scoped**: `roster-state-plan.md` **§6 Phase 5 — "anchor on the roster"**,
marked ▶ CURRENT and "the largest blast radius". Build the domain view from the spec's
declared roster, *joined against* the CDM, instead of from the CDM.

In fairness to the current design, the CDM is **not** purely a display concern: in combat
both `GetSpellCooldown` and `GetSpellCharges` are secret, so the CDM's **alert edges are the
only in-combat readiness sensor**. That justifies the CDM as a *signal source* — not as the
*identity spine*. Conflating the two is the wound.

**RECOMMENDATION.** Before Phase 2, do at least the **narrow version**: read cooldown and
charges **per roster spellID** out of combat, and use the CDM only for (a) the frame join and
(b) the in-combat edges. Much smaller than the full inversion, kills this whole bug class,
and does not touch the knownness question that §6.1 warns is where Phase 5 goes wrong.
Replicating the current model across four more specs would replicate the wound four times —
which is exactly the risk the plan's own gate exists to prevent.

> ✅ **DONE, 2026-08-03, and in the FULL form rather than the narrow one.**
> `roster-state-plan.md` **Phase 5 shipped as v0.32.92**: the spec's declared roster is the
> anchor and the CDM became **one evidence source joined against it**. The root fix is that
> `readAbilityFacts(rid, rep)` passes the **roster** spellID to both `readCd` and `readCharge`,
> so an ability's cooldown and its charges are asked about the **same** id. **Read
> `roster-state-plan.md` §6.3 before touching `State.lua`** — eleven implementation decisions
> there are not in the plan text.
> ⏳ **Code-complete is not flown.** Phase 5's acceptance had exactly one home (a max-level
> Retribution pass) and that home does not exist, which is half of why the gate was inverted
> onto Havoc. Criteria 6–9 of the Havoc flight ARE Phase 5's, carried over verbatim.

## Still open (nothing here is done)

1. **`/cdmp flight` has NEVER been armed on Retribution.** Every `wowkb.cdmp flight` report so
   far is a **stale Destruction capture from 2026-08-02 on v0.32.77**. The acceptance half of
   the gate is entirely unflown. All diagnosis this session came from the *decision log*.
2. **Keybind hints missing on the first two CDM icons — UNDIAGNOSED.** Fix #3 did not resolve
   it. `/cdmp hud layout` reports the **correct** keybind for those rows, so it is either
   (a) `HudBinds.B.map` stale during the fight and refreshed by the time the command ran, or
   (b) the value is correct and is lost downstream in the Binder/Renderer. **The
   discriminator:** run `/cdmp hud layout` *while the hints are visibly missing* and read the
   **`drew=`** column — `key=<x>` + `drew=—` means (b); `key=none` means (a). Note the layout
   is already re-scanned every tick, so "populated once at load" is not the shape.
3. **`w:-` (no winner) in combat rose from 0 % to 13.9 %** on v0.32.90. Partly *correct* —
   before the charge fixes something always looked ready — but it wants watching, especially
   whether L11's filler is being starved.
4. **A max-level Retribution pass**, for the hero-tree branch, the burst lines, and
   observability questions 1 and 5.
5. **The KB write-ups above have not been written.** `api-events-and-discovery.md` §2 still
   carries the standing `@verify-ingame` markers.
6. **Warlock brains still read the legacy `shardCost` seam** — mechanical migration to
   `powerCost` + `CostPowerType`.

## Lessons that generalise to the four remaining specs

- **An oracle authored from the document cannot catch a document that is wrong** — the plan
  already said this. New corollary: **an oracle whose harness stubs the reader cannot catch a
  mis-wired reader.** Prefer driving the *client-level* fake so the shipping ladder runs.
- **A pinned fixture case can encode a misread of its own source.** Check whether the cited
  rule is about *display* or *data* before trusting it.
- **Absent is never zero — and the inverse is just as sharp.** A reader that returns 0 for
  "I could not read it" will eventually be believed.
- **Measure before authoring a constant.** `chargeCD = 12` was wrong by 2 s; one OOC read
  gave the true, haste-scaled number for every ability at once.
- **Two ladders on one row will diverge.** If two facts about one ability are resolved
  through different identity rungs, they *will* disagree, and the disagreement will be silent.

---

# § THE PLAN AS HANDED TO THE SESSION

*Verbatim below, except that the original "START HERE" box (an instruction to ask the user
for in-flight results) has been retired — that flight happened and its results are the
session log above. Where the body conflicts with the session log, **the session log wins.***

## Context — what this is and why

The **Cooldown HUD** (`projects/cooldown-hud/`, addon `michac/CDMProbe`) is a spec-specific
overlay that skins Blizzard's built-in **Cooldown Manager** under Midnight 12.0. It reads
what the client will let it read under Secret Values, decides one "press this now" cue per
tick, and draws its own chrome around Blizzard's untouched icons.

It shipped with **two** registered specs, both Warlock: **Demonology (266)** and
**Destruction (267)**. Every other spec resolves passive by design. The goal of this work is
**seven specs across three classes** — adding **Retribution (70)**, **Havoc (577)**,
**Protection (66)**, **Vengeance (581)** and **Devourer (1480)**.

The pipeline was built for exactly this: `State → Coach → Binder → Renderer` is
spec-agnostic, and a spec is a `Spec<Name>.lua` (data) + `Coach<Name>.lua` (brain) pair that
self-registers into `ns.Specs`. Destruction was added through that seam with no pipeline
edit at all, which was the proof it works.

**What the first non-Warlock spec actually proved.** That "no pipeline edit" rule held for a
second spec *of the same class* and stopped holding at the third. Retribution needed three
pipeline changes — and every one was a **generalisation the seam had been deferring**, not a
special case. The rule is better read as *"a spec adds no pipeline **branch**"*, not *"a spec
adds no pipeline **line**"*. The test is whether the edit is still spec-agnostic when you are
done; all three were.

> ⚠ **The session log adds a fourth and fifth**: the cost seam (`powerCost` /
> `CostPowerType`) and the charge classification (`max >= 1`). Both were likewise
> generalisations, not special cases. Budget for one or two per new class, not zero.

## Where we are

### Shipped and deployed

| | |
|---|---|
| Addon version | **v0.32.91** *(was v0.32.87 when the plan was written)* |
| Tests | **849 passing** / 0 failing / 4 pending *(was 827)* |
| luacheck | **0 warnings** |
| Registered specs | Demonology 266, Destruction 267, **Retribution 70** |

### Phase 0 — the pipeline work (DONE)

- **0.1 `display = "none"` + two bugs beside it.** Added `"none"` to the `resourceDisplay`
  enum (`guidance-contract.json`): a spec can now *track* a resource the HUD does not
  *draw*. Critically this is **not** the same as declaring no powers — an empty
  `spec.powers` emits no `resourceBars[]` entry at all, so `DecisionLog`'s `PW:` column
  would render `?/?` and the one instrument that can explain a decision nobody watched would
  go dark.
  Two real defects fixed while there: `drawResourceRow` tested `display == "continuous"`
  alone, so the contract's own documented `"percentage"` synonym fell through into the pip
  loop; and the pip loop was **unbounded**. Now *only `discrete` draws pips*, with a
  `MAX_PIPS` clamp. **Both mutation-checked.**
- **0.2 `ns.Coach.PowerContext`.** Hoisted the ~15-line power-rail block both Warlock brains
  had copied byte-for-byte. **Both Warlock oracles green *unchanged*** — the success criterion.
- **0.3 The class-resource channel.** `ns.ReadCastCount` / `ns.ReadAuraApplications` /
  `ns.ReadMaxAuraApplications` on the standard guarded ladder, plus a declarative
  `spec.derived` block emitted as `state.derived[name]`. For DH Soul Fragments, which
  `Enum.PowerType` structurally cannot carry. **No consumer yet** — Vengeance and Devourer
  are it. ⚠ **No combat gate, deliberately**: `ReadCharges` carries one because
  `GetSpellCharges` was *measured* secret; copying it pre-emptively would make the
  measurement impossible.
- **0.4 Hero-tree vocabulary.** `HERO_BY_SUBTREE` gained the DH and Paladin trees
  (`TraitSubTree` @ 12.0.7, Tier-1 wago). Nine trees, each pinned by id in a test.

### Phase 1 — Retribution Paladin (DONE, then corrected)

Four docs in `specs/retribution/`, `SpecRetribution.lua` + `CoachRetribution.lua`, and a
**76-case branch oracle** authored from `rotation.md`.

**A KB/APL review then found five real bugs in it**, all fixed and redeployed:

1. **Hammer of Light was L1**, above Execution Sentence and Avenging Wrath. It heads
   `actions.finishers` — but `finishers` is only entered from `actions.generators`, and
   `actions.cooldowns` is called *before* generators. "First in its sub-list" is not
   "first". It is now the **spender choice**, not a line.
2. **Hammer of Wrath sat above Blade of Justice** while `rotation.md`'s own Deviation 5 said
   we were taking the *lower* one. The document was right and the code disagreed with it.
3. **`cost == 0` was treated as a refusal**, so a genuinely *free* finisher was refused at
   low Holy Power. ⚠ **See session-log defect #1** — fixing this exposed the mis-wired reader.
4. **"Six of nine Essential buttons keep their cooldown on a `SpellCategory`" was wrong** —
   it is **four**.
5. **Crusade 1253598 was unregistered.** Also registered: Eternal Flame 156322 and Templar
   Sweep 406661.

**One review finding was rejected with reasons:** it wanted Hammer of Wrath's primary ID
changed to 1241288 because the KB lists it — but the KB marks that row `PASSIVE`; it is the
node that *grants* the ability. 24275 owns the charge category and the cooldown data. Kept.

### What Phase 1 taught (already folded into `docs/adding-a-spec.md`)

- **The recipe had seven stale claims.** `adding-a-spec.md` now opens with a CORRECTIONS box.
- **`SpellName` is full of homonyms.** Eight spells are called "Hammer of Light". Resolve a
  name by a **property only the real spell has** — a Holy Power cost in `SpellPower`, a
  shared `ChargeCategory` — never by picking the plausible-looking number.
- **Read the APL's call structure, not its text order.** Both ordering bugs came from this.
- **Check `SpellCategories.ChargeCategory` for every rotation button during Step 0.**
- **An oracle authored from the document cannot catch a document that is wrong.**

### The charge-category story, stated correctly

- Four Retribution Essential buttons (Judgment, Crusader Strike, Blade of Justice, Wake of
  Ashes) have `SpellCooldowns.RecoveryTime = 0` and keep their cooldown on a **charge
  category**, so `ns.BaseCooldown` reads 0 and `HudNapkin` has nothing to count down from.
- **Readiness is unaffected.** It comes from the **charge count**. ⚠ **The session log
  qualifies this heavily** — it was only true for *multi-charge* pools; the 1-charge ones
  had no count at all until v0.32.90, and defect #4 is the result.
- **What is genuinely lost is `SOON` and `Escalate`'s overdue signal.** Decoration, not presses.
- A charged ability raises `Available` on every charge restore and **never** `OnCooldown`, so
  the ready-edge latches true forever. That is why `usable()` makes **the count outrank the
  cooldown read** — a live pass once had the HUD cueing Conflagrate at zero charges on 190 of
  194 log lines. ⚠ **Qualified by defect #5**: for a *1-charge* pool the count and the
  cooldown are the same fact and must agree.

### Also open, but not blocking (filed to `docs/status.md` → backlog)

- **📋 The napkin cannot count down a charge-category cooldown.** ✅ **Addressed** in
  v0.32.89 (declared fallback) and superseded by v0.32.90's measured recharge.
- **📋 `coach_destruction_apl_spec` never wires the cost reader**, so Destruction's
  "resolved live, never hardcoded" rule is currently unasserted. **Still open.**
- **📋 Pre-existing**: partial-shard pip rendering, "a cast in flight should put its own
  ability on cooldown", the `C_AssistedCombat` oracle's usefulness, `roster-state-plan.md`
  Phase 5, and the blocked v0.32.36 re-fly.

## The Retribution gate — the procedure

```bash
# in game, on a Retribution Paladin
/reload
/cdmp hud status       # expect: spec: Retribution (profile active)
/cdmp hud layout       # live tracked icons + resolved keybinds
/cdmp hud coverage     # expect: no BLIND rows
/cdmp flight           # arms the recorder — then just play
#   ... pull a target dummy for a minute, single-target AND /cdmp aoe ...
#   ... respec away and back, to prove the active/passive toggle ...
/reload                # ⚠ SavedVariables only flush here
```
```bash
cd ~/code/fun/hud-classes/tools
uv run python -m wowkb.cdmp flight        # PASS / FAIL / MEASURED
uv run python -m wowkb.cdmp decisionlog   # then grep the trace
```

⚠ **Exit code 2 from `wowkb.cdmp flight` means "no failures, but part of it was never
flown" — that is not a pass.** In the decision log, grep for `w:-` (Coach found no winner)
and `×` (Binder dropped a cue), and read the **COMBAT SPLIT**, not the raw ratio.

### Where to look first, by symptom

| Symptom | Most likely cause | Instrument |
|---|---|---|
| HUD passive / no profile | spec resolution | `hud status` |
| An ability never lights | not in the CDM tracked set, or `BLIND` | `hud coverage`, `hud layout` |
| **Hammer of Wrath never lights** | expected-ish — no tracked row; needs a virtual row | `hud coverage` |
| A cue for a button that cannot be pressed | the charged-ability trap | decision log `CH:` field |
| `w:-` a lot in combat | no line matched — check `PW:` | decision log COMBAT SPLIT |
| Cue order feels wrong | the L1–L11 cascade vs `rotation.md` | `CoachRetribution.lua`'s `-- Ln` comments |
| `PW:` shows `?/?` | the `display = "none"` rail is broken | decision log |

### The six questions the pass must settle

| # | Question | Status after 2026-08-03 |
|---|---|---|
| 1 | **Does Hammer of Wrath get a virtual icon?** | ⏳ **Unanswered** — needs a max-level pass. |
| 2 | **Is a 1-charge charge category marked `charges = true`** on the CDM row? | ✅ **ANSWERED — NO.** The CDM's charge display is multi-charge only (all 7 observed rows had `max=2`). But `C_Spell.GetSpellCharges` **does** answer `1/1`, which is what defect #4 now uses. |
| 3 | **Which Hammer of Wrath ID does the client surface?** | ✅ **24275** — it appears in the tracked set as `HoW`, alternating with Judgment. |
| 4 | **Which spender frame carries the Hammer of Light override?** | ⏳ Unanswered (Templar unavailable at level 37). |
| 5 | **Is `RET_HOL_FROM_BUFF` safe to enable?** | Already answered **NO** by measurement — Light's Deliverance is a 60-stack buff, present nearly the whole fight, secret in combat. Expect to **delete the switch**. |
| 6 | **Does the DB2-predicted tracked set match what loads?** | ⚠ **Partly — and it is NOT STATIC.** The tracked set *alternates* (`…,FV,Judg` ↔ `…,FV,HoW`) as row identity flips. This is the root of defect #5. |

## After the gate — the four remaining specs

> ✅ **RESOLVED 2026-08-03: Phase 2 is HAVOC, and it has shipped.** The user chose it over
> Protection so the gate could be discharged from the Demon Hunter side (they have a
> max-level DH and no max-level Paladin). The roster-anchor work the session log asked for
> **landed first**, as v0.32.92.
>
> ⚠ **Phases 3–5 are now blocked behind the HAVOC flight**, on the same reasoning the
> original gate used: do not clone an unflown pattern four more times.

| # | Spec | ID | Resources | Why it sits here |
|---|---|---|---|---|
| 2 | ✅ **Havoc DH** | 577 | Fury 0–**170** (**SECRET**) | **SHIPPED 2026-08-03; FLOWN AND FAILED the same day; Phase-1 remediation shipped; ⏳ RE-FLY outstanding.** Its four surprises: three lying cooldowns, three CDM-Utility presses, the wrapper-spell aliases — and **Fury being unreadable**, which is § FLIGHT RECORD. |
| 3 | **Protection Paladin** | 66 | Holy Power 0–5 (✅ never secret) | **First tank.** Reuses everything from Retribution. Charge-heavy (Shield of the Righteous). **The only remaining spec whose resource thresholds work.** |
| 4 | **Vengeance DH** | 581 | **Fury (SECRET)** + Soul Fragments | ⚠ **INHERITS EVERY WORD OF PHASE 1** — no `fury>=N` gate can be written. **First consumer of the Phase-0.3 derived channel** (Soul Fragments ride `GetSpellCastCount`, which is a different and still-readable channel). Largest APL (275 lines). |
| 5 | **Devourer DH** | 1480 | **Fury (SECRET)** + Souls (aura stacks) | ⚠ Same inheritance. New spec, and a resource that changes which aura it lives on. ⚠ **Expect to descope.** |

### Data sources (all on disk, all Tier 1)

The simc clone is in the **sibling `wow` worktree**:
`/home/mchristiansen/code/fun/wow/raw/addon-research/simc` — branch `midnight`, commit
`ab7b0b8`, **2026-08-01**. Alongside it: `wow-ui-source`, `BlizzardInterfaceResources`
(12.0.7 build 68256), `WeakAuras2`.

| Spec | APL file | Lines |
|---|---|---|
| Havoc | `demonhunter_havoc.simc` | 140 |
| Vengeance | `demonhunter_vengeance.simc` | 275 |
| Devourer | `demonhunter_devourer.simc` | 86 |
| Retribution | `paladin_retribution.simc` | 54 |
| Protection | `paladin_protection.simc` | 44 |

> **⚠ Do NOT use `ActionPriorityLists/assisted_combat/` as a rotation baseline.** It is
> Blizzard's one-button rotation and is **suboptimal**. *(The session log adds: it is
> nonetheless a useful window into what the engine filters vs. expresses.)*

### The three things Phase 1 says to do differently

0. ⚠ **ASK WHETHER THE SPEC'S RESOURCE IS SECRET, FIRST — before the DB2 sweep and before a
   line of `rotation.md`.** `C_Secrets.GetPowerTypeSecrecy(<Enum.PowerType>)`: **0** =
   `NeverSecret` (thresholds work), **2** = `ContextuallySecret` (for a player's own primary
   resource that means **secret forever** — there is no out-of-combat window). The seven
   never-secret types are Combo Points, Runes, Soul Shards, Holy Power, Chi, Arcane Charges
   and Essence; **everything else is secret**. A primary-resource spec cannot use
   resource-threshold gates **at all**, which changes the rotation model rather than being a
   detail to degrade later — see § FLIGHT RECORD — PHASE 2. ⚠ And the `SpellPower` sweep in
   step 1 becomes **informational only** for such a spec: there is nothing to compare a cost
   against, and **DB2 costs disagree with the live client anyway** (DB2 says Throw Glaive
   costs 25; the client reports it free).

1. **Do the DB2 sweep as one step, before writing any doc.** For every Essential ability:
   `SpellCooldowns.RecoveryTime`, `SpellCategories.ChargeCategory` (+ `MaxCharges` /
   `ChargeRecoveryTime`), and `SpellPower` for the spenders. And for every TrackedBuff:
   **`SpellAuraOptions.CumulativeAura`**.
   > ⚠ **Session-log addition: also take one OOC `C_Spell.GetSpellCharges` sweep in game.**
   > It gives the charge/no-charge split *and* haste-scaled recharge times in one pass, and
   > it caught a wrong authored constant that DB2 alone did not.
2. **Diff the APL's action list against the tracked set before designing the cascade.**
3. **Read the APL's *call structure*, not its text order.**

### Devourer — measure first, then decide (user's call, 2026-08-03)

Before writing any Devourer code, confirm in game whether
`ns.ReadAuraApplications(1225789)` (Dark Heart) returns a number or refuses. The reader
already ships, so this is a single flight.

- **If it reads** — build Devourer fully.
- **If it refuses** — descope to a **presence-gated** profile (the Backdraft precedent).
  Devourer's whole gameplan is "bank Souls, then transform", so a refused read is a genuinely
  smaller spec — not a reason to fabricate a count.

⚠ The KB records `knowledge/addon-dev/cooldown-manager.md:517` — the **entire `AuraData`
record is secret when restricted**, *"including `GetPlayerAuraBySpellID`"*. So expect a
refusal. **Vengeance's flight de-risks this for free** if it comes first: its
`GetSpellCastCount` read is a different, more promising API.

## The per-spec recipe (identical each phase) — THE WORKING CHECKLIST

1. **`specs/<spec>/` — four docs**, cloning `specs/destruction/` (the better template).
   - `rotation.md` — the flat priority list, numbered `L1…Ln`, distilled from the default
     APL. Every departure from simc's order goes under **Deviations** with a rationale.
     Hero-tree differences are a **delta section**, never a second list.
   - `notes.md` — ability roster, procs, resource mechanics, blind spots.
   - `input-contract.md` / `observability-map.md` — the evaluator's inputs, and the
     readability triage, as a desk exercise against a concrete APL.
2. **`Spec<Name>.lua`** — clone `SpecDestruction.lua`, not Demonology. Fill `SpecIDs`
   (Tier-1, **never guessed**), `powers` (`display = "none"`), `log`, the `Spec` signal
   bucket, `SpecInfo` + `SpecPowerDelta`, optional `SpecBindAlias`. `ns.RegisterSpec(<id>,
   spec)` at the bottom; **never** `SetActiveSpec`.
3. **`Coach<Name>.lua`** — `Context` / `RankWinner` / `Escalate` on `ns.Specs[<id>]`.
   `RankWinner` is a flat cascade whose `-- Ln` comments are the doc's line numbers. Honour
   `excluded` at **every** line naming an ability.
4. **`.toc`** — data then brain, after `SpecRegistry.lua`, before `Coach.lua`.
5. **Branch oracle** `tests/spec/coach_<spec>_apl_spec.lua`, authored **from `rotation.md`,
   never from `RankWinner`**. ~250 lines fixed + 3–5 per case; 40–70 cases for a Paladin.
   > ⚠ **Session-log addition:** wire the **real** readers (`powerCost = ns.PowerCost`) and
   > drive **client-level** fakes. A harness that stubs the reader cannot catch a mis-wired one.
6. **Gates**: `luacheck CDMProbe/` + `busted CDMProbe/tests/spec` — both **hard release gates**.

### Patterns to clone rather than re-derive

- **`usable()` — the charge rule** (`CoachDestruction.lua:327-348`). The CDM raises
  `Available` on every charge restore and **never** `OnCooldown`, so `cd` reads ready forever.
  **The count outranks the cooldown read.** ⚠ **Except for a 1-charge pool** — see defect #5.
- **Hero trees resolved independently of the tracked set** (`state.hero` from the talent API
  first, inference only as fallback).
- **The `spec.X = false` parked switch** for a genuinely unsettled read. Expect ~one per spec.
- **`expect = false`** on alias/override-only entries — load-bearing. `State.lua:1587-1604`
  auto-promotes an untracked `kind="button"` ability to a self-drawn virtual icon; an alias
  passing those fences draws a duplicate.

## Verification

**Offline, every phase** (from `projects/cooldown-hud/addon/`):

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck CDMProbe/ && busted CDMProbe/tests/spec
```

**Both are hard release gates** — `wowkb.addon release` aborts the cut on a non-zero exit.
Baselines: 706 before this work, **849 now**.

**Regression guard for the whole rollout:** the two Warlock oracles (`coach_apl_spec`,
`coach_destruction_apl_spec`) must stay green **unchanged** through every phase. They remain
the cheapest signal that a "generic" edit was actually generic. *(Held through all five
2026-08-03 fixes.)*

**In game, every phase**: auto-deploy is sanctioned for this project — cut and deploy, no ask.

## Out of scope

A dedicated defensive/mitigation cue channel for the two tanks, the continuous/partial-fill
resource renderer, retiring the Warlock shard bar, and the 7 healer specs.

---

# § APPENDIX — per-spec DB2 brief for the four remaining specs

> **Provenance:** a research pass run 2026-08-03 against `raw/wago/*.csv` @ 12.0.7 (Tier-1
> DB2), the four simc APLs, and `knowledge/classes/`. **Desk-derived, not flown.** Treat as a
> head start on the recipe's Step 0, not as verified fact — and re-run the OOC
> `GetSpellCharges` sweep in game per the session log.
>
> CooldownSet IDs: Havoc **1599**, ProtPal **637**, Vengeance **565**, Devourer **1864**.
> Retribution (spec 70, set 901) is the baseline: 9 Essential / 15 Utility / 31 TrackedBuff.

## ⚠ The finding that cuts across all four — read first

**`CooldownSetSpell` TrackedBuff rows frequently carry the *talent* spell ID, not the *aura*
spell ID.** `SpellAuraOptions.CumulativeAura` on the tracked ID then reads 0 or is absent
while the real aura stacks. Verified pairs include:

| Tracked row (in CDM) | cum | Real aura | cum |
|---|---:|---|---:|
| Light's Deliverance 425518 | 0 | 433674 | **60** |
| Shining Light 321136 | 0 | 182104 | **4** |
| Divine Guidance 433106 | *(no row)* | 460822 | **5** |
| Art of the Glaive 442290 | 0 | 444661 | **80** |
| Frailty 389958 | *(no row)* | 1241917/1241946 | **99** |
| Demonsurge 452402 | 0 | 452416 / 453323 | 4–5 |

TrackedBuff rows with **no `SpellAuraOptions` row at all**: Havoc 16/31, Vengeance 19/32,
Devourer 15/34, ProtPal 14/43. The APLs read `.stack` on ~8 different buffs across the DH
specs, so **this resolution step must be made explicit before it is trusted.**

## Summary table

| | Havoc 577 | ProtPal 66 | Vengeance 581 | Devourer 1480 | *(Ret 70)* |
|---|---:|---:|---:|---:|---:|
| Essential | 10 | 11 | 13 | **6** | 9 |
| Charge-cat hole (rec=0 & cc≠0) | 2 | 3 | **6** | 3 | 4 |
| …incl. *lying* base CDs | **+3** (Fel Rush 1 s→10 s, Immolation Aura 2 s→30 s, Vengeful Retreat 0.5 s→25 s) ⚠ *this row said "+1 (Fel Rush)" until Phase 2 measured it* | +1 (**GotAK 8 s→180 s**) | +2 (Demon Spikes, **Meta 1 s→120 s**) | +2 (no CD at all) | 0 |
| Essential with **no** readable CD | 3/10 | 4/11 | **8/13** | **5/6** | 4/9 |
| Rotation abilities with no icon | **6 override + 3 Utility** ⚠ *"3 override + 2 Utility" until Phase 2 — Fel Rush is the third Utility (and carries TWO rows)* | **2 homeless** + 2 override | 1 override + 3 Utility | **6 homeless** + 3 override | 2 homeless + 5 override |
| Key stacking buff | *(all behind talent IDs)* | Masterwork 6 | **Soul Fragments 20** | **Void Meta 50, Collapsing Star 40** | Light's Deliverance 60 |
| APL lines / variables / sub-lists | 140 / 24 / 3 | **44 / 0 / 1** | **275 / 65 / 15** | 86 / 23 / 5 | — |
| Hero trees | Fel-Scarred **34 (default)**, Aldrachi Reaver 35 | Templar 48 (raid), Lightsmith 49 (M+) | Aldrachi Reaver 35, Annihilator **124** | Annihilator **124**, Void-Scarred 126 |

## Per-spec headlines

**Havoc 577** — ✅ **SHIPPED (Phase 2, 2026-08-03).** ⚠ **This paragraph was the pre-build
estimate and Phase 2 corrected three of its four claims — the corrected version is
`specs/havoc/notes.md`; the ⚠ CORRECTIONS list in § SESSION LOG — PHASE 2 is the diff.**
What survived: `run_action_list,name=meta` *is* a hard state fork in simc, and **Rain from
Above 206803 never appears in the APL** (shipped as a knowingly dead Essential icon —
registered so Coverage does not report it blind, `cadence = "utility"` so SOON never
advertises it). What was wrong: the fork did **not** need two priority lists (both overrides
are 1:1 display overrides on their own base's frame, so it is **one cascade, two `ctx.inMeta`
lines**); it is **three** Utility presses, not two (**Fel Rush 195072** as well, with two CDM
rows), and scoring them needed **no pipeline edit** because the fences read the
spec-authored `cadence`; and there are **three** lying base cooldowns, not one — but all three
are 1-charge categories, so the charge count vetoes the early read and only the *decoration*
lies.

**Protection Paladin 66** — roughly Retribution's difficulty; **simplest APL of all four**
(44 lines, **zero** variables, zero sub-lists). Same Holy Power rail, same 3-cost spenders,
same Hammer-of-Light homonym (already solved). Three sharper edges: **Guardian of Ancient
Kings 86659 reports `RecoveryTime = 8000` against a real 180 000 ms** — the largest lying
cooldown in the set; **Crusader Strike 35395 never appears in the APL by name** (pressed only
through Blessed Hammer / Hammer of the Righteous, each with a *different* charge count than
the frame's own category); and **Hammer of Wrath 24275 is a top-3 builder with zero presence
in the CDM set**. ⚠ The KB warns the Prot APL **is not in the .simc file** — it lives in
`sc_paladin.cpp`'s `apl_protection`, and the 44-line file is a stub.

**Vengeance 581** — substantially harder. 275 lines, 65 variables, 15 sub-lists, and a
top-level **hero fork into two disjoint rotations** (`ar` / `anni`). **6 (de-facto 8) of 13
Essential buttons have no usable base cooldown**; Metamorphosis 187827 reports 1 s against a
real 120 000 ms. `variable.fragment_target` is a **moving** threshold (5 / 3 in Fiery Demise /
4 in Meta, −1 in AoE) on a 20-stack buff. Mitigating: the **best icon coverage of the four** —
12 of 13 Essential icons are actually pressed.

**Devourer 1480** — hardest, and different in kind. Only **6 Essential buttons, 5 with no
readable cooldown** (3 charge-category, 2 with *no* cooldown in DB2 at all — Void Ray and
Void Metamorphosis). **6 rotation abilities are genuinely homeless**, including the primary
filler (`consume`) and the primary payoff (`collapsing_star` 1221167). ⚠ **`consume` and
`devour` cannot be identified from DB2 by name** — 35 and 65 homonyms respectively, no
`SkillLineAbility` coverage for Devourer, and neither is in `talents.json` (they are
baseline). Retribution's Hammer-of-Light homonym was resolved by a `SpellPower` signature;
these have no such property. ⚠ **A Tier-1 conflict to resolve:** simc's
`collapsing_star_stacking` caps at **30**, DB2 says **40**. Also: Fury *drains* in Void
Metamorphosis at a rate DB2 does not represent at all. The KB flags Devourer
`confidence: medium` with **no Warcraft Logs history** and several open `@verify-ingame`
markers.

**Implementation order implied by this data:** ProtPal → Havoc → Vengeance → Devourer.
*(Note this differs from the plan body's risk ordering, which put Havoc first. The plan body
is the user's call; this row is only what the DB2 complexity suggests.)*

⚠ **SUPERSEDED 2026-08-03: Havoc went first**, and the reason had nothing to do with DB2
complexity — it is the only remaining spec on a class where the player has a **max-level
character**, which is what the gate needs. Remaining order: **ProtPal → Vengeance →
Devourer**, all behind the Havoc flight. And Havoc's complexity read **lower** than this
appendix estimated once it was built: the meta fork collapsed to one cascade, and the
CDM-Utility problem dissolved entirely.

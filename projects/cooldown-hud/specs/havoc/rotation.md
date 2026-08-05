# Havoc Demon Hunter — rotation priority list (APL)

This is the **spec of record** for the Havoc rotation as a flat, ordered **action
priority list**. It is evaluated top to bottom; the **first line whose action is
castable is the press**. Every line carries an implicit gate: *"the ability is
usable"* — off cooldown, charged, and **reported affordable by the client**.

> **⚠ STATUS: FLOWN TWICE 2026-08-03. The first pass FAILED; this document is the
> remediation (Phase 1), and it then FLEW CLEAN on v0.32.94** — Chaos Strike + Annihilation
> the top winner at 35.4 %, `PW:restricted` on all 1298 lines, and Eye Beam / Blade Dance /
> Metamorphosis all cueing after zero. A third flight is owed for v0.32.95 (L12's charge-cap
> gate, `ctx.ampWindow`, the look-ahead) and for the AoE and Essence Break paths, which
> neither flight exercised. Distilled from the Tier-1 simc midnight APL
> (`raw/addon-research/simc/ActionPriorityLists/default/demonhunter_havoc.simc`, 140
> lines, commit `ab7b0b8` 2026-08-01) with `knowledge/classes/demon-hunter/havoc/`
> (**confidence: high**, Tier-1 sourced) for corroboration. Every departure from the
> simc order is called out under **Deviations** — those are the lines to adjudicate.
>
> **What the FIRST flight found, in one sentence: `UnitPower("player", Fury)` returns a
> Secret Value, so every Fury-threshold gate in this list was comparing against a
> fabricated zero.** 2380 decision-log lines, 2374 of them in combat, `PW:0/+0` on all
> of them. Chaos Strike, Eye Beam, Blade Dance and Metamorphosis won **zero** times
> between them; Throw Glaive won 770 and Vengeful Retreat 480. The whole core rotation
> was structurally unreachable. See `docs/multi-class-rollout.md` → *Phase 2 flight
> record* for the full winner distribution.
>
> **Fury is the Demon Hunter's PRIMARY resource, and primary resources are always
> secret** — there is no out-of-combat window and no seed value, ever. See *Fury is
> secret* below. So the resource-threshold gates this list was originally written
> around are not merely degraded, they are **unimplementable**, and this revision
> replaces them with the client's own per-spell affordability verdict.
>
> **This list SHIPS**: `CoachHavoc.lua` implements L1–L15 line-for-line (the line
> numbers below are its `-- Ln` comment labels, so the two diff by eye), and
> `tests/spec/coach_havoc_apl_spec.lua` is the independent oracle that pins the code
> to *this document*. A change here is a change to the addon — edit the list, then the
> brain, then the oracle.
>
> **⚠ THE HAVOC IN-GAME PASS IS A HARD DELIVERABLE, NOT A SMOKE TEST**, and it is now
> a **re-fly**. Retribution (the pattern this spec clones) has never been flown at max
> level and cannot be — the player has no max-level Paladin. The Havoc flight therefore
> does double duty: it is Havoc's own acceptance *and* the pattern-verification flight
> Retribution's was meant to be, including `roster-state-plan.md` Phase 5's criteria.
> See `observability-map.md` → *The flight's job*.

> **v1 profile: Fel-Scarred.** simc's default profile is Fel-Scarred
> (`talents=…Fel-Scarred`) and the KB calls it "the recommended S1 pick for nearly all
> content". The **Aldrachi Reaver delta** is a section at the bottom, not a second
> list. ⚠ That delta is unusually thin, and for a **data** reason rather than a
> priority reason — see it.

## How to read it

- **`affordable`** means **the client says so**: `C_Spell.IsSpellUsable(id)`'s second
  return, `insufficientPower`, is false. It is **not** a Fury comparison — no line in
  this list may compare a Fury number, because there is no readable Fury number. See
  *Fury is secret* below.
- **Implicit gate on every line:** the named ability is only a candidate if it is
  usable right now. A line whose ability is not usable is skipped and evaluation
  continues.
- **`[META]` / `[NO META]`** marks the two lines the demon-form fork moves. Everything
  else is shared — see *The metamorphosis fork* below.
- **Abbreviations:** CS = Chaos Strike (→ **Annihilation** in meta), BD = Blade Dance
  (→ **Death Sweep** in meta), EB = Eye Beam (→ **Abyssal Gaze** on Fel-Scarred with
  Demonic Intensity), IA = Immolation Aura (→ **Consuming Fire**), TG = Throw Glaive
  (→ **Reaver's Glaive** on Aldrachi Reaver), FB = Felblade, VR = Vengeful Retreat,
  FR = Fel Rush, EssB = Essence Break, Meta = Metamorphosis.

## Fury is SECRET — the resource difference from every spec shipped so far

**This is the single most important fact about this spec, and it is a fact about the
game, not about Havoc.** `UnitPower("player", Enum.PowerType.Fury)` returns a **Secret
Value**. The HUD cannot read the number, cannot compare it, and — critically — cannot
ever read it, in a city or mid-pull.

Secrecy is **per power type**, and the rule is **primary vs. secondary resource**
(Blizzard blue post, *Midnight Public Alpha Addon API Changes*, 2025-11-24):

> "We have relaxed restrictions around `UnitPower` so the player's **secondary**
> resources are no longer secret (**primary resources remain secret**). Affected
> resources: Combo Points, Runes, Soul Shards, Holy Power, Chi, Arcane Charges,
> Essence."

Fury is the Demon Hunter's **primary** resource. Measured in game 2026-08-03:

| probe | Fury (17) | Holy Power (9), the control |
|---|---|---|
| `C_Secrets.GetPowerTypeSecrecy` | **2** (`ContextuallySecret`) | **0** (`NeverSecret`) |
| `C_Secrets.ShouldUnitPowerBeSecret("player", …)` | **true**, in a city *and* mid-pull | false |

⚠ **The "context" in `ContextuallySecret` is the UNIT, not combat.** The predicate is
`SecretWhenUnitPowerRestricted`, whose documentation reads *"…unless the subject unit
does not have a power of this type."* You always have Fury, so it is always secret.
**There is no out-of-combat window and no seed value.** Do not go looking for one.

`UnitPowerMax` is a **different predicate** (`SecretWhenUnitPowerMaxRestricted`, which
only applies to units that are not player-controlled), so **the max is readable** — and
it measured **170** on the test character, not the 120 this spec used to declare.

**The first four specs shipped were lucky, not right.** Soul Shards ×2 and Holy Power ×1
are all on the never-secret list. Rage, Energy, Focus, Mana, Insanity, Maelstrom, Runic
Power, Pain and Fury are not — so **most specs in the game behave like Havoc**. Of the
remaining rollout, Protection Paladin is Holy Power (safe) and **Vengeance and Devourer
are both Fury** and inherit every word of this.

### What replaces the number: read the verdict, not the resource

`C_Spell.IsSpellUsable(spellID) -> isUsable, insufficientPower`. It carries
`SecretArguments = "AllowedWhenTainted"` and — decisively — **no `SecretReturns` and no
`SecretWhen*` predicate at all** (T1: `SpellDocumentation.lua:873-888` @ 12.0.7.68887),
so both returns are plain booleans from a tainted caller. `insufficientPower` is
documented as *"True if spell is specifically unusable due to insufficient power (ie
MANA, RAGE, etc)"*. This is the same shape the pipeline already uses for cooldowns
(`GetSpellCooldownDuration` → an opaque duration object): **Blizzard answers the
question, we never see the input.**

Measured in game, **one sample, at low Fury**:

| spell | `isUsable` | `insufficientPower` |
|---|---|---|
| Throw Glaive 185123 | true | **false** |
| Eye Beam 198013 | false | **true** |
| Blade Dance 188499 | false | **true** |
| Chaos Strike 162794 | false | **true** |

Three spells reporting insufficient power while a fourth in the **same sample** reports
fine is the proof the flag is computed **per spell against its own cost**. At high Fury
all four read `true / false`.

⚠ **Two traps in that data, and both have already cost this project a flight.**

1. **Use `insufficientPower`, NOT `isUsable`.** The Retribution flight measured
   `isUsable` returning **true while a spell was visibly on cooldown** — it answers
   *"can I afford it"*, not *"can I cast it"*. Readiness still comes from the CDM
   edges / the napkin / the charge count, exactly as before.
2. **Throw Glaive is FREE per the live client.** It reported `insufficientPower = false`
   at a Fury level where everything else failed. The old `GLAIVE_COST_FALLBACK = 25`
   (from DB2 `SpellPower`) is **wrong against the live client**, and that is precisely
   why L15 won 770 times in the failed flight — a cost of 0 compared against a
   fabricated Fury of 0 passes. **DB2 costs are not the client's costs.** The four
   `*_COST_FALLBACK` constants are deleted rather than corrected; a cost this list can
   no longer compare against anything has no reason to exist.

### What this costs, knowingly — and why it costs far less than it looks

`IsSpellUsable` is **binary**. It is false at 40 Fury and at 170 alike, so **overcap
avoidance is unrecoverable through it**: Havoc will overcap Fury and the HUD will not warn.

**⚠ MEASURED 2026-08-03, AND IT DOWNGRADES THIS FROM A REGRESSION TO A NON-ISSUE.** Fury
overcap in the top-100 Mythic parses on Imperator Averzian (WCL, 12.0.7, `resourcechange`
events — `waste` against `resourceChange`, `resourceChangeType 17`):

| player | Fury gained | wasted | waste |
|---|---:|---:|---:|
| Paprzdh | 4,119 | 311 | 7.6 % |
| Yunadh | 4,345 | 482 | 11.1 % |
| Bibussy | 5,612 | 708 | 12.6 % |
| Chezzar | 5,386 | 1,237 | 23.0 % |
| **pooled** | **19,462** | **2,738** | **14.1 %** |

**The best Havoc players in the world throw away one Fury in seven.** The dominant waste
source is **Demon Blades** — a *passive* that procs off autoattacks and cannot be gated by
any rotation decision — with Immolation Aura's ticks second. That is why the guides are
quiet about Fury: maxroll's only Fury sentence for this spec is *"Cast Immolation Aura if
you won't overcap on fury"* (`maxroll-raid.md:209`). **One line, about one button.**

So the thing Phase 1 gives up is a discipline top parses demonstrably do not practise, and
the one *controllable* piece of it — Immolation Aura — is recovered by **L12's charge-cap
gate**, which is fully readable. ⚠ **`docs/multi-class-rollout.md`'s Phase 2 (the
two-branch `LuaCurveObject` cascade) is therefore RECOMMENDED AGAINST**: it is elaborate
machinery, with a permanent decision-log blind spot, to recover a behaviour worth ~14 % of a
resource nobody optimises. **Essence Break's pooling gate (Deviation 13) is the only Fury
loss still worth calling real**, and it is one line rather than an architecture. **Blizzard's own
rotation accepts the same loss**: the in-client Assisted Combat list
(`ActionPriorityLists/assisted_combat/demonhunter_havoc.simc`) contains **zero** Fury
references and handles the resource purely by ordering and repetition —

```
chaos_strike,if=buff.metamorphosis.up
felblade                              <- bare, no deficit gate
chaos_strike                          <- again
immolation_aura,if=active_enemies>1   <- enemy count only, no deficit gate
throw_glaive
chaos_strike                          <- and again, as the floor
```

⚠ **Do not over-read that as "Blizzard avoids secret resources."** Their other
assisted-combat lists branch on energy / rage / focus / runic_power freely — that engine
runs in C and sees everything. The finding is narrower and still load-bearing: **a
competent Havoc rotation is expressible with no Fury threshold at all**, with the
spender appearing at several priorities and simply falling through when unaffordable.
That is the shape L11–L15 now take.

### The rail still exists, and it now says so honestly

**The bar is deliberately not drawn** (`display = "none"`). Blizzard's own Fury bar is
right there under the player frame, and the project's stance is enhance-don't-replace.
The resource still rides the whole rail (`ctx.powers` → `resourceBars[]` → the decision
log's `PW:` column) — `none` turns off exactly one thing, pixels. ⚠ It is **not** the
same as declaring no powers: an empty `spec.powers` emits no bar and `PW:` renders
`?/?`, losing the one instrument that can explain a decision nobody watched.

⚠ **Do not reach for `continuous`.** Its pixel path is a declared stub that draws
nothing, and `discrete` clamps at `MAX_PIPS = 12` — a 170-max Fury bar would render
meaningless. `none` is the correct member and the reason it was added.

**`PW:` now reads `restricted`, and it must never read `0`.** The failed flight's
`PW:0/+0` was two coercions (`Coach:ResourceBars`' `value = p.value or 0` and the
brain's `ctx.fury or 0`) turning *"we could not read it"* into *"you have zero"* — the
project's own **absent-is-never-zero** rule broken in the one place nothing tested. Zero
Fury is the worst possible degradation: every spender is unaffordable and every
generator is maximally urgent, which is exactly the winner distribution the flight
produced. Both coercions are gone, `State.readOnePower` now asks
`C_Secrets.ShouldUnitPowerBeSecret` and marks a structurally-unreadable rail
`restricted`, and the decision log renders that word.

## The metamorphosis fork — one cascade, two lines

simc's top-level list ends with `run_action_list,name=meta,if=buff.metamorphosis.up`
(:82), a **hard fork** into a second complete priority list (`actions.meta`, :118–140)
that never returns. Two full lists where the same buttons mean different things.

**The HUD does not need two cascades, and modelling it as two would be wrong.** The
demon-form transformation is a **display override on the same tracked frames**:

| Frame (base spellID) | Out of meta | In meta | granted by |
|---|---|---|---|
| 162794 | Chaos Strike | **Annihilation** 201427 | Metamorphosis 162264 |
| 188499 | Blade Dance | **Death Sweep** 210152 | Metamorphosis 162264 |

That is the same channel Demonology's Demonic Art and Retribution's Hammer of Light
ride — `liveSpellID ~= base`, readable in restricted combat. The Coach cues the **base
spellID**; the Binder resolves it to the frame; the icon already shows the right art.
So a "second list" would be fifteen duplicated lines whose only difference is a label
the pipeline supplies for free.

**What the fork genuinely changes is ORDER, in exactly two places**, and those are the
only lines carrying a `[META]` / `[NO META]` marker:

1. **Essence Break is meta-only.** In this APL revision the top-level `essence_break`
   line at :87 is **commented out** — the whole `actions+=/essence_break,…` sits inside
   a `#` comment. It survives only in `actions.meta` (:121). This is a fact about the
   APL text, not an inference; see Deviation 3.
2. **Blade Dance outranks Eye Beam in meta, and not outside it.** Out of meta:
   `eye_beam` :86 above `blade_dance` :88. In meta: `death_sweep` at :118 / :122 /
   :130, `eye_beam` at :129 — i.e. two Death Sweep lines above Eye Beam.

`ctx.inMeta` is read from **two ORed sources**, both readable in combat:
- the Metamorphosis **TrackedBuff** row (191427) reporting `IsActive()`, and
- **either** meta override visibly live on its base frame — Chaos Strike showing
  Annihilation *or* Blade Dance showing Death Sweep. Metamorphosis 162264 grants both, so
  demon form always transforms both frames and seeing either is sufficient.

⚠ 191427 is the **cast** id; the aura that actually grants the overrides is 162264, which
the CDM does not track — so source 1 is the row we have, not the aura we would pick. That
is precisely why there are two. Either alone is sufficient; ORing costs nothing and covers
a build or a row that surfaces only one. The brain checks the two frames **explicitly**
rather than walking `factsByBase`, so the answer cannot depend on `pairs` order.

## The priority list (as derived)

```
L1   if the Throw Glaive frame shows Reaver's Glaive:      cast Reaver's Glaive
L2   if Meta usable and Inner Demon down:                  cast Metamorphosis
L3   if The Hunt usable and no Essence Break window
        and no Reaver's Glaive armed:                      cast The Hunt
L4   if AoE and Immolation Aura usable:                    cast IA
L5   if VR usable and Eye Beam is within ~1 GCD
        and Initiative is down:                            cast Vengeful Retreat
L6   [META] if Essence Break usable:                       cast Essence Break
L7   [META] if Blade Dance usable and affordable:          cast BD  (-> Death Sweep)
L8   if inside an Essence Break window
        and the spender is affordable:                     cast CS  (-> Annihilation)
L9   if Eye Beam usable and affordable:                    cast EB  (-> Abyssal Gaze)
L10  [NO META] if Blade Dance usable and affordable:       cast BD
L11  if Felblade usable:                                   cast Felblade
L12  if IA at its CHARGE CAP, outside an EssB window
        and Blade Dance not up:                            cast IA  (-> Consuming Fire)
L13  if the spender is affordable:                         cast CS  (-> Annihilation)
L12b if Immolation Aura usable:                            cast IA  (-> Consuming Fire)
L14  if AoE and Fel Rush usable:                           cast Fel Rush
L15  if Throw Glaive usable and affordable:                cast Throw Glaive
```

Fifteen lines; Destruction has 13, Retribution 11.

⚠ **L13 SITS BETWEEN L12 AND L12b, AND THE OUT-OF-ORDER NUMBERING IS DELIBERATE.** The
L-numbers are permanent labels that the brain's `-- Ln` comments and the oracle's case
names both key on; renumbering them would silently invalidate every cross-reference in
this document, the code and the tests for a cosmetic gain. The *evaluation* order is the
order written above, and it is Blizzard's own shape from the assisted-combat list:
**generator → spender → generator**, with the spender repeated so it takes the press
whenever it is affordable and falls through when it is not. Before this revision the two
generators sat above the main dump behind Fury-deficit gates; with no readable deficit
they would have fired unconditionally and starved the spender — which is the flight
failure repeated by a different mechanism.

**Abilities that appear on two lines** — Immolation Aura (L4 AoE, L12 filler), Blade
Dance (L7 meta, L10 non-meta), the spender (L8 window, L13 dump). Each pair keys on
**one base spellID**, so a single `excluded` entry drops both occurrences and the
runner-up recompute stays honest. This is Retribution's three-line-spender shape.

**Which lines carry an affordability gate, and why the others do not.** Only the five
abilities the spec declares with `spends = "fury"` *and* that the list gates on the
resource ask `IsSpellUsable`: the spender (L8, L13), Blade Dance (L7, L10), Eye Beam
(L9) and Throw Glaive (L15). Felblade, Immolation Aura, Fel Rush, Vengeful Retreat, The
Hunt and Metamorphosis are **generators or free presses** — asking about them would burn
a guarded call per pulse to learn a constant. ⚠ **Essence Break has no Fury cost at all**
(its old `fury>=35` gate was a *pooling* rule, not a press gate — see Deviation 13), so
there is nothing for the API to report and L6 asks nothing.

⚠ **An UNREADABLE verdict does not block the press.** `nil` from `ns.SpellUsable` means
*"we could not ask"*, and it falls through to allowing the line. That is the safe
direction here and only here: the CDM / napkin / charge readiness gate still sits in
front of every line, so the worst case is a cue for a press that fails — where the
alternative, treating unreadable as unaffordable, reproduces the exact flight failure
this revision exists to fix.

## Deviations from the simc order (adjudicate these)

1. **The Reaver's Glaive SEQUENCE is not implemented, and this is a data fact rather
   than a difficulty.** simc's `variable.rg_inc` / `variable.rg_ds` encode a multi-GCD
   ordering (Reaver's Glaive → Rending Strike → Glaive Flurry → the empowered spender),
   and the flat cascade has no sequencing vocabulary. But the deeper reason is that
   **the sequence's two ordering buffs are not readable at all**: `Rending Strike`
   442442 and `Glaive Flurry` 442435 have **no `CooldownSetSpell` row** in set 1599
   (T1 DB2 @ 12.0.7), so there is no `item:IsActive()` presence channel for either.
   Nor is `buff.reavers_glaive` (442294). Six APL lines (:56–61) read exactly those
   buffs, and every one of them is dark.

   What **is** readable is the **transform** — a Throw Glaive frame overridden to
   Reaver's Glaive — and that is L1. So the HUD says *"a Reaver's Glaive is up, press
   it"* and then goes quiet about what to spend it on. Under-serving one hero tree's
   payoff, never mis-serving it.

   ⚠ **This is deliberately NOT a parked `spec.X = false` switch.** A parked switch
   waits on a *question a flight can settle*; this one has an answer already, and it is
   "the read does not exist". Building the machinery behind a switch nothing can ever
   flip would be worse than the honest gap. See `notes.md` → *What Aldrachi Reaver
   costs us*.

2. **Every `variable.inertia_*` gate is dropped.** simc has three lines
   (:76, :77, :83) whose whole purpose is consuming an **Inertia trigger** with
   Felblade or Fel Rush before a burst window, and `variable.inertia_ready` reads
   `buff.inertia_trigger.up`. The tracked row is the **talent** `Inertia` 427640; the
   consumed buff is 427641; the *trigger* is a third aura with no tracked row. Reading
   the talent row's presence as "the trigger is up" is the Light's Deliverance mistake
   (Retribution's `RET_HOL_FROM_BUFF`) — a near-permanently-present buff jamming a line
   at the top of the list. **Dropped**, so an Inertia build simply loses an
   optimisation; Felblade and Fel Rush still cue on their Fury lines (L11, L14).

3. **Essence Break is meta-only, because the APL says so.** The top-level
   `essence_break` action at :87 is inside a comment; only `actions.meta`'s :121
   survives. The KB agrees in spirit ("Essence Break inside/around the Meta window").
   ⚠ This may be a simc **authoring accident** rather than a tuning decision — the
   comment on :87 reads like an intended line that was commented out for a test and not
   restored. Taking the file literally is the Tier-1-faithful call, and it fails safe
   (a missed press, never a wrong one). Re-check on the next simc pull.

4. **Two Felblade lines folded into one (L11), and the deficit gate is GONE.** simc has
   `felblade` at :90 (`fury.deficit>=15+gen*0.5`, above the main dump) and at :97
   (`fury<40`, below it). The second is unreachable: whenever `fury < 40` the deficit is
   ≥ 80, so :90 already fired. One line, at :90's position.

   ⚠ **The `deficit >= 40` gate it used to carry is dropped, because the deficit is not
   a readable number** (*Fury is secret*). What replaces it is not a weaker threshold but
   **position**: Felblade fires whenever it is usable, and the spender (L13) sits
   immediately below it, so a Felblade press costs the rotation one GCD it was going to
   spend generating anyway. That is Blizzard's own handling —
   `assisted_combat/demonhunter_havoc.simc` presses a bare `felblade` with no gate of any
   kind, between two `chaos_strike` lines. Felblade has a real 12 s cooldown, so
   "whenever usable" is self-limiting; **Immolation Aura (L12) is deliberately below the
   spender for the same reason and is not**, being a 30 s charge category.

5. **Two Throw Glaive lines folded into one (L15).** :93 is the Soulscar / Furious
   Throws build line — gated on three talents we cannot read — and :99 is the plain
   filler. Keeping only the filler under-presses Throw Glaive on a Soulscar build
   (where it is a real rotational press, not a filler) and is correct everywhere else.

6. **Two Fel Rush lines folded into one (L14), AoE-gated.** :94 and :98 are both
   filler; :94 carries `active_enemies>1`. Fel Rush is a movement ability with a real
   damage component in AoE and a real *cost* in single target (it moves you). Gating on
   the mode toggle is the conservative reading. ⚠ And see *The two lying cooldowns*
   below — Fel Rush is the ability whose readiness the HUD is least sure of.

7. **`active_enemies` becomes the manual mode toggle everywhere.** The HUD has no
   target roster. Every `active_enemies>=N` term collapses to `mode == "aoe"`, a player
   **declaration** rather than an observation — exactly as Destruction's Rain of Fire
   and Retribution's Divine Storm do. This affects L4, L14 and `variable.use_blade_dance`
   (Deviation 8).

8. **`variable.use_blade_dance` is treated as always true.** simc:
   `active_enemies>=3-talent.trail_of_ruin | talent.first_blood |
   talent.screaming_brutality&(…)`. Three unreadable talents, and **First Blood is the
   standard single-target pick** — with it, Blade Dance is a full ST spender. So Blade
   Dance is offered whenever it is usable. On a build without First Blood in pure ST
   this over-presses a 15 s cooldown that is still a positive-value press (it merely
   loses a little to Chaos Strike); the alternative — gating on `mode == "aoe"` — would
   make Blade Dance **invisible for the whole single-target rotation of the standard
   build**, which is a far larger error. Recorded because it is the one place this list
   deliberately chooses over-pressing.

9. **`variable.pool_glaive_tempest` and `variable.cs_machine` are dropped.** Both are
   talent-derived Fury-threshold adjustments (`75 - gen*gcd - 20*cs_machine +
   25*pool_glaive_tempest`) on the main spender line. With no talent read the adjusted
   threshold is unknowable, and the un-adjusted gate is simply *"can you afford it"* —
   which is L13, and which is what the implicit affordability gate already says. The
   pooling nuance is lost; the press is not.

   ⚠ **Strengthened by the flight rather than weakened**: with Fury secret, *every*
   threshold on this line is unknowable, not just the three talent-derived terms. "Can
   you afford it" is no longer a reduction of simc's gate — it is the only formulation
   the client can answer at all.

10. **Rain from Above 206803 gets no line.** It is a tracked **Essential** ability with
    a real 90 s cooldown that **never appears anywhere in the 140-line APL**. A dead
    icon by construction. It is registered (so the decision log can name it and the
    coverage probe does not report it blind) and cued by nothing.

11. **`the_hunt`'s Eternal-Hunt alignment clauses are dropped.** :115's real gate runs
    to nine terms, seven of which are `cooldown.X.remains` reads of *other* abilities —
    secret in combat. What survives is `debuff.essence_break.down` (readable via cast
    history, see below) and `!buff.reavers_glaive.up` (readable via the transform).
    The Hunt therefore fires roughly on cooldown, which is the KB's own summary
    ("The Hunt on cooldown, kept out of Essence Break windows").

12. **Metamorphosis's :103 gate — the longest single line in the APL — reduces to ONE
    readable term, `!buff.inner_demon.up`.** ⚠ **Corrected 2026-08-03; the Blade Dance
    term was a MISREADING and it cost Metamorphosis every press of the flight.**

    The original derivation kept `cooldown.blade_dance.remains` as "Blade Dance is not
    usable right now" — a truthy non-zero duration read as a boolean, which is a correct
    reading of *that fragment*. The error was reading the fragment instead of the clause.
    In full, with simc's precedence (`&` binds tighter than `|`):

    ```
    ( cooldown.blade_dance.remains
      & ( cooldown.blade_dance.remains > gcd.max*3
        | prev_gcd.1.death_sweep | prev_gcd.2.death_sweep | prev_gcd.3.death_sweep ) )
    | !talent.chaotic_transformation
    ```

    Two things follow, and each alone is disqualifying.

    - **The whole clause is TRUE for anyone without Chaotic Transformation.** That
      talent is what makes Metamorphosis reset Eye Beam and Blade Dance; the gate exists
      only to stop you wasting the reset. Without it the gate does not apply at all — and
      **`talent.chaotic_transformation` is not readable**, so the escape hatch is
      invisible to us.
    - **Even with it, the requirement is not "Blade Dance is on cooldown" but "Blade
      Dance is at least ~3 GCDs from ready, or a Death Sweep just went out."** The
      implemented term was strictly weaker in one direction and, because it could never
      see the escape clause, strictly stronger in another.

    **Measured consequence:** `not bladeDanceUsable` vetoed Metamorphosis on **all 2374
    in-combat lines** of the 2026-08-03 flight, which won it zero presses. (Blade Dance
    read Ready almost always *because* of the Fury bug — it was never pressed, so it
    never went on cooldown — but the veto is a real defect on its own and would have bitten
    a working rotation too, on any build lacking Chaotic Transformation.)

    **The term is dropped.** This is the same call the Eye Beam alignment block already
    got, for the same stated reason: holding a **2-minute cooldown** on a gate we cannot
    evaluate is worse than landing it out of sync. Dropping means Meta may be cast while
    Blade Dance happens to be ready, wasting part of a reset on a Chaotic Transformation
    build — a damage loss on a press that is still strongly positive. Vetoing means never
    casting it at all, which is what shipped. ⚠ If a talent read ever lands in the
    pipeline, this is the first gate to revisit; it needs `talent.chaotic_transformation`
    and an *anticipation* read of Blade Dance, not a usability boolean.

13. **Essence Break's `fury>=35` is dropped (L6).** simc's `essence_break,if=fury>=35`
    is a **pooling** rule — it exists so the 4 s amplification window opens with enough
    Fury behind it to actually flood, not because the press costs 35. **Essence Break has
    no Fury cost at all** (DB2 `SpellPower` has no PowerType 17 row for 258860), so
    `IsSpellUsable` has nothing to report and the gate has no readable replacement.
    Dropped rather than approximated. The cost is that Essence Break can open on an empty
    bar; the following lines then generate rather than spend inside the window, which
    wastes it. ⚠ This is the **one genuine rotational regression** of the secrecy
    finding — every other dropped gate is a pooling nuance on a press that stays correct,
    and this one can waste a 40 s cooldown. It is the strongest argument for Phase 2, and
    it is recorded here so Phase 2's design does not have to rediscover it.

## Settled-by-derivation clarifications

1. **The Essence Break window is read from CAST HISTORY, not from an aura.** simc gates
   four lines on `debuff.essence_break.up` / `.down`. The debuff is **320338**, which
   has no `CooldownSetSpell` row — only the 258860 *cast* is tracked. But the debuff's
   duration is a flat **4000 ms** (T1 DB2 `SpellDuration`), and `ns.Coach.CommittedWithin`
   already answers *"was this base cast within N seconds"* off the pulse's cast history,
   which **is** readable in combat (`UNIT_SPELLCAST_SUCCEEDED` spellIDs are a settled
   readable channel). So `ctx.ebWindow = CommittedWithin(state, 258860, 4.0)`.

   ⚠ This is an **estimate with a known bias**: it cannot see a window ended early by
   the target dying, and it does not model the talent that extends it. Both fail toward
   *thinking the window is open slightly too long*, which spends a GCD on Chaos Strike —
   the press L13 would have made anyway. The failure is a **reordering, not a wasted
   press**, which is why the estimate is acceptable here and a napkin-derived aura would
   not be.

2. **Stack counts are unavailable, and it costs less than it looks.** simc reads
   `.stack` on `buff.cycle_of_hatred`, `buff.immolation_aura`, and (via
   `soul_fragments.total`) the Aldrachi fragment counter. Every one of those is behind
   a **talent** spellID whose CDM row reads `CumulativeAura = 0` — the cross-cutting DB2
   trap. Art of the Glaive 442290 reads 0 while the real aura 444661 carries **80**;
   Demonsurge 452402 reads 0 against 452416's **4**. Immaterial in practice: the HUD's
   buff channel is `item:IsActive()`, a **bool**, so a stack count was never reachable
   whichever ID we keyed on. Every gate that needed one is dropped, not approximated.

3. **Havoc declares NO `derived` resource, and that is a positive finding.** The
   Phase-0.3 `spec.derived` channel exists for a class resource `Enum.PowerType` cannot
   carry — Demon Hunter Soul Fragments. Havoc does not need it, on three Tier-1 checks:
   `demonhunter_havoc.simc` references `soul_fragments` **once** (as one of three ORed
   alternatives gating a single `annihilation` line) against `demonhunter_vengeance.simc`'s
   **32**; the `castCount` reader is Soul Cleave 228477, a *Vengeance* spell Havoc does
   not have; and Blizzard's own `DemonHunterSoulFragmentsBar.lua:18` sets
   `self.requiredSpec = SPEC_DEMONHUNTER_DEVOURER`. What Aldrachi Reaver Havoc actually
   interacts with are ordinary **buffs**, which ride the existing presence channel.
   Vengeance (`castCount`) and Devourer (`auraStacks`) remain the first consumers.

4. **The action-bar ID is not the tracked ID for two abilities.** SkillLine 1848
   (Havoc) teaches *wrapper* spells that the CDM does not track:
   `Chaos Strike 344862` → the CDM tracks **162794**, and `Fel Rush 344865` → the CDM
   tracks **195072** (344865's only effect is `trigger → 195072`). The rung ladder asks
   the action bar about the tracked ID and finds nothing, so both would lose their
   keybind hint. `spec.SpecBindAlias` covers it — the Imp Lord case exactly.

## The two lying cooldowns — Havoc's defining observability fact

Every spec so far has had one headline data problem. Destruction's was the DoT read;
Retribution's was four Essential buttons whose cooldown lives on a charge category with
`RecoveryTime = 0`, so `ns.BaseCooldown` reads 0 and the napkin has nothing to count.

**Havoc's is worse in kind: two Essential buttons report a base cooldown that is not
merely absent but WRONG.**

| Ability | `RecoveryTime` | `CategoryRecoveryTime` | ChargeCategory (max, recov) | `ns.BaseCooldown` reads | truth |
|---|---:|---:|---|---:|---:|
| **Fel Rush** 195072 | **1000** | 500 | 1545 (1, 10 000) | **1 s** | 10 s |
| **Immolation Aura** 258920 | 0 | **1500** | 1676 (1, 30 000) | **2 s** | 30 s |
| Throw Glaive 185123 | 0 | — | 1612 (1, 9 000) | 0 s | 9 s |
| Vengeful Retreat 198793 | 500 | 25 000 | 1601 (1, 25 000) | **0.5 s** | 25 s |

*(T1 DB2 @ 12.0.7. `ns.BaseCooldown` returns `CategoryRecoveryTime` when `RecoveryTime`
is 0 — the property Avenging Wrath demonstrated, `SpecRetribution.lua:43-45`.)*

**⚠ The plan's DB2 appendix said "+1 (Fel Rush)". It is three** — Immolation Aura and
Vengeful Retreat carry the same shape, both with a short *shared-category lockout*
masquerading as the button's own cooldown.

**Why a lie is worse than a zero.** `HudNapkin.lua:113-119` falls back to the
spec-declared `chargeCD` **only when the live read is not positive** (`if not (type(len)
== "number" and len > 0)`). An honest 0 trips that fence; a lying `1` does not. So Fel
Rush would get a 1-second napkin against a 10-second cooldown, and no declared constant
could rescue it.

**What saves it, and it was not built for this.** All four are **1-charge charge
categories**, and `usable()`'s one-charge rule — shipped for Retribution's flight defect
#5 on 2026-08-03 — requires **both** a banked charge **and** `probablyUp` for a pool of
one. The charge napkin decrements on the cast and only restores on the `ChargeGained`
alert at the *real* 10 s, so the count vetoes the early cooldown read for the whole
duration. **The press is protected; only the decoration lies** (a `SOON` that lights
about a second after the cast and goes quiet, and a countdown that is wrong).

That is the same loss Retribution takes on its four charge-category buttons —
decoration, not presses — arrived at from the opposite direction.

**The residual risk is narrow and real:** if the charge count is *absent*
(`ch.charged == false`, or no out-of-combat seed — `C_Spell.GetSpellCharges` is
combat-gated), `usable()` falls through to `probablyUp or chargeBanked` and the early
napkin wins. That is an early cue on a button that cannot be pressed. **Acceptance
criterion 4 of the flight is exactly this question.**

**The fix, if the flight shows it biting**, is one fence, and it is a *generalisation*
rather than a special case: let a declared `chargeCD` win when the live base-cooldown
read disagrees with it beyond a tolerance. The napkin's existing honesty rules make it
safe in one direction only (an observed `Available` edge always clears the record;
expiry never claims readiness), so the worst a longer number can do is hold a button
back. **Deliberately not shipped in this diff** — the plan's instruction is to let the
flight arbitrate, and shipping a pipeline edit against a symptom nobody has seen is how
a guard outlives its reason.

## Aldrachi Reaver delta (not a second list)

Aldrachi Reaver is the funnel / cleave alternative. It changes **one** readable thing;
the rest of the list stands.

- **Throw Glaive becomes Reaver's Glaive.** Reaver's Glaive 444686 applies an
  override-actionbar-spell aura (`EffectAura 332`, `misc0 = 185123`) replacing Throw
  Glaive 185123 with 442294. That is **L1** — the top of the list, because it is a free
  armed press that blocks nothing and expires.
- **The payoff is invisible.** Everything Reaver's Glaive *arms* — Rending Strike,
  Glaive Flurry, the empowered Chaos Strike / Blade Dance, and the `rg_ds` ordering —
  rides buffs with no CDM row. See Deviation 1.
- **Reaver's Mark 442679, Fury of the Aldrachi 442718, Thrill of the Fight 442686 and
  Art of the Glaive 442290 ARE tracked** and are registered as `kind = "aura"` inputs,
  so the decision log can name them and the coverage probe stays quiet. None gates a
  line: Reaver's Mark is a **debuff on the target** and it is unsettled whether a
  TrackedBuff row reports a target debuff through `IsActive()` at all
  (`observability-map.md` Q3).

Fel-Scarred's own additions (Demonsurge, Abyssal Gaze, Consuming Fire, Student of
Suffering, Monster Rising) are all **display overrides on frames the list already
presses**, so they need no lines either — L9 presses Eye Beam and the icon shows
Abyssal Gaze; L4/L12 press Immolation Aura and the icon shows Consuming Fire. That
symmetry is why the fork model works.

## Implementation notes (what `CoachHavoc.lua` had to decide)

1. **`ctx.inMeta` reads two sources, ORed.** The Metamorphosis TrackedBuff row (191427)
   and the Chaos Strike frame's meta transform. Neither is a guess and neither is more
   trustworthy; a build or a row that surfaces only one still forks correctly.

2. **L5's Vengeful Retreat gate is the one cross-ability anticipation read in the
   file.** simc presses VR when Eye Beam is about a GCD away (`cooldown.eye_beam.remains
   <= gcd.remains`), and a *client* cooldown-remains read of another ability is secret
   in combat. But **our own napkin's** `remaining` is not a client read — Eye Beam's
   base cooldown is an honest 30 s (`CategoryRecoveryTime = 30000`), so the countdown is
   a real number the pipeline already computes for `SOON`. L5 reads
   `ctx.facts[EYE_BEAM].remaining <= 1.5`.

   ⚠ **This is new vocabulary for the cascade and is flagged as such.** Retribution
   dropped its equivalent handshake (Execution Sentence paired with Wake of Ashes)
   because Wake of Ashes is charge-category and has no napkin to read. Eye Beam does.
   The rule generalises as: *a cross-ability timing gate is allowed when the other
   ability's cooldown is one the napkin can honestly count.* If the flight shows VR
   cueing at wrong moments, this line is the first suspect.

3. **The parked one-line switch is `HAVOC_RG_FROM_BUFF`, defaulted OFF.** L1's
   unambiguous read is the transform. The tempting second source is **Art of the
   Glaive** (442290), which is the fragment counter that *arms* Reaver's Glaive at 6
   fragments — and its presence is readable while its 80-stack count is not. If it is
   simply present for most of a fight, treating presence as "armed" pins L1 above
   Metamorphosis and The Hunt permanently. This is the Light's Deliverance shape
   verbatim (`RET_HOL_FROM_BUFF`), so it takes the same default and the same one-line
   reversal. Flip it only if the decision log shows 442290 present *only* while a
   Reaver's Glaive is genuinely available.

4. **`Escalate` lists only the four honest cooldowns, and NOTHING ELSE.** Metamorphosis
   (120 s), The Hunt (90 s), Eye Beam (30 s) and Blade Dance (15 s) carry their cooldown
   on the **spell row** (`CategoryRecoveryTime`), so `ns.BaseCooldown` reads them
   correctly and `overdue` is meaningful. **Nothing on a charge category is listed** — a
   charged ability raises `Available` on every charge restore, so its ready-edge latches
   and `overdue` would fire constantly. Escalating on a signal we cannot trust is what
   `Escalate` is forbidden to do.

   ⚠ **The "spender parked at a full Fury bar" rule is DELETED** (2026-08-03). It was the
   analogue of Destruction's Chaos-Bolt-at-full-bar and Retribution's spender-at-cap, and
   it needed a number — `ctx.fury >= ctx.furyMax` — that does not exist. It is
   unrecoverable through `IsSpellUsable`, which is binary and reads identically at 40 and
   at 170 Fury. Phase 2's `LuaCurveObject` branch is the only route back to it; do not
   reinstate it against a fabricated value.

5. **`SpecPowerDelta` and the whole in-flight Fury projection are DELETED** (2026-08-03).
   They projected the signed cost of an in-flight spender onto the live rail so a spender
   mid-GCD stopped being re-cued — **and there is no live rail to project onto.** A
   projection over an absent value is either `nil` (no effect) or a fabricated number,
   and the second is the bug this whole revision is remediating. `spec.powers` keeps
   `incoming = false`, which is the honest declaration that this bar carries no
   projection.

   The *reasoning* that used to live here is kept because it is still true and still
   binding on anyone who tries to bring the projection back: Havoc's generators are
   auto-attack, Immolation Aura ticks, Felblade and Vengeful Retreat's Tactical Retreat —
   every one talent-modified and none of it on the pulse. simc computes
   `variable.fury_gen_per_sec` from six terms including haste and three buff stacks.
   Authoring a base number would over-credit a builder and promise a spender you cannot
   cast, which is the failure direction that actively misleads. That argument applied to
   *builders* when spenders were still projectable; with the rail secret it applies to
   both halves, and there is nothing left to project.

   ⚠ **Re-cueing a spender mid-GCD is the behaviour we lose**, and it is not free: the
   HUD may keep showing "Chaos Strike" for the fraction of a second between the cast
   going out and the client updating its own affordability answer. Blizzard's answer
   updates on the server's schedule rather than ours, which is at worst the same latency
   every other consumer of `IsSpellUsable` lives with. Accepted; watch for it in the
   re-fly.

## Winner and NEXT PRESS (for the module)

⚠ **CHANGED 2026-08-03, and it changed for all four specs at once.** The second cue used
to be the *runner-up* — the same list re-run with the winner's ability removed, answering
*"if I am wrong, press this instead"*. It is now a **one-GCD look-ahead**: *"what will I
press next?"*

- The **winner** is the first castable line, top to bottom. Unchanged.
- The **next press** is what the **same list** produces over
  `ns.Coach.Advance(state, winner)` — the board one global cooldown later, assuming the
  winner is pressed. The advance starts the winner's cooldown, spends one of its charges,
  and moves every other ability one GCD closer to ready.
- **When the answer is the winner's own ability there is no second cue.** The winner's cue
  carries `next = true` and the Renderer draws a small **companion dot** on the same icon —
  the double-tap hint. That is the common case here: Chaos Strike has no cooldown at all
  and won **35 %** of the 2026-08-03 flight, so a second *icon* could not say it.

⚠ **What the look-ahead deliberately does NOT model**, because pretending otherwise is the
bug class that failed the first flight:

- **Resources.** Fury is secret, so affordability passes through *unchanged*. The
  look-ahead assumes you can still afford whatever you can afford now — wrong immediately
  after a spend, and the least-wrong option available.
- **Buffs and cast history.** A press that would open a window (Metamorphosis → demon form,
  Vengeful Retreat → Initiative, Essence Break → its window) does not flip it. So the hint
  **under-predicts the burst lines** and fails toward the steady-state next press.
- **The clock.** `state.at` is not advanced; only `cd.remaining` moves. Rolling the clock
  would age every napkin, dot timer and history window as a side effect of one question.

⚠ **`spec.Spec[id].baseCD` / `.chargeCD` IS NOW LOAD-BEARING**, not decoration: it is the
only source the advance has for "what does pressing this start". A rotational button with a
real cooldown and no declared number would stay `ready` in the hypothetical and be
re-offered forever. Havoc's table is complete (audited 2026-08-03); the pairing is pinned by
`coach_apl_spec`'s *"an ability WITH a cooldown does not repeat"*.

**The exclusion machinery survives without a shell caller.** `RankWinner(ctx, excluded)` is
still part of the brain contract and still correct — Immolation Aura appears at L4/L12/L12b,
Blade Dance at L7/L10, the spender at L8/L13, each keyed on one base spellID so an exclusion
drops *every* line that names it. Nothing in the shell calls it now; the four oracles test
it directly.

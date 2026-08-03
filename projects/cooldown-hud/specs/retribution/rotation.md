# Retribution Paladin — rotation priority list (APL)

This is the **spec of record** for the Retribution rotation as a flat, ordered
**action priority list**. It is evaluated top to bottom; the **first line whose
action is castable is the press**. Every line carries an implicit gate: *"the
ability is usable"* — off cooldown, procced, charged, and affordable.

> **⚠ STATUS: IMPLEMENTED, DESK-DERIVED, NOT FLOWN.** Like `specs/destruction/`,
> this list is **distilled from the Tier-1 simc midnight APL**
> (`ActionPriorityLists/default/paladin_retribution.simc` @ `ab7b0b8`, 2026-08-01,
> DBC build 12.0.7) and corroborated against
> `knowledge/classes/paladin/retribution/rotation.md` (12.0.7, reviewed 2026-07-11).
> Every place I departed from the simc order is called out under **Deviations** —
> those are the lines to adjudicate. **Nothing here has been flown.**
>
> **This list SHIPS:** `CoachRetribution.lua` implements L1–L11 line-for-line (the
> line numbers below are its comment labels, so the two diff by eye), and
> `tests/spec/coach_retribution_apl_spec.lua` is the independent oracle that pins
> the code to *this document*. A change here is a change to the addon — edit the
> list, then the brain, then the oracle.

> **v1 profile: Templar.** The KB calls Templar the S1 default; it is also the tree
> whose identity the HUD can actually *see*, because Hammer of Light arrives as a
> **spell override on the spender frame** — the same readable channel Demonology's
> Ruination and Destruction's Infernal Bolt ride. **Herald of the Sun** is a delta
> section at the bottom, not a second list.

## How to read it

- **`hp`** means **projected Holy Power**: the live count plus anything already in
  flight. Holy Power's `modifier` is **1**, so the exact rail and the display rail
  are the same number — none of Destruction's fragment arithmetic applies here.
- **Implicit gate on every line:** the named ability is only a candidate if it is
  usable right now (off cooldown / a charge banked / procced / affordable). A line
  whose ability is not usable is skipped and evaluation continues.
- **Abbreviations:** HoL = Hammer of Light, TV = Templar's Verdict, FV = Final
  Verdict, DS = Divine Storm, BoJ = Blade of Justice, WoA = Wake of Ashes,
  ES = Execution Sentence, DT = Divine Toll, AW = Avenging Wrath, HoW = Hammer of
  Wrath, CS = the filler frame (Crusader Strike / Templar Strike / Slash / Sweep).

## The resource: Holy Power, tracked but NOT drawn

Holy Power is `Enum.PowerType.HolyPower` (**9**, confirmed offline against
`BlizzardInterfaceResources/Resources/LuaEnum.lua:5691`), 0–5, `modifier` 1. State
already reports it: `readPower` iterates the whole enum and emits every power the
character has, so `state.power.HolyPower` is on the pulse today with **no State
edit and no `spec.powers` declaration** — `spec.powers` is the *render* list.

This spec declares it with **`display = "none"`**, which means *tracked but not
drawn*. That is a deliberate design decision, not an omission:

- The HUD draws **no resource bar** for Retribution. Blizzard's own Holy Power bar
  is right there and the project's stance is *enhance, don't replace*.
- But the power still travels the whole rail — `ctx.powers` → `resourceBars[]` →
  the decision log's `PW:` column. That column is the primary instrument for
  debugging a brain nobody can watch live, and an empty `spec.powers` would have
  emitted no bar at all and rendered `?/?`.

**Every spender costs 3 Holy Power, not 5** `[T1 DB2: SpellPower @ 12.0.7 —
Templar's Verdict 85256, Divine Storm 53385, Final Verdict 383328 and Hammer of
Light 427453 all read PowerType 9, cost 3]`. The KB's "spend at 5 Holy Power" is a
*pooling* rule (don't overcap), not a cost — do not read it as one. The cost is
resolved **live** through `env.shardCostFn` anyway, with 3 only as the fallback.

## Priority list

> **⚠ THIS LIST WAS REORDERED ON 2026-08-03**, after a KB/APL review caught two real
> mistakes. Both came from reading the generated APL's *text* order instead of its **call
> structure**, and both are recorded here because the error is easy to repeat:
>
> - **Hammer of Light was L1, above Execution Sentence and Avenging Wrath.** It heads
>   `actions.finishers` — but `finishers` is only ever entered from `actions.generators`,
>   and `actions.cooldowns` (which owns `execution_sentence` and `avenging_wrath`) is called
>   *before* generators. "First in its sub-list" is not "first". The KB agrees: AW(1), ES(2),
>   HoL(3). Since a hammer is armed for up to 20s after every Wake of Ashes, the old order
>   deferred the burst buttons for a large fraction of every pull. **Hammer of Light is now
>   a spender *choice*, not a line** — see *Choosing the spender*.
> - **Hammer of Wrath sat above Blade of Justice**, which is simc's
>   `talent.walk_into_light` placement — while Deviation 5 below said we were taking the
>   *lower*, default-build placement. The document was right and the code disagreed with it.

### L1 — Execution Sentence, on cooldown

60s. simc fires it immediately before Wake of Ashes so its delayed detonation lands inside
the burst. See **Deviation 2**.

⚠ **Above Avenging Wrath, following simc rather than the KB.** `actions.cooldowns` lists
`execution_sentence` (simc:33) before `avenging_wrath` (simc:34); the KB's single-target
list puts wings first. Both cannot be right, and simc wins here: it is Tier-1,
machine-generated against this same 12.0.7 build, and its ES line is explicitly gated to
fire just before Wake of Ashes. The KB file is `confidence: medium`, reviewed 2026-07-11,
and its ordering reads like an editorial "cooldowns block" rather than a transcription.
*Decision recorded 2026-08-03.*

### L2 — Avenging Wrath, on cooldown

120s. On a **Radiant Glory** build this button does not exist (WoA/ES cast the wings), so
the line simply finds nothing tracked and evaluation continues — the degradation is free and
needs no talent read.

⚠ **Crusade** (1253598) is the alternative on some builds. It is registered and counted as
"wings" for L9's gate, but it is *not* registered as a button — DB2 gives it no cooldown and
no cost, so it is the talent node rather than a press.

### L3 — Spend at cap, unless Wake of Ashes is ready

`hp >= 5` **and** Wake of Ashes is *not* ready. simc:
`call_action_list,name=finishers,if=holy_power=5&cooldown.wake_of_ashes.remains`.
The second clause is not a rounding detail: at cap with WoA **ready** you press WoA anyway
(L4) because it *arms Hammer of Light*, and the armed spender is worth more than the overcap.
Which spender — see **Choosing the spender** below.

### L4 — Wake of Ashes, on cooldown

30s (charge category 2285). Arms Hammer of Light. See **Deviation 2**.

### L5 — Divine Toll, on cooldown

60s.

### L6 — Blade of Justice on a proc

**Art of War** (406064) or **Righteous Cause** (402912) — both are tracked buffs, so this is
ordinary readable presence.

### L7 — Spend

`hp >= cost`. The unconditional `call_action_list,name=finishers` that sits in the middle of
simc's generator list — its second and last finisher entry point.

### L8 — Blade of Justice, on cooldown

12s (charge category 2128), no proc needed.

### L9 — Hammer of Wrath, while wings are up

Its true gate is *target health ≤ 20% **or** wings are up **or** Walk into Light*. We can
read the wings (Avenging Wrath 31884 **or** Crusade 1253598, both presence reads) and nothing
else. See **Deviation 4** — and note L9 is doubly degraded, because Hammer of Wrath is not in
the tracked set at all (**Blind spots**, below).

⚠ **Below Blade of Justice**, per Deviation 5.

### L10 — Judgment, on cooldown

11s (charge category 1663).

### L11 — The filler builder

The **Crusader Strike frame** (35395). On Templar this frame carries **Templar Strike**
(407480), **Templar Slash** (406647) and **Templar Sweep** (406661) as overrides; the brain
presses the frame and the game decides which strike comes out, which is exactly right — the
alternation is Blizzard's, not ours. **2 charges** `[T1 DB2: SpellCategory 1627 —
MaxCharges 2, ChargeRecoveryTime 6s]`, so this is the line the charge rule matters most for.
*(Only Templar Strike shares category 1627; Slash and Sweep are chain follow-ups with
`ChargeCategory 0`.)*

## Choosing the spender (L1 / L4 / L8)

simc's finisher block resolves to one of three buttons. Flattened:

```
ds_castable = (active_enemies >= 3 - (tempest_of_the_lightbringer & !jurisdiction)
               | buff.empyrean_power.up)
              & !buff.empyrean_legacy.up
```

- **Hammer of Light** if a spender frame is transformed — it *outranks both others*. That
  is simc's `(!buff.hammer_of_light_ready.up|buff.hammer_of_light_free.up)` gate on
  `divine_storm` and `templars_verdict` (simc:38-39): while a hammer is ready, no ordinary
  finisher may be pressed.
- **Divine Storm** if `ds_castable`.
- **Templar's Verdict** (or **Final Verdict**, its talent override) otherwise.

⚠ **This is why Hammer of Light is not a priority line.** It has no cooldown and no
readiness of its own — being *armed* is the entire condition, and "armed" only matters at
the moment you were going to spend anyway. Modelling it as a line put it above the burst
cooldowns; modelling it as the spender choice puts it exactly where simc does.

We have no target roster, so `active_enemies >= 3` becomes the **manual AoE mode
toggle** — a player *declaration*, never an observation, exactly as Destruction's
Rain of Fire does. **Empyrean Power** (326732) and **Empyrean Legacy** (387170) are
both tracked buffs, so those two terms survive verbatim.

## Deviations from the simc APL

Every departure, with the reason. These are the lines to adjudicate on a live pass.

**1. Hammer of Light is pressed whenever armed; simc's free-proc timing is dropped.**
simc's first finisher is `hammer_of_light,if=!buff.hammer_of_light_free.up|<four
duration clauses>`. The first clause — *"if this is the **paid** one, just press
it"* — we implement exactly. The four clauses that govern dumping a **free** proc
(`buff.undisputed_ruling.remains<gcd*1.5`, `buff.avenging_wrath.remains<gcd*2`,
`buff.hammer_of_light_free.remains<gcd*2`, `target.time_to_die<gcd*2`) are all
**buff-duration reads, and buff durations are Secret Values in combat**. We can see
that a buff is *present* and never how long it has left. Pressing early is the safe
direction: the cost is a little optimisation, where holding risks wasting the proc
outright.

**2. Execution Sentence and Wake of Ashes are plain on-cooldown lines; their
pairing is not expressed.** simc gates ES on `cooldown.wake_of_ashes.remains<gcd`
and WoA on `cooldown.execution_sentence.remains>4` — a two-way cooldown-remaining
handshake. ⚠ **Both sides of it are unreadable here, and for a sharper reason than
usual:** `C_Spell.GetSpellCooldown` is secret in combat (settled game-wide), and the
napkin that normally covers for it has **nothing to count down from** —
`SpellCooldowns.RecoveryTime` is **0** for Judgment, Crusader Strike, Blade of Justice
and Wake of Ashes, because all four live on **charge categories** `[T1 DB2 @ 12.0.7]`.
That is the Conflagrate problem (`docs/roster-state-plan.md`, field-fix C2) applied to four
abilities instead of one.
⚠ **This said "six" until 2026-08-03 and it was wrong in two ways.** Avenging Wrath is not
one — it carries `CategoryRecoveryTime = 120000` on the *spell* row, so its base cooldown
reads fine. Templar's Verdict and Divine Storm read 0 because they have **no cooldown at
all**, which is a different thing entirely. And the old list named Hammer of Wrath, which
is not among the nine because it is not in the tracked set. So both fire on cooldown and the burst is a little
less tight than simc's.

**3. Every `raid_event.adds` and `target.time_to_die` gate is dropped.** There is
no roster and no TTD. Affects ES, AW, WoA and DT; in every case dropping the gate
means "press it on cooldown", which is the standard degradation.

**4. Hammer of Wrath is gated on the Avenging Wrath *buff*, not on execute range.**
Its real gate is `target.health.pct<20 | buff.avenging_wrath.up |
talent.walk_into_light`. Target health is not on the pulse at all (State has no
target channel — the same hole `specs/destruction/observability-map.md` #13
records), and a talent read is a per-build luxury we have not wired here. So the
line fires only inside wings. Outside wings and in execute range we simply **miss**
a press — a missed cue, never a wrong one.

**5. simc's two Hammer of Wrath lines are collapsed into one, at the lower
position.** `hammer_of_wrath,if=talent.walk_into_light` sits above Blade of Justice
and the plain `hammer_of_wrath` below it. We cannot read the talent, so we keep the
**lower** placement — the one that is correct for the build that does *not* have it.
⚠ **The code disagreed with this paragraph until 2026-08-03** — it had Hammer of Wrath
*above* Blade of Justice, i.e. the Walk-into-Light placement, while this text claimed the
opposite. The oracle never caught it because every Hammer of Wrath case left Blade of
Justice on cooldown, so the relative order was never exercised. There is now a case that
pins it.

**5b. simc's proc-Blade-of-Justice line carries an extra suppression we drop.** Line 45's
full condition is `(buff.art_of_war.up|buff.righteous_cause.up)&(!talent.walk_into_light|
!buff.avenging_wrath.up)` — with Walk into Light, the proc line is *suppressed during wings*.
Talent-gated, so unreadable; dropping it means L6 fires during wings on that build where
simc would skip it.

**5c. The Crusading Strikes "spend at 4" rule is not implemented.** The KB
(`knowledge/.../rotation.md`, `abilities.md`) says that on a Crusading Strikes build you
spend at 4 Holy Power when an auto-attack is about to land. Auto-attack timing is not on the
pulse at all, so on that build the HUD will consistently cue one press later than the guide.

**6. `talent.holy_flames` / `dot.expurgation.ticking` is dropped from the cooldown
gates.** Expurgation (383344) *is* tracked, so its presence is readable — but the
gate is `!talent.holy_flames|dot.expurgation.ticking`, i.e. it only bites on a
Holy Flames build, and reading the talent to know whether the gate applies is the
part we skipped. Untalented, the gate is vacuously true, so dropping it is correct
for the majority build and slightly early for the other.

**7. The opener's `blade_of_justice,if=talent.holy_flames&!dot.expurgation.ticking
&time<5` is not implemented.** It is an opener-only line (`time<5`) on a talent we
do not read. The HUD has no opener sequencer since the TCT redesign.

**8. Trinkets, potions, racials and `invoke_external_buff` are out of scope**
entirely — they are not Cooldown-Manager abilities and the HUD never cues them.
`rebuke` (the interrupt) is registered as a utility and, like every utility, is
never scored.

## Blind spots

- **Hammer of Wrath has no icon.** It is absent from Retribution's
  `CooldownSetSpell` rows entirely `[T1 DB2 @ 12.0.7]` — the same hole Destruction
  has with Incinerate. It *may* recover as a **virtual row**: `RecoveryTime` is 0
  (its cooldown lives on charge category 1895), and `State.virtualCandidates`
  admits a declared `kind = "button"`, non-utility, known ability whose
  `ns.BaseCooldown` reads 0. Whether `GetSpellBaseCooldown` really returns 0 for a
  charge-category spell is the one thing only a live pass settles. `@verify-ingame`
- **No buff durations, no stacks.** Every "remains < gcd*N" clause in the APL is
  unreachable (Deviation 1).
- **No target health** ⇒ no execute window (Deviation 4).
- **No target count** ⇒ the AoE threshold is the manual mode toggle.
- **The napkin has no countdown for four of the nine Essential buttons** (Deviation 2).
  ⚠ **This is narrower than it sounds, and the earlier wording oversold it.** Their
  *readiness* does not depend on the napkin at all — it comes from the **charge count**,
  which State seeds out of combat and maintains in combat off the `ChargeGained` alert,
  using the charge-category recovery as a **gain floor** (`ns.ReadCharges`' third return,
  already wired). What is genuinely lost is the **`SOON` decoration** and **`Escalate`'s
  overdue signal**, both of which need a positive `remaining`. Destruction has shipped this
  exact shape for Conflagrate since field-fix C2; the only difference here is four
  abilities instead of one.

## Hero-tree delta — Herald of the Sun

Not a second list; the same L1–L12 with these differences:

- **There is no Hammer of Light.** L1 finds no transform on the spender frame and
  yields nothing, so the list starts at L2. No branch is needed — the line is
  self-gating, which is the same independence `specs/destruction/rotation.md`
  relies on for Malevolence.
- The tree's identity is **Dawnlight** (431377) / **Blessing of An'she** (445206) /
  **Sun Sear** (431413) and the Sun's Avatar window. All three are tracked buffs, so
  a future line can read them; **none is in the list today**, because the KB does not
  distil Herald line-by-line and inventing an order from a tree summary would be
  guessing.
- ⚠ **Herald's spender lines are INCOMPLETE, not merely un-optimised.** **Eternal Flame**
  (156322) is a real 3-Holy-Power finisher on this tree `[T1 DB2: SpellPower @ 12.0.7]` and
  it is **not in the tracked set**, so it has no icon and no line. It is registered with
  `expect = false` — which keeps it out of the virtual-row walk, because a self-drawn button
  no line ever cues would be worse than none. Closing this properly needs the KB to distil
  Herald first.
- Wake of Ashes stays an on-cooldown press; it simply stops arming a spender.

⚠ The hero tree is resolved from **`state.hero`** (State's talent-API read,
`TraitSubTree` 48 = Templar, 50 = Herald of the Sun) and **never inferred from the
tracked set**. That inference is field-fix B: deriving the tree from a tracked
ability corrupted both answers at once on Destruction's first live session.

## Implementation notes

- **The spender frame is resolved by transform, not by ID.** `ctx.holFrame` is
  whichever tracked spender the pulse shows transformed with `spender ==
  "hammer_of_light"`, exactly as `CoachDestruction`'s `ruinationFrame` works. Which
  of the two spender frames (85256 / 53385) the client actually overrides is
  unknown offline, so **both** carry the mapping. `@verify-ingame`
- **`RET_HOL_FROM_BUFF = false`** is this spec's one parked switch (the
  `ART_FROM_RITUAL` precedent). It asks: should a present **Light's Deliverance**
  buff (433674) *by itself* arm L1, without a visible transform? Default **false** —
  only a transform arms it — because Light's Deliverance is a *stacking* buff whose
  count is secret, so its mere presence may be true for most of the cycle and would
  jam L1 permanently. Flip it if the live pass shows the buff is present only while
  a free Hammer of Light is genuinely available.
- **Hammer of Wrath resolves through a candidate walk**, not a constant: three Paladin-side
  ids exist (24275 the class skill-line castable that owns charge category 1895, 326730 a
  second skill-line row, 1241288 the Midnight talent *node*, which the KB marks PASSIVE), and
  `ctx.howKey` takes whichever the pulse actually carries — the `ctx.dotID` pattern.
  ⚠ Until 2026-08-03 the brain asked for 24275 alone while `notes.md` claimed "whichever the
  client surfaces resolves the same cue"; nothing implemented that, so a client surfacing a
  different id would have killed the line silently.
- **Charges decide readiness** wherever a charge pool exists — the count outranks
  the cooldown read, verbatim from `CoachDestruction.usable()`. Crusader Strike's
  2-charge pool (category 1627) is the case that matters most; Judgment, Blade of
  Justice, Wake of Ashes and Hammer of Wrath are 1-charge categories, and whether
  the CDM marks a 1-charge category row as `charges = true` is unsettled offline.
  `@verify-ingame`
- **Final Verdict (383328) is a talent override of Templar's Verdict**, not a
  separate button. It is mapped with `expect = false` so the expected-vs-bound diff
  never reports it missing and State's virtual-row walk never draws a second icon.

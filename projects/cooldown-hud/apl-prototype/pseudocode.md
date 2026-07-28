# Demonology Warlock — rotation priority list (APL)

This is the **spec of record** for the Demonology rotation as a flat, ordered
**action priority list**. It is evaluated top to bottom; the **first line whose
action is castable is the press**. Every line carries an implicit gate: *"the
ability is usable"* — off cooldown, procced, and affordable.

## How to read it

- **`shards`** means **projected** soul shards: the live shard count **plus any
  shards already in flight** from a cast that has not yet landed. A builder
  mid-cast adds to the projection; a spender mid-cast subtracts from it.
- **Implicit gate on every line:** the named ability is only a candidate if it is
  actually usable right now (off cooldown / procced / enough shards). A line whose
  ability is not usable is skipped and evaluation continues to the next line.
- **Abbreviations:** IB = Infernal Bolt, DB = Demonbolt, SB = Shadow Bolt,
  HoG = Hand of Gul'dan, Grim = Grimoire (Imp Lord / Fel Ravager),
  Core = Demonic Core proc.

## The priority list (as authored)

```
if Ruination:
    cast Ruination
if Tyrant is in the "Tyrant window"
   (= Tyrant is not on cooldown, OR Tyrant is within ~3 seconds of coming up by
    napkin-math cooldown):
        if shards < 2:
            cast IB (if procced)
        if shards < 4 and a Core is present:
            cast DB
        if shards < 5:
            cast SB
        if Dreadstalkers was being held, use it now
        if Grimoire:
            cast Grim
        cast Tyrant
if Dreadstalkers AND not in the Tyrant window:
    cast Dreadstalkers
if Implosion:
    cast Implosion
if shards < 3:
    cast DB (if a Core is present)
    else cast SB
cast HoG
```

## Settled clarifications (do not restructure the list — these annotate it)

1. **Pooling is emergent.** There is deliberately **no explicit "pool to N" step**
   outside the Tyrant window. The build gates (`shards < 2`, `shards < 3`) and the
   bottom filler (`HoG` / `SB`) fill the bar on their own between higher-priority
   presses.

2. **Holding Dreadstalkers is the one reactive judgment.** "not in the Tyrant
   window" on the Dreadstalkers line — and "if Dreadstalkers was being held, use it
   now" inside the window — exist so Dreadstalkers **lands fresh inside the Tyrant
   window** rather than firing on cooldown just before it. Model this *only* through
   the Tyrant-window test. Do **not** attempt to model finer Reign-of-Tyranny stack
   or fight-timer optimization; that is left to the player.

3. **Core-dump depends only on "is a Core present" (yes/no).** The Core **stack
   count** is not knowable to us, so **no line may depend on "2+ cores"** or any
   count.

4. **Implosion's true gate (a wild-imp count) is not knowable to us.** The list
   treats Implosion as castable when off cooldown. Whether that press should be
   softened to a "your call" cue because we cannot confirm the imp count is a
   question for the **input/readability contract**, not for the priority order.

5. **"Tyrant window" has two distinct senses — the list uses the SETUP sense.**
   - *Setup sense (used above):* Tyrant is off cooldown, or ~3s out by napkin math →
     run the `cap shards → stage demons → Tyrant` sequence.
   - *Buff-active sense (separate):* the Tyrant **buff** is up (post-summon) → flood
     HoG. That behavior **falls out of the bottom `cast HoG` line** and needs no
     special step.

6. **Dreadstalkers and Implosion sit BELOW the Tyrant block (corrected).** The first
   draft put them at the top (rules 2–3), which let them **preempt the Tyrant setup**:
   Implosion reads probably-up almost every pulse (its cooldown is short), so as a
   high rule it hijacked the burst window *and the opener*. Placed below the Tyrant
   block, the block owns the press whenever a Tyrant window is open; only **outside**
   the window do Dreadstalkers-on-cooldown and Implosion get a look. Dreadstalkers is
   still "off cooldown ⇒ a rotation press" — it just gets that press either as the
   **staged** summon inside the window or via its **own line** in steady state, never
   by stepping on the setup. (The staged copy inside the block is why the outside line
   keeps its `not in the Tyrant window` guard.)

> **Implementation note (W4 Phase 8).** The clean-sheet `apl.lua` evaluator that
> accompanied this prototype has been **retired**. This file remains the **spec of
> record**; the living implementation is the addon's `Coach.lua` (`RankWinner`), and
> the independent branch-coverage oracle is `CDMProbe/tests/spec/coach_apl_spec.lua`
> (authored from this document). `input-contract.md` / `observability-map.md` describe
> the same inputs the Coach's `Context` gathers from the State pulse.

## Winner and second place (for the module)

- The **winner** is the first castable line, top to bottom.
- **Second place** is what the **same list** produces when the winner's ability is
  **removed from consideration** and the list is re-evaluated from the top. (It is
  not "the next line after the winner" — a lower line may reference the same ability,
  or a skipped-then-reachable branch may change; recompute honestly.)

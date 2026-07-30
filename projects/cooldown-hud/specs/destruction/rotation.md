# Destruction Warlock — rotation priority list (APL)

This is the **spec of record** for the Destruction rotation as a flat, ordered
**action priority list**. It is evaluated top to bottom; the **first line whose
action is castable is the press**. Every line carries an implicit gate: *"the
ability is usable"* — off cooldown, procced, charged, and affordable.

> **⚠ STATUS: IMPLEMENTED, but derived and not play-settled.** Unlike
> `specs/demonology/rotation.md` (authored by the player, then annotated with
> settled clarifications), this list is **distilled from the Tier-1 simc midnight
> APL** via `knowledge/classes/warlock/destruction/rotation.md`. Every place I
> departed from the simc order is called out under **Deviations** — those are the
> lines to adjudicate before this becomes settled. **Nothing here has been flown.**
>
> **This list SHIPS** as of 2026-07-29: `CoachDestruction.lua` implements L1–L13
> line-for-line (the line numbers below are its comment labels, so the two diff by
> eye), and `tests/spec/coach_destruction_apl_spec.lua` is the independent oracle
> that pins the code to *this document*. So a change here is a change to the addon
> — edit the list, then the brain, then the oracle. What the implementation had to
> decide that this document left open is recorded in **Implementation notes** at the
> bottom.

> **v1 profile: Diabolist.** Both hero trees are live-viable (the KB calls
> Diabolist the default / best single target). Diabolist is taken as the profile
> because it reuses machinery the HUD already has confirmed for Demonology —
> Diabolic Ritual → Demonic Art → a free replacement cast. The **Hellcaller
> delta** is a separate section at the bottom, not a second list.

## How to read it

- **`shards`** means **projected** Soul Shards: the live count **plus any shards
  already in flight** from a cast that has not yet landed. A builder mid-cast adds
  to the projection; a spender mid-cast subtracts from it. ⚠ Destruction's bar is
  finer-grained than Demonology's — see **Fragments**, below.
- **Implicit gate on every line:** the named ability is only a candidate if it is
  actually usable right now (off cooldown / a charge banked / procced / enough
  shards). A line whose ability is not usable is skipped and evaluation continues.
- **Abbreviations:** CB = Chaos Bolt, Inc = Incinerate, IB = Infernal Bolt,
  Conf = Conflagrate, SB\* = Shadowburn (*never* Shadow Bolt — Destruction does not
  cast Shadow Bolt), RoF = Rain of Fire, Art = a Demonic Art proc.

## Fragments — the resource difference from Demonology

Demonology's rail is **5 discrete shards**. Destruction spends in whole shards but
**the bar reads in tenths** ("Soul Shard Fragments"): Incinerate, Conflagrate,
Soul Fire and Immolate ticks each pay out a *fraction* of a shard. That is why the
simc gates read `soul_shard<=4.2` and `>=3.5` rather than integers.

**This list rounds those to whole shards on purpose** (`shards <= 4`, `shards >= 4`),
because the fractional read is not currently available to the HUD — see
`observability-map.md` → *the fragment read*. If the fragment read is wired up, the
fractional thresholds from the KB APL are the values to restore, and they are noted
per line below.

## The priority list (as derived)

```
L1   if Ruination:                                   cast Ruination
L2   if Soul Fire and shards <= 4:                   cast Soul Fire
L3   if Art is armed:                                cast CB
L4   if Conflagrate and shards <= 4                  (simc: <= 4.2)
        and Backdraft is not stacked:                cast Conf
L5   if Summon Infernal:                             cast Summon Infernal
L6   if Chaotic Inferno and shards <= 4:             cast Inc     (simc: <= 4.6)
L7   if Shadowburn and (Fiendish Cruelty
        or target <= 20% HP):                        cast SB*
L8   if Immolate is missing or refreshable:          cast Immolate
L9   if Cataclysm:                                   cast Cataclysm
L10  if AoE and shards >= 4:                         cast RoF
L11  cast CB
L12  if shards <= 3:                                 cast IB
L13  cast Inc
```

## Deviations from the simc order (adjudicate these)

1. **Ruination moved to L1** (simc has it at #8). Rationale: it is a *free* granted
   press that **replaces Chaos Bolt on the button** — sitting on it blocks nothing
   and gains nothing, and Demonology's settled list makes the same call for its own
   Ruination. ⚠ Confirm Ruination is genuinely free for Destruction
   (`@verify-ingame`); if it costs shards, it belongs back down by L8.

2. **Summon Infernal at L5, not #4-of-a-different-shape.** simc puts Infernal after
   the Conflagrate builder, which is what L5 does. Kept faithful. But note the
   **burst-window rule is a cooldown-sync rule, not a priority-list rule** — potion,
   racials and trinkets fire *inside* the Infernal, and the list has no way to say
   that. See `notes.md` → *the burst window*.

3. **Rain of Fire added as L10 with a hard AoE gate.** simc's Diabolist branch only
   reaches RoF at very high target counts (method: "don't cast Rain of Fire until
   ~8+ targets") because Chaos Bolt keeps feeding Diabolic Ritual. The HUD reads
   `mode` (single/aoe), **not a target count**, so L10 is gated on the mode toggle
   alone and is deliberately *below* the Art/anti-cap Chaos Bolts. On Hellcaller
   this line moves up — see the delta.

4. **The fractional shard gates were rounded** (see *Fragments*). L4's `<= 4.2` and
   L6's `<= 4.6` both become `<= 4`, which is **more conservative** — it builds one
   press later than simc would. That is the safe direction (never overcap-by-guess)
   but it is a real fidelity loss, and it is the single best argument for wiring the
   fragment read.

5. **Havoc is not in the list.** simc's Havoc logic is `target_if` — "the add with
   the most time-to-die that isn't your current target, and not right before
   Infernal." The HUD has no target roster and no time-to-die, so a Havoc line
   could only ever be a "your call" cue. It is left out of the priority order and
   handled as a `judgeable = false` availability instead (`input-contract.md`).

6. **Channel Demonfire is omitted.** It is a choice node (vs Demonfire Infusion) and
   simc's placement depends on Immolate/Wither spread we cannot count. If the player
   talents it, it wants a line around L9; parked until the build is settled.

## Settled-by-derivation clarifications (annotations, not restructurings)

1. **Backdraft stacks are not knowable — L4's gate is softened.** simc gates
   Conflagrate on "no Backdraft stacked" so a 2-stack buff is not wasted. Backdraft
   is a tracked buff, so **presence** is readable; the **stack count is not** (the
   same Secret-Value wall as Demonology's Demonic Core). L4 therefore reads *"no
   Backdraft present"*, which is stricter than *"not at 2 stacks"* — it will hold
   Conflagrate at 1 stack where simc would press. **Open:** whether to soften L4 to
   presence-ignoring instead, and let the player judge.

2. **The execute gate (`target <= 20%`) is a real read, unlike Demo's imp count.**
   Target health percent is ordinary unit data, not a Secret Value — but it is not
   currently in the State pulse. See the observability map; this is a *missing
   input*, not a blind spot.

3. **Immolate maintenance is the spec's spine and the spec's biggest open question.**
   Destruction lives or dies on a fire DoT being up (it also *pays* shard fragments
   on tick). L8 needs a "is it up / is it in the pandemic window" read, which the
   pipeline does not have today — `abilities[base].uptime` is an open backlog item
   in `docs/status.md`. Until it exists, L8 cannot fire honestly.

4. **Charges are new here.** Conflagrate and Shadowburn are both 2-charge abilities.
   Demonology has **no charged tracked ability**, which is why the `charge` half of
   the full-database read is still `@verify-ingame` in `docs/status.md`. Destruction
   is the spec that closes that item. Until it is closed, L4/L7 can only see
   "off cooldown", not "how many charges are banked" — so the list will under-press
   Conflagrate rather than dump a second charge.

5. **The two Diabolist replacements split the same way Demonology's do.** Ruination
   replaces **Chaos Bolt**; Infernal Bolt replaces **Incinerate**. Chaos Bolt is in
   the tracked set, Incinerate appears **not to be** — so the Ruination half has an
   icon to light and the Infernal Bolt half does not. This is Demo's
   HoG-glowable / Shadow-Bolt-blind asymmetry transplanted exactly (`notes.md`).

## Hellcaller delta (not a second list)

Hellcaller is the sustained-AoE / long-fight tree. It changes **three** things; the
rest of the list stands:

- **Wither replaces Immolate.** L8 becomes "Wither is missing or refreshable."
  Wither is a *stacking* DoT (8 stacks arms Blackened Soul) — its **stack count is
  as unreadable as Backdraft's**, so the list can only maintain it, never play
  around its stacks.
- **Malevolence is a second burst cooldown** (~60s) that does *not* align with
  Infernal (120s / 90s w/ Inferno). It slots beside L5 as its own on-cooldown line,
  and per the KB you spend maximum shards inside its window.
- **Rain of Fire comes online much earlier** — L10 moves above the anti-cap Chaos
  Bolt, and its gate is `shards >= 4` at 5+ targets (−1 with Destructive Rapidity)
  rather than Diabolist's ~8+.

Ruination / Infernal Bolt / Demonic Art (L1, L3, L12) **do not exist on Hellcaller**;
those lines simply never fire.

## Implementation notes (what `CoachDestruction.lua` had to decide)

These are the places the list above was under-specified for code, and the call that
was made. They are the first things to revisit after a live pass.

1. **L1 vs L3 — what does "Art is armed" actually read off?** The two lines look
   distinct but collapse under observation: the only unambiguous "the Art is armed"
   signal is the **transform** (a Chaos Bolt frame overridden to Ruination), and that
   is already L1's read. `observability-map.md` #4 suggests the Diabolic Ritual aura
   `428514` as a second source — but that is the ritual **container**, and the KB's
   simc line gates on a separate `demonic_art` buff. If the container is up for most
   of the cycle, using it would pin Chaos Bolt above Conflagrate and Summon Infernal
   permanently. **Decision:** L3 is transform-only by default
   (`spec.ART_FROM_RITUAL = false`); flip that one boolean if the live pass shows the
   container is honest. So today L3 is reached only in the second-place recompute.

2. **L5b — Malevolence needed a line of its own.** The Hellcaller delta says
   "Malevolence slots beside L5", which is now an explicit line **below** Summon
   Infernal. Both are plain on-cooldown presses and neither waits for the other, per
   `notes.md`. Hero tree is detected **structurally** — a tracked Wither means
   Hellcaller — so there is no talent-API branch anywhere.

3. **L8 is half-live, not dead.** The draft assumed the DoT line could not fire at
   all. It fires on **positive evidence of absence** (the tracked Immolate/Wither aura
   reads inactive *and the read succeeded*); the pandemic-refresh half is still blocked
   on `abilities[base].uptime`. The three-way `up` / `missing` / `unknown` distinction
   is load-bearing — an *unreadable* DoT must stay silent, because treating "no read"
   as "not up" would spam the refresh press every GCD.

4. **L10's Hellcaller delta needed no branch.** "Rain of Fire moves above the anti-cap
   Chaos Bolt" is already true of the base list (L10 sits above L11), and the part that
   differs between trees is a *target count* we cannot read either way. The mode toggle
   covers both trees; only the shard floor is expressed.

5. **Charges are now read, out of combat only.** L4/L7 treat "a charge is banked" as
   usable even while the recharge timer runs — but `C_Spell.GetSpellCharges` is secret
   in combat, so in a pull they fall back to binary off-cooldown and the list
   under-presses, exactly as clarification 4 predicted.

## Winner and second place (for the module)

Identical contract to Demonology:

- The **winner** is the first castable line, top to bottom.
- **Second place** is what the **same list** produces when the winner's ability is
  **removed from consideration** and the list is re-evaluated from the top. It is
  not "the next line after the winner" — Chaos Bolt appears at L3, L11 (and Incinerate
  at L6, L13), so removing an ability must suppress *every* line that names it, and
  a skipped-then-reachable branch may change the answer. Recompute honestly.

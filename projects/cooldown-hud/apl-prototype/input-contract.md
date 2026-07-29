# Input contract — Demonology APL evaluator

> **⚠ STATUS: reference-only.** The standalone `apl.lua` prototype was retired — its
> logic lives in the shipped `Coach.lua` (which `Coach.Context` gathers these same inputs
> for). This doc is kept as the **specification of the inputs** the priority list needs;
> `pseudocode.md` remains the rotation spec of record. Read it to understand what the
> Coach's context-gather must produce, not as a description of a separate module.

This is the **caller-facing** contract for the APL evaluator. It describes precisely what
information the priority list needs, one field per real rotation fact the list
reads. The evaluator is a pure function: it evaluates the settled
priority list in `pseudocode.md` top-to-bottom and returns the winner + a
second-place recompute. It does **no** observation of its own — the caller is
responsible for producing every field below from the live game state.

Design principle: **minimal and rotation-grounded.** Every field maps to exactly
one fact the list reads. There are no speculative extras, and no field encodes a
Core *count* or an imp *count* (both are unknowable to us — see notes).

## KB grounding

Ability names, shard costs/yields, and the Tyrant / Dreadstalkers / Grimoire /
Core relationships were sanity-checked against the WoW knowledge base (not any
addon):

- `knowledge/classes/warlock/demonology/rotation.md` — the distilled Tier-1 simc
  APL: builder/spender core, the Tyrant window as the central lever, Dreadstalkers
  timed to land fresh inside Tyrant, Infernal Bolt (builds 3 shards, cast ≤2
  shards) as the Demoniac replacement for Shadow Bolt, Demonbolt as the Core
  spender, Hand of Gul'dan as the imp generator / shard dump.
- `knowledge/classes/warlock/demonology/abilities.md` — canonical ability names,
  resource costs, and the Demonic Core proc system (0–4 stacks, count not exposed);
  Implosion consumes Wild Imps.
- `knowledge/classes/warlock/demonology/diabolist-sequences.md` — confirms Ruination
  and Infernal Bolt are *free auto-replacements* (Ruination replaces HoG, Infernal
  Bolt replaces Shadow Bolt when armed), and the "hold Tyrant a beat so
  Dreadstalkers / Grimoire land inside it" burst idea the window test models.

## The input table

A single flat Lua table of plain data (numbers / booleans). Fields:

| Field | Type | Default | Meaning / rotation concept | Read by |
|---|---|---|---|---|
| `shards` | number (0–5) | `0` | **Projected** Soul Shards: live count **plus shards in flight** from an unlanded cast (a builder mid-cast adds; a spender mid-cast subtracts). This is the pivot for every `shards < N` gate. | L4, L5, L6 |
| `ruination_up` | boolean | `false` | Ruination proc is armed (the Diabolist finisher that auto-replaces Hand of Gul'dan). "if Ruination" in the list = this proc is up **and** therefore castable. | L1 |
| `dreadstalkers_usable` | boolean | `false` | Call Dreadstalkers is **off cooldown and affordable** (2 shards, or free with Demonic Calling). Pure usability; the *when* is decided by the window fields. | L2, L6 |
| `tyrant_window` | boolean | `false` | **SETUP sense** of "Tyrant window": Summon Demonic Tyrant is **off cooldown, OR within ~3s of coming up** by napkin-math cooldown. Gates the whole L6 setup block, and (negated) gates L2 so Dreadstalkers is *held* as the window approaches. **Not** the buff-active sense (see notes). | L2, L6 |
| `dreadstalkers_held` | boolean | `false` | Reactive-hold flag: Dreadstalkers was **deliberately held** (deferred by L2 because the window was near) and is now waiting to be released inside the window. Distinct from `dreadstalkers_usable`. | L6 |
| `implosion_usable` | boolean | `false` | Implosion is castable (off cooldown). Its *true* gate (a Wild-Imp count) is unknowable to us, so this is "off cd" only — see the softening note below. | L3 |
| `ib_usable` | boolean | `false` | Infernal Bolt is castable ("procced"/armed). The list's L4 casts it only when `shards < 2`, as the fast shard-refill builder. | L4 |
| `core_present` | boolean | `false` | **A Demonic Core proc is present (yes/no).** This single boolean is also the usability gate for Demonbolt: the list only ever casts Demonbolt "if a Core is present" (instant + affordable with a Core), so no separate `db_usable` field exists. The Core stack **count is not modeled** — no line depends on "2+ cores". | L5, L6 |
| `grimoire_usable` | boolean | `false` | Grimoire (the talented one — Imp Lord for AoE, Fel Ravager for ST) is off cooldown and castable. Staged inside the Tyrant window. | L6 |
| `tyrant_castable` | boolean | `false` | Summon Demonic Tyrant is **off cooldown right now** and affordable (1 shard). Distinct from `tyrant_window`: the window opens ~3s early so the setup runs, but the final "cast Tyrant" step only fires once it is actually castable. | L6 |
| `sb_usable` | boolean | `true` | Shadow Bolt is castable. No cooldown / no cost, so this defaults to `true`; set `false` only if genuinely locked out (e.g. silenced). It is the low-shard / pool-to-5 builder. | L5, L6 |
| `hog_usable` | boolean | `true` | Hand of Gul'dan is affordable/castable — the bottom filler and the list's floor. Defaults `true`. If it is ever `false` and nothing higher fires, the evaluator returns a "nothing castable" result. | L7 |

Any field omitted takes its default. Omitting a usability boolean therefore means
"that ability is not usable," the safe reading of an unknown fact.

## The derived / ambiguous facts, called out

- **Projected `shards` (`shards`)** — the caller must fold *in-flight* shards into
  the number, not just the current resource. A builder mid-cast counts its future
  shards; a spender mid-cast subtracts what it will consume. The list's `< 2 / < 3
  / < 4 / < 5` thresholds are all read against this projection.

- **Per-ability usability** — every line carries an implicit "the ability is
  usable" gate (off cooldown / procced / affordable). That gate is surfaced as the
  per-ability booleans above (`ruination_up`, `dreadstalkers_usable`,
  `implosion_usable`, `ib_usable`, `grimoire_usable`, `tyrant_castable`,
  `sb_usable`, `hog_usable`) plus `core_present` standing in for Demonbolt.

- **"Is a Core present" is a boolean, never a count** (`core_present`). The Demonic
  Core stack count is not knowable to us, so no field or line depends on "2+ cores."
  Both Demonbolt gates (L5 and L6) read this single yes/no.

- **Two distinct Tyrant senses.** `tyrant_window` is the **SETUP** test (off cd OR
  ~3s out) that runs the cap-shards → stage-demons → Tyrant sequence. The separate
  **buff-active** sense (the Tyrant *buff* is up post-summon → flood Hand of
  Gul'dan) is **not** an input: that behavior falls out of the bottom `L7 cast HoG`
  line on its own and needs no field. `tyrant_castable` is the narrower "off cd
  right now" fact used only for the final cast step.

- **"Dreadstalkers was being held" (`dreadstalkers_held`)** is the one reactive
  judgment in the rotation, per clarification 2. L2 holds Dreadstalkers when the
  window is near (`not tyrant_window` is false); L6 releases it (`dreadstalkers_held
  and dreadstalkers_usable`) so it lands fresh inside the window. Model the hold
  **only** through the window test — do not attempt Reign-of-Tyranny stack or
  fight-timer optimization here; that is the player's call.

- **Implosion's unknowable imp-count gate (`implosion_usable`).** The list treats
  Implosion as castable when off cooldown (clarification 4). Because we cannot
  confirm the Wild-Imp count that makes the press correct, **the softening decision
  lives here in the contract, not in the priority list.** Recommended caller
  behavior: still feed `implosion_usable = true` when off cooldown so L3 can win,
  but present that particular press to the player as a *"your call"* cue (it may be
  wrong if imps are few) rather than a hard command. The priority order is
  unchanged; only the display confidence of an L3 win is softened.

## Return shape

`M.evaluate(state)` returns:

```lua
{
  winner = { ability = <string>, rule = <string>, why = <string> },
  second = { ability = <string>, rule = <string>, why = <string> },
}
```

- `ability` — one of `M.ABILITY` (e.g. `"Ruination"`, `"Call Dreadstalkers"`,
  `"Hand of Gul'dan"`).
- `rule` — the matched line identifier (`"L1"`, `"L5.DB"`, `"L6.Tyrant"`, …) so the
  result is auditable, not an oracle.
- `why` — a human-readable reason string.
- **Nothing castable:** if no line fires, that slot is `{ ability = nil, rule =
  "none", why = ... }`. In practice the winner is always castable (Shadow Bolt /
  Hand of Gul'dan are the always-available floor); the nothing-castable result
  shows up mainly as the *second* place when the winner is the last remaining floor
  filler.

### Second place — how it is computed

Second place is **not** "the next line after the winner." The evaluator removes the
winner's *ability* from consideration **everywhere it appears** and re-evaluates the
entire list from the top. This matters because:

- A lower line may name the same ability (e.g. Demonbolt is in both L5 and L6;
  Dreadstalkers in both L2 and L6). Removing it must suppress *all* of them.
- Previously-skipped fallback branches become reachable. Example: if the winner is
  Demonbolt via `L5.DB` (shards < 3, Core present), removing Demonbolt lets the
  L5 Shadow Bolt fallback surface as second place — the honest "what would I press
  instead" answer, not a pool-past-the-gate press.

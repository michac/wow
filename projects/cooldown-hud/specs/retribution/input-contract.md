# Input contract — Retribution APL evaluator

> **⚠ STATUS: reference / specification.** There is no standalone evaluator module —
> the shipped logic lives in **`CoachRetribution.lua`** (`spec:RankWinner`), and
> **`spec:Context`** is what gathers these inputs from the State pulse. Every field
> below has a real `ctx.*` counterpart there; where the field is absent from the
> pulse (`target_execute`) the brain reads the shape it *would* take, so it stays
> nil-safe today and correct the day State grows the channel. `Coach.lua` is the
> generic shell and holds no Retribution logic. `rotation.md` remains the rotation
> spec of record.

This describes precisely what information the priority list needs — one field per
real rotation fact the list reads. The evaluation is pure: it walks the list in
`rotation.md` top to bottom and returns the winner plus a second-place recompute. It
does **no** observation of its own; the caller produces every field below.

Design principle: **minimal and rotation-grounded.** Every field maps to exactly one
fact the list reads. No field encodes a **buff duration**, a **stack count**, a
**target count** or **target health** — all four are unreadable (see
`observability-map.md`), and inventing a field for one would be a promise the
pipeline cannot keep.

## KB grounding

Ability names, Holy Power costs, and the Templar Hammer-of-Light loop were checked
against the WoW knowledge base and Tier-1 game data (not any addon):

- `knowledge/classes/paladin/retribution/rotation.md` @ 12.0.7 — the distilled
  Tier-1 simc APL: the Holy Power economy, the Wake of Ashes → Hammer of Light
  loop, the Avenging Wrath / Execution Sentence pairing, the Radiant Glory variant.
- `ActionPriorityLists/default/paladin_retribution.simc` @ `ab7b0b8` (2026-08-01) —
  the generated default APL this list is distilled from, line for line.
- wago DB2 @ 12.0.7 (`CooldownSetSpell` 901, `SpellPower`, `SpellCategory`,
  `TraitNode`→`TraitDefinition`) — every spell ID in `notes.md`, the 3-Holy-Power
  spender cost, and the charge categories behind **four** of the nine Essential buttons
  (*"six" until 2026-08-03 — see `observability-map.md` §Retribution's headline hole*).

## The input table

A single flat table of plain data (numbers / booleans / spellIDs).

| Field | Type | Default | Meaning / rotation concept | Read by |
|---|---|---|---|---|
| `hp` | number (0–5) | `0` | **Projected** Holy Power: the live count plus anything in flight from an unlanded cast. `modifier` is 1, so this is a plain integer. | L4, L8 |
| `hpMax` | number | `5` | The cap, live off the pulse. L4 is "at cap", not "at 5". | L4 |
| `spenderCost` | number | `3` | Live Holy Power cost of the chosen spender, resolved through `env.shardCostFn`. **Never hardcoded at a call site** — it is talent-modifiable. | L4, L8 |
| `holFrame` | spellID \| nil | `nil` | The BASE spellID of the tracked spender frame currently showing a **Hammer of Light** override. Non-nil ⇒ Hammer of Light is armed. | L1 |
| `spenderKey` | spellID \| nil | `nil` | Which spender the finisher block resolves to *right now* — Divine Storm when `dsCastable`, else Templar's Verdict. | L4, L8 |
| `dsCastable` | bool | `false` | `(aoe mode ∨ Empyrean Power) ∧ ¬Empyrean Legacy`. simc's `variable.ds_castable`, with the target count replaced by the mode toggle. | spender choice |
| `mode` | `"st"` \| `"aoe"` | `"st"` | The **manual** target-mode toggle. A player *declaration*, never an observation. | `dsCastable` |
| `artOfWar` | bool | `false` | Art of War (406064) present — a free instant Blade of Justice. | L7 |
| `righteousCause` | bool | `false` | Righteous Cause (402912) present. Same slot as Art of War. | L7 |
| `empyreanPower` | bool | `false` | Empyrean Power (326732) present — the next Divine Storm is free. | `dsCastable` |
| `empyreanLegacy` | bool | `false` | Empyrean Legacy (387170) present — the next Templar's Verdict cleaves, so it **suppresses** Divine Storm. | `dsCastable` |
| `lightsDeliverance` | bool | `false` | Light's Deliverance (433674) present — a **free** Hammer of Light. Gated behind `RET_HOL_FROM_BUFF`, default off. | L1 (parked) |
| `wingsUp` | bool | `false` | Avenging Wrath (31884) buff present. The readable half of Hammer of Wrath's gate. | L9 |
| `executionUsable` | bool | `false` | Execution Sentence is a press right now (charge-aware readiness). | L2 |
| `wingsUsable` | bool | `false` | Avenging Wrath is a press right now. | L3 |
| `woaUsable` | bool | `false` | Wake of Ashes is a press right now. Also **suppresses** L4 — at cap with WoA ready you press WoA, because it arms Hammer of Light. | L4, L5 |
| `tollUsable` | bool | `false` | Divine Toll is a press right now. | L6 |
| `bojUsable` | bool | `false` | Blade of Justice is a press right now. **Charge-aware** (category 2128). | L7, L10 |
| `judgmentUsable` | bool | `false` | Judgment is a press right now. **Charge-aware** (category 1663). | L11 |
| `howUsable` | bool | `false` | Hammer of Wrath is a press right now. **Charge-aware** (category 1895). ⚠ May be structurally false — it has no tracked icon. | L9 |
| `fillerKey` | spellID \| nil | `nil` | The **Crusader Strike frame** (35395), whatever override it is showing. Presented as one key on purpose: the Templar Strike → Templar Slash alternation is Blizzard's, not ours. **Charge-aware**, 2 charges. | L12 |
| `facts` | map | `{}` | base spellID → the shell's Classify record. Every `key(id)` in the cascade is "is this ability tracked at all"; an untracked line yields nil and evaluation continues. | every line |
| `hero` | string \| nil | `nil` | `"templar"` \| `"herald-of-the-sun"`, off **`state.hero`** (State's talent-API read). Never inferred from the tracked set — that is field-fix B. | delta section |

## Fields that deliberately do NOT exist

Each of these is a real gate in the simc APL, and each is omitted rather than
faked. Adding one would be a promise the pipeline cannot keep.

| Absent field | Why | Consequence |
|---|---|---|
| `targetHealthPct` | State has no target channel at all. Not secrecy — an absent capability. | L9 loses its execute half (`rotation.md` Deviation 4). |
| `activeEnemies` | No target roster. | Replaced by the manual `mode` toggle. |
| `buffRemains(x)` | Buff durations are Secret Values in combat. | All four of simc's free-Hammer-of-Light timing clauses are unreachable (Deviation 1). |
| `buffStacks(x)` | Same wall. | Light's Deliverance's stack count is invisible ⇒ `RET_HOL_FROM_BUFF` defaults false. |
| `cooldownRemains(x)` for a *different* ability | `GetSpellCooldown` is secret in combat, and the napkin has nothing to count down from for the six charge-category abilities. | The ES ↔ WoA handshake is dropped (Deviation 2). |
| `talentKnown(x)` | Readable OOC via `C_SpellBook.IsSpellKnown` (the Diabolic Embers precedent) but not wired here. | Radiant Glory / Walk into Light / Holy Flames gates are dropped; each degrades to "press it on cooldown", and Radiant Glory self-degrades because the button is simply absent. |
| `timeToDie` | Not a thing we can observe. | Every `target.time_to_die` gate dropped (Deviation 3). |

## The evaluation contract

Identical to every other spec, restated once so this file is self-contained:

- `RankWinner(ctx, excluded)` walks L1…L12 top to bottom and returns
  `(winnerKey, level, note)` — the **first** line whose ability is a candidate.
- `excluded` is a base spellID dropped at **every** line that names it, so the
  shell can recompute an honest second place by re-running the whole list. This
  matters more here than on most specs: the spender appears at **three** lines
  (L1 as Hammer of Light, L4 at cap, L8 as the dump) and Blade of Justice at
  **two** (L7 procced, L10 plain). All of them key on the same base spellID, so
  one exclusion drops every occurrence.
- `Escalate` may only raise `ROTATION → LATE` from **readable** overdue-ness.

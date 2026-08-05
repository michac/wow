# Input contract — Havoc APL evaluator

> **⚠ STATUS: reference / specification.** There is no standalone evaluator module —
> the shipped logic lives in **`CoachHavoc.lua`** (`spec:RankWinner`), and
> **`spec:Context`** is what gathers these inputs from the State pulse. Every field
> below has a real `ctx.*` counterpart there. `Coach.lua` is the generic shell and holds
> no Havoc logic. `rotation.md` remains the rotation spec of record.

This describes precisely what information the priority list needs — one field per real
rotation fact the list reads. The evaluation is pure: it walks the list in `rotation.md`
top to bottom and returns the winner plus a second-place recompute. It does **no**
observation of its own; the caller produces every field below.

Design principle: **minimal and rotation-grounded.** Every field maps to exactly one
fact the list reads. No field encodes a **buff duration**, a **stack count**, a **target
count**, **target health**, or a **sequence position** — all five are unreadable (see
`observability-map.md`), and inventing a field for one would be a promise the pipeline
cannot keep.

## KB grounding

Ability names, Fury costs, the meta override pair and the hero-tree split were checked
against the WoW knowledge base and Tier-1 game data (not any addon):

- `knowledge/classes/demon-hunter/havoc/rotation.md` @ 12.0.7, **confidence: high** —
  the distilled Tier-1 APL plus method.gg / Icy Veins framing: the demon-form loop, the
  Eye Beam ↔ Vengeful Retreat pairing, the Essence Break window, both hero branches.
- `ActionPriorityLists/default/demonhunter_havoc.simc` @ `ab7b0b8` (2026-08-01) — the
  generated default APL this list is distilled from, line for line. **140 lines, 24
  variables, 3 sub-lists.**
- wago DB2 @ 12.0.7 (`CooldownSetSpell` **1599**, `SpellCooldowns`, `SpellCategories` +
  `SpellCategory`, `SpellPower`, `SpellAuraOptions`, `SpellEffect`, `SkillLineAbility`) —
  every spell ID in `notes.md`, the four Fury costs, the three lying base cooldowns, and
  the five override pairs (resolved by `EffectAura == 332`, never by name).

## The input table

A single flat table of plain data (numbers / booleans / spellIDs).

| Field | Type | Default | Meaning / rotation concept | Read by |
|---|---|---|---|---|
| `fury` | number (0–120) | `0` | Live Fury off the exact rail. `modifier` is 1, so this is a plain integer — **no fragment arithmetic**. | L6, L11, L12 |
| `furyProjected` | number | `= fury` | Fury plus any in-flight cast's signed delta. Spenders only (see `rotation.md` note 5). | L8, L13 |
| `furyMax` | number | `120` | The cap, live off the pulse. | L11, L12, `Escalate` |
| `spenderCost` | number | `40` | Live Fury cost of the spender **as it will actually be pressed** — Annihilation's own ID in meta, Chaos Strike's outside. Resolved through `env.powerCostFn` against `Enum.PowerType.Fury`. **Never hardcoded at a call site.** | L8, L13 |
| `spenderKey` | spellID \| nil | `nil` | The base spellID of the Chaos Strike frame (162794), whatever it is showing. One key on purpose: the Chaos Strike → Annihilation swap is Blizzard's, not ours. | L8, L13 |
| `inMeta` | bool | `false` | Demon form is active. Read from **two ORed sources**: the Metamorphosis TrackedBuff row (191427) and the Chaos Strike frame's meta transform (`live == 201427`). The one fork in the list. | L6, L7, L10 |
| `mode` | `"st"` \| `"aoe"` | `"st"` | The **manual** target-mode toggle. A player *declaration*, never an observation. Every `active_enemies>=N` collapses to this. | L4, L14 |
| `rgFrame` | spellID \| nil | `nil` | The base spellID of a Throw Glaive frame showing the **Reaver's Glaive** override (442294). Non-nil ⇒ a Reaver's Glaive is armed. The only readable Aldrachi Reaver signal. | L1 |
| `rgArmed` | bool | `false` | `rgFrame ~= nil`, OR the Art of the Glaive buff when `HAVOC_RG_FROM_BUFF` is on (default **off**). | L1, L3 |
| `ebWindow` | bool | `false` | An Essence Break window is open — `ns.Coach.CommittedWithin(state, 258860, 4.0)`, from **cast history** against the debuff's 4000 ms DB2 duration. Not an aura read: 320338 has no CDM row. | L3, L8 |
| `innerDemon` | bool | `false` | Inner Demon (389693) present. **Vetoes** Metamorphosis — simc's `!buff.inner_demon.up`. | L2 |
| `initiative` | bool | `false` | Initiative (388108) present. **Vetoes** Vengeful Retreat: you already have the buff it exists to proc. | L5 |
| `metaUsable` | bool | `false` | Metamorphosis is a press right now. | L2 |
| `huntUsable` | bool | `false` | The Hunt is a press right now. | L3 |
| `eyeBeamUsable` | bool | `false` | Eye Beam is a press right now. | L9 |
| `eyeBeamSoon` | bool | `false` | Eye Beam's **napkin** `remaining` is ≤ 1.5 s. ⚠ The one cross-ability timing read in the file — legitimate only because Eye Beam's 30 s cooldown lives on the **spell row**, so the napkin can honestly count it. | L5 |
| `bladeDanceUsable` | bool | `false` | Blade Dance is a press right now. Charge-free (`CategoryRecoveryTime` 15 000). | L2, L7, L10 |
| `essenceBreakUsable` | bool | `false` | Essence Break is a press right now. The only Essential with an honest `RecoveryTime`. | L6 |
| `immoUsable` | bool | `false` | Immolation Aura is a press right now. **Charge-aware** (category 1676, 1 charge). ⚠ Its base cooldown read is a **lie** — see `rotation.md` → *The two lying cooldowns*. | L4, L12 |
| `felbladeUsable` | bool | `false` | Felblade is a press right now. Honest 12 s `RecoveryTime`. Filed CDM-**Utility**; `cadence = "filler"` is what makes it cueable. | L11 |
| `vrUsable` | bool | `false` | Vengeful Retreat is a press right now. **Charge-aware** (category 1601, 1 charge). Filed CDM-Utility; `cadence = "oncd"`. | L5 |
| `felRushUsable` | bool | `false` | Fel Rush is a press right now. **Charge-aware** (category 1545, 1 charge). ⚠ The sharpest lying-cooldown case: base reads **1 s** against a real **10 s**. | L14 |
| `throwGlaiveUsable` | bool | `false` | Throw Glaive is a press right now. **Charge-aware** (category 1612, 1 charge). | L15 |
| `facts` | map | `{}` | base spellID → the shell's Classify record. Every `key(id)` in the cascade is "is this ability tracked at all"; an untracked line yields nil and evaluation continues. | every line |
| `powers` | array | `{}` | The generic power array the shell's `ResourceBars` emits from. One entry: Fury, `display = "none"`. | the shell |
| `hero` | string \| nil | `nil` | `"fel-scarred"` \| `"aldrachi-reaver"`, off **`state.hero`** (State's talent-API read). Never inferred from the tracked set — that is field-fix B. **No line reads it today** (`rotation.md` → hero trees). | delta section |

## Fields that deliberately do NOT exist

Each of these is a real gate in the simc APL, and each is omitted rather than faked.
Adding one would be a promise the pipeline cannot keep.

| Absent field | Why | Consequence |
|---|---|---|
| `rendingStrike` / `glaiveFlurry` | **No `CooldownSetSpell` row** in set 1599 for 442442 or 442435. There is no presence channel, not a secret one. | The whole Reaver's Glaive spend sequence is unimplementable (Deviation 1). Six APL lines dark. |
| `rgSequenceStep` | simc's `variable.rg_inc` / `rg_ds` are sim-internal state, and the buffs that would reconstruct them are the row above. | L1 says "press it"; nothing says what to spend it on. |
| `inertiaTrigger` | The tracked row 427640 is the **talent**; 427641 is the consumed buff; the *trigger* is a third aura with no row. Reading the talent's presence as "armed" is the Light's Deliverance mistake. | Three inertia-consumer lines dropped (Deviation 2). |
| `buffStacks(x)` | The buff channel is `item:IsActive()`, a **bool**. Every stacking buff's count also sits behind a talent ID whose `CumulativeAura` reads 0. | `cycle_of_hatred.stack`, `immolation_aura.stack`, `soul_fragments.total` all dropped (Clarification 2). |
| `buffRemains(x)` | Buff durations are Secret Values in combat. | `buff.metamorphosis.remains<gcd.max` (the "meta is ending, dump now" line) is dropped; L7 fires on Blade Dance's own readiness instead. |
| `activeEnemies` | No target roster. | Replaced by the manual `mode` toggle (Deviation 7). |
| `targetHealthPct` / `timeToDie` | State has no target channel at all. Not secrecy — an absent capability. | Every `fight_remains` / `target.time_to_die` gate dropped. |
| `cooldownRemains(x)` **as a client read** | `C_Spell.GetSpellCooldown` is secret in combat (settled game-wide). | Every `cooldown.X.remains<=N` alignment gate dropped — Meta's :103 block, The Hunt's :115 block, the inertia timing (Deviations 11, 12). |
| `talentKnown(x)` | Readable OOC via `C_SpellBook.IsSpellKnown` (the Diabolic Embers precedent) but not wired here. | `use_blade_dance`, `tg_spender`, `cs_machine`, `pool_glaive_tempest` all dropped or defaulted (Deviations 8, 9). A talented-out ability self-degrades: it is simply not tracked, the line finds nothing, evaluation continues. |
| `furyGenPerSec` | simc computes it from six terms including haste and three buff stacks. | Every `fury.deficit > gen*gcd` gate becomes a flat deficit threshold (L11, L12). |
| `soulFragments` | Havoc has no fragment channel and needs none — `spec.derived` is declared **absent** on purpose (`notes.md`). | One ORed alternative on one APL line (:134) loses one of its three disjuncts. |

**One field is present that looks like it belongs above, and the distinction matters.**
`eyeBeamSoon` is a `cooldownRemains` read — but of **our own napkin**, not the client.
Eye Beam's cooldown lives on the spell row (`CategoryRecoveryTime = 30000`), so
`ns.BaseCooldown` reads it honestly and the countdown is the same number `SOON` already
draws. The rule that separates it from every dropped gate above: *a cross-ability timing
read is allowed when the other ability's cooldown is one the napkin can honestly count.*
Retribution's dropped ES↔WoA handshake fails that test (Wake of Ashes is charge-category,
base cooldown 0); this passes it.

## The evaluation contract

Identical to every other spec, restated once so this file is self-contained:

- `RankWinner(ctx, excluded)` walks L1…L15 top to bottom and returns
  `(winnerKey, level, note)` — the **first** line whose ability is a candidate.
- `excluded` is a base spellID dropped at **every** line that names it, so the shell can
  recompute an honest second place by re-running the whole list. Three abilities appear
  twice here — Immolation Aura (L4 AoE, L12 Fury), Blade Dance (L7 meta, L10 non-meta)
  and the spender (L8 window, L13 dump) — and each pair keys on one base spellID, so one
  exclusion drops both occurrences.
- `Escalate` may only raise `ROTATION → LATE` from **readable** overdue-ness. On Havoc
  that means the four spell-row cooldowns (Metamorphosis, Eye Beam, The Hunt, Blade
  Dance) and a Fury-at-cap rule. **Nothing on a charge category** — a charged ability
  raises `Available` on every restore, so its ready-edge latches and `overdue` would fire
  constantly.

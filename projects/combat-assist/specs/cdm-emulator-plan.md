# Plan — drive the preview from state, not from hand-drawn rows

⚠ **Status: a plan, not a specification.** Nothing here is agreed. It is written to be argued
with, and §8 lists the decisions it is waiting on. It is a temporary planning artifact in the
sense `CLAUDE.md` uses — not a ninth permanent document, and it should go to `specs/archive/`
once its stages land or are abandoned, the way the simplification and rule-split artifacts did on
2026-09-01.

## 1. The problem this solves

Every scenario is authored **twice**, in two languages that cannot be compared.

```
- **State.** … single target, no procs, **Holy Power 5**. …          <- English
- **CDM row.** … Divine Toll `overcap` · Final Verdict `press` · …   <- the picture
```

Nothing checks that the second follows from the first. The English is decoration; the picture is
what renders. If they disagree, the preview shows a state that cannot occur and nothing objects.

Three costs, all observed rather than hypothetical:

1. **A silent gap in Havoc.** Blizzard tints an unaffordable icon (`0.5, 0.5, 1.0` — see
   `knowledge/addon-dev/cooldown-manager.md` §3.4). Retribution declares that per icon;
   **Havoc declares it nowhere**, so ST-11's two starved spenders render at full colour. Not a
   bug in the renderer — an author has to remember, on every icon, and for Havoc nobody did.
2. **The picture cannot contradict the author.** RET-1 was authored pressing Avenging Wrath.
   The APL presses Blade of Justice on a Holy Flames build, because both cooldowns are gated on
   `dot.expurgation.ticking`. The row rendered exactly as typed, confidently, and only a human
   reading the APL caught it.
3. **Exploration is impossible.** Thirteen states exist because thirteen were typed. Nobody can
   ask *"what does the row look like at 4 Holy Power with Art of War up and Wake of Ashes 3s
   out?"* without authoring that scenario first — which is the wrong way round, because the
   states worth looking at are the ones nobody thought to author.

## 2. What the game data already gives us

Verified against `raw/wago/` @ 12.1.0.69214 before writing this.

| Table | Columns that matter | What it answers |
| --- | --- | --- |
| `CooldownSet` | `ID`, `ChrSpecialization` | which set belongs to a spec (Retribution = 901) |
| `CooldownSetSpell` | `CooldownSetID`, `SpellID`, `Category`, `OrderIndex`, `PlayerConditionID` | which rows exist, in which viewer, and which are condition-gated |
| `SpellPower` | `SpellID`, `PowerType`, `ManaCost`, `PowerCostPct`, `RequiredAuraSpellID` | what an ability costs, **and under what condition** |
| `SpellMisc` | `SpellIconFileDataID` | icon art (already used) |

⚠ **`OrderIndex` is Blizzard's order, NOT cap's.** Retribution's DB2 order is Judgment 2,
Crusader Strike 3, Blade of Justice 4, Wake of Ashes 5, Execution Sentence 6, Divine Toll 7,
Avenging Wrath 8 — nothing like `catalog.md`'s authored order, because `Anchor.lua` re-anchors the
viewer to the catalog. **The data supplies membership; the catalog supplies order.** Anyone
reconciling the two by editing the catalog has it backwards.

⚠ **Cost is conditional and that is the whole trick.** `SpellPower` rows carry
`RequiredAuraSpellID`. Throw Glaive's single row is gated on `393029` (Furious Throws), so it is
free unless talented — which is why the client once reported it affordable while we believed the
table said 25 Fury. Hammer of Light carries **two** rows at 3 Holy Power, discriminated by
`137027` / `137028`. So a cost model is buildable, provided the emulator reads the condition
column and the scenario declares its talents. (`security-taint-and-restricted-data.md` §4.11
trap 2 said the opposite until 2026-08-19; it was generalised from one sample.)

## 3. What the emulator computes

Only what the **client itself** computes when it paints a row. Every rule below is already
documented, and the citation is the point — this is transcription, not invention.

| Output | Rule | Source |
| --- | --- | --- |
| desaturated | `cooldownDesaturated = isOnActualCooldown` — cooldown, never usability | `cooldown-manager.md` §3.4 |
| swipe | the cooldown branch, on the **displayed** spell | §3.1.1 |
| icon tint | four-way ladder: out-of-range > usable > insufficient power > otherwise unusable | §3.4 |
| affordability | `SpellPower` cost for the row's power type vs declared resource, honouring `RequiredAuraSpellID` against declared talents | §2 above |
| charges | a **different** identity ladder — `overrideSpellID or spellID`, skipping the aura and linked rungs | §3.3 |
| GCD | `isOnGCD` is excluded from `isOnActualCooldown`, so a GCD does not desaturate | §3.4, §5 |

Everything cap draws on top — the scan edge, badges, the walk — is a separate layer and is
untouched by this. Whether cap's own badges later become computed from the same inputs is a real
question and a later stage (§7.5), not a prohibition.

## 4. Where it must render UNKNOWN

**A confidently wrong emulator is worse than the blank icons we have now**, because the whole
point is that you would believe it. So the model needs a third state everywhere it has two.

- A spell with **no** `SpellPower` row is free — that is a real answer, not a missing one.
- A spell whose cost is gated on an aura the scenario has not declared is **unknown**, not free.
- A `PlayerConditionID` we do not evaluate makes the row's *presence* unknown.
- Range and "otherwise unusable" are not derivable from static data at all; they are declared or
  they are unknown.

Unknown must be **visible** on the page — a hatch, a question mark, something that reads as "the
model has nothing to say here" and cannot be mistaken for "the client draws nothing here."

## 5. The scenario's inputs

The `- **State.**` prose stays for humans. A fenced block beside it becomes authoritative:

```yaml
holy_power: 5
talents: [holy_flames, templar_strikes]
cooldowns: { wake_of_ashes: down, avenging_wrath: down, execution_sentence: down }
procs: []
aoe: false
```

**The rendered page shows the block, not the prose**, so the two cannot drift where it matters.
Cooldown states are coarse (`up` / `down` / a number of seconds for the sealed bands) because the
scenarios are arguments about ordering, not a timeline.

## 6. What stays hand-authored, and why

- **The walk and the press.** The catalogs are a written argument about ordering. That argument
  is the deliverable; a computed press would not be one.
- **Display identity** — which spell a transforming row is showing. The client picks it through a
  five-rung ladder over auras (`cooldown-manager.md` §2); simulating it means simulating auras.
  Scenarios already name the displayed spell, which is the honest place for it. (§8, decision 2.)
- **Cap's markers**, for now.

## 7. Stages, each useful alone

1. **Row membership from `CooldownSetSpell`.** Replaces the hand-typed roster and immediately
   *audits* it: which rows the catalog claims vs which the game has, per category. Cheap, and it
   checks something currently asserted.
2. **Machine-readable inputs** (§5) parsed and rendered. No emulation yet — the page just shows
   the declared state. Kills the prose/picture drift on its own.
3. **The paint emulator** (§3), replacing the hand-declared client layer. Havoc's missing tints
   stop being an audit item and become impossible.
4. **Controls on the page** — a Holy Power slider, proc and cooldown toggles. This is the payoff:
   you stop authoring states and start *finding* the ones where the row reads wrong.
5. **Per-spec massage**, and the open question of whether cap's own markers become computed too.

Stage 4 is the prize. Stages 2–3 pay for themselves by deleting an error class.

## 8. Decisions this plan is waiting on

1. **Do the hand-authored rows stay once the picture is computable?**
   *Recommend: DO NOT DECIDE YET — the question is not live until stage 5.*

   The rows are the `- **CDM row.**` bullets: 285 entries across the two specs (Havoc 168,
   Retribution 117). Measured, they are mostly clerical —

   | verdict | Havoc | Ret | derivable from |
   | --- | ---: | ---: | --- |
   | `below` | 48% | 42% | where the press is |
   | `cd` | 31% | 31% | the declared cooldown state |
   | `press` | 8% | 11% | elimination over the rest |
   | `starved` / `overcap` | 4% | 9% | cost vs declared resource |
   | `hold-readable` / `hold-sealed` | 5% | 7% | **cap's markers — not derivable** |

   ~75% of every line is `below` or `cd`, which a machine derives knowing nothing about cap.
   But `hold-*` comes from marker conditions that live as **English prose in the roster**, not
   as data, so until stage 5 encodes them the line has to stay whatever we decide. Fill in the
   clerical 75% from the emulator and let the authored line shrink to the entries carrying a
   claim; that is most of the win and defers the decision to when it is real.

   ⚠ **Do not justify keeping them with "it would have caught RET-1."** It would not. RET-1's
   error was the APL gating Avenging Wrath on a target DoT, and the emulator models nothing
   about the APL. What a cross-check catches is narrower: a picture contradicting its own
   declared state — a spender drawn `starved` at 5 Holy Power, a row drawn `cd` while the state
   says it is up, Havoc's absent tints. Reasoning errors about the priority list are caught by a
   human reading the priority list, which is what the walk prose is for.
2. **Does the emulator resolve display identity?**
   *Recommend: no*, per §6. Revisit if aura state is being modelled anyway by stage 4.
3. **Where does `starved` meet the client's power branch?** cap's `starved` marker and Blizzard's
   power tint read the *same* underlying fact, so once cost is computed they must agree — a
   scenario asserting one without the other is a contradiction. *Recommend*: report it, do not
   fail the build.

## 9. Risks

- **The cost model is wrong for a build nobody tested.** Mitigated by §4's unknown state and by
  the in-game flight remaining the arbiter, never this.
- **The emulator becomes a second source of truth about the client**, drifting from
  `knowledge/addon-dev/`. Mitigated by every rule in §3 citing the KB section it transcribes; a
  rule with no citation is a bug.
- **Scope.** Stages 3–4 are the largest thing built in `capart`. Stages 1–2 are small and
  independently valuable, which is why they are first.

# Combat Assist Plus — tier-preserving simplification plan

**Purpose:** correct the first simplification pass without rebuilding the ontology it removed.
⚠ **ARCHIVED 2026-09-01, and superseded by `spec.md` before it was.** Its corrected target is the
three discrete tiers `ASAP` / `SOON` / `FALLBACK`, and `spec.md` §3.1 retired those on 2026-08-25:
the shipped renderer had already collapsed every tier onto the one scan treatment, so the model was
changed to say what the product does. Read this for the arguments, never in the present tense.

The *first*, failed plan is archived beside it at `simplification-plan-2026-08-11.md`.

## What the first pass got wrong

Its decision packet offered a false choice between one continuously graded emphasis and the
entire old HIGH / MEDIUM / LOW system. The missing choice was the intended product: a small
set of discrete, reusable priority categories without continuous grades, mandatory cue
machinery, exhaustive catalog coverage, automatic sequences or visual-policy invariants.

The rewritten §3.1 then contradicted §1. Principle (c) rejects an engine that always selects
one winner; it does not reject relative guidance. Multiple abilities may occupy any priority
category at once.

## Corrected target

1. **Discrete emphasis tiers.** `ASAP`, `SOON` and `FALLBACK` are ordered player guidance.
   They are categories, not quotas, and do not rank abilities within the same category.
2. **Readable conditions choose tiers.** A catalog entry declares ordered bands using only
   facts Lua may read. Unknown input never promotes an ability.
3. **No continuous grade.** A tier selects one whole treatment. The player never compares
   small alpha differences within a tier.
4. **Context markers stay independent.** Readable markers add facts without changing tier.
   Optional sealed markers may be added only with a renderer that sends their value directly
   to a client-owned sink.
5. **Cooldown bars stay independent.** The Tyrant bar remains the one pilot experiment; bars
   do not inherit icon tier or markers automatically.
6. **The pilot stays small.** Restoring the tier abstraction does not restore the old
   ten-entry Demonology catalog. Abilities return only after a player problem and tier rules
   have been authored deliberately.

## Implementation contract

- Catalog entries carry ordered `bands = { { tier = ..., when = ... }, ... }`.
- First true band wins. Alternative bands may share a tier. False tries the next band; an
  unknown in a potentially matching tier may try another band in that tier but never fall
  through to a weaker answer.
- The catalog validator admits only the three tier names and the readable predicate vocabulary
  used by the pilot.
- The signal result carries `tier`, never a continuous strength.
- Treatment maps each tier to a discrete static appearance. Exact pixels remain provisional
  until flown.
- Several entries may return the same tier, different tiers, or no tier in one evaluation.

## Execution

- [x] Archive the failed plan and identify the false A1/A2 choice.
- [x] Reconcile `spec.md`, the Demonology catalog, backlog, discussion and notes.
- [x] Restore the small tier contract in Lua and its mechanical tests.
- [x] Run parser, unit and repository consistency checks.
- [ ] Release and fly only after separate approval.

## Deliberately not restored

- continuous within-tier grading;
- animated pulse rates and phase arithmetic;
- no-tier veils or dimming unrelated CDM rows;
- mandatory sealed halves for readable markers;
- tier-colored marker reuse;
- tier-colored cooldown bars;
- exhaustive entry-or-silence coverage;
- automatic current/next sequences;
- gameplay-opinion tests presented as engine guarantees.

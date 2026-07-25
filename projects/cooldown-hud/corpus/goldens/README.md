# Phase-2 goldens — the independent `State → Guidance` corpus

Each `<scenario>/` holds a frozen test case:
- **`state.json`** — a **synthetic** State pulse (per `docs/architecture.md` Stage 1),
  **templated on the real `corpus/statelog/` captures** (real cooldownIDs, real field shapes).
  Synthetic-not-captured by design (see `docs/w4-phase2-goldens-plan.md`), gated by the
  **State-contract validator** so it stays physically realizable.
- **`guidance.json`** — the **expected Coach output** (per `guidance-contract.json`), reasoned
  from the Demonology rotation source, **never** from code. This is the oracle.
- **`rationale.md`** — why that Guidance follows from the readable State + the rotation source,
  with the readability caveats.

## Conventions

- **`cues` lists only the cues that DRAW.** An unlisted cooldownID = `draw:false` (`AVAILABLE`
  internal). This keeps the single-top-press check legible: at most one listed cue is
  `ROTATION`/`LATE`.
- **Decision-relevant subset.** A live pulse anchors all ~64 CDM entries; a fixture carries only
  the abilities that determine the ranking (the ~6 rotational buttons + the relevant buffs). The
  validator checks the subset is *sufficient* to justify the winner.
- **Readability filter (combat).** Cooldown reads go **secret** (`readable:false`) → the napkin
  fills (`source:"napkin"`); shards/power stay readable; procs read via `buff.isActive` + `glow`
  (never `aura`, which is `readable:false` in combat). Expected Guidance is what the **readable**
  state justifies — secret-gated refinements (e.g. Demonic Core *stack count*) soften.

## The two implementation decisions (locked here on real examples)

1. **Harness fixture-path.** Goldens live **here** in the wow repo (source of truth, versioned
   with the contract). The busted harness runs in the *separate* CDMProbe repo → it loads these
   JSON files via **`dkjson`** through a **configurable path** (default: the sibling
   `…/projects/cooldown-hud/corpus/goldens`). Chosen over generating Lua-table fixtures so the
   goldens stay one artifact, diffable next to the contract. *(Harness itself is a follow-up;
   these files are its input.)*
2. **Validator home.** A **`wowkb.cdmp goldens check`** subcommand (Python, reuses the cdmp
   reader/JSON scaffolding, runs in the wow repo): validates each `state.json` against the
   State-contract invariants and each `guidance.json` against `guidance-contract.json` (token
   vocab, no RGBA, single-top-press, the secrecy gate). *(Follow-up; the format below is what it
   asserts.)*

## Status

Three **proof-of-shape** scenarios, hand-authored 2026-07-25: `hand-of-guldan` (clean single
`ROTATION`), `demonbolt-proc` (proc-driven via readable buff/glow; HoG shard-excluded),
`implosion` (`JUDGE` coexisting with the single `ROTATION`). The rest fan out via the workflow in
`docs/w4-phase2-goldens-plan.md`.

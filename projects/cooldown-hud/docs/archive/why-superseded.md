# Why the Cooldown HUD was superseded — 2026-08-05

⚠ **History. This is the record of one decision about one retired product. It is not a
criterion to evaluate current work against, and it is deliberately kept out of every
`CLAUDE.md` so it does not read as one.** The live mechanism for the question it raises is
the `cap-conscience` reviewer (`.claude/agents/cap-conscience.md`), which runs **after a
release is cut**, asks it once, from outside a single change, and returns questions to the
author. That cadence is the whole point: the drift it looks for is invisible from inside any
one edit, so asking it continuously turns every design discussion into a re-litigation and
produces nothing but hesitation.

## The reasoning at the time

CDMProbe started as "what can I do with the CDM" and grew into a **next-action decision
engine** — one answer per GCD. That runs against Blizzard's stated position on combat
addons, and the 12.0 Secret-Values restrictions had already begun capping what it could
calculate.

Combat Assist Plus is the same premise re-aimed at what the platform invites: re-present,
grade, contextualise — narrow the decision instead of making it. The positive statement of
what cap *is* lives in `projects/combat-assist/specs/spec.md` §1, and that is the document
to read when changing cap's behaviour. This file is not.

## Consequences that were acted on

- No new CDMProbe work; the multi-class rollout stopped at Phases 3-5.
- The owed Havoc flight became moot — it gated rollout phases that were not built.
- No code ported. The `State -> Coach -> Binder -> Renderer` pipeline was shaped around
  authoring a priority answer, so inheriting it would have smuggled the premise back in.
- What stayed authoritative: the measured client facts (now in `knowledge/addon-dev/`,
  which is the authority) and the per-spec rotation research under `specs/`.

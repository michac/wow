# Combat Assist Plus — project root

`/cap` is a Retail / Midnight combat-assistance addon that extends Blizzard's Cooldown
Manager. It is a standalone companion app, not part of the gameplay KB.

Read `specs/spec.md` before changing behavior. Section 1 is the constitution; later details
are valid only while they remain downstream of it.

The addon source is `addon/`, a separate gitignored repository with its own `CLAUDE.md`.

## Project documents

Five permanent files have five jobs:

| File | Owns |
| --- | --- |
| `specs/spec.md` | Approved player-visible behavior and product boundaries. |
| `specs/backlog.md` | The only implementation-status block and the ordered work list. |
| `specs/notes.md` | Short dated records of completed rounds. |
| `specs/discussion.md` | Only unresolved product questions requiring an author decision. |
| `specs/flight-reading.md` | How to interpret the capture format the current source emits. |

`specs/simplification-plan.md` and `specs/simplification-audit.md` are temporary migration
artifacts. They are not additional product authorities.

The live addon version comes from `wowkb.addon list`. What is built or flown comes only from
`specs/backlog.md` → `## Status`.

If behavior is not in `spec.md`, put it in `backlog.md` → `Ideas` or ask before building it.
A question leaves `discussion.md` when decided. Record completed work briefly in `notes.md`.

## Working on addon code

Read the workspace `wow-developer` skill and its `references/house-rules.md` before editing
Lua, XML or the `.toc`.

Client facts belong in `knowledge/addon-dev/`, not in product docs or source comments. A
marked unknown that would be load-bearing is a stop-and-ask under that skill.

Before touching the gitignored addon checkout, run `wowkb.addon pull --all`. Captures leave
the addon only through `wowkb.capture cap <stream>`; SavedVariables flush on `/reload` or
logout. `specs/flight-reading.md` describes what each current stream can and cannot prove.

Tests protect mechanical and platform guarantees. They do not turn product prose, gameplay
opinions or visual taste into invariants.

## Authoring another spec

1. Start from the current authoritative APL and name the player problem each proposed hint
   solves. Enumerate only the facts those rules require.
2. Classify every fact as **readable**, **sealed-display-only**, or **unavailable** on the live
   patch. A marked addon-dev unknown is a stop-and-ask, not permission to guess.
3. Author readable facts into broad independent tiers and readable markers. Author sealed
   facts only as independent context sent to an existing client-owned display sink; unavailable
   facts produce no hint.
4. Link every mechanism to its canonical source example and the evidence in
   `knowledge/addon-dev/`: Demonbolt for proc plus resource, Tyrant for readiness and readable
   markers, Conflagrate for charged readiness, and Backdraft for sealed player-aura stacks.
5. Add a narrow shared mechanism only when the authored vertical slice needs one. Do not
   prebuild aura/totem duration, target-aura, APL-DSL, capability-registry, or unused marker
   vocabulary.

Gameplay choices remain in `Catalogs/<Spec>.lua` and the matching `specs/<spec>/catalog.md`;
unknown-safe evaluation remains in `Signal`, and pixels remain in shared treatment/overlay
code. Fly the player judgment before reading captures.

## Releasing

Releasing is always ask-first. A push alone does not reach the game; deployment installs the
latest GitHub release.

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.addon release cap [--patch|--minor|--major]
```

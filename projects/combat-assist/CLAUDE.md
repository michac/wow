# Combat Assist Plus — project root

A standalone companion app (NOT the KB): `/cap`, a combat-assistance addon for
Retail / Midnight 12.0. **Scaffold stage** — the addon loads, registers its slash
router and does nothing else. What it is *for* has not been decided; that decision
belongs in `specs/spec.md` and is the first item in `specs/backlog.md`.

The addon source is `addon/` — its own git repo (`michac/cap`), **gitignored** by
the wow workspace, with its own `CLAUDE.md` covering the release workflow. This
folder is the tracked side: docs live here, code lives there.

## The spec process — three files, three jobs

Everything about this project's direction lives in **`specs/`**. Three files, and
the split is what keeps each of them readable:

| File | Holds | The test for "does it go here?" |
| --- | --- | --- |
| **`specs/spec.md`** | **What the addon is supposed to do.** The product definition — behaviours, boundaries, constraints. Present tense, no history. | Would a stranger reading only this know what to build? |
| **`specs/backlog.md`** | **The list of work items.** Agreed work not yet done, one line each, in `Now` / `Next` / `Ideas` / `Done`. | Is it a thing someone could pick up and finish? |
| **`specs/notes.md`** | **What we actually did.** Session logs, decisions and their rationale, dead ends, in-game observations. Newest first, dated. | Is it about the past — ours, not the game's? |

**How they interact.** A session reads `spec.md` for intent and `backlog.md` for
the next item, does the work, then records the outcome in `notes.md` and strikes
or moves the backlog line. If the work changed *what the addon should do*, edit
`spec.md` in place — don't leave the old text standing with a correction under it,
and don't let `notes.md` become the real spec by accident.

Three rules worth stating because they're the ones that erode:

- **`spec.md` is present-tense and history-free.** History is `notes.md`. A dated
  aside in the spec is a defect — same rule as the KB's topic files.
- **If it isn't in `spec.md`, don't build it.** A behaviour nobody wrote down is
  the thing that gets built twice, differently. Un-specced work goes to
  `backlog.md` → `Ideas` first, or ask.
- **A fact about the client does not stay in `specs/`.** How the API behaves, what
  is readable under Secret Values, what an event's payload is — that is
  `knowledge/addon-dev/`, written back in the same session (see the
  **wow-developer** skill). `notes.md` records *our* work; the KB records the
  game's behaviour. Getting this backwards is how the KB goes stale while every
  project quietly re-learns the same thing.

## Working on the code

Read the **wow-developer** skill first; its house rules are enforced by
`/addon-review`. The two that bind hardest on a young addon are already live in
`Core.lua`: commands come from the `ns.Commands` schema table (never a hand-rolled
parser, no substring dispatch), and any future data extraction rides the one
capture path (`ns.Capture.Open` → `wowkb.capture cap <stream>`).

## Releasing

Ask first — this project has **no** standing auto-deploy exception (the Cooldown
HUD's is scoped to CDMProbe alone). The recipe:

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.addon release cap [--patch|--minor|--major]
```

⚠ **A push does not reach the game.** `ghaddons` installs from the latest GitHub
*release*. Nothing is deployed until a release is cut — as of now none has been,
so the addon is not in the game folder. Current version: `wowkb.addon list`.

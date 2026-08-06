# Combat Assist Plus — project root

A standalone companion app (NOT the KB): `/cap`, a combat-assistance addon for
Retail / Midnight 12.0. It makes Blizzard's Cooldown Manager tell you more without
telling you what to press — re-presenting, *grading* and contextualising what you
already have, rather than deciding for you. The core is a **tier signal**: HIGH /
MEDIUM / LOW emphasis across the tracked set, several things lit at once, you pick.
Around it: procs as a tier input, auto-detected sequence hints layered on top, and a
movable cooldown-bar panel reusing the same signal. **`specs/spec.md` is the
definition** — read it before touching anything, especially §3.1's three rules,
which are what keep the tier signal from quietly becoming a rotation engine.

**cap supersedes Cooldown HUD** (`projects/cooldown-hud/`, CDMProbe), which grew
into the decision engine this project is deliberately not. No code is ported;
CDMProbe's client facts live in `knowledge/addon-dev/` and stay authoritative.

**Code status: M2 code-complete, not flown.** `Core.lua` (router + the
`ns.RegisterCommand` / `ns.RegisterStatus` registries), `Bind.lua` (the CDM binding)
and `Frame.lua` (the movable panel). ⚠ **The deployed release is still the scaffold** —
Bind and Frame have never executed in the client. `specs/backlog.md` → `Now` holds the
acceptance list they need.

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
*release*, so nothing is deployed until a release is cut. cap **is** released and
installed — but the deployed build is the **scaffold** (`.toc` + `Core.lua`); any
module added since is working-tree-only until the next cut. Always read the live
version off `wowkb.addon list` rather than this file.

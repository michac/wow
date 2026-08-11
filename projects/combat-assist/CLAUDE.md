# Combat Assist Plus — project root

A standalone companion app (NOT the KB): `/cap`, a combat-assistance addon for
Retail / Midnight 12.0. It makes Blizzard's Cooldown Manager tell you more without
telling you what to press — re-presenting, *grading* and contextualising what you
already have, rather than deciding for you. The core is a **tier signal**: HIGH /
MEDIUM / LOW emphasis across the tracked set, several things lit at once, you pick.
Around it: procs as a tier input, auto-detected sequence hints layered on top, and a
movable cooldown-bar panel reusing the same signal. **`specs/spec.md` is the
definition** — read it before touching anything, especially §1's three principles,
which everything else in the spec is downstream of.

**cap supersedes Cooldown HUD** (`projects/cooldown-hud/`, CDMProbe), which grew
into the decision engine this project is deliberately not. No code is ported;
CDMProbe's client facts live in `knowledge/addon-dev/` and stay authoritative.

**Code status: M2 flown; M3a done; M3b released and flown 2026-08-07.** `Core.lua`
(router + the `ns.RegisterCommand` registry), `Bind.lua` (the CDM binding), `Frame.lua`
(the movable panel), `Capture.lua` (vendored — the one data-out path) and `Log.lua`. The
binding is confirmed **correct**, not merely present — 200 identity rows across 3 specs
and 2 classes, including a Paladin.

M3's tier signal is four pure modules and two impure ones: `Catalog.lua` (the closed
vocabulary and §3.5's five checks), `Catalogs/Demonology.lua`, `Tier.lua` (first-match
bands, three-valued gates), `Track.lua` (the readiness latch and the aura/elapsed edges),
`Treatment.lua` (tier → look — **the only place the visual numbers exist**), `Sense.lua`
(hooks, clock, client reads), `Channel.lua` (the two sealed comparisons — cap offers, the
client decides, cap is never told) and `Overlay.lua` (cap's own frames, anchored to the CDM
icons). Plus `Mode.lua` — `/cap aoe`, cap's own answer to a target count the client will
not give us — and `Bars.lua`, §3.4's cooldown bars riding the same verdicts onto the movable
panel (`Bars.Plan` is its pure seam). **M3c, M3d and the bars are built and have never run in
the client** — the M3b flight measured the tiers computing correctly with no pixels involved,
and nothing since has been flown. ⚠ **Neither cue channel has a readback**, so `cap draw`'s `C{}` says whether cap
*armed* a cue and never whether a marker appeared; an eyeball is the only oracle for that.
Both readings and acceptance tables: `specs/backlog.md` → `## Reference`.

⚠ **The order is `simplify → draw → add detail from play`.** The **window migration
landed 2026-08-08**: the code and `specs/demonology/catalog.md` now speak the vocabulary
`spec.md` §3.1/§3.5 describes — no windows, subjects legal in bands, negation legal, cues
carrying polarity and a channel — so **the drawing rungs are next** and what they draw is
the model we are keeping. ⚠ "Simplify" was the code catching up, **not** another design
round: `spec.md` §3 is not re-opened. Reasoning: `specs/notes.md` 2026-08-08 (migration);
the queue: `specs/backlog.md` → `Now`.

**Four capture streams, and they are the only way anything here reports what it saw:**
`wowkb.capture cap bind` (the binding), `cap tier` (the tier verdicts + gate health),
`cap edge` (every alert edge that landed) and `cap draw` (what the overlay painted, and
whether it found a frame to anchor to — the instrument that separates a treatment bug
from an anchoring one). ⚠ SavedVariables only flush on `/reload`.

⚠ **The capture on disk is a client-authored fixture, and it is the cheapest instrument
in the project.** Reading the 21 live Demonology rows settled five catalog open questions
and found three defects — including that Shadow Bolt *does* have a CDM row — before any
M3 code existed. Read it before asserting what the CDM tracks.

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
| **`specs/discussion.md`** | **Questions raised and not yet decided**, with the case on both sides. Nothing here is a commitment and nothing here ages. | Would deciding it change the design, and is it genuinely still open? |

⚠ **`discussion.md` is the newest of the four and the easiest to skip.** It exists because
the other three have no home for an open question — so questions were getting decided in
passing, or lost. An item leaves it when decided: the decision to `spec.md` or
`backlog.md`, the reasoning to `notes.md`, struck here with a pointer to where it went.

**Two published reference artifacts** — derived from the code and the captures rather than
written from memory, so they are a view and these files are the truth. ⚠ **Both are STALE
as of 2026-08-07**: they describe **windows**, the six-window cap and stack-count-only
cues, none of which exist any more. Do not read a vocabulary claim out of either one until
`backlog.md` → **The stale artifacts** re-derives them.

- [Architecture — how cap is wired, and where the signal stops](https://claude.ai/code/artifact/2de40ee9-5457-4ca3-b46e-77178e021207)
- [Demonology reference — every tracked row, what lights it, what is drawn on it](https://claude.ai/code/artifact/46bb78b6-7c41-4210-a9b0-3b1707678569)

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
parser, no substring dispatch), and data extraction rides the one capture path
(`ns.Capture.Open` → `wowkb.capture cap <stream>`) — `Log.lua`'s `bind` stream is the
first user of it, and there is no second way out.

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

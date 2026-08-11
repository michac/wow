# Combat Assist Plus — project root

`/cap` — a combat-assistance addon for Retail / Midnight 12.0 that rides Blizzard's
Cooldown Manager. A standalone companion app, **not** the KB.

**`specs/spec.md` is the definition.** Read it before touching anything, especially §1's
three principles — everything else in the spec is downstream of them. What the addon is,
what it deliberately does not do, and why it supersedes the Cooldown HUD are all answered
there and are **not** restated in this file.

The addon source is `addon/` — its own git repo (`michac/cap`), **gitignored** here, with
its own `CLAUDE.md`. Docs live here, code lives there.

## The docs — five files, five jobs

Everything about this project's direction lives in **`specs/`**. The split is what keeps
each file readable, and the right-hand column is the whole of the routing rule:

| File | Holds | The test for "does it go here?" |
| --- | --- | --- |
| **`specs/spec.md`** | **What the addon is supposed to do.** The product definition — behaviours, boundaries, constraints. | Would a stranger reading only this know what to build? *Present tense, no history — a dated aside here is a defect.* |
| **`specs/backlog.md`** | **The work items, plus the one `## Status` block.** Open work in `Now` / `Next` / `Ideas`; one line per finished item in `Done`. | Is it a thing someone could pick up and finish? |
| **`specs/notes.md`** | **What we actually did.** One short dated entry per round, newest first, past tense. | Is it about the past — ours, not the game's? *Never a rule in normative form; notes cites the spec, it does not restate it.* |
| **`specs/discussion.md`** | **Questions raised and not yet decided**, the case on both sides, and what would decide it. Nothing here is a commitment and nothing here ages. | Would deciding it change the design, and is it genuinely still open? |
| **`specs/flight-reading.md`** | **How to read a capture.** Every field cap emits and every acceptance criterion. | Would a pilot diagnosing a flight need this open beside them? |

⚠ **Status is asserted in exactly one place: `backlog.md` → `## Status`.** Nothing else —
this file included — says what is built or what has flown. The rule exists because three
files once carried contradictory present-tense claims about whether the addon had ever
drawn a pixel, and the two that load every session were the stale ones. The live addon
version comes from `wowkb.addon list`, never out of a document. **One sanctioned
exception:** `spec.md`'s Milestones table mirrors the Status block and must stay consistent
with it — it is the ladder, not a second status claim.

⚠ **Two published reference artifacts (Architecture, Demonology reference) are STALE** —
they describe a catalog mechanic and a cue vocabulary that no longer exist. `backlog.md`
tracks re-deriving them; do not read a vocabulary claim out of either.

**How a session moves through them.** Read `spec.md` for intent and `backlog.md` for the
next item; do the work; record the outcome in `notes.md` and strike the backlog line. If the
work changed *what the addon should do*, edit `spec.md` in place. An open question that
would change the design goes to `discussion.md` rather than being decided in passing.

**If it isn't in `spec.md`, don't build it.** A behaviour nobody wrote down gets built
twice, differently. Un-specced work goes to `backlog.md` → `Ideas` first, or ask.

## Working on the code

Read the **wow-developer** skill first. The house rules live in that skill
(`references/house-rules.md`) and are enforced by `/addon-review` — they are not restated
per project, so that there is one copy to drift from.

⚠ **A fact about the client does not stay in `specs/`** — it belongs in
`knowledge/addon-dev/`, written back in the same session. That routing is this project's
half; the rule itself is the skill's (*Improve the KB as you go*).

Captures are the only way anything here reports what it saw — `wowkb.capture cap <stream>`,
streams `bind` / `tier` / `edge` / `draw`. How to read any of them, and the `/reload` flush
rule that governs them: **`specs/flight-reading.md`**.

## Releasing

**Ask first.** There is no *standing* auto-deploy exception (the Cooldown HUD's is scoped to
CDMProbe alone). A `--patch` cut was pre-authorised for **M3 flights and nothing else**, and
that no longer reaches anything: the build has carried M4a since v0.2.4, so a cut today
carries work from another milestone and is ask-first. `backlog.md` → *The drawing rungs*
owns this and wins if the two ever drift.

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.addon release cap [--patch|--minor|--major]
```

⚠ **A push does not reach the game.** `ghaddons` installs from the latest GitHub *release*,
so nothing is deployed until a release is cut, and any module added since the last cut is
working-tree-only.

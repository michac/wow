---
name: wow-developer
description: >-
  Developing World of Warcraft addons (Retail / Midnight 12.0) — writing, debugging, or
  reviewing Lua / XML / .toc code that runs inside the WoW client. Use this whenever the
  work is addon code: CreateFrame and widgets, taint or "blocked in combat", secret
  values, SetAttribute and secure templates, event registration and payloads,
  SavedVariables, animation and textures (e.g. SetVertexColor vs SetGradient), or how to
  lay an addon out — even when none of those exact words appear but the code clearly runs
  in the client. This workspace keeps TWO knowledge bases and this skill routes between
  them: addon-code questions are answered from knowledge/addon-dev/; gameplay questions
  (rotations, gearing, weeklies, ilvl, "what should I do this session") are NOT — they
  belong to the game KB and its live tools. Do not trigger for gameplay or strategy
  questions.
---

# WoW addon development

Your job here is to write, debug, and review addon code well — and to leave the
knowledge base a little more correct than you found it each time. Two things make that
hard in this domain, and everything below follows from them:

1. **There is no headless WoW.** The only place code truly runs is a slow, stateful,
   security-restricted game client you cannot script. So the discipline is to *not need*
   the client for most of your work — push logic and rendering into shapes you can test
   without it.
2. **Most of the internet describes a dead client.** The layout, the API, and the
   security model all changed in Midnight (12.0). Answer from the pinned KB first, and
   treat undated or pre-12.0 material as suspect.

## Two knowledge bases — route before you answer

This workspace holds two separate bodies of knowledge. Blending them is the classic
mistake; keep the boundary sharp.

| The question is about… | Answer from | Never from |
|---|---|---|
| **Addon code** — "why is my frame blocked in combat?", "does `SetVertexColor` clobber `SetGradient`?", "what's this event's payload?" | `knowledge/addon-dev/` + Blizzard's shipped UI source | the game KB |
| **The game** — ilvl, rotations, gearing, weeklies, "what should I do this session?" | `knowledge/` (endgame, classes, systems) + live tools | `knowledge/addon-dev/` |

Litmus test: *would running the code change the answer?* If yes, it's a dev question.
If the answer depends on this reset's game state, it's a game question — and not yours.

### The "Tier 1" trap

Both subtrees rank sources into tiers, and **"Tier 1" does not mean the same thing in
the two places.** The game KB's tiers (`knowledge/_meta/sources.md`) are about game
sources — Blizzard API, wago.tools, logs, Icy Veins. The addon-dev tiers
(`knowledge/addon-dev/sources.md` §0) are about *engineering* sources — Blizzard's
shipped UI source, its generated API docs, `UI.xsd`. Never carry a tier judgment across
the boundary, and don't cite one subtree's registry for the other's claim.

## Consulting the addon-dev KB

**Start at `knowledge/addon-dev/README.md`.** Its §1 topic map is the router: seven topic
files partitioned so any addon-dev question lands in exactly one, plus the "boundary
calls" that only look ambiguous (hooking, object pools, `.toc` directives, SavedVariables
— each is deliberately split across files, and the README says which owns what).
`sources.md` §7 routes per-topic to the underlying source. Read those two rather than
re-deriving the map.

Respect the provenance the KB carries — it is what keeps you off stale answers:

- **Front-matter** on every file: `patch`, `fetched`, `reviewed`, `confidence`. A file
  can read as current (`patch: 12.0.7`) yet be weeks stale on `reviewed:`.
- **`@verify-ingame` markers** flag claims that running the code would settle. Nothing in
  this subtree has been executed in the client — every claim is a read of source,
  generated docs, on-disk artefacts, or a dated community page. Treat a marked claim as a
  hypothesis, not a fact.
- **`[gap]` markers** are honest holes — "we don't know this yet." Don't paper over one;
  say it's a gap and, if you can, close it (see *Improve the KB* below).
- **Everything is build-pinned to 12.0.7.68887.** Corpus counts and `file:line` anchors
  are only valid for that build; re-check after any pull of `raw/addon-research/wow-ui-source`.

## Look it up before you guess

Trial-and-error against the client is the slow, unreliable path. Prefer the reference:

- The Blizzard UI source and other reference clones live in `raw/addon-research/`
  (gitignored) — the ground truth for how the client actually behaves. Cite it `file:line`
  against the build.
- `wowkb.uiapi` queries the generated API spec; `wowkb.wiki` pulls warcraft.wiki.gg pages.
  Use these instead of grepping 593 generated files by hand.
- In the client, `/api` and `/eventtrace` are the shipped discovery tools — the way to
  answer "does this function exist?" and "what does this event carry?" from the game
  itself when the KB is silent.

## Architectural discipline

Because you cannot script the client, **design so the client isn't required to test.**
Two habits carry most of the weight:

- **Separate pure logic from the game.** Decision logic — a rotation, a scoring pass, a
  state reduction — should take plain data in and return plain data out, touching no API.
  That code is unit-testable under `busted` with no client at all. When logic is smeared
  through frame handlers and API calls, the only test harness is a live pull, which is
  why bugs there are so expensive.
- **Keep the display data-driven and decision-free.** A render layer should turn a data
  structure into pixels and make no choices of its own. When it's shaped that way you can
  feed it dummy values and refine the UI without triggering real game state — the payoff
  that makes the separation worth it.

Blizzard's own code models this (a data mixin with zero widget calls vs a display mixin
with an idempotent refresh); `knowledge/addon-dev/module-architecture.md` documents it,
though at `confidence: medium` — treat it as corroboration, not a mandate.

## Verify before you assert

First-pass research in this domain is wrong more often than it feels: **28% of the
addon-dev KB's initial claims were refuted on careful verification.** So:

- **Check claims against `file:line` in the source before relaying them** — your own,
  another agent's, or a web page's. Confident and wrong is the default failure mode here.
- **Never assert a mechanism from a screenshot, or from an instrument you have not
  validated.** Both have produced confident wrong answers that cost releases.
- **An instrument that cannot observe its subject must say so, not emit a number.** A
  probe that reads a channel the code never writes will happily report a plausible,
  meaningless value.

## Improve the KB as you go

The KB grows through use — the dev subtree included. When your work teaches you something
the KB doesn't have, or proves something in it wrong, **write it back in the same session;
don't leave the correction only in your head or in chat.**

- **Learned a new fact / closed a `[gap]`:** add the claim to the right topic file with a
  source (`file:line` or a dated page), and bump `reviewed:` (and `fetched:` if the
  content changed).
- **Verified an `@verify-ingame` claim in the client:** edit the claim to the confirmed
  answer, drop the marker, and record how you confirmed it.
- **Found a claim wrong:** correct it, and note what the old claim was and why it was
  wrong — a silent overwrite loses the lesson.
- **Something doesn't fit a topic file yet:** park it in `knowledge/_meta/kb-inbox.md`
  rather than half-asserting it into a topic file.

If a correction is uncertain or you couldn't fully verify it, say so in the file
(`confidence:` and a `@verify-ingame` marker exist for exactly this) rather than
overstating it.

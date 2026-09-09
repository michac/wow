# Smart Glo — project root

Rule-driven glows on **Cooldown Manager icons**. The slash prefix is `/sg`; the addon short
name in `wowkb.addon` is `sg`.

## Project documents

- **`README.md`** — the design, the survey that motivated it, and the product-level scope.
- **`rule-language.md`** — **the rule language**: the gate/binding split, what may be combined
  with what, the evaluation semantics, the compilation model, the syntax sketch and the
  checker's refusal list. ⚠ It is a **design, not an implementation** — none of it has been
  built or flown, and it says so at the top. `README.md` defers to it on anything about what a
  rule can say.
- **`backlog.md`** — `## Status` (what is BUILT), `## Now` (the ordered work list), `## Parked`.
  ⚠ Status lives **only** there. Do not restate it here, in `README.md`, or in the root
  `CLAUDE.md`.
- **`addon/CLAUDE.md`** — the release workflow for `michac/SmartGlo`. The checkout at `addon/`
  is its own git repo and is **gitignored** by the wow repo, so a `git pull` here does not
  fetch it; `wowkb.addon pull sg` does.

The live version comes from `wowkb.addon list`, never from prose.

## What crosses into this project, and what does not

Smart Glo is the third addon in this repo to ride the Cooldown Manager — Combat Assist Plus
(`/cap`) is live, Cooldown HUD (CDMProbe) is archived. Being the same shape does **not** make
them precedent.

**Facts cross. Decisions do not.**

- ✅ **Measured client facts** — how the CDM lays out its viewers, what a rebind hook fires,
  which API returns what. These are read from **`knowledge/addon-dev/`**, where the KB's
  evidence gates apply and each claim carries provenance. `cdm-rider-patterns.md` is the
  relevant topic file, and citing it from here is correct and expected.
- ❌ **Design stances, principles, taglines, scope prohibitions and product boundaries** from
  `projects/combat-assist/` or `projects/cooldown-hud/`. Those were decided against a
  different product's goals. A rule that reads like doctrine ("we don't do X") is **cap's or
  cdmp's, not ours**, unless this project's own docs say so.
- ❌ **Their code.** Nothing is ported. Where behaviour is shared, the shared thing is the
  documented client fact, not an implementation.

If a sibling project's document seems to settle a question here, it does not. Re-decide it
against Smart Glo's own goals, or ask.

## Scope is deliberately open

`README.md`'s **"decorate, never replace"** is a statement about *drawing surface* — no viewer
is hidden, no icon row of our own is drawn, nothing is conjured onto the screen that the CDM
does not lay out. It is **not** a limit on how opinionated a rule may be. How far toward
rotation advice this addon goes is an open question, to be answered against a concrete
request rather than pre-decided. Do not weigh a feature against an unwritten prohibition.

The v1 rule vocabulary is one class wide (resource thresholds) so that the **attach path** is
what gets proven first. That is a sequencing decision, not a ceiling — the parked rule classes
in `backlog.md` are parked for sequencing, and each is fair game once the attach path holds.

## Working on addon code

Lua that runs in the client is governed by the **`wow-developer`** skill and
`knowledge/addon-dev/`. A claim there carrying an open marker (`[gap]`, `@verify-ingame`,
`@pending-test:`) that you are about to build on is a **STOP: ask**.

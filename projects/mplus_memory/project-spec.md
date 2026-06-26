# Project Spec — M+ Memory Trainer

*A spaced-repetition trainer for memorizing Midnight Season 1 Mythic+ dungeon
mechanics. Derived from the design conversation in
[`original_convo_archive.md`](./original_convo_archive.md).*

---

## 1. Problem & goal

Player joined Midnight late in Season 1 and is at a knowledge disadvantage:
teammates have months of reps. Reflexes (procedural memory) can't be
fast-tracked, but **knowing what to expect** (declarative memory) can be. A
strong declarative scaffold also speeds reflex acquisition, because attention
is spent executing rather than figuring out *what* is happening.

**Goal:** learn, to recall speed, what happens in each of the 8 S1 dungeons and
what the player should do about it — boss mechanics, key trash, routes.

Non-goal: replacing in-game practice. This is the pre-load, not the substitute.

## 2. Guiding principle — trainer, not reference

Data dumps don't stick because reading is **recognition** ("I've seen this"),
while play demands **recall** ("what do I do, right now, before this cast
finishes"). A prettier page you still just *read* fails the same way.

The basic unit is a **rep**: show a cue → player produces a response → app
grades it. The deliverable is a *trainer*, not a prettier wiki.

### Learning approaches feeding the design

1. **Alphabet before words** — a small recurring vocabulary of ~15–20 mechanic
   *archetypes* (interruptible cast, frontal cone, ground AoE, stack-vs-spread,
   soak, dispel, kill-priority add…). Learn these to automaticity; then every
   ability is just "that's a frontal." Collapses 8 dungeons × dozens of
   abilities into a tiny set + a mapping.
2. **Encode by consequence, not flat** — tier everything: group-wipe → your
   death → your job → flavor.
3. **Spaced repetition (SM-2 / Anki-style)** — active recall + spacing; cards
   shaped like the in-game cue (front = "Boss X casts [name]", back = response).
4. **Dungeon as memory palace** — a route is already a spatial sequence; peg
   mechanics to real rooms.
5. **Mental rehearsal** — walk the route in your head, narrating responses.
6. **Generation effect** — writing route notes in your own words ~doubles
   retention vs passive reading.
7. **External aids as training wheels** — BigWigs/DBM + WeakAuras offload now,
   internalize gradually.

## 3. Scope decisions (locked)

- **Role:** player is **DPS**. Build role tagging in from day one so "support
  healers/tanks eventually" is a *filter flip*, not a rebuild.
- **Breadth:** all **8 dungeons**, lighter detail each (modest card budget per
  dungeon) rather than deep on a few.
- **Build order:** engine first — trainer mechanics + archetype layer + **one
  fully-fleshed dungeon** — before mass-entering all eight.

## 4. Architecture

Single self-contained file, **React**, four layers:

- **Content layer** (plain data, separate from logic):
  - *archetypes* — the ~15–20 mechanic alphabet.
  - *dungeons* — ordered route segments.
  - *cards* — `{ cue, promptType: recognize|recall|order, answer,
    archetypeRef, tags: { dungeon, segment, consequenceTier, role } }`.
- **Engine layer:** SRS scheduler (SM-2), session builder (draws due cards
  through active filters), grader.
- **Persistence layer:** all scheduling state batched into one stored object +
  settings. (Originally artifact-storage API; for a local repo build, target
  `localStorage`.)
- **View layer:** the modes.

**Modes (priority order):**

1. **Drill** — the core cue→response loop. Stark screen: at the moment of
   retrieval, just the cue + options. Self-grade on reveal.
2. **Archetype trainer** — learn the alphabet, made visual (simple diagrams).
3. **Route walk** — spatial; step through or drag pulls into order.
4. **Dashboard** — mastery heatmap, solid vs shaky per dungeon.
5. **Browse** — demoted plain reference.

**Scheduler note:** the session builder should **interleave** dungeons, not
block one at a time — harder in the moment, better retention, and it fights the
"eight dungeons blur together" problem.

## 5. UI style

- **Dark by default** — fits Midnight, kinder for repeated drilling.
- **Semantic color = the four consequence tiers**, so color itself teaches
  priority (dual-coding, not decoration):
  - 🔴 red = group wipe
  - 🟠 amber = your death
  - 🔵 blue = your job
  - ⚪ muted = flavor
- Clean sans for body; some character in the display face.
- Drill screen deliberately stark; **motion reserved for correct/incorrect
  feedback** only.
- Run through frontend-design guidelines so it doesn't read as a template.

## 6. Precedents

| Source | Borrowed idea |
|--------|---------------|
| Anki / SM-2 | SRS backbone, reveal-then-self-grade |
| Leitner boxes | visual SRS for the dashboard |
| Quizlet | one content base, many modes |
| Duolingo | mixed exercise types, low friction, instant feedback (minus hollow gamification) |
| Brilliant | teach through interaction, not text |
| Retrieval-practice + dual-coding research | testing effect; name + picture |
| Mythic Dungeon Tools | route-walk model |
| Boss WeakAura | "do this now" minimalism of the drill screen |

## 7. Content dependency ⚠

The app is **downstream of content that does not exist yet.** As of patch
12.0.5 the KB has only the S1 *overview*
(`knowledge/endgame/mythic-plus/season-1-overview.md`); per-dungeon detail
(routes, trash, boss abilities → cue/response pairs) is an open `## TODO` there.

"Fully-flesh one dungeon" therefore means **sourcing real mechanic data first**
(Blizzard journal API via `wowkb.blizzard` + Icy Veins, tier-highest source
first) and distilling it into `knowledge/` with full front matter — *then*
feeding the trainer. Don't let the app invent mechanics.

## 8. Dungeon pool (verified vs KB, patch 12.0.5, confidence high)

Source: `knowledge/endgame/mythic-plus/season-1-overview.md`.

| Dungeon | Origin |
|---------|--------|
| Magisters' Terrace | TBC (new to M+) |
| Maisara Caverns | Midnight (new) |
| Nexus-Point Xenas | Midnight (new) |
| Windrunner Spire | Midnight (new) |
| Algeth'ar Academy | Dragonflight (returning) |
| Seat of the Triumvirate | Legion (returning) |
| Skyreach | WoD (returning) |
| Pit of Saron | WotLK (returning) |

Locked pool all season → nothing memorized goes stale mid-season.

## 9. Suggested build sequence

1. **Archetype glossary** → `knowledge/systems/` (dungeon-agnostic, no live data
   needed). The foundation layer.
2. **One dungeon's content** → source + distill to `knowledge/` (start with
   Magisters' Terrace or whichever the player runs most).
3. **Engine** → React shell with SRS + Drill + Archetype mode, wired to (1)+(2).
4. **Remaining modes** → Route walk, Dashboard, Browse.
5. **Fill out the other 7 dungeons** once the engine is proven.

---

*Spec authored 2026-06-24 from the archived design conversation. Dungeon pool
cross-checked against the live KB. Update if game state moves past 12.0.5.*

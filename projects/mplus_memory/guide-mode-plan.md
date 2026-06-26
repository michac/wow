# Plan — Guide Mode (a click-through Adventure Guide for your phone)

*Supersedes the earlier "subway-map + accordion over content.json" sketch. New
direction, decided 2026-06-25: recreate the in-game Adventure Guide as a
phone-friendly website you tap through — and source it **only** from the journal
data, not the distilled Drill/Test KB.*

## Context

Drill and Test don't click at 365 cards — they're recall reps with no mental
model to hang them on. The fix is an **orientation-first guide** you reach for
*before* drilling. It should feel like **a presentation**: full-screen slides,
one boss at a time, tap to advance. The fast scan is shallow on purpose — boss →
lore → role tips — so you can click through a whole dungeon in under a minute and
build the gist. Ability detail is a deeper layer added later (see §Later).

Guide sits **alongside** Drill/Test (the on-ramp), not replacing them.

## Data + generator — done, journal-only

**`tools/wowkb/advguide.py`** (done) generates **`app/src/adventure-guide.json`**:
**8 dungeons, 29 bosses.** Per dungeon: `slug, name, lore, location, bosses[]`.
Per boss: `name, slug, artKey, encounterId, lore, roleTips{DD/Healer/Tank}[],
abilities[] (nested tree), loot[]`. All 29 `artKey`s match the existing
`app/src/assets/bosses/*.webp` portraits. Run: `uv run python -m wowkb.advguide`
(add `--refresh-db2` on patch days).

Pipeline (see `journal-text-investigation.md` for the full how/why):
`journal-instance` + `journal-encounter` (web API) → lore, role tips, ability
tree, loot; `Spell*` DB2 via wago.tools → resolved ability descriptions. **No
content.json, no Method/Icy Veins** — this guide is pure Blizzard source. The
tool mirrors `bossart.py`: roster read from the committed KB `### <Boss>
<!-- enc:NNN -->` headings (not the gitignored `raw/`), DB2 tables auto-pulled
into `raw/wago/` if missing, output byte-stable run-to-run.

## Phase 1 — the presentation (v1, the fast-scan path)

Phone-first, full-bleed, swipe/tap deck. **No timer, no grading, read-only.**

New components under `app/src/lib/components/`:
- **`Guide.svelte`** — entry. A grid of the 8 dungeons (name + hue); tap one to
  open its deck. Remembers last dungeon in component-local `$state`.
- **`GuideDeck.svelte`** — the slide runner. `let i = $state(0)`; prev/next
  buttons, left/right **swipe** (pointer events) and arrow keys, a progress
  indicator ("Boss 2 / 4") and dot strip. Slides = `[dungeon intro] +
  [one per boss]`.
- **`DungeonIntroSlide.svelte`** — title slide: dungeon name (display face),
  `location`, `lore`, and a row of boss portrait thumbnails as a roster preview.
- **`BossSlide.svelte`** — the core slide:
  - Portrait hero (reuse the art resolver). Phones are portrait, so give it real
    vertical room and frame from the top (`object-position` top / taller band) —
    fixes the existing "portraits crop" complaint by spending the headroom.
  - Boss **name** + one-line **lore**.
  - **Role tips** — emphasize the player's role from `store.settings.role`
    (defaults DPS): show that list big with generous tap targets; the other two
    roles sit behind a small toggle. Strip/transform the `[Ability]` bracket
    markers into bold (they're AG hyperlink syntax).

Reuse / extract:
- Pull the portrait resolver out of `DungeonFrame.svelte:16-28` into
  `lib/bossArt.js` (the `import.meta.glob` over `assets/bosses/*.webp` keyed by
  `artKey`); both `BossSlide` and `DungeonFrame` import it. The AG JSON's
  `artKey` already uses the same `<dungeonSlug>__<bossSlug>` convention.
- Per-dungeon `--dgn` hue, display/body type, dark theme — all already in the
  token system.

New content layer:
- **`lib/guide.js`** — imports `adventure-guide.json`, exposes
  `guideDungeons`, `guideDungeon(slug)`. Mirrors `content.js`'s selector style.
  Kept separate from `content.js` so the guide and the trainer don't entangle.

Wiring:
- **`ModeNav.svelte`** — turn the disabled `route` entry into a live
  `{ id: "guide", icon: "🗺", label: "Guide", on: true }`.
- **`App.svelte`** — `{:else if store.settings.mode === "guide"} <Guide />`.
- **`store.svelte.js`** — none needed (`setMode("guide")` already works).

## Later — folding ability detail into the tour

The fast path stays shallow; depth is one tap away, recommended order:

1. **"Mechanics ▾" expander on each `BossSlide`** (build first) — reveals the
   nested `abilities[]` as a one-open-at-a-time **`AbilityAccordion.svelte`**
   (headers = ability names, expand = resolved description; children indent under
   parents, exactly the journal tree). Non-modal, so it never breaks the
   click-through. This is the natural home for the resolved AG text.
2. **Two-speed deck (option):** a "Quick tour" vs "Full guide" toggle at dungeon
   start; Full inserts one sub-slide per top-level ability so the presentation
   itself walks the mechanics. Decide after using the expander.
3. **Cross-link to the trainer (option):** later, tag guide abilities with the
   archetype/tier from `content.json` (match on spell name) so a boss slide can
   show "you have N shaky cards here → Drill them," tying Guide → Drill.

## Files

| File | Change |
|------|--------|
| `tools/wowkb/advguide.py` | **done** — generator → `app/src/adventure-guide.json` |
| `app/src/adventure-guide.json` | **done** — bundled data (8 dungeons / 29 bosses) |
| `projects/mplus_memory/journal-text-investigation.md` | done (method) |
| `app/src/lib/guide.js` | new — selectors |
| `app/src/lib/bossArt.js` | new — extracted portrait resolver |
| `app/src/lib/components/Guide.svelte` | new — dungeon picker |
| `app/src/lib/components/GuideDeck.svelte` | new — slide runner |
| `app/src/lib/components/DungeonIntroSlide.svelte` | new |
| `app/src/lib/components/BossSlide.svelte` | new |
| `app/src/lib/components/AbilityAccordion.svelte` | new (Later §1) |
| `app/src/lib/components/DungeonFrame.svelte` | refactor to use `bossArt.js` |
| `app/src/lib/components/ModeNav.svelte` | `route` → live `guide` |
| `app/src/App.svelte` | route `mode === "guide"` |

## Verification
- `app && bun run dev` → tap **Guide** → pick a dungeon. Confirm: intro slide
  (lore + roster), then one slide per boss with portrait + lore + DPS role tips;
  swipe/arrows/dots navigate; progress reads "Boss n / N"; portraits frame the
  face (no head-crop). Cycle all 8 dungeons — all 29 bosses render, no console
  errors.
- `bun run build` succeeds; Drill / Test / Alphabet still work (Guide additive).
- Regenerate data: running `advguide.py` reproduces `adventure-guide.json`
  byte-stable (modulo patch changes).

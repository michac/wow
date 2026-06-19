# Talent Calculator — prototype spec

Status: **in progress** · Owner: Michael · Created: 2026-06-18

## Progress log

- **2026-06-18 — Milestone 4 done (loadout codec).** Pure `app/src/lib/codec.ts`
  encodes/decodes Blizzard v2 loadout strings; **acceptance gate passes**:
  `encode(decode(ORACLE)) === ORACLE` byte-for-byte against the real Wowhead
  Affliction/Soul-Harvester string. Format nailed down: a *bitstream* at 6 bits
  per base64 char (standard charset, LSB-first per char, final char zero-padded —
  **not** byte-aligned); header `version(8)=2 · specId(16) · hash(128)=0`; per
  node `isSelected[/isPurchased[/isPartial[ranks6]/isChoice[idx2]]]`.
  **Correction to the investigation's premise: N = 202, not 207.** The "207"
  was a greedy-decode artifact — the oracle's 601 real body+header bits pad to
  606 (5 zero bits), and reading those as unselected slots faked 5 extra nodes.
  DB2 has exactly 202 nodes in tree 720; `tree_node_count` was right all along.
  The real data gaps were (a) emitting N, (b) the 3 auto-granted
  (selected-not-purchased) slots, and (c) the dropped type-3 hero-selector node.
  Closed in `tools/wowkb/talents.py` (`_codec_meta`): each spec's JSON now carries
  `serial_count`, `granted_serials` (class/spec `TraitCond` CondType==2 grants +
  each usable hero tree's prereq-less keystone root), and `hero_selector`
  `{serial, choices}`. For Affliction this derives exactly `{10,84,94}` granted +
  selector serial 103 → byte-identical. Stage B passes the three fields through;
  `types.ts` gains `serialCount`/`grantedSerials`/`heroSelector`. The codec keeps
  granted/selector slots **out** of the user `Build` (decode skips them, encode
  re-emits from data), so decode→`Build` drops straight into `BuildController`
  and structural round-trips stay clean. `codec.test.ts` (25 tests via `bun test`):
  header LSB parse, oracle decode (spec 265, hero Soul Harvester, 73 purchased,
  34/31/13 pts), the byte-identical acceptance test, 6-class structural
  round-trips (choice + a forced partial multi-rank node), and malformed /
  wrong-spec / version-mismatch errors. Full suite 36 green; `bun run check`,
  `bun run build`, and `talents verify` all clean. Regenerated all 40
  `talents.json` + app data. **Residual:** the oracle is fully maxed, so the
  `isPartial` path is only covered structurally, not against a real partial
  string; spec-set-scoped grants are skipped (`SpecSetMember` unfetched at this
  build) — none affect the warlock oracle. **Next:** icons + tooltips + URL share
  (milestone 5) — wire `decodeLoadout`/`encodeLoadout` to a paste/copy box + hash.
  Still deferred: Stage A enrichment, Stage A′ real budgets (hardcode remains).
- **2026-06-18 — Milestone 3 done (interaction + validation).** Split into a pure
  validator (`app/src/lib/validate.ts` — gates, OR-prereqs with the fully-ranked
  rule, choice exclusivity, per-tree budget, and a fixpoint cascade prune) and a
  reactive `BuildController` (`app/src/lib/build.svelte.ts`, `SvelteMap` state,
  shared via context). Trees are now a working editor: left-click spends /
  shift-click maxes / right-click removes, choice nodes pick one half, visual
  states (selected/maxed/available/locked) with reason tooltips, header HUD +
  Reset, per-tree spent/budget. Unit suite `validate.test.ts` (11 tests via
  `bun test`) covers the high-risk rules; `bun run check` clean.
  **Data fix along the way:** hero `req_points` was wrongly inheriting the spec
  tree's gate lines (`is_for_class=false`), giving `req 8/20` that deadlocked the
  hero entry node. Root-caused in `tools/wowkb/talents.py` (`_api_node` now zeroes
  the gate for hero — hero trees gate by level 71 + prereq edges, not points);
  regenerated all 40 `talents.json` + the app data. See
  `knowledge/classes/_talents/README.md` → "Gates & leveling". **Next:** codec
  (milestone 4). Still deferred: Stage A icons/desc + Stage A′ real budgets — the
  point budget remains the provisional hardcode (`{class:31, spec:30, hero:11}`),
  which is TWW-era and undercounts Midnight's level-90 totals.
- **2026-06-18 — Milestones 1 + 2 done (data spike + static render).** Scaffolded
  `app/` (Bun 1.3.14 + Vite 6 + Svelte 5 + TS); `bun install`, `bun run check`
  (0 errors), `bun run build` all clean. Stage B (`app/scripts/build-data.ts`)
  compacts all **40 specs / 13 classes / 4562 nodes** from
  `knowledge/classes/**/talents.json` → `app/static/data/{index.json,<class>/<spec>.json}`
  (per-spec ~20 KB raw / ~5–6 KB gz). App renders any spec's three trees (class /
  spec / hero) as DOM nodes + one SVG edge layer, with a class/spec picker and
  hero-tree toggle; node shape varies by type (square ACTIVE / circle PASSIVE /
  split CHOICE), gated nodes dashed, patch/build badge from `index.json`.
  Bundle 17 KB gz. **Next:** interaction + validation (milestone 3). Still
  deferred: codec (4), icons/desc Stage A + budgets Stage A′ (5) — point budget
  is a provisional hardcode (`{class:31, spec:30, hero:11}`) until Stage A′.

A fast, web-hostable WoW talent calculator for **Retail / Midnight (12.0.x)**,
driven by the talent database this repo already generates
(`knowledge/classes/<class>/<spec>/talents.json`, built by
`tools/wowkb/talents.py`).

## Decisions (locked)

| Axis | Choice | Why |
|------|--------|-----|
| Rendering | **DOM nodes + SVG edges** | ≤~70 nodes on screen; DOM gives free tooltips, hit-testing, focus, a11y. SVG for crisp connector/gate lines. Canvas would reimplement all of that for no perf win at this scale. |
| Data delivery | **Static, lazy per-spec** | Patch-versioned JSON on a static/CDN host. Tiny `index.json` + fetch one spec (~8 KB gz) on select. No backend, no DB, free hosting. |
| Stack | **Svelte + Vite + TypeScript, run on Bun** | Compiles to near-vanilla JS, reactive state for free, tiny bundle. Bun = package manager + runtime; runs the `.ts` data script directly (no `tsc`/`ts-node`) and runs Vite. |
| Hosting | **Static** (GitHub Pages / Cloudflare Pages) | Data only changes on patch day → no API justified. |

> **`static/data/` vs `dist/`** — two different folders, easy to conflate:
> `static/data/` is the runtime **input** JSON the app *fetches* (Stage B
> output, served as plain assets). `dist/` is the compiled **app** (Svelte →
> JS/CSS/HTML) — that's what you host.

### v1 scope (all in)
- **Import/export strings** — encode/decode Blizzard loadout strings.
- **Spell icons + tooltips** — neither icon nor description text exists in the
  KB today (entries carry only name + `spell_id`); both are resolved in Stage A
  from the Blizzard API and rendered as our own tooltips (no Wowhead dependency).
- **Shareable URL state** — build encoded in the URL hash.
- **Point/gate validation** — req_points gates, prereqs, choice exclusivity, budget.

## Goals / non-goals

**Goals**
- Snappy: instant interaction (no network on click), fast first paint, smooth.
- Faithful to live game rules so exported strings paste straight into the game.
- Provenance-aware: surface the `patch`/`build` the data was generated from
  (repo staleness doctrine — see root `CLAUDE.md`).
- Zero server. Deploy = upload a static `dist/`.

**Non-goals (v1)**
- Sims / DPS numbers, gear, stat weights.
- Accounts, server-side saved builds, social features.
- Classic / pre-Midnight trees.
- PvP talents (revisit later; not in the current data model).

## Architecture overview

```
knowledge/classes/**/talents.json   (existing, patch-versioned, committed)
        │
        │  Stage A — icon enrichment (python, patch-day, in wowkb)
        ▼
knowledge/...talents.json  +  entries[].icon slug   (or icons sidecar)
        │
        │  Stage B — web compaction (node prebuild in the app, no network)
        ▼
app/static/data/index.json            (specs list + meta + budgets)
app/static/data/<class>/<spec>.json   (compact per-spec graph)
        │
        │  fetch on spec-select
        ▼
Svelte app  ──renders──►  DOM nodes + SVG edges
   ├─ state: Map<node_id, {rank, choiceIndex}>
   ├─ validation engine (gates / prereqs / choice / budget)
   ├─ loadout codec (Blizzard import/export strings)
   └─ URL hash sync (#<class>/<spec>/<code>)
```

Two transform stages, split by whether they need the network:
- **Stage A** needs the Blizzard API (resolve `spell_id → icon`), so it lives
  with the existing python pipeline and uses its cached `raw/` + credentials.
- **Stage B** is a pure local transform (no network), so it ships inside the
  app and runs as a `prebuild` from the committed knowledge JSON. Keeps the app
  buildable without python or API creds.

## Data pipeline

### Stage A — spell enrichment: icon **and** description (python, patch day)
Verified: entries today carry only `talent` (name) + `spell_id` — **no icon and
no description text**. Both must be resolved; this is new pipeline work. Once per
patch, for each distinct `spell_id`:
- **Icon:** GET `/data/wow/media/spell/{id}` (Blizzard media, Tier 1) → icon slug
  from the asset URL (`.../icons/.../<slug>.jpg`).
- **Description:** GET the spell endpoint (Tier 1) → effect/description text, so
  we render **our own** tooltips and avoid depending on Wowhead's (undated)
  tooltip script. (Wowhead's only unique value was this text + an icon mirror;
  both are self-sourceable, keeping us inside the repo's provenance doctrine.)
- Both reachable today via `wowkb.blizzard get` (raw escape hatch); wire a small
  loop/subcommand. Cache responses in `raw/` (gitignored).
- Emit `icon` + `desc` onto each entry in `talents.json` (prefer inline so the
  per-spec file stays self-contained).
- **Risks:** some `spell_id`s may lack media/description (choice/aura spells) →
  placeholder icon + empty desc, log misses (mirror the existing `verify`
  reporting style). Rate-limit the calls.

### Stage A′ — point-budget data (python, patch day)
Verified reliable source: the level→points curve lives in **`TraitCurrencySource`**
(DB2, Tier 1), which is **not currently fetched** — add it to `WAGO_TABLES`.
It maps `(currency, level) → points granted`, giving per-tree (class/spec/hero)
budgets for **any character level** straight from game data (no hardcode).
- Cross-check available now: Blizzard's starter loadouts (`TraitTreeLoadoutEntry`,
  already cached) sum to **~76 points** at max level (class ~31 + spec ~30 +
  hero ~10–11), so the level-90 totals are verifiable even before the curve lands.
- Emit a `budgets` block into `index.json`: `{ currencyId → [{minLevel, points}] }`
  plus the tree→currency mapping (`TraitTreeXTraitCurrency`, already fetched).

### Stage B — web compaction (node, app prebuild)
Read `knowledge/classes/**/talents.json` → emit static data the app fetches.
Goals: small bytes, app-ready shape, no runtime parsing of stringly fields.

- `index.json`: `{ patch, build, fetched, classes:[{slug,name,id,specs:[{slug,name,id,heroTrees:[…]}]}], pointBudget }`.
- `<class>/<spec>.json`: compact graph (see schema below). Normalize numeric
  fields (`max_ranks`, `entry_id`, `choice_index` are strings in source → ints).
  Normalize node coords (use raw `x`/`y`; offset/scale per tree to a 0-based box).
- Keep files per-spec so a switch fetches ~8 KB gz. Let the host gzip/brotli.

### Compact per-spec schema (draft)
```jsonc
{
  "spec": "arcane", "class": "mage", "specId": 62, "treeId": 658,
  "patch": "12.0.7", "build": "12.0.7.67808",
  "trees": {
    "class": { "nodes": [Node, …] },
    "spec":  { "nodes": [Node, …] },
    "hero":  { "Sunfury": { "nodes": [Node, …] }, "Spellslinger": {…} }
  }
}
// Node:
{
  "id": 80175, "type": "PASSIVE|ACTIVE|CHOICE",
  "x": 0, "y": 600,                 // normalized layout coords
  "serial": 12,                     // serial_order (export-string walk)
  "req": 8,                         // req_points gate (0 = ungated)
  "prereq": [80170],                // prereq_node_ids
  "entries": [                      // 1, or 2 for CHOICE
    { "id": 12345, "name": "Amplification", "spell": 236628,
      "ranks": 2, "icon": "spell_arcane_arcane01",
      "desc": "Arcane Missiles deals 4% more damage.",  // from Stage A
      "choice": 0 }
  ]
}
```

## Rendering

- **One SVG layer** under the nodes for: prereq edges (node→node), gate lines
  (the horizontal "spend N points" dividers from `req_points`), and the
  selected/locked styling of edges.
- **DOM node** per talent: icon (`<img loading=lazy>`, Blizzard media or zamimg
  mirror by slug), rank pip `x/max`, square (active) vs octagon/circle (passive)
  vs split (choice) shape via CSS. Hover → **our own tooltip** built from the
  enriched `name` + `desc` (no Wowhead script).
- **Layout** from normalized `x`/`y` (authoritative pixel positions from the
  API). Each of class/spec/hero is its own coordinate box; lay them side by side
  or stacked. Scale to fit; no manual hand-placement.
- **Three trees visible:** class, spec, and the user-chosen hero subtree (toggle
  between the spec's 2 hero trees).
- Interaction: left-click adds a rank / picks a choice, right-click removes,
  shift-click max/clear. Aim for <1 frame from click to repaint.

## State & validation engine

State = `Map<nodeId, { rank: number, choiceIndex: 0|1 }>` plus selected hero tree.

Validation must match the game so exports are legal:
- **Budget:** per-tree points (class/spec/hero) from `index.json` `budgets`,
  evaluated at the selected **character level** (default 90). Source is
  `TraitCurrencySource` (Tier 1) — see Stage A′. Level selector is a v1 feature;
  hardcoding the level-90 totals (~76) is the trivial fallback.
- **Gates:** a node with `req: N` is locked until ≥N points spent earlier in
  that tree.
- **Prereqs:** `prereq` nodes must be filled (to their unlocking rank) first.
- **Choice nodes:** exactly one entry selectable.
- Removing a node that others depend on cascades (refund dependents) — match
  in-game behavior.
- Surface: points spent/remaining per tree; illegal/over-budget highlighted.

## Loadout import/export strings (the killer feature) — ✅ done (M4)

Implemented in `app/src/lib/codec.ts` (`decodeLoadout` / `encodeLoadout` /
`peekHeader` + error types). **As-built, confirmed byte-for-byte against a real
Wowhead string** (the ORACLE in `codec.test.ts`). The earlier sketch here had
two errors — it omitted the `isPurchased` bit and guessed N=207; both corrected
below.

Blizzard loadout string = **bitstream → base64**. The bitstream is emitted **6
bits per base64 char**, **LSB-first within each char**, standard charset
`A-Za-z0-9+/`, final char zero-padded. It is **not** byte-aligned (a common
mis-assumption — byte alignment yields the wrong char count).

- **Header:** `version(8)=2` · `specId(16)` · `treeHash(128)`. The hash is
  **all-zero** in third-party strings and the game accepts it → we emit 16 zero
  bytes (risk eliminated).
- **Body — one slot per node, walked over the whole class-wide tree** in
  ascending node-id order, `serialCount` slots total (warlock = **202**, not the
  207 the greedy decode appeared to show). Per slot:
  - `isSelected(1)`; if selected:
    - `isPurchased(1)`; if purchased:
      - `isPartiallyRanked(1)` → `ranksPurchased(6)` if partial
      - `isChoice(1)` → `choiceIndex(2)` if choice

Slots the game auto-fills (the encoder reproduces them from static spec data,
not from the user `Build`):
- **Granted nodes** (`spec.grantedSerials`): free talents, emitted
  `isSelected=1, isPurchased=0`. Derived in `talents.py` as class/spec
  `TraitCond` CondType==2 grants + each usable hero tree's prereq-less keystone.
- **Hero selector** (`spec.heroSelector`): the type-3 node whose 2-bit choice
  index picks the active hero tree (`{serial, choices:[name...]}`).

The decoder keeps granted/selector slots out of the `Build` (so it drops straight
into `BuildController`); the encoder re-adds them, so round-trips are clean and
the oracle re-encodes identically.

**Acceptance test (the gate, passing):** `encode(decode(ORACLE)) === ORACLE`,
byte-identical, plus 6-class structural round-trips. The oracle is fully maxed,
so the `isPartial`+ranks path is only covered structurally — harden later with a
real partially-ranked string.

## URL / share state

- Hash: `#<class>/<spec>/<loadoutCode>` (reuse the export string, or a shorter
  internal code). Pasting a link reproduces the build fully client-side.
- On load, parse hash → fetch spec → apply build. On change, debounce-write hash.

## Repo layout (proposed)

```
app/                         # the Svelte app (new), run on Bun
  src/
    lib/codec.ts             # loadout string encode/decode
    lib/validate.ts          # gates/prereqs/choice/budget (level-aware)
    lib/layout.ts            # coord normalization
    components/*.svelte      # Tree, Node, Edge, Tooltip, SpecPicker, LevelPicker
  scripts/build-data.ts      # Stage B compaction — run via `bun run`, no tsc
  static/data/               # Stage B output (runtime input); commit (see below)
  vite.config.ts             # Vite under Bun; static adapter -> dist/
  package.json               # bun install / bun run dev|build|build-data
tools/wowkb/talents.py       # extend: Stage A (icon+desc) + Stage A′ (budgets)
```
Open: commit `app/static/data/` (simple, diffable per patch) vs generate on CI.
Lean **commit it** — it's small, patch-versioned, and matches the repo's
"everything is greppable + provenanced" ethos.

## Milestones

1. ✅ **Data spike** — Stage B compaction **done for all 40 specs** (not just one);
   JSON eyeballed (schema matches the draft). Icon-strategy sampling still TODO
   (deferred to milestone 5, where icons actually land).
2. ✅ **Static render** — Svelte renders a spec's three trees from compact JSON,
   layout + prereq edges, no interaction. Build/type-check clean; bundle 17 KB gz.
   Visual "snappy first paint" eyeball still pending (run `cd app && bun run dev`).
3. ✅ **Interaction + validation** — click to spend; gates / OR-prereqs (fully-
   ranked rule) / choice exclusivity / per-tree budget / cascade prune. Pure
   validator + reactive controller; 11-test `bun test` suite, `bun run check`
   clean.
4. ✅ **Codec** — encode/decode; round-trip acceptance test
   (`encode(decode(ORACLE))===ORACLE`, byte-identical) passing, plus 6-class
   structural round-trips. Pure `codec.ts`; 25-test `bun test` suite.
5. **Icons + tooltips + URL share** — Stage A enrichment, CDN icons, hash state.
   ← **next**
6. **All 40 specs + spec picker + patch badge** — full `index.json`, deploy.

## Resolved (was open)

- **Point budgets** — reliable Tier-1 source confirmed: `TraitCurrencySource`
  (level→points), add to the wago fetch. Build the level selector; default 90;
  cross-checkable against the ~76-point starter loadouts already cached.
- **Tooltips** — roll our own from Stage-A `desc` (Blizzard spell API). Wowhead
  brought only tooltip text + an icon mirror, both self-sourceable → no dep.
- **Stack/runtime** — Bun runs Vite + the `.ts` data script directly. **Confirmed
  working** (Bun 1.3.14 installed): `bun run scripts/build-data.ts` runs the TS
  with no `tsc`/`ts-node`; `bun run dev|build` drives Vite. The Bun script is
  intentionally excluded from the app's DOM-lib `tsconfig` (it uses node/Bun
  globals); add a separate `tsconfig.scripts.json` if it needs checking later.

## Still open

- **Icon CDN:** Blizzard media URLs vs zamimg-by-slug — pick the more stable;
  placeholder fallback either way.
- **PvP talents** — out of v1 (not in the current data model); note for later.
- **Commit generated `static/data/` vs CI-generate** — leaning commit
  (small, patch-versioned, diffable, matches the repo's greppable ethos).
- **Spell-API rate/coverage** — ~hundreds of distinct `spell_id`s to enrich;
  confirm the media+spell endpoints cover talent spells and pick a polite rate.
```

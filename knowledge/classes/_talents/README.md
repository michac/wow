---
title: Talent database — schema & regeneration
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-18
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* tables (Tier 1)
confidence: high
---

# Talent database

A local, greppable database of every class/spec/hero talent tree for the
current patch, regenerated each patch day by `tools/wowkb/talents.py`.

## Files

| File | One row/record per | Use |
|------|--------------------|-----|
| `all-talents.tsv` | talent **entry** (CHOICE nodes → 2 rows) | grep/awk lookups, patch diffs |
| `trees.tsv` | class/spec/hero **tree** | index for joins, node counts |
| `../<class>/<spec>/talents.md` | spec (human-readable) | reading, citing in answers |
| `../<class>/<spec>/talents.json` | spec (graph-shaped) | tooling / talent-calculator app |

## How the data is sourced (hybrid)

- **Primary = Blizzard Game Data API talent-tree endpoints** (Tier 1). They
  group nodes into class / spec / hero per spec with spell names resolved, and
  give prerequisites (`locked_by`) and choice options (`choice_of_tooltips`).
- **Required = wago.tools `Trait*` DB2 CSVs** (Tier 1). They cross-check the API
  and supply the two columns the Game Data API does **not** expose — the
  export-string node ordering (`serial_order`) and choice ordinal
  (`choice_index`) — and drive the PTR-only path (the API has no PTR data).

Both are pinned to the **same build** (the API's static build, e.g.
`12.0.7.67808`), so the DB2 join is exact.

### API quirks handled in the build

- The tree endpoint duplicates each usable hero tree's ~14 nodes into
  `spec_talent_nodes`; we strip all hero-tree node ids back out of the spec
  (and class) sections so each node lands in exactly one tree.
- The tree endpoint lists *every* class hero tree per spec. The **2** a spec
  may use are those named by the `/playable-specialization/{id}` endpoint
  **and** populated (their nodes overlap `spec_talent_nodes`) — this drops
  unreleased `[DNT]` placeholder trees.
- Placeholder/selector CHOICE nodes that carry no granted spell (empty in both
  the API and DB2) are omitted.
- **Hero `req_points` is forced to 0.** Hero trees have no points-spent gate
  (see "Gates & leveling" below). The API's `restriction_lines` describe only
  class/spec gates, but they carry an `is_for_class` flag and nothing marks them
  hero-specific — so a naive match hands hero nodes the **spec tree's** gate
  lines (`is_for_class=false`), giving spurious `req 8`/`20` that exceed the
  ~11-point hero budget and deadlock the hero entry node. `_api_node` zeroes the
  gate for `kind == "hero"`.

## Gates & leveling (game rules behind `req_points`)

`req_points` is a node's **gate**: the points that must be spent *in that same
tree* before it unlocks. Sourced from the API's `restriction_lines` (the
horizontal divider lines drawn across a tree).

- **Class / spec trees are gated.** Two gates: **8** (opens the middle rows) and
  **20** (opens the lower rows). In **Midnight** the class tree's deepest gate
  rose **20 → 23** (Blizzard, *Level Up Your Talents in Midnight*) — so some
  class trees show `req 23` (e.g. Warrior) while others top out at `20`.
- **Hero trees are NOT point-gated.** They gate by **character level** (the tree
  unlocks at level **71**) plus prereq edges (`locked_by`) within the tree —
  never by points spent. Hence the forced `req 0` above.
- **When points unlock (by level):** class/spec talents begin at **level 10** and
  award 1 point per level, alternating class→spec, up through the cap. Hero
  talents award 1 point per level from **71**. Midnight (cap **90**) adds **10**
  new points across levels 81–90: **+3 class, +4 spec, +3 hero**. (Exact level-90
  per-tree budgets come from `TraitCurrencySource` — Stage A′, not yet fetched;
  the app uses a provisional hardcode until then.)

Sources: [Level Up Your Talents in Midnight](https://news.blizzard.com/en-us/article/24230699/level-up-your-talents-in-midnight)
(Tier 1) · [Dragonflight Talent Preview](https://news.blizzard.com/en-us/world-of-warcraft/23797209/world-of-warcraft-dragonflight-talent-preview)
(Tier 1, level-10 start + 31/30 base).

## `all-talents.tsv` columns (tab-separated, header row)

| Column | Meaning |
|--------|---------|
| `class`, `class_id` | class slug (`death-knight`) + numeric id |
| `spec`, `spec_id` | spec slug (`beast-mastery`) + numeric id |
| `tree` | `class` \| `spec` \| `hero` |
| `hero_tree` | hero subtree name (e.g. `Soul Harvester`), else empty |
| `node_id` | TraitNode id (shared by the 2 rows of a CHOICE node) |
| `node_type` | `PASSIVE` \| `ACTIVE` \| `CHOICE` |
| `entry_id` | TraitNodeEntry id (DB2) |
| `talent` | talent name |
| `spell_id` | granted spell id |
| `max_ranks` | rank cap for this entry |
| `req_points` | points that must be spent in-tree to unlock (gate); empty if ungated |
| `row`, `col` | grid position (`display_row`/`display_col`) |
| `choice_group` | CHOICE node id grouping its 2 entries; empty otherwise |
| `prereq_node_ids` | comma-joined unlock prerequisites (`locked_by`) |
| `serial_order` | node position in the export-string bitstream walk (ascending node id within the tree) — **DB2** |
| `choice_index` | this entry's ordinal among the node's entries, 0 or 1 for CHOICE, else 0 — **DB2** |

`serial_order` + `choice_index` make the TSV sufficient to write a loadout
export-string encoder/decoder later without re-fetching. `serial_order` is per
**tree** (shared across a class's specs); a class's range has small gaps where
DB2 carries type-3 selector/grant nodes that hold no talent.

## Grep recipes

```bash
cd knowledge/classes/_talents
awk -F'\t' '$1=="mage" && $3=="arcane"' all-talents.tsv      # Arcane node set
grep -iP '\tHaunt\t' all-talents.tsv                          # find a talent by name
awk -F'\t' '$5=="hero"' all-talents.tsv | cut -f6 | sort -u   # every hero tree
awk -F'\t' '$8=="CHOICE"' all-talents.tsv                     # all choice options
```

## Regenerate (patch day)

```bash
cd tools
uv run python -m wowkb.talents fetch                  # live: API + wago @ API build
uv run python -m wowkb.talents build --fetched <YYYY-MM-DD>
uv run python -m wowkb.talents verify                 # sanity report
```

For **PTR** (the Game Data API has no PTR data), force the DB2-only path:

```bash
uv run python -m wowkb.talents fetch --build 12.0.7.<ptr>   # wago only
```

(The DB2-only `build` path is stubbed — wire it up when a PTR pull is needed;
outputs are stamped `confidence: medium` + a "PTR/DB2-derived" note.)

Also bump the build in `knowledge/_meta/game-version.md` on patch day; the
generated front matter reads `patch`/`build` from the fetch manifest.

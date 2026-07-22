# WoW Q&A Agent Workspace

This repo is a knowledge base + ingestion toolkit for answering World of
Warcraft questions **reliably**. Scope: **Retail, Midnight expansion only**
(no Classic, no leveling-era content unless asked historically).

## Git workflow

Single dev, single line of history: **work on, commit to, and push whatever
branch the repo is already checked out on** — even if that's `main`. Do **not**
create a new branch, `git checkout -b`, or switch branches unless explicitly told
to — no PRs, no surprise branches. If you think a different branch is warranted,
**ask first**; never silently start working off a branch you created.

**Don't mother-hen the git state.** This is a scratch-history repo; uncommitted
work sitting in the tree is the normal resting state, not a problem to flag.
Commit and push **only when asked** — do not offer to commit, do not append
"(not pushed)" / "changes are uncommitted" / "want me to commit?" to answers,
and do not treat a dirty tree as a finding. If a `git status` detail actually
matters to the question, state it once, plainly, and move on. (Exception: the
gitignored sub-repos — `planner-state/`, `projects/cooldown-hud/addon/`,
`projects/keybinder/addon/` — where
"a push does not reach the game, you must cut a release" is a real deploy fact
worth saying when a deploy is in play.)

**Pushing this repo ⇒ push the addons too.** If you push **this** repo to
GitHub, assume I also want the latest addon code on GitHub for all three sub-repos
(they're separate repos a wow-repo push does not touch). So when you push here,
run `wowkb.addon check` and, for any addon it flags with **unpushed** commits,
`git -C <path> push` it as well; if it flags **uncommitted** changes, surface
that to me first. (`check` is read-only and exits non-zero when anything is
local-only — a clean pre-push gate.) Cutting a release is a separate, ask-first
step — this is just "don't leave addon commits stranded on one machine."

## Current game state

- **Live: patch 12.0.7 "Revelations"** — Midnight expansion, level cap **90**,
  Season 1 (went live 2026-06-16). No PTR currently.
- `knowledge/_meta/game-version.md` is the **single source of truth** for
  game state and must be updated on patch days. If anything in this file
  disagrees with it, that file wins.

## Staleness doctrine (read this before answering anything)

WoW is 22 years old. **Most of the internet describes a dead version of the
game.** Defenses, in order:

1. Answer from `knowledge/` first — it carries provenance.
2. Every KB file has YAML front matter: `patch`, `fetched`, `sources`,
   `confidence`. Treat `patch` older than live as needing re-verification.
3. When web-searching, require **"Midnight" / "12.0" / 2026** signals in
   results. Undated or pre-2026 content is suspect by default; pre-Midnight
   mechanics (The War Within 11.x and earlier) are historical.
4. Trust tiers live in `knowledge/_meta/sources.md`:
   1 = Blizzard API / wago.tools / patch notes / simc APLs,
   2 = Warcraft Logs / Archon, 3 = Icy Veins / Method / class Discords /
   trusted YouTubers, 4 = Wowhead editorial / Reddit / SEO sites (corroborate).
5. **Answers must cite the patch version and at least one source.** If
   confidence is low or data is stale, say so explicitly.
6. Volatile data (AH prices, token price, realm status, "what event is up
   this week") is **never** answered from the KB — fetch live.

## Directory map

- `knowledge/_meta/` — game version (source of truth), source trust registry,
  `moving-values.md` (flattened latest-value-wins stale-data catcher — check it
  when a source's reward tier/ilvl looks off), `patch-notes/` (verbatim archive
  of official notes, against link rot), `changelog-<patch>.md` (per-patch diff),
  `feed-watermark.md` (the "reviewed through" cursor that drives `/update`),
  `verify-in-game.md` (**generated** "confirm while logged in" checklist —
  collected from `@verify-ingame` markers by `wowkb.gen_verify`; `/sync-characters`
  surfaces it. Resolve an item → edit the claim + drop the marker + regen),
  `kb-inbox.md` (**free-form parking lot** — drop any un-routed todo here instead of
  half-implementing it or asserting an unvalidated claim into `knowledge/**`: tooling
  ideas, addon features, research-to-do, structural work. Distinct from the three
  scoped queues — in-game-verify markers, `discovered-weeklies.json`, session
  `todo.md`; route/strike items as they land. Not harvested by any tool)
- `knowledge/endgame/` — `weekly-checklist.md` (the anchor doc), `raids/`,
  `mythic-plus/`, `delves/`, `prey.md`, `great-vault.md`, `world-events.md`
- `knowledge/characters/` — per-character snapshots from the Blizzard
  profile API (volatile — re-fetch live before answering; files are context).
  **To update these, use the `/sync-characters` command (or
  `wowkb.character <name>` for a single one). Don't re-improvise the API
  calls + Syndicator parse by hand.**
- `knowledge/factions/` — one file per renown faction (5)
- `knowledge/classes/<class>/<spec>/` — rotation.md, builds.md, gearing.md, sims.md
  (also abilities.md, talents.md/.json, maxroll-*.md captures). **builds.md =
  talents / loadouts / hero-tree only; gearing.md = stats / trinkets / tier-set /
  embellishments / enchants / gems / consumables.** This split exists for the 6
  DH/Warlock specs (devourer/havoc/vengeance + affliction/demonology/destruction)
  as of 2026-07-14; rolling it out to the other 34 specs is a documented follow-up.
- `knowledge/systems/` — housing, ritual sites, void incursions, professions
- `knowledge/economy/` — pointers to live tools only; never cached prices
- `knowledge/planning/` — **the session-planner system** (rank "what should I
  do this session?"). Start at `planning/README.md` (overview + roadmap +
  cross-machine resume runbook); `scoring-model.md` is the scoring contract,
  `activities/*.md` the task catalog (`_facets.md` = its tag contract).
  `candidates.json` is the ranker input — **generated** from `activities/*.md`
  by `wowkb.gen_candidates`; edit the `.md`, not the JSON. Feeds off the
  **PlannerState** addon via `wowkb.plan`. `discovered-weeklies.json` is
  **auto-maintained** by `wowkb.plan` from the addon's active-quest-log dump —
  weeklies the watchlist doesn't track yet land there to be verified + promoted
  into `wowkb.repeatables`' seed (don't hand-curate it as a source of truth).
- `planner-state/` — **local checkout of the PlannerState addon** (separate repo
  `michac/wow-planner-state`; **gitignored** here via `/planner-state/`, so the
  wow repo never sees it as an embedded repo). This is the addon **source of
  truth** — edit `planner-state/PlannerState/*.lua` here, then deploy per that
  folder's `CLAUDE.md` (bump `.toc` Version + `schema`, luaparser-check, commit,
  **cut a GitHub release**, `ghaddons update`, in-game `/ps` + `/reload`). A plain
  push does **not** reach the game. Don't confuse it with the *installed* copy
  under `…/_retail_/Interface/AddOns/PlannerState/`.
- `addon-manager/` — `ghaddons`, a GitHub-driven WoW addon manager (installs
  PlannerState + any other addon from a repo list). Its own README; stdlib-only.
  **The one deploy command**, for any of our addons, runnable from any directory:
  ```bash
  PYTHONPATH=~/code/fun/wow/addon-manager python3 -m ghaddons.cli update <owner/repo>
  ```
  It installs from the **latest GitHub release**, so it only sees a change after
  `gh release create` — a push alone deploys nothing. `addons_dir` may be stored
  in either the WSL (`/mnt/c/...`) or native-Windows (`C:\…`) form; ghaddons
  translates to whichever side it's running on. Full recipe + per-addon release
  checklists: `addon-manager/README.md` and each addon repo's `CLAUDE.md`.
- `tools/` — uv project, `wowkb` package
- `raw/` — gitignored fetch cache; distill into `knowledge/`, don't cite raw/

### Side projects / prototypes (standalone apps — NOT the KB)

These are self-contained companion apps living beside the KB. They have their
own build stacks and don't follow the `knowledge/**.md` front-matter convention.
Each has a design doc with a progress/milestone log — **read the doc before
touching the code**. Status as of 2026-07-09:

- `projects/trainer/` — **rotation trainer** (Flutter/Dart). A target-dummy rotation-
  practice game; one spec so far (simplified Affliction Warlock). Two packages:
  `sim/` (headless pure-Dart engine — GCD, DoTs/pandemic, shards, RNG,
  `advisePriority()`, `SessionStats` + a fixed-length pull lifecycle; 71 tests)
  and `app/` (Flutter UI, `path:`-depends on `sim/`; hint glow + end-of-pull
  summary). Spec + milestone log: `todo/rotation-trainer.md`. **M1–M4 done;
  M5 (Affliction fidelity: real icons, tuned numbers/weights, Nightfall
  proc-glow, Drain Soul + Darkglare) is next.**
- `projects/talent-calculator/` — **talent calculator** (`wow-talent-calculator`; Svelte + Vite, `bun`).
  Data-driven from a `build-data` script. Spec: `todo/talent-calculator-prototype.md`.
- `projects/mplus_memory/` — **M+ Memory Trainer**: a spaced-repetition trainer
  for Midnight S1 Mythic+ dungeon mechanics. Has its own `project-spec.md` +
  `backlog.md` and its own inner `app/` (`mplus-memory-trainer`, Svelte/Vite/bun).
  Note: its data pipeline writes into the KB proper
  (`knowledge/systems/mechanic-archetypes.md` + per-dungeon files).
- `projects/keybinder/` — **BucketBinds**: a one-shot keybind/action-bar dumper
  addon. Sorts every ability of your class+spec into fixed **bucket → action-slot**
  categories and sets the keybinds in one go, so the same category sits on the same
  key across all 40 specs; plus transactional snapshot/restore of your whole
  keybind+bar+macro state. Concept from Bellular's Midnight keybind sheet, extracted
  into `data/bellular-keybinds.seed.json` (**CANONICAL, hand-edited**) →
  `tool/gen_data_lua.py` → `addon/BucketBinds/Data.lua` (**generated — never
  hand-edit**). Docs: `project-spec.md` (design + milestones + the
  layout-of-record), `data/layout-v2-proposal.md` (banding contract; §6 per-spec
  re-filing SHIPPED via the floats rollout), `data/seed-review.md` +
  `seed-edits-proposed.md` + `unmapped-abilities.md` (per-spec audits). The addon
  (`michac/BucketBinds`) is at `addon/` — own git repo, **gitignored**, own
  `CLAUDE.md` for the release workflow. **Floating buckets shipped across all 33
  DPS/tank specs (2026-07-21)** — the 7 healers stay held per layout-v2
  §10. In-game verification: Demonology pilot verified; the other 32
  DPS/tank specs' float placement is the outstanding in-game pass. Read off disk
  by `wowkb.diagnostics`. (Current addon version: `wowkb.addon list`.)
- `projects/cooldown-hud/` — **Cooldown HUD**: a spec-specific overlay that skins
  Blizzard's built-in **Cooldown Manager** (Midnight 12.0), CRT/green-phosphor
  aesthetic; v1 target **Demonology Warlock**. Docs live in `docs/` (`spec.md`
  vision · `guidance-model.md` §0.5 rotation-helper contract · `notes.md` technical
  findings · `milestones.md` roadmap+status) — see its `CLAUDE.md`. The addon
  (`michac/CDMProbe`) is at `addon/` (own git repo, gitignored, own `CLAUDE.md` for
  the release workflow). **M0.5 + M1 + M2 + M2.5 + M3a + M3b + M3c-a done** (M2 was
  a decision-only scope collapse — bind to the *live* CDM layout, don't ship/move one;
  M0.5 shipped the §0.5 guidance model; M2.5 committed the v1 indicator set as
  §0.5.8 — those three docs-only. M3a shipped the identity layer, M3b readiness +
  procs, **M3c-a the dot score** — a per-ability actionability dot + a row saying
  *why*, plus the napkin anticipation engine pulled forward from M4;
  **in-game pass outstanding** and it's the real test: strictness
  (expect 1–2 lit dots, not 4–5) and whether cast spellIDs read non-secret **in a
  raid**, which is what the anticipation feature rides on). Next is the rest of M3c
  (shard rail + mode chrome + pre-pull opener queue). (Current addon version:
  `wowkb.addon list`.)
- `todo/` — design docs / specs with milestone logs for the above
  (`rotation-trainer.md`, `talent-calculator-prototype.md`). The informal
  "what's unfinished" inventory, but not exhaustive (mplus_memory's spec lives
  in its own folder).

### Front-matter convention (every knowledge/**.md)

```yaml
---
title: Midnight Season 1 Mythic+ Overview
patch: 12.0.5            # game version the content describes
fetched: 2026-06-03      # when the content was last sourced / changed
reviewed: 2026-07-07     # when the claims were last verified-still-true (a sweep stamps this even if nothing changed)
sources:
  - https://...
confidence: high          # high | medium | low
---
```

`reviewed:` ≥ `fetched:` always. A file can be `patch: 12.0.7` (current game
version) yet `reviewed:` weeks old — meaning it *looks* current but hasn't been
re-checked. `grep -rL 'reviewed: <sweep-date>' knowledge --include='*.md'` after
a sweep = every file the sweep did **not** cover (audit + resume list). This is
how we avoid another silent "16 files left behind."

**`verbatim: true`** marks an *unedited external capture* (e.g. a maxroll guide
via `wowkb.maxroll --kb`) rather than a curated/distilled claim. The doctrine:
**distill on read, not on insert** — distilling both when writing *and* when
answering garbles the content, so these land whole (with `source:` +
`confidence: medium` since we didn't re-verify) and get condensed only at query
time. Grep them apart from curated files with `grep -rl 'verbatim: true'`.

## Tools (run from `tools/`, needs `.env` at repo root — see `.env.example`)

```bash
uv run python -m wowkb.youtube transcript <url>      # → raw/youtube/<id>.md
uv run python -m wowkb.youtube channel <url> --limit 10
uv run python -m wowkb.blizzard token-price          # also: item/spell/journal-*/realms/get
uv run python -m wowkb.wcl rankings <encounter-id> --class Warlock --spec Affliction
uv run python -m wowkb.wcl casts <report-code> --fight <id>
uv run python -m wowkb.wago <Db2Table> [--build 12.0.5.xxxxx]   # → raw/wago/
uv run python -m wowkb.fetch <url>                   # → raw/pages/
uv run python -m wowkb.maxroll <url> [--kb]          # maxroll.gg guide → markdown (--kb: verbatim into knowledge/classes/<class>/<spec>/maxroll-<type>.md; else raw/maxroll/)
uv run python -m wowkb.simc <class> <spec> [--variant Name] [--list] [--no-sha]  # simc MID1 default APL (Tier 1) → raw/simc/<file>.simc + .digest.md (talents hash + grouped actions.*, pinned to a commit SHA+date). The reproducible source the rotation.md files distill.
uv run python -m wowkb.character <name> [--realm kiljaeden] [--json]  # full char digest (unions all 3 sources; carries a "This reset" section)
uv run python -m wowkb.plan --minutes 60 [--mood efficiency|fun] [--include-repeatables]  # ranked session shortlist
uv run python -m wowkb.plan --gear --character <name>  # per-slot gearing chart (cache/crest targets + accolade heuristic)
uv run python -m wowkb.gen_addon_quests              # regen addon quest-ID table from repeatables.json (then cut an addon release)
uv run python -m wowkb.gen_candidates                # regen planning/candidates.json from activities/*.md (--check in CI; edit the .md, not the JSON)
uv run python -m wowkb.gen_verify                    # regen _meta/verify-in-game.md from @verify-ingame markers (--check for CI; tag the claim, not the JSON)
uv run python -m wowkb.spec_inventory [--spec X] [--unseeded] [--json PATH] [--validate CHAR]  # per-spec ability inventory as a UNION: all-talents.tsv (node_type!=PASSIVE) ∪ SkillLineAbility class kit ∪ CooldownSetSpell residue (cdm-only), annotated with cooldown, Blizz category, origin (class-baseline|talent-active|talent-choice|cdm-only), suggestedMode (fixed|float), talent tree/hero placement, and the seed bucket that binds each name. Tier 1, all 40 specs. `--validate <char>` diffs the union against a real in-game `/bb diagnostics` dump (false-negatives = holes). Feeds the BucketBinds floats work (layout-v2 §6).
uv run python -m wowkb.addon list                       # the 3 sub-repo addons: presence + local HEAD + .toc version + latest release + drift
uv run python -m wowkb.addon pull [--all|bb cdmp ps]     # clone-if-missing + git pull each sub-repo (the machine-B sync)
uv run python -m wowkb.addon check                       # report addons with local-only (uncommitted/unpushed) work; exit 1 if any (pre-push gate)
uv run python -m wowkb.addon release <bb|cdmp|ps> [--patch|--minor|--major] [--notes …]  # bump .toc → luaparser check → commit → push → gh release (tag=version) → ghaddons deploy
uv run python -m wowkb.addon deploy <bb|cdmp|ps>         # redeploy the latest existing release via ghaddons (no new cut)
```

Blizzard + WCL commands require credentials in `.env` (user-registered).

**`wowkb.addon`** is the one door for the three gitignored **sub-repo addons**
(`bb` = BucketBinds · `cdmp` = CDMProbe · `ps` = PlannerState — short name =
in-game slash prefix; a checkout path also resolves). The registry inside the
module (repo ↔ path ↔ `.toc`) is the source of truth for the addon set, and it
owns the mechanical release recipe the per-addon `CLAUDE.md` files used to spell
out by hand (they keep the *why*; this owns the *how*).
- **`list` is the live version signal — never hardcode an addon's current version
  in prose, run it.** It shows presence + local HEAD + `.toc` version + latest
  GitHub release + drift (unreleased commits / behind-release / dirty tree).
- **`pull` closes the machine-B gap.** These are separate repos gitignored here,
  so a `git pull` of *this* repo never fetches them — a fresh machine gets new
  docs describing addon code it doesn't have. **On a fresh checkout / before
  touching an addon, run `wowkb.addon pull --all`** (clone-if-missing + `git pull`
  each). Since this file loads every session, that's the standing reminder.
- **`check` is the pre-push gate** (see the Git-workflow note): reports any addon
  with local-only work (uncommitted or unpushed), exits 1 if so. Run it when you
  push this repo — pushing here means I want the addon code on GitHub too.
- **`release`** runs the whole publish flow one-shot: refuses a dirty tree (commit
  your feature work first), bumps the `.toc` version (`--patch` default), warns if
  `## Interface:` drifts from `game-version.md`, luaparser-checks the Lua, commits
  the bump, pushes, cuts a GitHub release whose **tag = `.toc` version**, then
  `ghaddons`-deploys into the game install and reads back `ok`. For `ps` it also
  warns to bump the Lua `schema` field by hand if the `/ps` dump format changed
  (it does **not** touch schema). `--dry-run` stops before the commit.

**`wowkb.character`** is the one-shot snapshot for `knowledge/characters/`:
it pulls every Blizzard profile endpoint (summary/equipment/specs/professions/
reputations/raids/keystone+season) AND currencies — the profile API does *not*
expose currencies, so it reads them from the **Syndicator** addon's
SavedVariables on disk (`…/_retail_/WTF/Account/*/SavedVariables/Syndicator.lua`)
and resolves IDs via wago `CurrencyTypes`. Requires the WoW install reachable
(default `--wow-path` is the WSL `/mnt/c` path) and the character to have been
logged in / `/reload`ed recently. Emits **data only** — add narrative/deltas by
hand when writing the KB file. Note: **Catalyst charges = Dawnlight Manaflux**
(currency 3378 — a normal currency). **Sparks of Radiance** (232875) and **Ascendant
Voidshards** (268650) are *items* — read from **Syndicator**'s full bag+bank+warband
inventory (the same file we read for currencies), surfaced as `state["item_counts"]`
and a digest "Crafting mats" line. (So they're **not** a gap; the old "check in-game"
note was wrong. `wowkb.character --skip-if-current` short-circuits the whole pull when
the snapshot's `fetched:` is already ≥ the dump's capture date.)

**Three sources, one loader.** `wowkb.charstate.load` is the single door that
unions all character data: the **PlannerState `/ps` dump** (reset-state the API
can't see — weeklies done/not, vault progress, world-boss kills, active events —
plus an equipment/currency mirror; the **offline spine**), the **Blizzard API**
(names/specs/professions/renown/raids), and **Syndicator** (gold + currencies).
Both `wowkb.character` and `wowkb.plan` consume it; enrichment degrades silently
when offline (`--no-enrich` forces dump-only). So `wowkb.character` now also
carries a **"This reset"** section. The profile API doesn't reliably expose the
numeric upgrade track (and **drops it entirely on crafted gear**), so the **addon
dump is the primary track source** (PlannerState schema≥8 reads `track`/step off the
item tooltip; API is fallback). `wowkb.character` shows a **Track column** + a
**"…of the Dawn" discount** section (which sub-263 slots gate the 50% Champion
discount, and whether each is crestable or a crafted slot needing a recraft).
⚠ Track-aware *scoring* in `wowkb.plan` (crest-consumer costing) is still a
follow-up — the ranker's `track_caps` remains ilvl-based for now (see `_meta/kb-inbox.md`).

**Routing rule — don't reinvent the planner from the KB.** For any "how do I
gear up / progress <char>" question, run the tools FIRST (they already union the
three sources) rather than re-deriving a per-slot chart by hand:
`wowkb.plan --gear --character <name>` (gearing chart + accolade heuristic),
`wowkb.plan --character <name>` (ranked session), `wowkb.character <name>`
(snapshot + reset-state). The **`/plan-character`** command wraps this flow.
Add warband/cross-character moves + KB colour on top; don't recompute the slots.

⚠ git-bash mangles leading-slash args (`/data/...` →
`C:/Program Files/Git/data/...`). Prefix `wowkb.blizzard get` calls with
`MSYS_NO_PATHCONV=1`.

## Workflow: the KB grows through use

1. **Answer from `knowledge/`** when fresh (`patch` == live, decent confidence).
2. **If missing or stale**: fetch with the tools (tier-highest source first),
   distill, and **write back** to the right `knowledge/` file with full front
   matter and resolved TODOs.
3. Stubs with `## TODO` sections name their intended sources — follow them.
4. Keep `raw/` as scratch; the curated claim + citation goes in `knowledge/`.

## Keeping the KB current: the `/update` command

`/update` is the **one door** for patch/hotfix maintenance. It reads
`_meta/feed-watermark.md`, detects what's shipped since (wago build feed +
Blizzard blue-post tracker JSON), and offers the right amount of work:

- **Quick apply** — hotfixes / tuning / small content. Archives blue posts
  verbatim to `patch-notes/<patch>.md`, applies verified content edits to the
  files the posts name, refreshes `moving-values.md`, advances the watermark.
- **Full apply** — a real content patch (minor version bump / new zone-raid-
  system). Everything quick does, plus verbatim note capture, a change ledger,
  a **full-tree** re-verify via the `kb-patch-sweep` workflow (RESTAMPs files no
  post mentioned — the only thing that catches silent drift), NEW files, and a
  `game-version.md` bump. It's authorized to spawn subagents, author a Workflow,
  and research sparse notes via web + `wowkb.youtube` transcripts.

**Provenance precedence (the immune system):** authoritative Tier-1 feed data —
blue posts, the `patch-notes/` archive, `moving-values.md` — is the **floor**.
Lower-tier sources (Icy Veins / Wowhead editorial) may corroborate or add but
must **never overwrite** it; on conflict, keep the Tier-1 value and flag. Resolve
name/number conflicts via game data (wago DB2 / Wowhead DB page), not prose.

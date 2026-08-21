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
gitignored sub-repos — `planner-state/`,
`projects/keybinder/addon/`, `projects/combat-assist/addon/` — where
"a push does not reach the game, you must cut a release" is a real deploy fact
worth saying when a deploy is in play.)

**Pushing this repo ⇒ push the addons too.** If you push **this** repo to
GitHub, assume I also want the latest addon code on GitHub for all four sub-repos
(they're separate repos a wow-repo push does not touch). So when you push here,
run `wowkb.addon check` and, for any addon it flags with **unpushed** commits,
`git -C <path> push` it as well; if it flags **uncommitted** changes, surface
that to me first. (`check` is read-only and exits non-zero when anything is
local-only — a clean pre-push gate.) Cutting a release is a separate step — ask-first for
`bb` and `ps`, pre-authorized for `cap` (`projects/combat-assist/CLAUDE.md` § Releasing) —
this is just "don't leave addon commits stranded on one machine."

## Current game state

- **Live: patch 12.1 "Curse of Ula'tek"** — Midnight expansion, level cap **90**,
  build `12.1.0.69214`, live 2026-08-11. **Season 1 has ended**; Season 2 opens
  **2026-08-18**, so the week of 2026-08-11 is pre-season. No PTR currently.
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
7. **When you correct the KB, rewrite the claim — never append a correction
   under it.** A stale number left standing with a ⚠ note below it is a trap:
   the next reader greps that line, or stops reading before the note, and gets
   the wrong answer. Delete the old value; put one line in the file's
   `## Changelog` if the error is worth remembering. Full doctrine (and the
   `wowkb.kblint` gates that enforce it):
   **`knowledge/_meta/writing-claims.md`**.

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
- `tools/` — uv project, `wowkb` package. **`tools/README.md` is the full command
  reference** (flags, subcommands, rationale); `tools/docs/` holds deeper per-tool docs
  (e.g. `wowkb-sim.md`, the sim harness design doc + field log)
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
- `projects/cooldown-hud/` — **Cooldown HUD** (CDMProbe): 🗄 **ARCHIVED 2026-08-30.** Superseded
  by Combat Assist Plus on 2026-08-05 and closed out on 2026-08-30: the GitHub repo
  (`michac/CDMProbe`) is **archived read-only**, `cdmp` is **out of `wowkb.addon`'s registry**, and
  the `wowkb.cdmp` graders are **deleted** (recoverable from git). Nothing here is worked on,
  released or deployed. **There is one addon riding the CDM and it is `cap`.**
  ⚠ **The directory is KEPT, and two things in it are still worth reading** — its **measured
  client facts**, which already live in `knowledge/addon-dev/` where the KB's gates apply (that
  is the authority, never these docs), and its **per-spec rotation research** (`specs/demonology/`
  especially), which cap drew on by hand. Its *code* is not ported and its `docs/status.md` is a
  closed worklist. **Do NOT route new work here**, and read anything present-tense in it as
  history. The checkout stays at `addon/` (own git repo, gitignored); build history in
  `docs/archive/`; captures still readable via `wowkb.capture cdmp`.
- `projects/combat-assist/` — **Combat Assist Plus** (`/cap`): **the live CDM addon**, a
  combat-assistance overlay that makes the Cooldown Manager tell you more **without
  telling you what to press**. It is the reason the Cooldown HUD above is superseded.
  v1 spec: **Demonology Warlock**; a spec without a catalog gets nothing, by design.
  **Start at its `CLAUDE.md`** (project root), which owns the doc map; `specs/spec.md` is
  the definition and §1's two principles are what everything else is downstream of.
  ⚠ **What is built and what has flown lives in `specs/backlog.md` → `## Status`** and is
  deliberately not restated here or anywhere else. ⚠ **cap's releases do NOT need asking**
  (2026-08-31) — its `CLAUDE.md` § Releasing carries the standing authorization and the three
  gates that make it cheap; the old blanket ask-first rule here is retired. The addon
  (`michac/cap`) is at `addon/` — own git repo, **gitignored**, own `CLAUDE.md` for the
  release workflow. (Current addon version: `wowkb.addon list`.)
- `projects/addon-lab/` — **ClientLab**: the scratch lab addon that answers
  `knowledge/addon-dev/` questions by running Lua in the live client, plus
  **`questions.json`, the test registry** (four statuses:
  `answered`/`built`/`parked`/`not-answerable`). Deliberately **not** a product: no repo,
  no releases, not in `wowkb.addon`; deploy is a directory copy. **An unknown is recorded
  as a marker on the claim, not in a tool** — `[gap]`/`@verify-ingame` → `@pending-test:
  <id>` once a test exists → `[client YYYY-MM-DD]` once drained. A marked claim you are
  about to build on is a **STOP: ask**. Nothing ages an open marker. The process is
  `docs/lab-process.md`; the addon rules are its `CLAUDE.md`.
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

**`tools/README.md` is the full reference** — every command's flags, subcommands, and
the hard-won rationale/gotchas behind each. Run `<cmd> --help` for exact flags. This
section is the **index + the doctrine that must stay in context**; when in doubt about a
command, open `tools/README.md`.

```bash
# Research & fetch
uv run python -m wowkb.youtube transcript|channel <url>   # YouTube → raw/youtube/
uv run python -m wowkb.blizzard token-price|get <path>    # Blizzard Game Data / profile API
uv run python -m wowkb.wcl rankings|casts …               # Warcraft Logs
uv run python -m wowkb.wago <Db2Table> [--build …]        # wago.tools DB2 → raw/wago/
uv run python -m wowkb.fetch <url>                        # page → raw/pages/
uv run python -m wowkb.maxroll <url> [--kb]               # maxroll guide → markdown
# APLs (Tier 1, from the simc checkout)
uv run python -m wowkb.simc <class> <spec> [--variant|--module|--list]  # upstream default APL → raw/simc/ (REFUSES a stale profile)
uv run python -m wowkb.simc --kb [--all|<class> [<spec>]] [--check]      # the KB door: writes knowledge/…/simc-apl.md (--check = CI drift gate)
# Sim harness  — doctrine below; full reference in tools/README.md + tools/docs/wowkb-sim.md
uv run python -m wowkb.sim import|check|compare|gear|crests|log …        # local SimulationCraft harness (import --from-api builds from the Blizzard API)
# Character & planner
uv run python -m wowkb.character <name> [--realm …] [--json]            # full char digest (unions all 3 sources; "This reset" section)
uv run python -m wowkb.plan [--minutes N | --gear --character <name>]   # ranked session shortlist / per-slot gearing chart
# KB generation & maintenance
uv run python -m wowkb.gen_addon_quests | gen_candidates | gen_verify   # regen generated artifacts (edit the source .md/.json, not the output; --check in CI)
uv run python -m wowkb.kbpass current|allocate|check                    # pass identity for /update runs (check = did a claimed regen actually happen)
uv run python -m wowkb.spec_inventory [--spec X] [--validate CHAR]      # per-spec ability inventory, all 40 specs (feeds BucketBinds floats)
uv run python -m wowkb.kblint [--gate N] [--all]                        # the 6 KB gates (exit 1 on any hit)
uv run python -m wowkb.citecheck [--lines] [--verbose]                  # do the Tier-1 `[T1 src …]` citations still resolve? symbol-anchored fails hard; line-anchored counted, not failed
# Addon-dev & art
uv run python -m wowkb.uiart find|atlas|icon|manifest                   # Blizzard UI art → image files (+ tintability measure)
uv run python -m wowkb.capart tokens|assets|import|build|export|check   # combat-assist previews + the addon's Style.lua/art (numbers live in specs/render-tokens.json, not here)
uv run python -m wowkb.serve <dir> [--watch PATH] [--on-change CMD]     # stdlib static server + mtime watcher + live reload
# Addons & captures
uv run python -m wowkb.addon list|pull|check|release|deploy <bb|ps|cap>  # the one door for the 3 sub-repo addons
uv run python -m wowkb.capture <bb|cap|cdmp|clab|ps> [stream]           # THE ONE READER for addon captures
uv run python -m wowkb.lab deploy|show|drain|blocked                    # the ClientLab addon-dev lab
uv run python -m wowkb.obs list|check|drain OBS-nnn                     # the addon-dev observations queue + drain
```

Blizzard + WCL commands require credentials in `.env` (user-registered). ⚠ git-bash
mangles leading-slash args (`/data/...` → `C:/Program Files/Git/data/...`) — prefix
`wowkb.blizzard get` calls with `MSYS_NO_PATHCONV=1`.

**Doctrine that must stay in context (the rest of each command's docs is in `tools/README.md`):**

- **`wowkb.sim` — the local SimulationCraft harness.** A sim result is **evidence for an
  answer, not a sourced claim**; it never belongs in `knowledge/**`. The APL always comes
  from upstream unmodified (never simc's built-in list); the **FIRING GATE** — an equipped
  or swapped-in on-use effect that never fires is invisible in simc's own output — is the
  reason the tool exists. `check` reports **no DPS** on purpose; `compare` deltas only
  **within one invocation**. ⚠ **LIVING COMMAND** — when a session gives a wrong answer the
  fix is a new GATE, never a hand-edited profile or APL. **Read `tools/docs/wowkb-sim.md`'s
  Field log before designing a comparison, and append to it after.**
- **`wowkb.capture` is the one door for getting data out of an addon** — every recorder in
  every addon writes `<AddonDB>.captures.<stream>` and this is the only thing that reads it,
  which is the enforcement. Contract + the Lua-side `Capture.lua`/`DumpPanel.lua`:
  `.claude/skills/wow-developer/references/capture-and-dump-standard.md`. ⚠ SavedVariables
  only flush on `/reload` or logout.
- **`wowkb.addon` is the one door for the three gitignored sub-repos** (`bb` = BucketBinds ·
  `ps` = PlannerState · `cap` = Combat Assist Plus; short name = slash prefix; CDMProbe left
  the registry when it was archived, though `wowkb.capture cdmp` still reads its captures). `list` is the **live version signal — never hardcode an addon's version, run it.**
  The addons are gitignored and cloned **independently per worktree**, so **run
  `wowkb.addon pull` on a fresh checkout / in any worktree you have not released from lately,
  before touching or releasing an addon** (`list`'s `drift` column flags a stale one as
  `BEHIND release — pull`). `check` is the pre-push gate (local-only work → exit 1); pushing
  **this** repo means the addon code should go to GitHub too. Cutting a release is ask-first
  for `bb` and `ps` and **pre-authorized for `cap`** (`projects/combat-assist/CLAUDE.md`
  § Releasing).
- **Routing — don't reinvent the planner from the KB.** For any "how do I gear up / progress
  <char>" question, run the tools FIRST — `wowkb.plan --gear --character <name>`,
  `wowkb.plan --character <name>`, `wowkb.character <name>` (the **`/plan-character`** command
  wraps this) — rather than re-deriving a per-slot chart by hand. **Three sources, one
  loader:** `wowkb.charstate.load` unions the PlannerState `/ps` dump (reset-state the API
  can't see + the **primary upgrade-track source**), the Blizzard API, and Syndicator
  (gold + currencies).
- **Reading a character's talents — use the profile API, not the loadout string.**
  `wowkb.blizzard get /profile/wow/character/<realm>/<name>/specializations --namespace profile`
  returns every loadout with resolved names, its `talent_loadout_code`, and an `is_active`
  flag — no need to decode the export string.

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

⚠ **This governs a SOURCE CONFLICT — two live sources disagreeing now.** It does
**not** govern a **temporal correction**, where we were simply wrong and now know
better. There is no disagreement to preserve there: **delete the old claim and
write the new one** (staleness doctrine 7). Reading "keep it and flag" as
"never delete anything" is exactly how a KB file grows a stack of ⚠ notes with
the dead value still sitting at the top.

---
title: Session Planner — System Overview & Resume Runbook
patch: 12.0.7
fetched: 2026-07-02
reviewed: 2026-07-07
sources:
  - knowledge/planning/scoring-model.md
  - addon-manager/README.md
  - https://github.com/michac/wow-planner-state
confidence: high
---

# Session Planner — start here

> **If you're a fresh Claude session (or a human on a new machine): this is the
> hub.** It explains what the planner is, how the pieces connect, what's built
> vs. next, and how to stand it up on another computer. Conversation history and
> per-machine agent memory do **not** travel between machines — the repo does.
> Everything you need to resume is here or linked from here.

## The larger process (why this exists)

Decomposing high-level WoW goals into an action system. Four goals:

1. **Be time-efficient** — progress per minute, not puttering.
2. **Have fun** — don't let efficiency crowd out rare/limited events.
3. **Narrow ~100 possible tasks → a few** via explicit heuristics.
4. **Improve tooling** — near-term: gather + critique combat parses.

Insight: **goals 1–3 are one engine.** Efficiency is the reward axis, fun is the
counterweight (urgency/novelty), heuristics are the scoring function that
combines them and cuts the list. The deliverable is a **session planner**:
given (character state, calendar, time budget, mood) → a ranked shortlist with a
one-line "why" each. **Goal 4 (parses) is a separate, not-yet-built track.**

Default stance: **efficiency-first** (fun surfaces via the urgency term + a small
collectible floor; it never outranks real power). Full rationale in
[scoring-model.md](scoring-model.md).

## Architecture

```
PlannerState addon  ──dump──▶  PlannerState.lua   ──read──▶  wowkb.plan  ──rank──▶  shortlist
(in-game, own repo)  (/ps)      (SavedVariables)   (Lua parse)  (scoring-model.md)
```

The planner **subtracts what you've already done this reset** (the "Gate" step).
Some of that state is in the Blizzard profile API (M+ runs, renown); the rest —
delve/prey journeys, Great Vault slots, per-currency weekly-earned — is **not**,
so the `PlannerState` addon dumps it to disk and the planner reads it, the same
pattern `wowkb.character` uses for Syndicator currencies.

## Component map

| Piece | Location | Repo |
|---|---|---|
| Scoring contract | `knowledge/planning/scoring-model.md` | michac/wow |
| Activity catalog | `knowledge/planning/activities/*.md` (`_facets.md` = tag contract) | michac/wow |
| Ranker input (generated) | `knowledge/planning/candidates.json` ← `wowkb.gen_candidates` | michac/wow |
| Planner tool | `tools/wowkb/plan.py` (`uv run python -m wowkb.plan`) | michac/wow |
| Addon manager (ghaddons) | `addon-manager/` (+ its README) | michac/wow |
| **PlannerState addon** | installed into `Interface/AddOns/` | **michac/wow-planner-state** (its own git root; gitignored here) |

## Status & roadmap

**Built + tested (2026-07-02):**
- Planner v1: Lua-dump parser, gating (done/todo/unknown), scoring, greedy
  time-budget walk, `--mood efficiency|fun` dial.
- ghaddons: resolves GitHub releases, installs/updates/removes; verified against
  a real release install.
- PlannerState addon: dumps vault/M+/lockouts/currencies/quests/items.
- **Scoring v2a — breakpoint proximity** (`plan.py:breakpoint_R()`): boosts R→4 for
  the M+ run that crosses a Great Vault threshold (1/4/8) and zeroes it once capped,
  reading live progress from the dump. Verified offline via
  `tools/tests/check_breakpoint.py` against `tools/tests/fixtures/vault-*.lua`.

**Built + tested (2026-07-06, addon v0.4.1):**
- **Per-slot equipment** in the dump (`equipment[]`, schema 4) — `plan.py` prints a
  weakest-slots line. Cached in-world so the logout write no longer records
  `equippedIlvl=0`. Verified live: `back 250, trinket2 259, waist 259`.
- **Auto-wired weekly-quest IDs.** `wowkb.gen_addon_quests` generates the addon's
  `PlannerState_Quests.lua` (`ns.GENERATED_QUESTS`) from the scraper's high-confidence
  questIDs, merged *under* the hand-verified slug map. Re-run after `wowkb.repeatables`.
- **Repeatables in the ranker.** `plan.py --include-repeatables` folds the scraper
  catalog in (deduped against curated prey/void); rows marked `~` = placeholder T/E.
- **`vault_track` gate + `delve-tier11` re-model.** Delve/world weekly motive resolves
  off Great Vault column progress in the dump — killed one unverifiable slug.
- **Objective progress** (schema 5): weeklies dump `have/need`; the plan shows `at 1/3`
  (prey etc.) alongside done/todo.

**Next — see [`roadmap.md`](roadmap.md) for the durable, detailed version.**
The plumbing is done; what's parked (2026-07-06, awaiting user sign-off because these
are scoring-knob calls) is **scoring quality**:
- **A. Formula rebalance** — cheap chores currently outrank power (Trading Post 5.0 >
  M+ 3.0); proposal `sqrt(T)` + floored-R cap flips it (M+ → 4.24).
- **B. Slot-targeting v2b** — make the printed weak slot (`back 250`) actually boost the
  spark/catalyst that can fill it.
- **C. De-noise repeatables** — real per-type T/E + overlap dedup.

Plus **coverage**: three weekly slugs still need in-game resolution
(`delve_weekly_cache` key-cap check, `dungeon_weekly` / `liadrin_spark` quest IDs) —
scoreboard in `roadmap.md`. And the untouched **parse-critique track** (goal 4;
reconcile `encomplete-plan.md` from Affliction → **Demonology** first).

## Resume on another machine (runbook)

The repo carries everything except your credentials. On the gaming machine:

**Prereqs:** `git`, `gh` (logged in), `uv`, and the WoW install. For the ghaddons
GUI only: `python3-tk`.

```bash
# 1. Clone the workspace
git clone https://github.com/michac/wow && cd wow

# 2. Recreate credentials (NOT in the repo — gitignored)
cp .env.example .env       # then fill BLIZZARD_* and WCL_* from your dev.battle.net / WCL clients

# 3. Point paths at THIS machine's WoW install.
#    Defaults assume the WSL path: /mnt/c/Program Files (x86)/World of Warcraft/_retail_
#    Change if the gaming machine differs (native Windows / Mac / different drive):
#      - addon-manager/config.json   -> "addons_dir"
#      - wowkb.plan / wowkb.character -> --wow-path flag (or edit DEFAULT_WOW / DEFAULT_ADDONS_DIR)

# 4. Install the PlannerState addon via ghaddons
cd addon-manager
cp config.example.json config.json          # edit addons_dir to your AddOns folder
python3 -m ghaddons.cli add michac/wow-planner-state
python3 -m ghaddons.cli install --all
# (GUI alternative: sudo apt install python3-tk; python3 -m ghaddons.gui)

# 5. In-game: log in on the character, then  /ps  and  /reload  (writes the dump)

# 6. Run the planner
cd ../tools
uv run python -m wowkb.plan --minutes 60
```

**Gotchas:**
- **WoW path is per-machine** — the single most likely thing to need changing.
- `.env` is gitignored; without it, `wowkb.blizzard/wcl/character` can't call the
  APIs (the planner still runs; it just can't fetch live profile data).
- Editing quest IDs: clone `michac/wow-planner-state`, edit `ns.WEEKLY_QUESTS`,
  commit/push, then `ghaddons update` — editing the installed copy directly gets
  overwritten on the next update.
- git-bash mangles leading-slash args; prefix `wowkb.blizzard get` with
  `MSYS_NO_PATHCONV=1` (see CLAUDE.md).
- To pick this thread back up with Claude on the new machine, point it at this
  file: *"read knowledge/planning/README.md and let's continue the planner."*

---
title: How Quests Work + How to Fetch Quest Data
patch: 12.0.7
fetched: 2026-07-06
sources:
  - https://us.api.blizzard.com/data/wow/quest/92013   # Blizzard Game Data API
  - https://www.wowhead.com/quest=92013/wanted-dionaeas-thorntusks
  - https://nether.wowhead.com/tooltip/quest/92013
  - https://wago.tools/db2/QuestV2/csv
  - "FollowTheArrow addon v0.7.0 (local Lua)"
confidence: high
---

# How Quests Work + How to Fetch Quest Data

Agent-facing methodology doc. Read before answering "why can't I get quest X?"
or trusting a single number off a quest page. Companion to `sources.md` (trust
tiers) and `game-version.md` (live state).

## 1. "Level" vs "Requires level" — two different fields

Two distinct level numbers exist; conflating them is the classic mistake:

- **Level** (quest level / con level) — the quest's **tuning level**. Drives XP
  scaling and log color. Says nothing about who can *accept* it.
- **Requires level** = the API's **`min_character_level`** — the **minimum
  player level to accept**. The real level accept-gate.

They're often equal for endgame quests (both 88), which hides the distinction.
Neither one tells you whether the quest is currently **obtainable** — see §2.

## 2. Availability is gated by more than level

A quest you meet the level for can still be un-obtainable:

- **Prerequisite quests** — a `PrevQuest` / questline done first (`QuestLine` /
  `QuestLineXQuest` DB2 give chain + order).
- **Campaign progress** — repeatables often unlock only after a story chain.
  Can be **warband/account-wide** (once on any character) **or per-character** —
  always distinguish and say which; flag it if unsure.
- **Renown / reputation** thresholds.
- **Phasing / world state / weekly rotation** — daily/weekly quests offer a
  *random* subset; "none available" may be the roll, not a lock.

### Case study — the Harandar "WANTED" board (level is a red herring)

Quest 92013 shows `min_character_level: 88`, so "you're too low" is tempting.
But a Wowhead comment from a **level-90** player who "completed Harandar" reports
it **still unavailable** — proving an independent gate: these are the tail of
the **Trials of the Shul'ka** chain, *"locked behind main campaign progress"*
(Follow the Arrow's own note), plus a random daily roll. Verify obtainability
*separately* from level; comments are often the fastest way to find a hidden
gate. Full write-up: `systems/leveling-notes.md`.

## 3. Where quest data lives — three sources, ranked

**(a) Blizzard Game Data API — authoritative for core fields. USE FIRST.**
There *is* a good direct-from-Blizzard source (don't assume Wowhead is the only
option). `GET /data/wow/quest/{id}` (namespace `static`) returns structured
JSON, non-JS:

```bash
uv run python -m wowkb.blizzard get /data/wow/quest/92013
# → title, description, type, area (+id), rewards.experience, rewards.money,
#   requirements.min_character_level (= the real "Requires level"), max_character_level
```

Enumerate by zone: `GET /data/wow/quest/area/{areaId}` → every quest ID+name in
the area (Harandar `15355` → 195 quests). `GET /data/wow/quest/category/index`
exists but is legacy buckets (Epic, Warlock, Fishing…) — **no Daily/Weekly**.

**API gaps** (this is Wowhead's job): currency/reputation/item rewards (92013's
Coffer Key Shards / Voidlight Marl / Hara'ti rep are absent from the API), the
daily/weekly flag, prerequisite/gating, spawn/drop data, and comments.

**(b) Wowhead — the aggregate/crowd-sourced layer, filling the API's gaps.**
Its edge is data only observable in-game (drop rates, coords), editorial
classification (daily/weekly), gating context, and **comments** (hidden gates) —
largely from Wowhead Client uploads + editors, not a magic Blizzard feed.
**The data is inline in the raw HTML — no Playwright needed for most of it:**

```bash
# Core page: FOLLOW the redirect (-L) to the slug + a browser UA → inline data.
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://www.wowhead.com/quest=92013/wanted-dionaeas-thorntusks" \
  | grep -oE '"reqlevel":[0-9]+|Coffer Key Shard|Voidlight Marl|The Hara.ti'
# Bare /quest=ID 301-redirects; without -L you get 0 bytes (my earlier mistake).

# Basic-only, tiny: tooltip JSON (name + quest level), non-JS.
curl -s https://nether.wowhead.com/tooltip/quest/92013

# Enumeration: listview pages embed  data:[ … ]  as a JS array in the HTML.
curl -sL -A "Mozilla/5.0" "https://www.wowhead.com/quests/min-level:90/max-level:90" \
  | grep -o 'new Listview' -A0    # then extract the data:[...] array
```

**Holdout:** user **comments** load via a separate XHR (`comments=quest.ID`
404s — correct endpoint TBD). Comments are where gate info surfaces, so that one
slice may still need the rendered page until the XHR is identified.

**⚠ Listview cadence filters DON'T segment (verified 2026-07-06).** The path
suffixes `/quests/…/daily` and `/quests/…/weekly` are **silently ignored** — they
return the *same* set as the unfiltered page (`/quests/daily` and `/quests/weekly`
each return the identical popularity-sorted 1000). So you **cannot** classify a
quest's cadence from which filter URL surfaced it. Real cadence signals:
- **Per-quest infobox** `Type: Weekly|Daily` in the `markup.printHtml("[ul]…")`
  block (authoritative, needs the quest page). NB Wowhead types the Shul'ka WANTED
  dailies as `Group`, not `Daily` — combine with the name/recurring signals.
- **Listview `icon`** field: `quest-start-daily` marks a daily; there is **no**
  `quest-start-weekly` (weeklies show `quest-start`); `quest-start-campaign` marks
  one-time story quests.
- **Recurring turn-in icon** (`quest-recurring-*.png`) on the page = repeatable.

**⚠ Listview caps at 1000 rows, popularity-sorted** — the tail (e.g. Void Assault
Eversong `94385`, the WANTED board at quest-level 88) falls off and a level-90-only
filter misses sub-90 repeatables entirely. Backfill with a curated KB seed +
`/data/wow/quest/area/{id}` per-zone cross-check.

**(c) Client DB2 (wago.tools) — near-useless for quest fields; good for
relationships.** `QuestV2` = `ID, UniqueBitFlag, UiQuestDetailsThemeID` only;
level/text/rewards are server-side. Use DB2 only for `QuestLine` /
`QuestLineXQuest` (chain + `OrderIndex`) and non-quest data. Single-row filter
avoids full dumps:

```bash
curl -s 'https://wago.tools/db2/QuestLineXQuest/csv?filter%5BID%5D=<id>'   # header + matches only
uv run python -m wowkb.wago QuestLineXQuest                                # full dump → raw/wago/
```

**Do NOT use:** the legacy Wowhead `&xml` API (`/quest=ID&xml`) — dead, empty.

## 4. Decision tree — "why can't I get / obtain quest X?"

1. **Blizzard API** `/data/wow/quest/{id}` → title, `min_character_level`, XP,
   area. Authoritative basics.
2. **Wowhead page** (curl -L, grep inline) → currency/rep rewards, daily/weekly,
   reqlevel cross-check.
3. **Wowhead comments + addon Lua** (`grep -rniE "unlock|locked behind|account"`)
   → hidden gates (campaign / renown / warband).
4. **DB2 `QuestLine`** → is it mid-chain? what's the prior quest?
5. **In-game** → resolve account-vs-character, current rotation, post-hotfix
   reality.

Answer with **both** the level facts *and* the obtaining gate; flag
warband-vs-character if unverified. Never let a lone "Requires level N" imply
obtainability.

## 5. Tooling — built 2026-07-06

- **`wowkb.blizzard quest <id>`** (+ `quest-area <id>`) — thin wrappers on
  `/data/wow/quest/{id}` and `/data/wow/quest/area/{id}`.
- **`wowkb.quest <id|name>`** — one digest: Blizzard API basics + `curl -sL` the
  Wowhead page (cadence/reqlevel/currency+item reward names) + a reward **value**
  block (R + goal tags via `wowkb.rewards`). Grep-able text or `--json`; degrades
  gracefully if either source is down. Name→id via the Wowhead suggestions
  endpoint (`type==5`). Comments/gating still out of scope (holdout).
- **`wowkb.repeatables`** — re-runnable scraper → `knowledge/planning/
  repeatables.json` (planner candidate-shaped + `by_goal`/`by_currency` reverse
  indexes) and the human `knowledge/endgame/daily-weekly-quests.md`. Wide Wowhead
  listview net + curated KB seed (for the 1000-cap tail) + `/quest/area/{id}`
  cross-check; the quest page confirms repeatability + cadence. Values rewards via
  `wowkb.rewards` — **do not invent a parallel scorer**; it emits the planner's R.
- **`wowkb.rewards`** — the reward model (descriptor + `value_quest`). The first
  reward→value logic in the repo; reused by `wowkb.quest` and `wowkb.repeatables`.

### Deferred follow-up — character-relative reward value

`rewards.value_quest(descriptor, char_state=None)` ships with the `char_state`
branch **implemented + unit-tested** (`tools/tests/check_rewards.py`) but **not yet
wired** to live data — the catalog/doc use the character-agnostic baseline R. To
finish: feed `char_state` from **`wowkb.character`** (per-slot ilvl, renown,
currencies) so gear rewards score by ilvl-delta to your weakest slot and currency
by whether it advances an uncapped track; optionally add a `plan.py
--include-repeatables` flag that merges `repeatables.json` and rescores with
`char_state`. This realizes the planner's designed-but-unimplemented **v2b
slot-targeting** (`planning/scoring-model.md`) using data `wowkb.character` already
exposes.

## 6. Coverage gaps found in practice (12.0.7 world bosses)

Two blind spots surfaced when the 12.0.7 "Revelations" world-boss system
(Val & Naigtal — see `endgame/world-events.md`) slipped past the scraper. Both
are now handled; note them so the pattern is recognized next time.

### (i) Some Midnight zones are AREA-LESS in the Blizzard API

`GET /data/wow/quest/{id}` returns **`area: None`** for the Val/Naigtal
"Showdown" weeklies (96713 / 96717), and Val/Naigtal are **not in
`/data/wow/quest/area/index`** at all — so *both* the harvest's zone attribution
and the `MIDNIGHT_ZONES` cross-check are blind to them (they also sit off the
level-90 popularity listview's 1000-row cap). A Blizzard area is **not**
guaranteed for every zone. Fix: a curated **`QUEST_ZONE_OVERRIDES`** map in
`repeatables.py` (applied as the *last* zone fallback, after category → id2zone →
`area.name`) plus a `KNOWN_REPEATABLES` seed for the quest IDs — the same
belt-and-suspenders pattern the 1000-row cap already needs. Source of the zone
name is the KB (`world-events.md`), not the API.

### (ii) Container/cache rewards hide their currency

The Showdown reward is a **cache item** (Riftstalker's Cache, item 275690), not
inline currency, so a currency-only valuation sees nothing and scores R=0. But
the item API's **`description` literally enumerates the contents** ("Cache
containing Field Accolades, Relic Coffer Key shards, materials for upgrading
gear, gold, and more") — so cache value is *derivable* by description-parsing,
not just hardcodable. Fix: **`rewards.CACHE_RULES` + `classify_cache()`** (same
substring→goal shape as `classify_currency`) with a `KNOWN_CACHES` name-map
fallback; `resolve_item()` detects a container (non-gear item named
cache/coffer, or whose description matches a rule) and attaches a `caches[]` block
to the descriptor that `value_quest` folds in. **The R is a floor** — the gear
roll *inside* the cache is opaque to the API.

### Cadence for these has no structured signal

The Showdown pages carry **no infobox `Type:` and no recurring icon**, so the
`is_repeatable()` / `classify_cadence()` structured checks never fire — only the
**name signals** (`WORLD_BOSSES` / `REPEATABLE_NAME_RE` / the `classify_cadence`
"showdown" branch) classify them, as a **weekly world-boss** lockout. Their
questIDs land in the catalog's "questIDs to wire (verify in-game)" list but are
**not** auto-wired: world-boss quest flags don't always flip on
`IsQuestFlaggedCompleted`, so confirm in-game before adding to
`ns.WEEKLY_QUESTS`. The original-4 rotation bosses (creature lockouts) are done-
tracked separately via PlannerState's `worldBosses[]` block
(`GetSavedWorldBossInfo`, schema 3) + the `world_boss_weekly` gate — because
`GetSavedInstanceInfo` does **not** return world bosses.

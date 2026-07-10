---
title: KB Inbox — free-form parking lot for un-routed todos
patch: 12.0.7
fetched: 2026-07-10
reviewed: 2026-07-10
confidence: high
---

# KB Inbox

A **free-form parking lot**. Drop a todo here the moment it appears, instead of
half-implementing it, or asserting an unvalidated claim into a `knowledge/**` file.
Nothing here is trusted as fact or acted on automatically — it's a holding pen until
someone routes each item to where it belongs.

## What goes here vs. the other queues

This is deliberately the *catch-all*. Use the more specific queue when one fits:

| If the todo is… | Put it in | Not here |
|---|---|---|
| a **claim that needs an in-game check** before we trust it | the in-line verify marker on the claim → harvested into `verify-in-game.md` by `wowkb.gen_verify` | ✗ |
| a **weekly the addon saw but the watchlist doesn't track** | `planning/discovered-weeklies.json` (auto-maintained) | ✗ |
| a **per-reset chore to tick off** | `planning/todo.md` (session checklist) | ✗ |
| a **stub/next-step scoped to one KB doc** | that doc's own `## TODO` section | ✗ |
| **anything else** — tooling ideas, addon features, research-to-do, structural KB work, "look into X" | **here** | ✓ |

## How to use it

- **Add:** append a bullet under the right heading (or make a new heading). One line of
  *what* + one of *why it matters* + any *how/pointer* is plenty. Date it.
- **Route/clear:** when an item is implemented, or promoted into a real KB doc / an
  in-game-verify marker / a tool ticket, **strike it and note where it went** (or delete
  it). This file should shrink as often as it grows.
- **Don't** let items rot silently — a `/update` or sync is a good moment to skim it.

---

## PlannerState addon — backlog

The addon (`planner-state/PlannerState/`) dumps reset state for the planner +
`wowkb.character`. Deploy any of these per `planner-state/CLAUDE.md` (edit lua → bump
`.toc` Version + `schema` → luaparser-check → **cut a GitHub release** → `ghaddons update`
→ in-game `/ps` + `/reload`; a plain push does **not** reach the game).

### ✅ Shipped in v0.6.0 / schema 8 (2026-07-10)
- ~~**Per-slot upgrade track/level**~~ — DONE. `refreshEquip` now reads it off the item
  **tooltip** (`C_TooltipInfo.GetInventoryItem`, matches the "<Track> cur/max" line) rather
  than `C_ItemUpgrade.GetItemUpgradeItemInfo` (which only reads the item in the open upgrade
  UI — useless headless). Each `equipment[]` slot carries `track/upgradeLevel/upgradeMax/upgradeText`.
  Resolves the 259 Champion-5/6-vs-Hero-1/6 ambiguity. ✅ **Consumed:** `charstate` normalizes
  it (dump-primary, API fallback) → `track_by_slot`; `wowkb.character` shows a Track column;
  the crest scoring model reads it for real headroom.
- ~~**The five "…of the Dawn" achievement IDs**~~ — DONE + consumed. New `achievements[]` block
  (`GetAchievementInfo`, account-wide) → `charstate` exposes `dawn_achievements`; `wowkb.character`
  renders the discount-status section (which sub-263 slots gate the 50% Champion discount).
- ~~**Hidden-currency-by-ID mechanism**~~ — DONE. `scanCurrencies` now appends reads for
  `ns.HIDDEN_CURRENCY_IDS` via `GetCurrencyInfo`. Table ships **empty** — see below.

### ✅ The three "missing currencies" — all resolved (2026-07-10)
The right source turned out to be one we already read, not the addon:
- ~~**Sparks of Radiance** (232875)~~ + ~~**Ascendant Voidshards** (268650)~~ — they're
  **items**, and **Syndicator already tracks the full bag+bank+warband inventory
  account-wide**. So `wowkb.charstate` now reads item counts from Syndicator (the same file
  we read for currencies) → `state["item_counts"]`, and `wowkb.character` shows a **Crafting
  mats** line. The brief detour of curating them in the addon (`ns.ITEMS`, v0.6.1/v0.6.2) was
  **reverted** — `ns.ITEMS` is empty again (v0.6.3); Syndicator is the item source.
- ~~**Catalyst charges**~~ = *Dawnlight Manaflux* (currency **3378**), a normal visible
  currency already captured — no work. `HIDDEN_CURRENCY_IDS` stays empty (neither was a real
  hidden currency); the mechanism remains for a genuine off-list one.
- **Also added:** `wowkb.character --skip-if-current` — skips the whole pull when the KB
  snapshot's `fetched:` is already ≥ the dump's capture date (the "don't re-pull if you
  already have the latest" short-circuit).

---

## Tooling / KB structure

- **Schema-8 ingest — Phase A + B DONE (2026-07-10).** `charstate.load` makes the addon dump
  the **primary** per-slot track source (`{track,level,cap}`, `None` for crafted), exposes
  `track_by_slot` + `dawn_achievements`; `wowkb.character` renders a **Track column** + a
  **"…of the Dawn" discount** section. Phase B: `rewards._crest_consumer(track)` values each
  crest as `max(real-per-slot headroom → CREST_CEILING {263/276/285}, CREST_FLOOR {Champion
  .25 / Hero .5 / Myth .75})` — Champion crests now have a consumer, the flat "Myth=4" rule is
  retired, and above-need crests keep a rarity-scaled future-material floor (never 0, always
  below a real need). Validated: Encomplete Champion 1.67 / Hero 3.83 / Myth 0.75(floor);
  Uncomplete Champion 3.83 / Hero 3.83 / Myth 0.75.
  **Two genuine remainders:**
  - **Precise craft-reagent term** (deferred, fully *unblocked* on data): value a crest by
    whether an 80-crest craft (Hero→272 / Myth→285) beats a craftable *non-tier* slot. Spark
    count is now in `state["item_counts"]` (Syndicator, item 232875), so the remaining work is
    pure wiring: read the spark count in the consumer + thread per-slot **tier flags** into
    `char_state` (equipment already carries `tier`). The floor is the stand-in until then.
  - **Gear-DROP ilvl-band fallback** still uses the overloaded/stale `TRACK_CEILING`
    (`Champion=259`) + `track_of_ilvl` 259→Hero-band guess. Now that real per-slot track is in
    the dump, `best_slot_delta`/the drop path could read it instead of band-guessing — separate cleanup.

## Research to-do

_(empty — drop "look into X" research threads here that aren't claim-verifications)_

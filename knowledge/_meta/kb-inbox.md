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

- **BucketBinds: source `spec_inventory` talents from wago `Trait*` (shrink `inventoryGaps` to
  zero).** The talent side of `wowkb.spec_inventory`'s union comes from `all-talents.tsv`, built
  off the Blizzard talent-tree API — whose static build (67808) **itself omits some real
  talents**, and a `wowkb.talents fetch` re-fetch returns the same holes (verified during the
  floats rollout). The floats workflow works around it with a **relaxed name-gate** (a name in the
  spec's `rotation.md` **and** in `raw/wago/SpellName.csv` is allowed, flagged in `inventoryGaps`,
  resolved by-name at runtime), but the real fix is to build the talent inventory natively from the
  wago **`Trait*`** tables (`TraitNodeXTraitNodeEntry` → `TraitNodeEntry` → `TraitDefinition.SpellID`,
  joined to the spec's tree via the manifest). Then API-omitted talents are covered and
  `inventoryGaps` shrinks to zero. **Per-spec gaps observed across the DPS/tank floats rollout**
  (the verification checklist — each already resolves in `SpellName.csv` and binds at runtime):
  - Hunter/Beast Mastery: Wailing Arrow
  - Hunter/Marksmanship: Arcane Shot, Steady Shot, Multi-Shot, Wailing Arrow
  - Mage/Arcane: Arcane Blast · Mage/Fire: Fireball
  - Monk/Brewmaster: Empty the Cellar · Monk/Windwalker: Zenith Stomp
  - Paladin/Protection: Hammer of Wrath, Hammer of Light, Hammer of the Righteous
  - Paladin/Retribution: Hammer of Light, Hammer of Wrath, Templar Slash
  - Priest/Shadow: Void Volley
  - Rogue/Subtlety: Shadowstrike, Shuriken Storm, Black Powder
  - Shaman/Elemental: Fire Elemental, Storm Elemental
  - Warlock/Destruction: Incinerate
  - Warrior/Arms: Heroic Strike · Warrior/Protection: Devastate
  - (Batches 1–2 — Frost Mage, Evoker Engulf, Devourer Consume/Devour/Pierce the Veil, etc. — noted
    in prior sessions; fold those in when building the checklist.)

- 🧭 **Planner re-architecture — see `../planning/goal-model.md` (design proposal, 2026-07-10).**
  Replace the activity-centric multiplier scorer (`scoring-model.md`) with a **goal-centric**
  pipeline: per-slot upgrade-candidate graph → goals → rank(value, steps) → select-to-time →
  TODO expansion with **shared-step dedup**. This is the agreed direction; the doc has a worked
  Uncomplete sketch. The remaining scoring items below are folded into it.

- **Schema-8 ingest — Phase A + B DONE (2026-07-10).** `charstate.load` makes the addon dump
  the **primary** per-slot track source (`{track,level,cap}`, `None` for crafted), exposes
  `track_by_slot` + `dawn_achievements`; `wowkb.character` renders a **Track column** + a
  **"…of the Dawn" discount** section. Phase B: `rewards._crest_consumer(track)` values each
  crest as `max(real-per-slot headroom → CREST_CEILING {263/276/285}, CREST_FLOOR {Champion
  .25 / Hero .5 / Myth .75})` — Champion crests now have a consumer, the flat "Myth=4" rule is
  retired, and above-need crests keep a rarity-scaled future-material floor (never 0, always
  below a real need). Validated: Encomplete Champion 1.67 / Hero 3.83 / Myth 0.75(floor);
  Uncomplete Champion 3.83 / Hero 3.83 / Myth 0.75.
  The two former "remainders" are resolved/redirected:
  - ~~**Gear-DROP ilvl-band fallback**~~ — DONE. `track_of_ilvl` had no callers (dead) and
    `TRACK_CEILING` was used only inside it; both removed. The live drop path (`best_slot_delta`)
    already values off real per-slot ilvls, so this was pure dead-code cleanup, no scoring change.
  - ~~**Precise craft-reagent term** as a crest multiplier~~ — DROPPED as the wrong shape.
    A craft isn't a multiplier on a crest; it's **one candidate path for a slot** in the
    goal model above (cost 80 crests + 2 sparks, yield 272/285, weighed by mats-in-hand).
    Data's all there (`item_counts`, tier flags); it gets built as part of the candidate graph,
    not bolted onto `_crest_consumer`. The `CREST_FLOOR` stays as the interim crest value.

## Research to-do

_(empty — drop "look into X" research threads here that aren't claim-verifications)_

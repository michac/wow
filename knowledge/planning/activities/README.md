---
title: Activity Catalog — outline (browse by goal / venue / cadence)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/activities/_facets.md
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Content Update Notes (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24295085   # Lairs preview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293963   # Coiled Isle / Vaults of Atal'Utek (Tier 1)
confidence: high
---

# Activity catalog — the outline

> **The reviewable index.** One line per activity; details live in the per-activity
> file. This is a **projection over tags** (`_facets.md`) — the same 28 activities
> shown three ways. Intended to be **generated** from the front matter eventually;
> hand-maintained for now (seed 2026-07-06; YouTube research pass 2026-07-06;
> 12.1 pass 2026-08-11).
>
> Read the contract first: [`_facets.md`](_facets.md). Include-by-default —
> `status: invalidated` hides a file; low `confidence` does **not**.

## ⚠ Pre-season week (2026-08-11 → 08-17): six activities are parked

12.1 went live **2026-08-11** but **Midnight Season 2 does not open until
2026-08-18**. Six catalog entries are therefore `status: invalidated` **for this
week only** and are marked ⏸ below — each carries a re-activate note in its own
front matter. They are *not* dead; do not delete them, and do not let the ranker
surface them:

| ⏸ Parked | Returns | Why |
|---|---|---|
| `mplus` | 2026-08-18 | no keystones drop until S2 opens |
| `delve-bountiful` | 2026-08-18 | no Bountiful Delves during pre-season |
| `prey-weekly` | 2026-08-18 | Nightmare Mode offline Aug 11–17 |
| `pvp-conquest` | 2026-08-18 | rated PvP + Conquest return with S2 |
| `voidcores` | 2026-08-25 | S1 cores converted to gold; bonus rolls arrive week 3 |
| `turbulent-timeways` | — | **event ended 2026-08-11** (not a pre-season park) |

**Two goal facets have no active rider this week:** `goal:rating` (both `mplus`
and `pvp-conquest` are parked) and `goal:leveling` (its only rider was
`turbulent-timeways`). `venue:delve` is likewise empty until Aug 18. Expect the
ranker's shortlist to skew hard toward `venue:world` — that is correct, not a bug.

## Seed status

**28 activities.** 13 seed (migrated from `candidates.json`) + 12 net-new from the
2026-07-06 YouTube research pass + **3 net-new for 12.1** (`coiled-isle`,
`lair-tidebound-grotto`, `zuljarra-renown`). M+, delves, raid, and rated PvP each
*fill* the single Great Vault via a `breakpoint`, so there's **one** vault-claim
entry, not four.

**12.1 additions and the tag vocabulary:** none of the three new files needed a
new facet value. **Lairs are `venue:world`, not `venue:raid`** — a Lair is an
instanced *world-boss* format found at a fixed outdoor location with a summoning
stone, on a weekly lockout, so it inherits world-solo/flex E rather than the
raid-group E penalty. `zuljarra-renown` is tagged by *what its next unlock is*
(`gearing` / `professions` / `collectibles`) per `_facets.md`'s
no-`reputation`-goal rule.

**Remaining thin spots / research targets:**
- `goal:leveling` has lost its only rider now that Timeways has ended — it needs a
  real activity, not a re-tag.
- **No M0 / Heroic-dungeon entry.** `mplus.md` records that the S2 pool is already
  live on **Heroic and Mythic 0** this week, with **M0 on a weekly lockout dropping
  Champion 1/6 (ilvl 292)** — real gearing value, but explicitly *not* that activity
  (no keystone, no IO, no M+ vault credit). With `mplus` parked, `venue:dungeon` has
  exactly one active rider (`renown-dungeon-weekly`) and **the week's actual
  dungeon-gearing route is rankable nowhere.** Minting an M0/Heroic entry is the
  second catalog job, alongside the `venue:raid` job noted below.
- Several gates are `manual`/best-effort (see per-file **Gate TODO**s); resolving
  detectable signals is the separate ranker-wiring phase, not this md pass.

## By goal (default view — "what am I working on")

**gearing** (22, 6 parked)
- `great-vault` — claim the one weekly Great Vault reward
- `mplus` ⏸ — Mythic+ dungeons: loot, crests, IO; fills the Vault's M+ column
- `delve-bountiful` ⏸ — Bountiful delves: weekly cache + fills the Vault's world column
- `prey-weekly` ⏸ — 3 Nightmare Prey hunts
- `pvp-conquest` ⏸ — weekly Conquest → gear/tier; fills the Vault's PvP column (also rating)
- `voidcores` ⏸ — Nebulous Voidcore bonus-roll gear
- `turbulent-timeways` ⏸ — Timewalking gear/mounts (also leveling, collectibles)
- `lair-tidebound-grotto` — weekly Tidebound Grotto kill (Nymrissa Wavecaller) *(new 12.1)*
- `coiled-isle` — Curse Surges, Vaults of Atal'Utek, isle rares *(new 12.1)*
- `zuljarra-renown` — Zul'jarra's Forces renown track *(new 12.1)*
- `liadrin-spark` — world-event weekly, Spark (also professions)
- `world-boss` — weekly world boss (also collectibles)
- `ritual-sites` — Field Accolades + Season 2 crests (repeatable)
- `void-assault` — Void Assault weekly (also collectibles)
- `renown-dungeon-weekly` — 1500 choice-rep → gear unlock
- `val-naigtal` — Val/Naigtal zone farm: Field Accolades → slot gear (also collectibles)
- `showdown-weekly` — Val/Naigtal Showdown weekly; World Tier boss (also collectibles)
- `faction-weeklies` — faction events → champion-track gear (also collectibles)
- `omnium-folio` — weekly power-track rune (also story)
- `midnight-campaign` — campaign gear + unlocks (also story)
- `crafting-orders` — orders → crafted gear (also professions)
- `pvp-honor` — honor set + weekly PvP quests

**leveling** (1, **all parked**) — `turbulent-timeways` ⏸
**professions** (5) — `liadrin-spark` · `profession-weekly` · `crafting-orders` · `darkmoon-faire` · `zuljarra-renown`†
**collectibles** (13, 1 parked) — `world-boss` · `void-assault` · `housing-weekly` · `trading-post` · `faction-weeklies` · `showdown-weekly` · `val-naigtal` · `darkmoon-faire` · `abyss-anglers` · `sporefall-raid`‡ · `coiled-isle`† · `zuljarra-renown`† · `turbulent-timeways` ⏸
**rating** (2, **all parked**) — `mplus` ⏸ · `pvp-conquest` ⏸
**story** (2) — `midnight-campaign` · `omnium-folio`

_† = net-new in the 12.1 pass · ‡ = `sporefall-raid` dropped `goal:gearing` in 12.1 — it is
previous-tier now, so its remaining pull is mounts/transmog, not power._

## By venue (the gather axis)

- **meta** — `great-vault` · `trading-post` · `voidcores` ⏸
- **dungeon** — `renown-dungeon-weekly` · `mplus` ⏸ · `turbulent-timeways` ⏸
- **delve** — `delve-bountiful` ⏸    _(no active rider this week)_
- **world** — `liadrin-spark` · `world-boss` · `ritual-sites` · `void-assault` · `faction-weeklies` · `showdown-weekly` · `val-naigtal` · `darkmoon-faire` · `abyss-anglers` · `coiled-isle`† · `lair-tidebound-grotto`† · `zuljarra-renown`† · `prey-weekly` ⏸
- **housing** — `housing-weekly`
- **raid** — `sporefall-raid`
- **pvp** — `pvp-honor` · `pvp-conquest` ⏸
- **quest** — `midnight-campaign` · `omnium-folio`
- **profession** — `profession-weekly` · `crafting-orders`

> **No `venue:raid` entry for The Venomous Abyss yet** — the raid does not open
> until **2026-08-18**, so there is deliberately no rankable activity for it
> during pre-season. Minting one is the first catalog job of the Aug-18 pass.

## By cadence / time (the urgency lens)

- **event · time-boxed** (U↑) — `turbulent-timeways` ⏸    _(ended 2026-08-11; bucket now empty)_
- **monthly · time-boxed** (U↑ recurring) — `darkmoon-faire`
- **weekly · standing** (expires this reset) — `great-vault` · `sporefall-raid` · `liadrin-spark` · `world-boss` · `void-assault` · `renown-dungeon-weekly` · `housing-weekly` · `omnium-folio` · `profession-weekly` · `faction-weeklies` · `showdown-weekly` · `lair-tidebound-grotto`† · `mplus` ⏸ · `delve-bountiful` ⏸ · `prey-weekly` ⏸ · `voidcores` ⏸ · `pvp-conquest` ⏸
- **monthly · standing** — `trading-post`
- **repeatable · standing** (no expiry) — `ritual-sites` · `pvp-honor` · `crafting-orders` · `val-naigtal` · `abyss-anglers` · `coiled-isle`† · `zuljarra-renown`†
- **one-time · standing** — `midnight-campaign`

> ⚠ **`lair-tidebound-grotto` is weekly per lair, not per difficulty** — the Lair
> lockout is one kill per week, and a Voidcore may be spent once per week per lair.
> This week it is **World difficulty only**; Normal/Heroic/Mythic open 2026-08-18.

---

**After editing any activity file, re-run `wowkb.gen_candidates`** — `candidates.json`
is generated from these `.md` files and will not pick up a status flip, a new file,
or a tag change on its own.

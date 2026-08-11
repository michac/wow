---
id: zuljarra-renown
name: Zul'jarra's Forces renown (Coiled Isle)
goal: [gearing, professions, collectibles]
venue: world
group: solo
cadence: repeatable
time: standing
scope: account
status: active
gate: { type: always }        # a standing renown track, never "done this reset"; the dailies/weeklies that FEED it gate under `coiled-isle`
reward: { type: [power, currency, collectible], detail: "20 renown ranks: R2 Cursebreaker's Bracers I (Veteran wrist) · R8 daily Warbound Veteran gear chance from Curse Surge bosses · R9 Cursebreaker's Bracers II (Champion wrist); plus Coiled Isle profession recipes + knowledge, housing decor, Spirit of Tok'jara mount questline (R10) and the title Hash'ura of Zul'jarra (R20)" }
yields:
  slots:
    # The two vendor bracers are the only DETERMINISTIC gear on the track: you buy the
    # wrist piece outright, so `targeted: true`. Landing ilvls are the Season 2 track
    # 1/6 steps (Veteran 279 / Champion 292, `endgame/lairs.md` + `_meta/moving-values.md`);
    # the vendor's exact step is not published. @verify-ingame: read the tooltip on
    # Cursebreaker's Bracers I and II at Jan'sari the Watchful and pin the real ilvl.
    - { track: veteran, ilvl: 279, chance: 1.0, targeted: true, slots: [wrist] }   # R2 — Cursebreaker's Bracers I
    - { track: champion, ilvl: 292, chance: 1.0, targeted: true, slots: [wrist] }  # R9 — Cursebreaker's Bracers II
time_blocks: 2
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" Content Update Notes (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963  # Follow the Snakes to the Coiled Isle (Tier 1)
  - https://www.icy-veins.com/wow/news/renown-and-vendor-rewards-zone-talents-corrosive-powers-new-coiled-isle-zone-in-12-1-and-everything-on-it-detailed/  # renown track rank-by-rank (Tier 3)
  - https://www.method.gg/guides/zuljarras-forces-reputation-guide-for-wow-midnight  # rep sources + 2,500/rank (Tier 3)
  - knowledge/factions/zuljarras-forces.md
  - knowledge/endgame/world-events.md
confidence: medium
---
**Zul'jarra's Forces** is the Coiled Isle's renown faction and the zone's primary
progression track — **20 ranks**, account/warband-wide, **2,500 reputation per rank**
(Tier 3; not stated in the Tier-1 notes). Quartermaster **Jan'sari the Watchful** at
**Tokka's Landing**; rewards are priced in **Voidlight Marl**, with the profession
recipes costing profession-specific **Artisan Moxies**. Full rank-by-rank track:
`knowledge/factions/zuljarras-forces.md`.

**Live now, in the pre-season week.** Unlike most of the 12.1 headline content, this
track does *not* wait for Season 2 (2026-08-18) — the Coiled Isle, Curse Surges and the
Vaults of Atal'Utek are all up from 2026-08-11, so renown accrues today. Rep even starts
*before* landfall: the Zul'Aman quests with **Lady Liadrin**, **Orweyna** and
**Zul'jarra** feed it, then the Coiled Isle campaign and zone activities carry it.

**Why it's `goal:gearing` and not just collectibles** (renown is instrumental —
`_facets.md`): three ranks pay in power, and they are the whole reason this row
competes with a delve.

| Rank | Unlock | Note |
|---|---|---|
| **R2** | **Cursebreaker's Bracers I** — Veteran-track wrist | early catch-up wrist for a fresh 90 / alt |
| **R8** | Curse Surge bosses gain a **daily chance at Warbound Veteran equipment** | Warbound-until-Equipped ⇒ alt-feeder, not just this char |
| **R9** | **Cursebreaker's Bracers II** — Champion-track wrist | the track's real gearing payoff |
| R10 | **Spirit of Tok'jara** mount questline | `goal:collectibles` |
| R5–R7 | Coiled Isle profession recipes, knowledge tomes, Artisan Moxie spends | `goal:professions` |
| R20 | title **"Hash'ura of Zul'jarra"** | terminal completionist |

Only the two **bracer** vendor buys are declared in `yields.slots` — they're
deterministic (you pick the piece, `targeted: true`), so the runtime slot-target R
values them against this character's actual wrist ilvl and correctly reads **0 for a
geared main** whose wrist already beats them. The **R8 daily Curse Surge chance is
deliberately NOT declared**: its drop rate is unpublished and unmeasured, and inventing
a `chance:` would push a fabricated number straight into scoring. It is real upside for
an alt-heavy warband; treat it as prose colour until someone measures it.

**Overlap — do not double-count.** `coiled-isle` is the zone's daily/weekly loop and
`renown-dungeon-weekly` / `midnight-campaign` also hand out Zul'jarra rep; those rows
own the *clears*, this row owns the **renown track** those clears advance. Ranking both
at full value for one Coiled Isle session over-counts the same hour. (Same shape as the
`faction-weeklies` ↔ `liadrin-spark` ↔ `void-assault` note.)

**Known scoring gap.** `scoring-model.md` names "renown level that unlocks a specific
gear/recipe reward" as a breakpoint, but `plan.py` implements **`breakpoint.type: vault`
only** — there is no renown breakpoint type and the PlannerState dump does not carry
Zul'jarra renown, so no `breakpoint:` block is declared here (an unsupported type is a
silent no-op). Until that lands, this row scores off `goal` + the two bracer slot
vectors, which means it **under-values the R2 → R8 → R9 crossings** — the runs that
actually unlock something. Parked in `_meta/kb-inbox.md` territory alongside the
track-aware crest costing.

**Confidence is `medium` on purpose.** The Tier-1 notes confirm the zone, the Curse
Surges and Tokka; the *renown track itself* — 20 ranks, 2,500/rank, the quartermaster's
name and location, and every per-rank reward above — comes from Tier-3 guides
(Icy Veins, Method) and has not been corroborated against game data or seen in game.

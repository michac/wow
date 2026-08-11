---
title: Lairs — Instanced World Bosses (Midnight Season 2)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24295085            # "Step Into Lairs and Face the Foes Inside" — the reward table (tier 1; archived raw/pages/worldofwarcraft-com-en-us-news-24295085.md)
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 information — lockout, BoP, Voidcore, pre-season split (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281            # Curse of Ula'tek Content Update Notes (tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214    # Mistcrest currency IDs 3437–3441 + upgrade bands (tier 1 game data)
  - https://www.icy-veins.com/wow/news/no-more-world-world-boss-evolution-all-you-need-to-know-about-lairs/  # corroboration only (tier 3)
confidence: high
---

# Lairs (12.1 "Curse of Ula'tek")

**New in 12.1.** A Lair is an **instanced world boss** — Blizzard's stated
"evolution on world bosses". It replaces the old fly-out-and-tag-a-boss-in-the-
open-world flow with a queued instance that has real difficulties, real lockouts
and a real loot table.

Structurally it sits between a Delve and a raid: you find it at a **fixed
location in the world, with a summoning stone outside**, exactly like a Delve —
but inside it is a scaling boss encounter with a raid-style reward track.

⚠ **Pre-season split.** 12.1 went live **2026-08-11**, but Midnight Season 2
does not open until **2026-08-18**. Right now **only World difficulty is
available.** Normal / Heroic / Mythic all unlock with the week of Aug 18
maintenance. The pre-season split is tabulated in
`../_meta/changelog-12.1.md` (the Aug-11 / Aug-18 table, "Lair" row);
`../_meta/game-version.md` records the same state once its 12.1 bump lands.

## Difficulties

| Difficulty | Group | Available |
|---|---|---|
| **World** | Solo queue; the instance fills itself | **Live now (2026-08-11)** |
| **Normal** | Pre-made group | 2026-08-18 |
| **Heroic** | Pre-made group | 2026-08-18 |
| **Mythic** | **Flexible 15–25** players | 2026-08-18 |

Flexible Mythic is the same sizing Sporefall introduced in 12.0.7 (see
`raids/overview.md`) — no fixed-20 requirement.

### How World difficulty actually plays

This is the part that differs most from a raid. You queue **solo** and are put
straight in; **the instance then fills up with additional challengers while you
play**. What you play is a **two-part scenario**:

1. Clear **elite monsters** until the boss appears.
2. Fight the boss.

**The boss scales 5–40 players**, so the encounter stays valid whether the
instance filled to a handful or to a small raid's worth of people. That scaling
range is the design's whole point: a solo queuer and a 40-strong pile-in both
walk away with the same epic loot.

### ⚠ 12.1's global combat retune applies in here too

Lairs are new in 12.1, so there is no instance-specific "before" to compare
against — but the encounter does **not** sit outside the patch's four global,
every-spec changes (`../_meta/changelog-12.1.md`, Classes preamble):

- **Player health and creature damage both +25% at max level**, with health
  consumables rescaled and several DPS/Tank healing + absorb spells retuned.
  Any pre-2026-08-11 absolute HP / healing / potion number is now wrong.
- **Major DPS cooldowns lowered, steady-state damage raised** for several specs
  — burst-vs-sustained planning has moved even where per-ability numbers look
  familiar.
- **Interrupts now show a "missed" visual + sound** when the target was not
  casting.
- **Diminishing-return categories reset after 20s** (was 16s).

So recommended-ilvl-versus-actual-difficulty intuitions carried over from
Season 1 world bosses do not transfer cleanly.

## Loot, lockouts and Voidcores

- Lair gear is **bind-on-pickup**, like raid gear — **not** warbound-until-
  equipped the way outdoor rare drops are. You cannot funnel it to an alt.
- **Weekly lockout** per lair.
- A **Nebulous Voidcore** bonus roll may be spent **once per week, per lair**.
  ⚠ Voidcores are **not** available yet in Season 2 — they return as a Great
  Vault reward and bonus rolls only start the **week of Aug 25**, requiring at
  least 3 vault panes unlocked (see `great-vault.md`).

## Tidebound Grotto — the first (and so far only) lair

| | |
|---|---|
| **Zone** | The Coiled Isle (see `../systems/coiled-isle.md`) |
| **Level** | 90 |
| **Bosses** | 1 — **Nymrissa Wavecaller**, a naga sorceress |
| **Entrance** | **Underwater.** Swim down into the waters below the isle to a submerged cave. |

> "Nymrissa Wavecaller commands the restless sea itself, concealing her lair
> beneath shifting tides."

### Reward table (Tier 1, verbatim from the Lairs preview)

| Difficulty | Recommended ilvl | Drops at | Crest |
|---|---|---|---|
| **World** | 273 | **279** — Veteran 1/6 | Veteran Mistcrest |
| **Normal** | 286 | **292** — Champion 1/6 | Champion Mistcrest |
| **Heroic** | 299 | **305** — Hero 1/6 | Hero Mistcrest |
| **Mythic** | 312 | **318** — Myth 1/6 | Myth Mistcrest |

All four rows, including Mythic, are verbatim from the Blizzard preview table.
*(Provenance: an early draft of the 12.1 ledger truncated the Mythic row and
told this file to leave it unstated. That was a capture gap, not an absence —
the row is present in the archived page
`raw/pages/worldofwarcraft-com-en-us-news-24295085.md`, and
`_meta/changelog-12.1.md` and `_meta/moving-values.md` were both corrected to
match on 2026-08-11. No lower-tier source was used to establish this row.)*

Season 2's crest currency is the **Mistcrest** line (Season 1's was the
Dawncrest — see `dawncrests.md`). The five crest **names** are Tier-1 **game
data**, not editorial: `CurrencyTypes` DB2 @ build `12.1.0.69214`, currency IDs
**3437–3441** (Adventurer / Veteran / Champion / Hero / Myth Mistcrest). The
preview table above independently corroborates four of the five.

⚠ **The track-step labels here and the crest upgrade bands in `dawncrests.md`
are offset by one step (3 ilvl) — this is expected, not a typo.** This table
says a World drop is **279, "Veteran 1/6"**; the DB2 band for Veteran Mistcrest
reads **282–295**. Both are Tier-1. The DB2 band's **upper** number is the
track's 6/6 ceiling, while 1/6 sits one ~3-ilvl step below the band's lower
number. `dawncrests.md` carries the reconciled per-track ladder — use it, and
do not "fix" either number against the other.

## Where it fits in the week

- **Right now (pre-season, week of Aug 11):** Tidebound Grotto World difficulty
  is a **Season 2 Veteran gear** source and one of the few things dropping 279
  during the pre-season week. Worth one clear per character per week.
- **From Aug 18:** Normal/Heroic/Mythic open. Heroic at 305 (Hero 1/6) is
  competitive with early raid Normal, on a much cheaper time cost — one boss.
- Lairs **supersede the old world-boss rotation** as the outdoor group-content
  gearing path. Note that the legacy Midnight world bosses' drops are now frozen
  at Season 1 items and **can no longer be upgraded** (see `world-events.md`).

## TODO / open questions

- [ ] **Which Great Vault row does a lair clear credit?** A Tier-4 guide claims
      the **Raid** row; no Tier-1 source states it. Do not plan around this
      until confirmed. @verify-ingame
- [ ] Nymrissa Wavecaller's actual mechanics — no Tier-1 encounter detail
      published, and no Dungeon Journal capture taken yet.
- [x] **Whether the World-difficulty elite-clear phase has its own rewards, or
      is purely a gate.** Tier-1 frames it as a **gate only** — the preview says
      the elite phase "just ensures a certain critical mass before the second
      part of the scenario can begin." No phase-specific reward is stated.
      Absence of a stated reward is not proof of none; if you see elite-phase
      loot in game, reopen this. @verify-ingame
- [ ] Whether more lairs are planned for Season 2. Tidebound Grotto is the only
      one shipped in 12.1; Blizzard has not said whether a second follows.
- [ ] Confirm the summoning stone's location/coordinates on the Coiled Isle.
      Tier-1 confirms only that lairs sit at fixed zone locations "with an
      available summoning stone just outside the instance" — no coords given.
      @verify-ingame

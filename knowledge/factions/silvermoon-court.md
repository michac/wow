---
title: Silvermoon Court (Renown Faction — Midnight)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://wago.tools/db2/Faction          # Tier 1 — faction/house IDs, 2500 ReputationMax_0, ParagonFactionID 2727
  - https://worldofwarcraft.com/en-us/news/24293281  # Tier 1 — 12.1 content update notes (no Silvermoon Court entry)
  - https://www.icy-veins.com/wow/silvermoon-court-renown-guide
  - https://www.sportskeeda.com/mmo/wow-midnight-silvermoon-court-rep-guide-vendor-rewards-farming-tips
confidence: medium
---

# Silvermoon Court

One of the Midnight renown factions. 12.1 "Curse of Ula'tek" took the set from
**four to five**: Silvermoon Court, Amani Tribe, The Hara'ti, The Singularity,
and the new **Zul'jarra's Forces** on the Coiled Isle
(`factions/zuljarras-forces.md`).

> ⚠ **Slayer's Rise is not one of them.** *Slayer's Duellum* is an old-school,
> **character-specific** standing (Friendly → Exalted), not a Warband-wide
> renown track — see `factions/slayers-rise.md`, which carries the explicit
> 2026-06-03 correction. Counting it gives the wrong total (6 instead of 5).

12.1 made **no Silvermoon-Court-specific changes** — neither the content update
notes nor the 12.0.7 hotfix log mentions the faction, its quartermaster, its
currencies or its renown rewards — so the content below carries over from
12.0.5. (Kirana and Orin Straylight relocated *to Silvermoon* in 12.1, but they
are Catalyst/Voidcore vendors, not Court vendors — see `endgame/catalyst.md`.)
12.1's four game-wide class changes — max-level player health and creature
damage **+25%**, DPS cooldowns lowered against raised steady-state damage,
interrupts showing a "missed" visual, and diminishing-return categories
resetting after **20s** (was 16) — apply everywhere, including Eversong Woods
content, but touch no reward or rep number on this page.

## Quartermaster + location

- **Caeris Fairdawn**, at **Saltheril's Haven, Eversong Woods**
  (`/way #2395 43.4 47.4`).
- Four sub-faction ("Noble House") vendors also sell cosmetics for the
  secondary currency **Brimming Arcana**:
  - Blood Knights — Armorer Goldcrest
  - Farstriders — Ranger Allorn
  - Magisters — Apprentice Diell
  - Shades of the Row — Neriv

> **Resolved 2026-08-11 (Tier 1).** The fourth house is **"Shades of the Row"**,
> not "Shades of the Bow" — wago.tools `Faction` DB2, faction **2714**. All four
> houses are children of Silvermoon Court (**2710**): Magisters 2711, Blood
> Knights 2712, Farstriders 2713, Shades of the Row 2714.

## Currencies

- **Voidlight Marl** — primary quartermaster currency.
- **Brimming Arcana** — earned from Saltheril's Soiree activities; spent at the
  four Noble House sub-faction vendors.

## Renown track highlights

**2,500 rep per rank**, **20 ranks**, with Paragon rewards beyond the final
rank. Those two numbers do **not** share a source — read the attribution below
before citing either.

> **What is Tier-1 here (wago.tools `Faction` DB2, row 2710, 2026-08-11):** the
> **2,500** is `ReputationMax_0` (**not** `ReputationBase_0`, which is `0`), and
> `ParagonFactionID` is **2727** = "Silvermoon Court (Paragon)". That row's
> `RenownFactionID` is **0** and it carries **no rank count**, so the **"20
> ranks" figure is Tier-3** (Icy Veins) and unconfirmed against game data.

- Rank 4 — Friend of the Court 1
- Rank 6 — Silvermoon Bounty 1 (500 Voidlight Marl)
- Rank 8 — Friend of the Court 2
- Rank 9 — **Veteran helm**, re-issued each season (S2: **279**, upgrades
  **282 → 295**). The runestone unlock quest must be redone to collect it again.
  [in-game 2026-08-16]
- Rank 12 — Dragonhawk Munchkin battle pet
- Rank 17 — Crimson Silvermoon Hawkstrider (ground mount)
- Rank 19 — Fiery Dragonhawk (flying mount)
- Rank 20 — "Life of the Party" title

Early ranks also unlock transmog ensembles, an ilvl 180 helm, profession
recipes, event bonuses, and housing decor.

⚠ Tier-3 guides (Method's Season 2 gearing guide among them) call the renown gear
**Champion** track. It is **Veteran** — observed in game, and consistent with
`factions/zuljarras-forces.md`, where Veteran sits at Rank 2 and Champion at Rank 9.
The early-rank **ilvl 180 helm** is a Season 1 number and has not been re-checked.
@verify-ingame

## Weekly renown sources

- **Saltheril's Soiree** — select a faction/Noble House to bring to Saltheril's
  Haven for the week, then complete the **"Fortify the Runestones"** weekly
  quest for the bulk of weekly reputation.
- World quests and events in Eversong Woods / the Quel'Thalas zones contribute
  ongoing rep.

> Source confidence stays **medium**. **Tier-1** (`Faction` DB2, 2026-08-11):
> the faction and sub-faction names/IDs, the 2,500 rep per rank, and the
> existence of a Paragon faction. **Tier-3/4 and not re-verified in 12.1**:
> the **rank count (20)**, the **per-rank reward list**, and every **ilvl** on
> this page — all from Icy Veins (last updated 2026-05-19) plus a Tier-4 SEO
> guide. Confirm a specific rank's reward in-game or against the Wowhead DB page
> before relying on it. @verify-ingame Silvermoon Court renown: confirm the
> final rank number and the Rank 9 / early-rank reward ilvls on a 12.1 character.

## Changelog

2026-08-17 — rank-9 helm is a Veteran-track piece that re-issues each season (S2 279),
not a dead Season 1 Champion 246. The page had said renown gear was not rescaled at all.

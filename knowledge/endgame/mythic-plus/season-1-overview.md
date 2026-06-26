---
title: Midnight Season 1 Mythic+ Overview
patch: 12.0.7
fetched: 2026-06-19
sources:
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - Warcraft Logs zone 47 "Mythic+ Season 1" (tier 2)
  - Blizzard Game Data API, journal-expansion/516 (tier 1)
confidence: high
---

# Mythic+ — Midnight Season 1

M+ unlocked the week of **2026-03-24** (season opened 2026-03-17).

## Dungeon pool (8)

Each links to a one-page **cheat sheet** (`dungeons/`) — route, the boss
mechanics that actually wipe groups, must-interrupt trash, role notes.

| Dungeon | Origin | WCL enc. ID | Cheat sheet |
|---------|--------|-------------|-------------|
| Magisters' Terrace | TBC (Midnight-new to M+) | 12811 | [`dungeons/magisters-terrace.md`](dungeons/magisters-terrace.md) |
| Maisara Caverns | Midnight (new) | 12874 | [`dungeons/maisara-caverns.md`](dungeons/maisara-caverns.md) |
| Nexus-Point Xenas | Midnight (new) | 12915 | [`dungeons/nexus-point-xenas.md`](dungeons/nexus-point-xenas.md) |
| Windrunner Spire | Midnight (new) | 12805 | [`dungeons/windrunner-spire.md`](dungeons/windrunner-spire.md) |
| Algeth'ar Academy | Dragonflight (returning) | 112526 | [`dungeons/algethar-academy.md`](dungeons/algethar-academy.md) |
| Seat of the Triumvirate | Legion (returning) | 361753 | [`dungeons/seat-of-the-triumvirate.md`](dungeons/seat-of-the-triumvirate.md) |
| Skyreach | WoD (returning) | 61209 | [`dungeons/skyreach.md`](dungeons/skyreach.md) |
| Pit of Saron | WotLK (returning) | 10658 | [`dungeons/pit-of-saron.md`](dungeons/pit-of-saron.md) |

> Cheat-sheet boss mechanics are corroborated across **tier-3 Midnight
> guides** (Method/Icy Veins/Wowhead-Midnight/Conquest Capped), not tier-1 —
> most carry `confidence: medium`. Boss *rosters* and kill orders are
> web-verified current; exact numeric tuning (timers, % buffs) is the soft
> spot. Returning dungeons (5 of 8) had their old-expansion rosters confirmed
> **replaced/retuned**, not copied.

(One secondary source listed 9 dungeons; both the Icy Veins S1 guide and
WCL zone 47 "Mythic+ Season 1" confirm **8** — verified 2026-06-03. The
Midnight *expansion* ships more dungeons — Den of Nalorakk, Murder Row,
The Blinding Vale, Voidscar Arena per journal-expansion/516 — but they are
not in the S1 M+ rotation.)

## Affixes

| Key level | Affixes |
|-----------|---------|
| +2 to +4 | **Lindormi's Guidance** (newcomer-help affix, teaches routes) |
| +5 to +11 | One rotating **Xal'atath's Bargain** (Ascendant / Voidbound / Pulsar / Devour) + Fortified **or** Tyrannical |
| +7 to +10 | Fortified/Tyrannical rotate weekly |
| +10 and up | Fortified **and** Tyrannical both active |
| +12 and up | **Xal'atath's Guile** replaces all Bargains; deaths more punishing |

See `affixes.md` for **what each affix does and how to play around it**
(Lindormi's Guidance, the four Xal'atath's Bargains, Guile).

## Rewards

See `keystones.md` for **how keys work** (first key, upgrade/downgrade,
resilient floor). See `loot.md` for **how M+ loot actually works** (end-of-run
drop vs vault vs currency, why most runs give no gear, the +6 Hero breakpoint).
See `rating-and-rewards.md` for **M+ rating + what you're chasing** (score
mechanics, +10 teleport portals, KSM/KSH titles, the Calamitous Carrion mount).
See `../great-vault.md` for the full ilvl table. Vault cap at **+10** (272).

12.0.5 notes (SignsOfKelani, 2026-04-26):

- **+6 and up**: hero-track end-of-run drops.
- **+9 and up**: Myth Dawncrests every run (fastest myth-crest income).
- **+10 and up**: vault gives myth-track; **Nebulous Void Core bonus
  rolls give myth-track here** (`../../systems/void-forge.md`) — 2 cores
  + 1 vault slot = up to 3 myth pieces/week without ever timing higher.
- ~2 runs/hour with RNG loot vs ritual sites' ~1 guaranteed hero piece
  per ~5 runs — armor-stacked premades trade loot, pugs often don't.

## TODO

- [x] **One file per dungeon** (route, trash, boss notes) → `dungeons/*.md`
      (8 cheat sheets, 2026-06-21). Boss detail is tier-3-sourced; the
      open follow-up is **tier-1 numeric tuning** (timers, %s, spell IDs via
      `wowkb.wago` / journal-encounter) and confirming the stale-tagged affix
      lines in each sheet against live 12.0.
- [ ] Verify Xal'atath's Bargain **weekly rotation schedule** (which Bargain
      is up which week — mechanics now in `affixes.md`, the *schedule* is not).

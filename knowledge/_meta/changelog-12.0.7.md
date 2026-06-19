---
title: Change Ledger — 12.0.7 "Revelations" (+ hotfixes through 2026-06-19)
patch: 12.0.7
build: 12.0.7.68256
fetched: 2026-06-19
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://worldofwarcraft.blizzard.com/en-us/news/24276957/hotfixes-june-18-2026
  - https://www.icy-veins.com/wow/news/patch-12-0-7-revelations-full-content-update-notes/
confidence: high
---

# Change Ledger — 12.0.7 "Revelations"

> **Purpose:** the diff between 12.0.5 and 12.0.7. Use this to re-verify every
> `knowledge/**` file still labeled `patch: 12.0.5`. A file is **touched** if
> its topic appears in the "KB file impact map" below; otherwise its content is
> still current for 12.0.7 and only needs a front-matter re-stamp after a sanity
> read. **Patch 12.0.7 "Revelations" went live 2026-06-16.**
>
> This is a distillation of Tier-1 official notes + the running hotfix log.
> When a number matters, corroborate against wago.tools / the live API.

## Headline content additions (12.0.7)

- **New zones: Val and Naigtal** — two new worlds via portal from Voidstorm,
  rotating weekly. Naigtal = fungal/arcane world held by the ethereal
  **Hal'hadar**; Val = icy ex-Legion world ruled by **Domanaar Imperator
  Pertinax**. World quests, rares, events, world boss.
- **Omnium Folio** — NEW runic-power progression system; weekly unlocks, runes
  customizable for the rest of Midnight. (No existing KB file — needs creation.)
- **Sporefall raid** — single-boss raid vs **Rotmire** (fungal giant). RF /
  Normal / Heroic / Mythic, flexible Mythic 15–25. Drops: Luminous Sporeglider
  mount, Sporefused gear (ilvl **259–298**), housing decor. (Needs creation.)

## Systems changes (12.0.7)

- **Durability:** weapons/armor **no longer take durability damage from
  combat**. (Affects general gameplay / professions repair economy.)
- **Abundance harvesting:** can consume 1/2/4/8 Shards at once with scaled
  rewards. (Hotfix: bug fixed where Abundance couldn't begin in Voidstorm;
  refunds via Unalloyed Abundance.)
- **Housing:** outdoor lighting added (overlap prevention); exterior decor caps
  raised (Lv5–6: 300; Lv7+: 350); 100+ new common decor at vendors.
- **Void Assaults:** XP from wrapper quests / Strikes / Incursions **doubled**;
  higher drop rates for Dark Particles & Bulging Satchels; new cosmetic vendors
  for Dark Particles.
- **Ritual Sites:** new **Tier 6** difficulty (6 challenges, ilvl ~274 rec.);
  rewards 5 Mythic + 10 Heroic Dawncrests; new weekly quests w/ bonus rolls
  (Weeks 3 & 6); achievements "Advanced Ritual Site Studies" + "Pinnacle Ritual
  Work" (Ritual Breaker title).
- **Moth Hunt:** redesigned from Luminous Dust vendor → quest reward per 10 moths.

## Raid / dungeon tuning (12.0.7 + hotfixes)

- **March on Quel'danas — Midnight Falls boss:** broad Mythic/Heroic nerfs
  (Glimmering −20% Mythic; Criticality cast 3→4s; Dark Constellation 2.5→3s
  Mythic; Radiance −50% Heroic; Tears of L'ura soaks 2→1 Heroic; Resonance no
  longer triggers Tears). Earlier hotfix (5/19): Mythic damage/mechanic adjusts.
- **Voidspire (raid):** telepad / Salhadaar warning / teleportation fixes (hotfixes).
- **Turbulent Timeways:** timewalking event Jun 30–Aug 11, Dragonflight dungeon
  rotation, enhanced rewards. (Not a M+ Season 1 structural change.)

## Class / PvP tuning (hotfixes through 2026-06-19)

- **DK San'layn:** Thrill of Blood +damage to Dread/Virulent Plague 5%→**10%**.
- **DK Unholy/Magus:** Magus Shadow Bolt −15% (PvE only); Unholy Aura/Forbidden
  Ritual early-cancel fixed.
- **Annihilator (Warrior):** Voidfall Meteor −12%. **Thick Skin** Armor 150%→190%.
- **Deathstalker (Rogue):** Mark +30%; Clear the Witnesses → Fan of Knives
  40%→**60%**.
- **Warlock Affliction:** mechanic fixes (5/19, 4/24, 4/23 hotfixes) — re-verify
  rotation/builds numbers.
- **PvP (12.0.7):** Legend/Marshal/Warlord cutoffs → top 8 per spec (Solo
  Shuffle + BG Blitz); **PvP gear ilvl +9**; Galactic Voidsliver & Void Matrix
  removed → gold; rating gains from 2v2/3v3/Solo Shuffle increased (hotfix).
- Broad balance passes logged 5/26 and 5/5 across most specs — assume **all
  class spec files need numeric re-verification**.

## Prey / Delves / progression (12.0.7 + hotfixes)

- **Prey:** "Preferential Killing" once-per-week cap **removed** after rank 10
  (Custom Hunts repeatable); hunt progression increased; mode adjustments.
  New "Big Prey Hunter (Season 1)" Feat of Strength.
- **XP:** significantly increased for first-time delves (Delver's Call), Midnight
  dungeon quests, Prey, and weekly Renown activities.
- **Crests/Conquest:** accumulation caps removed for Season 1 (5/19 hotfix).
- **Ascendant Voidcore:** fixed eligibility for pre-12.0.5 crafted weapons/trinkets.

## Faction / story (12.0.7)

- **Amani troll storyline:** Zul'jan Chapter questline (Jul 7); Lorewalking with
  Loa; Jan'alai egg-hatching with Loa Speaker Brek. → touches Amani faction.
- New hostile factions introduced: **Hal'hadar** (Naigtal), **Domanaar** (Val).

## Items / misc (12.0.7)

- Great Vault raid tooltip formatting improved (display only).
- PvP currencies removed (see PvP above); various trinket/item ilvl fixes (hotfixes).

---

## KB file impact map

Legend: **CHANGED** = notes touch this topic, content edit needed ·
**RESTAMP** = no 12.0.7 change found, re-verify + bump front matter ·
**NEW** = create file.

| KB file | Verdict | Why |
|---|---|---|
| endgame/raids/march-on-quel-danas.md | CHANGED | Midnight Falls boss heavily retuned |
| endgame/raids/the-voidspire.md | CHANGED | Voidspire hotfix fixes |
| endgame/raids/overview.md | CHANGED | add Sporefall raid; ilvl ranges |
| endgame/raids/the-dreamrift.md | RESTAMP | no 12.0.7 mention found |
| endgame/prey.md | CHANGED | custom-hunt cap removed, XP, FoS |
| endgame/delves/overview.md | CHANGED | Delver's Call XP; delve hotfixes |
| endgame/great-vault.md | RESTAMP | only tooltip formatting changed |
| endgame/catalyst.md | RESTAMP | no 12.0.7 mention found |
| endgame/mythic-plus/season-1-overview.md | RESTAMP | Turbulent Timeways is timewalking, not M+ structure |
| endgame/weekly-checklist.md | CHANGED | new Tier 6 ritual weeklies, prey, void assault XP |
| endgame/world-events.md | CHANGED | Val/Naigtal, Turbulent Timeways, micro-holidays |
| endgame/dawncrests.md | CHANGED | Tier 6 Dawncrest rewards |
| systems/ritual-sites.md | CHANGED | Tier 6, new weeklies/achievements |
| systems/void-incursions.md | CHANGED | Void Assault XP/drops/vendors |
| systems/void-forge.md | CHANGED | Abundance harvesting multi-shard |
| systems/housing.md | CHANGED | outdoor lighting, decor caps, new decor |
| systems/professions.md | CHANGED | durability change affects repair economy |
| systems/tailoring-leveling.md | RESTAMP | no direct 12.0.7 mention |
| factions/amani-tribe.md | CHANGED | Zul'jan/Jan'alai/Lorewalking |
| factions/harati.md | RESTAMP | verify, no mention |
| factions/silvermoon-court.md | RESTAMP | verify, no mention |
| factions/slayers-rise.md | CHANGED | PvP cutoffs/ilvl/currency changes |
| factions/the-singularity.md | RESTAMP | verify, no mention |
| classes/warlock/affliction/rotation.md | CHANGED | aff hotfix mechanic fixes |
| classes/warlock/affliction/builds.md | CHANGED | re-verify talents/numbers |
| economy/live-data.md | RESTAMP | pointers only; verify links |
| characters/encomplete-plan.md | RESTAMP | re-fetch live before answering anyway |
| characters/hallick-kiljaeden.md | RESTAMP | re-fetch live before answering anyway |
| _meta/sources.md | RESTAMP | tier registry; just bump patch |
| (none) — Omnium Folio | NEW | systems/omnium-folio.md |
| (none) — Sporefall raid | NEW | endgame/raids/sporefall.md |

---
title: Midnight Daily/Weekly Repeatable Quests
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://www.wowhead.com/quests/min-level:90/max-level:90   # listview harvest
  - https://us.api.blizzard.com/data/wow/quest/area/15355       # Blizzard zone cross-check
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Curse of Ula'tek content update notes (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293963   # Coiled Isle / Vaults of Atal'Utek preview (Tier 1)
  - knowledge/_meta/patch-notes/12.1.md   # verbatim 12.1 notes (Tier 1 floor for rewards)
  - knowledge/_meta/moving-values.md   # crest family + reward-value registry (Tier 1)
  - knowledge/_meta/quests.md   # quest-data doctrine
confidence: medium   # auto-generated; cadence/track marked per-row, verify gated ones in-game
---

# Midnight Repeatable Quests — auto-generated catalog

> **Generated file — do not hand-edit.** Regenerate with `cd tools && uv run python -m wowkb.repeatables`. Machine-readable twin: `knowledge/planning/repeatables.json` (planner candidate-shaped + reverse indexes). This is a *repeatable scrape*, safe to re-run on patch days.

Reward **value** is the planner's baseline **R** (0–5) + goal tags (`gearing/vault/crafting/renown/cosmetic/gold/xp`), from `rewards.value_quest` — see `knowledge/planning/scoring-model.md`. R here is **character-agnostic**; a piece worthless to a geared character still shows its baseline. Character-relative scoring is the deferred follow-up below.

Catalog: **40** repeatable quests.

> ⚠ **Pre-season week.** 12.1 went live **2026-08-11**, but **Midnight Season 2 opens 2026-08-18**. Rows tagged `⚠pre-season` in the notes column are dormant or gated until then; `⚠S1-currency` marks a reward column still showing a Season 1 currency; `⚠volatile-amount` marks an amount the 12.1 notes say is still being tuned. All of them are spelled out under [Pre-season & Season-2 gating](#pre-season--season-2-gating-week-of-2026-08-11).

## Weekly (13)

| id | name | zone | rewards | value (R + goals) | questID | notes |
|---|---|---|---|---|---|---|
| rep-94446 | A Nightmarish Task | unknown | Voidlight Marl ×500; Hero Dawncrest ×20; Remnant of Anguish ×50 | R=3 gearing | 94446 | value:medium; ⚠pre-season; ⚠S1-currency; time/E _needs_human |
| rep-96730 | Ritual Site Studies: Week 3 of 3 | unknown | Nebulous Voidcore ×1; Voidlight Marl ×300; 68g | R=3 gearing,gold | 96730 | cadence:medium; questID:medium; ⚠pre-season; time/E _needs_human |
| rep-94385 | Void Assaults: Eversong Woods | unknown | Ranger's Cache [cosmetic, crafting, gearing, gold, vault]; Recruit's Cache [gold]; 88250 XP | R=3 cosmetic,crafting,gearing,gold,vault,xp | 94385 | cadence:medium; time/E _needs_human |
| rep-94386 | Void Assaults: Zul'Aman | unknown | Ranger's Cache [cosmetic, crafting, gearing, gold, vault]; Recruit's Cache [gold]; 88250 XP | R=3 cosmetic,crafting,gearing,gold,vault,xp | 94386 | cadence:medium; time/E _needs_human |
| rep-93593 | A Call to Battle | unknown | Conquest ×175 | R=2 gearing | 93593 | value:medium; ⚠pre-season; time/E _needs_human |
| rep-95416 | Going Postal | unknown | Voidlight Marl ×500; Community Coupons ×25; Essence of Lumber [crafting]; 13690 XP; 34g | R=2 cosmetic,crafting,gearing,gold,xp | 95416 | time/E _needs_human |
| rep-95438 | Lost Animals | unknown | Voidlight Marl ×500; Community Coupons ×25; Essence of Lumber [crafting]; 13690 XP; 34g | R=2 cosmetic,crafting,gearing,gold,xp | 95438 | time/E _needs_human |
| rep-93605 | The World Awaits | unknown | Voidlight Marl ×500; The Amani Tribe ×2500; Silvermoon Court ×2500; The Hara'ti ×2500 | R=2 gearing,renown | 93605 | time/E _needs_human |
| rep-96731 | Advanced Ritual Site Studies: Week 4 of 6 | unknown | Voidlight Marl ×300; 68g | R=1 gearing,gold | 96731 | cadence:medium; questID:medium; time/E _needs_human |
| rep-96732 | Advanced Ritual Site Studies: Week 5 of 6 | unknown | Voidlight Marl ×300; 68g | R=1 gearing,gold | 96732 | cadence:medium; questID:medium; time/E _needs_human |
| rep-96733 | Advanced Ritual Site Studies: Week 6 of 6 | unknown | Voidlight Marl ×300; 68g | R=1 gearing,gold | 96733 | cadence:medium; questID:medium; value:medium; ⚠T1-override; time/E _needs_human |
| rep-96728 | Ritual Site Studies: Week 1 of 3 | unknown | Voidlight Marl ×300; 68g | R=1 gearing,gold | 96728 | cadence:medium; questID:medium; time/E _needs_human |
| rep-96729 | Ritual Site Studies: Week 2 of 3 | unknown | Voidlight Marl ×300; 68g | R=1 gearing,gold | 96729 | cadence:medium; questID:medium; time/E _needs_human |

## Daily (19)

| id | name | zone | rewards | value (R + goals) | questID | notes |
|---|---|---|---|---|---|---|
| rep-92013 | WANTED: Dionaea's Thorntusks | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 92013 | cadence:medium; time/E _needs_human |
| rep-91970 | WANTED: Gelatonius | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 91970 | cadence:medium; time/E _needs_human |
| rep-92012 | WANTED: Gorebarb's Pincers | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 92012 | cadence:medium; time/E _needs_human |
| rep-91980 | WANTED: Hellebora's Thorn | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 91980 | cadence:medium; time/E _needs_human |
| rep-91998 | WANTED: Muckmire's Choking Vines | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 91998 | cadence:medium; time/E _needs_human |
| rep-92010 | WANTED: Slewstalk's Stalks | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 92010 | cadence:medium; time/E _needs_human |
| rep-91982 | WANTED: Toadshade's Petals | Harandar | Coffer Key Shards; Voidlight Marl; The Hara'ti; 16050 XP; 67g | R=3 gearing,gold,renown,vault,xp | 91982 | cadence:medium; time/E _needs_human |
| rep-97016 | Mixing Mysteries | The Coiled Isle | Corrosive Coin; Voidlight Marl; Handful of Esoteric Ingredients [crafting]; Handful of Esoteric Ingredients [crafting]; 13690 XP; 34g | R=2 crafting,gearing,gold,xp | 97016 | value:low; time/E _needs_human |
| rep-93865 | Carve Your Way | The Voidstorm | Honor ×50; Bloody Tokens ×50; Slayer's Duellum ×100; 13690 XP; 34g | R=1 gearing,gold,xp | 93865 | value:medium; ⚠pre-season; time/E _needs_human |
| rep-92554 | Addition of Anguish | Silvermoon City | — | R=0 — | 92554 | time/E _needs_human |
| rep-95616 | Barrier A | Vaults of Atal'Utek | — | R=0 — | 95616 | time/E _needs_human |
| rep-95617 | Barrier B | Vaults of Atal'Utek | — | R=0 — | 95617 | time/E _needs_human |
| rep-95619 | Barrier C | Vaults of Atal'Utek | — | R=0 — | 95619 | time/E _needs_human |
| rep-95695 | Barrier D | Vaults of Atal'Utek | — | R=0 — | 95695 | time/E _needs_human |
| rep-95639 | Clear the Clutch | Vaults of Atal'Utek | — | R=0 — | 95639 | time/E _needs_human |
| rep-95640 | Clear the Clutch | Vaults of Atal'Utek | — | R=0 — | 95640 | time/E _needs_human |
| rep-95641 | Clear the Clutch | Vaults of Atal'Utek | — | R=0 — | 95641 | time/E _needs_human |
| rep-96528 | Prey: Anguish from Beyond | The Coiled Isle | 13690 XP; 34g | R=0 gold,xp | 96528 | time/E _needs_human |
| rep-91464 | Stormarion Assault | unknown | — | R=0 — | 91464 | time/E _needs_human |

## World-Boss (6)

| id | name | zone | rewards | value (R + goals) | questID | notes |
|---|---|---|---|---|---|---|
| rep-96717 | Showdown on Naigtal | Val / Naigtal (rotating) | Riftstalker's Cache [cosmetic, crafting, gearing, gold, vault]; 17110 XP | R=3 cosmetic,crafting,gearing,gold,vault,xp | 96717 | cadence:medium; value:medium; ⚠S1-frozen-loot; time/E _needs_human |
| rep-96713 | Showdown on Val | Val / Naigtal (rotating) | Riftstalker's Cache [cosmetic, crafting, gearing, gold, vault]; 17110 XP | R=3 cosmetic,crafting,gearing,gold,vault,xp | 96713 | cadence:medium; value:medium; ⚠S1-frozen-loot; time/E _needs_human |
| rep-92123 | Cragpine | Zul'Aman | Bramblestalker's Feathered Cowl (? 197); Dawncrazed Beast Cleaver (? 197); Devouring Outrider's Chausses (? 197); Forgotten Farstrider's Insignia (? 197); Host Commander's Casque (? 197); Radiant Eversong Scepter (? 197); 13690 XP | R=1 gearing,xp | 92123 | value:medium; time/E _needs_human |
| rep-92560 | Lu'ashal | Eversong Woods | Bramblestalker's Feathered Cowl (? 197); Dawncrazed Beast Cleaver (? 197); Devouring Outrider's Chausses (? 197); Forgotten Farstrider's Insignia (? 197); Host Commander's Casque (? 197); Radiant Eversong Scepter (? 197); 13690 XP | R=1 gearing,xp | 92560 | value:medium; time/E _needs_human |
| rep-92636 | Predaxas | Harandar | Bramblestalker's Feathered Cowl (? 197); Devouring Outrider's Chausses (? 197); Devouring Vanguard's Soulcleaver (? 197); Encroaching Shadow Signet (? 197); Forgotten Farstrider's Insignia (? 197); Host Commander's Casque (? 197); 13690 XP | R=1 gearing,xp | 92636 | value:medium; time/E _needs_human |
| rep-92034 | Thorm'belan | Harandar | Host Commander's Casque (? 197); Beastly Blossombarb (? 197); Blooming Thornblade (? 197); Bramblestalker's Feathered Cowl (? 197); Devouring Outrider's Chausses (? 197); Forgotten Farstrider's Insignia (? 197); 13690 XP | R=1 gearing,xp | 92034 | value:medium; time/E _needs_human |

## Unknown (2)

| id | name | zone | rewards | value (R + goals) | questID | notes |
|---|---|---|---|---|---|---|
| rep-96640 | Bounty of the Cursed | Vaults of Atal'Utek | Coffer Key Shards ×100; Zul'jarra's Forces ×50; 13690 XP; 34g | R=3 gearing,gold,vault,xp | 96640 | cadence:low; questID:medium; value:low; ⚠volatile-amount; time/E _needs_human |
| rep-89354 | Preparing for Battle | The Voidstorm | Honor ×500; Bloody Tokens ×150; Slayer's Duellum ×1000 | R=1 gearing | 89354 | cadence:low; value:medium; ⚠pre-season; time/E _needs_human |

## Pre-season & Season-2 gating (week of 2026-08-11)

12.1 shipped **2026-08-11**; **Midnight Season 2 opens 2026-08-18** (`_meta/changelog-12.1.md`). Every row below is either not currently available, or carries a reward the season change has moved. The tables above list them because they are catalogued repeatables — not because they are all completable today.

- **Preparing for Battle** (`89354`) — ⚠ **pre-season**: Voidstorm PvP turn-in — same S1-closed / S2-not-open gap as 93865.
- **A Call to Battle** (`93593`) — ⚠ **pre-season**: Season 2 PvP opens 2026-08-18 — unrated only this week, so the Conquest reward is not earnable yet.
- **Carve Your Way** (`93865`) — ⚠ **pre-season**: Voidstorm PvP turn-in — S1 PvP closed with the 08-11 maintenance and S2 opens 2026-08-18; treat the Honor/token payout as pre-season only.
- **A Nightmarish Task** (`94446`) — ⚠ **pre-season**: Nightmare mode is off this week — the S1 Prey weekly is dormant until 2026-08-18.
- **A Nightmarish Task** (`94446`) — ⚠ **S1-currency**: Hero **Dawncrest** is the Season 1 crest family; S2 crests are **Mistcrests** (moving-values.md). Whether the S2 version of this weekly pays a Mistcrest is not confirmed — do not read the scraped amount as a live S2 reward.
- **Bounty of the Cursed** (`96640`) — ⚠ **volatile-amount**: 12.1 "adjusted delve Coffer Key Shard amounts from multiple sources" and calls the tuning "still ongoing and a work in progress" (`_meta/patch-notes/12.1.md:1343-1344`; `_meta/moving-values.md`), so the scraped `×100` is a Wowhead number the Tier-1 feed does not confirm — read it as an order of magnitude, not a current value.
- **Showdown on Val** (`96713`) — ⚠ **S1-frozen-loot**: Val/Naigtal world-boss drops stay Season 1 items and can no longer be upgraded (12.1, "VAL AND NAIGTAL").
- **Showdown on Naigtal** (`96717`) — ⚠ **S1-frozen-loot**: Val/Naigtal world-boss drops stay Season 1 items and can no longer be upgraded (12.1, "VAL AND NAIGTAL").
- **Ritual Site Studies: Week 3 of 3** (`96730`) — ⚠ **pre-season**: the Tier 6 removal does **not** touch this Tier 1-3 chain, so the scraped `Nebulous Voidcore ×1` stands — but the payout is not spendable this week: Season 1 Voidcores **convert to gold at the end of S1 and may no longer be used in S1 content**, and Voidcore bonus rolls return only the **week of 2026-08-25**, and then only with **≥3 vault panes** unlocked (`_meta/patch-notes/12.1.md:1337-1338,1645`; `_meta/moving-values.md` row "Nebulous Voidcores — availability"). This row's **R=3 rests on that Voidcore**, so treat it as next-season value, not this week's.
- **Advanced Ritual Site Studies: Week 6 of 6** (`96733`) — ⚠ **Tier-1 override**: 12.1 removed the T6 Voidcore bonus roll; the reward was removed from this row before valuation, so R excludes it.

## Coiled Isle repeatables not yet in this catalog (12.1)

The 12.1 change ledger asks this file for the **Coiled Isle weeklies**. The zone's repeatable *systems* are Tier-1 confirmed, so they are named here rather than left as a silent hole — but their quests are **not** in the tables above, because on patch day Wowhead's pages for them carry neither `Type: Weekly|Daily` nor a recurring-turn-in icon (the coverage caveat below measures how big that hole is). **No cadence, quest ID, reward, or amount is asserted for any of them.** The zone's mechanics and currencies are written up in `knowledge/systems/coiled-isle.md`.

- **Curse Surges** — regularly spawn rare elites at **five rotating locations** across the isle (`_meta/patch-notes/12.1.md:99`).
- **Venom Fishing** — killing a Curse Surge rare elite **unlocks Venom Fishing at that location**; it comes with a local story for the tortollan sea captain **Tokka**, reputation with his crew, and fishing in more cursed waters around the isle (`:103`).
- **Vaults of Atal'Utek** — group content plus **rotating public events that build up to a boss fight** (`:87`).
- **Zul'jarra's Forces** — the isle's renown faction; quartermaster **Jan'sari the Watchful** at **Tokka's Landing** ([Coiled Isle preview](https://worldofwarcraft.com/en-us/news/24293963); `_meta/changelog-12.1.md`). Whether its renown turn-in exists as a discrete weekly quest is **unconfirmed** — the only catalogued row paying that currency today is `Bounty of the Cursed` (`96640`).

Curse Surges and the Vaults are **live during the pre-season week**, not Aug-18 content (`_meta/patch-notes/12.1.md:1613`).

## Caveats

- **Campaign gating.** Several repeatables unlock only after a story chain — notably the Shul'ka Li'tya **WANTED** board (Harandar): level 88 *and* Trials-of-the-Shul'ka campaign progress *and* a random daily roll. An empty board is expected, not a bug. See `knowledge/systems/leveling-notes.md`.
- **`_needs_human` fields.** `time_blocks` and `enjoyment_key` are placeholder defaults, not measured — tune before trusting the planner score.
- **Gear track** is a coarse ilvl-band guess (`track_confidence: low`); the Blizzard item API does not expose the upgrade track. Never asserted as fact. Bands are the real crest bands (`_meta/moving-values.md`): Season 2 **Mistcrests** 269-282-295-308-321-334, Season 1 **Dawncrests** 224-237-250-263-276-289, with `(S1)` appended below 269. An item under **224** sits below both ladders — leveling-era or pre-season gear — and gets **no** track label (`?`) rather than being flattened into "Adventurer".
- **Cadence** is best-effort (Wowhead `Type` + recurring icon + name); rows flag low/medium confidence.
- **Turn-in ≠ activity loot.** R values the *quest reward* only. For world-boss and Void-Assault rows the bigger prize is the boss/activity drop under its own lockout, which this model never sees — so their R is a floor, whatever it reads.
- **Container/cache rewards are R-floored.** When a quest rewards a *cache* (e.g. the Val/Naigtal Showdowns' Riftstalker's Cache), R + goals are derived from the item's description (which lists the contents), but the gear roll *inside* the cache is opaque to the API — so the shown R is a floor a real open can only beat.
- ⚠ **Coffer Key Shard rewards: the number is volatile and the `vault` goal is dormant this week.** Eight rows pay Coffer Key Shards — the seven Harandar **WANTED** dailies (unquantified in the scrape) and **Bounty of the Cursed** (`96640`, scraped at `×100`). Two things qualify them. (1) 12.1 "adjusted delve Coffer Key Shard amounts from multiple sources", weighted toward Coiled Isle content, and states the tuning is "still ongoing and a work in progress" (`_meta/patch-notes/12.1.md:1343-1344`; `_meta/moving-values.md` row "Delve Coffer Key Shards") — the Tier-1 feed publishes **no** shard number, so there is nothing to overwrite the scrape with and nothing that confirms it either. (2) During the pre-season week there are **no Bountiful Delves and Coffer Keys do not drop** — keys begin dropping with the 2026-08-18 maintenance (`_meta/moving-values.md` row "Delve rewards (pre-season)"; `_meta/patch-notes/12.1.md:1615`). Shards are what feed the keys that open the Bountiful chests these rows' `vault` tag is counting on, so that tag is **next-week value** and R over-states these rows for the week this file describes.
- ⚠ **Tier-1 patch notes outrank this scrape on rewards, and the override is applied, not just annotated.** Wowhead's quest pages lag a patch by days, so a scraped reward can be one the notes removed; `TIER1_REWARD_DROPS` (`tools/wowkb/repeatables.py`) strips those **before** valuation, so the removal reaches the reward column, **R**, and `repeatables.json` alike. Known 12.1 override: the **Tier 6 Advanced Ritual Site Studies** quests **no longer award a Nebulous Voidcore bonus roll** — they stay completable for the achievement ([12.1 notes](https://worldofwarcraft.com/en-us/news/24293281); `_meta/patch-notes/12.1.md`; `_meta/moving-values.md` row "Ritual Sites T6 bonus roll → Removed"). The note names the **Advanced** (Tier 6) chain only, so the **Tier 1-3 "Ritual Site Studies" quests (96728/96729/96730) keep their Voidcore** — the two families are one word apart, and only the *Advanced* one lost it. The override is **registered for all three** Advanced quests (96731/96732/96733) but the `⚠T1-override` tag marks only the row where it actually **fired**: 96731 and 96732 never scraped a Voidcore in the first place, so nothing was removed from them and they carry no tag. Read a missing tag as "the scrape was already clean", not as "the override skipped this row".
- ⚠ **Val/Naigtal world-boss rewards are frozen at Season 1.** Per 12.1, "the World Boss drops will remain as Season 1 drops and can no longer be upgraded" (the "Knocking off the Top (Heroic)" Mythic quest rewards likewise) — `_meta/patch-notes/12.1.md` (VAL AND NAIGTAL), `_meta/moving-values.md` row "World boss loot (Val/Naigtal …)". So the Showdown rows' gearing R is **last season's** gear at a dead end of the upgrade ladder, not S2 progression; the part that still advances you is the S2 crest payout (**Adventurer** in Normal World Tier, **Veteran** in Heroic), which is activity loot this quest-reward model does not see. The older Midnight world bosses (Lu'ashal / Thorm'belan / Predaxas / Cragpine) are not named by that note; their quest gear sits below every crest ladder regardless.
- ⚠ **12.1 Coiled Isle coverage is thin, by measurement.** The isle carries **167** level-90 quests across its zones in the Blizzard per-zone index (The Coiled Isle 124, Tokka's Landing 1, The Whispering Marsh 3, Vaults of Atal'Utek 36, The Venomous Abyss 3) — the same numbers as the Zone cross-check below — but on patch day Wowhead's pages for them carry no `Type: Weekly|Daily` and no recurring-turn-in icon, which are this scraper's two authorities on repeatability. Only rows with a daily-quest listview icon or a power-goal currency reward can be caught today. The Coiled Isle systems that are certainly repeatable but not yet classifiable are named in [Coiled Isle repeatables not yet in this catalog](#coiled-isle-repeatables-not-yet-in-this-catalog-121) above and described in full in `knowledge/systems/coiled-isle.md`. Widening the name-regex to catch them today would sweep the zone's Prey/Nightmare one-offs in with them, which is a scoping decision, not a scrape fix. **Re-run this scrape in a week.**

## questIDs to wire (verify in-game first) @verify-ingame

Candidate IDs for the planner's `weekly_quest` gate / PlannerState `ns.WEEKLY_QUESTS`. **Not auto-wired** — a wrong ID false-reports "done" (`weekly-checklist.md`). Confirm each in-game before adding.

- `92034` — Thorm'belan (world-boss, id-confidence high)
- `92123` — Cragpine (world-boss, id-confidence high)
- `92560` — Lu'ashal (world-boss, id-confidence high)
- `92636` — Predaxas (world-boss, id-confidence high)
- `93593` — A Call to Battle (weekly, id-confidence high)
- `93605` — The World Awaits (weekly, id-confidence high)
- `94385` — Void Assaults: Eversong Woods (weekly, id-confidence high)
- `94386` — Void Assaults: Zul'Aman (weekly, id-confidence high)
- `94446` — A Nightmarish Task (weekly, id-confidence high)
- `95416` — Going Postal (weekly, id-confidence high)
- `95438` — Lost Animals (weekly, id-confidence high)
- `96713` — Showdown on Val (world-boss, id-confidence high)
- `96717` — Showdown on Naigtal (world-boss, id-confidence high)
- `96728` — Ritual Site Studies: Week 1 of 3 (weekly, id-confidence medium)
- `96729` — Ritual Site Studies: Week 2 of 3 (weekly, id-confidence medium)
- `96730` — Ritual Site Studies: Week 3 of 3 (weekly, id-confidence medium)
- `96731` — Advanced Ritual Site Studies: Week 4 of 6 (weekly, id-confidence medium)
- `96732` — Advanced Ritual Site Studies: Week 5 of 6 (weekly, id-confidence medium)
- `96733` — Advanced Ritual Site Studies: Week 6 of 6 (weekly, id-confidence medium)

## Zone cross-check coverage

Blizzard `/data/wow/quest/area/{id}` per Midnight zone vs this catalog (quests in-zone but not catalogued are one-off/story quests or misses to spot-check):

- **Eversong Woods**: 0 catalogued of 219 zone quests
- **Harandar**: 7 catalogued of 194 zone quests
- **Isle of Quel'Danas**: 0 catalogued of 17 zone quests
- **Silvermoon City**: 1 catalogued of 68 zone quests
- **Sunstrider Isle**: 0 catalogued of 9 zone quests
- **The Coiled Isle**: 2 catalogued of 124 zone quests
- **The Venomous Abyss**: 0 catalogued of 3 zone quests
- **The Voidstorm**: 2 catalogued of 194 zone quests
- **The Whispering Marsh**: 0 catalogued of 3 zone quests
- **Tokka's Landing**: 0 catalogued of 1 zone quests
- **Vaults of Atal'Utek**: 1 catalogued of 36 zone quests
- **Zul'Aman**: 0 catalogued of 185 zone quests

## How this was generated / how to refresh

```bash
cd tools && uv run python -m wowkb.repeatables      # rewrites this file + repeatables.json
```

Pipeline: Wowhead listview harvest (`min-level:90/max-level:90`, Midnight-patch only) + curated KB seed (sub-90 repeatables the 1000-row cap drops) + Blizzard per-zone cross-check. Each candidate's Wowhead page confirms repeatability (recurring icon / `Type: Weekly|Daily`) and cadence; gear rewards resolve ilvl via the Blizzard item API. Rewards are valued by `rewards.value_quest`.

## Deferred follow-up — character-relative value

This catalog uses a **character-agnostic** baseline R. The reward valuation (`rewards.value_quest`) already accepts a `char_state` argument for **character-relative** scoring (gear scored by ilvl-delta to your weakest slot; currency by whether it advances an uncapped track) — implemented and unit-tested, but **not yet wired**. To finish it: feed `char_state` from `wowkb.character` (per-slot ilvl, renown, currencies) into `value_quest`, and add a `plan.py --include-repeatables` flag that merges `repeatables.json` and rescores with `char_state`. That realizes the planner's designed-but-unimplemented **v2b slot-targeting** (`scoring-model.md`).

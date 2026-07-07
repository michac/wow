---
title: Hunter Survival — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Hunter Survival — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Rejuvenating Wind | 385539 | 1 | PASSIVE | 2,2 | — | — |
| Survival of the Fittest | 264735 | 1 | ACTIVE | 2,4 | — | — |
| Posthaste | 109215 | 1 | PASSIVE | 2,6 | — | — |
| Natural Mending | 270581 | 2 | PASSIVE | 3,2 | — | 102381 |
| Padded Armor | 459450 | 1 | PASSIVE | 3,4 | — | 102422 |
| Hunter's Avoidance | 384799 | 1 | PASSIVE | 3,6 | — | 102411 |
| Wilderness Medicine | 343242 | 1 | PASSIVE | 4,1 | — | 102401 |
| Combat Experience | 1268871 | 1 | PASSIVE | 4,3 | — | 102406,102401 |
| Improved Aspect of the Cheetah | 1258407 | 1 | PASSIVE | 4,5 | — | 102423,102406 |
| Concussive Shot | 5116 | 1 | ACTIVE | 4,7 | — | 102423 |
| Precision Strikes | 1267003 | 1 | PASSIVE | 5,2 | — | 102383,110157 |
| Muzzle | 187707 | 1 | ACTIVE | 5,4 | — | 109485,110157 |
| Serrated Tips | 459502 | 2 | PASSIVE | 5,6 | — | 109485,102407 |
| Tranquilizing Shot | 19801 | 1 | ACTIVE | 6,1 | 8 | 102380 |
| Pathfinding | 378002 | 1 | PASSIVE | 6,3 | 8 | 102380,79837 |
| Disruptive Rounds | 343244 | 1 | PASSIVE | 6,4 | 8 | 79837 |
| Improved Feign Death | 1258486 | 2 | PASSIVE | 6,5 | 8 | 79837,102384 |
| Misdirection | 34477 | 1 | ACTIVE | 6,7 | 8 | 102384 |
| Kodo Tranquilizer / Devilsaur Tranquilizer | 459983 / 459991 | 1/1 | CHOICE | 7,1 | 8 | 109489 |
| Kindling Flare | 459506 | 1 | PASSIVE | 7,2 | 8 | 102404,109489 |
| Trigger Finger | 459534 | 2 | PASSIVE | 7,3 | 8 | 102404,102395 |
| Tar Trap / Scare Beast | 187698 / 1513 | 1/1 | CHOICE | 7,4 | 8 | 102395 |
| Touch of Grass | 1258402 | 2 | PASSIVE | 7,5 | 8 | 102395,109484 |
| Camouflage | 199483 | 1 | ACTIVE | 7,6 | 8 | 102419,109484 |
| No Hard Feelings | 459546 | 1 | PASSIVE | 7,7 | 8 | 102419 |
| Improved Aspect of the Turtle | 1258485 | 1 | PASSIVE | 8,2 | 8 | 102396,102425,102415 |
| Specialized Arsenal | 459542 | 1 | PASSIVE | 8,4 | 8 | 102396,102393,109487 |
| Scout's Instincts | 459455 | 1 | PASSIVE | 8,6 | 8 | 102412,109487,110156 |
| Shell Wall | 1267218 | 1 | PASSIVE | 9,1 | 23 | 102424 |
| Intimidation | 19577 | 1 | ACTIVE | 9,2 | 23 | 102424 |
| Improved Snaring | 1268868 | 1 | PASSIVE | 9,3 | 23 | 102390,102424 |
| Lone Survivor | 388039 | 1 | PASSIVE | 9,4 | 23 | 102390 |
| Catlike Reflexes | 1258404 | 1 | PASSIVE | 9,5 | 23 | 102390,109483 |
| Binding Shot | 109248 | 1 | ACTIVE | 9,6 | 23 | 109483 |
| Trailblazer / Moment of Opportunity | 199921 / 459488 | 1/1 | CHOICE | 9,7 | 23 | 109483 |
| Cold Feet | 1268671 | 1 | PASSIVE | 10,1 | 23 | 103989,110154 |
| Territorial Instincts / Guttural Roar | 459507 / 1258509 | 1/1 | CHOICE | 10,2 | 23 | 103989 |
| Born To Be Wild | 266921 | 2 | PASSIVE | 10,3 | 23 | 102414,102391,103989 |
| Keen Eyesight | 378004 | 2 | PASSIVE | 10,5 | 23 | 109488,109486,102391 |
| Tar-Coated Bindings / Horsehair Tether | 459460 / 472729 | 1/1 | CHOICE | 10,6 | 23 | 109488 |
| Improved Traps | 343247 | 1 | PASSIVE | 10,7 | 23 | 109488,110155 |
| Emergency Salve | 459517 | 1 | PASSIVE | 11,2 | 23 | 102416,110153 |
| Roar of Sacrifice / Guardian's Hide | 53480 / 1272094 | 1/1 | CHOICE | 11,4 | 23 | 102409,102416 |
| Unnatural Causes | 459527 | 1 | PASSIVE | 11,6 | 23 | 102409,102418 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Kill Command | 259489 | 1 | ACTIVE | 2,18 | — | — |
| Wildfire Bomb | 259495 | 1 | ACTIVE | 3,17 | — | 102255 |
| Raptor Strike | 186270 | 1 | ACTIVE | 3,19 | — | 102255 |
| Guerrilla Tactics | 264332 | 1 | PASSIVE | 4,17 | — | 102264 |
| Tip of the Spear | 260285 | 1 | PASSIVE | 4,19 | — | 102262 |
| Lunge | 378934 | 1 | PASSIVE | 5,16 | — | 102285 |
| Boomstick | 1261193 | 1 | ACTIVE | 5,18 | — | 102263,102285 |
| Strike as One | 1251717 | 1 | PASSIVE | 5,20 | — | 102263 |
| Shrapnel Bomb / Flamebreak | 1253172 / 1253176 | 1/1 | CHOICE | 6,15 | 8 | 102272 |
| Bloodseeker | 260248 | 1 | PASSIVE | 6,17 | 8 | 109324,102272 |
| Quick Reload | 1272136 | 1 | PASSIVE | 6,18 | 8 | 109324 |
| Flanker's Advantage | 459964 | 1 | PASSIVE | 6,19 | 8 | 109324,109321 |
| Two Against Many | 1251718 | 1 | PASSIVE | 6,21 | 8 | 109321 |
| Mongoose Fury | 1252708 | 1 | PASSIVE | 7,16 | 8 | 109309,102270 |
| Mongoose Rounds / Wildfire Shells | 1253945 / 1261229 | 1/1 | CHOICE | 7,17 | 8 | 110162 |
| Shellshock | 1252931 | 1 | PASSIVE | 7,19 | 8 | 110162 |
| Sic 'Em | 1253137 | 1 | PASSIVE | 7,20 | 8 | 110163,102279 |
| Bloody Claws / Wallop | 385737 / 1252738 | 1/1 | CHOICE | 8,15 | 8 | 109310 |
| Improved Wildfire Bomb | 321290 | 2 | PASSIVE | 8,16 | 8 | 109310 |
| Bonding | 1262442 | 1 | PASSIVE | 8,17 | 8 | 109310,109316 |
| Sweeping Spear | 378950 | 2 | PASSIVE | 8,18 | 8 | 109316,109319 |
| Vulnerability / Blackrock Munitions | 1257011 / 462036 | 1/1 | CHOICE | 8,19 | 8 | 109305,109319 |
| Shower of Blood | 1253053 | 2 | PASSIVE | 8,20 | 8 | 109305 |
| Outland Venom | 459939 | 1 | PASSIVE | 8,21 | 8 | 109305 |
| Explosives Expert | 378937 | 2 | PASSIVE | 9,16 | 20 | 102289,109311,109307 |
| Takedown | 1250646 | 1 | ACTIVE | 9,18 | 20 | 109311,109313,102282 |
| Killer Companion | 378955 | 2 | PASSIVE | 9,20 | 20 | 109304,109306,102282 |
| Flamefang Pitch | 1251592 | 1 | ACTIVE | 10,16 | 20 | 102281 |
| Twin Fangs | 1272139 | 1 | PASSIVE | 10,17 | 20 | 109323 |
| Savagery | 1251790 | 2 | PASSIVE | 10,19 | 20 | 109323 |
| Wildfire Infusion | 460198 | 1 | PASSIVE | 10,20 | 20 | 109312 |
| Grenade Juggler | 459843 | 1 | PASSIVE | 11,15 | 20 | 102252 |
| Wildfire Imbuement | 1252943 | 1 | PASSIVE | 11,17 | 20 | 102252 |
| Flanked | 1256938 | 1 | PASSIVE | 11,18 | 20 | 109320,109470 |
| Lethal Calibration | 1262409 | 1 | PASSIVE | 11,19 | 20 | 102268 |
| Primal Surge | 1272154 | 1 | PASSIVE | 11,21 | 20 | 102268 |
| Raptor Swipe | 1259003 | 1 | ACTIVE | 12,18 | 20 | — |

## Hero: Sentinel

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Sentinel | 1253599 | 1 | PASSIVE | 2,10 | — | — |
| Don't Look Back | 450373 | 1 | PASSIVE | 3,9 | — | 94976 |
| Moon's Blessing | 1253825 | 1 | PASSIVE | 3,10 | — | 94976 |
| Sanctified Armaments | 1253831 | 1 | PASSIVE | 3,11 | — | 94976 |
| Moonlight Chakram | 1264902 | 1 | PASSIVE | 3,12 | — | 94976 |
| Stargazer / Open Fire | 1253751 / 1253807 | 1/1 | CHOICE | 4,9 | — | 94989 |
| Can't Miss, Won't Miss | 1253830 | 1 | PASSIVE | 4,10 | — | 94973 |
| Invigorating Pulse | 450379 | 1 | PASSIVE | 4,11 | — | 94981 |
| Twilight Requiem / Stalk and Strike | 1264904 / 1266069 | 1/1 | CHOICE | 4,12 | — | 109807 |
| Arcane Talons | 1253846 | 1 | PASSIVE | 5,9 | — | 94958 |
| Lunar Calling | 1253852 | 1 | PASSIVE | 5,10 | — | 94990 |
| Conditioning / Scout's Vigil | 1253887 / 1253892 | 1/1 | CHOICE | 5,11 | — | 94971 |
| Radiant Edge | 1264903 | 1 | PASSIVE | 5,12 | — | 110028 |
| Lunar Storm | 1253732 | 1 | PASSIVE | 6,10 | — | 94980,94965,94970,109805 |

## Hero: Pack Leader

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Howl of the Pack Leader | 471876 | 1 | PASSIVE | 7,10 | — | — |
| Pack Mentality | 472358 | 1 | PASSIVE | 8,9 | — | 94991 |
| Dire Summons | 472352 | 1 | PASSIVE | 8,10 | — | 94991 |
| Better Together | 472357 | 1 | PASSIVE | 8,11 | — | 94991 |
| Slicked Shoes / Masterful Call | 472719 / 1268705 | 1/1 | CHOICE | 8,12 | — | 94991 |
| Ursine Fury / Sharpened Claws | 472476 / 472524 | 1/1 | CHOICE | 9,9 | — | 94985 |
| Fury of the Wyvern | 472550 | 1 | PASSIVE | 9,10 | — | 94992 |
| Hogstrider | 472639 | 1 | PASSIVE | 9,11 | — | 94962 |
| Lethal Barbs | 1264781 | 1 | PASSIVE | 9,12 | — | 94979 |
| No Mercy | 472660 | 1 | PASSIVE | 10,9 | — | 94972 |
| Shell Cover | 472707 | 1 | PASSIVE | 10,10 | — | 94984 |
| Hoof and Blade / Wyvern's Gaze | 1264797 / 1264792 | 1/1 | CHOICE | 10,11 | — | 94988 |
| Sharpened Fangs | 1264775 | 1 | PASSIVE | 10,12 | — | 109803 |
| Stampede! | 472741 | 1 | PASSIVE | 11,10 | — | 94967,94969,109804,109802 |

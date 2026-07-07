---
title: Hunter Beast Mastery — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Hunter Beast Mastery — talents (12.0.7)

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
| Counter Shot | 147362 | 1 | ACTIVE | 5,4 | — | 109485,110157 |
| Serrated Tips | 459502 | 2 | PASSIVE | 5,6 | — | 109485,102407 |
| Tranquilizing Shot | 19801 | 1 | ACTIVE | 6,1 | 8 | 102380 |
| Pathfinding | 378002 | 1 | PASSIVE | 6,3 | 8 | 102292,102380 |
| Disruptive Rounds | 343244 | 1 | PASSIVE | 6,4 | 8 | 102292 |
| Improved Feign Death | 1258486 | 2 | PASSIVE | 6,5 | 8 | 102384,102292 |
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
| Cold Feet | 1268671 | 1 | PASSIVE | 10,1 | 23 | 102397,110154 |
| Territorial Instincts / Guttural Roar | 459507 / 1258509 | 1/1 | CHOICE | 10,2 | 23 | 102397 |
| Born To Be Wild | 266921 | 2 | PASSIVE | 10,3 | 23 | 102397,102414,102391 |
| Keen Eyesight | 378004 | 2 | PASSIVE | 10,5 | 23 | 109488,109486,102391 |
| Tar-Coated Bindings / Horsehair Tether | 459460 / 472729 | 1/1 | CHOICE | 10,6 | 23 | 109488 |
| Improved Traps | 343247 | 1 | PASSIVE | 10,7 | 23 | 109488,110155 |
| Emergency Salve | 459517 | 1 | PASSIVE | 11,2 | 23 | 102416,110153 |
| Roar of Sacrifice / Guardian's Hide | 53480 / 1272094 | 1/1 | CHOICE | 11,4 | 23 | 102409,102416 |
| Unnatural Causes | 459527 | 1 | PASSIVE | 11,6 | 23 | 102409,102418 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Kill Command | 34026 | 1 | ACTIVE | 2,18 | — | — |
| Animal Companion / Solitary Companion | 267116 / 474746 | 1/1 | CHOICE | 3,17 | — | 102346 |
| Barbed Shot | 217200 | 1 | ACTIVE | 3,19 | — | 102346 |
| Alpha Predator | 269737 | 1 | PASSIVE | 4,16 | — | 110158 |
| Dire Beast | 120679 | 1 | PASSIVE | 4,17 | — | 110158 |
| Stomp | 199530 | 1 | PASSIVE | 4,19 | — | 102377 |
| War Orders | 393933 | 1 | PASSIVE | 4,20 | — | 102377 |
| Wild Thrash | 1264359 | 1 | ACTIVE | 5,16 | — | 102368,102376 |
| Bestial Wrath | 19574 | 1 | ACTIVE | 5,18 | — | 102347,102376 |
| Cobra Shot | 193455 | 1 | ACTIVE | 5,20 | — | 102343,102347 |
| Beast Cleave | 115939 | 1 | PASSIVE | 6,16 | 8 | 102363 |
| Scent of Blood | 193532 | 1 | PASSIVE | 6,17 | 8 | 102340 |
| Thundering Hooves | 459693 | 1 | PASSIVE | 6,19 | 8 | 102340 |
| Go for the Throat | 459550 | 1 | PASSIVE | 6,20 | 8 | 102354 |
| Laceration | 459552 | 1 | PASSIVE | 7,15 | 8 | 102341 |
| Kill Cleave | 378207 | 1 | PASSIVE | 7,16 | 8 | 102341 |
| Training Expert | 378209 | 2 | PASSIVE | 7,17 | 8 | 102342,102341 |
| The Beast Within | 231548 | 1 | PASSIVE | 7,18 | 8 | 102342,102370 |
| Thrill of the Hunt | 1265051 | 2 | PASSIVE | 7,19 | 8 | 102357,102370 |
| Pack Tactics | 321014 | 1 | PASSIVE | 7,20 | 8 | 102357 |
| Barbed Scales | 469880 | 1 | PASSIVE | 7,21 | 8 | 102357 |
| Aspect of the Beast | 191384 | 1 | PASSIVE | 8,15 | 8 | 102369 |
| Dire Cleave | 1217524 | 1 | PASSIVE | 8,16 | 8 | 102369,102355,102338 |
| Dire Command | 378743 | 1 | PASSIVE | 8,17 | 8 | 102338,102373 |
| Jagged Wounds | 1265044 | 1 | PASSIVE | 8,19 | 8 | 102345,102373 |
| Serpentine Strikes | 468701 | 1 | PASSIVE | 8,20 | 8 | 102353,102374,102345 |
| Snakeskin Quiver / Cobra Senses | 468695 / 378244 | 1/1 | CHOICE | 8,21 | 8 | 102353 |
| Dire Frenzy | 385810 | 2 | PASSIVE | 9,16 | 20 | 102351,102365,102337 |
| Frenzy | 1264934 | 2 | PASSIVE | 9,18 | 20 | 102358,102365 |
| Killer Instinct | 273887 | 2 | PASSIVE | 9,20 | 20 | 102344,102372,102358 |
| Brutal Companion | 386870 | 1 | PASSIVE | 10,15 | 20 | 102367 |
| Huntmaster's Call | 459730 | 1 | PASSIVE | 10,16 | 20 | 102367 |
| Heart of the Pack | 1265052 | 1 | PASSIVE | 10,17 | 20 | 102336,102367 |
| Bloodshed | 1272099 | 1 | PASSIVE | 10,18 | 20 | 102336 |
| Savagery | 424557 | 1 | PASSIVE | 10,19 | 20 | 102336,102364 |
| Killer Cobra | 199532 | 1 | PASSIVE | 10,20 | 20 | 102364 |
| Master Handler | 424558 | 1 | PASSIVE | 10,21 | 20 | 102364 |
| Wildspeaker | 1232739 | 1 | PASSIVE | 11,16 | 20 | 107286,102350 |
| Wild Instincts / Bloody Frenzy | 378442 / 407412 | 1/1 | CHOICE | 11,18 | 20 | 102362 |
| Piercing Fangs | 392053 | 1 | PASSIVE | 11,20 | 20 | 102375,102359 |
| Nature's Ally | 1273043 | 1 | ACTIVE | 12,18 | 20 | — |

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

## Hero: Dark Ranger

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Black Arrow | 466932 | 1 | PASSIVE | 2,10 | — | — |
| Black Arrow | 466930 | 1 | ACTIVE | 2,10 | — | — |
| Bleak Arrows | 467749 | 1 | PASSIVE | 3,9 | — | 94987,109961 |
| Soul Drinker | 469638 | 1 | PASSIVE | 3,10 | — | 94987,109961 |
| Bleak Powder | 467911 | 1 | PASSIVE | 3,11 | — | 94987,109961 |
| Corpsecaller | 1264289 | 1 | PASSIVE | 3,12 | — | 109961,94987 |
| Ebon Bowstring / Through the Eyes | 467897 / 1277565 | 1/1 | CHOICE | 4,9 | — | 94961 |
| Smoke Screen | 430709 | 1 | PASSIVE | 4,10 | — | 94968 |
| Dark Chains / Shadow Dagger | 430712 / 467741 | 1/1 | CHOICE | 4,11 | — | 94974 |
| Wailing Dead | 1264290 | 1 | PASSIVE | 4,12 | — | 109801 |
| Blighted Quiver | 1264291 | 1 | PASSIVE | 5,9 | — | 94986 |
| Banshee's Mark / The Bell Tolls | 467902 / 467644 | 1/1 | CHOICE | 5,10 | — | 94959 |
| Umbral Reach | 1235397 | 1 | PASSIVE | 5,11 | — | 94960 |
| Pact of the Hollow | 1264690 | 1 | PASSIVE | 5,12 | — | 109800 |
| Withering Fire | 466990 | 1 | PASSIVE | 6,10 | — | 94982,109799,94957,94983 |

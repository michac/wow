---
title: Hunter Marksmanship — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-18
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Hunter Marksmanship — talents (12.0.7)

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
| Pathfinding | 378002 | 1 | PASSIVE | 6,3 | 8 | 102380,102402 |
| Disruptive Rounds | 343244 | 1 | PASSIVE | 6,4 | 8 | 102402 |
| Improved Feign Death | 1258486 | 2 | PASSIVE | 6,5 | 8 | 102384,102402 |
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
| Intimidation | 474421 | 1 | ACTIVE | 9,2 | 23 | 102424 |
| Improved Snaring | 1268868 | 1 | PASSIVE | 9,3 | 23 | 102390,102424 |
| Lone Survivor | 388039 | 1 | PASSIVE | 9,4 | 23 | 102390 |
| Catlike Reflexes | 1258404 | 1 | PASSIVE | 9,5 | 23 | 102390,109483 |
| Binding Shot | 109248 | 1 | ACTIVE | 9,6 | 23 | 109483 |
| Trailblazer / Moment of Opportunity | 199921 / 459488 | 1/1 | CHOICE | 9,7 | 23 | 109483 |
| Cold Feet | 1268671 | 1 | PASSIVE | 10,1 | 23 | 103990,110154 |
| Territorial Instincts / Guttural Roar | 459507 / 1258509 | 1/1 | CHOICE | 10,2 | 23 | 103990 |
| Born To Be Wild | 266921 | 2 | PASSIVE | 10,3 | 23 | 102414,102391,103990 |
| Keen Eyesight | 378004 | 2 | PASSIVE | 10,5 | 23 | 109488,109486,102391 |
| Tar-Coated Bindings / Horsehair Tether | 459460 / 472729 | 1/1 | CHOICE | 10,6 | 23 | 109488 |
| Improved Traps | 343247 | 1 | PASSIVE | 10,7 | 23 | 109488,110155 |
| Emergency Salve | 459517 | 1 | PASSIVE | 11,2 | 23 | 102416,110153 |
| Roar of Sacrifice / Guardian's Hide | 53480 / 1272094 | 1/1 | CHOICE | 11,4 | 23 | 102409,102416 |
| Unnatural Causes | 459527 | 1 | PASSIVE | 11,6 | 23 | 102409,102418 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Aimed Shot | 19434 | 1 | ACTIVE | 2,18 | — | — |
| Rapid Fire | 257044 | 1 | ACTIVE | 3,17 | — | 103982 |
| Precise Shots | 260240 | 1 | PASSIVE | 3,19 | — | 103982 |
| Quick Draw | 459794 | 1 | PASSIVE | 4,17 | — | 103961 |
| Lock and Load | 194595 | 1 | PASSIVE | 4,19 | — | 103977 |
| Surging Shots | 391559 | 1 | PASSIVE | 5,16 | — | 103975 |
| Avian Specialization / Unbreakable Bond | 466867 / 1223323 | 1/1 | CHOICE | 5,18 | — | 103975,107289 |
| Trick Shots / Aspect of the Hydra | 257621 / 470945 | 1/1 | CHOICE | 5,20 | — | 107289 |
| Obsidian Arrowhead / On Target | 471350 / 471348 | 1/1 | CHOICE | 6,15 | 8 | 104130 |
| Penetrating Shots | 459783 | 1 | PASSIVE | 6,17 | 8 | 104127,104130 |
| Tenacious / Cunning | 474456 / 474440 | 1/1 | CHOICE | 6,18 | 8 | 104127 |
| Master Marksman | 260309 | 1 | PASSIVE | 6,19 | 8 | 104127,103957 |
| Light Ammo | 378913 | 1 | PASSIVE | 6,21 | 8 | 103957 |
| Kill Shot | 53351 | 1 | ACTIVE | 7,16 | 8 | 103964,103959 |
| No Scope | 473385 | 1 | PASSIVE | 7,17 | 8 | 103986,103964 |
| Trueshot | 288613 | 1 | ACTIVE | 7,18 | 8 | 103986 |
| Critical Precision | 1277572 | 1 | PASSIVE | 7,19 | 8 | 103974,103986 |
| Explosive Shot | 212431 | 1 | ACTIVE | 7,20 | 8 | 107288,103974 |
| Deathblow | 343248 | 1 | PASSIVE | 8,15 | 8 | 109490 |
| Headshot / Deadeye | 471363 / 321460 | 1/1 | CHOICE | 8,16 | 8 | 109490 |
| Bullseye | 204089 | 1 | PASSIVE | 8,17 | 8 | 109490,110572,103947 |
| Feathered Frenzy | 470943 | 1 | PASSIVE | 8,18 | 8 | 103947 |
| Small Game Hunter | 459802 | 1 | PASSIVE | 8,19 | 8 | 110575,103955,103947 |
| Precision Detonation | 471369 | 1 | PASSIVE | 8,20 | 8 | 110575 |
| Shrapnel Shot | 473520 | 1 | PASSIVE | 8,21 | 8 | 110575 |
| Unmatched Precision | 1232955 | 2 | PASSIVE | 9,16 | 20 | 103985,103972,109491 |
| Calling the Shots / Unerring Vision | 260404 / 474738 | 1/1 | CHOICE | 9,18 | 20 | 103984 |
| Eagle's Accuracy | 473369 | 2 | PASSIVE | 9,20 | 20 | 103978,110574,110573 |
| Focused Aim | 378767 | 1 | PASSIVE | 10,15 | 20 | 103950 |
| Bulletstorm | 389019 | 1 | PASSIVE | 10,17 | 20 | 103958,103950 |
| Tensile Bowstring | 471366 | 1 | PASSIVE | 10,18 | 20 | 103958 |
| Volley | 260243 | 1 | ACTIVE | 10,19 | 20 | 103958,103973 |
| Focus Fire | 1277546 | 1 | PASSIVE | 10,21 | 20 | 103973 |
| Windrunner Quiver | 473523 | 1 | PASSIVE | 11,15 | 20 | 103987 |
| Incendiary Ammunition | 471428 | 1 | PASSIVE | 11,17 | 20 | 103962 |
| Double Tap | 473370 | 1 | PASSIVE | 11,18 | 20 | 103956,103962,103966 |
| Salvo | 400456 | 1 | PASSIVE | 11,19 | 20 | 103956 |
| Unload | 1277548 | 1 | PASSIVE | 11,21 | 20 | 103979 |
| Take Aim | 1273132 | 1 | ACTIVE | 12,18 | 20 | — |

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

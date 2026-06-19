---
title: Paladin Retribution — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Paladin Retribution — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Lay on Hands | 633 | 1 | ACTIVE | 2,2 | — | — |
| Auras of the Resolute | 385633 | 1 | ACTIVE | 2,4 | — | — |
| Hammer of Wrath | 1241288 | 1 | PASSIVE | 2,6 | — | — |
| Cleanse Toxins | 213644 | 1 | ACTIVE | 3,1 | — | 81597 |
| Empyreal Ward | 387791 | 1 | PASSIVE | 3,2 | — | 81597 |
| Fist of Justice | 234299 | 1 | PASSIVE | 3,3 | — | 81600,81597 |
| Blinding Light | 115750 | 1 | ACTIVE | 3,5 | — | 81510,81600 |
| Turn Evil | 10326 | 1 | ACTIVE | 3,7 | — | 81510 |
| A Just Reward | 469411 | 2 | PASSIVE | 4,1 | — | 81507 |
| Afterimage / Healing Hands | 385414 / 326734 | 1/1 | CHOICE | 4,2 | — | 81507,103859,109999 |
| Guided Prayer | 404357 | 1 | PASSIVE | 4,3 | — | 109999 |
| Divine Steed | 190784 | 1 | ACTIVE | 4,4 | — | 81598,81600,109999 |
| Light's Countenance | 469325 | 1 | PASSIVE | 4,5 | — | 81598 |
| Greater Judgment | 231663 | 1 | PASSIVE | 4,6 | — | 81510,81598 |
| Wrench Evil / Stand Against Evil | 460720 / 469317 | 1/1 | CHOICE | 4,7 | — | 93010 |
| Holy Reprieve | 469445 | 1 | PASSIVE | 5,1 | — | 93189,103858 |
| Shield of Vengeance | 1261562 | 1 | PASSIVE | 5,2 | — | 110012,93189 |
| Cavalier | 230332 | 1 | PASSIVE | 5,3 | — | 81632 |
| Divine Spurs | 469409 | 1 | PASSIVE | 5,4 | — | 81632 |
| Steed of Liberty / Blessing of Freedom | 469304 / 1044 | 1/1 | CHOICE | 5,5 | — | 81632 |
| Rebuke | 96231 | 1 | ACTIVE | 5,7 | — | 103855,81603 |
| Obduracy | 385427 | 2 | PASSIVE | 6,2 | 8 | 81605,103860,109867 |
| Divine Toll | 375576 | 1 | ACTIVE | 6,4 | 8 | 81631,81605 |
| Unbound Freedom | 305394 | 1 | PASSIVE | 6,5 | 8 | 81631 |
| Sanctified Plates | 402964 | 2 | PASSIVE | 6,6 | 8 | 110093,81631,81603 |
| Punishment | 403530 | 1 | PASSIVE | 6,7 | 8 | 110093 |
| Divine Reach | 469476 | 1 | PASSIVE | 7,1 | 8 | 103860,81630 |
| Brought to Light | 1265549 | 1 | PASSIVE | 7,2 | 8 | 81630 |
| Blessing of Sacrifice | 6940 | 1 | ACTIVE | 7,3 | 8 | 109368,81605,81630 |
| Divine Resonance / Quickened Invocation | 384027 / 379391 | 1/1 | CHOICE | 7,4 | 8 | 109368 |
| Blessing of Protection | 1022 | 1 | ACTIVE | 7,5 | 8 | 109368,93174,93009 |
| Fear No Evil | 1265541 | 1 | PASSIVE | 7,6 | 8 | 93009 |
| Consecrated Ground | 204054 | 1 | PASSIVE | 7,7 | 8 | 110091,93009 |
| Holy Aegis | 385515 | 1 | PASSIVE | 8,2 | 8 | 93168,81614,109998 |
| Sacrifice of the Just / Recompense | 384820 / 384914 | 1/1 | CHOICE | 8,3 | 8 | 81614 |
| Sacred Strength / Divine Purpose | 469337 / 408459 | 1/1 | CHOICE | 8,4 | 8 | 81616,81614 |
| Improved Blessing of Protection | 384909 | 1 | PASSIVE | 8,5 | 8 | 81616 |
| Unbreakable Spirit | 114154 | 1 | PASSIVE | 8,6 | 8 | 81543,81616,109997 |
| Lightforged Blessing | 403479 | 1 | PASSIVE | 9,1 | 23 | 93168,81609 |
| Lead the Charge | 469780 | 1 | PASSIVE | 9,2 | 23 | 81609,81607 |
| Worthy Sacrifice / Righteous Protection | 469279 / 469321 | 1/1 | CHOICE | 9,3 | 23 | 81607 |
| Holy Ritual | 199422 | 1 | PASSIVE | 9,4 | 23 | 81618,81607 |
| Blessed Calling | 469770 | 1 | PASSIVE | 9,5 | 23 | 81617,81618 |
| Inspired Guard | 469439 | 1 | PASSIVE | 9,6 | 23 | 81617,81615 |
| Light's Revocation | 146956 | 1 | PASSIVE | 9,7 | 23 | 81615,81543 |
| Faith's Armor | 406101 | 1 | PASSIVE | 10,1 | 23 | 93008,103867 |
| Stoicism | 469316 | 1 | PASSIVE | 10,2 | 23 | 103867 |
| Seal of Might | 385450 | 2 | PASSIVE | 10,3 | 23 | 103866,103865,103867 |
| Vengeful Wrath | 1241958 | 2 | PASSIVE | 10,5 | 23 | 103866,103864,103868 |
| Eye for an Eye | 469309 | 1 | PASSIVE | 10,6 | 23 | 103864 |
| Golden Path / Selfless Healer | 377128 / 469434 | 1/1 | CHOICE | 10,7 | 23 | 103864,81608 |
| Blessing of Dawn | 183416 | 1 | PASSIVE | 11,2 | 23 | 81495,81621,103862 |
| Lightbearer | 469416 | 1 | PASSIVE | 11,4 | 23 | 103851,81621 |
| Blessing of Dusk | 1241945 | 1 | PASSIVE | 11,6 | 23 | 103851,103856,81628 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Blade of Justice | 184575 | 1 | ACTIVE | 2,18 | — | — |
| Divine Storm | 53385 | 1 | ACTIVE | 3,17 | — | 81526 |
| Expurgation | 383344 | 1 | PASSIVE | 3,19 | — | 81526 |
| Swift Justice / Light of Justice | 383228 / 404436 | 1/1 | CHOICE | 4,17 | — | 81527 |
| Judgment of Justice | 403495 | 1 | PASSIVE | 4,18 | — | 92689,81527 |
| Avenging Wrath | 31884 | 1 | ACTIVE | 4,19 | — | 92689 |
| Final Verdict | 383328 | 1 | ACTIVE | 5,16 | — | 81521 |
| Improved Blade of Justice / Holy Blade | 403745 / 383342 | 1/1 | CHOICE | 5,18 | — | 81544,81521,93161 |
| Righteous Cause / Art of War | 402912 / 406064 | 1/1 | CHOICE | 5,20 | — | 81544 |
| Jurisdiction | 402971 | 1 | PASSIVE | 6,15 | 8 | 81532 |
| Tempest of the Lightbringer | 383396 | 1 | PASSIVE | 6,17 | 8 | 92838,81532 |
| Rush of Light | 407067 | 1 | PASSIVE | 6,18 | 8 | 92838 |
| Sanctify | 382536 | 1 | PASSIVE | 6,19 | 8 | 81523,92838 |
| Holy Flames | 406545 | 1 | PASSIVE | 6,21 | 8 | 81523 |
| Improved Judgment / Boundless Judgment | 405461 / 405278 | 1/1 | CHOICE | 7,16 | 8 | 81542,81532,109372 |
| Zealot's Fervor | 403509 | 2 | PASSIVE | 7,17 | 8 | 81512,109372 |
| Heart of the Crusader | 406154 | 2 | PASSIVE | 7,19 | 8 | 81512,109370 |
| Blade of Vengeance | 403826 | 1 | PASSIVE | 7,20 | 8 | 109370,109371,81523 |
| Empyrean Power | 326732 | 1 | PASSIVE | 8,15 | 8 | 81533,81542 |
| Highlord's Wrath | 404512 | 1 | PASSIVE | 8,17 | 8 | 81533,92952 |
| Templar Strikes / Crusading Strikes | 406646 / 404542 | 1/1 | CHOICE | 8,18 | 8 | 93190,92952 |
| Blessed Champion | 403010 | 1 | PASSIVE | 8,19 | 8 | 81545,93190 |
| Burning Crusade | 403026 | 1 | PASSIVE | 8,21 | 8 | 109371,81545 |
| Blades of Light | 403664 | 2 | PASSIVE | 9,16 | 20 | 81534,92860 |
| Wake of Ashes | 255937 | 1 | ACTIVE | 9,18 | 20 | 81541,109374,81534 |
| Divine Wrath | 406872 | 2 | PASSIVE | 9,20 | 20 | 92839,81541 |
| Execution Sentence | 343527 | 1 | ACTIVE | 10,16 | 20 | 93164 |
| Seething Flames | 405355 | 1 | PASSIVE | 10,18 | 20 | 81525 |
| Empyrean Legacy | 387170 | 1 | PASSIVE | 10,20 | 20 | 93160 |
| Judge, Jury and Executioner | 406157 | 1 | PASSIVE | 11,16 | 20 | 109373 |
| Radiant Glory | 458359 | 1 | PASSIVE | 11,17 | 20 | 92854 |
| Burn to Ash | 446663 | 1 | PASSIVE | 11,19 | 20 | 92854 |
| Crusade | 1253598 | 1 | PASSIVE | 11,20 | 20 | 93173 |
| Light Within | 1261113 | 1 | ACTIVE | 12,18 | 20 | — |

## Hero: Templar

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Light's Guidance | 427445 | 1 | PASSIVE | 1,23 | — | — |
| Zealous Vindication | 431463 | 1 | PASSIVE | 2,21 | — | 95180 |
| Shake the Heavens | 431533 | 1 | PASSIVE | 2,22 | — | 95180 |
| Wrathful Descent | 431551 | 1 | PASSIVE | 2,23 | — | 95180 |
| Divine Hammer | 432929 | 1 | PASSIVE | 2,24 | — | 95180 |
| Sacrosanct Crusade | 431730 | 1 | PASSIVE | 3,21 | — | 95183 |
| Higher Calling | 431687 | 1 | PASSIVE | 3,22 | — | 95187 |
| Bonds of Fellowship / Unrelenting Charger | 432992 / 432990 | 1/1 | CHOICE | 3,23 | — | 95177 |
| Light's Judicator | 1261525 | 1 | PASSIVE | 3,24 | — | 109747 |
| Endless Wrath / Sanctification | 432615 / 432977 | 1/1 | CHOICE | 4,21 | — | 95179 |
| Hammerfall | 432463 | 1 | PASSIVE | 4,22 | — | 95178 |
| Undisputed Ruling | 432626 | 1 | PASSIVE | 4,23 | — | 95181 |
| Divine Exaction / Seal of the Templar | 1260429 / 1263252 | 1/1 | CHOICE | 4,24 | — | 109746 |
| Light's Deliverance | 425518 | 1 | PASSIVE | 5,23 | — | 95186,95184,95185,109745 |

## Hero: Herald of the Sun

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Dawnlight | 431377 | 1 | PASSIVE | 2,11 | — | — |
| Morning Star / Gleaming Rays | 431482 / 431480 | 1/1 | CHOICE | 3,9 | — | 95099 |
| Eternal Flame | 156322 | 1 | ACTIVE | 3,10 | — | 95099 |
| Luminosity | 431402 | 1 | PASSIVE | 3,11 | — | 95099 |
| Endless Gleam | 1263787 | 1 | PASSIVE | 3,12 | — | 95099 |
| Illumine / Will of the Dawn | 431423 / 431406 | 1/1 | CHOICE | 4,9 | — | 95073 |
| Blessing of An'she / Lingering Radiance | 445200 / 431407 | 1/1 | CHOICE | 4,10 | — | 95095 |
| Sun Sear | 431413 | 1 | PASSIVE | 4,11 | — | 95080 |
| Solar Grace | 431404 | 1 | PASSIVE | 4,12 | — | 109748 |
| Aurora | 439760 | 1 | PASSIVE | 5,9 | — | 95098 |
| Walk Into Light | 1263782 | 1 | PASSIVE | 5,10 | — | 95071 |
| Second Sunrise | 431474 | 1 | PASSIVE | 5,11 | — | 95072 |
| Born in Sunlight | 1263920 | 1 | PASSIVE | 5,12 | — | 109750 |
| Sun's Avatar | 431425 | 1 | PASSIVE | 6,11 | — | 95086,95094,95069,109749 |

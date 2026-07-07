---
title: Druid Guardian — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Druid Guardian — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Rake | 1822 | 1 | ACTIVE | 2,3 | — | — |
| Frenzied Regeneration | 22842 | 1 | ACTIVE | 2,5 | — | — |
| Rejuvenation | 774 | 1 | ACTIVE | 2,7 | — | — |
| Starfire | 197628 | 1 | ACTIVE | 2,9 | — | — |
| Starfire | 197628 | 1 | ACTIVE | 2,9 | — | — |
| Grievous Wounds | 474526 | 1 | PASSIVE | 3,2 | — | 82199 |
| Swipe | 213764 | 1 | ACTIVE | 3,4 | — | 82220,82199 |
| Ursoc's Spirit | 449182 | 1 | PASSIVE | 3,6 | — | 82217,82220 |
| Wild Growth | 48438 | 1 | ACTIVE | 3,8 | — | 82217 |
| Starsurge | 197626 | 1 | ACTIVE | 3,10 | — | 91044 |
| Rip | 1079 | 1 | ACTIVE | 4,3 | — | 82199 |
| Verdant Heart | 301768 | 1 | PASSIVE | 4,5 | — | 82219,82223,82220 |
| Remove Corruption | 2782 | 1 | ACTIVE | 4,7 | — | 82217,82219 |
| Moonkin Form | 24858 | 1 | ACTIVE | 4,9 | — | 91044 |
| Moonkin Form | 197625 | 1 | ACTIVE | 4,9 | — | — |
| Maim | 22570 | 1 | ACTIVE | 5,2 | — | 82222 |
| Killer Instinct | 108299 | 2 | PASSIVE | 5,4 | — | 82222,82223,82218 |
| Ironfur | 192081 | 1 | ACTIVE | 5,5 | — | 82218 |
| Improved Barkskin | 327993 | 1 | PASSIVE | 5,6 | — | 82219,82218,82241 |
| Hibernate | 2637 | 1 | ACTIVE | 5,7 | — | 82241 |
| Nurturing Instinct | 33873 | 2 | PASSIVE | 5,8 | — | 91047,82205,82208,82241 |
| Sunfire | 93402 | 1 | ACTIVE | 5,10 | — | 82208 |
| Primal Fury | 159286 | 1 | PASSIVE | 6,3 | 8 | 82225 |
| Thick Hide | 16931 | 1 | PASSIVE | 6,5 | 8 | 82225,104085 |
| Skull Bash | 106839 | 1 | ACTIVE | 6,6 | 8 | 104085 |
| Natural Recovery | 377796 | 1 | PASSIVE | 6,7 | 8 | 82214,104085,82211 |
| Astral Influence | 197524 | 1 | PASSIVE | 6,9 | 8 | 82214 |
| Wild Charge / Tiger Dash | 102401 / 252216 | 1/1 | CHOICE | 7,4 | 8 | 82225,82228 |
| Soothe / Cyclone | 2908 / 33786 | 1/1 | CHOICE | 7,6 | 8 | 82206,82228 |
| Aessina's Renewal | 474678 | 1 | PASSIVE | 7,8 | 8 | 82214,82206 |
| Starlight Conduit | 451211 | 1 | PASSIVE | 7,10 | 8 | 82210,93714 |
| Feline Swiftness | 131768 | 1 | PASSIVE | 8,3 | 8 | 82198 |
| Well-Honed Instincts | 377847 | 1 | PASSIVE | 8,4 | 8 | 82198 |
| Matted Fur | 385786 | 2 | PASSIVE | 8,5 | 8 | 82228,82198 |
| Stampeding Roar | 106898 | 1 | ACTIVE | 8,6 | 8 | 82229 |
| Lingering Healing | 231040 | 1 | PASSIVE | 8,7 | 8 | 82206,82232 |
| Typhoon | 132469 | 1 | ACTIVE | 8,8 | 8 | 82232 |
| Mass Entanglement / Ursol's Vortex | 102359 / 102793 | 1/1 | CHOICE | 8,9 | 8 | 82232 |
| Oakskin | 449191 | 1 | PASSIVE | 9,3 | 23 | 82235,82236 |
| Perfectly-Honed Instincts | 1213597 | 1 | PASSIVE | 9,4 | 23 | 82235 |
| Instincts of the Claw | 449184 | 1 | PASSIVE | 9,5 | 23 | 82234 |
| Lycara's Teachings | 378988 | 2 | PASSIVE | 9,6 | 23 | 82234 |
| Lore of the Grove | 449185 | 1 | PASSIVE | 9,7 | 23 | 82234 |
| Gale Winds / Incessant Tempest | 400142 / 400140 | 1/1 | CHOICE | 9,8 | 23 | 82209 |
| Gift of the Wild | 1262034 | 1 | PASSIVE | 9,9 | 23 | 82207,82209 |
| Incapacitating Roar / Mighty Bash | 99 / 5211 | 1/1 | CHOICE | 10,2 | 23 | 100176 |
| Ursine Vigor | 377842 | 1 | PASSIVE | 10,4 | 23 | 100176 |
| Improved Stampeding Roar | 288826 | 1 | PASSIVE | 10,5 | 23 | 82233 |
| Circle of the Wild / Circle of the Heavens | 474530 / 474541 | 1/1 | CHOICE | 10,6 | 23 | 82233 |
| Lycara's Inspiration | 1232897 | 1 | PASSIVE | 10,7 | 23 | 82233 |
| Symbiotic Relationship | 474750 | 1 | ACTIVE | 10,8 | 23 | 100175 |
| Forestwalk | 400129 | 2 | PASSIVE | 10,10 | 23 | 100175 |
| Fluid Form | 449193 | 1 | PASSIVE | 11,3 | 23 | 100176 |
| Heart of the Wild | 1261867 | 1 | ACTIVE | 11,6 | 23 | 82230,92229,104078 |
| Innervate | 29166 | 1 | ACTIVE | 11,9 | 23 | 100175 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Maul | 6807 | 1 | ACTIVE | 2,20 | — | — |
| Gore | 210706 | 1 | PASSIVE | 3,19 | — | 82127 |
| Survival Instincts | 61336 | 1 | ACTIVE | 3,21 | — | 82127 |
| Front of the Pack | 377835 | 1 | PASSIVE | 4,18 | — | 82126 |
| Persistence | 1251406 | 1 | PASSIVE | 4,19 | — | 82126 |
| Dream of Cenarius / Dream Guide | 372119 / 1278886 | 1/1 | CHOICE | 4,21 | — | 82129 |
| Infected Wounds | 345208 | 1 | PASSIVE | 4,22 | — | 82129 |
| Innate Resolve | 377811 | 1 | PASSIVE | 5,18 | — | 109275,92227 |
| Berserk | 50334 | 1 | ACTIVE | 5,20 | — | 92227,92585 |
| Vulnerable Flesh | 372618 | 1 | PASSIVE | 5,22 | — | 92585,109376 |
| Survival of the Fittest | 203965 | 2 | PASSIVE | 6,17 | 8 | 82160 |
| Reinvigoration | 372945 | 2 | PASSIVE | 6,19 | 8 | 82160,82149 |
| After the Wildfire | 371905 | 1 | PASSIVE | 6,20 | 8 | 82149 |
| Memory of Ysera | 1250906 | 2 | PASSIVE | 6,21 | 8 | 82131,82149 |
| Scintillating Moonlight | 238049 | 2 | PASSIVE | 6,23 | 8 | 82131 |
| Ward of the Forest / Brambles | 1250923 / 203953 | 1/1 | CHOICE | 7,17 | 8 | 82143 |
| Soul of the Forest | 158477 | 1 | PASSIVE | 7,18 | 8 | 82157,82143 |
| Natural Resilience | 1278789 | 1 | PASSIVE | 7,19 | 8 | 82140,82157 |
| Reinforced Fur / Bristling Fur | 393618 / 155835 | 1/1 | CHOICE | 7,20 | 8 | 82140 |
| Gift of an Ancient Guardian / Guardian of Elune | 1251876 / 155578 | 1/1 | CHOICE | 7,21 | 8 | 82140,82144 |
| Ursoc's Endurance / Gory Fur | 393611 / 200854 | 1/1 | CHOICE | 7,22 | 8 | 82146,82144 |
| Ursol's Warding | 471492 | 1 | PASSIVE | 7,23 | 8 | 82146 |
| Rend and Tear / Untamed Savagery | 204053 / 372943 | 1/1 | CHOICE | 8,18 | 8 | 82156,109378,92226 |
| Raze | 400254 | 1 | ACTIVE | 8,20 | 8 | 82156,82161,109377 |
| Lunar Beam | 204066 | 1 | ACTIVE | 8,22 | 8 | 82148,109377,109375 |
| Ursoc's Fury | 377210 | 1 | PASSIVE | 9,17 | 20 | 109378,82152 |
| Flashing Claws | 393427 | 2 | PASSIVE | 9,18 | 20 | 82152 |
| Blood Frenzy | 203962 | 1 | PASSIVE | 9,19 | 20 | 82137,82152 |
| Moonless Night | 400278 | 1 | PASSIVE | 9,21 | 20 | 92587,82137 |
| Fury of Nature | 370695 | 2 | PASSIVE | 9,22 | 20 | 92587 |
| Twin Moonfire / Red Moon | 372567 / 1252871 | 1/1 | CHOICE | 9,23 | 20 | 82148,92587 |
| Harnessed Rage | 1253035 | 1 | PASSIVE | 10,18 | 20 | 82154,82142,82159 |
| Incarnation: Guardian of Ursoc / Convoke the Spirits | 102558 / 391528 | 1/1 | CHOICE | 10,20 | 20 | 82137,82142,92586 |
| Elune's Favored | 370586 | 1 | PASSIVE | 10,22 | 20 | 82138,82147,92586 |
| Killing Blow | 1252994 | 1 | PASSIVE | 11,17 | 20 | 82159,109379 |
| Sundering Roar | 1253799 | 1 | ACTIVE | 11,19 | 20 | 82136,109379 |
| Ursoc's Guidance | 393414 | 1 | PASSIVE | 11,20 | 20 | 82136 |
| Waking Nightmare | 1253461 | 1 | PASSIVE | 11,21 | 20 | 82134,82136 |
| Galactic Guardian | 203964 | 1 | PASSIVE | 11,23 | 20 | 82134,82147 |
| Wild Guardian | 1269614 | 1 | ACTIVE | 12,20 | 20 | — |

## Hero: Druid of the Claw

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Ravage | 441583 | 1 | PASSIVE | 8,2 | — | — |
| Fount of Strength | 441675 | 1 | PASSIVE | 9,1 | — | 94609 |
| Dreadful Wound | 441809 | 1 | PASSIVE | 9,2 | — | 94609 |
| Bestial Strength | 441841 | 1 | PASSIVE | 9,3 | — | 94609 |
| Limb from Limb | 1271540 | 1 | PASSIVE | 9,4 | — | 94609 |
| Wildshape Mastery | 441678 | 1 | PASSIVE | 10,1 | — | 94618 |
| Exacerbating Wounds | 1271839 | 1 | PASSIVE | 10,2 | — | 94620 |
| Pack's Endurance | 441844 | 1 | PASSIVE | 10,3 | — | 94611 |
| Ruthless Aggression / Killing Strikes | 441814 / 441824 | 1/1 | CHOICE | 10,4 | — | 109722 |
| Empowered Shapeshifting / Wildpower Surge | 441689 / 441691 | 1/1 | CHOICE | 11,1 | — | 94610 |
| Aggravate Wounds | 441829 | 1 | PASSIVE | 11,2 | — | 94619 |
| Strike for the Heart / Tear Down the Mighty | 441845 / 441846 | 1/1 | CHOICE | 11,3 | — | 94615 |
| Twin Claw | 1271635 | 1 | PASSIVE | 11,4 | — | 109723 |
| Claw Rampage | 441835 | 1 | PASSIVE | 12,2 | — | 94614,94616,94612,109721 |

## Hero: Elune's Chosen

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Boundless Moonlight | 424058 | 1 | PASSIVE | 2,13 | — | — |
| Moon Guardian | 429520 | 1 | PASSIVE | 3,12 | — | 94608 |
| Lunar Insight | 429530 | 1 | PASSIVE | 3,13 | — | 94608 |
| Glistening Fur | 429533 | 1 | PASSIVE | 3,14 | — | 94608 |
| Star Cascade | 1271206 | 1 | PASSIVE | 3,15 | — | 94608 |
| Stellar Command | 429668 | 1 | PASSIVE | 4,12 | — | 94598 |
| Atmospheric Exposure | 429532 | 1 | PASSIVE | 4,13 | — | 94588 |
| Moondust / Elune's Grace | 429538 / 443046 | 1/1 | CHOICE | 4,14 | — | 94594 |
| Penumbral Swell | 1271261 | 1 | PASSIVE | 4,15 | — | 109720 |
| Lunar Calling | 429523 | 1 | PASSIVE | 5,12 | — | 94596 |
| The Light of Elune / Astral Insight | 428655 / 429536 | 1/1 | CHOICE | 5,13 | — | 94607 |
| Arcane Affinity / Lunation | 429540 / 429539 | 1/1 | CHOICE | 5,14 | — | 94597 |
| Bask in Moonlight | 1271305 | 1 | PASSIVE | 5,15 | — | 109719 |
| The Eternal Moon | 424113 | 1 | PASSIVE | 6,13 | — | 94590,94585,94586,109718 |

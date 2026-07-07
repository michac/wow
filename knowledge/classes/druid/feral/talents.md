---
title: Druid Feral — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Druid Feral — talents (12.0.7)

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
| Tiger's Fury | 5217 | 1 | ACTIVE | 2,20 | — | — |
| Omen of Clarity | 16864 | 1 | PASSIVE | 3,19 | — | 82124 |
| Coiled to Spring | 449537 | 1 | PASSIVE | 3,20 | — | 82124 |
| Primal Wrath | 285381 | 1 | ACTIVE | 3,21 | — | 82124 |
| Merciless Claws | 231063 | 1 | PASSIVE | 4,18 | — | 82123 |
| Predator | 202021 | 1 | PASSIVE | 4,20 | — | 82120,82123 |
| Double-Clawed Rake | 391700 | 1 | PASSIVE | 4,22 | — | 82120 |
| Sabertooth | 202031 | 1 | PASSIVE | 5,19 | — | 82098,82122,82123 |
| Tireless Energy | 383352 | 2 | PASSIVE | 5,20 | — | 82122 |
| Pouncing Strikes | 390772 | 1 | PASSIVE | 5,21 | — | 82086,82122,82120 |
| Taste for Blood | 384665 | 1 | PASSIVE | 6,18 | 8 | 82102 |
| Survival Instincts | 61336 | 1 | ACTIVE | 6,20 | 8 | 82119,82102 |
| Dreadful Bleeding | 391045 | 1 | PASSIVE | 6,22 | 8 | 82119 |
| Sudden Ambush | 384667 | 1 | PASSIVE | 7,17 | 8 | 82104 |
| Moment of Clarity | 236068 | 1 | PASSIVE | 7,18 | 8 | 82104 |
| Savage Fury | 449645 | 1 | PASSIVE | 7,19 | 8 | 82104 |
| Berserk | 106951 | 1 | ACTIVE | 7,20 | 8 | 82116 |
| Panther's Guile | 1280316 | 1 | PASSIVE | 7,21 | 8 | 82118 |
| Rampant Ferocity | 391709 | 1 | PASSIVE | 7,22 | 8 | 82118 |
| Infected Wounds | 48484 | 1 | PASSIVE | 7,23 | 8 | 82118 |
| Raging Fury / Tiger's Tenacity | 391078 / 391872 | 1/1 | CHOICE | 8,17 | 8 | 82106,92641 |
| Wild Slashes | 390864 | 1 | PASSIVE | 8,19 | 8 | 82099,82106,82101 |
| Berserk: Heart of the Lion | 391174 | 1 | PASSIVE | 8,20 | 8 | 82101 |
| Blood Spattered | 1244532 | 1 | PASSIVE | 8,21 | 8 | 82101,82103,82117 |
| Soul of the Forest | 158476 | 1 | PASSIVE | 8,23 | 8 | 82117,82088 |
| Carnivorous Instinct | 390902 | 2 | PASSIVE | 9,18 | 20 | 82107,82106,82105 |
| Frantic Momentum | 391875 | 2 | PASSIVE | 9,20 | 20 | 82100 |
| Saber Jaws | 421432 | 2 | PASSIVE | 9,22 | 20 | 82091,82117,82090 |
| Apex Predator's Craving | 391881 | 1 | PASSIVE | 10,17 | 20 | 82110,82110,82107 |
| Feral Frenzy | 274837 | 1 | ACTIVE | 10,19 | 20 | 82110,82115 |
| Incarnation: Avatar of Ashamane / Convoke the Spirits | 102543 / 391528 | 1/1 | CHOICE | 10,20 | 20 | 82115 |
| Lacerating Claws | 1244632 | 1 | PASSIVE | 10,21 | 20 | 82094,82115 |
| Veinripper / Rip and Tear | 391978 / 391347 | 1/1 | CHOICE | 10,23 | 20 | 82091,82094 |
| Lunar Inspiration / Chomp | 155580 / 1244258 | 1/1 | CHOICE | 11,18 | 20 | 82109,82110,82112 |
| Focused Frenzy / Frantic Frenzy | 1244544 / 1243807 | 1/1 | CHOICE | 11,19 | 20 | 82112 |
| Ashamane's Guidance | 391548 | 1 | PASSIVE | 11,20 | 20 | 82114 |
| Hunger for Battle | 1244547 | 1 | PASSIVE | 11,21 | 20 | 82096 |
| Circle of Life and Death | 400320 | 1 | PASSIVE | 11,22 | 20 | 82093,82094,82096 |
| Unseen Predator | 1263657 | 1 | ACTIVE | 12,20 | 20 | — |

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

## Hero: Wildstalker

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Thriving Growth | 439528 | 1 | PASSIVE | 2,26 | — | — |
| Hunt Beneath the Open Skies | 439868 | 1 | PASSIVE | 3,24 | — | 94626 |
| Strategic Infusion | 439890 | 1 | PASSIVE | 3,25 | — | 94626 |
| Wildstalker's Power | 439926 | 1 | PASSIVE | 3,26 | — | 94626 |
| Green Thumb | 1270565 | 1 | PASSIVE | 3,27 | — | 94626 |
| Lethal Preservation | 455461 | 1 | PASSIVE | 4,24 | — | 94629 |
| Entangling Vortex / Flower Walk | 439895 / 439901 | 1/1 | CHOICE | 4,25 | — | 94623 |
| Bond with Nature / Harmonious Constitution | 439929 / 440116 | 1/1 | CHOICE | 4,26 | — | 94621 |
| Bursting Growth | 440120 | 1 | PASSIVE | 4,27 | — | 109717 |
| Resilient Flourishing / Root Network | 439880 / 439882 | 1/1 | CHOICE | 5,24 | — | 94624 |
| Patient Custodian | 1270592 | 1 | PASSIVE | 5,25 | — | 94622 |
| Twin Sprouts / Implant | 440117 / 440118 | 1/1 | CHOICE | 5,26 | — | 94625 |
| Rampancy | 1270586 | 1 | PASSIVE | 5,27 | — | 109716 |
| Vigorous Creepers | 440119 | 1 | PASSIVE | 6,26 | — | 94630,94628,94631,109715 |

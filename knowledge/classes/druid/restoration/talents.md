---
title: Druid Restoration — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Druid Restoration — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Rake | 1822 | 1 | ACTIVE | 2,3 | — | — |
| Frenzied Regeneration | 22842 | 1 | ACTIVE | 2,5 | — | — |
| Rejuvenation | 774 | 1 | ACTIVE | 2,7 | — | — |
| Starfire | 197628 | 1 | ACTIVE | 2,9 | — | — |
| Grievous Wounds | 474526 | 1 | PASSIVE | 3,2 | — | 82199 |
| Swipe | 213764 | 1 | ACTIVE | 3,4 | — | 82220,82199 |
| Ursoc's Spirit | 449182 | 1 | PASSIVE | 3,6 | — | 82217,82220 |
| Wild Growth | 48438 | 1 | ACTIVE | 3,8 | — | 82217 |
| Starsurge | 197626 | 1 | ACTIVE | 3,10 | — | 91044 |
| Rip | 1079 | 1 | ACTIVE | 4,3 | — | 82199 |
| Verdant Heart | 301768 | 1 | PASSIVE | 4,5 | — | 82219,82223,82220 |
| Improved Nature's Cure | 392378 | 1 | PASSIVE | 4,7 | — | 82219,82217 |
| Moonkin Form | 24858 | 1 | ACTIVE | 4,9 | — | 91044 |
| Maim | 22570 | 1 | ACTIVE | 5,2 | — | 82222 |
| Killer Instinct | 108299 | 2 | PASSIVE | 5,4 | — | 82222,82223,82218 |
| Ironfur | 192081 | 1 | ACTIVE | 5,5 | — | 82218 |
| Improved Barkskin | 327993 | 1 | PASSIVE | 5,6 | — | 82219,82218,104084 |
| Hibernate | 2637 | 1 | ACTIVE | 5,7 | — | 104084 |
| Nurturing Instinct | 33873 | 2 | PASSIVE | 5,8 | — | 82205,82208,104084 |
| Sunfire | 93402 | 1 | ACTIVE | 5,10 | — | 82208 |
| Primal Fury | 159286 | 1 | PASSIVE | 6,3 | 8 | 82225 |
| Thick Hide | 16931 | 1 | PASSIVE | 6,5 | 8 | 82225,104085 |
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
| Lifebloom | 33763 | 1 | ACTIVE | 2,20 | — | — |
| Swiftmend | 18562 | 1 | ACTIVE | 3,19 | — | 82049 |
| Nature's Swiftness | 132158 | 1 | ACTIVE | 3,20 | — | 82049 |
| Omen of Clarity | 113043 | 1 | PASSIVE | 3,21 | — | 82049 |
| Verdant Infusion / Prosperity | 392410 / 200383 | 1/1 | CHOICE | 4,18 | — | 82047 |
| Nature's Splendor / Passing Seasons | 392288 / 382550 | 1/1 | CHOICE | 4,20 | — | 82050 |
| Improved Regrowth | 231032 | 1 | PASSIVE | 4,22 | — | 104125 |
| Soul of the Forest | 158478 | 1 | PASSIVE | 5,19 | — | 82079,82051 |
| Tranquil Mind | 403521 | 1 | PASSIVE | 5,21 | — | 82083,82051 |
| Efflorescence | 145205 | 1 | ACTIVE | 6,18 | 8 | 82079,82055 |
| Tranquility | 740 | 1 | ACTIVE | 6,20 | 8 | 82055,92674 |
| Ironbark | 102342 | 1 | ACTIVE | 6,22 | 8 | 82083,92674 |
| Verdancy | 392325 | 1 | PASSIVE | 7,17 | 8 | 82057 |
| Lifetreading | 1217941 | 1 | PASSIVE | 7,18 | 8 | 82057 |
| Grove Guardians | 1226140 | 1 | PASSIVE | 7,19 | 8 | 82057 |
| Inner Peace / Flourish | 197073 / 197721 | 1/1 | CHOICE | 7,20 | 8 | 82054 |
| Cultivation | 200390 | 1 | PASSIVE | 7,21 | 8 | 82082 |
| Improved Wild Growth | 328025 | 1 | PASSIVE | 7,22 | 8 | 82082,82082 |
| Stonebark / Improved Ironbark | 197061 / 382552 | 1/1 | CHOICE | 7,23 | 8 | 82082 |
| Renewing Surge | 470562 | 1 | PASSIVE | 8,16 | 8 | 82059 |
| Rampant Growth | 404521 | 1 | PASSIVE | 8,17 | 8 | 82059 |
| Regenesis | 383191 | 2 | PASSIVE | 8,18 | 8 | 82043,82059,103874 |
| Wild Synthesis | 400533 | 1 | PASSIVE | 8,19 | 8 | 82043 |
| Power of the Archdruid | 392302 | 1 | PASSIVE | 8,20 | 8 | 82053,82056,82043 |
| Unstoppable Growth | 382559 | 2 | PASSIVE | 8,22 | 8 | 82045,82056,82045 |
| Improved Swiftmend | 470549 | 1 | PASSIVE | 8,23 | 8 | 82081,82045 |
| Regenerative Heartwood | 392116 | 1 | PASSIVE | 8,24 | 8 | 82081 |
| Ysera's Gift | 145108 | 1 | PASSIVE | 9,17 | 20 | 82062,82060,82058 |
| Incarnation: Tree of Life / Convoke the Spirits | 33891 / 391528 | 1/1 | CHOICE | 9,19 | 20 | 82065,82062,94535 |
| Call of the Elder Druid | 426784 | 1 | PASSIVE | 9,21 | 20 | 82080,82065 |
| Intensity | 1264649 | 1 | PASSIVE | 9,23 | 20 | 103873,82075,82080 |
| Liveliness / Master Shapeshifter | 426702 / 289237 | 1/1 | CHOICE | 10,16 | 20 | 82060,82048 |
| Waking Dream | 392221 | 1 | PASSIVE | 10,17 | 20 | 82048 |
| Embrace of the Dream | 392124 | 1 | PASSIVE | 10,18 | 20 | 82048,82064 |
| Cenarius' Guidance | 393371 | 1 | PASSIVE | 10,19 | 20 | 82064 |
| Nature's Bounty | 1263879 | 1 | PASSIVE | 10,20 | 20 | 82064,82067 |
| Dream of Cenarius | 158504 | 1 | PASSIVE | 10,21 | 20 | 82067 |
| Thriving Vegetation | 447131 | 2 | PASSIVE | 10,22 | 20 | 82052,82067 |
| Abundance | 207383 | 1 | PASSIVE | 10,23 | 20 | 82052 |
| Nurturing Dormancy | 392099 | 1 | PASSIVE | 10,24 | 20 | 82052,82075 |
| Photosynthesis | 274902 | 1 | PASSIVE | 11,17 | 20 | 82046,82074,82070 |
| Harmonious Blooming | 392256 | 1 | PASSIVE | 11,19 | 20 | 82063,82072,82070 |
| Reforestation | 392356 | 1 | PASSIVE | 11,21 | 20 | 82068,82072,82066 |
| Germination | 155675 | 1 | PASSIVE | 11,23 | 20 | 103876,82076,82068 |
| Everbloom | 392167 | 1 | ACTIVE | 12,20 | 20 | — |

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

## Hero: Keeper of the Grove

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Dream Surge | 433831 | 1 | PASSIVE | 7,13 | — | — |
| Treants of the Moon | 428544 | 1 | PASSIVE | 8,12 | — | 94600 |
| Expansiveness | 429399 | 1 | PASSIVE | 8,13 | — | 94600 |
| Protective Growth | 433748 | 1 | PASSIVE | 8,14 | — | 94600 |
| Sylvan Beckoning | 1264614 | 1 | PASSIVE | 8,15 | — | 94600 |
| Power of Nature / Durability of Nature | 428859 / 429227 | 1/1 | CHOICE | 9,12 | — | 94599 |
| Cenarius' Might | 455797 | 1 | PASSIVE | 9,13 | — | 94602 |
| Grove's Inspiration / Potent Enchantments | 429402 / 429420 | 1/1 | CHOICE | 9,14 | — | 94593 |
| Dryad's Dance | 1264776 | 1 | PASSIVE | 9,15 | — | 109714 |
| Bounteous Bloom / Early Spring | 429215 / 428937 | 1/1 | CHOICE | 10,12 | — | 94605 |
| Power of the Dream / Control of the Dream | 434220 / 434249 | 1/1 | CHOICE | 10,13 | — | 94604 |
| Blooming Infusion | 429433 | 1 | PASSIVE | 10,14 | — | 94595 |
| Spirit of the Thicket | 1264899 | 1 | PASSIVE | 10,15 | — | 109713 |
| Harmony of the Grove | 428731 | 1 | PASSIVE | 11,13 | — | 94601,94592,94591,109712 |

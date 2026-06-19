---
title: Druid Balance — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Druid Balance — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Rake | 1822 | 1 | ACTIVE | 2,3 | — | — |
| Frenzied Regeneration | 22842 | 1 | ACTIVE | 2,5 | — | — |
| Rejuvenation | 774 | 1 | ACTIVE | 2,7 | — | — |
| Starfire | 194153 | 1 | ACTIVE | 2,9 | — | — |
| Grievous Wounds | 474526 | 1 | PASSIVE | 3,2 | — | 82199 |
| Swipe | 213764 | 1 | ACTIVE | 3,4 | — | 82220,82199 |
| Ursoc's Spirit | 449182 | 1 | PASSIVE | 3,6 | — | 82217,82220 |
| Wild Growth | 48438 | 1 | ACTIVE | 3,8 | — | 82217 |
| Starsurge | 78674 | 1 | ACTIVE | 3,10 | — | 82201 |
| Rip | 1079 | 1 | ACTIVE | 4,3 | — | 82199 |
| Verdant Heart | 301768 | 1 | PASSIVE | 4,5 | — | 82219,82223,82220 |
| Remove Corruption | 2782 | 1 | ACTIVE | 4,7 | — | 82217,82219 |
| Moonkin Form | 24858 | 1 | ACTIVE | 4,9 | — | 82201 |
| Maim | 22570 | 1 | ACTIVE | 5,2 | — | 82222 |
| Killer Instinct | 108299 | 2 | PASSIVE | 5,4 | — | 82222,82223,82218 |
| Ironfur | 192081 | 1 | ACTIVE | 5,5 | — | 82218 |
| Improved Barkskin | 327993 | 1 | PASSIVE | 5,6 | — | 82219,82218,82241 |
| Hibernate | 2637 | 1 | ACTIVE | 5,7 | — | 82241 |
| Nurturing Instinct | 33873 | 2 | PASSIVE | 5,8 | — | 82205,82208,82241 |
| Sunfire | 93402 | 1 | ACTIVE | 5,10 | — | 82208 |
| Primal Fury | 159286 | 1 | PASSIVE | 6,3 | 8 | 82225 |
| Thick Hide | 16931 | 1 | PASSIVE | 6,5 | 8 | 82225,104085 |
| Light of the Sun | 202918 | 1 | PASSIVE | 6,6 | 8 | 104085 |
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
| Eclipse | 1239669 | 1 | PASSIVE | 2,20 | — | — |
| Shooting Stars | 202342 | 1 | PASSIVE | 3,19 | — | 88223 |
| Solar Beam | 78675 | 1 | ACTIVE | 3,21 | — | 88223 |
| Solstice | 343647 | 1 | PASSIVE | 4,18 | — | 88225 |
| Force of Nature | 205636 | 1 | ACTIVE | 4,20 | — | 88225,88231 |
| Twin Moons | 279620 | 1 | PASSIVE | 4,22 | — | 88231 |
| Improved Eclipse | 1240906 | 1 | PASSIVE | 5,17 | — | 88203 |
| Nature's Balance | 202430 | 1 | PASSIVE | 5,19 | — | 88203,88210 |
| Umbral Intensity | 383195 | 1 | PASSIVE | 5,21 | — | 88201,88210 |
| Aetherial Kindling / Meteor Storm | 327541 / 1240262 | 1/1 | CHOICE | 5,23 | — | 88201 |
| Wild Surges | 406890 | 1 | PASSIVE | 6,18 | 8 | 91048,88226 |
| Celestial Alignment | 194223 | 1 | ACTIVE | 6,20 | 8 | 88208,88226,88210 |
| Soul of the Forest | 114107 | 1 | PASSIVE | 6,22 | 8 | 88209,88208 |
| Sunseeker Mushroom / Wild Mushroom | 468936 / 88747 | 1/1 | CHOICE | 7,17 | 8 | 91048,88204 |
| Nature's Grace / Elune's Challenge | 450347 / 1240283 | 1/1 | CHOICE | 7,18 | 8 | 88204 |
| Stellar Amplification | 450212 | 1 | PASSIVE | 7,19 | 8 | 88215,88204 |
| Whirling Stars / Orbital Strike | 468743 / 390378 | 1/1 | CHOICE | 7,20 | 8 | 88215 |
| Touch the Cosmos | 450356 | 1 | PASSIVE | 7,21 | 8 | 88215,88219 |
| Meteorites | 1240907 | 1 | PASSIVE | 7,23 | 8 | 88209,88219 |
| Cosmic Rapidity | 400059 | 2 | PASSIVE | 8,18 | 8 | 88212,88202,110279 |
| Celestial Fire | 1240185 | 1 | PASSIVE | 8,19 | 8 | 88221 |
| Astral Communion | 450598 | 1 | PASSIVE | 8,20 | 8 | 88221 |
| Hail of Stars | 469004 | 1 | PASSIVE | 8,21 | 8 | 88222 |
| Starlord | 202345 | 2 | PASSIVE | 8,22 | 8 | 88232,88222,88219 |
| Sculpt the Stars | 1240188 | 1 | PASSIVE | 9,17 | 20 | 88202,88227 |
| Balance of All Things | 394048 | 2 | PASSIVE | 9,19 | 20 | 88227,88216 |
| Total Eclipse | 1240206 | 2 | PASSIVE | 9,21 | 20 | 88207,88216 |
| Starweaver / Rattle the Stars | 393940 / 393954 | 1/1 | CHOICE | 9,22 | 20 | 88207 |
| Power of Goldrinn | 394046 | 1 | PASSIVE | 9,23 | 20 | 88232,88207 |
| Sundered Firmament / Orbit Breaker | 394094 / 383197 | 1/1 | CHOICE | 10,18 | 20 | 88220,88214 |
| Incarnation: Chosen of Elune / Convoke the Spirits | 102560 / 391528 | 1/1 | CHOICE | 10,20 | 20 | 88214,88200 |
| Fury of Elune / New Moon | 202770 / 274281 | 1/1 | CHOICE | 10,22 | 20 | 88236,88235,88200 |
| Umbral Embrace | 393760 | 1 | PASSIVE | 11,18 | 20 | 88218 |
| Harmony of the Heavens | 450558 | 1 | PASSIVE | 11,19 | 20 | 88206,88218 |
| Elune's Guidance | 393991 | 1 | PASSIVE | 11,20 | 20 | 88206 |
| Denizen of the Dream | 394065 | 1 | PASSIVE | 11,21 | 20 | 88224,88206 |
| Radiant Moonlight | 394121 | 1 | PASSIVE | 11,22 | 20 | 88224 |
| Ascendant Eclipses | 1261564 | 1 | ACTIVE | 12,20 | 20 | — |

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

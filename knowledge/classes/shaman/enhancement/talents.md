---
title: Shaman Enhancement — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-18
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Shaman Enhancement — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Chain Heal | 1064 | 1 | ACTIVE | 2,2 | — | — |
| Lava Lash | 60103 | 1 | ACTIVE | 2,4 | — | — |
| Chain Lightning | 188443 | 1 | ACTIVE | 2,6 | — | — |
| Earth Shield | 974 | 1 | ACTIVE | 3,1 | — | 103588 |
| Ancestral Wolf Affinity | 382197 | 1 | PASSIVE | 3,3 | — | 103588,109389 |
| Fire and Ice | 382886 | 1 | PASSIVE | 3,4 | — | 109389 |
| Spirit Wolf / Thunderous Paws | 260878 / 378075 | 1/1 | CHOICE | 3,5 | — | 103583,109389 |
| Frost Shock | 196840 | 1 | ACTIVE | 3,7 | — | 103583 |
| Elemental Orbit | 383010 | 1 | PASSIVE | 4,1 | — | 103596 |
| Spirit Walk / Gust of Wind | 58875 / 192063 | 1/1 | CHOICE | 4,2 | — | 103596,103610 |
| Astral Shift | 108271 | 1 | ACTIVE | 4,4 | — | 103581,103610,103605 |
| Nature's Guardian | 30884 | 1 | PASSIVE | 4,6 | — | 103581,109492 |
| Encasing Cold / Arctic Snowstorm | 462762 / 462764 | 1/1 | CHOICE | 4,7 | — | 109492 |
| Healing Stream Totem | 5394 | 1 | ACTIVE | 5,1 | — | 103591,103602 |
| Winds of Al'Akir | 382215 | 2 | PASSIVE | 5,3 | — | 103591,103616 |
| Planes Traveler / Astral Bulwark | 381647 / 377933 | 1/1 | CHOICE | 5,4 | — | 103616 |
| Brimming with Life | 381689 | 2 | PASSIVE | 5,5 | — | 103613,103616 |
| Wind Shear | 57994 | 1 | ACTIVE | 5,7 | — | 103613,109493 |
| Elemental Resistance | 462368 | 1 | PASSIVE | 6,1 | 8 | 103590 |
| Earthgrab Totem | 51485 | 1 | ACTIVE | 6,2 | 8 | 103614,103590 |
| Capacitor Totem | 192058 | 1 | ACTIVE | 6,4 | 8 | 103614,103611 |
| Spiritual Awakening | 1270375 | 1 | PASSIVE | 6,5 | 8 | 103582,103611 |
| Enhanced Imbues | 462796 | 1 | PASSIVE | 6,6 | 8 | 103615,103582 |
| Windveil | 355630 | 1 | PASSIVE | 6,7 | 8 | 103615 |
| Refreshing Waters | 378211 | 1 | PASSIVE | 7,1 | 8 | 103601,103622 |
| Cleanse Spirit | 51886 | 1 | ACTIVE | 7,3 | 8 | 103622,103579 |
| Static Charge | 265046 | 2 | PASSIVE | 7,4 | 8 | 103579 |
| Wind Rush Totem | 192077 | 1 | ACTIVE | 7,5 | 8 | 110085,103579 |
| Earth Elemental | 198103 | 1 | ACTIVE | 7,6 | 8 | 103606,110085 |
| Purge / Greater Purge | 370 / 378773 | 1/1 | CHOICE | 8,2 | 8 | 103608,103594 |
| Nature's Fury | 381655 | 2 | PASSIVE | 8,4 | 8 | 103627,103618,103608 |
| Ascending Air / Jet Stream | 462791 / 462817 | 1/1 | CHOICE | 8,5 | 8 | 103627 |
| Primordial Bond | 1279819 | 1 | PASSIVE | 8,6 | 8 | 103585 |
| Hex | 51514 | 1 | ACTIVE | 8,7 | 8 | 103585,103628 |
| Spiritwalker's Grace | 79206 | 1 | ACTIVE | 9,1 | 23 | 103594,103624 |
| Totemic Projection | 108287 | 1 | ACTIVE | 9,3 | 23 | 103617,103624 |
| Elemental Warding | 381650 | 1 | PASSIVE | 9,4 | 23 | 103617,103607 |
| Totemic Focus | 382201 | 1 | PASSIVE | 9,6 | 23 | 103607,103612,103623 |
| Graceful Spirit / Spiritwalker's Aegis | 192088 / 378077 | 1/1 | CHOICE | 10,1 | 23 | 103584 |
| Mana Spring | 381930 | 1 | PASSIVE | 10,3 | 23 | 103586,109386 |
| Tremor Totem / Poison Cleansing Totem | 8143 / 383013 | 1/1 | CHOICE | 10,4 | 23 | 103586 |
| Therazane's Resilience / Reactive Warding | 1217622 / 462454 | 1/1 | CHOICE | 10,5 | 23 | 103586,103625 |
| Voodoo Mastery | 204268 | 1 | PASSIVE | 10,7 | 23 | 103623 |
| Nature's Swiftness | 378081 | 1 | ACTIVE | 11,2 | 23 | 103587,103626 |
| Totemic Surge | 381867 | 1 | PASSIVE | 11,4 | 23 | 103599,103587,103593 |
| Instinctive Imbuements | 1270350 | 1 | PASSIVE | 11,6 | 23 | 103593,103625,103600 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Maelstrom Weapon | 187880 | 1 | PASSIVE | 2,17 | — | — |
| Windfury Weapon | 33757 | 1 | ACTIVE | 3,16 | — | 80941 |
| Flametongue Weapon | 318038 | 1 | ACTIVE | 3,18 | — | 80941 |
| Forceful Winds | 262647 | 1 | PASSIVE | 4,15 | — | 80958 |
| Crash Lightning | 187874 | 1 | ACTIVE | 4,17 | — | 80942,80958 |
| Molten Assault | 334033 | 1 | PASSIVE | 4,19 | — | 80942 |
| Unruly Winds | 390288 | 1 | PASSIVE | 5,15 | — | 80969 |
| Overflowing Maelstrom | 384143 | 1 | PASSIVE | 5,17 | — | 80974 |
| Ashen Catalyst | 390370 | 1 | PASSIVE | 5,19 | — | 80943 |
| Stormblast | 319930 | 1 | PASSIVE | 6,14 | 8 | 80968 |
| Overcharge | 1251026 | 1 | PASSIVE | 6,16 | 8 | 80939,80968 |
| Raging Maelstrom | 384149 | 1 | PASSIVE | 6,17 | 8 | 80939 |
| Flurry | 382888 | 1 | PASSIVE | 6,18 | 8 | 80947,80939 |
| Hot Hand | 201900 | 2 | PASSIVE | 6,20 | 8 | 80947 |
| Storm's Wrath | 392352 | 1 | PASSIVE | 7,15 | 8 | 80968,80960,80944 |
| Elemental Tempo | 1250364 | 1 | PASSIVE | 7,17 | 8 | 80944,80938,103642 |
| Voltaic Blaze | 470057 | 1 | ACTIVE | 7,19 | 8 | 80947,80945,103642 |
| Chaining Storms | 334308 | 1 | PASSIVE | 8,14 | 8 | 80967,80960 |
| Converging Storms | 384363 | 1 | PASSIVE | 8,15 | 8 | 80967 |
| Stormflurry | 344357 | 1 | PASSIVE | 8,16 | 8 | 80961,80967 |
| Stormbind | 1251069 | 1 | PASSIVE | 8,17 | 8 | 80961 |
| Elemental Weapons | 384355 | 1 | PASSIVE | 8,18 | 8 | 80954,80961 |
| Fire Nova | 1260666 | 1 | PASSIVE | 8,19 | 8 | 80954 |
| Lashing Flames | 334046 | 1 | PASSIVE | 8,20 | 8 | 80954,80945 |
| Ride the Lightning | 289874 | 1 | PASSIVE | 9,15 | 20 | 109192,103871,80973 |
| Doom Winds | 384352 | 1 | ACTIVE | 9,17 | 20 | 103871,80953,109191 |
| Sundering | 197214 | 1 | ACTIVE | 9,19 | 20 | 80948,80953,109909 |
| Lightning Strikes | 384450 | 1 | PASSIVE | 10,14 | 20 | 80962 |
| Elemental Assault | 210853 | 1 | PASSIVE | 10,16 | 20 | 80959,80962 |
| Static Accumulation | 384411 | 2 | PASSIVE | 10,17 | 20 | 80959 |
| Feral Spirit | 469314 | 1 | PASSIVE | 10,18 | 20 | 80975,80959 |
| Surging Elements | 382042 | 1 | PASSIVE | 10,20 | 20 | 80975 |
| Thunder Capacitor | 1262635 | 1 | PASSIVE | 11,14 | 20 | 109193 |
| Deeply Rooted Elements / Ascendance | 378270 / 114051 | 1/1 | CHOICE | 11,16 | 20 | 80950 |
| Thorim's Invocation | 384444 | 1 | PASSIVE | 11,18 | 20 | 80950 |
| Primordial Storm | 1218047 | 1 | PASSIVE | 11,20 | 20 | 80964 |
| Storm Unleashed | 1262713 | 1 | ACTIVE | 12,17 | 20 | — |

## Hero: Totemic

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Surging Totem | 444995 | 1 | ACTIVE | 2,23 | — | — |
| Totemic Rebound | 445025 | 1 | PASSIVE | 3,21 | — | 94877 |
| Amplification Core / Oversurge | 445029 / 445030 | 1/1 | CHOICE | 3,22 | — | 94877 |
| Lively Totems | 445034 | 1 | PASSIVE | 3,23 | — | 94877 |
| Totemic Momentum | 1260644 | 1 | PASSIVE | 3,24 | — | 94877 |
| Oversized Totems / Swift Recall | 445026 / 445027 | 1/1 | CHOICE | 4,21 | — | 94890 |
| Wind Barrier | 445031 | 1 | PASSIVE | 4,22 | — | 94874 |
| Splitstream | 445035 | 1 | PASSIVE | 4,23 | — | 94882 |
| Elemental Attunement | 1263288 | 1 | PASSIVE | 4,24 | — | 109726 |
| Imbuement Mastery | 445028 | 1 | PASSIVE | 5,21 | — | 94859 |
| Pulse Capacitor / Supportive Imbuements | 445032 / 445033 | 1/1 | CHOICE | 5,22 | — | 94891 |
| Totemic Coordination / Earthsurge | 445036 / 455590 | 1/1 | CHOICE | 5,23 | — | 94872 |
| Primal Catalyst | 1260874 | 1 | PASSIVE | 5,24 | — | 109725 |
| Whirling Elements | 445024 | 1 | PASSIVE | 6,23 | — | 94881,94866,94871,109724 |

## Hero: Stormbringer

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Tempest | 454009 | 1 | PASSIVE | 7,10 | — | — |
| Unlimited Power | 454391 | 1 | PASSIVE | 8,9 | — | 94892 |
| Stormcaller | 454021 | 1 | PASSIVE | 8,10 | — | 94892 |
| Lightning Conduit / Electroshock | 467778 / 454022 | 1/1 | CHOICE | 8,11 | — | 94892 |
| Stormwell | 1264762 | 1 | PASSIVE | 8,12 | — | 94892 |
| Storm Swell / Supercharge | 455088 / 455110 | 1/1 | CHOICE | 9,9 | — | 94886 |
| Arc Discharge | 455096 | 1 | PASSIVE | 9,10 | — | 94893 |
| Rolling Thunder | 454026 | 1 | PASSIVE | 9,11 | — | 94863 |
| Natural Gift | 1264691 | 1 | PASSIVE | 9,12 | — | 109729 |
| Voltaic Surge | 454919 | 1 | PASSIVE | 10,9 | — | 94873 |
| Conductive Energy | 455123 | 1 | PASSIVE | 10,10 | — | 94885 |
| Nature's Protection / Surging Currents | 454027 / 454372 | 1/1 | CHOICE | 10,11 | — | 94889 |
| Descending Skies | 1264688 | 1 | PASSIVE | 10,12 | — | 109728 |
| Awakening Storms | 455129 | 1 | PASSIVE | 11,10 | — | 94880,94868,94870,109727 |

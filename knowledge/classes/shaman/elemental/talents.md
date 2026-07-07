---
title: Shaman Elemental — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Shaman Elemental — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Chain Heal | 1064 | 1 | ACTIVE | 2,2 | — | — |
| Lava Burst | 51505 | 1 | ACTIVE | 2,4 | — | — |
| Chain Lightning | 188443 | 1 | ACTIVE | 2,6 | — | — |
| Earth Shield | 974 | 1 | ACTIVE | 3,1 | — | 103588 |
| Ancestral Wolf Affinity | 382197 | 1 | PASSIVE | 3,3 | — | 103598,103588 |
| Fire and Ice | 382886 | 1 | PASSIVE | 3,4 | — | 103598 |
| Spirit Wolf / Thunderous Paws | 260878 / 378075 | 1/1 | CHOICE | 3,5 | — | 103583,103598 |
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
| Earth Shock / Elemental Blast | 8042 / 117014 | 1/1 | CHOICE | 2,17 | — | — |
| Earthquake / Earthquake | 462620 / 61882 | 1/1 | CHOICE | 3,16 | — | 80984 |
| Elemental Fury | 60188 | 1 | PASSIVE | 3,17 | — | 80984 |
| Echo of the Elements | 333919 | 1 | PASSIVE | 3,18 | — | 80984 |
| Flash of Lightning | 381936 | 1 | PASSIVE | 4,15 | — | 80985 |
| Tectonic Collapse / Aftershock | 1258899 / 273221 | 1/1 | CHOICE | 4,17 | — | 80983 |
| Molten Wrath / Master of the Elements | 1258843 / 16166 | 1/1 | CHOICE | 4,19 | — | 80981 |
| Lightning Capacitor | 462862 | 1 | PASSIVE | 5,14 | — | 80990 |
| Stormkeeper | 191634 | 1 | ACTIVE | 5,17 | — | 81000 |
| Flametongue Weapon | 318038 | 1 | ACTIVE | 5,20 | — | 80999 |
| Storm Frenzy | 462695 | 1 | PASSIVE | 6,15 | 8 | 80990 |
| Swelling Maelstrom | 381707 | 1 | PASSIVE | 6,16 | 8 | 80988 |
| Primordial Fury | 378193 | 1 | PASSIVE | 6,17 | 8 | 80988 |
| Fury of the Storms / Herald of the Storms | 191717 / 468571 | 1/1 | CHOICE | 6,18 | 8 | 80988 |
| Flames of the Cauldron | 378266 | 1 | PASSIVE | 6,20 | 8 | 81004 |
| Amped Up | 1269360 | 1 | PASSIVE | 7,14 | 8 | 80997,103635 |
| Elemental Resonance / Thunderstrike Ward | 1258895 / 462757 | 1/1 | CHOICE | 7,16 | 8 | 103635,81016,103639 |
| Path of the Seer | 1269364 | 1 | PASSIVE | 7,17 | 8 | 103639 |
| Elemental Unity | 462866 | 1 | PASSIVE | 7,18 | 8 | 80998 |
| Searing Flames | 381782 | 1 | PASSIVE | 7,19 | 8 | 80998,103630 |
| Power of the Maelstrom | 191861 | 1 | PASSIVE | 8,14 | 8 | 103638 |
| Earthshatter | 468626 | 1 | PASSIVE | 8,15 | 8 | 103635,103631,103638 |
| Storm Infusion | 1258889 | 1 | PASSIVE | 8,16 | 8 | 103631 |
| Echo Chamber | 382032 | 1 | PASSIVE | 8,17 | 8 | 103633,110066,103631 |
| Everlasting Elements | 462867 | 1 | PASSIVE | 8,18 | 8 | 103633 |
| Earthen Rage | 170374 | 1 | PASSIVE | 8,19 | 8 | 103633,81005 |
| Lava Flows | 1273485 | 1 | PASSIVE | 8,20 | 8 | 81005,103630 |
| Fusion of Elements | 462840 | 1 | PASSIVE | 9,14 | 20 | 80996 |
| Eye of the Storm | 381708 | 1 | PASSIVE | 9,16 | 20 | 81015,103636,80995 |
| Ascendance | 114050 | 1 | ACTIVE | 9,17 | 20 | 81015 |
| Inferno Arc | 1259047 | 1 | PASSIVE | 9,18 | 20 | 81010,103634,81015 |
| Flames of the Firelord | 381784 | 1 | PASSIVE | 9,20 | 20 | 110186,81010 |
| Lightning Rod | 210689 | 1 | PASSIVE | 10,15 | 20 | 80993,81003 |
| Mountains Will Fall | 381726 | 1 | PASSIVE | 10,16 | 20 | 80989,81003 |
| Call of Fire | 378255 | 1 | PASSIVE | 10,17 | 20 | 80989 |
| Voltaic Blaze | 470057 | 1 | ACTIVE | 10,19 | 20 | 103641,81008 |
| Charged Conduit | 468625 | 1 | PASSIVE | 11,14 | 20 | 81012 |
| First Ascendant / Preeminence | 462440 / 462443 | 1/1 | CHOICE | 11,16 | 20 | 80992 |
| Primal Elementalist | 117013 | 1 | PASSIVE | 11,18 | 20 | 80992 |
| Crackling Fury | 1269215 | 2 | PASSIVE | 11,19 | 20 | 81007 |
| Purging Flames | 1259471 | 1 | PASSIVE | 11,20 | 20 | 81007 |
| Feedback Loop | 1270061 | 1 | ACTIVE | 12,17 | 20 | — |

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

## Hero: Farseer

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Call of the Ancestors | 443450 | 1 | PASSIVE | 2,10 | — | — |
| Latent Wisdom / Ancient Fellowship | 443449 / 443423 | 1/1 | CHOICE | 3,9 | — | 94888 |
| Heed My Call / Routine Communication | 443444 / 443445 | 1/1 | CHOICE | 3,10 | — | 94888 |
| Elemental Reverb | 443418 | 1 | PASSIVE | 3,11 | — | 94888 |
| Ancestral Influence | 1270446 | 1 | PASSIVE | 3,12 | — | 94888 |
| Offering from Beyond | 443451 | 1 | PASSIVE | 4,9 | — | 94862 |
| Primordial Capacity | 443448 | 1 | PASSIVE | 4,10 | — | 94884 |
| Spiritwalker's Momentum | 443425 | 1 | PASSIVE | 4,11 | — | 94869 |
| Windspeaker | 1270447 | 1 | PASSIVE | 4,12 | — | 109732 |
| Natural Harmony / Earthen Communion | 443442 / 443441 | 1/1 | CHOICE | 5,9 | — | 94887 |
| Maelstrom Supremacy | 443447 | 1 | PASSIVE | 5,10 | — | 94860 |
| Final Calling | 443446 | 1 | PASSIVE | 5,11 | — | 94861 |
| Mystic Knowledge | 1270450 | 1 | PASSIVE | 5,12 | — | 109731 |
| Ancestral Swiftness | 443454 | 1 | ACTIVE | 6,10 | — | 94875,94883,94858,109730 |

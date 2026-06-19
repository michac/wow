---
title: Shaman Restoration — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-18
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Shaman Restoration — talents (12.0.7)

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
| Improved Purify Spirit | 383016 | 1 | PASSIVE | 7,3 | 8 | 103622,103579 |
| Static Charge | 265046 | 2 | PASSIVE | 7,4 | 8 | 103579 |
| Wind Rush Totem | 192077 | 1 | ACTIVE | 7,5 | 8 | 110085,103579 |
| Earth Elemental | 198103 | 1 | ACTIVE | 7,6 | 8 | 103606,110085 |
| Purge / Greater Purge | 370 / 378773 | 1/1 | CHOICE | 8,2 | 8 | 81073,103594 |
| Nature's Fury | 381655 | 2 | PASSIVE | 8,4 | 8 | 81073,103627,103618 |
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
| Riptide | 61295 | 1 | ACTIVE | 2,18 | — | — |
| Healing Rain | 73920 | 1 | ACTIVE | 3,17 | — | 81027 |
| Healing Stream Totem | 5394 | 1 | ACTIVE | 3,19 | — | 81027 |
| Soothing Rain | 1252874 | 1 | PASSIVE | 4,16 | — | 81040 |
| Acid Rain | 378443 | 1 | PASSIVE | 4,17 | — | 81040 |
| Ascendance / Healing Tide Totem | 114052 / 108280 | 1/1 | CHOICE | 4,18 | — | 81022,81040 |
| Water Totem Mastery | 382030 | 1 | PASSIVE | 4,20 | — | 81022 |
| Overflowing Shores | 383222 | 1 | PASSIVE | 5,15 | — | 103428 |
| Ancestral Vigor | 207401 | 2 | PASSIVE | 5,17 | — | 81032,103428,81039 |
| First Ascendant / Preeminence | 462440 / 462443 | 1/1 | CHOICE | 5,18 | — | 81032 |
| Resurgence | 16196 | 1 | PASSIVE | 5,19 | — | 81032,81021 |
| Living Stream | 382482 | 1 | PASSIVE | 5,21 | — | 81021 |
| Current Control | 1253093 | 1 | PASSIVE | 6,16 | 8 | 103429,103428 |
| White Water | 462587 | 1 | PASSIVE | 6,18 | 8 | 81033,103429,81024 |
| Calm Waters | 1252841 | 1 | PASSIVE | 6,20 | 8 | 81018,81024 |
| Quickstream | 1253099 | 1 | PASSIVE | 6,21 | 8 | 81018 |
| Rip Current | 1254251 | 1 | PASSIVE | 7,15 | 8 | 81038,92677 |
| Crashing Waves | 1253090 | 1 | PASSIVE | 7,16 | 8 | 81038 |
| Unleash Life | 73685 | 1 | ACTIVE | 7,17 | 8 | 81038,81047 |
| Torrent | 200072 | 1 | PASSIVE | 7,18 | 8 | 81047 |
| Earthliving Weapon | 382021 | 1 | ACTIVE | 7,19 | 8 | 81047,81019 |
| Earthweaver | 1254210 | 1 | PASSIVE | 7,21 | 8 | 81048,81019 |
| Deluge | 200076 | 1 | PASSIVE | 8,16 | 8 | 92675,110084,109301 |
| Earthen Accord | 1271104 | 1 | PASSIVE | 8,17 | 8 | 92675 |
| Tidal Waves | 51564 | 1 | PASSIVE | 8,18 | 8 | 81049,92675,103432 |
| Improved Earthliving Weapon | 382315 | 1 | PASSIVE | 8,19 | 8 | 81049 |
| Ancestral Reach / Flow of the Tides | 382732 / 382039 | 1/1 | CHOICE | 8,20 | 8 | 81046,81019,81049 |
| Downpour | 462486 | 1 | ACTIVE | 9,15 | 20 | 81037,109301 |
| Echo of the Elements | 333919 | 1 | PASSIVE | 9,17 | 20 | 110083,81037,81044 |
| Spirit Link Totem | 98008 | 1 | ACTIVE | 9,19 | 20 | 81031,81050,81044 |
| Earthen Harmony | 382020 | 1 | PASSIVE | 9,21 | 20 | 81046,81031 |
| Water Expulsion | 1253014 | 1 | PASSIVE | 10,15 | 20 | 103436 |
| Ancestral Awakening | 382309 | 2 | PASSIVE | 10,16 | 20 | 81055,103436 |
| Tidewaters | 462424 | 1 | PASSIVE | 10,17 | 20 | 81055 |
| Undercurrent | 382194 | 2 | PASSIVE | 10,18 | 20 | 81041,81055 |
| Spouting Spirits | 462383 | 1 | PASSIVE | 10,19 | 20 | 81041 |
| Wavespeaker's Blessing | 381946 | 2 | PASSIVE | 10,20 | 20 | 103430,81041 |
| Double Dip | 1252882 | 1 | PASSIVE | 11,15 | 20 | 103434 |
| Primal Tide Core | 382045 | 1 | PASSIVE | 11,17 | 20 | 103433,81043,81052 |
| Coalescing Water | 470076 | 1 | PASSIVE | 11,19 | 20 | 103427,103915,81052 |
| Deeply Rooted Elements | 378270 | 1 | PASSIVE | 11,21 | 20 | 103427,103430 |
| Stormstream Totem | 1267016 | 1 | ACTIVE | 12,18 | 20 | — |

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

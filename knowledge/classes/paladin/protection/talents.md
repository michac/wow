---
title: Paladin Protection — talent tree (12.1.0)
patch: 12.1.0
build: 12.1.0.68914
fetched: 
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.1.0.68914 (Tier 1)
confidence: high
---
> **Build provenance.** This file was generated from the Blizzard Game Data API and
> wago `Trait*` DB2 at build **12.1.0.68914**, which is what the API's `static-12.1.0`
> namespace reported on 2026-08-11. The live client that day was **12.1.0.69214**. The
> `Trait*` DB2 exports at the two builds are **byte-identical** (verified by md5 on
> `TraitNodeEntry`), so this data is valid for live 12.1 — cite it as **@ 12.1.0.68914**,
> not 69214.


# Paladin Protection — talents (12.1.0)

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
| Afterimage | 385414 | 1 | PASSIVE | 4,2 | — | 109999,103859,81507 |
| Guided Prayer | 404357 | 1 | PASSIVE | 4,3 | — | 109999 |
| Divine Steed | 190784 | 1 | ACTIVE | 4,4 | — | 109999,81598,81600 |
| Light's Countenance | 469325 | 1 | PASSIVE | 4,5 | — | 81598 |
| Greater Judgment | 231663 | 1 | PASSIVE | 4,6 | — | 81510,81598 |
| Wrench Evil / Stand Against Evil | 460720 / 469317 | 1/1 | CHOICE | 4,7 | — | 93010 |
| Holy Reprieve | 469445 | 1 | PASSIVE | 5,1 | — | 93188,103858 |
| Cavalier | 230332 | 1 | PASSIVE | 5,3 | — | 81632 |
| Divine Spurs | 469409 | 1 | PASSIVE | 5,4 | — | 81632 |
| Steed of Liberty / Blessing of Freedom | 469304 / 1044 | 1/1 | CHOICE | 5,5 | — | 81632 |
| Rebuke | 96231 | 1 | ACTIVE | 5,7 | — | 81603,103855 |
| Obduracy | 385427 | 2 | PASSIVE | 6,2 | 8 | 81605,103860,93188 |
| Divine Toll | 375576 | 1 | ACTIVE | 6,4 | 8 | 81631,81605 |
| Unbound Freedom | 305394 | 1 | PASSIVE | 6,5 | 8 | 81631 |
| Sanctified Plates | 402964 | 2 | PASSIVE | 6,6 | 8 | 81604,81631,81603 |
| Punishment | 403530 | 1 | PASSIVE | 6,7 | 8 | 81604 |
| Divine Reach | 469476 | 1 | PASSIVE | 7,1 | 8 | 81630,103860 |
| Brought to Light | 1265549 | 1 | PASSIVE | 7,2 | 8 | 81630 |
| Blessing of Sacrifice | 6940 | 1 | ACTIVE | 7,3 | 8 | 81630,110006,81605 |
| Divine Resonance / Quickened Invocation | 386738 / 379391 | 1/1 | CHOICE | 7,4 | 8 | 110006 |
| Blessing of Protection | 1022 | 1 | ACTIVE | 7,5 | 8 | 93009,110006,93187 |
| Fear No Evil | 1265541 | 1 | PASSIVE | 7,6 | 8 | 93009 |
| Consecrated Ground | 204054 | 1 | PASSIVE | 7,7 | 8 | 93009,93165 |
| Holy Aegis | 385515 | 1 | PASSIVE | 8,2 | 8 | 109998,93168,81614 |
| Sacrifice of the Just / Recompense | 384820 / 384914 | 1/1 | CHOICE | 8,3 | 8 | 81614 |
| Sacred Strength / Divine Purpose | 469337 / 223817 | 1/1 | CHOICE | 8,4 | 8 | 81614,81616 |
| Improved Blessing of Protection | 384909 | 1 | PASSIVE | 8,5 | 8 | 81616 |
| Unbreakable Spirit | 114154 | 1 | PASSIVE | 8,6 | 8 | 109997,81543,81616 |
| Lightforged Blessing | 406468 | 1 | PASSIVE | 9,1 | 23 | 93168,81609 |
| Lightforged Blessing | 406468 | 1 | PASSIVE | 9,1 | 23 | 81609,93168 |
| Lead the Charge | 469780 | 1 | PASSIVE | 9,2 | 23 | 81609,81607 |
| Worthy Sacrifice / Righteous Protection | 469279 / 469321 | 1/1 | CHOICE | 9,3 | 23 | 81607 |
| Holy Ritual | 199422 | 1 | PASSIVE | 9,4 | 23 | 93192,81607 |
| Blessed Calling | 469770 | 1 | PASSIVE | 9,5 | 23 | 81617,93192 |
| Inspired Guard | 469439 | 1 | PASSIVE | 9,6 | 23 | 81617,81615 |
| Light's Revocation | 146956 | 1 | PASSIVE | 9,7 | 23 | 81615,81543 |
| Faith's Armor | 406101 | 1 | PASSIVE | 10,1 | 23 | 103850,103853,103867 |
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
| Avenger's Shield | 31935 | 1 | ACTIVE | 2,18 | — | — |
| Shining Light | 321136 | 1 | PASSIVE | 3,17 | — | 81502 |
| Hammer of the Righteous / Blessed Hammer | 53595 / 204019 | 1/1 | CHOICE | 3,19 | — | 81502 |
| Valiant Crusade / Blessed Word | 1245979 / 1301732 | 1/1 | CHOICE | 4,16 | — | 81489 |
| Grand Crusader | 85043 | 1 | PASSIVE | 4,18 | — | 81469,81489 |
| Imbued Shield / Redoubt | 1276945 / 280373 | 1/1 | CHOICE | 4,20 | — | 81469 |
| Blessing of Spellwarding / Uther's Counsel | 204018 / 378425 | 1/1 | CHOICE | 5,17 | — | 81487,81476 |
| Ardent Defender | 31850 | 1 | ACTIVE | 5,18 | — | 81487 |
| Searing Sunlight / Hand of the Protector | 1244070 / 315924 | 1/1 | CHOICE | 5,19 | — | 81494,81487 |
| Refining Fire | 469883 | 1 | PASSIVE | 6,16 | 8 | 110862,81476 |
| Bulwark of Order | 209389 | 1 | PASSIVE | 6,17 | 8 | 81481,110862 |
| Avenging Wrath | 31884 | 1 | ACTIVE | 6,18 | 8 | 81481 |
| Light of the Titans / Tirion's Devotion | 378405 / 392928 | 1/1 | CHOICE | 6,19 | 8 | 81501,81481 |
| Solace / Instrument of the Divine | 1245891 / 1277162 | 1/1 | CHOICE | 6,20 | 8 | 81494,81501 |
| Tyr's Enforcer | 378285 | 2 | PASSIVE | 7,15 | 8 | 81486 |
| Undying Embers | 1244019 | 1 | PASSIVE | 7,16 | 8 | 81486 |
| Relentless Inquisitor | 383388 | 1 | PASSIVE | 7,17 | 8 | 81483,81499 |
| Improved Ardent Defender / Seal of Reprisal | 393114 / 377053 | 1/1 | CHOICE | 7,18 | 8 | 81483 |
| Crusader's Judgment | 204023 | 1 | PASSIVE | 7,19 | 8 | 81483,81503 |
| Vision of Sanctity | 1245354 | 1 | PASSIVE | 7,20 | 8 | 101927,81503 |
| Consecration in Flame | 379022 | 2 | PASSIVE | 7,21 | 8 | 101927 |
| Soaring Shield / Focused Enmity | 378457 / 378845 | 1/1 | CHOICE | 8,16 | 8 | 81492,81506,81474 |
| Guardian of Ancient Kings | 86659 | 1 | ACTIVE | 8,18 | 8 | 90062,81612,81506 |
| Sanctuary | 379021 | 1 | PASSIVE | 8,20 | 8 | 81612,81485,81470 |
| Strength in Adversity / Crusader's Resolve | 393071 / 380188 | 1/1 | CHOICE | 9,15 | 20 | 101928,81474 |
| Gift of the Golden Val'kyr | 378279 | 1 | PASSIVE | 9,17 | 20 | 81490 |
| Empyrean Authority | 1246481 | 1 | PASSIVE | 9,19 | 20 | 81490 |
| Seal of Charity | 384815 | 1 | PASSIVE | 9,21 | 20 | 81488,81485 |
| Ferren Marcus's Fervor | 378762 | 2 | PASSIVE | 10,16 | 20 | 81484,101928,81493 |
| Sentinel | 389539 | 1 | ACTIVE | 10,18 | 20 | 81484,81490,103877 |
| Zealot's Paragon | 391142 | 2 | PASSIVE | 10,20 | 20 | 81488,81498,103877 |
| Sweeping Verdict / Adjudication | 1246488 / 1277005 | 1/1 | CHOICE | 11,15 | 20 | 81482,81493 |
| Bulwark of Righteous Fury | 386653 | 1 | PASSIVE | 11,17 | 20 | 81484,81482,81497 |
| Final Stand | 204077 | 1 | PASSIVE | 11,19 | 20 | 81471,81497,103877 |
| Righteous Protector | 204074 | 1 | PASSIVE | 11,21 | 20 | 81498,81471 |
| Glory of the Vanguard | 1267203 | 1 | ACTIVE | 12,18 | 20 | — |

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

## Hero: Lightsmith

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Holy Bulwark | 432459 | 1 | ACTIVE | 7,11 | — | — |
| Holy Armaments | 432459 | 1 | ACTIVE | 7,11 | — | — |
| Rite of Sanctification / Rite of Adjuration | 433568 / 433583 | 1/1 | CHOICE | 8,9 | — | 95234,110257 |
| Solidarity | 432802 | 1 | PASSIVE | 8,10 | — | 95234,110257 |
| Divine Guidance / Blessed Assurance | 433106 / 433015 | 1/1 | CHOICE | 8,11 | — | 95234,110257 |
| Masterwork | 1271387 | 1 | PASSIVE | 8,12 | — | 110257,95234 |
| Laying Down Arms | 432866 | 1 | PASSIVE | 9,9 | — | 95233 |
| Divine Inspiration / Forewarning | 432964 / 432804 | 1/1 | CHOICE | 9,10 | — | 95228 |
| Authoritative Rebuke / Tempered in Battle | 469886 / 469701 | 1/1 | CHOICE | 9,11 | — | 95235 |
| Hammer and Anvil | 433718 | 1 | PASSIVE | 9,12 | — | 109742 |
| Shared Resolve | 432821 | 1 | PASSIVE | 10,9 | — | 95236 |
| Valiance | 432919 | 1 | PASSIVE | 10,10 | — | 95231 |
| Reflection of Radiance | 1271466 | 1 | PASSIVE | 10,11 | — | 95232 |
| Resounding Strike | 1271553 | 1 | PASSIVE | 10,12 | — | 109743 |
| Blessing of the Forge | 433011 | 1 | PASSIVE | 11,11 | — | 95238,95229,95237,109744 |

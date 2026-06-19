---
title: Mage Arcane — talent tree (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-06-19
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)
  - https://wago.tools/db2 Trait* @ 12.0.7.67808 (Tier 1)
confidence: high
---

# Mage Arcane — talents (12.0.7)

> Generated from `knowledge/classes/_talents/all-talents.tsv`. Spell IDs are the talent's granted spell. Choice nodes show both options as `A / B`. See `_talents/README.md` for the schema.

## Class tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Prismatic Barrier | 235450 | 1 | ACTIVE | 1,4 | — | — |
| Alter Time | 342245 | 1 | ACTIVE | 2,3 | — | 62121 |
| Ice Block | 45438 | 1 | ACTIVE | 2,5 | — | 62121 |
| Time Walk / Temporal Realignment | 1244087 / 1244090 | 1/1 | CHOICE | 3,2 | — | 62115 |
| Master of Time | 342249 | 2 | PASSIVE | 3,3 | — | 62115 |
| Winter's Protection | 382424 | 2 | PASSIVE | 3,5 | — | 62122 |
| Frost Conditioning | 1250315 | 1 | PASSIVE | 3,6 | — | 62122 |
| Arcane Warding | 383092 | 2 | PASSIVE | 4,2 | — | 62102,108654 |
| Inspired Intellect | 458437 | 1 | PASSIVE | 4,4 | — | 62123,62102 |
| Mirror Image | 55342 | 1 | ACTIVE | 4,6 | — | 62107,62123 |
| Spellsteal | 30449 | 1 | ACTIVE | 5,1 | 8 | 62114 |
| Quick Witted | 382297 | 1 | PASSIVE | 5,3 | 8 | 108660,62114 |
| Dragon's Breath / Supernova | 31661 / 157980 | 1/1 | CHOICE | 5,4 | 8 | 108660 |
| Remove Curse | 475 | 1 | ACTIVE | 5,5 | 8 | 108660,62124 |
| Improved Conjuration | 1244025 | 2 | PASSIVE | 5,7 | 8 | 62124 |
| Improved Spellsteal | 1270827 | 1 | PASSIVE | 6,1 | 8 | 62084 |
| Shimmer / Improved Blink | 212653 / 1244340 | 1/1 | CHOICE | 6,2 | 8 | 62104,62084 |
| Improved Counterspell | 1270865 | 1 | PASSIVE | 6,3 | 8 | 62104 |
| Overflowing Energy | 390218 | 1 | PASSIVE | 6,4 | 8 | 62116,62104,101883 |
| Improved Remove Curse | 1270847 | 1 | PASSIVE | 6,5 | 8 | 62116 |
| Greater Invisibility | 110959 | 1 | ACTIVE | 6,6 | 8 | 62116,108662 |
| Improved Frost Nova / Ice Ward | 343183 / 205036 | 1/1 | CHOICE | 7,1 | 8 | 62105,110082 |
| Captured Thoughts | 1270872 | 1 | PASSIVE | 7,2 | 8 | 62105 |
| Tome of Rhonin | 382493 | 1 | PASSIVE | 7,3 | 8 | 62105,108661,110079 |
| Tome of Antonidas | 382490 | 1 | PASSIVE | 7,5 | 8 | 108661,93524,110078 |
| Incantation of Swiftness | 382293 | 2 | PASSIVE | 7,6 | 8 | 93524 |
| Master of Escape | 210476 | 1 | PASSIVE | 7,7 | 8 | 93524 |
| Charm of Aegwynn | 1244105 | 1 | PASSIVE | 8,2 | 20 | 62110,62127,62125 |
| Brainstorm | 461261 | 1 | PASSIVE | 8,3 | 20 | 62127 |
| Flow of Time | 382268 | 1 | PASSIVE | 8,4 | 20 | 62098,62127 |
| Mana Confluence | 1270845 | 1 | PASSIVE | 8,5 | 20 | 62098 |
| Charm of Medivh | 1244107 | 1 | PASSIVE | 8,6 | 20 | 62112,108659,62098 |
| Permafrost Bauble | 1265517 | 1 | PASSIVE | 9,1 | 20 | 108658 |
| Freezing Cold / Ice Nova | 386763 / 157997 | 1/1 | CHOICE | 9,2 | 20 | 108658 |
| Time Manipulation | 387807 | 1 | PASSIVE | 9,3 | 20 | 62096,108658,110081 |
| Ring of Frost / Mass Polymorph | 113724 / 383121 | 1/1 | CHOICE | 9,4 | 20 | 62096 |
| Energized Barriers | 386828 | 1 | PASSIVE | 9,5 | 20 | 108657,62096,110080 |
| Mass Invisibility | 414664 | 1 | ACTIVE | 9,6 | 20 | 108657 |
| Barrier Diffusion | 455428 | 1 | PASSIVE | 9,7 | 20 | 108657 |
| Ice Cold | 414659 | 1 | PASSIVE | 10,2 | 20 | 62087,62086,62129 |
| Spatial Manipulation / Reflection | 1244031 / 1270829 | 1/1 | CHOICE | 10,4 | 20 | 62088,62129,62100 |
| Improved Prismatic Barrier | 321745 | 1 | PASSIVE | 10,6 | 20 | 62092,62091,62100 |

## Spec tree

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Arcane Missiles | 5143 | 1 | ACTIVE | 1,18 | — | — |
| Concentrated Power | 414379 | 1 | PASSIVE | 2,17 | — | 102467 |
| Arcane Salvo | 384452 | 1 | PASSIVE | 2,19 | — | 102467 |
| Amplification | 236628 | 1 | PASSIVE | 3,16 | — | 108538 |
| Improved Clearcasting | 321420 | 1 | PASSIVE | 3,18 | — | 108538,108539 |
| Arcing Cleave | 231564 | 1 | PASSIVE | 3,20 | — | 108539 |
| Arcane Pulse | 1241462 | 1 | ACTIVE | 4,16 | — | 102473 |
| Arcane Surge | 365350 | 1 | ACTIVE | 4,18 | — | 102445 |
| Arcane Orb | 153626 | 1 | ACTIVE | 4,20 | — | 102471 |
| Reverberate | 281482 | 1 | PASSIVE | 5,15 | 8 | 102439 |
| Presence of Mind / Slipstream | 205025 / 236457 | 1/1 | CHOICE | 5,17 | 8 | 102449,102439 |
| Mana Bomb | 457521 | 1 | PASSIVE | 5,18 | 8 | 102449 |
| Arcane Familiar | 205022 | 1 | PASSIVE | 5,19 | 8 | 102449,104113 |
| Charged Orb | 384651 | 1 | PASSIVE | 5,21 | 8 | 104113 |
| Intuition | 1223798 | 1 | PASSIVE | 6,16 | 8 | 102460,102462 |
| Touch of the Magi | 321507 | 1 | ACTIVE | 6,18 | 8 | 102469,102460 |
| Energized Familiar | 452997 | 1 | PASSIVE | 6,19 | 8 | 102469 |
| Expanded Mind | 1243557 | 1 | PASSIVE | 6,20 | 8 | 102475,102469 |
| Consortium's Bauble | 461260 | 1 | PASSIVE | 7,15 | 8 | 102446 |
| Arcane Tempo | 383980 | 1 | PASSIVE | 7,16 | 8 | 102446 |
| Aether Attunement | 1243307 | 2 | PASSIVE | 7,17 | 8 | 102446,102468 |
| Aegwynn's Technique / Arcane Echo | 1243507 / 342231 | 1/1 | CHOICE | 7,18 | 8 | 102468 |
| Resonance | 205028 | 1 | PASSIVE | 7,19 | 8 | 102441,102468,109002 |
| Impetus | 383676 | 1 | PASSIVE | 7,21 | 8 | 109002 |
| Evocation / Mana Adept | 12051 / 321526 | 1/1 | CHOICE | 8,16 | 20 | 110442,108535,108536 |
| Enlightened | 321387 | 1 | PASSIVE | 8,17 | 20 | 108535,102465 |
| Focusing Crystal | 461257 | 1 | PASSIVE | 8,19 | 20 | 102465,108541 |
| Illuminated Thoughts | 384060 | 1 | PASSIVE | 8,20 | 20 | 108541,102453 |
| Prodigious Savant | 384612 | 2 | PASSIVE | 9,16 | 20 | 102470,102454 |
| Eureka | 452198 | 1 | PASSIVE | 9,18 | 20 | 102451,102470 |
| Arcane Singularity | 1244001 | 2 | PASSIVE | 9,20 | 20 | 102451,108551 |
| High Voltage / Charged Missiles | 461248 / 461251 | 1/1 | CHOICE | 10,15 | 20 | 102480 |
| Overflowing Insight | 1243542 | 1 | PASSIVE | 10,17 | 20 | 102480 |
| Overpowered Missiles | 1244329 | 1 | PASSIVE | 10,18 | 20 | 108665 |
| Orb Mastery | 1243435 | 1 | PASSIVE | 10,19 | 20 | 108537 |
| Orb Barrage | 384858 | 1 | PASSIVE | 10,21 | 20 | 108537 |
| Touch of the Archmage | 1257942 | 1 | ACTIVE | 11,18 | 20 | — |

## Hero: Sunfury

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Spellfire Spheres | 448601 | 1 | PASSIVE | 7,10 | — | — |
| Mana Cascade | 449293 | 1 | PASSIVE | 8,9 | — | 94647 |
| Invocation: Arcane Phoenix | 448658 | 1 | PASSIVE | 8,10 | — | 94647 |
| Burden of Power | 451035 | 1 | PASSIVE | 8,11 | — | 94647 |
| Glorious Incandescence | 449394 | 1 | PASSIVE | 8,12 | — | 94647 |
| Merely a Setback / Time Twist | 449330 / 1255166 | 1/1 | CHOICE | 9,9 | — | 94653 |
| Codex of the Sunstriders | 449382 | 1 | PASSIVE | 9,10 | — | 94652 |
| Lessons in Debilitation / Explosive Potential | 449627 / 1246030 | 1/1 | CHOICE | 9,11 | — | 94644 |
| Pyrocosm | 1260673 | 1 | PASSIVE | 9,12 | — | 109675 |
| Savor the Moment / Sunfury Execution | 449412 / 449349 | 1/1 | CHOICE | 10,9 | — | 94649 |
| Ashes of Inspiration | 1260272 | 1 | PASSIVE | 10,10 | — | 94645 |
| Rondurmancy | 449596 | 1 | PASSIVE | 10,11 | — | 94651 |
| Spellfire Salvo | 1260616 | 1 | PASSIVE | 10,12 | — | 109674 |
| Memory of Al'ar | 449619 | 1 | PASSIVE | 11,10 | — | 94643,94650,94648,109673 |

## Hero: Spellslinger

| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |
|---|---|---|---|---|---|---|
| Splintering Sorcery | 443739 | 1 | PASSIVE | 2,10 | — | — |
| Augury Abounds | 1280165 | 1 | PASSIVE | 3,9 | — | 94664 |
| Force of Will | 444719 | 1 | PASSIVE | 3,10 | — | 94664 |
| Splintering Orbs | 444256 | 1 | PASSIVE | 3,11 | — | 94664 |
| Attuned Familiar / Shifting Shards | 1261106 / 444675 | 1/1 | CHOICE | 3,12 | — | 94664 |
| Slippery Slinging / Look Again | 444752 / 444756 | 1/1 | CHOICE | 4,9 | — | 94662 |
| Controlled Instincts | 444483 | 1 | PASSIVE | 4,10 | — | 94663 |
| Reactive Barrier / Phantasmal Image | 444827 / 444784 | 1/1 | CHOICE | 4,11 | — | 94661 |
| Infused Splinters | 1261080 | 1 | PASSIVE | 4,12 | — | 109669 |
| Archmage's Wrath | 444968 | 1 | PASSIVE | 5,9 | — | 94659 |
| Signature Spell | 470021 | 1 | PASSIVE | 5,10 | — | 94656 |
| Spellfrost Teachings | 444986 | 1 | PASSIVE | 5,11 | — | 94660 |
| Polished Focus | 1261082 | 1 | PASSIVE | 5,12 | — | 109668 |
| Splinterstorm | 443783 | 1 | PASSIVE | 6,10 | — | 94655,94658,94657,109667 |

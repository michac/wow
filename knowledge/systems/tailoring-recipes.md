---
title: Midnight Tailoring — full recipe inventory, sources, buy/skip verdicts
patch: 12.0.7
fetched: 2026-06-05
reviewed: 2026-07-07
sources:
  - Blizzard API /data/wow/profession/197/skill-tier/2918 + per-recipe (tier 1, static-12.0.5_66741)
  - wago.tools SkillLineAbility + SpellName, SkillLine 2918 (tier 1)
  - https://www.wow-professions.com/midnight/tailoring-guide (tier 3 — acquisition sources)
  - https://www.wow-professions.com/guides/wow-tailoring-leveling-guide (tier 3)
confidence: high
---

# Midnight Tailoring — recipe inventory (skill tier 2918)

Full catalog: **88 entries, 78 real recipes** (9 "Appendix" glossary entries +
Recraft Equipment are not learnable crafts). Raw data:
`raw/blizzard/midnight-tailoring-2918.json`, `midnight-tailoring-recipes.json`
(per-recipe mats), `raw/wago/sla-2918.json` (skill-up + grey thresholds).
Re-fetch with `tools/fetch_tailoring_recipes.py`.

⚠ API `reagents` omit quality-tiered reagents (bolts sit in modified-crafting
slots) — every "Mats" column below is **plus bolts**. 4 SkillLineAbility rows
have no live recipe (cut content, incl. a never-shipped Thalassian Fishing Hat).

`grey` = skill at which the craft stops giving skill-ups (from DB2
TrivialSkillLineRankHigh). First-craft KP is independent of grey — grey
recipes still give the first-craft bonus.

## Trainer — Galana, Silvermoon City (~160g/recipe, user-verified 2026-06-04)

29 recipes total: 2 auto-learned + 27 purchasable.

| Learn | Recipe | Grey | Mats (visible + bolts) | Verdict |
|---|---|---|---|---|
| auto | Bright Linen Bolt | 25 | 4 Silverleaf Thread | free |
| auto | Bright Linen Bandage | 20 | — | free |
| 5–30 | **Courtly ×9** (Wrists 5, Belt 10, Cloak/Gloves/Slippers 15, Pants 20, Helm 25, Robes/Shoulders 30) | 25–55 | 2–4 Thread, 0–3 Floss (vendor mats) + bolts | **BUY ALL** — ~1.45k for 9 first-crafts, ~200g/KP |
| 25 | Imbued Bright Linen Bolt | 45 | 4 Thread + 2 bolts | **BUY** — core leveling craft |
| 35 | Bright Linen Spellthread | 65 | 3 Floss + imbued bolts | **BUY** — leveling + sellable |
| 35 | Imbued Bright Linen Backpack | 55 | 3 Thread, **8 Fantastic Fur** + bolts | **BUY recipe**; check fur AH price before crafting spares — first craft fine |
| 35 | Bright Linen Reagent Satchel | 50 | 3 Thread, **8 Fantastic Fur** + bolts | same as above |
| ~35–40 | **Green profession gear ×6** (Alchemy Apron, Cooking Chapeau, Enchanting/Fishing/Herbalism Hats, Tailoring Robe) | 45 | 3–5 Thread + bolts | **BUY ALL** — cheap KP; equip the Tailoring Robe |
| 50 | Arcanoweave Reagent Rucksack | 80 | 2 Floss, 6 Mote of Pure Void + **Arcanoweave Bolts (daily CD)** | **BUY recipe, DEFER first craft** — see below |
| 50 | Sunfire Silk Backpack | 80 | 2 Floss, 6 Mote of Primal Energy + **Sunfire Silk Bolts (daily CD)** | **BUY recipe, DEFER first craft** — see below |
| 50 | **Wardrobe capes ×6** (Smuggler's, Silvermoon Agent's, Scout's, Farstrider's, Blood-Tempered, Spellbreaker's — warband cosmetic) | 80 | 2 Floss, 6 motes + **10 rare cloth + 32 CD bolts each** | **SKIP for leveling/KP** — vanity mat-sinks, see below |

⚠ **Cape mats verified 2026-06-05** (wago `ModifiedCraftingSpellSlot`,
tier 1; corroborated Wowhead): every cape's hidden slots are **10×
Arcanoweave/Sunfire Silk + 32× Arcanoweave/Sunfire Silk Bolt** — the
daily-CD bolts, ~140–175g each on AH (volatile) → **~5k+ gold of mats
per cape** for 1 first-craft KP. These are transmog prestige sinks
(Arcanoweave-themed: Smuggler's, Scout's, Blood-Tempered; Sunfire:
Silvermoon Agent's, Farstrider's, Spellbreaker's). Earlier verdict
"cheap KP" was wrong — it read only the visible API reagents.

**Skips despite first-craft bonus:**
- **Wardrobe capes ×6** — 32 CD bolts each. Only craft from your own
  bolt-CD surplus, and only if you want the cosmetic. Never for KP/skill.
- **Arcanoweave Rucksack / Sunfire Silk Backpack** — same CD-bolt trap,
  smaller scale. 160g recipes are harmless to own; **defer the first
  craft until your own bolt CD has spares.**

Everything else at Galana is unambiguous buy: Courtly + bolts +
spellthread + green prof gear + fur bags ≈ **3.4k gold for 21 recipes**
of first-craft KP — far under the ~1.5k/KP yardstick.

## Other vendors

| Vendor | Sells | Cost | Verdict |
|---|---|---|---|
| **Deynna** (Silvermoon, supply) | Elegant Artisan prof gear ×6 (blue), Thalassian prof gear ×5 (epic) | **150 Moxie each** | **SKIP for KP** — Moxie→KP via these is ~50–150 Moxie/KP; the renown book (below) is 7.5 Moxie/KP. Buy only what you'll use: Elegant Artisan's Tailoring Robe for your own gear, +1 Elegant recipe ~skill 90 for the 90–100 grind |
| **Deynna** | Chic Silvermoon Pillow, Plush Silvermoon Bed (house decor) | unverified | Decor uses Thalassian Lumber (8/46×) — buy if housing matters, KP value depends on lumber price |
| **Caeris Fairdawn** (Eversong, Silvermoon Court R5/R6) | Arcanoweave Spellthread (R5); **Skill Issue: Tailoring book = 10 KP for 75 Moxie (R6)** | Moxie | **Book is the best Moxie sink in the profession — buy first.** Spellthread recipe: epic leg enchant, strong gold-maker, buy when R5 |
| **Void Researcher Anomander** (Voidstorm, Singularity R5) | Lush Telogrus Carpet | unverified | housing-only |
| **Mirvedon** (Silvermoon, PvP) | Thalassian Competitor's set ×9 | unverified (likely gold/honor) | 9 first-crafts; mats = 2 Thread + 4 motes + 4 Carving Canine each + bolts. Check price in-game — if ~trainer-priced, worth it for KP even if you never PvP |

## Not purchasable (for completeness)

- **Spec nodes — Nimble Needlework**: Arcanoweave Bolt + Sunfire Silk Bolt
  (daily CDs), Arcanoweave/Sunfire Bracers, Cloaks, Treads (embellished sets)
- **Spec nodes — Sin'dorei Finery**: Martyr's ×8 + Adherent's Silken Shroud
  (epic armor, all 9 slots). Full names (wow-professions, raw cache
  2026-06-06): Crown (head), Mantle (shoulder), Vestments (chest),
  Bindings (wrist), Gloves (hands), **Waistwrap (waist)**, Leggings
  (legs), Slippers (feet) + Adherent's Silken Shroud (back).
  ⚠ Which of the three 3-slot sub-spec nodes covers which slots is
  still the open TODO — names alone don't reveal the grouping.
- **Drops**: Arcanoweave Cord (Heavy Trunk, Delves), Sunfire Sash (Restless
  Heart, Windrunner Spire), Arcanoweave Lining (Degentrius, Magisters'
  Terrace), Sunfire Silk Lining (Heavy Trunk, Delves), Sunfire Silk
  Spellthread (Fallen-King Salhadaar, Voidspire), Luxurious Silvermoon Lounge
  Cushion (Eversong treasures), Voidstrider Saddlebag (Stormarion Pinnacle)
- **Quest**: Silvermoon Curtains (Clothes Make the Man)

AH drop-recipe rule of thumb stands: buy only if price < ~1.5k per KP granted.

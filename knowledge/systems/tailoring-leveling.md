---
title: Midnight Tailoring — leveling 1–100, knowledge points, specs
patch: 12.0.5
fetched: 2026-06-03
sources:
  - https://www.wow-professions.com/guides/wow-tailoring-leveling-guide
  - https://www.wow-professions.com/midnight/tailoring-specialization-guide-and-builds
  - https://www.wowhead.com/guide/midnight/professions/tailoring-leveling-1-100
  - https://www.method.gg/guides/midnight-tailoring-profession-guide
  - https://www.icy-veins.com/wow/professions-tailoring
confidence: medium
---

# Midnight Tailoring (1–100)

Trainer: **Galana, Silvermoon City** (The Bazaar artisan area). All
leveling mats are AH-buyable; the whole path is solo-friendly.

## Leveling path

| Skill | Craft | Mats / notes |
|---|---|---|
| 1–25 | **Bright Linen Bolts ×66** | Bright Linen; keep crafting past grey ~20 — bolts feed later crafts. Vendor: Silverleaf Thread + Embroidery Floss |
| 25–40 | **Imbued Bright Linen Bolts ×14** | 28 bolts + 14 Eversinging Dust |
| 40–45 | **First-craft sweep** — profession-window filter "First Craft Bonus", craft each once | KP per first craft; equip the Bright Linen Tailoring Robe you make |
| 44–50 | **Courtly Shoulders ×6** | 12 bolts; repeat as needed |
| 50–80 | **Daily bolt cooldown** — Sunfire Silk Bolt *or* Arcanoweave Bolt (pick one; needs 5 KP in Nimble Needlework) | +2 skill/day, stays yellow to 80, **~2 weeks**; bolts sell — "slow & profitable." A rush path exists (Bright Linen Spellthread ×30 to ~100) — "fast & expensive" |
| 80–90 | **Lining recipes** | Recipes are world drops — buy from AH |
| 90–100 | **Elegant Artisan recipes** | 150 Artisan Tailor's Moxie each (tailoring vendor); green crafts — slow. Little reason to rush: guaranteed gold quality is far off regardless |

Early-stage cost estimate ~6–8k gold buying everything (tier-3/4,
medium confidence).

## Recipe acquisition — what to buy vs skip

- **1–50: all trainer-taught** (Galana) — no AH recipes needed.
  Trainer recipes cost **~160g each** (user-verified in-game
  2026-06-04). **Buy the whole Courtly line as it unlocks** (~9 recipes
  ≈ 1,450g): API-verified 2026-06-04 (Blizzard recipe endpoint, tier 1)
  — Courtly mats are vendor Silverleaf Thread/Embroidery Floss + ~2
  Bright Linen Bolts each, so each first-craft KP costs ~200g vs
  1–1.5k/KP from books. ⚠ API recipe `reagents` omits quality-tiered
  reagents (bolts live in modified-crafting slots) — cross-check guides.
  Full Midnight tier catalog (72 recipes, incl. Martyr's/Arcanoweave/
  Sunfire endgame garments): `raw/blizzard/midnight-tailoring-2918.json`
  (profession 197, skill tier 2918).
- **Daily bolt CD + endgame slot recipes: from KP spec nodes** (Nimble
  Needlework 5; each slot sub-spec's 10-pt node = that slot's recipe).
- **Lining recipes (80–90)**: AH world-drops — only needed if pushing
  past 80; defer until bolt dailies cap.
- **Elegant Artisan (90–100)**: Artisan Tailor's Moxie currency, not gold.
- **AH drop-recipes for first-craft KP**: value yardstick — vendor books
  ≈ **1–1.5k gold per KP**; buy a recipe only if price < ~1.5k per KP
  it grants (first crafts give 1–3 KP). Otherwise skip.

## Knowledge points

- **First crafts**: 1–3 KP per new recipe (the 40–45 sweep)
- **Crafting orders**: bonus KP for first fills of the week — **Patron
  Orders (NPC-generated, zero social contact)** also pay augment runes
  and skill-boost reagents
- **8 profession treasures** in Midnight zones — 3 KP each (24 total).
  TomTom waypoints (verified wow-professions / wowhead, 2026-06-14):
  ```
  /way #2393 35.9 61.3 A Really Nice Curtain (Tailoring)            # Silvermoon City
  /way #2393 31.8 68.2 Particularly Enchanting Tablecloth (Tailoring)# Silvermoon City
  /way #2395 46.3 34.8 Sin'dorei Outfitter's Ruler (Tailoring)      # Eversong Woods
  /way #2437 40.5 49.4 Artisan's Cover Comb (Tailoring)             # Zul'Aman
  /way #2413 69.8 51.0 Wooden Weaving Sword (Tailoring)             # Harandar
  /way #2413 70.5 50.9 A Child's Stuffy (Tailoring)                 # Harandar
  /way #2444 62.0 83.6 Book of Sin'dorei Stitches (Tailoring)       # Voidstorm
  /way #2444 61.6 85.0 Satin Throw Pillow (Tailoring)               # Voidstorm
  ```
  Map IDs: #2393 Silvermoon · #2395 Eversong · #2437 Zul'Aman ·
  #2413 Harandar · #2444 Voidstorm. (Harandar pair and Voidstorm pair
  each ~0.5 yd apart = single stops.)
- **Weekly trainer quest** — 3 KP
- **Vendor books** — 10 KP, ~10–15k gold each (optional catch-up)
- **Renown book "Skill Issue: Tailoring"** — 10 KP, sold by **Caeris
  Fairdawn, Eversong Woods** (`/way #2395 43.4 47.4`, Saltheril's Haven
  near Fairbreeze Village) for **75 Artisan Tailor's Moxie**, gated at
  **Renown 6 with Silvermoon Court**. Grab once at Renown 6.
  (Web tier-3, 2026-06-14: method.gg / misti.services / wowhead.)
- **~19 KP/week** from the four weekly sources: Patron Orders, weekly
  trainer quest, treatise, treasure/world-drops. ~40–50 KP reachable on
  day 1 (first crafts + 8 treasures + renown book if Renown 6).

## Specialization trees (four trees, not slot sub-specs)

Verified web tier-3, 2026-06-14 (wow-professions / method.gg / overgear):

- **Nimble Needlework** — daily bolt CD, embellished cloth (cloaks/
  bracers/treads), and **enables Sunfire Silk + Arcanoweave to drop from
  humanoid mobs** (the real value; guides say ~20 KP at skill 25 to turn
  drops on — supersedes the older "5 KP for bolt CD" claim; trust node
  tooltips in-game).
- **Sin'dorei Finery** — epic cloth armor recipes (the gear).
- **Fiber Arts** — flat skill on all recipes + crafting stats; the
  quality tree; prerequisite (with skill 100) for no-concentration gold.
- **Fabric Specialist** — boosts cloth drop rate while farming.

### Build order (gear-crafting)

1. **Nimble Needlework** — bolt CD + turn on mob cloth drops
2. **Sin'dorei Finery** — your epic recipe source
3. **Fiber Arts → ~30** — skill/quality; take **Resourcefulness side
   first** in sub-nodes. (Pick **Fabric Specialist** here instead only
   if farming/selling raw cloth rather than crafting your own gear.)
4. Profession gear: epic BiS; stat lean **Ingenuity + Resourcefulness**
   for endgame gear crafting (Multicraft + Ingenuity only for
   mass-producing bolts/consumables). Tool missives exist (Thalassian
   Missive of Ingenuity etc. — see `professions.md`)

## Expectations

Guaranteed gold (rank 5 without concentration) takes skill 100 + deep
spec investment — **weeks, not days**. Realistic interim goal:
self-recraft cloth pieces at rank 5 *using concentration* once skill
~80+, Fiber Arts 30, and the relevant slot sub-spec are in. Weapon
(Aln'hara Cane) is Inscription — always commissioned.

## TODO

- [x] Treasure locations (8 × 3 KP) — TomTom coords added 2026-06-14
- [x] Weekly treatise confirmed (one of four weekly KP sources) — 2026-06-14
- [x] Renown KP book "Skill Issue: Tailoring" (Renown 6 Silvermoon
      Court, 75 Moxie, Caeris Fairdawn) — 2026-06-14
- [ ] Which Finery node covers wrist (Martyr's Bindings) vs belt/boots
- [ ] Artisan Tailor's Moxie earn rate

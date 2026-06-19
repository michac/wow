---
title: Midnight Tailoring — leveling 1–100, knowledge points, specs
patch: 12.0.7
fetched: 2026-06-19
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
- **8 profession treasures** in Midnight zones — 3 KP each (24 total)
- **Weekly trainer quest** — 3 KP
- **Vendor books** — 10 KP, ~10–15k gold each (optional catch-up)

## Specialization order (gear-crafting build)

1. **Nimble Needlework 5–10 first** — unlocks the daily bolt CD (5) and
   the Arcanoweave Bolt recipe path (10)
2. **Fiber Arts root → 30** — flat skill on all recipes + passive
   stats; prerequisite for no-concentration gold quality (needs this +
   skill 100). In its sub-nodes take **Resourcefulness side first**
3. **Slot sub-specializations**: 5 KP root unlock → pick the
   sub-spec for the slot you want → 10 KP unlocks that slot's recipe.
   With profession gear + decent skill you can then craft that slot at
   rank 5 **with concentration** long before guaranteed gold
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

- [ ] Treasure locations (8 × 3 KP) — coords per zone
- [ ] Verify Midnight has/lacks DF-style weekly treatise for KP
- [ ] Which slot sub-spec covers wrist (Martyr's Bindings) vs
      belt/boots — node names
- [ ] Artisan Tailor's Moxie earn rate

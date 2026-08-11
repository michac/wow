---
title: Midnight Tailoring — leveling 1–100, knowledge points, specs
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://www.wow-professions.com/guides/wow-tailoring-leveling-guide
  - https://www.wow-professions.com/midnight/tailoring-specialization-guide-and-builds
  - https://www.wowhead.com/guide/midnight/professions/tailoring-leveling-1-100
  - https://www.method.gg/guides/midnight-tailoring-profession-guide
  - https://www.icy-veins.com/wow/professions-tailoring
  - https://worldofwarcraft.com/en-us/news/24293281        # 12.1 "Curse of Ula'tek" content update notes (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963  # Follow the Snakes to the Coiled Isle (Tier 1)
  - https://www.icy-veins.com/wow/news/renown-and-vendor-rewards-zone-talents-corrosive-powers-new-coiled-isle-zone-in-12-1-and-everything-on-it-detailed/  # Zul'jarra renown rank-by-rank listing (Tier 3 — corroborates the Tier-1 article, does not override it)
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
  ⚠ **12.1 added a second Moxie sink** at **Jan'sari the Watchful**
  (Zul'jarra's Forces quartermaster, **Tokka's Landing**, Coiled Isle), whose
  stock is priced in **Voidlight Marl + profession-specific Artisan Moxies**
  rather than gold. Two renown ranks carry profession content, and only one of
  them really matters to a tailor:
  - **Renown 5 — "Coiled Isle Crafting"**: nine purchasable recipes, of which
    exactly one is Tailoring — **Pattern: Flat Snakeskin Canopy** (item
    275332), a **decor** pattern. Nice to have, not a skill-up or gear recipe.
  - **Renown 6 — "Demystifyin' Professions"**: **profession knowledge tomes**
    go on sale. *This* is the Moxie-relevant sink for a tailor, because it buys
    KP (see below), and KP is what actually gates this file's spec plan.
  - **Renown 7 is furnishings only** (bags, weapon rack) — no profession content.

  So Moxie is no longer a single-purpose skill-up currency: budget it against
  the Elegant Artisan recipes **and the R6 tomes**. The zone, the vendor, the
  rank gates and the currencies are Tier-1 (Blizzard 12.1 Coiled Isle article,
  recipe names resolved against game data); only the **tome price** is
  unconfirmed — Tier-4 guides quote **750 Voidlight Marl + 75 or 150 Artisan
  Tailor's Moxie** per tome and `systems/professions.md` carries the
  in-game-verify marker for it. See `factions/zuljarras-forces.md` and
  `systems/professions.md`. **The 1–100 crafting route below is unaffected** —
  12.1 adds no new leveling recipes and changes no mats; what it does change is
  where KP comes from and how it can be re-spent.
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
- **Jan'sari's profession knowledge tomes (12.1, new)** — unlocked at
  **Zul'jarra's Forces Renown 6** ("Demystifyin' Professions"), bought with
  Voidlight Marl + Artisan Tailor's Moxie (price unconfirmed — see above).
  This is the one new KP faucet in 12.1, and it is the reason R6 is the
  profession breakpoint on that renown track.

⚠ **One-time Knowledge Point reset (12.1)** — once per Midnight profession,
every KP spent in that profession's specialization trees is refunded and can be
re-assigned from scratch. **Recipes unlocked by spending those points are
unlearned by the reset** and only come back when you re-spend, so do not fire it
half-way through a plan. Base skill, Artisan Moxie balances and banked
(unspent) knowledge are untouched. It is **permanent and single-use** — save it
for a real mis-spend. Detail + provenance (not in the official notes; Wowhead
relay corroborated by Method, with an in-game-verify marker) lives in
`professions.md`.

## Specialization order (gear-crafting build)

> **Read the KP-reset note above before spending.** The spend order below is
> a one-way commitment *per reset*: you now get exactly one free do-over per
> profession, and using it unlearns the slot recipes these nodes granted until
> the points are re-placed.

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

- [ ] **Artisan Tailor's Moxie earn rate — now load-bearing.** 12.1 gave Moxie a
      second sink (Jan'sari's R6 knowledge tomes) on top of the Elegant Artisan
      recipes at 150 each, so "can I afford both?" is a real planning question
      and we have no earn rate at all. Resolve with the tome price
      (already marked for in-game verification in `professions.md`) at the
      same time.
- [ ] Treasure locations (8 × 3 KP) — coords per zone
- [ ] Verify Midnight has/lacks DF-style weekly treatise for KP
- [ ] Which slot sub-spec covers wrist (Martyr's Bindings) vs
      belt/boots — node names

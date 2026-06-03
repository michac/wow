---
title: Ritual Sites & Field Accolades (12.0.5)
patch: 12.0.5
fetched: 2026-06-03
sources:
  - https://www.youtube.com/watch?v=e6GLeeqwV4U  # SignsOfKelani, 2026-04-26
  - https://www.icy-veins.com/wow/midnight-1205-guide
confidence: medium
---

# Ritual Sites (12.0.5)

**Instanced solo-friendly content** added in 12.0.5; the fastest reliable
solo path to hero-track gear. (Earlier KB note calling this "open-world"
was wrong.)

## Structure

- **5 difficulty tiers**; higher tier = more Field Accolades. **1–5
  players** (instanced scenario).
- **One ritual site active per week**, rotating Eversong Woods ↔
  Zul'Aman. Runs at the active site are **repeatable without limit**.
- **Reward gates**: accolades are **uncapped** — verified tier 1
  (CurrencyTypes DB2 2026-06-03: ID 3405 MaxQty=0, MaxEarnablePerWeek=0,
  no cap world state); crests count toward
  the **100/week per-tier Dawncrest cap** → ~5 T5 runs/week saturate
  Hero crests (`../endgame/dawncrests.md`). Coffer key shards also drop.
- **Sequential unlock**: each tier must be completed to open the next —
  no skipping straight to T5 on fresh characters.
- **T5 UI-recommended ilvl: 264** (tier-4 sourced; corroborate). T5 also
  **requires ≥4 active challenges**. Challenges first appear at T3.
- **Death penalty**: first 2 deaths free, then **−5% spoils each, max
  −50%** — deaths cut rewards, not completion.
- Challenge stacking: ~+75% spoils possible at T5 (Embers + Malevolent
  Boons + two 15% modifiers).
- **Challenges** (optional modifiers) multiply the final score. Unlocked
  via quests from NPCs in Silvermoon near the gear vendors + treasures/
  items inside the sites.
- Scoring favors **mini-bosses and bosses; trash gives little** — skip
  trash. Challenges that fight this strategy (avoid for fast runs):
  **Reinforced** (more mobs to skip), **Embers** (must kill mobs to strip
  boss buffs), **Malevolent Boons** (detour to destroy obelisks).
- Benchmark: ~ilvl 256 character clears tier 5 in **10–15 min**.

## Rewards (tier 5)

- **100+ Field Accolades** per run
- **20 Hero Dawncrests** per run (≈5 runs = a hero vendor piece + enough
  crests to fully upgrade it)
- Coffer key shards (reduces need to farm prey/world events for keys)
- **Great Vault**: tier 4–5 ritual sites beat delve T8 for the world row —
  up to **ilvl 269 vault** (hero track; myth vault still requires M+10/raid)

## Field Accolades & gear vendors (Silvermoon)

- **Champion piece: 75 accolades · Hero piece: 500 accolades**
- ⚠ **The purchased piece is a RANDOM slot** (like prey/delve loot), not
  a targeted buy — per video comments (tier 4; verify in-game/Icy Veins).
  Expected value is high while you own little-to-no hero gear (almost any
  roll upgrades) and decays as hero slots fill (duplicate risk: ~1 hour
  of farming can whiff). Plan to pivot to targeted sources (vault, M+
  dungeon-specific drops, spark crafts) once roughly half your slots are
  hero-track.
- Vendors also stock cosmetics (décor, mounts, pets, transmog).
- Other sources: Void Strikes (8 each) and Void Incursions (30 each) in
  Eversong Woods / Zul'Aman — much slower than ritual sites and Void
  Strikes were bugged as of late April 2026. Dark Particles convert at
  the vendor at **100 particles → 10 accolades** (tier 4, boostmatch.gg
  farm guide — corroborate in-game).
- **12.0.7 (2026-06-16) adds a second real source**: Showdown zones
  (Naigtal/Val) pay accolades from WQs/rares/objectives, increased in
  Heroic World Tier; also slot-targeted 750-accolade hero caches and
  ritual T6. See `../_meta/next-patch.md`.
- **Not warbound**: accolades and dark particles can't be transferred;
  each character farms its own.

## Ritual-site renown track (account-wide)

Separate renown track; unlocks persist for alts:

- **Rank 4**: rare mobs spawn (kill for extra spoils → faster accolades)
- **Rank 5**: shrines of power, regeneration-orb bonuses, larger treasures

## TODO

- [ ] Exact tier → accolade/crest table (corroborate vs Icy Veins 12.0.5
      guide, tier 3)
- [ ] Full challenge list + multipliers
- [ ] Vendor inventory (which slots purchasable; weapon/trinket available?)
- [x] Dark particles → accolades at vendor, 100:10 (tier 4, 2026-06-03 —
      still corroborate the ratio in-game)

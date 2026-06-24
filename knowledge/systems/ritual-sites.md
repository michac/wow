---
title: Ritual Sites & Field Accolades (12.0.5)
patch: 12.0.5
fetched: 2026-06-03
sources:
  - https://www.youtube.com/watch?v=e6GLeeqwV4U  # SignsOfKelani, 2026-04-26
  - https://www.icy-veins.com/wow/midnight-1205-guide
  - https://www.method.gg/guides/field-accolades-vendor-location-and-rewards
  - https://skycoach.gg/blog/wow/articles/ritual-sites-guide
  - https://conquestcapped.com/guides/wow/midnight-delves-rewards/  # accolade:spoils ratio
  - https://seramate.com/news/2026/05/22/maren-silverwing-gear-caches-patch-1207-1f155eb2
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
- Scoring favors **objectives, mini-bosses and bosses; unmarked trash
  gives ~nothing** — skip trash.
- Benchmark: ~ilvl 256 character clears tier 5 in **10–15 min**.

## Run structure (Overgear/Wowhead, 2026-06-03)

Enter via the **Curious Obelisk** (also where tier + challenges are
chosen). Staged: **objectives → mini-boss → boss → Ritual Chest**
(chest value = Spoils × challenge modifiers − death penalty). Stage-1
objective types vary by site: Corrupted Wildlife, Void Reinforcements,
Rituals in the Depths, Face Off (Warlord Gurrtack), Research Trove.
Only **marked** enemies count toward kill stages.

## Challenges (all 8 — Overgear 2026-06-03, tier 4; corroborate in-game)

Toggled at the obelisk; available T3+, **T5 requires ≥4 active**.

| Challenge | Effect | Spoils | Unlock |
|---|---|---|---|
| Tendrils | dodge green swirls | +10% | found in Ritual Spoils chest |
| Manifestations | spirits spawn | +15% | complete Tier 3 |
| Magical Alarm Bells | kills spawn adds | +10% | Tier 4 + Lady Darkglen (Bazaar) |
| Malevolent Boons | destroy buff obelisks | +15% | Tier 2 + Lady Darkglen |
| Tainted Corpses | kills leave void zones | +10% | **Tainted Bone Pile** (in-site, off-path) |
| Reinforced | more enemies | +25% | Tier 2 + Ranger Captain Lilatha |
| Patrols | elite patrols | +10% | T3+ in-site treasures |
| Embers | empowered enemies | +15% | **Embers of Power** (in-site, T4+) |

**Fast-skip 4-stack: Tendrils + Manifestations + Tainted Corpses +
Patrols (+45%)** — none force trash kills. Avoid for speed:
**Reinforced** (more mobs to skip), **Embers** (kill mobs to strip
buffs), **Malevolent Boons** (obelisk detours) — bigger % but slower
runs.

## Items found inside sites

Challenge keys: Tainted Bone Pile, Embers of Power, T3+ treasures
(Patrols), Tendrils via spoils chest. Collectible triggers:
**Misplaced Ritual Candle** → bring to ritual circle → Void-Corrupted
Hex Eagle mount; **Practically Pork ×5** → warbear mount; **Washed Up
Kelp / Void-Bathed Snapdragon** → snapdragon spawn / pet. Don't vendor
oddball loot.

## Rewards (tier 5)

- **100+ Field Accolades** per run
- **20 Hero Dawncrests** per run (≈5 runs = a hero vendor piece + enough
  crests to fully upgrade it)
- Coffer key shards (reduces need to farm prey/world events for keys)
- **Great Vault**: tier 4–5 ritual sites beat delve T8 for the world row —
  up to **ilvl 269 vault** (hero track; myth vault still requires M+10/raid)

## Accolades per run (added 2026-06-05)

- **Accolades ≈ Spoils ÷ 10, rounded down** (ConquestCapped: 330 spoils
  → 32, 507 → 50). Spoils scale with tier, challenges (+10–25% each),
  and performance; deaths past 2 cut up to −50%.
- Anchors: **T5 ≈ 100+/run** (Kelani) · **T6 (12.0.7) ≈ another
  100+** · mid-tier examples above suggest **T3 ≈ 30–50/run** clean
  (estimate — no direct T3 source; verify in-game from the chest).
- Challenge picks for weaker characters (skycoach + Overgear agree):
  **take Tendrils (+10%) and Tainted Corpses (+10%)** — both are
  just movement checks; add Manifestations/Patrols if comfortable.
  **Avoid Embers (+25%) and Magical Alarm Bells** (skycoach: worst
  solo offenders; Embers spawns empowerments enemies claim), and skip
  Reinforced/Malevolent Boons for run speed.
- ⚠ Source conflict: this file (Overgear) says only **T5 requires ≥4
  challenges**; ConquestCapped says T3/T4/T5 all *require* adding
  challenges. Check the obelisk UI at T3.

## Field Accolades & gear vendors (Silvermoon — Maren Silverwing)

- **12.0.5 live: Cache of Void-Touched Armaments — Champion 75
  accolades · Hero 500 accolades** (Method.gg 2026-06-05: both are
  **random** spec-appropriate items incl. rings/necks; duplicates
  possible).
- **12.0.7 (June 16, PTR-sourced — seramate/overgear/masterofwarcraft
  2026-05-22):**
  - slot-specific **Hero cache: 750**
  - random **Hero cache cut 500 → 100** (!)
  - slot-specific **Champion cache: 100, warbound** (single tier-4
    source — corroborate at patch)
  - i.e. every ~100 banked accolades ≈ one hero roll after June 16;
    banking now is even better than the 750-cache math alone.
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
- [x] Full challenge list + multipliers (2026-06-03, Overgear — tier 4;
      verify %s in-game at the obelisk)
- [ ] Vendor inventory (which slots purchasable; weapon/trinket available?)
- [x] Dark particles → accolades at vendor, 100:10 (tier 4, 2026-06-03 —
      still corroborate the ratio in-game)

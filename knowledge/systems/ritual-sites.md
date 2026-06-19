---
title: Ritual Sites & Field Accolades (12.0.7)
patch: 12.0.7
fetched: 2026-06-19
sources:
  - https://www.youtube.com/watch?v=e6GLeeqwV4U  # SignsOfKelani, 2026-04-26
  - https://www.icy-veins.com/wow/midnight-1205-guide
  - https://www.icy-veins.com/wow/news/patch-12-0-7-revelations-full-content-update-notes/  # T6 details
  - https://www.wowhead.com/news/ritual-sites-in-patch-12-0-7-feature-more-difficulty-and-rewards-381858
  - https://news.blizzard.com/en-us/article/24244888/revelations-content-update-notes
confidence: medium
---

# Ritual Sites (12.0.7)

**Instanced solo-friendly content** added in 12.0.5; the fastest reliable
solo path to hero-track gear, and as of 12.0.7 "Revelations" a repeatable
solo source of **Mythic** Dawncrests too. (Earlier KB note calling this
"open-world" was wrong.)

## Structure

- **6 difficulty tiers** as of 12.0.7 (was 5 in 12.0.5); higher tier =
  more Field Accolades. **1–5 players** (instanced scenario).
- **One ritual site active per week**, now rotating **three** sites as of
  12.0.7 (was two in 12.0.5): **Daggerspine Point** (Eversong Woods),
  **Broken Throne** (Zul'Aman), and the new **Blinding Bloom** (Harandar,
  added 12.0.7). The third site is tier-4 sourced — corroborate in-game.
  Any specific site now comes up less often. Runs at the active site are
  **repeatable without limit**.
- **Reward gates**: accolades are **uncapped** — verified tier 1
  (CurrencyTypes DB2 2026-06-03: ID 3405 MaxQty=0, MaxEarnablePerWeek=0,
  no cap world state). **Dawncrest accumulation is also uncapped** — the
  old 100/tier/week cap was **removed in the May 19 2026 hotfix**, so ritual
  sites (a repeatable source) can be farmed for Hero/Myth crests without
  limit (`../endgame/dawncrests.md`). Coffer key shards also drop.
- **Sequential unlock**: each tier must be completed to open the next —
  no skipping straight to T5/T6 on fresh characters.
- **T5 UI-recommended ilvl: 264** (tier-4 sourced; corroborate). T5 also
  **requires ≥4 active challenges**. Challenges first appear at T3.
- **T6 (12.0.7) UI-recommended ilvl: 274**. T6 **requires all 6 standard
  challenges selected** (the achievement-only "all 8 active" run is
  harder still). T6 rewards Mythic Dawncrests — see Rewards below.
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

## Rewards (tier 6, 12.0.7)

- **5 Mythic Dawncrests + 10 Heroic Dawncrests** per run — the first
  repeatable **solo** source of Myth crests (Myth crests otherwise come
  from M+/raid). Crest accumulation is **uncapped** (the per-tier weekly cap
  was removed 2026-05-19), so T6 is a true repeatable Myth-crest farm
  (`../endgame/dawncrests.md`).
- Drops **ilvl ~270+ gear** (Tier-1/Tier-3 notes; corroborate exact range
  in-game).
- **Great Vault**: a T6 clear fills the world row at the same level as a
  **Heroic 4/6** raid drop / Tier-5 ritual — i.e. it does *not* push the
  vault above the Tier-5 hero cap despite paying Myth crests. Myth vault
  slots still require M+10/raid.
- Field Accolades, coffer key shards, and the in-site collectibles below
  all still drop.

### New weekly quests & bonus rolls (12.0.7)

- New **weekly quests** ask you to clear a Tier 6 site with specific
  challenges applied.
- On **Week 3 and Week 6** of the cadence, completing the weekly grants an
  extra **Bonus Roll**.

### New achievements (12.0.7)

- **Advanced Ritual Site Studies** — complete all 6 advanced challenges
  for Lady Darkglen.
- **Pinnacle Ritual Work** — complete **each** Ritual Site at Tier 6 with
  **all 8 challenges active** (Daggerspine Point, Broken Throne, and the new
  Blinding Bloom). Rewards the title **"Ritual Breaker."**

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
- **12.0.7 (live 2026-06-16) added a second real source**: the new
  Naigtal/Val worlds (reached by portal from Voidstorm, rotating weekly)
  pay accolades from WQs/rares/objectives, increased in Heroic World Tier;
  there are also slot-targeted 750-accolade hero caches, plus the Tier 6
  ritual difficulty above. See `../endgame/world-events.md`.
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

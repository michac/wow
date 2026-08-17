---
title: Ritual Sites & Field Accolades (12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # Curse of Ula'tek Content Update Notes (Tier 1) — EVENTS → RITUAL SITES
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 information (Tier 1) — pre-season week reward caps
  - wago.tools CurrencyTypes DB2 (via wowkb.wago, 12.1.0.69214)  # Tier 1 — Field Accolade 3405 still MaxQty=0/MaxEarnablePerWeek=0 AND names Maren Silverwing as the cache vendor; Mistcrest rows 3442-3446 MaxQty=100 behind world states 30933/30934 while MaxEarnablePerWeek=0 on all ten rows; the crest descriptions name their sources verbatim (Adventurer "Tier 4 Delves", Veteran "Delves T5-6", Myth 3441/3446 "Mythic The Venomous Abyss / Mythic Keystone +9 and up")
  - https://warcraft.wiki.gg/wiki/Cache_of_Void-Touched_Armaments:_Boots  # S2 cache slot / ilvl / binding detail (via systems/void-incursions.md)
  - https://www.icy-veins.com/wow/midnight-patch-12-1-guide  # Tier 3 — corroborates the T4/T5/T6 ilvls + "up to Veteran Mistcrests"
  - https://www.youtube.com/watch?v=e6GLeeqwV4U  # SignsOfKelani, 2026-04-26
  - https://www.icy-veins.com/wow/midnight-1205-guide
  - https://www.icy-veins.com/wow/news/patch-12-0-7-revelations-full-content-update-notes/  # T6 details
  - https://www.wowhead.com/news/ritual-sites-in-patch-12-0-7-feature-more-difficulty-and-rewards-381858
  - https://news.blizzard.com/en-us/article/24244888/revelations-content-update-notes
  - https://us.forums.blizzard.com/t/world-of-warcraft-midnight-hotfixes-june-30/2296045/359  # T6 quest pickup in Silvermoon (hotfix 2026-06-22)
confidence: medium
---

# Ritual Sites (12.1)

**Instanced solo-friendly content** added in 12.0.5 — instanced, not
open-world. 12.1 made **no ritual-site-specific changes** to
the structure, tiers, challenges or site rotation — what changed here is the
**reward tuning** (below).

⚠ But "no site-specific change" is **not** "plays the same." 12.1 shipped four
**global** class/combat changes that apply inside every instance, this one
included: **player health and creature damage both +25% at max level** (health
consumables rescaled; several DPS/Tank healing and absorb spells retuned),
**major DPS cooldowns lowered with steady-state damage raised** on several
specs, **interrupts now show a "missed" visual + sound** when the target was not
casting, and **diminishing-return categories now reset after 20s** (was 16).
That is the likeliest reason a tier feels different from your Season 1 memory of
it — and it lands on top of the T4–T6 recommended-ilvl bumps
(`../_meta/changelog-12.1.md`, "Four GLOBAL changes that apply to every spec").

## ⚠ 12.1 re-tiered the rewards — read this before quoting a payout

The 12.1 notes (EVENTS → RITUAL SITES, Tier 1, verbatim in
`../_meta/patch-notes/12.1.md`) say four things:

1. **Tier 1–6 Great Vault rewards now match Season 2 *Delve* tiers 1–6.**
2. **Ritual Sites now award Season 2 crests (Mistcrests) equivalent to Delves
   at these tiers.**
3. **Tiers 1–3 keep the Season 1 recommended item levels and tuning.** New
   recommended ilvls: **T4 259** (was 257) · **T5 268** (was 264) ·
   **T6 275** (was 274).
4. **The Tier 6 Advanced Ritual Studies quests no longer offer a Nebulous
   Voidcore bonus roll.** They remain completable for the achievement.

**What that costs you:** in 12.0.7 a T6 clear was the only *repeatable solo*
source of **Myth** crests and T4–T5 beat delve T8 for the world vault row.
Pegging the sites to **Delve tiers 1–6** ends both. Delve tiers 1–6 top out at
**Veteran** crests, and the delve vault row does not reach **Hero 1/6 (305)**
until **Tier 8** (`../endgame/delves/overview.md`) — so a T6 ritual site is now
a *mid*-ladder activity, not the ceiling. Tier-3 reporting agrees the sites now
pay "up to Veteran Mistcrests". ⚠ Blizzard published **no per-tier ritual table**
and **no per-run crest amounts** — those are the open questions. The *crest tier*
a given delve tier pays is **not** open: it is Tier-1 game data (below).

> **Pre-season note (week of 2026-08-11):** Season 2 opens **2026-08-18**. The
> Tier-1 pre-season post caps *Delves* at **Adventurer 3/6 gear + Veteran
> crests** and says nothing about Ritual Sites specifically — so whether the
> ritual payouts are additionally throttled this week is **unconfirmed**.
> @verify-ingame

## Structure

- **6 difficulty tiers** as of 12.0.7 (was 5 in 12.0.5); higher tier =
  more Field Accolades. **1–5 players** (instanced scenario).
- **One ritual site active per week**, now rotating **three** sites as of
  12.0.7 (was two in 12.0.5): **Daggerspine Point** (Eversong Woods),
  **Broken Throne** (Zul'Aman), and the new **Blinding Bloom** (Harandar,
  added 12.0.7). The third site is tier-4 sourced — corroborate in-game.
  Any specific site now comes up less often. Runs at the active site are
  **repeatable without limit**.
- **Reward gates**: accolades are **still uncapped in 12.1** — Tier-1 game data,
  re-read on the current build (`CurrencyTypes` DB2 @ `12.1.0.69214`, ID **3405**
  "Field Accolade": `MaxQty=0`, `MaxEarnablePerWeek=0`, `MaxQtyWorldStateID=0`).
  *(This is a fresh read, not the 12.0.x one — worth doing, because the same table
  demonstrably moved for S2: the crest rows now ship a cap where S1's did not.)*
- ⚠ **Crest accumulation: cap machinery is BACK in Season 2 — do not carry Season 1's
  "caps removed" forward.** The May-19-2026 hotfix that removed the 100/tier/week
  cap was a **Season 1** action and died with the season. The S2 crest rows carry
  **MaxQty 100** behind world states **30933** (Adventurer/Veteran/Champion) and
  **30934** (Hero/Myth) — the same machinery S1 used to raise its cap over time.
  ⚠ Read that field precisely: `MaxQty` is a **holding cap** (how many you may
  have at once), and **`MaxEarnablePerWeek` is 0 on every Mistcrest row** — the
  field that would encode a literal per-week earn cap is unset. Tier-3 guides
  report the familiar **100 per tier per week, cumulative**, with excess
  downgrading to the tier below; that framing is **editorial and not Tier-1
  confirmed**. So: a cap of some form exists and ritual-site crest farming will
  hit it, but **do not plan a week around the weekly reading**.
  `../endgame/dawncrests.md` owns this claim and the live world-state value can be
  changed by hotfix at any time — read the real cap off the currency tooltip in
  week 1 of S2. @verify-ingame
  *(DB2 detail, in case a later read looks contradictory: the cap sits on currency
  rows **3442–3446**; the parallel rows **3437–3441** are uncapped. Both sets are
  named for the five Mistcrests.)*
- Coffer key shards also drop — their amounts were retuned across many sources in
  12.1 and Blizzard calls that retune **a work in progress**, so treat any shard
  number as volatile.
- **Sequential unlock**: each tier must be completed to open the next —
  no skipping straight to T5/T6 on fresh characters.
- **Recommended item levels (12.1, Tier 1):** **T4 259** (was 257) ·
  **T5 268** (was 264) · **T6 275** (was 274). **Tiers 1–3 are untouched** —
  same Season 1 recommended ilvls *and* same tuning.
- **T5 requires ≥4 active challenges.** Challenges first appear at T3.
- **T6 requires all 6 standard challenges selected** (the achievement-only
  "all 8 active" run is harder still).
- **Death penalty**: first 2 deaths free, then **−5% spoils each, max
  −50%** — deaths cut rewards, not completion.
- Challenge stacking: ~+75% spoils possible at T5 (Embers + Malevolent
  Boons + two 15% modifiers).
- Scoring favors **objectives, mini-bosses and bosses; unmarked trash
  gives ~nothing** — skip trash.
- Benchmark: ~ilvl 256 character cleared tier 5 in **10–15 min** — a
  **Season 1** measurement against the old T5 (rec. 264). T5 is now rec. **268**
  and re-tuned, so treat this as a shape, not a number. @verify-ingame

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

## Rewards (12.1) — pegged to Season 2 Delve tiers 1–6

**The reward identity of this content changed.** Since 12.1, a tier-N ritual
site (N ≤ 6) pays the **Season 2 Delve tier-N** vault reward and the **crest
tier a Delve at N pays**. The site's own *difficulty* is unchanged for T1–3 and
slightly re-tuned upward for T4–6 (the new recommended ilvls above).

- **Crests: Mistcrests, up to Veteran.** Delve tiers 1–6 do not pay Champion
  crests, so **the Myth-crest farm is gone** — T6 no longer prints Myth
  Dawncrests, and there is currently **no repeatable solo Myth-crest source**.
  Where Myth Mistcrests *do* come from is **Tier-1 and settled**: **Mythic The
  Venomous Abyss** and **Mythic Keystone +9 and up**, named verbatim in the Myth
  Mistcrest currency description (`CurrencyTypes` DB2 @ `12.1.0.69214`, rows
  3441/3446). ⚠ Both open **2026-08-18** — keystones do not drop before then.
  (`../endgame/dawncrests.md` owns the full source map.)
  **Which crest tier a ritual tier pays is likewise Tier-1-derived**: the notes peg
  ritual T-N to Delve T-N, and the Mistcrest descriptions name **"Tier 4 Delves"**
  for Adventurer and **"Delves T5–6"** for Veteran — so **T4 → Adventurer
  Mistcrest · T5–T6 → Veteran Mistcrest**. What is *not* published is the
  per-tier **amount** at the chest. @verify-ingame the amounts.
- **Great Vault (world row):** the row still counts ritual completions
  (2 / 4 / 8 world activities fills the three slots), but the *quality* a
  ritual contributes is now the delve tier-N quality. The S2 delve/world row
  does not reach **Hero 1/6 (305)** until **Tier 8**, which a ritual site
  cannot reach — so **rituals no longer top out the world row; delves do.**
  ⚠ The first S2 vault (claimable 2026-08-18) caps the world row at
  **Champion 3/6** regardless; **Hero 1/6** only from the second vault onward
  (`../endgame/great-vault.md`).
  - The S1 planning line "tier 4–5 ritual sites beat delve T8 for the world
    row (up to ilvl 269)" is **dead** — do not plan from it.
  - The world-row mechanic still bites the other way: the slot pays your
    **Nth-highest** world activity, so a stack of low-tier rituals fills the
    counters while *lowering* what the slot offers. Run rituals for accolades
    and crest volume; run delves for slot quality.
- **Field Accolades: still the reason to be here.** The currency is uncapped
  (Tier-1 DB2 re-read above) and the sites remain by far the fastest source
  (`#field-accolades--gear-vendors-silvermoon` below). ⚠ The **~100+ per run at
  T5** figure is a **Season 1 measurement against the old T5** (rec. 264) — the
  12.1 notes say nothing about accolade *rates*, and T5 was re-tuned to rec. 268,
  so the per-run number is an inference from Tier-1 silence, not a 12.1
  measurement. Treat it as the right order of magnitude, not a payout.
  @verify-ingame
- Coffer key shards, the ritual-site renown track, and the in-site
  collectibles below all still drop.
- **End-of-run gear**: follows the same delve-tier realignment; the old
  "T6 drops ilvl ~270+" figure was a Season 1 number and no longer applies.
  Exact S2 end-of-run ilvls per ritual tier are **unpublished**. @verify-ingame

### Weekly quests & the removed bonus roll (12.1)

- **⚠ The Tier 6 Advanced Ritual Studies quests no longer offer a Nebulous
  Voidcore bonus roll** (Tier 1, 12.1). They **remain completable for the
  achievement**. The old "Week 3 and Week 6 of the cadence grant an extra
  Bonus Roll" rule is **removed** — do not schedule a week around it.
  Voidcores are a **Great Vault** reward in S2 instead
  (`../endgame/great-vault.md`).
- The **weekly quests** themselves remain: clear a Tier 6 site with specific
  challenges applied.
- **Quest pickup (hotfix 2026-06-22, still current):** Lady Darkglen's Tier 6
  quest can be picked up at the **Silvermoon hub** as well as outside the
  active Ritual Site — no need to travel to the site just to grab it.

### New achievements (12.0.7)

- **Advanced Ritual Site Studies** — complete all 6 advanced challenges
  for Lady Darkglen.
- **Pinnacle Ritual Work** — complete **each** Ritual Site at Tier 6 with
  **all 8 challenges active** (Daggerspine Point, Broken Throne, and the new
  Blinding Bloom). Rewards the title **"Ritual Breaker."**

## Field Accolades & gear vendors (Silvermoon)

- **⚠ The Season 1 gear caches were REMOVED in 12.1.** The old Maren Silverwing
  line ("Champion cache 100 · Heroic cache 750 accolades, ~ilvl 259") is dead —
  do not send anyone to buy it. The Void-Touched Cache stock is now
  **Season 2** (Tier 1, 12.1 notes):

  **Vendor: still Maren Silverwing** (above the Bazaar, Silvermoon), the same NPC
  who carried the S1 caches. The 12.1 notes head the change "VOID-TOUCHED CACHES"
  and name no NPC, but the **Field Accolade currency description itself does** —
  *"Maren Silverwing will exchange these for Void-Touched Caches in Silvermoon
  City"* (`CurrencyTypes` DB2 @ `12.1.0.69214`, ID 3405). That is Tier-1 game data
  on the current build, so this is **settled, not pending**. Agrees with
  `void-incursions.md`.

  | Cache | Cost | Slot | Binding | Drops at |
  |---|---|---|---|---|
  | **S2 Adventurer** | **200** Field Accolades | slot-specific | **Warbound until equipped** | ilvl **266** (Adventurer 1/6) |
  | **S2 Veteran** | **500** Field Accolades | **random** | Bind-on-Pickup | **279** (Veteran 1/6) |
  | **S2 Veteran** | **750** Field Accolades | slot-specific | Bind-on-Pickup | **279** (Veteran 1/6) |

  *(Slot, binding and ilvl detail per `void-incursions.md`, sourced to
  warcraft.wiki.gg's cache item pages. The Tier-1 notes state only the three
  costs, the two tracks, and Warbound-vs-BoP — they are **silent on the 200
  cache's slot**, so the slot-specific reading is wiki-derived, not Tier-1.)*

  The Warbound Adventurer cache is the notable one — it is the accolade lever
  that can be **mailed to an alt**; ⚠ **both Veteran caches are BoP**, so 500/750
  gears only the character that farmed the accolades. Slot-specific is available
  at both **200** (Adventurer) and **750** (Veteran) — so a stubborn empty slot
  has a cheap Adventurer answer before the 750 one. Value decays the same way as
  before: pivot to targeted sources (vault, dungeon-specific drops, spark crafts)
  once your slots outgrow the Veteran track.
- Vendors also stock cosmetics (décor, mounts, pets, transmog).
- Other sources: Void Strikes (8 each) and Void Incursions (30 each) in
  Eversong Woods / Zul'Aman — much slower than ritual sites and Void
  Strikes were bugged as of late April 2026. Dark Particles convert at
  the vendor at **100 particles → 10 accolades** (tier 4, boostmatch.gg
  farm guide — corroborate in-game).
- **12.0.7 (live 2026-06-16) added a second real source**: the
  Naigtal/Val worlds (reached by portal from Voidstorm, rotating weekly)
  pay accolades from WQs/rares/objectives, increased in Heroic World Tier.
  Still true in 12.1, but their *gear* rewards were re-tiered to Season 2 —
  see `../endgame/world-events.md` (and note the World Boss drops there are
  **frozen at Season 1 and no longer upgradeable**).
- **Not warbound**: accolades and dark particles can't be transferred;
  each character farms its own.

## Ritual-site renown track (account-wide)

Separate renown track; unlocks persist for alts:

- **Rank 4**: rare mobs spawn (kill for extra spoils → faster accolades)
- **Rank 5**: shrines of power, regeneration-orb bonuses, larger treasures

## TODO

- [ ] **The 12.1 per-tier reward table.** Blizzard published only "matches
      Season 2 Delve tiers 1–6". The crest *tier* per ritual tier is settled off
      DB2 (above); what is missing is the **amount** per run, the end-of-run gear
      ilvl/track, and the vault ilvl each tier offers. Read the obelisk + chest at
      T4/T5/T6. This is the single biggest hole in the file. @verify-ingame
- [ ] Whether the **pre-season week additionally throttles ritual rewards**
      (Delves are explicitly capped at Adventurer 3/6 + Veteran crests; the
      Tier-1 post is silent on Ritual Sites). Re-check on/after 2026-08-18.
      @verify-ingame
- [ ] **Do Mistcrests have an S2 *weekly* accumulation cap?** Partly answered:
      cap machinery is back — DB2 @ 12.1.0.69214 ships **MaxQty 100** on the S2
      crest rows behind world states 30933/30934, so S1's "caps removed" hotfix
      does **not** carry forward. But `MaxEarnablePerWeek` is **0**, so game data
      supports a *holding* cap only; the "100 per tier per week" reading is Tier-3.
      Owned by `../endgame/dawncrests.md`: read the **live** cap text off a
      currency tooltip in S2 week 1 (does it say "this week" or "maximum"?),
      since a world state is hotfixable. @verify-ingame
- [x] **Which vendor stocks the S2 Void-Touched Caches: Maren Silverwing** —
      named outright in the Field Accolade currency description (DB2 @
      12.1.0.69214, ID 3405). Warbound flag on the 200 Adventurer cache is Tier-1
      from the notes ("Season 2 Adventurer **Warbound** caches").
- [ ] Whether the **200 Adventurer cache is slot-specific**. `void-incursions.md`
      says yes (warcraft.wiki.gg); the Tier-1 notes name a slot only for the
      500 (random) and 750 (specific). Confirm at the vendor. @verify-ingame
- [x] Full challenge list + multipliers (2026-06-03, Overgear — tier 4;
      verify %s in-game at the obelisk)
- [ ] Vendor inventory (which slots purchasable; weapon/trinket available?)
- [x] Dark particles → accolades at vendor, 100:10 (tier 4, 2026-06-03 —
      still corroborate the ratio in-game)

## Changelog

2026-08-17 — ritual sites are instanced solo content; an earlier note called them open-world.

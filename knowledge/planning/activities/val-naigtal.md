---
id: val-naigtal
name: Val / Naigtal zone content (WQs, rares, events)
goal: [gearing, collectibles]
venue: world
group: flex
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
breakpoint: { type: vault, track: world, thresholds: [1, 4, 8] }
reward: { type: [power, currency, collectible], detail: "Field Accolades → Hero-track slot gear (Maren Silverwing, ~ilvl 259); Relic Coffer Key shards → coffers; direct WQ/rare gear; fills the World Vault row" }
reward_ilvl_max: 276   # Hero-track ceiling (Field Accolade slot gear starts ~259); vault row keeps value via breakpoint
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources: ["yt:kUP8oqI7Ekc", "https://www.wowhead.com/news/target-specific-gear-slots-with-hero-track-gear-in-patch-12-0-7-381690", "https://www.method.gg/guides/new-and-updated-field-accolade-vendors-in-wow-midnight-patch-12-0-7", "https://www.icy-veins.com/wow/news/two-new-world-bosses-and-locations-12-0-7s-val-and-naigtal-rewards-quests-and-more/", "https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1", "knowledge/endgame/world-events.md"]
confidence: high
---
The ongoing content of the two 12.0.7 worlds (**Val**, **Naigtal**) reached via the Voidstorm
portal — only one is up per week (portal rotates every few days). **World quests, rares, and
events** give **direct gear** plus two instrumental currencies: **Field Accolades** and
**Relic Coffer Key shards**. This is a **premier catch-up gearing loop**, arguably the best
**Hero-track** source outside M+ / raid:

- **Field Accolades → slot-targeted Hero-track gear (~ilvl 259)** at **Maren Silverwing**
  (top of the Bazaar, Silvermoon City) — 12.0.7 updated her to sell *specific slots* (buy the
  belt/boots you're missing instead of praying for a drop). Field Accolades also buy cosmetics
  / mounts at the new Val/Naigtal vendors (the `collectibles` tag) — a correction to the
  12.0.5 "accolades = transmog only" framing.
- **Relic Coffer Key shards** assemble into keys that open **coffers** for more gear.
- On **Heroic World Tier** rares now drop **Heroic Warbound-until-equipped** pieces (post-6/26
  hotfix; was Champion) and, since the 6/26 reward buff, **2× crests** plus more frequent spawns;
  **Dark Particles** also drop in Val/Naigtal now (stack to 1000), and Maren's Void-Touched
  Heroic caches are now **Warbound**.
- The active **world boss** (weekly capstone, see `showdown-weekly`) drops a **Warbound Heroic
  1/6** item on Normal World Tier / **Heroic 4/6** on Heroic, plus a per-character **Soulbound
  Champion 4/6** (Normal) / **Heroic 1/6** (Heroic) piece.

**Vault note:** like delves and prey, this content **fills the *World* row of the Great
Vault** — the **same column** `delve-bountiful` advances, not a second one. The `breakpoint`
here marks that it advances that column; the ranker-wiring phase must treat the World row as
one shared counter (don't double-count delve + world progress). **Overlap:** the weekly
capstone quest lives in `showdown-weekly`; Field Accolades are also earned from `ritual-sites`
— this row is the *zone farm* that earns the currency and the direct WQ/rare drops.

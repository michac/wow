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
reward_ilvl_max: 279   # Hero-track (Field Accolade slot gear); vault row keeps value via breakpoint
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-06
sources: ["yt:kUP8oqI7Ekc", "https://www.wowhead.com/news/target-specific-gear-slots-with-hero-track-gear-in-patch-12-0-7-381690", "https://www.method.gg/guides/new-and-updated-field-accolade-vendors-in-wow-midnight-patch-12-0-7", "https://www.icy-veins.com/wow/news/two-new-world-bosses-and-locations-12-0-7s-val-and-naigtal-rewards-quests-and-more/", "knowledge/endgame/world-events.md"]
confidence: medium
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
- On **Heroic World Tier** (~ilvl 274+) rares drop Champion (Warbound) pieces and yield more
  shards/gold; the active world boss drops a weekly Hero Warbound piece (see `showdown-weekly`).

**Vault note:** like delves and prey, this content **fills the *World* row of the Great
Vault** — the **same column** `delve-bountiful` advances, not a second one. The `breakpoint`
here marks that it advances that column; the ranker-wiring phase must treat the World row as
one shared counter (don't double-count delve + world progress). **Overlap:** the weekly
capstone quest lives in `showdown-weekly`; Field Accolades are also earned from `ritual-sites`
— this row is the *zone farm* that earns the currency and the direct WQ/rare drops.

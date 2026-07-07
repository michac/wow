---
id: showdown-weekly
name: Val / Naigtal Showdown weekly
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: showdown }
reward: { type: [power, currency, collectible], detail: "Riftstalker's Cache (Field Accolades, Relic Coffer Key shards, mats); heroic-WT world boss = Warbound Heroic 4/6 + per-character Soulbound Heroic 1/6 (6/30 hotfix); showdown-achievement mounts" }
yields:
  currencies: { field_accolade: 100 }   # weekly Riftstalker's Cache (world-events.md)
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # Soulbound Hero piece LANDS at 259 (1/6, dawncrests.md), 276 is the crested ceiling; chance carried for Phase-3 EV, unused in 2a
time_blocks: 1.5
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources: ["yt:kUP8oqI7Ekc", "knowledge/endgame/world-events.md", "https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1"]
confidence: medium
---
The **"Showdown on Val" / "Showdown on Naigtal"** weekly (whichever world the Voidstorm portal
points at this reset — it rotates every few days). WQs, rares, and events across the active
world culminate in the world-boss showdown; the weekly pays a **Riftstalker's Cache** (Field
Accolades, Relic Coffer Key shards, materials, gold).

On **Heroic World Tier** (recommended ~ilvl 274+) the loop upgrades: rares drop Champion
gear, the active world boss drops a **Warbound Heroic 4/6 piece** for the warband **plus** a
per-character **Soulbound Heroic 1/6 piece** each kill (**6/30 hotfix** — superseded the launch
Champion/Hero drop), Void Commander's Emblems feed a longer Myth-track quest, and the **Heroic
Showdowns achievement path unlocks mounts** (hence `collectibles`). **Dedup note:** the boss loot roll overlaps `world-boss`, and the *ongoing
zone farm* (WQs/rares that earn the currency + fill the World Vault row) lives in
`val-naigtal`; this row is specifically the **weekly capstone quest** (Riftstalker's Cache) +
achievement.

**Field Accolades are a real gearing currency in 12.0.7** (not just cosmetics): they buy
**slot-targeted Hero-track gear (~ilvl 259)** from **Maren Silverwing** (Bazaar, Silvermoon),
and cosmetics/decor at Fieldsmith Ventem / Zuronar — see `val-naigtal` for the full spend.

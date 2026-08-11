---
id: housing-weekly
name: Housing weekly (Vaeli)
goal: [collectibles]
venue: housing
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: housing_weekly }
reward: { type: [currency], detail: "Community Coupons (housing decor currency) + Endeavor progress / House XP; flavor" }
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/news/24296054/
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281
  - https://www.wowhead.com/quest=95413/community-engagement
  - knowledge/systems/housing.md
  - knowledge/planning/candidates.json
confidence: medium
---
Vaeli's rotating housing weekly — Community Coupons (the housing decor currency) and
Endeavor progress, pure flavor (low R). She stands beside the tent/mailbox in the
neighborhood; the weekly asks you to take part in whatever the neighborhood is doing that
reset (e.g. **"Community Engagement"**, quest **95413** — buy an item from an endeavor
trader). **Gate is a likely-gap:** the quest-of-the-week rotates IDs, so `housing_weekly`
may not resolve; low value means it's fine to leave as best-effort until the addon tracks
it. @verify-ingame confirm which quest ID Vaeli actually offers on a given reset, and
whether one stable ID backs the gate.

## 12.1 (2026-08-11)

- **Four new neighborhood Endeavors**, so there is more to feed the weekly into:
  Amani trolls **"Knock-off Amani"** (Griftah's travelling traders — their own
  *Griftah's Token of Appreciation* currency) · kobolds **"Candle Culture"**
  (vendor Timicky) · Ohn'ahran centaur **"Every Bakar Has Its Day"** (Roshai
  Lightstep) · tortollan **"Vacation Season"** (Taifa). **Knock-off Amani is the one
  live at patch launch**; after it, the neighborhood picks from the array of Endeavors
  as new visitors arrive.
- **Neighborhoods now show visible results from completed Endeavors**, old and new —
  the sink is cosmetic but now legibly so.
- **Houses can reach level 12** (higher decor limits, large exteriors), and **Artisanal
  Rooms** are purchasable from the General Contractor NPCs for **Community Coupons**
  (four new rooms each in orc / human / night elf / blood elf style; cross-faction
  styles come from the neighborhood smugglers). That is a real Coupon sink, which
  nudges this row up slightly for a housing-goal character — still not a gearing row.
- Ranker impact: **none on the seasonal split.** Housing is unaffected by the
  pre-season week; this row is equally available before and after Season 2 opens
  2026-08-18.

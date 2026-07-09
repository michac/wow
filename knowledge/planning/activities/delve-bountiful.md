---
id: delve-bountiful
name: 6 keyed Bountiful delves
goal: [gearing]
venue: delve
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: delve_weekly_cache }
breakpoint: { type: vault, track: world, thresholds: [2, 4, 8] }
reward: { type: [power], detail: "crests + catalyst + keyed Champion-250 coffer; fills the world Vault column (Hero 259 is the Vault slot, not the coffer)" }
yields:
  currencies: { hero_crest: 35, myth_crest: 5 }   # Bountiful T11 weekly chunk (dawncrests.md); Myth needs Journey rank 4, Hero-from-gilded rank 2 — 0 for a rankless fresh alt
  slots:
    - { track: champion, ilvl: 250, chance: 1.0, slots: [all] }   # keyed Bountiful Coffer + end-of-run = Champion 2/6 (250), NOT Hero (corrected 2026-07-09); Hero 259 comes from the Great Vault delve slot (the world-row `breakpoint`), a Delver's Bounty map, or Journey rank 9
time_blocks: 1
enjoyment: 1.4
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-09
sources:
  - knowledge/planning/candidates.json
  - knowledge/endgame/delves/overview.md
  - https://www.icy-veins.com/wow/midnight-delve-rewards-guide
  - https://conquestcapped.com/guides/wow/midnight-delves-rewards/
confidence: high
---
The core solo loop — key 6 Bountiful delves for crests, catalyst charges, and the coffer.
**Track correction (2026-07-09):** the keyed Bountiful Coffer (and end-of-run drop) is
**Champion 250 (2/6)** at every tier T8–11, **not Hero** — Hero 259 from delves comes only
from the **Great Vault delve slot** (the world-row `breakpoint`), a **Delver's Bounty map**
consumed in-run, or **Delver's Journey rank 9** (T11 coffer, RNG). So for a rankless fresh
alt this is a **Champion + crest** engine, not a Hero source. Running them **also fills the
world/delve column of the single Great Vault** (slots at **2/4/8**), so that vault progress
is a `breakpoint` here rather than its own row (merged the old `delve-world-vault`).
**Gate TODO (roadmap):** the weekly cap sits on the Restored Coffer Key economy, not
the shard currency (dump shows shards `weeklyMax=0`); resolve the key signal in-game. @verify-ingame

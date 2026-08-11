---
id: liadrin-spark
name: World-event weekly (Liadrin, spark)
goal: [gearing, professions]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: liadrin_spark }   # ⚠ S2 quest-giver/IDs unconfirmed — see "Unconfirmed" below
reward: { type: [currency, power], detail: "1 crafting spark (S2 = Spark of Tides) → gear crafting" }
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.forums.blizzard.com/en/wow/posts/29833350   # S1 ending / S2 information — "Crafting Sparks will also begin dropping during the pre-season" (Tier 1)
  - https://news.blizzard.com/en-us/article/24295090        # Midnight: Curse of Ula'tek Pre-Season Details (Tier 1)
  - https://www.wowhead.com/ptr/item=274476/spark-of-tides  # Spark of Tides, item 274476 (game data — name/ID resolution)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214 # Mistcrest names/IDs 3437-3441 + upgrade bands (Tier 1 game data — the floor)
  - https://warcraft.wiki.gg/wiki/Midnight_Season_2         # S2 spark costs + crest pairing (Tier 3, corroboration)
  - https://www.icy-veins.com/wow/spark-crafting-guide      # updated 2026-08-11 for S2 launch (Tier 3, corroboration)
  - https://www.wowhead.com/news/pve-weekly-spark-quests-added-on-lady-liadrin-380715   # S1 origin of this row (historical)
  - knowledge/planning/candidates.json
confidence: medium
---
Lady Liadrin's weekly Spark quest (Silvermoon, ~48.9, 64.9): pick **one of four**
PvE objectives — 6 World Quests, 3 Stormarion Assault Waves, 3 Prey Hunts, or 1
Battleground — and turn in for a **full crafting spark**. (In Season 1 the turn-in
also paid an **Apex Cache + gold**; that side reward is a Season-1 detail and is
**not verified for Season 2** — nothing in the 12.1 notes mentions it.) In Midnight,
sparks drop **whole** (no fractured half-spark like The War Within). `goal` spans
`gearing` (the crafted item) and `professions` (the craft).
**Gate:** four-choice weekly from Lady Liadrin (NPC 256203); the specific quest ID
varies by which objective you pick, so read the live log when picked up. A 12.0.7
hotfix restored the offering to four choices.

## Pre-season week (Aug 11–17): sparks are back on — run this now

12.1 went live **2026-08-11**; Season 2 opens **2026-08-18**. Most Season-2 rewards
are gated through that week, but sparks are explicitly **not** one of them:
Blizzard's pre-season post says *"Crafting Sparks will also begin dropping during
the pre-season."* (Tier 1). So this row is **`active` today** — the weekly spark is
one of the few things that banks crafting-side gearing progress during a week when
keystones, Bountiful Delves, the raid and rated PvP are all still offline.

That also makes it a **cheap 30-minute win right now**: it is one of the few
gearing-adjacent weeklies that is actually available before Aug 18.

⚠ Two caveats on how hard to push it:

- **A skipped week is not lost.** In Season 1 the seasonal cap had a **catch-up**
  — if you were below cap, most content randomly awarded sparks — plus **Sparks of
  War** (100 in the rotating War Mode zone → an extra spark). Nothing in the 12.1
  notes removes either, so treat a missed week as recoverable, not gone
  (`../../systems/professions.md`).
- **Blizzard's line does not name the spark.** The Tier-1 sentence is only
  *"Crafting Sparks will also begin dropping during the pre-season"* — it does not
  say whether pre-season drops are the new **Spark of Tides** or still Season 1's
  **Spark of Radiance**. If it is the latter, a spark banked this week buys S1
  crafting, not S2, and the urgency argument above inverts. **Unverified.**

## Season 2 changes the spark itself

- **The Season 2 spark is the `Spark of Tides` (item 274476)**, replacing Season 1's
  **Spark of Radiance** (232875). **Whether leftover Sparks of Radiance convert to
  anything is not published either way** — the 12.1 notes specify a conversion only
  for **Nebulous Voidcores** (→ gold at the end of S1). Don't plan a stockpile around
  either outcome until it's read in game.
- **Still one spark per week per character**, whole (not fractured).
- **2–4 sparks per crafted item** — as in S1, 2 for armor / a one-hander and 4 for a
  two-hander (Tier 3; the S1 split is assumed to carry, not re-verified).
- **The crests you pair with a spark are now Mistcrests.** All five Season-2 tiers
  are **Tier-1 confirmed from game data** (`CurrencyTypes` DB2 @ `12.1.0.69214`,
  currency IDs **3437–3441**): Adventurer **269–282** · Veteran **282–295** ·
  Champion **295–308** · Hero **308–321** · Myth **321–334** — the whole ladder
  shifted **+45** from the S1 Dawncrests (224–237 / 237–250 / 250–263 / 263–276 /
  276–289). These bands are the floor; no guide's ilvl chart overrides them.
  See `../../_meta/moving-values.md` and `../../endgame/dawncrests.md` (that file
  covers crests generally and may be renamed for S2 — if this link 404s, look for
  the crests file under `../../endgame/`).
- ⚠ **How many crests a spark craft takes in S2 is NOT known.** Tier-3/4 guides
  describe the S1 shape carried forward with the crest renamed — Hero/Myth-range
  crafts wanting **Spark of Tides + the matching Mistcrest** as an optional
  reagent — but **the counts are unconfirmed**. For reference, the **Season 1**
  numbers were **80** Hero or Myth Dawncrests (**160** for a two-hander). Do not
  quote those as S2 values, and **do not quote a crafted ilvl bracket for S2 until
  it's measured** (`../../systems/professions.md`).

## ⚠ Unconfirmed: does the Liadrin weekly itself carry into Season 2?

**The 12.1 notes and the pre-season post never name a spark quest-giver.** They say
only that Crafting Sparks begin dropping. Nothing published confirms that the
four-choice Lady Liadrin weekly is still the delivery vehicle in Season 2, or that
its objective list is unchanged. **Do not read the lead paragraph above as verified
for 12.1** — it is the Season 1 mechanic, carried forward unverified, and the
`gate.quest: liadrin_spark` mapping is unresolved for S2 on top of that.

All three PvE objectives are worth a second look even if the quest is intact:

- **3 Prey Hunts** — Prey runs **Normal and Hard modes only** this week (Nightmare is
  offline until Aug 18, `prey-weekly.md`). Normal/Hard hunts are presumably still
  hunts for this objective's purposes, but that is an assumption.
- **1 Battleground** — unrated PvP **is** live during pre-season, so this should be the
  fastest completion of the four right now.
- **3 Stormarion Assault Waves** — the 12.1 notes carry **no Stormarion-specific
  change**; the objective is assumed intact.

**No objective here is combat-unchanged, though.** 12.1 shipped four global class
changes that land in every instance and every open-world pull: **player health and
creature damage both +25% at max level** (health consumables rescaled, some DPS/Tank
healing and absorb spells retuned), **major DPS cooldowns lowered with steady-state
damage raised** on several specs, interrupts now showing a **"missed" visual + sound**
when the target wasn't casting, and **diminishing-return categories resetting after
20s (was 16)**. So Prey hunts, assault waves and the BG will feel different even
though the quest didn't change — budget the time block accordingly.

@verify-ingame: log in and check Lady Liadrin (Silvermoon ~48.9, 64.9) for the weekly
spark offering — confirm (a) the quest still exists in Season 2, (b) it rewards a
**Spark of Tides** (and whether pre-season drops are Tides or still Radiance),
(c) the four objectives are still the same four, (d) the live quest ID for whichever
you pick, so `gate.quest` can be wired for real, and (e) whether the Apex Cache +
gold side reward is still attached. Until that is answered this file's `confidence`
stays `medium`.

Season-wide spark/crafting detail: `../../systems/professions.md`.

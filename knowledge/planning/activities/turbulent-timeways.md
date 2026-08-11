---
id: turbulent-timeways
name: Turbulent Timeways (Timewalking event)
goal: [gearing, collectibles, leveling]
venue: dungeon
group: flex
cadence: event
time: time-boxed
scope: character
status: invalidated
ended: 2026-08-11
gate: { type: event_active, match: "Timewalking" }
reward: { type: [collectible, power], detail: "HISTORICAL (event over). Was: Spawn of Vyranoth mount (Mastery in 4 of 6 event weeks); weekly Heroic Cache of Quel'Thalas (ilvl 259–276)" }
yields:
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # HISTORICAL — Heroic Cache LANDED at 259 (S1 1/6); not obtainable post-event
time_blocks: 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - "yt:rliFXbEHghU"
  - "yt:kUP8oqI7Ekc"
  - knowledge/endgame/world-events.md
  - knowledge/_meta/moving-values.md
  - https://www.wowhead.com/news/spawn-of-vyranoth-mount-requires-one-less-week-of-timewalking-during-turbulent-381738
  - https://www.wowhead.com/achievement=61463/master-of-the-turbulent-timeways-v
  - https://www.wowhead.com/quest=93497/a-soaring-path-through-time
  - https://www.icy-veins.com/wow/turbulent-timeways-guide
confidence: high
---
⛔ **ENDED 2026-08-11 — historical, not a rankable activity.** Turbulent Timeways V ran
**2026-06-30 → 2026-08-11** and closed with the 12.1 "Curse of Ula'tek" patch day.
`status: invalidated` is what keeps `wowkb.gen_candidates` from emitting it, so the ranker
no longer sees it; the gate below is kept only so this file is ready to re-arm if a
**Turbulent Timeways VI** is announced (flip `status:` back to `active`, re-date the run,
re-check the achievement ID — the meta is versioned per run). Everything past this banner
is a record of the run that finished, in past tense.

The recurring Timewalking event — **Turbulent Timeways V**, six weeks, **Dragonflight**-
bookended. While live, `time: time-boxed` drove U up (1.5, recurring) so the fun survived
efficiency-first, and the collectible R-floor kept a rare mount in the tail. ⚠ Do **not**
rely on the gate to retire it: `event_active` / "Timewalking" matches *any* Timewalking
holiday in the calendar dump, and an ordinary Timewalking week is not this event —
`status: invalidated` is the thing doing the work.

**Mechanics measured during the run (`yt:rliFXbEHghU`, `yt:kUP8oqI7Ekc`):**
- First TW dungeon of the week → **Knowledge of Timeways** (+5% XP). Four TW dungeons →
  upgraded to **Mastery of Timeways** (+30% XP to kills *and quest turn-ins*, 3h, **persisted
  through death**); re-queuing a dungeon refreshed the timer.
- The XP buff **stacked with Darkmoon Faire** and other XP buffs — banking delve/WQ quest
  turn-ins under Mastery was a huge leveling burst (the alt-leveling star case).
- **5 TW dungeons/week** completed the weekly quest → a **Heroic Cache of Quel'Thalas**
  (one **Season 1** Heroic-track piece, ilvl **259–276**). The weekly-quest ID **rotated by the
  active week's expansion** — Dragonflight weeks (which bookended this run) were **"A Soaring
  Path Through Time," quest 93497** (cache = item **250116**). ⚠ Those are S1 numbers on the
  retired Dawncrest track; 12.1 moved endgame gearing to **Season 2 / Mistcrests**
  (`endgame/dawncrests.md`), so do not reuse this band as a live reference.
- **Mount:** *Spawn of Vyranoth* (new proto-drake) required earning **Mastery of Timeways in
  4 of the event's 6 weeks** — you could **miss up to two** (the requirement was **reduced from
  5 to 4** near launch, Wowhead #381738, which is the source of the older "4 of 5 / miss at
  most one" phrasing). Progress was **account-wide** and could be spread across alts.
  **Missed it → it is gone with this run**; treat any "buy it later from a Timewalking
  vendor" claim as unverified (only low-tier guide sites say so, and they contradict each
  other) until it's confirmed in game or on a Tier-1 source.
- **Tracking (for the addon):** the mount meta was **achievement 61463** ("Master of the
  Turbulent Timeways V") — account-wide, a single week-counter criterion, so
  `GetAchievementCriteriaInfo(61463, 1)` read "weeks earned / needed" and survived logout;
  the transient **Mastery of Timeways** aura told you "is this week banked yet." That answered
  the "can PlannerState surface mount progress?" — **yes**, off the achievement, not the buff.
  Keep this: it's the reusable recipe for the *next* run's meta, whose achievement ID will
  differ (each Turbulent Timeways numbers its own).

**Why it ranked the way it did (kept for the re-arm).** At **max level** the only value was the
**mount** (collectible) and the **weekly Heroic Cache** — the +30% XP was worthless. On a
**leveler** (Hallick) `goal:leveling` + +30% XP made it a top pick *while live* — the
"1 hour → level the alt" flip. ⚠ The scorer does **not** suppress the `leveling` reward for a
capped char (no level-conditional R until Phase 4's roster/level model), so on a 90 the
`leveling` tag still nudged `reward_base` — a known over-count pending Phase 4, and one that
now only matters if this file is re-armed for a future run.

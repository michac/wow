---
id: turbulent-timeways
name: Turbulent Timeways (Timewalking event)
goal: [gearing, collectibles, leveling]
venue: dungeon
group: flex
cadence: event
time: time-boxed
scope: character
status: active
gate: { type: event_active, match: "Timewalking" }
reward: { type: [collectible, power], detail: "Spawn of Vyranoth mount (Mastery in 4 of 6 event weeks); weekly Heroic Cache of Quel'Thalas (ilvl 259–276). At cap the mount + weekly cache are the only value — the +30% XP is leveler-only" }
yields:
  slots:
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }   # Heroic Cache LANDS at 259 (1/6, dawncrests.md), 276 is the crested ceiling; chance carried for Phase-3 EV, unused in 2a
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-09
sources:
  - "yt:rliFXbEHghU"
  - "yt:kUP8oqI7Ekc"
  - knowledge/endgame/world-events.md
  - https://www.wowhead.com/news/spawn-of-vyranoth-mount-requires-one-less-week-of-timewalking-during-turbulent-381738
  - https://www.wowhead.com/achievement=61463/master-of-the-turbulent-timeways-v
  - https://www.wowhead.com/quest=93497/a-soaring-path-through-time
confidence: medium
---
The recurring Timewalking event — **Turbulent Timeways V**, live **~2026-06-30 → 08-11**
(six weeks; this run is **Dragonflight**-bookended). `time: time-boxed` drives U up (1.5,
recurring) so the fun survives efficiency-first; the collectible R-floor keeps a rare mount
in the tail. Gate keeps it only when a Timewalking holiday is active in the calendar dump.

**Mechanics learned this pass (`yt:rliFXbEHghU`, `yt:kUP8oqI7Ekc`):**
- First TW dungeon of the week → **Knowledge of Timeways** (+5% XP). Four TW dungeons →
  upgrades to **Mastery of Timeways** (+30% XP to kills *and quest turn-ins*, 3h, **persists
  through death**); re-queue a dungeon to refresh the timer.
- The XP buff **stacks with Darkmoon Faire** and other XP buffs — bank delve/WQ quest
  turn-ins under Mastery for a huge leveling burst (the alt-leveling star case).
- **5 TW dungeons/week** completes the weekly quest → a **Heroic Cache of Quel'Thalas**
  (one Heroic-track piece, ilvl **259–276**). The weekly-quest ID **rotates by the active
  week's expansion** — Dragonflight weeks (which bookend this run) are **"A Soaring Path
  Through Time," quest 93497** (cache = item **250116**).
- **Mount:** *Spawn of Vyranoth* (new proto-drake) requires earning **Mastery of Timeways in
  4 of the event's 6 weeks** — you may **miss up to two** (the requirement was **reduced from
  5 to 4** near launch, Wowhead #381738, which is the source of the older "4 of 5 / miss at
  most one" phrasing). Progress is **account-wide** and can be spread across alts.
- **Tracking (for the addon):** the mount meta is **achievement 61463** ("Master of the
  Turbulent Timeways V") — account-wide, a single week-counter criterion, so
  `GetAchievementCriteriaInfo(61463, 1)` reads "weeks earned / needed" and survives logout;
  the transient **Mastery of Timeways** aura tells you "is this week banked yet." That answers
  the "can PlannerState surface mount progress?" — **yes**, off the achievement, not the buff.

**Value split by character level.** At **max level** the only value is the **mount** (collectible)
and the **weekly Heroic Cache** (one Hero piece 259–276) — the +30% XP is worthless. On a
**leveler** (Hallick) `goal:leveling` + +30% XP makes it a top pick *only while live* — the
"1 hour → level the alt" flip. ⚠ The scorer does **not** yet suppress the `leveling` reward
for a capped char (no level-conditional R until Phase 4's roster/level model) — so on a 90 the
`leveling` tag still nudges `reward_base`; treat that as a known over-count pending Phase 4.

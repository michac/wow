---
id: omnium-folio
name: Omnium Folio weekly (Seeking Knowledge)
goal: [gearing, story]
venue: quest
group: solo
cadence: weekly
time: standing
scope: account            # 12.1: row unlocks AND the intro questline are both account-wide — see "Alt cost" below
status: invalidated       # ⚠ NOT "gone" — the Tier-1 five-week series ran out the reset week of 2026-07-14 and nothing confirms a Seeking Knowledge quest is offered on 2026-08-11. Not rankable until someone looks; RE-ACTIVATE on an in-game sighting.
gate: { type: weekly_quest, quest: omnium_seeking_knowledge }
reward: { type: [power], detail: "empower a folio rune — the Midnight runic-power track (added 12.0.7, runes persist through Midnight). ⚠ availability on 2026-08-11 unverified; see prose" }
time_blocks: 1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/news/24277442/   # Omnium Folio deep-dive — the system + weekly cadence (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281        # 12.1 content update notes — QUESTS: intro questline account-skippable (Tier 1)
  - https://us.forums.blizzard.com/t/world-of-warcraft-midnight-hotfixes-june-30/2296045/364  # 2026-06-25 hotfix — Seeking Knowledge prerequisites account-wide from Week 2; also names "Seeking Knowledge Week 4 of 5" (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29759681   # 2026-07-14 hotfix — Rommath's Magister's Terrace portal beside the Missive (Tier 1)
  - https://warcraft.wiki.gg/wiki/Seeking_Knowledge_Week_1_of_5:_The_Omnium_Folio  # quest 96410, "Patch 12.0.7 (2026-06-16): Added" — corroborates the Week-1-of-5 start (Tier 3)
  - knowledge/systems/omnium-folio.md                      # full mechanics: 5 rows, account-wide row unlocks, rune swapping
confidence: medium
---
The **Omnium Folio** is the runic-power progression track added in 12.0.7 and still present
in **12.1** — the runes are "available to players throughout the rest of the Midnight
expansion" (Tier-1 12.0.7 notes), so Season 2 does not reset them. You join **Magister
Umbric** and **Grand Magister Rommath** to restore the **Sunstrider Omnium**, starting from
the **Magister's Missive** in **Silvermoon City**; since the **2026-07-14 hotfix** Rommath
parks a **Magister's Terrace portal right next to the Missive**, so the weekly no longer
costs a run across the city. Full mechanics — rows, rune swapping, currency — live in
`knowledge/systems/omnium-folio.md`; this file is only the planner row.

**⚠ Not rankable today — the schedule ran out.** This is a **fixed five-week** series, one
row per weekly reset. That count is Blizzard's own, not an inherited estimate: the Tier-1
hotfix archive names the quest *"Seeking Knowledge Week 4 of 5: Magical Primessence"*
(`_meta/patch-notes/12.0.7.md`). 12.0.7 went live **2026-06-16**, which puts Week 5 in the
reset week of **2026-07-14** — four weeks before this sweep. **No source at any tier states
whether a Seeking Knowledge quest is still offered on 2026-08-11, or whether a character
behind the schedule restarts at Week 1.** So the row carries `status: invalidated` to keep
`wowkb.plan` from proposing work that may not exist (`changelog-12.1.md` → planning/: an
activity that is not available today must not be rankable today). Re-activate it on a
sighting, not on an assumption.
@verify-ingame Is a Seeking Knowledge weekly still offered after the five-week series ran out the reset week of 2026-07-14 — and does a character that never started get Week 1 or the current week?

**Alt cost is near-zero (12.1) — hence `scope: account`.** Two changes stack:

- **2026-06-25 hotfix** — from **Week 2**, the Seeking Knowledge weekly's quest
  *prerequisites* are account-wide, so an alt does not grind back up through the earlier
  weeks to reach the current week's quest.
- **12.1** — the **Sunstrider Omnium introduction questline can be skipped** on any other
  character once **one** character on the account has completed it. That was the last real
  per-alt tax.

Row unlocks were already account-wide (systems file), so nothing about this activity is
per-character any more except slotting the runes — which is not the work the ranker counts.
The `scope: character` this file used to carry was justified solely by the intro questline
and is retired; that settles the DECIDE item filed in `knowledge/_meta/kb-inbox.md`.

⚠ It is **not** the only Midnight system handing out player power — 12.1 shipped the
**Altar of Corrosion**, a zone-scoped custom talent tree on the Coiled Isle
(`knowledge/systems/coiled-isle.md`), fed by **Corrosive Coins**, with **Spirit of
Corrosion I/II** as discrete Zul'jarra renown-8/14 grants rather than feedstock. Any older
phrasing calling the Folio "the one Midnight addition tied to new player power" is dead as
of 12.1.

`gate` is best-effort on the weekly step ID — read the live log if it doesn't resolve.

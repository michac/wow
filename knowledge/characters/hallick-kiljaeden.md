---
title: Hallick – Kil'jaeden (US) — druid alt snapshot
patch: 12.0.5
fetched: 2026-06-08
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/hallick?namespace=profile-us
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/hallick/specializations?namespace=profile-us
confidence: high
---

# Hallick – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). Re-fetch
> before answering gear/progress questions.

**Alt of the user's main (Encomplete)** — same guild (The Soggy Bottom
Boys), achievement points match account-wide (7,100 vs 7,125).

## Identity

- Night Elf **Druid** (male), active spec **Feral**
- Level **80** (TWW cap — has not started Midnight; cap is 90)
- Alliance, Kil'jaeden · Guild: The Soggy Bottom Boys
- Achievement points 7,100

## State

- Equipped ilvl **102** — pre-Midnight leveling gear
- Needs the 80→90 Midnight leveling path before any endgame loop
  (weekly checklist, delves, crests) applies

## Talent audit (2026-06-08)

- **Hero tree: Druid of the Claw — now SELECTED** (was unspent at the
  2026-06-03 fetch). Confirmed live: Ravage, Dreadful Wound, Bestial
  Strength, Tear Down the Mighty, Twin Claw, Claw Rampage, etc.
- Active-loadout code (Blizzard API):
  `CcGA8cL7tpvige+kkmGM9zUPWDAAAAAAMYmxMzMzstN2mZbmZm5BmZAAAAYLYYYMzomxsMmZmxYGAAAAAAYgBAAAQGz2YmBEYBMzAswgBAAwMbA`
- Key spec picks: Tiger's Fury, Predator, Sabertooth, Primal Wrath,
  Berserk (+Heart of the Lion), Convoke the Spirits, Apex Predator's
  Craving, Pouncing Strikes, Sudden Ambush, Omen of Clarity + Moment of
  Clarity, Wild Slashes, Rampant Ferocity. **Has Berserk, NOT
  Incarnation.**
- ⚠ **Feral Frenzy discrepancy:** API active loadout lists Feral Frenzy,
  but user reported in-game they do NOT have it (2026-06-07). Profile API
  refreshes only on logout, so user's client view is newer — rotation page
  treats Feral Frenzy as ABSENT pending a post-logout re-fetch to confirm.
- Leveling rotation page: `../classes/druid/feral/leveling-rotation.html`
  (rebuilt 2026-06-08 from live loadout; `raw/blizzard/hallick-specializations.json`)
- Icy Veins 12.0.5 "Level 80 Starting Talents" import string (alt build,
  not his current loadout):
  `CcGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMYmxMzMzstN2mZbmZm5BmZAAAAYLYYYMzomxsMmZmxYGAAAAAAYgBAAAQGz2YmBAsAmZAWYwAAAYmNA`

## TODO

- [ ] Re-fetch after next logout to resolve the Feral Frenzy discrepancy
- [ ] Leveling route 80→90 (Midnight zones; check Icy Veins leveling guide)
- [x] Feral leveling rotation page created 2026-06-03, rebuilt 2026-06-08;
      full max-level build/rotation docs still TODO when he hits 90
- [ ] Heirloom / warband XP buffs in 12.0 — worth fetching if user asks

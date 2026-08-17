---
title: Next Patch — none confirmed (12.1 shipped 2026-08-11)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://wago.tools/api/builds  # Tier 1 — retail + PTR build feeds
  - https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json?category_id=171  # Tier 1 blue-post tracker
confidence: high
---

# Next Patch Watch — nothing confirmed

> **12.1 "Curse of Ula'tek" went live 2026-08-11** (build `12.1.0.69214`). It was
> the patch this file used to track; that content now lives in
> `game-version.md`, `changelog-12.1.md` and the topic files.
>
> **There is no next patch on PTR.** As of the 2026-08-11 feed review the `wowt`
> PTR line has converged onto `12.1.0.69214` — the same build as live — which is
> the normal post-launch state, not a signal. No 12.1.5 / 12.2 build, blue post
> or datamining recap exists yet.

## What IS still ahead inside 12.1

These are dated, confirmed unlocks — not a future patch, but the things that
change the live state without a new build:

| Date | What opens |
|---|---|
| **2026-08-18** | **Midnight Season 2**: Venomous Abyss (Normal/Heroic/Mythic + LFR Wing 1), Mythic+ S2 + keystones, rated PvP S2, Bountiful Delves + Coffer Keys + "??" Nemesis, Nightmare Prey + Curse of the Isle, Tidebound Grotto on Normal/Heroic/Mythic, first S2 Great Vault |
| **2026-08-25** | Venomous Abyss LFR Wing 2 + Story Mode; **Voidcore bonus rolls return** to the Great Vault (needs ≥3 panes) |
| **2026-09-01** | Venomous Abyss LFR Wing 3 |
| **2026-09-08** | Venomous Abyss LFR Wing 4 |
| **week 8 of S2** | Orin Straylight begins granting +1 Nebulous Voidcore per week |

⚠ **The 2026-08-18 rollover is a real KB event**, not just a date: it flips
`game-version.md` out of pre-season, re-activates the planner activities parked
as `status: invalidated`, and turns a large set of "opens Aug 18" claims into
present tense. Run `/update` (or at minimum a targeted pass over
`endgame/weekly-checklist.md` + `planning/activities/`) that week.

## PTR-era claims that did NOT ship in 12.1

Recorded so a stale pre-release source is recognisable. These appeared in the
pre-launch dev notes / Tier-3 recaps and are **absent from the final
content-update notes**:

- **One-time Profession Knowledge reset** — no mention in the shipped notes.
- **Account-wide user-interface settings** — only **Auto Loot** became account
  wide, plus Auction House filters persisting across sessions.
- **"No gear-upgrade cost scaling"** (Tier-3 report) — unconfirmed; the shipped
  notes say nothing about upgrade costs.

The PTR items that *did* ship, and are now live claims, are in
`changelog-12.1.md` — notably the **+25% player health / creature damage** retune
(reported pre-launch and confirmed in the shipped CLASSES preamble).

## Watch list (where the next signal will land)

- `https://wago.tools/api/builds` → a `wowt` build with a version **above**
  `12.1.0` is the earliest signal of the next patch (Tier 1).
- The `?product=wow` retail feed flipping to a new minor version = **go-live** →
  trigger `/update` Full path.
- Blizzard blue-post tracker + PTR development notes (Tier 1).
- Wowhead PTR hub / Icy Veins dev-note recaps (Tier 3 — corroborate numbers,
  never let them overwrite Tier-1 feed data).

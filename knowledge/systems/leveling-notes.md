---
title: Leveling Notes — Midnight Alt & Endgame Path
patch: 12.0.7
fetched: 2026-07-06
sources:
  - https://www.icy-veins.com/wow/midnight-leveling-guide
  - https://warcraft.wiki.gg/wiki/Midnight_campaign
  - https://warcraft.wiki.gg/wiki/The_War_Within_campaign
  - https://www.wowhead.com/npc=249361/shulka-litya
  - https://www.wowhead.com/quest=92013/wanted-dionaeas-thorntusks
  - "FollowTheArrow addon v0.7.0 (local: Interface/AddOns/FollowTheArrow/Data/Modules/*.lua)"
confidence: high
---

# Leveling Notes (Midnight, Retail)

Practical leveling mechanics for **alts** in Midnight, plus the route gotchas
that are painful to re-derive. Not a step-by-step guide — for that, use the
**Follow the Arrow** addon (see below). See `_meta/quests.md` for *how quest
data works* (level vs required level, gating, how to fetch it reliably).

## The level ladder (cap 90)

| Levels | Content | Notes |
|--------|---------|-------|
| 10–70  | **Chromie Time** (Dragonflight default; TWW/older selectable) | Scales a chosen expansion to your level. |
| **70** | **Chromie Time ends** | Past 70 you leave Chromie Time. Old-expansion quests (e.g. Dragonflight) now award **trivial XP** — this is expected, not a bug. |
| 70–80  | **The War Within** campaign | Most-recently-tuned, linear; the smooth path 70→80. |
| **78** | Midnight intro unlocks | You *can* peel into Midnight at 78 instead of finishing TWW to 80. |
| 80–90  | **Midnight** zones/campaign | Adventure Mode scales all Midnight content to your level. |

> **Symptom → cause:** "Chromie Time stopped giving good XP around 71–77" =
> you aged out of Chromie Time at 70. The fix is to move to War Within / Midnight
> content, not to toggle anything.

## Starting the newer expansions on an alt

- **The War Within (70→80):** *reportedly* auto-offered on entering **Stormwind
  (Jaina)** / **Orgrimmar (Thrall)** — both added in the 2026-01-27 hotfix; alt
  skip is said to be the Dalaran intro → **"I have heard this tale before"** →
  **Dornogal** → Brann → *Adventuring in Khaz Algar*.
  > ⚠ **Unverified / low confidence.** This is from guides, not confirmed in
  > practice — a player on this account **could not find or start the TWW
  > campaign at all** and skipped 70→80 entirely (see next bullet). The
  > auto-offer may not reliably fire. Verify in-game before repeating as fact.
- **70→80 without TWW (what actually worked): Turbulent Timeways / timewalking.**
  During the **Turbulent Timeways** event (2026: Jun 30–Aug 11, Dragonflight
  timewalking dungeons; see `_meta/game-version.md`), timewalking dungeon spam
  gives large XP and is a viable, low-friction path through 70→80 that **does
  not require finding the TWW campaign start**. Verified as the route this
  account used to clear the last few levels to 80.
- **Midnight (80→90):** pick up **"Midnight"** (quest **91281**) from **Lady
  Liadrin** (Dornogal / Stormwind / Orgrimmar), then use the same **"I have heard
  this tale before"** dialogue to skip the **Sunwell intro** and portal to
  Harandar. That skip requires the **full Midnight campaign done on your account**
  (first character); if you can't skip, you're on a character that must do the
  campaign.

## Follow the Arrow (FTA) — route structure

Free leveling addon by Harldan (CurseForge, **v0.7.0** at time of writing).
**Closed-source (no GitHub, no contributions) but ships as plain readable Lua** —
the route data is greppable on disk:

```
Interface/AddOns/FollowTheArrow/Data/Modules/*.lua
```

Three distinct routes (dropdown, top-right of the addon window):

| Route | routeId | For | Behavior |
|-------|---------|-----|----------|
| Midnight **Campaign** | `MIDNIGHT_*` (SunwellIntro…) | **First character** | Full campaign; required once per account to unlock endgame features. |
| Midnight **Alt 80-90** | `MIDNIGHT_ALT` | Alts | **Skips the campaign.** Ports to Harandar early, front-loads **delves + Legends of the Haranir + Voidstorm sidequests**. Module `Alt8090Delves.lua` is first (`moduleOrder = 10`). |
| Midnight **Sojourner** | `MIDNIGHT_SOJOURNER` | Achievement / overflow XP | Per-zone side-questline chains. |

The alt route intentionally has you **port to Harandar → Legends of the Haranir →
Grudge Pit delve**, with no Sojourner campaign. So "I don't remember a Harandar
campaign" on the alt route is correct — you're not doing one.

## Gotcha: Shul'ka Li'tya's "WANTED" board (Harandar)

**Shul'ka Li'tya** (Harandar **51.82, 74.24**, faction *The Hara'ti*) gives 7
repeatable **"WANTED:"** elite-kill dailies (quests 91970/91980/91982/91998/
92010/92012/92013). Rewards are **endgame currency** — *Coffer Key Shards*,
*Voidlight Marl*, *The Hara'ti* rep — not leveling rewards.

FTA's alt route points you here as an **explicitly optional** detour
(`Alt8090Delves.lua`, `kind = "MANUAL"`): *"since this is not always the case, I
can't make it a required part of the guide… entirely optional."* If she has no
quests for you, **that is expected** — do not treat it as broken. Two independent
gates plus a rotation:

1. **Level 88** — the quests' level *and* required level (see `_meta/quests.md`
   for why those are different fields).
2. **Main-campaign progress** — the WANTED board is the repeatable tail of the
   **"Trials of the Shul'ka"** chain, which FTA's own note flags as *"locked
   behind main campaign progress"* (`HarandarSojourner.lua:634`). This gate is
   **independent of level**: a level-**90** player who "completed Harandar" still
   reported no WANTED quest available (Wowhead comment on 92013).
3. **Random daily rotation** — even when unlocked, she offers a random subset
   (sometimes 0–1, sometimes 3) each day.

**Unresolved:** whether the Trials-of-the-Shul'ka unlock is **warband-wide** or
**per-character**. Midnight *does* have account-wide unlocks (e.g. FTA notes
"Blessings of the Loa" unlocks account-wide after one Twilight Crypts Delve,
`Alt8090Zulaman.lua:219`), but the alt route also presupposes a campaign-complete
main, so the observed emptiness could instead be gate #1 (under 88) + the daily
roll. **In-game tiebreaker:** on an 88+ character, fly to Harandar 51.82, 74.24
and check — if bounties show, it's account-unlocked and the alt is simply too low.

**Bottom line:** skip it on a leveling alt; it's optional endgame content.

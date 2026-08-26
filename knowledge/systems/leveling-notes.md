---
title: Leveling Notes — Midnight Alt & Endgame Path
patch: 12.1
fetched: 2026-08-25
reviewed: 2026-08-25
sources:
  - https://worldofwarcraft.com/en-us/news/24293281
  - https://www.icy-veins.com/wow/midnight-leveling-guide
  - https://warcraft.wiki.gg/wiki/Midnight_campaign
  - https://warcraft.wiki.gg/wiki/The_War_Within_campaign
  - https://wago.tools/db2/SpellEffect?build=12.1.0.69214&filter%5BSpellID%5D=exact%3A448924
  - https://www.wowhead.com/spell=448924/wide-eyed-wonder
  - https://www.wowhead.com/spell=436341/ingest-minerals
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

## Exploration XP — rebalanced in 12.1 (2026-08-11)

Map-discovery XP (the chunk you get for uncovering a zone's subzones) was cut in
**12.1 "Curse of Ula'tek"**:

| Change | Value |
|--------|-------|
| Baseline XP from exploring zones | **−60%** |
| Reduced XP for exploring **low-level** zones | **removed** — low zones now pay the same (new, lower) baseline as anything else |
| Earthen **Ingest Minerals** — effectiveness of the Well Fed it grants | **+30%**, as compensation |

**Scope — what Tier 1 actually says.** The official notes file all three bullets
under **Characters → Earthen**, and *Earthen* is the only scope Blizzard states.
The first two bullets are nonetheless worded without a race qualifier ("baseline
experience gained from exploring zones"), and the dev note frames the change as
"revisiting the amount of experience points gained when exploring zones" which
"will **particularly** impact… Earthen" — which reads like a game-wide baseline
cut that lands hardest on Earthen. **We do not assert either reading.** The
Earthen-scoped version is the sourced claim; the game-wide version is
plausible-but-unconfirmed. In-game tiebreaker: level any **non-Earthen** alt and
compare a zone-discovery XP tick against a pre-12.1 value — unchanged means the
cut is Earthen-only. @verify-ingame

**Why Earthen got singled out:** the racial passive **Wide-Eyed Wonder**
(spell 448924) carries exactly one effect — an Apply Aura of *Mod Experience
Gained From Exploration %* with **value 200** (`SpellEffect` DB2 @ build
**12.1.0.69214**: `EffectAura` 637, `EffectBasePointsF` 200; the Wowhead spell
page renders the same "200%"). Read the usual way for a percent-modifier aura,
that is **+200% — i.e. triple** exploration XP, which made "fly the zone and
reveal the map" a disproportionately strong Earthen leveling lever. **The racial
itself was not touched** — the baseline it multiplies was.

> ⚠ *Our arithmetic, not a published number.* Blizzard gave no net figure. If the
> racial is still ×3 and the baseline is now 40% of what it was, an Earthen
> map-sweep pays **3 × 40% = 1.2×** the pre-12.1 *non-Earthen* rate — i.e. down to
> ~40% of what an Earthen used to get. Whether that is still "3× everyone else"
> depends on the unresolved scope above: game-wide cut ⇒ yes, still 3× a
> non-Earthen; Earthen-only cut ⇒ only ~1.2×. Inference from the two sourced
> numbers, not a claim.

**Practical effect on a leveling alt:**

- **Map-sweeping is no longer a leveling strategy on its own** — certainly on an
  Earthen, and for everyone else too if the cut turns out to be game-wide. Level
  off quests / dungeons / campaign and treat discovery XP as incidental.
- **Earthen:** keep **Ingest Minerals** (spell 436341) up — the Well Fed it
  grants is now **30% stronger**, and that buff is the compensation you were
  handed. Re-consume the Khaz Algar gem matching the stat you want.
- **Low-level zones** are relatively *better* than they were (no more low-zone
  penalty on top of the cut), but only relative to the new floor — this does not
  make Chromie-Time map sweeps worth a detour.

## Starting the newer expansions on an alt

- **The War Within (70→80):** *reportedly* auto-offered on entering **Stormwind
  (Jaina)** / **Orgrimmar (Thrall)** — both added in the 2026-01-27 hotfix; alt
  skip is said to be the Dalaran intro → **"I have heard this tale before"** →
  **Dornogal** → Brann → *Adventuring in Khaz Algar*.
  > ⚠ **Unverified / low confidence.** This is from guides, not confirmed in
  > practice — a player on this account **could not find or start the TWW
  > campaign at all** and skipped 70→80 entirely (see next bullet). The
  > auto-offer may not reliably fire. Verify in-game before repeating as fact. @verify-ingame
- **70→80 without TWW — available again in a Timewalking bonus week.**
  Timewalking dungeon spam gives large XP and needs no TWW campaign start; it is
  the route this account used to clear the last few levels to 80. Turbulent
  Timeways V (the six-week special event) ended 2026-08-11, but the **ordinary
  weekly-bonus Timewalking rotation resumed** — **Northrend/Wrath Timewalking is
  live 2026-08-25 → 09-01**, and a **Midnight Dungeon Event** week follows
  Sep 8 → Sep 15. So this route is usable **in a TW week, not every week**;
  check the in-game calendar first. The mechanic: 4 TW dungeons grants
  **Mastery of Timeways, +30% XP** to kills and quest turn-ins for 3h, stacking
  with other XP buffs — bank quest turn-ins and hand them in under it.
  See `endgame/world-events.md` (§ Timewalking).
  > **Live 70→80 options as of 2026-08-25:** a **Timewalking bonus week** when one
  > is up (Wrath TW is up now), the TWW campaign (bullet above), or Khaz Algar
  > questing / dungeons outside Chromie Time. **Turbulent Timeways V** specifically
  > is over — don't take a "Turbulent Timeways is running" line from any other file
  > as current; `endgame/world-events.md` is the one to trust on this event.
- **Midnight (80→90):** pick up **"Midnight"** (quest **91281**) from **Lady
  Liadrin** (Dornogal / Stormwind / Orgrimmar), then use the same **"I have heard
  this tale before"** dialogue to skip the **Sunwell intro** and portal to
  Harandar. That skip requires the **full Midnight campaign done on your account**
  (first character); if you can't skip, you're on a character that must do the
  campaign.
- **One more alt skip, new in 12.1:** the **Omnium Folio introduction questline is
  now account-skippable** once any one character has completed it — a fresh 90 no
  longer re-runs the intro to reach the system. Details: `systems/omnium-folio.md`.

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
*Voidlight Marl*, *The Hara'ti* rep — not leveling rewards. ⚠ **No shard count is
given here on purpose:** 12.1 retuned Coffer Key Shard amounts across multiple
sources and Blizzard calls that retune "ongoing and a work in progress", so any
specific number is volatile — see `endgame/delves/overview.md`.

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

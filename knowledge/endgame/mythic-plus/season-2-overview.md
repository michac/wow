---
title: Midnight Season 2 Mythic+ Overview
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24294369   # "The Shadows Deepen: Midnight Season 2 Begins August 18" (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season details (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Content Update Notes (tier 1)
  - https://wago.tools/db2/CurrencyTypes             # Mistcrest names + ilvl bands, build 12.1.0.69214 (tier 1 game data)
  - https://worldofwarcraft.blizzard.com/en-us/news/24271855  # 12.0.5 notes — Keystone Myth introduced in Season 1 (tier 1)
  - https://www.icy-veins.com/wow/midnight-mythic-season-2-guide  # (tier 3, corroborating)
  - https://warcraft.wiki.gg/wiki/Midnight_Season_2  # (tier 4, corroborating only)
confidence: medium
---

# Mythic+ — Midnight Season 2

Season 2 ships in **two steps**, and almost everything on this page is dated:

| | **Week of 2026-08-11 (live now — pre-season)** | **Week of 2026-08-18 (Season 2 opens)** |
|---|---|---|
| Dungeon pool | The S2 pool is active on **Heroic and Mythic 0 only** | unchanged pool; **Mythic+ difficulties open** |
| Keystones | **none — keys do not drop** | Mythic Keystones begin dropping |
| Mythic 0 lockout | **weekly, this week only** | back to **daily** |
| M0 reward | **Champion 1/6 (292)** | Champion 1/6 (292), daily |
| Rating / titles | no M+ rating is earned | rating ladder live (see below) |

So: **right now there is no Mythic+**, only Heroic and a once-per-week Mythic 0
clear of each of the eight dungeons. Everything below the pool table describes
the **Aug 18** state unless it says otherwise. (Blizzard, "Midnight Season 1
Ending / Season 2 Information", 2026-08-01.)

## Dungeon pool (8)

| Dungeon | Origin | Notes |
|---------|--------|-------|
| Altar of Fangs | Midnight (**new in 12.1**) | 3 bosses, inside the Vaults of Atal'Utek on the Coiled Isle |
| Murder Row | Midnight | first M+ appearance |
| Den of Nalorakk | Midnight | first M+ appearance |
| The Blinding Vale | Midnight | first M+ appearance |
| Voidscar Arena | Midnight | first M+ appearance |
| Ruby Life Pools | Dragonflight | returning — ships with design/QoL updates |
| Kings' Rest | Battle for Azeroth | returning — ships with design/QoL updates |
| Temple of Sethraliss | Battle for Azeroth | returning — ships with design/QoL updates |

**The whole Season 1 pool rotated out.** Magisters' Terrace, Maisara Caverns,
Nexus-Point Xenas, Windrunner Spire, Algeth'ar Academy, Seat of the Triumvirate,
Skyreach and Pit of Saron are **not** in the S2 rotation — their files are
S1-era history now (`season-1-overview.md`). Five of the eight S2 dungeons are
Midnight-native, so this is the season the expansion's own dungeons finally
carry the rotation.

Blizzard called out the three returning dungeons as having received "design and
quality of life updates" but did not enumerate them — treat any pre-12.1 route
guide for Ruby Life Pools / Kings' Rest / Temple of Sethraliss as suspect.

**No dungeon in this pool is "unchanged by 12.1."** Even the five with no
instance-specific notes are reshaped by the patch's four **global** class/combat
changes, which apply to every spec in every instance: **player health and
creature damage both +25% at max level** (health consumables rescaled, and some
DPS/Tank healing and absorb spells retuned to keep their relative impact); **major
DPS cooldowns lowered with steady-state damage raised** on several specs;
**interrupts now show a "missed" visual and sound** when the target was not
casting; and **diminishing-return categories now reset after 20s** (was 16s).
Practically: any absolute HP/damage-taken number, any "this pull one-shots you"
threshold, and any stop-rotation written before 2026-08-11 is stale even for a
dungeon that carried over untouched.

## Practicing as Follower Dungeons

Follower Dungeons (Normal difficulty, AI companions; no affixes/timer) only
cover **Dragonflight / War Within / Midnight** dungeons, so the two BfA
dungeons have no follower version at all.

| S2 M+ Dungeon | Follower Dungeon? |
|---|---|
| Altar of Fangs | ❓ new in 12.1 — not confirmed in the follower pool (**verify in game**) |
| Murder Row | ✅ Midnight follower pool |
| Den of Nalorakk | ✅ |
| The Blinding Vale | ✅ |
| Voidscar Arena | ✅ |
| Ruby Life Pools | ⚠️ DF follower pool only (DF tuning/level, not Midnight) |
| Kings' Rest (BfA) | ❌ no follower version |
| Temple of Sethraliss (BfA) | ❌ |

Useful for learning layout/routes/boss mechanics blind — **not** for M+
affix/tuning practice. (Midnight follower pool carried over from
`season-1-overview.md`, verified 2026-06-13; the S2-specific rows are inference
from that pool plus the dungeons' expansion of origin.)

## Affixes

⚠️ **The S2 affix set is not settled.** The content update notes carry no affix
section, and neither does the archive (`_meta/patch-notes/12.1.md`). The Season 2
blog does contain one affix sentence, but it sits under the **Prey** heading:

> "Season 2 brings about new Affixes, four new targets in Nightmare Mode, and
> some new hunts on the Coiled Isle in Prey."

Read in place that scopes to Prey's Nightmare affixes, not the Mythic+ ladder —
but "Season 2 brings about new Affixes" is loose enough that it may cover both,
and it is the only Tier-1 affix signal for the season. It is a **counter-signal
to "M+ affixes are unchanged"**, not a confirmation of a new M+ set.

Against that, Icy Veins' S2 guide describes the **same ladder as Season 1** —
Lindormi's Guidance at +2 to +4, a
rotating Xal'atath's Bargain (Ascendant / Voidbound / Pulsar / Devour) plus
Fortified or Tyrannical from +5, both Fortified and Tyrannical from +10, and
Xal'atath's Guile from +12. Until that is seen live, `affixes.md` is the file of
record and this claim is **tier-3, unverified for S2**.

## Rewards

### Crests — Season 2 uses **Mistcrests** (Dawncrests are Season 1)

Confirmed against game data (wago `CurrencyTypes`, build 12.1.0.69214), with
the ilvl band each crest upgrades within:

| Crest | Upgrades within |
|---|---|
| Adventurer Mistcrest | 269–282 |
| Veteran Mistcrest | 282–295 |
| Champion Mistcrest | 295–308 |
| Hero Mistcrest | 308–321 |
| Myth Mistcrest | 321–334 |

Season 1 Dawncrests do not carry over as an upgrade currency for S2 gear. See
`../dawncrests.md` for the crest system itself and every source that grants them.

### Gear item levels

**Tier-1 anchor:** Mythic 0 drops **Champion 1/6 (292)** — weekly lockout for
the pre-season week of Aug 11, daily from Aug 18.

Everything above M0 is currently **tier-3 only** (Icy Veins S2 guide) and should
be re-checked against live drops once keys are running: end-of-run rewards from
**Champion 2/6 (295)** at +2 up to **Hero 3/6 (311)** at +10 and above, with the
Great Vault M+ row running **Hero 1/6 (305)** to **Myth 1/6 (318)**. The files of
record are `loot.md` and `../great-vault.md`, not this page.

### Rating ladder

Full detail (how rating is computed, what to chase first) lives in
`rating-and-rewards.md`. The S2 headline rewards:

| Achievement | Rating | Reward |
|---|---|---|
| Keystone Conqueror: Season 2 | **1,500** | title **"the Venomous"** |
| Keystone Master: Season 2 | **2,000** | mount **Breath of Blight** |
| Keystone Hero: Season 2 | 2,500 | criterion toward *Sssensational!* (*Insidious Venomstone* per secondary sources) — **rating + reward unverified** |
| Keystone Legend: Season 2 | **3,000** | mount **Breath of Ruin** |
| Keystone Myth: Season 2 | **not announced** | title **"the Venomous Contender"** (Tier-1) |
| Venomous Champion | **top 1%** | Feat of Strength |
| Venomous Hero | **top 0.1%** | title **"the Venomous Hero"** |

**What is Tier-1 here:** the 1,500 / 2,000 / 3,000 rows, both percentile rows,
**and the existence of Midnight Keystone Myth: Season 2 with the title "the
Venomous Contender"** — all listed in the Season 2 blog. Keystone Myth is **not**
a new rung: it shipped in Season 1 (12.0.5 notes, "New Achievement: Midnight
Keystone Myth: Season One").

**What is not:** the blog gives Keystone Myth **no rating threshold**, so do not
carry Season 1's **3,400** across. The S1 dev note is explicit that the number
"will not remain fixed forever" and may be adjusted in future seasons; the
*Timelost Saddle* reward is likewise an S1 detail with no S2 restatement. The
**2,500 Keystone Hero** row appears in no Tier-1 12.1 capture at all — treat both
its rating and its reward as secondary-source only. `rating-and-rewards.md` is
the file of record for this ladder and carries the same split.

Mount and title rewards are **seasonal**: they stop being obtainable when
Season 2 ends.

### Dungeon teleports

Completing **Mythic 10 or higher within the time limit** unlocks a permanent
teleport to that dungeon — eight dungeons, eight teleports (Tier-1, stated
directly in the Season 2 blog). Season 1's teleports are unaffected and stay.

## Per-dungeon detail

One file each — route, notable trash, and boss tables with archetype +
consequence tags, every ability tagged against the
[mechanic-archetype taxonomy](../../systems/mechanic-archetypes.md).

- [Altar of Fangs](altar-of-fangs.md)
- [Murder Row](murder-row.md)
- [Den of Nalorakk](den-of-nalorakk.md)
- [The Blinding Vale](the-blinding-vale.md)
- [Voidscar Arena](voidscar-arena.md)
- [Ruby Life Pools](ruby-life-pools.md)
- [Kings' Rest](kings-rest.md)
- [Temple of Sethraliss](temple-of-sethraliss.md)

All eight are **new files in the 12.1 sweep** — none existed before Season 2,
and the three returning dungeons need fresh captures because of the announced
design/QoL updates.

## TODO

- [ ] Confirm the **S2 affix ladder** in game / from a Tier-1 source, and settle
      whether the blog's "Season 2 brings about new Affixes" line reaches Mythic+
      or only Prey; if it differs from S1, fix this file and `affixes.md` together.
- [ ] Read the **Keystone Hero** and **Keystone Myth** *rating thresholds* off
      achievement game data (Blizzard achievement API / wago) — Blizzard published
      neither number for S2. The Keystone Myth achievement and its title are
      Tier-1; only its threshold is open.
- [ ] Record **Warcraft Logs encounter IDs** for the eight S2 dungeons (the S1
      file carries them; WCL's S2 zone needs to be read once logs exist).
- [ ] Re-check the **+2 → +10 end-of-run and vault ilvl table** against live
      drops after 2026-08-18; it is tier-3 today.
- [ ] Enumerate what the "design and quality of life updates" to Ruby Life
      Pools / Kings' Rest / Temple of Sethraliss actually changed.

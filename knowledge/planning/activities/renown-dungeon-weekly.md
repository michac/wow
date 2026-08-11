---
id: renown-dungeon-weekly
name: Dungeon weekly (choice-rep → renown)
goal: [gearing]
venue: dungeon
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: dungeon_weekly }
reward: { type: [currency], detail: "one lump of choosable renown (KB record 1500; two Tier-3 12.1 guides say 1000 — unverified); in Season 2 point it at Zul'jarra's Forces for the Cursebreaker's Bracers ranks" }
reward_base: 1   # Phase 0 pin, kept — but see the ⚠ below: the S1 rationale for it (Singularity trinket already claimed) died with Season 2, and the pin is now under-valuing the common case rather than the rare one. Re-tune with the scoring model, not in a patch sweep.
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/candidates.json
  - knowledge/factions/
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369   # Midnight Season 2 overview — S2 dungeon pool (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 pre-season split (Tier 1)
  - https://www.method.gg/guides/zuljarras-forces-reputation-guide-for-wow-midnight  # dated 2026-08-10, 12.1 (Tier 3)
  - https://www.icy-veins.com/wow/news/players-skipping-these-weeklies-will-fall-behind-in-season-1/  # any-difficulty rule (Tier 3)
confidence: medium
---
Halduron Brightwing's weekly dungeon quest in Silvermoon, paying one lump of
**choosable renown**. **Renown is instrumental** (see `_facets.md`): retag if you're
chasing a recipe (`professions`) or mount (`collectibles`) instead of gear.

**Still rankable during the 2026-08-11 pre-season week.** The quest completes on a
Midnight dungeon at **any difficulty** — Normal, Heroic, Mythic 0, and Follower
Dungeons all count — so the absence of Mythic+ keystones until 2026-08-18 does not
block it. In fact this is the cheapest weekly on the board right now: **Mythic 0 is on
a one-week-only weekly lockout dropping Champion 1/6 (ilvl 292)**, so the clear you
were already doing for gear ticks this off for free. (See `mplus.md`, which *is*
`invalidated` this week — that file is the keystone activity, this one is not.)

**New Season 2 dungeon pool** (live now on Heroic + M0, Mythic+ from Aug 18):
**Altar of Fangs** (new, 3 bosses, inside the Vaults of Atal'Utek) · Murder Row ·
Den of Nalorakk · The Blinding Vale · Voidscar Arena · Ruby Life Pools · Kings' Rest ·
Temple of Sethraliss. The Season 1 pool (Algeth'ar Academy, Magisters' Terrace,
Maisara Caverns, Nexus-Point Xenas, Pit of Saron, Seat of the Triumvirate, Skyreach,
Windrunner Spire) has rotated out. Because any difficulty counts, the pool turnover
changes *what you queue*, not whether the weekly is completable.

**Point it at Zul'jarra's Forces now.** 12.1 adds a **sixth** renown faction (the
Coiled Isle's Zul'jarra's Forces, 20 ranks, quartermaster **Jan'sari the Watchful** at
Tokka's Landing) and it is a valid target for the choice-rep. It is also the only one
whose track still carries live power: **Cursebreaker's Bracers I/II** (Veteran →
Champion wrist). See `zuljarra-renown.md` / `../../factions/zuljarras-forces.md`.

⚠ **The old Singularity rationale is dead.** This row used to exist to buy the
Singularity rank-7 trinket (*Crucible of Erratic Energies*, **ilvl 246**). Season 2
gear spans **269 → 334** (Mistcrest bands, Tier-1 DB2), so every Season 1 renown gear
unlock now lands **below the S2 floor** and is worthless as gearing. The `reward_base: 1`
pin is therefore still *numerically* where it was but for the opposite reason: it was
pinned low because the geared main had already passed the unlock, and now **no
character has passed the Zul'jarra unlock** — i.e. the pre-unlock case the pin
deliberately under-values is currently *everyone*. Left as-is rather than re-tuned
mid-sweep; resolve it with the Phase-4 conditional (full gearing value below the unlock
rank) once renown rank lands in planner state.

**Gate TODO / open questions** — @verify-ingame
- **Quest ID still unknown.** Not exposed by any source; read the live quest log when
  it's picked up (also tracked in `../roadmap.md` and `../../endgame/weekly-checklist.md`).
- **Rep amount disputed.** This file has recorded **1500** since 12.0.x; two Tier-3
  12.1-era guides (Method 2026-08-10, Icy Veins) both say **1000**. No Tier-1 source
  states it. Read the quest reward in game and settle it.
- **Does it name a specific dungeon each week?** Sources phrase it both as "the
  Midnight dungeon" and as any dungeon in the rotation. Confirm on pickup.

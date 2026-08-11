---
title: Midnight Raids — Overview
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - Blizzard Game Data API, journal-expansion/516 + journal-instance/{1307,1314,1308,1305,1312} (tier 1)
  - Blizzard Game Data API, journal-instance/1320 "The Venomous Abyss" + 1317 "The Tidebound Grotto", namespace static-12.1.0 (tier 1)
  - Warcraft Logs zone 46 "VS / DR / MQD" (tier 2)
  - https://worldofwarcraft.blizzard.com/en-us/news/24294062 (tier 1 — Venomous Abyss raid overview)
  - https://worldofwarcraft.blizzard.com/en-us/news/24295085 (tier 1 — Lairs preview)
  - https://us.forums.blizzard.com/en/wow/posts/29833350 (tier 1 — S1 ending / S2 information, the unlock schedule)
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes (tier 1)
  - https://news.blizzard.com/en-us/article/24272110/prepare-to-face-rotmire-in-the-sporefall-raid (tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214 (tier 1 — Mistcrest currency IDs 3437–3441 + per-track upgrade bands; the floor for every S2 ilvl number here)
  - https://worldofwarcraft.com/en-us/news/24293281 (tier 1 — 12.1 Content Update Notes; the four global class changes that apply in every instance)
confidence: high
---

# Midnight Raids

Patch **12.1 "Curse of Ula'tek"** went live **2026-08-11**, but **Midnight
Season 2 does not open until 2026-08-18**. The week in between is an official
**pre-season week**, and for raiding it is the quietest week of the expansion:

> ⚠ **During pre-season (Aug 11–17) there is no current-tier raid.** The
> Venomous Abyss does **not** open until the week of **Aug 18**. The Season 1
> raids below are still enterable but are now **previous tier**. The only new
> instanced boss content live this week is the **Tidebound Grotto lair on World
> difficulty** (see *Lairs*).

| Instance | Journal ID | Bosses | Status | File |
|---|---|---|---|---|
| **The Venomous Abyss** | 1320 | 8 | **current tier** — opens 2026-08-18 | `venomous-abyss.md` |
| The Tidebound Grotto | 1317 | 1 | lair (new format) — World live now, N/H/M Aug 18 | `../lairs.md` |
| The Voidspire | 1307 | 6 | previous tier (S1) | `the-voidspire.md` |
| The Dreamrift | 1314 | 1 | previous tier (S1) | `the-dreamrift.md` |
| March on Quel'Danas | 1308 | 2 | previous tier (S1) | `march-on-quel-danas.md` |
| Sporefall | 1305 | 1 (Rotmire) | previous tier (S1, added 12.0.7) | `sporefall.md` |
| Midnight (world bosses) | 1312 | 4 rotating | superseded in practice by Lairs | below |

Warcraft Logs zone 46 ("VS / DR / MQD") tracks the original nine Season 1
bosses; Sporefall and the Venomous Abyss are separate instances.

> ⚠ **No raid here is "unchanged by 12.1", even the ones with no
> instance-specific notes.** Four global changes apply to every spec in every
> instance, current tier and previous tier alike: **player health and creature
> damage both +25% at max level** (health consumables rescaled, and several
> DPS/Tank healing + absorb spells retuned to keep their relative impact);
> **major DPS cooldowns lowered with steady-state damage raised** on several
> specs, which moves the burst/sustained split; **interrupts now show a "missed"
> visual + sound** when the target was not casting; and **diminishing-return
> categories now reset after 20s** (was 16s). Any absolute HP / healing / potion
> number written before 2026-08-11 — including in the previous-tier raid files —
> is now wrong.

## The Venomous Abyss (12.1 — Season 2)

Eight-boss raid on **The Coiled Isle**, level **90**, the culmination of the
Curse of Ula'tek story: Ula'tek is an ancient creature of hatred, corruption and
venom unleashed by Zul'jan's actions. Difficulties are **Raid Finder / Normal /
Heroic / Mythic**, plus a **Story Mode** that unlocks the week of Aug 25.
**Raid Finder minimum item level: 273.**

Boss order (names + encounter IDs from the in-game journal, `journal-instance/1320`):

| # | Boss | Encounter ID | LFR wing |
|---|---|---|---|
| 1 | Nek'zali the Soulcoiler | 2888 | 1 |
| 2 | The Twin Fangs | 2887 | 1 |
| 3 | Entombed Sentinels | 2874 | 2 |
| 4 | Vashnik the Malignant | 2882 | 2 |
| 5 | The Lost Explorers | 2894 | 3 |
| 6 | Sszorak | 2871 | 3 |
| 7 | The Coiled Altar | 2883 | 4 |
| 8 | Ula'tek | 2895 | 4 |

### Unlock schedule (Tier 1 — the "S1 ending / S2 information" blue post)

| Date | What opens |
|---|---|
| Week of **Aug 11** (pre-season) | **Nothing.** The raid is closed. |
| Week of **Aug 18** | **Normal / Heroic / Mythic** all at once, plus **LFR Wing 1 "The Soulcoilers"** (Nek'zali, Twin Fangs) |
| Week of **Aug 25** | **LFR Wing 2 "The Essence of Venom"** (Entombed Sentinels, Vashnik) + **Story Mode** |
| Week of **Sep 1** | **LFR Wing 3 "The Serpent Warren"** (Lost Explorers, Sszorak) |
| Week of **Sep 8** | **LFR Wing 4 "The Tomb of Ula'tek"** (Coiled Altar, Ula'tek) |

Note the departure from the usual staggered opening: Normal, Heroic **and**
Mythic all open on day one of the season.

### Rewards

- **Class armor sets drop here** — 13 tier sets across all classes. (Sporefall
  had none; this is a real tier raid.) The class-set vendor **Kirana** has moved
  from the March on Quel'Danas entrance to **beside the Catalyst in Silvermoon**
  and stocks the Season 2 sets for **Slumbering Coil Curios**.
- **Primeval Skyfriend** mount — drops from **Mythic Ula'tek** (3 copies per kill).
- Title **"Venom's End"** for killing Mythic Ula'tek; **"Famed Slayer of
  Ula'tek"** for the Hall of Fame (first 200 guilds world-wide).
- Battle pet **Ula'took** from the "No Egg Scramble" achievement.
- **Great Vault tracks changed in 12.1**: LFR / Normal / Heroic raid vault
  rewards now arrive at **the first step of the next harder difficulty's track**
  (so every Heroic-raid vault reward is **Myth 1/6**). Mythic raid vault rewards
  arrive at **Myth 6/6**, except Very Rare items and loot from the **penultimate
  and final bosses** (The Coiled Altar, Ula'tek), which are **Myth 9** whether
  they came off the boss or out of the vault. See `../great-vault.md`.

**Item level per difficulty** — Blizzard published the LFR entry requirement
(273) but not the raid's own per-difficulty drop steps. The **track ladder** below
is **Tier 1** and is the floor: 1/6 values are verbatim from the Lairs reward
table, ceilings from the `CurrencyTypes` DB2 upgrade bands at build
`12.1.0.69214` (Adventurer 269–282 · Veteran 282–295 · Champion 295–308 · Hero
308–321 · Myth 321–334 — see `../dawncrests.md`). What is **inferred** is only
the standard LFR→Veteran / Normal→Champion / Heroic→Hero / Mythic→Myth mapping,
and exactly which step within a track each boss drops at:

| Difficulty | Track | Drops at (1/6) | Fully upgraded (6/6) |
|---|---|---|---|
| Raid Finder | Veteran | 279 | 295 |
| Normal | Champion | 292 | 308 |
| Heroic | Hero | 305 | 321 |
| Mythic | Myth | 318 | 334 |

Very Rare items and loot from the **penultimate and final bosses** are the
exception — Blizzard's notes put those at **Myth 9**, above the ordinary 6/6
crest ceiling, from the boss or the vault alike (no upgrading needed).

Season 2 gear as a whole spans **269 → 334**, a clean +45 shift on Season 1's
224 → 289. ⚠ Do not let an editorial "S2 item level" article pull these down —
several published in the patch-launch week carry a ladder about 6 ilvl low
(e.g. Mythic capped at 328). The DB2 bands above win.

See `venomous-abyss.md` for boss mechanics.

## Lairs — a new raid-adjacent format (12.1)

**Lairs** are Blizzard's "evolution of world bosses": instanced single-boss
encounters at fixed outdoor locations (like Delves), each with a **summoning
stone outside**. They are the biggest structural change to outdoor endgame in
12.1 and they sit between world bosses and raids — raid-style bind-on-pickup
loot on a **weekly lockout**, but soloable at the entry difficulty.

- **Difficulties: World / Normal / Heroic / Mythic** (Mythic is flexible 15–25).
- On **World** difficulty you queue in solo and play a **two-part scenario** —
  clear elites until the boss appears — while the instance backfills. The boss
  itself **scales 5–40 players**.
- Pre-made groups pick the difficulty before entering and get filled around.
- Loot is **bind-on-pickup**, **weekly lockout**, and a **Voidcore may be spent
  once per week per lair** (Voidcore bonus rolls themselves only return the week
  of Aug 25).
- Recommended ilvl runs **273 (World) → 312 (Mythic)**; drops **279 → 318**.

**The Tidebound Grotto** (journal-instance 1317, category RAID, 1 encounter) is
the first lair: on the **Coiled Isle**, level **90**, boss **Nymrissa
Wavecaller** (encounter 2849), a naga sorceress. The entrance is **underwater**
below the isle — bring an aquatic mount. Nymrissa drops 12 unique items across
the difficulty tiers.

| Difficulty | Recommended ilvl | Drops | Crest |
|---|---|---|---|
| World | 273 | 279 (Veteran 1/6) | Veteran Mistcrest |
| Normal | 286 | 292 (Champion 1/6) | Champion Mistcrest |
| Heroic | 299 | 305 (Hero 1/6) | Hero Mistcrest |
| Mythic | 312 | 318 (Myth 1/6) | Myth Mistcrest |

All four rows are Tier 1, verbatim from the Lairs preview table (re-read
2026-08-11) — this is the source that names all four Mistcrest tiers.

**Availability:** World difficulty is live **now** (pre-season, Aug 11);
**Normal / Heroic / flexible Mythic arrive the week of Aug 18.** Full detail in
`../lairs.md`.

## Sporefall (12.0.7) — previous tier

Single-boss raid in **Harandar** against the fungal giant **Rotmire**.
Available in **Raid Finder / Normal / Heroic / Mythic**. It was the game's first
**flexible Mythic** (scales **15–25** players) rather than fixed 20 — the
Venomous Abyss and the Tidebound Grotto's Mythic both inherit that.

- **Sporefused gear** by difficulty: RF **259** · Normal **272** · Heroic
  **285** · Mythic **298**. These are Season 1 items and are **no longer
  upgradeable** past the S1 caps.
- No tier set / class weapons drop here.
- Collectibles: **Luminous Sporeglider** mount (earned by collecting 4
  Delicious Sporesnacks from weekly Rotmire kills), **Luminous Rotshroom**
  housing decor, plus toys/cosmetics/achievement rewards.
- RF entry requirement: level 90, ~ilvl 240.

Still worth a weekly clear for the mount and the collectibles; it is no longer a
gearing activity in Season 2. See `sporefall.md` for boss mechanics.

## World boss rotation (journal-instance 1312 "Midnight")

One up per week:

| Boss | Journal encounter |
|------|-------------------|
| Lu'ashal | 2827 |
| Thorm'belan | 2829 |
| Predaxas | 2828 |
| Cragpine | 2782 |

⚠ **12.1 froze this rotation as Season 1 content.** World boss drops remain
**Season 1 items and can no longer be upgraded**. **Lairs are the format that
replaces this loop** for Season 2 gearing — the old world bosses stay up for
collectors and completionists. See `../world-events.md`.

## TODO

- [ ] World boss zones/locations and loot
- [ ] Confirm **which step within its track** each Venomous Abyss difficulty
      actually drops at, against live loot once Season 2 opens (Aug 18). The
      track ladder itself is settled Tier-1 (DB2 bands + the Lairs 1/6 anchors);
      what is unconfirmed is only whether raid drops land on 1/6 like the lair
      rows do, or a step or two higher. *(The Tidebound Grotto Mythic crest name
      is no longer open — Myth Mistcrest, Tier-1, 2026-08-11.)*
- [ ] Raid unlock schedule for **Season 1** (which difficulties/wings opened
      when); the Season 2 schedule is recorded above

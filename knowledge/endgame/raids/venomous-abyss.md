---
title: The Venomous Abyss (Raid — Midnight Season 2, added 12.1) — STUB
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24294062/ (tier 1 — Venomous Abyss raid preview)
  - https://worldofwarcraft.com/en-us/news/24294369 (tier 1 — Midnight Season 2 overview)
  - https://worldofwarcraft.com/en-us/news/24293281 (tier 1 — Curse of Ula'tek content update notes)
  - https://us.forums.blizzard.com/en/wow/posts/29833350 (tier 1 — end of S1 / start of S2 information)
  - Blizzard Game Data API, journal-instance/1320 "The Venomous Abyss", namespace static-12.1.0 (tier 1 — instance + encounter IDs)
  - wago.tools CurrencyTypes DB2 @ 12.1.0.69214, currency IDs 3437–3441 (tier 1 — Mistcrest upgrade bands; raw/wago/CurrencyTypes-12.1.0.69214.csv)
confidence: medium
---

# The Venomous Abyss

> ⚠ **NOT OPEN YET.** Written on patch day (**2026-08-11**), a week before the
> raid exists. **The raid opens with maintenance the week of 2026-08-18**, when
> Midnight Season 2 begins; 12.1 shipped on Aug 11 in a **pre-season** state
> with no raid available. Everything below is from Tier-1 Blizzard previews,
> patch notes and game data (journal + DB2) — **nothing here has been seen in
> game**. Boss *names*, encounter IDs, room grouping and a set of *named*
> mechanics (via achievement criteria) are known; full ability lists, routes and
> loot tables are not. Re-source after Aug 18 (see `## TODO`).

The **8-boss** Midnight **Season 2** raid, added in patch **12.1 "Curse of
Ula'tek"**. Located on **The Coiled Isle**, level **90**. The raid ends with
**Ula'tek** herself — an ancient creature of hatred, corruption and venom,
unleashed by **Zul'jan's** actions, which is the throughline of the 12.1
campaign.

Available in **Raid Finder / Normal / Heroic / Mythic / Story Mode**. Weekly
lockout. Raid Finder **minimum item level: 273**.

## Unlock schedule

| Date | What opens |
|------|-----------|
| 2026-08-11 (12.1 launch) | **Nothing** — pre-season week, no raid |
| week of 2026-08-18 | **Normal / Heroic / Mythic** (all 8 bosses) + **Raid Finder Wing 1** |
| week of 2026-08-25 | Raid Finder **Wing 2** + **Story Mode** |
| week of 2026-09-01 | Raid Finder **Wing 3** |
| week of 2026-09-08 | Raid Finder **Wing 4** |

## Bosses

**Order and encounter IDs are from game data** — the Blizzard Game Data API,
`journal-instance/1320` "The Venomous Abyss", namespace `static-12.1.0` (Tier 1).
Wing assignment is from the LFR schedule above.

⚠ **Do not take the boss order from the preview article's prose.** The preview
lists bosses grouped by *room* (Soulcoil Well → Vile Crypt → Crypt of the
Soulcoilers → Pit of Fangs → Coiled Altar), which puts The Twin Fangs sixth, and
its all-difficulty meta achievement lists them in a third order again. The
journal order below is the authoritative one.

| # | Boss | Encounter ID | Room | LFR wing |
|---|------|---|---|----------|
| 1 | Nek'zali the Soulcoiler | 2888 | The Soulcoil Well | Wing 1 — *The Soulcoilers* |
| 2 | The Twin Fangs (Vexhul + Ithraz) | 2887 | Pit of Fangs | Wing 1 — *The Soulcoilers* |
| 3 | Entombed Sentinels (Blood + Breath of Ula'tek) | 2874 | The Vile Crypt | Wing 2 — *The Essence of Venom* |
| 4 | Vashnik the Malignant | 2882 | Chamber of Virulence (Vile Crypt) | Wing 2 — *The Essence of Venom* |
| 5 | The Lost Explorers | 2894 | Crypt of the Soulcoilers | Wing 3 — *The Serpent Warren* |
| 6 | Sszorak | 2871 | Crypt of the Soulcoilers | Wing 3 — *The Serpent Warren* |
| 7 | The Coiled Altar | 2883 | The Coiled Altar | Wing 4 — *The Tomb of Ula'tek* |
| 8 | Ula'tek | 2895 | The Coiled Altar | Wing 4 — *The Tomb of Ula'tek* |

### What is and isn't known about mechanics

The journal **is** readable — `journal-instance/1320` and all eight encounter
IDs were pulled from the live API on 2026-08-11 (see `overview.md`). What has
**not** been distilled yet is each encounter's full ability list; that is a
`journal-encounter/<id>` pull away, not a wait for the raid to open.

Beyond names, the Tier-1 preview publishes per-boss lore and — through the
achievement criteria — a set of **named mechanics**:

| Boss | Named mechanic / object (from achievement criteria) |
|---|---|
| Nek'zali the Soulcoiler | **Kupamanduka**, returned to the Soulcoil Well |
| Entombed Sentinels | **Vitriolic Stasis** (a self-heal each Sentinel uses) |
| Vashnik the Malignant | **Solidified Snake Venom** (a killable add) |
| The Lost Explorers | **Hoji** (an optional extra explorer) |
| Sszorak | rings that appear and can be jumped through |
| The Twin Fangs | **Ravenous Feast** — feed Ithraz slimes in order: Crunchy Appetizer → Sumptuous Soup → Tasty Blob → Jiggly Dessert |
| The Coiled Altar | **Unnerving Fixation** (a debuff that can be spread to all players) |
| Ula'tek | **Greasy Hatchling** (an egg that can break during the fight) |
| *(instance-wide)* | **Ancestral Vision** — a visitable vision containing 8 trapped spirits |

⚠ These are mechanic *names and shapes*, not strategies. **Do not answer "how do
I do <boss>" from this file** — no rotation, no positioning and no timings are
known, and nothing here has been observed in game.

### This raid is entered under the 12.1 global retune

There are no *instance-specific* 12.1 changes to record here — the raid is new —
but four **global** class changes shipped with 12.1 and apply inside it, and
they change how every encounter feels relative to Season 1:

1. **Player health and creature damage both +25% at max level.** Health
   consumables were rescaled to match, and healing/absorb spells on several DPS
   and Tank specs were retuned. Any absolute HP or healing number written before
   2026-08-11 is wrong.
2. **Major DPS cooldowns lowered and steady-state damage raised** for several
   specs — burst/sustained splits have moved.
3. **Interrupts now show a "missed" visual + sound** when the target was not
   casting. Relevant here given how much of this raid's known mechanic set is
   add- and cast-shaped.
4. **Diminishing-return categories reset after 20s** (was 16s).

See `_meta/changelog-12.1.md` → *Classes (12.1)* for the full list.

## Loot

**Blizzard has published no per-difficulty drop ilvls directly** — only the LFR
*entry* requirement (273). Do not infer them from Sporefall's 259/272/285/298
band; that is a Season 1 raid and the Season 2 ladder sits ~45 ilvl higher.

**The Tier-1 floor is the Season 2 upgrade ladder**, from `CurrencyTypes` DB2 @
`12.1.0.69214` (currency IDs 3437–3441). Season 2 gear spans **269 → 334**:

| Crest | Upgrade band |
|---|---|
| Adventurer Mistcrest | 269–282 |
| Veteran Mistcrest | 282–295 |
| Champion Mistcrest | 295–308 |
| Hero Mistcrest | 308–321 |
| Myth Mistcrest | 321–334 |

**For per-difficulty numbers, use `overview.md`'s ladder** — it maps each
difficulty onto one of these tracks (LFR → Veteran, Normal → Champion, Heroic →
Hero, Mythic → Myth) and gives the drop step and the 6/6 ceiling for each. Its
1/6 values are Tier-1 verbatim from the Lairs reward table and its ceilings are
the DB2 band tops above; what is **inferred** is only the difficulty-to-track
mapping and the exact step each boss drops at. Do not re-derive per-difficulty
bands here, and treat any editorial "S2 item level" ladder as suspect until it
matches those numbers.

What *is* known:

- **Class sets** drop here — the preview lists **13 class armor sets**, one per
  class. (Sporefall, the S1 raid, dropped no tier set; this one does.)
- The Season 2 class sets are also purchasable from **Kirana**, relocated to
  **near the Catalyst in Silvermoon**, for **Slumbering Coil Curios**.
  See `endgame/catalyst.md` and `endgame/raids/march-on-quel-danas.md`.
- **Great Vault tracks changed in 12.1** and apply to this raid:
  Raid Finder / Normal / Heroic vault rewards come in at the **first step of the
  next harder difficulty's track** (so every Heroic-raid vault reward is
  **Myth 1/6**); **Mythic** raid vault rewards come in at **Myth 6/6**, except
  **Very Rare** items and loot from the **penultimate and final bosses**, which
  are **Myth 9** whether they came from the boss or the vault.
  See `endgame/great-vault.md`.
- **Nebulous Voidcore** raid re-roll now costs **1** (was 2), but Voidcore bonus
  rolls are **not available in the first Season 2 Great Vault** — they arrive the
  week of **2026-08-25** and need at least 3 vault panes unlocked.

## Collectibles & achievements

- **Primeval Skyfriend** (mount, item 275658) — drops from **Mythic Ula'tek**.
  The Season 2 overview settles what "3×" means: *"Defeating Mythic Ula'tek
  drops 3 mounts"* — i.e. **3 copies per kill**, not three colour variants.
- **"Venom's End"** (title) — the reward on *Mythic: Ula'tek*, defeat **Ula'tek
  on Mythic**.
- **"Famed Slayer of Ula'tek"** (title) — *Hall of Fame: Ula'tek*, the first
  **200 guilds** world-wide to kill Mythic Ula'tek.
- **Ula'took** (battle pet) — the reward on **"No Egg Scramble"**: *defeat
  Ula'tek before the Greasy Hatchling breaks*, on **Normal difficulty or
  higher**.
- **Housing decor trophies** — **100% drop to every raid member** from killing
  Ula'tek, tiered by difficulty:
  - Raid Finder / Normal → **The Venomous Abyss Argent Trophy**
  - Heroic → Argent **+ Gleaming**
  - Mythic → Argent + Gleaming **+ Aureate**

### Achievements

**All difficulties** — four meta achievements, each a defeat-these-bosses list:

- *The Venomous Abyss: Essence of Ula'tek* — Nek'zali; Entombed Sentinels; Vashnik
- *The Venomous Abyss: Beasts of Ula'tek* — The Lost Explorers; Sszorak; The Twin Fangs
- *The Venomous Abyss: Ula'tek* — The Coiled Altar; Ula'tek
- *The Venomous Abyss* — all eight bosses on any difficulty

**Normal or higher** — nine feats-of-strength-style achievements, one per boss
plus an instance-wide one. Their criteria are the mechanic names listed under
*Bosses* above: *Well, Well, Little Sky* · *Is Venom Stasis A Joke To You?* ·
*Accidental Inclusion* · *Kept You Waiting Huh?* · *Jumping Through Hoops* ·
*Taking a Bite out of Slime* · *Watch Out Behind You* · *No Egg Scramble*
(→ Ula'took) · *Comforting Da Spirits*.

**Heroic or higher** — **Ahead of the Curve: Ula'tek**, before the next raid
tier releases.

**Mythic** — a per-boss *Mythic: <boss>* achievement for seven of the eight
(the preview omits one for The Twin Fangs), plus **Cutting Edge: Ula'tek**
before the next tier releases.

*(Achievement names are transcribed from the Tier-1 preview, which contains
several obvious typos in boss names — "Ssorak", "Ulatek", "Unnerving Fication".
Confirm exact strings against the in-game achievement UI after Aug 18.)*

## See also

- `overview.md` — the raid lineup, updated for 12.1. It carries this raid's
  journal/encounter IDs, the same unlock schedule, and the **per-difficulty
  track ladder** pointed at under *Loot*.
- `endgame/lairs.md` — **Tidebound Grotto**, the new instanced world-boss format
  that opens alongside this raid (World difficulty was already live in the
  pre-season week).
- `systems/coiled-isle.md` — the zone this raid sits in.
- `_meta/changelog-12.1.md` — the 12.1 change ledger.

## TODO

This file is a **day-1 stub**. It was written on 2026-08-11 from Blizzard
previews and game data; Tier-3 guides (Icy Veins, Wowhead) had not been updated
because the raid did not exist yet. Fill it in **on or after 2026-08-18** from,
in order:

1. **Tier 1 — game data.** `wowkb.blizzard journal-encounter <id>` for each of
   the eight encounter IDs tabled above — this is the outstanding pull, and it
   yields each boss's **ability list** and loot table. `wowkb.blizzard item` for
   drop item levels. This settles ability names and ilvl bands, not editorial
   prose. *(The instance ID and the encounter list are already done — 1320 and
   2888/2887/2874/2882/2894/2871/2883/2895.)*
2. **Tier 1 — Blizzard.** Any raid-release blue post / hotfix batch archived into
   `_meta/patch-notes/12.1.md`, plus the raid preview above re-read for anything
   this stub missed.
3. **Tier 2 — Warcraft Logs.** `wowkb.wcl` for the new zone id once logs exist:
   confirms the pull order groups actually use and gives per-boss cast lists.
4. **Tier 3 — guides.** Icy Veins / Wowhead raid guides for mechanics prose and
   strategy, once they exist. Corroborate every number against 1–3; they must
   never overwrite a Tier-1 value — in particular the Mistcrest bands under
   *Loot*.

Specifically still missing: **observed per-difficulty drop item levels** (only
the LFR entry requirement, 273, is Tier-1 published directly — and it is already
recorded in `_meta/moving-values.md`; the rest is `overview.md`'s inferred
difficulty-to-track mapping), **each encounter's ability list and any strategy**,
notable trinkets/weapons, and the class-set piece-to-boss mapping. Once the drop
bands are confirmed against live drops, add them to `_meta/moving-values.md`
beside the existing LFR-minimum row (Sporefall's band row is the model), confirm
or correct `overview.md`'s inferred mapping against them, and drop the "NOT OPEN
YET" banner + the `— STUB` title suffix.

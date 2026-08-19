---
title: Delves — Midnight Season 2 (12.1 "Curse of Ula'tek")
patch: 12.1
fetched: 2026-08-18
reviewed: 2026-08-18
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281   # 12.1 Curse of Ula'tek content update notes (Tier 1) — 3 new delves, Coffer Key Shard retune
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 information (Tier 1) — the pre-season delve rules, verbatim in _meta/patch-notes/12.1.md
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214     # Tier 1 game data — all five Mistcrest names, base rows 3437-3441 + cap/crafting-bearing rows 3442-3446, per-track upgrade ilvl bands (local copy: raw/wago/CurrencyTypes-12.1.0.69214.csv, read directly 2026-08-11)
  - https://www.icy-veins.com/wow/midnight-delve-rewards-guide  # S2 per-tier ilvl table (Tier 3, updated 2026-08-01, PTR-sourced)
  - https://www.icy-veins.com/wow/delvers-journey-guide         # S2 Delver's Journey rank table (Tier 3, updated 2026-07-30, PTR-sourced)
  - https://www.icy-veins.com/wow/delves-guide                  # S2 delves guide (Tier 3, updated 2026-08-03) — Bountiful rerolls on the DAILY reset + in-game countdown; "non-Bountiful Delves do not have scaling rewards past Tier 3"
  - https://www.bluetracker.gg/wow/topic/eu-en/557563-feedback-delves-in-season-2/  # Blizzard blue post 2025-01-16 (Tier 1, but TWW 11.1-era) — Bountiful selection rotates through the pool "until all of them have had some time in the sun" (replaced one-per-zone)
  - https://conquestcapped.com/guides/wow/midnight-delves-season-2/  # corroborates 13-delve pool + Azta'rec "?"/"??" unlock conditions (Tier 3)
  - https://www.wowhead.com/news/how-to-unlock-myth-dawncrests-from-delves-in-midnight-season-1-380813  # S1 history
  - IN-GAME field test 2026-07-10 (Uncomplete) — S1: T11 open at 90; Bounty Hidden Trove 1/week reward-locked
confidence: medium
---

# Delves (Midnight Season 2)

Solo/small-group scaling endgame pillar. Tiers 1–11, plus the **Nemesis
difficulties "?" and "??"**.

## ⚠ 12.1 shipped in two steps — read this before quoting any reward

**12.1 went live 2026-08-11. Midnight Season 2 does not open until
2026-08-18.** The week between is an official **pre-season week**, and delves
are one of the pillars most reshaped by it. Most published delve guides
describe the **Aug-18** state.

| | **Now — pre-season (Aug 11–17)** | **From Aug 18 — Season 2** |
|---|---|---|
| Tiers | 1–11 **+ "?" Nemesis** | same, **+ "??" Nemesis** |
| Bountiful | **none — Bountiful Delves do not appear** | Bountiful Delves appear |
| Coffer Keys | **do not drop** | **Coffer Keys begin dropping** |
| Max reward | **Adventurer 3/6 gear (ilvl 272) + Veteran Mistcrests** | full S2 table below |

Source for that split is Tier 1 (Blizzard's "Season 1 Ending and Season 2
Information" post, archived verbatim in `../../_meta/patch-notes/12.1.md`).
Anything below marked *(S2)* is **upcoming, not live today**.

> ⚠ **Two Tier-1 statements disagree on this week's tier ceiling — flagged, not
> silently resolved.** The **content-update notes** say that with the start of
> Season 2 on Aug 18 "players will be able to push into the upper tiers to
> challenge themselves **beyond Tier 7** and face the new Nemesis boss"
> (`../../_meta/patch-notes/12.1.md` line 147) — which reads as a **Tier-7
> ceiling during the pre-season**. The **Season-1-ending post** says "Delve
> difficulties **1-11** will be available, along with the '?' Nemesis
> difficulty" (line 1611). This file follows the second, because it is the
> specific post written to answer exactly this question and it enumerates the
> tiers rather than gesturing at them — but the conflict is **unresolved**, and
> it is the single most quotable line in this file this week. **Confirm the
> highest selectable tier at a delve entrance before planning a T8+ evening.**
> @verify-ingame

## 12.1 changes

- **Three new Delves**, all on the Coiled Isle: **The Ring of Glory** (an Amani
  arena, north end of the isle), **Gnarldor Isle** (the overgrown coast), and
  **the Venomfall Deeps** — a **Nemesis Delve**, in the poisoned waterways
  beneath the island. Nothing rotates out, so the pool is **13** (10 S1 delves
  + 3).
- **New snake and venom enemy variants seeded into the existing Midnight
  Delves** — beyond that the S1 delves take **no delve-specific changes** in
  12.1 (layouts and gimmicks stand). ⚠ That is **not** the same as "they play
  the same": see the global retune immediately below.
- ⚠ **The difficulty moved even where the delve did not.** 12.1's game-wide
  class pass raises **player health and creature damage by 25% at max level**,
  rescales health consumables to match, and retunes several **healing and absorb
  spells on DPS and Tank specs**; separately, **major DPS cooldowns came down
  while steady-state damage went up** for a number of specs. None of this is
  delve-scoped, and delves are not exempt from it — so any remembered
  "T11 is comfortable at ilvl X" feel from 12.0.7 is **stale**, and every
  absolute HP / potion / self-heal number written before 2026-08-11 is wrong.
  Re-feel a tier before you burn a key on it. Two more game-wide changes land
  squarely in solo play: **interrupts now show a "missed" visual + sound** when
  the target was not casting, and **diminishing-return categories reset after
  20s** (was 16) — both matter when you are your own kicker and CC chain.
  Details in `../../_meta/changelog-12.1.md`.
- **New Nemesis boss: Azta'rec**, in the Venomfall Deeps. Two difficulties:
  **"?"** (live now) and **"??"** *(S2, Aug 18)*. Defeating **"??" during the
  first week of Season 2** earns the Fabled achievement **"Let Me Solo Him:
  Azta'rec"** — a first-week-only window, per Tier-1. (Tier-3 reporting says
  "?" unlocks after clearing Tier 7 with lives remaining and "??" after Tier 10
  with lives remaining — unconfirmed, @verify-ingame.)
- **Coffer Key Shard amounts adjusted from multiple sources**, weighted toward
  Coiled Isle content. ⚠ Blizzard explicitly calls this **ongoing and a work in
  progress** — **treat every specific shard number as volatile** and re-check
  before planning a farm around it.
- **Delver's Journey resets for Season 2** with new unlocks. Its rank count and
  progress numbers are **Tier-3 only** — see the section below.
- Prey S2 ties into delves: **Afflicted Souls** (Champion-track bonus gear) and
  **Tormented Souls** (Hero-track) drop from **Heavy Trunks in Tier 6+ Bountiful
  Delves** and accelerate Nightmare hunts; bonus equipment is once per week per
  character *(S2 — Bountifuls don't exist yet)*. See `../prey.md`.

## Crests: Season 1 Dawncrests → Season 2 **Mistcrests**

**All five tier names are Tier-1 confirmed from game data**, not guesswork:
wago `CurrencyTypes` DB2 @ `12.1.0.69214`
(`raw/wago/CurrencyTypes-12.1.0.69214.csv`) carries **Adventurer / Veteran /
Champion / Hero / Myth Mistcrest** with their upgrade bands. These numbers are
the **floor** — no guide's per-tier ilvl table may override them.

**Why each crest has two IDs, and why the pair is not interchangeable:** the DB2
ships **two blocks** — **3437–3441** and **3442–3446** — with the same five
names, the same five upgrade bands and the same earned-from source lists. They
**diverge on the fields that matter**, read straight off
`raw/wago/CurrencyTypes-12.1.0.69214.csv`:

- **3437–3441** — `MaxQty` **0**, `MaxQtyWorldStateID` **0**. No cap machinery.
- **3442–3446** — `MaxQty` **100**, `MaxQtyWorldStateID` **30933**
  (Adventurer/Veteran/Champion) / **30934** (Hero/Myth). These are also the only
  rows carrying the **crafting line** ("sets the item level of the resulting item
  to 266–279", etc.) — on 3442/3443/3445/3446; Champion **3444** has no crafting
  line at all.
- `MaxEarnablePerWeek` is **0 on all ten rows**.

So the cap-bearing (and, bar Champion, crafting-bearing) rows are specifically
**3442–3446**.
Cite the ID that carries the field you are talking about; do not treat the pair
as identical. `../dawncrests.md` owns this claim.

| Crest | Currency IDs |
|---|---|
| Adventurer Mistcrest | 3437 / 3442 |
| Veteran Mistcrest | 3438 / 3443 |
| Champion Mistcrest | 3439 / 3444 |
| Hero Mistcrest | 3440 / 3445 |
| Myth Mistcrest | 3441 / 3446 |

Their upgrade bands:

| Crest | Upgrades its track to ilvl |
|---|---|
| Adventurer Mistcrest | 269–282 |
| Veteran Mistcrest | 282–295 |
| Champion Mistcrest | 295–308 |
| Hero Mistcrest | 308–321 |
| Myth Mistcrest | 321–334 |

Each band starts at rank 2/6. **`../dawncrests.md` owns the full table** — it
carries each track's **1/6 entry ilvl** as well, corroborated against the Lairs
reward table, and that is the version to quote. Don't re-derive the 1/6 values
here.

## Loot table (Season 2)

⚠ **Confidence note for this whole half of the file.** Everything from here to
the end of the Delver's Journey section that is not the DB2 crest bands is
**Tier-3, PTR-sourced guide prose, and unverifiable in game until 2026-08-18**,
when Bountifuls, Coffer Keys and "??" Nemesis turn on. That is what the file's
`confidence: medium` is describing. Quote the pre-season table at the top of
this file for anything you are doing *this* week.

### Is the table below keyed-only above Tier 3? — an open question, not a settled one

Tier-1 says that during the pre-season "the maximum tier of rewards available
from Delves will be **Adventurer 3/6 gear and Veteran Crests**", and it says so
**while tiers 1–11 are all open**. There are **two readings of that one sentence
and this file does not pick between them**:

1. **Structural** — an unkeyed delve stops at Adventurer 3/6 whatever tier you
   run, so the per-tier ladder below is what a **Bountiful** delve of that tier
   pays. (If a plain unkeyed T8 paid Champion 2/6, the pre-season cap could not
   be Adventurer 3/6.)
2. **Blanket pre-season cap** — the sentence is a flat reward ceiling for this
   week only, saying nothing about keyed-vs-unkeyed scaling once S2 opens. This
   is what **S1's measured shape** would predict: there the plain end-of-run
   chest scaled with tier up to Champion 2/6 at T8–11.

Either way, **nothing below row 3 is reachable this week** — Coffer Keys don't
drop until Aug 18. What is unresolved is whether rows 4–11 stay Bountiful-only
*after* Aug 18. Do not quote rows 4–11 as this week's rewards, and do not quote
them as keyed-only after Aug 18 either until someone has looked. @verify-ingame

**Reading 1 gained a corroborating source on 2026-08-18, and it is not enough to
close this.** Icy Veins' 12.1 delves guide states flatly: *"Non-Bountiful Delves
do not have scaling rewards past Tier 3"* and *"for End of Delve runs, loot
rewards are capped out at Tier 3"* — i.e. a structural keyed-only ladder, with
no pre-season qualifier attached. That is **Tier 3**, and worse, it is
**plausibly circular**: a guide written in the pre-season week could be
paraphrasing the same Blizzard sentence this section is trying to interpret,
which would make it an echo rather than an independent observation. It moves the
odds toward reading 1; it does not settle it. **The deciding measurement is one
unkeyed T8 run on or after Aug 18** — if the end-of-run chest pays above
Adventurer 3/6, reading 1 is dead. @verify-ingame

*(Per-tier assignments: Icy Veins, updated 2026-08-01 off the 12.1 PTR —
**Tier 3**, not in-game verified. The track boundaries corroborate exactly
against the DB2 crest bands above, which is what earns them any credit at all.)*

| Tier | End-of-run gear | Reachable this week? |
|---|---|---|
| 1 | 266 — Adventurer 1/6 | yes |
| 2 | 269 — Adventurer 2/6 | yes |
| 3 | **272 — Adventurer 3/6** | yes — **and this is the ceiling** |
| 4 | 276 — Adventurer 4/6 | no — not this week *(S2)* |
| 5 | 279 — Veteran 1/6 | no — not this week *(S2)* |
| 6 | 282 — Veteran 2/6 | no — not this week *(S2)* |
| 7 | 292 — Champion 1/6 | no — not this week *(S2)* |
| 8–11 | 295 — Champion 2/6 | no — not this week *(S2)* |

- **A Bountiful delve is opened with a Restored Coffer Key** *(S2)* — and keys
  do not drop at all until Aug 18. Together with the Tier-1 Adventurer-3/6
  pre-season cap, that is why rows 4–11 are unreachable for everyone this week
  regardless of tier or gear.
- ⚠ Whether rows 4–11 need **re-splitting into keyed vs unkeyed columns** is the
  open question above. If in-game testing on/after Aug 18 shows unkeyed chests
  scaling past Adventurer 3/6 — S1's shape — then this is one table for both,
  and reading 1 was wrong. @verify-ingame
- **Great Vault delve/world row** *(S2)*: scales 279 (Veteran 1/6) up to
  **305 (Hero 1/6)**, which is reached at **Tier 8** — tiers 9–11 do **not**
  raise the vault ilvl, they raise crests and the Journey. ⚠ For the **first**
  S2 vault (claimable Aug 18) the World row is capped at **Champion 3/6**;
  Hero 1/6 only from the second vault onward (`../great-vault.md`).
- **Crest tier by delve tier — Tier 1, from the Mistcrest currency descriptions
  themselves**: **T4 → Adventurer · T5–6 → Veteran · T7–10 → Champion · T11 →
  Hero Mistcrest**. (Verbatim source lists in `../dawncrests.md`.)
- ⚠ **The "T11 Gilded Stash pays Myth Mistcrests" claim is contradicted by game
  data and is dropped.** The **Myth** Mistcrest row (3441/3446) names only
  **Mythic The Venomous Abyss** and **Mythic Keystone +9 and up** — **no delve
  source at all** — while T11 delves appear on the **Hero** row. Doctrine
  resolves this against DB2, not guide prose. If a Gilded Stash does pay Myth in
  week 1 of S2, that is a Tier-1-vs-Tier-1 surprise worth recording here.
  @verify-ingame

## Which delves are Bountiful, and how often that changes

**The Bountiful flag is a property of the DAY, not of the delve.** A delve is
not permanently Bountiful; a rotating subset of the pool wears the flag, and
you spend a Restored Coffer Key inside one of *those* to open the Bountiful
Coffer.

- **Cadence: the set rerolls at the DAILY reset** — not weekly. The in-game UI
  shows **a countdown to the next reroll**, so you never have to guess: the
  Delver's Guide at Delver's Headquarters (Journeys tab) marks today's set, and
  Bountiful delves render with **glowing map icons**. *(Tier 3 — Icy Veins
  delves guide, updated 2026-08-03, written for 12.1 / Season 2.)*
- **So yes, it changes across a single week — seven different sets per week.**
  The practical consequence for a key stockpile: a day with fewer Bountifuls up
  than you hold keys costs you nothing, because **keys carry across resets**
  (see the cap bullet below). You are never racing a key against a day.
- **Selection is a ROTATION through the pool, not one-per-zone and not per-player
  RNG.** Blizzard replaced the original one-bountiful-per-zone logic in TWW
  Season 2: *"The new logic will rotate through delves from the original launch
  until all of them have had some time in the sun as bountiful before turning on
  new ones."* — blue post 2025-01-16. ⚠ **That is Tier 1 but it is TWW-era**: it
  describes the mechanism's design, and no 12.1 note revisits it, but it is not
  a 12.1 confirmation. Treat as *current shape, last stated for 11.1*.
- **Everyone sees the same set on a given day** — it is a server-wide rotation,
  not rolled per character. *(Tier 4 — player reports; consistent across
  threads, never contradicted, never blue-confirmed.)*
- ⛔ **HOW MANY are Bountiful at once is NOT KNOWN for the 13-delve Season 2
  pool.** Checked 2026-08-18 across Icy Veins, Conquest Capped, Wowhead's delve
  system guide and five Season 2 SEO guides: **not one publishes a per-day
  count.** Do not infer it from TWW's numbers — the pool grew from 10 to 13 in
  12.1 and the rotation logic is explicitly "until all have had a turn", which
  makes the count a tuning knob. **Count it in game.** @verify-ingame

## Delver's Journey (Season 2 track)

⚠ **Everything in this section is Tier-3** (Icy Veins, 2026-07-30, PTR-sourced)
and is **not verifiable in game until Bountifuls turn on Aug 18** — the rank
count, the progress numbers and the rank table alike. The Tier-1 12.1 notes
describe a **10-level Prey Journey** (`../../_meta/patch-notes/12.1.md` line
189), *not* a Delver's Journey rank count, so don't mistake one for a source for
the other. Do not plan a week around a specific rank number yet. @verify-ingame

Reported shape *(Tier-3)*: **4,200 progress/rank, 42,000 total over 10 ranks** —
same shape as S1, different unlocks. Progress: weekly quest turn-in **1,500** ·
opening a Bountiful Coffer **250** · Bountiful runs **50–150** by tier.

| Rank | Unlock *(S2, Tier-3)* |
|---|---|
| 1 | Boons and Blessings from end-of-delve rewards |
| 2 | Corrosive Reticule (6 Corrosive Souls) |
| 3 | Shrine of Abundance appears in Bountiful delves |
| 4 | **Gilded Stash after a Tier 11 delve — Hero Mistcrests, up to 4×/week** (this row's "+ Myth" is Tier-3 and contradicted by DB2 — see the loot section) |
| 5 | Corroded Soul Crusher mount; **Zah'ran** sells Champion gear (from week 3) |
| 6 | **Buy 2 Restored Coffer Keys/week** (Naleidea Rivergleam) |
| 7 | Delve-O-Bot 7001 upgrade chip |
| 8 | **Champion Warbound equipment from Tier 9+ delves** (farmable → mail to alts) |
| 9 | **Hero equipment from Tier 11 Bountiful Coffers** |
| 10 | Title **"Snake Eater"**; increased Coffer Key Shards |

Vendors: **Naleidea Rivergleam** and **Telemancer Astrandis** at Delver's
Headquarters; **Zah'ran** for the Journey gear. Currency reporting is
inconsistent across Tier-3 sources (Undercoin / Voidlight Marl / an S2
successor to Untainted Mana-Crystals) — **unresolved, @verify-ingame**.

Companion: **Valeera Sanguinar** (levels like TWW's Brann; carried from S1). A
12.0.7 hotfix gave **tank Valeera accompanied by a healer** a tier-scaled
damage-taken reduction (values verbatim in
`../../_meta/patch-notes/12.0.7.md`). Those are **12.0.7-era numbers and are not
restated here**: 12.1's game-wide **+25% player health / +25% creature damage**
retune is exactly the kind of pass that rescales companion mitigation, and no
12.1 note says either way. Treat the mitigation as *S1 shape, unconfirmed for
S2*. @verify-ingame

## Carried-over mechanics — status unconfirmed for S2

These were solid **Season 1 measurements**. No 12.1 note removes them, but none
of the S2 material re-confirms them either, and **none can be tested until
Aug 18**. The default here is *S1 shape, unconfirmed for S2* — **not "probably
still true"**, which is too generous a hedge for a season boundary that already
changed the crest names, the whole ilvl ladder and the vault tracks. Where game
data actively points the other way, the bullet says so and wins. Do not build a
plan on anything in this section. @verify-ingame

- **The weekly cap is on SHARDS EARNED, not on keys held — and an
  already-restored key from another source bypasses it entirely.** In S1: **600
  Coffer Key Shards per week**, with **100 shards auto-converting to a Restored
  Coffer Key on delve entry** (Naleidea Rivergleam will also convert on demand)
  → 6 keys/week *from shards*. Whole keys handed to you do **not** count against
  that: the **2 keys in Naleidea's Delver's Starter Kit** (Journey rank 6) land
  on top, so **8 keys in a week is a normal total, not a bug**. Keys are stored
  and **carry across resets** — an unspent key is not lost, so a week with fewer
  Bountifuls up than you have keys costs you nothing. Do **not** restate this as
  "max 6 Bountiful Coffers/week"; that inference is wrong and was in this file
  until 2026-08-18. With the 12.1 shard retune explicitly "a work in progress",
  **the S2 shard rates and the 600 number itself are unconfirmed**.
  @verify-ingame
- **Delver's Bounty** map → consumed during a Bountiful delve before the final
  boss dies, spawns a **Hidden Trove** at the end. In S1 the Hero trove was
  **one per character per week — the lockout was on the REWARD, not the map**,
  and it was **shared with the Prey weekly's map**. Whether the S2 delve reward
  structure keeps this shape is unverified.
- ⚠ **Crest totals are NOT known to be uncapped in S2 — do not carry S1's
  "caps removed" forward.** The 2026-05-19 hotfix that removed the 100/tier/week
  accumulation cap was a **Season-1** action, and `../dawncrests.md` says
  explicitly not to carry it into S2. What game data actually supports, read
  precisely: the **duplicate rows 3442–3446** carry a **holding** cap
  (`MaxQty` **100**) gated by a movable world state (**30933** Adv/Vet/Champ,
  **30934** Hero/Myth), while `MaxEarnablePerWeek` — the field that would encode
  a literal per-week earn cap — is **0 on every Mistcrest row**. So *some* cap
  machinery is back, but **a weekly cap is Tier-3 reporting, not game data**.
  A world-state gate also means the live number can change by hotfix.
  `../dawncrests.md` owns this claim and states it the same way. @verify-ingame
- Delve **runs** themselves were unlimited in S1 — the gates were keys, Gilded
  Stashes and the weekly cache, with only *per-activity* chunks weekly-limited.
  That is an **S1 measurement and nothing in the 12.1 notes re-confirms it**;
  it is listed here as prior shape, not as a live S2 fact. @verify-ingame
- For the vault world row, **Ritual Sites** compete directly — their T1–6 vault
  rewards were **realigned to match Season 2 Delve tiers 1–6** in 12.1 and they
  now pay S2 crests at Delve-equivalent rates (`../../systems/ritual-sites.md`).

## Delve pool (13)

Season 1 ten (all returning, now with snake/venom variants):

1. Collegiate Calamity
2. Atal'Aman
3. The Grudge Pit
4. Shadowguard Point
5. Parhelion Plaza
6. The Darkway
7. Twilight Crypts
8. The Gulf of Memory
9. Sunkiller Sanctum
10. The Shadow Enclave

New in 12.1 (Coiled Isle):

11. The Ring of Glory
12. Gnarldor Isle
13. The Venomfall Deeps — **Nemesis** (Azta'rec)

## Season 1 — historical

Retained because alts and warband math still reference it; **none of this is a
current reward**.

- S1 loot capped at **Champion 250 (2/6)** from both the end-of-run chest and
  the keyed Bountiful Coffer at T8–11; **Hero 259 (1/6)** came only from the
  Great Vault delve/world row, a **Delver's Bounty** map consumed in-run, or
  **Delver's Journey rank 9** (a Hero *chance* in T11 coffers) — the T8+ coffer
  was never Hero without that rank.
- Only solo Myth **Dawncrest** source was the T11 Bountiful **Gilded Stash**
  (~20/week, 3 stashes, Journey rank 4). S1 vendor currency: **Untainted
  Mana-Crystals** (currency 3356; earn cap 250/wk, hold 1,000).
- S1 delve Nemesis was **Nullaeus**; the S1 weekly was ≥1 Tier 11 delve +
  4 Bountiful delves → weekly cache.
- 12.0.7 "Revelations" made no structural delve change; its **Delver's Call XP
  buff** (first-time completions, ~80k–140k+ XP) was a leveling/alt buff only.
  Its 12.1 status is unchecked.

## TODO

- [ ] **Re-verify the whole S2 reward table in game from 2026-08-18**, when
      Bountifuls, Coffer Keys and "??" Nemesis turn on. Everything marked
      Tier-3 above is PTR-sourced guide prose. @verify-ingame
- [ ] **Resolve the Tier-1 vs Tier-1 tier-ceiling conflict** — content-update
      notes imply a **Tier 7** pre-season ceiling, the S1-ending post says
      **1–11**. Read the highest selectable difficulty at a delve entrance this
      week and record which post was right. @verify-ingame
- [ ] **Read the live Mistcrest cap off the currency tooltip** in week 1 of S2 —
      and record whether it says "this week" or "maximum". DB2 gives rows
      3442–3446 a *holding* cap of 100 behind world states 30933/30934 and
      leaves `MaxEarnablePerWeek` unset, so a **weekly** cap is Tier-3 only.
      Reconcile with `../dawncrests.md`, which owns this claim. @verify-ingame
- [ ] **Confirm whether unkeyed end-of-run chests scale past Adventurer 3/6**
      once Bountifuls are live — this decides between the two readings of the
      Tier-1 pre-season cap noted above the loot table (structural keyed-only
      ladder vs a blanket pre-season ceiling). S1's shape was the latter.
      @verify-ingame
- [ ] Confirm the **S2 weekly Coffer Key SHARD cap** (S1: 600/week) after the
      shard retune settles (Blizzard calls the retune a work in progress), and
      re-confirm that vendor-bought whole keys still sit outside it. Also count
      **how many delves carry the Bountiful flag at once and on what cadence the
      set rotates** — the file has never carried a claim on this, and the S1
      shape (a subset re-flagged at the DAILY reset) is untested for S2.
      @verify-ingame
- [ ] Confirm the **Delver's Journey S2 vendor currency** name(s). @verify-ingame
- [ ] Per-delve location + gimmick notes for the three new delves (Ring of
      Glory, Gnarldor Isle, Venomfall Deeps) — own files, like
      `gulf-of-memory.md`
- [ ] Valeera upgrade path / curio equivalents in S2
- [x] S1 Myth-stash conflict (resolved 2026-07-07) and the S1 "T9 champion
      trinket" observation (resolved 2026-07-09) — both now historical, see the
      Season 1 section

## Changelog

2026-08-18 — Added "Which delves are Bountiful, and how often that changes": the flag rerolls at the DAILY reset (in-game countdown + glowing icons), selection is a rotation through the pool per Blizzard's 2025-01-16 blue post (TWW-era), and the set is server-wide. The PER-DAY COUNT for the 13-delve S2 pool is published nowhere — left open, not guessed. Also recorded Icy Veins' "non-Bountiful Delves do not have scaling rewards past Tier 3" as corroboration for reading 1 of the keyed-only question, flagged as possibly circular.

2026-08-18 — Coffer Key cap restated: the weekly limit is 600 SHARDS, not 6 keys. Vendor-bought whole keys (Naleidea's 2-key Starter Kit) sit outside the cap, so 8 keys in a week is normal; keys also carry across resets. The old "max 6 Bountiful Coffers/week" line was a false inference and is deleted. Field-observed 8 keys (Uncomplete, S2 opening day).

2026-08-17 — S1's T8+ Bountiful Coffer capped at Champion 250; Hero needed Delver's Journey rank 9, a Bounty map or the vault, not the coffer alone.

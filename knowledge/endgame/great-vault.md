---
title: Great Vault — Midnight Season 2 (12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-20
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Curse of Ula'tek content update notes (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season details (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24295085   # Lairs preview — S2 track ↔ ilvl anchors (Tier 1)
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-2/  # S2 M+ vault table (Tier 3, upd. 2026-08-02)
  - https://www.icy-veins.com/wow/great-vault-guide   # slot unlock thresholds (Tier 3)
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide  # S1 table (historical)
confidence: medium
---

# Great Vault (Midnight Season 2)

Weekly gear chest in the capital; slots unlock from last week's activity.
Open it after reset, before doing anything else.

## ⚠ Read this first — the vault is mid-season-transition right now

12.1 went live **2026-08-11**, but **Season 2 does not open until 2026-08-18**.
The week in between is an official **pre-season week**, and the vault behaves
differently in it (Tier 1, S1-ending blue post):

- **The vault you open the week of Aug 11 pays out on your *final Season 1
  week* activity** — S1 rows, S1 tracks, S1 item levels. Nothing about 12.1's
  new reward rules applies to it.
- **Season 2 vault credit starts accruing during the pre-season week.** What you
  do Aug 11–17 fills the panes you will **claim on Aug 18**.
- So this week: do the activities, but judge the *offered* items by the Season 1
  tables below (kept as history), not by the Season 2 ones.

Everything in the "Season 2 rules" section is **effective with the first S2
vault (claimable 2026-08-18)** unless the row says otherwise.

## Slot unlock counts (verified in-game 2026-06-03, vault UI)

Unchanged in 12.1 — the thresholds are the same, only the qualifying content
rolled to Season 2:

- **Raids**: defeat 2 / 4 / 6 Midnight Season 2 bosses
- **Dungeons**: complete 1 / 4 / 8 Heroic, Mythic, or Timewalking dungeons
- **World**: complete 2 / 4 / 8 world activities (Delves, Prey, Ritual Sites,
  world activities)

@verify-ingame Icy Veins' 12.1 vault page words the raid row as "bosses in the
**two raids** of Midnight Season 2" (i.e. Venomous Abyss plus a second raid
still counting for credit). No Tier-1 note says that. Confirm on/after Aug 18
whether previous-tier raid bosses still fill S2 raid panes.

## Season 2 rules — what 12.1 changed

### Raid row: every reward jumps a difficulty (Tier 1)

Verbatim rule from the 12.1 notes (ITEMS → RAID REWARDS):

| Raid difficulty cleared | Vault reward comes in at |
|---|---|
| Raid Finder | first step of the **Normal** track |
| Normal | first step of the **Heroic** track |
| Heroic | **Myth 1/6** (stated by name in the notes) |
| Mythic | **Myth 6/6** |
| Mythic **Very Rare** items, and loot from the **penultimate and final bosses** | **Myth 9** — and that applies whether the item came from the boss directly or from the vault |

This is the single biggest gearing change in 12.1: a Heroic raid vault slot is
now a Myth-track item, so Heroic raiding feeds Myth gear without setting foot in
Mythic. @verify-ingame the exact **item levels** these tracks map to in the live
S2 build — day-1 third-party raid tables disagree with each other (one has the
Myth track topping out at 328, another has Myth 1/6 at 318), so only the *track
names* above are trustworthy today.

### The Season 2 bonus-roll currency — ⚠ NAME DISPUTED, verify week of Aug 25

⚠ **Do not quote a currency NAME from this section until it is confirmed in game.**
Two sources disagree and neither is conclusive:

- **This file previously asserted (Tier 1, from the 12.1 notes) that the S2
  bonus-roll currency is the *Nebulous Voidcore*** — the same currency as S1.
- **The user reports (2026-08-20) that the S2 currency is the *Venomous
  Voidcore*.**
- **Game data is ambiguous and does not settle it.** `CurrencyTypes` DB2 at
  **both** 12.1.0.69214 and the live client build **12.1.0.69382** carries
  `3511 = "[DNT, Unused] Venomous Voidcore"` — described as the Season 2
  equivalent, but flagged Unused — alongside two live *Nebulous Voidcore* rows
  (`3418`, `3513`). A `[DNT, Unused]` marker is a **development flag, not proof
  the currency does not ship**; Blizzard routinely leaves such names uncleaned on
  currencies that go live. Encomplete's `/simc` export tracks **both**
  (`bonus_roll_currencies=3418:0/3511:0`), which is consistent with either.

The currency does not exist on any character yet — it first appears as a **Great
Vault option the week of Aug 25**. **Read the name off the vault UI that week and
resolve this.** @verify-ingame

*(Recorded 2026-08-20: an earlier revision stated the Nebulous name as settled
Tier-1 fact. That confidence was not warranted — the 12.1 notes were read as
naming the S2 currency when they may only have been describing S1 wind-down.)*

### Mechanics (independent of the name)

- Season 1 Voidcores **convert to gold** at the end of S1 and can no longer be
  spent on S1 content.
- **From the start of Season 2, Voidcores are a Great Vault reward option.**
- ⚠ **Not in the first S2 vault.** Voidcore bonus rolls arrive the **week of
  Aug 25** (second week of S2) and can be selected by anyone who has unlocked
  **at least 3 panes**. (Icy Veins' page says "starting with the first week of
  Season 2" — that is **wrong**; the Tier-1 blue post is explicit that week 1 has
  none.)
- The **raid re-roll cost is now 1 Voidcore** (was 2). Items bought with a
  Voidcore remain **item-level-equivalent to a vault reward**.
- **Orin Straylight** has relocated **near the Catalyst in Silvermoon** and
  hands out **one extra Voidcore per week starting week 8 of Season 2**.
- A Voidcore can also be spent **once per week per Lair** (see `lairs.md`).
- The **Tier 6 Advanced Ritual Studies** quests no longer offer a Voidcore bonus
  roll (still completable for the achievement) — see `../systems/ritual-sites.md`.

### World row is capped, and the cap moves after week 1 (Tier 1)

- **First S2 vault (claimable Aug 18): World row maxes at Champion 3/6.**
- **Every vault after that: World row maxes at Hero 1/6.**

That kills the S1 habit of treating the world row as a near-free Hero-track
slot in the opening week. It also interacts with the pre-season Delve caps —
during the pre-season week Delves only pay **Adventurer 3/6 gear + Veteran
crests**, and **there are no Bountiful Delves** until Aug 18
(`delves/overview.md`).

### Dungeon row during the pre-season week

Mythic 0 is on a **weekly** lockout for the week of Aug 11 only and drops
**Champion 1/6 (292)**; it returns to a daily lockout on Aug 18 when keystones
start dropping (`mythic-plus/keystones.md`). Heroic/M0 runs done this week still
count toward the **Season 2** dungeon panes you claim on Aug 18.

## Mythic+ slot ilvls — Season 2 (from 2026-08-18)

Tier-3 table (ConquestCapped, updated 2026-08-02). Its track ↔ ilvl anchors
agree with the Tier-1 Lairs reward table (Veteran 1/6 = 279 · Champion 1/6 = 292 ·
Hero 1/6 = 305), which is why it is carried here — but the numbers have **not**
been seen in a live vault yet. @verify-ingame confirm against the vault UI at the
first S2 reset.

| Key level | End-of-run ilvl | Crest | Vault ilvl |
|-----------|-----------------|-------|------------|
| Mythic 0 | 292 (Champion 1/6) | — | — |
| +2 to +3 | 295 (Champion 2/6) | Champion Mistcrest | 305 (Hero 1/6) |
| +4 | 298 (Champion 3/6) | Hero Mistcrest | 308 (Hero 2/6) |
| +5 | 302 (Champion 4/6) | Hero Mistcrest | 308 (Hero 2/6) |
| +6 to +8 | 305 (Hero 1/6) | Hero Mistcrest | 311–315 (Hero 3–4/6) |
| +9 | 308 (Hero 2/6) | **Myth Mistcrest** | 315 (Hero 4/6) |
| **+10 and up** | 311 (Hero 3/6) | Myth Mistcrest | **318 (Myth 1/6)** |

→ **+10 is still the vault target** — it is the first key level whose vault
reward is Myth-track. Run 8× +10 for max M+ row choices.
⚠ Season 2 crests are **Mistcrests**, not Dawncrests (`dawncrests.md`).

## Mythic+ slot ilvls — Season 1 (HISTORICAL, ended 2026-08-11)

Kept because the vault opened during the pre-season week still pays out on S1
activity. Do not use these for anything after Aug 18.

| Key level | End-of-run ilvl | Vault ilvl |
|-----------|-----------------|------------|
| Mythic 0 | 246 | 256 |
| +2 to +3 | 250 | 259 |
| +4 to +5 | 253–256 | 263 |
| +6 to +9 | 259–263 | 266–269 |
| **+10 and up** | 266 | **272 (cap)** |

## World row mechanics (measured in S1 — mechanics still apply, caps do not)

The *shape* of the world row was measured in-game during Season 1 and 12.1
changed none of it; only the reward ceiling moved (above). Keep the mechanics,
discard the S1 item levels.

- **Each slot's reward = the Nth-highest world activity of the week** — slot 1 =
  2nd-highest, slot 2 = 4th, slot 3 = 8th. Confirmed by the vault-slot tooltip
  (2026-06-05): *"Current Reward: Item Level 259 - (Tier 9) · Top 2 Runs This
  Week: Tier 10 (1), Tier 9 (1) · Reward at Highest Item Level."*
- **Vault credit is per completion, not per loot.** A T10 delve counted for the
  vault even though the Bountiful Coffer was lost to deaths.
- **Unkeyed delve completions count as world activities.** In S1 that made
  6 keyed + 2 unkeyed T8s enough to put all three world slots at the cap.
- **Low-tier fillers drag the slot down.** Because the reward is the Nth-highest
  activity, a stack of T3 ritual sites fills the counters but lowers what the
  slot offers. Use rituals for accolades/crests, delves for vault slot quality.
- **The vault UI shows ilvl only, not track** — hover the actual item at reset
  for its "Upgrade Level: <track> x/6" line if the track matters.
- The world row **can offer real class tier-set pieces** (observed in S1:
  Abyssal Immolator's Fury warlock shoulders) — no Catalyst charge needed.
- **Skipping the gear pays a flat 6× currency** instead (observed 2026-06-03;
  currency identity still unverified — likely the seasonal vault token).
- Ritual sites → vault tier mapping is being realigned in 12.1: **T1–6 vault
  rewards now match Season 2 Delve tiers 1–6**, with new recommended ilvls
  **T4 259 · T5 268 · T6 275** (`../systems/ritual-sites.md`).

## Open questions

- @verify-ingame Item levels behind the S2 raid-row tracks (Normal-first-step,
  Heroic-first-step, Myth 1/6, Myth 6/6, "Myth 9"). Tier-1 gives names only and
  day-1 third-party tables conflict.
- @verify-ingame Whether the S2 raid row counts bosses from more than one raid
  (see the slot-unlock note above).
- @verify-ingame The S2 M+ vault ilvl table above, against the live vault UI at
  the first S2 reset (2026-08-18).
- @verify-ingame The identity of the "skip the gear" currency payout.

---
title: Crests — Mistcrests (Midnight S2) & Dawncrests (S1, historical)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24295085   # Lairs preview — Tidebound Grotto reward table, the Tier-1 Mistcrest names + track 1/6 ilvls
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 information — pre-season week reward caps
  - https://worldofwarcraft.com/en-us/news/24293281            # 12.1 Content Update Notes — crest sources re-pointed to S2
  - https://worldofwarcraft.com/en-us/news/24293963            # Coiled Isle / Vaults of Atal'Utek — Trovehunter's Bounty as a Vaults reward
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214       # TIER-1 FLOOR — Mistcrest IDs 3437-3446: names, per-track ilvl bands, crafting ilvls, cap fields, and the per-crest source map (local pull: raw/wago/CurrencyTypes-12.1.0.69214.csv)
  - https://wago.tools/db2/Achievement?build=12.1.0.69214          # "…of the Mist" IDs 62410/62411/62412/62414/62416 (+ CriteriaTree for the high-watermark triggers)
  - https://conquestcapped.com/guides/wow/wow-midnight-mistcrests/     # T3/T4 — 20/rank, Vaskarn 30→10, per-tier source map (2026-08-07)
  - https://www.method.gg/guides/mistcrests-from-mythic-dungeons-and-raid-bosses-in-wow-midnight-season-2  # T3 — M+/raid amounts (2026-08-10)
  - https://www.icy-veins.com/wow/news/these-five-mistcrests-decide-how-fast-your-gear-climbs-in-midnight-season-2/
  - https://www.wowhead.com/news/upgrade-achievements-cut-crest-costs-by-50-in-midnight-380457  # 50% discount, achievement-gated (Feb 2026)
  - IN-GAME field test 2026-07-10 (Uncomplete) — full crests charged; TWW 0-crest same-slot rule is GONE
  - IN-GAME 2026-07-11 (Encomplete) — all-slots-263 → Champion of the Dawn → 50% Champion **Dawncrest** discount (S1 only; does not carry to S2)
  - https://blizzardwatch.com/2026/03/02/upgrade-gear-midnight-no-valorstones-required/   # Valorstones removed
  - https://www.wowhead.com/currency=3343/champion-dawncrest         # S1 Champion track 246→263
confidence: high   # crest names, ilvl bands, track 1/6s, and the per-activity source map are Tier-1 DB2; only the per-run/per-boss AMOUNTS and the cap semantics remain Tier-3, and both are marked as such
---

# Crests — the gear-upgrade currency

⚠ **The Season 2 currency is the MISTCREST.** Dawncrests were **Season 1 only**
and are dead currency from S2 onward (see the historical section at the bottom).

*(**Filename decision, 2026-08-11:** `dawncrests.md` is kept deliberately — it is the
long-standing crest anchor and several files link to it, so the name is held for link
stability even though the document is now Mistcrest-primary. This is a recorded choice,
not an oversight; revisit only if the S1 section is ever split out.)*

**Upgrades cost crests + a small gold fee ONLY — Valorstones were REMOVED in
Midnight** (there is no stone/filler currency; a common stale-info trap).

## ⚠ Timing: 12.1 is live, Season 2 is not (as of 2026-08-11)

12.1 went live **2026-08-11**; **Midnight Season 2 opens the week of 2026-08-18**.
The week between is an official **pre-season week**, and it is already paying
**Season 2 crests** — the sources listed below were re-pointed at patch launch,
not at season start. What pre-season *withholds*:

- **Delves**: tiers 1–11 + "?" Nemesis only. **No Bountiful Delves, no Coffer
  Keys.** Max Delve reward is **Adventurer 3/6 gear + Veteran Crests**.
- **Mythic+**: nothing — keystones do not drop until Aug 18. **Mythic 0** runs on
  a **weekly** lockout this week only (Champion 1/6, 292 gear), then returns to daily.
- **Raid**: none. Venomous Abyss opens Aug 18.
- **Lairs**: Tidebound Grotto is **World difficulty only** (S2 Veteran).
- **Prey**: Normal + Hard only (S2 Veteran). Nightmare (Champion) opens Aug 18.

## The Season 2 tracks (Tier-1: wago DB2 + the Lairs reward table)

Five tiers, same shape as S1: **Adventurer / Veteran / Champion / Hero / Myth**.
Each crest upgrades **its own track only**.

| Crest | Currency IDs | Track 1/6 | Track 6/6 (ceiling) |
|---|---|---|---|
| Adventurer Mistcrest | 3437 / 3442 | **266** | **282** |
| Veteran Mistcrest | 3438 / 3443 | **279** | **295** |
| Champion Mistcrest | 3439 / 3444 | **292** | **308** |
| Hero Mistcrest | 3440 / 3445 | **305** | **321** |
| Myth Mistcrest | 3441 / 3446 | **318** | **334** |

Both columns are Tier-1. The 1/6 values for Veteran/Champion/Hero/Myth are verbatim
from the Lairs reward table (World 279 · Normal 292 · Heroic 305 · Mythic 318); the
ceilings are the top of each DB2 currency description ("up to item levels 269–282", etc.).

**Adventurer 1/6 = 266 is corroborated by game data, not inferred.** The duplicate DB2
rows carry a crafting line whose *low* value is exactly that track's 1/6: Adventurer
3442 "sets the item level of the resulting item to **266**–279", Veteran 3443
"**279**–292", Hero 3445 "**305**–318", Myth 3446 "**318**–331" — and 279 / 305 / 318 are
precisely the Lairs-table 1/6 drops. The same rule read on Adventurer gives **266**.
(Each crafting range runs from that track's 1/6 to the *next* track's 1/6, which is why
the highs look one tier off.)

Intermediate steps are ~3 ilvl each and are **not individually confirmed**.

**Note the overlap, it's the same trap as S1:** a *fully capped* lower-track piece
out-ilvls a *fresh* drop one track up — Champion 6/6 (**308**) beats a fresh Hero
drop (**305**). Hero only pulls ahead once crested.

### Cost per upgrade

**A flat 20 crests per rank → 100 crests to take a piece 1/6 → 6/6**, plus gold.
*(Tier-3, consistent across ConquestCapped / Icy Veins / Method 2026-08; the
Tier-1 notes do not state a cost. The "150 crests per piece" figure this file
carried for S1 was never sourced and is dropped.)*

### ⚠ Cap machinery is back in Season 2 — do not carry S1's "caps removed" forward

The May-19-2026 hotfix that removed accumulation caps was a **Season 1** action.
*Some* cap machinery is back in S2 — but read the DB2 fields precisely, because they
do **not** say "per week":

- The **duplicate rows 3442–3446** carry **`MaxQty` = 100**, gated by
  **`MaxQtyWorldStateID`** — **30933** (Adventurer/Veteran/Champion) and **30934**
  (Hero/Myth). `MaxQty` is a **holding cap** (how many you may have at once), and a
  world-state gate means the live number is whatever Blizzard sets that world state
  to and can be changed by hotfix without a patch — the same machinery S1 used to
  *raise* its cap over time.
- **`MaxEarnablePerWeek` = 0 on every Mistcrest row** — the field that would encode a
  literal per-week earn cap is **unset**.
- The **base rows 3437–3441** carry `MaxQty` 0 / `MaxQtyWorldStateID` 0 outright.

So **do not read `MaxQty` 100 as proof of a weekly cap.** Tier-3 guides report the
familiar **100 per tier per week, cumulative** (unearned cap rolls forward as
catch-up) with excess crests **downgrading to the tier below** — that framing is
*editorial*, and the only thing game data actually supports is a world-state-gated
holding cap of 100.

**Not Tier-1 confirmed as a weekly cap.** @verify-ingame — read the actual cap text
off a Mistcrest tooltip in week 1 of S2 and record whether it says "this week" or
"maximum", and whether it accumulates.

## Where Mistcrests come from

### Tier-1: the per-crest source map (wago `CurrencyTypes` DB2 @ 12.1.0.69214)

**This is game data and it is the floor.** Each Mistcrest's own currency description
names the activities that pay it, verbatim. (IDs 3437–3441 are the base rows;
3442–3446 are the duplicates that additionally carry the crafting line and the cap
fields — the source lists are identical across the pair.)

| Crest | Paid by (verbatim from the currency description) |
|---|---|
| **Adventurer** | Repeatable Outdoor Events · **Tier 4 Delves** |
| **Veteran** | Repeatable Outdoor Events · **Raid Finder** The Venomous Abyss · **Heroic** Season Dungeons · **Delves T5–6** · **Trovehunter's Bounty T4–5** |
| **Champion** | **Weekly** Outdoor Events · **Normal** The Venomous Abyss · **Mythic** Season Dungeons (= M0) · **Mythic Keystone +2 to +3** · **Delves T7–10** · **Trovehunter's Bounty T6–7** |
| **Hero** | **Heroic** The Venomous Abyss · **Mythic Keystone +4 to +8** · **Delves T11** · **Trovehunter's Bounty T8 and up** |
| **Myth** | **Mythic** The Venomous Abyss · **Mythic Keystone +9 and up** |

⚠ **The M+ key-level → crest-tier map is settled by this table: +2–3 Champion ·
+4–8 Hero · +9+ Myth.** Method's guide (2026-08-10) claims "+2–6 → Hero, +7–12+ →
Myth"; that is **contradicted by game data and is wrong** — do not plan from it.
Project doctrine resolves number conflicts against DB2, not editorial prose.
ConquestCapped (2026-08-07) agrees with DB2 on both the M+ and Delve maps.
⚠ Remember the timing gate: **keystones do not drop until Aug 18**, so the M+ rows
are correct-but-not-yet-earnable, and the raid rows open Aug 18 too.

**Trovehunter's Bounty** appears in this map and nowhere else in the crest material:
it is a **tiered** Vaults of Atal'Utek reward on the Coiled Isle (Tier-1 notes list it
alongside Corrosive Souls / Venom-Cursed Fragments / Corrosive Coins from Temple
Patrols, Strikes, Incursions and Ancient Foes). Its tiers 4–5 / 6–7 / 8+ pay
Veteran / Champion / Hero respectively — i.e. it is a **real, live-now crest engine
that the content-update notes never framed as one**. See `systems/coiled-isle.md`.

### Tier-1 confirmed (12.1 content update notes — these are live NOW)
- **Ritual Sites T1–T6** — now award **Season 2 crests at Delve-equivalent rates**,
  and T1–6 vault rewards match Season 2 Delve tiers 1–6. T1–3 keep S1 recommended
  ilvls; **new rec. ilvls: T4 259 · T5 268 · T6 275**. ⚠ The **T6 Advanced Ritual
  Studies quests no longer give a Nebulous Voidcore bonus roll** (still completable
  for the achievement). Still the solo player's repeatable volume engine.
- **Void Assaults** — Void Strikes, Void Incursions and the Weekly Quest give
  **Season 2 Adventurer crests**.
- **Val and Naigtal** — World Quests, rares and elites give **S2 Adventurer crests**
  in *both* Normal and Heroic World Tier. World Boss + Weekly Quests give **S2
  Adventurer** (Normal WT) / **S2 Veteran** (Heroic WT). Rare equipment stays
  Warbound-until-Equipped, now at **S2 Adventurer 1/6** (Normal) / **4/6** (Heroic).
- **Lairs — Tidebound Grotto** (weekly lockout, BoP loot): **World** → Veteran
  Mistcrest · **Normal** → Champion Mistcrest · **Heroic** → Hero Mistcrest ·
  **Mythic** → Myth Mistcrest. Only World difficulty exists until Aug 18.
- **Delves (pre-season week)** — capped at **Veteran** crests. The full DB2 map above
  (T4 Adventurer · T5–6 Veteran · T7–10 Champion · T11 Hero) is what applies from
  Aug 18; this week's Veteran ceiling is the pre-season restriction, not the tier map.
- **Trovehunter's Bounty (Vaults of Atal'Utek, Coiled Isle)** — **T4–5 Veteran ·
  T6–7 Champion · T8+ Hero**, per the DB2 map above. Live now.
- **Void-Touched Caches** are gear, not crests: new **S2 Adventurer Warbound** cache
  for **200 Field Accolades**; **S2 Veteran BoP** for **500** (random slot) / **750**
  (slot-specific). **The Season 1 gear caches were removed.**

### Tier-3 only: the *amounts*, which DB2 does not state
DB2 settles **which tier** each activity pays (table above). It says nothing about
**how many**, so the per-run / per-boss numbers below stay Tier-3 and unverified:

- **Raid, per boss** (Method, 2026-08-10): Normal **10–20 Champion** · Heroic
  **10–20 Hero** · Mythic **10–20 Myth**, with the **final boss** adding **10 of the
  next tier up**. *(Method's key-level → tier mapping in the same guide is wrong —
  see the DB2 note above — so treat its amounts with matching caution.)*
- **M+, per run** (Method): ~**10–18** at the lower key levels, ~**10–20** higher.
- **Vaskarn trade**: 30 → 10 (ConquestCapped, 2026-08-07).
- **Per upgrade rank**: a flat **20** (see "Cost per upgrade" above).

Nobody has measured any of this in the live season — **M+ and raid do not open until
Aug 18.** Re-check the amounts once S2 starts.

## The "…of the Mist" achievements — the S2 warband lever

The S1 "…of the Dawn" family has a **direct S2 replacement**, same structure, new
IDs and new (much higher) thresholds. ⚠ **Your S1 achievement does NOT carry the
discount into S2** — the discount is per-crest-currency, and Dawncrests are gone.
This lever resets to zero for everybody on Aug 18.

Tier-1 (wago `Achievement` + `CriteriaTree` DB2, 12.1):

| Achievement | ID | Trigger | Unlocks (Vaskarn trade) |
|---|---|---|---|
| Adventurer of the Mist | 62410 | high watermark **282** in every slot | Adventurer → Veteran |
| Veteran of the Mist | 62411 | high watermark **295** in every slot | Veteran → Champion |
| Champion of the Mist | 62412 | high watermark **308** in every slot | Champion → Hero |
| Hero of the Mist | 62414 | high watermark **321** in every slot | Hero → Myth |
| Myth of the Mist | 62416 | **average** ilvl **331** | — |

Each threshold is exactly that track's 6/6 ceiling — "outgrow this crest tier".

**Each achievement does TWO things** (carried from S1, corroborated Tier-3 for S2):
1. a **50% crest discount for that track, warband-wide** — alts pay **10 instead of
   20** per rank. The earner still pays full price; it's a lever for your *other*
   characters. (Midnight's figure is **50%**; TWW's was 33% — don't quote 33%.)
2. the **Vaskarn crest-trade unlock** for that tier (below).

Hard-won S1 lessons that still apply verbatim:

- ❌ **There is no "0-crest same-slot upgrade."** The TWW high-watermark rule
  (*"same slot up to the main's ilvl = free"*) did **not** carry into Midnight —
  field-tested 2026-07-10, the UI charged full crests. Any guide still saying
  same-slot upgrades are free is **stale TWW carryover; reject it.**
- **All-or-nothing gate:** *some* slots at the ceiling is not enough. One lagging
  slot → the achievement never fires → your alt pays full price.
- ⚠ **Crafted gear is the classic blocker:** a spark-crafted piece below the
  threshold with **no upgrade track** can't be crested up — it must be **recrafted
  higher or replaced**. The Blizzard API hides this (it drops track on crafted
  gear); only the addon tooltip read (PlannerState schema≥8) surfaces it.
- **If every slot is at the ceiling and it's still full price:** known Midnight
  discount-not-applying bug → relog / `/reload`; may need re-earn.
- **Tooling:** the CurseForge addon *Outgrow Crests Tracker* shows per-slot
  high-watermark progress and flags the slot holding the achievement back.
- **Addon detection:** the achievements are readable + **account-wide** via
  `GetAchievementInfo(id).completed` (wrap in `IsValidAchievement`). Actual crest
  cost is in `C_ItemUpgrade.GetItemUpgradeItemInfo().currencyCostsToUpgrade[]`, but
  it's `MayReturnNothing` — reliable only with the upgrade UI open, **not headless**.

## Vaskarn conversion (Silvermoon) — overflow only, not a farm
Vaskarn ("Crest Exchange", Silvermoon `/way #2393 48.6 61.7`) trades **30 lower-tier
→ 10 next-tier** crests. The per-tier unlock is the matching **"…of the Mist"**
achievement (table above). **3:1 is a bad rate** — ~300 Champion = 100 Hero = one
piece. Only worth it to drain a surplus you'll never otherwise spend; never a reason
to farm the lower tier deliberately. *(Vaskarn's S2 role is Tier-3-sourced; the
trade-unlock half is Tier-1 from the achievement reward text.)*

## For Encomplete (solo, pre-season week)
- **The Champion-of-the-Dawn discount you just earned is spent** — it applied to
  Dawncrests. Starting Aug 18 the equivalent lever is **Champion of the Mist**
  (308 in every slot), which is a *long* way up from S1's 263.
- **This week, crest income is: Ritual Sites (T4–T6, S2 crests, repeatable) +
  Delves 1–11 (Veteran cap) + Val/Naigtal world content (Adventurer) + Void
  Assaults (Adventurer) + Tidebound Grotto World (Veteran, weekly) +
  Trovehunter's Bounty in the Vaults of Atal'Utek (Veteran → Hero by tier).**
  That is the whole list — no M+, no raid, no Bountiful.
- **Pre-season is a gear-up week, not a crest-bank week** — DB2 shows a 100-per-tier
  cap gated by a world state (weekly or holding is unconfirmed), so hoarding past
  100 of a tier risks being wasted either way. Spend on the S2 pieces you actually
  pick up.
- Ritual Sites remain the solo repeatable engine, now at rec. **T4 259 / T5 268 /
  T6 275**.

## Season 1 — Dawncrests (HISTORICAL, do not plan from this)

Season 1 ran 2026-06-16 → 2026-08-11. **Unspent Dawncrests do not convert to
Mistcrests and have no S2 use** (Tier-3; unlike Nebulous Voidcores, which the
Tier-1 notes say convert to gold — the notes are silent on Dawncrests, so the "no
conversion" claim is *not* Tier-1). S1 gear caches were removed from the
Void-Touched Cache vendor.

- Currency IDs **3341–3348, 3383, 3391**. Tracks: Adventurer 224–237 ·
  Veteran 237–250 · Champion 250–263 · Hero 263–276 · Myth 276–289.
- **Champion track: 246 (1/6) → 250 → 253 → 256 → 259 (5/6) → 263 (6/6).**
- **Accumulation caps were REMOVED by the May-19-2026 hotfix** (they had been
  100/tier/week and were headed for 1,000). **This was Season-1-specific — see the
  S2 cap section above; do not carry it forward.**
- "…of the Dawn" achievements: Adventurer **61809** (237) · Veteran **42767** (250) ·
  Champion **42768** (263) · Hero **42769** (276) · Myth **42770** (285 avg).
  Encomplete earned **Champion of the Dawn** on 2026-07-11 by clearing the last three
  blockers (Ring 2 and Trinket 2 crested; the untracked crafted *Martyr's Waistwrap*
  belt **replaced** with a Champion-track *Sprawling Rhizomecord*).
- S1 one-time crest grants (now dead): **Cracked Keystone** (item 253245 → quest
  92600, 20 Hero + 20 Myth) and the **Nullaeus first kill** (30 Hero).

## TODO
- [ ] **Read the live cap off a Mistcrest tooltip in S2 week 1** @verify-ingame
      — DB2 gives `MaxQty` 100 behind world states 30933/30934 with
      `MaxEarnablePerWeek` **unset**, so game data supports a *holding* cap, not a
      weekly one. Confirm which the tooltip says, and whether it accumulates.
- [x] ~~Resolve the M+ crest-tier conflict~~ — **closed 2026-08-11 from DB2**:
      +2–3 Champion · +4–8 Hero · +9+ Myth (Method's "+2–6 → Hero" is wrong).
- [x] ~~Confirm the Adventurer Mistcrest 1/6 ilvl~~ — **closed 2026-08-11**: DB2
      currency 3442's crafting line gives **266**, matching the 1/6 rule that holds
      for Veteran 279 / Hero 305 / Myth 318.
- [ ] Confirm the per-rank cost is really a flat **20** in S2 (Tier-3 only) and
      whether the 50% discount halves it to 10.
- [ ] Confirm **Bountiful Delve / gilded stash** crest payouts once Bountifuls appear
      (Aug 18) — the S1 numbers (~35 Hero, gilded stash Hero→Myth at Delver's Journey
      rank 4) are S1 measurements and should not be assumed to carry.
- [ ] Does a keyless T11 standard chest pay crests **every run** or once/day? @verify-ingame
      (open since S1 — still unanswered, still the question that decides whether
      keyless delves are an uncapped Champion engine.)

---
title: The Catalyst (Midnight Season 2)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 Content Update Notes, ITEMS/THE CATALYST (Tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214   # currency 3465 Venomblight Manaflux (Tier 1)
  - https://wago.tools/db2/ItemSparse?build=12.1.0.69214      # item 270909 Slumbering Coil Curio (Tier 1)
  - https://wago.tools/db2/Achievement?build=12.1.0.69214     # 62871 Catalyst Unbound, 62872 Serpent Scion (Tier 1)
  - https://www.wowhead.com/ptr/item=270909/slumbering-coil-curio   # Tier 3, PTR — curio drop source only, unconfirmed
  - https://www.icy-veins.com/wow/catalyst-guide
  - https://www.icy-veins.com/wow/news/your-catalyst-gear-keeps-its-stats-and-cantrips-in-wow-midnight-season-2/
  - https://www.wowhead.com/guide/midnight/matrix-catalyst-crafting-tier-set
confidence: high
---

# The Catalyst (Midnight Season 2)

Console in **Silvermoon City**; converts eligible gear into class tier-set
pieces at the same ilvl. As of **12.1** two other vendors sit **next to it**:
**Kirana** (class sets for Slumbering Coil Curios) and **Orin Straylight**
(Nebulous Voidcores) — both relocated here in this patch.

> ⚠ **Pre-season week (Aug 11–17).** Season 2 opens **2026-08-18**. The
> stat-inheritance change below is **live now**; the Season 2 charge currency
> accrues **from Season 2**, not from patch day.

## What 12.1 changed

- **Converted class-set armor now inherits the source item's secondary AND
  tertiary stats, plus certain special cantrip effects.** Previously secondaries
  were fixed per tier piece. This is the headline change: you can now farm a
  piece with the stats you want in a tier slot and catalyze it without losing
  them. (Tier-1 note; the in-game currency tooltip repeats it.)
- **Kirana relocated** from near the **March on Quel'danas** raid entrance to
  **next to the Catalyst in Silvermoon**, and now also stocks **Midnight
  Season 2 class set armor** for **Slumbering Coil Curios**.
- **Orin Straylight relocated** near the Catalyst too (Nebulous Voidcores — see
  `great-vault.md`).

## Charges

Season 2's charge currency is **Venomblight Manaflux** (currency **3465**);
Season 1's was Dawnlight Manaflux (3378).

- 1 charge at season start, then **+1 every two weeks** (game data: recharge
  1 per 14 days).
- +1 bonus from the season achievement **Midnight Season 2: Serpent Scion**
  (1600 rated PvP / 2000 M+ rating / Ula'tek killed on Heroic or Mythic). Its
  reward is an item called **Crystallized Venomblight Manaflux** (`Achievement`
  DB2 62872) — that is the *achievement's item reward*, **not** a second
  currency. The currency is plain **Venomblight Manaflux** (3465); if a guide
  calls the currency "Crystallized", it has conflated the two.
- After you earn **Midnight Season 2: Catalyst Unbound** (`Achievement` 62871 —
  *"Unlocked your class set bonuses during Midnight Season 2"*; the reward line
  reads *"Venomblight Manaflux can drop from additional sources"*), charges also
  drop from **Mythic Keystone dungeons, Season 2 raid bosses, Bountiful Delves,
  and rated Arenas/BGs**. ⚠ The achievement text says "class set bonuses"
  without naming a threshold — assuming it means specifically the **4pc** is an
  inference, not a stated fact. @verify-ingame
- **Cap: 8 charges** per character (game data `MaxQty` = 8). **No catch-up**
  mechanic.
- ⚠ Leftover **Season 1** Dawnlight Manaflux: the notes do not say whether it
  carries, converts, or is spent-or-lost, and Bountiful Delves are not running in
  the pre-season week anyway. Do not plan around banked S1 charges.
  @verify-ingame

## What converts

- PvE gear **Veteran track or higher**; PvP gear (Honor/Conquest/War Mode).
- **Crafted gear CANNOT be catalyzed** — never spark-craft tier slots
  (head/shoulders/chest/hands/legs) expecting to convert.
- Only head/shoulder/chest/hands/legs results count for set bonuses;
  other slots convert for appearance only. Old-season gear converts free
  (transmog only).
- Output keeps ilvl, upgrade track, sockets, **secondary stats, tertiary stats
  and cantrip effects** (12.1 — see above).

## Kirana and Slumbering Coil Curios (the no-charge route)

**Slumbering Coil Curio** (item **270909**) is the token Kirana takes for
Season 2 class-set armor. Two things are Tier-1: the patch note (*"expanded her
stock to include Midnight Season 2 class set armor in exchange for Slumbering
Coil Curios"*) and the item's own tooltip — *"Find Kirana near the Catalyst in
Silvermoon to trade this for powerful class set armor."* (wago `ItemSparse`
@ 12.1.0.69214). She also still sells **Midnight Season 1** class sets.

⚠ **Everything past that is unconfirmed** — the only source is pre-release
datamining of a raid that has not opened (Tier 3, **confidence: low**):

- **Where curios drop.** Wowhead's PTR item page attributes them to **Ula'tek**,
  the raid's final boss. The 12.1 notes name no source at all. If Ula'tek really
  is the only source, then the earliest an **LFR-difficulty** curio can exist is
  the **week of Sep 8**, when LFR Wing 4 "The Tomb of Ula'tek" unlocks — *not*
  raid open on Aug 18.
- **Whether it is an omni-token** (redeemable for any slot / any piece) and
  **how many it costs per piece** are both unverified.
- **Per-difficulty item levels are not published.** Do not back-derive them from
  the Mistcrest upgrade bands (crest bands are not loot steps — Sporefall's S1
  table was 259/272/285/298 while S1 bands started at 237/250/263/276), and do
  not infer them from Sporefall at all. `raids/venomous-abyss.md` §Loot records
  the same hole; keep the two files in step.
  @verify-ingame

What *is* safe to plan on: redeeming a curio does **not** consume a Catalyst
charge. So for a tier slot where you hold no good non-tier piece, a curio is the
better route — but it gives the **stock tier stats**, whereas the Catalyst now
gives you the stats of whatever item you fed it. No curios exist during the
pre-season week; the raid opens **2026-08-18**.

## Strategy

- The stat-inheritance change flips the old advice: **catalyze the piece with
  the best stats/tertiaries, not merely the highest ilvl**, when the two differ
  by a step or less. Speed/Leech/Avoidance and cantrips now survive conversion.
- Otherwise still catalyze **highest-ilvl, highest-track** non-tier pieces in
  tier slots; upgrade with crests *before* catalyzing only if you won't replace
  soon (track carries over, so upgrading after also works).
- Once curios exist, spend them on the slots you can't cover and save charges
  for slots where you're holding a great-stat non-tier item. ⚠ Their drop
  source, exchange rate and ilvl are all unverified (above) — don't build a
  gearing plan that assumes a specific number of them.
- Charges accrue slowly and cap at 8 — banking a few is fine, but sitting
  at cap wastes accrual.

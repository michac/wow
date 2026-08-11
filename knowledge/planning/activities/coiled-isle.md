---
id: coiled-isle
name: Coiled Isle zone content (Curse Surges, Vaults of Atal'Utek, rares)
goal: [gearing, collectibles]
venue: world
group: flex
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [power, currency, collectible], detail: "Curse Surges → Corrosive Souls + other loot (Zul'jarra R4: first Curse Surge boss gets a daily Corrosive Soul chance; R8: Curse Surge bosses get a daily chance at Warbound Veteran equipment); Vaults of Atal'Utek patrols/strikes/incursions → Corrosive Coins + Corrosive Souls (the Altar of Corrosion zone power tree) + Zul'jarra's Forces renown; Venom-Soaked Satchels throughout the isle (gear-upgrade materials, gold); rares/treasures for gear, pets and mounts" }
# yields: deliberately absent. The isle's currencies (Voidlight Marl, Corrosive
# Coins, Corrosive Souls, Artisan Moxies, Adventurer Mistcrest) have no canonical
# key in tools/wowkb/rewards.py yet, and Coffer Key Shards do not drop here until
# 2026-08-18. Add the keys there first, then declare amounts — don't fabricate
# them (_facets.md, "Amounts … don't fabricate").
time_blocks: 3
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/news/24293963/     # Coiled Isle / Vaults of Atal'Utek preview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281         # 12.1 Content Update Notes (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350    # S1 ending / S2 pre-season state (Tier 1)
  - https://www.icy-veins.com/wow/the-coiled-isle-guide     # Tier 3 — cadences, unlock chain
  - https://www.icy-veins.com/wow/vaults-of-atalutek-guide  # Tier 3 — patrol/strike/incursion tiers
  - https://www.wowhead.com/guide/midnight/vaults-of-atalutek-patch-12-1-zone-activities-rewards-player-power  # Tier 4 — corroboration only
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214  # Mistcrest names + upgrade bands, currency IDs 3437-3441 (Tier 1 game data)
  - knowledge/_meta/changelog-12.1.md
confidence: medium   # structure is Tier-1; cadences/counts are day-one Tier-3 and unverified in game
---
The **Coiled Isle** — the fog-shrouded island off the east coast of Zul'Aman, added by
**12.1 "Curse of Ula'tek" (live 2026-08-11)**. This row is the **zone farm**: the standing,
no-reset outdoor loop you can drop into with any amount of time. Unlocked off the 12.1
campaign (*"Hagar's Invitation"* in Silvermoon; the isle opens fully after *"What Lies
Beyond the Fog"*) — the campaign itself is `midnight-campaign`, this is what's left when
the story is done.

⚠ **Pre-season week (Aug 11–17):** Blizzard names **Curse Surges and the Vaults of
Atal'Utek explicitly as available during pre-season**, so this row is rankable **today**.
What is *not* live yet: **Coffer Keys/shards do not begin dropping until the week of
Aug 18**, and Prey's Nightmare hunts on the isle (`prey-weekly`) and *"The Curse of the
Isle"* toggle also wait for Aug 18. Consequently **two of Tier 1's listed Corrosive Soul
sources are not earnable yet** — **Ral'Kala** (Nightmare-only summon) and **Bountiful
Delves** (`delve-bountiful` is `status: invalidated` this week for exactly that reason).
Everything below that is not dated **Aug 18** is live today.

⚠ **12.1's global combat retune applies here like everywhere else** — player health **and**
creature damage are up **25%** at max level (with health consumables rescaled and some
DPS/Tank heal/absorb spells retuned), major DPS cooldowns are shorter with steady-state
damage raised on several specs, and DR categories now reset after **20s** (was 16). So any
pre-2026-08-11 read on how survivable this zone's rares and elites are solo is stale.

**Three loops, all repeatable:**

- **Curse Surges** — waves of corruption at **five rotating locations** *(spawn cadence
  reported as roughly hourly — **Tier 3, unverified in game**)*; each is a
  clear-the-objectives public event capped by a **rare elite**. Tier-1 payout is
  **Corrosive Souls and other loot**, and killing the rare elite **unlocks Venom Fishing
  (a "Cursed Fishing" pool) at that location**. This is the cheapest per-minute thing on the isle — and the only Curse
  Surge *gear* source is renown-gated: **Zul'jarra's Forces Renown 4** gives your **first
  Curse Surge boss of the day a chance at a Corrosive Soul**, and **Renown 8** gives Curse
  Surge bosses a **daily chance at a piece of Warbound Veteran equipment** (see
  `zuljarra-renown` — that row is what unlocks this row's ceiling).
- **Vaults of Atal'Utek** — the ancient Amani complex hidden beneath the isle, opened by
  *"Into the Vaults of Atal'Utek"* from **Warleader Abdumati**. Three tiers that feed each
  other: **Temple Patrols** → **Temple Strikes** → **Temple Incursions**, ending on an
  **Ancient Foe** boss fight. *(The tier cadences and group sizes below are **Tier 3,
  unverified in game**: patrols a new set every ~10 min and soloable; strikes ~3–5 players,
  unlocked by a number of patrols; incursions after two strikes or hourly, whichever comes
  first, ~15–20 players.)* Tier-1 names the payout: **Corrosive Souls**, **Trovehunter's
  Bounty**, **Venom-Cursed Fragments**, **Corrosive Coins**, and **Zul'jarra's Forces
  renown**. Amani Windcallers ferry you around and briefly hide you from hostile creatures.
- **Rares, treasures and lore objects** — *(all counts and rep values here are **Tier 3,
  unverified in game**)* 12 rares (*Coiled to Strike*), ~22 treasures, ~10 lore objects;
  direct gear, pets, and renown (≈50 rep per rare/treasure/quest, ≈250 per lore object).
  From **Aug 18** rares also feed **Coffer Key Shards** — Blizzard retuned shard
  acquisition **weighted toward Coiled Isle content** but calls the tuning **ongoing and a
  work in progress**, so treat any specific shard number as volatile.

**Venom-Soaked Satchels** are earned **throughout the isle** (not as a fixed Curse Surge
drop) and contain **materials for upgrading gear, gold, and more**.

**Crests.** Season 2's upgrade currency is the **Mistcrest** ladder, and the entry tier is
the **Adventurer Mistcrest** (upgrades ilvl **269 → 282**). All five names and bands are
Tier-1 game data — `CurrencyTypes` DB2 @ `12.1.0.69214`, currency IDs **3437–3441** — so the
name is asserted, not reported. Tier 1 names Adventurer Mistcrests for **Val/Naigtal world
quests, rares and elites** and for **Void Assaults** — it does **not** state a payout for
any Coiled Isle content, so nothing is declared here, neither a source nor an amount.

**Altar of Corrosion — the zone power tree.** The Altar sits in the **Amani Foothold inside
the Vaults of Atal'Utek**; you spend **Corrosive Coins** *there* on a zone-scoped talent
tree of exploration / combat / mobility / reward perks, including **cutting the potency of
the isle's venom**, and you can re-spec at it freely. Early Altar investment is genuinely
instrumental: the tree's top row auto-unlocks **Corrosive Spirit I–IV** at 5/10/15/20 more
points spent, worth **+25% / +50% / +75% / +100% Corrosive Coin income**, so it pays to
bank the tree before farming the rest of the zone hard.

**Corrosive Powers** are the second, separate half. They come from the **"Corrosive Gifts:
Corrosive Power"** questline (you need the **Codex of the Soul Coilers** item to start it),
which unlocks the **Corrosive Codex** at the Altar. **Corrosive Souls** — earned this week
from **Vaults of Atal'Utek activities and bosses**, **Curse Surges**, the **Nymrissa
Wavecaller** lair and **Prey hunts**, and **from Aug 18** additionally from the **Ral'Kala
Prey boss** (summoned only in Nightmare Mode) and **Bountiful Delves** (neither is live in
the pre-season week) — are spent at the Altar **via the Codex** to unlock powers, in any
order. ⚠ **Two powers active at once only after you have unlocked eight of them**; before
that it is one. The powers work **in Midnight
outdoor zones and inside Delves**, and a **projection of the Altar appears in Midnight
Delves** once the system is unlocked, so you can re-combine at the start of a Delve.

⚠ **Er'inye is not the talent vendor.** The **Skull of Er'inye** is a *cosmetics* vendor —
mounts, pets, ensembles, arsenals, profession recipes and housing decor for **Corrosive
Coins** — and is also the **conversion door**: hand it Corrosive Souls to get Corrosive
Coins back. (Distinct again from **Spirit of Corrosion I/II**, a Zul'jarra Renown *reward
item* — **I at Renown 8** — that you bring to Er'inye for use at the Altar. It is a
one-off grant, not the feeding currency.)

**Tokka's crew (fishing).** The tortollan sea captain **Tokka**, at **Tokka's Landing**,
teaches **Cursed Fishing** — the Tier-1 preview uses **"Venom Fishing"** and **"Cursed
Fishing"** for the same system, and the rest of the KB (`changelog-12.1.md`,
`systems/coiled-isle.md`, `abyss-anglers`) files it under **Venom Fishing** — and carries a
**local story with its own five-rank friendship
faction** — **Stranger → Doomed Sailor → Cursed Angler → Venom Trawler → Bloodsworn Crew**
— leveled by his dailies, fishing up artifacts, and killing spirits from his past. Each
Curse Surge you finish opens another cursed pool to fish. **Second Mate Sluggs** at Tokka's
Folly sells the rewards, for Coins / Voidlight Marl / **Coiled Filament** / Artisan Moxie
and/or Tokka's Crew renown. Collector payoff, not gearing — see `abyss-anglers` for the
other fishing row.

Note the **Anglin' Score is not an isle track** — 12.1 adds it to **fishing across all of
Midnight**, each fish worth up to 100 points, with **2,500 Midnight Anglin' Score** awarding
*The Briny Best* and the **"Briny"** title. Isle fishing feeds it, but so does every other
Midnight zone, so don't rank isle time for it specifically.

**Overlaps — don't double-count.** Renown itself (20 ranks, quartermaster **Jan'sari the
Watchful** at Tokka's Landing, Voidlight Marl + Artisan Moxies) is its own row,
`zuljarra-renown`; this row is the *content that earns it*. The isle's lair is
`lair-tidebound-grotto` (weekly lockout, World difficulty only until Aug 18); the isle's
Prey hunts are `prey-weekly`; the story chapters are `midnight-campaign`.

**Vault note (unconfirmed):** Val/Naigtal-style outdoor content fills the **World row** of
the Great Vault, and the pre-season rules cap that row at **Champion 3/6** for the first
Season 2 vault (**Hero 1/6** thereafter). Whether **Curse Surges / Vault-of-Atal'Utek
events** credit that row — and at what count — is **not stated in any Tier-1 source**, so
no `breakpoint:` is declared here yet; if they do, the World row is the **same shared
counter** `delve-bountiful` and `val-naigtal` advance, never a second one.
@verify-ingame: does completing a Curse Surge or a Temple Incursion advance the World row
of the Great Vault, and at what threshold?
@verify-ingame: Coiled Isle Tier-3 cadences and counts — Curse Surge spawn interval, Temple
Patrol/Strike/Incursion timings and group sizes, and the 12 rares / ~22 treasures / ~10
lore objects and their rep values. None of these appear in any Tier-1 source.

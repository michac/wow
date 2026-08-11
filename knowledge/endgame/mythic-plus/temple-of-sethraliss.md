---
title: Temple of Sethraliss — Midnight S2 M+ dungeon (STUB)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24294369   # "Midnight Season 2" overview — S2 dungeon pool (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes — returning dungeons list (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season schedule (tier 1)
  - Blizzard journal-instance/1030 + journal-encounter/2142 (Adderis and Aspix) + 2143 (Merektha) + 2144 (Galvazzt) + 2145 (Avatar of Sethraliss), namespace static-12.1.0 (tier 1 game data — boss roster + ability names)
  - https://www.wowhead.com/news/first-look-at-new-temple-of-sethraliss-in-mythic-season-2-382156  # (tier 4, PTR-era first look — NOT yet distilled, see TODO)
confidence: low
---

# Temple of Sethraliss — Midnight Season 2 Mythic+

> ⚠️ **STUB, written on patch day (2026-08-11).** Everything here is either Tier-1
> patch notes or Tier-1 journal game data. **There is no route, no trash table, no
> affix guidance and no loot table yet** — the Tier-3 guide sites (Method, Icy
> Veins) have not published Midnight-tuned versions, and pre-12.1 guides are
> explicitly suspect because Blizzard reworked this dungeon (below). Do not answer
> route or strategy questions from this file; see `## TODO`.

Battle for Azeroth dungeon in Vol'dun, **returning to the Mythic+ pool in Midnight
Season 2**. Four bosses. Blizzard journal instance **1030**, expansion *Battle for
Azeroth*, and the 12.1 journal lists **Mythic+ Dungeons** among its modes —
i.e. the M+ flag is live in game data, not just in the blog.

Journal flavor: Sethraliss, a snake loa, sacrificed herself to stop Mythrax. Her
followers built the temple around her remains to await her rebirth; a dark force
now stirs inside it and seeks to twist her power.

## Availability — this is dated

| | **Week of 2026-08-11 (live now — pre-season)** | **Week of 2026-08-18 (Season 2 opens)** |
|---|---|---|
| Difficulties | Heroic and **Mythic 0** only | Mythic+ opens |
| Mythic 0 lockout | **weekly, this week only** | back to **daily** |
| M0 reward | **Champion 1/6 (292)** | Champion 1/6 (292) |
| Keystones | **do not drop** | Mythic Keystones drop |

Pool-wide detail lives in [`season-2-overview.md`](season-2-overview.md);
`keystones.md` and `loot.md` are the files of record for lockouts and rewards.

**No Follower Dungeon version.** Follower Dungeons only cover Dragonflight / War
Within / Midnight content, so a BfA dungeon cannot be practiced that way.

## The 12.1 rework — what is actually known

Blizzard's own wording is all we have from Tier 1. The Content Update Notes list
Temple of Sethraliss under **"Returning dungeons with design and quality of life
updates"** (alongside Kings' Rest and Ruby Life Pools) and **do not enumerate a
single change**. Tier-3/4 PTR coverage through late July reports that this
dungeon took *the majority* of the Season 2 dungeon tuning across several PTR
passes, including repeated changes to the flow of the final boss encounter — but
those are PTR-era reports, unverified against the shipped build, and are not
recorded here as facts.

**Practical consequence: treat every pre-12.1 Temple of Sethraliss route guide,
timer and trash count as wrong until re-verified.** That includes anything
written for BfA Season 1–4 and for Dragonflight's Season 3 reappearance.

## Bosses (Tier-1 journal roster)

Names and ability names below come from the Blizzard journal at the **12.1**
namespace, so they reflect the shipped build. **The journal does not tell you the
route, the timer, the pull order, or how the abilities interact with affixes** —
those are deliberately absent below rather than guessed. Archetype/consequence
tagging against [`mechanic-archetypes.md`](../../systems/mechanic-archetypes.md),
which every other dungeon file in this directory carries, is **not yet done here**.

### 1. Adderis and Aspix <!-- enc:2142 -->

Sethrak duo — Adderis the melee warrior, Aspix the caster. Journal core loop:
**Storm Blessed** alternates between the two and grants **damage immunity**, so
the pair must be killed in the right order/window; both **Frenzy** at low health.

- Adderis: **Thunder and Lightning** (two-part; first part splits damage evenly
  between players hit), **Overload** (rapid extra Nature damage on melee swings —
  tank).
- Aspix: **Tempest Winds** (damages players on creation), **Gale Force**, **Gust**.

### 2. Merektha <!-- enc:2143 -->

Snake boss with adds and a burrow phase.

- **Hatch** — releases snakes that join the fight: **Toxic Viper** (interruptible
  **Poison Spit**) and **Storm Serpent** (**Storm Catalyst**, leaving **Lingering
  Storm** underneath it).
- **A Knot of Snakes** — stuns an ally until destroyed or incapacitated, and
  damages them while active.
- **Burrow** → **Burrowquake**, party-wide damage while she is burrowed.
- **Lightning Bite** — heavy hit on her current target (tank).
- **Thunder Spit** (leaves **Lingering Storm**), **Serpentstorm** (significant
  damage to all players) with **Storm Strikes**.

### 3. Galvazzt <!-- enc:2144 -->

A soak/positional puzzle. Galvazzt accumulates energy from **Lightning Spires**
that form at targeted locations (damaging and knocking away anyone struck).
**Players standing between Galvazzt and a spire become Galvanized**, which blocks
the energy flow and prevents **Consume Charge** / **Capacitance**. Galvanized
inflicts significant damage and **greatly increases Physical damage taken** — so
soaking is a rotate-and-defensive job, not a tank job. Also: **Induction** /
**Induction Field**.

### 4. Avatar of Sethraliss <!-- enc:2145 -->

Not a damage race — a **healing/escort encounter**: you win when the Avatar
reaches **full health**. ⚠️ **This is the encounter Tier-3/4 PTR reports say had
its flow changed more than once during 12.1 testing** — the structure below is
the shipped journal's, but the moment-to-moment execution is unverified.

- **Stage One: Defiler's Corruption** — Jakra'zet's allies arrive to stop healing
  energy reaching the Avatar. **Essence Defilers** channel **Defiling Taint**
  (thwarts healing); killing them all cleanses it. **Corrupted Guardians** carry
  **Corrupted Lifeforce** which can be **cleansed/purified** so the Avatar consumes
  it (**Consume Lifeforce**; failure states **Corruption** / **Corruption Burst**);
  Guardians hit the tank hard with **Tainted Strike** and **Vile Charge**.
  **Twisted Hexxer** adds bring **Flame Shock** and **Latent Hex** → **Hex Muck**.
- **Stage Two: Tormentor's Fixation** — **Faithless Tormentors** disrupt the
  restoration with **Shadowlash** (also thwarts healing).
- Avatar's own: **Siphon the Weak**, **Agony of Sethraliss**.

## DPS notes (you are DPS)

Only what the Tier-1 journal supports:

- **Adderis and Aspix:** watch **Storm Blessed** — hitting the immune one is
  wasted damage. Spread/stack for **Thunder and Lightning** is a real call but the
  correct one is unverified for 12.1.
- **Merektha:** interrupt **Toxic Viper**'s Poison Spit; break **A Knot of Snakes**
  off whoever it stuns.
- **Galvazzt:** the **spire soak is a DPS/healer job** and it stacks Physical
  damage taken — plan defensives, don't chain-soak.
- **Avatar of Sethraliss:** add-kill priority is the whole fight (Essence Defilers
  → Corrupted Guardians → Faithless Tormentors), and boss damage is irrelevant.

## TODO

- [ ] **Enumerate the actual 12.1 "design and quality of life updates."** Tier-1
      notes name none. Sources to work: the 12.1 PTR development-notes blue posts
      and Wowhead's dungeon-tuning news series (382156 / 382227 / 382294), then
      confirm in game. Until then this file cannot say what changed.
- [ ] **Confirm the Mythic+ timer.** SEO-tier sources quote **33 minutes**; that
      is **not** corroborated by any Tier-1/2 source and is deliberately not
      stated as fact above. Read it off the keystone in game after 2026-08-18.
- [ ] **Write the route + trash table** once Method / Icy Veins publish
      Midnight-tuned guides (they had not on patch day), following the sibling
      format in `skyreach.md` — mob · ability · see→do · archetype · tier · role.
- [ ] **Tag every boss ability against
      [`mechanic-archetypes.md`](../../systems/mechanic-archetypes.md)** and add
      the consequence tiers (🔴/🟠/🔵/⚪) the other dungeon files use. This also
      feeds `projects/mplus_memory/`.
- [ ] **Record the Warcraft Logs encounter IDs** for the S2 zone once logs exist
      (`wowkb.wcl`), and the loot table from live drops.
- [ ] Confirm whether the **journal ability list changed** vs the BfA/DF version —
      a diff of journal-encounter 2142–2145 against a pre-12.1 capture would show
      any removed or renamed ability without waiting for guide sites.

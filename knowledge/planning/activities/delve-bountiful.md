---
id: delve-bountiful
name: 6 keyed Bountiful delves
goal: [gearing]
venue: delve
group: solo
cadence: weekly
time: standing
scope: character
status: invalidated       # ⚠ pre-season week ONLY — Bountiful Delves do not appear until 2026-08-18. RE-ACTIVATE then, but re-source `yields` FIRST (see the yields comment below + prose).
gate: { type: weekly_quest, quest: delve_weekly_cache }
breakpoint: { type: vault, track: world, thresholds: [2, 4, 8] }
reward: { type: [power], detail: "crests + catalyst + keyed coffer; fills the world Vault column. ⚠ unavailable during the 2026-08-11 pre-season week; the Season-2 delve tier → track/ilvl mapping is not yet published" }
# yields: DELIBERATELY ABSENT — do not re-add Season 1 numbers.
#   Bountiful Delves cannot be run in the 12.1 pre-season week, so the honest declared
#   yield is nothing (_facets.md: "must not carry live yields for content nobody can
#   enter yet"). The figures that used to sit here (hero_crest 35 / myth_crest 5;
#   champion coffer landing at ilvl 250) were Season 1 / Dawncrest-era and are dead:
#   the whole gear ladder shifted +45 into Season 2 and the crests are Mistcrests
#   (Tier-1 CurrencyTypes DB2 @ 12.1.0.69214 — endgame/dawncrests.md, _meta/moving-values.md).
#   ⚠ RE-ACTIVATION GATE (2026-08-18): re-declare yields.currencies + yields.slots from a
#   sourced Season-2 delve reward table BEFORE flipping status back to active. Flipping
#   status alone would have shipped the S1 numbers straight into the ranker.
time_blocks: 1
enjoyment: 1.4
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/candidates.json
  - knowledge/endgame/delves/overview.md
  - https://us.forums.blizzard.com/en/wow/posts/29833350   # S1 ending / S2 information — the pre-season availability statement (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281        # 12.1 Curse of Ula'tek content update notes (Tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214 # S2 Mistcrests + upgrade bands, currency IDs 3437–3441 (Tier 1 game data)
  - https://www.icy-veins.com/wow/midnight-delve-rewards-guide      # Tier 3 — corroboration only, no number in this file comes from it
  - https://conquestcapped.com/guides/wow/midnight-delves-rewards/  # Tier 4 — S1-era reward table; never a source for an S2 number
confidence: medium
---
The core solo loop — key 6 Bountiful delves for crests, catalyst charges, and the coffer.

## ⛔ NOT RUNNABLE THIS WEEK (12.1 pre-season, week of 2026-08-11)

**Bountiful Delves do not appear during the pre-season week, and Coffer Keys do not
drop** (Tier 1: "Season 1 Ending and Season 2 Information"). There is no Bountiful
loop, no Bountiful Coffer, and no key economy to spend into until Season 2 opens.
That is why `status: invalidated` — the whole activity is unavailable, so it must not
be rankable today.

What Delves **do** offer during the pre-season week:

- Difficulties **Tiers 1–11**, plus the **"?" Nemesis** difficulty.
- Maximum reward from Delves is **Adventurer 3/6 gear and Season 2 Veteran crests** —
  a hard cap, well below what this activity is written for.
- Three new delves are in: **The Ring of Glory**, **Gnarldor Isle**, and the
  **Venomfall Deeps** Nemesis Delve. Existing Midnight delves get new snake/venom
  enemy variants.

**Re-activate with maintenance the week of 2026-08-18** — flipping `status` back to
`active` **only after** `yields` is re-declared from a Season-2 source — when Bountiful Delves appear,
**Coffer Keys begin dropping**, and the **"??" Nemesis** difficulty unlocks (clearing
"??" in that first season week earns the Fabled *Let Me Solo Him: Azta'rec*).

## What still holds, and what needs re-sourcing on Aug 18

**Structure (no delve-specific change in 12.1):** running these **also fills the
world/delve column of the single Great Vault** (slots at **2/4/8**), so vault progress
is a `breakpoint` here rather than its own row (merged the old `delve-world-vault`).
Note that delves are still touched by 12.1's **global** combat retune — max-level
player health and creature damage both **+25%** (health consumables rescaled, several
DPS/Tank healing and absorb spells re-tuned), major DPS cooldowns shortened with
steady-state damage raised for several specs, and diminishing-return categories now
reset after **20s** (was 16s). Solo delve pacing and defensive planning change even
though no delve mechanic did.

**⚠ The old front-matter numbers were Season 1 figures and have been removed, not
re-labelled.** The 2026-07-09 track correction (keyed coffer = Champion 250 (2/6) at
T8–11, *not* Hero; Hero 259 only from the Great Vault delve slot, a Delver's Bounty
map, or Delver's Journey rank 9) described the **Season 1 / Dawncrest** reward table.

What **is** Tier-1 settled for Season 2 (`CurrencyTypes` DB2 @ `12.1.0.69214`, currency
IDs 3437–3441 — the floor no editorial source may override): the crests are
**Mistcrests**, all five tiers named, and the whole upgrade ladder shifts a clean
**+45** — Adventurer **269–282** · Veteran **282–295** · Champion **295–308** ·
Hero **308–321** · Myth **321–334** (S1: 224–237 / 237–250 / 250–263 / 263–276 /
276–289). So Season 2 gear runs **269 → 334**, and an S1 figure like the 250 coffer is
below the *bottom* of the S2 ladder — not stale-ish, impossible.

What is **not** yet published is the piece this activity actually needs: the Season-2
**delve tier → track/landing-ilvl** mapping (which tier hands which track, and the
per-run crest amounts). Re-source that on Aug 18 from game data or the season's Tier-1
notes; do not fill it from the +45 arithmetic (landing ilvls are a separate ladder from
the crest bands — a Hero drop *lands* at 305 while the Hero Mistcrest band starts at
308), and do not fill it from SEO reward guides.

**Coffer Key Shards were retuned** in 12.1 across multiple sources, weighted toward
Coiled Isle content — and Blizzard explicitly calls the tuning **ongoing and a work in
progress**. Treat any specific shard-per-source number as volatile and do not encode
one here.

**Gate TODO (roadmap):** the weekly cap sits on the Restored Coffer Key economy, not
the shard currency (dump shows shards `weeklyMax=0`); resolve the key signal in-game.
Cannot be resolved this week — keys do not drop at all until Aug 18. @verify-ingame

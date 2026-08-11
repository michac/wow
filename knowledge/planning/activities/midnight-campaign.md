---
id: midnight-campaign
name: Midnight story campaign (leveling spine + the 12.1 Curse of Ula'tek chapters)
goal: [story, gearing]
venue: quest
group: solo
cadence: one-time
time: standing
scope: character
status: active
# ⚠ Gate changed in the 12.1 sweep: was `campaign_incomplete`, which plan.py resolves
# as "level >= 90 ⇒ done" and therefore HIDES the row on every max-level character —
# exactly the characters the 12.1 chapters are for (they require level 90). During a
# patch window a false "still todo" is far cheaper than making the season's
# prerequisite invisible, so this is `manual`: the planner ranks it with a "(?)".
# The real fix is a campaign-complete / quest-ID flag in the PlannerState dump —
# kb-inbox material, see the "Gate + scoring note" section below.
gate: { type: manual }
reward: { type: [power, story], detail: "leveling spine: campaign gear (~ilvl 240 catch-up, 12.0.7-era figure) + unlocks WQs, renown, Adventure Mode, Hero-tree 4th lane + Apex slot. 12.1 chapters: the ONLY key to the Coiled Isle — zone entry, its world quests, the Vaults of Atal'Utek hub, the Altar of Corrosion tree, and Zul'jarra's Forces renown" }
time_blocks: 4
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281              # 12.1 "Curse of Ula'tek" Content Update Notes (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963     # Follow the Snakes to the Coiled Isle (Tier 1)
  - https://www.icy-veins.com/wow/the-coiled-isle-guide          # Tier 3 — unlock chain, warband access
  - https://www.icy-veins.com/wow/news/players-can-already-take-the-first-step-toward-wow-patch-12-1s-raid-zone/  # Tier 3 — chapter 1, pre-patch
  - https://conquestcapped.com/guides/wow/wow-12-1-campaign-guide/  # Tier 4 — chapter names/counts, corroboration only
  - https://www.wowhead.com/news/midnight-patch-12-0-7-guide-compendium-every-guide-you-ll-need-for-launch-381872
  - knowledge/_meta/changelog-12.1.md
  - "yt:cpbQXd04ehI"
  - "yt:6OkVWEdttZ0"
confidence: medium
---
The Midnight story campaign. **A gate for almost everything else** — and as of
**12.1 "Curse of Ula'tek" (live 2026-08-11)** this row carries **two** arcs with very
different audiences:

1. **The leveling spine** — the original Midnight campaign, run on the way to 90.
2. **The 12.1 chapters** — a **max-level** arc that is the *only* door to the Coiled Isle
   and every system on it.

`cadence: one-time` per character; `goal:story` is the terminal want, `gearing` the
byproduct.

## 1. The leveling spine (unchanged in 12.1)

Completing it unlocks World Quests, the renown tracks, Adventure Mode, and the
**Hero-tree fourth lane + Apex Talent slot**, and hands out catch-up gear.
⚠ The **~ilvl 240** figure was measured in the **12.0.7** era and was *not* re-verified
for 12.1 — Season 2 shifted the whole gear ladder **+45** (269→334, `_meta/moving-values.md`),
and whether the leveling campaign's catch-up gear moved with it is unstated in any Tier-1
source. Treat 240 as the last known value, not a 12.1 claim.
@verify-ingame: loot a leveling-campaign gear reward on a fresh character in 12.1 and read
its ilvl.

**Cross-character star case:** on a leveling/fresh alt this outranks any capped weekly —
it's the prerequisite that opens the whole endgame loop. `scope:character`, scored per
active row.

## 2. The 12.1 "Curse of Ula'tek" chapters — the patch-week prerequisite

This is the new work, and it is **level 90 only**. Nothing on the Coiled Isle is reachable
without it: not the zone, not its world quests, not the Vaults of Atal'Utek loop, not the
Altar of Corrosion tree. Tier 1 frames it as *"Continue the story of Zul'jan as the fog
lifts from the island off the east coast of Zul'Aman"* — you join **Zul'jarra** as she
pursues her brother, and dig into the long-buried history of the isle.

**Where it starts:** the quest **"Hagar's Invitation"**, from **Orweyna** at the Sanctum
of Light in the centre of **Silvermoon City**. That first chapter, **"Legacy of the
Amani"**, went live in the **pre-patch week (week of 2026-08-04)** — it is the one piece of
12.1 you could have banked before patch day. It runs ~45–60 min, routes through **Maisara
Caverns** (Follower difficulty is enough; loot Malacrass's Notes off the second boss,
Vordaza), and pays the **Dusk Grimlynx** mount and the **Akiki** pet. (Tier 3.)

**Chapters** (names from the "Curse of Ula'tek" campaign achievement criteria; quest counts
are Tier 4 and uncorroborated):

| # | Chapter | ~Quests | What it opens |
|---|---|---|---|
| 1 | **Legacy of the Amani** | — | the arc; live since the pre-patch week |
| 2 | **An Island of Fangs** | ~17 | **entry to the Coiled Isle** — via *"What Lies Beyond the Fog"* |
| 3 | **Ghosts of the Past** | ~6 | story |
| 4 | **Original Sin** | ~10 | story |
| 5 | **The Battle for Atal'Utek** | ~8 | the isle's **repeatable systems** (below) |

⚠ Tier-3 and Tier-4 guides disagree on whether "Legacy of the Amani" counts as chapter 1
or as a prologue in front of a four-chapter campaign — hence 5 rows here against
conquestcapped's "4 chapters, 41 quests". The **names** are consistent across sources; the
**numbering** is not. @verify-ingame: open the Campaign tab of the quest log on the Coiled
Isle and read the real chapter list + count.

**Three system unlocks sit in the final chapter** (Tier 4, verify):

- *"Nature of Her Wounds"* — heal Zul'jarra with the Fang of Ula'tek → **Coiled Isle world
  quests**.
- *"Into the Vaults of Atal'Utek"* (from Warleader Abdumati) → the **Vaults hub** and the
  **Corrosive Coin** economy.
- *"The Altar of Corrosion"* → the **zone talent tree**.
- *"The Vaults of Atal'Utek: Altar of Fangs"* wants a clear of the **Altar of Fangs**
  dungeon — available on Heroic/M0 from patch day, so it is not a blocker this week.

**⚠ You cannot finish the campaign during pre-season week (Aug 11–17).** The final chapter
ends on **"The Venomous Abyss"**, which asks for a raid clear on any difficulty (LFR
counts) — and **the raid does not open until 2026-08-18** (Tier 1). So: everything *up to*
that quest is playable and worth clearing now; the last beat waits a week. Do not rank this
row as completable-in-one-sitting on the assumption the whole arc is available.

**Warband unlock.** Icy Veins reports that once *"What Lies Beyond the Fog"* is done, isle
entry opens for the **entire warband** — i.e. alts get in without re-running chapters 1–2,
even though the chapters themselves (and their rewards) are still per-character. That is a
Tier-3 claim and materially changes alt planning, so verify before leaning on it.
@verify-ingame: log an alt that has never touched the 12.1 campaign and confirm it can
reach the Coiled Isle.

**Travel note:** the **Amani Pass** between Eversong Woods and Zul'Aman **no longer
dismounts** (12.1) — the campaign's overland route got noticeably less annoying.

## 3. Not live yet — do not rank these today

- **Arator / the hunt for Xal'atath.** *"After the start of Season 2"* (so **2026-08-18 at
  the earliest**), Arator returns to deal with the **Voidspire** fallout and the
  **resurgence of the Twilight's Blade**, continuing the hunt for **Xal'atath**. Tier 1 gives
  no chapter names, quest count, or rewards. This is a **separate story arc** from the
  Coiled Isle chapters; when it lands with real detail it likely deserves its own row rather
  than a third arc bolted onto this one.
- **New stories in the Arcantina.** A one-line Tier-1 QUESTS bullet with no further detail —
  scope, length and rewards all unknown. Not enough to rank; recorded so the sweep does not
  lose it.

## Overlaps — don't double-count

This row owns the **story chapters**. The isle's standing farm (Curse Surges, Vaults
patrols/strikes/incursions, rares) is `coiled-isle`; the renown track those clears advance
is `zuljarra-renown` (it also accrues **before landfall**, off the Zul'Aman quests with
**Lady Liadrin**, **Orweyna** and **Zul'jarra** — so the campaign is itself a renown source);
the isle's weekly-lockout boss is `lair-tidebound-grotto`; its hunts are `prey-weekly`.
Ranking this row *and* the zone rows at full value for one Coiled Isle session over-counts
the same hour.

## Gate + scoring note (read before trusting the ranking)

- **Gate.** `campaign_incomplete` resolves in `plan.py` as *"level ≥ 90 ⇒ done"* — a proxy
  chosen because the PlannerState dump carries no campaign-complete flag. That proxy is
  now **backwards**: the 12.1 chapters *require* 90, so the old gate hid this row from
  exactly the characters that need it. Switched to `manual`, which surfaces the row with a
  **"(?)"** flag and leaves the judgement to the reader. **Cost of the change:** the row no
  longer disappears once you finish, on any character. The proper fix is a campaign /
  quest-ID completion field in the addon dump.
- **Urgency is understated.** `time:standing` + `cadence:one-time` inherits **U = 1**, but
  through 2026-08-18 this is a hard prerequisite for four other rows and the season's raid
  quest. No `urgency:` override is set here — deliberately, so nobody inherits a stale
  patch-week thumb on the scale — but read this row above its printed score during the
  pre-season and first S2 week.

**Confidence is `medium` on purpose.** Tier 1 confirms the arc, the Zul'jarra/Zul'jan
story, the Aug-18 raid opening and the Arator/Arcantina teasers. The **chapter names,
counts, quest names and per-quest unlocks are Tier 3/4 day-one guide material** and have
not been corroborated against game data or seen in game.

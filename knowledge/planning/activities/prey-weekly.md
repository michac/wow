---
id: prey-weekly
name: 3 Nightmare Prey hunts
goal: [gearing]
venue: world
group: solo
cadence: weekly
time: standing
scope: character
status: invalidated   # PRE-SEASON ONLY: Nightmare Mode is offline Aug 11–17. FLIP BACK TO `active` ON 2026-08-18.
gate: { type: weekly_quest, quest: prey_weekly }   # ⚠ S1 wiring: 94446 is dormant pre-season and unverified for S2 — the S2 weekly has its own reserved slug `prey_s2_weekly` (ID unknown). RE-WIRE BEFORE FLIPPING TO `active`.
reward: { type: [power], detail: "weekly objective; S2 Nightmare pays Champion-track" }
yields:
  # S2 crest yield is UNMEASURED — no Tier-1 source states an amount, and the S1 figure
  # this row used to carry (20 Hero Dawncrests) was never reconciled with dawncrests.md,
  # so it is dropped rather than renamed to Mistcrests. No `currencies` block until it is
  # read off a live S2 hunt. Absent currencies just means currency_R falls back to
  # reward_base (plan.py) — safe.
  slots:
    - { track: champion, ilvl: 292, chance: 1.0, slots: [all] }   # S2 Nightmare = Champion gear (Tier 1); 292 = S2 Champion 1/6 (dawncrests.md — DB2 + Lairs reward table); exact step unverified
time_blocks: 1.5
enjoyment: 1.1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.forums.blizzard.com/en/wow/posts/29833350   # S1 ending / S2 information — pre-season Prey state (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281        # 12.1 "Curse of Ula'tek" content update notes (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369        # Midnight Season 2 overview — Aug 18 (Tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214      # Mistcrest names/IDs 3437-3441 + upgrade bands (Tier 1 game data — the floor)
  - https://www.method.gg/guides/prey-in-wow-midnight-season-2   # S2 target names, Ral'kala relic cost, Coiled Nightmares achievement (Tier 3, corroboration)
  - knowledge/endgame/prey.md
confidence: medium
---
Track and kill 3 Nightmare Prey for the weekly objective.

⚠ **The gate is still Season 1's wiring.** Quest **94446** ("A Nightmarish Task", objective
*Nightmare Hunts completed (3)*) is what `gate.quest: prey_weekly` maps to, and the
PlannerState dump exposes it as `have/need` (reads e.g. "at 1/3"). That quest is the **S1**
weekly and is **dormant during the pre-season** — no progress can occur this week — and
nothing published says it survives Aug 18. The Season 2 weekly sits under *"A Slithering
Threat"* and already has a **separate reserved slug, `prey_s2_weekly`, with no known ID**
(`../../endgame/weekly-checklist.md`). **Re-wire `gate.quest` before flipping `status:` back
to `active`**, or the ranker will read a dead quest as permanently "not done".

In Season 1 this cleared alongside the **Lady Liadrin world-event weekly**, whose four-choice
offering includes *3 Prey Hunts*. **Do not assume that overlap in Season 2**: `liadrin-spark.md`
records that the S2 quest-giver, the quest IDs, and even the survival of the four-choice weekly
are all unconfirmed — and its Prey option counts *hunts*, which during the pre-season means
Normal/Hard hunts that do nothing for this row.

## ⛔ Pre-season week (Aug 11–17): this activity does not exist

12.1 went live **2026-08-11**, but **Season 2 opens 2026-08-18**. During the week between,
Prey runs **Normal and Hard modes only** — **Nightmare Mode is offline**, so the "3 Nightmare
Prey hunts" weekly cannot be completed. That is why `status:` is `invalidated` right now:
the ranker must not surface an uncompletable weekly. **Flip it back to `active` on
2026-08-18** along with the rest of the S2 catalog.

What *is* payable this week: **Hard Prey drops Season 2 Veteran gear** — a real pre-season
gearing floor for a fresh/undergeared character, but not this row's weekly.

**Nothing about Prey combat is "unchanged by 12.1", either.** There is no Prey-specific
combat change in the notes, but 12.1's four **global** class changes apply here like
everywhere else: **player health and creature damage both +25% at max level** (health
consumables rescaled, several DPS/Tank healing and absorb spells retuned), **major DPS
cooldowns lowered with steady-state damage raised** on several specs, interrupts now showing
a **"missed" visual + sound** when the target wasn't casting, and **diminishing-return
categories resetting after 20s (was 16)**. Nightmare Prey is solo content tuned against
creature damage, so an S1-comfortable hunt is not automatically the same fight — treat the
`time_blocks: 1.5` estimate as untested for 12.1.

## What Season 2 changes (from 2026-08-18)

- **Unlock is a questline again.** *Prey: A Slithering Threat* (Astalor) opens Nightmare
  Mode and the S2 Journey track. Whether that unlock is account-wide or must be repeated
  per character is **unverified** — the S1 answer (Nightmare available on a fresh 90, no
  per-character Rank-4 gate, resolved in-game 2026-07-10) does **not** carry over, because
  S2 puts a new questline in front of it. @verify-ingame
- **The gear roll stays Champion-track — what moved is the ladder, not the tier.**
  Nightmare Prey awards **Season 2 Champion** gear (Tier 1). ⚠ An earlier draft of this row
  called that "a tier drop from S1's Hero roll"; **that was wrong.** S1 Nightmare also paid
  **Champion-track** (`../../_meta/moving-values.md` before-column; `../../endgame/prey.md`).
  The label is unchanged; the numbers are not — **S2 Champion runs 292 (1/6) → 308 (6/6)**
  against S1 Champion's 246 → 263, and **Champion Mistcrest** upgrades the **295–308** band
  (Tier-1 `CurrencyTypes` DB2 @ 12.1.0.69214 + the Lairs reward table, via
  `../../endgame/dawncrests.md`). Which Champion step the hunt reward lands on is
  unconfirmed, so the `yields` slot carries the 292 floor.
- **Four new serpent Nightmare targets, hunted across the Coiled Isle** rather than only the
  four Midnight zones (Tier 1). ⚠ The *names* — Janoa the Fang, Batani the Scaled, Kursak the
  Coiled, Kadani the Claw — are **Tier 3** (method.gg) and appear in no Blizzard note; so is
  the separate claim that killing all four awards a ***Prey: Coiled Nightmares*** achievement,
  which is attested nowhere else in this KB. **Both need in-game corroboration.**
- **"The Curse of the Isle"** — a **permanent, toggleable zone-wide Nightmare mode** for the
  Coiled Isle, for players who want more danger (Tier 1). Whether hunts run under the toggle
  count toward this weekly, or whether it only raises difficulty/drops, is **unstated** — if
  it means you can stay in Nightmare without re-arming a hunt, it changes how this row is
  farmed. @verify-ingame
- **Ral'kala, Terror of the Isle** — summoned by burning **Ossified Relics** at **Haunted
  Braziers** while in Nightmare mode. Blizzard designed it as **group content**, so it is
  not this solo row's business; it is the reason to keep a group handy on the isle. Its
  guaranteed drops are *reported* to include **Champion Mistcrests** — the crest name and
  band are Tier-1 game data (currency **3439**), but **the drop claim itself is Tier 3**.
- **Afflicted / Tormented Souls** drop from **Tier 6+ Bountiful Delves** and **accelerate an
  active Nightmare hunt**, plus grant bonus **Champion-track** (Afflicted) / **Hero-track**
  (Tormented) equipment, **once per week per character**. ⚠ Bountiful Delves are themselves
  not live until Aug 18 (`delve-bountiful.md`), so this coupling starts then — and it makes
  the delve weekly a *prerequisite* to running Prey efficiently, not a parallel chore.
- **Season 2 Prey Journey track: 10 levels** (vendors Construct Ali'a and Construct V'anore
  at Astalor's Sanctum, Silvermoon; track viewable in the Adventure Guide, Shift+J).
- **Anguish costs for housing items are substantially cut**, for both S1 and S2 items — so
  a stockpiled Anguish balance buys noticeably more than the KB's old prices imply.

## Why run it (terminal reward, not the gear roll)

The forced hunt gear piece is a **Champion-track** roll (S2 Champion, 292 floor) — the same
tier S1 paid, so it deflates for a geared main exactly as it did last season and the
slot-target R will discount it fast. The durable reason to keep running Prey is the **Journey
track terminal** (10 ranks of decor, cosmetics, mounts), **Ral'kala's rare drops**, and the
cheaper Anguish spend — not the weekly gear roll.

The S1 draw was **Nightmare → Ascendant Voidshards** (weapon/trinket overcap mats,
`../../systems/void-forge.md`). The 12.1 notes don't mention the Void Forge at all, so that
is **carried, not re-verified**: assume Voidshards still drop until someone checks a live S2
Nightmare hunt. @verify-ingame

Full system detail: `../../endgame/prey.md`.

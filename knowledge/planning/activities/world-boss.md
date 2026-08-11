---
id: world-boss
name: Weekly world boss
goal: [gearing, collectibles]
venue: world
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: world_boss_weekly }
reward: { type: [power, collectible], detail: "weekly loot roll + mount/transmog chance — ⚠ 12.1: the Val/Naigtal boss drops FROZEN Season 1 items (no upgrade path) while its weekly quests pay S2 crests" }
yields:
  slots:
    - { track: hero, ilvl: 263, chance: 1.0, slots: [all] }   # S1 Hero 1/6 = 263 (dawncrests.md S1 bands: Champion 250–263 · Hero 263–276; 259 is Champion 5/6, NOT Hero 1/6 — the old 259 here was wrong and was corrected in the 12.1 sweep). This is the Warbound Normal-WT drop; Heroic WT lands Hero 4/6, and each kill also gives a per-character Soulbound piece (Champion 4/6 Normal WT / Hero 1/6 Heroic WT). chance carried for Phase-3 EV, unused in 2a
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # Curse of Ula'tek Content Update Notes — VAL AND NAIGTAL (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24295085   # "Step Into Lairs and Face the Foes Inside" (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - knowledge/endgame/lairs.md
  - knowledge/endgame/dawncrests.md
  - knowledge/endgame/world-events.md
  - knowledge/planning/candidates.json
confidence: high
---
The rotating weekly world boss — one loot roll for gear, plus a chance at its
mount/transmog (hence `collectibles`). Fast, group-tagged only because you tag along
with whoever's there. Gate resolves from the dump's world-boss lockout.

**What this row actually covers.** The gate is `world_boss_weekly`, which
`plan.py` resolves from PlannerState's `GetSavedWorldBossInfo` lockout — i.e. **every
weekly world boss**: the four Midnight outdoor rotation bosses (**Lu'ashal,
Thorm'belan, Predaxas, Cragpine**) *and* the Val/Naigtal boss (**Imperator Pertinax** /
**Nexus-Captain Leth'ir**). Keep that scope in mind below: the 12.1 changes are
Tier-1 **for Val/Naigtal only**, and the Val/Naigtal *showdown quest* has its own row
(`showdown-weekly`), as does the zone farm (`val-naigtal`).

## ⚠ 12.1: Lairs took the gearing role, and the Val/Naigtal boss's loot is frozen

**Outdoor bosses are no longer the outdoor group-gearing path.** 12.1 introduced
**Lairs**, an instanced world-boss format with real difficulties, a weekly lockout and a
real Season 2 reward track — Blizzard's own framing is "an evolution on world bosses"
(see `../../endgame/lairs.md`, and the activity row `lair-tidebound-grotto`). The old
fly-out-and-tag-a-boss loop still exists and still runs its rotation, but the Season 2
ladder has moved past it:

- **Val/Naigtal only (Tier 1): the World Boss drops remain Season 1 items and can no
  longer be upgraded** (verbatim: *"The World Boss drops will remain as Season 1 drops
  and can no longer be upgraded"*). So that piece **lands at S1 Hero 1/6 = 263 and stays
  there** — the 276 crested Hero ceiling this file used to value it at is **gone**. Same
  freeze applies to the Mythic quest rewards from *"Knocking off the Top (Heroic)"*.
  (Two drops per kill, not one: a **Warbound** item — S1 Hero 1/6 on Normal World Tier,
  Hero 4/6 on Heroic — **plus** a per-character **Soulbound** piece, S1 Champion 4/6 on
  Normal / Hero 1/6 on Heroic. For a fresh alt the Soulbound half is often the better of
  the two. Both are frozen; see `_meta/moving-values.md`.)
- For comparison, the **World difficulty of Tidebound Grotto** — solo-queueable, also a
  weekly lockout, also ~one boss — drops **279 (S2 Veteran 1/6)** *and* a Veteran
  Mistcrest, and Season 2's ladder runs 269 → 334 against Season 1's 224 → 289. A frozen
  263 loses to it on every axis. **If you only have time for one outdoor boss this week,
  run the Lair.**
- **The four Midnight rotation bosses are an open question.** No Tier-1 12.1 note names
  them, so nothing here asserts their drops are frozen, retiered, or worth taking — that
  is the open in-game item in `../../endgame/world-events.md` (§TODO,
  `@verify-ingame`): *do Lu'ashal / Thorm'belan / Predaxas / Cragpine still drop anything
  worth taking in Season 2, or are they cosmetic-only now that Lairs carry the track?*
- Either way, keep running whichever boss is up for the **mount / transmog** roll; treat
  the Val/Naigtal one as a gearing move only for a genuinely fresh alt sitting under 263.

**No `reward_base` override is set on this row**, deliberately. A demotion to 1 would be
justified by the Val/Naigtal freeze alone — but this gate fires on *all* weekly world
bosses, so overriding here would silently down-rank the four Midnight bosses on evidence
that does not cover them. The `goal: gearing` prior of **3** therefore stands until the
`@verify-ingame` above is resolved; if the answer is "cosmetic-only", the override belongs
here, and if it stays Val/Naigtal-specific it belongs on `showdown-weekly` instead.

## Crests (new in 12.1)

**In Val and Naigtal**, the **World Boss and the zone's weekly quests now give Season 2
crests** — **S2 Adventurer Mistcrest** on Normal World Tier, **S2 Veteran Mistcrest** on
Heroic World Tier. That is a genuine change from 12.0.7, where the boss itself paid no
crest at all and crests came only from the surrounding rares. (Season 2's crests are
**Mistcrests**, confirmed from `CurrencyTypes` DB2 @ 12.1.0.69214, IDs 3437–3441;
Adventurer upgrades 269–282, Veteran 282–295 — see `../../endgame/dawncrests.md`.)
Nothing equivalent is documented for the four Midnight rotation bosses.

It is **deliberately not declared as `yields.currencies` here**: the Val/Naigtal zone-farm
row already carries the zone's crest yield (`val-naigtal`), and splitting it would
double-count the same weekly. Two open wiring items, both belonging to the planner tooling
rather than to this file: `rewards.py` has **no canonical `adventurer_crest` key** yet, and
no Tier-1 source states a crest *amount* for this quest (so nothing is invented here).
⚠ `_facets.md` still uses "world boss" as its example of *a gear drop declares no
`yields.currencies`* — true of this row's front matter, but the Val/Naigtal boss does now
pay a crest, so that example needs rewording when `_facets.md` is next touched.

**Grouping is easy — the quest carries an LFG hook** (in-game, 2026-07-09): the world-boss
quest shows a little **LFG icon** that opens the free-form group finder pre-seeded with a
search term, so finding a group is very likely. This is why a world boss shouldn't take the
full `group`-content solo penalty (a future `--solo` down-rank, Phase 4) — it's `group` to
*fight* but trivially puggable via the hook. (Note the Lair goes further still: World
difficulty is a **solo queue** that fills itself, so it carries no grouping cost at all.)

**No `yields.currencies` (needs-first Phase 1).** The boss yields a **gear** roll
(Warbound on Normal World Tier) — valued off the **263 landing ilvl** via `slot_target_R`,
and no longer off a `reward_ilvl_max: 276` ceiling, because for the Val/Naigtal boss that
ceiling no longer exists. Its warbound-cache-for-alts value is a Phase-4 flow.

**The fight itself is not what it was in 12.0.7 either**, even where no boss-specific note
exists: 12.1's global combat retune applies everywhere — **player health and creature
damage +25% at max level** (with health consumables rescaled and several DPS/Tank
healing/absorb spells adjusted), **major DPS cooldowns lowered with steady-state damage
raised** on several specs, interrupts now flashing a **"missed"** visual when the target
wasn't casting, and **diminishing-return categories resetting after 20s** (was 16).

---
id: showdown-weekly
name: Val / Naigtal Showdown weekly
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: showdown }
reward: { type: [power, currency, collectible], detail: "Riftstalker's Cache (Field Accolades, Relic Coffer Key shards, mats, gold); 12.1: the weekly also pays S2 Adventurer crests (Normal WT) / S2 Veteran crests (Heroic WT); ⚠ the world-boss gear drop is a FROZEN Season 1 item, not upgradeable; showdown-achievement mounts" }
yields:
  currencies: { field_accolade: 100 }   # weekly Riftstalker's Cache (world-events.md). ⚠ 12.1 also adds an S2 crest payout — no Tier-1 amount published, and rewards.py has no `adventurer_crest` key, so it is deliberately NOT declared here (see "Planner wiring" below)
  # NO `slots:` VECTOR, deliberately (12.1). The kill's gear roll is declared by `world-boss`,
  # which owns it; declaring it here too double-counts. And it can no longer be expressed here
  # honestly: candidates.json is regenerated from this front matter, where `track: hero` now
  # means the SEASON 2 Hero band (305–321) — while this boss's drop is frozen at a Season 1
  # item level. A Season-1 track label in a Season-2 field is worse than no label. This row is
  # the weekly capstone quest + the achievement; see `world-boss` for the loot.
time_blocks: 1.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes — EVENTS ▸ VAL AND NAIGTAL / VOID-TOUCHED CACHES (Tier 1)
  - https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1
  - yt:kUP8oqI7Ekc
  - knowledge/endgame/world-events.md
  - knowledge/endgame/dawncrests.md   # S1/S2 track-1/6 ilvls, from CurrencyTypes DB2 @ 12.1.0.69214
  - knowledge/_meta/patch-notes/12.1.md   # verbatim EVENTS ▸ VAL AND NAIGTAL block
confidence: medium
---
The **"Showdown on Val" / "Showdown on Naigtal"** weekly (whichever world the Voidstorm portal
points at this reset — it rotates every few days). WQs, rares, and events across the active
world culminate in the world-boss showdown; the weekly pays a **Riftstalker's Cache** (Field
Accolades, Relic Coffer Key shards, materials, gold).

## ✅ 12.1: still running — and re-tiered to Season 2

**The weekly is live in 12.1.** The confirmation is Tier-1 and indirect but unambiguous: the
Content Update Notes' **VAL AND NAIGTAL** section re-tiers this content rather than retiring
it, verbatim — *"The World Boss and **Weekly Quests** will offer Season 2 Adventurer crests in
Normal World Tier and Season 2 Veteran crests in Heroic World Tier."* You do not re-price the
rewards of a weekly you are switching off. It is **not** untouched, though: 12.1's game-wide
class/combat retune lands here like everywhere else (see below).

⚠ **WHEN the retier takes effect is inferred, not stated.** No Tier-1 note dates it, and the
Aug-11 / Aug-18 pre-season split table in `_meta/changelog-12.1.md` carries **no Val/Naigtal
row** at all. The dated siblings that behave like this one (Ritual Sites, Pinnacle Caches)
flipped on patch day, so the reasonable read is that everything below is live **this** week —
but that is analogy, not a source. Confirm by watching an Adventurer/Veteran Mistcrest actually
land off the weekly turn-in before planning a pre-season crest bank around it. @verify-ingame

What actually changed for this row:

| | 12.0.7 | **12.1** |
|---|---|---|
| Weekly-quest crests | none from the quest itself | **S2 Adventurer** (Normal WT) / **S2 Veteran** (Heroic WT) |
| World-boss gear drop | Warbound **Hero-track** (1/6 Normal WT · 4/6 Heroic WT) + Soulbound **Champion 4/6** (Normal WT) / **Hero 1/6** (Heroic WT), crestable to 276 | **same items, frozen as Season 1 — no longer upgradeable** |
| Field Accolade spend | slot-targeted **Hero-track** gear (Maren Silverwing) | that S1 stock is **removed**; new **S2 Adventurer / S2 Veteran** Void-Touched Caches |

⚠ **The boss loot is now the weakest part of this row.** *"The World Boss drops will remain as
Season 1 drops and can no longer be upgraded"* — the piece lands at its **Season 1** item level
and stays there forever (**S1 Hero 1/6 = 263** for the Warbound Normal-WT drop; `world-boss`
carries the full per-tier landing table, and the old crested 276 ceiling is unreachable). The
"Knocking off the Top (Heroic)" Mythic quest reward is frozen the same way. Run the Showdown for
the **cache, the crests and the achievement mounts**; for outdoor group gearing the **Lair**
(`lair-tidebound-grotto`, World difficulty, solo-queueable) drops **279 = S2 Veteran 1/6** plus a
Veteran Mistcrest and beats a frozen Season 1 piece on every axis.

⚠ **12.1's global combat retune changes how this feels, not what it pays.** Applying to every
spec in every instance and outdoors: **player health and creature damage are both up 25% at max
level** (health consumables rescaled; several DPS/Tank healing + absorb spells retuned to keep
their relative value), **major DPS cooldowns were lowered with steady-state damage raised** for
several specs, **interrupts now show a "missed" visual + sound** when the target wasn't casting,
and **diminishing-return categories reset after 20s** (was 16). Practically for this row: the
"can I solo the Heroic-WT approach" judgement below was formed pre-patch, so re-test it rather
than trusting it, and any remembered health-potion/self-heal number is now wrong.

On **Heroic World Tier** the loop still upgrades — rares drop better gear (now **S2 Adventurer 4/6** Warbound-until-equipped, vs Adventurer 1/6 on Normal), the weekly
pays the **Veteran** crest tier instead of Adventurer, Void Commander's Emblems still feed the
(now frozen) "Knocking off the Top" quest, and the **Heroic Showdowns achievement path unlocks
mounts** (hence `collectibles`). **Dedup note:** the boss loot roll overlaps `world-boss` and
the *ongoing zone farm* (WQs/rares that earn the currency + fill the World Vault row) lives in
`val-naigtal`; this row is specifically the **weekly capstone quest** (Riftstalker's Cache) +
achievement.

**No ilvl gate is stated for Heroic World Tier.** This row used to carry a pre-12.1 "recommended
~ilvl NNN" figure; the 12.1 notes do not restate it, and with player health and creature damage
both up 25% and the whole track ladder shifted +45, a remembered Season 1 threshold is not
transferable. It has been struck rather than hedged — pull one Heroic-WT elite and judge from
that.

## Field Accolades — same currency, a different shop (12.1)

Accolades are still a real gearing currency, but **what they buy was re-cut**. At **Maren
Silverwing** (top of the Bazaar, Silvermoon City) the **Season 1 gear caches have been removed**,
replaced by **Void-Touched Caches** on the Season 2 tracks:

- **200 Accolades** — Season 2 **Adventurer** cache, **Warbound until equipped**, **ilvl 266**
  (Adventurer 1/6) *(slot: not stated — see the note below)*
- **500 Accolades** — Season 2 **Veteran** cache, **Bind-on-Pickup**, random slot, **ilvl 279**
  (Veteran 1/6)
- **750 Accolades** — Season 2 **Veteran** cache, **Bind-on-Pickup**, slot-specific, **ilvl 279**

Both ilvls come from the track-1/6 column in `../../endgame/dawncrests.md`, which derives them
from `CurrencyTypes` DB2 @ `12.1.0.69214` — game data, not editorial inference. The notes
themselves state only the costs, the tracks and the binding.

So the deterministic "buy the exact slot you're missing" play survives **at the same 750
Accolades it cost in Season 1** — the *price* did not move. What moved is the item it hands
you: Season 1's 750 cache was a slot-specific **Hero**-track piece, Season 2's is a
**Veteran 1/6 (279)**. That is two tracks down (Hero → Champion → Veteran) at an unchanged
price, offset by the whole ilvl ladder shifting up a season. The S1 **100**-Accolade
slot-specific Champion cache has no direct successor; the cheap tier is now the **200**
Adventurer cache. Accolades also still buy cosmetics/decor at Fieldsmith Ventem / Zuronar —
see `val-naigtal` for the full spend.

⚠ **Open question on the 200 cache: is it slot-specific?** The 12.1 notes say only *"New Season 2
Adventurer **Warbound** caches available for 200 Field Accolades"* — cost, track and binding, no
slot. The **ilvl is settled** (266, above). `systems/void-incursions.md` additionally records the
cache as **slot-specific**, sourced to a warcraft.wiki.gg cache page (Tier 3) rather than to the
notes — plausible, and it matches how the Season 1 lineup was cut, but not corroborated by Tier 1
or by DB2. If it holds, there is a *cheaper* deterministic slot buy at 200 Accolades (Warbound,
so it also gears alts) and the 750 line is only the deterministic *Veteran* buy. Until then,
don't build an Accolade budget around targeting a specific slot at 200. Check Maren Silverwing's
stock in game. @verify-ingame

**Planner wiring (open, tooling-side):** (1) No Tier-1 source states a crest *amount* for this
weekly, and `rewards.py` has **no canonical `adventurer_crest` key** at all, so
`yields.currencies` still lists only accolades — the row under-values its crest payout until both
land. Confirm the quantity on the cache turn-in. @verify-ingame (2)
`rewards.py::_consume_field_accolade` values accolades against the **deleted Season 1 Hero-track
box**; its consumer should be re-pointed at the S2 Veteran slot-specific cache (750 Accolades →
279). (3) This row's `yields.slots` vector was **removed** in the 12.1 sweep — it declared a
Season 1 ilvl under a `track:` label that now names a Season 2 band, and it double-counted a roll
`world-boss` already declares. How a **frozen, non-upgradeable** drop should be valued at all is
a `planning/scoring-model.md` question, not a per-file number. All three are filed in
`_meta/kb-inbox.md`.

**Grouping the boss — LFG hook + the Val lair-access catch** (in-game, 2026-07-09): the
world-boss quest carries a **LFG icon** that opens the free-form group finder with a
pre-filled search term, so getting a group for the *kill* is easy — you don't need to solo
the Heroic-WT boss even under-geared. The real friction is **reaching the boss**: the **Val**
boss sits in an **underground lair that's hard to enter — a lot of elites floating around the
approach** (Naigtal's is more accessible). Practically: form/join via the LFG hook and punch
through the lair *together*. So for an under-geared alt the boss is feasible via group; the
**zone-farm** survivability caveat (soloing Heroic-WT rares/elites for Accolades) in
`val-naigtal` still stands separately.

---
id: pvp-honor
name: Honor gear + repeatable PvP quests
goal: [gearing]
venue: pvp
group: flex
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [power, currency], detail: "Honor → full honor set (S1 baseline ~10K honor; S2 cost unmeasured); Voidstorm PvP quests → Honor + Bloody Tokens + Slayer's Duellum rep" }
time_blocks: 1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281
  - https://worldofwarcraft.com/en-us/news/24294369
  - https://www.icy-veins.com/wow/midnight-pvp-gearing-guide
  - "yt:6OkVWEdttZ0"
  - "yt:cpbQXd04ehI"
confidence: low
---
The entry-level PvP floor: unrated PvP for **Honor**, which buys a full honor set.
`cadence: repeatable` — no reset, always available (`gate: always`, low urgency).

**Pre-season week (Aug 11–17): this is the only PvP row that works.** 12.1 shipped with
**unrated PvP only** — Battlegrounds and outdoor-world PvP — plus the new **Training
Grounds: Arenas** (3v3 versus bots), reached from **Group Finder → Player vs. Player tab →
Training Grounds**, alongside the existing Training-Grounds Battlegrounds. **All rated PvP
(Arena, Solo Shuffle, BG Blitz) is off until Season 2 opens the week of Aug 18**, so
`pvp-conquest` has nothing to offer this week and every PvP minute routes here.

12.1 changed how BG combat feels, which is worth knowing before queueing:

- **Battlegrounds now apply 20% reduced healing received** to all players. Blizzard's
  stated intent is lower survivability — healers and off-heal kits are meaningfully
  weaker, kills land faster, damage output matters more.
- **Gladiator's Distinction** (the PvP trinket set bonus the honor trinket carries) was
  re-weighted: tank/DPS **+15% primary stat** (was 12%) and **+5% Stamina** (was 10%);
  healers **+10% Stamina** (was 15%). Non-healers trade EHP for throughput; healers
  simply lose EHP.
- **Missing a Solo Shuffle or Battleground Blitz queue** now applies a **1-minute
  re-queue debuff** that **stacks** on consecutive misses within a window and is
  **account-wide** (anti win-trading). Only bites from Aug 18, when those queues return,
  but "queue and go do something else" is now punished across the whole roster.
- Players are **no longer knocked back while under Fear or Disorient**.
- 12.1's **four global class changes** land in PvP too, and none of them is
  spec-specific: **player health +25% at max level** (health consumables rescaled
  to match, and several DPS/Tank heal + absorb spells retuned), **major DPS
  cooldowns lowered with steady-state damage raised** on several specs,
  **interrupts now show a "missed" visual + sound** when the target was not
  casting, and **diminishing-return categories now reset after 20s (was 16)** —
  the last one lengthens every CC chain window in a BG.
- Game-wide **PvP snare tier-down**: auto-applied rotational slows are cut a tier
  ("70% reduced to 50%, 50% to 30%"), while some activated slows keep their value.
  Kiting is better; every class has a line changed here.

**Season 2 honor gear arrives Aug 18.** The unrated set is reported to be the **Venomous
Aspirant** line at **PvP ilvl 324**, bought with Honor and upgraded with **Mistcrests**
plus gold. ⚠ The *set name* and the *324* are Tier-3/4 only — Blizzard's S2 PvP line names
only the mounts and the Venomous* title ladder, and published no honor ilvl — and the
Season 1 figures below are S1-era. The **Mistcrests** part is not in doubt: all five S2
crest tiers are Tier-1 confirmed from `CurrencyTypes` DB2 @ 12.1.0.69214 (Adventurer
269–282 · Veteran 282–295 · Champion 295–308 · Hero 308–321 · Myth 321–334), so upgrade
costs will be quoted in Mistcrests whatever the set turns out to be called. Note a PvP
*item level* is the instance-scaled number, not a position on those crest bands — don't
read 324 as a Myth-track item. @verify-ingame at the Silvermoon PvP
vendor once S2 opens: the honor set's real name and ilvl, the honor cost of a full kit,
whether Training Grounds (BGs *or* the new Arenas) actually pays Honor, and whether
war-mode gear still matches honor gear in ilvl.

Season 1 shape, kept as the baseline until the above is re-measured: a complete honor kit
ran **~10K honor**, and war-mode gear was the **same ilvl** as honor gear, making bloody
tokens optional min-max only.

Also the home of the **repeatable Voidstorm PvP quests**, folded in here rather than split
out. Both are in the scraped quest table (`endgame/daily-weekly-quests.md`) and both pay the
same three things — **Honor + Bloody Tokens + Slayer's Duellum rep**, no other currency:

| Quest | ID | Cadence | Pays |
|---|---|---|---|
| **Carve Your Way** | 93865 | daily (high conf.) | Honor ×50 · Bloody Tokens ×50 · Slayer's Duellum ×100 · 13,690 XP · 34g |
| **Preparing for Battle** | 89354 | **unknown** (low conf. — likely weekly) | Honor ×500 · Bloody Tokens ×150 · Slayer's Duellum ×1,000 |

*(Corrected 2026-08-11: an earlier revision of this row described these as two weekly quests
from an NPC "Zaralla" in Silvermoon paying **Marks of Honor**. All three of those are wrong —
the giver name is attested nowhere else in the KB, Marks of Honor is a legacy transmog
currency that no 12.x quest here pays, and only one of the two is a confirmed weekly. Also
not this row: the **Sparks of War** War-Mode weekly — collect 100 in the rotating War-Mode
zone (Voidstorm / Zul'Aman / Harandar) — which pays a **crafting spark**, not Honor, and
belongs to `liadrin-spark` / `systems/professions.md`.)* @verify-ingame the quest givers and
`Preparing for Battle`'s real cadence at the Voidstorm PvP hub.

`gate: always` keeps it as fill-time; the rated push lives in `pvp-conquest`.

⚠ **This row needs a re-pass on/after 2026-08-18.** Two of its load-bearing sentences invert
when Season 2 opens: "every PvP minute routes here" and "`pvp-conquest` has nothing to offer"
are both pre-season-only. `status` stays `active` either way, but the priority framing, the
S2 honor set's real name/ilvl/cost, and the Solo Shuffle / BG Blitz missed-queue debuff all
become live facts that week.

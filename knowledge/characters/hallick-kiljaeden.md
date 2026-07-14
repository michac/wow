---
title: Hallick – Kil'jaeden (US) — druid alt snapshot
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/hallick?namespace=profile-us
  - PlannerState /ps dump + Syndicator (currencies), 2026-07-11
confidence: high
---

# Hallick – Kil'jaeden (US)

> **Snapshot** — character data is volatile (updates on logout). The body
> below reflects the **2026-07-10** live profile fetch (last login
> 2026-07-09 16:37 UTC). **Always re-fetch the live profile before answering any
> gear/level/progress question** — this alt is actively leveling/gearing
> and numbers move fast. Raw JSON: `raw/blizzard/hallick-*.json`.
>
> **Δ since 2026-07-10:** **fully static — no login since 2026-07-09 16:37 UTC.**
> Gear, renown, and currencies are byte-identical to the last sync (worn ilvl
> 153, gold 14,074, vault 0/0/0). ⚠ Because he hasn't `/reload`ed since, the
> Syndicator currency values may lag reality — re-`/reload` on Hallick before
> trusting them for any spend. (Note: the account-wide **Champion of the Dawn**
> discount that Encomplete just earned applies to Hallick too — but he has no
> Champion-track gear yet to spend it on.)

**Alt of the user's main (Encomplete).** No longer same guild — Hallick is
still in **The Soggy Bottom Boys**, Encomplete moved to Dungeon Dojo.
Achievement points 7,750 (account-wide, tracks Encomplete's 7,800).

## Identity

- Night Elf **Druid**, active spec **Feral**
- **Level 90 (cap)** — reached the Midnight cap since the last snapshot
  (was 80 on 2026-06-03). Now in the early endgame gearing phase.
- Alliance, Kil'jaeden · Title: Knight-Lieutenant
- Last login at fetch: 2026-07-09 16:37 UTC

## State

- **Equipped ilvl 153** (API average 202 — inflated by best-in-bags;
  worn value is ~153). Fresh-90 leveling/quest greens and early Midnight
  drops; a couple of Preyseeker/crafted pieces (chest 151, back 171).
- The full endgame loop now applies (weekly checklist, delves, crests,
  ritual sites). This is a from-scratch Season 1 gearing runway — same
  playbook as Encomplete's, one tier behind.

## Gear (equipped ilvl 153, API 2026-07-10 — unchanged since 07-02)

| Slot | ilvl | id | Item |
|---|---|---|---|
| Head | 165 | 256996 | Verdant Tracker's Guise |
| Neck | 158 | 248050 | Tranquillien Choker |
| Shoulders | 158 | 249642 | Osseoclad Razorspaulders |
| Chest | 151 | 259925 | Preyseeker's Sleek Jerkin |
| Waist | 145 | 248041 | Belt of Herbicide |
| Legs | 158 | 248033 | Twilight Spy's Tights |
| Feet | 145 | 248056 | Lightstalker's Treads |
| Wrist | 152 | 249644 | Osseoclad Ivory Wrist |
| Hands | 165 | 249639 | Osseoclad Spinegrapplers |
| Ring 1 | 152 | 250361 | Depleted Voidshard Ring |
| Ring 2 | 145 | 248048 | Ring of Overgrowth |
| Trinket 1 | 146 | 251783 | Lost Idol of the Hash'ey |
| Trinket 2 | 145 | 251785 | Void-Reaper's Libram |
| Back | 171 | 251132 | Speakeasy Shroud |
| Main Hand | 152 | 250355 | Twilight Agitator's Stave |

No enchants or gems detected — all low-hanging fruit as gear stabilizes.

## Currencies & renown (2026-07-10)

- **Gold 14,074** · **Restored Coffer Key 5** (+19 shards) · Field Accolade 20 ·
  Voidlight Marl 2,554 · Remnant of Anguish 467 · Dawnlight Manaflux 8 ·
  Radiant Spark Dust 7. **No Dawncrests banked** (fresh gearer — none earned yet).
- **Renown (Midnight-relevant):** Silvermoon Court **12** (2095/2500) · Amani Tribe
  **8** (2310/2500) · Hara'ti **8** (680) · The Singularity **8** · Ritual Sites **4**.
- **Crafting mats (Syndicator items):** Sparks of Radiance **7** · Ascendant
  Voidshards **0**. Catalyst charges = Dawnlight Manaflux (8, above).
- ⚠ Currencies from Syndicator (last login 07-09) — re-`/reload` on Hallick before
  trusting for spend advice.
- This reset: all weeklies undone, **0 world bosses**, vault **0/0/0** — the fresh-gearer
  runway is untouched this week.

## Talent audit (2026-07-02)

- **Resolved:** Hallick now has a hero talent tree selected — **Druid of
  the Claw** (Ravage, Dreadful Wound, Wildshape Mastery, Twin Claw, Claw
  Rampage, …), which is exactly the earlier recommendation. Full 14-node
  hero loadout in place.
- Feral class-talent loadout active. Re-audit vs the current simc Feral
  reference once he's settled at 90 and gearing (leveling carryover may
  have suboptimal points).
- Leveling rotation page (built at 80):
  `../classes/druid/feral/leveling-rotation.html`.

## Professions

- **Herbalism** (Midnight 21/100; Classic tier barely started)
- **Alchemy** (Midnight 7/100)
- Cooking 124/300, Fishing 122/300 (Classic tiers)
- Herb/Alch is a self-sufficient gathering+consumables pair — flasks/pots
  for his own raiding/M+ once leveled.

## TODO

- [ ] Max-level Feral **build/rotation** docs now that he's 90
      (`../classes/druid/feral/` — currently only a leveling page exists)
- [ ] Re-audit Feral talents vs simc reference on real gear
- [ ] Early Season 1 gearing path (delves/ritual sites/spark crafts) —
      mirror Encomplete's plan, adjusted for ilvl 153 start
- [ ] Level Midnight Herbalism/Alchemy for self-supplied consumables

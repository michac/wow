---
title: Current Game Version — Single Source of Truth
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # Curse of Ula'tek content update notes (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 information — the pre-season split (Tier 1)
  - https://news.blizzard.com/en-us/article/24295090/midnight-curse-of-ula-tek-pre-season-details  # pre-season details (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # Midnight Season 2 overview + unlock schedule (Tier 1)
  - https://wago.tools/api/builds                     # live client build (Tier 1)
confidence: high
---

# Current Game Version

> **This file is the single source of truth for game state.** Every answer the
> agent gives must be consistent with this file. Update it on patch days.

| Field | Value |
|-------|-------|
| Expansion | **Midnight** (WoW's 11th expansion, 10th in numbering: 12.x) |
| Live patch | **12.1 "Curse of Ula'tek"** (live client build `12.1.0.69214`, pushed 2026-08-10, live 2026-08-11) |
| PTR patch | **none** — the `wowt` PTR line converged onto `12.1.0.69214`, the same build as live. No next patch announced. |
| Level cap | **90** |
| Current season | ⚠ **Midnight Season 2 — PRE-SEASON WEEK** (see below). Season 1 ended with the week of 2026-08-11 maintenance. |
| Season 2 opens | **2026-08-18** (weekly maintenance) |
| Weekly reset | Tuesday (US region) |

> ⚠ **Game Data API namespace lag (measured 2026-08-11):** the Blizzard Game
> Data API's `static-12.1.0` namespace reports build **12.1.0.68914** while the
> live client is **12.1.0.69214**. The Trait\* DB2 exports at the two builds are
> **byte-identical** (verified by md5 on `TraitNodeEntry`), so API-sourced talent
> data is valid for live — but do not report 68914 as the live build.

---

## ⚠ THE THING TO GET RIGHT THIS WEEK: 12.1 shipped in two steps

**12.1 went live 2026-08-11 into an official pre-season week. Midnight Season 2
does not open until 2026-08-18.** Most published 12.1 coverage describes the
Aug-18 state. Answering "what's live?" from the content-update notes alone will
be wrong all week.

| | **Week of Aug 11 — LIVE NOW** | **Week of Aug 18 — Season 2 opens** |
|---|---|---|
| Zone | Coiled Isle, Curse Surges, Vaults of Atal'Utek, Venom Fishing, Zul'jarra's Forces renown | — |
| Dungeons | New S2 pool on Heroic + Mythic 0. **M0 on a WEEKLY lockout, this week only**, drops Champion 1/6 (ilvl 292) | Mythic+ opens, keystones drop, **M0 back to daily** |
| Raid | **none** | Venomous Abyss — Normal / Heroic / Mythic + LFR Wing 1 |
| Lair | Tidebound Grotto — **World difficulty only** | Tidebound Grotto — Normal / Heroic / Mythic (flex 15–25) |
| Delves | Tiers 1–11 + **"?" Nemesis**. **No Bountiful, no Coffer Keys.** Max **Adventurer 3/6 + Veteran Mistcrests** | Bountiful Delves, Coffer Keys, **"??" Nemesis** |
| Prey | Normal + Hard. Hard Prey drops S2 Veteran | Nightmare Mode (Champion gear) + "Curse of the Isle" |
| PvP | Training Grounds: Arenas; **unrated only** | PvP Season 2, all rated |
| Great Vault | Pays out on your **final Season 1 week**. S2 credit starts accruing now | First S2 vault. **World row capped Champion 3/6**, then Hero 1/6 |
| Other | Pinnacle Caches drop S2 Veteran; **Crafting Sparks begin dropping** | Voidcore bonus rolls arrive **week of Aug 25** (needs ≥3 panes) |

Later LFR wings: **Wing 2 + Story** Aug 25 · **Wing 3** Sep 1 · **Wing 4** Sep 8.

**A follow-up `/update` pass is owed on or after 2026-08-18** to flip this file
and the activity catalog from pre-season to Season 2.

## 12.1 "Curse of Ula'tek" highlights (live 2026-08-11)

- **New zone: The Coiled Isle** — island off the east coast of Zul'Aman.
  **Vaults of Atal'Utek** (group content + rotating public events), **Curse
  Surges** (rare elites at 5 rotating locations; each kill unlocks **Venom
  Fishing** there), the **Altar of Corrosion** zone-scoped talent tree bought
  with **Corrosive Coins**, and the tortollan captain **Tokka**'s local story.
  (`systems/coiled-isle.md`)
- **New renown faction: Zul'jarra's Forces** — 20 ranks, quartermaster
  **Jan'sari the Watchful** at Tokka's Landing (`factions/zuljarras-forces.md`).
- **Lairs** — a new **instanced world-boss format**, World/Normal/Heroic/Mythic
  (flex 15–25), Delve-like locations with a summoning stone. First lair: **the
  Tidebound Grotto** (boss Nymrissa Wavecaller). (`endgame/lairs.md`)
- **New dungeon: Altar of Fangs** (3 bosses) and **new raid: The Venomous
  Abyss** (8 bosses, final boss Ula'tek) — the raid opens Aug 18.
- **Three new Delves**: The Ring of Glory, Gnarldor Isle, and the **Venomfall
  Deeps** Nemesis delve.
- **Season 2 crests are Mistcrests**, and the whole gear ladder shifts **+45**:
  S2 runs **ilvl 269 → 334** against Season 1's 224 → 289.
  (`endgame/dawncrests.md`)
- **Global combat retune**: player health **and** creature damage **+25%** at max
  level (health consumables rescaled); major DPS cooldowns lowered with
  steady-state damage raised; interrupts now show a "missed" visual + sound;
  diminishing-return categories reset after **20s** (was 16s).
- **Cooldown Manager now tracks trinkets, potions and racial cooldowns**, and
  spells/items on it can be **pinged**; new `/pingspell:` and `/pingitem:`
  macros. New addon APIs for displaying filtered aura sets without exposing the
  underlying aura data. (`knowledge/addon-dev/`)
- **Housing**: Blueprints (export/import, 50 slots), Pet Beds, four new
  neighborhood Endeavors, **houses to level 12**, new Artisanal Rooms.
- **Earthen**: zone-exploration XP **−60%** baseline (low-level zones no longer
  reduced); Ingest Minerals' Well Fed **+30%**.

## 12.0.7 "Revelations" highlights (historical — superseded by 12.1)

- New zones **Val and Naigtal**; the **Omnium Folio** runic-power system;
  the single-boss **Sporefall** raid; **Ritual Sites Tier 6** (3-site rotation);
  Void Assault XP/drop buffs; gear no longer takes combat durability damage;
  Turbulent Timeways (**ended 2026-08-11**).

## 12.0.5 "Lingering Shadows" (historical)

- Ritual Sites + Field Accolades; Void Incursions / Void Strikes; Abyss Anglers;
  Decor Duels; the Voidforge questline and Nebulous Voidcores.

## Update checklist (patch day)

1. Bump `patch:` / `build:` / PTR fields above.
2. Re-verify `knowledge/endgame/weekly-checklist.md` — the anchor doc.
3. Sweep `knowledge/**` front matter: anything with `patch:` older than the
   live version needs re-verification or a `confidence: low` downgrade.
4. Regenerate the DB2-derived artifacts — `wowkb.talents fetch/enrich/build` and
   `wowkb.gen_abilities`. ⚠ **Both carry a hardcoded build/patch constant**
   (`spec_inventory.PINNED_BUILD`, `gen_abilities.PATCH`); bump them or the
   "regenerated" files silently stay on the old patch.

---
title: Next Patch — 12.0.7 "Midnight: Revelations" (releases 2026-06-16)
patch: 12.0.7            # describes the upcoming patch (PTR state as of fetch)
fetched: 2026-06-03
sources:
  - https://www.wowhead.com/news/patch-12-0-7-release-on-june-16-381783
  - https://www.icy-veins.com/wow/news/the-12-0-7-revelations-content-patch-arrives-on-june-16th/
  - https://us.forums.blizzard.com/en/wow/t/midnight-revelations-ptr-development-notes/2300244
  - https://www.icy-veins.com/wow/news/increased-heroic-world-tier-rewards-midnight-12-0-7-ptr-development-notes-may-19th/
  - https://www.youtube.com/watch?v=9bwN3anUE-E (MrGM, 2026-05-20, full patch overview)
  - https://www.youtube.com/watch?v=UL2pVoG48DI (MrGM, 2026-05-26, Omnium Folio deep dive)
  - https://warcraft.wiki.gg/wiki/Turbulent_Timeways (TT5 dates/rotation, XP buff mechanics)
confidence: medium       # PTR data — numbers/details can change before live
---

# Patch 12.0.7 "Midnight: Revelations"

> **Releases Tuesday 2026-06-16 (US) / 06-17 (EU)** — officially confirmed
> (Wowhead/Icy Veins news; earlier "June 30" speculation was caused by
> Turbulent Timeways moving to June 30, decoupled from the patch itself).
> **Two weekly resets remain on 12.0.5: June 9 and June 16.**
>
> ⚠ Everything below is PTR-sourced (dev notes through late May, RC build).
> Numbers — especially Omnium Folio rune values, which explicitly do NOT
> scale with ilvl yet — are subject to change. Re-verify on patch day and
> fold confirmed details into the topic files; then this file gets rewritten
> for 12.1.

## Headline features

### Sporefall raid (one boss: Rotmire, in Harandar)
- Difficulties: LFR / Normal / Heroic / Mythic — Mythic is **flex 15–25**
  (first time ever for Mythic).
- Loot is **not upgradeable** but drops at max-equivalent ilvls:
  **LFR 259 · Normal 272 · Heroic 285 · Mythic 298**.
- Extras: Luminous Spore Glider mount (combine 4× Delicious Spore Sacks,
  believed to drop on all difficulties), decor item, cosmetic helm, 2 toys.

### Showdown mini-zones: Naigtal & Val (Void Assault Escalations)
- Two redesigned Legion-invasion maps; **rotate weekly** (one up at a time).
  Naigtal = fungal world (Hal'hadar ethereals, Nexus-Captain Leth'ir);
  Val = icy world (Domanaar Imperator Pertinax). Entry portal in the
  Voidstorm or Silvermoon after a short unlock questline.
- Story quests, bonus objectives, world quests, rares, treasures, world boss.
- **Normal vs Heroic World Tier** (delve-style dropdown). Heroic gives:
  more Field Accolades, Champion crests from WQs (Veteran on normal),
  warbound Hero loot from rares (Veteran on normal), **Hero** world-boss
  loot (Champion on normal).
- **One-time quest: a Myth-track item for 4 world-boss kills** — i.e. 4
  weeks; first Myth-track access for pure world players. Start week 1.
- Cosmetics: blue Prey set recolor (accolades + lots of Voidlight Marl;
  rares can drop pieces), 3 achievement mounts, Trading Post set recolor.

### Omnium Folio (Sunstrider Omnium) — borrowed power
- Passive buff + 5-node rune talent tree, **not an item**. Unlock via short
  questline (Silvermoon → Magisters' Terrace, Umbric/Rommath), then it's a
  minimap icon; swap freely out of combat.
- **5 weeks to fully unlock** via easy weekly quests: wk1 free · wk2 one
  ritual site · wk3 five void assaults · wk4 a dungeon/delve/LFR boss ·
  wk5 three WQs + world boss in the new mini-zone.
- **Account-wide**: unlock + upgrades apply to all level-90 characters.
- Tree: core rune (Void-Touched Orbs or Unleashed Fire) → defensive choice
  → Rune of Lingering (DoT/HoT echo) → secondary-stat rune (+78 rating) →
  capstone (Overlord +100% core / Residual Energy +100% lingering / Echoes
  50% repeat). PTR values, not ilvl-scaled — expect tuning.
- Full unlock awards a house-decor Omnium (more buyable for Voidlight Marl).

### Ritual Sites: Tier 6 + targeted accolade gear
- **Tier 6** (requires ≥6 challenges active): same Great Vault reward as T5,
  but end-of-run loot adds **Hero AND Myth Dawncrests** plus big Voidlight
  Marl/accolade payouts. New "Ritual Breaker" title for T6 with all 8
  challenges. ⚠ MrGM (tier 3) says the T6 Myth crests "don't seem to be
  capped", but CurrencyTypes DB2 (tier 1, fetched 2026-06-03) shows Myth
  Dawncrest with MaxQty=100 raised via world state (ID 29185) — the same
  weekly-growing-cap structure as Hero. Treat "uncapped" as **unverified**;
  check on live.
- **Slot-specific Hero-track caches for 750 Field Accolades** — replaces
  praying to the 500-accolade random-slot piece. Accolades remain
  NOT warbound (confirmed late PTR).
- **Vendor details (added 2026-06-05, seramate/overgear/masterofwarcraft,
  PTR)**: random **Hero cache price cut 500 → 100 accolades**; new
  slot-specific **Champion cache at 100 accolades, warbound** (single
  tier-4 source — corroborate at patch). Net: post-patch, ~every 100
  banked accolades ≈ one hero roll, 750 ≈ one chosen hero slot —
  banking now is even stronger than previously noted.
  **Banking is safe**: Field Accolade (currency 3405) has MaxQty=0,
  MaxEarnablePerWeek=0, no cap world state in CurrencyTypes DB2 (tier 1)
  — no holding cap and no weekly earn cap.
- Datamined but inactive: new ritual site "Lightbloom" in Harandar (loading
  screen + map only; possibly later in 12.0.7 — ignore until live).

### Timewalking
- **Dragonflight Timewalking** debuts: Algeth'ar Academy, Halls of Infusion,
  Neltharus, Ruby Life Pools, The Azure Vault, Brackenhide Hollow. Vendor:
  2 mounts, unused DF appearances (Fire Druid set, Evoker shoulders),
  3 toys, dragonriding cosmetics, rep tokens.
- **Turbulent Timeways 5: June 30 → Aug 11** (6 weeks — Aug 11 is the
  community guess for 12.1). Weekly TW quest gives a **Heroic Quel'Thalas
  raid piece (285)** each week. "Master of the Turbulent Timeways 5"
  (4 TW dungeons in a row, 5 separate weeks) → **Spawn of Vyranoth** mount.
  - Weekly rotation (warcraft.wiki.gg): DF → BfA → SL → Classic → TBC → DF.
  - **XP buff mechanics**: each TW dungeon completion grants a stack of
    *Knowledge of the Timeways* (+5% XP, 2 hr). At 4 stacks it converts to
    *Mastery of the Timeways* (**+30% XP, 3 hr**). The buff is hours-long,
    not week-long — chain dungeons to keep it up while leveling alts.
    Earning Mastery the first time each week is what ticks the achievement
    (so 4 dungeons/week × 5 separate weeks for the mount).

### Story / smaller features
- One chapter of "Curse of Ul'atek" — the 12.1 campaign opener (troll/elf
  origins, ~1 hr, includes a My'shera Caverns run). 12.1 = Atul'Aman island.
- New Loa lorewalking campaign (Tome of Kings decor) + Jan'alai egg
  questline in Zul'Aman (pet reward). Darkspear Dash microholiday.
- **Moth hunt rebuilt**: Luminous Dust currency **removed entirely**; rewards
  now via quests per 10 moths collected. Existing progress/rewards kept.
- Housing: outdoor lighting (no-overlap restriction), exterior decor caps up
  (300 at house lvl 5–6, 350 at lvl 7+), 100+ new common decor items.
- Big UI pass: Personal Resource Display customization, damage-meter
  visibility/sizing, threat colors, Boss Timeline, Vault tooltip.
- PvP gear ilvls +9 (Galactic Gladiator/Aspirant/Warmonger/crafted).
- Galactic Voidsliver / Galactic Void Matrix **removed**, auto-compensated
  in gold (already applied — nothing to do).
- Prey: new Feat of Strength for completing Preyseeker's Journey.
- XP buffs to Delver's Call / Midnight dungeons / Prey / renown weeklies
  (alt-leveling only; irrelevant at 90).

## What this changes for the next two weeks (until June 16)

**Stop / change now:**
1. **Stop buying 500-accolade random-slot hero pieces — bank Field
   Accolades.** In two weeks, 750 accolades buys a *chosen-slot* Hero-track
   cache. Random pieces are only acceptable value while ~every slot is
   sub-hero; with targeted caches this close, banking wins. (This reverses
   the spend rule in `../characters/encomplete-plan.md`.)
2. **Spend any Luminous Dust at the moth keeper before June 16** — the
   currency is deleted in 12.0.7 (collection progress itself is preserved).
3. Don't over-invest Champion Dawncrests in stopgap pieces that Showdown
   world bosses / 750-caches / Sporefall will replace within 2–3 weeks.

**Keep doing (unchanged value or better):**
- Spark crafts, enchants, gems — 259 crafted gear stays correct and is
  exactly LFR-Sporefall ilvl; nothing in 12.0.7 devalues it.
- Ritual site climbing (T4→T5): crest income now + positions you for T6
  (≥6 challenges) and its **uncapped Myth crest** farm at patch.
- Voidforge + **Nilhammer weekly chain — started now, the 4-week chain
  completes right around patch week**; don't skip a week.
- Delves / Delver's Journey ranks, prey to Preyseeker 4, renown — all
  still the plan; nothing resets at 12.0.7 (it's a mid-season patch, NOT
  Season 2 — vault, crests, catalyst all continue).

**Queue for patch week (June 16):**
1. Unlock **Omnium Folio** day one (5-week ramp; weekly quests overlap
   activities already on the checklist — ritual site, void assaults, delve).
2. Showdown zone unlock questline → world boss kill #1 of 4 (**Myth-track
   item quest**) — weekly-locked, so missing a week delays it.
3. Kill **Rotmire** (LFR at minimum — 259 + Spore Sack mount chance;
   Normal 272 pugs are vault/loot upside).
4. Spend banked accolades on **750 slot-targeted Hero caches** for worst
   slots.
5. From June 30: Turbulent Timeways weekly = **free 285 Heroic raid piece
   every week** — top-tier solo-friendly loot; plan the 5 weeks of "Master
   of the Timeways" for the Spawn of Vyranoth mount.

## Update checklist for patch day (2026-06-16)

- [ ] `game-version.md`: live → 12.0.7, PTR → 12.1 (expected on PTR soon)
- [ ] Verify Omnium Folio rune values/tuning went live as datamined
- [ ] Verify T6 ritual Myth-crest payout and whether it is truly uncapped
- [ ] Verify 750-accolade cache slots/cost and Sporefall ilvls
- [ ] Fold confirmed details into: `../endgame/weekly-checklist.md`,
      `../systems/ritual-sites.md`, `../endgame/raids/overview.md`,
      `../endgame/world-events.md`, `../characters/encomplete-plan.md`
- [ ] Rewrite this file for the next patch (12.1, rumored ~Aug 11)

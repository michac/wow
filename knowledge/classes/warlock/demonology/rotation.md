---
title: Demonology Warlock — rotation & CDM setup (Midnight S1)
patch: 12.0.5
fetched: 2026-06-13
sources:
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-rotation-cooldowns-abilities  # upd. 2026-05-19
  - https://www.method.gg/guides/demonology-warlock/interface-and-macros  # upd. 2026-04-26
  - https://www.kalamazi.gg/guides/addons  # Demo CDM / Edit Mode / Better CDM imports
  - https://wago.io/browse/cooldown-manager/classes/warlock/demonology
  - https://wago.io/mLLnL5_Jt  # KatUI Demonology Warlock COOLDOWN-MANAGER
confidence: medium
---

# Demonology — rotation & CDM (Midnight Season 1)

> Pairs with `builds.md` (talents/gear). Live patch 12.0.5; **Diabolist**
> hero tree assumed for M+.

## Core idea

Demo is a builder/spender pet-army spec. You build **Soul Shards**, spend
them on **Hand of Gul'dan** (summons Wild Imps), and funnel everything
into the **Summon Demonic Tyrant** window (1-min CD), which empowers and
extends every active demon. The single biggest DPS lever is **how many
Hand of Gul'dan casts you fit inside the Tyrant window** — enter it with
demon-generation ready, not starved.

## Single-target priority (12.0.5)

1. **Pre-set your demons** before Tyrant — Dreadstalkers + Grimoire:
   Felguard/Vilefiend out (Diabolist: keeps the demon-ritual procs rolling).
2. **Summon Demonic Tyrant** on CD as the primary cooldown; align it with
   a full board of Wild Imps + Dreadstalkers freshly summoned.
3. **Call Dreadstalkers** on cooldown (refresh just before Tyrant).
4. **Hand of Gul'dan at 4–5 Soul Shards** — never overcap shards; this is
   your imp generator and the thing you maximize in the Tyrant window.
5. **Demonbolt (or Infernal Bolt if talented) with 2+ Demonic Core stacks**
   — spend cores so they don't overcap.
6. **Power Siphon** with ≤2 Demonic Core stacks and 2+ Wild Imps up
   (converts imps → cores to fuel the next Hand of Gul'dan).
7. **Filler:** Shadow Bolt / Infernal Bolt to rebuild shards.

**Tyrant window rule:** go in with **2+ Demonic Core charges** so you can
chain Hand of Gul'dan fast and pump the summon count over the duration.

## AoE / Mythic+ priority

The priority is **largely the same** across target counts — Demo is a
"passive cleave" spec; your demons hit everything. The one big addition:

- **Implosion at 6 Wild Imps** for cleave — sacrifices imps for burst AoE.
  On heavy multi-target this beats letting imps keep auto-attacking. On
  pure ST, only Implode if talented into **To Hell and Back** (otherwise
  let imps live).
- **Diabolist** front-loads burst via **Overlord / Pit Lord** ritual
  summons inside Tyrant — pop your big AoE on the pull/Tyrant overlap.
- Hold **Tyrant** a few seconds for the pull to connect rather than
  wasting it on one target.

## CDM (Cooldown Manager) setup — Midnight

The built-in **Cooldown Manager** (Blizzard's CDM, expanded in Midnight)
plus the **Better Cooldown Manager** addon are the standard combo. What to
track for Demo (Method, 2026-04-26):

- **Soul Shards** (resource — gates your whole rotation)
- **Demonic Core** procs/stacks (your Demonbolt/Infernal Bolt trigger)
- **Dreadstalkers / Grimoire (Felguard·Vilefiend) / demon durations**
- **Summon Demonic Tyrant** cooldown
- **Diabolist rituals & secondary effects** (Overlord/Pit Lord/Art procs)
- Cast bar + player/target frames

### Ready-made imports (copy-to-clipboard / wago)

- **Kalamazi addons page** has three Demo imports: **"Demonology CDM"**,
  **"Demonology Edit Mode"**, and **"Demonology Better Cooldown Manager
  (Addon)"** — https://www.kalamazi.gg/guides/addons (most current; matches
  the M+ build in `builds.md`).
- **wago.io Demo cooldown-manager browse:**
  https://wago.io/browse/cooldown-manager/classes/warlock/demonology
- **KatUI Demonology Warlock — COOLDOWN-MANAGER:** https://wago.io/mLLnL5_Jt

> Import strings are copy-button/JS-gated on those pages, so they're not
> cached here — grab them live in-game. Verify the profile's patch tag is
> **12.0.x / Midnight** before importing.

## Useful macros (Method)

- Drain Life + `/cancelaura Burning Rush` (don't bleed out while channel-healing)
- `/cast [@focus] Axe Toss` (Felguard interrupt on focus)
- Mouseover cast variants
- `/cast [@cursor] Shadowfury` (instant AoE stun placement)

## TODO

- [ ] Re-verify vs **12.0.7** (2026-06-16) — confirm Demonbolt vs Infernal
      Bolt filler choice and any Tyrant-window tuning.
- [ ] Capture an actual CDM import string into the KB if one becomes
      cacheable (currently behind copy buttons on Kalamazi/wago).

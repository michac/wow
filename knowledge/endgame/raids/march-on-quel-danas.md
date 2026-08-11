---
title: March on Quel'Danas (Raid — Midnight Season 1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - Blizzard Game Data API, journal-instance/1308 (tier 1)
  - Warcraft Logs zone 46 (tier 2)
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281 (tier 1, 12.1 "Curse of Ula'tek" content update notes)
  - https://www.icy-veins.com/wow/midnight-falls-raid-guide (tier 3)
  - https://www.wowhead.com/guide/midnight/raids/march-on-quel-danas-midnight-falls-boss-strategy-abilities (tier 4)
confidence: high
---

# March on Quel'Danas

Two-boss Midnight Season 1 raid. Journal instance **1308**.

> Journal blurb: "Darkness has eclipsed the Isle of Quel'Danas, clouding the
> skies above Silvermoon City. With Arator the Redeemer by their side, the
> Champions of Azeroth must march on the Sunwell before the light of the
> blood elves is lost forever."

Available in **Raid Finder / Normal / Heroic / Mythic**. Weekly lockout.

> **Status as of 12.1 "Curse of Ula'tek" (live 2026-08-11):** this is a
> **previous-tier** raid. Season 1 ended with the week of Aug 11 maintenance;
> **The Venomous Abyss** (Coiled Isle, 8 bosses) becomes the current-tier raid
> when **Midnight Season 2 opens 2026-08-18**. During the Aug 11 pre-season week
> no new raid is open.
>
> **No instance-specific encounter tuning for this raid appears in the 12.1
> notes** — the boss mechanics and the 12.0.7 tuning below still stand as
> written. But 12.1 is not a no-op here: two game-wide changes reach this
> instance like every other.
>
> - **The +25% pass.** Player health and creature damage were both increased
>   **25% at max level**, with health-consumable values rescaled and encounter
>   abilities hand-tuned alongside. So absolute damage/HP numbers from a
>   Season-1 log or guide no longer read across, even though nothing about this
>   raid was singled out. (12.1 also lowered several specs' major DPS cooldowns
>   while raising steady-state damage, added a "missed" interrupt visual, and
>   moved DR-category reset to 20 s from 16 s.)
> - **Raid Great Vault tracks.** 12.1 moved LFR / Normal / Heroic raid vault
>   rewards to **the first step of the next harder difficulty's track** (Heroic
>   → Myth 1/6) and Mythic raid vault rewards to **Myth 6/6**. The notes state
>   this for raid vault rewards generally and **do not scope it to the current
>   tier**, so it most likely applies to this raid's vault slot too —
>   ⚠ *not separately confirmed for a previous-tier raid; verify before relying
>   on it.* See `endgame/great-vault.md`.
>
> The instance-specific 12.1 change is the vendor move below.

## 12.1 — Kirana no longer stands at the entrance

The **class set vendor Kirana** has **relocated away from the March on
Quel'Danas raid entrance** to **near the Catalyst in Silvermoon**, and her stock
now also includes **Midnight Season 2 class set armor** in exchange for
**Slumbering Coil Curios**. Don't fly out to Quel'Danas for class-set pieces —
see `endgame/catalyst.md`.

## Bosses (journal order)

| # | Boss | Journal enc. | WCL enc. |
|---|------|--------------|----------|
| 1 | Belo'ren, Child of Al'ar | 2739 | 3182 |
| 2 | Midnight Falls (L'ura) | 2740 | 3183 |

## Midnight Falls (L'ura) — final boss

Three-phase fight (with an intermission) against L'ura, the void-corrupted
naaru, beneath the eclipsed Sunwell.

- **Phase 1 — Memory Game + adds.** Symbols appear in sequence next to the
  boss; marked players must line up in that order as a rotating beam (Dark
  Quasar) sweeps. Manage **Termination Prism** adds (interrupt/CC),
  **Heaven's Glaives** bouncing projectiles, and **Heaven's Lance** — tanks
  swap after the stack applies **Impale** (5 stacks). DPS grip/kill **Midnight
  Crystals**; healers top off **Dusk Crystals** before **Cosmic Fracture**
  resolves. Healed Dusk Crystals become **Dawn Crystals** — assign carriers
  for Phase 3.
- **Intermission.** Straight-line Dark Quasar beams plus **Starsplinter**
  spread; healing absorbs go out on the raid.
- **Phase 2 — void cores.** ~12 **Void Cores** rotate the room; designated
  players aim **Galvanize** beams at them, triggering **Cosmic Fission** pulls;
  remaining cores get dragged in by **Core Harvest**.
- **Phase 3 — darkness.** Environmental ticking damage; **Dark Constellation**
  orbs form beam connections (kept clear of **Light Siphon** soak pools), and
  Dawn-Crystal holders pop shields against **The Dark Archangel** cone.

Mythic Midnight Falls drops **Season 1 ilvl 282** gear (S1 Myth Dawncrest band
276–289). ⚠ Don't misread this as a Season 2 number — 282 is coincidentally also
the Season 2 Adventurer/Veteran **Mistcrest** boundary (S2 runs 269 → 334).

## 12.0.7 "Revelations" tuning — Midnight Falls

Patch 12.0.7 (live 2026-06-16) applied a broad set of Mythic/Heroic nerfs to
this boss, plus an earlier 5/19 hotfix pass on Mythic damage/mechanics.

- **Glimmering** damage reduced **20%** on Mythic.
- **Criticality** cast time increased **3 → 4 s**.
- **Dark Constellation** cast time **2.5 → 3 s** on Mythic, and now spawns
  further away from Light Siphons.
- **Radiance** damage reduced **50%** on Heroic.
- **Tears of L'ura** now spawns **1 soak** on Heroic (down from 2).
- **Resonance** no longer triggers **Tears of L'ura**.
- **Starsplinter** can no longer target the same player multiple times
  simultaneously.
- Midnight and Dusk Crystal spread reduced.
- Dawn Crystals begin pulsing Radiance after **6 s** on Heroic and Mythic
  (was 5 s).

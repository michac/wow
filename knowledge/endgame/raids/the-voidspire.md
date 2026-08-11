---
title: The Voidspire (Raid — Midnight Season 1, previous tier as of 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - Blizzard Game Data API, journal-instance/1307 (tier 1)
  - Warcraft Logs zone 46 (tier 2)
  - https://worldofwarcraft.blizzard.com/en-us/news/24276957/hotfixes-june-18-2026 (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29731810 (tier 1, hotfixes 2026-07-07)
  - https://worldofwarcraft.com/en-us/news/24293281 (tier 1, 12.1 "Curse of Ula'tek" content update notes)
  - https://us.forums.blizzard.com/en/wow/posts/29833350 (tier 1, Season 1 ending / Season 2 information)
confidence: high
---

# The Voidspire

Main Midnight Season 1 raid — 6 bosses. Journal instance **1307**.
Difficulties: LFR / Normal / Heroic / Mythic.

> ⚠ **Previous tier as of patch 12.1 "Curse of Ula'tek" (live 2026-08-11).**
> Season 1 ended with that week's maintenance and **The Venomous Abyss** (Coiled
> Isle, 8 bosses) is the Season 2 raid, opening **2026-08-18**. The Voidspire is
> still fully enterable at every difficulty — the encounters are unchanged — but
> it is no longer current-tier content. See the "12.1 status" section below for
> what did change *around* it.

## Bosses (journal order)

| # | Boss | Journal enc. | WCL enc. |
|---|------|--------------|----------|
| 1 | Imperator Averzian | 2733 | 3176 |
| 2 | Vorasius | 2734 | 3177 |
| 3 | Vaelgor & Ezzorak | 2735 | 3178 |
| 4 | Fallen-King Salhadaar | 2736 | 3179 |
| 5 | Lightblinded Vanguard | 2737 | 3180 |
| 6 | Crown of the Cosmos (Alleria) | 2738 | 3181 |

(WCL encounter IDs are what `wowkb.wcl rankings` takes.)

## 12.1 status (live 2026-08-11)

**The instance itself is unchanged** — still 6 bosses, LFR / Normal / Heroic /
Mythic, journal instance **1307**. The 12.1 notes contain no Voidspire encounter
tuning or structural change. What changed is its *context*:

- **Season 1 is over.** Competitive PvP ended 22:00 the night before regional
  maintenance; Season 1 Mythic+ and the raid feats of strength stayed obtainable
  **until maintenance began** the week of Aug 11. So **Cutting Edge: Crown of the
  Cosmos** and the Season 1 **Ahead of the Curve** are no longer obtainable.
- **Nebulous Voidcore bonus rolls no longer work here.** Season 1 Voidcores
  **convert to gold** at the end of Season 1 and can no longer be spent on Season 1
  content — which includes every Voidspire encounter. (From Season 2 they return as
  a Great Vault reward, at a raid re-roll cost of **1**, but for Season 2 content.)
- **Story continues from it.** After Season 2 starts, Arator returns to deal with
  the **fallout from the Voidspire** and the resurgence of the **Twilight's Blade**,
  continuing the hunt for Xal'atath. That's new questing content, not a raid change.

## 12.0.7 status & hotfixes

No structural changes in 12.0.7 "Revelations" (live 2026-06-16): still 6 bosses,
LFR / Normal / Heroic / Mythic, journal instance **1307**. All recent Voidspire
changes are bug-fix hotfixes (no encounter retuning beyond the May 5 Crown of the
Cosmos / Alleria Mythic nerfs noted below):

- **Jul 7** — *Lightblinded Vanguard:* fixed the boss respawning after a soft
  reset when the raid skip had been used.
- **May 15** — A teleport pad now appears on the Isle of Quel'Danas for raid
  groups that used the raid shortcut and still have bosses remaining.
- **May 15** — *Fallen-King Salhadaar:* fixed the **Broken Oath** warning being
  unmovable in Edit Mode.
- **May 8** — Using the raid skip no longer auto-teleports players when returning
  to the entrance.
- **May 6 / May 8** — Fixed players being unable to teleport to **The Approach**
  after the instance was soft reset.
- **May 5** — *Crown of the Cosmos (Alleria):* multiple Mythic nerfs to Alleria
  and her minions (health, energy generation, ability targeting).

These match the ledger's "telepad / Salhadaar warning / teleportation fixes."

## TODO

- [ ] Loot ilvls per difficulty; tier tokens; very rares — *still open after the
      12.1 sweep. Neither `patch-notes/12.0.5.md`, `12.0.7.md` nor `12.1.md`
      states a Voidspire ilvl band (12.0.7 gives one only for Sporefall,
      259–298), and `moving-values.md` carries no Voidspire row. Verify against
      wago.tools / Blizzard API rather than editorial prose. Lower priority now
      that the raid is previous-tier.*
- [ ] Per-boss strategy summaries — source: Icy Veins raid guide
- [ ] Confirm 3↔4 boss order in-instance (journal lists Vaelgor & Ezzorak
      before Salhadaar; guide sources implied otherwise)

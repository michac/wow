---
title: The Blinding Vale — Midnight S2 M+ dungeon guide (day-1 stub)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.api.blizzard.com/data/wow/journal-instance/1309  # Blizzard journal-instance/1309 (tier 1) — instance, location, boss roster, difficulties
  - https://us.api.blizzard.com/data/wow/journal-encounter/2769  # Lightblossom Trinity (tier 1, Adventure Guide)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2770  # Ikuzz the Light Hunter (tier 1, Adventure Guide)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2771  # Lightwarden Ruia (tier 1, Adventure Guide)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2772  # Ziekket (tier 1, Adventure Guide)
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369  # Midnight Season 2 overview (tier 1) — the S2 M+ pool
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281  # 12.1 Content Update Notes (tier 1) — S2 rotation list
confidence: medium
---

# The Blinding Vale — Midnight Season 2 Mythic+

> 🌱 **DAY-1 STUB (written 2026-08-11, the day 12.1 went live).** Everything below
> comes from **Tier-1 game data** — the Blizzard journal (Adventure Guide) at build
> `12.1.0_68914` — plus the Tier-1 Season 2 announcements. What is **missing** is
> everything that only exists after people run it as a keystone: **route/pull order,
> trash tables, kick priorities, affix interactions, tuning, and M+ loot ilvls**.
> Nothing of that kind has been invented here. Tier-3 guides (Method / Icy Veins)
> had not published Season 2 dungeon guides at the time of writing — see `## TODO`.

> ⏳ **Pre-season, week of 2026-08-11:** The Blinding Vale is in the Season 2 pool but
> **Mythic+ is not open yet**. This week it is playable at Normal / Heroic / **Mythic 0
> on a weekly lockout** (M0 drops Champion 1/6, ilvl 292). **Keystones begin dropping
> the week of 2026-08-18**, when M0 returns to a daily lockout. See
> [season-2-overview.md](season-2-overview.md).

A Midnight-expansion dungeon in **Harandar** that **sat out Season 1** — this is its
**first Mythic+ appearance**. Four bosses. The theme is the **Lightbloom**: after its
defeat in Eversong, the Lightbloom took root in the Vale, and the rutaani it infests
cultivate a garden that grows new creatures and magic to serve one imperative —
"growth unstoppable" (journal-instance/1309 description).

Difficulties tracked by the journal: Normal / Heroic / Mythic (5-player) plus the
Mythic Keystone mode. A **Follower Dungeon** version exists (Midnight follower pool)
— useful for learning the layout blind, not for affix or tuning practice.

## Route

**Not yet written.** No verified route exists on day 1 — pull order, skips and
trash packs need either a live run or a Tier-3 guide (see `## TODO`). Boss order as
listed by the Adventure Guide is:

1. **Lightblossom Trinity** (`enc:2769`)
2. **Ikuzz the Light Hunter** (`enc:2770`)
3. **Lightwarden Ruia** (`enc:2771`)
4. **Ziekket** (`enc:2772`)

## Trash

**Not yet written.** The journal names only boss-linked creatures (Bloodthorn Roots
under Ikuzz, Lightspawn Lasher under Ziekket); it does not enumerate trash packs or
their abilities, and guessing them would be invention.

## Bosses

Consequence tiers: 🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor.

⚠️ **Ability rows below are the Adventure Guide's own text**, condensed. The
"Archetype" and "Tier" columns are **provisional** — assigned by reading the journal
description against the
[mechanic-archetype taxonomy](../../systems/mechanic-archetypes.md), **not** from
watching the fight. Re-check both columns after a live run before feeding them to
`mplus_memory`.

### Lightblossom Trinity <!-- enc:2769 -->

**Hint:** block the beams, share the damage

A trio of Lightbloom rutaani — **Meittik**, **Lekshi** and **Kezkitt** — working in
tandem to sow a Lightblossom garden. **Damage taken is shared between all three**
(Thicket's Trinity), so they die together. The core loop: Meittik creates **Fertile
Loam**, Lekshi plants it with **Lightsower Dash**, Kezkitt germinates the resulting
**Lightblossoms** with **Lightblossom Beam** until they burst.

| Ability | Source | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Thicket's Trinity** | all three | Damage taken is **shared between the trio** — cleave/AoE is the whole damage plan | balance-kill | 🔵 | all |
| **Lightblossom Beam** | Kezkitt | Rays that germinate the Lightblossoms; the blossoms gain stacking **Light-Gorged** **unless the rays are blocked** | positional-gimmick | 🔴 | all |
| **Lightbloom Overgrowth** | Lightblossom | Blossoms burst — damage **scales with the number of Light-Gorged applications**; leaves **Light-Scorched Earth** | raid-damage; ground-void-zone | 🔴 | healer |
| **Bedrock Slam** | Meittik | Hits the current target and creates patches of **Fertile Loam** near their location | tank-buster | 🟠 | tank |
| **Fertile Loam** | Meittik | The ground patches Lekshi's dash plants blossoms into | ground-void-zone | 🔵 | all |
| **Bedrock Surge** | Meittik | Periodic damage to **all** players | raid-damage | 🔵 | healer |
| **Lightsower Dash** | Lekshi | Dashes across the loam, planting **Lightblossoms** | positional-gimmick | 🟠 | all |
| **Thornblade** / **Fan Of Thorns** | Lekshi | Random players **bleed for high damage** | raid-damage; dispel | 🔵 | healer |
| **Light Bolt** | Kezkitt | Bolt cast at players _(no journal detail — cast type unconfirmed)_ | interruptible-cast? | ⚪ | all |

**The mechanic that decides the pull:** Light-Gorged only stacks while the beams
reach the blossoms, and Lightbloom Overgrowth's damage is a function of those stacks.
Blocking beams is a group job. *(Whether "blocked" means body-blocking the ray or
killing the blossom first is not stated by the journal — confirm live.)*

### Ikuzz the Light Hunter <!-- enc:2770 -->

**Hint:** break the roots, then run the gaze

A carnivore of Harandar, now Light-maddened. He roots players in place, then at
**100 energy** fixates one of them.

| Ability | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|
| **Bloodthorn Roots** | Entangles players and **immobilizes them until the roots are destroyed** (they are targetable creatures) | kill-priority-add | 🟠 | all |
| **Bloodthirsty Gaze** | At 100 energy he **fixates a player**; that player is **Incised** if Ikuzz reaches their location | fixate-chase | 🔴 | all |
| **Incise** → **Crunched** | The payoff of the gaze — **high damage** to the caught player | fixate-chase | 🔴 | all |
| **Crushing Footfalls** | Damage along his path during the gaze | ground-void-zone | 🟠 | all |
| **Thorncaller Roar** | **Channels Nature damage on all players** | raid-damage | 🔵 | healer |
| **Verdant Stomp** | Stomp _(no journal role callout)_ | raid-damage | 🟠 | all |
| **Lightcrazed Frenzy** | _(listed by the journal with no description)_ | flavor | ⚪ | all |

**The mechanic that decides the pull:** the roots + the gaze overlap by design — a
rooted player cannot kite the fixate. Free the target first.

### Lightwarden Ruia <!-- enc:2771 -->

**Hint:** two forms, then everything at once

Formerly **Root**warden Ruia; he took Lightbloom power after failing to beat it and
now punishes everyone with it. He **shapeshifts between Moonkin and Bear forms**, and
at **40% remaining health** returns to **Haranir form** and channels **Spirits of the
Vale**, casting **all of his abilities in a rapid flurry**.

| Ability | Form | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Spirits of the Vale** | Haranir (≤40%) | Channel that fires his **whole kit in a rapid flurry** — the burn/execute phase | burn-window | 🔴 | all |
| **Lightfire** → **Lightfire Beams** | Moonkin | Beams across the arena | ground-void-zone | 🟠 | all |
| **Lightfall** | Moonkin | **High damage to players within each impact** | ground-void-zone | 🔴 | all |
| **Warden's Wrath** | Moonkin | **Replaces his melee attacks** while in Moonkin form | tank-buster | 🔵 | tank |
| **Pulverizing Strikes** → **Pulverized** | Bear | Launches a **cone of Physical damage at each target** | frontal-cone | 🟠 | all |
| **Grievous Thrash** | Bear | Bleed that is **only removed when the afflicted player reaches full health** | heal-absorb | 🔵 | healer |
| **Mangling Claws** | Bear | Melee-form attack _(no journal detail)_ | tank-buster | 🔵 | tank |

**The mechanic that decides the pull:** Grievous Thrash does not fall off on a timer —
it stays until the target is topped, so it stacks with everything else the healer is
handling. Save cooldowns for the 40% flurry.

### Ziekket <!-- enc:2772 -->

**Hint:** feed the beam to the dormant lashers

The Lightbloom's own spawn, incubated at the epicenter. Periodically **Awakens the
Lightbloom** — sprouting new **Lightspawn Lashers** and waking any **Dormant** ones —
while projecting a **Concentrated Lightbeam** that annihilates whatever it crosses.

| Ability | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|
| **Awaken the Lightbloom** | Summons a **thicket of Lightspawn Lashers** and wakes **Dormant** ones | kill-priority-add | 🔴 | all |
| **Concentrated Lightbeam** | Beam projected at players; it **vaporizes Dormant Lightspawn Lashers into Lightsap** | positional-gimmick | 🔴 | all |
| **Lightspawn Lasher** kit | **Lightspore Shot**; **Dormant**; **Vicious Regrowth** | kill-priority-add | 🟠 | all |
| **Lightbloom's Essence** | Globules — touching one **inflicts Holy damage but increases your damage and healing done** (→ **Fluorescent Outburst** / **Fluorescent Shield** / **Lightbloom's Might**) | soak | 🔵 | all |
| **Oozing Xylem** | **Continual Holy damage to all players** | pulsing-aura | 🔵 | healer |
| **Thornspike** | **Impales Ziekket's current target** | tank-buster | 🟠 | tank |

**The mechanic that decides the pull:** the beam is a tool, not just a threat — line
it up on **Dormant** Lashers to delete them, and pick up **Lightbloom's Essence** for
the damage/healing buff if you can afford the Holy damage.

## DPS notes (you are DPS)

Deliberately thin on day 1 — these follow from the journal text alone:

- **Trinity is a cleave fight**, not a priority-target fight: damage is shared across
  all three rutaani, so AoE everything and spend the attention budget on blocking
  **Lightblossom Beam** rays instead.
- **Add control is the through-line** — Bloodthorn Roots (frees a rooted ally),
  Lightspawn Lashers (Ziekket). Hold a stop/burst for them.
- **Ruia's 40% flurry** is the one scripted burn window in the dungeon; bank
  cooldowns for it.
- **Ziekket's Lightbloom's Essence** is an optional personal damage buff paid for in
  Holy damage — a DPS decision, not free value.

## Rewards

No dungeon-specific loot claims here on day 1. Mythic 0 drops **Champion 1/6 (292)**
and the M+ end-of-run / vault ladder lives in [loot.md](loot.md) and
[../great-vault.md](../great-vault.md); Season 2 upgrade currency is **Mistcrests**
(see [../dawncrests.md](../dawncrests.md)). The journal does list a per-boss item
table for the dungeon, but item levels there are the Normal/Heroic values, not M+ —
capture it properly once the season is running.

## TODO

- [ ] **Route + trash tables.** Fetch Method (`method.gg/guides/dungeons/…`) and Icy
      Veins Blinding Vale guides once Season 2 guides publish (expect on/after
      2026-08-18), the way `skyreach.md` was built. Do **not** write a route from
      memory or from the follower dungeon alone.
- [ ] **Confirm what "blocking" Lightblossom Beam means** on Lightblossom Trinity
      (body-block the ray vs. kill the blossom) — this is the fight's core mechanic.
- [ ] **Confirm the archetype + consequence tags** against a live run before feeding
      them into `systems/mechanic-archetypes.md` / the `mplus_memory` pipeline; they
      are journal-derived inference today.
- [ ] **Interrupt list.** The journal exposes no cast/interrupt flags; Kezkitt's
      **Light Bolt** in particular is unconfirmed as interruptible.
- [ ] **Warcraft Logs encounter IDs** for the four bosses, once the S2 zone exists.
- [ ] **Per-boss loot** at M+ ilvls once keys are running.

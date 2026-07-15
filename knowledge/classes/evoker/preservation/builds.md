---
title: Evoker Preservation — talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/preservation-evoker/talents  # tier 3, 2026-07-11 — build + import strings
  - https://maxroll.gg/wow/class-guides/preservation-evoker-mythic-plus-guide  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/preservation-evoker-raid-guide  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/preservation-evoker-pve-healing-guide  # tier 3, 2026-07-11
  - knowledge/classes/evoker/preservation/talents.md  # tier 1 tree structure (Blizzard API + wago @ 12.0.7.67808)
confidence: medium
---

# Evoker Preservation — talents & builds (Midnight S1, 12.0.7)

Layered on top of the generated **`talents.md`** (the full 12.0.7 tree from
Blizzard API + wago). This file is the *narrative*: which hero tree, which
loadouts, and why. The tree structure there is Tier-1; the build opinions here
are Tier-3 (method / maxroll / Icy Veins, all 12.0.7). No Tier-1 simc talent
string exists for a healer spec.

> **Midnight removal:** **Spiritbloom**, **Emerald Communion**, and **Engulf**
> were **removed from Preservation this patch** (maxroll, 12.0.7). The old
> "one-button heal-everyone" burst is gone; the spec now leans harder on the
> Echo → Merithra's Blessing / Verdant Embrace ramp. @verify-ingame

## Hero tree: Chronowarden (default everywhere)

**Chronowarden** is the recommended pick for **both raid and Mythic+**. It makes
**Tip the Scales** a genuine throughput cooldown through **Temporal Burst** (haste
+ move speed + cooldown-recovery-rate), and **Chronoboon** shortens Tip the
Scales' CD so you press it far more often. The extra haste from **Primacy** tightens
the **Temporal Anomaly** cooldown loop, and **Reverberations** amplifies Verdant
Embrace healing. Overall a more deliberate, cooldown-planned playstyle with the
higher ceiling.

**Flameshaper** is a viable alternative, best at **+11 and lower keys**: it leans
into **Dream Breath / Fire Breath** breath interactions for steadier sustained
group HoT healing that can be converted to targeted burst. Simpler, lower ceiling.

## Recommended loadouts (12.0.7, method.gg)

> Import strings are tree-version-sensitive; **confirm they load as the right hero
> tree in-game** before trusting. Re-verify if the tree changes in a later patch.

- **Raid (Chronowarden):**
  `CwbBAAAAAAAAAAAAAAAAAAAAAAAAAAAYmZ2WmHADzMmNjZmZWmxAAAzYGDmxMyMzAAAAMzMTmxMjZbmZAwAjZsxCMwMaoBsAjZGgxA`
- **M+ advanced +12 (Chronowarden):**
  `CwbBAAAAAAAAAAAAAAAAAAAAAAAAAAAMzMz22YGDzMmNzYM2GGAAGzYGzYMMTMmBAAAMzMTzYmZmxYGAAGzYjFYgZ0QDYBGzMAjB`
  (includes **Energy Loop** for mana + situational utility.)

## Core mandatory talents (all builds)

From the spec tree (see `talents.md` for IDs / positions):

- **Unshakable**, **Spiritual Clarity** (choice vs Empath) — foundation.
- **Call of Ysera** — buffs Dream Breath / Living Flame healing.
- **Temporal Anomaly** + **Nozdormu's Teachings** (advanced choice-node pick) —
  the Echo-blanket engine; Nozdormu's reduces breath CDs for skilled play.
- **Grace Period** — extends Reversion duration (Reversion synergy).
- **Golden Hour** — amps Reversion / post-damage healing.
- **Time Lord** — throughput/EHP passive.
- **Twin Echoes** — "one of the main talents the spec revolves around"; lets an
  Echo apply a **second** Echo to the lowest-health ally (free healing). Triggered
  by **Emerald Blossom** (and by **Verdant Embrace** with the tier 4-piece).
- **Timeless Magic** — extends buff durations.
- **Merithra's Blessing** (apex) — the bouncing burst-heal finisher; procs from
  Essence spends + Dream Breath and drops Reversion on echoed targets.
- **Spark of Insight** — Essence Burst procs from breath abilities (feeds the
  Merithra's Blessing proc frequency).
- **Field of Dreams**, **Lifebind** (Verdant Embrace's echo-heal), **Fluttering
  Seedlings** — throughput passives on the AoE side.

## Key interactions

- **Echo + Twin Echoes:** Emerald Blossom → buff → next Echo applies an *extra*
  Echo to the lowest-health ally = free duplicated healing. Bank up to **2 Twin
  Echoes charges**; when at 2, spend Essence Burst on **Echo** rather than Emerald
  Blossom so you don't waste them.
- **Reversion cluster:** Grace Period (duration) + Golden Hour + Merithra's
  Blessing all key off Reversion — hence "double Reversion on the tank."
- **Essence economy:** Spark of Insight (breaths → Essence Burst) + Reversion /
  Living Flame procs feed free Emerald Blossoms / Echoes → more Merithra's procs.
- **Temporal Anomaly → Dream Breath:** Temporal Anomaly reduces Dream Breath CD
  (and Nozdormu's Teachings reduces breath CDs further) — the Chronowarden CD loop.

## Mana / utility swaps

- **Mana trouble:** replace **Dream Simulacrum** or **Temporal Artificer** with
  **Energy Loop**; then weave **Disintegrate** to spend surplus Essence for mana.
- Choice nodes to tune to content: **Dream Flight / Stasis** (big raid vs planned
  burst), **Time Spiral / Spatial Paradox** (raid mobility vs external empower
  enabler), **Empath / Spiritual Clarity**, **Delay Harm / Just in Time**.

## Class-tree utility (always relevant)

Cauterizing Flame + Naturalize/Expunge (dispels), Zephyr, Time Dilation, Rescue,
Source of Magic, Obsidian Scales / Renewing Blaze / Panacea (survivability),
Sleep Walk / Landslide / Oppressing Roar (CC), Blessing of the Bronze, Hover /
Aerial Mastery (mobility). See `talents.md` for the full class-tree node list.

## TODO

- [ ] Add stat priority, enchants, gems, consumables, and crafted/embellishment
      meta (Icy Veins / method gearing pages) — this file is talents-only so far.
- [ ] Capture a Tier-1 talent export once a healer sim/loadout source exists;
      current strings are Tier-3 (method). Verify hero tree on import. @verify-ingame
- [ ] Confirm tier-set bonuses (Verdant Embrace → Twin Echoes 4pc) against 12.0.7
      set data.

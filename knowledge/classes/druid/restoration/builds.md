---
title: Restoration Druid — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/restoration-druid/talents  # tier 3, 12.0.7 (upd 2026-06-16) — import strings + hero-tree calls
  - https://www.method.gg/guides/restoration-druid/playstyle-and-rotation  # tier 3, 12.0.7 — interactions
  - https://www.icy-veins.com/wow/restoration-druid-pve-healing-guide  # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/restoration-druid-mythic-plus-guide  # tier 3, 12.0.7
  - https://wowlazymacros.com/t/mob-s-druid-restoration-wildstalker-mythic-keeper-of-the-grove-raid-midnight-12-0-complete-revamp-4-12-2026/61453  # tier 4, 2026-04-12 — hero-tree assignment contrast
  - knowledge/classes/druid/restoration/talents.md  # tier 1 game-data tree (Blizzard API + wago, build 12.0.7.67808)
confidence: medium
---

# Restoration Druid — Talents & Builds (Midnight Season 1)

> Layer this on top of `talents.md` / `talents.json` (the Tier-1 game-data
> tree). Below is the *narrative* — which nodes matter and why — sourced from
> Tier-3 guides. **No Tier-1 SimC APL/profile exists for a healer spec**, so
> the loadouts here are guide-recommended rather than sim-optimized; confidence
> **medium.** Import strings are from method.gg (12.0.7) — one bad character
> breaks an import, so **confirm the hero tree loads correctly in-game**.

## Hero tree — which and where (CONTESTED)

Both hero trees are competitive in S1; **sources disagree on which content
each is best in**, so this is a genuine split to verify against your own logs:

- **method.gg (talents page, upd 2026-06-16):** **Wildstalker for raid**
  (Symbiotic Blooms amplify regular healing; higher throughput ceiling) and
  **Keeper of the Grove for Mythic+** (well-rounded, cooldown reduction, the
  *Protective Growth* defensive).
- **Other sources (wowlazymacros "Mob's Druid" 2026-04-12; and method's own
  Playstyle page framing):** the reverse — **Keeper of the Grove for raid**
  (the reliable Grove-Guardian engine, lower APM) and **Wildstalker for M+**
  (cat-weaving damage while dungeon healing is lighter).

@verify-ingame — resolve against current WCL/Archon representation for your
content; the two trees play very differently regardless of label:

- **Keeper of the Grove** — Grove Guardians tied to Swiftmend/Wild Growth,
  each active guardian +5% healing (to +25%); Convoke can field 5 at once;
  *Cenarius' Guidance* cuts Convoke to ~1 min; *Protective Growth* defense.
  Lower APM, forgiving, strong reliable output. Default with **Incarnation:
  Tree of Life**.
- **Wildstalker** — *Symbiotic Blooms* from Wild Growth / Regrowth /
  Efflorescence buff your normal healing (*Vigorous Creepers*, *Bursting
  Growth*), plus a cat-weaving damage loop (Moonfire/Sunfire → Cat Form
  finishers, empowered by *Heart of the Wild*). Higher ceiling + higher APM.
  Default with **Convoke the Spirits**.

## Spec-tree core (both builds)

The recurring engine, independent of hero tree:

- **Abundance** — each active Rejuvenation lowers Regrowth cost 8% and adds 8%
  crit, to **+96%** at ~12 stacks. The single most important interaction: it
  turns a wide Rejuv bed into cheap, near-guaranteed-crit Regrowth spot heals.
- **Soul of the Forest** — Swiftmend empowers the next Rejuv/Wild Growth.
  Pairs with **Power of the Archdruid** so that empowered Rejuv copies to 2
  extra allies. This is why **Swiftmend is cast on cooldown**.
- **Everbloom (apex)** — Lifebloom auto-stacks up to 3 and blooms for AoE;
  consuming a Soul of the Forest makes Lifebloom **bloom 3× in rapid
  succession**. Big burst-healing multiplier off the maintenance kit.
- **Omen of Clarity / Clearcasting** — periodic heals proc a free Regrowth;
  the Regrowth-spam economy runs on this + Abundance.
- **Incarnation: Tree of Life ↔ Convoke the Spirits** — the major-cooldown
  choice node; pick per hero tree (see above).
- **Inner Peace ↔ Flourish** — Flourish (HoT extension) is the ramp-stretching
  pick; Inner Peace gives Tranquility −20% damage taken. Tranquility applies
  Flourish in 12.0 regardless.
- **Efflorescence** + **Lifetreading** (auto-moves the zone to the Lifebloom
  target) — cheap sustained AoE once placed.
- Throughput passives seen in both builds: **Cultivation**, **Photosynthesis**,
  **Reforestation**, **Harmonious Blooming**, **Verdancy**, **Nature's
  Bounty**, **Intensity** (Regrowth crits hit harder), **Germination** (2×
  Rejuv per target), **Improved Wild Growth**, **Grove Guardians** (Keeper).
- **Master Shapeshifter** — damage spells (Wrath/Moonfire/finishers) return
  mana; the reason downtime DPS is baked into the kit (and mandatory for
  Wildstalker weaving).

## Recommended loadouts (method.gg, 12.0.7)

**Raid — Wildstalker (method.gg talents):**
```
CkGAAAAAAAAAAAAAAAAAAAAAAMjxMbz2MmZGz2wDwMzmxCzAAAAAAAAAAgNoZzMmmZgxsMzMzMMMDAAAAAAAAAgAAAmtZWa2mZzGjZmhZGY0MAAzMAMA
```

**Mythic+ — Wildstalker (method.gg talents):**
```
CkGAAAAAAAAAAAAAAAAAAAAAAMMmZZMjZmxsN8AMzswsYbGAAAAAAAAAAsMoZbGmmZM8AmFzMzYZm8AGAAAAADAwMAAAAAY2mZbmlZWsxMzAzMLgmBAYmBgB
```

> method.gg published **two Wildstalker** strings (raid + M+) but recommends
> **Keeper of the Grove for M+** in its prose — an internal inconsistency in
> the source. Treat the strings as starting points and swap the hero tree /
> Incarnation-vs-Convoke node to match the tree you actually run. A dedicated
> **Keeper of the Grove** string was not captured — build it from the tree in
> `talents.md` (Grove Guardians + Cenarius' Guidance + Incarnation) or import
> from Icy Veins/Wowhead. @verify-ingame

## Stat priority (Tier-3, corroborate)

Guides broadly run **Haste** (more HoT ticks / faster ramp) and **Mastery**
(*Harmony* — your healing is amplified per HoT on the target, so it rewards the
same stacking playstyle) high, with **Crit** valued for the Abundance/Intensity
Regrowth crits and **Versatility** as the flat/defensive filler. Secondaries
are relatively flat — favor item level, and **sim on Raidbots** when it
matters. @verify-ingame (exact stat order varies by source/content).

## Notes / gaps

- **No Tier-1 optimization source** (SimC omits healers). All ordering here is
  guide consensus, not sim output — hence medium confidence.
- **Hero-tree raid/M+ assignment is unresolved** across sources; flagged above.
- A clean **Keeper of the Grove** import string is missing — only Wildstalker
  strings were published by the primary source.
- Exact stat weights not pinned to a Tier-1/Tier-2 source — verify on Raidbots
  / WCL for your gear and content.

---
title: Restoration Shaman — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/restoration-shaman/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/restoration-shaman-pve-healing-spec-builds-talents  # tier 3, 12.0.7, 2026-07-11
  - https://maxroll.gg/wow/class-guides/restoration-shaman-mythic-plus-guide  # tier 3, 12.0.7, 2026-07-11
  - knowledge/classes/shaman/restoration/talents.md  # tier 1 game-data tree (12.0.7.67808)
confidence: medium
---

# Restoration Shaman — Talents & Builds (Midnight S1)

This layers build guidance on top of the game-data tree in
[`talents.md`](./talents.md) (Tier-1, build 12.0.7.67808) — that file is the
node/spell-ID source of truth; this one is the *what to pick and why*.

## Hero tree: Totemic (all content)

**Play Totemic for both raid and Mythic+.** Method 12.0.7: "going into Midnight
Season 1, I will be recommending that you play Totemic for all content. It is a
very strong hero talent, that's also a lot easier to play." **Farseer** lost a
lot of power in Midnight (removal of Whispering Waves) and now underperforms;
keep it as a solo/niche or single-target-flavor pick.

- **Totemic** turns Healing Rain into the instant, relocatable **Surging Totem**,
  adds the apex **Stormstream Totem** (empowered Healing Stream Totem, proc'd by
  Riptide and guaranteed by Nature's/Ancestral Swiftness), and — via **Lively
  Totems** — makes your totems fire off free Chain Heals. Net: more passive group
  healing, lower APM, and easy repositioning with **Totemic Projection**.
- **Farseer** leans on **Call of the Ancestors** (Ancestors mirror your heals)
  and **Ancestral Swiftness** (upgraded Nature's Swiftness that also spawns an
  Ancestor + deals damage). Casts hit harder individually but you lose the
  passive totem throughput; **Ascendance + Deeply Rooted Elements** is its CD
  engine. Import string exists for a Farseer delve/solo variant.

## Recommended builds (import strings, 12.0.7)

Strings parsed from Method / Icy Veins 12.0.7 pages — **confirm they load as the
right hero tree in-game** before trusting (one bad character breaks an import).
Talent import strings are tree-version-sensitive; re-verify if the trees change.
@verify-ingame

**Raid — Totemic, Downpour (Method's recommended raid build):**
```
CgQAAAAAAAAAAAAAAAAAAAAAAAAAAgBAAAAzMzMLLbDzwYmZmZGzYB2gZsox2AyMwGjhZsNGz0stMzwMmFWMzMjZYWGAAYAzMDmZAgBD
```
Totem-centric raid healing (Healing Stream / Surging / Stormstream + Spirit Link
CD), taking **Downpour** as a burst-AoE top-up used before the Surging
Totem/Healing Rain puddle expires.

**Raid — Totemic, no Downpour (Riptide/mana-efficiency lean):**
```
CgQAAAAAAAAAAAAAAAAAAAAAAAAAAgBAAAAzMzMbLbDzMGzMzMzYGLwGMjFN2GQmB2MDGsNGz0stMzwMmFWMzMjZYWGAAAYmZwMDAMYA
```
Drops Downpour for the **Riptide package (Undercurrent, Wavespeaker's Blessing)**
and more mana efficiency — smoother sustained healing, less burst.

**Mythic+ — Totemic (recommended):**
```
CgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYMjZbbZmZmxYmZYGzYB2gZspx2AyMwGjZMzsNzY0stMzwMmFWMzMjhlZZAAwMgZGYmBAzgB
```
Shifts weight onto **Healing Wave / Chain Heal** casting over passive totem
ticks (smaller groups heal less from puddles), takes **Ancestral Vigor** for the
party max-health buff, and skips **Acid Rain** (low value in dungeons).

> Icy Veins lists slightly different Totemic strings and a **Farseer delve**
> string for the same patch; either source's Totemic build is fine. The three
> above are Method's. See both source pages if importing.

## Core talent picks & interactions

**Universal spine (both builds):**
- **Riptide** + **Tidal Waves** — the cast economy; Riptide banks a Tidal Waves
  charge that speeds/empowers the next Healing Wave/Surge, and enables
  **Flow of the Tides** (Chain Heal off a Riptide target gains an extra bounce).
- **Healing Stream Totem** + **Totemic Momentum** (reduced CD) — keep it rolling;
  feeds Lively Totems and Stormstream procs.
- **Unleash Life** — ~100% empower on the next Healing Wave/Riptide/Chain Heal;
  the tier 2-set adds direct healing, 4-set lets it empower a second spell.
- **Nature's Swiftness** (or **Ancestral Swiftness** on Farseer) — free instant
  cast on ~1 min, guarantees a Stormstream Totem proc.
- **Earth Shield** (+ **Earthen Harmony**) on the tank — heals on hit and boosts
  healing the shielded target takes (~20%; only that target, not the whole Chain
  Heal).
- **Resurgence** — mana back on heal crits; scales with Ascendance's guaranteed
  crits.
- **Spirit Link Totem**, **Ancestral Vigor**, **Ancestral Wolf Affinity**,
  utility/mobility (**Wind Rush Totem**, **Spirit Walk / Graceful Spirit**,
  **Nature's Guardian**, **Astral Shift** improvers) rounded in per content.

**Totemic-specific:** **Surging Totem**, **Stormstream Totem** (apex), **Lively
Totems** (free totem Chain Heals), **Totemic Projection**, **Downpour** (in the
Downpour build), plus tree passives like **Splitstream** / **Primal Catalyst**.

**Farseer-specific:** **Call of the Ancestors**, **Ancestral Swiftness**,
**Deeply Rooted Elements** (Ascendance procs), **Maelstrom Supremacy** /
**Windspeaker** / **Preeminence** (bigger, faster casts during Ascendance).

## Choice-node & CD notes

- **Ascendance / Healing Tide Totem** (spec choice node) — Totemic runs
  **Healing Tide** as its raid CD; Farseer runs **Ascendance**.
- **Downpour vs Riptide package** — Method's two raid strings are literally the
  Downpour-in / Downpour-out split; pick burst (Downpour) vs sustained/mana
  (Undercurrent + Wavespeaker's Blessing).
- **Purify Spirit + Improved Purify Spirit** — adds Curse removal to the dispel;
  standard in group content.

## TODO / gaps

- [ ] No Tier-1 simc APL/profile for Restoration (simc MID1 has only
      Elemental/Enhancement, verified 2026-07-11) — builds here rest on Tier-3
      Method/Icy Veins/Maxroll; re-verify strings in-game and re-sim on Raidbots
      when it matters.
- [ ] Gems/enchants/consumables and stat priority not yet captured here — add a
      gearing section (mirror the Affliction `builds.md` layout) when sourced.

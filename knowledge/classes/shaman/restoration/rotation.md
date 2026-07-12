---
title: Restoration Shaman — Rotation & Healing Priority (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/restoration-shaman/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/restoration-shaman-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/restoration-shaman-pve-healing-mythic-plus-tips  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Restoration Shaman — Rotation & Healing Priority (Midnight S1)

Restoration is a **priority-list healer**, not a fixed rotation. There is **no
Tier-1 simc APL** for this spec — simc ships MID1 profiles only for Elemental
and Enhancement (verified 2026-07-11), so the priority below is distilled from
Method and Icy Veins (Tier 3) and should be treated as **medium confidence**.

The whole spec is built on one habit: **keep totems down and cooldowns rolling,
then fill with direct heals.** Almost everything is more valuable used *on
cooldown* than banked. When nobody is in danger, **weave damage** (Flame Shock →
Lava Burst on Lava Surge → Lightning Bolt) — resto's damage also regens mana
(Mana Spring) and feeds group DPS.

Two passives shape every fill decision:
- **Tidal Waves** — Riptide and Chain Heal each bank a Tidal Waves charge that
  makes the next **Healing Wave** cast faster (or the next **Healing Surge** hit
  harder). Weaving a Riptide before a Healing Wave is almost always correct.
- **Unleash Life** — empowers the *next* Healing Wave / Riptide / Chain Heal by
  ~100%; spend it into your biggest upcoming heal, don't sit on it.

## Pre-combat

- **Water Shield** up (mana upkeep) and **Earth Shield** on the tank (if
  talented). Refresh **Riptide** on the tank just before the pull. Pre-place
  **Surging Totem** (Totemic) / **Healing Rain** if the group starts stacked.

## Cooldown rules

- **Use majors on cooldown, but not overlapping other healers** — Method: two
  raid cooldowns stacked on the same damage event mostly waste one. Assign
  windows.
- **Spirit Link Totem** — needs the raid **stacked within its radius (~13yd)**;
  best on predictable spread-damage or a soak where health is uneven. Gives
  ~10–15% DR plus a big Spouting Spirits upfront heal.
- **Ascendance** (Farseer's raid CD) / **Healing Tide Totem** (Totemic's raid
  CD) — the choice-node major; drop on the assigned heavy-damage phase.
- **Nature's Swiftness / Ancestral Swiftness** — on cooldown, preferably into
  **Chain Heal** (instant + free); also **guarantees a Stormstream Totem proc**.
- **Heroism/Bloodlust** — per raid/key plan (pull or execute), one per fight.
- **Relocate totems with Totemic Projection** rather than recasting when the
  group moves off them.

## Single-target priority

1. **Unleash Life** on cooldown (bank the empower into the next big heal).
2. **Nature's Swiftness / Ancestral Swiftness** on cooldown — ideally on Chain
   Heal; procs Stormstream Totem.
3. **Healing Stream Totem** — keep on cooldown / spend at max charges (also a
   safety heal); guaranteed value even single-target.
4. **Stormstream Totem** procs (apex) when banked.
5. **Riptide** on the injured target (and to bank a Tidal Waves charge).
6. **Healing Wave** on the most-injured target (Tidal-Waves-boosted); **Healing
   Surge** only when you need the health *now*.
7. **DPS** (Flame Shock → Lava Burst / Lightning Bolt) when no one is in danger.

## AoE / raid priority

1. **Healing Stream Totem** at/near max charges (keep it rolling).
2. **Surging Totem** (Totemic) — keep active; place where it hits the most
   allies/enemies. Non-Totemic: **Healing Rain** where the group will stand.
3. **Downpour** (if talented) before Surging Totem / Healing Rain expires — burst
   heal on the lowest allies.
4. **Unleash Life** + **Nature's/Ancestral Swiftness** on cooldown (Swiftness →
   Chain Heal).
5. **Riptide** on cooldown, prioritizing targets that don't already have it —
   spreads HoTs and sets up Chain Heal bounces.
6. **Chain Heal** — preferentially *starting on a Riptide target* to trigger
   **Flow of the Tides** (extra bounce); otherwise on the injured cluster.
7. **Healing Wave** for a hard single-target top-up amid the AoE.
8. Major cooldown (**Spirit Link / Healing Tide / Ascendance**) on the assigned
   heavy-damage window.
9. **DPS / Chain Lightning** when the group is safe.

## Cleave / Mythic+

Same shape as raid AoE but smaller groups, so **direct heals carry more of the
load** — the M+ Totemic build leans harder on Chain Heal / Healing Wave than on
passive totem ticks. Keep Riptides spread on the party, Chain Heal off Riptide
targets for Flow of the Tides, and **weave damage aggressively** between damage
events (Flame Shock on the pull, Lava Burst on Lava Surge, Chain Lightning on
packs) — Resto contributes meaningful dungeon DPS. Slot **Ancestral Vigor** for
the party max-health buff. Save **Spirit Link Totem** for big pull-damage or a
mechanic soak; **Wind Rush Totem** / **Spirit Walk** for movement-heavy pulls;
**Capacitor / Earthgrab / Thunderstorm** for pack control; **Tremor Totem** vs
fear mechanics.

## Hero-tree branches

- **Totemic (recommended, all content)** — priority above with **Surging Totem**
  replacing Healing Rain and **Stormstream Totem** in the mix; **Lively Totems**
  hands you free Chain Heals off your totems, so lean on totem uptime and use
  **Totemic Projection** to keep them on the group. Lower APM, more mobile.
  Primary raid CD: **Healing Tide Totem**.
- **Farseer** — **Call of the Ancestors** spawns Ancestors that echo your casts
  (Healing Wave→Healing Wave, Riptide/Unleash Life→Healing Surge, Chain
  Heal/AoE→Chain Heal), so casts are individually bigger but there's less passive
  group healing. Lead with **Ancestral Swiftness** and **Unleash Life** to keep
  Ancestors up; primary raid CD is **Ascendance** (pairs with Deeply Rooted
  Elements for extra procs). Weaker overall in Midnight S1 — solo/niche.

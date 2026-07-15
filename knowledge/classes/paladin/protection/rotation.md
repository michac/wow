---
title: Protection Paladin — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/tree/midnight/profiles/MID1  # tier 1, MID1_Paladin_Protection.simc (talent string; APL lives in engine sc_paladin.cpp)
  - https://www.method.gg/guides/protection-paladin/playstyle-and-rotation  # tier 3, upd. 2026-07-09
  - https://www.icy-veins.com/wow/protection-paladin-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://maxroll.gg/wow/class-guides/protection-paladin-raid-guide  # tier 3, 12.0.7
confidence: medium
---

# Protection Paladin — rotation (Midnight S1)

Protection is a **Holy-Power tank**: a fast builder→spender loop where damage and
survival are the same rotation. Generate Holy Power with short-CD builders, spend
it in 3-Holy-Power blocks on **Shield of the Righteous** (mitigation) — or on
**Word of Glory** when you need the heal — and keep **Consecration** under you at
all times. The two overriding rules: **never sit at 5 Holy Power** (builders
overcap and waste value) and **keep the Shield of the Righteous buff rolling**.
The hero tree changes the top of the priority: **Templar** revolves around the
**Divine Toll → Hammer of Light** burst window and **Shake the Heavens** upkeep;
**Lightsmith** folds in **Holy Armaments** (Sacred Weapon / Holy Bulwark) charge
spending.

> The Tier-1 simc **MID1_Paladin_Protection** profile carries the talent/gear
> loadout; the Protection APL itself lives in the SimC engine
> (`class_modules/sc_paladin.cpp`, `apl_protection`). The priority below is
> distilled from that APL's shape as reflected in the method.gg 12.0.7 lists
> (updated 2026-07-09) and corroborated against Icy Veins — treat exact ordering
> of the low-priority fillers as guide-sourced (Tier 3), the resource rules
> (don't overcap, SotR upkeep) as the hard contract.

## Pre-combat

- Set your aura (**Devotion**, or Concentration for a heavy-interrupt fight).
- **Lightsmith:** cast **Rite of Sanctification** (or Rite of Adjuration) and
  pre-apply a **Holy Armament** (Sacred Weapon).
- Drop **Consecration** and pre-cast **Judgment** / **Avenger's Shield** on pull.
- Pull with **Avenger's Shield** (ranged, generates Holy Power, silences a caster).

## Cooldown rules

- **Avenging Wrath** (or **Sentinel**) is the burst window — roughly every
  **2 min**, or **~1 min with Righteous Protector**, which is the standard build.
  Line trinkets/potion (Light's Potential) up with it.
- **Divine Toll** is used on cooldown (~1 min), synced into the Wings window for
  the Holy-Power flood. **Templar:** Divine Toll then grants **Hammer of Light**
  for 12s — spend it immediately and keep spending while it's up.
- **Instrument of the Divine:** during high-Holy-Power phases (Wings), fire
  Shield of the Righteous at 5 Holy Power for the bonus damage rather than banking.
- Defensives are used *proactively* on known damage, not saved forever:
  **Ardent Defender** (shortest CD, the cheat-death floor) → **Guardian of
  Ancient Kings** (big wall) → **Divine Shield / Lay on Hands** for emergencies.
- **Blessing of Sacrifice / Protection / Spellwarding** guard allies or cover a
  co-tank on demand.

## Single-target priority

1. **Avenging Wrath / Sentinel** — on cooldown (burst window).
2. **Divine Toll** — on cooldown (into the Wings window when possible).
3. **Hammer of Light** *(Templar, while available)* — top priority for its 12s.
4. **Shield of the Righteous** — at 5 Holy Power (with Instrument of the Divine),
   to avoid capping, or on a **Divine Purpose** proc. Keep the buff rolling.
5. **Consecration** — if you're not standing in it / it's about to expire.
6. **Hammer of Wrath** — whenever available (during Avenging Wrath via the
   Judgment transform, or on execute-range targets).
7. **Avenger's Shield** — on **Glory of the Vanguard** proc (or when off CD /
   Grand Crusader reset).
8. **Judgment** — builder, on cooldown.
9. **Sacred Weapon / Holy Bulwark** *(Lightsmith)* — spend Holy Armament charges;
   refresh Sacred Weapon when its buff drops below ~5s.
10. **Blessed Hammer / Hammer of the Righteous** — filler builder.
11. **Word of Glory** — when you need the heal, or free via **Shining Light**
    (Templar: cheaper with Shake the Heavens up).
12. **Consecration** — as the last filler if nothing else is available.

## Cleave / AoE (2+ targets)

Same core loop, but **Avenger's Shield and Consecration rise sharply** and Blessed
Hammer becomes your main builder:

1. **Avenging Wrath / Sentinel** and **Divine Toll** on CD (Divine Toll hits up
   to 5 → huge Holy-Power burst; **Hammer of Light** for Templar cleaves hard).
2. **Consecration** — keep it down; it's a big chunk of your AoE damage and
   feeds Divine Guidance (Lightsmith).
3. **Avenger's Shield** — high priority (multi-target, Grand Crusader resets it).
4. **Shield of the Righteous** — spend to avoid capping / on procs (still your
   mitigation; Instrument of the Divine bonus AoE in Wings).
5. **Hammer of Wrath** when available.
6. **Blessed Hammer** — primary AoE builder (choose over Hammer of the Righteous
   for AoE).
7. **Judgment**, then Consecration/Word of Glory as filler.

## Hero-tree branches

- **Templar (raid / single-target lean):** the priority is built around
  **Divine Toll → Hammer of Light** (12s window, top priority while up) and
  keeping **Shake the Heavens** rolling via Hammer of Light / Blessed Hammer.
  Word of Glory is often free with Shining Light + Shake the Heavens. Fewer
  Avenger's Shield casts than Lightsmith on single target.
- **Lightsmith (M+ / preferred by method for dungeons):** insert **Holy
  Armaments** — refresh **Sacred Weapon** when its buff wanes and spend **Holy
  Bulwark** charges outside the Wings window. **Reflection of Radiance** and
  **Divine Guidance** (5-stack Consecration empowerment) reward tight
  Consecration and Avenger's Shield play; **Divine Resonance / Punishment**
  give extra interrupt/Avenger's Shield coverage in dungeons.

## TODO

- [ ] Distill the exact `apl_protection` action order from SimC engine source
      (`class_modules/sc_paladin.cpp`) for a Tier-1 numeric ordering — current
      list is guide-shaped (Tier 3) over the Tier-1 talent profile.
- [ ] Confirm the Judgment→Hammer of Wrath transform's Holy-Power/charge
      behaviour in-game (@verify-ingame in abilities.md).

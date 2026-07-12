---
title: Enhancement Shaman — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Shaman_Enhancement.simc  # tier 1 APL (single_sb / single_totemic / aoe / buffs), 2026-07-11
  - https://www.method.gg/guides/enhancement-shaman/playstyle-and-rotation  # tier 3, 12.0.7 upd. 2026-06-16 (Weber), 2026-07-11
  - https://www.icy-veins.com/wow/enhancement-shaman-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: high
---

# Enhancement Shaman — Rotation (Stormbringer / Totemic, Midnight S1)

Distilled from the SimulationCraft default APL (tier 1), corroborated by the
Method 12.0.7 guide (Weber) and Icy Veins. The APL branches by **hero tree**
(`single_sb` = Stormbringer, `single_totemic` = Totemic) and by **enemy count**
(`aoe` at 2+). Both branches share one idea: **build Maelstrom Weapon with
strikes and spend it as late as possible** — hold to 9–10 stacks, dumping at 5+
only when nothing else is worth pressing, so **Elemental Tempo** keeps refunding
Stormstrike/Lava Lash cooldown.

> **Midnight framing.** Maelstrom Weapon (0–10 stacks) is the resource: at 5+
> stacks Lightning Bolt / Chain Lightning / Tempest / Primordial Storm become
> instant and gain ~20% damage per stack consumed. **Hot Hand** was reworked to
> give less Lava Lash CD reduction (two GCDs between Lava Lashes, not one)
> **unless** Elemental Tempo is talented. The spec is currently **thin
> defensively** (Stone Bulwark Totem removed, Earth Elemental nerfed) — plan
> Astral Shift + instant Healing Surge deliberately.

## Pre-combat

1. **Windfury Weapon** (main hand) + **Flametongue Weapon** (off hand) imbues.
2. **Lightning Shield**.
3. `snapshot_stats`; pre-use a "weird" trinket (e.g. Algethar Puzzle Box) so its
   buff lines up with the opener.

**Stormbringer opener:** Voltaic Blaze → Ascendance → Crash Lightning →
Stormstrike.
**Totemic opener:** Voltaic Blaze → Surging Totem → Sundering → Lava Lash →
Doom Winds → Crash Lightning → Lava Lash → Primordial Storm.

## Cooldown rules

- **Doom Winds** (~60s) is the main burst on the non-Ascendance build — it spikes
  Windfury procs and Maelstrom generation (Static Accumulation). If **Ascendance**
  is talented as an active it **replaces** Doom Winds and the burst moves to a
  ~2-min cadence; **Deeply Rooted Elements** instead makes Ascendance a random
  proc you react to.
- **Sundering** after Doom Winds, then on cooldown (the APL gates it on Surging
  Elements / Whirling Earth / Feral Spirit being talented).
- **Surging Totem** (Totemic) is the pivot — drop it and build the Hot
  Hand/Lava Lash window around it.
- **Trinkets, potion, and racials** (Blood Fury / Berserking / Fireblood /
  Ancestral Call) all sync to **Ascendance up / Doom Winds up / Surging Totem
  active** — the `buffs` list fires them together. Power Infusion (external) is
  timed to Ascendance on DRE builds.
- End of fight (`fight_remains` short): dump everything, spend remaining
  Maelstrom.

## Single target — Stormbringer

From `actions.single_sb`:

1. **Primordial Storm** if 9+ Maelstrom (or buff about to expire at 5+) — *only
   if talented; otherwise the lightning spender below fills this slot.*
2. **Voltaic Blaze** to apply Flame Shock if it's missing (opener) → **Flame
   Shock** if not ticking.
3. **Lava Lash** if Lashing Flames debuff is missing (opener).
4. `buffs` (trinkets/potion/racials — see cooldown rules).
5. **Sundering** (if Surging Elements / Feral Spirit talented).
6. **Doom Winds**.
7. **Crash Lightning** if its buff is down (or always, with Storm Unleashed).
8. Inside Doom Winds/Ascendance with Thorim's Invocation: **Voltaic Blaze →
   Windstrike → Ascendance → Stormstrike → Crash Lightning** (the burst spends
   Maelstrom for you).
9. **Tempest** at **10 Maelstrom** → else **Lightning Bolt** at **10 Maelstrom**.
10. **Stormstrike** if it's about to cap charges (`charges_fractional>=1.8`).
11. **Lava Lash** → **Stormstrike** → **Voltaic Blaze** → **Sundering**.
12. **Lightning Bolt** at **8+ Maelstrom** → **Crash Lightning** → **Lightning
    Bolt** at **5+ Maelstrom** → **Flame Shock** (last-resort filler).

The through-line: keep Flame Shock up (Voltaic Blaze), keep Crash Lightning's
buff up, hold strikes off cap, and spend Maelstrom at 10 (Tempest > Lightning
Bolt), dropping the spend threshold only when idle.

## Single target — Totemic

From `actions.single_totemic`:

1. **Voltaic Blaze** if Flame Shock is missing → **Flame Shock** if not ticking.
2. **Surging Totem** (drop/maintain it).
3. `buffs`.
4. **Sundering** (Surging Elements / Whirling Earth / Feral Spirit talented).
5. **Lava Lash** with **Whirling Fire** or **Hot Hand** up (this is the Totemic
   payoff button).
6. **Doom Winds**.
7. **Crash Lightning** if its buff is down (or always with Storm Unleashed).
8. **Primordial Storm** at **10 Maelstrom** (or expiring at 5+).
9. Ascendance/Thorim's window: **Windstrike → Ascendance → Crash Lightning →
   Stormstrike**.
10. **Lightning Bolt** on the Elemental Tempo timing (5+ Maelstrom when Lava Lash
    is close to coming back, or 10 Maelstrom).
11. **Crash Lightning** (buff down) → **Lava Lash** → **Sundering** (if Surging
    Totem CD > 25s) → **Stormstrike** → **Voltaic Blaze** → **Crash Lightning**.
12. **Lightning Bolt** at **5+ Maelstrom** → **Flame Shock**.

## Cleave & AoE (2+)

From `actions.aoe`. Rule of thumb: **at 2+ targets, Chain Lightning replaces
Lightning Bolt** as the Maelstrom spender; Crash Lightning becomes near-
mandatory upkeep and a spam button.

1. **Voltaic Blaze** (Totemic, Flame Shock missing) → **Flame Shock** if not
   ticking → **Surging Totem**.
2. **Ascendance** (if Thorim's is set to Chain Lightning).
3. `buffs`.
4. **Sundering** (Surging Elements / Whirling Earth).
5. **Lava Lash** with **Whirling Fire** up.
6. **Doom Winds**.
7. Thorim's/Doom Winds/Ascendance + Whirling Air window: **Crash Lightning →
   Windstrike → Stormstrike**.
8. **Tempest** at 10 Maelstrom (when not overlapping Ascendance+Doom Winds) →
   **Primordial Storm** at 10 Maelstrom.
9. **Crash Lightning** (main AoE builder/upkeep).
10. **Chain Lightning** at **9–10 Maelstrom** (10 for Totemic).
11. **Sundering** (Feral Spirit talented) → **Voltaic Blaze** → **Windstrike /
    Stormstrike** (charges near cap or Converging Storms maxed) → **Lava Lash**.
12. **Chain Lightning** at **5+ Maelstrom** → **Flame Shock** (filler).

Flame Shock is spread up to ~6 targets (the APL tracks `flame_shock_saturated`)
for Lightning Rod funnel and fire synergies; Voltaic Blaze does the spreading.

## Hero-tree branches — summary

- **Stormbringer** (`single_sb`): no Surging Totem. Spends into **Tempest**
  (its "massive nuke") then Lightning Bolt/Chain Lightning. Flexible; common in
  M+. Burst is Doom Winds or Ascendance.
- **Totemic** (`single_totemic`): built around **Surging Totem** + **Hot Hand /
  Whirling Fire** Lava Lashes and **Sundering**; spends into **Primordial Storm**
  instead of Tempest. Raid-preferred (see `builds.md`).

## TODO

- [x] ST priority (both hero trees) — from simc `single_sb` / `single_totemic`
      APL, 2026-07-11
- [x] AoE priority — from simc `actions.aoe`, 2026-07-11
- [x] Cooldown/`buffs` sync rules — from simc `actions.buffs`, 2026-07-11
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Confirm Sundering CD (30 vs 40s) and Voltaic Blaze trigger in-game

---
title: Holy Paladin — Rotation & Priority (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/holy-paladin/playstyle-and-rotation  # tier 3, 2026-07-11 (12.0.7)
  - https://www.icy-veins.com/wow/holy-paladin-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/holy-paladin-mythic-plus-guide  # tier 3, 2026-07-11
  - https://www.wowhead.com/guide/classes/paladin/holy/rotation-cooldowns-pve-healer  # tier 4, 2026-07-11 (nav shell only)
confidence: medium
---

# Holy Paladin — Rotation & Priority (Midnight S1)

Holy Paladin has no SimulationCraft healing APL (SimC does not model healer
throughput), so this priority is distilled from three Tier-3 guides that agree
on the shape. Confidence is **medium**, not high — there is no Tier-1 APL to
pin exact numbers to. The governing rule from every source is the same:
**"cast as many spells as possible, as fast as possible," and never overcap
Holy Power.** Holy is a reactive, build-and-spend healer — you are almost never
idle; you fill downtime by generating Holy Power (and dealing damage) so a
spender is always ready when damage lands.

The rotation is **the same for both hero trees**; the only difference is which
throughput cooldown you keep on cooldown (Herald: **Divine Toll**; Lightsmith:
**Holy Armaments**).

## Pre-combat / opener

- Apply **Beacon of Light** (and **Beacon of Faith**, if talented) to the tank(s)
  or a low-mobility target before the pull.
- Buff up: **Sacred Weapon** via **Holy Armaments** (Lightsmith) or, for Herald,
  just top the group and hold Divine Toll for the first damage event.
- Judgment / Crusader Strike / Holy Shock into the pull to enter combat with
  Holy Power banked and a spender ready.

## Cooldown rules

- **Avenging Wrath** — on cooldown unless a raid assignment says to hold it.
  Best combined with **Divine Toll** ("godlike" per maxroll); Avenging Wrath
  alone is "strong," Divine Toll alone is "okay," Aura Mastery alone is "weak."
- **Avenging Crusader** (choice vs Avenging Wrath) — pop when you can stay on a
  target and pump Judgment/Crusader Strike; the window converts that damage into
  group healing.
- **Divine Toll** — keep on cooldown; hold only for imminent, known burst. For
  **Herald** it seeds Dawnlight, so it is your single most important button.
- **Holy Prism** — keep on cooldown (enemy-cast to heal, ally-cast to damage).
  **Do not** stack it with Avenging Wrath on fights with constant AoE bursts —
  that is "massive overkill."
- **Aura Mastery** — pre-cast before scripted raid-wide damage (Devotion Aura →
  ~12% party DR).
- **Tyr's Deliverance** — on cooldown as a rolling group-HoT / heal amp.
- **Beacon of Virtue** (if talented) — cast **right after the first tick of
  damage** so the extra beacons catch the whole hit; aim to keep it on cooldown.

## Single-target healing priority

1. **Holy Shock** on cooldown (heal) — core builder, crit → **Infusion of Light**.
2. **Divine Toll** / **Holy Armaments** on cooldown (per hero tree) — big
   Holy-Power + throughput.
3. Spend Holy Power at/near cap: **Eternal Flame** (or **Word of Glory**) on the
   injured target. **Never overcap.**
4. **Flash of Light** — spend **Infusion of Light** procs on it (instant, boosted);
   the emergency fast heal.
5. **Holy Light** — when mana permits and the damage is not urgent (efficient
   top-up).
6. **Judgment** / **Crusader Strike** / **Hammer of Wrath** as builder filler to
   keep Holy Power flowing (and to deal damage).
7. **Shield of the Righteous** to dump Holy Power when nobody needs healing.

## AoE / raid healing priority

1. **Beacon of Virtue** (if talented) right as the AoE damage lands.
2. **Divine Toll** (up to 5-target Holy Shock) and/or **Holy Prism** on an enemy
   for instant multi-target healing.
3. **Holy Shock** on cooldown.
4. Spend Holy Power on **Light of Dawn** (15-yd radius around you — stand in the
   group) for even AoE damage; use **Eternal Flame**/**Word of Glory** instead
   when the damage is concentrated on one or two targets.
5. **Flash of Light** on Infusion procs for spot triage; **Holy Light** for
   efficient refills between bursts.
6. Builders (Judgment / Crusader Strike / Hammer of Wrath) + **Shield of the
   Righteous** to avoid overcapping in lulls.

## Mythic+ notes

- Same priority, but you spend far more time **dealing damage**: keep Judgment,
  Crusader Strike, Hammer of Wrath, and Holy Prism (enemy-cast) rolling, and
  dump spare Holy Power into **Shield of the Righteous** when the group is
  healthy. "Even if there isn't much to heal you can always use Shield of the
  Righteous" — do not overcap.
- **Eternal Flame** is the default M+ Holy-Power spender (HoT value); switch to
  **Light of Dawn** on even, group-wide AoE damage.
- Cooldown potency ranking (maxroll): **Avenging Wrath + Divine Toll** > Avenging
  Wrath alone > Divine Toll alone > Aura Mastery. Avoid Avenging Wrath + Holy
  Prism on frequent-AoE pulls (overkill).

## Hero-tree branches

- **Herald of the Sun** — **Divine Toll** and **Holy Prism** each apply
  **Dawnlight** HoTs; during **Avenging Wrath / Avenging Crusader**, **Sun's
  Avatar** links beam-lines between Dawnlight targets that heal allies / damage
  enemies crossing them. Press Divine Toll and Holy Prism on cooldown to keep
  Dawnlights out — this is where most of Herald's throughput comes from. Default
  for raid, and per maxroll the stronger M+ tree as well.
- **Lightsmith** — replace "Divine Toll on cooldown" with **Holy Armaments on
  cooldown**, alternating **Sacred Weapon** (ally offensive/healing buff) and
  **Holy Bulwark** (ally absorb) each cast; Holy Armaments now also gives 3 Holy
  Power. Everything else in the priority is identical. Method leans Lightsmith
  for M+ utility; maxroll counts its raw healing lower (see `builds.md`).

## Gaps / caveats

- No Tier-1 SimC APL exists for a healer spec — exact press-order between
  near-equal builders (Judgment vs Crusader Strike vs Hammer of Wrath) is not
  numerically pinned. @verify-ingame
- Whether **Flash of Light / Holy Light** generate Holy Power in Midnight is
  asserted by two Tier-3 guides but not confirmed against game data. @verify-ingame

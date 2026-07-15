---
title: Beast Mastery Hunter — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-12
reviewed: 2026-07-12
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Beast_Mastery.simc  # tier 1 APL, WoW 12.0.x (st/cleave = Pack Leader, drst/drcleave = Dark Ranger)
  - https://www.method.gg/guides/beast-mastery-hunter/playstyle-and-rotation  # tier 3, 12.0.7 corroboration
  - https://www.icy-veins.com/wow/beast-mastery-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: medium
---

# Beast Mastery Hunter — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1). The APL splits four
ways by hero tree and enemy count: **`st` / `cleave`** are the **Pack Leader**
lists (no Black Arrow), **`drst` / `drcleave`** are the **Dark Ranger** lists
(`talent.black_arrow`). Pack Leader is the S1 default (see `builds.md`); the
Dark Ranger branches are given below it.

**The mental model (both trees):** never let **Kill Command** or **Barbed
Shot** charges cap; keep the pet's **Frenzy** rolling with Barbed Shot; fill
every remaining GCD with **Cobra Shot**; and line all of it up under **Bestial
Wrath** every 30s. Everything is instant — cast while moving.

## Pre-combat

- Summon pet (`summon_pet`); apply **Hunter's Mark** to the main target;
  pre-use a burst trinket (e.g. Algethar Puzzle Box) so it lands on the pull.

## Cooldown rules

- **Bestial Wrath every 30s on cooldown** — it's the whole game. It triggers
  **both** hero capstones (Pack Leader's Howl summon + Stampede line, Dark
  Ranger's Withering Fire). **Dump Barbed Shot charges into the target *before*
  pressing it** (the APL's `barbed_shot ... if=cooldown.bestial_wrath.remains<gcd`
  line) so Frenzy is maxed for the window.
- **Racials, potion, and trinkets are all gated on Bestial Wrath** in the APL
  (`if=cooldown.bestial_wrath.ready` / `.remains<2`). Berserking, Blood Fury,
  Ancestral Call, Fireblood, Light's Potential potion, and every on-use trinket
  fire with the burst window — don't bank them past a lost use near the end of a
  fight (`fight_remains<…` fallbacks).
- External **Power Infusion** is requested for the Bestial Wrath window.

## Single target — Pack Leader (`st`)

1. **Barbed Shot** — if Bestial Wrath is about to come up (`remains<gcd`), to
   dump charges and max Frenzy before the window.
2. **Bestial Wrath** — on cooldown.
3. **Wild Thrash** — if 2+ enemies (splash it in even on near-single-target).
4. **Kill Command** — when it won't cap Barbed Shot charges *and* **Nature's
   Ally is up or a Howl summon is ready** (`buff.natures_ally.react |
   howl_summon.ready`), or whenever the apex condition frees it (`!apex.3`).
5. **Barbed Shot** — as a builder when Focus is low (`focus<75`) or a charge is
   about to cap (`full_recharge_time<gcd`); with **Serpentine Strikes** talented,
   Barbed Shot is pressed more aggressively.
6. **Cobra Shot** — Focus-dump filler on any leftover GCD (holds if Bestial
   Wrath is within a GCD).

## AoE / cleave — Pack Leader (`cleave`)

The Pack Leader `cleave` list is entered at 3+ targets, or 2+ with **Beast
Cleave** talented.

1. **Barbed Shot** — on the target with the least remaining bleed if a charge is
   about to cap (`full_recharge_time<gcd`).
2. **Wild Thrash** — to put up / keep **Beast Cleave** (with Beast Cleave
   talented this is priority; the pet then cleaves its Kill Commands).
3. **Bestial Wrath** — unless you just cast Wild Thrash.
4. **Wild Thrash** — (fallback when Beast Cleave isn't talented).
5. **Kill Command** — with **Nature's Ally** up or **Master Handler** talented.
6. **Cobra Shot** — with the **Hogstrider** buff up at <4 targets (Pack Leader
   proc); otherwise Barbed Shot / Cobra Shot as fillers, re-Barbed on the
   lowest-bleed target.

## Single target — Dark Ranger (`drst`)

1. **Barbed Shot** — pre-Bestial-Wrath dump, specifically with the Bloody
   Frenzy + Snakeskin Quiver + Jagged Wounds cluster.
2. **Bestial Wrath**.
3. **Black Arrow** — while **Withering Fire** is up (and Kill Command is near
   capping): the tripled-damage Black Arrow window.
4. **Kill Command** — with **Nature's Ally** up (or `!apex.3`).
5. **Wailing Arrow** — as Withering Fire is about to fall off, or as an execute
   near death; guarantees a Deathblow.
6. **Cobra Shot** — with **Killer Cobra** during Bestial Wrath to reset Kill
   Command when Barbed Shot charges are safe.
7. **Black Arrow** → **Barbed Shot** (lowest bleed) → **Cobra Shot** as fillers.

## AoE / cleave — Dark Ranger (`drcleave`)

1. **Black Arrow** — when **Beast Cleave** is about to lapse and Bestial Wrath
   is ready at 3+ targets (re-applies cleave).
2. **Bestial Wrath** — while Beast Cleave is up.
3. **Wild Thrash**.
4. **Kill Command** — with Nature's Ally (or `!apex.3`).
5. **Barbed Shot** — when a charge is about to cap.
6. **Black Arrow** during **Withering Fire** → **Wailing Arrow** as the window
   ends → Barbed Shot → Black Arrow → Wailing Arrow → **Cobra Shot** filler.

## Hero-tree summary

- **Pack Leader:** the **Howl of the Pack Leader** timer (30s, ticked down by
  Cobra Shot / Kill Command) arms your next Kill Command to summon a rotating
  beast; **Bestial Wrath also arms it instantly** and the first Kill Command in
  Bestial Wrath drops a **Stampede** line (position it through where mobs are
  moving). Kill Command with Howl/Nature's Ally up is the payoff button.
- **Dark Ranger:** **Bestial Wrath** opens **Withering Fire**, during which
  **Black Arrow** is spammable at tripled damage; **Wailing Arrow** guarantees a
  **Deathblow** reset. Slightly bursts harder in single target.

## TODO

- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`).
- [ ] Confirm exact Focus costs / cooldowns for Cobra Shot, Wild Thrash, and
      Nature's Ally in-game (marked @verify-ingame in `abilities.md`).
- [~] Re-distill when the simc midnight branch publishes a dated 12.0.7 APL
      (current profile pulled 2026-07-12; talent string
      `C0PAAAAAAAAAAAAAAAAAAAAAAAMmxwCsBzwQDbAAYG2GzsNzwMmZYYmxYmxMzYGzwMzYGzgx0MAAAAAmBAAgxMzMgZ2AbwsA2GA`).

---
title: Vengeance Demon Hunter — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-14
sources:
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Vengeance.simc  # tier 1 APL, WoW 12.0.7.67808 — PRIMARY
  - wago.tools DB2 SpellCooldowns/SpellCategories, spell 247454 Spirit Bomb  # tier 1, CategoryRecoveryTime 25000ms — confirms Spirit Bomb's ~25s CD
  - ../../../_meta/patch-notes/12.0.5.md  # tier 1, Feast of Souls heals instantly on Soul Cleave
  - https://www.method.gg/guides/vengeance-demon-hunter/playstyle-and-rotation  # tier 3, Midnight 12.0.7, upd. 2026-06-16
  - https://www.icy-veins.com/wow/vengeance-demon-hunter-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://wowcarry.com/blog/wow/wow-news/vengeance-demon-hunter-in-midnight-talents-annihilator-guide  # tier 4, Annihilator mechanics corroboration
confidence: high
---

# Vengeance Demon Hunter — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1); method.gg and Icy Veins
(Tier 3) corroborate the priority. The APL splits hard by **hero tree** — it
runs `actions.ar` for **Aldrachi Reaver** and `actions.anni` for **Annihilator**
— and both are competitive in S1 (see `builds.md`). Below: the shared framing,
then each tree. Both share the same core builders/spenders (Fracture → Spirit
Bomb / Soul Cleave) and the same maintenance layer.

The whole spec is a **builder/spender**: **Fracture** makes Fury + 2 Soul
Fragments; you dump fragments into **Spirit Bomb** (AoE / high fragment count)
or **Soul Cleave** (ST + self-heal), and keep **Immolation Aura**, **Sigil of
Flame**, **Fiery Brand**, and **Demon Spikes** rolling constantly. The two hero
trees change *what you're building toward*, not the core buttons.

## Always-on maintenance (both trees, off the top of the APL)

- **Disrupt** the moment a target is casting something interruptible.
- **Infernal Strike** off-GCD (mobility, and free fire damage — don't sit on 2 charges).
- **Demon Spikes** off-GCD whenever it's down and you're in combat — active
  mitigation, near-100% uptime is the goal.
- Keep **Immolation Aura** and **Sigil of Flame** on cooldown for the passive
  damage / Fury / mitigation they compound into.

## Cooldown rules (both trees)

- **Fiery Brand** is offensive as well as defensive: dump a charge when at 2
  charges (don't overcap), or to open a **Fiery Demise** window that amps your
  fire spenders. Line **Soul Carver** / **Fel Devastation** inside that window.
- **Soul Carver**, **Sigil of Spite**, **Fel Devastation** (40–60s CDs) and
  buff trinkets are gated in dungeons on the pull living long enough (APL:
  `dung_cd_ok`) — hold them if the current pack is about to die or a bigger
  pull is <12s away.
- **Metamorphosis** (2min) is held to a stricter TTD guard in dungeons; on a
  boss / long pull, use it on cooldown (it's both a burst and a defensive).
- **Potion / racials / external Power Infusion**: line up with Metamorphosis /
  the burst window (or the execute phase, `fight_remains<20`).
- End of fight (`fight_remains<20`): dump all cooldowns and trinkets.

## Fragment targeting (the key variable)

Spirit Bomb wants a **fragment target** before it's worth casting. The APL sets
it to **5** normally, **3** inside a Fiery Demise (Fiery Brand) window, and **4**
in Metamorphosis (Annihilator); Aldrachi Reaver drives its own count off Art of
the Glaive stacks. Practically: **spend at 5 fragments** in single target, spend
earlier (3–4) inside Brand/Meta, and drop the threshold by 1 in AoE.

> **Spirit Bomb is on a ~25-second cooldown (haste-reduced) — new in Midnight.**
> Confirmed via DB2 (SpellCooldowns, spell 247454: CategoryRecoveryTime 25 000 ms,
> not charge-based). This is why the APL fires it *at fragment target* without an
> explicit cooldown check — SimC only casts it when it's off cooldown anyway. The
> practical consequence: **Soul Cleave is your between-Spirit-Bomb Fury spender
> and self-heal** — it has no such cooldown, so it soaks fragments/Fury while
> Spirit Bomb recharges. (12.0.5 confirms Feast of Souls heals *instantly* on
> Soul Cleave.)

---

## Aldrachi Reaver (AR)

AR revolves around the **Reaver's Glaive** cycle. Art of the Glaive builds
stacks (from consumed fragments); when it fills you get a **Reaver's Glaive**,
which empowers your next **Fracture** (Rending Strike) and next **Soul Cleave**
(Glaive Flurry). You alternate "slash" and "refresh" cycles to keep **Reaver's
Mark** on the target.

Single-target priority (from `actions.ar` / `ar_fillers`):

1. **Felblade** immediately after a Vengeful Retreat (Unhindered Assault combo).
2. **Metamorphosis** — free on an Untethered-Rage-style proc, else on cooldown (TTD-gated in dungeons).
3. **Reaver's Glaive** when stored and it's the right cycle (mark expiring/aging, execute, or Art of the Glaive about to overflow).
4. **Glaive cycle** (`ar_glaive_cycle`) while Rending Strike / Glaive Flurry are up: on a **slash** cycle cast **Fracture** first (applies Reaver's Mark + slash), on a **refresh** cycle cast **Soul Cleave** first (so the following Fracture lands a 3-stack mark).
5. **Fiery Brand** at 2 charges, or to set up a Fiery Demise window.
6. **Sigil of Spite** for fragments (skip mid-glaive-cycle).
7. **Emergency consume** (`ar_quick_consume`) if Art of the Glaive + fragments would overflow, or 6+ fragments in AoE.
8. **Immolation Aura** in combat.
9. **Fel Devastation** at high Fury (>85) with in-flight fragments, not right before a Reaver's Glaive.
10. **Sigil of Flame**.
11. **Soul Carver** in a Fiery Demise window (or mark aging / execute).
12. Fillers: **Spirit Bomb** at fragment target → **Soul Cleave** (at 5+ fragments ST, or to avoid capping / spend Fury) → **Fracture** → **Felblade** → **Vengeful Retreat** (Felblade reset) → **Throw Glaive**.

## Annihilator (Anni)

Anni builds **Voidfall** stacks with **Fracture**; at **3 stacks**, spending
(**Spirit Bomb** / **Soul Cleave**) releases meteors. **Metamorphosis** grants
meteors + resets Spirit Bomb, and the **Untethered Rage** Apex talent grants
free Metamorphosis charges from consumed fragments — the burst trigger.

Priority (from `actions.anni` and its Voidfall sub-lists):

1. If **Voidfall is spending** (3 stacks, `anni_voidfall_spending`): fire **Fiery
   Brand**, bridge Fury with **Felblade**/**Fracture** if needed, then **Spirit
   Bomb** at fragment target (or **Soul Cleave** if Spirit Bomb is on CD),
   backfilling fragments with Soul Carver / Fel Devastation / Sigil of Spite.
2. **Metamorphosis** entry: on an **Untethered Rage** proc (unconditional), or
   when Meta is about to come up and TTD allows — set up fragments + ~75 Fury
   first for the post-Meta Spirit Bomb + Soul Cleave Voidfall combo.
3. **Anni cooldowns** (`anni_cooldowns`): **Spirit Bomb** at target → **Soul
   Carver** (≤3 frags) → **Sigil of Spite** (low frags) → **Fel Devastation**.
4. **Fiery Brand** at 2 charges / to open Fiery Demise.
5. **Fracture** if about to cap charges.
6. **Immolation Aura** (priority in AoE with Fallout, or in a Brand window with Charred Flesh).
7. **Spirit Bomb** at fragment target.
8. **Immolation Aura** → **Sigil of Flame**.
9. **Fracture** to rebuild (total frags ≤4 or Fury <40).
10. **Soul Cleave** to spend down / avoid capping Fury.
11. Fillers: **Fracture** → **Felblade** → **Throw Glaive**.

Core Anni heuristic (method.gg / Icy Veins): **Metamorphosis at 0–1 Voidfall
stacks or when Untethered Rage is about to expire; Spirit Bomb (≈6 souls) or
Soul Cleave (≈3 souls) at 3 Voidfall stacks; keep Fracture on cooldown always**
to feed Voidfall.

---

## AoE / cleave

Both trees: `variable.aoe` triggers at **3+ targets** (Spirit Bomb target count).
In AoE —

- **Spirit Bomb** is the priority spender (fragment threshold drops by 1); Soul
  Cleave only to avoid capping.
- **Immolation Aura** rises in priority (Fallout spawns fragments off it).
- **Sigil of Flame** and **Throw Glaive** (Bouncing Glaives) add cleave.
- Pre-place **Sigil of Spite** and use **Soul Carver** to flood fragments into
  back-to-back Spirit Bombs.
- Two-target cleave plays like single target with Spirit Bomb used a touch more.

## Pre-combat / opener

APL precombat: **Sigil of Flame** → **Sigil of Spite** (AR always; Anni only
with Soul Carver talented) → **Immolation Aura**.

- **Aldrachi Reaver:** Immolation Aura → Sigil of Flame → Fiery Brand →
  Immolation Aura → Sigil of Spite → **Reaver's Glaive** → empowered Fracture →
  empowered Soul Cleave → into the loop.
- **Annihilator:** Immolation Aura → Sigil of Spite → Fiery Brand → Immolation
  Aura → Fracture (if <4 fragments) → Spirit Bomb → **Metamorphosis** →
  Fracture → Spirit Bomb → into the loop.

## TODO

- [ ] Re-distill if the simc midnight branch publishes an updated 12.0.7 APL
      revision (current pull WoW 12.0.7.67808).
- [ ] Sanity-check the opener against a top WCL Vengeance log
      (`wowkb.wcl rankings` → `casts`).
- [x] Confirm Spirit Bomb's cooldown value — **~25s (haste-reduced)**, resolved
      2026-07-14 via DB2 (SpellCooldowns spell 247454, CategoryRecoveryTime
      25000ms, not charge-based). Documented under Fragment targeting.

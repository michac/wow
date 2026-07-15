---
title: Unholy Death Knight — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Unholy.simc  # tier 1 APL (default = Rider), talents=CwPAAAAA… 2026-07-11
  - https://www.method.gg/guides/unholy-death-knight/playstyle-and-rotation  # tier 3, 12.0.7 (upd. 2026-06-16), 2026-07-11
  - https://www.method.gg/guides/unholy-death-knight  # tier 3, 12.0.7 overview, 2026-07-11
confidence: high
---

# Unholy Death Knight — Rotation (Rider of the Apocalypse, Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1) — the shipped profile
is `MID1_Death_Knight_Unholy_Rider`, i.e. **Rider of the Apocalypse is the simc
default**. Method.gg (Tier 3) corroborates the ordering and adds the San'layn
branch. The APL splits on enemy count: **single_target (<3)** vs **aoe (≥3)**.

> **Midnight loop in one breath.** Keep two diseases up (**Dread Plague** ST /
> **Virulent Plague** multi, both from **Outbreak**), build **Lesser Ghoul**
> stacks with **Festering Strike**, consume them with **Scourge Strike**, spend
> Runic Power with **Death Coil** (→ **Necrotic Coil** during Forbidden
> Knowledge) or **Epidemic** in AoE, and press **Putrefy** on cooldown —
> concentrating its charges inside **Dark Transformation**. Festering Wounds are
> gone; Lesser Ghoul stacks are the maintenance resource now. See `abilities.md`
> for the mechanic rework details and `builds.md` for talents.

## Resource logic (the APL's `spending_rp` gate)

The APL only spends Runic Power (Death Coil / Epidemic as a *spender*) when
`spending_rp` is true, i.e. one of:
- **Rune < 2** (about to be starved of Rune actions — dump RP so you don't cap),
- **Forbidden Knowledge is up** and (Rune < 4 or the Gargoyle is active), or
- a **Sudden Doom** proc is available (free, empowered — always spend it).

Otherwise it prefers Rune actions (Festering Strike / Scourge Strike / Putrefy)
so Runic Power keeps flowing. This is the ST/AoE spend cadence — don't hard-cast
Death Coil just because you have the RP unless one of the above holds.

## Pre-combat

- **Raise Dead** (get the permanent Ghoul out) and `snapshot_stats`.
- Open on the pull with **Outbreak** to seed diseases (unless running
  Blightburst, which delays Outbreak behind the first Putrefy).

## Cooldown rules

- **Stack everything into the Dark Transformation window.** The burst window is
  **Army of the Dead + Dark Transformation + on-use trinket + potion** fired
  together (`cds_active` in the APL = Ghoul Army active, Forbidden Knowledge up,
  or Dark Transformation up with >5s left). Externals like Power Infusion are
  told to land during Dark Transformation / Forbidden Knowledge.
- **Outbreak** — refresh only when **Dread Plague or Virulent Plague** is
  missing (never clip a healthy disease). With Blightburst, gate it so Putrefy
  goes first.
- **Army of the Dead** — on cooldown inside the planned burst; triggers
  **Forbidden Knowledge** (Death Coil → Necrotic Coil for 30s) and, with
  Commander of the Dead, buffs your minions.
- **Soul Reaper** — the APL fires it well before execute range (Reaping /
  Dark Transformation grant near-free casts). It's used as a burst button, not
  only <35% HP. Also dumped if `fight_remains` is short.
- **Putrefy** — press on cooldown, but **bank a charge for Dark Transformation**
  when Soul Reaper/Reaping is talented: cast at **max charges** (unless a Sudden
  Doom proc is pending and Dark Transformation is >9s away), and freely **while
  Dark Transformation is up**. Also dumped if the fight/adds are about to end.
- **Dark Transformation** — on cooldown; the APL prefers to have the Ghoul Army
  active (or Army >30s away) so Commander of the Dead overlaps.

## Single target (<3 enemies)

Priority as the APL orders it:

1. **Festering Strike** to keep **Festering Scythe** alive (if talented) — refresh
   when the buff/trigger is about to expire (≤3s).
2. **Scourge Strike** — San'layn only: with a Lesser Ghoul stack + Gift of the
   San'layn, when Blood Queen stacks <5 and Vampiric Strike is up (banks Essence).
3. **Death Coil** on a **Sudden Doom** proc (free + empowered — highest priority spend).
4. **Scourge Strike** with a Lesser Ghoul stack while **Blighted** is up.
5. **Death Coil** when `spending_rp` (see resource logic above).
6. **Putrefy** when target >35% HP (or no Soul Reaper) **and** Commander of the
   Dead has >9s left (or isn't talented) — i.e. inside the buffed window.
7. **Scourge Strike** with a Lesser Ghoul stack (spend the stack).
8. **Festering Strike** (build a Lesser Ghoul stack).
9. **Death Coil** (RP dump / filler).

## Cleave & AoE (≥3 enemies)

The APL's `aoe` list. Key breakpoint: **`epidemic_prio` = 4+ targets** (or 6+
while Forbidden Knowledge is up). So at *exactly 3* targets it still spends with
**Death Coil**, not Epidemic; Epidemic takes over at 4+.

1. **Death and Decay** — lay it down if not ticking (with Desecrate), or to feed
   **Putrefy's cooldown reduction** via Cycle of Death. Position for sustained contact.
2. **Festering Strike** (lowest-HP target) to maintain **Festering Scythe**.
3. **Epidemic** when `spending_rp` **and** `epidemic_prio` (4+ targets).
4. **Death Coil** (lowest-HP target) when `spending_rp` and *not* epidemic_prio (3 targets).
5. **Festering Strike** on a target with **0 Lesser Ghoul** stacks (build).
6. **Scourge Strike** on a target with **≥1 Lesser Ghoul** stack (consume).
7. **Epidemic** (epidemic_prio, non-spending overflow).
8. **Death Coil** (lowest-HP, filler at 3 targets).

Cooldowns (Outbreak / Army / Dark Transformation / Soul Reaper / Putrefy) run
from the shared `cooldowns` list above the split, so they fire in AoE too —
Putrefy's target strike + explosion is strong multi-target damage.

## Hero-tree branches

- **Rider of the Apocalypse (default, raid/ST).** No hero-specific rotational
  button beyond passives — **Rider's Champion** summons the Four Horsemen
  passively and **Apocalypse Now** is the capstone burst. Just execute the
  priority above; the horsemen ride along with your cooldowns. Best single-target
  and strong cleave (Method).
- **San'layn (sustained cleave alt).** Adds **Vampiric Strike** management:
  Vampiric Strike replaces some Scourge Strikes and builds **Essence of the Blood
  Queen** stacks (to 5). The San'layn priority inserts, before the generic
  Scourge/Festering line: build Festering Strike to ≤3 stacks pre-Dark
  Transformation, then **Vampiric Strike when Blood Queen stacks are low**, and
  spends Death Coil at high RP / on Sudden Doom. **Gift of the San'layn** is the
  layered burst tied to Dark Transformation. Priorities are otherwise the same
  shape as Rider.

## TODO

- [ ] Sanity-check the opener/burst window against a top WCL Unholy log
      (`wowkb.wcl rankings` → `casts`).
- [ ] Capture a distilled San'layn simc profile if one ships (the default MID1
      profile is Rider-only; San'layn ordering here is from method.gg, Tier 3).
- [ ] Confirm method.gg's "Graveyard (6+ targets)" AoE step — it does **not**
      appear as a spell in the Tier-1 simc APL; may be a guide rendering of an
      Epidemic breakpoint or a talent. @verify-ingame

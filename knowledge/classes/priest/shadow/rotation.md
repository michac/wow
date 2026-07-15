---
title: Shadow Priest — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Priest_Shadow.simc  # tier 1 APL (Voidweaver default profile), 2026-07-11
  - https://www.method.gg/guides/shadow-priest/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/shadow-priest-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Shadow Priest — Rotation (Midnight S1)

Distilled from the SimulationCraft **MID1_Priest_Shadow** APL (Tier 1 — the
shipped default is the **Voidweaver** profile) and corroborated by method.gg /
Icy Veins (Tier 3). Shadow is a DoT builder/spender: keep **Shadow Word: Pain**
and **Vampiric Touch** on everything, build **Insanity** with short-CD
generators, and spend it keeping **Shadow Word: Madness** ticking. **Psychic
Link** splatters your damage onto all DoTed targets, so multi-dot upkeep is
the whole AoE game — "the priority of the spells does not change" in AoE, you
just widen your DoT coverage before pressing burst.

> **The two hero trees share one skeleton** and differ only in a few slotted
> buttons: **Voidweaver** adds **Void Torrent → Entropic Rift → Void Blast**;
> **Archon** adds **Halo** and the **Mind Flay: Insanity** empowered filler.
> The simc default profile is Voidweaver; the Archon list below is from
> method.gg. Exact Insanity costs/CDs are corroborated at Tier 3 only —
> @verify-ingame the numbers before treating them as exact.

## Pre-combat

- Ensure **Shadowform** is up (cast if missing).
- **Tentacle Slam** just before the pull (applies Vampiric Touch broadly / banks value).
- Snapshot stats; racial (e.g. Arcane Torrent) as filler.

## Cooldown rules

- **Sync Voidform + Power Infusion** — press them together for the burst window;
  the APL gates Power Infusion on Voidform being up (or not being talented).
- **Pre-apply DoTs before Voidform** so you don't waste globals re-dotting mid-CD.
- **Potion / racials (Berserking, Blood Fury, Fireblood, Ancestral Call) only
  inside the Voidform + Power Infusion window** (or in the last few seconds of
  the fight).
- **Trinkets** fire during Voidform / while Power Infusion has ≥10s left (Entropic
  Rift up for the on-use damage trinkets), or when the fight is about to end.
- **Halo** (Archon) on cooldown; **Voidform** when `active_dot.shadow_word_pain
  >= active_dot.vampiric_touch` (DoTs spread first).
- **Desperate Prayer** reactively when Shadow Word: Death self-damage or a spike
  drops you below **~75%** health.

## Single target — Voidweaver (simc default APL)

1. **Shadow Word: Death** — if the target has an absorb shield (or forced) and
   **Devour Matter** is talented (pops the shield for burst).
2. **Shadow Word: Madness** — the spender. Cast when it's not ticking / has
   ≤~1 GCD left, when **Insanity deficit ≤35** (don't overcap), on a **Mind
   Devourer** proc, or when the Entropic Rift is up. This is the button that
   must never fall off the priority target.
3. **Void Volley** — Insanity generator, high priority (don't lose charges).
4. **Void Blast** — spends the **Entropic Rift** window; prioritize while SWM is
   ticking or the Rift is about to expire.
5. **Tentacle Slam** — to refresh **Vampiric Touch** (refreshable) or to avoid
   capping its charges.
6. **Void Torrent** — the Voidweaver burst channel; cast when DoTs are up and
   you're not holding for incoming adds (opens the Entropic Rift; wants near-full
   Mastery value).
7. **Shadow Word: Pain** — as a filler *only if talented into Invoked Nightmare*
   and refreshable on a target living >12s.
8. **Mind Blast** — dump charges when VT + SW:P are up (unless a Mind Devourer
   proc is being saved).
9. **Tentacle Slam** — for Void Apparitions / Maddening Tentacles value.
10. **Vampiric Touch** — hard-cast to apply/refresh on targets living >12s when
    Tentacle Slam won't cover it.
11. **Shadow Word: Death** — execute (< 20%, or < 35% with Deathspeaker), and as
    an Inescapable Torment trigger while a fiend/wraith pet is active.
12. **Mind Flay** — filler channel (interrupt after 3 ticks to resume priority).
13. Movement fillers: **Tentacle Slam** / **Shadow Word: Death** / **Shadow
    Word: Pain** while moving.

## Single target — Archon (method.gg)

Same skeleton; the burst buttons change:

1. **Shadow Word: Pain** (if Invoked Nightmare talented) → maintain **Vampiric Touch**.
2. **Halo** on cooldown → **Voidform** → **Power Infusion**.
3. **Shadow Word: Madness** (spend when inactive / expiring / near Insanity cap).
4. **Void Volley** → **Tentacle Slam** (VT upkeep / charge management) → **Mind Blast**.
5. **Mind Flay: Insanity** when SWM is active (empowered filler, procs off Halo).
6. **Shadow Word: Death** in execute.
7. Filler: **Mind Flay**.

## AoE / multi-dot (3+ targets)

Per the APL's `aoe_variables`, the spec computes how many Vampiric Touches it
can keep up (up to ~12) and prioritizes DoT coverage before burst. **Spell
priority is unchanged from single target** — the work is the dotting:

- **Tentacle Slam** auto-spreads/refreshes Vampiric Touch across **6–12 targets**;
  keep its charges rolling. Hold a charge if adds are imminent.
- **Without Voidform ready**: manually **Vampiric Touch** an extra 4–5 targets so
  the majority are DoTed before you press burst.
- **With Voidform available**: dot any target that will live a decent while.
- Then run the single-target priority — **Shadow Word: Madness**, **Void
  Volley**, **Void Blast** / **Halo**, **Mind Blast** — and let **Psychic Link**
  cleave it onto every DoTed enemy.
- **Shadow Word: Pain** upkeep matters more in AoE (Voidform wants
  `SW:P dots ≥ VT dots`), and with **Invoked Nightmare** SW:P becomes an active
  AoE filler.

## Hero-tree branches (summary)

- **Voidweaver** — the extra buttons are **Void Torrent** (opens Entropic Rift),
  **Void Blast** (spends the Rift), and stronger Devour Matter / SW:D shield-pop
  interplay. Burst-window-centric; the simc default.
- **Archon** — the extra buttons are **Halo** (on-CD, enables **Mind Flay:
  Insanity** procs) and a more sustained/cleave feel. No Void Torrent / Void
  Blast in the priority.

## TODO

- [ ] Nail exact Insanity costs (SW:Madness spend, generator values) and the
      Void Volley / Void Torrent / Voidform cooldowns against Tier-1 game data
      or in-game — current numbers are Tier-3 approximations (@verify-ingame).
- [ ] Distill the Archon-specific simc list if/when the midnight branch ships an
      `MID1_Priest_Shadow_Archon` profile (only the Voidweaver default exists as
      of 2026-07-11).
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` → `casts`).

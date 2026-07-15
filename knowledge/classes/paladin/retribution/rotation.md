---
title: Retribution Paladin — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Paladin_Retribution.simc  # tier 1 APL (PRIMARY), 2026-07-11
  - https://www.method.gg/guides/retribution-paladin/playstyle-and-rotation  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/retribution-paladin-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Retribution Paladin — Rotation (Templar, Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1), corroborated by
method.gg and Icy Veins (Tier 3). The S1 default hero tree is **Templar**,
which reshapes the finisher priority around **Hammer of Light**: after **Wake
of Ashes** your spender slot becomes Hammer of Light for 20s, and **Light's
Deliverance** later grants free Hammer of Light procs. **Herald of the Sun** is
a viable alternative but is not the button-backbone below.

The engine is a Holy Power economy: build with Judgment / Blade of Justice /
the Templar Strike (or Crusading Strikes) filler / Wake of Ashes / Divine Toll,
and spend at 5 Holy Power on **Final Verdict** (ST) or **Divine Storm** (AoE) —
except that a ready **Hammer of Light** always jumps the spender queue. Ret
"spends aggressively": don't sit on 5 Holy Power just to keep a builder on
cooldown, because procs (Art of War, Empyrean Power) come fast.

## Pre-combat

- Buff **Devotion Aura** (or the raid-assigned aura); ensure a Blessing is set.
- Pre-pull on-use trinket (e.g. Algeth'ar Puzzle Box) if equipped.

## Opener (Templar, Execution Sentence build)

1. **Blade of Justice** (apply Expurgation if Holy Flames)
2. **Judgment**
3. **Avenging Wrath** (skip the manual cast if playing **Radiant Glory** — it
   auto-triggers off Wake of Ashes / Execution Sentence)
4. On-use trinkets + combat potion
5. **Execution Sentence**
6. **Wake of Ashes**
7. **Hammer of Light** (now enabled by Wake of Ashes)
8. **Divine Toll**
9. → fall into the single-target priority (Final Verdict ×2, etc.)

## Cooldown rules

- **Avenging Wrath + Execution Sentence are paired** — cast ES just before
  wings so its ~10s-delayed detonation lands inside the buff, and so you're
  spending max Holy Power during the window (feeds Crusade stacks / the ES
  final tick). The APL gates ES on `cooldown.wake_of_ashes.remains<gcd`, i.e.
  fire ES immediately before Wake of Ashes.
- **Potion / racials / on-use trinkets** sync to the Avenging Wrath window
  (or, on Radiant Glory, to `cooldown.wake_of_ashes.remains=0`). The APL
  matches trinket cooldown cadence to Avenging Wrath's 60s.
- **Radiant Glory build:** you never press Avenging Wrath — Wake of Ashes and
  Execution Sentence generate the wings automatically, so treat WoA/ES as the
  burst trigger and align externals (Power Infusion, potion) to WoA coming up.
- **Wake of Ashes** is gated so it doesn't clip Execution Sentence
  (`cooldown.execution_sentence.remains>4`) and, on non-Radiant-Glory, waits
  for wings to be >6s away.
- **Sub-8s fight remaining:** dump Divine Toll / remaining Holy Power; the APL
  relaxes the add-timing gates late in a fight.

## Single target (Templar)

1. **Avenging Wrath** — on cooldown (skip if **Radiant Glory**)
2. **Execution Sentence** — on cooldown, lined up with wings
3. **Hammer of Light** — whenever castable (from Wake of Ashes, or a free
   **Light's Deliverance** proc). Top spend priority; the APl's finisher list
   fires it before Final Verdict/Divine Storm, with extra rules to dump the
   *free* proc before it expires or before Avenging Wrath ends.
4. **Final Verdict at 5 Holy Power** (or at 4 with a Crusading Strikes auto
   about to land) — main single-target spender
5. **Wake of Ashes** — on cooldown (re-enables Hammer of Light)
6. **Divine Toll** — on cooldown
7. **Blade of Justice** — refresh **Expurgation** if missing, or spend an
   **Art of War** / **Righteous Cause** proc (free instant)
8. **Final Verdict at 4 Holy Power**
9. **Blade of Justice** (without a proc, on cooldown)
10. **Judgment** → **Hammer of Wrath** (Hammer of Wrath usable any-health
    during wings, or below ~20% otherwise; free/high with Walk Into Light)
11. **Divine Storm** — only on an **Empyrean Power** proc (free AoE, still a
    single-target gain on the proc)
12. **Final Verdict at 3 Holy Power** — spend rather than overcap
13. **Templar Strike** → **Templar Slash** (or **Crusader Strike**) — filler
    builder to keep Holy Power flowing

## Cleave / AoE (3+ targets)

Swap to the AoE list at **3+ enemies** — or **2+** with **Tempest of the
Lightbringer** talented and **Jurisdiction** not talented (the APL's
`variable.ds_castable` encodes exactly this threshold; Empyrean Power also
flips a single hit into Divine Storm).

Same skeleton as single target, but **Divine Storm replaces Final Verdict** as
the spender everywhere:

1. **Avenging Wrath** (skip on Radiant Glory)
2. **Execution Sentence**
3. **Hammer of Light** (still top spend when enabled)
4. **Divine Storm at 5 Holy Power** (or 4 with a pending Crusading Strikes auto)
5. **Wake of Ashes** — cone hits everything, big AoE Holy Power
6. **Divine Toll** — up to 5 Judgments + (with **Divine Hammer**) summons
   **Empyrean Hammers** for sustained area damage
7. **Blade of Justice** — Expurgation missing, or Art of War proc
8. **Divine Storm at 4 Holy Power**
9. **Blade of Justice** (no proc)
10. **Judgment** / **Hammer of Wrath**
11. **Divine Storm at 3 Holy Power**
12. **Templar Strike / Templar Slash** (or Crusader Strike) filler

## Hero-tree branches

- **Templar (default):** the priority above. The identity is the Wake of Ashes
  → Hammer of Light loop, **Shake the Heavens** / **Empyrean Hammer** procs,
  and free **Light's Deliverance** Hammer of Light casts to dump inside wings.
  Wake of Ashes also becomes a defensive with **Sacrosanct Crusade**.
- **Herald of the Sun (alternative):** builds around **Dawnlight** /
  **Eternal Flame** and the **Sun's Avatar** burst window instead of Hammer of
  Light — there is no Hammer-of-Light spender swap. Slightly behind Templar in
  S1 sims; play priority is otherwise similar (build → spend Final Verdict/
  Divine Storm, align Avenging Wrath). Not distilled line-by-line here.

## Notes / open items

- The two spender-swap builds differ only in **cooldown source**: standard
  (press **Avenging Wrath** manually) vs **Radiant Glory** (Wake of Ashes /
  Execution Sentence auto-cast the wings — one fewer button, tighter alignment).
  See `builds.md`.
- Execution Sentence's exact delay/cost and Wake of Ashes / Divine Toll base
  cooldowns are talent-modified; re-confirm in-game against tooltips. @verify-ingame
- Re-distill if the simc midnight branch publishes a retuned 12.0.7 APL.

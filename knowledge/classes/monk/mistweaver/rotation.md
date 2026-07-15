---
title: Mistweaver Monk — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/mistweaver-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/mistweaver-monk-pve-dps-guide  # tier 3, 12.0.7 (damage priority)
confidence: medium
---

# Mistweaver Monk — Rotation (Midnight S1)

> **No SimulationCraft APL exists for this spec.** simc does not model healing,
> and the midnight branch ships only `MID1_Monk_Brewmaster/_Windwalker` profiles
> — there is **no `MID1_Monk_Mistweaver.simc`** (confirmed via the simc midnight
> `profiles/MID1` listing, 2026-07-11). This priority is therefore distilled from
> Tier-3 guides (method.gg, upd. 2026-06-16; Icy Veins 12.0.7) rather than a
> Tier-1 APL — **confidence medium**. Re-verify the ordering in-game.

Mistweaver has no rigid single rotation. The mantra is **"keep everything on
cooldown"** and **pre-plan the major cooldowns against incoming damage**. Two
loops run at once: a **healing/HoT** loop (Renewing Mist, Enveloping Mist,
Soothing Mist, Vivify/Sheilun's Gift) and a **Fistweaving damage** loop
(Rising Sun Kick / Rushing Wind Kick, Blackout Kick, Tiger Palm, Spinning Crane
Kick) whose damage is converted to raid healing by **Ancient/Jadefire
Teachings**. When nobody needs a direct heal, you are meleeing to heal.

## Pre-combat / opener

- Pre-cast **Renewing Mist** so it's ticking (and its charges are ready to
  spend into a cooldown window).
- Open the first big window with **Thunder Focus Tea → Renewing Mist** (banks
  the Secret Infusion haste), then the planned Celestial (**Invoke Yu'lon** for
  raid / **Invoke Chi-Ji** for M+).

## Cooldown rules

- **Don't stack high-impact cooldowns.** Revival and Invoke Yu'lon/Chi-Ji
  should **not** fire together for throughput — spread them across the damage
  events. Save Revival's real value (raid-wide **dispel**) for a dispel check.
- **Thunder Focus Tea on cooldown (~30s)** — it's off-GCD and empowers the next
  Renewing Mist / RSK / Enveloping Mist / Vivify (and drives Secret Infusion +,
  under Master of Harmony, Aspect of Harmony). Pick the empower target per the
  hero-tree loop below.
- **Mana Tea** — spend it around ~20 stacks when there's a spare GCD; it
  discounts your mana while active. Life Cocoon (with Refreshment) feeds stacks.
- **Life Cocoon** — pre-shield the tank/target before a known hit; with
  Refreshment it can be used ~on cooldown in raid for the Mana Tea stacks.
- **Celestial Conduit** (Conduit of the Celestials) — a ~90s heal/damage channel
  for burst windows; movement-enabled, and can be ended early via Unity Within.

## Single-target / spot-healing priority

1. **Vivify** immediately if anyone risks death (or **Life Cocoon** for a
   lethal single-target hit).
2. **Thunder Focus Tea** (empower the planned spell) when available.
3. **Rising Sun Kick** / **Rushing Wind Kick** on cooldown (damage→heal core).
4. **Sheilun's Gift** on a critically injured target (if talented).
5. **Renewing Mist** — keep both charges cycling; don't cap.
6. **Mana Tea** at ~20 stacks.
7. **Enveloping Mist** — especially when buffed instant/cheap (Celestial out,
   TFT, or a Strength of the Black Ox proc under Conduit).
8. **Vivify** when targets are meaningfully injured (its Renewing-Mist cleave
   makes it efficient with HoTs spread).
9. **Blackout Kick → Tiger Palm** to fill: build Teachings of the Monastery
   stacks and fish RSK resets (the damage is healing via Teachings).

## Damage (Fistweaving) priority

When healing is under control, do damage — it heals the raid:

- **Single target:** Rising Sun Kick on CD → Blackout Kick at 3–4 Teachings of
  the Monastery stacks → Tiger Palm to build stacks. (Awakened Jadefire makes
  Tiger Palm strike twice for two stacks.)
- **~4 targets:** Rising Sun Kick on CD → Blackout Kick with remaining stacks →
  **Spinning Crane Kick**.
- **5+ targets:** **Spinning Crane Kick** primarily (spend Dance of Chi-Ji
  procs on it).
- **Touch of Death** on eligible low-HP targets for a burst of damage→heal.
- **Crackling Jade Lightning** as a ranged filler when you must heal at range;
  it's empowered by **Jade Empowerment** after Thunder Focus Tea.

## Raid / AoE-healing priority

1. **Life Cocoon** to prevent a death.
2. **Thunder Focus Tea**.
3. **Rising Sun Kick** / **Rushing Wind Kick** on cooldown.
4. **Spinning Crane Kick** with a **Dance of Chi-Ji** proc (free AoE
   damage→heal).
5. **Sheilun's Gift** on critical targets.
6. **Renewing Mist** at full charges (spreads the HoT web that Vivify cleaves).
7. **Mana Tea** at ~20 stacks.
8. **Spinning Crane Kick** at 4+ enemies for the AoE conversion.
9. **Enveloping Mist** when a proc/CD makes it instant/cheap.
10. **Vivify** to mop up raid-wide injury (cleaves off Renewing Mist).

## Hero-tree branches

### Conduit of the Celestials (raid + M+ default)

- Point **Thunder Focus Tea at Renewing Mist** to extend its duration.
- **Celestial Conduit** grants cooldown reduction to **Rushing Wind Kick** and
  **Renewing Mist**; **alternate the two** to keep dragging both cooldowns down
  — this is the **ramping loop** that grows your Renewing Mist count on the raid.
- **Invoke Yu'lon raid loop:** TFT + Renewing Mist → Yu'lon → Enveloping Mist ×2
  → Renewing Mist → Rushing Wind Kick (extends via Rising Mist) → instant Vivify
  (Vivacious Vivification) → repeat.

### Master of Harmony (alt, damage-leaning in M+)

- **Thunder Focus Tea procs Aspect of Harmony** — the tree's core: it **banks
  vitality** from your healing/damage and releases it later. Play is largely
  **passive** beyond hitting TFT on cooldown to keep Aspect fed.
- Most healing flows through **Ancient Teachings** (damage→heal) synergizing
  with Aspect of Harmony, so keep the Fistweaving damage loop rolling.
- **Invoke Chi-Ji M+ loop:** TFT + Enveloping Mist (banks Secret Infusion vers /
  feeds Spiritfont) → Invoke Chi-Ji → instant Enveloping Mists as needed →
  Rising Sun Kick (Jadefire Teachings converts to healing) → Blackout Kick
  spending 4 Teachings stacks → Rising Sun Kick if reset → Sheilun's Gift /
  Enveloping Mist for direct healing → Tiger Palm + Blackout Kick to rebuild
  stacks for RSK resets.

## TODO

- [ ] No Tier-1 APL exists (simc doesn't sim healers) — if a community
      healer-sim or WCL top-log cast sequence becomes available, corroborate the
      ordering and raise confidence.
- [ ] Verify the exact single-target vs AoE Fistweaving thresholds and Teachings
      stack counts in-game.

---
title: Arcane Mage — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Mage_Arcane.simc  # tier 1 APL (primary), fetched 2026-07-11
  - https://www.method.gg/guides/arcane-mage/playstyle-and-rotation  # tier 3, upd. 2026-06-29 (12.0.7)
  - https://www.method.gg/guides/arcane-mage  # tier 3, upd. 2026-06-29
  - https://www.icy-veins.com/wow/arcane-mage-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: high
---

# Arcane Mage — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (tier 1), corroborated by
method.gg (12.0.7, upd. 2026-06-29). The APL branches by **hero tree**:
`spellslinger` / `spellslinger_orbm` (Splintering Sorcery, ± Orb Mastery) and
`sunfury` (Spellfire Spheres). Both are S1-viable — see `builds.md`.

**The whole spec is one sentence:** build **Arcane Salvo** stacks (via Arcane
Missiles waves, or Arcane Orb with *Orb Mastery*) to the **20-stack** threshold
(**25** on Sunfury), then unload empowered **Arcane Barrages** inside a **Big
Burn** (Arcane Surge + Touch of the Magi). Arcane Blast is the filler that
fishes **Clearcasting**, which fuels the free builders that stack Salvo.

> **12.0.7 "Revelations" (live 2026-06-16): no direct Arcane changes** (method,
> 2026-06-29 — the patch added Sporefused gear and the Omnium Folio, not spec
> retuning). Priority ordering below matches the current simc midnight APL.
> **Midnight removed *Nether Precision*** (base Arcane Missiles buffed instead),
> so there is no Missiles→Blast empowerment step anymore. @verify-ingame

## Pre-combat

- **Arcane Intellect** up; **Mirror Image** pre-cast; snapshot stats.
- **Spellslinger:** open into **Arcane Orb**, then spam Arcane Blast (Arcane
  Pulse if AoE) to reach **20 Arcane Salvo** → **Arcane Surge** → **Touch of the
  Magi** → dump **Arcane Barrage**.
- **Sunfury:** **potion/trinkets** → **Arcane Surge** first → **Arcane Missiles**
  to build Salvo → **Arcane Blast** → **Touch of the Magi** when Arcane Surge has
  **~5s left** (so Magi carries into the Arcane Soul window) → **Arcane Barrage**
  spam during **Arcane Soul**.

## Cooldown rules

- **Use Arcane Surge and Touch of the Magi on cooldown and together** — this is
  the "Big Burn." Arcane Surge is **90s**; Touch of the Magi is **45s**, so one
  **"Miniburn"** (solo Touch of the Magi) falls between each Big Burn. **Never
  delay the Miniburn** — desyncing the two cooldowns wrecks the rotation.
- **Spellslinger:** cast **Touch of the Magi immediately after Arcane Surge**.
- **Sunfury:** **delay Touch of the Magi** until Arcane Surge has ~5s remaining,
  extending the burst buffs into the **Arcane Soul** window.
- **Potion / racials / on-use trinkets** sync to the Arcane Surge (+ Touch of the
  Magi) window; the APL gates them on `buff.arcane_surge.up` & the Magi debuff.
- **Evocation** only when **mana < ~10%** and no burst is active/imminent
  (`buff.arcane_surge.down & touch_of_the_magi.down & arcane_surge.remains>10`).
  Cancel the channel once mana ≥ 95%.
- End-of-fight (`fight_remains` small): dump **Arcane Barrage**, and burn any
  banked Clearcasting into a final **Arcane Missiles/Orb** at high Salvo.

## Single target — Spellslinger (Orb Mastery, the S1 default)

1. **Arcane Orb** — after an Arcane Barrage, when you have **Clearcasting** and
   Salvo ≤ ~14 (Orb Mastery: Orb is your Salvo builder, Missiles is unused).
2. **Arcane Barrage** at **4 Arcane Charges** and **Salvo ≥ 20** (Touch of the
   Magi not about to come up). *Polished Focus* refunds 5 Salvo and adds +15%,
   so hold Barrage for **exactly 20**.
3. **Presence of Mind** (off-GCD) at <2 Arcane Charges when no Orb/Clearcasting
   is available, to instant-cast Arcane Blast and rebuild.
4. **Arcane Blast** (with Presence of Mind, then) as the filler/charge-builder.
5. **Arcane Pulse** if it's an AoE count or charges are low and mana > 30%.
6. **Arcane Blast** — default filler / Clearcasting fishing.
7. **Arcane Barrage** when out of mana (spend rather than starve).

## Single target — Sunfury

1. **Arcane Barrage** if **Arcane Soul** is up (free, instant, empowered — spam it).
2. **Arcane Barrage** at 4 Arcane Charges when the burst is ending (Arcane
   Surge/Magi about to fall off) with high Salvo, or at **25 Salvo** + 4 charges.
3. **Arcane Missiles** on **Clearcasting** when Salvo is below ~15 (build stacks;
   Missiles is the Salvo engine for Sunfury). Chain the channel.
4. **Arcane Orb** if **< 2 Arcane Charges** (rebuild charges cheaply).
5. **Arcane Pulse** on AoE counts / low charges with mana > 30%.
6. **Arcane Blast** — filler and Clearcasting fishing.
7. **Arcane Barrage** when out of mana.

## Cleave / AoE (3+ targets)

- Same skeleton; **Arcane Pulse** becomes a maintained AoE builder once
  `active_enemies ≥ pulse_aoe_count` (2 + Orb Mastery), and **Arcane Orb** rises
  in priority (it's multi-target and, with Orb Mastery, your Salvo source).
- **Spellslinger AoE:** Arcane Orb with Clearcasting at ≤14 Salvo → Arcane
  Barrage at 20 Salvo → Arcane Pulse (3+) → Arcane Barrage when OOM.
- **Sunfury AoE:** priority identical to its single-target list with **Arcane
  Blast** as the primary filler; **Arcane Explosion** is a niche 4+-target filler
  at <2 charges if *Impetus* is not talented.
- **High Voltage** (Spellslinger) lets **Arcane Barrage restore Arcane Charges**
  below the Salvo threshold, smoothing charge upkeep in AoE.

## Hero-tree branches (summary)

- **Spellslinger (Splintering Sorcery + Orb Mastery):** Arcane Orb is the Salvo
  builder (a Clearcasting Orb fires **three** orbs, 2 Salvo each); **Arcane
  Missiles is not used**. Passive **Arcane Splinters** proc extra Salvo (~25%).
  *Polished Focus* → hold Barrage for exactly 20 Salvo.
- **Sunfury (Spellfire Spheres):** **Clearcasting** is the scaling engine —
  Arcane Surge, Touch of the Magi, and Arcane-Soul Barrages guarantee procs.
  Building to **25** Salvo and the **Arcane Soul** free-Barrage window are the
  payoff; Touch of the Magi is delayed to overlap Arcane Soul.

## TODO

- [x] Single-target + AoE priority (both hero trees) — simc midnight APL, 2026-07-11
- [x] Cooldown pairing (Big Burn / Miniburn) — method.gg + APL, 2026-07-11
- [ ] Sanity-check opener vs a top WCL log (`wowkb.wcl rankings` → `casts`)
- [ ] Confirm exact Arcane Orb / Arcane Pulse / Touch of the Archmage cooldowns
      in-game (marked `@verify-ingame` in `abilities.md`)

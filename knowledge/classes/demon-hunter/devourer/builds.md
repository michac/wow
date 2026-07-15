---
title: Demon Hunter Devourer — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/devourer-demon-hunter/talents  # tier 3, Hype, upd. 2026-06-17, 2026-07-11
  - https://www.method.gg/guides/devourer-demon-hunter/gearing  # tier 3, 2026-07-11 (Mastery>Haste, Gaze of the Alnseer trinket)
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer.simc  # tier 1 talent string, 2026-07-11
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer_Void-Scarred.simc  # tier 1, 2026-07-11
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-guide  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Demon Hunter Devourer — Talents & Builds (Midnight S1)

Layers on top of `talents.md` / `talents.json` (the full Tier-1 tree). This file
is the *narrative* — which hero tree, which loadouts, and what the key talents
change. See `rotation.md` for how the picks play out button-to-button.

## Hero tree: **Annihilator everywhere**

**Annihilator is the S1 default for raid and Mythic+.** Method: "Annihilator is
the better choice for raids and Mythic+... way stronger the moment more targets
are present." It is a caster-leaning build that ramps **Voidfall** stacks and
consumes them (with Reap/Eradicate) to call down **3 Void Meteors** via
*Meteoric Fall*. It is flatter outside cooldowns but ramps hard inside **Void
Metamorphosis** — and "barely does damage outside of it," so sharp in-window play
is required.

**Void-Scarred** is the alternative — Void Metamorphosis-centric, ramping
*Burning Blades* with Reap/Cull and lining big hits inside *Student of Suffering*
windows. It has a single-target-competitive **caster** variant and a **melee
hybrid** variant (The Hunt / Hungering Slash / Voidblade weaving). It falls off
in multi-target, so it's a niche ST pick rather than the default.

## Recommended loadouts (talent strings, 12.0.7)

- **Annihilator — raid cleave / M+ (default, Tier-1 simc default profile):**
  `CgcBAAAAAAAAAAAAAAAAAAAAAAA2MmZmZmZmBzMAAAAAAALzYAzAAAAAAAAwMGMmZmZMzMzYmFzYsotNmZmZ2abmZGAjZAIwMzgxMA`
  (simc `MID1_Demon_Hunter_Devourer.simc`). Method's equivalent string:
  `CgcBAAAAAAAAAAAAAAAAAAAAAAA2mxMzMzMzMGmBAAAAAAgxsNYGAAAAAAAAmxMMzMzMzMDzsYGjFZhZmZmt2mZmBwwAQgZMYMD`
- **Annihilator — single target** (Method): swaps **Eradicate → Devourer's Bite**
  and makes **Voidblade** a damage amplifier:
  `CgcBAAAAAAAAAAAAAAAAAAAAAAA2mxMzMzMzMGmBAAAAAAgxsNYGAAAAAAAAmxMMzMzMjZmZYmFzYsILMzMzs12MzMAGGACMzMYMD`
- **Void-Scarred — melee (alternative ST):** incorporates Hungering Slash + The
  Hunt (Tier-1 `MID1_Demon_Hunter_Devourer_Void-Scarred.simc`). Crit becomes
  stronger, Haste weaker.

> ⚠ Import strings are tree-version-sensitive and were captured 2026-07-11 for a
> brand-new spec — **confirm each loads as the right hero tree in-game** before
> trusting (one bad char breaks the import). @verify-ingame

## Key talent interactions

- **Void Metamorphosis** — the build's engine. Activates at **50 Souls**,
  empowers core abilities, and *is* the damage window. Everything else exists to
  fill it and lengthen it.
- **Soul Glutton** (choice vs *Emptiness*) — drops the Meta requirement **50 → 35
  Souls** for more frequent windows, but Fury drains **~25% faster** inside, so
  each window is ~30% shorter. Favored where more, shorter windows beat fewer
  long ones (esp. Void-Scarred melee's fast in/out loops).
- **Devourer's Bite** — makes **Voidblade** (and The Hunt) a **+12%-per-stack
  damage amp** on affected targets; the single-target Annihilator swap (replaces
  Eradicate) and a Void-Scarred ST staple, strong because the charge resets
  inside Meta.
- **Eradicate** — turns **Reap** into an **AoE frontal cone** (after a full Void
  Ray channel); "a massive portion of Devourer's multi-target damage." The AoE/M+
  pick; drop it for Devourer's Bite in pure single target.
- **Moment of Craving** — gates the AoE Eradicate spend (Eradicate at *Moment of
  Craving* active + 10 Souls on the ground).
- **Second Helping** — Reap gains a charge when you fully channel Void Ray,
  smoothing the builder loop.
- **Hungering Slash** — converts Voidblade / The Hunt into melee slashes that
  generate Fury and shatter up to 2 Soul Fragments; the core of the Void-Scarred
  **melee hybrid**.
- **Midnight** (capstone) — enables/empowers **Collapsing Star** so it **always
  crits** (first rank). The payoff for the whole Soul economy. @verify-ingame
- **Student of Suffering** (Void-Scarred) — buff window to line up big casts
  (e.g. Cull) for out-of-Meta damage.
- **Meteoric Fall / Voidfall** (Annihilator) — build **3 Voidfall stacks**, then
  Reap/Eradicate consumes them to call **3 Void Meteors**. The Annihilator damage
  identity (see `rotation.md` — "Reap/Eradicate at 3 Voidfall").

## Gearing

> **Moved to `gearing.md` (2026-07-14).** Stat priority (Mastery > Haste > Crit ≈
> Vers per Method; Void-Scarred melee shifts toward Crit), trinkets, tier set,
> embellishments, enchants, gems, and consumables now live in `gearing.md`. This
> file is talents / loadouts / hero-tree only.

## TODO

- [ ] Verify all import strings load as the correct hero tree in-game.
- [ ] Re-check Annihilator vs Void-Scarred usage split against murlok.io / WCL
      once the spec has ladder history (new spec — no aggregation yet).
- [ ] Confirm Soul Glutton's exact Fury-drain penalty and Meta Soul thresholds.

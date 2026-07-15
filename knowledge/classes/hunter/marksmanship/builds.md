---
title: Marksmanship Hunter — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Hunter_Marksmanship.simc  # tier 1 simc talent string + gear, 2026-07-11
  - https://www.method.gg/guides/marksmanship-hunter/talents  # tier 3, 12.0.7 (upd. 2026-06-16)
  - https://www.method.gg/guides/marksmanship-hunter  # tier 3, 12.0.7 intro (hero-tree framing)
  - https://maxroll.gg/wow/class-guides/marksmanship-hunter-raid-guide  # tier 3, 12.0.7 raid
  - https://www.icy-veins.com/wow/marksmanship-hunter-pve-dps-spec-builds-talents  # tier 3, 12.0.7
  - https://murlok.io/hunter/marksmanship/m+  # tier 2, top-key talent aggregation
confidence: medium
---

# Marksmanship — talents & builds (Midnight Season 1)

Layer this on top of `talents.md` / `talents.json` (the full Tier-1 tree dump);
this file is the narrative on **which** nodes and **why**. Import strings and
per-slot gearing beyond talents are not re-derived here — sim on Raidbots when
it matters.

## Hero tree: Sentinel (default), Dark Ranger (pure ST)

**Sentinel is the S1 default** — maxroll: *"Sentinel currently performs better
in all PvE content and Dark Ranger will not be recommended in this guide."* It
replaces **Spotter's Mark** with **Sentinel's Mark**, adds **Moonlight Chakram**
(a recastable mini-Trueshot that bounces and explodes, also a free Lock and Load),
and **Lunar Storm** (auto-procs when a Mark is consumed — no positioning). It
also grants **Don't Look Back** absorbs for survivability.

**Dark Ranger** is the situational pick for **pure single-target** fights (and is
defensively stronger in general). It replaces **Kill Shot** with **Black Arrow**
— usable above 80% and below 20% HP, or off a **Deathblow** proc — and turns the
Trueshot cast into a one-shot **Wailing Arrow** via **Withering Fire**. The whole
loop is about generating and dumping Deathblow to fire Black Arrow as often as
possible; Black Arrow triples during the Trueshot window.

Both trees are fully supported in the simc APL (`sentst/sentaoe` and
`drst/draoe`). Default to Sentinel; swap to Dark Ranger only when the fight is
"stand and tunnel one target" (maxroll cites e.g. Vorasius).

## Reference talent string (simc MID1, Tier 1, 12.0.7)

```
C4PAAAAAAAAAAAAAAAAAAAAAAYzsMwAGwMsFYWAAAAAAAAAmxMmhZMzMmBjpZMzM22YMzyMzMzMzyYmlBDAAwYmZmZmZAyGMAbMDA
```

This is the simc default profile's loadout (the exact hero tree it encodes must
be confirmed on import — a single bad char breaks the string). Method/Icy Veins
publish per-content variants (raid ST vs M+/AoE vs defensive); pull the current
string from those pages when building for a specific slot. @verify-ingame

## Spec-tree backbone (12.0.7)

Near-universal picks across top guides + murlok top-key data:

- **Aimed Shot / Rapid Fire / Precise Shots** — the core spend/build loop.
- **Trueshot** + **Calling the Shots** — the 2-min burst CD, cut toward ~90s by
  Calling the Shots (choice-node vs **Unerring Vision**).
- **Lock and Load** + **Explosive Shot** — free/instant Aimed Shots.
- **Master Marksman**, **Penetrating Shots**, **Bullseye** — throughput passives.
- **Bulletstorm** + **Volley** + **Double Tap** — the Sentinel Rapid-Fire/Volley
  engine (Double Tap doubles the next Aimed Shot or Rapid Fire; **don't overlap
  a live Double Tap with Trueshot** — consume it first, see `rotation.md`).
- **Trick Shots** (vs **Aspect of the Hydra** choice) — Trick Shots is the true
  AoE build (Multi-Shot on 3+ → Aimed/Rapid cleave); Aspect of the Hydra is the
  low-target-count / cleave-without-setup alternative.
- **Salvo / Volley / Focus Fire / Unload / Windrunner Quiver** — the AoE cluster.
- **Kill Shot** (Sentinel) / **Deathblow** → **Black Arrow** + **Withering Fire**
  + **Wailing Dead** (Dark Ranger).

## Key interactions

- **Precise Shots economy** — Aimed Shot makes Precise Shots; spend them with
  Arcane Shot (ST) / Multi-Shot (AoE) / Kill Shot / Black Arrow, which also
  applies **Sentinel's/Spotter's Mark** to buff the next Aimed Shot. Overcapping
  Precise Shots or Aimed Shot charges is the main throughput leak.
- **Trick Shots enables AoE** — nothing cleaves until Multi-Shot (3+) or Volley
  lights Trick Shots.
- **Bulletstorm** (Sentinel) — Rapid Fire stacks it; each stack adds ~1% Aimed
  Shot damage (~20 cap). The APL keeps Rapid Fire on cooldown partly to hold
  Bulletstorm.
- **Deathblow** (Dark Ranger) — the proc that makes Black Arrow a frequent
  button instead of an execute-only one; queue Black Arrow off Aimed Shot to
  chain another proc.
- **Lunar Storm** (Sentinel) auto-fires on Mark consumption — no aiming needed.

## Choice-node leans

- **Calling the Shots vs Unerring Vision** — Calling the Shots (CD reduction) is
  the general default; Unerring Vision is a Trueshot-window crit lean.
- **Trick Shots vs Aspect of the Hydra** — Trick Shots for real AoE / M+; Hydra
  for sustained 2-target cleave without setup.
- **Kodo vs Devilsaur Tranquilizer**, **Tar Trap vs Scare Beast**, hero-tree
  survivability choice nodes (Sentinel **Conditioning/Scout's Vigil**, Dark
  Ranger **Dark Chains/Shadow Dagger**) are content/comfort picks — see the full
  node list in `talents.md`.

## Pet

MM runs **Lone Wolf** (no pet) by default; take **Unbreakable Bond** only if a
build wants the pet out (the simc precombat summons a pet *only* when that talent
is present). Pet utility that still matters when a pet is out: **Intimidation**
(stun), **Roar of Sacrifice** (external DR).

## TODO

- [x] Hero-tree choice — Sentinel default, Dark Ranger for pure ST (2026-07-11)
- [x] Backbone talents + key interactions — simc string + method/maxroll/murlok
- [ ] Store per-content import strings (raid ST / M+ / defensive) from Icy Veins
      + method talents pages; verify hero tree on import
- [ ] Stat priority + gearing/enchants/gems/consumables (own file, like the
      Affliction set) — not yet distilled for MM

---
title: Frost Death Knight — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Frost.simc  # tier 1 APL, midnight branch, fetched 2026-07-11
  - https://www.method.gg/guides/frost-death-knight/playstyle-and-rotation  # tier 3, upd. 2026-06-16
  - https://www.icy-veins.com/wow/frost-death-knight-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: high
---

# Frost Death Knight — Rotation (Midnight S1)

Distilled from the SimulationCraft default APL (Tier 1) for the MID1 profile,
corroborated with method.gg and Icy Veins (Tier 3). The simc default is the
**Deathbringer + Breath of Sindragosa** raid build (its talent string matches
method's "Raid Breath of Sindragosa" string exactly); the APL branches internally
on `hero_tree.deathbringer` vs `hero_tree.rider_of_the_apocalypse`,
`talent.breath_of_sindragosa` vs `talent.obliteration`, and enemy count
(1 / 3+). Frost is a **proc-priority** spec: everything below is really "spend
Killing Machine, spend Rime, don't overcap runes or Runic Power, and pool for the
next Pillar of Frost window."

## Core loop (what the priorities are really doing)

- **Killing Machine** → dump into **Obliterate** (ST) / **Frostscythe** (AoE).
  Bank to 2 stacks is fine; 2 stacks jumps the queue.
- **Rime** → free empowered **Howling Blast**.
- **Runic Power** → **Frost Strike** (ST) / **Glacial Advance** (AoE) so you
  never overcap; but **pool** RP when Breath is about to come up.
- **Runes** → never sit capped; but **pool** 3+ runes going into a Pillar of
  Frost / Obliteration or Reaper's Mark window.

## Pre-combat

- Runeforge weapons (Razorice + Fallen Crusader), summon ghoul / **Raise Dead**,
  `snapshot_stats`.

## Cooldown rules (from `actions.cooldowns`)

- **Pillar of Frost** is the anchor — send it when "sending CDs" (single-target,
  or adds will stay ≥ its window). Everything else lines up to it.
- **Reaper's Mark (Deathbringer)** just *before* Pillar (`cooldown.pillar_of_frost.remains<=gcd`),
  onto a target without the mark. With Breath, hold it unless Breath is >20s away
  or is about to be cast with RP ready.
- **Breath of Sindragosa** off-GCD once **Pillar is up**; pool to 60 RP first.
- **Frostwyrm's Fury**: with Apocalypse Now / Chosen of Frostbrood, fire it
  inside the Pillar/Breath window (not while Reaper's Mark or Exterminate is up).
  On pure builds, fire it while Pillar is up. Deathbringer holds the FWF
  **recall** until after Reaper's Mark explodes and Exterminate charges are spent.
- **Empower Rune Weapon**: to refill when rune-starved / low RP and not sitting
  on 2 Killing Machine, to avoid overcapping charges, and pre-Breath to guarantee
  fuel. It also sustains Bonegrinder/Killing Machine density.
- **Remorseless Winter**: on cooldown when sending CDs at 2+ targets, or with
  Gathering Storm; at 1 target only with Gathering Storm (or a maxed 10-stack
  about to fall off). Avoid clipping a Killing Machine consumption with it during
  an Obliteration window.
- **Trinkets / potion / racials**: sync to the Pillar of Frost (or Breath) window
  via `variable.cooldown_check` (Pillar up, or fight < 20s).
- **Anti-Magic Shell**: proactively when RP deficit > 40 (it generates RP) after
  the first-AMS timer, i.e. it doubles as a Runic Power builder, not only a soak.

## Single target (`actions.single_target`)

1. **Obliterate** if **2 Killing Machine** stacks, or (1 stack **and** rune ≥ 3)
2. **Howling Blast** on **Rime** — only if talented **Frostbound Will** (free
   Howling Blast worth prioritizing) 
3. **Frost Strike** at **5 Razorice** with **Shattering Blade** (and not pooling RP)
4. **Howling Blast** on **Rime**
5. **Frost Strike** if not Shattering-Blade build, not pooling RP, and RP
   deficit < 30 (dump before overcap)
6. **Obliterate** with a single **Killing Machine** stack (not rune-pooling)
7. **Frost Strike** (RP dump, when not pooling)
8. **Obliterate** filler (not rune-pooling; and *not* during the Obliteration
   Pillar window if that talent is up — see below)
9. **Howling Blast** without Killing Machine, *inside* an Obliteration Pillar
   window (the talent turns your builders into Killing Machine generators)

**Pooling gates.** `rp_pooling` holds Frost Strike when Breath is < ~4 GCDs away
and you're below the RP you need to open Breath. `rune_pooling` (Deathbringer)
holds Obliterate/Frostscythe when Reaper's Mark is < 6s away and you have < 3
runes — so the mark window opens with resources.

## AoE (3+ targets, `actions.aoe`)

Same skeleton, with **Frostscythe** replacing Obliterate and **Glacial Advance**
replacing Frost Strike, plus disease/Remorseless upkeep:

1. **Frostscythe** at **2 Killing Machine** (≥ frostscythe_priority = 3 targets)
2. **Frost Strike** on the 5-Razorice / Frostbane target (`debuff.razorice=5 &
   frostbane`) — burst the Razorice stack
3. **Frostscythe** at 1 Killing Machine with rune ≥ 3
4. **Obliterate** at 2 KM (or 1 KM + rune ≥ 3) — Rider prefers the
   Trollbane-slowed target
5. **Howling Blast** on **Rime** (or when Frost Fever isn't ticking — keep the
   disease up)
6. **Frost Strike** at 5 Razorice + Shattering Blade (< 5 targets, no Frostbane)
7. **Frostscythe** / **Obliterate** with Killing Machine (not rune-pooling)
8. **Howling Blast** on **Rime**
9. **Glacial Advance** (RP dump, when not pooling)
10. **Frostscythe** / **Obliterate** filler (skip during an Obliteration Pillar
    window), then **Howling Blast** to feed Killing Machine inside that window

Keep **Remorseless Winter** rolling and **Frost Fever** applied via Howling Blast.

## Hero-tree branches

- **Deathbringer** (raid/ST default): weave **Reaper's Mark** just before Pillar,
  detonate it, then spend the **Exterminate** charges (empowered, −1 rune
  Obliterate/Frostscythe) before recalling Frostwyrm's Fury. `rune_pooling`
  exists specifically to line resources up for the mark.
- **Rider of the Apocalypse** (M+/AoE lean): **Frostwyrm's Fury** summons the
  Horsemen *immediately* after Pillar so they're buffed by it. Obliterate
  target-swaps toward the **Trollbane-slowed** enemy; the tree scales with
  Mastery via Trollbane's Icy Fury.

## Engine branches (see `builds.md`)

- **Breath of Sindragosa** (simc default): pool 60 RP into each Pillar, open
  Breath off-GCD, then just keep feeding Killing Machine + Rime to extend it
  toward ~30s. Standard priority continues underneath the channel.
- **Obliteration**: during Pillar, **Frost Strike / Glacial Advance / Howling
  Blast all proc Killing Machine**, so the window becomes a predictable
  builder→Killing-Machine→Obliterate weave. Enter it with runes/RP ready and
  avoid dumping no-proc Obliterates in the ~5s before Pillar.

## TODO

- [x] Single-target priority — from simc MID1 APL, fetched 2026-07-11
- [x] AoE priority — from simc MID1 APL
- [x] Cooldown rules (Pillar anchor, Reaper's Mark/Breath/FWF sync) — simc + method
- [x] Hero-tree + engine branches — Deathbringer/Rider, Breath/Obliteration
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once S1 raid logs are pulled
- [ ] Re-distill if the simc midnight branch publishes a retuned 12.0.7 APL

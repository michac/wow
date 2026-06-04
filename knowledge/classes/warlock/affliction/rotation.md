---
title: Affliction Warlock — Rotation (Midnight Season 1)
patch: 12.0.5
fetched: 2026-06-03
sources:
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1 APL, commit 204b88d 2026-06-02, WoW 12.0.5.67823
confidence: high
---

# Affliction Warlock — Rotation (Soul Harvester, Midnight S1)

Distilled from the SimulationCraft default APL (tier 1). The APL branches
by hero tree (Soul Harvester / Hellcaller) and enemy count (1 / 2 / 3+).
Soul Harvester lists below — it's the only S1 build (see `builds.md`).

## Pre-combat

- Summon pet; pre-cast **Haunt** (ST) or **Seed of Corruption** (2+ targets).

## Cooldown rules

- Potion/racials **only while Darkglare is active**.
- Trinkets sync to Darkglare windows (don't bank past a lost use).
- **Dark Harvest before Darkglare** — the APL gates Darkglare on Dark
  Harvest already being on cooldown; the pair is the burst window.
- <8s left on the fight: dump shards into UA (or Seed with Patient
  Zero + Sow the Seeds), drain remaining Nightfall procs.

## Single target

1. **Haunt** on cooldown (Improved Haunt + apex make it a damage button)
2. **Agony** if <3s remaining
3. **Corruption** if <3s remaining
4. **Dark Harvest** when **<3 shards** and the channel fits inside both
   Agony and Corruption remaining (it refunds 3 shards — deplete first)
5. **Summon Darkglare** (once Dark Harvest is on CD)
6. At **2+ Nightfall stacks**: Malefic Grasp > Drain Soul > Shadow Bolt
7. **Unstable Affliction** with any shard or Shard Instability proc
   (primary spender; feeds succulent shards / Demonic Soul)
8. Filler: Malefic Grasp during Darkglare (if talented — Shadow Bolt
   *becomes* Malefic Grasp while Darkglare is active) → **Drain Soul**
   (if a Nightfall proc appears mid-channel, restart the channel so the
   new one consumes the proc — procs only apply to channels *started*
   while the buff is up) → Shadow Bolt

Nightfall (from Corruption ticks, stacks to 2): empowers the next
filler *started* while it's up — Shadow Bolt instant +75%, Drain
Soul/Malefic Grasp +75% and 50% faster. Two distinct rules: **start**
draining when at 2 stacks (about to overcap → spend now, jumps the
priority queue); **restart** an already-running filler channel when a
fresh proc lands mid-channel.

## Cleave (exactly 2)

As ST, plus: Seed to apply Corruption to both; **UA-cycle onto both
targets right before Dark Harvest comes off CD**; spend on Seed if
Patient Zero + Sow the Seeds.

## AoE (3+)

1. **Haunt** on cooldown
2. **Seed of Corruption** when Corruption is missing/refreshable — never
   double-sow (APL checks in-flight + previous cast)
3. **Dark Harvest** on cooldown
4. **Agony on up to 5 targets** (lowest-remains first; refresh <5s)
5. **Darkglare**
6. Shard spender: **Seed with Sow the Seeds** (or >9 targets without
   Darkglare up); otherwise UA
7. Keep Agonies above 50% duration; Malefic Grasp to carry Darkglare's
   last GCD
8. Nocturnal Yield: on 2+ targets, dump Seed when Nightfall stacks
   are capped or about to overflow
9. Filler as ST

## Hellcaller

Lists exist in the APL (`HC_st/cleave/aoe` — Wither instead of
Corruption, Malevolence as the 1-min CD) but the tree sees 0/50 usage
in top M+ (see `builds.md`); not distilled here.

## TODO

- [x] Single-target priority (opener + sustain) — from simc APL 2026-06-03
- [x] Multi-dot / M+ priority — from simc APL 2026-06-03
- [x] Hero talent build(s) used in S1 — Soul Harvester (see `builds.md`)
- [x] Cooldown usage rules — Dark Harvest→Darkglare pairing, trinket sync
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings`
      → `casts`) per the original sourcing plan
- [ ] Re-distill on 12.0.7 (PTR APL may change)

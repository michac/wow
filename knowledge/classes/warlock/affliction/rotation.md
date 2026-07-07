---
title: Affliction Warlock — Rotation (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1 APL, commit 204b88d 2026-06-02, WoW 12.0.5.67823
  - https://news.blizzard.com/en-us/article/24287397/hotfixes-june-30-2026  # tier 1, 6/30 hotfix — Seed of Corruption/Nightfall detonation + PvP-only +3%
  - https://www.wowhead.com/news/affliction-warlock-restoration-druid-and-frost-mage-issues-resolved-midnight-381441  # tier 4, 12.0.7 hotfix mechanic fixes
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 rotation corroboration
confidence: high
---

# Affliction Warlock — Rotation (Soul Harvester, Midnight S1)

Distilled from the SimulationCraft default APL (tier 1). The APL branches
by hero tree (Soul Harvester / Hellcaller) and enemy count (1 / 2 / 3+).
Soul Harvester lists below — it's the only S1 build (see `builds.md`).

> **12.0.7 "Revelations" (live 2026-06-16) — mechanic hotfixes, no number
> retuning for the core spec.** Three resource bugs were corrected, all of
> which were leaking value out of the shard economy below:
> - **Shard Instability** is no longer fully consumed by a single Unstable
>   Affliction cast — only one stack per UA, as intended. Before the fix a
>   UA could eat *all* stacks, so banking Shard Instability for free UAs
>   now actually pays off (see the UA spender rule below).
> - **Fatal Echoes**-applied Unstable Affliction no longer wrongly consumes
>   a Soul Shard or a Shard Instability stack. The free echoed UAs are now
>   genuinely free — treat them as a damage bonus, not a shard drain.
> - **Soul Swap** no longer carries Unstable Affliction stacks across an
>   instance entry/exit (zoning into a delve/dungeon/raid). No rotational
>   action needed; just don't expect pre-pulled UA stacks to survive a load
>   screen anymore.
>
> **6/30 hotfix (Tier-1):** casting **Seed of Corruption on an already-seeded
> target to consume a Nightfall proc** causes the **preexisting Seed to
> detonate**. ⚠ **Scope unconfirmed for PvE:** this line sits under the **Player
> versus Player** section of the 6/30 notes (next to Affliction's explicit **+3%
> damage in PvP combat only**) and, unlike the damage line, carries no "in PvP
> combat" suffix — so whether the detonation applies in PvE is **unresolved;
> verify in-game** before relying on it. If it does apply, it makes the
> Nightfall→Seed dump safe on an already-seeded target (see AoE Nocturnal Yield
> rule). No PvE core-number retune this pass.
>
> The priority ordering itself is unchanged from 12.0.5 (corroborated vs the
> 12.0.7 Icy Veins rotation guide). Re-sim against an updated 12.0.7 APL when
> the simc midnight branch publishes one (see TODO).

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
   (primary spender; feeds succulent shards / Demonic Soul). As of 12.0.7
   each UA consumes only **one** Shard Instability stack, so you can chain
   UAs through a multi-stack Shard Instability window without wasting it.
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
   are capped or about to overflow, **preferring a target without a Seed**
   so the proc isn't wasted. (A 6/30 hotfix may make a Nightfall-consuming
   Seed **detonate** an existing Seed instead — but that line is in the PvP
   section of the notes, so treat its PvE applicability as unconfirmed and
   verify in-game before relying on it.)
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
- [~] Re-distill on 12.0.7 — 12.0.7 went live 2026-06-16; the three hotfix
      mechanic fixes (Shard Instability / Fatal Echoes / Soul Swap) plus the
      6/30 Seed-of-Corruption/Nightfall detonation change are captured above,
      and priority ordering is unchanged (re-verified 2026-07-07 vs the Tier-1
      6/30 hotfix log — Affliction got no PvE number retune, only PvP-only
      +3%). Still pending: a refreshed simc midnight 12.0.7 APL for a full
      numeric re-distill (none published as of 2026-07-07).

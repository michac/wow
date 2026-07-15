---
title: Discipline Priest — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/discipline-priest/playstyle-and-rotation  # tier 3, 2026-07-11 (Midnight 12.0.7)
  - https://www.icy-veins.com/wow/discipline-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11 (12.0.7)
  - https://www.wowhead.com/guide/classes/priest/discipline/rotation-cooldowns-pve-healer  # tier 4, 2026-07-11
confidence: medium
---

# Discipline Priest — Rotation (Midnight S1)

> **No Tier-1 SimulationCraft APL exists for this spec.** SimulationCraft ships
> only `profiles/MID1/MID1_Priest_Shadow.simc` — Discipline (a healer) has no
> default action list. This priority is distilled from Tier-3 guides (method.gg
> playstyle page + Icy Veins 12.0.7), which agree with each other; confidence is
> **medium** and the "damage priority" is a soft ordering, not a sim-optimized
> APL. Re-verify tuning-sensitive steps in-game.

Discipline heals by **dealing damage through Atonement**. Every pull is a rhythm
of two phases: **(1) blanket the group in Atonement** (ramp), then **(2) unload
damage** while that blanket is up so the mirrored healing lands. Damage abilities
*are* your healing rotation — you press them constantly, not just when the group
is hurt. Direct heals fill gaps; the big healing comes from a well-timed ramp
into a damage window.

## Pre-combat

- **Power Word: Fortitude** up; summon **Shadowfiend/Mindbender** is a combat CD.
- Pre-apply **Shadow Word: Pain** (or **Purge the Wicked**) on the pull target.
- If damage is coming immediately, start a **mini-ramp** ~4-5s before the hit
  (Power Word: Shield / Void Shield + a Power Word: Radiance) so Atonement is
  live when you begin dealing damage.

## Cooldown rules

- **Evangelism** is the raid ramp engine — it drops **5 Atonements** and makes
  the **next 2 Power Word: Radiance instant**. Fire it right before a known
  heavy-damage moment, chain the two instant Radiances, then dump damage.
- **Ultimate Penitence** (4-min) is used **offensively** — cast it *on enemies*
  during a ramp for a large Atonement-healing burst (pre-load 2 Radiances so its
  channel's instants are free). Do **not** target it on allies.
- **Power Infusion** (2-min) syncs to your biggest damage/ramp window.
- **Shadowfiend/Mindbender** on cooldown inside damage windows (mana + Atonement
  damage; **Inescapable Torment** ties it to Shadow Word: Death).
- **Pain Suppression / Power Word: Barrier** are reactive raid/tank saves, not
  part of the damage loop.

## The big ramp (raid, Evangelism version)

Method's canonical sequence — cast just before the damage event:

1. Refresh **Shadow Word: Pain / Purge the Wicked** if about to fall off
2. **Penance** (defensive, on ally)
3. **Void Shield** (or **Power Word: Shield + Plea**)
4. **Flash Heal**
5. **Evangelism** (→ 5 Atonements, next 2 Radiances instant)
6. **Power Word: Radiance ×2** (instant)
7. **Shadow Word: Death** (line up trinket/potion here)
8. **Penance** (now on enemy — damage)
9. **Mind Blast**
10. **Penance** / continue damage filler

The **Ultimate Penitence ramp** is the same setup but casts **2× Radiance →
Ultimate Penitence** (on enemies) so the channel's free instants land into a
full Atonement blanket.

## Single-target damage priority (inside a window)

**Oracle:**

1. Maintain **Shadow Word: Pain / Purge the Wicked**
2. **Shadow Word: Death** (on cooldown / execute)
3. **Mind Blast**
4. **Penance** (on enemy)
5. **Holy Nova** (if talented / multiple targets)
6. **Smite** (filler)

**Voidweaver:**

1. **Shadow Word: Pain / Purge the Wicked** (maintain)
2. **Shadow Word: Death** (execute range)
3. **Mind Blast** (opens/refreshes **Entropic Rift**)
4. **Penance**
5. **Void Blast** (while Entropic Rift is up — replaces Smite)
6. **Shadow Word: Death** (outside execute, for Expiation / pet)

## AoE / multi-target

- **Dungeons:** a single **Power Word: Radiance** blankets the whole party;
  then run the normal damage priority — passive Atonement handles the pack.
- Keep **Shadow Word: Pain / Purge the Wicked** rolling; **Penance spreads it**
  (Purge the Wicked) across the pack.
- **Holy Nova** and pet damage (**Shadowfiend/Mindbender/Voidwraith**) scale the
  AoE; **Voidweaver's Entropic Rift** is a large chunk of pack damage.
- Reserve one **Radiance** charge for the next incoming hit rather than dumping
  both — the mini-ramp (Shield/Void Shield + Radiance + a couple manual
  Atonements) is your between-ramp maintenance.

## Hero-tree branches

- **Oracle** — default; smoother throughput outside cooldowns and the
  **Premonition** utility toolkit. Guidance: **always use Penance defensively**
  when not actively pushing damage; leans **Master the Darkness → Void Shield**
  and Shadow Mend procs in M+.
- **Voidweaver** — **Entropic Rift** (opened by **Mind Blast**) gives very
  frequent mini-ramp windows and much higher group DPS; **Void Blast** is the
  in-rift filler and **Void Torrent** a channel CD. Strong M+ pick and a bigger
  raid damage contributor than Oracle.

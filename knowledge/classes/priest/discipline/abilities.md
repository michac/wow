---
title: Discipline Priest — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/priest/discipline/ability-inventory.tsv  # tier 1, generated from DB2 @ build 12.0.7.67808 — name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - https://www.method.gg/guides/discipline-priest/playstyle-and-rotation  # tier 3, 2026-07-11 (Midnight 12.0.7)
  - https://www.icy-veins.com/wow/discipline-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11 (12.0.7)
  - https://www.wowhead.com/guide/classes/priest/discipline/rotation-cooldowns-pve-healer  # tier 4, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1, game-data name reconciliation, build 12.0.7.67808
  - knowledge/classes/priest/discipline/talents.md  # tier 1, Blizzard talent-tree API 12.0.7.67808
confidence: medium
---

# Discipline Priest — Ability Inventory (Midnight S1)

## Overview

Discipline is a **healer** spec whose throughput comes from **damage, not direct
heals**: **Atonement** (passive, spell 81749) is applied to allies by a handful of
spells, and while it is up on them a percentage of the Priest's **damage done**
is mirrored back as healing to everyone carrying the buff. The whole spec is a
loop of **stack Atonement on the group → deal as much damage as possible inside
that window** ("ramping"). Direct heals (Flash Heal, Penance-on-ally) exist but
are secondary; big single-hit healing usually comes from *spending* a pre-built
Atonement blanket into damage.

- **Resource:** Mana. No builder/spender combo resource — everything is
  mana-gated with per-ability cooldowns/charges.
- **Hero trees (Midnight):** **Oracle** (default, more consistent throughput; its live
  subtree carries **Prophet's Insight**, **Prophet's Will**, **Piety** and **Twinsight** —
  the old `Premonition` button is gone, see the reconciliation notes — and the "always use
  Penance defensively" habit comes with it) and **Voidweaver**
  (`Entropic Rift` / `Void Blast` / `Void Torrent` — frequent "mini-ramp" windows
  and much higher group damage). See `builds.md` / `rotation.md`.
- **Notable gap:** Discipline has **no baseline interrupt** (no kick/silence) —
  unusual among healers; plan CC/utility around that.

`Function` below is the ability's game role, not any bind assignment.

## Inventory

**`ability-inventory.tsv` in this directory is the Tier-1 floor** — canonical name, spellID,
origin and baseline cooldown are regenerated there from DB2 and are not duplicated here.
This file is the prose layer: the Atonement loop and what each button contributes to it.

A cooldown written **`30s [T1]`** was read off that tsv (DB2 @ build 12.0.7.67808); `~`
values are guide-derived. `@verify-ingame` marks what Tier 1 could not settle.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.0.7.67808).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Atonement | Passive (core) | — | — | Buff placed on allies by shields/heals; a share of your **damage done** heals every Atonement'd ally. The entire spec builds around it. |
| Penance | Rotational-spender / Defensive | Mana | Channel ~2s / ~9s CD (reduced by Castigation, Harsh Discipline) | Channels 3 bolts. **On an enemy = damage** (main damage button); **on an ally = heal** ("defensive Penance"). Power of the Dark Side empowers the next cast; Weal and Woe rewards weaving shields between casts. |
| Smite | Rotational-builder (filler) | Mana | ~1.5s cast | Baseline Holy damage filler — lowest-priority damage button, heals via Atonement. Replaced by **Void Blast** while Entropic Rift is open (Voidweaver). |
| Mind Blast | Rotational-builder | Mana | ~1.5s cast / short CD (hasted) | Priority damage. **Voidweaver:** opens/refreshes **Entropic Rift** and enables **Void Blast**. |
| Shadow Word: Pain | Rotational (DoT) | Mana | Instant | Class-baseline, not a talent [T1]. Maintained Shadow DoT (the anchor DoT). **Purge the Wicked** talent upgrades it and lets **Penance spread it** to nearby enemies. |
| Purge the Wicked | Rotational (DoT, talented) | Mana | Instant | Talent replacement for Shadow Word: Pain — stronger DoT that Penance propagates. @verify-ingame |
| Shadow Word: Death | Rotational-spender / execute | Mana | Instant / 10s CD (2 charges w/ talent) | Execute-window nuke (big sub-20%). Feeds pet resets via **Inescapable Torment**; used outside execute for **Expiation**. |
| Void Blast | Rotational-spender (Voidweaver) | Mana | Instant | Replaces Smite as filler **while Entropic Rift is active**; Voidweaver's damage core. |
| Void Torrent | Major cooldown (Voidweaver channel) | Mana | Channel ~3s / 30s [T1] | Heavy Atonement-damage channel that drives an Entropic Rift window. |
| Entropic Rift | Passive (Voidweaver) | — | — | Mind Blast opens a rift doing AoE Void damage over its duration — the Voidweaver "mini-ramp" engine. |
| Holy Nova | Rotational (AoE) | Mana | Instant | PBAoE damage (+ Atonement application when talented). Situational AoE / pack-tagging. |
| Power Word: Shield | Rotational (Atonement applier) | Mana | Instant | Damage absorb that **applies Atonement**. Buffed ~25% in 12.0.5. Upgraded into **Void Shield** by Master the Darkness. |
| Void Shield | Rotational (upgraded Atonement applier) | Mana | Instant | **Master the Darkness** upgrade of Power Word: Shield (procced by Penance): shields **up to 3 allies** and applies Atonement to each. Buffed ~25% in 12.0.5. @verify-ingame |
| Power Word: Radiance | Rotational (AoE Atonement applier) | Mana | ~2s cast / 2 charges, ~20s recharge | Applies Atonement to **5 allies** — the mass-ramp button. **Evangelism** makes the next two casts **instant**. |
| Flash Heal | Rotational (Atonement applier / spot heal) | Mana | ~1.5s cast | Fast direct heal that also applies Atonement; used in ramps and for spot healing. Surge of Light can make it instant. |
| Plea | Rotational (cheap Atonement applier) | Mana (low) | Instant | Low-cost single-target Atonement applier / small heal — used to top up Atonement blankets during ramps. @verify-ingame |
| Shadow Mend | Reactive heal | Mana | Cast (instant on proc) | Emergency direct heal; in the Oracle M+ build it comes up as a **proc** for burst spot-healing. @verify-ingame |
| Evangelism | Major cooldown (ramp) | Mana | Instant / ~90s CD | Applies **5 Atonements** at once and makes the **next 2 Power Word: Radiance instant** — the primary raid ramp opener (no longer extends Atonement duration in Midnight; it seeds fresh ones). |
| Ultimate Penitence | Major cooldown | Mana | Channel / **4 min CD** | Long-CD flying Penance barrage; **used offensively** (cast on enemies) for a large Atonement-healing burst. Choice node vs Power Word: Barrier. |
| Power Infusion | Major cooldown | — | Instant / 2 min CD | +25% haste for 20s (self, or gifted to an ally; Twins of the Sun grants both). |
| Shadowfiend | Major cooldown (pet) | — | Instant / ~3 min CD | Summons a fiend that deals damage and returns mana. **A talent, not baseline [T1]** — you take it (or swap it for Mindbender). **Inescapable Torment** synergy. |
| Mindbender | Major cooldown (pet) | — | Instant / ~1 min CD | Choice-node replacement for Shadowfiend — shorter CD, more frequent pet damage/mana. |
| Master the Darkness | Rotational apex active | — | — / — | Apex spec talent (min 3 pts for Atonement-healing increases); empowers Atonement and upgrades Power Word: Shield → **Void Shield**. @verify-ingame |
| Power Word: Barrier | Major defensive (raid) | Mana | Instant / 3 min CD | Ground zone granting **−25% damage taken** to allies inside. Choice node vs Ultimate Penitence. |
| Pain Suppression | Defensive (external) | Mana | Instant / ~3 min CD | Strong single-target damage reduction on an ally (~40%) for 8s. @verify-ingame |
| Desperate Prayer | Defensive (self) | — | Instant / ~90s CD | +25% max health and a self-heal for 10s. |
| Fade | Defensive / Utility | — | Instant / 30s CD | Drops threat; with **Improved Fade / Phantasm** adds personal damage reduction / snare break. |
| Psychic Scream | CC (AoE fear) | Mana | Instant / **40s** `[T1]` | Fears up to 5 nearby enemies for a few seconds. |
| Shackle Horror | CC | Mana | ~1.5s cast | Incapacitates an Undead/Horror target (Midnight name for the old Shackle Undead). @verify-ingame |
| Mind Control | CC | Mana | Cast (channel) | Takes control of an enemy; Dominate Mind is the talent variant. |
| Mind Soothe | Utility | Mana | Instant | Reduces an enemy's aggro range (pull management). |
| Purify | Dispel | Mana | Instant / 8s CD | Removes Magic + Disease from an ally. |
| Dispel Magic | Dispel (offensive) | Mana | Instant | Removes a beneficial Magic effect from an enemy. |
| Mass Dispel | Dispel (AoE) | Mana | Cast / **120s** `[T1]` | AoE Magic dispel; can strip certain immunities. |
| Leap of Faith | Utility (save) | — | Instant / ~90s CD | Yanks a targeted ally to your location. |
| Angelic Feather | Movement | — | Instant / 3 charges | Places a feather; allies passing over it gain a movement-speed burst. |
| Levitate | Movement / Utility | Mana | Cast | Slow-fall / water-walk-style movement utility. |
| Power Word: Fortitude | Utility (raid buff) | Mana | Cast | Raid-wide Stamina buff. |
| Resurrection | Utility | Mana | ~10s cast | Out-of-combat single-target resurrection. |

## Reconciliation notes — Tier 1 @ 12.0.7.67808

- **Premonition is not acquirable at 12.0.7** and the row is deleted. Every spell of that
  name is TWW-era and attaches to nothing; the Oracle subtree (**20**) *is* live on the
  Priest tree (**795**) but now carries `Prophet's Insight`, `Prophet's Will`, `Piety` and
  `Twinsight` — no Premonition node and no `Premonition of *`. Oracle is still the default
  hero tree; the button it used to hand you is gone.
- **Shadow Word: Pain is class-baseline** (not a talent) and **Shadowfiend is a talent**
  (not baseline) — the file had these the wrong way round.
- **Void Torrent is 30s**, not the ~30–45s range carried from the guides.
- **Void Shield keeps its `@verify-ingame` marker on purpose.** The talent that grants it,
  **Master the Darkness**, is live on tree 795 and the button has Midnight-range spell IDs,
  but it is a Power Word: Shield *override* with no acquisition row — DB2 cannot settle its
  numbers, so this is a tool gap, not a stale claim.

> No simc APL exists for Discipline (SimulationCraft ships only `MID1_Priest_Shadow`
> profiles — healers have no default APL), so cast/CD/resource figures above are
> from Tier-3 guides + game-data names and are approximate; tuning-sensitive
> numbers carry `@verify-ingame`.

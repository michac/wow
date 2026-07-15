---
title: Discipline Priest — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
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
- **Hero trees (Midnight):** **Oracle** (default, more consistent throughput +
  the `Premonition` toolkit; "always use Penance defensively") and **Voidweaver**
  (`Entropic Rift` / `Void Blast` / `Void Torrent` — frequent "mini-ramp" windows
  and much higher group damage). See `builds.md` / `rotation.md`.
- **Notable gap:** Discipline has **no baseline interrupt** (no kick/silence) —
  unusual among healers; plan CC/utility around that.

`Function` below is the ability's game role, not any bind assignment.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Atonement | Passive (core) | — | — | Buff placed on allies by shields/heals; a share of your **damage done** heals every Atonement'd ally. The entire spec builds around it. |
| Penance | Rotational-spender / Defensive | Mana | Channel ~2s / ~9s CD (reduced by Castigation, Harsh Discipline) | Channels 3 bolts. **On an enemy = damage** (main damage button); **on an ally = heal** ("defensive Penance"). Power of the Dark Side empowers the next cast; Weal and Woe rewards weaving shields between casts. |
| Smite | Rotational-builder (filler) | Mana | ~1.5s cast | Baseline Holy damage filler — lowest-priority damage button, heals via Atonement. Replaced by **Void Blast** while Entropic Rift is open (Voidweaver). |
| Mind Blast | Rotational-builder | Mana | ~1.5s cast / short CD (hasted) | Priority damage. **Voidweaver:** opens/refreshes **Entropic Rift** and enables **Void Blast**. |
| Shadow Word: Pain | Rotational (DoT) | Mana | Instant | Maintained Shadow DoT (the anchor DoT). **Purge the Wicked** talent upgrades it and lets **Penance spread it** to nearby enemies. |
| Purge the Wicked | Rotational (DoT, talented) | Mana | Instant | Talent replacement for Shadow Word: Pain — stronger DoT that Penance propagates. @verify-ingame |
| Shadow Word: Death | Rotational-spender / execute | Mana | Instant / 10s CD (2 charges w/ talent) | Execute-window nuke (big sub-20%). Feeds pet resets via **Inescapable Torment**; used outside execute for **Expiation**. |
| Void Blast | Rotational-spender (Voidweaver) | Mana | Instant | Replaces Smite as filler **while Entropic Rift is active**; Voidweaver's damage core. |
| Void Torrent | Major cooldown (Voidweaver channel) | Mana | Channel ~3s / ~30-45s CD | Heavy Atonement-damage channel that drives an Entropic Rift window. @verify-ingame |
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
| Shadowfiend | Major cooldown (pet) | — | Instant / ~3 min CD | Summons a fiend that deals damage and returns mana. Talent baseline; **Inescapable Torment** synergy. |
| Mindbender | Major cooldown (pet) | — | Instant / ~1 min CD | Choice-node replacement for Shadowfiend — shorter CD, more frequent pet damage/mana. |
| Master the Darkness | Rotational apex active | — | — / — | Apex spec talent (min 3 pts for Atonement-healing increases); empowers Atonement and upgrades Power Word: Shield → **Void Shield**. @verify-ingame |
| Premonition | Cooldown / utility (Oracle) | — | Instant / ~60s CD | Oracle hero active granting a situational **Premonition of Insight/Solace/Piety/Clairvoyance** effect (throughput or defensive). @verify-ingame |
| Power Word: Barrier | Major defensive (raid) | Mana | Instant / 3 min CD | Ground zone granting **−25% damage taken** to allies inside. Choice node vs Ultimate Penitence. |
| Pain Suppression | Defensive (external) | Mana | Instant / ~3 min CD | Strong single-target damage reduction on an ally (~40%) for 8s. @verify-ingame |
| Desperate Prayer | Defensive (self) | — | Instant / ~90s CD | +25% max health and a self-heal for 10s. |
| Fade | Defensive / Utility | — | Instant / 30s CD | Drops threat; with **Improved Fade / Phantasm** adds personal damage reduction / snare break. |
| Psychic Scream | CC (AoE fear) | Mana | Instant / 30s CD | Fears up to 5 nearby enemies for a few seconds. |
| Shackle Horror | CC | Mana | ~1.5s cast | Incapacitates an Undead/Horror target (Midnight name for the old Shackle Undead). @verify-ingame |
| Mind Control | CC | Mana | Cast (channel) | Takes control of an enemy; Dominate Mind is the talent variant. |
| Mind Soothe | Utility | Mana | Instant | Reduces an enemy's aggro range (pull management). |
| Purify | Dispel | Mana | Instant / 8s CD | Removes Magic + Disease from an ally. |
| Dispel Magic | Dispel (offensive) | Mana | Instant | Removes a beneficial Magic effect from an enemy. |
| Mass Dispel | Dispel (AoE) | Mana | Cast | AoE Magic dispel; can strip certain immunities. |
| Leap of Faith | Utility (save) | — | Instant / ~90s CD | Yanks a targeted ally to your location. |
| Angelic Feather | Movement | — | Instant / 3 charges | Places a feather; allies passing over it gain a movement-speed burst. |
| Levitate | Movement / Utility | Mana | Cast | Slow-fall / water-walk-style movement utility. |
| Power Word: Fortitude | Utility (raid buff) | Mana | Cast | Raid-wide Stamina buff. |
| Resurrection | Utility | Mana | ~10s cast | Out-of-combat single-target resurrection. |

> No simc APL exists for Discipline (SimulationCraft ships only `MID1_Priest_Shadow`
> profiles — healers have no default APL), so cast/CD/resource figures above are
> from Tier-3 guides + game-data names and are approximate; tuning-sensitive
> numbers carry `@verify-ingame`.

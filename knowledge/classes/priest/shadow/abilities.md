---
title: Shadow Priest — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Priest_Shadow.simc  # tier 1 APL + ability list, 2026-07-11
  - raw/wago/SpellName.csv (wago.tools DB2 SpellName @ 12.0.7)  # tier 1, name reconciliation, 2026-07-11
  - https://www.method.gg/guides/shadow-priest  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/shadow-priest-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Shadow Priest — abilities (Midnight Season 1)

## Overview

Shadow is Priest's ranged-DPS spec. It is a **DoT-based builder/spender**: you
keep **Shadow Word: Pain** and **Vampiric Touch** rolling on every target,
build the **Insanity** resource with short-cooldown generators (**Mind Blast**,
**Void Volley**, **Mind Flay**), and spend it on **Shadow Word: Madness** — the
primary spender that must stay ticking on the priority target. Its Mastery,
**Shadow Weaving**, amplifies damage; **Shadowform** is the passive DPS stance
you sit in. **Psychic Link** splits much of your single-target damage onto all
DoTed enemies, so multi-dot upkeep *is* the AoE rotation.

**Hero trees (Midnight):**
- **Voidweaver** — builds around **Void Torrent** opening an **Entropic Rift**,
  spending it with **Void Blast**; the simc default profile. Void-damage burst.
- **Archon** — builds around **Halo** and the **Mind Flay: Insanity** empowered
  filler; more AoE-cleave / sustained flavour.

**Resource:** Insanity (0–100). **Voidform** is now a ~2-min burst cooldown
(reworked from the old Void Eruption/stacking-Voidform), synced with **Power
Infusion**, rather than a sustained stack meter.

> **Midnight renames/reworks to know (Tier-1 game-data + method.gg):**
> - **Shadow Word: Madness** (spell 335467) is the renamed **Devouring Plague**
>   — same builder/spender spender role. @verify-ingame
> - **Void Volley** replaced **Void Bolt** as the recharging Insanity generator.
> - **Tentacle Slam** (spell 1227280) is the reworked **Shadow Crash** — the
>   AoE DoT-applicator / Vampiric Touch spreader, now with charges.
> - **Shackle Horror** (spell 9484) is the renamed **Shackle Undead** (Horror
>   creature-type CC for the Void theme).
> - **Shadowfiend / Mindbender / Voidwraith** are passive-summon procs in this
>   build (Depth of Shadows / Inescapable Torment), not hard-cast buttons.

## Inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Shadow Word: Pain | Rotational-DoT (builder upkeep) | — | Instant | Shadow DoT; keep on all targets. Feeds Psychic Link + Misery/Invoked Nightmare. |
| Vampiric Touch | Rotational-DoT (builder upkeep) | — | 1.5s cast | Primary Shadow DoT; also heals you. Keep on all targets; main multi-dot spread. |
| Shadow Word: Madness | Rotational-spender | −50 Insanity (approx) @verify-ingame | Instant | Renamed Devouring Plague. Spend Insanity to keep this ticking; refresh when <~1s left or Insanity deficit ≤35. |
| Mind Blast | Rotational-builder | +Insanity | Instant, ~8s / 2 charges @verify-ingame | Instant Insanity generator; dump charges (avoid capping) unless holding for Voidform. |
| Void Volley | Rotational-builder | +Insanity | Recharge CD (haste-scaled) @verify-ingame | Replaced Void Bolt; short-CD Insanity generator, high priority to avoid losing charges. |
| Mind Flay | Rotational-filler (channel) | +Insanity/tick | 1.5s channel | Filler builder when nothing else is up; channel, interruptible after 3 ticks. |
| Mind Flay: Insanity | Rotational-filler (empowered) | spends/uses Insanity | Instant | Archon proc after Halo (via Surge of Insanity); harder-hitting instant filler. |
| Tentacle Slam | Rotational-builder / AoE DoT-spread | — | Instant, ~10s / 2 charges @verify-ingame | Reworked Shadow Crash. Applies/refreshes Vampiric Touch to many targets (6–12), Void Apparitions/Maddening Tentacles value; charge-managed. |
| Shadow Word: Death | Rotational-execute | +Insanity | Instant, short CD | Execute (sub-20%, extended by Deathspeaker). Also a movement filler and a shield-popper with Devour Matter. Deals self-damage if target survives. |
| Void Torrent | Major cooldown / Rotational (Voidweaver) | +Insanity (channel) | 3s channel, ~15s CD @verify-ingame | Voidweaver keystone; channel that opens an Entropic Rift. Cast near full Mastery value. |
| Void Blast | Rotational-builder (Voidweaver) | +Insanity | Instant | Spends the Entropic Rift window; high-priority when SWM is up or the Rift is expiring. |
| Halo | Major cooldown / AoE (Archon) | — | ~2.5s cast, ~20s CD @verify-ingame | Archon keystone; expanding ring of damage, enables Mind Flay: Insanity procs. |
| Voidform | Major cooldown | — | Instant, ~2 min | Reworked burst window (was Void Eruption); sync with Power Infusion + trinkets/potion. |
| Power Infusion | Major cooldown (haste) | — | Instant, 2 min | +25% haste for 20s; self-cast or given to an ally. Sync with Voidform. |
| Shadowfiend / Mindbender / Voidwraith | Pet (proc summon) | — | Passive proc | Summoned by Depth of Shadows / talents; melee pet that funnels Insanity & enables Inescapable Torment SW:D. |
| Void Apparitions | Rotational (proc) | — | Instant (talent) | Talented Void-damage apparitions add-on to the Tentacle Slam / DoT package. |
| Holy Nova | Utility / off-heal | — | Instant | AoE heal+damage; in the APL only used to proc Twist of Fate healing (niche). |
| Dispersion | Defensive (major) | — | ~6s channel, ~90s CD @verify-ingame | −75% damage taken while channeled; also purges movement-impairing effects. Baseline in Midnight. |
| Desperate Prayer | Defensive (self-heal) | — | Instant, ~90s CD | Instant self-heal + short max-HP bump; use when SW:D self-damage or spike drops you below ~75%. |
| Vampiric Embrace | Defensive (group heal) | — | Instant, ~2 min | Your shadow damage heals you and nearby allies for a window. |
| Fade | Defensive / Utility | — | Instant, ~30s CD | Drops threat; with talents (Improved Fade / Phantasm) adds damage reduction & snare immunity. |
| Power Word: Shield | Defensive (absorb) | mana | Instant | Absorb shield on self/ally; Body and Soul can add a speed burst. |
| Flash Heal | Off-heal | mana | ~1.5s cast | Emergency heal; in the APL also pressed to proc a trinket (Nexus-King's Command). |
| Silence | Interrupt / CC | — | Instant, 30s CD (baseline) | Interrupts a cast and locks the school; short silence. Baseline in Midnight. |
| Psychic Scream | CC (AoE fear) | mana | Instant, ~30s CD | Fears nearby enemies; Petrifying Scream (talent) roots instead. |
| Shackle Horror | CC (single) | mana | ~1.5s cast | Incapacitates a Horror/Undead-type enemy (renamed Shackle Undead). |
| Mind Control / Dominate Mind | CC (control) | mana | ~1.8s cast | Takes control of an enemy (choice node). |
| Mind Soothe | Utility (pull control) | mana | Instant | Reduces an enemy's aggro range. |
| Dispel Magic | Dispel (offensive/defensive) | mana | Instant | Removes a magic effect from an ally or purges an enemy buff. |
| Purify Disease | Dispel | mana | Instant | Removes disease effects from an ally. |
| Mass Dispel | Dispel (AoE) | mana | ~1.5s cast, CD | Removes magic from multiple allies / enemies; can strip some immunities. |
| Leap of Faith | Utility (movement/save) | mana | Instant, CD | "Life Grip" — pulls a targeted ally to you. |
| Angelic Feather | Movement | — | Instant, charges | Places a feather that grants a large speed burst when walked over. |
| Levitate | Movement / Utility | mana | Instant | Slow fall / walk-on-water travel utility. |
| Power Word: Fortitude | Utility (raid buff) | mana | ~1.5s cast | Raid-wide +Stamina buff. |
| Resurrection | Utility (res) | mana | Out of combat | Revives a dead ally. |
| Shadowform | Passive (stance) | — | — | The DPS stance; kept up at all times (precombat cast if down). |

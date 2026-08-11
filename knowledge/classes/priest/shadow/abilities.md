---
title: Shadow Priest — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/priest/shadow/ability-inventory.tsv  # tier 1, generated from DB2 @ build 12.0.7.67808 — name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Priest_Shadow.simc  # tier 1 APL + ability list, 2026-07-11
  - raw/wago/SpellName.csv (wago.tools DB2 SpellName @ 12.0.7)  # tier 1, name reconciliation, 2026-07-11
  - https://www.method.gg/guides/shadow-priest  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/shadow-priest-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


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

**`ability-inventory.tsv` in this directory is the Tier-1 floor** — canonical name, spellID,
origin and baseline cooldown are regenerated there from DB2 and are not duplicated here.
This file is the prose layer: the DoT/Insanity loop and what each button is for.

A cooldown written **`30s [T1]`** was read off that tsv (DB2 @ build 12.0.7.67808) and is
the baseline before talents and Haste; `~` values are guide-derived. `@verify-ingame` marks
what Tier 1 could not settle — Insanity costs, charge counts and recharge rates, and the
Midnight override buttons that carry no acquisition row at all.

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
| Shadow Word: Pain | Rotational-DoT (builder upkeep) | — | Instant | Shadow DoT; keep on all targets. Feeds Psychic Link + Misery/Invoked Nightmare. |
| Vampiric Touch | Rotational-DoT (builder upkeep) | — | 1.5s cast | Primary Shadow DoT; also heals you. Keep on all targets; main multi-dot spread. |
| Shadow Word: Madness | Rotational-spender | −50 Insanity (approx) @verify-ingame | Instant | Renamed Devouring Plague. Spend Insanity to keep this ticking; refresh when <~1s left or Insanity deficit ≤35. |
| Mind Blast | Rotational-builder | +Insanity | Instant, ~8s / 2 charges @verify-ingame | Instant Insanity generator; dump charges (avoid capping) unless holding for Voidform. |
| Void Volley | Rotational-builder | +Insanity | Recharge CD (haste-scaled) @verify-ingame | Replaced Void Bolt; short-CD Insanity generator, high priority to avoid losing charges. |
| Mind Flay | Rotational-filler (channel) | +Insanity/tick | 1.5s channel | Filler builder when nothing else is up; channel, interruptible after 3 ticks. |
| Mind Flay: Insanity | Rotational-filler (empowered) | spends/uses Insanity | Instant | Archon proc after Halo (via Surge of Insanity); harder-hitting instant filler. |
| Tentacle Slam | Rotational-builder / AoE DoT-spread | — | Instant, ~10s / 2 charges @verify-ingame | Reworked Shadow Crash. Applies/refreshes Vampiric Touch to many targets (6–12), Void Apparitions/Maddening Tentacles value; charge-managed. |
| Shadow Word: Death | Rotational-execute | +Insanity | Instant, short CD | Execute (sub-20%, extended by Deathspeaker). Also a movement filler and a shield-popper with Devour Matter. Deals self-damage if target survives. |
| Void Torrent | Major cooldown / Rotational (Voidweaver) | +Insanity (channel) | 3s channel, 30s [T1] | Voidweaver keystone; channel that opens an Entropic Rift. Cast near full Mastery value. |
| Void Blast | Rotational-builder (Voidweaver) | +Insanity | Instant | Spends the Entropic Rift window; high-priority when SWM is up or the Rift is expiring. |
| Halo | Major cooldown / AoE (Archon) | — | ~2.5s cast, 60s [T1] | Archon keystone; expanding ring of damage, enables Mind Flay: Insanity procs. |
| Voidform | Major cooldown | — | Instant, ~2 min | Reworked burst window (was Void Eruption); sync with Power Infusion + trinkets/potion. |
| Power Infusion | Major cooldown (haste) | — | Instant, 2 min | +25% haste for 20s; self-cast or given to an ally. Sync with Voidform. |
| Shadowfiend / Mindbender / Voidwraith | Pet (proc summon) | — | Passive proc | Summoned by Depth of Shadows / talents; melee pet that funnels Insanity & enables Inescapable Torment SW:D. |
| Void Apparitions | Passive (talent) | — | — | **A passive, not a button [T1]** — no castable spell of this name exists; every ID carries the passive attribute. Talented Void-damage apparitions ride along with the Tentacle Slam / DoT package. |
| Holy Nova | Utility / off-heal | — | Instant | AoE heal+damage; in the APL only used to proc Twist of Fate healing (niche). |
| Dispersion | Defensive (major) | — | ~6s channel, 120s [T1] | −75% damage taken while channeled; also purges movement-impairing effects. Class-baseline in Midnight [T1]. |
| Desperate Prayer | Defensive (self-heal) | — | Instant, ~90s CD | Instant self-heal + short max-HP bump; use when SW:D self-damage or spike drops you below ~75%. |
| Vampiric Embrace | Defensive (group heal) | — | Instant, ~2 min | Your shadow damage heals you and nearby allies for a window. |
| Fade | Defensive / Utility | — | Instant, ~30s CD | Drops threat; with talents (Improved Fade / Phantasm) adds damage reduction & snare immunity. |
| Power Word: Shield | Defensive (absorb) | mana | Instant | Absorb shield on self/ally; Body and Soul can add a speed burst. |
| Flash Heal | Off-heal | mana | ~1.5s cast | Emergency heal; in the APL also pressed to proc a trinket (Nexus-King's Command). |
| Silence | Interrupt / CC | — | Instant, 30s CD (baseline) | Interrupts a cast and locks the school; short silence. Baseline in Midnight. |
| Psychic Scream | CC (AoE fear) | mana | Instant / **40s** `[T1]` | Fears nearby enemies; Petrifying Scream (talent) roots instead. |
| Shackle Horror | CC (single) | mana | ~1.5s cast | Incapacitates a Horror/Undead-type enemy (renamed Shackle Undead). |
| Mind Control / Dominate Mind | CC (control) | mana | ~1.8s cast · Dominate Mind **30s** `[T1]` | Takes control of an enemy (choice node). Dominate Mind 205364 `talent-choice`; the cast time is Tier-3. |
| Mind Soothe | Utility (pull control) | mana | Instant | Reduces an enemy's aggro range. |
| Dispel Magic | Dispel (offensive/defensive) | mana | Instant | Removes a magic effect from an ally or purges an enemy buff. |
| Purify Disease | Dispel | mana | Instant | Removes disease effects from an ally. |
| Mass Dispel | Dispel (AoE) | mana | ~1.5s cast / **120s** `[T1]` | Removes magic from multiple allies / enemies; can strip some immunities. |
| Leap of Faith | Utility (movement/save) | mana | Instant, CD | "Life Grip" — pulls a targeted ally to you. |
| Angelic Feather | Movement | — | Instant, charges | Places a feather that grants a large speed burst when walked over. |
| Levitate | Movement / Utility | mana | Instant | Slow fall / walk-on-water travel utility. |
| Power Word: Fortitude | Utility (raid buff) | mana | ~1.5s cast | Raid-wide +Stamina buff. |
| Resurrection | Utility (res) | mana | Out of combat | Revives a dead ally. |
| Shadowform | Passive (stance) | — | — | The DPS stance; kept up at all times (precombat cast if down). |

## Reconciliation notes — Tier 1 @ 12.0.7.67808

- **Void Apparitions is a passive**, not a pressed ability — corrected above. Tier 1 has no
  castable spell of that name at any ID.
- Cooldowns corrected against the guide values previously carried here: **Void Torrent 30s**
  (was ~15s), **Halo 60s** (was ~20s), **Dispersion 120s** (was ~90s).
- **Void Volley and Mind Flay: Insanity keep their open questions on purpose.** Void Volley
  carries a live `@verify-ingame`; **Mind Flay: Insanity does not** — it is recorded in
  `../../_abilities/section-4-catalogue.md` (`prose-only`) instead, which is where an
  unreachable name belongs. Do not read the absence of a marker as a settled claim. Both are
  Midnight override/proc-replacement buttons with no acquisition row in DB2: Void Volley has
  eight Midnight-range spell IDs and no attachment (and `Void Bolt`, the button it replaced,
  is itself gone from tree 795, with the Voidweaver subtree now carrying `Void Blast` /
  `Entropic Rift`); Mind Flay: Insanity's parents — `Surge of Insanity` on tree 795 and
  `Mind Flay` via `SpecializationSpells` — are live, but the proc buttons themselves are not
  in any acquisition table. These are tool gaps, not stale claims, and only an in-game
  spellbook enumeration will close them.

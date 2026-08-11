---
title: Elemental Shaman — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/shaman/elemental/ability-inventory.tsv  # tier 1, generated from DB2 @ 12.0.7.67808 — name/spellID/origin/cooldown source of record
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the 12.0.7.67808 adjudication behind this pass
  - raw/wago/SpellName.csv (Blizzard game data, Tier 1)   # tier 1, 2026-07-11
  - simc midnight profiles/MID1/MID1_Shaman_Elemental.simc   # tier 1, 2026-07-11
  - https://www.method.gg/guides/elemental-shaman/playstyle-and-rotation   # tier 3, upd 2026-06-16
  - https://www.icy-veins.com/wow/elemental-shaman-pve-dps-rotation-cooldowns-abilities   # tier 3, 12.0.7
confidence: high
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


# Elemental Shaman — abilities (Midnight S1, 12.0.7)

## Overview

Elemental is a ranged spell-caster that builds and spends **Maelstrom** (a
0–100 resource, raised by talents such as Swelling Maelstrom). Builders —
**Lightning Bolt**, **Chain Lightning**, **Lava Burst**, **Frost Shock** —
generate Maelstrom; spenders — **Earth Shock**, **Earthquake**, **Elemental
Blast** — dump it. **Flame Shock** is a maintained DoT that fuels **Lava
Surge** procs (free instant Lava Bursts) and enables **Lava Burst**. Mastery
(Elemental Overload) gives spells a chance to fire a second, free ~75%-damage
copy — the whole kit is tuned around maximizing overloads.

**Two hero trees:**
- **Stormbringer** — the lightning/single-target tree. Spending Maelstrom
  charges **Tempest**, a hard-hitting overloading nuke that supercharges the
  next Lightning Bolt (stacks to 2). Applies **Lightning Rod**. Default for
  raid / low target counts.
- **Farseer** — the summoning/cleave tree. **Call of the Ancestors** summons
  ancestor spirits (via Stormkeeper / Ancestral Swiftness) that copy your
  casts. Stronger in 2–3 target cleave and Mythic+.

## Ability inventory

> **Where the numbers live.** `ability-inventory.tsv` in this folder is the Tier-1
> source of record for **name, spellID, origin and cooldown** (generated from DB2 @
> `12.0.7.67808`). This table is the *judgement* layer — function, role, rotational
> context — and does not re-transcribe columns that drift with every build.

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
| **Lightning Bolt** | Rotational-builder | Generates Maelstrom | ~2s cast | Primary single-target filler; generates Maelstrom, can Overload. Supercharged by Tempest / instant under Stormkeeper. |
| **Chain Lightning** | Rotational-builder (AoE) | Generates Maelstrom/target | ~2s cast | AoE builder, bounces between targets; the AoE replacement for Lightning Bolt (worth it at ~3 targets Stormbringer / 2 Farseer). |
| **Lava Burst** | Rotational-builder | Generates Maelstrom | 2 charges / ~8s recharge | Guaranteed crit vs a Flame Shocked target. Instant and free when **Lava Surge** is up — the rule is "never hardcast Lava Burst, cast only on Lava Surge." |
| **Flame Shock** | Rotational-builder (DoT) | Generates Maelstrom | instant, 6s CD | Maintained fire DoT; each tick can proc **Lava Surge**. Enables Lava Burst crits. Refresh at ≤ ~6s / pandemic. |
| **Voltaic Blaze** | Rotational-builder (AoE Flame Shock) | Generates Maelstrom | instant (proc-gated) / **10s** `[T1]` | Talent (Voltaic Blaze). Instant nature/fire hit that also applies Flame Shock to up to 5 nearby targets — the AoE Flame Shock spreader. @verify-ingame |
| **Frost Shock** | Rotational-builder / movement filler | Generates Maelstrom | instant, no CD | Instant filler; usable while moving. Slows the target. Low priority — a movement/overcap-dump button. |
| **Earth Shock** | Rotational-spender | Spends Maelstrom | instant | Single-target Maelstrom dump (choice node vs Elemental Blast). Instant, so the mobility spender. |
| **Elemental Blast** | Rotational-spender | Spends Maelstrom | ~2s cast | Alternative spender (choice vs Earth Shock): higher damage + grants a random secondary-stat buff, but has a cast time and higher cost. |
| **Earthquake** | Rotational-spender (AoE) | Spends Maelstrom | instant (ground-target) | AoE Maelstrom dump; soft-caps ~20 targets. The AoE replacement for Earth Shock/Elemental Blast. |
| **Tempest** | Rotational-spender (proc) | Charged by spending Maelstrom | instant | **Stormbringer** signature. Charges up after spending Maelstrom; overloads hard and supercharges the next Lightning Bolt/Chain Lightning (stacks to 2). Applies Lightning Rod. |
| **Stormkeeper** | Major cooldown | — | instant, ~1min | Next 2 Lightning Bolts / Chain Lightnings are instant and empowered. On Farseer also summons an ancestor; shorter CD / stacks on Stormbringer. Pair with Ascendance. |
| **Ascendance** | Major cooldown | — | instant, ~3min (First Ascendant/Preeminence adjust) | Burst window: Lava Burst gains charges / no cooldown and overload damage is boosted. Always cast **after** Stormkeeper. Sync with Heroism + trinkets. |
| **Ancestral Swiftness** | Major cooldown / Utility | — | instant / **30s** `[T1]` | **Farseer** active (replaces Nature's Swiftness when talented). Makes the next spell instant, grants haste, and summons an ancestor. Use on cooldown; follow with a cast-time spell. |
| **Nature's Swiftness** | Utility | — | instant, ~1min | Class talent (used when NOT running Ancestral Swiftness): next Nature/Frost spell is instant and empowered. Often spent on an instant Chain Heal / Lava Burst / hardcast filler. |
| **Wind Shear** | Interrupt | — | instant, ~12s | The interrupt — a short-cooldown, no-GCD spell kick. |
| **Astral Shift** | Defensive | — | instant / **120s** `[T1]` | −40% damage taken for ~8s (Nature's Guardian etc. improve). Core personal defensive. |
| **Earth Elemental** | Defensive / Pet | — | instant, **180s** | **Tier-1 origin: `talent-active`** (spell 198103, class tree), cooldown **180s** — not the ~5min this file previously carried from Tier 3. Summons a tanky Earth Elemental to taunt/soak; a threat/defensive tool, strong solo/delve. **This is the only elemental summon the live Shaman tree grants** — see the note at the foot of this file. |
| **Skyfury** | Utility (raid buff) | — | instant, 1hr buff | The Shaman group buff: empowers you and party/raid members' attack and spell power. Cast pre-pull. @verify-ingame |
| **Heroism** | Major cooldown (party) | — | instant, ~5min (10min exhaustion) | Bloodlust/Heroism — party/raid +30% haste for 40s. Sync with Ascendance. (Alliance = Heroism, Horde = Bloodlust.) |
| **Healing Surge** | Utility (heal) | Mana | ~1.5–2s cast | Emergency direct self/ally heal. |
| **Chain Heal** | Utility (heal) | Mana | ~2.5s cast | Bouncing group heal — off-heal utility. |
| **Healing Stream Totem** | Utility (heal) | Mana | instant, ~30s | Drops a totem that trickle-heals the lowest-health nearby ally. |
| **Earth Shield** | Defensive / Utility | Mana | instant, ~1min | Places a charge-based shield on self (Elemental Orbit) or an ally that heals on hit and reduces damage. |
| **Spiritwalker's Grace** | Movement | — | instant / **120s** `[T1]` | Lets you cast normally-stationary spells while moving for ~15s. The caster-mobility button. |
| **Ghost Wolf** | Movement | — | instant | Travel form; +movement speed, quick in/out. |
| **Spirit Walk** | Movement | — | instant, ~1min | Removes movement-impairing effects + speed burst (choice vs Gust of Wind). |
| **Wind Rush Totem** | Movement (group) | — | instant, ~2min | Totem that grants passing allies a movement-speed burst — group mobility. |
| **Capacitor Totem** | CC | — | instant, ~1min | Totem that charges up then AoE-stuns nearby enemies. |
| **Earthgrab Totem** | CC | — | instant / **30s** `[T1]` | Totem roots nearby enemies, then slows them. |
| **Thunderstorm** | CC / Defensive | — | instant, **30s** | **Tier-1 origin: `class-baseline`** (spell 51490, `SpecializationSpells` → **Elemental**), cooldown **30s**. Knocks back nearby enemies and slows them. **Elemental-only** — it is not a shared Shaman button and not a PvP talent (absent from `PvpTalent` entirely); the Enhancement and Restoration files used to claim it and no longer do. |
| **Hex** | CC | Mana | ~1.5s cast, ~30s | Transforms a humanoid/beast enemy into a frog (incapacitate). |
| **Tremor Totem** | Utility (CC break) | — | instant, ~1min | Totem that removes and prevents Fear/Sleep/Charm for nearby allies (choice vs Poison Cleansing Totem). |
| **Purge** | Dispel (offensive) | Mana | instant | Removes a beneficial Magic effect from an enemy (choice vs Greater Purge). |
| **Cleanse Spirit** | Dispel | Mana | instant, ~8s | Removes a Curse from a friendly target. |
| **Totemic Projection** | Utility | — | instant, ~10s | Relocates your active totems to a targeted location. |
| **Ancestral Spirit** | Utility (battle rez) | Mana | ~10s cast | Combat resurrection of a fallen ally (out-of-combat res too). |
| **Lightning Shield** | Passive/buff (maintain) | — | instant | Self-buff that damages melee attackers; kept up (precombat). |
| **Flametongue Weapon** | Utility (imbue) | — | instant | Weapon imbue (talent); maintained buff, applied precombat. |
| **Thunderstrike Ward** | Defensive/buff (imbue) | — | instant | Talent weapon enchant / ward that retaliates with lightning; applied precombat (choice vs Elemental Resonance). |

**Not acquirable at 12.0.7 — `Fire Elemental` and `Storm Elemental` are gone.**
Fire Elemental (198067) and Storm Elemental (192249) attach to **no** live acquisition
row: their only trait attachment is the **legacy** Shaman trees 1033/1034 (the trees that
still carry the pre-Midnight set — Icefury, Primordial Wave, Liquid Magma Totem,
Stormstrike). The **live** Shaman tree is **786**, and it carries `Earth Elemental`
(198103) and the `Primal Elementalist` / `Call of Fire` passives but no Fire or Storm
Elemental node. Both rows have been deleted rather than left marked; the burst window
they used to anchor is Stormkeeper → Ascendance. Do not restore them from a Tier-3 guide
without a fresh DB2 read — a guide describing them is describing The War Within.
*[Tier 1: DB2 @ 12.0.7.67808, via `_abilities/reconcile-ledger.md`.]*

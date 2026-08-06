---
title: Priest Holy — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/priest/holy/ability-inventory.tsv  # tier 1, generated from DB2 @ build 12.0.7.67808 — name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - https://www.method.gg/guides/holy-priest  # tier 3, upd. 2026-06-16
  - https://www.method.gg/guides/holy-priest/playstyle-and-rotation  # tier 3, 2026-06-16
  - https://www.icy-veins.com/wow/holy-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/holy-priest-pve-healing-easy-mode  # tier 3, 12.0.7
  - knowledge/classes/priest/holy/talents.md  # tier 1, Blizzard talent-tree API @ 12.0.7.67808
  - raw/wago/SpellName.csv  # tier 1, spell-name reconciliation
confidence: medium
---

# Priest Holy — Ability Inventory (Midnight S1)

## Overview

Holy is Priest's atonement-free, throughput-and-spot-heal spec. It has **no
secondary resource beyond mana** — its rotational engine is **Holy Words**.
Casting normal spells reduces Holy Word cooldowns via **Serendipity**: **Flash Heal**
reduces **Holy Word: Serenity** (single-target nuke-heal), **Prayer of Healing** reduces
**Holy Word: Sanctify** (group nuke-heal), and **Smite** reduces **Holy Word: Chastise**
(damage + stun). So the playstyle is "cast the right filler to bring the right Holy Word
online, then fire it." **Mastery: Echo of Light** leaves a HoT behind every direct heal, and
**Prayer of Mending** (a bouncing heal kept on cooldown) is a second always-on
passive-value stream. The Midnight kit is narrower than the one most guides describe —
**Heal**, **Renew** and **Circle of Healing** are no longer acquirable (see the
reconciliation notes), so the Serendipity feeders are Flash Heal and Prayer of Healing.

**Hero trees (both viable in S1):**
- **Archon** — turns Prayer of Healing into the primary throughput button;
  **Halo** becomes a 40s cooldown that grants Surge of Light procs, and
  **Spiritwell** lets those procs empower Prayer of Healing. Burst-window / raid
  AoE lean.
- **Oracle** — passive, consistent value centered on Prayer of Mending
  enhancements (Guiding Light, Prompt Prognosis, Piety, Prophet's Insight).
  Lower-maintenance, strong for spread/rot damage.

## Ability table

**`ability-inventory.tsv` in this directory is the Tier-1 floor** — canonical name, spellID,
origin and baseline cooldown are regenerated there from DB2 and are not duplicated here.
This file is the prose layer: the Holy Word loop and what each button is for.

A cooldown written **`60s [T1]`** was read off that tsv (DB2 @ build 12.0.7.67808) and is
the baseline before talents and Haste; `~` values are guide-derived. `@verify-ingame` marks
what Tier 1 could not settle — durations, percentages, CC types and charge *recharge* times
(the tsv's cooldown column returns the GCD for charge abilities such as Prayer of Mending).

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
| Holy Word: Serenity | Rotational-spender (heal) | Mana | 1.5s cast / ~60s CD | Large single-target heal; the payoff for Flash Heal / Heal casts (Serendipity reduces its CD). @verify-ingame (exact CD/reduction) |
| Holy Word: Sanctify | Rotational-spender (heal) | Mana | 1.5s cast / ~60s CD | Large ground/group heal; payoff for Prayer of Healing / Renew casts. @verify-ingame (exact CD) |
| Holy Word: Chastise | Rotational-spender / CC | Mana | Instant / 60s [T1] | Holy damage + incapacitate/stun; payoff for Smite. With **Empyreal Blaze** it resets/empowers Holy Fire, making it a DPS/AoE-damage button. @verify-ingame (CC type) |
| Prayer of Mending | Rotational-builder (heal) | Mana | Instant / ~12s recharge | Bouncing heal-shield kept on cooldown; core passive-value stream. Enhanced heavily by Oracle. @verify-ingame (charges/CD) |
| Flash Heal | Frequent (heal) | Mana | 1.5s cast / — | Fast single-target heal; reduces Holy Word: Serenity CD. Builds **Lightweaver** stacks. Free/instant with Surge of Light. |
| Prayer of Healing | Frequent (AoE heal) | Mana | ~2s cast / — | Group heal (5 targets); reduces Holy Word: Sanctify CD. Archon's main throughput button (empowered by Surge of Light / Spiritwell). |
| Holy Nova | Situational (AoE heal+dmg) | Mana | Instant / — | Instant PBAoE heal + damage; strong while moving. Damage source with **Lightburst**. |
| Benediction | Rotational (heal) | Mana | Instant / — | Apex talent — an upgraded/empowered heal tied to Prayer of Mending bounces (baseline points give a flat healing increase). @verify-ingame (exact effect) |
| Halo | Major cooldown / Rotational (Archon) | Mana | Instant / 60s [T1] | Expanding ring: heals allies + damages enemies. Under Archon grants **4 Surge of Light** procs over its duration for Prayer of Healing, and Archon shortens the cooldown below the baseline above. |
| Apotheosis | Major cooldown | Mana | Instant / 120s [T1] | Triples Holy Word cooldown reduction and empowers them for a short window — spam Holy Words while active. @verify-ingame (duration) |
| Divine Hymn | Major cooldown | Mana | ~8s channel / 180s [T1] | Channeled raid-wide heal; also increases healing received by the group (~20%). @verify-ingame (%) |
| Guardian Spirit | Defensive / Major cooldown | Mana | Instant / 180s [T1] | Places a cheat-death on an ally that also increases their healing received ~60%; on lethal hit it prevents death instead. |
| Power Infusion | Major cooldown (throughput) | Mana | Instant / 120s [T1] | +25% haste for 20s; cast on self or a DPS (self via **Twins of the Sun Priestess**). @verify-ingame (values) |
| Desperate Prayer | Defensive | Mana | Instant / ~90s CD | Self-heal + temporary max-health increase. |
| Smite | Rotational-builder (damage) | Mana | ~1.5s cast / — | Filler damage; reduces Holy Word: Chastise CD. Primary DPS filler when no healing is needed. |
| Holy Fire | Rotational (damage) | Mana | ~1.5s cast / 10s [T1] | Damage + DoT; kept on cooldown for DPS. With **Burning Vehemence** it cleaves nearby enemies; reset/empowered by Empyreal Blaze. |
| Shadow Word: Death | Rotational (damage) / execute | Mana | Instant / ~10s CD (charges) | Instant Shadow damage, bonus vs low-health targets; backlash if target survives. @verify-ingame (charges/CD) |
| Power Word: Fortitude | Utility (raid buff) | Mana | Instant / — | Raid-wide +5% Stamina, 60-min buff. |
| Levitate | Movement / Utility | Mana | ~1.5s cast / — | Slow-fall buff on an ally. |
| Leap of Faith | Utility (movement) | Mana | Instant / ~1.5min CD | "Life Grip" — yanks a targeted ally to you. @verify-ingame (CD) |
| Angelic Feather | Movement | Mana | Instant / ~20s recharge (charges) | Ground feather that grants a big move-speed burst to whoever steps on it. |
| Fade | Defensive / Utility | — | Instant / 30s [T1] | Drops threat; with **Translucent Image** grants ~10% damage reduction. |
| Psychic Scream | CC | Mana | Instant / **40s** `[T1]` | AoE fear (short). |
| Shackle Horror | CC | Mana | ~1.5s cast / — | Incapacitates an Undead/Horror target (formerly "Shackle Undead"). @verify-ingame (target type) |
| Mind Control | CC | Mana | Channel / — | Takes control of an enemy (mostly outdoor/PvP). |
| Mind Soothe | Utility | Mana | Instant / — | Reduces an enemy's detection range (skip pulls). |
| Purify | Dispel | Mana | Instant / 8s [T1] | Removes Magic + Disease from an ally. @verify-ingame (schools) |
| Dispel Magic | Dispel (offensive) | Mana | Instant / — | Removes a beneficial Magic effect from an enemy. |
| Mass Dispel | Dispel (AoE) | Mana | ~1.5s cast / 120s [T1] | Area dispel; removes Magic from allies + purges enemies; can strip normally-undispellable effects. |
| Resurrection | Utility (combat res of dead) | Mana | ~10s cast / — | Out-of-combat revive. |
| Mastery: Echo of Light | Passive | — | — | Direct heals leave a HoT healing for a % of the amount over 6s — the spec's signature passive throughput. @verify-ingame (%) |
| Surge of Light | Passive (proc) | — | — | Procs a free, instant Flash Heal (or Prayer of Healing under Archon/Spiritwell). |
| Lightweaver | Passive (talent) | — | — | Flash Heal builds stacks that make the next Prayer of Healing cheaper/stronger; don't cast Prayer of Healing without a stack (Archon). |
| Empyreal Blaze | Passive (talent) | — | — | Holy Word: Chastise resets/empowers Holy Fire — the DPS/AoE-damage enabler. |
| Restitution | Passive (talent) | — | — | Death-prevention: extends/replaces Spirit of Redemption as a cheat-death (progression pick over Guardian Angel). @verify-ingame (exact effect) |

## Reconciliation notes — Tier 1 @ 12.0.7.67808

Three heals this file listed are **not acquirable at 12.0.7** and their rows are deleted.
Each was checked against every acquisition table — trait nodes on the live Priest tree
(**795**), `SkillLineAbility` on the Priest line (**804**), `SpecializationSpells` and
`PvpTalent` — and attaches to none of them:

- **Heal** (2060) — the Priest kit carries Flash Heal, Power Word: Shield, Prayer of Mending
  and Smite; it does not carry Heal, and none of the other 112 spells named "Heal" attaches
  either.
- **Renew** (139) — tree 795 has `Renewed Faith`, but no Renew.
- **Circle of Healing** — no node on tree 795 and no other attachment.

This is a real narrowing of the spec, not a bookkeeping detail: **Serendipity now runs off
Flash Heal and Prayer of Healing**, and any guide still describing a Heal/Renew filler loop
is describing The War Within.

- **Mastery: Echo of Light keeps its `@verify-ingame` marker on purpose.** It *is* attached
  (`SpecializationSpells` → Holy, spell 77485); it is simply passive, and the generator drops
  passive `SpecializationSpells` rows, so the tsv cannot corroborate its magnitude. Tool gap,
  not a stale claim.
- **Halo is 60s baseline** (Archon shortens it) — the file carried Archon's reduced value as
  the baseline. **Mass Dispel is 120s**, not ~1 min.
- Markers on Apotheosis (duration), Divine Hymn (%), Power Infusion (values), Chastise (CC
  type), Purify (schools) and Prayer of Mending (charge recharge) stay open: those are cast
  times, magnitudes and recharge rates, which the Tier-1 join carries no column for.

---
title: Priest Holy — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
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
Casting normal spells reduces Holy Word cooldowns via **Serendipity**: Flash
Heal / Heal reduce **Holy Word: Serenity** (single-target nuke-heal), Prayer of
Healing / Renew reduce **Holy Word: Sanctify** (group nuke-heal), and Smite
reduces **Holy Word: Chastise** (damage + stun). So the playstyle is "cast the
right filler to bring the right Holy Word online, then fire it." **Mastery: Echo
of Light** leaves a HoT behind every direct heal, and **Prayer of Mending** (a
bouncing heal kept on cooldown) is a second always-on passive-value stream.

**Hero trees (both viable in S1):**
- **Archon** — turns Prayer of Healing into the primary throughput button;
  **Halo** becomes a 40s cooldown that grants Surge of Light procs, and
  **Spiritwell** lets those procs empower Prayer of Healing. Burst-window / raid
  AoE lean.
- **Oracle** — passive, consistent value centered on Prayer of Mending
  enhancements (Guiding Light, Prompt Prognosis, Piety, Prophet's Insight).
  Lower-maintenance, strong for spread/rot damage.

## Ability table

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Holy Word: Serenity | Rotational-spender (heal) | Mana | 1.5s cast / ~60s CD | Large single-target heal; the payoff for Flash Heal / Heal casts (Serendipity reduces its CD). @verify-ingame (exact CD/reduction) |
| Holy Word: Sanctify | Rotational-spender (heal) | Mana | 1.5s cast / ~60s CD | Large ground/group heal; payoff for Prayer of Healing / Renew casts. @verify-ingame (exact CD) |
| Holy Word: Chastise | Rotational-spender / CC | Mana | Instant / ~60s CD | Holy damage + incapacitate/stun; payoff for Smite. With **Empyreal Blaze** it resets/empowers Holy Fire, making it a DPS/AoE-damage button. @verify-ingame (CC type + CD) |
| Prayer of Mending | Rotational-builder (heal) | Mana | Instant / ~12s recharge | Bouncing heal-shield kept on cooldown; core passive-value stream. Enhanced heavily by Oracle. @verify-ingame (charges/CD) |
| Flash Heal | Frequent (heal) | Mana | 1.5s cast / — | Fast single-target heal; reduces Holy Word: Serenity CD. Builds **Lightweaver** stacks. Free/instant with Surge of Light. |
| Heal | Frequent (heal) | Mana | ~2.5s cast / — | Slow, mana-efficient single-target heal; also reduces Holy Word: Serenity CD. |
| Prayer of Healing | Frequent (AoE heal) | Mana | ~2s cast / — | Group heal (5 targets); reduces Holy Word: Sanctify CD. Archon's main throughput button (empowered by Surge of Light / Spiritwell). |
| Renew | Frequent (HoT) | Mana | Instant / — | Heal-over-time; reduces Holy Word: Sanctify CD. Also applied for free by **Lasting Words** on Holy Word casts. |
| Circle of Healing | Frequent (AoE heal) | Mana | Instant / ~15s CD | Instant smart AoE heal around a target (talent). @verify-ingame (talented?/CD) |
| Holy Nova | Situational (AoE heal+dmg) | Mana | Instant / — | Instant PBAoE heal + damage; strong while moving. Damage source with **Lightburst**. |
| Benediction | Rotational (heal) | Mana | Instant / — | Apex talent — an upgraded/empowered heal tied to Prayer of Mending bounces (baseline points give a flat healing increase). @verify-ingame (exact effect) |
| Halo | Major cooldown / Rotational (Archon) | Mana | Instant / ~40s CD | Expanding ring: heals allies + damages enemies. Under Archon grants **4 Surge of Light** procs over its duration for Prayer of Healing. @verify-ingame (CD) |
| Apotheosis | Major cooldown | Mana | Instant / ~2min CD | Triples Holy Word cooldown reduction and empowers them for a short window — spam Holy Words while active. @verify-ingame (duration) |
| Divine Hymn | Major cooldown | Mana | ~8s channel / ~3min CD | Channeled raid-wide heal; also increases healing received by the group (~20%). @verify-ingame (CD/%) |
| Guardian Spirit | Defensive / Major cooldown | Mana | Instant / ~3min CD | Places a cheat-death on an ally that also increases their healing received ~60%; on lethal hit it prevents death instead. @verify-ingame (CD) |
| Power Infusion | Major cooldown (throughput) | Mana | Instant / ~2min CD | +25% haste for 20s; cast on self or a DPS (self via **Twins of the Sun Priestess**). @verify-ingame (values) |
| Desperate Prayer | Defensive | Mana | Instant / ~90s CD | Self-heal + temporary max-health increase. |
| Smite | Rotational-builder (damage) | Mana | ~1.5s cast / — | Filler damage; reduces Holy Word: Chastise CD. Primary DPS filler when no healing is needed. |
| Holy Fire | Rotational (damage) | Mana | ~1.5s cast / ~10s CD | Damage + DoT; kept on cooldown for DPS. With **Burning Vehemence** it cleaves nearby enemies; reset/empowered by Empyreal Blaze. @verify-ingame (CD) |
| Shadow Word: Death | Rotational (damage) / execute | Mana | Instant / ~10s CD (charges) | Instant Shadow damage, bonus vs low-health targets; backlash if target survives. @verify-ingame (charges/CD) |
| Power Word: Fortitude | Utility (raid buff) | Mana | Instant / — | Raid-wide +5% Stamina, 60-min buff. |
| Levitate | Movement / Utility | Mana | ~1.5s cast / — | Slow-fall buff on an ally. |
| Leap of Faith | Utility (movement) | Mana | Instant / ~1.5min CD | "Life Grip" — yanks a targeted ally to you. @verify-ingame (CD) |
| Angelic Feather | Movement | Mana | Instant / ~20s recharge (charges) | Ground feather that grants a big move-speed burst to whoever steps on it. |
| Fade | Defensive / Utility | — | Instant / ~30s CD | Drops threat; with **Translucent Image** grants ~10% damage reduction. @verify-ingame (CD) |
| Psychic Scream | CC | Mana | Instant / ~30s CD | AoE fear (short). |
| Shackle Horror | CC | Mana | ~1.5s cast / — | Incapacitates an Undead/Horror target (formerly "Shackle Undead"). @verify-ingame (target type) |
| Mind Control | CC | Mana | Channel / — | Takes control of an enemy (mostly outdoor/PvP). |
| Mind Soothe | Utility | Mana | Instant / — | Reduces an enemy's detection range (skip pulls). |
| Purify | Dispel | Mana | Instant / ~8s CD | Removes Magic + Disease from an ally. @verify-ingame (schools/CD) |
| Dispel Magic | Dispel (offensive) | Mana | Instant / — | Removes a beneficial Magic effect from an enemy. |
| Mass Dispel | Dispel (AoE) | Mana | ~1.5s cast / ~1min CD | Area dispel; removes Magic from allies + purges enemies; can strip normally-undispellable effects. @verify-ingame (CD) |
| Resurrection | Utility (combat res of dead) | Mana | ~10s cast / — | Out-of-combat revive. |
| Mastery: Echo of Light | Passive | — | — | Direct heals leave a HoT healing for a % of the amount over 6s — the spec's signature passive throughput. @verify-ingame (%) |
| Surge of Light | Passive (proc) | — | — | Procs a free, instant Flash Heal (or Prayer of Healing under Archon/Spiritwell). |
| Lightweaver | Passive (talent) | — | — | Flash Heal builds stacks that make the next Prayer of Healing cheaper/stronger; don't cast Prayer of Healing without a stack (Archon). |
| Empyreal Blaze | Passive (talent) | — | — | Holy Word: Chastise resets/empowers Holy Fire — the DPS/AoE-damage enabler. |
| Restitution | Passive (talent) | — | — | Death-prevention: extends/replaces Spirit of Redemption as a cheat-death (progression pick over Guardian Angel). @verify-ingame (exact effect) |

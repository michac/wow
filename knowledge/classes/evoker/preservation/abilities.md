---
title: Evoker Preservation — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw/wago/SpellName.csv  # tier 1, 2026-07-11 — every ability name below canonicalized against game data
  - https://www.method.gg/guides/preservation-evoker  # tier 3, 2026-07-11 — playstyle framing
  - https://www.method.gg/guides/preservation-evoker/playstyle-and-rotation  # tier 3, 2026-07-11 — ability roles
  - https://www.icy-veins.com/wow/preservation-evoker-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/preservation-evoker-mythic-plus-guide  # tier 3, 2026-07-11 — Spiritbloom/Engulf removal
confidence: medium
---

# Evoker Preservation — abilities (Midnight S1, 12.0.7)

## Overview

Preservation is the Evoker healing spec: a **mid-range (25-yd) empower-and-HoT
healer** built around *preparation* — pre-spreading HoTs and shields, then
duplicating them with **Echo** so a single follow-up heal lands on many targets
at once. It heals best when the group is stacked.

- **Resource: Essence** (5 max; **6** with *Font of Magic* / *Power Nexus*).
  Essence regenerates over time (faster with haste) and is spent on **Echo**,
  **Emerald Blossom**, **Reversion**, and **Disintegrate**. **Essence Burst** is
  a proc (from Reversion / Living Flame / Fire Breath, per talents) that makes
  the **next Essence spell free** — the spec's core economy.
- **Empower spells** are press-and-**hold** to charge through ranks I–IV, then
  release: higher rank = more targets / more front-loaded healing but longer
  cast. Preservation's empowers are **Dream Breath**, **Fire Breath**,
  **Temporal Anomaly**, and **Deep Breath**.
- **Echo** is the signature mechanic: it places a buff so your **next healing
  spell is duplicated** onto the echoed ally (all effects, including HoTs and
  shields). Most of the spec is "build Echoes → consume with a big heal."

> **Midnight removal (verify-ingame):** **Spiritbloom**, **Emerald Communion**,
> and **Engulf** were **removed from Preservation this patch** (maxroll M+ guide,
> 12.0.7) — the old one-button raid-burst heal is gone. Do not list them as
> current abilities. @verify-ingame

## Inventory

Cast/CD values marked "~" are approximate baselines carried from live retail and
not re-pulled from a Tier-1 tooltip this pass — treat as provisional. @verify-ingame

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Reversion** | Rotational-builder (core HoT) | 2 Essence | Instant / — | Primary HoT. Kept rolling on the whole group; **double-stacked** on the tank via Echo. Generates **Essence Burst**. Amped by Grace Period / Golden Hour. |
| **Echo** | Rotational-builder (setup) | 2 Essence | Instant / — | Buffs an ally so your **next heal is duplicated** onto them. The engine of every ramp; consumed by Verdant Embrace / Merithra's Blessing / Dream Breath / Reversion. |
| **Living Flame** | Rotational-filler / builder | — | ~1.5s / — | Heals an ally (or damages an enemy). Low-cost filler that **generates Essence Burst**; feeds Leaping Flames. |
| **Emerald Blossom** | Rotational-spender | 3 Essence | Instant / — | Delayed AoE burst heal at a target area; **best Essence Burst dump** (more value than Echo). Triggers **Twin Echoes**. |
| **Verdant Embrace** | Spot-heal / movement | — | Instant / ~24s | Flies you to an ally and heals them; applies **Lifebind** (60% of your healing echoes to them for 8s). Strongest single-target combo when Echo-duplicated. |
| **Merithra's Blessing** | Major rotational (apex heal) | Essence Burst / proc | Instant / — | Apex-talent burst heal that **bounces to ~5 lowest-health targets** and places Reversion on echoed allies. The default Echo finisher; procs from Dream Breath + Essence spends. |
| **Dream Breath** | Rotational cooldown (empower) | — | Empower / ~30s | Frontal AoE burst + HoT. **Rank 1 on cooldown** for the guaranteed Merithra's Blessing proc; higher ranks only for immediate heavy AoE. Reduced CD by Temporal Anomaly. |
| **Temporal Anomaly** | Rotational cooldown (empower) | — | Empower / ~1min | Slow-moving orb that **shields the group** and spreads **weak (50%) Echoes** across party; also reduces Dream Breath CD. Main Echo-blanket / Reversion-spread engine. @verify-ingame |
| **Fire Breath** | Rotational cooldown (empower, damage) | — | Empower / ~30s | Frontal fire damage + DoT; **generates Essence Burst** (via Afterimage) and feeds Leaping Flames / Life-Giver's Flame healing. Max rank on CD in Chronowarden DPS windows. |
| **Disintegrate** | Rotational-spender (damage) | 3 Essence | Channel ~3s / — | Blue-magic damage channel. Only used in the **Energy Loop** mana build — spend excess Essence for mana return. |
| **Azure Strike** | Damage (filler) | — | Instant / — | Instant blue damage to 2 targets. Off-heal-time filler damage. |
| **Rewind** | Major cooldown (emergency raid heal) | — | Instant / ~4min | Heals the group based on **recent damage taken** — the strongest raw heal. Use right after a big raid hit. |
| **Stasis** | Major cooldown (stored heals) | — | Instant / ~90s | Records your next **3 healing spells**, then re-releases them all at once. Load with high-impact heals for a burst window. |
| **Dream Flight** | Major cooldown (raid heal) | — | ~1.5s / ~2min | Fly forward, healing everyone crossed + a HoT. Best in large (20+) raids. Choice vs **Stasis**. |
| **Tip the Scales** | Cooldown (empower enabler) | — | Instant / ~2min | Makes your **next empower spell cast instantly at max rank**. Chronowarden turns it into throughput via Temporal Burst (haste + CDR). |
| **Zephyr** | Defensive (party) | — | Instant / ~2min | ~20% damage reduction + HoT for the 5 nearest allies, 8s. |
| **Time Dilation** | Defensive (external) | — | Instant / ~1min | Absorbs/delays damage dealt to a target ally over the next several seconds — an external cooldown. |
| **Obsidian Scales** | Defensive (self) | — | Instant / ~90s, 2 charges | ~30% damage reduction. Can trigger Renewing Blaze healing (talent). |
| **Renewing Blaze** | Defensive (self heal) | — | Instant / ~90s | Heals you over time for damage taken during the window (class talent). |
| **Rescue** | Movement / utility (external) | — | Instant / ~1min | Flies to an ally (or grips them) to reposition them out of danger; can grant a shield (Twin Guardian). |
| **Spatial Paradox** | Cooldown (empower enabler, external) | — | Instant / ~1.5min | Next empower for you **and** a targeted ally is instant + hastes them. Choice vs **Time Spiral**. |
| **Time Spiral** | Utility (raid mobility) | — | Instant / ~2min | Lets allies cast an empower / benefit while moving. Choice vs Spatial Paradox. |
| **Cauterizing Flame** | Dispel (offensive-ish) + heal | — | Instant / ~1min | Removes a Bleed/Poison/Curse/Disease from an ally and heals them. |
| **Naturalize** | Dispel | — | Instant / ~8s (GCD) | Removes **Magic and Poison** from an ally (the Preservation group dispel). |
| **Expunge** | Dispel | — | Instant / ~8s | Removes **Poison** from an ally (class-tree option). |
| **Source of Magic** | Utility (mana) | — | Instant / — | Buffs an ally so a share of your healing/regen returns them **mana** (put on another healer / mana user). |
| **Blessing of the Bronze** | Utility (raid buff) | — | Instant / — | Raid-wide buff removing snares / boosting movement — the Evoker group buff. |
| **Fury of the Aspects** | Major cooldown (Bloodlust) | — | Instant / ~5min | The Evoker **Bloodlust/Heroism** equivalent (+30% haste, Exhaustion after). |
| **Sleep Walk** | CC | — | ~1.5s / — | Puts an enemy to sleep (incapacitate); breaks on damage. |
| **Landslide** | CC (root) | — | Instant / ~90s | Roots enemies in place. |
| **Oppressing Roar** | CC (utility) | — | Instant / ~2min | Increases the duration of crowd control on affected enemies (and can add a disorient via talent). |
| **Tail Swipe** | CC (knockback) | — | Instant / ~3min | Cone knockback behind you. |
| **Swoop Up** | CC / utility | — | Instant / ~90s | Picks up an enemy and drops them at a new location. |
| **Chrono Loop** | CC (PvP-leaning) | — | Instant / ~1min | Traps an enemy; after a few seconds returns them to their position and health. |
| **Time Stop** | Defensive (external) | — | Instant / ~1min | Freezes an ally in time — briefly invulnerable but unable to act. @verify-ingame |
| **Hover** | Movement | — | Instant / ~35s, 2 charges | Lets you **cast while moving** and hover briefly. Core mobility for the empower playstyle. |
| **Deep Breath** | Movement / damage | — | Instant / ~2min | Fly across the battlefield dealing damage along the path. Mobility + minor damage. @verify-ingame |
| **Verdant Embrace (Lifebind)** | Passive (talent) | — | — | Lifebind: 60% of your healing to a Verdant Embrace target also heals allies near them. Central to the ramp. |
| **Essence Burst** | Passive (resource proc) | — | — | Makes the next Essence spell **free**; procs from Reversion / Living Flame / Fire Breath per talents. The economy backbone. |
| **Return** | Utility (movement) | — | Instant / — | Teleport back to a previously placed point (with the portal talent). |

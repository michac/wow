---
title: Restoration Druid — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree  # Blizzard Game Data API, tier 1, 2026-07-11 (via knowledge/classes/druid/restoration/talents.md, build 12.0.7.67808)
  - raw/wago/SpellName.csv  # tier 1 game data name canonicalization, 2026-07-11
  - https://www.icy-veins.com/wow/restoration-druid-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7 (upd 2026-06-15)
  - https://www.method.gg/guides/restoration-druid/playstyle-and-rotation  # tier 3, 12.0.7 (upd 2026-06-16)
  - https://www.wowhead.com/guide/classes/druid/restoration/rotation-cooldowns-pve-healer  # tier 4, 12.0.7 (Voulk, 2026-06-12)
confidence: high
---

# Restoration Druid — Abilities (Midnight Season 1)

## Overview

Restoration is the Druid healing spec: a **hybrid HoT (heal-over-time)
healer** whose strength is layering many overlapping regen effects and then
amplifying them, rather than reacting with big single-target casts.

- **Resource:** Mana. No secondary resource in caster form. When the spec
  dips into **Cat Form** (Wildstalker cat-weaving) it uses **Energy + Combo
  Points**; **Bear Form** uses **Rage**. Mana regen is helped by damage
  spells via *Master Shapeshifter* and by *Innervate*.
- **Hero trees (12.0):** **Keeper of the Grove** (Grove Guardian treant
  summons tied to Swiftmend/Wild Growth, cooldown reduction, *Protective
  Growth* defense) and **Wildstalker** (Symbiotic Blooms from
  Wild Growth/Regrowth/Efflorescence that amplify regular healing, plus a
  cat-weaving damage loop). See `builds.md`.
- **Playstyle:** "Ramp" a bed of Rejuvenations (up to ~10–12) to power
  *Abundance* (cheap, near-guaranteed-crit Regrowths), keep Lifebloom +
  Efflorescence + Wild Growth rolling, and spend Swiftmend on cooldown to
  drive *Soul of the Forest* / *Power of the Archdruid* / Grove Guardians.
  Midnight intentionally slowed the pace of healing so recovery from heavy
  damage is more gradual.

## Ability inventory

Cast/CD values are the live 12.0.7 baseline where a Tier-1/Tier-3 source
confirms them; entries where the exact cooldown could not be pinned to a
Tier-1 tooltip carry `@verify-ingame`.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Rejuvenation** | Rotational-builder | Mana | Instant / — | Core rolling HoT. The stack you maintain across the raid/party; each active Rejuv feeds *Abundance* (cheaper, higher-crit Regrowth). |
| **Regrowth** | Rotational-spender | Mana | 1.5s / — | Direct heal + short HoT. With a full *Abundance* stack it becomes near-instant-value spot healing (up to +96% crit); free with *Clearcasting* (Omen of Clarity). |
| **Lifebloom** | Rotational-builder | Mana | Instant / — | Single-target HoT that **blooms** (burst heal) when it expires or is Swiftmended. Stacks/auto-refreshes up to 3 via *Everbloom*; refresh in the last ~4.5s. Kept on tank (and often self). Feeds *Clearcasting* procs. |
| **Wild Growth** | Rotational-builder | Mana | Instant / ~8s @verify-ingame | Smart AoE HoT on injured allies (up to 9 with *Incarnation*). Triggers Wildstalker *Symbiotic Blooms* and summons Keeper-of-the-Grove **Grove Guardians**. |
| **Swiftmend** | Rotational-spender | Mana | Instant / ~15s @verify-ingame | Instant burst heal that consumes a Rejuv/Regrowth (not with *Verdant Infusion*). The engine of the rotation: procs *Soul of the Forest*, *Power of the Archdruid*, Grove Guardians, and extends nearby HoTs. |
| **Efflorescence** | Rotational-builder | Mana | Instant / — | Ground-targeted AoE healing zone (blossoms). High mana cost; place under stacked melee. *Lifetreading* auto-repositions it to the Lifebloom target. |
| **Nourish** | Rotational-spender | Mana | ~2s / — | Slow, mana-efficient direct heal (talent/utility filler). Rarely core; used when mana-starved. @verify-ingame |
| **Tranquility** | Major cooldown | Mana | Channeled (~8s) / ~180s | Big raid-wide channeled heal; extends active HoTs and grants knockback immunity. In 12.0 also applies **Flourish** (HoT-extension) via talent. *Inner Peace* → −20% damage taken while channeling. |
| **Incarnation: Tree of Life** | Major cooldown | Mana | Instant / ~180s @verify-ingame | 30s form: +healing, cheaper/instant Regrowth, Rejuv affects an extra target, Wild Growth hits up to 9. Choice-node vs Convoke; default for Keeper of the Grove. |
| **Convoke the Spirits** | Major cooldown | Mana | Channeled (~4s) / ~120s (→~60s w/ *Cenarius' Guidance*) | Channels a burst of random Druid spells (many Swiftmend/Wild Growth/Rejuv casts); with Keeper summons up to 5 Grove Guardians. Choice-node vs Incarnation. |
| **Flourish** | Rotational-spender / CD | Mana | Instant / ~90s @verify-ingame | Extends the duration of all your active HoTs by ~8s and briefly boosts their rate. Talent (choice vs *Inner Peace*); also auto-triggered by Tranquility in 12.0. |
| **Grove Guardians** | Pet (summon) | Mana | Passive/charge (via Swiftmend, Wild Growth) | Keeper-of-the-Grove treants; each active guardian grants +5% healing done, stacking to +25%. Not a directly-cast button — spawned by rotational casts and Convoke. |
| **Nature's Swiftness** | Utility (empower) | Mana | Instant / ~60s | Makes the next Regrowth (or other cast) instant and stronger — emergency spot heal. |
| **Innervate** | Utility (mana) | Mana | Instant / ~180s | 8s of free spellcasting (0 mana). Used during a ramp / expensive Efflorescence window; can be cast on another healer. |
| **Ironbark** | Defensive (external) | Mana | Instant / ~90s @verify-ingame | Targeted 20% damage reduction on an ally (12s). *Stonebark*/*Improved Ironbark* modify it. Core tank/spot external. |
| **Barkskin** | Defensive (personal) | — | Instant / ~60s @verify-ingame | −20% damage taken self-defensive, usable in any form and while CC'd. |
| **Nature's Cure** | Dispel | Mana | Instant / 8s (GCD) | Resto dispel — removes Magic, Curse, and Poison from an ally. *Improved Nature's Cure* adds a small heal. |
| **Soothe** | Dispel (offensive) | Mana | Instant / 10s | Removes an Enrage effect from an enemy. (Choice-node vs *Cyclone*.) |
| **Rebirth** | Utility (combat res) | Mana | ~2s / 10min (charges) | Battle resurrection of a dead ally in combat. |
| **Revive** | Utility (res) | Mana | ~8s / — | Out-of-combat resurrection. |
| **Mark of the Wild** | Utility (raid buff) | Mana | Instant / — | Raid-wide +Versatility buff. Cast pre-pull. |
| **Symbiotic Relationship** | Utility (buff/heal-share) | Mana | Instant / — | Links you to an ally (usually the tank), sharing a portion of healing/absorb. Cast pre-pull. |
| **Stampeding Roar** | Movement (raid) | — | Instant / ~120s @verify-ingame | Group movement-speed burst (works from any form; *Improved Stampeding Roar* widens range). |
| **Wild Charge** | Movement | — | Instant / ~15s | Form-dependent mobility (leap/dash/etc.). Choice-node vs *Tiger Dash*. |
| **Dash** | Movement | — | Instant / ~120s | Cat Form sprint. |
| **Travel Form** | Movement | — | Instant / — | Fast travel shapeshift (auto-picks flight/land/aquatic). |
| **Entangling Roots** | CC (root) | Mana | 1.5s / — | Single-target root. Baseline soft CC. |
| **Mass Entanglement** | CC (AoE root) | Mana | Instant / ~30s | Roots a target and spreads to nearby enemies. Choice-node vs *Ursol's Vortex*. |
| **Ursol's Vortex** | CC (AoE pull/slow) | Mana | Instant / ~60s | Ground vortex that pulls and slows enemies leaving it. Choice-node vs Mass Entanglement. |
| **Typhoon** | CC (knockback) | Mana | Instant / ~30s | Frontal cone knockback + daze. |
| **Mighty Bash** | CC (stun) | Mana | Instant / ~50s | Single-target stun. Choice-node vs *Incapacitating Roar*. |
| **Incapacitating Roar** | CC (AoE incap) | — | Instant / ~30s | Short AoE incapacitate. Choice-node vs Mighty Bash. |
| **Hibernate** | CC (sleep) | Mana | 1.5s / — | Sleeps a Beast or Dragonkin. |
| **Cyclone** | CC (banish) | Mana | 1.5s / — | Removes a target from combat (untargetable) briefly. Choice-node vs Soothe. |
| **Moonfire** | Rotational (damage DoT) | Mana | Instant / — | Arcane DoT. Baseline damage; used for downtime DPS and Wildstalker weaving. |
| **Sunfire** | Rotational (damage DoT) | Mana | Instant / — | AoE-spreading Nature DoT. Downtime/Wildstalker DPS. |
| **Wrath** | Rotational (damage filler) | Mana | ~1.5s / — | Nature nuke; downtime DPS + *Master Shapeshifter* mana. |
| **Starfire** | Rotational (damage, AoE) | Mana | ~2s / — | Arcane nuke with cleave. Downtime DPS. |
| **Starsurge** | Rotational (damage spender) | Mana | Instant / — | Instant Astral nuke. Downtime DPS. |
| **Heart of the Wild** | Major cooldown (offensive/hybrid) | Mana | Instant / ~5min @verify-ingame | Greatly empowers off-spec abilities (Feral/Balance) for 45s — the enabler for meaningful Wildstalker damage windows (empowered *Feral Frenzy*). |
| **Rake** | Damage (cat, builder) | Energy | Instant / — | Cat-Form combo builder + bleed. Wildstalker weaving (auto-shifts via *Fluid Form*). |
| **Shred** | Damage (cat, builder) | Energy | Instant / — | Cat-Form combo builder. |
| **Rip** | Damage (cat, spender) | Energy/CP | Instant / — | Cat-Form finishing bleed. |
| **Ferocious Bite** | Damage (cat, spender) | Energy/CP | Instant / — | Cat-Form finisher. |
| **Swipe** | Damage (cat, AoE) | Energy | Instant / — | Cat-Form AoE builder (talented). |
| **Cat Form** | Form (utility/damage) | — | Instant / — | Melee/energy form; the Wildstalker damage stance and a speed boost. |
| **Bear Form** | Form (defensive) | — | Instant / — | Tanky form (Rage, +stam/armor); emergency personal mitigation. |
| **Moonkin Form** | Form (caster damage) | — | Instant / — | Balance caster form for stronger downtime DPS. |
| **Prowl** | Utility (stealth) | — | Instant / — | Cat-Form stealth. |
| **Frenzied Regeneration** | Defensive (self-heal) | Rage | Instant / ~36s (charges) | Bear-Form self-heal over 3s. Personal survivability while bear-weaving. |
| **Omen of Clarity (Clearcasting)** | Passive (proc) | — | — | Periodic-heal-driven proc that makes the next Regrowth free. Fuels the Regrowth spot-heal loop. |
| **Abundance** | Passive | — | — | Each active Rejuvenation lowers Regrowth cost 8% and adds 8% crit (to +96%). The reason to keep a wide Rejuv bed. |
| **Soul of the Forest** | Passive (proc) | — | — | After Swiftmend, next Rejuv/Wild Growth is empowered — the core Swiftmend payoff. |
| **Power of the Archdruid** | Passive (proc) | — | — | Swiftmend's *Soul of the Forest* Rejuv also copies to 2 nearby allies (+healing). |

### Name reconciliation notes

- **Efflorescence** (seed listed it as "Efflorescence?"): confirmed live —
  spell 145205 in the 12.0.7 spec tree (`talents.md`), name matches
  `SpellName.csv`. Not uncertain; drop the question mark.
- **Grove Guardians** (spell 1226140) is the Keeper-of-the-Grove passive that
  turns Swiftmend/Wild Growth into treant summons — not a hand-cast button.
- **Convoke the Spirits** / **Incarnation: Tree of Life** are a single
  choice node (33891 / 391528) — you take one, not both.
- No Midnight rename detected among the seed list; **Nourish**,
  **Cenarion Ward**, and **Adaptive Swarm** are *not* in the 12.0.7 resto
  tree — omitted from the build (Nourish kept only as an off-tree mana-filler
  note, @verify-ingame).

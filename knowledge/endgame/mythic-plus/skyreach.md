---
title: Skyreach — Midnight S1 M+ dungeon guide
patch: 12.0.7
fetched: 2026-06-25
reviewed: 2026-07-07
sources:
  - https://www.method.gg/guides/dungeons/skyreach
  - https://www.icy-veins.com/wow/skyreach-dungeon-guide
  - Blizzard journal-instance/476 + journal-encounter/965 (Ranjit) + journal-encounter/966 (Araknath) + journal-encounter/967 (Rukhran) + journal-encounter/968 (High Sage Viryx) (tier 1, boss-name corroboration)
  - https://www.youtube.com/watch?v=DMcpeEK_tHE  # Dalaran Gaming "How to Master All 8 Dungeons: Midnight S1 M+ Walkthrough", uploaded 2026-03-24 (tier 3, boss corroboration)
confidence: high
---

# Skyreach — Midnight Season 1 Mythic+

Arakkoa spire atop Sethekk Hollow. Four bosses, linear vertical climb. Three of
four bosses are **stationary** (Araknath, Rukhran, High Sage Viryx) so tanks must
hold melee range to suppress a punishing "no-one-in-melee" cast. Several edges to
get knocked / dragged off — positional awareness is the through-line of the whole
dungeon.

Boss names corroborated against Blizzard journal-encounters 965/966/967/968 — all
four guide names match the journal spelling exactly.

## Route

1. **Entrance → Ranjit approach.** Clear the wind-themed packs (Soaring Chakram
   Master, Outcast Warrior, Raging Squall, Driving Gale-Caller, Adorned Bladetalon,
   Dread Raven) on the lower terraces.
2. **Ranjit** (first boss) — wind/chakram fight on an exposed platform.
3. **Solarium approach → Araknath.** Solar-themed packs (Blinding Sun Priestess,
   Adept of the Dawn, Initiate of the Rising Sun, Solar Elemental, Solar Construct)
   before the construct boss.
4. **Araknath** (second boss) — stationary solar construct in the central solarium.
5. **Suntalon ramp → Rukhran.** Suntalon Tamer + Skyreach Sun Talon packs.
6. **Rukhran** (third boss) — stationary phoenix on a pillared platform.
7. **Final ascent → High Sage Viryx.** Note: Icy Veins flags **Adorned Bladetalon**
   as also appearing on the path here and being the single hardest-hitting trash mob
   for the tank in the dungeon (stacking Shear).
8. **High Sage Viryx** (final boss) — focusing-lens fight on the topmost platform,
   with an add that drags players off the edge.

## Trash

First-class. Mechanic word + consequence emoji + role. Claims appearing in **both**
Method and Icy Veins are high-confidence; single-sourced claims are flagged
`confidence: low`.

### Ranjit packs

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Driving Gale-Caller** | **Repel** | Mass knockback cast → **Interrupt every cast** | interruptible-cast | 🔵 | all |
| **Dread Raven** | **Dread Wind** | Targets a random player near an edge → watch your position so you aren't knocked off the platform | knockback | 🟠 | all |
| **Dread Raven** | **Dire Screech** | Heavy group damage → pre-top group; use group defensives | raid-damage | 🔵 | healer |
| **Raging Squall** | **Wrathful Wind** | Enrage → soothe it off if you can; use a defensive | purge-soothe | 🔵 | all |
| **Raging Squall** | **Wind Blast** | AoE dropped on death → move out of the lingering AoE | ground-void-zone | 🟠 | all |
| **Adorned Bladetalon** | **Blade Rush** | Dashes to 2 random players + tank (bleed), immune to CC → bleed-cleanse if able, else defensive + healing CDs | charge; dispel | 🟠 | all |
| **Adorned Bladetalon** | **Shear** | Stacking tank debuff (Icy Veins: hardest-hitting tank mob in dungeon) → tank uses CDs, watch overlap with Blade Rush | tank-buster | 🟠 | tank |
| **Soaring Chakram Master** | **Ricocheting Chakram** | Bounces between nearby players → spread slightly to limit bounce damage _(Method-only)_ | spread-out | 🔵 | all |
| **Outcast Warrior** | **Rushing Winds** | Self-buff → purge it off if possible _(Method-only)_ | purge-soothe | ⚪ | all |

### Araknath packs

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Blinding Sun Priestess** | **Blinding Light** | Casts it → **Interrupt every cast** | interruptible-cast | 🔵 | all |
| **Initiate of the Rising Sun** | **Solar Bolt** | Cast at a random player → use spare interrupts on it | interruptible-cast | 🔵 | all |
| **Solar Elemental** | **Solar Orb** | Spawns a Solar Orb add, immune to CC → swap and kill the orb ASAP | kill-priority-add | 🟠 | all |
| **Solar Elemental** | **Solar Fire** | Circles on the ground → avoid the circles | ground-void-zone | 🟠 | all |
| **Solar Construct** | **Solar Flame** | Targets you, immune to CC → defensive or combat-drop (Vanish/Feign) if targeted | fixate-chase | 🟠 | all |
| **Solar Construct** | **Solar Nova** | AoE underneath the mob → get out from under it | ground-void-zone | 🟠 | all |
| **Adept of the Dawn** | **Fiery Talon** | Melee stacks the debuff → defensive or kite to drop stacks | tank-buster | 🟠 | all |
| **Blinding Sun Priestess** | **Solar Barrier** | Buffs a random ally → purge it / focus the mob to stop the damage _(Method-only)_ | purge-soothe | 🔵 | all |

### Rukhran packs

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Suntalon Tamer** | **Mark of Death** | Makes nearby Suntalons **Bloodcrazed** → CC the Tamer during the cast; kite if you get the debuff | interruptible-cast | 🟠 | all |
| **Skyreach Sun Talon** | **Bloodcrazed** | Becomes enraged → lock down with CC/stuns while bloodcrazed | purge-soothe | 🟠 | all |

## Bosses

Consequence tiers: 🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor.

### Ranjit <!-- enc:965 -->

**Hint:** dodge the returning chakram

Wind / chakram fight on an exposed platform — most deaths are positional (knocked
into orbs or off the edge).

| Ability | What it does | Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Gale Surge** | Targets a player, moderate damage + knockback; spawns a persistent **Coalesced Wind** orb where you land | Pre-position before each cast so the knockback sends you somewhere safe; drop the wind orb (Coalesced Wind) at the edge or out of the group's path, and never walk through existing orbs left behind | knockback | 🟠 | all |
| **Fan of Blades** | Group-wide bleed, moderate damage to all | Healing CDs / bleed-cleanse on cast | raid-damage; dispel | 🔵 | healer |
| **Wind Chakram** | Fires a projectile at a random player that **returns** to the boss (Method/Icy Veins: can one-shot) | Avoid the projectile both ways; tank moves boss so the return doesn't clip melee | frontal-cone | 🔴 | all |
| **Chakram Vortex** | Spawns tornadoes that move/rotate across the arena | Dodge the tornadoes — often overlaps Wind Chakram/Gale Surge | ground-void-zone | 🟠 | all |

### Araknath <!-- enc:966 -->

**Hint:** soak the energize beams

Stationary solar construct. Core loop: intercept the **Energize** beams feeding the
boss so it doesn't reach full energy and blow up the group.

| Ability | What it does | Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Energize** | Lesser Constructs channel beams (in sets of 3) toward the boss, healing/charging it via **Solar Infusion** stacks | Non-tanks stand in the beam paths to **soak/block** them (you take damage — use defensives, healer spot-heals soakers) | soak | 🔴 | all |
| **Heat Exhaustion** | After ~12s Energize ends, a frontal goes out | Everyone avoid it; step into the AoE under the boss if needed | frontal-cone | 🟠 | all |
| **Supernova** | Full-energy nuke to all players; **hits harder if any Energize beams reached the boss** | Pre-top + group defensives, especially if beams leaked | raid-damage | 🔴 | healer |
| **Fiery Smash** | Tank frontal, left or right arm | Tank points it away from beam-soakers and steps out of it | frontal-cone | 🟠 | tank |
| **Defensive Protocol** | 5yd AoE created underneath the boss | All players avoid the puddle under the boss | ground-void-zone | 🟠 | all |
| **Blast Wave** | Cast if the tank is **not in melee range** | Tank stays in melee at all times to suppress it | positional-gimmick | 🔵 | tank |

### Rukhran <!-- enc:967 -->

**Hint:** break los on quills

Stationary phoenix. Adds (**Sunwing**) fixate and pulse group damage; bodies become
**Smoldering Eggs** that re-hatch if another add dies on top of them.

| Ability | What it does | Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Sunbreak** | Spawns a **Sunwing** add | Stack near the boss so it spawns where you can cleave it; kill it fast | kill-priority-add | 🟠 | all |
| **Burning Pursuit** | Sunwing fixates a random player and pulses heavy group damage while alive | CC/kite the fixate; healer spot-heals the target; kill the add | fixate-chase; raid-damage | 🟠 | all |
| **Smoldering Egg** | Dead Sunwings leave an egg; a new Sunwing dying on top **re-hatches** it | Don't kill Sunwings on top of eggs | positional-gimmick | 🔴 | all |
| **Searing Quills** | Heavy fire damage to everyone in **line of sight** across the platform | Break LoS behind the central pillar; tank returns to boss right after | positional-gimmick | 🔴 | all |
| **Burning Claws** | Heavy fire tank hit | Active mitigation / defensive every cast | tank-buster | 🟠 | tank |
| **Screech** | Cast if **no one is in melee range** for too long | Tank stays in melee except during Searing Quills LoS | positional-gimmick | 🔵 | tank |

### High Sage Viryx <!-- enc:968 -->

**Hint:** stun the off-edge add

Final boss, focusing-lens fight on the top platform with an edge. The **Cast Down**
add will throw a player off Skyreach if not stopped.

| Ability | What it does | Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| **Cast Down** | Summons a **Solar Zealot** that grabs a random player and drags them **off the edge** | Targeted player runs toward the entrance (don't hug the wall) to buy distance; everyone swaps + stuns the add; tank cleaves it by the boss | kill-priority-add | 🔴 | all |
| **Lens Flare** | Focuses a player and burns anything in the beam's path, leaving a lingering **Blazing Ground** fire trail | Run to the sides with movement CDs when targeted; trail the fire away from the group and place it at the arena edge — then avoid the Blazing Ground fire trail you laid down | ground-void-zone | 🟠 | all |
| **Scorching Ray** | DoT on 3 players at a time | Defensive if hit repeatedly; healer watches the 3 targets | raid-damage | 🔵 | healer |
| **Solar Blast** (a.k.a. Solar Burst) | Significant Fire tank hit, interruptible | Keep an **interrupt rotation** on it to cut tank damage | interruptible-cast; tank-buster | 🔵 | all |

## DPS notes (you are DPS)

- **Interrupt discipline is the whole dungeon.** Hard kicks: Driving Gale-Caller
  (Repel), Blinding Sun Priestess (Blinding Light), Initiate (Solar Bolt) on trash;
  Solar Blast on Viryx. Hold a kick where possible.
- **Kill-priority swaps:** Solar Orb (Solar Elemental), Sunwing (Rukhran), Solar
  Zealot (Viryx's Cast Down). Stop everything and burst these — Cast Down especially,
  the add has a large HP pool and a player goes off the edge if it lives.
- **Araknath:** soaking Energize beams is a DPS/healer job — eat the beams, pop a
  defensive, keep boss uptime between soaks.
- **Edges everywhere:** Ranjit Gale Surge knockback, Dread Raven Dread Wind, Viryx
  Cast Down. Know where the platform edge is before each pull.

---
title: Nexus-Point Xenas — Midnight S1 M+ dungeon guide
patch: 12.0.5
fetched: 2026-06-24
sources:
  - https://www.method.gg/guides/dungeons/nexus-point-xenas  # upd. 2026-03-23
  - https://www.icy-veins.com/wow/nexus-point-xenas-dungeon-guide  # upd. 2026-06-15, Patch 12.0.7
  - Blizzard journal-instance/1316 + journal-encounter/2813,2814,2815 (tier 1, boss-name corroboration)
  - https://www.youtube.com/watch?v=DMcpeEK_tHE  # Dalaran Gaming "How to Master All 8 Dungeons: Midnight S1 M+ Walkthrough", uploaded 2026-03-24 (tier 3, boss corroboration)
confidence: high
---

# Nexus-Point Xenas — Midnight S1 M+ dungeon guide

Player is **DPS**. Three bosses: **Chief Corewright Kasreth** (ethereals),
**Corewarden Nysarra** (void), **Lothraxion** (light). The dungeon is split
into 3 wings radiating from a central start room; you clear two side wings
(in either order), then the north light wing opens for the final boss.

## Route

1. **Start room** — forces from all 3 wings fight each other here; mixed
   ethereal / void / light trash (Shadowguard Defender, Lingering Image,
   Corewright Arcanist, Hollowsoul Scrounger).
2. **West (ethereal) wing → Chief Corewright Kasreth.** Environmental
   objects: Arcane Tripwires (5s stun, rogue/Engineering 25 can disarm),
   Broken Pipes, Mana Batteries, Corespark Conduits (soak for a high-DoT
   damage buff). Kill Kasreth.
3. **Conduit** at the end of the ethereal wing teleports you back to start.
4. **East (void) wing → Corewarden Nysarra.** Kill her, take that wing's
   conduit back to start.
5. **Activate the central console** (now interactable) to form the **bridge
   north** to Lothraxion's platform.
6. **North (light) wing → Lothraxion.** Light trash including the Lingering
   Images from the start room. Kill Lothraxion.

MDT PUG route (Method): https://wago.io/sX3WNXcg5

## Trash

Notable packs. Claims appearing in **both** Method and Icy Veins are
confidence high; single-sourced claims are flagged `(single-source)`.

### Start room (mixed)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Shadowguard Defender | **Null Sunder** | Tank's stacks climbing → tank uses self-heals / health pots / defensives to clear absorb if stacks get high | heal-absorb | 🔵 | tank |
| Lingering Image | **Searing Rend** | Cast on tank, leaves puddles → tank defensive + move out of the puddles (immune to CC) | tank-buster | 🟠 | tank |
| Lingering Image | **Luciferin Flare** | Frontal cone → face the mob away from group, step out of the frontal _(single-source: Method)_ | frontal-cone | 🔵 | all |
| Lingering Image | **Blistering Smite** | Random-target damage → extra healing / defensive on the target _(single-source: Method)_ | raid-damage | 🔵 | healer |
| Corewright Arcanist | **Arcane Explosion** | Interruptible channel → interrupt or CC it _(single-source: Method)_ | interruptible-cast | 🔴 | all |
| Corewright Arcanist | **Transference** | Magic debuff that heals the mob → dispel ASAP _(single-source: Method)_ | dispel | 🔵 | healer |
| Hollowsoul Scrounger | **Leech Veil** | At 45% HP jumps to an ally and channels a shield → CC to stop it; cleave them down _(single-source: Method)_ | interruptible-cast | 🔵 | all |

### Ethereal wing (before Kasreth)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Flux Engineer | **Suppression Field** | Random-target ground debuff; more movement = more damage taken → pre-spread so you don't cleave allies; if targeted, move as little as possible. On death drops an active **Mana Battery** — swap and destroy it before its explosion cast finishes | spread-out | 🟠 | all |
| Flux Engineer | **Mana Battery (Corespark Overload)** | The active battery dropped on Flux Engineer death casts an explosion → swap and destroy it before the cast finishes | kill-priority-add | 🔴 | all |
| Nexus Adept | **Umbral Bolt** | Random-target interruptible cast → use spare interrupts _(single-source: Method; Icy Veins lists it as "Umbra Bolt" on Nexus Adept — same cast)_ | interruptible-cast | 🔵 | all |
| Circuit Seer | **Arcing Mana** | Channel applying a group-wide stacking debuff, heavy damage → pop defensives / healing CDs (immune to CC) | raid-damage | 🔴 | all |
| Circuit Seer | **Erratic Zap / Power Flux** | Ground circles / puddles → sidestep them, move off puddles (Icy Veins: "Erratic Surge") | ground-void-zone | 🔵 | all |
| Circuit Seer | **Circuit Sense** | Activates nearby Mana Batteries (Corespark Overload) → focus the seer first; if a battery activates, swap and destroy it | kill-priority-add | 🟠 | all |

### Void wing (before Nysarra)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Reformed Voidling | **Smudge → Nascent Dreadflail** | On death becomes a Smudge that tries to wake a Nascent Dreadflail → CC / cleave the Smudge down fast _(single-source: Method)_ | kill-priority-add | 🔵 | all |
| Cursed Voidcaller | **Creeping Void** | On death casts a Curse-type debuff + burst → self-dispel / Curse dispel if able; expect the hit | dispel | 🔵 | all |
| Duskfright Herald | **Dark Beckoning** | Pulsing damage + projectiles (Icy Veins calls it a lethal frontal) → avoid the frontal / dodge projectiles (immune to CC) | frontal-cone | 🟠 | all |
| Duskfright Herald | **Entropic Leech** | Channel into a random player applying a healing absorb → combat-drop or clear the absorb to stop it _(single-source: Method)_ | heal-absorb | 🔵 | all |
| Grand Nullifier | **Nullify** | Interruptible cast → interrupt **every** cast | interruptible-cast | 🔴 | all |
| Grand Nullifier | **Dusk Frights** | Ground fear zones → avoid the fear puddles (Icy Veins also notes "Void Ritual" ground puddles to sidestep). On death also drops a Smudge (see Reformed Voidling) | ground-void-zone | 🟠 | all |
| Dreadflail | **Void Lash** | Frontal that cleaves; can kill in the wrong melee spot → tank faces it away from group + defensive (immune to CC) | frontal-cone | 🟠 | tank |
| Dreadflail | **Flailstorm** | Fixate + AoE → if fixated, kite / out-range it | fixate-chase | 🟠 | all |
| Null Sentinel | **Dreadbellow** | Knockback + AoE DoT → watch positioning for the knockback; healers handle the DoT _(single-source: Method)_ | knockback | 🔵 | all |
| Null Sentinel | **Nullwark Blast** | Tank-targeted hit + DoT → tank defensive _(single-source: Method)_ | tank-buster | 🔵 | tank |

### Light wing (before Lothraxion)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Radiant Swarm | **Fixate** | Fixates a random player → kite / CC if targeted. Takes extra AoE damage (Cluster Weakness) | fixate-chase | 🟠 | all |
| Flarebat | **Holy Echo** | Corpse-explodes into an AoE damage + healing zone on death → purge the Holy Echo buff if able, else out-range the explosion | purge-soothe | 🟠 | all |
| Lightwrought | **Holy Bolt** | Random-target interruptible cast → keep it interrupted | interruptible-cast | 🔵 | all |
| Lightwrought | **Burning Radiance** | Magic debuff on 2 players → dispel one ASAP, defensive/heal the other _(single-source: Method)_ | dispel | 🟠 | all |

## Bosses

### Chief Corewright Kasreth (journal-encounter 2813)

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| **Leyline Array** | Beams link between conduits across the room; lethal to cross | Don't cross active beams; **if you have Reflux Charge**, stand in intersections to break as many beams as possible | `positional-gimmick` | 🔴 |
| **Reflux Charge** | Debuff that ticks damage; used to disable Leyline Array beams | When debuffed, walk through beam intersections to disable them | `positional-gimmick` | 🔵 |
| **Corespark Detonation** | At 100 energy boss overcharges a corespark; impact does damage + knockback + healing absorb (Sparkburn) | Outrange the impact; bait toward room edges; healers pre-plan CDs for the party-wide Sparkburn absorb; mind the knockback | `proximity-bait` | 🟠 |
| **Flux Collapse** | Continuous arcane flow toward a player, leaving puddles (Arcane Spill) | Bait puddles to edges; sidestep them | `ground-void-zone` | 🔵 |
| **Arcane Zap** | Boss has no melee; instead instant-cast arcane hit on tank (Icy Veins lists an interruptible Arcane Zap) | Tank expects arcane melee damage; interrupt where applicable | `tank-buster` | 🔵 |

### Corewarden Nysarra (journal-encounter 2814)

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| **Eclipsing Step** | Boss carves into 2 targeted players plus nearby; applies a DoT | Spread so you don't cleave allies; defensive for the hit + DoT | `spread-out` | 🟠 |
| **Null Vanguard** | Spawns a Dreadflail + 2 Grand Nullifiers | Interrupt every Nullify; tank points Dreadflail away when it gains Void Lash; **kill all adds before the Lightscar phase** | `kill-priority-add` | 🔴 |
| **Umbral Lash** | Tank channel that cleaves nearby + applies Void Gash | Tank major defensive, especially if adds are up | `tank-buster` | 🟠 |
| **Lightscar Flare** | A Lothraxion image aims a flare at the boss; creates a Holy frontal that ticks heavy damage but amps boss damage +300% | Dodge the initial flare, then stand in the frontal to burst (300% amp); healers heal the ticking; ensure adds are dead first | `soak` | 🔵 |
| **Devour the Unworthy** | If adds live to the end of the Lightscar channel, boss consumes them (empower) | Make sure all adds are dead before the channel ends | `kill-priority-add` | 🔴 |

### Lothraxion (journal-encounter 2815)

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| **Searing Rend** | Tank buster, heavy Physical, leaves Radiant Scar puddles that persist all fight | Tank defensive; drop puddles out of the way | `tank-buster` | 🟠 |
| **Brilliant Dispersion** | Targets 3 players; damages all nearby at the destination + a hard-hitting DoT; spawns 2 Fractured Images each | Spread to avoid cleaving; defensive for the DoT; healers use CDs each cast | `spread-out` | 🟠 |
| **Mirrored Rend** | Fractured Images strike anyone within ~5 yds | Stay >5 yds from images | `ground-void-zone` | 🔵 |
| **Flicker** | Image dashes/repositions, hitting anyone in its path | Avoid the dash path | `charge` | 🔵 |
| **Divine Guile** | At full energy boss hides among images; find the copy **without** horns of light and interrupt it | Interrupt the hornless copy to resume; **never** interrupt an image | `interruptible-cast` | 🔴 |
| **Core Exposure** | Triggered by failing Divine Guile (interrupting wrong copy / not interrupting) | Avoid by interrupting the correct copy | `ground-void-zone` | 🔴 |

## DPS notes

- **Corespark Conduits** in the ethereal wing give a damage buff (Corespark
  Surge) but with a high DoT — only soak if your healer can cover it.
- **Kasreth:** if you have **Reflux Charge** as a melee, the tank may park the
  boss near a Leyline Array so you keep uptime while breaking beams.
- **Nysarra Lightscar phase** is the burst window: hold offensive CDs for the
  +300% amp, but only after all Null Vanguard adds are dead (else Devour).
- **Lothraxion Divine Guile** is the wipe check: identify the hornless boss
  copy and interrupt only that one. Bring an extra interrupt for it.

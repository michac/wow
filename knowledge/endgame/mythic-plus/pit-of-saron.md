---
title: Pit of Saron — Midnight S1 M+ dungeon guide
patch: 12.0.5
fetched: 2026-06-24
sources:
  - https://www.method.gg/guides/dungeons/pit-of-saron        # upd. 2026-03-23
  - https://www.icy-veins.com/wow/pit-of-saron-dungeon-guide    # upd. 2026-06-15 (12.0.7)
  - Blizzard journal-instance/278 + journal-encounter/608 + /609 + /610 (tier 1, boss-name corroboration)
  - https://www.youtube.com/watch?v=DMcpeEK_tHE  # Dalaran Gaming "How to Master All 8 Dungeons: Midnight S1 M+ Walkthrough", uploaded 2026-03-24 (tier 3, boss corroboration)
confidence: high
---

# Pit of Saron — Midnight S1 M+ dungeon guide

Wrath-era ICC-adjacent dungeon, brought into Midnight Season 1 M+. Three
bosses: **Forgemaster Garfrost**, **Ick and Krick**, **Scourgelord
Tyrannus** (journal names confirmed against journal-instance 278). Frost
/ Scourge / plague themed throughout.

## Route

The opening is an open quarry; the back half is an ice cave up to the
final boss.

1. **Quarry (open area).** Start point. You may go **left toward Ick and
   Krick** or **right toward Forgemaster Garfrost** — both directions
   share the same trash pool, just in different compositions. Method
   recommends pathing **right toward Garfrost** first.
2. **Liberate the 6 Quarry Camps.** Spread throughout the quarry — you
   **must free all 6** to open the path to the final boss. Path past them
   while clearing trash on whichever side you took.
3. **Forgemaster Garfrost** — boss 1 (on the Garfrost side).
4. **Ick and Krick** — boss 2 (on the opposite side). Both bosses + all 6
   camps must be done before the final approach.
5. **Up the hill, through the ice cave** toward Tyrannus — familiar quarry
   mobs plus the **Glacieth** mini-boss.
6. **Scourgelord Tyrannus** — boss 3, at the entrance to the Halls of
   Reflection.

**MDT route (PUG-friendly):** https://wago.io/ychDjUfcX

## Trash

Both guides agree on the quarry pool. Single-sourced claims flagged
`confidence: low`.

### Quarry packs (shared on both paths)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Quarry Tormentor | **Curse of Torment** | Random target gains a shadow curse/absorb → **decurse it**, or heal off the absorb to remove it. Its melee also deals bonus shadow damage to the tank while the tank is above 65% HP | dispel | 🔵 | healer |
| Gloombound Shadebringer | **Shadow Bolt** | Cast on a random player → **interrupt** the cast (spare interrupts) | interruptible-cast | 🔵 | DPS |
| Dreadpulse Lich | **Icy Blast** | Tank-targeted, hits extremely hard → **interrupt every cast** (IMPORTANT MOB, immune to CC) | interruptible-cast | 🟠 | all (kick) |
| Dreadpulse Lich | **Torrent of Misery** | Random-target channel, heavy → pre-defensive + focus-heal the target; you can drop combat (Feign Death / Vanish) to cancel it | raid-damage | 🟠 | healer |
| Dreadpulse Lich | **Dread Pulse** | At **50% HP** begins pulsing every ~2s until it dies → group defensives / healing CDs | pulsing-aura | 🟠 | all |
| Ymirjar Graveblade | **Frostbane Slash** | Tank-targeted heavy hit → tank defensive (immune to CC) | tank-buster | 🔵 | tank |
| Ymirjar Graveblade | **Dark Rupture** | Ground circles → **avoid the puddles** | ground-void-zone | 🟠 | all |
| Iceborn Proto-Drake | **Frost Breath** | Random-target frontal cone → **move out of the cone** (immune to CC) | frontal-cone | 🟠 | all |
| Iceborn Proto-Drake | **Icy Strikes** | Melees deal bonus frost to the tank (passive) _(Method-only)_ | flavor | ⚪ | tank |
| Plungetalon (Gargoyle) | **Plungegrip** | Abduction grab → break its **Stoneskin** shield to enable the interrupt, then interrupt Plungegrip (or drop combat with Vanish / Feign Death). (Method lists it as "Plungetalon", Icy Veins "Plungetalon Gargoyle") | interruptible-cast | 🟠 | all (kick) |
| Wrathbone Enforcer | **Sunderstrike** | Melee may apply Sunderstrike stacks → tank watches stacks, uses defensives _(Method-only)_ | tank-buster | 🔵 | tank |
| Rotting Ghoul | **Rotting Strikes** | Melee applies disease stacks → tank dispels disease or kites if no dispel _(Method-only)_ | dispel | 🔵 | tank |
| Leaping Geist | **Leaping Maul** | Cleave attack → loosely spread so it doesn't cleave allies _(Method-only)_ | spread-out | 🔵 | all |
| Deathwhisper Necrolyte | **Deathless Bond** | Makes its minions immune until it dies → **kill-priority** the Necrolyte first _(Method-only)_ | kill-priority-add | 🟠 | DPS |
| Deathwhisper Necrolyte | **Necromantic Infusion** | Buffs a random minion → purge if able _(Method-only)_ | kill-priority-add | 🟠 | DPS |
| Risen Soldier | **Charging Slash** | Random-target charge + physical hit → be ready for it _(Method-only)_ | charge | ⚪ | all |
| Arcanist Cadaver | **Netherburst** | Large AoE hit → **interrupt every cast** _(Method-only)_ | interruptible-cast | 🔴 | all (kick) |
| Lumbering Plaguehorror | **Blight Splatter** | Drops puddles → avoid them _(Method-only)_ | purge-soothe | 🟠 | all |
| Lumbering Plaguehorror | **Plague Frenzy** | Enrage → **soothe** it off if possible _(Method-only)_ | purge-soothe | 🟠 | DPS |
| Rimebone Coldwraith | **Icebolt** | Random-target → spare interrupts _(Method-only)_ | dispel | 🔵 | all (kick) |
| Rimebone Coldwraith | **Permeating Cold** | Debuffs 2 random players → **magic dispel** / freedom to remove _(Method-only)_ | dispel | 🔵 | healer |

### Tyrannus approach (ice cave)

| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| Glacieth (mini-boss) | **Cryoburst** | Hits all players, drops icy ground (**Cryopatch**) → loosely spread to avoid cleaving each other, then move the group out of the puddles (immune to CC) | spread-out | 🟠 | all |
| Glacieth (mini-boss) | **Focused Guard** | Channel aimed at a random player; attacking the shielded front = **99% reduced damage** → **attack from behind** the mob (guaranteed crits while behind it during the channel) | positional-gimmick | 🔵 | DPS |

## Bosses

### Forgemaster Garfrost <!-- enc:608 -->

Single tank-and-position fight. Garfrost throws saronite ore that becomes
cover; at 100 energy he channels **Glacial Overload** from his closest
forge — you hide behind ore to survive it.

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| Throw Saronite | Targets 2 players; the **Ore Chunks** that drop leave a puddle (Saronite Sludge) when destroyed, and become cover vs Glacial Overload | Don't cleave allies; don't overlap your circles; place chunks deliberately as cover | ground-void-zone | 🔵 |
| Orebreaker | Tank-targeted hit; **stuns** unless it strikes an Ore Chunk | Tank overlaps an Ore Chunk so the hit breaks the chunk instead of stunning you; pre-defensive | tank-buster | 🔵 |
| Glacial Overload | At 100 energy, channels frost from the closest forge into the room | **Hide behind a remaining Ore Chunk**; >3 stacks of the chill will likely kill you | positional-gimmick | 🔴 |
| Cryostomp | Follows Glacial Overload; destroys remaining chunk, group-wide damage, applies **Cryoshards** magic debuff to 2 players | Group defensives; **dispel Cryoshards ASAP** (freedom helps) | dispel | 🟠 |
| Siphoning Chill | Passive chill aura running the whole fight; Cryostomp increases its danger | Sustained healing throughline — bring strong healing talents | pulsing-aura | 🔵 |

### Ick and Krick <!-- enc:609 -->

Two bodies that **share health via Necrolink** — cleave both. Krick rides
Ick; Ick is the bruiser, Krick the caster, plus Shade adds.

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| Necrolink | Ick and Krick **share a health pool** | Position both together and **cleave** constantly | positional-gimmick | 🔵 |
| Death Bolt | Krick casts on random players | **Interrupt** — this is the priority interrupt | interruptible-cast | 🟠 |
| Shade Shift | Spawns 2 **Shades of Krick** nearby | **Kill-priority** the shades (they explode if left up); cleave them | kill-priority-add | 🟠 |
| Shadowbind | Shades channel on a random player (a **Curse**) | Interrupt, or **decurse** / freedom / drop-combat to break it | interruptible-cast | 🔵 |
| Blight Smash | Ick's heavy tank hit; drops a **Blight** ground ichor | Tank major defensive; **drop the puddle out of the way** | tank-buster | 🟠 |
| Plague Expulsion / Plague Globs | Puddles spawn under ~4 random players | Pre-spread, sidestep the globs, stay off the **Blight** ground | spread-out | 🟠 |
| Get 'Em, Ick! (Lumbering Fixation) | At 100 energy Krick mounts Ick, who **fixates** a random player ~7s at a time over ~28s | **Kite** Ick if fixated; others save burst for cleave; stay away from boss to avoid melee | fixate-chase | 🟠 |
| Shadow Lance | Krick cast, spike damage | Spot-heal target | raid-damage | 🔵 |

### Scourgelord Tyrannus <!-- enc:610 -->

Death knight + frost wyrm **Rimefang** (airborne). Build-up phase with
brands and ground zones, then **Army of the Dead** at 100 energy raises
the **Bone Piles** into adds. Pre-freeze the piles to trivialize it.

| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
| Rime Blast | Rimefang debuffs targeted players; freezes any **Bone Piles** it impacts | Drop the debuff **on top of the Bone Piles / Infused Bone Piles** to pre-freeze them for the Army phase | spread-out | 🔵 |
| Bone Infusion | Empowers some Bone Piles into **Infused** ones; group damage on cast | Healer CDs / personal defensives on the cast | raid-damage | 🟠 |
| Army of the Dead | At 100 energy the 5 Bone Piles animate: normal → **Rotlings**, infused → **Scourge Plaguespreaders** | Cleave adds down; Rotlings stack **Rotting Strikes** disease on tank (dispel) — **Plaguespreaders are kill-priority** | kill-priority-add | 🔴 |
| Plague Bolt (Plaguespreader) | Scourge Plaguespreader random-target cast; **Festering Pulse** is a heavy group-damage passive | **Swap to Plaguespreaders ASAP** and keep an **interrupt rotation** on Plague Bolt | interruptible-cast | 🟠 |
| Scourgelord's Brand | Tank-targeted **knockback**, then a leap attack (**Scourgelord's Reckoning**) at the tank's new spot | Tank major defensive + move to dodge the second hit | knockback | 🟠 |
| Death's Grasp | Ground circles | **Sidestep** the puddles | ground-void-zone | 🔵 |
| Ice Barrage | Rimefang channel during the Army phase, ground damage zones | **Avoid** being hit | ground-void-zone | 🔵 |
| Frost Spit | Rimefang spit, damage to players | Healer awareness | raid-damage | 🔵 |

## DPS notes (you are DPS)

- **Garfrost:** if you're a Throw Saronite target, place your Ore Chunk
  near the tank's pile so it's easy to break for Orebreaker; you do not
  want loose chunks scattering cover. Save burst — there's no priority
  add, it's a positioning fight.
- **Ick and Krick:** the only thing that matters for throughput is keeping
  **both bodies cleaved** (shared HP) and **killing Shades fast**. Hold an
  interrupt for Death Bolt. If Ick fixates you, kite and DPS over your
  shoulder.
- **Tyrannus:** the fight is won in the pre-phase — **dump Rime Blast on
  the Bone Piles** so they're frozen when Army of the Dead fires.
  Otherwise swap-and-interrupt **Scourge Plaguespreaders** the instant
  they spawn (Festering Pulse is what wipes pugs). Save AoE burst for the
  Army phase.

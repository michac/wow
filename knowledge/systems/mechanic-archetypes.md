---
title: M+ Mechanic Archetypes (Midnight S1)
patch: 12.0.5
fetched: 2026-06-24
sources:
  - Derived from the 8 Midnight S1 M+ dungeon files in knowledge/endgame/mythic-plus/ (boss + trash corpus)
confidence: high
---

# M+ Mechanic Archetypes (Midnight S1)

This taxonomy is **derived empirically from the real boss + trash ability
corpus of all 8 Season 1 dungeons** (Magisters' Terrace, Maisara Caverns,
Nexus-Point Xenas, Windrunner Spire, Algeth'ar Academy, Seat of the
Triumvirate, Skyreach, Pit of Saron) — 380 abilities pooled, every one
mapped to exactly one archetype. **Trash abilities are first-class** here:
roughly two-thirds of the corpus comes from trash, and the same alphabet
covers bosses and trash alike. Nothing was invented that the dungeons don't
use; nothing they use was dropped.

These 21 slugs are **canonical** for the tagging stage. The trainer's
Archetype mode reads them. Each ability maps to a **primary** slug, plus
zero-or-more **also-valid** slugs when one tell genuinely demands two responses
(see Tagging rule 3).

Consequence legend: 🔴 wipe · 🟠 your death · 🔵 your job · ⚪ flavor.

## Tagging rules (read before assigning a slug)

**One in-game tell → one card.** The learner drills *reactions to tells*, not
journal rows. Two corollaries the classifier must enforce:

1. **Cast + lingering-effect de-duplication.** When a *cast* creates a lingering
   zone/DoT/pool that the source guide or journal lists as a **separate**
   ability (e.g. a cast and the puddle it drops), treat the two as **one
   mechanic, one card**. Default: keep the **cast** card and fold the zone's
   "don't stand in it" response into the cast card's reveal — do **not** mint a
   second card for the puddle. Exception: if the lingering zone (not the cast)
   is the thing the player actually reacts to, make the **zone** the card and
   treat the cast as its tell. Never two cards for one tell.

2. **Classify by response, not by surface words.** Tag what the player *does*,
   not what the ability text *says*. A "stack"ing DoT is not `stack-up`; a
   "void" puddle owner is not automatically `ground-void-zone`. Read the
   per-slug **Not this if** guards below before pattern-matching a keyword.

3. **A card may carry more than one valid archetype.** One tell → one card still
   holds — do **not** split an ability into two cards — but that single card can
   have a **primary** archetype (the response a player reacts to *first / most*,
   which drives the reveal + diagram) plus one or more **also-valid** archetypes
   when the same tell legitimately demands two distinct responses (e.g. a
   tank-buster that *also* knocks the tank back, or a knockback that is *also*
   unavoidable raid damage). The trainer accepts any of a card's valid
   archetypes as correct and never offers another valid one as a distractor.
   Discipline: a secondary archetype must be a response a competent player would
   **actually give** — not a loosely-related slug. Most abilities are
   single-archetype; reach for a secondary only when forcing one answer would
   mark a real response wrong. In the dungeon tables, write multi-tag cells as
   `primary; secondary` (primary first, semicolon-separated).

---

## `interruptible-cast`
**Interruptible Cast** — a mob/boss casts something with a kickable bar.
- **Tell:** a visible cast bar on a spell you can kick (Polymorph, a heal, a bolt, a summon).
- **Response:** interrupt it. Rotate kicks/stuns across the group; the worst casts (heals, summons, raidwide channels) come first.
- **Consequence:** 🔵 usually (one cast leaks) → 🔴 if it's a heal/summon/empower (e.g. Reanimation, Healing Touch, Arcing Mana).
- **Role:** all — every DPS/tank/healer with a kick. The non-negotiable group job.
- **Examples:** *Healing Touch* — Overgrown Ancient (Algeth'ar Academy); *Reanimation* — Reanimated Warrior trash (Maisara Caverns).
- **Diagram idea:** mob silhouette with a cast bar mid-fill and a red "X" kick icon snapping it shut.

## `ground-void-zone`
**Ground Void Zone** — a damaging puddle/patch you stand out of (and that often grows or shrinks the room).
- **Tell:** a colored circle, swirl, or spreading goo appears under or near you.
- **Response:** move out / don't stand in it. Drop boss-placed zones at the edge so you don't eat the arena.
- **Not this if:** the zone is a lingering pool *left by a cast that already has its own card* — per the cast+effect de-dup rule, fold "don't stand in it" into the cast's card instead of minting a second `ground-void-zone` card. Only tag the zone itself when the pool (not the cast) is the primary tell.
- **Consequence:** 🟠 standing in it kills you fast → 🔴 when zones stack and eat the floor (Leyline Array, Core Exposure).
- **Role:** all.
- **Examples:** *Flamestrike* — Blazing Pyromancer trash (Magisters' Terrace); *Coalesced Wind* — Ranjit (Skyreach).
- **Diagram idea:** top-down floor with a glowing puddle and a footstep arrow stepping clear of the edge.

## `tank-buster`
**Tank Buster** — a big melee hit, stacking shred, or bleed aimed at whoever holds threat.
- **Tell:** boss/elite winds up a heavy melee swing or applies a stacking armor/heal-absorb debuff on the tank.
- **Response:** tank presses an active mitigation cooldown; healer tops the tank; trade taunts if stacks get scary.
- **Consequence:** 🔵 mostly (mitigate it) → 🟠/🔴 unmitigated or with stacked shred/absorb (Hulking Fragment, Blight Smash).
- **Role:** tank (with healer support).
- **Examples:** *Orebreaker* — Forgemaster Garfrost (Pit of Saron); *Crunch Armor* (stacking shred) — Bramblemaw Bear trash (Maisara Caverns).
- **Diagram idea:** side view of a shield icon flashing "MIT" as a big fist lands on the tank.

## `spread-out`
**Spread Out** — damage/debuff that hits an area around its target, so clumping chains it.
- **Tell:** a marker on you (or several players) that will detonate, or spawns a patch where you stand.
- **Response:** spread to your assigned spacing before it lands; don't share your splash with melee.
- **Consequence:** 🔵→🟠 (you eat your own) → 🔴 if overlap chains the group (Runic Mark, Plague Expulsion).
- **Role:** all (healers/ranged especially watch spacing).
- **Examples:** *Runic Mark* — Seranel Sunlash (Magisters' Terrace); *Mana Bombs* — Vexamus (Algeth'ar Academy).
- **Diagram idea:** five dots fanning outward from a clumped cluster, arrows pushing apart.

## `dispel`
**Dispel** — a debuff on a player (or buff to remove) that someone must cleanse off.
- **Tell:** a harmful magic/curse/poison/disease icon on a player, a heal-absorb shield, or an offensive buff on a friendly-turned-add.
- **Response:** dispel the flagged target (or free the shackled ally). Know which school your class can remove.
- **Consequence:** 🔵 usually → 🟠/🔴 when the debuff is lethal or feeds the boss (Burning Radiance, Curse of Darkness).
- **Role:** all dispellers — frequently the **healer's** signature job, sometimes any class with a tradeable cleanse.
- **Examples:** *Ethereal Shackles* — Arcane Sentry trash (Magisters' Terrace); *Lasher Toxin* — Overgrown Ancient (Algeth'ar Academy).
- **Diagram idea:** a debuff icon over a player head with a green sparkle wiping it away.

## `kill-priority-add`
**Kill-Priority Add** — a spawned/secondary unit that must die (or be CC'd) before it does something bad.
- **Tell:** an add appears — a totem, a caster, an orb, a "Voidcaller" — usually with its own cast or a buff it feeds.
- **Response:** swap and burn it (or stun/interrupt) on the timer. Treat the add, not the boss, as the threat.
- **Consequence:** 🔵→🟠 (a single add leaks) → 🔴 when ignored adds empower or overwhelm (Mana Battery, Army of the Dead).
- **Role:** all — DPS swaps, tank grabs, everyone helps cleave.
- **Examples:** *Army of the Dead* — Scourgelord Tyrannus (Pit of Saron); *Mana Battery (Corespark Overload)* — Flux Engineer trash (Nexus-Point Xenas).
- **Diagram idea:** a small add glowing with a skull/priority marker while the boss is greyed out.

## `frontal-cone`
**Frontal Cone** — a directional sweep/breath/cleave in front of the caster.
- **Tell:** boss/mob faces a direction and winds up a cone, breath, or wide cleave (often a tank-facing arrow).
- **Response:** get out of the front; tank points it away from the group; melee sidestep behind.
- **Consequence:** 🟠 mostly → 🔵 when small/cleave → 🔴 on the big ones (Wind Chakram).
- **Role:** all (tank controls facing).
- **Examples:** *Fire Breath* — Emberdawn (Windrunner Spire); *Shield Slam* (frontal) — Runed Spellbreaker trash (Magisters' Terrace).
- **Diagram idea:** a wedge fanning from the mob's face with a player dodging to the flank.

## `knockback`
**Knockback** — a shove, pull, or repel that moves you (often toward a hazard or off a ledge).
- **Tell:** a slam/gale/vacuum wind-up, sometimes a pull-in or bouncing orbs.
- **Response:** position with your back safe before it fires; use anti-knockback if you have it; pre-stack against pulls.
- **Consequence:** 🟠 (knocked into the void/hazard) → 🔵 when harmless reposition → 🔴 on arena-ledge fights (Collapsing Void, Burning Gale).
- **Role:** all.
- **Examples:** *Burning Gale* — Emberdawn (Windrunner Spire); *Crowd Dispersal* — Arcane Sentry trash (Magisters' Terrace).
- **Diagram idea:** a player figure blown along a motion-arc toward a void edge, with a "brace" anchor icon.

## `soak`
**Soak** — a mechanic that demands bodies in it: stand in the orb/zone/beam to absorb or split it.
- **Tell:** an orb to grab, an energy bar refueling, a beam/bomb that needs N players, or a stabilize cast.
- **Response:** assign soakers and get in. The failure here is **under**-soaking, the opposite of a void zone.
- **Consequence:** 🔴 mostly — missed soaks wipe (Refueling Protocol, Wave of Silence, Overload, Energize).
- **Role:** all (often pre-assigned).
- **Examples:** *Refueling Protocol* / *Energy Orb* — Arcanotron Custos (Magisters' Terrace); *Stabilize* — Rift Warden trash (Seat of the Triumvirate).
- **Diagram idea:** glowing orb with two player figures stepping **into** it (green check), one staying out (red X).

## `raid-damage`
**Raid Damage** — unavoidable group-wide pulse/channel (and incidental single-target spikes the healer must catch).
- **Tell:** a raidwide cast, a screech/nova, a stacking room-wide DoT, or a sudden spike on one player.
- **Response:** pre-heal and use raid cooldowns on the channel; healer triages the spikes. Often paired with an interrupt window.
- **Consequence:** 🔵 (healable) → 🟠/🔴 when stacked or untended (Bone Infusion, Supernova, Burst Forth).
- **Role:** healer-led, all survive-through.
- **Examples:** *Supernova* — Araknath (Skyreach); *Spore Dispersal* — Bloated Lasher trash (Windrunner Spire).
- **Diagram idea:** the whole party ringed by an expanding shockwave with healer cooldown sparkles overhead.

## `stack-up`
**Stack Up** — damage/debuff that wants the group **physically together** to split or share it.
- **Tell:** a marker that splits damage by player count, a shared-soak debuff, a melee-stack cue, or a "fear if alone" / "hit if isolated" cast.
- **Response:** collapse to the stack point (or to an ally) on time — the inverse of spread-out. The defining feature is **players converging**.
- **Not this if:** there is **no converge-to-split / group-up response**. A *personal* stacking DoT or applied debuff you just heal/defensive through is `raid-damage` (or the parent mechanic). A "you missed a soak" / "you stood in it" stacking marker is the **consequence of another mechanic** — tag it as that parent (the `soak`, the `ground-void-zone`), not here. The word "stack" in the ability text is **not** the signal; players grouping up is.
- **Consequence:** 🟠 (solo-eaten / feared) → 🔴 when the whole group must share a single hit.
- **Role:** all.
- **Examples:** *Intimidating Shout* (fears players standing alone → stack near an ally) — The Restless Heart (Windrunner Spire); *Throw Spear* (stack inside its minimum range) — Keen Headhunter trash (Maisara Caverns).
- **Diagram idea:** scattered dots converging onto one bracketed stack marker.

## `fixate-chase`
**Fixate / Chase** — an enemy locks onto one player and pursues, ignoring threat.
- **Tell:** a mob (or boss) targets a non-tank and runs them down; sometimes a tornado/blades chase.
- **Response:** the fixated player kites with speed/CC until it drops; don't drag it through the group.
- **Consequence:** 🟠 mostly (caught = dead) → 🔵 on slow chases → 🔴 if it bodies the group (Bladestorm, Flailstorm).
- **Role:** all (whoever's tagged kites; tank can't taunt it off).
- **Examples:** *Burning Pursuit* — Rukhran (Skyreach); *Fixate* — Radiant Swarm trash (Nexus-Point Xenas).
- **Diagram idea:** a mob with an eye icon trailing a fleeing player along a kite path.

## `purge-soothe`
**Purge / Soothe** — an *enemy* buff or enrage you remove from the mob (not a player debuff).
- **Tell:** a mob gains haste/damage/enrage, a fortifying buff, or a frenzy you can soothe/dispel off it.
- **Response:** purge/soothe the buff off the enemy (or kill the buff source) before it snowballs.
- **Consequence:** 🔵 mostly → 🟠/🔴 on enrages and pet-cleave windows (Bestial Wrath, Plague Frenzy). *(The Derelict Duo's Broken Bond reads like an enrage but is **not** soothable — see `balance-kill`.)*
- **Role:** all with an enemy-dispel/soothe (hunters/druids/mages especially).
- **Examples:** *Bolstering Flames* — Territorial Dragonhawk trash (Windrunner Spire); *Plague Frenzy* (soothe) — Lumbering Plaguehorror trash (Pit of Saron).
- **Diagram idea:** an angry red buff icon over a mob being stripped to grey.

## `positional-gimmick`
**Positional Gimmick** — the mechanic is solved by *where* you stand: line-of-sight, reflect angle, or move-the-mob.
- **Tell:** a beam/quills cast you must LoS behind a pillar, a reflect-shield you must hit from a side, or an add you must reposition.
- **Response:** break line of sight, attack from the correct facing, or drag the mob to the marked spot.
- **Consequence:** 🔵→🔴 depending (Searing Quills / Glacial Overload are LoS-or-wipe).
- **Role:** all (tank often owns the repositioning).
- **Examples:** *Searing Quills* (line-of-sight) — Rukhran (Skyreach); *Vigilant Defense* (reflect, hit from behind) — Bound Defender trash (Maisara Caverns).
- **Diagram idea:** a pillar between player and boss-beam, with a dotted "blocked" sightline.

## `heal-absorb`
**Heal Absorb** — a shield/debuff that soaks incoming healing until it's burned off.
- **Tell:** a dark shield bar over a player's health; heals fill it instead of the health bar.
- **Response:** burn the absorb down (overheal or DPS the shield); don't waste cooldowns trying to out-heal a full absorb.
- **Consequence:** 🔵→🟠 (the player can't be healed until cleared, then dies to follow-up).
- **Role:** healer-critical (DPS may need to attack the shield).
- **Examples:** *Null Sunder* — Shadowguard Defender trash (Nexus-Point Xenas); *Entropic Leech* — Duskfright Herald trash (Nexus-Point Xenas).
- **Diagram idea:** a health bar with a black overlay shield, healing arrows bouncing off it.

## `charge`
**Charge** — a fast gap-closer the mob slams into a target's position.
- **Tell:** a mob breaks formation and rushes a player (intercept/charging slash/break ranks).
- **Response:** sidestep the line; tank picks it back up; don't let it land on the backline.
- **Consequence:** ⚪→🟠 (most are minor, the breakers hurt — Break Ranks).
- **Role:** all (tank re-grabs).
- **Examples:** *Break Ranks* — Phalanx Breaker trash (Windrunner Spire); *Intercepting Charge* — Haunting Grunt trash (Windrunner Spire).
- **Diagram idea:** a dashed charge line from mob to player with a sidestep arrow off it.

## `proximity-bait`
**Proximity Bait** — a mechanic baited by *closeness*: get near (or away) to place/trigger it correctly.
- **Tell:** a cast that targets the nearest player, or a root/zone dropped where someone is standing.
- **Response:** the designated baiter steps to the safe drop spot; everyone else stays clear of the trigger radius.
- **Consequence:** 🟠 (caught in the placement) — usually a death, not a wipe.
- **Role:** all (often one assigned baiter).
- **Examples:** *Rend Souls* (proximity bait) — Hollow Soulrender trash (Maisara Caverns); *Cries of the Fallen* (proximity bait root) — Rak'tul, Vessel of Souls (Maisara Caverns).
- **Diagram idea:** a player stepping to a marked drop-spot with a radius ring pulling the cast toward them.

## `pulsing-aura`
**Pulsing Aura** — a persistent, location-less damage/chill aura that just ticks while you're near the source.
- **Tell:** no dodgeable shape — a stacking chill/dread debuff that ramps the longer the pack lives.
- **Response:** burn the source fast; healer rides the ramp; spread if the aura also debuffs proximity.
- **Consequence:** 🔵→🟠 (it ramps — kill the caster before it overwhelms).
- **Role:** healer-watched, DPS race.
- **Examples:** *Siphoning Chill* — Forgemaster Garfrost (Pit of Saron); *Dread Pulse* — Dreadpulse Lich trash (Pit of Saron).
- **Diagram idea:** a mob radiating concentric faint rings with a rising debuff-stack counter.

## `burn-window`
**Burn Window** — a phase where the boss becomes vulnerable and you dump damage cooldowns; the "mechanic" is capitalizing, not dodging.
- **Tell:** the boss takes massively increased damage (a shield drops, an intermission opens, all the adds/notes are cleared, an execute/sub-threshold phase begins).
- **Response:** pool and pop DPS cooldowns / Bloodlust for the window; maximize burst while it's open. Failing it doesn't kill *you* — it overruns the *timer* and snowballs the next cycle.
- **Consequence:** 🔵 (your job to capitalize) → 🔴 indirectly when a missed window means the fight never ends and a later mechanic wipes you.
- **Role:** DPS-led (everyone shifts to damage).
- **Examples:** *Siphon Void* (after all 6 Notes silenced) — L'ura (Seat of the Triumvirate).
- **Diagram idea:** a boss health bar flashing "+DMG" with cooldown icons lighting up beneath it.

## `balance-kill`
**Balance Kill (Paired Bosses)** — two linked enemies that must die *together*; leaving one alive triggers a runaway enrage on the survivor.
- **Tell:** two bosses sharing the fight, with a stacking enrage/empower on whichever one outlives the other.
- **Response:** keep both at even HP and cleave them down to die simultaneously; don't tunnel one. Not interruptible, dispellable, or soothable — it's a damage-routing problem.
- **Consequence:** 🔴 — a lopsided kill enrages the survivor and wipes the group.
- **Role:** all (DPS balance their target damage; tank keeps both together).
- **Examples:** *Broken Bond* — Derelict Duo / Latch & Kalis (Windrunner Spire).
- **Diagram idea:** two health bars side by side with a balance-scale icon and a warning when they diverge.

## `flavor`
**Flavor** — low-priority filler: chip damage, cosmetic casts, defensives that don't demand a reaction.
- **Tell:** a small auto-ish hit, a self-buff like Shield Wall, or a tiny poke with no real consequence.
- **Response:** nothing special — keep doing your job. Listed so the trainer can mark "safe to ignore."
- **Consequence:** ⚪ flavor.
- **Role:** all (no action required).
- **Examples:** *Shield Wall* — Commander Kroluk (Windrunner Spire); *Shoot* — Swiftshot Archer trash (Windrunner Spire).
- **Diagram idea:** a greyed-out ability icon with a small "ignore" tag.

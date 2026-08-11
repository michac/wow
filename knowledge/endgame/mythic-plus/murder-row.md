---
title: Murder Row — Midnight S2 M+ dungeon guide (STUB, day-1)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" content update notes — S2 M+ rotation (tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # "The Shadows Deepen: Midnight Season 2 Begins August 18" (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-instance/1304   # instance + boss list + description (tier 1 game data, static-12.1.0_68914)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2679   # Kystia Manaheart (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2680   # Zaen Bladesorrow (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2681   # Xathuux the Annihilator (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2682   # Lithiel Cinderfury (tier 1)
confidence: low
---

# Murder Row — Midnight Season 2 Mythic+

> 🚧 **STUB — written on patch day (2026-08-11).** Murder Row is a Midnight
> launch dungeon that has **never been in a Mythic+ pool before**; it joins the
> rotation with Season 2. Everything below comes from **Tier-1 game data** (the
> Adventure Guide via the Blizzard journal API at build 12.1.0.69214) plus the
> Tier-1 12.1 notes. There is **no route, no trash table, no affix interaction
> and no loot table here yet** — the Tier-3 guide sites (Method / Icy Veins /
> Wowhead) had not published M+ coverage for it on patch day, and no keys exist
> to test against until **2026-08-18**. Fill it from the sources in `## TODO`;
> do not infer the missing parts.

**Where:** Silvermoon City (the Murder Row district). 4 bosses. Journal
instance **1304**, map 2813, expansion Midnight (journal-expansion/516).

**Premise (journal):** *"The darkened streets of Murder Row hide a secret
fel-smuggling operation that has been preying on the fears of Silvermoon's
citizens ever since the Voidstorm appeared."* Fel is the dungeon's theme
throughout — the final boss is a warlock running the operation.

## Availability right now (pre-season)

12.1 shipped **one week ahead of Season 2**, so this dungeon's status is dated:

| | **Week of 2026-08-11 (live now)** | **From 2026-08-18** |
|---|---|---|
| Difficulties | Normal / Heroic / **Mythic 0** | + **Mythic+ (keystones)** |
| Mythic 0 lockout | **weekly, this week only** | back to **daily** |
| M0 reward | **Champion 1/6 (292)** | Champion 1/6 (292) |
| Keystones | **do not drop** | drop normally |
| Teleport | — | unlocked by a timed **Mythic 10+** |

Season-wide context (crests, rating ladder, vault rows, the other seven
dungeons) lives in [`season-2-overview.md`](season-2-overview.md); rewards in
[`loot.md`](loot.md); affixes in [`affixes.md`](affixes.md) — the S2 affix set
is **not yet confirmed**, so nothing here is written against an affix.

**Practice:** Murder Row has a **Follower Dungeon** version (it is in the
Midnight follower pool — carried from `season-1-overview.md`, tier-3 Icy Veins,
verified 2026-06-13). Good for learning the layout blind before keys open;
useless for M+ tuning or affixes.

## Bosses

Boss names and order are **Tier-1** (journal-instance/1304). The mechanic text
below is the **Adventure Guide's own overview and role callouts, verbatim in
substance** — it names abilities and says what they do, but it does **not**
give positioning, kill order, cooldown timing or route context. Archetype and
consequence tags are deliberately **omitted** until the fight is seen live, so
that nothing here can be mistaken for a played-and-verified guide.

### 1. Kystia Manaheart <!-- enc:2679 -->

A Magister who never gave up fel magic and backs the smugglers. She fights with
her pet mana wyrm **Nibbles**, which she controls with **Illicit Infusion**;
remove the infusion and Nibbles breaks free, reverts to its light form and
**helps the group** via **Light Infusion**.

| Ability | What the journal says |
|---|---|
| **Illicit Infusion** | Kystia's control on Nibbles — it turns Nibbles hostile to players |
| **Light Infusion** | What Nibbles reverts to once freed; it then assists the group |
| **Destabilized** | While Kystia is Destabilized she inflicts heavy damage to **all** players (healer callout) |
| **Fel Spray** (Nibbles) | Avoid it |
| **Corroding Spittle** (Nibbles) | (named in the journal; no description published) |
| **Mirror Images** | **Interrupt it** (DPS + tank callout); the images cast **Felstorm** |
| **Felshield** | (named; no description published) |
| **Chaos Barrage** | (named; no description published) |
| **Fel Nova** | (named; no description published) |

### 2. Zaen Bladesorrow <!-- enc:2680 -->

Oversees the shipments of illegal fel artifacts. The signature cast is a
**line-of-sight** check — *"demonstrates how this town got its name."*

| Ability | What the journal says |
|---|---|
| **Murder in a Row** | At **100 energy** Zaen casts it at **all** players — **get to cover** or take heavy damage |
| **Forbidden Freight** | Shipment crates that **provide the cover** for Murder in a Row |
| **Freight Explosion** / **Fel-Infused Freight** | Freight-related follow-ups (named; no description published) |
| **Same-Day Delivery** | Avoid its damage |
| **Fire Bomb** | Avoid its damage |
| **Envenom** | Heavy damage to Zaen's **current target** (tank callout); applies **Heartstop Poison** |
| **Killing Spree** | (named; no description published) |

### 3. Xathuux the Annihilator <!-- enc:2681 -->

A summoned demon — one of Lithiel Cinderfury's, serving her for the joy of
destruction. His rage builds until it erupts.

| Ability | What the journal says |
|---|---|
| **Demonic Rage** | The rage eruption; grants him **Burning Steps** |
| **Burning Steps** | Damaging **fel pools** that expand from Xathuux's location and remain on the ground **for a long duration** |
| **Axe Toss** | Targets a random player and applies **Fel Lightning** to **all** players **until the axe is destroyed** |
| **Legion Strike** | Heavy Physical damage **and reduces incoming healing** (tank + healer callout) |
| **Infernal Crush** | (named; no description published) |

### 4. Lithiel Cinderfury <!-- enc:2682 -->

The warlock running the smuggling operation — she sells fel as protection from
the Voidstorm and pockets the profit. A demonology-flavored fight built around
a slowly expanding wave and her own **Demonic Gateway**.

| Ability | What the journal says |
|---|---|
| **Fingers of Gul'dan** | Summons **Wild Imps** near **every** target (imps cast **Felfire Burst**) |
| **Demonic Gateway** | Lithiel casts it to escape after Fingers of Gul'dan. Players who travel through it are **immune to Malefic Wave's initial impact** — but passing through the Wave that way still applies the lingering DoT (healer callout) |
| **Malefic Wave** | Slowly **expands over a large area**, heavy damage plus a lingering damage-over-time. Grants **Malefic Empowerment** to any summoned demons still alive when it passes over them |
| **Chaos Bolt** | High damage to a random target **if not interrupted** |
| **Summon Vilefiend** | Summons a vilefiend (**Shadow Bite**); the **Furious Vilefiend** inflicts heavy damage (tank + healer callout) |
| **Summon Infernal** | A slow but powerful Infernal that **fixates** onto players (**Felfire Core**) |
| **Searing Fel Flame** | (named; no description published) |
| **Felshield** | (named; no description published) |

## DPS notes (you are DPS)

Only what the Tier-1 journal actually supports:

- **Two hard interrupts are named outright:** Kystia's **Mirror Images** and
  Lithiel's **Chaos Bolt**. Both are called out for damage dealers.
- **Kystia is a "free the pet" fight** — Nibbles flips from hostile to helpful
  when Illicit Infusion comes off, so the infusion is the thing to act on, not
  the wyrm.
- **Zaen is a cover fight**, not a dodge fight: watch his **energy to 100** and
  put a **Forbidden Freight** crate between you and him.
- **Xathuux's Axe Toss is a kill-the-object check** — Fel Lightning ticks on
  everyone *until the axe is destroyed*, so it is a stop-and-swap.
- **Lithiel's Demonic Gateway is usable by the group** and is the stated answer
  to Malefic Wave's impact; her Wild Imps and other demons must die before the
  Wave passes over them or they get **Malefic Empowerment**.

## TODO

- [ ] **Route + trash table** — the whole thing. Sources to use, in order:
      `https://www.method.gg/guides/dungeons/murder-row` ·
      `https://www.icy-veins.com/wow/murder-row-dungeon-guide` ·
      Wowhead's Murder Row M+ guide. **None had S2 M+ coverage on 2026-08-11** —
      re-check after 2026-08-18.
- [ ] Convert the boss tables to the house format used by
      [`skyreach.md`](skyreach.md): **Ability | What it does | Do | Archetype |
      Tier | Role**, with archetypes drawn from
      [`../../systems/mechanic-archetypes.md`](../../systems/mechanic-archetypes.md)
      and consequence tiers 🔴/🟠/🔵/⚪. Archetype tagging needs the fight seen,
      not the journal text.
- [ ] Fill the abilities the journal names but does not describe (Corroding
      Spittle, Felshield, Chaos Barrage, Fel Nova, Killing Spree, Freight
      Explosion, Fel-Infused Freight, Infernal Crush, Searing Fel Flame) from
      spell data (`wowkb.blizzard spell <id>` / wago DB2) or a live pull.
- [ ] **Warcraft Logs encounter IDs** for the four bosses, once an S2 zone
      exists on WCL (the S1 dungeon files carry theirs).
- [ ] Confirm whether the dungeon received any **12.1 tuning or QoL changes**.
      Blizzard only announced updates for the three *returning* dungeons (Ruby
      Life Pools / Kings' Rest / Temple of Sethraliss) — Murder Row was not
      named, but it has never been keystone-tuned before.
- [ ] Confirm the **Follower Dungeon** row in game (currently tier-3 inference).
- [ ] Re-check the M0 / M+ **loot ilvls** against live drops; the 292 figure is
      Tier-1 for M0 but the +2→+10 ladder in `loot.md` is tier-3 today.

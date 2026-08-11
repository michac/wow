---
title: Den of Nalorakk — Midnight S2 M+ dungeon guide (day-1; no route yet)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes → Mythic+ Dungeon Rotation (tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # "The Shadows Deepen: Midnight Season 2 Begins August 18" (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season details (tier 1)
  - Blizzard journal-instance/1311 + journal-encounter/2776 (The Hoardmonger) + /2777 (Sentinel of Winter) + /2778 (Nalorakk) — fetched live 2026-08-11 at namespace static-12.1.0_68914-us (tier 1, boss + ability names and the Adventure Guide text)
  - https://www.icy-veins.com/wow/dungeons-guide  # Midnight dungeons overview, upd. 2026-08-10 "for Season 2" — entrance coords + level req only (tier 3)
  - https://maxroll.gg/wow/class-guides/demonology-warlock-mythic-plus-guide  # per-boss + trash tips w/ spell IDs, captured to the KB 2026-08-11, source updated 2026-08-11 (tier 3)
  - https://maxroll.gg/wow/class-guides/havoc-demon-hunter-mythic-plus-guide  # same Den of Nalorakk section, independent capture (tier 3, corroboration)
  - https://warcraft.wiki.gg/wiki/Den_of_Nalorakk  # zone/subzone + enemy families (tier 4, corroboration only)
confidence: medium
---

# Den of Nalorakk — Midnight Season 2 Mythic+

> ⚠ **DAY-1 FILE, written 2026-08-11.** This dungeon shipped with Midnight
> (12.0.1, 2026-02-10) but **sat out Season 1** and enters the keystone rotation
> for the first time in **Season 2**.
>
> **Evidence classes in this file, kept apart on purpose:**
> - **Tier 1 — the Blizzard dungeon journal.** The boss list and every ability
>   name in the boss tables come straight from it (fetched live at build
>   `12.1.0_68914`), not from editorial prose. This is the floor.
> - **Tier 3 — maxroll, captured 2026-08-11.** Four of this repo's
>   `classes/*/*/maxroll-mplus.md` captures — **Demonology**, **Affliction**,
>   **Havoc** and **Vengeance** — carry a **dedicated "Den of Nalorakk" section**
>   with per-boss tips and a trash list, **with spell IDs**, and all four agree
>   near-verbatim (the only divergence is a wording difference on Raging Squall,
>   flagged where it lands). The **Destruction** capture has the dungeon heading
>   and a talent import but **no tips**, so it corroborates nothing here. The
>   Route / Trash / DPS-notes sections below are built from that material and
>   **tagged Tier 3** inline.
> - **Still missing, and not invented:** a pull-by-pull MDT route, keystone par
>   time, consequence tiers, affix interactions, and the per-boss loot table.
>   The searches that came up empty on patch day were **Method's per-dungeon S2
>   guide pages, Icy Veins' per-dungeon S2 guide pages and wago.io MDT routes**
>   — *searched 2026-08-11, those three instruments only*. That is not a claim
>   that no Tier-3 M+ content exists for this dungeon; maxroll's clearly does.
>   See `## TODO`.
>
> ⚠ **12.1's four global class changes apply here like everywhere else** — most
> importantly **player health and creature damage both +25% at max level** (with
> health consumables rescaled and several DPS/Tank healing+absorb spells
> retuned), plus lowered major DPS cooldowns with raised steady-state damage,
> a "missed" interrupt visual, and DR categories resetting after **20s** (was
> 16s). So nothing in this dungeon is "unchanged by 12.1": there are no
> *instance-specific* 12.1 changes on record, but the damage/health math under
> every pull moved. Anyone's pre-12.1 sense of how hard a pull hits is stale.

> 📅 **12.1 shipped in two steps.** The week of **2026-08-11** is a **pre-season
> week**: this dungeon is available on **Heroic and Mythic 0 only**, M0 is on a
> **weekly** lockout (this week only) and drops **Champion 1/6 (292)**. **No
> keystones drop until the week of 2026-08-18**, when Mythic+ Season 2 opens and
> M0 returns to a daily lockout. See
> [`season-2-overview.md`](season-2-overview.md).

## At a glance

| | |
|---|---|
| Zone | **Zul'Aman** — subzone *Nalorakk's Prowl*, southern mountains |
| Entrance | ~**31.0, 84.0** in Zul'Aman *(tier-3, Icy Veins)* @verify-ingame |
| Level | **88+** (Normal) · level 90 at endgame *(tier-3, Icy Veins — same source as the coords)* @verify-ingame |
| Bosses | **3** — The Hoardmonger → Sentinel of Winter → Nalorakk |
| journal-instance | **1311** |
| Added | patch **12.0.1** (2026-02-10); first M+ appearance **Season 2** |
| Follower Dungeon | ✅ yes (Midnight follower pool) — the cheapest way to learn the layout before Aug 18 |

**Premise (Adventure Guide, verbatim-ish):** Nalorakk, the **Loa of War**, was
wounded by Zul'jin and Malacrass and turned his back on the Amani, retreating to
his den to sleep off the pain. The Amani now want the rift healed — so you escort
**Zul'jarra** into the Loa of War's *mind* and beat his three **trials** to earn
his blessing. The first two bosses are the trials; the third is Nalorakk himself,
fought inside his battle-dream.

This ties directly into the 12.1 storyline — Zul'jarra is the same character
driving the Coiled Isle campaign (see [`../../factions/zuljarras-forces.md`](../../factions/zuljarras-forces.md)
and [`../../systems/coiled-isle.md`](../../systems/coiled-isle.md)).

## Route

**No pull-by-pull route yet.** No MDT route was found on wago.io on 2026-08-11
and neither Method nor Icy Veins had a per-dungeon S2 page for it *(searched
2026-08-11; those instruments only)*. Do **not** infer a pull order from the boss
order.

What *is* known about the space between the bosses, from the maxroll trash list
(Tier 3) plus the wiki's enemy families (Tier 4): the dungeon runs through
**forest-troll, furbolg/beast and ice-elemental** packs, and the named trash
below sorts into three clusters that match the boss themes — a **hunger/beast**
cluster (Spirit of Hunger, Keen-Eyed Striker, Grizzled Warbringer) before
The Hoardmonger, an **ice** cluster (Frigid Mauler, Glacial Revenant, Avatar of
Determination) before Sentinel of Winter, and a **troll-caster** cluster
(Earthwhisper Tender, Stormbound Mystic, Ruthless Totemcaller, Loa Speaker Nanea)
on the way to Nalorakk. That is a *reading* of the trash list, not a verified
path — treat it as orientation, not a route.

## Trash

**Tier 3 — maxroll, captured 2026-08-11**; identical across all four captures
that carry tips (Demonology / Affliction / Havoc / Vengeance). Ability spell IDs
are maxroll's Wowhead links, not journal data. **Consequence tiers and role
columns are deliberately absent** — keystones do not drop until **2026-08-18**
(Tier 1), so nobody *can* have run this on a key yet and those columns would be
fabricated. Sibling files (e.g. [`skyreach.md`](skyreach.md)) show the fuller
target format.

### Interrupt these

| Mob | Ability | Spell ID |
|---|---|---|
| **Earthwhisper Tender** | Earth Bolt · Healing Breeze | 1241214 · 1297696 |
| **Frigid Mauler** | Frigid Roar | 1309919 |
| **Stormbound Mystic** | Lightning Bolt · Arc Lightning | 1246687 · 1297778 |
| **Loa Speaker Nanea** | Lightning Bolt | 1290205 |

Note the healer mob: **Earthwhisper Tender's Healing Breeze** is the one cast in
the list that undoes damage rather than dealing it.

### Casts to watch (stop / mitigate / kill)

| Mob | Cast | Spell ID | What maxroll says to do |
|---|---|---|---|
| **Spirit of Hunger** | Feast of Misery | 1238687 | Pay extra attention to it |
| **Avatar of Determination** | Glacial Tomb | 1241463 | Applies a **root**; maxroll notes it can be broken by an invisibility-type effect (its example links **Greater Invisibility**, 115877 — a *Mage* spell, so the "which class breaks it" half is boilerplate reused across specs and is unverified for Warlock/DH) |
| **Ruthless Totemcaller** | Magma Totem | 1246820 | **Instant cast** — kill the totem immediately |
| **Grizzled Warbringer** | Primal Echo | 1246957 | Pay extra attention to it |

### Debuffs to respect

| Mob | Debuff | Spell ID | Note |
|---|---|---|---|
| **Keen-Eyed Striker** | Razor Dive | 1238440 | — |
| **Spirit of Hunger** | Starvation Effigy | 1238760 | Swap to the effigy/totem as soon as it appears |
| **Glacial Revenant** | Cryo Surge | 1239860 | — |

## Bosses

Three bosses, fixed order (journal-instance 1311). Ability names and behaviour
below are **quoted/condensed from the Blizzard dungeon journal**, which is Tier 1
and available on day 1. What is **missing** is the part the journal never gives:
how punishing each thing is in practice, what to actually press, and how affixes
change it. So the usual **consequence tier (🔴/🟠/🔵/⚪) and role columns are
omitted** — they would be fabricated. Archetype slugs are tagged only where the
journal text states the mechanic shape outright.

### The Hoardmonger <!-- enc:2776 -->

A gluttonous brute defending food and supplies stolen from the nearby troll
tribes. Nalorakk's **first trial**.

Core loop per the journal: he casts **Resourceful Measures** at **90%, 70% and
40% health**, each cast empowering one of his abilities (he gathers from the
**nearest resource pile** while doing it — a tank positioning lever). At **100
energy** he throws **Spoiled Supplies**, seeding **Rotten Mushrooms** that grow
for **12 seconds** and then detonate as **Putrid Burst**, covering everyone in
**Toxic Spores**. Touching a mushroom transfers the spores to you and **destroys
the fungus**, preventing the burst.

| Ability | Journal says | Archetype |
|---|---|---|
| **Resourceful Measures** | Cast at 90% / 70% / 40% health; empowers one of his abilities. He gathers from the **nearest resource pile** during it | burn-window |
| **Spoiled Supplies** <!-- 1234233 --> | At 100 energy — grows **Rotten Mushrooms** across the arena | soak |
| **Rotten Mushroom** → **Putrid Burst** | Grows 12s then detonates, applying **Toxic Spores** to all players | soak |
| **Toxic Spores** | Applied on contact with a mushroom; **removable by Poison-cleansing effects** | dispel |
| **Earthshatter Slam** <!-- 1234021 --> / **Bonespike Slam** | "Massive damage in a frontal cone" (Bonespike is the empowered version; applies **Bonespiked**) | frontal-cone |
| **Ravenous Bellow** <!-- 1234681 --> / **Hearty Bellow** | "High damage to all players" (Hearty is the empowered version) | raid-damage |
| **Overflowing Supplies** | Listed under Resourceful Measures; effect not described in the journal | — |

The one clearly actionable line: **run the mushrooms over before they pop.** The
journal repeats it in all three role sections (DPS, healer, tank), which is as
close to "this is the fight" as the Adventure Guide gets.

⚠ **Tier-3 correction to the obvious reading:** the journal makes soaking sound
free. maxroll (all four captures with tips) says **do not overdo it** — every soak applies
a **stacking poison** to you. So the mushrooms are a *shared* job with a personal
cap, not a "whoever is closest, always" job. maxroll also puts a **defensive
cooldown on every Ravenous Bellow**, which the journal's flat "high damage to all
players" does not convey.

### Sentinel of Winter <!-- enc:2777 -->

An embodiment of a winter storm. Nalorakk's **second trial**.

| Ability | Journal says | Archetype |
|---|---|---|
| **Frozen Tempest** <!-- 1235656 --> | "A massive storm that pulses Frost damage to all players and **continuously pushes them back**" — called out as heavy damage for all three roles | raid-damage; knockback |
| **Raging Squall** <!-- 1235623 --> | Squalls that **wander the landscape** inflicting moderate damage | ground-void-zone |
| **Shattering Frostspike** → **Fractured Shivercore** | Spawns Shivercore adds that channel **Winter's Shroud** until killed; also **Snowdrift**, and **Rimeshatter** → **Rime Detonation** | kill-priority-add; interrupt |
| **Glacial Torment** <!-- 1235549 --> | "Inflicts a large amount of damage, but **can be removed by Magic-cleansing effects**" | dispel |

⚠ **Tier-3 additions (maxroll, 2026-08-11)** that the journal does not state:
- The **Shivercore adds are interruptible and interrupt-worthy**, and the one to
  take is **the add that is *not* in melee of the boss** if you have a ranged
  kick — a role-split the journal's flat "kill them" doesn't give.
- Those adds **leave a pool under them**, and standing in it **counters Frozen
  Tempest's pushback**. That reframes the adds from pure kill-priority into
  positioning tooling.
- **Glacial Torment**: if the healer is not dispelling you, **press a personal
  defensive** — the journal only says it is dispellable, not what to do when it
  isn't dispelled.
- **Raging Squall** spawns the tornado **directly under the targeted player** and
  then mostly stays put (maxroll's Demonology capture words this as "stays in
  that area", Havoc/Vengeance as "doesn't leave the spawn location much") — so
  *where you are standing when it goes out* is what decides where the zone lives.
  Note this reads slightly against the journal's "wander the landscape"; the
  journal is the Tier-1 floor and stays, but expect the squalls to be far less
  mobile than the journal text suggests. **Confirm in game.** @verify-ingame

⚠ A Tier-4 SEO summary describes an "Eternal Winter" phase on this boss. **That
name does not appear anywhere in the dungeon journal** and is not recorded here.

Note the name collision: **Raging Squall** is also a trash mob in
[`skyreach.md`](skyreach.md) (a WoD/S1 dungeon) with a different ability set —
different creature, same name.

### Nalorakk <!-- enc:2778 -->

The **Loa of War**, fought inside his own battle-dream. **Zul'jarra fights
alongside you** and the fight is built around protecting her — the only escort-
shaped boss in the S2 pool as far as the journal shows.

| Ability | Journal says | Archetype |
|---|---|---|
| **Echoing Maul** <!-- 1242860 --> | Nalorakk's recurring hit; **every Echo of Nalorakk casts it too, at the same time** | raid-damage |
| **Forceful Roar** | "Pushes all players away" | knockback |
| **Fury of the War God** <!-- 1243011 --> | At **100 energy** — slams Zul'jarra across the arena and incapacitates her with **Concussive Shock**; **Echoes of Nalorakk** then charge the defenceless Zul'jarra, casting **Echoing Fury** on the **first target they collide with** | charge; kill-priority-add; **soak** |
| **Overwhelming Onslaught** <!-- 1243569 --> | "Inflicts significant damage **even while protected** by Zul'jarra's **Defensive Stance** <!-- 1261776 -->" — Defensive Stance "greatly reduces" it | tank-buster; stack |
| **Echo of Nalorakk** | The add; casts **Spectral Slash** | kill-priority-add |
| **Concussive Shock** · **Demoralizing Scream** · **Forceful Slam** | Named sub-abilities; the journal gives no body text for them | — |

The implied shape — **body-block the charging Echoes before they reach
Zul'jarra**, and keep Defensive Stance up for Overwhelming Onslaught — follows
from the journal text, but the *cost* of failing either (does Zul'jarra dying wipe
the group? does the encounter reset?) is **not stated anywhere Tier-1** and must
be seen live.

⚠ **Tier-3 additions (maxroll, 2026-08-11)** — note the vocabulary difference:
maxroll calls Fury of the War God a **soak** ("helping with soaking"), i.e. the
body-block is treated as an assigned group job, not an optional intercept. Hence
the extra `soak` tag above; the journal's charge/collide wording is the Tier-1
floor and stays. Also:
- **Press a personal defensive** when you are **targeted by Echoing Maul**, and
  again when you take a Fury of the War God soak.
- **Defensive Stance is a shield you have to be inside**, so **watch the
  Overwhelming Onslaught timer and be near the boss before it lands** — being
  out of position is what turns a tank-buster into your death. This is the one
  place the fight asks a ranged DPS to give up range on a timer.

## Affixes, loot and rating

**No dungeon-specific affix or rating facts** were found in the 12.1 Tier-1 notes
or in the maxroll captures *(searched 2026-08-11: the Content Update Notes, the
Season 2 overview post, the S1-ending forum post, and all five Warlock/Demon
Hunter maxroll M+ captures)*. The season-wide facts live in the files of record,
not here:

- Affixes → [`affixes.md`](affixes.md) (the S2 set is **still unconfirmed** —
  the 12.1 notes say nothing about it)
- Item levels / end-of-run + vault rewards → [`loot.md`](loot.md),
  [`../great-vault.md`](../great-vault.md)
- Crests (S2 = **Mistcrests**, 269–334) → [`../dawncrests.md`](../dawncrests.md)
- Rating, titles, the **M10 teleport** → [`rating-and-rewards.md`](rating-and-rewards.md)

**Six drops from this dungeon are already named** in the maxroll BiS tables
(Tier 3, captured 2026-08-11 — spread across the Warlock and Demon Hunter
**M+ *and* raid** captures under `knowledge/classes/`, since a dungeon item can
be BiS for a raid build). Which *boss* drops each is **not** stated there and is
not recorded here:

| Slot | Item | Item ID |
|---|---|---|
| Neck | Yoke of the Charging Bear | 251173 |
| Chest | War Trial Vestments | 251159 |
| Wrist | Winter's Embrace Bracers | 251154 |
| Legs | Forest Dream Leg-guards | 251160 |
| Boots | Arctic Explorer's Legwraps | 251153 |
| Weapon (2×) | Grim Harvest Gloves | 251143 |

⚠ The last row is maxroll's own table quoted as printed — a **"Weapon"** slot
holding **"Gloves"** is almost certainly a mislabel in the source. Do not act on
the slot; the item ID is the thing to trust. **Verify against the Wowhead item
page or the journal loot table before using this list to plan gear.**

## DPS notes (you are DPS)

**Tier 1 = the journal; Tier 3 = maxroll's per-boss DPS lines, captured
2026-08-11 and identical across the four captures that carry them (Demonology,
Affliction, Havoc, Vengeance).** These
are per-boss *survival and job* lines, not a rotation — for what to press, go to
the spec's own `rotation.md` under `knowledge/classes/`. The capture these came
from is
[`../../classes/warlock/demonology/maxroll-mplus.md`](../../classes/warlock/demonology/maxroll-mplus.md)
(§ Den of Nalorakk).

**The Hoardmonger**
- **Defensive on every Ravenous Bellow** (1234681). *(Tier 3 — the journal only
  says "high damage to all players".)*
- **Help soak Spoiled Supplies** (1234233) — popping **Rotten Mushrooms** by
  walking into them is a DPS job, listed first under Damage Dealers in the
  journal. *(Tier 1)* **But do not over-soak** — each soak stacks a poison on
  you *(Tier 3)*. The journal's **Toxic Spores** are Poison-dispellable, so a
  Poison cleanse is what resets your budget.
- **Stay reasonably close to the boss** so **Earthshatter Slam** (1234021) is an
  easy frontal to sidestep rather than a long run out of a cone *(Tier 3)* — the
  one line here that costs a caster uptime if ignored.

**Sentinel of Winter**
- **Defensive when you have Glacial Torment** (1235549) **and the healer is not
  dispelling it** *(Tier 3)*.
- **Interrupt the Shivercore adds**, and if you have a **ranged kick, take the
  add that is not in the boss's melee** — that split is why a ranged DPS is the
  right owner of that interrupt *(Tier 3)*.
- The adds' **ground pool counteracts Frozen Tempest's** (1235656) **pushback** —
  stand in it during the channel instead of fighting the knockback *(Tier 3)*.
- **Raging Squall** (1235623) spawns **under you**, so move before it goes out
  and it is parked somewhere harmless *(Tier 3)*.

**Nalorakk**
- **Defensive when targeted by Echoing Maul** (1242860), and again when you
  **soak Fury of the War God** (1243011) *(Tier 3)*. Per the journal, the Echoes
  stop at the **first target they collide with** — so the soak is positional, not
  a DPS race *(Tier 1)*.
- **Watch the Overwhelming Onslaught** (1243569) **timer and be near the boss**
  in time to be inside Zul'jarra's **Defensive Stance** (1261776) *(Tier 3)*.
  This is a scheduled uptime loss for ranged — plan a movement-friendly or
  instant filler around it rather than clipping a channel.

## TODO

Sources to fill this from, in priority order. **Do not close any of these from
memory or from a pre-Season-2 article.**

- [ ] **Play it.** The three bosses are live *now* on Heroic / M0 (weekly lockout
      this week) — a single M0 clear settles most of the "how punishing is it"
      gaps above, and confirms the entrance coords marked above.
- [ ] **A real pull-by-pull route.** Method (`method.gg/guides/dungeons/…`) and
      Icy Veins publish per-dungeon S2 guides; neither had one for this dungeon
      on 2026-08-11, and no wago.io MDT route was found. Re-check all three
      after 2026-08-18. *(The trash **table** is now filled from maxroll — what
      is still missing is the ordering and the count/percentage, which only an
      MDT route or a run gives.)*
- [ ] **Re-check maxroll** (`maxroll.gg/wow/class-guides/…-mythic-plus-guide`)
      after 2026-08-18 — it is the source that *did* have day-1 content here, and
      its Den of Nalorakk section is the thing most likely to gain detail once
      keys are live. Re-capture with `wowkb.maxroll --kb`, then re-harvest this
      file's Route / Trash / DPS sections from it; do not hand-edit the capture.
- [ ] **Consequence tiers + role columns** on the three boss tables, tagged
      against [`../../systems/mechanic-archetypes.md`](../../systems/mechanic-archetypes.md)
      — this file is a `mplus_memory` data source and the tags are its contract.
- [ ] **Fill the blank journal entries** — Overflowing Supplies, Snowdrift,
      Rimeshatter / Rime Detonation, Winter's Shroud, Concussive Shock,
      Demoralizing Scream, Forceful Slam, Bonespiked. The journal names them but
      ships no body text; resolve them via `wowkb.blizzard spell` / wago
      `SpellName`. **Start from the IDs this repo already has** rather than
      re-searching by name — maxroll's capture gives, and the tables above now
      carry inline: Ravenous Bellow **1234681** · Spoiled Supplies **1234233** ·
      Earthshatter Slam **1234021** · Glacial Torment **1235549** · Frozen
      Tempest **1235656** · Raging Squall **1235623** · Echoing Maul **1242860** ·
      Fury of the War God **1243011** · Overwhelming Onslaught **1243569** ·
      Defensive Stance **1261776**, plus the 15 trash spell IDs in `## Trash`.
      The blanks above sit adjacent to these in the spell tables, so a small ID
      window around each is the cheap way in.
- [ ] **Warcraft Logs encounter IDs** for the three bosses, once the S2 zone
      exists and logs are being uploaded (the S1 files carry these).
- [ ] **Confirm the "Eternal Winter" phase** on Sentinel of Winter — tier-4 only,
      absent from the journal. Either find it in game data or drop the question.
- [ ] **Resolve the Raging Squall conflict** — the journal says the squalls
      "wander the landscape"; maxroll (Tier 3) says the tornado spawns under the
      targeted player and largely stays put. Both are recorded above with the
      Tier-1 wording kept as the floor. One M0 clear settles it. @verify-ingame
- [ ] **Map the six known drops to bosses**, and get the full per-boss loot table
      (journal loot / Wowhead item pages). The item IDs above come from maxroll
      BiS tables that name the dungeon but not the encounter — and one row's slot
      label is visibly wrong.
- [ ] **Timer** (the keystone par time) — unknown until keys drop on Aug 18.

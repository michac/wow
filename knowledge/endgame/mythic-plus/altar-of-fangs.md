---
title: Altar of Fangs — Midnight S2 M+ dungeon guide (day-1 stub)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-20
reviewed: 2026-08-20
sources:
  - https://us.api.blizzard.com/data/wow/journal-instance/1322   # tier 1 — instance, bosses, modes, location
  - https://us.api.blizzard.com/data/wow/journal-encounter/2878  # tier 1 — Rav'i
  - https://us.api.blizzard.com/data/wow/journal-encounter/2879  # tier 1 — The Writhing Coil
  - https://us.api.blizzard.com/data/wow/journal-encounter/2880  # tier 1 — Zul'jan
  - https://worldofwarcraft.blizzard.com/news/24293281           # tier 1 — Curse of Ula'tek content update notes
  - https://worldofwarcraft.blizzard.com/news/24294369           # tier 1 — Midnight Season 2 overview
  - https://us.forums.blizzard.com/en/wow/posts/29833350         # tier 1 — S1 ending / S2 pre-season information
  - https://www.wowhead.com/spell=1306345/messy-eater            # game data — Messy Eater tooltip (chunk soak)
  - https://www.wowhead.com/spell=1307700/carrion-burst          # game data — Carrion Burst tooltip (stacking Nature DoT)
confidence: medium
---

# Altar of Fangs — Midnight Season 2 Mythic+

New 12.1 dungeon. **3 bosses**, 5 players, set inside the **Vaults of Atal'Utek**
on the **Coiled Isle**. Journal instance **1322** (map 2993), expansion Midnight.

> **Day-one file.** Everything below is transcribed from **Tier-1 game data** —
> the Blizzard journal (Adventure Guide) API at build `12.1.0_68914` — plus the
> Tier-1 content-update notes. That covers boss names, abilities, role callouts
> and drop lists. It does **not** cover routes, trash packs, pull order, kick
> priority, affix interactions or tuning, because no Tier-1 source publishes
> those and Tier-3 guides (Method / Icy Veins / Wowhead) will not be written
> until the season opens. See `## TODO`. Do not treat the absence of a route
> here as "the dungeon has no route problem."

Journal blurb: *"Upon the Altar of Fangs, the ancient Amani sealed the vaults of
Atal'Utek with the Fang of Ula'tek. Only that cursed dagger has the power to
unseal the prison of the great weapon of the Amani. Aid Orweyna and Liadrin in
their pursuit of Zul'jan, who has entered this accursed place in a misbegotten
attempt to bring lost glory back to the Amani."*

## Availability — read this before planning around it

12.1 shipped in two steps and this dungeon is on the split.

| | **Week of Aug 11 — live now (pre-season)** | **Week of Aug 18 — Season 2 opens** |
|---|---|---|
| Difficulties | Normal · Heroic · **Mythic 0** | + **Mythic+** (keystones begin dropping) |
| M0 lockout | **Weekly, this week only** | back to **daily** |
| M0 reward | **Champion 1/6 (ilvl 292)** | season-standard M+ table |

Corroboration that the keystone mode is not yet active: the journal instance
lists a `MYTHIC_KEYSTONE` mode with **`is_tracked: false`** at build
`12.1.0_68914`, while Normal / Heroic / Mythic are all tracked.

It is one of the **8 dungeons in the Season 2 Mythic+ pool** — see
`season-2-overview.md` for the full rotation and `keystones.md` for the
pre-season keystone rules.

## Route

**Unknown — not published on day 1.** Nothing has been measured or sourced, and
the journal API does not describe trash or pathing. The boss *order* below is
the journal's own encounter order (`order_index` on instance 1322):

1. **Rav'i**
2. **The Writhing Coil**
3. **Zul'jan** (final)

Whether that order is forced or route-optional is unverified.

## Trash

**Unknown — not published on day 1.** No mob names, no kick list, no percentage
counts. Do not infer them from the boss themes.

## Bosses

Consequence tiers: 🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor.

⚠ **Ability text below is the journal's, condensed; the tier and archetype
columns are our reading of that text and are not themselves Tier-1.** No
numbers (damage, cast time, cooldown) are stated anywhere in the journal, so
none are stated here.

### Rav'i <!-- enc:2878 -->

**Hint:** keep her off the meat

Ravenous hydra (creature 6210). Journal: *"This ravenous hydra has survived this
cursed place through scavenging the meat of the fallen."*

Core loop per the journal overview: the arena is littered with **Carrion Piles**
from creatures sacrificed into the pit. **Ravenous Stomp** drops **Fresh Meat**
onto some of those piles. When Rav'i runs out of energy she begins
**Ssscavenging** from the nearest Carrion Pile — and if that pile has Fresh Meat
on it, she escalates into a **Feeding Frenzy** instead.

| Ability | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|
| **Ssscavenging** (1298221) | Begun when Rav'i runs out of energy; she eats from the nearest Carrion Pile. Continuously applies **Carrion Burst** to all players until stopped. **Stops when her absorb shield is removed.** | burn-window; raid-damage | 🟠 | all |
| **Feeding Frenzy** (1307765) | The escalated form of Ssscavenging, entered if the pile she eats from holds **Fresh Meat**. Also applies **Carrion Burst** to everyone until stopped; likewise ends when the absorb is broken. | burn-window; raid-damage | 🔴 | all |
| **Carrion Burst** (1307700) | Stacking group damage applied continuously while Rav'i is eating — journal calls out "increasing applications". | pulsing-aura | 🔴 | healer |
| **Messy Eater** (1306345) | Her chomping throws chunks of rotting meat across the pit; each chunk hits enemies within **3.5 yd** of its impact for Nature damage, and **every chunk not caught by a player explodes into a Carrion Burst** on the group. | soak | 🟠 | all |
| **Ravenous Stomp** (1307915) | Drops **Fresh Meat** (1307703) onto some Carrion Piles. Fresh Meat carries **Scent of Blood** (1310378). | positional-gimmick | 🟠 | tank |
| **Regurgitate** (1296069) | Hurls waves of acid **in a player's direction**. | frontal-cone | 🟠 | all |
| **Triple Shot** (1297876) | Damage around **3 players** over time. | spread-out | 🔵 | healer |
| **Hydrastrike** (1298683) | Rav'i's melee damage on the tank. | tank-buster | 🔵 | tank |

**The one lever the journal actually names:** her eating (both Ssscavenging and
Feeding Frenzy) **ends when her absorb shield is removed** — so the group's job
is burst the shield off, and the tank's job is to manage where Fresh Meat lands
so she does not reach a fed pile.

**Messy Eater is a soak, not just healer damage.** The spell tooltip is explicit:
while she eats, chunks of meat land around the pit, and **a chunk nobody stands
in explodes into a Carrion Burst** — the stacking group-wide Nature DoT (29,095
per 3 s for 9 s, stacking). So the small circles that appear during her eating
phases are caught on purpose: each player eats one 3.5-yd hit instead of the
whole group eating another Carrion Burst stack. Journal callout tiers are
role-agnostic here — everyone soaks.

### The Writhing Coil <!-- enc:2879 -->

**Hint:** grip the Death Rattle

Creature 6230. Journal: *"In the feeding frenzy upon each other, there has been
one Child of Ula'tek that has proved victorious over the rest of the brood."*

Core loop: the Coil pressures the group with **Vindictive Onslaught** and **Tail
Scythe**. When it winds up **Death Rattle**, **Orweyna** empowers players with
**Vine Grip** — using that interrupts the cast, forcing the creature to
**Uncoil** so the group fights the constituent serpents one at a time. Damage
dealt while it is Uncoiled **persists after Assimilation** (i.e. it does not
reset when the serpents recombine).

| Ability | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|
| **Death Rattle** (1299053) | Increasing damage to all players. **Interrupted with Vine Grip**, which forces **Uncoil**. | raid-damage; interruptible-cast | 🔴 | all |
| **Vine Grip** (1287798) | The encounter-granted ability from Orweyna used to interrupt Death Rattle. | positional-gimmick | 🔴 | all |
| **Uncoil / Uncoiled** (1287811 / 1300612) | The split state — the monstrosity comes apart into individual serpents. | burn-window | 🟠 | all |
| **Spiteful Hunt** (1300503) | Cast by the Uncoiled Writhe. | fixate-chase | 🟠 | all |
| **Undermining** (1305393) | Cast by the Uncoiled Writhe. | ground-void-zone | 🟠 | all |
| **Vindictive Onslaught** (1299940) | The Coil's relentless assault; comprises **Burrowing Charge** (1300083) and **Venom Jet** (1300044). | charge | 🟠 | all |
| **Tail Scythe** (1298949) | Heavy Physical damage on the tank. | tank-buster | 🟠 | tank |
| **Toxic Barrage** (1310357) | Applies **Toxic Atrophy** (1310974): reduces **all players' movement speed and damage done**. | pulsing-aura | 🔵 | all |
| **Synchronized Venom** (1299189) | Listed on the Coil; the journal gives no description. | *(unclassified)* | ⚪ | all |

⚠ `Spiteful Hunt`, `Undermining` and `Synchronized Venom` are named in the
journal with **no body text at all** — the archetypes guessed above are the
weakest claims on this page. Verify in game or replace from a Tier-3 guide.

### Zul'jan <!-- enc:2880 -->

**Hint:** intercept the ritual

Final boss, creature 6218 — Zul'jarra's brother, the through-line of the whole
Coiled Isle campaign. Journal: *"With the Fang of Ula'tek, Zul'jan performs the
final ritual … Still held in the sway of the spirit of Malacrass, Zul'jan is
unaware that the Fang is also the only hope for his sister Zul'jarra's
survival."*

Core loop: during **Ritual of the Fang** he invokes the altar's ancient venoms
to empower the dagger, and it **damages the whole group unless intercepted**.
Then he hacks and chops through the group while **Bloodletting** stains the
ground — and Bloodletting is what **removes Ritual Venom**.

| Ability | What the journal says | Archetype | Tier | Role |
|---|---|---|---|---|
| **Ritual of the Fang** (1300876) | Empowers the dagger; **damages all players unless intercepted**. Grants **Fang Empowered** (1300888) and applies **Ritual Venom** (1300894). Called out to all three roles. | soak; raid-damage | 🔴 | all |
| **Ritual Venom** (1300894) | The debuff/stack the ritual leaves behind. **Removed by Bloodletting.** | dispel | 🟠 | all |
| **Bloodletting** (1301217) | The ground-staining follow-up; **removes Ritual Venom**. Called out to all three roles. | positional-gimmick | 🟠 | all |
| **Axegrinder** (1301111) | Physical damage to players struck. | frontal-cone | 🟠 | all |
| **Boneslicer** (1301413) | Physical damage to players struck. | frontal-cone | 🟠 | all |
| **Chop Down** (1301350) | Heavy Physical damage on the tank. | tank-buster | 🟠 | tank |

⚠ **"Unless intercepted" is the whole fight and the journal does not say what
intercepting *is*** — a soak position, an add kill, an interrupt, or an
encounter-granted button like the Coil's Vine Grip. This is the single most
important unknown on this page. Do not guess it into an answer.

## Loot

Per-boss drop lists, transcribed from the journal API. **Item levels are not
stated by the journal and are not stated here** — the difficulty→ilvl mapping
lives in `loot.md` and `../dawncrests.md`. Season 2 gear spans **269 → 334**;
this week's Mythic 0 drops **Champion 1/6 (292)**.

### Rav'i

| Item | ID |
|---|---|
| Vile Vial of Volatile Venom | 273796 |
| Coiled Fangstone | 273795 |
| Primordial Robe of Rites | 273785 |
| Hydra Scale Wristguards | 273775 |
| Poison-Proof Stompers | 273777 |
| Venom-Etched Crescent | 273780 |
| Hydraspine Twinblade | 273793 |

### The Writhing Coil

| Item | ID |
|---|---|
| Strand of Warding Fangs | 273781 |
| Knot of Writhing Serpents | 273794 |
| Leggings of Entwined Serpents | 273786 |
| Snakeskin Spaulders | 273774 |
| Aged Interwoven Scaleplate | 273787 |
| Vile Writhefang Glaive | 273782 |
| Toxin-Coated Warstaff | 273783 |
| Nocuous Focal Fang | 273779 |

### Zul'jan

| Item | ID |
|---|---|
| Band of the Amani Warlord | 273792 |
| Tattered Amani War Banner | 273797 |
| Handwraps of Blasphemous Rites | 273773 |
| Spare Speaker's Hood | 273791 |
| Chestguard of Corroded Scales | 273789 |
| Ancient General's Obsidian Pillars | 273776 |
| Polished Lightwood Channeler | 273778 |
| Ancestral Amani Recurve | 273784 |
| Sharpened Lightwood Slasher | 275070 |
| **Pillar of the Fanged Altar** | 279211 |
| **The Writhing Brood** | 276804 |
| Pattern: Snakeskin Lining | 270900 |

**Pillar of the Fanged Altar** and **The Writhing Brood** are the two entries on
Zul'jan's table with item IDs well outside the dungeon's contiguous 2737xx
block, and **Pattern: Snakeskin Lining** is a profession recipe — flagged for
whoever writes `classes/*/trinkets.md`, but their slot/type is **not confirmed
here** and must be read off the item API before being called trinkets.

## DPS notes (you are DPS)

Too thin to write honestly on day 1. The two things the journal makes
unambiguous:

- **Rav'i:** her eating states end when **her absorb shield is broken** — that
  is a burst-window check, not a dodge check.
- **The Writhing Coil:** damage done while it is **Uncoiled persists after
  Assimilation**, so the Uncoiled window is where the kill is banked.

Everything else — kick targets, cooldown timings, priority swaps — is unwritten.

## TODO

Fill from these, in trust order, once they exist:

1. **Tier 1 — game data (available now, partially drained):**
   - `wowkb.blizzard journal-encounter 2878|2879|2880` (done — this file).
   - `wowkb.blizzard item 279211` / `item 276804` — confirm whether **Pillar of
     the Fanged Altar** and **The Writhing Brood** are the dungeon's trinkets.
   - `wowkb.blizzard item <id>` across the drop lists for slots + ilvl bands.
   - **Answer "unless intercepted"** on Ritual of the Fang — read the spell
     (1300876 and its children) via `wowkb.blizzard spell`, or verify in game.
2. **Tier 1 — in game:** the **route** (pull order, percentage requirement,
   skips) and the **trash tables** (mob names, interruptible casts, enrages).
   Nothing but a run produces these. @verify-ingame
3. **Tier 3 — once Season 2 opens 2026-08-18:** Method
   (`method.gg/guides/dungeons/…`) and Icy Veins dungeon guides for route,
   trash, and the See→Do treatment the sibling files carry. Corroborate every
   number against Tier 1 before writing it. ⚠ Guide authors will not have
   these written on 2026-08-11; do not fetch and cache an empty page.
4. **Tier 2 — after two weeks of logs:** Warcraft Logs / Archon for actual
   pull-order consensus and the mechanics that kill pugs.
5. **`systems/mechanic-archetypes.md`** — once trash lands, feed the archetype
   tags into the mplus_memory pipeline; the S2 pool change is already flagged
   there as CHANGED.

## Changelog

- **2026-08-20** — **Messy Eater** was written as a pulsing healer-damage aura
  ("additional Carrion Burst on top"), which is what the Adventure Guide says.
  The spell tooltip says it drops **soakable chunks** and that an unsoaked chunk
  is what causes the extra Carrion Burst. Row rewritten (`pulsing-aura`/healer →
  `soak`/all) and the mechanic spelled out under Rav'i.

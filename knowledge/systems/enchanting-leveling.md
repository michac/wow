---
title: Midnight Enchanting — leveling 1–100, knowledge points, specs
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-29
reviewed: 2026-08-29
sources:
  - https://us.api.blizzard.com/data/wow/profession/333/skill-tier/2909?namespace=static   # full Midnight Enchanting recipe catalog (Tier 1, game data)
  - https://us.api.blizzard.com/data/wow/recipe/52940?namespace=static                     # per-recipe reagents (Tier 1, game data)
  - https://wago.tools/db2/SkillLineAbility?build=12.1.0.69214                            # shatter unlock ranks + AcquireMethod (Tier 1, game data)
  - https://www.wow-professions.com/guides/wow-enchanting-leveling-guide                   # the 1-100 route (Tier 3)
  - https://www.wow-professions.com/midnight/enchanting-specialization-guide-and-builds    # spec trees (Tier 3)
  - https://www.method.gg/guides/midnight-enchanting-profession-guide                      # spec trees + KP sources (Tier 3)
  - https://www.method.gg/guides/all-profession-knowledge-point-sources-in-midnight        # KP sources (Tier 3)
  - https://warcraft.wiki.gg/wiki/Enchant_Boots_-_Lynx's_Dexterity                         # skill-50 gate on the endgame enchants (Tier 3)
  - https://www.wowhead.com/guide/midnight/professions/enchanting-specializations          # spec trees (Tier 4)
confidence: medium
---

# Midnight Enchanting (1–100)

Trainer: **Dolothos**, Silvermoon City — the Bazaar artisan area, by the
enchanting table. Supply vendor **Lyna** stands next to him (vellums, rods).
Companion file for the profession *systems* layer (orders, sparks, the 12.1 KP
reset, Coiled Isle vendors): `professions.md`.

**Skill 50 is the real milestone, not 100.** Every enchant the endgame guides
call BiS — Empowered Rune of Avoidance, Amirdrassil's Grace, Eyes of the Eagle,
Lynx's Dexterity, Acuity of the Ren'dorei — is `Midnight Enchanting (50)`.
1–50 is cheap and fast; 50–100 is a long, expensive grind that buys craft
*quality* (rank 4/5 enchants) rather than access. A self-enchanter who wants
their own gear done can stop caring at 50 and drift the rest.

## The tier at a glance (Tier 1, game data)

Midnight Enchanting is skill **1–100** and holds enchants for exactly seven
equipment slots: **chest · helm · boots · rings · shoulders · weapon · profession
tool**. Plus rods, wands, oils, illusions, 25 Gleeful Glamours, the three
Shattering recipes (see below)
and house decor.

⚠ **There is no back (cloak) or bracer enchant in the Midnight tier.** Anyone
counting "9 enchantable slots" is counting a cloak enchant that this expansion
does not have; wrist and waist take a **socket** (Miasmic Jewelbinder) instead.

## Leveling path (Tier 3 — wow-professions)

| Skill | Craft | Mats / notes |
|---|---|---|
| 1–25 | **Runed Refulgent Copper Rod ×30**, then disenchant them | 30 Refulgent Copper Rod + ~150 Eversinging Dust; DE returns ~half the dust |
| 25–27 | **First-craft sweep**: 1× Enchant Helm - Rune of Avoidance, 1× Thalassian Phoenix Oil | dust + Radiant Shard; oil also needs 5 Mote of Light + Sunglass Vial |
| 27–38 | **Enchant Ring - Nature's Wrath** + **Illusory Adornment - Blooming Light**, ~14 each | ring = dust only; adornment = 1 Mote of Light + 1 Enchanting Vellum + dust |
| 38–40 | 1× **Enchant Shoulders - Flight of the Eagle**, 1× **Enchant Helm - Hex of Leeching** | dust + Radiant Shard each |
| 40–52 | **Thalassian Spellweaver's Wand ×4** | dust + Radiant Shard; **3 skill points each** — the best single step in the route |
| 52–55 | 1× each **Enchant Ring - Amani Mastery**, **Enchant Helm - Blessing of Speed**, **Enchant Shoulders - Thalassian Recovery** | first-craft points |
| 55–62 | **Enchant Ring - Amani Mastery ×9** | dust only; yellow, so expect to craft extra |
| 62–80 | Craft **1 of every recipe you own** (first-craft points), then whatever stays orange | rings go yellow around 80 |
| 80–90 | Helm / shoulder / **weapon** enchants | |
| 90–100 | **Weapon enchants only** — *Enchant Weapon - Worldsoul Aegis* stays orange to 100 | the expensive stretch |

Approximate mats for 1–62: **~412 Eversinging Dust · 27 Radiant Shard ·
6 Mote of Light**, plus the 30 rods for the opening step.

⚠ Reagent **quantities** above are Tier-3. The Blizzard recipe endpoint confirms
the reagent *names* but reports dust/shards as **modified-crafting slots**, which
carry no quantity — the same blind spot `tailoring-leveling.md` records for
bolts. Trust the names, sanity-check the counts in the crafting window.

**Enchanting is the most expensive Midnight profession to level, and also the
one that refunds itself**: everything you craft to skill up can be disenchanted
back into dust. Pair it with a crafting profession (Tailoring especially) and the
mat cost mostly collapses into "craft cloth, disenchant cloth."

Racials matter here: **Blood Elf +5 Enchanting skill**, Kul Tiran +2.

## The 24-KP freebie: Gleeful Glamours

**Jennara Sunglow** — second floor of the tower behind the trainer in Silvermoon
— sells the **Gleeful Glamour** recipes (one per playable race). Crafting each
once pays a first-craft knowledge point. Game data lists **25** of them; the
Tier-3 route says 24 and quotes the mats as **48 Eversinging Dust · 10 Mote of
Wild Magic · 8 Mote of Primal Energy · 4 Mote of Light · 2 Mote of Pure Void**.

This is the single cheapest block of knowledge in the profession and it is
available immediately. @verify-ingame: count Jennara's stock (24 vs 25) and
whether the Earthen glamour is sold alongside the rest.

## The Shattering line — mats convert DOWNWARD, one way

Three recipes under **Shattering** (Tier 1, Blizzard recipe endpoint, 12.1):

| Recipe | ID | Unlocked at | Effect |
|---|---|---|---|
| **Shatter Essence** | 53915 | skill 1 | Consumes a magical essence for a temporary Resourcefulness / Ingenuity / Multicraft buff — not a mat conversion |
| **Dawn Shatter** | 57152 | **skill 25** | Disenchant a **Dawn Crystal** → **3 Radiant Shards** |
| **Radiant Shatter** | 57153 | **skill 50** | Disenchant a **Radiant Shard** → **3 Eversinging Dust** |

**Both shatters are auto-granted — there is nothing to train, buy, drop or spend
knowledge on.** `SkillLineAbility` (12.1.0.69214) gives them `AcquireMethod: 1`
(automatically learned) with `MinSkillLineRank` **25** and **50** respectively;
the same flag carries the starter Runed Refulgent Copper Rod and Recraft
Equipment. So having Dawn Shatter and not Radiant Shatter just means Enchanting
skill is between 25 and 49 — **push to 50 and it appears**, which is the same
milestone the endgame enchants sit behind. Note the inversion: the crystal→shard
step unlocks *earlier* than the shard→dust step.

So **yes, Radiant Shards convert to Eversinging Dust**, at 1 shard → 3 dust, and
crystals step down to shards the same way. Output *quality* is capped by the
input's quality and otherwise scales with Enchanting skill plus the
**Shard Supplier** (Dawn Shatter) / **Dust Deliverer** (Radiant Shatter)
specializations. There is **no upward conversion** — dust does not become shards.
The specializations affect output *quality*, not access: neither shatter is
gated behind a spec node.

### ⚠ The shatter line is NOT the pre-50 dust faucet

Radiant Shatter unlocking at 50 looks like a chicken-and-egg — 1–50 costs dust,
and the shard→dust conversion is behind 50 — but it isn't one, because
**disenchanting is tiered by item quality and the dust tier is baseline**
(Tier 1, `TraitDefinition` 12.1.0.69214, the three Disenchanting Delegate
sub-specs):

| Disenchant | Yields | Sub-spec that improves it |
|---|---|---|
| **Uncommon** Midnight equipment | **Eversinging Dust** | Dust Deliverer |
| **Rare** Midnight equipment | Radiant Shards | Shard Supplier |
| **Epic** Midnight equipment | Dawn Crystals | Crystal Collector |

So the pre-50 supply is **disenchant every green (uncommon) you pick up** —
quest greens, dungeon greens, cheap AH greens — plus the leveling route's own
rods, which refund roughly half their dust when you DE them back. The shatters
are a **surplus tool for the endgame**: they exist because a max-level enchanter
DEing rare/epic drops drowns in shards and crystals while the dust runs dry.
Reading them as a leveling faucet is the trap; nothing in the 1–50 route needs
them.

⚠ The three sub-specs are a **choice**, taken one at a time
("learning a sub-specialization of your choice" → "another" → "the final one"),
so Dust Deliverer is not free either — but it only improves yield, it does not
grant access.

### Feeding it from Tailoring

A Midnight tailor's crafted armor is **rare or epic**, so it disenchants into
shards/crystals rather than dust; the shattering line is what turns that into
dust — which means **this loop only works at skill 50+**, and below that a
tailor cannot self-supply dust at all (see the trap note above: buy or farm
greens instead). The cheap loop is **Courtly Wrists** (recipe 52185, item 239671, RARE
ilvl 197, trainer-taught at skill 5): **2 Silverleaf Thread (vendor) + Bright
Linen Bolts**, no dust in the recipe. Craft → disenchant → Radiant Shatter.

⚠ Don't route this through the **Thalassian Competitor's cloth** set (items
239677-239685) even though it is the only **UNCOMMON** armor a tailor makes and
so would disenchant straight to dust: it needs 4 Mote of Primal Energy +
4 Carving Canine each *and* **Imbued** Bright Linen Bolts, which themselves cost
Eversinging Dust — the loop spends dust to make dust.

## Knowledge points

- **First craft of any recipe** — 1 KP each. The catalog is ~90 recipes deep, so
  first crafts are the dominant early faucet.
- **Gleeful Glamours** — ~24 KP in one sitting (above).
- **8 profession treasures** in the Midnight zones — 3 KP each (24 total).
- **Weekly trainer quest** — 3 KP.
- **Disenchanting** — ~9 KP/week (Tier 3; Enchanting-specific faucet).
- **Repeatable treasures** ~2 KP/week · **Thalassian Treatise** 1 KP/week.
- **Vendor books** — 10 KP each.
- **Jan'sari the Watchful** (Zul'jarra's Forces **Renown 6**, Tokka's Landing,
  Coiled Isle) — a 12.1 knowledge tome, 10 KP. Priced in Voidlight Marl +
  Artisan Enchanter's Moxie; price unconfirmed, see `professions.md`.
- **Chel the Chip** (The Abundance) — a one-time 10-KP item for Enchanting,
  quoted at **1,600 Unalloyed Abundance + 75 Artisan Enchanter's Moxie**
  (Tier 3). @verify-ingame: confirm the vendor, the cost and that Enchanting is
  on the list.

Tier-3 estimate for a fresh enchanter: **~60–70 KP on day one** from first
crafts + one-time treasures, then **~17 KP/week**.

⚠ The **one-time KP reset (12.1)** applies here as to every profession: once per
Midnight profession, permanent, and **it unlearns the recipes those points
bought**. Full doctrine in `professions.md`.

## Specializations

Four trees, unlocked by **skill level**:

- **Elevating Equipment** — every gear and profession-tool enchant, branched by
  faction style: **Thalassian Talents**, **Amani Augments**, and a nature /
  Haranir branch. This is where the enchants you actually want live (e.g.
  *Enchant Boots - Lynx's Dexterity* comes from
  **Elevating Equipment → Amani Augments → Berserker Brawn**).
- **Transitories, Tonics and Tools** — mana oils, combat wands, the enchanting
  rod, temporary illusions.
- **Disenchanting Delegate** — better mats from disenchanting (uncommon / rare /
  epic). Sub-node **Dust Deliverer**.
- **Spellbound Shatterer** — crafting stats: Multicraft, Ingenuity,
  Resourcefulness, and Concentration cost reduction.

⚠ **The unlock levels are disputed at Tier 3/4** and are not worth guessing.
One source has the four gates at skill **25 / 50 / 60 / 75** in the order listed
above; Method puts **Disenchanting Delegate at 25** and **Transitories at 50**.
@verify-ingame: read the four gates off the specialization UI.

### Spending, by goal

- **Enchanting your own gear** → **Elevating Equipment**, and specifically the
  branch that carries the enchants on your class's list. The branches are
  faction-flavoured, not slot-flavoured, so a single character's BiS set
  usually spans two or three of them — check each enchant's node before
  committing points.
- **Not paying for mats** → **Disenchanting Delegate**, 5 in the root then all
  30 into **Dust Deliverer** (Tier 3 recommendation).
- **Rank-5 enchants without mass production** → **Spellbound Shatterer** 20 +
  Infinite Ingenuity 30, the "concentration build": log in every few days,
  burn concentration on one guaranteed high-quality enchant.

## Expectations

Access is a skill-50 problem and a knowledge problem; **quality** is the skill-100
problem. Rank 5 without concentration wants skill 100 plus deep spec investment —
weeks. The realistic interim is skill ~50, the right Elevating Equipment branch,
and **concentration-assisted** rank-4/5 enchants on your own gear.

## TODO

- [ ] **Which node grants which enchant.** Only one is pinned down
      (Lynx's Dexterity ← Amani Augments → Berserker Brawn, Tier 3). The rest of
      the Elevating Equipment map is uncatalogued, and it is the thing a
      self-enchanter most needs before spending KP.
- [ ] Spec-tree **unlock levels** — two Tier-3/4 sources disagree (see above).
- [ ] **Artisan Enchanter's Moxie earn rate** — same open question as Tailoring's;
      12.1 gave Moxie a second sink (Jan'sari's tomes, Chel the Chip's KP item).
- [ ] Profession treasure locations (8 × 3 KP) — shared with `tailoring-leveling.md`.
- [ ] Confirm the 90–100 stretch: is *Worldsoul Aegis* really the only
      stays-orange-to-100 option, and what does it cost per craft?

---
title: Change Ledger — 12.1 "Curse of Ula'tek" (+ 12.0.7 hotfixes through 2026-07-28)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # Content Update Notes (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 information (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294062   # Venomous Abyss raid overview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24295085   # Lairs preview (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293963   # Coiled Isle / Vaults of Atal'Utek (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294064   # Cooldown Manager + UI updates (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24295382   # Housing blueprints (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24296054   # Neighborhood endeavors (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29850460  # S1 M+ title cutoffs (Tier 1)
confidence: high
---

# Change Ledger — 12.1 "Curse of Ula'tek"

> **Purpose:** the diff between 12.0.7 and 12.1. Use this to re-verify every
> `knowledge/**` file still labeled `patch: 12.0.7`. A file is **touched** if
> its topic appears in the "KB file impact map" below; otherwise its content is
> still current for 12.1 and only needs a front-matter re-stamp after a sanity
> read.
>
> This is a distillation of Tier-1 official notes. The verbatim archive is
> `patch-notes/12.1.md`. When a number matters, corroborate against
> wago.tools / the live API — never against editorial prose.

---

## ⚠ THE ONE THING THAT GOVERNS EVERY EDIT: 12.1 shipped in two steps

**12.1 went live 2026-08-11. Midnight Season 2 does NOT open until 2026-08-18.**
The week between is an official **pre-season week**. A large fraction of the
content-update notes describes the **Aug-18** state, not the state that is live
today. Writing those as present-tense is the single biggest correctness risk in
this sweep.

| | **Week of Aug 11 — LIVE NOW (pre-season)** | **Week of Aug 18 — Season 2 opens** |
|---|---|---|
| Zone | Coiled Isle, Curse Surges, Vaults of Atal'Utek, Venom Fishing, Zul'jarra's Forces renown | — |
| Dungeons | New S2 pool on Heroic + Mythic 0. **M0 on a WEEKLY lockout this week only**, drops Champion 1/6 (292) | Mythic+ S2 opens, keystones drop. **M0 returns to daily lockout** |
| Raid | none | Venomous Abyss — Normal / Heroic / Mythic + LFR Wing 1 |
| Lair | Tidebound Grotto — **World difficulty only**, drops S2 Veteran | Tidebound Grotto — Normal / Heroic / Mythic (flex) |
| Delves | Tiers 1–11 + **"?" Nemesis**. **No Bountiful.** Max reward **Adventurer 3/6 gear + Veteran crests** | Bountiful Delves, **Coffer Keys begin dropping**, **"??" Nemesis** |
| Prey | Normal + Hard modes. Hard Prey drops S2 Veteran | Nightmare Mode (Champion gear) + "Curse of the Isle" |
| PvP | Training Grounds: Arenas; unrated only | PvP Season 2, all rated |
| Great Vault | Rewards are from your **final Season 1 week**. S2 credit starts accruing now | First S2 vault claimable. **World row capped at Champion 3/6** for that first vault; **Hero 1/6** thereafter |
| Other | Pinnacle Caches drop S2 Veteran; **Crafting Sparks begin dropping** | Voidcore bonus rolls still absent — they arrive **week of Aug 25**, and need ≥3 vault panes unlocked |

Later LFR wings: **Wing 2 + Story Mode** week of Aug 25 · **Wing 3** week of
Sep 1 · **Wing 4** week of Sep 8.

**Rule for this sweep:** any Season-2 fact that is not in the Aug-11 column gets
written as *upcoming, dated*, not as current. `game-version.md` records the
pre-season state; a follow-up pass on/after 2026-08-18 flips it.

---

## Headline content additions (12.1)

- **New zone: The Coiled Isle** — the fog-shrouded island off the east coast of
  Zul'Aman. Continues the Zul'jan story; Zul'jarra pursues her brother. Contains
  the **Vaults of Atal'Utek** (group content + rotating public events that build
  to a boss fight), the **Altar of Fangs** dungeon, and the **Venomous Abyss** raid.
- **Zul'jarra's Forces** — the zone's **new renown faction**, and the primary
  renown track for the Coiled Isle. Renown begins accruing *before* landfall via
  Zul'Aman quests with Lady Liadrin, Orweyna and Zul'jarra. Quartermaster
  **Jan'sari the Watchful** at **Tokka's Landing**. Currencies: **Voidlight Marl**
  and **Artisan Moxies** (profession items). **20 renown ranks**; rewards include
  Cursebreaker's Bracers I/II (Veteran → Champion wrist), Curse Surge drop
  upgrades, crafting recipes, Spirit of Corrosion I/II, the Spirit of Tok'jara
  mount questline (R10), the title "Hash'ura of Zul'jarra" (R20).
- **Altar of Corrosion** — the zone's progression system: a **zone-scoped custom
  talent tree** granting player-power and quality-of-life perks (e.g. reducing
  the potency of the isle's venom), sited **in the Amani Foothold inside the
  Vaults of Atal'Utek**. Fed by **Corrosive Coins**. *(An earlier draft of this
  ledger said "Fed by Spirits of Corrosion" — wrong. Tier-1 24293963:216: "Spend
  Corrosive Coins to unlock various abilities in a custom talent tree at the
  Altar of Corrosion." **Spirit of Corrosion I/II** are discrete renown-rank-8
  and rank-14 grants (24293963:103,143), not the feedstock. Corrected
  2026-08-11 — `endgame/weekly-checklist.md:58,204` still repeat the wrong
  wording and need the same fix.)*
- **Curse Surges** — regularly spawn rare elites at **five rotating locations**
  across the isle. Killing a rare elite unlocks **Venom Fishing** at that
  location. Associated local story with the tortollan sea captain **Tokka**.
- **Lairs** — a new **instanced world-boss format**, and the biggest structural
  change to outdoor endgame. Found at fixed locations like Delves, with a
  summoning stone outside. Difficulties **World / Normal / Heroic / Mythic
  (flexible 15–25)**. On World difficulty you queue in solo and play a two-part
  scenario (clear elites until the boss appears) while the instance fills; the
  boss itself **scales 5–40 players**. Loot is **bind-on-pickup**, **weekly
  lockout**, and a Voidcore may be spent **once per week per lair**.
  - **Tidebound Grotto** (Coiled Isle, level 90, 1 boss): **Nymrissa Wavecaller**,
    a naga sorceress. Entrance is **underwater** below the isle.
  - Rewards: **World** rec. 273 → drops 279 (Veteran 1/6), Veteran Mistcrest ·
    **Normal** rec. 286 → 292 (Champion 1/6), Champion Mistcrest · **Heroic**
    rec. 299 → 305 (Hero 1/6), Hero Mistcrest · **Mythic** rec. 312 → 318
    (Myth 1/6), Myth Mistcrest. *(All four rows are in the Tier-1 preview table.
    An earlier draft of this ledger truncated the Mythic row and told the sweep
    to leave it unstated — corrected 2026-08-11 against
    `raw/pages/worldofwarcraft-com-en-us-news-24295085.md`.)*
- **New dungeon: Altar of Fangs** — 3 bosses, inside the Vaults of Atal'Utek.
  Available to Mythic 0 at launch; joins the **Mythic+ rotation on Aug 18**.
- **New raid: The Venomous Abyss** — 8 bosses, Coiled Isle, level 90, **LFR
  minimum ilvl 273**. Difficulties: LFR / Normal / Heroic / Mythic / Story Mode.
  Boss order and LFR wings:
  - **Wing 1 "The Soulcoilers"** (Aug 18): Nek'zali the Soulcoiler; The Twin Fangs
  - **Wing 2 "The Essence of Venom"** (Aug 25, with Story Mode): Entombed
    Sentinels; Vashnik the Malignant
  - **Wing 3 "The Serpent Warren"** (Sep 1): The Lost Explorers; Sszorak
  - **Wing 4 "The Tomb of Ula'tek"** (Sep 8): The Coiled Altar; Ula'tek
  - Mythic Ula'tek drops **3× Primeval Skyfriend** mounts; "Famed Slayer of
    Ula'tek" for the world-first 200 guilds; title "Venom's End" for Mythic Ula'tek.
- **Three new Delves**: **The Ring of Glory**, **Gnarldor Isle**, and the
  **Venomfall Deeps** Nemesis Delve. New snake/venom enemy variants seeded into
  existing Midnight Delves. The Nemesis boss is **Azta'rec** (per the
  "Let Me Solo Him: Azta'rec" Fabled achievement, earned by clearing "??"
  Nemesis in the first week of S2).
- **Training Grounds expands to Arena** — 3v3 vs bots, via Group Finder → PvP tab.
- **Prey Season 2** — "Prey: A Slithering Threat" questline; four new
  serpent-themed Nightmare targets; hunts across the Coiled Isle. **Ral'kala,
  Terror of the Isle** is summoned by burning **Ossified Relics** at **Haunted
  Braziers** while in Nightmare mode (designed as group content). **Afflicted
  Souls** (Champion-track bonus gear) and **Tormented Souls** (Hero-track) drop
  from Heavy Trunks in **Tier 6+ Bountiful Delves** and accelerate Nightmare
  hunts; bonus equipment is once per week per character. **"The Curse of the
  Isle"** is a permanent, toggleable Nightmare mode for the whole zone. The
  Season 2 Prey Journey track has **10 levels** (vendors: Construct Ali'a and
  Construct V'anore at Astalor's Sanctum, Silvermoon; track viewable in the
  Adventure Guide, Shift+J).
- **Mythic+ Season 2 rotation (8 dungeons)**: **Altar of Fangs** (new) ·
  Murder Row · Den of Nalorakk · The Blinding Vale · Voidscar Arena ·
  **Ruby Life Pools** (Dragonflight) · **Kings' Rest** (BfA) · **Temple of
  Sethraliss** (BfA). The three returning dungeons ship with design/QoL updates.
- **Story**: new stories in the **Arcantina**; after S2 starts, Arator returns to
  deal with the Voidspire fallout and the resurgence of the Twilight's Blade,
  continuing the hunt for Xal'atath.

## Currency & reward changes (12.1) — the moving-values material

- **Season 2 crests are "Mistcrests"** (Season 1's were Dawncrests). **All five
  tiers are confirmed from game data** — `CurrencyTypes` DB2 @ `12.1.0.69214`,
  currency IDs **3437–3441** (`raw/wago/CurrencyTypes-12.1.0.69214.csv`) — along
  with the upgrade band each one covers:

  | Crest | Upgrades | Season 2 ilvl band | (Season 1 equivalent) |
  |---|---|---|---|
  | Adventurer Mistcrest | Adventurer gear | **269–282** | Adventurer Dawncrest 224–237 |
  | Veteran Mistcrest | Veteran gear | **282–295** | Veteran Dawncrest 237–250 |
  | Champion Mistcrest | Champion gear | **295–308** | Champion Dawncrest 250–263 |
  | Hero Mistcrest | Hero gear | **308–321** | Hero Dawncrest 263–276 |
  | Myth Mistcrest | Myth gear | **321–334** | Myth Dawncrest 276–289 |

  So **Season 2 gear spans ilvl 269 → 334**, against Season 1's 224 → 289 — a
  clean +45 shift of the whole ladder. This is Tier-1 game data and is the
  **floor**: no editorial source may override these numbers.
- **Ritual Sites**: Tier 1–6 vault rewards now match **Season 2 Delve tiers 1–6**,
  and the sites now award **Season 2 crests** at Delve-equivalent rates.
  Tiers 1–3 keep Season 1 recommended ilvls and tuning. New recommended ilvls:
  **T4 259** (was 257) · **T5 268** (was 264) · **T6 275** (was 274).
  The **Tier 6 Advanced Ritual Studies quests no longer offer a Nebulous Voidcore
  bonus roll**; they remain completable for the achievement.
- **Void Assaults**: Void Strikes, Void Incursions and the Weekly Quest now give
  **Season 2 Adventurer crests**.
- **Void-Touched Caches**: new **Season 2 Adventurer Warbound** cache for **200
  Field Accolades**; new **Season 2 Veteran BoP** caches for **500** (random slot)
  and **750** (slot-specific). **The Season 1 gear caches have been removed.**
- **Val and Naigtal**: world quests, rares and elites now give **S2 Adventurer
  crests** in both Normal and Heroic World Tier. Rare equipment stays
  Warbound-until-Equipped and now drops at **S2 Adventurer 1/6** (Normal) /
  **Adventurer 4/6** (Heroic). World Boss + Weekly Quests give **S2 Adventurer**
  crests (Normal) and **S2 Veteran** crests (Heroic). ⚠ **World Boss drops stay
  Season 1 items and can no longer be upgraded**, as do the Mythic quest rewards
  from "Knocking off the Top (Heroic)".
- **The Catalyst**: converted class-set armor **now inherits secondary and
  tertiary stats plus certain special cantrip effects** of the source item.
- **Class set vendor Kirana relocated** — from near the March on Quel'danas raid
  entrance to **near the Catalyst in Silvermoon** — and now also stocks
  **Midnight Season 2 class set armor** for **Slumbering Coil Curios**.
- **Raid Great Vault tracks changed**: LFR / Normal / Heroic vault rewards now
  come in at **the first step of the next harder difficulty's track** (e.g. every
  Heroic-raid vault reward is **Myth 1/6**). Mythic raid vault rewards come in at
  **Myth 6/6**, except Very Rare items and loot from the penultimate and final
  bosses, which are **Myth 9** regardless of whether they came from the boss or
  the vault.
- **Nebulous Voidcores**: Season 1 Voidcores **convert to gold** at the end of
  S1 and can no longer be used in S1 content. From the start of S2 they are a
  **Great Vault reward**. The **raid re-roll cost drops to 1** (was 2). **Orin
  Straylight relocated near the Catalyst** in Silvermoon and provides **one extra
  Voidcore per week starting week 8 of Season 2**. ⚠ Voidcore bonus rolls are
  **not** in the first S2 Great Vault — they arrive the **week of Aug 25** and
  require **at least 3 panes unlocked**.
- **Delve Coffer Key Shard** amounts adjusted from multiple sources, weighted
  toward Coiled Isle content. Blizzard explicitly calls this **ongoing and a work
  in progress** — treat any specific shard number as volatile.
- **Prey vendors**: **Anguish costs for housing items substantially reduced**,
  for both Season 1 and Season 2.
- Ranged weapons (bows, crossbows, guns) can now use **transmog illusions**.
- New wild pets on the Coiled Isle; Pet Battler achievements added for Outland
  and Cataclysm.

## Season 1 close-out (final, historical values)

- **Midnight Season 1 M+ title cutoffs (US region, final, posted 2026-08-04,
  updated 2026-08-10):** Umbral Champion (top 1%) = **3960** · Umbral Hero
  (top 0.1%) = **4211**. These are now *historical* — S1 ended with the week of
  Aug 11 maintenance.
- S1 competitive PvP ended at 22:00 the night before regional maintenance. S1
  M+ dungeons and Cutting Edge / Ahead of the Curve stayed obtainable until
  maintenance began.

## Housing (12.1)

- **Blueprints** — export/import the whole house, interior only, exterior only,
  or a single room. Codes are shareable **cross-region** (excluding China) and
  linkable/inspectable in chat. **50 save slots + 10 auto-save slots**;
  auto-saves are created on import so a player can revert. Import preview lists
  required rooms/decor, budget, and what is missing. Dye handling tries to do the
  right thing and **does not replace already-dyed items**. New house permission
  **"Export"**, default **no one**. New **Reset** button (whole house / interior /
  exterior). Blueprints can be reported.
- **Pet Beds** — place a non-combat pet in the home. **Up to 100 indoors, 25
  outdoors.** Indoor pets can be **Stationary or Roaming** (new pet navigation);
  outdoor pets are Stationary only for now. A small number of pets are excluded.
- **Four new neighborhood Endeavors**: Amani trolls **"Knock-off Amani"** (Griftah's
  traders) · kobolds **"Candle Culture"** · Ohn'ahran centaur **"Every Bakar Has
  Its Day"** · tortollan **"Vacation Season"**. Neighborhoods now show visible
  results from completed Endeavors, old and new.
- **Houses can now reach level 12**, unlocking increased limits and large exteriors.
- New **Artisanal Rooms** from the General Contractor NPCs — four new rooms each
  for orc, human, night elf and blood elf styles, for **Community Coupons**;
  cross-faction room styles come from the neighborhood smugglers.
- **Dye crafting streamlined** (big bag-space saving); new dye colors including
  ones that **replicate the darker pre-12.0.5 appearances**.
- Two new decor categories: **Vines and Hanging Plants**, **Pet Beds**.

## Interface / Cooldown Manager (12.1) — also `knowledge/addon-dev/`

- **Cooldown Manager now tracks trinkets, potions, and racial ability cooldowns
  and durations.** Trinkets, health potions, combat potions and healthstones can
  also be **pinged** from the Cooldown Manager.
- Buff/debuff icons on raid and party frames get **independent sizes and border
  scales**. Healers can assign visual alerts to specific group buff spells via a
  new **Group Buff Filter UI**, and can configure or hide the buffs shown on Raid
  Frames.
- New **"Short" sounds** category for the Cooldown Manager; CDM sounds are now
  usable by the **Combat Audio Assist** accessibility feature.
- **Ping system**: ping the action bar and Cooldown Manager spells; ping certain
  items; ping player resources (health, and mana for healers) rendered as a chat
  bubble; ping icons appear on target/focus/raid frames; a new option to target
  environment-only / units-only / both; new slash commands **`/pingspell:1234`**
  and **`/pingitem:1234`** (id or name); ping macros support **`[@cursor]`**.
- **Addons**: *"Added new APIs that allow addons to display filtered sets of
  auras in customized ways, without exposing the underlying aura information that
  could be used for automation."* — the shipping form of the AuraContainer /
  AuraButton path. **New UI texture filenames are no longer published to the
  `ManifestInterfaceData` DB** (existing names remain; textures still usable).
- Edit Mode: Raid Warnings movable; raid/party frames gain the **Frame Size**
  setting (scalable up to +100%); the Loss of Control display is movable.
- Nameplates: friendly-nameplate options for name-only, class-colored names, and
  hiding realm names; **"Big Debuff" is now on by default** for enemy player
  buffs/debuffs.
- Misc: **Auto Loot is now account-wide**; Auction House filters persist across
  sessions; the World Map can show **player and cursor coordinates**
  (Gameplay > Interface); shift-clicking a map pin copies a **`/mappin`** slash
  command shareable outside the game; Friends List overhaul (WoW Friends, Recent
  Allies, filtering); Group Finder + Achievements pane fixes.

> ⚠ **`knowledge/addon-dev/` is NOT swept by the generic patch-sweep.** It has
> its own evidence classes and lint gates (`wowkb.kblint`), and most of its
> claims are `[client]` measurements taken on 12.0.7 — restamping those to
> `patch: 12.1` would falsely assert they were re-measured. Its patch-day edit
> list already exists as `addon-dev/12.1.0-ptr-heads-up.md`, which is now
> **live, not PTR**, and is the anchor for a separate hand pass.

## Classes (12.1)

### ⚠ Four GLOBAL changes that apply to every spec

These sit in the CLASSES preamble, above the per-class lists, and are easy to
miss because they are not attached to any class heading. They matter more than
most of the per-spec numbers.

1. **Player health and creature damage increased by 25% at max level.**
   Health-consumable values were adjusted to match the new health pool. This is
   a deliberate anti-spikiness tuning pass (Blizzard did the same at the start of
   Midnight and in early Dragonflight). Several **healing and absorb spells on
   DPS and Tank specs were adjusted** so they keep their relative impact.
   ⚠ **Any absolute HP / healing / consumable number written before 2026-08-11 is
   now wrong** — that includes health-potion values and any "X heals for N" claim.
2. **Major DPS cooldowns lowered, steady-state damage raised** for several
   specs — a stated design direction, not a one-off. So a spec's burst/sustained
   split has moved even where the KB's per-ability numbers still look familiar.
3. **All class interrupts** (Kick, Pummel, Counterspell, …) now show a **"missed"
   visual** over the target's head and play a distinct sound when used while the
   target was not casting.
4. **Diminishing-return categories now reset after 20 seconds** (was 16).

### Global PvP

A deliberate, game-wide **PvP snare tier-down** — "70% reduced to 50%,
50% to 30%, and so on" — targeting auto-applied rotational snares while leaving
some activated reductions intact. **Every class has PvP movement-slow lines.**
These are PvP-only and must not be written into PvE rotation guidance.

Non-PvP changes that matter to the specs this KB actually details:

- **Warlock (all)**: Drain Life health drain **+25%**; Zevrim's Resilience healing
  **+25%**; **Summon Demonic Gateway is now a Utility spell by default in the
  Cooldown Manager**. Large Soul Leech correctness pass — many abilities now
  *do* grant Soul Leech (Wither, Blackened Soul, Infernal Bolt, Soul Anathema,
  Wicked Reaping, Avatar of Destruction's Chaos Bolt, Unstable Affliction,
  Malefic Grasp, and several pet abilities), while Legion Strike, Cunning Cruelty
  and Channel Demonfire no longer erroneously do.
  - **Hellcaller**: **Blackened Soul redesigned** — if the target has your Wither,
    Chaos Bolt and Shadowburn add a stack; each stack gain has a chance to
    collapse, consuming a stack per second for Shadowflame damage until 1 stack
    remains. Blackened Soul damage **+45%**. **Mark of Peroth'arn redesigned** —
    Wither crits deal 215% (vs the usual 200%), Blackened Soul crits 225%.
    Wither damage **+25%**. Malevolence is deliberately unchanged.
  - **Affliction**: two new talents — **Hedonic Gorging** (Drain Life +10% damage;
    Siphon Life adds +10% Corruption damage; Dark Harvest channels 10% faster and
    deals +15%) and **Impetuous Wrath** (Shadow Bolt / Drain Soul / Malefic Grasp
    +10%, or +20% vs a Haunted target; Dark Harvest +10%/+20% likewise).
    **Shard Instability redesigned** — Shadow Bolt or Drain Soul damage has a 20%
    chance to make the next Unstable Affliction or Seed of Corruption free and
    instant. **Haunt now +16% damage for 18s (was 12%)**. **Removed: Nocturnal
    Yield, Patient Zero.**
  - **Demonology**: Shadow Bolt **+45%**, Demonbolt **+55%**, Summon Gloomhound
    **+35%**. **Diabolist** nerfed: Chaos Salvo / Felseeker / Wicked Cleave / Eye
    Explosion all **−20%**; Flames of Xoroth now **+3%** Fire and demon damage
    (was 4%).
  - **Destruction**: **Conflagration of Chaos redesigned** — Conflagrate and
    Shadowburn always crit and their damage is increased by your crit chance.
    All damage **+4.5%**; Soul Fire **+45%**; Chaos Bolt **+5%**; **Havoc now
    copies 50% (was 60%)**. **Shadowburn added as a tracked buff in the Cooldown
    Manager; Conflagration of Chaos removed from it.**
- **Demon Hunter (all)**: **Demon Hunters can now equip daggers** (so Devourer can
  use Intelligence daggers).
  - **Devourer**: **Mastery: Monster Within bonus damage during Void Metamorphosis
    reduced by 66%**, compensated by **all ability damage +32%** — net intent is
    slightly less damage inside Meta, significantly more outside. Collapsing Star
    +12%; Eradicate −6% (secondary target −15%); **Consume +60%** (does not affect
    Devour); Void Metamorphosis now +40% Void Ray damage (was 67%); Impending
    Apocalypse now +20% per Collapsing Star (was 30%); Hungering Slash now grants
    a temporary Vengeful Retreat charge instead of a free cast + reset.
    **Annihilator**: Otherworldly Focus +30% single-target (was 35%); Final Hour
    persists 6s (was 8s).
  - **Havoc**: **Demon Blades, Blade Dance and Chaos Strike now require equipped
    Warglaives / Axes / Swords / Fist Weapons.** New talent **Never Say Die**
    (+3% damage above 50% health; +5% leech below 50%). Trail of Ruin now applies
    damage **immediately** instead of as a 4s DoT. Serrated Glaive is now a **12s
    buff on the Demon Hunter** instead of a 15s debuff on targets. Blade Dance /
    Death Sweep / Chaos Strike / Annihilation all **+6%**; The Hunt **+12%**;
    Essence Break initial **+49%**; Immolation Aura **−8%**. Fury retune:
    Burning Hatred +30 Fury (was 40); Demon Blades 10–16 (was 8–15); Blind Fury
    10/20 per second (was 15/30). Inertia **+12% for 6s** (was 18% for 5s).
    **Inner Demon moved** — now a choice node with Chaos Theory (was with Chaotic
    Transformation). **Dash of Chaos removed.**
  - **Vengeance**: Fracture and Soul Cleave gain the same weapon requirement.
    **Sigil of Chains is now baseline at level 35** (no longer a talent), cooldown
    **60s** (was 90s), and **no longer replaces Sigil of Misery** — **Sigil of
    Silence** now does when selected. Improved Sigil of Misery no longer affects
    Sigil of Chains and instead cuts Sigil of Silence's cooldown by 15s when
    selected. All damage **+5.5%**; Soul Cleave, Fel Devastation and Feast of
    Souls healing **+25%**; Charred Warblades 5% (was 4%); Frailty 10% (was 8%);
    Revel in Pain 6% (was 5%). **Several talents changed tree locations.**

Other specs' 12.1 non-PvP changes exist in the verbatim archive
(`patch-notes/12.1.md`, CLASSES section, lines under each `▶ CLASS` heading) and
should be consulted per-file rather than restated here.

## PvP (12.1)

- **Gladiator's Distinction** (PvP trinket set bonus): tank/DPS now **+15%
  primary** (was 12%) and **+5% Stamina** (was 10%); healers **+10% Stamina**
  (was 15%).
- **Battlegrounds: players receive 20% less healing.**
- Players are **no longer knocked back while under Fear or Disorient**.
- **Solo Shuffle / BG Blitz**: missing a queue applies a stacking, **account-wide
  1-minute** re-queue debuff (anti win-trading).
- **Spoils of War** grants **+50% Conquest** once Conquest is uncapped for the
  season (was 30%).
- Season 2 PvP rewards: **Venomous Gladiator's Goredrake** (Gladiator) and
  **Vicious Lightbloom Boar** (Vicious Saddle) mounts; the Venomous* title ladder.

## Characters / world / quests (12.1)

- **Earthen**: baseline zone-exploration experience **reduced by 60%**;
  exploration XP from **low-level zones is no longer reduced** from baseline;
  **Ingest Minerals' Well Fed effect +30%** as compensation. (Directly changes
  Earthen leveling guidance.)
- **Omnium Folio introduction questline is now account-skippable** once any one
  character has completed it.
- New stories in the **Arcantina**.
- The **Amani Pass** between Eversong Woods and Zul'Aman no longer dismounts.
- Creature-spawn fixes across the game that could cause stuck-in-combat.

## 12.0.7 hotfixes folded in (2026-07-07 → 2026-07-28)

Archived verbatim in `patch-notes/12.0.7.md`. Nothing here changes a 12.1 claim;
listed so the sweep does not treat them as unreviewed.

- **Jul 7** — Voidspire skip respawn; Housing Daylight/Evening Circle Room grant
  fix; Mycomancer's Hearthspore charge bug; Thrillbot/Chillbot now unique; quest
  fixes (A Grave Concern, A Humble Servant, Delves Nemesis Primessence).
- **Jul 14** — Rune of Lingering no longer interrupts flag captures; Maisara
  Caverns Mythic quest-item drop; **Rommath now provides a Magister's Terrace
  portal for Omnium Folio weeklies**; Lighthook Grapple confined to Naigtal.
- **Jul 21** (announced Jul 17 as class tuning) — **Decor Duels**: last-30s
  auto-reveal removed, seeker energy rate −20%, hiders no longer attract flies,
  **Illusionary Coins rewards +100%**. PvP: DH Demon Muzzle 5% (was 15%) and
  Glimpse 25% (was 35%); Mistweaver Way of the Crane 100% (was 340%); Disc +3%;
  Holy Fire +15%/+27% and Holy +3%; Resto Shaman Riptide +15%.
- **Jul 28** — Blood DK Dance of Midnight ranks 2–3 damage-taken bug; Will of the
  Forsaken PvP-trinket cooldown display; **World Boss alt soulbound-item bug and
  off-spec reward bug fixed**.

---

## KB file impact map

Legend: **CHANGED** = notes touch this topic, content edit needed ·
**RESTAMP** = no 12.1 change found, re-verify + bump front matter ·
**NEW** = create file · **REGEN** = generated artifact, re-run its generator
rather than hand-editing · **RECAPTURE** = `verbatim: true` external capture,
re-fetch with its tool · **EXCLUDED** = not swept by this workflow, see note.

### endgame/

| KB file | Verdict | Why |
|---|---|---|
| endgame/dawncrests.md | CHANGED | S1 Dawncrests → S2 **Mistcrests**; every crest source re-pointed to S2 crests; file may need renaming/generalizing |
| endgame/great-vault.md | CHANGED | raid vault track jump (Heroic→Myth 1/6, Mythic→Myth 6/6, Very Rare/last-two→Myth 9); Voidcores as a vault reward; pre-season vault rules; World row Champion 3/6 then Hero 1/6 |
| endgame/weekly-checklist.md | CHANGED | the anchor doc — pre-season week reshapes nearly every row; new Coiled Isle weeklies, Lairs, M0 weekly-lockout week |
| endgame/prey.md | CHANGED | Prey S2, Nightmare targets, Ral'kala, Ossified Relics, Afflicted/Tormented Souls, Curse of the Isle, 10-level track, Anguish price cut |
| endgame/world-events.md | CHANGED | Val/Naigtal crest + drop retier; World Boss drops frozen at S1; Lairs supersede the old world-boss flow; Turbulent Timeways ended Aug 11 |
| endgame/catalyst.md | CHANGED | Catalyst now inherits secondary/tertiary stats + cantrips; Kirana relocated next to it and stocks S2 sets for Slumbering Coil Curios |
| endgame/delves/overview.md | CHANGED | 3 new delves, Nemesis Venomfall Deeps, pre-season tier/reward caps, Coffer Key Shard retune, Bountiful timing |
| endgame/delves/gulf-of-memory.md | RESTAMP | existing delve; only new snake/venom enemy variants |
| endgame/delves/sunkiller-sanctum.md | RESTAMP | same |
| endgame/raids/overview.md | CHANGED | add Venomous Abyss + its unlock schedule; add Lairs as a raid-adjacent format |
| endgame/raids/venomous-abyss.md | **NEW** | 8-boss raid; opens 2026-08-18 |
| endgame/raids/sporefall.md | RESTAMP | S1 raid, now previous-tier |
| endgame/raids/march-on-quel-danas.md | CHANGED | Kirana the class-set vendor moved away from its entrance |
| endgame/raids/the-voidspire.md | RESTAMP | S1 raid; Arator story continues from it but the raid is unchanged |
| endgame/raids/the-dreamrift.md | RESTAMP | no 12.1 mention |
| endgame/lairs.md | **NEW** | new instanced world-boss format + Tidebound Grotto |
| endgame/mythic-plus/season-1-overview.md | CHANGED | S1 is over — mark historical, record final cutoffs 3960 / 4211 |
| endgame/mythic-plus/season-2-overview.md | **NEW** | S2 pool, unlock dates, rating rewards, portals at M10 |
| endgame/mythic-plus/keystones.md | CHANGED | keys do not drop until Aug 18; M0 weekly then daily lockout |
| endgame/mythic-plus/loot.md | CHANGED | M0 drops Champion 1/6 (292); S2 crest currency |
| endgame/mythic-plus/rating-and-rewards.md | CHANGED | S2 titles/mounts (Venomous ladder, Breath of Blight/Ruin at 2000/3000) |
| endgame/mythic-plus/altar-of-fangs.md | **NEW** | new 3-boss dungeon, in the S2 pool |
| endgame/mythic-plus/kings-rest.md | **NEW** | returning BfA dungeon in the S2 pool |
| endgame/mythic-plus/temple-of-sethraliss.md | **NEW** | returning BfA dungeon in the S2 pool |
| endgame/mythic-plus/ruby-life-pools.md | **NEW** | returning DF dungeon in the S2 pool |
| endgame/mythic-plus/murder-row.md | **NEW** | in the S2 pool; no file exists |
| endgame/mythic-plus/den-of-nalorakk.md | **NEW** | in the S2 pool; no file exists |
| endgame/mythic-plus/the-blinding-vale.md | **NEW** | in the S2 pool; no file exists |
| endgame/mythic-plus/voidscar-arena.md | **NEW** | in the S2 pool; no file exists |
| endgame/mythic-plus/{algethar-academy,magisters-terrace,maisara-caverns,nexus-point-xenas,pit-of-saron,seat-of-the-triumvirate,skyreach,windrunner-spire}.md | CHANGED | **rotated OUT of the S2 pool** — mark as S1-era / not in the current rotation |
| endgame/mythic-plus/affixes.md | CHANGED | S2 affixes — notes mention "new Affixes" for Prey but the M+ affix set needs live confirmation |
| endgame/daily-weekly-quests.md | CHANGED | Coiled Isle weeklies; Ritual Sites T6 Voidcore bonus roll removed |

### systems/

| KB file | Verdict | Why |
|---|---|---|
| systems/housing.md | CHANGED | Blueprints, Pet Beds, 4 Endeavors, level 12, Artisanal Rooms, dye rework, 2 decor categories |
| systems/ritual-sites.md | CHANGED | T1–6 vault rewards realigned to S2 Delves; S2 crests; T4/T5/T6 rec ilvl 259/268/275; T6 Voidcore bonus roll removed |
| systems/void-incursions.md | CHANGED | Void Strikes/Incursions/weekly now give S2 Adventurer crests |
| systems/omnium-folio.md | CHANGED | intro questline now account-skippable |
| systems/void-forge.md | RESTAMP | no 12.1 mention found |
| systems/coiled-isle.md | **NEW** | the new zone: Vaults of Atal'Utek, Curse Surges, Altar of Corrosion, Venom Fishing, Tokka |
| systems/professions.md | CHANGED | Coiled Isle recipes via Zul'jarra renown; Artisan Moxies; dye-crafting streamline; Crafting Sparks in pre-season |
| systems/leveling-notes.md | CHANGED | **Earthen exploration XP −60%**, low-level zones no longer reduced, Ingest Minerals +30% |
| systems/mechanic-archetypes.md | CHANGED | S2 dungeon pool changes which archetypes are in rotation (feeds mplus_memory) |
| systems/macros.md | CHANGED | new `/pingspell:` `/pingitem:` `[@cursor]` ping macros; `/mappin` |
| systems/tailoring-leveling.md | RESTAMP | no direct 12.1 mention |
| systems/tailoring-recipes.md | RESTAMP | no direct 12.1 mention |

### factions/

| KB file | Verdict | Why |
|---|---|---|
| factions/zuljarras-forces.md | **NEW** | the Coiled Isle renown faction, 20 ranks, Jan'sari the Watchful |
| factions/amani-tribe.md | CHANGED | Coiled Isle campaign, Zul'jarra, Zul'jan, Amani Pass fix, Knock-off Amani endeavor |
| factions/slayers-rise.md | CHANGED | S1 PvP ended; S2 PvP rewards + Gladiator's Distinction change |
| factions/harati.md | RESTAMP | no 12.1 mention |
| factions/silvermoon-court.md | RESTAMP | no 12.1 mention |
| factions/the-singularity.md | RESTAMP | no 12.1 mention |

### planning/

The ranker's activity catalog is where the pre-season/Season-2 split bites
hardest — an activity that is not available until Aug 18 must not be rankable
today.

| KB file | Verdict | Why |
|---|---|---|
| planning/activities/mplus.md | CHANGED | no keys until Aug 18; new pool; M0 weekly lockout this week |
| planning/activities/great-vault.md | CHANGED | pre-season vault semantics; S2 credit accrual; World-row caps |
| planning/activities/delve-bountiful.md | CHANGED | **no Bountiful Delves during pre-season** |
| planning/activities/prey-weekly.md | CHANGED | S2 Prey; Nightmare not until Aug 18 |
| planning/activities/ritual-sites.md | CHANGED | S2 crests, new rec ilvls, T6 bonus roll removed |
| planning/activities/void-assault.md | CHANGED | S2 Adventurer crests |
| planning/activities/val-naigtal.md | CHANGED | crest/drop retier; World Boss frozen at S1 |
| planning/activities/world-boss.md | CHANGED | superseded by Lairs; old world-boss loot no longer upgradeable |
| planning/activities/lair-tidebound-grotto.md | **NEW** | new weekly-lockout activity, World difficulty live now |
| planning/activities/coiled-isle.md | **NEW** | new zone dailies/weeklies + Curse Surges |
| planning/activities/zuljarra-renown.md | **NEW** | new renown grind |
| planning/activities/voidcores.md | CHANGED | S1 Voidcores convert to gold; reroll cost 1; vault reward; week-8 Orin bonus; not in first S2 vault |
| planning/activities/sporefall-raid.md | CHANGED | previous-tier raid; demote priority |
| planning/activities/turbulent-timeways.md | CHANGED | **event ended 2026-08-11** — remove from ranking |
| planning/activities/showdown-weekly.md | CHANGED | verify still running post-patch |
| planning/activities/housing-weekly.md | CHANGED | 4 new Endeavors |
| planning/activities/pvp-conquest.md | CHANGED | S2 PvP not until Aug 18; Spoils of War +50% |
| planning/activities/pvp-honor.md | CHANGED | unrated only during pre-season; Training Grounds: Arenas |
| planning/activities/liadrin-spark.md | CHANGED | Crafting Sparks begin dropping in pre-season |
| planning/activities/omnium-folio.md | CHANGED | intro now account-skippable |
| planning/activities/renown-dungeon-weekly.md | CHANGED | dungeon pool changed |
| planning/activities/profession-weekly.md | CHANGED | new Coiled Isle recipes/knowledge |
| planning/activities/crafting-orders.md | RESTAMP | verify |
| planning/activities/abyss-anglers.md | CHANGED | verify vs new Venom Fishing |
| planning/activities/faction-weeklies.md | CHANGED | add Zul'jarra's Forces |
| planning/activities/midnight-campaign.md | CHANGED | new Coiled Isle campaign chapters |
| planning/activities/darkmoon-faire.md | RESTAMP | unaffected |
| planning/activities/trading-post.md | RESTAMP | monthly, volatile anyway |
| planning/candidates.json | REGEN | `wowkb.gen_candidates` after the activity edits |
| planning/{README,scoring-model,goal-model,roadmap,todo,active-characters,redesign-needs-first}.md | RESTAMP | process docs; re-stamp after a sanity read |
| planning/activities/{README,_facets}.md | RESTAMP | contract docs; may need new tags for Lairs |

### classes/ — routed by file kind, NOT swept wholesale

228 files. Most are generated or verbatim; hand-sweeping them would be both
wasteful and wrong.

| Pattern | Count | Verdict | Why |
|---|---|---|---|
| `classes/*/*/ability-inventory.md` | 40 | REGEN | `AUTO-GENERATED by wowkb.gen_abilities` — re-run against 12.1 DB2 |
| `classes/*/*/talents.md` | 40 | REGEN | generated from `_talents/all-talents.tsv`; re-pull DB2 at 12.1 first. **DH Vengeance and Havoc trees moved nodes — this is not cosmetic** |
| `classes/_talents/*`, `classes/_abilities/*.tsv`/`.json` | — | REGEN | DB2-derived data twins |
| `classes/*/*/maxroll-{raid,mplus}.md` | 12 | RECAPTURE | `verbatim: true` — re-run `wowkb.maxroll --kb`; do not hand-edit. ⚠ guide authors will not have updated on day 1 |
| `classes/*/*/sims.md` | 3 | REGEN | `wowkb.simc` — re-pull the MID1 APL at the 12.1 SHA |
| `classes/warlock/*/{rotation,builds,gearing,abilities}.md` | 12 | CHANGED | Affliction talent removals/additions + Haunt 16%; Demo Diabolist nerfs; Destro Conflagration of Chaos redesign + CDM tracking changes |
| `classes/demon-hunter/*/{rotation,builds,gearing,abilities}.md` | 12 | CHANGED | daggers equippable; Devourer mastery/damage rebalance; Havoc weapon reqs + Dash of Chaos removed + Inner Demon moved; Vengeance Sigil of Chains baseline |
| `classes/*/*/{rotation,builds}.md` (other 34 specs) | 68 | RESTAMP | only PvP snare lines changed for most; re-read and stamp, edit only where a non-PvP change lands |
| `classes/{README,_abilities/*.md,_talents/*.md}` | ~6 | RESTAMP | schema/process docs |
| `classes/warlock/demonology/diabolist-sequences.md` | 1 | CHANGED | Diabolist damage −20% across Chaos Salvo/Felseeker/Wicked Cleave/Eye Explosion |
| `classes/*/trinkets.md` | 1 | CHANGED | S2 trinkets from the new raid/dungeon pool |

### _meta/ and the rest

| KB file | Verdict | Why |
|---|---|---|
| _meta/game-version.md | CHANGED | **F8, last** — 12.1 live, pre-season state, S2 opens Aug 18 |
| _meta/next-patch.md | CHANGED | 12.1 shipped; reset to "none confirmed" or the next PTR signal |
| _meta/moving-values.md | CHANGED | crest rename, ritual-site ilvls, cache costs, vault tracks, Voidcore cost |
| _meta/feed-watermark.md | CHANGED | Step W |
| _meta/sources.md | RESTAMP | trust registry unchanged |
| _meta/quests.md | RESTAMP | verify |
| _meta/verify-in-game.md | REGEN | `wowkb.gen_verify` after markers land |
| _meta/patch-notes/*, _meta/changelog-* | — | archives; not swept |
| **knowledge/addon-dev/** (13 files) | **EXCLUDED** | separate hand pass driven by `addon-dev/12.1.0-ptr-heads-up.md` + a fresh pull of `Patch_12.1.0/API_changes`, under the addon-dev evidence rules and `wowkb.kblint` gates |
| knowledge/characters/*.md (5) | RESTAMP | volatile snapshots — re-fetch with `/sync-characters`, do not sweep |
| knowledge/economy/live-data.md | RESTAMP | pointers only |

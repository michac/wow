---
title: Affliction Warlock — talents, gearing, enchants, embellishments (Midnight S1)
patch: 12.0.7
fetched: 2026-06-19
sources:
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-spec-builds-talents  # 12.0.7
  - https://www.method.gg/guides/affliction-warlock/talents  # 12.0.7, upd. 2026-06-16
  - https://maxroll.gg/wow/class-guides/affliction-warlock-mythic-plus-guide  # 12.0.7
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-gems-enchants-consumables  # upd. 2026-05-19
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-stat-priority
  - https://murlok.io/warlock/affliction/soul-harvester/m+  # M+ usage aggregation (Blizzard API), fetched 2026-06-03 → raw/pages/
  - https://www.method.gg/guides/affliction-warlock/gearing
  - https://www.wowhead.com/news/best-early-season-crafted-gear-and-embellishments-for-all-classes-midnight-380801
  - https://www.method.gg/guides/midnight-missives-for-crafted-gear-profession-equipment  # 2026-03-04, missive names
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1
confidence: medium
---

# Affliction — talents & gearing (Midnight Season 1)

## Talents (S1, 12.0.7)

**Hero tree: Soul Harvester for everything** — ST, cleave, and pure AoE.
12.0.7 had no talent/tree rework for Affliction, but the late-S1 hotfixes
(4/23, 4/24, 5/19) buffed the spec hard, mostly in single target, and
pushed Soul Harvester to **~99% usage** (icy-veins; maxroll: "outperforms
Hellcaller in every scenario — single target, cleave or pure AoE").
Hellcaller is now a near-dead pick, only a niche long-sustained-AoE
alternative with worse ST. The build still revolves around aggressive
shard spending to recycle **Dark Harvest** (~40s burst CD when lined up
with Cull the Weak) and high **Cascading Calamity** uptime; all 4 apex
points (**Shadow of Nathreza**, Haunt-amp — top point adds a meteor
proc) are worth taking. Cast Haunt on cooldown, not just to maintain it.

Reference talent strings (12.0.7, icy-veins):
- Raid/ST (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZxxMzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjBGmZmZGzgZmZGAwMwA`
- M+/AoE (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxiZGzyAAAmZmlZzMzyYAALwAziRjZAZ2ALDAAAzAAAzMYMzMmtxYGmZmZYYmZmBAMDMA`
- Delves (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAgZmZGNLmxmZGzyAAAmZmlZZmZWGDAMLbLjhxsYmGzMDbZ2YYbAAAYGAAAzMjZGzsNGzYMzMDDzMjBAMgB`

Core spec picks (icy-veins/method/maxroll, 12.0.7):
Agony, Unstable Affliction, Seed of Corruption, Nightfall, Haunt,
Shared Agony, Improved Haunt, Drain Soul, Cunning Cruelty, Creeping
Death, Dark Harvest, Practiced Pestilence, Summon Darkglare, Summoner's
Embrace, Cull the Weak, Sudden Onset, Nether Plating, Contagion, Potent
Soul Shards, Nocturnal Yield, Ravenous Afflictions, Death's Embrace,
Shadow of Nathreza 4/4.

**Build split (12.0.7):**
- **ST/raid** leans the UA-amp cluster — **Cascading Calamity +
  Xavius' Gambit + Fatal Echoes** (method's single-target build). These
  three were "trap picks" in the 12.0.5 murlok snapshot; the S1 hotfixes
  flipped them into the recommended ST package.
- **M+/AoE** runs the Seed cluster — **Seeds of Destruction, Patient
  Zero, Sow the Seeds** to weaponize Seed of Corruption; Eye Contract is
  the AoE-lean choice-node pick.

Filler: Icy Veins recommends Improved Shadow Bolt for mobility in
dungeons; the aggregated M+ data runs Drain Soul + Cunning Cruelty.
Default to Drain Soul, treat Shadow Bolt as a personal-comfort swap.

Still trap-tier (avoid): **Withering Bolt, Malefic Grasp, Sacrolash's
Dark Strike, Malediction**.

Class tree universals (murlok): Fel Domination, Soul Leech, Burning
Rush, Demon Skin, Fel Armor, Demonic Embrace, Demonic Fortitude, Curse
of Tongues, Mortal Coil, Pact of the Annihilan, **Demonic Circle**
(50/50), Pact of the Satyr, Improved Mortal Coil (46/50), Dark Pact,
Foul Mouth, **Empowered Healthstone** (50/50), Fortified Soul, Frequent
Donor (45/50), Pact of the Eredar, Pact of the Nathrezim, Strength of
Will (42/50), Demonic Gateway, Shadowfury, Swift Artifice, Soul Link,
Oppressive Darkness, Pact of Gluttony, Soulburn, Blight of Tongues
(38/50). Fringe (<15/50): Infernal Beneficiary, Demonic Resilience,
Empowered Drain Life, Fel Synergy, Horrify, Abyss Walker.

**Pet** (with Summoner's Embrace, keep one out): DPS difference between
Felhunter / Imp / Sayaad / Voidwalker simmed **within noise** (<0.25%,
inside the 0.27% error bar — Encomplete's gear, 2026-06-03). Pick on
utility: **Felhunter** for group content (Spell Lock interrupt + purge),
**Voidwalker** for solo delves (taunt/tank), Imp for the self-dispel.

Hero choice nodes (offense vs defense, zero point cost): default to
**Friends in Dark Places**, **Shared Fate**, and **Eternal Servitude**
(method 12.0.7 default); Eternal Servitude vs Gorefiend's Resolve is the
genuine split — tank the defensive halves for a "solo delve" variant.

See `sims.md` for a measured cost of off-meta picks (Encomplete audit
was vs the 12.0.5 string: −12.7% ST / −3.9% 4T on identical gear; the
ST tuning shifted in S1 hotfixes — re-sim against the 12.0.7 build).

## Stat priority

Sources differ slightly (Icy Veins: Crit > Haste > Mastery; others lean
Mastery/Crit). Secondaries are **flat** — ilvl > stats; avoid hard
stacking. Sim on Raidbots when it matters.

### Upgrade decision rules (ilvl vs stats)

- **Tier set pieces: take/upgrade regardless of secondaries** — 2pc/4pc
  are worth several ilvls each; bad stats never outweigh them.
- **Most armor: higher ilvl wins** (int + stam scale with ilvl and
  dominate the budget; secondaries are flat for Affliction anyway).
- **Vers is lowest-throughput but not worthless** — flat damage +
  damage reduction; fine on a solo/delve-leaning character.
- **Be stat-picky only on**: rings (no primary stat — secondaries are
  the whole item), trinkets (effect > ilvl; sim), and near-ties
  (≤~6 ilvl gaps). Crafted pieces get exact stats via missive.

## Crafted gear & embellishments

- Staff: **Aln'hara Cane** — craft early; the only raid staff is off
  L'ura (Midnight Falls) and 1H+OH wastes crests.
- Popular Affliction crafts: **Martyr's Bindings** (wrist, most-used),
  **Adherent's Silken Shroud**.
- Embellishment meta: **Arcanoweave Lining ×2** (38.5% usage; proc:
  primary stat for you + ally) or **Darkmoon Sigil: Hunt + Arcanoweave
  Lining** for weapon builds.

### Missives (Method 2026-03-04)

Midnight combat missives are **Thalassian Missives** (Inscription,
AH-buyable; dual-stat, equal split). Customer slots them in the **work
order request window** as an optional reagent — buy before placing the
order. The six: Aurora (Vers/Haste), Feverflare (Mastery/Haste),
**Fireflash (Crit/Haste)**, Harmonious (Vers/Mastery), **Peerless
(Crit/Mastery)**, Quickblade (Vers/Crit).

**Affliction order: Thalassian Missive of the Peerless** (Crit/Mastery,
default) or **of the Fireflash** (Crit/Haste, Icy Veins lean) — stats
are flat, either is fine; never the Vers trio.

## Enchants (Icy Veins 2026-05-19)

| Slot | Enchant |
|---|---|
| Helm | Empowered Blessing of Speed |
| Shoulders | Akil'zon's Swiftness |
| Chest | Mark of the Worldsoul |
| Legs | Sunfire Silk Spellthread |
| Feet | Farstrider's Hunt |
| Rings | Eyes of the Eagle |
| Weapon | Acuity of the Ren'dorei (or secondary-stat enchant — sim) |
| Weapon oil | Thalassian Phoenix Oil |

All player-crafted → **all buyable on the AH**. Quality tiers exist;
quality 1–2 is much cheaper for most of the effect (budget-friendly).

## Gems

- **Epic (1 per character, unique)**: Indecipherable Eversong Diamond
  (until myth-track gear; then Powerful Eversong Diamond).
- **Rare sockets (need 4 different colors)**: Deadly Peridot / Deadly
  Lapis / Deadly Amethyst / Masterful Garnet — crit-leaning.

## Consumables

- Flask: **Flask of the Magisters** (not the generic haste flask)
- Potion: Draught of Rampant Abandon (best, but silencing pool) or
  Light's Potential (~10% weaker, no drawback — saner default)
- Food: Royal Roast / Harandar Celebration feast
- Rune: Void-Touched Augment Rune (~1%)

## TODO

- [x] Hero talent tree choice — **Soul Harvester everywhere** (resolved
      2026-06-03; Icy Veins + murlok top-50 agree, Hellcaller 0/50)
- [x] Midnight missive names resolved 2026-06-03 (Method): **Thalassian
      Missive of the Peerless** (Crit/Mastery) for Affliction
- [x] sims.md created 2026-06-03 (Encomplete talent audit baseline);
      re-sim once gear stabilizes — **audit predates 12.0.7 hotfixes
      (Xavius'/Fatal Echoes ST shift); re-sim against the 12.0.7 build**
- [x] M+ import string captured 2026-06-19 (icy-veins 12.0.7 M+/AoE
      Soul Harvester string above, Seeds-of-Destruction/Sow-the-Seeds
      variant)

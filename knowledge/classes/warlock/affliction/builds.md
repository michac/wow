---
title: Affliction Warlock — talents, gearing, enchants, embellishments (Midnight S1)
patch: 12.0.7
fetched: 2026-06-16
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/265  # Blizzard Game Data API, static-12.0.7_67808 namespace — survivability tooltips (tier 1)
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-gems-enchants-consumables  # upd. 2026-05-19
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-stat-priority
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-spec-builds-talents
  - https://murlok.io/warlock/affliction/soul-harvester/m+  # top-50 M+, tier-2-equiv (Blizzard API aggregation), fetched 2026-06-03 → raw/pages/
  - https://www.method.gg/guides/affliction-warlock/gearing
  - https://www.wowhead.com/news/best-early-season-crafted-gear-and-embellishments-for-all-classes-midnight-380801
  - https://www.method.gg/guides/midnight-missives-for-crafted-gear-profession-equipment  # 2026-03-04, missive names
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1
confidence: medium
---

# Affliction — talents & gearing (Midnight Season 1)

## Talents (S1, 12.0.5)

**Hero tree: Soul Harvester for everything** — ST, cleave, and pure AoE
(Icy Veins; murlok top-50 M+: 50/50 Soul Harvester, 0/50 Hellcaller).
Hellcaller is a niche heavy-AoE alternative with worse ST. The build
revolves around aggressive shard spending to recycle **Dark Harvest**
and high **Cascading Calamity** uptime; all 4 apex points (**Shadow of
Nathreza**, Haunt-amp) are worth taking.

Reference talent string (simc MID1 Soul Harvester, raid/ST):
`CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZZ2MzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjxwwMmZmxgZmZGAwMwA`

### In-game import strings (Icy Veins, page updated 2026-05-19; fetched 2026-06-06)

- **Single-Target — Soul Harvester** (near-identical to the MID1
  reference; differs by a couple of nodes — likely the documented
  Drain Soul vs Improved Shadow Bolt filler disagreement):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZxyMzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjBGmZmZGzgZmZGAwMwA`
- **Delves — Soul Harvester** (solo-survivability lean; the pick for
  delves/ritual sites/world):
  `CkQAAAAAAAAAAAAAAAAAAAAAAgZmZGNLmxmZGzyAAAmZmlZZmZWGDAMLbLjhxsYmGzMDbZ2YYbAAAYGAAAzMjZGzsNGzYMzMDDzMjBAMgB`

  **Intent is survivability, not DPS** (Icy Veins' own framing: "better
  defensives, plays more fluidly... short burst loops" via Haunt-triggered
  Sataiel's Volition / Quietus / Wicked Reaping — no throughput claim).
  Verified in-game 2026-06-06: drops **Drain Soul** (Shadow Bolt mobility
  filler) and **Cascading Calamity** (poor uptime when mobs die fast /
  constant target swaps), spends those points defensively. If comfortably
  surviving (overgeared, Voidwalker tanking), run the ST/M+ string with
  Drain Soul instead — faster kills are their own defense solo.
- **AoE — Hellcaller** (niche heavy-AoE; murlok top-50 M+ runs 0/50
  Hellcaller — keep for funnel/AoE curiosities only):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxiZGzyAAAmZmlZzMzyYAALwAziRjZAZ2ALDAAAzAAAzMYMzMmtxYGmZmZYYmZmBAMDMA`

⚠ Import strings are tree-version-sensitive — re-verify after 12.0.7
(2026-06-16) in case the talent trees changed.

Near-universal spec picks among top-50 M+ (murlok, 2026-06-03):
Agony, Unstable Affliction, Seed of Corruption, Nightfall, Haunt,
Shared Agony, **Improved Haunt** (50/50), Drain Soul (49/50),
Cunning Cruelty (48/50), Creeping Death, Dark Harvest, Practiced
Pestilence, Summon Darkglare, Summoner's Embrace, Cull the Weak,
Sudden Onset, Nether Plating, Contagion, Potent Soul Shards, Nocturnal
Yield, Ravenous Afflictions, Seeds of Destruction, Death's Embrace,
**Patient Zero** (48/50), **Sow the Seeds** (48/50), Shadow of
Nathreza 4/4. Eye Contract (24/50) is the AoE-lean choice-node pick.

Trap picks (≤3/50 usage): **Withering Bolt, Xavius' Gambit, Malefic
Grasp, Sacrolash's Dark Strike, Fatal Echoes, Malediction**.

Filler disagreement: Icy Veins recommends Improved Shadow Bolt for
mobility in dungeons; murlok top-50 runs Drain Soul + Cunning Cruelty
(49–48/50). Tier 2 > tier 3 — default to Drain Soul, treat Shadow Bolt
as a personal-comfort swap.

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

Hero choice nodes (offense vs defense, zero point cost): tops take
Friends in Dark Places (48/50) and Feast of Souls (44/50); Eternal
Servitude vs Gorefiend's Resolve is genuinely split (33/17). Tanking
these three is the cheap way to build a "solo delve" variant.

See `sims.md` for a measured cost of off-meta picks (Encomplete audit:
−12.7% ST / −3.9% 4T vs the reference string on identical gear).

## Survivability toolkit — heals & absorbs (12.0.7)

> Tooltips pulled live from the **Blizzard Game Data API**
> (`talent-tree/720/playable-specialization/265`, `static-12.0.7_67808`
> namespace) — tier-1, exact base values for the live patch. These are
> *base* numbers; the API does not compose talents, so improvements are
> listed under the ability they modify. Covers the **shared class tree**,
> the **Affliction spec tree**, and the **Soul Harvester** hero tree.

### Heals

| Ability | Effect | Source |
|---|---|---|
| **Drain Life** | 1,140 Shadow over 4.5s, heals **500% of damage done** (channel) | baseline |
| **Mortal Coil** | Horror (3s) + heal **20% max health**, 45s CD | class talent |
| ↳ *Improved Mortal Coil* | +10yd range, **+5% max health** (→25%) | class talent |
| **Healthstone** | Instant **25% health** restore | baseline item |
| ↳ *Empowered Healthstone* | **+5%** (→30%) | class talent |
| ↳ *Pact of Gluttony* | Healthstones become **Demonic Healthstones — reusable in combat**, 25% heal, 60s CD | class talent |
| ↳ *Gorebound Fortitude* | Consuming a Healthstone always gets Soulburn bonus: **+30% healing, +20% max HP for 12s** | **Soul Harvester** |
| **Soul Leech → heal** (*Fel Synergy*) | Soul Leech also **heals you 15% / pet 50%** of the absorb it grants | class talent |
| **Drain Life buffs** | *Gorefiend's Avarice* (channel + heal 100% faster), *Empowered Drain Life* (+200% heal & feeds Soul Leech), *Infernal Beneficiary* (also heals pet 400%) | class/spec |
| **Zevrim's Resilience** | Dark Pact also **heals 625/sec** while the shield is up | **Soul Harvester** |

### Absorbs / shields

| Ability | Effect | Source |
|---|---|---|
| **Soul Leech** | Damage grants a shield = **3% of damage dealt**, 15s, cap **5% max HP** — the core passive absorb | baseline |
| ↳ *Demon Skin* | Passively recharges Soul Leech (**0.2%/sec**), raises cap **+10% max HP**, +90% armor | class talent |
| ↳ *Fortified Soul* | Soul Leech cap **+5% max HP** | class talent |
| ↳ *Illhoof's Design* | Sacrifice 10% max HP → Soul Leech cap **+15% max HP** | **Soul Harvester** |
| ↳ *Fel Armor* | When Soul Leech absorbs, **10% of damage taken** is absorbed & spread over 5s; −3% damage taken | class talent |
| **Dark Pact** | Sacrifice 20% *current* HP → shield **200% of sacrificed HP + 950**, 20s; **usable while CC'd** | class talent |
| ↳ *Friends In Dark Places* | Dark Pact shields an **additional 50%** of sacrificed HP | **Soul Harvester** |
| ↳ *Ichor of Devils* | Dark Pact sacrifices only **5%** current HP for the **same** shield | class talent |
| ↳ *Frequent Donor* | Dark Pact **−15s CD** | class talent |
| **Soulburn → Drain Life** | Drain Life grants an absorb = healing done, 30s, cap **30% max HP** | class talent |

### Related damage reduction (not heal/absorb, but stacks the EHP)

- **Unending Resolve** — −25% damage, 8s (baseline); **Strength of Will** → −40%.
- **Soul Link** — redirect **10%** of damage taken to your pet.
- **Demonic Embrace** +10% Stamina · **Demonic Fortitude** +5% max HP.

**The big combo (per Icy Veins):** `Soulburn → Healthstone → Dark Pact` —
Soulburn/Gorebound inflate the Healthstone (and your max HP), then Dark Pact
shields off the now-higher *current* health, with Friends In Dark Places
adding +50% on top. Pact of Gluttony makes the Healthstone reusable so this
is repeatable, not a one-shot.

## Survivability / delve import string (Soul Harvester, 12.0.7)

```
CkQAAAAAAAAAAAAAAAAAAAAAAgZmZGNLmxmZGzyAAAmZmlZZmZWGDAMLbLjhxsYmGzMDbZ2YYbAAAYGAAAzMjZGzsNGzYMzMDDzMjBAMgB
```

Bakes in **Gorebound Fortitude + Friends In Dark Places + Gorefiend's
Resolve** (self-rez Soulstone). Pure ST/raid string for comparison:
`CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZxxMzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjBGmZmZGzgZmZGAwMwA`.

> Strings parsed from the Icy Veins builds page — **confirm they load as
> Soul Harvester in-game** before trusting (one bad char breaks an import).

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
      re-sim once gear stabilizes
- [x] Import strings stored 2026-06-16: survivability/delve + ST Soul
      Harvester (from Icy Veins; verify hero tree on import).
- [x] Survivability heals/absorbs table added 2026-06-16 from Blizzard
      API (static-12.0.7 tooltips); patch bumped 12.0.5 → 12.0.7 (no
      warlock spec changes in 12.0.7, confirmed via Icy Veins notes).
- [ ] M+ Eye Contract/Sow the Seeds variant import string still TODO
      from kalamazi/Archon (murlok's copy-build button is JS-only, not
      fetchable; Icy Veins ST/Delves/AoE strings already stored above).

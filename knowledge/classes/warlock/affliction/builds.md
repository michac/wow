---
title: Affliction Warlock — talents & loadouts (Midnight S1)
patch: 12.0.7
fetched: 2026-06-19
reviewed: 2026-07-14
sources:
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-spec-builds-talents  # 12.0.7
  - https://www.method.gg/guides/affliction-warlock/talents  # 12.0.7, upd. 2026-06-16
  - https://maxroll.gg/wow/class-guides/affliction-warlock-mythic-plus-guide  # 12.0.7
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/265  # Blizzard Game Data API, static-12.0.7_67808 namespace — survivability tooltips (tier 1)
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

The **delve/survivability string** above **trades DPS for defense** (Icy
Veins' own framing: "better defensives, plays more fluidly... short burst
loops" via Haunt-triggered Sataiel's Volition / Quietus / Wicked Reaping —
no throughput claim). Verified in-game 2026-06-06: it drops **Drain Soul**
(Shadow Bolt mobility filler) and **Cascading Calamity** (poor uptime when
mobs die fast / constant target swaps) to spend those points defensively.
If comfortably surviving (overgeared, Voidwalker tanking), run the ST/M+
string with Drain Soul instead — faster kills are their own defense solo.

⚠ Import strings are tree-version-sensitive. Re-verified against Icy
Veins on 2026-06-26 (post-12.0.7) — the three strings above still match
the source; re-check again if the talent trees change in a later patch.

Core spec picks (icy-veins/method/maxroll, 12.0.7) — near-universal among
top-50 M+ (murlok, 2026-06-03):
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
Resolve** (self-rez Soulstone). Pure ST/raid string for comparison
(identical to the ST — Soul Harvester string in the Talents section):
`CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZxyMzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjBGmZmZGzgZmZGAwMwA`.

> Strings parsed from the Icy Veins builds page — **confirm they load as
> Soul Harvester in-game** before trusting (one bad char breaks an import).

## Gearing

> **Moved to `gearing.md` (2026-07-14).** Stat priority + upgrade rules,
> crafted gear & embellishments, missives, enchants, gems, and consumables now
> live in `gearing.md`; trinket tiers in `gearing.md` / `trinkets.md`. This file
> is talents / loadouts / hero-tree (incl. the survivability toolkit) only.

## TODO

- [x] Hero talent tree choice — **Soul Harvester everywhere** (resolved
      2026-06-03; Icy Veins + murlok top-50 agree, Hellcaller 0/50)
- [x] Midnight missive names resolved 2026-06-03 (Method): **Thalassian
      Missive of the Peerless** (Crit/Mastery) for Affliction
- [x] sims.md created 2026-06-03 (Encomplete talent audit baseline);
      re-sim once gear stabilizes — **audit predates 12.0.7 hotfixes
      (Xavius'/Fatal Echoes ST shift); re-sim against the 12.0.7 build**
- [x] Import strings stored 2026-06-16: survivability/delve + ST Soul
      Harvester (from Icy Veins; verify hero tree on import).
- [x] Survivability heals/absorbs table added 2026-06-16 from Blizzard
      API (static-12.0.7 tooltips); patch bumped 12.0.5 → 12.0.7 (no
      warlock spec changes in 12.0.7, confirmed via Icy Veins notes).
- [x] M+ import string captured 2026-06-19 (icy-veins 12.0.7 M+/AoE
      Soul Harvester string above, Seeds-of-Destruction/Sow-the-Seeds
      variant) — resolves the earlier Eye Contract/Sow the Seeds TODO.

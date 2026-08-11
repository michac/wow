---
title: Affliction Warlock — talents & loadouts (Midnight S2 / 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" content update notes, CLASSES ▶ WARLOCK / Affliction (Tier 1)
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/265  # Blizzard Game Data API, static-12.1.0_68914 namespace — talent tooltips re-pulled 2026-08-11 (Tier 1)
  - https://us.api.blizzard.com/data/wow/spell/234153  # Drain Life, static-12.1.0_68914 (Tier 1)
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-spec-builds-talents  # updated 2026-08-10 for 12.1 (Tier 3) — import strings
  - https://www.method.gg/guides/affliction-warlock/talents  # ⚠ still 12.0.7 as of 2026-08-11
  - https://murlok.io/warlock/affliction/soul-harvester/m+  # M+ usage aggregation, fetched 2026-06-03 — SEASON 1 DATA, stale for S2
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1
confidence: medium
---

# Affliction — talents & loadouts (Midnight Season 2 / 12.1)

> Scope note: gearing moved to `gearing.md` (2026-07-14). This file is talents /
> loadouts / hero-tree, plus the survivability toolkit.
>
> **The floor for "does this talent exist" is `talents.md` / `talents.json` in
> this directory** — generated from the Blizzard Game Data API + wago `Trait*`
> DB2 at 12.1.0. If prose here disagrees with those, they win.

## 12.1 global changes that land on this spec

Four changes sit in the CLASSES preamble, above every class heading, and are
easy to miss:

1. **Player health and creature damage +25% at max level**, with health
   consumables rescaled to match. ⚠ **Every absolute HP / healing number written
   before 2026-08-11 is stale.** Percentage-of-max-health effects (Healthstone,
   Mortal Coil, Soul Leech cap, Dark Pact's sacrifice) are unaffected by
   definition; the flat numbers in the tables below were re-pulled from the live
   12.1 API on 2026-08-11.
2. **Major DPS cooldowns lowered, steady-state damage raised** across several
   specs — a stated design direction. The burst/sustained split has moved even
   where per-ability numbers look familiar.
3. **All class interrupts** now show a "missed" visual + distinct sound when
   used on a target that was not casting. (Relevant to Felhunter Spell Lock.)
4. **Diminishing-return categories reset after 20s** (was 16s).

**Warlock class-wide (12.1):**

- **Drain Life health drain +25%** — and the live tooltip's damage went up in
  step: **1,425 Shadow over 4.5s** (was 1,140), still healing **500% of damage
  done**.
- **Zevrim's Resilience healing +25%** → **781/sec** (was 625). *(Hellcaller
  talent — see the correction note in the Absorbs table.)*
- **Soul Leech correctness pass.** Now correctly grant Soul Leech: **Unstable
  Affliction**, **Malefic Grasp**, Soul Anathema, Wicked Reaping, Wither,
  Blackened Soul, Infernal Bolt, and several pet abilities.
  ⚠ **Cunning Cruelty no longer grants Soul Leech** (it did so erroneously) —
  that is a real passive-mitigation loss for a near-universal Affliction pick,
  partly offset by UA and Malefic Grasp now feeding it.
- **Summon Demonic Gateway is now a Utility spell by default in the Cooldown
  Manager.**

## Talents (S2, 12.1)

**Hero tree: Soul Harvester for everything** — ST, cleave, and pure AoE. Icy
Veins' 12.1 rewrite (2026-08-10) still calls Soul Harvester "the dominant
choice" in both single-target and AoE, and Hellcaller a worse pick with slower
gameplay. The build still revolves around aggressive shard spending to recycle
**Dark Harvest** (short burst CD when lined up with Cull the Weak) and high
**Cascading Calamity** uptime; take the **Shadow of Nathreza** apex node's
points (Haunt-amp; the top point adds a meteor proc). Cast Haunt on cooldown,
not just to maintain it — **12.1 raised Haunt's amp to +16% damage for 18s
(was 12%)**, which makes Haunt uptime worth more than it was in S1.

### What 12.1 changed in the spec tree

Verified against the generated `talents.md` @ 12.1.0 (Tier 1), not against
guide prose:

| Change | Detail |
|---|---|
| **NEW: Hedonic Gorging** (row 11, col 19) | Drain Life damage **+10%**; Siphon Life additionally increases **Corruption damage +10%**; Dark Harvest channels **10% faster** and deals **+15%** damage |
| **NEW: Impetuous Wrath** (row 9, col 21) | Shadow Bolt / Drain Soul / Malefic Grasp damage **+10%**, or **+20% against a Haunted target**; Dark Harvest likewise +10% / +20% |
| **REDESIGNED: Shard Instability** (row 9, col 15) | Shadow Bolt or Drain Soul damage has a **20% chance** to make your next **Unstable Affliction or Seed of Corruption free and instant**. (This absorbed Nocturnal Yield's free-Seed feel.) |
| **BUFF: Haunt** | **+16% damage taken for 18s** (was 12%). Live tooltip: 2,719 Shadow on impact; cooldown resets if the target dies |
| **REMOVED: Nocturnal Yield** | Gone from the tree. Blizzard's stated reason: it was always best spent on Seed of Corruption, so it wasn't a choice |
| **REMOVED: Patient Zero** | Gone from the tree. Blizzard's stated reason: it warped Seed of Corruption into priority damage and diluted its multi-target identity |

⚠ **Tooltip vs patch-note conflict (Tier 1 vs Tier 1), noted not resolved:** the
patch notes list **Drain Soul** in both Impetuous Wrath and Shard Instability;
the talent-tree API tooltip names only **Shadow Bolt** (plus Malefic Grasp /
Dark Harvest). Almost certainly because Improved Shadow Bolt and Drain Soul are
a **choice node** (row 5, col 16) and the character-agnostic tree renders the
Shadow Bolt branch. Treat the patch notes as the floor: **whichever filler you
picked is the one that procs.** Worth an in-game confirm. @verify-ingame

### Import strings (12.1, Icy Veins, updated 2026-08-10)

- Raid/ST (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZZ2mZmlxAAjllBGwEMDbBG2GAAAmBAAwMDzMjBzwMzMzMGMzMzAAmBG`
- M+/AoE (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxyMzYWGAAwMzsMLzMzyYAgxyyADYAzwWghtBAAgZAAAMzMmZY2GjZMmZmhhZmZGAwAG`
- Delves (Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxyMzYWGAAwMzsMLzMzyYAgxyyADYAzwWghtBAAgZAAAMzMmZY2GjZwMzMMMzMzAAmBG`

⚠ **The three 12.0.7 strings this file used to carry are gone and must not be
resurrected** — the tree lost two nodes and gained two, so an S1 string will
either fail to import or silently land somewhere else. These are freshly parsed
from Icy Veins' 12.1 page; **confirm they load as Soul Harvester in-game**
before trusting one (a single bad character breaks an import). @verify-ingame

Note the 12.1 Delves string is now a near-clone of the AoE string rather than
the distinct defensive build S1 had. The old S1 framing — that the delve string
drops **Drain Soul** and **Cascading Calamity** to buy defensives — was verified
in-game on 2026-06-06 **against the 12.0.7 tree** and has **not** been
re-verified for 12.1; do not restate it as current.

### Core spec picks

Near-universal in S1 (murlok top-50, 2026-06-03) and still the spine of Icy
Veins' 12.1 builds:

Agony, Unstable Affliction, Seed of Corruption, Nightfall, Haunt, Shared Agony,
Improved Haunt, Drain Soul, Cunning Cruelty, Creeping Death, Dark Harvest,
Practiced Pestilence, Summon Darkglare, Summoner's Embrace, Cull the Weak,
Sudden Onset, Nether Plating, Contagion, Potent Soul Shards, Ravenous
Afflictions, Death's Embrace, Shadow of Nathreza (apex).

⚠ **Nocturnal Yield was on this list and has been struck — it no longer
exists.** The usage percentages behind the list are **Season 1** data; no S2
aggregation exists yet on patch day.

**Build split (12.1):**

- **ST/raid** leans the UA-amp cluster — **Cascading Calamity + Xavius' Gambit +
  Fatal Echoes**, plus **Malefic Grasp** (see below). Icy Veins' 12.1 ST framing
  is unchanged from S1: spend shards aggressively to pull Dark Harvest forward
  while holding Cascading Calamity uptime.
- **M+/AoE** runs the Seed cluster — **Seeds of Destruction + Sow the Seeds**.
  **Patient Zero used to be the third pick here and is gone**; those points now
  have to go elsewhere, and the two new nodes (**Hedonic Gorging**, sitting one
  column from Sow the Seeds at row 11, and **Impetuous Wrath** at row 9) are the
  obvious candidates. Icy Veins swaps **Malefic Grasp → Eye Contract** for AoE:
  "2% more AoE but worse single-target."

**Malefic Grasp is no longer trap-tier.** This file called it a trap through
S1; 12.1 buffed it twice over (**Impetuous Wrath** gives it +10%/+20% on a
Haunted target, and it now correctly grants **Soul Leech**), and Icy Veins'
12.1 build treats it as the ST pick you swap *out* for Eye Contract in AoE.

Filler: Icy Veins' 12.1 line is that "Drain Soul shard sniping is not as
important, and instead using Shadow Bolts can offer more mobility" — a softer
stance than S1's. Both branches are buffed by Impetuous Wrath and both proc
Shard Instability, so treat this as a genuine comfort/mobility choice rather
than a DPS one.

Still trap-tier (avoid): **Withering Bolt, Sacrolash's Dark Strike,
Malediction**. ⚠ These three carry over from the S1 assessment and were **not**
re-evaluated for 12.1 — no 12.1 note touches them, but no 12.1 source ranks
them either.

Class tree universals (murlok, **S1 data**): Fel Domination, Soul Leech,
Burning Rush, Demon Skin, Fel Armor, Demonic Embrace, Demonic Fortitude, Curse
of Tongues, Mortal Coil, Pact of the Annihilan, **Demonic Circle** (50/50),
Pact of the Satyr, Improved Mortal Coil (46/50), Dark Pact, Foul Mouth,
**Empowered Healthstone** (50/50), Fortified Soul, Frequent Donor (45/50), Pact
of the Eredar, Pact of the Nathrezim, Strength of Will (42/50), Demonic
Gateway, Shadowfury, Swift Artifice, Soul Link, Oppressive Darkness, Pact of
Gluttony, Soulburn, Blight of Tongues (38/50). Fringe (<15/50): Infernal
Beneficiary, Demonic Resilience, Empowered Drain Life, Fel Synergy, Horrify,
Abyss Walker. *(All of these nodes still exist at 12.1 — verified against
`talents.md`. The class tree took no 12.1 structural changes for Warlock.)*

**Pet** (with Summoner's Embrace, keep one out): DPS difference between
Felhunter / Imp / Sayaad / Voidwalker simmed **within noise** (<0.25%, inside
the 0.27% error bar — Encomplete's gear, 2026-06-03, **S1 tuning**). Pick on
utility: **Felhunter** for group content (Spell Lock interrupt + purge),
**Voidwalker** for solo delves (taunt/tank), Imp for the self-dispel.

Hero choice nodes (offense vs defense, zero point cost): default to **Friends
in Dark Places**, **Shared Fate**, and **Eternal Servitude**; Eternal Servitude
vs Gorefiend's Resolve is the genuine split — take the defensive halves for a
"solo delve" variant. *(Defaults carried from Method's 12.0.7 guide, which is
**still on 12.0.7** as of 2026-08-11; no 12.1 note changed these nodes.)*

See `sims.md` for a measured cost of off-meta picks — ⚠ **that audit is against
the 12.0.5 string and is now two tuning passes stale**; it predates both the S1
hotfixes and the 12.1 talent shuffle. Re-sim against a 12.1 build before
quoting it.

## Survivability toolkit — heals & absorbs (12.1)

> Tooltips **re-pulled 2026-08-11** from the **Blizzard Game Data API**
> (`talent-tree/720/playable-specialization/265`, `static-12.1.0_68914`
> namespace) plus `spell/234153` for Drain Life — Tier 1, exact base values for
> the live patch. These are *base* numbers; the API does not compose talents, so
> improvements are listed under the ability they modify. Covers the **shared
> class tree**, the **Affliction spec tree**, and both hero trees.

### Heals

| Ability | Effect | Source |
|---|---|---|
| **Drain Life** | **1,425** Shadow over 4.5s, heals **500% of damage done** (channel) — *+25% in 12.1, was 1,140* | baseline |
| **Mortal Coil** | Horror (3s) + heal **20% max health**, 45s CD | class talent |
| ↳ *Improved Mortal Coil* | +10yd range, **+5% max health** (→25%) | class talent |
| **Healthstone** | Instant **25% health** restore | baseline item |
| ↳ *Empowered Healthstone* | **+5%** (→30%) | class talent |
| ↳ *Pact of Gluttony* | Healthstones become **Demonic Healthstones — reusable in combat**, 25% heal, 60s CD, not tradeable | class talent |
| ↳ *Gorebound Fortitude* | Consuming a Healthstone always gets the Soulburn bonus: **+30% healing, +20% max HP for 12s** | **Soul Harvester** |
| **Soul Leech → heal** (*Fel Synergy*) | Soul Leech also **heals you 15% / pet 50%** of the absorb it grants (rank 2) | class talent |
| **Drain Life buffs** | *Gorefiend's Avarice* (channels **and restores health** 100% faster), *Empowered Drain Life* (+200% healing **and grants Soul Leech equal to 10% of damage dealt**), *Infernal Beneficiary* (also heals your primary demon at 400% effectiveness) | class talent |
| **Zevrim's Resilience** | Dark Pact also heals **781/sec** while the shield is up — *+25% in 12.1, was 625* | **Hellcaller** |

### Absorbs / shields

| Ability | Effect | Source |
|---|---|---|
| **Soul Leech** | All **single-target** damage by you and your minions grants you and your pet a shield = **3% of damage dealt**, 15s, cap **5% max HP** — the core passive absorb | baseline |
| ↳ *Demon Skin* | Passively recharges Soul Leech (**0.2%/sec**), raises cap **+10% max HP**, +90% armor (rank 2) | class talent |
| ↳ *Fortified Soul* | Soul Leech cap **+5% max HP** | class talent |
| ↳ *Illhoof's Design* | Sacrifice 10% max HP → Soul Leech cap **+15% max HP** | **Hellcaller** |
| ↳ *Fel Armor* | When Soul Leech absorbs, **10% of damage taken** is absorbed & spread over 5s; **−3.0%** damage taken (rank 2) | class talent |
| **Dark Pact** | Sacrifice 20% *current* HP → shield **200% of sacrificed HP + 950**, 20s; **usable while CC'd** | class talent |
| ↳ *Friends In Dark Places* | Dark Pact shields an **additional 50%** of sacrificed HP | **Soul Harvester** |
| ↳ *Ichor of Devils* | Dark Pact sacrifices only **5%** current HP for the **same** shield | class talent |
| ↳ *Frequent Donor* | Dark Pact **−15s CD** | class talent |
| **Soulburn → Drain Life** | Drain Life grants an absorb = healing done, 30s, cap **30% max HP** | class talent |

> ⚠ **Correction (2026-08-11):** this file previously filed **Zevrim's
> Resilience** and **Illhoof's Design** under *Soul Harvester*. They are the
> **Hellcaller** row-3 choice node (`Zevrim's Resilience / Illhoof's Design`,
> row 3 col 24) — verified against the generated `talents.md`. Since this spec
> runs Soul Harvester everywhere, **neither is actually available in the
> recommended build**; the Soul Harvester defensives are Gorebound Fortitude /
> Friends In Dark Places, Gorefiend's Resolve, Quietus and Sataiel's Volition.

### Related damage reduction (not heal/absorb, but stacks the EHP)

- **Unending Resolve** — −25% damage, 8s, plus immunity to interrupt/silence/
  pushback (baseline); **Strength of Will** adds a further −15% (→ −40%).
- **Soul Link** — redirect **10%** of damage taken to your pet (rank 2); with
  Grimoire of Sacrifice active it instead gives **+6% Stamina**.
- **Demonic Embrace** +10% Stamina · **Demonic Fortitude** +5% max HP (you and
  pets).

**The big combo (per Icy Veins):** `Soulburn → Healthstone → Dark Pact` —
Soulburn/Gorebound inflate the Healthstone (and your max HP), then Dark Pact
shields off the now-higher *current* health, with Friends In Dark Places adding
+50% on top. Pact of Gluttony makes the Healthstone reusable so this is
repeatable, not a one-shot.

⚠ **12.1 recalibration:** with player health up 25% and creature damage up 25%,
the *percentage* toolkit above holds its relative value, but the two flat terms
(**Dark Pact's +950**, which the API shows unchanged, and Soul Leech's 3%
accrual against a bigger pool) are relatively weaker than they were in S1. The
Cunning Cruelty Soul Leech removal cuts the other way too.

## Gearing

> **Moved to `gearing.md` (2026-07-14).** Stat priority + upgrade rules, crafted
> gear & embellishments, missives, enchants, gems, and consumables live in
> `gearing.md`; trinket tiers in `gearing.md` / `trinkets.md`. This file is
> talents / loadouts / hero-tree (incl. the survivability toolkit) only.

## TODO

- [ ] **Where do the freed Patient Zero / Nocturnal Yield points go?** Decode
      the three 12.1 Icy Veins strings (or import them in-game) and write the
      exact AoE and ST node lists, instead of the reasoned-from-adjacency
      guess above. Blocked on no loadout-string decoder in `tools/`.
- [ ] **Confirm Impetuous Wrath / Shard Instability proc off Drain Soul**, not
      just Shadow Bolt — patch notes say both, the tree API tooltip says only
      Shadow Bolt. @verify-ingame
- [ ] **Verify the three 12.1 import strings load as Soul Harvester.**
      @verify-ingame
- [ ] Re-sim `sims.md` against a 12.1 build — the existing audit is a 12.0.5
      baseline and is now two tuning passes stale.
- [ ] Re-evaluate the trap-tier list (Withering Bolt, Sacrolash's Dark Strike,
      Malediction) once S2 usage data exists; the current ranking is S1-only.
- [ ] Re-capture `maxroll-raid.md` / `maxroll-mplus.md` once the author
      re-publishes — both still recommend the deleted Nocturnal Yield and
      Patient Zero (see their `kb_caveat`).
- [ ] Re-check Method's guide (`method.gg/guides/affliction-warlock/talents`)
      once it leaves 12.0.7; the hero choice-node defaults above are still
      sourced from it.
- [x] Hero talent tree choice — **Soul Harvester everywhere** (resolved
      2026-06-03; re-confirmed for 12.1 by Icy Veins 2026-08-10)
- [x] Midnight missive names resolved 2026-06-03 (Method): **Thalassian
      Missive of the Peerless** (Crit/Mastery) for Affliction — now in
      `gearing.md`
- [x] Survivability heals/absorbs table **re-pulled at 12.1** from the Blizzard
      API (2026-08-11), including the Zevrim's/Illhoof's hero-tree correction
- [x] 12.1 import strings captured 2026-08-11 (Icy Veins, updated 2026-08-10);
      the three 12.0.7 strings deleted as unimportable

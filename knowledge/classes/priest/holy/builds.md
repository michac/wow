---
title: Priest Holy — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/holy-priest/talents  # tier 3, upd. 2026-06-16
  - https://www.method.gg/guides/holy-priest  # tier 3, 2026-06-16
  - https://www.icy-veins.com/wow/holy-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - knowledge/classes/priest/holy/talents.md  # tier 1, Blizzard talent-tree API @ 12.0.7.67808
confidence: medium
---

# Priest Holy — Talents & Builds (Midnight S1)

Layered on top of the raw tree in `talents.md` (Tier-1 Blizzard talent-tree
API @ 12.0.7.67808) — that file is the node/prereq source of truth; this is the
narrative "what to pick and why." No Tier-1 simc talent string exists for Holy
(simc ships no Holy profile), so loadout guidance is **Tier-3 (method.gg +
Icy Veins)** and carries medium confidence.

## Hero tree — Archon vs Oracle (both live in S1)

Unlike most specs in S1, Holy runs **both** hero trees depending on content and
taste — neither is dead:

- **Archon** — converts Prayer of Healing into the primary throughput button.
  **Spiritwell** makes Surge of Light procs empower Prayer of Healing (not Flash
  Heal); **Energy Conservation** grants an extra **Halo** cast; **Halo** itself
  becomes a 40s cooldown feeding 4 Surge of Light procs. Best for **raid AoE and
  scripted burst windows**, and the higher-ceiling M+ AoE-damage build (pairs
  with Burning Vehemence Holy Fire cleave).
- **Oracle** — passive, consistent value via **Prayer of Mending** enhancements
  (**Guiding Light, Prompt Prognosis, Piety, Prophet's Insight**), which replace
  the old Premonition mechanic. Lower-maintenance, strong for **sustained/spread
  rot damage**. Choose it if you'd rather auto-pilot Prayer of Mending value than
  micromanage Prayer of Healing/Halo.

Rule of thumb: **Archon for burst-heavy raid + high-end AoE**, **Oracle for
smooth sustained healing**. Both share the same Holy Word core and the same
damage rotation.

## Core spec talents (near-universal)

The Holy Word engine is mandatory: **Holy Word: Serenity, Holy Word: Sanctify,
Holy Word: Chastise, Apotheosis, Divine Hymn, Prayer of Healing**. On top:

- **Benediction** (apex active, node 12,19) — take **all three baseline points**
  for a ~12% healing increase; the **4th point is optional** (adds cooldown
  potency). High priority.
- **Ultimate Serenity** (11,18) — merges Sanctify's group effect into
  **Holy Word: Serenity**, consolidating your two big Holy Words into one
  stronger heal. Core of the Archon "Serenity" build and the M+ build.
- **Lightweaver** (11,17) — Flash Heal buffs the next Prayer of Healing; strong
  but **requires management** (never cast Prayer of Healing without a stack).
- **Divine Image** (11,19) — summons a Naaru that mirrors your Holy Words;
  scales with how often you fire them.
- **Empyreal Blaze** (4,21) + **Burning Vehemence** (5,22) — turn Holy Word:
  Chastise → instant Holy Fire, and make Holy Fire cleave. This is the **M+
  AoE-damage package** (both hero trees run Burning Vehemence in M+).
- **Miracle Worker** (9,18) — a second charge / stronger Holy Word usage
  (throughput backbone).
- **Epiphany** (11,21) + **Lasting Words** (11,20) — Holy Word casts reset Prayer
  of Mending (Epiphany) and apply a free Renew (Lasting Words); another reason to
  never waste a Holy Word charge.

## Choice-node picks

- **Restitution / Guardian Angel** (4,19) — take **Restitution** (cheat-death,
  extends Spirit of Redemption) for **progression**; Guardian Angel only when the
  extra flexibility matters. method.gg's default is Restitution.
- **Eternal Sanctity / Divinity** (9,19, gates Apotheosis behavior) — take
  **Divinity** on most encounters (stronger, instant empowered Prayer of Healing
  during Apotheosis); **Eternal Sanctity** only when a longer Apotheosis duration
  is tactically better.
- **Seraphic Crescendo / Gales of Song** (7,19) — **Gales of Song** is the
  default Divine Hymn choice-node pick.
- **Dispersing Light / Trail of Light** (9,16) — Trail of Light for the extra
  smart-heal carryover (raid), situational.
- Class-tree defensives worth flagging: **Translucent Image** (Fade → ~10% DR),
  **Protective Light** (+ Binding Heals: Flash Heal grants ~10% DR),
  **Angelic Bulwark**, **Light's Inspiration**, **Improved Fade**.

## Build shapes

- **Raid — Archon:** Ultimate Serenity + Benediction + Halo/Spiritwell/Energy
  Conservation, Divinity, Restitution. Prayer of Healing is your throughput
  button; Halo before Divine Hymn/Apotheosis.
- **Raid — Oracle:** Prayer of Mending cluster (Guiding Light / Prompt Prognosis
  / Piety / Prophet's Insight) + Benediction; keep PoM on cooldown, maximize
  bounces. Lower APM.
- **M+ (either hero tree):** add **Burning Vehemence** (Holy Fire cleave) +
  Empyreal Blaze for meaningful AoE damage; **Serenity + Ultimate Serenity** for
  throughput. Archon leans the higher damage/AoE ceiling.

## Reconciliation notes (Tier-1 game data)

Seed ability names check out against `talents.md` / `SpellName.csv`:
- **Shackle Horror** (spell 9484) is the current name (the old "Shackle Undead").
- **Halo** appears twice in the Archon tree (spell 120644 / 120517) — the
  heal+damage ring; also a general talent granted at row 2 of Archon.
- **Benediction** (spell 1262755) is a Midnight apex **active** talent at spec
  node 12,19 — not the old Discipline/Disc-era passive of the same name.
- **Ultimate Serenity** (1246517), **Divine Image** (392988), **Lightweaver**
  (390992), **Empyreal Blaze** (372616), **Miracle Worker** (235587),
  **Epiphany** (414553), **Lasting Words** (471504) all confirmed present.
- "Res" = **Resurrection**; "Power Word: Fortitude" is the raid Stamina buff.

## TODO / verify

- No Tier-1 simc talent string for Holy — capture exact import strings from
  method.gg / Icy Veins per hero tree and store them here; verify they load as
  the intended hero tree in-game. @verify-ingame
- Confirm Benediction's exact mechanic (empowered Flash Heal vs Prayer-of-Mending
  bounce trigger — Tier-3 sources describe it slightly differently). @verify-ingame
- Stat priority + gearing/enchants/consumables not yet captured (Tier-3);
  add a gearing section on the next pass.

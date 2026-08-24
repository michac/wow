---
title: Valeera Sanguinar — delve companion loadout (Midnight Season 2, 12.1)
patch: 12.1
fetched: 2026-08-21
reviewed: 2026-08-21
sources:
  - https://wago.tools/db2/Spell?build=12.1.0.69214            # Tier 1 game data — every curio + poison description below, resolved from the live build (local copy: raw/wago/Spell-12.1.0.69214.csv)
  - https://us.api.blizzard.com/data/wow/spell/1248875          # Tier 1 — Corrosive Bilespear, confirms the live text against DB2
  - https://www.wowhead.com/guide/midnight/delves-season-journey-best-builds-nemesis-rewards  # Tier 3, updated 2026-08-19 (post-launch) — the option pool, and "role is a matter of personal preference"
  - https://www.wowhead.com/news/new-curios-and-poisons-choice-node-added-to-valeera-in-patch-12-1-delves-381968  # Tier 3, 2026-06-27 PTR — the poison choice-node change
  - https://www.icy-veins.com/wow/valeera-sanguinar-delve-companion-guide  # Tier 3, updated 2026-08-06 (PRE-season) — the Bilespear + Dreamcatcher recommendation
  - https://conquestcapped.com/guides/wow/midnight-delves-season-2/  # Tier 3 — S1 curios still compete; its Bilespear/Ouroboric descriptions are PTR-era and WRONG on live (see below)
confidence: medium
---

# Valeera's loadout in Season 2

A loadout is **four independent picks**: her **role** (Damage / Healer / Tank),
one **combat curio**, one **utility curio**, and one **poison**.

**The structural 12.1 change: poisons are a choice node.** In Season 1 the poison
was welded to her role — Tank meant Bloodcrypt Toxin whether it suited the run or
not. In 12.1 the poison is picked in the same menu as the curios, independent of
role. Three are available from the start; the other three unlock from the
seasonal intro questline (`Seasonal Refresher: Midnight`, quest 97454).

**Season 1 curios were not removed.** They keep dropping and compete for the same
two slots, so an S1 collection carries into S2 *(Tier 3, unverified in game)*.

## Combat curios (Season 2)

| Curio | What it does *(Tier 1, DB2 12.1.0.69214)* |
|---|---|
| **Corrosive Bilespear** (1248875) | Chance in combat to impale the highest- and lowest-health nearby targets for **tremendous Nature damage**; damage is **increased against Poisoned enemies**. Carries ranks (the live row is `Rank 4/4`). |
| **Essence Trap** (1295975) | Chance to place a trap; an enemy within 3 yds arms it, slowing enemies inside, then detonating for **moderate** Nature damage + a short stun. |
| **Ouroboric Curse** (1305629) | When any player drops below a health threshold, **Horrifies** nearby enemies and grants increased primary stat + leech/avoidance/speed. Long cooldown, **reduced by killing Poisoned enemies**. |

⚠ **A widespread Tier-3 error: the Bilespear/Ouroboric descriptions are swapped
in PTR-era guides.** Wowhead's 2026-06-27 PTR article and Conquest Capped's S2
guide both describe *Corrosive Bilespear* as a below-50%-health Horrify panic
button. That text belongs to **spell 1295761**, which on the live build carries
the **Ouroboric Curse** description; the live Corrosive Bilespear (1248875) is
the raw-damage curio above. Resolved against DB2 and the Blizzard spell endpoint
2026-08-21. If a guide says Bilespear Horrifies, it is reading PTR data.

## Utility curios (Season 2)

| Curio | What it does *(Tier 1, DB2 12.1.0.69214)* |
|---|---|
| **Soul-Cracking Dreamcatcher** (1296121) | When **any party member interrupts or crowd-controls an Elite**, that enemy takes increased damage for a while, **stacking twice**. |
| **Dundun's Favor** (1296018) | A Mislaid Spirit may appear in combat; walking over it or a Mislaid Curiosity fires Volatile Sprites at random enemies. **Curiosity contents are looted on activation.** |
| **Venom Infusion** (1305686) | The party enters combat Poisoned: takes a % of *current* health as Nature damage per minute, and gains movement speed + haste **per 5% of health missing**. Reversed for the opening seconds of combat. |

## Poisons

Available immediately (the S1 role poisons, cut loose from their roles):

- **Bloodcrypt Toxin** (1251113) — struck enemies deal reduced damage and lose Haste. *(S1 Tank poison.)*
- **Poison of the Forgotten Master** (1248501) — stacking **increased damage done**, building every few seconds in combat; **all stacks are removed when the wielder takes damage**. *(S1 DPS poison.)*
- **Soulthirst Venom** (1251862) — increased Leech, Avoidance and Speed. *(S1 Healer poison.)*

Unlocked by the intro questline:

- **Bursting Toad Toxin** (1298001) — struck enemies occasionally burst, dealing Nature damage over time to everything nearby. The **only AoE-damage poison**.
- **Frostheart Venom** (1298011) — struck enemies are slowed and have **melee, ranged and casting speed reduced**.
- **Phantasmal Spore Toxin** (1298052) — struck enemies are **interrupted and feared**.

## What the guides recommend, and how much weight it carries

The recommendation echoed across Icy Veins and the boost/SEO cluster is
**Corrosive Bilespear + Soul-Cracking Dreamcatcher**, on the claim that it is
correct for all three of her roles, with **Healer Valeera** and **Frostheart
Venom** as the safe all-purpose pick for a solo DPS player.

⚠ **This is not yet a community consensus, and should not be quoted as one.**
Season 2 opened 2026-08-18. Every source making the recommendation is a **guide
site**, several of them boost vendors; Icy Veins' page is stamped **2026-08-06**,
i.e. pre-season and PTR-sourced. **Wowhead's post-launch guide (2026-08-19)
deliberately declines to crown a build**, saying only that her role is "a matter
of personal preference". No Tier-1 or Tier-2 source ranks these, no sim models a
delve companion, and nothing published measures one curio against another.

The reasoning behind the popular pick does hold up against the Tier-1 text:
Bilespear is the only new combat curio whose payload is **damage** (the other two
are survival/CC), it scales with Poisoned targets which every poison applies, and
the Dreamcatcher's amp keys off **any party member** interrupting or CCing an
Elite — so a player who interrupts is feeding it themselves. That is an argument,
not a measurement.

## Open questions

- [ ] Do curio **ranks** (`Rank 1/4` … `4/4`) come from drops, from Valeera's
      level, or both, and does a rank-1 S2 curio beat a maxed S1 one?
      @verify-ingame
- [ ] Whether S1 curios genuinely still drop and slot in S2 — Tier 3 only.
      @verify-ingame
- [ ] Role choice at high tiers: the 12.0.7 tank-Valeera mitigation hotfix was
      never re-confirmed for 12.1's +25% health/damage retune
      (see `overview.md`). @verify-ingame

## Changelog

2026-08-21 — File created. Closes the `overview.md` TODO "Valeera upgrade path / curio equivalents in S2". All curio and poison text resolved from DB2 at the live build rather than from guide prose, which caught the swapped Bilespear/Ouroboric descriptions in the PTR-era Tier-3 guides.

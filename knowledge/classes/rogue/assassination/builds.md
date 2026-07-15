---
title: Assassination Rogue — Talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/assassination-rogue/talents  # tier 3, upd. 2026-06-16 (import strings)
  - https://www.icy-veins.com/wow/assassination-rogue-pve-dps-guide  # tier 3, 12.0.7
  - simc midnight branch profiles/MID1/MID1_Rogue_Assassination.simc  # tier 1 talent string (Deathstalker default)
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Rogue_Assassination.simc  # tier 1
confidence: medium
---

# Assassination — talents & builds (Midnight Season 1)

Layer this on top of `talents.md` / `talents.json` (the full 12.0.7 tree from
Blizzard game data — don't re-derive node lists from here).

## Hero tree: Fatebound vs Deathstalker (genuine split)

The two hero trees pull in different directions and the sources **disagree**,
so this is a real choice, not a settled meta:

- **Deathstalker** — the **simc default profile** and the higher simulated
  ceiling. Built on **Deathstalker's Mark** (auto-applied by Garrote) →
  **Darkest Night** (a supercharged 7-CP Envenom every few finishers). Adds
  Shiv usage (via Toxic Stiletto) and `Unshakeable Drive` builder tuning.
  Cost: heavy mark bookkeeping, especially on target swaps and in AoE.
- **Fatebound** — **Method's recommendation for all content**: "better in all
  circumstances… the only option for players," because Deathstalker's "quality
  of life is frankly atrocious." Fatebound is **fully passive** — 5+ CP
  finishers flip a coin whose outcomes always help (extra Envenom damage,
  Caustic Spatter boosts). No mark management.

**Practical read:** if you want maximum output and don't mind the tracking, run
**Deathstalker** (matches the simc APL in `rotation.md`). If you want a smooth,
low-APM playstyle at a small throughput cost, run **Fatebound**. @verify-ingame
(which tree leads on live 12.0.7 logs)

## Talent import strings (Method, 12.0.7, upd. 2026-06-16, Fatebound)

| Build | String |
|---|---|
| Raid | `CMQAAAAAAAAAAAAAAAAAAAAAAYmlxsZwAAAAAAzyglZAAAAAAttNzMzMzMGzMzMbzsMzMDzMzMzMMDzMAGYBmxoxsAy2A2MAYmBAG` |
| Pure single target | `CMQAAAAAAAAAAAAAAAAAAAAAAYmlxsNDGAAAAAYWGsMDAAAAAottZmZmZmxYmZmZbmlZmZwYmZmxMjhBwALwMGNmFQ2GwmBAzMzMGA` |
| Mythic+ / open world | `CMQAAAAAAAAAAAAAAAAAAAAAAYmlZmNDGAAAAAYWGsNDAAAAAottZmZmZmxYmZmZbmlZG8AzMzMjhZGjBwALwMGNmNQ2GwmxGgZGGD` |

Deathstalker reference (Tier-1, simc default profile — **use with the
`rotation.md` APL**):
`CMQAAAAAAAAAAAAAAAAAAAAAAYmZMbzgBAAAAAmlBbzAAAAAAabbmZmZmZMmZmZ2mZZmZGMmZmZMzYYAMwCMjRjZBklBsZAwMzgB`

> ⚠ Import strings are tree-version-sensitive — one bad character breaks the
> import, and the string encodes the **hero tree** too. Confirm the tree loads
> as expected in-game before trusting. Re-check if the trees change in a later
> patch. @verify-ingame

## Core talent picks & interactions (12.0.7)

**Poison / bleed engine (universal):**
- **Deadly Poison + Amplifying Poison** — the S1 lethal pair; Amplifying stacks
  are consumed by Envenom for bonus damage.
- **Deathmark** + **Kingsbane** — the burst core (see `rotation.md`); Deathmark
  duplicates bleeds/poisons, Kingsbane ramps with every poison application.
- **Venomous Wounds** took "insane nerfs" in Midnight (~25% of its old energy
  return); **Motivated Murderer** now supplies much of the passive energy regen,
  and **Thistle Tea** auto-procs energy so it barely needs pressing.

**Single-target lean:**
- **Cold Blooded Killer** — big Envenom crit boost.
- **Deeper Stratagem** — 6th/7th combo point; prevents overcap and raises
  finisher damage (enables the 7-CP Darkest Night Envenom in Deathstalker).
- **Rapid Injection** — rewards chaining Envenoms back-to-back.
- **Regicide's Reward** — added single-target damage.

**AoE / Mythic+ lean:**
- **Crimson Tempest** (reworked) — copies the longest-lasting bleeds onto
  enemies that lack them; the Midnight AoE bleed-spreader.
- **Caustic Spatter** — cleaves poisons, Envenom, and Kingsbane in a large
  radius; core M+ multiplier.
- **Thrown Precision** — Fan of Knives crit + extra poison spread.
- **Avulsion** — strengthens Rupture in multi-target.

**Apex (spec-tree capstones):**
- Apex 1: energy generation when the Envenom buff expires (rewards deliberate
  timing of the buff drop).
- Apex 4: Kingsbane enhancement — grants ~10 poison stacks and ~5 combo points
  immediately after cast. @verify-ingame (exact apex numbers)

## Poisons

- **Lethal:** Deadly Poison + Amplifying Poison (default).
- **Non-lethal (raid):** **Atrophic Poison** (target-damage reduction) unless a
  specific slow is needed.
- **Non-lethal (M+):** pick to the pull — **Crippling** (kiting), **Numbing**
  (attack-speed slow), or **Atrophic** (damage reduction).

## TODO

- [ ] Resolve hero-tree lead on live logs (simc/Deathstalker vs Method/Fatebound)
- [ ] Exact apex-talent numbers (Apex 1 energy, Apex 4 stacks/CP) — verify in-game
- [ ] Gearing / stat priority / enchants / consumables (not yet sourced — see
      Icy Veins gems-enchants + stat-priority pages and Raidbots)
- [ ] Confirm Method import strings load as Fatebound in-game

---
title: Feral Druid — talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/feral-druid/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/feral-druid-pve-dps-spec-builds-talents  # tier 3, 12.0.7, 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Druid_Feral.simc  # tier 1 talent string (Wildstalker), 2026-07-11
confidence: high
---

# Feral Druid — talents & builds (Midnight S1)

This layers on top of `talents.md` / `talents.json` (the full generated tree).
It covers **which hero tree**, **which loadout**, and the **key interactions** —
not the raw node list.

## Hero tree: it's context-dependent (unlike most specs)

Feral genuinely splits its two hero trees by content type in 12.0.7:

- **Wildstalker → raid / single-target.** DoT-centric. Rake and Rip ticks grow
  **Bloodseeker Vines** that deal bonus bleed damage and amplify finishers, and
  the **Unseen Predator** apex amplifies Rip. method.gg has it **~4% ahead of
  Druid of the Claw on all bosses**; the simc MID1 default profile is
  Wildstalker. Also carries **self-healing** (Symbiotic Bloom → instant/free
  Regrowths), which helps survivability.
- **Druid of the Claw → Mythic+ / AoE.** Auto-attacks and Berserk build
  **Ravage** procs — a cone-AoE empowered Ferocious Bite delivered through
  **Claw Rampage** — plus **Tear Down the Mighty** buffing Feral Frenzy/Chomp
  and stronger Bear-Form defensives. Still the M+ pick, though Wildstalker has
  **closed the gap** and is now viable there too (it shores up the weak
  single-target moments that deplete keys).

Rule of thumb: **Wildstalker for bosses, Druid of the Claw for dungeons** — but
either is playable in either, so pick on comfort if you don't want to swap.

## Spec-tree loadout

**Near-universal core (take in every build):**
Tiger's Fury, Feral Frenzy, **Convoke the Spirits** (over Incarnation),
**Rampant Ferocity** (AoE Ferocious Bite cleave), **Soul of the Forest**,
**Moment of Clarity**, **Lacerating Claws**, **Circle of Life and Death**,
**Focused Frenzy** (single-target) / **Frantic Frenzy** (AoE) on the Feral
Frenzy choice node, **Frantic Momentum**, **Sabertooth** (Bite extends Rip),
**Tiger's Tenacity**.

**Apex — Apex Predator's Craving:** free full-damage Ferocious Bite procs.
**Mandatory in AoE/M+** (drives multi-target Rip damage); one of the flexible
ST picks (see below).

**Raid single-target flex (~3 points, all within ~0.2% — pick to taste):**
Lunar Inspiration (third DoT + a ranged CP builder), Apex Predator's Craving,
Ashamane's Guidance (halves Convoke's CD to 1 min), or Carnivorous Instinct.

**Mythic+ / AoE priorities:** Apex Predator's Craving (mandatory) → Carnivorous
Instinct or Ashamane's Guidance for the rest; **Veinripper** (extended Rips →
more Bites) over Rip and Tear.

**Avoid (both guides):** **Chomp**, **Rip and Tear** (take Veinripper instead),
**Saber Jaws**.

## Key interactions

- **Tiger's Fury snapshot:** the backbone. Rake, Rip, Primal Wrath, Lunar
  Inspiration's Moonfire, Dreadful Wound, and Feral Frenzy's bleed all snapshot
  the +15% (and Pouncing Strikes). Refresh bleeds inside Tiger's Fury; that's
  why the rotation clips DoTs only when a stronger snapshot is available.
- **Sudden Ambush (Midnight change):** **no longer snapshots Rake** — so spend
  the proc on **Shred** (single-target) or **Swipe** (AoE), not on re-Raking.
- **Panther's Guile (Midnight):** builders can grant an extra Ferocious Bite —
  watch CP and weave the free Bite rather than double-Shredding.
- **Berserk + Overflowing Power:** Berserk lets combo points bank up to **8**,
  so a single finisher out of Berserk can be oversized; it also cheapens
  builders and drips 1 CP / 1.5s.
- **Convoke gating:** only worth its ~16 free casts inside Berserk + Tiger's
  Fury with Rip already applied — treat it as part of the burst combo, not a
  standalone CD.
- **Wildstalker Bloodseeker Vines** scale off Rake/Rip **ticks**, which is why
  bleed *uptime* (not just presence) is the Wildstalker throughput lever.
- **Druid of the Claw Ravage** needs auto-attack uptime + Berserk Swipes to
  proc — positioning/facing matters more than for Wildstalker.

## Reference talent strings (12.0.7)

> Import strings are tree-version-sensitive — **confirm the hero tree loads
> correctly in-game** before trusting (one bad char breaks the import).
> @verify-ingame

- **Raid / ST — Wildstalker (simc MID1 default):**
  `CcGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjZwMzMzMmtFPwyMbzYGzMDAAAALBzGMmZUzYWYmZGjZmZAAAAAAAGAAAABAz2MLNbzssBmZAWMDGAAzMAYA`
- **Raid / ST — Wildstalker (Icy Veins):**
  `CcGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjZwMzMzMmtlxyMbzYGzMDAAAAbBzmhxMjaGzyMzMzYMjBAAAAAgBGAAAAAgZbmlmtZW2Az8AALmBDAgZGAMA`
- **Mythic+ / AoE — Druid of the Claw (Icy Veins):**
  `CcGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMDzMzMjZmNjtZ2mZmZegZGAAAA2CmNDPgZG1MmFzMzMLjZYAAAAAAMwAAAAoZWmtZmZAALwMzAswgBAAwMbYA`

## TODO

- [x] Hero tree split — Wildstalker (raid/ST) vs Druid of the Claw (M+), 2026-07-11
- [x] Core + flex talent loadout — method.gg / Icy Veins 12.0.7, 2026-07-11
- [x] Talent strings captured (2 Wildstalker + 1 DotC), verify hero tree on import
- [ ] Gearing / stat priority / enchants / consumables — not yet sourced (see gaps)
- [ ] Re-sim flex ST points once S1 gear stabilizes (the ~0.2% spread may shift)

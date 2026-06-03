---
title: Affliction Warlock — Rotation (Midnight Season 1)
patch: 12.0.5
fetched: 2026-06-03
sources: []
confidence: low
---

# Affliction Warlock — Rotation

> **Stub.** This spec is the test case for the ingestion pipeline. Populate
> from the sources below, in tier order, and reconcile disagreements.

## Intended sources (tier order)

1. **simc APL** (tier 1): `engine/class_modules/apl/warlock.cpp` /
   `ActionPriorityLists` in the SimulationCraft GitHub repo, `midnight`
   branch — the canonical priority list.
2. **Warcraft Logs** (tier 2): top Affliction parses on Midnight S1 bosses
   via `wowkb.wcl rankings` → pull a top log's cast table and sanity-check
   the opener against the APL.
3. **Icy Veins Affliction guide** (tier 3): human-readable rotation +
   explanations: https://www.icy-veins.com/wow/affliction-warlock-pve-dps-rotation-cooldowns-abilities
4. **Warlock Discord** (tier 3): Council of the Black Harvest — for anything
   the guides lag on.

## TODO

- [ ] Single-target priority (opener + sustain)
- [ ] Multi-dot / M+ priority
- [ ] Hero talent build(s) used in S1 — which tree, why
- [ ] Cooldown usage rules (and 12.0.5 tuning changes, if any)

## Companion files (to create when populated)

- `builds.md` — talent strings (raid ST, raid cleave, M+)
- `sims.md` — stat weights / top gear sims, with sim date + simc version

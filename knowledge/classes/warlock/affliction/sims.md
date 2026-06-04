---
title: Affliction Warlock — sim baselines (Encomplete talent audit)
patch: 12.0.5
fetched: 2026-06-03
sources:
  - SimulationCraft 1205-01 (docker simulationcraftorg/simc:latest, WoW 12.0.5.67823)
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc (tier 1, commit 204b88d 2026-06-02)
confidence: high
---

# Affliction — sim baselines

## Encomplete talent audit (2026-06-03)

Setup: armory import `us,kiljaeden,encomplete` (active loadout verified
identical to `raw/blizzard/encomplete-specializations-live.json`), vs a
`copy=` of the same character with the **simc MID1 default Soul Harvester
talent string** (raid/ST reference build). Identical gear both actors
(ilvl ~236, **no enchants/gems** — as equipped). 300s Patchwerk,
`vary_combat_length=0.2`, `target_error=0.2%`.

| Scenario | Current talents | MID1 reference talents | Delta |
|---|---|---|---|
| 1 target | 52,361 DPS | 59,006 DPS | **+12.7%** |
| 4 targets | 112,054 DPS | 116,478 DPS | **+3.9%** |

Notes:

- The reference string is the **raid ST** profile; it still wins at 4
  targets. A dungeon-optimized build (Sow the Seeds, Patient Zero — see
  `builds.md`) would widen the AoE gap.
- Talent delta is isolated: gear identical across actors. Absolute DPS
  numbers are low vs top players (ilvl 236 vs ~290, zero enchants).
- Reference talent string (simc MID1, Soul Harvester):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZhhZmZmlBAAYmZZ2MzsMzAAjllBGwEMDbBG2GAAAmBAAwMDzMjxwwMmZmxgZmZGAwMwA`
- Encomplete's audited string (2026-06-03):
  `CkQAMrNP5kak+EBqLfUa3dMm+amZegZGNbmx2MzY2GAAwMzsMLmZWMDAMW2GYATwMsEYYDAAAGAAAzMjZGmlxAjZmZm5BYmZMAgZgB`

## How to reproduce

```bash
docker run --rm -v /tmp/sim:/app/SimulationCraft/sim simulationcraftorg/simc:latest \
  sim/encomplete-compare.simc apikey="$BLIZZARD_CLIENT_ID:$BLIZZARD_CLIENT_SECRET" \
  [desired_targets=4]
```

## TODO

- [ ] Re-sim after talent fix + enchants (expect both deltas to move)
- [ ] Stat weights once gear stabilizes (murlok top-50 anchor: Crit > Haste
      > Mastery > Vers; ~27% crit / 24% haste / 58% mastery at ilvl ~290)

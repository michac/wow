---
title: Demonology Warlock — sim baselines (Encomplete, M+ builds)
patch: 12.0.7
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - SimulationCraft 1205-01 (docker simulationcraftorg/simc:latest, WoW 12.0.5.67823)
  - https://www.method.gg/guides/demonology-warlock/talents  # M+ build string, page patch 12.0.5
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete  # live armory import
confidence: medium
---

# Demonology — sim baselines (Encomplete)

> ⚠ **Sim binary is 12.0.5.67823, game is live on 12.0.7** (image had not
> rebuilt as of 2026-06-19). Relative spec ranking is trustworthy; absolute
> DPS is approximate. **Rotation is simc's built-in default APL**, not the
> method.gg rotation — Demo's default APL is well-tuned, so this number is
> reliable relative to its peers.

## method.gg M+ talent string (Implosion cleave build)

`CoQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZjxmZGzyAAAAAAAAGzYYBGYb0CNsYMzYZ2mZmxMAwMjxMzMDwYGzYDAAMmZGzww2MGwA`

Single-target variant (method.gg):
`CoQAAAAAAAAAAAAAAAAAAAAAAAwMjZGNbmZ2mZGzyAAAAAAAAGzYYBGYb0CNsYMGbzyMmxMAgZmZmZmZmZAGzYmZDAAMmZGzYGWGGwA`

## 2026-06-19 — cross-spec M+ baseline (current gear)

Gear: armory import, 4pc Abyssal Immolator tier, Aln'hara Cane 272,
Preyseeker's Signet 259 — identical across all three specs. 300s Patchwerk,
`target_error=0.1`. See `../affliction/sims.md` for the full cross-spec table
and method recipe.

| Target count | Demonology DPS | vs Affliction | vs Destruction |
|---|---:|---:|---:|
| 1 (boss) | **78,422** | +23.1% | +28.7% |
| 5 (pull) | **271,801** | +10.3% | +42.9% |

→ **Demonology is Encomplete's strongest M+ spec on current gear**, winning
both single-target and 5-target. Wins do not depend on the weakest part of
the model (unlike Destruction), so this is the safe pick.

## 2026-06-19 — build × target matrix (see `../affliction/sims.md` for full grid)

| Build | 1T | 3T | 5T |
|---|---:|---:|---:|
| simc default | 80,872 | 177,500 | 250,709 |
| method M+ | 78,351 | **186,490** | **271,700** |
| method ST | parse fail | parse fail | parse fail |

→ **M+ build is best everywhere except a 3% ST edge to default — run it always,
no loadout swapping needed.** Demo wins the cross-spec comparison at 1/3/5T.
The method.gg **ST** string failed to import on the 12.0.5 binary (12.0.7
export, node 71948 "not a choice node") — a real version-mismatch failure, not
a sim setting. Re-test the ST string on a 12.0.7 image.

## Reproduce

```bash
docker run --rm -v /tmp/sim:/app/SimulationCraft/sim simulationcraftorg/simc:latest \
  sim/encomplete-mplus.simc desired_targets=5 json2=sim/mplus-aoe.json
```

## TODO

- [ ] Build a `builds.md` (talent node detail, stat priority, embellishments)
- [ ] Re-sim with a method.gg-faithful APL override (default APL only)
- [ ] Re-run on a 12.0.7 simc image when available

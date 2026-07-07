---
title: Destruction Warlock — sim baselines (Encomplete, M+ builds)
patch: 12.0.7
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - SimulationCraft 1205-01 (docker simulationcraftorg/simc:latest, WoW 12.0.5.67823)
  - https://www.method.gg/guides/destruction-warlock/talents  # M+ build string, page patch 12.0.7
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete  # live armory import
confidence: medium
---

# Destruction — sim baselines (Encomplete)

> ⚠ **Sim binary is 12.0.5.67823, game is live on 12.0.7** — relative ranking
> trusted, absolute approximate.
>
> **CORRECTION (2026-06-19, APL experiment below):** an earlier version of
> this file blamed Destruction's low AoE on the default simc APL "mishandling
> the method M+ build." That was **wrong**. A hand-authored APL translated
> from method.gg's prose scored **~3% *below* the default APL** at both 1T and
> 5T — the default is already near-optimal for this build. **The AoE deficit
> vs Demo/Aff is real, not an APL artifact.** Patchwerk still undervalues
> burst-on-pull/target-swap M+ damage, but the gap is genuine.

## method.gg M+ talent string (Hellcaller / Cataclysm build)

`CsQAAAAAAAAAAAAAAAAAAAAAAwMzDMzoZzM2mZGz2sZYmFzMLLjBAAzY2MzsYBGYWMaMDgZL2YAAgZGMDAAzMYMDmNAAAzMzMAAMDD`

Build uses Cataclysm to spread Wither in mass AoE; Hellcaller hero tree.

## 2026-06-19 — cross-spec M+ baseline (current gear)

Same gear (4pc Abyssal Immolator tier, Aln'hara Cane) and settings as the
other two specs. 300s Patchwerk, `target_error=0.1`. Tier 2pc+4pc confirmed
active; talent string imported without errors.

| Target count | Destruction DPS | vs Affliction | vs Demonology |
|---|---:|---:|---:|
| 1 (boss) | 60,953 | −4.3% | −22.3% |
| 5 (pull) | 190,177 | −22.8% | −30.0% |

→ Sims **behind both other specs** on current gear, AoE worst. Gap confirmed
real by the build-vs-APL experiment below.

## 2026-06-19 — build vs APL experiment (3 variants, Destruction only)

Question: is Destruction's low number the *build*, the *rotation (APL)*, or
the spec? Ran three self-contained profiles, identical Encomplete gear, 300s
Patchwerk, `target_error=0.1`. Files: `/tmp/sim/destro-{A,B,C}.simc`.

- **A** = simc **reference** Hellcaller build + its **reference APL**
  (`profiles/MID1/MID1_Warlock_Destruction_Hellcaller.simc`, a raid/ST profile)
- **B** = **method.gg M+** build + simc **default APL** (the cross-spec number)
- **C** = **method.gg M+** build + a **hand-authored APL** translated from
  method.gg's playstyle-and-rotation prose

| Variant | 1T (boss) | 5T (pull) |
|---|---:|---:|
| A. Ref build + Ref APL | **77,132** | 158,182 |
| B. Method build + Default APL | 60,892 | **190,178** |
| C. Method build + Hand-authored APL | 58,964 | 183,866 |

Findings:

1. **APL is not the problem (B vs C, same build).** The hand-authored APL
   scored −3.2% (1T) / −3.3% (5T) vs the default. simc's default APL already
   plays the method M+ build near-optimally (`target_if` Wither juggling,
   Havoc placement, Shadowburn targeting that prose can't capture). Lesson:
   **hand-authoring from a guide gets ~97% of the dev default at best** — use
   the default as the trustworthy baseline.
2. **Build choice dominates single-target (A vs B).** The reference ST build
   sims **+26.7% at 1T** (77.1k ≈ Demonology's 78.4k, > Affliction's 63.7k) —
   so the 61k from the M+ build at 1T was an *AoE build doing single-target*,
   not Destruction being weak at ST. That same ST build loses at 5T (it's not
   an AoE build).
3. **The M+ AoE deficit is real.** Best Destruction 5T (190k, the method M+
   build on default APL) is still well behind Demo (272k) and Aff (246k).

## 2026-06-19 — build × target matrix (see `../affliction/sims.md` for full grid)

| Build | 1T | 3T | 5T |
|---|---:|---:|---:|
| simc default (non-Hellcaller) | **80,541** | **128,071** | 169,125 |
| method M+ (Hellcaller) | 60,911 | 127,707 | **190,218** |
| method ST (Hellcaller) | 72,124 | 107,938 | 147,200 |

→ Destruction sims a **strong single-target** on the simc default build (80.5k,
≈ Demonology) but is **behind in M+ AoE** on every build. Notable: method.gg's
**ST** build (72.1k) sims *below* the simc default build at all counts — likely
because the default main MID1 profile isn't Hellcaller; verify the hero-tree
choice and the 12.0.7→12.0.5 mapping before trusting the ST string. M+ build
only leads at 5T; at 3T it ties the default ST build.

## Reproduce

```bash
# cross-spec: /tmp/sim/encomplete-mplus.simc (all 3 specs)
# build-vs-APL: /tmp/sim/destro-{A,B,C}.simc, run at desired_targets=1 and =5
docker run --rm -v /tmp/sim:/app/SimulationCraft/sim simulationcraftorg/simc:latest \
  sim/destro-C.simc desired_targets=5 json2=sim/destro-C-5.json
```

## TODO

- [x] APL fidelity tested 2026-06-19: default APL ≈ best; gap is not an artifact
- [ ] Add `builds.md`; pull a Destruction M+ import from Archon/murlok to cross-check
- [ ] If chasing Destruction ST: store the reference Hellcaller ST talent string
- [ ] Re-run on a 12.0.7 simc image when available

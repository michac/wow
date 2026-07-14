---
title: Affliction Warlock — sim baselines & gear decisions (Encomplete)
patch: 12.0.7
fetched: 2026-06-19
reviewed: 2026-07-07
sources:
  - SimulationCraft 1205-01 (docker simulationcraftorg/simc:latest, WoW 12.0.5.67823)
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc (tier 1, commit 204b88d 2026-06-02)
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete (live armory import)
  - https://www.icy-veins.com/wow/news/every-item-level-in-midnight-season-1-from-delves-to-mythic-raids/
  - https://www.method.gg/guides/new-and-updated-field-accolade-vendors-in-wow-midnight-patch-12-0-7
confidence: high
---

# Affliction — sim baselines & gear decisions

> ⚠ **Sim binary is 12.0.5.67823, game is live on 12.0.7.** The
> `simulationcraftorg/simc:latest` image had not rebuilt for 12.0.7 as of
> 2026-06-19. No notable Affliction changes between 12.0.5 and 12.0.7, so
> relative gear deltas below are trusted; re-run on a 12.0.7 image when
> available before trusting absolute DPS.

## Method — how gear enters the sim (reusable recipe)

1. **Armory import** pulls live equipped gear + talents:
   `armory=us,kiljaeden,encomplete apikey="$BLIZZARD_CLIENT_ID:$BLIZZARD_CLIENT_SECRET"`
   → one line per slot, e.g. `finger1=preyseekers_circle,id=259914,bonus_id=...`.
2. **Override one slot** on a `copy=` of the base actor to isolate a change:
   `id=` picks the item, `ilevel=` forces ilvl, `bonus_id=` applies
   sockets/tertiaries, `gems=` sockets a gem. Everything else stays identical,
   so the DPS delta is purely that slot.
3. Resolve item IDs via the Blizzard item-search API
   (`/data/wow/search/item?name.en_US=...&orderby=id:desc` — newest first;
   Midnight items are id ~240k–275k).
4. Run via docker (image already pulled):
   `docker run --rm -v /tmp/sim:/app/SimulationCraft/sim simulationcraftorg/simc:latest sim/<file>.simc`
   Use `json2=sim/out.json` and parse `players[].collected_data.dps.mean`.

Scripts/profiles live in `/tmp/sim/` (gitignored scratch). 300s Patchwerk,
`target_error=0.08–0.1`, ST (`desired_targets=1`) and AoE (`=4`) passes.

## 2026-06-19 — build × target-count matrix (all 3 specs, current gear)

3 builds per spec (simc default / method.gg M+ / method.gg ST), all on the
default APL, Encomplete gear, 300s Patchwerk, `target_error=0.1`.
Files: `/tmp/sim/matrix-{spec}.simc`.

| Spec | Build | 1T | 3T | 5T |
|---|---|---:|---:|---:|
| Affliction | simc default | 76,781 | 126,916 | 170,076 |
| | method M+ | 63,736 | 159,283 | **246,479** |
| | method ST | 76,381 | 124,956 | 167,547 |
| Demonology | simc default | **80,872** | 177,500 | 250,709 |
| | method M+ | 78,351 | **186,490** | **271,700** |
| | method ST | parse fail | parse fail | parse fail |
| Destruction | simc default | 80,541 | 128,071 | 169,125 |
| | method M+ | 60,911 | 127,707 | **190,218** |
| | method ST | 72,124 | 107,938 | 147,200 |

**Cross-spec best build per count: Demonology wins at 1/3/5T.**
1T (best ST build): Demo 80,872 > Destro 80,541 > Aff 76,781.
3T (M+): Demo 186,490 > Aff 159,283 > Destro 127,707.
5T (M+): Demo 271,700 > Aff 246,479 > Destro 190,218.

Two-loadout question (does the M+ build cost ST?):
- **Affliction: yes** — M+ build is −17% ST / +45% AoE vs its ST build. Swap for bosses.
- **Demonology: no** — M+ build within 3% of default at 1T, ahead elsewhere. One build everywhere.
- **Destruction: behind regardless** — M+ build only leads at 5T; default (non-Hellcaller) build is the ST option.

Findings:
- With proper ST builds, **Affliction is the weakest single-target of the three** (the M+-build-only table below masked this).
- **Demo ST string failed to parse** (12.0.7 export, node 71948 not a choice node on the 12.0.5 binary) — concrete version-mismatch failure.
- method.gg Destro **ST** build (72.1k) sims *below* simc's default Destro build (80.5k) at all counts — hero-tree/mapping difference, verify before trusting.

## 2026-06-19 — cross-spec M+ comparison (Aff vs Demo vs Destro, current gear)

Question: which warlock spec is Encomplete's best M+ pick on current gear?
Imported live gear once, ran three actors (one per spec) with the **method.gg
M+ talent strings**, simc's built-in default APL per spec. 300s Patchwerk,
`target_error=0.1`. File: `/tmp/sim/encomplete-mplus.simc`.

method.gg M+ strings used (fetched 2026-06-19):
- Affliction (Sow the Seeds AoE):
  `CkQAAAAAAAAAAAAAAAAAAAAAAwMjZGNbmxmZGzyAAAmZmlZzMz2YAgx22ADYCmhtADbDAAAGAAAzMjZMzsNzYGMzMzYYmZmBAMDMA`
- Demonology + Destruction strings: see each spec's `sims.md`.

| Spec | 1 target (boss) | 5 targets (pull) |
|---|---:|---:|
| **Demonology** | **78,422** | **271,801** |
| Affliction | 63,693 | 246,495 |
| Destruction | 60,953 | 190,177 |

→ **Demonology wins both** (+23% ST / +10% AoE over Affliction). Affliction
is the all-rounder. **Destruction sims worst — but its default APL is the
weakest fit for the method.gg Hellcaller build, so its gap is the least
trustworthy** (see `../destruction/sims.md`). Caveats: Patchwerk undervalues
burst/target-swap M+ damage; 12.0.5 binary (relative ranking trusted,
absolute approximate). All three confirmed 2pc+4pc Abyssal Immolator tier.

## 2026-06-18 — Great Vault pick: Preyseeker's Signet (ring) vs Astalor's Anguish Agitator (trinket)

World-row vault offered three; weapon (Preyseeker's Spire 259) skipped (had
Aln'hara Cane 272). Real choice: ring vs trinket, **take only one**.

- **Preyseeker's Signet** (id 259912, ring, 259) → replaces Preyseeker's
  Circle (246), finger1. **Has a gem socket.**
- **Astalor's Anguish Agitator** (id 264878, trinket, 259, on-use Shadow
  bolt + Leech) → replaces Void-Reaper's Libram (250), trinket1. On-use
  **is modelled** by simc (≈3 casts/fight), so not a stat-stick floor.

| Variant | ST | 4-target |
|---|---:|---:|
| Take Signet (gemmed `26stragiint`) | **+1.30%** | **+1.87%** |
| Take Agitator (trinket) | +0.78% | +0.49% |
| Current | — | — |

→ **Take the Signet (ring).** The socket was decisive: un-gemmed the ring was
~+0.1% ST (a wash vs the trinket), but a full epic gem flipped it to a clear
win at all target counts. **Decision applied in-game** (Signet now equipped).
Lesson: never compare an un-socketed slot against a socketed one.

## 2026-06-19 — Field-Accolade Hero pieces: which two slots

Buying two slot-**targeted** **Hero pieces** (**750 Field Accolades each** —
the *targeted* Maren cache where you pick the slot; the cheaper **500-accolade**
cache is the **RNG/random-slot** version. Prices confirmed in-game 2026-07-10.
Maren Silverwing, 12.0.7). Hero track floor = **259** (Hero 1/6), max **276**
(Hero 6/6). Champion track caps at **263**.

**Fair test:** a Hero piece only helps in a slot whose current item is
**Champion track or lower** — comparing Hero-max (276) against the *current
item upgraded to its own track max*, not its half-upgraded current ilvl.
Hero-track slots (head/chest/legs 272, Signet 259, waist crafted) gain nothing
from a purchase — just crest them. Per-slot value = sim(276) − sim(263):

| Slot | Budget | ST | AoE |
|---|---|---:|---:|
| hands | med (.75) | +0.61% | +0.62% |
| neck | minor | +0.56% | +0.54% |
| shoulders* | med (.75) | +0.50% | +0.62% |
| feet | med (.75) | +0.48% | +0.58% |
| back | minor | +0.42% | +0.27% |
| finger2 | minor | +0.34% | +0.62% |
| wrists | minor | +0.34% | +0.25% |

\*shoulders is Champion-maxed (263) tier piece → buy a Hero shoulder + **1
Catalyst charge** to reconvert to tier and keep the 4pc (6 charges banked).

Top four are within ~0.1% = sim noise; reliable signal is "medium-budget
Champion slots > minor slots."

→ **Buy Hands + Feet** (both medium budget, Champion-track, non-tier, no
catalyst needed). Swap Feet → **Shoulders** if willing to spend a catalyst
charge to push a tier slot (DPS-equivalent within noise). ~+1.1–1.2% combined.

**The "slot tier list" = item stat-budget multiplier** (only visible once ilvl
gap is equalised): Head/Chest/Legs (1.00) > Hands/Feet/Waist/Shoulders (0.75)
> Neck/Wrists/Rings/Back (~0.56). Weapon/trinkets are highest *impact* but
effect-driven, not budget-ranked.

### Gear baseline at analysis time (armory import 2026-06-19)

4pc Abyssal Immolator tier (head 272 / shoulders 263 / chest 272 / legs 272),
main hand Aln'hara Cane 272, Preyseeker's Signet 259 (finger1, claimed from
vault). Champion-track slots: neck 256, feet 256, hands 256, wrists 250,
back 250, finger2 253, shoulders 263 (Champion-maxed). Caveat: per-slot sims
used current items ilvl-scaled as the stat proxy; vendor pieces' actual
secondaries can shift minor slots slightly, not the budget-driven order.

## 2026-06-03 — talent audit (HISTORICAL, ilvl ~236 gear, superseded)

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

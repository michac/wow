---
title: Discipline Priest — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/discipline-priest/talents  # tier 3, 2026-07-11 (Midnight 12.0.7)
  - https://www.icy-veins.com/wow/discipline-priest-pve-healing-guide  # tier 3, 2026-07-11 (12.0.7)
  - https://www.wowhead.com/guide/classes/priest/discipline/talent-builds-pve-healer  # tier 4, 2026-07-11
  - knowledge/classes/priest/discipline/talents.md  # tier 1, Blizzard talent-tree API 12.0.7.67808
confidence: medium
---

# Discipline Priest — Talents & Builds (Midnight S1)

Layered on top of `talents.md` / `talents.json` (the full Tier-1 tree dump). This
is the *narrative*: which hero tree, which loadouts, and why. See `rotation.md`
for how the picks play out.

## Hero tree: Oracle (default) vs Voidweaver

Both are viable in 12.0.7; **Oracle is the recommended default for raid and M+**
— more consistent healing outside cooldowns, easier to pilot, and the
**Premonition** toolkit for reactive throughput/defense.

- **Oracle** — smoother baseline healing; **always uses Penance defensively**.
  M+ Oracle leans **Master the Darkness** (→ **Void Shield**, multi-target
  shield + Atonement) and **Shadow Mend** procs; Penance spreading Shadow Word:
  Pain raises Shadow Mend proc chances.
- **Voidweaver** — **Entropic Rift** (opened by **Mind Blast**), **Void Blast**,
  **Void Torrent**, plus pet damage (**Mindbender/Shadowfiend/Voidwraith**) with
  **Inescapable Torment**. Much higher group **damage** and very frequent
  "mini-ramp" windows; a strong M+ pick and bigger raid DPS contributor. Note:
  Voidweaver took a **−14% hit in 12.0.5** balancing, which is why Oracle sits as
  the safe default — re-check current tuning before committing.

## Recommended loadouts (Method, 12.0.7)

Import strings (verify they load as the intended **hero tree** in-game before
trusting — one bad character breaks the import):

- **Raid (Oracle):**
  `CAQAAAAAAAAAAAAAAAAAAAAAAADsAz2MzMYmhZbmtZmZmhZAAAAAAAAAAMDLzgZmZYGmBmpZamBYmFMEGzyAMGsAAAjxMjBzAMzMaGG`
- **Mythic+ (Oracle):**
  `CAQAAAAAAAAAAAAAAAAAAAAAAADsYwyMjZmZmhZbGzMzMDzAAAAAAAAAAYMWmBzMzYzYmBMNTMAzsghwYWGgxgFAAYMzMjBzAMzMTwA`

@verify-ingame — strings parsed from the method.gg talents page; confirm the hero
tree and no dead points before relying on them.

## Core talents (near-universal)

Across builds, method calls out: **Enduring Luminescence**, **Protector of the
Frail**, **Ultimate Penitence** (over Power Word: Barrier for damage/ramp), and
**Evangelism**, plus the **Master the Darkness** apex — take **at least 3 points**
in it for the Atonement-healing increases (it also upgrades Power Word: Shield →
**Void Shield**).

From the spec tree (`talents.md`), the throughput backbone:

- **Atonement** (baseline node) → **Power Word: Radiance**, **Power of the Dark
  Side** (empowers Penance) — the ramp core.
- **Purge the Wicked** — upgrades Shadow Word: Pain and lets **Penance spread the
  DoT**; standard in M+ for pack coverage.
- **Castigation** / **Harsh Discipline** — extra Penance bolt / reduced Penance
  CD (more of your main button).
- **Weal and Woe** — rewards **weaving shields between Penance casts** (empowers
  the next Penance / Smite); shapes the shield-between-damage cadence.
- **Evangelism** + **Ultimate Penitence** — the two ramp cooldowns.
- **Shadowfiend** → **Mindbender** (shorter-CD pet) + **Inescapable Torment**
  (Shadow Word: Death pulses the pet) + **Expiation** (SW:D consumes DoT for
  burst) — the execute/pet damage cluster.
- **Divine Aegis**, **Borrowed Time**, **Blaze of Light**, **Searing Light** —
  absorb/haste/throughput passives.

## Build differences (raid vs M+)

- **Raid** emphasizes big scheduled ramps (Evangelism + double Radiance) and, on
  **Voidweaver**, pet damage during **execute (<20%)** phases (Shadow Word: Death
  → Shadowfiend/Mindbender). Oracle raid weaves shields between Penances for
  **Weal and Woe** value.
- **Mythic+** prioritizes **shield strength + mobility** — **Power Word: Shield
  and Void Shield were both buffed ~25% in 12.0.5**, so the M+ build maximizes
  Weal and Woe with strategic shield placement, keeps **Purge the Wicked** spread
  via Penance, and (Oracle) plays around **Shadow Mend** procs. Voidweaver M+
  plays around **Atonement + Entropic Rift + Inescapable Torment** for sustained
  pack damage.

## Notes / open items

- **No SimulationCraft APL or talent profile for Discipline** (SimC ships only
  Shadow priest MID1 profiles), so there is **no Tier-1 import string** — the
  strings above are Tier-3 (method.gg). Treat build weighting as guide consensus,
  not sim-proven.
- Voidweaver's post-12.0.5 −14% nerf means the **Oracle/Voidweaver split is
  tuning-sensitive**; re-verify which is ahead on patch/hotfix days via
  method.gg + murlok/WCL usage before recommending one over the other.

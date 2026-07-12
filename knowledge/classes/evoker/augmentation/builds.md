---
title: Augmentation Evoker — talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/augmentation-evoker/talents  # tier 3, 2026-07-11 (12.0.7, import strings)
  - https://maxroll.gg/wow/class-guides/augmentation-evoker-mythic-plus-guide  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/augmentation-evoker-raid-guide  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/augmentation-evoker-pve-dps-spec-builds-talents  # tier 3, 2026-07-11
  - knowledge/classes/evoker/augmentation/talents.json  # tier 1 game data (talent tree @ 12.0.7.67808)
confidence: medium
---

# Augmentation Evoker — talents & builds (Midnight Season 1)

Layered on top of the generated talent tree in `talents.md` / `talents.json`
(Tier-1 Blizzard game data @ build 12.0.7.67808). Build narrative and import
strings are Tier-3 (method.gg / maxroll / Icy Veins, all 12.0.7). Augmentation
is a **support DPS** spec — the whole tree is bent toward keeping **Ebon Might**
and **Prescience** on allies and funnelling group damage into **Breath of Eons**
(see `rotation.md`).

## Hero tree: Scalecommander (default) vs Chronowarden

The two Augmentation hero trees are **close in throughput** — pick by content:

- **Scalecommander** — the **default and the M+ pick**. Shifts value toward
  **your own damage** via the **Bombardments** layer: empowered spells + **Mass
  Eruption** apply a stacking debuff that explodes, and **Extended Battle** pools
  for it. Wins on the multi-target encounters and in dungeon cleave. Only ~2%
  behind Chronowarden on pure single target, so it's the safe all-rounder.
- **Chronowarden** — the **single-target raid** lean (~2–3% more ST). Leans on
  **time-magic buff extension** and **Chrono Flame** (a Living-Flame filler
  replacement that synergizes with **Afterimage**); **Tip the Scales** feeds a
  **Temporal Burst** window. Plays around precise buff timing rather than a
  damage bombardment. The **Duplicate** apex copies your Ebon Might extensions
  and casts Eruption / Fire Breath / Upheaval alongside you.

Rule of thumb: **Scalecommander everywhere unless the raid fight is a strict
single-target patchwerk**, where Chronowarden edges ahead.

## Import strings (method.gg, 12.0.7)

> Tree-version-sensitive — one bad character breaks an import. **Confirm the
> hero tree loads correctly in-game** before trusting. @verify-ingame

- **Raid ST + Cleave (Chronowarden):**
  `CEcBAAAAAAAAAAAAAAAAAAAAAMmZmZbmZmxyAzsMjxwMAAAAAgBAAzMDMYM1YmZGAAAAMjZmxMzyYmBmZzAjZswCMwMM0IWwMjZGAYA`
- **Raid ST + Cleave (Scalecommander):**
  `CEcBAAAAAAAAAAAAAAAAAAAAAMmZmZbmZmxyAzsMjxwMAAAAAgBAAzMDMYM1YmZGAAAAMjZmxMzyYmBmZzYwCsMGGbDgZiYDzMwMDgB`
- **Mythic+ (Scalecommander):**
  `CEcBAAAAAAAAAAAAAAAAAAAAAMmZmZbmZmxyAzsMjxwMAAAAAAAAYmBmBjHoGzMzAAAAgZmZmxMzyYmBmZzYwCsMGGbDgZiYDzMDmZAM`

Note the two Scalecommander strings share the same class/spec spine and differ
only in the hero-tree tail — the M+ string reallocates a few spec points toward
Bombardments/Mass-Eruption AoE and Breath-of-Eons enhancement.

## Spec-tree core (near-universal)

The engine of the spec, taken in essentially every build:

- **Ebon Might** — the whole spec. Grants your primary stat to your top damage
  allies; **Eruption, Fire Breath, Upheaval, and Deep Breath extend it**. Every
  other pick exists to keep this buff rolling.
- **Prescience** + **Anachronism** / **Motes of Possibility** — Prescience buffs
  an ally (echo damage) and has a **35% chance to grant Essence Burst**; Motes of
  Possibility can auto-grant extra Prescience. This is your second maintenance
  buff and a real Essence source.
- **Eruption** + **Essence Burst** + **Ignition Rush** / **Volcanism** — Eruption
  is the signature spender (Volcanism drops its cost to 2 Essence); Essence Burst
  makes the next one free; Ignition Rush and **Momentum Shift** turn Essence Burst
  procs into throughput.
- **Breath of Eons** + **Imminent Destruction** + **Plot the Future** — the
  2-min group-burst cooldown (Temporal Wound copies a slice of buffed-ally
  damage). Imminent Destruction and Plot the Future strengthen the Breath window;
  this is where the spec's damage concentrates, so these are core.
- **Fate Mirror** / **Ricocheting Pyroclast** — extra Eruption/Living-Flame
  damage riders that feed the spender loop.
- **Defy Fate** (+ **Improved Defy Fate**) — an **Augmentation-exclusive cheat
  death**. method.gg: "a no-brainer to always go with" — its value doesn't show
  on the meter but it's taken in every serious build.

Class-tree utility staples: **Rescue** (ally mobility), **Zephyr** (group DR),
**Cauterizing Flame** (dispel), **Tip the Scales** (instant max-rank empower),
**Sleep Walk** (CC), and **Landslide**. **Spatial Paradox** vs **Time Spiral** is
the class choice node (Spatial Paradox — the haste-burst-on-an-ally — is the
usual pick).

## Scalecommander package

- **Bombardments** — empowered spells + Eruption stack a debuff that detonates;
  "makes up for a good amount of our overall damage" (method.gg). The reason
  Scalecommander does more personal damage.
- **Mass Eruption** — Eruption gains stacks you dump for AoE; **Concentrated
  Power** raises the target count. Turns Eruption into the AoE engine (the APL
  spends Eruption on the highest-Bombardment target and dumps Mass Eruption
  stacks immediately — see `rotation.md`).
- **Extended Battle** — pooling that the APL uses to bank Essence Burst before an
  empower comes off cooldown.
- **Command Squadron** — summons allies during Breath of Eons for extra burst.

## Chronowarden package

- **Chrono Flame** — replaces Living Flame as the filler; synergizes with
  **Afterimage** (stored casts replayed).
- **Temporal Burst** — a haste/throughput window fed by **Tip the Scales**.
- **Interwoven Threads** / **Tomorrow, Today** — choice node (row 13) governing
  cooldown-rate vs empower behaviour; Chronowarden's time-extension theme.
- **Duplicate** (apex) — casts Eruption / Fire Breath / Upheaval alongside you,
  and your Ebon Might extensions lengthen the duplicate's duration. The Chrono
  single-target payoff.

## Key interactions to remember

- **Everything that extends Ebon Might also extends its riders** — with the right
  talents your Ebon-Might-extension casts also lengthen **Symbiotic Bloom**,
  **Inferno's Blessing**, and (Chronowarden) the **Duplicate**. Spending Essence
  during the Ebon Might window is therefore what sustains the whole buff stack,
  not just Ebon Might itself.
- **Prescience → Essence Burst (35%)** ties buff maintenance to your resource
  economy — casting Prescience on cooldown isn't just an ally buff, it fuels
  Eruption.
- **Breath of Eons scales with what your allies do inside it** (Temporal Wound
  copies buffed-ally damage), so the build's Breath enhancers (Imminent
  Destruction, Plot the Future, Overlord) pay off only when raid cooldowns are
  stacked into the window.

## Stats & consumables (brief)

Secondary stats are on **diminishing returns**; **item level generally wins** and
hard-stacking a single secondary is discouraged. Sim on Raidbots when it matters.
Tertiaries: **Avoidance** (AoE mitigation) is the useful one; Leech/Speed are
niche. (Detailed stat weights / gems / enchants not distilled here — see the
method.gg "Stats, Races and Consumables" page. @verify-ingame for exact weights.)

## TODO / gaps

- [ ] No `MID1_Evoker_Augmentation.simc` profile in the simc midnight branch to
      cross-check talent strings against a Tier-1 loadout — strings above are
      Tier-3 (method.gg). Re-verify hero tree on import.
- [ ] Exact stat weights / gem / enchant / consumable list not distilled (only
      the DR-and-ilvl rule of thumb captured). Pull from the method.gg stats page
      or a Raidbots sim when needed.
- [ ] Confirm Scalecommander-vs-Chronowarden ST gap in current tuning (method
      says ~2%, other guides ~3%) in-game / via sim.

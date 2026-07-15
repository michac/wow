---
title: Guardian Druid — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/guardian-druid/talents  # tier 3, 12.0.7 upd. 2026-06-16 (Tactyks)
  - simc midnight branch profiles/MID1/MID1_Druid_Guardian.simc  # tier 1 talents= string, WoW 12.0.x
  - https://www.method.gg/guides/guardian-druid/playstyle-and-rotation  # tier 3, 12.0.7 (talent interactions)
  - knowledge/classes/druid/guardian/talents.md  # tier 1 tree map (Blizzard API + wago @ 12.0.7.67808)
confidence: medium
---

# Guardian Druid — Talents & Builds (Midnight S1)

Layered on top of the full tree map in `talents.md` (do not regenerate that).
Focus here: **hero-tree choice**, recommended loadouts, and the key
interactions that shape the rotation.

## Hero tree

Guardian's two hero trees are **Elune's Chosen** and **Druid of the Claw**.

- **Elune's Chosen — S1 M+ default.** "Gained a decent chunk of power thanks to
  its synergy with Thrash" (method.gg), pushing it above Druid of the Claw after
  S1 tuning. Built around **Lunar Beam** and **Moonfire**; the **Lunation**
  talent makes Lunar Beam a near-on-cooldown button (Thrash + Moonfire reduce
  its CD). Simplest, smoothest playstyle. The Tier-1 simc midnight profile ships
  an **Elune's Chosen / Lunation** build (`talents=` string below).
- **Druid of the Claw — raid-competitive, higher ceiling.** In raid "both hero
  trees are within 2–3% of each other, so play whichever you prefer"
  (method.gg), with Elune's Chosen still slightly favored post-buffs. Druid of
  the Claw adds the **Ravage** proc (empowers Maul/Swipe) and enables optional
  **catweaving / ripweaving** for more damage at the cost of complexity.

**Recommendation:** Elune's Chosen for M+ and as the default everywhere; Druid
of the Claw only if you specifically want the catweave/ripweave ceiling in raid.

## Reference talent string (Tier 1 — simc midnight, Elune's Chosen)

```
CgGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgZmxsYmZMzmZZgZbZgxMMaimZmFzMzMLjZeADAAAAgZYGLzAAAAQNzysMzMDAgFMDgFzgBsYZbAwMbwA
```

Method.gg's **Elune's Chosen M+** string (Tier 3, corroborating):

```
CgGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgZmZmlZmZMziZZGmZZZgZzwoJamZWmZmZmlxMMAAAAAgZsMDYZbmBjZZAMFAAAYDz8AALmBDMLWAYmBA
```

> ⚠ Import strings are tree-version-sensitive — one wrong character breaks the
> import. **Confirm the string loads as the intended hero tree in-game** before
> trusting it. @verify-ingame

## Key class-tree talents

- **Heart of the Wild** — reworked, ~2 min CD, effect depends on current form:
  bear → instant heal (Wild Growth-like), cat → empowers physical, moonkin →
  DoT burst. Enables the catweave/ripweave window and is a strong throughput CD.
- **Fluid Form** — instant form-shifts without wasting a global; **essential for
  catweaving** builds.
- **Dream of Cenarius** — reworked to **stack up to 4** with no internal
  cooldown; a meaningful, controllable source of off-healing (Regrowth).
- Standard defensive/utility class picks: Improved Barkskin, Thick Hide,
  Well-Honed Instincts, Ursine Vigor, Stampeding Roar (+ Improved), a CC choice
  (Incapacitating Roar / Mighty Bash), and a movement choice (Wild Charge /
  Tiger Dash).

## Key spec-tree talents

- **Thrash cluster** — Flashing Claws (more Thrash stacks), Blood Frenzy, Ursoc's
  Fury; underpins both hero trees and (via Lunation) Lunar Beam CDR.
- **Twin Moonfire + Galactic Guardian** — "extremely strong in 2+ target
  situations"; Moonfire spread + free Galactic Guardian procs. The go-to AoE
  capstone lean.
- **Red Moon** — Midnight-new capstone alternative to Twin Moonfire for **pure
  single-target**; press on CD, and Mangle on 2 charges while Red Moon is active.
- **Rend and Tear** — commonly selected, strong value (Thrash/Maul synergy).
- **Sundering Roar** (Midnight-new) — damage + armor shred, fired at high Thrash
  stacks; feeds the rage/CD economy.
- **Wild Guardian** — the row-12 capstone **active** (replaces the old **Rage of
  the Sleeper** for Guardian); a high burst-damage button, best during a Ravage
  proc (Druid of the Claw) or Lunar Beam window (Elune's Chosen). @verify-ingame
- **Incarnation: Guardian of Ursoc / Convoke the Spirits** — choice-node major
  CD (Berserk is the other side of the Incarnation split in the class/spec
  trees). Incarnation is the standard tank pick.
- **Natural Resilience** — newer defensive: converts **Frenzied Regeneration**
  overheal into an **absorb shield**. Strong for smoothing spike damage.
- **Persistence** — required if you intend to catweave while actively tanking
  (Druid of the Claw).

## Key interactions (how talents shape the rotation)

- **Lunation (Elune's Chosen):** Thrash and Moonfire reduce Lunar Beam's CD →
  Lunar Beam becomes a near-CD rotational button and Moonfire graduates from
  "maintain the DoT" to "spam as filler." This is the main reason M+ Guardians
  run Elune's Chosen.
- **Ravage (Druid of the Claw):** procs empower Maul/Swipe; consuming them is a
  rotation priority and the ideal window for **Wild Guardian**.
- **Ursoc's Guidance + After the Wildfire:** the more rage you spend, the more
  Incarnation CDR and self-healing you generate — a direct incentive to keep
  spending (Ironfur/Maul/Raze) rather than sitting near rage-cap.
- **Harnessed Rage:** offensive spends above ~80 rage raise the **Gore** proc
  chance → more Mangle resets → more rage.
- **Catweave/ripweave (Fluid Form + Heart of the Wild + Wildpower Surge):**
  optional Cat Form window for Rip/Ferocious Bite via **Feline Potential**;
  note **rage resets to 25 when shifting back to Bear Form** — dump below 25
  first. @verify-ingame

## TODO

- [x] Hero-tree choice — **Elune's Chosen** default (M+); Druid of the Claw
      raid-competitive (method.gg 12.0.7, 2026-06-16).
- [x] Tier-1 talent string captured from simc midnight profile.
- [ ] Add gearing / stat-priority / enchants section (pull Icy Veins +
      method.gg gearing pages; not in scope for this pass).
- [ ] Re-verify strings against a 12.0.7-stamped source and confirm hero-tree
      on import (@verify-ingame above).

---
title: Shadow Priest — talents & builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://github.com/simulationcraft/simc/blob/midnight/profiles/MID1/MID1_Priest_Shadow.simc  # tier 1, Voidweaver talent string, 2026-07-11
  - https://www.method.gg/guides/shadow-priest/talents  # tier 3, Midnight 12.0.7, 2026-07-11
  - https://www.method.gg/guides/shadow-priest/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
confidence: medium
---

# Shadow Priest — talents & builds (Midnight S1)

> Layers on top of `talents.md` / `talents.json` (the full Tier-1 tree dump).
> This file is the *narrative* — hero-tree choice, loadouts, key interactions.
> Don't regenerate the tree files from here.

## Hero tree: Voidweaver vs Archon (both viable in S1)

Unlike some specs, Shadow's two hero trees are **close in S1** and both see play:

- **Voidweaver** — the **default lean** (method.gg) and the shipped **simc
  profile**. First point is **Void Torrent**, which opens an **Entropic Rift**
  (AoE void field) and turns **Mind Blast into Void Blast** while the Rift is
  up. "Focuses and shines on small burst windows." Recommended raid single-target
  lean.
- **Archon** — the **consistency** pick. Built around **Halo** on cooldown to
  empower **Voidform** windows and enable **Mind Flay: Insanity** (via Surge of
  Insanity). "A much more consistent damage pattern," strong sustained AoE/cleave.

For Mythic+/AoE method.gg publishes distinct builds for **both** trees; pick by
comfort and encounter (burst vs sustained). @verify-ingame the current top-log
split before calling one strictly better.

## Reference talent string (Voidweaver, simc default)

```
CIQAAAAAAAAAAAAAAAAAAAAAAMMjZGAAAAAAAAAAAgxYxMGLzMMz2MDzw2MzYmZGbIzYxMNAzMzAABY2mtFwsxAMDwYmZGz2YGMzgZwA
```

(From `MID1_Priest_Shadow.simc`, branch `midnight`. Import strings are
tree-version-sensitive — confirm it loads as **Voidweaver** in-game before
trusting; one bad char breaks the import. method.gg's talents page also carries
per-content strings — Raid, 3-target, and M+ with Misery / Invoked Nightmare —
for both hero trees.)

## Core spec talents

The build is a DoT/Insanity skeleton (see `rotation.md`). Near-universal picks:

- **Psychic Link** — your single-target damage splashes onto all DoTed enemies.
  This is what makes "multi-dot = AoE"; it is the backbone of the spec.
- **Shadow Word: Madness** — the Insanity spender (renamed Devouring Plague).
- **Tentacle Slam** — reworked Shadow Crash; the charge-based Vampiric Touch
  spreader (6–12 targets). High-value, on-CD-ish.
- **Voidform** + a Voidform amp (see choice node below) — the burst cooldown,
  synced with Power Infusion.
- **Mind Devourer** — chance for a free/empowered Shadow Word: Madness; changes
  spender timing (fire on the proc).
- **Auspicious Spirits / Shadowy Apparitions** — apparition damage that scales
  the DoT package.
- **Shadowfiend / Mindbender / Voidwraith** + **Inescapable Torment** — the pet
  procs that fund Insanity and turn Shadow Word: Death into extra pet swings.

## Key choice-node interactions

- **Misery vs Invoked Nightmare** (3,19):
  - **Misery** — casting **Vampiric Touch also applies Shadow Word: Pain**. One
    button covers both DoTs; favors **fast-dying dungeon targets** (less setup).
  - **Invoked Nightmare** — favors **longer-lived** targets; here **Shadow Word:
    Pain becomes an active filler** (the APL hard-casts SW:P on targets living
    >12s only when Invoked Nightmare is talented).
- **Improved Voidform vs Ancient Madness** (7,19):
  - **Improved Voidform** — direct **damage bonus** during the window → burst.
  - **Ancient Madness** — **extends Voidform duration** → sustained fights.
- **Deathspeaker vs Death and Madness** (9,18): Deathspeaker widens the **Shadow
  Word: Death execute window** (the APL executes at `<20 + 15*talent.deathspeaker`
  %, i.e. sub-35% with it).
- **Devour Matter** (Voidweaver) — makes **Shadow Word: Death pop enemy absorb
  shields** for burst; the APL gives that SW:D top priority when a target is
  shielded.

## Hero-tree talent notes

**Voidweaver:**
- **Void Torrent → Entropic Rift → Void Blast** is the burst loop. Void Torrent
  wants **near-full Mastery value**; the Rift converts Mind Blast to Void Blast.
- **Void Apparitions / Maddening Tentacles** add extra Tentacle-Slam value (the
  APL presses an extra Tentacle Slam for them).
- Devour Matter / Collapsing Void round out the void-damage package.

**Archon:**
- **Halo** on cooldown drives the tree; it empowers Voidform and (via Surge of
  Insanity) turns Mind Flay into **Mind Flay: Insanity** — a hard-hitting instant
  filler. Trends toward more consistent, cleave-friendly output.

## Cooldowns & externals

- **Power Infusion** (+25% haste, 2 min) is the signature cooldown — self-cast
  synced with **Voidform**, or handed to a top-damage ally. **Twins of the Sun
  Priestess** (class tree) lets you buff an ally *and* yourself.
- **Twist of Fate** — a damage/heal buff the APL will even proc via **Holy Nova
  / Halo** healing when an ally can take the heal (niche, `heal_for_tof`).

## TODO

- [ ] Capture method.gg's exact per-content import strings (Raid / 3T / M+
      Misery / M+ Invoked Nightmare, both hero trees) once the JS page is
      scrapable — currently only the simc Voidweaver string is stored.
- [ ] Confirm the S1 top-log Voidweaver/Archon split (murlok/Archon aggregation)
      to firm up the hero-tree recommendation beyond "both viable, lean
      Voidweaver."
- [ ] Add gearing / stat priority / enchants / consumables section (mirror the
      Affliction builds.md structure) — not yet sourced this pass.

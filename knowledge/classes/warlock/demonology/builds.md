---
title: Demonology Warlock — M+ & Delve builds (Midnight S1)
patch: 12.0.5
fetched: 2026-06-13
sources:
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-spec-builds-talents  # upd. 2026-05-19, M+ import string
  - https://murlok.io/warlock/demonology/diabolist/m+  # top-player M+ aggregation (Blizzard API), fetched 2026-06-13
  - https://www.wowhead.com/guide/classes/warlock/demonology/talent-builds-pve-dps  # NotWarlock, upd. 2026-03-30
  - https://www.method.gg/guides/demonology-warlock/talents
  - https://www.kalamazi.gg/guides/demonology
confidence: medium
---

# Demonology — M+ & Delve builds (Midnight Season 1)

## TL;DR

- **Hero tree: Diabolist for M+** (the default for pushers — comparable
  single-target to Soul Harvester but clearly better AoE). Soul Harvester
  is the pure-ST/raid pick.
- **Apex: Dominion of Argus** — big Summon Demonic Tyrant buff; the whole
  spec is built around the 1-min Tyrant window.
- **Pet: Felguard** for group content (universal among top M+ players).
  Swap to **Voidwalker** for solo delves (tank/taunt).
- **Stats: Mastery ≈ Crit > Haste >> Versatility.**

## M+ build (Diabolist)

**Hero tree — Diabolist.** Consensus across Icy Veins, Wowhead, Method,
and murlok top-player aggregation: Diabolist is the better choice "at any
key level" — comparable ST while retaining superior AoE. The build is
deterministic and burst-leaning, front-loading damage through the
**Demonic Rituals → Overlord / Pit Lord** procs inside the Tyrant window.
All 14 Diabolist nodes show ~49–50/50 adoption — no real choice points.

Soul Harvester is the ST/raid alternative (passive damage via Demonic
Soul / Wicked Reaping / Soul Anathema) and has **better defensives**
overall — relevant for delves (see below).

**Spec tree near-universals (murlok top players):** Hand of Gul'dan,
Demoniac, Call Dreadstalkers, Fel Intellect, Imp-erator, Implosion,
Summon Felguard, Rune of Shadows, Demonic Brutality, Summon Demonic
Tyrant, **Dominion of Argus** (apex). Trap picks (~0 usage): Dominant
Hand, Doom, Empowered Felstorm.

**Class tree near-universals:** Fel Domination, Soul Leech, Burning Rush,
Demon Skin, Fel Armor, Demonic Embrace, Demonic Fortitude, Mortal Coil,
Pact of the Annihilan, Demonic Circle, Pact of the Satyr, Dark Pact,
Fortified Soul, Demonic Gateway, Swift Artifice, Soul Link, Pact of
Gluttony, Soulburn.

**M+-specific class swaps (vs raid):** take the AoE-utility nodes —
**Foul Mouth** (Curse of Exhaustion/Tongues/Weakness curses everything in
10 yd), **Curse of Tongues / Blight of Weakness**, **Shadowfury** (AoE
stun). Diabolist also grants a **25-sec Howl of Terror** hitting up to 10
targets — strong trash CC.

**Pet: Felguard** (universal). The Felguard, Dreadstalkers, Tyrant, and
Diabolist demon summons are a large chunk of both ST and cleave.

### M+/AoE import string (Icy Veins, upd. 2026-05-19)

```
CoQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxiZGzyAAAAAAAMWWGYADYG2CM2MmZsMmxMzMAwMzMGDwMzYmxMbAAgxMzMzYw2MDwA
```

> Paste in-game: Talents UI → Import. Verify it loads as **Diabolist**
> before keying. Pull a fresh string after any 12.0.7 talent changes.

## Stat priority

Mastery ≈ Crit > Haste >> Versatility. murlok top-player secondary
distribution: **Crit ~30% / Mastery ~34% / Haste ~22% / Vers ~1%**
(Avoidance > Leech > Speed for minors). As with Affliction, secondaries
are fairly flat — **ilvl and tier pieces win**; sim on Raidbots for
close calls. (See the Affliction `builds.md` for the shared
enchant/gem/consumable/missive meta — warlock-wide, not spec-specific.)

## Delves / solo build

Hero-tree choice is **mostly stylistic** for delves:

- **Soul Harvester** = the safer solo pick — better defensives overall:
  stronger multi-use Healthstone, **Gorebound Fortitude**, **Friends in
  Dark Places**. Good when you want to faceroll T8+ Bountiful delves.
- **Diabolist** = more burst to delete dangerous packs/bosses fast.

**Solo survivability levers** (independent of hero tree):
- **Pet: Voidwalker** for the taunt/tank and shield — standard solo swap
  off Felguard.
- Lean on **Demonic Healthstone** (reusable in combat), **Dark Pact**,
  **Soul Link**, **Mortal Coil** (heal + fear), **Burning Rush** for
  kiting. Demonology lacks an immunity/damage-reversal, so kite + pet
  threat carries solo content.

## TODO

- [ ] Re-verify vs 12.0.7 on patch day (2026-06-16) — Demo had **no**
      12.0.5 tuning changes, so this should be stable, but confirm.
- [ ] Pull a separate Soul-Harvester ST/raid import string if Encomplete
      wants a raid loadout too.
- [x] rotation.md added 2026-06-13 (ST/AoE priority, Tyrant window,
      CDM setup + Kalamazi/wago import pointers).

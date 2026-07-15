---
title: Demonology Warlock — M+ & Delve builds (talents / loadouts)  (Midnight S1)
patch: 12.0.7
fetched: 2026-07-14
reviewed: 2026-07-14
sources:
  - simc midnight branch profiles/MID1/MID1_Warlock_Demonology.simc  # tier 1 APL, commit 48103ef 2026-05-18 — default Diabolist talent hash
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-spec-builds-talents  # upd. 2026-05-19, M+ import string
  - https://murlok.io/warlock/demonology/diabolist/m+  # top-player M+ aggregation (Blizzard API), fetched 2026-06-13
  - https://www.wowhead.com/guide/classes/warlock/demonology/talent-builds-pve-dps  # NotWarlock, upd. 2026-03-30
  - https://www.method.gg/guides/demonology-warlock/talents
  - https://www.kalamazi.gg/guides/demonology
  - ../../../_meta/patch-notes/12.0.7.md  # 12.0.7 Demo changes are PvP-combat-only; no PvE build impact
confidence: high
---

# Demonology — M+ & Delve builds (Midnight Season 1)

> **Talents / loadouts / hero-tree only.** Stat priority, trinkets, tier set,
> enchants/gems/consumables now live in `gearing.md`. Rotation is in
> `rotation.md` (Tier-1 APL-distilled).

## TL;DR

- **Hero tree: Diabolist everywhere** (M+ *and* raid) — the burst tree via
  **Ruination**; maxroll has it "slightly better in (almost) all scenarios" and
  murlok top-player data agrees. Soul Harvester mechanically *emphasizes*
  Implosion/AoE and has better defensives but sims slightly behind — the
  niche/solo-defensive alternative, not the M+ default.
- **Apex: Dominion of Argus** — big Summon Demonic Tyrant buff; the whole
  spec is built around the 1-min Tyrant window.
- **Pet: Felguard** for group content (universal among top M+ players).
  Swap to **Voidwalker** for solo delves (tank/taunt).
- **Stats: Mastery ≈ Crit > Haste >> Versatility** — full detail in `gearing.md`.

## M+ build (Diabolist)

**Hero tree — Diabolist.** Consensus across Icy Veins, Wowhead, Method,
and murlok top-player aggregation: Diabolist is the better choice "at any
key level" — comparable ST while retaining superior AoE. The build is
deterministic and burst-leaning, front-loading damage through the
**Demonic Rituals → Overlord / Pit Lord** procs inside the Tyrant window.
All 14 Diabolist nodes show ~49–50/50 adoption — no real choice points.

Soul Harvester is the passive/defensive alternative (damage via Demonic
Soul / Wicked Reaping / Soul Anathema) with **better defensives** overall —
a reasonable raid-ST or delve pick, though maxroll has Diabolist edging it
even there ("slightly better in almost all scenarios"). See delves below.

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

### M+/AoE import strings

**Tier-1 (simc default APL, Diabolist, commit 48103ef 2026-05-18):**
```
CoQAAAAAAAAAAAAAAAAAAAAAAYmxMzoZjZ2mZGzyAAAAAAAAGzYYBGYb0CNsYMGLzyMzMmBAmZMzMzMDgZGzAAAYMzMjhhlZMgB
```

**Tier-3 (Icy Veins M+/AoE, upd. 2026-05-19):**
```
CoQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxiZGzyAAAAAAAMWWGYADYG2CM2MmZsMmxMzMAwMzMGDwMzYmxMbAAgxMzMzYw2MDwA
```

> Paste in-game: Talents UI → Import. Verify it loads as **Diabolist**
> before keying. The simc profile ships **only the Diabolist hash** — Soul
> Harvester is the same spec tree on the `demonic_soul` branch, so there is no
> separate simc Soul-Harvester string; pull one from a build guide (Icy
> Veins/murlok) if you want the raid/ST loadout.

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

- [x] Re-verify vs 12.0.7 (checked 2026-07-07). Confirmed stable for PvE:
      the only Demo tuning in 12.0.7 is **PvP-combat-only** (Shadow Bolt
      +200%, Demonbolt +30% in PvP; freecasting buff for PvP). No PvE
      talent/stat/hero-tree changes — M+ Diabolist build, stat priority,
      and import string below all still current.
- [ ] Pull a separate Soul-Harvester ST/raid import string if Encomplete
      wants a raid loadout too.
- [x] rotation.md added 2026-06-13 (ST/AoE priority, Tyrant window,
      CDM setup + Kalamazi/wago import pointers).

---
title: Frost Death Knight — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Death_Knight_Frost.simc  # tier 1 default talent string, fetched 2026-07-11
  - https://www.method.gg/guides/frost-death-knight/talents  # tier 3, upd. 2026-06-16
  - https://www.method.gg/guides/frost-death-knight/playstyle-and-rotation  # tier 3
  - https://www.icy-veins.com/wow/frost-death-knight-pve-dps-guide  # tier 3, 12.0.7
confidence: medium
---

# Frost Death Knight — Talents & Builds (Midnight S1)

This layers on top of `talents.md` / `talents.json` (the full 12.0.7 tree dump
from the Blizzard API + wago). It captures **which** talents S1 runs and **why**,
not the raw tree.

## The two axes

Frost's build space is two independent choices:

1. **Hero tree**: **Deathbringer** (Reaper's Mark → Exterminate) vs **Rider of
   the Apocalypse** (summon the Four Horsemen).
2. **Rune-spending engine**: **Breath of Sindragosa** (sustained Runic-Power
   cone) vs **Obliteration** (a Pillar-of-Frost burst weave).

## Recommended builds (12.0.7)

### Raid / single target — Deathbringer + Breath of Sindragosa

This is the **simc default profile** and method's raid recommendation.

```
CsPAAAAAAAAAAAAAAAAAAAAAAMDwMjZMDY2mZmZmZZmZkZMmZYGGPgZGMzMzMDAAAAAAAAAjZbgBsAWGmQGLYmxMzAzAYYmBYmBD
```
(simc MID1_Death_Knight_Frost.simc = method "Raid Breath of Sindragosa" string —
they match exactly.)

- **Deathbringer** applies **Reaper's Mark**; when it detonates you gain
  **Exterminate** charges that empower and cheapen Obliterate/Frostscythe. The
  mark is timed just before **Pillar of Frost** so the burst stacks.
- **Breath of Sindragosa** costs 60 Runic Power to open and then drains RP,
  dealing frontal AoE; it **extends up to ~30s** by consuming Killing Machine /
  Rime. Always paired with Pillar. This is the "frantic proc-focused" playstyle —
  you pool RP into each Pillar window, open Breath, then keep the proc engine fed.

### Mythic+ / AoE — Rider of the Apocalypse + Frostbane / Obliteration

Method's M+ recommendation; the murlok/aggregate lean.

```
CsPAAAAAAAAAAAAAAAAAAAAAAYAzMjZmZAz2MzMzMLmZkZMGmZGGzMwMzMzMDAAAAAAAAAjZbgBsAWGmQGLYmZmZGYGADzMAzAD
```
(method "M+ Frostbane" string.)

- **Rider of the Apocalypse** summons the Horsemen (Mograine, Whitemane,
  Trollbane, Nazgrim). **Frostwyrm's Fury** brings them out *immediately* after
  Pillar so they inherit its Strength buff; **Trollbane's Icy Fury** scales with
  Mastery and slows, and the rotation target-swaps onto the Trollbane-slowed
  enemy.
- **Frostbane** powers the cleave — you track and burst **Razorice** stacks.
  **Obliteration** turns the Pillar window into a Killing-Machine weave
  (Frost Strike / Glacial Advance / Howling Blast each proc Killing Machine while
  Pillar is up), giving predictable Obliterate/Frostscythe crits.

> Note: method's talents page frames the split as **Deathbringer=raid/ST,
> Rider=M+/AoE**, and separately **Breath=raid engine, Frostbane/Obliteration=M+
> engine**. The two axes are chosen together per the strings above. The
> Deathbringer+Breath vs Rider+Obliteration pairing is the common S1 convention;
> mixed pairings exist but are off-default. @verify-ingame current top-key /
> top-parse pairing once S1 logs stabilize.

## Key talents & interactions

- **Killing Machine** (passive proc engine) → **Obliterate** / **Frostscythe**
  guaranteed crits. Everything funnels here.
- **Rime** → free empowered **Howling Blast**; **Rage of the Frozen Champion**
  and **Frostbound Will** raise Rime value/priority.
- **Shattering Blade** — at 5 **Razorice**, **Frost Strike** consumes the stacks
  for a big hit (a distinct ST priority line).
- **Gathering Storm** — **Remorseless Winter** stacks a growing AoE buff; drives
  the AoE cooldown line and a 1-target Remorseless Winter usage.
- **Enduring Strength / Icy Onslaught / Bonegrinder** — Pillar-window damage
  amps; Bonegrinder rank 2 gives a Frost-damage buff that influences Frostwyrm's
  Fury timing (`fwf_buffs`).
- **Chosen of Frostbrood** / **Apocalypse Now** — capstones that tie Frostwyrm's
  Fury into the burst window (the APL fires FWF differently when either is
  talented). @verify-ingame Chosen of Frostbrood exact effect (Midnight-era)
- **Exterminate** (Deathbringer) — post-Reaper's-Mark charges that empower and
  reduce the rune cost of your spenders.
- **Empower Rune Weapon + Runic Attenuation / Runic Overflow / Murderous
  Efficiency** — the rune/RP sustain package that keeps the proc loop fed.

## Runeforges & pet

- **Weapons**: **Razorice** (mainhand for the stacking debuff the rotation
  burns) + **Fallen Crusader** (offhand / 2H) is the standard S1 pairing.
  @verify-ingame confirm current-patch runeforge meta.
- **Pet**: **Raise Dead** ghoul baseline; **Rider of the Apocalypse** adds the
  Horsemen as its damage identity.

## Stat priority

Frost secondaries are close and gear-dependent — **ilvl generally wins**; sim on
Raidbots when it matters. Mastery is emphasized by the Rider/Trollbane build
(Trollbane's Icy Fury scales with Mastery); Crit/Haste feed the Killing
Machine / auto-attack proc density. @verify-ingame precise S1 stat weights per
build (Breath vs Obliteration differ) via Raidbots.

## TODO

- [x] Hero-tree + engine axes — Deathbringer/Rider × Breath/Obliteration
- [x] Import strings — simc default (raid Breath) + method M+ Frostbane, 2026-07-11
- [ ] Confirm live top-key / top-parse build pairing once S1 logs stabilize
- [ ] Exact S1 stat weights per build (Raidbots) — currently ilvl-first heuristic
- [ ] Enchants / gems / consumables / crafted gear (mirror the Affliction
      builds.md gearing section) — not yet sourced for Frost DK

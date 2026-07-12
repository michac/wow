---
title: Beast Mastery Hunter — talents & builds (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-12
reviewed: 2026-07-12
sources:
  - simc midnight branch profiles/MID1/MID1_Hunter_Beast_Mastery.simc  # tier 1 talent string
  - https://www.method.gg/guides/beast-mastery-hunter/talents  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/beast-mastery-hunter-pve-dps-guide  # tier 3, 12.0.7
confidence: medium
---

# Beast Mastery — talents & builds (Midnight S1, 12.0.7)

Layers on top of `talents.md` / `talents.json` (the full tree with spell IDs).
This file is the narrative: which hero tree, which spec clusters, and why.

## Hero tree: Pack Leader (default), Dark Ranger (alt ST)

**Pack Leader is the recommended tree for both single-target/raid and
AoE/Mythic+** (method.gg, 12.0.7). It's the straightforward, high-uptime beast
build:

- **Howl of the Pack Leader** runs a 30s timer, ticked down by **Cobra Shot**
  and **Kill Command**. When it hits 0 your next Kill Command deals bonus damage
  and **summons the next beast** in a rotating cast (**Wyvern → Boar → Bear**),
  each with its own damage/utility effect.
- **Bestial Wrath also arms Howl instantly**, and the **first Kill Command
  inside Bestial Wrath fires a Stampede** — a stationary ~40-yard beast line
  that hammers everything inside it for ~7s. Aim it through where mobs will be.
- Supporting picks: **Pack Mentality**, **Dire Summons**, **Better Together**,
  **Fury of the Wyvern**, **Hogstrider** (Cobra Shot cleave proc at <4 targets),
  **Stampede!**.

**Dark Ranger** is the alternative single-target line. It adds **Black Arrow**
(a Deathblow-triggering shadow shot) and a **Withering Fire** window opened by
Bestial Wrath during which Black Arrow is spammable at tripled damage;
**Wailing Arrow** guarantees a **Deathblow** reset. Supporting picks:
**Withering Fire**, **Bleak Powder**, **Blighted Quiver**, **Banshee's Mark**.
Slightly higher burst ST, a touch more to manage than Pack Leader.

## Spec-tree core (both hero trees)

The Midnight redesign centres three reworked buttons — the guide-highlighted
changes:

- **Barbed Shot** is now a **rolling/stacking bleed** (stacks damage rather
  than just refreshing duration), so it's meaningful ST throughput, not only a
  Frenzy/Focus tool. Two charges; keep them off cap.
- **Cobra Shot** got real damage talents — it's a genuine filler, not dead
  weight, and it ticks the Howl timer.
- **Wild Thrash** **replaces Multi-Shot** as the AoE spender and the **Beast
  Cleave** enabler.
- **Bestial Wrath** is a **static 30s cooldown** with **+20% damage** (down from
  30%) plus a burst on activation — the redesign's anchor.

Near-universal spec picks (method/icy-veins, mirrored in the simc profile):
**Kill Command, Barbed Shot, Cobra Shot, Bestial Wrath, Wild Thrash**, plus
**Alpha Predator** (2-charge Kill Command), **Dire Beast** + **Dire Command** /
**Dire Cleave**, **Scent of Blood**, **Go for the Throat**, **Training Expert**,
**The Beast Within**, **Thrill of the Hunt**, **Pack Tactics** (instant Focus on
Barbed Shot), **Frenzy** / **Dire Frenzy**, **Killer Instinct**, **Bloodshed**
(passive in Midnight), **Savagery**, and the AoE cluster
(**Beast Cleave**, **Kill Cleave**).

**Choice-node / build-defining picks:**
- **Animal Companion vs Solitary Companion** — a permanent second pet vs a
  buffed single pet. Animal Companion is the common AoE/cleave pick.
- **Wild Instincts vs Bloody Frenzy** (spec capstone choice, 11,18) — the simc
  profile and Dark Ranger ST list lean on **Bloody Frenzy** (with Snakeskin
  Quiver + Jagged Wounds); Wild Instincts is the Pack Leader / Wild Thrash lean.
  @verify-ingame (current best per hero tree)
- **Killer Cobra** — makes Cobra Shot reset Kill Command during Bestial Wrath
  (Dark Ranger ST leans on it: `talent.killer_cobra&buff.bestial_wrath.up`).
- **Master Handler** — lets Kill Command be pressed in AoE without waiting on the
  Nature's Ally proc (`buff.natures_ally.react|talent.master_handler`).
- **Serpentine Strikes** / **Snakeskin Quiver** — change how greedily Barbed
  Shot is pressed in the ST list.
- **Nature's Ally** (12,18 capstone active) — grants the empowerment buff Kill
  Command keys off.

## Reference talent string (Tier 1)

From the simc midnight `MID1_Hunter_Beast_Mastery.simc` profile (the default,
Pack-Leader-flavoured build):

```
C0PAAAAAAAAAAAAAAAAAAAAAAAMmxwCsBzwQDbAAYG2GzsNzwMmZYYmxYmxMzYGzwMzYGzgx0MAAAAAmBAAgxMzMgZ2AbwsA2GA
```

method.gg publishes four import strings — **Pack Leader ST/Raid**, **Pack
Leader AoE/M+**, **Dark Ranger ST/Raid**, **Dark Ranger AoE/M+** — grab those
from the talents page for scenario-exact loadouts. @verify-ingame (confirm the
string loads as the intended hero tree before trusting an import).

## Single-target vs AoE build split

- **Single target** maximizes Barbed Shot (rolling bleed) + Cobra Shot damage;
  Dark Ranger with the Bloody Frenzy / Killer Cobra cluster is the burst-ST
  alternative to Pack Leader.
- **AoE / M+** leans **Wild Thrash + Beast Cleave** coverage (**Beast Cleave,
  Kill Cleave, Dire Cleave**) and Animal Companion; Pack Leader's Stampede is
  strong sustained multi-target.

## Pet

Keep a pet out at all times (dead pet = a large DPS loss). Family choice is
mostly utility — pick for the group buff / Bloodlust (**Primal Rage / Ancient
Hysteria** on the right families) and CC needs; the raw DPS between families is
close. @verify-ingame (S1 best-pet-family consensus)

## Stat priority

Beast Mastery in Midnight favours **Mastery** and **Haste** with **Crit**,
Versatility lowest — the simc profile is Mastery-heaviest (mastery 1057 >
haste 827 > crit 531 > vers 84 rating). Secondaries are relatively flat; **ilvl
generally wins** and you should sim on Raidbots for close calls. @verify-ingame
(precise S1 stat order)

## TODO

- [ ] Capture method.gg's four exact import strings (Pack Leader / Dark Ranger
      × ST / AoE) once the JS-rendered talents page can be parsed.
- [ ] Confirm Wild Instincts vs Bloody Frenzy per hero tree, and the S1 pet /
      stat consensus (Raidbots + murlok aggregation).
- [~] Talent string above is the Tier-1 simc default (pulled 2026-07-12); swap
      for a dated 12.0.7 published profile when one lands.

---
title: Vengeance Demon Hunter — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/vengeance-demon-hunter/talents  # tier 3, Midnight 12.0.7, upd. 2026-06-16
  - https://www.method.gg/guides/vengeance-demon-hunter  # tier 3, 12.0.7 intro / hero-tree framing
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Vengeance.simc  # tier 1, talents=CUkAAAAAAAAAAAAAAAAAAAAAAAAYMzMjhZkZmZGDzMzMDGzMmxMmhxMmZsMmZZMmBAAAAAAAgZmxGAAAAGYmZmZ2abmZGAYAAAAMA (Annihilator)
  - https://www.icy-veins.com/wow/vengeance-demon-hunter-pve-tank-spec-builds-talents  # tier 3, 12.0.7
  - https://wowcarry.com/blog/wow/wow-news/vengeance-demon-hunter-in-midnight-talents-annihilator-guide  # tier 4, Annihilator/Apex corroboration
confidence: medium
---

# Vengeance Demon Hunter — talents & builds (Midnight Season 1)

Layers on the generated talent tree in `talents.md` (do not regenerate that
file — this is the narrative on top of it). Node names, spell IDs, and tree
positions live there.

## Hero tree: both viable in S1

Vengeance's two Midnight hero trees are **Aldrachi Reaver** and **Annihilator**.
**Annihilator is Midnight-new** — it replaces The War Within's *Fel-scarred*
tree (Fel-scarred is gone for Vengeance; don't cite pre-Midnight Fel-scarred
guides). As of the 12.0.7 Heroic-week tuning, **both trees are viable**:
Annihilator was the earlier default, but buffs to Aldrachi Reaver pulled them
close for raid and M+ (method.gg, upd. 2026-06-16). The simc default profile
ships as **Annihilator**.

- **Aldrachi Reaver** — the **Reaver's Glaive** empower cycle. Consuming Soul
  Fragments builds **Art of the Glaive**; at cap it grants a **Reaver's Glaive**
  that empowers your next Fracture (**Rending Strike**) and Soul Cleave (**Glaive
  Flurry**), while **Reaver's Mark** sits on the target as a damage-taken debuff.
  You alternate "slash" and "refresh" cycles (see `rotation.md`). More
  execution-heavy; rewards precise cycle management. Key nodes: Art of the
  Glaive, Reaver's Mark, Fury of the Aldrachi, Aldrachi Tactics, Warblade's
  Hunger, Thrill of the Fight; choice of **Evasive Action / Unhindered Assault**
  (Unhindered Assault = the Vengeful-Retreat→Felblade rotational reset).

- **Annihilator** — a **Voidfall** stack engine. **Fracture** builds Voidfall;
  at **3 stacks**, spending (Spirit Bomb / Soul Cleave) drops meteors.
  **Metamorphosis** grants meteors + resets Spirit Bomb, and **World Killer**
  (capstone) reduces Meta's cooldown. Defensive value comes from **Swift
  Erasure** + **Phase Shift**, extended by **Final Hour** (Haste + DR scaling
  with Voidfall). Smoother to pilot: keep Fracture on cooldown, spend at 3
  stacks, and manage the **Untethered Rage** Apex proc. Key nodes: Voidfall,
  Meteoric Fall, Swift Erasure, Phase Shift, Final Hour, Mass Acceleration,
  World Killer; choice of **Path to Oblivion / State of Matter** and
  **Doomsayer / Harness the Cosmos**.

## The Apex talent — Untethered Rage (Annihilator burst)

**Untethered Rage** (spec tree row 12, spell 1270444 — a Midnight-new
**Apex** talent) is the standout. Each Soul Fragment consumed by Soul Cleave /
Spirit Bomb has a **rising chance** to grant a special **Metamorphosis charge**
(activate within 12s, grants Meta for 10s); further points let both spenders
consume **one extra fragment** and increase the fragment damage bonus. The proc
chance ramps steeply — activations commonly land at 6–8 stacks and are near-
guaranteed by ~13–14, so in practice you get **at least one free Meta per
minute**, usually more. It's why the Annihilator loop is built around spending
fragments aggressively and jumping into Meta on the proc. @verify-ingame

## Core spec + class talents (both builds)

The maintenance backbone is shared: the builder/spender core (**Fracture**,
**Spirit Bomb**, **Soul Cleave**), **Immolation Aura**, **Sigil of Flame**,
**Fiery Brand** + **Fiery Demise** (fire-damage amp window), **Fel Devastation**,
**Soul Carver**, **Sigil of Spite**, and the **Demon Spikes** mitigation
package. Near-universal picks per the guides:

- **Fragment / spender cluster:** Spirit Bomb, Soul Cleave value nodes,
  **Feed the Demon** (Demon Spikes uptime), **Frailty** + **Painbringer**
  (mitigation from fragments), **Fallout** (Immolation Aura spawns fragments in
  AoE), **Soul Sigils** / **Soul Barrier** choice.
- **Fire / brand cluster:** **Fiery Demise**, **Charred Flesh** (Immolation
  Aura extends Brand), **Stoke the Flames**, **Burning Blood**, **Darkglare
  Boon** (Fel Devastation cooldown reduction).
- **Sustain / defensive:** **Revel in Pain**, **Feast of Souls** (buffed in
  12.0.7 but still underused per method.gg), **Soulcrush**, **Last Resort**
  (cheat-death), **Calcified Spikes** (Demon Spikes DR extension).
- **Class tree:** the mobility/CC/utility spine — **Vengeful Retreat**,
  **Felblade**, **Sigil of Misery**, **Chaos Nova**, **Consume Magic**,
  **Imprison**, **Darkness**, **Master of the Glaive / Champion of the Glaive**
  (Throw Glaive charges), **Disrupting Fury** (Fury on interrupt), **Soul
  Rending** (leech in Meta), **Blazing Path** (Infernal Strike charge).

## Build split by content

- **Single target / raid:** lean the fragment-value + fire-amp clusters; both
  hero trees raid-viable post-12.0.7. Annihilator squeezes value from the free
  Meta procs; Aldrachi Reaver leans on tight Reaver's Glaive cycles.
- **Mythic+ / AoE:** favor **Fallout** + **Spirit Bomb** throughput, **Sigil**
  cluster (Sigil of Chains / Sigil of Silence via the Roaring Fire choice) for
  pull control, and **Charred Flesh** for extended Brand windows on big packs.

## Reference talent string (Tier-1, simc default — Annihilator)

```
CUkAAAAAAAAAAAAAAAAAAAAAAAAYMzMjhZkZmZGDzMzMDGzMmxMmhxMmZsMmZZMmBAAAAAAAgZmxGAAAAGYmZmZ2abmZGAYAAAAMA
```

> Import strings are tree-version-sensitive — confirm it loads as **Annihilator
> Vengeance** in-game before trusting (one bad character breaks the import).
> For an Aldrachi Reaver string, pull the current method.gg / Icy Veins talents
> page (a matching Tier-1 AR simc profile was not captured this pass).

## TODO

- [ ] Capture a Tier-1 Aldrachi Reaver simc talent string (only the Annihilator
      default profile was available on the midnight branch this pass).
- [ ] Add measured hero-tree DPS/survivability deltas once a Vengeance sims.md
      exists (mirror the Affliction sims.md pattern).
- [ ] Confirm the exact live tuning gap between AR and Annihilator for M+ vs raid
      (method.gg says "close" post-12.0.7 Heroic week — quantify).

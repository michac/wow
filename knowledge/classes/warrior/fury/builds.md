---
title: Fury Warrior — talents & builds (Midnight Season 1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Warrior_Fury.simc  # tier 1, default talents= string (Slayer ST), 2026-07-11
  - https://www.method.gg/guides/fury-warrior/talents  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/fury-warrior-pve-dps-spec-builds-talents  # tier 3, 12.0.7, 2026-07-11
  - https://murlok.io/warrior/fury/m+  # tier 2, top-50 M+ usage aggregation (Blizzard API), 2026-07-11
  - knowledge/classes/warrior/fury/talents.md  # sibling tier-1 talent inventory (the tree floor)
confidence: high
---

# Fury Warrior — talents & builds (Midnight S1)

Layered on top of the sibling `talents.md` (Blizzard game-data tree inventory) —
this file is the *narrative*: which hero tree, which loadout, and why. Import
strings below are Tier-1 (simc profile) or Tier-3 (method / Icy Veins) as tagged.

## Hero tree — both are live in S1

Unlike most specs, Fury genuinely splits its hero tree by content. Top-50 M+
usage is a near coin-flip (**Slayer ~52% / Mountain Thane ~48%**, murlok
2026-07-11), and the two guides agree on *when* to pick each:

- **Slayer** — the **single-target and burst-AoE** tree. Built around
  **Sudden Death** procs, **Execute**, and **Bladestorm**. Its signature is
  the Recklessness burst window: **Reckless Abandon** turns Bloodthirst into
  **Bloodbath** and Raging Blow into **Crushing Blow**, and **Unrelenting
  Onslaught** feeds Bladestorm cooldown reduction off Sudden Death consumption.
  Best on pure ST raid bosses and short burst-AoE pulls. **This is the simc
  default profile** (the `MID1_Warrior_Fury.simc` `talents=` string is Slayer ST).
- **Mountain Thane** — the **sustained-AoE and lightning** tree. **Thunder Clap
  replaces Whirlwind** as the cleave enabler; **Storm Surge** makes Avatar buff
  Thunder Clap (+50% damage, −50% CD), and **Thunder Blast** (an empowered
  Thunder Clap that extends Avatar and always fires a Lightning Strike) becomes
  a priority button. Wins most **sustained** multi-target — long M+ pulls, raid
  adds. Slightly behind Slayer on pure ST.

**Rule of thumb:** Slayer for single-target / burst-AoE (raid bosses like
Imperator, Vorasius, Belo'ren, Midnight Falls per Icy Veins); Mountain Thane for
sustained AoE (most M+, add-heavy fights). Both are within a few percent — either
is defensible in M+.

## Import strings

**Slayer — Single Target** (Tier-1 simc default profile; matches Icy Veins ST):
```
CgEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGDjxMsMzMzMDjZmZGzMzsMzMGzMbDzMAAQMWWGYBMBzwEYG2AmZ2Y2GAAMzYYMzMMYA
```

**Mountain Thane — Multi-target / Mythic+** (Tier-3, Icy Veins 12.0.7):
```
CgEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGDjZMz2yMzMjZmxMjZMjZWmZGjZmlxMzAAAhB2glFjGzAysgZsAYGMGAMzAYYmZGMYA
```

Method.gg additionally publishes Slayer Cleave and Mountain Thane ST/Cleave
variants; the two above are the anchor picks (pure ST vs M+). @verify-ingame
(confirm each string loads on the correct hero tree before trusting — one bad
character breaks an import).

⚠ Import strings are tree-version-sensitive. These were captured at build
12.0.7.67808; re-verify if the talent tree changes in a later patch.

## Core talents (near-universal, top-50 M+)

These appear in ~all top builds regardless of hero tree (murlok 2026-07-11) —
treat them as the fixed skeleton and tune the rest per content.

**Class tree:** War Machine, Impending Victory, Heroic Leap, Rend, Frothing
Berserker, Pain and Gain, Overwhelming Rage (Rage cap → 120), Rallying Cry,
Spell Reflection, Armored to the Teeth, Double Time (2 Charge charges),
Reinforced Plates, Crushing Force, Cruel Strikes, **Dual Wield Specialization**,
Wild Strikes, **Anger Management** (Rage spent → Recklessness/Avatar/Bladestorm
CD reduction — this is why the majors come up ~every 45s), Battlefield Commander.

**Spec tree:** Bloodthirst, Raging Blow, **Sudden Death**, **Frenzied Enrage**
(Enrage tuning), Improved Execute, Focus in Chaos, **Improved Whirlwind**
(single-target strikes cleave), **Fresh Meat** (Bloodthirst crits Enrage),
**Rampage**, Improved Raging Blow, Deep Wounds, Spite, Scent of Blood, Cruelty,
Cold Steel Hot Blood, **Recklessness**, **Deft Experience**, **Frenzy**, Vicious
Contempt, **Odyn's Fury**, Bloodborne, Executioner's Wrath, **Reckless Abandon**,
and the capstone **Rampaging Berserker**.

## Key talent interactions

- **Rampaging Berserker** (capstone) — the payoff of the whole Rage loop.
  Centered on Rampage: ~10% damage increase plus stacking Strength (per method,
  3% Str/use) and, during Recklessness, reduced Rage cost + amplified damage.
  It also extends the Recklessness window. This is why Rampage is spammed as the
  primary spender rather than banked.
- **Anger Management + Reckless Abandon** — Rage spending shortens Recklessness'
  cooldown (Anger Management), and Recklessness upgrades your builders to
  Bloodbath / Crushing Blow (Reckless Abandon). Spending Rage literally buys more
  burst windows, so overcapping Rage is a double loss.
- **Sudden Death** (Slayer core) — random procs that make **Execute** usable at
  any health and free; under Slayer these procs are more frequent and jump
  Execute up the priority. Pairs with **Improved Execute** / **Executioner's
  Wrath** for the execute-window damage.
- **Massacre** (choice on the execute cluster) — raises Execute's health
  threshold from 20% → **35%**, greatly lengthening the execute phase. Simc's
  default profile takes it (`variable.execute_phase` keys off 35%).
- **Storm Surge / Thunder Blast** (Mountain Thane) — Avatar supercharges Thunder
  Clap; Thunder Blast is worth more than its tooltip (extends Avatar + guaranteed
  Lightning Strike). This is what makes the tree's *sustained* AoE win — the
  value compounds over Avatar's duration on 3+ targets.
- **Slayer's Dominance / Executioner stacks** (Slayer) — attacks proc Slayer's
  Strike, each stacking Executioner for +Execute damage, crit chance, and crit
  damage. Feeds the burst/Execute identity.

## S1 tier set

The Season 1 set bonus package reinforces the Enrage loop and (per the sibling
`abilities.md`) **reduces Odyn's Fury's cooldown**, tightening the burst cadence.
2pc/4pc are worth several ilvls each — take/upgrade tier regardless of
secondaries. @verify-ingame (exact 2pc/4pc wording + Odyn's Fury CD reduction for
the live 12.0.7 set)

## Stat priority (brief)

Fury's secondaries are relatively flat — **ilvl generally wins** over stat
weights, and tier pieces win regardless. Sources lean Crit/Haste with Mastery
close behind; sim on Raidbots when a choice is close rather than hard-stacking a
single stat. (Full gearing/enchant/gem detail is out of scope for this file —
run `wowkb.plan --gear --character <name>` for a per-slot chart.) @verify-ingame
(current stat order for the live 12.0.7 build)

## TODO

- [x] Hero tree choice — both live (Slayer ST/burst, Mountain Thane sustained
      AoE); usage ~52/48 (murlok 2026-07-11)
- [x] Import strings — Slayer ST (Tier-1 simc default) + Mountain Thane M+
      (Tier-3 Icy Veins), captured 2026-07-11
- [x] Core near-universal talent list — murlok top-50, 2026-07-11
- [ ] Confirm S1 2pc/4pc exact wording + Odyn's Fury CD reduction (Blizzard
      journal / spell API) for the live build
- [ ] Nail down live 12.0.7 stat order (Raidbots sim) rather than the flat
      "Crit/Haste-ish" guide consensus

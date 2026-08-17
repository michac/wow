---
title: Demon Hunter Devourer — Talents & Builds (12.1 pre-season; S2 opens Aug 18)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes (archived: _meta/patch-notes/12.1.md)
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-spec-builds-talents  # tier 3, upd. 2026-08-10, explicitly 12.1 (Void-Scarred loadouts)
  - https://maxroll.gg/wow/class-guides/devourer-demon-hunter-raid-guide  # tier 3, upd. 2026-08-11, 12.1 (captured verbatim as maxroll-raid.md)
  - ./ability-inventory.md  # tier 1, Blizzard Game Data API + wago DB2 @ 12.1.0.69214, 2026-08-11 (talent tooltips)
  - ./talents.md  # tier 1, talent tree from wago DB2 @ 12.1.0.68914, 2026-08-11 (node/spell names)
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer.simc  # tier 1 talent string, 12.0.7 — NOT re-pulled at 12.1
confidence: medium
---

# Demon Hunter Devourer — Talents & Builds (12.1 pre-season; S2 opens Aug 18)

Layers on top of `talents.md` / `talents.json` / `ability-inventory.md` (the
Tier-1 generated twins — tree at build `12.1.0.68914`, ability tooltips at
`12.1.0.69214`; where prose and those files disagree, they win). This file
is the *narrative* — which hero tree, which loadouts, and what the key talents
change. See `rotation.md` for how the picks play out button-to-button.

> ⚠ **Season 2 opens 2026-08-18.** 12.1 went live 2026-08-11; the week of Aug 11
> is a pre-season week — the S2 dungeon pool is already playable on Heroic and
> Mythic 0 (and S2 gear is dropping), but there are **no keystones and no
> Venomous Abyss** until Aug 18. So the build advice below is 12.1-current, but
> **nobody has ladder or log data for it yet** — re-check the hero-tree call once
> S2 has logs.

## ⚠ What 12.1 did to this spec (read before trusting any older build)

Blizzard rebalanced Devourer *away from* the Void Metamorphosis window
(Tier 1, 12.1 notes; dev note quoted verbatim in `_meta/patch-notes/12.1.md`):

- **Mastery: Monster Within — bonus damage during Void Metamorphosis reduced by
  66%**, compensated by **all ability damage +32%**. Blizzard's stated intent:
  *"damage during Void Metamorphosis to be slightly reduced while damage outside
  of Metamorphosis is significantly increased."* The stated reason for the Mastery
  cut is to **let other secondaries compete** — so treat any "Mastery is king"
  line (including `gearing.md`'s S1 priority) as needing re-derivation.
- **Void Metamorphosis now increases Void Ray damage by 40%** (was 67%).
- **Consume +60%** (does **not** affect Devour) · **Collapsing Star +12%** ·
  **Eradicate −6%, secondary-target damage −15%** ·
  **Impending Apocalypse now +20% per Collapsing Star** (was 30%).
- **Hungering Slash** now grants a **temporary charge of Vengeful Retreat**
  instead of a free cast *plus* a cooldown reset. (12.1 tooltip: the next
  Vengeful Retreat within 6s also deals extra Cosmic damage.)
- **Annihilator**: **Otherworldly Focus +30% single-target** (was 35%) ·
  **Final Hour persists 6s** (was 8s).
- **Demon Hunters can now equip daggers**, explicitly so Devourer can use
  Intelligence daggers — a weapon-slot change, see `gearing.md`.

**The build consequence:** the S1 doctrine of "pool everything, dump it all
inside Meta" is no longer the whole game. Out-of-Meta throughput is now a much
larger share of the damage, which is exactly the axis **Void-Scarred** builds on
(Enduring Torment: +20% Mastery effectiveness outside demon form; Monster
Rising: +15% Intellect outside demon form) — see the contested hero-tree call
below.

**Global 12.1 changes that touch build/utility picks:** player health **+25%**
and creature damage **+25%** at max level (defensive-talent value shifts, and
every absolute HP/heal number written before 2026-08-11 is stale);
**diminishing-return categories now reset after 20s** (was 16) — i.e. you must
now wait 20s, not 16, before a CC category returns to full duration, so repeat
class-tree CC (Imprison / Sigil of Misery / Void Nova) comes back to full
strength *later*, not sooner;
interrupts now show a **"missed"** visual + sound when the target was not casting.

## Hero tree: **contested in 12.1 — was Annihilator-everywhere in S1**

The 12.1 rebalance flipped, or at least reopened, the S1 answer. The two
12.1-current Tier-3 sources disagree, and neither has S2 logs behind it:

| Source (12.1) | Call |
|---|---|
| **Icy Veins**, upd. 2026-08-10 | **Void-Scarred** for both raid and M+ — "a significant lead in pure single-target situations, while *also* bringing more burst cleave for free"; AoE narrows the gap but Void-Scarred keeps it by cycling **Voidsurge** procs |
| **Maxroll (raid)**, upd. 2026-08-11 | **Annihilator** "currently slightly ahead of Void-Scarred in both AoE and Single-Target" |

**How to read that:** the direction of the 12.1 change (less damage inside Meta,
much more outside) mechanically favours Void-Scarred's out-of-Meta package and
its fast in/out window loop, and it took the two direct Annihilator nerfs
(Otherworldly Focus 35→30%, Final Hour 8→6s) plus the Void-Ray-in-Meta cut
(67→40%) that its Void Ray → Reap/Eradicate loop leans on. That is the reasoning
behind the Icy Veins flip. **Do not treat either call as settled** — pick the one
matching the guide you follow, and re-check against WCL/murlok once S2 starts.

- **Annihilator** — caster-leaning; ramps **Voidfall** stacks (Consume has a 35%
  chance to grant one) and at 3 stacks **Reap/Eradicate** consumes them for
  **Voidfall meteors** via *Meteoric Fall*. Flatter outside cooldowns, sharp
  inside Meta. The S1 default.
- **Void-Scarred** — Meta-centric and melee-leaning; **Voidsurge** (spell 452402 — still
  emitted as `Demonsurge` by `talents.md` @ build `12.1.0.68914`, while the 12.1
  ability data @ `12.1.0.69214` calls it **Voidsurge**) makes Void Metamorphosis empower Voidblade and Hungering
  Slash, and the first cast of each empowered ability explodes for Cosmic damage.
  Pairs with **Soul Glutton** for frequent short windows, and with *Student of
  Suffering* for out-of-Meta burst.

## Recommended loadouts (talent strings)

⚠ Strings below are **as published by their source** — Icy Veins' are 12.1
(2026-08-10); the simc string is **12.0.7 and has not been re-pulled at 12.1**. Devourer's tree had no node moves in the 12.1 notes (unlike Havoc and
Vengeance), so the old strings should still import — but they encode an S1 build
made before the Mastery rebalance.

- **Void-Scarred — single target (Icy Veins, 12.1):**
  `CgcBAAAAAAAAAAAAAAAAAAAAAAAWMzMzMzMjBmBAAAAAAY5BGz2gZAAAAAAAAYGzw8AzMzMzMzMjZ2mZM202CACYAMmZmtZmpZbmlZmxYGA`
- **Void-Scarred — AoE / Mythic+ (Icy Veins, 12.1):**
  `CgcBAAAAAAAAAAAAAAAAAAAAAAAWMzMzMzYMGmBAAAAAAY5BGz2gZAAAAAAAAYGzw8AzMzMzMzMjZ2mZM202CACYAMmZmtZmpZZmlZmhZGA`
- **Annihilator — raid (Maxroll, 12.1):** published only as a maxroll planner
  link, not a bare game string — see `maxroll-raid.md` (captured 2026-08-11) or
  the guide's "Maxroll talents import" link
  (`…/embed-tools/talents=CicBIo1c2KfIEsPoy9fznypG4BA2MmZmZmZmBzMAAAAAAALzYMYGAAAAAAAEMjBzMzMzMzMzwMLmxYRLLMzMzs12MzMAmxAQAjBjZA`).
  Maxroll uses the **same** Annihilator build for single-target and multi-target.
- **Annihilator — 12.0.7 simc default (historical, pre-rebalance):**
  `CgcBAAAAAAAAAAAAAAAAAAAAAAA2MmZmZmZmBzMAAAAAAALzYAzAAAAAAAAwMGMmZmZMzMzYmFzYsotNmZmZ2abmZGAjZAIwMzgxMA`
  (simc `MID1_Demon_Hunter_Devourer.simc`, 12.0.7). Kept as the S1 reference
  point; a 12.1 MID1 APL has not been pulled (`wowkb.simc demon-hunter devourer`).

> ⚠ Import strings are tree-version-sensitive — **confirm each loads as the right
> hero tree in-game** before trusting (one bad char breaks the import).
> @verify-ingame

## Key talent interactions

Tooltip text below is from `ability-inventory.md` (Tier 1, Blizzard Game Data API
@ `12.1.0.69214`), so it is 12.1-accurate except where flagged.

- **Void Metamorphosis** — still the engine, but no longer the *whole* damage
  profile after the Mastery cut. Activates at **50 Soul Fragments**; enhances
  Consume and Reap, drains Fury over time, and makes **Void Ray** reduce that
  drain, cost no Fury, and deal **+40% damage** (was +67%).
- **Soul Glutton** (choice vs *Emptiness*) — Void Metamorphosis requires **15
  fewer souls** (50 → 35) but Fury drains **25% faster** inside, so windows are
  more frequent and shorter. Icy Veins' 12.1 Void-Scarred builds take it, to
  cycle **Voidsurge** as often as possible.
- **Emptiness** (the other half) — every soul consumed in Meta grants **0.25%
  Haste, up to 25%**; the "fewer, longer, ramping windows" side of the node.
- **Devourer's Bite** — Voidblade and The Hunt damage increase the damage the
  target takes from you by **12% for 10s**, and applications may overlap. The
  priority-target amp; the single-target swap opposite Eradicate.
- **Eradicate** — fully channelling **Void Ray** upgrades **Reap** into
  **Eradicate**: primary-target damage plus a **25 yd frontal cone**, reduced
  beyond **5 targets**. Still the multi-target backbone; 12.1 cut it **−6%**
  (**−15%** on secondary targets).
- **Moment of Craving** — after fully channelling Void Ray, **Reap's cooldown
  resets** and the next Reap collects up to **6 additional Soul Fragments**.
- **Second Helping** — **Reap gains an additional charge**, flat. It is
  unconditional: the charge is not earned by channelling Void Ray (that is
  Moment of Craving, above).
- **Soulshaper** — each Soul Fragment gathered by Reap increases its damage by
  **8%**; a core Reap amplifier in the 12.1 Void-Scarred lists.
- **Devourer's Edge** — Reap and Consume damage **+10%**; note **Consume itself
  was buffed 60%** in 12.1, so this node's absolute value rose with it.
- **Focused Ray** — Void Ray hits much harder when it is not spread across
  targets. The 12.1 tooltip reads, verbatim: *"Void Ray deals 80% more damage
  when damaging 3 targets."* That wording is ambiguous — it does not say whether
  the threshold is "at most 3" or "exactly 3"; Maxroll reads the talent as
  "significantly more damage if you only hit one target". Avoid clipping
  off-targets with the beam. @verify-ingame
- **Hungering Slash** — after The Hunt or Voidblade deals damage, Voidblade is
  replaced by **Hungering Slash for 6s**: AoE Cosmic damage, **+10 Fury**,
  shatters up to **2 Soul Fragments**. **12.1: it now grants a temporary
  Vengeful Retreat charge** (and makes the next Vengeful Retreat within 6s deal
  extra damage) **instead of a free cast + cooldown reset** — so it is a mobility
  *charge* to bank, not a free reposition you can double-dip.
- **Collapsing Star** — in Meta, every **30** Soul Fragments harvested grants a
  cast; Fury drain slows heavily while channelling it. **+12%** in 12.1.
- **Impending Apocalypse** — each Collapsing Star increases the damage of your
  next one by **20%** (was 30%).
- **Midnight** (Apex) — Rank 1 makes **Collapsing Star always critically
  strike**, which is why it pairs with **Calamitous** (crits deal 240% instead of
  200%). ⚠ **Contested in 12.1:** Icy Veins' Void-Scarred lists *skip* it —
  "Collapsing Star doesn't deal enough damage to justify the impact it has on its
  pacing" — while Maxroll's Annihilator raid build builds around it (R2: +6% all
  Cosmic damage; R3: Collapsing Star available immediately on entering Meta, +5
  souls on entry). Hero tree decides this one.
- **Student of Suffering** (Void-Scarred, choice vs *Flamebound*) — buff window
  for out-of-Meta damage; worth more after the 12.1 shift toward out-of-Meta.
- **Enduring Torment / Monster Rising** (Void-Scarred) — **+20% Mastery
  effectiveness** outside demon form and **+15% Intellect** while not in demon
  form. Counter-intuitive next to "stay in Meta", and the main reason
  Void-Scarred gained from the 12.1 rebalance.
- **Meteoric Fall / Voidfall** (Annihilator) — Consume has a **35%** chance to
  grant a Voidfall stack; at **3 stacks**, Reap consumes all 3 to call down that
  many meteors. The Annihilator damage identity (see `rotation.md` — "Reap at
  3 Voidfall"). Watch overcapping around Meta entry.
- **Otherworldly Focus** (Annihilator) — Collapsing Star and Voidfall meteors
  deal **+30% against a single target** (was 35%), **−5% per additional target**.
- **Final Hour** (Annihilator) — Voidfall's passive bonuses persist **6s** after
  being consumed (was 8s). ⚠ The 12.1.0.69214 spell tooltip still reads **8 sec**;
  the Tier-1 patch note says 6. Treating the note as the floor. @verify-ingame

## Gearing

> **Moved to `gearing.md` (2026-07-14).** Stat priority, trinkets, tier set,
> embellishments, enchants, gems and consumables live there. Two 12.1 items that
> land on that file, not this one: **daggers are now equippable by Demon Hunters**
> (Intelligence daggers are explicitly for Devourer), and the **Mastery −66%
> in-Meta / +32% all-ability** rebalance was explicitly done so *"other stats can
> compete"* — the S1 "Mastery > Haste" priority needs re-derivation, not a restamp.

## TODO

- [ ] Verify all import strings load as the correct hero tree in-game.
- [ ] **Resolve the hero-tree call** (Icy Veins: Void-Scarred both roles ·
      Maxroll: Annihilator both roles) against WCL / murlok.io once Season 2 has
      logs (opens 2026-08-18).
- [ ] Pull a 12.1 simc MID1 APL (`wowkb.simc demon-hunter devourer`) and replace
      the 12.0.7 Annihilator string with the Tier-1 12.1 default.
- [ ] Re-capture `maxroll-mplus.md` — it is still the 2026-06-22 (pre-12.1)
      guide and its build predates the Mastery rebalance.
- [ ] Confirm Focused Ray's exact target-count wording, and whether Final Hour is
      6s or 8s live.

## Changelog

2026-08-17 — Moment of Craving resets Reap's cooldown and adds up to 6 Soul Fragments
(it was once written as gating an "Eradicate spend at 10 souls"), and Second Helping's
extra Reap charge is unconditional (it was once written as earned by channelling Void Ray).

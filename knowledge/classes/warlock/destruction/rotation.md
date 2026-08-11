---
title: Destruction Warlock — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes — Destruction + global class changes, 2026-08-11
  - knowledge/_meta/patch-notes/12.1.md  # tier 1, verbatim archive, CLASSES ▶ WARLOCK / Destruction (l.1208-1216)
  - knowledge/classes/warlock/destruction/ability-inventory.md  # tier 1, generated from Blizzard Game Data API + wago Spell* DB2 @ 12.1.0.69214 — live Conflagration of Chaos / Fiendish Cruelty tooltips
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warlock_Destruction.simc  # tier 1, simc midnight APL, 2026-07-11 (12.0.7-era — see TODO)
  - wago.tools DB2 SpellCooldowns, spell 1122 Summon Infernal  # tier 1, RecoveryTime 120000ms — corrects base CD to 120s (Inferno → 90s)
  - https://www.method.gg/guides/destruction-warlock/playstyle-and-rotation  # tier 3, upd. 2026-06-16, 2026-07-11 — page still labelled 12.0.7
  - https://www.icy-veins.com/wow/destruction-warlock-pve-dps-guide  # tier 3, upd. 2026-08-10 for 12.1 — corroborates Havoc 50% + Conflagration of Chaos redesign
  - raw/addon-research/simc @ ab7b0b8  # tier 1, local simc checkout (branch midnight, DBC 12.0.7.68887) — the Rain of Fire gate note, 2026-08-01
confidence: medium
---

# Destruction Warlock — Rotation (Midnight 12.1)

Distilled from the **SimulationCraft midnight-branch APL** (tier 1) with
method.gg (tier 3) for colour. The APL branches by **hero tree** — `aoe_dia`
(Diabolist / Diabolic Ritual) and `aoe_hc` (Hellcaller / Wither) — and by enemy
count. Destruction is a **Soul Shard economy**: keep your fire DoT up, never
overcap shards, and pour shards into **Chaos Bolt** (single target) or **Rain of
Fire** (big AoE), timed around **Summon Infernal**.

> **12.1 "Curse of Ula'tek" (live 2026-08-11).** Both hero trees are viable:
> **Diabolist** is the default (best ST, competitive stacked cleave — it cycles
> Diabolic Ritual → Demonic Art → a free **Ruination**, so it presses Chaos Bolt
> even into moderate AoE). **Hellcaller** trades Immolate for **Wither** and adds
> the **Malevolence** burst CD; it is the sustained-AoE / long-fight pick. See
> `builds.md`.

## What 12.1 changed for Destruction

The stated design direction is **single-target up, cleave down** — Destruction
should still be the best 2-target spec, but by a smaller margin.

- **Conflagration of Chaos redesigned — it is no longer a proc.** It now reads:
  *"Conflagrate and Shadowburn have a 100% chance to critically strike, and
  their damage is increased by your critical strike chance."* There is no buff
  to react to and **nothing in the rotation is gated on it any more** — take the
  talent and press Conflagrate/Shadowburn on their own merits. Any older guide
  (or older revision of this file) that says "Shadowburn when Conflagration of
  Chaos is up" is describing the dead pre-12.1 proc.
  - Second-order: because both abilities always crit, **crit is the stat that
    scales them** and **Fiendish Cruelty** — *"Critical strikes dealt by Chaos
    Bolt, Conflagrate, or Incinerate have a 10% chance to make your next
    Shadowburn free and usable on any target regardless of health"* — is now
    fed by every Conflagrate. Fiendish Cruelty **is** still a proc and is still
    the thing you react to.
- **Havoc now copies 50% of a spell's damage to the marked target (was 60%).**
  The cleave section below is unchanged in *order*, but the payoff per
  duplicated Chaos Bolt is a sixth smaller.
- **Soul Fire damage +45%**, **Chaos Bolt +5%**, **all Destruction damage
  +4.5%**. Soul Fire's relative position in the priority is stronger than the
  12.0.7 APL ordering below reflects.
- **Cooldown Manager:** **Shadowburn was added as a tracked buff** and
  **Conflagration of Chaos was removed** (it no longer produces a buff). If you
  run a CDM-driven overlay, its tracked set for this spec changed on patch day.
- **Class-wide Warlock:** Drain Life health drain **+25%**; Summon Demonic
  Gateway is now a Utility spell by default in the Cooldown Manager. A Soul
  Leech correctness pass means **Infernal Bolt** and **Avatar of Destruction's
  Chaos Bolt** now *do* grant Soul Leech, while **Channel Demonfire** no longer
  erroneously does — a small, real self-shielding shift in Diabolist play.
- **Embers of Nihilam (Rank 1)** tooltip now states the percent chance for
  Incinerate to evoke an Echo of Sargeras. Tooltip only; no behaviour change.

**Four global 12.1 changes apply here as to every spec:** player health and
creature damage **+25% at max level** (health-consumable values rescaled, so
**any absolute HP/healing number written before 2026-08-11 is stale**); major
DPS cooldowns lowered with steady-state damage raised across several specs;
interrupts now show a **"missed"** visual + sound when the target was not
casting; diminishing-return categories now reset after **20s** (was 16s).

## Pre-combat (opener)

APL precombat: `summon_pet` → set trinket-sync variables →
`grimoire_of_sacrifice` (if talented) → `snapshot_stats` → **Cataclysm** (if 2+
targets) → **Soul Fire** (pre-cast at ~4s on the pull timer) → Cataclysm →
Immolate (if 2+ & Roaring Blaze) → **Incinerate**.

- **Diabolist opener:** pre-cast Soul Fire → **Summon Infernal + trinket +
  potion + racial** → Conflagrate → resume.
- **Hellcaller opener:** pre-cast Soul Fire → Summon Infernal → Conflagrate →
  **Malevolence + trinket + potion + racial** → resume.
- No Soul Fire talented: open with 2× Incinerate into Immolate/Wither.

## Cooldown rules

- **Summon Infernal is the burst window** — everything syncs to it. Potion,
  racials (Berserking/Blood Fury/Fireblood/Ancestral Call), and external buffs
  (Power Infusion) fire *only* while the Infernal is active (`variable.infernal_active`),
  and trinkets are sync-scored to the **120s base (or 90s w/ Inferno)** Infernal cadence.
- **Malevolence (Hellcaller, 60s)** does **not** naturally align with Infernal
  (120s base, 90s w/ Inferno) — only line them up on the final casts of a fight; otherwise use
  Malevolence on cooldown and spend maximum shards inside its window.
- **Pool for adds:** if important adds are about to spawn, pool Soul Shards and
  delay Infernal/Malevolence to that point — a large gain over blind on-CD use.

## Single target — Diabolist (APL `default`)

1. **Soul Fire** if `soul_shard<=4` (fits without overcapping)
2. **Chaos Bolt** to spend a **Demonic Art** proc or restart Diabolic Ritual
   (`demonic_art` up, or ritual short, and target >20% HP)
3. **Conflagrate** to build if `soul_shard<=4.2` and no Backdraft stacked
4. **Summon Infernal**
5. **Incinerate** if **Chaotic Inferno** buff up and `soul_shard<=4.6`
6. **Shadowburn** with a free **Fiendish Cruelty** proc up, or when
   **target ≤20%** (execute). *(Pre-12.1 this line also read "or Conflagration
   of Chaos" — that proc no longer exists; see the 12.1 section above.)*
7. **Immolate** — refresh in the pandemic window (<30% duration / refreshable)
8. **Ruination** (free proc — press it)
9. **Cataclysm** if **Lake of Fire** talented
10. **Chaos Bolt** as the main shard dump (ritual length >4)
11. **Infernal Bolt** if `soul_shard<=3` (shard refill)
12. **Incinerate** (filler)

Method's shorthand: **Chaos Bolt (spend Demonic Art / restart ritual) →
maintain Immolate → Summon Infernal → Shadowburn (Fiendish Cruelty / anti-cap) →
Chaos Bolt (anti-cap) → Soul Fire (with Backdraft) → Conflagrate (don't sit on 2
charges) → Incinerate.**

## Single target — Hellcaller

1. Maintain **Wither** (re-apply in the pandemic window)
2. **Summon Infernal**
3. **Malevolence**, then maximize shard spenders inside the window
4. **Shadowburn** (free Fiendish Cruelty proc, or anti-cap; the APL also gates
   on `soul_shard>=4` / Malevolence up / Infernal active / fight ending).
   ⚠ 12.1 Hellcaller: **Chaos Bolt and Shadowburn each add a Blackened Soul
   stack** to a Withered target under the redesigned Blackened Soul, so both
   spenders now feed the hero tree's priority damage — see `builds.md`.
5. **Chaos Bolt** — spend when `soul_shard>=4`, or Malevolence up, or Infernal
   active, or fight_remains ≤15 (otherwise pool)
6. **Soul Fire** (with Backdraft)
7. **Conflagrate** (don't sit on 2 charges)
8. **Incinerate** (filler)

## Cleave (2 targets) — Havoc

- **Havoc** the second target; single-target casts (Chaos Bolt, Shadowburn, Soul
  Fire) are duplicated onto it — **for 50% of their damage as of 12.1 (was
  60%)**. The APL `target_if` logic points Havoc at the add with the most
  time-to-die that isn't your current target, gated so it isn't wasted right
  before Summon Infernal (or Malevolence, Hellcaller).
- The 60→50% nerf is deliberate: Blizzard wanted Destruction to keep the
  2-target crown but by a smaller margin. It does **not** change the priority
  order — Havoc is still worth pressing on cooldown in cleave — it just lowers
  the ceiling relative to the single-target lists.
- Otherwise run the single-target list; keep Immolate/Wither on both, and dump
  duplicated **Chaos Bolt** through the Havoc window.

## AoE (3+)

**Diabolist (`aoe_dia`):**
1. **Summon Infernal**
2. **Chaos Bolt** for Demonic Art / short ritual at `active_enemies<=4` (Diabolist
   keeps pressing Chaos Bolt into moderate AoE)
3. **Rain of Fire** at **4+ targets** when `soul_shard >= (3.5 - 0.1 × active_dot.immolate)`
   or Alythess's Ire up — see the ⚠ note under *AoE* below before using the 3.5
4. **Conflagrate** to refresh Immolate across targets (`target_if` most Immolate
   remaining)
5. **Shadowburn** on low-HP targets (or on a free **Fiendish Cruelty** proc,
   which lifts the health requirement)
6. **Ruination**
7. **Cataclysm** (Lake of Fire, or when no adds incoming)
8. **Havoc** on the longest-living off-target
9. **Infernal Bolt** if `soul_shard<3`
10. **Chaos Bolt** at ≤3 targets with long ritual
11. **Soul Fire** (Avatar of Destruction extends the target cap to 10)
12. **Immolate** to spread (refreshable, ≤5 Immolates, no Cataclysm)
13. **Conflagrate** (Backdraft <2) → **Incinerate**

> ⚠ **THE `3.5` IS NOT RAIN OF FIRE'S COST, and reading it as one is the mistake this
> note exists to stop.** Rain of Fire costs **3 whole shards (30 fragments)** on both
> spell IDs; the in-game tooltip is right. `3.5` is a **hand-tuned APL constant on one
> Diabolist AoE line**, gated `active_enemies>=4`, and it has two siblings this file
> never mentioned:
>
> ```
> :48  rain_of_fire,if=((soul_shard>=(3.5-0.1*(active_dot.immolate)))|buff.alythesss_ire.up)&active_enemies>=4
> :63  rain_of_fire,if=(soul_shard>=(4.0-0.1*(active_dot.wither)))&active_enemies>=(5-talent.destructive_rapidity)   ← Hellcaller, 4.0
> :68  rain_of_fire,if=active_enemies>=(5-talent.destructive_rapidity)                                                ← NO shard condition at all
> ```
>
> The `-0.1 × active_dot` term is exactly one Immolate tick's yield per active DoT, so it
> reads as income anticipation — but the buffer **shrinks as income rises**, which is
> backwards for a pooling reserve, and at 8 Immolates it falls *below* the real 3-shard
> cost. Nothing in the APL, its generator or simc's C++ explains it, so no rationale is
> asserted here. **Treat the cost as 3 and the 3.5 as a Diabolist-AoE pooling heuristic.**
> *(Read from the local simc checkout `raw/addon-research/simc` @ `ab7b0b8`, branch
> midnight, DBC build 12.0.7.68887, 2026-08-01.)*

> Diabolist AoE note (method): **don't cast Rain of Fire until ~8+ targets** —
> Chaos Bolt stays more efficient for priority damage because it feeds Diabolic
> Ritual. Only true stacked AoE flips to Rain of Fire.

**Hellcaller (`aoe_hc`):**
1. **Summon Infernal** → **Malevolence**
2. **Rain of Fire** at `soul_shard>=~4` and **5+ targets** (−1 with Destructive
   Rapidity) — Rain of Fire is the Hellcaller spender much sooner than Diabolist
3. **Conflagrate** to refresh Wither across targets
4. **Shadowburn** (free **Fiendish Cruelty** proc, or target ≤20%)
5. **Cataclysm** (no adds incoming)
6. **Havoc** on the longest-living off-target
7. **Rain of Fire** (5+ targets) → **Chaos Bolt** (≤4 targets) → **Soul Fire**
8. **Wither** to spread → **Incinerate** (Fire and Brimstone + Backdraft) →
   **Conflagrate** → **Incinerate**

## Hero-tree summary

- **Diabolist** — Immolate DoT; Chaos Bolt-centric even into AoE via Diabolic
  Ritual → Demonic Art → **Ruination**; **Infernal Bolt** as the shard-refill
  builder. Rain of Fire only at very high target counts. Best single target.
- **Hellcaller** — **Wither** replaces Immolate; **Malevolence** is the extra
  ~60s burst CD; **Rain of Fire** comes online earlier as the AoE spender. The
  long-fight / sustained-AoE choice. **12.1 buffed this tree meaningfully**:
  Blackened Soul redesigned (Chaos Bolt/Shadowburn stack it on a Withered
  target) and **+45%** damage, Wither **+25%**, Mark of Peroth'arn redesigned
  around crit multipliers. Malevolence is deliberately unchanged.

## ⚠ Provenance of the priority lists

**The numbered lists below the 12.1 section are distilled from the
12.0.7-era simc midnight APL** (profile pulled 2026-07-11, local checkout DBC
`12.0.7.68887`). 12.1 landed today; simc has not published a retuned MID1
Destruction profile yet. So:

- The **order** is still the best available model and nothing in the 12.1 notes
  invalidates its structure.
- The **relative weights** have moved — Soul Fire +45%, Chaos Bolt +5%, Havoc
  60→50% — and the removed Conflagration of Chaos proc has been struck from the
  lists by hand. Treat the ordering as *likely* rather than *sim-verified*
  until the APL is re-pulled. This is why `confidence:` is `medium`.

## TODO

- [ ] **Re-distill off a 12.1 simc MID1 APL** (`wowkb.simc warlock destruction`)
      once the midnight branch retunes for 12.1 — that closes the provenance
      caveat above and re-raises confidence to high.
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings` →
      `casts`) once Season 2 logs exist (S2 opens **2026-08-18**; there is no
      12.1 raid data during the Aug-11 pre-season week).
- [ ] Confirm in game what **"Shadowburn added as a tracked buff in the Cooldown
      Manager"** actually surfaces (which aura, on whom) — the patch note says
      buff, but Shadowburn's own effect is a target-side kill-refund.
      @verify-ingame

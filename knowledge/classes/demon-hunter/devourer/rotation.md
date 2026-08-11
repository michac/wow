---
title: Demon Hunter Devourer — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — CLASSES ▶ DEMON HUNTER ▶ Devourer; archived verbatim at knowledge/_meta/patch-notes/12.1.md
  - https://wago.tools/db2  # tier 1, Trait*/Spell* DB2 @ 12.1.0.69214 — corroborated Impending Apocalypse 20% and Otherworldly Focus 30% via the generated ability-inventory.md sibling
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer.simc  # tier 1 APL, 2026-07-11 @ 12.0.7 — NOT re-pulled at 12.1 (talents=CgcBAAAAAAAAAAAAAAAAAAAAAAA2MmZmZmZmBzMAAAAAAALzYAzAAAAAAAAwMGMmZmZMzMzYmFzYsotNmZmZ2abmZGAjZAIwMzgxMA); collapsing_star_stacking max_stack 30 confirms Collapsing Star's 30-Soul cost
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Devourer_Void-Scarred.simc  # tier 1 APL variant, 2026-07-11 @ 12.0.7 — NOT re-pulled at 12.1
  - https://www.method.gg/guides/devourer-demon-hunter/playstyle-and-rotation  # tier 3, Hype, upd. 2026-06-17, read 2026-07-11 @ 12.0.7 — pre-rebalance
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, read 2026-07-11 @ 12.0.7 — pre-rebalance
confidence: low
---

# Demon Hunter Devourer — Rotation (Annihilator, Midnight 12.1)

Devourer has **no fixed rotation — it is a priority system that flips between two
states**: a build phase **outside Void Metamorphosis** (generate Fury + bank Soul
Fragments to 50) and a spend phase **inside Void Metamorphosis** (dump Souls into
Collapsing Star + empowered casts before Fury drains out). As a mid-range caster
the golden rule is **always be casting** — use the mobility kit (Shift, Vengeful
Retreat) to reposition between/around casts rather than dropping a global.

The two-state *shape* is unchanged in 12.1, but **the weight between the two
states moved deliberately** — see "What 12.1 changed" below before trusting any
ordering on this page.

Distilled from the Tier-1 SimulationCraft APL (`MID1_Demon_Hunter_Devourer.simc`,
sub-lists `math_for_wizards` / `reaps` / `melee_combo` / `illicit_doping`)
corroborated against method.gg and Icy Veins (both Tier-3). **Annihilator was the
S1 default in every scenario** (see `builds.md`); Void-Scarred variants are noted
at the end. Talent names on this page were re-checked against the generated
Tier-1 `talents.md` / `ability-inventory.md` siblings at build `12.1.0.68914` —
every talent referenced below still exists.

> ⚠ **The priority orders below are 12.0.7-derived and 12.1 moved the balance
> under them.** The APL was pulled pre-patch and has not been re-run
> (`wowkb.simc demon-hunter devourer`), and both Tier-3 guides predate the
> rebalance. Blizzard's stated intent is *slightly less damage inside Meta,
> significantly more outside* — which is exactly the axis these lists encode. The
> **button list and the state machine are still right**; the **ordering,
> especially anything that reads as "hold it for Meta", is not yet re-verified**.
> Treat exact Soul/Fury/stack thresholds as `@verify-ingame`, and no Warcraft
> Logs sanity-check has been distilled yet.

## What 12.1 changed (2026-08-11)

Tier-1, from the Curse of Ula'tek notes. Blizzard's own framing: *"we expect
damage during Void Metamorphosis to be slightly reduced while damage outside of
Metamorphosis is significantly increased."*

**The rebalance itself**

| Change | Effect on how you play |
|---|---|
| **Mastery: Monster Within** bonus damage during Void Metamorphosis **−66%**, compensated by **all ability damage +32%** | The single biggest change. Meta is no longer a damage cliff you fall off — out-of-Meta GCDs now carry real weight. Also deliberately de-scales Mastery so other stats compete (a `gearing.md` question). |
| **Consume +60%** — *explicitly does not affect Devour* | The out-of-Meta filler got a large buff and the in-Meta filler (Devour) did not. Consume is no longer "the thing you press when nothing else is up". |
| **Void Metamorphosis now grants +40% Void Ray damage (was 67%)** | Much less reason to hold a Void Ray for the window. Cast it when Fury says to. |
| **Collapsing Star +12%** | Still the in-Meta payload, but see the two multipliers below. |
| **Impending Apocalypse: +20% to the next Collapsing Star per cast (was 30%)** | Chaining Collapsing Stars back-to-back pays less; don't contort the window to squeeze one more. |
| **Eradicate −6%, secondary-target damage −15%** | Still the AoE backbone, but the falloff past the primary target is steeper. |
| **Hungering Slash** now grants a **temporary Vengeful Retreat charge** instead of a free cast **plus** a cooldown reset | Void-Scarred melee only. You get *one* Retreat back, not an effectively free chain — see that section. |
| **Annihilator — Otherworldly Focus: +30% single-target (was 35%)** | Small ST nerf to Collapsing Star + Voidfall Meteors. |
| **Annihilator — Final Hour: Voidfall bonuses persist 6s (was 8s)** | Tighter. After Reap consumes 3 stacks you have **6s**, not 8, to cash in the lingering Haste/damage-taken bonuses. |

**Global 12.1 changes that land here too**

- **Player health and creature damage +25% at max level**, with health
  consumables rescaled. Any absolute HP or healing number written before
  2026-08-11 is wrong; incoming damage is proportionally larger, so a dropped
  Void Ray channel to survive a hit is a more common correct call.
- Blizzard lowered major DPS cooldowns and raised steady-state damage across
  several specs as a stated direction — Devourer's mastery swap is that policy
  applied here.
- **Interrupts now show a "missed" visual + sound** when used on a non-casting
  target. Cosmetic, but it makes a wasted Disrupt legible mid-pull.
- **Diminishing-return categories now reset after 20s (was 16s)** — affects
  chained CC (Void Nova, Sigil of Misery, Imprison), not the damage priority.
- **Demon Hunters can now equip daggers**, explicitly so Devourer can use
  Intelligence daggers. That is a weapon-slot change; see `gearing.md`, not this
  file.

> ⚠ **Tier-1 vs Tier-1 conflict — `Final Hour`.** The patch notes say the
> Voidfall bonuses persist **6 seconds** (was 8). The spell tooltip pulled from
> the Blizzard Game Data API on the same day (`ability-inventory.md`, spell
> `1253805` @ build `12.1.0.69214`) still reads **8 sec**. The neighbouring
> nerfs *did* land in that same dump (Impending Apocalypse reads 20%,
> Otherworldly Focus 30%), so this looks like a stale tooltip string rather than
> an unshipped change. **6s is written above per the patch notes.**
> `@verify-ingame` — time the buff after a 3-stack Reap.

## Pre-combat / opener (Annihilator)

1. **Soul Immolation** ~2s before pull.
2. **Consume** ~1s before pull.
3. **Consume** spam until **100 Fury or 3 Voidfall stacks**.
4. **Reap** (at 3 Voidfall) → **Void Ray** → **Void Metamorphosis** once at 50 Souls.
5. On-use trinket + potion inside the Meta window (see cooldown rules).
6. Inside Meta: **Void Ray → Voidblade → Collapsing Star → Cull/Eradicate → Devour**.

## Cooldown rules

- **Void Metamorphosis is still the spec's engine, but it is no longer the whole
  game.** It is fragment-gated, not on a timer: bank to **50 Souls** (35 with
  *Soul Glutton*) and pop it, then extract as many **Collapsing Star** + empowered
  casts as possible before Fury drains and the form drops. Don't sit on 50 Souls
  (Feast of Souls caps out and you overflow). **12.1 caveat:** with Mastery's
  in-Meta bonus cut 66% and all ability damage up 32%, the window is a smaller
  share of your total damage than it was in 12.0.7 — **do not stall or waste
  out-of-Meta GCDs setting one up**, and in particular don't hold Void Ray
  (its Meta bonus is now 40%, was 67%).
- **Trinkets / potion / Power Infusion** sync to the Void Metamorphosis window
  (the APL's `illicit_doping` list gates them on the burst window / on-use logic).
  ⚠ That gating was tuned when Meta was a far bigger multiplier; whether the
  window is still the right sync point is an open 12.1 question.
- **The Hunt** (90s) — weave into a Meta window for burst; a core damage button in
  the Void-Scarred melee build, a lesser priority for Annihilator ST.
- **Don't overcap Souls or Fury.** *Soul Glutton* lowers the Meta requirement to
  35 but drains Fury ~25% faster, shortening windows ~30% — spend faster inside.
  (Shorter, more frequent windows plausibly look better after the 12.1 swap; that
  is a `builds.md` call and is **not** yet re-simmed, so it is not asserted here.)
- **12.1: Consume is a real button now** (+60%, on top of the +32% global). It is
  the out-of-Meta filler *and* the Annihilator Voidfall generator (35% chance per
  cast). Its Meta form, **Devour**, was explicitly excluded from that buff.

## Single target (Annihilator)

**Outside Void Metamorphosis:**
1. **Reap / Eradicate** at **3 Voidfall stacks** (spend the stacks → Void Meteors).
   *12.1:* the lingering Voidfall bonuses from *Final Hour* now last **6s**, so
   line up what you want buffed before you spend the stacks, not after.
2. **Void Metamorphosis** as soon as it's available (50 Souls)
3. **Void Ray** at 100 Fury (main spender + Soul generation) — **cast it, don't
   bank it for Meta** (12.1: Meta's Void Ray bonus is 40%, was 67%)
4. **Soul Immolation** if not active
5. **Consume** (filler / Fury + Soul builder — **+60% in 12.1**, and the Voidfall
   generator)
6. **Reap** at 4+ Souls if it pushes you to Void Metamorphosis access

**Inside Void Metamorphosis:**
1. **Collapsing Star** if Meta is about to expire (don't lose the cast)
2. **Void Ray** if Meta is about to expire
3. **Cull / Eradicate** if Meta is expiring and it makes enough Souls for one more Collapsing Star
4. **Voidblade** (if *Devourer's Bite* talented — damage amp)
5. **Collapsing Star** — costs **30 Souls** per cast; fire it at **≥30 stored
   Souls** so you don't overcap (was mis-stated as 35)
6. **Void Ray**
7. **Cull / Eradicate** at 3 Voidfall stacks, <30 Souls
8. **Collapsing Star**
9. **Devour** (filler — the one button 12.1's +60% Consume buff deliberately
   skipped; it is now the weakest GCD in the window)

*12.1 note on the in-Meta list:* *Impending Apocalypse*'s stacking bonus dropped
to **20% per Collapsing Star** (was 30%), so the payoff for bending the window
around a longer Collapsing Star chain is smaller than the ordering above implies.

## Cleave / AoE (Annihilator)

**Outside Void Metamorphosis:**
1. **Void Metamorphosis** when available
2. **Eradicate** at **3 Voidfall stacks**
3. **Eradicate** with *Moment of Craving* active + 10 Souls on the ground
4. **Void Ray**
5. **Soul Immolation** if not active
6. **Consume**
7. **Reap** at 4+ Souls (grants Meta access)

**Inside Void Metamorphosis:**
1. **Collapsing Star** (before overcapping ~40 Souls)
2. **Eradicate** with *Moment of Craving* + 10 Souls
3. **Void Ray**
4. **Devour**

*Eradicate* (the AoE frontal that Reap becomes after a full Void Ray channel) is
the multi-target backbone — it "stands for a massive portion" of Devourer's AoE.
**12.1 trimmed it**: base damage **−6%** and **secondary-target damage −15%**, so
the cone falls off harder past the primary target. It is still the backbone (the
+32% global buff more than covers the −6%), but its share of a big pull is lower,
and the case for aiming the cone carefully — primary target first — is stronger.

## Void-Scarred branches

Two Void-Scarred variants exist (`MID1_Demon_Hunter_Devourer_Void-Scarred.simc`,
Tier-1) and are single-target-competitive but weaker the moment targets are added:

- **Void-Scarred caster** — outside Meta: Voidblade (if *Devourer's Bite*, next
  cast is Meta) → Void Metamorphosis → Void Ray → Soul Immolation → Reap →
  Consume. Inside Meta: Collapsing Star / Void Ray (if expiring) → **Cull on CD**
  → Pierce the Veil (if *Devourer's Bite*) → Void Ray → Collapsing Star → Cull
  (Student of Suffering-buffed) → Cull → Devour → Soul Immolation (fallback).
- **Void-Scarred melee** — adds a `melee_combo` layer: **Vengeful Retreat** (if
  *Voidstep*-buffed) → **Hungering Slash** → **The Hunt** → **Voidblade** before
  transforming, then inside Meta: Reaper's Toll → Pierce the Veil → Predator's
  Wake weave between Void Ray / Collapsing Star / Devour. Stat priority shifts
  toward Crit (see `builds.md`).
  - ⚠ **12.1 changed the Retreat half of that combo.** Hungering Slash used to
    give a **free Vengeful Retreat cast *and* reset its cooldown** — Blizzard
    calls the old behaviour a bug. It now grants **one temporary Vengeful Retreat
    charge**, and your next Retreat **within 6s** deals bonus Cosmic damage
    (Tier-1 tooltip, spell `1239519` @ `12.1.0.69214`). Practically: you get
    **one** Retreat back, not an effectively free chain, and it is **use-it-or-
    lose-it inside 6s** — so fire the Retreat promptly after Hungering Slash
    rather than saving it, and stop planning around a reset that no longer
    happens. The pre-transform sequence order above still holds.

Gameplay difference: **Annihilator** ramps *Voidfall* → Void Meteors and did
little outside Meta (sharp in-window play required); **Void-Scarred** ramps
*Burning Blades* with Reap/Cull and lines big hits inside *Student of Suffering*,
so it has more consistent out-of-Meta damage. **12.1 narrowed that gap from the
Annihilator side** — the mastery-for-ability-damage swap is precisely a transfer
of power out of the Meta window, which is where Annihilator's edge sat. Whether
Annihilator is still the default in every scenario is now an open question, not a
settled one; `builds.md` still says S1's answer and has not been re-simmed.

## TODO

- [ ] **Re-pull the Tier-1 APL at 12.1** (`wowkb.simc demon-hunter devourer`,
      both the default and the Void-Scarred variant) and re-derive the priority
      orders. This is the blocker on raising `confidence:` back to medium —
      everything on this page below the "What 12.1 changed" section is
      12.0.7-derived ordering.
- [ ] Re-check the Annihilator-vs-Void-Scarred default after the mastery swap
      (feeds `builds.md`, and the Mastery-heavy stat priority in `gearing.md` —
      Blizzard's stated goal was to let other stats compete).
- [ ] `@verify-ingame` **Final Hour**: patch notes say Voidfall bonuses persist
      **6s**, the 12.1.0.69214 spell tooltip still reads 8s. Time it after a
      3-stack Reap.
- [ ] Sanity-check the opener + Meta window against a top WCL log
      (`wowkb.wcl rankings` → `casts`) — none distilled yet (new spec).
- [ ] Re-distill exact Soul/Fury/Voidfall thresholds from a fuller simc APL dump
      (the sub-list conditions were summarized, not reproduced line-for-line).
- [x] Collapsing Star Soul cost — **30** (resolved 2026-07-14): `abilities.md`
      and the Tier-1 APL agree (the `collapsing_star_stacking` buff caps at 30,
      `stack>=30` / `.max_stack`). Fixed the "35+" in the in-Meta priority above.
- [ ] Confirm Void Ray in-Meta cooldown (14s vs 16s) in-game (still open — the
      12.1 DB2 dump lists no cooldown on the spell at all, so this is unresolved
      rather than answered).

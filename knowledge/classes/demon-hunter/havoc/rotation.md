---
title: Havoc Demon Hunter — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-12
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — CLASSES ▶ DEMON HUNTER / Havoc, 2026-08-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1 APL, simc midnight branch (default = Fel-Scarred) — re-pulled 2026-08-11, still pinned at commit 6e14948 dated 2026-03-13 (NOT retuned for 12.1)
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, page updated to 12.1; priority corrected 2026-08-13 from the page's INTERACTIVE build tool (Fel-Scarred tab) — the static HTML is a 24-item both-heroes union the JS filters; the Fel-Scarred single-target list is 13 items led by Vengeful Retreat (Exergy build). Earlier "leads Aldrachi Reaver" note was wrong (one hero-filtered list, not two).
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7 framing, 2026-07-11
  - https://www.warcraftlogs.com/  # tier 2, top-100 Mythic Imperator Averzian parses, 12.0.7, 2026-08-03 (cast + damage + resourcechange event timelines, n=7)
  - https://www.method.gg/guides/havoc-demon-hunter/interface-and-macros  # tier 3, 12.0.7, 2026-08-03
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-macros-addons  # tier 3, 12.0.7, 2026-08-03
confidence: medium
---

# Havoc Demon Hunter — Rotation (Midnight 12.1)

Distilled from the SimulationCraft default APL (Tier 1) with method.gg /
Icy Veins (Tier 3) for framing. The simc default profile is **Fel-Scarred**
(`talents=...Fel-Scarred`), but the single APL carries both hero trees'
lines (Aldrachi Reaver's `reavers_glaive` / `rending_strike` / `glaive_flurry`
and Fel-Scarred's `demonsurge` / `abyssal_gaze`).

> ⚠ **The shape of the loop below is unchanged by 12.1; the tuning underneath it
> is not.** 12.1 retuned Fury generation, moved Inner Demon, deleted Dash of
> Chaos, and put a **weapon-type requirement** on three core abilities — see
> *What changed in 12.1* immediately below. Two caveats on the sourcing:
> - the **simc MID1 APL is still pinned at a 2026-03-13 commit** (re-pulled
>   2026-08-11, unchanged), so every APL condition quoted here is a **pre-12.1**
>   condition and has not been re-derived against the new Fury/Inertia numbers;
> - **Fel-Scarred was the S1 recommendation**, and that ranking has *not* been
>   re-verified for Season 2. Icy Veins does not lead with either hero tree: its page
>   carries **one hero-filtered priority tool**, not an AR-led list, and picking
>   Fel-Scarred renders a 13-item Vengeful-Retreat-led list. Treat hero-tree choice as
>   open until `builds.md` is re-sourced; both branches are documented below.

## What changed in 12.1 (2026-08-11)

Tier-1, verbatim-archived in `_meta/patch-notes/12.1.md` (CLASSES ▶ DEMON
HUNTER ▶ Havoc). Blizzard's own framing of the Fury block: *"a small overall
increase, paced more smoothly and relying less heavily on Immolation Aura's
talent effects."*

**⛔ Weapon requirement — the one that can silently break your rotation.**
**Demon Blades, Blade Dance and Chaos Strike now require equipped Warglaives,
Axes, Swords or Fist Weapons.** Demon Hunters *can* now equip **daggers** in
12.1 (added so Devourer can take Intelligence daggers) — so for the first time
it is possible to equip a weapon that turns off your Fury generator, your AoE
button and your Fury dump at once. Death Sweep / Annihilation are the demon-form
forms of Blade Dance / Chaos Strike and go with them. **Never equip a dagger on
Havoc.**

| Thing | 12.0.7 | 12.1 |
|---|---|---|
| Burning Hatred (Immolation Aura Fury) | +40 | **+30** |
| Demon Blades (per attack) | 8–15 Fury | **10–16** |
| Blind Fury (Eye Beam, per sec, per rank) | 15 / 30 | **10 / 20** |
| Inertia | +18% for 5s | **+12% for 6s** |
| Blade Dance / Death Sweep / Chaos Strike / Annihilation | — | **+6% each** |
| The Hunt | — | **+12%** |
| Essence Break (initial hit) | — | **+49%** |
| Immolation Aura | — | **−8%** |
| Trail of Ruin | damage as a 4s DoT | **applied immediately** |
| Serrated Glaive | 15s **debuff on the target** | **12s buff on you** |
| Inner Demon | choice node with Chaotic Transformation | **choice node with Chaos Theory** |
| Dash of Chaos | talent | **removed entirely** |
| Never Say Die | — | **new talent**: +3% damage above 50% HP, +5% leech below 50% |

What that means at the keyboard:

- **Immolation Aura's rotational pull is weaker in both directions** — 8% less
  damage *and* 10 less Fury per Burning Hatred proc — while your spenders gained
  6%. The "don't sit on 2 IA charges" rule survives (it is still the one Fury
  decision that matters, see the logs section), but IA is no longer the Fury
  engine it was; **Demon Blades is** (and it went up).
- **Inertia is a flatter, wider window**: 12% over 6s instead of 18% over 5s. The
  extra second means you are no longer racing to cram the amp into one Eye Beam
  cast, but the payoff for perfect alignment is a third smaller. Do not contort.
- **Essence Break's initial hit is now a real chunk of the ability** (+49%), on
  top of the ~4s amp window. Pressing it on cooldown-with-Fury-banked matters
  more than it did; wasting the window matters the same.
- **Serrated Glaive no longer lives on a target.** It is a buff on you, so it
  **carries across target swaps and into cleave** instead of needing to be
  re-applied per mob — one less thing to track in M+ and funnel.
- **Trail of Ruin is front-loaded**, so its cleave contribution lands with the
  Blade Dance rather than trickling for 4s. Its APL role is unchanged: it still
  drops the Blade Dance AoE gate to **2+ targets** (`active_enemies>=3-talent.trail_of_ruin`).
- **Chaotic Transformation is now a standalone passive**; Inner Demon moved off
  it and onto the **Chaos Theory** choice node. So the "Metamorphosis resets Eye
  Beam + Blade Dance" behaviour below is now available without giving up Inner
  Demon — a build question, but it makes the cooldown rule below more reliably
  true.
- **Dash of Chaos is gone.** Any older opener/macro list naming it is dead text.

Game-wide 12.1 changes that land on this spec: **player health and creature
damage are both +25% at max level** (so absolute HP/healing numbers written
before 2026-08-11 are wrong — Never Say Die's 50%-health thresholds are
percentage-based and unaffected); **Disrupt now shows a "missed" visual + sound**
when you kick nothing; **diminishing-return categories reset after 20s** (was
16s), which lengthens Chaos Nova / Imprison / Sigil of Misery DR chains.

## Season 2 meta correction: Exergy over Inertia (2026-08-12)

The 12.1 tuning table above carries the *Inertia nerf numbers* but the loop below
was still written Inertia-first (S1 framing). Season 2's recommended mover pick is
**Exergy** (though **Inertia remains a live alternative** — see the first bullet),
and that changes how Vengeful Retreat is pressed. This agrees with `builds.md`'s 12.1
choice-node table (Tier 3, Icy Veins 12.1 page, re-checked 2026-08-12); folded into
the rotation here so the two files agree.

- **Exergy is the recommended pick — but Inertia is not dead.** The live Icy Veins
  12.1 page (re-checked 2026-08-12) calls **Exergy** (206476) *"the go-to pick in
  Season 2,"* a flat **+5% damage for 20s** that **The Hunt and Vengeful Retreat
  apply directly** (no Fel Rush / Felblade follow-up), with *"100% uptime."* ⚠ But
  the **same page's rotation still leans on Felblade-with-Inertia near the top of the
  priority** (and its opener triggers Inertia) — so treat **Inertia** (427640, now
  **+12%/6s**, cashed by Fel Rush/Felblade after a VR/Hunt) as a **live alternative**,
  not legacy text. My earlier draft over-flattened this. The pick is real; Exergy
  leads. ⚠ Day-one, unsimmed — Season 2 opens 2026-08-18; Tier-3 consensus, not a
  simmed result (`builds.md` carries the same caveat).
- **Vengeful Retreat is a maintain-on-cooldown button either way.** VR is pressed
  **on cooldown** in both builds — it always refreshes **Initiative** crit, and it
  triggers your mover talent: under **Exergy** its ~20–25s cooldown covers Exergy's
  20s for ~full uptime; under **Inertia** it arms the next Fel Rush/Felblade amp. So
  the "earlier cap drafts missing VR" gap was real regardless of the mover pick —
  VR is a core rotational press, not situational movement.
- **Essence Break is mandatory in S2.** +49% initial hit in 12.1, and the Season 2
  tier set keys off it (Tier-3 claim, see `gearing.md`/`builds.md`) — press it on
  cooldown with Fury banked and flood the ~4s window with Death Sweep + Annihilation.
- **Apex → Eternal Hunt.** The sanctioned apex/capstone spend is **Eternal Hunt**
  (1270898: The Hunt empowers your next Eye Beam, +100% damage / wider area),
  which welds The Hunt into the Eye Beam cadence rather than reducing its cooldown.
- **Dancing with Fate is the sanctioned low-mover fallback.** A player who does not
  want to weave VR/movers precisely takes **Dancing with Fate** (389978, +25% on
  Blade Dance's final slash) — a pure passive that asks nothing of movement timing.

Everything below still describes the loop; where it says "Inertia trigger," that is
the Inertia build — on the Exergy build read it as "press Vengeful Retreat on cooldown
to hold Exergy."

**The core loop:** everything orbits the **demon-form window**. Eye Beam (and
Metamorphosis) put you in demon form; while transformed your Chaos Strike →
**Annihilation** and Blade Dance → **Death Sweep** hit far harder. The job is
to keep Eye Beam and Metamorphosis rolling, press **Vengeful Retreat** on cooldown
(to hold **Exergy** +5% and refresh **Initiative**) around each Eye Beam, dump
**Essence Break** windows into Death Sweep + Annihilation, and never Fury-starve
your spenders or let Blade Dance / Immolation Aura charges cap.

## Pre-combat

- **Immolation Aura** ~1s before the pull (Fel-Scarred: spend **both** charges,
  2–3s out — `A Fire Inside`).
- Snapshot stats; pot on the pull (see cooldowns).

## Cooldown rules

- **Potion of Recklessness + on-use trinket** on the pull, then aligned to Eye
  Beam / Metamorphosis windows (the APL gates trinkets on `cooldown.eye_beam.up`
  and Meta being active). Don't bank a use past its cooldown.
- **Metamorphosis** every ~2 min, held to line up with an Eye Beam window
  (**Chaotic Transformation** resets Eye Beam + Blade Dance on cast) and **not**
  while a Demonsurge Annihilation/Death Sweep is still pending.
- **The Hunt** on cooldown, kept **out of** Essence Break windows and (with
  **Eternal Hunt**) synced so its cooldown reduction feeds the next Eye Beam.
  Fel-Scarred sends The Hunt + Meta before the next Eye Beam for trinket value.
- **Essence Break** is a ~4s amp window *plus* a hard initial hit (**+49% in
  12.1**) — open it with Fury banked (≥35) and immediately fill it with **Death
  Sweep** and **Annihilation** (Chaos Strike outside meta). Don't cast anything
  weak inside it.
- **Vengeful Retreat**: **press it on cooldown** to maintain **Exergy** (+5% for
  20s, the S2 pick) and refresh **Initiative** (crit), aligning it around Eye Beam;
  the APL cancels its movement when it's used to reposition into Metamorphosis.
  (On the Exergy build VR's mover job is to hold the flat 5%; on the Inertia build
  VR/The Hunt arm a **+12%/6s** Fel Rush/Felblade empower instead. Both are current —
  see the *Season 2 meta correction* above.)

## Single target (Fel-Scarred)

Opener (method.gg — ⚠ this is the **Inertia-build** opener (a current build); on the
Exergy build the Felblade presses below are just Fury/filler and you press Vengeful
Retreat on cooldown for Exergy instead of to arm an Inertia amp):
Immolation Aura (pre-pull ×2) → pot+trinket → **Eye Beam** → **The Hunt** →
**Felblade** (triggers Inertia) → **Death Sweep** ×2 → **Annihilation** →
**Vengeful Retreat + Metamorphosis** → Death Sweep → Annihilation → **Consuming
Fire** → Felblade (Inertia) → **Abyssal Gaze** → Death Sweep ×2 → Annihilation.

Sustained priority (Fel-Scarred), read 2026-08-13 off the live Icy Veins 12.1 page's
**interactive build tool with Fel-Scarred selected** — the 13-item list below.

> ⚠ **Sourcing gotcha — how to read that page.** Its *static HTML* carries a **24-item
> union** of both hero trees' lines (Reaver's Glaive, duplicate Metamorphosis/Vengeful
> Retreat entries, both Inertia and Exergy). That union is **not the Fel-Scarred
> priority** — the page's JavaScript build-selector **filters and re-orders** it per the
> chosen hero. So `wowkb.fetch` of the raw page returns the superset (Metamorphosis #1),
> not the Fel-Scarred view; the real Fel-Scarred list must be read from the **rendered
> tool (Fel-Scarred tab)**. There is **one list**, hero-filtered — not one per hero tree.
> The filtered Fel-Scarred list leads with **Vengeful Retreat**, and it is the **Exergy
> build** (no Inertia-Felblade rung).

1. **Vengeful Retreat** to trigger **Exergy** — it leads because it is **off the GCD** and
   holds Exergy at ~100% uptime, so you weave it whenever it is up (free). Align with Eye Beam
   for **Initiative**.
2. **Metamorphosis** when Eye Beam **and** Death Sweep are both on cooldown
   (**Chaotic Transformation** resets them — that's the payoff).
3. **The Hunt** — **hold to buff Abyssal Gaze if Metamorphosis is available** (a *readable*
   condition: Meta's cooldown state), else cast on cooldown.
4. **Death Sweep** during an **Essence Break** window or with **Demonsurge** active.
5. **Annihilation** with **Demonsurge** active.
6. **Eye Beam / Abyssal Gaze** — consume any Annihilation / Death Sweep procs of Demonsurge
   first.
7. **Essence Break** — **hold if Eye Beam's cooldown has ≤4s remaining** (don't clip the
   window into Eye Beam).
8. **Death Sweep / Blade Dance** as the baseline spender.
9. **Consuming Fire** with **Demonsurge** active (Fel-Scarred, in Meta).
10. **Annihilation / Chaos Strike** as the raw Fury dump — low, climbs only via the windows
    above.
11. **Immolation Aura / Consuming Fire** (don't sit at 2 charges; dump both before Meta so
    **A Fire Inside / Demonic Intensity** refunds them).
12. **Felblade** for Fury when nothing above is up.
13. **Fel Rush** with nothing else available.

*(Throw Glaive is not in the Fel-Scarred priority — it's a rarely-cast filler unless
**Screaming Brutality** is taken, in which case Blade Dance triggers it rather than a hard
cast. With **Serrated Glaive** it buffs *you* for 12s rather than debuffing the target.)*

## Cleave / AoE (3+)

Largely the single-target loop with these shifts (APL `use_blade_dance` triggers
at **3+ targets**, or 2+ with **Trail of Ruin** — whose damage is now applied
immediately rather than over 4s — or always with First Blood):

1. **Immolation Aura** early and kept rolling — it's still a top AoE source with
   **Ragefire** / **A Fire Inside**; the APL fires extra Immolation Auras at
   `active_enemies>2`. (12.1: **−8% damage**, and the APL condition predates
   that — the ordering here is unverified against 12.1 tuning.)
2. **Blade Dance / Death Sweep** become primary — they trigger the **Glaive
   Tempest** passive at 3+ targets. Keep them on cooldown.
3. **Eye Beam** — at 5+ targets its raw AoE outweighs alignment; the APL drops
   the `eb_aligned` gate at `active_enemies>=5` and just casts it.
4. **The Hunt** on cooldown (higher relative value in AoE).
5. **De-emphasize Chaos Strike / Annihilation** as single-target Fury dumps —
   spend into Blade Dance instead.
6. With **Burning Wound**, tab-target to spread the debuff — **your auto-attacks do the
   applying, not a button**. The tooltip reads *"Demon's Bite and Throw Glaive leave open
   wounds"*, and under baseline **Demon Blades** the Demon's Bite effect arrives through
   auto-attacks, so switching target is what moves the wound. The APL spreads it with
   `retarget_auto_attack` up to `min(spell_targets, 3)`
   `[T1 simc: MID1_Demon_Hunter_Havoc.simc:41-43]`.
   ⚠ **It is gated on a user toggle**, `variable.tab_target_burning_wound` (default `1`)
   `[T1 simc: :25]` — simc puts a line behind a switch when it models a *manual play cost*
   rather than a rotational fact. So the talent's simmed value assumes you actually tab-target;
   if you don't, it is worth materially less than the default sim says.
7. **Metamorphosis** + Essence Break as the AoE burst, same rules.

## Hero-tree branches

### Fel-Scarred (default)

- Each demon-form entry should spend the **Demonsurge** empowerment: two
  **Death Sweep** (via Eternal Hunt) and one **Annihilation** per window.
- **Demonic Intensity** during Meta gives the empowered **Abyssal Gaze**
  (Eye Beam) and **Consuming Fire** (Immolation Aura) — spend Immolation charges
  before Meta so Demonic Intensity refreshes them.
- **Exergy** (via The Hunt / Vengeful Retreat, S2 pick) is a flat **+5% for 20s**
  held by pressing VR on cooldown — no Felblade/Fel Rush follow-up. The legacy
  **Inertia** amp (**+12% for 6s** in 12.1, cashed by Fel Rush/Felblade) is the
  alternative on that choice node but lost the S2 comparison (see the *Season 2
  meta correction*).

### Aldrachi Reaver

- Build 6 soul fragments (**Art of the Glaive**) → Throw Glaive becomes
  **Reaver's Glaive**. Cast it to apply **Reaver's Mark** on the priority target
  early, then spend the **Rending Strike** (empowered Chaos Strike/Annihilation)
  and **Glaive Flurry** (empowered Blade Dance/Death Sweep → **Fury of the
  Aldrachi** slashes) it grants.
- **The Hunt every ~min** guarantees a Reaver's Glaive proc.
- Funnel comes from **Wounded Quarry** repeat Death Sweeps into the Reaver's
  Mark target; in AoE, tab-target to keep **Burning Wound** spread.
- Priority (method.gg): Reaver's Glaive → Vengeful Retreat → The Hunt (if
  Reaver's Glaive unavailable) → Death Sweep → Eye Beam → Metamorphosis →
  Annihilation → Blade Dance → Chaos Strike → Immolation Aura → Felblade.

## TODO

- [x] ST + AoE priority from simc midnight APL (2026-07-11) + method.gg
- [x] Both hero-tree branches captured (Fel-Scarred default, Aldrachi Reaver)
- [x] 12.1 tuning + talent-tree changes folded in against Tier-1 notes (2026-08-11)
- [x] **Season 2 mover-meta swing folded in (2026-08-12)** — Exergy over Inertia,
      Vengeful Retreat as a maintain-on-cooldown press; agrees with `builds.md`'s
      12.1 choice-node table (Tier 3, Icy Veins). Closed the S1 Inertia-first framing.
- [x] **VR-on-cooldown centrality + Essence-Break-mandatory / Eternal-Hunt-apex /
      Dancing-with-Fate low-mover fallback documented (2026-08-12).** These were the
      gaps that left Vengeful Retreat out of earlier Combat Assist Plus drafts.
- [ ] Sanity-check the opener against a top WCL Havoc log (`wowkb.wcl`)
- [ ] **Re-distill when the simc midnight branch publishes a 12.1 APL.** Checked
      2026-08-11: still commit `6e14948` (2026-03-13), i.e. pre-12.1. Every APL
      condition on this page is therefore untuned for the new Fury/Inertia
      numbers.
- [ ] **Re-verify the hero-tree recommendation for Season 2** (`builds.md`) —
      Fel-Scarred-first is an S1 claim; Icy Veins' 12.1 page leads Aldrachi
      Reaver. Needs Tier-1/Tier-2 evidence, not day-1 editorial.
- [ ] Re-measure Fury waste on 12.1 parses once Season 2 logs exist (2026-08-18+)
      — the table below is 12.0.7 and the generation retune invalidates its
      magnitudes.


## What the logs say — measured from real parses (Tier 2, 2026-08-03)

⚠ **These are 12.0.7 measurements, taken before the 12.1 Fury retune** (Burning
Hatred 40→30, Demon Blades 8–15→10–16, Blind Fury 15/30→10/20). The *conclusions*
below still hold — Fury is not a tightly managed resource, Demon Blades dominates
generation, VR's positioning cost is negligible — but **treat the specific
percentages as historical**, not as 12.1 numbers.

Pulled from the **top-100 Mythic Imperator Averzian** rankings (WCL, 12.0.7): full cast,
damage and `resourcechange` event timelines for **7 parses**, 47 Vengeful Retreats.

### Fury management is close to a non-issue for this build

| player | Fury gained | wasted (overcap) | waste |
|---|---:|---:|---:|
| Paprzdh | 4,119 | 311 | 7.6 % |
| Yunadh | 4,345 | 482 | 11.1 % |
| Bibussy | 5,612 | 708 | 12.6 % |
| Chezzar | 5,386 | 1,237 | 23.0 % |
| **pooled** | **19,462** | **2,738** | **14.1 %** |

**Top players waste roughly one Fury in seven** (12.0.7), and the dominant source is
**Demon Blades** — a *passive* off autoattacks that no rotation decision can gate — with
Immolation Aura's ticks second. This is why the guides carry almost no Fury advice: the
only Fury instruction maxroll gives is *"Cast Immolation Aura if you won't overcap on
fury"*. Practical reading: **do not treat Fury as a resource to be managed tightly.** The
one decision that matters is not sitting on capped Immolation Aura charges.

12.1 moves this the *right* way without changing the conclusion: Blizzard shifted
generation **off** Immolation Aura (Burning Hatred 40→30) and **onto** Demon Blades
(8–15→10–16), calling it "a small overall increase, paced more smoothly." More of your
Fury now comes from the ungateable passive and less from the button whose overcap you
were being told to avoid — so the overcap share is unlikely to fall much, and the advice
stands.

⚠ Fury's max measured **170** on these characters (`maxResourceAmount` in the raw events),
not the 120 class base — it is talent-inflated.

### Vengeful Retreat: what actually follows it

VR is **off the global cooldown** (since patch 8.1.0), so it is woven into another
ability's GCD rather than costing a press. It does, however, impose a short lockout on
**Felblade and Fel Rush** specifically.

First ability cast after each VR (n=47):

| followup | share | median delay | range |
|---|---:|---:|---|
| **Felblade** | 46.8 % | **0.86 s** | 0.69–1.04 |
| **Fel Rush** | 23.4 % | **1.07 s** | 0.97–1.41 |
| **Metamorphosis** | 17.0 % | 1.14 s | 0.30–1.37 |
| other (Consuming Fire / IA / BD / EB) | 12.8 % | ~0.8 s | — |

Felblade at 0.86 s is **one hasted GCD** — no waiting, because its lockout is shorter than
a global. Fel Rush's delays cluster hard against **1.0 s** (`0.97, 0.99, 1.01, 1.02, 1.03,
1.07, 1.07, …`), which is its lockout to the millisecond: players press it the instant it
is legal. Metamorphosis at 17 % is the animation-cancel technique — VR backward, Meta
leaps you back in.

**Nobody macros VR.** Neither method.gg (10 macros) nor Icy Veins (6) lists one at 12.0.7;
it stays a hand-pressed button because the movement is situational.

### The positioning cost is real, and irrelevant

Melee swings landed in the 5 s after a VR (baseline 5.34 expected):

| | swings | vs baseline |
|---|---:|---:|
| VR alone (n=36) | 4.92 | −8 % |
| **VR → Fel Rush ≤2 s** (n=11) | 2.82 | **−47 %** (≈2.5 swings lost) |

So the pair does cost ~2.5 autoattacks — players are **not** threading a needle. But
**autoattacks are only ~3.1 % of Havoc damage** (2.8–3.6 % across parses), so 2.5 swings is
≈ **0.05 % of a pull**. Against that, VR resets **Initiative** (+crit) on every hostile
target. Take the retreat; do not contort to save the swings.

## Changelog

2026-08-17 — Icy Veins carries one hero-filtered priority tool, not an Aldrachi-Reaver-led
list, and the Fel-Scarred priority is the tool's 13-item Vengeful-Retreat-led (Exergy) list;
earlier drafts transcribed the static page's 24-item both-hero union (Metamorphosis #1).

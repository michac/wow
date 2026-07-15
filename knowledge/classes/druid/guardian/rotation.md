---
title: Guardian Druid — Rotation & Priority (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Druid_Guardian.simc  # tier 1 APL (actions.bear / actions.cooldowns), WoW 12.0.x
  - https://www.method.gg/guides/guardian-druid/playstyle-and-rotation  # tier 3, 12.0.7 upd. 2026-06-16 (Tactyks)
  - https://www.icy-veins.com/wow/guardian-druid-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: high
---

# Guardian Druid — Rotation (Midnight S1)

Distilled from the **SimulationCraft default APL** (Tier 1, `actions.bear` +
`actions.cooldowns`), corroborated by the method.gg 12.0.7 rotation page and Icy
Veins. Guardian is a **rage tank**: keep the two generators (**Mangle**,
**Thrash**) rolling, hold **Thrash at max stacks**, maintain **Moonfire**, and
spend rage on **Ironfur** (defensive) or **Maul / Raze** (offensive) without
rage-capping. Almost everything worth pressing is off-GCD or a generator on
cooldown, so the "priority" is really *don't waste a generator cast and don't
overflow rage.* The APL branches by **hero tree** (Elune's Chosen vs Druid of
the Claw) and by enemy count.

## Pre-combat

- Be in **Bear Form** (Cat Form if running Heart of the Wild, per the APL
  precombat).
- Pre-pot **Light's Potential** (or Draught) timed into the opener.
- Snapshot stats; pre-place any on-use trinket (Algethar Puzzle Box in the
  sim profile).

## Opener (method.gg)

Barkskin → **Lunar Beam** → potion → Rake → **Heart of the Wild** →
**Incarnation** (or Berserk) → **Wild Guardian** → Thrash → **Red Moon** →
Mangle → **Ironfur** → Mangle → Thrash → into the standard priority. The goal is
to get an Ironfur rolling ASAP and start consuming procs while dumping cooldowns.

## Cooldown rules

There are four majors: **Barkskin**, **Survival Instincts**, **Berserk /
Incarnation**, and **Lunar Beam**.

- **Never overlap Barkskin and Survival Instincts** — the reductions are
  multiplicative, so stacking them wastes total coverage. Stagger them across a
  damage profile.
- **Incarnation/Berserk and Lunar Beam are damage gains as well as defensives** —
  unless you need one to survive a specific hit, press them near on cooldown.
- **Lunar Beam** (APL): use when Incarnation/Berserk is available, or when they
  are >60s out (>30s with **Lunation**). With Lunation it becomes a near-CD button.
- **Convoke the Spirits** (if talented over Incarnation): press in Bear Form,
  gated behind the Lunar Beam window when running Lunation.
- **Frenzied Regeneration**: press *before* incoming damage; with **Natural
  Resilience** the overheal becomes an absorb.
- **Ironfur**: keep **≥1 stack up whenever taking physical damage**. Extra casts
  add stacks (more armor) but don't refresh — don't spam-overwrite.
- **Bristling Fur**: fire when both generators are on CD and rage is low (APL:
  rage<40, or <60 with Killing Blow) and no Ravage proc is up — a rage refill.
- **Sundering Roar**: press once Thrash is above its stack threshold (>2, or
  >3/>4 with Flashing Claws ranks).
- **Wild Guardian** (capstone): fire during a **Ravage** proc (Druid of the
  Claw) or a **Lunar Beam** window (Elune's Chosen) — i.e. line it up with burst.
- Potion/racials while **Lunar Beam is up**; sync on-use trinkets to the
  Incarnation/Lunar Beam window.

## Single target — Elune's Chosen (S1 M+ default)

1. **Thrash** to keep **3+ stacks** (Lunar Calling makes Thrash the opener).
2. **Lunar Beam** on cooldown (Lunation → treat as a core rotational button).
3. **Mangle** on cooldown.
4. **Maul / Raze** when **above ~80 rage** (offensive dump; don't cap).
5. **Ironfur** to spend rage / stay defended (off-GCD, alongside the above).
6. **Moonfire** as filler — with **Lunation** every Moonfire shaves Lunar
   Beam's cooldown. *Moonfire pushes Swipe out of the rotation but must never
   take priority over Mangle.*

## Single target — Druid of the Claw (standard, no weaving)

1. Maintain **Moonfire** DoT.
2. Maintain **3+ Thrash** stacks (more with Flashing Claws).
3. **Maul / Raze / Ravage** when **above ~60 rage** (consume **Ravage** procs).
4. **Mangle** on cooldown.
5. **Thrash** on cooldown.
6. Proc'd **Galactic Guardian Moonfire** (free instant).
7. **Swipe** as filler.

## Cleave / AoE

Same generator-first skeleton, favoring the AoE spender:

1. **Thrash** on cooldown (and to max stacks) — AoE bleed + Lunar Beam CDR.
2. **Mangle** on cooldown.
3. **Lunar Beam** on cooldown (Elune's Chosen) / **Wild Guardian** + **Red Moon**
   window (Druid of the Claw).
4. **Heart of the Wild** in Cat Form (bosses / ≤5) or **Moonkin Form** (6+ trash,
   per the APL — Moonkin HotW spreads Moonfire).
5. **Sundering Roar** at high Thrash stacks.
6. Spend excess rage on **Raze** (frontal AoE dump) or **Ironfur**.
7. **Moonfire** as filler (Elune's Chosen; reduces Lunar Beam CD) / **Swipe**
   filler (Druid of the Claw).
8. **Twin Moonfire + Galactic Guardian** make Moonfire spread strong at 2+
   targets (see `builds.md`).

## Hero-tree branches

### Elune's Chosen
- Built around **Lunar Beam** + **Moonfire**; **Lunation** turns Thrash and
  Moonfire into Lunar Beam CDR, so Lunar Beam is pressed close to on-cooldown.
- Simplest playstyle; the S1 M+ default (Thrash synergy buffed it above Druid
  of the Claw). Moonfire is a real rotational filler here, not just a DoT.

### Druid of the Claw
- Adds the **Ravage** proc (empowers Maul/Swipe) and, optionally, **catweaving /
  ripweaving**: with **Fluid Form** + **Heart of the Wild** up you shift to Cat
  Form for **Rip**/**Ferocious Bite** empowered by **Feline Potential** stacks,
  then shift back to bear.
  - **Catweave ST priority (APL):** Maul/Raze/Ravage >80 rage → **Ferocious Bite
    with 6 Feline Potential** if empowered Rip >8s → **Rip with 6 Feline
    Potential** → Ferocious Bite/Rip with combo points → Mangle → Thrash →
    Galactic Guardian Moonfire → maintain Rake/Shred in Cat → Swipe filler.
  - **Ripweaving** (via **Wildpower Surge**) applies an empowered Rip without a
    full cat window — safer than traditional catweaving while tanking.
  - ⚠ **Rage resets to 25 on shifting back into Bear Form** — dump rage below 25
    before you shift out, or you waste it. @verify-ingame
- Catweaving is a modest, execution-heavy gain; **skip it while progging / when
  survival is tight** and just play the standard priority above.

## Rage economy (why the priority is shaped this way)

- Build from **Mangle**/**Thrash**, auto-attacks, and being hit; **+25 rage** on
  entering Bear Form.
- The more rage you *spend*, the more **Ursoc's Guidance** CDR and **After the
  Wildfire** healing you get → more Incarnation/Lunar Beam uptime. So spending
  (Maul/Raze/Ironfur) is throughput *and* CD generation — never sit rage-capped.
- **Harnessed Rage**: spending an offensive dump above ~80 rage raises the
  **Gore** proc chance to reset **Mangle**.

## TODO

- [ ] Sanity-check opener/CD windows against a top WCL Guardian log
      (`wowkb.wcl rankings` → `casts`).
- [~] Re-distill numeric thresholds once a 12.0.7-stamped simc midnight APL
      publishes (current APL rage thresholds captured above are from the
      midnight-branch profile; exact rage costs of Ironfur/Maul flagged
      @verify-ingame in `abilities.md`).

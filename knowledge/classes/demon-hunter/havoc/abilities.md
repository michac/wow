---
title: Havoc Demon Hunter — Ability Inventory (Midnight 12.1)
patch: 12.1
fetched: 2026-08-26
reviewed: 2026-08-26
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes — the CLASSES > DEMON HUNTER > Havoc list
  - knowledge/_meta/patch-notes/12.1.md  # tier 1 verbatim archive of the above
  - knowledge/classes/demon-hunter/havoc/ability-inventory.tsv  # tier 1, DB2 @ 12.1.0.69214 + Blizzard Game Data API spell descriptions — names, spellIDs, origin, cooldowns
  - knowledge/classes/demon-hunter/havoc/talents.md  # tier 1, Trait* DB2 @ 12.1.0 — node existence + choice-node pairings
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06 (build-pinned 12.0.7.67808 where noted)
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Demon_Hunter_Havoc.simc  # tier 1, simc midnight branch APL + default profile (Fel-Scarred), 2026-07-11 — PRE-12.1, colour only
  - https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7-era, 2026-07-11 — colour only, superseded wherever the 12.1 notes disagree
  - https://www.method.gg/guides/havoc-demon-hunter/playstyle-and-rotation  # tier 3, 12.0.7-era, 2026-07-11 — colour only
  - raw/wago/SpellName-12.1.0.69214.csv  # tier 1, spell-ID anchors @ build 12.1.0.69214
  - raw/wago/Spell-12.1.0.69214.csv  # tier 1, spell + aura description text @ build 12.1.0.69214
  - raw/wago/SpellEffect-12.1.0.69214.csv  # tier 1, effect/aura types + implicit targets @ build 12.1.0.69214
  - raw/wago/SpellMisc-12.1.0.69214.csv  # tier 1, DurationIndex @ build 12.1.0.69214
  - raw/wago/SpellDuration-12.1.0.69214.csv  # tier 1, aura durations @ build 12.1.0.69214
  - raw/wago/CooldownSetSpell-12.1.0.69214.csv  # tier 1, Cooldown-Manager rows @ build 12.1.0.69214
confidence: high
---

# Havoc Demon Hunter — Ability Inventory (Midnight 12.1)

## Overview

Havoc is the melee-DPS Demon Hunter spec. Its resource is **Fury** (0–120+),
generated mostly passively (auto-attacks via **Demon Blades**, plus **Immolation
Aura** ticks) and spent on **Chaos Strike** (single-target) and **Blade Dance**
(AoE). The whole spec is built around the **demon-form (Demonic) window**:
casting **Eye Beam** briefly transforms you, and while transformed Chaos Strike
and Blade Dance are replaced by the stronger **Annihilation** and **Death Sweep**.
**Metamorphosis** is the big transform on a 120s cadence. High mobility
(Fel Rush, Vengeful Retreat, Felblade, The Hunt) is core to both damage and
positioning.

Two hero trees:

- **Fel-Scarred** — the pre-12.1 default (the simc profile is `..._Fel-Scarred`).
  Adds **Demonsurge** (Eye Beam/Meta empower next Annihilation + Death Sweep) and,
  via **Demonic Intensity**, the empowered forms **Abyssal Gaze** (Eye Beam) and
  **Consuming Fire** (Immolation Aura). Frontloads burst inside Metamorphosis.
- **Aldrachi Reaver** — collect 6 soul fragments (via **Art of the Glaive**) to
  turn Throw Glaive into **Reaver's Glaive**, which applies **Reaver's Mark** and
  empowers the next Chaos Strike (**Rending Strike**) and Blade Dance
  (**Glaive Flurry** → **Fury of the Aldrachi** slashes). Strong funnel/cleave.

> Midnight note: a **third** Demon Hunter spec, **Devourer**, is live and has its
> own folder. This file is Havoc only.

## What 12.1 changed

**⚠ Weapon requirement — the one that can silently turn the spec off.**
**Demon Blades, Blade Dance and Chaos Strike now require an equipped Warglaive,
Axe, Sword or Fist Weapon.** Separately, 12.1 made **daggers equippable by Demon
Hunters** — that change exists so **Devourer** can use Intelligence daggers, and
**daggers are not on the required-weapon list**. So a Havoc who picks up a dagger
loses their core spender, their AoE spender *and* their passive Fury generation.
*[Tier 1: 12.1 notes, DEMON HUNTER preamble + Havoc list.]*

**Fury retune** — Blizzard's stated intent is *"a small overall increase, paced
more smoothly and relying less heavily on Immolation Aura's talent effects"*:

| Source | 12.1 | was |
|---|---|---|
| **Burning Hatred** (Immolation Aura bonus Fury) | **+30** | +40 |
| **Demon Blades** (per attack) | **10–16** | 8–15 |
| **Blind Fury** (Eye Beam, per second) | **10 / 20** | 15 / 30 |

**Damage tuning:** Blade Dance **+6%** · Death Sweep **+6%** · Chaos Strike
**+6%** · Annihilation **+6%** · The Hunt **+12%** · Essence Break **initial
damage +49%** · Immolation Aura **−8%**. Net: the spender core and the burst
buttons went up, the aura came down — consistent with the Fury note above.

**Talent changes:**

- **NEW — Never Say Die** (`427794`, spec row 4 col 15): damage **+3% while
  above 50% health**; leech **+5% while below 50% health**. A low-gate passive
  next to Improved Chaos Strike.
- **Trail of Ruin** (`258881`): the final slash of Blade Dance now inflicts its
  extra Chaos damage **immediately**, instead of as a DoT over 4 seconds. Same
  budget, no ramp — it now lands inside an Essence Break window.
- **Serrated Glaive** (`390154`): now a **buff on you, 12s**, instead of a 15s
  debuff on the target — striking with Chaos Strike or Throw Glaive increases
  Chaos Strike and Throw Glaive damage by **15%**. This flips it from a
  per-target debuff you had to re-apply on swaps into a personal window, which
  makes it materially better in dungeon pulls.
- **Inner Demon** (`389693`) **moved**: it is now the choice-node partner of
  **Chaos Theory** (`389687`) at spec row 9 col 16. It used to sit opposite
  **Chaotic Transformation**, which is now a standalone passive at 9,18 — so you
  can take Chaotic Transformation *and* Inner Demon together, and you can no
  longer take Inner Demon alongside Chaos Theory.
  *[Tier 1: `talents.md` / `_talents/all-talents.tsv` @ 12.1.0.]*
- **Inertia** (`427640`, the talent passive): **+12% damage for 5 seconds** (was
  18%) — a smaller window, worth less at its peak. `427640` itself grants
  nothing: both its `SpellEffect` rows are `Effect=6 EffectAura=4` (dummy) on the
  caster, and it has no `SpellMisc.DurationIndex`. The **buff** is a separate
  spell, **`427641`**, and the **armed state** a third, **`1215159`** — see
  **Spell-ID anchors** below, which is also where the 5s comes from
  (`SpellDuration.Duration=5000`). ⚠ The 12.1 patch note prose says **6 seconds**
  and both the client tooltip and DB2 say **5**; number conflicts resolve to game
  data, so 5s stands here. @verify-ingame (Inertia buff duration — 5s or 6s)
- **REMOVED — Dash of Chaos.** Gone entirely. It reaches no trait node on the
  12.1 Demon Hunter tree; three legacy spellIDs (427793 / 428160 / 428393) still
  carry the name in `SpellName`, which is only name residue, not a button.
  *[Tier 1: `_talents/all-talents.tsv` @ 12.1.0 — zero rows; SpellName @
  12.1.0.69214.]*

**Global 12.1 changes that land on this kit** (they sit in the CLASSES preamble,
not under Demon Hunter, and are easy to miss):

- **Player health and creature damage both +25% at max level**, with health
  consumables rescaled and some DPS/Tank healing + absorb retuned. Any *absolute*
  HP or healing number written before 2026-08-11 is now wrong. Percentage
  mitigation — Blur, Darkness, Soul Rending leech — is unaffected as a percentage.
- **Interrupts now show a "missed" visual over the target's head and play a
  distinct sound** when used while the target was not casting. Applies to
  **Disrupt**.
- **Diminishing-return categories now reset after 20 seconds** (was 16) — a
  straight nerf to chaining **Chaos Nova** / **Imprison** / **Sigil of Misery**
  on the same target.
- Blizzard's stated direction is **major DPS cooldowns lowered, steady-state
  damage raised**. No Havoc cooldown was shortened in the 12.1 list, so read that
  as context for other specs rather than as a Havoc change.

## Inventory

> **Where the numbers come from.** `ability-inventory.tsv` in this folder is the
> Tier-1 record for **name, spellID, origin and cooldown** (DB2 @ 12.1.0.69214,
> with Blizzard Game Data API spell descriptions) — read it rather than trusting a
> number restated here. A `[T1]` stamp marks a cooldown taken from it; a `~` value
> is Tier-3 colour from simc / Icy Veins / method.gg, or a value the tsv cannot
> express. The remaining `@verify-ingame` markers mostly ask about **Fury cost**,
> which that file has no column for.
>
> **The demon-form buttons are invisible to Tier 1.** **Annihilation**,
> **Death Sweep**, **Abyssal Gaze**, **Consuming Fire** and **Reaver's Glaive**
> are runtime *overrides* of Chaos Strike / Blade Dance / Eye Beam / Immolation
> Aura / Throw Glaive. They attach to no acquisition table, so they appear in no
> generated inventory — that is a hole in the generator, not evidence they are
> gone. Each parent, and each hero subtree that grants the override, is live on
> tree 854, and each override name still resolves in `SpellName` @ 12.1.0.69214
> (e.g. Annihilation 201427, Death Sweep 210152).
> *[Tier 1: reconcile-ledger.md §4 + §5 G2 @ 12.0.7.67808, re-checked @ 12.1.0.69214.]*
>
> **Demon Blades is in the same blind spot** and is *not* a generator artifact you
> may drop: it reaches no trait node and no `SkillLineAbility` row in our join, yet
> the **Tier-1 12.1 patch notes tune it by name** ("Demon Blades now generates
> 10-16 Fury per attack") and `SpellName` @ 12.1.0.69214 carries it as 203555. The
> notes are the floor here, not the generated inventory.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.1.0.69214).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD. The recharge lives in
> `SpellCategory.ChargeRecoveryTime`, unreachable without breaking the build pin
> (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv wins" applies to the
> values it actually carries, not to every row** — on this spec, Immolation Aura
> (1.5s), Fel Rush (1s), Blur (0.5s), Vengeful Retreat (0.5s) and the four
> zero-cooldown rows all read as artifacts and keep their `~` prose instead.
>
> ⚠ **Vengeful Retreat lost its Tier-1 backing at 12.1.** It read **25s** in the
> 12.0.7.67808 tsv and reads **0.5s** at 12.1.0.69214 — the charge-ability
> artifact — which is consistent with 12.1 giving Devourer's Hungering Slash "a
> temporary charge of Vengeful Retreat". The ~25s below is now carried prose, not
> a measurement. @verify-ingame (Vengeful Retreat cooldown / charges)
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Chaos Strike** | Rotational-spender | ~40 Fury | Instant | Core single-target spender; a **20% chance to refund 20 Fury** (**Critical Chaos** adds 30% of your crit chance to that). Replaced by Annihilation in demon form. **12.1: +6% damage; now requires an equipped Warglaive / Axe / Sword / Fist Weapon.** @verify-ingame (exact Fury cost) |
| **Annihilation** | Rotational-spender | ~40 Fury | Instant | Demon-form (Metamorphosis/Demonic) version of Chaos Strike; higher damage. Consumes **Demonsurge** for Fel-Scarred. **12.1: +6% damage.** |
| **Blade Dance** | Rotational-spender (AoE) | ~35 Fury | Instant, **15s** `[T1]` | Spin dealing AoE around you; the final slash triggers **Glaive Tempest** at 3+ targets (which itself consumes 25 Fury). Replaced by Death Sweep in demon form. **Class-baseline `[T1]`.** The base cooldown is 15s — the ~9s people quote is the *hasted* value, so treat 15s as the floor when planning AoE cadence. **12.1: +6% damage; now requires an equipped Warglaive / Axe / Sword / Fist Weapon.** @verify-ingame (exact Fury cost) |
| **Death Sweep** | Rotational-spender (AoE) | ~35 Fury | Instant, shares Blade Dance's CD | Demon-form version of Blade Dance; higher damage. Consumes **Demonsurge** for Fel-Scarred. **12.1: +6% damage.** |
| **Eye Beam** | Rotational-builder / burst (talent) | ~30 Fury | ~1.8s channel, **30s** `[T1]` | Channel that triggers the **Demonic** demon-form window (5s of demon form after it finishes); primary damage cooldown. **Chaotic Transformation** resets its CD on Meta; **Cycle of Hatred** shaves 2.5s per cast, stacking to 10s; **Eternal Hunt** empowers the next one after The Hunt (+100% damage, wider area); **Furious Gaze** grants +8% Haste for 8s on a full channel. At a 30s base it comes back four times per Metamorphosis, so the Demonic window is the *frequent* one and Meta is what you plan around. **12.1: Blind Fury now feeds it 10/20 Fury per second (was 15/30).** @verify-ingame (exact Fury cost) |
| **Immolation Aura** | Rotational-builder | Free (generates Fury) | Instant, ~30s CD (2 charges w/ **A Fire Inside**, which also cuts 6s off the CD and turns it to Chaos damage) | AoE fire aura over 6s + steady Fury generation; **Ragefire** stores 35% of up to 3 crits' damage to detonate on expiry. **12.1: damage −8%, and Burning Hatred's bonus Fury cut to +30 (was 40) — this is the ability the Fury retune deliberately de-emphasises.** |
| **Felblade** | Movement / builder | Free (generates Fury) | Instant / **12s** `[T1]` | Gap-closer that generates Fury; used to trigger **Inertia** / **Unbound Chaos** before burst windows. |
| **Demon Blades** | Passive (Fury generation) | — | — | Replaces Demon's Bite: auto-attacks generate Fury instead. **12.1: 10–16 Fury per attack (was 8–15); now requires an equipped Warglaive / Axe / Sword / Fist Weapon.** Reaches no acquisition row in our generated data — see the blind-spot note above. |
| **Demon's Bite** | Rotational-builder | Generates Fury | Instant | Baseline Fury builder — **replaced by the passive Demon Blades** in the standard build, so rarely a manual press. |
| **Essence Break** | Rotational (burst amp) | Free | Instant, **40s** `[T1]` | Slash in front of you that makes Chaos Strike and Blade Dance deal bonus Chaos damage **for 4s**; filled with Death Sweep + Annihilation. **12.1: initial damage +49%** — the largest single Havoc buff in the patch, and it shifts a slice of the talent's value from the amp window onto the press itself. |
| **Metamorphosis** | Major cooldown | Free | Instant, **120s** `[T1]` | Leap to target (3s stun on landing; players are Dazed instead), transform for **20s**: **+20% Haste**, empowers Chaos Strike/Blade Dance into Annihilation/Death Sweep, and (w/ **Chaotic Transformation**) resets Eye Beam + Blade Dance. Core 2-min burst. |
| **The Hunt** | Major cooldown | Free | ~1.5s cast, **90s** `[T1]` | Charge that strikes for Chaos damage, roots for 1.5s, and leaves a 6s DoT on up to 5 enemies in your path; central burst button. For Aldrachi Reaver, guarantees a Reaver's Glaive proc. **12.1: damage +12%.** ⚠ **Eternal Hunt** does *not* reduce its cooldown — at 12.1 it makes The Hunt empower your next Eye Beam (+100% damage, wider area). *[Tier 1: spell 1270898 description @ 12.1.0.69214 — the old "reduced CD via Eternal Hunt" line here was wrong.]* |
| **Throw Glaive** | Rotational / ranged | Free (charges) | Instant, ~9s recharge | Ranged glaive throw; becomes a rotational button with **Soulscar** / **Furious Throws** / **Screaming Brutality**. Turns into **Reaver's Glaive** for Aldrachi Reaver. **12.1: benefits from Serrated Glaive's new self-buff (+15% for 12s).** |
| **Reaver's Glaive** | Rotational-spender enabler (AR) | Free | Instant | Aldrachi Reaver: replaces Throw Glaive after 6 soul fragments; applies **Reaver's Mark** and empowers the next Chaos Strike + Blade Dance. |
| **Abyssal Gaze** | Major cooldown (FS) | ~30 Fury | ~2s channel | Fel-Scarred **Demonic Intensity** empowered Eye Beam during Metamorphosis, and a **separate spell id** (452497) that overrides Eye Beam rather than modifying it. Demonic Intensity (452415) is **spec-conditional text**, not Devourer-only: it reads `$?a212612[][Void ]Metamorphosis greatly empowers $?a212612[Eye Beam, Immolation Aura][The Hunt]`, so the Havoc branch is *"Metamorphosis greatly empowers Eye Beam, Immolation Aura"* and the Devourer branch is the Void/The Hunt one. *[Tier 1: `Spell` @ 12.1.0.69214.]* ⚠ **The magnitude is not readable.** 452497's own description is byte-identical to Eye Beam (198013) — same damage line, same Furious Gaze clause — and states no increase, so "greatly" lives in damage values or an aura this file cannot reach. @verify-ingame (Abyssal Gaze damage vs Eye Beam) ⚠ **Whether Eternal Hunt's empower carries across the override is unstated** — 1270898 reads *"The Hunt empowers your next **Eye Beam**"*, and Abyssal Gaze is a different spell. The 12.1 APL holds The Hunt for the demon-form cast **only on Fel-Scarred**, which implies it does carry, but no text says so. @verify-ingame (Eternal Hunt buff on Abyssal Gaze) |
| **Consuming Fire** | Rotational-builder (FS) | Free | Instant | Fel-Scarred **Demonic Intensity** empowered Immolation Aura during Metamorphosis. |
| **Demonsurge** | Passive/proc (FS) | — | — | Fel-Scarred proc from Eye Beam/Meta; makes the next Annihilation + Death Sweep hit harder (tracked as "demonsurge available"). |
| **Glaive Tempest** | Passive | — | — | Talent: the final slash of Blade Dance/Death Sweep **consumes 25 Fury** at 3+ enemies to launch spinning glaives dealing Chaos damage over 3s (reduced beyond 8 targets). A passive, not a pressed button. |
| **Never Say Die** | Passive (NEW 12.1) | — | — | Damage **+3% while above 50% health**; leech **+5% while below 50% health**. Spec tree row 4, col 15. |
| **Fel Rush** | Movement | Free (2 charges) | Instant, ~10s recharge | Dash forward dealing damage; mobility + an **Inertia** / **Unbound Chaos** trigger / filler. |
| **Vengeful Retreat** | Movement | Free | Instant / ~25s (see the ⚠ note above — no longer Tier-1-backed at 12.1) | Backflip away, slows nearby enemies; procs **Initiative** / **Tactical Retreat**; woven before Eye Beam windows. |
| **Blur** | Defensive | Free | Instant, ~1 min CD (**+1 charge** w/ Demonic Resilience) | **Reduces all damage taken by 25% for 10s** *[Tier 1: spell 198589 description @ 12.1.0.69214]*; core personal defensive. **The old "+50% dodge / −20% damage taken" line here was stale and has been replaced.** |
| **Darkness** | Defensive (raid) | Free | Instant, **300s** `[T1]` | 8-yd zone for 8s granting friendly targets a **15% chance to avoid all damage from an attack** — **doubled to 30% when not in a raid** *[Tier 1: spell 196718 description]*. Group cooldown. |
| **Disrupt** | Interrupt | Free | Instant, **15s** `[T1]` | Interrupts a spellcast and locks that school for **5s**; the primary interrupt. **12.1: shows a "missed" visual + sound if the target was not casting** (game-wide interrupt change). |
| **Consume Magic** | Dispel (talent) | Free | Instant, **10s** `[T1]` | Consumes a beneficial magic effect from the target (offensive dispel). At 10s it is effectively always available — treat it as a free purge on any enrage/absorb buff, not a saved cooldown. |
| **Chaos Nova** | CC (AoE stun) | ~Free | Instant, **45s** `[T1]` | Eruption of fel energy stunning all nearby enemies for **3s** *[Tier 1: spell 179057 description]*. **12.1: its DR category now resets after 20s (was 16).** |
| **Sigil of Misery** | CC (AoE) | Free | Instant, ~90s CD | Places a delayed sigil that causes enemies in its area to cower/disorient. **12.1: DR reset now 20s.** ⚠ On **Vengeance** this row changed (Sigil of Silence now replaces it when selected); that is a Vengeance-only change and does not touch Havoc. |
| **Imprison** | CC | Free | Instant, **45s** `[T1]` | Incapacitates a target (Demon/Beast/Humanoid/Undead) for the duration. **12.1: DR reset now 20s.** |
| **Torment** | Utility (taunt) | Free | Instant, ~8s CD | Taunts the target to attack you; single-target threat/utility. |
| **Spectral Sight** | Utility | Free | Instant, **30s** `[T1]` | See hidden/stealthed enemies and through obstacles; reduced movement speed while active. |
| **Rain from Above** | CC / utility (PvP talent) | Free | Instant / **90s** `[T1]` | PvP talent: lift into the air, immune to melee, rain glaives; not a PvE button. |
| **Illidan's Grasp** | CC (PvP talent) | Free | Channel / **60s** `[T1]` | PvP talent: seize a target, then throw or slam them. |
| **Reverse Magic** | Dispel (PvP talent) | Free | Instant, **60s** `[T1]` | PvP talent: remove harmful magic from party/raid and send it back to enemies. |

> **PvP-only, deliberately not in the table above.** 12.1 ran a game-wide **PvP
> snare tier-down** ("70% reduced to 50%, 50% to 30%, and so on") and every class
> has movement-slow lines in that list. Those are **PvP-only** and must never be
> written into PvE rotation guidance. The same applies to the 12.0.7 hotfix that
> cut **Demon Muzzle** to 5% (was 15%) and **Glimpse** to 25% (was 35%) in PvP.

**Not on the Midnight Havoc tree:** **Sigil of Spite** (390163) is a **Vengeance** spec
talent and appears on no Havoc tree — class, spec or hero. *[Tier 1: `all-talents.tsv`
@ 12.1.0, all 40 specs — re-checked for 12.1.]*

**Removed in 12.1:** **Dash of Chaos** — see the talent-changes section above. Do not
re-add it from a guide written before 2026-08-11.

**Not acquirable at 12.1:** **Fel Barrage** — still absent. Twenty-one spells carry the
name in `SpellName`, and **none** of them attaches to a trait node, a
`SkillLineAbility` row, `SpecializationSpells` or `PvpTalent`; the live Demon Hunter tree
(854) has no Fel Barrage node and no Midnight-range ID was ever minted for it (highest is
400185, a War Within-era leftover). It is not an off-meta talent you could pick up — there
is no button. Do not re-add it from a guide that predates Midnight.
*[Tier 1: reconcile-ledger.md §4 @ 12.0.7.67808; zero rows in `all-talents.tsv` and in
this folder's `ability-inventory.tsv` @ 12.1.0.69214.]*

⚠ **Do not lift builds from this folder's `maxroll-raid.md` / `maxroll-mplus.md`.**
They are Tier-3 `verbatim: true` captures and, as of the 12.1 recapture, several still
recommend talents 12.1 deleted or moved. `talents.md` / `talents.json` (Tier 1, DB2 @
12.1.0) are the floor for whether a talent exists and where it sits.

## Spell-ID anchors — Tier 1 @ build 12.1.0.69214

Which spell id a display should bind when a name maps to several ids. Read from
wago DB2 at build **12.1.0.69214** — `SpellName`, `Spell` (description +
aura-description text), `SpellEffect`, `SpellMisc` → `SpellDuration`, and
`CooldownSetSpell` → `CooldownSet`.

### Inertia — three ids, three different things

The simc APL treats `buff.inertia` and `buff.inertia_trigger` as **two auras**
(`MID1_Demon_Hunter_Havoc.simc` uses `buff.inertia.up` and
`!buff.inertia_trigger.up` in one term), and `SpellName` @ 12.1.0.69214 carries
exactly three ids named "Inertia". They map one-to-one.

| ID | What it is | Evidence |
|---|---|---|
| `427640` | **The talent passive.** Two `SpellEffect` rows, both `Effect=6 EffectAura=4` (dummy) at `ImplicitTarget_0=1` (caster), `EffectBasePointsF` 20 and 24000 — no modifier, no duration (`SpellMisc.DurationIndex=0`). `Spell.Description_lang`: *"The Hunt and Vengeful Retreat cause your next Fel Rush or Felblade to empower you, increasing damage by $427641s1% for $427641d."* — i.e. it *names* `427641` as the thing you actually get. It is also the **Cooldown-Manager row**: `CooldownSetSpell` at `CooldownSetID=1599` (`CooldownSet.ChrSpecialization=577`, Havoc) carries `SpellID=427640` twice, `Category=2 OrderIndex=25` and `Category=3 OrderIndex=26`. |
| **`427641`** | ✅ **`buff.inertia` — the damage buff you have.** Three `Effect=6` rows on the caster: `EffectAura=108` (add percent modifier) ×2 and `EffectAura=344`, every one `EffectBasePointsF=12` — the +12%. `Spell.AuraDescription_lang` is *"Damage increased by $w1%."* `SpellMisc.DurationIndex=28` → `SpellDuration.Duration=5000` (**5s**). |
| **`1215159`** | ✅ **`buff.inertia_trigger` — the armed state.** One `Effect=6 EffectAura=4` (dummy) row on the caster, `EffectBasePointsF=300`, carrying no damage modifier at all. `Spell.AuraDescription_lang` is *"Your next Fel Rush or Felblade increases your damage by $427641s1% for $427641d."* — future tense, and it points at `427641` for both the magnitude and the duration. `SpellMisc.DurationIndex=29` → `SpellDuration.Duration=12000` (**12s**), the window The Hunt / Vengeful Retreat gives you to spend it. |

The split is unambiguous on two independent axes: only `427641` carries a damage
modifier aura, and the durations differ (5s held vs 12s armed), which is exactly
the shape `buff.inertia.up & !buff.inertia_trigger.up` needs.

⚠ **The empowerment spenders are Fel Rush and Felblade, per `427640`'s own
description at 12.1.0.69214 — not Immolation Aura.**

## Changelog

2026-08-22 — Abyssal Gaze row rewritten. The old text called Demonic Intensity's description Devourer-worded and unconfirmed for Havoc; it is spec-CONDITIONAL text with a Havoc branch that reads normally, so the row now carries the raw conditional. Two narrower unknowns replace the old blanket one: Abyssal Gaze's own description states no increase over Eye Beam, and Eternal Hunt's empower names "Eye Beam" while Abyssal Gaze is a separate spell id.

2026-08-26 — Spell-ID anchors section added (Tier 1, DB2 @ 12.1.0.69214) resolving Inertia's three ids: 427640 talent passive / CDM row, 427641 the 5s damage buff (`buff.inertia`), 1215159 the 12s armed state (`buff.inertia_trigger`). The Inertia talent-change bullet now carries 5s from `SpellDuration` rather than the patch note's 6s, per game-data-resolves-numbers.

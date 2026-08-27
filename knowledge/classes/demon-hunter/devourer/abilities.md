---
title: Demon Hunter Devourer — Abilities (Midnight, 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-27
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes — CLASSES ▶ DEMON HUNTER ▶ Devourer
  - knowledge/_meta/patch-notes/12.1.md  # tier 1, verbatim archive of the above (lines 434-450)
  - knowledge/classes/demon-hunter/devourer/ability-inventory.tsv  # tier 1, DB2 @ 12.1.0.69214 + Blizzard Game Data API spell descriptions — names, spellIDs, origin, cooldowns, tooltips
  - knowledge/classes/demon-hunter/devourer/talents.md  # tier 1, Trait* DB2 @ 12.1.0.68914 — tree membership, choice nodes
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied 2026-08-06 (§4, §5 G1/G2/G6)
  - https://www.method.gg/guides/devourer-demon-hunter/playstyle-and-rotation  # tier 3, upd. 2026-06-17, 2026-07-11 — pre-12.1, kept only for values Tier 1 has no column for
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11 — same caveat
  - https://github.com/simulationcraft/simc/tree/midnight/profiles/MID1  # tier 1, MID1_Demon_Hunter_Devourer.simc, 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/engine/class_modules/sc_demon_hunter.cpp  # tier 1, the spec implementation — read 2026-08-17 for the Void Metamorphosis override identities
confidence: medium
---

# Demon Hunter Devourer — Abilities (Midnight, 12.1)

Devourer is the **Midnight-new 4th Demon Hunter specialization** — a **mid-range
(~25 yd, Evoker-like) Void caster** that keeps the class's mobility toolkit but
"plants" for its key casts. It is a DPS spec, not a tank.

**Resource system — two interlocking resources plus a mastery:**
- **Fury** — the standard DH primary resource. **Consume** generates **8 Fury**
  `[T1]` (baseline; +2 more with *Celestial Echoes*), **Reap** generates 10 with
  *Scythe's Embrace* `[T1]`, and Fury is the fuel for **Void Ray**, the main
  spender, at **100 Fury** `[T1]` outside transform. *Untethered Fury*
  (Void-Scarred) raises maximum Fury by 20 `[T1]`.
- **Soul Fragments ("Souls")** — the secondary economy unique to how Devourer
  plays. **Reap / Eradicate gather up to 4 souls per cast** `[T1]`; souls power
  **Feast of Souls** (**+1% damage per fragment for 6s, stacking** `[T1]`) and
  accumulate to **50** to unlock **Void Metamorphosis** (**35** with *Soul
  Glutton*, which reduces the requirement by 15 `[T1]`). ⚠ Consume is **not** a
  baseline soul generator — *Predator's Thirst* is the talent that makes it one
  `[T1]`. (A pre-12.1 draft of this file asserted a baseline "+1 Soul and +4 Fury
  per Soul" from Consume; no 12.1 tooltip carries either figure, so both are gone.)
- **Mastery: Monster Within** — bonus damage **during Void Metamorphosis**. In
  12.1 this is the axis the whole spec was rebalanced on (below). *Enduring
  Torment* (Void-Scarred) makes it 20% more effective and leaks a weakened form
  of it outside demon form `[T1]`.

**Playstyle in one line (12.1 wording):** build Fury + Souls outside of transform,
bank to **50 Souls**, pop **Void Metamorphosis**, then dump Souls into
**Collapsing Star** and empowered casts before Fury drains and the form ends —
but **12.1 deliberately flattened how much of your damage lives inside that
window** (see below), so out-of-Meta uptime now carries materially more of the total.

**Hero trees:** **Annihilator** (a caster-leaning build that ramps *Voidfall*
stacks to call down Void Meteors) and **Void-Scarred** (Void Metamorphosis-centric;
a single-target-competitive caster variant and a melee-hybrid variant using The
Hunt / Hungering Slash). See `builds.md`. ⚠ The "Annihilator is the S1 default
everywhere, and barely does damage outside Meta" framing this file carried through
Season 1 is **exactly what the 12.1 rebalance targets** — do not restate it as
current; `builds.md` and fresh sims own the post-12.1 verdict.

## What 12.1 changed for Devourer

All values here are from the **Tier-1 12.1 Content Update Notes** and are the
floor — no Tier-3 guide may overwrite them.

**The rebalance, and its stated intent.** Blizzard's developer note: *"We're
reducing the scaling of Devourer's Mastery: Monster Within to help other stats to
compete and compensating with an overall ability damage buff. Between that and a
few more targeted changes, we expect damage during Void Metamorphosis to be
slightly reduced while damage outside of Metamorphosis is significantly
increased."*

| Change | 12.1 value | was |
|---|---|---|
| **Mastery: Monster Within** — bonus damage during Void Metamorphosis | **reduced by 66%** | — |
| **All ability damage** | **+32%** | — |
| Collapsing Star damage | **+12%** | — |
| Eradicate damage | **−6%** (secondary targets **−15%**) | — |
| **Consume** damage | **+60%** (does **not** affect Devour) | — |
| Void Metamorphosis' Void Ray damage bonus | **+40%** | +67% |
| *Impending Apocalypse* — per-Collapsing-Star damage to the next one | **+20%** | +30% |
| *Hungering Slash* follow-up | grants a **temporary charge of Vengeful Retreat** | free cast **+** a cooldown reset |
| **Annihilator** — *Otherworldly Focus* single-target bonus | **+30%** | +35% |
| **Annihilator** — *Final Hour* Voidfall-bonus persistence | **6s** | 8s |

⚠ **Consequence for guidance, not just numbers.** Mastery got worse *and* Meta
got a smaller Void Ray multiplier while flat ability damage and Consume — a
button you press *outside* transform — went up sharply. Any advice of the form
"pool everything for the Meta window" or "Mastery is the runaway stat" is
pre-12.1 and needs re-derivation from sims, not from this file. See `gearing.md`
for the stat side and `sims.md` for the APL.

**Demon Hunters can now equip daggers**, explicitly *"to allow Devourer Demon
Hunters to acquire and use daggers with Intelligence on them."* This widens the
weapon-slot loot pool for the spec — it is a **gearing** change and
`gearing.md` owns it.

**Global 12.1 changes that land on this spec** (they sit in the CLASSES preamble,
above the per-class lists, and apply to every spec):
- **Player health and creature damage both +25% at max level**, with health
  consumables rescaled and several DPS/Tank healing + absorb effects retuned.
  **Any absolute HP or heal-for-N number written before 2026-08-11 is wrong.**
  Devourer's percentage-based survivability (Soul Immolation's 24%-of-max-health
  heal, Blur's 25% reduction, *Soul Rending*'s leech) scales with the new pool.
- **Major DPS cooldowns lowered, steady-state damage raised** across several
  specs as a stated design direction — for Devourer, that direction *is* the
  Mastery/ability-damage swap above.
- **All class interrupts** now show a **"missed" visual** over the target's head
  and play a distinct sound when fired while the target was not casting. Applies
  to **Disrupt**.
- **Diminishing-return categories now reset after 20 seconds** (was 16) — this
  lengthens the effective DR window on **Void Nova**, **Imprison** and **Sigil of
  Misery** chains.

*(PvP only, recorded so nobody mistakes it for a PvE nerf: in PvP combat Consume
damage is reduced by 40% and Devour by 8%. Never fold this into PvE rotation
guidance.)*

> ⚠ Still a young spec with no Warcraft Logs history distilled here. What changed
> since Season 1 is **where the numbers come from**: the generated siblings in this
> directory (`ability-inventory.tsv` / `.md`, `talents.md`, `talents.json`) were
> regenerated on 2026-08-11 against **live 12.1 game data** (Blizzard Game Data
> API + wago `Trait*`/`Spell*` DB2 @ **12.1.0.69214**), so most effect text below
> is now Tier 1 rather than guide prose. A **`[T1]`** stamp marks a value read out
> of those files. A `~` value was **not** — it is a Tier-3 number the generated
> data could not settle, and it is kept on purpose.
>
> **One Devourer-specific caveat, unchanged at 12.1.** The transform-form buttons —
> **Cull**, **Devour**, **Pierce the Veil** — are runtime *overrides* of Reap /
> Consume / Voidblade. They exist in `SpellName` but attach to no acquisition
> table, so they still appear in **no** generated inventory (re-checked against the
> 12.1.0.69214 pull) and the tsv cannot confirm them. That is a hole in the
> generator, not evidence they are gone — their parents are all live, and 12.1's
> own notes name **Devour** in the Consume line. Same for the passive **Demonic
> Wards**, which the generator drops because it drops passive
> `SpecializationSpells` rows.
> *[Tier 1: reconcile-ledger.md §4 + §5 G1/G2; re-verified against the 12.1.0.69214 inventory.]*
>
> ⚠ **A FOURTH override exists and it is not one of these — Void Metamorphosis itself
> becomes Collapsing Star** for the duration of the form (in-game 2026-08-27;
> `rotation.md` → *The transform overrides*). It is listed separately because the caveat
> above does not apply to it: Collapsing Star `1221167` **is** in the generated inventory,
> as a `TraitNodeEntry` (`ability-inventory.md` item 7). What the generators cannot show is
> that it is an *override* rather than an additional button — an acquisition row says a
> spell exists, never which button casts it.
>
> ⚠ **The `maxroll-*.md` captures in this directory are Tier 3 and several carry a
> `kb_caveat`** — do not lift builds or stat orders from them without checking them
> against `talents.md`.

## Ability inventory

> **What the Tier-1 floor does and does not cover.** The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD. That is why **Reap**, **Blur**, **Shift**
> and **Vengeful Retreat** read 0.5–0.8s in the generated file and keep their `~`
> prose here; the recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable
> without breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6).
> **So "the generated file wins" applies to the values it actually carries** — and
> as of the 12.1 regen it carries the full **spell description text**, which is why
> most rows below now cite mechanics rather than guide paraphrase.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Consume** | Rotational-builder | **Generates 8 Fury** `[T1]` | ~2s cast (Tier 3; *Improved Consume* takes 0.25s off it `[T1]`), **castable while moving** `[T1]` | Primary filler outside transform. **12.1: damage +60%** — the single biggest reason out-of-Meta uptime matters more now. Souls only if *Predator's Thirst* is taken (+15% damage, generates a Soul Fragment) `[T1]`; *Improved Consume* adds +10% damage and −0.25s cast `[T1]`. Becomes **Devour** inside Void Metamorphosis — **the +60% explicitly does not apply to Devour**. |
| **Void Ray** | Rotational-spender | **100 Fury** `[T1]`; consumes 5 Fury per 0.1s while channelling. Free inside Meta `[T1]` | **Channelled, ends after ~2.7s or at 0 Fury** `[T1]`; you stand still | The main spender and a huge chunk of Devourer's damage. Outside Meta: no cooldown, costs Fury. Inside Meta: **no Fury cost, reduces Fury drain, and deals increased damage — 12.1 set that bonus to +40% (was +67%)**. It **does** have a cooldown inside Meta: Tier 1 confirms the cooldown exists via *Voidpurge* (**−2.0s during Void Metamorphosis** `[T1]`); the magnitude itself is still Tier 3 at **~16s (14s with Voidpurge)** — @verify-ingame. Fully channelling it upgrades Reap to **Eradicate** `[T1]`. |
| **Reap** | Rotational-builder | **Gathers up to 4 Souls** `[T1]`; +10 Fury with *Scythe's Embrace* `[T1]` | ~8s CD (charge ability — see the floor note); *Second Helping* adds a charge and *Umbral Blade* reduces the CD by your Haste `[T1]` | Instant ranged Cosmic bolt that collects up to 4 Soul Fragments. **The "resets on a full Void Ray channel" behaviour is a talent, not baseline** — *Moment of Craving*: after fully channelling Void Ray, Reap's cooldown resets and the next Reap collects up to 6 **additional** fragments `[T1]`. *Soulshaper* makes each fragment Reap gathers raise its damage by 8% `[T1]`. Becomes **Cull** inside Void Metamorphosis. **Class-baseline `[T1]`** — granted with the spec, in every build. |
| **Soul Immolation** | Rotational-builder / maintenance | **Heals 24% of max health, generates 30 Fury, shatters 3 Soul Fragments — all over 5s** `[T1]` | ~1 min CD (Tier 3; the generated file carries no usable value) | On-demand Soul/Fury/health pump. *Singed Spirit* adds +12 Fury over the duration; *Tempered Soul* cuts 30s off the cooldown and adds a charge; *Spontaneous Immolation* adds +6% health healed and resets it on a killing blow `[T1]`. ⚠ The 24% figure is **percentage-based**, so it tracks the 12.1 +25% health pool. |
| **Void Metamorphosis** | Major cooldown | **Requires 50 Soul Fragments** `[T1]` (35 w/ *Soul Glutton*); Fury drains while active | Fragment-gated (no fixed timer) | The defining transform and burst window. Consumes banked Souls to activate; **Consume and Reap are enhanced, Fury slowly drains, and Void Ray reduces that drain, costs no Fury and deals increased damage** `[T1]`. ⚠ **This button BECOMES Collapsing Star for the whole window** — an override, not an unlock: same keybind, changed art, drawn unusable below the 30-fragment grant, and no Void Metamorphosis button on the bar until the form ends (in-game 2026-08-27; `rotation.md` → *The transform overrides*). ⚠ *Soul Glutton*'s discount has a cost the pre-12.1 file omitted: **Fury drains 25% faster** `[T1]`. **12.1: the Void Ray bonus dropped to +40% (was 67%), and Mastery's in-Meta bonus fell by 66% — this window is deliberately less dominant than it was in Season 1.** |
| **Collapsing Star** | Rotational-spender (Meta only) | **Every 30 Soul Fragments harvested inside Meta grants a cast** `[T1]` — a gate, not a flat "costs 30" | Meta-only | The in-Meta payoff button: a single cataclysmic blast on the target plus splash to all nearby enemies, **reduced beyond 8 targets**, and **your Fury drain is significantly reduced while casting it** `[T1]`. **12.1: damage +12%.** *Impending Apocalypse* now makes each cast buff the next by **+20% (12.1; was 30%)**; *Star Fragments* makes it generate 3 Soul Fragments; *Voidrush* has it cut 10s off Voidblade `[T1]`. |
| **Midnight** | Spec capstone | — | — | Spell 1242486. **Resolved at 12.1 — Tier 1 tooltip: "Collapsing Star always critically strikes."** (The old @verify-ingame on this row is discharged.) Pairs hard with *Calamitous*, which raises critical-strike damage to 240% from the usual 200% `[T1]`. |
| **Cull** | Rotational-builder (Meta form of Reap) | Up to 4 Souls | Meta-only | Enhanced Reap while transformed. ⚠ **Not in any generated inventory** (see the override caveat above), so nothing below the name is Tier 1. The pre-12.1 claim that Cull is "buffed by *Student of Suffering*" was **wrong** and is removed — Tier 1 says *Student of Suffering* is applied by **Void Ray** (see Void-Scarred note below). |
| **Devour** | Rotational-builder (Meta form of Consume) | Fury | Meta-only, castable while moving | Consume's transformed version — the in-Meta filler. **12.1 explicitly excluded Devour from Consume's +60% buff**, which is part of how the patch shifted damage out of the transform window. |
| **Eradicate** | Rotational-spender / AoE (talent) | Gathers up to 4 Souls `[T1]` | Talent; **replaces Reap after a full Void Ray channel** `[T1]` | Slams the scythe for a **25 yd frontal cone**, full damage to the primary target and reduced damage to everything else in the cone, **reduced beyond 5 targets** `[T1]`. A large share of Devourer's multi-target damage. **12.1: damage −6%, and secondary-target damage −15%** — the AoE profile is narrower than it was in Season 1. |
| **Voidblade** | Rotational-builder / gap-closer | Generates Fury | ~30s CD (Tier 3) | Charge to your target for Cosmic damage — enables the melee-hybrid builds. **Class-tree talent** `[T1]` (not spec). Follows into **Hungering Slash** (talent) or **Pierce the Veil** (Void-Scarred, inside Meta). *Duty Eternal* doubles its damage and makes it generate 20 Fury; *Singular Strikes* adds +25%; *Devourer's Bite* makes Voidblade **and The Hunt** raise the target's damage taken from you by **12% for 10s, stacking** `[T1]` (the pre-12.1 file attached this to Voidblade alone). |
| **Hungering Slash** | Rotational-builder (talent) | **Generates 10 Fury; shatters up to 2 Soul Fragments** `[T1]` | **Replaces Voidblade for 6s after The Hunt or Voidblade deals damage** `[T1]` | Whirling melee slash, damage reduced beyond 8 targets; core of the Void-Scarred melee hybrid. **12.1 reworked its follow-up: it now grants a *temporary charge* of Vengeful Retreat (previously a free cast **plus** a cooldown reset) and makes your next Vengeful Retreat within 6s deal extra Cosmic damage** `[T1]`. *Flamebound* adds 2 yd radius and +50% crit damage; *Soulforged Blades* adds +15% crit chance `[T1]`. |
| **Pierce the Veil** | Rotational-spender (Void-Scarred, Meta) | — | Meta-only | Void-Scarred's empowered Voidblade. ⚠ **Not in any generated inventory** — but the mechanic behind it is Tier 1 via **Voidsurge**: *"Void Metamorphosis now also greatly empowers Voidblade and Hungering Slash. While demon form is active, the first cast of each empowered ability induces a Voidsurge,"* an area Void explosion, reduced beyond 8 targets `[T1]`. *Focused Hatred* gives Voidsurge +50% against a single target; *Demonic Intensity* stacks +10% per prior trigger in the window `[T1]`. |
| **Reaper's Toll** | Rotational-spender (Void-Scarred, Meta) | Generates Fury; shatters soul fragments | Meta-only | Void Metamorphosis' form of **Hungering Slash**, and the second Voidsurge cast. Spell `1245470` — *"Violently slash your scythe around you, dealing Cosmic damage to nearby enemies and generating Fury. Shatters up to N soul fragments from nearby enemies"* `[T1: Spell @ 12.1.0.69214]`; its damage and energize spells are Hungering Slash's (`1239127` / `1239507`), which is what identifies the parent. ⚠ Like Cull and Devour it attaches to no acquisition table and appears in **no** generated inventory. A companion aura `1245523` reads *"Pierce the Veil is replaced with Reaper's Toll"*. |
| **Predator's Wake** | Major cooldown (Void-Scarred, Meta) | — | Meta-only | Void Metamorphosis' form of **The Hunt**, and the third Voidsurge cast — which is exactly what *Demonic Intensity* means by *"Activating Void Metamorphosis greatly empowers The Hunt"*. Spell `1259431`, whose description is The Hunt's verbatim (charge, root, Cosmic damage over time to enemies in your path) `[T1: Spell @ 12.1.0.69214]`. ⚠ Not in any generated inventory. |
| **The Hunt** | Major cooldown / Movement | — | **90s `[T1]`** | Charge to the target, root them briefly, and inflict Cosmic damage over 6s to up to 5 enemies in your path `[T1]`. Opener + burst tool, heavier in Void-Scarred melee builds. **12.1: no Devourer-specific change** (the +12% in the notes is Havoc's line). *Violent Transformation* resets Voidblade and The Hunt on entering Meta, and makes The Hunt +25% and reset Soul Immolation `[T1]`. |
| **Void Nova** | CC (talent) | — | **45s `[T1]`** | Midnight-new class talent. Erupts for Cosmic damage and **stuns your target and all nearby enemies for 2 sec** `[T1]` — ⚠ the pre-12.1 "~3s per Tier-3 guides" figure is **wrong**; Tier 1 says 2s. Still the shortest hard CC in the kit and the one to spend freely on M+ trash. Range is not carried by Tier 1 — the old "30 yd" is unverified. |
| **Disrupt** | Interrupt | — | **15s `[T1]`**; locks the school for 5s `[T1]` | Baseline interrupt. ⚠ **It is not natively a 30 yd ranged kick** — Tier 1: *Improved Disrupt* "increases the range of Disrupt to 10 yds" and *Guile* adds "+20 yds" to Voidblade, Consume Magic **and Disrupt** `[T1]`, so 30 yd is the **both-talents** state, which is how a mid-range Devourer gets a usable interrupt at all. *Disrupting Fury* generates 30 Fury on a successful interrupt; *Demon Muzzle* cuts magic damage taken by 15% for 12s after one `[T1]`. **12.1 global: a missed interrupt now shows a "missed" visual + sound.** |
| **Consume Magic** | Dispel / Utility | — | **10s `[T1]`** | Offensive dispel — consumes 1 beneficial Magic effect from the target `[T1]`. *Swallowed Anger* generates 20 Fury on a successful removal `[T1]`. |
| **Imprison** | CC | — | **45s `[T1]`** | Incapacitates a demon, beast or humanoid for **1 min**; damage may cancel it; **limit 1** `[T1]`. |
| **Sigil of Misery** | CC | — | class talent | Places a sigil that disorients enemies in the area after a short delay. *Improved Sigil of Misery* is in the class tree `[T1]`. |
| **Torment** | Utility (taunt) | — | — | Single-target taunt: forces the target to attack you and raises your threat against it by **800% for 6s** `[T1]`. Off-tank/soak utility for a DPS. |
| **Spectral Sight** | Utility | — | **30s `[T1]`**, 8s duration `[T1]` | See enemies and treasure through barriers, plus stealthed/invisible enemies; loss-of-control effects break it `[T1]`. *Lost in Darkness* cuts 5s off the CD and removes the movement-speed penalty `[T1]`. |
| **Throw Glaive** | Utility / ranged | — | short CD/charges | Thrown glaive: minor Physical damage, **ricochets to an additional enemy within 10 yd** `[T1]`. *Bouncing Glaives* adds another ricochet; *Master of the Glaive* gives 2 charges + a 50%/6s snare; *Champion of the Glaive* gives 2 charges + 10 yd range `[T1]`. |
| **Vengeful Retreat** | Movement / Defensive | — | ~25s CD (charge ability — the generated file reads the GCD here) | Removes all snares and vaults you backward, damaging nearby enemies `[T1]`. What buffs it is **Hungering Slash**, which since 12.1 grants a temporary extra charge and empowers the next retreat within 6s `[T1]`. That empowerment is the **Voidstep** buff, spell `1223157` — *"Your next Vengeful Retreat will release a Cosmic explosion at your location"* `[T1: Spell @ 12.1.0.69214]`. ⚠ Voidstep is a **buff, not a talent**: there is no Voidstep node in the talent tree `[T1]`. It is the only reason the simc Void-Scarred priority presses Vengeful Retreat at all (`rotation.md`);  *Vengeful Bonds* snares nearby enemies by 70% for 3s `[T1]`. |
| **Shift** | Movement | — | ~20s recharge, to cursor | **Midnight-new Devourer movement** — *"Shift through the void, reappearing at your targeted destination"* `[T1]`; Devourer's replacement for Fel Rush. ⚠ **Charge question resolved at 12.1:** baseline 1, **+1 from *Blazing Path*** (class tree) and **+1 from *State of Matter*** (Annihilator) `[T1]` — so **up to 3**, which is where the Tier-3 guides' "3 charges" came from. *First In, Last Out* adds a decaying shield worth 6% of max health on each Shift `[T1]`. |
| **Blur** | Defensive | — | ~1 min CD (charge ability), **10s duration `[T1]`** | **Reduces all damage taken by 25% for 10 sec** `[T1]`. **Class-baseline `[T1]`, not a talent** — every Devourer has it. *Demonic Resilience* grants a second charge `[T1]`. (The cooldown column reads the GCD for this one, so ~1 min stays Tier 3 — reconcile-ledger §5 G6.) |
| **Darkness** | Defensive (raid/group) | — | **300s `[T1]`** | 8 yd zone granting allies a **15% chance to avoid all damage from an attack, for 8s** — **doubled to 30% when not in a raid** `[T1]`. *Long Night* adds 3s duration; *Pitch Black* cuts **120s** off the cooldown `[T1]`. |
| **Soul Rending** | Passive (defensive) | — | passive, 2 ranks `[T1]` | **+6% Leech per rank, plus another +6% per rank while Metamorphosis is active** `[T1]` (tooltip figures are rank 1). |
| **Demonic Wards** | Passive (defensive) | — | passive | Always-on magic damage reduction (Devourer's baseline mitigation). ⚠ Not in the generated inventory — the generator drops passive `SpecializationSpells` rows, so this row is not Tier 1. |
| **Feast of Souls** | Passive (offensive) | — | passive | **Each Soul Fragment grants +1% damage for 6s, and multiple applications overlap** `[T1]` — the concrete reason banking Souls matters. *Sweet Suffering* (2 ranks) extends its duration by 1s per rank `[T1]`. |
| **Voidfall** | Passive (Annihilator mechanic) | — | passive | **Consume has a 35% chance to grant a stack; at 3 stacks, Reap consumes one to call down a meteor** in an 8 yd area, reduced beyond 8 targets `[T1]`. *Meteoric Fall* makes Reap consume **all 3** for a rapid three-meteor sequence; *Meteoric Rise* also grants a stack on a full Void Ray channel; each stack additionally gives 2% Haste (*Swift Erasure*), 2% damage reduction (*Phase Shift*) or 3% movement speed (*Path to Oblivion*) `[T1]`. **12.1: *Final Hour* now persists those per-stack bonuses for 6s after the stacks are consumed (was 8s)** — ⚠ the 12.1.0.69214 tooltip still reads "8 sec"; the Tier-1 patch notes are the floor and say 6, so **6s is what this file asserts**, with the disagreement flagged. **12.1: *Otherworldly Focus* now gives Collapsing Star and Voidfall meteors +30% against a single target (was 35%), decaying 5% per additional target** `[T1]`. |

## Changelog

**2026-08-27 — Collapsing Star is an override of Void Metamorphosis, not an unlock.** Two claims
here were weaker than the measured fact: the override caveat named only Cull, Devour and Pierce
the Veil, and the Void Metamorphosis row said the transform *"unlocks"* Collapsing Star. In the
client the transform button **becomes** Collapsing Star for the duration of the window — same
keybind, changed art, unusable below the 30-fragment grant. Both rewritten; the full table is in
`rotation.md` → *The transform overrides*.

**2026-08-17 — three Meta-form buttons named, and the Voidstep claim rewritten.** Reading simc's
`sc_demon_hunter.cpp` (Tier 1) against `SpellName` / `Spell` @ `12.1.0.69214` resolved three actions the
priority list presses that this file had no row for: **Reaper's Toll** (`1245470`) is Void Metamorphosis'
form of Hungering Slash, **Pierce the Veil** (`1245483`) of Voidblade, and **Predator's Wake** (`1259431`)
of The Hunt — the three Voidsurge casts. All three sit in the same blind spot as Cull and Devour: real
spells, no acquisition row, invisible to the generators.

The **Vengeful Retreat** row said *"no talent named Voidstep exists in the 12.1 tree"* and left the reader
with "Voidstep is not a thing". Voidstep is a thing — it is the **buff** (`1223157`) Hungering Slash
grants, and it is what the Void-Scarred priority gates the retreat on. The claim is rewritten, not
annotated.

Also recorded in `rotation.md`, not here: `collapsing_star_stacking` caps at **40**, not 30 (30 is the
Collapsing Star grant threshold), and `void_metamorphosis_stack` caps at **50**, which is the soul
requirement expressed as a buff `[T1: SpellAuraOptions @ 12.1.0.69214]`.

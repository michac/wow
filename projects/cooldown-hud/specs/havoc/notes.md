# Havoc Demon Hunter — spec facts

> **⚠ DRAFT — desk-derived, not flown.** Every ID here is Tier-1 (wago DB2 @ 12.0.7,
> fetched 2026-08-03: `CooldownSetSpell` for set **1599**, `SpellCooldowns`,
> `SpellCategories` + `SpellCategory`, `SpellPower`, `SpellAuraOptions`, `SpellEffect`,
> `SkillLineAbility`) cross-checked against
> `knowledge/classes/demon-hunter/havoc/` (confidence **high**) and the Tier-1 simc
> midnight APL. What is **unconfirmed** is which of them the live Cooldown Manager
> tracks for a given build — `/cdmp hud layout` on a real Havoc character is the
> one-time check.

The rotation itself is `rotation.md`. This file is the roster, the mechanics, and the
blind spots.

---

## The tracked set — CooldownSet 1599, 57 rows

**10 Essential / 13 Utility / 31 TrackedBuff / 3 TrackedBar.** Retribution's set 901 is
9 / 15 / 31 for comparison — the same order of magnitude, so nothing structural is
different about the size.

### Essential (10)

| Ability | spellID | Fury | Real cooldown | Where it lives in DB2 | Line |
|---|---:|---:|---:|---|---|
| Chaos Strike | **162794** | 40 | none | — | L8, L13 |
| Blade Dance | 188499 | 35 | 15 s | `CategoryRecoveryTime` (cat 1640) | L7, L10 |
| Immolation Aura | 258920 | — | 30 s | **ChargeCategory 1676** (1 charge) | L4, L12 |
| Eye Beam | 198013 | 30 | 30 s | `CategoryRecoveryTime` (cat 1582) | L9 |
| Throw Glaive | 185123 | 25 | 9 s | **ChargeCategory 1612** (1 charge) | L15 |
| Fel Rush | **195072** | — | 10 s | **ChargeCategory 1545** (1 charge) | L14 |
| The Hunt | 370965 | — | 90 s | `CategoryRecoveryTime` (cat 2427) | L3 |
| Metamorphosis | 191427 | — | 120 s | `CategoryRecoveryTime` (cat 1577) | L2 |
| Essence Break | 258860 | — | 40 s | `RecoveryTime` (the only honest one) | L6 |
| **Rain from Above** | 206803 | — | 90 s | `RecoveryTime` | **none — dead icon** |

⚠ **Rain from Above never appears in the 140-line APL.** A tracked Essential ability
with a real cooldown that no priority line will ever cue. It is registered so the
decision log can name it and so the coverage probe does not report it blind; it is
simply never the answer. (This is the first ability the project has knowingly shipped
in that state — Retribution's dead weight was the other way round, an ability the APL
presses with no icon.)

### Utility (13) — and the three rotational presses hiding in it

Disrupt 183752 · Reverse Magic 205604 · Blur 198589 · Darkness 196718 · Chaos Nova
179057 · Sigil of Misery 207684 · Imprison 217832 · Consume Magic 278326 · Spectral
Sight 188501 · Torment 185245 — all genuinely utility, never scored.

**Three are not:**

| Ability | spellID | Why it is rotational |
|---|---:|---|
| **Felblade** | 232893 | The Fury generator on a 12 s cooldown. simc presses it on two lines. |
| **Vengeful Retreat** | 198793 | Procs Initiative / triggers Inertia; simc presses it before every Eye Beam. |
| **Fel Rush** | 195072 | Appears as **BOTH** an Essential and a Utility row — two CDM rows, one ability. |

⚠ **This is a smaller problem than the rollout plan implied, and the correction is
worth stating.** The plan said two rotational presses are "filed Utility, which
Retribution's model never scores". The pipeline's two relevant fences —
`Coach.lua:501`'s SOON fence and `State.lua:1941`'s virtual-row fence — both test the
**spec-authored** `info.cadence`, **not** the CDM's category. Declaring these
`cadence = "filler"` / `"oncd"` in the signal bucket makes them cueable with **no
pipeline edit at all**. The CDM category only affects which viewer frame they draw on
and how a claim is ranked when two roster entries contest one row.

Fel Rush's double row is handled by the roster claim ranker
(`St.RosterClaims`), which assigns each row to at most one ability and prefers
Essential over Utility — so 195072 claims its Essential row and the Utility row goes
unclaimed. **Verify in the flight** (`/cdmp hud coverage` should show 195072 `ok`, not
a contested or duplicated entry).

### TrackedBuff (31) + TrackedBar (3)

Registered as `kind = "aura"` — inputs to the decision, never scored, never cued.

**The ones a line actually reads:** Metamorphosis 191427 (the fork), Inner Demon 389693
(L2's veto), Initiative 388108 (L5's veto).

**The ones registered so the log can name them:** Art of the Glaive 442290 · Inertia
427640 · Ragefire 388107 · Thrill of the Fight 442686 · Demonsurge 452402 · Student of
Suffering 452412 · Monster Rising 452414 · Fury of the Aldrachi 442718 · Reaver's Mark
442679 · Evasive Action 444926 · Cycle of Hatred 258887 · Burning Wound 391189 ·
Soulscar 388106 · Serrated Glaive 390154 · Chaos Theory 389687 · Army Unto Oneself
442714 · Incorruptible Spirit 442736 · Eternal Hunt 1270898 / 1270901 · Mortal Dance
328725 · Furious Gaze 343311 · Unbound Chaos 347461 · Exergy 206476.

---

## The five overrides — every one rides its base frame

**Resolved by property (`SpellEffect.EffectAura == 332`, override-actionbar-spell),
never by name.** This is the discipline the Retribution run paid for: eight spells are
called "Hammer of Light"; Demon Hunter has the same problem (76 spells named
"Annihilation", 19 named "Chaos Strike").

| Granting aura | replaces | with | corroborating property |
|---|---|---|---|
| **Metamorphosis 162264** | Chaos Strike 162794 | **Annihilation 201427** | same Fury cost, 40 |
| **Metamorphosis 162264** | Blade Dance 188499 | **Death Sweep 210152** | same **category 1640**, same Fury 35 |
| Demonsurge 452489 | Eye Beam 198013 | **Abyssal Gaze 452497** | same **category 1582**, same Fury 30 |
| Demonsurge 452489 | Immolation Aura 258920 | **Consuming Fire 452487** | same **ChargeCategory 1676** |
| Reaver's Glaive 444686 | Throw Glaive 185123 | **Reaver's Glaive 442294** | `misc0 = 185123`, explicit |

**This uniformity is Havoc's structural gift.** Retribution's overrides needed a
`spender` discriminator because two different frames could carry the same Hammer of
Light. Here every override is a 1:1 replacement of one named base, so `ctx.facts[base]`
is always the record and `rec.live` is always the label. Nothing in `CoachHavoc.lua`
has to ask *which frame*.

Every override entry carries **`expect = false`**. That field is load-bearing:
`State.lua`'s virtual-row walk auto-promotes an untracked `kind = "button"` ability with
no base cooldown into a self-drawn icon, so an override that passed those fences would
draw a **duplicate** beside the real one.

⚠ **Consuming Fire is a homonym pair and both are registered.** 452487 and 456640 are
both named "Consuming Fire", both share ChargeCategory 1676, and both are granted by
452489 — 452487 by spell-class mask (which covers Immolation Aura 258920) and 456640
against 427917 (a different Immolation Aura variant). No property separates them
offline. Both get an entry with a **distinct `abbr`** (`CFire` / `CFire2`), which is
what lets one capture answer which the client actually surfaces. Retribution's two
Hammer-of-Light entries exist for exactly this reason.

## The action-bar / CDM ID split

SkillLine 1848 (Havoc) teaches **wrapper** spells; the Cooldown Manager tracks the real
ones. Evidence, not inference:

| Wrapper (on your action bar) | CDM tracks | how we know |
|---|---|---|
| Chaos Strike **344862** | **162794** | 344862 is a bare dummy effect with `SkillLine 1848`; 162794 carries the Fury cost and triggers 222031 / 199547 |
| Fel Rush **344865** | **195072** | 344865's *only* effect is `Effect 64, trigger → 195072` |

`HudBinds.B.Resolve` asks the action bar about the tracked ID and finds nothing, so both
would silently lose their keybind hint. `spec.SpecBindAlias = { [162794] = 344862,
[195072] = 344865 }` closes it — the Imp Lord case (cast id ≠ action-bar id), which is
the one documented reason that table exists.

⚠ Demon's Bite 344859 is taught on the same skill line and is **deliberately not
registered**: it appears nowhere in the APL (Midnight Havoc generates Fury from
auto-attacks, Immolation Aura and Felblade), and registering an ability no line presses
would put a phantom entry in the coverage report.

---

## The buff channel — tracked IDs, not aura IDs

`state.buffs` is keyed by the **CDM row's base spellID** (`State.lua:2304`,
`buffs[baseOf(entry)] = true`). For Havoc that is almost always the **talent** ID, and
the real aura the talent grants is a different number carrying the stack count:

| Tracked (what the brain keys on) | `CumulativeAura` | Real aura | `CumulativeAura` |
|---|---:|---|---:|
| Art of the Glaive 442290 | 0 | 444661 | **80** |
| Demonsurge 452402 | 0 | 452416 | **4** |
| Inertia 427640 | 0 | 427641 (5 s) | *(no row)* |
| Initiative 388108 | 0 | 391215 (5 s, `aura 290` = crit) | *(no row)* |
| Unbound Chaos 347461 | *(no row)* | 347462 (12 s) | 1 |
| Metamorphosis 191427 | *(no row)* | **162264** | 0 |
| Essence Break 258860 | *(no row)* | 320338 (**4000 ms**) | 0 |

⚠ **The trap the rollout plan warns about is real and it does not matter here.** The
HUD's presence channel is `item:IsActive()` — a **bool** on the tracked row. A stack
count was never reachable through it whichever ID we keyed on, so resolving the real
aura buys documentation, not capability. The brain keys on the **tracked** ID; the real
IDs are recorded above and in `SpecHavoc.lua`'s comments so a future stack-capable
channel knows where to look.

**Two aura IDs are load-bearing anyway:**

- **Metamorphosis 162264** is the aura that carries both meta overrides
  (`EffectAura 332 → 201427`, `→ 210152`). It is *not* the tracked row (191427 is), but
  it is what proves the override pair by property.
- **Essence Break 320338**'s **4000 ms** duration is the window length `ctx.ebWindow`
  counts back over the cast history. Without that number the window would be a tuned
  guess.

## What is NOT readable — the wall

| simc reads | channel | verdict |
|---|---|---|
| `buff.rending_strike` 442442 | — | **NO CDM ROW.** Not in set 1599 at all. |
| `buff.glaive_flurry` 442435 | — | **NO CDM ROW.** |
| `buff.reavers_glaive` 442294 | — | **NO CDM ROW** (only the transform is visible). |
| `debuff.essence_break` 320338 | — | No CDM row; recovered from **cast history + a 4 s duration**. |
| `variable.rg_inc` / `rg_ds` | — | Sequence state; simc-internal. |
| `buff.inertia_trigger` | — | A third aura with no tracked row (427640 is the talent, 427641 the consumed buff). |
| `.stack` on anything | `IsActive()` | Presence only, everywhere. |
| `talent.*` | — | Not on the pulse. An **untracked** ability is the only talent signal. |
| `cooldown.X.remains` | `C_Spell.GetSpellCooldown` | **Secret in combat** (settled game-wide). Our own napkin is not. |
| `active_enemies`, `raid_event.*`, `fight_remains`, `target.time_to_die`, `buff.out_of_range` | — | Sim-only. `active_enemies` → the mode toggle. |
| `soul_fragments.total` | — | Havoc has no fragment channel (see below). |
| `prev_gcd.1.death_sweep` | cast history | **Readable** — `UNIT_SPELLCAST_SUCCEEDED` spellIDs survive combat. Unused today; available if a line ever needs it. |

## What Aldrachi Reaver costs us

Six of the APL's 140 lines (:56–61) implement the Reaver's Glaive spend sequence, and
**all six read buffs with no CDM row**. This is not a modelling difficulty the HUD could
solve with better vocabulary — the signal does not exist on any channel the addon can
reach under Secret Values.

So on Aldrachi Reaver the HUD says *"a Reaver's Glaive is up, press it"* (L1, off the
transform) and then goes quiet about what to spend the resulting Rending Strike and
Glaive Flurry on. The rest of the list — Metamorphosis, The Hunt, Eye Beam, Blade
Dance, the Fury dump — is unaffected and correct.

**Under-serving a hero tree's payoff, never mis-serving it.** The alternative — a
`spec.HAVOC_RG_SEQUENCE = false` switch guarding a phase machine — would be machinery
behind a switch that no flight can ever flip on, because flipping it needs a read that
does not exist. `rotation.md` Deviation 1 records the decision.

## Havoc declares no derived resource

`spec.derived` (Phase 0.3) exists for a class resource `Enum.PowerType` structurally
cannot carry: Demon Hunter **Soul Fragments**. It ships fully wired and tested
(`derived_resource_spec.lua`) with zero consumers, and **Havoc is not the first one.**

Three Tier-1 checks:

1. `demonhunter_havoc.simc` references `soul_fragments` **once**, as one of three ORed
   alternatives gating a single `annihilation` line (:134).
   `demonhunter_vengeance.simc` references it **32 times**. Havoc's resource is Fury;
   Vengeance's is fragments.
2. Neither shipped reader is Havoc's. The `castCount` path reads **Soul Cleave 228477**,
   a Vengeance spell Havoc does not have. The `auraStacks` path reads **Dark Heart
   1225789**, and Blizzard's own `DemonHunterSoulFragmentsBar.lua:18` sets
   `self.requiredSpec = SPEC_DEMONHUNTER_DEVOURER` — the fragment bar is **Devourer-only**.
3. What Aldrachi Reaver Havoc actually interacts with are ordinary buffs — Rending
   Strike, Glaive Flurry, Reaver's Mark, Thrill of the Fight — which ride the existing
   presence channel, not a counter.

Vengeance (`castCount`) and Devourer (`auraStacks`) remain the channel's first
consumers.

## Hero trees

| Tree | `TraitSubTree` | `state.hero` | role |
|---|---:|---|---|
| **Fel-Scarred** | **34** | `"fel-scarred"` | simc's default profile; the v1 profile here |
| Aldrachi Reaver | 35 | `"aldrachi-reaver"` | funnel / cleave |

Both are already in `State.lua`'s `HERO_BY_SUBTREE` (Phase 0.4). The brain reads
`state.hero` off the pulse and **never infers it from the tracked set** — that inference
is field-fix B, and it confidently returned the wrong tree on Destruction's first live
session.

⚠ **`ctx.hero` has no reader in `RankWinner` today, and that is honest rather than
useless.** No line branches on the tree: L1 fires because the Throw Glaive frame is
*visibly* transformed, which is an Aldrachi Reaver fact that announces itself, and every
Fel-Scarred addition is a display override on a frame the list already presses. It is
published because it is the honest name for the build, the decision log wants it, and
the first line that genuinely needs a tree branch must read this instead of re-inferring.

## The burst window

Havoc's burst is **Metamorphosis + Eye Beam**, and unlike Demonology's Tyrant **nothing
is staged for it**. There is no pooling, no partner summon, no window to hold a resource
across. Chaotic Transformation resets Eye Beam and Blade Dance when Meta is cast, which
is why simc's :103 wants Meta to land while Eye Beam is on cooldown — an alignment gate
built entirely from secret cooldown reads, and therefore dropped
(`rotation.md` Deviation 12).

Structurally this makes Havoc **Destruction's Summon Infernal**, not Demonology's
Tyrant: a plain on-cooldown press, no `stage` bit, no go-gate, and no window
suppression in `Escalate`.

Potion / trinket / racial alignment lives in `actions.cooldown` (:104–113) and is a
**cooldown-sync rule, not a priority-list rule**. The list has no way to say it and does
not try.

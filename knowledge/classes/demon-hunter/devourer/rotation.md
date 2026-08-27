---
title: Demon Hunter Devourer — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-17
reviewed: 2026-08-27
augments: simc-apl.md @5f916c6
sources:
  - knowledge/classes/demon-hunter/devourer/simc-apl.md  # tier 1, the generated 12.1 priority list this file explains (apl_demon_hunter.cpp @5f916c6, 2026-08-14)
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/engine/class_modules/sc_demon_hunter.cpp  # tier 1, the spec implementation the APL is written against — read 2026-08-17 for buff/override identities and the Fury-drain model
  - https://wago.tools/db2  # tier 1, SpellName / Spell / SpellAuraOptions / SpellClassOptions / SpellActivationOverlay / CooldownSetSpell @ 12.1.0.69214
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — CLASSES ▶ DEMON HUNTER ▶ Devourer; archived at knowledge/_meta/patch-notes/12.1.md
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, read 2026-07-11 @ 12.0.7 — pre-rebalance, corroboration only
  - https://www.method.gg/guides/devourer-demon-hunter/playstyle-and-rotation  # tier 3, upd. 2026-06-17 @ 12.0.7 — pre-rebalance, corroboration only
confidence: medium
---

# Demon Hunter Devourer — Rotation (Midnight 12.1)

**The priority list is `simc-apl.md` in this folder. This file is why each rung sits
where it does, and what the sim does not model.** It does not restate the list; open
that file for the order and the exact conditions.

Devourer is a **mid-range (~25 yd) Void caster** with two interlocking economies. **Fury**
is the primary resource and fuels **Void Ray**, the main spender, at 100 Fury. **Soul
Fragments** are the secondary economy: Reap harvests them, and every fragment you consume
**outside** demon form adds a stack to the `void_metamorphosis_stack` buff. That buff caps
at **50** `[T1: SpellAuraOptions.CumulativeAura on 1225789]` and **Void Metamorphosis is
not castable until it is full** — the transform is fragment-gated, not on a timer. *Soul
Glutton* lowers the requirement to 35 and drains Fury 25 % faster.

Inside Void Metamorphosis the same consumed fragments feed a **different** counter,
`collapsing_star_stacking` — every **30** grants a **Collapsing Star** cast, and the
counter itself caps at **40** `[T1: SpellAuraOptions.CumulativeAura on 1227702]`. So
in-window play is: harvest, spend Collapsing Star before the counter reaches 40, and keep
Fury above the drain until the form ends.

The whole spec is that loop. **12.1 deliberately flattened how much of your damage lives
inside the window** — Mastery's in-Meta bonus fell 66 %, all ability damage rose 32 %, and
**Consume** (an out-of-Meta button) gained 60 % on top. Any pre-12.1 advice of the form
"pool everything for the window" is wrong now. `abilities.md` carries the full 12.1 change
table; `builds.md` carries the hero-tree argument.

## Four branches, and which one you are reading

`actions.default` is not the body. It dispatches to one of **four** priority lists on hero
tree × `talent.the_hunt`:

| List | Selected by | Lines | Shape |
| --- | --- | ---: | --- |
| `annihilator_ranged` | Annihilator, no The Hunt | 19 | flat priority |
| `annihilator_melee` | Annihilator + The Hunt | 27 | flat priority + melee weave |
| `voidscarred_ranged` | Void-Scarred, no The Hunt | 15 | flat priority |
| `voidscarred_melee` | Void-Scarred + The Hunt | 3 → `vsm_st` (20) / `vsm_meta` (18) / `vsm_out` (16) | a **three-state machine**: 54 lines, 47 presses |

**`talent.the_hunt` is the melee/ranged switch**, and it is a real playstyle fork, not a
talent swap: taking The Hunt pulls in Hungering Slash, Voidblade weaving and Vengeful
Retreat chains, and the Void-Scarred version of it stops being a priority list at all —
`voidscarred_melee` branches on single-target / in-Meta / out-of-Meta and runs a different
list in each. It also presses two buttons no other branch has (**Reaper's Toll**,
**Predator's Wake**), drops **Collapsing Star** entirely, and promotes **Soul Immolation**
from last to first.

⚠ **Do not read a rung number across branches.** Rung numbers below count lines **within
their own list**, because this spec has no shared body.

## The transform overrides — six pairs, and the transform button is one of them

Void Metamorphosis re-skins buttons the way demon form does for Havoc, and the same
override-identity care applies. `sc_demon_hunter.cpp` (Tier 1, read 2026-08-17) names the first
five by inheritance; the sixth is not a simc fact and was measured in the client:

| Outside Meta | Inside Meta | Evidence |
| --- | --- | --- |
| **Reap** `1226019` | **Cull** `1245453` | long-known; both in `SpellName` |
| **Consume** `473662` | **Devour** `1217610` | both in `SpellName` |
| **Voidblade** `1245412` | **Pierce the Veil** `1245483` | `pierce_the_veil_t : voidsurge_trigger_t<PIERCE_THE_VEIL, voidblade_base_t>` |
| **Hungering Slash** `1239123` ⚠ *[T3]* | **Reaper's Toll** `1245470` `[T1]` | `reapers_toll_t : voidsurge_trigger_t<REAPERS_TOLL, hungering_slash_base_t>` |
| **The Hunt** `1246167` | **Predator's Wake** `1259431` | `predators_wake_t : voidsurge_trigger_t<PREDATORS_WAKE, the_hunt_base_t>` |
| **Void Metamorphosis** `1217605` | **Collapsing Star** `1221167` | in-game 2026-08-27 — the button itself is overridden for the whole window |

⚠ **The transform button becomes the payoff button, and that is stronger than "unlocks".**
Collapsing Star is not a new button that appears somewhere: **Void Metamorphosis's own button
becomes it for the duration of the form** — the same keybind casts it, the art changes, and below
the 30-fragment grant it simply draws unusable rather than disappearing. Measured in the client
2026-08-27. It behaves like every other row above, which is why it is in this table; what makes it
worth its own note is that the other five re-skin a *rotational* button while this one re-skins the
**cooldown you pressed to get here**, so for the whole window there is no Void Metamorphosis button
on the bar at all. Neither `1221167` nor `1221150` has a `CooldownSetSpell` row of its own
(`CooldownSetID 1864` @ `12.1.0.69214` `[T1]`) — which is exactly what an override does not need,
since it borrows the row of the spell it replaces.

⚠ **Hungering Slash is a FAMILY of ids, and only one of them is Tier 1 here.** `1239519` is the
**talent entry** — the node you take — and it is what `all-talents.tsv` and
`spell-descriptions.tsv` carry at `12.1.0.69214` `[T1]`. `1239123` is the **cast / override**
id, the one the Voidblade button becomes, and it is the id in the table above; the two damage /
energize members (`1239127`, `1239507`) appear nowhere in this KB. They are not in conflict —
one talent, four spells, which is the ordinary shape.

**But `1239123` has no Tier-1 backing in this workspace.** It reaches us only through Wowhead
links inside `maxroll-raid.md` / `maxroll-mplus.md`, both Tier 3 and both `verbatim: true`, so
it is marked `[T3]` above rather than left bare beside its Tier-1 neighbours. `projects/combat-assist/specs/devourer/catalog.md`
builds an override chain on it, which is the reason this matters.

- Confirm Hungering Slash's cast id: cast it and read the override, or pull `SpellName` / the override tables at `12.1.0.69214` for 1239123, 1239127 and 1239507. @verify-ingame

⚠ **Reaper's Toll, Pierce the Veil and Predator's Wake are new to this file** and were
previously unexplained APL actions. They are Void-Scarred's **Voidsurge** casts: entering
Void Metamorphosis empowers Voidblade, Hungering Slash and The Hunt, and the *first* cast
of each in the window induces a Voidsurge explosion. Like Cull and Devour they attach to no
acquisition table, so they appear in **no** generated inventory — but all three are in
`SpellName` at `12.1.0.69214` with descriptions that match their parents' text, which is
what settles them.

⚠ **"Voidsurge" is what 12.1 calls it; "Demonsurge" is the stale name.** The Void-Scarred
hero tree is the **same node set and the same spell IDs as Havoc's Fel-Scarred tree**
(452402–452415, choice pairs and all). `talents.md` @ `12.1.0.68914` still emits the Havoc
name **Demonsurge** for 452402; the ability data @ `12.1.0.69214` carries `Voidsurge` with
`Demonsurge` recorded as a former name. **Use Voidsurge.**

## Void-Scarred, ranged (`actions.voidscarred_ranged`) — why each rung is there

The 15-line list, in order. This is the branch a Void-Scarred player without The Hunt runs.

1. **Voidblade at a full soul bank, with *Devourer's Bite*** — Voidblade applies a stacking
   +12 %-damage-taken debuff for 10 s. Spending the last global before you transform puts
   that amp *on* the window instead of wasting it outside one. Without the talent the line
   is inert.
2. **Void Metamorphosis** — the engine. Gated on `buff.eradicate.up` (or no *Eradicate*
   talent, or single target), i.e. don't transform mid-way through setting up the AoE
   upgrade. Note the button is uncastable below a full soul bank regardless: simc's
   `action_ready()` returns false unless `void_metamorphosis_stack` is at max stacks.
3–4. **Devour / Consume on Soulburst** — `buff.soulburst` is the **Season 2 2-piece**
   (`1297433`): harvesting 4+ fragments with Reap has a 20 % chance to make your next
   Consume instant and explode. It promotes the spec's *last* rung to near the top, so it
   is the single largest rank swing in the list. Rung 3 is the single-target Devour case;
   rung 4 catches everything else. **Both rungs vanish without the tier.**
5. **Collapsing Star at 35+ counter, single target** — the counter caps at 40, so 35 is
   "five from wasting harvested souls". At 2+ targets this is unconditional and drops to
   rung 9 instead.
6–7. **Reap / Cull / Eradicate at 4+ available fragments** (and a `fight_remains<=6` dump).
   `actions.reaps` is `eradicate` → `cull` → `reap`: one list, whichever form is live.
8. **Void Ray** — the main spender, and the line that *creates* the Eradicate upgrade
   (a full channel turns Reap into Eradicate). Its condition is `!buff.eradicate.up |
   !buff.moment_of_craving.up | set_bonus.midnight_season_2_4pc`: with the S2 4-piece it is
   unconditional; without it, you hold the channel only while **both** upgrades are already
   banked.
9. **Collapsing Star, 2+ targets** — unconditional in AoE.
10. **Vengeful Retreat on Voidstep** — `buff.voidstep` (`1223157`) is *"Your next Vengeful
    Retreat will release a Cosmic explosion at your location"*, granted by **Hungering
    Slash**. This is a damage press, not a mobility one, and it is the only Vengeful Retreat
    rung in the branch: **no Voidstep, no press.**
11–12. **Reaper's Toll / Pierce the Veil while their Voidsurge is owed** — the once-per-window
    empowered casts. See the caveat below: the sim tracks the owed cast with an internal
    placeholder buff, so these two rungs have no game aura behind them.
13. **Soul Immolation when its effect is absent, and — in Meta — only while Fury is below
    one second of drain.** Out of Meta this is ordinary maintenance. **Inside Meta it is an
    emergency top-up that keeps the form alive**, which is a shape no other DH spec has: a
    press that *sustains a form* rather than spending into it. Soul Immolation returns 30
    Fury (+12 with *Singed Spirit*) over 5 s.
14–15. **Devour / Consume** — the unconditional floor. Whatever is left, you press this.

### The Fury drain is a fitted model, not a game number

`void_metamorphosis_base_drain_ps` in the APL is simc's own curve,
`15.0 + 1.40 · e^(0.0775 · stacks)` where `stacks` counts drain ticks so far
(`sc_demon_hunter.cpp`, `fury_state_t`; the comment says it was fit against per-tick drain
schedules from logs, PR #11549). That is **≈16.4 Fury/s at the start of a window and
accelerating** — ~22/s twenty ticks in. *Soul Glutton* divides the whole curve up by 25 %.
So rung 13's `fury < void_metamorphosis_base_drain_ps` means roughly *"under ~16–25 Fury,
one tick from dropping out"*. It is a model, not a tooltip. `@verify-ingame`

### Two upstream oddities, flagged and left alone

- ⚠ **`annihilator_ranged` negates the set-bonus term** where the other three branches do
  not: `void_ray,if=…|!set_bonus.midnight_season_2_4pc` vs `…|set_bonus.midnight_season_2_4pc`.
  Possibly an upstream typo. It is Tier 1, so it is reported and not "fixed".
- ⚠ **`buff.voidsurge_reapers_toll` and `buff.voidsurge_pierce_the_veil` are not game auras.**
  Both are simc's `demonsurge_placeholder_buff`, created `set_quiet(true)` and triggered for
  every Voidsurge ability on entering the form — the sim's bookkeeping for "this window's
  empowered cast is still owed". There is a real overlay aura in the neighbourhood
  (`1245523`, *"Pierce the Veil is replaced with Reaper's Toll"*), but it describes the
  *replacement*, not the owed cast. Do not read these two rungs as tracking something the
  client shows. `@verify-ingame`

## Season 2 tier is load-bearing on this branch

Three of the fifteen rungs move on the Midnight Season 2 set, which did not exist when the
Season 1 guidance was written:

- **2-piece → `buff.soulburst`** (`1297433`, damage `1297432`): rungs 3 and 4 exist only
  with it.
- **4-piece → `set_bonus.midnight_season_2_4pc`**: it makes Void Ray unconditional at rung 8
  and grants *Moment of Craving* independently of the talent
  (`spec.moment_of_craving_buff` is looked up on `talent || MID2 B4`).

Season 2 opens **2026-08-18**. Read every rung above as the *geared* list.

## What the sim does not model

- **Range and planting.** Void Ray is a ~2.7 s channel you stand still for, and the sim's
  dummy never has to move. The real cost of a dropped channel is a lost Eradicate upgrade
  *and* a lost Moment of Craving reset, which is much worse than the lost damage.
- **Picking fragments up.** `pick_up_fragment` is a real action in **two** of the four
  branches — `annihilator_ranged` (twice) and `voidscarred_melee` (in all three of its
  sub-lists). `annihilator_melee` and `voidscarred_ranged` have none at all. It is
  *walking over a soul*, with a
  `line_cd` and a `mode=nearest`. It is not a button and it has no spell; it is the sim's
  model of positioning, and in play it is the largest thing on this list that no icon can
  tell you about.
- **`fight_remains`.** Rung 7 and the trinket lines are perfect-information dumps with no
  human equivalent. Read them as "burn it if the pull is nearly over".
- **`wait,sec=0.05`.** **All three** of `voidscarred_melee`'s sub-lists contain an
  explicit *do nothing* —
  hold the global rather than spend a fragment that would overflow the bank. The correct
  answer at those moments is genuinely "press nothing".

## Talent gates that change the priority

- **The Hunt** — the melee/ranged branch switch (above). The single biggest fork.
- **Devourer's Bite** — without it, `voidscarred_ranged` rung 1 (the pre-transform
  Voidblade) does not exist.
- **Eradicate** — without it, Void Metamorphosis's rung-2 condition is vacuous and it is
  pressed the moment the bank fills.
- **Soul Glutton / Emptiness** — 35-soul windows that are shorter and faster, versus 50-soul
  windows that ramp Haste. Icy Veins' 12.1 Void-Scarred lists take Soul Glutton to cycle
  Voidsurge as often as possible.
- **Moment of Craving** — the Void-Ray-resets-Reap loop. Also granted by the S2 4-piece.
- **Second Helping** — a flat extra Reap charge, unconditional.
- **Hero tree** — the four-way branch above. `builds.md` owns the contested Annihilator vs
  Void-Scarred call; it is **not settled** as of 2026-08-17.

⚠ **Which Void-Scarred branch the guides recommend is unresolved.** Icy Veins publishes two
Void-Scarred loadouts (`builds.md`) but the strings have not been decoded, so whether they
take The Hunt — and therefore whether the recommended build runs `voidscarred_ranged` or the
three-state `voidscarred_melee` — is unknown. `@verify-ingame`

## Open questions

- `@verify-ingame` **Void Ray's in-Meta cooldown.** *Voidpurge* reduces it by 2.0 s
  `[T1]`, so a cooldown exists; the magnitude is still Tier-3 (~16 s, 14 s with Voidpurge)
  and the 12.1 DB2 lists none on the spell.
- `@verify-ingame` **Final Hour's Voidfall persistence.** The 12.1 patch notes say **6 s**;
  the `12.1.0.69214` tooltip still reads 8 s. The notes are the floor. Time it after a
  3-stack Reap.
- `@verify-ingame` **The Fury drain rate.** simc's fitted curve (above) is the only number
  anyone has. Watch a window and see whether ~16/s rising is right.
- `@verify-ingame` **Is Void Metamorphosis greyed out below a full bank, or merely
  unusable?** simc refuses the action; whether the client shows the button as unusable (and
  therefore whether the Cooldown Manager already communicates the gate) is unmeasured.
- No Warcraft Logs history has been distilled for this spec — it is new in Midnight and
  Season 2 has not opened.

## Changelog

**2026-08-27 — Void Metamorphosis → Collapsing Star added to the override table.** The table
listed five pairs and omitted the sixth, and `abilities.md` said only that the transform
*"unlocks"* Collapsing Star. Measured in the client: the Void Metamorphosis button **becomes**
Collapsing Star for the whole window — same keybind, changed art, drawn unusable below the
30-fragment grant. "Unlocks" was not wrong so much as weaker than the fact, and the difference
is load-bearing for anything reading the button rather than the spell.

**2026-08-17 — rewritten as a supplement to the generated `simc-apl.md`.** The file was a
hand-transcription of the **12.0.7** MID1 profiles, at `confidence: low`, with no reference
to `simc-apl.md` at all — two copies of the priority in one folder. The transcribed
Annihilator single-target / AoE / in-Meta lists are deleted rather than annotated; the
current list is one file away. What the re-source changed:

- **The APL has four branches, not one.** The old file described a single Annihilator
  priority with Void-Scarred as a footnote. `talent.the_hunt` forks each hero tree into a
  ranged priority list and a melee one, and `voidscarred_melee` is a three-state machine
  rather than a list.
- **`collapsing_star_stacking` caps at 40, not 30.** The old sourcing note read "max_stack
  30 confirms Collapsing Star's 30-Soul cost". 30 is the *grant threshold*
  (`talent.collapsing_star->effectN(1)`); the buff's `CumulativeAura` is **40**. The
  distinction is what makes `voidscarred_ranged`'s `stack>=35` reachable at all — under the
  old number it would have been dead code and Collapsing Star would never fire at single
  target.
- **Reaper's Toll, Pierce the Veil and Predator's Wake are identified** as the Void
  Metamorphosis forms of Hungering Slash, Voidblade and The Hunt.
- **Voidstep is real.** `abilities.md` said "no talent named Voidstep exists in the 12.1
  tree", which is true and misleading: Voidstep (`1223157`) is the **buff** Hungering Slash
  grants — *"your next Vengeful Retreat will release a Cosmic explosion"* — and it is the
  only thing that makes Vengeful Retreat a press in `voidscarred_ranged`.
- **Voidsurge is the 12.1 name** for the Void-Scarred signature; `talents.md`'s
  **Demonsurge** is a stale build's string, and the tree itself is Fel-Scarred's node set.
- **The Season 2 tier set moves three rungs**, including creating the branch's biggest rank
  swing (Soulburst on Consume).
- **The Fury drain in Meta is a fitted simc curve**, not a game constant.

**2026-08-11 — the 12.1 rebalance.** Mastery's in-Meta bonus −66 %, all ability damage
+32 %, Consume +60 % (Devour excluded), Void Ray's Meta bonus 40 % (was 67 %), Collapsing
Star +12 %, Eradicate −6 % / −15 % secondary, Impending Apocalypse 20 % (was 30 %), Final
Hour 6 s (was 8 s), Otherworldly Focus 30 % (was 35 %), Hungering Slash's follow-up reworked
to a temporary Vengeful Retreat charge. `abilities.md` holds the full table.

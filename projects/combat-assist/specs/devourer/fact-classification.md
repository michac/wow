# Devourer Demon Hunter — fact classification

**What this file is for.** The **safety case**: every fact this catalog consumes, sorted readable / sealed-display / open, with its recipe and evidence. It stands alone so that *"does anything here branch on a sealed value?"* can be answered without reading the roster.

⚠ **Section numbers are preserved from the single-file catalog they were split out of
(2026-08-19), so a `§4.x` citation anywhere still resolves here.** They are not renumbered
precisely so those citations keep working.

**Cross-links.** `catalog.md` beside this file is the definition — roster, lanes, cues, contract
boundary. `../spec.md` §3.6 owns the readable/sealed boundary, `../authoring.md`'s recipe index the recipe IDs,
`../render-shelf.md` every pixel. **Three files per spec** (`../authoring.md` §0): a definition,
its proof, and its safety case.

---

## 4. Fact classification

Every fact this catalog would consume, tagged **readable** / **sealed-display** / **open**
against `../authoring.md`'s recipe index, with the evidence behind it. `../spec.md` §3.6 is
the boundary: **no sealed fact appears in a proposed Lua condition, in either polarity.**

### 4.1 The resources: both sealed, for different reasons

**Fury is secret**, as on every DH spec. `PowerType.csv` gives `FURY` id 17, and the Midnight
alpha blue post lists exactly seven never-secret power types — Combo Points, Runes, Soul
Shards, Holy Power, Chi, Arcane Charges, Essence — of which Fury is not one (R3). So this
catalog declares **no `power` field** and uses **no `resource` predicate**, exactly as Havoc.
Fury reaches the player only through S1's graded route.

**Soul Fragments are not a power type at all.** There is **no soul-fragment row in
`PowerType.csv`**, and Blizzard's own `DemonHunterSoulFragmentsBar` appears in the shipped UI
as a consumer of `isFullUpdate` **aura** payloads rather than `UnitPower`
(`knowledge/addon-dev/cooldown-manager.md:855`). Under 12.1's wholesale aura secrecy the soul
count is **sealed-display**. The same holds for the two stacking counters the APL reads —
they are auras, and their maxima are Tier 1:

| Counter | Aura | Max stacks | What it means |
| --- | ---: | ---: | --- |
| `void_metamorphosis_stack` | `1225789` | **50** | the soul bank. Void Metamorphosis is uncastable below the **required** count, and that requirement is talent-selected: **50**, or **35 with *Soul Glutton*** (`catalog.md` §1c). The aura's cap and the cast's requirement are the same number only on the build without the talent. |
| `collapsing_star_stacking` | `1227702` | **40** | in-window harvest. Every **30** grants a Collapsing Star; the counter itself wastes above 40. |

`[T1: SpellAuraOptions.CumulativeAura @ 12.1.0.69214]`. ⚠ The 30/40 distinction is the one
the KB previously had wrong (it recorded max 30, conflating the grant threshold with the
cap) — which is exactly what makes rung 5's `stack>=35` reachable rather than dead code.

### 4.2 The hinge: four of the branch's buff gates are readable procs

cap's readable `proc` predicate is `C_SpellActivationOverlay.IsSpellOverlayed(spellID)`
(`Sense.lua:69-74`) — a plain boolean keyed on a spell id, wholly independent of the aura
API, and measured readable in combat (`cooldown-manager.md:1339`, `[client]`, 27 fires in a
measured pull). **A buff Blizzard registers as a spell-activation overlay is readable; one it
does not is sealed.** That distinction decides most of this design, because **11 of the 15
lines are gated on buff state**.

It is answerable from Tier-1 game data without logging in. `SpellActivationOverlay`
`[T1 @ 12.1.0.69214]` carries an `IconHighlightSpellClassMask`; a spell glows when its
`SpellClassOptions` mask intersects it within the same class set (107 = Demon Hunter). Resolved:

| APL term | Aura | Overlay row | Icon-highlights | Lane |
| --- | ---: | --- | --- | --- |
| `buff.voidstep.up` | `1223157` | 4785, mask₀ = 8 | **Vengeful Retreat** (198793 / 198813 / 344866) | **readable** |
| `buff.eradicate.up` | `1239524` | 4854, mask₃ = 64 | **Reap · Eradicate · Cull** | **readable** |
| `buff.moment_of_craving.up` | `1238495` | 4853, mask₃ = 64 | **Reap · Eradicate · Cull** (plus a full-screen overlay, art `7549806`) | **readable** |
| `buff.soulburst.up` | `1297433` (S2 2pc) | 5065, mask₃ = 2 | **Consume · Devour** | **readable** |
| *(Reaper's Toll replacement)* | `1245523` | 4885, mask₃ = 2048 | **Hungering Slash · Reaper's Toll** | **readable** |
| `buff.void_metamorphosis_stack` | `1225789` | — | none | **sealed-display** |
| `buff.collapsing_star_stacking` | `1227702` | — | none | **sealed-display** |
| Void Metamorphosis itself | `471306` / `1217605` | — | none | (readiness only) |

⚠ **This is Tier-1 *candidate*, not measured.** The DB2 says the glow exists; it does not
prove `IsSpellOverlayed` answers true for it in instanced combat. The status is the one
Havoc gave Immolation Aura's charge row: settled by mechanism, named as a flight question,
never asserted as measured. `@verify-ingame` (§8, item 1).

⚠ **Two auras glow the same three spells, and cap cannot tell them apart.** Eradicate
(`1239524`) and Moment of Craving (`1238495`) both highlight Reap / Eradicate / Cull, so
`proc(reap)` is their **OR**, not either one. Rung 8's hold —
`!buff.eradicate.up | !buff.moment_of_craving.up | 4pc`, i.e. *hold Void Ray only when both
are already banked and you lack the 4-piece* — needs the **AND**, and is therefore **not
authorable**. Its necessary condition is authorable and its sufficient condition is not, and
a negative badge authored on the necessary condition would fire in states where the APL
casts. So rung 8 gets **no hold**, and Void Ray is directed by affordability instead (§5).
This is a genuine expressiveness gap and it is stated rather than papered over.

⚠ **`buff.voidsurge_reapers_toll` / `buff.voidsurge_pierce_the_veil` are not game auras at
all.** Both are simc's `demonsurge_placeholder_buff`, created `set_quiet(true)` and triggered
for every Voidsurge ability on entering the form — the sim's own bookkeeping for "this
window's empowered cast is still owed" (`sc_demon_hunter.cpp:10213-10222`). Rungs 11 and 12
therefore have nothing behind them to read. This is the **same open fact as Havoc's
`demonsurge_available`** (its open-facts item 6), on the same hero tree, and resolving it
resolves both. `1245523` is adjacent but describes the *replacement*, not the owed cast.
`@verify-ingame` (§8, item 2).

### 4.3 Main classification table

| Fact | Lane | Recipe | Evidence | Consumed by |
| --- | --- | --- | --- | --- |
| `ready` — spell readiness | **readable** | R2 | `cooldown-manager.md`, `cdm-rider-patterns.md` — Settled | every lit row for ITSELF, plus **one cross-row read**: cue **H** asks `ready(void_ray)` from the Void Metamorphosis row, to hold the in-form Collapsing Star while the rung above it can actually fire. Named because a cross-row read is a different claim from self-readiness and this table is where the question *"does anything here branch on a value cap may not read?"* is supposed to be answerable without the roster. It does not: `ready` is R2 on any bound row. |
| `affordable` / `insufficientPower` | **readable** | R1 | `security-taint-and-restricted-data.md` — Settled | **Void Ray** (100 Fury). The one spender in the branch with a real cost. |
| `identity` — Void Metamorphosis override (`overrideSpellID ~= spellID`) | **readable** | R7 | `cooldown-manager.md`, `observations.md` — Settled; the third chain measured in game 2026-08-27 | Reap→Cull/Eradicate; Voidblade→Hungering Slash/Pierce the Veil/Reaper's Toll; **Void Metamorphosis→Collapsing Star**. **Three chains on one spec**, the Voidblade chain is three-deep, and the third is the reason the spec's most-missed press is reachable at all — Collapsing Star has no `CooldownSetSpell` row of its own and rides Void Metamorphosis's (`catalog.md` §3). |
| `proc` — spell-activation overlay | **readable** ⚠ candidate | R2-adjacent; `IsSpellOverlayed` | `cooldown-manager.md:1334-1341` `[client]` for the API; §4.2's DB2 rows for *which* auras | Vengeful Retreat (Voidstep); Reap (Eradicate ∪ Moment of Craving); Consume/Devour (Soulburst) — **but Consume has no row**, §3 |
| `talent` — trait-config node/entry | **readable** ⚠ `[gap]` on the call | the `talent` predicate (shipped for Havoc) | ⚠ `knowledge/addon-dev/` records nothing about `C_Traits.GetNodeInfo` — the same open item as Havoc's #7 | `devourers_bite` (node 110167 / entry 136692) gates rung 1; `eradicate` (node 107345 / entry 132287) gates rung 2; `soul_glutton` selects the bank threshold and cue B's break point (`catalog.md` §1c) |
| `aoe` — cap's own `/cap aoe` toggle | **readable, not a game read** | the `aoe` predicate (shipped) | n/a — cap owns the value | rungs 2, 3, 5, 9. **Four target-count terms**, against Havoc's one. |
| Secret **Fury value / Fury-%** | **sealed-display** (`sealed-power-percent`) | S1 graded + an authored `threshold`, selected on `talent(soul_glutton)` — the talent drains 25 % faster, so the break point is per-build (`catalog.md` §1c) | `security-…` — Settled; the number itself is simc's fitted model | **Soul Immolation** in Meta — rung 13's `fury < void_metamorphosis_base_drain_ps` |
| **Soul bank** (`void_metamorphosis_stack`, 0–50 aura cap) | **sealed-display** | S2, as `sealed-count-bands` (V16/V17). The band's threshold is talent-selected — **35 with *Soul Glutton*, else 50** — so it is authored as two mutually-exclusive `when`-gated markers, one per build | OBS-065 for the mechanism; §4.1 for the cap; `catalog.md` §1c for the fork | Void Metamorphosis readiness; rung 1's pre-transform Voidblade |
| **Collapsing Star counter** (`collapsing_star_stacking`, 0–40) | **sealed-display** | S2, as `sealed-count-bands`. The authored threshold is the **grant at 30**, not rung 5's 35 — 35 would hatch a row rung 9 wants pressed (`catalog.md` §6) | as above | rung 5 — *"five from wasting harvested souls"* |
| A related ability's **cooldown remaining** | **sealed-display** (`sealed-cooldown-range`) | S4 | `cdm-rider-patterns.md` — Settled | **nothing in this branch.** No rung in `voidscarred_ranged` reads another ability's `cooldown.X.remains`. Havoc's most-used sealed form has **no consumer here**. |
| `action.reap.souls_consumed` — fragments **on the ground** | **open** | — no API tried that could carry it | `[searched 2026-08-17: PowerType.csv, the CDM readable surface, the shipped UI's DemonHunterSoulFragmentsBar]` — ⚠ **every one of those is a player-state instrument, and this is not player state.** The search looked in the right places for the wrong kind of thing. See the note below. | rungs 6, 7 — the `reaps` gate. **No hint.** |
| `fight_remains` | **open** (and out of scope) | — | — | rung 7. Perfect information; no human equivalent. |
| `buff.voidsurge_*` — an owed empowered cast | **open** | — | §4.2; simc placeholder | rungs 11, 12. **No hint.** Shared with Havoc's open item 6. |
| Void Metamorphosis **castability below the bank threshold** | **open** | R1 (`isUsable`, first return) | unmeasured | rung 2's gate as a *readable* hold. ⚠ It is no longer what holds up the drawing: the client does **not** grey a fragment-gated button — desaturation means on cooldown and nothing else, and usability is a tint *[T1 src @12.1.0: `knowledge/addon-dev/cooldown-manager.md` §3.4]* — so `scenarios.md` §7.1 eliminates that row with cue **C**'s own sealed band instead, reading nothing. See §8, item 3 (item 7 collapsed into it 2026-08-26). |
| Collapsing Star **castability** — a spell gated by aura-granted access | **client-drawn; cap neither reads it nor redraws it** | — | the client's usability **vertex-colour tint** `ITEM_NOT_USABLE_COLOR` *[T1 src @12.1.0: `cooldown-manager.md` §3.4, `CooldownViewer.lua:1195-1233`]*, seen on the in-form row in game 2026-08-27 | **nothing.** It was the gate on a V12 gated virtual row until 2026-08-27; Collapsing Star is a Cooldown Manager row (`catalog.md` §3), Blizzard already draws its availability, and cap does not draw a second mark for a fact the client marks. ⚠ A tint is not one of cap's three eliminating signals, so what rules the row out of a **walk** is a separate question — `scenarios.md` §7.2. |

**No sealed fact appears in any proposed condition above.** The soul bank, the Collapsing
Star counter and Fury are sink-only; every gate is `ready`, `affordable`, `identity`, `proc`,
`talent` or `aoe`.

⚠ **Two different quantities were being conflated, and only one of them is player state.**
The distinction is what decides where `action.reap.souls_consumed` can be looked for at all.

- **Collected / banked** — a player **aura stack**: `void_metamorphosis_stack` (`1225789`,
  cap 50) out of the form, `collapsing_star_stacking` (`1227702`, cap 40) inside it. Blizzard's
  shipped `DemonHunterSoulFragmentsBar` draws this, as a bar. ⚠ It is **not a resource**: Demon
  Hunter has exactly one row in `PowerType.csv`, **FURY (17)**, and there is no soul-fragment
  power type at all — so that bar is an aura stack rendered as a bar. cap still cannot
  read it, and the **sealed-display (S2) classification above is correct and stays**.
- **On the ground** — fragments that have spawned and not yet been picked up, collected by
  walking over them (`pick_up_fragment`) or harvested by Reap. This is what the APL's
  `action.reap.souls_consumed` counts, and it is a count of **world objects, not player state**.

The `[searched 2026-08-17]` marker names three instruments — `PowerType.csv`, the CDM readable
surface, `DemonHunterSoulFragmentsBar` — and **all three read the player**. That is why the
search came back empty: it was the right search for the banked count and the wrong one for this.

**One route has not been tried: the combat log.** Fragment spawn and despawn events, with cap
maintaining a derived count off them, is the only shape that could carry a world-object count into
a readable predicate. ⚠ **Nothing in `knowledge/addon-dev/` covers CLEU**, so this is a
**candidate ClientLab question and not a working answer** — and a derived count can desync from
the world (a missed event, a fragment expiring off-log, a reload mid-pull) in a way an authoritative
read cannot. It stays **open**, now with a named next step rather than a settled negative.

### 4.4 What this spec does *not* need, and one thing it does

- **No `sealed-cooldown-range` band.** Havoc's signature mechanism — hold this because a
  related cooldown is near or far — has **zero consumers** in this branch. Devourer's
  ordering-reasons are resource-and-buff shaped, not cooldown-alignment shaped.
- **No new sealed form is required** by anything above. S1's `threshold` (shipped for
  Felblade) and S2's `sealed-count-bands` (V16/V17 — which replaced `player-aura-stacks` and its
  `min = 2` guard on 2026-08-22) cover the two sealed values, and R1/R2/R7 plus the shipped `proc` / `talent` / `aoe` predicates cover the
  readable ones.
- **But R7 is harder here than anywhere cap has been.** Three chains on one spec, and the
  Cooldown Manager reaches Collapsing Star only through one of them (`catalog.md` §3): a spell
  with no `CooldownSetSpell` row of its own has an icon exactly when some other row overrides to
  it, which is the reading Retribution's Hammer of Light already had written down. Voidblade is a
  **three-deep** chain
  — Voidblade → Hungering Slash (a 6 s replacement, out of Meta) → Pierce the Veil (in Meta)
  → Reaper's Toll (in Meta, when Hungering Slash is the live form). `1245523` exists
  precisely to say *"Pierce the Veil is replaced with Reaper's Toll"*. Bind a static
  identity with the full id union and never carry state across a flip.

---

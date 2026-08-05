# Observability map — Havoc Demon Hunter

What the game will let the HUD read for this spec, what it hides, and what is simply
**not there**. Three categories, and conflating them is how a spec ships a lie:

- **SECRET** — the client has the value and refuses it under Midnight 12.0's Secret
  Values (`GetSpellCooldown` in combat, aura durations, stack counts).
- **MISSING** — nobody is hiding it; the pipeline has no channel for it (target health,
  target count).
- **ABSENT** — the value does not exist in the CDM's tracked set at all, so there is no
  row to ask. **This is Havoc's characteristic problem** and it is the one a future
  build could change.

> **⚠ PART-FLOWN.** Most of what follows is still desk-derived — reasoned from Tier-1 DB2 @
> 12.0.7 and the settled game-wide readability rules (`docs/adding-a-spec.md` → *the
> readability rules are already settled*) — and the open questions at the bottom are what the
> in-game pass exists to close.
>
> **What the FIRST 2026-08-03 flight settled is the resource, and it settled it the hard
> way:**
> **Fury is SECRET** and this document did not say so. See *SECRET* below, and
> `docs/multi-class-rollout.md` → § FLIGHT RECORD — PHASE 2. ⚠ The lesson generalises past
> Havoc: this file's three categories (SECRET / MISSING / ABSENT) were applied to cooldowns,
> auras and stacks, and **the resource rail was never put through them at all** — it was
> assumed readable because the two Warlock specs' was. A future spec's map must classify its
> **resource** explicitly, first.

---

## THE FLIGHT'S JOB — and why it is bigger than Havoc

Havoc is the 4th registered spec and the 2nd class outside Warlock. Ordinarily its
in-game pass would be a smoke test. **It is not, and this section is the reason.**

`docs/multi-class-rollout.md`'s gate said Phase 2 was blocked until a **max-level
Retribution** pass. That pass cannot happen — the player has no max-level Paladin. The
level-37 flight of 2026-08-03 found five defects but could not exercise the hero-tree
branch, the burst lines, or `roster-state-plan.md` Phase 5's acceptance at all.

The user's decision (2026-08-03) was to proceed to Havoc and **discharge the gate from
the Demon Hunter side instead** — the player *does* have a max-level Demon Hunter. So
this flight carries two sets of criteria: Havoc's own, and the inherited Phase-5 /
Retribution-pattern criteria that have nowhere else to run.

If it finds a pattern defect, that defect is now in **two** shipped specs rather than
one. That is the accepted cost, and the mitigation is that this flight happens **before**
Protection, Vengeance and Devourer — not after.

> ### ✅ FLIGHT 2 (v0.32.94) PASSED — Phase 1 is discharged. FLIGHT 3 is for v0.32.95.
>
> 1276 in-combat lines. Every Phase-1 criterion (10–13) cleared, and **criteria 2 and 3 were
> exercised for the first time**: the meta fork resolved (`# config` flipped
> `BD,CS ↔ Anni,DS` six times mid-session) and Felblade + Vengeful Retreat both cued from
> CDM-Utility rows.
>
> | | flight 1 (v0.32.93) | flight 2 (v0.32.94) |
> |---|---:|---:|
> | `PW:` | `0/+0` ×2380 | **`restricted` ×1298** |
> | Chaos Strike + Annihilation | **0** | **452 (35.4 %)** — top winner |
> | Eye Beam / Abyssal Gaze | 0 | 277 |
> | Blade Dance / Death Sweep | 0 | 140 |
> | Metamorphosis | 0 | 119 |
> | Throw Glaive | 770 (top) | 0 |
>
> **Rider answered:** `C_AssistedCombat.GetNextCastSpell` returns a **readable number in
> combat** (201427, Annihilation) — publish under `api-events-and-discovery.md` §2. It
> agreed with the Coach, which makes it a usable independent oracle.
>
> **⏳ WHAT FLIGHT 3 MUST ADD — criteria 14–17, all new in v0.32.95:**
>
> | # | Criterion | Instrument |
> |---|---|---|
> | 14 | **Immolation Aura cues at its charge cap.** Flight 2 had it win ZERO on 839 ready-with-a-charge lines; L12 now promotes it above the spender at `cur >= max` | decision log `w:IA:charge_cap` vs `CH:IA=` |
> | 15 | **The COMPANION DOT reads as "press twice", not as clutter.** ⚠ EYEBALL ONLY — this is a design call, not a measurement | on screen; log shows `w:CS+1` |
> | 16 | **The LOOK-AHEAD leads usefully** — does the second dot help, or jump around? | on screen + `fb:` in the log |
> | 17 | **AoE (L4, L14) and Essence Break (L6, L8) actually run.** Neither flight has exercised either: flight 2 had zero `AoE` notes and `EssB:unlearned` on all 1298 lines | `/cdmp aoe`; a build that talents Essence Break |
>
> ⚠ **`wowkb.cdmp flight` reports ONE FALSE FAILURE on this spec** — *"the DoT `not_up` cue
> appears at all: 0 vs 0"* is a **Destruction** criterion scored against a Havoc flight, and
> Havoc has no DoTs. Ignore it until the tool skips it.
>
> ### ⚠ FLIGHT 1 RAN 2026-08-03 ON v0.32.93, AND IT FAILED — the record, kept.
>
> Fury is secret (see *SECRET* below), so every Fury gate compared against a fabricated zero.
> 2380 decision-log lines, 2374 in combat, `PW:0/+0` on all of them:
>
> | winner | count | why |
> |---|---:|---|
> | Throw Glaive | 770 | L15 — its cost resolved to 0 |
> | Vengeful Retreat | 480 | L5 — no Fury gate |
> | Felblade | 414 | L11 — `deficit = 120 - 0`, always ≥ 40 |
> | Immolation Aura (+CFire/CFire2) | 385 | L12 — same |
> | The Hunt | 41 | L3 — no Fury gate |
> | **Chaos Strike / Annihilation** | **0** | L8/L13 — `projected >= cost` never true |
> | **Eye Beam** | **0** | L9 — same |
> | **Blade Dance / Death Sweep** | **0** | L7/L10 — same |
> | **Metamorphosis** | **0** | L2 — vetoed by a misread Blade Dance term (Dev. 12) |
>
> Criteria 1 and 5 were exercised; **2, 3 and 4 were not meaningfully tested** (the cues that
> would have shown the meta fork never fired). Phase 1 was the remediation — `rotation.md` →
> *Fury is SECRET* — and it flew clean on v0.32.94, above.

### Acceptance — Havoc's own

| # | Criterion | Instrument |
|---|---|---|
| 1 | `/cdmp hud layout` matches the DB2-predicted tracked set from Step 0 (10 Essential incl. Rain from Above; Felblade / Vengeful Retreat / Fel Rush on Utility) | `hud layout` |
| 2 | **The meta fork resolves.** In Metamorphosis the cues read **Annihilation** and **Death Sweep**, not Chaos Strike and Blade Dance | `hud layout` + the decision log's `w:` field |
| 3 | **Felblade and Vengeful Retreat cue at all** — the CDM-Utility question | decision log |
| 4 | **Fel Rush does not cue while genuinely on cooldown** — the lying-base-cooldown question | decision log `CD:` vs `CH:` |
| 5 | A hero swap flips the tree in `# config` **without a `/reload`** | decision log `# config` |

### Acceptance — the Phase-1 remediation ✅ ALL FOUR PASSED on v0.32.94

| # | Criterion | Instrument |
|---|---|---|
| 10 | **`PW:` reads `restricted`, never `0`.** A number in that column means the rail is being fabricated again | decision log `PW:` |
| 11 | **Chaos Strike / Annihilation is the MOST COMMON winner**, as it is in any real Havoc rotation. Zero was the failure; dominant is the pass | decision-log winner distribution |
| 12 | **Eye Beam, Blade Dance / Death Sweep and Metamorphosis each cue at least once**, and Throw Glaive is no longer the top winner | same |
| 13 | `IsSpellUsable` behaves from a tainted 10 Hz tick as it did from the macro — no divergence between the verdict and what is castable | decision log + play |

⚠ **`w:-` IS NOT THE SCORE HERE.** Flight 1 scored **0.0 %** in-combat `w:-`, a perfect
number, precisely because the generator lines were jammed on and something always won.
**Read the winner distribution, not the ratio.** Flight 2 also scored 0.0 % and there it was
genuine — which is exactly why the ratio proves nothing on its own. Criterion 8 below still
applies as a floor.

### Acceptance — v0.32.95's three new features ⏳ NONE FLOWN

| # | Criterion | Instrument |
|---|---|---|
| 14 | **Immolation Aura cues at its charge cap** (L12). Flight 2 had it win ZERO across 839 lines where it was ready with a banked charge | `w:IA:charge_cap` vs `CH:IA=` |
| 15 | **The COMPANION DOT reads as "press twice"**, not as clutter. ⚠ **EYEBALL ONLY — a design call, not a measurement** | on screen; `w:CS+1` in the log |
| 16 | **The LOOK-AHEAD leads usefully** rather than jumping around | on screen + `fb:` |
| 17 | **AoE (L4, L14) and Essence Break (L6, L8) actually run** — neither has ever been exercised | `/cdmp aoe`; a build talenting Essence Break |

### Acceptance — the inherited Phase-5 criteria this flight discharges

| # | Criterion | Why it lands here |
|---|---|---|
| 6 | `abilities` is never empty on login — the wholesale guard, the v0.32.25 shape | Phase 5's own; never flown |
| 7 | **No ability cues while its own cooldown reads down** — the roster-anchor root fix, the generalised form of Retribution's `Judg=c<n>` beside `Judg~1/1` (191 of 226 lines) | the fix shipped v0.32.92 and has never been observed |
| 8 | In-combat `w:-` ratio no worse than v0.32.90's **13.9 %** | the charge fixes raised it and nobody has watched it since |
| 9 | **MEASURED, not scored:** the out-of-combat guarded-call rate | Phase 5 sizing claim |

### The procedure

```
# in game, on a max-level Havoc Demon Hunter
/reload
/cdmp hud status        # expect: spec: Havoc (profile active)
/cdmp hud coverage      # every blind row must be an ability the character LACKS
/cdmp flight            # ARM FIRST — then just play
#   ... single-target at a dummy, then /cdmp aoe on a pack ...
#   ... swap hero tree (Fel-Scarred <-> Aldrachi Reaver) ...
#   ... respec away to Vengeance and back, to prove the active/passive toggle ...
/reload                 # ⚠ SavedVariables only flush here
```
```bash
uv run python -m wowkb.cdmp flight        # exit 2 = "never flown", NOT a pass
uv run python -m wowkb.cdmp decisionlog   # read the COMBAT SPLIT, never the raw w:- ratio
```

⚠ **One extra, and it is worth the thirty seconds** (the session log's own lesson —
`chargeCD = 12` was wrong by 2 s and one read caught it): **out of combat**, before
arming, dump `C_Spell.GetSpellCharges` for the four charge-category abilities. It gives
the charge/no-charge split *and* the haste-scaled recharge in one pass, and it is the
only way to check the three lying base cooldowns against the truth.

```
195072 Fel Rush          -> expect ~1/1 rc≈10 * haste   (base reads 1 s)
258920 Immolation Aura   -> expect ~1/1 rc≈30 * haste   (base reads 2 s)  [2/2 with A Fire Inside]
198793 Vengeful Retreat  -> expect ~1/1 rc≈25 * haste   (base reads 0.5 s)
185123 Throw Glaive      -> expect ~1/1 rc≈9  * haste   (base reads 0 s)
198013 Eye Beam          -> expect nil (an ORDINARY cooldown — the control)
```

The control matters: `C_Spell.GetSpellCharges` **refuses (nil)** for an ordinary
cooldown, which is the property that makes `cur ~= nil` the real charge predicate.

---

## Readable — the channels this spec's list actually stands on

| Fact | Channel | Confidence |
|---|---|---|
| A tracked ability's readiness | the CDM's `Available` / `OnCooldown` alert edges + the napkin | settled |
| **The meta fork** | `item:IsActive()` on the Metamorphosis TrackedBuff row (191427) **and** the Chaos Strike frame's `liveSpellID == 201427` | settled channel, two sources |
| **Every override label** | `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` + live-identity divergence — the same channel Demonology's Ruination and Retribution's Hammer of Light use | settled |
| Buff **presence** (Inner Demon, Initiative, Art of the Glaive, …) | `item:IsActive()` on the TrackedBuff row | settled |
| Fury value and cap | `UnitPower(unit, Fury, true)` — works in combat | settled (Phase 6.2) |
| **Fury AFFORDABILITY, per spell** | `C_Spell.IsSpellUsable(id)`'s 2nd return, `insufficientPower`, via `ns.SpellUsable` | ✅ **VALIDATED IN GAME 2026-08-03** — and it is the whole resource channel now; see *SECRET* below |
| Fury **costs**, as numbers | `C_Spell.GetSpellPowerCost` filtered to `Enum.PowerType.Fury` via `ns.PowerCost` | readable, and **NO LONGER CONSUMED** by this spec — there is nothing to compare a cost against. ⚠ It also disagrees with the client: DB2 says Throw Glaive costs 25, the live client reports it FREE |
| Fury's **max** | `UnitPowerMax` — a DIFFERENT secrecy predicate (`SecretWhenUnitPowerMaxRestricted`, non-player-controlled units only) | readable; **170** measured. Only the current value is secret |
| **The Essence Break window** | cast history — `UNIT_SPELLCAST_SUCCEEDED` spellIDs are readable in combat — against 320338's 4000 ms DB2 duration | settled channel, **derived** value |
| Charge counts | `C_Spell.GetSpellCharges` OOC + State's in-combat charge napkin (`ChargeGained`) | settled |
| The active hero tree | `C_ClassTalents.GetActiveHeroTalentSpec` → `TraitSubTree` (34 / 35) | settled (Phase 0.4) |
| **Eye Beam's remaining cooldown** | our own napkin — its 30 s lives on the spell row, so `ns.BaseCooldown` reads it | settled, and L5's whole basis |

## SECRET — the client has it and will not say

| Fact | simc gates that die |
|---|---|
| **FURY ITSELF — the current value** | ⚠⚠ **every** `fury>=N` / `fury.deficit>=N` gate in the APL. See below; this is the headline |
| A cooldown's remaining duration, in combat (`C_Spell.GetSpellCooldown`) | Metamorphosis's :103 alignment block; The Hunt's :115 Eternal-Hunt clauses; every `cooldown.eye_beam.remains<=N` inertia gate; the `chaotic_transformation` handshake |
| Aura durations | `buff.metamorphosis.remains<gcd.max` (the "meta is ending, dump" line); `buff.inertia.remains`; `buff.demonsurge.remains<gcd.max` |
| Aura **stack counts** | `buff.cycle_of_hatred.stack<3/4`; `buff.immolation_aura.stack`; the Art-of-the-Glaive fragment count |
| `C_UnitAuras` generally, in combat | any aura read outside the CDM's own `IsActive()` |

### ⚠⚠ FURY IS SECRET — the finding that failed the first flight

`UnitPower("player", Enum.PowerType.Fury)` returns a **Secret Value**. This section did not
mention Fury at all before 2026-08-03, and that omission is what shipped a HUD whose entire
core rotation was unreachable.

Secrecy is **per power type**, and the rule is **primary vs. secondary resource** — Blizzard
blue post, *Midnight Public Alpha Addon API Changes*, 2025-11-24: *"…the player's **secondary**
resources are no longer secret (**primary resources remain secret**). Affected resources:
Combo Points, Runes, Soul Shards, Holy Power, Chi, Arcane Charges, Essence."* Fury is the
Demon Hunter's **primary** resource. Measured:

| probe | Fury (17) | Holy Power (9), the control |
|---|---|---|
| `C_Secrets.GetPowerTypeSecrecy` | **2** (`ContextuallySecret`) | **0** (`NeverSecret`) |
| `C_Secrets.ShouldUnitPowerBeSecret("player", …)` | **true**, in a city *and* mid-pull | false |

⚠ **The "context" is the UNIT, not combat** — the predicate reads *"…unless the subject unit
does not have a power of this type."* You always have Fury. **There is no out-of-combat
window and no seed value, ever.** ⚠ And this invalidated a claim in
`roster-state-plan.md` §7.2, which measured Soul Shards (never-secret) and generalised to
every power; that section now carries a correction box.

### ✅ RECLASSIFIED — `C_Spell.IsSpellUsable` *is* the rescue, for AFFORDABILITY

This section read *"⚠ `C_Spell.IsSpellUsable` is not a rescue"* until 2026-08-03. **That
verdict was right about READINESS and wrong about AFFORDABILITY**, and the distinction was
the difference between a working HUD and a broken one.

What was measured, and is still true: it **ignores cooldown**. `isUsable` returned **true**
for a spell visibly on cooldown during the Retribution flight. So it is not a readiness
channel, and `GetActionCooldown(slot)` is secret in combat, so the action-bar surface stays
closed exactly like `GetSpellCooldown`.

What was **not** asked: the **second return**. `insufficientPower` is documented as *"True if
spell is specifically unusable due to insufficient power (ie MANA, RAGE, etc)"*
`[T1 src: SpellDocumentation.lua:873-888 @ 12.0.7.68887]`, and the function carries
`SecretArguments = "AllowedWhenTainted"` with **no `SecretReturns` and no `SecretWhen*`
predicate at all** — both returns are plain booleans from a tainted caller.

**In-game validation, one sample, at low Fury:**

| spell | `isUsable` | `insufficientPower` |
|---|---|---|
| Throw Glaive 185123 | true | **false** |
| Eye Beam 198013 | false | **true** |
| Blade Dance 188499 | false | **true** |
| Chaos Strike 162794 | false | **true** |

Three spells reporting insufficient power while a fourth in the **same sample** reports fine
proves the flag is computed **per spell against its own cost**. At high Fury all four read
`true / false`. ⚠ **Throw Glaive is FREE per the client** while DB2 `SpellPower` says 25 —
**DB2 costs are not the client's costs**, and that mismatch is why the failed flight's L15
won 770 times.

⚠ **What it structurally CANNOT do: overcap.** It is binary — false at 40 Fury and at 170
alike — so *"the bar is full, dump it"* is unrecoverable through this channel. That is the one
thing Phase 1 knowingly gives up; `docs/multi-class-rollout.md` → *Phase 2* has the
`LuaCurveObject` design that recovers it.

## MISSING — no channel exists

| Fact | Consequence |
|---|---|
| Target health % | no execute logic; Havoc has none in this APL, so the cost is zero |
| Target count | every `active_enemies>=N` → the manual `mode` toggle |
| `time_to_die` / `fight_remains` | every end-of-fight dump line dropped |
| Talent knownness | readable OOC (`C_SpellBook.IsSpellKnown`, the Diabolic Embers precedent) but **not wired** for this spec. An ability talented out is simply untracked, which self-degrades correctly. |
| `variable.fury_gen_per_sec` | six terms including haste and three stack counts; every `fury.deficit > gen*gcd` becomes a flat threshold |

## ABSENT — not in the tracked set, so there is no row to ask

**This is the category Havoc is defined by, and it is the one a future patch could
change** (Blizzard edits `CooldownSetSpell` between builds).

| spellID | Name | What it costs us |
|---|---|---|
| **442442** | Rending Strike | the RG sequence's first ordering buff |
| **442435** | Glaive Flurry | the RG sequence's second ordering buff |
| **442294** | Reaver's Glaive (the buff) | "is a glaive armed" — recovered from the *transform* instead |
| **320338** | Essence Break (the debuff) | the window — recovered from *cast history* instead |
| 427641 / *the trigger aura* | Inertia | three inertia-consumer lines |

Two of the five have a workaround (transform, cast history). Three do not, and together
they are Deviation 1: **six of the APL's 140 lines are dark on Aldrachi Reaver.**

---

## Open questions the live pass must settle

| # | Question | Why it matters | How to answer |
|---|---|---|---|
| **1** | **Does the Fel Rush / Immolation Aura / Vengeful Retreat charge count actually arrive?** | This is the entire mitigation for the three lying base cooldowns. With a count, `usable()`'s one-charge rule (`cur >= 1 AND probablyUp`) vetoes the early cue. **Without one**, `usable()` falls through to `probablyUp or chargeBanked` and the 1-second napkin wins — an early cue on a button that cannot be pressed. | decision log: `CD:` vs `CH:` for `FR` / `IA` / `VR`. `FR~1/1` present ⇒ protected. `FR~` absent while `FR=` reads ready within 10 s of a Fel Rush cast ⇒ **the defect is live** and the napkin-tolerance fix in `rotation.md` is owed. |
| **2** | **Does the Chaos Strike frame really show `liveSpellID = 201427` in meta?** | L6–L13's entire fork, and criterion 2. The override is proven in DB2 (`Metamorphosis 162264`, `EffectAura 332`), but *which* channel surfaces it — `overrideSpellID`, `overrideTooltipSpellID`, or a live-identity divergence — is a client fact. | `/cdmp hud layout` while transformed; the decision log's `# config` line. ⚠ `ctx.inMeta` ORs the TrackedBuff row, so the fork survives even if this answers no — but the **icon label** does not, and that is half the value. |
| **3** | **Does a TrackedBuff row report a DEBUFF ON THE TARGET through `IsActive()`?** | Reaver's Mark 442679 is a target debuff filed as a TrackedBuff. No line reads it today, so this is not blocking — but it is the first time the project has met the shape, and Vengeance's `Frailty` (a 99-stack target debuff, 32 APL references) depends on the answer. | `/cdmp hud coverage` + the decision log's `PR:` field with and without a marked target. |
| **4** | **Is Fel Rush's double CDM row (Essential + Utility) claimed cleanly?** | `St.RosterClaims` assigns each row to at most one ability and prefers Essential. If both rows are claimed, or the Utility row wins, Fel Rush's readiness is read off the wrong frame. | `/cdmp hud coverage` — 195072 must read `ok` exactly once. |
| **5** | **Does Rain from Above draw an icon nothing ever cues?** | A tracked Essential the APL never mentions. Expected and harmless (it is a real button the player may press manually), but it is the first knowingly-dead icon the project has shipped and the coverage report should say `ok`, not `blind`. | `/cdmp hud coverage` |
| **6** | **Is `HAVOC_RG_FROM_BUFF` safe to enable?** | L1's second source. Art of the Glaive 442290 is the 80-stack fragment counter that arms Reaver's Glaive; if it is present for most of a fight, enabling this pins L1 at the top of the list permanently. **Expect the answer to be NO** — this is the Light's Deliverance shape, and that one was answered NO by measurement. | decision log `PR:` — is `AotG` present only while a glaive is genuinely armed, or nearly always? |
| **7** | **Does the keybind hint resolve for Chaos Strike and Fel Rush?** | The `SpecBindAlias` question. The rung ladder asks the action bar about 162794 / 195072 and will find nothing; the alias to 344862 / 344865 is the fix. | `/cdmp hud layout` → the `key=` column for those two rows. ⚠ If the hint is missing there, it is a *different* bug from the undiagnosed "first two CDM icons" issue in the rollout doc's *Still open* #2 — check `drew=` to tell them apart. |

## What this spec does NOT need a new testing layer for

Following `adding-a-spec.md`: the Secret-Values and cooldown-readability rules are
settled **game-wide invariants**, not per-spell facts, so nothing above re-measures
them. The one genuinely new *measurement* asked for is the OOC `GetSpellCharges` sweep,
and that is a thirty-second read, not a layer.

If Havoc *violates* an established contract — something that worked for three shipped
specs failing here — that is a genuine surprise worth a new instrument **at that point**.
Do not pre-build one.

# Observability map — the Retribution APL inputs vs. what the game lets us read

> **⚠ STATUS: reference / desk-derived.** For each field the priority list needs
> (`input-contract.md`), where the value comes from in the State pulse, how
> reliably it reads **out of combat vs. in combat**, and how it degrades. The list
> itself (`rotation.md`) is unchanged — this only says *how honestly each input can
> be fed*. **None of this has been confirmed against a live Retribution capture.**
> The Secret-Value facts carry over as settled game-wide invariants; the
> Retribution-specific rows are marked **verify**.

## Sources of truth for this pass

- **What the client exposes** — the State pulse: per-ability `cd`
  (`state ∈ ready|on-cooldown|unknown`, `source ∈ live|napkin|none|static`,
  `remaining`), `charge` (`cur`/`max`/`charged`), `glow` (the combat-readable
  spell-overlay proc signal), `aura`/`buff.isActive` (buff **presence**),
  `power.<PowerType>.{value,max,unmodified,unmodifiedMax,modifier}`, cast
  `history`, the spell `override`/`liveSpellID` (transforms), `hero`, and `mode`.
- **What is provably secret** (settled game-wide by the retired probe, and
  class-independent — do **not** re-verify per spec): in-combat
  `C_Spell.GetSpellCooldown` and `C_Spell.GetSpellCharges` read **secret**; cast
  `START`/`SUCCEEDED` spellIDs are **readable**; `item:IsActive()` is a **readable
  bool**; `IsSpellOverlayed` is **readable**; `C_UnitAuras` is **dead in combat**;
  the override channel works. Retribution inherits all of it unchanged.

## The readiness model (spec-agnostic — read Demonology's first)

Readiness is **observed, not guessed**: an observed CDM alert edge, else the
out-of-combat readiness baseline carried across combat entry, else the napkin
(a base-cooldown countdown from the last observed cast, which supplies *remaining*
only and expires to "probably-up, **unconfirmed**" — never a laundered `ready`).
The full statement is in `specs/demonology/observability-map.md` and transfers
verbatim.

### ⚠ Retribution's headline hole: four abilities have no napkin countdown

**Four of the nine Essential buttons keep their cooldown on a CHARGE CATEGORY** rather
than on the spell, so `SpellCooldowns.RecoveryTime` is 0 `[T1 DB2 @ 12.0.7]`.
⚠ *This section said "six" until 2026-08-03; Avenging Wrath and the two spenders are not
among them — see the note under the table.*

| Ability | ID | Charge category | Recovery | Max charges |
|---|---:|---:|---:|---:|
| Judgment | 20271 | 1663 | 11.0s | 1 |
| Crusader Strike | 35395 | 1627 | 6.0s | **2** |
| Blade of Justice | 184575 | 2128 | 12.0s | 1 |
| Wake of Ashes | 255937 | 2285 | 30.0s | 1 |

**Not in this set, and why it matters:** *Hammer of Wrath* (24275, category 1895) has the
same shape but is not one of the nine — it is not in the tracked set at all. *Avenging Wrath*
carries `CategoryRecoveryTime = 120000` on the **spell** row, so `GetSpellBaseCooldown`
answers for it normally. *Templar's Verdict* and *Divine Storm* read 0 because they have **no
cooldown**, which is not the same condition.

`ns.BaseCooldown` reads `GetSpellBaseCooldown`, which reports the **spell's**
recovery — 0 for all of these. So `HudNapkin` has nothing to count down from and
contributes **no** `remaining` for them. This is exactly the mechanism
`roster-state-plan.md` field-fix C2 recorded for Conflagrate ("Conflagrate's
`RecoveryTime` is 0 in DB2 — the recharge lives on its ChargeCategory — so the
base-cooldown countdown is 0 and the just-cast guard never fires"), except that on
Destruction it is **one** ability (Conflagrate, category 672) and here it is **four**.

**Consequences, in order of how much they bite:**

1. **Readiness for those four does NOT rest on the napkin** — it comes from the **charge
   count**, which State seeds out of combat and maintains in combat off the `ChargeGained`
   alert, using the charge-category recovery as a **gain floor** (`ns.ReadCharges`' third
   return → `State.chargeGain`). That machinery already ships for Destruction's Conflagrate.
   ⚠ An earlier draft of this section claimed readiness "rests entirely on the alert edges
   with no fallback underneath". That overstated it.
2. **`SOON` will not light** for them, and **`Escalate` cannot call them overdue** — both
   need a positive `remaining`, and there is none. This is the real, visible loss.
3. **The charged ones may read `ready` forever.** The measured CDM defect is that a
   charged ability raises `Available` on every charge restore and **never** raises
   `OnCooldown`, so State's ready-edge latches true and is never cleared. That is
   why `usable()` makes **the count authoritative and the cooldown read
   subordinate** — cloned verbatim from `CoachDestruction.lua:327-348`, where a live
   pass once had the HUD cueing Conflagrate at zero charges on **190 of 194** log
   lines.
4. **Whether a *1-charge* charge category is marked `charges = true` on the CDM row
   is unknown offline.** If it is, all four take the charged path; if not, only
   Crusader Strike does. Either way `usable()` is correct — it consults the count
   *when there is one* and falls back to the cooldown read otherwise. **verify**

⚠ Feeding the charge-category recovery into `ns.BaseCooldown` would fix (2) — the only
consequence that is still open. The duration itself is already read (State uses it as the
charge napkin's gain floor); what is missing is a spec-declared fallback the *napkin* can
count down from. A **new pipeline seam**, deliberately out of scope here, filed to
`docs/status.md` → backlog. ⚠ Mind the honesty rule if you build it: a declared constant is
not a measurement, so it must reach the pulse as something that can only make the HUD
*early*, never as `source = "live"`.

## Field-by-field

Legend: **OOC** = out of combat · **IC** = in restricted combat.

| # | Field | Source | OOC | IC | Degradation |
|---|---|---|---|---|---|
| 1 | `hp` / `hpMax` | `state.power.HolyPower` | ✅ exact | ✅ exact | **None.** `UnitPower`/`UnitPowerMax` are readable in combat for ordinary powers; `modifier` is 1 so the two rails coincide. Guarded anyway — a power that turned secret degrades to `readable = false` rather than tainting. |
| 2 | `spenderCost` | `ns.ShardCost` → `C_Spell.GetSpellPowerCost` | ✅ | ⚠ | Resolved live each pulse; an unreadable cost falls back to the declared 3. ⚠ The client **pre-applies the display divisor**, and Holy Power's divisor is 1, so unlike Soul Shards there is no unit conversion here at all — do not copy Destruction's `*Frags` multiplication. |
| 3 | `holFrame` | `liveSpellID ~= spellID` on a tracked spender row | ✅ | ✅ | The override channel is settled and works in combat (`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` + live-identity divergence). **This is the whole reason Templar is the v1 profile** — Hammer of Light's readiness arrives through the one proc-like channel that survives restricted combat. |
| 4 | `spenderKey` / `dsCastable` | `mode` + two tracked buffs | ✅ | ✅ | `mode` is our own toggle. Empyrean Power / Empyrean Legacy are presence reads off tracked rows. |
| 5 | `artOfWar`, `righteousCause`, `empyreanPower`, `empyreanLegacy`, `lightsDeliverance`, `wingsUp` | `state.buffs[id]` | ✅ | ✅ **presence only** | Presence is readable; **counts and durations are not**. Absence of a read is folded in by State as absence, never a false `true`. |
| 6 | `*Usable` | `Classify.probablyUp` ∨ a banked charge | ✅ exact | ⚠ edges + napkin | See the readiness hole above. |
| 7 | `fillerKey` | the Crusader Strike frame, whatever it shows | ✅ | ✅ | Presented as one key on purpose. |
| 8 | `hero` | `state.hero` (`C_ClassTalents`, cached) | ✅ | ✅ cached | Read OOC and cached, wiped on `SPELLS_CHANGED` / `TRAIT_CONFIG_UPDATED` / `PLAYER_SPECIALIZATION_CHANGED`. `TraitSubTree` 48 = Templar, 50 = Herald of the Sun `[T1 wago @ 12.0.7]`. **Never inferred from the tracked set** — field-fix B. |
| 9 | `targetHealthPct` | — | ❌ | ❌ | **Missing, not secret.** State has no target channel. L9 loses its execute half. |
| 10 | `activeEnemies` | — | ❌ | ❌ | Missing. Replaced by `mode`. |
| 11 | buff **durations** and **stacks** | — | ⚠ | ❌ | Secret in combat. Kills all four free-Hammer-of-Light timing clauses. |
| 12 | `cooldownRemains` of a *different* ability | `Classify.remaining` | ✅ | ❌ (secret; and no napkin countdown for the four charge-category abilities) | The ES ↔ WoA handshake is dropped. |

## Retribution-specific open questions (the live pass settles these)

1. **Does Hammer of Wrath get a virtual icon?** It is absent from the tracked set,
   so the only way it can ever be cued is `State.virtualCandidates`, which requires
   `ns.BaseCooldown(24275) == 0`. DB2 says `RecoveryTime = 0` (the cooldown is on
   charge category 1895), so it *should* qualify — but whether
   `GetSpellBaseCooldown` really returns 0 for a charge-category spell is untested.
   If it returns 7500 instead, Hammer of Wrath has **no icon and no virtual row**,
   and L9 is dead code. **verify** — `/cdmp hud coverage` answers it directly.
2. **Which Hammer of Wrath ID does the client surface** — 24275, 326730 or the
   Midnight talent-node 1241288? All three are mapped, the primary carries the
   cue, the other two are `expect = false` aliases. **verify**
3. **Which spender frame carries the Hammer of Light override** — Templar's Verdict
   85256, Divine Storm 53385, or both? Both are mapped; identity is keyed on the
   semantic `spender` field, so either resolves the same. The **decision log's
   per-ID `abbr` codes** (`HoL` on 85256's row vs `HoL2` on 53385's) are what let
   one capture answer this — the lesson `SpecDestruction.lua` learned the hard way
   when a shared `abbr` made its own capture unable to answer the question it was
   recording for. **verify**
4. **Is a 1-charge charge category marked `charges = true`?** See consequence (4)
   above. **verify**
5. **Is `RET_HOL_FROM_BUFF` safe to turn on?** Only if `/cdmp hud layout` plus the
   decision log show Light's Deliverance (433674) present **only** while a free
   Hammer of Light is genuinely available. If it is up for most of a cycle, leaving
   it off is correct and the switch should be deleted rather than flipped.
6. **Does the default tracked set match what actually loads?** The Destruction
   surprise (Incinerate absent from the union) says to check. `/cdmp hud layout` on
   a real Retribution character, once. **verify**

## What this spec does *not* need to re-verify

Stated explicitly so a future pass does not re-measure settled ground: the
cooldown-readability rules, the cast-event readability, `item:IsActive()`, the glow
channel, `C_UnitAuras`'s in-combat death, and the override/transform channel are
**properties of the API and the Secret-Values model**, not of the spell. They were
settled game-wide by the retired `/cdmp probe` and every spec obeys them
identically. `docs/adding-a-spec.md` carries the table.

---
title: Retribution Paladin — fact classification
spec: Retribution Paladin (Templar) — specID 70, Midnight 12.1
---

# Retribution Paladin (Templar) — fact classification

**What this file is for.** The **safety case**: every fact this catalog consumes, sorted readable / sealed-display / open, with its recipe and its evidence. It is separate so it can be read without reading the roster — the question *"does anything here branch on a sealed value?"* must be answerable on its own.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../pattern-shelf.md` owns the recipes; `../render-shelf.md` owns every pixel and this file
describes none. Priority source: `knowledge/classes/paladin/retribution/simc-apl.md` (Tier 1,
generated), explained by that spec's `rotation.md`; neither is restated here.

**Three files per spec, and Havoc is the model** (`../authoring.md` §0): a definition, its proof,
and its safety case.

---

## Facts, classified

Every fact the catalog consumes, tagged **readable** / **sealed-display** / **open**, with its
recipe and evidence (`../spec.md` §3.6 is the boundary; `../pattern-shelf.md` Parts 1–2 own the
recipes).

| Fact | Lane | Recipe | Evidence |
| --- | --- | --- | --- |
| Holy Power current value | **readable** | R3 | `C_Secrets.GetPowerTypeSecrecy(9)` → 0 `NeverSecret`, `ShouldUnitPowerBeSecret("player",9)` → false `[client 2026-08-03]`; T1 blue *Midnight Public Alpha Addon API Changes, 2025-11-24* |
| Readiness of a cooldown row | **readable** | R2 | alert-edge latch; `security-…` §4.8 |
| Affordability of a spender | **readable** | R1 | `C_Spell.IsSpellUsable` second return, no `SecretWhen*` predicate |
| Spell identity across an override | **readable** | R7 | `overrideSpellID` readable in combat on 21/21 rows (`cooldown-manager.md`); the three override paths this catalog uses are established from spell data, not observed in the client — see the roster section |
| Art of War / Righteous Cause proc | **readable** | R-new (below) | `SpellActivationOverlay` @ 12.1.0.69214 |
| Empyrean Power proc | **readable** | R-new | as above |
| Empyrean Legacy proc | **readable** | R-new | as above |
| AoE / single-target intent | **readable** | cap's own `/cap aoe` toggle | not a game read |
| Whether Radiant Glory is taken | **readable** | the `talent` predicate | node 81549 / entry 102525 (`ability-inventory.tsv`); ⚠ the `C_Traits` call shape is `[gap]` — Havoc's *Open facts* 7 |
| Avenging Wrath / Execution Sentence / Wake of Ashes **cooldown remaining** | **sealed-display** | S4 → `sealed-cooldown-range` | `C_Spell.GetSpellCooldown` is `SecretWhenCooldownsRestricted`; the duration object carries the secrecy |
| Free vs ordinary Hammer of Light | **open** | — | one overlay row for both; buff identity sealed |
| `buff.undisputed_ruling.remains`, `buff.avenging_wrath.remains`, `buff.hammer_of_light_free.remains` | **open** | — | aura *durations*; cap has no aura-duration range display and this pass does not prebuild one |
| `dot.expurgation.ticking` | **open** | — | a **target** aura; cap has no target-aura vocabulary |
| Target health / execute range | **not needed** | — | subsumed by the Hammer of Wrath override |
| Enemy count | **not modelled** | — | replaced by the toggle, as on Havoc |
| `raid_event.adds`, `fight_remains`, `target.time_to_die` | **not facts** | — | simulation state |

### The proc measurement, in full — it is what makes this catalog cheap

`../pattern-shelf.md` has no recipe for *"is this proc readable"*, and the honest answer is that
it is a question about **spell data**, not about the secrecy rules. Under 12.1's wholesale aura
secrecy a buff is sealed — but cap's `proc` predicate is
`C_SpellActivationOverlay.IsSpellOverlayed(spellID)` (`Sense.lua`'s `readProc`), a plain boolean
keyed on the **highlighted spell**, wholly independent of the aura API and measured readable in
combat (`knowledge/addon-dev/cooldown-manager.md`). Blizzard's own Cooldown Manager calls it the
same way (`CooldownViewerCooldownItemMixin:RefreshOverlayGlow` → `IsSpellOverlayed(self:GetSpellID())`)
*[T1 src @ 12.1.0]*.

Which spells glow is `SpellActivationOverlay.db2`: each row names a trigger aura and an
`IconHighlightSpellClassMask` matched against the highlighted spell's `SpellClassOptions` mask.
At **12.1.0.69214**, for Retribution *[T1 DB2]*:

| Trigger aura | Highlight mask | Matches | So `proc(x)` is true when |
| --- | --- | --- | --- |
| **Art of War** `406086` | mask₃ `1073741824` | Blade of Justice `184575` (mask₃ `1073741824`) | `proc(blade_of_justice)` |
| **Righteous Cause** `402916` | mask₃ `1073741824` | same | `proc(blade_of_justice)` |
| **Empyrean Power** `326733` | mask₁ `131072` | Divine Storm `53385` (mask₁ `131072`) | `proc(divine_storm)` |
| **Empyrean Legacy** `387178` | mask₂ `8192` | Templar's Verdict `85256` (mask₂ `8192`), Final Verdict `383328` (mask₂ `8194`) | `proc(templars_verdict)` |
| **Hammer of Light** `427441` | mask₀ `536870912` | Hammer of Light `427453` (mask₀ `671088640`) | — (not used; see below) |

Three consequences the design leans on:

1. **The OR is free.** Generators 5 is `(buff.art_of_war.up|buff.righteous_cause.up)`, and both
   auras drive the *same* highlight, so one `proc(blade_of_justice)` term is the whole disjunct.
   cap does not author the OR; the game data already did.
2. **`proc` names the button, not the buff**, which is why the same predicate reads a proc that
   makes a *different* button better — `proc(divine_storm)` is Empyrean Power's, and it is used
   to badge Templar's Verdict.
3. **Hammer of Light's overlay is useless to this catalog**, because there is exactly one row for
   it and it therefore cannot separate `buff.hammer_of_light_ready` from
   `buff.hammer_of_light_free`. The row's `identity` says everything the overlay would.

⚠ **One collision is unresolved.** Overlay rows `267345` (Divine Storm) and `267346` (Templar's
Verdict) carry the same highlight masks as Empyrean Power and Empyrean Legacy, and belong to an
older Divine Purpose. Modern **Divine Purpose 408459** *is* a Retribution class talent, and its
own overlay row `408458` highlights **nothing** (all four masks zero — it registers a screen
overlay only), so on the face of it there is no collision. But whether a Divine Purpose proc
raises `267345` / `267346` in the live client is not measured, and if it does, both spender procs
would read true together. The failure direction is a missed *skip*, not a wrong press
(`!proc(templars_verdict)` would suppress the AoE badge and the player would press the
single-target spender in AoE — mild, and only during a proc that makes either free anyway).
*Open facts* 4. **Divine Arbiter** and **Echoes of Wrath**, which carry the same masks, are
absent from Retribution's inventory entirely and are not a risk.

**No sealed fact appears in any proposed Lua condition, in either polarity.** The only sealed
facts this catalog uses are the five cooldown-remaining bands, and each goes straight to a
client-owned sink as an authored range curve.

---

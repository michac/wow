# Observability map — the 12 APL inputs vs. what the game actually lets us read

> **⚠ STATUS: reference-only** (like `input-contract.md`). `apl.lua` was retired; the
> readability facts below now describe what `State.lua` / `Coach.Context` can honestly
> feed the shipped Coach. `rotation.md` is the rotation spec of record.

This is the **readability pass**: for each of the 12 fields the priority list needs
(`input-contract.md`), where the value comes from in the observed client picture, how
reliably it reads **out of combat vs. in combat**, and how it degrades when the game
hides it. The list itself (`rotation.md`) is unchanged — this only says
*how honestly each input can be fed*.

## Sources of truth for this pass

- **What the client exposes** — the reduced-State pulse: per-cooldown `cd`
  (`state ∈ ready|on-cooldown|unknown`, `source ∈ live|napkin|none`, `remaining`),
  `glow` (the combat-readable spell-overlay proc signal), `aura`/`buff.isActive`
  (buff presence), `power.SoulShards.{value,incoming,max}`, cast `history`, the spell
  `override`/`liveSpellID` (transforms), and `mode` (st/aoe).
- **What's provably secret** — the tested-assumptions-of-record: **in-combat cooldown
  reads go secret** (readiness survives via an OOC baseline + observed alert edges);
  **the Wild-Imp count side-channel is closed** (`imp-side-channel-closed`); **Core
  stack count is not read** (auraData-derived → secret). Buff *presence* is readable;
  buff *counts/durations* are not.

## The readiness model (three fields lean on it — read this first)

Cooldown readiness is **observed, not guessed**. Out of combat every cd reads
precisely. In combat the live read goes secret, so "is it up?" is answered by, in order:

1. **an observed CDM alert edge** (`Available`/`OnCooldown`, fires in combat) → *ready
   is a real observation*;
2. **the OOC-readiness baseline** carried across combat entry → a never-cast summon
   that was up at the pull still reads ready;
3. **the napkin** (base-cooldown countdown from the last observed cast) → supplies the
   *remaining* estimate only; when it elapses the cd is "on-cooldown, remaining 0,
   **unconfirmed**" — probably-up, never a laundered `ready`.

So a usability field can be **observed-true** (edge/baseline) or **estimated-true**
(napkin elapsed). That distinction is the confidence the caller should carry into the
cue (a napkin-elapsed press is honest but soft).

## The map

| # | Field | Source in the pulse | OOC | In combat | Confidence | Degrades to |
|---|---|---|---|---|---|---|
| 1 | `shards` | `power.SoulShards.value + .incoming` (signed in-flight projection) | exact | **readable** (power survives combat) | **High** | value secret one pulse → treat as unknown; don't force a shard gate |
| 2 | `ruination_up` | `override`/`liveSpellID` on the HoG frame = the Ruination Art id (`spends=art`, no generate) | exact | **readable** (override event fires in combat) | **High** | no override seen → false |
| 3 | `dreadstalkers_usable` | `cd` on Call Dreadstalkers (readiness model above) | exact | edge/baseline **observed**, else napkin **estimate** | **Med–High** | no edge+no baseline+no napkin → `unknown` → false (won't press unconfirmed) |
| 4 | `tyrant_window` *(setup)* | Tyrant `cd`: ready/probably-up **OR** napkin `remaining ≤ ~3s` | exact | off-cd half observed; the **"~3s out" half is napkin-only** | **Med** | napkin absent → window only opens on the observed-ready edge (a beat late, never wrong) |
| 5 | `dreadstalkers_held` | **not a read** — engine memory: Dreadstalkers deferred by L2 while `tyrant_window`, not yet cast this window (derive from `history` + window) | n/a | n/a | **Derived** | if you can't tell, treat as not-held → it simply fires off-cd via L2 when the window isn't active |
| 6 | `core_present` | `glow` on Demonbolt (Core proc overlay) **or** Demonic Core `buff.isActive` | exact | **readable** (glow reads in combat; count does **not**) | **High (presence)** | neither readable → false. **Count is secret — never inferred** (validates OQ2) |
| 7 | `ib_usable` | `override`/`liveSpellID` on the Shadow Bolt frame = the Infernal Bolt Art id (`spends=art`, `generates=3`) | exact | override event *should* fire in combat | **Med — verify** | ⚠ documented v1 blind spot is about the *glow* (SB frame has no lit icon); confirm the **override event** itself fires for SB→IB, else false |
| 8 | `grimoire_usable` | `cd` on the talented Grimoire (readiness model) | exact | edge/baseline/napkin | **Med–High** | unknown → false (2-min CD; absent on off-Tyrant cycles is correct) |
| 9 | `tyrant_castable` *(off cd now)* | Tyrant `cd` ready/probably-up **only** (no ~3s lead) | exact | edge/baseline observed, else napkin | **Med–High** | unknown → false |
| 10 | `sb_usable` | no cd / no cost | true | true | **High** | only false if silenced/locked out |
| 11 | `hog_usable` | `shards ≥ cost` (cost live via `ns.ShardCost`, talent-dependent) + off GCD | exact | **readable** | **High** | cost unreadable → assume the fallback cost (3) |

## The three fields that need a decision or a check

- **`dreadstalkers_held` (#5) is engine state, not a game read.** Nothing in the pulse
  says "I'm holding this for Tyrant." The evaluator's *caller* must maintain it: set it
  when L2 defers Dreadstalkers because `tyrant_window` is true, clear it once
  Dreadstalkers is cast (visible in `history`) or the window closes. This is the
  reactive-hold judgment from clarification 2 — the one bit of memory the otherwise-pure
  list depends on. **Open item:** decide whether the module owns this memory (stateful
  wrapper) or the caller computes it each pulse from `history` + `tyrant_window`. The
  module today takes it as an input, which keeps the evaluator pure — I'd keep it there
  and compute the flag in the (stateful) State→input adapter.

- **`implosion_usable` (#6→L3) is cooldown-observable but its real gate is secret.**
  We can read "Implosion is off cd," but the imp-count that makes the press *correct*
  (`≥6 Wild Imps`) is **provably unreadable** (`imp-side-channel-closed`). Per your OQ1
  call the line still fires when off-cd, and the softening ("your call") lives in the
  contract, not the list. This map just confirms the *why*: the confidence gap is a hard
  capability limit, not a modeling choice.

- **`ib_usable` (#7) rides the transform-observability path — verify it.** Ruination
  (#2) is confirmed observable because the HoG→Ruination override fires and is mapped.
  Infernal Bolt is the *same mechanism* on the Shadow Bolt frame, but the documented v1
  blind spot ("SB→Infernal Bolt has no icon to light") was about the **glow**. The
  **override event** is a different signal and should still fire — but this is the one
  field I'd put an explicit in-game check against before trusting `ib_usable` in combat.

## What is simply not observable (and no field pretends to be)

- **Wild-Imp count** — the Implosion gate. Side-channel closed; asserted so we'd notice
  if Blizzard ever opened it.
- **Demonic Core stack count** — only presence is read; `core_present` is deliberately a
  boolean. No line depends on "2+ cores".

Both absences are load-bearing: they are exactly why L3 (Implosion) softens to a cue and
why the Core-dump (L5/L6) gates on presence only.

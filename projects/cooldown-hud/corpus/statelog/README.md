# statelog corpus — real captured State pulses (W4 Phase 1)

Real `/cdmp statelog` captures from CDMProbe **v0.29.5**, Demonology Warlock,
open-world dummy (build 12.0.7). Each file is a State pulse — the reduced,
spec-agnostic client picture the W4 pipeline's Stage 1 emits
(`docs/architecture.md`). These are the **independent corpus** the Phase-2 Coach
is tested against (build plan P2).

## Files
- `_raw-show-json.json` — the **verbatim** `wowkb.cdmp show --json` dump: the
  whole on-disk capture (`probe` + `pulls` + `statelog`), unmodified.
- `_full-ring.json` — all pulses in the statelog ring, lightly normalized
  (cooldowns keyed by cooldownID string; empty tables → `[]`).
- `pulse-NNN-<kind>.json` — hand-picked exemplars:
  - `ooc-baseline` — out of combat: every cd reads **live**; the full aura scan is
    readable (8 buffs).
  - `combat-proc` — a Demonic Core proc: **`buff.isActive` (Core) and `glow`
    (Demonbolt) both true**, while `aura.readable=false` (see the finding below).
  - `combat-transform` — a spell-override transform; `liveSpellID` diverges from base.
  - `combat-cast-napkin` — mid-pull: live cd reads go **secret** → cds fall to the
    **napkin** (`source:"napkin"`, `state:"anticipated"`).

## Reading a pulse
`at`/`combat`/`reason`/`seq` are the envelope. `cooldowns[cooldownID]` carries
structural metadata (`spellID` base, `liveSpellID` resolved, overrides,
`linkedSpellIDs`, `selfAura`/`hasAura`, `flags`, `category`, `isKnown`) plus live
facts, each **secrecy-first-class**:
- `cd{state,remaining,readable,source}` · `charge{cur,max,readable}`
- `aura{active,readable}` — C_UnitAuras; **OOC only** (see finding)
- `glow{active,readable}` — `IsSpellOverlayed`; **readable in combat**, lands on the
  empowered spell (Demonbolt glows when a Core proc is up)
- `buff{isActive,shown,hideWhenInactive}` — the CDM buff-tracking item's frame state;
  `isActive` is **readable in combat** and the canonical per-buff presence
- `keybind` — OOC-resolved off the base id

`power` is keyed by the real `Enum.PowerType` name; `activeAuras` is every readable
active player buff; `events` is the delta since the previous pulse.

## Key finding (measured, cross-validated — see `docs/architecture.md`)
**Combat-applied auras are Secret Values.** `C_UnitAuras` (both the scan and the
by-id read) is blind to combat procs, so `aura.readable=false` in combat — honest,
not a false `active:false`. The readable combat proc signals are **`buff.isActive`**
(direct on the buff entry) and **`glow`** (on the empowered spell); in this capture
they agreed on all 32 pulses. `IsActive()` is preferred over `IsShown()` (the latter
tracks the aura only when `hideWhenInactive` is set).

⚠ Not a rotation oracle. These say what the client reported, nothing about which
cue should light — that judgment is Phase 2's.

# ruination — rationale

**Situation:** combat; **Pit-Lord Demonic Art armed** (Diabolic Ritual tracker `9426`
`buff.isActive:true`), so the Hand of Gul'dan frame (`34991`) is **transformed into Ruination**
(`overrideSpellID = liveSpellID = 434635`) and **glows** (`glow.active:true`, readable). **4 soul
shards**; Demonic Core down; Tyrant / Dreadstalkers / Implosion cooling (napkin). Not inside a
Tyrant window (Tyrant frame `2742` is cooling, no active-window buff).

**Oracle (rotation source → expected Guidance):**
- The Diabolic Ritual cycle arms **Pit Lord's Art → the next Hand of Gul'dan becomes Ruination**, a
  **free triple-imp spend (0 shards)** (`diabolist-sequences.md` "The engine you must understand
  first: Diabolic Ritual"; proc taxonomy: HoG → Ruination is "same keybind, upgraded effect; the
  Demonic Art buff is the light-up"). The steady-state loop's **first rule** is *"if a Demonic Art
  is armed → press its button now"* (`diabolist-sequences.md` steady-state loop). Ruination is
  extremely high value, so it is the **#1 ready ability → the single `ROTATION` press** on
  cooldownID `34991`.
- **Tyrant-window preference is a nicety, not a gate.** The source says to *prefer* firing Ruination
  inside/entering the Tyrant window ("prefer to fire it inside/entering the Tyrant window; the
  parses cluster RUIN around Tyrant"). But Tyrant is on cooldown here and the Art is armed **now**;
  the armed-Art rule presses on availability. Holding an armed Art indefinitely risks it expiring —
  so on-cd, Ruination is still the press. `ROTATION`, not `SOON`.
- **Demonbolt (`1979`) does not draw** — Core is down (`777 buff.isActive:false`, no glow on the
  Demonbolt frame). Not a call. Unlisted.
- **Shadow Bolt (`34990`) is the filler** (`rotation.md` step 12) — outranked by an armed spender.
  Unlisted.
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin) — not ready, not close enough for
  `SOON`. Unlisted (`AVAILABLE`/internal).

**Readability (the crux):**
- The press rests entirely on **readable** signals: the **glow** on frame `34991`
  (`IsSpellOverlayed`, readable in combat) is the "press this now / this is Ruination" light, the
  Diabolic Ritual tracker's **`buff.isActive`** (`9426`, readable) confirms an Art is armed, and
  **shards** (`power.SoulShards.value = 4`, readable) confirm it is castable. None of these read a
  secret `cd` or `aura`.
- The **identity-coherence** of the transform is expressed in State, not decoded from a secret:
  `spellID` stays the base `105174` while `overrideSpellID` and `liveSpellID` both flip to
  `434635` (Ruination) — the frame *is* wearing the Ruination hat, and its glow is the readable
  edge that justifies the call.
- **No `transient`.** This is a **steady armed proc** (the Art is up), not the arming edge — same
  treatment as `demonbolt-proc` (a persistent proc is not a transient). The arming `proc` edge
  would be a separate scenario.

**Contract checks this exercises:**
- **Single-top-press holds** — exactly one cue is `ROTATION` (the transformed HoG/Ruination); every
  other ready ability caps at `AVAILABLE` (unlisted).
- **Transform / identity-coherence** — `overrideSpellID = liveSpellID = 434635` on `34991` with
  the base `spellID` retained; the golden pins the cue to the **cooldownID** (`34991`), stable
  across the transform.
- **Secrecy gate** — the drawn cue leans only on readable state (glow + ritual `buff.isActive` +
  shards); the secret `cd`/`aura` fields are never the source.
- **Pass-through string** — the `note` ("Ruination — free triple-imp (Pit Lord)") is Coach-authored
  display text, the sanctioned place for class vocabulary.

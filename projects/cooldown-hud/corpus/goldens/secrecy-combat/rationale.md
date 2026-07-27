# secrecy-combat — rationale

**Situation:** combat; the readability-discipline stress test. **Every** cooldown field is
`readable:false` — the near ones carry a napkin estimate (`source:"napkin"`), the instant/no-model
ones carry `source:"none"`. Shards are readable (**2**). Demonic Core is **up**. No Diabolic Art is
armed (cd 9426 `buff.isActive:false`). Tyrant's napkin says **~2 s out** (`state:"anticipated"`).

The point of this case: **nothing pressable is read from a cooldown.** Despite everything
cd-shaped being dark, every drawn cue still traces to a readable signal.

**Oracle (rotation source → expected Guidance):**
- **Demonbolt is the single `ROTATION` press.** With a Demonic Core available, the steady-state
  loop (`diabolist-sequences.md`: *"else if Demonic Core ≥ 2 → Demonbolt, else if Soul Shards ≥ 3
  → Hand of Gul'dan"*) puts the Core dump **above** Hand of Gul'dan. Here HoG is doubly out — it
  sits below Demonbolt in the loop **and** is uncastable at 2 shards (cost 3). Demonbolt wins
  cleanly → one `ROTATION`.
- **Summon Demonic Tyrant draws `SOON`.** It is the 60 s burst cooldown coming back up; the napkin
  estimates ~2 s remaining. `SOON` is anticipation, **not** a press — it coexists with the single
  `ROTATION` (like the resourceBar and `JUDGE`), so the single-top-press invariant is untouched.

**Losers demoted (unlisted = `AVAILABLE`, no cue):**
- **Hand of Gul'dan (34991)** — 2 shards < its 3-shard cost, so not castable; and it ranks below
  Demonbolt anyway. Unlisted.
- **Shadow Bolt (34990)** — the free builder, outranked by the Core consumer. Unlisted.
- **Call Dreadstalkers (671) / Implosion (149122)** — both cooling (napkin, `state:"cooling"`,
  remaining > 0). Not up, not a call. Unlisted. (Implosion is also nowhere near its ≥6-imp gate —
  no imp buff frame is even present — so no `JUDGE` arises.)
- **Ruination / Infernal Bolt** — not on the board: the Diabolic Ritual tracker (9426) is
  `isActive:false`, so **no Art is armed**. HoG stays HoG and Shadow Bolt stays Shadow Bolt
  (`liveSpellID == spellID` on both — identity coherence). Nothing to transform, nothing to draw.

**Readability (the crux):**
- **Demonbolt's `ROTATION` rests on `buff.isActive` (cd 777) + `glow` on Demonbolt (cd 1979)** —
  both `readable:true` in combat. The `aura` field is `readable:false` on **every** frame
  (C_UnitAuras is dark in combat) and is never the source. This inherits the `demonbolt-proc`
  **readable-approximation** caveat: the ideal gate is **≥2 Core stacks**, but the stack *count*
  is a Secret Value — so we assert the readable stand-in ("Core up + Demonbolt glows → press"),
  accepting it may occasionally be 1 stack.
- **Tyrant's `SOON` rests on the napkin-anticipated estimate**, not a readable live cooldown. This
  is the sanctioned anticipation signal — and it obeys **napkin honesty**: `state:"anticipated"`
  carries `remaining:2.0 > 0` and never claims `"ready"` (a napkin cd may never read ready; that
  is only ever a live read, which does not happen in combat). We surface "coming — not yet" and
  let the Renderer own the dim/countdown treatment; no secret number is put in a note.
- **No cue cites a secret.** Not one drawn cue leans on a `cd` value (all `readable:false`) or on
  an `aura` (all `readable:false`). Shards feed the resourceBar readably; the Core press is
  readable via buff+glow; Tyrant's SOON is the honest napkin projection.

**Contract invariants this exercises:**
- **Secrecy gate (the headline)** — with *every* cd dark, the case proves the Coach draws only
  from readable signals (shards / `buff.isActive` / `glow`) plus the sanctioned napkin anticipation.
- **Single-top-press** — exactly one cue is `ROTATION` (Demonbolt); `SOON` is a non-press signal
  that legitimately coexists.
- **Napkin honesty** — the one `anticipated` cd carries `remaining > 0` and is never "ready"; the
  `unknown`/`none` cds carry no `remaining`.
- **Identity coherence** — no Art armed, so `liveSpellID == spellID` on HoG and Shadow Bolt (no
  Ruination / Infernal Bolt transform).
- **Steady-state proc, not an edge** — the Core is already up, so Demonbolt carries **no**
  `transient` (a persistent proc is not an edge — same as `demonbolt-proc`).

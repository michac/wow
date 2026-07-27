# cast-ended-edge — rationale

**Situation:** combat, single-target; a **Shadow Bolt just landed** — `history` carries a
`succeeded` for spellID 686 with `at == pulse at (1000.0)` (its earlier `start` at 997.8 is now
resolved). The cast refunded +1 Soul Shard → **2 shards** in hand. No Demonic Core (777
`buff.isActive:false`, no glow on Demonbolt), Hand of Gul'dan **not castable** at 2 shards (needs
3), summons cooling (napkin), no Demonic Art armed.

**Why this golden exists:** it closes the **only uncovered transient member**. `transient-edges`
carries `cast_started` + `ready` + `proc`; `cast_ended` — "the cast landed (succeeded)" — had no
home. This is the readable landing edge.

**Oracle (rotation source → expected Guidance):**
- With no Core, no Art, and shards below HoG's cost, the readable play is to **keep building** —
  **Shadow Bolt is the filler press** (`rotation.md` step 12 / `diabolist-sequences.md` "SB when
  you have neither [shards nor a Core]"). So **Shadow Bolt is the single `ROTATION`.**
- **Hand of Gul'dan does NOT draw** — 2 shards < its 3-shard cost, not castable. Unlisted.
- **Demonbolt does NOT draw** — no Core up (`buff.isActive:false`), nothing to spend. Unlisted.
- No summon is up (napkin cooling), no Art armed → nothing else competes.

**The transient (the point of the case):**
- Shadow Bolt's cue carries **`transient:"cast_ended"`** — the edge fires on the **transition into**
  "landed," read from the `history` `succeeded` entry whose `at` equals this pulse's `at`. The
  Renderer edge-detects it (a brief landing flash), does not re-fire while it persists, and clears
  to null next pulse. Since the same Shadow Bolt is immediately the next filler press, the cue is
  both the `ROTATION` press **and** the `cast_ended` flash this pulse — a legal pairing (emphasis
  and transient are orthogonal channels).

**Readability / contract checks:**
- **Readable-only:** the press rests on readable shards (2, below cost → build) + the readable
  `history` landing edge. No secret cd or aura is read; all `cd` entries are `readable:false`
  (secret in combat → napkin/none), every `aura` is `readable:false`.
- **Napkin honesty:** Tyrant/Dreadstalkers are `source:"napkin"` `state:"cooling"` with
  `remaining>0`; no napkin claims `"ready"`.
- **Single-top-press:** exactly one drawn cue, `ROTATION`.

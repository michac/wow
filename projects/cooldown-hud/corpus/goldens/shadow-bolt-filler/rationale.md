# shadow-bolt-filler — rationale

**Situation:** combat; **1 soul shard**; no Demonic Core proc (777 `buff.isActive:false`, 1979
`glow:false`); no Demonic Art armed (9426 `buff.isActive:false`); Tyrant / Dreadstalkers /
Implosion cooling (napkin); Hand of Gul'dan has no cooldown but is **unaffordable** (costs 3
shards, you hold 1). This is the "empty buckets" case — nothing is lit, so the rotation falls
through to its floor.

**Oracle (rotation source → expected Guidance):**
- **Shadow Bolt** is the **filler / free builder** (`rotation.md` step 12: "Shadow Bolt filler …
  to rebuild shards"; `diabolist-sequences.md` steady-state loop: *"else → Shadow Bolt (build)"*).
  The conditional loop is checked top-down and every higher branch fails here — no armed Art, no
  Implosion (ST + cooling), no Demonbolt (no Core), no Hand of Gul'dan (<3 shards) — so the `else`
  fires. **Shadow Bolt is the #1 ready ability → the single `ROTATION` press.**
- **Hand of Gul'dan** is the primary spender (`rotation.md` step 9) but is gated at **3 Soul
  Shards**; with only 1 shard readable it is not castable. Demoted → `AVAILABLE`, unlisted.
- **Demonbolt** is the Demonic-Core spender (`rotation.md` step 11) and is `reactive` on a Core
  proc. The Core buff is down (777 `isActive:false`, and 1979 carries no `glow`), so it is not a
  call. Unlisted.
- **Infernal Bolt / Ruination** are the transformed Shadow Bolt / HoG that appear only when the
  matching Diabolic Art is armed (`diabolist-sequences.md`). 9426 reads `isActive:false` → no Art
  armed → neither transform is live. State keeps `34990.liveSpellID == 686` and
  `34991.liveSpellID == 105174` (no transform, identity-coherent). Unlisted.
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin estimates, `remaining > 0`) — not
  ready, and not close enough to warrant `SOON`. Unlisted.

**Readability:** every `cd` read is `readable:false` (combat secret). The summons' cooling is the
**napkin** (`source:"napkin"`, `state:"cooling"` with a live `remaining`). Shadow Bolt, HoG, and
Demonbolt are instant/no-cd (`source:"none"`, `state:"unknown"`), so their availability is decided
by **readable** signals only: shard count (`power.SoulShards.value = 1`, readable) rules HoG out;
the readable **`buff.isActive`** on 777 (Core) and 9426 (Ritual) plus 1979's readable `glow` rule
out Demonbolt and the Art transforms. So the `ROTATION` call on Shadow Bolt — "nothing affordable
above the floor, build shards" — rests entirely on readable state. `aura` is `readable:false`
throughout and is never consulted.

**Contract invariants exercised:**
- **Single-top-press:** exactly one drawn cue holds a press emphasis — `34990` = `ROTATION`. No
  `LATE` (Shadow Bolt is the current play, not overdue); every other ability caps at `AVAILABLE`
  (unlisted).
- **List-only-drawn-cues:** `cues` names just the one press; the seven demoted / cooling / proc-
  down abilities are absent (= `draw:false` / `AVAILABLE`).
- **Readable-only justification:** the winner traces to shards + buff/glow, never to a secret `cd`
  or `aura`.
- **No transient:** Shadow Bolt is steady-state filler, not a phase edge (the prior Shadow Bolt in
  `history` already `succeeded`); no `cast_started`/`ready`/`proc` edge applies, so `transient` is
  omitted.
- **Identity coherence:** with no Art armed, both transform-capable frames keep
  `overrideSpellID == liveSpellID == spellID`.

# infernal-bolt — rationale

**Situation:** combat; **1 soul shard** (shard-starved, <3); the **Mother of Chaos** Demonic Art
is armed, so the **Shadow Bolt frame is transformed to Infernal Bolt** (cd 34990:
`overrideSpellID = liveSpellID = 434506`, frame **glows**); a **Demonic Core is also up** (cd 777
`buff.isActive`, Demonbolt cd 1979 glows); Tyrant / Dreadstalkers / Implosion cooling.

This is the mirror of the Ruination transform, but on the **Shadow-Bolt** frame instead of the
Hand-of-Gul'dan frame.

**Oracle (rotation source → expected Guidance):**
- The Diabolic-Ritual wheel is deterministic Overlord → Mother of Chaos → Pit Lord
  (`diabolist-sequences.md`). When **Mother of Chaos's Art is armed, the next Shadow Bolt becomes
  Infernal Bolt (+3 shards)** — "same keybind, upgraded effect." The steady-state loop's **top
  branch is "if a Demonic Art is armed → press its button now."** So the transformed frame is the
  #1 call, above the Demonbolt/HoG/Shadow-Bolt branches → **single `ROTATION` on 34990.**
- **Shard-starved seals it.** Both authorities converge: `rotation.md` step 10 — *"Infernal Bolt
  if <3 Soul Shards — the shard-refill builder"*; `diabolist-sequences.md` — *"fire it when
  shard-starved (it's your best builder)."* Infernal Bolt is a **3-shard builder self-gated to <3
  shards**; at 1 shard it is both castable and the best refill. (At high shards the +3 would
  overcap and you'd spend first — but that is not this fixture.)
- **Demonbolt does NOT draw** — even though a Core is genuinely up and Demonbolt is castable
  (it costs no shards). The priority puts the armed Art (top loop branch) and Infernal Bolt
  (`rotation.md` step 10) **above** Demonbolt (step 11). This is the case's point: a **live,
  readable competitor demoted by rank**, not excluded by castability. Unlisted → `AVAILABLE`.
- **Hand of Gul'dan does NOT draw** — a 3-shard spender at **1 shard is not castable**. Unlisted.
- **Shadow Bolt** as a plain builder is exactly the frame that got transformed; there is no
  separate plain-SB press. The single winner is the transformed frame.
- No `SEQUENCE` (no opener/burst pane active), no `SOON`/`JUDGE` (Implosion cooling; no
  anticipation edge to surface).

**Readability (the crux):**
- The `ROTATION` traces entirely to **readable** signals: shards `value = 1` (readable, <3 → the
  builder is the call), **cd 9426 `buff.isActive = true`** (the Diabolic-Ritual / Art tracker,
  readable in combat), and **cd 34990 `glow.active = true`** (IsSpellOverlayed on the empowered
  Infernal-Bolt frame — the "press this now" light). No secret `cd` and no `aura` is consulted
  (`aura.readable:false` throughout; C_UnitAuras is dark in combat).
- The **transform itself is readable**: the frame carries `overrideSpellID = liveSpellID = 434506`
  and glows — that is how "Shadow Bolt is now Infernal Bolt" shows without reading a hidden aura.
- Demonbolt's demotion is honest: its Core is readable (777 `buff.isActive` + 1979 glow), so the
  Coach *can* see the competitor and still ranks it below the armed Art — a priority decision, not
  a false instruction.
- **Steady-state Art, not the arming edge** → **no `transient`** (per `demonbolt-proc`: a
  persistent proc is not a transient; the arming edge is a separate scenario).

**Contract invariants exercised:**
- **Single top press** — exactly one `ROTATION`/`LATE` (34990); a readable, castable Demonbolt is
  capped at `AVAILABLE` (unlisted) rather than lit as a second press.
- **Identity coherence under transform** — `spellID` stays 686 while
  `overrideSpellID = overrideTooltipSpellID = liveSpellID = 434506` (the Infernal-Bolt target).
- **Readable-only justification** — every drawn cue traces to shards / `buff.isActive` / `glow`,
  never a secret `cd` or `aura`.
- **`incoming = 0`** — nothing in flight (`history` carries only `succeeded` casts), so projected
  shards = value = 1; the ranking rests on the current shard read, not a projection.

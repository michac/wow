# hog-overcap-late — rationale

**Situation:** combat; **Soul Shards at 5/5 (cap)**; the last two builders (Shadow Bolt) landed
at t=993.4 and t=997.0 with **no spender since** — so you have been sitting at cap for ~3 s. No
Demonic Core proc. Tyrant / Dreadstalkers / Implosion cooling (napkin).

**The readable gate:** shards are always readable (`power.SoulShards.value = 5`). Two consecutive
`succeeded` builder events in `history` and **no HoG/spender `succeeded` after them** means the
economy has been parked at the cap. Every builder tick from here (and Inner Demons / pet-fed
shard gen) is now **wasted generation** — the textbook overcap loss.

**Oracle (rotation source → expected Guidance):**
- Hand of Gul'dan is the **shard spender** the whole rotation is built to dump into
  (`diabolist-sequences.md`: *"Hand of Gul'dan dumps Soul Shards … bucket filling up → press its
  spender"*; steady-state loop `Soul Shards ≥ 3 (never overcap) → Hand of Gul'dan`). At 5 shards
  it is the #1 ready ability.
- Because the shards are not merely available but have been **capped ~3 s** (readable evidence:
  value at max, no spend in history), this is not a fresh `ROTATION` press — it is **overdue**.
  Per the contract, `LATE` = *"you have been sitting on it."* So **HoG draws `LATE`**, the single
  top press.
- **`LATE` here is fully justified**, unlike a secret-cd `LATE`: the overdue-ness rests entirely on
  the **readable** shard count sitting at cap, not on a napkin-estimated cooldown we can't see. This
  is the readable overcap, the exact case the emphasis is for.

**Why each loser is demoted (AVAILABLE, unlisted):**
- **Shadow Bolt (34990)** — the free builder/filler. At 5 shards it would *overcap*, the opposite
  of what you want; it is only the press when shard-starved. Not a call. Unlisted.
- **Demonbolt (1979)** — the Demonic-Core spender. Core is **down** (`777` `buff.isActive:false`,
  `glow:false`), so there is nothing to spend. Not a call. Unlisted.
- **Tyrant (2742) / Dreadstalkers (671) / Implosion (149122)** — all cooling on the napkin, not
  ready, and not close enough for `SOON`. Unlisted.

**Readability caveat — the Demonbolt-overcap LATE we deliberately do NOT assert:** Demo has a
*second* overcap bucket — **Demonic Cores** (cap 4; `diabolist-sequences.md`: they overflow on
their own, ~131/fight). A symmetric "cores at cap → Demonbolt LATE" call would be the same shape as
this one — but the **Core STACK count is a Secret Value**. In combat we can read that a Core is up
(`buff.isActive`) or lit (`glow`), but **not how many** — so we can never know a Core bucket is
*capped* and thus can never justify a Demonbolt overcap `LATE`. That is a documented readability
limit. The **shard** bucket is the readable one (`power.value` gives the exact count against a known
max), so the shard-cap dump is the only overcap-`LATE` this HUD can honestly instruct.

**Contract invariants exercised:**
- **`LATE` vs `ROTATION` distinction** — same press, escalated to overdue on readable
  cap-plus-elapsed evidence (contrast `hand-of-guldan`, where HoG is a fresh `ROTATION` at 3 shards).
- **Single-top-press** — exactly one drawn cue holds `ROTATION`/`LATE` (here the lone `LATE`); every
  other ready ability caps at `AVAILABLE` (unlisted).
- **Readable-only justification** — the drawn cue traces to `power.SoulShards.value = 5` + the
  `history` spend-gap; no secret `cd` or `aura` is read.
- **Secret-gated softening** — the parallel Demonic-Core overcap call is *withheld*, not falsely
  asserted, because its gate (Core stack count) is secret.

# overcap-soften — rationale

**Situation:** combat; **4 soul shards**; **Demonic Core up** (`buff.isActive:true` on cd 777 +
`glow.active:true` on Demonbolt cd 1979 — both readable in combat); no Demonic Art armed (Shadow
Bolt / HoG frames sit at identity `liveSpellID`, glows off); Tyrant / Dreadstalkers / Implosion
cooling (napkin). No cast in flight (`history` carries only `succeeded` entries) → `incoming:0`.

This is the two-buckets-both-loaded moment: **shards near cap AND a Core banked.** Both spenders
are affordable and instant, so the Coach must *rank*, not light both.

## Oracle (rotation source → expected Guidance)

- **Hand of Gul'dan is the single `ROTATION` press.** At 4 shards the shard bucket is one builder
  away from overcapping. `rotation.md` step 9 spends shards with HoG "at ≥3 Soul Shards … or at 5
  to avoid overcapping," and the whole spec is framed as **"don't overcap"** — the buckets you keep
  from overflowing (`diabolist-sequences.md` TL;DR). Dumping HoG now (3 shards → back to 1) makes
  room; sitting on 4 while you do anything else risks a wasted shard.
- **Demonbolt does NOT draw — it demotes to `AVAILABLE` (unlisted).** The Core is real and the
  glow says "you *may* press this" (it's a fine instant cast), but the rotation source **gates
  Demonbolt to `<4` shards** (`rotation.md` step 11: "Demonbolt with a Demonic Core proc **and <4
  shards** … spend cores so they don't overcap"). At exactly 4 shards that gate is *not* met, so
  Demonbolt is not the call this GCD — the shard bucket is the more urgent overflow. Cores cap at 4
  and overflow slowly (`diabolist-sequences.md`: "Cores barely need managing … you're never
  starved"), so holding one Core for a GCD costs nothing, whereas an overcapped shard is a flat
  loss now. Demonbolt is outranked, and single-top-press caps every non-winner at `AVAILABLE`.
  **This is the soften:** we do not falsely green Demonbolt, and — because the only non-press tokens
  that may coexist (SOON / JUDGE / SEQUENCE) don't fit an *outranked-but-pressable* spender — the
  contract-legal expression is to **leave it unlisted** and let HoG's `ROTATION` + the `4/5`
  resourceBar carry the "spend shards first" story. (A JUDGE cue would misclassify it: JUDGE is a
  *secret-gated* your-call like Implosion's imp count; Demonbolt here is plainly pressable and
  simply loses the rank, which is exactly `AVAILABLE`.)
- **Shadow Bolt / Infernal Bolt — the builders — are excluded, and this is IB's self-gate home.**
  Shadow Bolt (34990) sits at identity (`liveSpellID:686`, no Mother-of-Chaos Art), so it's the
  plain filler; pressing it at 4 shards would build the 5th and then overcap on the next tick —
  wrong. Its transformed form, **Infernal Bolt** (a 3-shard *builder*), **self-gates to `<3`
  shards** — at 4 shards IB would not (and should not) be offered even were the Art armed, because
  it would blow you past the cap. So neither the builder nor its empowered form competes here;
  the only cap-relieving press is the *spender*, HoG.
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin) — not ready, not close enough for
  `SOON`. Unlisted. No opener/burst pane, so `sequence.show:false`.

## Readability (the crux)

- **The winner rests entirely on readable state.** HoG has no cooldown (`cd.state:"unknown",
  source:"none"` — instant); its gate is **shards**, and `power.SoulShards.value:4` is
  `readable:true`. The overcap ranking is arithmetic on that readable value — no secret is touched.
- **Core presence is read from `buff.isActive` (777) + `glow` on Demonbolt (1979)** — both
  `readable:true` in combat. The `aura` field is `readable:false` (C_UnitAuras dark in combat) and
  is never the proc source.
- **The secret we soften around:** the ideal Demonbolt gate involves the **Core *stack* count**
  (≥2 preferred), which is a Secret Value — unreadable. But that secret doesn't *promote* Demonbolt
  here; the **readable** shard count already demotes it. So the golden never needs the hidden count:
  a readable fact (4 shards) settles the rank, and the softened Demonbolt is simply held.

## Contract invariants exercised

- **Single-top-press** — exactly one cue is `ROTATION` (HoG); a second genuinely-affordable spender
  (Demonbolt) is held at `AVAILABLE`/unlisted rather than co-lit. This is the *positive* soften case
  (both spenders pressable, one wins), complementing `demonbolt-proc` (Core up, 0 shards → Demonbolt
  wins) — same two abilities, opposite ranking, decided by the readable shard count.
- **Secrecy gate** — no drawn cue leans on a `readable:false` fact; the ranking is driven by the
  readable shard value and the readable Core proc, never the secret Core stack count.
- **`incoming` honesty** — no in-flight cast, so `incoming:0`; the `4/5` bar shows the true readable
  shards that justify the dump (contrast `incoming-overcap`, where a projected 5 drives the same
  HoG press off an in-flight builder).

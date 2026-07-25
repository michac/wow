# incoming-overcap — rationale

**Situation:** combat; **4 soul shards**; a **Shadow Bolt is in flight** (cast committed —
`history` carries its `start` with no `succeeded` yet); no Demonic Core; summons cooling.

**The projection:** Shadow Bolt generates +1 shard on completion, so State's napkin sets
`power.soulShards.incoming = 1` → **projected shards = value + incoming = 5** (the cap).

**Oracle (rotation source → expected Guidance):**
- The Coach **ranks on the projection, not the raw value.** At a projected 5, starting *another*
  builder would overcap the moment the in-flight Shadow Bolt lands — wasted generation
  (`rotation.md`: spend at/near cap, don't overcap; the old HudScore overcap guard, same rule).
- So **Hand of Gul'dan is the press** — spend now to make room before the incoming shard caps you.
  `HoG: ROTATION`.
- **Shadow Bolt is not re-queued** (it's already in flight, and a second builder overcaps).
- `incoming:1` is **forwarded to `resourceBar`** so the bar shows the pending shard.

**What this exercises:**
- **State carries `incoming`** (the projection from an in-flight cast) — the field the old W4
  State contract was missing.
- **The Coach respects projected shards** — the ranking changes *because* of `incoming` (without
  it, at 4 shards a builder looks fine; with it, HoG wins). This is the decision-level test, not
  just a display test.
- **Readability:** the shard `value` is readable; `incoming` is a napkin projection off the
  readable in-flight cast (`history`) + the builder's mechanical yield. No secret is read.

# resource-states — rationale

**Situation:** combat; **0 soul shards**; a **Shadow Bolt is in flight** (`history` carries its
`start` for spell 686 with no `succeeded` yet); no Demonic Core proc (`777` `buff.isActive:false`);
no Demonic Art armed (`9426` `buff.isActive:false`); Tyrant / Dreadstalkers / Implosion cooling
(napkin). This is a **resourceBar / `incoming`-channel** fixture: an empty-but-filling meter.

**The projection:** Shadow Bolt generates +1 shard on completion, so State's napkin sets
`power.SoulShards.incoming = 1` → **projected shards = value + incoming = 0 + 1 = 1**. The bar
still reads `value:0` (nothing banked yet) with a pending `+1`.

**Oracle (rotation source → expected Guidance):**
- With **0 shards**, no spender is affordable. **Hand of Gul'dan** costs 3 shards (`rotation.md`
  step 9 / `diabolist-sequences.md`: "Soul Shards ≥ 3 → Hand of Gul'dan"), so it is **not a call**
  at 0 — unlisted. **Demonbolt** needs a Demonic Core (`rotation.md` step 11), which is down
  (`buff.isActive:false`, `glow:false`) — unlisted.
- **Shadow Bolt is the free builder / filler** you press when you have neither shards nor a Core
  (`rotation.md` step 12; `diabolist-sequences.md` steady-state loop: "else → Shadow Bolt (build)",
  and the `SB SB` refill runs "whenever shards/Cores desync"). From empty, rebuilding shards is the
  whole job → **Shadow Bolt is the #1 ready ability, the single `ROTATION` press.**
- Shadow Bolt is already in flight, but it stays the lit press: after this cast lands you are at 1
  shard, still short of a spender, so the next press is another Shadow Bolt — exactly the starved
  `SB SB` refill run. (No transform: no Mother-of-Chaos Art is armed, so Shadow Bolt is **not**
  Infernal Bolt here — `liveSpellID == spellID == 686`, identity-coherent.)
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin) — not ready, not close enough for
  `SOON`. Unlisted.

**What this exercises (primarily a resourceBar/incoming test):**
- **The `incoming` channel end to end.** State's napkin projects `incoming:1` off the readable
  in-flight cast (`history` `start` for 686) + Shadow Bolt's mechanical +1 yield; the Coach
  **forwards `incoming:1` to `resourceBar`** so the meter shows the empty-but-filling state.
- **A new shard `value` for corpus coverage: 0** (hand-of-guldan=3, incoming-overcap=4,
  demonbolt-proc=0-with-a-Core-press). Here 0 shards with **no** Core makes the builder — not a
  spender — the press, the opposite decision from incoming-overcap (4→cap → spend).
- **Discrete meter.** `display:"discrete"` — Soul Shards render as whole segments (0 of 5 lit,
  one pending), not a continuous fill.

**Readability:** Soul Shards are **always readable** (`power.SoulShards.value`) — never a combat
secret, unlike `cd`/`aura`. The `ROTATION` call rests entirely on readable state: shards = 0
(readable) rules out HoG, Core absent (`buff.isActive`, readable) rules out Demonbolt, so the
readable filler wins. `incoming` is a napkin projection off the readable in-flight cast, not a
secret read. Single-top-press holds: exactly one `ROTATION` cue; every other ability is `AVAILABLE`
(unlisted).

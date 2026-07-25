# demonbolt-proc — rationale

**Situation:** combat; Demonic Core **up**; 0 soul shards; no Art transform on the Shadow Bolt
frame; Tyrant/Dreadstalkers/Implosion cooling.

**Oracle (rotation source → expected Guidance):**
- With a Demonic Core available, **Demonbolt is the empowered press** (`rotation.md`: consume
  Core with Demonbolt; `SpecDemonology` `spends="core"`, `cadence="reactive"`). It outranks the
  filler → **single `ROTATION`.**
- **Hand of Gul'dan does NOT draw** — at **0 shards it is not castable** (spender, needs shards).
  This is the reviewer's correction: HoG is not a competitor here. Unlisted.
- **Shadow Bolt** filler is outranked by the Core consumer. Unlisted.
- No `SEQUENCE`, no burst pane.

**Readability (the crux):**
- Core presence is read from **`buff.isActive` (cd 777) + `glow` on Demonbolt (cd 1979)** — both
  `readable:true` in combat. The `aura` field is `readable:false` (C_UnitAuras is dark in combat)
  and is **not** the source.
- The *ideal* rotation gate is **≥2 Core stacks**, but the stack **count is a Secret Value** —
  unreadable. So the golden asserts the **readable approximation**: "Core up + Demonbolt glows →
  press," accepting it may occasionally be 1 stack when ideal is ≥2 (the inform-where-secret
  rule). This is the readability filter in action.
- Steady-state proc (not the arming edge) → **no `transient`**. The `proc` edge is a separate
  scenario (`transient-edges`).

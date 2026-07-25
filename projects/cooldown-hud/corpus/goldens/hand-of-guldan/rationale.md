# hand-of-guldan — rationale

**Situation:** combat; 3 soul shards; no Demonic Core proc; Tyrant/Dreadstalkers/Implosion on
cooldown (napkin-estimated); Shadow Bolt available (filler).

**Oracle (rotation source → expected Guidance):**
- Hand of Gul'dan is the **primary spender** the shard economy points at (`rotation.md` step 9:
  spend shards with HoG; `SpecDemonology` `primary=true`). With 3 shards banked and no higher
  call up, **HoG is the #1 ready ability → the single `ROTATION` press.**
- **Shadow Bolt** is `filler` (`rotation.md` step 12) — it is the press *only when nothing else
  is affordable*. HoG is affordable, so Shadow Bolt does **not** draw (`AVAILABLE`, unlisted).
- **Demonbolt** is `reactive` — it needs a Demonic Core, which is down here (`buff.isActive:false`,
  `glow:false`), so it is not a call. Unlisted.
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin) — not ready, not close enough for
  `SOON`. Unlisted.

**Readability:** all `cd` reads are `readable:false` (combat secret); the summons' cooling is
supplied by the **napkin** (`source:"napkin"`). HoG's readiness is **not** a cd read — it has no
cooldown; the gate is **shards**, which are readable (`power.soulShards`). So the `ROTATION` call
rests entirely on readable state. Single-top-press holds: exactly one `ROTATION` cue.

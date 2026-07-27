# in-tyrant-window — rationale

**Situation:** combat; **Summon Demonic Tyrant window ACTIVE**; Wild Imps out; **Demonic Core up**
(Demonbolt glowing); **4 soul shards**; Dreadstalkers / Implosion cooling (napkin). This is the
single most valuable DPS window of the rotation.

**Oracle (rotation source → expected Guidance):**
- Inside the Tyrant window the priority is **Hand of Gul'dan spam**. `diabolist-sequences.md`
  SEQUENCE 3 ("Inside the Tyrant window"): **`HoG HoG` opens the window** (flood Wild Imps while
  Tyrant empowers them), and maxroll's only window instruction is *"cast as many Hand of Gul'dan
  as possible for 15 s"* (Dominion of Argus refunds a shard per cast to sustain the spam — why
  4 shards persists mid-window). HoG needs 3 shards; we have **4 → castable**. So **HoG is the
  #1 ready ability → the single `ROTATION` press.**
- **Demonbolt does NOT draw**, even though it **glows** (Core up, readable). SEQUENCE 3 is explicit:
  *"HoG-priority spam with **DB dumping Cores between casts**."* Demonbolt is the fill you slot
  *between* HoGs to keep Cores from overcapping — a real press, but **not the top press** while a
  HoG is affordable inside the window. Under single-top-press it caps at `AVAILABLE` (unlisted).
  This is the deliberate contrast to the `demonbolt-proc` golden: there a glowing Core *was* the
  `ROTATION` winner (0 shards, HoG uncastable); **here HoG outranks the glow** because we can
  afford it and the window rewards HoG above all. A readable proc glow does **not** force a draw —
  ranking does.
- **Shadow Bolt** (filler) is outranked by both. Unlisted.
- **Tyrant (2742)** is on cooldown — it was just cast to *open* this window (`history` shows the
  265187 succeed at t=990, and its own cd is cooling on the napkin). It is not a press; it is the
  *reason* HoG is the press. Unlisted.
- **Dreadstalkers / Implosion** are cooling (napkin) — not ready. Implosion additionally would be
  wrong here even if up: in ST you keep imps alive to be empowered by Tyrant, never Implode them
  mid-window. Unlisted.

**Readability (the crux):**
- **Window-active is READABLE** — `2742` frame `buff.isActive:true` (the Tyrant-window TrackedBuff
  read), `readable:true`. The oracle's "we are inside Tyrant" premise rests on this readable buff,
  **not** on any secret cd.
- **Shards are READABLE** (`power.SoulShards.value:4`) — HoG's affordability gate is fully known.
- **Core presence is READABLE** — `777 buff.isActive:true` + `1979 glow.active:true`. We *know*
  Demonbolt is empowered; we simply **rank it below HoG** for this window. The `aura` field is
  `readable:false` (C_UnitAuras dark in combat) and is not the source, per the readable-combat
  model.
- **Secret-Value softening:** the Wild Imp **count** (143038) is secret — `buff.isActive:true`
  tells us imps are *out* but not *how many*. The oracle never leans on the count; the HoG call
  needs only "window active + shards ≥ 3," both readable. (No JUDGE for Implosion because its cd
  reads cooling on the napkin — not available — so there is nothing to defer to the player.)
- **No transient:** HoG-as-the-press is steady-state window spam, not a phase edge; the Core and
  the window are persistent, not arming this pulse (persistent proc ≠ transient, per
  `demonbolt-proc`). `transient` omitted.

**Contract checks this exercises:**
- **Single-top-press** — exactly one cue is `ROTATION` (HoG); the glowing Demonbolt is demoted to
  `AVAILABLE`/unlisted rather than lit as a second press.
- **Ranking beats raw proc-glow** — a readable "press me" glow is *not* auto-promoted; the rotation
  source's window priority (HoG > DB inside Tyrant) wins. This is the inverse of `demonbolt-proc`.
- **Secrecy gate** — no drawn cue traces to a secret cd/aura/count; HoG's `ROTATION` rests on the
  readable window buff + readable shards.
- **Pass-through string** — `cue.note` is Coach-authored display text (sanctioned).
- **incoming projection** — all `history` entries are `succeeded` (nothing in flight) → `incoming:0`;
  projected shards = 4.

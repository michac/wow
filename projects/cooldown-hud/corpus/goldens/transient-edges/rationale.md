# transient-edges — rationale

**Situation:** combat, AoE; **4 soul shards**; a **Hand of Gul'dan cast just committed** (in
flight — `history` carries its `start` for `105174` with no `succeeded`); a **Demonic Core proc
just lit this pulse**; **Implosion's cooldown just came up this pulse** (napkin flipped to
probably-up); Wild Imps out (count secret); Tyrant/Dreadstalkers cooling. This is the
**transient-channel coverage** golden: three distinct readable EDGES co-occur on one pulse, each
attached to the cue it belongs to, without breaking single-top-press.

## The three edges and why each draws where it does

### `34991` Hand of Gul'dan — **ROTATION + cast_started**
- HoG is the **primary spender** the shard economy points at (`rotation.md` step 9: spend shards
  with HoG at ≥3; don't overcap). At **4 shards** with nothing higher cleanly instructable, HoG is
  the **#1 readable press → the single `ROTATION`.**
- The **`cast_started`** edge fires because a HoG cast **committed this pulse**: `history` has
  `{ "phase":"start", "spellID":105174, "at":999.5 }` with **no matching `succeeded`** — the cast
  is in flight. The edge fires on the *commit transition*; it does not re-fire while the spell
  resolves. This is the contract's headline transient shape (cf. the contract example's
  `emphasis:LATE, transient:cast_started` — here `ROTATION` because the press is on-time, not
  overdue). The press and its just-fired edge legitimately share one cue.
- **`incoming:0`** on the bar (neutralized at 6a). Under 5b's **builder-only** incoming, an
  in-flight HoG (a *spender*) contributes no projection — signed negative incoming is 6d's work.
  This keeps the golden a pure transient-channel probe: with `incoming:0` the projected-shards gate
  (6b) still sees `4 >= cost`, so HoG stays the `ROTATION` press and the `cast_started` coverage is
  preserved. The negative-incoming / casting-display case returns properly in 6d.

### `1979` Demonbolt — **JUDGE + proc**
- A **Demonic Core** is up (`cd 777 buff.isActive:true`) and Demonbolt **glows**
  (`cd 1979 glow.active:true`) — both **readable** in combat.
- The **`proc`** edge fires because the glow **turned true THIS pulse**: `glow.changedAt == at`
  (`1000.0`). This is the **arming edge**, deliberately distinct from `demonbolt-proc`, whose glow
  is `active:true` with **no `changedAt`** (steady-state, no transient). The `changedAt == at`
  marker is how the State says "this lit *now*."
- **Why `JUDGE`, not `ROTATION`:** unlike `demonbolt-proc` (0 shards → HoG not castable → Demonbolt
  is the uncontested press), here **HoG is a live competitor** (4 shards). Whether Demonbolt
  *outranks* HoG depends on the **Demonic Core stack count** (`rotation.md`: `Core ≥2 → Demonbolt`,
  else `shards ≥3 → HoG`) — and the **stack count is a Secret Value** (unreadable in combat; only
  Core *presence* reads via `buff.isActive`). So we **inform, don't instruct**: HoG takes the
  readable `ROTATION`; Demonbolt draws `JUDGE` ("dump if 2+") — a your-call whose gate is secret.
  This is the same secrecy softening as `demonbolt-proc`, but the readable-competitor context
  demotes it from `ROTATION` to `JUDGE`.

### `149122` Implosion — **JUDGE + ready**
- Implosion's real gate is **≥6 Wild Imps** (`rotation.md` step 7), and the imp **count is a Secret
  Value**. Imps are present (`cd 143038 buff.isActive:true`) but the count is unreadable, so —
  exactly as in the `implosion` golden — it draws **`JUDGE`**, never an auto-green.
- The **`ready`** edge fires because Implosion's **cooldown just came up this pulse**: its `cd` is
  `state:"unknown", source:"napkin", changedAt:1000.0` — the napkin estimate ran out and flipped to
  **probably-up on this pulse** (`changedAt == at`). Per the napkin honesty rule, an elapsed napkin
  reads `unknown` with **no `remaining`** and is **never** `"ready"` as a *state* (that word is a
  live read that combat never gives) — but the *edge* `transient:"ready"` legitimately marks the
  just-came-up transition. `mode:"aoe"` is what puts Implosion on the table at all
  (`rotation.md`: Implode only at 3+ targets).

## Contract invariants this exercises

- **Transient channel, all four semantics.** Fires `cast_started` (in-flight commit), `proc`
  (arming glow), and `ready` (CD just up) on **three separate cues** in one pulse — the coverage
  scenario for `cues[].transient`. `cast_ended` is the one token **not** drawn: it would fire when
  the in-flight HoG's `succeeded` lands (a *future* pulse), noted here rather than faked.
- **Edges fire on the transition, not the persistence.** Every drawn transient is justified by a
  **"this pulse" marker** in State: `glow.changedAt == at` (proc), `cd.changedAt == at` (ready), or
  a `history.start` with no `succeeded` at `at−0.5` (cast_started). A steady-state proc/CD carries
  no such marker and would draw **no** transient (contrast `demonbolt-proc`).
- **Single-top-press holds.** Exactly **one** cue is `ROTATION`/`LATE` (HoG). The two `JUDGE` cues
  are non-press signals that **may coexist** (like `SOON`) — and multiple `JUDGE` cues are allowed
  (the cap is only on `ROTATION`/`LATE`). Both are legitimately `JUDGE` because both are
  **secret-gated**: Demonbolt by the Core stack count, Implosion by the Wild Imp count.
- **Readable-only justification.** No drawn cue leans on a secret. HoG's press rests on readable
  **shards**; its edge on readable **history**. Demonbolt's presence on readable **glow +
  `buff.isActive`**; its edge on **`glow.changedAt`**. Implosion's availability on the **napkin +
  imps-present buff**; its edge on **`cd.changedAt`**. Where the true rotational gate is secret
  (Core stack count, imp count), the golden **softens to `JUDGE`** rather than instructing — the
  proc/ready edges inform, they do not falsely green.
- **`aura` stays dark.** Every `aura.readable:false` (C_UnitAuras is secret in combat); no proc is
  sourced from it.

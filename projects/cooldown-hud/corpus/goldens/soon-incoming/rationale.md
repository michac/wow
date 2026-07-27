# soon-incoming — rationale

*(Re-pointed at W4 Phase 6a, 2026-07-27: the projected-shards intent. This golden used
to expect Shadow Bolt=ROTATION + HoG=SOON; it now expects HoG=ROTATION with Shadow Bolt
uncued — "incoming promotes the spender to the press." It is authored **RED** against the
pre-6b Coach, which still gates the HoG press on live shards; 6b greens it by gating on
`ctx.projected`.)*

**Situation:** combat; **2 soul shards** in hand; a **Shadow Bolt is in flight** (cast
committed — `history` carries its `start` for 686 with no `succeeded` yet, following an
earlier Shadow Bolt that already landed to build to 2); **no Demonic Core**
(`buff.isActive:false`, Demonbolt `glow:false`); **no Demonic Art armed** (Diabolic Ritual
`9426 buff.isActive:false` → Shadow Bolt stays Shadow Bolt, HoG stays HoG); Tyrant /
Dreadstalkers / Implosion cooling (napkin).

**The projection:** Shadow Bolt generates +1 shard on completion, so State's napkin sets
`power.SoulShards.incoming = 1` → **projected shards = value + incoming = 3**. Three is
**exactly Hand of Gul'dan's cost** (`rotation.md` step 9: "HoG at ≥3 Soul Shards … its cost
is 3").

**Oracle (rotation source → expected Guidance):**

- **Hand of Gul'dan is the single `ROTATION` press.** Walk the steady-state loop
  (`diabolist-sequences.md`, "the true steady state is a 3-state conditional loop"): no Art
  armed → *(skip Ruination/Infernal Bolt)*; imps not ≥6 / single-target → *(skip Implosion)*;
  Demonic Core down → *(skip Demonbolt)*; **Soul Shards ≥ 3?** — the readable in-flight
  Shadow Bolt makes the answer **yes on the projection** (`projected = 3`), and the builder
  is already committed, so the honest *next move to prompt* is the spender it feeds: **HoG**.
  It is the #1 ranked press → the single `ROTATION`.

- **This is the "one move ahead" call.** The overlay prompts the press you are *setting up*,
  not the press you have already committed. Shadow Bolt is in flight — re-cuing it teaches
  nothing; cuing HoG says "your shard is about to land, here is where it goes." Gating the
  press on `projected` (value + in-flight builder yield) rather than on live `value` is what
  turns this from a lagging read into an anticipatory one.

- **Shadow Bolt does NOT draw.** The builder is mid-flight (its `start` is in `history`); the
  single-top-press winner is HoG. Shadow Bolt is not the top press and carries no non-press
  signal here, so it is **uncued** (unlisted = `AVAILABLE`). (Contrast the pre-6a intent,
  which drew Shadow Bolt=ROTATION because the press was gated on the 2 shards in hand.)

- **Demonbolt does not draw** — `reactive`, needs a Demonic Core, which is down here
  (`buff.isActive:false`, `glow:false`). Unlisted (`AVAILABLE`).
- **Tyrant / Dreadstalkers / Implosion** are cooling (napkin) — not ready, not close enough
  for their own `SOON`. Unlisted.

**Why HoG=ROTATION and no separate SOON — the teaching:** this is the **mirror of
`incoming-overcap`**. There, `incoming` pushed the projection to the **cap** and forced a
**spend now** (`ROTATION` HoG, value 4 + 1 = 5). Here, `incoming` lifts the projection
**exactly to the spender's cost** — the same projected-gate promotes HoG to the press. The
projected shard number is the single quantity the press is gated on; there is no
value-vs-projected split, so there is no residual "SOON" anticipation cue riding alongside a
ROTATION. One projected number, one press.

**Readability (the crux):**
- Shard **`value` (2) is readable**; **`incoming` (+1)** is a napkin projection off the
  **readable in-flight cast** (`history` `start` for 686) + Shadow Bolt's mechanical +1
  yield. No secret is read. The HoG `ROTATION` cue rests entirely on readable state:
  - projected shards = `value` 2 + napkin `incoming` 1 = the cost 3;
  - no Core (`buff.isActive` 777 + Demonbolt `glow`), no Art (`buff.isActive` 9426), so HoG
    is still HoG.
  - HoG has no cooldown (`cd.state:"unknown"`, `source:"none"`); its readiness is a
    shard-gate, not a `cd` countdown.
- All `cd` reads are `readable:false` (combat secret); summon cooling is napkin-supplied.
  `aura` is `readable:false` throughout (C_UnitAuras dark in combat) and is never a source.
- **No `transient`.** HoG is not a fresh `cast_started` edge this pulse (nothing for 105174
  in `history`); the Shadow Bolt cast is already mid-flight (started 998.9, pulse 1000.0),
  not this pulse's edge. Steady-state → transients omitted.

**Contract invariants this exercises:**
- **`incoming` promotes the spender to the press** — the projected-shards gate. The ranking
  depends on the projection reaching the cost, with the builder already committed.
- **Single-top-press holds** — exactly one cue is `ROTATION` (HoG) and nothing else draws.
  There is no value-vs-projected split emitting a redundant SOON alongside it.
- **Napkin honesty, restated for 6b** — the press is gated on the *readable* projection
  (2 in hand + a readable in-flight builder = 3), not on a secret or a guess. The overlay
  anticipates the landing shard because the cast that yields it is observable.
- **`incoming` forwarded to `resourceBar`** so the meter shows the pending shard (`value:2`,
  `incoming:1`).

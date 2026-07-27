# implosion-primed — rationale

**Situation:** combat, AoE mode; Implosion off cooldown (napkin probably-up); Wild Imps out
(`143038` buff active, **count secret**); **2** soul shards; Demonic Core down. Cast `history`
shows **two recent full Hand of Gul'dan casts** (`105174 succeeded`, ~3 Wild Imps each) and **no
Implosion cast since**.

**Oracle (rotation source → expected Guidance):**
- **Implosion is the single `ROTATION` press — the napkin is confident, so it promotes.**
  `rotation.md` step 7 / `diabolist-sequences.md` ("Implosion at ≥6 Wild Imps", "Fixed 15 s CD;
  press on CD with ~6 imps up", 3+ targets) makes Implosion a real button in AoE once ~6 imps are
  banked. The gate — imp **count** — is a Secret Value, but the **imp-napkin** (estimate from the
  readable cast `history`) is *confident* here: **two** full HoGs since the last Implosion (~6 imps)
  in a conservative AoE window that **under-counts** if anything. Per the promotion rule (confident
  estimate ⇒ real press; conservative window errs low, so a confident state is genuinely pressable),
  Implosion promotes from `JUDGE` to `ROTATION`. This is the **positive** side of the gate the
  paired `implosion` golden holds at `JUDGE`.
- **Hand of Gul'dan is NOT the winner here — it is not even castable.** HoG costs **3** shards and
  the readable resource is **2** (`power.SoulShards.value:2`). Below cost ⇒ resource-gated,
  `AVAILABLE`/off — no cue. This is *why* the fixture sits at 2 shards: it removes the shard-spender
  from contention so a single unambiguous press remains, and the single-top-press invariant is
  satisfied structurally (Implosion vs. an un-castable HoG, not two live presses).
- **Demonbolt is off** — no Demonic Core (`777` `buff.isActive:false`); a Core proc is its gate, so
  it is not a call.
- **Shadow Bolt** (the free builder) would be the fallback if nothing else fired, but Implosion
  outranks it in the AoE priority — it caps at `AVAILABLE` (unlisted).
- **Tyrant (`2742`) and Dreadstalkers (`671`) are cooling** (napkin, `remaining>0`) — not ready,
  no cue.

**Contract checks this exercises:**
- **Single-top-press** — exactly one cue is `ROTATION` (Implosion `149122`); nothing else is
  `ROTATION`/`LATE`. HoG stays silent because it is below cost.
- **Napkin-confident promote** — the intended *positive twin* behaviour: a JUDGE-class ability
  becomes a real `ROTATION` press when the readable history makes the secret-count estimate
  confident. The `implosion` golden is the negative control (one HoG ⇒ not confident ⇒ stays
  `JUDGE`).
- **Secrecy gate** — the promote leans only on **readable** signals: the imp **count** is secret,
  but the cue rests on (a) Implosion's cd reading napkin **probably-up** (`cd.state:"unknown"`,
  `source:"napkin"`, **no** `remaining` — the honesty rule forbids a napkin `"ready"`), (b) imps
  present via `143038.buff.isActive:true` (readable), and (c) two full HoGs in the readable cast
  `history` with no Implosion since. None of these reads the secret imp count directly — the napkin
  is the sanctioned readable approximation. `aura` stays `readable:false` throughout and is never
  the proc source.
- **Pass-through string** — `note:"imps banked — implode"` is Coach-authored display text
  (sanctioned; the only place spec vocab may appear).
- **No transient** — Implosion's readiness is a napkin inference, not a readable phase edge, so no
  `ready`/`proc` transient is claimed (steady-state cue).

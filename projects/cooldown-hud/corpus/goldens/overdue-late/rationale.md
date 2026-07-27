# overdue-late — rationale

**Situation:** combat, single-target; **3 soul shards**; **Call Dreadstalkers (671) has been
ready ~6 s** (overdue); **Summon Demonic Tyrant (2742) is far** (~31 s out) so you are **not**
pooling Dreadstalkers for the Tyrant window; no Demonic Core; Implosion cooling; HoG castable.

**Oracle (rotation source → expected Guidance):**
- **Call Dreadstalkers is the press.** In `rotation.md`'s single-target priority it sits at
  **step 5**, *above* Hand of Gul'dan (step 9); `diabolist-sequences.md` classes it as a **hard
  cooldown — "press on time"** and pins its measured CD at **20.0 s**. Its side-rule is *"Call
  Dreadstalkers whenever it's up **and Tyrant isn't imminent**"* (steady-state loop). Both gates
  are satisfied here: it is up, and Tyrant is far — so Dreadstalkers is the #1 ready ability.
- **It draws `LATE`, not `ROTATION`, because the readable evidence says it is overdue.** The
  napkin has held it at *probably-ready* since `changedAt = 994` (~6 s of the current pulse at
  `at = 1000`). A hard-CD summon left sitting for ~6 s is generation wasted off its cooldown — the
  "you've been sitting on it" case the contract reserves `LATE` for. A *fresh* ready would be
  `ROTATION`; the old `changedAt` is what promotes it to `LATE`.
- **This is the single top press.** `LATE` and `ROTATION` never co-occur, and here exactly one
  cue is drawn. All competitors demote to `AVAILABLE` (unlisted).

**Why each loser is demoted (AVAILABLE, not drawn):**
- **Hand of Gul'dan (34991)** — castable at 3 shards (instant, no cooldown gate), but it is the
  **lower-priority spender** (step 9) and there is **no overcap pressure** (3/5, `incoming:0`), so
  holding it one GCD to fire the overdue summon costs nothing. It ranks *below* the overdue
  Dreadstalkers → `AVAILABLE`, unlisted. (Contrast `hand-of-guldan`, where nothing higher was up
  and the same 3-shard HoG *was* the `ROTATION`.)
- **Demonbolt (1979)** — reactive; needs a Demonic Core. Core is **down** (cd 777
  `buff.isActive:false`, Demonbolt `glow:false`, both readable). Not a call. Unlisted.
- **Shadow Bolt (34990)** — filler; the press only when nothing else is affordable. Dreadstalkers
  and HoG are both affordable, so it does not draw. Unlisted.
- **Implosion (149122)** — AoE gate (≥6 Wild Imps, 3+ targets); this is `mode:"st"` and it is
  cooling (napkin) anyway. Unlisted. (No `JUDGE` here — the imp-count "your call" only surfaces in
  an AoE fixture.)
- **Summon Demonic Tyrant (2742)** — anticipated **far** (`remaining:31`, napkin). Far anticipation
  is neither a press nor `SOON` (which is a ~2 s countdown edge), so no cue is drawn. Its distance
  is exactly what *permits* the Dreadstalkers press: it is not imminent, so we do not pool.

**The `LATE`-vs-`JUDGE` qualifier (why this fixture, not a burst-hold):**
If Tyrant were **near** instead of far — anticipated with a small `remaining` (a `SOON`-grade
countdown, ~2–12 s) — the rotation source says to **hold Dreadstalkers to be the last cast before
Tyrant** (`diabolist-sequences.md` SEQUENCE 2: *"Dreadstalkers is the last thing you press before
Tyrant"*). That is a your-call burst-timing hold whose ideal gate (exact Tyrant offset) is a
napkin estimate, not a live read — so it would surface as **`JUDGE` coexisting with a different
`ROTATION` press**, never as `LATE`. Here Tyrant is far, the hold rationale evaporates, and the
overdue summon is simply overdue → `LATE`.

**Readability (what's secret, what stands in):**
- **Every `cd` is `readable:false`** in combat. Dreadstalkers' readiness is **not** a live cd read
  (a napkin cd may never be `ready` — only `source:"live"` can be, and that never happens in
  combat). The readable stand-in is the **napkin transition**: the ~20 s estimate ran out, so the
  entry reads `state:"unknown", source:"napkin"` (carrying **no `remaining`**, per the honesty
  invariant) with an **old `changedAt`** = the readable "probably-ready, and has been for a while"
  signal that the `LATE` call rests on.
- **Shards are readable** (`power.SoulShards.value = 3`) — that is the readable gate confirming HoG
  *is* an alternative (hence a real demotion, not a vacuous one), and it feeds the `resourceBar`.
- **Core presence** reads via `buff.isActive` (777) + Demonbolt `glow` (1979), both readable and
  both false → Demonbolt correctly excluded. The `aura` field is `readable:false` throughout and is
  never the proc source.

**Contract invariants exercised:**
- **`LATE` as the single-top-press.** The overdue form of the one #1 press — proving `LATE` is not
  a co-equal second light but *the* press when readable evidence shows it is overdue (at most one
  `ROTATION`/`LATE`, and here it is `LATE`).
- **Napkin honesty for "probably ready."** `unknown`/`napkin` with no `remaining` + an old
  `changedAt` is how a hard-CD reads as overdue in combat — no false live `ready`.
- **Secret-gated softening.** The Tyrant-offset gate that would flip this to `JUDGE` is a secret
  estimate; because Tyrant reads *far*, the readable state cleanly justifies the `LATE` press with
  no hold ambiguity to soften.

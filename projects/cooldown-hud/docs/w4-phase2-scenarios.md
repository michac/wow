# Cooldown HUD — W4 Phase 2 scenario catalog (situation → expected Guidance)

> **STATUS: DRAFT r2, 2026-07-25.** The golden scenarios the Phase-2 corpus will freeze:
> each is a State *situation* + the *Guidance we expect the Coach to emit*, reasoned from the
> **Demonology rotation** — never from any addon code. Companion to `w4-phase2-goldens-plan.md`;
> contract is `guidance-contract.json`. Game state: patch **12.0.7**, Midnight S1.
>
> **r2 folds in the independent rotation review** (KB-only, no code): correctness fixes,
> the readability filter, the `mode` toggle, and the added in-Tyrant-window / hold / overdue
> scenarios. Review verdicts on the open questions: **IB never overcaps (self-gated) → spend
> first · Implosion stays JUDGE (secret gate) · AoE = a light mode toggle, not a track.**

## How to read this (self-contained)

**Guidance vocab** (Coach output tokens the Renderer resolves to pixels):
- **emphasis** (one per cue): `SOON` (anticipating — *not* a press) · `ROTATION` (press now) ·
  `LATE` (overdue press) · `JUDGE` (your call / can't instruct) · `SEQUENCE` (**attention-redirect**:
  "look at the sequence panel" — an anti-tunnel-vision nudge, *not* a press). **`AVAILABLE`** =
  off cd but not the call → **no cue** (internal).
- **SINGLE TOP PRESS:** at most **one** cue holds `ROTATION` (or `LATE`) at a time — the
  rotation's **#1 ready ability**. Others cap `AVAILABLE`. `SOON`/`JUDGE`/resource bar coexist.
- **resourceBar:** `{value, max, incoming, powerType}` (soul shards; colour game-canonical).
- **transient** (per cue, a phase EDGE): `cast_started` · `cast_ended` · `ready` · `proc`.
- **sequence:** `{show, title, cursor, steps:[{label, keybind, state}]}`, `state ∈ done ·
  active · pending · blocked · skipped`.

**Two framing rules the review forced:**
- **Readability filter.** Expected Guidance = the rotation applied to the **readable** State.
  Where the true gate is a Secret Value (e.g. Demonic Core *stack count*, Wild Imp count), the
  golden asserts what the readable signals justify (Core *up* via `buff.isActive`/`glow`), and a
  secret-gated refinement **softens** rather than instructing — the "inform where we can't read"
  rule. So a scenario's "ideal" rotational call and its expected Guidance can differ.
- **`mode`.** State forwards a **user-toggled `mode` (`st` | `aoe`)** constant. Demo's priority
  is "passive cleave" — largely the same across target counts — so `mode` drives only small
  divergences (Grimoire summon choice); it is not a separate scenario track. *(Added to State
  shape — architecture.md Stage 1.)*
- **Burst is an optional side-branch, not a mode switch.** The build/spend cue logic runs
  continuously and **mostly unchanged**; when the burst window becomes available the **sequence
  pane** shows the branch (with the resource **buildup prepended**, so build/spend cues don't
  special-case it), and the **only** cue change is **Dreadstalkers + Implosion → JUDGE** ("hold
  for burst — your call"). The player can keep running the rotation to intentionally hold burst.
  So the burst branch is carried by the *pane + JUDGE-holds*, not a `SEQUENCE` cue-mode — which
  largely dissolves the SEQUENCE-vs-ROTATION conflict (see Still open).

**The oracle is the Demonology rotation source applied to the readable State** — never the code.

---

## A · Positive priority — the single press

| Scenario | Situation (State) | Expected Guidance |
|---|---|---|
| **tyrant-ready** | Combat; Tyrant ready + 5 shards + summons **out & fresh** (full board); no summon pending | `Tyrant: ROTATION` (press now) · others AVAILABLE · `bar 5/5`. ⚠ *If a burst pane is active with Tyrant as its step, see design-Q (SEQUENCE vs ROTATION).* |
| **dreadstalkers** | Combat, outside a Tyrant window; Dreadstalkers off cd; **Tyrant far (>~20s)** | `Dreadstalkers: ROTATION` · others AVAILABLE · `bar 3/5` |
| **hand-of-guldan** | Combat; 3 shards; no Core; summons on cd; not overcapping | `HoG: ROTATION` · others AVAILABLE · `bar 3/5` |
| **demonbolt-proc** | Combat; Core **up** (`buff.isActive`+`glow` on Demonbolt); **no Art on the SB frame**; shards ≥2 | `Demonbolt: ROTATION`. *Readability note:* ideal gate is ≥2 core **stacks**, but the count is secret — the readable signal is "Core up + Demonbolt glows," so this is the readable approximation. `bar 2/5` |
| **shadow-bolt-filler** | Combat; nothing else lit (no proc, summons/HoG down) | `Shadow Bolt: ROTATION` · `bar 1/5` |
| **ruination** | Combat; Pit Lord Art armed; HoG frame → Ruination (liveSpellID 434635) | `Ruination: ROTATION` on HoG's cooldownID (nuance: source prefers firing it entering/inside Tyrant) |
| **infernal-bolt** | Combat; Mother-of-Chaos Art armed; SB frame (**cd 34990**) → Infernal Bolt (434506); **shards <3** (self-gated) | `Infernal Bolt: ROTATION` on cd 34990 (a **3-shard** builder). Ranks *above* Demonbolt when shard-starved. `bar 1/5` |
| **in-tyrant-window** *(new)* | Combat; **Tyrant active** (window open); imps out; shards up; core up | `HoG: ROTATION` (flood imps) · `Demonbolt: AVAILABLE` (dump cores between HoGs) · `bar 4/5`. *The most important DPS window — was unrepresented.* |
| **implosion-primed** *(new)* | Combat; Implosion off cd; **imp-napkin confident**: ≥2 recent full HoGs (~3 imps each), **no Implosion since**, within a conservative window (Tyrant-up widens it) | `Implosion: ROTATION` — napkin-confident press. *Imps estimated from cast `history`, not read; conservative window under-counts → errs to JUDGE, rarely false-greens (accepted napkin imperfection).* |

---

## B · Negative — must not falsely instruct

| Scenario | Situation (State) | Expected Guidance |
|---|---|---|
| **implosion** *(uncertain → JUDGE)* | Combat; Implosion off cd; imps out (count **secret**); **imp-napkin NOT confident** (only 1 recent HoG, an Implosion since, or window lapsed) | `Implosion: JUDGE` + note *"imps uncertain — your call"*; never auto-ROTATION here. The readable press winner (e.g. `HoG: ROTATION`) sits alongside. *(When the napkin IS confident → `implosion-primed` above.)* |
| **grimoire-available** | Combat; Grimoire off cd (**Imp Lord** if `mode:aoe`, **Fel Ravager** if `mode:st`) | `Grimoire: AVAILABLE` (**not** suppressed) — sits idle; the **sequence** drives the actual press. Never standalone ROTATION. |
| **overcap-soften** | Combat; Core up **but 4 shards** (Demonbolt +2 → overcap) | `HoG: ROTATION` (dump first) · `Demonbolt: AVAILABLE` + note *"core up — spend first"*. `bar 4/5`. *Also the home for IB: self-gated to <3 shards, so it likewise never overcaps.* |
| **burst-hold** *(was summon-hold)* | Combat; burst branch available/imminent (Tyrant ~15s out); Dreadstalkers + Implosion off cd | `Dreadstalkers: JUDGE` + `Implosion: JUDGE` — *hold for burst, your call* (press on cd, or hold to stage the window). The build/spend `ROTATION` pick keeps running underneath. *This is the **only** cue-logic change when burst is available (see Burst model).* |

---

## C · Cross-cutting — emphasis edges & channels

| Scenario | Situation (State) | Expected Guidance |
|---|---|---|
| **overdue-late** | Combat; Dreadstalkers ready ~6s (`cd.changedAt` old) **AND Tyrant far / long CD** (not pooling) | `Dreadstalkers: LATE` (overdue; sole winner). *Qualifier matters — if Tyrant were near, this is `summon-hold`, not LATE.* |
| **hog-overcap-late** *(new)* | Combat; **5 shards, capped ~3s** (`changedAt` old) | `HoG: LATE` (overdue dump) · `bar 5/5`. *The readable LATE-dump. (Demonbolt-at-4-cores would be the other, but core stacks are secret → **not assertable** — a documented readability limit.)* |
| **soon-anticipated** | Combat; Tyrant ~2s out (`state:anticipated, source:napkin`); summons not all out | `Dreadstalkers: ROTATION` (staging) · `Tyrant: SOON` + countdown. *Fixed: pre-Tyrant you stage/pool — you do **not** spend HoG (shards are banked to flood HoG inside the window).* |
| **opener-midflight** | Combat; opener active: Dreadstalkers+Imp Lord done, cursor on Tyrant, HoG pending; **Implosion step present only if `mode:aoe`/talented** | `pane {title:"OPENER", cursor:2, steps:[done, done, active, pending, …]}` · active-step cue `Tyrant: SEQUENCE` |
| **resource-states** | 3 sub-fixtures: 0 · 3 · 5 shards + in-flight SB (+1) | `bar {value:0/3/5, incoming:0/0/+1, powerType:SOUL_SHARDS}` |
| **transient-edges** | Series: HoG cast commits → lands; Dreadstalkers cd comes up; Core lands | (a) `HoG transient:cast_started` → (b) `cast_ended` · (c) `Dreadstalkers transient:ready` · (d) `Demonbolt transient:proc` |
| **secrecy-combat** | Combat; cds `readable:false`; napkin fills; Core via `buff.isActive`+`glow`, `aura.readable:false` | Cues from **readable values only**: `Demonbolt: ROTATION` (buff/glow, inherits the demonbolt-proc readable-approx caveat), `Tyrant: SOON` (napkin). **No cue cites a secret cd.** Largely a State-contract test. |

---

## Resolved by the review (with KB sources)

- **IB overcap → spend first.** Infernal Bolt is self-gated to `<3 shards` (`maxroll-mplus.md`
  212, `rotation.md` step 10), so it never overcaps; at 3+ shards you dump with HoG and the Art
  stays armed. No "fire anyway" branch. → folded into `overcap-soften`.
- **Implosion → JUDGE by default, napkin-promote to ROTATION when confident** (revised
  2026-07-25, overriding the reviewer's blanket-JUDGE). The imp count is a **napkin** —
  approximate-but-honest, the same shape as the cooldown napkin. Promote when the estimate is
  confident (≥2 recent full HoGs, no Implosion since, conservative window); else JUDGE. The
  reviewer's objections are handled by keeping the window **conservative** (under-count → errs to
  JUDGE, never systematically false-greens) plus the accepted "doesn't have to be perfect."
  Untracked adders (Inner Demons / Ruination) only *add* imps → under-count is safe; expiry is
  the one real risk, bounded by the short window (Tyrant-up widens it). *Coach-side:* computed
  from State `history` (HoG casts − Implosion consumption); `history` may want a per-HoG
  imp-yield so partial HoGs don't over-count.
- **AoE → a `mode` toggle, not a track** (per design intent; Demo is passive-cleave). Only real
  divergence is Grimoire (Imp Lord vs Fel Ravager) + Implosion being universally in-rotation.

## Still open

**Rotation confirms (small):**
- **v1 build = current meta** (confirmed 2026-07-25): Implosion talented in ✓, Power Siphon not
  the pick ✓, **Summon Doomguard NOT in the build** ✓. Off-build talents are out of scope for v1
  goldens; the addon falls back to neutral / no-cue for unmapped IDs (existing behavior) — an
  optional `offbuild-neutral` scenario could prove that graceful degradation.
- **KB fix (side):** ✅ done 2026-07-25 — `abilities.md` Infernal Bolt corrected **+2 → +3**
  (Tier-1 maxroll / `diabolist-sequences.md`), `reviewed:` bumped.

**Design (contract, not rotation):**
- **SEQUENCE → resolved: keep it, as an ATTENTION-REDIRECT.** Not a press and not a press-mode —
  `SEQUENCE` tells the Renderer to point the player at the sequence **panel** (anti-tunnel-vision
  when locked on the CDM icons). It coexists with the single `ROTATION` press, like `SOON`/`JUDGE`,
  and fires when the panel holds the salient plan (opener active, burst branch available). Its
  exact Renderer treatment (arrow/glow, loudness) is deferred to the Renderer.
- **Readability filter — confirm the principle** (expected Guidance = rotation applied to
  *readable* state; secret-gated refinements soften). Applied above to demonbolt-proc and the
  Demonbolt-at-4-cores LATE that can't be asserted.
- **State `mode` field** — ✅ added to State shape (architecture.md Stage 1).

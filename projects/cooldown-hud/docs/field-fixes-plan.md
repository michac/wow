# Cooldown HUD — field-fixes plan (what the first live session found)

> **STATUS: PLANNED — not started.** Four phases (A, B, C, C2), each `busted`-gated.
> Written 2026-07-30 after the **first session in which the HUD actually rendered** (the
> v0.32.25 outage fix) and the **first in-client alert capture** (v0.32.26/27). Both
> produced findings that invalidate parts of the shipped Destruction brain.
>
> **Doc map:** the rotation of record is `specs/destruction/rotation.md`; the pipeline is
> `architecture.md`; the live worklist is `status.md` (this plan is its Active-work item).
> The alert-channel facts this plan builds on are in
> `knowledge/addon-dev/api-events-and-discovery.md` §2.8 — **confirmed in-client**, not
> desk-derived.

---

## Why — the field session invalidated four assumptions

| Assumption | What actually happened |
|---|---|
| The tracked set from DB2 ≈ what loads | **Incinerate has no CDM icon at all.** The live Essential set is 9 entries; Incinerate, Soul Fire, Havoc and Channel Demonfire are absent. |
| `state.abilities` holds pressable abilities | It holds the **enumerated DB set** (`allowUnlearned = true`). Untalented spells read `ready` forever and win the rotation. **216 dropped Soul Fire cues** in one session. |
| Immolate is keyed on the DoT aura `157736` | The **pressable** row is `348`; `157736` lives on the Buff-bar viewer and never enters `abilities[]`. So L8 can never fire. |
| A tracked Wither means Hellcaller | A live Hellcaller build tracked **Malevolence but Immolate**. The inference picked Diabolist. |

Plus one capability gain the capture handed us: **the alert channel carries more than we
consume.** `PandemicTime` and `ChargeGained` both fire in combat, on the choke point State
already hooks — while the corresponding *state* reads are secret.

## Decisions locked before starting

1. **Filter in `State`, not in the Coach.** `abilities` is documented as "the PRESSABLE
   representative row"; an ability with no icon is not pressable. Filtering there fixes both
   specs at once and needs no spec/Coach edits.
2. **`displayable` is the primary gate, `isKnown` the secondary.** `isKnown` alone does not
   cover Incinerate (known, but untracked by the layout). Gating on "can the Binder draw
   it?" covers both causes.
3. **Dropped rows are logged, never silent.** A filter that silently removes a real ability
   would be the same class of bug as the nil-guard outage. The decision log records what was
   dropped and why.
4. **The state is secret; the edge is not.** Pandemic and charges are both solved as
   **edge latches over a seeded baseline**, never as state polls. `IsInPandemicTime` throws,
   and `GetSpellCharges` is secret — measured, not assumed.
5. **The napkin honesty rule extends to charges.** Overcount claims a charge you do not
   have; undercount only under-presses. Bias to undercount, clamp to `[0, max]`, and let an
   exact OOC read always win.
6. **No rotation re-shaping in this plan.** The `hero × mode` four-list split is real work
   and is **backlogged separately** — four lists are worthless while phantom abilities win
   and the DoT line cannot fire.

---

## Phases

Existing gates are the regression net: **luacheck clean + 209 busted tests**, which must
stay green throughout. One release at the end of C2.

| Phase | Work | Gate |
|---|---|---|
| **A** | **Stop phantom abilities winning.** In `State.Build`'s domain-view fold, mark each row `displayable` (an item frame exists in `itemFrameMap()`) and carry `isKnown`; filter `abilities` on them. Raw `cooldowns` keeps everything (it is the diagnostic view). Record drops in the decision log. | New `state_domainview_spec`: an unknown row and an undisplayable row never reach `abilities`; the raw view still has both. A Coach test proves the winner falls through to the next line instead of vanishing. 209 stay green. |
| **B** | **Fix identity.** (1) `ctx.dotID` resolves to whichever id is actually in `ctx.facts` — Wither → Immolate-aura `157736` → Immolate-cast `348`. (2) Hero detection: try a real API (`C_ClassTalents` / `TraitSubTree`) first; fall back to **multi-signal** inference (Malevolence **or** Wither ⇒ Hellcaller; Ruination / Infernal Bolt / Diabolic Ritual ⇒ Diabolist), ambiguity defaults to Diabolist **and says so in the log**. | `coach_destruction_apl_spec` gains the **live configuration as a fixture** (Malevolence + Immolate-as-`348`): asserts hero = Hellcaller and L8 targets `348`. |
| **C** | **Pandemic edge latch.** State grows `dotEdge` beside `readyEdge`, fed by the alert hook that already sees all six types: `PandemicTime` ⇒ latch set, `OnAuraRemoved` ⇒ cleared+absent, `OnAuraApplied` ⇒ cleared+fresh. Surfaced on the domain-view row so the brain reads `ctx.dotRefreshable` and never sees a cooldownID. **Delete** `DOT_REFRESH_LEAD` and the speculative `uptime` read. | ⚠ The latch keys on **cooldownID**, and Immolate has **two** (`133441` aura + `164597` cast) that BOTH fired `PandemicTime` — either must set one latch on one base spellID. Spec covers the two-cid case. |
| **C2** | **Charge napkin** — same seam. Seed exact from `ReadCharges` OOC; `−1` on `UNIT_SPELLCAST_SUCCEEDED`; `+1` on `ChargeGained` (which also captures **cooldown-reset procs**, since it fires on any upward move of Blizzard's cached count); clamp `[0,max]`; exact re-read wins OOC. Surfaced as `charge.cur` with `source = "napkin"` so the brain can tell an estimate from a measurement. | Spec drives the full loop off synthetic pulses incl. clamping and the OOC re-seed. Only Conflagrate consumes it today — Shadowburn has **no charges** (DB2 `ChargeCategory = 0`). |

## Risks, and what makes each safe

- **A drops a real ability.** The whole point is removing rows, so a wrong signal removes a
  real button. Mitigated by gating primarily on `displayable` (a frame either exists or it
  does not — no inference), and by logging every drop so it is visible on the next capture
  rather than silent.
- **B's hero API may not exist.** If there is no clean read, the multi-signal fallback is
  strictly better than today's single-signal inference, which has already been observed
  failing. Ambiguity resolves to Diabolist (the KB's default profile) and is logged.
- **C latches stale.** A DoT ticking on a target that died, or a target swap, could leave
  the latch set. `OnAuraRemoved` should cover it; if not, the latch needs a target-change
  reset — which is the first thing to check on the next capture.
- **C2 drifts.** Every napkin drifts; this one is fenced so drift can only *under*-press,
  and it re-seeds exactly on every combat exit.

## Out of scope — backlogged in `status.md`

- **`hero × mode` four-list rotation split** (the real rotation work; do it after this).
- **Artificial CDM icons** — a HUD-owned panel for Incinerate / Shadow Bolt, which is the
  actual fix for "the floor press has no icon". Phase A only stops it corrupting the
  *decision*; it does not make Incinerate visible.
- **Branch fallback** — "we cannot decide, because X" instead of always offering a runner-up.
- **Command consolidation** — one sectioned `/cdmp dump` behind a section registry.

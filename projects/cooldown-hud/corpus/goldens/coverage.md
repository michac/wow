# Golden corpus — contract-vocab coverage

Generated over the 23 scenario goldens under `corpus/goldens/` against the
`guidance` contract (`guidance-contract.json`, v1). One line of status at the
bottom. `README.md` is not a scenario.

Scenarios (23): `burst-hold`, `cast-ended-edge`, `demonbolt-proc`,
`dreadstalkers`, `grimoire-available`, `hand-of-guldan`, `hog-overcap-late`,
`implosion`, `implosion-primed`, `in-tyrant-window`, `incoming-overcap`,
`infernal-bolt`, `opener-midflight`, `overcap-soften`, `overdue-late`,
`resource-states`, `ruination`, `secrecy-combat`, `shadow-bolt-filler`,
`soon-anticipated`, `soon-incoming`, `transient-edges`, `tyrant-ready`.

## emphasis (`cues[].emphasis`)

| member | scenarios |
|---|---|
| SOON | secrecy-combat, soon-anticipated |
| ROTATION | burst-hold, cast-ended-edge, demonbolt-proc, dreadstalkers, grimoire-available, hand-of-guldan, implosion, implosion-primed, in-tyrant-window, incoming-overcap, infernal-bolt, overcap-soften, resource-states, ruination, secrecy-combat, shadow-bolt-filler, soon-anticipated, soon-incoming, transient-edges, tyrant-ready |
| LATE | hog-overcap-late, overdue-late |
| JUDGE | burst-hold, implosion, transient-edges |
| SEQUENCE | opener-midflight |

All 5 public emphasis members exercised. Internal-only tokens (`NEVER`,
`AVAILABLE`) correctly never appear as drawn cues — they mean "no cue," and the
`_expected` prose repeatedly names demoted abilities as AVAILABLE/unlisted.

## transient (`cues[].transient`)

| member | scenarios |
|---|---|
| cast_started | transient-edges |
| cast_ended | cast-ended-edge |
| ready | transient-edges |
| proc | transient-edges |

All 4 transient members exercised. `transient-edges` carries 3 on one pulse (HoG
cast_started + Demonbolt proc + Implosion ready); `cast-ended-edge` (added
2026-07-25 to close the last hole) carries the landing edge (a Shadow Bolt
`succeeded` at == pulse at, still the filler press).

## stepState (`sequence.steps[].state`)

| member | scenarios |
|---|---|
| done | opener-midflight |
| active | opener-midflight |
| pending | opener-midflight |
| blocked | opener-midflight |
| skipped | opener-midflight |

All 5 members exercised, all by the single sequence-bearing golden
(`opener-midflight`, a 6-step OPENER panel). `opener-midflight` is the only
scenario with `sequence.show: true`; every other golden is steady-state
(`sequence.show: false`).

## resourceDisplay (`resourceBar.display`)

| member | scenarios |
|---|---|
| discrete | all 23 |
| percentage | — (none) |

## powerType (`resourceBar.powerType`)

| member | scenarios |
|---|---|
| SOUL_SHARDS | all 23 |

## resourceBar incoming projection (`resourceBar.incoming`)

| projection | scenarios |
|---|---|
| zero (0) | burst-hold, cast-ended-edge, demonbolt-proc, dreadstalkers, grimoire-available, hand-of-guldan, hog-overcap-late, implosion, implosion-primed, in-tyrant-window, infernal-bolt, opener-midflight, overcap-soften, overdue-late, ruination, secrecy-combat, shadow-bolt-filler, soon-anticipated, transient-edges, tyrant-ready |
| positive (+1) | incoming-overcap, resource-states, soon-incoming |
| negative | — (deferred to 6d) |

2 of 3 sign cases exercised: positive (in-flight builder about to add a shard)
and the zero baseline. **Negative is deferred to 6d** — 5b's `incoming` is
**builder-only**, so no golden carries a negative sign yet; `transient-edges` was
neutralized to 0 at 6a (its synthetic −3 pre-dated the signed-incoming work). The
signed in-flight-spend case returns with 6d.

## GAPS

- **`resourceDisplay.percentage` — EXPECTED gap.** Demonology's only resource
  meter is soul shards, which are discrete whole segments. `percentage`
  (continuous fill) has no Demo home; it exists in the closed-set enum for a
  future spec whose resource is a bar (mana/energy/fury as %). No golden should
  force it. Confirmed expected.
- **`transient.cast_ended` — CLOSED (2026-07-25).** Was the one real hole; now
  covered by `cast-ended-edge` (a Shadow Bolt landing edge, `succeeded` at ==
  pulse at, still the filler `ROTATION`). All 4 transient members now exercised.
- **`powerType` — only SOUL_SHARDS.** Every golden is Demo, so only the
  SOUL_SHARDS token appears. Expected for a v1 Demo-only corpus; other
  Enum.PowerType tokens arrive with other specs.
- **stepState / SEQUENCE concentration — noted, not a hole.** All 5 stepStates
  and the SEQUENCE emphasis live entirely in `opener-midflight`. Coverage is
  complete but single-sourced; a second sequence golden (e.g. a burst-branch
  panel, or a `blocked`→`active` progression) would add redundancy but is not
  required for vocab coverage.

## Malformed check

No malformed goldens found. Spot-checks that passed on all 23:

- **single-top-press invariant** (≤1 cue holds ROTATION or LATE, never both
  co-occurring): every golden has exactly one ROTATION *or* one LATE, except
  `opener-midflight` which has zero press cues (allowed — the panel + SEQUENCE
  carry the guidance). JUDGE/SOON/SEQUENCE coexist with the single press as the
  contract permits (burst-hold: 1 ROTATION + 2 JUDGE; soon-anticipated: 1
  ROTATION + 1 SOON; etc.).
- **cue shape**: every cue has `draw` + `emphasis`; optional `transient`/`note`
  omitted where null. No class/spec vocabulary leaks outside pass-through
  `note`/`label`/`title` fields.
- **resourceBar**: all carry value/max/incoming/display/powerType; no resolved
  RGBA, no class tokens — powerType is the sanctioned game-token exception.
- **projected-ranking consistency**: incoming-signed goldens rank on
  value+incoming as the contract states (incoming-overcap 4+1=cap → dump;
  soon-incoming 2+1=cost → HoG promoted to the ROTATION press, the 6a re-point;
  resource-states 0+1 → still builds). NOTE: `soon-incoming` is authored **RED**
  against the pre-6b Coach (which still gates the HoG press on live shards); 6b
  greens it by gating the press on `projected`.

## Status

STATUS: 5/5 emphasis, 4/4 transient, 5/5 stepState, 2/3 incoming signs, discrete
display all covered (23 goldens); remaining gaps — `percentage` display
(expected, no Demo home; arrives with a future non-shard spec) and the
**negative incoming sign** (deferred to 6d with the signed in-flight-spend work).
`soon-incoming` re-pointed at 6a (projected-shards intent) — authored RED, greened
by 6b. `cast_ended` closed 2026-07-25 via `cast-ended-edge`. No malformed goldens.

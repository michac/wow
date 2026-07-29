# Cooldown HUD — the collect-vs-assert doctrine

How in-game truth is captured and checked. `wowkb.cdmp` is the addon's analogue of
the KB's `verify-in-game.md`: it reads a `/cdmp probe` capture off SavedVariables and
**asserts** it against `probe-baseline.json`, the tested-assumptions-of-record.

## The governing rule

> **Collect a new observation → addon change + release. Assert / interpret /
> re-verify → local, no release.**

The addon owns only *observation* (stable — it changes rarely). The assertions
(which change often) live where they're cheapest to change: editable Python/JSON, one
edit away, no release. So adding or retuning an assumption is a JSON edit;
teaching the addon to observe a *new* datum is the one thing that needs a release.

This is why `/cdmp selftest` (an in-client assertion suite) was shelved: the probe
already captures the observations, so a selftest would only re-collect them and bake
the expected answers into shipped Lua. Interpretation belongs in local tooling —
which also buys cross-run diffing, history, and the KB, none of which a chat-line
PASS/FAIL has.

## What the probe captures

`/cdmp probe` persists a **structured** table `CDMProbeDB.probe.ooc` / `.combat`
(one observation set, two renderers — a shared serializer builds both the text report
a human reads and this table, so they never drift). Per context: the secret-API map,
Section A cooldown readability per tracked spell, Section B override pairs +
base→live divergence, Section C per-phase cast readability, Section D the imp-count
side channel, plus the folded HUD state block. The pull log `CDMProbeDB.pulls` (last
5 combat exits) is captured separately and already structured.

⚠ **Everything flushes to disk only on `/reload`.** In-game, `/cdmp probe guide`
prints a pull-based coverage checklist — what the capture is still missing — so you
learn a capture is incomplete *while still able to fix it*, not an hour later.

## The reader — `wowkb.cdmp`

Mirrors `wowkb.diagnostics`: locates the newest `CDMProbe.lua` under
`WTF/Account/*/SavedVariables/`, reads `CDMProbeDB.probe` (+ `.pulls`).

- **`check`** — assert the capture against the baseline → **PASS / WARN / FAIL** per
  assumption, a diff vs baseline and vs the previous capture, and a **"not covered
  this run"** list for goals the capture didn't hit. **Exit non-zero on any
  high-severity FAIL** — a CI-style gate you can eyeball.
- **`show`** — pretty-print the latest capture (off structured data).
- **`diff`** — capture vs capture / capture vs baseline (`ooc` vs `combat` is the
  combat-seam view), for spotting drift.

The baseline (`probe-baseline.json`, patch-stamped) maps each assumption's `expect`
onto a check over the structured capture. Editing or adding one is a JSON edit.

## The two flows

**Patch dropped — verify assumptions hold (no release):** deploy the current addon →
`/cdmp probe guide` walks standard coverage (OOC probe → pull the tracked set →
in-combat probe → `/reload`) → `wowkb.cdmp check` → **PASS** (holds) or **FAIL**
(SUCCEEDED went secret, a spellID moved, an override changed…). Triage: fix the addon,
**or** re-stamp the baseline if the game legitimately changed and we accept the new
truth.

**Test a new assumption (extend the baseline):** if the probe doesn't already observe
the datum → add a passive recorder / field (**addon change + release**, the one place
a new in-game test needs one). Add the expectation to the baseline JSON (local) →
guided capture → `check` → promote with a `confirmed` stamp; Case 1 now re-checks it
every patch.

## The honesty guards

- **Absence of evidence is not a pass.** A check whose capture lacks the evidence
  reports as *not covered*, never as a pass — a two-context claim refuses to confirm
  off one context. (The empty-store failure mode: probing on pre-release code flushes
  an empty `CDMProbeDB.probe`; `check` correctly reports *no capture*.)
- **The baseline is only as honest as its stamps.** An assumption re-confirmed on a
  new patch must re-stamp `confirmed`/`patch`; a stale stamp silently claims a check
  that hasn't run (the same failure mode the KB's `reviewed:` convention guards). The
  reader surfaces each assumption's `confirmed` age.
- **Structured/text never drift** — both are built from one in-memory observation set.

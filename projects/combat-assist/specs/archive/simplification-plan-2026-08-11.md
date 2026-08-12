# Combat Assist Plus — philosophy-first simplification plan

> Archived after execution: the decision packet incorrectly coupled removal of the tier
> engine's complexity with removal of discrete priority tiers. The replacement plan lives at
> `../simplification-plan.md`.

**Purpose:** bring the project back under `spec.md` §1 after the rest of the design
grew into a formal system whose internal rules began directing the product. This is a
temporary migration plan, not a sixth permanent source of product truth. It records the
order of work; decisions that survive the work land in `spec.md`, implementation tasks in
`backlog.md`, and completed rounds in `notes.md`. Delete or archive this file when the plan
is complete.

The plan starts from one presumption: **§1 is the constitution; everything after it is
reviewable.** Existing prose, schemas, tests and code are evidence of an attempted design,
not evidence that the design is required.

## Execution preamble — start here on a fresh context

This section makes the plan resumable without the conversation that produced it. **Read this
whole file before acting. Do not treat the recommendations below as newly approved product
doctrine.** The author approved creating this cleanup plan; they have not pre-approved every
product choice it proposes or any source change. The audit and decision checkpoints are how
those choices become authorized.

### Required reading order

1. `projects/combat-assist/CLAUDE.md` — project routing and the rule that status lives in
   `backlog.md`.
2. This plan, in full.
3. `spec.md` **§1 only** — read it once without the later ontology coloring it. Write down its
   commitments in plain language before continuing.
4. `backlog.md` → `## Status` and `What the first flight said` — current implementation and
   the first real play/capture findings.
5. The rest of `spec.md`, then `demonology/catalog.md`.
6. `discussion.md` D7, D12, D14, D15, D16 and D17, followed by the 2026-08-10 and
   2026-08-11 entries in `notes.md`.
7. `flight-reading.md` only far enough to understand what the captures can and cannot prove.
8. Before reviewing or changing addon source, follow the workspace's standing addon-sync
   instructions. Then read the addon's own `CLAUDE.md` and inspect, in this order:
   `Catalog.lua`, `Catalogs/Demonology.lua`, `Tier.lua`, `Treatment.lua`, `Channel.lua`,
   `Overlay.lua`, `Bars.lua`, `Glow.lua`, and the tests under `tests/spec/`.

Do not begin by reading all 2,000+ lines of later design prose as one undifferentiated source
of truth. The point of the order is to compare it against §1, not absorb it before making the
comparison.

### Why this plan exists — findings from the adversarial review

The review that produced this plan found the following. These are **audit leads with concrete
evidence**, not replacement commandments; verify them against the files during Phase 1.

1. **The catalog ontology outran §1.** Section 1 says the gate/channel restriction is the one
   line worth enforcing in code. Later sections created five catalog checks, mandatory
   coverage and silences, subject types, cue schema, estimate disclosures and a closed rule
   language. `Catalog.lua` and its tests then made those derived choices expensive to question.
2. **The ontology blocks a request that §1 plainly allows.** The author asked for simple
   Tyrant context dots driven by readable facts. D16 records that the existing definition of a
   cue cannot express them because it requires a sealed client-owned half. Principle (b) says
   readable information is fair material for good hints.
3. **Automatic sequences appear to cross the product boundary.** M5 marks the current and
   next spell after automatically detecting an opener or burst sequence. The prose calls that
   a pattern the player chose even though it explicitly provides no arming or selection step.
4. **The tier language obscures real ordering.** The spec says tiers describe value rather
   than order, but HIGH / MEDIUM / LOW are ordered, LOW says to press it only when nothing
   above is lit, and the source ranks the tiers numerically. Whether that ordering is wanted is
   an author decision; euphemistic wording is not an answer.
5. **The first play report was subordinated to the model.** The author said the rings were too
   flickery and should be brighter. D14 promoted saturation to the root explanation and said
   the brightness report could not be taken at face value. Saturation may be relevant, but the
   capture could not establish that the independent visual choices were good. The backlog also
   said §3 would not be reopened immediately after the first pixels exposed problems in it.
6. **Visual hypotheses became invariants and safety claims.** Exact alphas, pulse rates, a
   `0.68` trough, pairwise-distinct rates and a golden-ratio phase stride are pinned in source
   and tests. The first flight described the result as candles. The repository does not
   establish that its pixel-area extrapolation is a validated safety guarantee for the actual
   rendered surface.
7. **Tests canonize mutable gameplay opinions.** `tier_spec.lua` asserts that Tyrant becomes
   HIGH after Dreadstalkers, Grimoire becomes HIGH around Tyrant, and several entries should be
   HIGH together. Play already reversed the Tyrant opinion while the test correctly proved the
   old rule fired as authored.
8. **Exhaustive silence coverage creates work unrelated to the player experience.** The
   Demonology catalog accounts for defensives, movement, CC, passive rows, removed talents and
   other abilities cap does not enhance because the schema requires every bound row to be an
   entry or silence.
9. **Strict validation still admits inert behavior.** The legal channel vocabulary is wider
   than the renderer; several accepted forms draw nothing and report `nodraw`. At the same
   time, the admitted `talent` gate is not wired into the current reads.
10. **The documentation process failed its own status rule.** `backlog.md` says the drawn
    surfaces were flown on 2026-08-10, while the addon's `CLAUDE.md` says no cap-drawn pixel has
    ever been observed. Treat `backlog.md` as current and the contradiction as evidence that
    the permanent documentation needs less duplicated state.

### Authority and decision boundaries

Use these categories throughout the work:

- **Already authoritative:** `spec.md` §1; sourced and current client facts in
  `knowledge/addon-dev/`; workspace safety, capture and release rules.
- **Observed evidence:** the author's play reports and interpreted captures. Evidence can
  disprove a design or explain behavior; it does not manufacture a product requirement by
  itself.
- **Existing but reviewable:** `spec.md` §2 onward, the Demonology catalog, discussion
  arguments, backlog recommendations, source architecture and tests.
- **Proposals in this plan:** removing M5, reducing tiers, allowing gate-only markers,
  dropping mandatory silence coverage, simplifying visuals and shrinking the catalog. These
  are the review's recommendations, not approved product decisions until the Phase 1
  checkpoint.

When a sourced platform fact and a product preference conflict, the platform fact bounds the
solution. When two product choices conflict, stop at the checkpoint and ask the author; do not
resolve it by inventing a more elaborate abstraction.

### Artifacts, checkpoints and resume protocol

Execute one phase at a time. Do not silently run the whole plan in one session.

| Phase | Required artifact | May change source? | Stop for author? |
| --- | --- | --- | --- |
| 0 | Baseline + test classification in `simplification-audit.md` | No | No |
| 1 | Normative-claim ledger and compact decision packet in `simplification-audit.md` | No | **Yes — mandatory** |
| 2 | Proposed edits to the permanent docs | No addon source | **Yes — approve the rewritten product spec** |
| 3 | Approved catalog/API design and source migration | Yes | Ask only on a newly exposed product choice |
| 4 | Mechanical/characterization test split | Yes | No, if it implements approved Phase 2–3 decisions |
| 5 | Static visual baseline | Yes | **Yes — requires an in-game judgment** |
| 6 | Small Demonology pilot | Yes | **Yes — approve/fly the chosen experiences** |
| 7 | Play report first, capture-supported findings second | Yes | At every product judgment |
| 8 | Cleanup and permanent-doc consolidation | Yes | Release remains separately ask-first |

`projects/combat-assist/specs/simplification-audit.md` is a **temporary execution artifact**.
Create it in Phase 0 with:

- the baseline and test classification;
- the Phase 1 claim ledger;
- the author decision packet and recorded answers;
- links to proposed Phase 2 doc edits;
- a short phase log, newest entry last.

Do not let that audit file become another product spec. It records migration evidence and is
deleted or archived with this plan in Phase 8.

Maintain the block below whenever a phase begins or ends. A fresh context resumes from the
first incomplete phase, reads the named artifacts, and does not redo completed analysis unless
new evidence invalidates it.

### Resume status

- **Current phase:** Phase 5 checkpoint — awaiting an in-game judgment of the static baseline
- **Last completed phase:** Phase 4; Phase 5 source baseline is built
- **Temporary audit artifact:** `simplification-audit.md`
- **Pending author checkpoint:** separately approve a test release, then judge the Phase 5
  flight questions in `flight-reading.md`
- **Source changes made by this plan:** reduced catalog/signal/track contract, two-entry pilot,
  static overlay, fixed readable markers, one independent bar, and split tests
- **Last updated:** 2026-08-11

At a mandatory checkpoint, end the work with a concise decision packet. Present the disputed
choice, the smallest viable options, the review's recommendation and the consequence of each.
Do not encode a default choice into the next phase while waiting.

## Desired outcome

cap remains an opinionated addon that makes the Cooldown Manager more useful while
respecting Midnight's restricted-data boundary. Its code enforces the boundary the client
requires. Product choices that can only be judged by playing remain easy to change and are
described as hypotheses until play earns stronger language.

The finished project should have:

- a short product spec whose rules can be traced directly to §1;
- a small catalog API that expresses useful hints without becoming a rotation DSL;
- no feature whose practical effect contradicts “without telling you what to press”;
- mechanical tests for mechanical guarantees, not tests that canonize rotation opinions or
  visual taste;
- visual treatments chosen through play, without unsupported constants promoted to safety
  invariants;
- one reliable status source and substantially less documentation routing overhead.

## Guardrails for the cleanup

1. **Do not change §1 during the first pass.** If the cleanup exposes a real ambiguity in
   §1, record the question in `discussion.md` and ask the author; do not resolve it by
   redefining a term elsewhere.
2. **Do not preserve a rule merely because code or tests implement it.** Implementation cost
   is migration information, not product justification.
3. **Keep platform facts separate from product choices.** Secret Values, combat lockdown and
   measured CDM behavior remain sourced from `knowledge/addon-dev/`. A product document
   records only the consequence cap chooses.
4. **Use “must” only for a §1 commitment, a platform constraint, or a deliberately approved
   product boundary.** Everything else begins as a hypothesis to fly.
5. **Do not optimize toward an occupancy quota.** Capture distributions may explain a play
   report; they do not decide what percentage of a pull ought to be HIGH.
6. **No release is implied by this plan.** Source changes are tested locally and a release
   remains ask-first under the project rules.

## Phase 0 — freeze expansion and establish the baseline

- Pause M3e, the remaining M4 work, M5, new channel forms, and second-spec work.
- Record the current v0.2.4 behavior as a baseline, not an acceptance target: supported
  catalog, visible surfaces, known failures, and the already-interpreted first flight.
- Classify the existing tests before editing them:
  - **mechanical** — secret/readable separation, unknown propagation, binding, safe failure;
  - **characterization** — what the present Demonology catalog happens to say;
  - **policy/taste** — tier meanings, pulse rules, visual ordering, catalog exhaustiveness.
- Preserve enough characterization coverage to detect accidental migration changes, but do
  not treat those tests as reasons to retain the behavior.

**Exit:** no new feature work is competing with the simplification, and every existing test
has an explicit role.

## Phase 1 — audit every normative statement against §1

Review `spec.md` §2–§6 and the Demonology catalog line by line. Mark each claim in a working
ledger as one of:

- **KEEP — §1:** directly required by the philosophy;
- **KEEP — platform:** required by a sourced client constraint;
- **CHOICE:** a product decision the author affirmatively wants;
- **HYPOTHESIS:** a plausible design awaiting play;
- **REMOVE:** an agent-created rule with no current job.

Apply a deliberately high bar to rules about:

- HIGH / MEDIUM / LOW / none and whether all four are needed;
- the separation among tiers, grades, cues, holds and registers;
- “value, not order” and other language that disguises actual prioritization;
- cue polarity, mandatory thresholds and the requirement that a cue have a client-owned
  half;
- mandatory silence coverage and declared-subject exhaustiveness;
- exact colors, alpha bands, pulse rates, midpoint behavior and phase rules;
- generic inactivity for uncataloged specs;
- bars as a required second surface;
- automatic sequences.

Do not edit code in this phase. Bring genuine product choices and any proposed change to §1
back to the author as a compact decision set.

**Exit:** every surviving normative rule has a named justification, and no disputed rule is
silently inherited by the rewrite.

## Phase 2 — rewrite the product spec around outcomes

Rewrite §2 onward so it describes player-visible outcomes before mechanisms.

### Required changes

- Keep §1 intact and make its precedence operational: a later section that conflicts with it
  is invalid without needing an elaborate routing rule.
- Replace §3.0's ontology with the smallest vocabulary needed to explain the currently chosen
  behavior. Move implementation terminology out of the product definition.
- State honestly whether tiers are an ordering. If they remain HIGH / MEDIUM / LOW, describe
  their actual player meaning without the “value, not order” loophole.
- Make the restricted-data rule simple: cap may branch on readable facts; sealed facts may
  feed presentation but never Lua decisions. Keep this as the primary code-enforced rule.
- Allow a useful visual hint to be driven entirely by readable information. A secret client
  channel is a capability, not a required half of every marker.
- Mark visual treatments and Demonology thresholds as provisional until flown.
- Remove automatic current-step/next-step sequences from the committed design. If sequence
  context still seems valuable, return it to `discussion.md` with the explicit test: does it
  inform a choice, or choose the next press?
- Reconsider bars as an independent experiment rather than something every tier/cue must
  automatically reuse.
- Replace “§3 is not re-opened” with the opposite lifecycle: early flights are allowed to
  revise §3 because that is what prototypes are for.

### Documentation reduction

- Keep `spec.md` for approved intent, `backlog.md` for work and status, and `notes.md` for
  dated outcomes.
- Keep `discussion.md` only for questions that require an author decision; strike speculative
  branches once the simpler choice is known.
- Keep `flight-reading.md` only for fields that still exist after the source simplification.
- Remove stale present-tense status from both `CLAUDE.md` files and replace it with a pointer
  to `backlog.md`.
- Re-derive or retire the two already-stale published artifacts; do not maintain explanatory
  artifacts for a model being removed.

**Checkpoint:** review the rewritten spec with the author before source deletion or behavior
changes begin.

## Phase 3 — reduce the catalog contract

Design the smallest catalog that can express the approved Demonology experience.

The default target is:

- catalog only the abilities cap enhances;
- no mandatory accounting for every CDM row;
- optional diagnostic reporting for unclaimed rows, not authoring failure;
- readable predicates may directly drive emphasis or markers;
- sealed values are represented only by the few client-evaluated bindings actually drawn;
- no legal schema form that silently renders nothing;
- no unimplemented vocabulary such as `talent` admitted in advance;
- no prohibition against a future form unless it protects §1 or a platform constraint.

Retain three-valued/unknown handling where game reads can refuse. Retain validation that
prevents a secret channel from entering a branch. Remove checks that merely enforce the old
ontology, including mandatory silence reasons and visual-policy constraints.

Prefer a small safe API over a general rule language. If a closed data format remains useful,
its vocabulary should grow from demonstrated catalog needs rather than anticipating every
future spec.

**Exit:** the Demonology catalog can be read without learning a miniature programming
language, and a straightforward hint such as “show a dot while Dreadstalkers are out” is
straightforward to author.

## Phase 4 — separate mechanics from opinions in the tests

Rewrite the pure tests into two visibly different groups.

### Engine guarantees

Use synthetic catalogs to test only stable mechanics:

- readable facts can drive output;
- sealed values never become branch inputs;
- unknown values fail safely and negation does not turn unknown into confidence;
- binding and transforms resolve deterministically;
- unsupported display bindings fail visibly rather than loading as inert behavior;
- the addon is inert when it cannot safely establish a result.

### Product characterization

Keep a small set of Demonology examples as change detectors, not universal correctness:

- label them as current hypotheses;
- do not assert that Tyrant, Grimoire or Hand of Gul'dan objectively belongs at a tier;
- delete examples as soon as their corresponding catalog choice is removed;
- do not require an arbitrary number of simultaneous HIGH entries.

Delete tests that require every tier to pulse, pairwise-distinct pulse rates, unique phase for
forty rows, midpoint treatment for ungraded entries, mandatory rings/veils, or other visual
choices not retained explicitly by the author.

**Exit:** a green suite means the addon obeys platform and engine contracts; it does not mean
an unflown gameplay opinion is correct.

## Phase 5 — simplify the visible treatment

Return to a static, legible baseline before adding motion:

- start with one clearly distinguishable emphasis treatment and one clearly distinguishable
  hold/context marker;
- avoid pulsing by default; add motion only when a specific play problem requires it;
- judge brightness, contrast, size and stock-proc interaction directly in game;
- treat alpha, color, blend mode, rate and size as tuning values, not invariants;
- remove any safety claim that has not been validated for the actual rendered surface. Use a
  conservative non-flashing design rather than unsupported threshold arithmetic;
- fix or abandon stock proc-glow suppression based on whether it materially improves the
  chosen treatment, rather than because §3.2 requires a particular mechanism.

Add complexity one variable at a time, with an explicit observed problem each addition
solves.

**Exit:** the base treatment looks good in a real pull without relying on animation or a
dense tier field to communicate its meaning.

## Phase 6 — re-author the Demonology pilot from play goals

Start with a deliberately small pilot rather than translating the old ten-entry catalog.
Candidate experiences to evaluate with the author:

1. Demonbolt: make the proc more or less prominent based on readable shard state.
2. Tyrant: show it as available and add simple readable context markers for relevant setup
   facts, without converting those facts into a single verdict.
3. One cooldown presentation: decide whether the CDM icon is enough or whether a separate bar
   materially helps.

Everything else begins absent. Add an ability only after stating the player problem its hint
solves. Use authoritative rotation sources for factual mechanics, but use play to decide
whether a hint is useful.

Do not infer correctness from a rule firing as written. A flight must answer both:

- did the mechanism display what was authored?;
- was the authored opinion helpful?

**Exit:** the pilot is small enough that every signal can be explained from §1 and recalled by
the player without consulting the catalog vocabulary.

## Phase 7 — fly qualitatively, then measure in support

For each iteration:

1. State the experience question before the flight: for example, “Can I tell that Demonbolt is
   available without it drowning out Tyrant context?”
2. Play first and record the player's report in their own terms.
3. Use captures to diagnose why the observed result happened.
4. Do not reinterpret or dismiss the player's report merely because a metric suggests a more
   elegant root cause.
5. Change one conceptual variable at a time where practical.

Occupancy, refusal rate and rendered-state duration remain useful diagnostics. None becomes an
acceptance quota unless the author deliberately adopts one after seeing repeated flights.

**Exit:** the captured evidence explains the play result, and the play result—not schema
symmetry—selects the next change.

## Phase 8 — close the migration

- Remove obsolete modules, vocabulary, tests and capture fields rather than leaving
  compatibility scaffolding for an unreleased design.
- Update `flight-reading.md` to the smaller live capture format.
- Collapse completed work into short entries in `notes.md` and `backlog.md` → `Done`.
- Verify the milestone table and `backlog.md` status agree.
- Confirm both `CLAUDE.md` files contain no independent status claim.
- Delete or archive this plan and route any remaining undecided product questions to
  `discussion.md`.

## Completion criteria

The simplification is complete when:

- every enforced product rule traces to §1, an approved author decision, or a sourced platform
  constraint;
- the code enforces Secret-Value legality without enforcing unearned visual or rotation
  doctrine;
- a gate-only hint is first-class;
- no supported catalog form silently draws nothing;
- no automatic next-action sequence remains in the committed design;
- mechanical tests and mutable Demonology opinions are clearly separated;
- the first useful Demonology experience has been flown and judged in game;
- the permanent documentation once again has five files with five jobs, not a growing process
  for routing around contradictions.

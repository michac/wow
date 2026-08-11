# Combat Assist Plus — simplification audit

Temporary execution artifact for `simplification-plan.md`. This records migration evidence,
decisions, and phase progress; it is not a product specification.

## Section 1 commitments

Recorded before reviewing the later design:

1. cap makes the Cooldown Manager more informative without trying to become a next-action
   decision engine.
2. cap respects Midnight's secret-value restrictions. Readable facts may drive Lua choices;
   sealed facts may be displayed through client-owned channels but may not be read back for
   branching.
3. Readable information is fair material for useful hints.
4. cap does not try to always present one best decision. Depending on the situation, one,
   several, or no options may deserve emphasis; there is no occupancy quota.
5. In descending preference, cap re-presents existing information, grades binary signals,
   and contextualises moments so the player remains the decision-maker.
6. An ability cap has an opinion about receives an emphasis level. Several abilities may be
   emphasized together, and the player chooses.
7. cap is opinionated rather than configurable. Incorrect gameplay opinions are fixed in the
   product rather than delegated to user-authored rules.
8. cap rides on and extends Blizzard's Cooldown Manager instead of replacing it.

## Phase 0 — baseline and test classification

### Frozen baseline

- Live source baseline: Combat Assist Plus v0.2.4 (`fc98cc8`), in sync with its release.
- Scope: Demonology / Diabolist only. Ten entries are authored; the captured build binds
  eight. Four cooldown bars are declared: Tyrant, Dreadstalkers, Grimoire and Implosion.
- Visible surfaces: a HIGH / MEDIUM / LOW animated ring, a no-tier veil, a count marker, a
  hold marker, cooldown bars and attempted stock-proc dimming.
- The first flown pull established that binding, ring, marker and bar paths execute. It also
  established five product/implementation failures: the field is saturated; the animated
  rings read as flickery candles and were wanted brighter; an unrelated transformed row stays
  emphasized; Tyrant's HIGH promotion is unwanted; and the stock proc glow remains dominant.
- The interpreted capture adds three implementation facts: E3 was emphasized for 98% of the
  pull; E1/E2's channel-backed grades cannot drive Lua alpha; and E8's cue was offered for
  96.7% of the time E8 was lit. It cannot say whether the sealed marker appeared.
- Expansion is frozen while this plan runs: no M3e, remaining M4 work, M5, new channel forms
  or second-spec work.
- Baseline command: `busted CombatAssistPlus/tests/spec` from the addon repo root.
  Result: **164 successes, 0 failures, 0 errors, 0 pending**.

### Test classification

The line ranges below partition all five existing spec files. A range marked mixed names the
individual exceptions, so every current test has a role without reproducing 164 test names.

| File and test range | Role now | Migration meaning |
| --- | --- | --- |
| `bars_spec.lua:31-49` | characterization / policy | Pins the current four-bar Demonology opinion and single-roster declaration. Preserve only until the bar decision and pilot roster are approved. |
| `bars_spec.lua:52-95` | mechanical | Order preservation, empty-roster behavior, bound-spell selection and visible `nobind` planning are reusable planning mechanics if bars survive. |
| `bars_spec.lua:97-115` | policy / taste | Pins tier reuse on bars and the rule that an opinion-less cooldown still gets a bar. Rewrite around the approved independent bar experiment. |
| `catalog_spec.lua:18-31` | characterization | Says the present Demonology table passes its current checks, has no estimate and names Shadow Bolt as floor. It describes this catalog, not engine truth. |
| `catalog_spec.lua:37-74` | mixed | Channel-in-branch and unknown-term refusal are mechanical Secret-Value safety. Banning `casts`, cross-entry `elapsed`, and gate-driven display is policy from the old ontology. |
| `catalog_spec.lua:76-86` | policy | Pins negation as part of the general rule language. Keep only if the smaller API needs it. |
| `catalog_spec.lua:94-190` | mechanical | Prevents permanently inert reads by validating entry-subject versus aura-subject forms. Retain in a smaller form for whatever bindings remain. |
| `catalog_spec.lua:197-207` | policy / latent defect | Exempts `talent` and other argument forms. `talent` is accepted by the schema but not wired by `Sense`; remove it rather than preserve this test. |
| `catalog_spec.lua:214-263` | policy, with one mechanical seam | Polarity, mandatory gate precondition, mandatory sealed channel, positive tier and thresholded-negative rules canonize the old cue model. Malformed/unsupported display bindings should still fail visibly. |
| `catalog_spec.lua:267-277` | policy | Pins estimate disclosure and the `elapsed` vocabulary. Remove if the smaller API has no estimate term. |
| `catalog_spec.lua:282-307` | mixed | Basic shape and known result names are mechanical. A separate ordered bar list is mechanical only if bars survive; refusing per-entry `bar` is API taste. |
| `catalog_spec.lua:317-365` | mixed | Entry resolution, choice-node `alt` binding and row-family disambiguation are mechanical. Exact dropped entries are characterization. Exhaustive silence coverage is policy and should not be an acceptance rule. |
| `catalog_spec.lua:373-414` | mixed | Read collection by actual subject is mechanical. The exact Demonology read set and absence of `elapsed` are characterization. |
| `tier_spec.lua:31-51` | characterization / policy | Pins Shadow Bolt as an unconditional LOW floor and Infernal Bolt's current shard opinion. |
| `tier_spec.lua:56-75` | product characterization | Pins the current Demonbolt proc/shard hypothesis, including MEDIUM/LOW labels and inverted grade. |
| `tier_spec.lua:79-91` | mixed | Independent verdicts for entries sharing a row are mechanical; the E5/E6 tier assignments are Demonology characterization. |
| `tier_spec.lua:96-123` | mixed | First-match evaluation and aura-key form are mechanical; apex/shard outcomes are current gameplay hypotheses. |
| `tier_spec.lua:129-169` | mixed | Cross-entry readable predicates, `this` resolution and unknown-safe negation are mechanical. Tyrant HIGH/MEDIUM and Grimoire HIGH opinions are characterization already contradicted by play. |
| `tier_spec.lua:173-216` | mixed | Withholding output on false/unknown input and passing sealed descriptors without reading them are mechanical. Positive/negative polarity, mandatory client half and the current E1/E2/E8 offers are policy/characterization. |
| `tier_spec.lua:219-224` | policy / characterization | Requires at least three simultaneous HIGH entries in a staged setup. Delete; it canonizes saturation rather than protecting principle (c). |
| `tier_spec.lua:236-333` | mechanical, with one policy meta-test | Three-valued reads, unknown-safe negation, inert-on-blind behavior and refusal counts are engine guarantees. The meta-test requiring every admitted vocabulary term to have a case preserves unused terms such as `talent`; scope it to the approved API. |
| `track_spec.lua:21-45` | mechanical | Binding, shared rows and aura-read filtering are stable engine behavior. |
| `track_spec.lua:50-101` | mechanical | Three-state readiness, edge handling, charge refusal, rebind reset and baseline seeding are stable mechanics. |
| `track_spec.lua:106-143` | mechanical | Aura presence, elapsed bookkeeping and combat state are mechanics; delete elapsed bookkeeping if no approved consumer remains. |
| `track_spec.lua:149-171` | policy / unused characterization | Cast counting exists only for automatic sequences. Remove with M5 unless an approved future feature needs it. |
| `track_spec.lua:177-198` | product characterization | Pins Tyrant promotion/demotion and the unconditional floor through the full Track-to-Tier path. Preserve only as temporary migration detection. |
| `track_spec.lua:201-238` | mechanical | Gate-health known/unknown accounting and subject attribution are stable diagnostics for retained readable predicates. |
| `treatment_spec.lua:24-49` | policy / taste | Pins four ordered states, brightness ordering, rings on all tiers, a veil on none, and higher-tier shared-row selection. None follows directly from §1. |
| `treatment_spec.lua:52-109` | policy / unsupported safety claim | Pins motion on every tier, distinct rates, exact trough semantics and unique golden-ratio phases. Delete for the static baseline; do not retain the pixel-area argument as a safety invariant. |
| `treatment_spec.lua:113-129` | policy | Pins continuous within-tier brightness, midpoint defaults and band clamping. Retain only if graded multi-level emphasis survives. |
| `treatment_spec.lua:133-157` | mixed | Nil-safe descriptor construction is mechanical. The no-tier veil, channel-grade passthrough and midpoint rendering are old-model policy. |
| `treatment_spec.lua:162-225` | policy / taste | Pins hold polarity, no tier effect, tier-colored cue ink and LOW/none exclusions. Rewrite for the approved marker vocabulary and static treatment. |
| `treatment_spec.lua:230-279` | policy / taste | Pins tier reuse on bars, resting-fill ordering and track contrast. Replace with characterization of the chosen bar experiment, if retained. |
| `treatment_spec.lua:292-322` | product characterization | Pins the current Demonology catalog as drawn, including floor, Dreadstalkers-over-Demonbolt ordering and hold behavior. Keep only as short-lived migration detection. |

The intended Phase 4 split is therefore clear: `Catalog` subject/register safety, `Tier`'s
three-valued evaluation, retained binding/transform mechanics and gate-health accounting are
engine guarantees. Exact Demonology outcomes move to a small explicitly provisional
characterization file. Visual constants, tier population, bar roster, exhaustive coverage and
automatic-sequence vocabulary do not belong in the mechanical suite.

## Phase 1 — normative-claim ledger

The ledger groups adjacent claims that have the same justification. “Platform” means a
current sourced client constraint; it does not endorse the product mechanism built around it.

### `spec.md` §2

| Claim | Classification | Reason |
| --- | --- | --- |
| Author-first, chosen defaults, no v1 settings panel | KEEP — §1 | Directly follows the opinionated-product commitment. |
| One spec at a time; uncataloged specs are inert | CHOICE | Sensible scope and safe failure, but not required by §1. |
| Must work in restricted combat, not only on a city dummy | KEEP — platform | The product is for combat and the restrictive environment bounds shipped behavior. |
| Quiet out of combat except setup | CHOICE | Product behavior, not constitutional. |
| Player-set single/AoE mode, macroable and persistent | CHOICE | A response to an unavailable input; the exact UI and “only opinion you set” rule need affirmative retention. |

### `spec.md` §3.0–§3.2

| Claim | Classification | Reason |
| --- | --- | --- |
| Four features plus one catalog, each separately deliverable | REMOVE | Milestone architecture, not a player-visible requirement. |
| HIGH / MEDIUM / LOW / none; first-match bands; grade only within a tier | CHOICE | A possible emphasis design, not implied by “grade” in §1. HIGH/MEDIUM/LOW are an ordering in actual use. |
| Treatment plus a separate hold treatment | HYPOTHESIS | A visual vocabulary awaiting play. |
| Cue must combine a Lua gate and sealed channel, carry polarity and never change tier | REMOVE | Blocks the requested readable-only Tyrant markers and is not required by the platform. |
| Separate graded/cued registers | REMOVE | Implementation ontology. The surviving rule is only that sealed facts never become Lua branch inputs. |
| Named floor and unconditional LOW behavior | CHOICE | A rotation/product opinion, not a §1 commitment. |
| Catalog/roster/entry/silence/sequence/subject terminology | REMOVE | Mostly implementation vocabulary; keep only words needed to explain approved behavior. |
| Gate/channel legality split | KEEP — §1 / platform | This is the constitutional enforcement boundary. Readable facts may branch; sealed values may only feed client-owned presentation. |
| Three-valued readable inputs; unknown fails safely, including under negation | KEEP — platform | Prevents refused reads from becoming confident recommendations. |
| Every opinionated icon continuously carries one of three levels | CHOICE | The chosen tier count and continuous coverage are not required by §1. |
| Sealed facts may drive presentation without Lua learning the result | KEEP — platform | Core legal capability; it need not masquerade as a computed tier. |
| “Tiers describe value, not order” and “LOW only when nothing above is lit” | REMOVE | The implementation ranks them and the player meaning is ordered. The euphemism obscures rather than resolves prioritization. |
| Never rank within a tier | CHOICE | A product boundary only if tiers survive. Principle (c) forbids always collapsing to one answer, not every local ordering. |
| Tier plus cue answer different questions; positive/negative polarity | HYPOTHESIS | Plausible display model, not earned by §1 or the first flight. |
| Own unprotected frames anchored to CDM rather than editing its texture | KEEP — platform | Current sourced implementation constraint. It belongs primarily in engineering docs/code, not the product vocabulary. |
| Exact colors, alphas, ranges, sizes, blend mode, pulse rates, `0.68` trough and phase stride | REMOVE | Tuning picks and unsupported safety arithmetic promoted to invariants. Return to a static baseline. |
| Ordered brightness ladder, ring-versus-veil none state, midpoint for ungraded, tier reuse on markers | HYPOTHESIS | Visual choices contradicted or left unanswered by first play. |
| A marker must not leak the offered state when the sealed result is absent | KEEP — platform | Required honesty for a client-decided marker; irrelevant to readable-only markers. |
| Veiled opinion versus completely bare silence | CHOICE | A semantic visual distinction, not constitutional. |
| Shared row draws the higher tier | CHOICE | Conflict-resolution policy; revisit after the catalog shrinks. |
| cap emphasis must be distinguishable from stock proc glow | KEEP — §1 | Grading availability is useless if the stock availability signal overwhelms it. The suppression mechanism remains a hypothesis. |
| Proc desirability may be graded from readable shard/proc facts | KEEP — §1 | A direct instance of principles (b) and the “grade” move. |
| Replace/dim stock proc treatment, use a fade, and assign current Demonbolt thresholds | HYPOTHESIS | Mechanism, visual taste and gameplay tuning all require play. |
| An uncataloged proc gets a plain treatment | CHOICE | Safe fallback behavior, not required by §1. |

### `spec.md` §3.3–§3.4

| Claim | Classification | Reason |
| --- | --- | --- |
| Automatically detect a sequence and mark current and next spells | REMOVE | Its practical effect is a next-action guide with no player choice/arming step; it crosses the product boundary. |
| Silent drop, layered sequence styling and automatic trigger details | REMOVE | Scaffolding for the removed automatic sequence feature. |
| A movable panel of curated cooldown bars | HYPOTHESIS | Valid independent experiment, not a required second surface. |
| Every bar reuses tier, grade and cues | REMOVE | Schema symmetry, not a demonstrated player need. |
| A bar counts down without an opinion | HYPOTHESIS | Reasonable baseline for a retained bar experiment, still subject to play. |
| Ready/none/empty-track bar styling and ordered fill rules | HYPOTHESIS | Visual choices; the document already admits their numbers were not judged. |
| Ordered bar roster in the catalog | CHOICE | Small API detail if bars survive; not product doctrine. |
| Bars are the home for crowded cues / channel-backed grades | HYPOTHESIS | A question to test, not a rule. |

### `spec.md` §3.5

| Claim | Classification | Reason |
| --- | --- | --- |
| Closed declarative vocabulary rather than arbitrary catalog code | CHOICE | A safety/maintainability option, but the present language is much larger than demonstrated needs. |
| The prose catalog is normative over Lua for product choices | CHOICE | Documentation process, not player behavior. Keep only if the catalog remains large enough to need two forms. |
| Applies-to, roster, entries, silences and sequences are mandatory catalog sections | REMOVE | Old ontology. Only enhanced abilities and any retained surface roster are needed. |
| First-match bands evaluated independently | CHOICE | Small engine design if multiple conditions survive. |
| Bands may name any declared ability; verdicts cannot be inputs; negation is general | CHOICE | Prevents one cheap priority-ladder form but still admits another. The smaller pilot should drive the needed predicate set. |
| Grade/cue cannot change a band; cue requires polarity, tier, gate and channel | REMOVE | Old ontology and the direct blocker for gate-only markers. |
| Threshold is mandatory for negative sealed cues | KEEP — platform / honesty | If a sealed countdown drives a hold marker, a permanent unthresholded marker would misstate the answer. Do not generalize this into a requirement on readable markers. |
| Exact gate vocabulary (`ready`, `affordable`, `proc`, `identity`, `auraUp`, `talent`, `mode`, `resource`, `combat`, `elapsed`) | CHOICE | Admit only terms required by the approved pilot. `talent` is currently unwired; `elapsed` and `casts` anticipate removed features. |
| Exact channel vocabulary and legal forms | CHOICE constrained by platform | Retain only client-evaluated bindings that a live renderer supports. A legal-but-`nodraw` form must not exist. |
| Prefer a channel over a readable gate whenever both exist | REMOVE | Principle (b) explicitly allows good hints from readable facts. Exact client display is a capability, not an automatic design preference. |
| Adding a term requires a sourced client fact | KEEP — platform | Necessary before branching on or displaying a new game value. |
| `casts == n` only in sequence triggers | REMOVE | No consumer remains after automatic sequences are removed. |
| Hidden-row distinction and visible diagnostic | HYPOTHESIS | Useful developer feedback, but not part of the player-facing product definition. |
| Every tracked row must be an entry or reasoned silence | REMOVE | Creates exhaustive work unrelated to what cap enhances. Unclaimed rows may be diagnostics, never authoring failure. |
| No catalog / unmatched build / dropped entry is inert in play | KEEP — §1 | Safe non-guessing behavior supports the opinionated per-spec design. |
| Five catalog checks | REMOVE except register safety | Keep malformed-shape, supported-binding and gate/channel legality checks. Drop exhaustive coverage, old cue ontology and estimate disclosure. Subject validation survives only where it prevents inert reads. |
| HIGH-at-once distribution is diagnostic, never a quota | KEEP — §1 | Consistent with principle (c), provided it remains support for play rather than an acceptance target. |

### `spec.md` §4–§6 and milestones

| Claim | Classification | Reason |
| --- | --- | --- |
| Never press, queue, macro-generate or act for the player | KEEP — §1 | Direct product boundary. |
| Never reduce to a bare next-button flag; every emphasis carries why and alternatives | CHOICE | Compatible with §1, but stronger than principle (c) and needs honest wording after sequences disappear. |
| Do not surface Assisted Combat | CHOICE | Product-positioning decision. |
| No WeakAuras-style configuration; ride CDM; supported specs only; Retail/Midnight only | KEEP — §1 / scope | Directly restates §1 commitments and approved scope. |
| Supersede Cooldown HUD and do not port its code | KEEP — §1 / project | Establishes the product boundary and source lineage. |
| Secret Values and combat-lockdown constraints | KEEP — platform | Sourced client constraints. |
| Two visual registers are required by Secret Values | REMOVE | The restriction requires legal data flow, not this display ontology. |
| Clean-slate implementation | REMOVE | Historical implementation choice, not current product behavior. |
| §6 tier count, cue budget, demotion visibility, missing-floor surface, second spec and prior-art questions | HYPOTHESIS | Keep only genuinely undecided questions after the simpler design is approved; none is a commitment. |
| Milestone ladder and check text | REMOVE from product spec | Work/status belongs in `backlog.md`; rebuild the ladder only around the approved product. |

### Demonology catalog

| Claim group | Classification | Reason |
| --- | --- | --- |
| Demonology / Diabolist applies-to and no Soul Harvester behavior | CHOICE | Pilot scope. |
| Spell IDs, row families, transforms, costs/cooldowns and readable/secret classifications | KEEP — platform / game fact | Retain only current sourced facts used by the smaller pilot; route client facts to the addon-dev KB. |
| Ten-entry roster | HYPOTHESIS | Evidence of the old design, not the minimum useful experience. Phase 6 starts with Demonbolt, Tyrant and one cooldown presentation. |
| E1 Tyrant always MEDIUM when ready, with readable setup markers | CHOICE | The player explicitly reversed the HIGH promotion and asked for markers. The marker representation remains in the decision packet. |
| E1's current HIGH promotion, channel grade and sealed hold cue | REMOVE | Contradicted by play, inert as a grade, and more complex than the requested context dots. |
| E2 Dreadstalkers HIGH plus 20-second hold cue | HYPOTHESIS | The cue over-fires for twelve seconds by the catalog's own account and has not been judged useful. Absent from the small pilot unless a stated player problem restores it. |
| E3 Grimoire current bands | REMOVE | The transformed state is decided to be none; the rest is not in the initial pilot. If restored, identity handling must be explicit or mechanically safe. |
| E4 Doomguard authored despite no bound row | REMOVE | Pre-authoring for a build not under test. |
| E5 Hand of Gul'dan bands/grade; E6 Ruination HIGH | HYPOTHESIS | Plausible rotation opinions, not needed in the small first pilot. Preserve as migration evidence only. |
| E7 Demonbolt proc/shard demotion and optional core-count context | HYPOTHESIS grounded in §1 | This is the strongest pilot candidate because it directly grades a stock binary proc using readable shards. Exact thresholds and treatment await play. |
| E8 Implosion MEDIUM plus HIGH count cue | REMOVE from first pilot | Its band and offer are saturated; the visible sealed result cannot be measured. Reintroduce only for a specific play problem. |
| E9 Power Siphon and E10 Shadow Bolt/Infernal Bolt floor rules | HYPOTHESIS | Current gameplay opinions outside the small pilot. Automatic unconditional floor behavior is not required. |
| Exhaustive silence list, including removed/passive/utility abilities | REMOVE | No player-visible job. Optional unclaimed-row diagnostics are sufficient. |
| Four-bar roster and tier/cue reuse on every bar | HYPOTHESIS | Replace with one independent cooldown-presentation experiment selected at the checkpoint. |
| Automatic Tyrant sequence and drafted opener | REMOVE | Crosses the current product boundary and has not been flown. |
| Catalog open questions O1–O8 | HYPOTHESIS or obsolete | Carry forward only questions still load-bearing for the approved pilot. Do not preserve them to justify the old language. |

### Source enforcement found during the audit

- `Catalog.lua` implements five checks plus shape rules. Only readable-versus-sealed
  register safety, unknown-safe shapes, subject forms that prevent inert reads, and
  supported renderer bindings have a durable job.
- `Catalog.GATES.talent` is admitted while `Sense` does not answer it. This is an explicit
  example of anticipatory vocabulary producing legal but inert behavior.
- `Overlay.slotFor` draws only positive thresholded `stacks` and negative thresholded
  `cooldownRemaining`; other accepted channel forms become `nodraw` instead of load errors.
- `Treatment.lua` encodes the unearned visual doctrine: ordered numeric ranks, exact hues and
  alpha bands, pulse rates, a `0.68` trough, golden-ratio phase stride, shared-row ranking and
  bar reuse.
- `Track` retains cast counting solely for the unbuilt automatic-sequence milestone.
- No sequence renderer exists yet, so removal is documentary plus dead-preparation cleanup,
  not a compatibility migration.
- No Python tool parses or validates the Combat Assist project documents. CAP's Python
  integration is operational only: `wowkb.addon` manages/syncs/releases the addon and invokes
  its Busted directory; `wowkb.capture` reads the standard capture format. The product-rule
  enforcement is in Lua validation and Lua tests. After Phase 4, the release runner should
  still run the suite, but that suite should enforce engine/platform guarantees rather than
  opinions derived from prose.

## Author decision packet — approved

The author approved the recommended packet by directing the plan to continue after the
checkpoint. Source still does not change until the Phase 2 rewrite is reviewed.

### A — Emphasis vocabulary

- **A1 — one emphasis plus context/hold (recommended):** an ability is emphasized or not;
  readable context markers and optional sealed markers explain why or when to wait. Demonbolt
  can vary the strength of that one emphasis from readable shards without inventing three
  named ranks.
- **A2 — retain HIGH / MEDIUM / LOW / none:** state plainly that these are ordered player
  priorities, keep only thresholds intentionally approved, and make every treatment
  provisional.

Consequence: A1 removes most tier ontology and prevents a dense field from becoming a weak
priority list. A2 preserves more current behavior but keeps substantially more schema and
testing surface.

### B — Markers and sealed data

- **B1 — readable-only markers are first-class (recommended):** a marker may be driven by a
  readable predicate. A separate optional client binding handles sealed values and may never
  feed Lua decisions.
- **B2 — every marker requires a sealed client half:** Tyrant's requested Dreadstalker and
  Grimoire dots remain impossible until a real client-owned channel exists.

Consequence: B1 implements principle (b) directly while preserving the actual security line.
B2 preserves the old cue definition at the cost of blocking an allowed and requested hint.

### C — Catalog scope and validation

- **C1 — catalog only enhanced abilities (recommended):** unclaimed CDM rows are optional
  diagnostics; no silence list. Reject malformed terms, sealed values in branches, and any
  display binding the renderer cannot draw. Remove unwired/unused `talent`, `elapsed` and
  `casts` vocabulary.
- **C2 — retain exhaustive entry-or-silence coverage and the closed future vocabulary.**

Consequence: C1 produces the small API this migration is for. C2 preserves authoring work and
legal-but-inert states unrelated to player experience.

### D — Automatic sequences

- **D1 — remove M5 and park sequence context as an open question (recommended):** any future
  proposal must explain how it informs a choice rather than selecting the next press.
- **D2 — retain only an explicitly player-armed sequence experiment.**
- **D3 — retain automatic current/next hints.**

Consequence: D1 cleanly restores the stated boundary. D2 leaves a narrower future path. D3
keeps the design the audit found most difficult to reconcile with “without telling you what
to press.”

### E — Visual baseline

- **E1 — static treatment first (recommended):** one legible emphasis and one legible
  context/hold marker; no default pulse. Colors, alpha, blend, size and stock-glow handling
  are tuning hypotheses judged in game.
- **E2 — retain animated tier treatments but unpin exact rates/trough/phase.**

Consequence: E1 directly answers the candle report and deletes unsupported safety arithmetic.
E2 keeps motion before a demonstrated player problem asks for it.

### F — Cooldown bars

- **F1 — one independent bar experiment (recommended):** use Tyrant as the pilot cooldown;
  it counts down independently and does not automatically inherit icon emphasis or markers.
- **F2 — remove bars from the pilot.**
- **F3 — retain the four-bar roster with shared tier/cue treatment.**

Consequence: F1 tests whether the extra surface earns its cost. F2 is the smallest product.
F3 preserves the old symmetry and the largest visual footprint.

### G — Initial Demonology pilot

- **G1 — Demonbolt + Tyrant + the F decision (recommended):** Demonbolt tests readable proc
  grading; Tyrant is available at one base emphasis with separate readable setup markers;
  everything else starts absent.
- **G2 — translate the current eight bound entries into the new API.**

Consequence: G1 makes every signal recallable and attributable to §1. G2 carries the current
saturation and gameplay-opinion load into the migration.

## Recorded answers

- **Tooling boundary:** the author is broadly in favor of removing tools that parse product
  docs and enforce their rules. The audit found no such CAP-specific Python tool. Carry this
  as the recommended direction: remove doc-derived policy enforcement from Lua
  validation/tests, while retaining operational Python tools and mechanical engine/platform
  tests. This does not concern the workspace-wide KB generators or provenance linters, which
  do not consume Combat Assist project docs.
- **A1:** one emphasis plus context/hold.
- **B1:** readable-only markers are first-class; sealed display bindings remain optional.
- **C1:** catalog only enhanced abilities and reject unsupported bindings; no exhaustive
  silences or anticipatory vocabulary.
- **D1:** remove automatic sequences and park any future sequence-context idea.
- **E1:** return to a static visual baseline.
- **F1:** keep one independent Tyrant-bar experiment.
- **G1:** begin with Demonbolt, Tyrant and that Tyrant bar.

## Phase 2 — permanent-document proposal

- [`spec.md`](spec.md) preserves §1 byte-for-byte and rewrites everything after it around the
  approved player-visible outcomes and safety boundary.
- [`backlog.md`](backlog.md) is again the only implementation-status source and carries the
  Phase 3–8 work in order.
- [`discussion.md`](discussion.md) now holds only the visual, proc-glow, marker-shape and bar
  questions that still require play or author judgment.
- [`notes.md`](notes.md) records the completed audit and documentation round without becoming
  a second status source.
- [`../CLAUDE.md`](../CLAUDE.md) and the addon's `CLAUDE.md` point to the backlog rather than
  asserting independent implementation status.
- [`demonology/catalog.md`](demonology/catalog.md) is labeled migration evidence until Phase 3
  replaces it alongside the catalog API.
- `flight-reading.md` remains unchanged in Phase 2 because it documents the capture format the
  current source still emits. Phase 8 reduces it after source and fields have actually changed.

## Phase log

- 2026-08-11 — Began Phase 0 and recorded the §1 commitments before reviewing the later
  design.
- 2026-08-11 — Completed Phase 0: synced the addon checkout, froze v0.2.4, ran the unchanged
  164-test baseline and classified every existing test group.
- 2026-08-11 — Completed Phase 1: audited `spec.md` §2–§6, the Demonology catalog, source
  enforcement and tests against §1. Paused at the mandatory author decision checkpoint.
- 2026-08-11 — Recorded approval of A1–G1 and completed the Phase 2 permanent-document
  proposal. Paused at the required rewritten-spec checkpoint before source migration.
- 2026-08-11 — The author approved the rewritten product spec. Completed Phase 3's source
  migration and Phase 4's mechanical/product test split. Built Phase 5's static border, two
  fixed readable dots, stock-glow coexistence baseline and independent Tyrant bar; paused for
  the separately authorized release and mandatory in-game judgment.

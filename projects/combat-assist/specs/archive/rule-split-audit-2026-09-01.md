# Combat Assist Plus — the rule ledger for the process/philosophy split

**Temporary migration artifact**, in the same class as `simplification-plan-2026-09-01.md` and
`simplification-audit-2026-09-01.md` beside it, and covered by the same sentence in the project `CLAUDE.md`: *these are
not additional product authorities.* Delete it or move it to `specs/archive/` once the surgery has
settled.

**What it is.** The merged output of the three doc sweeps that preceded the split (~809 rules,
~140 defensive caveats across `specs/` and the two `CLAUDE.md` files), reduced to the rows the
surgery actually acted on plus every PROCESS rule that survived because it names a gate. It exists
so that a rule cut on **2026-08-15** can be found again, with its old text and the reason, if its
absence turns out to cause a real mistake.

⚠ **Every `pattern-shelf.md` locator below is a historical address.** That file was dissolved on
2026-08-21 — its client evidence into `knowledge/addon-dev/`, its `R#` / `S#` namespace and the
single statement of *accepted is not drawn* into `authoring.md` → *The recipe index*. The rows are
kept as the record of where a rule or a copy stood on 2026-08-15, which is the whole point of this
ledger; none of them resolves today.

**The governing principles it was applied under.** Too loose is the correct failure mode; a rule
gets re-added *after* a dated mistake, never pre-emptively. BORDERLINE resolves to CUT. Worked
examples (the Havoc catalog + scenario walk) beat stated rules. Line numbers below are
**post-surgery** for surviving rules and **pre-surgery** for cut ones.

## The buckets

| Bucket | Meaning | Disposition |
| --- | --- | --- |
| **PROCESS** | where a thing is written, what a tool requires, what the client permits | stays; rewritten to name its enforcing gate where one exists |
| **PHILOSOPHY** | the self-imposed stance — chiefly "cap must not become a decision engine" | moved out of `specs/` to `.claude/agents/cap-conscience.md`, which runs post-release |
| **FACT-CAVEAT** | "this *client fact* is narrower than it looks" | stays, deduplicated to one statement + citations |
| **PHIL-CAVEAT** | "this *prohibition* is narrower than it looks" | cut with the stance it defends |

---

## 1 · The transmission mechanism (fixed first)

| Rule | Was | Bucket | Gate | Disposition |
| --- | --- | --- | --- | --- |
| "Section 1 wins over every detail below" + the next-action / useful-hint invalidation clauses | `spec.md:82-84` | PHILOSOPHY | none | **CUT.** Only the sealed-data clause survives, as `spec.md:76-79` — a narrow statement about the platform boundary. |
| "Section 1 is the constitution; later details are valid only while they remain downstream of it" | `CLAUDE.md:6-7` | PHILOSOPHY | none | **CUT**, replaced by the same platform-boundary sentence. |
| The sealed-data half of both | `spec.md` §3.6 | PROCESS | `Catalog.lua:140-145`, `Channel.lua:41-197` | **KEPT** and named as the one enforced line. |

## 2 · `spec.md` §1 rebuild

| Rule | Was | Bucket | Disposition |
| --- | --- | --- | --- |
| Tagline: "tell you more **without telling you what to press**" | `:12-13` | PHILOSOPHY | **REWRITTEN to describe** — "carry more of what you already know". It was the first thing every agent read and it re-derived the whole prohibition unaided. |
| Principle (a) — does not fight the secret restrictions | `:23-24` → `:24-27` | PROCESS | **KEPT**, now pointing at §3.6 as a platform fact and naming the code that holds it. |
| Principle (b) — freely uses non-secret information | `:25-26` → `:28-29` | PROCESS | **KEPT** unchanged. Permission-granting. |
| Principle (c) — "does not try to *always* present a single best decision" | `:27-31` | PHILOSOPHY + PHIL-CAVEAT | **CUT**, with both of its "this is distinct from…" caveats. |
| "How many are lit … is not a quota" / "convergence is the goal, not a banned single winner" | `:50-54` | PHIL-CAVEAT | **CUT.** |
| "Two tools, layered — convergence is the goal, not a violation" + "the line cap does not cross is a mechanism, not an outcome" | `:104-123` | PHILOSOPHY + PHIL-CAVEAT | **TRIMMED to the mechanism.** The emphasis/cue definition and the readable-fact rule survive; the defensive two paragraphs do not. |
| Three moves (re-present, grade, contextualise) | `:33-44` → `:31-42` | PROCESS | **KEPT.** They paint the vision and grant permission. |

## 3 · Borderlines WITH a gate — kept, and made to say so

| Rule | Now at | Gate — and which command holds it |
| --- | --- | --- |
| **Eye-direction by elimination** | `spec.md` §3.1, `render-shelf.md` Part 0.5 | `elimination_gate` in `capart.py` — **`check`**, not `build`. Reads as philosophy, *is* code. |
| A catalog form that loads and renders nothing is a defect | `spec.md` §3.2 | `cmd_check` gate 1c (`capart.py`) at shelf level; cited by `render-shelf.md` Parts 0.5 and 2 |
| At most one positive cue **per entry** | `render-shelf.md` Part 0.5 | `cmd_check` gate 0b |
| Every declared cue is worn by some scenario | `render-shelf.md` Part 0.5 | `cmd_check` gate 1c |
| Positive-cue pre-emption (pass 1 points at the press) | `render-shelf.md` Part 0.5 | `positive_gate` — `check` |
| The tint guard still has a subject | `render-shelf.md` Part 4 | `cmd_check` gate 0 + `assert_tintable` in **`build`** |
| Art declared `tint: "lane"` must measure neutral | `render-shelf.md` Part 4 | `assert_tintable` — **`build`** (one of only two things that stop a build) |
| Nothing in `verdicts`/`cues` may name anything in `lab` | `render-shelf.md` Part 7 rule 1 | `validate_lab_isolation` — **`build`** |
| The committed HTML and `Style.lua` match the shelf | `render-shelf.md` Part 0 step 4 | `cmd_check` gates 2 and 3 |
| **The veil is derived from cue polarity** | *retired 2026-08-16 with the veil itself* | gate 0c went with its subject. |
| **A positive cue ranks onto the corner** | `render-shelf.md` Part 1 | `cmd_check` gate **0d — NEW, added by this work.** Was prose claiming to be mechanical. |

## 4 · Borderlines with NO gate — cut

| Rule | Was | Bucket |
| --- | --- | --- |
| "cap never misrepresents availability" | `spec.md:193-194` | PHILOSOPHY |
| "must earn its screen space" (Tyrant bar; independent bar surface) | `spec.md` §3.3, `render-shelf.md` Part 1 | PHILOSOPHY |
| "the player surface does not claim exactness beyond availability" | `spec.md:256-257` | PHIL-CAVEAT |
| "A future sequence idea must first show how it informs a choice" + its parenthetical | `spec.md:401-405` | PHILOSOPHY + PHIL-CAVEAT |
| "must not turn provisional gameplay or visual opinions into platform rules" | `spec.md:426` | PHILOSOPHY |
| Tests-don't-encode-taste triplet | `spec.md:436-437`, `authoring.md:178-179` + `:181`, `CLAUDE.md:73-74` | PHILOSOPHY |
| **The two-consumer rule** — "generalise only after two consumers show the same shape" | `authoring.md:161-162`, `pattern-shelf.md:13-14`, `:323-325`, `:326-331` | PROCESS-shaped, unenforceable — its deciding half ("the same shape") admits no test. Four copies, cut in all four. |
| "no new test asserts a gameplay opinion" (a *stage exit criterion* with no test behind it) | `authoring.md:181` | PHILOSOPHY written as a gate |
| "a genuinely new marker shape" as the justification bar for a renderer edit | `authoring.md:160-161` | softened to a description of what a renderer edit *means* |
| "every row reads identically under both" (shared hero-tree doc) | `authoring.md:21-23` | softened; the "…unless Aldrachi Reaver" test is the operative half and stays |
| "Do not prebuild vocabulary" generalised past its four named things | `authoring.md:223-224` | the four concrete things stay; the generalisation to intent is cut |
| "Comprehensive … does **not** mean every button" | `authoring.md:65-66` | PHIL-CAVEAT (restates `spec.md` §3.7) |
| "Do not file a threshold as 'cap can't rank this'" | `authoring.md:96` | PHIL-CAVEAT; the expressibility *fact* stays |
| "not permission to guess and not a reason to stall the rest of the catalog" | `authoring.md:135-136` | PHIL-CAVEAT; the stop-and-ask stays |
| "convergence is the goal, not a violation" (catalog + contract boundary) | `havoc/catalog.md:49-53`, `:328-330` | PHIL-CAVEAT |
| "the §4 oracle, forbidden by choice, not a wall the restriction builds" | `spec.md` §3.1 + §3.7, `havoc/scenarios.md:181-184` | PHIL-CAVEAT; replaced by a plain statement of what the platform does not allow |
| "What keeps that inside `spec.md` §4 is not that the cue is passive…" | `render-shelf.md` Part 0.5 | PHIL-CAVEAT |
| "…would be a second voice in pass 1" scope defence, long form | `render-shelf.md` Part 0.5 | trimmed |

## 5 · Fact caveats — all kept, deduplicated

**"Accepted ≠ drawn" was stated eleven times across five files.** Eleven copies is drift waiting to
happen, not eleven insights. It was consolidated to **one** statement, in `pattern-shelf.md` Part 2
where sink behaviour was defined; the other ten cite it.

⚠ **Superseded 2026-08-21 as to WHERE, not as to WHAT.** `pattern-shelf.md` was dissolved into
`knowledge/addon-dev/` and `authoring.md`; the single home of *accepted is not drawn* is now
`authoring.md` → *Accepted is not drawn*, and the client fact under it is
`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1. The consolidation itself
stands — one statement, everything else citing it — and every `pattern-shelf.md` locator in the
table below is a record of where a copy *was*, not a live address.

| Copy | Was | Now |
| --- | --- | --- |
| the canonical statement | `pattern-shelf.md:234-236` | **the one home**, expanded to say it is the single statement |
| flight-reading header | `flight-reading.md:7-8` | cites Part 2, and says it applies to every field below without per-field repetition |
| `B{}` bar path | `flight-reading.md:81-83` | trimmed |
| `C{}` sealed channel | `flight-reading.md:84-85`, `:88-90` | trimmed to the distinct fact (`never a value`) |
| draw-stream reading | `flight-reading.md:127-128` | trimmed |
| Phase 9 checkpoint | `flight-reading.md:160-161` | left — it is an iteration instruction, not a restatement |
| anti-pattern | `pattern-shelf.md:360-361` | cites Part 2 |
| `spec.md` §6 | `spec.md:434-435` | cites Part 2 |
| `authoring.md` stage 8 | `authoring.md:194-195` | cites Part 2 |
| graded-vs-readable cue in `P{}` | `flight-reading.md:74-75` | **left as-is** — a different fact (which cues appear in which field), not a restatement |

Every other fact caveat — Secret Values per-power-type, `overrideSpellID` vs `GetSpellID()`,
`isActive` below full charges, `SetVertexColor` multiplies, `SetScaleFrom` not `SetFromScale`,
`RefreshSpellCooldownInfo` clobbering a one-shot restyle, SavedVariables flushing only on
`/reload` — **stays untouched**. These prevent real technical errors.

## 6 · Doc↔code discrepancies found by the sweep and fixed here

| # | Was | Truth | Fixed |
| --- | --- | --- | --- |
| 1 | `render-shelf.md` "these **ten** keys" | nine, per Part 0.5, `scenarios.md`, and the table itself | corrected in Part 2 |
| 2 | `render-shelf.md` Part 0.5 (twice) and `scenarios.md` "fails the build" | both gates are in `cmd_check` (`capart.py`), never `build`; Part 0.5 said so correctly a few lines earlier | all three now say `check` |
| 3 | `render-shelf.md` Part 4's base64 budget "a `check` concern" | it is a `_warn` in `cmd_build`; `cmd_check` never tests it | Part 4 table row rewritten |
| 4 | `capart.py` cited `spec.md:194-195` | the text had moved to `:200-201`, and this work renumbers further | all citations converted to **section** references (`spec.md` §3.2), which do not rot. Same for `render-shelf.md` Parts 0.5 and 2, and `scenarios.md` |
| 5 | veil "**DERIVED**… mechanical rather than a promise" and "slot 3 ⇔ positive polarity" claimed gates that did not exist | neither was checked | **made true** — two new assertions in `cmd_check` (0c, 0d), both passing on current tokens |

⚠ Discrepancy 2 caused a wrong statement in the session that produced this plan, which is why
stale process prose is treated here as a defect rather than a cosmetic issue.

## 7 · Where the philosophy went

`.claude/agents/cap-conscience.md`. It runs **after** a release is cut and deployed, holds
`Read`/`Grep`/`Glob` and no write tools, and asks one question: *is cap drifting back toward the
Cooldown HUD shape — a single channel that weighs the whole row into one answer?*

Its criteria never load into a planner's or implementor's context (a subagent's body does not
reach the parent; only its `description` appears in the agent listing, and that description carries
no criteria and discourages mid-work use). It cannot edit a file, there is no release left to
block, and its output is questions addressed to the author.

Explicitly outside its remit, because these three were the recurring misreadings: how many buttons
are lit, whether the press is obvious, whether a cue is positive or negative.

The post-release reminder is printed by `wowkb.addon release cap` (`tools/wowkb/addon.py`), after
the release is cut and deployed, so it structurally cannot gate anything. `authoring.md` stage 8's
exit names the review and **states no criteria** — putting them there would walk the philosophy
straight back into the doc it left.

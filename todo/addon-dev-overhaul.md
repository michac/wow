# addon-dev overhaul — KB accretion, consistency, and the wow-developer skill

**Opened 2026-08-05.** Working doc for a three-part cleanup: the `knowledge/addon-dev/`
KB, the `wow-developer` skill, and the addon code the skill produces.

This is a **work log** — dated entries belong here. That is the point: the KB files
themselves are supposed to stop carrying this material (see §1.5), so it lands here.

Findings below come from three parallel review agents run 2026-08-05. Numbers marked
**[verified]** were re-checked by hand against the tree; the rest are as reported.

---

## 0. The one-paragraph summary

`SKILL.md` is generating two of the three problems. Its *"note what the old claim was and
why it was wrong"* instruction produces the KB sediment; its *"treat a marked claim as a
hypothesis"* now tells the agent to disbelieve the KB's own in-client measurements. The
addon-side problems (narrative comments, probe sprawl, four capture formats) are the same
disease in Lua: **nothing in the system ever removes anything.**

---

## 1. KB — the accretion problem

### 1.1 Root cause, and it is written down as policy

`knowledge/addon-dev/README.md:224-228` **[verified]**:

> "the files carry an unusual amount of **visible self-correction**: inline
> `[corrected 2026-07-23]` notes saying what the earlier draft claimed and what the source
> actually says. That apparatus is deliberate. Do not clean it up — it is how a reader who
> saw an earlier version knows what to un-learn."

That licensed 59 "an earlier draft…" asides and 29 `[corrected]` tags. A second layer
accreted 07-30 → 08-04: dated CDMProbe capture diaries appended *below* base text the
capture falsified, with the base text left standing.

### 1.2 Scale

| Category | Bytes | Share |
|---|---|---|
| "what an earlier draft said" sediment | ~30 KB | 4 % |
| Dated session diary | ~46 KB | 6 % |
| Rules-section duplication | ~107 KB | 14 % |

Every *"Rules we could audit against"* section is a second copy of the body, and
corrections get applied to the two copies independently. **~25 % of the corpus is not a
claim.**

### 1.3 Wrong-base-text cases — the priority list

Cases where the base claim is now false and only a buried note corrects it. Grepping or
skimming returns the wrong answer. **These are the highest-value fixes in the whole doc.**

| # | Location | Defect |
|---|---|---|
| 1 | `api-events-and-discovery.md:628-648` **[verified]** | Base: `pandemicStartTime`/`pandemicEndTime` are "plain numeric fields an addon can read", called "one of the few routes to a tracked DoT's remaining duration". 11 lines below: measured `SECRET` in combat, `IsInPandemicTime` **throws**. Base untouched. |
| 2 | `security…:923-961` vs `:1374-1383` | §4.6 declares "three distinct outcomes" as alternatives and picks `SetText` as its (a) example. Finding 4 proves `SetText` does (a) **and** (b) at once. §4.6 never amended — following its own worked example produces broken anchoring. |
| 3 | `frames…:656-659` vs `security…:1385-1389` | `SetTexture` with a secret string: `frames` says accepts (docs read), `security` says the client **refuses** — *"Cannot set texture to a secret string value"* (measured 08-04). Security wins. The docs annotation is necessary, not sufficient. |
| 4 | `security…:631-635` vs `:1892-1904` | `table` in the secure-snippet env: §3.2 prose says deliberately excluded; rule 7 says `table.new()` **is** available and snippet-local storage works. Correction applied to the rule only. `mined-pending-verification.md:212` wrongly records this as fully applied. |
| 5 | `security…:1230` vs `:1246-1258` | Duration-sink table still reads ✅ "carries" under a correction explaining that exact reading shipped a 0 %-width bar for four builds. |
| 6 | `frames…:1409-1421` vs `module…:938-942` | Secure pool proxy: **eight** methods or **nine**? `frames` is right (`GetTemplate` bolted on at `Pools.lua:539`); `module` carried the pre-correction number through its own 08-05 review. |
| 7 | `api-events…:584` vs 3 other files | `item:IsActive()` cited as positive evidence of a readable-in-combat channel; three files call it a constant `true` and *"ACTIVELY MISLEADING"*. api-events is the outlier. |
| 8 | `cooldown-manager.md:525` | Opens *"The entire `AuraData` record is secret when restricted"* then immediately *"⚠ But … was too strong — CORRECTED 2026-08-05"*. First sentence is what a table scan returns. |
| 9 | `anatomy…:283-293` vs `:221` + `sources.md:96` | 08-05 mined note claims `## Category:` is "a real, addon-facing field this file did not carry" — the file *does* carry it (`:221`), and `sources.md` counts one occurrence in the shipped corpus. Also filed under §2.3 **"Restricted directives — do not use them"**, inverting its meaning. |
| 10 | `security…:1241-1242` | Cites *"§4.9's 'aura data is wholly sealed in combat'"*. §4.9 is "Communication and combat log" and contains no such sentence. Dangling. |
| 11 | `api-events…:650` | *"So the earlier hypothesis (b) is what happens"* — no (a)/(b) list exists in §2.8. Dangling. |
| 12 | `security…:1315-1318` | §4.8.1 correcting itself three findings later; the channel table at `:1222-1235` still reflects the pre-correction model. |
| 13 | `security…:1237-1407` | Findings numbered **1, 9, 10, 11, 12, 13, 14, 2, 3, 4, 5, 6, 7**. Finding 8 does not exist. Accretion visible in the ordinals. |

Minor drift also logged: oUF 784 K vs 504 K, LibDataBroker 40 vs 90 lines, EllesmereUI 18
vs 20 modules, 592 vs 593 doc files, README's rule census says 204 and counts to 200.

### 1.4 The stale epistemics — biggest single item

`README.md:40` and `SKILL.md:66-69` **[verified]** both assert *"Nothing in the seven topic
files has been executed in the client"*, and SKILL.md turns it into an instruction:
**"Treat a marked claim as a hypothesis, not a fact."**

False since at least 07-30. `security…:1201` **[verified]**: *"This subsection is the first
thing in this file that was RUN"* — `/cdmp curve`, CurveLab v0.32.98, Havoc DH. Also
measured content in `api-events` (§2.8, §2.9) and `frames` (§5.7). The files contradict
themselves: `security…:1828` **[verified]** still lists *"[gap] Nothing here has been
executed in the client."*

**Consequence:** an agent obeying SKILL.md discards the measured facts CDMProbe is built
on — that `SetTexture` refuses a secret, `SetColorTexture` poisons the anchor chain, and
`FormatRemainingDuration → SetText` is the one confirmed-rendering route.

**Fix:** the "never run" property is dead. Replace with the `[client]` marker convention
`cooldown-manager.md:44-47` already defines, applied subtree-wide.

### 1.5 The prophylactic rule (proposed README §7)

> **A topic file states what is true now. It never states what it used to say.**
>
> 1. Correcting a claim means **rewriting the claim** in place. If a reader can get the
>    wrong answer reading top-down or grepping one line, the edit is not finished.
> 2. History goes in **one line** in a `## Changelog` at the bottom, or nowhere. Cap 2 KB /
>    20 entries. Longer belongs in `projects/<addon>/docs/`.
> 3. A measurement is a claim plus a `[client YYYY-MM-DD]` tag, not a story. One sentence of
>    method if load-bearing. Spec, build, what we tried first → project docs.
> 4. Dates appear in exactly four places: front matter, a citation stamp, a `[client]` tag,
>    the Changelog. **A date in prose is a defect.**
> 5. No numbered "findings" list in a reference body — merge each into the section it amends.
> 6. A claim is scoped to the API, not the call site.
> 7. Unsettled findings go in a queue file, not a topic file. A topic file asserts; a queue
>    file asks.

**CI gates** (proposed `wowkb.kblint`), current hit counts:

| Gate | Checks | Now |
|---|---|---|
| 1 | No retrospective prose outside a `## Changelog` | ~105 |
| 2 | Every date in front matter / citation / `[client]` / Changelog | ~380 |
| 3 | No section corrected by a later part of the same file | ~30 |

Driving these to zero *is* the burn-down; the gate then keeps them there.

### 1.6 Per-file verdicts

| File | Verdict |
|---|---|
| `README.md` | **Surgery first** — root cause. Delete `:224-228`; cut §5 (4.9 K meeting minutes); compress §3. |
| `security-taint…md` (122 K) | **Split or regenerate §4.8 subtree** (18 K). See §1.7. |
| `api-events…md` | Surgery + move §2.8–2.9 (20.9 K, 22 %) to `cooldown-manager.md` per README's own partition contract |
| `frames…md` | **Mechanical strip pass** — good prose, 29 `[corrected]` barnacles. Not regeneration; provenance is dense |
| `libraries…md` | Strip pass; delete the 3.4 K "Adversarial verification pass" Was/Is table at `:51-94` |
| `module-architecture.md` | Strip pass; `§1.1a` style advice moves out |
| `anatomy-and-runtime.md` | Light in-place |
| `state-persistence…md` | **Healthy** — proof the corpus can be written this way |
| `sources.md` | Healthy but **13 days behind its consumers** — no registry entry for EllesmereUI (cited in 5 files' front matter, clone deleted), no evidence class for in-client measurement |
| `cooldown-manager.md` | Restructure §7/§9 only. §0 scope statement is the best-written thing in the corpus |
| `mined-pending-verification.md` | **Healthy — this is the template** |
| `12.1.0-ptr-heads-up.md` | Healthy; dated by design |

The two healthiest files are the two newest, and both were written with an **explicit
contract about what belongs in them.** That is the lesson.

### 1.7 Open decision — the security file

Three reviews, three framings of one item:

- Regenerate §4.8 from the pinned `wow-ui-source` checkout + CurveLab captures (loses only
  chronology, which belongs in project docs)
- **Extract** §4.8–§4.12 into `displaying-secret-values.md` that declares itself
  run-in-client at the top
- Fly CurveLab once more, drain it, delete it — the answers land, the 2,857-line file goes

These are compatible: **fly → drain into a new extracted file → delete CurveLab.** All of
it is gated behind the Havoc flight `projects/cooldown-hud/docs/status.md` already owes.

### 1.8 Two files are unreachable from the index

`grep 'mined-pending\|ptr-heads' README.md sources.md` → **0 hits** **[verified]**.
SKILL.md routes to "§1 topic map … seven topic files plus `sources.md`", so an agent
following the documented route never learns the staging queue or the patch-day list exist.

### 1.9 The `@verify-ingame` firewall has leaked

README `:393-403` says 64 of 68 markers are backticked so the generated checklist lists
**zero** addon-dev items — deliberately, so nobody asks a player at an obelisk to test
`table.freeze`. Actual: **81 markers** **[verified]**, and `_meta/verify-in-game.md`
carries addon-dev items across five files. Re-backtick or drop the claim; do not document
it as intact while broken.

### 1.10 Gaps — topics nothing covers

Frame attributes as a general mechanism · the **`Cooldown` widget** (the thing CDMProbe
exists to skin) · **`StatusBar`** · ScrollBox/ScrollUtil · slash-command registration (how
all three addons are driven) · **keybindings** (BucketBinds' entire subject) · tooltips ·
**`busted`/offline testing** — which SKILL.md promises as a capability the KB never
documents · no evidence class in `sources.md` for a deleted-clone source · no doctrine for
`patch:` values *ahead* of live.

---

## 2. The addon code

### 2.1 Measured

| Addon | files | code | comment | ratio |
|---|---:|---:|---:|---:|
| **CDMProbe** shipped | 31 | **7,911** | **8,321** | **1.05** **[verified]** |
| CDMProbe `tests/` | 30 | 11,275 | 3,867 | 0.34 |
| BucketBinds | 7 | 3,683 | 568 | 0.15 |
| PlannerState | 2 | 417 | 151 | 0.36 |

CDMProbe ships more comment than code. **This is a CDMProbe pathology, not workspace-wide**
— the rules held on the two small addons and failed on the one that got big.

- 263 comment blocks (23 %) carry a history marker; being the long ones, they are **4,293
  lines = 52 % of all comment lines**
- In comments: `⚠` 551 · ISO dates 132 · `Phase N` 142 · "used to" 56 · version numbers 18
- Longest blocks: `SpecHavoc.lua:1` (**101 lines**), `CurveLab.lua:1` (80),
  `SpecRetribution.lua:1` (72), `State.lua:360` (66)
- Worst ratios: `CoachHavoc.lua` **2.98** · `CoachRetribution.lua` 2.06 · `HudLayout.lua`
  1.82 · `State.lua` 1.40 but the largest absolute mass (1,416 comment lines)

### 2.2 Dead code shipped to the client

**4,070 of 17,178 shipped lines (24 %) load on every login** **[verified]**:
`AlertTape.lua` 332 · `Assist.lua` 235 · `CurveLab.lua` 2,857 · `RenderTest.lua` 646.

The `rtfx` case is the clearest **[verified]**: `Core.lua:53` still seeds the
SavedVariables key and `Core.lua:50` still says *"Read by `wowkb.cdmp rtfx`"*, but the only
writer is in `archive/` (not in the `.toc`) and `cdmp.py:954` admits the reader was deleted
2026-08-02. **The comment is the only thing keeping a dead key alive, and it is lying.**

### 2.3 A fact that exists only in a comment

`State.lua:377-378` — *"`ChargeGained` IS NOT '+1 CHARGE'. Corrected 2026-07-31 after a
live pull where Conflagrate won 702 of 1272 decisions and was cued while genuinely on
cooldown."* A measured, in-client fact about a Blizzard alert event, recorded **nowhere
else**. Delete CDMProbe and it is gone. This is the case for `observations.md`.

### 2.4 Command surface

**CDMProbe** — `/cdmp curve` alone has **19 invocations up to 4 tokens deep** behind a
hand-rolled recursive-descent parser whose ordering hazards are documented in-code
*because they were bugs* (`CurveLab.lua:2696, :2712, :2727`).

**Substring dispatch** (`rest:find("on")`) is used in `hud`, `assist`, `flight`, `curve`,
`aoe`. `HudDriver.lua:512`: *"`sound` IS MATCHED FIRST, and it has to be … 'sound on'
contains 'on'"* — a latent bug generator, three times realised.

**BucketBinds already solved this**: 14 commands, all depth ≤ 2, declared in **one schema
table** (`Core.lua:210`, `{name, args, desc, handler, complete}`) that drives help,
did-you-mean (Levenshtein, `:301`), tab-complete and the console dropdown for free. **Zero
hand-rolled parsing.** Copy the addon we already got right.

Verdicts: `alerts` **DEAD** (its own docs say the rules landed) · `assist` **DEAD** (235
lines, nothing reads it) · `rt pop burst <knob> <value>` **DEAD** (dialling is over) ·
`curve` experimental-still-needed until §1.7 resolves · `flight` **LIVE and correctly
designed — the model to follow.**

### 2.5 Capture surface — 7 stores, 4 retention policies, 3 destinations

| Store | Written by | Retention | Read by |
|---|---|---|---|
| `decisionlog` | always-on | 6 sessions, cap 5000 | `wowkb.cdmp decisionlog` |
| `alerttape` | `/cdmp alerts on` | 3 sessions | `wowkb.cdmp alerttape` |
| `assist` | `/cdmp assist watch` | dedup, unbounded-ish | **chat only** |
| `curvelab` | `/cdmp curve watch` | dedup by verdict | `wowkb.cdmp curvelab` |
| `flight` | `/cdmp flight` | cap, **wiped on arm** | `wowkb.cdmp flight` |
| `rtfx` | **nothing** | — | **nothing** |
| `virtualPanel` | UI | settings | — |

Plus chat-only outputs (`/cdmp hud layout`, `hud coverage`, `alerts probe`,
`/bb diagnostics`). `AlertTape.lua:220-224` already records the lesson, learned once and
never generalised: *"an earlier cut printed it to chat only, which was useless: WoW's
default chat frame has no copy/paste, so the one output that has to reach the analysis
machine was the one output that could not leave the client."*

Python side: `cdmp.py` (1,023 lines) has **four near-identical loaders** (`:84`, `:200`,
`:314`, `:525`) plus two dead functions (`_fmt:935`, `_rtfx_cues:945`) **[verified]**.

### 2.6 Test triage

**28 spec files, 964 `it()`, 16,600 lines** — 1.42:1 against shipped code.

| Action | Files | Δ |
|---|---|---:|
| **DELETE** with their probes | `curvelab_spec` (1,143 lines, tests a file whose header says delete me, against fakes of an API nobody validated), `assist_spec`, `alerttape_spec` | **−72** |
| **REWRITE** | `renderer_spec` 73 → ~12 (keep the two-term cull union + the mutation-checked "no animated ancestor of a rotating texture"; drop token→texture mappings) | −60 |
| **TRIM** | `hudvirtual_spec` 40 → ~25 | −15 |
| **CAP** | `harness_spec` 34 → ≤15 (keep only stubs whose breakage makes a real branch unreachable — the `issecrettable`-hardcoded-`false` class of bug) | −19 |
| **KEEP** | 4 coach APL oracles (350), `state_domainview` (129), `cdm_cases` + 107 fixtures, `flight_spec`, 15 pure-module specs | — |

964 → ~800; Coach share **36 % → 44 %**. The suite is not bad — **nothing ever removes
anything from it**, so its signal is diluted by exactly the experimental code that should
already be gone.

Two patterns already right here and worth making doctrine everywhere:
- `fixtures/cdm-cases.lua` is authored **from the KB**, and a meta-test *forbids* a case's
  `ref` pointing at `State.lua`. A test authored from the implementation is a
  change-detector wearing a contract's clothes.
- `status = "pinned-defect"` cases assert the contract answer and **fail on purpose**, so
  the fix flips its own case green in the same diff.

---

## 3. Decisions taken

### 3.1 How the standards ship — vendored, not a dependency (2026-08-05)

**No dependency tree, no shared library, no example addon.**

WoW has no package manager. The options are a separate addon the user must install
(fragile: load order, `## Dependencies`, a release per change across three repos) or
embedding — and embedding *is* vendoring. Ace3/LibStub work this way for this reason. An
example addon is worse: a fourth addon nobody runs rots immediately, which is the dead-code
problem in new clothes.

**The seam:**

| Layer | Contract |
|---|---|
| SavedVariables shape (`<DB>.captures.<stream>`) | **HARD** — identical across all three addons |
| `Capture.lua` internals, function names, ergonomics | **SOFT** — copy and adapt |
| Dump panel UI, layout, which buttons | **SOFT** — whatever fits the addon |

**Enforcement is free:** `wowkb.capture` is the only reader. Write the wrong shape and it
fails loudly the first time you read a capture. No lint, no CI gate, no drift check — the
consuming tool is the test. "Slightly different implementations maintaining the spirit" is
right for the Lua and wrong for the format; the seam just has to be drawn there.

### 3.2 Verified-vs-experimental — file location, not annotations (proposed)

Per-function "verified" annotations are the disease, not the cure: they are prose, prose
drifts, and `Core.lua:50` is the receipt. **`ls` cannot lie**, so location is the marker:
`<Addon>/` shipped · `<Addon>/probes/` experimental with an expiry · `<Addon>/archive/`
out of the `.toc` and out of grep (already exists, keep it).

One genuine exception, because it is per-claim not per-file: **`--@unverified`**, the
code-side twin of `@verify-ingame`, with the rule that every one must appear in the current
flight's acceptance set. An unverified path nobody will fly is either dead or a lie not yet
caught. (Havoc's deliberately-unshipped napkin fix is exactly this and currently exists
only as 12 lines of prose no tool can see.)

Rejected: a `VERIFIED = {…}` manifest, confidence levels in comments, per-function
decorators.

### 3.3 Code-review mode — a slash command (proposed)

`.claude/commands/addon-review.md`, **not** a new skill (would contest triggering with
`wow-developer`, whose description already says "or reviewing Lua") and **not** a mode of
the skill (which must stay small enough to read every session). Every checklist item is a
grep or a CLI call. **It must not auto-fix comments** — deleting one can destroy the only
surviving record of a measured fact, so the fix is always *move*.

---

## 4. Plan

Chosen start (2026-08-05): **write the new standards first**, additively, breaking nothing.

### Phase 1 — the standards ✅ DONE 2026-08-05

- [x] `.claude/skills/wow-developer/references/capture-and-dump-standard.md` — the
      wire-format contract. **Placed in the skill, not the KB**: the KB is descriptive
      (facts about WoW), a house standard is normative. Keeping the firewall the
      consistency review praised.
- [x] `tools/wowkb/capture.py` — the single reader. Tested against all three addons;
      the per-character SavedVariables path branch was load-bearing (PlannerState uses
      `SavedVariablesPerCharacter` and resolves nowhere without it)
- [x] `Capture.lua` in CDMProbe — ratio 0.21, luacheck clean
- [x] `DumpPanel.lua` + `Dumps.lua` — ratio 0.07 / 0.11, luacheck clean. Wired: `.toc`,
      `DEFAULTS` (`captures`, `dumpPanel`), `/cdmp dump`. Two dumps registered
      (`layout`, `coverage`). Full suite green: **1081 / 0 / 0 / 4 pending**
- [x] `knowledge/addon-dev/observations.md` + `wowkb.obs` (list / check / drain) — seeded
      with 4 entries, all `open`
- [x] `references/house-rules.md`, `.claude/commands/addon-review.md`, new `SKILL.md`
- [x] `README.md` §7 (the current-state rule) + §1.2 (the queue index) + the evidence-class
      block replacing the dead "nothing has been run in the client" property

⚠ **Sequencing correction made during the work:** the original plan said port `decisionlog`
first as the proof. That is the *risky* one — it is the live instrument and a cutover
strands existing captures. The **dump stream is new**, so it proves `Capture.lua`
end-to-end at zero migration risk. `decisionlog` migrates during the fly-drain-cutover.

⚠ **Gate calibration fixed:** the three queue files and `sources.md` are inherently dated
(a queue entry *is* a dated event; a registry row is "what was on disk, when"), so Gate 2
exempts them. Without that it cried wolf on its own new files.

### Phase 1b — KB cleanup fan-out (plans written, awaiting review)

Plans in `todo/kb-cleanup-plans/`. **Six agents, not seven**: `api-events` and
`cooldown-manager` share an owner because §2.8–2.9 transfers between them and two
independent agents would duplicate or drop it.

| Agent | File(s) | Gate 1 | Gate 2 | Gate 3 |
|---|---|---:|---:|---:|
| 01 | `frames-textures-animation.md` | 32 | 49 | 0 |
| 02 | `libraries-and-ecosystem.md` | 19 | 67 | 0 |
| 03 | `module-architecture.md` | 12 | 12 | 1 |
| 04 | `anatomy-and-runtime.md` | 2 | 19 | 3 |
| 05 | `api-events-and-discovery.md` + `cooldown-manager.md` | 8 | 50 | 2 |
| 06 | `security-taint-and-restricted-data.md` **(§4.8–§4.12 FROZEN)** | 17 | 28 | 4 |
| — | `README.md`, `sources.md` | held centrally (me) | | |

Corpus baseline: **Gate 1 = 94 · Gate 2 = 273 · Gate 3 = 11.**

**§4.8–§4.12 of the security file is frozen for everyone** — it is the only run-in-client
evidence, it needs a rewrite rather than a strip, and its resolution is gated behind the
Havoc flight.

### Phase 1b — RESULT ✅ 2026-08-05

**Gates: 94 / 273 / 11 → 3 / 26 / 4.** Everything remaining is accounted for:

| Remaining | Where | Why it stays |
|---|---|---|
| 3 / 12 / 4 | `security` §4.8–§4.12 | **frozen** — catalogued, gated behind the Havoc flight |
| 6 | `libraries` | evidence dates: clone commit pins, the WoWInterface-vs-upstream staleness contrast |
| 8 | `state-persistence` | wiki `lastedit` / commit-pin citations that wrap across lines |

Integrity held: **876** tier tags, **144** `[gap]`, **84** `@verify-ingame`, **42**
`[client]`. No citation class shrank. Corpus 772 KB.

**The gate itself was wrong three times**, each caught by an agent rather than by me:
1. It flagged `## Changelog` entries — the very thing §7 rule 2 *mandates*. Caught
   independently by agents 03, 04, 05 and 06.
2. It had no legal form for an external event's date (a bug filed, a repo pushed, a wiki
   `lastedit`), so agent 03 **degraded three real citations** to satisfy it before
   escalating.
3. Its filename qualifier didn't allow a closing backtick, so a cross-file pointer read
   as a self-correction.

That is why the three greps became `tools/wowkb/kblint.py`: a grep cannot tell a
front-matter continuation from prose, cannot skip a fenced code block (so README §7's own
gate definitions matched themselves), and cannot tell `foo.md §4.6` from `§4.6`.

**What the agents found that the plans did not:**

- **The 2026-07-23 "adversarial pass" shipped wrong locators as tightenings.** Agent 02
  verified three against source — LibSharedMedia's dup-key early-out is `:264-267`, not
  the pass's `:265-268` — and in each case *the original text was right*. I re-verified,
  then warned agent 05 mid-flight; it re-checked every claim that pass touched in
  `api-events` and found them all correct, so this is not corpus-wide.
- **`RequiresNonSecretAura` declares no `FailureMode`** (one of only two Preconditions
  that don't), so `cooldown-manager`'s "silent absence" was an inference wearing Tier-1
  clothes. Found by agent 06, verified centrally, relayed mid-flight to agent 05, which
  found a further Tier-1 caveat neither had: all three getters *also* carry
  `SecretWhenUnitAuraRestricted`.
- **My plan was wrong about which getters carry it** — agent 06 checked rather than
  transcribing.
- **The animation `NotAllowed` set is 10 entries across 13 doc tables**, not "seven across
  five" — agent 01 caught that the old text contradicted itself in the same paragraph,
  and flagged the value change rather than making it silently.
- **The dead "nothing has been run in the client" claim had four homes**, not two: README,
  SKILL.md, `frames` §"Build skew" + gap 16, and `security` §6.

**Central pass (mine):** README §5 deleted (84 lines of meeting minutes); the brittle
204-rule census replaced with the reason no census is kept; §6's stale firewall numbers
corrected to the true 84 markers / 13 bare; §0's `[client]` file list replaced with a grep;
`sources.md` LDB 40→**90** lines, 593→**592** doc files, `Category` reframed as
addon-facing, EllesmereUI's contested count removed; `state-persistence` (unassigned —
review 1 called it healthy, and it was: exactly 2 asides) stripped; `gen_verify` re-run
once at the end, as every agent correctly insisted.

### Phase 0 — free wins (~1 hour, reversible, no game session)

Deferred by choice, not dropped:
- [ ] Delete `rtfx` key + `DEFAULTS` entry + `_fmt`/`_rtfx_cues` in `cdmp.py`
- [ ] Delete `AlertTape.lua` + spec + `.toc` line + store + Python subcommand — **drain its
      comments into `api-events…` §2.8 first**, that is where its value is
- [ ] Delete `Assist.lua` + spec + stores

### Phase 2 — the ratchet (ongoing, no deadline)

- [ ] `wowkb.addon lint --comments`, warn-only on `--patch`
- [ ] Comment drain **file by file as touched**. ⚠ **Not a big-bang sweep** — a mass comment
      deletion is unreviewable and will destroy facts. ~60 % delete (changelog), ~40 % move
- [ ] Test triage per §2.6

### Phase 3 — breaking changes (needs a decision each)

- [ ] CurveLab: fly → drain → delete (§1.7)
- [ ] `/cdmp` → schema table. ⚠ **Breaks macros** — `aoe`/`single`/`multi` are explicitly
      macro-friendly and likely bound. Needs an alias shim or an explicit go-ahead
- [ ] Retire old SavedVariables keys. ⚠ **Fly, drain, then cut over** — a pre-cutover
      capture is unreadable by the new extractor, the same one-way door that cost the
      v0.32.36 re-fly

### The KB work (§1) — not yet scheduled

Sequencing note: the doctrine fix (§1.5) and the SKILL.md epistemics fix (§1.4) are the
same edit and should land together, since SKILL.md is what generates the pattern.

---

## 5. Log

- **2026-08-05** — Three review agents run (accretion / consistency / skill). Findings
  captured here. Decided: vendored standards with a hard wire format (§3.1). Started
  Phase 1.
- **2026-08-05** — Phase 1 complete: the capture/dump standard, `wowkb.capture`,
  `Capture.lua` + `DumpPanel.lua` + `Dumps.lua`, `observations.md` + `wowkb.obs`,
  `house-rules.md`, the SKILL.md rewrite, `/addon-review`, and README §7 + §1.2.
  The two SKILL.md instructions that were *generating* the KB problems are gone: "note
  what the old claim was and why it was wrong" (produced the sediment) and "treat a marked
  claim as a hypothesis" (told the agent to disbelieve its own measurements).
  Phase 1b plans written for six parallel agents; **stopped for review before dispatch.**
- **2026-08-05** — Phase 1b dispatched and landed. Six agents, gates **94/273/11 →
  3/26/4**, all residue either frozen or load-bearing evidence dates. `wowkb.kblint`
  written after the grep-form gate produced three classes of false positive. Central
  pass done: README §5 cut, censuses de-brittled, `sources.md` drifts fixed,
  `state-persistence` swept, `gen_verify` re-run, OBS-001 drained into
  `cooldown-manager` §5.3.

## 5b. The curve freeze was wrong — CLOSED 2026-08-05

**I froze §4.8 for the wrong reason and should have checked before writing it into six
agent plans.** The freeze rested on `docs/status.md` saying `/cdmp curve` was *"shipped
v0.32.97, owed a flight"* — but the work then ran through **v0.32.118** on 2026-08-04 with
live in-game validation, and the doc never caught up. I also conflated it with the **Havoc
flight**, which is real, still owed, and about rotation features (charge-cap gate, amp
window, look-ahead) — nothing to do with curves.

The KB already largely agreed with the user: §4.8.2 was titled *"shipped and confirmed in
play"* and finding 9 read `✅✅ CONFIRMED IN COMBAT`. **The one genuinely stale line was
`@verify-ingame — our own bar's fix is shipped but not yet re-flown`**, which the user's
own session had already settled.

**Closed out:**
- Recorded the bar re-fly `[client 2026-08-04]`; the duration row now reads
  *"carries, **renders**, and does not poison the anchor chain"*.
- Rewrote the grade correction as a forward claim ("accepted ≠ displayed; on an
  aspect-less channel the only oracle is an eyeball") instead of an apology.
- **Renumbered the findings 1–13.** They ran 1, 9–14, 2–7 with no 8; 12 cross-references
  updated, one of them in `mined-pending-verification.md`.
- Finding 10 no longer reads as a refutation *of* §4.6 (§4.6 has absorbed it), and the
  dangling `§4.9's "aura data is wholly sealed"` citation is gone.
- Converted the remaining `MEASURED <date>` prose to `[client <date>]` tags.
- **Deleted CurveLab** — all five checklist items: `CurveLab.lua` (2,857) +
  `curvelab_spec.lua` (1,143) + `.toc` line + `curvelab` store/DEFAULTS +
  `wowkb.cdmp curvelab` (215 lines of Python). Verified no code dependency first: every
  reference outside the file and its spec was a comment.
- The one thing no instrument can settle — whether the **aspect-less** sinks (`SetAtlas`,
  `AnimVertexColor:SetStartColor/SetEndColor`) move a pixel — is parked as
  `secret-aspectless-pixel-moved` in `projects/addon-lab/questions.json`. ⚠ `SetTexture`
  (refuses) and `SetColorTexture` (poisons the chain) are **settled** and are not part of it.

⚠ **The lesson, which is the point.** This probe reached 2,857 lines *inside a product
addon*, and most of the last ten builds went on fixing the instrument rather than reading
it. `projects/addon-lab/` (ClientLab) exists for exactly this — its own `CLAUDE.md` says
it is the home for API-poking that "would otherwise keep accreting inside product addons
(**it was accreting inside CDMProbe**)". House rule 2 is that lesson made checkable.

## 6. Still open

- **The `security` three-way split** is now unblocked but undecided. ⚠ Agent 06's read:
  split the **rules section alongside the body it audits**, because the `table` defect cut
  across the proposed §0–§3 / §4.1–§4.7 seam, and a split that leaves the rules undecided
  reproduces it *across files*, where no single-file grep can catch it.
- ~~**The `@verify-ingame` firewall leaks** — 13 bare markers of 84, putting 19 addon-dev
  items into the player-facing checklist. Backtick them.~~ **CLOSED — see §7.**
- **EllesmereUI's module count** is contested (18/19/20) and the clone is deleted;
  `module-architecture.md:129` still asserts 18. Re-clone or drop the number.
- **Ten stale `api-events…§2.8` pointers** in the cooldown-hud project (docs, addon
  source, and 6 `ref =` strings in `cdm-cases.lua`) now that the material lives in
  `cooldown-manager.md` §5.x. Several are in the gitignored sub-repo.
- **Addon Phase 0 / 2 / 3** — untouched by choice; see §4.
- **OBS-002/003** (EditBox copy-out + its unmeasured limits) drain into a `frames`
  EditBox section that does not exist yet — deliberately deferred so it is written once
  against settled limits.

---

## 7. The fourth queue — CLOSED 2026-08-05

**Backticking the firewall leak would have destroyed four open questions**, and that is
the finding, not the fix. Of the 13 bare markers, **8 had no entry in
`projects/addon-lab/questions.json`** — the registry that is supposed to hold every
addon-dev question. Hiding a marker does not answer it. Register, then backtick.

The root cause is §1.8 recurring in a file the §1.8 fix did not cover: **the registry was
unreachable from the KB.** `grep -rn 'questions.json\|addon-lab\|ClientLab'
knowledge/addon-dev/*.md` returned **zero hits**, so README §1.2 indexed three queues when
there were four, and an agent following the documented route never learned the
open-question list existed.

The same dead sentence — *"64 of its 68 markers are backticked"* — had **four** homes, one
more than §1.4's dead "never run in the client" claim: `README.md` §6, `gen_verify.py`'s
docstring, `addon-lab/CLAUDE.md`, and `w1-plan.md`. Each was written when it was true and
none had a reason to be revisited. Every one is now a **grep instruction instead of a
number**, which is the same de-brittling the central pass applied to the rule census.

**Done:**
- README §1.2 indexes `questions.json` as the fourth queue, with the rule that a fifth gets
  indexed here too; §6 now states register-then-backtick as the ordering constraint.
- Registry **71 → 75**: `cdm-auradatacached-plain-in-combat` (⭐ the highest-value question
  in the subtree), `secret-compare-to-nil-permitted`, `toc-category-grouping`,
  `traitconfig-fires-on-hero-swap` (retired from `kb-inbox`, which was leaking a nonsense
  row into the player checklist).
- Two anchors repaired; `_meta` gained an `anchor_drift` note. **Nothing validates anchors**
  — that check is scoped into the W2 plan, not left as a comment.
- `security:1877`'s marker **dropped rather than backticked**: it is a coverage statement,
  not a claim, so there was nothing for a marker to resolve.
- Checklist **489 → 475 items, 0 addon-dev rows.** Gates unchanged at 0/15/2 — including
  one gate-2 hit on my own edit, caught and removed.

**W2 is now planned** in `projects/addon-lab/docs/w2-answer-pass.md`: the lab predates the
capture standard, has no drain path into `observations.md`, and batches its unbuilt tests
by topic file rather than by what one play session can cover.

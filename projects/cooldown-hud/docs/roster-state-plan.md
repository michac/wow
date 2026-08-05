# Cooldown HUD — the roster-anchored State

> **STATUS: ✅ ALL PHASES DONE — THE PLAN IS COMPLETE.** Phases 1 + 2 + 3 + 4 done
> 2026-07-31; Phase 6 done 2026-08-01 (it jumped the queue as §10 permitted);
> **Phase 5, the last one, done 2026-08-03 — §6.3 is its record.**
> (⚠ This header read "▶ PHASE 4 IS CURRENT" until 2026-08-01, weeks after Phase 4 shipped
> and was flown — §10's `▶ CURRENT` marker was stale the same way. Move BOTH when a phase
> lands.) **Read §6.1 before touching the knownness code** — it is Phase 5's load-bearing
> design decision (knownness: MARK, don't filter), and it now carries a ⚠ **correction**: the
> `judgeable`/`secretGate` mechanism it leaned on **does not exist** and has not since the W4
> cutover. **Read §6.3 before "fixing" anything in `State.lua`** — eleven decisions there are
> not in the plan text above and were each forced by something it did not anticipate.
>
> ⏳ **Code-complete is not flown.** Phase 5's acceptance is one pass on a **max-level
> Retribution** character, which also discharges Retribution's own open gate, the owed
> v0.32.36 re-fly and Phase 6.2's fragment pass. `docs/status.md` carries the gate.
>
> **✅ Phase 3 SHIPPED 2026-07-31** (commits C1–C4, released as **v0.32.48**). The DrawList
> gained a **`keybinds[]` channel**, so `cues[]` means *decisions* again and the empty-cue
> special case is gone from three files; the keybind now resolves down the **rung ladder**
> (3 → 4 → 5), which is what gives **Hellcaller its key hint** — its row's base is Immolate
> 348 while the bar holds Wither, so base-only resolution had left that icon blank. Two
> pinned cases went red on the fix and flipped in its own diff; corpus **0 `pinned-defect` /
> 21 `fixed`**. Suite **567 → 562** (the new tests net out against the deleted
> `census_spec`), luacheck 0 warnings, 96 → 99 cases. Two housekeeping items rode along:
> `GetValidAlertTypes` was promoted into `Util.lua` (Phase 4's prerequisite, rescued from the
> doomed `AlertTape.lua`) and **`Census.lua` was deleted**. **§4.2 records what actually
> changed.** ✅ **FLOWN the same day** — `cd=164597 … key=F drew=F` on Hellcaller is the
> acceptance signal, with 16 key hints against 2 cues proving the channel separation. The
> flight cost three extra builds to a **pre-existing** keybind-cache bug (the scan refused to
> run in combat, and a dummy session is continuous combat) — **no Phase 3 code was involved**;
> see §4.2. Phase 2's and v0.32.47's re-flies are still owed.
>
> **✅ Phase 2 SHIPPED 2026-07-31** (commits C1–C10, released as **v0.32.46**). **All ten
> correctness fixes landed** — §3.1 through §3.10, in the evidence-led order §10 sets out, not
> the §3.x numbering. The corpus went **0 `pinned-defect` / 19 `fixed`**: every pin Phase 1
> planted was cleared, and the `fixed` tag is the permanent record that each case once failed.
> **§3.11 records what each fix actually changed**, including the several that resolved
> differently from the plan — read it before "fixing" any of them back. Suite **498 → 567
> successes / 0 failures / 4 pending**, luacheck 0 warnings, 87 → 96 cases.
>
> The headline: the DoT read now has a channel that **self-clears**. Before this work a whole
> Destruction pull produced **169 `pandemic_refresh` cues and 0 `not_up`** — the HUD could tell
> you to refresh the DoT and structurally could not tell you to apply it. That ratio moving is
> the acceptance signal, and it is **the one thing still owed: the live pass** (which doubles as
> the outstanding v0.32.36 re-fly).
>
> Written out of two
> inputs: the `wow-developer` client-correctness review of `State.lua` (2026-07-31, findings
> reproduced in *Phase 2*), and the design conversation that followed it.
>
> **Revised 2026-07-31** after a Phase-1 design pass against the v0.32.41 source: §2.3 rewritten
> (two of its premises were wrong — see the correction there), §2.4/§2.5 grew the case-encoding
> and group contract, and **five further defects landed as §3.4–§3.8**, all verified, none
> scheduled. Every line number cited in this doc still lands at v0.32.41 except `Util.lua:229`,
> which is `:230`.
>
> **✅ THE GATING CAPTURE IS DONE (2026-07-31).** `/cdmp census` + the alert tape, Destruction
> both hero trees, 72 cooldownIDs, in and out of combat. It answered **all three** §9
> questions, promoted **§3.1 to live** (17 tab-1 rows carry an aura flag, Immolate among
> them), demoted **§3.9 to trigger-absent**, **removed rung 2 from Phase 3's ladder**, forced a
> rewording of **Phase 4** (`GetValidAlertTypes` under-reports), and turned up **§3.10** — the
> pandemic latch can never clear itself, which is the one the player feels. **Phase 2's
> internal order is now evidence-led (§10), not the §3.x numbering.**
>
> **✅ Phase 1 SHIPPED 2026-07-31** (commits C1–C7, test-only, **no release cut** — see §10).
> `tests/fixtures/cdm-cases.lua` + `tests/spec/cdm_cases_spec.lua` carry **87 cases in 7 axes:
> 72 green · 11 `pinned-defect` · 4 `unreachable`**, plus `tests/spec/harness_spec.lua` (22)
> for the four new harness knobs. Suite **384 → 498 successes / 0 failures / 4 pending**,
> luacheck 0 warnings. Writing it added a **sixth finding, §3.9 — now settled empirically**:
> `H.poison` makes `St.Build` throw, so the bare struct index IS a live crash path.
>
> **The thesis in one line:** State should be anchored on **what the spec asks about**, not on
> **what the Cooldown Manager happens to enumerate** — and almost all the machinery to do that
> already exists, pointed at the wrong anchor.
>
> **Doc map:** the pipeline contract is `architecture.md`; the design pillars are `design.md`;
> the Secret-Values reality is `notes.md`; the live worklist is `status.md`. The client-side
> facts this plan leans on are `knowledge/addon-dev/cooldown-manager.md` (the system study) and
> `api-events-and-discovery.md` §2.8. **Prose here defers to those.**

---

## 1 · The reframe — invert the anchor

Today `State.Build` enumerates the whole CDM database (`allowUnlearned = true`, ~64 rows on
Demonology), reads live facts for every row, and then **filters back down** to what is
pressable. The spec table enters only at the end, as the source for *virtual* rows.

The proposal inverts that:

| | Today | Proposed |
|---|---|---|
| Anchor | the CDM category set | **the spec's declared roster** (abilities + auras) |
| CDM's role | the source of truth | **one evidence source** among reads, edges, napkin |
| Unknown abilities | enumerated, then filtered out | never enumerated |
| Untracked abilities | clawed back by `virtualCandidates` | first-class from the start |

**Why this is worth doing, concretely:** field-fix A's entire apparatus — `displayable`,
the three-valued `isKnown` fence, `dropped`, and `virtualCandidates`' six fences — exists
*only* because the anchor is wider than the question. Anchor on the roster and "is this
pressable" stops being an inference. Whether Blizzard draws the icon or we draw it becomes a
**Binder/Renderer** question, which is where it belonged.

### 1.1 How far we actually are

Most of this is built. The gap is smaller than the design's size suggests.

| Step | Status | Where it lives today |
|---|---|---|
| Spec declares abilities **and auras** | ✅ **done** | `SpecDestruction.lua:336-345` (9 auras), `SpecDemonology.lua:306-311` (4). `kind = "aura"` already distinguishes them |
| Talent/availability filter, OOC | ✅ **done twice** | `info.isKnown` (three-valued, `State.lua:1362`) and `C_SpellBook.IsSpellKnown` (`State.lua:1210`, cached, wiped on `SPELLS_CHANGED`) |
| OOC full-API seed | ✅ **done** | `cdBaseline`, `chargeSeed`, `foldBase`, `knownCache`, `heroCache` |
| …refreshed **periodically** | ❌ runs every tick instead | `HudDriver.lua:39` — 10 Hz, no OOC throttle |
| In-combat CDM maintenance | ✅ **done, and already generic** | `readCd`'s four-rung cascade, `chargeEst`, `dotEdge`, `readyEdge`. None of these names a spell |
| Return state + cast + history + power | ✅ **done** | `St.Build`'s return, verbatim |
| Cast-*results* computed in the Coach | ❌ **the one genuinely new item** | currently `inflightIncoming`/`projectIncoming` in State |

So the work is: **one deletion, one throttle, one inversion** — plus the correctness and
testing work below, which is worth doing first and stands on its own.

---

## 2 · Phase 1 — the CDM edge inventory and its fixture suite

**Do this first.** The review found real defects in the CDM→State mapping and the felt
experience agrees. Every phase after this one changes that mapping; going in without a net is
how the next 216-dropped-cues bug ships.

### 2.1 Is it tested today? Yes — but regression-shaped, not input-shaped

`tests/spec/state_domainview_spec.lua` is **1,106 lines, ~90 tests**, loading the *real*
`State.lua` with only the CDM database and frame discovery faked. That is a genuinely good
harness. But read its `describe` blocks and the shape is unmistakable — every one is named
after a **past bug**:

> the pressable filter (field-fix A) · virtual rows + fences · the aura-lifecycle latch
> (field-fix C) · the charge napkin (C2) · the hero tree · readiness vs a foreign live override

Coverage therefore tracks **what has already bitten us**, not **what the CDM can hand us**.
The gaps line up exactly with the review's findings — none of these had a single test.
✅ **All five now have cases** (case names as shipped):

| Gap | Now covered by |
|---|---|
| `readBuffItem` / `buff.isActive` → the `buffs` fold *(finding 1)* | `family/tab2-IsActive-is-a-real-signal` · `family/tab1-IsActive-is-constant-true-…` · `draw/a-throwing-IsActive-…` · `draw/a-secret-IsActive-…` · `draw/IsShown-rides-with-its-capability-flag` · `draw/a-throwing-hideWhenInactive-index-…` |
| which spellID `readCharge` reads charges from *(finding 2)* | `flags/charges-are-read-on-the-DISPLAY-identity` (**pinned**) |
| the identity ladder's rung 2, `linkedSpellID` *(finding 3)* | `identity/the-static-pool-is-carried-whole-…` + the three rung-1/2 `unreachable` pendings |
| `readCd`'s combat cascade — 7a/7b, **no direct tests at all** | the whole **C** axis: 12 cases, incl. both baseline directions and edge-vs-napkin precedence both ways |
| `readGlow`, and `readAura`'s `aurasSecret` degradation | `read/a-throwing-glow-read-…` · `read/a-readable-glow-…` · `read/a-SECRET-glow-answer-…` · `read/a-partially-secret-aura-space-…` · `read/a-fully-readable-aura-space-…` |

### 2.2 The inventory

The CDM-resolution study is already this document in prose. **The on-disk canonical copy is
`knowledge/addon-dev/cooldown-manager.md`** — author the cases from that file, not from the
rendering at `https://claude.ai/code/artifact/bbe1740a-9f6f-493f-8082-cab23152965a`. It carries
the family split (§1), the five identity rungs with their lifetimes (§2), the value cascade and
charges' separate ladder (§3), the per-family event table and the alert choke point (§5), the
glow chain (§6), the three-tier readable surface (§7), and — most usefully for fixtures — **nine
numbered audit rules in §8**, which are the assertions in prose form.

Turn it into `tests/fixtures/cdm-cases.lua`: a flat list of named cases, each a declarative
(CDM input → expected State row) pair. One parametrised spec drives all of them.

The sketch below is the **original**, kept because four of its seven problems were *fatal* and
worth not re-deriving: `expect.ready` is not a State field (State emits `cd.state` / `source` /
`readable`); `expect.buffPresent = nil` is unassertable in Lua; `reads.cooldown = { ready = … }`
feeds a **verdict** rather than a client return, which skips `Util.lua`'s whole guard ladder and
the GCD trap; and a single-row-only shape cannot express the two-cooldownID Immolate fold or an
identity contest. **The shipped schema is in `tests/fixtures/cdm-cases.lua`'s header** — `rows[]`
+ `world` (client-API level) + an ordered `script[]` + `expect` as a map of *views*.

```lua
-- SUPERSEDED — see the fixture file's header for the shipped schema.
{
  name = "hellcaller: essential Immolate row with Wither elected (rung 2)",
  category = "Essential",              -- family is derived, never asserted from category
  info = { cooldownID = 164597, spellID = 348, linkedSpellIDs = { 157736, 445474 },
           isKnown = true, hasAura = true, selfAura = false, charges = false },
  frame = { linkedSpellID = 445474, IsActive = true, hideWhenInactive = false },
  reads = { cooldown = { ready = false, duration = 15, startTime = 100 } },
  combat = false,
  expect = { identity = 445474, ready = false, buffPresent = nil },
}
```

**The axes the case list has to span** (from the artifact's own structure):

| Axis | Values |
|---|---|
| Family | tab 1 spells · tab 2 auras |
| Winning identity rung | 1 aura · 2 linked · 3 tooltip · 4 override · 5 base |
| Combat | OOC readable · in-combat secret |
| Per-field readability | value · `SECRET` · `nil` · **throws** |
| Alert edges | all six, incl. the same-frame refresh tie |
| Struct flags | `isKnown` true/false/**nil** · `hasAura` · `selfAura` · `charges` |
| Drawability | item frame present · absent |

Not the cross-product — a **named case per interesting combination**, the way the study already
picks its scenarios. Target ~70 cases across ten groups (§2.5).

### 2.3 What the harness needs first

*(Rewritten 2026-07-31 after a design pass against the current source. The original two items
were right in kind and wrong in detail — item 2 named a call State does not make.)*

`tests/mock_ns.lua` is closer than expected: `H.secret[v] = true` already drives
`ns.IsSecret` (`:160`) and `H.combat` drives `InCombatLockdown` (`:159`). So the
secret-value axis is **already expressible**. Four gaps:

1. **`issecrettable` is hardcoded `false`** (`mock_ns.lua:161`). Every `ns.IsSecretTable`
   branch is therefore unreachable in tests — six real call sites: the info struct
   (`State.lua:104`), a packed auraData (`:429`), the cooldown table (`Util.lua:158`) and the
   charges table (`:179`, `:199`). Make it table-driven (`H.secretTable`) like `H.secret`.

2. **No "this call throws" fixture.** ⚠ **Correction:** the original text named
   `IsInPandemicTime`, but **State never calls it** — the only caller is `AlertTape.lua:100`,
   the file scheduled for deletion. `State.lua:170` merely *names* it in a comment. The throw
   axis is still needed; it just lands elsewhere. Reachable-from-`St.Build` `pcall` sites a
   throw fixture would newly cover: `IsCooldownViewerAvailable` (`:76`),
   `GetCooldownViewerCategorySet` (`:80`), `GetCooldownViewerCooldownInfo` (`:103`), the aura
   field index (`:428`), `AuraUtil.ForEachAura` (`:443`), `GetPlayerAuraBySpellID` (`:467`),
   `IsSpellOverlayed` (`:491`), `item:IsActive()`/`IsShown()` (`:508`/`:516`), the
   `hideWhenInactive` index (`:519`), `item:GetCooldownID()` (`:536`), and `Util.lua:156`/`:163`
   (`GetSpellCooldown` + its field index). Two primitives, not one: `H.throws["<dotted.name>"]`
   for calls, and an `H.poison(fields)` table whose `__index` errors, for the field-index
   `pcall`s.

3. **The client-API fakes have to be real, so `Util.lua`'s guard ladder is in the path.**
   `mock_ns` has no `C_Spell.GetSpellCooldown`/`GetSpellCharges`, no `AuraUtil.ForEachAura`, no
   `C_UnitAuras`, no `C_SpellActivationOverlay` — so `state_domainview_spec` replaces
   `ns.ReadCooldown` wholesale instead (`:1056-1064`). That is fine for the one thing it
   proves and wrong for this suite, three ways: it moves the **combat** short-circuit
   (`Util.lua:217`) outside the code under test, it puts the whole **readability** axis
   (`rawCooldown`'s six-guard ladder, `:154-167`) out of reach, and it hides the two places a
   readable client answer produces a *different* State answer — the **GCD trap** (`:225-239`)
   and the **banked-charge short-circuit** (`:222`). It also happens to be the cheapest possible
   fixture for §3.3: a call-counting fake asserts `gcdCount == N rows` today and `== 1` after
   the hoist, which is the entire fix in one assertion. Make the fakes **default-inert** (an
   unregistered id returns `nil`, which `rawCooldown` already treats identically to "the
   function does not exist"), so the existing suite cannot move.

4. **Globals leak between spec files.** `mock_ns.lua:157-199` installs the `_G` fakes at *file*
   scope, once per `dofile`. Busted loads every spec file and *then* runs the tests, so a
   `_G` mutation during a test survives into later files — `state_domainview_spec.lua:229`
   nils `_G.C_Spell.GetSpellCharges` for the remainder of the process. Extract the block into
   `H.installGlobals()` and call it from `H.fresh()` too. This is the single riskiest line in
   Phase 1; run the full suite immediately after it and expect the count **unchanged**.

### 2.4 Acceptance

Every finding in Phase 2 arrives with a case from this list, red before the fix and green
after. That is the phase's real deliverable — the inventory is the artefact, the fixes are
the proof it works.

**Encoding a case whose right answer is not today's answer.** *(Superseded during
implementation — the `expectAfter`/`contract` pair became a single `status` field, which is
strictly better: a pending case asserts nothing, so it cannot prove the defect is still live.)*
A case carries **one** `expect` — always the **contract** answer — plus a `status`:

| `status` | Runs as | Meaning |
|---|---|---|
| `green` | a normal `it` | agrees with the contract today |
| **`pinned-defect`** | **inverted** — `pcall(runCase)`, and **errors if it PASSES** | proves the defect is still live, and goes red the instant Phase 2 fixes it, so the fix commit flips `status` in its own diff. Requires `fixes`, naming the §3.x below |
| `unreachable` | `pending(pins .. " — " .. ref)` | the input does not exist today (identity rungs 1–2; the dual-category cid) |

**A suite that is 100 % green against the current code is, by construction, a snapshot.** The
inversion is what makes that structurally impossible — and a meta-test enforces a floor of five.

Two rules that decide whether this phase was worth doing at all:

- **Author from the KB, not from `State.lua`.** A suite transcribed from the source is a
  change-detector wearing a contract's clothes — green on every refactor, red on every fix.
  Walk `cooldown-manager.md` §1–§3 and the nine rules in §8, write the expected answer, *then*
  run it. The six findings in §3.4–§3.9 exist only because that order was followed.
- **Every case carries `pins` (what contract it holds) and a MANDATORY `ref`** naming the study
  section or Blizzard source it is measured against. A meta-test refuses any `ref` pointing at
  `State.lua` — a case justified only by State's own code is *characterisation*, and its `pins`
  must say so in the word "characterisation:". `grep -c 'characterisation:'` is then a
  one-command measure of how self-referential the corpus is (**6 of 87** as shipped).

And one structural rule: **do not add `St.*` seams for the read helpers.** `readCd`,
`readCharge`, `readBuffItem`, `readAura` and `readGlow` are file locals; `St.Build` is the only
door, and that is correct, because all three Phase-2 defects are at **call sites**, not in the
helpers (`:1381` passes the wrong argument to correct code, `:1415` gates on the wrong thing,
`Util.lua:230` is called from the wrong place). A helper-level test would go green on a fixed
helper while `Build` still passed the wrong argument — which is defect §3.2's exact shape.

### 2.5 The seven case axes — **as shipped**

The ten-group sketch collapsed to **seven axes** during authoring (the charge ladder is one
case inside *struct flags*, drawability absorbed the buff item, and "documented hazards"
turned out to be one `unreachable` case, not a group). Real counts, `busted` **@ end of Phase 2
(2026-07-31)** — the corpus grew 87 → 96 as §3.10's new *inputs* needed cases written rather
than flipped, and every `pinned` became `fixed`:

| Axis | Cases | green | `fixed` | unreachable | Spans |
|---|---|---|---|---|---|
| **A · Family** | 9 | 8 | 2 | 1 | tab-1 press vs tab-2 run; `pressableRep` order; the `buffs` fold; the dual-category cid; the tab-2 row that has no cooldown rung to read |
| **B · Identity rungs** | 13 | 10 | 1 | 3 | rungs 5/4/3 + their refusals, the observed override, the static pool, rungs 1–2 as unreachable |
| **C · Combat + `Util.lua`'s cascade** | 12 | 12 | 1 | 0 | OOC read, the in-combat short-circuit, 7a baseline projection both ways, the GCD trap + both its edges, banked charges, edge-vs-napkin precedence |
| **D · Per-field readability** | 30 | 30 | 11 | 0 | value · `SECRET` · absent · **throws** · **poisoned index**, at every guarded site — plus the **per-frame aura verdict** group (§3.10) |
| **E · The six alert edges** | 13 | 13 | 0 | 0 | all six types through `Build`, the same-frame tie both ways, and the three drop paths |
| **F · Struct flags** | 9 | 9 | 1 | 0 | `charges` measured-vs-flag, the `max <= 1` case, `hasAura`/`selfAura`, the charge ladder |
| **G · Drawability + the buff item** | 10 | 10 | 3 | 0 | frame present/absent, the wholesale guard, the `GetCooldownID()` fallback, `IsActive`/`IsShown`/`hideWhenInactive` refusals |
| **Total** | **96** | **92** | **19** | **4** | |

`fixed` is a **subset of green**, not a fourth state: it marks a case that was `pinned-defect`
and now passes, and it is the corpus's defect history. Six cases additionally carry
`characterisation:` in `pins` — the self-referential ones, which is how a case that *must*
describe `State.lua` says so without smuggling a `ref` past the meta-test.

**Ten meta-tests** ride on top (unique names · non-empty `pins` + `ref` · **no `ref` may point
at `State.lua`** · a `fixes` on every `pinned-defect` · a known `status` · cid uniqueness within
a case · a `spec` on any case carrying an override field · a **per-axis coverage floor** ·
`fixed` and `pinned-defect` mutually exclusive · **a floor on `#pinned + #fixed`**). That last
one replaced Phase 1's "≥ 5 failing today": once Phase 2 cleared every pin, a live-failure floor
would have had to be deleted, taking the history with it. Flooring the *sum* survives the
transition — **never lower it, and never lower a per-axis floor.**

Assert against `St.Build`'s pulse, partially and deeply — full-table equality on a 20-field row
makes the suite a change-detector, so equality is opt-in per view (`exact = { raw = true }`).
Two schema details are load-bearing: the **`ABSENT` sentinel** (in Lua an absent key and a `nil`
value are indistinguishable, and "we must not fabricate a value" is most of this project's
contract), and an **`asked` view** recording the ids the *client fake* was called with — a
membership map that answers **`false`** for an unasked id, so a case can state "you must NEVER
have asked about this one". That is what makes §8 rules 2 and 3 assertable at all, rather than
inferred from a downstream number; **§3.2, §3.3 and §3.8 are each pinned on `asked` alone.**

---

## 3 · Phase 2 — the correctness fixes

> **✅ ALL TEN SHIPPED 2026-07-31 (v0.32.46).** §3.1–§3.10 below are kept as written — they are
> the *diagnosis*, and the reasoning in each is still the reason the fix looks the way it does.
> **What actually changed is §3.11**, which also records the half-dozen places the
> implementation resolved differently from the plan. Where the two disagree, §3.11 wins.

**§3.1–§3.3 are the original three**, source-verified against `wow-ui-source @ 12.0.7.68887`.
Each is small and independently shippable, and each should land with its Phase-1 fixture
(H7, I3 and C5 respectively).

**§3.4–§3.9 were found by the Phase-1 work (2026-07-31)** — authoring the case list against
`cooldown-manager.md` §8's audit rules turned up **six** more, all verified in the v0.32.41
source and none of them fixed. That is the inventory paying for itself: five before a line of it
was written, and §3.9 while writing it. **None is scheduled.** Each carries a `pinned-defect`
fixture asserting the CONTRACT answer, run inverted so it *fails today* (§2.4) — the day a fix
lands, its case goes red and the fix commit flips the status in its own diff. Promote them
deliberately, not as a batch — §3.5 in particular touches the key rows are filed under, which
the v0.32.36 incident is the standing lesson about.

**Eleven cases are pinned, not eight**, because two findings are two-sided: §3.4 has a
secret-value half (over-show) and an absent-field half (under-show), and §3.9 is pinned at two
separate fields so it cannot be dismissed as one unlucky line.

### 3.1 Gate the buff-item read on **family**, not on the struct flags

`State.lua:1415` decides whether to read the item frame from `hasAura or selfAura`. But
`CooldownViewerItemMixin:ShouldBeActive()` is `return self.cooldownID ~= nil`
(`CooldownViewer.lua:362-364`), and **only `CooldownViewerBuffItemMixin` overrides it**
(`:1186`). So on any Essential/Utility row `item:IsActive()` is **constant `true`** — no error,
no nil, nothing to distinguish it from a real signal.

That feeds `buffs` directly (`State.lua:1491-1495`), which both brains read:
`CoachDemonology.lua:130` `ctx.tyrantWindowActive = buffActive(S.TYRANT)`,
`CoachDestruction.lua:364` `buffActive(dotID)`. Tyrant is one Essential row **plus** one
TrackedBar row sharing a base spellID — so if the Essential row carries `selfAura`, the burst
window reads **permanently open**.

> ✅ **GATE ANSWERED — THIS IS LIVE, AND IT IS THE WORST OF THE SIX.** `[client]` 2026-07-31
> (`/cdmp census`, Destruction, both hero trees). **17 tab-1 rows carry `hasAura`/`selfAura`**,
> including **cid 164597 Immolate — the spec's spine**. Every tab-1 row with a frame read
> `IsActive = true`, out of combat, standing still, with no target; the sharpest single
> reading is that same Immolate row simultaneously reporting `IsActive=true`,
> `wasSetFromAura=false` and `auraDataUnit=nil` — the frame calls itself active while its own
> source flags say no aura drove it.
>
> **The traced consequence is bigger than "a burst window can read open".** It jams
> `CoachDestruction`'s DoT read to `"up"` on *both* hero trees — Diabolist via
> `buffs[348]` (the fold reads `buff.isActive`), Hellcaller via `dotRow.buff.isActive`
> directly — so `dotState` can only ever reach `"missing"` through an `OnAuraRemoved` edge.
> **Evidence:** across the whole capture, all **169** DoT cues carry the note
> `pandemic_refresh` and **zero** carry `not_up`. The HUD can tell you to *refresh* the DoT
> and structurally cannot tell you to *apply* it.

**Fix:** read the buff item only when `category` is `TrackedBuff`/`TrackedBar`.
(`cooldown-manager.md` §8 rule 4.) **Fixture:** `family/tab1-IsActive-is-constant-true-and-must-not-reach-buffs` (**pinned**), with its green sibling `family/tab2-IsActive-is-a-real-signal` beside it. Note `readBuffItem`'s own header at `State.lua:496-503`
reasons solely about Demonic Core — a tab-2 row. The comment is the trail showing which family
was actually checked.

### 3.2 Read charges off `overrideSpellID or spellID`

`readCharge(ident, …)` (`State.lua:379`, called `:1381`) keys on the **display identity**,
which can resolve to `overrideTooltipSpellID` (rung 3). Blizzard deliberately excludes that
rung, and says why:

```lua
-- To ensure that charges work correctly for cooldown items that are actively cast,
-- apply auras, and have charges only check the override or base spell ids.
local chargeSpellID = info.overrideSpellID or info.spellID;
```
`CooldownViewerItemData.lua:283-288`

Two ladders on one row. Rung-3 rows exist in Warlock (cid 182891 → tooltip 1288945).
(§8 rule 3.) **Fixture:** `flags/charges-are-read-on-the-DISPLAY-identity` (**pinned**), asserted purely on *which id the client fake was asked about*. The `ident` keying for the *cooldown* read stays — that was the right fix for the
Grimoire/Singe Magic bug; charges just need the narrower ladder.

### 3.3 Hoist the GCD read out of the per-entry loop

`ns.ReadCooldown` calls `rawCooldown(GCD_SPELLID)` for **every** entry (`Util.lua:230`) —
~64 identical reads per tick, 10 Hz. Read once per pulse, pass it down. Pure win, no
behaviour change. **Fixture:** `combat/the-GCD-is-re-read-once-per-enumerated-entry` (**pinned**)
— three rows, `asked.gcdCount` reads **3** today against a contract of **1**, so the fix is one
number changing.

### 3.4 A refused `isKnown` read becomes an affirmative `true` *(found 2026-07-31)*

`State.lua:1362-1363` is
```lua
local isKnown
if info ~= nil then isKnown = info.isKnown and true or false end
```
The comment above it is a good one — it documents the and/or trap that kept `isKnown`
`true`-or-`nil` since W4 Phase 1. But it reasons only about the *absent* case. **A secret value
is truthy in Lua**, so a `SECRET` `isKnown` on a present struct yields **`true`**, not `nil`.
`nil` is only reachable when the *entire* info struct is missing (absent / secret table /
thrown call).

Two consequences. First, "is `isKnown` three-valued?" is not a per-field readability axis at
all — it is an all-or-nothing *struct* axis, which is worth knowing before §6.1 builds a whole
design on the three values. Second, this is a **refusal laundered into an assertion**: the row
reads "the client says you have this talented" on the strength of a value we could not read.
It fails in the over-show direction (a phantom ability re-enters the rotation — the Soul Fire
shape), which is the direction field-fix A existed to close.

**Contract:** `readable(info.isKnown)`-style guarding, so a secret lands on `nil` with the
absent case. **Fixtures:** `read/a-SECRET-isKnown-becomes-an-affirmative-true` (**pinned**,
over-show) and its twin `read/an-absent-isKnown-on-a-present-struct-becomes-false` (**pinned**,
under-show — a struct that *answers* but omits the field yields `false`, i.e. a DROP; found
while authoring the case).

### 3.5 `DisplayIdentity` inverts Blizzard's rungs 3 and 4 *(found 2026-07-31)*

`GetSpellID()`'s ladder is rung 3 `overrideTooltipSpellID` **before** rung 4 `overrideSpellID`
(`cooldown-manager.md` §2). `State.lua`'s `liveSpellID` (`:130-131`) gets this right. But
`ns.DisplayIdentity` (`Viewers.lua:153-154`) does the reverse:

```lua
local shown = overrideSpellID
if type(shown) ~= "number" or ns.IsSecret(shown) then shown = overrideTooltipSpellID end
```

So on a row carrying **both** fields the two ladders disagree — and it is the *display* one,
the id the row is keyed under and read under, that is wrong against the client.

> ⚠ **Do not fix this casually.** `DisplayIdentity` decides which key an `abilities` entry is
> filed under; that is the seam the v0.32.36 Diabolist bug lived in, and the fix note there
> lists three fences to hold in mind first.
>
> ✅ **GATE ANSWERED — the trigger EXISTS but is currently harmless.** `[client]` 2026-07-31:
> exactly two rows carry both fields — cid `133729` Blight of Weakness (`ov=1271798`,
> `ovt=1271748`) and cid `133730` Blight of Tongues (`ov=1272122`, `ovt=1271802`). Both are
> `cadence = "utility"`, so neither is ever cued or scored. **Real, reachable, zero blast
> radius today** — which makes this the one to fix *calmly*, not first. **Fixtures:** `identity/rung3-outranks-rung4-in-the-live-ladder`
> (green — the correct order) and `identity/rung3-vs-rung4-the-display-ladder-is-inverted`
> (**pinned**), which sit side by side over the same row and make the disagreement legible.

### 3.6 One throwing aura read condemns the whole row *(found 2026-07-31)*

`readAura` (`State.lua:464-471`) walks the row's associated ids and, on the first `pcall`
failure, returns `{ readable = false }` **immediately** — ids 2..n are never asked. So the row
claims "the aura space is unreadable" on evidence about *one* id, when a later id might have
answered cleanly. It fails in the under-show direction (an aura that is genuinely up reads
unknown), which for Destruction's DoT line means the refresh press goes quiet rather than
wrong — the safer direction, but still a claim we did not earn.

**Contract:** remember the refusal, keep walking, and return `{readable=false}` only if no
later id answers positively. **Fixture:**
`read/a-throwing-aura-read-condemns-the-whole-row` (**pinned**).

### 3.7 `readCharge` claims `readable = true` on a read that never happened *(found 2026-07-31)*

`readCharge` has four return shapes (`State.lua:379-396`). Two of them —
`:388` (a live read with `max <= 1`) and **`:394`** (`not hasCharges`, after
`ns.ReadCharges` already returned `nil`) — are byte-identical: `{ readable = true, cur = nil,
max = 0 }`. The first is a measurement. The second is a **struct-flag inference**, and it is
the common case in combat, because `ns.ReadCharges` short-circuits on `InCombatLockdown`
(`Util.lua:195`) — so every non-charged row in combat reports a positive readability it did
not measure.

Nothing consumes it wrongly today (the brain keys on the measured `charged`, which is exactly
why `charged` was introduced). But it violates §8 rule 5 — trust and meaning are independent
axes — and it makes an inference indistinguishable from an observation at the one field whose
whole job is to say which it is. **Contract:** the inferred shape reports `readable = false`,
or carries a distinct `source`. **Fixture:**
`draw/a-charge-shape-inferred-from-a-flag-is-not-a-measurement` (**pinned**).

### 3.8 `readCd` runs for tab-2 rows, which structurally cannot have one *(found 2026-07-31)*

`State.lua:1409` calls `readCd` for **every** enumerated row. Per `cooldown-manager.md` §3.2,
tab 2 (TrackedBuff / TrackedBar) has **no cooldown rung at all** — first match wins among the
aura sources. On Demonology roughly a third of the ~64 enumerated rows are tab 2, and each one
costs the full guarded-call budget per 10 Hz tick to produce a field nothing can consume.

This is the same defect *class* as §3.1 — reading a family-specific channel uniformly across
families — and it is cost rather than incorrectness, so it is the least urgent of the five.
It is also the one §6's roster anchor makes mostly moot, which is an argument for leaving it
until then rather than fixing it twice. **Fixture:**
`family/a-tab2-row-has-no-cooldown-rung-to-read` (**pinned**), asserted on `asked` — the read is
not wrong, it simply must never happen.

> ⚠ **"Least urgent" undersold it.** Skipping the call meant the `foldBase` write that used to
> ride inside `readCd` had to be hoisted into `St.Build`'s loop — and hoisting it made it fire
> **whenever `base` is readable**, which is strictly wider than the old placement. So the
> smallest-looking of the five had the largest knock-on of the four cheap ones. See §3.11.

### 3.9 `St.Build` reads the CDM struct with bare indexes, and it CAN throw *(found + confirmed 2026-07-31)*

`cooldownInfo` (`State.lua:99-106`) pcalls the *call* and checks `IsSecretTable`, then stops.
`St.Build` then bare-indexes `info.spellID`, `info.overrideSpellID`, `info.overrideTooltipSpellID`,
`info.hasAura`, `info.selfAura`, `info.charges`, `info.isKnown` and `info.linkedSpellIDs`
(`:1344-1354`, `:1363`, `:1372`) **outside any pcall**. Meanwhile `rawCooldown` pcalls the
equivalent field access on a table that passed the *same two checks*, with the comment:

> `-- Indexing is itself pcall'd: a table that passes issecrettable can still`
> `-- throw on access under the 12.0 restrictions` — `Util.lua:160-163`

Either that general claim is true and `St.Build`'s loop is a live crash path, or the guard is
superstition. **Both cannot be true.**

> ✅ **Settled empirically, and it is the answer that costs something.** `H.poison` (a table that
> indexes fine except on named fields — the exact shape `Util.lua:163` guards against) makes
> **`St.Build` throw**, at both fields tested. So the guard is not superstition, and the same
> hazard it defends against is unguarded in Build's own loop — a structural crash path, not a
> stylistic inconsistency. It would take the whole 10 Hz pipeline down from inside a per-row
> loop, with no `dropped` entry and no decision-log line, which is the worst diagnostic shape
> this project has.
>
> ✅ **AND THE TRIGGER IS NOT PRESENT.** `[client]` 2026-07-31: **zero** struct fields raised
> on index, across 72 cooldownIDs × 2 hero trees × in/out of combat. So the crash path is
> real and currently unreachable — which puts this LAST of the six, not first. Keep both
> pinned cases: they cost nothing and they are the alarm if a future patch changes it.
>
> ⚠ **What this does NOT settle** is whether the client ever hands us such a table. `Util.lua`'s
> comment adds a context-specific reason (it runs from a `hooksecurefunc` callback inside
> Blizzard's layout path) that Build does not share, so the honest framing stays *a contradiction
> resolved in favour of the guard*, with the trigger still unmeasured — the same honest gate
> §3.1 and §3.5 carry. **`@verify-ingame`.**

**Contract:** the struct read is pcall'd once as a whole, or each field goes through a guarded
accessor, so a raising field yields `nil` rather than taking the pulse down.
**Fixtures:** `read/isKnown-is-bare-indexed-on-a-struct-that-can-raise` and
`read/hasAura-is-bare-indexed-on-a-struct-that-can-raise` (both **pinned**).

### 3.10 The pandemic latch can never clear itself *(found + measured 2026-07-31)*

**This is the one the player actually feels**, and it is not a coding slip — it is a wrong
model of the channel.

`PandemicTime` is a **one-shot notification, not a state.** `TriggerPandemicAlert`
(`CooldownViewer.lua:552-555`) clears `pandemicAlertTriggerTime` and sets
`nextAvailableTimeToPlayPandemicAlert = pandemicEndTime`, commented *"Prevent the alert from
playing again for this instance"*. And **a re-application of a live aura raises nothing at
all** — not `OnAuraApplied`, not `OnAuraRemoved`. `[client]` 2026-07-31: **41 Immolate casts
produced 1 `OnAuraApplied`, 1 `PandemicTime`, and 0 `OnAuraRemoved`**; the latch age simply
climbed (`Imm=fresh@2.2 → @43.8`) and never reset.

So the aura-lifecycle latch sees an aura's *first application and first pandemic entry, then
silence* for as long as it is maintained. `DOT_PANDEMIC_TTL = 6.0` (added 2026-07-30) is the
right instinct, and the capture shows it doing exactly its job — and shows the cost:
**`w:Imm` fired t92.5 → t98.3, precisely one 5.8 s window, then went silent for the rest of
the pull** with the DoT still latched `pandemic@10.1`.

Combined with §3.1 the DoT line has **no working channel at all** after that window.

**The fix is now available, and it is a capability rather than a repair.** Two frame fields
measured readable in combat over a full DoT cycle (`security-taint-and-restricted-data.md`
§4.11 owns the mechanism and its four preconditions):

| Field | Answers | Measured cycle |
|---|---|---|
| `item.auraDataUnit` | **is the aura up**, and on which side | `nil` in combat pre-application → `"target"` once applied |
| `item.PandemicIcon` | **is it in the refresh window** | `nil` → `table` on entry → **`nil` again on refresh** |

Both are recomputed by Blizzard every frame, so both *self-clear* — which is precisely what
the edge cannot do. ⚠ Both are widget internals, so per §4.11 **rule 17b** they need a bind-time
capability check and a fallback to the existing edge latch; a silently-absent field must not
read as "no DoT". *(Cited as "rule 18" before 2026-07-31 — that file had two rules numbered 18,
and the widget-internals one was renumbered `17b` to sit beside rule 17, its nearest neighbour.)*

**Contract:** the DoT read consults `auraDataUnit` for presence and `PandemicIcon` for the
window, with the alert edges demoted to what they are — a fast-path notification.
**Fixtures:** none yet. These are new *inputs*, so they need cases **written** rather than
flipped — axis D, the frame-field group.

### 3.11 What actually shipped *(the record — 2026-07-31, v0.32.46)*

Ten commits, `C1`…`C10`, each with its fixture red-then-green. **All ten diagnoses above held.**
What follows is only where the *implementation* diverged from what §3.x proposed — a fresh
reader should treat every one of these as deliberate and **not "fix" it back**.

| | Commit | What landed |
|---|---|---|
| C1 | `c1b1d86` | the frame-field harness knob + the defect-history floor that survives Phase 2 |
| C2 | `f21e41e` | §3.10's cases pinned — the per-frame aura verdict the DoT line had no channel for |
| C3 | `3b7761e` | **§3.1 + §3.10** — the family gate, and the self-clearing DoT channel |
| C4 | `54b1433` | §3.3 the GCD hoist — read it once per pulse, not once per enumerated entry |
| C5 | `40be5ad` | §3.4 + §3.9 — extract the struct once, guarded; stop laundering a refused `isKnown` |
| C6 | `fe33e34` | §3.6 one throwing aura read must not condemn the whole row |
| C7 | `56a244e` | §3.7 an inferred charge shape is not a measurement |
| C8 | `f587c83` | §3.8 don't read a cooldown rung tab 2 cannot have |
| C9 | `b16c96e` | §3.2 charges read off `overrideSpellID or spellID` |
| C10 | `a55a6a7` | §3.5 the display ladder |

**Ten deviations worth knowing:**

1. **`mint` / `buildItem` moved out of `cdm_cases_spec.lua`** into `tests/case_builders.lua`, a
   factory `(H, SECRET) -> {mint, buildItem}`, so `harness_spec.lua` can prove them. Frame knobs
   are `fields` (minted verbatim), `methods` (no-op stubs, so `ns.HasMethod` answers true —
   **absent by default**, which is what keeps the capability check falsifiable) and `raises`.
2. **The meta-test floor is `#pinned + #fixed >= 11`.** Actual is **19**, not the 18 the plan
   estimated — §3.10 shipped 8 cases, not 7.
3. **`state_domainview_spec.lua` needed no changes at all.** The plan's warning about collateral
   reds there did not materialise: it never exercised the buff-item channel.
4. **`coach_destruction_apl_spec.lua:509-512` needed no re-sourcing either** — it is fed by the
   alert edge, which survives as channel 2. Instead a new *"the DoT's three channels, in trust
   order (§3.10)"* block adds 8 tests, **including the `not_up` press that was structurally
   unreachable before**, and the rule-17b fallback-to-the-latch case.
5. **§3.4/§3.9 (C5):** `readInfo` does a **batch pcall with a per-field salvage fallback**, not a
   single pcall — one pcall around the whole copy would lose every field *after* the one that
   threw. New helpers `readableBool` (asks `issecretvalue` **before** `type`) and `flagOf`.
   ⚠ `hasAura`/`selfAura`/`charges` stay **truthy on a secret** deliberately, pinned by
   `flags/a-SECRET-hasAura-is-truthy-and-arms-the-read`; only `isKnown`, which *removes* a row,
   refuses to launder a refusal.
6. **§3.3 (C4):** new `ns.ReadGCD()`; `gcd` is **always a table** (empty when the read refused)
   so "asked and got nothing" cannot be mistaken for "nobody asked".
   `combat/a-banked-charge-short-circuits-the-recharge-timer` moved `gcdCount` 0 → 1 — a
   contract change, documented in its `pins`.
7. **§3.7 (C7):** both charge shapes now carry a `source` — `"live"` (measured) vs `"flag"`
   (inferred) vs `"static"` (`virtualRow`, stating the spell's nature).
8. **§3.8 (C8):** a tab-2 row still carries a `cd`, shaped
   `{ state = "unknown", readable = false, source = "none" }` — a uniform shape beats a `nil`
   every consumer and `stampCd` would have to guard. And the `foldBase` hoist (see the §3.8 note)
   made that write **strictly wider** than before.
9. **DecisionLog's `DOT:` field is two-sided**, `<code>=<frame>/<edge>` — e.g.
   `Imm=tgt+p/pandemic@43.8`. Frame tokens: `tgt`/`plr` (bound), `off` (**the MISSING answer**),
   `?` (refused), `X` (writers gone), `+p` (in the pandemic window). Six new `decisionlog_spec`
   tests cover it.
10. **`/cdmp hud status`** grew an `aura-frame read: N/N auraDataUnit, N/N pandemic writers`
    line, backed by a new `St.AuraFrameCapability()` in `State.lua`. If either half reads **0**
    in game, the frame internals moved and the HUD is on the edge-latch fallback — that is
    rule 17b working as designed, and it is **the finding, not a bug**.

**Files touched:** `State.lua` (every fix except §3.5) · `Util.lua` (§3.3) · `Viewers.lua`
(§3.5) · `CoachDestruction.lua` (trust order) · `DecisionLog.lua` · `HudDriver.lua` ·
`tests/case_builders.lua` **(new)** · `tests/fixtures/cdm-cases.lua` ·
`tests/spec/{cdm_cases,harness,coach_destruction_apl,decisionlog}_spec.lua`.

**Still owed:** the live pass. Its acceptance signal is the **`not_up` DoT cue appearing at
all** in `wowkb.cdmp decisionlog` (baseline: 169 `pandemic_refresh` / 0 `not_up` across a whole
pull), the DoT cue firing across the *whole* pull rather than one 5.8 s window, `Imm=off/…` in
the `DOT:` field, and a Demonology sanity pass that Tyrant's burst window still opens and closes
(it rides a tab-2 TrackedBar row, which survives the family gate).

---

## 4 · Phase 3 — separate the keybind from the cue channel

**This restores the original design.** `HudBinds.lua`'s own header still states the intent:

> *"Identity chrome, deliberately OUTSIDE the cue contract: a keybind is not a rotation
> signal, it's how you know which icon is which button."*

The plumbing then does the opposite. `Binder.lua:87` is explicit: keybinds ride **every**
button "with no separate DrawList channel (W4 P5d)", by emitting an **empty cue** — a cue with
a keybind and no emphasis. So a display concern travels through the decision channel, the
Coach's Guidance is padded with entries that assert nothing, and the Renderer has to special-case
"cue with no dot."

**The change:**

- State resolves a keybind **per CDM row**, as it does now — it is the single resolver.
- The DrawList gains a **`keybinds[]` channel** alongside `cues[]`, built by the Binder
  straight from the Layout. No Coach involvement.
- Guidance stops carrying keybind-only cues entirely. The empty-cue special case disappears
  from `Binder.lua` and `Renderer.lua`.

### 4.1 Resolve the keybind down the rung ladder

Today the keybind resolves off the **base** id. That rule came from a real bug (v0.7.0
finding-3, documented at `Viewers.lua:75-80`): a Demonic Art transform changes `GetSpellID`,
the bar slot still holds the base, so keying on the transformed id misses.

That rule is still right, and it is **not** in tension with following the ladder — because
the ladder is a **candidate list with fallback**, not a replacement:

```
try rung 2 (linkedSpellID) → rung 3 (overrideTooltipSpellID)
  → rung 4 (overrideSpellID) → rung 5 (base);  first id with a real binding wins
```

Rung 1 (the live aura instance) and the **observed live override** are excluded — those are
the transform case the v0.7.0 rule fences off. Everything below them is a legitimate "this is
the spell actually sitting on your bar" candidate. An unbound spell yields `nil`, so
first-hit-wins is self-correcting.

The motivating case is Hellcaller: the row's base is Immolate 348, but **Wither 445474** is
what is on the bar and what Blizzard displays. Base-only resolution misses it.

> ✅ **MEASURED 2026-07-31 — AND RUNG 2 COMES OUT OF THE LADDER ENTIRELY.** The blocking
> question is answered, in the direction that makes this phase *smaller*:
>
> - **The elected `linkedSpellID` does not exist to be read.** 0 of 72 rows carried it in a
>   fresh struct read, and `item:GetLinkedSpell()` returned `nil` on **every frame** too — so
>   this was never a struct-vs-frame divergence. Nothing ran the election at all (§2.2 path B
>   needs a `SPELL_UPDATE_COOLDOWN` naming a pool candidate; none came).
> - **The motivating case is served by rung 4 instead.** Hellcaller's Wither arrives as
>   `overrideSpellID = 445468` on cid 164597 (vs `348` on Diabolist), straight out of a plain
>   struct read — and `ns.DisplayIdentity` already resolves it correctly. Confirmed
>   end-to-end in the decision log: `w:Wth` on Hellcaller, `w:Imm` on Diabolist.
>
> **So the ladder is `rung 3 → rung 4 → rung 5`**, all three of which are plain struct fields,
> and the frame read is not needed. (Wither is also **two** ids — 445468 cast, 445474
> pool-aura — mirroring Immolate's 348/157736, which refutes the one-id reading in
> `cooldown-manager.md` §2.7.)

### 4.2 What actually shipped *(the record — 2026-07-31, v0.32.48)*

Four commits, `C1`…`C4`. **Both diagnoses held**, and the phase came out the size §4.1's
measurement predicted. What follows is only where the *implementation* diverged from what
§4 proposed — a fresh reader should treat every one of these as deliberate and **not "fix"
it back**.

| | Commit | What landed |
|---|---|---|
| C1 | `a0809c5` | the two keybind cases **pinned**, + the harness swap to the real `HudBinds.lua` |
| C2 | `eae9d53` | §4.1 the rung ladder — `B.Resolve`, State's call site, `hudbinds_spec` (flips both pins) |
| C3 | `1551937` | §4 the `keybinds[]` channel — HudGeometry / Binder / Renderer / RenderTest / HudVirtual |
| C4 | `de2ab1f` | the two housekeeping items: `ns.ReadValidAlertTypes`, `Census.lua` deleted |

**Six deviations worth knowing:**

1. **The harness now loads the REAL `HudBinds.lua`** instead of stubbing it, with `B.map`
   pointed at `fx.keybind`. The fixture supplies the action-bar *cache*; everything above it
   (the secret guard, the `SpecBindAlias` fallback, the ladder) is shipping code. A stub
   would have had to duplicate the ladder and could then get it right while the shipping
   code got it wrong. `Start` stays stubbed — the real one scans 180 slots through
   `GetActionInfo`, and `St.Acquire` calls it unguarded.
2. **Three cases shipped, not one, and two were pinned.** The plan named the Hellcaller case
   as the `pinned-defect`; the rung-*order* case fails base-only too, so it was pinned as
   well. The Diabolist case is the no-regression half and was green throughout — a ladder
   that reached past a bound base would have broken what already worked. Corpus **0
   `pinned-defect` / 21 `fixed`**.
3. **The Binder normalises a blank layout keybind** rather than passing `entry.keybind`
   through with `or`: `""` now falls through to the cfg seam instead of reaching the
   DrawList. The old cue path let a blank ride and the Renderer filtered it; with its own
   channel the blank entry would simply have been noise.
4. **`R:drawKeybinds` reuses `cueHolders` and the `cueKeys` pool**, so both channels ride the
   same per-icon strata/level fix. That is what forces the union cull, and the plan called
   it correctly as the one real trap. Three `renderer_spec` tests pin it: dot drops / key
   survives, key drops / dot survives, and both drop / holder hides.
5. **`R:drawCues` keeps its unknown-token `else` branch.** The plan said to delete "the
   branch's *reason for existing*", which it did — but "an emphasis the theme has no entry
   for draws nothing, and hides any prior dot" is a contract of its own, independent of
   empty cues, and `renderer_spec` already asserted it against a deliberately unknown token.
6. **The golden close-the-loop scenarios now compare the cue channel EXACTLY.** They used to
   filter the Binder's empty-cue padding out before comparing, because the `/cdmp rt`
   fixtures never carried it. Nothing to filter now.

**Files touched:** `HudBinds.lua` · `State.lua` · `HudGeometry.lua` · `Binder.lua` ·
`Renderer.lua` · `RenderTest.lua` · `HudVirtual.lua` · `Util.lua` · `AlertTape.lua` ·
`Core.lua` · `CDMProbe.toc` · `Census.lua` **(deleted)** · `tests/mock_ns.lua` ·
`tests/fixtures/cdm-cases.lua` · `tests/spec/{binder,renderer,hudvirtual}_spec.lua` ·
`tests/spec/hudbinds_spec.lua` **(new)** · `tests/spec/census_spec.lua` **(deleted)** ·
and in the workspace `tools/wowkb/cdmp.py` + both `CLAUDE.md`s. Suite **567 → 562** (the
new work nets out against `census_spec`'s deletion), luacheck 0 warnings, 96 → 99 cases.

### ✅ Flown 2026-07-31 — the acceptance signal, verbatim

```
cd=164597  spellID=445468 (Wither)  key=F  drew=F  frame=bound
```

That is the whole phase in one line. On **Hellcaller** the row's base is Immolate 348, it
resolved *nothing* before this work, and the icon showed no key at all; the ladder now finds
Wither at **rung 4** and the `keybinds[]` channel carries it to the screen. The same dump
shows the channel separation working — **16 key hints, 2 cues** across 17 displayed icons
(`cue=ROTATION` on Conflagrate, `cue=ROTATION_FALLBACK` on Summon Infernal) — and
`Command Demon key=none / drew=—`, which is correct: genuinely unbound, and **never a
placeholder**.

⚠ **The flight cost three extra builds, and none of them were Phase 3's fault.** The first
pass ran entirely keyless because `HudBinds` refused to scan the action bars in combat and a
target-dummy session is *continuous combat* — so the 180-slot scan had never run once. Every
symptom in that session, including the earlier and more confusing "only *some* icons have
keys", comes from that one gate. Not a line of Phase 3 code changed in the fix; the
`key=none` reading covered rows like Dark Pact that never needed the ladder at all. Full
account in `status.md`. **The lesson is the instrument:** `B.stats` had tracked
`slots`/`bound`/`scans`/`deferred` since v0.6.1 and nothing displayed it, so a cache that had
silently given up was indistinguishable from a rendering bug.

**Still owed on this flight** — *not* Phase 3's, but it rides the same trip: the
**Diabolist** half of the ladder (the same row should show Immolate's key), Phase 2's DoT
acceptance (`not_up` appearing at all), and v0.32.47's `ChargeGained` re-fly. Checklist in
`status.md` → *Owed: the v0.32.36 re-fly*.

---

## 5 · Phase 4 — the roster coverage probe

The in-combat maintenance layer is **already generic** — `readCd`'s cascade, `chargeEst`,
`dotEdge` name no spell between them. The open question was never *can this be general*; it is
**does it cover every declared id**. That is answerable out of combat, cheaply.

Checked the current rosters against `CooldownSetSpell @ 12.0.7`:

| Declared aura | CDM rows | Category |
|---|---|---|
| Diabolic Ritual 428514 | 4 | tracked |
| Backdraft 117828 · Chaotic Inferno 1244860 · Fiendish Cruelty 1245664 | 1 each | 2 · TrackedBuff |
| Backlash · Flashpoint · Lake of Fire · Alythess's Ire | 1 each | 2 |
| Demonic Core 264173 · Wild Imp 296553 · Dominion 1276166 | 1 each | 2 / 3 |
| **Crashing Chaos 417234** | **0** | **NONE** |

10 of 11 are CDM-tracked in the auras family — alert channel *and* a meaningful `IsActive()` in
combat. **One is not tracked at all**, and for it there is no combat-readable channel
whatsoever (`C_UnitAuras` is fully secret in combat, `GetPlayerAuraBySpellID` included).

> ✅ **…and on inspection it should not be in the roster at all** (2026-07-31). Crashing Chaos
> has exactly **one** reference in the addon — its own declaration at `SpecDestruction.lua:341`
> — and nothing reads it. More to the point, what it *would* tell us is a **shard-cost
> change**, and the brain already reads cost live via `costOf` → `ns.ShardCost` →
> `C_Spell.GetSpellPowerCost` (`CoachDestruction.lua:205-214`). The effect is observable
> through a channel we already trust, so the aura is redundant rather than blind.
>
> **Consequence for the gap analysis:** "a declared aura with no CDM row" is still a real
> *class* of blind spot — no `IsActive()`, no `auraDataUnit`, no edges, and the combat log is
> gone (`security-taint-and-restricted-data.md` §4.9: `COMBAT_LOG_EVENT_UNFILTERED` errors on
> registration) — but it currently has **no live instance**. Delete the roster entry; keep
> the coverage probe, whose job is exactly to make the next one loud instead of silent.

**Build:** at roster load (OOC), for each declared id resolve its cooldownID and call
`C_CooldownViewer.GetValidAlertTypes(cooldownID)`. Emit a **coverage report** per id —
tracked/untracked, family, which alert types can ever fire. Surface it on `/cdmp hud status`.

Two things this buys that nothing currently expresses:

1. **"This aura will be blind in combat"** becomes a design-time answer the spec author sees,
   not a silent runtime degradation.
2. State can finally distinguish **"no ready edge yet"** from **"this row is not reported
   eligible for one"** — today both look identical and both fall to the napkin forever.

> ⚠ **REWORDED 2026-07-31, because the probe UNDER-REPORTS.** `[client]`: `GetValidAlertTypes`
> returned **`PandemicTime` only** for cid `164597`, and the alert tape recorded an
> **`OnAuraApplied`** on that same cooldownID in the same session. So it is a **lower bound on
> what a row can raise, not the set** — the original phrasing above ("can never fire one") is
> exactly the claim it cannot support, and building a coverage report on it as an authority
> would have produced confident false negatives. The report must say *"not reported
> eligible"*. A `TriggerAlertEvent` hook remains the only complete observation.

> ⚠ `GetValidAlertTypes` currently lives **only** in `AlertTape.lua:204-220` — the file
> scheduled for deletion. **Promote it before the tape goes.** ✅ Done in Phase 3.

### 5.1 What actually shipped *(the record — 2026-07-31)*

**`Coverage.lua`** — a new file, in the `.toc` immediately after `State.lua`. Plus
`St.CoverageRows` in State, `ns.AlertEventName` promoted into `Util.lua`, two `/cdmp hud`
surfaces, and the deletion of Crashing Chaos. 31 new tests (`coverage_spec.lua` 27 +
`state_domainview_spec`'s shipped-symbol block 4).

**The vocabulary is the deliverable**, not the readout. Per declared roster id a
**coverage** fact (`tracked` / `untracked` / `unreadable`) and a **verdict**:

| verdict | when | loud? |
|---|---|---|
| `ok` | tracked — some CDM row carries the id as base, `overrideSpellID`, `overrideTooltipSpellID` or a `linkedSpellIDs` member | no |
| `virtual` | untracked, but the **real** `St.VirtualCandidates` fences say we draw our own icon | no |
| `expected` | untracked and `expect == false` — the override-only ids and cast aliases | no |
| `blind` | untracked, `expect ~= false`, not virtual-covered | **yes** |
| `unknown` | a row refused its fields, so the negative is unprovable | mild |

**Three decisions, and they are the whole design:**

1. **Diagnostic only — payoff #2 was deliberately NOT built.** §5 above lists a second
   payoff: State distinguishing "no ready edge yet" from "this row is not reported eligible
   for one". `GetValidAlertTypes` was **measured under-reporting**, so it is a **lower
   bound**, and branching readiness on a lower bound produces confident false negatives in
   the one place a wrong answer reaches the screen. Every alert list renders as
   **"reported eligible: …"**, with the cid-164597 measurement quoted in the dump's footer.
   Revisit only if a `TriggerAlertEvent` hook ever gives a complete observation.
2. **The wholesale guard, twice.** An empty scan is `ok = false, reason = "cdm-empty"` and
   reports **no** entry as untracked — an empty database means the read refused, not that
   your roster is blind. The deliberate twin of `domainView`'s `next(items) ~= nil` refusal
   and of §6.1's knownness guard. In combat `Get()` hands back the cached report marked
   stale rather than rescanning (the struct reads go secret in a pull). The zero-row case is
   **mutation-checked**: delete the guard and it goes red. There is a per-row twin too — a
   row that refused its fields could be carrying any id, so every untracked answer degrades
   to `unknown` rather than joining the alarm.
3. **Crashing Chaos 417234 is deleted** (`SpecDestruction.lua`), per the adjudication above.
   ⚠ **Consequence: the `blind` verdict now has no live instance and is proven by fixture
   only.** Stated here so a clean report is not mistaken for a tested path.

**Reuse, not re-derivation.** Virtual eligibility calls the real fence list —
`St.VirtualCandidates(specTable, {}, nil, known, baseCooldown)` — with an **empty**
`abilities` map, i.e. "if nothing were on screen, which of these would we synthesise?",
which is exactly the question the untracked branch asks. The fences are **not** copied into
`Coverage.lua`; that is how the two would drift and the report would start calling a drawn
ability blind.

**Why `St.CoverageRows` lives in State.** `enumerate` / `readInfo` / `readable` / `flagOf`
are the addon's only guarded CDM-database readers, and a copy of that walk in `Coverage.lua`
would be a **second guard ladder** over the same restricted API — the mistake §3.9 exists
about. `St.AuraFrameCapability` is the standing precedent for a diagnostic exported from
State. No new client reads: coverage is a question about the **database** (which ids exist
at all), not the domain view (which rows are pressable now), and the fold throws away
exactly the id fields the join needs.

**One nuance the live pass should watch.** The `virtual` fence requires
`known(spellID) == true`, so an untracked button whose knownness read **refuses** falls
through to `blind`. The per-row knownness annotation and a footer line say so, but if the
field shows this as a real false alarm, the fix is to ask the fence list a second time with
knownness forced true (still reuse, not re-derivation) rather than to invent a sixth verdict.

**Not built, and deliberately:** no `fixtures/cdm-cases.lua` additions — that corpus is
about State's fold, not this join, and its `#pinned + #fixed` floor is untouched.

### 5.2 ✅ FLOWN 2026-08-01 — and the flight changed two things

The pass ran on the **first `/cdmp flight`** (the acceptance recorder built the same day,
because collecting this by hand was ten slash commands, several typed mid-pull).
`wowkb.cdmp flight` reported **4 FAILURES** on the first read and now reports **ALL
CRITERIA PASS**. What held, and what did not:

**Held, unmodified.** All **nine** in-combat wholesale-guard checks — three pulls across
two specs — showing coverage served the cached report `stale` and invented no blind rows,
plus the cold-start rows refusing honestly with `reason = "in-combat"`. That was the
phase's most important claim and it needed no change. Spec + hero invalidation both fired.
Diabolic Ritual read tracked across its 4 rows; the four override-only ids read `expected`;
Crashing Chaos was absent.

**Changed #1 — `blind` was crying wolf, and every single instance proved it.** All three
blind rows were ids the character **does not have**: Axe Toss `119914` on both specs (no
Felguard) and Wither `445468` on Diabolist (untalented on that tree). Zero real findings,
three loud rows — the precise failure mode this report was built to avoid.
§5.1 pre-registered this as "the one nuance the live pass should watch"; the field hit it on
the first pass. **v0.32.54 adds two quiet rungs** to the untracked branch — `unlearned`
(knownness `false`) and `unknown` (knownness unreadable) — so **`blind` now means "the
character HAS this ability and the CDM tracks it nowhere"**, the only version of the claim
worth shouting. §5.1's pre-registered fix (re-ask the fence list with knownness forced true)
was **not** what was needed and is withdrawn: for `known == false` the answer is not "would
we synthesise it", it is "there is nothing to be blind to."

**Changed #2 — two acceptance criteria were wrong, not the code.** "Incinerate 29722 reads
`virtual`" and "Shadow Bolt 686 reads `virtual`" came from this document's own prose calling
them the ids "the CDM tracks nowhere". That conflates two different facts:

| | |
|---|---|
| **in the CDM database** | `GetCooldownViewerCategorySet(…, allowUnlearned=true)` carries the id. **This is what `coverage` joins on**, and Incinerate IS in it (1 row). |
| **displayed** | a live viewer frame exists to anchor a cue to. Incinerate is **not** — which is exactly why `HudVirtual` synthesises an icon for it. |

Both true simultaneously. The criteria became "must not be blind", and drawability moved to
its own **MEASURED** section of the report (it depends on the viewers being up, so it is not
something to fail a build over).

> ⚠ **THE OPEN CONSEQUENCE, and it is a real limit of this phase.** `counts.virtual` is
> computed in the **untracked branch only**, so it never runs for an id the database join
> already matched — and the live HUD *is* synthesising Incinerate while the report says
> **"0 our own icons"**. The count is an artefact of branch ordering, not a fact about the
> HUD. Coverage as shipped answers *"is this id in the CDM database"*; the question the HUD
> actually cares about is *"does this id have an icon — Blizzard's or ours"*. **Not fixed
> here** (drawability needs the viewers up, so it wants the same wholesale guard the
> database join has, and that is a design step, not a patch). Backlog: *status.md →
> Improvements*.

**Also discharged by the same ring** (no extra flying): Phase 3's owed Diabolist half —
`cd=164597` reads `spellID=348 (Immolate) key=F` on Diabolist against
`spellID=445468 (Wither) key=F` on Hellcaller, so the keybind ladder **falls through** to
whichever spell the row actually displays rather than having simply learned Wither. Phase 2's
DoT acceptance (**15 `not_up`** against a pre-Phase-2 baseline of **0**) and v0.32.47's
`ChargeGained` re-fly (Conflagrate 27.3 % of decisions, baseline 55.2 %) both passed.

> 📌 **Observed in passing, not chased:** the first Diabolist sample reads
> `cd=164597 key=None drew=F` and the next reads `key=F` — the `HudBinds` invalidate →
> rescan window after a talent swap, visible for about a second. Harmless (the DrawList kept
> the previous resolution meanwhile) but it is the first time that window has been observed
> at all.

---

## 6 · Phase 5 — anchor on the roster

With Phases 1–4 in place this is mostly subtraction.

- `enumerate()` still walks the CDM (we need the cooldownID ↔ spellID join), but the domain
  view is built from the **roster**, joined against it.
- A declared ability with a CDM row behaves exactly as today.
- A declared ability **without** one is a virtual row — no `virtualCandidates` fences needed,
  because the roster already answered "is this a press this spec cares about."
- `dropped` / `displayable` retire from the decision layer. Knownness survives as the
  **load-time** talent filter, which is what it was always for — but as a **mark**, not a
  delete. See §6.1, which is the load-bearing design decision of this phase.
- Refresh becomes periodic OOC (1–2 Hz) rather than per-tick.

### 6.1 ⚠ Knownness: MARK, don't filter — and guard the wholesale case

**This is the one place the inversion can go badly wrong, and it is not where it looks.**

Dropping an ability the client says you have not talented is not a loss — it is the correct
answer, and it is the whole point of the filter. The danger is the filter **not knowing** and
defaulting to removal.

**Why the roster anchor makes this harder than it is today.** The two knownness sources
currently carry **opposite defaults, and both are right**:

| Source | Role today | On an unreadable / refused answer |
|---|---|---|
| CDM `info.isKnown` | *removes* rows from the wide enumerated set | **keeps the row** — `dropReason` drops only on an explicit `false` |
| `C_SpellBook.IsSpellKnown` | *adds* virtual rows to a narrow set | **no row** — `virtualCandidates` requires `known == true` |

Each is the conservative choice *for its own base set* — one is conservative about removing,
the other about adding. Both are asserted by tests: *"an UNREADABLE isKnown is not a drop —
absence of a read is not evidence"* and *"a REFUSED knownness read ⇒ no row (under-show,
never a guess)."*

Anchor on the roster and those collapse into **one** question over **one** base set. There is
now a single default to pick and neither is safe: `nil → drop` silently deletes a real
ability, `nil → keep` reintroduces the Soul Fire failure for a roster ability that is
untalented in this build.

**So do neither.** Carry knownness three-valued on the row — `true | false | unknown` — and
let the Coach decide:

- **`false`** → never cue. Cheap and correct.
- **`unknown`** → ~~the Coach already owns this shape. `judgeable = false` + `secretGate`
  exist so an ability whose true gate is unreadable **caps at "available" and says why**
  rather than claiming it is the right press.~~
  ⚠ **CORRECTED 2026-08-03 — THAT MECHANISM DOES NOT EXIST.** Both fields are *declared* by
  the spec files and *read by nothing*: their consumer was `HudScore.lua`, deleted at the W4
  cutover, and the `JUDGE` emphasis token they fed was retired in W4 Phase 8. The plan was
  written against a capability the codebase had already lost.
  **The resolution costs nothing, because the two halves land in different places.**
  `guidance-contract.json` defines AVAILABLE as *"off cooldown but not a call — no cue"*, so
  **"cap at available" and "never cue" are the same pixels**: zeroing
  `ready`/`probablyUp`/`anticipated`/`overdue` on the finished record IS the cap, and it is
  the entire implementation (`usable()` in both brains needs `probablyUp` or a banked charge,
  `Emit`'s fallback needs a castable rec, `SOON` needs `anticipated`). The **"say why"** half
  lands in the decision log's `DR:` field — `<abbr>:unknown` — which is exactly where
  `pulse.dropped` used to say it. A new emphasis token / Binder reason pass-through /
  Renderer treatment would be the **`JUDGE` revival**, a contract change in its own right,
  and is filed in `status.md` rather than done here.
- Either way the row is **present and visible** in the pulse and the decision log, rather than
  absent without a trace. That visibility is what made the Soul Fire bug findable at all, and
  it is what replaces `pulse.dropped`.

**Three ways the read comes back unknown**, all real: a refused/`pcall`-failed read; **load
order** (the filter running before the spellbook is populated); and the **cache window**
(knownness is cached and invalidated only on `SPELLS_CHANGED`, so a wipe followed by a refused
re-read leaves a stale-empty answer).

> Note `C_SpellBook.IsSpellKnown` carries `SecretArguments = "AllowedWhenUntainted"`, but that
> governs whether a **secret argument** may be passed — a plain number spellID from addon code
> is fine. Rarer than the annotation suggests; the guard still earns its place.

**And keep the wholesale guard.** `domainView` already refuses to apply the `displayable`
filter when the frame map is empty (`next(items) ~= nil`), on the reasoning that an empty map
means "the viewers are not up yet," not "nothing is drawable." Knownness needs the identical
twin: **if the answer is `unknown` for the entire roster, that is a broken read, not an
untalented character — do not filter at all.** Without it, a load-order slip empties the
roster outright, which is the exact shape of the v0.32.25 total outage — and more dangerous
here, because there is no CDM breadth left to fall back on.

### 6.2 The sizing worry, answered

The periodic refresh is **not** a new cost — it is a large reduction of one already being
paid. `HudDriver.lua:39` ticks at 10 Hz with no OOC throttle, and each tick runs `State.Build`
over all ~64 rows. Per row, out of combat: `cooldownInfo` (1 pcall) + `ReadCooldown`
(`rawCooldown` 2 + `readCharges` 2 + **`rawCooldown(GCD)` 2**) + `ReadCharges` (2) +
`readGlow` (1) + `readAura`/`readBuffItem` (1–3) ≈ **10 guarded calls**.

≈ 700 per tick → **~7,000/sec out of combat**, plus three full viewer walks per tick
(`itemFrameMap`, `installAlertHooks`, `HudLayout.Scan`).

Roster-anchored: ~20 abilities + ~10 auras = 30 rows at 2 Hz ≈ **600/sec**. Over an order of
magnitude cheaper. (Phase 2.3's GCD hoist alone removes ~128 calls/tick before any of this.)

### 6.3 What actually shipped *(the record — 2026-08-03)*

The inversion landed whole, in one phase: the spec's declared roster is the anchor and the CDM
is **one evidence source joined against it**. Desk gates at the cut: **luacheck 0 warnings**,
**busted 883 tests / 0 failures / 4 pending** (from 737), corpus **107 cases / 0 pinned /
29 `fixed`**.

**The root fix (§C2)** is one line of intent: `readAbilityFacts(rid, rep)` passes the **roster
spellID** to both `readCd` and `readCharge`. Before, the cooldown ladder resolved on the
*display identity* while charges used `overrideSpellID or spellID` — two ladders, and on a row
whose identity flips mid-session (Judgment alternates with Hammer of Wrath in the tracked set)
they resolve to **different spells**, so the HUD compared one ability's cooldown against
another's charges. That is three of the five Retribution flight defects, one cause. The claimed
row's `cooldownID` still goes in, so `cdBaseline` / `readyEdge` / the charge napkin's gain-floor
seed cadence are unchanged.

**Eleven decisions were taken during implementation that this plan did not anticipate.** They
are recorded here because each was *forced* by something the plan text did not foresee, and a
fresh reader would otherwise "fix" them back:

1. **The third value of `known` is the STRING `"unknown"`, not `nil`.** `nil` has to keep
   meaning *"nobody asked"* — it is what every hand-built fixture pulse carries and what every
   consumer written before the field existed sees. Making absence mean "unreadable" would have
   capped every Coach-spec fixture row at once.
2. **The spellbook is the AUTHORITY; the CDM row's `isKnown` is the FALLBACK.** The naive fold
   ("false wins") is wrong: a row's `isKnown` describes the row's *base*, which on a
   display-overridden row is a different spell. On Hellcaller, cid 66181's base (Shadow Bolt)
   is unlearned while the ability it draws (Incinerate) is pressed every GCD.
3. **Unclaimed CDM rows cost no reads.** A row no declared ability claims gets
   `cd = {state="unknown", source="none"}` / `charge = {readable=false}` rather than its own
   read. **This is where §6.2's sizing win actually comes from**, and it is why the
   `asked.cooldownCount` assertions in `cdm-cases` had to move.
4. **`linkedSpellIDs` is deliberately NOT a domain-view join field** (Coverage's *is*).
   Coverage asks *"does the CDM know this id at all"*; the join asks *"which ability IS this
   row"*, and the pool is a bag of alternatives — joining on it lets one id claim a row that
   visibly draws another ability.
5. **Synthesis has THREE wholesale guards, not one:** no frame map · empty database · **any row
   with no resolvable base** (an unreadable row makes every "untracked" negative unprovable —
   Coverage's `unreadableRows` rule). Without them a refused CDM read puts *our* icon on screen
   for the whole rotation: the v0.32.32 duplicate at roster scale. ⚠ Guard 3 is keyed on
   `baseOfRow(entry, fold) == nil`, **not** on "the spellID read secret", so a warm in-combat
   pulse keeps drawing.
6. **`virtualCd`** — static `ready` / `source = "static"` only when `ns.BaseCooldown` genuinely
   reads 0; otherwise the real `readCd` ladder (no cooldownID ⇒ no baseline/edge, but the OOC
   read and the napkin both key on the spell). The virtual **charge** stays static, because the
   charge napkin is keyed by cooldownID and a virtual row has none.
7. **An undrawable *claimed* row keeps its row and its readings**, and merely takes the negative
   display handle. It is no longer dropped and replaced by a from-scratch static row — strictly
   better than the pre-Phase-5 Hellcaller path.
8. **`pulse.virtual` is the DRAW list and stays knownness-fenced** (`known == true`, or all of
   them when the wholesale guard fired). *Marking* buys visibility for free; an **icon on
   screen** for an ability you do not have is noise.
9. **Coverage's `blind` verdict narrows to `kind = "aura"` entries.** Every declared non-utility
   button now gets a virtual row, so the HUD cannot be blind to a *button* any more. ⚠ This
   makes acceptance criterion 4 nearly free — **report it honestly in the flight write-up
   rather than claiming a win.**
10. **cdm-cases fixture moves:** `TYRANT` → `SUMMON_INFERNAL 1122` in the four `spec = 3` cases
    that used a Demonology id; *"a trackedbuff row is never a press and never a drop"* split
    into an aura case plus a new **declared-button-tracked-as-a-bar** case (Immolate now DOES
    get a row — the CDM tracks it only as a tab-2 bar, and the roster says it is a button);
    `flags/charges-are-read-on-the-DISPLAY-identity` **inverted** into
    `flags/charges-and-the-cooldown-are-read-about-the-SAME-id`.
11. **`state_domainview_spec` runs Destruction throughout** (`H.setSpecIndex(3)`), and the
    "exactly one virtual row per spec" guards build their board from `St.RosterEntries`
    (`onScreenExcept(...)`) instead of a hand-listed id set — a hand-listed board silently
    stops covering anything added to the spec table later.

**Retained on purpose:** `CoachRetribution:usable()`'s `max == 1` invariant. Its cause is gone
(decision §C2 above), but deleting a guard in the same diff that removes its cause leaves a
regression in the cause with nothing beneath it. It is commented to that effect and retires on
its own, after a clean max-level `Judg=` / `Judg~` column.

**Two mutation checks were run, not merely asserted** (§Verification): deleting the
`(asked == 0) or sawReadable` term turns *"knownReadable is FALSE when the whole roster
refused"* red (plus a downstream Coach case); deleting the `info.expect ~= false` fence in
`virtualCandidates` turns four cases red, including both *"EXPECT=FALSE ⇒ no row"* and
*"…and the cast-id ALIAS beside it changes nothing"*.

**⚠ Still open — the aura half of the roster is write-only for State** (roster gap #2):
`kind = "aura"` entries claim no row and are never consulted. Recorded here, deliberately not
fixed in this phase.

---

## 7 · Phase 6 — move cast-*results* to the Coach

> **✅ SHIPPED 2026-08-01.** Jumped the queue ahead of Phase 5, exactly as §10 permits.
> **§7.1 is the record of what actually changed**, including the one deliberate behaviour
> change — the double-deduction guard was **dropped, not ported**. Read it before "fixing"
> that back.

Independent of Phase 5; can land any time after Phase 1. **Pure deletion from State:**

- `inflightIncoming` + `projectIncoming` + `spendStartShards` + `currentShardValue` —
  ~270 lines. *(⚠ The line numbers this plan originally cited, `State.lua:753-1025` and
  `:756` / `:1439`, were v0.32.41 coordinates and were already stale when Phase 6 ran.
  Symbol names only from here on.)*
- the `ns.SpecPowerDelta` injection — one of the four spec readers State consults
- **both `Enum.PowerType.SoulShards` hardwires** — the only class-specific literals in
  State's *code*, and the leak the review flagged

State returns raw `power` (keyed by `Enum.PowerType` name), `history`, and the current cast.
The Coach derives projected power as a **pure function of the pulse** — the same property the
architecture already prizes for the sequence cursor (`architecture.md` → *Sequence memory*),
and it moves the logic into the layer that is already fixture-tested.

**On charges and cast time.** Conflagrate is the project's only charged tracked ability and it
is instant, so "an ability mid-cast has already consumed a charge" is vacuous today. Deriving
it from `history` handles it for free regardless: a `start` with no later `succeeded` is
in flight, and charges-since-seed is a count of `succeeded` entries. No special case either
way, which is the point.

### 7.1 What actually shipped *(the record — 2026-08-01)*

**The move.** `ns.Coach.InflightPower(state, deltaFn, window)` is the whole replacement:
one pure walk of `state.history` for the latest phase per base inside a 3 s flight window,
summing the spec's signed `ns.SpecPowerDelta` per named power. It sits in Coach.lua's
*Small readers over the pulse* section beside `castingFresh`, which already performs a
structurally identical walk, and it is **public shell kit** (the `C.CommittedWithin`
precedent) because both brains read it from their `Context`. `deltaFn` is **passed in**
rather than reached for, so the helper is testable and the spec global is not a hidden
dependency. Net: **State.lua −147/+21 (−126 lines), Coach.lua +58.** *(The plan's "~270
lines" was measured against the pre-Phase-3 single-power version; the per-power rewrite had
already shrunk it.)*

`ns.SpecPowerDelta` stays a live-client read (it calls `ns.ShardCost`), which introduces
**no new class of impurity** at this layer — the brains' `costOf` already does live cost
reads through `env.shardCostFn`. Re-plumbing it through `env` was deliberately NOT done here.

**The leak is gone.** `State.lua` now contains **zero** `Enum.PowerType.SoulShards` and zero
`ns.SpecPowerDelta`; the only surviving `Enum.PowerType` reference in its code is
`buildPowerNames`' generic enum walk, which is what keys `power` by name in the first place.
A bonus fell out: `ns.ActiveSpec` was read in exactly one place in State (the deleted
`projectIncoming` call), so **State no longer touches the spec registry at all**.

**⚠ THE DOUBLE-DEDUCTION GUARD WAS DROPPED, NOT PORTED — a knowing behaviour change.**
`spendStartShards` snapshotted live `UnitPower` *at the `UNIT_SPELLCAST_START` event* and
suppressed a spender's −delta once the live value fell below it. A pure function of the pulse
has no `before` value to diff against; preserving it would have meant stamping the snapshot
onto the history entry, i.e. keeping the mechanism and merely relocating its state. The
minimal deletion was chosen instead, with eyes open:

- **The accepted cost** is a stale −N for **at most one ~10 Hz tick** at completion.
  `SUCCEEDED` supersedes the `start` on the very next pulse, and often lands before a Build
  even runs — making the window zero in practice.
- **It removed two latent defects outright** rather than carrying them forward. The snapshot
  **leaked**: the terminal-event branch cleared it only when the spellID read *readable*, so a
  secret terminal event left the map entry alive into the *next* cast of that spender, which
  then silently under-projected for a full flight window. And the comparison was **already
  wrong for a multi-power spec** by its own in-code admission — it compared a `SoulShards`
  live value against any spender's snapshot, correct only because Demo has one spender-power.
- **No test covered the guard**, in State or anywhere else. That is precisely why this is
  written down: the next reader must not "restore" it on the assumption it was load-bearing.

**`"stopped"` became load-bearing, and is finally documented.** The third cast phase has
existed since W4 P6 Part 2 but appeared in no contract. It is the only thing that lets a
latest-phase-per-base walk cancel a mid-flight spender, so the four terminal
`RegisterUnitEvent` lines at the bottom of `State.lua` — `INTERRUPTED` / `FAILED` /
`FAILED_QUIET` / `STOP` — now look orphaned *from inside State* while the Coach depends on
them. Both files carry a ⚠ saying so, and `architecture.md`'s Stage-1 `history` block
documents all three phases.

**The trace kept the information.** `DecisionLog`'s `PW:` field read
`pulse.power[…].incoming` directly, which stops being written, so it was re-pointed at
`guidance.resourceBars[1]` — which already carries **both** `value` and `incoming`, so the
whole string now comes from one place. Two consequences accepted deliberately: a passive spec
(`EmptyGuidance` → `resourceBars = {}`) renders `PW:?/?` rather than reading through to the
pulse (honest — there is no bar), and the secret-degradation now happens at the *Coach*
boundary (`ResourceBars` floors a non-numeric value to 0) rather than at the log's. The log
keeps its own `?` guard anyway, since it is a formatter over a channel it does not own.

**Tests: 624 → 630, 0 failures, luacheck 0 warnings.**
- `resource_multipower_spec` — the dual-power seam proof **moved to the Coach**, re-pointed
  from `ns.State.InflightIncoming`/`ProjectIncoming` at `ns.Coach.InflightPower`. It is the
  proof the **per-power map survived** the move. Its synthetic 2-power brain's `Context` now
  mirrors the real brains (derive `sums`, fold onto declared powers), so the whole path is
  under test rather than the two ex-State cores in isolation.
- **The latest-phase-supersedes rule is now tested for the first time** — it was untested in
  State and was the behaviour most likely to break silently here. Five new cases: a
  `succeeded` cancels the projection, a `stopped` cancels it while leaving a sibling power
  untouched, a **re-cast after a terminal phase projects again** (latest phase wins, not
  "ever terminal"), an aged-out `start` drops, and a nil `deltaFn` yields an empty map.
- `coach_apl_spec` / `coach_destruction_apl_spec` — the fixture builders' `f.incoming` no
  longer sets a pulse field the Coach ignores; it synthesises a **real in-flight spender**
  (HoG / Chaos Bolt) plus the live `ns.ShardCost` its `SpecPowerDelta` reads, so the fixtures
  now drive the actual derivation. Placed at `NOW - 2`: inside the 3 s flight window but
  outside `CAST_FRESH` (1.0), so it does not also raise a `cast_started` edge. Every existing
  call site (`winner{ shards = 5, incoming = -4 }`, …) works unchanged.

**Two things noted, not done** (they would have widened the diff): the five byte-identical
`Context` lines shared by both brains are still duplicated, and `architecture.md`'s Stage-1
block still carried a `resources.shards` alias retired back in Phase 3 — that one line was
corrected in passing since it named `incoming`.

---

### 7.2 Phase 6.2 — Soul Shard *fragments*, the exact resource rail *(2026-08-01)*

**Why there is a 6.2 at all.** Flying Phase 6 surfaced a limitation that is not about *where*
the projection lives but about **what it can represent**:

> *"I can't accurately tell you to do X as you're casting Y if I can't know that you have 1.8
> shards and Y gives you .2 so you'll have 2 and that's enough for X."*

`State.lua`'s `readOnePower` called `UnitPower("player", pt)` with no `unmodified` flag, so
the whole pipeline saw **whole shards only**. A true 1.9 arrived as `1`, `shards >= 2` was
false, and the HUD said "build" when you were one Incinerate tick from a Chaos Bolt. That is
a **missing capability, not imprecision** — and `status.md` had it filed as *"rotation
quality, not correctness"*, which was wrong and is corrected in this diff.

**Measured in game 2026-08-01, so nothing here is speculative:**

```
UnitPowerMax("player", SoulShards)        = 5     UnitPower(…) = 3
UnitPowerMax("player", SoulShards, true)  = 50    UnitPower(…, true) = 30
```

Fragments confirmed, **modifier 10**, and the call **works in combat** — closing the
Secret-Values question that gated this for a month. `ShouldUnitPowerBeSecret` takes
`(unit, powerType)` (`knowledge/addon-dev/security-taint-and-restricted-data.md`), so the
`unmodified` flag is not a parameter of the verdict, which is exactly why it behaves
identically.

> ### ⚠ CORRECTION (2026-08-03) — "the flagged read WORKS IN COMBAT" is TRUE FOR SOUL SHARDS AND FALSE FOR MOST OF THE GAME
>
> The paragraph above is **correct as a measurement and wrong as a generalisation**, and the
> generalisation is the one that got used. What it measured is Soul Shards; what it was read
> as saying is *"`UnitPower` works in combat"*. It does not.
>
> **Secrecy is per POWER TYPE, and the rule is primary vs. secondary resource.** Blizzard blue
> post, *Midnight Public Alpha Addon API Changes*, 2025-11-24: *"We have relaxed restrictions
> around `UnitPower` so the player's **secondary** resources are no longer secret (**primary
> resources remain secret**). Affected resources: Combo Points, Runes, Soul Shards, Holy
> Power, Chi, Arcane Charges, Essence."*
>
> Soul Shards are on that list. So are Holy Power. **Fury, Rage, Energy, Focus, Mana, Runic
> Power, Pain, Insanity and Maelstrom are not** — and the sentence above is the reason nobody
> checked before shipping Havoc. `C_Secrets.GetPowerTypeSecrecy(17)` (Fury) is **2**
> (`ContextuallySecret`) and `ShouldUnitPowerBeSecret("player", 17)` is **true in a city and
> mid-pull alike**; the "context" is the UNIT, not combat.
>
> **What it cost:** the Havoc flight, 2026-08-03. Every Fury gate compared against a
> fabricated zero, and the core rotation was unreachable for a whole session. The remediation
> is `specs/havoc/rotation.md` → *Fury is SECRET* and
> `knowledge/addon-dev/security-taint-and-restricted-data.md` §4.12.
>
> ⚠ **The `unmodified` sub-claim survives intact** — the flag genuinely is not a parameter of
> the secrecy verdict. It is the scope of "works" that was wrong, not the mechanism.
>
> **The first four specs this project shipped were LUCKY**: Soul Shards ×2 and Holy Power ×1
> are all never-secret. Of the remaining rollout, Protection Paladin is Holy Power (safe) and
> **Vengeance and Devourer are both Fury**.

#### The unit model, and why it is INTEGERS

WoW stores fragments 0–50; simc divides by 10 at the DBC layer and works in whole shards as a
`double`, so `soul_shard<=4.2` means **42 fragments**. The client hands us an exact integer,
and **we keep it that way**. Dividing by 10 manufactures an imprecision the source does not
have, and this is a **boundary comparison** problem — the exact case where binary floating
point bites. A projected total that should be `2.0` can come out `1.9999999999999998`, `>= 2`
fails, and a cast that is available is withheld: the same wrong answer as rounding, but rarer
and unreproducible. `InflightPower` **sums** deltas, and summing integers is exact. simc uses
doubles, but simc is not making 10 Hz boundary decisions. **Floats live at the edges** —
`DecisionLog`'s `PW:1.8`, log prose — never inside a gate.

#### The five design decisions

1. **Integer fragments internally, never floats** (above).
2. **Rename, don't re-unit.** If `ctx.shards` had kept its name and changed meaning, a missed
   `shards >= 2` would compile fine and be silently wrong by 10×. Every gate field is renamed
   — `frags` / `fragsIncoming` / `fragsProjected` / `fragsMax`, `*CostFrags`, `*_FRAGS`
   tunables — so a stale call site gets nil and fails loudly. `ctx.shards` is **deleted**, not
   repurposed. `spec.SHARD_CAP` became `spec.FRAG_CAP` (50) for the same reason, and
   `Coach.lua`'s file-local fallback became `BAR_MAX_FALLBACK` because it is a **display**
   number. This is the mitigation for the phase's headline risk; an incomplete rename is what
   `grep -rn "ctx\.shards\|SHARD_CAP\|Cost\b" Coach*.lua` exists to catch.
3. **State stays spec-agnostic.** Phase 6 removed State's last class-specific literal and this
   phase does not reintroduce one: the new fields use Blizzard's own vocabulary —
   `unmodified` / `unmodifiedMax` / `modifier` — not "fragments", which is a Soul-Shard word.
   `modifier` is **derived** from the two maxes, not assumed.
4. **Guidance keeps whole shards; the exact values ride alongside.** ⚠ `Renderer.lua`'s
   `drawResourceRow` pools **one pip texture per unit of `max`**, so a `max` of 50 would try
   to draw fifty pips. `resourceBars[].value`/`max`/`incoming` therefore stay in display units
   and **the Renderer is untouched**; the bar gained additive
   `valueExact`/`maxExact`/`incomingExact`/`modifier`.
5. **Builder projection is fenced to the conservative floor.** Incinerate's crit bonus is
   deterministic *given a crit* and the crit is not; Immolate's is 50 % on a crit tick. Only
   base yields are projected. Under-crediting delays a cue by one press; over-crediting
   promises a cast you cannot make. Same doctrine as the charge napkin's undercount.

#### ⚠ THE COST DENOMINATION WENT THE OTHER WAY

```
/run for _,id in ipairs({116858,105174}) do for _,c in ipairs(C_Spell.GetSpellPowerCost(id) or {}) do print(id,c.type,c.name,c.cost) end end
→ 116858  7  SOUL_SHARDS  2      → 105174  7  SOUL_SHARDS  3
```

**The client API pre-applies the divisor.** DB2 stores Chaos Bolt's cost as `20` fragments and
`C_Spell.GetSpellPowerCost` hands back **2**. Two consequences:

- **`ns.ShardCost`'s fragment heuristic was DELETED, not generalised.**
  `if raw >= 10 and raw % 10 == 0 then return raw / 10` can only fire on a shard cost of ≥ 10,
  impossible against a five-shard cap. It never fired, and its `@verify-ingame` marker pointed
  at the decision log — which could not have answered the question anyway, since a raw 3 and a
  raw 30 both render `3`. The **type filter stays**; that part is load-bearing.
- **Costs arrive in shards while the bar arrives in fragments**, so every cost is multiplied
  **UP at exactly one site per brain** (`Context`) and renamed `*CostFrags` from there down.
  The fallbacks (`CB_COST_FALLBACK = 2`, …) stay in shards and cross the same boundary, so
  each brain has exactly one crossing.

#### What shipped

- **State** — `readOnePower` gained a guarded `pcall(UnitPower, "player", value, true)` +
  `UnitPowerMax(…, true)`, emitting `unmodified` / `unmodifiedMax` / `modifier`. Same secrecy
  ladder; **absent, never zero**, on a refusal. `value`/`max`/`readable` are byte-identical.
- **Coach** — both brains derive `ctx.frags*` from `unmodified`, falling back to
  `value × modifier`. Every gate moved, **including both LATE-at-full-bar rules**, which now
  read `frags >= fragsMax` (50, not 5) — the two comparisons that most look like whole-shard
  ones and are not.
- **Simc's fractions are restored.** `<= 4.2` (Conflagrate, `warlock_destruction.simc:33`) and
  `<= 4.6` (Chaotic-Inferno Incinerate, `:36`) are back as 42 and 46, hardcoded **with a
  citation** rather than derived: `4.6 + 0.4` is exactly 5.0, which makes them *look* like
  overcap guards computed off the yields, but `4.2 + 0.5` is 4.7 — suggestive, not exact.
- **Yields** — `SpecDestruction` grew fragment `generatesFrags` (Incinerate 2, Conflagrate 5,
  Soul Fire 10, Infernal Bolt 20), base values only. Immolate/Wither carry **none**: their
  income is per-tick, and the in-flight projection answers "what will the bar read when this
  cast resolves". **Diabolic Embers (387173)** doubles Incinerate and is read via
  `C_SpellBook.IsSpellKnown`, cached through the registry's `Invalidate` seam — **the first
  spec to use it**, which was left wired for exactly this. A refused read assumes untalented
  and does **not** cache, so it self-heals. The MID1 4-set's +2 on Conflagrate is
  knowingly skipped (no tier-set channel on the pulse; the failure direction is safe).
  Demonology's yields converted 1/2/3 → 10/20/30, and `generates` was renamed
  `generatesFrags` on both specs by the same loud-failure argument as decision 2.
- **The trace** — `DecisionLog`'s `PW:` prefers `valueExact`/`incomingExact` and divides at
  the edge, so it prints `PW:1.8/+0.2`. **An all-integer `PW:` column in a capture means the
  exact read is not wired**, which is the in-flight acceptance signal for this phase.

#### ⚠ THE `>= 3.5` PUZZLE — the KB was misleading, and is corrected

The in-game tooltip saying **3** is right; Rain of Fire costs 30 fragments on both spell IDs.
The `3.5` is a **hand-tuned APL constant, Diabolist-AoE only**, gated `active_enemies>=4`:

```
:48  rain_of_fire,if=((soul_shard>=(3.5-0.1*(active_dot.immolate)))|buff.alythesss_ire.up)&active_enemies>=4
:63  rain_of_fire,if=(soul_shard>=(4.0-0.1*(active_dot.wither)))&active_enemies>=(5-talent.destructive_rapidity)
:68  rain_of_fire,if=active_enemies>=(5-talent.destructive_rapidity)          ← no shard condition at all
```

The `-0.1 × active_dot` term is exactly one Immolate tick's yield per active DoT, so it reads
as income anticipation — but the buffer **shrinks as income rises**, which is backwards for a
pooling reserve, and at 8 Immolates it falls **below** the real 3-shard cost. Nothing in the
APL, the generator or the C++ explains it, so no rationale is invented here. **Rain of Fire
stays on a plain integer floor**: the gate is hero-tree- and AoE-specific, has an
unconditional fallback the KB never mentioned, and the brain has no `active_dot` count to feed
it. Recorded in `specs/destruction/rotation.md` rather than half-implemented.

#### Open, and deliberately not blocking

- **Infernal Bolt 20 vs 30 on Destruction** — the one place the two simc researchers
  disagreed (agent 1: the spec aura `137046 e#13` applies −10; agent 2 read the unmodified
  30). **20 is taken** because it is the lower figure and the floor is the contract. It is
  Diabolist-only, so it gates nothing. Settle it by casting one and watching the bar move 2
  shards or 3.
- **Crit yields are unprojectable**, fenced to the floor by design.
- **Yields are gear- and talent-dependent** and authored constants will drift; the alternative
  is a live energize read the API does not expose.

**Tests: 645 → 689, 0 failures, luacheck 0 warnings.** The fixture builders keep `f.shards`
in **whole shards** and multiply by 10 internally, so all ~146 existing `shards = N` call
sites work unchanged — the same trick Phase 6 used for `f.incoming` — with `f.frags`,
`f.inflight` and `f.exactRefused` as the new escape hatches. New coverage: the motivating
boundary (**18 fragments + an in-flight Incinerate makes Chaos Bolt the press; 17 + 2 does
not**, with the display rail asserted to read `1` in both, which is the mutation check), the
two restored gates at 42/43 and 46/47, the unit boundary asserted **as a number** rather than
only through the press it produces, the exact read refusing, `modifier == 1` as a no-op, the
Diabolic Embers cache and its invalidation, and — the regression the deletion is really about
— `ns.ShardCost` returning a raw `20` as `20`. `util_shardcost_spec.lua` is new and is the
first test of the **real** `ns.PowerCost`/`ns.ShardCost` ladder; every other spec reads costs
through the harness override, which proves the callers and nothing about the reader.

**Two things filed rather than done** (`docs/status.md` backlog): **partial-fill pip
rendering** — the decision layer now knows the bar sits at 1.8 while the HUD still draws two
lit pips of five, blocked on the Renderer's per-pip loop, **not** on the read — and
**projecting an in-flight cast's COOLDOWN effect** the way this phase projects its resource
effect.

---

## 8 · Risks, stated plainly

> ⚠ **Corrected 2026-07-31.** An earlier draft of this section led with "the failure direction
> flips from over-show to under-show," on the strength of a forgotten ability becoming
> invisible. That was **overstated on two counts** and is retained here so the reasoning is not
> re-derived: (a) it conflated *authoring omission* with *talent filtering* — filtering an
> ability the client says you have not talented is simply correct, not an under-show; and (b)
> the omission case loses less than claimed, because **keybind hints come from the Layout, not
> from `abilities`** (`HudLayout.Scan` walks the viewers independently, and Phase 3 separates
> the channel outright), and `pulse.cooldowns` can be retained as-is since `enumerate()` still
> runs for the id join. The real risk is narrower and lives in §6.1.

- **`unknown` knownness being treated as `false`** — the genuine under-show, and the reason
  §6.1 exists. Mitigated by marking rather than filtering, plus the wholesale guard. **This is
  the risk to design against; the rest are bookkeeping.**
- **The `pulse.dropped` diagnostic changes shape.** Its per-pulse "the filter removed a real
  button, and why" is what made the Soul Fire bug visible. Roster-anchored there is no filter
  to report from, so the visibility has to come from two replacements: the three-valued
  `known` riding the row (§6.1) and Phase 4's load-time coverage report. Both must actually be
  built, or a loud failure is traded for a quiet one.
- **Roster maintenance becomes correctness-bearing.** Adding a spec means enumerating its
  auras, not just its buttons. Phase 4's coverage report is the guardrail.
- **Authoring omission is now silent in the decision layer** — though, per the correction
  above, `RankWinner` already gates on `ctx.facts[base]` and never names an undeclared spell,
  so cue behaviour is unchanged; only the diagnostic breadth narrows, and only if
  `pulse.cooldowns` is dropped too.

---

## 9 · Open questions — ✅ ALL THREE ANSWERED 2026-07-31

The `/cdmp census` + alert-tape capture (Destruction, both hero trees, 72 cooldownIDs, in and
out of combat) closed every question this plan was gated on. Kept, struck through, because
the answers reshaped three phases and the reasoning should not be re-derived.

- ~~Does a fresh read carry the elected `linkedSpellID`?~~ → **No, and neither does the
  frame.** It is never elected. Rung 2 leaves the Phase-3 ladder; rung 4 carries Wither. (§4.1)
- ~~Do any tab-1 rows set `hasAura`/`selfAura`?~~ → **Yes, 17 of them, including Immolate.**
  §3.1 is live, and it is the worst of the six. (§3.1)
- ~~Do `wasSetFrom*` and `auraDataUnit` survive restricted combat?~~ → **Both do.** That plus
  `PandemicIcon` is what makes §3.10's fix possible at all.

**Newly open, from the same capture:**

- **Does the rung-2 election ever fire on any spec?** It did not on Destruction in either hero
  tree. If it never does, rung 2 is dead weight in every consumer's ladder, not just ours.
- **How far does `GetValidAlertTypes` under-report?** One row was measured raising an edge it
  did not list (§5). Phase 4 is built on this API; the size of the error matters.
- **Do `auraDataUnit` / `PandemicIcon` behave the same on a PLAYER-side aura?** The cycle was
  measured on a target DoT. Pandemic only ever arms for `GetAuraDataUnit() == "target"`
  (`CooldownViewer.lua:515`), so the self-buff case is unmeasured and Demonology's whole
  roster is self-buffs.

---

## 10 · Suggested order

```
Phase 1  fixture harness + CDM edge inventory      ← ✅ DONE 2026-07-31 (the net)
Phase 2  the correctness fixes (all ten)           ← ✅ DONE 2026-07-31, v0.32.46 (see §3.11)
Phase 3  keybind channel separation                ← ✅ DONE 2026-07-31, v0.32.48 (see §4.2)
Phase 4  roster coverage probe                     ← ✅ DONE 2026-07-31 (see §5.1), FLOWN 2026-08-01 (§5.2)
Phase 6  cast-results → Coach                      ← ✅ DONE 2026-08-01 (see §7.1) — it did jump the queue
Phase 6.2 Soul Shard FRAGMENTS (the exact rail)    ← ✅ DONE 2026-08-01 (see §7.2), awaiting its in-game pass
Phase 5  roster anchor inversion                   ← ✅ DONE 2026-08-03 (see §6.3), awaiting its in-game pass
```

**✅ THE PLAN IS COMPLETE.** Every phase is code-complete and green at the desk. What remains
is not code: **one max-level Retribution flight** discharges Phase 5's acceptance, Phase 6.2's
fragment pass and the owed v0.32.36 re-fly together. `docs/status.md` owns that gate.

**⚠ PHASE 2's INTERNAL ORDER WAS EVIDENCE-LED, not the §3.1→§3.9 numbering.** The 2026-07-31
capture measured every trigger, and the numbering predates it. **This is the order it shipped
in**, kept because it is the reasoning a future phase should copy:

| Order | Item | Why here |
|---|---|---|
| 1 | **§3.1** (family gate) + **§3.10** (consume `auraDataUnit`/`PandemicIcon`) | Do them TOGETHER. §3.1 alone removes the false "up" and leaves the DoT read with nothing; §3.10 supplies the replacement. Apart, the first is a regression. |
| 2 | **§3.3** GCD hoist | Unchanged: pure win, no behaviour change, one number in one fixture. |
| 3 | **§3.4** `isKnown` | Two-sided, both directions silent, no trigger needed — it is always wrong. |
| 4 | **§3.6 / §3.7 / §3.8** | Real, bounded, no measured blast radius. |
| 5 | **§3.2** charges ladder | Correct but currently inert: no charged row carries a rung-3 override. |
| 6 | **§3.5** display ladder | Trigger exists on two *utility* rows only. Fix calmly; it touches the v0.32.36 seam. |
| 7 | **§3.9** bare struct index | Crash path real, trigger **absent**. Cheapest to leave pinned. |

⚠ In the event **§3.9 was fixed too**, folded into C5 alongside §3.4 — both touch the same
struct read, and guarding it once was cheaper than guarding it twice. Nothing was left pinned.

**The Phase-2 workflow
was mechanical, and it worked exactly as designed:** make the fix, watch the named case go RED
(a `pinned-defect` errors when it starts passing), flip its `status` to `"green"` + `fixed` in
the same diff, and the message the runner prints tells you which one and why.

**Phase 1 did not warrant a release cut, and did not get one** — say so out loud, because the
next reader will otherwise assume it was forgotten. It touches `tests/` only, which is deliberately
absent from `CDMProbe.toc` and never loaded in-game — nothing to `/reload`, nothing to eyeball.
The project's standing auto-deploy exception did not apply. **Phase 2 cut once, at the end
(v0.32.46)**, rather than per fix: the ten commits are individually green but only the whole set
is meaningfully flyable, since §3.1 without §3.10 is a regression. ⚠ Note `busted` **is** a hard
release gate (`tools/wowkb/addon.py:373-385` aborts the cut on a non-zero exit), so from the
first fixture commit onward a flaky case blocks *every* future release: fixed clock, no
`pairs`-order dependence, one case per `it`.

# Cooldown HUD — the roster-anchored State

> **STATUS: ▶ PHASE 4 IS CURRENT. Phases 1 + 2 + 3 done (2026-07-31); Phases 4–6 planned.**
> (§10 also permits **Phase 6** to jump the queue — it is independently shippable today and
> touches nothing else.)
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
> scheduled for deletion. **Promote it before the tape goes.**

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
- **`unknown`** → the Coach already owns this shape. `judgeable = false` + `secretGate` exist
  so an ability whose true gate is unreadable **caps at "available" and says why** rather than
  claiming it is the right press. Unknown knownness is the same class of claim.
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

---

## 7 · Phase 6 — move cast-*results* to the Coach

Independent of Phase 5; can land any time after Phase 1. **Pure deletion from State:**

- `inflightIncoming` + `projectIncoming` + `spendStartShards` + `currentShardValue` —
  ~270 lines, `State.lua:753-1025`
- the `ns.SpecPowerDelta` injection — one of the four spec readers State consults
- **both `Enum.PowerType.SoulShards` hardwires** (`State.lua:756`, `:1439`) — the only
  class-specific literals in State's *code*, and the leak the review flagged

State returns raw `power` (keyed by `Enum.PowerType` name), `history`, and the current cast.
The Coach derives projected power as a **pure function of the pulse** — the same property the
architecture already prizes for the sequence cursor (`architecture.md` → *Sequence memory*),
and it moves the logic into the layer that is already fixture-tested.

**On charges and cast time.** Conflagrate is the project's only charged tracked ability and it
is instant, so "an ability mid-cast has already consumed a charge" is vacuous today. Deriving
it from `history` handles it for free regardless: a `start` with no later `succeeded` is
in flight, and charges-since-seed is a count of `succeeded` entries. No special case either
way, which is the point.

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
Phase 4  roster coverage probe                     ← ▶ CURRENT. Its API prerequisite landed in Phase 3
Phase 6  cast-results → Coach                      ← independent deletion, can jump the queue
Phase 5  roster anchor inversion                   ← last; the largest blast radius
```

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

Phase 6 remains independently shippable today and touches nothing else. **The Phase-2 workflow
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

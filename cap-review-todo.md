# cap — catalog review findings (2026-08-25)

**What this is.** Five independent read-only reviews, one per spec, each comparing the spec's
catalog against its upstream SimulationCraft priority list and against the ten BUILT primitives.
Run immediately after the provenance pass that added `apl` / `exception` / `drawn_by` to the four
migrated catalogs and created `specs/render-primitives.json`.

**Scope.** Demonology, Havoc, Protection, Retribution (full — `catalog.json`), Devourer (reduced —
still hand-written `catalog.md`). **Destruction was not reviewed**: `backlog.md` records it shelved.

**Gate state at time of review, and now.** `capart check --all` green, `busted` 232/0, `luacheck` 0,
all four catalogs round-trip byte-identical to their committed Lua. **Every finding below is
something no gate looks at.** That is the point of the exercise, not an aside.

**Confidence marks.** `[verified]` = I re-checked it against the files myself. `[reported]` = the
reviewer's claim with its cited evidence, not independently re-checked. `[speculative]` = the
reviewer marked it as needing a judgement call or a client measurement.

---

## 0 · Already fixed — do NOT redo

Four defects were fixed during the review because each was introduced by the provenance pass
itself, or was a plain factual error contradicting it. All verified, all gates re-run green.

| Fix | What it was |
| --- | --- |
| `protection/catalog.json` `as_band_armed.condition` | Read *"its count below five"* under `verdict: ruled-sealed`, but its band draws `mark`+`hatch` at `threshold: 5` — nothing is drawn below five. Now *"at five or more"*. Found before the reviews; Protection's review independently re-verified the fix as correct. |
| `capart.py` `_check_one`'s success banner | I made it name the two new catalog gates unconditionally, so `check devourer` / `check destruction` claimed gates that never ran (they are inside `if cjson.exists()`). Now prints `(catalog gates SKIPPED — no catalog.json)` for those. Caught by the Devourer review — one of the two specs it was lying about. |
| `drawn_by` on `sotr_starved`, `tv_starved`, `ds_starved` | I derived `drawn_by` as *"primitives in play on this row"* rather than *"what draws in THIS state"*, so V13 (scan edge) was listed on states that fail their entry's `scan_when` and are therefore non-members. `Treatment.lua:47` is `scan = verdict.member == true`; cues are returned regardless. V13 dropped from those three. ⚠ Deliberately NOT `woa_starved` — Wake of Ashes' `scan_when` is a two-alternative OR and its transformed life satisfies the second, so that row IS a member while starved. Found independently by both Protection (A7) and Retribution (4). |
| `retribution/catalog.md` lines 22, 174, 175, 256, 279 | The five `cooldowns` rung citations were off by one (Execution Sentence is rung 10, Avenging Wrath 11). `catalog.json` had them right. Worst instance was line 22 — the ⚠ that *teaches* the citation convention, using a wrong worked example. |

---

## 1 · The two cross-cutting patterns

These matter more than any single finding, because each recurs across specs and each has a
mechanical shape you can grep for.

### Pattern A — a hold names the row it yields to, but never checks that row is AVAILABLE

Four instances across three specs. Each **eliminates the correct press** in an ordinary state,
each is a one-term fix, and **in every case a sibling marker in the same file does it right** —
so this is inconsistency within a file, not a missing idea. Scenarios miss them because each
scenario pins the hiding branch into its own state string.

| Spec | Marker | Missing term | Consequence |
| --- | --- | --- | --- |
| Protection | `as_guidance_capped` | `ready(consecration)` | DG ≥ 5 + Consecration swiped ⇒ client hatches Avenger's Shield `ruled-sealed` (an eliminating signal) while the APL's press IS Avenger's Shield at rung 18 |
| Protection | `judgment_awaits_assurance` | `ready(crusader_strike)` | Both Blessed Hammer charges down ⇒ rungs 20/21 cannot fire, rung 22 (Judgment) is the press, cap wears `blocked` on it |
| Demonology | `hog_awaits_tyrant` + `hog_awaits_shards` | `identity(hand_of_guldan, "base")` | Both holds fire on the row's OTHER life, Ruination (`diabolist 10`, **unconditional**, ranked above the rung the holds come from) |
| Retribution | `boj_opener` | `resource <= 4` | `generators 2` sits below `generators 1`, which leaves for `finishers` at 5 HP — so at 5 HP with WoA down the APL never reaches the opener rung, but cap draws the gold ring and **pass 1 presses it without running elimination** |

**Suggested standing check** (not built): for every marker whose `note` or `condition` names
another row as the outranker, assert the `when` carries a readiness/identity term for that row.

### Pattern B — recorded defeats that went STALE under V16–V20

Roughly half the "we cannot do this yet" claims across the catalogs are no longer true. The
primitives pass did not only add fields; it made these claims checkable, and they failed.

| Spec | The claim | Why it is stale |
| --- | --- | --- |
| Protection | Defeat 3: rung 10's `buff.sacred_weapon.remains<6` needs *"an aura-remaining band — an S-form nobody has written"* | V19's `outside_s` shipped 2026-08-24 and is live code (`Channel.lua:214-224, 638, 839`; `Catalog.lua:306-314`). Direction matches exactly: V19 hatches while there is plenty left. `outside_s = 6` is the APL's own number. |
| Protection | Defeats 4 + 5: `capped` *"has no subject"* without a `charged` declaration and a Tier-1 charge count | `Sense.lua:96-106` `readCapped` calls `C_Spell.GetSpellCharges` **live**, reads `maxCharges` off the client, self-withholds at `maxCharges <= 1`, and never consults `ability.charged` (`Track.lua:190-193` says so explicitly). |
| Devourer | Cue C parked on *"needs `Channel.Plan`'s `min == 2` guard widened first — widening that guard is the whole of the work"* | The form and the guard were **deleted 2026-08-22**; `Catalog.lua:235` records the replacement. Cue C is a `sealed-count-bands` (V16) or `sealed-count-bar` (V18) declaration today, with no engine change. |
| Devourer | Open fact 3 (`IsSpellUsable` for aura-granted access) as *"the single most load-bearing open fact"* | V17 obviates it for two of its three consumers — both are sealed aura counts, which is exactly what V17 draws without cap reading anything. Only Collapsing Star's gated virtual row still needs it. |
| Havoc | Open facts 1-3 framed as *"is this window's active-state readable?"* ⇒ no hint until answered | Correct for **promotion** (emphasis may only move on a readable fact) but not for **display**. V20 needs no read — visibility is the gate. Split each into a promotion half (still open) and a display half (available today). |

---

## 2 · Per-spec findings

### Demonology

1. **`[reported]` Ruination inherits Hand of Gul'dan's holds — a wrong press.** Pattern A above.
   `catalog.json:675-698` + `:700-728`; the rung is `simc-apl.md:58`. Also fills the only
   `diabolist` rung with no state citing it anywhere. **Not** a recorded defeat — `catalog.md:218-219`
   addresses row *position* and never notices the holds are rung-11-specific. Fix: two `identity`
   terms + a `hog_ruination` state citing `diabolist 10` + a walk (DEM-16: Ruination armed during
   the ramp).
2. **`[reported]` `fact-classification.md` lags the code by one release.** Says the catalog uses
   *five* sealed values (`:23`) and that Tyrant's two-sided band is *"sealed, no authored form"*
   (`:82`, `:71`, `:205-209`) — cue J shipped 2026-08-24. `catalog.md:242-245` carries a matching
   stale claim. Staleness doctrine 7: rewrite the rows, don't append.
3. **`[reported]` The safety case denies a risk that is live.** `fact-classification.md:298`:
   *"This catalog authors no `aura` marker at all"* — `implosion_no_imps` (`catalog.json:513-526`)
   is exactly that marker, and the same file documents it twice (`:78`, `:227`). The sentence that
   loses is the one making the safety claim. Real exposure: cue H depends on the player having the
   Wild Imp tracked-buff row enabled; failure direction is a missed skip, which is acceptable and
   should be *said*.
4. **`[speculative]` Implosion argues with itself.** Single target with 6+ imps ⇒ a **gold**
   numeral in the ceded corner *and* the red `aoe_only` badge. Unwalked, so `check` cannot see it.
   Fix: partition the band into two display markers gated by mode/talent; or drop the high band to
   `draw: "none"`.
5. **`[speculative]` V18's red-at-full on Demonbolt makes a claim no rung makes.** At 4 shards +
   4 Cores the row wears `overcap` (*don't press*) beside a red-full Core bar (*press, Cores are
   wasting*). No `diabolist` rung reads Core as a count. Either drop `"full": true` or declare the
   authored-past-the-APL claim the way cue I's is declared.
6. **Nits.** No state cites `diabolist 7` (non-Reign builds); `db_core_up`'s condition prose is
   stricter than its marker; `backlog.md:206` says "fourteen scenarios" (15 since DEM-15) and
   `:210` calls V18 "Demonbolt's Core radial" (retired 2026-08-24); `catalog.md:375, 386` spell a
   `<` term the engine cannot author (it implements `<=` / `>=` only).
   ⚠ **FIXED 2026-08-27 — option (a), the partition.** `implosion_imps_short` became two
   mutually-exclusive `when`-gated markers, `implosion_imps_aoe` (`aoe`) and `implosion_imps_thab`
   (`!aoe ∧ talent(to_hell_and_back)`), each carrying the full band table, plus five `excludes`.
   In single target without To Hell and Back **neither draws**, so the row wears `aoe_only` alone.
   The Havoc precedent was weighed and REJECTED as the mirror image, not the analogue: there the
   POSITIVE cue was the correct answer and the negative was noise, so pass 1 landed the reader on
   the right button. Here the negative badge is correct and the gold numeral is the lie — in
   `tokens.count.rgb`, byte-identical to the `priority` and `capped` cue hues (V5.1). Accepted cost,
   stated so it is not re-litigated: `cornerBase` 1 → 2 with one stack step permanently blank, and
   the imp count is silent in ST-no-THAB and on a refused `talent` read. **Silence over a false
   promotion.**
   ⚠ **RESOLVED 2026-08-27, and the finding as written was WRONG TWICE.** (a) A `diabolist` rung
   DOES read Demonic Core as a count — `simc-apl.md:51`, `power_siphon,if=buff.demonic_core.stack<=1`.
   The true, narrower claim is that no rung reads it at a HIGH threshold or says four Cores is bad.
   (b) **`"full": true` was INERT** — `Channel.BarPlan` copied it to `plan.full` and *nothing in the
   addon ever read `plan.full`*; `Channel.Arm` adds the flip on `plan.kind` alone. So "drop
   `full`" was never a behaviour change. The key is deleted from the catalog, `Catalog.Check` and
   `BarPlan`; the flip still draws and the shelf owns it, unconditionally. No reading defect
   remained: both marks are negative, both true, neither touches pass 1. The real defect was a
   catalog key that read as a switch, controlled nothing, and had been cited in prose as if it fired
   the flip. Two garbled `catalog.md` sentences rewritten with it.

**Clean negatives worth keeping:** every `condition` checked against markers and bands — no
inversion. No §3.6 violation. Of 16 `diabolist` rungs only two are undrawn and **both reasons still
hold** (rung 2 blocked on one client measurement; rung 13's `target_if` dead on the product).
**No rung is left whose sealed condition V16–V20 could newly express.** One primitive to
deliberately NOT adopt: V19's `outside_s` would badge a press rung 14 makes unconditionally.

### Havoc

1. **`[reported]` Metamorphosis's three holds are missing `talent(chaotic_transformation)`.**
   The catalog's own docs say the gate exists (`catalog.md:146-147`, `scenarios.md:671`); the
   markers don't carry it and the talent isn't in the `talents` array (`catalog.json:60-79`,
   `:198-232`). The Hunt's identical structure IS gated, one entry down, with the same sentence as
   justification. Effect: on a build without it, rung 3 is unconditional and the leftmost GCD row
   wears a permanent red badge. Fix: add the talent (node 91024 / entry 112947 / spell 388112,
   Tier 1) + one `when` term ×3.
2. **`[reported]` Rung 2 fell through every net.** `immolation_aura,if=talent.violent_transformation
   &talent.a_fire_inside&cooldown.metamorphosis.remains<gcd.max*3` — the **highest** rung in the
   list, a Fel-Scarred rung, and `violent_transformation` appears nowhere in `specs/havoc/`: no
   state, no `exception`, no open fact, not in `rotation.md`. Fully expressible today (two readable
   `talent` terms + `sealed-cooldown-range within: 5` on `metamorphosis`) — but it is a
   **promotion**, so it would be cap's first *sealed-driven* positive cue. That is a real design
   decision. **At minimum, write down why it is or isn't authored.**
3. **`[speculative]` Retire cue D, or rewrite why it is parked.** Its APL content is one rung
   (23 → 21, over rung 22's conditional Felblade) which the anchored row order already delivers;
   the *large* promotion is rung 12's Essence-Break/Demonsurge window, correctly filed as Open
   fact 1. And the parking reason — *"the single positive cue is spent"* — is dead: there is no
   positive-cue budget (`backlog.md:450-476`).
4. **`[speculative]` V20 for Demonsurge (Metamorphosis row) and Inertia (Felblade row).** Both are
   `cdm-only:CooldownSetSpell` buff rows in the 12.1 inventory, so the ids are near-Tier-1. Does
   NOT promote either row — that still needs the readability measurement — but puts the window's
   clock on the row. ⚠ `buff.inertia_trigger` may be a distinct id from Inertia 427640; needs
   `@verify-ingame`.
5. **Nits.** `fb_overcap`'s condition says "at or above 100" where rung 22 presses AT 100 (hold is
   `> 100`); `ia_st_no_talents`'s condition asserts a `capped` term that reads UNKNOWN in that very
   state; `fact-classification.md:21-23` still defines readable in terms of the role tiers removed
   2026-08-25, and `:66` omits `blade_dance_starved`.

**Clean negatives worth keeping:** all twelve `apl` citations resolve to the right rung. The three
*"absent from 12.1"* exceptions (Demon's Bite, Fel Rush, Throw Glaive) are true — zero occurrences.
The Vengeful Retreat bands look inverted and are **not**. AR-only rungs (9, 11) correctly get
nothing. No §3.6 violation, no inverted condition.

⚠ **A clean NEGATIVE answer to the brief's own premise:** **V16/V17/V18 cannot state Fury.** All
three ride the aura *application count* (`SetApplicationCount` / `SetApplicationBar`); Fury is
`UnitPower`, and the only sealed-power sink is `sealed-power-percent`'s colour curve. Havoc using
none of V16–V20 is not an oversight — it has no stacking aura and no DoT of its own. **The gap is
a missing SINK and is currently recorded nowhere.** If a Fury bar is wanted, that is a lab
question for `backlog.md` → Ideas, not a catalog edit.

### Protection

1. **`[reported]` `as_guidance_capped` missing `ready(consecration)`.** Pattern A. `catalog.json:445-465`;
   outranking rung is `default 15`. Sibling `cons_awaits_hammer` (`:591-597`) does it right.
   PROT-6 pins "Consecration off cooldown" into its state string — exactly the branch that hides it.
2. **`[reported]` `judgment_awaits_assurance` missing `ready(crusader_strike)`.** Pattern A.
   `catalog.json:682-711`. PROT-11 *states* "both charges down" and only escapes because Judgment
   is swiped there too.
3. **`[reported]` Defeat 3 is stale — author the Sacred Weapon hold with V19.** Pattern B. Marker
   on `holy_armaments` gated to the Sacred Weapon life, `display: {kind: "sealed-pandemic",
   ability: "sacred_weapon", outside_s: 6}`. ⚠ The second half of the defeat also fails: sealed
   sinks need **no** Category-2 CDM row — `Channel.WindowPlan`/`ProcBarPlan` bind `ability.spell`
   and nothing else, and Demonology's shipped `ib_art_clock` is a V20 on an aura with no row. The
   census read blocks the *readable* latch only. **Still genuinely open:** the buff's spell id.
4. **`[reported]` Defeats 4 + 5 rest on a false premise.** ⚠ **PARTLY WRONG — measured
   2026-08-26. The PREMISE is confirmed; the prescribed FIX is not applied and should not be.**
   `capped` does have a subject here (`Sense.readCapped` reads the client live and self-withholds
   at one charge, consulting no `charged` declaration), so Defeats 4/5's stated reason was false
   and both are rewritten. But adding `capped(holy_armaments) negate` to `ha_banks_bulwark`
   **inverts the priority in the common case**: rung 23 sits BELOW rungs 15-22, while Holy
   Armaments is row 4 and Avenger's Shield is row 5 — so releasing the hold at two charges makes
   Holy Armaments leftmost-and-clean whenever Avenger's Shield is ready, and cap names the wrong
   button. It trades a rare missed press for a common WRONG one. Defeat 4's real blocker is the
   grammar (no way to say *"ranked below the rows to my right"*), and enumerating the outrankers
   is unsound because rung 16's `hammer_of_wrath` has no roster row. See `specs/backlog.md` →
   Tooling. **Original text below, kept because the premise half of it is right:**
   Pattern B. Highest-value single edit:
   add `capped(holy_armaments) negate` to `ha_banks_bulwark.when` — cue D currently holds at two
   charges where rung 23 presses, which the catalog itself calls *"the worst failure direction"*.
   ⚠ Do **not** also add the `capped` badge `fact-classification.md` §5.4 anticipates without
   argument: a positive cue is judged by pass 1 and redirects the scan, and at two banked charges
   the APL's press is usually rung 18.
5. **`[speculative]` Defeats 1 and 2 do NOT close together, and both docs claim they do.**
   ⚠ **CONFIRMED and PARTLY AUTHORED 2026-08-26.** The asymmetry is real and is now a stated rule
   in `spec.md` §3.6: a sealed display may assert an aura's **presence** and never its **absence**.
   Defeat 2 is **narrowed, not closed** — the presence band ships on a *Blessed Assurance* build
   only, because rung 15 presses Consecration on a capped Divine Guidance count **with the field
   still up**, so an ungated band would eliminate the correct button there. Defeat 1 stands whole.
   Original text below:
   (`catalog.md:735`, `scenarios.md`, `fact-classification.md` §5.2.) A sealed container slot is
   visible *while the aura exists* — so a sealed display can say "this aura is up" and can never
   say "this aura is absent". Defeat 2 (`!consecration.up`) needs **presence** and may be routable
   via a single `{draw: mark, hatch: true, polarity: negative, threshold: 0}` band — no alert edge,
   no `aura()` latch. Defeat 1 (`buff.avenging_wrath.up`) needs **absence** and stands. If the sink
   works this is the highest-value gap in the catalog: Consecration is the most-pressed button in
   the rotation.
   ⚠ **Corrected 2026-08-26 — this item used to make finding #3's mistake in reverse**, asking
   whether `SetApplicationCount` works *on a TrackedBar row*. That question does not arise. **#3 is
   the correct account: a sealed container is cap's OWN frame, not a CDM row.**
   `Channel.lua:768` derives the aura filter from `plan.unit`, `:849` calls
   `container:SetUnit(plan.unit)`, and the candidate set is bound by `includeSpellIDs` — the code
   path never touches a Cooldown-Manager row at all, and Demonology's shipped `ib_art_clock` is a
   V20 on an aura with no row. The CDM census gates the **readable** latch and nothing else.
   So what this needs is one thing, not two: **the Consecration player-buff spell id**
   (⚠ `backlog.md:238-243` records the Destruction bug where a missing `family` silently gave a
   sealed display no subject).
6. **`[verified]` `backlog.md` → `## Status` has no Protection entry.** One hit in the whole file
   (the migration list). Every other authored spec has a bullet. So Protection's three honesty
   banners live only in `capart.py`'s `SPECS_BUILT` and on the preview page, not where the project
   says status lives.
7. **Nits.** `dt_awaits_wrath`'s "correct across the entire 120s cooldown" is overbroad at
   `remains = 0` (a band reads nothing on a ready dependency); `catalog.md:690-693` lists
   `Catalog.DISPLAYS` without `sealed-proc-bar`, which dates the whole Defeats analysis to before
   V19's `outside_s` and V20 existed.

**Clean negatives worth keeping:** both Divine Guidance sealed-count tables — the hardest thing in
the file — check out in bands, thresholds, gates, verdicts, prose and rung derivation, **including
the 2026-08-25 inversion fix**. V16 vs V17 directions are both right. All 29 rungs mapped; the
Templar exclusions (8, 11, 12) are correct because this catalog is Lightsmith. ⚠ Note the upstream
list is a **mixed** list carrying both hero trees' terms, so filtering it is a judgement, not a
transcription. No §3.6 violation. Nothing drawn with a primitive a better one supersedes.

### Retribution

1. **`[reported]` `boj_opener` missing the resource guard.** Pattern A, and the most expensive
   instance because it is the catalog's only pass-1 promotion. `catalog.json:1219`; rung is
   `APL:56`, below `APL:55`. Siblings `tv_awaits_blade` (`:868`) and `ds_awaits_blade` (`:1140`)
   both carry `resource <= 4`, and `catalog.md:381` states the reason. Fix: the APL condition is
   *"HP ≤ 4 **or** WoA ready"* and `when` is AND-only, so split into `boj_opener` + `boj_opener_woa`,
   both `cue: "priority"` — one badge, union IS the OR. Cheap version: the `resource <= 4` term
   alone removes the wrong press and costs one narrow case.
2. **`[reported]` `es_awaits_expurgation` does not exist.** `APL:49` carries
   `(!talent.holy_flames|dot.expurgation.ticking)`; `catalog.md:257` quotes the line in full and
   `catalog.md:280-282` authors the identical clause for Avenging Wrath one entry down. Every
   predicate is already declared and bound. Exposure: on a Radiant Glory build cue F withholds both
   Wrath holds, so Execution Sentence draws **clear at row 1, leftmost**, for a press the APL forbids.
3. **`[speculative]` V20 proc bar for Expurgation — the highest-value addition available.** Host it
   on the **Avenging Wrath** row, not Blade of Justice, so the fact sits under the badge that
   depends on it. Rationale: `catalog.md:626-633` records the catalog's own worst failure mode —
   row unbound ⇒ no edge ever arrives ⇒ the seed stays "absent" ⇒ cap holds Wings **for the whole
   fight while looking confident**. A sealed display doesn't fix the branch but makes a stale latch
   *visible*. ⚠ **V19 is wrong here** — its badge wears the full positive treatment ("press now")
   and nothing in the priority refreshes Expurgation. ⚠ `render-shelf.md`'s V20 text says
   "HELPFUL, unit player" where `Channel.lua:768` derives both from `ability.unit`; the shelf prose
   is narrower than the code and should be widened before a second spec relies on it.
4. **`[speculative]` Light's Deliverance's 60-stack counter is drawable today.** `backlog.md` says
   the count *"cannot be"* logged and the player must watch a Tracked Buff row — true of the
   capture, but V16 exists to defeat exactly that. A `sealed-count-bands` on the Wake of Ashes row,
   `[{0, none}, {60, mark}]`, is silent until armed then says "a free Hammer is coming". Does NOT
   resolve the defeat (the four clip conditions still need the aura-duration form). Needs
   measuring: that `425518` is the stacking aura, and that it resets rather than banks past 60.
5. **`[reported]` Combined states use a different citation convention from single-marker states.**
   `dt_overcap` cites `generators 1` (correct) but `dt_overcap_and_wrath` cites `generators 4`;
   same shape on the `tv_*` and `ds_*` pairs. Both conventions defensible; running two in one file
   is not. Pick one, note it in `entries_note`. **Do not gate it** — display-only by design.
6. **`[reported]` The "latch subsumes `time<5`" claim is false on a target swap.** Expurgation is a
   *target* debuff, so any swap to an un-DoTted mob re-fires the promotion mid-fight. Behaviour is
   probably right; the justification is wrong. Rewrite to say the latch **generalises** `time<5`,
   and note it depends on the unmeasured retarget behaviour (`catalog.md:637-641`).
7. **`[reported]` Templar Strike id disagreement.** `catalog.json:50-53` gives
   `crusader_strike.alt = [406646]`; `catalog.md:82` names the live override as **407480** and
   `:566` identifies 406646 as the *talent*. `alt` feeds `Catalog.findRow`, so 406646 risks binding
   the talent's own row. Which id the row reports is Open fact 2 and genuinely unmeasured — the
   proven defect is that two documents name different numbers for the same thing.
8. **Nit.** `catalog.md:461-476` still reasons in `slot 1` / `slot 2` about the fixed three-slot
   badge geometry deleted 2026-08-19. Havoc's `catalog.md:359, 452` has the same leftover. ⚠ `capart`'s
   vocabulary gate fails a *catalog* naming one, but these are in the `.md`, which is ungated.
   ⚠ **REVERSED 2026-08-27 — the band was authored, then DELETED, and this item is what recommended
   it.** Two things went wrong. **(a) The band drew a fact the priority list never consults.**
   `lights_deliverance` appears **zero times** in `simc-apl.md`; the APL reads only the RESULT,
   `buff.hammer_of_light_free.up` at `finishers` 2. Its state cited `generators 3`, which *resolves*
   — but `generators 3` is the Wake of Ashes rung and never mentions it. **(b) The mechanic this
   item and the catalog both asserted was wrong.** Consumption **IS** automatic; it is *conditional*
   on Wake of Ashes and Hammer of Light both being unavailable. The docs read the spell text's
   *"empowering yourself to **cast**"* — a claim about the CAST — as a claim about the COUNTER, and
   concluded the counter never drains on its own. It does: WoA on cooldown with HoL spent is exactly
   when 60 stacks convert, which is the *"an additional time"*. So there **is** a fill-and-empty
   cycle the band would have drawn through.
   ⚠ **And the pass's own delegation lesson INVERTS on this case.** The `@verify-ingame` an agent
   put on this threshold was **warranted**; the recorded "settled" decision that removed it was the
   unreliable one, having been closed from a source that could not settle it. Read that lesson as
   *check a settled claim as hard as a hedged one* — especially when it was settled by reading prose
   rather than by measurement. RET-14 was deleted with the band: without it, its nine rows were
   byte-identical to RET-3, which its own title had already conceded.

**Clean negatives worth keeping:** all 33 `condition` strings faithful to their markers — no
disagreement. Rung coverage complete across all four lists; `generators 7` is dead on Templar
(Walk into Light is a Herald of the Sun talent), which also makes `generators 5`'s clause vacuous,
so cue D's omission of it is **right, not sloppy**. §3.6 clean, including the shipped `Sense.lua`
implementation. `finishers 1` citations (the `ds_castable` *variable* rung) are the **right** call —
that is where the facts live; note the convention so nobody "fixes" it later.

### Devourer

1. **`[reported]` Cue C + two bank holds are parked on work already done.** Pattern B. Re-author
   against V16/V17/V18. `catalog.md:272`, `:464`; `fact-classification.md:105-106, 124`.
2. **`[reported]` Three scenarios draw a cooldown swipe that will never exist.** `scenarios.md:76-81`,
   `:95`, and B-1/B-2/B-3 write below-bank Void Metamorphosis as **`cd`** (`swipe: true, hatch: true`)
   on the premise that *"the CDM desaturates off `SPELL_UPDATE_USABLE`"*. Tier 1 contradicts it:
   `cooldownDesaturated = self.isOnActualCooldown`, **every assignment** — usability is a *tint*
   (`ITEM_NOT_USABLE_COLOR`), not desaturation. Void Metamorphosis is fragment-gated with no timer.
   Fix: adopt the V17 band and write those rows `ruled-sealed`. ⚠ **`render-shelf.md:239` carries the
   same conflation** and should be fixed with it. **Open fact 7 collapses into open fact 3.**
3. **`[reported]` *Soul Glutton* appears nowhere in the spec directory** — and it moves the bank
   threshold from **50 to 35** (`abilities.md:164`) on the build Icy Veins' 12.1 Void-Scarred lists
   actually publish (`rotation.md:213-215`). It also makes Fury drain 25 % faster, which moves cue
   B's fitted break point. Every bank number in the directory is build-wrong. Thresholds must be
   talent-selected — legal, since `talent` is a readable gate on a sealed curve.
4. **`[reported]` `catalog.md:133` claims rung 9 outranks rung 8. It does not** — `simc-apl.md:102`
   is `void_ray` (8), `:103` is `collapsing_star` (9). Only rung 5 outranks it. That sentence is the
   load-bearing justification for the entire virtual-row design; it survives on rung 5 alone.
5. **`[reported]` The gated virtual row is read pre-emptively but carries no target term**, so in
   AoE it jumps rungs 6-8 (its rung is 9, below both). Fixable rather than merely recordable: `aoe`
   is cap's own readable toggle, so the gate may be `castable ∧ !proc ∧ /cap aoe off` — and
   misordering 1's ST-only 30-vs-35 case then becomes a V16 band on the same toggle. Closes both.
6. **`[verified]` Both virtual rows draw a scan edge, and V12 says they must not.** `catalog.md:187-188`
   marks them `scan`; `render-shelf.md:722-725` says a virtual row wears V11's hatch *"and nothing
   else — no scan edge, no badge"*. `stepper.js:149` is an unconditional `if (rule.scan)`. The doc
   and the pixels disagree and only one can be right.
7. **`[reported]` Cue D under-fires.** It encodes `!eradicate ∧ !moment_of_craving` where rung 2
   negates `!eradicate` alone (`proc(reap)` is the OR of both auras). The uncovered state is the
   safe direction, so this is bookkeeping — but it is a second instance of the same expressiveness
   gap and belongs in §7.5 with the first.
8. **`[reported]` Vengeful Retreat is in the roster and in NO scenario.** `catalog.md:299-323`
   openly doubts the binding pays for itself and routes the question to `discussion.md`; the row
   appears in none of the ten walks. The one row whose existence the catalog doubts is the one the
   proof never exercises. Write one scenario that reaches it — that settles the question on
   evidence — or drop the row.
9. **`[speculative]` Eradicate carries two different ids across two documents.** `catalog.md:141`
   says `1226033` (the tracked-buff row); `fact-classification.md:62` says `1239524`. Plausibly
   genuinely distinct, but nothing says so, and cue D's correctness depends on which the `proc`
   predicate is keyed to. Needs a DB2 read.
10. **`[verified]` `backlog.md:230` says Destruction is *"the ONE spec with no `catalog.json`"*.**
    Devourer has none either. That is the file the project designates as its only status source,
    so a reader grepping "which specs are migrated" gets a wrong count. ⚠ Fixing it means
    rethinking the Destruction entry's framing — editorial, not mechanical.

**⚠ On migrating Devourer to `catalog.json` — DO NOT, YET.** ~8 entries / ~20-24 states (about half
a Havoc). The blocker is specific: **`drawn_by` rejects a `declared` primitive, and V12 is
`declared`** — so every Collapsing Star and Consume state fails by name, i.e. the gate refuses
precisely the two rows the design exists for. Migrating the six real rows and omitting the panel
would produce a `catalog.json` describing a Devourer nobody authored. **Build V12 first**; the
migration is then a day's transcription (`catalog.md:16-19` already fixes the rung convention and
every rung cite resolves). Two smaller things migration would also refuse today: cue B cites V9 and
cue C cites V8 — both `mechanism`, both rejected (cue B's primitive is **V5**, cue C's is V16/V18);
and cue C's sink name `player-aura-stacks` is not in `SEALED_DISPLAYS`.

---

## 3 · Standing notes

- **Scenario rows carry `cues` on ALL FOUR migrated specs** — corrected 2026-08-26; the original
  bullet claimed only Retribution's did, and that is simply false. Counted in
  `specs/*/scenarios.json`, the number of row entries carrying a `cues` key is **Protection 38,
  Demonology 43, Retribution 26, Havoc 15**. What survives of the finding is narrower and still
  worth saying: a scenario row names *cue keys*, not the catalog **state** it is meant to be an
  instance of, so `capart check`'s elimination gate reasons over what the page draws rather than
  over the authored state table. The `catalog_gate_scenarios` check does match each row against
  *some* declared state, so the two are not unrelated — but nothing pins a row to the one state
  its walk is arguing about. Project-wide, not a per-spec defect.
- **`condition` prose remains a second ungated source** — already in `knowledge/_meta/kb-inbox.md`
  with the one live instance that was found and fixed. Retribution's review suggests deriving the
  scan bit from `scan_when`; that is not mechanically available, because whether a state satisfies
  its `scan_when` lives only in the hand-written prose. Same gap.
- **Two doc-vs-code seams found:** `render-shelf.md`'s V20 text is narrower than `Channel.lua`
  (unit derivation), and V12's "no scan edge" is contradicted by `stepper.js`. Both are the shelf's
  call.
- **Destruction was not reviewed.** If it should be, it needs its own pass.

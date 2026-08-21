# `wowkb.sim` — local SimulationCraft harness

**Status:** Phases 1-2 built (2026-08-20). `import`, `check`, `compare` ship.
Phase 0 (slot enum) needs the user in-game; Phases 3-5 not started.

## ⚠ This is a LIVING command — read this before touching it

`wowkb.sim` is **never finished**. It is a harness for a simulator we do not
control, answering questions we have not thought of yet, against game data that
changes every patch. Every real sim session is expected to expose something the
harness cannot express or silently gets wrong.

**The rule: when a sim session produces a wrong or misleading answer, the fix is
a new GATE in this tool — not a hand-edit to a profile or an APL.**

A hand-fix repairs one answer and teaches the tool nothing; the next person hits
the identical trap. A gate converts a one-time discovery into a permanent
property of every future run. The firing gate in this document exists *only*
because Stormbound Emblem sat inert through four comparisons on 2026-08-20 and
nothing said so. That is the pattern to repeat.

Obligations on anyone using it:

1. **Append to the Field log** (bottom of this file) after any substantive sim
   session — the question asked, what the harness could not express, what went
   wrong. A session that revealed nothing is worth one line saying so.
2. **Every artifact discovered becomes a gate**, registered in the artifact
   registry with a detection rule and a regression test.
3. **Never "fix" a bad number by editing the APL.** If the upstream APL is
   genuinely wrong, that is an upstream bug report, not a local patch.
4. **Read the Field log before designing a new comparison.** It is the list of
   ways this has already fooled us.

The phases below are a starting shape, not a finished scope. Expect to add
commands that nobody has predicted here.


## Why

Simming Encomplete's Season 2 gear on 2026-08-20 produced **five wrong answers**
before it produced a right one. Every single error was in the *harness* — the
profile and APL scaffolding — and **none** were in the game data or in simc
itself. That is the entire case for this tool: the sim engine is reliable, the
hand-authored plumbing around it is not.

The failure log, because the design is derived from it line by line:

| # | What went wrong | Consequence |
|---|---|---|
| 1 | Hand-rolled a bare profile; got simc's built-in APL instead of the upstream reference | On-use trinkets never fired |
| 2 | Wrote `use_item,slot=trinketN` without `use_off_gcd=1` | −3.2% DPS baked into every forced-use run |
| 3 | Did not control APL **action order** between two on-use trinkets | Order alone swung 3.21%; confounded the whole alignment test |
| 4 | Compared numbers **across separate simc invocations** with different frames | **Recommended the wrong vault item** |
| 5 | Never checked whether an equipped on-use trinket actually fired | Reported a confident +2.16% that was pure artifact |
| 6 | Mixed the profileset table (**median**) with the baseline line (**mean**) | Phantom 2,486 DPS discrepancy chased for a while |
| 7 | Left `—` in a results table for "not simulated" | Read as "negligible"; user had to ask |
| 8 | Skipped the export's `### Weekly Reward Choices` block entirely | Missed the vault options until the user asked |

## Non-goals (deliberate)

- ⛔ **This is not a library of hand-tuned APLs.** The trinket-alignment work that
  motivated some of this was a **one-off investigation**, not reusable content.
  The APL always comes from upstream, unmodified. There is an `--apl-override`
  escape hatch for genuine experiments, and anything using it is stamped
  `UNVALIDATED HARNESS` in the output so a result from it can never be quietly
  cited later.
- ⛔ Not a Raidbots replacement. No Droptimizer over raid loot tables.
- ⛔ Not a DPS-ranking authority. It answers "which of *these* options for *this*
  character", never "what is the best trinket in the game".

## Core invariants

These are the design, not implementation details.

1. **The harness is not user-supplied.** The base is always the upstream
   reference profile for the character's class+spec
   (`profiles/MID2/MID2_<Class>_<Spec>[_<Hero>].simc`), which carries the
   maintained APL — including the trinket-priority logic that took a day to
   rediscover by hand. The tool overrides identity, talents and **all** gear
   slots on top; it never writes an `actions` line.
2. **One invocation, one comparison.** Every variant in a question runs as a
   `profileset` inside a **single** simc process against a single base. The
   baseline is emitted as an explicit profileset (`_baseline`) so it appears in
   the same median-ranked table as everything else. The tool **refuses** to
   print a delta between two different runs — that is failure #4, and it is
   structurally prevented rather than warned about.
3. **Slot hygiene.** Every one of the 17 slots is explicitly assigned or
   explicitly cleared. The reference profile ships gear — including an
   `off_hand` — and a 2H-wielding character silently inherits an off-hand
   otherwise. (Hit for real on 2026-08-20.)
4. **Effects must be observed firing.** After every run the report is parsed and
   each equipped item carrying a use/proc effect is checked. This is failure #5
   and it is the highest-value gate in the tool.
5. **Medians only, with significance.** Every delta is reported as
   `Δ% ± error` plus a verdict of `significant` / `NOISE`, computed from the
   combined per-profileset error. No bare numbers.
6. **No ambiguous blanks.** A cell is a number or the literal string
   `not simulated`.
7. **Multi-fight-style by default.** Minimum 1T/300s **and** 5T/120s, because on
   2026-08-20 they disagreed on ordering more than once. A single-style answer
   is never printed without the other alongside.

## The firing gate (invariant 4, expanded)

For each equipped item with a special effect, parse the buff/action tables:

- on-use effect, **0 uses** → **FAIL**, refuse to report DPS
- uses < 50% of `fight_length / cooldown` → **WARN** (held, gated, or contended)
- proc effect with 0 triggers → **WARN**
- item has a registered effect in simc but produced no buff *and* no action →
  **WARN: possibly unimplemented**

Rationale: Stormbound Emblem of Dazar sat inert through four separate
comparisons and nothing in simc's output said so. A silent no-op is the
characteristic failure mode of gear sims and it is invisible unless asserted on.

## Commands

```
wowkb.sim import <export.simc|->        # parse /simc paste; store verbatim under
                                        # raw/simc-exports/<char>-<date>.simc; print
                                        # equipped + bags + VAULT CHOICES (failure #8)
wowkb.sim gear <char> --slot <slot>     # local Top Gear: every bag/vault candidate for
        [--all-slots]                   # that slot, one profileset each, ranked
wowkb.sim compare <char> A=<ovr> B=...  # arbitrary named variants (tier-set questions)
wowkb.sim crests <char>                 # DPS-per-crest for every upgradeable equipped
                                        # item, respecting each item's track ceiling
wowkb.sim log <char> [--variant X]      # iterations=1 deterministic cast timeline,
                                        # always labelled SINGLE SAMPLE - NOT A DPS RESULT
wowkb.sim check <char>                  # harness validation only, no DPS
```

`--targets`, `--time`, `--iterations` override the default matrix on any command.

## Generalization across characters

- Class+spec+hero come from the export; the reference profile is looked up, not
  assumed. Nothing is warlock- or Demonology-specific.
- **4 specs have no upstream APL** (Preservation, Mistweaver, Holy Paladin,
  Restoration Shaman). Exit non-zero with that named as a known absence — same
  contract `wowkb.simc` already uses, rather than silently falling back to the
  built-in APL, which is failure #1.
- Weapon layout is read from the export: a 2H main hand forces `off_hand=`.
- Bag/vault candidates are filtered to the character's armor class and slot, so
  the same code path serves a plate tank and a cloth caster.

## Staleness

Reuses the doctrine already in `wowkb.simc`: refuse to run when the simc
checkout predates `_meta/game-version.md`'s live-patch date, and record the simc
commit SHA + date in every result header. A DPS number with no build stamp is
not citable. Note the client can be **ahead** of `game-version.md` — Encomplete's
export read `12.1.0.69382` against a recorded `12.1.0.69214` — so `import`
should surface a client-build mismatch rather than assume the KB is current.

## Output

Markdown table to stdout; `--json` for machine use. Header always carries:
character, spec, simc SHA+date, iterations, fight styles, and the **firing-gate
verdict**. Results are written under `raw/sim-results/` (gitignored) — a sim
result is evidence for an answer, not a KB claim, and must not be pasted into
`knowledge/**` as if it were sourced.

## Open questions

- `crests` should model the same-character high-watermark free-upgrade rule
  (confirmed in-game 2026-08-19), which changes cost-per-ilvl substantially.
  **The encoding is now decoded** (2026-08-20), from the SimC addon's own source
  at `Interface/AddOns/SimulationCraft/core.lua:773-785`:

  ```lua
  -- These are not normal equipment slots, they are Enum.ItemRedundancySlot
  for slot = 0, 16 do
    local characterHighWatermark, accountHighWatermark =
      C_ItemUpgrade.GetHighWatermarkForSlot(slot)
  ```

  So `slot_high_watermarks=<i>:<a>:<b>` is **`Enum.ItemRedundancySlot` : character
  watermark : ACCOUNT watermark** — not inventory slots, and not (current, max).
  Every standard `INVSLOT` mapping failed because the index is a different enum
  entirely. Corroborated by Encomplete's data: **account >= character in all 17
  rows**, which is only consistent with this reading.

  Remaining work is one **ClientLab** run to dump `Enum.ItemRedundancySlot`
  (a static client table) so index -> slot names can be recorded once per patch.
  No reverse-engineering required.
- ⚠ Note the API exposes an **account-wide** watermark, which sits in tension
  with the 2026-07-10 finding that an alt does NOT get free same-slot upgrades.
  Both can be true (the account value may feed the "...of the Mist" warband
  achievements rather than upgrade cost), but it is unverified. @verify-ingame
- Is `--apl-override` worth having at all, or does it just recreate the failure
  mode the tool exists to prevent?


## Implementation plan

Phases are ordered so that **validation lands before anything that reports DPS**.
An unvalidated number is worse than no number — it gets acted on.

### Phase 0 — unblock the enum *(prerequisite for Phase 4)* — ✅ DONE 2026-08-20
`Enum.ItemRedundancySlot` — the key to the export's `slot_high_watermarks` rows.
Resolved from `wowkb.uiapi` (Blizzard's machine-generated API documentation,
Tier 1), **not** from a ClientLab run: `uv run python -m wowkb.uiapi enum
ItemRedundancySlot`. It lives as `ITEM_REDUNDANCY_SLOT` in `sim.py`, cited to
`ItemConstants_MainlineDocumentation.lua:28`, and `import` prints the decoded
table. **Done:** all 17 rows resolve to named slots, confirmed against eight
slots whose watermark equals the ilvl worn there.
⚠ Paired rows (`Finger`, `Trinket`) remain UNSETTLED — see the Field log entry;
Phase 4 may not cost a paired slot until they are.

### Phase 1 — `import` + `check` (the foundation) — ✅ DONE 2026-08-20
- `import` parses a `/simc` export: identity, talents, all equipped slots, the
  `### Gear from Bags` block, the `### Weekly Reward Choices` block, currencies,
  catalyst charges, watermarks. Stores the paste **verbatim** under
  `raw/simc-exports/<char>-<date>.simc`.
- Resolves class+spec+hero → upstream reference profile; hard-fails on the four
  specs with no upstream APL.
- Builds the base profile: reference profile + identity + talents + **all 17
  slots explicitly assigned or cleared**.
- `check` runs a short sim and reports **harness health only, no DPS**: firing
  gate, slot leakage, client-vs-`game-version.md` build mismatch, simc staleness.

**Done when:** `check` on Encomplete's 2026-08-20 export FAILS on Stormbound
Emblem firing zero times under the stock APL. That is the regression test for
this whole tool — if it ever passes silently, the gate is broken.

### Phase 2 — `compare` (the workhorse) — ✅ DONE 2026-08-20
Named variants as profilesets in **one** invocation, baseline emitted as
`_baseline`, medians only, `Δ% ± error` with `significant` / `NOISE` verdicts,
1T/300s **and** 5T/120s by default.
**Done when:** the tier-set question from 2026-08-20 reproduces in a single
command, and the tool *refuses* to delta two separate runs.
Register in `CLAUDE.md`'s tool block once this lands.

### Phase 3 — `gear` (local Top Gear) — ✅ DONE 2026-08-20
Auto-enumerate every bag + vault candidate for a slot, filtered by armor class
and class usability, one profileset each, ranked. `--all-slots` sweeps.
**Done:** `--slot hands` ranks all 6 (1 worn + 2 bag + 3 vault) with Handwraps
of Blasphemous Rites first among the alternatives, annotates `4 → 3 pieces —
this delta includes losing the 4pc` on every non-tier glove, and prints the
exclusion count. The whole-character sweep completes without simc throwing
`Invalid type.`

### Phase 4 — `crests` — ✅ DONE 2026-08-20
DPS-per-crest for every upgradeable equipped item, respecting each item's track
ceiling and the same-character watermark free-upgrade rule.

**Acceptance met.** `crests encomplete --track Champion` derives the 140-Champion
allocation by computation: 140 ÷ 20 = **7 ranks** affordable (branded `Tier-3 est`),
**no S2 discount** (the four achievements the export carries are all "…of the Dawn"),
**14 of 15 slots UNRESOLVED TRACK** and costed at nothing, and the one tracked slot —
trinket2, Champion 5/6 — ranked at **+0.20% ± 0.09% (significant)** for its 6/6 rank.
So the honest answer is *1 of 7 affordable ranks is worth buying*, and the other six
are unbuyable because nothing else resolves a track. That is a computed answer, not a
failure, and it is the shape the hand-run session never produced.

⚠ Two things the phase changed from its own plan:

- **It reads outside the export.** Track and step exist nowhere in the `/simc` paste and
  provably cannot be inferred from ilvl (295 is Veteran 6/6 *or* Champion 2/6). This one
  command calls `charstate.load()`; `import` / `check` / `compare` / `gear` stay
  export-only, because comparing items as they are never needs a track.
- **The acceptance case itself needs `--accept-failing-gate`**, because the only tracked
  slot on this character is the Stormbound trinket the firing gate FAILS. That is not a
  wart: the tool refusing to price the upgrade ladder of a trinket nobody presses is the
  entire point of the gate, and the reason must be typed out.

### Phase 5 — `log` — ✅ DONE 2026-08-20
Deterministic single-iteration cast timeline around a chosen cooldown window,
always stamped `SINGLE SAMPLE — NOT A DPS RESULT`.

**Acceptance met.** `log encomplete --around summon_demonic_tyrant --all-windows` puts
the 2026-08-20 mechanism on screen instead of leaving it to be inferred: Tyrant is cast
**5 times** (4.41 / 66.09 / 127.40 / 192.68 / 258.96s) and **not one on-use trinket is
pressed inside any of the five windows.** Stormbound Emblem is never pressed anywhere in
300 seconds; Freightrunner's Flask — a 120s cooldown — is pressed **once**, at 285.10s,
i.e. 280s from the first Tyrant. That is what the aggregate `check` WARN ("1.0 of an
expected ~3.3") means, made legible.

Two runs of the same command produce byte-identical output (md5 verified); `--seed 7`
produces a different one. Three structural facts, all deliberate and all tested:

1. **One iteration, and there is no `--iterations` flag.** A single sample cannot
   support a DPS claim, a delta or a frequency, so it prints none and every timeline row
   carries the `SINGLE SAMPLE — NOT A DPS RESULT` brand — the same
   brand-every-row rule the DPS tables use, for the same reason.
2. **It cannot use profilesets.** simc disables logging outright when profilesets are
   enabled (`sim.cpp:4361`), so `--variant` is a separate invocation. Safe here for
   exactly the reason it is forbidden everywhere else in this tool: nothing can be
   deltaed across the two runs because no number is reported at all.
3. **It reads the TEXT log, not the JSON.** The JSON is used only for the leak gate,
   which is structural and iteration-independent.

## Artifact registry

Each entry: detection rule + regression test. Seeded from 2026-08-20.

| Artifact | Detection |
|---|---|
| Effect never fires | on-use effect with 0 uses → FAIL |
| Effect under-fires | uses < 50% of `fight_length / cooldown` → WARN |
| Effect unimplemented | registered in simc but no buff and no action → WARN |
| Reference-profile gear leak | any slot not explicitly set by the builder → FAIL |
| Cross-run comparison | delta requested between two run IDs → refuse |
| Mean/median mixing | baseline read from the `DPS=` line rather than `_baseline` → refuse |
| Stale engine | simc commit older than live patch date → FAIL |
| Client/KB build drift | export build ≠ `game-version.md` build → WARN |
| Single-fight-style answer | only one target count run without `--force` → WARN |
| Effect unpressed vs unmodelled | on-use with 0 uses → FORCE the slot on cooldown in a throwaway probe run; forced>0 → FAIL (the APL never presses it), forced=0 → WARN (simc does not model it). Nothing else separates these, and they need opposite verdicts |
| Unfiltered bag candidates | the export's bag block is filtered ONLY by "has an equippable inventory type" — `gear` must apply armor class + class usability itself |
| Variant effect never fires | a profileset reports summary metrics only, so a swapped-in on-use trinket is as invisible inside one as Stormbound was inside a bare run. Every variant that INTRODUCES an item with a registered effect gets its own short validation run, gated before any DPS prints |
| Trinket/ring index swap | the addon files every trinket under `trinket1` and every ring under `finger1`. The family is searched so a vault trinket is reachable as a `trinket2` candidate, but the move is REPORTED — `damage_trinket_priority` tie-breaks to trinket1, so the same item in the other index is a different answer |
| Ambiguous candidate name | one item name matching two different item strings (same item, two upgrade levels, both in bags) → refuse and list the ilvls, never pick |
| Blank result cell | a variant absent from a frame renders the literal `not simulated` (failure #7) |
| Unwearable candidate | `class_mask` bit (`1 << (class_id-1)`, `util::class_id`) then armor type on the 8 `util::is_match_slot` slots, mirroring `item_t::is_valid_type`'s `>=` and its COSMETIC exemption. Also a CRASH guard: `player.cpp:2011` THROWS `Invalid type.` during gear init, so an unfiltered `--all-slots` aborts mid-sweep rather than merely misleading |
| Silent filter | every exclusion is printed with its reason, and the count line prints even at ZERO — a filter that excludes everything looks exactly like one that excludes nothing until you read the count. The indices into `item_data.inc` were miscounted once (dropping `type_flags`) and reported every bag row unwearable; they are now asserted against three known rows in `check_sim.py` |
| Unfilterable weapon | simc carries NO weapon usability data (`is_match_slot` excludes weapon slots, `class_mask` is never read for equip validation, `translate_weapon_subclass` is damage/speed math only), so weapon candidates are ranked under a `NOT-USABILITY-CHECKED` brand rather than filtered by a hand-authored table that would rot silently |
| Tier-set confound | a swap that changes a set-piece count is annotated `<set>: 4 → 3 pieces — this delta includes losing the 4pc`, off `item_set_bonus.inc`. simc models the loss correctly; the ROW reads as "this glove is bad" when it means "this glove costs you the 4pc" |
| Duplicate family item | a trinket/ring worn in the OTHER index of its family is not offered as a swap into this one — that would sim two copies of an item the character owns one of |
| Paired-slot watermark misread | `Enum.ItemRedundancySlot` gives ONE `Finger` and ONE `Trinket` row for two worn items. That row is NOT "highest ilvl ever worn here" — Encomplete's reads 295 with a 305 ring equipped. The ADOPTED rule (user, 2026-08-20) is that the row marks the SECOND-highest — the level at which you actually hold redundancy — so moving one 305 ring between finger1 and finger2 cannot raise both marks. `crests` costs paired slots under that rule and LABELS every row it changes `paired-slot rule (UNVERIFIED)`; `check_sim.py` keeps the 295-vs-305 pair as a live regression subject |
| Inferred upgrade track | a slot's track/step comes ONLY from the `/ps` dump (or the API fallback). It is NEVER inferred from the ilvl band, which is provably ambiguous: 292/295 is Veteran or Champion, 305 is Champion or Hero, 318 is Hero or Myth. A slot neither source resolves prints `UNRESOLVED TRACK` and is costed at nothing |
| Baseline ilvl drift | simc's resolved `gear.<slot>.ilevel` must equal the export's stated ilvl for every slot → FAIL. Every rank is "this item, +N ilvl", so a baseline that is not the worn item measures a different ladder. Passes on all 15 of Encomplete's slots today, so it was proved to fire against a deliberately doctored export |
| Interpolated track step | only 1/6 and 6/6 are Tier-1 (`dawncrests.md:53-64`); the four intermediates are interpolated and branded `~interp`. The error bar is known: Season 1's recorded Champion ladder (246/250/253/256/259/263) beats linear interpolation by ±1 at two steps |
| Track-model disagreement | a tracked item whose worn ilvl ≠ the ilvl the track table puts its CURRENT step at → WARN. Champion 5/6 interpolates to 305 and Encomplete's trinket2 is worn at 305, which is what corroborates the model; a disagreement means the interpolation is wrong for that step and every target derived from it is suspect |
| Crest-cost provenance | every crest-denominated number is branded `Tier-3 est` (`dawncrests.md:84-89`, open TODO at `:301`). The rank ORDER is deliberately NOT branded: because cost is UNIFORM per rank, the constant moves the affordable COUNT and nothing else — asserted in `check_sim.py` by re-running the allocator at 20 and at 10 and requiring the same order |
| Assumed discount | the 50% warband discount is derived from `upgrade_achievements` against the five "…of the Mist" ids, never assumed either way. S1 "…of the Dawn" ids grant NOTHING in S2 and are reported as inert. Two things the export cannot say are stated rather than guessed: the EARNER still pays full price, and the achievement list is account-wide, so cost is quoted at full with the discounted figure beside it |
| Season drift in currencies | an S1 Dawncrest id (3341/3343/3345/3347/3383) in an export → WARN. This is the exact silent failure that left `goalboard.py` reading every S2 crest balance as zero |
| Non-stacking rank allocation | ranks stack within a slot — 6/6 cannot be bought without 5/6 — so the allocator is greedy on MARGINAL Δ (Δ(k) − Δ(k−1)), not on the raw Δ a frame reports. Sorting on the raw Δ buys the top of a ladder while pretending the rungs below were free |
| Upgrade-vs-replace seam | `crests` costs the WORN item's ladder and `gear` ranks replacements; neither knows about the other. A slot with a bag/vault candidate within 6 ilvl of what is worn prints a pointer to run `gear --slot <slot>` first, rather than the seam being papered over |
| Single sample read as a rate | a timeline is ONE iteration. It reports no DPS, no delta and no frequency, has no `--iterations` flag to become a statistical run by accident, and brands EVERY row `SINGLE SAMPLE — NOT A DPS RESULT`. The "how often" question is redirected in the output to `check`/`compare`, which are aggregate and gated |
| Irreproducible timeline | `deterministic=1` plus an explicit `--seed`, so the same command reproduces the same timeline byte-for-byte. Without it "reproduce the Tyrant window" is not an instruction anyone can follow. Verified by md5 across two runs |
| Anchor absent from the sample | `--around <action>` that never fired prints the actions that DID, and says plainly that one iteration cannot tell "never casts it" from "did not cast it this time" — the first question goes to `check`, the second to a different `--seed`. It never prints an empty window |
| Hardcoded window length | the window's `+after` comes from the anchor's OWN summon duration in the log (`summons demonic_tyrant for 20.272s`), not a constant. A 20s Tyrant default would be a Demonology special case in a tool that has none, and the output names which source it used |
| Log verb drift | `parse_log` keeps only the verbs a reader can act on and drops `schedules execute` / `schedules travel` / `refreshes` / `decrements` / per-hit damage — ~60% of a log, none of it about ORDER. The kept/dropped split is asserted against a log fragment in `check_sim.py`, so a simc format change fails there rather than silently emptying a timeline |
| Effect identity drift | `effect_subjects()` is the ONE definition of "what an item's effect is" and its keys/ids are shared by the firing gate (aggregate counts) and `log` (timeline placement), so the two cannot disagree about whether a trinket fired |
| Pooled crest budget | crest budgets are PER TRACK and are never summed. Each tier upgrades its own track only (dawncrests.md:47). Found by a real character on 2026-08-20: 186 Adventurer + 139 Veteran + 20 Myth + **0 Champion** was pooled into "16 ranks affordable" and then spent entirely on Champion and Hero ranks. Every row was individually true and the plan was unbuyable. A track with ranks but no crests is now named outright |
| Character variable override | `wowkb/data/sim_overrides.json` → `variables`. The DECLARED exception: re-points a variable the upstream reference APL **already declares**. The tool builds the `variable,name=X,value=N` line itself (nothing in the JSON is ever pasted), an undeclared variable is rejected loudly, `why`+`measured` are mandatory, every row is branded, and the firing gate still judges |
| Appended `use_item` rung | `sim_overrides.json` → `apl_append`. The SECOND exception, and the narrower one: **only** `use_item` lines (never a damage action — failure #3 showed ordering alone swings 3.21%), `use_off_gcd=1` **mandatory** (failure #2 was this exact line without it, −3.2%), and `actions+=/` appends so upstream's list survives intact underneath. Branded `⛔ APL-APPEND` |
| Dead APL condition | a condition that can never evaluate true reads as load-bearing and gets tuned around. Caught 2026-08-21: `cooldown.summon_demonic_tyrant.remains>trinket.N.cooldown.duration` is impossible because Tyrant's cooldown (~62s) is SHORTER than either trinket's (90s/120s). Detection: the arm with and without the clause produced byte-identical output. Two arms that agree exactly are a claim about the code, not about the game |
| Silently ignored APL line | simc accepts a bare `use_item,...` line as an unknown option and ignores it — only `actions+=/use_item,...` reaches the priority list. Six analysis arms returned identical numbers before this was spotted. Any multi-arm script asserts that the arm meant to CHANGE something actually did, and aborts if not |
| Fix disables its own test | a regression that asserts upstream's broken behaviour must pin `use_overrides=False`. The Phase 1 headline test (Stormbound inert) went green the moment the override fixed it — the right reason in the wrong place, and it would have stopped testing the firing gate at all |
| Branded table copied out | a caveat printed ABOVE a table does not survive someone copying one row, so `UNVALIDATED HARNESS` / `GATE FAILED` prefixes EVERY line of it |

## Field log

Append after every substantive sim session. Newest last.

### 2026-08-20 — Encomplete Season 2 gearing (the session that motivated this)
Questions: when to drop the S1 4pc; how to spend 140 Champion / 28 Hero crests;
which vault reward to take; on-use vs passive trinkets.

Produced **five wrong answers** before a right one. All eight failures in the
table above date from this session. Specifically worth remembering:

- **A wrong recommendation actually shipped** (take Mindpiercer's Sigil) purely
  because two numbers came from different simc invocations with different
  frames. This is why Phase 2 refuses cross-run deltas.
- **APL action ORDER swung 3.21%** with identical gear and identical use counts —
  larger than every gear decision in the session. Nothing in simc's output hints
  at this.
- The user caught three errors I did not: that forcing on-cooldown misrepresented
  their play; that one GCD per 90s could not plausibly cost 3.2%; and that a
  results table mixed measured cells with unmeasured ones.
- **The correct trinket conclusion inverted twice** depending on harness quality.
  Every apparent advantage of passive trinkets was an artifact of mispressing the
  on-use one.
- Time sunk decoding `slot_high_watermarks` by hand when the answer was a comment
  in `Interface/AddOns/SimulationCraft/core.lua`. **Read the addon source first.**

### 2026-08-20 — Phase 1 built (`import` + `check`)
Not a sim session; an implementation pass. Two things it turned up that the design
did not know:

- **"Registered but produced nothing" is two different findings.** Stormbound Emblem of
  Dazar reads identically whether simc fails to model the effect or the APL simply never
  presses it — and the verdicts are opposite (an upstream absence vs. every number in
  the session being wrong). The gate now settles it by **forcing the slot on cooldown in
  a throwaway probe run**: the probe fired it 3.0 times, so the zero in the real run is a
  FAIL. Measured cause: both trinkets sit at ilvl 305, so upstream's
  `damage_trinket_priority` tie-breaks to trinket1, whose cooldown never moves (it is a
  different effect shape) — and the trinket2 rung waits on `trinket.1.cooldown.remains`
  forever. Nothing in simc's output hints at any of this.
- **The `/simc` bag block is NOT pre-filtered to what the character can wear.** The
  design assumed it was. `SimulationCraft/core.lua:GetBagItemStrings` filters only on
  "has an equippable inventory type", which is why Encomplete's 68 bag rows include mail
  and plate and a one-handed sword. Phase 3 must filter; `import` says so in its output.
- The `use_off_gcd` check is a **NOTE, not a warning**. Upstream deliberately keeps
  on-GCD `use_item` rungs as the fallback below its off-GCD ones, so a gate there fires
  on every character forever and teaches nothing. Failure #2 was a *hand-written*
  `use_item` missing the flag, so it becomes a warning only under `--apl-override`.

### 2026-08-20 — Phase 2 built (`compare`)
Not a sim session; an implementation pass. What it turned up:

- **`profileset_output_data` emits uninitialized memory in json2.** Asking for `gear`
  produced a `stats` block full of denormals (`6.45e-310`, `1.29e+277`). The cause is in
  `engine/report/json/report_json.cpp:1041,1086`: the block is gated on
  `!sim.profileset_output_data.empty()` and then written unconditionally, whether or not
  `stats` was the option requested. **Do not use the option.** Nothing here does.
- **A profileset cannot be firing-gated from inside its own run.**
  `save_output_data` (`engine/sim/profileset.cpp:1043`) handles exactly four options —
  race, gear, stats, talents — so a profileset carries no buff, proc or action counts.
  Only the BASE actor gets a full report. So each variant that introduces an item with a
  registered effect gets its own short validation run, which reports no DPS and is never
  deltaed against anything. Immediately worth it: swapping Mindpiercer's Sigil into
  trinket2 shows **+4.52% ± 0.26%, "significant"** while its own effect produces no buff
  and no action at all. That is the exact number-shape of the recommendation that shipped
  wrong on 2026-08-20, now flagged in the same output.
- **The baseline needs a no-op option to exist as a profileset.** simc drops a profileset
  with no options, so `_baseline` re-asserts the character's own `level=`. That is what
  puts it in the median-ranked table instead of on the separate mean line that caused
  failure #6.
- **`mean_error` is simc's own 95% CI half-width** (`mean_stddev` × the confidence z;
  measured ratio 1.9599). We rank on medians, so the band is `mean_stddev` × 1.2533 —
  the asymptotic SE(median)/SE(mean) ratio for a normal sample — with baseline and
  variant errors added in quadrature. Quoting `mean_error` on a median comparison would
  be failure #6 wearing a different hat.
- **A failing firing gate blocks the numbers, and the escape hatch costs a sentence.**
  Encomplete's gate FAILS (Stormbound), so `compare` on that export refuses to print DPS
  at all. `--accept-failing-gate '<reason>'` prints the table with the reason echoed and
  every row prefixed `⚠ GATE-FAILED`, and the exit code stays 1. The 4pc question does
  survive the failure — the unpressed trinket is identical in both arms — and reproduces
  as **4pc = +2.5%** over 0pc, significant in both 1T/300s and 5T/120s. But that
  judgement is the caller's to state, not the tool's to assume.
- When the gate blocks, only the FIRST fight style is ever run. The base actor's report
  comes free with it; the second style is work nobody will be allowed to read.

### 2026-08-20 — Phase 3 built (`gear`)
An implementation pass, mostly a caller of Phase 2's machinery. What it turned up:

- **The usability filter is a crash guard, not just a correctness one.**
  `engine/player/player.cpp:2011` throws `std::invalid_argument("Invalid type.")` during
  gear init when `item_t::is_valid_type()` fails, so an unfiltered `--all-slots` would
  abort part-way through rather than print a wrong ranking. Both filters are
  transcriptions of upstream (`util::class_id`, `util::matching_armor_type`,
  `util::is_match_slot`, `is_valid_type`'s `>=` and COSMETIC exemption), not inventions.
- **The `item_data.inc` column indices are a real hazard.** Counting them by eye dropped
  `type_flags` and shifted everything, which reported EVERY bag row as unwearable —
  indistinguishable from a filter that never ran, which is why the exclusion count now
  prints even at zero. `check_sim.py` asserts the indices against three known rows
  (250043 Warlock cloth hands `class_mask 0x0100`, 245770 staff `class 2/subclass 10`,
  100013 Paladin plate `0x0002/subclass 4`, plus the `race_mask` that sits last before
  the one nested group — if that is right, every index before it is).
- **`level` in `item_data.inc` is the BASE ilvl** (250043 reads 197 for an item worn at
  276). It is parsed and never displayed; row labels keep coming from the export's own
  `# <Name> (<ilvl>)` comment, the only place the real ilvl exists.
- **Encomplete's bags are less contaminated than the plan assumed, but not clean:** 3
  unwearable armor rows across the whole export (2 mail, 1 leather — no plate), plus 8
  weapon rows including a one-handed sword. The weapons rank under the
  `NOT-USABILITY-CHECKED` brand, per the 2026-08-20 decision not to author a weapon
  table with no upstream source.
- **The per-variant gate earned itself again on the first trinket sweep.**
  `gear --slot trinket1` puts **Mindpiercer's Sigil at +2.35%, "significant"** on top of
  the table while its own gate line says the effect produced no buff and no action —
  the same shape as the recommendation that shipped wrong. A `--all-slots` sweep costs
  26 validation runs on this character, all of them in the two trinket slots.
- **Cost is stated before it is spent.** `gear` prints a run-count plan (slots ×
  candidates × frames + validation runs) before the first invocation, and
  `--gate-iterations` defaults to 150 here rather than `compare`'s 250, because a sweep
  runs many.

### 2026-08-20 — Phase 0 resolved WITHOUT the client
Phase 0 was written as a ClientLab run because `Enum.ItemRedundancySlot` is a client
enum. It did not need one, and the plan's routing was wrong in two ways worth recording:

- **The enum is in `wowkb.uiapi`.** Blizzard's machine-generated API documentation
  (`Blizzard_APIDocumentationGenerated/ItemConstants_MainlineDocumentation.lua:28`)
  carries 795 enumerations, this among them — Tier 1, build-stamped, already tooled.
  `uv run python -m wowkb.uiapi enum ItemRedundancySlot`. No game session, no lab test.
  **Check `uiapi enum` before planning a ClientLab run for any `Enum.*` value.**
- **The destination was inherited from the method, not chosen.** The plan said "drain
  into `knowledge/addon-dev/`" because that is ClientLab's output contract. Once the
  source changed, that rationale evaporated: nobody writing our addon code needs this,
  and it is an upstream constant a tool consumes — so it lives in `sim.py` beside
  `MATCHING_ARMOR_TYPE` and `CLASS_IDS`, cited to `file:line`, exactly as those are.

**Why every earlier mapping attempt failed:** it is not a permuted `INVSLOT`. It is
COARSER — one `Finger` and one `Trinket` row for two worn items each, and weapons split
by hand-count (`Twohand`, `OnehandWeapon`, `OnehandWeaponSecond`) rather than main/off.

Confirmed against Encomplete's own export without the client: eight rows equal the ilvl
actually worn in that slot (Head 295, Waist 295, Feet 285, Wrist 295, Hand 276, Cloak
292, Twohand 318, Trinket 305). A wrong mapping does not survive that fingerprint, and
`check_sim.py` asserts it.

**⚠ Open, and it blocks costing a paired slot in Phase 4.** The `Finger` row reads 295
while a **305** ring is equipped, so a paired row is provably NOT "highest ilvl ever worn
in this slot type". Working hypothesis (user, 2026-08-20, explicitly offered as
unverified): a paired slot is marked at the **second-highest** — the level at which you
actually hold redundancy, which is what the enum's name says — so moving one 305 ring
between `finger1` and `finger2` cannot raise both marks. Two data points in this one
export are consistent with it: `Finger` = 295 (the lower of a 295/305 pair), and the
one-hand weapon rows, which DO get two indices, read `OnehandWeapon` 246 vs
`OnehandWeaponSecond` 62 — the same redundancy shape made explicit. Encomplete's
trinkets are both 305 and cannot discriminate.

Not written into `knowledge/endgame/dawncrests.md`: it is one character's export and a
hypothesis, not a verified rule. If it holds it is a genuine gameplay claim about the
"…of the Dawn" discount and belongs there — verified first, then written.

### 2026-08-20 — Phase 4 built (`crests`)

**What shipped.** `crests <char> [--track X | --all-tracks] [--budget N]
[--ignore-watermark]`. Every remaining rank of every equipped, tracked item becomes one
profileset in ONE invocation, expressed as the item's own line plus `,ilevel=<target>`
— simc models no part of the upgrade system, so the target ilvl is computed here from
`dawncrests.md`'s track table. Seven new gates (registry above). 232 offline checks.

**The finding that shaped the command.** Encomplete resolves a track on **one slot of
fifteen**. The `/ps` dump reads the track off the item tooltip, and fourteen slots carry
no upgrade line the dump could see; the Blizzard API adds nothing (it drops the track on
crafted gear outright). So the honest output is fourteen `UNRESOLVED TRACK` rows and one
priced ladder. The temptation is to fill those in from the ilvl — and that is precisely
what cannot be done: **292/295 is Veteran or Champion, 305 is Champion or Hero, 318 is
Hero or Myth.** Most of this character's gear is ambiguous. Guessing would have produced
a full, confident, wrong crest plan — the exact shape of the five wrong answers this
whole tool was built against. The gate refuses instead.

**The cost side is Tier-3 and stays that way.** No crest-cost table exists anywhere in
the repo; `dawncrests.md:84-89` carries one prose sentence (flat 20 per rank) with its
own open TODO at `:301` asking whether that is even right for S2. The real source,
`C_ItemUpgrade.GetItemUpgradeItemInfo().currencyCostsToUpgrade[]`, is `MayReturnNothing`
and not headless. Rather than fake precision, the command leans on a property: **cost is
uniform per rank, so ranking by "DPS per crest" is arithmetically identical to ranking
by "DPS per rank".** The constant moves the affordable COUNT and nothing else. Every
crest number is branded `Tier-3 est`; the ORDER is not branded, and `check_sim.py`
re-runs the allocator at 20 and at 10 and requires the same order — the property is
tested, not asserted in prose.

**One corroboration worth keeping.** Champion 5/6 interpolates to 305, and Encomplete's
trinket2 is *worn* at 305 on Champion 5/6. That is one independent confirmation of an
interpolated step the KB explicitly does not confirm — so the disagreement case became a
gate (`track model`) rather than a silent use.

**Two things the acceptance case exposed.**

1. The only tracked slot is the Stormbound trinket the firing gate FAILS, so the
   acceptance run needs `--accept-failing-gate`. The tool refusing to price the upgrade
   ladder of a trinket nobody presses is the gate working, not a wart — but it does mean
   Phase 4's headline demo is a two-gate demo.
2. `relative_to(ROOT)` threw on an export passed by path from outside the repo. Fixed
   with `_rel()` across all four commands. That path is not hypothetical: a doctored
   copy of the export is how the ilvl-fidelity gate was proved to fire at all, since it
   passes on all 15 real slots.

**Byproduct.** simc's own item table carries none of the `i:` upgrade items
(268552 / 232875 / 274476 all read `None`), so their names are transcribed from
`Simulationcraft/extras.lua:395-410`. Item **268552 = Ascendant Voidcore**, which the KB
had as unidentified.

### 2026-08-20 — Phase 5 built (`log`)

**What shipped.** `log <char> [--around ACTION] [--occurrence N|--all-windows]
[--before S] [--after S] [--buffs] [--pets] [--variant …] [--seed N]`. One deterministic
iteration, a windowed cast timeline, and — the headline — an **on-use alignment
readout** per window. Six new registry rows. 262 offline checks.

**Why the alignment readout is the whole command.** The 2026-08-20 session inferred
trinket misalignment from summary counts and got it backwards twice. The mechanism is
that upstream's `trinket2` rung waits on `trinket.1.cooldown.remains`, and with both of
Encomplete's trinkets at ilvl 305 `damage_trinket_priority` tie-breaks to trinket1 —
whose cooldown therefore never moves. **Nothing simc prints in aggregate hints at
this.** The timeline shows it in one screen: five Tyrant windows, zero presses in any of
them, and the single Freightrunner press of the whole fight sitting at 285.10s.

**What the command deliberately cannot do.** It prints no DPS and has no `--iterations`
flag. A one-sample timeline that quietly became a 1000-iteration run would be showing a
timeline from an arbitrary one of them, and the brand would be a lie. `log_options()`
fixes `iterations=1 threads=1 deterministic=1` and `check_sim.py` asserts it, so the
guarantee is tested rather than documented.

**One upstream fact worth recording.** `sim.cpp:4361` — `if ( parent ||
profileset_enabled ) { debug = false; log = 0; }`. **Profilesets and logging are mutually
exclusive**, so `log --variant` is the only place in this tool that runs a second simc
invocation on purpose. That is safe precisely because no number crosses between them;
the rule this tool enforces everywhere else is about *numbers*, not about invocations.

**Refactor.** The firing gate's per-effect subject list became `effect_subjects()`, now
shared with `log`. Previously the gate held the only definition of "what an item's
effect is"; a second, drifting copy inside `log` is exactly how a timeline would come to
say a trinket fired while `check` said it did not.

### 2026-08-21 — the two-on-use trinket deadlock, and two declared exceptions

**How it started.** A fresh export (ilvl 294 → 300, the S1 4pc finally replaced) put 14 of
15 slots on a resolved track, so `crests` ran for real for the first time — and produced a
**wrong answer**. It pooled crest budgets across all five tracks into "16 ranks" and spent
them on Champion and Hero ranks for a character holding **zero** Champion crests. Fixed:
budgets are per track, a broke track is named, regression added.

**The trinket hunt, and what it cost to do properly.** Stormbound Emblem of Dazar fires
**0 times in 300s** under upstream. Four hypotheses died in order:

1. *The slot index* — swapped trinket1/trinket2; reproduces exactly. The deadlock follows
   the ITEM.
2. *`trinket_priority`* — overridden to 2; no change.
3. *`damage_trinket_priority`* — overridden to 2; no change. (Both were removed again
   rather than left in the file: my own README says an unmeasured override is a
   superstition, and two disproven ones are worse.)
4. *The ilvl tie* — bumped trinket2 to 308 so 305/305 no longer ties; no change. This one
   had been written up as the likely cause and was **wrong**.

**And the one that mattered: it is not our harness.** Running the shipped
`MID2_Warlock_Demonology.simc` completely untouched with **only the two trinket lines**
changed reproduces it exactly — Freightrunner 1.0, Stormbound 0.0. That bisect is also a
ready-made minimal repro for an upstream issue. Upstream's own default profile carries
**one** on-use trinket (Vile Vial on-use + Wavecaller's passive), so the two-on-use case —
where each rung waits on the other's cooldown — is never exercised there.

**The user was right about the history.** "We had two trinkets working before" was
accurate: failure #2's *"every forced-use run"* was a hand-written `use_item` APL, not
upstream. That is what `apl_append` now makes durable and gated instead of ad-hoc.

**Measured (stock upstream profile, common random numbers, `deterministic=1` + one seed,
so arms differ ONLY by APL — profilesets cannot carry an APL, so separate invocations are
structurally required here and CRN is the mitigation):**

| 1T/300s | flask presses | uptime | emblem presses | uptime | dps |
|---|---|---|---|---|---|
| upstream unaided | 1.00 | 5.0% | **0.00** | 0.0% | 196,348 |
| on cooldown | 3.64 | 17.9% | 2.81 | 18.1% | 200,776 (+2.27%) |
| held for Tyrant | 3.16 | 15.6% | 2.41 | 15.3% | **203,002 (+3.41%)** |

Held also wins at 5T/300s (+1.86% over on-cooldown), and at 120s it is **free** —
identical press counts either way, still +1.0–1.9%. A 10s grace clause is the worst of
both (+2.09%). So upstream leaves **>3%** on the floor for this gear.

**The uptime objection is real and still loses.** Holding costs 13% of presses (3.64 →
3.16), not the 25% the naive 90s-CD-forced-to-120s-cadence arithmetic predicts — Tyrant's
real cycle is ~62s and drifts against 90s. Tyrant multiplies pet damage, so stats placed
inside the window are worth disproportionately more; less uptime, better placed, wins.

**Two process failures worth keeping.** The first six-arm analysis returned six identical
rows because the lines were written bare (`use_item,...`) instead of `actions+=/use_item`,
which simc silently ignores — now an abort guard. And the shipped condition carried an
escape valve that is **dead code**, caught only because the arm with and without it was
byte-identical. Both are registered above.

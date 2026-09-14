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

### 2026-08-21 — Encomplete three-spec M+ compare, from the Blizzard API (no addon paste)

Ran demo/destro/affli on Encomplete's current gear from a **laptop with no `/simc` addon
dump and a stale WoW install**. Lessons, all confirmed by the session:

- **Equipped-gear sims do NOT need the addon paste.** Built the profile from the Blizzard
  **profile `/equipment` endpoint** (id + bonus_list + level.value + enchantments + sockets
  → addon-paste-format text) and fed the existing gated harness unchanged. The addon-paste
  requirement is really only for the **bag/vault/crest** subcommands (bag item LEVELS and
  track/step exist nowhere else). A converter lives at `scratchpad/mkprofile.py`. The
  built-in path everyone actually uses for this is simc's own `armory=` import; we build the
  profile ourselves so it runs through our gates + our creds.
- **`--no-overrides` is documented in CLAUDE.md but NOT wired into the CLI** (only the
  `use_overrides=` kwarg exists). To sim "upstream unaided" per spec, rename the character
  (overrides are keyed by NAME only) — `load_overrides` returns {} for an unknown name.
- **`sim_overrides.json` is spec-blind.** Encomplete's demo-tuned trinket append
  (`if=pet.demonic_tyrant.active`) applies to destro/affli too, where it's inert. **Re-check
  the firing gate per spec** — destro/affli fire both on-use trinkets under UPSTREAM unaided
  (the two-trinket deadlock is a demo-APL problem, not universal).
- **Measure, don't extrapolate.** A scale-factor weight predicted a full mastery→haste
  reforge for Affli at ~0.1%; the actual sim was **+4.2%** (haste compounds beyond its local
  derivative). Never integrate a scale factor over a large budget swing — sim the change.
- **`set_bonus=` needs the single-line `/` form in 12.0+** (`set_bonus=..._2pc=1/..._4pc=1`);
  two separate `+=set_bonus=` lines silently overwrite rather than stack. Overlaying the
  bonus EFFECT (via `set_bonus=`) answers "what's the tier worth on my current stats" without
  the 4-slot stat swap — exactly the right tool for a "magically give me the bonuses" ask.
- **`--hero <Tree>` to match the reference APL to the build's hero tree.** Confirm which tree
  a raider.io string actually encoded by grepping the sim's used abilities in json2 (base APLs
  branch on `talent.enabled`, so a mismatch usually costs ~0 — but confirm, don't assume).
- **Distinct character names** avoid clobbering built-profile files (`compare-<char>-…simc`).
- **Fixed a latent bug:** `cmd_compare` called `print_overrides(built,…)` with `built`
  undefined — crashed the print AFTER the sim whenever an override applied. Now
  `frames[0].built`. (`check` was fine; it defines `built`.)
- **Patchwerk ≠ M+.** The bare-gear ladder (demo ≫ destro ≫ affli, 5–20%) is steeper than the
  meta's day-3 A-tier cluster. Dummy sims measure throughput, not M+ (utility, big-pull AoE,
  priority damage). Always caveat + cross-check the meta; Affli is the spec a fixed-target
  dummy most understates.
- **Verify game mechanics before asserting.** Claimed "Affli loot spec → more haste/crit
  gear"; a 30-second check showed **loot spec does not touch secondaries at all**. Cheap to
  verify, expensive to state wrong.

### 2026-08-21 — "sim me on a target dummy" → `--dummy` / `--fixed-length` / `--distribution`

The ask was a **dummy** reading (no raid buffs, no consumables, just the gear) plus an idea
of run-to-run luck. The harness could express **neither**, and both failures were silent:

- **The reference profile is a raid-buffed, flasked, potioned, oiled character** — that is
  what a DPS ranking is measured under, and nothing in the output says so. Reading a
  `compare` median as "what I do on a dummy" overstates Encomplete by **32%**
  (112,997 → 85,646 at 1T/300s). Now `--dummy`.
- **`flask=` (empty) does not clear a consumable the reference profile set**, and an unset
  `potion=` makes the APL's `potion` rung pick a default rather than skip — the first probe
  looked cleared and still ran 93,894. The only token that disables one is the literal
  `disabled`. Raid buffs come from the SIM, not the profile: `optimal_raid=0` plus an
  explicit `override.bloodlust=0`.
- **New gate — `dummy_gate`.** Under `--dummy` the buff table is asserted empty of any
  potion / well-fed / flask / rune / weapon-oil / raid-buff / bloodlust application, and
  `optimal_raid` is re-read out of the sim's own options. A consumable that silently
  re-defaults is invisible in the DPS number, which is the firing gate's failure mode
  pointed the other way. It blocks the table like any other FAIL.
- **`compare` now accepts zero variants.** "What do I do right now" is a legitimate
  question and the only way to ask it was to invent a throwaway variant. The row is branded
  `this IS the baseline` and a note says the run is absolute, not a comparison.
- **`--distribution` + `--fixed-length`.** Per-pull spread comes from the base actor's
  `collected_data.dps` (profilesets carry only summary metrics). Default runs carry simc's
  **±20% fight-length variation**, which lands in the same σ and reads as luck when it is
  not: 1T σ was 2.7% varying vs **2.2%** fixed, 5T 5.0% vs **3.1%**. Quoting the varying
  number as "luck" would have overstated 5T spread by 60%.

Measured, Encomplete (Demonology, ilvl ~301, 2026-08-20 export), dummy, fixed length:
1T/300s median **86,504** (σ 2.2%, middle 80% 84.0k–89.0k) · 5T/120s median **285,502**
(σ 3.1%, middle 80% 274k–297k). Raid-buffed for contrast: 112,997 / 408,912.

Not built, and the reason the "what would a human hit" half of the question is an estimate
rather than a measurement: the harness has **no execution model**. simc plays the APL with
zero reaction time and perfect foresight; there is no knob here for latency, missed GCDs or
late Tyrant windows. If that question keeps coming up, the honest version is a
`--human` degradation frame (world_lag / reaction_time / a GCD-drop rate), not a fudge
factor applied to the median after the fact.

### 2026-08-25 — Encomplete's S2 week-2 vault pick

Question: which of seven vault options (and whether any of them beats taking the
Voidcore bonus roll instead). Result below; the harness gap it exposed matters more.

**⚠ NEW ARTIFACT — `compare` does not validate WEAPON GEOMETRY, and it fooled me for a
full round of sims.** Three of the six weapon variants I authored were **not equippable
in game**, and every one of them produced a confident, significant, plausible number:

- `off_hand=` assigned alongside a **two-handed staff** in `main_hand`. simc applied the
  off-hand's stats anyway. That read as **+1.34% ± 0.09%, "significant"** — the vault's
  292 staff "beating" the worn 318 crafted staff — when the entire gain was a 305
  off-hand's stats granted for free in a slot the character cannot fill.
- A **Wand** (`inventory_type = Ranged`, Spiritbound Focus, id 272271) placed in
  `main_hand`. simc took it, and the -7.01% it produced was read for a moment as "the
  318 staff is far ahead of a 1H+OH pair" — a conclusion drawn from a weapon combination
  that does not exist.
- The two errors partly cancelled, which is why neither looked wrong on its own.

**The tell that broke it open** was physical implausibility, not any gate: a 292 main
hand pairing 8.35% better than a 295 one. Nothing in the tool said anything. The
existing `NOT-USABILITY-CHECKED` brand is on `gear`'s weapon rows only; `compare` has no
weapon handling at all, and the brand would not have caught this anyway — each item IS
usable, it is the **combination** that is illegal.

**The export cannot answer this.** `/simc` files every weapon candidate under
`main_hand=` or `off_hand=` by inventory type, and carries no `Two-Hand` / `One-Hand`
distinction anywhere. Resolving it took the Blizzard item API
(`wowkb.blizzard item <id>` → `inventory_type`). Of Encomplete's eight `main_hand`
bag/vault rows, **three are two-handed staves, one is a wand, and only three are real
one-handers** — the block reads as eight interchangeable main hands and is nothing of
the kind.

**Gate to build (not built yet — recorded so the next session does not re-discover it):**
resolve each weapon's `inventory_type` (simc's own `item_data.inc` carries it — the same
table `gear`'s usability filter already parses, so no API call is needed at run time) and
**FAIL** any variant that assigns `off_hand` while `main_hand` is `INVTYPE_2HWEAPON`, or
that puts a non-`INVTYPE_WEAPON`/`WEAPONMAINHAND` item in `main_hand`. This belongs in
`compare` as well as `gear`, because `compare` is where hand-authored variants land.

**Second, smaller thing.** An `@<Item Name>` reference resolves to the export's row
verbatim, so it **drops the enchant** on a slot that has one. Enchant-matched controls
(`legs298_noench`, `mh_noench`) both landed inside noise here, so it cost nothing this
time — but the control is what proved that, and a variant that silently un-enchants a
slot is the same shape as every other artifact in this file. Worth either carrying the
equipped enchant forward automatically or naming it in the output.

**The answer, once the variants were legal** (1T/300s and 5T/120s, both frames, firing
gate PASS on the baseline):

| variant | 1T/300s | 5T/120s |
|---|---|---|
| Knot of Writhing Serpents (315) → trinket1 | **+1.31%** | **+0.81%** |
| Pyrewalker's Wraps (305) → wrist | +0.32% | +0.31% |
| Wind Soarer's Breeches (318) → legs | +0.14% | NOISE |
| *(baseline)* | — | — |
| Luminescent Sprout (308) + owned 292 dagger | -6.78% | -6.68% |
| Venomancer's Winged Channeler (292 staff) | -8.40% | -8.06% |

**And the winner's number is a floor, not an estimate.** Knot of Writhing Serpents'
effect (spell 1293304 — 2 RPPM haste-scaled, Nature damage **split among nearby
enemies** plus a DoT on the primary target) is registered in simc's item table and
produces **no buff and no action**: the +1.31% is its *stats alone*. The AoE half is
entirely unmodelled, which is why the 5T figure is *lower* than the 1T one — the exact
inversion of what the effect's own tooltip implies. A trinket whose proc is missing from
the sim beating two working trinkets on stats is a strong result, but it is strong in a
direction the tool cannot size.

Spirit-Rending Poison (1297145, on-use) is unmodelled too — forced-probe fired 0 — and
still lost by 3.8–6.0%, so that one is not close either way.

### 2026-08-25 (cont.) — the same session, two more artifacts, and the answer INVERTED

The user asked one question — *"did you sim the legs as-is or fully upgraded w/ crests
and enchant?"* — and it overturned the recommendation. Both causes are harness artifacts.

**⚠ ARTIFACT — `@<Item Name>` silently carries the EQUIPPED row's enchant, so an
"enchant-matched control" built that way is VACUOUS.** I wrote `legs298_noench` as a
control for the un-enchanted vault row, believing both arms were bare. They were not:
`@Wind Soarer's Breeches (298)` resolves to the **equipped** row, whose item string
already contains `enchant_id=7936`, so the control was byte-identical to the baseline
and measured `+0.06%` — which I read as "the enchant is worth nothing" when it actually
meant "this variant changed nothing at all". The vault row, having no enchant of its
own, really was bare. Enchant 7936 measures **+33 intellect** (bare-character
`spell_power` 885 → 918), and carrying it costs the legs comparison **~1.06%**:

| Wind Soarer's Breeches (318) | 1T/300s | 5T/120s |
|---|---|---|
| as I first simmed it (enchant dropped) | +0.14% | NOISE |
| with the enchant carried | **+1.20%** | **+1.20%** |

An identical-looking control that is identical *because it is the same string* reads
exactly like a control that is identical *because the variable does not matter*. The
tell is that a genuine no-op control should measure inside the noise band and this one
measured at `+0.06% ± 0.09%` — right where a true no-op sits, which is why it passed.
**Gate to build:** when a variant's resolved item string equals the baseline's for that
slot, say so — `variant X changes nothing in slot Y` — rather than ranking it. And when
an `@` reference lands in a slot whose equipped item carries an `enchant_id`/`gem_id`
the variant lacks, either carry it forward or name the difference in the output.

**⚠ GAP — `compare` cannot express `set_bonus=`.** It is not in `CANON_SLOTS`, so the
"what is the tier worth on my current stats" question — the *right* tool for a 12.1
Catalyst question, since converted pieces now inherit the source item's stats and the
bonus is therefore the ONLY thing that changes — has no route through the tool. Worked
around by stripping the profileset block off the tool's own generated frame
(`raw/sim-results/compare-encomplete-<frame>.simc`) and appending hand-written
profilesets. That reuses the gated harness and stays within one invocation per frame, so
invariant 2 holds, but it is outside the tool and nothing gated it. `set_bonus` should
be an accepted variant key.

**And set bonuses are invisible to the firing gate.** Both halves of
`midnight_season_2` (2pc spell 1296573, 4pc 1296574) are `[Passive, Hidden]` — no buff
row, no action, nothing in the JSON's `sets`/`set_bonus` keys, and simc does **not**
error on an unrecognized `set_bonus=` string. So "the option did nothing" and "the
option applied" look identical in the report: precisely the Stormbound failure mode.
Settled with a common-random-numbers triple (200 iterations, `deterministic=1`,
`threads=1`, one seed, arms differing only in the `set_bonus` line): 0pc 121,161 → 2pc
124,047 → 4pc 129,846, monotone. Those are same-seed means used **only** to prove the
option bites; the publishable medians come from the profileset frames.

**Results (medians, both frames, baseline = current gear).**

Crest runway, from `crests --all-tracks` — the fact that decided it: the **worn** legs
are **Champion 3/6, ceiling 308, and Encomplete holds ZERO Champion Mistcrests**, so
that slot is frozen at 298. The vault legs are **Myth 1/6, ceiling 334**, against 38
Myth crests in the bank.

| variant | 1T/300s | 5T/120s |
|---|---|---|
| legs 334 (Myth 6/6) + 4pc — reference, needs 4 charges | +9.94% | +11.70% |
| legs 334 + **2pc** | **+4.88%** | **+4.75%** |
| legs 334 (Myth 6/6) | +2.41% | +2.38% |
| **2pc alone, no legs** | +2.35% | +2.28% |
| Knot of Writhing Serpents 321 (Hero 6/6) | +1.79% | +1.08% |
| legs 321 (Myth 2/6 — all 38 Myth crests buy one rank) | +1.47% | +1.48% |
| Knot 315 as awarded | +1.26% | +0.75% |
| **legs 318 as awarded** | **+1.20%** | **+1.20%** |
| wrist 321 (Hero 6/6) | +0.89% | +0.88% |
| worn legs 308 (Champion 6/6) — UNREACHABLE, 0 Champion crests | +0.60% | +0.61% |
| wrist 305 as awarded | +0.35% | +0.29% |

**The recommendation flipped from the trinket to the legs**, on three things the first
pass got wrong or never priced: the enchant artifact above, the frozen-vs-open crest
track, and the fact that the legs are the only one of the seven options in a
catalyzable slot (head/shoulder/chest/hands/legs). The trinket's unmodelled proc still
cuts the other way and is the reason this is a judgement rather than a readout.

**Process note.** Nothing in the tool surfaced any of this — the user asked one question
about methodology and it inverted the answer. Both new gates above are cheap; the
enchant one in particular would have fired on the very first run.

### 2026-08-25 (cont.) — `log` judged on-use alignment against ONE window and libelled a working pair

Asked whether the two on-use trinkets alternate across Tyrant windows. `log --around
summon_demonic_tyrant` printed:

```
  summon_demonic_tyrant — cast 5 time(s) at 4.42s, 65.73s, 128.24s, 189.82s, 254.71s;
  showing occurrence 1
  ...
    ✅ trinket1  Freightrunner's Flask       pressed IN window (+2.89s)
    ✗  trinket2  Stormbound Emblem of Dazar  not in window; nearest press +63.76s away
```

That `✗` reads as a failure and is not one. The presses are 68.17s and 192.27s — **+2.44s
after Tyrant 2 and +2.45s after Tyrant 4.** Laid against all five anchors the pair is
perfect:

| Tyrant | 4.42s | 65.73s | 128.24s | 189.82s | 254.71s |
|---|---|---|---|---|---|
| Freightrunner's Flask (90s CD) | ✅ +2.89 | — | ✅ +0.00 | — | ✅ +0.00 |
| Stormbound Emblem (120s CD) | — | ✅ +2.44 | — | ✅ +2.45 | — |

Five anchors, five covered, strict alternation. The readout says the opposite because the
alignment block is computed against **the displayed occurrence only** while the press list
beside it spans the whole fight — so a trinket whose cooldown is longer than the anchor's
cycle can *never* be "in window" and always renders as `✗`. **Fix: compute alignment
against EVERY occurrence and report coverage (`2/5 anchors, alternating with trinket1`),
not membership of one.** As it stands the tool's own output argues against the override it
is there to validate.

**A second mis-read in the same block:** `4 press(es) ... at: 68.17s, 68.67s, 192.27s,
192.77s` — those 0.5s-apart pairs are not two presses of a 120s-cooldown trinket. The
buff table shows `the_kings_unyielding_wind: start= 2.0, interval=124.1, duration=20.0,
uptime=13.33%` — **two** uses, the second timestamp being the effect landing after the
use. The press counter is counting driver and application as separate presses.

**Worth recording because it was nearly a wrong conclusion:** Stormbound Emblem's action
row reads `pDPS=0 DPE=0`, which looks like a dead trinket. It is a driver for a 20s
**buff**, and the value is in the buff row, not the action row. Do not read an on-use
stat trinket's contribution off the Actions table.

**And the alternation is emergent, not designed.** Both override rungs say the same thing
— `if=pet.demonic_tyrant.active`. Nothing alternates them. It works because 90s and 120s
cooldowns interleave against a measured ~62.6s Tyrant cycle. Change either cooldown and
both could want the same window. Also note upstream unaided fires Freightrunner **1×/300s**
and Stormbound **0×**; every bit of this behaviour comes from the two declared
`apl_append` entries, which are keyed to this character by NAME and are spec-blind.

**Consequence for the vault question:** taking Knot of Writhing Serpents evicts
Freightrunner's Flask, leaving ONE on-use. The `trinket1` override rung goes inert and
`sim_overrides.json` needs re-checking for this character before the next comparison.

### 2026-08-27 — Void-Reaper's Libram: which trinket does it replace, and the firing gate's first FALSE NEGATIVE

Question: Encomplete looted a **Hero-track (305) Void-Reaper's Libram** (id 251785); sim it
at Hero 2/6 and 6/6 and say which equipped trinket it replaces. Six variants in one frame
each (1T/300s, 5T/120s), 10,023 iterations: the libram at 305 / 308 / 321 in `trinket1`
(evicting Freightrunner's Flask) and in `trinket2` (evicting Stormbound Emblem of Dazar).

**The find, before the numbers: the item was not in the export at all.** The 08-25 `/simc`
paste carries a *different* copy — bonus `12834/41`, **295** — and nothing else. The 305 one
was located in **Syndicator's** `Characters > Encomplete-Kil'jaeden > bags` (line 13171,
bonus `12841/6652`). Syndicator stores **no item level**, so the ilvl was recovered by
calibrating the **bonus ID** against the export itself, which prints both: `12841` = 305 on
four separate items in that file, `12834` = 295 on six. That is a usable workaround for
"is X in my bags" between pastes, and it is *only* a workaround — it cannot price anything,
and the sim still had to run off a two-day-old baseline.

**⚠ NEW ARTIFACT — the firing gate WARNed on a proc that was firing perfectly.** All six
variants printed:

```
⚠ WARN  trinket1  Void-Reaper's Libram
        → spell 1253113, equip/proc — registered in simc's item table but produced
          no buff and no action — possibly unimplemented
        observed 0.0; expected not computable
```

It is implemented — `unique_gear_midnight.cpp:2825 voidreapers_libram`, registered at 5552 —
and it fired ~7.4 times per 300s in **every** gate run. The gate missed it because it looks
for a buff or action **named after the item**, and this effect registers its children under
their own spell names: action `sacred_text` (1266394), child `text_ignite` (1266407), buff
`sacred_duty` (1266403). Nothing in the item's own name appears anywhere in the output.

This is the **inverse** of the failure the gate was built for. Stormbound Emblem sat inert and
nothing said so; here the gate said "possibly unimplemented" about a working trinket, which is
the shape that gets a real upgrade thrown away. It also nearly cost this answer: the previous
session's Knot of Writhing Serpents entry established "gate is quiet ⇒ stats-only ⇒ the number
is a floor", and applying that rule here would have branded a fully-modelled result as a floor
and inflated it.

**Gate to build:** resolve the driver spell's own **triggered spell ids** (simc's
`item_effect.inc` → driver → `sc_spell_data` effect rows already carry them; the DBC comment
block above each implementation lists them literally) and look for actions/buffs under *those*
names, not the item's. Failing that, at minimum widen the WARN text: "no action or buff
matching this item's name — the effect may register under its spell's name; check the JSON
before treating this as unmodelled." The one-line check that settled it here was grepping the
gate JSON's `stats`/`buffs` for the spell names in the implementation's comment header.

**Results** (medians, `_baseline` = gear as of the 08-25 export, both `apl_append` rungs live):

| variant | what it evicts | 1T/300s | 5T/120s |
|---|---|---|---|
| libram 321 (Hero 6/6) → trinket1 | Freightrunner's Flask | **+1.85%** | **+1.25%** |
| libram 308 (Hero 2/6) → trinket1 | Freightrunner's Flask | **+1.03%** | **+0.41%** |
| libram 305 (as looted) → trinket1 | Freightrunner's Flask | +0.73% | +0.22% |
| *(baseline — both on-use trinkets)* | — | — | — |
| libram 321 → trinket2 | Stormbound Emblem | -0.03% NOISE | -1.80% |
| libram 308 → trinket2 | Stormbound Emblem | -0.92% | -2.56% |
| libram 305 → trinket2 | Stormbound Emblem | -1.09% | -2.68% |

Unambiguous and monotone in both frames: **it replaces Freightrunner's Flask; dropping
Stormbound Emblem loses at every ilvl.** The surviving on-use fires in both arms (Stormbound
2.88×/300s, 18.3% uptime in the `t1` arm; Freightrunner 3.10× / 15.3% in the `t2` arm), so
neither `apl_append` rung went inert and the split is not an artifact of a dead override —
which was the specific thing the 08-25 entry warned the next session to check.

**Proc size, for the record.** `sacred_text`'s `compound_amount` (which *includes* its
`text_ignite` child — 265,272 + 235,942) is ~1,670 dps of a 123,080 total at ilvl 321,
i.e. **~1.36% of DPS is the proc**, ~1.06% at 305. The rest of each delta is stats minus the
evicted on-use. The 5T column being *lower* than 1T is correct here and not the Knot's
unmodelled-AoE inversion: Sacred Text is single-target by construction.

**Two things this run did not price**, both stated in the answer rather than guessed:
the baseline is two days old (the 08-25 vault pick may since be worn), and the Hero 2/6
target of **308** is `~interp` ±1 on the same interpolation `crests` brands.

### 2026-09-06 — "can I drop the Stormbound Emblem?" — the track lookup answered it before the sim did

Question: sim Encomplete's trinkets to see whether **Stormbound Emblem of Dazar** can be
swapped out, assuming the Hero-track trinkets go to **6/6 (321)**. The stated reason was
ergonomic: the Emblem's **2-second channel** is awkward to fit into the rotation.

**The premise did not survive the first lookup, and nothing simmed was needed to break it.**
`charstate.load('Encomplete')` reports `trinket2 Stormbound Emblem of Dazar 308 — Champion
6/6`. The Emblem is **not Hero track**; it is already at its ceiling and **cannot** be taken
to 321. The trinket the assumption *does* apply to is the other one, Void-Reaper's Libram,
at Hero 2/6. Worth recording as a habit: **read the track before designing the comparison.**
It cost one `charstate` call and it changed what the baseline meant — a frozen 308 that
every challenger gets to out-scale, rather than a peer that upgrades alongside them.

**Results.** `gear --slot trinket2` screened all 17 bag candidates; none beat the Emblem at
current ilvl, best being Freightrunner's Flask 305 at -2.72% / -4.28%. `compare` then took
the plausible Hero-track contenders to 321 in one frame:

| variant | 1T/300s | 5T/120s |
|---|---|---|
| **libram321** (Hero 6/6, trinket2 untouched) | **+0.84%** | **+0.64%** |
| *(baseline — Libram 308 + Emblem 308)* | — | — |
| flask321 + libram321 | -0.94% | -2.73% |
| flask321 (Freightrunner, Hero 6/6) | -1.81% | -3.52% |
| drum321 (Drum of Renewed Bonds) — **FLOOR** | -1.93% | -3.84% |
| flask305 (as looted) | -2.65% | -4.35% |
| idol321 (Lost Idol of the Hash'ey) | -3.73% | -6.03% |

+16 ilvl on the Flask closes only ~0.85 points of a 2.72-point gap, so the swap loses at
every ilvl the character can reach. **The crests go on the Libram, not on a replacement.**

**⚠ The APPEND OVERRIDE CONTRADICTS UPSTREAM, and upstream is wrong here — measured, not
assumed.** Upstream's own items list gates every trinket rung on `trinket.N.cast_time>0`
and prefers a cast-time trinket **outside** Tyrant (`!pet.demonic_tyrant.active&
trinket.N.cast_time>0`, MID2 profile lines 67-72). Our `apl_append` says the opposite.
CRN triple (1500 iterations, `deterministic=1`, `threads=1`, seed 20260906, 1T/300s; arms
differ only in that one APL line, so separate invocations are structurally required and CRN
is the mitigation — same method as the 2026-08-21 entry):

| arm | dps | Δ | presses | channel time | buff uptime |
|---|---|---|---|---|---|
| pressed **inside** Tyrant (current override) | 131,650 | — | 2.89 | 5.75s | 18.4% |
| pressed **outside** Tyrant (upstream's preference) | 126,728 | **-3.74%** | 2.73 | 5.43s | 17.2% |
| never pressed | 125,460 | **-4.70%** | 1.00 | 2.00s | 1.4% |

The Tyrant pet-damage multiplier outweighs the 2s of casting the channel costs. Upstream's
rule is not a bug — it is right for a spec without a burst window that multiplies everything
— it is simply the wrong call for Demonology. **These are same-seed means used ONLY to price
the press timing**; the publishable medians are the profileset table above. Recorded in
`sim_overrides.json`'s note.

**The 2s channel IS modelled, which is what makes the ergonomic answer honest.** simc
implements the Emblem as `channeled = true`, 2s ticking every 0.5s, cancelling the ready
event and blocking autos (`unique_gear_midnight.cpp:3747`); it burned 5.75s of the 300s
fight. So "the Emblem wins" is a claim net of the cast, not one that ignores it — and the
`never pressed` arm prices the fumble at **-4.70%**, which is the number that actually
answers "is it worth the hassle".

**Firing-gate status: the 2026-08-27 false negative is now firing on FOUR items and cost
real time to clear by hand.** Void-Reaper's Libram, Lost Idol of the Hash'ey, Sylvan
Wakrapuku and Effigy of Ula'tek's Faithful all printed *"registered in simc's item table but
produced no buff and no action — possibly unimplemented"* and **all four are implemented and
firing** — they register under their spell names (Sylvan's `divebomb` ran 40.8×; the Idol's
`lynx_Haste` / `pangolin_Crit` / `focused_hunt` buffs are all in the output; the Libram's
`sacred_text` 7.4× with `sacred_duty` at 41.7% uptime). Distinguishing them from the three
genuinely-unmodelled ones (**Drum of Renewed Bonds** = `DISABLED_EFFECT` at
`unique_gear_midnight.cpp:5567`, **Ruby Whelp Shell** = on-use dead under a forced probe,
**Pulse Seeker's Oculus** = spell 1294326 not registered anywhere) took a manual grep of the
simc source per item. That is the gate the 08-27 entry already specified and it is now the
single highest-value unbuilt thing in this file: **resolve the driver's triggered spell ids
and look for actions/buffs under THOSE names.** Until it exists, every trinket screen needs
this manual pass, and a session that skips it will either throw away a working upgrade or
quote a floor as a result.

**One thing this run could not answer.** `drum321` is a floor: Drum of Renewed Bonds' on-use
is disabled in simc and its tooltip ("Echo the sound of your drum through a sacred loa
temple, aligning its beat with the will of the loa") is a mode-select with no numbers, so
its stats-only -1.93% / -3.84% would need the loa effect to be worth ~2% / ~3.8% to catch
the Emblem. Unknowable here; it is the one candidate where an in-game test would beat a sim.

### 2026-09-06 (cont.) — "do I want anything from Altar of Fangs 11+?" — the answer was in the enchant slot

Question: does **Altar of Fangs** at **+11** drop anything Encomplete wants. Answering it
properly needed three things the sim alone does not give: the **item API** (half the table
is unwearable), the **loot ilvl rule** (`mythic-plus/loot.md`: end-of-dungeon ilvl caps at
**+10**, so a +11 drops **Hero 3/6 ≈ 311** and the +11 only improves the *vault* row), and
**`charstate`** (which said the character has no tier set at all).

**Two lookups killed most of the table before any sim ran.**

- The item API resolves **Hydra Scale Wristguards as Mail** and **Poison-Proof Stompers as
  Plate** — and wrist (295) is this character's *weakest* slot, so the dungeon cannot fix
  the one slot that most needs fixing. **Pillar of the Fanged Altar** and **The Writhing
  Brood**, the two ids the KB file flagged as "outside the contiguous 2737xx block, must be
  read off the item API before being called trinkets", resolve as **Decor** and a **Mount**.
  That flag was right to be there and this closes it.
- `charstate` reports `tier=False` on all 15 equipped items and the generated profile carries
  no `set_bonus` line: **0pc**. The Pyrewalker pieces are the Prey set, not Damned Necrolyte.
  Altar of Fangs drops no tier, so the biggest available lever is not in this dungeon at all.

**Everything ranked in ONE frame, which is what made it answerable** (the 321 rows had been
measured in an earlier invocation against a *308* Libram, so part of each gain was just +13
ilvl — exactly the confound invariant 2 exists to stop):

| variant | 1T/300s | 5T/120s |
|---|---|---|
| Band of the Amani Warlord 308, enchanted + gemmed | +1.33% | +1.51% |
| **worn Signet 308, enchanted + gemmed** | **+1.25%** | **+1.62%** |
| **libram321** — spend the Hero crests on what is already worn | **+0.87%** | **+0.71%** |
| Knot of Writhing Serpents **321** → trinket1 | +0.67% | +0.65% |
| Preyhunter's Ring 295 (carries enchant + gem) | +0.63% | +0.98% |
| Vile Vial of Volatile Venom **321** → trinket1 | +0.27% | +1.01% |
| Strand of Warding Fangs **311** + gem | NOISE | -0.35% |
| *(baseline)* | — | — |
| Knot of Writhing Serpents **311** (as a +11 drops it) | NOISE | NOISE |
| Vile Vial **311** (as a +11 drops it) | -0.28% | +0.37% |

**At the ilvl a +11 actually drops, nothing from this dungeon is an upgrade.** The two
trinkets only pass the current 308 Libram after Hero crests go into them — and those same
crests spent on the Libram beat both. maxroll's nominal BiS trinket 2 (**Vile Vial**) is a
**loss** in the slot it would take (-0.83% / -2.01% evicting the Emblem, measured in the
prior frame).

**⚠ THE REAL FINDING WAS NOT A DROP — IT WAS AN EMPTY ENCHANT SLOT, and it beat every item
in the dungeon.** `gear --slot finger1` ranked a **295** Preyhunter's Ring *above* the worn
**308** Signet of Snarling Servitude (+0.66% / +1.12%). A 13-ilvl deficit winning is not a
gear result, it is a diagnostic: the bag ring carries `enchant_id=7967,gem_id=240890` and
the worn one carries **neither**. Split three ways to find out which half mattered:

| | 1T/300s | 5T/120s |
|---|---|---|
| Signet + **enchant only** | **+1.10%** | **+1.25%** |
| Signet + gem only | +0.11% | +0.37% |
| Signet + both | +1.15% | +1.52% |

**It is almost entirely the missing enchant**, which matters because the enchant is
unconditional while the gem needed an unverified socket (bonus id `13668`, present on every
socketed neck/ring in the export). The recommendation therefore does not rest on the socket
question at all. It also re-reads the Band of the Amani Warlord: its earlier +0.30% was the
gem it happens to carry, and once both rings are enchanted the two are a **tie** (+1.33% vs
+1.25%, bands overlapping in both frames) — so the dungeon ring is not an upgrade either.

**Gate to build (this is the second session in a row to want it).** `gear` and `compare`
should assert that **every enchantable worn slot carries an `enchant_id`** and say so. Nothing
in the tool mentioned the bare ring; it surfaced only because a 13-ilvl-lower item beat it and
I asked why. The 2026-08-25 entry already built half the case — there the artifact was an `@`
reference *silently carrying* an enchant, here it is a worn slot silently *missing* one. Both
are the same missing invariant: **the tool never says anything about enchants.** A character
walking around with an unenchanted ring is a ~1.2% standing loss that no gear question will
ever surface on its own.

**Firing-gate false negative, tally now SEVEN items.** Knot of Writhing Serpents, Vile Vial,
Coiled Fangstone and Tattered Amani War Banner all WARNed as "possibly unimplemented" and all
four fired (`writhing_venom_missile` 13.59× with its `writhing_venom` child at 776,610
compound; `empowering_venom` 2.90×; `coiled_fangstone` 5.51×; `tattered_amani_war_banner`
3.09×). Verifying them cost another manual pass through `unique_gear_midnight.cpp` plus a dig
into the gate JSON's `children` array — the Knot's damage is invisible at top level because
`missile->add_child(damage)` folds it in. Combined with the four from earlier today, the gate's
name-matching heuristic is now wrong far more often than it is right on Midnight trinkets.

### 2026-09-06 (cont.) — "what about Temple?" — and the enchant gate finally earns its keep

Same character, same day, third dungeon question: **Temple of Sethraliss** at +11. Unlike
Altar of Fangs this one has cloth in the two slots that actually need it — but the answer is
still "enchant your gear first", and this time the margin is not close.

**The KB had no loot table for this dungeon** (`temple-of-sethraliss.md` is a patch-day STUB,
`confidence: low`, explicitly "no route, no trash table, no affix guidance and no loot table
yet"). Pulled it from the **journal-encounter API** (2142/2143/2144/2145) and resolved every
id through the item endpoint, which is the same two-step the Altar of Fangs question needed.
Worth noting the shape: Avatar of Sethraliss lists each cloth piece **twice**, once as the
BfA id and once as a `239xxx` Midnight-refresh id — that is where this character's 295 Brood
Cleanser's Amice came from, and reading only the low ids would have missed the modern versions.

**Results, one frame:**

| variant | 1T/300s | 5T/120s |
|---|---|---|
| **enchAndSockets** — 4 missing enchants + 3 missing sockets | **+2.30%** | **+2.29%** |
| Charged Sandstone Band **321** (+ ring enchant) | +1.64% | +1.67% |
| Charged Sandstone Band **311** (+ ring enchant) | +1.24% | +1.16% |
| **enchOnly** — the 4 missing enchants alone | +1.18% | +1.25% |
| Bindings of the Slithering Current (wrist) **321** | +0.95% | +0.68% |
| Ouroborial Sash (waist) **321** | +0.80% | +0.65% |
| Jade Ophidian Band **321** | +0.73% | +1.19% |
| Bindings of the Slithering Current **311** | +0.59% | +0.28% |
| Ouroborial Sash **311** | +0.32% | NOISE |
| *(baseline)* | — | — |
| Staff of the Lightning Serpent **321** | NOISE | +0.37% |
| Sethraliss' Defiled Relic **321** — **FLOOR** | -1.23% | -0.34% |
| Tiny Electromental in a Jar **321** — **FLOOR** | -6.44% | -5.64% |

**The reading that matters is the pair `sandstone311` (+1.24%) vs `enchOnly` (+1.18%).** The
Sandstone Band variants *carry the ring enchant*, so at the ilvl a +11 actually drops, the
BiS-track ring is worth **+0.06% over simply enchanting the ring already worn** — inside the
error band. Its real contribution only appears at 321 (+0.46% over `enchOnly`). Putting the
enchant into both arms is what makes that legible, and it is the direct application of the
2026-08-25 `@`-reference artifact: **an item comparison where one arm silently carries an
enchant the other lacks is measuring the enchant, not the item.**

**The enchant audit, which is the actual finding of all three of today's sessions.** Parsing
`enchant_id`/`gem_id` out of every equipped line in the export against
`classes/warlock/demonology/gearing.md`'s enchant table: **head** (enchant + socket),
**shoulder** (enchant), **wrist** (socket), **waist** (socket), **feet** (enchant) and
**finger1** (enchant) are all bare; only chest/legs/finger2/weapon are done. That is
**+2.30%** sitting on a crafting table, more than any single item in either dungeon, and
nothing in `wowkb.sim` says a word about it. Enchant ids were resolved from
`spell_item_enchantment.inc` (Tier-2 quality, matching what the character already runs):
head 8017, shoulder 8001, feet 7963, ring 7967; sockets gemmed with 240898 (Flawless Deadly
Amethyst, the Mastery+Crit stone this spec's gearing.md names).

**⚠ THE GATE TO BUILD, now demanded by three consecutive sessions.** `gear`/`compare`/`check`
must audit **enchantable and socketable worn slots** and report bare ones. The slot list is
spec-dependent (Midnight puts sockets on head/wrist/waist via Miasmic Jewelbinder and no
enchant on the back at all), so it cannot be hardcoded blind — but even a dumb version that
printed "4 worn slots carry no enchant_id" would have opened today's first question with the
right answer instead of the third. This is now the single highest-value unbuilt gate in this
file, ahead of the triggered-spell-id resolver.

**Firing gate, running tally: eleven false-negative WARNs today, and two TRUE ones.** Tiny
Electromental in a Jar and Sethraliss' Defiled Relic WARNed and, unlike the other nine,
**genuinely produced nothing** — their gate runs contain no trinket action at all. simc
registers the BfA implementations against the **BfA** effect spell ids (267177 / 267402 at
`unique_gear_bfa.cpp:6196-6199`), which the Midnight-refreshed items do not carry. So both
rows are stats-only floors. That both classes of WARN appeared in the *same run* is the
argument for the resolver: the text is identical and only a source dig separates "working
fine" from "genuinely dead".

---

### 2026-09-10 — Pollynomial (Protection Paladin), Great Vault choice — **a two-hander wore a shield**

First tank, first paladin, and the first session where a `compare` variant produced a
confident, plausible, **structurally impossible** number.

**The question.** Four vault choices — three helms and a one-hand sword (Abyss Sabre 305) —
against an equipped main hand (Beast Collector's Cudgel **259**) left on from a Holy
experiment. The user's stated premise was that the bag held an obvious interim upgrade,
"Realm Splitter (295)".

**THE ARTIFACT — `compare` will equip a 2H main hand and keep the shield.** The first run
ranked `Realm Splitter 295` **above** the vault sword and above every capped variant, at
+26%. Realm Splitter (272274) is `inv_type 17` — **INVTYPE_2HWEAPON**, a 3.6-speed two-handed
sword. The profileset assigned it to `main_hand` and left `off_hand=` holding Wailing
Bulwark, a shield. simc happily simmed 2H-plus-shield and paid out roughly double weapon
damage. Three of six rows in that table were garbage, and **the garbage rows won**, which is
the only reason it got caught: a 295 beating a 321 was implausible enough to look at.

Invariant 3 ("a 2H main hand forces `off_hand=`") is implemented **only for the export's own
equipped layout**. Nothing re-checks layout when a *variant* changes a weapon slot. Failure #4
was "compared across invocations"; this is its structural sibling — *compared across
weapon layouts* — and one invocation does not save you from it.

`gear --slot main_hand` prints a `⚠ WEAPON SLOT — ranked but NOT usability-checked` banner
(simc carries no class weapon-usability data). That banner is real but it is about the **wrong
failure** and it lulled: usability is genuinely unknowable from simc, whereas **2H-with-shield
is trivially decidable from `inv_type`** and should never have been a warning at all.

> **GATES TO BUILD (in priority order).**
> 1. **Weapon-layout gate — HARD FAIL, not a warning.** Any variant (or gear candidate)
>    assigning `inv_type 17` to `main_hand` while `off_hand` is non-empty is refused. Same
>    for the inverse: a 1H main hand on a profile whose off_hand was force-cleared. This is
>    decidable from `item_data.inc` alone and there is no reason to ever print a number for it.
> 2. **`compare` must print `gear`'s weapon banner.** `gear` warns, `compare` says nothing,
>    and `compare` is the command you reach for on a cross-slot question. Hoist it.
> 3. **Candidate filtering must know 1H vs 2H.** `gear --slot main_hand` offered two
>    two-handers to a shield-using tank and ranked them 1st and 2nd.

**Second finding — the track IS recoverable from `bonus_id`, so the invariant at line ~2660
is false.** `item_tracks()` reads track/step only from `charstate.load()` (the PlannerState
tooltip dump), on the stated grounds that "the track CANNOT be inferred from the ilvl". True
but beside the point: the export carries `bonus_id`, and
`ItemBonusListGroupEntry.SequenceValue` **is** the step, with `ItemBonus` Type 34 `Value_0/1`
carrying the track group. Verified end-to-end this session against 12.1.0.69214 DB2:

| group | track | bonus ids | note |
|---|---|---|---|
| 614 | Adventurer | 12817-12824 | seq 7/8 carry `Flags=3`, disabled |
| 615 | Veteran | 12825-12832 | |
| 616 | Champion | 12833-12840 | 12838 = 6/6 = 308 |
| 617 | Hero | 12841-12848 | 12841 = 1/6 = 305 · 12846 = 6/6 = 321 |
| 618 | Myth | 12849-12856 | |

`ItemBonusListGroup.ItemGroupIlvlScalingID` is the **season** discriminator (11 = S1,
612-607; 12 = S2). It resolved the equipped Cudgel's `12793` as **Season 1 Hero 1/6** — a
leftover, which is exactly the kind of thing a track column would have made obvious at a
glance. Regenerate the map from the CSVs per build; do **not** hardcode the bases.

Two consequences, both large:
- **Bag and vault candidates become track-resolvable.** The PlannerState dump only ever sees
  *equipped* gear, so today the tool cannot say what track a vault item is on — which is the
  single most important fact in a vault decision, because a fresh Hero 305 and a capped
  Champion 308 are the same ilvl and *not* the same item.
- **"Sim everything at its track cap" becomes mechanical**, instead of the hand-written
  `,ilevel=321` strings this session used.

**Third finding — the PlannerState dump disagreed with the export, and nothing noticed.**
The dump (2026-09-09 23:05) is *newer* than the export (21:39) yet reports `mainhand` Hero
1/6 (=305) where the export holds a 259 Cudgel, and Champion 4/6 / Hero 2/6 for two trinkets
the export puts at 295 (`bonus_id 12834` = Champion 2/6, twice). The **export is internally
self-consistent and the dump is not**. With a bonus-id decoder these two sources can be
cross-checked; today they silently diverge and `item_tracks()` trusts the dump.

> **GATE:** cross-check dump track against bonus-id track per slot; on disagreement, report
> both and trust neither silently.

**Firing gate, running tally: one TRUE positive.** `Abyss Sabre` (spell 1253357) WARNed and
the WARN is **correct** — but the message is wrong. It reads "produced no buff and no
action"; in fact simc creates the action (`torments_duality`, `unique_gear_midnight.cpp:4216-4282`,
registered at :5599) and executes it **0.0 times in 300s** despite RPPM 5. So the item is
fully implemented upstream and still contributed nothing, and the sabre's numbers in this
session are a **floor**. Worth noting the effect is half of set 1970 "Torment's Duality" with
Radiant Foil (251885) — and its Void Tear debuff is inert without the partner, which a
shield-using Protection Paladin can never equip.

> **GATE:** the gate says "no buff and no action" when an action exists at 0 executes.
> Distinguish *absent* from *present-but-never-fired* — they point at different causes.

**Not an artifact, but the session's most useful number:** dropping the tier helm for either
non-tier Hero 305 helm cost **~8.5 points of relative DPS** (+15.0% → +6.5%), i.e. the 4pc
dwarfed a 3-ilvl-per-slot question. Any gear command that ranks a tier slot without reporting
the resulting set-piece count is inviting that mistake.

### 2026-09-11 — Encomplete `--all-slots`: the only "upgrade" in sixteen slots was a slot he cannot fill

The question was the player's own rule, put as a challenge: *"ilvl and raw int always trump
secondary stats — it's not worth replacing a Hero piece with a Champion piece for better
stats, trinkets excepted. Is that not true?"* `gear encomplete --all-slots` against the
2026-09-06 export ranks every equipped/bag/vault row per slot, so it tests the rule against
the actual bags rather than against a principle.

**The rule survived, emphatically.** Fifteen of sixteen slots put `_baseline` (current gear)
first or statistically tied for first. Nothing in the bags beat what is worn, at any ilvl
gap available. The largest same-slot spread was `main_hand`, where a **311** Nibbles Training
Rod lost to the equipped **318** Aln'hara Cane by −3.78% — ilvl winning across a 7-point gap
even against a differently-statted weapon. The trinket slots did not produce a counterexample
either: the best bag trinket was −0.01% (a tie) in `trinket1` and −2.66% in `trinket2`.

**The sixteenth slot was `off_hand`, and it is fiction.** The frame ranked Vessel of Last
Rites 305 at **+8.73%** and Soulsingers Horn 295 at **+8.25%**, both `significant`, against an
empty slot. Both are `inventory_type` **23** (holdable) — and the equipped Aln'hara Cane
(245770) is `inventory_type` **17**, a staff:

```
{ "Aln'hara Cane", 245770, …, 4, 17, 2, 10, 1, 3600, … }   # quality 4, invtype 17 (2H), class 2 subclass 10 (staff)
{ "Vessel of Last Rites", 159667, …, 3, 23, 4, 0, 1, 0, … } # invtype 23 (holdable)
```

A staff occupies both hands. There is no configuration in which this character equips either
item, and the harness ranked them anyway, flagged only by the generic
`⚠ WEAPON SLOT — NOT usability-checked` banner — which reads as "confirm the weapon is
wearable", not "this entire slot is unreachable". Left unread, an 8.7% `significant` row is
exactly the kind of number that gets acted on.

This is the **same defect as 2026-09-10's shield-wearing two-hander, from the other side**:
that session had the tool offer two-handers to a shield user; this one had it offer off-hands
to a staff user. The 2026-09-10 gate was written as a `main_hand` candidate filter, and so it
did not fire here.

> **GATE:** `inventory_type` of the equipped `main_hand` decides whether `off_hand` is a slot
> at all. When it is 17 (2H weapon), `off_hand` must be **skipped entirely** — not ranked with
> a banner — and `--all-slots` must say *why* it was skipped. The mirror already exists for
> `main_hand`; this is the same fact read in the other direction, and both should come from one
> helper, not two. Decidable from `item_data.inc` alone; no client, no usability table.

**Second finding — the `head` frame's `_baseline` was not the player's head.** Every other
frame encodes the equipped helm as `bonus_id=6652/12836/13662/13696` → **ilvl 302**. The
`head` frame encodes **12834** → **ilvl 295**, and its baseline lands at **108,447** against
~131,500 everywhere else. Same item id, same content_tuning, one bonus id different, and a
17% baseline gap that no 7-ilvl swing can explain.

The consequence is narrow but real: `head` deltas are measured against a degraded reference,
so they read better than they are. It does not change this session's answer — the best head
candidate was −0.00% *against the weakened baseline*, hence worse against the true one — but
the frame's absolute numbers are unusable, and a slot whose baseline silently differs from
every sibling frame is a defect the output did not mention.

> **GATE:** `--all-slots` builds N frames from one export; the equipped set must be
> **byte-identical** across all of them except the slot under test. Hash the non-test slots per
> frame and fail loudly on divergence. A per-frame `_baseline` median that differs from the
> run's median `_baseline` by more than the error band is the same alarm from the output side
> and is cheap to print.

**Firing gate — the 2026-08-27 false positive recurred, in all sixteen frames, and it cost an
answer a second time.** Void-Reaper's Libram (1253113) WARNed "no buff and no action" in every
frame. It is implemented (`unique_gear_midnight.cpp:2829`, registered at `:5552`) and it
**fired**: `sacred_text` at **7.39 executes / 300s**, `sacred_duty` present in `buffs`. The gate
misses it for the reason 2026-08-27 diagnosed — it matches on the item's name, and this effect
registers its children under their own spell names (`sacred_text` 1266394, `text_ignite` 1266407,
`sacred_duty` 1266403), none of which contain "libram".

The gate that entry specified was never built, so the WARN reappeared and this session repeated
the exact mistake the entry predicted: it told the player the run's numbers were a **floor**
because the Libram "produced nothing". They were not a floor. The proc is already in them.

> **GATE (restated from 2026-08-27, still unbuilt, now with two victims):** match the firing
> gate on the driver's **triggered spell ids**, not the item name. Until then the WARN text must
> not say "possibly unimplemented" — it must say "no action or buff matching this item's NAME;
> the effect may register under its spell's name — grep the JSON's `stats`/`buffs` for the ids in
> the implementation's comment header before treating this as unmodelled."

simc's own caveat on this trinket stands and is unrelated: the implementation raises
`UNVERIFIED_IMPLEMENTATION` — *"Sacred Text dot is assumed to be able to proc while Sacred Duty
buff is up."*

### 2026-09-11 — Pollynomial (Prot Paladin) Season 2 vault choice
Question: which of four vault rewards to take — the tier helm at Hero 1/6, Abyss Sabre at
Hero 1/6, or two non-tier Hero helms — and where 100 Hero Mistcrests should go.

Answered in one `compare` frame, 8 variants. Nothing about the gear question was hard: two
of the four vault helms break the 4pc (`Radiance of the Consecrated Flame`, worn 4/5 with a
non-tier chest) and cost **-7.5% / -5.0%**, which dwarfed every ilvl and track consideration
in the table — Step 7 earning its place for the second time.

**The name-matching gate failed for a THIRD time, and this time with a new mechanism.**
Abyss Sabre (1253357, `weapons::torments_duality`) WARNed "produced no buff and no action"
in both sabre arms. Following the 2026-08-27 / 2026-09-10 entry's instruction, I checked the
implementation's comment-header spell ids instead of trusting the WARN — and the effect is
**fully modelled and firing**: `abyss_sabre` at **36.95 executes / 159,648 damage per 300s**,
plus a `void_tear` debuff on the target at 2.72 starts. Roughly 532 DPS, which is essentially
the whole +0.84% the sabre showed over baseline.

The new wrinkle, and why the previous entry's fix would **not** have caught this one: the
implementation creates a **proxy parent action** (`torments_duality`, an `ACTION_OTHER` with
`name_str_reporting = "Torment's Duality"`) and hangs the real damage action on it via
`proxy->add_child( damage )`. The proxy legitimately has **0 executes of its own**. In json2
the child is **nested inside the parent's `children` array and does not appear in the flat
`stats` list at all** — my own first diagnostic pass dumped all 34 entries of `stats` and
found no `abyss_sabre`, which read exactly like confirmation of the WARN. The debuff is
likewise not on the player: it is a target debuff, under `sim.targets[].buffs`.

> **GATE (extends 2026-08-27, still unbuilt — now three victims and two distinct causes):**
> the firing gate must (a) match on the driver's **triggered spell ids**, not the item name,
> and (b) **recurse into each stat's `children`** rather than scanning the flat `stats` list,
> and (c) search **target** debuffs (`sim.targets[].buffs`) as well as player buffs. A proxy
> parent at 0 executes is a normal, correct reporting shape and must never by itself read as
> "no action". Until it is built, the WARN text must not say "possibly unimplemented".

Cost side, and the finding that actually decided the crest half of the question: Pollynomial
holds **exactly 100 Hero Mistcrests** and does **not** hold `Hero of the Mist` (62414), so
Hero ranks cost the full 20 — 100 crests is **precisely one Hero item 1/6 → 6/6, and no
more**. Spending them on the weapon is worth **+3.17%** (current sword) to **+4.17%** (Abyss
Sabre); spending them on the helm is worth **+0.86%**. Nearly a 5x difference per crest, and
invisible to anything that ranks by ilvl.

Also worth remembering: the two vault items differing *only* in secondaries (Abyss Sabre
Haste/Mastery vs the equipped Swordsman's Emanation Crit/Haste — identical 1H sword,
identical 2.60 speed, identical 5259 Str / 7889 Stam / 7000 secondary budget) split
**+0.84% on 1T but only +0.36% on 5T**. The whole gap is the proc; the stat reshuffle itself
is a wash. A single-fight-style answer would have overstated it by 2x.

# Cooldown HUD — project root

> ## ⛔ SUPERSEDED — 2026-08-05
>
> **This project is replaced by Combat Assist Plus (`projects/combat-assist/`, `/cap`).**
> There is one addon riding the Cooldown Manager going forward and it is not this one.
>
> **Why.** CDMProbe started as "what can I do with the CDM" and grew into a
> **next-action decision engine** — one answer per GCD. That runs against Blizzard's
> stated position on combat addons, and the 12.0 Secret-Values restrictions had already
> begun capping what it could calculate. cap is the same premise re-aimed at what the
> platform invites: re-present, grade, contextualise — **narrow** the decision instead of
> making it. See `projects/combat-assist/specs/spec.md` §1 and §4's *Cooldown HUD
> boundary*.
>
> **What that means in practice:**
>
> - **No new work.** The multi-class rollout is stopped; Phases 3–5 will not be built.
> - **The Havoc flight is MOOT as a CDMProbe deliverable.** Everything below that names
>   it as "the in-game gate" is describing a gate on work that is no longer happening.
> - **No code is ported to cap.** The `State → Coach → Binder → Renderer` pipeline was
>   shaped around authoring a priority answer, which is the one thing cap does not do;
>   inheriting it would smuggle the premise back in.
> - **Two things here stay authoritative and are actively read:**
>   1. **Measured client facts** — already written into `knowledge/addon-dev/` (that KB
>      is the authority, not these docs). §4.8's secret-display channels are what cap's
>      whole visual design rests on.
>   2. **Per-spec rotation research** — `specs/demonology/` especially, which cap
>      harvests into its catalog format.
> - **The auto-deploy exception below is dead** with the project. cap has no standing
>   exception; releasing it is ask-first.
>
> **Read the rest of this file as history.** Its present-tense claims about active work,
> gates and next phases were true on 2026-08-04 and are not now.

A standalone companion app (NOT the KB): a spec-specific overlay that skins
Blizzard's built-in **Cooldown Manager** under Midnight 12.0. Registered specs:
**Demonology** (266, play-settled), **Destruction** (267, shipped 2026-07-29, flown
2026-07-30), **Retribution Paladin** (70, shipped 2026-08-02, **cannot be flown** — the
player has no max-level Paladin) and **Havoc Demon Hunter** (577, shipped 2026-08-03,
**flown twice: the first pass FAILED — Fury is a SECRET value — and the Phase-1 remediation
then flew CLEAN. A third flight is owed for v0.32.95's three new features and is THE in-game
gate**, see `docs/status.md` → Active work). Every other
spec resolves passive by design.

**The W4 pipeline is LIVE** (`/cdmp hud` runs `State → Coach → Binder → Renderer`; the
old engine was deleted at the W4 cutover).

## Auto-deploy is OK for this project

Standing exception to the workspace-wide "cutting a release is ask-first" rule
(root `CLAUDE.md`), **scoped to the CDMProbe addon only**: when a change is ready
for me to eyeball/test in-game, **just cut it and deploy** — commit the feature
work, `wowkb.addon release cdmp --patch`, and tell me to `/reload`. No need to ask
first for a test build; iterating on the HUD *is* the loop. (This covers routine
test cuts; still flag anything genuinely irreversible or out-of-band.)

## Doc map

The docs split **general** (spec-agnostic — the product, the pipeline) from
**per-spec** (the rotation brain for one spec). Adding a 2nd spec is additive: a new
`specs/<spec>/` folder + a Coach spec table, with **no edits to the general docs**.

**General — `docs/`:**

- **`docs/design.md`** — the vision + design language (the non-technical *what & why*:
  what the product is, how it looks/feels, the enhance-don't-replace stance).
- **`docs/architecture.md`** — **THE technical design doc.** The
  `State → Coach → Guidance → Binder → Renderer` pipeline, the data-shape contracts, the
  invariants, and the Secret-Values reality the pipeline is shaped around. Read it before
  touching the data/display seam.
- **`docs/virtual-cdm-plan.md`** — ✅ **built and flown**: the virtual CDM panel — the
  HUD draws its own icons for abilities Blizzard's Cooldown Manager does not track, so a
  spec's floor press stops being invisible (Destruction was blank for 31 % of a pull).
  Only the v0.32.36 **re-fly** is outstanding, and that needs a live session, not code.
- **`docs/roster-state-plan.md`** — ✅ **THE PLAN IS COMPLETE.** Phases 1 + 2 + 3 + 4 DONE
  (2026-07-31), Phase 6 DONE (2026-08-01), and **Phase 5 — the last and largest — DONE
  2026-08-03**: anchor State on the spec's declared **roster** (abilities + auras) rather than
  on the CDM database, plus the correctness fixes and the **fixture inventory** of CDM edges
  that had to come first. Written out of a client-correctness review of `State.lua`
  against `knowledge/addon-dev/cooldown-manager.md`.
  ⏳ **Code-complete is not flown** — Phase 5's acceptance is one **max-level Retribution**
  pass, which discharges Retribution's own gate, the v0.32.36 re-fly and Phase 6.2's fragment
  pass at the same time. `docs/status.md` owns that gate.
  **Phase 5 inverted the anchor**: the spec's roster leads and the CDM became **one evidence
  source joined against it**. The root fix is that an ability's cooldown and its charges are
  now read about the **same spellID** — they used to resolve on two different ladders, which
  on a row whose identity flips (Judgment) meant comparing one ability's cooldown against
  another's charges, and that was three of the five Retribution flight defects. **Read §6.3
  before touching `State.lua`** — eleven implementation decisions there are *not* in the plan
  text and a fresh reader will otherwise revert them. **Read §6.1's ⚠ CORRECTION** too: the
  `judgeable`/`secretGate` "cap at available and say why" mechanism the phase was planned
  around **does not exist** (its consumer died at the W4 cutover); "cap at available" and
  "never cue" turn out to be the same pixels, and the "why" lands in the decision log's `DR:`
  field.
  **Phase 1 shipped the inventory** — `addon/CDMProbe/tests/fixtures/cdm-cases.lua`, now 107
  declarative cases — where a `pinned-defect` case asserts the contract answer and FAILS ON
  PURPOSE, so the fix turns its own case red and flips the status in the same diff.
  **Phase 2 (v0.32.46) landed all ten correctness fixes** and cleared every pin. The
  headline: the DoT read now has a channel that
  **self-clears** (`item.auraDataUnit` + `item.PandemicIcon`), where before a whole pull
  produced 169 "refresh the DoT" cues and **zero** "apply it".
  **Phase 3 (v0.32.48) separated the keybind from the cue channel** — the DrawList gained a
  `keybinds[]` channel so `cues[]` means *decisions*, and the keybind now resolves down the
  **rung ladder** (3 → 4 → 5), which is what gives **Hellcaller its key hint** — ✅ **flown
  the same day**: `cd=164597 … (Wither) key=F drew=F`, 16 key hints against 2 cues. Corpus
  **0 `pinned-defect` / 21 `fixed`**.
  **Phase 4 shipped the roster coverage probe** — `Coverage.lua` + `/cdmp hud coverage`:
  does the CDM actually *track* every id the spec declares, or is the HUD silently blind to
  one? It was also the required replacement for `pulse.dropped`, which Phase 5 deleted. Its
  wholesale guard (an empty scan reports "the read refused", never "your roster is blind")
  is the load-bearing part; Crashing Chaos 417234, its one live instance, was **deleted**
  rather than covered — so the `blind` verdict is fixture-proven only. ⚠ The first flight
  then found `blind` was **crying wolf** (every instance was an ability the character does
  not have), so v0.32.54 fenced it on knownness — see §5.2.
  ✅ **Flown 2026-08-01** — one `/cdmp flight` pass discharged Phases 2, 3 and 4, the
  `ChargeGained` re-fly and the `C_AssistedCombat` rider. **§5.2 is the flight record.**
  **Phase 6.2 gave the resource rail its EXACT unit** (v0.32.73, 2026-08-01) — `State.lua`
  now reads `UnitPower(unit, type, true)`, so the pipeline sees Soul Shards as the **0–50
  fragments** the game actually stores rather than the 0–5 it displays. That was a **missing
  capability, not imprecision**: a true 1.9 arrived as `1`, so "you are one Incinerate from a
  Chaos Bolt" was unsayable and the HUD said "build". Every gate in both brains is
  fragment-denominated now (integers — floats only at the log's edge), simc's `<= 4.2` /
  `<= 4.6` are restored verbatim, and Destruction projects **builders** as well as spenders.
  ⚠ Costs go the OTHER way (`C_Spell.GetSpellPowerCost` pre-applies the divisor), so the
  rename — `ctx.shards` **deleted**, `*Frags` everywhere — is the mitigation for a silent 10×
  error. **§7.2 is the record.** ⏳ Its in-game pass rides with the flight below.
  **Phase 6 moved the in-flight power projection out of State and into the Coach** —
  `ns.Coach.InflightPower`, a pure function of the pulse's cast history — deleting
  `inflightIncoming`/`projectIncoming`/`spendStartShards`, the `ns.SpecPowerDelta` injection
  and **both `Enum.PowerType.SoulShards` hardwires**, the last class-specific literals in
  State's code. ⚠ The double-deduction guard was **dropped, not ported** (a deliberate
  behaviour change) and the `"stopped"` cast phase became load-bearing — **§7.1 has both**.
  ⏳ Two things remain and neither is a re-pull: the **v0.32.36 re-fly is BLOCKED** (the
  decision log carries no combat flag, so its `w:-` acceptance cannot be read — fix the log,
  then re-read the capture already on disk), and the `/cdmp rt states` visual card.
  `status.md` → *Owed: the v0.32.36 re-fly* has both.
  **§3.11, §4.2, §5.1, §5.2 and §7.1 are the records of what actually changed**, including the deliberate
  deviations — read them before "fixing" any of those back, and read §3.1–§3.10 / §4.1
  before "fixing" anything a case pins.
- **`docs/field-fixes-plan.md`** — ✅ **done, history** (Phases A/B/C/C2, v0.32.28–31): the
  correctness + capability fixes the first live session surfaced, and the record of the live
  pass that confirmed them. Read it for the field evidence, not for outstanding work.
- **`docs/status.md`** — **THE live worklist.** Released version, the phase ledger, open
  items, and the **improvements/backlog** (the single place feature + quality work lands).
  **Routing — "plan / do the next cooldown-HUD thing" starts HERE:** read `status.md`
  first. If **Current state → Active work** names an item, *continue that* (it points at a
  plan doc + the current phase — pick up the next phase); if there is **no** Active-work
  line, pull the next item from **Improvements / backlog** and, once chosen, add an
  Active-work line for it. Only fall back to asking the user when both are empty/ambiguous.

**Per-spec — `specs/<spec>/`:**

- **`specs/demonology/rotation.md`** — the flat priority list (APL) the Coach implements.
  The rotation spec of record.
- **`specs/demonology/notes.md`** — Demonology facts: ability roster, the burst window
  (Tyrant + Dreadstalkers), Demonic Core proc, shard mechanics.
- **`specs/demonology/input-contract.md`**, **`observability-map.md`** — reference-only:
  the evaluator's inputs and what the game exposes vs. hides.
- **`specs/retribution/`** — the same four docs for **Retribution Paladin** (v1 profile
  **Templar**, Herald of the Sun as a delta section). **Shipped 2026-08-02** —
  `SpecRetribution.lua` + `CoachRetribution.lua` implement `rotation.md` L1–L12, with a
  branch oracle now **87 tests** (68 at ship; the flight's five defects and Phase 5 added the
  rest). The project's **first non-Warlock spec**, and the one that proved
  the seam is class-agnostic — at the cost of three pipeline generalisations it had deferred
  (`display = "none"`, `ns.Coach.PowerContext`, the hero-tree vocabulary).
  ⚠ Its defining fact is **not** the rotation: **four of its nine Essential buttons** —
  Judgment, Crusader Strike, Blade of Justice, Wake of Ashes — keep their cooldown on a
  **charge category** with `RecoveryTime = 0`, so `ns.BaseCooldown` reads 0 and the napkin
  has nothing to count down from. ⚠ *This said "six" until 2026-08-03; Avenging Wrath and
  the two spenders are not among them.* **Readiness itself is not lost** — it comes from the
  **charge count**; what is genuinely lost is `SOON` and `Escalate`'s overdue call, i.e.
  decoration rather than presses. `usable()`'s "the count outranks the cooldown read" rule
  carries far more weight here than on Destruction — and for a **1-charge** pool the count
  and the cooldown are the same fact and must AGREE (the v0.32.90 defect).
  `observability-map.md` has the open questions the live pass must settle.
- **`specs/havoc/`** — the same four docs for **Havoc Demon Hunter** (v1 profile
  **Fel-Scarred**, Aldrachi Reaver as a delta section). **Shipped 2026-08-03** —
  `SpecHavoc.lua` + `CoachHavoc.lua` implement `rotation.md` **L1–L15**, with a branch oracle
  of **100 tests**. The project's **4th spec and 2nd class outside Warlock**, and it needed
  **zero pipeline generalisations** — which is itself the finding.
  ⚠ **Its defining fact is an observability one, and it is worse in KIND than
  Retribution's:** three Essential buttons report a base cooldown that is not absent but
  **WRONG** — Fel Rush 195072 reads **1 s** against a real 10 s, Immolation Aura 258920
  reads 2 s against 30 s, Vengeful Retreat 198793 reads 0.5 s against 25 s, because a short
  *shared-category lockout* sits on the spell row while the real recovery lives on a charge
  category. A lie defeats the mitigation an honest zero gets (HudNapkin's declared-`chargeCD`
  fallback is gated on `not (len > 0)`, which a lying 1 passes). **All three are 1-charge
  categories**, so `usable()`'s one-charge rule makes the count veto the early read — **the
  press is protected; only the decoration lies.** The napkin fix is **deliberately unshipped**
  and the flight arbitrates it.
  ⚠ **Three rotational presses are filed CDM-Utility** (Felblade, Vengeful Retreat, Fel Rush
  — the last with *two* CDM rows) and that needed **no pipeline edit**: both fences read the
  **spec-authored `cadence`**, never the CDM category. The next tank spec meets the same shape.
  ⚠ **The meta fork is ONE cascade**, not simc's two lists — both overrides are 1:1 display
  overrides on their own base's frame, so `ctx.inMeta` touches exactly two lines.
  `observability-map.md` → *THE FLIGHT'S JOB* is the whole in-game procedure and **both**
  acceptance sets (Havoc's own, plus `roster-state-plan.md` Phase 5's, which had nowhere else
  to run).
- **`specs/destruction/`** — the same four docs for **Destruction Warlock** (v1 profile
  Diabolist, Hellcaller as a delta section). **Shipped 2026-07-29** —
  `SpecDestruction.lua` + `CoachDestruction.lua` implement `rotation.md` L1–L13, with a
  branch oracle now **116 tests** (57 at ship). ⚠ Of the three inputs once listed as *missing rather than merely
  secret*, **DoT presence + refresh is now solved** (roster-state-plan §3.10, v0.32.46 — the
  per-frame `auraDataUnit`/`PandemicIcon` verdict); **in-combat charges** and **target health**
  are still missing. `rotation.md` → *Implementation notes* and
  `docs/status.md` → *Open items* carry what the live pass has to settle.

**Machine-readable contracts (source of truth — prose defers to these):**

- `guidance-contract.json` — the Stage-2 Guidance output contract.

**History — `docs/archive/`:** done/superseded plans — the whole W4 build sequence +
phase handoffs, the M-series plans, the frozen `milestones.md` log, and the retired
old-engine QA docs. **Nothing here is current**; read before re-proposing a dead end,
don't cite it as fact. See `docs/archive/README.md`.

## Layout

- `docs/` — the general design docs (above).
- `specs/<spec>/` — per-spec rotation brain + facts. `demonology/` (shipped, play-settled),
  `destruction/` (shipped, flown), `retribution/` (shipped 2026-08-02, **cannot be flown** —
  no max-level Paladin) and `havoc/` (shipped 2026-08-03, **not yet flown — the gate**).
  Adding another is `docs/adding-a-spec.md` — ⚠ **read its CORRECTIONS box first**; the
  Retribution and Havoc runs between them found nine stale claims in the recipe body.
- `addon/` — the **CDMProbe addon** (`michac/CDMProbe`), its **own git repo**,
  **gitignored** from this workspace. Has its own `CLAUDE.md` for the
  deploy/release workflow (a plain push does NOT reach the game — cut a release).
  This is the code source of truth.
- `prototype/` — HTML design prototypes (layout directions + the CRT visual-style
  exploration that drove the v1 aesthetic).

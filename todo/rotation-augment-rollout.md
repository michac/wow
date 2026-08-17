# Rollout — every `rotation.md` becomes a supplement to `simc-apl.md`

**Status:** planned. Pilot (Havoc) shipped 2026-08-17 in `55a9081`.
**Owner doc.** Milestone log at the bottom; update it as waves land.

## The change, in one line

`simc-apl.md` (generated, Tier 1, citable) says **what the priority is**.
`rotation.md` says **why each rung sits there** and **what the sim does not model**.
Nothing that can be read off the APL is restated anywhere.

Contract enforced by tooling: `augments: simc-apl.md @<sha>` in front matter, checked by
`wowkb.simc --kb --check`, which reports when the APL moves past the commit the reasons
were written against.

## An APL's line count is not its button count — organise by ability

Measured across all 36 specs: **9 buttons minimum, 16 median, 23 maximum.** The 12×
spread in APL line count (17 → 203) collapses to a **2.5× spread in abilities**.

| Spec | APL lines | sub-lists | abilities pressed |
|---|---:|---:|---:|
| `demon-hunter/vengeance` | 203 | 16 | **18** |
| `warrior/arms` | 146 | 10 | **22** |
| `warlock/destruction` | 125 | 7 | **16** |
| `demon-hunter/havoc` | 35 | 2 | **12** |

Three things inflate a line count, none of them keybinds:

1. **Hero trees write the same rotation twice.** Destruction's `aoe_hc` (28 lines) and
   `aoe_dia` (28) are the AoE rotation once per hero tree — 56 of its 125 lines are two
   versions of one thing, and a player runs one. Demonology's `diabolist` (16) and
   `soulharvest` (14) are the same.
2. **One button appears at many rungs.** Destruction presses `conflagrate` at 12 points
   in the list, `incinerate` at 10, `chaos_bolt` at 10.
3. **A third of the lines are not abilities.** Destruction: 11 `variable` lines, 10
   `call_action_list` dispatches, 12 item/potion/racial lines — 33 lines with no
   keybind behind them.

Havoc is short because **12.1 flattened it** — one combat list, no sub-lists, no
dispatch, no in-combat variables. That is a property of that one rewrite, not of the
spec being simple.

**Consequence for this rollout:** `## Why each rung is there` is organised **per
ability**, not per APL line — 9 to 23 entries for any spec in the game. What actually
varies is the **branch structure**, so the section carries a short companion list
explaining what each sub-list is for (hero tree, AoE, cooldown window). Vengeance is
then ~18 abilities + ~16 branch notes, not 203 bullets.

## Inventory — what is actually left

40 specs. 36 have an APL; Havoc is done. **35 remain**, in two tiers that need
different work.

### Tier A — 5 specs, already 12.1-verified, no banner

Pure shape conversion. Content was swept on 2026-08-11 and is trusted; the job is to
stop restating the list and add the reason layer.

| Spec | APL actions |
|---|---:|
| `demon-hunter/vengeance` | 203 |
| `demon-hunter/devourer` | 157 |
| `warlock/destruction` | 125 |
| `warlock/affliction` | 98 |
| `warlock/demonology` | 61 |

⚠ **These are the biggest APLs in the game.** The "easy" tier by content is the hard
tier by size.

### Tier B — 30 specs, banner'd at `patch: 12.0.7`

Shape conversion **and** the first 12.1 read these files have had. Their APLs are
mostly small (17–146, median ~62) and their rotation.md files are already short
(134–192 lines, median 156, 5,411 lines total) — so unlike Havoc there is little to
evict. The work is correcting claims against a 12.1 APL that did not exist when they
were written.

All 30 carry the `NOT RE-VERIFIED FOR 12.1` banner on `rotation.md`, `abilities.md` and
`builds.md`.

### Out of scope — 4 specs with no upstream APL

`evoker/preservation`, `monk/mistweaver`, `paladin/holy`, `shaman/restoration`. simc
does not model them. Their `rotation.md` cannot become a supplement to a file that does
not exist, so they stay full standalone rotation docs. **They still need a 12.1 read**,
but that is a different job — do not fold it in here.

## Sourcing — what an agent may build a "why" on

The central risk is confabulation: an agent authoring reasons for a spec it does not
know will invent mechanics, which is precisely how the errors the Havoc review found got
in. The defence is a strict source floor.

**Current and Tier 1 for every spec** (regenerated 2026-08-11 from live 12.1 game data):
- `talents.md` / `talents.json` — what exists, what is a choice node, hero placement
- `ability-inventory.md` — the spec's real ability set
- `_meta/patch-notes/12.1.md` → CLASSES section (26 class entries)
- `simc-apl.md` — the priority itself

**Usable for mechanics, NOT for numbers** (banner'd, Tier B only):
- `abilities.md`, `builds.md` — describe 12.0.7. Cooldowns and mechanics are mostly
  still true; every absolute number is suspect.

**Tier 3, corroboration only:** Icy Veins, method.gg, maxroll (`maxroll-*.md` exists for
6 specs only).

**Hard rule:** every reason must be traceable to a named source, or carry an explicit
`⚠ Inference, not Tier 1` marker — the pattern Havoc's Immolation Aura entry uses. An
unmarked invented reason is the failure mode this rollout must not produce.

## Per-spec instruction template

Each agent gets a written brief. Constant across specs:

1. **Read** `knowledge/_meta/writing-claims.md`, the spec's `simc-apl.md`, its current
   `rotation.md`, `talents.md`, `ability-inventory.md`, and the spec's section of
   `_meta/patch-notes/12.1.md`.
2. **Rewrite `rotation.md`** to the target structure (below).
3. **Never** restate the priority. Reference an action by its **simc action name plus a
   plain-English gloss** — `` (`essence_break`) — cast when Eye Beam is more than 4s
   from ready``. **Never paste a verbatim `,if=` condition**; that reintroduces the
   exact strings that drift. (The Havoc pilot violated this seven times and needed a
   hand fix — call it out explicitly in every brief.)
4. **Front matter:** `patch: 12.1`, `fetched`/`reviewed` stamped today, `sources:`
   leading with `simc-apl.md`, and `augments: simc-apl.md @<sha>` copied from that
   spec's `simc-apl.md` pin.
5. **Corrections are rewrites**, never notes appended under a surviving stale claim.
6. **Do not touch** `projects/**`, `simc-apl.md` (generated), or any other spec.

### Target structure

```
front matter          incl. augments: simc-apl.md @<sha>
# H1 + lede           the core loop, flat, current-truth, no hedges
## Why each rung is there
## What the sim doesn't model
## Talent gates that change the priority
## Hero-tree branches
## Changelog
```

### Tier B additions

- The `NOT RE-VERIFIED FOR 12.1` banner comes **off `rotation.md`** once the file is
  rewritten against the 12.1 APL — but **stays on `abilities.md` and `builds.md`**,
  which this pass does not touch. The banner is shared boilerplate across all three;
  removing it from one requires the other two to still carry their own copy. *(Open
  decision — see below.)*
- Every claim carrying an absolute number (damage, healing, HP, consumable) must be
  re-checked or deleted: 12.1 raised player health and creature damage 25% game-wide.

## Execution

### Wave 0 — a second pilot, on the most BRANCHED APL (do this first)

`demon-hunter/vengeance` — 203 lines, but only **18 abilities** across **16 sub-lists**.
It is the pilot not because it has more buttons (it has 6 more than Havoc) but because
it has **8× the branch structure**, and branching is the thing Havoc's flattened APL
never exercised.

The question it answers is **not** "does one-bullet-per-rung scale" — measurement above
says the ability layer is 9–23 entries everywhere. It is: **how does a supplement
express 16 sub-lists without turning into a map of the APL?** A reader needs to know
which branch they are in and why, without the file redrawing the dispatch tree.

Deliverable: the converted file, plus an explicit judgement on whether the branch
companion list works, needs collapsing (several sub-lists are usually one idea — hero
tree A vs B), or needs a different treatment entirely.

### Waves 1–6 — the rest, batched

Per-spec work is fully independent, so this is a `pipeline()` (apply → verify per spec,
no barrier). Sizing against the session's 15-agent guideline: **6 specs per wave = 12
agents**, six waves.

Suggested order — fewest sub-lists first within each tier, so failures surface cheap:

- **Wave 1** — Tier A remainder: devourer, destruction, affliction, demonology (8 agents)
- **Waves 2–6** — Tier B, 30 specs, 6 per wave, ascending **sub-list count** (the real
  difficulty sort — APL line count is misleading, see the measurement above)

### Per-spec pipeline

1. **Apply** — one agent, one spec, one file. Written brief per the template.
2. **Verify** — a *different* agent, read-only, adversarial. Checks: does any claim
   contradict `simc-apl.md`? Does the file restate the list anywhere? Is every reason
   sourced or marked inference? Does it satisfy `writing-claims.md`? Reports failures
   only, makes no edits.

### Gates, once per wave

```bash
uv run python -m wowkb.kblint
uv run python -m wowkb.simc --kb --check     # drift + augment-pin staleness
uv run python -m wowkb.kbpass check
uv run python -m wowkb.gen_verify --check
```

### Review

`git diff` per wave, read by a human (or by me, not by the agents' summaries). The Havoc
pilot's apply agent reported all ten corrections clean; the adversarial verifier found
three real defects it had missed, including the referencing violation. **The verify step
is not optional and must not be merged into the apply agent.**

## Cost

The Havoc pilot cost ~233k subagent tokens for 3 agents on a 35-action APL. 35 specs at
2 agents each, with APLs averaging ~4× Havoc's, is a large multiple of that. Worth
knowing before starting; worth splitting across sessions.

## Open decisions

1. **Does the banner come off `rotation.md` per spec?** It is shared boilerplate across
   three files. Removing it from a converted `rotation.md` is correct — that file *has*
   now been read against 12.1 — but leaves `abilities.md`/`builds.md` carrying a banner
   that says "this directory was not re-verified", which becomes partly false.
   Alternative: reword the banner in place to scope it to the two files that remain
   unverified.
2. **How far does Tier B go?** Converting the shape is cheap; genuinely re-verifying a
   12.0.7 rotation against 12.1 is the expensive half. A middle option: convert the
   shape, correct only what the APL directly contradicts, and leave the banner on for a
   later content pass.
3. **Does the "Why each rung is there" section scale?** Wave 0 answers this. If a
   203-action APL needs one bullet per rung, the section becomes a transcription by
   another name and the structure needs a phase-grouped variant.

## Milestone log

- **2026-08-17** — Tooling landed: `wowkb.simc --kb` generates `simc-apl.md` for 36 of
  40 specs (`2ea0f6d`); pass ledger + `wowkb.kbpass` (`561ebb0`); `simc-apl.md` added to
  the 30 banner'd specs' banners (`d4fdeb6`).
- **2026-08-17** — **Pilot: Havoc converted**, 386 → 171 lines (`55a9081`). Ten claims
  corrected against the 12.1 APL. Adversarial verifier caught three defects the apply
  agent's own report called clean — referencing violated 7×, a mechanic misattributed
  (Demonic Intensity vs Violent Transformation), and a talent-gated rule stated flat in
  the lede.

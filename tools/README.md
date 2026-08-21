# `wowkb` toolkit — detailed command reference

Run these from `tools/`; they need a `.env` at the repo root (see `.env.example`).
This file is the **detailed reference**; the project `CLAUDE.md` carries the one-line
index plus the cross-cutting doctrine (staleness, provenance, front matter). Run
`<cmd> --help` for exact flags.

## Command index

### Research & fetch
- `wowkb.youtube` — pull a video transcript or list a channel's videos into `raw/`.
- `wowkb.blizzard` — Blizzard API reads (token price, item/spell/journal/realms, raw `get`).
- `wowkb.wcl` — Warcraft Logs rankings and per-fight cast lists.
- `wowkb.wago` — dump a wago.tools DB2 table into `raw/wago/`.
- `wowkb.fetch` — fetch a URL to `raw/pages/`.
- `wowkb.maxroll` — a maxroll.gg guide to markdown (`--kb` lands it verbatim in the KB).

### APLs
- `wowkb.simc` — fetch the upstream SimC MID1 APL (profile or module source) to `raw/`.
- `wowkb.simc --kb` — the KB door for APLs: write the priority list as a citable artifact.

### Sim harness
- `wowkb.sim` — the local SimulationCraft harness (import/check/compare/gear/crests/log).

### Character & planner
- `wowkb.character` — one-shot per-character snapshot (unions all 3 sources).
- `wowkb.plan` — ranked session shortlist and per-slot gearing chart.
- `wowkb.charstate` — the single loader that unions PlannerState + Blizzard API + Syndicator.

### KB generation & maintenance
- `wowkb.gen_addon_quests` — regen the addon quest-ID table from `repeatables.json`.
- `wowkb.gen_candidates` — regen `planning/candidates.json` from `activities/*.md`.
- `wowkb.gen_verify` — regen `_meta/verify-in-game.md` from `@verify-ingame` markers.
- `wowkb.kbpass` — pass identity for maintenance runs (mint / stamp / check IDs).
- `wowkb.kblint` — the 6 KB current-state / evidence-class gates.
- `wowkb.spec_inventory` — per-spec ability inventory as a union.

### Addon-dev & art
- `wowkb.uiart` — Blizzard UI art as image files (atlas / icon / manifest).
- `wowkb.capart` — assemble combat-assist's per-spec HTML previews from the docs.
- `wowkb.serve` — stdlib static server + mtime watcher + live reload.

### Addons & captures
- `wowkb.addon` — the one door for the 4 gitignored sub-repo addons (list/pull/check/release/deploy).
- `wowkb.cdmp` — Cooldown-HUD flight acceptance report + pipeline decision log.
- `wowkb.capture` — THE ONE READER for addon captures.
- `wowkb.lab` — the ClientLab addon-dev lab (deploy/show/drain/blocked).
- `wowkb.obs` — the addon-dev observations queue + its drain.

---

## Research & fetch

### `uv run python -m wowkb.youtube transcript <url>`
→ `raw/youtube/<id>.md`

### `uv run python -m wowkb.youtube channel <url> --limit 10`

### `uv run python -m wowkb.blizzard token-price`
Also: item/spell/journal-*/realms/get.

### `uv run python -m wowkb.wcl rankings <encounter-id> --class Warlock --spec Affliction`

### `uv run python -m wowkb.wcl casts <report-code> --fight <id>`

### `uv run python -m wowkb.wago <Db2Table> [--build 12.0.5.xxxxx]`
→ `raw/wago/`

### `uv run python -m wowkb.fetch <url>`
→ `raw/pages/`

### `uv run python -m wowkb.maxroll <url> [--kb]`
maxroll.gg guide → markdown (`--kb`: verbatim into `knowledge/classes/<class>/<spec>/maxroll-<type>.md`; else `raw/maxroll/`).

> Blizzard + WCL commands require credentials in `.env` (user-registered).

## APLs

### `uv run python -m wowkb.simc <class> <spec> [--variant Name] [--module] [--list] [--no-sha]`
simc MID1 default APL (Tier 1) → `raw/simc/<file>.simc` + `.digest.md` (talents hash + grouped actions.*, pinned to a commit SHA+date). The reproducible source the rotation.md files distill. ⚠ **It now REFUSES a stale profile** — exit 3 plus a banner in the digest when the pinned commit predates `game-version.md`'s live-patch date, because upstream regenerates profiles PER SPEC and sometimes never gets to one: measured 2026-08-16, every Warlock MID1 profile carried a 12.1 launch-day commit while Havoc's was still 2026-03-13, **151 days stale**, and had been cited as current. The newest file that exists is not the same as a current one. `--module` is the fallback: it fetches the APL SOURCE the profiles are generated from (`engine/class_modules/apl/apl_<class>.cpp`, the `//<spec>_apl_start` block) and unwraps it back into plain `actions.*` lines, so a spec whose profile has lagged still has a Tier-1 12.1 list. It carries no talents hash or consumables — those exist only in a profile. `--module` now exits 3 on a stale SOURCE too, matching the profile path.

### `uv run python -m wowkb.simc --kb [--all|<class> [<spec>]] [--check]`
**the KB door for APLs.** Writes `knowledge/classes/<class>/<spec>/simc-apl.md` — the priority list as a GENERATED, citable artifact. This exists because `raw/` is gitignored and uncitable, so a rotation.md could never point at a fetched APL and had to hand-copy the list — and a hand-copied list drifts (measured 2026-08-17: Havoc's rotation.md quoted `use_blade_dance` / `eb_aligned`, APL variables the 12.1 rewrite deleted outright). **`rotation.md` augments `simc-apl.md`; it does not restate it.** `--check` is the CI gate: exit 1 on drift from upstream or on an APL source that predates the live patch (a pin-only change re-stamps rather than failing, so a rate-limited commits API cannot cry wolf). Covers **36 of 40 specs**; the 4 without an upstream APL are Preservation, Mistweaver, Holy Paladin and Restoration Shaman — simc does not model them, which is a known absence, not a gap to fill. Handles all five upstream layouts (`apl_<class>.cpp` markers · `<class>.cpp` for mage/warlock · `<class>/<spec>_apl.inc` for druid · `namespace <spec>` for monk · the MID1 profile as last resort for enhancement), and reads each action-list NAME from its `get_action_priority_list("…")` declaration rather than the C++ variable holding it — monk opens `pre`/`def`/`ite` for precombat/default/item_actions, so guessing mislabels every list.

## Sim harness

### `uv run python -m wowkb.sim import <export.simc|-> | check <char> | compare <char> NAME=CHANGES ... | gear <char> --slot <slot>|--all-slots | crests <char> --track <Track>|--all-tracks | log <char> --around <action>`
**the local SimulationCraft harness.** The `/simc` addon paste is the SINGLE input (equipped + bags + vault + talents + currencies + watermarks, correctly slotted with ilvls) — do not mine Syndicator or resolve slots from DBC instead; that dead-ends because bag item LEVELS exist nowhere on disk. It exists because simming Encomplete on 2026-08-20 produced FIVE wrong answers before a right one and **every error was in the hand-written harness, none in simc or the game data** — so the plumbing is owned here instead of re-improvised per question. The APL always comes from upstream unmodified (`profiles/MID2/` → `profiles/MID1/` with a loud staleness warning → the generated `knowledge/classes/<class>/<spec>/simc-apl.md` → **exit 2**; never simc's built-in APL, which is what left on-use trinkets unfired). `check` reports harness health and **deliberately no DPS** — an unvalidated number is worse than none, it gets acted on. `compare` runs every named variant as a profileset in **ONE** invocation with the baseline emitted as `_baseline` so it ranks in the same median table; medians only, `Δ% ± 95%` band, `significant`/`NOISE`, 1T/300s **and** 5T/120s by default, cells read `not simulated` never blank. It **cannot** delta across invocations — failure #4 shipped a wrong vault recommendation and is structurally prevented, not warned about. ⚠ The **FIRING GATE** is the point: an equipped or swapped-in on-use effect that never fires is invisible in simc's output, so it is asserted on (0 uses → force the slot in a throwaway probe: forced>0 = FAIL, the APL never presses it; forced=0 = WARN, simc does not model it), and a FAIL **blocks the DPS table** until you pass `--accept-failing-gate '<reason>'`, which brands every row. Variants get their own validation run because a profileset carries no buff/action counts. `gear` is local Top Gear: it enumerates the export's own bag + vault rows for a slot and ranks them as variants — so it answers "which of THESE, for THIS character", never "best in the game". Two things it owns: the **usability filter** (the addon's bag block is filtered ONLY by "has an equippable inventory type", so it carries other classes' armor — filtered here by `class_mask` then armor type, transcribed from `util.cpp`/`item.cpp`, which is also a crash guard since `player.cpp:2011` THROWS on an invalid type mid-sweep; exclusions are printed with reasons and the count prints even at ZERO, because a filter that excludes everything looks exactly like one that never ran) and the **tier-set confound** annotation (`4 → 3 pieces — this delta includes losing the 4pc`, off `item_set_bonus.inc`, so a row cannot read "this glove is bad" when it means "this glove costs you the 4pc"). Weapons are ranked under a NOT-USABILITY-CHECKED brand rather than filtered — simc holds no weapon usability data at all. `crests` answers "where do the next crests go": every remaining upgrade rank of every equipped item as one profileset in one frame, expressed as the item's own line plus `,ilevel=<target>` — simc models **no** part of the upgrade system, so the target ilvl is computed from `endgame/dawncrests.md`'s track table (1/6 and 6/6 are Tier-1; the four intermediates are interpolated and branded `~interp`). ⚠ It is the **ONE** subcommand that reads outside the export, because an item's **track and step exist nowhere in the paste and cannot be inferred from its ilvl** (292/295 is Veteran *or* Champion, 305 is Champion *or* Hero) — so track/step comes from `charstate.load()` and a slot neither the `/ps` dump nor the API resolves prints `UNRESOLVED TRACK` and is **costed at nothing**, never guessed. `import`/`check`/`compare`/`gear` stay export-only. Free-by-watermark ranks are listed separately (`dawncrests.md:215-232`, same character only; a **paired** Finger/Trinket row is read as the second-highest and every row it moves says `paired-slot rule (UNVERIFIED)`). The crest COST is **Tier-3 only** so every crest number is branded `Tier-3 est` — but because cost is uniform per rank it moves the affordable COUNT and nothing else, so the rank **ORDER is not branded** and `check_sim.py` proves it by re-running the allocator at 20 and at 10. Allocation is greedy on **marginal** Δ because ranks stack within a slot. Two more gates: **ilvl fidelity** (simc's resolved `gear.<slot>.ilevel` must equal the export's stated ilvl, or FAIL — every rank is "this item, +N ilvl") and **season drift** (an S1 Dawncrest id in the export → WARN; that silent zero is what broke `goalboard.py`). The 50% "…of the Mist" discount is **derived** from `upgrade_achievements`, never assumed, and the two things the export cannot say — the earner pays full price, the list is account-wide — are printed rather than guessed. It does **not** know about `gear`: a slot with a bag/vault candidate within 6 ilvl of what is worn prints a pointer to run `gear --slot <slot>` first. `log` is the **timeline**: ONE deterministic iteration (`iterations=1 threads=1 deterministic=1` + an explicit `--seed`, so it reproduces byte-for-byte), a windowed cast list around each cast of `--around <action>`, and an **on-use alignment readout** per window — which is the thing no aggregate can show. It reports **no DPS, no delta, no frequency** and has no `--iterations` flag; every row is branded `SINGLE SAMPLE — NOT A DPS RESULT` and the "how often" question is redirected to `check`/`compare`. The window's length comes from the anchor's OWN summon duration in the log, not a constant. ⚠ It is the only subcommand that may run a second invocation (`--variant`), because simc disables logging outright when profilesets are enabled (`sim.cpp:4361`) — safe only because no number is reported, so nothing can be deltaed across the two. Run it with no `--around` to list the action vocabulary the sample produced. This is what made the 2026-08-20 trinket disaster legible: five Tyrant windows, zero on-use presses in any of them. ⚠ **Two DECLARED exceptions to "never touch the APL"**, both per-character in `tools/wowkb/data/sim_overrides.json` and looked up automatically (`--no-overrides` to disable): `variables` re-points a variable the upstream reference **already declares** (the tool builds the line; an undeclared name is rejected), and `apl_append` appends **`use_item` rungs only**, `use_off_gcd=1` **mandatory**, via `actions+=/` so upstream's list survives underneath. Both need `why`+`measured`, both brand every row, and the firing gate still judges. They exist because upstream deadlocks on **two on-use trinkets** — its own default profile ships only one, so the case is never exercised — costing Encomplete >3%; proven not to be our harness by running the stock profile with only the two trinket lines changed. Writes only to `raw/simc-exports/` + `raw/sim-results/` (gitignored): a sim result is **evidence for an answer, not a sourced claim**, and never belongs in `knowledge/**`. ⚠ **LIVING COMMAND** — when a session gives a wrong answer the fix is a new GATE, never a hand-edited profile or APL; read `tools/docs/wowkb-sim.md`'s **Field log** before designing a comparison and append to it after

The harness normally takes a `/simc` addon paste, but `wowkb.sim import --from-api <name> [--realm <slug>]` builds the EQUIPPED-gear profile from the Blizzard profile API (equipment + summary + active talent loadout) when no addon paste is available — bags/vault are not available that way, so it does **not** serve the crest/gear-swap subcommands. `--no-overrides` on `check`/`compare` ignores the character's `sim_overrides.json` entry (runs upstream unaided).

## Character & planner

### `uv run python -m wowkb.character <name> [--realm kiljaeden] [--json]`
full char digest (unions all 3 sources; carries a "This reset" section)

**`wowkb.character`** is the one-shot snapshot for `knowledge/characters/`:
it pulls every Blizzard profile endpoint (summary/equipment/specs/professions/
reputations/raids/keystone+season) AND currencies — the profile API does *not*
expose currencies, so it reads them from the **Syndicator** addon's
SavedVariables on disk (`…/_retail_/WTF/Account/*/SavedVariables/Syndicator.lua`)
and resolves IDs via wago `CurrencyTypes`. Requires the WoW install reachable
(default `--wow-path` is the WSL `/mnt/c` path) and the character to have been
logged in / `/reload`ed recently. Emits **data only** — add narrative/deltas by
hand when writing the KB file. Note: **Catalyst charges = Dawnlight Manaflux**
(currency 3378 — a normal currency). **Sparks of Radiance** (232875) and **Ascendant
Voidshards** (268650) are *items* — read from **Syndicator**'s full bag+bank+warband
inventory (the same file we read for currencies), surfaced as `state["item_counts"]`
and a digest "Crafting mats" line. (So they're **not** a gap; the old "check in-game"
note was wrong. `wowkb.character --skip-if-current` short-circuits the whole pull when
the snapshot's `fetched:` is already ≥ the dump's capture date.)

### `uv run python -m wowkb.plan --minutes 60 [--mood efficiency|fun] [--include-repeatables]`
ranked session shortlist

### `uv run python -m wowkb.plan --gear --character <name>`
per-slot gearing chart (cache/crest targets + accolade heuristic)

### `wowkb.charstate` — three sources, one loader

**Three sources, one loader.** `wowkb.charstate.load` is the single door that
unions all character data: the **PlannerState `/ps` dump** (reset-state the API
can't see — weeklies done/not, vault progress, world-boss kills, active events —
plus an equipment/currency mirror; the **offline spine**), the **Blizzard API**
(names/specs/professions/renown/raids), and **Syndicator** (gold + currencies).
Both `wowkb.character` and `wowkb.plan` consume it; enrichment degrades silently
when offline (`--no-enrich` forces dump-only). So `wowkb.character` now also
carries a **"This reset"** section. The profile API doesn't reliably expose the
numeric upgrade track (and **drops it entirely on crafted gear**), so the **addon
dump is the primary track source** (PlannerState schema≥8 reads `track`/step off the
item tooltip; API is fallback). `wowkb.character` shows a **Track column** + a
**"…of the Dawn" discount** section (which sub-263 slots gate the 50% Champion
discount, and whether each is crestable or a crafted slot needing a recraft).
⚠ Track-aware *scoring* in `wowkb.plan` (crest-consumer costing) is still a
follow-up — the ranker's `track_caps` remains ilvl-based for now (see `_meta/kb-inbox.md`).

### Routing rule — don't reinvent the planner from the KB

**Routing rule — don't reinvent the planner from the KB.** For any "how do I
gear up / progress <char>" question, run the tools FIRST (they already union the
three sources) rather than re-deriving a per-slot chart by hand:
`wowkb.plan --gear --character <name>` (gearing chart + accolade heuristic),
`wowkb.plan --character <name>` (ranked session), `wowkb.character <name>`
(snapshot + reset-state). The **`/plan-character`** command wraps this flow.
Add warband/cross-character moves + KB colour on top; don't recompute the slots.

### Reading a character's TALENTS — use the profile API, not the loadout string

**Reading a character's TALENTS — use the profile API, not the loadout string.**
`wowkb.blizzard get /profile/wow/character/<realm>/<name>/specializations --namespace profile`
returns every saved loadout with **resolved talent names** (plus its `talent_loadout_code` and an
`is_active` flag), so there is no need to decode the export string. Decoding one *is* feasible —
`knowledge/classes/<class>/<spec>/talents.json` carries the `serial_count` + `granted_serials` +
hero-selector ordering a decoder needs — but the header layout of serialization **version 8** is
not what the pre-12.x format documents describe, so it would need confirming against the client's
`ExportUtil` first. ⚠ **Don't reach for `snakybo/TalentParser`** — evaluated 2026-08-15 and it is
not the tool for this: it converts a Classic-era `TalentExtractor.lua` dump into Lua data and does
not touch loadout strings at all. Cloned, checked, deleted.

## KB generation & maintenance

### `uv run python -m wowkb.gen_addon_quests`
regen addon quest-ID table from `repeatables.json` (then cut an addon release)

### `uv run python -m wowkb.gen_candidates`
regen `planning/candidates.json` from `activities/*.md` (`--check` in CI; edit the .md, not the JSON)

### `uv run python -m wowkb.gen_verify`
regen `_meta/verify-in-game.md` from `@verify-ingame` markers (`--check` for CI; tag the claim, not the JSON)

### `uv run python -m wowkb.kbpass current|allocate|check`
**pass identity for maintenance runs.** Every `/update` run mints an ID (`<date>.<n>`, never reused) recorded in `_meta/feed-watermark.md`'s pass ledger; every GENERATED artifact stamps that ID in its front matter. `check` compares them and exits 1 on any artifact behind the active pass — which catches the one failure a log cannot: a pass that claims to have regenerated something and didn't (the `spec_inventory.PINNED_BUILD` defect the 12.1 sweep found by hand). A no-op regeneration still RE-STAMPS, same rule `reviewed:` follows. Hand-written files are deliberately NOT stamped — they keep `reviewed:` as a parseable date; the residual limit is that two passes on the SAME DAY over overlapping scopes are indistinguishable to `grep -rL 'reviewed: <date>'`, and `allocate` warns when it mints a second ID for a day.

### `uv run python -m wowkb.kblint`
the 6 KB gates: 1-3 + 6 = README §7's current-state rule, 4-5 = §0's evidence classes. **1, 3 and 6 are KB-WIDE** (`--all`); 2, 4 and 5 stay scoped to knowledge/addon-dev, whose evidence classes are stricter — gate 2 would fire on every legitimate game date in the gameplay KB. Gate 6 = no correction in the LEDE (the text above the first `##`, which is what a reader who stops after the first screen sees) — scoped to retrospective prose only, so a lede warning about the CURRENT state is fine. Gate 4 = no negative existential ("there is no way to…") in a claim unit tagged [client] — a negative takes [searched YYYY-MM-DD: <instruments>], which names where we looked. Gate 5 = no claim citing OBS-nnn / projects/** / a capture path / one of OUR addons in any of its three names: repo (CDMProbe), slash command (/cdmp, /clab, /bb, /ps, /cap) or capture reader (wowkb.capture/.cdmp/.lab/.obs/.addon/.diagnostics) — but NOT wowkb.uiapi/.wiki/.wago, which reach admissible sources. `--gate N` for one; exit 1 on any hit

### `uv run python -m wowkb.spec_inventory [--spec X] [--unseeded] [--json PATH] [--validate CHAR]`
per-spec ability inventory as a UNION: all-talents.tsv (node_type!=PASSIVE) ∪ SkillLineAbility class kit ∪ CooldownSetSpell residue (cdm-only), annotated with cooldown, Blizz category, origin (class-baseline|talent-active|talent-choice|cdm-only), suggestedMode (fixed|float), talent tree/hero placement, and the seed bucket that binds each name. Tier 1, all 40 specs. `--validate <char>` diffs the union against a real in-game `/bb diagnostics` dump (false-negatives = holes). Feeds the BucketBinds floats work (layout-v2 §6).

## Addon-dev & art

### `uv run python -m wowkb.uiart find|atlas|icon|manifest`
Blizzard UI art as image files: atlas member → sheet FileDataID (wago.tools/atlas) → CASC bytes → BLP decode → the member's crop, + flipbook grid/CSS recipe and a TINTABILITY measure (mean saturation; SetVertexColor multiplies, so baked-hue art can't carry our hues). `icon` pulls 56px spell icons. Feeds combat-assist's render-shelf.md and its previews (data URIs — a preview renders from the file alone; no CDN)

### `uv run python -m wowkb.capart tokens|assets|import|build|export|check`
assemble combat-assist's per-spec HTML previews from the docs that own them. It holds NO color, rate or size: every number comes from render-shelf.md Part 6's `render-tokens` block, every ability/lane/verdict from havoc/catalog.md + scenarios.md. `build` is deliberately ungated except for the TINT GUARD (`assert_tintable` — art declared `tint: "lane"` must MEASURE neutral, the check that stops the preview showing a recolor SetVertexColor cannot do; it is art-agnostic and moved from the retired flipbook rings onto the badge sprites) and the closed verdict/cue/roster vocabulary; `check` is the CI-shaped gate (doc↔sidecar, HTML staleness, no literal hex in the template, the tint guard still has a subject, and the ELIMINATION GATE — for every scenario the leftmost entry that is neither swiped nor wearing a NEGATIVE badge must be the one the doc calls the press, which is what makes the mostly-negative cue vocabulary safe; the veil was retired 2026-08-16 and the gate is now two-term, which is also the proof the veil carried no information). The cue vocabulary is negative BY DEFAULT with exactly ONE positive cue (`capped`, impending loss); three further `check` gates fence it — a second `polarity: "positive"` fails, so does any declared cue that no scenario wears, and so does a positive cue outside badge slot 3 (or a negative one in it). ⚠ That one-positive rule is under review and reads as a budget it was never meant to be — `specs/backlog.md` → *"There is no positive-cue budget"*. `export [lua|badges|ring|hatch|lab|all]` writes the SAME tokens into the addon — `CombatAssistPlus/Style.lua` (Part 6 as a Lua table, data only; `Treatment.lua`/`Paint.lua` are the logic that reads it), the badge art as 32-bit TGA under `Media/badges/`, the lane border's arrival flipbook as `Media/ring.tga` (one white-alpha sheet, frames × `motion.tick_s` == `arrival.duration_s`, gated), V11's cooldown-hatch sheet as `Media/stripes.tga` (byte-gated the same way; the `/cap style` gallery borrows this one file rather than keeping a copy), and `Lab.lua` (`ns.LabStyle`) plus `Media/lab/` for Part 7, which only the `/cap style` gallery may read and `check`'s REACH GATE keeps out of the live overlay — and `check` gates the committed Lua against the shelf exactly as it gates the HTML, so the preview and the addon cannot drift. Change the look by editing the shelf, not this

### `uv run python -m wowkb.serve <dir> [--watch PATH] [--on-change CMD] [--port N] [--no-reload]`
stdlib static server + mtime watcher + live reload. Generic, not cap-specific. The `edit → rebuild → look → tweak` loop: it injects an SSE reload script into SERVED html only, never into the file, so the committed preview stays clean. Pair with capart:

```bash
uv run python -m wowkb.serve ../projects/combat-assist/previews --watch ../projects/combat-assist/specs --on-change "python -m wowkb.capart build --all"
```

## Addons & captures

### `uv run python -m wowkb.addon list`
the 4 sub-repo addons: presence + local HEAD + .toc version + latest release + drift

### `uv run python -m wowkb.addon pull [--all|bb cdmp ps cap]`
clone-if-missing + git pull each sub-repo (the machine-B sync)

### `uv run python -m wowkb.addon check`
report addons with local-only (uncommitted/unpushed) work; exit 1 if any (pre-push gate)

### `uv run python -m wowkb.addon release <bb|cdmp|ps|cap> [--patch|--minor|--major] [--notes …]`
bump .toc → luaparser check → commit → push → gh release (tag=version) → ghaddons deploy

### `uv run python -m wowkb.addon deploy <bb|cdmp|ps|cap>`
redeploy the latest existing release via ghaddons (no new cut)

**`wowkb.addon`** is the one door for the four gitignored **sub-repo addons**
(`bb` = BucketBinds · `cdmp` = CDMProbe · `ps` = PlannerState · `cap` = Combat
Assist Plus — short name =
in-game slash prefix; a checkout path also resolves). The registry inside the
module (repo ↔ path ↔ `.toc`) is the source of truth for the addon set, and it
owns the mechanical release recipe the per-addon `CLAUDE.md` files used to spell
out by hand (they keep the *why*; this owns the *how*).
- **`list` is the live version signal — never hardcode an addon's current version
  in prose, run it.** It shows presence + local HEAD + `.toc` version + latest
  GitHub release + drift (unreleased commits / behind-release / dirty tree).
- **`pull` closes the machine-B gap.** These are separate repos gitignored here,
  so a `git pull` of *this* repo never fetches them — a fresh machine gets new
  docs describing addon code it doesn't have. **On a fresh checkout / before
  touching an addon, run `wowkb.addon pull --all`** (clone-if-missing + `git pull`
  each). Since this file loads every session, that's the standing reminder.
  - ⚠ **AND THE SAME GAP EXISTS BETWEEN WORKTREES ON ONE MACHINE** — the docs used
    to frame this as a cross-*machine* problem only, which is half the story.
    `wow`, `hud-classes` and `wwt-keyboard` are git **worktrees of the same repo**,
    but because the addons are gitignored **each worktree carries its own
    independent full clone** of `michac/CDMProbe` (and of BucketBinds/PlannerState).
    Three clones, one GitHub remote, no shared refs — so a release cut in one
    worktree leaves the others silently behind, on the same machine, with no `git`
    signal anywhere in the parent repo.
  - **What that actually breaks (measured 2026-08-03):** the stale worktree's
    `.toc` is behind, so `wowkb.addon release` there bumps into a version number
    **that already exists as a tag** and the push fails. That is the *good* failure
    — loud, and mid-release rather than silent — but it costs a rebase to unpick.
    **So: `wowkb.addon pull` in a worktree you have not released from lately, before
    you cut anything.** `wowkb.addon list`'s `drift` column is the cheap check — it
    diffs the LOCAL `.toc` against the latest GitHub release, so a stale worktree
    reads **`BEHIND release — pull`** instead of `in sync`. ⚠ And it is genuinely
    per-worktree: the registry resolves its paths from the *running tools'* repo
    root (`addon.py`'s `REPO = Path(__file__).parents[2]`), so `wowkb.addon list`
    always reports the clone belonging to the worktree you ran it from — which is
    exactly the one you are about to release.
  - **Nothing is ever lost by this** — every clone points at the same remote, so a
    behind worktree is a plain fast-forward (`git -C <path> merge --ff-only
    origin/main` after a fetch). It only diverges if you cut releases from two
    worktrees without pulling, and even then the tag collision stops you first.
- **`check` is the pre-push gate** (see the Git-workflow note): reports any addon
  with local-only work (uncommitted or unpushed), exits 1 if so. Run it when you
  push this repo — pushing here means I want the addon code on GitHub too.
- **`release`** runs the whole publish flow one-shot: refuses a dirty tree (commit
  your feature work first), bumps the `.toc` version (`--patch` default), warns if
  `## Interface:` drifts from `game-version.md`, luaparser-checks the Lua, commits
  the bump, pushes, cuts a GitHub release whose **tag = `.toc` version**, then
  `ghaddons`-deploys into the game install and reads back `ok`. For `ps` it also
  warns to bump the Lua `schema` field by hand if the `/ps` dump format changed
  (it does **not** touch schema). `--dry-run` stops before the commit.

### `uv run python -m wowkb.cdmp flight`
the PASS/FAIL ACCEPTANCE REPORT for an in-game pass recorded by `/cdmp flight` (run this after a test build)

**`wowkb.cdmp flight`** is the door for **verifying a Cooldown-HUD test build in game**, and
it exists because that used to be a checklist of ~10 slash commands, several of them typed
mid-pull, whose answers a human eyeballed. Now: `/cdmp flight` in game arms a recorder (it
samples coverage / assist / capability / layout on every *change of answer*, through combat
entry and spec + hero swaps, with **no further typing**), you play, you `/reload`, and this
prints a **PASS / FAIL / MEASURED** report judged against criteria that live in code. Exit
**2** = no failures but part of it was never flown — a criterion nobody exercised must never
read as a pass. ⚠ SavedVariables only flush on **`/reload`**.

### `uv run python -m wowkb.cdmp decisionlog`
extract the CDMProbe pipeline DECISION LOG off SavedVariables → flat .log

**`wowkb.cdmp decisionlog`** also prints a **COMBAT SPLIT** (v0.32.75+): `w:-` (the Coach
found no winner) is only meaningful **in a pull** — out of combat "no winner" is the correct
answer, so idle time inflates the raw ratio. The addon stamps `# combat start`/`# combat end`
on the edge and this reports the in-combat ratio off it. ⚠ A capture recorded **before** that
marker shipped is reported **UNREADABLE, never 0 %**: entries are stored pre-rendered, so
combat cannot be recovered retroactively — you have to re-fly.

**`wowkb.cdmp decisionlog`** extracts the Cooldown HUD's **pipeline decision log**
off SavedVariables (newest `WTF/Account/*/SavedVariables/CDMProbe.lua`,
`CDMProbeDB.decisionlog`) and flattens it to a grep-friendly `.log` — a ring of the
last 3 sessions, one `S{…} G{…} B{…}` line per pipeline decision change, the
instrument for "why does `/cdmp hud` show nothing here?". ⚠ SavedVariables only flush on **`/reload`**. *(The old `/cdmp probe` +
`probe-baseline.json` assertion suite was retired 2026-07-29 — the readability rules it
discovered are settled game-wide, and a spec's tracked set comes from wago DB2 via
`wowkb.spec_inventory`, so per-spec re-measurement bought nothing.)*

### `uv run python -m wowkb.capture <bb|cap|cdmp|clab|ps> [stream]`
THE ONE READER for addon captures — `<DB>.captures.<stream>` → greppable .log (`--list` for streams + bounds)

**`wowkb.capture` is the one door for getting data out of an addon.** Every recorder in
every addon writes to a single SavedVariables key with one shape
(`<AddonDB>.captures.<stream>`), and this is the only thing that reads it — which is the
enforcement: an addon that writes the wrong shape fails here, loudly, the first time
anyone reads a capture. Graders stay per-addon (`wowkb.cdmp flight`) and consume
`capture.load()` rather than globbing a path. The contract, the Lua-side `Capture.lua` /
`DumpPanel.lua` interfaces and the dump-panel design live in
`.claude/skills/wow-developer/references/capture-and-dump-standard.md`.
⚠ SavedVariables only flush on `/reload` or logout.

### `uv run python -m wowkb.lab [deploy|show|drain|blocked]`
the ClientLab addon-dev lab: deploy the scratch addon (a directory copy + the id ⇄ ns.Test{} cross-check), read a run (`show` = result BESIDE expect, never a verdict), drain an answer into the KB. `blocked` = the untested rows, grouped by the capability each waits on. ⚠ An UNKNOWN is not filed here — it is a marker on the claim in knowledge/addon-dev/ (projects/addon-lab/docs/lab-process.md)

### `uv run python -m wowkb.obs [list|check|drain OBS-nnn]`
the addon-dev observations queue + its drain; `check` gates a --minor/--major release

## Notes

- Blizzard + WCL commands require credentials in `.env` (user-registered).
- ⚠ git-bash mangles leading-slash args (`/data/...` →
  `C:/Program Files/Git/data/...`). Prefix `wowkb.blizzard get` calls with
  `MSYS_NO_PATHCONV=1`.

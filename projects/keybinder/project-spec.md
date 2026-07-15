# BucketBinds — a one-shot keybind/bar dumper for WoW

**Status: M3 shipped (spillover, v0.3.0) on top of M2 (dumper) + M1
(snapshot/restore). Seed is now JSON-authoritative (xlsx frozen to archive), bars
re-laid-out to a modifier-grouped 12-slot scheme, and `/bb dump --nobind` +
`/bb test` added. M4 (in-addon tweak UI) is next. 2026-07-14.**

A self-contained WoW addon that does two things the game won't:

1. **Ability dump** — given your class+spec, place every ability/item into a
   fixed **bucket → action-slot** layout and set the keybinds in one shot, then
   get out of your way. No background daemon, no continuous re-sync. Dump once,
   tweak by hand, done.
2. **Transactional save/restore** — snapshot your entire keybind + action-bar +
   macro state to a named profile and restore it atomically (with a pre-restore
   backup). The game has binding *sets* and Edit Mode *layouts* but no
   snapshot/rollback of "this whole arrangement." This fills that gap.

Everything happens **inside the addon** — no external web tool. (Decision:
2026-07-10.) The seed data ships baked into the addon as a Lua table.

## Origin

Concept lifted from Bellular's "Ultimate Midnight Keybinding System"
([video](https://www.youtube.com/watch?v=PohMTq87jds)). We take their two good
ideas — (a) sort every ability into a **category/bucket**, (b) bind the same
category to the same key on **every spec** — and drop what we didn't want: a
live-maintained web tool and an addon that wants to run/re-sync continuously.

## The core insight (why "same key across all specs" works)

WoW keys bind to **action-bar slots** (`ACTIONBUTTON1`, `MULTIACTIONBAR…`), not
to spells. So "V always interrupts" really means:

> bind the key→slot layer **once** (stable, rarely touched), then for each spec
> place *that spec's* interrupt into the slot `V` fires.

The dump is therefore two independent layers:

- **Key→slot layer** — a stable table `(bar, slot) → keybind`. Set once.
- **Spec→slot layer** — the classification `(spec, bucket) → ability`, placed
  into the slot that bucket owns.

The Bellular spreadsheet turned out to encode exactly this (its "Master Sheet"
is literally `Bar | Slot | Keybind | Category | <ability per spec>`), which
validated the model and handed us the whole classification as a seed.

## The layout (decoded from the seed)

**Re-layout 2026-07-14: one modifier layer per physical bar, 12 slots each.**
Each stock MultiBar has 12 buttons; the seed now fills all 12 rather than 8, so
the four modifier layers pack onto four bars and **bar 5 is freed**:

| Bar (modifier) | Slots 1–8            | Slots 9–12         | Buckets                                     |
|----------------|----------------------|--------------------|---------------------------------------------|
| 1 unmod        | `1 2 3 4 Q E R F`    | `Z X C V`          | Combat 1–8 + Def1/Move/CC/Interrupt         |
| 2 Shift        | `S1..S4 SQ SE SR SF` | `SZ SX SC SV`      | Combat 9–12, Class 1–4 + Def2/Move2/CC2/Slow|
| 3 Ctrl         | `C1..C4 CQ CE CR CF` | `CZ CX CC CV`      | Self-heals, purge/dispel/raid-def/lust + buff/res/immune/taunt |
| 4 Alt          | `A1..A4 AQ AE AR AF` | `AZ AX AC AV`      | item/trinket/racial macros (M5) + PvP 1–3, Mount |
| 5              | —                    | —                  | **free** (available for a compact/overflow layout) |

Consequences: the singles (`Z X C V` + Shift/Ctrl variants) join their modifier's
bar instead of being scattered, and the bar-1 form-mirror now covers all 12 unmod
slots (druids/rogues get interrupt + defensives on their form bars too).

Out-of-combat sprawl (mounts/toys/teleports/buffs/specs) is **not** bound to
keys — it goes on OPie rings. The addon marks those buckets "on a ring" and
skips them. The OPie master-ring import string is a separate, untouched asset
([pastebin](https://pastebin.com/bG3zMdT7)).

## Data pipeline

```
data/bellular-keybinds.seed.json   CANONICAL, hand-edited source of truth
  └─ tool/gen_data_lua.py          (the one live-workflow step)
       └─ addon/BucketBinds/Data.lua   generated; the addon loads this (never hand-edit)
```

The **JSON is authoritative** — it carries the Tier-A/B ability corrections and
the modifier-grouped re-layout the workbook never had. Edit the JSON, run
`gen_data_lua.py` (which also has `--check` for CI), diff, ship. `Data.lua` is a
generated build artifact.

The Bellular **.xlsx is a frozen archive**, no longer in the workflow.
`tool/extract_seed.py` still exists but only to *re-derive* the seed from the
workbook for reference — it writes a **side file**
(`data/bellular-keybinds.archive-import.json`, gitignored) and does **not** touch
the canonical seed or `Data.lua`. Diff it by hand if Bellular ever ships a sheet
worth comparing. Current seed: **52 buckets (48 placed + 4 stance), 40 specs,
1538 ability mappings**, plus item-ID and buff reference tables.

## Milestones

- [x] **M0 — seed + skeleton.** Extract workbook → seed.json + Data.lua; project
      home under `projects/keybinder/`; this doc.
- [x] **M1 — snapshot/restore.** Read current bindings (`GetBinding` /
      `GetCurrentBindingSet`), every action slot (`GetActionInfo` incl.
      bonus/stance/dragonriding bars), and macro bodies → serialize to a named
      SavedVariables profile. Restore = back up current, then re-apply
      atomically, combat-guarded. **Ship this first** — it's taxonomy-independent
      and de-risks the write-bars plumbing everything else needs.
      *Shipped v0.1.0: `Snapshot.lua` (`Capture`/`Apply`) + `/bb
      save|restore|undo|list|delete` + combat-defer queue.*
- [x] **M2 — dumper.** Given class+spec, walk the seed's 40 placeable spell
      buckets, resolve each ability name→spellID at runtime, place it on the
      fixed `(bar, slot)` action slot, mirror the main bar onto form/stance
      bonus bars, and set the key→slot bind — one shot, combat-gated, with an
      auto-backup so `/bb undo` reverts it. The 12 `bar=None` buckets
      (consumable/trinket/racial macros + Stance/Free) are reported as
      `skipped (M5)`, never silently dropped.
      *Shipped v0.2.0: `Dump.lua` (`ResolveSpec`/`Resolve`/`Run`, runtime
      `resolveSpellID` + spellbook fallback + alias layer, `BAR_MAP`,
      `FORM_BONUS_BARS` + self-healing `UPDATE_SHAPESHIFT_FORM` hook) + `/bb
      dump [<Spec>|<Class> <Spec>]` + generalized combat-defer thunk queue
      (`ns.QueueAction`). Dev-side `tool/check_seed_spells.py` cross-checks every
      seed ability name against a wago `SpellName` dump (caught the
      `Efflorescence?` sheet typo → aliased).*
- [x] **M3 — spillover: surface every unmapped ability.** After a dump, enumerate
      the character's full active spellbook (General + class + active-spec skill
      lines), subtract what's already on a bar (**override-normalized** via
      `FindBaseSpellByID`, so a placed base and its talented replacement count as
      one), drop passives / `FutureSpell` / `Flyout` / `PetAction`, and place the
      remainder onto a reserved free-slot region with a log of each `name (spellID)`.
      No keybinds — the value is *visibility*. Triple payoff: (a) **live QA of the
      seed** — an important ability landing in spillover is a seed miss; (b) surfaces
      useful-but-non-rotational utility the buckets don't cover; (c) **subsumes
      hand-encoding build-specific abilities** — spillover catches
      `Tempest`/`Reaver's Glaive`/etc. per-character, so the seed stays
      build-agnostic. Combat-guarded; caps the region and reports overflow (listed,
      never dropped). Natural precursor to M4 (its bar is the tweak palette).
      *Shipped v0.3.0: `Dump.Spill` (`enumerateCastable` + `placedSpellSet` +
      `normID` override-collapse) + `/bb spill [clear]`. Reserve region = Action
      Bars 6–7, abs slots **145–168** (flagged `@verify-ingame` — the 133–180 range
      shifted across expansions; placement is empty-slots-only so a wrong base can't
      clobber real bars). Tracks the slots it filled in `BucketBindsDB.spillSlots`
      so re-runs are idempotent and never wipe abilities the player parked there.
      Also v0.3.0: JSON-authoritative pipeline, modifier-grouped 12-slot re-layout,
      `/bb dump --nobind` (place without rebinding), and `/bb test` (Recuperate →
      ALT-0 place+bind smoke test, `test clear` to revert).*
- [ ] **M4 — in-addon tweak UI.** Pick spec → dump → drag abilities between
      slots → save as profile. This is the "then tweak" half of the promise; the
      M3 spillover bar is its natural palette — drag the keepers into place.
- [ ] **M5 — items/macros.** Auto-generate potion/trinket/racial/@cursor macros
      from the Items table; respect the macro caps.

## M1 plan — snapshot / restore (target release v0.1.0)

Capture the full keybind + action-bar + macro state to a named profile and
restore it safely with an auto-backup. Taxonomy-independent; also builds the
write-bars plumbing M2 needs.

### Three subsystems

| Layer | Read | Write | Note |
|---|---|---|---|
| Keybindings | `GetNumBindings()`/`GetBinding(i)` → key→command; `GetCurrentBindingSet()` (account/char) | `SetBinding` → `SaveBindings(set)` | must `SaveBindings` or lost on relog |
| Action slots | `GetActionInfo(slot)` for **slots 1–180** → `{type,id}` | pickup (`C_Spell.PickupSpell`/item/macro) → `PlaceAction(slot)` | protected in combat; 1–180 already covers stance/skyriding bars |
| Macros | `GetNumMacros()`, `GetMacroInfo(i)` → name/icon/body/scope | `CreateMacro`/`EditMacro` | index unstable → slots reference macros **by name** |

### Restore ordering (safe, not truly atomic)

1. **Combat guard** — `InCombatLockdown()` → refuse + queue to `PLAYER_REGEN_ENABLED`.
2. **Auto-backup** current state into a single `__prerestore` slot → `/bb undo`
   (single level; no undo stack).
3. Apply in dependency order: **macros first** (build name→index map) →
   **action slots** (resolve macro slots via map; skip unknown spells) →
   **bindings** (apply map, then `SaveBindings`).
4. **Report** counts + anything skipped; never fail silently.

### Settled decisions

- **Bindings = exact mirror** (clear all, apply saved). **Macros = additive**
  (create/update saved; don't delete the user's other macros) with an opt-in
  `exact` mode.
- **Stance/skyriding bars**: captured by full 1–180 enumeration — no deferral,
  no shapeshifting. (Per-form *targeting* is M2, see risks.)
- **`/bb undo`**: single-level restore of `__prerestore`.

### Files (in the michac/BucketBinds repo)

- `Snapshot.lua` (new) — `Capture()→table`, `Apply(profile,opts)`; split
  `{capture,apply}{Bindings,Actions,Macros}`; combat queue.
- `Core.lua` — add `/bb save|restore|list|delete|undo`.
- `BucketBinds.toc` — load `Snapshot.lua` before `Core.lua`; bump `## Version: 0.1.0`.

### SavedVariables shape

```lua
profiles["<name>"] = {
  meta     = { created, char="Name-Realm", class, specID, bindingSet=1|2 },
  bindings = { {key="SHIFT-1", command="ACTIONBUTTON9"}, ... },
  actions  = { [slot] = {type="spell|item|macro|mount|...", id=, name=, body=, icon=} },
  macros   = { {name, body, icon, scope="account|char"}, ... },
}
-- plus BucketBindsDB.autobackup = <the __prerestore snapshot>
```

### Verification

luaparser syntax gate + an in-game smoke protocol (documented in the addon's
`CLAUDE.md`): save → rebind a key & move an action → restore → confirm revert;
`/bb undo`; combat-lockdown deferral; Druid Cat/Bear bar round-trip.

## Open technical questions / risks

- **Spell-ID resolution (the one real engineering piece).** The seed carries
  ability *names*, `PlaceAction` needs the spellbook entry. Resolve name→ID at
  apply-time from the player's spellbook; cross-check offline against wago DB2
  (this repo already pulls wago). Names drift with patches — needs a fuzzy/alias
  fallback and a "couldn't place N abilities" report rather than silent gaps.
- **Combat lockdown.** Can't change bindings or move actions in combat. Guard
  everything behind `InCombatLockdown()`; queue to `PLAYER_REGEN_ENABLED`.
- **Macro caps.** 120 account + 18 per-char. Auto-generated @cursor/item macros
  eat into this — M2/M5 need a budget and a graceful "out of macro slots" path.
- **Bonus-bar slot numbering.** Druid forms / Rogue stealth / Warrior stances /
  skyriding page the *visible* bar to a bonus bar — but the underlying slots are
  fixed absolute IDs, so `GetActionInfo`/`PlaceAction` reach them regardless of
  current form (you can write the Cat bar while in Bear form). The bonus bars sit
  at computable ranges:

  ```
  firstSlot = 1 + (NUM_ACTIONBAR_PAGES + bonusOffset − 1) × 12   -- pages=6, buttons=12
    offset 1 → 73–84    offset 2 → 85–96    offset 3 → 97–108
    offset 4 → 109–120  offset 5 → 121–132 (skyriding)
  ```

  Consequence: **M1 capture is complete by enumerating slots 1–180** — form bars
  come along for free, no shapeshifting needed. What's genuinely fiddly is
  *labeling*: which `bonusOffset` each form/stance/stealth uses is a per-class
  table the API doesn't hand you by name, and some forms re-page the base bar
  instead of taking a bonus bar. That table is load-bearing for **M2** (a Feral's
  abilities must land on the Cat slots or they won't show in Cat form) — it's a
  bounded, formula-backed chunk of the dumper, **not** an M1 concern.
  Refs: [Wowpedia API_GetBonusBarOffset](https://wowpedia.fandom.com/wiki/API_GetBonusBarOffset).
- **Bar addon assumptions — DECIDED (2026-07-10): direct modifier binds on
  all-visible stock bars, no paging.** The seed stores an explicit keybind string
  per `(bar, slot)` (`1`, `S1`=Shift+1, `C1`=Ctrl+1…), so each combo maps **1:1**
  to one fixed absolute action slot via `SetBinding(key, <SLOT_COMMAND>)` — no
  paging addon, nothing hidden, every bar clickable and showing its own cooldown
  swipe. Rationale: placement (where an ability lives / whether it's visible) is
  independent of binding (what key fires it); paging bundles them only by
  convention. Modifier paging's *only* wins are screen-declutter and stock-bar
  setup speed — but it costs click-ability and at-a-glance cooldowns, and the
  seed already carries per-combo keys that direct binding consumes WYSIWYG (every
  combo always points at the same slot — simpler to reason about than paged
  swaps). Cooldown-tracking at the high end is done off-bar anyway (WeakAuras /
  Cooldown Manager as "front end", bars as "back end"), so hiding bars buys
  little. **Paging is a deferred opt-in "compact mode", not the M2 default.**
  Refs: [wowinterface Paging](https://www.wowinterface.com/downloads/info18229-Paging.html),
  [Blizzard: tracked bars w/o WeakAuras](https://us.forums.blizzard.com/en/wow/t/feedback-action-bars-tracked-bars-and-unit-frame-options-after-playing-without-weakauras/2203580).
- **Naming.** Addon is provisionally `BucketBinds` — easily renamed; not final.

## Layout

The seed pipeline + this doc live in **`wwt-keyboard`** (this workspace). The
**addon is its own git repo** (`michac/BucketBinds`), checked out at
`addon/` but gitignored here — mirroring how `planner-state/`
(michac/wow-planner-state) is handled. `extract_seed.py` writes the generated
`Data.lua` across that boundary into the addon repo's working tree; you then
commit + cut a **GitHub Release** there so `ghaddons` can install/update it. See
`addon/CLAUDE.md` for the release workflow (a plain push does **not** reach the
game).

```
projects/keybinder/                    ── tracked by wwt-keyboard ──
  project-spec.md                     this doc
  data/
    bellular-keybinds.seed.json       CANONICAL seed (hand-edited, diffable)
    seed-notes.md                     provenance + notation legend
  tool/
    gen_data_lua.py                   seed.json → Data.lua (the live step; writes ↓)
    extract_seed.py                   ARCHIVAL: frozen .xlsx → side file only

  addon/            ── separate repo michac/BucketBinds; gitignored here ──
    CLAUDE.md                         addon-repo instructions + release flow
    README.md
    BucketBinds/
      BucketBinds.toc
      Core.lua                        slash cmds, namespace, load
      Data.lua                        GENERATED — the seed as a Lua table
      Snapshot.lua                    (M1) save/restore
      Dump.lua                        (M2) seed → bars
```

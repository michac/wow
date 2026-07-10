# BucketBinds — a one-shot keybind/bar dumper for WoW

**Status: M0 (project stood up, seed extracted). 2026-07-10.**

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

5 action bars × 8 slots, addressed through four modifier layers:

| Layer   | Keys                     | Buckets                                   |
|---------|--------------------------|-------------------------------------------|
| unmod   | `1 2 3 4 Q E R F`        | Combat 1–8 (core rotation)                |
| Shift   | `S1..S4 SQ SE SR SF`     | Combat 9–12, Class 1–4 (move/CC/util)     |
| Ctrl    | `C1..C4 CQ CE CR CF`     | Self-heals, purge/dispel/raid-def/lust    |
| Alt     | `A1..A4 AQ AE …`         | Items, trinket, racial, PvP               |
| singles | `Z X C V` (+S/A variants)| defensives, movement, CC, interrupt, mount|

Out-of-combat sprawl (mounts/toys/teleports/buffs/specs) is **not** bound to
keys — it goes on OPie rings. The addon marks those buckets "on a ring" and
skips them. The OPie master-ring import string is a separate, untouched asset
([pastebin](https://pastebin.com/bG3zMdT7)).

## Data pipeline

```
Bellular .xlsx (Windows host / Google Sheets, volatile snapshot)
  └─ tool/extract_seed.py  (uv run --with openpyxl)
       ├─ data/bellular-keybinds.seed.json   canonical, diffable, in-repo
       └─ addon/BucketBinds/Data.lua          generated; the addon loads this
```

Refresh the sheet → re-run the extractor → diff the JSON. The JSON is the
source of truth *for the repo*; `Data.lua` is a generated build artifact (do not
hand-edit). Current seed: **52 buckets, 40 specs, 1554 ability mappings**, plus
item-ID and buff reference tables.

## Milestones

- [x] **M0 — seed + skeleton.** Extract workbook → seed.json + Data.lua; project
      home under `projects/keybinder/`; this doc.
- [ ] **M1 — snapshot/restore.** Read current bindings (`GetBinding` /
      `GetCurrentBindingSet`), every action slot (`GetActionInfo` incl.
      bonus/stance/dragonriding bars), and macro bodies → serialize to a named
      SavedVariables profile. Restore = back up current, then re-apply
      atomically, combat-guarded. **Ship this first** — it's taxonomy-independent
      and de-risks the write-bars plumbing everything else needs.
- [ ] **M2 — dumper.** Given class+spec, walk the 52 buckets, resolve each to
      `(bar, slot, keybind)`, place the ability/item/macro, set key→slot binds
      once. Skip "on a ring" buckets. Requires the spell-ID resolve (below).
- [ ] **M3 — in-addon tweak UI.** Pick spec → dump → drag abilities between
      slots → save as profile. This is the "then tweak" half of the promise.
- [ ] **M4 — items/macros.** Auto-generate potion/trinket/racial/@cursor macros
      from the Items table; respect the macro caps.

## Open technical questions / risks

- **Spell-ID resolution (the one real engineering piece).** The seed carries
  ability *names*, `PlaceAction` needs the spellbook entry. Resolve name→ID at
  apply-time from the player's spellbook; cross-check offline against wago DB2
  (this repo already pulls wago). Names drift with patches — needs a fuzzy/alias
  fallback and a "couldn't place N abilities" report rather than silent gaps.
- **Combat lockdown.** Can't change bindings or move actions in combat. Guard
  everything behind `InCombatLockdown()`; queue to `PLAYER_REGEN_ENABLED`.
- **Macro caps.** 120 account + 18 per-char. Auto-generated @cursor/item macros
  eat into this — M2/M4 need a budget and a graceful "out of macro slots" path.
- **Bonus-bar slot numbering.** Druid forms / Rogue stealth / Warrior stances /
  dragonriding remap the action bar; naive slot math breaks here. This is the
  fiddliest correctness surface — snapshot must capture it, dump must respect it.
- **Bar addon assumptions.** The 5×8 modifier-layer layout assumes paged/modified
  bars (Blizzard Edit Mode can do 8 bars; ElvUI/Bartender do modifier paging more
  cleanly). Decide whether we target stock bars, drive an addon, or document a
  required bar setup. TBD in M2.
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
    bellular-keybinds.seed.json       canonical seed (diffable)
    seed-notes.md                     provenance + notation legend
  tool/
    extract_seed.py                   xlsx → seed.json + Data.lua (writes ↓)

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

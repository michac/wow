# Seed provenance & notation

`bellular-keybinds.seed.json` is extracted from a **user copy** of Bellular's
"Midnight Keybind Planner (Oldschool Edition)" spreadsheet
([copy](https://docs.google.com/spreadsheets/d/1h9rM8K2HjYaxAj_rQ5kOBl3qH6_kN-SJ25J2cDgeG5s/edit)),
via `../tool/extract_seed.py`. The `.xlsx` snapshot lives on the Windows host
(`C:\Users\mchris\Downloads\…`) and is **not** committed — it rots as the game
changes. The JSON is the in-repo source of truth; `../addon/BucketBinds/Data.lua`
is generated from it.

## What's in it

- `buckets` (52) — `category → keybind`, plus `bar`/`slot` from the Master Sheet.
  This is the stable key→slot layer.
- `specs` (40) — `class`, `spec`, and `abilities: {category → ability name}`.
  40 = 13 classes × 3 specs, +1 (Druid has 4; Demon Hunter's third spec is the
  Midnight-new **Devourer**).
- `bonus_binds` — out-of-combat rings/buttons (OPie master ring on `T`, markers,
  ExtraActionButton, Interact `` ` ``). (Autorun on middle-mouse was removed
  2026-07-16 — the three mouse buttons are now combat binds; see below.)
- `items` — potions/flasks/oils with Q1/Q2 item IDs (for macro generation).
- `buffs` — raid/self buffs by spec.
- `exclude_spells` — noise list (`{id?, name?, why}`) that both `/bb spill` and
  `/bb ring` suppress: auto-attack, wand Shoot, Glide, Revive Battle Pets (the
  Pet Battles minigame — NOT hunter pet control), Mobile Banking, Lighthook
  Grapple. `gen_data_lua` emits it as `ns.SEED.excludeSpells` keyed by id/name.
  The tuning knob for the overflow ring — add IDs to hide more; warlock-niche
  utility + hunter pet abilities are deliberately left visible.

## Keybind notation

Bellular's shorthand, carried verbatim in `keybind`:

| Prefix / form | Means         | Example  | Resolves to |
|---------------|---------------|----------|-------------|
| bare digit    | number row    | `1`      | `1`         |
| bare letter   | that key      | `Q`      | `Q`         |
| `S…`          | Shift+        | `S1`,`SQ`| `SHIFT-1`   |
| `C…`          | Ctrl+         | `C1`,`CV`| `CTRL-V`    |
| `A…`          | Alt+          | `A1`,`AQ`| `ALT-1`     |
| `F1`–`F4`     | stance/form bars | `F1`  | form bar 1  |
| `M3`/`M4`/`M5`| mouse buttons | `M4`     | `BUTTON4`   |
| `MU`/`MD`     | mouse wheel up/down | `SMU` | `SHIFT-MOUSEWHEELUP` |

Modifier prefixes (`S`/`C`/`A`) compose with mouse tokens: `SM4`→`SHIFT-BUTTON4`,
`CM5`→`CTRL-BUTTON5`. `M3` = middle/scroll-click (`BUTTON3`), `M4`/`M5` = the two
side/thumb buttons (`BUTTON4`/`BUTTON5`). Mouse **wheel** is only ever used
*modified* (`MU`/`MD` never appear bare) because unmodified `MOUSEWHEELUP/DOWN`
are reserved for camera zoom.

The dumper (M2) is responsible for translating this shorthand into the real
binding command strings WoW expects (`normKey` in `Dump.lua`).

### Mouse-button binds (2026-07-16 relocate)

The movement + personal-defensive family moved off the awkward `Z`/`X` keyboard
cluster onto the mouse — strictly easier to hit while strafing. Ease order
followed: unmodified > Shift (no Ctrl/Alt needed). Autorun (formerly middle-mouse)
was dropped; it stays on the NumLock default if wanted.

| Combo | Bucket | Was (freed) |
|-------|--------|-------------|
| `M4`  | Movement Ability | `X` |
| `M5`  | Personal Defensive 1 | `Z` |
| `M3`  | Class 1 (Movement) | `S1` |
| `SM4` | Movement Ability 2 | `SX` |
| `SM5` | Personal Defensive 2 | `SZ` |
| `SM3` | Immune/Spell Immune/Movement | `CC` |

Buckets keep their `(bar, slot)` — only the firing key changed — so the six
keyboard keys above free up. The dump now clears any stale key on a managed slot
before binding the seed key, so a relocated key genuinely vacates.

### Contextual bar → `ALT+1..8` (2026-07-16)

`ALT+1..8` now binds the character's **pet bar** (`BONUSACTIONBUTTON1-8`) or
**stance/form bar** (`SHAPESHIFTBUTTON1-N`) — chosen at *dump* time by the addon
(`GetNumShapeshiftForms() > 0` → stance; else a pet class → pet; else cleared).
This is **dumper logic, not a seed bucket** — the pet/stance bars are their own
binding namespaces the game auto-populates, so the seed carries no entries for
them. Consequence in the seed: the four `A1..A4` buckets (`Trinket Macro`,
`Racial Ability`, `Free`, `Free`) are now **keyless** (`"keybind": ""`) — they
keep bar-4 slots 5–8 for the future M5 macro pass, but `ALT+1..4` belongs to the
contextual bar. Trinket + Racial will need a new key when M5 generates them.

## Caveats

- Ability **names only** — no spell IDs. Name→ID resolution happens in-addon at
  apply time (see project-spec "Open technical questions").
- These are Bellular's *recommended* placements. They're the seed/default; the
  whole point of the tool is that you dump then tweak.
- A few cells carry the author's uncertainty (e.g. Druid `Efflorescence?`,
  a stray "wait where did demo's demons go?" note). Treat low-confidence cells
  as prompts to verify in-game, not gospel.

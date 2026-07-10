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
  ExtraActionButton, Interact `` ` ``, Autorun on middle-mouse).
- `items` — potions/flasks/oils with Q1/Q2 item IDs (for macro generation).
- `buffs` — raid/self buffs by spec.

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
| words         | literal       | `Middle Mouse` | `BUTTON3` |

The dumper (M2) is responsible for translating this shorthand into the real
binding command strings WoW expects.

## Caveats

- Ability **names only** — no spell IDs. Name→ID resolution happens in-addon at
  apply time (see project-spec "Open technical questions").
- These are Bellular's *recommended* placements. They're the seed/default; the
  whole point of the tool is that you dump then tweak.
- A few cells carry the author's uncertainty (e.g. Druid `Efflorescence?`,
  a stray "wait where did demo's demons go?" note). Treat low-confidence cells
  as prompts to verify in-game, not gospel.

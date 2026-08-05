---
description: Review addon Lua against the wow-developer house rules
---

Review the addon code in the current diff (or the paths given in `$ARGUMENTS`) against the
seven house rules. Load `.claude/skills/wow-developer/references/house-rules.md` first —
it carries the full text and the reasoning; this command is the mechanical pass.

Run each check. Report `file:line → rule → verdict` in a table, most severe first.

**Do NOT auto-fix rules 1 or 7.** Deleting a comment can destroy the only surviving record
of a measured fact, so the fix is always *move it to `observations.md`*, which needs
judgement. Propose those; apply nothing until the user says so.

## 1 · Comments

```bash
# ratio per file, and no file's ratio increased in this diff
for f in <changed .lua>; do
  c=$(grep -cvE '^\s*(--|$)' "$f"); m=$(grep -cE '^\s*--' "$f")
  awk -v c=$c -v m=$m -v f="$f" 'BEGIN{printf "%-28s %5d %5d  %.2f\n", f, c, m, m/c}'
done
grep -nE '^\s*--.*20[0-9]{2}-[0-9]{2}' <files>                      # dates
grep -nE '^\s*--.*v0\.[0-9]' <files>                                # versions
grep -nEi '^\s*--.*(used to|Phase [0-9]|CORRECTION|was wrong|this replaced|deleted)' <files>
```
Also flag any comment block > 6 lines (> 10 for a file header). Every hit is DELETED or
MOVED to `knowledge/addon-dev/observations.md` — never silently dropped.

## 2 · Probes

```bash
ls <Addon>/probes/ 2>/dev/null                                       # the inventory
grep -rn 'TEMPORARY\|MEANT TO BE DELETED' <Addon>/*.lua              # must be ZERO
```
- Any probe past its `expires` date?
- Any probe whose `lands-in` target already asserts the answer? (If so it should already be deleted.)
- A removed probe left nothing behind: `.toc` line, capture stream, `DEFAULTS` entry, spec, extractor.

## 3 · Captures

- Every write goes to `<DB>.captures.<stream>` — no new top-level SavedVariables store.
- Every stream declares `sessions` AND `cap`. Nothing unbounded.
- No game value reaches a line except through `Capture.Safe()`.
- No `|cff` colour escape inside a captured line.
- Anything a future reader would slice by is a `:Mark`, not implied. (Pre-rendered lines
  are a one-way door — this is the check that prevents a re-fly.)

```bash
uv run python -m wowkb.capture <addon> --list                        # streams + bounds
```

## 4 · Surfaces

```bash
grep -nE ':find\("(on|off)"\)' <files>                               # substring dispatch — ZERO
```
- Every "give me a dump" path is a `Dumps.Register` button, not a slash subcommand.
- No command deeper than `/<addon> <verb> [<arg>]`.
- Commands come from a schema table, not a hand-rolled parser.

## 5 · Shipped vs experimental

- The `.toc`'s probe lines all sit below the probe banner.
- Every `--@unverified` path is in the current flight's acceptance set.

```bash
grep -rn '\-\-@unverified' <Addon>/*.lua
```

## 6 · Tests

- No spec asserts against a fake of an API this workspace has never called.
- Probe specs live in `tests/probes/`, ≤8 each, referenced by no other spec.
- No spec transcribed from the module under test — check every `ref:`.
- `busted` green, and `#pinned + #fixed` did not go down.

```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck <Addon>/ && busted <Addon>/tests/spec
```

## 7 · The KB

- Every game fact learned in this diff is in `observations.md` or a topic file.
- No `observations.md` entry lacks a `Drains to:`.

```bash
uv run python -m wowkb.obs check
```

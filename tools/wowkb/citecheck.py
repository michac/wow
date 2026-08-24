"""Do the KB's Tier-1 source citations still resolve?

`knowledge/addon-dev/` cites Blizzard's shipped UI source and its generated docs by
`[T1 src @12.1.0: <file>:<lines>]` / `[T1 docs @12.1.0: <file> — <Symbol>]`. Both forms name a
file in one of the two clones under `raw/addon-research/`. Only one of them survives Blizzard
reflowing that file.

Measured 2026-08-21: `Blizzard_SharedXML/Dump.lua` is 486 lines in both 12.0.7.68887 and
12.1.0.69273, with `type(val)` at 98 / 149 / 309 in both — while `CooldownViewer.lua` went
2168 → 2374 lines over the same interval. A line anchor is therefore right in the files nobody
touched and silently wrong in the ones that were reworked, and NOTHING ABOUT THE CITATION SAYS
WHICH. A symbol plus a quoted fragment survives reflow and fails loudly when the code actually
changes, which is the event worth catching.

So this checker has two verdicts, deliberately unequal:

  SYMBOL citations  — hard failures. The symbol either appears in the named file or it does not,
                      and "does not" means the claim above it is describing code that is gone.
  LINE citations    — reported, never failed. There are ~1000 of them, they predate the rule, and
                      repairing them is its own job. The count is the size of that job.

    uv run python -m wowkb.citecheck             # symbol citations gate, line citations counted
    uv run python -m wowkb.citecheck --lines     # also list every line-anchored citation
    uv run python -m wowkb.citecheck --verbose   # print every resolved symbol too
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KB = REPO / "knowledge" / "addon-dev"
CLONES = REPO / "raw" / "addon-research"

# `@12.1` and `@12.1.0` both mean the 12.1 clone. An unstamped or 12.0.x citation is the older
# one — that is what the files' own front matter says a bare locator was read at.
CLONE_12_1 = CLONES / "wow-ui-source-12.1.0"
CLONE_12_0 = CLONES / "wow-ui-source"

# [T1 src @12.1.0: <body>] / [T1 docs: <body>] / [T1 src @12.1: <body>]
CITE = re.compile(r"\[T1 (?P<kind>src|docs)(?P<ver>[^:\]]*): (?P<body>[^\]]+)\]")

# The first thing in the body that looks like a source file.
FILE = re.compile(r"[A-Za-z_][\w./-]*\.(lua|xml|xsd|toc)")

# A bare `:123` / `:123-145` locator, with no file of its own — it continues the file named
# earlier in the same citation, or in the sentence above it. Nothing to resolve by symbol.
LINES_ONLY = re.compile(r"^`?:\d")

# A `File.lua:123` locator ANYWHERE in the prose, not only inside a `[T1 …]` bracket. The KB
# writes most of its source pointers this way — inline, in parentheses — and they rot the same
# way, so the repair job is sized off both forms together.
INLINE = re.compile(r"[A-Za-z_][\w./-]*\.(?:lua|xml|xsd|toc):\d+")

# What counts as a symbol worth grepping for. Deliberately narrow: an identifier of 4+ chars,
# optionally with a `:` or `.` qualifier (`CustomAuraButtonPrivateMixin:ApplyApplicationCount`,
# `Enum.SecretAspect`), or a SCREAMING_CASE event name.
SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}(?:[:.][A-Za-z_][A-Za-z0-9_]*)*")

# Words that match SYMBOL but are prose, not code. A citation whose symbol part is entirely
# prose resolves on its filename alone — it is not a symbol citation and is not gated.
PROSE = {
    "the", "and", "its", "with", "from", "into", "that", "this", "path", "call", "line",
    "lines", "block", "table", "field", "fields", "entry", "entries", "marker", "markers",
    "comment", "apply", "shape", "which", "where", "when", "their", "there", "these",
    "those", "each", "both", "only", "same", "whole", "above", "below", "under", "over",
    "name", "names", "value", "values", "case", "cases", "form", "forms", "list", "lists",
    "declaration", "definition", "member", "members", "row", "rows", "column", "columns",
    "section", "sections", "constant", "constants", "record", "records", "struct", "type",
    "types", "return", "returns", "argument", "arguments", "example", "examples", "note",
    "notes", "verbatim", "quoted", "fragment", "sibling", "siblings", "variant", "variants",
    "Event", "LiteralName", "Name", "Type", "Documentation",
}


def clone_for(ver: str) -> Path:
    return CLONE_12_1 if "12.1" in ver else CLONE_12_0


def find_file(clone: Path, name: str) -> Path | None:
    """Resolve a cited path or bare basename inside a clone.

    Citations name a file three ways — full repo-relative path, `Addon/File.lua`, and bare
    `File.lua`. All three are legitimate; only the last can be ambiguous, and in this corpus
    every basename that matters is unique.
    """
    direct = clone / name
    if direct.is_file():
        return direct
    hits = list(clone.rglob(name.split("/")[-1]))
    if len(hits) == 1:
        return hits[0]
    if hits and "/" in name:
        tail = name.lstrip("./")
        for h in hits:
            if h.as_posix().endswith(tail):
                return h
    return hits[0] if hits else None


def symbols(rest: str) -> list[str]:
    """The identifier-shaped tokens in a citation's symbol part, prose removed."""
    out = []
    for m in SYMBOL.finditer(rest):
        tok = m.group(0)
        if tok in PROSE or tok.lower() in PROSE:
            continue
        # A qualified name is checked by its last component too — `Mixin:Method` appears in
        # source as `function Mixin:Method(`, but `Enum.SecretAspect` may appear split.
        out.append(tok)
    return out


def resolves(path: Path, syms: list[str]) -> str | None:
    """The first cited symbol that appears in the file, or None if none does."""
    text = path.read_text(encoding="utf-8", errors="replace")
    for s in syms:
        if s in text:
            return s
        tail = re.split(r"[:.]", s)[-1]
        if len(tail) > 3 and tail in text:
            return s
    return None


def scan() -> tuple[list[dict], list[dict], list[dict]]:
    """(symbol failures, symbol passes, line-anchored citations)."""
    fails: list[dict] = []
    passes: list[dict] = []
    lines: list[dict] = []

    for md in sorted(KB.rglob("*.md")):
        # ⚠ Scanned as ONE STRING, not line by line. A citation naming a symbol is the longest
        # kind there is, so it is the kind that wraps — and a per-line regex sees none of them.
        # Measured 2026-08-21: a line-based scan found 11 symbol citations where the corpus held
        # more, silently skipping every multi-line one. A gate that ignores its most informative
        # subjects is worse than no gate, because the count reads like coverage.
        text = md.read_text(encoding="utf-8")
        for m in CITE.finditer(text):
            body = " ".join(m.group("body").split())   # unwrap: a wrapped cite is one cite
            ver = m.group("ver")
            rec = {"file": md.relative_to(REPO).as_posix(),
                   "line": text.count("\n", 0, m.start()) + 1,
                   "cite": " ".join(m.group(0).split())}

            if LINES_ONLY.match(body):
                lines.append(rec)
                continue

            hits = list(FILE.finditer(body))
            if not hits:
                # No file named at all — a corpus-count or wiki-shaped T1 cite. Not ours.
                continue

            # ONE CITATION MAY NAME SEVERAL FILES ("Interpolator.lua, EasingUtil.lua";
            # "…Documentation.lua; T1 xsd: UI.xsd:702-713"). Each file owns the text up to
            # the next one, so a later filename is never mistaken for a symbol of an
            # earlier file — which is exactly what two false positives looked like.
            clone = clone_for(ver)
            for n, fm in enumerate(hits):
                name = fm.group(0)
                end = hits[n + 1].start() if n + 1 < len(hits) else len(body)
                rest = body[fm.end():end]

                # A line range after the filename is a line anchor, whatever else follows.
                if re.match(r"^:\d", rest):
                    lines.append(dict(rec))
                    continue

                syms = symbols(rest)
                if not syms:
                    # Filename-only, or prose-only. Nothing to gate on beyond the file.
                    continue

                target = find_file(clone, name)
                if target is None:
                    fails.append(rec | {"why": f"file not found in {clone.name}: {name}"})
                    continue

                hit = resolves(target, syms)
                if hit is None:
                    fails.append(rec | {
                        "why": f"none of {syms} found in {target.relative_to(clone)}"})
                else:
                    passes.append(rec | {"sym": hit,
                                         "target": target.relative_to(clone).as_posix()})
    return fails, passes, lines


def inline_locators() -> list[tuple[str, int, str]]:
    """Every `File.lua:123` pointer in the KB's prose, `[T1 …]` brackets included.

    Reported, never gated — this is the pre-existing corpus the symbol rule postdates. What the
    number is FOR is deciding whether repairing them is a job worth scheduling, so it counts
    every rotting form, not only the ones inside a citation bracket.
    """
    out: list[tuple[str, int, str]] = []
    for md in sorted(KB.rglob("*.md")):
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for m in INLINE.finditer(line):
                out.append((md.relative_to(REPO).as_posix(), i, m.group(0)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lines", action="store_true", help="list every line-anchored citation")
    ap.add_argument("--verbose", action="store_true", help="list resolved symbol citations too")
    args = ap.parse_args()

    for c in (CLONE_12_1, CLONE_12_0):
        if not c.is_dir():
            print(f"missing clone: {c} — nothing to resolve against", file=sys.stderr)
            return 2

    fails, passes, lines = scan()

    print(f"symbol-anchored citations : {len(passes) + len(fails)}  "
          f"({len(passes)} resolve, {len(fails)} do NOT)")
    inl = inline_locators()
    print(f"line-anchored citations   : {len(lines)}  (report-only — see --lines)")
    print(f"  …of a total {len(inl)} `File.lua:123` locators in the subtree, counting the ones")
    print(f"     written inline in prose rather than inside a [T1 …] bracket")

    if args.verbose:
        print()
        for r in passes:
            print(f"  ok  {r['file']}:{r['line']}  {r['sym']} → {r['target']}")

    if args.lines:
        print()
        for f, i, loc in inl:
            print(f"  line  {f}:{i}  {loc}")

    if fails:
        print()
        for r in fails:
            print(f"{r['file']}:{r['line']}  [citation does not resolve]")
            print(f"    {r['cite']}")
            print(f"    {r['why']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

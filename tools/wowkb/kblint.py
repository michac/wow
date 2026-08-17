"""The addon-dev KB gates — README §7's current-state rule and §0's evidence classes.

A topic file states what is true now, it never states what it used to say, and it stands
on what it says. Five checks keep it that way.

README §7 — the current-state rule:

  1. no retrospective prose ("an earlier draft said…") outside a Changelog
  2. every date sits in front matter, a citation, a [client]/[searched] tag, or the
     Changelog
  3. no section corrected by a later part of the SAME file

README §0 — the evidence classes:

  4. no negative existential ("there is no way to…") in a CLAIM UNIT tagged [client] — one
     bullet, one table row, one ordinal, one quote, one paragraph (see claim_units). A
     [client] tag means "we ran code and saw this value"; a claim about the whole space
     of ways to observe something is not a value anybody saw. It takes [searched …],
     which names where we looked — and whose omissions a reader can then see.
  5. no citation circle: a topic-file claim may not rest on OBS-nnn, a projects/** path,
     a capture path or one of our addon names. Those point back at the work that produced
     the claim, which is how a wrong claim gets cited as its own support.

    uv run python -m wowkb.kblint            # report, exit 1 on any hit
    uv run python -m wowkb.kblint --counts   # per-file table only
    uv run python -m wowkb.kblint --gate 2   # one gate

Why a tool and not five greps: a grep cannot tell a front-matter continuation line from
prose, cannot skip a fenced code block (so README §7's own gate definitions match
themselves), cannot tell `security.md §4.6` — a cross-file pointer — from `§4.6`, a
self-correction, and cannot see that a claim's phrasing and its evidence tag are on
different lines of the same claim unit. Each of those produced a false positive or a miss
that cost an agent real work.
"""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]
KB = REPO / "knowledge" / "addon-dev"
KB_ALL = REPO / "knowledge"

# Gates 1, 3 and 6 are KB-WIDE (_meta/writing-claims.md). Gates 2, 4 and 5 encode
# addon-dev's stricter evidence classes and stay scoped to that subtree — gate 2 in
# particular would fire on every legitimate game date ("Season 2 opens 2026-08-18")
# in the gameplay KB, where the game's own calendar is content, not provenance.
UNIVERSAL_GATES = (1, 3, 6)
ADDON_DEV_GATES = (2, 4, 5)

# Queues are exempt from everything: a queue entry IS a dated event (README §1.2).
# sources.md is a registry whose rows are "what was on disk, when".
QUEUES = {"observations.md", "mined-pending-verification.md", "12.1.0-ptr-heads-up.md"}
REGISTRY = {"sources.md"}

# The KB-wide equivalents, by path relative to knowledge/. Same principle: a file whose
# ROWS ARE DATED EVENTS cannot be asked to state only the present.
#   - the parking lot and the patch ledgers are history BY CONSTRUCTION
#   - patch-notes/ is a verbatim archive against link rot — editing it would be the defect
#   - verify-in-game.md is GENERATED (wowkb.gen_verify); fix the markers, not the output
#   - characters/ snapshots carry hand-written deltas ("since last reset…") by design
#   - writing-claims.md is the doctrine, so it necessarily quotes what it bans
EXEMPT_GLOBS = (
    "_meta/kb-inbox.md",
    "_meta/changelog-*.md",
    "_meta/patch-notes/*",
    "_meta/verify-in-game.md",
    "_meta/feed-watermark.md",
    "_meta/writing-claims.md",
    "characters/*",
)

# addon-dev README §7 *defines* the rules, so its prose necessarily contains the patterns
# it bans. Matched by PATH, not by name — rglob sees four other README.md files.
DOCTRINE = {"README.md"}
DOCTRINE_PATH = KB / "README.md"
DOCTRINE_SECTION = re.compile(r"^## 7\. How a claim is written")

# Gates 4 and 5 both need a WHOLE-file pass over README, which DOCTRINE's truncate-at-§7
# does not give: §0 defines the evidence classes, so it must be free to print the exact
# shapes it bans — `never "there is no way to"` is the counter-example a stranger needs to
# see, and the doctrine is worth less without it.
# ⚠ Belt and braces, honestly labelled: claim_units() alone is currently enough here, since
# §0's `[client 20]` grep hint sits in its own bullet. But that is an accident of where one
# incidental tag landed — before claim units, that single tag vouched for all 30 lines of
# the class list — and §0 is the one file guaranteed to keep quoting banned phrasings. The
# exemption is what stops a future edit re-arming it.
NEG_EXEMPT = DOCTRINE

# Gate 5 exempts sources.md too: it is the registry of what is on disk, and our own addons
# are literally rows in it. README earns it a second way — §1's topic map, §1.2's queue
# table and §4's audit targets all name OBS-nnn, projects/** and our addons legitimately.
POINTER_EXEMPT = DOCTRINE | REGISTRY

# Gate 1. The first seven alternatives are addon-dev's original list; the rest were added
# when the rule went KB-wide, harvested from the 69 files the first census found. The
# shape that dominates outside addon-dev, and that none of the original seven caught:
#   "This page previously claimed X. That was wrong."
#   "⚠ The old KB label … has been dropped"
#
# ⚠ EVERY ALTERNATIVE HERE MUST NAME OUR OWN PRIOR TEXT. That is the line this gate walks,
# and two attempts to widen it past that line were measured and reverted 2026-08-17:
#
#   - `supersed(e|ed|es)` — reverted. Both of its addon-dev hits were ordinary English
#     about the SUBJECT, not about us: "a re-application supersedes the removal it
#     resolves" (an aura-lifecycle fact) and "superseded per LibDeflate README" (one
#     library replacing another). Zero true positives, two false.
#   - a case-insensitive `corrected` — reverted. It fires on "corrected by practitioners"
#     (a description of how the wiki works) and "every one of the 124 was corrected before
#     publication" (a description of a mining pass). Kept only in the CAPITALISED banner
#     shapes below, which are ours.
#
# A statement that an EXTERNAL SOURCE is wrong is deliberately not matched: "Tier-3 guides
# say Champion; they are wrong" is a live source-conflict note, which CLAUDE.md's
# provenance-precedence rule positively requires. Only "WE said" is retrospective.
RETRO = re.compile(
    r"an earlier (draft|version|pass|run|note)"
    r"|previously (said|read|cited|written|showed|gave|asserted|claimed|implied|also listed)"
    r"|\[corrected"
    r"|used to (be|read|say|assert|show)"
    r"|Adversarial verification pass"
    r"|th(is|e) (page|file|entry|section|line) previously"
    r"|corrects an earlier"
    r"|(is|are|was|were) corrected \(20"
    r"|the old KB"
    r"|has been dropped"
    r"|no longer (true|correct|accurate)"
    r"|earlier KB", re.I)

# The banner shapes, CASE-SENSITIVE — these are ours by construction. A lower-case
# "corrected" is ordinary English and belongs to the subject; a capitalised one is a
# heading we wrote about ourselves.
RETRO_CS = re.compile(
    r"\bCORRECTED\b"
    r"|\*\*Correct(ed|ion)"
    r"|GRADE CORRECTION")

DATE = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}")

# A date is legal inside a bracketed citation stamp or a [client]/[searched] tag. The
# bracket may open on an earlier line (citations wrap), so we also accept a line that is
# plainly a continuation of one.
DATE_OK = re.compile(
    r"\[(T[0-9][^]]*|client|searched|gh[^]]*)\s"  # [T2 wiki: … [client … [gh: …
    r"|revid [0-9]+,\s*20"
    r"|lastedit \*{0,2}20|rev [0-9]+, lastedit"   # wiki citation, the revid twin
    r"|filed 20|closed 20|created 20"             # a bug's era is evidence about the bug
    r"|pushed_at 20|created_at 20"
    r"|@ '?[0-9a-f]{6,}'?,\s*20"                 # commit-pin: @ '3fdc10f6', 2026-07-21
    r"|`[0-9a-f]{6,}`,\s*20"                     # commit-pin: `38d4bf1e`, 2026-07-20
    r"|`[0-9a-f]{6,}`\s*\(20"                    # commit-pin: `e89d5055c761` (2026-07-16)
    r"|@ ?`?[0-9a-f]{6,}`?"                      # any `path @ <sha>` pin on the same line
    r"|\$(Id|Revision):"                         # SVN keyword expansion, verbatim
    r"|quoted at|\"\s*,\s*20[0-9]{2}-")          # blue-post attribution inside a quote

# Gate 3: a ⚠/❌ pointing at a § in THIS file is a defect ticket. One qualified by a
# filename is an ordinary cross-reference.
SELFREF = re.compile(r"(⚠⚠?|❌)(?P<mid>.{0,120}?)§[0-9]")
FILENAME_NEAR = re.compile(r"[A-Za-z0-9_.-]+\.md`?[\s,]*$|README`?[\s,]*$")

# Gate 4: the phrasings that turn an observation into a claim about an unbounded space.
# This is README §0's floor list and a strict superset of it — add alternatives, never
# narrow one. Two additions: `\W{0,4}` tolerates the emphasis this KB writes its headlines
# in ("⚠ Aspect-less — there is **no readback**" is precisely the Dreadstalkers shape, and
# a literal `there is no` walks straight past it), and `never reports` joins the two verbs
# the floor already names. Deliberately loose in the floor's own direction — it inherits
# "there is normally" from `there is no`. Over-flagging costs one triage verdict;
# under-flagging is how the disease got in.
NEG = re.compile(
    r"there (is|are)\W{0,4}no"
    r"|nothing\W{0,4}can"
    r"|no way to"
    r"|cannot\W{0,4}be"
    r"|is not possible"
    r"|never\W{0,4}(fires|answers|reports)", re.I)

# The two evidence tags gate 4 arbitrates between. Both are dated by README §0, and
# requiring the date here is what stops `[searched: auras]` from silencing the gate
# without saying when we looked.
CLIENT_TAG = re.compile(r"\[client 20")
SEARCHED_TAG = re.compile(r"\[searched 20")

# Where one claim unit ends and the next begins — a list marker, an ordinal, a table row or
# a heading. See claim_units() for why a blank line alone is not enough. The trailing \s on
# the bullet and ordinal forms is what keeps `**bold**` and `---` out: both open a
# continuation line, not a new unit.
# ⚠ `>` is DELIBERATELY ABSENT — do not add it for symmetry. A blockquote is ONE claim
# quoted across many lines, not one claim per line, and this KB has 17 multi-line quotes
# (up to 27 lines) with the `[client]` tag on the opening line of the quoted measurement —
# `cooldown-manager.md:355-369` is exactly that shape. Splitting per line would orphan the
# tag from every later line of its own quote. Measured: including `>` changes gate 4 by
# nothing at all, so it buys zero findings and costs a whole false-negative class.
UNIT_START = re.compile(r"[-*+]\s|[0-9]+\.\s|\||#{1,6}\s")

# Gate 5: a pointer back into our own work. `raw/*.log` is a capture path — the file is a
# rolling SavedVariables ring, so it is the least re-checkable citation in the subtree.
# An addon has three names here and all three are the same pointer: the repo name
# (`CDMProbe`), the slash command that drove it (`/cdmp curve card`) and the reader that
# pulled the capture out (`wowkb.capture`). README §0's rule is "never the tool that drove
# them", so all three are findings.
# ⚠ Slash forms are matched with a lookbehind, never bare: `cap` is ordinary English here
# ("Cap: 20 entries or 2 KB"), and a bare `ps`/`bb` would fire inside half the prose.
# ⚠ And only the wowkb modules that read OUR ADDONS are listed. `wowkb.uiapi`, `.wiki` and
# `.wago` reach Blizzard's generated docs, the wiki and DB2 — admissible sources, named 27
# times here as the way to look something up, which is precisely what a `[searched]`
# instrument list is FOR. A blanket `wowkb\.\w+` swept all 27 in and would have turned this
# gate into the sourcing ban that was rejected 2026-08-09. The target is the pointer home,
# not the road out.
POINTER = re.compile(
    r"OBS-[0-9]{3}"
    r"|projects/"
    r"|CDMProbe|BucketBinds|PlannerState|ClientLab"
    r"|(?<![\w/])/(cdmp|clab|bb|ps|cap)\b"
    r"|wowkb\.(capture|cdmp|lab|obs|addon|diagnostics)\b"
    r"|raw/[^\s`)\]]*\.log")


def strip(path: Path) -> list[tuple[int, str]]:
    """(lineno, text) for lines that carry a CLAIM.

    Drops front matter (including wrapped continuation lines), fenced code blocks, the
    Changelog section, and — in the doctrine file — the section that defines these rules.
    """
    out: list[tuple[int, str]] = []
    in_fm = False
    in_fence = False
    done = False
    doctrine = path.resolve() == DOCTRINE_PATH.resolve()

    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if i == 1 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if line.strip() == "---":
                in_fm = False
            continue
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or done:
            continue
        if line.startswith("## Changelog"):
            done = True
            continue
        if doctrine and DOCTRINE_SECTION.match(line):
            done = True          # §7 is last in README; everything after defines the rules
            continue
        out.append((i, line))
    return out


def is_exempt(path: Path) -> bool:
    """True for the KB-wide queues, archives and generated files (EXEMPT_GLOBS)."""
    try:
        rel = path.resolve().relative_to(KB_ALL.resolve()).as_posix()
    except ValueError:
        return False
    return any(PurePosixPath(rel).match(g) for g in EXEMPT_GLOBS)


def lede(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """strip()'s output down to the LEDE — everything before the first `##` heading.

    Gate 6's scope. The rule it enforces (writing-claims.md rule 3) is that a reader who
    quits after the first screen is incomplete, never wrong: the lede states what is true
    and carries no correction note.

    ⚠ Scoped to RETRO only, not to ⚠ or hedging generally. A lede warning about the
    CURRENT state is exactly right and common in this KB — `factions/silvermoon-court.md`
    opens by warning that Slayer's Rise is not one of the five renown tracks, which is a
    live fact a reader needs before the list, not a correction of our own earlier text.
    """
    out: list[tuple[int, str]] = []
    for n, text in lines:
        if text.startswith("## "):
            break
        out.append((n, text))
    return out


def claim_units(lines: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    """Group strip()'s output into CLAIM UNITS — the scope gate 4 arbitrates over.

    Gate 4 cannot work line by line: a claim's phrasing and its evidence tag routinely sit
    on different lines, because the sentence wraps or the `[client]` stamp closes a bullet
    three lines below the "there is no".

    It cannot work on blank-line blocks either, and that is the harder lesson. This KB
    writes its densest evidence as unseparated tables and numbered lists, so a blank-line
    block in `security-taint-and-restricted-data.md` reaches 136 lines — and one incidental
    `[client]` tag then vouches for negatives 13, 36 and 57 lines away, on unrelated rows.
    Worse for a gate whose job is to be driven to zero: a CORRECT `[searched]` conversion
    of one row would silence every other negative in the same 136 lines, so the gate would
    read clean with the sites never triaged. Measured: one such conversion took the file
    from 11 findings to 8, three of them vanishing unread.

    So a unit ends at a blank line OR where the next one begins, and a new unit begins at a
    list marker, an ordinal, a table row or a heading — NOT a blockquote, see UNIT_START.
    An indented line carrying no marker is a continuation and belongs to the unit above it.

    ⚠ Three residual shapes, none of which bites the current corpus. Listed so the next
    person recognises one instead of rediscovering it:

      - THE FENCE JOIN. strip() drops a fenced block whole, so a unit / code block /
        continuation run with no blank line between them still joins. This inflates scope
        — and, the direction that actually matters, it can SILENCE: a `[searched 20…]` on
        a continuation line just after a fence merges backwards across it and suppresses a
        negative on the far side. A false negative in a gate driven to zero is the
        expensive kind.
      - NESTED LISTS. A child bullet opens its own unit, so a parent's `[client]` does not
        vouch for the child's negative, nor the reverse.
      - A BOLD HEADLINE NEGATIVE followed by a blank line and then an evidence bullet: the
        blank line separates them, so the tag never reaches the headline it supports.
    """
    units: list[list[tuple[int, str]]] = []
    cur: list[tuple[int, str]] = []
    for n, text in lines:
        if not text.strip():
            if cur:
                units.append(cur)
                cur = []
            continue
        if cur and UNIT_START.match(text.lstrip()):
            units.append(cur)
            cur = []
        cur.append((n, text))
    if cur:
        units.append(cur)
    return units


def check(path: Path) -> dict[int, list[tuple[int, str]]]:
    """Run every gate in scope for `path`.

    Gates 2, 4 and 5 are addon-dev-only; outside that subtree they return empty rather
    than being skipped, so the report keeps one column layout for the whole KB.
    """
    name = path.name
    hits: dict[int, list[tuple[int, str]]] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    in_addon_dev = KB.resolve() in path.resolve().parents
    if (in_addon_dev and name in QUEUES) or is_exempt(path):
        return hits
    lines = strip(path)

    for n, text in lines:
        if RETRO.search(text) or RETRO_CS.search(text):
            hits[1].append((n, text.strip()))
        if in_addon_dev and name not in REGISTRY and DATE.search(text) and not DATE_OK.search(text):
            hits[2].append((n, text.strip()))
        m = SELFREF.search(text)
        if m and not FILENAME_NEAR.search(m.group("mid")):
            hits[3].append((n, text.strip()))
        if in_addon_dev and name not in POINTER_EXEMPT and POINTER.search(text):
            hits[5].append((n, text.strip()))

    for n, text in lede(lines):
        if RETRO.search(text) or RETRO_CS.search(text):
            hits[6].append((n, text.strip()))

    if in_addon_dev and name not in NEG_EXEMPT:
        for unit in claim_units(lines):
            body = "\n".join(text for _, text in unit)
            if not CLIENT_TAG.search(body) or SEARCHED_TAG.search(body):
                continue
            for n, text in unit:
                if NEG.search(text):
                    hits[4].append((n, text.strip()))
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m wowkb.kblint",
        description="Check the KB against the current-state rule "
                    "(_meta/writing-claims.md) and addon-dev's evidence classes.")
    ap.add_argument("--counts", action="store_true", help="per-file table only")
    ap.add_argument("--gate", type=int, choices=(1, 2, 3, 4, 5, 6),
                    help="report one gate only")
    ap.add_argument("--all", action="store_true",
                    help="scan all of knowledge/ (gates 1,3,6), not just addon-dev")
    ap.add_argument("--warn", action="store_true",
                    help="report findings but exit 0 — for burning down the backlog. "
                         "SCAFFOLDING: stop passing it once the count reaches zero")
    args = ap.parse_args(argv)

    gates = [args.gate] if args.gate else [1, 2, 3, 4, 5, 6]
    names = {1: "retrospective prose", 2: "date in prose", 3: "self-correcting section",
             4: "unqualified negative", 5: "citation circle", 6: "correction in the lede"}
    total = {g: 0 for g in gates}
    rows = []

    if args.all:
        paths = sorted(KB_ALL.rglob("*.md"))
        label = lambda p: p.resolve().relative_to(KB_ALL.resolve()).as_posix()
    else:
        paths = sorted(KB.glob("*.md"))
        label = lambda p: p.name

    for path in paths:
        hits = check(path)
        counts = {g: len(hits[g]) for g in gates}
        for g in gates:
            total[g] += counts[g]
        rows.append((label(path), counts, hits))

    w = max(len(r[0]) for r in rows)
    print(f"{'file':<{w}}  " + "  ".join(f"G{g}" for g in gates))
    for name, counts, _ in rows:
        if any(counts.values()) or not args.counts:
            marks = "  ".join(f"{counts[g] or '.':>2}" for g in gates)
            print(f"{name:<{w}}  {marks}")
    print(f"{'TOTAL':<{w}}  " + "  ".join(f"{total[g]:>2}" for g in gates))

    if not args.counts:
        for name, counts, hits in rows:
            for g in gates:
                for n, text in hits[g]:
                    print(f"\n{name}:{n}  [gate {g}: {names[g]}]\n    {text[:160]}")

    if args.warn and any(total.values()):
        print(f"\n⚠ --warn: {sum(total.values())} findings, exiting 0. "
              f"This flag is scaffolding — drop it once the backlog is zero.")
        return 0
    return 1 if any(total.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())

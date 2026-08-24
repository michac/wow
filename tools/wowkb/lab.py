"""Deploy the ClientLab scratch addon, read its runs, and drain answers into the KB.

ClientLab is the lab addon (projects/addon-lab/): a long-lived scratch addon that
answers knowledge/addon-dev/ questions by running one line of Lua in the client.
It is deliberately NOT a product — no GitHub repo, no releases, no ghaddons, not in
the wowkb.addon registry. So its deploy is a plain DIRECTORY COPY into the WoW
install, and adding a test costs a copy, not a release cut.

    uv run python -m wowkb.lab deploy            # copy + registry cross-check
    uv run python -m wowkb.lab deploy --check     # cross-check only, don't copy
    uv run python -m wowkb.lab show               # result BESIDE expect, per question
    uv run python -m wowkb.lab show --id <id>     # one question, full text
    uv run python -m wowkb.lab drain <id>         # mint the observation that carries it
    uv run python -m wowkb.lab blocked            # open rows grouped by what they need

THE UNKNOWNS LOOP IS NOT IN THIS FILE, DELIBERATELY. An unknown is recorded as a MARKER
on the claim itself — `[gap]` / `[unverified]` / `@verify-ingame`, promoted to
`@pending-test` once a test exists — because an agent reading the topic file meets the
marker in the prose it is already reading. A tool that re-derives that list is a step
somebody has to remember, and a step somebody has to remember is a gate that fails
silently. What this file owns is the half a marker cannot do: the id ⇄ test ⇄ run join,
and the drain. The process is `projects/addon-lab/docs/lab-process.md`.

THE REGISTRY CROSS-CHECK (the same "no check function for this id" rule cmd_check in
cdmp.py applies, both directions): every `built` question in questions.json must have a
matching ns.Test{} in ClientLab/T_*.lua, and every ns.Test{} id must be a `built` question.
An unmatched id is a LOUD ERROR, never a silent skip — a test that runs but has no registry
row would emit a value nobody is expecting, and a registry row with no test is a silent
hole in coverage. An ANSWERED question must have NO test: it is deleted with the claim it
produced, and a leftover one fails the check by name.

THE ONE RULE OF `show`: it renders result beside `expect` and STOPS. `expect` is never
compared programmatically and no verdict is ever printed — a human reads the pair and
decides. An automatic PASS/FAIL would be the instrument grading its own subject
(Lab.lua:1-8). `skipped` is rendered as its own loud group; it is never a pass.

Reuses charstate.DEFAULT_WOW rather than repeating the /mnt/c/... path here, where
it would rot out of step with every other tool.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from . import capture
from .capture import render_value
from .charstate import DEFAULT_WOW, parse_savedvar

REPO = Path(__file__).resolve().parents[2]
LAB = REPO / "projects" / "addon-lab"
SRC = LAB / "ClientLab"
QUESTIONS = LAB / "questions.json"
KB = REPO / "knowledge" / "addon-dev"
OBS = KB / "observations.md"

# A question whose registry row expects a test to exist — `built`, and only `built`.
#
# A DRAINED QUESTION'S ROW IS REMOVED, AND ITS TEST IS DELETED WITH THE CLAIM IT PRODUCED.
# House rule 2 (probe code dies in the commit that writes its KB claim), applied to the lab.
# `cmd_drain` deletes the row on drain — questions.json stays a live worklist of OPEN
# questions only, shrinking on drain exactly like the T_*.lua files. The OBS entry the drain
# mints (observations.md) plus git together archive the question, its `expect`, the run and
# the verdict — everything the old retained `answered` row held, in richer form — so the row
# was pure duplication. (Patch-day re-verification is owned by `<version>-ptr-heads-up.md`
# and the `/update` sweep, not by a kept row: `show` refuses to print a verdict by design,
# so a retained test re-measured settled facts on every pull and caught no regression.)
HAS_TEST = ("built",)

# The whole status vocabulary. `answered` is GONE — a drained question is removed, not
# restatused (see cmd_drain / HAS_TEST). A row outside these three is a loud error in the
# cross-check: the collapse holds only if nothing can re-introduce a fourth.
STATUSES = ("built", "parked", "not-answerable")

# ns.Test{ id = "X" ... }  and  ns.Test{ id="X" ... }
_ID_ASSIGN = re.compile(r'\bid\s*=\s*"([^"]+)"')
# T_Security's row("X", line, ...) helper
_ROW_CALL = re.compile(r'\brow\(\s*"([^"]+)"')

# An `expect` that says only a human eye can close the question. Matching on the PHRASE
# rather than a hardcoded id list means a newly-written visual question is refused too —
# the failure mode this guards is a visual question going green off a programmatic run,
# which the registry records as having already cost this workspace twice.
#
# Matches three questions today: `toc-category-grouping` and `secret-aspectless-pixel-moved`
# (both wholly or half visual, and both named in the W2 plan), plus `draw-layer-z-order`,
# whose `expect` asks for "two overlapping textures and a visual read". The third is not in
# the plan's list and is refused anyway: a test CAN read `GetDrawLayer()` back, but the
# question is whether OVERLAY actually draws above ARTWORK, and no readback answers that.
_EYEBALL = re.compile(
    r"only an eyeball|an eyeball closes|no programmatic oracle"
    r"|\bVISUAL\b|a visual read|and LOOK\b", re.I)

# A verdict option that declines to answer. Author-chosen wording, so matched by phrase.
_UNDECIDED = re.compile(r"can'?t tell|cannot tell|unsure|don'?t know|unclear", re.I)


# ----------------------------------------------------------------- the registry


def load_questions(path: Path = QUESTIONS) -> tuple[dict, dict]:
    """(whole document, {id: question}) — the document is kept so drain can rewrite it."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data, {q["id"]: q for q in data["questions"]}


def lua_ids(src: Path = SRC) -> tuple[list[str], list[str]]:
    """(test ids, ask ids) declared in ClientLab/T_*.lua, in file+source order.

    Three syntaxes: `ns.Test{ id = "..." }`, the `row("...", ...)` helper T_Security
    uses for the 14-row §4.2 table, and `ns.Ask.Register{ id = "..." }` for a visual
    question. All are matched so the cross-check sees the whole registered set.

    Tests and asks are returned SEPARATELY because one question may legitimately have
    both — `draw-layer-z-order` has a test for the facts an API can answer and an ask
    for the composite ordering no API returns. Merging them would report that as a
    duplicate id and fail the check on a correct arrangement.
    """
    tests: list[str] = []
    asks: list[str] = []
    for f in sorted(src.glob("T_*.lua")):
        target = tests
        for line in f.read_text(encoding="utf-8").splitlines():
            # The most recent opening construct owns the `id =` that follows it.
            if "ns.Ask.Register" in line:
                target = asks
            elif "ns.Test" in line:
                target = tests
            m = _ID_ASSIGN.search(line)
            if m:
                target.append(m.group(1))
                target = tests
                continue
            m = _ROW_CALL.search(line)
            if m:
                tests.append(m.group(1))
    return tests, asks


def lua_test_ids(src: Path = SRC) -> list[str]:
    """Every id the Lua registers, tests and asks together, deduplicated."""
    tests, asks = lua_ids(src)
    return tests + [i for i in asks if i not in tests]


def tested_question_ids(path: Path = QUESTIONS) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [q["id"] for q in data["questions"] if q.get("status") in HAS_TEST]


def cross_check() -> tuple[bool, list[str]]:
    """Assert the Lua test set and the tested-question set match, both directions.

    Returns (ok, messages). ok is False on ANY mismatch: a duplicate id, a question
    that should have a test and does not, or a test with no such question.
    """
    msgs: list[str] = []
    ok = True

    data, _ = load_questions()
    bad = sorted({f"{q['id']} ({q.get('status')})" for q in data["questions"]
                  if q.get("status") not in STATUSES})
    if bad:
        ok = False
        msgs.append(f"question(s) with a status outside {STATUSES}: {', '.join(bad)}")

    tests, asks = lua_ids()
    tested = tested_question_ids()

    for kind, got in (("ns.Test{}", tests), ("ns.Ask.Register{}", asks)):
        dupes = sorted({i for i in got if got.count(i) > 1})
        if dupes:
            ok = False
            msgs.append(f"duplicate {kind} id(s) in ClientLab/T_*.lua: {', '.join(dupes)}")

    registered = tests + [i for i in asks if i not in tests]
    lua_set, tested_set = set(registered), set(tested)

    missing_tests = sorted(tested_set - lua_set)
    if missing_tests:
        ok = False
        msgs.append("built questions with NO ns.Test{} in the Lua "
                    f"({len(missing_tests)}): {', '.join(missing_tests)}")

    # A Lua id with no `built` row. Since a drained question's row is REMOVED (not kept as
    # `answered`), a test left behind after its claim was written lands here too — which is
    # the direction the suite quietly grows back. The message names that case because it is
    # the common one and its fix (delete the test — its claim is in the KB) differs from a
    # typo'd id's.
    orphan_tests = sorted(lua_set - tested_set)
    if orphan_tests:
        ok = False
        msgs.append("Lua ids with no `built` question in questions.json "
                    f"({len(orphan_tests)}): {', '.join(orphan_tests)}. If one was just "
                    "drained, delete its test — the claim is in the KB and nothing "
                    "re-checks it here (see HAS_TEST).")

    if ok:
        msgs.append(f"registry cross-check OK — {len(lua_set)} ids match "
                    f"{len(tested_set)} built questions, both directions "
                    f"({len(tests)} tests, {len(asks)} visual checks).")
    return ok, msgs


# ------------------------------------------------------------------ reading a run


@dataclass
class Result:
    """One test's outcome, normalised across the legacy store and the capture stream."""
    id: str
    status: str = "?"
    anchor: str = ""
    bucket: str = ""
    question: str = ""
    value: object = None
    err: str = ""
    why: str = ""
    source: str = "measured"                     # "measured" | "eyeball"
    at: str = ""                                 # the ROW's own moment, not the run's
    stamps: dict = field(default_factory=dict)   # spec / hero / instance / combat

    @property
    def verdict(self) -> str:
        """The human's chosen option, for an eyeball row."""
        if isinstance(self.value, dict):
            return str(self.value.get("verdict", ""))
        return ""

    @property
    def undecided(self) -> bool:
        """A verdict that declines to answer — the eyeball twin of `measured = false`.

        "can't tell" is an honest and useful thing for a person to say, and it must
        never drain: it records that the stimulus did not settle the question, which is
        a finding about the STIMULUS, not an answer to the question.
        """
        return bool(_UNDECIDED.search(self.verdict))

    @property
    def partial(self) -> bool:
        """The test answered, but flagged its own coverage as incomplete.

        A test that says `partial` has measured less than the same test did on a luckier
        run — one side of a pair, one branch of a fork. It must never outrank a complete
        result, for the same reason `measured = false` must not: the tool would be
        choosing the weaker evidence and calling it the answer.
        """
        return isinstance(self.value, dict) and bool(self.value.get("partial"))

    @property
    def eyeball(self) -> bool:
        """A human's answer to a shown stimulus, not an instrument's reading.

        The right evidence for a question with no programmatic oracle, and the wrong
        evidence for anything measurable — which is why it is a field and not a
        convention. Nothing may silently promote one to the other.
        """
        return self.source == "eyeball"

    @property
    def outcome(self) -> str:
        """What the run actually recorded — the ONLY thing rendered beside `expect`."""
        if self.status == "ok":
            return render_value(self.value)
        if self.status == "error":
            return self.err or "(errored, no message)"
        return self.why or "(no reason recorded)"

    @property
    def declined(self) -> bool:
        """The test RAN but reported it could not measure — `{measured = false, why = …}`.

        Status is `ok` for these, because the test itself worked; only its own value says
        nothing was observed. So status alone cannot rank two runs of one test, and a
        declined result must never outrank a real measurement when picking what to drain.
        """
        return isinstance(self.value, dict) and self.value.get("measured") is False


@dataclass
class Run:
    """One `/clab run`, from either store."""
    label: str
    started: str = "?"
    version: str = "?"
    interface: str = "?"
    combat: bool = False
    instance: str = "?"
    source: str = "?"
    legacy: bool = False
    meta: dict = field(default_factory=dict)
    results: list[Result] = field(default_factory=list)

    def counts(self) -> dict:
        """`ok` means ANSWERED — a declined row is counted apart, never as a pass.

        The wire keeps `status = "ok"` for a declined row because the TEST worked; only
        its value says nothing was observed. Folding the two together is what let a run
        report `ok 55 / error 0 / skipped 0` while three tests measured nothing.
        """
        out = {"ok": 0, "error": 0, "skipped": 0, "declined": 0}
        for r in self.results:
            key = "declined" if r.declined else r.status
            out[key] = out.get(key, 0) + 1
        return out

    @property
    def header(self) -> str:
        bits = [f"# run {self.label}  {self.started}  v{self.version}",
                f"iface {self.interface}",
                f"combat={str(self.combat).lower()}",
                f"instance={self.instance}"]
        for k in sorted(self.meta):
            bits.append(f"{k}={self.meta[k]}")
        return "  ".join(bits)


def _results_from_legacy(raw) -> list[Result]:
    out = []
    for r in capture._aslist(raw):
        r = capture._asdict(r)
        out.append(Result(
            id=r.get("id", "?"), status=r.get("status", "?"), anchor=r.get("anchor", ""),
            bucket=r.get("bucket", ""), question=r.get("question", ""),
            value=r.get("value"), err=str(r.get("err", "")), why=str(r.get("why", "")),
        ))
    return out


def load_legacy(wow_path: str = DEFAULT_WOW) -> list[Run]:
    """`ClientLabDB.runs.{ooc,combat}` — the bespoke two-slot store that predates §2.

    Kept as a reader after the migration so a SavedVariables file written by an older
    build stays readable instead of silently reporting "no runs". It is reported AS
    legacy, never merged into the capture stream.
    """
    pth = capture.find_savedvar("ClientLab", wow_path)
    if not pth:
        return []
    db = parse_savedvar(Path(pth).read_text(encoding="utf-8", errors="replace"),
                        "ClientLabDB")
    if not isinstance(db, dict):
        return []
    runs = capture._asdict(db.get("runs"))
    out: list[Run] = []
    for slot in ("ooc", "combat"):
        raw = capture._asdict(runs.get(slot))
        if not raw:
            continue
        out.append(Run(
            label=slot, started=str(raw.get("at", "?")), version=str(raw.get("version", "?")),
            interface=str(raw.get("interface", "?")),
            combat=bool(raw.get("combat")), instance=str(raw.get("instance", "?")),
            source=f"ClientLabDB.runs.{slot}  ({pth})", legacy=True,
            results=_results_from_legacy(raw.get("results")),
        ))
    return out


def load_capture(wow_path: str = DEFAULT_WOW) -> list[Run]:
    """The `runs` capture stream, split into one Run per `/clab run`.

    A session is one addon load and holds SEVERAL runs — the whole point of the ring
    over the old two named slots is that an OOC run and a combat run in the same
    session no longer overwrite each other. So rows are grouped by their `run`
    ordinal, not by session, and the stamps come off the ROWS: a session-level
    `combat` could only ever describe one of the runs it contains.
    """
    cap = capture.load("clab", wow_path)
    if cap is None or "runs" not in cap.streams():
        return []
    out: list[Run] = []
    for i, s in enumerate(cap.sessions("runs"), 1):
        groups: dict[object, list[dict]] = {}
        for r in s.rows:
            groups.setdefault(r.get("run", 1), []).append(r)
        meta = dict(s.meta)
        meta.pop("runs", None)
        interface = str(meta.pop("interface", "?"))
        for key in sorted(groups, key=lambda k: (isinstance(k, str), k)):
            rows = groups[key]
            first = rows[0]
            results = [Result(
                id=str(r.get("id", "?")), status=str(r.get("status", "?")),
                anchor=str(r.get("anchor", "")), bucket=str(r.get("bucket", "")),
                value=r.get("value"), err=str(r.get("err", "")), why=str(r.get("why", "")),
                source=str(r.get("source", "measured")), at=str(r.get("at", "")),
            ) for r in rows]
            combat = bool(first.get("combat"))
            out.append(Run(
                label=f"s{i}/run {key} ({'combat' if combat else 'ooc'})",
                started=str(first.get("at", s.started)), version=str(s.version),
                interface=interface, combat=combat,
                instance=str(first.get("instance", "?")),
                source=f"ClientLabDB.captures.runs[{i}]  ({cap.path})",
                meta={"spec": first.get("spec", "?"), "hero": first.get("hero", "?")},
                results=results,
            ))
    return out


def load_runs(wow_path: str = DEFAULT_WOW) -> list[Run]:
    """Every readable run, capture stream first, then the legacy slots.

    Both are returned rather than one shadowing the other: during the migration a file
    holds both, and silently preferring one would hide a run somebody is looking for.
    """
    return load_capture(wow_path) + load_legacy(wow_path)


# ------------------------------------------------------------------------ `show`


WIDTH = 94


def _wrap(text: str, label: str, indent: int = 10) -> list[str]:
    """`label` then wrapped body, hanging-indented so the columns line up."""
    pad = " " * indent
    body = textwrap.wrap(" ".join(str(text).split()), WIDTH - indent) or [""]
    head = f"  {label:<{indent - 2}}{body[0]}"
    return [head] + [pad + ln for ln in body[1:]]


def _render_result(r: Result, q: dict | None, verbose: bool) -> list[str]:
    anchor = r.anchor or (q or {}).get("anchor", "")
    bucket = r.bucket or (q or {}).get("bucket", "")
    out = [f"{r.id:<38} {anchor}  [{bucket}]".rstrip()]
    if q is None:
        out.append("  ⚠ NOT IN questions.json — a result with no registry row. "
                   "Register it or delete the test.")
    else:
        if verbose:
            out += _wrap(q.get("question", ""), "Q")
        out += _wrap(q.get("expect", "(no expect recorded)"), "expect")
    out += _wrap(r.outcome, "EYEBALL" if r.eyeball else
                 ("DECLINED" if r.declined else
                  ("result" if r.status == "ok" else r.status)))
    if r.eyeball:
        out.append("  ^ a HUMAN answered this after being shown a stimulus. "
                   "Not an instrument reading.")
    if r.stamps:
        out.append("  " + "  ".join(f"{k}={r.stamps[k]}" for k in sorted(r.stamps)))
    if q is not None and q.get("status") == "answered":
        a = q.get("answered", {})
        out.append(f"  (already drained — {a.get('obs', '?')}, run {a.get('run', '?')})")
    return out


def cmd_show(args) -> int:
    _, byid = load_questions()
    runs = load_runs(args.wow_path)
    if not runs:
        print(f"no ClientLab run found under {args.wow_path}/WTF/Account/", file=sys.stderr)
        print("  run /clab run in game, then /reload — SavedVariables only flush then.",
              file=sys.stderr)
        return 1

    if args.slot:
        runs = [r for r in runs if args.slot in r.label.lower()
                or (args.slot == "combat" and r.combat)
                or (args.slot == "ooc" and not r.combat)]
        if not runs:
            print(f"no run matching slot '{args.slot}'", file=sys.stderr)
            return 1

    for run in runs:
        print()
        print(run.header)
        print(f"#   source: {run.source}")
        if run.legacy:
            print("#   ⚠ LEGACY two-slot store (pre-capture-standard). Nothing here is "
                  "stamped with spec/hero,")
            print("#     and a second run in the same slot CLOBBERED the first — so this "
                  "is one run, not a history.")
        c = run.counts()
        print(f"#   ok {c.get('ok', 0)} / declined {c.get('declined', 0)} / "
              f"error {c.get('error', 0)} / skipped {c.get('skipped', 0)}")

        wanted = [r for r in run.results if not args.id or r.id == args.id]
        if args.id and not wanted:
            print(f"  (no result for '{args.id}' in this run)")
            continue

        for status in ("ok", "declined", "error", "skipped"):
            if status == "declined":
                group = [r for r in wanted if r.declined]
            else:
                group = [r for r in wanted if r.status == status and not r.declined]
            if not group:
                continue
            print()
            if status == "skipped":
                print(f"── skipped ({len(group)}) "
                      "── ⚠ SKIPPED IS NEVER A PASS: the precondition was unmet "
                      "and NOTHING was measured")
            elif status == "declined":
                print(f"── declined ({len(group)}) "
                      "── ⚠ DECLINED IS NEVER A PASS EITHER: the test ran and "
                      "observed NOTHING")
            else:
                print(f"── {status} ({len(group)}) " + "─" * (WIDTH - 10 - len(status)))
            for r in group:
                print()
                for ln in _render_result(r, byid.get(r.id), args.id or args.verbose):
                    print(ln)

        other = [r for r in wanted if r.status not in ("ok", "error", "skipped")]
        for r in other:
            print()
            print(f"  ⚠ unknown status '{r.status}' for {r.id}")

    if not args.id:
        print()
        ran = {r.id for run in runs for r in run.results}
        tested = [i for i in tested_question_ids() if i not in ran]
        if tested:
            print(f"# {len(tested)} question(s) with a test but no result in any run "
                  f"above: {', '.join(sorted(tested))}")
        print("# NO VERDICT IS PRINTED, BY DESIGN. Read result beside expect and decide;")
        print("# then `uv run python -m wowkb.lab drain <id>` mints the observation "
              "that carries it into the KB.")
    return 0


# ----------------------------------------------------------------------- `drain`


def next_obs_id(text: str) -> str:
    nums = [int(m) for m in re.findall(r"^## OBS-(\d+)", text, re.M)]
    return f"OBS-{(max(nums) + 1 if nums else 1):03d}"


def _anchor_context(anchor: str, span: int = 2) -> list[str]:
    """The KB lines an anchor points at — so the drain prints the text to be rewritten."""
    m = re.match(r"^(.*?):(\d+)$", anchor)
    if not m:
        return [f"  (anchor '{anchor}' is not <file>:<line>)"]
    # Anchors are relative to knowledge/addon-dev/, and a few point OUT of it with
    # `../../` (traitconfig-fires-on-hero-swap parks in the game KB's inbox).
    path = (KB / m.group(1)).resolve()
    if not path.exists():
        return [f"  (no such file: {m.group(1)})"]
    n = int(m.group(2))
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for i in range(max(1, n - span), min(len(lines), n + span) + 1):
        mark = ">>" if i == n else "  "
        out.append(f"  {mark} {i:>5}  {lines[i - 1]}")
    return out


def cmd_drain(args) -> int:
    data, byid = load_questions()
    q = byid.get(args.id)
    if not q:
        # A drained question's row is removed (wipe-on-answer), so a missing id is either a
        # typo or an already-drained question — whose OBS in observations.md is the record.
        print(f"error: no question '{args.id}' in questions.json — a typo, or already "
              "drained (the row is removed on drain; its OBS in observations.md is the "
              "record).", file=sys.stderr)
        return 1

    visual = bool(_EYEBALL.search(f"{q.get('expect', '')}\n{q.get('question', '')}"))
    runs = load_runs(args.wow_path)
    hits = [(run, r) for run in runs for r in run.results
            if r.id == args.id and (not args.slot or args.slot in run.label.lower())]
    if not hits and not (visual and args.verdict):
        print(f"error: no stored result for '{args.id}' — has it been flown?",
              file=sys.stderr)
        return 1

    eyeballs = [h for h in hits if h[1].eyeball]
    if visual and eyeballs:
        # A person may answer the same stimulus several times — the panel says as much
        # ("answering again replaces it"), so the LAST answer is the one that counts.
        # `hits` is in run order, so the last eyeball hit is the latest.
        run, res = eyeballs[-1]

        # Disagreement is never resolved silently. Picking the verdict that happens to
        # be drainable would be the tool choosing the answer it prefers, which is the
        # exact failure the eyeball channel exists to avoid.
        given = [h[1].verdict for h in eyeballs]
        distinct = sorted({v for v in given if v})
        if len(distinct) > 1:
            print(f"⚠ {args.id} has {len(given)} verdicts and they DISAGREE:",
                  file=sys.stderr)
            for r_, s_ in eyeballs:
                print(f"    {s_.at or r_.started}  {s_.verdict}", file=sys.stderr)
            print(f"  Taking the latest ({res.verdict}). If that is not what you meant, "
                  "re-answer in game", file=sys.stderr)
            print("  and drain again — do not hand-edit the capture.", file=sys.stderr)
        if res.undecided:
            print(f"REFUSED: the latest verdict for {args.id} is "
                  f"'{res.verdict}' — that declines to answer.", file=sys.stderr)
            print("  'can't tell' is a finding about the STIMULUS, not about the "
                  "question. Fix what is shown", file=sys.stderr)
            print("  so the answer is unambiguous, then re-answer.", file=sys.stderr)
            return 2
    else:
        # Prefer a run that answered. Ways a run can fail to, in order of badness:
        # `skipped` (precondition gate), `measured=false` (ran, observed nothing),
        # `error`. None may shadow a real answer in another run.
        hits.sort(key=lambda h: (h[1].status == "skipped", h[1].declined,
                                 h[1].status == "error", h[1].partial))
        run, res = hits[0] if hits else (None, None)

    # An authored verdict: the human answered in PROSE instead of pressing the panel's
    # option button. Same evidence class (a person decided), different channel — added
    # 2026-08-24 when the click requirement proved to be ceremony: the author had already
    # stated the verdict, with a screenshot, and the tool was refusing it over which
    # surface the words arrived on. A recorded click still wins over --verdict, because
    # the click is bound to the exact stimulus text and prose is not.
    authored = bool(visual and args.verdict and not (eyeballs and res is not None
                                                     and res.eyeball))
    if args.verdict and eyeballs:
        print("note: a recorded panel click exists — using it; --verdict ignored.",
              file=sys.stderr)

    if visual and not authored and (res is None or not res.eyeball):
        print(f"REFUSED: {args.id}'s `expect` says only an eyeball closes it, and no "
              "eyeball verdict is on record.", file=sys.stderr)
        print("  A visual question can never go green off a programmatic run. Either "
              "answer the panel in game", file=sys.stderr)
        print("  (/clab -> `visual checks`) or state the verdict here: "
              "drain <id> --verdict '<what you saw>'.", file=sys.stderr)
        return 2

    if res is not None and not authored and res.status == "skipped":
        print(f"REFUSED: {args.id} is `skipped` in every stored run — "
              "SKIPPED IS NEVER A PASS.", file=sys.stderr)
        print(f"  why: {res.why}", file=sys.stderr)
        print("  Nothing was measured. Fly it with its precondition met, then drain.",
              file=sys.stderr)
        return 2

    if res is not None and not authored and res.declined:
        why = res.value.get("why") if isinstance(res.value, dict) else None
        print(f"REFUSED: {args.id} reports `measured = false` in every stored run.",
              file=sys.stderr)
        print(f"  why: {why or '(none recorded)'}", file=sys.stderr)
        print("  The test ran but observed nothing, which is not an answer. Fly it with "
              "its precondition met.", file=sys.stderr)
        return 2

    stamp = run.started.split()[0] if run and run.started and run.started != "?" \
        else date.today().isoformat()
    obs_text = OBS.read_text(encoding="utf-8")
    obs_id = next_obs_id(obs_text)

    anchors = [q["anchor"]] + list(q.get("also", []))
    title = args.title or (q.get("question", args.id).split("?")[0].strip()[:88])

    entry = [
        "",
        "---",
        "",
        f"## {obs_id} · {date.today().isoformat()} · {title}",
        "",
        (f"**Observed:** `{args.id}` — a **HUMAN VERDICT, reported in prose**: "
         f"{args.verdict}"
         if authored else
         f"**Observed:** `{args.id}` — a **HUMAN VERDICT**: `{res.outcome}`"
         if res.eyeball else
         f"**Observed:** `{args.id}` recorded **{res.status}** — `{res.outcome}`"),
        "",
        ("**How:** the author looked at the ClientLab stimulus and stated the verdict "
         "in conversation (`drain --verdict`) rather than pressing the panel's option "
         "button"
         + (f", beside run **{run.started}** (v{run.version}, interface "
            f"{run.interface}), {'in combat' if run.combat else 'out of combat'}"
            if run else "")
         + ". ⚠ **This is an eyeball verdict, not an instrument reading** — the only "
         "evidence class that can close this question, and it must never be cited as a "
         "measurement. The prose here is the record; no runs-stream row exists for it."
         if authored else
         f"**How:** ClientLab showed a stimulus and a person answered, "
         f"**{run.started}** (v{run.version}, interface {run.interface}), "
         f"{'in combat' if run.combat else 'out of combat'}, instance `{run.instance}`. "
         "⚠ **This is an eyeball verdict, not an instrument reading** — it is the only "
         "evidence class that can close this question, and it must never be cited as a "
         "measurement."
         if res.eyeball else
         f"**How:** ClientLab run **{run.started}** (v{run.version}, interface "
         f"{run.interface}), {'in combat' if run.combat else 'out of combat'}, instance "
         f"`{run.instance}`. A direct measurement in the client."),
        "",
        f"**Expected (questions.json):** {q.get('expect', '(none recorded)')}",
        "",
        "**Confidence:** high — the client answered directly. Low only if the result "
        "contradicts `expect` in a way that suggests the test asked the wrong thing.",
        "",
        f"**Drains to:** {', '.join(f'`{a}`' for a in anchors)}",
        "",
        "**Status:** open",
    ]
    OBS.write_text(obs_text.rstrip("\n") + "\n" + "\n".join(entry) + "\n", encoding="utf-8")

    # Wipe-on-answer: the drained row is REMOVED, not retained as `answered`. The OBS minted
    # above plus git together archive the question, its `expect`, the run and the verdict, so
    # the row was pure duplication; questions.json stays a live worklist of OPEN questions.
    data["questions"] = [x for x in data["questions"] if x.get("id") != args.id]
    # indent=1 matches the file as authored — a drain must produce a one-question diff,
    # not a whole-file reformat that buries what changed.
    QUESTIONS.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                         encoding="utf-8")

    print(f"{obs_id} minted in knowledge/addon-dev/observations.md "
          f"(tag `[client {stamp}]`)")
    print(f"  questions.json: {args.id} -> REMOVED "
          f"(OBS {obs_id} + git archive the question; "
          + (f"run {run.started}, v{run.version}" if run else "authored verdict, no run")
          + ")")
    print()
    if authored:
        print(f"  verdict (prose): {args.verdict}")
    elif res.eyeball:
        asked = res.value.get("asked") if isinstance(res.value, dict) else None
        print(f"  verdict:  {res.verdict}")
        print(f"  asked:    {asked or '(not recorded)'}")
        print("  ^ CHECK THIS MATCHES THE QUESTION YOU ARE DRAINING. The stimulus text is")
        print("    recorded with every verdict precisely so a mis-bound button is visible.")
    else:
        print(f"  measured: {res.outcome}")
    print()
    print("NOW EDIT THE TOPIC FILE — this is the part no tool can do for you:")
    for a in anchors:
        print()
        print(f"  {a}")
        for ln in _anchor_context(a):
            print(ln)
    print()
    print("  1. REWRITE THE CLAIM IN PLACE to say what was measured.")
    print("     Never a correction note left under standing wrong text "
          "(addon-dev/README.md §7 rule 1).")
    print("  2. DROP the marker — `@pending-test` / `@verify-ingame` / `[gap]`. "
          "It is answered now.")
    print(f"  3. TAG it `[client {stamp}]` — THE DATE OF THE RUN, not today.")
    print(f"  4. DELETE THE TEST from ClientLab — every `{args.id}` declaration, and the")
    print("     file plus its .toc line if that was the last test in it. House rule 2: "
          "probe code dies")
    print("     in the edit that writes its claim. `deploy --check` fails by name until "
          "you do.")
    print(f"  5. Then: uv run python -m wowkb.obs drain {obs_id}")
    return 0


# --------------------------------------------------------------------- `blocked`


def cmd_blocked(args) -> int:
    data, _ = load_questions()
    groups: dict[str, list[dict]] = {}
    for q in data["questions"]:
        if q.get("status") == "answered":
            continue
        if "blocked_on" not in q:
            continue
        groups.setdefault(q["blocked_on"] or "", []).append(q)

    if not groups:
        print("no open question records a `blocked_on`.")
        return 0

    print("# what the open registry is actually waiting on — the residue is a list of")
    print("# MISSING CAPABILITIES, not a list of stuck questions.")
    free = groups.pop("", [])
    for blocker in sorted(groups, key=lambda b: (-len(groups[b]), b)):
        rows = groups[blocker]
        print()
        print(f"── {blocker}  ({len(rows)})")
        for q in rows:
            print(f"     {q['status']:<14} {q['id']:<38} {q.get('anchor', '')}")
    if free:
        print()
        print(f"── nothing — simply not needed yet  ({len(free)})")
        for q in free:
            print(f"     {q['status']:<14} {q['id']:<38} {q.get('anchor', '')}")
    print()
    print(f"# {len(groups)} missing capability/ies across "
          f"{sum(len(v) for v in groups.values())} question(s)"
          f"{f', plus {len(free)} needing nothing at all' if free else ''}.")
    print("# NOTHING HERE IS OVERDUE. Parked has no clock, no cap and no release gate — "
          "that is the point.")
    return 0


# ---------------------------------------------------------------------- `deploy`


def luacheck() -> tuple[bool, list[str]]:
    """Lint the lab's Lua before it can reach the client.

    ⚠ THIS EXISTS BECAUSE THE GAME WAS THE LINTER. Measured 2026-08-21: an edit to `Ask.lua`
    deleted a constant and left two uses of it behind; `deploy` copied the file, and the first
    thing to notice was `attempt to perform arithmetic on global 'OPTION_AREA' (a nil value)`
    thrown at the person trying to answer a visual check. The same pass also left a test
    filtering an aura slot on a table keyed by a STRING, which matches nothing forever and is
    indistinguishable from a refused slot — the one failure this whole suite is built to avoid.

    `luac -p` would not have caught either: both are syntactically fine. Undefined globals and
    unused locals are exactly what luacheck reads, and `.luacheckrc` beside the addon already
    declares the WoW environment. A missing luacheck is reported and does NOT block — a linter
    nobody has installed must not stop a deploy — but a FAILING one does.
    """
    rc = SRC.parent / ".luacheckrc"
    if shutil.which("luacheck") is None:
        return True, ["luacheck not on PATH — skipped (install it: the game is the fallback "
                      "linter and it reports at the worst possible moment)"]
    # `-q` drops the per-file OK lines. Without it a single bad file reports behind nine good
    # ones and the actual message scrolls off — which is how a linter gets ignored.
    cmd = ["luacheck", "-q", str(SRC)] + (["--config", str(rc)] if rc.exists() else [])
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(SRC.parent))
    if proc.returncode == 0:
        return True, ["luacheck clean"]
    lines = [ln.rstrip() for ln in (proc.stdout or proc.stderr).splitlines() if ln.strip()]
    return False, ["luacheck FAILED — not deploying:"] + lines[:20]


def deploy(wow_path: str) -> tuple[bool, str]:
    """Mirror ClientLab/ into <wow>/Interface/AddOns/ClientLab/ (deletions too)."""
    dest_root = Path(wow_path) / "Interface" / "AddOns"
    if not dest_root.exists():
        return False, (f"AddOns directory not found: {dest_root}\n"
                       "Is --wow-path pointing at a real _retail_ install?")
    dest = dest_root / "ClientLab"
    # A clean copy mirrors deletions without a per-file diff: remove the addon's
    # own folder (and nothing else) then copy the source tree in whole.
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC, dest)
    n = sum(1 for _ in dest.glob("*.lua"))
    return True, f"deployed {n} Lua files -> {dest}"


def cmd_deploy(args) -> int:
    ok, msgs = cross_check()
    for m in msgs:
        print(("  " if ok else "ERROR: ") + m, file=(sys.stdout if ok else sys.stderr))
    if not ok:
        print("registry cross-check FAILED — not deploying.", file=sys.stderr)
        return 1

    lok, lmsgs = luacheck()
    for m in lmsgs:
        print(("  " if lok else "ERROR: ") + m, file=(sys.stdout if lok else sys.stderr))
    if not lok:
        return 1

    if args.check:
        return 0

    dok, dmsg = deploy(args.wow_path)
    print(("  " if dok else "ERROR: ") + dmsg, file=(sys.stdout if dok else sys.stderr))
    if dok:
        print("  in-game: /reload, and that is all — the lab runs itself (OOC after login, "
              "again on combat entry,")
        print("           then retries whatever could not answer while the pull lasts). "
              "Pull something.")
        print("  /clab opens the panel: [copy] takes an answer out mid-pull with no reload.")
    return 0 if dok else 1


def main(argv=None) -> int:
    # --wow-path is shared, and accepted on EITHER side of the subcommand: the old
    # single-command CLI put it after `deploy`, and that spelling still has to work.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--wow-path", default=DEFAULT_WOW,
                        help=f"WoW _retail_ path (default: {DEFAULT_WOW})")

    ap = argparse.ArgumentParser(
        prog="python -m wowkb.lab", parents=[common],
        description="Deploy the ClientLab scratch addon, read its runs, drain answers.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("deploy", parents=[common],
                       help="cross-check the registry, then copy the addon in")
    p.add_argument("--check", action="store_true",
                   help="run the registry cross-check only; do not copy files")
    p.set_defaults(fn=cmd_deploy)

    p = sub.add_parser("show", parents=[common],
                       help="render each result BESIDE its expect (no verdict)")
    p.add_argument("--id", help="one question, with its full text")
    p.add_argument("--slot", choices=["ooc", "combat"], help="only runs of this kind")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="include each question's full text, not just expect")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("drain", parents=[common],
                       help="mint the observation that carries an answer to the KB")
    p.add_argument("id", help="question id, as in questions.json")
    p.add_argument("--slot", choices=["ooc", "combat"], help="drain from this run")
    p.add_argument("--title", help="observation heading (default: from the question)")
    p.add_argument("--verdict", help="the author's eyeball verdict, stated in prose — "
                   "closes a visual question WITHOUT a recorded panel click. The human "
                   "requirement stands; the in-game button does not. Ignored when a "
                   "recorded click exists (the click wins).")
    p.add_argument("--again", action="store_true",
                   help="mint a second observation for an already-answered question")
    p.set_defaults(fn=cmd_drain)

    p = sub.add_parser("blocked", parents=[common],
                       help="open rows grouped by what they are waiting on")
    p.set_defaults(fn=cmd_blocked)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

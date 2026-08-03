"""Extract the CDMProbe pipeline DECISION LOG off the WoW SavedVariables file.

The probe (`/cdmp probe` + probe-baseline.json assertions) was retired 2026-07-29:
the secret-values / readability rules it discovered are settled game-wide invariants,
and a spec's tracked set comes from wago DB2 (`wowkb.spec_inventory`), so per-spec
re-measurement bought nothing. What remains is the always-on decision log — the
greppable pipeline trace this module flattens.

WHAT WE READ:

    CDMProbeDB.decisionlog   <- a ring of the last 3 sessions, each a list of one-line
                                `S{…} G{…} B{…}` pipeline traces appended on every
                                DECISION CHANGE (addon DecisionLog.lua).

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale almost
always means the /reload was skipped.

    CDMProbeDB.alerttape     <- ⚠ TEMPORARY. The CDM alert-channel discovery tape
                                (addon AlertTape.lua): per session an `elig` eligibility
                                baseline, an `events` tape of every TriggerAlertEvent, and
                                a `fields` three-way readability probe of the pandemic
                                fields. Delete this half of the module with AlertTape.lua
                                once the rules land in knowledge/addon-dev/
                                api-events-and-discovery.md §2.8.

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale almost
always means the /reload was skipped.

Usage:
    uv run python -m wowkb.cdmp decisionlog                 # → raw/cdmp-decision.log
    uv run python -m wowkb.cdmp decisionlog --out my.log
    uv run python -m wowkb.cdmp decisionlog --wow-path <dir>
    uv run python -m wowkb.cdmp alerttape                   # → raw/cdmp-alerttape.log
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

from .charstate import DEFAULT_WOW, parse_savedvar

REPO_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Loading (mirrors diagnostics.py one-for-one)                                 #
# --------------------------------------------------------------------------- #

def _find_savedvar(wow_path: str) -> str | None:
    """Newest CDMProbe.lua under any account's SavedVariables (mtime desc)."""
    pattern = f"{wow_path}/WTF/Account/*/SavedVariables/CDMProbe.lua"
    hits = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


def _aslist(v) -> list:
    """The Lua parser yields a Python list for a non-empty positional table but an
    empty dict for `{}`, and an int-keyed dict for a sparse array — normalize all
    three to a list."""
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        return [v[k] for k in sorted(v)] if v else []
    return []


def _asdict(v) -> dict:
    return v if isinstance(v, dict) else {}


def load_decisionlog(wow_path: str) -> tuple[object, str] | None:
    """(decisionlog, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (db.get("decisionlog"), pth)


# --------------------------------------------------------------------------- #

def cmd_decisionlog(decisionlog, path: str, out: Path) -> int:
    """Flatten the pipeline decision log to a grep-friendly .log file.

    Each session is written newest-last, headed by a `# session … tracked:…` line and
    then one entry per line. Real line numbers fall out for `grep -n`. The parser already
    un-escapes the entries (each is a single quote-free line by format), so there is
    nothing to un-escape here.
    """
    sessions = _aslist(decisionlog)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    total = 0
    # The addon stamps `# config <spec> hero:<hero> tracked:<codes>` into the entry stream
    # whenever the configuration CHANGES, so a mid-session spec or hero-tree swap is marked
    # in place.  Collected here as well, because a swap 400 lines into a trace is invisible
    # unless you already suspect it — and the whole point of asking is that you might not.
    configs: list[str] = []
    # THE COMBAT SPLIT (addon v0.32.75+).  `w:-` — the Coach found no winner — is the
    # acceptance signal for the v0.32.36 re-fly, and it is only meaningful IN A PULL: out of
    # combat "no winner" is the CORRECT answer, so idle time inflates the raw ratio without
    # anything being wrong.  The 2026-08-01 capture measured 53.6 % across 21,048 lines and
    # that number was unreadable for exactly this reason.  The addon now stamps
    # `# combat start` / `# combat end` on the edge, above its own change-only dedup, and
    # this is the consumer.
    #
    # ⚠ A CAPTURE WITH NO MARKERS IS REPORTED UNREADABLE, NEVER AS 0 %.  Entries are stored
    # PRE-RENDERED, so combat cannot be recovered from an older capture — and silently
    # scoring one would hand back a confident wrong answer, which is the whole failure this
    # change exists to end.
    split: list[dict] = []
    for session in sessions:
        s = _asdict(session)
        entries = _aslist(s.get("entries"))
        lines.append(
            f"# session {s.get('started', '?')} v{s.get('version', '?')} "
            f"tracked:{s.get('tracked', '?')}")
        # None until the session's first `# combat` marker: lines before it are of unknown
        # combat state and are counted separately rather than guessed into a bucket.
        in_combat: bool | None = None
        tally = {"started": s.get("started", "?"), "version": s.get("version", "?"),
                 "marked": False,
                 "in": 0, "in_nowin": 0, "out": 0, "out_nowin": 0, "unknown": 0}
        for e in entries:
            text = str(e)
            lines.append(text)
            if "# config " in text:
                configs.append(f"{s.get('started', '?')}  {text}")
            if "# combat " in text:
                tally["marked"] = True
                in_combat = text.rstrip().endswith("start")
            elif "S{" in text:
                nowin = "G{w:-" in text
                if in_combat is None:
                    tally["unknown"] += 1
                elif in_combat:
                    tally["in"] += 1
                    tally["in_nowin"] += nowin
                else:
                    tally["out"] += 1
                    tally["out_nowin"] += nowin
            total += 1
        split.append(tally)
    if configs:
        lines.append("")
        lines.append("# ── CONFIG SEGMENTS (each is a spec / hero-tree / talent change) ────")
        lines += ["# " + c for c in configs]
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"{path}")
    print(f"{len(sessions)} session(s) · {total} line(s) → {out}")
    if configs:
        print(f"{len(configs)} config segment(s) — the trace spans more than one build:")
        for c in configs:
            print("  " + c)

    print()
    print("# ── COMBAT SPLIT · `w:-` (no winner) is only meaningful IN COMBAT ──")
    for t in split:
        head = f"  {t['started']} v{t['version']}"
        if not t["marked"]:
            print(f"{head}  UNREADABLE — no `# combat` markers "
                  f"({t['unknown']} decision line(s)). Capture predates addon v0.32.75; "
                  f"entries are stored pre-rendered, so this cannot be recovered — re-fly.")
            continue
        pct = (100.0 * t["in_nowin"] / t["in"]) if t["in"] else None
        inc = (f"{t['in_nowin']}/{t['in']} = {pct:.1f}%" if pct is not None
               else "no in-combat lines — nothing was pulled")
        print(f"{head}  IN COMBAT w:- {inc}"
              f"   ·   out of combat {t['out_nowin']}/{t['out']}"
              + (f"   ·   {t['unknown']} pre-marker" if t["unknown"] else ""))
    return 0


# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# alerttape — the TEMPORARY CDM alert-channel discovery instrument               #
# --------------------------------------------------------------------------- #
# ⚠ Delete this section with the addon's AlertTape.lua once the alert-channel rules are
# settled in knowledge/addon-dev/api-events-and-discovery.md §2.8. It is a one-question
# instrument, not a permanent recorder.

def load_alerttape(wow_path: str) -> tuple[object, str] | None:
    """(alerttape, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    db = parse_savedvar(Path(pth).read_text(encoding="utf-8", errors="replace"), "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (db.get("alerttape"), pth)


def _rows(store) -> list[dict]:
    """The addon keys both channels by a dedup string, so SavedVariables yields a dict of
    row-dicts (not a positional array). Normalize either shape to a list of dicts."""
    if isinstance(store, dict):
        return [v for v in store.values() if isinstance(v, dict)]
    if isinstance(store, list):
        return [v for v in store if isinstance(v, dict)]
    return []


def cmd_alerttape(alerttape, path: str, out: Path) -> int:
    """Flatten the alert tape, newest session last.

    Two channels per session, and they answer different questions:
      EV  — did this alert type fire at all, in or out of combat, and how often
      FLD — the three-way READABILITY class of the pandemic fields (num/bool/SECRET/nil/
            threw). `SECRET` and `nil` mean very different things and are never merged.

    Read the EV rows for Available/OnCooldown FIRST: those are the control group. If they
    are present and PandemicTime is not, the instrument is live and the absence is a real
    finding; if nothing is present, the capture proves nothing (tape off, HUD off, or no
    /reload).
    """
    sessions = _aslist(alerttape)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    builds: set[str] = set()
    ev_total = fld_total = elg_total = 0
    for session in sessions:
        s = _asdict(session)
        lines.append(f"# session {s.get('started', '?')} v{s.get('version', '?')} "
                     f"build-at-open={s.get('build', '?')}")

        # ELG — the eligibility baseline, captured automatically when the session opened.
        # Read this FIRST: without it, "PandemicTime never appeared" is unreadable, because
        # you cannot tell "it fired and we missed it" from "this spell was never eligible".
        if s.get("eligError"):
            lines.append(f"ELG <unavailable: {s['eligError']}>")
        # ⚠ SORTED BY BUILD FIRST, always.  The tape keeps recording across a spec or
        # hero-tree swap when there is no /reload, so one session can hold two builds — and
        # a cooldownID shared between them is a DIFFERENT row per build.  Reading them
        # interleaved is how you conclude the client is nondeterministic when you simply
        # respecced.
        elgs = _rows(s.get("elig"))
        elgs.sort(key=lambda r: (str(r.get("build")), str(r.get("viewer")), r.get("cid") or 0))
        for r in elgs:
            lines.append(
                f"ELG [{r.get('build')}] cid={r.get('cid')} spell={r.get('spellID')} "
                f"[{r.get('viewer')}] {r.get('name')} :: {r.get('types')}")
            elg_total += 1
            builds.add(str(r.get("build")))

        evs = _rows(s.get("events"))
        evs.sort(key=lambda r: (str(r.get("build")), str(r.get("event")),
                                str(r.get("combat")), r.get("cid") or 0))
        for r in evs:
            lines.append(
                f"EV  [{r.get('build')}] cid={r.get('cid')} event={r.get('event')} "
                f"{r.get('combat')} n={r.get('n')} first={r.get('first')} last={r.get('last')}")
            ev_total += 1
            builds.add(str(r.get("build")))

        flds = _rows(s.get("fields"))
        flds.sort(key=lambda r: (str(r.get("build")), r.get("cid") or 0, str(r.get("combat"))))
        for r in flds:
            lines.append(
                f"FLD [{r.get('build')}] cid={r.get('cid')} {r.get('combat')} "
                f"on={r.get('event')} n={r.get('n')} class[{r.get('class')}] "
                f"sample[{r.get('sample')}]")
            fld_total += 1

    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"{path}")
    print(f"{len(sessions)} session(s) · {elg_total} eligibility row(s) · "
          f"{ev_total} event row(s) · {fld_total} field row(s) → {out}")
    known = sorted(b for b in builds if b not in ("None", "?"))
    if known:
        print("builds: " + ", ".join(known))
    if builds - set(known):
        # Rows written before the build tag existed (pre-v0.32.44) cannot be attributed.
        print("⚠ some rows carry NO build tag — captured by an older addon build; they "
              "cannot be attributed to a spec and may merge two.", file=sys.stderr)
    if ev_total == 0:
        print("\n⚠ No event rows. The capture proves NOTHING about the alert channel — "
              "check: /cdmp alerts on, /cdmp hud on, then a pull, then /reload.",
              file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #
# flight — the ACCEPTANCE REPORT                                                #
# --------------------------------------------------------------------------- #
# The other two subcommands FLATTEN a recorder and leave the reading to you. This one
# JUDGES, and that is the point of it: an in-game pass used to be a checklist of slash
# commands whose answers a human eyeballed in a chat dump, several of them typed during a
# GCD. The addon's `/cdmp flight` records the answers structurally; this turns them into
# PASS / FAIL / MEASURED lines against criteria that live in code.
#
# ⚠ THREE VERDICT KINDS, AND THEY ARE NOT THE SAME THING:
#   PASS/FAIL   an acceptance criterion with a known right answer
#   MEASURED    an open question whose whole point is that we do not know the answer
#               (the C_AssistedCombat rider). Never scored — a "failing" measurement is
#               just a result, and scoring it would invite someone to "fix" it.
#   SKIPPED     the flight never covered this (no combat sample, no spec swap). Loud,
#               because a criterion nobody exercised must never read as a pass.

def load_db(wow_path: str) -> tuple[dict, str] | None:
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    db = parse_savedvar(Path(pth).read_text(encoding="utf-8", errors="replace"), "CDMProbeDB")
    return (db, pth) if isinstance(db, dict) else None


# The Phase-4 acceptance criteria, per spec. `verdict` is what Coverage.Build must have
# concluded for that spellID; `absent` means the id must not be in the roster at all.
# ⚠ `29722 reads virtual` / `686 reads virtual` WERE CRITERIA HERE AND WERE WRONG (fixed
# 2026-08-01, off the first flight). They came from plan prose calling Incinerate and Shadow
# Bolt "the ids the CDM tracks nowhere", and that prose conflates two different facts:
#   * IN THE CDM DATABASE — `GetCooldownViewerCategorySet(…, allowUnlearned=true)` carries
#     the id. This is what `coverage` joins on, and Incinerate IS in it (1 row).
#   * DISPLAYED — a live viewer frame exists to anchor a cue to. Incinerate is NOT, which
#     is exactly why `HudVirtual` synthesises an icon for it.
# Coverage answers the first; the criteria were written as if it answered the second. The
# drawability question now lives in its own MEASURED section below, where it belongs — it
# depends on the viewers being up, so it is not something to fail a build over.
COVERAGE_EXPECT = {
    267: {  # Destruction
        "name": "Destruction",
        "absent": {417234: "Crashing Chaos (deleted in Phase 4 — redundant, not blind)"},
        "verdict": {
            434635: ("expected", "Ruination alt id — override-only by design"),
            434636: ("expected", "Ruination alt id — override-only by design"),
            132411: ("expected", "Singe Magic — the pet dispel override"),
            388215: ("expected", "Devour Magic — the pet dispel override"),
        },
        "not_blind": {29722: "Incinerate — the floor press must be covered somehow"},
        "tracked_rows": {428514: (4, "Diabolic Ritual — tracked across 4 cooldownIDs")},
    },
    266: {  # Demonology
        "name": "Demonology",
        "absent": {},
        "verdict": {},
        "not_blind": {686: "Shadow Bolt — the floor press must be covered somehow"},
        "tracked_rows": {},
    },
}


class Report:
    """Accumulates verdict lines and the exit code."""

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.failed = 0
        self.skipped = 0

    def head(self, text: str) -> None:
        self.lines.append("")
        self.lines.append(text)

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        self.lines.append(f"  {'PASS' if ok else 'FAIL'}  {label}"
                          + (f"   {detail}" if detail else ""))
        if not ok:
            self.failed += 1

    def skip(self, label: str, why: str) -> None:
        self.lines.append(f"  SKIP  {label}   {why}")
        self.skipped += 1

    def measured(self, label: str, value: str) -> None:
        self.lines.append(f"  ····  {label}   {value}")

    def note(self, text: str) -> None:
        self.lines.append(f"        {text}")


def _verdict_map(sample: dict) -> dict[int, dict]:
    """Per-id verdicts, with the pre-v0.32.54 rings NORMALISED.

    ⚠ COMPATIBILITY SHIM. `blind` originally ignored knownness, so a ring recorded before
    v0.32.54 marks an ability the character does not even HAVE as blind — which the first
    flight showed was 3 of 3 blind rows. The addon now emits `unlearned` itself; this
    re-derives it for rings already on disk, so an old capture is judged by the corrected
    rule rather than needing a re-fly. Delete once no pre-v0.32.54 ring matters.
    """
    out = {}
    for v in _aslist(_asdict(sample.get("cov")).get("verdicts")):
        if isinstance(v, dict) and v.get("id") is not None:
            v = dict(v)
            if v.get("v") == "blind" and v.get("known") is False:
                v["v"], v["relabelled"] = "unlearned", True
            elif v.get("v") == "blind" and v.get("known") is None:
                v["v"], v["relabelled"] = "unknown", True
            out[int(v["id"])] = v
    return out


def _recount(vm: dict[int, dict]) -> dict[str, int]:
    """Counts derived from the (possibly re-judged) verdict map, not from the recorded
    summary — otherwise the shim above would fix the detail and leave the totals lying."""
    out: dict[str, int] = {}
    for v in vm.values():
        out[v.get("v", "?")] = out.get(v.get("v", "?"), 0) + 1
    return out


def _check_coverage(rep: Report, samples: list[dict]) -> None:
    """Per spec, the first OUT-OF-COMBAT sample is the one the criteria are written for
    (in-combat rows are deliberately the stale cache, not a fresh read)."""
    by_spec: dict[int, dict] = {}
    for s in samples:
        spec = s.get("specID")
        cov = _asdict(s.get("cov"))
        if spec is None or s.get("combat") or not cov.get("ok"):
            continue
        by_spec.setdefault(int(spec), s)

    for specID, expect in COVERAGE_EXPECT.items():
        rep.head(f"Phase 4 — roster coverage · {expect['name']} ({specID})")
        sample = by_spec.get(specID)
        if sample is None:
            rep.skip("the whole spec", f"no out-of-combat sample for {expect['name']} — "
                                       "the flight never played this spec")
            continue
        cov = _asdict(sample.get("cov"))
        vm = _verdict_map(sample)
        n = _recount(vm)
        blind = n.get("blind", 0)
        rep.check(blind == 0, "0 BLIND",
                  f"({n.get('ok', 0)} tracked · {n.get('virtual', 0)} our own icons · "
                  f"{n.get('expected', 0)} override-only · {n.get('unlearned', 0)} unlearned · "
                  f"{blind} blind · {n.get('unknown', 0)} unknown, "
                  f"over {cov.get('scanned')} CDM rows)")
        relabelled = sorted(s for s, v in vm.items() if v.get("relabelled"))
        if relabelled:
            rep.note(f"{len(relabelled)} row(s) re-judged from a pre-v0.32.54 ring "
                     f"(blind -> unlearned/unknown on knownness): {relabelled}")
        for spell, v in sorted(vm.items()):
            if v.get("v") == "blind":
                rep.note(f"BLIND {spell} — the character HAS it and no CDM row carries it")
        for spell, why in expect["absent"].items():
            rep.check(spell not in vm, f"{spell} absent from the roster", why)
        for spell, (want, why) in expect["verdict"].items():
            got = vm.get(spell, {}).get("v")
            rep.check(got == want, f"{spell} reads {want}",
                      f"got {got or '<not in roster>'} — {why}")
        for spell, why in expect.get("not_blind", {}).items():
            got = vm.get(spell, {}).get("v")
            rep.check(got is not None and got != "blind", f"{spell} is not blind",
                      f"reads {got or '<not in roster>'} — {why}")
        for spell, (n, why) in expect["tracked_rows"].items():
            got = vm.get(spell, {})
            rows = got.get("n") or 0
            rep.check(got.get("v") == "ok" and rows >= n,
                      f"{spell} tracked across >= {n} rows", f"got {rows} — {why}")


def _check_combat_guard(rep: Report, samples: list[dict]) -> None:
    """THE most important check on the live path: in combat the coverage report must be
    the cached out-of-combat one marked stale, and must never invent blind rows."""
    rep.head("Phase 4 — the wholesale guard, in combat (the one that matters most)")
    combat = [s for s in samples if s.get("combat")]
    if not combat:
        rep.skip("in-combat coverage", "the flight never entered combat — pull a dummy")
        return
    for s in combat:
        spec = s.get("specID")
        cov = _asdict(s.get("cov"))
        prior = next((_asdict(p.get("cov")) for p in reversed(samples[:samples.index(s)])
                      if not p.get("combat") and p.get("specID") == spec
                      and _asdict(p.get("cov")).get("ok")), None)
        label = f"spec {spec} @ t{s.get('at', 0):.0f}"
        if not cov.get("ok"):
            # A cold in-combat start: the honest refusal, not a roster read.
            rep.check(cov.get("reason") == "in-combat" and (cov.get("blind") or 0) == 0,
                      f"{label}: refused honestly", f"reason={cov.get('reason')}, "
                      f"blind={cov.get('blind')}")
            continue
        rep.check(bool(cov.get("stale")), f"{label}: served the CACHE, did not rescan",
                  f"stale={cov.get('stale')}")
        if prior is None:
            rep.note("no prior out-of-combat row for this spec — invariance unproven")
            continue
        rep.check(cov.get("blind") == prior.get("blind")
                  and cov.get("scanned") == prior.get("scanned"),
                  f"{label}: combat invented no blind rows",
                  f"blind {prior.get('blind')} -> {cov.get('blind')}, "
                  f"scanned {prior.get('scanned')} -> {cov.get('scanned')}")


def _check_invalidation(rep: Report, samples: list[dict]) -> None:
    rep.head("Phase 4 — the report rebuilds on a spec / hero swap")
    specs = {s.get("specID") for s in samples if s.get("specID") is not None}
    heroes = {s.get("hero") for s in samples if s.get("hero")}
    if len(specs) < 2:
        rep.skip("PLAYER_SPECIALIZATION_CHANGED invalidation",
                 f"only one spec played ({sorted(specs)}) — swap spec and pull again")
    else:
        rep.check(True, "the roster rebuilt across a spec swap",
                  f"specs seen: {sorted(specs)}")
    if len(heroes) < 2:
        rep.skip("Phase 3's Diabolist half (the keybind ladder falls through)",
                 f"only one hero tree seen ({sorted(heroes) or ['none']}) — swap it and pull")
    else:
        rep.check(True, "two hero trees seen", f"{sorted(heroes)}")


def _check_drawability(rep: Report, samples: list[dict]) -> None:
    """Which roster BUTTONS the CDM database carries but no viewer DISPLAYS.

    MEASURED, never scored, and the distinction is the finding the first flight produced:
    `coverage` joins on the CDM DATABASE, while whether an ability has an icon to anchor a
    cue to is a question about the live VIEWERS. Incinerate is in the database (so it reads
    `tracked`) and has no icon (so `HudVirtual` synthesises one) — both true, and the
    summary line's "0 our own icons" hides it, because the untracked branch that computes
    virtual eligibility never runs for an id the database join already matched.

    ⚠ AURAS ARE EXCLUDED, and without that this list is unreadable: they live in the BUFF
    viewers, which `HudLayout.Scan` does not walk at all, so every tracked aura would show
    up here as "no icon". Rings from before v0.32.54 carry no `kind`, so the exclusion
    cannot be made and the list is reported raw with a warning.
    """
    rep.head("Roster DRAWABILITY (MEASURED) — in the CDM database, but no icon on screen")
    seen: set[int] = set()
    for s in samples:
        spec = s.get("specID")
        cov = _asdict(s.get("cov"))
        if s.get("combat") or not cov.get("ok") or not s.get("layout") or spec in seen:
            continue
        seen.add(int(spec))
        shown = {int(x["spellID"]) for x in _aslist(s.get("layout"))
                 if x.get("spellID") is not None}
        vm = _verdict_map(s)
        have_kind = any(v.get("kind") for v in vm.values())
        undrawn = sorted(i for i, v in vm.items()
                         if v.get("v") == "ok" and i not in shown
                         and (v.get("kind") == "button" if have_kind else True))
        rep.measured(f"spec {spec}", f"{len(shown)} icon(s) displayed · "
                                     f"{len(undrawn)} tracked button(s) with no icon")
        if undrawn:
            rep.note(f"{undrawn}")
        if not have_kind:
            rep.note("⚠ pre-v0.32.54 ring: no `kind` recorded, so AURAS could not be "
                     "excluded — most of that list is buff-viewer rows, not a finding")
        else:
            rep.note("each of these must be covered by HudVirtual's own icon, or it is "
                     "genuinely undrawable — the next thing worth checking")
    if not seen:
        rep.skip("drawability", "no out-of-combat sample carried a layout")


def _check_assist(rep: Report, samples: list[dict]) -> None:
    """MEASURED, never scored. The rider's whole question is open; a 'no' closes it just
    as usefully as a 'yes', and a PASS/FAIL frame would invite someone to 'fix' it."""
    rep.head("RIDER (MEASURED, not scored) — does C_AssistedCombat survive combat?")
    ooc = next((s for s in samples if not s.get("combat")), None)
    hot = next((s for s in samples if s.get("combat")), None)
    if ooc is None and hot is None:
        rep.skip("the rider", "no samples")
        return
    for label, s in (("out of combat", ooc), ("IN COMBAT", hot)):
        if s is None:
            rep.skip(f"{label}", "never sampled in this state")
            continue
        a = _asdict(s.get("assist"))
        rep.measured(f"{label:14s} GetNextCastSpell(false)",
                     f"{a.get('next0')}"
                     + (f" = {a.get('next0Value')}" if a.get("next0Value") is not None else ""))
        rep.measured(f"{'':14s} GetNextCastSpell(true) ",
                     f"{a.get('next1')}"
                     + (f" = {a.get('next1Value')}" if a.get("next1Value") is not None else ""))
        rep.measured(f"{'':14s} IsAvailable/GetRotationSpells",
                     f"{a.get('available')} / {a.get('rotation')}")
    if hot is not None:
        cls = _asdict(hot.get("assist")).get("next0")
        rep.note("THE ANSWER: in combat GetNextCastSpell reads " + str(cls)
                 + (" — READABLE through combat; publish it under "
                    "api-events-and-discovery.md §2"
                    if cls == "num" else
                    " — NOT readable in combat; that closes the channel question, publish it"))
        # ⚠ READABILITY IS NOT USEFULNESS, and the recorder cannot tell them apart by
        # construction: it dedups by CLASS, so a value that never changes class is sampled
        # only at transitions. Identical values out of and in combat prove the call did not
        # go secret; they do not prove it was tracking the rotation.
        vals = {str(_asdict(s.get("assist")).get("next0Value")) for s in samples
                if _asdict(s.get("assist")).get("next0Value") is not None}
        if cls == "num" and len(vals) <= 1:
            rep.note("⚠ but the value never varied across the flight " + str(sorted(vals))
                     + " — readability is proven, USEFULNESS is not. The ring dedups by "
                       "class, so it samples only at transitions; a value-sampling pass is "
                       "needed before treating this as an oracle to diff the Coach against.")


def _check_capability(rep: Report, samples: list[dict]) -> None:
    rep.head("Standing capability checks (they degrade silently, so they are checked here)")
    s = samples[-1]
    aura = _asdict(s.get("aura"))
    rows = aura.get("rows") or 0
    if rows == 0:
        rep.skip("aura-frame read", "no CDM item frames in the last sample")
    else:
        ok = (aura.get("unit") == rows and aura.get("window") == rows)
        rep.check(ok, "aura-frame writers present on every row",
                  f"{aura.get('unit')}/{rows} auraDataUnit, {aura.get('window')}/{rows} "
                  f"pandemic writers" + ("" if ok else "  — the internals moved; the DoT "
                                         "line is on the edge-latch fallback"))
    binds = _asdict(s.get("binds"))
    bound = binds.get("bound") or 0
    rep.check(bound > 0, "keybinds resolved",
              f"{bound} bound / {binds.get('slots')} slot(s)"
              + ("" if bound else "  — every key hint will be blank (the v0.32.50 shape)"))
    errs = [s for s in samples if s.get("err")]
    rep.check(not errs, "no pipeline tick errors",
              errs[0].get("err", "")[:120] if errs else "")


def _check_decisionlog(rep: Report, decisionlog) -> None:
    """Phases 2 and v0.32.47 are answered by the decision log, which lives in the same
    SavedVariables file — so one command covers the whole owed pass rather than two."""
    rep.head("Phase 2 (the DoT read) + v0.32.47 (ChargeGained) — from the decision log")
    entries: list[str] = []
    for session in _aslist(decisionlog):
        entries += [str(e) for e in _aslist(_asdict(session).get("entries"))]
    if not entries:
        rep.skip("the decision log", "no entries — was the HUD on? did you /reload?")
        return
    not_up = sum(1 for e in entries if ":not_up" in e)
    refresh = sum(1 for e in entries if ":pandemic_refresh" in e)
    rep.check(not_up > 0, "the DoT `not_up` cue appears at all",
              f"{not_up} not_up vs {refresh} pandemic_refresh "
              f"(baseline before Phase 2: 0 vs 169)")
    conf = sum(1 for e in entries if "w:Conf" in e or "w!Conf" in e)
    total = sum(1 for e in entries if "w:" in e or "w!" in e)
    share = (100.0 * conf / total) if total else 0.0
    rep.check(share < 40.0, "Conflagrate is not cued at zero charges",
              f"{conf}/{total} decisions = {share:.1f}% (baseline 702/1272 = 55.2%)")
    nowin = sum(1 for e in entries if "w:-" in e)
    rep.measured("nil-winner rate", f"{nowin}/{len(entries)} lines "
                                    f"({100.0 * nowin / len(entries):.1f}%)")
    # ⚠ NOT COMPARABLE TO THE 6.2% BASELINE, and saying so is the point. That figure was
    # measured across a PULL; this log spans the whole session, and out of combat "no
    # winner" is the correct answer (there is no rotation to advise), so idling inflates it
    # without anything being wrong. The decision-log line carries no combat flag, so the
    # split cannot be made here — treat the number as a trend on like-for-like captures
    # only, never against the pull-only baseline.
    rep.note("^ spans OOC + combat; the 6.2% pull baseline is NOT comparable (no combat "
             "flag on a decision-log line to split by)")


def cmd_flight(db: dict, path: str) -> int:
    store = _asdict(db.get("flight"))
    samples = [s for s in _aslist(store.get("samples")) if isinstance(s, dict)]
    print(path)
    if not samples:
        print("\nNo flight samples. The flow is:\n"
              "  /cdmp flight        arm it (turns the HUD on)\n"
              "  …play a dummy pull, swap hero tree, swap spec, pull again…\n"
              "  /reload             flush SavedVariables\n"
              "  uv run python -m wowkb.cdmp flight", file=sys.stderr)
        return 1
    print(f"flight started {store.get('started', '?')} on v{store.get('version', '?')} · "
          f"{len(samples)} sample(s)")

    rep = Report()
    _check_coverage(rep, samples)
    _check_combat_guard(rep, samples)
    _check_invalidation(rep, samples)
    _check_capability(rep, samples)
    _check_drawability(rep, samples)
    _check_decisionlog(rep, db.get("decisionlog"))
    _check_assist(rep, samples)
    print("\n".join(rep.lines))

    print("")
    if rep.failed:
        print(f"{rep.failed} FAILURE(S)" + (f" · {rep.skipped} skipped" if rep.skipped else ""))
        return 1
    if rep.skipped:
        # A criterion nobody exercised must never read as a pass.
        print(f"no failures, but {rep.skipped} criteria were NOT EXERCISED — the flight "
              f"did not cover them. Read the SKIP lines and fly the missing parts.")
        return 2
    print("ALL CRITERIA PASS.")
    return 0


# --------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------
# rtfx — the `/cdmp rt fx` capture: what was ACTUALLY on each cue, per view change.
# ---------------------------------------------------------------------------
# WHY THIS EXISTS.  Dialling the cue treatment meant reading a screenful of chat per
# ladder rung and pasting it back, across eight rungs and two paths — the transcription
# cost swamped the judgement, which is the same complaint that turned the acceptance pass
# into `/cdmp flight`.  The addon now snapshots every redraw into `CDMProbeDB.rtfx`; this
# flattens it.
#
# THE OUTPUT IS A DIFF, NOT A LISTING.  Every sample carries the same ~20 fields per cue,
# and reading them side by side is exactly what the eye is bad at — so consecutive samples
# are compared and only CHANGED fields are printed.  A rung that reports nothing changed
# but LOOKS different is itself the finding: it means the fault is not in widget state.
_RTFX_KNOBS = ("layers", "noPop", "scale", "spinMul", "rays", "stack", "bg", "art",
               "pulseMul", "pulseFloor", "pulseOff", "echoOff", "echoMul",
               "echoLight", "echoScale")
# Per-cue fields, in the order they are worth reading: the frame first (the pop animates
# its scale, and a rotation inside a scaled frame is the shape of a "surging spin"), then
# the ring, then the echo.
_RTFX_CUE = ("dotW", "layW", "layH", "layScale", "layEff", "popPlaying",
             "ringW", "ringH", "ringShown", "ringAlpha", "regionAlpha",
             "spinSecs", "spinDeg", "spinPlay", "pulseSecs", "pulsePlay",
             "echoW", "echoShown", "echoAlpha", "echoSecs", "echoDeg", "echoPlay")


def _fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.3f}".rstrip("0").rstrip(".") or "0"
    if isinstance(v, bool):
        return "1" if v else "0"
    return str(v)


def _rtfx_cues(sample: dict) -> dict[str, dict]:
    out = {}
    for c in _aslist(sample.get("cues")):
        c = _asdict(c)
        k = str(c.get("key", "?"))
        out[k] = c
    return out


# ⚠ `cmd_rtfx` and `cmd_rtlab` WERE HERE AND ARE DELETED (2026-08-02).  They extracted
# `CDMProbeDB.rtfx` (the `/cdmp rt fx` dialling capture) and `CDMProbeDB.rtlab` (the
# `/cdmp rt lab` rotation-phase capture); BOTH IN-GAME PRODUCERS ARE ARCHIVED, so neither
# saved-var is ever written again and both commands could only ever re-print a stale
# capture.  The rtlab analysis — unwrap `Animation:GetProgress()` into a cumulative phase,
# subtract a uniform spin, and read the residual in degrees — is worth rebuilding if a
# rotation is ever suspect again; recover it from git history at v0.32.73 rather than
# re-deriving it, and note the sign-change counter needs hysteresis or float noise reads
# as a 0.1s oscillation.

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract CDMProbe recorders off SavedVariables.")
    ap.add_argument("command", choices=["decisionlog", "alerttape", "flight"],
                    help="flight: the PASS/FAIL ACCEPTANCE REPORT for an in-game pass "
                         "recorded by `/cdmp flight` (this is the one you want after a "
                         "test build) · decisionlog: flatten the pipeline decision log · "
                         "alerttape: flatten the temporary CDM alert-channel discovery tape")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--out", default=None,
                    help="flat .log destination (default: <repo>/raw/cdmp-<command>.log, gitignored)")
    args = ap.parse_args(argv)

    if args.command == "flight":
        loaded = load_db(args.wow_path)
        if loaded is None:
            print(f"No readable CDMProbe.lua under "
                  f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
            return 1
        db, path = loaded
        return cmd_flight(db, path)

    if args.command == "alerttape":
        loaded = load_alerttape(args.wow_path)
        if loaded is None:
            print(f"No readable CDMProbe.lua under "
                  f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
            return 1
        alerttape, path = loaded
        out = args.out or str(REPO_ROOT / "raw" / "cdmp-alerttape.log")
        return cmd_alerttape(alerttape, path, Path(out))

    loaded = load_decisionlog(args.wow_path)
    if loaded is None:
        print(f"No readable CDMProbe.lua under "
              f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
        print("Enable the HUD (/cdmp hud), play, and /reload first.", file=sys.stderr)
        return 1
    decisionlog, path = loaded
    out = args.out or str(REPO_ROOT / "raw" / "cdmp-decision.log")
    return cmd_decisionlog(decisionlog, path, Path(out))


if __name__ == "__main__":
    raise SystemExit(main())

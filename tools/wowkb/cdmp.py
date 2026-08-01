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
    for session in sessions:
        s = _asdict(session)
        entries = _aslist(s.get("entries"))
        lines.append(
            f"# session {s.get('started', '?')} v{s.get('version', '?')} "
            f"tracked:{s.get('tracked', '?')}")
        for e in entries:
            text = str(e)
            lines.append(text)
            if "# config " in text:
                configs.append(f"{s.get('started', '?')}  {text}")
            total += 1
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
COVERAGE_EXPECT = {
    267: {  # Destruction
        "name": "Destruction",
        "absent": {417234: "Crashing Chaos (deleted in Phase 4 — redundant, not blind)"},
        "verdict": {
            29722: ("virtual", "Incinerate — untracked, but we draw our own icon"),
            434635: ("expected", "Ruination alt id — override-only by design"),
            434636: ("expected", "Ruination alt id — override-only by design"),
            132411: ("expected", "Singe Magic — the pet dispel override"),
            388215: ("expected", "Devour Magic — the pet dispel override"),
        },
        "tracked_rows": {428514: (4, "Diabolic Ritual — tracked across 4 cooldownIDs")},
    },
    266: {  # Demonology
        "name": "Demonology",
        "absent": {},
        "verdict": {686: ("virtual", "Shadow Bolt — the untracked floor press")},
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
    out = {}
    for v in _aslist(_asdict(sample.get("cov")).get("verdicts")):
        if isinstance(v, dict) and v.get("id") is not None:
            out[int(v["id"])] = v
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
        blind = cov.get("blind") or 0
        rep.check(blind == 0, "0 BLIND",
                  f"({cov.get('okN')} tracked · {cov.get('virtualN')} our own icons · "
                  f"{cov.get('expectedN')} override-only · {blind} blind · "
                  f"{cov.get('unknownN')} unknown, over {cov.get('scanned')} CDM rows)")
        if blind:
            for spell, v in sorted(vm.items()):
                if v.get("v") == "blind":
                    known = v.get("known")
                    rep.note(f"BLIND {spell} — knownness "
                             + ("true" if known is True else
                                "FALSE (untalented — a weaker finding)" if known is False
                                else "unreadable (a weaker finding)"))
        for spell, why in expect["absent"].items():
            rep.check(spell not in vm, f"{spell} absent from the roster", why)
        for spell, (want, why) in expect["verdict"].items():
            got = vm.get(spell, {}).get("v")
            rep.check(got == want, f"{spell} reads {want}",
                      f"got {got or '<not in roster>'} — {why}")
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
                 + (" — a readable oracle; publish it under api-events-and-discovery.md §2"
                    if cls == "num" else
                    " — NOT readable in combat; that closes the channel question, publish it"))


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

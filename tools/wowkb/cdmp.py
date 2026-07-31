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

    CDMProbeDB.census        <- ⚠ TEMPORARY. The CDM STRUCT CENSUS (addon Census.lua,
                                `/cdmp census`): per capture, one row per cooldownID with
                                every documented Tier-1 struct field read through its OWN
                                pcall and classified five ways, plus the frame-side reads
                                (GetSpellID/GetAuraSpellID/GetLinkedSpell, wasSetFrom*,
                                auraDataUnit). Answers the six "is this defect live or
                                latent" questions projects/cooldown-hud/docs/
                                roster-state-plan.md Phase 2 is gated on. Delete this
                                third of the module with Census.lua.

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
    uv run python -m wowkb.cdmp census                      # → raw/cdmp-census.log
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
# census — the TEMPORARY CDM struct census                                     #
# --------------------------------------------------------------------------- #
# ⚠ Delete this section with the addon's Census.lua. See that file's header for the six
# questions and why each one gates a Phase-2 fix.


def load_census(wow_path: str) -> tuple[object, str] | None:
    """(census, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    db = parse_savedvar(Path(pth).read_text(encoding="utf-8", errors="replace"), "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (db.get("census"), pth)


def _cell(entry) -> str:
    """One `{c=<class>, v=<sample>}` reading, rendered so the CLASS is never lost.

    A bare value would erase the distinction the whole instrument exists for — `nil`,
    `SECRET` and `threw` are three different findings with opposite implications.
    """
    e = _asdict(entry)
    if not e:
        return "-"
    cls, val = e.get("c"), e.get("v")
    # "table" joins these: for PandemicIcon the CLASS *is* the signal (a frame reference is
    # present or it is not), and there is no scalar to render.
    if cls in ("nil", "absent", "threw", "SECRET", "SECRET-TABLE", "table"):
        return str(cls)
    if val is None:
        return f"{cls}:?"
    return str(val)


# The columns, in the order a reader wants them: identity first, then the flags a fix is
# gated on, then the pool.
_STRUCT_COLS = ["spellID", "overrideSpellID", "overrideTooltipSpellID", "linkedSpellID",
                "isKnown", "hasAura", "selfAura", "charges", "flags", "category"]
_FRAME_COLS = ["GetSpellID", "GetBaseSpellID", "GetAuraSpellID", "GetLinkedSpell",
               "IsActive", "IsShown"]
_FRAME_FIELDS = ["wasSetFromCharges", "wasSetFromCooldown", "wasSetFromAura",
                 "auraDataUnit", "hideWhenInactive",
                 # The pandemic trio.  PandemicIcon's PRESENCE is the live, self-clearing
                 # pandemic state (Blizzard sets/nils it every frame from the item OnUpdate);
                 # the other two are the throttle that makes the PandemicTime alert one-shot.
                 "PandemicIcon", "pandemicAlertTriggerTime",
                 "nextAvailableTimeToPlayPandemicAlert"]


def _tally(counts: dict[str, int]) -> str:
    """A readability-class census, most common first — `SECRET=40 boolean=12` reads as a
    finding; a bare count does not."""
    if not counts:
        return "(no frames)"
    return " ".join(f"{k}={v}" for k, v in
                    sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def cmd_census(census, path: str, out: Path) -> int:
    """Flatten the struct census, oldest capture first, and answer the six questions.

    Each capture is labelled OOC or CMB. Half the questions are ONLY about the difference,
    so a run with just one of the two proves nothing — that is called out explicitly rather
    than left for the reader to notice.
    """
    captures = _aslist(census)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    verdict: list[str] = []
    # ⚠ GROUPED BY BUILD, never pooled.  The CDM's tracked set changes wholesale on a spec
    # swap and substantially on a hero-tree or loadout swap, so captures from two builds are
    # not comparable row by row — and the OOC/CMB pairing every combat question depends on
    # is only meaningful WITHIN one build.  Pooling them would let a Demonology OOC capture
    # silently answer a question about Destruction in combat.
    by_build: dict[str, set[str]] = {}
    stale: list[str] = []

    for cap in captures:
        c = _asdict(cap)
        combat = str(c.get("combat", "?"))
        build = (f"{c.get('spec')}/hero:{c.get('heroID')}"
                 f"/cfg:{c.get('config')}")
        by_build.setdefault(build, set()).add(combat)
        if c.get("heroStale"):
            stale.append(f"{c.get('when')} {build}: live={c.get('heroID')} "
                         f"pipeline={c.get('hero')}")
        lines.append(
            f"# capture {combat} {c.get('when', '?')} at={c.get('at')} "
            f"v{c.get('version', '?')} build={build} "
            f"specID={c.get('specID')} heroName={c.get('hero')} "
            f"active={c.get('active')} cids={c.get('cids')} frames={c.get('frames')}"
            + (" ⚠ HERO-STALE" if c.get("heroStale") else "")
            + (f" ⚠ {c['catError']}" if c.get("catError") else ""))

        dual, q1, q2, elected, pool_only, threw = [], [], [], 0, 0, []
        # Q6 is a CLASS CENSUS, not a yes/no: "readable on 12 rows, SECRET on 40" is the
        # finding, and it is only meaningful compared against the other combat state.
        was_set: dict[str, int] = {}
        aura_unit: dict[str, int] = {}
        for row in _aslist(c.get("rows")):
            r = _asdict(row)
            cid, cats = r.get("cid"), str(r.get("cats", "?"))
            struct = r.get("struct")
            head = f"{combat} cid={cid} [{cats}] {r.get('name') or '?'}"
            if struct != "table":
                lines.append(f"{head} STRUCT={struct}")
                threw.append(f"{cid}:struct={struct}")
                continue

            f = _asdict(r.get("f"))
            cols = " ".join(f"{k}={_cell(f.get(k))}" for k in _STRUCT_COLS)
            poolinfo = _asdict(r.get("pool"))
            pool = poolinfo.get("v") if poolinfo.get("c") == "table" else poolinfo.get("c")
            lines.append(f"{head} {cols} pool=[{pool or ''}]")

            if r.get("nCats", 1) > 1:
                dual.append(f"{cid}({cats})")
            # Q1 — a TAB-1 row carrying either aura flag makes §3.1 live rather than latent.
            tab1 = ("Essential" in cats) or ("Utility" in cats)
            ha, sa = _asdict(f.get("hasAura")), _asdict(f.get("selfAura"))
            if tab1 and (ha.get("v") is True or sa.get("v") is True):
                q1.append(f"{cid} {r.get('name')}(hasAura={ha.get('v')} "
                          f"selfAura={sa.get('v')})")
            # Q2 — both static override fields on one row make §3.5 reachable.
            ov, ovt = _asdict(f.get("overrideSpellID")), _asdict(f.get("overrideTooltipSpellID"))
            if ov.get("c") == "number" and ovt.get("c") == "number":
                q2.append(f"{cid} {r.get('name')}(ov={ov.get('v')} ovt={ovt.get('v')})")
            # Q3 — did the FRESH read carry the elected singular link?
            if _asdict(f.get("linkedSpellID")).get("c") == "number":
                elected += 1
            elif poolinfo.get("c") == "table" and (poolinfo.get("n") or 0) > 0:
                pool_only += 1
            # Q4 — any field whose INDEX raised is the §3.9 trigger, observed.
            for k, entry in f.items():
                if _asdict(entry).get("c") == "threw":
                    threw.append(f"{cid}.{k}")

            m, ff = _asdict(r.get("m")), _asdict(r.get("ff"))
            for k in ("wasSetFromCharges", "wasSetFromCooldown", "wasSetFromAura"):
                cls = _asdict(ff.get(k)).get("c")
                if cls:
                    was_set[str(cls)] = was_set.get(str(cls), 0) + 1
            cls = _asdict(ff.get("auraDataUnit")).get("c")
            if cls:
                aura_unit[str(cls)] = aura_unit.get(str(cls), 0) + 1
            if m or ff:
                mcols = " ".join(f"{k}={_cell(m.get(k))}" for k in _FRAME_COLS)
                fcols = " ".join(f"{k}={_cell(ff.get(k))}" for k in _FRAME_FIELDS)
                lines.append(f"{head}   FRAME {mcols} {fcols}")

        verdict += [
            f"[{build} {combat}] Q1 tab-1 rows with an aura flag  : "
            + (", ".join(q1) if q1 else "NONE → §3.1 is LATENT"),
            f"[{build} {combat}] Q2 rows with BOTH override fields: "
            + (", ".join(q2) if q2 else "NONE → §3.5 is LATENT"),
            f"[{build} {combat}] Q3 elected linkedSpellID on a FRESH read: {elected} row(s); "
            f"pool-only: {pool_only}"
            + ("  → Phase 3 CAN use a fresh read" if elected
               else "  → Phase 3 must read item:GetLinkedSpell() off the FRAME"),
            f"[{build} {combat}] Q4 struct fields whose INDEX raised: "
            + (", ".join(threw) if threw else "NONE → §3.9 has no observed trigger yet"),
            f"[{build} {combat}] Q5 cids in >1 category set       : "
            + (", ".join(dual) if dual else "NONE"),
            f"[{build} {combat}] Q6 wasSetFrom* {_tally(was_set)} | auraDataUnit {_tally(aura_unit)}",
        ]

    lines.append("")
    lines.append("# ── BUILDS CAPTURED ─────────────────────────────────────────────────")
    for b, seen in sorted(by_build.items()):
        lines.append(f"# {b}: {'+'.join(sorted(seen))}")
    lines.append("# ── VERDICT ─────────────────────────────────────────────────────────")
    lines += ["# " + v for v in verdict]
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    print(f"{path}")
    print(f"{len(captures)} capture(s) → {out}\n")
    for v in verdict:
        print("  " + v)
    if not captures:
        print("\n⚠ No captures. Run /cdmp census in game, then /reload.", file=sys.stderr)
        return 1
    if stale:
        # Not a census artefact — the pipeline was DECIDING on the wrong hero tree.
        print("\n⚠ PIPELINE HERO WAS STALE in " + str(len(stale)) + " capture(s):",
              file=sys.stderr)
        for row in stale:
            print("    " + row, file=sys.stderr)

    # Per BUILD, because the OOC/CMB pairing is only meaningful inside one.
    incomplete = {b: {"OOC", "CMB"} - seen for b, seen in by_build.items()
                  if {"OOC", "CMB"} - seen}
    if incomplete:
        print("\n⚠ Incomplete build(s) — half these questions are ONLY about the combat "
              "difference, so a build with just one side answers none of them:",
              file=sys.stderr)
        for b, missing in sorted(incomplete.items()):
            print(f"    {b}: missing {'/'.join(sorted(missing))}", file=sys.stderr)
        print("    Fix: `/cdmp census` standing still, then `/cdmp census arm` and pull.",
              file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract CDMProbe recorders off SavedVariables.")
    ap.add_argument("command", choices=["decisionlog", "alerttape", "census"],
                    help="decisionlog: flatten the pipeline decision log · alerttape: "
                         "flatten the temporary CDM alert-channel discovery tape · "
                         "census: flatten the temporary CDM struct census")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--out", default=None,
                    help="flat .log destination (default: <repo>/raw/cdmp-<command>.log, gitignored)")
    args = ap.parse_args(argv)

    if args.command == "census":
        loaded = load_census(args.wow_path)
        if loaded is None:
            print(f"No readable CDMProbe.lua under "
                  f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
            return 1
        census, path = loaded
        out = args.out or str(REPO_ROOT / "raw" / "cdmp-census.log")
        return cmd_census(census, path, Path(out))

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

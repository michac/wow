"""Read + ASSERT CDMProbe `/cdmp probe` captures off the WoW SavedVariables file.

THE DIVISION OF LABOUR THIS MODULE EXISTS TO ENFORCE
(projects/cooldown-hud/docs/m4.5-t3-plan.md):

    COLLECT a new observation  -> addon change + release.
    ASSERT / interpret / re-verify -> here, local, no release.

An earlier design put an assertion suite *in the client* (`/cdmp selftest`). It
was shelved because `/cdmp probe` already collects every observation it would
have re-collected — the missing piece was never collection, it was
INTERPRETATION. Baking expected answers into shipped Lua means a release per
tweak; keeping them in probe-baseline.json means an edit.

WHAT WE READ. The addon writes each probe run twice: a TEXT report (for a human)
and the same facts as a structured table. We read only the structured half —
text-parsing a report this codebase re-words freely is a maintenance trap, which
is exactly why the structured store was added.

    CDMProbeDB.probe.ooc / .combat   <- the structured snapshots (A1)
    CDMProbeDB.pulls                 <- the pull recorder's ring (M3e, already structured)

⚠ SavedVariables only flush on /reload or logout. A capture that looks stale
almost always means the /reload was skipped, which is indistinguishable from a
probe that silently did nothing — hence the timestamps in every render.

This mirrors the on-disk read pattern wowkb.diagnostics already uses for
BucketBinds: glob the newest CDMProbe.lua under WTF/Account/*/SavedVariables/,
parse with charstate.parse_savedvar, render.

Usage:
    uv run python -m wowkb.cdmp check
    uv run python -m wowkb.cdmp check --wow-path <dir>     # e.g. a test fixture
    uv run python -m wowkb.cdmp show [--json]
    uv run python -m wowkb.cdmp diff                       # ooc vs combat (the M3d seam)
    uv run python -m wowkb.cdmp diff --against saved.json  # vs an exported capture
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from .charstate import DEFAULT_WOW, parse_savedvar

# The baseline lives with the project docs, not in tools/ — it is a project
# artifact (the assumptions-of-record), and tools/ is the reader, not the truth.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = REPO_ROOT / "projects" / "cooldown-hud" / "probe-baseline.json"

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"
CONTEXTS = ("ooc", "combat")


# --------------------------------------------------------------------------- #
# Loading (mirrors diagnostics.py one-for-one)                                 #
# --------------------------------------------------------------------------- #

def _find_savedvar(wow_path: str) -> str | None:
    """Newest CDMProbe.lua under any account's SavedVariables (mtime desc)."""
    pattern = f"{wow_path}/WTF/Account/*/SavedVariables/CDMProbe.lua"
    hits = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


def _fmt_time(epoch) -> str:
    if not isinstance(epoch, (int, float)) or epoch <= 0:
        return "?"
    try:
        return (datetime.fromtimestamp(int(epoch), tz=timezone.utc)
                .astimezone().strftime("%Y-%m-%d %H:%M"))
    except (ValueError, OSError, OverflowError):
        return "?"


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


def load_capture(wow_path: str) -> tuple[dict, dict, str] | None:
    """(probe, pulls, path) from the newest CDMProbe.lua, or None."""
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return _asdict(db.get("probe")), _asdict(db.get("pulls")), pth


def _iface_to_patch(iface) -> str | None:
    """"120007" -> "12.0.7".  Lets the reader notice a baseline stamped for a
    different patch than the capture actually came from."""
    s = str(iface or "")
    if not s.isdigit() or len(s) != 6:
        return None
    return f"{int(s[0:2])}.{int(s[2:4])}.{int(s[4:6])}"


# --------------------------------------------------------------------------- #
# Small accessors over a snapshot                                             #
# --------------------------------------------------------------------------- #

def _reads(snap) -> dict:
    """{spellID: {readable, duration/startTime | why}} for one snapshot."""
    return _asdict(_asdict(snap).get("reads"))


def _readable_split(snap) -> tuple[int, int]:
    """(readable, unreadable) counts over a snapshot's Section A reads."""
    r = u = 0
    for obs in _reads(snap).values():
        if _asdict(obs).get("readable"):
            r += 1
        else:
            u += 1
    return r, u


def _phase_counts(probe: dict, phase: str) -> tuple[int, int] | None:
    """(readable, secret) for a cast phase.

    The addon's counters are CUMULATIVE SINCE LOAD, so the ooc and combat
    snapshots are nested samples of one series, not independent ones — summing
    them would double-count. Take the snapshot that saw the most events.
    """
    best = None
    for ctx in CONTEXTS:
        b = _asdict(_asdict(_asdict(probe.get(ctx)).get("casts")).get(phase))
        if not b:
            continue
        rd, sec = int(b.get("readable") or 0), int(b.get("secret") or 0)
        if best is None or (rd + sec) > (best[0] + best[1]):
            best = (rd, sec)
    return best


def _observed_transforms(probe: dict) -> set[int]:
    """Every spellID a button was observed to have TRANSFORMED INTO, from both
    independent channels: the override event's pairs and the live base-vs-live
    divergence. They can disagree, and the union is what we must recognise."""
    out: set[int] = set()
    for ctx in CONTEXTS:
        snap = _asdict(probe.get(ctx))
        for pair in _aslist(_asdict(snap.get("overrides")).get("pairs")):
            over = _asdict(pair).get("over")
            if isinstance(over, int):
                out.add(over)
        for live in _asdict(snap.get("divergence")).values():
            if isinstance(live, int):
                out.add(live)
    return out


def _imps(probe: dict) -> dict | None:
    for ctx in CONTEXTS:
        imps = _asdict(probe.get(ctx)).get("imps")
        if isinstance(imps, dict) and not imps.get("noFontString"):
            return imps
    return None


# --------------------------------------------------------------------------- #
# The checks — one function per baseline `id`                                  #
# --------------------------------------------------------------------------- #
# Each returns (status, detail).  SKIP is load-bearing and must never be
# confused with PASS: it means the capture does not CONTAIN the evidence, and
# absence of evidence is not evidence.  Only FAIL gates the exit code.

# Set by cmd_check when the two snapshots did not come from one session. A
# two-context check must DOWNGRADE to "not covered" rather than assert across
# separate runs -- absence of a single-session observation is not evidence.
_MIXED: set = set()


def _minutes_apart(ats) -> float:
    from datetime import datetime
    ds = []
    for a in ats:
        try:
            ds.append(datetime.strptime(a, "%Y-%m-%d %H:%M:%S"))
        except (ValueError, TypeError):
            return 0.0
    if len(ds) < 2:
        return 0.0
    return abs((max(ds) - min(ds)).total_seconds()) / 60.0



def _check_secret_api(probe, expect):
    want = expect.get("secretAPI", True)
    seen = [(_asdict(probe.get(c)).get("secretAPI"), c) for c in CONTEXTS
            if isinstance(_asdict(probe.get(c)).get("secretAPI"), bool)]
    if not seen:
        return SKIP, "no snapshot recorded secretAPI"
    bad = [c for v, c in seen if v is not want]
    if bad:
        return FAIL, f"secretAPI is not {want} in: {', '.join(bad)}"
    return PASS, f"secretAPI={want} in {', '.join(c for _, c in seen)}"


_SEAM_RULES = {
    "all-readable": (lambda r, u: u == 0 and r > 0, "readable"),
    "all-secret": (lambda r, u: r == 0 and u > 0, "secret"),
}


def _check_combat_seam(probe, expect):
    """The M3d seam is a TWO-CONTEXT claim, so one context can never confirm it.
    A missing half is SKIP even when the half we have looks perfect — reporting
    PASS off one context is exactly how a half-done capture gets mistaken for a
    verified one."""
    # A mixed capture cannot support a two-context claim -- see cmd_check.
    if _MIXED:
        return SKIP, ("snapshots came from different sessions/builds; a seam is a "
                      "one-sitting claim and will not be asserted across runs")
    parts, missing, failed = [], [], []
    for ctx in CONTEXTS:
        rule = expect.get(ctx)
        if rule is None:
            continue
        if not _reads(probe.get(ctx)):
            missing.append(ctx)
            continue
        pred, word = _SEAM_RULES.get(rule, (None, rule))
        r, u = _readable_split(probe.get(ctx))
        if pred is None:
            return FAIL, f"baseline asks for unknown rule {rule!r} on {ctx}"
        got = r if word == "readable" else u
        parts.append(f"{ctx} {got}/{r + u} {word}")
        if not pred(r, u):
            failed.append(f"{ctx}: wanted {rule}, got {r} readable / {u} unreadable")
    if failed:
        return FAIL, "; ".join(failed)
    if missing:
        seen = f" ({'; '.join(parts)} — but that half alone cannot confirm a seam)" if parts else ""
        return SKIP, f"no Section A reads for: {', '.join(missing)}{seen}"
    return PASS, " · ".join(parts)


def _check_phase(probe, expect):
    phase = expect.get("phase")
    counts = _phase_counts(probe, phase)
    if counts is None:
        return SKIP, f"no {phase} bucket in the capture"
    rd, sec = counts
    if rd + sec == 0:
        return SKIP, f"no {phase} events observed (cast something and re-capture)"
    if sec > 0 and rd == 0:
        return FAIL, f"{phase} ALL SECRET — {sec} events, 0 readable (feature dark here)"
    if sec > 0:
        return FAIL, f"{phase} MIXED — {rd} readable / {sec} secret"
    return PASS, f"{phase} fully readable — {rd} events, 0 secret"


def _check_transforms_known(probe, expect):
    known = {int(k) for k in _aslist(expect.get("known")) if isinstance(k, int)}
    seen = _observed_transforms(probe)
    if not seen:
        return SKIP, "no transform observed (arm a Demonic Art / let a Grimoire hit CD)"
    unknown = sorted(seen - known)
    if unknown:
        return FAIL, (f"unmapped transform target(s): {unknown} — an unrecognised "
                      "override gets NO dot, so the button silently blanks")
    return PASS, f"{len(seen)} observed transform(s), all mapped: {sorted(seen)}"


def _check_tracked_set(probe, expect):
    want = _asdict(expect.get("contains"))
    have: set[int] = set()
    for ctx in CONTEXTS:
        have |= {k for k in _reads(probe.get(ctx)) if isinstance(k, int)}
    if not have:
        return SKIP, "no Section A reads in the capture at all"
    missing = [(int(k), v) for k, v in want.items() if int(k) not in have]
    if missing:
        names = ", ".join(f"{n} ({i})" for i, n in sorted(missing))
        return FAIL, f"not tracked by the CDM: {names}"
    return PASS, f"all {len(want)} core abilities tracked ({len(have)} reads total)"


def _check_imps_closed(probe, expect):
    """Inverted on purpose: asserts a capability we DON'T have, so it fires if
    Blizzard ever opens the leak."""
    imps = _imps(probe)
    if imps is None:
        return SKIP, "Section D not exercised (no Wild Imp aura during the capture)"
    want = expect.get("imps", "unreadable")
    readable = [f for f in ("width", "text") if imps.get(f + "Readable")]
    if want == "unreadable":
        if readable:
            vals = ", ".join(f"{f}={imps.get(f)!r}" for f in readable)
            return FAIL, (f"side channel OPENED — {vals}. Do NOT build on it before "
                          "a deliberate review (a width derived from a secret may "
                          "still taint on comparison).")
        how = "errored" if imps.get("widthErrored") else "secret/absent"
        return PASS, f"still closed — width+text {how}"
    if want == "readable":
        if readable:
            return PASS, f"readable: {', '.join(readable)}"
        return FAIL, "expected a readable imp count, got none"
    return FAIL, f"baseline asks for unknown rule {want!r}"


def _check_cue_render(probe: dict, expect: dict):
    """M4.6 — did every cue RENDER the colour its level was set to?

    ⚠ THE INSTRUMENT IS INVALID AS BUILT (v0.27.0). It compares the palette colour
    against `Texture:GetVertexColor()`, and the first real capture returned
    got=1/1/1 on EVERY record for EVERY level -- including ROTATION, which the
    player confirms renders green on screen. So the read cannot see the rendered
    colour: with a gradient in play the vertex colour stays white regardless of
    what the bar actually draws. Every "divergence" it reported is the instrument,
    not the HUD, and the "the breathe hypothesis is dead" verdict it printed was
    never supported -- a blind instrument cannot falsify anything.

    This is the SECOND wrong confident answer about the white cue in one session
    (the first read a mechanism off a single screenshot). Hence: report the
    measurement as UNUSABLE rather than quietly reinterpreting it. A check that
    cannot observe its subject must say so, not produce a number.
    """
    for ctx in CONTEXTS:
        w = _asdict(_asdict(probe.get(ctx)).get("cueWatch"))
        if not w:
            continue
        samples, bad = w.get("samples") or 0, w.get("mismatch") or 0
        if samples and bad == samples * _lit_per_sample(w):
            pass  # every lit cue diverged every pass -- the signature of a blind read
        return SKIP, (f"INSTRUMENT INVALID — GetVertexColor reads white for every "
                      f"level whether or not the bar renders correctly, so the "
                      f"{bad} divergences over {samples} passes measure nothing. "
                      f"Needs a different probe; see m4.5-playtest5-feedback.md §4.5.c")
    return SKIP, "no cueWatch section in either snapshot (needs CDMProbe v0.27.0+)"


def _lit_per_sample(w: dict) -> int:
    by = _asdict(w.get("byLevel"))
    samples = w.get("samples") or 0
    return int(round(sum(by.values()) / samples)) if samples else 0



CHECKS = {
    "secret-api-present": _check_secret_api,
    "cooldown-read-combat-seam": _check_combat_seam,
    "succeeded-readable": _check_phase,
    "start-readable": _check_phase,
    "override-ids-known": _check_transforms_known,
    "tracked-set-core": _check_tracked_set,
    "imp-side-channel-closed": _check_imps_closed,
    "cue-renders-its-level": _check_cue_render,
}


# --------------------------------------------------------------------------- #
# Rendering                                                                   #
# --------------------------------------------------------------------------- #

def _snap_line(ctx: str, snap: dict) -> str:
    if not snap:
        return f"  {ctx:<7} — no snapshot (run /cdmp probe in that state, then /reload)"
    r, u = _readable_split(snap)
    return (f"  {ctx:<7} {snap.get('at', '?')}  v{snap.get('version', '?')}  "
            f"iface={snap.get('interface', '?')}  instance={snap.get('instance', '?')}  "
            f"reads={r + u} ({r} readable/{u} not)")


def _print_header(probe: dict, path: str) -> None:
    print(f"CDMProbe capture — {path}")
    print(f"  file mtime: {_fmt_time(os.path.getmtime(path))}")
    for ctx in CONTEXTS:
        print(_snap_line(ctx, _asdict(probe.get(ctx))))


def _stamp_age(stamp) -> str:
    try:
        d = date.fromisoformat(str(stamp))
    except (TypeError, ValueError):
        return "unstamped"
    days = (date.today() - d).days
    return f"{stamp} ({days}d ago)"


def cmd_check(probe: dict, pulls: dict, path: str, baseline: dict, bl_path: Path) -> int:
    _print_header(probe, path)
    if not probe:
        print("\nNo structured probe capture (CDMProbeDB.probe is empty).", file=sys.stderr)
        print("Needs CDMProbe v0.25.0+: run /cdmp probe, then /reload.", file=sys.stderr)
        return 1

    print(f"\nbaseline — {bl_path}")
    print(f"  patch {baseline.get('patch', '?')}, stamped {baseline.get('stamped', '?')}")

    # A baseline stamped for a different patch than the capture came from is the
    # KB's stale-`reviewed:` failure mode wearing addon clothes: every check
    # below would pass while asserting last patch's truth.
    ifaces = {_iface_to_patch(_asdict(probe.get(c)).get("interface")) for c in CONTEXTS}
    ifaces.discard(None)
    if ifaces and baseline.get("patch") not in ifaces:
        print(f"  ⚠ capture is from patch {'/'.join(sorted(ifaces))} but the baseline is "
              f"stamped {baseline.get('patch')} — re-verify and re-stamp.")

    # ── The two snapshots must come from ONE session ──────────────────────────
    # Play-test 5 follow-up: an `ooc` captured on v0.27.0 sat beside a `combat`
    # left on disk from a DIFFERENT session two hours earlier on v0.25.0, and the
    # two-context `cooldown-read-combat-seam` check happily PASSED by combining
    # them. That is a fabricated result: the seam is a claim about one client, one
    # build, one sitting, and stitching two runs together asserts something nobody
    # observed. `/cdmp probe clear` exists precisely to avoid this, and forgetting
    # it must be LOUD rather than silent.
    stamps = {c: _asdict(probe.get(c)) for c in CONTEXTS}
    vers = {c: s.get("version") for c, s in stamps.items() if s}
    if len(vers) > 1 and len(set(vers.values())) > 1:
        pairs = ", ".join(f"{c}={v}" for c, v in sorted(vers.items()))
        print(f"  ⚠ MIXED CAPTURE — snapshots came from different addon builds ({pairs}). "
              f"Any two-context check below is combining separate sessions. "
              f"Re-run: /cdmp probe clear, then ooc -> pull -> combat -> /reload.")
        _MIXED.add(True)
    else:
        # Same build is necessary but not sufficient — check the wall clock too.
        ats = [s.get("at") for s in stamps.values() if s and s.get("at")]
        if len(ats) > 1 and _minutes_apart(ats) > 45:
            print(f"  ⚠ MIXED CAPTURE — snapshots are {_minutes_apart(ats):.0f} minutes "
                  f"apart ({', '.join(sorted(ats))}); that is very unlikely to be one "
                  f"sitting. Re-run after /cdmp probe clear.")
            _MIXED.add(True)

    results = []
    for a in _aslist(baseline.get("assumptions")):
        aid = a.get("id")
        fn = CHECKS.get(aid)
        if fn is None:
            results.append((FAIL, aid, a, "no check function for this id (see CHECKS in cdmp.py)"))
            continue
        try:
            status, detail = fn(probe, _asdict(a.get("expect")))
        except Exception as e:  # noqa: BLE001 — a broken check must not look like a pass
            status, detail = FAIL, f"check raised {type(e).__name__}: {e}"
        results.append((status, aid, a, detail))

    print()
    hard_fails = 0
    for status, aid, a, detail in results:
        sev = (a.get("severity") or "medium").lower()
        if status == FAIL:
            label = "FAIL" if sev == "high" else "WARN"
            if label == "FAIL":
                hard_fails += 1
        elif status == SKIP:
            label = "----"
        else:
            label = "PASS"
        print(f"  {label}  {aid:<28} {detail}")

    skipped = [(aid, a) for status, aid, a, _ in results if status == SKIP]
    if skipped:
        print(f"\nnot covered this run ({len(skipped)}) — the capture lacks the evidence, "
              "which is NOT a pass:")
        for aid, a in skipped:
            print(f"  · {aid} — {a.get('desc')}")
        print("  (in-game: /cdmp probe guide says which of these you can still close)")

    # Stamp ages: a check that passes against a year-old stamp is a check that
    # has not actually run this patch.  The `context` prose is only unfolded for
    # results that need reading — on an all-green run it is noise that buries
    # the one line you came for.
    print("\nassumption stamps:")
    for status, aid, a, _ in results:
        print(f"  {aid:<28} confirmed {_stamp_age(a.get('confirmed'))}")
        ctx = a.get("context")
        if ctx and status != PASS:
            print(f"  {'':<28}   ↳ {ctx}")

    _print_pulls(pulls, brief=True)

    passed = sum(1 for s, _, _, _ in results if s == PASS)
    warns = sum(1 for s, _, a, _ in results
                if s == FAIL and (a.get("severity") or "medium").lower() != "high")
    print(f"\n{passed} pass · {hard_fails} fail · {warns} warn · {len(skipped)} not covered")
    return 1 if hard_fails else 0


def _print_pulls(pulls: dict, brief: bool = False) -> None:
    items = _aslist(pulls)
    if not items:
        return
    print(f"\npull log ({len(items)} recorded):")
    for p in items[-3:] if brief else items:
        p = _asdict(p)
        hist = _asdict(p.get("hist"))
        total = sum(v for v in hist.values() if isinstance(v, (int, float))) or 1
        dist = " ".join(f"{k}:{round(100 * v / total)}%" for k, v in sorted(hist.items()))
        print(f"  {p.get('at', '?')}  v{p.get('version', '?')}  "
              f"{round(float(p.get('dur') or 0))}s  peak={p.get('peak', '?')}")
        if dist:
            print(f"      lit {dist}")


def cmd_show(probe: dict, pulls: dict, path: str) -> int:
    _print_header(probe, path)
    if not probe:
        print("\nNo structured probe capture (CDMProbeDB.probe is empty).")
        return 1
    for ctx in CONTEXTS:
        snap = _asdict(probe.get(ctx))
        if not snap:
            continue
        print(f"\n── {ctx} ──")
        print(f"  secretAPI={snap.get('secretAPI')}")

        reads = _reads(snap)
        if reads:
            print(f"  A. cooldown readability ({len(reads)} tracked):")
            for sid in sorted(reads, key=lambda k: str(k)):
                obs = _asdict(reads[sid])
                if obs.get("readable"):
                    print(f"      {sid:<10} readable  duration={obs.get('duration')} "
                          f"startTime={obs.get('startTime')}")
                else:
                    print(f"      {sid:<10} NOT readable — {obs.get('why')}")

        ov = _asdict(snap.get("overrides"))
        div = _asdict(snap.get("divergence"))
        print(f"  B. overrides: {ov.get('count', 0)} event(s), "
              f"{len(_aslist(ov.get('pairs')))} pair(s), {len(div)} live divergence(s)")
        for pair in _aslist(ov.get("pairs")):
            pair = _asdict(pair)
            print(f"      event  base={pair.get('base')} -> over={pair.get('over')}")
        for base, live in sorted(div.items(), key=lambda kv: str(kv[0])):
            print(f"      live   base={base} -> {live}")

        casts = _asdict(snap.get("casts"))
        if casts:
            print("  C. cast readability per phase:")
            for phase in ("START", "SUCCEEDED", "STOP", "INTERRUPTED"):
                b = _asdict(casts.get(phase))
                if b:
                    print(f"      {phase:<12} readable={b.get('readable', 0):<5} "
                          f"secret={b.get('secret', 0)}")

        imps = snap.get("imps")
        if isinstance(imps, dict):
            print(f"  D. imps: width={imps.get('width')!r} (readable={bool(imps.get('widthReadable'))}"
                  f"{', errored' if imps.get('widthErrored') else ''})  "
                  f"text={imps.get('text')!r} (readable={bool(imps.get('textReadable'))}"
                  f"{', errored' if imps.get('textErrored') else ''})  shown={imps.get('shown')}")

    _print_pulls(pulls)
    return 0


def _reads_summary(probe: dict) -> dict:
    """{ctx: {spellID: 'readable'|why}} — the comparable shape for diffing."""
    out = {}
    for ctx in CONTEXTS:
        reads = _reads(probe.get(ctx))
        if reads:
            out[ctx] = {str(k): ("readable" if _asdict(v).get("readable")
                                 else str(_asdict(v).get("why")))
                        for k, v in reads.items()}
    return out


def cmd_diff(probe: dict, path: str, against: str | None) -> int:
    if against:
        other = json.loads(Path(against).read_text(encoding="utf-8"))
        a, b = _reads_summary(_asdict(other.get("probe", other))), _reads_summary(probe)
        la, lb = f"{against}", "this capture"
        ctxs = sorted(set(a) | set(b))
        for ctx in ctxs:
            print(f"\n── {ctx}: {la} → {lb} ──")
            _diff_maps(a.get(ctx, {}), b.get(ctx, {}))
        return 0

    # Default: the M3d seam, ooc vs combat within this capture.
    s = _reads_summary(probe)
    if len(s) < 2:
        print(f"Need both an ooc and a combat snapshot to diff the seam "
              f"(have: {', '.join(s) or 'neither'}).", file=sys.stderr)
        return 1
    print(f"CDMProbe capture — {path}")
    print("\n── Section A reads: ooc → combat (the M3d seam) ──")
    _diff_maps(s["ooc"], s["combat"])
    return 0


def _diff_maps(a: dict, b: dict) -> None:
    keys = sorted(set(a) | set(b))
    changed = 0
    for k in keys:
        va, vb = a.get(k), b.get(k)
        if va != vb:
            changed += 1
            print(f"  {k:<10} {va} → {vb}")
    if not changed:
        print("  (identical)")
    else:
        print(f"  {changed} of {len(keys)} changed")


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Read and assert CDMProbe /cdmp probe captures.")
    ap.add_argument("command", choices=["check", "show", "diff"])
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE),
                    help=f"assumptions-of-record JSON (default: {DEFAULT_BASELINE})")
    ap.add_argument("--json", action="store_true",
                    help="show: dump the raw capture as JSON (archive it to diff against later)")
    ap.add_argument("--against", help="diff: compare against a JSON capture exported by `show --json`")
    args = ap.parse_args(argv)

    loaded = load_capture(args.wow_path)
    if loaded is None:
        print(f"No readable CDMProbe.lua under "
              f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
        print("Run /cdmp probe in-game and /reload first.", file=sys.stderr)
        return 1
    probe, pulls, path = loaded

    if args.command == "show" and args.json:
        print(json.dumps({"probe": probe, "pulls": pulls, "_path": path},
                         indent=2, ensure_ascii=False, sort_keys=True, default=str))
        return 0
    if args.command == "show":
        return cmd_show(probe, pulls, path)
    if args.command == "diff":
        return cmd_diff(probe, path, args.against)

    bl_path = Path(args.baseline)
    if not bl_path.exists():
        print(f"Baseline not found: {bl_path}", file=sys.stderr)
        return 1
    baseline = json.loads(bl_path.read_text(encoding="utf-8"))
    return cmd_check(probe, pulls, path, baseline, bl_path)


if __name__ == "__main__":
    raise SystemExit(main())

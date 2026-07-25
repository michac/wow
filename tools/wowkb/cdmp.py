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
    CDMProbeDB.statelog              <- the W4 Phase-1 reduced-State pulse ring
                                        (/cdmp statelog); asserted by the baseline's
                                        `statelog` block (STATELOG_CHECKS below)

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
DEFAULT_GOLDENS = REPO_ROOT / "projects" / "cooldown-hud" / "corpus" / "goldens"
DEFAULT_CONTRACT = REPO_ROOT / "projects" / "cooldown-hud" / "guidance-contract.json"

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


def load_capture(wow_path: str) -> tuple[dict, dict, dict, str] | None:
    """(probe, pulls, statelog, path) from the newest CDMProbe.lua, or None.

    `statelog` is the W4 Phase-1 reduced-State capture ring (CDMProbeDB.statelog),
    written by `/cdmp statelog`. Separate from `.probe` — a stream of full State
    pulses, not the two-snapshot capability diagnostic.
    """
    pth = _find_savedvar(wow_path)
    if not pth:
        return None
    text = Path(pth).read_text(encoding="utf-8", errors="replace")
    db = parse_savedvar(text, "CDMProbeDB")
    if not isinstance(db, dict):
        return None
    return (_asdict(db.get("probe")), _asdict(db.get("pulls")),
            _asdict(db.get("statelog")), pth)


def _statelog_pulses(statelog: dict) -> list:
    """The captured State pulses as a list (parser yields list or int-keyed dict)."""
    return _aslist(_asdict(statelog).get("pulses"))


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



# --------------------------------------------------------------------------- #
# The statelog checks — the W4 Phase-1 fixture-quality gate                    #
# --------------------------------------------------------------------------- #
# A FIXTURE-QUALITY gate, NOT a rotation gate (build plan Phase 1). Each fn takes
# the captured State pulses and returns (status, detail). Two families:
#   * per-pulse State-CONTRACT invariants -> PASS/FAIL (a broken contract is a bug)
#   * corpus COVERAGE -> PASS/not-covered (absence of a moment is not a failure)
# Neither says anything about which cue lights or whether advice is right — that is
# Phase 2's independent oracle, and folding it in here would re-couple the layers.

# The reduced State's own vocabulary — the enum/domain the contract pins.
_CD_STATES = {"ready", "cooling", "anticipated", "unknown"}
_CD_SOURCES = {"live", "napkin", "none"}

# Real Enum.PowerType member names (game vocabulary). A power keyed by anything
# else means State invented a resource, which invariant #3 forbids.
_POWER_TYPES = {
    "Mana", "Rage", "Focus", "Energy", "ComboPoints", "Runes", "RunicPower",
    "SoulShards", "LunarPower", "HolyPower", "Alternate", "Maelstrom", "Chi",
    "Insanity", "Obsolete", "Obsolete2", "ArcaneCharges", "Fury", "Pain",
    "Essence", "RuneBlood", "RuneFrost", "RuneUnholy", "AlternateQuest",
    "AlternateEncounter", "AlternateMount", "NumPowerTypes",
}

# Rotation/spec vocabulary that must NEVER appear in a spec-agnostic State entry
# (invariant #3, the hard denylist SpecDemonology owns — grepped from that file).
_SPEC_DENYLIST = {
    "group", "role", "builder", "spender", "kind", "spends", "generates",
    "cadence", "burstalign", "gogate", "emphasis", "primary", "judgeable",
    "stage", "pole", "colorkey", "reasontag",
}

_SECRET_MARKER = "<secret>"


def _cooldowns(pulse) -> list:
    """A pulse's cooldown entries as a list of dicts."""
    return [_asdict(v) for v in _aslist(_asdict(pulse).get("cooldowns"))]


def _powers(pulse) -> dict:
    return _asdict(_asdict(pulse).get("power"))


def _events(pulse) -> list:
    return [_asdict(e) for e in _aslist(_asdict(pulse).get("events"))]


def _walk_scalars(obj):
    """Every scalar leaf under obj, for the raw-secret-marker scan."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_scalars(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_scalars(v)
    else:
        yield obj


def _transform_targets(pulses: list) -> set:
    """Every spellID an observed transform event resolved TO, across the corpus —
    the legitimate homes a divergent liveSpellID can point at even when the entry's
    static override fields are empty (an aura-driven override arrives by event)."""
    out = set()
    for p in pulses:
        for e in _events(p):
            to = e.get("to")
            if isinstance(to, int):
                out.add(to)
    return out


def _no_pulses(pulses):
    return (SKIP, "no statelog pulses captured (/cdmp statelog, play, /reload)") \
        if not pulses else None


def _check_sl_secrecy(pulses, expect):
    """Invariant #4: no raw secret ever reaches disk, and the unreadable-live paths
    carry no value. A '<secret>' marker anywhere, or a charge/aura marked
    readable=false that still carries a value, is a leak."""
    skip = _no_pulses(pulses)
    if skip:
        return skip
    bad = []
    for i, p in enumerate(pulses):
        for s in _walk_scalars(p):
            if isinstance(s, str) and s == _SECRET_MARKER:
                bad.append(f"pulse#{i}: a '<secret>' marker reached disk")
                break
        for c in _cooldowns(p):
            ch = _asdict(c.get("charge"))
            if ch.get("readable") is False and ("cur" in ch or "max" in ch):
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: unreadable charge carries a value")
            au = _asdict(c.get("aura"))
            if au.get("readable") is False and "active" in au:
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: unreadable aura carries a value")
    if bad:
        return FAIL, "; ".join(bad[:4]) + (f" (+{len(bad) - 4} more)" if len(bad) > 4 else "")
    return PASS, f"{len(pulses)} pulse(s): no secret on disk, unreadable paths carry null"


def _check_sl_enum(pulses, expect):
    """Enum/domain validity: cd.state and cd.source in-vocabulary, power keyed by a
    real Enum.PowerType name."""
    skip = _no_pulses(pulses)
    if skip:
        return skip
    bad = []
    for i, p in enumerate(pulses):
        for c in _cooldowns(p):
            cd = _asdict(c.get("cd"))
            st, src = cd.get("state"), cd.get("source")
            if st not in _CD_STATES:
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: cd.state={st!r}")
            if src is not None and src not in _CD_SOURCES:
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: cd.source={src!r}")
        for name in _powers(p):
            if str(name) not in _POWER_TYPES:
                bad.append(f"pulse#{i}: power keyed by {name!r} (not a real power-type)")
        for h in _aslist(p.get("history")):
            ph = _asdict(h).get("phase")
            if ph not in ("start", "succeeded"):
                bad.append(f"pulse#{i}: history phase={ph!r} (not start/succeeded)")
    if bad:
        return FAIL, "; ".join(bad[:4]) + (f" (+{len(bad) - 4} more)" if len(bad) > 4 else "")
    return PASS, f"{len(pulses)} pulse(s): cd.state/source, power keys, history phases all in-domain"


def _check_sl_napkin(pulses, expect):
    """The napkin honesty rule, on disk: an estimate never claims readiness. A cd
    sourced 'napkin' is anticipated (remaining>0) or unknown (no remaining) — never
    'ready'; and NO cd of any source is 'ready' unless it was a live read."""
    skip = _no_pulses(pulses)
    if skip:
        return skip
    bad = []
    for i, p in enumerate(pulses):
        for c in _cooldowns(p):
            cd = _asdict(c.get("cd"))
            st, src, rem = cd.get("state"), cd.get("source"), cd.get("remaining")
            if src == "napkin":
                if st == "ready":
                    bad.append(f"pulse#{i} cd{c.get('cooldownID')}: napkin cd claims READY")
                elif st == "anticipated" and not (isinstance(rem, (int, float)) and rem > 0):
                    bad.append(f"pulse#{i} cd{c.get('cooldownID')}: anticipated but remaining={rem!r}")
                elif st == "unknown" and rem is not None:
                    bad.append(f"pulse#{i} cd{c.get('cooldownID')}: unknown estimate carries remaining")
            if st == "ready" and src != "live":
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: READY from source={src!r} (only a live read may)")
    if bad:
        return FAIL, "; ".join(bad[:4]) + (f" (+{len(bad) - 4} more)" if len(bad) > 4 else "")
    return PASS, f"{len(pulses)} pulse(s): no estimate claims readiness"


def _check_sl_identity(pulses, expect):
    """Identity coherence (B1): a live identity never diverges from the base without
    a source. liveSpellID must equal spellID unless an override field or an observed
    transform target explains the divergence; and a liveSpellID implies a base."""
    skip = _no_pulses(pulses)
    if skip:
        return skip
    targets = _transform_targets(pulses)
    bad = []
    for i, p in enumerate(pulses):
        for c in _cooldowns(p):
            base = c.get("spellID")
            live = c.get("liveSpellID")
            if live is not None and base is None:
                bad.append(f"pulse#{i} cd{c.get('cooldownID')}: liveSpellID with no base spellID")
                continue
            if live is None or base is None or live == base:
                continue
            homes = {c.get("overrideSpellID"), c.get("overrideTooltipSpellID")}
            if live in homes or live in targets:
                continue
            bad.append(f"pulse#{i} cd{c.get('cooldownID')}: liveSpellID={live} diverges from "
                       f"base={base} with no override/transform source")
    if bad:
        return FAIL, "; ".join(bad[:4]) + (f" (+{len(bad) - 4} more)" if len(bad) > 4 else "")
    return PASS, f"{len(pulses)} pulse(s): live identity coherent with the raw ids"


def _check_sl_spec_agnostic(pulses, expect):
    """Invariant #3: no rotation/spec vocabulary leaked into a State entry."""
    skip = _no_pulses(pulses)
    if skip:
        return skip
    bad = []
    for i, p in enumerate(pulses):
        for c in _cooldowns(p):
            for k in c:
                if str(k).lower() in _SPEC_DENYLIST:
                    bad.append(f"pulse#{i} cd{c.get('cooldownID')}: spec key {k!r} in State")
    if bad:
        return FAIL, "; ".join(sorted(set(bad))[:4])
    return PASS, f"{len(pulses)} pulse(s): no spec/rotation keys — State stays spec-agnostic"


# ── Coverage checks — PASS when the moment is in the corpus, SKIP when it is not ──

def _check_sl_cov_contexts(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    ooc = any(not _asdict(p).get("combat") for p in pulses)
    combat = any(_asdict(p).get("combat") for p in pulses)
    if ooc and combat:
        return PASS, "both OOC and in-combat pulses captured"
    have = ", ".join(x for x, ok in (("OOC", ooc), ("combat", combat)) if ok) or "neither"
    return SKIP, f"only {have} captured — need both (pull a dummy, and sample OOC)"


def _check_sl_cov_secret(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    for p in pulses:
        for c in _cooldowns(p):
            if _asdict(c.get("cd")).get("readable") is False:
                return PASS, "an unreadable/secret live cd was captured"
    return SKIP, "no unreadable cd yet (the secret path fires in combat — pull a dummy)"


def _check_sl_cov_napkin(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    for p in pulses:
        for c in _cooldowns(p):
            if _asdict(c.get("cd")).get("source") == "napkin":
                return PASS, "a napkin-sourced cd was captured"
    return SKIP, "no napkin-sourced cd (cast a cooldown in combat, then re-capture)"


def _check_sl_cov_shards(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    vals = set()
    for p in pulses:
        ss = _asdict(_powers(p).get("SoulShards"))
        if isinstance(ss.get("value"), int):
            vals.add(ss["value"])
    if len(vals) >= 2:
        return PASS, f"a shard spread captured (values {sorted(vals)})"
    return SKIP, f"shard values seen: {sorted(vals) or 'none'} — need a spread (spend + generate)"


def _check_sl_cov_transform(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    if _transform_targets(pulses):
        return PASS, f"transform(s) observed: {sorted(_transform_targets(pulses))}"
    return SKIP, "no transform observed (arm a Demonic Art / let a Grimoire hit CD)"


def _check_sl_cov_proc(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    for p in pulses:
        for c in _cooldowns(p):
            if _asdict(c.get("aura")).get("active") is True:
                return PASS, f"a proc aura was observed active (cd{c.get('cooldownID')})"
    # Combat auras are secret, so the combat proc signal is the GLOW, not the aura.
    for p in pulses:
        if p.get("combat"):
            for c in _cooldowns(p):
                if _asdict(c.get("glow")).get("active") is True:
                    return PASS, f"a combat proc-glow was observed (cd{c.get('cooldownID')} glowing)"
    return SKIP, ("no proc observed — an aura active OOC, or a proc-glow in combat "
                  "(combat auras are secret; the glow is the readable combat signal)")


def _check_sl_cov_history(pulses, expect):
    skip = _no_pulses(pulses)
    if skip:
        return skip
    phases = set()
    for p in pulses:
        for h in _aslist(_asdict(p).get("history")):
            ph = _asdict(h).get("phase")
            if ph in ("start", "succeeded"):
                phases.add(ph)
    if {"start", "succeeded"} <= phases:
        return PASS, "cast history captured with both start and succeeded phases"
    if phases:
        return SKIP, f"history has only {sorted(phases)} — need both a START (cast-time spell) and a SUCCEEDED"
    return SKIP, "no cast history captured (cast something while recording)"


STATELOG_CHECKS = {
    "statelog-secrecy": _check_sl_secrecy,
    "statelog-enum-domain": _check_sl_enum,
    "statelog-napkin-honesty": _check_sl_napkin,
    "statelog-identity-coherence": _check_sl_identity,
    "statelog-spec-agnostic": _check_sl_spec_agnostic,
    "statelog-coverage-contexts": _check_sl_cov_contexts,
    "statelog-coverage-secret": _check_sl_cov_secret,
    "statelog-coverage-napkin": _check_sl_cov_napkin,
    "statelog-coverage-shards": _check_sl_cov_shards,
    "statelog-coverage-transform": _check_sl_cov_transform,
    "statelog-coverage-proc": _check_sl_cov_proc,
    "statelog-coverage-history": _check_sl_cov_history,
}


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


def _run_statelog(statelog: dict, baseline: dict) -> tuple[list, int]:
    """Run the statelog baseline block against the captured pulses.

    Returns (results, hard_fails) where results is a list of (status, aid, a, detail),
    the same shape the probe block produces, so cmd_check can render them uniformly.
    """
    pulses = _statelog_pulses(statelog)
    results, hard_fails = [], 0
    for a in _aslist(_asdict(baseline.get("statelog")).get("assumptions")):
        aid = a.get("id")
        fn = STATELOG_CHECKS.get(aid)
        if fn is None:
            results.append((FAIL, aid, a, "no statelog check function for this id (see STATELOG_CHECKS in cdmp.py)"))
            hard_fails += 1
            continue
        try:
            status, detail = fn(pulses, _asdict(a.get("expect")))
        except Exception as e:  # noqa: BLE001 — a broken check must not look like a pass
            status, detail = FAIL, f"check raised {type(e).__name__}: {e}"
        if status == FAIL and (a.get("severity") or "medium").lower() == "high":
            hard_fails += 1
        results.append((status, aid, a, detail))
    return results, hard_fails


def _print_results(results: list) -> tuple[int, int, list]:
    """Render a block of (status, aid, a, detail) rows; return (hard_fails, passed, skipped)."""
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
    passed = sum(1 for s, _, _, _ in results if s == PASS)
    skipped = [(aid, a) for status, aid, a, _ in results if status == SKIP]
    return hard_fails, passed, skipped


def cmd_check(probe: dict, pulls: dict, statelog: dict, path: str,
              baseline: dict, bl_path: Path) -> int:
    _print_header(probe, path)
    if not probe and not _statelog_pulses(statelog):
        print("\nNo structured probe capture (CDMProbeDB.probe is empty).", file=sys.stderr)
        print("Needs CDMProbe v0.25.0+: run /cdmp probe (or /cdmp statelog), then /reload.",
              file=sys.stderr)
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

    # The statelog block runs on its own capture (CDMProbeDB.statelog), rendered
    # beside the probe block but tallied together. When no statelog exists yet every
    # entry reports 'not covered' — the same absence-is-not-evidence discipline.
    sl_results, _ = _run_statelog(statelog, baseline)

    print()
    hf1, _p1, _s1 = _print_results(results)
    if sl_results:
        print("\n  ── statelog (W4 Phase-1 fixture gate: State contract + corpus coverage) ──")
        hf2, _p2, _s2 = _print_results(sl_results)
    else:
        hf2 = 0

    all_results = results + sl_results
    hard_fails = hf1 + hf2

    skipped = [(aid, a) for status, aid, a, _ in all_results if status == SKIP]
    if skipped:
        print(f"\nnot covered this run ({len(skipped)}) — the capture lacks the evidence, "
              "which is NOT a pass:")
        for aid, a in skipped:
            print(f"  · {aid} — {a.get('desc')}")
        print("  (in-game: /cdmp probe guide and /cdmp statelog guide say which you can still close)")

    # Stamp ages: a check that passes against a year-old stamp is a check that
    # has not actually run this patch.  The `context` prose is only unfolded for
    # results that need reading — on an all-green run it is noise that buries
    # the one line you came for.
    print("\nassumption stamps:")
    for status, aid, a, _ in all_results:
        print(f"  {aid:<28} confirmed {_stamp_age(a.get('confirmed'))}")
        ctx = a.get("context")
        if ctx and status != PASS:
            print(f"  {'':<28}   ↳ {ctx}")

    _print_pulls(pulls, brief=True)

    passed = sum(1 for s, _, _, _ in all_results if s == PASS)
    warns = sum(1 for s, _, a, _ in all_results
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


def _show_statelog(statelog: dict) -> None:
    pulses = _statelog_pulses(statelog)
    if not pulses:
        return
    sl = _asdict(statelog)
    print(f"\n── statelog ({len(pulses)} pulse(s) in ring, {sl.get('count', '?')} captured, "
          f"started {sl.get('startedAt', '?')}) ──")
    for p in pulses:
        p = _asdict(p)
        cds = _cooldowns(p)
        readable = sum(1 for c in cds if _asdict(c.get("cd")).get("readable"))
        procs = sum(1 for c in cds if _asdict(c.get("aura")).get("active"))
        glows = sum(1 for c in cds if _asdict(c.get("glow")).get("active"))
        ss = _asdict(_powers(p).get("SoulShards"))
        evk = ",".join(sorted({str(e.get("kind")) for e in _events(p)})) or "-"
        buffs = len(_active_auras(p))
        hist = len(_aslist(p.get("history")))
        print(f"  #{p.get('seq', '?'):<3} {p.get('reason', '?'):<9} "
              f"{'combat' if p.get('combat') else 'ooc':<6}  "
              f"cds={len(cds)} ({readable} live-readable, {procs} aura-proc, {glows} glow)  "
              f"buffs={buffs}  hist={hist}  shards={ss.get('value', '?')}/{ss.get('max', '?')}  events=[{evk}]")


def _active_auras(pulse) -> list:
    return [_asdict(a) for a in _aslist(_asdict(pulse).get("activeAuras"))]


def cmd_focus(statelog: dict, focus: str) -> int:
    """Narrow the statelog dump to one spell — by spellID, by name substring, or the
    special `auras` to list every distinct active buff seen (the discovery dump).

    This is how we chase a proc whose CDM entry's spellID does NOT match the buff's
    real aura id: `--focus "Demonic Core"` finds the active buff by NAME across the
    capture and prints its true spellID, which the entry never carried."""
    pulses = _statelog_pulses(statelog)
    if not pulses:
        print("No statelog pulses (/cdmp statelog, play, /reload).")
        return 1
    focus_id = int(focus) if str(focus).isdigit() else None
    focus_lc = str(focus).lower()

    # Special: list every distinct active buff seen, with how often — the discovery dump.
    if focus_lc == "auras":
        seen: dict = {}
        for p in pulses:
            for a in _active_auras(p):
                sid = a.get("spellID")
                if isinstance(sid, int):
                    e = seen.setdefault(sid, {"name": a.get("name"), "n": 0})
                    e["n"] += 1
        print(f"\n── distinct active buffs across {len(pulses)} pulses ──")
        for sid, e in sorted(seen.items(), key=lambda kv: -kv[1]["n"]):
            print(f"  {sid:<10} {str(e['name'] or '?'):<28} seen in {e['n']} pulse(s)")
        secret = sum(int(_asdict(p).get("activeAuraSecret") or 0) for p in pulses)
        if secret:
            print(f"  (+ {secret} aura-reads across pulses were secret/unreadable — combat-gated)")
        return 0

    print(f"\n── statelog focus: {focus!r} ──")
    hits = 0
    for p in pulses:
        p = _asdict(p)
        cd_matches = []
        for c in _cooldowns(p):
            ids = {c.get("spellID"), c.get("liveSpellID"),
                   c.get("overrideSpellID"), c.get("overrideTooltipSpellID")}
            if focus_id and focus_id in ids:
                cd_matches.append(c)
        aura_matches = [a for a in _active_auras(p)
                        if (focus_id and a.get("spellID") == focus_id)
                        or (not focus_id and focus_lc in str(a.get("name") or "").lower())]
        if not cd_matches and not aura_matches:
            continue
        hits += 1
        print(f"  #{p.get('seq')} {p.get('reason')} {'combat' if p.get('combat') else 'ooc':<6}:")
        for c in cd_matches:
            print(f"     cd[{c.get('cooldownID')}] spellID={c.get('spellID')} live={c.get('liveSpellID')} "
                  f"selfAura={c.get('selfAura')} hasAura={c.get('hasAura')}")
            print(f"        aura={json.dumps(c.get('aura'))}  glow={json.dumps(c.get('glow'))}")
            if c.get("buff") is not None:
                print(f"        buff={json.dumps(c.get('buff'))}")
        for a in aura_matches:
            print(f"     ACTIVE BUFF: spellID={a.get('spellID')} name={a.get('name')!r}")
    if not hits:
        print(f"  no cooldown entry or active buff matched {focus!r}. "
              f"Try `--focus auras` to list every active buff seen.")
    return 0


def cmd_show(probe: dict, pulls: dict, statelog: dict, path: str) -> int:
    _print_header(probe, path)
    if not probe and not _statelog_pulses(statelog):
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

    _show_statelog(statelog)
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
# The goldens checks — the W4 Phase-2 corpus validator                         #
# --------------------------------------------------------------------------- #
# Validates the hand-authored State->Guidance goldens under
# projects/cooldown-hud/corpus/goldens/ against BOTH contracts:
#   * state.json    -> the State-contract invariants, REUSED from the statelog
#                      block. A golden's synthetic State is one pulse, and it must
#                      be as realizable as a real captured one (that reuse is the
#                      whole point of the synthetic-baseline decision).
#   * guidance.json -> guidance-contract.json (token vocab, no RGBA, single-top-
#                      press, cue anchored in state, the secrecy gate).
# RANKING CORRECTNESS is NOT machine-checked here — that is the rationale + the
# adversarial verify stage. This gates FORMAT + CONTRACT + SECRECY only.

# The State-contract invariants (the statelog fixture gate), reused per golden.
# NOT the corpus-COVERAGE checks — those are about a ring having diverse moments,
# which is meaningless for a single hand-authored pulse.
_GOLDEN_STATE_CHECKS = {
    "state-secrecy": _check_sl_secrecy,
    "state-enum-domain": _check_sl_enum,
    "state-napkin-honesty": _check_sl_napkin,
    "state-identity-coherence": _check_sl_identity,
    "state-spec-agnostic": _check_sl_spec_agnostic,
}


def _contract_vocab(contract: dict) -> dict:
    """The bounded token sets from guidance-contract.json — so the validator tracks
    the committed contract instead of hardcoding a second copy."""
    v = _asdict(contract.get("vocabularies"))

    def members(name):
        return set(_asdict(_asdict(v.get(name)).get("members")).keys())

    return {
        "emphasis": members("emphasis"),
        "transient": members("transient"),
        "stepState": members("stepState"),
        "display": members("resourceDisplay"),
    }


def _is_rgba(x) -> bool:
    """A list of numbers = a resolved colour, which must never appear in Guidance."""
    return isinstance(x, list) and bool(x) and all(isinstance(n, (int, float)) for n in x)


def _check_guidance(state: dict, guidance: dict, vocab: dict) -> list:
    """Guidance-contract violations for one golden (empty list = clean)."""
    errs = []
    PRESS = {"ROTATION", "LATE"}
    cds = _asdict(state.get("cooldowns"))
    cues = _asdict(guidance.get("cues"))

    press = []
    for k, c in cues.items():
        c = _asdict(c)
        if not c.get("draw"):
            continue  # unlisted / draw:false = AVAILABLE, not a cue
        emph = c.get("emphasis")
        if emph not in vocab["emphasis"]:
            errs.append(f"cue {k}: emphasis {emph!r} not in {sorted(vocab['emphasis'])}")
        if emph in PRESS:
            press.append(str(k))
        if str(k) not in cds:
            errs.append(f"cue {k}: not anchored in state.cooldowns")
        tr = c.get("transient")
        if tr is not None and tr not in vocab["transient"]:
            errs.append(f"cue {k}: transient {tr!r} not in {sorted(vocab['transient'])}")
        if c.get("note") is not None and not isinstance(c.get("note"), str):
            errs.append(f"cue {k}: note must be a pass-through string")
        for kk, vv in c.items():
            if _is_rgba(vv):
                errs.append(f"cue {k}: field {kk!r} is an RGBA list (no pixels in Guidance)")
    if len(press) > 1:
        errs.append(f"single-top-press violated: {press} all carry ROTATION/LATE")

    rb = _asdict(guidance.get("resourceBar"))
    if rb:
        if "color" in rb or any(_is_rgba(x) for x in rb.values()):
            errs.append("resourceBar carries a raw colour (emit powerType, not RGBA)")
        if not rb.get("powerType"):
            errs.append("resourceBar missing powerType token")
        disp = rb.get("display")
        if disp is not None and disp not in vocab["display"]:
            errs.append(f"resourceBar.display {disp!r} not in {sorted(vocab['display'])}")

    for i, step in enumerate(_aslist(_asdict(guidance.get("sequence")).get("steps"))):
        stt = _asdict(step).get("state")
        if stt is not None and stt not in vocab["stepState"]:
            errs.append(f"sequence.steps[{i}].state {stt!r} not in {sorted(vocab['stepState'])}")

    # Secrecy gate (mechanical half): in a COMBAT fixture a drawn cue must not rest
    # on a LIVE-readable cd read — combat cds are secret, so a drawn cue anchored on
    # one is a fixture that lets the Coach cheat. (The full justification — that the
    # cue follows from napkin/buff/glow/shards — is the rationale + verify stage.)
    if state.get("combat"):
        for k, c in cues.items():
            if not _asdict(c).get("draw"):
                continue
            cd = _asdict(_asdict(cds.get(str(k))).get("cd"))
            if cd.get("readable") is True and cd.get("source") == "live":
                errs.append(f"cue {k}: drawn off a LIVE-readable cd in combat "
                            f"(combat cds are secret — expected napkin/none)")
    return errs


def cmd_goldens(goldens_dir: Path, contract_path: Path) -> int:
    if not goldens_dir.exists():
        print(f"Goldens dir not found: {goldens_dir}", file=sys.stderr)
        return 1
    if not contract_path.exists():
        print(f"Contract not found: {contract_path}", file=sys.stderr)
        return 1
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    vocab = _contract_vocab(contract)

    scenarios = sorted(p for p in goldens_dir.iterdir()
                       if p.is_dir() and (p / "state.json").exists())
    if not scenarios:
        print(f"No scenarios (a <dir>/state.json) under {goldens_dir}.", file=sys.stderr)
        return 1

    print(f"goldens  — {goldens_dir}")
    print(f"contract — {contract_path.name} v{contract.get('version', '?')}\n")

    fails = 0
    for sc in scenarios:
        name = sc.name
        try:
            state = json.loads((sc / "state.json").read_text(encoding="utf-8"))
            guidance = json.loads((sc / "guidance.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"[FAIL] {name}: parse error — {e}")
            fails += 1
            continue

        errs = []
        for cid, fn in _GOLDEN_STATE_CHECKS.items():
            status, detail = fn([state], {})
            if status == FAIL:
                errs.append(f"{cid}: {detail}")
        errs += _check_guidance(state, guidance, vocab)

        if errs:
            fails += 1
            print(f"[FAIL] {name}")
            for e in errs:
                print(f"         - {e}")
        else:
            cues = _asdict(guidance.get("cues"))
            lit = ", ".join(f"{k}:{_asdict(c).get('emphasis')}"
                            for k, c in cues.items() if _asdict(c).get("draw"))
            print(f"[PASS] {name:18} {lit or '(no cues)'}")

    print(f"\n{len(scenarios) - fails} pass · {fails} fail")
    return 1 if fails else 0


# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Read and assert CDMProbe /cdmp probe captures.")
    ap.add_argument("command", choices=["check", "show", "diff", "goldens"])
    ap.add_argument("subcommand", nargs="?", help="goldens: 'check' (default; only value accepted)")
    ap.add_argument("--wow-path", default=DEFAULT_WOW,
                    help=f"WoW _retail_ path (default: {DEFAULT_WOW})")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE),
                    help=f"assumptions-of-record JSON (default: {DEFAULT_BASELINE})")
    ap.add_argument("--goldens-dir", default=str(DEFAULT_GOLDENS),
                    help=f"goldens: corpus dir (default: {DEFAULT_GOLDENS})")
    ap.add_argument("--contract", default=str(DEFAULT_CONTRACT),
                    help=f"goldens: guidance contract JSON (default: {DEFAULT_CONTRACT})")
    ap.add_argument("--json", action="store_true",
                    help="show: dump the raw capture as JSON (archive it to diff against later)")
    ap.add_argument("--against", help="diff: compare against a JSON capture exported by `show --json`")
    ap.add_argument("--focus", help="show: narrow the statelog dump to a spell — a spellID, a name "
                    "substring (matched against active-buff names), or 'auras' to list every active buff seen")
    args = ap.parse_args(argv)

    # goldens reads the on-disk corpus, not a WoW SavedVariables capture, so it
    # dispatches before load_capture (no game install required).
    if args.command == "goldens":
        return cmd_goldens(Path(args.goldens_dir), Path(args.contract))

    loaded = load_capture(args.wow_path)
    if loaded is None:
        print(f"No readable CDMProbe.lua under "
              f"{args.wow_path}/WTF/Account/*/SavedVariables/.", file=sys.stderr)
        print("Run /cdmp probe in-game and /reload first.", file=sys.stderr)
        return 1
    probe, pulls, statelog, path = loaded

    if args.command == "show" and args.json:
        print(json.dumps({"probe": probe, "pulls": pulls, "statelog": statelog,
                          "_path": path},
                         indent=2, ensure_ascii=False, sort_keys=True, default=str))
        return 0
    if args.command == "show" and args.focus:
        return cmd_focus(statelog, args.focus)
    if args.command == "show":
        return cmd_show(probe, pulls, statelog, path)
    if args.command == "diff":
        return cmd_diff(probe, path, args.against)

    bl_path = Path(args.baseline)
    if not bl_path.exists():
        print(f"Baseline not found: {bl_path}", file=sys.stderr)
        return 1
    baseline = json.loads(bl_path.read_text(encoding="utf-8"))
    return cmd_check(probe, pulls, statelog, path, baseline, bl_path)


if __name__ == "__main__":
    raise SystemExit(main())

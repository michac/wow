"""Manage the three gitignored sub-repo addons (BucketBinds, CDMProbe, PlannerState).

These live at fixed paths inside the workspace but are **separate git repos**,
gitignored here so the wow repo never sees them as embedded repos. That decoupling
has one sharp edge: a `git pull` of the wow repo updates the docs/tooling and is
completely blind to whether the addon clones exist or are current — so a fresh
machine silently ends up with new prose describing addon code it doesn't have.
This tool is the single door that closes that gap and owns the mechanical release
recipe the per-addon CLAUDE.md files used to spell out by hand.

    uv run python -m wowkb.addon list                 # presence + versions + drift
    uv run python -m wowkb.addon pull [--all|bb cdmp] # clone-if-missing + pull (machine-B fix)
    uv run python -m wowkb.addon release bb --minor    # bump→lint→commit→push→gh release→deploy
    uv run python -m wowkb.addon deploy cdmp           # redeploy latest release, no new cut

Short names are the in-game slash prefixes (`bb`, `cdmp`, `ps`); a repo-relative
path also resolves. The registry (repo↔path↔toc) is the source of truth for the
addon set — `list` is the LIVE version signal, so never hardcode addon versions
in prose, run it. `pull` is why root CLAUDE.md tells the agent to sync on session
start: the tracked wow-repo pull does NOT fetch these separate repos.

The per-addon CLAUDE.md keeps the "why" (design, milestones); this owns the "how".
"""

from __future__ import annotations

import argparse
import glob as globmod
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # wow/
GAME_VERSION = REPO / "knowledge" / "_meta" / "game-version.md"
GHADDONS_PKG = REPO / "addon-manager"


class Addon:
    def __init__(self, short, repo, path, toc, lua_glob, reload_hint, schema_note=False):
        self.short = short              # slash-prefix short name
        self.repo = repo                # owner/repo on GitHub
        self.path = REPO / path         # local checkout root
        self.toc = self.path / toc      # .toc within the checkout
        self.lua_glob = lua_glob        # glob (relative to checkout) for the syntax check
        self.reload_hint = reload_hint  # in-game confirm command
        self.schema_note = schema_note  # warn about a companion schema bump on release

    @property
    def rel(self) -> str:
        return self.path.relative_to(REPO).as_posix()


REGISTRY = {
    "bb": Addon("bb", "michac/BucketBinds", "projects/keybinder/addon",
                "BucketBinds/BucketBinds.toc", "BucketBinds/*.lua", "/bb status"),
    "cdmp": Addon("cdmp", "michac/CDMProbe", "projects/cooldown-hud/addon",
                  "CDMProbe/CDMProbe.toc", "CDMProbe/*.lua", "/cdmp help"),
    "ps": Addon("ps", "michac/wow-planner-state", "planner-state",
                "PlannerState/PlannerState.toc", "PlannerState/*.lua", "/ps",
                schema_note=True),
}


# ----------------------------------------------------------------------------- subprocess helpers


def run(cmd, cwd=None, env=None, check=True, capture=True):
    """Thin subprocess wrapper. Returns CompletedProcess; raises on non-zero if check."""
    return subprocess.run(
        cmd, cwd=cwd, env=env, check=check, text=True,
        capture_output=capture,
    )


def git(addon: Addon, *args, check=True, capture=True):
    return run(["git", "-C", str(addon.path), *args], check=check, capture=capture)


def git_out(addon: Addon, *args) -> str:
    return git(addon, *args).stdout.strip()


def gh_latest_release(addon: Addon) -> str | None:
    """Latest release tag from GitHub, or None (offline / no releases / no gh)."""
    try:
        cp = run(["gh", "release", "list", "--repo", addon.repo, "--limit", "1",
                  "--json", "tagName"], check=False)
    except FileNotFoundError:
        return None
    if cp.returncode != 0 or not cp.stdout.strip():
        return None
    try:
        data = json.loads(cp.stdout)
    except json.JSONDecodeError:
        return None
    return data[0]["tagName"] if data else None


def ghaddons(*args, check=True, capture=True):
    env = dict(os.environ, PYTHONPATH=str(GHADDONS_PKG))
    return run(["python3", "-m", "ghaddons.cli", *args], env=env, check=check, capture=capture)


# ----------------------------------------------------------------------------- version helpers

_VER_RE = re.compile(r"^(##\s*Version:\s*)(\d+)\.(\d+)\.(\d+)\s*$", re.MULTILINE)
_IFACE_RE = re.compile(r"^##\s*Interface:\s*(\d+)\s*$", re.MULTILINE)


def toc_version(addon: Addon) -> tuple[int, int, int]:
    m = _VER_RE.search(addon.toc.read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"error: no '## Version: X.Y.Z' line in {addon.toc.relative_to(REPO)}")
    return int(m.group(2)), int(m.group(3)), int(m.group(4))


def toc_interface(addon: Addon) -> str | None:
    m = _IFACE_RE.search(addon.toc.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def bump(ver: tuple[int, int, int], part: str) -> tuple[int, int, int]:
    maj, minr, pat = ver
    if part == "major":
        return maj + 1, 0, 0
    if part == "minor":
        return maj, minr + 1, 0
    return maj, minr, pat + 1


def write_toc_version(addon: Addon, ver: tuple[int, int, int]) -> None:
    text = addon.toc.read_text(encoding="utf-8")
    text = _VER_RE.sub(rf"\g<1>{ver[0]}.{ver[1]}.{ver[2]}", text, count=1)
    addon.toc.write_text(text, encoding="utf-8")


def expected_interface() -> str | None:
    """'12.0.7' -> '120007' from game-version.md front matter."""
    if not GAME_VERSION.exists():
        return None
    m = re.search(r"^patch:\s*(\d+)\.(\d+)\.(\d+)", GAME_VERSION.read_text(encoding="utf-8"),
                  re.MULTILINE)
    if not m:
        return None
    return f"{int(m.group(1))}{int(m.group(2)):02d}{int(m.group(3)):02d}"


def vstr(ver: tuple[int, int, int]) -> str:
    return f"{ver[0]}.{ver[1]}.{ver[2]}"


# ----------------------------------------------------------------------------- resolve


def resolve(token: str) -> Addon:
    if token in REGISTRY:
        return REGISTRY[token]
    # accept a repo-relative or absolute path pointing at a checkout
    p = (REPO / token).resolve() if not Path(token).is_absolute() else Path(token).resolve()
    for a in REGISTRY.values():
        if a.path.resolve() == p:
            return a
    sys.exit(f"error: unknown addon '{token}' — known: {', '.join(REGISTRY)}")


# ----------------------------------------------------------------------------- commands


def cmd_list(_args) -> int:
    rows = []
    for a in REGISTRY.values():
        if not a.path.exists():
            rows.append((a.short, "—", "—", "—", "MISSING — run `addon pull`"))
            continue
        head = git_out(a, "log", "-1", "--pretty=%h %s")
        head = head[:44] + "…" if len(head) > 45 else head
        try:
            tv = vstr(toc_version(a))
        except SystemExit:
            tv = "?"
        rel = gh_latest_release(a) or "(offline?)"
        dirty = bool(git(a, "status", "--porcelain").stdout.strip())
        drift = _drift(a, tv, rel, dirty)
        rows.append((a.short, head, tv, rel, drift))

    w = [max(len(str(r[i])) for r in ([("name", "local HEAD", ".toc", "release", "drift")] + rows))
         for i in range(5)]
    hdr = ("name", "local HEAD", ".toc", "release", "drift")
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(hdr)))
    print("  ".join("-" * w[i] for i in range(5)))
    for r in rows:
        print("  ".join(str(r[i]).ljust(w[i]) for i in range(5)))
    return 0


def _drift(a: Addon, toc_v: str, release: str, dirty: bool) -> str:
    bits = []
    if release.startswith("v"):
        rel_v = release[1:]
        tag = release
        # unreleased commits after the latest release tag (if the tag is local)
        if git(a, "rev-parse", "-q", "--verify", f"refs/tags/{tag}", check=False).returncode == 0:
            n = git_out(a, "rev-list", "--count", f"{tag}..HEAD")
            if n and n != "0":
                bits.append(f"{n} commit(s) unreleased")
        if toc_v != "?" and _cmp(toc_v, rel_v) < 0:
            bits.append("BEHIND release — pull")
        elif toc_v != "?" and _cmp(toc_v, rel_v) > 0:
            bits.append("toc ahead (release pending)")
    if dirty:
        bits.append("dirty tree")
    return ", ".join(bits) if bits else "in sync"


def _cmp(a: str, b: str) -> int:
    ta = tuple(int(x) for x in a.split("."))
    tb = tuple(int(x) for x in b.split("."))
    return (ta > tb) - (ta < tb)


def cmd_pull(args) -> int:
    targets = list(REGISTRY.values()) if (args.all or not args.names) \
        else [resolve(t) for t in args.names]
    rc = 0
    for a in targets:
        if not a.path.exists():
            print(f"[{a.short}] cloning {a.repo} → {a.rel} …")
            cp = run(["gh", "repo", "clone", a.repo, str(a.path)], check=False, capture=False)
            if cp.returncode != 0:
                print(f"[{a.short}] clone FAILED", file=sys.stderr)
                rc = 1
            continue
        print(f"[{a.short}] pull {a.rel} …")
        cp = git(a, "pull", "--ff-only", check=False)
        out = (cp.stdout + cp.stderr).strip()
        print(f"[{a.short}] {out.splitlines()[-1] if out else 'ok'}")
        if cp.returncode != 0:
            print(f"[{a.short}] pull FAILED (not fast-forward? commit/stash first)", file=sys.stderr)
            rc = 1
    return rc


def cmd_check(args) -> int:
    """Report addons with LOCAL-ONLY work (uncommitted or unpushed) — exit 1 if any.

    The push-safety gate: before pushing THIS repo, make sure no addon has commits
    stranded on this machine. Fetches the tracking ref first (skip with --no-fetch)
    so 'unpushed' is accurate.
    """
    any_local = False
    for a in REGISTRY.values():
        if not a.path.exists():
            print(f"[{a.short}] MISSING — run `addon pull`")
            any_local = True
            continue
        if not args.no_fetch:
            git(a, "fetch", "--quiet", check=False)
        dirty = bool(git(a, "status", "--porcelain").stdout.strip())
        # ahead of upstream tracking ref = committed but not pushed
        up = git(a, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
        bits = []
        if up.returncode != 0:
            bits.append("no upstream tracking branch")
        else:
            ahead = git_out(a, "rev-list", "--count", "@{u}..HEAD")
            if ahead and ahead != "0":
                bits.append(f"{ahead} commit(s) not pushed → `git -C {a.rel} push`")
        if dirty:
            bits.append("uncommitted changes → commit first")
        if bits:
            any_local = True
            print(f"[{a.short}] LOCAL-ONLY: {'; '.join(bits)}")
        else:
            print(f"[{a.short}] clean — pushed & committed")
    if any_local:
        print("\n→ addon work exists only on this machine. Push it before/with the "
              "wow-repo push (or `addon release` if it should ship).")
    return 1 if any_local else 0


def cmd_deploy(args) -> int:
    a = resolve(args.name)
    if not a.path.exists():
        sys.exit(f"error: {a.rel} not present — run `addon pull {a.short}`")
    print(f"[{a.short}] ghaddons update {a.repo} …")
    cp = ghaddons("update", a.repo, check=False, capture=False)
    if cp.returncode != 0:
        return cp.returncode
    print(f"[{a.short}] deployed. In-game: /reload, then {a.reload_hint}")
    return 0


def cmd_release(args) -> int:
    a = resolve(args.name)
    if not a.path.exists():
        sys.exit(f"error: {a.rel} not present — run `addon pull {a.short}`")

    # 1. Clean-tree guard: feature work must already be committed, so the version
    #    bump commit never sweeps up unrelated edits.
    if git(a, "status", "--porcelain").stdout.strip():
        sys.exit(f"error: {a.rel} has uncommitted changes — commit your work first, "
                 f"then release just bumps + tags + deploys")

    # 2. Bump the .toc version.
    part = "major" if args.major else "minor" if args.minor else "patch"
    old = toc_version(a)
    new = bump(old, part)
    tag = f"v{vstr(new)}"
    print(f"[{a.short}] {vstr(old)} → {vstr(new)} ({part})")

    # 3. Interface sanity (warn, don't block).
    exp, have = expected_interface(), toc_interface(a)
    if exp and have and exp != have:
        print(f"[{a.short}] ⚠ Interface {have} != live patch {exp} "
              f"(game-version.md) — fix the .toc if this is wrong", file=sys.stderr)

    # 3b. PlannerState schema reminder.
    if a.schema_note:
        print(f"[{a.short}] ⚠ PlannerState: if the /ps dump format changed, bump the "
              f"`schema` field in the Lua too — this tool does NOT touch it.", file=sys.stderr)

    # 4. Lua syntax check (the documented luaparser one-liner).
    if not args.skip_lint:
        files = sorted(globmod.glob(str(a.path / a.lua_glob)))
        if not files:
            sys.exit(f"error: no lua matched {a.lua_glob} under {a.rel}")
        code = ("import luaparser.ast as A,sys;"
                "[A.parse(open(f,encoding='utf-8').read()) for f in sys.argv[1:]];"
                "print('lua OK')")
        print(f"[{a.short}] luaparser check ({len(files)} file(s)) …")
        cp = run(["uv", "run", "--with", "luaparser", "python", "-c", code, *files],
                 cwd=str(a.path), check=False)
        if cp.returncode != 0:
            print(cp.stdout, cp.stderr, file=sys.stderr)
            sys.exit(f"error: lua syntax check FAILED — aborting release")

    if args.dry_run:
        print(f"[{a.short}] --dry-run: would commit {tag}, push, gh release, ghaddons deploy. "
              f"Reverting .toc write.")
        write_toc_version(a, old)  # undo the in-place bump
        return 0

    # 5. Write + commit the bump.
    write_toc_version(a, new)
    git(a, "commit", "-am", f"release: {tag}")

    # 6. Push + cut the GitHub release (tag == .toc version). Notes default to the
    #    commit log since the previous release tag.
    git(a, "push")
    notes = args.notes
    if not notes:
        prev = gh_latest_release(a)
        if prev and git(a, "rev-parse", "-q", "--verify", f"refs/tags/{prev}",
                        check=False).returncode == 0:
            notes = git_out(a, "log", f"{prev}..HEAD", "--pretty=- %s") or tag
        else:
            notes = tag
    print(f"[{a.short}] gh release create {tag} …")
    run(["gh", "release", "create", tag, "--title", tag, "--notes", notes,
         "--repo", a.repo], capture=False)

    # 7. Deploy into the game install + confirm.
    print(f"[{a.short}] ghaddons update {a.repo} …")
    ghaddons("update", a.repo, capture=False)
    listing = ghaddons("list", check=False).stdout
    ok = any(a.repo.split("/")[-1].lower() in ln.lower() and "ok" in ln.lower()
             for ln in listing.splitlines())
    status = "ghaddons reports ok" if ok else "⚠ verify with `ghaddons list`"

    print(f"\n[{a.short}] released {tag} + deployed — {status}.")
    print(f"[{a.short}] In-game: /reload, then {a.reload_hint}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="wowkb.addon", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="presence + local HEAD + .toc version + latest release + drift")

    pp = sub.add_parser("pull", help="clone-if-missing + git pull each sub-repo (machine-B sync)")
    pp.add_argument("names", nargs="*", help="short names (default: all)")
    pp.add_argument("--all", action="store_true", help="pull every registered addon")

    rp = sub.add_parser("release", help="bump→lint→commit→push→gh release→ghaddons deploy")
    rp.add_argument("name", help="short name (bb|cdmp|ps) or a checkout path")
    g = rp.add_mutually_exclusive_group()
    g.add_argument("--major", action="store_true", help="X+1.0.0")
    g.add_argument("--minor", action="store_true", help="x.Y+1.0")
    g.add_argument("--patch", action="store_true", help="x.y.Z+1 (default)")
    rp.add_argument("--notes", help="release notes (default: commit log since last release)")
    rp.add_argument("--skip-lint", action="store_true", help="skip the luaparser syntax check")
    rp.add_argument("--dry-run", action="store_true",
                    help="do everything up to (not including) commit; revert the .toc bump")

    cp = sub.add_parser("check", help="report addons with local-only (uncommitted/unpushed) work; exit 1 if any")
    cp.add_argument("--no-fetch", action="store_true", help="don't fetch first (faster, less accurate)")

    dp = sub.add_parser("deploy", help="redeploy the latest release via ghaddons (no new cut)")
    dp.add_argument("name", help="short name or checkout path")

    args = p.parse_args(argv)
    return {
        "list": cmd_list, "pull": cmd_pull, "release": cmd_release,
        "check": cmd_check, "deploy": cmd_deploy,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())

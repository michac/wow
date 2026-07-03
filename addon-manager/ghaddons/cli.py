"""Command-line front end.

    python -m ghaddons.cli list
    python -m ghaddons.cli add  Nevcairiel/Bartender4
    python -m ghaddons.cli install --all
    python -m ghaddons.cli update Nevcairiel/Bartender4
    python -m ghaddons.cli remove Nevcairiel/Bartender4
    python -m ghaddons.cli path "/mnt/c/.../Interface/AddOns"
"""

from __future__ import annotations

import argparse
import sys

from . import manager as m
from .paths import CONFIG_PATH, MANIFEST_PATH

STATE_MARK = {
    "up-to-date": "  ok",
    "update-available": " UPD",
    "not-installed": "  --",
    "error": " ERR",
}


def _load():
    return m.Config.load(CONFIG_PATH), m.load_manifest(MANIFEST_PATH)


def cmd_list(args) -> int:
    cfg, manifest = _load()
    if not cfg.repos:
        print("No repos configured. Add one:  python -m ghaddons.cli add owner/repo")
        return 0
    print(f"AddOns dir: {cfg.addons_dir}\n")
    print(f"{'':4}  {'repo':<40} {'installed':<20} {'latest':<20}")
    for repo in cfg.repos:
        s = m.status_for(repo, cfg, manifest)
        mark = STATE_MARK.get(s.state, "    ")
        latest = s.latest if s.state != "error" else s.error[:40]
        print(f"{mark}  {repo:<40} {s.installed or '-':<20} {latest:<20}")
    return 0


def cmd_add(args) -> int:
    cfg, _ = _load()
    repo = args.repo.strip().strip("/")
    if repo in cfg.repos:
        print(f"already configured: {repo}")
        return 0
    cfg.repos.append(repo)
    cfg.save(CONFIG_PATH)
    print(f"added: {repo}")
    return 0


def cmd_rm(args) -> int:
    cfg, _ = _load()
    repo = args.repo.strip().strip("/")
    if repo in cfg.repos:
        cfg.repos.remove(repo)
        cfg.save(CONFIG_PATH)
        print(f"removed from config: {repo}  (files left in place; use `remove` to delete them)")
    else:
        print(f"not in config: {repo}")
    return 0


def _targets(args, cfg) -> list[str]:
    return list(cfg.repos) if args.all else [args.repo.strip().strip("/")]


def cmd_install(args) -> int:
    cfg, manifest = _load()
    rc = 0
    for repo in _targets(args, cfg):
        try:
            entry = m.install(repo, cfg, manifest)
            m.save_manifest(MANIFEST_PATH, manifest)
            print(f"installed {repo} @ {entry['version']}  → {', '.join(entry['folders'])}")
        except Exception as e:  # noqa: BLE001
            print(f"FAILED {repo}: {e}", file=sys.stderr)
            rc = 1
    return rc


def cmd_update(args) -> int:
    cfg, manifest = _load()
    rc = 0
    for repo in _targets(args, cfg):
        try:
            s = m.status_for(repo, cfg, manifest)
            if s.state == "up-to-date":
                print(f"up-to-date {repo} @ {s.installed}")
                continue
            entry = m.install(repo, cfg, manifest)
            m.save_manifest(MANIFEST_PATH, manifest)
            print(f"updated {repo} → {entry['version']}")
        except Exception as e:  # noqa: BLE001
            print(f"FAILED {repo}: {e}", file=sys.stderr)
            rc = 1
    return rc


def cmd_remove(args) -> int:
    cfg, manifest = _load()
    removed = m.remove(args.repo.strip().strip("/"), cfg, manifest)
    m.save_manifest(MANIFEST_PATH, manifest)
    print(f"removed folders: {', '.join(removed) or '(none tracked)'}")
    return 0


def cmd_path(args) -> int:
    cfg, _ = _load()
    if args.dir:
        cfg.addons_dir = args.dir
        cfg.save(CONFIG_PATH)
    print(cfg.addons_dir)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ghaddons", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="show configured addons + update status").set_defaults(fn=cmd_list)

    a = sub.add_parser("add", help="add owner/repo to the config")
    a.add_argument("repo"); a.set_defaults(fn=cmd_add)

    r = sub.add_parser("rm", help="drop owner/repo from the config (keeps files)")
    r.add_argument("repo"); r.set_defaults(fn=cmd_rm)

    for name, fn, helptext in [
        ("install", cmd_install, "download + install"),
        ("update", cmd_update, "install only if a newer version exists"),
    ]:
        s = sub.add_parser(name, help=helptext)
        s.add_argument("repo", nargs="?")
        s.add_argument("--all", action="store_true", help="apply to every configured repo")
        s.set_defaults(fn=fn)

    rm = sub.add_parser("remove", help="delete an addon's installed folders")
    rm.add_argument("repo"); rm.set_defaults(fn=cmd_remove)

    pa = sub.add_parser("path", help="show or set the AddOns directory")
    pa.add_argument("dir", nargs="?"); pa.set_defaults(fn=cmd_path)

    args = p.parse_args(argv)
    if getattr(args, "all", False) is False and args.cmd in ("install", "update") and not args.repo:
        p.error(f"{args.cmd}: pass a repo or --all")
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

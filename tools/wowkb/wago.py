"""Download DB2 tables as CSV from wago.tools into raw/wago/.

Usage:
    uv run python -m wowkb.wago JournalEncounter
    uv run python -m wowkb.wago Faction --build 12.0.5.64722
"""

import argparse
from pathlib import Path

import requests

from ._common import save_raw

_UA = {"User-Agent": "wowkb/0.1 (personal knowledge base)"}


def latest_build(product: str = "wow") -> str:
    """Newest build string for a product (e.g. '12.0.7.68256') from wago.tools."""
    resp = requests.get("https://wago.tools/api/builds", headers=_UA, timeout=30)
    resp.raise_for_status()
    builds = resp.json()[product]
    return builds[0]["version"]


def download(table: str, build: str | None, raw: str | None = None) -> None:
    params = {"build": build} if build else {}
    resp = requests.get(
        f"https://wago.tools/db2/{table}/csv",
        params=params,
        headers=_UA,
        timeout=120,
    )
    resp.raise_for_status()
    suffix = f"-{build}" if build else ""
    name = f"{table}{suffix}.csv"
    if raw:
        # Write beside an existing pinned set rather than splitting the cache in
        # two — the readers resolve ONE raw/, so a table fetched into a different
        # directory than its siblings is invisible to them. See _common.save_raw.
        out = Path(raw).expanduser().resolve() / "wago" / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(resp.text, encoding="utf-8")
    else:
        out = save_raw("wago", name, resp.text)
    print(out)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.wago", description=__doc__)
    p.add_argument("table", help="DB2 table name, e.g. JournalEncounter")
    p.add_argument("--build", default=None, help="exact build, e.g. 12.0.5.64722 (default: latest)")
    p.add_argument("--raw", metavar="PATH", default=None,
                   help="DB2 cache to write into (default: <repo>/raw). Use the same "
                        "value the readers use, or the fetch lands where nothing looks.")
    args = p.parse_args()
    download(args.table, args.build, args.raw)


if __name__ == "__main__":
    main()

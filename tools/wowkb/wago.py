"""Download DB2 tables as CSV from wago.tools into raw/wago/.

Usage:
    uv run python -m wowkb.wago JournalEncounter
    uv run python -m wowkb.wago Faction --build 12.0.5.64722
"""

import argparse

import requests

from ._common import save_raw

_UA = {"User-Agent": "wowkb/0.1 (personal knowledge base)"}


def latest_build(product: str = "wow") -> str:
    """Newest build string for a product (e.g. '12.0.7.68256') from wago.tools."""
    resp = requests.get("https://wago.tools/api/builds", headers=_UA, timeout=30)
    resp.raise_for_status()
    builds = resp.json()[product]
    return builds[0]["version"]


def download(table: str, build: str | None) -> None:
    params = {"build": build} if build else {}
    resp = requests.get(
        f"https://wago.tools/db2/{table}/csv",
        params=params,
        headers=_UA,
        timeout=120,
    )
    resp.raise_for_status()
    suffix = f"-{build}" if build else ""
    out = save_raw("wago", f"{table}{suffix}.csv", resp.text)
    print(out)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.wago", description=__doc__)
    p.add_argument("table", help="DB2 table name, e.g. JournalEncounter")
    p.add_argument("--build", default=None, help="exact build, e.g. 12.0.5.64722 (default: latest)")
    args = p.parse_args()
    download(args.table, args.build)


if __name__ == "__main__":
    main()

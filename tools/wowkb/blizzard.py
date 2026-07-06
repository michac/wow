"""Blizzard Game Data API client (client-credentials OAuth).

Usage:
    uv run python -m wowkb.blizzard token-price
    uv run python -m wowkb.blizzard item 19019
    uv run python -m wowkb.blizzard spell 980
    uv run python -m wowkb.blizzard media-spell 980
    uv run python -m wowkb.blizzard journal-instances
    uv run python -m wowkb.blizzard journal-encounter 2902
    uv run python -m wowkb.blizzard quest 92013
    uv run python -m wowkb.blizzard quest-area 15355
    uv run python -m wowkb.blizzard realms
    uv run python -m wowkb.blizzard get /data/wow/item/19019 --namespace static
"""

import argparse
import json
import os

import requests

from ._common import env, get_oauth_token


def _token() -> str:
    return get_oauth_token(
        "blizzard",
        "https://oauth.battle.net/token",
        env("BLIZZARD_CLIENT_ID"),
        env("BLIZZARD_CLIENT_SECRET"),
    )


def get(path: str, namespace: str = "static", **params) -> dict:
    """GET a Game Data API path. namespace is 'static'/'dynamic'/'profile' (region suffix added)."""
    region = os.getenv("REGION", "us")
    resp = requests.get(
        f"https://{region}.api.blizzard.com{path}",
        params={"namespace": f"{namespace}-{region}", "locale": "en_US", **params},
        headers={"Authorization": f"Bearer {_token()}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


COMMANDS = {
    "token-price": lambda a: get("/data/wow/token/index", "dynamic"),
    "item": lambda a: get(f"/data/wow/item/{a.id}", "static"),
    "spell": lambda a: get(f"/data/wow/spell/{a.id}", "static"),
    "media-spell": lambda a: get(f"/data/wow/media/spell/{a.id}", "static"),
    "journal-instances": lambda a: get("/data/wow/journal-instance/index", "static"),
    "journal-encounter": lambda a: get(f"/data/wow/journal-encounter/{a.id}", "static"),
    "quest": lambda a: get(f"/data/wow/quest/{a.id}", "static"),
    "quest-area": lambda a: get(f"/data/wow/quest/area/{a.id}", "static"),
    "realms": lambda a: get("/data/wow/realm/index", "dynamic"),
    "get": lambda a: get(a.path, a.namespace),
}


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.blizzard", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("token-price", help="current WoW Token gold price")
    for name in ("item", "spell", "media-spell", "journal-encounter", "quest", "quest-area"):
        sp = sub.add_parser(name)
        sp.add_argument("id", type=int)
    sub.add_parser("journal-instances", help="index of raids/dungeons")
    sub.add_parser("realms", help="realm index")
    g = sub.add_parser("get", help="raw GET escape hatch")
    g.add_argument("path")
    g.add_argument("--namespace", default="static", choices=["static", "dynamic", "profile"])
    args = p.parse_args()
    print(json.dumps(COMMANDS[args.cmd](args), indent=2))


if __name__ == "__main__":
    main()

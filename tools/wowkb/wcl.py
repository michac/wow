"""Warcraft Logs API v2 (GraphQL) client.

Usage:
    uv run python -m wowkb.wcl rankings <encounter-id> --class Warlock --spec Affliction
    uv run python -m wowkb.wcl casts <report-code> --fight 3
    uv run python -m wowkb.wcl query '<raw graphql>'
"""

import argparse
import json

import requests

from ._common import env, get_oauth_token

API = "https://www.warcraftlogs.com/api/v2/client"


def gql(query: str, variables: dict | None = None) -> dict:
    token = get_oauth_token(
        "wcl",
        "https://www.warcraftlogs.com/oauth/token",
        env("WCL_CLIENT_ID"),
        env("WCL_CLIENT_SECRET"),
    )
    resp = requests.post(
        API,
        json={"query": query, "variables": variables or {}},
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        raise SystemExit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]


RANKINGS = """
query ($id: Int!, $klass: String, $spec: String) {
  worldData {
    encounter(id: $id) {
      name
      characterRankings(className: $klass, specName: $spec, metric: dps)
    }
  }
}
"""

CASTS = """
query ($code: String!, $fights: [Int]) {
  reportData {
    report(code: $code) {
      title
      table(fightIDs: $fights, dataType: Casts)
    }
  }
}
"""


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.wcl", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("rankings", help="top character rankings for an encounter")
    r.add_argument("encounter_id", type=int)
    r.add_argument("--class", dest="klass", default=None)
    r.add_argument("--spec", default=None)

    c = sub.add_parser("casts", help="casts table for a report fight")
    c.add_argument("code")
    c.add_argument("--fight", type=int, action="append", default=None)

    q = sub.add_parser("query", help="raw GraphQL escape hatch")
    q.add_argument("graphql")

    args = p.parse_args()
    if args.cmd == "rankings":
        out = gql(RANKINGS, {"id": args.encounter_id, "klass": args.klass, "spec": args.spec})
    elif args.cmd == "casts":
        out = gql(CASTS, {"code": args.code, "fights": args.fight})
    else:
        out = gql(args.graphql)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

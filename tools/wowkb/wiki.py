"""Fetch warcraft.wiki.gg pages as RAW WIKITEXT via the MediaWiki API.

WHY NOT JUST WebFetch
---------------------
WebFetch renders the page through a summarising model.  For a KB whose whole
point is "cite everything, never paraphrase a spec", that is the wrong tool:
you get a plausible restatement with no revision id.  `api.php` gives you

  * the exact source text (signatures, argument tables, `{{patch}}` stamps),
  * a per-revision `timestamp` you can cite as "last edited <date>",
  * category listings and search, without scraping HTML.

That last point matters right now: since 2026-07-23T06:08Z the wiki carries an
"API wiki is under maintenance, ETA at least multiple days" banner.  The banner
is a site notice, not a data outage — `api.php` kept serving through it in
testing — but you should still stamp every wiki claim with the revision date
this tool prints, so a stale page is visible as stale.

TIER
----
warcraft.wiki.gg is **Tier 2**.  It is community-maintained, not Blizzard's.
Two specific failure modes to watch for and to write into any claim you take
from it:

  1. **Age.** Many API pages were last touched years ago (e.g. `API_CreateFrame`'s
     newest patch note is 2.0.1 from 2006).  A page that is not *wrong* may still
     be describing pre-Midnight behaviour.  Always print the timestamp.
  2. **Build skew.** The `World of Warcraft API` index page is currently stamped
     "PTR Patch 12.1.0 (68301)", i.e. ahead of live 12.0.7.  Content may describe
     an unreleased build.

Prefer `wowkb.uiapi` (Tier 1, Blizzard's own generated docs at the live build)
whenever it covers the thing.  Use the wiki for what Tier 1 does not carry:
prose/behaviour, the Lua security primitives (`issecurevariable`, `securecall`,
`forceinsecure`, `scrub`, `hooksecurefunc`), the `.toc` format, HOWTOs, and the
per-patch `Patch <ver>/API changes` diffs (which also archive Blizzard blue
posts with citations).

USAGE
-----
    uv run python -m wowkb.wiki page API_issecurevariable
    uv run python -m wowkb.wiki page "Secret values" --out raw/wiki/secret-values.wiki
    uv run python -m wowkb.wiki pages API_CreateFrame API_hooksecurefunc TOC_format
    uv run python -m wowkb.wiki search "secret value" --limit 20
    uv run python -m wowkb.wiki category "HOWTOs"
    uv run python -m wowkb.wiki category "Interface customization" --subcats
    uv run python -m wowkb.wiki changes 12.0.7        # Patch 12.0.7/API changes
    uv run python -m wowkb.wiki info API_UnitHealth   # just the revision stamp

Everything is cached under raw/wiki/ (gitignored). `--fresh` bypasses the cache.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "raw" / "wiki"
API = "https://warcraft.wiki.gg/api.php"
UA = "wowkb-addon-dev-research/1.0 (local KB tooling; contact: repo owner)"


def _get(params: dict, fresh: bool = False) -> dict:
    params = {**params, "format": "json", "formatversion": "2"}
    qs = urllib.parse.urlencode(params)
    key = CACHE / "_api" / (urllib.parse.quote(qs, safe="")[:180] + ".json")
    if not fresh and key.exists():
        return json.loads(key.read_text())
    req = urllib.request.Request(f"{API}?{qs}", headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                sys.exit(f"wiki api failed: {e}")
            time.sleep(2 * (attempt + 1))
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text(json.dumps(data))
    return data


def fetch_pages(titles: list[str], fresh: bool = False) -> list[dict]:
    """-> [{title, missing, timestamp, revid, content}] (batched 20 at a time)."""
    out = []
    for i in range(0, len(titles), 20):
        batch = titles[i : i + 20]
        d = _get(
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": "content|timestamp|ids",
                "rvslots": "main",
                "titles": "|".join(batch),
                "redirects": "1",
            },
            fresh,
        )
        q = d.get("query", {})
        redirects = {r["from"]: r["to"] for r in q.get("redirects", [])}
        for p in q.get("pages", []):
            if p.get("missing"):
                out.append({"title": p["title"], "missing": True})
                continue
            rev = (p.get("revisions") or [{}])[0]
            out.append(
                {
                    "title": p["title"],
                    "missing": False,
                    "timestamp": rev.get("timestamp"),
                    "revid": rev.get("revid"),
                    "content": rev.get("slots", {}).get("main", {}).get("content", ""),
                    "redirected_from": [k for k, v in redirects.items() if v == p["title"]],
                }
            )
    return out


def _url(title: str) -> str:
    return "https://warcraft.wiki.gg/wiki/" + urllib.parse.quote(title.replace(" ", "_"))


def _emit(p: dict, args) -> None:
    if p.get("missing"):
        print(f"### {p['title']} -- PAGE DOES NOT EXIST")
        print("    [gap] no such wiki page; do not infer one exists.")
        return
    hdr = (
        f"### {p['title']}\n"
        f"    url      : {_url(p['title'])}\n"
        f"    revid    : {p['revid']}\n"
        f"    lastedit : {p['timestamp']}   <-- cite this; the wiki is Tier 2\n"
    )
    if args.out:
        dest = Path(args.out)
        if len(args.title) > 1 if hasattr(args, "title") else False:
            dest = dest / (p["title"].replace("/", "_") + ".wiki")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(hdr + "\n" + p["content"])
        print(hdr + f"    written  : {dest}")
        return
    print(hdr)
    body = p["content"]
    if args.head:
        body = "\n".join(body.splitlines()[: args.head])
    print(body)
    print()


def cmd_page(args):
    for p in fetch_pages(args.title, args.fresh):
        _emit(p, args)


def cmd_info(args):
    for p in fetch_pages(args.title, args.fresh):
        if p.get("missing"):
            print(f"{p['title']}\tMISSING")
        else:
            n = len(p["content"].splitlines())
            print(f"{p['timestamp']}\trev {p['revid']}\t{n:5d} lines\t{p['title']}")


def cmd_search(args):
    d = _get(
        {
            "action": "query",
            "list": "search",
            "srsearch": args.query,
            "srlimit": args.limit,
            "srprop": "timestamp|snippet|wordcount",
        },
        args.fresh,
    )
    hits = d.get("query", {}).get("search", [])
    for h in hits:
        snip = (
            h.get("snippet", "")
            .replace('<span class="searchmatch">', "**")
            .replace("</span>", "**")
        )
        print(f"{h['timestamp'][:10]}  {h['wordcount']:6d}w  {h['title']}")
        print(f"    {snip}")
        print(f"    {_url(h['title'])}")
    print(f"-- {len(hits)} hit(s) of {d.get('query',{}).get('searchinfo',{}).get('totalhits')}")


def cmd_category(args):
    cont = None
    members = []
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{args.name}",
            "cmlimit": "500",
            "cmtype": "subcat|page" if args.subcats else "page",
        }
        if cont:
            params["cmcontinue"] = cont
        d = _get(params, args.fresh)
        members += d.get("query", {}).get("categorymembers", [])
        cont = d.get("continue", {}).get("cmcontinue")
        if not cont:
            break
    for m in members:
        print(f"{m['title']}\t{_url(m['title'])}")
    print(f"-- {len(members)} member(s) of Category:{args.name}")


def cmd_changes(args):
    titles = [f"Patch {v}/API changes" for v in args.versions]
    for p in fetch_pages(titles, args.fresh):
        _emit(p, args)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="wowkb.wiki",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--fresh", action="store_true", help="bypass the raw/wiki cache")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("page", help="dump raw wikitext")
    p.add_argument("title", nargs="+")
    p.add_argument("--out", help="write to this file/dir instead of stdout")
    p.add_argument("--head", type=int, help="only the first N lines")
    p.set_defaults(fn=cmd_page)

    p = sub.add_parser("pages", help="alias for page")
    p.add_argument("title", nargs="+")
    p.add_argument("--out")
    p.add_argument("--head", type=int)
    p.set_defaults(fn=cmd_page)

    p = sub.add_parser("info", help="revision stamp only (staleness triage)")
    p.add_argument("title", nargs="+")
    p.set_defaults(fn=cmd_info)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=25)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("category")
    p.add_argument("name")
    p.add_argument("--subcats", action="store_true")
    p.set_defaults(fn=cmd_category)

    p = sub.add_parser("changes", help="Patch <ver>/API changes pages")
    p.add_argument("versions", nargs="+")
    p.add_argument("--out")
    p.add_argument("--head", type=int)
    p.set_defaults(fn=cmd_changes)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()

"""One-quest digest: Blizzard API basics + Wowhead page gap-fill, in one grep-able
block. Replaces driving Playwright for everything except user comments.

    uv run python -m wowkb.quest 92013
    uv run python -m wowkb.quest "WANTED: Dionaea's Thorntusks"   # name -> id
    uv run python -m wowkb.quest 92013 --json

Blizzard is authoritative for title/type/area/level/xp/money; Wowhead fills the
gaps the Game Data API omits — currency/rep/item reward *names*, the daily/weekly
cadence, and the reqlevel cross-check (see knowledge/_meta/quests.md). Reward names
are run through rewards.value_quest() for a baseline value (R + goal tags).

NOT included (known holdout): user **comments** and prerequisite/campaign gating,
which load via an unidentified Wowhead XHR. For hidden gates (e.g. the Shul'ka
WANTED board's campaign lock) check the quest in-game — see
knowledge/systems/leveling-notes.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse

import requests

from . import blizzard, rewards

_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"}
_SEARCH = "https://www.wowhead.com/search/suggestions-template"
QUEST_TYPE = 5  # Wowhead search "type" for a Quest


# --------------------------------------------------------------------------- #
# ID resolution                                                                #
# --------------------------------------------------------------------------- #
def resolve_id(arg: str) -> tuple[int, list[dict]]:
    """(quest_id, candidates). Digits -> direct. Else Wowhead name search (type==5)."""
    if arg.isdigit():
        return int(arg), []
    resp = requests.get(_SEARCH, params={"q": arg}, headers=_UA, timeout=30)
    resp.raise_for_status()
    results = [r for r in resp.json().get("results", []) if r.get("type") == QUEST_TYPE]
    if not results:
        sys.exit(f"error: no quest matches {arg!r} on Wowhead search")
    return int(results[0]["id"]), results


# --------------------------------------------------------------------------- #
# Blizzard block                                                               #
# --------------------------------------------------------------------------- #
def blizzard_block(qid: int) -> dict:
    try:
        q = blizzard.get(f"/data/wow/quest/{qid}", "static")
    except Exception as e:  # noqa: BLE001 — 404 / network: degrade, don't crash
        return {"_error": str(e)}
    req = q.get("requirements", {})
    rw = q.get("rewards", {})
    return {
        "id": q.get("id"),
        "title": q.get("title"),
        "type": (q.get("type") or {}).get("name"),
        "area": (q.get("area") or {}).get("name"),
        "area_id": (q.get("area") or {}).get("id"),
        "min_level": req.get("min_character_level"),
        "max_level": req.get("max_character_level"),
        "xp": rw.get("experience"),
        "money": (rw.get("money") or {}).get("value"),
        "description": q.get("description"),
    }


# --------------------------------------------------------------------------- #
# Wowhead block                                                                #
# --------------------------------------------------------------------------- #
def _infobox(html: str) -> dict:
    """Pull Type / Requires level / Side from the quest quickfacts infobox."""
    m = re.search(r'[Mm]arkup\.printHtml\("((?:[^"\\]|\\.)*)"', html)
    out: dict = {}
    if not m:
        return out
    txt = m.group(1).replace("\\/", "/").replace('\\"', '"')
    t = re.search(r"Type:\s*([A-Za-z ]+?)\s*(?:\[|$)", txt)
    if t:
        out["type"] = t.group(1).strip()
    r = re.search(r"Requires level\s*(\d+)", txt)
    if r:
        out["requires_level"] = int(r.group(1))
    s = re.search(r"Side:\s*([A-Za-z ]+?)\s*(?:\[|$)", txt)
    if s:
        out["side"] = s.group(1).strip()
    return out


def wowhead_block(qid: int) -> dict:
    """reqlevel + cadence + reward currency/item names from the inline HTML.

    allow_redirects is essential: bare /quest=<id> 301s to the slug; without it the
    body is 0 bytes (knowledge/_meta/quests.md).
    """
    try:
        resp = requests.get(f"https://www.wowhead.com/quest={qid}",
                            headers=_UA, allow_redirects=True, timeout=30)
        resp.raise_for_status()
    except Exception as e:  # noqa: BLE001
        return {"_error": str(e)}
    html = resp.text
    out: dict = {"url": resp.url}
    out.update(_infobox(html))
    reqs = [int(x) for x in re.findall(r'"reqlevel":(\d+)', html)]
    if reqs:
        out["reqlevel"] = max(reqs)  # the quest's own reqlevel (page also carries 1s)
    # Reward links. Currency links on a quest page are the reward currencies in
    # practice; item links can include quest-provided items, so label them loosely.
    out["currencies"] = list(dict.fromkeys(
        re.findall(r'/currency=\d+/[^"]*">([^<]+)</a>', html)))
    out["items"] = list(dict.fromkeys(
        re.findall(r'/item=\d+/[^"]*">([^<]+)</a>', html)))
    return out


# --------------------------------------------------------------------------- #
# Assembly                                                                      #
# --------------------------------------------------------------------------- #
def digest(arg: str) -> dict:
    qid, candidates = resolve_id(arg)
    bz = blizzard_block(qid)
    wh = wowhead_block(qid)
    desc = rewards.descriptor_from_names(
        wh.get("currencies", []) if "_error" not in wh else [],
        wh.get("items", []) if "_error" not in wh else [],
        xp=bz.get("xp") or 0, money=bz.get("money") or 0)
    value = rewards.value_quest(desc)
    return {"resolved_id": qid, "candidates": candidates,
            "blizzard": bz, "wowhead": wh, "value": value}


def render(d: dict) -> str:
    bz, wh, val = d["blizzard"], d["wowhead"], d["value"]
    qid = d["resolved_id"]
    L: list[str] = []
    if len(d["candidates"]) > 1:
        L.append(f"note: {len(d['candidates'])} name matches; using the top one. Others:")
        for c in d["candidates"][1:6]:
            L.append(f"      {c['id']}  {c['name']}")
    title = bz.get("title") or (wh.get("url") or f"quest {qid}")
    L.append(f"Quest {qid} — {title}")
    if "_error" in bz:
        L.append(f"  ⚠ Blizzard API unavailable: {bz['_error']}")
    else:
        L.append(f"  type: {bz['type']}   area: {bz['area']} ({bz['area_id']})   "
                 f"side: {wh.get('side', '?')}")
        L.append(f"  required level (min_character_level): {bz['min_level']}   "
                 f"max: {bz['max_level']}   "
                 f"wowhead reqlevel: {wh.get('reqlevel', '?')}   "
                 f"cadence/type: {wh.get('type', '?')}")
        money = bz.get("money") or 0
        L.append(f"  base rewards: {bz.get('xp') or 0} XP, {money // 10000}g")
    if "_error" in wh:
        L.append(f"  ⚠ Wowhead unavailable ({wh['_error']}) — currency/rep rewards + cadence missing")
    else:
        L.append(f"  currency/rep rewards: {', '.join(wh['currencies']) or '(none found)'}")
        if wh["items"]:
            L.append(f"  item rewards (may include quest-provided items): {', '.join(wh['items'])}")
    L.append(f"  value: R={val['R']}  goals={','.join(val['goals']) or '—'}  "
             f"({val['confidence']} confidence){'  · ' + val['note'] if val['note'] else ''}")
    if "_error" not in bz and bz.get("description"):
        desc = re.sub(r"\s+", " ", bz["description"]).strip()
        L.append(f"  description: {desc[:280]}{'…' if len(desc) > 280 else ''}")
    src = [f"blizzard /data/wow/quest/{qid}"]
    if "_error" not in wh:
        src.append(wh.get("url", f"https://www.wowhead.com/quest={qid}"))
    L.append(f"  sources: {' ; '.join(src)}")
    L.append("  (comments + campaign/prereq gating not included — verify in-game; see leveling-notes.md)")
    return "\n".join(L)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.quest", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("quest", help="quest id (digits) or name (Wowhead search)")
    p.add_argument("--json", action="store_true", help="emit the structured digest")
    args = p.parse_args(argv)
    d = digest(args.quest)
    print(json.dumps(d, indent=2) if args.json else render(d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

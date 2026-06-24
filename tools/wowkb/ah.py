"""Auction house price checks (region-wide commodities).

Usage:
    uv run python -m wowkb.ah price "Mote of Primal Energy" "Radiant Shard"
    uv run python -m wowkb.ah price --fresh "Sunfire Silk Bolt"   # force re-download
    uv run python -m wowkb.ah ids "Thalassian Missive"            # name -> item IDs only

Commodities (stackable mats) are region-wide, so no realm needed.
The commodities snapshot is cached in raw/ah/ for 30 minutes — Blizzard
only refreshes it hourly anyway.
"""

import argparse
import json
import time

from . import blizzard
from ._common import RAW

_CACHE = RAW / "ah" / "commodities.json"
_CACHE_TTL = 30 * 60  # seconds


def search_items(name: str) -> list[dict]:
    """Item search by (partial) name. Returns [{id, name, quality}]."""
    data = blizzard.get(
        "/data/wow/search/item", "static",
        # no orderby: keep relevance ordering, or exact matches fall off page 1
        **{"name.en_US": name, "_pageSize": 100},
    )
    out = []
    for hit in data.get("results", []):
        d = hit["data"]
        item_name = d["name"]
        if isinstance(item_name, dict):
            item_name = item_name.get("en_US", "?")
        # search is substring-ish; keep only real matches
        if name.lower() in item_name.lower():
            out.append({
                "id": d["id"],
                "name": item_name,
                "quality": d.get("quality", {}).get("type", "?"),
            })
    return out


def load_commodities(fresh: bool = False) -> list[dict]:
    """Region commodities auctions, disk-cached for _CACHE_TTL."""
    if not fresh and _CACHE.exists() and time.time() - _CACHE.stat().st_mtime < _CACHE_TTL:
        return json.loads(_CACHE.read_text())["auctions"]
    data = blizzard.get("/data/wow/auctions/commodities", "dynamic")
    _CACHE.parent.mkdir(parents=True, exist_ok=True)
    _CACHE.write_text(json.dumps(data))
    return data["auctions"]


def price_summary(auctions: list[dict], item_ids: set[int]) -> dict[int, dict]:
    """Per item id: min unit buyout, total quantity, and price to buy cheapest N."""
    by_item: dict[int, list[tuple[int, int]]] = {}
    for a in auctions:
        iid = a["item"]["id"]
        if iid in item_ids:
            by_item.setdefault(iid, []).append((a["unit_price"], a["quantity"]))
    out = {}
    for iid, lots in by_item.items():
        lots.sort()
        out[iid] = {
            "min_unit": lots[0][0],
            "qty_total": sum(q for _, q in lots),
            "lots": lots,
        }
    return out


def gold(copper: int) -> str:
    g, rem = divmod(copper, 10000)
    s = rem // 100
    return f"{g:,}g {s:02d}s" if g else f"{s}s {rem % 100:02d}c"


def cost_for(lots: list[tuple[int, int]], n: int) -> int:
    """Copper cost to buy the cheapest n units."""
    total, need = 0, n
    for unit, qty in lots:
        take = min(need, qty)
        total += take * unit
        need -= take
        if need == 0:
            break
    return total


def cmd_ids(args) -> None:
    for it in search_items(args.name):
        print(f"{it['id']:>8}  {it['quality']:<9} {it['name']}")


def cmd_price(args) -> None:
    name_to_items = {n: search_items(n) for n in args.names}
    all_ids = {it["id"]: it for items in name_to_items.values() for it in items}
    if not all_ids:
        print("no items matched")
        return
    summary = price_summary(load_commodities(args.fresh), set(all_ids))
    age_min = (time.time() - _CACHE.stat().st_mtime) / 60
    print(f"(commodities snapshot ~{age_min:.0f} min old; region-wide)\n")
    for name, items in name_to_items.items():
        print(f"== {name}")
        for it in items:
            s = summary.get(it["id"])
            if not s:
                print(f"  {it['name']:<46} — no listings")
                continue
            n = args.need
            line = (f"  {it['name']:<46} min {gold(s['min_unit']):>12}/ea"
                    f"  ({s['qty_total']:,} listed)")
            if n:
                line += f"  | cheapest {n}: {gold(cost_for(s['lots'], n))}"
            print(line)
        print()


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.ah", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("ids", help="search item IDs by name")
    sp.add_argument("name")
    sp = sub.add_parser("price", help="min buyout for commodities by item name")
    sp.add_argument("names", nargs="+")
    sp.add_argument("--need", type=int, default=0, help="also price buying N units")
    sp.add_argument("--fresh", action="store_true", help="ignore snapshot cache")
    args = p.parse_args()
    {"ids": cmd_ids, "price": cmd_price}[args.cmd](args)


if __name__ == "__main__":
    main()

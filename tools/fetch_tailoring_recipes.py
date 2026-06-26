"""One-off: fetch all Midnight Tailoring (tier 2918) recipe details → raw/blizzard/."""

import json
import pathlib

from wowkb.blizzard import get

RAW = pathlib.Path(__file__).resolve().parent.parent / "raw" / "blizzard"
tier = json.loads((RAW / "midnight-tailoring-2918.json").read_text())

out = {}
for cat in tier["categories"]:
    for r in cat["recipes"]:
        rid = r["id"]
        detail = get(f"/data/wow/recipe/{rid}")
        detail["_category"] = cat["name"]
        out[rid] = detail
        print(f"{rid}  {cat['name']:28s}  {r['name']}")

(RAW / "midnight-tailoring-recipes.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote {len(out)} recipes")

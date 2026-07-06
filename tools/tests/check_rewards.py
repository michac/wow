"""Offline verification for the reward valuation model (rewards.value_quest).

Stdlib-only, no uv / no network:  python3 tools/tests/check_rewards.py
Exits non-zero if any check fails. Proves the character-agnostic baseline AND the
(not-yet-wired) character-relative branch behave — the latter must return a
*different* R for a low-ilvl vs high-ilvl char_state on the same descriptor.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb import rewards as rw  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


# --- baseline: currency classification -> R + goals ---------------------------
wanted = rw.descriptor_from_names(
    ["Coffer Key Shards", "Voidlight Marl", "The Hara'ti"], xp=16050, money=670000)
v = rw.value_quest(wanted)
check(v["R"] == 3, f"WANTED baseline R=3 (got {v['R']})")
check({"gearing", "vault", "renown"} <= set(v["goals"]),
      f"WANTED goals include gearing/vault/renown ({v['goals']})")

hero = rw.value_quest(rw.descriptor_from_names(["Hero Dawncrest"]))
check(hero["R"] == 3, f"Hero Dawncrest R=3 (got {hero['R']})")
myth = rw.value_quest(rw.descriptor_from_names(["Myth Dawncrest"]))
check(myth["R"] == 4, f"Myth Dawncrest R=4 (got {myth['R']})")

# --- cosmetic-only is R=0 on purpose (scoring-model.md) -----------------------
cos = rw.value_quest(rw.descriptor_from_names(["Field Accolade"]))
check(cos["R"] == 0 and cos["goals"] == ["cosmetic"], f"cosmetic-only -> R=0 ({cos})")
xponly = rw.value_quest(rw.descriptor_from_names([], xp=99999))
check(xponly["R"] == 0 and xponly["goals"] == ["xp"], f"xp-only -> R=0 ({xponly})")

# --- unknown currency degrades confidence but still tags a goal ---------------
unk = rw.value_quest(rw.descriptor_from_names(["Fabricated Whatsit"]))
check(unk["confidence"] == "low", f"unknown currency -> low confidence ({unk['confidence']})")

# --- container/cache rewards: value derived from the item description ----------
# Riftstalker's Cache (item 275690) description literally lists its contents.
rift_desc = ("Cache containing Field Accolades, Relic Coffer Key shards, "
             "materials for upgrading gear, gold, and more.")
cgoals, cR = rw.classify_cache(rift_desc, "Riftstalker's Cache")
check(cR > 0, f"classify_cache: description yields R>0 (got {cR})")
check({"vault", "cosmetic"} <= set(cgoals),
      f"classify_cache: goals include vault+cosmetic ({cgoals})")
# a cache attached to a descriptor folds its goals + floored R into value_quest
cache_d = rw.empty_descriptor()
cache_d["caches"] = [{"id": 275690, "name": "Riftstalker's Cache",
                      "goals": cgoals, "R": cR}]
cache_v = rw.value_quest(cache_d)
check(cache_v["R"] > 0, f"cache descriptor -> R>0 (got {cache_v['R']})")
check({"vault", "cosmetic"} <= set(cache_v["goals"]),
      f"cache descriptor goals include vault+cosmetic ({cache_v['goals']})")
# a cache with no recognizable contents string falls back to KNOWN_CACHES by name
fb_goals, fb_R = rw.classify_cache("A mysterious container.", "Riftstalker's Cache")
check(fb_R > 0 and "vault" in fb_goals,
      f"classify_cache: name fallback (KNOWN_CACHES) -> R>0 + vault ({fb_goals}, R={fb_R})")

# --- char-relative branch: SAME descriptor, DIFFERENT R by char_state ---------
gear = {"currencies": [], "rep": [], "xp": 0, "money": 0,
        "items": [{"id": 1, "name": "Boots", "ilvl": 230, "track": "Veteran"}]}
base = rw.value_quest(gear)["R"]
fresh = rw.value_quest(gear, {"ilvl_by_slot": {"feet": 200, "chest": 205}, "track_caps": {}})["R"]
geared = rw.value_quest(gear, {"ilvl_by_slot": {"feet": 278, "chest": 280}, "track_caps": {}})["R"]
capped = rw.value_quest(gear, {"ilvl_by_slot": {"feet": 200}, "track_caps": {"Veteran": True}})["R"]
check(fresh > geared, f"fresh-90 R ({fresh}) > geared R ({geared}) on same gear")
check(fresh != base, f"char-relative R ({fresh}) differs from baseline ({base})")
check(geared == 0, f"gear below your slots -> R=0 (got {geared})")
check(capped == 0, f"capped track -> R=0 (got {capped})")

# --- descriptor_from_listview shape ------------------------------------------
entry = {"currencyrewards": [[3345, 20]], "itemrewards": [[999, 1]], "xp": 100, "money": 50000}
d = rw.descriptor_from_listview(entry, {3345: "Hero Dawncrest"})
check(d["currencies"][0]["name"] == "Hero Dawncrest" and d["currencies"][0]["amount"] == 20,
      "listview descriptor carries currency name+amount")
check(d["items"][0]["id"] == 999 and d["items"][0]["track"] is None,
      "listview descriptor leaves gear track unresolved (scraper fills it)")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)

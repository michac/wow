"""Offline verification for currency → pending-consumer valuation (needs-first Phase 1).

Stdlib-only, no uv / no network:  python3 tools/tests/check_currency.py
Exits non-zero if any check fails. Proves currency_yield_R scores a crest/accolade
source high for a weak-slot char, 0 for a Hero-capped one, and that Field Accolades
zero out once the weakest slot is already ≥ 259.
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


# Two char_states: Encomplete-like (weak slots 259) vs a fully-276 Hero-capped main.
WEAK = {"ilvl_by_slot": {"waist": 259, "trinket2": 259, "neck": 263, "head": 276,
                         "back": 285, "mainhand": 285}, "track_caps": {}}
CAPPED = {"ilvl_by_slot": {s: 276 for s in
                           ("waist", "trinket2", "neck", "head", "back", "mainhand")},
          "track_caps": {}}

# The ritual-sites yield descriptor (headline): Hero + Myth crests + accolades.
RITUAL = {"hero_crest": 10, "myth_crest": 5, "field_accolade": 100}

weak = rw.currency_yield_R(RITUAL, WEAK)
capped = rw.currency_yield_R(RITUAL, CAPPED)
check(weak is not None and weak[0] >= 4.0,
      f"ritual-sites currency_R stays high for a weak-slot char ({weak})")
check(capped == (0.0, capped[1]) and capped[0] == 0.0,
      f"ritual-sites currency_R → 0 for a fully-276 Myth-capped main ({capped})")
check(weak[0] > capped[0], f"same yield: weak ({weak[0]}) outranks capped ({capped[0]})")

# Myth crests are the binding constraint → they win the max for the weak char.
myth_only = rw.currency_yield_R({"myth_crest": 5}, WEAK)
check(myth_only[0] == rw.MYTH_CREST_R, f"Myth crests carry the high flat weight ({myth_only})")

# Hero crests: a consumer while any slot < 276, R scales with headroom.
hero_weak = rw.currency_yield_R({"hero_crest": 20}, WEAK)
hero_capped = rw.currency_yield_R({"hero_crest": 20}, CAPPED)
check(hero_weak[0] > 1.0, f"Hero crests score by weakest-slot headroom ({hero_weak})")
check(hero_capped[0] == 0.0, f"Hero crests → 0 once every slot ≥ 276 ({hero_capped})")

# Field Accolades: value a ~259 Hero box → 0 once the weakest slot is already ≥ 259.
acc_weak = rw.currency_yield_R({"field_accolade": 100},
                               {"ilvl_by_slot": {"waist": 240, "chest": 250}})
acc_at259 = rw.currency_yield_R({"field_accolade": 100}, WEAK)  # weakest is exactly 259
check(acc_weak[0] > 0.0, f"Field Accolades help a sub-259 char ({acc_weak})")
check(acc_at259[0] == 0.0, f"Field Accolades → 0 once weakest slot ≥ 259 ({acc_at259})")

# Sparks: R=0 this phase (no craft model yet).
spark = rw.currency_yield_R({"radiant_spark_dust": 17}, WEAK)
check(spark == (0.0, spark[1]), f"Sparks → 0 this phase ({spark})")

# No currency yield → None (caller keeps reward_base).
check(rw.currency_yield_R(None, WEAK) is None, "no yields → None")
check(rw.currency_yield_R({}, WEAK) is None, "empty yields → None")
# No character state → None (can't value against a char).
check(rw.currency_yield_R(RITUAL, None) is None, "no char_state → None")
check(rw.currency_yield_R(RITUAL, {"ilvl_by_slot": {}}) is None,
      "empty equipment → None (pre-schema-4 dump)")
# Unknown canonical key contributes nothing → None when it's the only yield.
check(rw.currency_yield_R({"mystery_token": 1}, WEAK) is None,
      "unmodeled currency key → None (no consumer)")

# track_of_ilvl bands (coarse, biased low at boundaries).
check(rw.track_of_ilvl(276) == "Hero", "276 reads as Hero-capped, not Myth")
check(rw.track_of_ilvl(259) == "Hero", "259 reads as Hero 1/6")
check(rw.track_of_ilvl(285) == "Myth", "285 reads as Myth")
check(rw.track_of_ilvl(None) is None, "no ilvl → None")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)

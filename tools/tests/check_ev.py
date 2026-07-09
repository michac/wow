"""Offline verification for the deterministic-vs-RNG EV factor (needs-first Phase 3).

Stdlib-only:  python3 tools/tests/check_ev.py   (exits non-zero on failure)

Proves best_slot_delta / slot_target_R fold in the two probability effects:
  (a) `chance` = drop probability → straight EV multiplier;
  (b) slot randomness → a `[all]` roll is valued at the EXPECTED upgrade over its
      fillable slots, NOT the best one, UNLESS `targeted: true` (you pick the slot).

Headline: for a char whose one gap is waist 246, a TARGETED Hero-259 buy (Maren)
out-ranks a GUARANTEED-but-random Voidcore roll — even a Myth-272 one — because the
random roll usually lands on an already-good slot. This is the "accolades→Maren beats
random voidcore" inversion the model owner asked for.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from wowkb import rewards as rw  # noqa: E402
from wowkb.plan import load_state, slot_target_R  # noqa: E402

FIX = pathlib.Path(__file__).parent / "fixtures"
CAND = ROOT / "knowledge" / "planning" / "candidates.json"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


def close(a, b, eps=1e-6):
    return abs(a - b) < eps


onegap = load_state(str(FIX / "equipment-onegap.lua"), None)          # gap: waist 246
enc = load_state(str(FIX / "equipment-encomplete.lua"), None)         # geared, weakest 259
onegap_ilvls = {s["slot"]: s["ilvl"] for s in onegap["equipment"]}

# --- (b) slot randomness: targeted picks the gap; random gets the mean ---------
# Only waist (246) is sub-259, so a Hero-259 landing upgrades exactly one slot (+13).
d_tgt = rw.best_slot_delta([{"ilvl": 259, "targeted": True, "slots": ["all"]}], onegap_ilvls)
d_rnd = rw.best_slot_delta([{"ilvl": 259, "slots": ["all"]}], onegap_ilvls)
check(d_tgt == (13.0, "waist", 246.0),
      f"targeted 259 [all] lands the waist gap at full +13 ({d_tgt})")
check(close(d_rnd[0], 13.0 / 16) and d_rnd[1] == "waist",
      f"random 259 [all] = expected upgrade 13/16 slots ≈ 0.81, not 13 ({d_rnd})")
check(d_rnd[0] < d_tgt[0],
      "random-slot roll is worth less than a chosen slot at the SAME landing ilvl")

# --- (a) chance is a straight EV multiplier -----------------------------------
d_half = rw.best_slot_delta(
    [{"ilvl": 259, "targeted": True, "chance": 0.5, "slots": ["all"]}], onegap_ilvls)
check(close(d_half[0], 6.5), f"chance:0.5 halves the effective delta (13 → 6.5) ({d_half})")

# --- deterministic single-slot unchanged (Phase-2a regression) ----------------
d_waist = rw.best_slot_delta([{"ilvl": 272, "slots": ["waist"]}], onegap_ilvls)
check(d_waist == (26.0, "waist", 246.0),
      f"single-slot 272 into waist keeps exact +26 (no chance/targeted) ({d_waist})")

# --- Voidcore: track-conditional, guaranteed, but RANDOM slot ------------------
# Myth-272 (from a +10 M+ roll) beats Hero-259 (delve/prey), yet a guaranteed random
# Myth roll still loses to a TARGETED Hero pick for filling the specific waist gap.
R_tgt259 = slot_target_R({"yields": {"slots": [
    {"track": "hero", "ilvl": 259, "targeted": True, "slots": ["all"]}]}}, onegap)[0]
R_rnd259 = slot_target_R({"yields": {"slots": [
    {"track": "hero", "ilvl": 259, "slots": ["all"]}]}}, onegap)[0]
R_rnd272 = slot_target_R({"yields": {"slots": [
    {"track": "myth", "ilvl": 272, "slots": ["all"]}]}}, onegap)[0]
check(close(R_tgt259, 1.0 + 13.0 / 6.0), f"targeted Hero-259 R ≈ 3.17 ({R_tgt259:.3f})")
check(R_rnd272 > R_rnd259, "a random Myth-272 roll beats a random Hero-259 roll (track matters)")
check(R_tgt259 > R_rnd272,
      f"targeted Hero pick ({R_tgt259:.2f}) still beats a guaranteed RANDOM Myth roll "
      f"({R_rnd272:.2f}) — the modeled RNG is slot-randomness, not drop-chance")

# --- sidegrade floor: targeting can't manufacture an upgrade that isn't there --
enc_tgt = slot_target_R({"yields": {"slots": [
    {"track": "hero", "ilvl": 259, "targeted": True, "slots": ["all"]}]}}, enc)
check(enc_tgt[0] == 0.0,
      f"targeted 259 into a geared main (all slots ≥259) is still R=0 ({enc_tgt})")

# --- end-to-end on the real catalog: Maren-targeted val-naigtal > random voidcores
cands = {c["id"]: c for c in json.loads(CAND.read_text())["candidates"]}
vn = slot_target_R(cands["val-naigtal"], onegap)
vc = slot_target_R(cands["voidcores"], onegap)
check(vn is not None and vc is not None and vn[0] > vc[0],
      f"val-naigtal (targeted Maren) out-ranks voidcores (random roll) on the slot term "
      f"for a one-gap char (val-naigtal {vn} vs voidcores {vc})")

print(f"\n{_total} checks, {len(_fails)} failures")
sys.exit(1 if _fails else 0)

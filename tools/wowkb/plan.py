"""Session planner — rank "what should I do this session?" (efficiency-first).

Implements knowledge/planning/scoring-model.md:  score = (R * U * E) / T, with
gating that subtracts what you've already done this reset. Reset-state that the
Blizzard profile API can't see comes from the PlannerState addon's SavedVariables
dump (michac/wow-planner-state); pass it with --state, or let the tool find it
under the WoW install.

    uv run python -m wowkb.plan --minutes 60
    uv run python -m wowkb.plan --minutes 90 --state /path/to/PlannerState.lua
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CANDIDATES = REPO / "knowledge" / "planning" / "candidates.json"
DEFAULT_WOW = "/mnt/c/Program Files (x86)/World of Warcraft/_retail_"

# Enjoyment multipliers (E), capped at 1.5 per the model. Mirror of the table in
# scoring-model.md — that doc is canonical; keep these in sync when you tune.
E_TABLE = {
    "delve": 1.4, "ritual": 1.2, "prey": 1.1, "mplus": 1.0,
    "housing": 1.0, "chore": 1.0, "crafting": 0.9, "raid": 0.7, "pvp": 0.4,
}
E_CAP = 1.5
BLOCK_MIN = 15  # minutes per time block


# --------------------------------------------------------------------------- #
# Minimal Lua SavedVariables parser (subset: nested tables, [k]=v, positional,  #
# strings, numbers, booleans, nil). Enough for PlannerState's dump.            #
# --------------------------------------------------------------------------- #
class _LuaParser:
    def __init__(self, s: str):
        self.s = s
        self.i = 0
        self.n = len(s)

    def _ws(self):
        while self.i < self.n:
            c = self.s[self.i]
            if c in " \t\r\n":
                self.i += 1
            elif self.s.startswith("--", self.i):
                # line comment (SavedVariables never uses block comments)
                nl = self.s.find("\n", self.i)
                self.i = self.n if nl < 0 else nl + 1
            else:
                break

    def parse_value(self):
        self._ws()
        c = self.s[self.i]
        if c == "{":
            return self._table()
        if c in "\"'":
            return self._string(c)
        if self.s.startswith("true", self.i):
            self.i += 4; return True
        if self.s.startswith("false", self.i):
            self.i += 5; return False
        if self.s.startswith("nil", self.i):
            self.i += 3; return None
        return self._number()

    def _string(self, quote):
        self.i += 1
        out = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == "\\":
                out.append(self.s[self.i + 1]); self.i += 2; continue
            if c == quote:
                self.i += 1; break
            out.append(c); self.i += 1
        return "".join(out)

    def _number(self):
        j = self.i
        while self.i < self.n and self.s[self.i] not in ",}=\r\n \t":
            self.i += 1
        tok = self.s[j:self.i].strip()
        try:
            return int(tok)
        except ValueError:
            try:
                return float(tok)
            except ValueError:
                return tok  # bare identifier fallback

    def _key(self):
        # [key] = ... ; returns the key (str/int) or None for positional entries
        self._ws()
        if self.s[self.i] != "[":
            return None
        self.i += 1
        self._ws()
        c = self.s[self.i]
        key = self._string(c) if c in "\"'" else self._number()
        self._ws()
        assert self.s[self.i] == "]"; self.i += 1
        self._ws()
        assert self.s[self.i] == "="; self.i += 1
        return key

    def _table(self):
        self.i += 1  # {
        d, arr = {}, []
        while True:
            self._ws()
            if self.s[self.i] == "}":
                self.i += 1; break
            save = self.i
            key = self._key()
            if key is None:
                self.i = save
                arr.append(self.parse_value())
            else:
                d[key] = self.parse_value()
            self._ws()
            if self.i < self.n and self.s[self.i] == ",":
                self.i += 1
        if arr and not d:
            return arr
        for idx, v in enumerate(arr, 1):
            d.setdefault(idx, v)
        return d


def parse_savedvar(text: str, var: str) -> dict | None:
    """Extract `var = { ... }` from a SavedVariables Lua file."""
    marker = f"{var} = "
    pos = text.find(marker)
    if pos < 0:
        marker = f"{var}="
        pos = text.find(marker)
        if pos < 0:
            return None
    p = _LuaParser(text)
    p.i = pos + len(marker)
    return p.parse_value()


def load_state(state_path: str | None, wow_path: str) -> dict | None:
    if state_path:
        paths = [state_path]
    else:
        paths = sorted(glob.glob(
            f"{wow_path}/WTF/Account/*/*/*/SavedVariables/PlannerState.lua"))
    for pth in paths:
        try:
            text = Path(pth).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        try:
            db = parse_savedvar(text, "PlannerStateDB")
        except Exception:  # noqa: BLE001 — a malformed dump shouldn't crash the plan
            db = None
        if isinstance(db, dict) and db:
            db["_path"] = pth
            return db
    return None


# --------------------------------------------------------------------------- #
# Gating — is a candidate already done this reset?                             #
# Returns "done" | "todo" | "unknown".                                        #
# --------------------------------------------------------------------------- #
def gate_status(cand: dict, state: dict | None) -> str:
    g = cand.get("gate", {})
    t = g.get("type")
    if t == "always":
        return "todo"                       # standing content is never "done"
    if t == "manual":
        return "unknown"                    # planner can't see it
    if state is None:
        return "unknown"                    # no dump → can't gate the rest

    if t == "vault_has_rewards":
        vault = state.get("vault") or {}
        return "done" if not vault.get("hasRewards", False) else "todo"
    if t == "mplus_weekly_lt":
        runs = state.get("mythicPlus") or []
        done = sum(1 for r in runs if isinstance(r, dict) and r.get("thisWeek"))
        return "todo" if done < g.get("n", 8) else "done"
    if t == "weekly_quest":
        quests = state.get("weeklyQuests") or []
        for q in quests:
            if isinstance(q, dict) and q.get("label") == g.get("quest") or \
               (isinstance(q, dict) and str(q.get("id")) == str(g.get("quest"))):
                return "done" if q.get("complete") else "todo"
        return "unknown"                    # quest ID not configured in the addon
    if t == "lockout":
        needle = (g.get("name_contains") or "").lower()
        for lk in state.get("lockouts") or []:
            if isinstance(lk, dict) and needle in (lk.get("name") or "").lower():
                return "done"
        return "todo"
    return "unknown"


# --------------------------------------------------------------------------- #
# Scoring                                                                      #
# --------------------------------------------------------------------------- #
def score(cand: dict, mood: str) -> tuple[float, str]:
    R = float(cand.get("reward_base", 0))
    U = float(cand.get("urgency", 1))
    floor = 2 if mood == "fun" else 1          # collectible R-floor
    cap = 3.0 if mood == "fun" else E_CAP
    if R == 0 and U >= 1.5:
        R = floor
    E = min(E_TABLE.get(cand.get("enjoyment_key", "chore"), 1.0), cap)
    T = float(cand.get("time_blocks", 1)) or 0.1
    s = (R * U * E) / T
    # dominant-term reason
    terms = {"power": R, "urgency": U, "enjoyment": E}
    lead = max(terms, key=terms.get)
    return s, lead


def plan(minutes: int, state: dict | None, mood: str) -> dict:
    data = json.loads(CANDIDATES.read_text())
    budget = minutes / BLOCK_MIN
    rows = []
    for c in data["candidates"]:
        st = gate_status(c, state)
        if st == "done":
            continue
        s, lead = score(c, mood)
        rows.append({"c": c, "score": s, "lead": lead, "state": st})
    rows.sort(key=lambda r: r["score"], reverse=True)

    picks, spent = [], 0.0
    for r in rows:
        t = float(r["c"].get("time_blocks", 1))
        if spent + t <= budget + 1e-9:
            picks.append(r); spent += t
    return {"picks": picks, "all": rows, "budget": budget, "spent": spent}


# --------------------------------------------------------------------------- #
def _fmt(r: dict) -> str:
    c = r["c"]
    mins = round(float(c.get("time_blocks", 1)) * BLOCK_MIN)
    flag = " (?)" if r["state"] == "unknown" else ""
    return (f"  {r['score']:6.1f}  [{mins:>3}m] {c['name']:<42} "
            f"— {c['why']}{flag}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.plan", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--minutes", type=int, default=60, help="session time budget")
    p.add_argument("--mood", choices=["efficiency", "fun"], default="efficiency")
    p.add_argument("--state", help="path to PlannerState.lua (else auto-find)")
    p.add_argument("--wow-path", default=DEFAULT_WOW)
    args = p.parse_args(argv)

    state = load_state(args.state, args.wow_path)
    result = plan(args.minutes, state, args.mood)

    src = "no PlannerState dump — gates marked (?)" if state is None \
        else f"state: {Path(state['_path']).name} (char {state.get('character','?')})"
    print(f"\nSession plan · {args.minutes} min · mood={args.mood} · {src}\n")
    print(f"DO THIS ({round(result['spent']*BLOCK_MIN)} of {args.minutes} min):")
    for r in result["picks"]:
        print(_fmt(r))
    rest = [r for r in result["all"] if r not in result["picks"]]
    if rest:
        print("\nbacklog (didn't fit / lower value):")
        for r in rest:
            print(_fmt(r))
    if state is None:
        print("\n(!) No addon dump found. Install michac/wow-planner-state, /ps + /reload,")
        print("    then re-run so delve/prey/vault gates resolve instead of showing (?).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

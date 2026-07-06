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
REPEATABLES = REPO / "knowledge" / "planning" / "repeatables.json"
DEFAULT_WOW = "/mnt/c/Program Files (x86)/World of Warcraft/_retail_"

# Repeatable questIDs the hand-curated candidates.json already covers (via slug
# gates) — skip them when --include-repeatables merges the scraper catalog, so
# prey/void don't show up twice. Mirrors HAND_WIRED in gen_addon_quests.py.
CURATED_QUEST_IDS = {94446, 94385, 94386}

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
        want = str(g.get("quest"))
        matches = [q for q in (state.get("weeklyQuests") or [])
                   if isinstance(q, dict)
                   and (q.get("label") == g.get("quest") or str(q.get("id")) == want)]
        if not matches:
            return "unknown"                # quest ID(s) not configured in the addon
        # A slug may map to several quests (e.g. a rotating weekly present under two
        # zone IDs); it's done if ANY of them is flagged complete.
        return "done" if any(q.get("complete") for q in matches) else "todo"
    if t == "lockout":
        needle = (g.get("name_contains") or "").lower()
        for lk in state.get("lockouts") or []:
            if isinstance(lk, dict) and needle in (lk.get("name") or "").lower():
                return "done"
        return "todo"
    if t == "world_boss_weekly":
        # World bosses aren't returned by GetSavedInstanceInfo (the old 'lockout'
        # gate never fired). PlannerState schema>=3 emits a worldBosses[] block from
        # GetSavedWorldBossInfo — which lists only bosses ALREADY KILLED this reset,
        # exactly the weekly lockout signal. Mirror event_active's missing-key rule.
        wb = state.get("worldBosses")
        if wb is None:
            return "unknown"                # dump predates worldBosses (schema < 3)
        return "done" if wb else "todo"
    if t == "event_active":
        # Fun radar: surface a candidate only while its calendar event is live.
        cal = state.get("calendar")
        if cal is None:
            return "unknown"                # dump predates the calendar block (schema < 2)
        needle = (g.get("match") or "").lower()
        live = any(isinstance(e, dict) and e.get("active")
                   and needle in (e.get("title") or "").lower()
                   for e in cal)
        return "todo" if live else "done"   # not live now → drop it from the plan
    return "unknown"


# --------------------------------------------------------------------------- #
# Scoring                                                                      #
# --------------------------------------------------------------------------- #
DEFAULT_VAULT_THRESHOLDS = [1, 4, 8]


def _slot_thresholds(state: dict, track: str) -> list[int] | None:
    """Sorted unlock thresholds for a vault column, straight from the dump."""
    vault = state.get("vault") or {}
    thr = sorted(int(s["threshold"]) for s in (vault.get("slots") or [])
                 if isinstance(s, dict) and s.get("type") == track
                 and s.get("threshold") is not None)
    return thr or None


def _vault_track(track: str, state: dict | None) -> tuple[int | None, list[int] | None]:
    """(progress, thresholds) for a breakpoint track, both from live dump state.

    'mplus' counts this-week M+ runs (the gate's signal) and borrows the dungeon
    column's thresholds (Midnight reports M+ under the dungeon vault type). Any
    other track reads vault.slots[type].progress + its own thresholds — so we no
    longer assume [1,4,8]; delve/world/raid columns each carry their real cutoffs
    (observed live: world 2/4/6, dungeon 2/4/8, raid 1/4/8).
    """
    if not state:
        return None, None
    if track == "mplus":
        runs = state.get("mythicPlus") or []
        prog = sum(1 for r in runs if isinstance(r, dict) and r.get("thisWeek"))
        return prog, _slot_thresholds(state, "dungeon")
    vault = state.get("vault") or {}
    slots = [s for s in (vault.get("slots") or [])
             if isinstance(s, dict) and s.get("type") == track]
    if not slots:
        return None, None
    prog = max(int(s.get("progress") or 0) for s in slots)
    return prog, _slot_thresholds(state, track)


def breakpoint_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Breakpoint-proximity override for R (scoring-model.md 'breakpoint proximity').

    Returns (R, why-note) when a candidate carries a vault breakpoint AND live
    progress is known: R=4 for the run that *crosses* the next threshold, R=0
    once the track is capped, else the flat reward_base (progress is mid-track,
    no breakpoint nearby). Returns None when there's no breakpoint or no state to
    read — the caller then keeps reward_base and scores exactly as before.
    """
    bp = cand.get("breakpoint")
    if not bp or bp.get("type") != "vault":
        return None
    n, dump_thr = _vault_track(bp.get("track"), state)
    if n is None:
        return None
    thr = dump_thr or sorted(bp.get("thresholds") or DEFAULT_VAULT_THRESHOLDS)
    if n >= thr[-1]:
        return 0.0, "vault track capped"
    if (n + 1) in thr:
        return 4.0, f"next run unlocks vault slot {thr.index(n + 1) + 1}"
    return float(cand.get("reward_base", 0)), ""


def weakest_slots(state: dict | None, k: int = 3) -> list[tuple[str, float]]:
    """The k lowest-ilvl equipped slots from the dump (planner v2b context).

    schema>=4 dumps per-slot ilvls; older dumps omit `equipment` → empty list.
    """
    eq = (state or {}).get("equipment") or []
    rows = [(s.get("slot"), s.get("ilvl")) for s in eq
            if isinstance(s, dict) and isinstance(s.get("ilvl"), (int, float))]
    rows.sort(key=lambda r: r[1])
    return rows[:k]


def score(cand: dict, mood: str, state: dict | None = None) -> tuple[float, str, str]:
    R = float(cand.get("reward_base", 0))
    U = float(cand.get("urgency", 1))
    floor = 2 if mood == "fun" else 1          # collectible R-floor
    cap = 3.0 if mood == "fun" else E_CAP
    if R == 0 and U >= 1.5:                    # rare cosmetic gets a foot in the door
        R = floor
    note = ""
    bp = breakpoint_R(cand, state)            # vault-slot proximity overrides R
    if bp is not None:
        R, note = bp
    E = min(E_TABLE.get(cand.get("enjoyment_key", "chore"), 1.0), cap)
    T = float(cand.get("time_blocks", 1)) or 0.1
    s = (R * U * E) / T
    # dominant-term reason
    terms = {"power": R, "urgency": U, "enjoyment": E}
    lead = max(terms, key=terms.get)
    return s, lead, note


def load_candidates(include_repeatables: bool) -> list[dict]:
    """Curated candidates.json, optionally merged with the scraper catalog.

    candidates.json is the hand-tuned default. --include-repeatables folds in
    repeatables.json (auto-generated by wowkb.repeatables) for fuller coverage —
    minus the questIDs candidates.json already curates (CURATED_QUEST_IDS), so
    prey/void don't double up. Repeatable T/E are scraper placeholders
    (time_blocks=1, enjoyment=chore) — flagged in the output, tune in the JSON.
    """
    cands = list(json.loads(CANDIDATES.read_text())["candidates"])
    if not include_repeatables or not REPEATABLES.exists():
        return cands
    for c in json.loads(REPEATABLES.read_text()).get("candidates", []):
        if c.get("questID") in CURATED_QUEST_IDS:
            continue
        c = dict(c)
        c["_repeatable"] = True
        cands.append(c)
    return cands


def plan(minutes: int, state: dict | None, mood: str,
         include_repeatables: bool = False) -> dict:
    candidates = load_candidates(include_repeatables)
    budget = minutes / BLOCK_MIN
    rows = []
    for c in candidates:
        st = gate_status(c, state)
        if st == "done":
            continue
        s, lead, note = score(c, mood, state)
        rows.append({"c": c, "score": s, "lead": lead, "state": st, "note": note})
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
    src = " ~" if c.get("_repeatable") else ""   # ~ = scraper catalog (placeholder T/E)
    note = f" · {r['note']}" if r.get("note") else ""
    return (f"  {r['score']:6.1f}{src:1}  [{mins:>3}m] {c['name']:<42} "
            f"— {c['why']}{note}{flag}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wowkb.plan", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--minutes", type=int, default=60, help="session time budget")
    p.add_argument("--mood", choices=["efficiency", "fun"], default="efficiency")
    p.add_argument("--state", help="path to PlannerState.lua (else auto-find)")
    p.add_argument("--wow-path", default=DEFAULT_WOW)
    p.add_argument("--include-repeatables", action="store_true",
                   help="also rank the scraper catalog (repeatables.json); "
                        "rows marked ~ have placeholder time/enjoyment")
    args = p.parse_args(argv)

    state = load_state(args.state, args.wow_path)
    result = plan(args.minutes, state, args.mood, args.include_repeatables)

    src = "no PlannerState dump — gates marked (?)" if state is None \
        else f"state: {Path(state['_path']).name} (char {state.get('character','?')})"
    print(f"\nSession plan · {args.minutes} min · mood={args.mood} · {src}\n")
    weak = weakest_slots(state)
    if weak:
        il = state.get("equippedIlvl")
        head = f"equipped ilvl {round(il)}" if isinstance(il, (int, float)) and il else "gear"
        slots = ", ".join(f"{s} {round(v)}" for s, v in weak)
        print(f"weakest slots ({head}): {slots}\n")
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

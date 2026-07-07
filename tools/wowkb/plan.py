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
import os
from pathlib import Path

from wowkb import rewards

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
    "delve": 1.4, "ritual": 1.2, "prey": 1.1, "world": 1.1, "mplus": 1.0,
    "housing": 1.0, "chore": 1.0, "crafting": 0.9, "raid": 0.7, "pvp": 0.4,
}
E_CAP = 1.5
BLOCK_MIN = 15  # minutes per time block
LEVEL_CAP = 90  # Midnight cap (knowledge/_meta/game-version.md) — campaign_incomplete proxy


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


def load_state(state_path: str | None, wow_path: str,
               character: str | None = None) -> dict | None:
    """Load a PlannerState dump. Auto-find picks the **newest** dump so it's
    "the char you just played," not whoever sorts first alphabetically. Pass
    `character` to restrict the glob to a single character's SavedVariables.
    """
    if state_path:
        paths = [state_path]
    else:
        who = glob.escape(character) if character else "*"
        pattern = f"{wow_path}/WTF/Account/*/*/{who}/SavedVariables/PlannerState.lua"
        # Newest dump first = the character you most recently /reload-ed.
        paths = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
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
    if t == "raid_weekly":
        # Weekly raid kill. GetSavedInstanceInfo lockouts (state.lockouts, each with
        # name/isRaid/defeated) list the raids you're saved to this reset. Match the
        # raid by name; "done" once it's a raid lockout with >=1 boss defeated. A
        # single-boss raid (Sporefall) is "done" on the first difficulty cleared —
        # higher-difficulty re-kills for vault/ilvl are valued separately by the raid
        # vault breakpoint, so gating on any kill doesn't lose that signal.
        needle = (g.get("name_contains") or g.get("raid") or "").lower()
        if not needle:
            return "unknown"                # gate carries no matchable raid name
        for lk in state.get("lockouts") or []:
            if (isinstance(lk, dict) and lk.get("isRaid")
                    and needle in (lk.get("name") or "").lower()
                    and (lk.get("defeated") or 0) >= 1):
                return "done"
        return "todo"
    if t == "campaign_incomplete":
        # The Midnight main-story campaign is one-time and unlocks the endgame loop
        # (WQs, renown, Adventure Mode). The dump carries no campaign-complete flag,
        # so use level as a proxy: a max-level char has cleared the leveling spine and
        # this row should hide; a sub-cap roster member still needs it. Level absent →
        # unknown. (A precise campaign flag is a future PlannerState field.)
        lvl = state.get("level")
        if not isinstance(lvl, (int, float)):
            return "unknown"
        return "done" if lvl >= LEVEL_CAP else "todo"
    if t == "world_boss_weekly":
        # World bosses aren't returned by GetSavedInstanceInfo (the old 'lockout'
        # gate never fired). PlannerState schema>=3 emits a worldBosses[] block from
        # GetSavedWorldBossInfo — which lists only bosses ALREADY KILLED this reset,
        # exactly the weekly lockout signal. Mirror event_active's missing-key rule.
        wb = state.get("worldBosses")
        if wb is None:
            return "unknown"                # dump predates worldBosses (schema < 3)
        return "done" if wb else "todo"
    if t == "vault_track":
        # Delves/world activities aren't quest-flagged — their weekly motive is
        # Great Vault progress. Done once the named column is capped (its top
        # threshold met); the dump carries per-column progress+thresholds.
        # NOTE: the 'world' column counts world activities broadly (delves + world
        # bosses + …), so this is a delve *proxy*, not a pure delve counter.
        prog, thr = _vault_track(g.get("track"), state)
        if prog is None or not thr:
            return "unknown"
        return "done" if prog >= thr[-1] else "todo"
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


def quest_progress_note(cand: dict, state: dict | None) -> str:
    """'1/3'-style partial progress for a weekly_quest candidate, else ''.

    Reads have/need off the matched dumped quest (schema>=5). Only shows while the
    quest is in-log and unfinished — a turned-in weekly is already gated 'done'.
    """
    g = cand.get("gate", {})
    if g.get("type") != "weekly_quest" or not state:
        return ""
    want = str(g.get("quest"))
    for q in state.get("weeklyQuests") or []:
        if not isinstance(q, dict):
            continue
        if q.get("label") == g.get("quest") or str(q.get("id")) == want:
            have, need = q.get("have"), q.get("need")
            if isinstance(have, (int, float)) and isinstance(need, (int, float)) and need:
                return f"{int(have)}/{int(need)}"
    return ""


def weakest_slots(state: dict | None, k: int = 3) -> list[tuple[str, float]]:
    """The k lowest-ilvl equipped slots from the dump (planner v2b context).

    schema>=4 dumps per-slot ilvls; older dumps omit `equipment` → empty list.
    """
    eq = (state or {}).get("equipment") or []
    rows = [(s.get("slot"), s.get("ilvl")) for s in eq
            if isinstance(s, dict) and isinstance(s.get("ilvl"), (int, float))]
    rows.sort(key=lambda r: r[1])
    return rows[:k]


def currency_context(state: dict | None) -> str:
    """A one-line crest/currency balance summary (needs-first Phase 1 context).

    Surfaces the gearing currencies from the dump and flags the *bottleneck* — the
    smaller of the Hero/Myth crest balances — so "Myth is the binding constraint"
    is visible next to the plan. schema≥4 dumps `currencies`; older dumps → ''.
    """
    curs = {c.get("name"): c.get("quantity") for c in (state or {}).get("currencies") or []
            if isinstance(c, dict) and c.get("name")}
    if not curs:
        return ""
    hero = curs.get("Hero Dawncrest")
    myth = curs.get("Myth Dawncrest")
    # bottleneck = the scarcer crest tier (Myth for Encomplete: 20 vs 176 Hero).
    bottleneck = None
    if isinstance(hero, (int, float)) and isinstance(myth, (int, float)):
        bottleneck = "Myth Dawncrest" if myth <= hero else "Hero Dawncrest"
    order = [("Hero Dawncrest", "Hero"), ("Myth Dawncrest", "Myth"),
             ("Field Accolade", "Field Accolade"), ("Nebulous Voidcore", "Voidcore"),
             ("Coffer Key Shards", "Coffer shards")]
    parts = []
    for name, label in order:
        v = curs.get(name)
        if isinstance(v, (int, float)):
            tag = " (bottleneck)" if name == bottleneck else ""
            parts.append(f"{label} {int(v):,}{tag}")
    return " · ".join(parts)


def _slot_ilvls(state: dict | None) -> list[float]:
    """Every equipped slot's ilvl from the dump (schema>=4), else []."""
    eq = (state or {}).get("equipment") or []
    return [float(s["ilvl"]) for s in eq
            if isinstance(s, dict) and isinstance(s.get("ilvl"), (int, float))]


def slot_target_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Ilvl-relative reward: is this activity's gear an upgrade to THIS char?

    Generalizes breakpoint_R for gear: an activity carries `reward_ilvl_max`, the
    top ilvl its gear can reach (world/delve/prey/voidcore ≈ Hero 276; raid per-
    difficulty; faction champion 246). Compared against the char's equipped slots
    (weakest = the target):
      - ceiling ≤ your weakest slot  → R≈0 (can't upgrade anything; sidegrade)
      - ceiling well above it        → R toward 4–5 (weakest-slot targeting)
    Returns None when the activity has no ceiling or the dump carries no per-slot
    ilvls (schema<4) — the caller then keeps reward_base, scoring as before.
    """
    ceiling = cand.get("reward_ilvl_max")
    if not isinstance(ceiling, (int, float)):
        return None
    slots = _slot_ilvls(state)
    if not slots:
        return None
    weakest = min(slots)
    delta = ceiling - weakest
    if delta <= 0:
        return 0.0, f"reward ≤ your weakest slot ({round(weakest)})"
    # ~+1 R per 6 ilvl of headroom over the weakest slot, foot-in-door at 1.
    R = min(5.0, 1.0 + delta / 6.0)
    return R, f"+{round(delta)} ilvl over weakest slot ({round(weakest)})"


def _char_state(state: dict | None) -> dict:
    """Shape the dump into rewards.py's char_state schema (needs-first Phase 1).

    schema≥4 dumps per-slot `equipment` (itemID/ilvl/slot) and `currencies`
    (name/quantity). We map both into {ilvl_by_slot, currencies, track_caps}. The
    dump carries no upgrade track/level, so track_caps stays empty and the crest
    consumers approximate headroom from ilvl vs the Hero ceiling (rewards.py).
    """
    eq = (state or {}).get("equipment") or []
    ilvl_by_slot = {s["slot"]: float(s["ilvl"]) for s in eq
                    if isinstance(s, dict) and s.get("slot")
                    and isinstance(s.get("ilvl"), (int, float))}
    curs = {c["name"]: c.get("quantity") for c in (state or {}).get("currencies") or []
            if isinstance(c, dict) and c.get("name")}
    return {"ilvl_by_slot": ilvl_by_slot, "currencies": curs, "track_caps": {}}


def currency_R(cand: dict, state: dict | None) -> tuple[float, str] | None:
    """Currency-yield override for R: value this activity's declared crest/accolade
    yields by whether THIS char still has a consumer for them (needs-first Phase 1).

    Returns None when the candidate declares no `yields.currencies` or the dump
    carries no equipment (caller keeps reward_base); else delegates to
    rewards.currency_yield_R — 0 when the currency has no pending consumer (a
    Hero-capped main), high when a crest still fills a sub-cap slot.
    """
    yields = (cand.get("yields") or {}).get("currencies")
    if not yields:
        return None
    return rewards.currency_yield_R(yields, _char_state(state))


def score(cand: dict, mood: str, state: dict | None = None) -> tuple[float, str, str]:
    R = float(cand.get("reward_base", 0))
    U = float(cand.get("urgency", 1))
    floor = 2 if mood == "fun" else 1          # collectible R-floor
    cap = 3.0 if mood == "fun" else E_CAP
    if R == 0 and U >= 1.5:                    # rare cosmetic gets a foot in the door
        R = floor
    note = ""
    # R overrides: take the strongest of "crosses a vault threshold" (breakpoint
    # proximity), "upgrades my weakest slot" (ilvl-relative), and "the currency it
    # yields still has a consumer" (needs-first Phase 1). When none has data (no
    # breakpoint/ceiling/currency-yield, or a pre-schema-4 dump) fall back to
    # reward_base exactly as before. See scoring-model.md.
    overrides = [ov for ov in (breakpoint_R(cand, state),
                               slot_target_R(cand, state),
                               currency_R(cand, state)) if ov is not None]
    if overrides:
        R, note = max(overrides, key=lambda ov: ov[0])
    # Enjoyment: honor an explicit numeric `enjoyment`, else the (venue-keyed) table.
    if isinstance(cand.get("enjoyment"), (int, float)):
        E = min(float(cand["enjoyment"]), cap)
    else:
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
        prog = quest_progress_note(c, state)
        note = " · ".join(x for x in (f"at {prog}" if prog else "", note) if x)
        rows.append({"c": c, "score": s, "lead": lead, "state": st, "note": note})
    rows.sort(key=lambda r: r["score"], reverse=True)

    picks, spent = [], 0.0
    for r in rows:
        t = float(r["c"].get("time_blocks", 1))
        if spent + t <= budget + 1e-9:
            picks.append(r); spent += t
    return {"picks": picks, "all": rows, "budget": budget, "spent": spent}


# --------------------------------------------------------------------------- #
def _fmt_age(mtime: float) -> str:
    """Human 'how old is this dump' from an mtime, e.g. '2h ago', '3d ago'."""
    import time
    secs = max(0, time.time() - mtime)
    if secs < 90:
        return "just now"
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if secs >= n:
            return f"{int(secs // n)}{unit} ago"
    return "just now"


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
    p.add_argument("--character", help="restrict auto-find to this character's dump "
                                       "(else newest dump across the roster wins)")
    p.add_argument("--wow-path", default=DEFAULT_WOW)
    p.add_argument("--include-repeatables", action="store_true",
                   help="also rank the scraper catalog (repeatables.json); "
                        "rows marked ~ have placeholder time/enjoyment")
    args = p.parse_args(argv)

    state = load_state(args.state, args.wow_path, args.character)
    result = plan(args.minutes, state, args.mood, args.include_repeatables)

    if state is None:
        src = "no PlannerState dump — gates marked (?)"
    else:
        # Surface the dump's mtime so a stale dump (played a different char since)
        # is obvious — this is the "the char you just played" signal for 0.1.
        try:
            age = _fmt_age(os.path.getmtime(state["_path"]))
        except OSError:
            age = "?"
        src = (f"state: {Path(state['_path']).name} "
               f"(char {state.get('character','?')}, dumped {age})")
    print(f"\nSession plan · {args.minutes} min · mood={args.mood} · {src}\n")
    weak = weakest_slots(state)
    if weak:
        il = state.get("equippedIlvl")
        head = f"equipped ilvl {round(il)}" if isinstance(il, (int, float)) and il else "gear"
        slots = ", ".join(f"{s} {round(v)}" for s, v in weak)
        print(f"weakest slots ({head}): {slots}")
    cur = currency_context(state)
    if cur:
        print(f"crests: {cur}")
    if weak or cur:
        print()
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

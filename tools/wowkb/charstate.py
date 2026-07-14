"""Unified character-state loader — the single door that unions all three
sources the KB has on a character:

  1. **PlannerState `/ps` dump** — reset-state the Blizzard API can't see (vault
     progress, world-boss kills, weekly-quest completion, the event calendar)
     PLUS a mirror of equipment ilvls + **per-slot upgrade track/step** (schema>=8,
     read off the item tooltip — the reliable track source, present even for
     crafted gear the API drops), the **"…of the Dawn" achievements**, and
     currencies. This is the **offline spine**: always tried first, and it alone
     drives the planner when there is no network or no Blizzard credentials.
  2. **Blizzard profile API** — item names, specs, professions, renown, raid/M+
     history, and a *fallback* upgrade track (the API drops it on crafted/quest
     gear). Enrichment, when reachable.
  3. **Syndicator SavedVariables** — authoritative gold + the full currency
     table. Enrichment, when the WoW install is readable.

Graceful degradation: any source that errors is omitted and recorded under
`_sources` (+ `_errors`), so a caller (wowkb.plan) never breaks offline.

`load()` returns the `/ps` dump dict as the spine — so all existing plan.py
access by dump key keeps working — augmented with:
  - `equipment[].name` (API) / `.track` (normalized to {track, level, cap} — dump
    tooltip PRIMARY, API fallback; **None for genuinely untracked crafted/quest gear**)
  - `profile`         : the normalized API bundle (identity, gear, mplus, renown, …)
  - `syndicator`      : collect_currencies() result (gold + grouped currencies)
  - `track_by_slot`   : {slot: {track, level, cap}} for the gearing view / rewards
                        (tracked slots only; a crafted/untracked slot is absent)
  - `dawn_achievements`: {label: completed} from the schema>=8 achievements block —
                        tells whether a track's 50% warband discount is earned
  - `_sources`        : {planner_state, blizzard_api, syndicator} booleans

The Lua SavedVariables parser + `load_state` live here (moved from plan.py, which
re-imports them) so this module is the one place that reads a `/ps` dump.
"""

from __future__ import annotations

import glob
import os
import re
from pathlib import Path

DEFAULT_WOW = "/mnt/c/Program Files (x86)/World of Warcraft/_retail_"
DEFAULT_REALM = "kiljaeden"


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
# Enrichment: fold the Blizzard API + Syndicator onto the dump spine.         #
# --------------------------------------------------------------------------- #

# Blizzard API equipment slot display-name → PlannerState dump slot name.
_API_SLOT = {
    "Head": "head", "Neck": "neck", "Shoulder": "shoulder", "Shoulders": "shoulder",
    "Chest": "chest", "Waist": "waist", "Legs": "legs", "Feet": "feet",
    "Wrist": "wrist", "Hands": "hands",
    "Finger 1": "finger1", "Finger 2": "finger2",  # dump's internal slot names
    "Ring 1": "finger1", "Ring 2": "finger2",      # API's display names for the same slots
    "Trinket 1": "trinket1", "Trinket 2": "trinket2", "Back": "back",
    "Main Hand": "mainhand", "Off Hand": "offhand", "Two-Hand": "mainhand",
}

# Upgrade-track line as it appears on an item, e.g. "Hero 3/6", "Champion 2/8".
_TRACK_RE = re.compile(
    r"\b(Explorer|Adventurer|Veteran|Champion|Hero|Myth)\b\s*(\d+)?\s*(?:/\s*(\d+))?",
    re.I)


def _track_from_dump_slot(e: dict) -> dict | None:
    """Normalize the addon dump's per-slot track fields (schema>=8) into the shared
    {track, level, cap} shape. This is the PRIMARY track source — read off the item
    tooltip in-game, so it's present even for crafted gear the API drops. Returns
    None when the slot has no track line at all (a genuinely untracked crafted/quest
    piece — e.g. a spark-crafted belt), which the caller preserves as None rather
    than fabricating a band from ilvl.
    """
    tr = e.get("track")
    if not isinstance(tr, str) or not tr:
        return None
    lvl, cap = e.get("upgradeLevel"), e.get("upgradeMax")
    return {
        "track": tr.title(),
        "level": int(lvl) if isinstance(lvl, (int, float)) else None,
        "cap": int(cap) if isinstance(cap, (int, float)) else None,
    }


def _track_from_item(raw_item: dict) -> dict | None:
    """Parse {track, level, cap} from an API equipment item's upgrade line — the
    FALLBACK track source (used only when the dump has no track for the slot).

    The profile equipment endpoint carries the track on the item's
    `name_description.display_string` ("Hero 3/6") for tracked gear. Best-effort:
    returns None when the item isn't on a visible track (old/crafted/quest gear),
    and the caller falls back to ilvl-band inference.
    """
    nd = (raw_item.get("name_description") or {}).get("display_string") or ""
    m = _TRACK_RE.search(nd)
    if not m:
        return None
    return {
        "track": m.group(1).title(),
        "level": int(m.group(2)) if m.group(2) else None,
        "cap": int(m.group(3)) if m.group(3) else None,
    }


def _tracks_by_slot(prof: dict) -> dict:
    out = {}
    for it in (prof.get("equipment") or {}).get("equipped_items", []):
        slot = _API_SLOT.get((it.get("slot") or {}).get("name"))
        if not slot:
            continue
        t = _track_from_item(it)
        if t:
            out[slot] = t
    return out


def _merge_gear(state: dict, api_gear: list[dict], tracks: dict) -> None:
    """Overlay API item names + tracks onto the dump's equipment (by slot), or
    synthesize dump-shaped equipment from the API when there is no /ps dump."""
    by_slot = {}
    for g in api_gear:
        slot = _API_SLOT.get(g.get("slot"))
        if slot:
            by_slot[slot] = g
    eq = state.get("equipment")
    if eq:
        for e in eq:
            g = by_slot.get(e.get("slot"))
            if g:
                e.setdefault("name", g.get("name"))
                e["tier"] = bool(e.get("tier")) or bool(g.get("tier"))
            # track: the dump tooltip (schema>=8) is PRIMARY and was already
            # normalized to a {track,level,cap} dict (or None) by load(). Only fall
            # back to the API track when the dump had none AND the slot isn't a
            # genuinely untracked crafted piece the API would also miss.
            if not e.get("track"):
                t = tracks.get(e.get("slot"))
                if t:
                    e["track"] = t
    else:
        syn = []
        for slot, g in by_slot.items():
            row = {"slot": slot, "ilvl": g.get("ilvl"), "itemID": g.get("id"),
                   "name": g.get("name"), "tier": bool(g.get("tier"))}
            if slot in tracks:
                row["track"] = tracks[slot]
            syn.append(row)
        if syn:
            state["equipment"] = syn


def load(character: str | None = None, realm: str = DEFAULT_REALM,
         wow_path: str = DEFAULT_WOW, *, state_path: str | None = None,
         enrich: bool = True, syndicator: bool = True) -> dict | None:
    """Union the three sources into one dump-shaped dict (see module docstring).

    The `/ps` dump is the spine and always drives gating; `enrich=True` folds the
    Blizzard API + Syndicator on top when reachable, degrading silently otherwise.
    `syndicator=False` skips only the Syndicator read (the profile API still runs).
    Returns None only when there is neither a dump nor any enrichment to report.
    """
    dump = load_state(state_path, wow_path, character)
    state: dict = dict(dump) if dump else {}
    sources = {"planner_state": bool(dump)}
    name = character or state.get("character")

    # schema>=8: normalize per-slot track (raw string + upgradeLevel/Max) → a single
    # {track,level,cap} dict, or None for untracked crafted/quest gear. Done here so
    # every consumer sees one shape whether or not API enrichment runs below.
    for e in state.get("equipment") or []:
        if isinstance(e, dict):
            e["track"] = _track_from_dump_slot(e)

    # schema>=8: normalize the "…of the Dawn" achievement block to {label: completed}.
    # From the dump, so it's available even offline (no enrichment needed).
    ach = state.get("achievements")
    if isinstance(ach, list):
        state["dawn_achievements"] = {
            a["label"]: bool(a.get("completed"))
            for a in ach if isinstance(a, dict) and a.get("label")
        }

    # schema>=9: normalize the meta-achievement block (criterion progress, not just
    # completed) → {label: {earned, needed, completed, id}}. Account-wide, offline.
    # e.g. timeways_v = Spawn of Vyranoth mount meta (weeks of Mastery earned / 4).
    meta = state.get("metaAchievements")
    if isinstance(meta, list):
        state["meta_achievements"] = {
            a["label"]: {
                "id": a.get("id"),
                "earned": a.get("earned"),
                "needed": a.get("needed"),
                "completed": bool(a.get("completed")),
            }
            for a in meta if isinstance(a, dict) and a.get("label")
        }

    if enrich and name:
        # Blizzard API — item names, upgrade tracks, and the full profile bundle.
        try:
            from wowkb import character as charmod  # deferred: avoids import cycle
            prof = charmod.fetch_profile(realm, name)
            if "_error" not in prof.get("summary", {}):
                profile = charmod.normalize(prof)
                tracks = _tracks_by_slot(prof)
                state["profile"] = profile
                _merge_gear(state, profile.get("gear") or [], tracks)
                sources["blizzard_api"] = True
            else:
                sources["blizzard_api"] = False
        except Exception as e:  # noqa: BLE001 — enrichment is best-effort
            sources["blizzard_api"] = False
            state.setdefault("_errors", {})["blizzard_api"] = str(e)

        # Syndicator — authoritative gold + full currency table.
        if syndicator:
            try:
                from wowkb import character as charmod  # deferred
                cur = charmod.collect_currencies(name, realm, wow_path)
                if cur and not cur.get("_error"):
                    state["syndicator"] = cur
                    sources["syndicator"] = True
                    # Same Syndicator file already has the full item inventory — pull
                    # item counts here too (sparks, voidshards, …) so every field
                    # flows through the one door, no per-item ID list in the addon.
                    items = charmod.collect_items(name, realm, wow_path)
                    if items and not items.get("_error"):
                        state["item_counts"] = items["counts"]
                else:
                    sources["syndicator"] = False
                    if cur and cur.get("_error"):
                        state.setdefault("_errors", {})["syndicator"] = cur["_error"]
            except Exception as e:  # noqa: BLE001
                sources["syndicator"] = False
                state.setdefault("_errors", {})["syndicator"] = str(e)

    # Per-slot track for the gearing view / rewards, built from the merged
    # equipment (dump-primary track, API fallback filled in above). Tracked slots
    # only — a crafted/untracked slot (track None) is intentionally absent.
    track_by_slot = {
        e["slot"]: e["track"]
        for e in (state.get("equipment") or [])
        if isinstance(e, dict) and e.get("slot") and isinstance(e.get("track"), dict)
    }
    if track_by_slot:
        state["track_by_slot"] = track_by_slot

    state["_sources"] = sources
    return state or None

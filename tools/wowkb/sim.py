"""`wowkb.sim` — a local SimulationCraft harness that refuses to lie quietly.

Design doc + field log: `todo/wowkb-sim.md`. **Read the field log before designing a
new comparison** — it is the list of ways this has already fooled us.

Simming Encomplete's Season 2 gear on 2026-08-20 produced five wrong answers before a
right one. Every error was in the *harness* — the hand-written profile and APL
scaffolding — and none were in simc or in the game data. That asymmetry is the whole
reason this module exists: the engine is trustworthy, re-improvised plumbing is not,
and it fails **silently**. A trinket that never fires yields a confident, plausible,
wrong number and nothing anywhere in simc's output says so.

**This is a LIVING command.** When a sim session produces a wrong or misleading answer,
the fix is a new GATE here — never a hand-edit to a profile or an APL. A hand-fix
repairs one answer and teaches the tool nothing; the next person hits the identical
trap. The firing gate below exists *only* because Stormbound Emblem of Dazar sat inert
through four comparisons and nothing said so.

Phases 1-2 ship three subcommands:

    uv run python -m wowkb.sim import <export.simc|->   # parse a /simc paste, store it
    uv run python -m wowkb.sim check <char>             # harness health only, NO DPS
    uv run python -m wowkb.sim compare <char> A=... B=...   # ranked variants, one frame

`import` is the single input door. Everything the tool needs — equipped gear, bag
candidates, vault choices, talents, currencies, catalyst charges, watermarks — is in one
`/simc` paste, already correctly slotted with item levels in comments. Do **not** mine
Syndicator SavedVariables or resolve slots from simc's DBC item data instead: that path
was tried on 2026-08-20 and dead-ends, because bag item *levels* exist nowhere on disk.

`check` runs a short sim and reports harness health only — deliberately no DPS, because
an unvalidated number is worse than no number: it gets acted on.

Exit codes follow the house convention: 0 ok · 1 a gate failed · 2 bad input or an
unsupported spec · 3 STALE engine data.

Nothing here writes to `knowledge/**`. A sim result is **evidence for an answer, not a
sourced claim**; results live under `raw/sim-results/` (gitignored) and carry a build
stamp, and a DPS number with no build stamp is not citable.
"""

import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys

from .simc import (
    CLASS_ALIASES,
    kb_path,
    SPEC_ALIASES,
    _titleseg,
    kb_specs,
    live_patch_date,
    staleness,
)

# Paths are owned here rather than imported from `_common`, which pulls in
# python-dotenv: this module has to stay importable from the stdlib-only test
# runner (`tools/tests/check_sim.py`). `wowkb.simc` declines `_common` the same way.
ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "raw"

# ── Where things live ────────────────────────────────────────────────────────
# The simc checkout is a local build, deliberately: no runtime download, so a result is
# reproducible from a commit SHA that is sitting on this disk.
SIMC_DIR = RAW / "addon-research" / "simc"
SIMC_BIN = SIMC_DIR / "build" / "simc"
PROFILES = SIMC_DIR / "profiles"
ITEM_EFFECT_INC = SIMC_DIR / "engine" / "dbc" / "generated" / "item_effect.inc"
ITEM_DATA_INC = SIMC_DIR / "engine" / "dbc" / "generated" / "item_data.inc"
SET_BONUS_INC = SIMC_DIR / "engine" / "dbc" / "generated" / "item_set_bonus.inc"

EXPORTS = RAW / "simc-exports"
RESULTS = RAW / "sim-results"

BUILD_SIMC = (
    "cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j"
)

# ── Slots ────────────────────────────────────────────────────────────────────
# The canonical simc names, from `util::slot_type_string` (engine/util/util.cpp).
# EVERY one is explicitly assigned or explicitly cleared when a profile is built —
# invariant 3, and not theoretical: the reference profile ships an `off_hand`, and a
# 2H-wielding character silently inherited it on 2026-08-20.
CANON_SLOTS = [
    "head", "neck", "shoulders", "back", "shirt", "chest", "waist", "legs", "feet",
    "wrists", "hands", "finger1", "finger2", "trinket1", "trinket2",
    "main_hand", "off_hand", "tabard",
]
# The addon emits the singular forms; simc registers both as aliases onto the same
# option, so either overwrites the other — but we normalize anyway so the builder's
# "did I set every slot" bookkeeping is answerable without knowing that.
SLOT_ALIASES = {"shoulder": "shoulders", "wrist": "wrists"}

# Cosmetic slots simc does not model. Their item effects ("Has Tabard") are real DBC
# rows that would otherwise fire the unimplemented-effect warning on every character.
COSMETIC_SLOTS = {"shirt", "tabard"}

# Identity/meta keys the reference profile also carries. The builder drops the
# reference's copies and re-emits ours, so the two can never half-merge.
IDENTITY_KEYS = {
    "level", "race", "spec", "role", "position", "source", "talents", "omnium_talents",
    "region", "server", "professions",
}

# WoW's ITEM_SPELLTRIGGER enum, as stored in item_effect.inc's `type` column.
TRIGGER_ON_USE = 0

# Failure #2: `use_item` without this cost −3.2% in every forced run on 2026-08-20.
# Nothing here writes an `actions` line, so this constant exists only to be asserted
# on — see `apl_hygiene()`.
OFF_GCD = "use_off_gcd=1"


# ══ Export parsing ═══════════════════════════════════════════════════════════

def _canon_slot(key: str) -> str | None:
    key = SLOT_ALIASES.get(key, key)
    return key if key in CANON_SLOTS else None


NAME_ILVL = re.compile(r"^(?P<name>.+?)\s+\((?P<ilvl>\d+)\)\s*$")


def _name_ilvl(comment: str) -> tuple[str | None, int | None]:
    """`Pyrewalker's Miter (295)` → ("Pyrewalker's Miter", 295). Either half may be
    absent — the vault block ships item lines with no name comment at all, and a cell
    that reads `not stated` is the point (failure #7: a blank reads as "negligible")."""
    m = NAME_ILVL.match(comment.strip())
    if not m:
        return (comment.strip() or None), None
    return m.group("name"), int(m.group("ilvl"))


def _item_id(item_string: str) -> int | None:
    m = re.search(r"\bid=(\d+)", item_string)
    return int(m.group(1)) if m else None


def parse_export(text: str) -> dict:
    """A `/simc` paste → structured data. The single input door.

    Sections are the addon's own (`core.lua`): equipped slots first, then
    `### Gear from Bags`, `### Weekly Reward Choices`, `### Additional Character Info`.
    Bag and vault entries are commented-out item lines preceded by a `# <Name> (<ilvl>)`
    comment — usually. Vault rows frequently ship with no name line, so the name is
    filled in from simc's own item table rather than left blank.
    """
    out: dict = {
        "character": None, "class": None, "spec": None, "level": None, "race": None,
        "region": None, "server": None, "role": None, "professions": None,
        "talents": None, "omnium_talents": None, "loadouts": [],
        "exported": None, "client_build": None, "toc": None, "addon_version": None,
        "equipped": {}, "bags": [], "vault": [],
        "catalyst_currencies": None, "upgrade_currencies": None,
        "slot_high_watermarks": None, "upgrade_achievements": None,
        "bonus_roll_currencies": None, "checksum": None,
    }

    # Header: `# Encomplete - Demonology - 2026-08-20 11:12 - US/Kil'jaeden`
    m = re.search(r"^#\s*(\S+)\s+-\s+(\w+)\s+-\s+(\d{4}-\d{2}-\d{2})", text, re.M)
    if m:
        out["exported"] = m.group(3)
    m = re.search(r"^#\s*WoW\s+([\d.]+),\s*TOC\s+(\d+)", text, re.M)
    if m:
        out["client_build"], out["toc"] = m.group(1), m.group(2)
    m = re.search(r"^#\s*SimC Addon\s+(\S+)", text, re.M)
    if m:
        out["addon_version"] = m.group(1)
    m = re.search(r"^#\s*Checksum:\s*(\S+)", text, re.M)
    if m:
        out["checksum"] = m.group(1)

    section = "equipped"
    pending: str | None = None  # the last `# ...` comment, i.e. a candidate name line

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("### "):
            head = stripped[4:].strip().lower()
            if head.startswith("gear from bags"):
                section = "bags"
            elif head.startswith("weekly reward choices"):
                section = "vault"
            elif head.startswith("end of weekly reward"):
                section = "post-vault"
            elif head.startswith("additional character info"):
                section = "info"
            pending = None
            continue

        if not stripped:
            pending = None
            continue

        if stripped.startswith("#"):
            body = stripped.lstrip("#").strip()
            if not body:
                continue

            # `# <slot>=,id=...` — a bag/vault candidate.
            if "=" in body and section in ("bags", "vault"):
                key, _, value = body.partition("=")
                slot = _canon_slot(key.strip())
                if slot:
                    name, ilvl = _name_ilvl(pending) if pending else (None, None)
                    out[section].append({
                        "slot": slot, "item_string": value.strip(),
                        "name": name, "ilvl": ilvl,
                        "item_id": _item_id(value),
                    })
                    pending = None
                    continue

            # The `### Additional Character Info` key=value comments.
            m = re.match(r"^(catalyst_currencies|upgrade_currencies|slot_high_watermarks"
                         r"|upgrade_achievements|bonus_roll_currencies)=(\S+)$", body)
            if m:
                out[m.group(1)] = m.group(2)
                pending = None
                continue

            # Alternate saved loadouts, kept for reference; the active one is the bare
            # `talents=` line above them.
            m = re.match(r"^talents=(\S+)$", body)
            if m:
                out["loadouts"].append({"name": pending, "talents": m.group(1)})
                pending = None
                continue

            pending = body
            continue

        if "=" not in line:
            pending = None
            continue

        key, _, value = line.partition("=")
        key = key.strip()

        # `warlock="Encomplete"` — the class token IS the option name. This is also the
        # line that creates a player in simc, which is why the builder never emits the
        # reference profile's copy of it alongside ours.
        if key.lower() in CLASS_ALIASES and value.strip().startswith('"'):
            out["class"] = key.lower()
            out["character"] = value.strip().strip('"')
            pending = None
            continue

        slot = _canon_slot(key)
        if slot:
            name, ilvl = _name_ilvl(pending) if pending else (None, None)
            out["equipped"][slot] = {
                "slot": slot, "item_string": value.strip(),
                "name": name, "ilvl": ilvl, "item_id": _item_id(value),
            }
            pending = None
            continue

        if key in IDENTITY_KEYS:
            out[key] = value.strip()
        pending = None

    return out


# ══ simc's own item table (metadata for the rows the export left unnamed) ════
#
# `item_data.inc` declares `std::array<dbc_item_data_t, ...>` in chunks; the struct is
# `dbc_item_data_t` (engine/dbc/item_data.hpp:17), NOT `item_data_t`. Every field we
# need sits BEFORE `socket_color[3]`, the row's only nested `{ a, b, c }` group — so
# the prefix is captured lazily up to the first `{` and brace nesting never arises.
#
# ⚠ The indices below were miscounted once (`type_flags` is easy to drop), which
# silently reported EVERY bag row as unwearable. They are asserted against three known
# rows in tools/tests/check_sim.py; change them there too or not at all.
ITEM_ROW = re.compile(r'^\s*\{\s*"((?:[^"\\]|\\.)*)",\s*(\d+),([^{}]*)\{', re.M)

# Field positions in the captured prefix, i.e. AFTER `name, id`.
F_LEVEL = 3           # base ilvl — NOT the item's actual ilvl, see below
F_QUALITY = 7
F_INVENTORY_TYPE = 8
F_ITEM_CLASS = 9
F_ITEM_SUBCLASS = 10
F_CLASS_MASK = 17
F_RACE_MASK = 18

ITEM_CLASS_WEAPON = 2
ITEM_CLASS_ARMOR = 4
# engine/dbc/data_enums.hh:357-363
ARMOR_MISC, ARMOR_CLOTH, ARMOR_LEATHER, ARMOR_MAIL, ARMOR_PLATE, ARMOR_COSMETIC = range(6)
ARMOR_NAME = {ARMOR_MISC: "misc", ARMOR_CLOTH: "cloth", ARMOR_LEATHER: "leather",
              ARMOR_MAIL: "mail", ARMOR_PLATE: "plate", ARMOR_COSMETIC: "cosmetic"}

# `util::class_id` (engine/util/util.cpp:1955-1981). The class_mask bit is
# `1 << (class_id - 1)`, exactly as `util::class_id_mask` computes it.
CLASS_IDS = {
    "warrior": 1, "paladin": 2, "hunter": 3, "rogue": 4, "priest": 5,
    "deathknight": 6, "death_knight": 6, "shaman": 7, "mage": 8, "warlock": 9,
    "monk": 10, "druid": 11, "demonhunter": 12, "demon_hunter": 12, "evoker": 13,
}

# `util::matching_armor_type` (engine/util/util.cpp:1201-1226) — transcribed, not
# invented. This is upstream's table and the only defensible source for it.
MATCHING_ARMOR_TYPE = {
    "warrior": ARMOR_PLATE, "paladin": ARMOR_PLATE, "deathknight": ARMOR_PLATE,
    "death_knight": ARMOR_PLATE,
    "hunter": ARMOR_MAIL, "shaman": ARMOR_MAIL, "evoker": ARMOR_MAIL,
    "druid": ARMOR_LEATHER, "rogue": ARMOR_LEATHER, "monk": ARMOR_LEATHER,
    "demonhunter": ARMOR_LEATHER, "demon_hunter": ARMOR_LEATHER,
    "mage": ARMOR_CLOTH, "priest": ARMOR_CLOTH, "warlock": ARMOR_CLOTH,
}

# `util::is_match_slot` (engine/util/util.cpp:1184-1200) — the 8 slots that carry an
# armor type at all. Everything else (neck, back, rings, trinkets, weapons) is exempt,
# which is upstream's rule and not a simplification of ours.
MATCH_SLOTS = {"head", "shoulders", "chest", "waist", "legs", "feet", "wrists", "hands"}

WEAPON_SLOTS = {"main_hand", "off_hand"}

_ITEM_META: dict[int, dict] | None = None


def _int(token: str):
    try:
        return int(token.strip(), 0)
    except ValueError:
        return None


def item_meta() -> dict[int, dict]:
    """item id → the handful of `dbc_item_data_t` columns the usability filter needs.

    ⚠ `level` is the item's BASE ilvl (250043 reads 197 for an item worn at 276), so it
    is parsed for completeness and never displayed. Row labels come from the export's
    own `# <Name> (<ilvl>)` comment, which is the only place the real ilvl exists.
    """
    global _ITEM_META
    if _ITEM_META is None:
        _ITEM_META = {}
        try:
            text = ITEM_DATA_INC.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return _ITEM_META
        for m in ITEM_ROW.finditer(text):
            item_id = int(m.group(2))
            if item_id in _ITEM_META:
                continue
            f = m.group(3).split(",")
            if len(f) <= F_RACE_MASK:
                continue
            _ITEM_META[item_id] = {
                "name": m.group(1),
                "id": item_id,
                "level": _int(f[F_LEVEL]),
                "quality": _int(f[F_QUALITY]),
                "inventory_type": _int(f[F_INVENTORY_TYPE]),
                "item_class": _int(f[F_ITEM_CLASS]),
                "item_subclass": _int(f[F_ITEM_SUBCLASS]),
                "class_mask": _int(f[F_CLASS_MASK]),
                "race_mask": _int(f[F_RACE_MASK]),
            }
    return _ITEM_META


def item_names() -> dict[int, str]:
    """item id → display name, from the simc checkout's generated item table.

    The vault block ships rows with no `# <Name>` comment, and "the three hands options"
    is not a reviewable sentence. This is a local file read, not a lookup service.
    """
    return {i: row["name"] for i, row in item_meta().items()}


def label(entry: dict) -> str:
    """A candidate's human label. Never blank: an unnamed row reads as its id."""
    name = entry.get("name") or item_names().get(entry.get("item_id") or -1)
    ilvl = entry.get("ilvl")
    if name and ilvl:
        return f"{name} ({ilvl})"
    if name:
        return f"{name} (ilvl not stated)"
    return f"id={entry.get('item_id')} (name and ilvl not stated)"


# ── Upgrade high watermarks ──────────────────────────────────────────────────
#
# `Enum.ItemRedundancySlot`, transcribed from Blizzard's own machine-generated API
# documentation: `Blizzard_APIDocumentationGenerated/ItemConstants_MainlineDocumentation
# .lua:28`, reachable as `uv run python -m wowkb.uiapi enum ItemRedundancySlot`. Tier 1
# and build-stamped. Transcribed, not derived — same treatment as MATCHING_ARMOR_TYPE.
#
# This is the key to the export's `slot_high_watermarks=<i>:<char>:<acct>` rows, which
# the addon writes with a bare `for slot = 0, 16` loop (SimulationCraft/core.lua:773-785)
# and no names.
#
# ⚠ It is NOT a permuted INVSLOT, which is why every attempt to read it as one failed on
# 2026-08-20. It is COARSER than the equipment slots: ONE `Finger` and ONE `Trinket` row
# for two worn items each, and weapons split by hand-count rather than by main/off.
ITEM_REDUNDANCY_SLOT = {
    0: "Head", 1: "Neck", 2: "Shoulder", 3: "Chest", 4: "Waist", 5: "Legs", 6: "Feet",
    7: "Wrist", 8: "Hand", 9: "Finger", 10: "Trinket", 11: "Cloak", 12: "Twohand",
    13: "MainhandWeapon", 14: "OnehandWeapon", 15: "OnehandWeaponSecond", 16: "Offhand",
}

# One enum row, two worn items. ⚠ What that row MEANS is NOT settled: Encomplete's
# `Finger` row reads 295 while a 305 ring is equipped, so it is provably not "the highest
# ilvl ever worn in this slot type". The working hypothesis (user, 2026-08-20, explicitly
# unverified) is that a paired slot is marked at the SECOND-highest — the level at which
# you actually have redundancy, which is what the enum's name suggests — so moving one
# 305 ring between finger1 and finger2 cannot raise both marks. Encomplete's trinkets are
# both 305 and cannot discriminate. Phase 4 (`crests`) must confirm this before costing a
# paired slot; assuming it is how a confident wrong crest allocation gets shipped.
REDUNDANCY_PAIRED = {"Finger", "Trinket"}


def parse_watermarks(export: dict) -> list[dict]:
    """`0:295:295/1:292:305/...` → named rows. Unknown indices survive as their number:
    a future build adding an enum member must not silently vanish from the table."""
    raw = export.get("slot_high_watermarks")
    if not raw:
        return []
    rows = []
    for chunk in raw.split("/"):
        parts = chunk.split(":")
        if len(parts) != 3:
            continue
        index = _int(parts[0])
        if index is None:
            continue
        name = ITEM_REDUNDANCY_SLOT.get(index, f"index {index} (unknown to this build)")
        rows.append({"index": index, "slot": name,
                     "character": _int(parts[1]), "account": _int(parts[2]),
                     "paired": name in REDUNDANCY_PAIRED})
    return rows


# ══ Can this character actually wear it? ═════════════════════════════════════
#
# Phase 1 disproved the assumption that the export's bag block is pre-filtered:
# `SimulationCraft/core.lua:GetBagItemStrings` filters ONLY on "has an equippable
# inventory type" — no armor class, no class usability. Encomplete's 68 bag rows carry
# mail, plate and a one-handed sword. This is also a CRASH guard, not just a
# correctness one: engine/player/player.cpp:2011 THROWS `Invalid type.` during gear
# init when `is_valid_type()` fails, so an unfiltered sweep aborts mid-run.

def wearable(item_id: int | None, cls: str, slot: str) -> str | None:
    """None if this character can wear it in this slot, else the reason it is excluded.

    Two tests, in upstream's own terms:

    1. `class_mask` — genuinely populated (Abyssal Immolator's Grasps is 0x0100,
       Warlock only), and what removes another class's tier set. simc itself never
       reads it for equip validation, so it would otherwise sim fine and lie.
    2. Armor type, mirroring `item_t::is_valid_type` (engine/item/item.cpp:1636-1645):
       `matching_armor_type >= item_subclass`, i.e. a plate class may wear cloth but
       not the reverse, with the COSMETIC subclass exempt — and only on the 8 slots
       `util::is_match_slot` covers.

    WEAPONS are deliberately NOT filtered here beyond test 1: simc carries no weapon
    usability data at all (`is_match_slot` excludes weapon slots, `class_mask` is never
    read for equip validation, `translate_weapon_subclass` is damage/speed math only),
    and authoring a 13-class weapon table with no upstream source to re-derive from
    would rot silently. `gear` prints weapon candidates under a NOT-usability-checked
    banner instead of pretending to know.
    """
    meta = item_meta().get(item_id or -1)
    if not meta:
        return None  # unknown to this simc build; the run itself will say so

    class_id = CLASS_IDS.get(cls)
    mask = meta["class_mask"]
    if class_id and mask:
        if not (mask & (1 << (class_id - 1))):
            return "other-class"

    if slot in MATCH_SLOTS and meta["item_class"] == ITEM_CLASS_ARMOR:
        sub = meta["item_subclass"]
        if sub != ARMOR_COSMETIC:
            allowed = MATCHING_ARMOR_TYPE.get(cls)
            if allowed is not None and sub is not None and sub > allowed:
                return ARMOR_NAME.get(sub, f"armor subclass {sub}")
    return None


def is_weapon(item_id: int | None) -> bool:
    meta = item_meta().get(item_id or -1)
    return bool(meta and meta["item_class"] == ITEM_CLASS_WEAPON)


# ══ Tier sets (the confound gate) ════════════════════════════════════════════
#
# Encomplete wears the S1 4pc and `hands` is a tier slot, so ANY non-tier glove drops
# 4pc → 3pc and reads several percent negative. simc models that correctly; the ROW
# reads as "this glove is bad" when it means "this glove costs you the 4pc". The
# living-command mandate says the fix for a misleading answer is a gate, not a footnote
# in the prose, so every candidate that changes a set count is annotated.
#
# `plan.py:TIER_SLOTS` is deliberately NOT used: that is a slot heuristic for the
# (unsimulated) gearing chart, not an item→set map.

SET_ROW = re.compile(
    r'^\s*\{\s*"((?:[^"\\]|\\.)*)"\s*,\s*"(?:[^"\\]|\\.)*"\s*,\s*"((?:[^"\\]|\\.)*)"\s*,'
    r'\s*(\d+),\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*\{([^}]*)\}',
    re.M)

_SET_BONUS: dict[int, list[dict]] | None = None


def set_bonuses() -> dict[int, list[dict]]:
    """item id → the set(s) it belongs to, from `item_set_bonus.inc`.

    Rows are `item_set_bonus_t` (engine/dbc/item_set_bonus.hpp): set_name, set_opt_name,
    tier, enum_id, set_id, bonus, class_id, spec, trait_sub_tree, spell_id, item_ids[17].
    One row per (set, bonus tier, spec), so the same item appears many times; we keep
    one entry per (item, set_id).
    """
    global _SET_BONUS
    if _SET_BONUS is None:
        _SET_BONUS = {}
        try:
            text = SET_BONUS_INC.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return _SET_BONUS
        for m in SET_ROW.finditer(text):
            entry = {"set_name": m.group(1), "tier": m.group(2),
                     "set_id": int(m.group(4)), "class_id": int(m.group(6))}
            for token in m.group(10).split(","):
                item_id = _int(token)
                if not item_id:
                    continue
                rows = _SET_BONUS.setdefault(item_id, [])
                if not any(r["set_id"] == entry["set_id"] for r in rows):
                    rows.append(entry)
    return _SET_BONUS


def set_counts(equipped: dict[str, dict], cls: str) -> dict[int, int]:
    """set_id → how many of its pieces this loadout is wearing (this class's sets only)."""
    class_id = CLASS_IDS.get(cls)
    counts: dict[int, int] = {}
    for entry in equipped.values():
        for row in set_bonuses().get(entry.get("item_id") or -1, []):
            if class_id and row["class_id"] != class_id:
                continue
            counts[row["set_id"]] = counts.get(row["set_id"], 0) + 1
    return counts


def set_name(set_id: int) -> str:
    for rows in set_bonuses().values():
        for row in rows:
            if row["set_id"] == set_id:
                return row["set_name"]
    return f"set {set_id}"


def _bonus_step(before: int, after: int) -> str | None:
    """Which set-bonus threshold this swap crosses, if any. 2pc and 4pc are the only
    ones Midnight ships, and crossing one is what makes a delta unreadable."""
    for step in (4, 2):
        if before >= step > after:
            return f"losing the {step}pc"
        if after >= step > before:
            return f"gaining the {step}pc"
    return None


def tier_note(export: dict, overrides: dict[str, str]) -> str | None:
    """`Reign of the Abyssal Immolator: 4 → 3 pieces — this delta includes losing the
    4pc`, or None when the swap leaves every set count alone."""
    cls = export["class"]
    before = set_counts(export["equipped"], cls)
    after = set_counts(variant_export(export, overrides)["equipped"], cls)
    parts = []
    for set_id in sorted(set(before) | set(after)):
        old, new = before.get(set_id, 0), after.get(set_id, 0)
        if old == new:
            continue
        step = _bonus_step(old, new)
        parts.append(f"{set_name(set_id)}: {old} → {new} pieces"
                     + (f" — this delta includes {step}" if step else
                        " — below the 2pc threshold either way"))
    return "; ".join(parts) or None


# ══ simc's item effects (the firing gate's subject) ══════════════════════════

# item_effect.inc rows are `{ id, spell_id, item_id, index, type, cooldown_group,
# cooldown_duration, cooldown_group_duration }, // Name`, matching item_effect_t in
# engine/dbc/item_effect.hpp. Read the struct, don't guess the column order.
EFFECT_ROW = re.compile(
    r"^\s*\{\s*(\d+),\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),"
    r"\s*(-?\d+),\s*(-?\d+)\s*\},\s*//\s*(.*)$", re.M)

_ITEM_EFFECTS: dict[int, list[dict]] | None = None


def item_effects() -> dict[int, list[dict]]:
    """item id → [{spell_id, type, index, name}], from the simc checkout."""
    global _ITEM_EFFECTS
    if _ITEM_EFFECTS is None:
        _ITEM_EFFECTS = {}
        try:
            text = ITEM_EFFECT_INC.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return _ITEM_EFFECTS
        for m in EFFECT_ROW.finditer(text):
            _ITEM_EFFECTS.setdefault(int(m.group(3)), []).append({
                "spell_id": int(m.group(2)),
                "index": int(m.group(4)),
                "type": int(m.group(5)),
                "name": m.group(9).strip(),
            })
    return _ITEM_EFFECTS


_SPELL_CACHE: dict[int, dict] = {}


def spell_info(spell_id: int) -> dict:
    """Name + cooldown for a spell, asked of simc itself (`spell_query`).

    The cooldown is what turns "0 uses" into "0 of an expected 2.5", and it lives in the
    spell, not the item: item_effect.inc carries `cooldown_duration = -1` for most
    on-use trinkets. ~0.08s per call, cached per process.
    """
    if spell_id in _SPELL_CACHE:
        return _SPELL_CACHE[spell_id]
    info: dict = {"id": spell_id, "name": None, "cooldown": None}
    proc = subprocess.run([str(SIMC_BIN), f"spell_query=spell.id={spell_id}"],
                          capture_output=True, text=True, check=False)
    out = proc.stdout
    m = re.search(r"^Name\s*:\s*(.+?)\s*\(id=\d+\)", out, re.M)
    if m:
        info["name"] = m.group(1).strip()
    m = re.search(r"^Cooldown\s*:\s*([\d.]+)\s*seconds", out, re.M)
    if m:
        info["cooldown"] = float(m.group(1))
    _SPELL_CACHE[spell_id] = info
    return info


def tokenize(name: str) -> str:
    """simc's `util::tokenize`: lowercase, apostrophes dropped, the rest underscored.

    "Freightrunner's Flask" → `freightrunners_flask`; "The King's Unyielding Wind" →
    `the_kings_unyielding_wind`. Report rows are keyed by these, so this is how an
    effect is found when its buff carries a different spell id than the item effect.
    """
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_",
                                     name.lower().replace("'", ""))).strip("_")


# ══ The reference profile: resolution chain ══════════════════════════════════

class Unsupported(Exception):
    """No usable APL for this spec — exit 2, never a silent fallback (failure #1)."""


def profile_path(tier: str, cls: str, spec: str, hero: str | None) -> pathlib.Path:
    """`MID2_Warlock_Demonology_Soulharvester.simc` and friends.

    `wowkb.simc.profile_filename` builds the same name for MID1; it now takes `tier=`
    so both callers share one naming rule instead of two copies drifting apart.
    """
    from .simc import profile_filename
    return PROFILES / tier / profile_filename(cls, spec, hero, tier=tier)


def kb_apl(cls: str, spec: str) -> tuple[pathlib.Path, list[str]] | None:
    """The generated `knowledge/classes/<class>/<spec>/simc-apl.md` priority list.

    This is the notable reuse in the chain: `wowkb.simc --kb` already maintains a
    current APL for 36 specs, and nothing consumed it programmatically until now. MID2
    reference coverage is partial — 35 files over ~22 specs, with all Druid, all Evoker,
    Havoc, Retribution, Windwalker, Arms, Fury, Holy/Discipline Priest and all four
    healers absent — so "use the upstream reference profile" cannot be the only path.
    """
    from .simc import read_gen_block, gen_actions
    # `kb_path` speaks lowered filename segments (`demon_hunter`/`beast_mastery`), not
    # the alias tokens the export uses (`dh`) — passing the token silently misses.
    path = kb_path(_titleseg(cls, CLASS_ALIASES).lower(),
                   _titleseg(spec, SPEC_ALIASES).lower())
    actions = gen_actions(read_gen_block(path))
    if not actions:
        return None
    return path, [a for a in actions if a.strip()]


APL_SOURCES = ("auto", "mid2", "mid1", "kb")


def resolve_reference(cls: str, spec: str, hero: str | None,
                      source: str = "auto") -> dict:
    """The 4-step chain. Never falls through to simc's built-in APL — that is failure #1,
    and it is what left on-use trinkets unfired through a whole session.

    MID2 → MID1 → the generated `simc-apl.md` → exit 2. `source=` pins one rung, which
    matters most for the MID1 rung: see the warning it carries.
    """
    cls_seg = _titleseg(cls, CLASS_ALIASES)
    spec_seg = _titleseg(spec, SPEC_ALIASES)

    tiers = {"auto": ("MID2", "MID1"), "mid2": ("MID2",), "mid1": ("MID1",),
             "kb": ()}[source]
    for tier in tiers:
        for want_hero in ([hero] if hero else [None]):
            path = profile_path(tier, cls, spec, want_hero)
            if path.is_file():
                warn = None
                if tier == "MID1":
                    # Not a formality. Measured 2026-08-16: MID1_Demon_Hunter_Havoc.simc
                    # was pinned to a 2026-03-13 commit — 151 days before 12.1 went live
                    # — and had been cited as current. The newest file that exists is not
                    # the same as a current one.
                    warn = (
                        f"{path.name} is a **MID1** (previous-season) profile. Upstream "
                        "regenerates profiles per spec and sometimes never gets to one, "
                        "so its APL may predate 12.1 by months. It does carry "
                        "consumables and a talents hash, which the KB APL does not — "
                        "that is the trade. `--apl-source kb` takes the current "
                        "priority list instead" + (
                            f" ({kb_path(cls, spec).relative_to(ROOT)})"
                            if kb_apl(cls, spec) else ", but none exists for this spec"))
                return {
                    "kind": "profile", "tier": tier, "path": path,
                    "text": path.read_text(encoding="utf-8"), "warn": warn,
                }

    kb = kb_apl(cls, spec)
    if kb:
        path, actions = kb
        return {
            "kind": "kb-apl", "tier": "simc-apl.md", "path": path,
            "actions": actions,
            "warn": (
                ("pinned to the KB APL" if source == "kb" else
                 f"no MID2/MID1 reference profile for {cls_seg}/{spec_seg}") +
                f"; composed a minimal profile around {_rel(path)}. "
                "It carries the current "
                "priority list but NO consumables, no talents hash and no profileset "
                "variants — those exist only in a generated profile."),
        }

    known = kb_specs(cls_seg.lower())
    raise Unsupported(
        f"no APL for {cls_seg}/{spec_seg}.\n"
        f"  tried: profiles/MID2/, profiles/MID1/, "
        f"{kb_path(cls_seg.lower(), spec_seg.lower()).relative_to(ROOT)}\n"
        f"  specs the KB carries for {cls_seg}: {', '.join(known) or 'none'}\n"
        "  Four specs have no upstream APL at all (Preservation, Mistweaver, Holy "
        "Paladin, Restoration Shaman) — simc does not model them.\n"
        "  Refusing to fall back to simc's built-in APL: that is the failure this tool "
        "exists to prevent.")


# ══ Profile building ═════════════════════════════════════════════════════════

def strip_reference(text: str) -> list[str]:
    """The reference profile minus everything we re-own: its player line, its identity,
    its gear, and its Gear Summary. What survives is the APL and the consumables — the
    maintained content, including the trinket-priority logic that took a day to
    rediscover by hand on 2026-08-20."""
    kept: list[str] = []
    in_summary = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# Gear Summary"):
            in_summary = True
            continue
        if in_summary:
            if stripped.startswith("#") or not stripped:
                continue
            in_summary = False
        if not stripped or stripped.startswith("#"):
            kept.append(line)
            continue
        key = stripped.partition("=")[0].strip()
        if key.lower() in CLASS_ALIASES or key in IDENTITY_KEYS:
            continue
        if _canon_slot(key):
            continue
        kept.append(line)
    return kept



# ══ Character overrides (the declared, gated exception) ══════════════════════
#
# The mandate is "never write an actions line", and this is the one narrow place the
# tool does. It exists because a real character hit a real upstream deadlock that no
# gear arrangement fixes: Encomplete's two trinkets are both ilvl 305, upstream picks
# the damage trinket with a STRICT inequality (`trinket.2.ilvl>trinket.1.ilvl`), and an
# exact tie therefore always resolves to trinket1 — after which each trinket's rung
# waits on the other's cooldown. Measured 2026-08-20: 0 presses in 300s, and swapping
# the two indices in game reproduces it exactly, so the deadlock follows the ITEM.
#
# Five fences keep this from becoming the hand-edited-APL failure it replaces:
#   1. Only `variable,name=X,value=N` lines, and THE TOOL BUILDS THE LINE. Nothing from
#      the JSON is ever pasted into a profile, so the file cannot carry an action.
#   2. The variable must already be DECLARED by the upstream reference. An override can
#      re-point a decision upstream already makes; it cannot invent behaviour. A
#      variable upstream renames stops applying and says so.
#   3. Every row of every table computed with one active is branded.
#   4. The firing gate runs unchanged and stays the judge. The point of an override is
#      to make the gate go green HONESTLY.
#   5. `why` and `measured` are mandatory; an unmeasured override is a superstition.

SIM_OVERRIDES = pathlib.Path(__file__).resolve().parent / "data" / "sim_overrides.json"

VAR_NAME = re.compile(r"^[a-z0-9_]+$")
REF_VAR = re.compile(r"variable,name=([a-z0-9_]+)")


def load_overrides(character: str | None) -> dict:
    """The override entry for this character, or {}. Never raises: a malformed or
    missing file must degrade to 'upstream unaided', not to a crash mid-sweep."""
    if not character:
        return {}
    try:
        data = json.loads(SIM_OVERRIDES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    entry = data.get(character.strip().lower())
    return entry if isinstance(entry, dict) else {}


def resolve_overrides(ref: dict, entry: dict) -> tuple[list[dict], list[str]]:
    """(accepted, rejected-with-reasons), validated against the reference APL itself."""
    declared = set(REF_VAR.findall(ref.get("text") or "\n".join(ref.get("actions") or [])))
    accepted, rejected = [], []
    for name, spec in (entry.get("variables") or {}).items():
        if not VAR_NAME.match(name):
            rejected.append(f"{name!r}: not a plain variable name")
            continue
        if not isinstance(spec, dict) or "value" not in spec:
            rejected.append(f"{name}: no value")
            continue
        if not (spec.get("why") and spec.get("measured")):
            rejected.append(f"{name}: missing `why` and/or `measured` — an override with "
                            "no recorded measurement is a superstition")
            continue
        try:
            value = float(spec["value"])
        except (TypeError, ValueError):
            rejected.append(f"{name}: value is not a number")
            continue
        if name not in declared:
            rejected.append(f"{name}: the upstream reference APL does not declare this "
                            "variable — it may have been renamed; override NOT applied")
            continue
        accepted.append({"name": name, "value": value, "why": spec["why"],
                         "measured": spec["measured"]})
    return accepted, rejected


def override_brand(built: dict) -> str:
    bits = [o["name"] for o in built.get("overrides") or []]
    brand = f"⚠ OVERRIDE({', '.join(bits)}) " if bits else ""
    if built.get("apl_append"):
        # Louder than a variable override, because this one adds an ACTION. A row lifted
        # out of the table must carry the fact that upstream did not press these.
        brand += f"⛔ APL-APPEND(x{len(built['apl_append'])}) "
    return brand


def print_overrides(built: dict, indent: str = "    ") -> None:
    for o in built.get("overrides") or []:
        print(f"{indent}⚠ OVERRIDE  variable.{o['name']} = {o['value']:g}  "
              f"[measured {o['measured']}]")
        print(f"{indent}            {o['why']}")
    for a in built.get("apl_append") or []:
        print(f"{indent}⛔ APL-APPEND  actions+=/{a['line']}  [measured {a['measured']}]")
        print(f"{indent}               {a['why']}")
    for why in built.get("overrides_rejected") or []:
        print(f"{indent}⚠ OVERRIDE REJECTED  {why}")



# `use_item` lines appended to upstream's list — the SECOND declared exception, and a
# narrower one than it looks. Measured 2026-08-20 on Encomplete's two-on-use trinket
# set, common random numbers, 2000 iterations, stock upstream profile:
#     upstream untouched   Freightrunner 1.0   Stormbound 0.0    196,547 dps
#     forced on cooldown   Freightrunner 3.6   Stormbound 2.8    200,837  (+2.18%)
#     Tyrant-aligned       Freightrunner 3.2   Stormbound 2.4    203,099  (+3.33%)
# So upstream leaves >3% on the floor for this gear, and a human pressing two buttons
# recovers it. Refusing to model that would make the sim wrong in the direction that
# matters — it would rank gear as if the trinkets did not exist.
#
# Three fences, all mechanical:
#   1. `use_item` ONLY. Anything else is rejected, so this can never become "rewrite the
#      rotation" — the thing failure #3 showed swings 3.21% on ordering alone.
#   2. `use_off_gcd=1` is MANDATORY. Failure #2 was exactly this line without that flag,
#      and it baked −3.2% into every forced run for a day.
#   3. APPENDED with `actions+=/`, never `actions=`. Upstream's priority list survives
#      intact underneath; these only get a look when it has nothing to cast.
APL_APPEND_OK = re.compile(r"^use_item,[A-Za-z0-9_,.=|&!%<>+*()@$-]+$")


def resolve_apl_append(entry: dict) -> tuple[list[dict], list[str]]:
    accepted, rejected = [], []
    for spec in (entry.get("apl_append") or []):
        line = (spec or {}).get("line", "") if isinstance(spec, dict) else ""
        line = line.strip()
        if not APL_APPEND_OK.match(line):
            rejected.append(f"{line[:48]!r}: only `use_item,...` lines may be appended")
            continue
        if OFF_GCD not in line:
            rejected.append(f"{line[:48]!r}: missing {OFF_GCD} — a use_item rung without "
                            "it costs a GCD when it fires (failure #2, −3.2%)")
            continue
        if not (spec.get("why") and spec.get("measured")):
            rejected.append(f"{line[:48]!r}: missing `why` and/or `measured`")
            continue
        accepted.append({"line": line, "why": spec["why"], "measured": spec["measured"]})
    return accepted, rejected


def build_profile(export: dict, ref: dict, *, name: str | None = None,
                  overrides: dict[str, str] | None = None,
                  apl_override: list[str] | None = None,
                  use_overrides: bool = True) -> tuple[str, dict]:
    """The base profile, plus a bookkeeping record of what was set where.

    Every canonical slot is emitted — assigned from the export or explicitly cleared —
    so no reference gear can leak through, and so the "did it leak" gate has something
    to compare against rather than a guess.
    """
    overrides = overrides or {}
    cls = export["class"]
    lines: list[str] = [
        f'{cls}="{name or export["character"]}"',
        f'level={export.get("level") or 90}',
    ]
    for key in ("race", "spec", "role", "region", "server", "professions"):
        if export.get(key):
            lines.append(f"{key}={export[key]}")
    if export.get("talents"):
        lines.append(f"talents={export['talents']}")
    if export.get("omnium_talents"):
        lines.append(f"omnium_talents={export['omnium_talents']}")
    lines.append("")

    if ref["kind"] == "profile":
        lines += strip_reference(ref["text"])
    else:
        lines += ["# Minimal profile composed around the generated KB APL — no "
                  "consumables are available from this source.", ""] + ref["actions"]

    if apl_override:
        # Complete `actions...=` lines, replacing the default list. A later `actions=`
        # ASSIGNS where `actions+=/` appends, so this overrides upstream's top-level
        # list while leaving its sublists (and precombat) in place.
        lines += ["", "# ⚠ UNVALIDATED HARNESS — hand-written actions replace the "
                  "upstream priority list.", *apl_override]

    # Character overrides go AFTER the reference's own precombat, so a later
    # `variable,name=X` assignment wins over upstream's. Nothing here is copied from the
    # JSON — the line is constructed from a validated name and a float.
    applied, rejected, appended = ([], [], [])
    if use_overrides and not apl_override:
        entry = load_overrides(export.get("character"))
        applied, rejected = resolve_overrides(ref, entry)
        appended, app_rejected = resolve_apl_append(entry)
        rejected += app_rejected
        if appended:
            lines += ["", "# ⛔ APL-APPEND — `use_item` rungs appended BELOW upstream's "
                      "own list; see wowkb/data/sim_overrides.json"]
            lines += [f"actions+=/{a['line']}" for a in appended]
        if applied:
            lines += ["", "# ⚠ CHARACTER OVERRIDE — re-points variables the upstream APL "
                      "already declares; see wowkb/data/sim_overrides.json"]
            lines += [f"actions.precombat+=/variable,name={o['name']},value={o['value']:g}"
                      for o in applied]

    lines += ["", "# ── gear: every slot explicitly assigned or explicitly cleared ──"]
    assigned, cleared = {}, []
    for slot in CANON_SLOTS:
        if slot in overrides:
            value = overrides[slot]
        else:
            entry = export["equipped"].get(slot)
            value = entry["item_string"] if entry else ""
        lines.append(f"{slot}={value}")
        if value:
            assigned[slot] = value
        else:
            cleared.append(slot)

    return "\n".join(lines) + "\n", {"assigned": assigned, "cleared": cleared,
                                      "overrides": applied, "overrides_rejected": rejected,
                                      "apl_append": appended}


# ══ Running simc ═════════════════════════════════════════════════════════════

def simc_available() -> str | None:
    if SIMC_BIN.is_file():
        return None
    return (f"error: no simc binary at {SIMC_BIN.relative_to(ROOT)}\n"
            f"  build it in {SIMC_DIR.relative_to(ROOT)}:\n    {BUILD_SIMC}\n"
            "  This tool never downloads a binary at runtime — a result must be "
            "reproducible from a commit SHA on this disk.")


def simc_commit() -> dict | None:
    """The local checkout's HEAD → the same `{sha, short, date}` shape `wowkb.simc`
    uses, so `staleness()` works on it with no network call."""
    proc = subprocess.run(["git", "-C", str(SIMC_DIR), "log", "-1", "--format=%H %cI"],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    sha, _, iso = proc.stdout.strip().partition(" ")
    return {"sha": sha, "short": sha[:7], "date": iso[:10]}


def simc_data_build() -> str | None:
    """The client build simc's DBC was generated from, off its own banner line."""
    proc = subprocess.run([str(SIMC_BIN), "spell_query=spell.id=1"],
                          capture_output=True, text=True, check=False)
    m = re.search(r"for World of Warcraft ([\d.]+)", proc.stdout)
    return m.group(1) if m else None


def run_simc(profile: str, options: dict, workdir: pathlib.Path,
             tag: str, *, log_file: pathlib.Path | None = None
             ) -> tuple[dict, pathlib.Path]:
    """One simc invocation → parsed JSON. One invocation is one comparison frame; the
    caller must never delta a number from here against one from another call (failure
    #4 — it shipped a wrong vault recommendation).

    `log_file` routes simc's text output somewhere readable instead of /dev/null. It is
    for `log` alone: the combat log is a single-sample artifact, and every other command
    here reports statistics, which a log cannot support.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    profile_file = workdir / f"{tag}.simc"
    json_file = workdir / f"{tag}.json"
    body = profile + "\n" + "\n".join(f"{k}={v}" for k, v in options.items()) + "\n"
    profile_file.write_text(body, encoding="utf-8")

    proc = subprocess.run(
        [str(SIMC_BIN), str(profile_file), f"json2={json_file}",
         f"output={log_file if log_file else '/dev/null'}"],
        capture_output=True, text=True, check=False)
    if not json_file.is_file():
        raise RuntimeError(
            f"simc produced no JSON for {tag}\n"
            + (proc.stdout[-2000:] or "") + (proc.stderr[-2000:] or ""))
    return json.loads(json_file.read_text(encoding="utf-8")), profile_file


# ══ The firing gate ══════════════════════════════════════════════════════════
#
# The highest-value assertion in this tool, and the reason it exists. A silent no-op is
# the characteristic failure mode of gear sims: simc drops `use_item,slot=X` to a
# background action when slot X has no on-use effect it can find, and says nothing
# unless `debug=1` (engine/player/player.cpp, use_item_t::init).

def _observed(player: dict, keys: set[str], ids: set[int]) -> tuple[float, bool]:
    """(times the effect resolved, whether the engine knows it at all).

    Matched three ways because an effect's buff need not share the item's name or the
    item effect's spell id: by report-row token, by the item's own token, and by spell
    id where the report carries one.
    """
    seen = False
    count = 0.0
    for stat in player.get("stats", []):
        if stat.get("name") in keys or stat.get("id") in ids:
            seen = True
            count = max(count, float(stat.get("num_executes", {}).get("mean", 0.0)))
    for buff in player.get("buffs", []) + player.get("buffs_constant", []):
        if buff.get("name") in keys or buff.get("spell") in ids:
            seen = True
            count = max(count, float(buff.get("start_count", 0.0)))
    for proc in player.get("procs", []):
        if proc.get("name") in keys:
            seen = True
            count = max(count, float(proc.get("count", 0.0)))
    return count, seen


def probe_on_use(export: dict, ref: dict, slot: str, keys: set[str],
                 ids: set[int]) -> float:
    """Force this one slot on cooldown and count the uses. The discriminator.

    "No buff and no action" has two causes with opposite verdicts: simc does not model
    the effect (an upstream absence, not our problem), or simc models it fine and the
    APL never pressed it (our problem, and the exact shape of the 2026-08-20 disaster —
    Stormbound Emblem of Dazar sat inert through four comparisons). Only forcing the
    press separates them, so the gate forces it rather than guessing.

    The probe is throwaway and reports no DPS; `check` prints none either way.
    """
    profile, _ = build_profile(
        export, ref, apl_override=[f"actions=use_item,{OFF_GCD},slot={slot}"])
    try:
        data, _ = run_simc(profile, {"iterations": 50, "fight_style": "Patchwerk",
                                     "max_time": 300, "desired_targets": 1},
                           RESULTS, f"probe-{slot}")
    except (RuntimeError, IndexError, KeyError):
        return 0.0
    return _observed(data["sim"]["players"][0], keys, ids)[0]


def effect_subjects(export: dict) -> list[dict]:
    """Every equipped item's special effect, with the keys and spell ids that identify
    it in a report or a combat log.

    Shared by the firing gate (which counts them in aggregate) and `log` (which places
    them on a timeline), so the two can never disagree about what an effect IS.

    An on-use item usually carries a passive half as a second row (Stormbound Emblem
    ships both an on-use and an equip row, both named "The King's Unyielding Wind").
    They are one effect to a reader, so an item with an on-use effect is judged on the
    on-use and its passive rows are not reported separately — otherwise every on-use
    trinket reads as two findings.
    """
    subjects = []
    for slot in CANON_SLOTS:
        entry = export["equipped"].get(slot)
        if not entry or slot in COSMETIC_SLOTS:
            continue
        item_id = entry.get("item_id")
        effects = item_effects().get(item_id or -1, [])
        if not effects:
            continue
        item_token = tokenize(entry["name"] or item_names().get(item_id, "") or "")
        on_use_rows = [e for e in effects if e["type"] == TRIGGER_ON_USE]
        for effect in (on_use_rows or effects):
            info = spell_info(effect["spell_id"])
            eff_name = info["name"] or effect["name"]
            on_use = effect["type"] == TRIGGER_ON_USE
            subjects.append({
                "slot": slot, "entry": entry, "item": label(entry),
                "effect": eff_name, "spell_id": effect["spell_id"], "on_use": on_use,
                "cooldown": info["cooldown"] if on_use else None,
                "keys": {tokenize(eff_name)} | ({item_token} if item_token else set()),
                "ids": {effect["spell_id"]} | ({info["id"]} if info.get("id") else set()),
            })
    return subjects


def firing_gate(export: dict, ref: dict, data: dict) -> list[dict]:
    """Every equipped item's special effects, checked against what the run observed."""
    player = data["sim"]["players"][0]
    fight = float(player["collected_data"]["fight_length"]["mean"])
    findings: list[dict] = []

    for sub in effect_subjects(export):
        slot, keys, ids = sub["slot"], sub["keys"], sub["ids"]
        on_use, cooldown = sub["on_use"], sub["cooldown"]
        count, seen = _observed(player, keys, ids)
        expected = fight / cooldown if cooldown else None

        common = {
            "slot": slot, "item": sub["item"], "effect": sub["effect"],
            "spell_id": sub["spell_id"], "on_use": on_use,
            "cooldown": cooldown, "expected": expected, "observed": count,
            "forced": None,
        }
        if on_use and count == 0.0:
            forced = probe_on_use(export, ref, slot, keys, ids)
            common["forced"] = forced
            if forced > 0:
                findings.append({**common, "level": "FAIL", "why": (
                    "on-use effect NEVER FIRED under the upstream APL — and it is "
                    f"not an engine gap: forcing this slot on cooldown fired it "
                    f"{forced:.1f} times. Every DPS number from this gear set is "
                    "measuring a trinket that is not being pressed.")})
            else:
                findings.append({**common, "level": "WARN", "why": (
                    "on-use effect never fired, AND forcing the slot on cooldown "
                    "fired nothing either — simc does not model this effect. An "
                    "upstream absence, not a harness fault; the item still "
                    "contributes its stats.")})
        elif not seen:
            findings.append({**common, "level": "WARN", "why": (
                "registered in simc's item table but produced no buff and no "
                "action — possibly unimplemented")})
        elif count == 0.0:
            findings.append({**common, "level": "WARN", "why": (
                "proc effect never triggered")})
        elif expected and count < 0.5 * expected:
            findings.append({**common, "level": "WARN", "why": (
                f"fired {count:.1f} of an expected ~{expected:.1f} "
                f"({count / expected:.0%}) — held, gated or contended")})
    return findings


def leak_gate(export: dict, built: dict, data: dict) -> list[str]:
    """Any slot the run wore that the builder did not put there.

    The reference profile ships a full gear set. If a slot survives into the run without
    the builder assigning it, everything downstream is measuring somebody else's gear.
    """
    worn = set(data["sim"]["players"][0].get("gear", {}))
    return sorted(worn - set(built["assigned"]))


def apl_hygiene(profile: str) -> list[str]:
    """`use_item` rungs that will cost a GCD when they fire (failure #2: −3.2%).

    Reported as a NOTE, not a warning, and deliberately: we never write an `actions`
    line, so every hit here is upstream content — and upstream puts on-GCD `use_item`
    rungs at the bottom of its item list ON PURPOSE, as the fallback below the off-GCD
    ones. A gate that fires on every character forever teaches nothing. What failure #2
    actually was is a HAND-WRITTEN `use_item` missing the flag, so this becomes a
    warning only under `--apl-override`, where the actions are ours.
    """
    bad = []
    for line in profile.splitlines():
        line = line.strip()
        if not line.startswith("actions"):
            continue
        for action in line.partition("=")[2].split("/"):
            action = action.strip()
            if action.startswith("use_item,") and OFF_GCD not in action:
                bad.append(action)
    return bad


# ══ Comparison frames: one invocation, one frame, no cross-frame deltas ══════
#
# Failure #4 shipped a wrong vault recommendation because two numbers came from two
# simc invocations with different frames. This section is the structural prevention:
# a delta is only ever computed from `Frame.results`, every result carries the id of
# the frame that produced it, and `frame_deltas` refuses a mismatch. There is no code
# path that takes two run ids — the guard exists to catch a future one.

BASELINE = "_baseline"

# Invariant 7: minimum 1T/300s AND 5T/120s. They disagreed on ordering more than once
# on 2026-08-20, so a single-fight-style answer is never printed alone.
DEFAULT_STYLES = ((1, 300), (5, 120))

# SE(median)/SE(mean) for a normally-distributed sample. simc reports `mean_stddev`
# (the standard error of the MEAN) and `mean_error` (its 95% CI half-width, i.e.
# mean_stddev × the confidence z). We rank on MEDIANS per invariant 5, so quoting
# simc's mean error on a median comparison would be exactly the mean/median mixing
# that cost a day chasing a phantom 2,486 DPS gap (failure #6). Scaling by this
# converts one to the other honestly instead.
SE_MEDIAN_FACTOR = 1.2533

VARIANT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.+/-]*$")


class CrossFrame(Exception):
    """A delta was requested between results from two different simc invocations."""


def parse_variant(arg: str, export: dict,
                  notes: list[str] | None = None) -> tuple[str, dict[str, str]]:
    """`'0pc = hands=@Pyrewalker's Gloves; legs=' → ("0pc", {...})`.

    A change is `<slot>=<item string>`, `<slot>=` to strip the slot bare, or
    `<slot>=@<Item Name>` to pull the export's own item string for a bag or vault
    candidate — which is the only form anyone should be typing by hand, since the
    export already carries correct bonus ids and the ilvl they imply.
    """
    name, sep, body = arg.partition("=")
    name = name.strip()
    if not sep:
        raise Unsupported(
            f"variant {arg!r} has no `=`.\n"
            "  form: '<Name>=<slot>=<item>[; <slot>=<item> ...]'\n"
            "  e.g.  '0pc=hands=@Pyrewalker\\'s Gloves; legs=@Wind Soarer\\'s Breeches'")
    if name == BASELINE:
        raise Unsupported(
            f"{BASELINE!r} is reserved — it is emitted automatically as the "
            "character's current gear, so the baseline is ranked in the same median "
            "table as everything else rather than read off a separate line "
            "(failure #6).")
    if not VARIANT_NAME.match(name):
        raise Unsupported(f"variant name {name!r} must match {VARIANT_NAME.pattern} "
                          "(it becomes a simc profileset name)")

    overrides: dict[str, str] = {}
    for change in body.split(";"):
        change = change.strip()
        if not change:
            continue
        key, sep2, value = change.partition("=")
        if not sep2:
            raise Unsupported(f"change {change!r} in variant {name!r} has no `=`")
        slot = _canon_slot(key.strip())
        if not slot:
            raise Unsupported(
                f"{key.strip()!r} in variant {name!r} is not a gear slot.\n"
                f"  slots: {', '.join(CANON_SLOTS)}")
        value = value.strip()
        if value.startswith("@"):
            value, row = resolve_candidate(export, slot, value[1:].strip())
            if row["slot"] != slot and notes is not None:
                notes.append(
                    f"{name}: {label(row)} is filed under `{row['slot']}` in the "
                    f"export and was placed in `{slot}` as asked. The addon files "
                    f"every {row['slot'].rstrip('12')} candidate under index 1 "
                    "regardless — but the index is not cosmetic: trinket1 wins "
                    "upstream's damage_trinket_priority tie-break, so the same item "
                    "in the other index can be a different answer.")
        overrides[slot] = value
    if not overrides:
        raise Unsupported(f"variant {name!r} changes nothing")
    return name, overrides


# The paired slots. The addon files EVERY ring under `finger1` and EVERY trinket under
# `trinket1` regardless of where it would go, so a candidate for one is a candidate for
# the other — but the two indices are NOT interchangeable in a result: upstream's
# `damage_trinket_priority` tie-breaks to trinket1, and on 2026-08-20 that alone left
# trinket2's rung waiting on `trinket.1.cooldown.remains` forever. So the family is
# searched, and the move is reported rather than made quietly.
SLOT_FAMILIES = [("trinket1", "trinket2"), ("finger1", "finger2")]


def slot_family(slot: str) -> tuple[str, ...]:
    for fam in SLOT_FAMILIES:
        if slot in fam:
            return fam
    return (slot,)


def candidates(export: dict, slot: str) -> list[dict]:
    """Everything the export offers for a slot: what is worn, plus bags, plus vault."""
    fam = slot_family(slot)
    worn = [export["equipped"][s] for s in fam if s in export["equipped"]]
    return worn + [r for r in export["bags"] + export["vault"] if r["slot"] in fam]


def resolve_candidate(export: dict, slot: str, token: str) -> tuple[str, dict]:
    """`@Pyrewalker's Gloves` → that row's item string, from the export itself.

    Matched by name, optionally disambiguated by ilvl (`@Name (282)`) — the same item
    genuinely appears twice at two upgrade levels in Encomplete's bags, and picking one
    silently would be picking a different answer.
    """
    want, _, want_ilvl = token.partition("(")
    want = want.strip().casefold()
    want_ilvl = want_ilvl.strip().rstrip(")").strip() or None

    rows = candidates(export, slot)
    hits = [r for r in rows
            if (r.get("name") or item_names().get(r.get("item_id") or -1) or ""
                ).casefold() == want
            and (want_ilvl is None or str(r.get("ilvl")) == want_ilvl)]
    if not hits:
        raise Unsupported(
            f"no {'/'.join(slot_family(slot))} candidate named {token!r} in this "
            "export.\n"
            + "".join(f"    {label(r)}\n" for r in rows)
            + "  (equipped + `### Gear from Bags` + `### Weekly Reward Choices`)")
    if len({r["item_string"] for r in hits}) > 1:
        raise Unsupported(
            f"{token!r} matches {len(hits)} different {slot} items — say which:\n"
            + "".join(f"    @{label(r)}\n" for r in hits))
    return hits[0]["item_string"], hits[0]


def profileset_lines(variants: dict[str, dict[str, str]]) -> list[str]:
    """The baseline first, as a real profileset (invariant 2, failure #6).

    simc needs at least one option per profileset, so the baseline re-asserts the
    character's own level: provably a no-op, and it puts the baseline in the SAME
    median-ranked table as every variant instead of on a separate mean line.
    """
    lines = ["", "# ── variants: one profileset each, one invocation, one frame ──",
             "profileset_metric=dps"]
    lines.append(f'profileset."{BASELINE}"+=level={{level}}')
    for name, overrides in variants.items():
        for slot, value in overrides.items():
            lines.append(f'profileset."{name}"+={slot}={value}')
    return lines


class Frame:
    """One simc invocation = one comparison frame. Results only ever leave here."""

    def __init__(self, ident: str, targets: int, time: int, data: dict,
                 profile: str, profile_file: pathlib.Path, built: dict):
        self.id = ident
        self.built = built
        self.targets = targets
        self.time = time
        self.data = data
        self.profile = profile
        self.profile_file = profile_file
        self.iterations = data["sim"]["options"]["iterations"]
        self.results: dict[str, dict] = {}
        for row in data["sim"].get("profilesets", {}).get("results", []):
            self.results[row["name"]] = {**row, "frame": ident}

    @property
    def style(self) -> str:
        return f"{self.targets}T/{self.time}s"

    @property
    def player(self) -> dict:
        """The base actor's FULL report — buffs, stats, procs. Profilesets carry only
        summary metrics (`save_output_data` in engine/sim/profileset.cpp handles just
        race/gear/stats/talents), so the firing gate reads the base from here and each
        variant gets its own short validation run instead."""
        return self.data["sim"]["players"][0]


def run_frame(export: dict, ref: dict, variants: dict, *, targets: int, time: int,
              iterations: int, tag: str, apl_override: list[str] | None = None) -> Frame:
    profile, built = build_profile(export, ref, apl_override=apl_override)
    profile += "\n".join(
        ln.replace("{level}", str(export.get("level") or 90))
        for ln in profileset_lines(variants)) + "\n"
    data, profile_file = run_simc(profile, {
        "iterations": iterations, "fight_style": "Patchwerk",
        "max_time": time, "desired_targets": targets,
    }, RESULTS, tag)
    frame = Frame(tag, targets, time, data, profile, profile_file, built)
    missing = [n for n in [BASELINE, *variants] if n not in frame.results]
    if missing:
        raise RuntimeError(
            f"simc did not return profileset(s) {', '.join(missing)} for {frame.style}"
            f" — see {profile_file.relative_to(ROOT)}")
    return frame


def frame_deltas(frame: Frame) -> list[dict]:
    """Median, Δ% ± error and a significance verdict — all from ONE frame.

    Ranked by median, baseline included, because it is a profileset like any other.
    """
    rows = []
    base = frame.results[BASELINE]
    for name, res in frame.results.items():
        if res["frame"] != frame.id:
            raise CrossFrame(
                f"result {name!r} came from frame {res['frame']!r}, not {frame.id!r}. "
                "Refusing to delta across simc invocations — that is failure #4 and it "
                "shipped a wrong vault recommendation on 2026-08-20.")
        se = SE_MEDIAN_FACTOR * res["mean_stddev"]
        se_base = SE_MEDIAN_FACTOR * base["mean_stddev"]
        # Independent runs, so the errors add in quadrature. The baseline's own error
        # is part of the comparison and dropping it understates every band.
        combined = 1.96 * (se * se + se_base * se_base) ** 0.5
        delta = res["median"] - base["median"]
        rows.append({
            "name": name, "median": res["median"], "iterations": res["iterations"],
            "delta": delta,
            "delta_pct": 100.0 * delta / base["median"],
            "err_pct": 100.0 * combined / base["median"],
            "verdict": ("baseline" if name == BASELINE else
                        "significant" if abs(delta) > combined else "NOISE"),
        })
    rows.sort(key=lambda r: -r["median"])
    # The baseline's own row carries delta 0 ± its band. That is not a wasted cell: it
    # is the frame's noise floor, i.e. the smallest difference this many iterations can
    # resolve at all. The table prints it as "this IS the baseline" rather than 0.00%,
    # because a 0.00% in a Δ column reads as a measured tie.
    return rows


# ══ The variant firing gate ══════════════════════════════════════════════════
#
# The base actor's firing gate is free — its full report is in the frame. A VARIANT's
# is not: profilesets report summary metrics only, so a swapped-in on-use trinket that
# never fires is exactly as invisible inside a profileset as Stormbound Emblem was
# inside a bare run. That is the trap this whole tool exists for, so each variant that
# introduces an item carrying a special effect gets its own short validation run.
# Those runs report NO DPS and are never deltaed against anything.

def introduces_effects(export: dict, overrides: dict[str, str]) -> bool:
    for slot, value in overrides.items():
        new_id = _item_id(value)
        old = export["equipped"].get(slot) or {}
        if new_id and new_id != old.get("item_id") and item_effects().get(new_id):
            return True
    return False


def variant_export(export: dict, overrides: dict[str, str]) -> dict:
    """The export as it would read with this variant worn — so the gate inspects the
    variant's items, not the baseline's."""
    equipped = dict(export["equipped"])
    for slot, value in overrides.items():
        if not value.strip():
            equipped.pop(slot, None)
            continue
        equipped[slot] = {"slot": slot, "item_string": value,
                          "name": None, "ilvl": None, "item_id": _item_id(value)}
    return {**export, "equipped": equipped}


def gate_variants(export: dict, ref: dict, variants: dict, *,
                  iterations: int, targets: int, time: int) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for name, overrides in variants.items():
        if not introduces_effects(export, overrides):
            continue
        sub = variant_export(export, overrides)
        profile, _ = build_profile(sub, ref)
        data, _ = run_simc(profile, {
            "iterations": iterations, "fight_style": "Patchwerk",
            "max_time": time, "desired_targets": targets,
        }, RESULTS, f"gate-{tokenize(name)}")
        out[name] = firing_gate(sub, ref, data)
    return out


# ══ Storage ══════════════════════════════════════════════════════════════════

def _rel(path: pathlib.Path) -> str:
    """Repo-relative when it can be, absolute otherwise. An export passed by path from
    outside the repo is a legitimate input (a doctored copy is how the ilvl-fidelity
    gate is proved to fire), and `relative_to` throws on one."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def export_path(export: dict) -> pathlib.Path:
    char = (export["character"] or "unknown").lower()
    date = export["exported"] or datetime.date.today().isoformat()
    return EXPORTS / f"{char}-{date}.simc"


def find_export(token: str) -> pathlib.Path:
    """A character name, or a path to an export. Newest export wins for a bare name."""
    candidate = pathlib.Path(token)
    if candidate.is_file():
        return candidate
    matches = sorted(EXPORTS.glob(f"{token.lower()}-*.simc"))
    if not matches:
        have = sorted({p.name.rsplit("-", 3)[0] for p in EXPORTS.glob("*.simc")})
        raise Unsupported(
            f"no stored export for {token!r} in {EXPORTS.relative_to(ROOT)}\n"
            f"  stored: {', '.join(have) or 'none'}\n"
            f"  run `wowkb.sim import <export.simc>` first (or paste via `-`).")
    return matches[-1]


# ══ Commands ═════════════════════════════════════════════════════════════════

def _build_drift(export: dict) -> str | None:
    """The client can be AHEAD of the KB — Encomplete's export read 12.1.0.69382 against
    a recorded 12.1.0.69214 — so this reports drift rather than assuming the KB is
    current."""
    try:
        text = (ROOT / "knowledge" / "_meta" / "game-version.md").read_text(
            encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"^build:\s*(\S+)", text, re.M)
    if not m or not export.get("client_build"):
        return None
    if m.group(1) == export["client_build"]:
        return None
    return (f"export client build {export['client_build']} ≠ game-version.md "
            f"{m.group(1)} — the client may be ahead of the KB")


def cmd_import(args) -> int:
    text = sys.stdin.read() if args.source == "-" else pathlib.Path(
        args.source).read_text(encoding="utf-8")
    export = parse_export(text)
    if not export["character"] or not export["class"]:
        print("error: this does not look like a /simc export — no `<class>=\"<name>\"` "
              "line found", file=sys.stderr)
        return 2

    dest = export_path(export)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not (dest.is_file() and dest.read_text(encoding="utf-8") == text):
        dest.write_text(text, encoding="utf-8")

    print(f"{export['character']} — {export['spec']} {export['class']} "
          f"{export.get('level') or '?'} {export.get('race') or ''} "
          f"({export.get('region') or '?'}/{export.get('server') or '?'})")
    print(f"  exported     : {export['exported'] or 'not stated'}")
    print(f"  client build : {export['client_build'] or 'not stated'}"
          f"  (TOC {export['toc'] or 'not stated'}, "
          f"addon {export['addon_version'] or 'not stated'})")
    drift = _build_drift(export)
    if drift:
        print(f"  ⚠ {drift}")
    print(f"  stored       : {dest.relative_to(ROOT)}  (verbatim)")
    print(f"  checksum     : {export['checksum'] or 'not stated'}")

    print(f"\nEquipped ({len(export['equipped'])} of {len(CANON_SLOTS)} slots)")
    for slot in CANON_SLOTS:
        entry = export["equipped"].get(slot)
        print(f"  {slot:<10} {label(entry) if entry else 'empty'}")

    for section, title in (("bags", "Gear from bags"),
                           ("vault", "Weekly reward choices")):
        rows = export[section]
        print(f"\n{title} ({len(rows)})")
        if not rows:
            print("  none in the export")
        by_slot: dict[str, list[dict]] = {}
        for row in rows:
            by_slot.setdefault(row["slot"], []).append(row)
        for slot in CANON_SLOTS:
            for row in by_slot.get(slot, []):
                print(f"  {slot:<10} {label(row)}")
        if section == "bags" and rows:
            print("  ⚠ the bag block is filtered ONLY by 'has an equippable inventory "
                  "type' (SimulationCraft/core.lua:GetBagItemStrings) — not by armor "
                  "class and not by class usability, so it carries items this character "
                  "cannot wear. `gear` must filter; `import` reports what the export "
                  "said.")

    print("\nAdditional character info")
    for key in ("catalyst_currencies", "upgrade_currencies", "slot_high_watermarks",
                "upgrade_achievements", "bonus_roll_currencies"):
        print(f"  {key:<22} {export[key] or 'not stated'}")
    marks = parse_watermarks(export)
    if marks:
        print("\n  Upgrade high watermarks (Enum.ItemRedundancySlot, not inventory "
              "slots)")
        print(f"    {'idx':>3}  {'slot':<20} {'character':>9} {'account':>8}")
        for row in marks:
            print(f"    {row['index']:>3}  {row['slot']:<20} "
                  f"{row['character']:>9} {row['account']:>8}"
                  + ("   ← one row for TWO worn items" if row["paired"] else ""))
        print("    ⚠ `Finger` and `Trinket` are ONE row each for two worn items, and a "
              "paired row is\n      NOT simply the highest ilvl ever worn there — see "
              "REDUNDANCY_PAIRED in sim.py.\n      The rule is unconfirmed; `crests` "
              "(Phase 4) must settle it before costing a paired slot.")

    if args.json:
        print(json.dumps(export, indent=2))
    return 0


def cmd_check(args) -> int:
    missing = simc_available()
    if missing:
        print(missing, file=sys.stderr)
        return 2

    path = find_export(args.character)
    export = parse_export(path.read_text(encoding="utf-8"))

    commit = simc_commit()
    stale = staleness(commit)
    live = live_patch_date()

    try:
        ref = resolve_reference(export["class"], export["spec"], args.hero,
                                args.apl_source)
    except Unsupported as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    profile, built = build_profile(export, ref)
    options = {
        "iterations": args.iterations,
        "fight_style": "Patchwerk",
        "max_time": args.time,
        "desired_targets": args.targets,
    }
    data, profile_file = run_simc(profile, options, RESULTS,
                                  f"check-{(export['character'] or 'x').lower()}")

    findings = firing_gate(export, ref, data)
    leaks = leak_gate(export, built, data)
    on_gcd = apl_hygiene(profile)
    drift = _build_drift(export)

    print(f"wowkb.sim check — {export['character']} "
          f"({export['spec']} {export['class']}, "
          f"{export.get('region') or '?'}/{export.get('server') or '?'})")
    print("\n  harness")
    print(f"    export        : {_rel(path)} ({export['exported']})")
    print(f"    reference APL : {_rel(ref['path'])}  [{ref['tier']}]")
    if ref.get("warn"):
        print(f"    ⚠ {ref['warn']}")
    print(f"    simc commit   : {commit['short'] if commit else 'unresolved'} "
          f"{commit['date'] if commit else ''}"
          + (f"  — postdates {live[0]} ({live[1]})" if commit and live and not stale
             else ""))
    print(f"    simc data     : client {simc_data_build() or 'not stated'}")
    print(f"    export client : {export['client_build'] or 'not stated'}")
    if drift:
        print(f"    ⚠ {drift}")
    print(f"    profile       : {profile_file.relative_to(ROOT)}")
    print(f"    slots         : {len(built['assigned'])} assigned, "
          f"{len(built['cleared'])} explicitly cleared "
          f"({', '.join(built['cleared']) or 'none'})")
    print(f"    run           : {args.targets}T / {args.time}s / "
          f"{data['sim']['options']['iterations']} iterations")

    print("\n  firing gate")
    if not findings:
        print("    ✅ every equipped special effect fired at or above half its "
              "expected rate")
    for f in findings:
        icon = "❌ FAIL" if f["level"] == "FAIL" else "⚠ WARN "
        print(f"    {icon}  {f['slot']}  {f['item']}")
        print(f"             → {f['effect']} (spell {f['spell_id']}, "
              f"{'on-use' if f['on_use'] else 'equip/proc'}"
              + (f", {f['cooldown']:.0f}s cooldown" if f["cooldown"] else "") + ")")
        print(f"             {f['why']}")
        print(f"             observed {f['observed']:.1f} uses; expected "
              + (f"~{f['expected']:.1f}" if f["expected"] else "not computable "
                 "(no cooldown on the effect spell)")
              + (f"; forced-probe {f['forced']:.1f}" if f.get("forced") is not None
                 else ""))

    print("\n  other gates")
    print_overrides(built, "    ")
    if leaks:
        print(f"    ❌ FAIL  reference-profile gear leaked into: {', '.join(leaks)}")
    else:
        print("    ✅ no reference-profile gear leaked — every worn slot was assigned "
              "by the builder")
    if on_gcd:
        print(f"    · NOTE   {len(on_gcd)} upstream `use_item` rung(s) without "
              f"{OFF_GCD} — these cost a GCD when they fire. Upstream's own fallback "
              "rungs; not a harness fault, and not counted in the verdict:")
        for action in on_gcd:
            print(f"             {action.split(',if=')[0]}")
    else:
        print(f"    ✅ every `use_item` in the APL carries {OFF_GCD}")
    if stale:
        days, patch, live_date = stale
        print(f"    ❌ STALE  simc checkout is {days} days older than {patch} "
              f"(live {live_date}) — do not report DPS from it")

    fails = [f for f in findings if f["level"] == "FAIL"]
    warns = [f for f in findings if f["level"] == "WARN"]
    verdict = "FAIL" if (fails or leaks) else ("WARN" if warns else "PASS")
    print(f"\n  VERDICT: {verdict} — {len(fails) + len(leaks)} failure(s), "
          f"{len(warns)} warning(s). No DPS reported: this command validates the "
          "harness only.")

    if stale:
        return 3
    return 1 if verdict == "FAIL" else 0



def _fmt_row(row: dict | None) -> tuple[str, str, str]:
    if row is None:
        return ("not simulated",) * 3
    if row["name"] == BASELINE:
        return (f"{row['median']:,.0f}", "—  (this IS the baseline)", "baseline")
    return (f"{row['median']:,.0f}",
            f"{row['delta_pct']:+.2f}% ± {row['err_pct']:.2f}%",
            row["verdict"])


def _table(frames: list[Frame], deltas: dict[str, list[dict]],
           brand: str = "") -> list[str]:
    """Markdown, ranked by the FIRST frame's median, baseline included.

    `brand` prefixes every line rather than sitting once above the table: a caveat
    above a table does not survive someone copying one row out of it, and a row lifted
    out of a branded table is how an unvalidated number gets cited as a result.
    """
    head = ["variant"]
    for f in frames:
        head += [f"{f.style} median", "Δ% ± err", "verdict"]
    rows = [head]
    for name in [r["name"] for r in deltas[frames[0].id]]:
        cells = [name]
        for f in frames:
            cells += list(_fmt_row(
                next((r for r in deltas[f.id] if r["name"] == name), None)))
        rows.append(cells)
    width = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]

    def line(cells, fill=" "):
        return brand + "| " + " | ".join(c.ljust(w, fill)
                                         for c, w in zip(cells, width)) + " |"

    return [line(rows[0]),
            brand + "|" + "|".join("-" * (w + 2) for w in width) + "|",
            *(line(r) for r in rows[1:])]


def _print_findings(findings: list[dict], indent: str) -> None:
    for f in findings:
        icon = "❌ FAIL" if f["level"] == "FAIL" else "⚠ WARN "
        print(f"{indent}{icon}  {f['slot']}  {f['item']}")
        print(f"{indent}         → {f['effect']} (spell {f['spell_id']}, "
              f"{'on-use' if f['on_use'] else 'equip/proc'}) — {f['why']}")
        print(f"{indent}         observed {f['observed']:.1f}; expected "
              + (f"~{f['expected']:.1f}" if f["expected"] else "not computable")
              + (f"; forced-probe {f['forced']:.1f}"
                 if f.get("forced") is not None else ""))


def cmd_compare(args) -> int:
    missing = simc_available()
    if missing:
        print(missing, file=sys.stderr)
        return 2

    path = find_export(args.character)
    export = parse_export(path.read_text(encoding="utf-8"))
    variants: dict[str, dict[str, str]] = {}
    notes: list[str] = []
    for spec in args.variants:
        name, overrides = parse_variant(spec, export, notes)
        if name in variants:
            raise Unsupported(f"variant {name!r} given twice")
        variants[name] = overrides

    ref = resolve_reference(export["class"], export["spec"], args.hero,
                            args.apl_source)
    apl_override = None
    if args.apl_override:
        apl_override = [ln.rstrip() for ln in pathlib.Path(args.apl_override)
                        .read_text(encoding="utf-8").splitlines()
                        if ln.strip() and not ln.strip().startswith("#")]
        if not all(ln.strip().startswith("actions") for ln in apl_override):
            print("error: --apl-override may contain only `actions...=` lines "
                  "(and comments)", file=sys.stderr)
            return 2

    styles = [(args.targets, args.time)] if args.targets else list(DEFAULT_STYLES)
    commit = simc_commit()
    stale = staleness(commit)

    char = (export["character"] or "x").lower()

    def frame_for(targets: int, time: int) -> Frame:
        return run_frame(export, ref, variants, targets=targets, time=time,
                         iterations=args.iterations, apl_override=apl_override,
                         tag=f"compare-{char}-{targets}t{time}s")

    frames: list[Frame] = [frame_for(*styles[0])]

    # ── gates, before any number is printed ─────────────────────────────────
    # The base actor's full report comes free with the first frame; the remaining
    # fight styles are only run once we know a table will actually be printed.
    base_findings = firing_gate(export, ref, frames[0].data)
    leaks = leak_gate(export, frames[0].built, frames[0].data)
    var_findings = gate_variants(export, ref, variants,
                                 iterations=args.gate_iterations,
                                 targets=frames[0].targets, time=frames[0].time)
    on_gcd = apl_hygiene(frames[0].profile)

    fails = [f for f in base_findings if f["level"] == "FAIL"]
    fails += [f for fs in var_findings.values() for f in fs if f["level"] == "FAIL"]
    warns = [f for f in base_findings if f["level"] == "WARN"]
    warns += [f for fs in var_findings.values() for f in fs if f["level"] == "WARN"]
    blocked = bool(fails or leaks)

    if not blocked or args.accept_failing_gate:
        frames += [frame_for(*style) for style in styles[1:]]

    print(f"wowkb.sim compare — {export['character']} "
          f"({export['spec']} {export['class']})")
    print("\n  harness")
    print(f"    export        : {_rel(path)} ({export['exported']})")
    print(f"    reference APL : {_rel(ref['path'])}  [{ref['tier']}]")
    if ref.get("warn"):
        print(f"    ⚠ {ref['warn']}")
    print(f"    simc commit   : {commit['short'] if commit else 'unresolved'} "
          f"{commit['date'] if commit else ''}")
    print(f"    simc data     : client {simc_data_build() or 'not stated'}")
    drift = _build_drift(export)
    if drift:
        print(f"    ⚠ {drift}")
    for frame in frames:
        print(f"    frame         : {frame.id}  {frame.style}, "
              f"{frame.iterations} iterations  → "
              f"{frame.profile_file.relative_to(ROOT)}")
    print(f"    variants      : {BASELINE} (current gear) + "
          f"{', '.join(variants) or 'none'}")
    for note in notes:
        print(f"    · {note}")
    if apl_override:
        print("    ⚠ UNVALIDATED HARNESS — the upstream priority list was replaced by "
              f"{args.apl_override}. Nothing here may be cited as a sim result.")

    print("\n  firing gate")
    if not base_findings:
        print(f"    ✅ {BASELINE}: every equipped special effect fired at or above "
              "half its expected rate")
    else:
        print(f"    {BASELINE} (current gear)")
        _print_findings(base_findings, "    ")
    for name, findings in var_findings.items():
        if findings:
            print(f"    {name}")
            _print_findings(findings, "    ")
        else:
            print(f"    ✅ {name}: every effect it introduces fired")
    ungated = [n for n in variants if n not in var_findings]
    if ungated:
        print(f"    · {', '.join(ungated)} introduce no item with a special effect — "
              "nothing to fire, no validation run needed")

    print("\n  other gates")
    print_overrides(built, "    ")
    if leaks:
        print(f"    ❌ FAIL  reference-profile gear leaked into: {', '.join(leaks)}")
    else:
        print("    ✅ no reference-profile gear leaked")
    if on_gcd:
        level = "⚠ WARN " if apl_override else "· NOTE "
        print(f"    {level} {len(on_gcd)} `use_item` rung(s) without {OFF_GCD}"
              + (" — these are OURS under --apl-override, and failure #2 cost −3.2%"
                 if apl_override else " — upstream's own fallback rungs, not counted"))
        for action in on_gcd:
            print(f"             {action.split(',if=')[0]}")
    if stale:
        days, patch, live_date = stale
        print(f"    ❌ STALE  simc checkout is {days} days older than {patch} "
              f"(live {live_date}) — do not report DPS from it")
        return 3

    # ── results ─────────────────────────────────────────────────────────────
    deltas = {f.id: frame_deltas(f) for f in frames}

    if blocked and not args.accept_failing_gate:
        print(f"\n  VERDICT: FAIL — {len(fails) + len(leaks)} failure(s), "
              f"{len(warns)} warning(s).")
        print("\n  ⛔ NO DPS PRINTED. A failing firing gate means the numbers measure "
              "an\n     effect that is not being used, which is precisely how the "
              "2026-08-20\n     session produced five confident wrong answers.")
        print("     Fix the gear/APL question the gate names, or re-run with\n"
              "     --accept-failing-gate '<why this delta survives the failure>' "
              "to\n     print the table branded with your reason.")
        return 1

    if blocked:
        print(f"\n  ⚠ GATE FAILED, ACCEPTED — {args.accept_failing_gate}")
    print(f"\n  Medians only. Δ is against {BASELINE} WITHIN each frame; the tool "
          "cannot\n  delta across invocations. ± is a 95% band on the median "
          f"(simc's mean\n  standard error × {SE_MEDIAN_FACTOR}, baseline and variant "
          "errors combined).\n")
    brand = ("⛔UNVALIDATED " if apl_override else "⚠ GATE-FAILED " if blocked else "")
    brand += override_brand(frames[0].built)
    for line in _table(frames, deltas, brand):
        print("  " + line)

    if len(frames) == 1:
        print(f"\n  ⚠ ONE fight style only ({frames[0].style}). 1T and 5T disagreed on "
              "ordering\n    more than once on 2026-08-20 — drop --targets to get both.")

    verdict = "FAIL" if blocked else ("WARN" if warns else "PASS")
    print(f"\n  VERDICT: {verdict} — {len(fails) + len(leaks)} failure(s), "
          f"{len(warns)} warning(s).")
    if args.json:
        print(json.dumps({"frames": [
            {"id": f.id, "style": f.style, "iterations": f.iterations,
             "rows": deltas[f.id]} for f in frames]}, indent=2))
    return 1 if blocked else 0


# ══ gear — local Top Gear, driven entirely by the export ═════════════════════
#
# Mostly a CALLER of `compare`'s machinery: `candidates()` already enumerates worn +
# bag + vault rows for a slot family, each becomes one profileset, and the same frame /
# firing-gate / median-delta path runs them. What is new here is the usability filter
# (the export is NOT pre-filtered) and the tier-set confound annotation.

def _source_tag(export: dict, row: dict) -> str:
    if any(row is r for r in export["bags"]):
        return "bags"
    if any(row is r for r in export["vault"]):
        return "vault"
    return "worn"


def variant_name(entry: dict, taken: set[str]) -> str:
    """A profileset name for a candidate: its item name, scrubbed to the characters a
    simc profileset name may carry, with the ilvl kept because the same item genuinely
    appears twice at two upgrade levels in one bag."""
    base = (entry.get("name") or item_names().get(entry.get("item_id") or -1)
            or f"id{entry.get('item_id')}")
    name = re.sub(r"[^A-Za-z0-9 _.+/-]", "", base).strip() or f"id{entry.get('item_id')}"
    if not name[0].isalnum():
        name = "x" + name
    if entry.get("ilvl"):
        name = f"{name} {entry['ilvl']}"
    if name in taken:  # two rows, same name and ilvl, different bonus ids
        name = f"{name} id{entry.get('item_id')}"
    n, i = name, 2
    while name in taken:
        name, i = f"{n} v{i}", i + 1
    taken.add(name)
    return name


def gear_variants(export: dict, slot: str) -> dict:
    """Every candidate for `slot` the character can actually wear, as named variants.

    Excluded rows are RETURNED, not dropped: a silent filter is indistinguishable from
    a filter with a bug, and this one already reported every bag row unwearable once.
    """
    cls = export["class"]
    worn = export["equipped"].get(slot)
    fam = slot_family(slot)
    sibling = {s: export["equipped"][s] for s in fam
               if s != slot and s in export["equipped"]}

    variants: dict[str, dict[str, str]] = {}
    rows: dict[str, dict] = {}
    excluded: list[tuple[dict, str]] = []
    skipped: list[tuple[dict, str]] = []
    taken: set[str] = set()
    seen: set[str] = set()

    for row in candidates(export, slot):
        if worn and row["item_string"] == worn["item_string"]:
            continue  # this IS the baseline; it is already in the table
        if row["item_string"] in seen:
            continue
        seen.add(row["item_string"])
        # An item already worn in the OTHER index of the family: equipping it here too
        # would sim two copies of an item the character owns one of.
        other = next((s for s, e in sibling.items()
                      if e["item_string"] == row["item_string"]), None)
        if other:
            skipped.append((row, f"already worn in {other}"))
            continue
        reason = wearable(row.get("item_id"), cls, slot)
        if reason:
            excluded.append((row, reason))
            continue
        name = variant_name(row, taken)
        variants[name] = {slot: row["item_string"]}
        rows[name] = row

    return {"variants": variants, "rows": rows,
            "excluded": excluded, "skipped": skipped}


def _exclusion_summary(excluded: list[tuple[dict, str]]) -> str:
    tally: dict[str, int] = {}
    for _, reason in excluded:
        tally[reason] = tally.get(reason, 0) + 1
    return ", ".join(f"{n} {reason}" for reason, n in sorted(tally.items()))


def _gear_slot(args, export: dict, ref: dict, slot: str, styles: list,
               commit, char: str) -> tuple[int, bool]:
    """(exit code, did it print a ranking) for one slot."""
    plan = gear_variants(export, slot)
    variants, rows = plan["variants"], plan["rows"]
    worn = export["equipped"].get(slot)

    print(f"\n{'─' * 76}\n  {slot}   baseline: "
          f"{label(worn) if worn else 'nothing worn'}")

    for row, reason in plan["skipped"]:
        print(f"    · {label(row)} — {reason}; not offered as a swap")
    # Printed even at zero: silence here is indistinguishable from "the filter never
    # ran", and this filter has already been wrong once in the other direction.
    if plan["excluded"]:
        print(f"    · {len(plan['excluded'])} candidate(s) excluded "
              f"({_exclusion_summary(plan['excluded'])}):")
        for row, reason in plan["excluded"]:
            print(f"        {label(row)} — {reason}")
    else:
        print("    · 0 candidate(s) excluded — every export row for this slot is one "
              "this character can wear")
    if not variants:
        print("    nothing to rank: no wearable alternative in bags or the vault.")
        return 0, False

    weapons = slot in WEAPON_SLOTS
    gated = [n for n, ov in variants.items() if introduces_effects(export, ov)]
    print(f"    {len(variants)} candidate(s) "
          f"({', '.join(sorted({_source_tag(export, r) for r in rows.values()}))})"
          f" → {len(styles)} comparison frame(s) + {len(gated)} validation run(s)")

    frames: list[Frame] = []

    def frame_for(targets: int, time: int) -> Frame:
        return run_frame(export, ref, variants, targets=targets, time=time,
                         iterations=args.iterations,
                         tag=f"gear-{char}-{slot}-{targets}t{time}s")

    frames.append(frame_for(*styles[0]))
    base_findings = firing_gate(export, ref, frames[0].data)
    leaks = leak_gate(export, frames[0].built, frames[0].data)
    var_findings = gate_variants(export, ref, variants,
                                 iterations=args.gate_iterations,
                                 targets=frames[0].targets, time=frames[0].time)

    fails = [f for f in base_findings if f["level"] == "FAIL"]
    fails += [f for fs in var_findings.values() for f in fs if f["level"] == "FAIL"]
    warns = [f for f in base_findings if f["level"] == "WARN"]
    warns += [f for fs in var_findings.values() for f in fs if f["level"] == "WARN"]
    blocked = bool(fails or leaks)

    if not blocked or args.accept_failing_gate:
        frames += [frame_for(*style) for style in styles[1:]]

    print("\n    firing gate")
    if not base_findings:
        print(f"      ✅ {BASELINE}: every equipped special effect fired")
    else:
        print(f"      {BASELINE} (current gear)")
        _print_findings(base_findings, "      ")
    for name, findings in var_findings.items():
        if findings:
            print(f"      {name}")
            _print_findings(findings, "      ")
    clean = [n for n in gated if not var_findings.get(n)]
    if clean:
        print(f"      ✅ {', '.join(clean)}: every effect introduced fired")
    ungated = [n for n in variants if n not in gated]
    if ungated:
        print(f"      · {len(ungated)} candidate(s) carry no special effect — "
              "nothing to fire, no validation run needed")
    if leaks:
        print(f"      ❌ FAIL  reference-profile gear leaked into: {', '.join(leaks)}")

    if blocked and not args.accept_failing_gate:
        print(f"\n    ⛔ NO DPS PRINTED — {len(fails) + len(leaks)} failing gate(s). "
              "The ranking would\n       measure an effect that is not being used. "
              "Re-run with\n       --accept-failing-gate '<why this ranking survives "
              "the failure>'.")
        return 1

    if blocked:
        print(f"\n    ⚠ GATE FAILED, ACCEPTED — {args.accept_failing_gate}")

    deltas = {f.id: frame_deltas(f) for f in frames}
    brand = ("⚠ GATE-FAILED " if blocked else "") + override_brand(frames[0].built)
    if weapons:
        brand += "⚠ NOT-USABILITY-CHECKED "
        print("\n    ⚠ WEAPON SLOT — ranked but NOT usability-checked. simc carries no "
              "weapon\n      usability data (is_match_slot excludes weapon slots and "
              "class_mask is never\n      read for equip validation), so a weapon this "
              "character cannot equip sims\n      fine and yields a plausible wrong "
              "number. Confirm in game before acting.")
    print()
    for line in _table(frames, deltas, brand):
        print("    " + line)

    notes = []
    for name, overrides in variants.items():
        row = rows[name]
        bits = []
        if row["slot"] != slot:
            bits.append(f"filed under `{row['slot']}` in the export, placed in `{slot}`"
                        " — the index is not cosmetic (damage_trinket_priority "
                        "tie-breaks to trinket1)")
        note = tier_note(export, overrides)
        if note:
            bits.append(note)
        if bits:
            notes.append(f"      {name}: " + "; ".join(bits))
    if notes:
        print("\n    annotations")
        print("\n".join(notes))

    if len(frames) == 1:
        print(f"\n    ⚠ ONE fight style only ({frames[0].style}) — 1T and 5T disagreed "
              "on ordering\n      more than once on 2026-08-20.")
    print(f"\n    {slot}: {len(fails) + len(leaks)} failure(s), {len(warns)} warning(s)")
    return (1 if blocked else 0), True


def cmd_gear(args) -> int:
    missing = simc_available()
    if missing:
        print(missing, file=sys.stderr)
        return 2

    path = find_export(args.character)
    export = parse_export(path.read_text(encoding="utf-8"))

    if args.all_slots == bool(args.slot):
        print("error: pass exactly one of --slot <slot> or --all-slots", file=sys.stderr)
        return 2

    if args.slot:
        slot = _canon_slot(args.slot.strip())
        if not slot:
            print(f"error: {args.slot!r} is not a gear slot.\n"
                  f"  slots: {', '.join(CANON_SLOTS)}", file=sys.stderr)
            return 2
        slots = [slot]
    else:
        slots = [s for s in CANON_SLOTS if s not in COSMETIC_SLOTS
                 and gear_variants(export, s)["variants"]]

    ref = resolve_reference(export["class"], export["spec"], args.hero,
                            args.apl_source)
    commit = simc_commit()
    stale = staleness(commit)
    styles = [(args.targets, args.time)] if args.targets else list(DEFAULT_STYLES)
    char = (export["character"] or "x").lower()

    print(f"wowkb.sim gear — {export['character']} "
          f"({export['spec']} {export['class']})")
    print("\n  harness")
    print(f"    export        : {_rel(path)} ({export['exported']})")
    print(f"    reference APL : {_rel(ref['path'])}  [{ref['tier']}]")
    if ref.get("warn"):
        print(f"    ⚠ {ref['warn']}")
    print(f"    simc commit   : {commit['short'] if commit else 'unresolved'} "
          f"{commit['date'] if commit else ''}")
    print(f"    simc data     : client {simc_data_build() or 'not stated'}")
    drift = _build_drift(export)
    if drift:
        print(f"    ⚠ {drift}")

    if stale:
        days, patch, live_date = stale
        print(f"    ❌ STALE  simc checkout is {days} days older than {patch} "
              f"(live {live_date}) — do not report DPS from it")
        return 3

    # The cost is real and worth stating before it is spent: every candidate that
    # introduces an effect-bearing item costs its OWN validation run, because a
    # profileset carries no buff or action counts (engine/sim/profileset.cpp:1043).
    total_v = total_g = 0
    for slot in slots:
        plan = gear_variants(export, slot)
        total_v += len(plan["variants"])
        total_g += sum(1 for ov in plan["variants"].values()
                       if introduces_effects(export, ov))
    print(f"\n  plan: {len(slots)} slot(s), {total_v} candidate(s) → "
          f"{len(slots) * len(styles)} comparison frame(s) at {args.iterations} "
          f"iterations\n        + {total_g} firing-gate validation run(s) at "
          f"{args.gate_iterations} iterations (no DPS read from these)")

    rc = 0
    ranked = False
    for slot in slots:
        slot_rc, printed = _gear_slot(args, export, ref, slot, styles, commit, char)
        rc = slot_rc or rc
        ranked = ranked or printed

    print(f"\n{'─' * 76}")
    if not ranked:
        # No table was printed, so the reading notes below would be explaining a
        # ranking that does not exist.
        return rc
    print(f"  Medians only. Δ is against {BASELINE} (current gear) WITHIN each frame; "
          "the tool\n  cannot delta across invocations. ± is a 95% band on the median "
          f"(simc's mean\n  standard error × {SE_MEDIAN_FACTOR}, baseline and variant "
          "errors combined).")
    print("  Candidates come from the export's own equipped/bag/vault rows — this "
          "answers\n  \"which of THESE, for THIS character\", never \"best in the "
          "game\".")
    return rc



# ══ Upgrade tracks, crests and the rank ladder (Phase 4) ═════════════════════
#
# simc models NO part of this: there is no track enum, no step field and no crest data
# anywhere in engine/. A rank is expressed to simc the only way it can be — by computing
# the target ilvl here and appending `,ilevel=<target>` to the export's own item line.
# That is upstream's own pattern (profiles/MID1/MID1_Shaman_Enhancement.simc:154) and
# `ilevel` WINS over bonus-id resolution (item.cpp:529-551 prefers `item_level` over
# `data.level`), so sockets, item effects and stat mods from the bonus ids all survive.
#
# ⚠ A profileset line REPLACES the slot string wholesale (opt_string_t::do_parse assigns,
# option.cpp:188-196) — there is no `hands+=ilevel=282` shorthand — so every rank
# restates the FULL item line plus the new `ilevel=`.

TRACK_STEPS = 6

# knowledge/endgame/dawncrests.md:53-64. BOTH endpoint columns are Tier-1: the 1/6
# values are verbatim from the Lairs reward table, the 6/6 ceilings from the DB2
# currency descriptions. The five intermediate steps are NOT: the KB records them as
# "~3 ilvl each and not individually confirmed" (dawncrests.md:80), so they are
# interpolated here and every interpolated row is branded `~interp`.
#
# ⚠ Interpolation is provably approximate, and we know by how much. Season 1's Champion
# ladder is recorded exactly (dawncrests.md: 246 → 250 → 253 → 256 → 259 → 263); linear
# interpolation of 246..263 gives 246/249/253/256/260/263 — off by one at two steps.
# That is the error bar on every `~interp` number, and it is why the crest ORDER, not
# the ilvl, is what this command asks you to trust.
TRACKS = {
    "Adventurer": (266, 282),
    "Veteran": (279, 295),
    "Champion": (292, 308),
    "Hero": (305, 321),
    "Myth": (318, 334),
}


def track_ilvl(track: str, step: int, cap: int = TRACK_STEPS) -> tuple[int, bool]:
    """(target ilvl, was it interpolated) for `<track> <step>/<cap>`."""
    base, ceiling = TRACKS[track]
    if step <= 1:
        return base, False
    if step >= cap:
        return ceiling, False
    return round(base + (ceiling - base) * (step - 1) / (cap - 1)), True


# `Simulationcraft.upgradeCurrencies` (Interface/AddOns/Simulationcraft/extras.lua:332-352)
# — the addon's OWN id→name map, i.e. the authority on the ids it writes into the export.
# Transcribed, not derived; same treatment as MATCHING_ARMOR_TYPE.
CREST_CURRENCIES = {
    3442: "Adventurer", 3443: "Veteran", 3444: "Champion",
    3445: "Hero", 3446: "Myth",
}
# `Simulationcraft.upgradeItems` (extras.lua:395-410) — the `i:<id>:<n>` half of the
# same line. simc's own item table does NOT carry these (all three of Encomplete's read
# None through `item_names()`), so the addon's map is the only local name source.
# 232875 is not in the addon's list either; it is the KB's (CLAUDE.md, the Syndicator
# item-count note), and it is Season 1 — a Spark of Radiance buys nothing in S2.
UPGRADE_ITEMS = {
    268552: "Ascendant Voidcore",
    274476: "Spark of Tides",
    251994: "Runed Starlight Matrix",
    232875: "Spark of Radiance (Season 1)",
}

# Season 1. Present in an export ⇒ that export predates the season flip, and costing S2
# ranks from it would read every balance as zero — which is exactly how goalboard.py
# went silently wrong. A WARN, not a guess.
LEGACY_CREST_CURRENCIES = {
    3383: "Adventurer Dawncrest", 3341: "Veteran Dawncrest", 3343: "Champion Dawncrest",
    3345: "Hero Dawncrest", 3347: "Myth Dawncrest",
}

# `Simulationcraft.upgradeAchievements` (extras.lua:438-447) ∩ dawncrests.md:195-205.
# The addon writes only COMPLETED ones (core.lua:GetItemUpgradeAchievements), so an id's
# ABSENCE is meaningful: it is "not earned", not "unknown".
MIST_ACHIEVEMENTS = {
    62410: "Adventurer", 62411: "Veteran", 62412: "Champion",
    62414: "Hero", 62416: "Myth",
}
DAWN_ACHIEVEMENTS = {  # Season 1 — grants NOTHING against Mistcrests (dawncrests.md:191)
    61809: "Adventurer", 42767: "Veteran", 42768: "Champion",
    42769: "Hero", 42770: "Myth",
}

# dawncrests.md:84-89 — Tier-3 ONLY (ConquestCapped / Icy Veins / Method 2026-08); the
# Tier-1 notes state no cost at all, and dawncrests.md:301 still carries an open TODO
# asking whether it is really flat 20 in S2 and whether the discount halves it.
#
# ⚠ This is why every crest-denominated number below is branded and the rank ORDER is
# not: because the cost is UNIFORM across ranks, ranking by "DPS per crest" is
# arithmetically identical to ranking by "DPS per rank". The constant moves the COUNT
# you can afford and nothing else. If it is wrong, the shortlist is still right.
CREST_COST_PER_RANK = 20
CREST_COST_DISCOUNTED = 10


def parse_upgrade_currencies(export: dict) -> list[dict]:
    """`c:3442:186/c:3444:140/i:268552:2` → rows. Both kinds are kept: the `i:` entries
    are upgrade ITEMS (Ascendant Voidcore, Sparks) and belong in the balance readout
    even though nothing here costs a rank in them."""
    raw = export.get("upgrade_currencies")
    if not raw:
        return []
    rows = []
    for chunk in raw.split("/"):
        parts = chunk.split(":")
        if len(parts) != 3:
            continue
        kind, ident, count = parts[0], _int(parts[1]), _int(parts[2])
        if ident is None or count is None:
            continue
        track = CREST_CURRENCIES.get(ident) if kind == "c" else None
        legacy = LEGACY_CREST_CURRENCIES.get(ident) if kind == "c" else None
        name = (f"{track} Mistcrest" if track else legacy
                or (UPGRADE_ITEMS.get(ident) or item_names().get(ident)
                    if kind == "i" else None)
                or f"{'currency' if kind == 'c' else 'item'} {ident}")
        rows.append({"kind": kind, "id": ident, "count": count,
                     "name": name, "track": track, "legacy": bool(legacy)})
    return rows


def parse_upgrade_achievements(export: dict) -> list[int]:
    raw = export.get("upgrade_achievements")
    if not raw:
        return []
    return [i for i in (_int(t) for t in raw.split("/")) if i is not None]


def crest_balances(export: dict) -> dict[str, int]:
    return {r["track"]: r["count"]
            for r in parse_upgrade_currencies(export) if r["track"]}


def discount_state(export: dict) -> dict[str, dict]:
    """Per track: is the 50% warband discount earned, and by which achievement.

    ⚠ Two things the export genuinely cannot tell us, both stated rather than assumed:
    the "…of the Mist" discount is warband-wide but **the earner still pays full price**
    (dawncrests.md), and the achievement list is account-wide — so a completed row does
    not say whether THIS character is the earner. Cost is therefore quoted at full price
    with the discounted figure shown beside it, never silently halved.
    """
    earned = set(parse_upgrade_achievements(export))
    out = {}
    for track in TRACKS:
        mist = next((i for i, t in MIST_ACHIEVEMENTS.items() if t == track), None)
        dawn = next((i for i, t in DAWN_ACHIEVEMENTS.items() if t == track), None)
        out[track] = {
            "earned": mist in earned,
            "mist_id": mist,
            "s1_only": dawn in earned and mist not in earned,
        }
    return out


# ── Where a slot's track comes from ──────────────────────────────────────────
#
# ⚠ The ONE documented exception to "the export is the single input". The `/simc` paste
# carries an item's ilvl but not its track or step, and the track CANNOT be inferred from
# the ilvl because the bands overlap: 295 is Veteran 6/6 or Champion 2/6, 305 is Champion
# 6/6 or Hero 1/6. So track/step comes from `charstate.load()` — the PlannerState dump's
# tooltip read (schema>=8), which is the only reliable source (the Blizzard API drops the
# track outright on crafted gear). A slot neither source resolves is printed
# UNRESOLVED TRACK and costed at nothing; it is never guessed from its band.

# The dump keys equipment by its own slot names; three differ from simc's.
DUMP_SLOT_ALIASES = {"shoulder": "shoulders", "wrist": "wrists",
                     "mainhand": "main_hand", "offhand": "off_hand"}


def item_tracks(character: str) -> dict:
    """{slot: {track, level, cap}} plus the dump's own age, or an `error` key."""
    try:
        from wowkb import charstate  # deferred: charstate reaches the network + disk
        state = charstate.load(character, enrich=True, syndicator=False)
    except Exception as exc:  # noqa: BLE001 — a missing dump is a reported gate, not a crash
        return {"tracks": {}, "error": str(exc)}
    if not state:
        return {"tracks": {}, "error": "no PlannerState dump and no API enrichment"}
    tracks = {}
    for slot, row in (state.get("track_by_slot") or {}).items():
        canon = _canon_slot(DUMP_SLOT_ALIASES.get(slot, slot))
        if canon:
            tracks[canon] = row
    updated = state.get("updated")
    return {"tracks": tracks, "updated": updated,
            "sources": state.get("_sources") or {},
            "date": (datetime.date.fromtimestamp(updated).isoformat()
                     if isinstance(updated, (int, float)) else None)}


# ── The free-by-watermark rule ───────────────────────────────────────────────
#
# dawncrests.md:215-232, confirmed in-game 2026-08-19: on the SAME character a slot
# re-upgrades any item up to that slot's high watermark for FREE. It does not cross to
# alts. Still unmeasured: whether the free ride caps at the watermark or at the item's
# own track ceiling, and whether it crosses tracks within a slot.

# `Enum.InventoryType` values we need to route a weapon to its redundancy row. The
# redundancy enum splits weapons by HAND COUNT, not by main/off — which is why the
# export reads OnehandWeapon 246 and OnehandWeaponSecond 62 for the same character.
INVTYPE_WEAPON, INVTYPE_SHIELD = 13, 14
INVTYPE_2HWEAPON, INVTYPE_WEAPONMAINHAND = 17, 21
INVTYPE_WEAPONOFFHAND, INVTYPE_HOLDABLE = 22, 23

CANON_TO_REDUNDANCY = {
    "head": "Head", "neck": "Neck", "shoulders": "Shoulder", "chest": "Chest",
    "waist": "Waist", "legs": "Legs", "feet": "Feet", "wrists": "Wrist",
    "hands": "Hand", "finger1": "Finger", "finger2": "Finger",
    "trinket1": "Trinket", "trinket2": "Trinket", "back": "Cloak",
}


def redundancy_slot(item_id: int | None, slot: str) -> str | None:
    """The `Enum.ItemRedundancySlot` name a worn item's watermark lives under."""
    fixed = CANON_TO_REDUNDANCY.get(slot)
    if fixed:
        return fixed
    if slot not in WEAPON_SLOTS:
        return None
    meta = item_meta().get(item_id or -1)
    inv = meta and meta.get("inventory_type")
    if inv == INVTYPE_2HWEAPON:
        return "Twohand"
    if inv == INVTYPE_WEAPONMAINHAND:
        return "MainhandWeapon"
    if inv in (INVTYPE_SHIELD, INVTYPE_HOLDABLE):
        return "Offhand"
    if inv == INVTYPE_WEAPONOFFHAND:
        return "OnehandWeaponSecond"
    if inv == INVTYPE_WEAPON:
        return "OnehandWeaponSecond" if slot == "off_hand" else "OnehandWeapon"
    return None


def watermark_for(export: dict, slot: str) -> dict | None:
    """The watermark row governing `slot`, or None when nothing maps to it."""
    entry = export["equipped"].get(slot)
    name = redundancy_slot((entry or {}).get("item_id"), slot)
    if not name:
        return None
    return next((r for r in parse_watermarks(export) if r["slot"] == name), None)


def upgrade_ranks(export: dict, tracks: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    """(ranks, unresolved) — every remaining rank of every equipped, tracked item.

    A rank is one step. Ranks within a slot are ordered and cumulative: 6/6 cannot be
    bought without 5/6, which is what makes the allocator's marginal-delta greedy the
    correct one rather than a plain sort.
    """
    ranks: list[dict] = []
    unresolved: list[dict] = []
    for slot in CANON_SLOTS:
        entry = export["equipped"].get(slot)
        if not entry or slot in COSMETIC_SLOTS:
            continue
        row = tracks.get(slot)
        track = (row or {}).get("track")
        if not row or track not in TRACKS:
            unresolved.append({"slot": slot, "entry": entry,
                               "why": ("no track from the dump or the API"
                                       if not row else
                                       f"track {track!r} is not one of the five S2 tracks")})
            continue
        level, cap = int(row.get("level") or 0), int(row.get("cap") or TRACK_STEPS)
        mark = watermark_for(export, slot)
        # The track model says this item should be sitting at this ilvl right now. When
        # it does not, the interpolation is wrong for that step and every target ilvl
        # derived from it is suspect — so it is surfaced, not silently used.
        here, _ = track_ilvl(track, level, cap)
        model_gap = (entry.get("ilvl") is not None and here != entry["ilvl"])
        for step in range(level + 1, cap + 1):
            ilvl, interp = track_ilvl(track, step, cap)
            free = bool(mark and mark["character"] is not None
                        and ilvl <= mark["character"])
            ranks.append({
                "slot": slot, "entry": entry, "track": track, "step": step, "cap": cap,
                "ilvl": ilvl, "interpolated": interp, "free": free,
                "watermark": mark, "from_step": level, "from_ilvl": entry.get("ilvl"),
                "model_gap": model_gap, "model_ilvl": here,
                "nonstandard_cap": cap != TRACK_STEPS,
            })
    return ranks, unresolved


def rank_name(rank: dict) -> str:
    """A profileset name. `/` is inside VARIANT_NAME's charset, so the step reads as it
    does in game."""
    return f"{rank['slot']} {rank['track']} {rank['step']}/{rank['cap']} {rank['ilvl']}"


def rank_variants(ranks: list[dict]) -> dict[str, dict[str, str]]:
    return {rank_name(r): {r["slot"]: f"{r['entry']['item_string']},ilevel={r['ilvl']}"}
            for r in ranks}


def ilvl_fidelity_gate(export: dict, player: dict) -> list[dict]:
    """simc's RESOLVED ilvl per slot must equal the export's stated ilvl.

    Verified passing on all 15 of Encomplete's slots on 2026-08-20, which is the point:
    the whole rank ladder is "the same item, +N ilvl", so if the baseline does not
    resolve to the ilvl the character actually wears, every delta measures a different
    starting point than the one being planned from. A future data or bonus-id regression
    is what this catches.
    """
    gear = player.get("gear") or {}
    out = []
    for slot, entry in export["equipped"].items():
        stated = entry.get("ilvl")
        if stated is None or slot in COSMETIC_SLOTS:
            continue
        resolved = (gear.get(slot) or {}).get("ilevel")
        if resolved is None:
            continue
        if int(resolved) != int(stated):
            out.append({"slot": slot, "item": label(entry),
                        "stated": int(stated), "resolved": int(resolved)})
    return out


def allocate(ranks: list[dict], deltas: dict[str, dict],
             budgets: dict[str, int]) -> list[dict]:
    """Greedy over MARGINAL delta, honouring two constraints.

    1. **Ranks stack.** Rank k's Δ is measured against current gear, so it already
       includes k-1. The value of buying k once k-1 is bought is Δ(k) − Δ(k-1) — sorting
       on the raw Δ would buy the top of a ladder while pretending the rungs below were
       free.
    2. **Each crest tier upgrades ITS OWN TRACK ONLY** (dawncrests.md:47), so `budgets`
       is per track and a rank can only be bought out of its own track's pool.

    ⚠ Constraint 2 was missing on 2026-08-20 and it produced a confidently wrong plan on
    the first real character it met: the budget was summed across all five tracks (16
    ranks) and then spent entirely on Champion and Hero ranks, for a character holding
    **zero** Champion Mistcrests and 8 Hero. Every row was individually true and the
    recommendation was unbuyable. Pooling budgets across tracks is not a rounding error,
    it is a different game.
    """
    by_slot: dict[str, list[dict]] = {}
    for r in ranks:
        by_slot.setdefault(r["slot"], []).append(r)
    for rows in by_slot.values():
        rows.sort(key=lambda r: r["step"])

    taken: list[dict] = []
    cursor = {slot: 0 for slot in by_slot}
    prev: dict[str, float] = {slot: 0.0 for slot in by_slot}
    left = dict(budgets)
    while any(v > 0 for v in left.values()):
        best, best_gain = None, 0.0
        for slot, rows in by_slot.items():
            i = cursor[slot]
            if i >= len(rows):
                continue
            row = rows[i]
            # The rank's OWN track must still have crests. A slot whose next rung is
            # unaffordable is skipped, not deferred: the rungs above it are unreachable
            # too, since ranks stack.
            if left.get(row["track"], 0) <= 0:
                continue
            d = deltas.get(rank_name(row), {}).get("delta_pct")
            if d is None:
                continue
            gain = d - prev[slot]
            if best is None or gain > best_gain:
                best, best_gain = (slot, row, gain), gain
        if best is None or best_gain <= 0:
            break
        slot, row, gain = best
        taken.append({**row, "marginal_pct": gain})
        cursor[slot] += 1
        prev[slot] = deltas[rank_name(row)]["delta_pct"]
        left[row["track"]] -= 1
    return taken


def _crest_plan_lines(export: dict, tracks: dict, ranks: list[dict],
                      unresolved: list[dict]) -> None:
    """The computed, DPS-free half of the answer: what is on a track, what is free, and
    what the balance buys. All of it is printable before a single iteration is run."""
    print("\n  upgrade currencies (from the export's own upgrade_currencies line)")
    rows = parse_upgrade_currencies(export)
    if not rows:
        print("    none stated — this export carries no upgrade_currencies line")
    for r in rows:
        tag = ("  ⚠ SEASON DRIFT — a Season 1 Dawncrest; Mistcrests are what S2 ranks "
               "cost" if r["legacy"] else "")
        print(f"    {r['count']:>5} × {r['name']}  ({r['kind']}:{r['id']}){tag}")

    print("\n  the 50% warband discount (\"…of the Mist\", derived — never assumed)")
    disc = discount_state(export)
    earned = [t for t, d in disc.items() if d["earned"]]
    s1only = [t for t, d in disc.items() if d["s1_only"]]
    if earned:
        for t in earned:
            print(f"    ✅ {t} of the Mist ({disc[t]['mist_id']}) earned — 10 per rank "
                  "warband-wide")
        print("    ⚠ the EARNER still pays full price, and the achievement list is "
              "account-wide,\n      so the export cannot say whether THIS character "
              "earned it. Costs below are\n      quoted at full price with the "
              "discounted figure beside them.")
    else:
        print("    ✗ none of the five \"…of the Mist\" achievements is completed — "
              "no discount")
    if s1only:
        print(f"    · \"…of the Dawn\" earned for {', '.join(s1only)}, which grants "
              "NOTHING against\n      Mistcrests: the discount is per crest currency "
              "and Dawncrests are gone (dawncrests.md:191)")


def cmd_crests(args) -> int:
    missing = simc_available()
    if missing:
        print(missing, file=sys.stderr)
        return 2

    if args.all_tracks == bool(args.track):
        print("error: pass exactly one of --track <Track> or --all-tracks",
              file=sys.stderr)
        return 2
    if args.track:
        want = next((t for t in TRACKS if t.lower() == args.track.strip().lower()), None)
        if not want:
            print(f"error: {args.track!r} is not an upgrade track.\n"
                  f"  tracks: {', '.join(TRACKS)}", file=sys.stderr)
            return 2
        wanted = {want}
    else:
        wanted = set(TRACKS)

    path = find_export(args.character)
    export = parse_export(path.read_text(encoding="utf-8"))
    ref = resolve_reference(export["class"], export["spec"], args.hero, args.apl_source)
    commit = simc_commit()
    stale = staleness(commit)
    styles = [(args.targets, args.time)] if args.targets else list(DEFAULT_STYLES)
    char = (export["character"] or "x").lower()

    print(f"wowkb.sim crests — {export['character']} "
          f"({export['spec']} {export['class']})")
    print("\n  harness")
    print(f"    export        : {_rel(path)} ({export['exported']})")
    print(f"    reference APL : {_rel(ref['path'])}  [{ref['tier']}]")
    if ref.get("warn"):
        print(f"    ⚠ {ref['warn']}")
    print(f"    simc commit   : {commit['short'] if commit else 'unresolved'} "
          f"{commit['date'] if commit else ''}")
    print(f"    simc data     : client {simc_data_build() or 'not stated'}")
    drift = _build_drift(export)
    if drift:
        print(f"    ⚠ {drift}")

    # ⚠ The one documented departure from "the export is the single input" — an item's
    # track and step exist nowhere in the paste and cannot be inferred from its ilvl.
    src = item_tracks(export["character"] or args.character)
    print(f"    track source  : PlannerState /ps dump"
          f"{' + Blizzard API' if (src.get('sources') or {}).get('blizzard_api') else ''}"
          f" — the export carries no track")
    if src.get("error"):
        print(f"    ❌ FAIL  no track data: {src['error']}")
        print("       Every slot would be UNRESOLVED TRACK. Re-run `/ps` in game, "
              "`/reload`, and retry.")
        return 1
    print(f"    dump captured : {src.get('date') or 'not stated'}")
    if src.get("date") and export["exported"] and src["date"] < export["exported"]:
        print(f"    ⚠ WARN  the /ps dump ({src['date']}) is OLDER than the export "
              f"({export['exported']}) — it may be\n            describing gear the "
              "export has already replaced. Re-run `/ps` and `/reload`.")

    if stale:
        days, patch, live_date = stale
        print(f"    ❌ STALE  simc checkout is {days} days older than {patch} "
              f"(live {live_date}) — do not report DPS from it")
        return 3

    _crest_plan_lines(export, src, [], [])

    all_ranks, unresolved = upgrade_ranks(export, src["tracks"])
    ranks = [r for r in all_ranks if r["track"] in wanted]

    print("\n  equipped slots")
    for slot in CANON_SLOTS:
        entry = export["equipped"].get(slot)
        if not entry or slot in COSMETIC_SLOTS:
            continue
        row = src["tracks"].get(slot)
        if not row or row.get("track") not in TRACKS:
            why = next((u["why"] for u in unresolved if u["slot"] == slot), "")
            print(f"    {slot:<10} {label(entry):<52} UNRESOLVED TRACK — {why}")
            continue
        left = [r for r in all_ranks if r["slot"] == slot]
        mark = watermark_for(export, slot)
        bits = f"{row['track']} {row['level']}/{row['cap']}"
        if mark:
            bits += (f"; watermark {mark['character']}"
                     + (" (paired-slot rule, UNVERIFIED)" if mark["paired"] else ""))
        print(f"    {slot:<10} {label(entry):<52} {bits}; {len(left)} rank(s) left")
    print("    · UNRESOLVED TRACK is costed at NOTHING and never inferred from the "
          "ilvl band:\n      295 is Veteran 6/6 OR Champion 2/6, 305 is Champion 6/6 "
          "OR Hero 1/6.")

    if not ranks:
        scope = (f"the {args.track} track" if args.track else "any track")
        print(f"\n  COMPUTED: no equipped item has a remaining rank on {scope}. "
              "That is an\n  answer, not a failure — there is nothing to spend "
              "crests on in this scope.")
        return 0

    balances = crest_balances(export)
    print(f"\n  plan: {len(ranks)} rank(s) across "
          f"{len({r['slot'] for r in ranks})} slot(s) → {len(styles)} comparison "
          f"frame(s) at {args.iterations} iterations")
    print("        every rank is the SAME item at a higher ilvl, so no rank "
          "introduces a new\n        special effect and no firing-gate validation "
          "run is needed")

    def frame_for(targets: int, time: int) -> Frame:
        return run_frame(export, ref, rank_variants(ranks), targets=targets, time=time,
                         iterations=args.iterations,
                         tag=f"crests-{char}-{targets}t{time}s")

    frames = [frame_for(*styles[0])]
    base_findings = firing_gate(export, ref, frames[0].data)
    leaks = leak_gate(export, frames[0].built, frames[0].data)
    fidelity = ilvl_fidelity_gate(export, frames[0].player)

    fails = [f for f in base_findings if f["level"] == "FAIL"]
    warns = [f for f in base_findings if f["level"] == "WARN"]
    blocked = bool(fails or leaks or fidelity)

    if not blocked or args.accept_failing_gate:
        frames += [frame_for(*style) for style in styles[1:]]

    print("\n  gates")
    if not base_findings:
        print(f"    ✅ firing gate — {BASELINE}: every equipped special effect fired")
    else:
        _print_findings(base_findings, "    ")
    if leaks:
        print(f"    ❌ FAIL  reference-profile gear leaked into: {', '.join(leaks)}")
    if fidelity:
        for f in fidelity:
            print(f"    ❌ FAIL  ilvl fidelity — {f['slot']} {f['item']}: the export "
                  f"states {f['stated']},\n             simc resolved "
                  f"{f['resolved']}. Every rank below is 'this item, +N ilvl', so a "
                  "baseline\n             that is not the worn item measures a "
                  "different ladder than the one planned.")
    else:
        print(f"    ✅ ilvl fidelity — simc's resolved ilvl matches the export in all "
              f"{len([s for s in export['equipped'] if s not in COSMETIC_SLOTS])} slot(s)")
    gaps = sorted({(r["slot"], r["from_ilvl"], r["model_ilvl"])
                   for r in ranks if r["model_gap"]})
    for slot, worn, modelled in gaps:
        print(f"    ⚠ WARN  track model — {slot} is worn at {worn} but the track table "
              f"puts its\n            current step at {modelled}. Its target ilvls "
              "are interpolated and may be off by ±1.")
    odd = sorted({r["slot"] for r in ranks if r["nonstandard_cap"]})
    if odd:
        print(f"    ⚠ WARN  non-6-step track on {', '.join(odd)} — the KB table "
              "(dawncrests.md:53-64)\n            models 6 steps; targets are "
              "stretched over the reported cap.")

    if blocked and not args.accept_failing_gate:
        print(f"\n  ⛔ NO DPS PRINTED — {len(fails) + len(leaks) + len(fidelity)} "
              "failing gate(s).\n     Re-run with --accept-failing-gate '<why this "
              "allocation survives the failure>'.")
        return 1
    if blocked:
        print(f"\n  ⚠ GATE FAILED, ACCEPTED — {args.accept_failing_gate}")

    deltas = {f.id: frame_deltas(f) for f in frames}
    brand = ("⚠ GATE-FAILED " if blocked else "") + override_brand(frames[0].built)
    print()
    for line in _table(frames, deltas, brand):
        print("  " + line)

    interp = [rank_name(r) for r in ranks if r["interpolated"]]
    if interp:
        print(f"\n  ~interp — {len(interp)} rank(s) target an INTERPOLATED ilvl: "
              "only 1/6 and 6/6 are\n  Tier-1 (dawncrests.md:80 records the "
              "intermediates as unconfirmed). Season 1's known\n  Champion ladder "
              "shows linear interpolation landing ±1 off at two of the four\n  "
              "intermediate steps, which is the error bar on those rows.")
        for name in interp:
            print(f"    ~interp  {name}")

    by_name = {r["name"]: r for r in deltas[frames[0].id]}

    free = [r for r in ranks if r["free"] and not args.ignore_watermark]
    paid = [r for r in ranks if not (r["free"] and not args.ignore_watermark)]

    print("\n  free by watermark (0 crests)")
    if args.ignore_watermark:
        print("    · --ignore-watermark: every rank is costed, none treated as free")
    elif not free:
        print("    none — every remaining rank targets an ilvl above its slot's "
              "watermark")
    for r in free:
        row = by_name.get(rank_name(r))
        pct = f"{row['delta_pct']:+.2f}% ± {row['err_pct']:.2f}% ({row['verdict']})" \
            if row else "not simulated"
        note = "  paired-slot rule (UNVERIFIED)" if (r["watermark"] or {}).get("paired") \
            else ""
        print(f"    {rank_name(r):<40} ≤ watermark {r['watermark']['character']}"
              f"  {pct}{note}")
    if free:
        print("    · dawncrests.md:215-232, confirmed in-game 2026-08-19 — same "
              "character only.\n      Still unmeasured: whether the free ride caps at "
              "the watermark or at the item's\n      own track ceiling.")

    print("\n  budget")
    for track in sorted(wanted):
        held = balances.get(track, 0)
        n = len([r for r in paid if r["track"] == track])
        if not n and not held:
            continue
        afford = held // CREST_COST_PER_RANK
        disc_afford = held // CREST_COST_DISCOUNTED
        print(f"    {track:<11} {held:>4} held ÷ {CREST_COST_PER_RANK} per rank "
              f"= {afford} rank(s)   [Tier-3 est]"
              f"   (at the 50% discount: {disc_afford})")
    if args.budget is not None:
        print(f"    · --budget {args.budget}: overriding the derived rank count")
    print("    · the per-rank cost is Tier-3 ONLY (dawncrests.md:84-89, with an open "
          "TODO at :301).\n      Because it is UNIFORM across ranks, it moves the "
          "COUNT you can afford and nothing\n      else — the ORDER below is "
          "independent of it and is not branded.")

    print("\n  allocation (greedy on MARGINAL Δ, ranks stack within a slot)")
    # Per TRACK, never pooled — each crest tier upgrades its own track only.
    budgets = {t: (args.budget if args.budget is not None
                   else balances.get(t, 0) // CREST_COST_PER_RANK) for t in wanted}
    budget = sum(budgets.values())
    # A track carrying ranks but no crests is the answer, so it is named rather than
    # left to be inferred from an allocation that silently skips it.
    broke = sorted({r["track"] for r in paid if budgets.get(r["track"], 0) <= 0})
    for track in broke:
        n = len([r for r in paid if r["track"] == track])
        print(f"    ⛔ {track}: {n} rank(s) available but "
              f"{balances.get(track, 0)} crest(s) held — NONE of them is buyable")
    if not paid:
        print("    nothing to buy — every remaining rank in scope is free by watermark")
    elif budget <= 0:
        print(f"    0 rank(s) affordable: no crests held for {', '.join(sorted(wanted))}")
    else:
        chosen = allocate(paid, by_name, budgets)
        if not chosen:
            print(f"    {budget} rank(s) affordable in total, but no rank whose "
                  "OWN track has crests has a positive marginal Delta")
        for i, r in enumerate(chosen, 1):
            row = by_name.get(rank_name(r), {})
            print(f"    {i}. {rank_name(r):<40} marginal {r['marginal_pct']:+.2f}%"
                  f"   cumulative {row.get('delta_pct', 0):+.2f}%"
                  f" ± {row.get('err_pct', 0):.2f}% ({row.get('verdict', '?')})")
        per_track: dict[str, int] = {}
        for r in chosen:
            per_track[r["track"]] = per_track.get(r["track"], 0) + 1
        cost = ", ".join(f"{n * CREST_COST_PER_RANK} {tr}"
                         for tr, n in sorted(per_track.items()))
        print(f"    → {len(chosen)} rank(s) worth buying; {cost} crest(s) [Tier-3 est]")

    # `crests` answers "what should I upgrade"; `gear` answers "what should I wear".
    # Neither knows about the other, so the seam is printed rather than papered over.
    near = []
    for slot in {r["slot"] for r in ranks}:
        worn_ilvl = (export["equipped"].get(slot) or {}).get("ilvl")
        if worn_ilvl is None:
            continue
        for cand in candidates(export, slot):
            if cand["item_string"] == export["equipped"][slot]["item_string"]:
                continue
            if cand.get("ilvl") and abs(cand["ilvl"] - worn_ilvl) <= 6:
                near.append(slot)
                break
    if near:
        print(f"\n  ⚠ UPGRADE vs REPLACE — {', '.join(sorted(near))} has a bag or vault "
              "candidate within\n    6 ilvl of what is worn. This command costs the "
              "WORN item's ladder and knows nothing\n    about replacing it; run "
              f"`wowkb.sim gear {char} --slot <slot>` before spending.")

    if len(frames) == 1:
        print(f"\n  ⚠ ONE fight style only ({frames[0].style}) — 1T and 5T disagreed "
              "on ordering\n    more than once on 2026-08-20.")
    print(f"\n  Medians only. Δ is against {BASELINE} (current gear) WITHIN each frame; "
          "the tool\n  cannot delta across invocations. ± is a 95% band on the median "
          f"(simc's mean\n  standard error × {SE_MEDIAN_FACTOR}, baseline and variant "
          "errors combined).")
    print(f"  {len(fails) + len(leaks) + len(fidelity)} failure(s), "
          f"{len(warns)} warning(s).")
    return 1 if blocked else 0



# ══ The cast timeline (Phase 5) ══════════════════════════════════════════════
#
# `log` answers a question no aggregate can: WHEN did this happen, and next to what.
# The 2026-08-20 session inferred trinket misalignment from summary counts and got it
# backwards twice; the mechanism (upstream's trinket2 rung waits on
# `trinket.1.cooldown.remains`, and with both trinkets at 305 that cooldown never moves)
# is invisible in every aggregate simc prints and obvious in a timeline.
#
# ⚠ THREE structural facts, all deliberate:
#
# 1. **It is ONE iteration.** A single sample cannot support a DPS claim, a delta or a
#    frequency, so it never prints one — every line carries the SINGLE SAMPLE brand and
#    there is no `--iterations` flag to promote it into a statistical run by accident.
# 2. **It cannot use profilesets.** simc disables logging outright when profilesets are
#    enabled (`sim.cpp:4361` — `if ( parent || profileset_enabled ) { debug = false;
#    log = 0; }`), so `--variant` is a separate invocation. That is safe here for the
#    same reason it is forbidden everywhere else in this tool: no number crosses between
#    runs, because no number is reported at all.
# 3. **It reads the TEXT log, not the JSON.** The JSON is used only for the leak gate,
#    which is structural and iteration-independent.

# `deterministic=1` fixes the RNG stream, so the same seed reproduces the same timeline
# exactly. Without it a "reproduce the 2026-08-20 window" instruction means nothing.
LOG_SEED = 1000
def log_options(seed: int, targets: int, time: int) -> dict:
    """simc options for a timeline run. Every one of these is load-bearing.

    `iterations`/`threads` are FIXED at 1 and there is no flag to raise them: a log is a
    single sample, and one that quietly became a 1000-iteration run would print a
    timeline from an arbitrary one of them. `deterministic` fixes the RNG stream so the
    same seed reproduces the same timeline exactly — without it, "reproduce the window"
    is not a instruction anyone can follow. `log_spell_id` puts the spell id on every
    row, which is what makes an action token traceable back to game data.
    """
    return {"iterations": 1, "threads": 1, "deterministic": 1, "log": 1,
            "log_spell_id": 1, "seed": seed, "fight_style": "Patchwerk",
            "max_time": time, "desired_targets": targets}

LOG_BRAND = "SINGLE SAMPLE — NOT A DPS RESULT | "

LOG_TIME = re.compile(r"^(?P<t>\d+\.\d+)\s+(?P<rest>.*)$")
LOG_CAST = re.compile(
    r"^Player '(?P<actor>[^']+)' performs Action '(?P<action>[^']+)' \((?P<spell>-?\d+)\)")
LOG_SUMMON = re.compile(
    r"^Player '(?P<actor>[^']+)' summons (?P<pet>\S+) for (?P<dur>[\d.]+)s")
LOG_DISMISS = re.compile(r"^Player '(?P<actor>[^']+)' dismisses (?P<pet>\S+)")
LOG_BUFF_GAIN = re.compile(
    r"^(?:Player|Enemy) '(?P<actor>[^']+)' gains Buff '(?P<buff>[^']+)' "
    r"\((?P<spell>-?\d+)\)(?: \(stacks=(?P<stacks>\d+)\))?")
LOG_BUFF_LOSE = re.compile(
    r"^(?:Player|Enemy) '(?P<actor>[^']+)' loses Buff '(?P<buff>[^']+)'")
LOG_CONSUME = re.compile(
    r"^Player '(?P<actor>[^']+)' consumes (?P<amount>[\d.]+) (?P<resource>\w+) "
    r"for Action '(?P<action>[^']+)'")


def parse_log(text: str) -> list[dict]:
    """simc's combat log → typed events, in order.

    Only the verbs a timeline reader can act on. The ones dropped are deliberately the
    high-volume bookkeeping ones — `schedules execute`, `schedules travel`, `refreshes`,
    `decrements` and the per-hit damage rows are 60% of a 120s log and say nothing about
    ORDER, which is the only thing this command is for.
    """
    events: list[dict] = []
    for line in text.splitlines():
        m = LOG_TIME.match(line)
        if not m:
            continue
        t, rest = float(m.group("t")), m.group("rest")
        for kind, pat in (("cast", LOG_CAST), ("summon", LOG_SUMMON),
                          ("dismiss", LOG_DISMISS), ("buff", LOG_BUFF_GAIN),
                          ("buff_end", LOG_BUFF_LOSE), ("consume", LOG_CONSUME)):
            hit = pat.match(rest)
            if hit:
                events.append({"t": t, "kind": kind, "raw": rest, **hit.groupdict()})
                break
    return events


def log_actions(events: list[dict], actor: str) -> dict[str, int]:
    """The action vocabulary an actor actually used — what `--around` accepts."""
    out: dict[str, int] = {}
    for e in events:
        if e["kind"] == "cast" and e["actor"] == actor:
            out[e["action"]] = out.get(e["action"], 0) + 1
    return out


def log_windows(events: list[dict], actor: str, anchor: str,
                before: float, after: float | None) -> list[dict]:
    """One window per cast of `anchor` by `actor`.

    When `after` is not given it comes from the anchor's OWN summon duration in the log
    ("summons demonic_tyrant for 20.272s") — a cooldown window should be as long as the
    cooldown lasts, and hardcoding 20s for Tyrant would be a Demonology special case in
    a tool that has none.
    """
    windows = []
    for i, e in enumerate(events):
        if e["kind"] != "cast" or e["actor"] != actor or e["action"] != anchor:
            continue
        span, source = after, "--after"
        if span is None:
            follow = next((f for f in events[i:i + 40]
                           if f["kind"] == "summon" and f["actor"] == actor
                           and abs(f["t"] - e["t"]) < 0.01), None)
            if follow:
                span, source = float(follow["dur"]), f"the summon's own {follow['pet']} duration"
            else:
                span, source = 15.0, "the 15s default (this cast summons nothing)"
        windows.append({"anchor": e, "start": e["t"] - before, "end": e["t"] + span,
                        "span": span, "span_source": source})
    return windows


def window_events(events: list[dict], win: dict, actor: str, *,
                  pets: bool, buffs: bool) -> list[dict]:
    out = []
    for e in events:
        if not (win["start"] <= e["t"] <= win["end"]):
            continue
        own = e.get("actor") == actor
        if not own and not (pets and str(e.get("actor", "")).startswith(actor + "_")):
            continue
        if e["kind"] in ("buff", "buff_end") and not buffs:
            continue
        out.append(e)
    return out


def _log_line(e: dict, anchor_t: float, actor: str) -> str:
    off = e["t"] - anchor_t
    who = "" if e.get("actor") == actor else f"[{str(e.get('actor', '')).removeprefix(actor + '_')}] "
    if e["kind"] == "cast":
        body = f"CAST     {who}{e['action']} ({e['spell']})"
    elif e["kind"] == "summon":
        body = f"summon   {who}{e['pet']} for {float(e['dur']):.2f}s"
    elif e["kind"] == "dismiss":
        body = f"dismiss  {who}{e['pet']}"
    elif e["kind"] == "buff":
        body = (f"buff+    {who}{e['buff']} ({e['spell']})"
                + (f" x{e['stacks']}" if e.get("stacks") else ""))
    elif e["kind"] == "buff_end":
        body = f"buff-    {who}{e['buff']}"
    else:
        body = (f"spend    {who}{float(e['amount']):g} {e['resource']}"
                f" → {e['action']}")
    return f"{e['t']:8.3f}  {off:+7.3f}  {body}"


def on_use_presses(export: dict, events: list[dict], actor: str) -> list[dict]:
    """Every equipped on-use effect and the times it actually resolved in THIS sample.

    Matched by the same keys and spell ids the firing gate uses, against the log's cast
    and buff-gain rows — simc emits no `use_item` line of its own, so the effect landing
    IS the press.
    """
    out = []
    for sub in effect_subjects(export):
        if not sub["on_use"]:
            continue
        times = sorted({
            e["t"] for e in events
            if e["kind"] in ("cast", "buff")
            and (str(e.get("actor")) == actor
                 or str(e.get("actor", "")).startswith(actor + "_"))
            and (e.get("action") in sub["keys"] or e.get("buff") in sub["keys"]
                 or _int(str(e.get("spell", ""))) in sub["ids"])
        })
        out.append({**sub, "times": times})
    return out


def cmd_log(args) -> int:
    missing = simc_available()
    if missing:
        print(missing, file=sys.stderr)
        return 2

    path = find_export(args.character)
    export = parse_export(path.read_text(encoding="utf-8"))
    ref = resolve_reference(export["class"], export["spec"], args.hero, args.apl_source)
    commit = simc_commit()
    stale = staleness(commit)
    actor = export["character"] or "player"

    overrides: dict[str, str] = {}
    notes: list[str] = []
    if args.variant:
        _, overrides = parse_variant(f"variant={args.variant}", export, notes)

    print(f"wowkb.sim log — {export['character']} "
          f"({export['spec']} {export['class']})")
    print("\n  harness")
    print(f"    export        : {_rel(path)} ({export['exported']})")
    print(f"    reference APL : {_rel(ref['path'])}  [{ref['tier']}]")
    if ref.get("warn"):
        print(f"    ⚠ {ref['warn']}")
    print(f"    simc commit   : {commit['short'] if commit else 'unresolved'} "
          f"{commit['date'] if commit else ''}")
    drift = _build_drift(export)
    if drift:
        print(f"    ⚠ {drift}")
    for note in notes:
        print(f"    · {note}")
    if overrides:
        for slot, value in overrides.items():
            print(f"    variant       : {slot} = {value or '(cleared)'}")
        print("    ⚠ a variant is a SEPARATE simc invocation — simc disables logging "
              "entirely when\n      profilesets are enabled (sim.cpp:4361). Safe here "
              "only because no number is\n      reported, so nothing can be deltaed "
              "across the two runs.")

    if stale:
        days, patch, live_date = stale
        print(f"    ❌ STALE  simc checkout is {days} days older than {patch} "
              f"(live {live_date}) — do not read a timeline from it")
        return 3

    profile, built = build_profile(export, ref, overrides=overrides)
    log_file = RESULTS / f"log-{actor.lower()}.txt"
    options = log_options(args.seed, args.targets, args.time)
    data, profile_file = run_simc(profile, options, RESULTS,
                                  f"log-{actor.lower()}", log_file=log_file)
    print(f"    combat log    : {_rel(log_file)}")
    print(f"    determinism   : "
          + ", ".join(f"{k}={v}" for k, v in options.items()))

    leaks = leak_gate(export, built, data)
    if leaks:
        print(f"\n  ❌ FAIL  reference-profile gear leaked into: {', '.join(leaks)}"
              "\n           the timeline is a different character's. Nothing printed.")
        return 1

    events = parse_log(log_file.read_text(encoding="utf-8", errors="replace"))
    vocab = log_actions(events, actor)

    if args.list_actions or not args.around:
        print(f"\n  {len(vocab)} action(s) {actor} cast in this sample "
              "— any of these is a valid --around")
        for name, n in sorted(vocab.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"    {n:>4} ×  {name}")
        if not args.around:
            print("\n  pass --around <action> for a windowed timeline.")
        return 0

    if args.around not in vocab:
        print(f"\n  ⚠ {actor} never cast {args.around!r} in this sample.")
        print("    A single iteration cannot tell 'never casts it' from 'did not cast "
              "it THIS time'.\n    For the first question run `wowkb.sim check "
              f"{actor.lower()}`, which is aggregate; for the\n    second, re-run with "
              "a different --seed. Actions that DID fire:")
        for name, n in sorted(vocab.items(), key=lambda kv: (-kv[1], kv[0]))[:12]:
            print(f"      {n:>4} ×  {name}")
        return 1

    windows = log_windows(events, actor, args.around, args.before, args.after)
    chosen = windows if args.all_windows else windows[args.occurrence - 1:args.occurrence]
    if not chosen:
        print(f"\n  ⚠ occurrence {args.occurrence} requested but {args.around} was cast "
              f"only {len(windows)} time(s) in this sample.")
        return 1

    presses = on_use_presses(export, events, actor)

    print(f"\n  {args.around} — cast {len(windows)} time(s) at "
          + ", ".join(f"{w['anchor']['t']:.2f}s" for w in windows)
          + (f"; showing occurrence {args.occurrence}"
             if not args.all_windows and len(windows) > 1 else ""))

    for win in chosen:
        anchor_t = win["anchor"]["t"]
        rows = window_events(events, win, actor, pets=args.pets, buffs=args.buffs)
        print(f"\n{'─' * 76}")
        print(f"  window {win['start']:.2f}s → {win['end']:.2f}s  "
              f"(−{args.before:g}s / +{win['span']:.2f}s from {win['span_source']})")
        print(f"\n  {LOG_BRAND}{'time':>8}  {'Δanchor':>7}  event")
        for e in rows:
            print("  " + LOG_BRAND + _log_line(e, anchor_t, actor))
        if not rows:
            print(f"  {LOG_BRAND}(no events — widen with --before/--after, or add "
                  "--pets/--buffs)")

        # The headline. An on-use effect's alignment with a cooldown window is exactly
        # what aggregate counts cannot show and what got answered backwards twice.
        print("\n  on-use effects vs this window")
        if not presses:
            print("    · no equipped item carries a registered on-use effect")
        for p in presses:
            inside = [t for t in p["times"] if win["start"] <= t <= win["end"]]
            # Every press time is printed, not just the nearest. A single "nearest"
            # figure cannot be checked, and it hides the reading that matters most
            # here: Freightrunner's Flask has a 120s cooldown and fired ONCE in 300s.
            when = ", ".join(f"{x:.2f}s" for x in p["times"]) or "never"
            if inside:
                offs = ", ".join(f"{x - anchor_t:+.2f}s" for x in inside)
                print(f"    ✅ {p['slot']:<9} {p['item']:<38} pressed IN window ({offs})")
            elif p["times"]:
                near = min(p["times"], key=lambda x: abs(x - anchor_t))
                print(f"    ✗  {p['slot']:<9} {p['item']:<38} not in window; nearest "
                      f"press {near - anchor_t:+.2f}s away")
            else:
                print(f"    ❌ {p['slot']:<9} {p['item']:<38} NEVER pressed anywhere in "
                      "this sample")
            print(f"       {len(p['times'])} press(es) in {args.time}s at: {when}")

    print(f"\n{'─' * 76}")
    print("  SINGLE SAMPLE — NOT A DPS RESULT. One iteration, one RNG stream "
          f"(seed={args.seed},\n  deterministic=1), so this reproduces exactly and "
          "generalises to nothing. It shows\n  ORDER and ALIGNMENT; for how often "
          f"something happens run `wowkb.sim check {actor.lower()}`\n  or `compare`, "
          "which are aggregate and gated.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="wowkb.sim", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    imp = sub.add_parser("import", help="parse a /simc export and store it verbatim")
    imp.add_argument("source", help="path to a .simc export, or - for stdin")
    imp.add_argument("--json", action="store_true", help="also dump the parsed structure")
    imp.set_defaults(func=cmd_import)

    chk = sub.add_parser("check", help="harness validation only — reports NO DPS")
    chk.add_argument("character", help="character name, or a path to an export")
    chk.add_argument("--hero", help="hero-tree profile variant (e.g. Soulharvester)")
    chk.add_argument("--apl-source", choices=APL_SOURCES, default="auto",
                     help="pin a rung of the reference chain instead of taking the "
                          "first that exists")
    chk.add_argument("--iterations", type=int, default=1000)
    chk.add_argument("--time", type=int, default=300, help="fight length in seconds")
    chk.add_argument("--targets", type=int, default=1)
    chk.set_defaults(func=cmd_check)

    cmp_ = sub.add_parser(
        "compare", help="named gear variants as profilesets in ONE simc invocation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Rank named variants against the character's current gear.

Every variant is a profileset inside a SINGLE simc process, and the baseline is one of
them — so every number in the table comes from one frame and is directly comparable.
Deltas across invocations are not merely discouraged, there is no code path for them.

  wowkb.sim compare encomplete \\
      "0pc=shoulders=@Poisoner's Pauldrons; chest=@Venom-Cursed Dragonhawk's Robes; \\
       hands=@Pyrewalker's Gloves; legs=@Wind Soarer's Breeches"

`@<Item Name>` pulls the item string out of the export's own equipped/bag/vault rows
(add `(<ilvl>)` when one name appears twice); a bare `<slot>=` strips the slot.""")
    cmp_.add_argument("character", help="character name, or a path to an export")
    cmp_.add_argument("variants", nargs="+", metavar="NAME=CHANGES",
                      help="'<Name>=<slot>=<item>[; <slot>=<item> ...]'")
    cmp_.add_argument("--hero", help="hero-tree profile variant (e.g. Soulharvester)")
    cmp_.add_argument("--apl-source", choices=APL_SOURCES, default="auto")
    cmp_.add_argument("--apl-override", metavar="FILE",
                      help="replace the upstream priority list with `actions...=` "
                           "lines from FILE. Brands every result UNVALIDATED HARNESS")
    cmp_.add_argument("--iterations", type=int, default=10000)
    cmp_.add_argument("--gate-iterations", type=int, default=250,
                      help="iterations for each variant's firing-gate validation run "
                           "(no DPS is read from these)")
    cmp_.add_argument("--targets", type=int,
                      help="run ONE fight style instead of 1T/300s AND 5T/120s")
    cmp_.add_argument("--time", type=int, default=300,
                      help="fight length, with --targets")
    cmp_.add_argument("--accept-failing-gate", metavar="REASON",
                      help="print the table despite a FAILING firing gate, branded "
                           "with REASON")
    cmp_.add_argument("--json", action="store_true")
    cmp_.set_defaults(func=cmd_compare)

    gear = sub.add_parser(
        "gear", help="rank every wearable candidate the export offers for a slot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Local Top Gear: rank a slot's bag + vault candidates against what is worn.

Candidates come from the export itself, so this answers "which of THESE, for THIS
character" and never "best trinket in the game". The bag block is NOT pre-filtered by
the addon (it filters only on "has an equippable inventory type"), so items this
character cannot wear are excluded here — and the exclusions are printed, because a
silent filter is indistinguishable from a filter with a bug.

  wowkb.sim gear encomplete --slot hands --accept-failing-gate '<reason>'
  wowkb.sim gear encomplete --all-slots""")
    gear.add_argument("character", help="character name, or a path to an export")
    gear.add_argument("--slot", help="one gear slot (e.g. hands, trinket1)")
    gear.add_argument("--all-slots", action="store_true",
                      help="sweep every slot that has a wearable alternative")
    gear.add_argument("--hero", help="hero-tree profile variant (e.g. Soulharvester)")
    gear.add_argument("--apl-source", choices=APL_SOURCES, default="auto")
    gear.add_argument("--iterations", type=int, default=10000)
    gear.add_argument("--gate-iterations", type=int, default=150,
                      help="iterations for each candidate's firing-gate validation run "
                           "(no DPS is read from these; a sweep runs many)")
    gear.add_argument("--targets", type=int,
                      help="run ONE fight style instead of 1T/300s AND 5T/120s")
    gear.add_argument("--time", type=int, default=300,
                      help="fight length, with --targets")
    gear.add_argument("--accept-failing-gate", metavar="REASON",
                      help="print the ranking despite a FAILING firing gate, branded "
                           "with REASON")
    gear.add_argument("--json", action="store_true")
    gear.set_defaults(func=cmd_gear)

    crests = sub.add_parser(
        "crests", help="rank every remaining upgrade rank on the equipped gear",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Where should the next crests go?

Every remaining rank of every equipped, TRACKED item becomes one profileset inside a
single simc invocation, so every delta is directly comparable. A rank is expressed as
the same item line with `,ilevel=<target>` — simc models no part of the upgrade system,
so the target ilvl is computed here from the KB track table.

⚠ This is the ONE command that reads outside the /simc export: an item's track and step
exist nowhere in the paste, and cannot be inferred from its ilvl (295 is Veteran 6/6 OR
Champion 2/6). Track/step comes from the PlannerState /ps dump; a slot neither it nor
the API resolves prints UNRESOLVED TRACK and is costed at nothing.

  wowkb.sim crests encomplete --track Champion
  wowkb.sim crests encomplete --all-tracks --budget 5""")
    crests.add_argument("character", help="character name, or a path to an export")
    crests.add_argument("--track", help="cost one track only (e.g. Champion)")
    crests.add_argument("--all-tracks", action="store_true",
                        help="cost every track at once")
    crests.add_argument("--budget", type=int,
                        help="rank count to allocate, instead of deriving it from the "
                             "export's crest balance")
    crests.add_argument("--ignore-watermark", action="store_true",
                        help="cost every rank, including ones the slot's high watermark "
                             "would make free")
    crests.add_argument("--hero", help="hero-tree profile variant (e.g. Soulharvester)")
    crests.add_argument("--apl-source", choices=APL_SOURCES, default="auto")
    crests.add_argument("--iterations", type=int, default=10000)
    crests.add_argument("--gate-iterations", type=int, default=150)
    crests.add_argument("--targets", type=int,
                        help="run ONE fight style instead of 1T/300s AND 5T/120s")
    crests.add_argument("--time", type=int, default=300,
                        help="fight length, with --targets")
    crests.add_argument("--accept-failing-gate", metavar="REASON",
                        help="print the allocation despite a FAILING gate, branded "
                             "with REASON")
    crests.add_argument("--json", action="store_true")
    crests.set_defaults(func=cmd_crests)

    lg = sub.add_parser(
        "log", help="deterministic single-iteration cast timeline (reports NO DPS)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""What happened, in what order, around a cooldown window.

ONE iteration with a fixed RNG seed, so it reproduces exactly and generalises to
nothing. It answers questions no aggregate can — "was the trinket pressed inside the
Tyrant window", "what did the APL do instead" — and deliberately answers no others:
there is no DPS in the output and no --iterations flag to turn it into a statistical
run. For how OFTEN something happens, use `check` or `compare`, which are gated.

  wowkb.sim log encomplete                                   # what did it cast?
  wowkb.sim log encomplete --around summon_demonic_tyrant
  wowkb.sim log encomplete --around summon_demonic_tyrant --all-windows --buffs""")
    lg.add_argument("character", help="character name, or a path to an export")
    lg.add_argument("--around", metavar="ACTION",
                    help="anchor the window on each cast of this action; omit to list "
                         "the action vocabulary this sample produced")
    lg.add_argument("--list-actions", action="store_true",
                    help="list the actions cast in this sample and stop")
    lg.add_argument("--occurrence", type=int, default=1, metavar="N",
                    help="which cast of --around to window (default: the first)")
    lg.add_argument("--all-windows", action="store_true",
                    help="every cast of --around, not just one")
    lg.add_argument("--before", type=float, default=5.0, metavar="S",
                    help="seconds of lead-in before the anchor (default 5)")
    lg.add_argument("--after", type=float, metavar="S",
                    help="seconds after the anchor; default is the anchor's OWN summon "
                         "duration read from the log, else 15")
    lg.add_argument("--buffs", action="store_true",
                    help="include buff gains and losses (noisy, and often the point)")
    lg.add_argument("--pets", action="store_true",
                    help="include the character's pets as actors")
    lg.add_argument("--variant", metavar="CHANGES",
                    help="'<slot>=<item>[; <slot>=<item> ...]' — a SEPARATE invocation, "
                         "safe only because no number is reported")
    lg.add_argument("--seed", type=int, default=LOG_SEED,
                    help=f"RNG seed (default {LOG_SEED}); the same seed reproduces the "
                         "same timeline exactly")
    lg.add_argument("--hero", help="hero-tree profile variant (e.g. Soulharvester)")
    lg.add_argument("--apl-source", choices=APL_SOURCES, default="auto")
    lg.add_argument("--targets", type=int, default=1)
    lg.add_argument("--time", type=int, default=300, help="fight length in seconds")
    lg.set_defaults(func=cmd_log)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except Unsupported as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

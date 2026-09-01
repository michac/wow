"""Offline verification that `wowkb.capart`'s catalog emitter carries every authored entry key.

Stdlib-only:  python3 tools/tests/check_capart_catalog_lua.py   (exits non-zero on failure)

`catalog_lua()` emits an entry FIELD BY FIELD — `id`, `ability`, `virtual`, `scan_when`,
`markers` — rather than walking the dict. That is deliberate (it fixes the order and the
wrapping), and it has one failure mode: a key nobody added to the emitter is dropped in SILENCE.
The generated Lua stays valid, `Catalog.Check` sees a well-formed entry, and the declaration
simply is not there.

⚠ The byte-for-byte gate in `capart check` cannot catch that on its own. It re-emits the shipped
catalogs and compares — so a key no shipped catalog uses is invisible to it, which is exactly the
state a newly declared key is in on the day it is added. This is the check that covers that gap:
it feeds the emitter a fixture the shipped set does not contain.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb import capart  # noqa: E402

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


# V12's two kinds beside an ordinary CDM entry, so the emitter has to decide per entry rather
# than per file. `star` has no CDM row and that is the point of it.
FIXTURE = {
    "spec": 581,
    "name": "emitter fixture",
    "abilities": [
        {"id": "void_ray", "spell": 9000000},
        {"id": "star", "spell": 9000001},
        {"id": "consume", "spell": 9000002},
    ],
    "entries": [
        {"id": "void_ray", "ability": "void_ray"},
        {"id": "star", "ability": "star", "virtual": "gated",
         "scan_when": [[{"pred": "proc", "args": ["void_ray"]}]]},
        {"id": "consume", "ability": "consume", "virtual": "standing"},
    ],
}


def emit(cat):
    """`catalog_lua` for a fixture, with its two disk reads redirected."""
    real_load, real_path = capart._load_json, capart.catalog_json_path
    capart._load_json = lambda _path: cat
    capart.catalog_json_path = lambda _spec: pathlib.Path("fixture/catalog.json")
    try:
        return capart.catalog_lua("fixture")
    finally:
        capart._load_json, capart.catalog_json_path = real_load, real_path


lua = emit(FIXTURE)

check('virtual = "gated"' in lua, "a gated entry's `virtual` reaches the Lua")
check('virtual = "standing"' in lua, "a standing entry's `virtual` reaches the Lua")

# Beside the ability it qualifies, on the entry's head line — the kind is a property of the
# ability, and a reader scanning the roster should not have to look for it.
head = [ln for ln in lua.splitlines() if 'id = "star", ability = ' in ln]
check(len(head) == 1 and 'ability = "star", virtual = "gated",' in head[0],
      "`virtual` is emitted directly after `ability`")

# An entry that declares none must not grow one: the key is absent, never `nil` or `false`.
plain = [ln for ln in lua.splitlines() if 'id = "void_ray", ability = ' in ln]
check(len(plain) == 1 and "virtual" not in plain[0],
      "an ordinary CDM entry emits no `virtual` key")

# The declaration is the WHOLE of V12's authoring, so the emitter must not mangle the value —
# a truthy-but-wrong string would pass `Catalog.Check`'s branch on neither kind and hatch a row
# for life.
for bad in ("gated ", "GATED", "virtual"):
    cat = {**FIXTURE, "entries": [dict(FIXTURE["entries"][1], virtual=bad)]}
    check(f'virtual = "{bad}"' in emit(cat), f"the value {bad!r} travels verbatim")

# ⚠ THE OTHER DIRECTION, and it needs a test for the same reason the ones above do: this file
# asserts that authored keys REACH the Lua, so the obvious way to make a new key safe is to add
# it to the emitter — and `defeat` must not be. It cites a numbered item in `catalog.md`, i.e. a
# rung this catalog knowingly does NOT draw, so there is nothing in the client for it to be data
# for; `Catalogs/<Spec>.lua` is data only. It travels exactly as far as `states` do, which is to
# the preview and the gates and no further.
lua = emit({**FIXTURE, "entries": [dict(FIXTURE["entries"][0], defeat=[1, 4])],
            "defeats_unreferenced": [{"n": 2, "why": "catalog-wide"}]})
check("defeat" not in lua, "an entry's `defeat` does NOT reach the Lua (authoring metadata)")
check("catalog-wide" not in lua and "defeats_unreferenced" not in lua,
      "the catalog's `defeats_unreferenced` escape does NOT reach the Lua either")

# The two CATALOG-LEVEL keys, which the emitter carries in its top-level loop rather than per
# entry — and which no shipped catalog declares yet, so the byte-for-byte gate cannot see them.
lua = emit({**FIXTURE, "break_before": "star"})
check('break_before = "star"' in lua, "`break_before` reaches the Lua")

lua = emit({**FIXTURE, "grid": {"cols": 7, "rows": 2}})
check("grid = { cols = 7, rows = 2 }" in lua,
      "`grid` reaches the Lua as one line, cols before rows")

# Absent, never `nil`: `Anchor.Grid` reads the catalog tier by asking whether the field is there.
lua = emit(FIXTURE)
check("break_before" not in lua and "grid =" not in lua,
      "a catalog declaring neither emits neither key")

# One dimension alone is a legitimate proposal — `rows` from the token, `cols` from the catalog.
lua = emit({**FIXTURE, "grid": {"cols": 7}})
check("grid = { cols = 7 }" in lua, "a one-dimension grid emits just that dimension")

print()
print(f"{_total - len(_fails)}/{_total} passed")
if _fails:
    for f in _fails:
        print("  FAILED:", f)
    sys.exit(1)

"""Query Blizzard's *machine-generated* UI API documentation (Tier 1).

WHAT THIS IS
------------
`Interface/AddOns/Blizzard_APIDocumentationGenerated/` in the wow-ui-source
checkout is Blizzard's own, build-stamped, machine-generated description of the
entire addon-facing API surface.  As of build 12.0.7.68887 it carries:

    6144 Function   1741 Event   795 Enumeration   715 Structure
     308 System      77 ScriptObject (widget APIs)  55 Constants
      32 Precondition  19 Secret  (the Midnight secret-value predicates)

It is the *highest-confidence* source in the whole KB: it ships with the client,
it is regenerated per build, and it is what the in-game `/api` browser reads.
It beats warcraft.wiki.gg on freshness and completeness, and it is the only
source that records the Midnight-era security annotations per function:

    HasRestrictions        the function is guarded by secret predicates
    IsProtectedFunction    tainted code may not call it at all
    SecretArguments        NotAllowed | AllowedWhenUntainted | AllowedWhenTainted
    SecretReturnsForAspect the returns go secret for these Enum.SecretAspect
    SecretIn*/SecretWhen*  per-function predicate flags (see `predicates`)
    SecureHooksAllowed     hooksecurefunc is permitted on it
    MayReturnNothing       returns nothing rather than erroring when guarded

WHAT IT IS *NOT*
----------------
It documents *shape*, not *behaviour*: there is no prose for most entries (only
858 of 9521 carry a `Documentation` field), and there are no examples.

Coverage of the 6144 functions splits: 4068 namespaced (`C_Spell.*`), 692
non-namespaced globals (`UnitHealth`, `GetBuildInfo`, …) and 1384 widget
methods.  Coverage of globals is *partial*: `UnitHealth` is in, but the Lua
security primitives — `hooksecurefunc`, `issecure`, `issecurevariable`,
`forceinsecure`, `securecall`, `scrub` — and `CreateFrame` are NOT, because
Blizzard never generated docs for them.  Some of those (e.g. `issecurevariable`)
do not appear anywhere in the shipped UI source either, so the *only* source for
them is warcraft.wiki.gg — cite that tier honestly.  `uiapi missing <name>` tells
you which side a name is on, so "absent from the docs" is never mistaken for
"absent from the game".

USAGE
-----
    uv run python -m wowkb.uiapi index            # build/refresh the JSON index
    uv run python -m wowkb.uiapi stats            # what's in the index + build id
    uv run python -m wowkb.uiapi func Aura        # functions matching /Aura/i
    uv run python -m wowkb.uiapi func C_Spell.GetSpellCooldown --full
    uv run python -m wowkb.uiapi event COMBAT     # events + payloads
    uv run python -m wowkb.uiapi system Spell     # one whole system
    uv run python -m wowkb.uiapi enum SecretAspect
    uv run python -m wowkb.uiapi struct AuraData
    uv run python -m wowkb.uiapi widget Frame     # ScriptObject / widget methods
    uv run python -m wowkb.uiapi secure --protected      # IsProtectedFunction
    uv run python -m wowkb.uiapi secure --restricted     # HasRestrictions
    uv run python -m wowkb.uiapi secure --hookable       # SecureHooksAllowed
    uv run python -m wowkb.uiapi predicates       # the secret-predicate vocabulary
    uv run python -m wowkb.uiapi grep <regex>     # raw ripgrep over the UI source

Every result line ends with `<file>:<line>` into the checkout so a claim can be
cited the way the addon-dev KB requires.

Add `--json` to any query for machine-readable output.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------- locations

REPO = Path(__file__).resolve().parents[2]
UISRC = REPO / "raw" / "addon-research" / "wow-ui-source"
ADDONS = UISRC / "Interface" / "AddOns"
GENDOCS = ADDONS / "Blizzard_APIDocumentationGenerated"
INDEX = REPO / "raw" / "addon-research" / "_index" / "uiapi.json"

# Lua harness: load each documentation file with stubs for the two globals the
# files touch (`APIDocumentation:AddDocumentationTable` and the `Enum` /
# `Constants` tables they reference by path), then emit JSON.
LUA_HARNESS = r"""
local out = {}

-- Enum.Foo.Bar / Constants.X referenced by the doc files resolve to their
-- dotted path as a string, so the index records *which* enum was named.
local function pathproxy(prefix)
  -- Constants files do arithmetic on enum members (e.g. `Constants.X.LAST + 1`),
  -- so the proxy has to survive +,-,*,/ and comparison. It keeps the path.
  local mt
  mt = {
    __index = function(_, k)
      local p = prefix == "" and tostring(k) or (prefix .. "." .. tostring(k))
      return pathproxy(p)
    end,
    __tostring = function() return prefix end,
    __call = function() return prefix end,
    __add = function(a, b) return pathproxy(prefix) end,
    __sub = function(a, b) return pathproxy(prefix) end,
    __mul = function(a, b) return pathproxy(prefix) end,
    __div = function(a, b) return pathproxy(prefix) end,
    __unm = function() return pathproxy(prefix) end,
    __concat = function(a, b) return prefix end,
    __lt = function() return false end,
    __le = function() return false end,
  }
  return setmetatable({}, mt)
end
local function pathstr(v)
  local mt = getmetatable(v)
  if mt and mt.__tostring then return tostring(v) end
  return nil
end

Enum = pathproxy("Enum")
Constants = pathproxy("Constants")

APIDocumentation = {
  AddDocumentationTable = function(_, t) out[#out+1] = t end,
}

local esc = {
  ['"'] = '\\"', ['\\'] = '\\\\', ['\n'] = '\\n', ['\r'] = '\\r', ['\t'] = '\\t',
}
local function q(s)
  return '"' .. s:gsub('[%c"\\]', function(c)
    return esc[c] or string.format('\\u%04x', c:byte())
  end) .. '"'
end

local enc
local function isarray(t)
  local n = 0
  for k in pairs(t) do
    if type(k) ~= "number" then return false end
    n = n + 1
  end
  return n == #t
end
enc = function(v)
  local tv = type(v)
  if tv == "nil" then return "null"
  elseif tv == "boolean" then return tostring(v)
  elseif tv == "number" then return string.format("%.14g", v)
  elseif tv == "string" then return q(v)
  elseif tv == "table" then
    local p = pathstr(v)
    if p then return q(p) end
    local parts = {}
    if isarray(v) then
      for _, x in ipairs(v) do parts[#parts+1] = enc(x) end
      return "[" .. table.concat(parts, ",") .. "]"
    end
    local keys = {}
    for k in pairs(v) do keys[#keys+1] = tostring(k) end
    table.sort(keys)
    for _, k in ipairs(keys) do
      parts[#parts+1] = q(k) .. ":" .. enc(v[k])
    end
    return "{" .. table.concat(parts, ",") .. "}"
  end
  return "null"
end

local files = {}
for i = 1, #arg do files[#files+1] = arg[i] end

local results = {}
for _, f in ipairs(files) do
  local n0 = #out
  local chunk, err = loadfile(f)
  if not chunk then
    results[#results+1] = '{"file":' .. q(f) .. ',"error":' .. q(tostring(err)) .. '}'
  else
    local ok, perr = pcall(chunk)
    if not ok then
      results[#results+1] = '{"file":' .. q(f) .. ',"error":' .. q(tostring(perr)) .. '}'
    else
      for i = n0 + 1, #out do
        results[#results+1] = '{"file":' .. q(f) .. ',"table":' .. enc(out[i]) .. '}'
      end
    end
  end
end
io.write("[" .. table.concat(results, ",") .. "]")
"""


def _lua_bin() -> str:
    for c in ("lua5.1", "lua", "lua5.4", "luajit"):
        p = subprocess.run(["which", c], capture_output=True, text=True)
        if p.returncode == 0:
            return c
    sys.exit("no lua interpreter found (apt install lua5.1)")


def _build_version() -> str:
    vf = UISRC / "version.txt"
    return vf.read_text().strip() if vf.exists() else "unknown"


def _commit() -> str:
    p = subprocess.run(
        ["git", "-C", str(UISRC), "rev-parse", "HEAD"], capture_output=True, text=True
    )
    return p.stdout.strip()[:12] if p.returncode == 0 else "unknown"


# ------------------------------------------------------------------- index


def _line_of(path: Path, name: str, kind_hint: str) -> int:
    """Best-effort source line for `Name = "<name>"` inside `path`."""
    try:
        for i, ln in enumerate(path.read_text(errors="replace").splitlines(), 1):
            if re.search(r'Name\s*=\s*"%s"' % re.escape(name), ln):
                return i
    except OSError:
        pass
    return 0


def build_index() -> dict:
    if not GENDOCS.is_dir():
        sys.exit(f"missing {GENDOCS}\nrun: wowkb.uiapi index after cloning wow-ui-source")
    files = sorted(GENDOCS.glob("*.lua"))
    harness = INDEX.parent / "_uiapi_harness.lua"
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    harness.write_text(LUA_HARNESS)

    raw: list[dict] = []
    # chunk to stay under ARG_MAX
    for i in range(0, len(files), 120):
        batch = [str(f) for f in files[i : i + 120]]
        p = subprocess.run(
            [_lua_bin(), str(harness), *batch], capture_output=True, text=True
        )
        if p.returncode != 0:
            sys.exit(f"lua failed: {p.stderr[:2000]}")
        raw.extend(json.loads(p.stdout))

    systems, funcs, events, enums, structs, widgets, preds, consts = [], [], [], [], [], [], [], []
    errors = []
    for entry in raw:
        if "error" in entry:
            errors.append(entry)
            continue
        f = Path(entry["file"])
        rel = str(f.relative_to(UISRC))
        t = entry["table"]
        ttype = t.get("Type")
        ns = t.get("Namespace")
        # Constants-only doc files have no top-level Name; fall back to the file
        # stem so results are still attributable.
        sysname = t.get("Name") or f.stem.replace("Documentation", "")
        owner = {
            "system": sysname,
            "namespace": ns,
            "environment": t.get("Environment"),
            "file": rel,
            "type": ttype,
        }
        if ttype == "System":
            systems.append({**owner, "line": _line_of(f, sysname, "System")})
        elif ttype == "ScriptObject":
            widgets.append({**owner, "line": _line_of(f, sysname, "ScriptObject")})

        for fn in t.get("Functions") or []:
            qual = f"{ns}.{fn['Name']}" if ns else fn["Name"]
            rec = {
                "name": fn["Name"],
                "qualified": qual,
                "owner": sysname,
                "namespace": ns,
                "ownerType": ttype,
                "file": rel,
                "line": _line_of(f, fn["Name"], "Function"),
                "args": fn.get("Arguments") or [],
                "returns": fn.get("Returns") or [],
                "doc": fn.get("Documentation") or [],
            }
            for k, v in fn.items():
                if k in ("Name", "Type", "Arguments", "Returns", "Documentation"):
                    continue
                rec.setdefault("flags", {})[k] = v
            (widgets if ttype == "ScriptObject" else funcs).append(rec) if False else funcs.append(rec)
        for ev in t.get("Events") or []:
            events.append(
                {
                    "name": ev["Name"],
                    "literal": ev.get("LiteralName"),
                    "owner": sysname,
                    "file": rel,
                    "line": _line_of(f, ev["Name"], "Event"),
                    "payload": ev.get("Payload") or [],
                    "doc": ev.get("Documentation") or [],
                    "flags": {
                        k: v
                        for k, v in ev.items()
                        if k
                        not in ("Name", "Type", "LiteralName", "Payload", "Documentation")
                    },
                }
            )
        for tb in t.get("Tables") or []:
            rec = {
                "name": tb["Name"],
                "owner": sysname,
                "file": rel,
                "line": _line_of(f, tb["Name"], tb.get("Type", "")),
                "kind": tb.get("Type"),
                "fields": tb.get("Fields") or [],
                "values": tb.get("Values") or [],
                "doc": tb.get("Documentation") or [],
                "numValues": tb.get("NumValues"),
                "minValue": tb.get("MinValue"),
                "maxValue": tb.get("MaxValue"),
            }
            k = tb.get("Type")
            if k == "Enumeration":
                enums.append(rec)
            elif k == "Structure":
                structs.append(rec)
            elif k == "Constants":
                consts.append(rec)
            else:
                structs.append(rec)
        for pr in t.get("Predicates") or []:
            preds.append({**pr, "file": rel, "line": _line_of(f, pr["Name"], "Predicate")})

    idx = {
        "build": _build_version(),
        "commit": _commit(),
        "source": str(GENDOCS.relative_to(REPO)),
        "counts": {
            "systems": len(systems),
            "widgets": len(widgets),
            "functions": len(funcs),
            "events": len(events),
            "enums": len(enums),
            "structs": len(structs),
            "constants": len(consts),
            "predicates": len(preds),
        },
        "errors": errors,
        "systems": systems,
        "widgets": widgets,
        "functions": funcs,
        "events": events,
        "enums": enums,
        "structs": structs,
        "constants": consts,
        "predicates": preds,
    }
    INDEX.write_text(json.dumps(idx))
    return idx


def load_index() -> dict:
    if not INDEX.exists():
        return build_index()
    return json.loads(INDEX.read_text())


# ------------------------------------------------------------------ render


def _sig(rec: dict) -> str:
    a = ", ".join(
        f"{x.get('Name')}: {x.get('Type')}{'?' if x.get('Nilable') else ''}"
        for x in rec.get("args", [])
    )
    r = ", ".join(
        f"{x.get('Name')}: {x.get('Type')}{'?' if x.get('Nilable') else ''}"
        for x in rec.get("returns", [])
    )
    s = f"{rec['qualified']}({a})"
    if r:
        s += f" -> {r}"
    return s


SEC_FLAGS = (
    "IsProtectedFunction",
    "HasRestrictions",
    "SecretArguments",
    "SecretReturnsForAspect",
    "SecretArgumentsAddAspect",
    "SecureHooksAllowed",
    "ReturnsNeverSecret",
    "MayReturnNothing",
    "ConstSecretAccessor",
)


def _flagline(rec: dict) -> str:
    fl = rec.get("flags") or {}
    keep = {k: v for k, v in fl.items() if k != "SecretArguments" or v != "AllowedWhenUntainted"}
    if not keep:
        return ""
    return "    [" + " ".join(f"{k}={v}" for k, v in sorted(keep.items())) + "]"


def cmd_func(idx, args):
    pat = re.compile(args.pattern, re.I)
    hits = [
        f
        for f in idx["functions"]
        if pat.search(f["qualified"]) or (args.owner and pat.search(f.get("owner") or ""))
    ]
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    for f in hits[: args.limit]:
        print(f"{_sig(f)}")
        fl = _flagline(f)
        if fl:
            print(fl)
        if args.full:
            for d in f["doc"]:
                print(f"    # {d}")
            for a in f["args"]:
                if a.get("Documentation"):
                    print(f"    arg {a['Name']}: {' '.join(a['Documentation'])}")
            for r in f["returns"]:
                if r.get("Documentation"):
                    print(f"    ret {r['Name']}: {' '.join(r['Documentation'])}")
        print(f"    {f['file']}:{f['line']}  [owner {f.get('owner')} / {f.get('ownerType')}]")
    print(f"-- {len(hits)} match(es){' (truncated)' if len(hits) > args.limit else ''}")


def cmd_event(idx, args):
    pat = re.compile(args.pattern, re.I)
    hits = [e for e in idx["events"] if pat.search(e["name"]) or pat.search(e.get("literal") or "")]
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    for e in hits[: args.limit]:
        pay = ", ".join(
            f"{p.get('Name')}: {p.get('Type')}{'?' if p.get('Nilable') else ''}"
            for p in e["payload"]
        )
        print(f"{e.get('literal') or e['name']}({pay})")
        fl = {k: v for k, v in (e.get("flags") or {}).items()}
        if fl:
            print("    [" + " ".join(f"{k}={v}" for k, v in sorted(fl.items())) + "]")
        for d in e["doc"]:
            print(f"    # {d}")
        print(f"    {e['file']}:{e['line']}  [owner {e.get('owner')}]")
    print(f"-- {len(hits)} match(es){' (truncated)' if len(hits) > args.limit else ''}")


def cmd_system(idx, args):
    pat = re.compile(args.pattern, re.I)
    for s in idx["systems"] + idx["widgets"]:
        if not (pat.search(s["system"] or "") or pat.search(s.get("namespace") or "")):
            continue
        print(f"== {s['system']}  ns={s.get('namespace')}  env={s.get('environment')}  ({s['type']})")
        print(f"   {s['file']}:{s['line']}")
        fns = [f for f in idx["functions"] if f["owner"] == s["system"]]
        evs = [e for e in idx["events"] if e["owner"] == s["system"]]
        for f in fns:
            print(f"   {_sig(f)}")
            fl = _flagline(f)
            if fl:
                print("   " + fl)
        for e in evs:
            print(f"   EVENT {e.get('literal') or e['name']}")
        print(f"   -- {len(fns)} function(s), {len(evs)} event(s)")


def _cmd_table(idx, key, args):
    pat = re.compile(args.pattern, re.I)
    hits = [t for t in idx[key] if pat.search(t["name"])]
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    for t in hits[: args.limit]:
        print(f"{t['kind']} {t['name']}  ({t.get('owner')})")
        if t.get("kind") == "Enumeration":
            print(
                f"    numValues={t.get('numValues')} min={t.get('minValue')} max={t.get('maxValue')}"
            )
        for v in t.get("values") or []:
            print(f"    {v.get('Name')} = {v.get('EnumValue')}")
        for f in t.get("fields") or []:
            if "EnumValue" in f:
                print(f"    {f.get('Name')} = {f.get('EnumValue')}")
                continue
            print(
                f"    {f.get('Name')}: {f.get('Type')}"
                f"{'?' if f.get('Nilable') else ''}"
                + (f"  # {' '.join(f['Documentation'])}" if f.get("Documentation") else "")
            )
        print(f"    {t['file']}:{t['line']}")
    print(f"-- {len(hits)} match(es)")


def cmd_widget(idx, args):
    pat = re.compile(args.pattern, re.I)
    for w in idx["widgets"]:
        if not pat.search(w["system"] or ""):
            continue
        print(f"== {w['system']} (ScriptObject)  {w['file']}:{w['line']}")
        for f in idx["functions"]:
            if f["owner"] != w["system"]:
                continue
            print(f"   {_sig(f)}")
            fl = _flagline(f)
            if fl:
                print("   " + fl)


def cmd_secure(idx, args):
    def has(f, k):
        return (f.get("flags") or {}).get(k)

    if args.protected:
        sel, label = lambda f: has(f, "IsProtectedFunction"), "IsProtectedFunction"
    elif args.restricted:
        sel, label = lambda f: has(f, "HasRestrictions"), "HasRestrictions"
    elif args.hookable:
        sel, label = lambda f: has(f, "SecureHooksAllowed"), "SecureHooksAllowed"
    elif args.secret_returns:
        sel, label = lambda f: has(f, "SecretReturnsForAspect"), "SecretReturnsForAspect"
    elif args.args_not_allowed:
        sel, label = (
            lambda f: has(f, "SecretArguments") == "NotAllowed",
            'SecretArguments="NotAllowed"',
        )
    else:
        sel, label = (
            lambda f: any(has(f, k) for k in SEC_FLAGS if k != "SecretArguments")
            or has(f, "SecretArguments") not in (None, "AllowedWhenUntainted"),
            "any security annotation",
        )
    hits = [f for f in idx["functions"] if sel(f)]
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    print(f"== {label}: {len(hits)} function(s)")
    for f in hits[: args.limit]:
        print(f"{f['qualified']}")
        fl = _flagline(f)
        if fl:
            print(fl)
        print(f"    {f['file']}:{f['line']}")
    if len(hits) > args.limit:
        print(f"-- truncated at {args.limit}; use --limit or --json")


def cmd_predicates(idx, args):
    for p in idx["predicates"]:
        print(f"{p['Name']}  type={p.get('Type')}  failureMode={p.get('FailureMode')}")
        for d in p.get("Documentation") or []:
            print(f"    # {d}")
        print(f"    {p['file']}:{p['line']}")
    print(f"-- {len(idx['predicates'])} predicate(s)")


def cmd_stats(idx, args):
    print(f"build   : {idx['build']}")
    print(f"commit  : {idx['commit']}")
    print(f"source  : {idx['source']}")
    for k, v in idx["counts"].items():
        print(f"  {k:12s} {v}")
    if idx.get("errors"):
        print(f"!! {len(idx['errors'])} file(s) failed to load:")
        for e in idx["errors"][:10]:
            print(f"   {e['file']}: {e['error'][:160]}")


def cmd_missing(idx, args):
    """Is <name> in the generated docs, in the UI source, or nowhere?"""
    name = args.name
    in_docs = [f for f in idx["functions"] if f["name"] == name or f["qualified"] == name]
    print(f"generated docs : {'YES ' + in_docs[0]['file'] + ':' + str(in_docs[0]['line']) if in_docs else 'no'}")
    p = subprocess.run(
        [
            *_grep_bin(),
            "-rn",
            "--include=*.lua",
            "--include=*.xml",
            rf"\b{re.escape(name)}\b",
            str(ADDONS),
        ],
        capture_output=True,
        text=True,
    )
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    print(f"UI source hits : {len(lines)}")
    for l in lines[:15]:
        print("   " + l.replace(str(UISRC) + "/", "")[:200])
    if not in_docs and not lines:
        print("NOT FOUND in either -> treat as unverified; check warcraft.wiki.gg and say so.")


def _grep_bin() -> list[str]:
    """ripgrep if present (much faster on the 48 MB checkout), else GNU grep."""
    if subprocess.run(["which", "rg"], capture_output=True).returncode == 0:
        return ["rg"]
    return ["grep", "-E"]


def cmd_grep(idx, args):
    bin_ = _grep_bin()
    if bin_ == ["rg"]:
        rgargs = ["rg", "-n", "--no-heading", "--color", "never"]
        for t in args.type or []:
            rgargs += ["-t", t]
    else:
        rgargs = ["grep", "-rnE", "--color=never"]
        for t in args.type or []:
            rgargs.append(f"--include=*.{t}")
    rgargs += [args.pattern, str(args.path or ADDONS)]
    p = subprocess.run(rgargs, capture_output=True, text=True)
    out = p.stdout.replace(str(UISRC) + "/", "")
    lines = out.splitlines()
    for l in lines[: args.limit]:
        print(l)
    print(f"-- {len(lines)} hit(s){' (truncated)' if len(lines) > args.limit else ''}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="wowkb.uiapi", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, pattern=True):
        s = sub.add_parser(name)
        if pattern:
            s.add_argument("pattern")
        s.add_argument("--json", action="store_true")
        s.add_argument("--limit", type=int, default=60)
        s.set_defaults(fn=fn)
        return s

    sub.add_parser("index").set_defaults(fn=lambda i, a: None, reindex=True)
    s = sub.add_parser("stats"); s.set_defaults(fn=cmd_stats); s.add_argument("--json", action="store_true"); s.add_argument("--limit", type=int, default=60)

    f = add("func", cmd_func)
    f.add_argument("--full", action="store_true", help="include Documentation prose")
    f.add_argument("--owner", action="store_true", help="also match on owning system name")

    add("event", cmd_event)
    add("system", cmd_system)
    add("widget", cmd_widget)
    e = add("enum", lambda i, a: _cmd_table(i, "enums", a))
    st = add("struct", lambda i, a: _cmd_table(i, "structs", a))
    add("const", lambda i, a: _cmd_table(i, "constants", a))

    sec = sub.add_parser("secure")
    sec.add_argument("--protected", action="store_true")
    sec.add_argument("--restricted", action="store_true")
    sec.add_argument("--hookable", action="store_true")
    sec.add_argument("--secret-returns", action="store_true")
    sec.add_argument("--args-not-allowed", action="store_true")
    sec.add_argument("--json", action="store_true")
    sec.add_argument("--limit", type=int, default=100)
    sec.set_defaults(fn=cmd_secure)

    p = sub.add_parser("predicates"); p.set_defaults(fn=cmd_predicates); p.add_argument("--json", action="store_true"); p.add_argument("--limit", type=int, default=60)

    m = sub.add_parser("missing"); m.add_argument("name"); m.set_defaults(fn=cmd_missing); m.add_argument("--json", action="store_true"); m.add_argument("--limit", type=int, default=60)

    g = sub.add_parser("grep"); g.add_argument("pattern"); g.add_argument("--type", action="append")
    g.add_argument("--path"); g.add_argument("--limit", type=int, default=80); g.add_argument("--json", action="store_true")
    g.set_defaults(fn=cmd_grep)

    args = ap.parse_args(argv)
    if args.cmd == "index":
        idx = build_index()
        cmd_stats(idx, args)
        return
    idx = load_index()
    args.fn(idx, args)


if __name__ == "__main__":
    main()

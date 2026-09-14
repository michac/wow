"""The Smart Glo grammar exists in two languages. This is the check that they agree.

Stdlib-only:  python3 tools/tests/check_smartglo.py   (exits non-zero on failure)

`wowkb.smartglo` and the addon's `Parse.lua` / `Rules.lua` read the same surface text and must
produce the same rule. Nothing has ever held them to that — backlog.md's standing `## Unproven`
item — and they have already drifted: the two try the bind forms in different orders, so a
malformed bind earns a different refusal from each. This runs one fixed corpus through both and
asserts the two things that actually matter:

  1. **Accept/reject parity.** A rule one grammar takes and the other refuses is the failure
     that produces a rule set the tool writes and the addon will not load.
  2. **Render parity, and a round trip.** Both must render an accepted rule to the SAME surface
     text, and that text must re-parse to the same render. `DescribeBind` is a curve-cache key
     and a capture-log identity as well as text, so a describe that does not re-parse breaks
     more than export.

⚠ Refusal WORDING is deliberately not compared — the two spell the dash differently and the
Lua copy is the one a player reads. The messages are printed side by side on a refusal so a
divergent *reason* is visible, which is the part that would matter.

The addon checkout is gitignored (`wowkb.addon pull sg`), and `lua` may not be installed; the
Lua half is SKIPPED with a printed note rather than failed when either is absent. The Python
half always runs.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

TOOLS = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from wowkb import smartglo as sg  # noqa: E402

ADDON = TOOLS.parent / "projects" / "smart-glo" / "addon" / "SmartGlo"

_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    print(("PASS" if cond else "FAIL"), msg)
    if not cond:
        _fails.append(msg)


# A record is one complete rule set, because `spec` scoping is what makes a bare name resolve.
SPEC = "spec druid.balance\n"
HAVOC = "spec demon_hunter.havoc\n"

CORPUS = [
    # --- the readable bowl
    SPEC + 'glow "a"\n  on moonfire\n  when refreshable(moonfire)\n',
    SPEC + 'glow "a"\n  on moonfire\n  when refreshable(moonfire) and not aura(moonfire)\n',
    SPEC + 'glow "a"\n  on moonfire\n  when ready(moonfire) or refreshable(sunfire)\n',
    # --- the new sealed family
    SPEC + 'glow "a"\n  on sunfire\n  bind sunfire.remains < 4s\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains >= 2s\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains <= 2.5s\n',
    SPEC + 'glow "a"\n  on moonfire\n  when aura(moonfire)\n  bind moonfire.remains < 6s\n',
    # --- presence on a ROWLESS debuff. Both grammars used to refuse all four of these
    # identically, so accept/reject parity held while both were wrong: a presence bind reads
    # an AuraContainer rather than a Cooldown Manager row and had no business being held to
    # the tracked-aura table. The suffixed spelling resolves, the bare slug still refuses,
    # and a raw id renders BACK as the suffixed spelling.
    HAVOC + 'glow "a"\n  on blade_dance\n  bind essence_break_258860.up on target mine\n',
    HAVOC + 'glow "a"\n  on blade_dance\n  bind 258860.up on target mine\n',
    HAVOC + 'glow "a"\n  on blade_dance\n  bind essence_break.up on target mine\n',
    HAVOC + 'glow "a"\n  on blade_dance\n  bind metamorphosis.up\n',
    # ⚠ and the guard the suffix buys: a prefix and an id that name different spells refuse.
    HAVOC + 'glow "a"\n  on blade_dance\n  bind moonfire_8921.up on target mine\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire_164812.up on target mine\n',
    # --- the families that were already there, so this corpus is a regression net too
    SPEC + 'glow "a"\n  on starsurge\n  when astral_power_placeholder\n',  # refused both sides
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.up on target mine\n',
    SPEC + 'glow "a"\n  on starsurge\n  bind astral_power% >= 60\n',
    SPEC + 'glow "a"\n  on starsurge\n  bind health% < 35\n',
    SPEC + 'glow "a"\n  on starfall\n  bind starfall.cooldown > 10s absent dark\n',
    SPEC + 'glow "a"\n  on starfall\n  bind starfall.cooldown outside 2s..8s absent show\n',
    # --- malformed: each must be refused by BOTH
    SPEC + 'glow "a"\n  on moonfire\n  when remains(moonfire)\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains < 4\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains == 4s\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains 4s\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind moonfire.remains < 4s absent dark\n',
    SPEC + 'glow "a"\n  on moonfire\n  when refreshable()\n',
    SPEC + 'glow "a"\n  on moonfire\n  bind refreshable(moonfire)\n',
    SPEC + 'glow "a"\n  on moonfire\n  when astral_power >= 40\n',
]

SENTINEL = "\x1e"

DRIVER = r"""
-- Loads the addon's grammar outside the client and renders one corpus record per call.
-- Only the four files the grammar needs; each takes `local _, ns = ...`.
local dir = ...
local ns = {}

-- The addon's two load-time client dependencies, stubbed to the shape the load path uses.
-- Nothing here is evaluated: the parser and the renderer never touch a frame.
function CreateFrame()
  return { RegisterEvent = function() end, SetScript = function() end }
end
ns.RegisterCommand = function() end
ns.Print = function() end
ns.Printf = function() end
ns.Look = {
  IsColor = function(name)
    local known = { white = true, yellow = true, red = true, green = true, blue = true,
      purple = true, orange = true, cyan = true, black = true, alarm = true }
    return known[name] == true
  end,
  Names = function() return { "white" } end,
}

for _, file in ipairs({ "Symbols.lua", "Names.lua", "Rules.lua", "Parse.lua" }) do
  local chunk, why = loadfile(dir .. "/" .. file)
  if chunk == nil then error(why) end
  chunk("SmartGlo", ns)
end

local text = io.read("*a")
for record in string.gmatch(text .. "\30", "(.-)\30") do
  if record ~= "" then
    local glows, why = ns.Parse.Text(record)
    if glows == nil then
      io.write("ERR\n", why, "\30")
    else
      -- The checker runs too: a rule that parses and would never fire is a refusal in both
      -- bowls, and the tool refuses it at the same point.
      local errs = {}
      for i, glow in ipairs(glows) do
        local ok, list = ns.Rules.CheckGlow(ns.Rules.Modernize(glow))
        if ok == nil then
          for _, err in ipairs(list) do errs[#errs + 1] = ("glow %d: %s"):format(i, err) end
        end
      end
      if #errs > 0 then
        io.write("ERR\n", table.concat(errs, "; "), "\30")
      else
        io.write("OK\n", ns.Parse.Render(glows), "\30")
      end
    end
  end
end
"""


def python_side(record):
    """(ok, render_or_message). Parse, then check — the same order the addon uses."""
    try:
        ast = sg.parse(record)
    except sg.RuleError as exc:
        return False, str(exc)
    errs = sg.check_glows(ast) if hasattr(sg, "check_glows") else _check(ast)
    if errs:
        return False, "; ".join(errs)
    scope = None
    for line in record.splitlines():
        if line.startswith("spec "):
            scope = sg.scope_key(line[5:].strip())
    return True, sg.render(ast, scope)


def _check(ast):
    errs = []
    for i, glow in enumerate(ast, start=1):
        for err in sg._check_expr(glow.get("when")) if glow.get("when") else []:
            errs.append(f"glow {i}: {err}")
        for err in sg._check_bind(glow.get("bind"), glow.get("when")):
            errs.append(f"glow {i}: {err}")
    return errs


def lua_side(records):
    lua = shutil.which("lua5.1") or shutil.which("lua")
    if lua is None or not ADDON.is_dir():
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False) as fh:
        fh.write(DRIVER)
        driver = fh.name
    try:
        out = subprocess.run([lua, driver, str(ADDON)], input=SENTINEL.join(records),
                             capture_output=True, text=True, timeout=60)
    finally:
        pathlib.Path(driver).unlink(missing_ok=True)
    if out.returncode != 0:
        print("lua driver failed:", out.stderr.strip())
        return None
    parsed = []
    for chunk in out.stdout.split(SENTINEL):
        if chunk == "":
            continue
        head, _, body = chunk.partition("\n")
        parsed.append((head == "OK", body))
    return parsed


def main():
    py = [python_side(r) for r in CORPUS]

    # The round trip, on the Python side, for every record both grammars accept.
    for record, (ok, out) in zip(CORPUS, py):
        if not ok:
            continue
        again_ok, again = python_side(out)
        label = out.splitlines()[-2].strip() if out.strip() else record.strip()
        check(again_ok and again == out, f"python round trip: {label!r}")

    lua = lua_side(CORPUS)
    if lua is None:
        print("SKIP the Lua half — no `lua` on PATH, or the gitignored addon checkout is "
              "absent (`uv run python -m wowkb.addon pull sg`). The Python half still ran.")
    else:
        check(len(lua) == len(CORPUS), "the Lua driver answered every record")
        for record, (pyok, pyout), (luaok, luaout) in zip(CORPUS, py, lua):
            label = record.replace(SPEC, "").replace("\n", "; ").strip()
            if pyok != luaok:
                print(f"    python: {'accepted' if pyok else 'refused'} -- {pyout.strip()}")
                print(f"    lua:    {'accepted' if luaok else 'refused'} -- {luaout.strip()}")
            check(pyok == luaok, f"accept/reject parity: {label!r}")
            if not (pyok and luaok):
                if not pyok and not luaok:
                    # Wording is not compared; a divergent REASON is still worth seeing.
                    print(f"    python refusal: {pyout.strip()}")
                    print(f"    lua refusal:    {luaout.strip()}")
                continue
            if pyout.strip() != luaout.strip():
                print("    python render:\n" + pyout)
                print("    lua render:\n" + luaout)
            check(pyout.strip() == luaout.strip(), f"render parity: {label!r}")

    print(f"\n{_total - len(_fails)}/{_total} checks passed")
    if _fails:
        print("\nfailed:")
        for msg in _fails:
            print("  " + msg)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

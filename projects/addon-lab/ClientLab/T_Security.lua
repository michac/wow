-- T_Security.lua — the §4.2 secret-value operation table, anchored in
-- knowledge/addon-dev/security-taint-and-restricted-data.md.
--
-- Every row declares needs="secret".  The runner gates them: OUT OF COMBAT a
-- genuine Secret Value can't be obtained, so each records `skipped` with the
-- reason and NEVER a value.  In combat, ns.GetSecret() hands back a real secret
-- (a GCD cooldown field) and each op runs inside its own pcall — MOST ARE
-- EXPECTED TO ERROR, and the error is the claim being tested, so it is recorded
-- as the answer rather than allowed to break the run.
local ADDON, ns = ...

-- secret-api-surface is the PRECONDITION for the whole table: if issecretvalue is
-- missing, Secret.lua can gate nothing.  It needs no secret itself (it only asks
-- which primitives exist), so it carries no `needs`.
ns.Test{
  id = "secret-api-surface", anchor = "security-taint-and-restricted-data.md:1328", bucket = "call",
  question = "Which security primitives are actually visible to an addon? Several are absent from the generated docs, and issecurevariable appears nowhere in the shipped source either.",
  run = function()
    local names = {
      "issecure", "issecurevariable", "issecretvalue", "issecrettable",
      "canaccessvalue", "secureexecuterange", "forceinsecure", "hooksecurefunc",
      "C_Secrets", "scrub",
    }
    local out = {}
    for _, n in ipairs(names) do out[n] = ns.GlobalType(n).g end
    return out
  end,
}

-- op(fn) — run one operation on the secret and normalise the outcome.  On success
-- the result is stashed (a secret result degrades to "<secret>") and its secrecy
-- recorded — the OUTPUT's secrecy is the half the KB does not state for the
-- "allowed" rows.  On failure the error string is the answer.
local function op(fn)
  local ok, res = pcall(fn)
  if ok then
    return { errored = false, result = ns.stash(res), resultSecret = ns.IsSecret(res) }
  end
  return { errored = true, err = tostring(res) }
end

local function row(id, line, question, run)
  ns.Test{ id = id, anchor = "security-taint-and-restricted-data.md:" .. line,
           bucket = "secret", needs = "secret", question = question, run = run }
end

row("secret-op-store-local", 722, "§4.2 row 1 — store a secret in a local / table VALUE.",
  function()
    local v = ns.GetSecret()
    return op(function() local x = v; local t = {}; t.k = v; return (x ~= nil and t.k ~= nil) end)
  end)

row("secret-op-pass-lua-fn", 723, "§4.2 row 2 — pass a secret to a Lua function.",
  function()
    local v = ns.GetSecret()
    return op(function() return (function(a) return a end)(v) end)
  end)

row("secret-op-pass-c-fn", 724, "§4.2 row 3 — pass a secret to an unmarked C function (bit.band).",
  function()
    local v = ns.GetSecret()
    local band = ns.G("bit.band")
    if type(band) ~= "function" then return { errored = false, result = "bit.band absent — untestable" } end
    return op(function() return band(v, 1) end)
  end)

row("secret-op-concat", 725, "§4.2 row 4 — concatenate a secret with '..' (result secrecy is the interesting half).",
  function()
    local v = ns.GetSecret()
    return op(function() return "x" .. v end)
  end)

row("secret-op-string-format", 726, "§4.2 row 5 — string.format with a secret argument (result secrecy is the interesting half).",
  function()
    local v = ns.GetSecret()
    return op(function() return string.format("%s", v) end)
  end)

row("secret-op-arith", 727, "§4.2 row 6 — arithmetic on a secret number.",
  function()
    local v = ns.GetSecret()
    return op(function() return v + 1 end)
  end)

row("secret-op-compare", 728, "§4.2 row 7 — compare a secret with == and with < (tested separately).",
  function()
    local v = ns.GetSecret()
    return {
      eq = op(function() return v == 1 end),
      lt = op(function() return v < 1 end),
    }
  end)

row("secret-op-bool-test-boolean", 729, "§4.2 row 8 — boolean test on a BOOLEAN secret.",
  function()
    local v = ns.GetSecret()
    -- type() on a secret is allowed and returns the real type (row 14).  If our
    -- secret is not boolean we CANNOT measure this row honestly — record that,
    -- never a fabricated verdict.
    local ok, ty = pcall(type, v)
    if not ok then return { measured = false, why = "type() on the secret errored" } end
    if ty ~= "boolean" then
      return { measured = false, why = "no boolean secret available (cooldown source is " .. tostring(ty) .. ")" }
    end
    return op(function() if v then return "truthy" else return "falsy" end end)
  end)

row("secret-op-bool-test-nonboolean", 730, "§4.2 row 9 — boolean test on a NON-boolean secret (the subtle asymmetry with row 8).",
  function()
    local v = ns.GetSecret()
    return op(function() if v then return "truthy" else return "falsy" end end)
  end)

row("secret-op-length", 731, "§4.2 row 10 — length operator # on a secret.",
  function()
    local v = ns.GetSecret()
    return op(function() return #v end)
  end)

row("secret-op-table-key", 732, "§4.2 row 11 — use a secret as a table KEY (contrast row 1, as a value).",
  function()
    local v = ns.GetSecret()
    return op(function() local t = {}; t[v] = 1; return t ~= nil end)
  end)

row("secret-op-index", 733, "§4.2 row 12 — index and index-assign a secret (read and write, separately).",
  function()
    local v = ns.GetSecret()
    return {
      read = op(function() return v.foo end),
      write = op(function() v.foo = 1; return true end),
    }
  end)

row("secret-op-call", 734, "§4.2 row 13 — call a secret as a function.",
  function()
    local v = ns.GetSecret()
    return op(function() return v() end)
  end)

row("secret-op-type", 735, "§4.2 row 14 — type(secret): allowed, and returns the REAL type.",
  function()
    local v = ns.GetSecret()
    return op(function() return type(v) end)
  end)

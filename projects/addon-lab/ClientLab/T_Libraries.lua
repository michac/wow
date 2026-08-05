-- T_Libraries.lua — tests anchored in knowledge/addon-dev/libraries-and-ecosystem.md.
local ADDON, ns = ...

-- The three serializers are reached through LibStub rather than VENDORED into the lab:
-- an addon already installed here embeds them, so this measures the code that actually
-- ships instead of a copy that can drift from it.  When none is loaded the test says so
-- and records no value.
local function libs()
  local LibStub = ns.G("LibStub")
  if type(LibStub) ~= "function" then return nil, "LibStub absent — no addon embedding these is loaded" end
  local found = {}
  for _, name in ipairs({ "AceSerializer-3.0", "LibSerialize", "LibDeflate" }) do
    local ok, lib = pcall(LibStub, name, true)
    if ok and type(lib) == "table" then found[name] = lib end
  end
  if not next(found) then return nil, "none of AceSerializer-3.0 / LibSerialize / LibDeflate is registered with LibStub" end
  return found
end

ns.Test{
  id = "serializer-secret", anchor = "libraries-and-ecosystem.md:471", bucket = "call",
  needs = "secret",
  blocked = "AceSerializer / LibSerialize / LibDeflate loaded — none is present on this "
    .. "install and the lab vendors no libraries",
  question = "What happens when a Secret Value reaches AceSerializer-3.0 / LibSerialize / LibDeflate? None of the three tests for secrets.",
  run = function()
    local found, why = libs()
    if not found then return { measured = false, why = why } end

    local v = ns.GetSecret()
    local out = {}

    local ace = found["AceSerializer-3.0"]
    if ace and type(ace.Serialize) == "function" then
      local ok, res = pcall(function() return ace:Serialize(v) end)
      -- The error TEXT is the finding: the claim under test is that AceSerializer takes
      -- a normal branch on type() and then fails inside it, so the message names the
      -- wrong place rather than saying "cannot serialize".
      out.ace = ok and ("ok:" .. ns.Capture.Safe(res)) or ("error:" .. tostring(res))
    else
      out.ace = "absent"
    end

    local lser = found["LibSerialize"]
    if lser and type(lser.Serialize) == "function" then
      local ok, res = pcall(function() return lser:Serialize(v) end)
      out.libserialize = ok and ("ok:" .. ns.Capture.Safe(res)) or ("error:" .. tostring(res))
    else
      out.libserialize = "absent"
    end

    -- LibDeflate takes a STRING, so a secret reaches it only after one of the two above
    -- produced one. Passing the secret directly is still the honest probe of "no guard".
    local ldef = found["LibDeflate"]
    if ldef and type(ldef.CompressDeflate) == "function" then
      local ok, res = pcall(function() return ldef:CompressDeflate(v) end)
      out.libdeflate = ok and ("ok:" .. ns.Capture.Safe(res)) or ("error:" .. tostring(res))
    else
      out.libdeflate = "absent"
    end

    return out
  end,
}

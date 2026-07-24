-- T_Anatomy.lua — tests anchored in knowledge/addon-dev/anatomy-and-runtime.md.
-- Split by KB TOPIC FILE (not by bucket) so W2 can go straight from a result to
-- the file:line it edits.
--
-- Globals are probed BY STRING (ns.GlobalType / ns.G), never by identifier, so
-- luacheck never sees a name whose whole point is that it may not exist.
local ADDON, ns = ...

ns.Test{
  id = "addon-exists-nested-lib", anchor = "anatomy-and-runtime.md:127", bucket = "call",
  question = "Is a nested-.toc library (LibStub) enumerated as an addon, and is an installed top-level addon (RaiderIO) reported even though it is absent from AddOns.txt?",
  run = function()
    if not (C_AddOns and C_AddOns.DoesAddOnExist) then return { api = "C_AddOns.DoesAddOnExist absent" } end
    return {
      LibStub = C_AddOns.DoesAddOnExist("LibStub"),
      RaiderIO = C_AddOns.DoesAddOnExist("RaiderIO"),
    }
  end,
}

ns.Test{
  id = "sandbox-require-os-io", anchor = "anatomy-and-runtime.md:677", bucket = "call",
  question = "Does the addon sandbox expose require / os / io?",
  run = function()
    return {
      require = ns.GlobalType("require"),
      os = ns.GlobalType("os"),
      io = ns.GlobalType("io"),
    }
  end,
}

ns.Test{
  id = "string-rtgsub-callable", anchor = "anatomy-and-runtime.md:690", bucket = "call",
  question = "Is string.rtgsub (wiki-tagged framexml, i.e. flagged Blizzard-internal) actually callable from addon code?",
  run = function()
    local ty = ns.GlobalType("string.rtgsub")
    local out = { type = ty.g }
    local fn = ns.G("string.rtgsub")
    if type(fn) == "function" then
      -- Existence is one thing; whether an insecure addon frame may CALL it is the
      -- claim.  Record the outcome of a call rather than asserting either way.
      local ok, res = pcall(fn, "aXbXc", "X", "-")
      out.calledOk = ok
      out.result = ok and tostring(res) or tostring(res)
    else
      out.calledOk = false
      out.result = "not a function"
    end
    return out
  end,
}

ns.Test{
  id = "wow-lua-zero-use-fns", anchor = "anatomy-and-runtime.md:697", bucket = "call",
  question = "Do table.freeze / table.isfrozen / table.removemulti / strsplittable exist at 12.0.7? All four are wiki-listed with ZERO uses in the shipped source.",
  run = function()
    return {
      ["table.freeze"] = ns.GlobalType("table.freeze").g,
      ["table.isfrozen"] = ns.GlobalType("table.isfrozen").g,
      ["table.removemulti"] = ns.GlobalType("table.removemulti").g,
      strsplittable = ns.GlobalType("strsplittable").g,
    }
  end,
}

ns.Test{
  id = "issecure-in-addon-frame", anchor = "anatomy-and-runtime.md:768", bucket = "call",
  question = "Does issecure() ever return true from a plain addon call frame, and is AddLuaErrorHandler even visible to us?",
  run = function()
    local out = {
      issecure = ns.GlobalType("issecure").g,
      AddLuaErrorHandler = ns.GlobalType("AddLuaErrorHandler").g,
    }
    local fn = ns.G("issecure")
    if type(fn) == "function" then
      local ok, res = pcall(fn)
      out.issecureResult = ok and (res and true or false) or ("errored: " .. tostring(res))
    end
    return out
  end,
}

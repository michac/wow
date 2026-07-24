-- T_ApiEvents.lua — tests anchored in knowledge/addon-dev/api-events-and-discovery.md.
local ADDON, ns = ...

ns.Test{
  id = "combatlog-secure-globals", anchor = "api-events-and-discovery.md:484", bucket = "call",
  question = "Do the six C_CombatLog.* names documented only on C_CombatLogSecure resolve to nil for an addon?",
  run = function()
    local names = {
      "C_CombatLog.AddEventFilter", "C_CombatLog.ClearEventFilters",
      "C_CombatLog.GetCurrentEntryInfo", "C_CombatLog.GetCurrentEventInfo",
      "C_CombatLog.GetEntryCount", "C_CombatLog.ShouldShowCurrentEntry",
    }
    local out = {}
    for _, n in ipairs(names) do out[n] = ns.GlobalType(n).g end
    return out
  end,
}

ns.Test{
  id = "is-callback-event", anchor = "api-events-and-discovery.md:411", bucket = "call",
  question = "Does C_EventUtils.IsCallbackEvent return true for a flagged event (MINIMAP_PING) and false for an unflagged one (PLAYER_LOGIN)?",
  run = function()
    local fn = ns.G("C_EventUtils.IsCallbackEvent")
    if type(fn) ~= "function" then return { api = "C_EventUtils.IsCallbackEvent absent" } end
    local out = {}
    local ok1, r1 = pcall(fn, "MINIMAP_PING")
    out.MINIMAP_PING = ok1 and tostring(r1) or ("errored: " .. tostring(r1))
    local ok2, r2 = pcall(fn, "PLAYER_LOGIN")
    out.PLAYER_LOGIN = ok2 and tostring(r2) or ("errored: " .. tostring(r2))
    return out
  end,
}

ns.Test{
  id = "unregister-event-callback", anchor = "api-events-and-discovery.md:389", bucket = "call",
  question = "Does Frame:UnregisterEventCallback exist as a frame method, and what is its arity? Only one call site in the whole checkout, no doc entry, no wiki page.",
  run = function()
    local f = CreateFrame("Frame")
    local m = f.UnregisterEventCallback
    local out = { methodType = type(m) }
    if type(m) == "function" then
      -- Arity is unknown; a bad-arity call records the error AS the answer.
      local ok, err = pcall(m, f, "PLAYER_LOGIN")
      out.calledOk = ok
      if not ok then out.err = tostring(err) end
    end
    return out
  end,
}

ns.Test{
  id = "event-profiler-api", anchor = "api-events-and-discovery.md:893", bucket = "call",
  question = "Do GetCurrentEventID() and GetEventTime(idx) exist and return anything useful from an addon, called outside a handler? Zero call sites in the shipped Lua.",
  run = function()
    local getID = ns.G("GetCurrentEventID")
    local getTime = ns.G("GetEventTime")
    local out = { GetCurrentEventID = type(getID), GetEventTime = type(getTime) }
    if type(getID) == "function" then
      local ok, res = pcall(getID)
      out.currentEventID = ok and tostring(res) or ("errored: " .. tostring(res))
    end
    if type(getTime) == "function" then
      -- With no valid eventProfileIndex to hand, 0 is the natural probe; recording
      -- the error is the finding (the pair is unusable without a profiling CVar).
      local ok, res = pcall(getTime, 0)
      out.eventTime0 = ok and tostring(res) or ("errored: " .. tostring(res))
    end
    return out
  end,
}

ns.Test{
  id = "register-unit-event-cap", anchor = "api-events-and-discovery.md:200", bucket = "call",
  question = "Is RegisterUnitEvent's documented four-unit cap real? The generated docs express the unit parameter as an unbounded variadic.",
  run = function()
    local f = CreateFrame("Frame")
    -- Register with FIVE units and record whether the call raised.  A silent cap
    -- and a hard error are different worlds; distinguish them.
    local ok, err = pcall(f.RegisterUnitEvent, f, "UNIT_HEALTH",
      "player", "target", "focus", "pet", "mouseover")
    local out = { fiveUnitsCallOk = ok }
    if not ok then out.err = tostring(err) end
    f:UnregisterAllEvents()
    return out
  end,
}

ns.Test{
  id = "secure-hooks-allowed-flag", anchor = "api-events-and-discovery.md:959", bucket = "call",
  question = "What does the SecureHooksAllowed=false annotation do? hooksecurefunc a function carrying it (CreateFromMixins) and see whether the hook is refused.",
  run = function()
    local target = ns.G("CreateFromMixins")
    if type(target) ~= "function" then return { api = "CreateFromMixins absent" } end
    -- hooksecurefunc(name, hook): install a post-hook on the GLOBAL by name so we
    -- don't need to pass the function value.  Record whether it installs.
    local ok, err = pcall(hooksecurefunc, "CreateFromMixins", function() end)
    return { hookInstalledOk = ok, err = (not ok) and tostring(err) or nil }
  end,
}

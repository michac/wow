-- T_ApiEvents.lua — tests anchored in knowledge/addon-dev/api-events-and-discovery.md.
local ADDON, ns = ...

--------------------------------------------------------------------------------
-- Observational probes.
--
-- The questions below ask what the client DOES OVER TIME, which no single call
-- can answer.  Each therefore ARMS on its first run and REPORTS on a later one,
-- and a probe that is unarmed, still running, or that nothing has fired at
-- returns measured=false with the reason: a zero count must never read as "it
-- never happens".  Probe frames are parented to UIParent and hidden; every
-- OnUpdate this file installs is cleared again on a timer.
--------------------------------------------------------------------------------

local function since(t) return string.format("%.0fs", GetTime() - t) end

-- 2.4 SynchronousEvent / UniqueEvent ------------------------------------------
ns.Test{
  id = "synchronous-event-semantics", anchor = "api-events-and-discovery.md:279", bucket = "event",
  blocked = "a runtime predicate for the flags — nothing exposes SynchronousEvent/"
    .. "UniqueEvent the way C_EventUtils.IsCallbackEvent exposes CallbackEvent, so even a "
    .. "positive observation could not be tied to a flag",
  question = "What do the SynchronousEvent / UniqueEvent flags mean? Neither string is documented anywhere reachable — not the generated docs, not Blizzard_EventTrace, not the wiki.",
  run = function()
    -- Separating inline dispatch from queued dispatch needs an event this addon can
    -- RAISE from a known call frame, and there is no such raiser: the candidates
    -- either write client state (SetCVar, LoadAddOn) or are server round trips
    -- (addon messages, item-data loads) whose latency is indistinguishable from
    -- queueing.  The one thing here that IS measurable is whether the client exposes
    -- a predicate for these flags the way C_EventUtils.IsCallbackEvent exposes
    -- CallbackEvent — such a predicate would be the whole answer.
    local utils = ns.G("C_EventUtils")
    local members = {}
    if type(utils) == "table" then
      pcall(function()
        for k in pairs(utils) do members[#members + 1] = tostring(k) end
      end)
      table.sort(members)
    end
    return {
      measured = false,
      why = "no honest instrument: no runtime predicate exposes the two flags (see eventUtilsMembers), and no event can be raised from a known call frame without either changing client state or going through the server, which would confound queueing with latency",
      eventUtilsMembers = (#members > 0) and table.concat(members, ", ")
        or "C_EventUtils absent or not enumerable",
    }
  end,
}

-- 2.5 The leading _nilOwner argument ------------------------------------------
-- Only CallbackEvent-flagged events are accepted.  The COMBAT_LOG_* four are left
-- out: they carry HasRestrictions and one of them fires thousands of times a pull.
-- TOOLTIP_SHOW_ITEM_COMPARISON is the one a human can raise on purpose (shift-hover
-- an item).  MINIMAP_PING carries SecretPayloads, so every argument is classified
-- through IsSecret before anything touches it.
local CB_EVENTS = {
  "TOOLTIP_SHOW_ITEM_COMPARISON", "MINIMAP_PING",
  "CLASS_TALENTS_SWITCH_TO_LOADOUT_BY_NAME", "CLASS_TALENTS_SWITCH_TO_LOADOUT_BY_INDEX",
  "CLASS_TALENTS_SWITCH_TO_SPECIALIZATION_BY_NAME", "CLASS_TALENTS_SWITCH_TO_SPECIALIZATION_BY_INDEX",
}
local CB_MAX_SAMPLES = 6
local cb
local cbFns = {}

local function argKind(v)
  if ns.IsSecret(v) then return "<secret>" end
  local ok, t = pcall(type, v)
  return ok and t or "type() errored"
end

local function armEventCallback()
  local st = { armedAt = GetTime(), fired = 0, samples = {}, disarmed = false }
  local reg = ns.G("RegisterEventCallback")
  st.globalApi = type(reg)

  local f = CreateFrame("Frame", nil, UIParent)
  f:Hide()
  st.frameApi = type(f.RegisterEventCallback)

  local function hit(form, event, isFrameForm, ...)
    st.fired = st.fired + 1
    if #st.samples >= CB_MAX_SAMPLES then return end
    local n = select("#", ...)
    local a1 = ...
    local row = string.format("%s %s args=%d arg1=%s", form, event, n, argKind(a1))
    if isFrameForm then
      -- The hypothesis the shipped `_nilOwner` name invites: the Frame: form may pass
      -- the frame as owner where the global form has nobody to pass.
      local okEq, isSelf = pcall(rawequal, a1, f)
      row = row .. " arg1IsOwnFrame=" .. (okEq and tostring(isSelf) or "compare errored")
    end
    st.samples[#st.samples + 1] = row
  end

  for _, ev in ipairs(CB_EVENTS) do
    local gfn = function(...) hit("global", ev, false, ...) end
    cbFns[ev] = gfn
    if type(reg) == "function" then pcall(reg, ev, gfn) end
    if type(f.RegisterEventCallback) == "function" then
      pcall(f.RegisterEventCallback, f, ev, function(...) hit("frame", ev, true, ...) end)
    end
  end
  return st
end

ns.Test{
  id = "event-callback-nil-owner", anchor = "api-events-and-discovery.md:1259", bucket = "event",
  question = "Is the leading _nilOwner argument to a RegisterEventCallback handler a contract, or six consistent conventions? Is it ever non-nil?",
  run = function()
    if not cb then
      cb = armEventCallback()
      return {
        measured = false,
        why = "probe armed this run on " .. #CB_EVENTS .. " CallbackEvent events — shift-hover an item to raise TOOLTIP_SHOW_ITEM_COMPARISON, then /clab run again",
        globalApi = cb.globalApi, frameApi = cb.frameApi,
        events = table.concat(CB_EVENTS, ", "),
      }
    end
    if cb.fired == 0 then
      return { measured = false,
               why = "no CallbackEvent has fired in " .. since(cb.armedAt)
                 .. " — shift-hover an item (TOOLTIP_SHOW_ITEM_COMPARISON) or ping the minimap, then re-run",
               globalApi = cb.globalApi, frameApi = cb.frameApi }
    end
    -- Disarm the global form once a sample exists: it takes the callback value back,
    -- and we kept the reference for exactly this.  The Frame: form has no working
    -- unregister (Frame:UnregisterEventCallback reads nil), so that listener stays.
    if not cb.disarmed and #cb.samples > 0 then
      local unreg = ns.G("UnregisterEventCallback")
      if type(unreg) == "function" then
        for _, ev in ipairs(CB_EVENTS) do pcall(unreg, ev, cbFns[ev]) end
        cb.disarmed = true
      end
    end
    return {
      window = since(cb.armedAt),
      firings = cb.fired,
      samples = table.concat(cb.samples, " | "),
      globalApi = cb.globalApi, frameApi = cb.frameApi,
      globalFormDisarmed = cb.disarmed,
    }
  end,
}

-- TRAIT_CONFIG_UPDATED on a hero-tree swap ------------------------------------
-- The only always-on listener in the file, and it has to be: a swap happens when the
-- player swaps, not when a test runs, so the accumulator is installed at load and the
-- test reports what it has collected.  The COUNT is the finding as much as the fact —
-- anything these events drive must be idempotent — so every firing is tallied and the
-- hero spec is read beside it.
local TRAIT_EVENTS = { "TRAIT_CONFIG_UPDATED", "PLAYER_SPECIALIZATION_CHANGED", "PLAYER_TALENT_UPDATE" }
local TRAIT_MAX_LOG = 40
local trait = { armedAt = GetTime(), total = 0, counts = {}, log = {}, heroes = {}, heroCount = 0 }

local function heroSpec()
  local fn = ns.G("C_ClassTalents.GetActiveHeroTalentSpec")
  if type(fn) ~= "function" then return "api absent" end
  local ok, id = pcall(fn)
  if not ok then return "errored" end
  if id == nil then return "none" end
  return id
end

do
  -- Pre-seeded to zero so that once ANYTHING has fired, an event sitting at 0 is a
  -- reading rather than an absent key.
  for _, ev in ipairs(TRAIT_EVENTS) do trait.counts[ev] = 0 end
  local f = CreateFrame("Frame", nil, UIParent)
  f:Hide()
  for _, ev in ipairs(TRAIT_EVENTS) do f:RegisterEvent(ev) end
  f:SetScript("OnEvent", function(_, event)
    local hero = tostring(heroSpec())
    trait.total = trait.total + 1
    trait.counts[event] = (trait.counts[event] or 0) + 1
    if not trait.heroes[hero] then
      trait.heroes[hero] = true
      trait.heroCount = trait.heroCount + 1
    end
    if #trait.log < TRAIT_MAX_LOG then
      trait.log[#trait.log + 1] = string.format("+%.1fs %s hero=%s", GetTime() - trait.armedAt, event, hero)
    end
  end)
end

ns.Test{
  id = "traitconfig-fires-on-hero-swap", anchor = "../../knowledge/_meta/kb-inbox.md:140", bucket = "call",
  question = "Does TRAIT_CONFIG_UPDATED fire on a HERO-TREE swap (a build change with no spec change), and HOW MANY TIMES per swap? PLAYER_SPECIALIZATION_CHANGED demonstrably does not.",
  run = function()
    -- The gate is A SWAP HAVING HAPPENED, not "some event fired".  PLAYER_TALENT_UPDATE
    -- fires on its own several times a session, so a `total > 0` gate lets the test
    -- report TRAIT_CONFIG_UPDATED = 0 from a session where nothing was ever swapped —
    -- which reads as "it does not fire on a hero swap" and is the exact false claim this
    -- test exists to avoid. Two distinct hero values is the evidence that a swap occurred.
    if trait.heroCount < 2 then
      return { measured = false,
               why = "no hero-tree swap observed this session (hero has read "
                 .. trait.heroCount .. " distinct value(s)), so the counts below say "
                 .. "nothing about what a swap does — swap hero tree, then re-run",
               counts = trait.counts, heroNow = tostring(heroSpec()),
               window = since(trait.armedAt) }
    end
    return {
      window = since(trait.armedAt),
      total = trait.total,
      counts = trait.counts,
      heroNow = tostring(heroSpec()),
      distinctHeroValues = trait.heroCount,
      log = table.concat(trait.log, " | "),
      logTruncated = #trait.log >= TRAIT_MAX_LOG,
    }
  end,
}

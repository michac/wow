-- T_CooldownReadiness.lua — "is this ability on cooldown?", asked six ways.
--
-- WHY THIS FILE EXISTS. cap shipped a readiness latch fed by the Cooldown Manager's alert
-- edges. On 2026-08-16 a Havoc flight measured 320 `OnCooldown` edges across 8 rows and 35
-- `Available` edges on ONE row — the only row with an alert configured — so the latch went
-- down and never came back and every icon wore a permanent cooldown treatment.
--
-- The cause is in the source: `Available` is raised from `CooldownViewerItemMixin:OnUpdate`,
-- and the viewer only ticks frames `NeedsOnUpdateRegistration()` accepts, which is true only
-- when the player configured an alert. `OnCooldown` comes from the data-refresh path and is
-- unconditional. The channel is asymmetric by construction.
--
-- So cap needs a readiness answer that is NOT an edge latch. Every test here measures one
-- candidate route, and the first two are the ones cap is already built on.
local ADDON, ns = ...

local ESSENTIAL = "EssentialCooldownViewer"

-- One classified read. `pcall` first because a secret comparison THROWS rather than
-- returning, and a throw is itself the measurement.
local function classify(fn, ...)
  local ok, v = pcall(fn, ...)
  if not ok then return "threw" end
  if ns.IsSecret(v) then return "secret" end
  local t = type(v)
  if t == "boolean" then return tostring(v) end
  if t == "number" then return "number" end
  if t == "nil" then return "nil" end
  return t
end

local function viewer()
  return ns.G(ESSENTIAL)
end

--- Every laid-out item frame on the Essential viewer, or an empty list.
local function items()
  local v = viewer()
  if not v or type(v.GetItemFrames) ~= "function" then return {} end
  local ok, frames = pcall(v.GetItemFrames, v)
  if not ok or type(frames) ~= "table" then return {} end
  return frames
end

--- `n` rows summarised as counts of each classification, which is the shape that answers
--- "is this readable" without persisting a value per row.
local function tally(frames, read)
  local out, n = {}, 0
  for _, frame in ipairs(frames) do
    n = n + 1
    local k = read(frame)
    out[k] = (out[k] or 0) + 1
  end
  out.rows = n
  return out
end

-- ---------------------------------------------------------------------------
-- 1 · the read cap is now built on
-- ---------------------------------------------------------------------------

ns.Test{
  id = "cdm-cooldown-widget-shown-in-combat",
  anchor = "cooldown-manager.md:§7",
  bucket = "secret",
  phase = "combat",
  question = "Is the item's Cooldown widget `IsShown()` a plain boolean in restricted combat, "
    .. "and does `wasSetFromCooldown` stay plain beside it? Together they are cap's "
    .. "'is this row's own cooldown running' gate.",
  run = function()
    local frames = items()
    if #frames == 0 then return { measured = false, why = "no Essential rows laid out" } end
    return {
      shown = tally(frames, function(frame)
        if type(frame.GetCooldownFrame) ~= "function" then return "no-accessor" end
        local ok, cd = pcall(frame.GetCooldownFrame, frame)
        if not ok or type(cd) ~= "table" then return "no-widget" end
        return classify(cd.IsShown, cd)
      end),
      wasSetFromCooldown = tally(frames, function(frame)
        local v = frame.wasSetFromCooldown
        if ns.IsSecret(v) then return "secret" end
        return type(v) == "boolean" and tostring(v) or type(v)
      end),
      combat = InCombatLockdown() and true or false,
    }
  end,
}

-- ---------------------------------------------------------------------------
-- 2 · the edge cap is now built on
-- ---------------------------------------------------------------------------

-- Armed once, then it listens. A hook cannot report on the pull that installed it, so the
-- counters live at file scope and the test reports whatever has accumulated.
local doneSeen, doneRows, alertSeen, hookedCount = 0, {}, 0, 0
local armed = setmetatable({}, { __mode = "k" })

local function arm()
  for _, frame in ipairs(items()) do
    if not armed[frame] then
      armed[frame] = true
      hookedCount = hookedCount + 1
      if type(frame.TriggerAlertEvent) == "function" then
        hooksecurefunc(frame, "TriggerAlertEvent", function()
          alertSeen = alertSeen + 1
        end)
      end
      if type(frame.GetCooldownFrame) == "function" then
        local ok, cd = pcall(frame.GetCooldownFrame, frame)
        if ok and type(cd) == "table" and type(cd.HookScript) == "function" then
          pcall(cd.HookScript, cd, "OnCooldownDone", function(self)
            doneSeen = doneSeen + 1
            local parent = self:GetParent()
            local okID, cid = pcall(parent.GetCooldownID, parent)
            if okID and type(cid) == "number" and not ns.IsSecret(cid) then
              doneRows[cid] = (doneRows[cid] or 0) + 1
            end
          end)
        end
      end
    end
  end
end

ns.Test{
  id = "cdm-oncooldowndone-fires-without-alerts",
  anchor = "cooldown-manager.md:§5.1",
  bucket = "event",
  phase = "combat",
  question = "Does `OnCooldownDone` on the item's Cooldown widget fire for rows the player "
    .. "configured NO alert on — i.e. is it the symmetric ready edge the alert channel "
    .. "cannot give us? Count distinct cooldownIDs, not just firings.",
  run = function()
    arm()
    local distinct = 0
    for _ in pairs(doneRows) do distinct = distinct + 1 end
    -- The comparison that answers it: `Available` reaches TriggerAlertEvent for configured
    -- rows only, so `distinct` well above that count is the finding.
    return {
      hooked = hookedCount, doneFirings = doneSeen, doneDistinctRows = distinct,
      alertFirings = alertSeen,
      measured = doneSeen > 0 or nil,
      why = doneSeen == 0 and "armed; no cooldown has completed yet — re-run after a pull" or nil,
    }
  end,
}

-- ---------------------------------------------------------------------------
-- 3 · the fields behind both, and whether any of them is cheaper
-- ---------------------------------------------------------------------------

ns.Test{
  id = "cdm-item-cooldown-flags-secrecy",
  anchor = "cooldown-manager.md:§7",
  bucket = "secret",
  phase = "combat",
  question = "Are `isOnActualCooldown`, `cooldownIsActive`, `isOnGCD` and the method "
    .. "`IsOnCooldown()` plain in restricted combat? They are Blizzard's own verdicts and "
    .. "would be a one-field answer if they survive.",
  run = function()
    local frames = items()
    if #frames == 0 then return { measured = false, why = "no Essential rows laid out" } end
    local function field(name)
      return tally(frames, function(frame)
        local v = frame[name]
        if ns.IsSecret(v) then return "secret" end
        return type(v) == "boolean" and tostring(v) or type(v)
      end)
    end
    return {
      isOnActualCooldown = field("isOnActualCooldown"),
      cooldownIsActive = field("cooldownIsActive"),
      isOnGCD = field("isOnGCD"),
      IsOnCooldown = tally(frames, function(frame)
        if type(frame.IsOnCooldown) ~= "function" then return "no-method" end
        return classify(frame.IsOnCooldown, frame)
      end),
      combat = InCombatLockdown() and true or false,
    }
  end,
}

-- ---------------------------------------------------------------------------
-- 4 · the documented pattern we have never measured ourselves
-- ---------------------------------------------------------------------------

local scratchParent = CreateFrame("Frame")
scratchParent:Hide()
local scratch = CreateFrame("Cooldown", nil, scratchParent, "CooldownFrameTemplate")

ns.Test{
  id = "cdm-scratch-cooldown-isshown",
  anchor = "cdm-rider-patterns.md:§2.3",
  bucket = "secret",
  phase = "combat",
  question = "The scratch-frame pattern: feed a duration object to a hidden Cooldown widget "
    .. "and read `IsShown()`. §2.3 states this is a plain boolean even when the time is "
    .. "secret, but that is another addon's claim and we have never measured it.",
  run = function()
    local get = ns.G("C_Spell.GetSpellCooldownDuration")
    if type(get) ~= "function" then return { measured = false, why = "no GetSpellCooldownDuration" } end
    if type(scratch.SetCooldownFromDurationObject) ~= "function" then
      return { measured = false, why = "widget has no SetCooldownFromDurationObject" }
    end
    local frames = items()
    if #frames == 0 then return { measured = false, why = "no Essential rows laid out" } end

    local out = { rows = 0 }
    for _, frame in ipairs(frames) do
      local okID, spellID = pcall(frame.GetBaseSpellID, frame)
      if okID and type(spellID) == "number" and not ns.IsSecret(spellID) then
        out.rows = out.rows + 1
        local okDur, dur = pcall(get, spellID, true)
        if not okDur or dur == nil then
          out.noDuration = (out.noDuration or 0) + 1
        else
          local okSet = pcall(scratch.SetCooldownFromDurationObject, scratch, dur)
          if not okSet then
            out.setThrew = (out.setThrew or 0) + 1
          else
            local k = classify(scratch.IsShown, scratch)
            out[k] = (out[k] or 0) + 1
            pcall(scratch.SetCooldown, scratch, 0, 0)
          end
        end
      end
    end
    out.combat = InCombatLockdown() and true or false
    return out
  end,
}

-- ---------------------------------------------------------------------------
-- 5 · the route we chose NOT to take, measured anyway
-- ---------------------------------------------------------------------------

ns.Test{
  id = "cdm-forced-onupdate-registration",
  anchor = "cooldown-manager.md:§5.1",
  bucket = "call",
  phase = "manual",
  question = "Does calling `viewer:RegisterItemFrameForOnUpdate(item)` from addon code make "
    .. "`Available` fire for a row with no configured alert — without writing the player's "
    .. "saved layout or playing an alert? And does the viewer un-register it again?",
  run = function()
    if InCombatLockdown() then
      return { measured = false, why = "registration does a SetScript on the viewer; "
        .. "out of combat only until frame protection is settled" }
    end
    local v = viewer()
    if not v or type(v.RegisterItemFrameForOnUpdate) ~= "function" then
      return { measured = false, why = "no RegisterItemFrameForOnUpdate on the viewer" }
    end
    local frames = items()
    if #frames == 0 then return { measured = false, why = "no Essential rows laid out" } end

    local before = type(v.itemFramesNeedingOnUpdateMap) == "table" and 0 or nil
    if before then
      for _ in pairs(v.itemFramesNeedingOnUpdateMap) do before = before + 1 end
    end
    for _, frame in ipairs(frames) do pcall(v.RegisterItemFrameForOnUpdate, v, frame) end
    local after = type(v.itemFramesNeedingOnUpdateMap) == "table" and 0 or nil
    if after then
      for _ in pairs(v.itemFramesNeedingOnUpdateMap) do after = after + 1 end
    end
    return {
      rows = #frames, registeredBefore = before, registeredAfter = after,
      hasOnUpdateScript = v:GetScript("OnUpdate") ~= nil,
      -- The follow-on question a human answers by watching: did an alert SOUND or TEXT
      -- appear? It must not — `alertsByEvent` is empty, so TriggerAlertEvent plays nothing.
      note = "watch for alert sound/text; there should be none",
    }
  end,
}

-- ---------------------------------------------------------------------------
-- 6 · the long-open one, since we are here
-- ---------------------------------------------------------------------------

ns.Test{
  id = "cdm-item-frame-protected",
  anchor = "cooldown-manager.md:§4.1",
  bucket = "secret",
  phase = "combat",
  question = "Is a laid-out CDM item frame PROTECTED at runtime? The XML declares no "
    .. "`protected` attribute, but that settles the declaration, not the runtime — and 12.1.0 "
    .. "ships a `CooldownViewerSecure.lua`. cap re-anchors these frames and currently refuses "
    .. "to do so in combat out of caution rather than measurement.",
  run = function()
    local frames = items()
    if #frames == 0 then return { measured = false, why = "no Essential rows laid out" } end
    local v = viewer()
    return {
      combat = InCombatLockdown() and true or false,
      itemProtected = tally(frames, function(frame)
        if type(frame.IsProtected) ~= "function" then return "no-method" end
        local ok, protected, explicit = pcall(frame.IsProtected, frame)
        if not ok then return "threw" end
        return tostring(protected) .. "/" .. tostring(explicit)
      end),
      viewerProtected = v and type(v.IsProtected) == "function"
        and select(2, pcall(v.IsProtected, v)) or "no-method",
    }
  end,
}

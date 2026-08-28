-- T_AuraSink.lua — may a CustomAuraButton sink be re-called on a button that already has one?
--
-- ⚠ WHAT THIS CANNOT DO. Whether the NEW formatter's output reached a pixel is not readable:
-- the sink seals `Text` and `Shown`, so the drawn string is secret by construction. What is
-- readable is acceptance, refusal, and whether `GetApplicationCount` reports the second
-- FontString — which separates "overwrote the state" from "silently ignored" without needing
-- pixels. The pixel half is a human eyeball and is recorded as NOT MEASURED, never as a pass.
local ADDON, ns = ...

local TILE = 44

-- ⚠ Written out long on purpose. `ok and v or "…"` returns the fallback whenever `v` is
-- legitimately `false` or `nil`, which is half of what these getters are asked for.
local function describe(ok, v)
  if not ok then return "ERROR: " .. tostring(v) end
  if ns.IsSecret(v) then return "<secret>" end
  local t = type(v)
  if t == "nil" then return "nil" end
  if t == "boolean" then
    if v then return "true" end
    return "false"
  end
  if t == "number" then return string.format("%.4g", v) end
  if t == "string" then return v end
  return "<" .. t .. ">"
end

local host

local function ensureHost()
  if host then return host end
  host = CreateFrame("Frame", nil, UIParent)
  host:SetSize(TILE, TILE)
  host:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
  host:Hide()
  return host
end

--- A formatter whose bands make the two calls tell apart BY EYE: the first draws the numeral,
--- the second draws it wrapped in brackets. Nothing in Lua may compare them — the eyeball can.
local function formatter(wrap)
  local make = ns.G("C_StringUtil.CreateNumericRuleFormatter")
  if type(make) ~= "function" then return nil end
  local ok, f = pcall(make)
  if not (ok and f) then return nil end
  local set = pcall(f.SetBreakpoints, f, {
    { threshold = 0, format = "" },
    { threshold = 1, format = wrap and "[%d]" or "%d" },
  })
  if not set then return nil end
  return f
end

--- One call of the sink, recorded flat: accepted, refused with the message, or unavailable.
local function callSink(button, fs, fmt)
  if type(button.SetApplicationCount) ~= "function" then return "method absent" end
  if not fmt then return "no formatter" end
  local ok, err = pcall(button.SetApplicationCount, button, fs, { formatter = fmt })
  if ok then return "accepted" end
  return "REFUSED: " .. tostring(err)
end

ns.Test{
  id = "aura-sink-recall",
  anchor = "security-taint-and-restricted-data.md:1237",
  bucket = "call",
  question = "May SetApplicationCount be called a SECOND time on a button that already has an "
    .. "application count — on the same FontString and on a fresh one, with and without an "
    .. "intervening ClearApplicationCount — and in combat as well as out?",
  run = function()
    local log = { init = 0, combat = describe(true, InCombatLockdown()) }

    local ok, container = pcall(CreateFrame, "AuraContainer", nil, ensureHost(),
                                "CustomAuraContainerTemplate")
    if not ok or not container then
      return {
        measured = false,
        container = "FAILED: " .. tostring(container),
        why = "no container, so nothing about the sink was exercised.",
      }
    end
    container:SetAllPoints(host)

    local slotOk, slotFrame = pcall(function()
      return container:AddAuraSlot("recall", "HELPFUL", {
        candidateFilters = { isFromPlayerOrPlayerPet = true },
        initializeFrame = function(button)
          log.init = log.init + 1
          button:SetSize(TILE, TILE)
          button:SetAllPoints(container)

          -- Four calls, four separate records. The interesting one is `second`: the same
          -- FontString goes back through `ValidateInboundScriptObject` and then through
          -- `AddSecretAspect`/`AddForbiddenAspects` a second time, on a region those calls
          -- have already sealed.
          local a = button:CreateFontString(nil, "OVERLAY", "NumberFontNormal")
          a:SetPoint("CENTER")
          log.first = callSink(button, a, formatter(false))
          log.readAfterFirst = describe(pcall(button.GetApplicationCount, button))

          log.second = callSink(button, a, formatter(true))
          log.readAfterSecond = describe(pcall(button.GetApplicationCount, button))

          local b = button:CreateFontString(nil, "OVERLAY", "NumberFontNormal")
          b:SetPoint("CENTER")
          log.thirdNewString = callSink(button, b, formatter(true))

          if type(button.ClearApplicationCount) == "function" then
            local cOk, cErr = pcall(button.ClearApplicationCount, button)
            if cOk then log.clear = "accepted" else log.clear = "REFUSED: " .. tostring(cErr) end
            log.readAfterClear = describe(pcall(button.GetApplicationCount, button))
            log.fourthAfterClear = callSink(button, b, formatter(false))
          else
            log.clear = "method absent"
          end
        end,
      })
    end)
    if slotOk then log.slot = type(slotFrame) else log.slot = "FAILED: " .. tostring(slotFrame) end

    local uOk, uErr = pcall(container.SetUnit, container, "player")
    if uOk then log.setUnit = "ok" else log.setUnit = "FAILED: " .. tostring(uErr) end
    local aOk, aErr = pcall(container.UpdateAllAuras, container)
    if aOk then log.updateAllAuras = "ok" else log.updateAllAuras = "FAILED: " .. tostring(aErr) end

    -- `initializeFrame` fires at slot-creation time on a batchSize=1 provider, so 0 means the
    -- slot never built and every field above is about nothing.
    if log.init == 0 then
      log.measured = false
      log.why = "initializeFrame never ran, so no sink call was made."
      return log
    end

    log.measured = true
    log.eyeball = "NOT MEASURED: whether the SECOND formatter's output is what draws. The sink "
      .. "seals Text, so no getter reports the string. Put a stacking player buff up with the "
      .. "host shown and read the numeral: bare digits = the first formatter still owns it, "
      .. "digits in [brackets] = the re-call took effect."
    log.why = "Acceptance, refusal and GetApplicationCount read-backs only, for four call "
      .. "shapes; the combat field says which pass this run was."
    return log
  end,
}

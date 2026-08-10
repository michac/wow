-- CDMSweep — a generic value + event reader for every Cooldown Manager row.
--
-- It probes and records; it never judges.  Every expression the CDM exposes is read,
-- classified by READABILITY, and written to a capture a human reads later.
--
-- Not a ns.Test{}: it registers no ids, so the questions.json cross-check is untouched.
-- It calls no setter, writes no field onto a Blizzard frame, and resolves every game
-- global by string through ns.G.

local ADDON, ns = ...

local sweepLog = ns.Capture.Open("cdmsweep", { sessions = 3, cap = 3000 })
local eventLog = ns.Capture.Open("cdmevent", { sessions = 3, cap = 4000 })

local MAX_SWEEPS = 6
local EVENT_BUDGET = 40
local EDGE_BUDGET = 400
local STR_MAX = 70
local LIST_MAX = 24

-- The classifier -------------------------------------------------------------
-- One route for every probe, because the three ways to lose are all here: formatting a
-- Secret Value taints, `nil` and "returned nothing" are different answers, and a throw
-- is itself a measurement.  So: pcall -> IsSecret -> IsSecretTable -> type -> render,
-- with ns.Capture.Safe doing the final rendering of any plain value.

local function flat(s)
  s = s:gsub("[\r\n\t]+", " ")
  if #s > STR_MAX then s = s:sub(1, STR_MAX) .. ".." end
  return s
end

local function One(v)
  if v == nil then return "nil" end
  if ns.IsSecret(v) then return "secret" end
  if ns.IsSecretTable(v) then return "secrettable" end
  local t = type(v)
  if t == "string" then return "s:" .. flat(ns.Capture.Safe(v)) end
  if t == "table" then
    local ok, n = pcall(function() return #v end)
    return "t:" .. (ok and tostring(n) or "?")
  end
  return ns.Capture.Safe(v)
end

local function errStr(e)
  if e == nil then return "!err:nil" end
  if ns.IsSecret(e) then return "!err:secret" end
  local ok, s = pcall(tostring, e)
  return ok and ("!err:" .. flat(s)) or "!err:unrenderable"
end

--- Takes (ok, ...) straight from pcall.  First return value only.
local function Class(ok, ...)
  local n = select("#", ...)
  if not ok then return errStr(...) end
  if n == 0 then return "!nothing" end
  return One((...))
end

--- Same, but every return value, joined — for the two-return getters.
local function ClassAll(ok, ...)
  local n = select("#", ...)
  if not ok then return errStr(...) end
  if n == 0 then return "!nothing" end
  local parts = {}
  for i = 1, n do parts[i] = One((select(i, ...))) end
  return table.concat(parts, "|")
end

--- Class plus the live value, so a struct is classified and then walked field by field
--- without calling the API twice.  A secret never comes back out.
local function ClassKeep(ok, ...)
  local n = select("#", ...)
  if not ok then return errStr(...), nil end
  if n == 0 then return "!nothing", nil end
  local v = (...)
  local cls = One(v)
  if cls == "secret" or cls == "secrettable" then return cls, nil end
  return cls, v
end

--- A string return recorded as class + LENGTH.  The payload is not the evidence; its
--- readability and its size are, and a serialized blob has no business in a capture.
local function ClassLen(ok, ...)
  local n = select("#", ...)
  if not ok then return errStr(...), -1 end
  if n == 0 then return "!nothing", -1 end
  local v = (...)
  if v == nil then return "nil", -1 end
  if ns.IsSecret(v) then return "secret", -1 end
  if ns.IsSecretTable(v) then return "secrettable", -1 end
  if type(v) == "string" then return "string", #v end
  return "<" .. type(v) .. ">", -1
end

local function index(t, k) return t[k] end

local function Field(tbl, key)
  if type(tbl) ~= "table" then return "!skip:not a table" end
  if ns.IsSecretTable(tbl) then return "!skip:secret table" end
  return Class(pcall(index, tbl, key))
end

local function RawField(tbl, key)
  if type(tbl) ~= "table" or ns.IsSecretTable(tbl) then return nil end
  local ok, v = pcall(index, tbl, key)
  if not ok or ns.IsSecret(v) then return nil end
  return v
end

local function ClassEach(tbl, keys)
  local out = {}
  for _, k in ipairs(keys) do out[k] = Field(tbl, k) end
  return out
end

local function KeyList(tbl)
  if type(tbl) ~= "table" or ns.IsSecretTable(tbl) then return "" end
  local out = {}
  local ok = pcall(function()
    for k in pairs(tbl) do out[#out + 1] = tostring(k) end
  end)
  if not ok then return "!err:pairs" end
  table.sort(out)
  return table.concat(out, ",")
end

--- Keys the client hands back that the generated docs do not promise.
local function ExtraKeys(tbl, known)
  if type(tbl) ~= "table" or ns.IsSecretTable(tbl) then return "" end
  local set = {}
  for _, k in ipairs(known) do set[k] = true end
  local out = {}
  local ok = pcall(function()
    for k in pairs(tbl) do
      if type(k) == "string" and not set[k] then out[#out + 1] = k end
    end
  end)
  if not ok then return "!err:pairs" end
  table.sort(out)
  return table.concat(out, ",")
end

local function ListStr(t)
  if t == nil then return "nil" end
  if ns.IsSecret(t) then return "secret" end
  if ns.IsSecretTable(t) then return "secrettable" end
  if type(t) ~= "table" then return One(t) end
  local out, n = {}, 0
  local ok = pcall(function()
    for i, v in ipairs(t) do
      n = i
      if i <= LIST_MAX then out[#out + 1] = One(v) end
    end
  end)
  if not ok then return "!err:ipairs" end
  local s = table.concat(out, ",")
  if n > LIST_MAX then s = s .. ",+" .. (n - LIST_MAX) end
  return "n=" .. n .. "[" .. s .. "]"
end

local function CountOf(t)
  if type(t) ~= "table" or ns.IsSecretTable(t) then return -1 end
  local n = 0
  local ok = pcall(function() for _ in ipairs(t) do n = n + 1 end end)
  return ok and n or -1
end

local function IsObject(o) local t = type(o); return t == "table" or t == "userdata" end

local function Method(obj, name, ...)
  if not IsObject(obj) then return "!skip:no object" end
  if ns.IsSecretTable(obj) then return "!skip:secret table" end
  local okG, fn = pcall(index, obj, name)
  if not okG then return errStr(fn) end
  if type(fn) ~= "function" then return "!skip:no method" end
  return ClassAll(pcall(fn, obj, ...))
end

local function RawMethod(obj, name, ...)
  if not IsObject(obj) or ns.IsSecretTable(obj) then return nil end
  local okG, fn = pcall(index, obj, name)
  if not okG or type(fn) ~= "function" then return nil end
  local ok, v = pcall(fn, obj, ...)
  if not ok or ns.IsSecret(v) then return nil end
  return v
end

local function MethodEach(obj, names, ...)
  local out = {}
  for _, n in ipairs(names) do out[n] = Method(obj, n, ...) end
  return out
end

local ABSENT = "!skip:absent"

local function Fn(path) local f = ns.G(path); return type(f) == "function" and f or nil end

--- Both halves of ns.GlobalType, rendered `<_G>/<addon env>`. The two can differ and
--- that difference is sometimes the answer, so neither half is dropped.
local function globalType(path)
  local t = ns.GlobalType(path)
  return t.g .. "/" .. t.env
end

local function Call(path, ...)
  local f = Fn(path)
  if not f then return ABSENT end
  return ClassAll(pcall(f, ...))
end

--- Class + live value for an already-resolved function, so an absent API reads as a skip
--- rather than as a throw from a call that never happened.
local function KeepCall(f, ...)
  if type(f) ~= "function" then return ABSENT, nil end
  return ClassKeep(pcall(f, ...))
end

local function KeepMethod(obj, name, ...)
  if not IsObject(obj) then return "!skip:no object", nil end
  if ns.IsSecretTable(obj) then return "!skip:secret table", nil end
  local okG, fn = pcall(index, obj, name)
  if not okG then return errStr(fn), nil end
  if type(fn) ~= "function" then return "!skip:no method", nil end
  return ClassKeep(pcall(fn, obj, ...))
end

local function LenCall(f, ...)
  if type(f) ~= "function" then return ABSENT, -1 end
  return ClassLen(pcall(f, ...))
end

local function PlainNumber(v)
  if v == nil or ns.IsSecret(v) then return nil end
  return type(v) == "number" and v or nil
end

-- The probe sets -------------------------------------------------------------

local VIEWERS = {
  "EssentialCooldownViewer", "UtilityCooldownViewer",
  "BuffIconCooldownViewer", "BuffBarCooldownViewer",
}

local ENUMS = {
  "Enum.CooldownViewerCategory", "Enum.CooldownSetSpellFlags",
  "Enum.CooldownSetLinkedSpellFlags", "Enum.CooldownViewerAlertEventType",
  "Enum.CooldownViewerAlertType", "Constants.CooldownViewerUIConstants",
}

local INFO_FIELDS = {
  "cooldownID", "spellID", "overrideSpellID", "overrideTooltipSpellID", "linkedSpellIDs",
  "selfAura", "hasAura", "charges", "isKnown", "flags", "category",
}
local RUNG_FIELDS = {
  "cooldownID", "spellID", "overrideSpellID", "overrideTooltipSpellID", "linkedSpellIDs",
}

local F_CACHE = {
  "cooldownEnabled", "cooldownStartTime", "cooldownDuration", "cooldownModRate",
  "cooldownSwipeColor", "cooldownDesaturated", "cooldownShowDrawEdge", "cooldownShowSwipe",
  "cooldownUseAuraDisplayTime", "cooldownPlayFlash", "cooldownPaused",
}
local F_STATE = {
  "isOnGCD", "cooldownIsActive", "isOnActualCooldown", "allowAvailableAlert",
  "allowOnCooldownAlert", "availableAlertTriggerTime",
}
local F_SOURCE = { "wasSetFromCharges", "wasSetFromCooldown", "wasSetFromAura", "wasSetFromEditMode" }
local F_SHOWN = { "isActive", "hideWhenInactive", "allowHideWhenInactive", "needsFullRefresh", "isEditing" }
local F_RANGE = { "needsRangeCheck", "rangeCheckSpellID", "spellOutOfRange" }
local F_CHARGE = { "cooldownChargesCount", "cooldownChargesShown", "previousCooldownChargesCount" }
local F_PANDEMIC = {
  "pandemicAlertTriggerTime", "pandemicStartTime", "pandemicEndTime",
  "nextAvailableTimeToPlayPandemicAlert",
}
local F_AURA = { "auraSpellID", "auraInstanceID", "auraDataUnit" }

local AURA_FIELDS = {
  "expirationTime", "duration", "timeMod", "applications", "auraInstanceID",
  "spellId", "sourceUnit", "name",
}
local CD_INFO_FIELDS = {
  "startTime", "duration", "isEnabled", "isActive", "modRate",
  "activeCategory", "timeUntilEndOfStartRecovery", "isOnGCD",
}
local CHARGE_INFO_FIELDS = {
  "currentCharges", "maxCharges", "cooldownStartTime", "cooldownDuration",
  "chargeModRate", "isActive",
}

local M_IDENT = {
  "GetCooldownID", "GetCooldownInfo", "GetBaseSpellID", "GetSpellID", "GetLinkedSpell",
  "GetNameText", "GetSpellTexture", "HasEditModeData", "IsEditing",
}
local M_STATE = {
  "GetSpellCooldownInfo", "IsActive", "IsExpired", "IsDirty", "IsTimerShown", "IsShown",
  "IsVisible", "ShouldBeShown", "IsUsingVisualDataSource_Spell",
  "IsUsingVisualDataSource_Any", "HasVisualDataSource_Charges", "IsActivelyCast",
}
local M_AURA = {
  "GetAuraSpellID", "GetAuraSpellInstanceID", "GetAuraDataCached",
  "GetAuraDataUnit", "CanUseAuraForCooldown", "GetTotemData", "GetTotemSlot",
  "GetPandemicAlertTriggerTime",
}
local M_CHARGE = { "GetSpellChargeInfo", "GetApplicationsText" }
local M_WIDGET = { "GetCooldownFrame", "GetIconTexture" }

--- Eight named getters are NOT called, because none is a pure read.  GetAuraData and
--- GetCooldownValues assign auraDataCached/auraDataUnit; ShouldBeActive assigns
--- linkedSpellID and needsFullRefresh; the three alert getters create validAlertTypes;
--- and GetCurrentPlayerTotemCache / GetPreferredTotemSlotInfo rebuild a MODULE-LOCAL
--- totem cache that Blizzard's own refresh path reads on every refresh -- shared state
--- is subject state, not just a frame field.  The underlying fields are read instead.
local NOT_CALLED = "GetAuraData GetCooldownValues ShouldBeActive GetValidAlertTypes "
  .. "CanTriggerAnyAlertType GetFirstValidAlertType GetCurrentPlayerTotemCache "
  .. "GetPreferredTotemSlotInfo"

local CD_GETTERS = {
  "GetCooldownTimes", "GetCooldownDuration", "GetCooldownDisplayDuration",
  "GetDrawSwipe", "GetDrawEdge", "GetDrawBling", "GetReverse", "GetEdgeScale",
  "GetHideCountdownNumbers", "GetCountdownAbbrevThreshold", "GetMinimumCountdownDuration",
  "GetCountdownMillisecondsThreshold", "GetCountdownFormatter",
}

local DUR_METHODS = {
  "HasSecretValues", "GetRemainingDuration", "GetTotalDuration", "GetElapsedDuration",
  "GetStartTime", "GetEndTime", "GetRemainingPercent", "GetElapsedPercent",
  "GetClockTime", "GetModRate", "IsZero", "IsActive", "HasStarted", "HasExpired",
}

local UNIT_EVENTS = { UNIT_AURA = { "player", "target" }, UNIT_TARGET = { "player" } }
local PLAIN_EVENTS = {
  "PLAYER_IN_COMBAT_CHANGED", "PLAYER_LEVEL_CHANGED",
  "COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED", "SPELL_UPDATE_COOLDOWN", "SPELL_UPDATE_ICON",
  "PLAYER_TOTEM_UPDATE", "SPELL_ACTIVATION_OVERLAY_GLOW_SHOW",
  "SPELL_ACTIVATION_OVERLAY_GLOW_HIDE", "SPELL_UPDATE_USES", "SPELL_UPDATE_USABLE",
  "SPELL_RANGE_CHECK_UPDATE", "COOLDOWN_VIEWER_DATA_LOADED", "COOLDOWN_VIEWER_TABLE_HOTFIXED",
}

-- Row plumbing ---------------------------------------------------------------
-- Unchanged rows are dropped so six sweeps of a static bar do not bury the one row that
-- moved.  The signature is taken before `sweep`/`at` are stamped, and the whole table
-- resets on a combat-state or build change, so the first sweep after either writes
-- everything -- the two edges across which an identical-looking row is a different fact.

local ALWAYS = { sweep = true, env = true, event = true, alertedge = true }

local sweepN, rowsWritten, skippedUnchanged = 0, 0, 0
local sigs, lastCombat, lastBuild, capAnnounced = {}, nil, nil, false

local function rowSig(tbl)
  local keys = {}
  for k in pairs(tbl) do keys[#keys + 1] = k end
  table.sort(keys)
  local parts = {}
  for _, k in ipairs(keys) do
    local v = tbl[k]
    if type(v) == "table" then
      local ik = {}
      for k2 in pairs(v) do ik[#ik + 1] = k2 end
      table.sort(ik)
      local sub = {}
      for _, k2 in ipairs(ik) do sub[#sub + 1] = k2 .. "=" .. tostring(v[k2]) end
      parts[#parts + 1] = k .. "={" .. table.concat(sub, ",") .. "}"
    else
      parts[#parts + 1] = k .. "=" .. tostring(v)
    end
  end
  return table.concat(parts, " ")
end

local function Row(kind, key, tbl)
  tbl.kind = kind
  tbl.combat = InCombatLockdown() and true or false
  if key ~= nil then tbl.key = key end
  if not ALWAYS[kind] then
    local id = kind .. "|" .. tostring(key)
    local sig = rowSig(tbl)
    if sigs[id] == sig then
      skippedUnchanged = skippedUnchanged + 1
      return
    end
    sigs[id] = sig
  end
  tbl.sweep = sweepN
  tbl.at = date("%H:%M:%S")
  rowsWritten = rowsWritten + 1
  sweepLog:Row(tbl)
end

-- Context --------------------------------------------------------------------

local function stamp()
  if type(ns.Stamp) == "function" then
    local ok, s = pcall(ns.Stamp)
    if ok and type(s) == "table" then return s end
  end
  local spec, hero = "?", "?"
  local getIdx = Fn("C_SpecializationInfo.GetSpecialization") or Fn("GetSpecialization")
  local getInfo = Fn("C_SpecializationInfo.GetSpecializationInfo") or Fn("GetSpecializationInfo")
  if getIdx and getInfo then
    local okI, idx = pcall(getIdx)
    if okI and type(idx) == "number" then
      local okN, _, name = pcall(getInfo, idx)
      spec = (okN and type(name) == "string") and name or ("index " .. idx)
    end
  end
  local getHero = Fn("C_ClassTalents.GetActiveHeroTalentSpec")
  if getHero then
    local okH, id = pcall(getHero)
    if okH and type(id) == "number" then hero = id end
  end
  local inInstance, instanceType = IsInInstance()
  return { spec = spec, hero = hero, instance = inInstance and (instanceType or "unknown") or "none" }
end

-- The alert channel ----------------------------------------------------------
-- The mixin methods are Mixin()-copied onto each frame, so the hook is per instance.
-- Which frames are hooked is tracked in a weak-keyed table on OUR side: a marker field
-- on a Blizzard frame is a write, and this file does not write to Blizzard frames.

local hookedFrames = setmetatable({}, { __mode = "k" })
local edgeCount = 0

--- Edges share the sweep stream's row cap, and the ring drops OLDEST first — so an
--- unbudgeted alert channel would evict the login sweep's env/enum/struct rows, which
--- are written once and never regenerated.  Past the budget the edges are still counted.
local function recordEdge(self, alertEvent)
  edgeCount = edgeCount + 1
  if edgeCount < EDGE_BUDGET then
    Row("alertedge", nil, { cid = Field(self, "cooldownID"), alertEvent = One(alertEvent) })
  elseif edgeCount == EDGE_BUDGET then
    Row("alertedge", nil, { note = "!budget", written = EDGE_BUDGET - 1 })
  end
end

local function hookAlerts(frames)
  for _, f in ipairs(frames) do
    if not hookedFrames[f] and IsObject(f) and type(RawField(f, "TriggerAlertEvent")) == "function" then
      local ok = pcall(hooksecurefunc, f, "TriggerAlertEvent", function(self, alertEvent)
        pcall(recordEdge, self, alertEvent)
      end)
      -- Marked only on success: a frame marked hooked by a failed hook would produce no
      -- edge for the rest of the session and read as an ability that never alerted.
      if ok then hookedFrames[f] = true end
    end
  end
end

-- Environment, enums, category sets ------------------------------------------

local function sweepEnv()
  local layoutCls, layoutLen = LenCall(Fn("C_CooldownViewer.GetLayoutData"))
  local cat = ns.G("Enum.CooldownViewerCategory")
  local row = {
    fnCategorySet = globalType("C_CooldownViewer.GetCooldownViewerCategorySet"),
    fnCooldownInfo = globalType("C_CooldownViewer.GetCooldownViewerCooldownInfo"),
    fnValidAlertTypes = globalType("C_CooldownViewer.GetValidAlertTypes"),
    fnIsAvailable = globalType("C_CooldownViewer.IsCooldownViewerAvailable"),
    fnGetLayoutData = globalType("C_CooldownViewer.GetLayoutData"),
    fnSetLayoutData = globalType("C_CooldownViewer.SetLayoutData"),
    utilPresent = globalType("CooldownViewerUtil"),
    settingsPresent = globalType("CooldownViewerSettings"),
    available = Call("C_CooldownViewer.IsCooldownViewerAvailable"),
    layoutClass = layoutCls,
    layoutLen = layoutLen,
    cvar = Call("C_CVar.GetCVar", "cooldownViewerEnabled"),
    hiddenSpell = Field(cat, "HiddenSpell"),
    hiddenAura = Field(cat, "HiddenAura"),
  }
  local disabled = {}
  for c = 0, 5 do disabled["c" .. c] = Call("CooldownViewerUtil.IsDisabledCategory", c) end
  row.isDisabledCategory = disabled
  Row("env", nil, row)
end

local function sweepEnums()
  for _, path in ipairs(ENUMS) do
    local t = ns.G(path)
    local vals, n = {}, 0
    if type(t) == "table" and not ns.IsSecretTable(t) then
      pcall(function()
        for k, v in pairs(t) do
          if type(k) == "string" then n = n + 1; vals[k] = One(v) end
        end
      end)
    end
    Row("enum", path, { name = path, present = globalType(path), count = n, values = vals })
  end
end

local function sweepCategorySets()
  local f = Fn("C_CooldownViewer.GetCooldownViewerCategorySet")
  local seen = {}
  local function collect(list)
    if type(list) ~= "table" or ns.IsSecretTable(list) then return end
    pcall(function()
      for _, id in ipairs(list) do
        local n = PlainNumber(id)
        if n then seen[n] = true end
      end
    end)
  end
  for c = 0, 5 do
    local cls, t = KeepCall(f, c, false)
    local clsAll, tAll = KeepCall(f, c, true)
    local row = {
      category = c,
      learned = cls, learnedList = ListStr(t), learnedN = CountOf(t),
      all = clsAll, allList = ListStr(tAll), allN = CountOf(tAll),
    }
    collect(t)
    collect(tAll)
    Row("catset", c, row)
  end
  return seen
end

local function decodeFlags(f)
  if type(f) ~= "number" then return "" end
  local e = ns.G("Enum.CooldownSetSpellFlags")
  if type(e) ~= "table" or ns.IsSecretTable(e) then return "" end
  local out = {}
  pcall(function()
    for k, v in pairs(e) do
      if type(k) == "string" and type(v) == "number" and v > 0
        and math.floor(f / v) % 2 == 1 then out[#out + 1] = k end
    end
  end)
  table.sort(out)
  return table.concat(out, "+")
end

--- The id set includes the allowUnlearned side, which on some classes is far larger than
--- the laid-out rows.  It is bounded here rather than allowed to evict other kinds out of
--- the ring, and the count dropped goes on the sweep row: a truncation nobody is told
--- about reads as full coverage.
local STRUCT_MAX = 240

local function sweepStructs(ids)
  local info = Fn("C_CooldownViewer.GetCooldownViewerCooldownInfo")
  local alerts = Fn("C_CooldownViewer.GetValidAlertTypes")
  local sorted = {}
  for id in pairs(ids) do sorted[#sorted + 1] = id end
  table.sort(sorted)
  local dropped = 0
  while #sorted > STRUCT_MAX do
    table.remove(sorted)
    dropped = dropped + 1
  end
  for _, cid in ipairs(sorted) do
    local cls, t = KeepCall(info, cid)
    local alertCls, alertT = KeepCall(alerts, cid)
    Row("struct", cid, {
      cid = cid,
      struct = cls,
      fields = ClassEach(t, INFO_FIELDS),
      extraKeys = ExtraKeys(t, INFO_FIELDS),
      linked = ListStr(RawField(t, "linkedSpellIDs")),
      linkedN = CountOf(RawField(t, "linkedSpellIDs")),
      flagsDecoded = decodeFlags(PlainNumber(RawField(t, "flags"))),
      validAlertTypes = alertCls,
      validAlertTypesList = ListStr(alertT),
    })
  end
  return sorted, dropped
end

-- Viewers and their item frames ----------------------------------------------

local function itemFrames(v)
  local out = {}
  pcall(function()
    local fn = RawField(v, "GetItemFrames")
    if type(fn) ~= "function" then return end
    local ok, list = pcall(fn, v)
    if not ok or type(list) ~= "table" or ns.IsSecretTable(list) then return end
    for _, f in ipairs(list) do out[#out + 1] = f end
  end)
  return out
end

local function poolActive(v)
  local pool = RawField(v, "itemFramePool")
  if not IsObject(pool) then return -1 end
  local n = 0
  local ok = pcall(function()
    for _ in pool:EnumerateActive() do n = n + 1 end
  end)
  return ok and n or -1
end

local function family(item)
  if type(RawField(item, "GetBarFrame")) == "function" then return "buffbar" end
  if type(RawField(item, "GetApplicationsFrame")) == "function" then return "bufficon" end
  if type(RawField(item, "GetChargeCountFrame")) == "function" then return "cooldown" end
  return "?"
end

local function diffInfo(a, b)
  local out = {}
  for _, k in ipairs(INFO_FIELDS) do
    local ca, cb = Field(a, k), Field(b, k)
    if ca ~= cb then out[#out + 1] = k .. ":" .. ca .. "/" .. cb end
  end
  return #out == 0 and "same" or table.concat(out, " ")
end

local function durationSweep(obj)
  if not IsObject(obj) then return { present = One(obj) } end
  local out = MethodEach(obj, DUR_METHODS)
  out.present = "yes"
  return out
end

--- Takes KeepCall's (class, value) pair straight through, so the caller keeps both.
local function classAndSweep(cls, obj)
  return cls, durationSweep(obj)
end

--- The totem slots, read through the RAW API rather than Blizzard's cached wrapper.
--- The wrapper rebuilds a module-local cache its own refresh path depends on; these
--- calls own no shared state, so the slots can be read without touching the subject.
--- GetTotemInfo and GetTotemTimeLeft declare SecretWhenTotemSlotSecret; GetTotemDuration
--- declares no such thing and hands back a duration object, so the three are probed
--- together and the difference between them is the finding.
local TOTEM_RETURNS = { "haveTotem", "totemName", "startTime", "duration", "icon",
  "modRate", "spellID" }

local function totemReturns(row, ok, ...)
  if not ok then row.info = errStr(...); return end
  local n = select("#", ...)
  if n == 0 then row.info = "!nothing"; return end
  row.info = "returned:" .. n
  for i, name in ipairs(TOTEM_RETURNS) do
    if i <= n then row[name] = One((select(i, ...))) end
  end
end

--- `trigger` separates a slot read taken on the sweep schedule from one taken on a
--- PLAYER_TOTEM_UPDATE edge.  The schedule samples the START of a pull, which is exactly
--- when no summon is out; the edge is the instant the state it asks about exists.
local function sweepTotems(trigger)
  local getNum = Fn("GetNumTotemSlots")
  local n
  if getNum then
    local ok, v = pcall(getNum)
    if ok then n = PlainNumber(v) end
  end
  Row("totem", "slots." .. trigger,
    { numSlots = Call("GetNumTotemSlots"), walked = n or -1, trigger = trigger })
  if not n then return end

  local infoFn = Fn("GetTotemInfo")
  for slot = 1, n do
    local row = { slot = slot, trigger = trigger }
    if infoFn then totemReturns(row, pcall(infoFn, slot)) else row.info = ABSENT end
    row.timeLeft = Call("GetTotemTimeLeft", slot)
    -- Named durObj, NOT duration: GetTotemInfo's fourth return is already `duration`,
    -- and the two collided into one key, silently dropping the raw number.
    row.durObjClass, row.durObj = classAndSweep(KeepCall(Fn("GetTotemDuration"), slot))
    Row("totem", trigger .. ".slot" .. slot, row)
  end
end

--- Totem edges are sampled outside the sweep budget: they are cheap (a handful of calls
--- over five slots) and they are the only moment the occupied-slot question is askable.
local TOTEM_EDGE_BUDGET = 60
local totemEdges = 0

local function onTotemEdge()
  if totemEdges >= TOTEM_EDGE_BUDGET then return end
  totemEdges = totemEdges + 1
  sweepTotems("edge" .. totemEdges)
end

local function sweepIdent(item, key, viewer, idx)
  local cid = PlainNumber(RawField(item, "cooldownID"))
    or PlainNumber(RawMethod(item, "GetCooldownID"))
  local info = Fn("C_CooldownViewer.GetCooldownViewerCooldownInfo")
  local fresh, freshCls
  if cid then freshCls, fresh = KeepCall(info, cid) else freshCls = "!skip:no plain cooldownID" end
  local row = {
    viewer = viewer, idx = idx, family = family(item),
    cid = Field(item, "cooldownID"),
    layoutIndex = Field(item, "layoutIndex"),
    editModeIndex = Field(item, "editModeIndex"),
    viewerFrame = Field(item, "viewerFrame"),
    cooldownInfo = Field(item, "cooldownInfo"),
    freshInfo = freshCls,
    freshRungs = ClassEach(fresh, RUNG_FIELDS),
    frameRungs = ClassEach(RawField(item, "cooldownInfo"), RUNG_FIELDS),
    infoDiff = fresh and diffInfo(RawField(item, "cooldownInfo"), fresh) or "!skip:no fresh struct",
    methods = MethodEach(item, M_IDENT),
  }
  Row("ident", key, row)
  return cid, fresh
end

-- Every item row carries its cooldownID: the key is a positional index and Blizzard
-- re-binds indices to different cooldownIDs on a spec or talent change, so a row without
-- one cannot be attributed to a spell after the fact.
local function sweepCdState(item, key, viewer, cid)
  Row("cdstate", key, {
    viewer = viewer, cid = cid or "!skip:no plain cooldownID",
    cache = ClassEach(item, F_CACHE),
    state = ClassEach(item, F_STATE),
    source = ClassEach(item, F_SOURCE),
    shown = ClassEach(item, F_SHOWN),
    range = ClassEach(item, F_RANGE),
    methods = MethodEach(item, M_STATE),
  })
end

local function sweepAura(item, key, viewer, cid)
  local cached = RawField(item, "auraDataCached")
  Row("aura", key, {
    viewer = viewer, cid = cid or "!skip:no plain cooldownID",
    fields = ClassEach(item, F_AURA),
    cachedClass = One(cached),
    cached = ClassEach(cached, AURA_FIELDS),
    cachedExtraKeys = ExtraKeys(cached, AURA_FIELDS),
    totemData = Field(item, "totemData"),
    preferredTotemUpdateSlot = Field(item, "preferredTotemUpdateSlot"),
    pandemicIcon = Field(item, "PandemicIcon"),
    pandemic = ClassEach(item, F_PANDEMIC),
    chargeGainedAlertTimes = Field(item, "chargeGainedAlertTimes"),
    inPandemicTime = Method(item, "IsInPandemicTime", GetTime()),
    methods = MethodEach(item, M_AURA),
  })
end

local function sweepCharges(item, key, viewer, spellID, cid)
  local row = {
    viewer = viewer, cid = cid or "!skip:no plain cooldownID",
    fields = ClassEach(item, F_CHARGE),
    methods = MethodEach(item, M_CHARGE),
  }
  local cls, t = KeepMethod(item, "GetSpellChargeInfo")
  row.chargeInfo = cls
  row.charge = ClassEach(t, CHARGE_INFO_FIELDS)
  row.chargeExtraKeys = ExtraKeys(t, CHARGE_INFO_FIELDS)
  row.castCount = spellID and Call("C_Spell.GetSpellCastCount", spellID) or "!skip:no plain spell id"
  Row("charges", key, row)
end

local function sweepAlerts(item, key, viewer, cid)
  local byEvent = RawField(item, "alertsByEvent")
  local apiCls, apiT
  if cid then
    apiCls, apiT = KeepCall(Fn("C_CooldownViewer.GetValidAlertTypes"), cid)
  else
    apiCls = "!skip:no plain cooldownID"
  end
  -- The frame's copy is tInvert'd — a set keyed BY alert-event-type — so its content is
  -- in the keys.  The API's return is a plain array and stays a list read.
  Row("alerts", key, {
    viewer = viewer, cid = cid or "!skip:no plain cooldownID",
    frameValidAlertTypesClass = One(RawField(item, "validAlertTypes")),
    frameValidAlertTypes = KeyList(RawField(item, "validAlertTypes")),
    apiValidAlertTypes = apiCls,
    apiValidAlertTypesList = ListStr(apiT),
    alertsByEventClass = One(byEvent),
    alertsByEventKeys = KeyList(byEvent),
    notCalled = NOT_CALLED,
  })
end

local function sweepWidget(item, key, viewer, cid)
  local cd = RawField(item, "Cooldown")
  local fs = RawMethod(cd, "GetCountdownFontString")
  local icon = RawField(item, "Icon")
  local iconTex = RawField(icon, "Icon") or icon
  local chargeCount = RawField(item, "ChargeCount")
  local bar = RawField(item, "Bar")
  Row("widget", key, {
    viewer = viewer, cid = cid or "!skip:no plain cooldownID",
    cooldownClass = One(cd),
    cooldown = MethodEach(cd, CD_GETTERS),
    countdownFontString = Method(cd, "GetCountdownFontString"),
    countdownText = Method(fs, "GetText"),
    countdownShown = Method(fs, "IsShown"),
    iconTexture = Method(iconTex, "GetTexture"),
    iconDesaturated = Method(iconTex, "IsDesaturated"),
    chargeText = Method(RawField(chargeCount, "Current"), "GetText"),
    chargeShown = Method(chargeCount, "IsShown"),
    cooldownFlashShown = Method(RawField(item, "CooldownFlash"), "IsShown"),
    outOfRangeShown = Method(RawField(item, "OutOfRange"), "IsShown"),
    debuffBorderShown = Method(RawField(item, "DebuffBorder"), "IsShown"),
    applicationsText = Method(RawField(RawField(item, "Applications"), "Applications"), "GetText"),
    iconApplicationsText = Method(RawField(icon, "Applications"), "GetText"),
    barValue = Method(bar, "GetValue"),
    barMinMax = Method(bar, "GetMinMaxValues"),
    barPipShown = Method(RawField(bar, "Pip"), "IsShown"),
    barName = Method(RawField(bar, "Name"), "GetText"),
    barDuration = Method(RawField(bar, "Duration"), "GetText"),
    methods = MethodEach(item, M_WIDGET),
  })
end

--- Every probe here needs a PLAIN spell id as an argument. When none is readable the row
--- still gets written, with each probe saying so — a guessed id would be a fabricated
--- measurement, and a missing row would read as "not measured".
local NO_ID = "!skip:no plain spell id"
local API_KEYS = {
  "cooldown", "cooldownExtraKeys", "charges", "chargesExtraKeys",
  "overlayed", "usable", "hasRange", "inRange", "spellName", "spellTexture", "auraBySpellID",
}

local function sweepApi(item, key, viewer, spellID, source, cid)
  local row = { viewer = viewer, spellSource = source, cid = cid or "!skip:no plain cooldownID" }
  if not spellID then
    for _, k in ipairs(API_KEYS) do row[k] = NO_ID end
    row.cooldownFields = { note = NO_ID }
    row.chargesFields = { note = NO_ID }
    row.durFalse = { present = NO_ID }
    row.durTrue = { present = NO_ID }
    row.durCharge = { present = NO_ID }
    row.auraDuration = { present = NO_ID }
    Row("api", key, row)
    return
  end
  row.spellID = spellID
  local cdCls, cdT = KeepCall(Fn("C_Spell.GetSpellCooldown"), spellID)
  row.cooldown = cdCls
  row.cooldownFields = ClassEach(cdT, CD_INFO_FIELDS)
  row.cooldownExtraKeys = ExtraKeys(cdT, CD_INFO_FIELDS)
  local chCls, chT = KeepCall(Fn("C_Spell.GetSpellCharges"), spellID)
  row.charges = chCls
  row.chargesFields = ClassEach(chT, CHARGE_INFO_FIELDS)
  row.chargesExtraKeys = ExtraKeys(chT, CHARGE_INFO_FIELDS)

  -- The CLASS of the call is kept beside the object sweep: "returned nothing", "threw"
  -- and "returned a secret" all yield no object, and collapsing them to nil would record
  -- three different answers as one.
  local durFn = Fn("C_Spell.GetSpellCooldownDuration")
  row.durFalseClass, row.durFalse = classAndSweep(KeepCall(durFn, spellID, false))
  row.durTrueClass, row.durTrue = classAndSweep(KeepCall(durFn, spellID, true))
  row.durChargeClass, row.durCharge =
    classAndSweep(KeepCall(Fn("C_Spell.GetSpellChargeDuration"), spellID))

  row.overlayed = Call("C_SpellActivationOverlay.IsSpellOverlayed", spellID)
  row.usable = Call("C_Spell.IsSpellUsable", spellID)
  row.hasRange = Call("C_Spell.SpellHasRange", spellID)
  row.inRange = Call("C_Spell.IsSpellInRange", spellID, "target")
  row.spellName = Call("C_Spell.GetSpellName", spellID)
  row.spellTexture = Call("C_Spell.GetSpellTexture", spellID)

  local unit = RawField(item, "auraDataUnit")
  local instID = PlainNumber(RawField(item, "auraInstanceID"))
  if type(unit) == "string" and instID then
    row.auraDurationClass, row.auraDuration =
      classAndSweep(KeepCall(Fn("C_UnitAuras.GetAuraDuration"), unit, instID))
  else
    row.auraDurationClass = "!skip:no plain unit + auraInstanceID"
    row.auraDuration = { present = row.auraDurationClass }
  end
  local auraSpellID = PlainNumber(RawMethod(item, "GetAuraSpellID"))
  row.auraBySpellID = (type(unit) == "string" and auraSpellID)
    and Call("C_UnitAuras.GetUnitAuraBySpellID", unit, auraSpellID) or "!skip:no plain unit + spell id"
  Row("api", key, row)
end

-- The event tape -------------------------------------------------------------
-- Registered at load, not at sweep time: the tape has to cover the whole session, and a
-- sweep is a sample of state, not of traffic.

local tally = {}

local function tallyFor(event)
  local t = tally[event]
  if not t then
    t = { n = 0, combat = 0, lines = 0, sigs = {}, sigN = 0, minArity = -1, maxArity = -1 }
    tally[event] = t
  end
  return t
end

local function unitAuraLine(a1, a2)
  local added = CountOf(RawField(a2, "addedAuras"))
  local updated = CountOf(RawField(a2, "updatedAuraInstanceIDs"))
  local removed = CountOf(RawField(a2, "removedAuraInstanceIDs"))
  return string.format("unit=%s full=%s added=%d updated=%d removed=%d",
    One(a1), Field(a2, "isFullUpdate"), added, updated, removed)
end

local function onEvent(_, event, ...)
  local n = select("#", ...)
  local t = tallyFor(event)
  local inCombat = InCombatLockdown() and true or false
  t.n = t.n + 1
  if inCombat then t.combat = t.combat + 1 end
  if t.minArity < 0 or n < t.minArity then t.minArity = n end
  if n > t.maxArity then t.maxArity = n end

  -- Rendering stops once both budgets are spent: these fire tens of times a second in a
  -- pull, and an instrument that allocates per firing is measuring its own garbage.
  local spent = t.sigN >= 3 and t.lines > EVENT_BUDGET
  local parts = {}
  if not spent then
    for i = 1, n do parts[i] = One((select(i, ...))) end
    local sig = table.concat(parts, ",")
    if not t.sigs[sig] and t.sigN < 3 then
      t.sigs[sig] = true
      t.sigN = t.sigN + 1
    end
  end
  local at = date("%H:%M:%S")
  t.firstAt = t.firstAt or at
  t.lastAt = at

  if event == "PLAYER_TOTEM_UPDATE" then pcall(onTotemEdge) end

  if t.lines < EVENT_BUDGET then
    t.lines = t.lines + 1
    local body
    if event == "UNIT_AURA" then
      body = unitAuraLine((select(1, ...)), (select(2, ...)))
    else
      local args = {}
      for i = 1, n do args[i] = "a" .. i .. "=" .. parts[i] end
      body = table.concat(args, " ")
    end
    eventLog:Line("%s c=%d %s n=%d %s", at, inCombat and 1 or 0, event, n, body)
  elseif t.lines == EVENT_BUDGET then
    t.lines = t.lines + 1
    eventLog:Mark("%s !budget %s - %d lines written, still counting", at, event, EVENT_BUDGET)
  end
end

local function eventRows()
  local names = {}
  for _, e in ipairs(PLAIN_EVENTS) do names[#names + 1] = e end
  for e in pairs(UNIT_EVENTS) do names[#names + 1] = e end
  table.sort(names)
  for _, e in ipairs(names) do
    local t = tally[e]
    local row = { event = e, count = t and t.n or 0, inCombat = t and t.combat or 0 }
    if t then
      row.minArity, row.maxArity = t.minArity, t.maxArity
      row.firstAt, row.lastAt = t.firstAt, t.lastAt
      local sl = {}
      for s in pairs(t.sigs) do sl[#sl + 1] = s end
      table.sort(sl)
      row.signatures = table.concat(sl, " | ")
    end
    Row("event", e, row)
  end
  return names
end

local tape = CreateFrame("Frame")
for _, e in ipairs(PLAIN_EVENTS) do pcall(tape.RegisterEvent, tape, e) end
for e, units in pairs(UNIT_EVENTS) do
  pcall(tape.RegisterUnitEvent, tape, e, units[1], units[2])
end
tape:SetScript("OnEvent", function(self, event, ...)
  pcall(onEvent, self, event, ...)
end)

-- The sweep ------------------------------------------------------------------

local lastReport = { "no sweep taken yet" }

local function doSweep(reason)
  sweepN = sweepN + 1
  local started = GetTime()
  rowsWritten, skippedUnchanged = 0, 0

  local combat = InCombatLockdown() and true or false
  if lastCombat ~= combat then sigs = {}; lastCombat = combat end

  -- Both streams get the stamp and the boundary mark. The tape's lines are pre-rendered
  -- and cannot gain a field later, so a session that respecs mid-way has to be sliceable
  -- from what is already written.
  local st = stamp()
  local boundary = string.format("== sweep #%d %s combat=%d reason=%s spec=%s hero=%s instance=%s",
    sweepN, date("%H:%M:%S"), combat and 1 or 0, tostring(reason),
    tostring(st.spec), tostring(st.hero), tostring(st.instance))
  for _, log in ipairs({ sweepLog, eventLog }) do
    log:Meta("spec", st.spec)
    log:Meta("hero", st.hero)
    log:Meta("instance", st.instance)
    log:Meta("interface", select(4, GetBuildInfo()))
    log:Mark("%s", boundary)
  end

  -- A spec or talent change re-binds every positional index to a different cooldownID,
  -- so a row that renders identically is a different subject, not an unchanged one.
  local build = tostring(st.spec) .. "/" .. tostring(st.hero)
  if lastBuild ~= build then sigs = {}; lastBuild = build end

  sweepEnv()
  sweepEnums()
  sweepTotems("sweep" .. sweepN)
  local ids = sweepCategorySets()
  local report = { string.format("sweep #%d %s combat=%s reason=%s spec=%s hero=%s",
    sweepN, date("%H:%M:%S"), tostring(combat), tostring(reason), tostring(st.spec), tostring(st.hero)) }

  local itemCount = 0
  for _, vname in ipairs(VIEWERS) do
    local v = ns.G(vname)
    local frames = itemFrames(v)
    local active = poolActive(v)
    Row("viewer", vname, {
      viewer = vname,
      present = globalType(vname),
      isShown = Method(v, "IsShown"),
      isVisible = Method(v, "IsVisible"),
      category = Method(v, "GetCategory"),
      itemFrames = #frames,
      layoutChildren = CountOf(RawMethod(v, "GetLayoutChildren")),
      poolActive = active,
      itemCount = Method(v, "GetItemCount"),
      stride = Method(v, "GetStride"),
      horizontal = Method(v, "IsHorizontal"),
      hideWhenInactive = Method(v, "GetHideWhenInactive"),
      isEditing = Method(v, "IsEditing"),
      shouldBeShown = Method(v, "ShouldBeShown"),
      cooldownIDs = ListStr(RawMethod(v, "GetCooldownIDs")),
    })
    report[#report + 1] = string.format("%-24s frames=%d pool=%d shown=%s",
      vname, #frames, active, Method(v, "IsShown"))

    hookAlerts(frames)
    for i, item in ipairs(frames) do
      itemCount = itemCount + 1
      local key = vname .. "#" .. i
      local cid, fresh = sweepIdent(item, key, vname, i)
      if cid then ids[cid] = true end
      local spellID, source = PlainNumber(RawMethod(item, "GetBaseSpellID")), "frame"
      if not spellID then
        spellID, source = PlainNumber(RawField(fresh, "spellID")), "struct"
      end
      if not spellID then source = "none" end
      sweepCdState(item, key, vname, cid)
      sweepAura(item, key, vname, cid)
      sweepCharges(item, key, vname, spellID, cid)
      sweepAlerts(item, key, vname, cid)
      sweepWidget(item, key, vname, cid)
      sweepApi(item, key, vname, spellID, source, cid)
      report[#report + 1] = string.format("  %-3d cid=%s spell=%s name=%s active=%s cdText=%s",
        i, tostring(cid), tostring(spellID), Method(item, "GetNameText"),
        Method(item, "IsActive"),
        Method(RawMethod(RawField(item, "Cooldown"), "GetCountdownFontString"), "GetText"))
    end
  end

  local structIDs, structDropped = sweepStructs(ids)
  local events = eventRows()

  Row("sweep", nil, {
    reason = tostring(reason), spec = tostring(st.spec), hero = tostring(st.hero),
    instance = tostring(st.instance),
    items = itemCount, cooldownIDs = #structIDs, structDropped = structDropped,
    events = #events,
    rows = rowsWritten, skippedUnchanged = skippedUnchanged, alertEdges = edgeCount,
    elapsedMs = math.floor((GetTime() - started) * 1000 + 0.5),
  })

  report[#report + 1] = string.format(
    "items=%d cooldownIDs=%d structDropped=%d rows=%d skippedUnchanged=%d alertEdges=%d",
    itemCount, #structIDs, structDropped, rowsWritten, skippedUnchanged, edgeCount)
  lastReport = report
  return report
end

--- The cap exists so a long session cannot fill SavedVariables with near-identical
--- sweeps.  Reaching it is announced once; a manual press past it says so and returns.
local function trySweep(reason)
  if sweepN >= MAX_SWEEPS then
    if not capAnnounced then
      capAnnounced = true
      ns.Printf("cdm sweep cap reached (%d this session) — no further sweeps. /reload for a new session.",
        MAX_SWEEPS)
    end
    return nil
  end
  local ok, res = pcall(doSweep, reason)
  if not ok then
    ns.Printf("|cffff4040cdm sweep failed:|r %s", ns.Capture.Safe(res))
    return nil
  end
  return res
end

-- Dump-panel buttons ---------------------------------------------------------

ns.Dumps.Register{
  id = "cdmsweep",
  label = "cdm sweep",
  blurb = function()
    return string.format("%d/%d sweeps this session", sweepN, MAX_SWEEPS)
  end,
  capture = function()
    local report = trySweep("manual")
    if report then return report end
    local out = {
      string.format("cap reached — %d of %d sweeps already taken this session.", sweepN, MAX_SWEEPS),
      "Nothing was swept. /reload starts a new session.",
      "",
      "Last sweep:",
    }
    for _, ln in ipairs(lastReport) do out[#out + 1] = ln end
    return out
  end,
}

ns.Dumps.Register{
  id = "cdmevents",
  label = "cdm events",
  blurb = function()
    local fired, total = 0, 0
    for _, e in ipairs(PLAIN_EVENTS) do
      total = total + 1
      if tally[e] then fired = fired + 1 end
    end
    for e in pairs(UNIT_EVENTS) do
      total = total + 1
      if tally[e] then fired = fired + 1 end
    end
    return string.format("%d/%d events seen", fired, total)
  end,
  capture = function()
    local names = {}
    for _, e in ipairs(PLAIN_EVENTS) do names[#names + 1] = e end
    for e in pairs(UNIT_EVENTS) do names[#names + 1] = e end
    table.sort(names)
    local out = { "cdm event tape — " .. date("%H:%M:%S"),
      "an event with count 0 was registered and never fired", "" }
    for _, e in ipairs(names) do
      local t = tally[e]
      if not t then
        out[#out + 1] = string.format("%-40s count=0", e)
      else
        local sl = {}
        for s in pairs(t.sigs) do sl[#sl + 1] = s end
        table.sort(sl)
        out[#out + 1] = string.format("%-40s count=%-5d combat=%-5d arity=%d..%d first=%s last=%s",
          e, t.n, t.combat, t.minArity, t.maxArity, tostring(t.firstAt), tostring(t.lastAt))
        for _, s in ipairs(sl) do out[#out + 1] = "      sig: " .. s end
      end
    end
    return out
  end,
}

-- Driver ---------------------------------------------------------------------

local driver = CreateFrame("Frame")
driver:RegisterEvent("PLAYER_LOGIN")
driver:RegisterEvent("PLAYER_REGEN_DISABLED")
driver:RegisterEvent("PLAYER_REGEN_ENABLED")
driver:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")
driver:RegisterEvent("TRAIT_CONFIG_UPDATED")

driver:SetScript("OnEvent", function(_, event)
  if event == "PLAYER_LOGIN" then
    C_Timer.After(8, function()
      if InCombatLockdown() then return end
      trySweep("login")
    end)
  elseif event == "PLAYER_REGEN_DISABLED" then
    C_Timer.After(3, function()
      if InCombatLockdown() then trySweep("combat-early") end
    end)
    C_Timer.After(12, function()
      if InCombatLockdown() then trySweep("combat-late") end
    end)
  elseif event == "PLAYER_REGEN_ENABLED" then
    C_Timer.After(2, function() trySweep("post-combat") end)
  else
    C_Timer.After(3, function()
      if InCombatLockdown() then return end
      trySweep("build-changed")
    end)
  end
end)

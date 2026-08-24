-- T_Security.lua — three unflown mechanisms behind security-taint-and-restricted-data.md.
--
-- ⚠ WHAT NONE OF THESE CAN DO. All three sinks are aspect-less with no programmatic
-- read-back: once a duration object or a Region is handed to the client, whether a pixel
-- moved is not exposed by any API, and `IsShown` on an aura button is secret by design.
-- So every test here measures the SAME three things — was the call accepted, did it error,
-- and what (if anything) reads back — and says so, in its own words, for the half it cannot
-- see. The visual half is a human eyeball and is recorded as NOT MEASURED, never as a pass.
-- The `expect` text in questions.json carries the eyeball instruction beside the result.
local ADDON, ns = ...

-- ── shared helpers ───────────────────────────────────────────────────────────

-- ⚠ Written out long on purpose. `ok and v or "…"` returns the fallback whenever `v` is
-- legitimately `false` or `nil`, and `false`/`nil` is exactly what half of these getters
-- are being asked for (lab-process.md §3.2, hit twice).
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

--- Call a zero-arg getter by NAME on one of our own widgets and describe the result.
--- An absent method is reported as absent rather than as a nil value — the two mean
--- completely different things and `describe(true, nil)` cannot tell them apart.
local function probeGetter(obj, name)
  if obj == nil then return "subject absent" end
  local m = obj[name]
  if type(m) ~= "function" then return "method absent" end
  local ok, v = pcall(m, obj)
  return describe(ok, v)
end

local TILE = 44

--- One CustomAuraContainer + one slot, built the way `T_AuraPandemic` proved out:
--- `AddAuraSlot` uses a batchSize=1 provider, so `initializeFrame` fires at slot-creation
--- time whether or not any aura matches — an `init` of 0 therefore means the slot never
--- built at all, which is the one thing that would make every other field here meaningless.
--- `SetUnit` LAST of the wiring calls (mined-pending-verification.md:221).
local function buildSlot(parent, initFn)
  local log = { init = 0 }
  local ok, container = pcall(CreateFrame, "AuraContainer", nil, parent,
                              "CustomAuraContainerTemplate")
  if not ok or not container then
    log.container = "FAILED: " .. tostring(container)
    return log
  end
  log.container = type(container)
  container:SetAllPoints(parent)

  local slotOk, slotFrame = pcall(function()
    return container:AddAuraSlot("probe", "HARMFUL", {
      candidateFilters = { isFromPlayerOrPlayerPet = true },
      initializeFrame = function(button)
        log.init = log.init + 1
        button:SetSize(TILE, TILE)
        button:SetAllPoints(container)
        log.addPandemicRegion = type(button.AddPandemicRegion)
        initFn(button, log)
      end,
    })
  end)
  if slotOk then log.slot = type(slotFrame) else log.slot = "FAILED: " .. tostring(slotFrame) end

  local uOk, uErr = pcall(function() container:SetUnit("target") end)
  if uOk then log.setUnit = "ok" else log.setUnit = "FAILED: " .. tostring(uErr) end
  local aOk, aErr = pcall(function() container:UpdateAllAuras() end)
  if aOk then log.updateAllAuras = "ok" else log.updateAllAuras = "FAILED: " .. tostring(aErr) end
  return log
end

-- ═════════════════════════════════════════════════════════════════════════════
-- 1. Cooldown swipe driven from a duration object, and the ORDERING rider.
--
-- `C_Spell.GetSpellCooldownDuration(spellID, ignoreGCD)` returns a LuaDurationObject even in
-- restricted combat `[client 2026-08-09]` (cooldown-manager.md:1933-1945); the matching sink is
-- `Cooldown:SetCooldownFromDurationObject(dur, clearIfZero)`. The claim under test is the
-- RIDER at security-taint-and-restricted-data.md:2499 — "a widget that may be showing aura
-- display time needs `SetUseAuraDisplayTime(false)` FIRST" — which the KB itself grades
-- medium confidence. So BOTH orders are armed on their own widget and each call is recorded
-- separately; if the ordering matters as an ERROR the refused call names itself, and if it
-- matters only in pixels neither order errors and that is the finding.
-- ═════════════════════════════════════════════════════════════════════════════

-- Reported ALL of them, keyed by name — never `list[1]` (lab-process.md §3.2). Which of these
-- a character knows varies, and a probe that silently picked one would answer a narrower
-- question than its id claims. Hearthstone is here because every character has it.
local SPELL_CANDIDATES = {
  { name = "Hearthstone (8690)", id = 8690 },
  { name = "Shadow Bolt (686)", id = 686 },
  { name = "Immolate (348)", id = 348 },
  { name = "Chaos Bolt (116858)", id = 116858 },
  { name = "Demonbolt (264178)", id = 264178 },
}

local swipeHost, cdAuraFirst, cdSinkFirst

local function swipeWidget()
  if not swipeHost then
    swipeHost = CreateFrame("Frame", nil, UIParent)
    swipeHost:SetSize(TILE, TILE)
    swipeHost:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
    swipeHost:Hide()
  end
  local cd = CreateFrame("Cooldown", nil, swipeHost, "CooldownFrameTemplate")
  cd:SetAllPoints(swipeHost)
  return cd
end

--- Arm one widget in one order and report every call and read-back FLAT.
--- ⚠ `ns.stash` recurses exactly one level, so a nested read-back table would persist as the
--- string "<table>". Everything a reader needs is a scalar on this table.
local function arm(cd, dur, auraFirst)
  local log = {}
  -- Re-establish the precondition the rider is ABOUT — a widget that may be showing aura
  -- display time — because the widgets are reused across runs and a previous run already
  -- turned it off. Without this, the second run of "sink first" is not the same experiment.
  if type(cd.SetUseAuraDisplayTime) ~= "function" then
    log.preset = "SetUseAuraDisplayTime absent"
  else
    local pOk, pErr = pcall(cd.SetUseAuraDisplayTime, cd, true)
    if pOk then log.preset = "aura display time re-enabled"
    else log.preset = "REFUSED: " .. tostring(pErr) end
  end

  local function callAura()
    if type(cd.SetUseAuraDisplayTime) ~= "function" then
      log.setUseAuraDisplayTime = "method absent"
      return
    end
    local ok, err = pcall(cd.SetUseAuraDisplayTime, cd, false)
    if ok then log.setUseAuraDisplayTime = "accepted"
    else log.setUseAuraDisplayTime = "REFUSED: " .. tostring(err) end
  end
  local function callSink()
    if type(cd.SetCooldownFromDurationObject) ~= "function" then
      log.setCooldownFromDurationObject = "method absent"
      return
    end
    local ok, err = pcall(cd.SetCooldownFromDurationObject, cd, dur, true)
    if ok then log.setCooldownFromDurationObject = "accepted"
    else log.setCooldownFromDurationObject = "REFUSED: " .. tostring(err) end
  end

  if auraFirst then
    log.order = "SetUseAuraDisplayTime(false) FIRST, then SetCooldownFromDurationObject"
    callAura(); callSink()
  else
    log.order = "SetCooldownFromDurationObject FIRST, then SetUseAuraDisplayTime(false)"
    callSink(); callAura()
  end

  for _, g in ipairs({ "GetCooldownDuration", "GetCooldownTimes", "GetDrawSwipe",
                       "IsShown", "GetEffectiveAlpha" }) do
    log[g] = probeGetter(cd, g)
  end
  return log
end

ns.Test{
  id = "duration-object-swipe-ordering",
  anchor = "security-taint-and-restricted-data.md:2499",
  bucket = "call",
  question = "Does Cooldown:SetCooldownFromDurationObject accept a LuaDurationObject from "
    .. "C_Spell.GetSpellCooldownDuration, and does the SetUseAuraDisplayTime(false) ordering "
    .. "rider change whether either call is refused?",
  run = function()
    local getDur = ns.G("C_Spell.GetSpellCooldownDuration")
    if type(getDur) ~= "function" then
      -- An absent API is an ANSWER, not an ambiguity: no other world produces it.
      return {
        measured = true,
        api = "C_Spell.GetSpellCooldownDuration is ABSENT on this build",
        why = "Nothing further to arm; the source half of the claim is gone.",
      }
    end

    local seen, chosen, chosenName = {}, nil, nil
    for _, c in ipairs(SPELL_CANDIDATES) do
      local ok, v = pcall(getDur, c.id, false)
      if not ok then
        seen[c.name] = "ERROR: " .. tostring(v)
      else
        seen[c.name] = describe(true, v)
        if type(v) == "userdata" and chosen == nil then
          chosen = v
          chosenName = c.name
        end
      end
    end

    if chosen == nil then
      -- ⚠ DECLINE. "no candidate returned an object" has two worlds: the API refuses in this
      -- context (the finding), or this character simply knows none of these spells and every
      -- call correctly returned nothing. Same bytes; not an answer.
      return {
        measured = false,
        candidates = seen,
        why = "no candidate spell id yielded a duration object — indistinguishable from a "
          .. "character that knows none of them. Re-fly on a Warlock (Shadow Bolt / Immolate "
          .. "are in SPELL_CANDIDATES), or add an id this character casts.",
      }
    end

    cdAuraFirst = cdAuraFirst or swipeWidget()
    cdSinkFirst = cdSinkFirst or swipeWidget()

    return {
      measured = true,
      api = "present",
      candidates = seen,
      chosen = chosenName,
      auraFirst = arm(cdAuraFirst, chosen, true),
      sinkFirst = arm(cdSinkFirst, chosen, false),
      eyeball = "NOT MEASURED: whether a swipe was DRAWN, and whether the wrong order leaves "
        .. "the aura timer drawing instead. No getter on Cooldown reports the rendered arc; "
        .. "the only oracle is a human watching the widget. Acceptance is not pixels.",
      why = "Acceptance + refusal + read-backs only, both orders, on their own widget.",
    }
  end,
}

-- ═════════════════════════════════════════════════════════════════════════════
-- 2. AddPandemicRegion with a Frame that has CHILDREN.
--
-- security-taint-and-restricted-data.md:1460-1468: a Frame is a Region, so a plate and a
-- glyph parented under one wrapper are handed over together and the client's `SetShown`
-- hides both. `[client 2026-08-21]` covers ACCEPTANCE ONLY — observations.md:1402 records
-- that the flight which produced it was flown on DESTRUCTION, whose slot matched nothing, so
-- no tile was ever visible. The children drawing and hiding AS A UNIT is unmeasured.
-- ═════════════════════════════════════════════════════════════════════════════

local kidsHost, kidsLog, kidsSubjects

local function kidsInit(button, log)
  local wrap = CreateFrame("Frame", nil, button)
  wrap:SetAllPoints(button)
  local plate = wrap:CreateTexture(nil, "OVERLAY")
  plate:SetAllPoints(wrap)
  plate:SetColorTexture(1.0, 0.72, 0.20, 0.85)
  local glyph = wrap:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  glyph:SetPoint("CENTER", wrap, "CENTER", 0, 0)
  glyph:SetText("P")
  -- A child FRAME as well as child REGIONS: the claim is about a Frame being a Region, and a
  -- wrapper carrying only textures would not exercise the frame-child half of it at all.
  local kid = CreateFrame("Frame", nil, wrap)
  kid:SetSize(10, 10)
  kid:SetPoint("TOPLEFT", wrap, "TOPLEFT", 0, 0)
  local kidTex = kid:CreateTexture(nil, "OVERLAY")
  kidTex:SetAllPoints(kid)
  kidTex:SetColorTexture(0, 0, 0, 1)

  log.childFrames = select("#", wrap:GetChildren())
  log.childRegions = select("#", wrap:GetRegions())

  if type(button.AddPandemicRegion) ~= "function" then
    log.handover = "AddPandemicRegion absent"
    wrap:Hide()
  else
    local ok, err = pcall(function() button:AddPandemicRegion(wrap) end)
    if ok then
      log.handover = "accepted"
    else
      log.handover = "REFUSED: " .. tostring(err)
      -- It never became a sink, so hiding it is still ours to do — and a permanently-on
      -- orange block would otherwise read as "the window is always open".
      wrap:Hide()
    end
  end
  kidsSubjects = { button = button, wrap = wrap, plate = plate, glyph = glyph, kid = kid }
end

ns.Test{
  id = "pandemic-region-frame-with-children",
  anchor = "security-taint-and-restricted-data.md:1460",
  bucket = "secret",
  question = "Is a Frame carrying child frames and child regions accepted by "
    .. "AddPandemicRegion, and what of the handed-over frame stays readable afterwards?",
  run = function()
    if not kidsLog then
      kidsHost = CreateFrame("Frame", nil, UIParent)
      kidsHost:SetSize(TILE, TILE)
      kidsHost:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
      kidsHost:Hide()
      kidsLog = buildSlot(kidsHost, kidsInit)
    end

    if kidsLog.init == 0 then
      -- DECLINE: with no button there is no AddPandemicRegion to accept anything, so every
      -- other field would describe a path that never ran.
      return {
        measured = false,
        container = kidsLog.container,
        slot = kidsLog.slot,
        why = "initializeFrame never ran, so the handover was never attempted. The slot "
          .. "builds unconditionally when the container is valid — check `container`/`slot` "
          .. "above and re-fly after a /reload.",
      }
    end

    local s = kidsSubjects or {}
    return {
      measured = true,
      container = kidsLog.container,
      slot = kidsLog.slot,
      setUnit = kidsLog.setUnit,
      updateAllAuras = kidsLog.updateAllAuras,
      initFired = kidsLog.init,
      addPandemicRegion = kidsLog.addPandemicRegion or "initializeFrame never ran",
      handover = kidsLog.handover,
      childFrames = kidsLog.childFrames,
      childRegions = kidsLog.childRegions,
      -- After the handover the client owns SecretAspect.Shown on the WRAPPER. Whether that
      -- makes our own reads of it secret, throw, or stay plain is itself unrecorded, so read
      -- the wrapper AND each child and report what came back.
      wrap_IsShown = probeGetter(s.wrap, "IsShown"),
      wrap_GetAlpha = probeGetter(s.wrap, "GetAlpha"),
      kid_IsShown = probeGetter(s.kid, "IsShown"),
      glyph_IsShown = probeGetter(s.glyph, "IsShown"),
      plate_IsShown = probeGetter(s.plate, "IsShown"),
      button_IsShown = probeGetter(s.button, "IsShown"),
      eyeball = "NOT MEASURED: whether the plate AND the glyph AND the child frame appear and "
        .. "vanish together, only inside the refresh window. A child's own IsShown flag does "
        .. "not change when a parent is hidden, so no read above can answer it. Needs a human "
        .. "on DEMONOLOGY with a dot ticking — observations.md:1402 is the flight that missed "
        .. "this by flying Destruction, whose slot matched nothing.",
      why = "Acceptance and read-back only.",
    }
  end,
}

-- ═════════════════════════════════════════════════════════════════════════════
-- 3. An ANIMATED background on a pandemic region. `[gap]` — no KB claim exists.
--
-- The region's only sealed aspect is `Shown`, so alpha / scale / texcoord / animation on it
-- and on its children should stay ours. This asks whether the animation APIs are still
-- callable on a handed-over frame at all — not whether the result is pretty.
--
-- ⚠ COST, from security-taint-and-restricted-data.md:1471-1473: the pandemic sink is the only
-- one carrying an `OnUpdate`, and its enablement is itself `secretwrap`ped. Budget ONE per
-- armed tile; do not attach speculatively. The flipbook ticker below is bounded for the same
-- reason — a lab probe must not leave an unbounded timer running for the session.
--
-- ⚠ THE CONTROL IS THE POINT. An AnimationGroup stops when its frame is hidden, so a `false`
-- from IsPlaying on the ARMED region has two worlds — refused, or the client legitimately
-- hid it because the refresh window is closed. An identically-built wrapper that was NEVER
-- handed over is the discriminator, and the host is deliberately SHOWN (alpha 0) because an
-- animation on a hidden host would make the control useless.
-- ═════════════════════════════════════════════════════════════════════════════

local animHost, animLog, animSubjects, animTicker, animTicks

local function makeAnimated(parent, r, g, b)
  local wrap = CreateFrame("Frame", nil, parent)
  wrap:SetAllPoints(parent)
  local tex = wrap:CreateTexture(nil, "OVERLAY")
  tex:SetAllPoints(wrap)
  tex:SetColorTexture(r, g, b, 0.8)
  local ag = wrap:CreateAnimationGroup()
  ag:SetLooping("BOUNCE")
  local a = ag:CreateAnimation("Alpha")
  a:SetDuration(0.5)
  a:SetFromAlpha(1.0)
  a:SetToAlpha(0.25)
  local sc = ag:CreateAnimation("Scale")
  sc:SetDuration(0.5)
  sc:SetScaleFrom(1.0, 1.0)
  sc:SetScaleTo(1.15, 1.15)
  return wrap, tex, ag
end

local function animInit(button, log)
  local wrap, tex, ag = makeAnimated(button, 0.2, 0.8, 1.0)

  if type(button.AddPandemicRegion) ~= "function" then
    log.handover = "AddPandemicRegion absent"
    wrap:Hide()
  else
    local ok, err = pcall(function() button:AddPandemicRegion(wrap) end)
    if ok then
      log.handover = "accepted"
    else
      log.handover = "REFUSED: " .. tostring(err)
      wrap:Hide()
    end
  end

  -- Play AFTER the handover on purpose: that is the order real code would use, and if the
  -- handover seals anything on the frame this is where it would surface.
  local pOk, pErr = pcall(function() ag:Play() end)
  if pOk then log.play = "accepted" else log.play = "REFUSED: " .. tostring(pErr) end

  -- The second animated route the gap names: a SetTexCoord flipbook driven by a ticker.
  -- Bounded at 600 ticks (~60 s) — one armed tile's worth, never a session-long timer.
  animTicks = 0
  local tOk, ticker = pcall(function()
    return C_Timer.NewTicker(0.1, function()
      animTicks = animTicks + 1
      local f = animTicks % 4
      pcall(function() tex:SetTexCoord(f / 4, (f + 1) / 4, 0, 1) end)
    end, 600)
  end)
  if tOk then
    animTicker = ticker
    log.ticker = type(ticker)
  else
    log.ticker = "FAILED: " .. tostring(ticker)
  end

  animSubjects = { button = button, wrap = wrap, tex = tex, ag = ag }
end

ns.Test{
  id = "pandemic-region-animated-background",
  anchor = "security-taint-and-restricted-data.md:1471",
  bucket = "secret",
  question = "Can a Frame handed to AddPandemicRegion still carry an AnimationGroup and a "
    .. "SetTexCoord flipbook of ours — is the handover accepted, is the animation object "
    .. "created, and does it report as playing?",
  run = function()
    if not animLog then
      animHost = CreateFrame("Frame", nil, UIParent)
      animHost:SetSize(TILE, TILE)
      -- SHOWN, at alpha 0. An AnimationGroup on a hidden frame does not play, which would
      -- make the control report exactly what a refusal reports.
      animHost:SetPoint("BOTTOMLEFT", UIParent, "BOTTOMLEFT", 4, 4)
      animHost:SetAlpha(0)
      animHost:Show()
      animLog = buildSlot(animHost, animInit)

      -- The control: same construction, on the same shown host, NEVER handed over.
      local cHost = CreateFrame("Frame", nil, animHost)
      cHost:SetSize(TILE, TILE)
      cHost:SetPoint("TOPLEFT", animHost, "TOPLEFT", 0, 0)
      cHost:Show()
      local cWrap, _, cAg = makeAnimated(cHost, 1.0, 0.4, 0.2)
      local cOk, cErr = pcall(function() cAg:Play() end)
      if cOk then animLog.controlPlay = "accepted"
      else animLog.controlPlay = "REFUSED: " .. tostring(cErr) end
      animLog.controlWrap = type(cWrap)
      animSubjects = animSubjects or {}
      animSubjects.controlAg = cAg
      animSubjects.controlWrap = cWrap
    end

    local s = animSubjects or {}
    local controlPlaying = probeGetter(s.controlAg, "IsPlaying")

    if animLog.init == 0 then
      return {
        measured = false,
        container = animLog.container,
        slot = animLog.slot,
        why = "initializeFrame never ran, so nothing was ever handed over and the armed half "
          .. "does not exist. Check `container`/`slot`, /reload and re-fly.",
      }
    end
    if controlPlaying ~= "true" then
      -- DECLINE. If the CONTROL is not playing, the lab's own animation harness is not
      -- running, and "armed is not playing" would then be indistinguishable from a refusal.
      return {
        measured = false,
        container = animLog.container,
        slot = animLog.slot,
        handover = animLog.handover,
        play = animLog.play,
        control_IsPlaying = controlPlaying,
        why = "the CONTROL AnimationGroup — built identically and never handed over — does "
          .. "not report playing (" .. tostring(controlPlaying) .. "), so the armed reading "
          .. "cannot be attributed. The host must be visible for a group to play; re-fly "
          .. "after a /reload, and if it repeats the lab's animation harness is the subject, "
          .. "not the pandemic sink.",
      }
    end

    return {
      measured = true,
      container = animLog.container,
      slot = animLog.slot,
      setUnit = animLog.setUnit,
      initFired = animLog.init,
      addPandemicRegion = animLog.addPandemicRegion or "initializeFrame never ran",
      handover = animLog.handover,
      play = animLog.play,
      ticker = animLog.ticker,
      tickerTicks = animTicks or 0,
      tickerLive = type(animTicker),
      controlPlay = animLog.controlPlay,
      control_IsPlaying = controlPlaying,
      armed_IsPlaying = probeGetter(s.ag, "IsPlaying"),
      armed_IsPaused = probeGetter(s.ag, "IsPaused"),
      armed_wrap_IsShown = probeGetter(s.wrap, "IsShown"),
      armed_wrap_GetAlpha = probeGetter(s.wrap, "GetAlpha"),
      button_IsShown = probeGetter(s.button, "IsShown"),
      armedPlayingIsAmbiguous = "READ WITH CARE: a group stops when its frame is hidden, so "
        .. "armed_IsPlaying = false may mean the client closed the refresh window rather than "
        .. "that anything was refused. Only `handover`, `play`, `ticker` and the control are "
        .. "unambiguous here.",
      eyeball = "NOT MEASURED: whether the pulse/flipbook is VISIBLE on the tile, and whether "
        .. "it resumes when the refresh window opens. No API reports rendered pixels on this "
        .. "sink; the only oracle is a human watching a dot run down.",
      why = "Acceptance, object creation and a controlled IsPlaying reading only.",
    }
  end,
}

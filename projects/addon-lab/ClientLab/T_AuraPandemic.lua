-- T_AuraPandemic.lua — does the client drive a cap-owned texture from its own refresh window?
--
-- Open: `AddPandemicRegion(region)` adds SecretAspect.Shown to any Region and the client then
-- calls `SetShown(IsInPandemicWindow())` on it every frame
-- (`Blizzard_CustomAuraButton.lua:236-248`, `:567-573`). The window is Blizzard's real one,
-- computed as `GetRefreshExtendedDuration - GetAuraBaseDuration` (`:612-628`), NOT the community
-- 30% rule of thumb.
-- The form this gates: ../../combat-assist/specs/pattern-shelf.md S9.
--
-- ⚠ WHY IT MATTERS MORE THAN IT LOOKS. Every other sealed form makes cap author a threshold — a
-- curve break point, a breakpoint table — and every authored threshold is a thing to get wrong.
-- This one has none. It is also the only sealed form that reaches cap's OWN ART rather than text:
-- a Texture qualifies, so no numeral and no font trick.
--
-- ⚠ TWO REGISTRATIONS, ON PURPOSE, SHARING ONE ID. The `ns.Ask` below is the eyeball, because
-- whether a pixel appeared is secret and always will be. The `ns.Test` beside it records the
-- PLUMBING, which is not secret at all: whether the template exists, whether each call was
-- accepted, whether `initializeFrame` ever fired, and what type `AddPandemicRegion` is on this
-- build. Those are facts about OUR code path, and leaving them unrecorded meant a blank panel
-- could mean six different things and the only instrument was a human describing a black box.

local ADDON, ns = ...

-- ⚠ THE AURA ID IS NOT THE CAST ID, and this cost a whole flight. `includeSpellIDs` matches the
-- aura actually sitting on the target; Immolate is cast as `348` and applies a DoT whose own id is
-- `157736`, and Wither is cast as `445468` and applies `445474`. Filtering on the cast id matches
-- nothing, forever, and looks exactly like a refused call.
-- Our own KB says so at knowledge/addon-dev/cooldown-manager.md:588-596, which is where the CDM's
-- two Immolate rows (the cast row and the DoT row) are pulled apart for the same reason.
-- Both forms are listed anyway: the cast ids cost nothing and a build that ever unified them
-- would otherwise fail silently.
local IMMOLATE_CAST, IMMOLATE_DOT = 348, 157736
local WITHER_CAST, WITHER_DOT = 445468, 445474
local TILE, CELL_W, CELL_X0 = 44, 150, 6

local function dotIds()
  return {
    [IMMOLATE_DOT] = true, [WITHER_DOT] = true,
    [IMMOLATE_CAST] = true, [WITHER_CAST] = true,
  }
end

--- Build one container+slot and report every plain fact about it.
--
-- `filters == nil` means NO spell filter: every harmful aura the player put on the target. That
-- tile is the discriminator — if it fills and the filtered ones do not, the ids are wrong; if
-- nothing fills, nothing is binding at all and the ids are innocent.
local function build(parent, filters, withMark)
  local log = { init = 0, mark = "not attempted" }

  local ok, container = pcall(CreateFrame, "AuraContainer", nil, parent,
                              "CustomAuraContainerTemplate")
  log.container = ok and type(container) or ("FAILED: " .. tostring(container))
  if not ok or not container then return nil, log end
  -- ⚠ SetAllPoints, and that is NOT T_TargetAuras.lua's "one anchor, never SetAllPoints" — that
  -- is a GROUP rule, where the flow layout calls `container:SetSize` for you
  -- (Blizzard_CustomAuraContainer.lua:678-681). A SLOT runs no layout: `AddAuraSlot` creates ONE
  -- frame via a batchSize=1 provider and hands it back unanchored (:400-421, :652-665), so
  -- sizing the container and anchoring the button are both the caller's job.
  container:SetAllPoints(parent)

  local function initButton(button)
    log.init = log.init + 1
    -- ⚠ FIRST, and never removed — and on a SLOT it must be ANCHORED here too, because there is
    -- no layout to place it and a sized-but-unanchored button draws nothing at all.
    button:SetSize(TILE, TILE)
    button:SetAllPoints(container)

    -- The method surface, recorded from the only window that can see a button. If
    -- `AddPandemicRegion` is absent on this build that IS the answer, and it must be legible
    -- rather than inferred from an empty tile.
    log.hasPandemic = type(button.AddPandemicRegion)
    log.hasIcon = type(button.SetIcon)
    log.hasSwipe = type(button.SetDurationCooldown)

    local icon = button:CreateTexture(nil, "ARTWORK")
    icon:SetAllPoints(button)
    button:SetIcon(icon)

    local swipe = CreateFrame("Cooldown", nil, button, "CooldownFrameTemplate")
    swipe:SetAllPoints(button)
    swipe:SetHideCountdownNumbers(true)
    button:SetDurationCooldown(swipe)

    if not withMark then return end

    -- Deliberately UNMISSABLE and deliberately not subtle: this asks whether the region is driven
    -- at all, not whether a treatment is pretty. A thin border would leave "did not appear" and
    -- "appeared and I missed it" indistinguishable, the one outcome this cannot afford.
    local mark = button:CreateTexture(nil, "OVERLAY")
    mark:SetPoint("TOPLEFT", button, "TOPLEFT", -3, 3)
    mark:SetPoint("BOTTOMRIGHT", button, "BOTTOMRIGHT", 3, -3)
    mark:SetColorTexture(1.0, 0.72, 0.20, 0.85)
    local fine, err = pcall(function() button:AddPandemicRegion(mark) end)
    log.mark = fine and "accepted" or ("REFUSED: " .. tostring(err))
    if not fine then
      -- It never became a sink, so hiding it is still legal, and stops a permanently-on orange
      -- block reading as "the window is always open".
      mark:Hide()
    end
  end

  local slotOk, slotFrame = pcall(function()
    return container:AddAuraSlot("dot", "HARMFUL", {
      candidateFilters = filters,
      initializeFrame = initButton,
    })
  end)
  log.slot = slotOk and type(slotFrame) or ("FAILED: " .. tostring(slotFrame))

  -- SetUnit LAST of the wiring calls: it re-evaluates event registrations
  -- (mined-pending-verification.md:221).
  local unitOk, unitErr = pcall(function() container:SetUnit("target") end)
  log.setUnit = unitOk and "ok" or ("FAILED: " .. tostring(unitErr))
  local upOk, upErr = pcall(function() container:UpdateAllAuras() end)
  log.update = upOk and "ok" or ("FAILED: " .. tostring(upErr))

  return container, log
end

-- ── the programmatic half ────────────────────────────────────────────────────
-- Built once on a hidden host. A build per run would leak frames and re-measure the constructor
-- instead of the thing under test (the pattern T_TargetAuras.lua established).
local probeHost, probeLog

ns.Test{
  id = "aura-container-pandemic-region",
  anchor = "cooldown-manager.md:1303",
  bucket = "secret",
  question = "Plumbing only: does the slot build, does initializeFrame fire, and is "
    .. "AddPandemicRegion a function that accepts a Texture?",
  run = function()
    if not probeLog then
      probeHost = CreateFrame("Frame", nil, ns.G("UIParent"))
      probeHost:SetSize(TILE, TILE)
      probeHost:SetPoint("CENTER")
      probeHost:Hide()
      local _, log = build(probeHost, dotIds(), true)
      probeLog = log
    end
    local exists = ns.G("UnitExists")
    return {
      measured = true,
      container = probeLog.container,
      slot = probeLog.slot,
      -- ⚠ For a SLOT this must be 1: `CreateAuraSlotFrame` uses a batchSize=1 provider and
      -- acquires immediately, so the callback fires at slot-creation time whether or not any
      -- aura matches. A 0 here means the slot was never created and every tile is blank for a
      -- reason that has nothing to do with pandemic windows.
      initFired = probeLog.init,
      addPandemicRegion = probeLog.hasPandemic or "initializeFrame never ran",
      setIcon = probeLog.hasIcon or "initializeFrame never ran",
      setDurationCooldown = probeLog.hasSwipe or "initializeFrame never ran",
      markRegistration = probeLog.mark,
      setUnit = probeLog.setUnit,
      updateAllAuras = probeLog.update,
      -- Context for reading the above, not a result: a probe run with no target says nothing
      -- about whether an aura would have bound.
      hadTargetAtRun = (exists and exists("target")) and "yes" or "no",
      why = "Plumbing only. Whether a pixel appeared is secret and is the ns.Ask's job.",
    }
  end,
}

-- ── the eyeball half ─────────────────────────────────────────────────────────
local function tile(canvas, index, title, filters, withMark, expect)
  local cx = CELL_X0 + index * CELL_W

  local function caption(text, y, font)
    local fs = canvas:CreateFontString(nil, "OVERLAY", font or "GameFontHighlightSmall")
    fs:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx, y)
    fs:SetWidth(CELL_W - 8)
    fs:SetJustifyH("CENTER")
    fs:SetWordWrap(true)
    fs:SetText(text)
    canvas.regions[#canvas.regions + 1] = fs
    return fs
  end
  caption(title, -38)

  local holder = CreateFrame("Frame", nil, canvas)
  holder:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx + (CELL_W - 8 - TILE) / 2, -56)
  holder:SetSize(TILE, TILE)
  canvas.kids[#canvas.kids + 1] = holder
  -- An outlined slot. An empty TILE is a result; an empty PANEL is a bug report with no
  -- information in it, and the two must never look alike.
  if ns.UI and ns.UI.edge then ns.UI.edge(holder, 0.35, 0.35, 0.45, 0.9) end

  caption(expect, -(56 + TILE + 4), "GameFontDisableSmall")

  local container, log = build(holder, filters, withMark)

  local line = canvas:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  line:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx, -(56 + TILE + 30))
  line:SetWidth(CELL_W - 8)
  line:SetJustifyH("CENTER")
  line:SetWordWrap(true)
  canvas.regions[#canvas.regions + 1] = line

  -- ⚠ A BLANK TILE HAS SIX CAUSES and they must not look alike: no target, no dot on it, wrong
  -- spell ids, the method missing, the call refused, or the region genuinely not driven. The
  -- first flight could tell none of them apart, which is why it produced "showing nothing"
  -- instead of a finding.
  local unitExists = ns.G("UnitExists")
  local function status()
    if type(log.container) == "string" and log.container:find("FAILED") then
      line:SetText("|cffff5050" .. log.container .. "|r"); return
    end
    if type(log.slot) == "string" and log.slot:find("FAILED") then
      line:SetText("|cffff5050" .. log.slot .. "|r"); return
    end
    if log.init == 0 then
      line:SetText("|cffff5050initializeFrame never ran|r"); return
    end
    if withMark and log.mark ~= "accepted" then
      line:SetText("|cffff5050" .. tostring(log.mark) .. "|r"); return
    end
    if not (unitExists and unitExists("target")) then
      line:SetText("|cffffcc00no target|r"); return
    end
    line:SetText("built ok, init x" .. log.init)
  end
  status()

  -- The container registers UNIT_AURA for its unit only while VISIBLE
  -- (Blizzard_AuraContainer.lua:157-166) and NOTHING re-runs it on a target change — switching
  -- target fires no UNIT_AURA, so a panel opened before you targeted the dummy sits stale.
  local events = CreateFrame("Frame", nil, canvas)
  events:RegisterEvent("PLAYER_TARGET_CHANGED")
  events:RegisterEvent("PLAYER_ENTERING_WORLD")
  events:SetScript("OnEvent", function()
    if container then pcall(function() container:UpdateAllAuras() end) end
    status()
  end)
  canvas.kids[#canvas.kids + 1] = events
end

ns.Ask.Register{
  id = "aura-container-pandemic-region",
  anchor = "cooldown-manager.md:1303",
  bucket = "secret",
  question = "With your dot ticking on the dummy: which tiles show an icon, and does the orange "
    .. "block on the right appear ONLY near the end?",
  note = "Destruction, on a dummy. Open this OUT OF COMBAT, target the dummy, pull, cast Immolate "
    .. "(or Wither) and watch it run down WITHOUT refreshing -- the orange block should stay "
    .. "hidden most of the duration and switch on near the end. Refresh inside that window and it "
    .. "should go away as the timer resets. Left tile takes ANY harmful effect you applied and is "
    .. "the control: if it fills and the middle one does not, the spell ids are wrong; if nothing "
    .. "fills, nothing is binding at all. Leave combat before answering.",
  options = { "all three filled, and the block appeared only near the end",
              "all three filled, but the block was on the whole time",
              "all three filled, but the block never appeared",
              "only the left tile filled",
              "no tile filled at all" },
  setup = function(canvas)
    canvas.kids, canvas.regions = canvas.kids or {}, canvas.regions or {}

    local head = canvas:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    head:SetPoint("TOPLEFT", canvas, "TOPLEFT", 8, -6)
    head:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -8, -6)
    head:SetJustifyH("LEFT")
    head:SetWordWrap(true)
    head:SetText("The game decides when the refresh window is open and switches the block on "
      .. "itself. This addon hands it a texture and never learns whether it drew.")
    canvas.regions[#canvas.regions + 1] = head

    tile(canvas, 0, "any dot of yours", { isFromPlayerOrPlayerPet = true }, false,
         "icon whenever you have any dot up")
    tile(canvas, 1, "immolate only",
         { includeSpellIDs = dotIds(), isFromPlayerOrPlayerPet = true }, false,
         "icon only for Immolate / Wither")
    tile(canvas, 2, "immolate + block",
         { includeSpellIDs = dotIds(), isFromPlayerOrPlayerPet = true }, true,
         "same, plus orange near the end")
  end,
}

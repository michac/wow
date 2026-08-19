-- T_TargetAuras.lua — the sanctioned AuraContainer path, exercised from tainted addon code.
--
-- Open: does an addon-created container survive taint IN COMBAT, is `includeSpellIDs` honoured
-- on an enemy, and do the duration sinks fill.
-- The route and the seal it replaces: security-taint-and-restricted-data.md §3.5, §4.7.1.
--
-- ⚠ INVARIANT: nothing here may be a predicate. A button becomes forbidden while auras are
-- secret and its `IsShown` returns a secret, so this route DISPLAYS and never answers. A test
-- here that appears to read a button's state is a bug in the test.

local ADDON, ns = ...

-- Candidate DoTs a Retribution Paladin puts on a target. A SET, not a single id: the id a
-- talent carries is not always the id of the aura it applies.
local CANDIDATE_IDS = { 383344, 383346, 343527, 20271, 231663 }

local function idSet()
  local t = {}
  for _, id in ipairs(CANDIDATE_IDS) do t[id] = true end
  return t
end

-- One container per host. The lab re-runs tests every 3 s while a pull lasts, so a build
-- per run would leak frames and re-run the very construction path being measured.
local built, buildLog = nil, nil

-- Its own hidden parent, so construction does not depend on the panel being open. The panel
-- builds a SECOND container on its canvas; neither needs the other to have run.
local host

-- Counted in `initializeFrame`. See test 2: this must NOT track the number of auras.
local initCalls = 0

-- `initializeFrame` is the only window into a button (§3.5): everything it will ever need is
-- created here, and the engine writes the regions we hand it.
local BUTTON_SIZE = 40

local function initButton(button)
  initCalls = initCalls + 1
  -- ⚠ FIRST, and never removed: the container does not size its buttons, and every symptom
  -- of forgetting looks like success. security-taint-and-restricted-data.md §3.5.
  button:SetSize(BUTTON_SIZE, BUTTON_SIZE)

  local icon = button:CreateTexture(nil, "ARTWORK")
  icon:SetAllPoints(button)
  button:SetIcon(icon)

  local text = button:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  text:SetPoint("TOP", button, "BOTTOM", 0, -2)
  button:SetDurationText(text)

  local bar = CreateFrame("StatusBar", nil, button)
  bar:SetPoint("TOPLEFT", button, "BOTTOMLEFT", 0, -16)
  bar:SetSize(40, 4)
  bar:SetStatusBarTexture("Interface\\TargetingFrame\\UI-StatusBar")
  bar:SetStatusBarColor(0.9, 0.5, 0.2)
  button:SetDurationBar(bar)
end

--- Build the container and its two groups. Returns a log table describing every step, so a
--- failure names WHICH call refused rather than collapsing to "did not work".
local function buildContainer(parent)
  local log = { steps = {} }
  local function step(name, fn, ...)
    local ok, err = pcall(fn, ...)
    log.steps[#log.steps + 1] = name .. (ok and " = ok" or (" = ERROR: " .. tostring(err)))
    return ok
  end

  local container
  if not step("CreateFrame('AuraContainer')", function()
       container = CreateFrame("AuraContainer", nil, parent, "CustomAuraContainerTemplate")
     end) then
    return log
  end
  container:SetPoint("TOPLEFT", parent, "TOPLEFT", 12, -40)

  -- Group 1 — everything harmful this player applied. No spell ids, so it answers "does the
  -- mechanism work at all" independently of our id guesses.
  step("AddAuraGroup('mine', HARMFUL, isFromPlayerOrPlayerPet)", function()
    container:AddAuraGroup("mine", "HARMFUL", {
      maxFrameCount = 4,
      initializeFrame = initButton,
      candidateFilters = { isFromPlayerOrPlayerPet = true },
      layout = { elementWidth = 40, elementHeight = 40 },
    })
  end)

  -- Group 2 — the same, narrowed to spell ids. If group 1 populates and group 2 does not,
  -- the ids are wrong and NOT the mechanism, which is why both exist.
  step("AddAuraGroup('byid', HARMFUL, includeSpellIDs)", function()
    container:AddAuraGroup("byid", "HARMFUL", {
      maxFrameCount = 4,
      initializeFrame = initButton,
      candidateFilters = { includeSpellIDs = idSet() },
      layout = { elementWidth = 40, elementHeight = 40 },
    })
  end)

  step("SetUnit('target')", function() container:SetUnit("target") end)
  step("UpdateAllAuras()", function() container:UpdateAllAuras() end)

  log.container = container
  return log
end

-- ⚠ The combat flag belongs to the BUILD, not to the report. A container constructed out of
-- combat says nothing about construction under lockdown, and a cached log rendered with the
-- caller's current flag would claim it did — so an out-of-combat build is rebuilt once a pull
-- starts, and the log carries the state it was actually built in.
local function ensureBuilt()
  local combat = InCombatLockdown() and true or false
  if not buildLog or (combat and not buildLog.combat) then
    host = host or CreateFrame("Frame", nil, UIParent)
    host:SetSize(320, 80)
    host:SetPoint("CENTER")
    host:Hide()                     -- constructible is the question, not visible
    buildLog = buildContainer(host)
    buildLog.combat = combat
    built = buildLog.container
  end
  return built, buildLog
end

-- 1 ------------------------------------------------------------------------------------
-- Can an addon construct the sanctioned display at all, under taint, in combat? Every step is
-- reported by name. An out-of-combat build DECLINES: it answers a smaller question than the
-- one asked, and filing it as the answer would end the test before the pull that tests it.
ns.Test{
  id = "auracontainer-constructs-from-addon",
  anchor = "security-taint-and-restricted-data.md:§3.5",
  bucket = "call",
  question = "Can tainted addon code create an AuraContainer, add a spell-ID-filtered HARMFUL "
    .. "group on the target, and set a unit — and does any step refuse?",
  run = function()
    if type(CreateFrame) ~= "function" then
      return { measured = false, why = "no CreateFrame" }
    end
    local _, log = ensureBuilt()
    local out = { measured = true, combat = log.combat }
    for i, s in ipairs(log.steps) do out[string.format("step %d", i)] = s end
    if #log.steps == 0 then
      out.measured, out.why = false, "no steps ran"
    elseif not log.combat then
      out.measured, out.why = false,
        "built out of combat — the question is whether it survives under lockdown; retry in a pull"
    end
    return out
  end,
}

-- 2 ------------------------------------------------------------------------------------
-- Does the container tell us anything it should not? A callback count must not track the aura
-- count (§3.5's pre-allocated batch). ⚠ This can never CONCLUDE from one sample: the container
-- is built once, so the number cannot vary within a session, and a fixed batch and a tracking
-- count look identical from a single reading. It reports the value and declines; the comparison
-- is a human's, across sessions with different numbers of DoTs applied.
ns.Test{
  id = "auracontainer-initializeframe-count-does-not-track-auras",
  anchor = "security-taint-and-restricted-data.md:§3.5",
  bucket = "secret",
  question = "Does the number of initializeFrame callbacks reveal how many auras are on the "
    .. "target — i.e. is the pre-allocation batch doing its job?",
  run = function()
    ensureBuilt()
    local why = "one reading cannot tell a fixed pre-allocation batch from a count that tracks "
      .. "auras, and the container is built once so this number cannot vary within a session; "
      .. "compare it across sessions with different numbers of DoTs applied"
    if initCalls == 0 then
      why = "no callbacks to count — construction refused, see auracontainer-constructs-from-addon"
    end
    return {
      measured = false,
      why = why,
      combat = InCombatLockdown() and true or false,
      ["initializeFrame calls so far"] = initCalls,
    }
  end,
}

-- Visual ---------------------------------------------------------------------------------
--
-- The instrument that actually answers the question. Nothing here reads a button: the engine
-- fills the icon, the timer text and the bar, and the person says whether they filled.
--
-- Two rows, because they fail differently and the difference is the finding:
--   TOP    — every harmful effect YOU applied. Tests the mechanism, independent of spell ids.
--   BOTTOM — narrowed to a list of specific spell ids. Tests whether id filtering is allowed
--            on an enemy, which is what a per-spec tracker needs.
-- Top populated + bottom empty means our ids are wrong. Both empty means the route is shut.

ns.Ask.Register{
  id = "auracontainer-shows-target-dots",
  anchor = "security-taint-and-restricted-data.md:§3.5",
  bucket = "call",
  question = "After you put damage-over-time effects on a target, do icons with countdown "
    .. "timers appear in EITHER row below?",
  note = "Open this before you pull. Hit a training dummy with Blade of Justice and Judgment. "
    .. "The top row shows every harmful effect you applied; the bottom row is narrowed to a "
    .. "specific list of spells. They can legitimately differ — that is what is being tested.",
  options = { "both rows filled", "only the top row", "only the bottom row",
              "both stayed empty", "can't tell" },
  setup = function(canvas)
    canvas.kids, canvas.regions = canvas.kids or {}, canvas.regions or {}

    local function caption(text, y)
      local fs = canvas:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
      fs:SetPoint("TOPLEFT", canvas, "TOPLEFT", 10, y)
      fs:SetText(text)
      canvas.regions[#canvas.regions + 1] = fs
    end
    caption("EVERYTHING YOU APPLIED", -8)
    caption("ONLY THE LISTED SPELLS", -100)

    -- A container per row. Two groups on ONE container would share a layout and the rows
    -- could not be told apart, which is the entire comparison.
    local function row(y, filters)
      local holder = CreateFrame("Frame", nil, canvas)
      holder:SetPoint("TOPLEFT", canvas, "TOPLEFT", 10, y)
      holder:SetSize(360, 64)
      canvas.kids[#canvas.kids + 1] = holder
      -- An outlined, labelled slot. An empty ROW is a result; an empty PANEL is a bug report
      -- with no information in it, and the two must never look alike.
      if ns.UI and ns.UI.edge then ns.UI.edge(holder, 0.35, 0.35, 0.45, 0.9) end

      local ok, container = pcall(CreateFrame, "AuraContainer", nil, holder,
                                  "CustomAuraContainerTemplate")
      if not ok or not container then
        local err = canvas:CreateFontString(nil, "OVERLAY", "GameFontRedSmall")
        err:SetPoint("TOPLEFT", holder, "TOPLEFT", 0, 0)
        err:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -10, 0)
        err:SetJustifyH("LEFT")
        err:SetWordWrap(true)
        err:SetText("CreateFrame('AuraContainer') failed -> " .. tostring(container))
        canvas.regions[#canvas.regions + 1] = err
        return
      end
      -- ⚠ ONE anchor, never SetAllPoints — the layout sizes the container itself (§3.5).
      container:SetPoint("TOPLEFT", holder, "TOPLEFT", 0, 0)

      -- ⚠ ONE pcall around three calls swallows which one failed, and a rejected group then
      -- looks exactly like "no auras on the target": an empty row and no explanation. Each
      -- call gets its own, and the first failure is printed INTO the panel.
      local failure
      local function try(name, fn)
        if failure then return end
        local fine, err = pcall(fn)
        if not fine then failure = name .. " -> " .. tostring(err) end
      end
      try("AddAuraGroup", function()
        container:AddAuraGroup("row", "HARMFUL", {
          maxFrameCount = 5,
          initializeFrame = initButton,
          candidateFilters = filters,
          layout = { elementWidth = 40, elementHeight = 40 },
        })
      end)
      try("SetUnit('target')", function() container:SetUnit("target") end)
      try("UpdateAllAuras", function() container:UpdateAllAuras() end)

      -- A row that drew nothing must say WHY it drew nothing. Blank is not a result.
      local line = canvas:CreateFontString(nil, "OVERLAY",
        failure and "GameFontRedSmall" or "GameFontDisableSmall")
      line:SetPoint("TOPLEFT", holder, "BOTTOMLEFT", 0, 14)
      line:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -10, 0)
      line:SetJustifyH("LEFT")
      line:SetWordWrap(true)
      line:SetText(failure or "built ok — empty here means nothing matched")
      canvas.regions[#canvas.regions + 1] = line
    end

    row(-28, { isFromPlayerOrPlayerPet = true })
    row(-120, { includeSpellIDs = idSet() })

    local status = canvas:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    status:SetPoint("TOPLEFT", canvas, "TOPLEFT", 10, -196)
    status:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -10, -196)
    status:SetJustifyH("LEFT")
    status:SetWordWrap(true)
    status:SetText("|cff808080The game fills these icons and timers itself — this addon never "
      .. "reads the effects, and cannot.|r")
    canvas.regions[#canvas.regions + 1] = status
  end,
}

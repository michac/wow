-- T_AuraFormatter.lua — can cap author WHICH values of a secret stack count get drawn?
--
-- Open: `SetApplicationCount` with no options shows the count only above 1
-- (`Blizzard_CustomAuraButton.lua:351-368`, the `elseif applications > 1` branch). Passing an
-- `options.formatter` replaces that branch with a piecewise function WE author. Every band cap
-- wants — the complement, a middle band, a label, a colour — is one breakpoint table if a
-- tainted-created formatter is honoured, and nothing at all if it is not.
-- The forms this gates: ../../combat-assist/specs/pattern-shelf.md S7 and S8.
--
-- ⚠ INVARIANT, inherited from T_TargetAuras.lua and just as binding here: nothing in this file
-- may be a predicate. The button is forbidden while its aura is secret and its `IsShown` is
-- itself secret, so this route DISPLAYS and never answers. Every tile below is judged by eye.
--
-- ⚠ WHY THERE IS A CONTROL TILE. Blizzard's default already means "hide below 2". A tile that
-- also hides below 2 looks identical whether our rules ran or were ignored, so such a tile can
-- never prove anything on its own. Tile B is the discriminator: it asks for the number at EVERY
-- value, and the default never prints a "1". One `1` on screen is the whole measurement.

local ADDON, ns = ...

local BACKDRAFT = 117828
-- The Ask panel's canvas is ~460x215 (Ask.lua:81 root 480x500, less margins, header and the
-- option area). Five cells have to fit ACROSS that, so the pitch is fixed here and every cell
-- measures itself from it rather than from a hand-placed x.
local TILE, CELL_W, CELL_X0 = 34, 90, 6

-- Resolved BY STRING: `C_StringUtil` is not in `.luacheckrc`'s curated std, and naming it as an
-- identifier would fail the clean-luacheck house rule. `ns.G` hands back a local.
local function newFormatter()
  local su = ns.G("C_StringUtil")
  if not su or type(su.CreateNumericRuleFormatter) ~= "function" then return nil end
  local ok, f = pcall(su.CreateNumericRuleFormatter)
  if ok then return f end
  return nil
end

-- One tile: its own container, its own button, its own breakpoint table. Returns nothing —
-- everything it has to say, it says in pixels or in the red line under itself.
--
-- `bands == nil` is the CONTROL: no formatter, no options, exactly what cap ships today.
local function tile(canvas, index, title, at1, at2, bands)
  local cx = CELL_X0 + index * CELL_W

  local function caption(text, y, font)
    local fs = canvas:CreateFontString(nil, "OVERLAY", font or "GameFontHighlightSmall")
    fs:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx, y)
    fs:SetWidth(CELL_W - 6)
    fs:SetJustifyH("CENTER")
    fs:SetText(text)
    canvas.regions[#canvas.regions + 1] = fs
    return fs
  end
  caption(title, -34)

  local holder = CreateFrame("Frame", nil, canvas)
  holder:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx + (CELL_W - 6 - TILE) / 2, -48)
  holder:SetSize(TILE, TILE)
  canvas.kids[#canvas.kids + 1] = holder
  -- An outlined slot. An empty TILE is a result; an empty PANEL is a bug report carrying no
  -- information, and the two must never look alike.
  if ns.UI and ns.UI.edge then ns.UI.edge(holder, 0.35, 0.35, 0.45, 0.9) end

  -- What this tile SHOULD read at each stack, printed under it. The panel has to be judgeable
  -- without the spec open beside it, or the verdict is really a memory test.
  caption("1 -> " .. at1, -(48 + TILE + 4), "GameFontDisableSmall")
  caption("2 -> " .. at2, -(48 + TILE + 16), "GameFontDisableSmall")

  local ok, container = pcall(CreateFrame, "AuraContainer", nil, holder,
                              "CustomAuraContainerTemplate")
  if not ok or not container then
    local err = canvas:CreateFontString(nil, "OVERLAY", "GameFontRedSmall")
    err:SetPoint("TOPLEFT", holder, "TOPLEFT", 0, 0)
    err:SetWidth(CELL_W - 6)
    err:SetWordWrap(true)
    err:SetText("AuraContainer failed -> " .. tostring(container))
    canvas.regions[#canvas.regions + 1] = err
    return
  end
  -- ⚠ SetAllPoints, and that is NOT the rule T_TargetAuras.lua states. Its "one anchor, never
  -- SetAllPoints" is a GROUP rule: a group runs the flow layout, whose `OnLayoutComplete` calls
  -- `container:SetSize` (Blizzard_CustomAuraContainer.lua:678-681). A SLOT runs no layout at all
  -- — `AddAuraSlot` creates ONE frame via a batchSize=1 provider and returns it (:400-421,
  -- :652-665) — so nothing sizes the container and nothing anchors the button. Both are the
  -- caller's, which is what `cap`'s own `Channel.Arm` does.
  container:SetAllPoints(holder)

  -- ⚠ ONE pcall around several calls swallows WHICH one failed, and a rejected slot then looks
  -- exactly like "the aura is not up". Each call gets its own, and the first failure is printed
  -- into the panel rather than into a log nobody opens.
  local failure
  local function try(name, fn)
    if failure then return end
    local fine, err = pcall(fn)
    if not fine then failure = name .. " -> " .. tostring(err) end
  end

  -- Built ONCE, outside initializeFrame: a formatter is plain authored data with no secret in
  -- it, and rebuilding one per button would measure the constructor instead of the sink.
  local formatter
  if bands then
    formatter = newFormatter()
    if not formatter then
      failure = "C_StringUtil.CreateNumericRuleFormatter unavailable"
    else
      try("SetBreakpoints", function() formatter:SetBreakpoints(bands) end)
    end
  end

  local function initButton(button)
    -- ⚠ FIRST, and never removed: the container does not size its buttons, and every symptom
    -- of forgetting looks like success. On a SLOT it must also be ANCHORED here — there is no
    -- layout to place it, so a sized-but-unanchored button draws nothing at all.
    button:SetSize(TILE, TILE)
    button:SetAllPoints(container)

    local icon = button:CreateTexture(nil, "ARTWORK")
    icon:SetAllPoints(button)
    button:SetIcon(icon)

    local swipe = CreateFrame("Cooldown", nil, button, "CooldownFrameTemplate")
    swipe:SetAllPoints(button)
    swipe:SetHideCountdownNumbers(true)
    button:SetDurationCooldown(swipe)

    local count = button:CreateFontString(nil, "OVERLAY")
    count:SetFont("Fonts\\FRIZQT__.TTF", 16, "OUTLINE")
    count:SetPoint("CENTER", button, "CENTER", 0, 0)
    -- Set BEFORE registration, while the FontString is still ours to touch. `SetApplicationCount`
    -- adds only the Text and Shown aspects, so VertexColor stays writable — but doing it here
    -- keeps that claim out of the measurement.
    count:SetTextColor(1, 1, 1, 1)
    if formatter then
      button:SetApplicationCount(count, { formatter = formatter })
    else
      button:SetApplicationCount(count)
    end
  end

  try("AddAuraSlot", function()
    container:AddAuraSlot("tile", "HELPFUL", {
      candidateFilters = { includeSpellIDs = { [BACKDRAFT] = true } },
      initializeFrame = initButton,
    })
  end)
  try("SetUnit('player')", function() container:SetUnit("player") end)
  try("UpdateAllAuras", function() container:UpdateAllAuras() end)

  if failure then
    local err = canvas:CreateFontString(nil, "OVERLAY", "GameFontRedSmall")
    err:SetPoint("TOPLEFT", canvas, "TOPLEFT", cx, -(48 + TILE + 30))
    err:SetWidth(CELL_W - 6)
    err:SetWordWrap(true)
    err:SetText(failure)
    canvas.regions[#canvas.regions + 1] = err
  end
end

-- ── the programmatic half ────────────────────────────────────────────────────
-- Shares its id with the ns.Ask below, which the registry explicitly allows (lab.py:114-124):
-- the eyeball owns "did a glyph appear", which is secret forever; this owns the PLUMBING, which
-- is not secret at all and should never have been routed through a human describing a panel.
local probeHost, probeLog

ns.Test{
  id = "aura-container-rule-formatter",
  anchor = "security-taint-and-restricted-data.md:951",
  bucket = "secret",
  question = "Plumbing only: does C_StringUtil exist, does a tainted caller get a formatter, and "
    .. "is every band table this test uses ACCEPTED by SetBreakpoints?",
  run = function()
    if not probeLog then
      local log = {}
      local su = ns.G("C_StringUtil")
      log.cStringUtil = type(su)
      log.createFn = su and type(su.CreateNumericRuleFormatter) or "n/a"

      -- Every ruleset the panel draws with, accepted or refused BY NAME. A refusal here is the
      -- difference between "the client ignored our rule" and "we never handed it one", which a
      -- blank tile cannot distinguish and which decides whether S7 is dead or merely mis-authored.
      local sets = {
        showsAtOne = { { threshold = 0, format = "%d" } },
        word       = { { threshold = 0, format = "" }, { threshold = 2, format = "MAX" } },
        colour     = { { threshold = 0, format = "|cffff4040%d|r" },
                       { threshold = 2, format = "|cff40ff70%d|r" } },
        complement = { { threshold = 0, format = "%d" }, { threshold = 2, format = "" } },
      }
      for name, bands in pairs(sets) do
        if not su or type(su.CreateNumericRuleFormatter) ~= "function" then
          log[name] = "no factory"
        else
          local madeOk, f = pcall(su.CreateNumericRuleFormatter)
          if not madeOk then
            log[name] = "CreateNumericRuleFormatter FAILED: " .. tostring(f)
          else
            local setOk, err = pcall(function() f:SetBreakpoints(bands) end)
            log[name] = setOk and "accepted" or ("REFUSED: " .. tostring(err))
          end
        end
      end

      -- Does a slot actually build and does its callback fire? Headless, on a hidden host, built
      -- once — a build per run would re-measure the constructor instead of the sink.
      probeHost = CreateFrame("Frame", nil, ns.G("UIParent"))
      probeHost:SetSize(TILE, TILE)
      probeHost:SetPoint("CENTER")
      probeHost:Hide()
      local inits = 0
      local okC, container = pcall(CreateFrame, "AuraContainer", nil, probeHost,
                                   "CustomAuraContainerTemplate")
      log.container = okC and type(container) or ("FAILED: " .. tostring(container))
      if okC and container then
        container:SetAllPoints(probeHost)
        local slotOk, slotFrame = pcall(function()
          return container:AddAuraSlot("probe", "HELPFUL", {
            candidateFilters = { includeSpellIDs = { [BACKDRAFT] = true } },
            initializeFrame = function(button)
              inits = inits + 1
              button:SetSize(TILE, TILE)
              button:SetAllPoints(container)
              log.setApplicationCount = type(button.SetApplicationCount)
              local fs = button:CreateFontString(nil, "OVERLAY")
              fs:SetFont("Fonts\\FRIZQT__.TTF", 16, "OUTLINE")
              fs:SetPoint("CENTER", button, "CENTER", 0, 0)
              local f = su and su.CreateNumericRuleFormatter and su.CreateNumericRuleFormatter()
              if f then
                pcall(function() f:SetBreakpoints(sets.showsAtOne) end)
                local acc, err = pcall(function()
                  button:SetApplicationCount(fs, { formatter = f })
                end)
                log.optionsAccepted = acc and "accepted" or ("REFUSED: " .. tostring(err))
              else
                log.optionsAccepted = "no formatter to pass"
              end
            end,
          })
        end)
        log.slot = slotOk and type(slotFrame) or ("FAILED: " .. tostring(slotFrame))
        pcall(function() container:SetUnit("player") end)
        pcall(function() container:UpdateAllAuras() end)
      end
      log.initFired = inits
      probeLog = log
    end
    local out = { measured = true,
      why = "Plumbing only. Whether a glyph appeared is secret and is the ns.Ask's job." }
    for k, v in pairs(probeLog) do out[k] = v end
    return out
  end,
}

ns.Ask.Register{
  id = "aura-container-rule-formatter",
  anchor = "security-taint-and-restricted-data.md:951",
  bucket = "secret",
  question = "Backdraft stacks: does tile B show a 1, and does tile D show its numbers in "
    .. "colour?",
  note = "Destruction, on a dummy. Backdraft comes from Conflagrate -- one stack per cast, two "
    .. "at most -- and Incinerate, Chaos Bolt and Soul Fire all SPEND it. Open this out of "
    .. "combat at zero stacks, pull, then cast NOTHING BUT CONFLAGRATE, twice, looking at the "
    .. "tiles after each. Casting a filler in between spends the stack before you have read it. "
    .. "Leave combat before answering. Five tiles, "
    .. "each labelled with what it should read at one stack and at two. A is the control and "
    .. "behaves the way the game always has. B is the one that matters: the game NEVER prints a "
    .. "'1' by itself, so a 1 there means our own rule ran. C should print a word instead of a "
    .. "number. D should print the same numbers in red then green. E should do the opposite of "
    .. "A -- a 1, then nothing.",
  options = { "all five read as labelled",
              "A worked but B, C, D and E did not",
              "the numbers worked but D had no colour",
              "something else -- see chat",
              "can't tell" },
  setup = function(canvas)
    canvas.kids, canvas.regions = canvas.kids or {}, canvas.regions or {}

    local head = canvas:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    head:SetPoint("TOPLEFT", canvas, "TOPLEFT", 10, -6)
    head:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -10, -6)
    head:SetJustifyH("LEFT")
    head:SetWordWrap(true)
    head:SetText("Each tile draws Backdraft with its own display rule. The game fills the "
      .. "number in; this addon never reads it and cannot.")
    canvas.regions[#canvas.regions + 1] = head

    local su = ns.G("C_StringUtil")
    if not su or type(su.CreateNumericRuleFormatter) ~= "function" then
      local gone = canvas:CreateFontString(nil, "OVERLAY", "GameFontRedSmall")
      gone:SetPoint("TOPLEFT", canvas, "TOPLEFT", 10, -40)
      gone:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -10, -40)
      gone:SetJustifyH("LEFT")
      gone:SetWordWrap(true)
      gone:SetText("C_StringUtil.CreateNumericRuleFormatter is MISSING on this build -- every "
        .. "tile except A will be empty for that reason and not because a rule was refused.")
      canvas.regions[#canvas.regions + 1] = gone
    end

    -- A · the control. No formatter at all: this is cap today, and it is what B is read against.
    tile(canvas, 0, "A control", "nothing", "2", nil)
    -- B · THE DISCRIMINATOR. The default never prints a 1. If a 1 appears, our rule ran.
    tile(canvas, 1, "B shows at 1", "1", "2",
         { { threshold = 0, format = "%d" } })
    -- C · a band that is not a number at all, so a band can carry a label or a glyph.
    tile(canvas, 2, "C word", "nothing", "MAX",
         { { threshold = 0, format = "" }, { threshold = 2, format = "MAX" } })
    -- D · colour escapes inside the band. The route S8 prefers if the client does not strip them.
    tile(canvas, 3, "D colour", "red 1", "green 2",
         { { threshold = 0, format = "|cffff4040%d|r" },
           { threshold = 2, format = "|cff40ff70%d|r" } })
    -- E · the COMPLEMENT — show low, hide high. The exact inverse of the default, and the shape
    -- Power Siphon's `stack<=1` rung needs. `pattern-shelf.md` S2 called this impossible.
    tile(canvas, 4, "E complement", "1", "nothing",
         { { threshold = 0, format = "%d" }, { threshold = 2, format = "" } })

    local foot = canvas:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
    foot:SetPoint("TOPLEFT", canvas, "TOPLEFT", 8, -166)
    foot:SetPoint("TOPRIGHT", canvas, "TOPRIGHT", -8, -166)
    foot:SetJustifyH("LEFT")
    foot:SetWordWrap(true)
    foot:SetText("|cff808080If B stays blank at one stack, no custom rule was honoured and the "
      .. "answer is no -- report that even if C, D or E happened to look right.|r")
    canvas.regions[#canvas.regions + 1] = foot
  end,
}

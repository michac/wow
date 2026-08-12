-- RETIRED FROM ClientLab.toc ON 12.1. This settled visual mock is completed product
-- design rather than a live evidence question. Removing it keeps the lab load path
-- limited to active tests and their evidence plumbing.
--
-- Mock — one candidate tier design, realised. Five real spell icons at true Cooldown
-- Manager size: four tiers as a monotone ladder, then an animated number.
--
-- A MOCKUP, not a lab. No steppers, no A/B, no readouts — the only control is the
-- greyscale collapse, which is the one question this panel exists to answer.
--
-- INVARIANT: nothing in a product addon may depend on ClientLab.

local ADDON, ns = ...

ns.Mock = {}
local M = ns.Mock

local GetSpellTexture = ns.G("C_Spell.GetSpellTexture")
local SCALE_MODE = ns.G("Enum.FontStringScaleAnimationMode")

local KEY = "labmock"
local GAP = 26

-- ⚠ THE TROUGH INVARIANT, AND THE ONE NUMBER THAT ENFORCES IT. The pulse multiplies its
-- tier's alpha, so depth eats separation: at 0.68 MEDIUM's trough (0.530) still clears
-- LOW's peak (0.500) by 0.030. At 0.65 that margin is 0.007, which is not a margin.
-- HIGH-vs-MEDIUM crosses by design and is told apart by RATE, the primary channel.
local PULSE_FLOOR = 0.68

-- proc-loop first: it is the ring that was flown and chosen, and ants stays as contrast.
-- ⚠ BOTH NEED AN EXPLICIT `scale`: the registry path passes `o.scale or def.scale` and
-- neither def declares one, so a ring left to itself draws at HOST size and sits on the
-- icon edge instead of haloing outside it. These are Blizzard's own numbers for the two
-- atlases — 66px over a 45px button, and the alert frame's 1.4x.
local BASES = {
  { name = "proc-loop", glow = "blizzard", scale = 1.4 },
  { name = "ants", glow = "blizzardants", scale = 1.47 },
}

-- One word to change if OUTLINE reads thin at icon size.
local OUTLINE = "OUTLINE"

-- A Demonology set, so the mockup tells its own story without this conversation: the proc
-- you press now, the builder, the filler you press when nothing else is up, and a utility
-- that is not in the rotation at all. A texture that will not resolve draws a swatch.
local CELLS = {
  { spell = 264178, label = "HIGH",   gloss = "press now",    tier = "HIGH" },
  { spell = 105174, label = "MEDIUM", gloss = "builder",      tier = "MEDIUM" },
  { spell = 686,    label = "LOW",    gloss = "filler",       tier = "LOW" },
  { spell = 755,    label = "NONE",   gloss = "off-rotation", tier = "NONE" },
  { spell = 265187, label = "number", gloss = "animated",     tier = "NUMBER" },
}

-- MOTION is the ladder: 2.5 Hz -> 1.2 Hz -> 0.5 Hz -> no ring at all. Luminance is
-- monotone underneath and survives peripheral vision and dichromacy, so hue is
-- reinforcement and never the signal; three different rates also mean the set can never
-- flash as one area. LOW and NONE are different STATES, not two depths of one — in the
-- rotation but not now, versus not in it — so the step between them is the PRESENCE of a
-- ring and of motion, seen at once, where two veil depths must be compared.
local TIERS = {
  HIGH   = { hue = { 1.00, 0.92, 0.55 }, alpha = 1.00, hz = 2.5 },
  MEDIUM = { hue = { 0.45, 0.70, 0.95 }, alpha = 0.78, hz = 1.2 },
  -- cap's own HOLD hue: a neutral slate in no tier's hue family, so gold reads highest,
  -- blue middle, and neutral present-but-unranked. Hue stays redundant to luminance.
  LOW    = { hue = { 0.80, 0.82, 0.88 }, alpha = 0.50, hz = 0.5 },
  NONE   = { veil = 0.60 },
}

local panel, cells
local greyOn, baseIdx = false, 1
local notes = {}

local function note(s)
  for _, existing in ipairs(notes) do
    if existing == s then return end
  end
  notes[#notes + 1] = s
end

--- The whole point of the greyscale control: collapse hue to luminance and see whether
--- the ladder still ranks. If it does not, it cannot be ranked by a dichromat either.
local function hue(c)
  if not greyOn then return c[1], c[2], c[3] end
  local y = 0.299 * c[1] + 0.587 * c[2] + 0.114 * c[3]
  return y, y, y
end

-- ⚠ Alpha is SetFromAlpha / SetToAlpha but Scale is SetScaleFrom / SetScaleTo, and
-- SetFromScale / SetToScale do not exist at 12.0.7 — so a setter is probed, never assumed.
-- An animation that silently never received its endpoints looks exactly like a live one.
local function call(obj, name, ...)
  local m = obj[name]
  if type(m) ~= "function" then
    note(name .. " absent")
    return false
  end
  local ok, err = pcall(m, obj, ...)
  if not ok then note(name .. ": " .. tostring(err)) end
  return ok
end

local function group(obj, kind)
  local okG, g = pcall(function() return obj:CreateAnimationGroup() end)
  if not okG or not g then
    note("no AnimationGroup on this object")
    return nil
  end
  local okA, a = pcall(function() return g:CreateAnimation(kind) end)
  if not okA or not a then
    note(kind .. ": CreateAnimation failed")
    return nil
  end
  return g, a
end

-- BOUNCE plays an animation forward then back, so ONE animation of half the cycle is the
-- whole pulse and no timer runs. IN_OUT is the ramp: always fading, never mostly-solid.
local function pulse(halo, hz)
  local g, a = group(halo, "Alpha")
  if not g then return nil end
  call(a, "SetDuration", 0.5 / hz)
  call(a, "SetSmoothing", "IN_OUT")
  call(a, "SetFromAlpha", PULSE_FLOOR)
  call(a, "SetToAlpha", 1)
  call(g, "SetLooping", "BOUNCE")
  return g
end

-- Vertex mode scales the rendered quad instead of re-rasterising per step: softer, and
-- the only one of the two that fluctuates continuously rather than stepping font sizes.
local function breathe(fs)
  if SCALE_MODE and SCALE_MODE.Vertex ~= nil then
    call(fs, "SetScaleAnimationMode", SCALE_MODE.Vertex)
  else
    note("Enum.FontStringScaleAnimationMode absent — glyph scaling left at its default")
  end
  local g, s = group(fs, "Scale")
  if not g then return nil end
  call(s, "SetDuration", 0.6)
  call(s, "SetSmoothing", "IN_OUT")
  -- Straddles rest rather than starting there, so the number shrinks as well as grows
  -- instead of sitting at the bottom of its own range.
  call(s, "SetScaleFrom", 0.88, 0.88)
  call(s, "SetScaleTo", 1.15, 1.15)
  call(s, "SetOrigin", "CENTER", 0, 0)
  call(g, "SetLooping", "BOUNCE")
  return g
end

-- Painting -----------------------------------------------------------------------

--- Cleared with the glow that was APPLIED, not the one currently selected: the base can
--- change between the two calls and Proc:Clear resolves its teardown off that name.
local function stopGlow(cell)
  local lib = ns.Glow and ns.Glow.lib
  if lib and cell.glowing then
    pcall(lib.Proc.Clear, lib.Proc, cell.halo, { glow = cell.glowing, key = KEY })
    cell.glowing = nil
  end
end

local function paint(cell)
  local tier = TIERS[cell.tier]
  stopGlow(cell)
  pcall(cell.art.SetDesaturated, cell.art, greyOn)
  -- Show/Hide, never SetShown: SetShown is IsProtectedFunction.
  cell.veil:Hide()
  if tier and tier.veil then
    -- NONE draws no ring on purpose: dimming the un-emphasised raises relative contrast
    -- with no motion and no flash, and it is the absence of a ring that separates an
    -- off-rotation ability from LOW's steady one.
    cell.veil:SetColorTexture(0, 0, 0, tier.veil)
    cell.veil:Show()
    return
  end
  if not (tier and tier.hue) then return end
  local lib = ns.Glow and ns.Glow.lib
  if not lib then
    note("LibOrbitGlow unavailable — the ringed tiers show hue and alpha only")
    return
  end
  local base = BASES[baseIdx]
  local r, g, b = hue(tier.hue)
  if pcall(lib.Apply, cell.halo, base.glow, { key = KEY, scale = base.scale,
                                              color = { r, g, b, tier.alpha },
                                              loop = true }) then
    cell.glowing = base.glow
  end
end

local function repaint()
  for _, cell in ipairs(cells or {}) do
    paint(cell)
    if cell.fs then
      local r, g, b = hue({ 1.00, 0.92, 0.55 })
      cell.fs:SetTextColor(r, g, b)
    end
  end
  if panel then
    panel.grey.text:SetText(greyOn and "|cffffd100[x] greyscale|r" or "[ ] greyscale")
    for i, b in ipairs(panel.baseButtons or {}) do
      b.text:SetText(i == baseIdx and ("|cffffd100" .. BASES[i].name .. "|r") or BASES[i].name)
    end
    panel.note:SetText(#notes > 0
      and ("|cffff8844" .. table.concat(notes, " · ") .. "|r")
      or ("|cff808080icons at %d×%d, %s|r"):format(panel.w, panel.h, panel.why))
  end
end

-- Building -------------------------------------------------------------------------

local function makeCell(root, def, x, y, w, h)
  local cell = { tier = def.tier }

  cell.frame = CreateFrame("Frame", nil, root)
  cell.frame:SetPoint("TOPLEFT", root, "TOPLEFT", x, y)
  cell.frame:SetSize(w, h)

  cell.art = cell.frame:CreateTexture(nil, "ARTWORK")
  cell.art:SetAllPoints(cell.frame)
  local path
  if GetSpellTexture then
    local ok, p = pcall(GetSpellTexture, def.spell)
    if ok and (type(p) == "string" or type(p) == "number") then path = p end
  end
  if path then
    cell.art:SetTexture(path)
  else
    cell.art:SetColorTexture(0.25, 0.22, 0.18, 1)
    note(("spell %d has no texture"):format(def.spell))
  end

  cell.veil = cell.frame:CreateTexture(nil, "OVERLAY")
  cell.veil:SetAllPoints(cell.frame)
  cell.veil:Hide()

  -- The glow hangs on its OWN frame, so pulsing it never fades the icon underneath.
  cell.halo = CreateFrame("Frame", nil, root)
  cell.halo:SetPoint("CENTER", cell.frame, "CENTER", 0, 0)
  cell.halo:SetSize(w, h)
  cell.halo:SetFrameLevel(cell.frame:GetFrameLevel() + 2)

  -- Tier name AND a one-word gloss, so the panel is legible without the conversation
  -- that produced it.
  local label = root:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  label:SetPoint("TOP", cell.frame, "BOTTOM", 0, -5)
  label:SetJustifyH("CENTER")
  label:SetText(("%s\n|cff808080%s|r"):format(def.label, def.gloss))

  if def.tier == "NUMBER" then
    cell.fs = cell.frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    cell.fs:SetPoint("CENTER", cell.frame, "CENTER", 0, 0)
    cell.fs:SetJustifyH("CENTER")
    cell.fs:SetText("12")
    -- The outline is the primary edge. Re-set off GetFont so the cell keeps whatever
    -- font object it was built with, and CHECK THE RETURN: SetFont carries
    -- RequiresValidFontAsset + RequiresValidFontHeight, and a silently ignored call
    -- looks exactly like an outline that is too subtle — which is the bug we would
    -- then chase instead of this one.
    local okGet, fontPath, fontSize = pcall(cell.fs.GetFont, cell.fs)
    if okGet and fontPath then
      local ok, applied = pcall(cell.fs.SetFont, cell.fs, fontPath, fontSize, OUTLINE)
      if not (ok and applied ~= false) then
        note(("SetFont(%s) refused — the number has no outline"):format(OUTLINE))
      end
    else
      note("GetFont returned no path — the number keeps its font object's flags")
    end
    -- Faint, and under the outline: two heavy black edges at icon size muddy the glyph.
    cell.fs:SetShadowColor(0, 0, 0, 0.45)
    cell.fs:SetShadowOffset(1, -1)
    cell.anim = breathe(cell.fs)
  elseif TIERS[def.tier] and TIERS[def.tier].hz then
    cell.anim = pulse(cell.halo, TIERS[def.tier].hz)
  end
  return cell
end

local function build()
  local UI = ns.UI
  local w, h, why = ns.CDMItemSize()
  local width = math.max(400, 40 + #CELLS * w + (#CELLS - 1) * GAP)
  local height = h + 168

  local root = CreateFrame("Frame", nil, UIParent)
  root:SetSize(width, height)
  root:SetFrameStrata("DIALOG")
  root:SetMovable(true)
  root:EnableMouse(true)
  root:RegisterForDrag("LeftButton")
  root:SetScript("OnDragStart", root.StartMoving)
  root:SetScript("OnDragStop", root.StopMovingOrSizing)
  root.w, root.h, root.why = w, h, why

  local bg = root:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(root)
  bg:SetColorTexture(0.08, 0.08, 0.10, 0.96)
  UI.edge(root, 0.45, 0.45, 0.55, 0.9)

  local title = root:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  title:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -10)
  title:SetText("ClientLab — tier mockup")

  UI.button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  root.note = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  root.note:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -32)
  root.note:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, -32)
  root.note:SetJustifyH("LEFT")
  root.note:SetWordWrap(true)
  root.note:SetHeight(28)

  panel = root
  cells = {}
  local x0 = (width - (#CELLS * w + (#CELLS - 1) * GAP)) / 2
  for i, def in ipairs(CELLS) do
    cells[i] = makeCell(root, def, x0 + (i - 1) * (w + GAP), -70, w, h)
  end

  -- Which ring reads at 40 px is not guessable, so it is a comparison rather than a
  -- choice one of us makes. Ants stays the default: the comparison starts where the eye
  -- judging it already is.
  local baseLabel = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  baseLabel:SetPoint("BOTTOMLEFT", root, "BOTTOMLEFT", 12, 16)
  baseLabel:SetText("ring")
  root.baseButtons = {}
  local x = 46
  for i, base in ipairs(BASES) do
    local b = UI.button(root, base.name, 8 * #base.name + 22, 20, function()
      if baseIdx ~= i then baseIdx = i; repaint() end
    end)
    b:SetPoint("BOTTOMLEFT", root, "BOTTOMLEFT", x, 12)
    x = x + 8 * #base.name + 26
    root.baseButtons[i] = b
  end

  root.grey = UI.button(root, "[ ] greyscale", 110, 20, function()
    greyOn = not greyOn
    repaint()
  end)
  root.grey:SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -12, 12)

  root:SetScript("OnShow", function()
    repaint()
    for _, cell in ipairs(cells) do
      if cell.anim then pcall(cell.anim.Play, cell.anim) end
    end
  end)
  -- Every Apply is paired here, and the animations stop with them: a glow left on a
  -- hidden frame is the one way a picker turns into a bug report.
  root:SetScript("OnHide", function()
    for _, cell in ipairs(cells) do
      stopGlow(cell)
      if cell.anim then pcall(cell.anim.Stop, cell.anim) end
    end
  end)
  root:Hide()
  return root
end

function M.Toggle()
  if InCombatLockdown() and not panel then
    ns.Print("can't build the tier mockup in combat — open it once out of combat, then it "
      .. "stays usable mid-pull.")
    return
  end
  panel = panel or build()
  if panel:IsShown() then
    panel:Hide()
    return false
  end
  panel:ClearAllPoints()
  panel:SetPoint("CENTER", UIParent, "CENTER", 0, 160)
  panel:Show()
  return true
end

ns.Dumps.Register{
  id = "mock",
  label = "tier mockup",
  blurb = function()
    return ("%d icons · 2.5 / 1.2 / 0.5 Hz / no ring · %s")
      :format(#CELLS, BASES[baseIdx].name)
  end,
  capture = function()
    local shown = M.Toggle()
    if shown == nil then return { "refused — the tier mockup cannot be built in combat" } end
    return { shown and "opened the tier mockup — one control, [ ] greyscale: if the four "
                    .. "tiers cannot be ranked with saturation at zero — LOW against NONE "
                    .. "most of all — the design has failed at the distinction it exists for"
                   or "closed the tier mockup" }
  end,
}

-- Focused visual questions anchored in cooldown-manager.md.
local ADDON, ns = ...

local CONFLAGRATE = 17962

local function label(parent, text, x)
  local fs = parent:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  fs:SetPoint("TOP", parent, "TOP", x, -14)
  fs:SetText(text)
  parent.regions[#parent.regions + 1] = fs
end

local function iconHolder(parent, x)
  local holder = CreateFrame("Frame", nil, parent)
  holder:SetSize(72, 72)
  holder:SetPoint("CENTER", parent, "CENTER", x, -12)
  local icon = holder:CreateTexture(nil, "ARTWORK")
  icon:SetAllPoints(holder)
  icon:SetTexture(C_Spell.GetSpellTexture(CONFLAGRATE))
  parent.kids[#parent.kids + 1] = holder
  return holder
end

ns.Ask.Register{
  id = "conflagrate-charge-context-displays",
  anchor = "cooldown-manager.md:1479",
  bucket = "secret",
  question = "Do the exact count and both next-charge swipes work during recharge?",
  note = "Start at 2/2, enter combat, cast twice, then watch one natural recharge. "
    .. "Left is the exact display count; center is a normal swipe; right is teal and reversed.",
  options = { "all three work", "something fails", "can't tell" },
  setup = function(canvas)
    canvas.kids, canvas.regions = canvas.kids or {}, canvas.regions or {}
    label(canvas, "EXACT COUNT", -145)
    label(canvas, "NEXT CHARGE", 0)
    label(canvas, "STYLED", 145)

    local countHolder = iconHolder(canvas, -145)
    local count = countHolder:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    count:SetPoint("CENTER", countHolder, "CENTER")

    local normalHolder = iconHolder(canvas, 0)
    local normal = CreateFrame("Cooldown", nil, normalHolder, "CooldownFrameTemplate")
    normal:SetAllPoints(normalHolder)
    normal:SetDrawSwipe(true)
    normal:SetDrawEdge(true)
    normal:SetHideCountdownNumbers(true)
    normal:SetUseAuraDisplayTime(false)

    local styledHolder = iconHolder(canvas, 145)
    local styled = CreateFrame("Cooldown", nil, styledHolder, "CooldownFrameTemplate")
    styled:SetAllPoints(styledHolder)
    styled:SetDrawSwipe(true)
    styled:SetDrawEdge(false)
    styled:SetHideCountdownNumbers(true)
    styled:SetUseAuraDisplayTime(false)
    styled:SetReverse(true)
    styled:SetSwipeColor(0.05, 0.85, 0.80, 0.82)

    local function refresh()
      -- The display string may be secret. It goes straight to the leaf sink and is never
      -- compared, classified, formatted, or read back.
      local okCount, display = pcall(C_Spell.GetSpellDisplayCount, CONFLAGRATE, 9999, "*")
      if okCount then count:SetText(display) else count:SetText("refused") end

      -- The handle is plain; its timing may be secret. Presence only selects whether a
      -- duration exists to draw, never a gameplay verdict.
      local okDuration, duration = pcall(C_Spell.GetSpellChargeDuration, CONFLAGRATE)
      if okDuration and duration then
        normal:SetCooldownFromDurationObject(duration, true)
        styled:SetCooldownFromDurationObject(duration, true)
      else
        normal:Clear()
        styled:Clear()
      end
    end

    local events = CreateFrame("Frame", nil, canvas)
    events:RegisterEvent("SPELL_UPDATE_CHARGES")
    events:RegisterEvent("PLAYER_ENTERING_WORLD")
    events:SetScript("OnEvent", refresh)
    canvas.kids[#canvas.kids + 1] = events
    refresh()
  end,
}

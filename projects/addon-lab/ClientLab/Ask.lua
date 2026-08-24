-- Ask — the eyeball channel: show the human something, record their answer.
--
-- Some questions have no programmatic oracle BY CONSTRUCTION. Whether OVERLAY really
-- draws above ARTWORK, whether an aspect-less setter moved a pixel, whether `## Category`
-- groups the addon list — no API returns any of it. Until now those could only be left
-- open, because the one rule that must never bend is that an instrument may not grade
-- its own subject.
--
-- This does not bend it. It adds a DIFFERENT witness: the addon renders a stimulus and
-- a person answers. The answer is recorded with `source = "eyeball"`, so it is never
-- mistaken for a measurement — the reader renders it differently and the drain treats
-- it differently. A human verdict is the RIGHT evidence for a visual question and the
-- WRONG evidence for a measurable one, and the source field is what lets the tooling
-- tell those apart.

local ADDON, ns = ...

ns.Ask = {}
local A = ns.Ask

local registry, order = {}, {}
local frame, current

-- Option rows: full width, stacked, left-aligned, wrapping. Sized for the longest
-- option any question declares rather than the shortest, because a truncated option is
-- worse than a wordy one — the person cannot tell what they are agreeing to.
-- ⚠ OPTION_H is a MINIMUM, not a row height, and the option area is MEASURED rather than
-- budgeted. It used to be `OPTION_H * MAX_OPTIONS + 6` with the loop uncapped, which failed
-- two ways at once and silently: a 6th option drew past the area and through the nav row,
-- and any option that WRAPPED drew through the option under it. Both look like a mangled
-- panel rather than like a layout bug, so the person answering blames the question.
local OPTION_H = 26
local OPTION_GAP, OPTION_PAD = 3, 8
-- A hard ceiling, asserted at Register time rather than truncated at draw time. Truncating
-- would hide options from the one person whose job is to choose between them.
local MAX_OPTIONS = 8
-- The header (title + question + note) never occupies less than this, so a short question
-- does not leave the canvas floating at the top of the frame.
local HEADER_MIN = 110

--- Register a visual question. `setup(canvas)` draws the stimulus; `question` is what
--- the person is being asked; `options` default to yes/no/can't tell.
function A.Register(def)
  -- ⚠ Asserted at LOAD, not at draw. An overflowing option list used to render past the
  -- panel and through the nav row, which reads as a broken panel rather than as an authoring
  -- mistake -- and the author is not the person who sees it.
  -- ⚠ THE PANEL IS A STIMULUS, NOT A BRIEFING. Measured 2026-08-21: a ~700-character `note`
  -- rendered as a grey wall above the tiles, and the author's verdict came back as prose in chat
  -- because the panel was not worth reading. Long-form belongs in questions.json's `expect`,
  -- which is written for the person DRAINING the run, not for the person flying it.
  assert(type(def) ~= "table" or type(def.note) ~= "string" or #def.note <= 300,
    "Ask.Register '" .. tostring(def and def.id) .. "': `note` is " ..
    #(def and def.note or "") .. " chars; keep it under 300. What to do, not why it matters — "
    .. "the reasoning goes in questions.json `expect`.")
  assert(type(def) ~= "table" or type(def.question) ~= "string" or #def.question <= 200,
    "Ask.Register '" .. tostring(def and def.id) .. "': `question` is " ..
    #(def and def.question or "") .. " chars; keep it under 200. One question. If it needs "
    .. "four clauses it is four questions, and the tile labels can carry them.")
  assert(type(def) ~= "table" or type(def.options) ~= "table" or #def.options <= MAX_OPTIONS,
    "Ask.Register '" .. tostring(def and def.id) .. "': at most " .. MAX_OPTIONS
    .. " options; a longer list is a sign the question is really two questions")
  assert(type(def) == "table" and def.id and def.question and def.setup,
         "Ask.Register: id + question + setup required")
  if not registry[def.id] then order[#order + 1] = def.id end
  def.options = def.options or { "yes", "no", "can't tell" }
  registry[def.id] = def
  return def
end

function A.Count() return #order end

--- Has this question been answered THIS SESSION? Used by the panel's caption.
function A.Answered(id)
  local def = registry[id]
  return def and def.verdict or nil
end

function A.Pending()
  local n = 0
  for _, id in ipairs(order) do if not registry[id].verdict then n = n + 1 end end
  return n
end

-- Record a verdict as a row on the same `runs` stream every test writes to, joined by
-- the same id. One stream, one reader, one join (capture standard §6) — `source` is
-- what separates the two kinds of evidence, not a second store.
local function record(def, verdict)
  def.verdict = verdict
  local stamp = ns.Stamp()
  ns.runsLog:Row({
    run = ns.runCount or 0,
    at = date and date("%Y-%m-%d %H:%M:%S") or "?",
    id = def.id, status = "ok", source = "eyeball",
    anchor = def.anchor, bucket = def.bucket,
    value = { verdict = verdict, asked = def.question },
    combat = stamp.combat, spec = stamp.spec, hero = stamp.hero,
    instance = stamp.instance,
  })
  ns.Printf("|cff66ddaaeyeball|r %s -> |cffffffff%s|r", def.id, verdict)
end

-- UI --------------------------------------------------------------------------

local function build()
  local UI = ns.UI
  local root = CreateFrame("Frame", nil, UIParent)
  -- ⚠ WIDER AND BIGGER-TYPED THAN IT LOOKS LIKE IT NEEDS TO BE. Measured 2026-08-21: at 480px
  -- with GameFont*Small everywhere, the person answering had to put their face to the monitor,
  -- and a panel nobody can read is a panel whose verdicts are guesses.
  root:SetSize(620, 520)
  root:SetFrameStrata("DIALOG")
  root:SetMovable(true)
  root:EnableMouse(true)
  root:RegisterForDrag("LeftButton")
  root:SetScript("OnDragStart", root.StartMoving)
  root:SetScript("OnDragStop", root.StopMovingOrSizing)

  local bg = root:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(root)
  bg:SetColorTexture(0.08, 0.08, 0.10, 0.96)
  UI.edge(root, 0.45, 0.45, 0.55, 0.9)

  root.title = root:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  root.title:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -10)

  UI.button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  root.question = root:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
  root.question:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -32)
  root.question:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, -32)
  root.question:SetJustifyH("LEFT")
  root.question:SetWordWrap(true)

  root.note = root:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
  root.note:SetPoint("TOPLEFT", root.question, "BOTTOMLEFT", 0, -6)
  root.note:SetPoint("TOPRIGHT", root.question, "BOTTOMRIGHT", 0, -6)
  root.note:SetJustifyH("LEFT")
  root.note:SetWordWrap(true)

  -- The canvas the stimulus draws into. Deliberately a plain frame with a visible
  -- border: the person must be able to tell the stimulus apart from the chrome.
  local canvas = CreateFrame("Frame", nil, root)
  -- ⚠ The top anchor is re-applied per question in `A.Show`, because the header's height
  -- is not known until its text is set. It used to be a fixed -110, which meant a note
  -- longer than that budget silently drew ON TOP of the stimulus — and the stimulus is the
  -- entire point of this panel. A header may now push the canvas down; it may not overlap it.
  canvas:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -HEADER_MIN)
  -- A PLACEHOLDER extent only. `A.Show` re-anchors this from the option area it actually
  -- measured, exactly as it re-anchors the top from the header's real height -- there is no
  -- fixed option budget any more, so `build` cannot know the bottom either.
  canvas:SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -10, 34 + OPTION_H)
  local cbg = canvas:CreateTexture(nil, "BACKGROUND")
  cbg:SetAllPoints(canvas)
  cbg:SetColorTexture(0.02, 0.02, 0.03, 1)
  UI.edge(canvas, 0.3, 0.3, 0.4, 0.9)
  root.canvas = canvas

  -- The options stack VERTICALLY at full width. A horizontal row of fixed-width
  -- buttons truncated every label long enough to be precise, so the wording had to be
  -- short and the questions got vaguer to fit the chrome — backwards.
  root.verdictRow = CreateFrame("Frame", nil, root)
  root.verdictRow:SetPoint("BOTTOMLEFT", root, "BOTTOMLEFT", 10, 32)
  root.verdictRow:SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -10, 32)
  root.verdictRow:SetHeight(OPTION_H)
  root.verdictButtons = {}

  root.nav = root:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  root.nav:SetPoint("BOTTOMLEFT", root, "BOTTOMLEFT", 12, 12)

  UI.button(root, "next >", 60, 20, function() A.Step(1) end)
      :SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -10, 8)
  UI.button(root, "< prev", 60, 20, function() A.Step(-1) end)
      :SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -76, 8)
  UI.button(root, "re-show", 60, 20, function() A.Show(current) end)
      :SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -142, 8)

  root:Hide()
  return root
end

-- Everything the stimulus created last time goes away before the next one draws, or a
-- stale texture from the previous question becomes part of the next one's answer.
local function clearCanvas()
  local c = frame.canvas
  if c.kids then
    for _, k in ipairs(c.kids) do k:Hide(); k:SetParent(nil) end
  end
  if c.regions then
    for _, r in ipairs(c.regions) do r:Hide() end
  end
  c.kids, c.regions = {}, {}
end

-- ⚠ THE HANDLER IS REBOUND EVERY TIME, and that is not a style choice.  The buttons are
-- POOLED across questions — only their labels change — so a handler installed when the
-- button was first created keeps the FIRST question's `def` in its closure forever, and
-- every later answer is recorded against the wrong question.  Capture `opt` here too,
-- rather than reading the label back at click time, so the recorded verdict cannot drift
-- from the option that was bound.
-- A full-width option row. Its label is LEFT-aligned and wraps, so a precise option can
-- be written as a sentence instead of squeezed into a chip.
local function optionButton(parent)
  local b = CreateFrame("Button", nil, parent)
  local bg = b:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(b)
  bg:SetColorTexture(0.16, 0.16, 0.20, 0.9)
  ns.UI.edge(b, 0.4, 0.4, 0.5, 0.8)
  -- ⚠ TOP-anchored, not LEFT-anchored. A vertically-centred wrapping FontString grows in
  -- BOTH directions out of a fixed-height button, so its second line lands on the button
  -- above and its third on the one below. Anchored to the top it grows downward only, and
  -- the button is then sized to it.
  local fs = b:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
  fs:SetPoint("TOPLEFT", b, "TOPLEFT", OPTION_PAD, -OPTION_PAD / 2)
  fs:SetPoint("TOPRIGHT", b, "TOPRIGHT", -OPTION_PAD, -OPTION_PAD / 2)
  fs:SetJustifyH("LEFT")
  fs:SetWordWrap(true)
  b.text = fs
  b:SetScript("OnEnter", function() bg:SetColorTexture(0.26, 0.26, 0.34, 0.95) end)
  b:SetScript("OnLeave", function() bg:SetColorTexture(0.16, 0.16, 0.20, 0.9) end)
  return b
end

-- Returns the height the options actually needed. The caller anchors the canvas above it,
-- so a long option list pushes the stimulus UP rather than drawing on top of the chrome.
local function setVerdictButtons(def)
  for _, b in ipairs(frame.verdictButtons) do b:Hide() end
  local rowW = frame.verdictRow:GetWidth()
  if not rowW or rowW <= 0 then rowW = frame:GetWidth() - 20 end
  local y = 0
  for i, opt in ipairs(def.options) do
    local b = frame.verdictButtons[i]
    if not b then
      b = optionButton(frame.verdictRow)
      frame.verdictButtons[i] = b
    end
    -- Width BEFORE text, or GetStringHeight measures an unwrapped single line and every
    -- multi-line option reports one line tall.
    b.text:SetWidth(rowW - OPTION_PAD * 2)
    b.text:SetText(opt)
    b:SetScript("OnClick", function()
      record(def, opt)
      A.Refresh()
    end)
    local textH = b.text:GetStringHeight() or 0
    local h = textH + OPTION_PAD
    if h < OPTION_H - 4 then h = OPTION_H - 4 end
    b:ClearAllPoints()
    b:SetPoint("TOPLEFT", frame.verdictRow, "TOPLEFT", 0, -y)
    b:SetPoint("TOPRIGHT", frame.verdictRow, "TOPRIGHT", 0, -y)
    b:SetHeight(h)
    b:Show()
    y = y + h + OPTION_GAP
  end
  frame.verdictRow:SetHeight(math.max(y, OPTION_H))
  return math.max(y, OPTION_H)
end

-- Push the canvas below whatever the header actually needed, then make sure what is left
-- is still big enough to judge a stimulus in — growing the window rather than shrinking the
-- picture, since the picture is the evidence.
local MIN_CANVAS_H = 210
local function layoutCanvas(optionArea)
  if not frame then return end
  optionArea = optionArea or frame.verdictRow:GetHeight() or OPTION_H
  local header = 32 + (frame.question:GetStringHeight() or 0)
                    + 6 + (frame.note:GetStringHeight() or 0) + 10
  if header < HEADER_MIN then header = HEADER_MIN end
  frame.canvas:ClearAllPoints()
  frame.canvas:SetPoint("TOPLEFT", frame, "TOPLEFT", 10, -header)
  frame.canvas:SetPoint("BOTTOMRIGHT", frame, "BOTTOMRIGHT", -10, 34 + optionArea + 6)
  local need = header + MIN_CANVAS_H + 34 + optionArea + 6
  if frame:GetHeight() < need then frame:SetHeight(need) end
end

function A.Show(idx)
  if not frame then return end
  current = idx
  local def = registry[order[idx]]
  if not def then return end

  frame.title:SetText(("ClientLab — visual check %d/%d"):format(idx, #order))
  frame.question:SetText(def.question)
  frame.note:SetText(def.note or "")
  clearCanvas()
  -- ⚠ Options FIRST. The canvas is anchored above them, so its rect is not knowable until
  -- their measured height is -- and `setup` draws into that rect, so it must be final
  -- before the stimulus runs or every tile is placed against a stale size.
  local optionArea = setVerdictButtons(def)
  layoutCanvas(optionArea)

  -- A stimulus with an unmet precondition must say so instead of drawing something
  -- that looks like the real thing. Answering "no" to a blank canvas would be a
  -- fabricated verdict, which is the one failure this whole channel could introduce.
  if def.needs == "secret" then
    local sv, why = ns.GetSecret()
    if sv == nil then
      frame.note:SetText("|cffff8844Cannot show this yet:|r " .. tostring(why))
      for _, b in ipairs(frame.verdictButtons) do b:Hide() end
      frame.nav:SetText("precondition unmet — nothing to judge")
      return
    end
  end

  local ok, err = pcall(def.setup, frame.canvas)
  if not ok then
    frame.note:SetText("|cffff4040stimulus failed:|r " .. tostring(err))
    for _, b in ipairs(frame.verdictButtons) do b:Hide() end
    frame.nav:SetText("nothing to judge")
    return
  end

  -- Say where you are in the set AND that next wraps: a silently-wrapping `next` reads
  -- as "there are more questions", and re-answering one you already answered by mistake
  -- overwrites a good verdict.
  local wrap = (#order > 1) and (idx == #order) and "  ·  |cffffd100next wraps to #1|r" or ""
  frame.nav:SetText((def.verdict
    and ("answered: |cffffffff" .. def.verdict .. "|r — answering again REPLACES it")
    or ("|cffffd100unanswered|r · " .. A.Pending() .. " of " .. #order .. " left")) .. wrap)
end

function A.Refresh() if current then A.Show(current) end end

function A.Step(delta)
  if #order == 0 then return end
  A.Show(((current or 1) - 1 + delta) % #order + 1)
end

function A.Toggle()
  if #order == 0 then
    ns.Print("no visual checks registered.")
    return
  end
  if InCombatLockdown() and not frame then
    ns.Print("can't build the visual-check panel in combat — open it once out of combat, "
      .. "then it works mid-pull.")
    return
  end
  frame = frame or build()
  if frame:IsShown() then
    frame:Hide()
  else
    frame:ClearAllPoints()
    frame:SetPoint("CENTER", UIParent, "CENTER", 240, 0)
    frame:Show()
    A.Show(current or 1)
  end
end

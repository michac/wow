-- Dumps — captures a human takes at a moment, by button.
--
-- `[copy]` reads the IN-MEMORY ring, so an answer leaves the client with no /reload —
-- and a reload ends the pull that made a value secret in the first place. That is the
-- whole reason this file exists: it turns the loop from one answer per reload into
-- answer, adjust, re-answer without leaving the dummy.
--
-- Contract: .claude/skills/wow-developer/references/capture-and-dump-standard.md
-- Vendored from CDMProbe/DumpPanel.lua.

local ADDON, ns = ...

ns.Dumps = {}
local D = ns.Dumps

local SESSIONS, CAP = 8, 4000
local COPY_PAGE = 30000        -- chars per page; SetText stalls on very large payloads
local ROWS = 10
local MARK = "== dump "

local stream = ns.Capture.Open("dump", { sessions = SESSIONS, cap = CAP })

local registry, order = {}, {}
local entries = {}             -- in-memory index: { n, t, id, blurb, lines }
local panel                    -- built lazily, never in combat

--- Register a dump button. `capture` returns an array of plain-text lines.
function D.Register(def)
  assert(type(def) == "table" and def.id and def.capture, "Dumps.Register: id + capture required")
  if not registry[def.id] then order[#order + 1] = def.id end
  registry[def.id] = def
end

local function describe(def)
  if type(def.blurb) ~= "function" then return def.label or def.id end
  local ok, s = pcall(def.blurb)
  return (ok and type(s) == "string") and s or (def.label or def.id)
end

--- Take a dump: write it to the stream and index it for the list.
function D.Take(id)
  local def = registry[id]
  if not def then return end

  local ok, lines = pcall(def.capture)
  if not ok or type(lines) ~= "table" then
    ns.Printf("dump '%s' failed: %s", id, ns.Capture.Safe(lines))
    return
  end

  local blurb = describe(def)
  local n = #entries + 1
  local t = date("%H:%M:%S")

  stream:Mark("%s#%d %s %s · %s", MARK, n, t, id, blurb)
  for _, ln in ipairs(lines) do stream:Line("%s", tostring(ln)) end

  entries[n] = { n = n, t = t, id = id, blurb = blurb, lines = lines }
  if panel and panel:IsShown() then D.Refresh() end
  ns.Printf("dump #%d — %s (%d lines). |cffffffff[copy]|r it off the panel; no reload needed.",
    n, blurb, #lines)
end

-- Rebuild the index from the newest stored session, so the list survives a /reload.
function D.Restore()
  local ring = ns.db and ns.db.captures and ns.db.captures.dump
  if type(ring) ~= "table" or #ring == 0 then return end
  local sess = ring[#ring]
  local cur
  for _, ln in ipairs(sess.lines or {}) do
    local head = ln:match("^" .. MARK .. "(.+)$")
    if head then
      local num, t, rest = head:match("^#(%d+)%s+(%S+)%s+(.+)$")
      cur = { n = tonumber(num) or (#entries + 1), t = t or "?",
              id = (rest or ""):match("^(%S+)") or "?", blurb = rest or "?", lines = {} }
      entries[#entries + 1] = cur
    elseif cur then
      cur.lines[#cur.lines + 1] = ln
    end
  end
end

-- The buttons ----------------------------------------------------------------
-- Autorun.lua takes every run that can be taken from the state you are in, so these
-- are not the normal path — they are for a moment only the player can recognise:
-- re-run right now, at this point in the pull, on this target.
--
-- `run` records rows to the `runs` stream through the normal path AND renders the
-- same results as lines here, so the bytes a human copies and the bytes the
-- extractor reads describe one run rather than two.
local function shortValue(v)
  if v == nil then return "nil" end
  if type(v) ~= "table" then return tostring(v) end
  local keys = {}
  for k in pairs(v) do keys[#keys + 1] = tostring(k) end
  table.sort(keys)
  local parts = {}
  for _, k in ipairs(keys) do
    local inner = v[k]
    if type(inner) == "table" then
      local ik = {}
      for k2 in pairs(inner) do ik[#ik + 1] = tostring(k2) end
      table.sort(ik)
      local sub = {}
      for _, k2 in ipairs(ik) do sub[#sub + 1] = k2 .. "=" .. tostring(inner[k2]) end
      parts[#parts + 1] = k .. "={" .. table.concat(sub, ", ") .. "}"
    else
      parts[#parts + 1] = k .. "=" .. tostring(inner)
    end
  end
  return "{" .. table.concat(parts, ", ") .. "}"
end

D.Register{
  id = "run",
  label = "run all tests",
  blurb = function()
    local r = ns.lastRuns and (ns.lastRuns.combat or ns.lastRuns.ooc)
    if not r then return "no run yet" end
    return string.format("%d tests · ok %d / decl %d / err %d / skip %d",
      #r.results, r.counts.ok or 0, r.counts.declined or 0,
      r.counts.error or 0, r.counts.skipped or 0)
  end,
  capture = function()
    local run = ns.RunAll()
    local out = {
      string.format("run %d — %s — v%s — %s — spec %s — hero %s — instance %s",
        run.index, run.at, run.version, run.combat and "IN COMBAT" or "out of combat",
        tostring(run.spec), tostring(run.hero), tostring(run.instance)),
      string.format("ok %d / declined %d / error %d / skipped %d",
        run.counts.ok or 0, run.counts.declined or 0,
        run.counts.error or 0, run.counts.skipped or 0),
      "",
    }
    for _, r in ipairs(run.results) do
      local tail
      if r.status == "ok" then tail = shortValue(r.value)
      elseif r.status == "error" then tail = r.err
      else tail = r.why end
      out[#out + 1] = string.format("%-8s %-40s %s",
        r.declined and "declined" or r.status, r.id, tostring(tail))
    end
    return out
  end,
}

-- `secret` answers "why did 14 rows skip?" in five seconds. It reports the CLASS and
-- the source string, never the value — formatting a Secret Value taints the writer.
D.Register{
  id = "secret",
  label = "secret probe",
  blurb = function()
    if not ns.SecretAPI() then return "issecretvalue absent" end
    return InCombatLockdown() and "in combat — a secret should exist" or "out of combat"
  end,
  capture = function()
    local out = {
      "secret probe — " .. date("%H:%M:%S"),
      "combat: " .. tostring(InCombatLockdown() and true or false),
      "issecretvalue present: " .. tostring(ns.SecretAPI()),
    }
    local v, why = ns.GetSecret()
    if v == nil then
      out[#out + 1] = "GetSecret: NONE"
      out[#out + 1] = "why: " .. tostring(why)
      out[#out + 1] = ""
      out[#out + 1] = "Every needs=\"secret\" test will record `skipped` until this reads OK."
    else
      out[#out + 1] = "GetSecret: OK"
      out[#out + 1] = "source: " .. tostring(why)
      out[#out + 1] = "class: " .. ns.Capture.Safe(v)
      local okT, ty = pcall(type, v)
      out[#out + 1] = "type(): " .. (okT and tostring(ty) or "errored")
    end
    return out
  end,
}

-- Coverage: is the evidence complete, and if not, what game situation is missing.
-- Every unmet goal names something to DO, never something to type.
D.Register{
  id = "coverage",
  label = "coverage",
  blurb = function()
    local cov = ns.Coverage()
    return cov.complete and "COMPLETE" or (cov.left .. " goal(s) left")
  end,
  capture = function() return ns.CoverageLines() end,
}

-- The eyeball channel is a BUTTON on this panel too, because a visual check is the
-- same kind of act as a dump: a human deciding something at a moment. Ask.lua owns the
-- frame; this is just the door to it.
D.Register{
  id = "visual",
  label = "visual checks",
  blurb = function()
    if not ns.Ask or ns.Ask.Count() == 0 then return "none registered" end
    local pending = ns.Ask.Pending()
    return pending == 0 and "all answered" or (pending .. " unanswered")
  end,
  capture = function()
    if not ns.Ask then return { "Ask.lua not loaded" } end
    ns.Ask.Toggle()
    return { "opened the visual-check panel — answers record themselves as they are given" }
  end,
}

-- UI --------------------------------------------------------------------------

local function edge(f, r, g, b, a)
  for _, p in ipairs({ { "TOPLEFT", "TOPRIGHT", 0, 1 }, { "BOTTOMLEFT", "BOTTOMRIGHT", 0, -1 },
                       { "TOPLEFT", "BOTTOMLEFT", -1, 0 }, { "TOPRIGHT", "BOTTOMRIGHT", 1, 0 } }) do
    local t = f:CreateTexture(nil, "BORDER")
    t:SetColorTexture(r, g, b, a)
    t:SetPoint(p[1], f, p[1], p[3], p[4])
    t:SetPoint(p[2], f, p[2], p[3], p[4])
    if p[3] == 0 then t:SetHeight(1) else t:SetWidth(1) end
  end
end

local function button(parent, text, w, h, onClick)
  local b = CreateFrame("Button", nil, parent)
  b:SetSize(w, h)
  local bg = b:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(b)
  bg:SetColorTexture(0.16, 0.16, 0.20, 0.9)
  edge(b, 0.4, 0.4, 0.5, 0.8)
  local fs = b:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  fs:SetPoint("CENTER")
  fs:SetText(text)
  b.text = fs
  b:SetScript("OnEnter", function() bg:SetColorTexture(0.26, 0.26, 0.34, 0.95) end)
  b:SetScript("OnLeave", function() bg:SetColorTexture(0.16, 0.16, 0.20, 0.9) end)
  b:SetScript("OnClick", onClick)
  return b
end

-- Shared with Ask.lua so the two panels look like one addon and a chrome fix lands
-- in both. Nothing else should grow here — this is not a widget library.
ns.UI = { edge = edge, button = button }

-- WoW has no clipboard API: the payload goes into a multiline EditBox, is selected,
-- and the user's own Ctrl+C does the work. Never a secure frame.
local function showCopy(entry)
  local f = panel.copy
  local text = table.concat(entry.lines, "\n")
  f.pages, f.page = {}, 1
  for i = 1, math.max(1, math.ceil(#text / COPY_PAGE)) do
    f.pages[i] = text:sub((i - 1) * COPY_PAGE + 1, i * COPY_PAGE)
  end
  f.title:SetText(("#%d %s · %s   (page 1/%d — Ctrl+C)"):format(
    entry.n, entry.id, entry.blurb, #f.pages))
  f.box:SetText(f.pages[1])
  f.box:HighlightText()
  f.box:SetFocus()
  f:Show()
end

-- `print` is for the dumps you want to READ, not carry out: coverage, the secret probe,
-- anything whose whole content is a dozen lines. `copy` answers "get this to the desk";
-- a list row that only says "3 goals left" makes you route a dozen lines through the
-- clipboard and a text editor to find out which three.
local PRINT_MAX = 40

function D.Print(entry)
  ns.Heading(("#%d %s · %s"):format(entry.n, entry.id, entry.blurb))
  local n = math.min(#entry.lines, PRINT_MAX)
  for i = 1, n do ns.Printf("  %s", tostring(entry.lines[i])) end
  if #entry.lines > n then
    ns.Printf("  |cff808080… +%d more line(s) — |r|cffffffff[copy]|r|cff808080 for the whole thing|r",
      #entry.lines - n)
  end
end

local function buildCopy(parent)
  local f = CreateFrame("Frame", nil, parent)
  f:SetPoint("TOPLEFT", parent, "TOPLEFT", 8, -8)
  f:SetPoint("BOTTOMRIGHT", parent, "BOTTOMRIGHT", -8, 8)
  local bg = f:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(f)
  bg:SetColorTexture(0.05, 0.05, 0.07, 0.97)
  edge(f, 0.5, 0.5, 0.6, 0.9)

  f.title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  f.title:SetPoint("TOPLEFT", f, "TOPLEFT", 8, -8)

  local scroll = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
  scroll:SetPoint("TOPLEFT", f, "TOPLEFT", 8, -26)
  scroll:SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -30, 34)

  local box = CreateFrame("EditBox", nil, scroll)
  box:SetMultiLine(true)
  box:SetMaxLetters(0)          -- the default cap is unmeasured; make it not matter
  box:SetMaxBytes(0)
  box:SetAutoFocus(false)
  box:SetFontObject("GameFontHighlightSmall")
  box:SetWidth(520)
  box:SetScript("OnEscapePressed", function() f:Hide() end)
  -- Read-only by reselection: revert an edit and re-select, as WeakAuras' debug log does.
  box:SetScript("OnTextChanged", function(self, user)
    if user then self:SetText(f.pages[f.page] or ""); self:HighlightText() end
  end)
  box:SetScript("OnMouseUp", function(self) self:HighlightText() end)
  scroll:SetScrollChild(box)
  f.box = box

  button(f, "Close", 60, 20, function() f:Hide() end)
      :SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -8, 8)
  f.next = button(f, "Next page", 80, 20, function()
    f.page = (f.page % #f.pages) + 1
    f.title:SetText(f.title:GetText():gsub("page %d+/", "page " .. f.page .. "/"))
    box:SetText(f.pages[f.page]); box:HighlightText(); box:SetFocus()
  end)
  f.next:SetPoint("BOTTOMLEFT", f, "BOTTOMLEFT", 8, 8)

  f:Hide()
  return f
end

local function build()
  local root = CreateFrame("Frame", nil, UIParent)
  root:SetSize(560, 400)
  root:SetFrameStrata("DIALOG")
  root:SetMovable(true)
  root:EnableMouse(true)
  root:RegisterForDrag("LeftButton")
  root:SetScript("OnDragStart", root.StartMoving)
  root:SetScript("OnDragStop", function(self)
    self:StopMovingOrSizing()
    local db = ns.db and ns.db.dumpPanel
    if db then
      local p, _, rp, x, y = self:GetPoint()
      db.point, db.relPoint, db.x, db.y = p, rp, x, y
    end
  end)

  local bg = root:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(root)
  bg:SetColorTexture(0.08, 0.08, 0.10, 0.94)
  edge(root, 0.45, 0.45, 0.55, 0.9)

  local title = root:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  title:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -10)
  title:SetText("ClientLab — dumps")

  button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  local grid = CreateFrame("Frame", nil, root)
  grid:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -34)
  grid:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, -34)
  grid:SetHeight(1)
  local x, y, rowH = 0, 0, 22
  for _, id in ipairs(order) do
    local def = registry[id]
    local b = button(grid, def.label or id, 140, 20, function() D.Take(id) end)
    if x + 140 > 540 then x, y = 0, y + rowH end
    b:SetPoint("TOPLEFT", grid, "TOPLEFT", x, -y)
    x = x + 146
  end
  grid:SetHeight(y + rowH)

  local list = CreateFrame("Frame", nil, root)
  list:SetPoint("TOPLEFT", grid, "BOTTOMLEFT", 0, -8)
  list:SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -10, 10)
  root.rows = {}
  for i = 1, ROWS do
    local r = CreateFrame("Frame", nil, list)
    r:SetHeight(20)
    r:SetPoint("TOPLEFT", list, "TOPLEFT", 0, -(i - 1) * 21)
    r:SetPoint("TOPRIGHT", list, "TOPRIGHT", 0, -(i - 1) * 21)
    r.label = r:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    r.label:SetPoint("LEFT", r, "LEFT", 2, 0)
    r.label:SetJustifyH("LEFT")
    r.copy = button(r, "copy", 44, 18, function() if r.entry then showCopy(r.entry) end end)
    r.copy:SetPoint("RIGHT", r, "RIGHT", -2, 0)
    r.print = button(r, "print", 44, 18, function() if r.entry then D.Print(r.entry) end end)
    r.print:SetPoint("RIGHT", r.copy, "LEFT", -4, 0)
    r.label:SetPoint("RIGHT", r.print, "LEFT", -4, 0)
    root.rows[i] = r
  end

  root.copy = buildCopy(root)
  root:Hide()
  return root
end

function D.Refresh()
  if not panel then return end
  local total = #entries
  for i, r in ipairs(panel.rows) do
    local e = entries[total - i + 1]      -- newest first
    r.entry = e
    if e then
      r.label:SetText(("|cff888888#%d|r  %s  %s"):format(e.n, e.t, e.blurb))
      r.copy:Show(); r:Show()
    else
      r.label:SetText(""); r.copy:Hide()
    end
  end
end

function D.Toggle()
  if InCombatLockdown() and not panel then
    ns.Print("can't build the dump panel in combat — open it once out of combat, "
      .. "then it stays usable mid-pull.")
    return
  end
  if #entries == 0 then D.Restore() end
  if ns.db then ns.db.dumpPanel = ns.db.dumpPanel or {} end
  panel = panel or build()
  if panel:IsShown() then
    panel:Hide()
  else
    local db = (ns.db and ns.db.dumpPanel) or {}
    panel:ClearAllPoints()
    if db.point then
      panel:SetPoint(db.point, UIParent, db.relPoint or db.point, db.x or 0, db.y or 0)
    else
      panel:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
    end
    D.Refresh()
    panel:Show()
  end
end

ns.RegisterCommand("dump", "toggle the dump panel — run the tests and copy the answers "
  .. "out mid-pull, no /reload", function()
  D.Toggle()
end)

-- Report.lua — chat rendering of the last run, and /clab guide.
--
-- Rendering is deliberately answer-free: the lab shows what it MEASURED, never a
-- verdict.  Reading result-against-expectation and deciding is a desk job for
-- wowkb.lab (W2), which has questions.json; in-game we only confirm the channel
-- was exercised.
local ADDON, ns = ...

local STATUS_COLOR = {
  ok = "|cff88ff88", error = "|cffff8844", skipped = "|cff808080",
  declined = "|cffffcc44",
}

--- What to CALL a result. `declined` is not a status on the wire — the test ran, so its
--- status is `ok` — but it must never render in the same colour as a test that answered.
local function label(r) return r.declined and "declined" or r.status end

local function short(v)
  if v == nil then return "nil" end
  local t = type(v)
  if t == "table" then
    local parts = {}
    for k, val in pairs(v) do
      parts[#parts + 1] = tostring(k) .. "=" .. tostring(val)
      if #parts >= 6 then parts[#parts + 1] = "..."; break end
    end
    return "{" .. table.concat(parts, ", ") .. "}"
  end
  return tostring(v)
end

-- Chat rendering reads the SESSION-LOCAL run, not SavedVariables: the persisted copy
-- is the capture stream, and reading it back here would mean maintaining two shapes.
local function renderRun(key)
  local run = ns.lastRuns and ns.lastRuns[key]
  if not run then
    ns.Printf("no %s run this session — |cffffffff/clab run|r %s", key,
      key == "combat" and "while at a dummy" or "out of combat")
    return
  end
  ns.Heading(string.format("run %s — %s — ok %d / declined %d / error %d / skipped %d",
    key, run.at or "?", run.counts.ok or 0, run.counts.declined or 0,
    run.counts.error or 0, run.counts.skipped or 0))
  for _, r in ipairs(run.results) do
    local lab = label(r)
    local col = STATUS_COLOR[lab] or "|cffffffff"
    local tail
    if r.status == "ok" then tail = short(r.value)
    elseif r.status == "error" then tail = r.err
    else tail = r.why end
    ns.Printf("  %s%s|r %s  |cff808080%s|r", col, lab, r.id, tostring(tail))
  end
end

ns.RenderRun = renderRun

--------------------------------------------------------------------------------
-- Coverage — is this session's evidence complete yet?
--------------------------------------------------------------------------------
-- What it buys is TIMING: you learn the capture is incomplete while still standing
-- at the dummy, not an hour later from wowkb.lab.  Every goal asks whether a channel
-- was EXERCISED, never whether it returned a particular value — a secret op is
-- SUPPOSED to error, so "the secret table ran" is the honest goal, not "it passed".
-- A goal that can never go green is worse than no goal.
local function run(key) return ns.lastRuns and ns.lastRuns[key] end
local function hasRun(key) return run(key) ~= nil end
-- Count the §4.2 secret rows that actually EXECUTED (ok/error) vs skipped in a
-- stored run.  Pull-based: reads what the run captured, so a goal greens after the
-- pull whether you re-type /clab guide in combat or back out of it — the live
-- GetSecret only reads a secret WHILE you are in combat, which made these look
-- unreachable when checked at the wrong moment.
local function secretRowCounts(key)
  local r, ran, total = run(key), 0, 0
  if not r then return 0, 0 end
  for _, res in ipairs(r.results) do
    if res.bucket == "secret" then
      total = total + 1
      if res.status ~= "skipped" then ran = ran + 1 end
    end
  end
  return ran, total
end

--- Every test that reports `measured = false` in the given slot, minus the ones that
--- DECLARE what they are missing. A blocked test is excluded by declaration, never by
--- a hardcoded id list here: the list would rot the moment a blocker is lifted.
local function declining(key)
  local r, out = run(key), {}
  if not r then return out end
  for _, res in ipairs(r.results) do
    local rec = ns.testByID[res.id]
    if res.declined and not (rec and rec.blocked) then out[#out + 1] = res end
  end
  return out
end

--- Roundtrip tests with no read-back recorded this session. `ns.readBacks` is keyed
--- across every run in the session because the run that RECOVERS a payload is often not
--- the latest one — several of these re-arm immediately after reading back, so the last
--- run shows `written` while the answer sits in the run before it.
local function awaitingReadBack()
  local out = {}
  for _, rec in ipairs(ns.tests) do
    if rec.phase == "roundtrip" and not rec.blocked and not ns.readBacks[rec.id] then
      out[#out + 1] = rec.id
    end
  end
  return out
end

local function join(t, n)
  local parts = {}
  for i = 1, math.min(#t, n or 4) do parts[i] = t[i] end
  if #t > (n or 4) then parts[#parts + 1] = "+" .. (#t - (n or 4)) .. " more" end
  return table.concat(parts, ", ")
end

-- The nudges describe what the PLAYER has to do — go somewhere, pull something,
-- swap a tree. The driver takes every run that can be taken from where you are
-- standing, so an unmet goal is nearly always a missing game situation rather than a
-- missing keystroke. The ONE honest exception is the round trip: writing a payload and
-- reading it back needs a session boundary, and no amount of standing anywhere supplies
-- one — so that goal does name `/reload`, because that genuinely is the missing act.
--
-- A nudge may be a function, so a goal can say WHICH rows are holding it open. A goal
-- that reports "3 left" without naming them sends you to a copy button to find out.
local GOALS = {
  { label = "OOC run captured",
    nudge = "should happen by itself shortly after login",
    met = function() return hasRun("ooc") end },
  { label = "in-combat run captured",
    nudge = "pull something — the run fires on its own once combat starts",
    met = function() return hasRun("combat") end },
  { label = "a genuine secret value obtained (a §4.2 row executed in combat)",
    nudge = "cooldown reads only go secret in combat, and only for TRACKED abilities — pull with your real bar",
    met = function() local ran = secretRowCounts("combat"); return ran > 0 end },
  { label = "the full §4.2 secret-op table run (all rows execute, not skip)",
    nudge = "the secret went away mid-run — stay in combat longer; retries continue while the pull lasts",
    met = function() local ran, total = secretRowCounts("combat"); return total > 0 and ran == total end },
  { label = "every test that CAN answer has answered (no unexplained measured=false)",
    nudge = function()
      local d = {}
      for _, res in ipairs(declining("combat")) do d[#d + 1] = res.id end
      for _, res in ipairs(declining("ooc")) do d[#d + 1] = res.id end
      if #d == 0 then return "run once in combat and once out of it" end
      return "observed nothing yet: " .. join(d) .. "  (each one's `why` says what it wants)"
    end,
    met = function()
      return #declining("combat") == 0 and #declining("ooc") == 0
        and (hasRun("combat") or hasRun("ooc"))
    end },
  { label = "every two-phase test has read its payload back",
    nudge = function()
      local a = awaitingReadBack()
      return "armed, not yet recovered: " .. join(a)
        .. "  — |cffffffff/reload|r and let it run again; that is the only thing that finishes these"
    end,
    met = function() return #awaitingReadBack() == 0 end },
}

--- Coverage as DATA, so the panel, the driver's stop condition and the chat notice
--- all read one definition rather than three that can disagree.
function ns.Coverage()
  local out = { goals = {}, left = 0 }
  for i, g in ipairs(GOALS) do
    local called, res = pcall(g.met)
    local ok = called and (res and true or false)
    local nudge = g.nudge
    if type(nudge) == "function" then
      local okN, s = pcall(nudge)
      nudge = (okN and type(s) == "string") and s or "(nudge errored)"
    end
    out.goals[i] = { label = g.label, nudge = nudge, met = ok }
    if not ok then out.left = out.left + 1 end
  end
  out.complete = out.left == 0
  return out
end

--- The goal list, plus the REASON each unanswered test gave. A goal that only counts is
--- a goal you have to go somewhere else to act on — and the `why` a declining test
--- records is usually the whole answer ("shift-hover an item", "/reload to read it back").
function ns.CoverageLines()
  local cov = ns.Coverage()
  local lines = { "coverage — " .. (cov.complete and "COMPLETE"
    or (cov.left .. " goal" .. (cov.left == 1 and "" or "s") .. " left")), "" }
  for _, g in ipairs(cov.goals) do
    lines[#lines + 1] = (g.met and "[x] " or "[ ] ") .. g.label
    if not g.met then lines[#lines + 1] = "      <- " .. tostring(g.nudge) end
  end

  local seen = {}
  for _, key in ipairs({ "combat", "ooc" }) do
    for _, res in ipairs(declining(key)) do
      if not seen[res.id] then
        seen[res.id] = true
        lines[#lines + 1] = ""
        lines[#lines + 1] = "observed nothing — " .. res.id
        lines[#lines + 1] = "      why: " .. tostring(
          type(res.value) == "table" and res.value.why or "(none recorded)")
      end
    end
  end

  local blocked = {}
  for _, rec in ipairs(ns.tests) do
    if rec.blocked then blocked[#blocked + 1] = rec.id .. " — needs " .. rec.blocked end
  end
  if #blocked > 0 then
    lines[#lines + 1] = ""
    lines[#lines + 1] = "declared blocked (excluded from the goals, on purpose):"
    for _, b in ipairs(blocked) do lines[#lines + 1] = "      " .. b end
  end
  return lines
end

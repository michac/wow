-- Report.lua — chat rendering of the last run, and /clab guide.
--
-- Rendering is deliberately answer-free: the lab shows what it MEASURED, never a
-- verdict.  Reading result-against-expectation and deciding is a desk job for
-- wowkb.lab (W2), which has questions.json; in-game we only confirm the channel
-- was exercised.
local ADDON, ns = ...

local STATUS_COLOR = {
  ok = "|cff88ff88", error = "|cffff8844", skipped = "|cff808080",
}

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

local function renderRun(key)
  local run = ns.db and ns.db.runs and ns.db.runs[key]
  if not run then
    ns.Printf("no %s run yet — |cffffffff/clab run|r %s", key,
      key == "combat" and "while at a dummy" or "out of combat")
    return
  end
  ns.Heading(string.format("run %s — %s — ok %d / error %d / skipped %d",
    key, run.at or "?", run.counts.ok or 0, run.counts.error or 0, run.counts.skipped or 0))
  for _, r in ipairs(run.results) do
    local col = STATUS_COLOR[r.status] or "|cffffffff"
    local tail
    if r.status == "ok" then tail = short(r.value)
    elseif r.status == "error" then tail = r.err
    else tail = r.why end
    ns.Printf("  %s%s|r %s  |cff808080%s|r", col, r.status, r.id, tostring(tail))
  end
end

ns.RegisterCommand("list",
  "print the last run to chat (result only, no verdict). `list combat` for the in-combat run",
  function(arg)
    local key = (arg and arg:lower():find("combat")) and "combat" or "ooc"
    renderRun(key)
  end)

--------------------------------------------------------------------------------
-- /clab guide — pull-based coverage checklist (the Probe.lua:472-564 pattern)
--------------------------------------------------------------------------------
-- No frame, no ticker: re-type it to re-check.  What it buys is TIMING — you learn
-- the capture is incomplete while still standing at the dummy, not an hour later
-- from wowkb.lab.  Every goal asks whether a channel was EXERCISED, never whether
-- it returned a particular value (Probe.lua:522-526: never write a goal that can
-- never go green — a secret op is SUPPOSED to error, so "the secret table ran" is
-- the honest goal, not "it passed").
local function run(key) return ns.db and ns.db.runs and ns.db.runs[key] end
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

local GOALS = {
  { label = "OOC run captured",
    nudge = "run |cffffffff/clab run|r out of combat",
    met = function() return hasRun("ooc") end },
  { label = "in-combat run captured",
    nudge = "pull a dummy, then |cffffffff/clab run|r in combat",
    met = function() return hasRun("combat") end },
  { label = "a genuine secret value obtained (a §4.2 row executed in combat)",
    nudge = "the combat run must be taken WHILE in combat at a dummy — cooldown reads only go secret then",
    met = function() local ran = secretRowCounts("combat"); return ran > 0 end },
  { label = "the full §4.2 secret-op table run (all rows execute, not skip)",
    nudge = "if only some rows ran, the secret went away mid-run — re-run |cffffffff/clab run|r in sustained combat",
    met = function() local ran, total = secretRowCounts("combat"); return total > 0 and ran == total end },
}

ns.RegisterCommand("guide",
  "coverage checklist — what this session's runs still need (pull-based; re-type to re-check)",
  function()
    ns.Heading("coverage — what these runs still need")
    local left = 0
    for _, g in ipairs(GOALS) do
      local ok = false
      local called, res = pcall(g.met)
      if called then ok = res and true or false end
      if ok then
        ns.Printf("  |cff88ff88[x]|r %s", g.label)
      else
        left = left + 1
        ns.Printf("  |cff808080[ ]|r %s   |cffffd100<- %s|r", g.label, g.nudge)
      end
    end
    if left == 0 then
      ns.Print("  |cff88ff88coverage complete|r — |cffffffff/reload|r, then |cffffffffuv run python -m wowkb.lab show|r")
    else
      ns.Printf("  -> |cffffd100%d goal%s left|r; re-run |cffffffff/clab guide|r to re-check, then |cffffffff/reload|r",
        left, left == 1 and "" or "s")
    end
  end)

-- Autorun — the lab drives itself.
--
-- This addon is only enabled when someone is deliberately gathering values, so the
-- gathering must not cost keystrokes.  Nothing here waits to be asked: it runs when
-- the game reaches a state a run can answer from, and retries the rows that could not
-- answer yet while that state lasts.
--
-- The rule it is built around: a secret value only exists in combat, and only on the
-- player's TRACKED cooldowns.  That precondition arrives and departs on its own, so
-- the driver watches for it rather than asking a human to type during a pull.
--
-- The panel (Dumps.lua) stays for the captures a human takes at a moment only they can
-- recognise.  This file covers everything that is merely a matter of being in the right
-- state, which is all of it except that.

local ADDON, ns = ...

local SETTLE_AFTER_LOGIN = 6      -- let the CDM populate and the spec resolve
local COMBAT_FIRST_RUN = 2        -- cooldowns must actually be rolling
local RETRY_EVERY = 3
local RETRY_LIMIT = 12            -- ~36 s of pull; past that the pull is the problem

local state = { ranOOC = false, ranCombat = false, retries = 0, announced = false, said = nil }

-- Retry only what is still unanswered — which is a superset of the secret rows, and
-- the right set: a two-phase round-trip and a listener awaiting its first firing are
-- also "no answer yet" and also cost nothing to re-ask.  A blanket re-run on a 3 s
-- timer would re-send addon messages and churn the round-trip payloads to learn nothing.
local function retryFilter()
  local pending = ns.Unanswered()
  return function(rec) return pending[rec.id] == true end, next(pending) ~= nil
end

local function announceCoverage()
  local cov = ns.Coverage()
  if cov.complete then
    if not state.announced then
      state.announced = true
      ns.Print("|cff88ff88coverage complete|r — every channel this session can exercise has run.")
      ns.Print("  |cffffffff/clab|r -> [copy] to take it now, or |cffffffff/reload|r then "
        .. "|cffffffffuv run python -m wowkb.lab show|r")
    end
    return true
  end
  -- An unmet goal is said ONCE per state change, not every tick: the driver announces
  -- what is still missing so a session cannot end quietly incomplete, which is exactly
  -- what happened when the goals only covered the secret table.
  if not state.said or state.said ~= cov.left then
    state.said = cov.left
    ns.Printf("|cffffcc44coverage|r — %d goal%s left. |cffffffff/clab|r -> coverage -> "
      .. "|cffffffff[print]|r", cov.left, cov.left == 1 and "" or "s")
    for _, g in ipairs(cov.goals) do
      if not g.met then ns.Printf("  |cff808080[ ] %s|r", g.label) end
    end
  end
  return false
end

local function runFull(why)
  local run = ns.RunAll()
  ns.Printf("|cff66ddaaauto|r %s — %d tests, ok %d / declined %d / error %d / skipped %d",
    why, #run.results, run.counts.ok or 0, run.counts.declined or 0,
    run.counts.error or 0, run.counts.skipped or 0)
  announceCoverage()
  return run
end

local ticker
local function stopRetries()
  if ticker then ticker:Cancel(); ticker = nil end
end

-- While the pull lasts, keep offering the unanswered rows a chance.  A secret can be
-- unobtainable at one instant and available the next (nothing tracked was on cooldown
-- yet), so a single in-combat run is not evidence that the row cannot answer.
local function startRetries()
  stopRetries()
  state.retries = 0
  ticker = C_Timer.NewTicker(RETRY_EVERY, function()
    if not InCombatLockdown() then stopRetries(); return end
    state.retries = state.retries + 1
    local filter, anyPending = retryFilter()
    if not anyPending or state.retries > RETRY_LIMIT then
      stopRetries()
      if not anyPending then announceCoverage() end
      return
    end
    local before = ns.Unanswered()
    local nBefore = 0
    for _ in pairs(before) do nBefore = nBefore + 1 end
    ns.RunAll(filter)
    local after = ns.Unanswered()
    local nAfter = 0
    for _ in pairs(after) do nAfter = nAfter + 1 end
    if nAfter < nBefore then
      ns.Printf("|cff66ddaaauto|r retry %d — %d row%s answered, %d still waiting",
        state.retries, nBefore - nAfter, (nBefore - nAfter) == 1 and "" or "s", nAfter)
      announceCoverage()
    end
  end)
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("PLAYER_REGEN_DISABLED")
f:RegisterEvent("PLAYER_REGEN_ENABLED")
f:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")
f:RegisterEvent("TRAIT_CONFIG_UPDATED")

f:SetScript("OnEvent", function(_, event)
  if event == "PLAYER_LOGIN" then
    C_Timer.After(SETTLE_AFTER_LOGIN, function()
      if InCombatLockdown() then return end
      state.ranOOC = true
      runFull("out of combat")
    end)

  elseif event == "PLAYER_REGEN_DISABLED" then
    -- The whole point of the addon: this is the only window in which the §4.2 rows
    -- can execute at all, and it is not one a human should have to type into.
    C_Timer.After(COMBAT_FIRST_RUN, function()
      if not InCombatLockdown() then return end
      state.ranCombat = true
      runFull("in combat")
      startRetries()
    end)

  elseif event == "PLAYER_REGEN_ENABLED" then
    stopRetries()

  else
    -- A spec or hero-tree swap changes the answers, so the stamp on the old rows no
    -- longer describes the character. Re-run out of combat; in combat the retry
    -- ticker is already covering it and a full re-run mid-pull is not worth the churn.
    if not state.ranOOC then return end
    C_Timer.After(2, function()
      if InCombatLockdown() then return end
      state.announced = false
      runFull("build changed")
    end)
  end
end)

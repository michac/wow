-- Lab.lua — the test registry, the runner, and stash().
--
-- The collect/assert split (m4.5-t3-plan.md), restated here because the lab is
-- NOT wowkb.cdmp: cdmp asserts a known answer against regression; the lab
-- DISCOVERS an unknown one.  So a test's `run` returns a VALUE and nothing more —
-- no `expect`, no pass/fail.  `expect` lives in questions.json and is never
-- compared in-game.  The reader renders result beside expectation and a HUMAN
-- decides; an automatic verdict would be the instrument grading its own subject.
local ADDON, ns = ...

ns.tests = {}       -- ordered list of registered test records
ns.testByID = {}    -- id -> record (for the cross-check and dup detection)

-- ns.Test{ id, anchor, bucket, phase, needs, question, run } ------------------
-- `phase` and `needs` go unused by pass 1 (everything is manual; needs is only
-- "secret") but exist from day one, because validating the record format on a
-- cheap pass is the entire reason pass 1 exists.
function ns.Test(rec)
  assert(type(rec) == "table", "ns.Test needs a table")
  assert(type(rec.id) == "string" and rec.id ~= "", "ns.Test needs an id")
  assert(type(rec.run) == "function", "ns.Test '" .. tostring(rec.id) .. "' needs a run function")
  if ns.testByID[rec.id] then
    error("duplicate ClientLab test id: " .. rec.id)
  end
  rec.phase = rec.phase or "manual"
  ns.tests[#ns.tests + 1] = rec
  ns.testByID[rec.id] = rec
end

-- stash(v) -- reduce an observed value to something SavedVariables can hold ----
-- Everything in a run ends up in SavedVariables, so a Secret Value must never
-- reach it (serializing one would at best write garbage and at worst taint the
-- writer).  Secrets degrade to the STRING "<secret>", which is itself the finding
-- the reader wants ("this read secret here").  Scalars pass through; a flat table
-- of scalars is recursed ONE level (many tests return { require=..., os=... });
-- anything else (function, frame, deeper table) drops to a descriptive string
-- rather than persisting a live reference.
local function stashScalar(v)
  if ns.IsSecret(v) then return "<secret>" end
  local t = type(v)
  if t == "number" or t == "boolean" or t == "string" then return v end
  if t == "function" then return "<function>" end
  if t == "nil" then return nil end
  return "<" .. t .. ">"
end
function ns.stash(v)
  if ns.IsSecret(v) then return "<secret>" end
  if type(v) ~= "table" then return stashScalar(v) end
  if ns.IsSecretTable(v) then return "<secret table>" end
  local out = {}
  for k, val in pairs(v) do
    -- Keys are expected to be scalar strings/numbers; a secret key can't be used
    -- as a table key anyway, so guard it into a placeholder string.
    local key = (type(k) == "string" or type(k) == "number") and k or tostring(k)
    if type(val) == "table" and not ns.IsSecretTable(val) then
      -- one further level, flattened to scalars so nothing non-scalar persists
      local inner = {}
      for k2, v2 in pairs(val) do
        local key2 = (type(k2) == "string" or type(k2) == "number") and k2 or tostring(k2)
        inner[key2] = stashScalar(v2)
      end
      out[key] = inner
    else
      out[key] = stashScalar(val)
    end
  end
  return out
end

-- runOne(rec) -- the result envelope: status is "ok" | "error" | "skipped" -----
-- Every test is pcall'd individually.  A test that ERRORS records the error as
-- its answer (for many of these, "it errors" IS the claim), so one test can never
-- break the run.  `skipped` is never a pass: a test whose precondition is unmet
-- records why and never a value (the cdmp SKIP rule).
local function runOne(rec)
  local out = {
    id = rec.id, anchor = rec.anchor, bucket = rec.bucket, question = rec.question,
  }
  -- Precondition gate: `needs = "secret"` requires a genuine Secret Value, which
  -- only exists in combat.  Out of combat it is skipped WITH A REASON, never run.
  if rec.needs == "secret" then
    local sv, why
    if ns.GetSecret then sv, why = ns.GetSecret() end
    if sv == nil then
      out.status = "skipped"
      out.why = why or "no secret value obtainable in this context"
      return out
    end
  end
  local ok, res = pcall(rec.run)
  if ok then
    out.status = "ok"
    out.value = ns.stash(res)
  else
    out.status = "error"
    out.err = tostring(res)
  end
  return out
end

-- run() -- run every registered test, wrap in a header, store by combat state --
-- The header carries the fields wowkb.lab (and cdmp.py:414-443) use for
-- patch-drift and mixed-capture detection: at / version / interface / combat /
-- instance.  Keyed ooc vs combat so the two runs of a session don't clobber.
function ns.RunAll()
  local combat = InCombatLockdown() and true or false
  local inInstance, instanceType = IsInInstance()
  local run = {
    at = date and date("%Y-%m-%d %H:%M:%S") or "?",
    version = ns.version,
    interface = select(4, GetBuildInfo()),
    combat = combat,
    instance = inInstance and (instanceType or "unknown") or "none",
    results = {},
    counts = { ok = 0, error = 0, skipped = 0 },
  }
  for _, rec in ipairs(ns.tests) do
    local r = runOne(rec)
    run.results[#run.results + 1] = r
    run.counts[r.status] = (run.counts[r.status] or 0) + 1
  end
  ns.db.runs = ns.db.runs or {}
  ns.db.runs[combat and "combat" or "ooc"] = run
  return run
end

ns.RegisterCommand("run",
  "run every test and store the result under ClientLabDB.runs (run once OOC, once in combat, then /reload)",
  function()
    local run = ns.RunAll()
    ns.Heading(string.format("ran %d tests (%s) — ok %d / error %d / skipped %d",
      #run.results, run.combat and "in combat" or "out of combat",
      run.counts.ok, run.counts.error, run.counts.skipped))
    ns.Print("stored under |cffffffffClientLabDB.runs." .. (run.combat and "combat" or "ooc")
      .. "|r — |cffffffff/reload|r then read SavedVariables/ClientLab.lua")
  end)

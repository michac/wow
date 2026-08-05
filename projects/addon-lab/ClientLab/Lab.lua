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

-- Which roundtrip tests have completed a read-back THIS SESSION.  Session-scoped on
-- purpose: a round trip is arm -> /reload -> read, so "has it read back" is a fact
-- about the session you are in, and persisting it would let a stale flag report a
-- payload as recovered that this session never saw.
ns.readBacks = {}

-- ns.Test{ id, anchor, bucket, phase, needs, blocked, question, run } ---------
-- `blocked` is a string naming the input the test cannot obtain — the Lua mirror of
-- `blocked_on` in questions.json.  It exists so the "everything answerable has
-- answered" goal can go green: three tests can only ever report `measured = false`
-- (no boolean secret is obtainable, LibStub is not loaded, no runtime predicate
-- exposes the event flags), and a goal that can never go green is worse than no goal.
-- Declaring the blocker is how a test opts out; nothing may opt out silently.
function ns.Test(rec)
  assert(type(rec) == "table", "ns.Test needs a table")
  assert(type(rec.id) == "string" and rec.id ~= "", "ns.Test needs an id")
  assert(type(rec.run) == "function", "ns.Test '" .. tostring(rec.id) .. "' needs a run function")
  assert(rec.blocked == nil or (type(rec.blocked) == "string" and rec.blocked ~= ""),
    "ns.Test '" .. tostring(rec.id) .. "': `blocked` must name what is missing")
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
--
-- DECLINED IS NEVER A PASS EITHER.  A test returning `{ measured = false, why = … }`
-- ran correctly and observed NOTHING, so its status is `ok` — that is the wire format
-- and it stays, because the wire describes the TEST.  What it must never do is render
-- green beside a test that answered, so the envelope carries a `declined` flag and
-- every counter and colour downstream splits on it.  `readBack` is the same idea for
-- the other half of a round trip: the run that recovers a payload is the one that
-- measured something, and it is not always the latest one.
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
    if type(out.value) == "table" then
      out.declined = out.value.measured == false
      if out.value.phase == "read-back" then
        out.readBack = true
        ns.readBacks[rec.id] = true
      end
    end
  else
    out.status = "error"
    out.err = tostring(res)
  end
  return out
end

--- Counts split on `declined`, so `ok` means ANSWERED rather than merely ran.
--- Recomputed from the results rather than tallied as they land: a retry merges into
--- an existing run and replaces rows in place, and an incremental tally has to undo
--- the old row's contribution to stay right.
function ns.Recount(run)
  local c = { ok = 0, error = 0, skipped = 0, declined = 0 }
  for _, r in ipairs(run.results) do
    if r.declined then c.declined = c.declined + 1
    else c[r.status] = (c[r.status] or 0) + 1 end
  end
  run.counts = c
  return c
end

-- The `runs` stream -----------------------------------------------------------
-- Eight sessions because a pass that swaps spec AND hero tree burns 4-5 /reloads,
-- and the whole point of a ring over the old two named slots is that a later run
-- must not destroy the evidence an earlier one produced.
ns.runsLog = ns.Capture.Open("runs", { sessions = 8, cap = 2000 })

-- Stamp() -- the slice dimensions, read fresh at run time ----------------------
-- Anything a later reader might slice by has to be recorded NOW: a row is data, but
-- the CONTEXT it was taken in is unrecoverable afterwards (the capture standard's
-- rule 4, which cost a re-fly elsewhere).  Spec and hero tree are probed BY STRING
-- because their homes are exactly the kind of thing that moves between patches, and
-- a bare identifier for a maybe-absent global is what the ns.G rule exists to stop.
local function specName()
  local getIndex = ns.G("GetSpecialization") or ns.G("C_SpecializationInfo.GetSpecialization")
  local getInfo = ns.G("GetSpecializationInfo") or ns.G("C_SpecializationInfo.GetSpecializationInfo")
  if type(getIndex) ~= "function" or type(getInfo) ~= "function" then return "?" end
  local okI, idx = pcall(getIndex)
  if not okI or type(idx) ~= "number" then return "?" end
  local okN, _, name = pcall(getInfo, idx)
  return (okN and type(name) == "string") and name or ("index " .. idx)
end

-- The hero tree is recorded as its subTreeID, not a name: resolving the name needs a
-- live trait config and would fail differently from the rest of the stamp.  A number
-- is enough to slice by, which is all a stamp owes anyone.
local function heroTree()
  local fn = ns.G("C_ClassTalents.GetActiveHeroTalentSpec")
  if type(fn) ~= "function" then return "?" end
  local ok, id = pcall(fn)
  if not ok or type(id) ~= "number" then return "none" end
  return id
end

function ns.Stamp()
  local inInstance, instanceType = IsInInstance()
  return {
    combat = InCombatLockdown() and true or false,
    spec = specName(),
    hero = heroTree(),
    instance = inInstance and (instanceType or "unknown") or "none",
  }
end

-- RunAll() -- run every registered test, emit one ROW per result ---------------
-- Rows rather than lines because the consumer is `wowkb.lab`, which renders a result
-- beside its expectation and reads sub-fields out of it; a pre-rendered line would
-- freeze that shape forever.  The stamp goes on EVERY ROW as well as the session
-- meta, because one session holds several runs (an OOC one, then a combat one) and
-- a session-level `combat` could only describe one of them.
--
-- `filter` makes a run a RETRY of rows that could not answer yet rather than a fresh
-- run of everything: the driver retries the secret rows every few seconds while a pull
-- lasts, and re-running the whole set on that timer would re-send addon messages and
-- churn the round-trip payloads for nothing.  A retry MERGES into the same combat/ooc
-- slot, so a row that finally answers replaces its own earlier `skipped`.
--
-- The slot is session-local and is what the panel and the coverage goals read.  It is
-- deliberately NOT persisted: SavedVariables carries the capture stream, and keeping a
-- second copy is how the two shapes drift apart.
function ns.RunAll(filter)
  local stamp = ns.Stamp()
  local at = date and date("%Y-%m-%d %H:%M:%S") or "?"
  ns.runCount = (ns.runCount or 0) + 1
  local key = stamp.combat and "combat" or "ooc"

  ns.lastRuns = ns.lastRuns or {}
  local run = filter and ns.lastRuns[key]
  if not run then
    run = { results = {}, byID = {}, counts = { ok = 0, error = 0, skipped = 0, declined = 0 } }
  end
  run.at, run.index = at, ns.runCount
  run.version = ns.version
  run.interface = select(4, GetBuildInfo())
  run.combat, run.instance = stamp.combat, stamp.instance
  run.spec, run.hero = stamp.spec, stamp.hero

  for _, rec in ipairs(ns.tests) do
    if not filter or filter(rec) then
      local r = runOne(rec)
      if run.byID[r.id] then
        for i, existing in ipairs(run.results) do
          if existing.id == r.id then run.results[i] = r; break end
        end
      else
        run.results[#run.results + 1] = r
      end
      run.byID[r.id] = r
      ns.runsLog:Row({
        run = ns.runCount, at = at,
        id = r.id, status = r.status, anchor = r.anchor, bucket = r.bucket,
        value = r.value, err = r.err, why = r.why,
        combat = stamp.combat, spec = stamp.spec, hero = stamp.hero,
        instance = stamp.instance,
      })
    end
  end

  ns.Recount(run)

  -- Late-bound, per the standard: re-stamping on every run means a session that
  -- respecs mid-way is labelled by where it ENDED rather than mislabelled throughout.
  ns.runsLog:Meta("spec", stamp.spec)
  ns.runsLog:Meta("hero", stamp.hero)
  ns.runsLog:Meta("instance", stamp.instance)
  ns.runsLog:Meta("interface", run.interface)
  ns.runsLog:Meta("runs", ns.runCount)

  ns.lastRuns[key] = run
  return run
end

--- Which rows still have no answer FROM WHERE YOU ARE NOW. The driver's retry set and
--- its stop condition.
---
--- Scoped to the slot matching the current combat state, and that scoping is the whole
--- correctness of it: a needs="secret" row skipped OUT of combat is answered correctly —
--- there is no secret to be had there — so counting it as pending makes the retry set
--- permanently non-empty and the driver churns until its own retry limit stops it.
---
--- DECLINED ROWS COUNT AS PENDING TOO. A listener that has seen no firing yet and a
--- round trip awaiting its read-back are both "no answer yet", and both can go green a
--- few seconds later without anyone doing anything. A test that declares `blocked` is
--- excluded: its input does not exist on this machine, so re-asking it is pure churn.
function ns.Unanswered()
  local run = ns.lastRuns and ns.lastRuns[InCombatLockdown() and "combat" or "ooc"]
  local out = {}
  if run then
    for _, r in ipairs(run.results) do
      local rec = ns.testByID[r.id]
      if (r.status == "skipped" or r.declined) and not (rec and rec.blocked) then
        out[r.id] = true
      end
    end
  end
  return out
end

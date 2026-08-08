-- T_CooldownManager.lua — tests anchored in knowledge/addon-dev/cooldown-manager.md.
local ADDON, ns = ...


--------------------------------------------------------------------------------
-- §7 — does the Assisted Combat oracle MOVE?
--
-- The existing claim proves GetNextCastSpell is READABLE in combat and records a
-- constant 691 at every sample.  That constant is not evidence the oracle is stuck:
-- the recorder that produced it dedups by readability CLASS, so it only sampled at
-- transitions between readable and secret — of which there were none — and a value
-- that changed every GCD would have been recorded exactly once, looking identical
-- to a value that never changed.  The measurement cannot distinguish the two.
--
-- So the instrument here is the whole point.  Sampling on a TIMER would repeat the
-- same mistake at a different resolution: the oracle is a rotation answer, so the
-- moment it should advance is the moment you CAST something.  This samples on the
-- player's own UNIT_SPELLCAST_SUCCEEDED — readable in all four cast phases per §7
-- Tier 3 — which puts one sample on each GCD boundary and pairs it with the cast
-- that preceded it.  A human can then read "I cast X, it then said Y" down the
-- series and judge whether the answer is tracking or merely present.
--
-- DISTINCT COUNT IS THE FINDING.  distinct == 1 across a real pull means the oracle
-- is constant and anything built on it has no content; distinct > 1 means it moves
-- and the remaining question is whether it moves SENSIBLY, which is a judgement no
-- test should make for a reader.
--------------------------------------------------------------------------------

local MAX_SAMPLES = 24     -- a pull's worth; the accumulator stops appending past this
local REPORT_AT = 8        -- enough casts that "it never changed" means something
local PARTIAL_AFTER = 25   -- seconds; report a short series rather than lose it entirely
local MIN_PARTIAL = 3

local probe

local function since(t) return string.format("%.0fs", GetTime() - t) end

-- Read the oracle on both arguments.  Guarded through ns.IsSecret even though §7
-- measured it plain: "measured plain once" is not "plain by contract", and a secret
-- reaching a sample string would be formatted, which is the one thing never allowed.
local function readOracle()
  local fn = ns.G("C_AssistedCombat.GetNextCastSpell")
  if type(fn) ~= "function" then return nil, nil, "C_AssistedCombat.GetNextCastSpell absent" end
  local function one(arg)
    local ok, v = pcall(fn, arg)
    if not ok then return "errored" end
    if v == nil then return "nil" end
    if ns.IsSecret(v) then return "<secret>" end
    if type(v) ~= "number" then return "<" .. type(v) .. ">" end
    return v
  end
  return one(false), one(true), nil
end

local function spellName(id)
  if type(id) ~= "number" then return tostring(id) end
  local fn = ns.G("C_Spell.GetSpellName")
  if type(fn) ~= "function" then return tostring(id) end
  local ok, name = pcall(fn, id)
  if not ok or type(name) ~= "string" then return tostring(id) end
  return name .. "(" .. id .. ")"
end

local function arm()
  local st = {
    armedAt = GetTime(), casts = 0, samples = {}, distinct = {}, distinctN = 0,
    absent = nil,
  }
  local f = CreateFrame("Frame", nil, UIParent)
  f:Hide()
  f:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "player")
  -- Payload is (self, event, unitTarget, castGUID, spellID) — the 5th is the spell.
  f:SetScript("OnEvent", function(_, _, _, _, spellID)
    st.casts = st.casts + 1
    if #st.samples >= MAX_SAMPLES then return end
    local vFalse, vTrue, absent = readOracle()
    if absent then st.absent = absent; return end
    -- Distinctness is tracked on the `false` argument alone: it is the one a consumer
    -- would use (no "must be on a visible button" filter), and mixing both arguments
    -- into one set would report movement that is really just the two disagreeing.
    if type(vFalse) == "number" and not st.distinct[vFalse] then
      st.distinct[vFalse] = true
      st.distinctN = st.distinctN + 1
    end
    local cast = ns.IsSecret(spellID) and "<secret>" or spellName(spellID)
    st.samples[#st.samples + 1] = string.format("%s -> %s / %s",
      cast, tostring(vFalse), tostring(vTrue))
  end)
  st.frame = f
  return st
end

ns.Test{
  id = "assisted-combat-next-cast-varies",
  anchor = "cooldown-manager.md:902",
  bucket = "call",
  question = "Does C_AssistedCombat.GetNextCastSpell's return VARY over a pull, or is it constant? §7 proves it is readable in combat but recorded a constant 691 with an instrument that could not have seen it change.",
  run = function()
    if not probe then
      probe = arm()
      local vFalse, vTrue, absent = readOracle()
      return {
        measured = false,
        why = absent
          or "probe armed this run — it samples the oracle on each of your own casts; keep attacking",
        armedReading = tostring(vFalse) .. " / " .. tostring(vTrue),
      }
    end
    if probe.absent then
      return { measured = false, why = probe.absent }
    end
    local n = #probe.samples
    local enough = n >= REPORT_AT
      or (n >= MIN_PARTIAL and (GetTime() - probe.armedAt) > PARTIAL_AFTER)
    if not enough then
      return {
        measured = false,
        why = string.format("only %d cast%s sampled in %s — need %d (or %d after %ds); "
          .. "a short series cannot tell a constant oracle from an unexercised one",
          n, n == 1 and "" or "s", since(probe.armedAt), REPORT_AT, MIN_PARTIAL, PARTIAL_AFTER),
        castsSeen = probe.casts,
      }
    end
    return {
      window = since(probe.armedAt),
      casts = probe.casts,
      sampled = n,
      distinctValues = probe.distinctN,
      verdictInput = probe.distinctN == 1
        and "CONSTANT across this series — the oracle did not move"
        or "MOVED — read the series and judge whether it tracks",
      -- One string, not a nested list: ns.stash flattens only one level, and the
      -- reader renders text.  Format is `cast -> next(false) / next(true)`.
      series = table.concat(probe.samples, " | "),
    }
  end,
}

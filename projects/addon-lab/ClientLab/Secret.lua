-- Secret.lua — obtain ONE genuine Secret Value, and gate the tests that need it.
--
-- The §4.2 operation table (T_Security.lua) needs a real Secret Value to operate
-- on.  CDMProbe established where one comes from: a spell cooldown read is secret
-- IN COMBAT and readable out of it (probe-baseline.json cooldown-read-combat-seam,
-- measured open-world, so the gate is COMBAT not instancing).
--
-- ⚠ CORRECTED 2026-07-24 after the first in-game run.  The v0.1.0 build read the
-- GCD spell (61304) and its cooldown fields read NON-secret even in combat — the
-- GCD placeholder is not a tracked cooldown, so the restriction doesn't apply to
-- it.  The seam applies to the player's ACTUAL tracked abilities.  So we enumerate
-- the built-in Cooldown Manager's tracked spells (Essential + Utility) via the
-- public C_CooldownViewer API — spec-independent, since every spec has tracked
-- Essential cooldowns — and read one of THOSE.
--
-- ns.GetSecret() -> value, source   (a genuine Secret Value + where it came from)
--               -> nil,  why       (no secret obtainable in this context)
--
-- Out of combat the fields read as plain numbers, so GetSecret returns nil with a
-- reason and every needs="secret" test records `skipped`, never a value.
local ADDON, ns = ...

-- The tracked-cooldown categories that carry real ability cooldowns.  Buff
-- categories track auras, not cooldowns, so they're not a cooldown-secret source.
local function categories()
  local E = Enum and Enum.CooldownViewerCategory
  if not E then return {} end
  local out = {}
  if E.Essential then out[#out + 1] = E.Essential end
  if E.Utility then out[#out + 1] = E.Utility end
  return out
end

-- Every spellID the Cooldown Manager currently tracks, in category order.  Guarded
-- at each hop: the category set call, the per-id info call, and the .spellID field
-- (which is itself Secret-guarded — a secret spellID is no use as a lookup key).
local function trackedSpellIDs()
  local ids, seen = {}, {}
  if not (C_CooldownViewer and C_CooldownViewer.GetCooldownViewerCategorySet
          and C_CooldownViewer.GetCooldownViewerCooldownInfo) then
    return ids
  end
  for _, cat in ipairs(categories()) do
    local ok, set = pcall(C_CooldownViewer.GetCooldownViewerCategorySet, cat, true)
    if ok and type(set) == "table" then
      for _, cdID in ipairs(set) do
        local ok2, info = pcall(C_CooldownViewer.GetCooldownViewerCooldownInfo, cdID)
        if ok2 and type(info) == "table" and not ns.IsSecretTable(info) then
          local sid
          if pcall(function() sid = info.spellID end)
             and type(sid) == "number" and not ns.IsSecret(sid) and not seen[sid] then
            seen[sid] = true
            ids[#ids + 1] = sid
          end
        end
      end
    end
  end
  return ids
end

-- Pull a secret field off one spell's cooldown table.  Guards in order, because
-- each is a different world: the call failing, a secret TABLE (can't be indexed at
-- all), then a secret FIELD on a readable table.  Only the last is the value we
-- want.  Returns (value, "ok") | (nil, "why-not").
local function secretFromCooldown(spellID)
  local ok, info = pcall(C_Spell.GetSpellCooldown, spellID)
  if not ok then return nil, "GetSpellCooldown errored" end
  if type(info) ~= "table" then return nil, "non-table" end
  if ns.IsSecretTable(info) then return nil, "secret-table" end
  local st
  if not pcall(function() st = info.startTime end) then return nil, "index-errored" end
  if ns.IsSecret(st) then return st, "ok" end
  local dur
  if not pcall(function() dur = info.duration end) then return nil, "index-errored" end
  if ns.IsSecret(dur) then return dur, "ok" end
  return nil, "read-non-secret"
end

function ns.GetSecret()
  if not ns.SecretAPI() then
    return nil, "issecretvalue() absent on this build — no Secret Values exist"
  end
  if not (C_Spell and C_Spell.GetSpellCooldown) then
    return nil, "C_Spell.GetSpellCooldown absent"
  end
  if not InCombatLockdown() then
    return nil, "no secret value obtainable out of combat — pull a dummy and re-run"
  end
  local ids = trackedSpellIDs()
  if #ids == 0 then
    return nil, "no tracked Cooldown Manager spells found (is the built-in Cooldown Manager enabled with Essential cooldowns?)"
  end
  -- Walk the tracked spells and return the first whose cooldown reads secret.  A
  -- spell not on cooldown may still read secret in combat, but if none does we say
  -- so with the count we tried rather than a bare nil.
  for _, sid in ipairs(ids) do
    local v = secretFromCooldown(sid)
    if v ~= nil then
      return v, string.format("GetSpellCooldown(%d).cooldown-field", sid)
    end
  end
  return nil, string.format("scanned %d tracked spells in combat, none read secret", #ids)
end

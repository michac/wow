-- T_AuraEdges.lua — can a rider hear a TARGET aura go up and down, via the CDM alert channel?
--
-- The route `C_UnitAuras` no longer offers (§4.7.1) may exist as an EDGE rather than a read.
-- The Cooldown Manager binds a TrackedBuff row to an aura and calls
-- `CooldownViewerItemMixin:TriggerAlertEvent("OnAuraApplied" | "OnAuraRemoved")` when it
-- changes. Observing a CALL is not reading a value, so if the edges fire this is a genuinely
-- READABLE up/down signal — a predicate, not a display.
--
-- ⚠ PREDICTION, from source, recorded before the flight so the result can contradict it:
--
--   * A `HideByDefault` row NEVER gets an item frame, so it raises NOTHING — silently. The
--     settings data provider rewrites its category to a hidden pseudo-category
--     [T1 src @12.1: CooldownViewerSettingsDataProvider.lua:115-118] and the live viewer
--     draws its rows from that same provider [T1 src @12.1: CooldownViewer.lua:2066-2069].
--   * Un-hidden (the player adds it to tracked buffs), the edges SHOULD fire, on genuine
--     application and removal — and NOT on a refresh of a live aura (§5.4's one-shot limit).
--   * The aura edges should NOT be gated on the player's alert configuration the way
--     `Available` is: that gate is `OnUpdate` registration, and the aura path runs from
--     `OnUnitAura` instead [T1 src @12.1: CooldownViewer.lua:1845-1867].
--
-- So the experiment is a PAIRING: every edge is recorded beside the row's bound-state at that
-- instant, because "no edges" and "no edges WHILE HIDDEN" are different findings and they
-- look identical in a log that records only one of them.

local ADDON, ns = ...

-- Retribution's two TrackedBuff rows, from DB2 [CooldownSetSpell @12.1.0.69214]. The base
-- spell of 109208 is the TALENT 383344 (blue icon); the aura it binds is the linked spell
-- 383346, the DoT that carries Blade of Justice's icon.
local WATCH = {
  [109208] = "Expurgation (talent 383344 -> aura 383346)",
  [109294] = "Greater Judgment (231663)",
}

local VIEWERS = {
  "EssentialCooldownViewer", "UtilityCooldownViewer",
  "BuffIconCooldownViewer", "BuffBarCooldownViewer",
}

local edges = {}          -- {n, cid, event, boundAtTheTime}
local hooked = {}         -- item frame -> true, so a re-scan does not double-hook

--- Is this cooldownID one the viewers actually laid out? That is the whole bound/hidden
--- axis: the provider is the single source of truth the live viewer reads from.
--- Which cooldownIDs actually reached an ITEM FRAME. That is the bound/hidden axis, and it
--- is ground truth rather than inference: `RefreshLayout` acquires one frame per entry of the
--- ordered list and `RefreshData` either assigns a cooldownID or calls `ClearCooldownID()`
--- [T1 src @12.1: CooldownViewer.lua:2021-2031, 2071-2080], so a frame carrying the id IS the
--- definition of bound — and it is the same object the alert hook attaches to, which is what
--- makes it the right question to ask.
---
--- ⚠ The settings provider's ordered list is NOT this. Reconciling against
--- `GetOrderedCooldownIDsForCategory` returned the row in both halves of an enable/disable A/B
--- `[client 2026-08-19]`, so it answers something other than "will this raise an edge".
local function boundIDs()
  local out, frames = {}, 0
  for _, name in ipairs(VIEWERS) do
    local viewer = ns.G(name)
    local pool = viewer and viewer.itemFramePool
    if pool and pool.EnumerateActive then
      for item in pool:EnumerateActive() do
        frames = frames + 1
        if item.GetCooldownID then
          local ok, cid = pcall(item.GetCooldownID, item)
          -- A cleared frame answers nil, which is exactly the "laid out but bound to nothing"
          -- case and must not count.
          if ok and type(cid) == "number" then out[cid] = true end
        end
      end
    end
  end
  if frames == 0 then return out, "no active item frames — is the Cooldown Manager enabled?" end
  return out
end

--- Hook every item frame's `TriggerAlertEvent`. Per INSTANCE, never the mixin table — the
--- methods are `Mixin()`-copied onto each frame, so a hook on the shared table would observe
--- nothing (§5.1).
local function hookFrames()
  local n = 0
  for _, name in ipairs(VIEWERS) do
    local viewer = ns.G(name)
    local pool = viewer and viewer.itemFramePool
    if pool and pool.EnumerateActive then
      for item in pool:EnumerateActive() do
        if not hooked[item] and item.TriggerAlertEvent then
          hooked[item] = true
          n = n + 1
          hooksecurefunc(item, "TriggerAlertEvent", function(self, event)
            local ok, cid = pcall(self.GetCooldownID, self)
            if not ok then cid = nil end
            edges[#edges + 1] = {
              cid = cid, event = tostring(event),
              combat = InCombatLockdown() and true or false,
            }
          end)
        end
      end
    end
  end
  return n
end

ns.Test{
  id = "cdm-aura-edges-need-a-bound-row",
  anchor = "cooldown-manager.md:§5.1",
  bucket = "call",
  question = "Do OnAuraApplied/OnAuraRemoved fire for a TARGET DoT's TrackedBuff row — and "
    .. "does that depend on the row being un-hidden from HideByDefault?",
  run = function()
    if not (C_CooldownViewer and C_CooldownViewer.GetCooldownViewerCooldownInfo) then
      return { measured = false, why = "C_CooldownViewer absent" }
    end
    local out = { combat = InCombatLockdown() and true or false }
    out["item frames hooked this run"] = hookFrames()

    local bound, why = boundIDs()
    if why then out["bound set"] = why end

    -- Per watched row: the raw DB2 flags, and whether it reached a frame. Both, always —
    -- the join is the experiment, and either alone is the silence this test exists to break.
    local anyBound = false
    for cid, label in pairs(WATCH) do
      local ok, info = pcall(C_CooldownViewer.GetCooldownViewerCooldownInfo, cid)
      local flags, hidden = nil, nil
      if ok and type(info) == "table" then
        pcall(function() flags = info.flags end)
        if type(flags) == "number" and Enum.CooldownSetSpellFlags then
          hidden = (flags % (2 * Enum.CooldownSetSpellFlags.HideByDefault))
                   >= Enum.CooldownSetSpellFlags.HideByDefault
        end
      end
      local isBound = bound[cid] == true
      if isBound then anyBound = true end
      out[string.format("cid %d · %s", cid, label)] = string.format(
        "flags=%s hideByDefault=%s BOUND=%s",
        tostring(flags), tostring(hidden), tostring(isBound))
    end

    -- The edges themselves, flattened. Kept per-row rather than counted, because WHICH cid
    -- fired is the join back to the bound state above.
    out["edges observed"] = #edges
    for i, e in ipairs(edges) do
      if i > 12 then out["edges (truncated)"] = "showing first 12" break end
      out[string.format("edge %02d", i)] = string.format(
        "cid=%s %s combat=%s", tostring(e.cid), e.event, tostring(e.combat))
    end

    -- ⚠ Zero edges is only an ANSWER once we know a watched row was bound and the DoT was
    -- actually applied. Bound + cast + silence is the finding; unbound + silence is the
    -- prediction and needs the other half of the pair to mean anything.
    if not anyBound then
      out.measured = false
      out.why = "neither watched row has an item frame — this run records the HIDDEN half. "
        .. "Add Expurgation to your tracked buffs in the Cooldown Manager and fly again for "
        .. "the other half; BOUND should flip, and it did not with the previous detector."
      return out
    end
    if #edges == 0 then
      out.measured = false
      out.why = "a watched row IS bound but no edge fired yet — apply and drop the DoT "
        .. "while in combat, then let this retry"
      return out
    end
    out.measured = true
    return out
  end,
}

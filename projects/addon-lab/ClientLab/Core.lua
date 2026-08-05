-- ClientLab — a long-lived scratch addon that answers questions about the WoW
-- client by running one line of Lua in it.  It is the home for experimental
-- API-poking that would otherwise accrete inside real addons.
--
-- INVARIANT (the one rule that makes junk safe to accumulate here):
--   NOTHING IN A PRODUCT ADDON MAY EVER DEPEND ON ClientLab.
-- Not CDMProbe, not BucketBinds, not PlannerState.  ClientLab reads the client;
-- it never becomes a dependency of anything shipped.  See CLAUDE.md.
--
-- Not a product: never released through ghaddons, never in the wowkb.addon
-- registry, no version discipline.  Deploy is a directory copy (wowkb.lab deploy).
--
-- This bootstrap is copied nearly verbatim from CDMProbe/Core.lua — the
-- non-destructive defaults merge, the secret-safe ns.Print + capture buffer, and
-- the ns.RegisterCommand / commandOrder / pcall'd dispatch registry.  The lab
-- deliberately reuses the CDMProbe idioms it has already run in-game, so pass 1
-- is validating the RECORD FORMAT, not the plumbing.
local ADDON, ns = ...

ns.name = ADDON
ns.version = (C_AddOns and C_AddOns.GetAddOnMetadata and C_AddOns.GetAddOnMetadata(ADDON, "Version")) or "?"

-- Saved-variable defaults -----------------------------------------------------
-- Deliberately empty.  Everything this addon persists goes through Capture into the
-- single `captures` key, which Capture.lua creates on first write — one top-level
-- store per addon is rule 1 of the capture standard, and the alternative is the
-- seven-stores-four-retention-policies state that standard exists to end.
local DEFAULTS = {}

-- The pre-standard keys.  `runs` was a two-slot store (ooc/combat) where a second
-- run of the same kind CLOBBERED the first; `journal` was reserved for a lifecycle
-- log and never written.  Both are gone, and they are actively removed rather than
-- left to rot, so `ClientLabDB` cannot accumulate a shape nothing reads.
-- The last legacy run is archived at projects/addon-lab/runs/, and `wowkb.lab show`
-- keeps a reader for the old shape, so purging here loses nothing.
local RETIRED = { "runs", "journal" }

-- Chat helpers ----------------------------------------------------------------
-- Print also tees a color-stripped copy into an optional capture buffer so a
-- command can persist its whole (untruncated) output to SavedVariables — chat
-- scrollback eats the important lines.  Secret-safe: a Secret Value must never be
-- indexed/formatted (that taints), so it degrades to the string "<secret>".
local PREFIX = "|cff66ddaaClientLab|r "
local function secret(v)
  if type(issecretvalue) == "function" then
    local ok, s = pcall(issecretvalue, v)
    return ok and s
  end
  return false
end
local function strip(s)
  if secret(s) then return "<secret>" end
  return (tostring(s):gsub("|c%x%x%x%x%x%x%x%x", ""):gsub("|r", ""))
end
function ns.Print(msg)
  local disp = secret(msg) and "<secret>" or tostring(msg)
  DEFAULT_CHAT_FRAME:AddMessage(PREFIX .. disp)
  if ns._cap then ns._cap[#ns._cap + 1] = strip(msg) end
end
function ns.Printf(fmt, ...) ns.Print(string.format(fmt, ...)) end
function ns.Heading(t) ns.Print("|cffffd100" .. tostring(t) .. "|r") end

function ns.BeginCapture() ns._cap = {} end
function ns.EndCapture() ns._cap = nil end

-- Secret-Value helpers (copied from CDMProbe/Util.lua) -------------------------
-- Guarded so they are safe when the API is absent — issecretvalue itself may not
-- exist on some builds, which is one of the things the lab measures.
function ns.SecretAPI() return type(issecretvalue) == "function" end
function ns.IsSecret(v)
  if not ns.SecretAPI() then return false end
  local ok, s = pcall(issecretvalue, v)
  return ok and s or false
end
function ns.IsSecretTable(t)
  if type(issecrettable) ~= "function" then return false end
  local ok, s = pcall(issecrettable, t)
  return ok and s or false
end

-- GlobalType(name) -- probe a global BY STRING, never by identifier -----------
-- Many pass-1 tests ask whether a global exists (require, os, io, table.freeze,
-- the C_CombatLog.* names, UIDropDownMenu_*).  Writing those as bare identifiers
-- would make luacheck scream at exactly the code whose job is to touch them, so
-- the RULE is: look a probed global up by string.
--
-- It returns BOTH the type via rawget(_G, name) and the type via a pcall'd lookup
-- in the addon's own environment, because the two can DIFFER — a name scoped
-- through GetCurrentEnvironment() (e.g. UIDropDownMenu_*) may be present in one
-- and absent from the other, and that difference is itself the answer to
-- libraries-and-ecosystem.md:552.  Dotted names ("table.freeze") are walked one
-- segment at a time so a missing parent yields "nil", not an error.
local function walk(root, name)
  local cur = root
  for seg in string.gmatch(name, "[^.]+") do
    if type(cur) ~= "table" then return nil, false end
    cur = rawget(cur, seg)
    if cur == nil then return nil, false end
  end
  return cur, true
end
-- Resolve a global BY STRING to its value (or nil).  This is how a test that must
-- actually CALL a probed global gets a callable without naming it as an
-- identifier — the resolved value is a local, so luacheck never sees the name.
function ns.G(name)
  local v = walk(_G, name)
  return v
end
function ns.GlobalType(name)
  local v, found = walk(_G, name)
  local g = found and type(v) or "nil"
  -- The addon environment: getfenv(1) is this file's env, which is the addon's
  -- shared environment.  A pcall guards the (unlikely) case getfenv is restricted.
  local env = "nil"
  local ok, e = pcall(function()
    local fenv = getfenv and getfenv(1) or _G
    local ev, ok2 = walk(fenv, name)
    return ok2 and type(ev) or "nil"
  end)
  if ok and e then env = e end
  return { g = g, env = env }
end

-- Command registry ------------------------------------------------------------
ns.commands = {}       -- name -> { fn = function(argString), help = string }
ns.commandOrder = {}
function ns.RegisterCommand(name, help, fn)
  if not ns.commands[name] then ns.commandOrder[#ns.commandOrder + 1] = name end
  ns.commands[name] = { fn = fn, help = help }
end

local function printHelp()
  ns.Heading("ClientLab — /clab <command>")
  for _, name in ipairs(ns.commandOrder) do
    ns.Printf("  |cff88ff88%s|r — %s", name, ns.commands[name].help)
  end
  ns.Print("The lab runs itself: out of combat after login, again when combat starts, "
    .. "then retries whatever could not answer while the pull lasts. Nothing to type.")
end

-- Bare /clab opens the panel.  There is no run command to type: a human-triggered
-- capture is a BUTTON (the capture standard §4), and everything else happens on its
-- own, so chat has nothing left to drive.
local function dispatch(msg)
  msg = (msg or ""):gsub("^%s+", ""):gsub("%s+$", "")
  local cmd, rest = msg:match("^(%S+)%s*(.*)$")
  cmd = cmd and cmd:lower() or ""
  if cmd == "" and ns.Dumps then return ns.Dumps.Toggle() end
  if cmd == "" or cmd == "help" then return printHelp() end
  local entry = ns.commands[cmd]
  if not entry then
    ns.Printf("unknown command '%s' — try |cffffffff/clab help|r", cmd)
    return
  end
  local ok, err = pcall(entry.fn, rest)
  if not ok then ns.Printf("|cffff4040error in '%s':|r %s", cmd, tostring(err)) end
end

SLASH_CLIENTLAB1 = "/clab"
SLASH_CLIENTLAB2 = "/clientlab"
SlashCmdList["CLIENTLAB"] = dispatch

-- Bootstrap -------------------------------------------------------------------
local boot = CreateFrame("Frame")
boot:RegisterEvent("ADDON_LOADED")
boot:RegisterEvent("PLAYER_LOGIN")
boot:SetScript("OnEvent", function(_, event, arg1)
  if event == "ADDON_LOADED" and arg1 == ADDON then
    ClientLabDB = ClientLabDB or {}
    for k, v in pairs(DEFAULTS) do
      if ClientLabDB[k] == nil then
        ClientLabDB[k] = (type(v) == "table") and CopyTable(v) or v
      end
    end
    for _, k in ipairs(RETIRED) do ClientLabDB[k] = nil end
    ns.db = ClientLabDB
    -- A SECOND file, deliberately.  Probes that write values the serializer may not
    -- survive — NaN, infinity, a self-referencing table, a Secret Value — go here, so
    -- a file the loader rejects costs only the probe that caused it.  ns.db holds the
    -- capture ring, which is the evidence everything else in this addon exists to make.
    ClientLabScratchDB = ClientLabScratchDB or {}
    ns.scratch = ClientLabScratchDB
  elseif event == "PLAYER_LOGIN" then
    ns.Printf("v%s loaded. |cffffffff/clab help|r — the client lab.", ns.version)
  end
end)

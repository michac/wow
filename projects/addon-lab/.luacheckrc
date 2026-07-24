-- .luacheckrc — static-analysis config for ClientLab.
--
-- Same doctrine as CDMProbe's (m4.5-plan.md T1): CURATE THIS CONFIG, do NOT
-- inline-suppress.  A real catch (undefined global, dead local, shadow) gets
-- FIXED; a WoW API name the lab legitimately CALLS goes in the read_globals std
-- below.  Every name here is one the lab uses by IDENTIFIER, grepped from source.
--
-- The lab has a design rule that keeps this list SHORT: a global whose EXISTENCE
-- is in question is probed BY STRING (ns.GlobalType / ns.G), never by identifier —
-- so `require`, `os`, `io`, `string.rtgsub`, the C_CombatLog.* names, the
-- UIDropDownMenu_* set, C_EventUtils, CreateFromMixins, issecure, bit.band, etc.
-- never appear here.  Only globals the lab unconditionally calls are listed.
--
--     luacheck ClientLab/
-- (needs `luarocks install --local luacheck` + ~/.luarocks/bin on PATH).

std = "lua51+wow"

stds.wow = {
  read_globals = {
    "CreateFrame", "hooksecurefunc",
    "InCombatLockdown", "IsInInstance", "GetBuildInfo", "date",
    "CopyTable", "DEFAULT_CHAT_FRAME",
    "issecretvalue", "issecrettable",
    "C_AddOns", "C_Spell", "C_CooldownViewer", "Enum",
  },
  -- The lab's TRUE global writes.  Everything else is `local ADDON, ns = ...`.
  globals = {
    "SLASH_CLIENTLAB1", "SLASH_CLIENTLAB2",
    "SlashCmdList",
    "ClientLabDB",            -- SavedVariable
  },
}

-- Same intentional-noise knobs as CDMProbe, same justifications:
--   * unused_args — the WoW event-handler idiom is function(_, event, a1..aN).
--   * max_line_length — several files carry long doc-comment banners by design.
unused_args = false
max_line_length = false

-- Every module opens `local ADDON, ns = ...` (WoW's addonName, addonTable); most
-- use only `ns`, so `ADDON` reads unused — but it is the idiomatic, self-
-- documenting name for the first vararg and Core.lua uses it.  Ignore the
-- unused-ADDON case specifically; a genuine unused local under any other name
-- still warns.
ignore = { "211/ADDON" }

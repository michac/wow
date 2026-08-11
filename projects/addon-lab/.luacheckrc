-- .luacheckrc — static-analysis config for ClientLab.
--
-- Same doctrine as CDMProbe's (projects/cooldown-hud/docs/archive/m4.5-plan.md T1): CURATE THIS CONFIG, do NOT
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

-- Vendored third-party code is not ours to lint: LibOrbitGlow-1.0 (MIT) and LibStub
-- (public domain) ship as-is so a library update is a plain copy, and their warnings
-- would drown ours.  This is a FILE exclusion, not an inline suppression — the
-- zero-suppression rule still binds every file the lab writes.
exclude_files = { "ClientLab/Libs/**" }

stds.wow = {
  read_globals = {
    "CreateFrame", "hooksecurefunc",
    "InCombatLockdown", "IsInInstance", "GetBuildInfo", "date",
    "CopyTable", "DEFAULT_CHAT_FRAME",
    "issecretvalue", "issecrettable",
    "C_AddOns", "C_Spell", "C_CooldownViewer", "Enum",
    -- Glow.lua reads flipbook grids off C_Texture.GetAtlasInfo. Core namespace, existence
    -- not in question; the MayReturnNothing result is what gets handled, not the global.
    "C_Texture",
    -- The one guarded name in this list, and deliberately so. LibStub is VENDORED under
    -- Libs/ and loaded first by the .toc, so it is not a maybe-missing global to probe by
    -- string — it is ours. Glow.lua still guards the call (`LibStub and LibStub(...)`)
    -- because a load failure at file scope would take down the very fallback that reports
    -- it, which is a degradation path rather than an existence question.
    "LibStub",
    -- Scratch-frame and timing surface for the frame/event/lifecycle tests: these are
    -- globals whose EXISTENCE is not in question, so they are called by identifier.
    -- Anything a test is actually asking about still goes through ns.G / ns.GlobalType.
    "UIParent", "C_Timer", "GetTime",
  },
  -- The lab's TRUE global writes.  Everything else is `local ADDON, ns = ...`.
  globals = {
    "SLASH_CLIENTLAB1", "SLASH_CLIENTLAB2",
    "SlashCmdList",
    "ClientLabDB",            -- SavedVariable
    "ClientLabScratchDB",     -- SavedVariable: quarantine for payloads that may not survive a write
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

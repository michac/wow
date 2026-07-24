-- T_State.lua — tests anchored in
-- knowledge/addon-dev/state-persistence-and-communication.md.
--
-- (Not in the plan's illustrative T_* list, but the per-KB-topic-file split is the
-- design rule, so a state-anchored test belongs here rather than jammed into
-- T_Module.  It seeds the file the pass-2 SavedVariables candidates will fill.)
local ADDON, ns = ...

ns.Test{
  id = "addon-message-prefix-limit", anchor = "state-persistence-and-communication.md:935", bucket = "call",
  question = "Is the 16-char addon-message prefix limit real? Register a 16-char and a 17-char prefix and record both return values.",
  run = function()
    local reg = ns.G("C_ChatInfo.RegisterAddonMessagePrefix")
    if type(reg) ~= "function" then return { api = "C_ChatInfo.RegisterAddonMessagePrefix absent" } end
    local p16 = string.rep("A", 16)
    local p17 = string.rep("B", 17)
    local ok16, r16 = pcall(reg, p16)
    local ok17, r17 = pcall(reg, p17)
    return {
      len16 = ok16 and tostring(r16) or ("errored: " .. tostring(r16)),
      len17 = ok17 and tostring(r17) or ("errored: " .. tostring(r17)),
    }
  end,
}

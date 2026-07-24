-- T_Module.lua — tests anchored in knowledge/addon-dev/module-architecture.md.
local ADDON, ns = ...

ns.Test{
  id = "create-from-mixins-nil", anchor = "module-architecture.md:104", bucket = "call",
  question = "Does CreateFromMixins(nil) error, or silently produce an empty mixin? This is the failure mode of a .toc listing a mixin file after its consumer.",
  run = function()
    local fn = ns.G("CreateFromMixins")
    if type(fn) ~= "function" then return { api = "CreateFromMixins absent" } end
    local ok, res = pcall(fn, nil)
    if ok then
      -- Silent success is the nastier outcome worth flagging: what did it produce?
      return { errored = false, resultType = type(res),
               empty = (type(res) == "table") and (next(res) == nil) or nil }
    end
    return { errored = true, err = tostring(res) }
  end,
}

-- T_Libraries.lua — tests anchored in knowledge/addon-dev/libraries-and-ecosystem.md.
local ADDON, ns = ...

ns.Test{
  id = "dropdown-menu-globals", anchor = "libraries-and-ecosystem.md:552", bucket = "call",
  question = "Do the deprecated UIDropDownMenu_* globals still resolve for addon code at 12.0.7? The file resolves through GetCurrentEnvironment() rather than _G.",
  run = function()
    -- This is the test ns.GlobalType's two-lookup design exists for: a name may be
    -- present in the addon environment yet absent from _G (or vice versa), and that
    -- difference IS the answer.  Report both columns for each name.
    local names = {
      "UIDropDownMenu_Initialize", "UIDropDownMenu_AddButton",
      "UIDropDownMenu_SetWidth", "ToggleDropDownMenu",
    }
    local out = {}
    for _, n in ipairs(names) do
      local t = ns.GlobalType(n)
      out[n] = string.format("_G=%s env=%s", t.g, t.env)
    end
    return out
  end,
}

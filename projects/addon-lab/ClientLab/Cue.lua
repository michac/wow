-- Cue — a text-cue picker. Each treatment is drawn three times on one row: on a plain
-- string, on a secret string fed through SetText, and on one fed through a
-- DurationTextBinding. The difference between the columns is the experiment, and the
-- anchoring readout beside them says whether the leaf rule held.
--
-- Motion is C-side: every treatment is a list of animation DESCRIPTORS built into an
-- AnimationGroup, so nothing here runs per frame. Ordering and bounds: docs/cue-treatments.md.
--
-- INVARIANT: nothing in a product addon may depend on ClientLab. A treatment that wins
-- here gets built into cap directly.

local ADDON, ns = ...

ns.Cue = {}
local C = ns.Cue

-- Everything maybe-missing is resolved BY STRING, once, and reported on the panel's
-- capability line rather than assumed.
local function fn(name)
  local v = ns.G(name)
  return type(v) == "function" and v or nil
end
local GetCooldownDuration = fn("C_Spell.GetSpellCooldownDuration")
local MakeSecondsFormatter = fn("C_StringUtil.CreateSecondsFormatter")
local MakeTextBinding = fn("C_DurationUtil.CreateDurationTextBinding")
local GetSpellName = fn("C_Spell.GetSpellName")
local GetSpellTexture = fn("C_Spell.GetSpellTexture")
local GetBaseCooldown = fn("GetSpellBaseCooldown")
local MakeColor = fn("CreateColor")
local EnumFonts = fn("GetFonts")
local REALTIME = ns.G("Enum.DurationTimeModifier.RealTime")
local ASPECT_TEXT = ns.G("Enum.SecretAspect.Text")
local SCALE_MODE = ns.G("Enum.FontStringScaleAnimationMode")

local CAPS = {
  { "C_Spell.GetSpellCooldownDuration", GetCooldownDuration },
  { "C_StringUtil.CreateSecondsFormatter", MakeSecondsFormatter },
  { "C_DurationUtil.CreateDurationTextBinding", MakeTextBinding },
  { "C_Spell.GetSpellTexture", GetSpellTexture },
  { "CreateColor", MakeColor },
  { "Enum.DurationTimeModifier.RealTime", REALTIME },
  { "Enum.SecretAspect.Text", ASPECT_TEXT },
  { "Enum.FontStringScaleAnimationMode", SCALE_MODE },
}

-- The rate ceiling for flashing TEXT, and the reason it is a constant rather than a
-- taste: MIL-STD-1472F allows 3-5 Hz for a warning light but caps flashing text at 2 Hz
-- at ~70 % on-time, and flicker sensitivity peaks at 8-15 Hz, the band most
-- photosensitive individuals respond in. Over-limit settings stay REACHABLE and get
-- flagged on the row, because the comparison is what the panel is for.
local TEXT_MAX_HZ, TEXT_DUTY, TEXT_ALPHA_FLOOR = 2.0, 0.70, 0.65

-- cap's tier hues as DATA. LOW carries no hue on an icon — cap veils it and draws no
-- ring — but a text cue still has to render, so LOW is a dimmed grey here. That is a
-- choice this panel makes, not a value read out of cap.
local COLOURS = {
  { name = "HIGH",   c = { 1.00, 0.92, 0.55 } },
  { name = "MEDIUM", c = { 0.45, 0.70, 0.95 } },
  { name = "LOW",    c = { 0.62, 0.62, 0.66 } },
  { name = "white",  c = { 1.00, 1.00, 1.00 } },
  { name = "red",    c = { 1.00, 0.35, 0.30 } },
}

local MODES = { "steady", "onset" }
local TRANSIENTS = { { name = "250ms", secs = 0.25 }, { name = "400ms", secs = 0.40 } }
local DECAYS = { { name = "0.6s", secs = 0.6 }, { name = "1s", secs = 1.0 },
                 { name = "1.6s", secs = 1.6 } }
local AUTOFIRE = { { name = "off" }, { name = "3s", secs = 3 },
                   { name = "6s", secs = 6 }, { name = "12s", secs = 12 } }
-- ⚠ GLYPHS FIRST, AND THAT ORDER IS THE POINT. "Animate the plate, never the glyphs" is
-- a finding to be TESTED here, not a premise to build in — defaulting to the plate meant
-- a person could press every treatment and never see text move once.
local TARGETS = { "glyphs", "plate" }
local MOTION = { { name = "smooth" }, { name = "17Hz", hz = 17 }, { name = "8Hz", hz = 8 } }
local BACKDROPS = { "icon", "plate", "none" }
-- A ready spell's REMAINING cooldown is zero, which is why a correctly-picked 300 s
-- ability still rendered nothing. ignoreGCD = false reports the global cooldown instead,
-- and that rolls on every cast — so it is the default and something always ticks.
local SOURCES = { { name = "GCD", ignoreGCD = false }, { name = "full CD", ignoreGCD = true } }
local RAMPS = { "duty", "IN_OUT", "NONE", "IN", "OUT", "OUT_IN" }
local SMOOTHINGS = { "IN_OUT", "NONE", "IN", "OUT", "OUT_IN" }
local FACES = {
  { name = "Friz", path = "Fonts\\FRIZQT__.TTF" },
  { name = "Arial", path = "Fonts\\ARIALN.TTF" },
  { name = "Morph", path = "Fonts\\MORPHEUS.TTF" },
  { name = "Skurri", path = "Fonts\\skurri.ttf" },
}
local FLAGS = { "", "OUTLINE", "THICKOUTLINE", "MONOCHROME", "OUTLINE, MONOCHROME" }
local VIEWERS = { "EssentialCooldownViewer", "UtilityCooldownViewer",
                  "BuffIconCooldownViewer", "BuffBarCooldownViewer" }

local COL_W, LABEL_W = 104, 104
local PANEL_W, PANEL_H = 760, 700
local SCROLL_TOP, SCROLL_H = -88, 260
local READOUT_X = 450
local Y_LEGEND, Y_SEL, Y_CTRL, Y_PARAMS, Y_FOOTER = -354, -390, -424, -558, -640
local COLUMNS = {
  { key = "plain",   x = 122, caption = "plain" },
  { key = "settext", x = 230, caption = "secret · SetText" },
  { key = "binding", x = 338, caption = "secret · binding" },
}

-- Animation descriptors ---------------------------------------------------------

--- Call a widget method by name and report an ABSENT one rather than falling through.
--- A `Scale` animation that never received its endpoints looks exactly like one that is
--- playing and not helping, so a miss has to be loud.
local function call(obj, name, ...)
  local m = obj[name]
  if type(m) ~= "function" then return false, name .. " absent" end
  local ok, err = pcall(m, obj, ...)
  return ok, (not ok) and tostring(err) or nil
end

-- ⚠ THE DIRECTION WORD MOVES BETWEEN TYPES. Alpha is SetFromAlpha / SetToAlpha; Scale is
-- SetScaleFrom / SetScaleTo. SetFromScale / SetToScale, which older addon code uses, do
-- not exist at 12.0.7.68887 — hence the probe above rather than a bare call. VertexColor
-- takes ColorMixin OBJECTS, not four numbers.
local SETTERS = {
  Alpha = function(a, d)
    local ok, why = call(a, "SetFromAlpha", d.from[1])
    if not ok then return false, why end
    return call(a, "SetToAlpha", d.to[1])
  end,
  Scale = function(a, d)
    local ok, why = call(a, "SetScaleFrom", d.from[1], d.from[2])
    if not ok then return false, why end
    ok, why = call(a, "SetScaleTo", d.to[1], d.to[2])
    if not ok then return false, why end
    call(a, "SetOrigin", "CENTER", 0, 0)
    return true
  end,
  Translation = function(a, d)
    return call(a, "SetOffset", d.to[1], d.to[2])
  end,
  VertexColor = function(a, d)
    if not MakeColor then return false, "CreateColor absent" end
    local okA, c1 = pcall(MakeColor, d.from[1], d.from[2], d.from[3], 1)
    local okB, c2 = pcall(MakeColor, d.to[1], d.to[2], d.to[3], 1)
    if not (okA and okB) then return false, "CreateColor failed" end
    local ok, why = call(a, "SetStartColor", c1)
    if not ok then return false, why end
    return call(a, "SetEndColor", c2)
  end,
}

-- Steady = one animation under BOUNCE, or a three-part duty cycle; onset = hold then
-- decay, sequenced by `order`, with the repeat padded by `endDelay` so no Lua timer runs.
-- ⚠ BOUNCE + smoothing is symmetric by construction and cannot dwell longer at one end,
-- so the standard's 70 % on-time is three animations rather than a wave shape.
local function alphaShape(target, lo, hi, period, ramp, ctx)
  if ctx.onset then
    return { target = target, looping = ctx.pad and "REPEAT" or "NONE", finalAlpha = true,
      anims = {
        { kind = "Alpha", from = { hi }, to = { hi }, duration = ctx.transient },
        { kind = "Alpha", from = { hi }, to = { lo }, duration = ctx.decay,
          smoothing = "OUT", endDelay = ctx.pad },
      } }
  end
  if ramp == "duty" then
    local on, edge = period * TEXT_DUTY, period * (1 - TEXT_DUTY) / 2
    return { target = target, looping = "REPEAT",
      anims = {
        { kind = "Alpha", from = { hi }, to = { hi }, duration = on },
        { kind = "Alpha", from = { hi }, to = { lo }, duration = edge, smoothing = "IN_OUT" },
        { kind = "Alpha", from = { lo }, to = { hi }, duration = edge, smoothing = "IN_OUT" },
      } }
  end
  return { target = target, looping = "BOUNCE",
    anims = { { kind = "Alpha", from = { lo }, to = { hi },
                duration = period / 2, smoothing = ramp } } }
end

-- Treatments --------------------------------------------------------------------

local function P(key, label, values, default, render)
  return { key = key, label = label, values = values, default = default or 1, render = render }
end
local function SEC(v) return ("%.2gs"):format(v) end
local function PCT(v) return ("%d%%"):format(math.floor(v * 100 + 0.5)) end
local function PX(v) return v .. "px" end
local function HUE(v) return COLOURS[v].name end
local function FACE(v) return FACES[v].name end
local function FLAG(v) return FLAGS[v] == "" and "none" or FLAGS[v] end
local function AS_IS(v) return tostring(v) end

local greyOn = false

-- A dichromat keeps luminance and loses hue, and so does anyone's peripheral vision. If
-- the tiers cannot be ranked at zero saturation they cannot be ranked at all.
local function hueOf(i)
  local c = COLOURS[i].c
  if not greyOn then return c[1], c[2], c[3] end
  local y = 0.299 * c[1] + 0.587 * c[2] + 0.114 * c[3]
  return y, y, y
end

-- The secret is never anything but the string's CONTENT. Every number below is plain,
-- and `build` returns data — type, endpoints, duration, smoothing, looping — which is
-- the shape that pastes into cap, unlike a ticker's internal arithmetic.
local TREATMENTS = {
  {
    id = "plate", label = "plate pulse",
    note = "FIRST because the evidence puts it first: an opaque billboard isolating text "
        .. "from the background beat five other styles over six real textures, and glyph "
        .. "motion wrecks identification. Animate the backdrop, never the glyphs",
    params = {
      P("hue", "plate", { 1, 2, 5, 4 }, 1, HUE),
      P("period", "period", { 0.5, 0.8, 1.2, 2.0 }, 2, SEC),
      P("floor", "floor", { 0.00, 0.15, 0.35 }, 2, PCT),
      P("ramp", "ramp", RAMPS, 1, AS_IS),
    },
    rate = "period",
    reset = function(cell, p)
      -- Only recolours in `plate` backdrop mode; over an icon the art stays the art.
      if cell.backdrop == "plate" then cell.plate:SetColorTexture(hueOf(p.hue)) end
      cell.plate:Show()
    end,
    build = function(p, ctx) return alphaShape("plate", p.floor, 0.9, p.period, p.ramp, ctx) end,
  },
  {
    id = "static", label = "static baseline",
    note = "tinted only — the control every other row is judged against. Onset mode does "
        .. "nothing to it, which is the honest answer for a treatment with no time axis",
    params = {},
  },
  {
    id = "alpha", label = "alpha pulse",
    note = "always either fading in or fading out — BOUNCE with IN_OUT and a long period, "
        .. "so the whole cycle is ramp and none of it is dwell. Slower is also SAFER: the "
        .. "2 Hz limit is a ceiling and going under it is free",
    params = {
      P("period", "period", { 0.4, 0.5, 0.8, 1.6, 2.0, 3.0 }, 5, SEC),
      P("floor", "floor", { 0.30, 0.50, 0.65, 0.80 }, 3, PCT),
      P("ceil", "ceiling", { 0.75, 1.00 }, 2, PCT),
      P("ramp", "ramp", RAMPS, 2, AS_IS),
    },
    rate = "period",
    build = function(p, ctx) return alphaShape(nil, p.floor, p.ceil, p.period, p.ramp, ctx) end,
  },
  {
    id = "colour", label = "colour pulse",
    note = "a VertexColor animation between two tier hues. It reaches text for a measured "
        .. "reason: SetTextColor and SetVertexColor are ONE storage slot on a FontString",
    params = {
      P("from", "from", { 1, 2, 4, 5, 3 }, 1, HUE),
      P("to", "to", { 2, 1, 5, 4, 3 }, 1, HUE),
      P("period", "period", { 0.8, 1.2, 2.0, 3.0 }, 3, SEC),
      P("ramp", "ramp", SMOOTHINGS, 1, AS_IS),
    },
    rate = "period",
    build = function(p, ctx)
      local a, b = { hueOf(p.from) }, { hueOf(p.to) }
      if ctx.onset then
        return { looping = ctx.pad and "REPEAT" or "NONE", anims = {
          { kind = "VertexColor", from = b, to = b, duration = ctx.transient },
          { kind = "VertexColor", from = b, to = a, duration = ctx.decay,
            smoothing = "OUT", endDelay = ctx.pad },
        } }
      end
      return { looping = "BOUNCE", anims = {
        { kind = "VertexColor", from = a, to = b,
          duration = p.period / 2, smoothing = p.ramp },
      } }
    end,
  },
  {
    id = "scale", label = "scale pulse",
    note = "expand vs contract at EQUAL energy — capture by expansion is a published "
        .. "result WITH a published rebuttal. Vertex scales the rendered quad and "
        .. "pixelates; FontSize re-rasterises per step, and is the default with "
        .. "smoothScaling on",
    params = {
      P("period", "period", { 0.5, 0.8, 1.2, 2.0 }, 2, SEC),
      P("amp", "amplitude", { 0.05, 0.15, 0.35 }, 2, PCT),
      P("dir", "direction", { "expand", "contract" }, 1, AS_IS),
      P("mode", "glyph scale", { "FontSize", "Vertex" }, 1, AS_IS),
      P("smooth", "smoothScaling", { true, false }, 1, AS_IS),
    },
    liveNote = function(p)
      return ("scaleAnimationMode=%s smoothScaling=%s"):format(p.mode, tostring(p.smooth))
    end,
    reset = function(cell, p)
      if SCALE_MODE and SCALE_MODE[p.mode] ~= nil then
        local ok, why = call(cell.fs, "SetScaleAnimationMode", SCALE_MODE[p.mode])
        if not ok then cell.err = "SetScaleAnimationMode: " .. tostring(why) end
      end
      local ok, why = call(cell.fs, "SetSmoothScaling", p.smooth)
      if not ok then cell.err = "SetSmoothScaling: " .. tostring(why) end
    end,
    build = function(p, ctx)
      local s = 1 + p.amp * (p.dir == "contract" and -1 or 1)
      if ctx.onset then
        return { looping = ctx.pad and "REPEAT" or "NONE", anims = {
          { kind = "Scale", from = { s, s }, to = { s, s }, duration = ctx.transient },
          { kind = "Scale", from = { s, s }, to = { 1, 1 }, duration = ctx.decay,
            smoothing = "OUT", endDelay = ctx.pad },
        } }
      end
      return { looping = "BOUNCE", anims = {
        { kind = "Scale", from = { 1, 1 }, to = { s, s },
          duration = p.period / 2, smoothing = "IN_OUT" },
      } }
    end,
  },
  {
    id = "flash", label = "onset flash",
    note = "abrupt appearance, then settle. In onset mode the fire IS the flash, so this "
        .. "row shows the shared transient shape undiluted",
    params = {
      P("flash", "flash", { 1.00, 0.85 }, 1, PCT),
      P("settle", "settle", { 0.25, 0.45, 0.65 }, 3, PCT),
      P("decay", "decay", { 0.15, 0.30, 0.60 }, 2, SEC),
      P("interval", "every", { 1.5, 3.0, 5.0 }, 2, SEC),
    },
    rate = "interval",
    build = function(p, ctx)
      if ctx.onset then
        return alphaShape(nil, p.settle, p.flash, p.decay,
          "NONE", { onset = true, transient = ctx.transient, decay = p.decay, pad = ctx.pad })
      end
      return { looping = "REPEAT", anims = {
        { kind = "Alpha", from = { p.flash }, to = { p.settle },
          duration = p.decay, smoothing = "OUT",
          endDelay = math.max(0, p.interval - p.decay) },
      } }
    end,
  },
  {
    id = "outline", label = "font / outline",
    note = "no motion at all — legibility as the whole treatment, and the thing a plate "
        .. "competes with. SetFont returns a success bool and this row reports it",
    params = {
      P("face", "face", { 1, 2, 3, 4 }, 1, FACE),
      P("height", "height", { 12, 14, 16, 20, 24 }, 3, PX),
      P("flags", "outline", { 1, 2, 3, 4, 5 }, 2, FLAG),
      P("shadow", "shadow", { 0, 1, 2 }, 2, PX),
      P("shade", "shadow hue", { 5, 3 }, 1, HUE),
    },
    reset = function(cell, p)
      local ok, applied = pcall(cell.fs.SetFont, cell.fs,
        FACES[p.face].path, p.height, FLAGS[p.flags])
      cell.fontOK = ok and (applied ~= false)
      cell.fs:SetShadowOffset(p.shadow, -p.shadow)
      local r, g, b = hueOf(p.shade)
      cell.fs:SetShadowColor(r * 0.2, g * 0.2, b * 0.2, 1)
    end,
  },
  {
    id = "weight", label = "weight cross-fade",
    note = "the closest thing to animating font WEIGHT: WoW has no continuous weight axis "
        .. "and outline thickness is not animatable, so this cross-fades two leaves at "
        .. "different outline flags with opposed Alpha animations",
    params = {
      P("thin", "thin", { 1, 2, 4 }, 1, FLAG),
      P("thick", "thick", { 3, 2, 5 }, 1, FLAG),
      P("period", "period", { 0.8, 1.2, 2.0, 3.0 }, 3, SEC),
      P("ramp", "ramp", SMOOTHINGS, 1, AS_IS),
    },
    rate = "period",
    reset = function(cell, p)
      if cell.font then
        local okA, a = pcall(cell.fs.SetFont, cell.fs, cell.font, cell.size, FLAGS[p.thin])
        local okB, b = pcall(cell.fs2.SetFont, cell.fs2, cell.font, cell.size, FLAGS[p.thick])
        cell.fontOK = okA and okB and a ~= false and b ~= false
      end
      cell.fs2:Show()
      cell.fs2:ClearAllPoints()
      cell.fs2:SetPoint("CENTER", cell.holder, "CENTER", 0, 0)
    end,
    -- Two leaves on the common holder, never anchored to each other, each with its own
    -- group; BOUNCE runs them in step so one rises exactly as the other falls.
    build = function(p, ctx)
      local d = ctx.onset and (ctx.transient + ctx.decay) or p.period / 2
      local loop = ctx.onset and "NONE" or "BOUNCE"
      return {
        { target = "text", looping = loop, anims = {
          { kind = "Alpha", from = { 1 }, to = { 0 }, duration = d, smoothing = p.ramp } } },
        { target = "text2", looping = loop, anims = {
          { kind = "Alpha", from = { 0 }, to = { 1 }, duration = d, smoothing = p.ramp } } },
      }
    end,
  },
  {
    id = "double", label = "offset double",
    note = "⚠ HERE TO BE FALSIFIED, not as a candidate. It has no supporting literature at "
        .. "all, and every mechanism predicts a legibility cost. A 1 px shadow is its best "
        .. "case and therefore the default; larger offsets are where it should fail",
    params = {
      P("dx", "offset x", { 1, 2, 3, 4 }, 1, PX),
      P("dy", "offset y", { 0, 1, 2, 3 }, 2, PX),
      P("back", "behind", { 5, 3, 4 }, 1, HUE),
      P("front", "in front", { 4, 1, 2 }, 2, HUE),
    },
    reset = function(cell, p)
      cell.fs2:Show()
      cell.fs2:ClearAllPoints()
      cell.fs2:SetPoint("CENTER", cell.holder, "CENTER", p.dx, -p.dy)
      cell.fs2:SetTextColor(hueOf(p.back))
      cell.fs:SetTextColor(hueOf(p.front))
    end,
  },
  {
    id = "jitter", label = "jitter",
    note = "a Translation on the driven region. Positional, not luminance — the flash "
        .. "threshold does not bind it, so its fast steps are unflagged on purpose",
    params = {
      P("amp", "amplitude", { 1, 2, 4 }, 2, PX),
      P("period", "period", { 0.10, 0.20, 0.40 }, 2, SEC),
    },
    build = function(p, ctx)
      local a = p.amp
      if ctx.onset then
        local d = ctx.transient / 3
        return { looping = ctx.pad and "REPEAT" or "NONE", anims = {
          { kind = "Translation", from = { 0, 0 }, to = { a, a }, duration = d },
          { kind = "Translation", from = { 0, 0 }, to = { -2 * a, -2 * a }, duration = d },
          { kind = "Translation", from = { 0, 0 }, to = { a, a }, duration = d,
            smoothing = "OUT", endDelay = ctx.pad },
        } }
      end
      return { looping = "BOUNCE", anims = {
        { kind = "Translation", from = { 0, 0 }, to = { a, a }, duration = p.period / 2 },
      } }
    end,
  },
}

-- State ------------------------------------------------------------------------

local panel, content, rows, textTicker, readTicker
local selected, tintIdx = 1, 1
local modeIdx, transIdx, decayIdx, autoIdx = 1, 1, 2, 1
local backdropIdx, targetIdx, motionIdx, sourceIdx = 1, 1, 1, 1
local abA, abB, abLive, abOn = nil, nil, "A", false
local paramIdx = {}                  -- treatment id -> { param key = value index }
local t0, formatter = 0, nil
local iconW, iconH, iconWhy = 40, 40, "not sampled"
local sec = { armed = false, why = "not armed yet", ids = {}, idx = 1 }

for _, tr in ipairs(TREATMENTS) do
  local d = {}
  for _, p in ipairs(tr.params) do d[p.key] = p.default end
  paramIdx[tr.id] = d
end

local function paramsOf(tr)
  local out, idx = {}, paramIdx[tr.id]
  for _, p in ipairs(tr.params) do out[p.key] = p.values[idx[p.key]] end
  return out
end

local function backdrop() return BACKDROPS[backdropIdx] end
local function onsetMode() return MODES[modeIdx] == "onset" end
local function cellH() return backdrop() == "icon" and math.max(26, iconH) or 26 end
local function rowH() return cellH() + 8 end

-- The secret model, asked of a widget ------------------------------------------

-- Three failures are kept apart because they mean different things: `x` the method does
-- not exist on this build, `!` it threw, `s` the ANSWER is itself secret — reachable,
-- since IsAnchoringSecret carries SecretReturnsForAspect — and may not be branched on.
local function ask(obj, method, arg)
  if not obj then return "?" end
  local m = obj[method]
  if type(m) ~= "function" then return "x" end
  local ok, v = pcall(m, obj, arg)
  if not ok then return "!" end
  if v == nil then return "?" end
  if ns.IsSecret(v) then return "s" end
  return v and "+" or "-"
end

-- The secret feed ---------------------------------------------------------------

local function ensureFormatter()
  if formatter or not MakeSecondsFormatter then return formatter end
  local ok, f = pcall(MakeSecondsFormatter)
  if ok then formatter = f end
  return formatter
end

local function spellName(id)
  if not (GetSpellName and id) then return nil end
  local ok, n = pcall(GetSpellName, id)
  return (ok and type(n) == "string") and n or nil
end

local function durationOf(spellID)
  if not GetCooldownDuration then return nil, "GetSpellCooldownDuration absent" end
  local ok, dur = pcall(GetCooldownDuration, spellID, SOURCES[sourceIdx].ignoreGCD)
  if not ok then return nil, "GetSpellCooldownDuration errored" end
  if dur == nil then return nil, "returned nothing" end
  local okH, hs = pcall(function() return dur:HasSecretValues() end)
  if not okH then return nil, "HasSecretValues errored" end
  if ns.IsSecret(hs) then return nil, "HasSecretValues read secret" end
  if not hs then return nil, "carries no secret here" end
  return dur
end

local function eachBinding(f)
  for _, row in ipairs(rows or {}) do
    local cell = row.cells.binding
    if cell.binding then f(cell.binding) end
    if cell.binding2 then f(cell.binding2) end
  end
end

local function disarm(why)
  sec.armed, sec.dur, sec.why = false, nil, why
  eachBinding(function(b) pcall(function() b:Disable() end) end)
end

--- Longest base cooldown first. The only place a cooldown LENGTH is readable is out of
--- combat, where nothing is secret yet. Falls back to the tracked order and says so.
local function orderSpells(ids)
  if InCombatLockdown() then return ids, "tracked order (ordered out of combat only)" end
  local keyed, source = {}, nil
  for _, id in ipairs(ids) do
    local base = 0
    if GetBaseCooldown then
      local ok, ms = pcall(GetBaseCooldown, id)
      if ok and type(ms) == "number" and ms > 0 then base, source = ms, "GetSpellBaseCooldown" end
    end
    if base == 0 and GetCooldownDuration and REALTIME ~= nil then
      local ok, dur = pcall(GetCooldownDuration, id, true)
      if ok and dur then
        local okT, total = pcall(function() return dur:GetTotalDuration(REALTIME) end)
        if okT and type(total) == "number" and total > 0 then
          base, source = total, source or "GetTotalDuration"
        end
      end
    end
    keyed[#keyed + 1] = { id = id, base = base }
  end
  if not source then return ids, "|cffff8844no base cooldown readable|r — tracked order" end
  table.sort(keyed, function(a, b)
    if a.base ~= b.base then return a.base > b.base end
    return a.id < b.id
  end)
  local out = {}
  for i, e in ipairs(keyed) do out[i] = e.id end
  return out, "longest base cooldown first, via " .. source
end

local function refreshIDs()
  local ids = (ns.TrackedSpellIDs and ns.TrackedSpellIDs()) or {}
  -- Ordered once, out of combat; a combat re-arm keeps the order it was given.
  if not InCombatLockdown() or #sec.ids == 0 then
    sec.ids, sec.order = orderSpells(ids)
  end
  if sec.idx > #sec.ids then sec.idx = 1 end
end

local function armSecret()
  refreshIDs()
  if not (GetCooldownDuration and REALTIME ~= nil and ensureFormatter()) then
    disarm("the secret-text recipe is not available on this build")
    return false
  end
  local sv, why = ns.GetSecret()
  if sv == nil then disarm(why or "no secret obtainable here") return false end
  if #sec.ids == 0 then
    disarm("no tracked Cooldown Manager spells — is the Cooldown Manager on?")
    return false
  end
  local id = sec.ids[sec.idx]
  local dur, durWhy = durationOf(id)
  if not dur then disarm(("spell %d: %s"):format(id, tostring(durWhy))) return false end
  sec.dur, sec.spellID, sec.armed, sec.why = dur, id, true, "armed"
  -- ⚠ NOT pcall'd into silence. A binding that never received a duration, or never got
  -- enabled, draws nothing — which is exactly what a working-but-zero binding looks like.
  sec.bindWhy = nil
  eachBinding(function(b)
    local good, err = call(b, "SetDuration", dur)
    if not good then sec.bindWhy = "SetDuration: " .. tostring(err) end
    good, err = call(b, "Enable")
    if not good then
      local okSet, err2 = call(b, "SetEnabled", true)
      if not okSet then
        sec.bindWhy = ("Enable: %s / SetEnabled: %s"):format(tostring(err), tostring(err2))
      end
    end
  end)
  return true
end

-- The formatted string goes straight to SetText and is never concatenated, compared or
-- printed. A gate that has gone away disarms rather than writing the plain string the
-- same call hands back out of combat.
local function feedSecret()
  if not sec.armed then return end
  local okH, hs = pcall(function() return sec.dur:HasSecretValues() end)
  if not okH or ns.IsSecret(hs) or not hs then
    disarm("the duration stopped carrying a secret")
    return
  end
  local ok, s = pcall(function() return sec.dur:FormatRemainingDuration(formatter, REALTIME) end)
  if not ok then
    disarm("FormatRemainingDuration errored: " .. tostring(s))
    return
  end
  for _, row in ipairs(rows) do
    local cell = row.cells.settext
    pcall(cell.fs.SetText, cell.fs, s)
    if cell.fs2:IsShown() then pcall(cell.fs2.SetText, cell.fs2, s) end
  end
end

local function feedPlain()
  local txt = ("%.1f"):format(20 - ((GetTime() - t0) % 20))
  for _, row in ipairs(rows) do
    local cell = row.cells.plain
    cell.fs:SetText(txt)
    if cell.fs2:IsShown() then cell.fs2:SetText(txt) end
  end
end

-- Cells and rows -----------------------------------------------------------------

-- ⚠ THE ISOLATION. Every leaf counts the Lua text writes made through it, from ANY
-- caller, so "this string has never had SetText called on it" is a recorded fact rather
-- than an argument from reading our own code. The binding column's leaves are the ones
-- that matter: a C-side write does not pass through here, so `w-` on a column that is
-- visibly rendering is the isolated case.
local WRITERS = { "SetText", "SetFormattedText", "SetTextToFit" }

local function sealLeaf(fs)
  if not pcall(function() fs.written = 0 end) then return false end
  for _, name in ipairs(WRITERS) do
    local orig = fs[name]
    if type(orig) == "function" then
      local set = pcall(function()
        fs[name] = function(self, ...)
          fs.written = fs.written + 1
          return orig(self, ...)
        end
      end)
      if not set then return false end
    end
  end
  return true
end

local function makeCell(parent, x)
  local cell = {}
  local holder = CreateFrame("Frame", nil, parent)
  holder:SetPoint("LEFT", parent, "LEFT", x, 0)
  holder:SetSize(COL_W, cellH())

  -- Two tones, not one: a billboard isolates text from a VARYING background, and over a
  -- flat panel colour it would have nothing to isolate against and would test nothing.
  cell.bands = {}
  for i, tone in ipairs({ { 0.30, 0.29, 0.27 }, { 0.04, 0.04, 0.05 } }) do
    local band = holder:CreateTexture(nil, "BACKGROUND")
    band:SetPoint("TOPLEFT", holder, "TOPLEFT", (i - 1) * COL_W / 2, 0)
    band:SetColorTexture(tone[1], tone[2], tone[3], 1)
    cell.bands[i] = band
  end

  -- ONE animatable backdrop region wearing three dresses: the real spell icon at real
  -- Cooldown Manager size, an opaque billboard, or nothing.
  cell.plate = holder:CreateTexture(nil, "BORDER")
  cell.plate:SetPoint("CENTER", holder, "CENTER", 0, 0)
  cell.plate:Hide()

  -- The canary. A SIBLING on the common holder, never a dependent of the string: it
  -- reads clean while the leaf rule holds, and reports the moment poison escapes it.
  cell.probe = holder:CreateTexture(nil, "ARTWORK")
  cell.probe:SetPoint("BOTTOMLEFT", holder, "BOTTOMLEFT", 2, 2)
  cell.probe:SetSize(5, 5)
  cell.probe:SetColorTexture(0.35, 0.35, 0.45, 1)

  -- CENTER, always. A secret-fed FontString stops being measurable, so a symmetric
  -- anchor is the only one a scale or offset treatment can work from.
  cell.sealed = true
  local function leaf()
    local fs = holder:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    fs:SetPoint("CENTER", holder, "CENTER", 0, 0)
    fs:SetJustifyH("CENTER")
    if not sealLeaf(fs) then cell.sealed = false end
    return fs
  end
  cell.holder, cell.fs, cell.fs2 = holder, leaf(), leaf()
  cell.fs2:Hide()

  local okF, path, size = pcall(cell.fs.GetFont, cell.fs)
  if okF and type(path) == "string" then cell.font, cell.size = path, size end
  return cell
end

-- Every method the generated docs give DurationTextBinding. Probed on the first binding
-- created and reported on the capability line: which of these the object really carries
-- is a Tier 1 fact the KB does not have.
local BINDING_METHODS = {
  "SetFontString", "SetDuration", "SetFormatter", "SetTextFormat", "SetTimeModifier",
  "SetUpdateInterval", "SetExpiredText", "SetZeroDurationText", "Enable", "Disable",
  "SetEnabled", "IsEnabled", "CanFormatText", "CanUpdateFontString", "GetFormattedText",
  "UpdateFontString", "HasSecretValues", "GetDuration", "GetFontString",
}
local bindingReport

local function describeBinding(b)
  local miss = {}
  for _, name in ipairs(BINDING_METHODS) do
    if type(b[name]) ~= "function" then miss[#miss + 1] = name end
  end
  return ("binding: %d/%d documented methods present%s"):format(
    #BINDING_METHODS - #miss, #BINDING_METHODS,
    #miss > 0 and (" — |cffff8844ABSENT: " .. table.concat(miss, ", ") .. "|r") or "")
end

--@unverified the install order below is composed from the generated docs. Every step
-- reports its own failure instead of being swallowed, so a blank column names a cause
-- rather than looking like "the binding route fails".
local function bindingFor(fs)
  if not MakeTextBinding then return nil, "CreateDurationTextBinding absent" end
  local ok, b = pcall(MakeTextBinding)
  if not ok or not b then return nil, "CreateDurationTextBinding failed" end
  bindingReport = bindingReport or describeBinding(b)
  local good, why = call(b, "SetFontString", fs)
  if not good then return nil, "SetFontString: " .. tostring(why) end
  if ensureFormatter() then
    good, why = call(b, "SetFormatter", formatter)
    if not good then return nil, "SetFormatter: " .. tostring(why) end
  end
  if REALTIME ~= nil then call(b, "SetTimeModifier", REALTIME) end
  call(b, "SetUpdateInterval", 0.1)
  -- Expired, zero and "nothing installed" must be three different sets of pixels, or a
  -- broken column reads as a working one.
  call(b, "SetExpiredText", "--")
  call(b, "SetZeroDurationText", "0")
  return b
end

-- Building the animation ----------------------------------------------------------

--@unverified CreateAnimationGroup and CreateAnimation are SecretArguments = NotAllowed,
-- which constrains their ARGUMENTS and not their target, so animating a FontString that
-- has been fed a secret SHOULD be legal. The middle column is exactly that case and the
-- `a` readout is where a refusal would appear.
local function groupFor(cell, key)
  cell.groups = cell.groups or {}
  if cell.groups[key] then return cell.groups[key] end
  local obj = cell.fs
  if key == "plate" then obj = cell.plate elseif key == "text2" then obj = cell.fs2 end
  local ok, g = pcall(function() return obj:CreateAnimationGroup() end)
  if not ok or not g then return nil, key .. ": no AnimationGroup" end
  cell.groups[key] = g
  return g
end

-- Stepping the motion is the contested jerky-onset question, and the animation system
-- interpolates smoothly by construction — so a step is a short hold, and a descriptor
-- becomes N of them. Above the cap the row runs smooth and SAYS it did.
local MAX_STEPS = 20

local function stepped(anims)
  local hz = MOTION[motionIdx].hz
  if not hz then return anims, false end
  local out, capped = {}, false
  for _, d in ipairs(anims) do
    local n = math.floor(d.duration * hz + 0.5)
    -- Translation is excluded because its offset is a DELTA, not a position: a hold
    -- would have nothing to hold and the whole move would vanish.
    if n < 2 or n > MAX_STEPS or d.kind == "Translation" then
      out[#out + 1] = d
      capped = capped or n > MAX_STEPS
    else
      for i = 0, n - 1 do
        local u, v = (n > 1) and i / (n - 1) or 1, {}
        for k = 1, #d.from do v[k] = d.from[k] + (d.to[k] - d.from[k]) * u end
        out[#out + 1] = { kind = d.kind, from = v, to = v, duration = d.duration / n,
                          endDelay = (i == n - 1) and d.endDelay or nil }
      end
    end
  end
  return out, capped
end

local function addAnim(group, d, order)
  local ok, anim = pcall(function() return group:CreateAnimation(d.kind) end)
  if not ok or not anim then return false, d.kind .. ": CreateAnimation failed" end
  local good, why = call(anim, "SetDuration", d.duration)
  if not good then return false, why end
  call(anim, "SetOrder", math.min(order, 100))
  call(anim, "SetSmoothing", d.smoothing or "NONE")
  if d.endDelay and d.endDelay > 0 then call(anim, "SetEndDelay", d.endDelay) end
  local setter = SETTERS[d.kind]
  if not setter then return false, d.kind .. ": no setter mapping" end
  return setter(anim, d)
end

local function ctxOf()
  local auto = AUTOFIRE[autoIdx].secs
  local trans, decay = TRANSIENTS[transIdx].secs, DECAYS[decayIdx].secs
  return { onset = onsetMode(), transient = trans, decay = decay,
           pad = auto and math.max(0.01, auto - trans - decay) or nil }
end

local function stopGroups(cell)
  for _, g in pairs(cell.groups or {}) do
    pcall(function() g:Stop() end)
    pcall(function() g:RemoveAnimations() end)
  end
  cell.playing = {}
end

local function buildSpec(cell, spec, order)
  local key = spec.target or ((TARGETS[targetIdx] == "plate" and backdrop() ~= "none")
    and "plate" or "text")
  cell.animTarget = cell.animTarget or key
  local group, why = groupFor(cell, key)
  if not group then
    -- Whether FontString really is an AnimatableObject rests on Tier 2 alone, so this is
    -- a measurement rather than a dead row: name it instead of drawing nothing.
    cell.animNote = why
    return
  end
  local anims, capped = stepped(spec.anims)
  if capped then cell.animNote = "too many steps — running smooth" end
  for i, d in ipairs(anims) do
    local ok, err = addAnim(group, d, order + i)
    if not ok then
      cell.animNote = err
      return
    end
  end
  call(group, "SetLooping", spec.looping or "NONE")
  if spec.finalAlpha then call(group, "SetToFinalAlpha", true) end
  cell.playing[#cell.playing + 1] = group
  call(group, "Play")
end

--- Rebuild one cell's animation. A treatment may return one spec or several — the
--- weight cross-fade needs two, one per leaf.
local function rebuildAnim(cell, tr, p)
  cell.animNote, cell.animTarget = nil, nil
  if not tr.build then return end
  local specs = tr.build(p, ctxOf())
  if specs.anims then specs = { specs } end
  for i, spec in ipairs(specs) do buildSpec(cell, spec, (i - 1) * 10) end
end

local function dressBackdrop(cell)
  local mode = backdrop()
  cell.backdrop = mode
  if mode == "icon" then
    cell.plate:SetSize(iconW, iconH)
    if cell.icon then cell.plate:SetTexture(cell.icon) else cell.plate:SetColorTexture(0.15, 0.13, 0.10, 1) end
    cell.plate:Show()
  elseif mode == "plate" then
    cell.plate:SetSize(COL_W - 6, cellH() - 6)
    cell.plate:SetColorTexture(0.03, 0.03, 0.04, 0.96)
    cell.plate:Show()
  else
    cell.plate:Hide()
  end
end

local function resetCell(cell, tr, p)
  -- Groups stop FIRST: vertex colour is not restored when an animation ends, so a base
  -- colour written before the stop would be overwritten by wherever the animation was.
  stopGroups(cell)
  cell.fs:SetAlpha(1)
  call(cell.fs, "SetTextScale", 1)
  cell.fs:ClearAllPoints()
  cell.fs:SetPoint("CENTER", cell.holder, "CENTER", 0, 0)
  cell.fs:SetShadowOffset(0, 0)
  cell.fontOK = nil
  if cell.font then
    local ok, applied = pcall(cell.fs.SetFont, cell.fs, cell.font, cell.size, "")
    cell.fontOK = ok and (applied ~= false)
  end
  cell.fs2:SetAlpha(1)
  cell.fs2:Hide()
  cell.plate:SetAlpha(1)
  dressBackdrop(cell)
  -- SetTextColor and SetVertexColor are ONE storage slot on a FontString, so this file
  -- uses SetTextColor everywhere and never the region call.
  cell.fs:SetTextColor(hueOf(tintIdx))
  cell.fs2:SetTextColor(hueOf(tintIdx))
  cell.err = nil
  if tr.reset then
    local ok, err = pcall(tr.reset, cell, p)
    if not ok then cell.err = tostring(err) end
  end
  rebuildAnim(cell, tr, p)
end

-- A treatment that cannot even be set up is a finding, not a crash: the cell records it,
-- says so once in chat, and the rest carry on.
local function fail(row, key, cell, err)
  cell.err = tostring(err)
  ns.Printf("|cffff4040%s / %s:|r %s", row.tr.id, key, cell.err)
end

local function resetAll()
  for _, row in ipairs(rows or {}) do
    row.p = paramsOf(row.tr)
    for _, col in ipairs(COLUMNS) do
      local cell = row.cells[col.key]
      local ok, err = pcall(resetCell, cell, row.tr, row.p)
      if not ok then fail(row, col.key, cell, err) end
    end
  end
end

local function fireAll()
  for _, row in ipairs(rows or {}) do
    for _, col in ipairs(COLUMNS) do
      for _, g in ipairs(row.cells[col.key].playing or {}) do call(g, "Restart") end
    end
  end
end

-- Where a setting sits against the text standard. Returned as text so the row SAYS it
-- rather than the panel quietly refusing to offer the setting.
local function overLimit(row)
  local out = {}
  -- Onset mode does not flash at the steady period, so the rate flag does not apply.
  local hz = (not onsetMode()) and row.tr.rate and row.p[row.tr.rate]
    and (1 / row.p[row.tr.rate]) or nil
  if hz and hz > TEXT_MAX_HZ then out[#out + 1] = ("%.2gHz>%.2g"):format(hz, TEXT_MAX_HZ) end
  local floor = row.p.floor
  if floor and row.tr.id ~= "plate" and floor < TEXT_ALPHA_FLOOR then
    out[#out + 1] = ("floor %d%%"):format(math.floor(floor * 100 + 0.5))
  end
  return #out > 0 and ("  |cffff8844" .. table.concat(out, " ") .. "|r") or ""
end

-- The readout is the point of the panel. `s` is IsAnchoringSecret then
-- HasSecretAspect(Text) per column; `p` is the sibling canary; `a` names the animation
-- target then IsPlaying per column; `b` is the binding's three diagnostics plus THE
-- ISOLATION — whether any Lua SetText has ever touched that string.
local function readRow(row)
  local str, probes, anims, holderDirty, note = {}, {}, {}, false, nil
  for i, col in ipairs(COLUMNS) do
    local cell = row.cells[col.key]
    -- ⚠ AN UNINSTALLED BINDING MUST NOT BORROW THE OTHER ROUTE'S READING. This column's
    -- FontString exists whether or not a binding was attached, so reporting its aspects
    -- would attribute to the binding route a result the binding never produced.
    if col.key == "binding" and not cell.binding then
      str[i], probes[i], anims[i] = "xx", "x", "x"
      note = note or cell.bindNote or "no binding installed"
    else
      str[i] = ask(cell.fs, "IsAnchoringSecret") .. ask(cell.fs, "HasSecretAspect", ASPECT_TEXT)
      if cell.fs2:IsShown() then
        str[i] = str[i] .. "/" .. ask(cell.fs2, "IsAnchoringSecret")
      end
      probes[i] = ask(cell.probe, "IsAnchoringSecret")
      if not row.tr.build then anims[i] = "."
      elseif cell.animNote then anims[i] = "!"
      else anims[i] = ask(cell.playing and cell.playing[1], "IsPlaying") end
      if ask(cell.holder, "IsAnchoringSecret") ~= "-" then holderDirty = true end
      note = note or cell.animNote or (cell.fontOK == false and "SetFont refused" or nil)
    end
    if cell.err then note = cell.err end
  end
  local bcell = row.cells.binding
  -- An UNSEALED leaf reads `?`, never `-`: a seal that did not take would otherwise
  -- report "never written" for a string nobody was watching, which is a false isolation.
  local seen = (not bcell.sealed) and "?" or (((bcell.fs.written or 0) > 0) and "W" or "-")
  local diag = bcell.binding
    and (ask(bcell.binding, "CanFormatText") .. ask(bcell.binding, "CanUpdateFontString")
         .. ask(bcell.binding, "IsEnabled") .. seen)
    or "xxxx"
  row.read:SetText(("|cff808080s|r %s %s %s  |cff808080p|r%s%s%s  |cff808080a·%s|r"
    .. "%s%s%s  |cff808080b|r%s%s%s%s")
    :format(str[1], str[2], str[3], probes[1], probes[2], probes[3],
      (not row.tr.build) and "-" or ((row.cells.plain.animTarget == "plate") and "p" or "g"),
      anims[1], anims[2], anims[3], diag,
      holderDirty and "  |cffff4040HOLDER|r" or "",
      note and ("  |cffff4040" .. note .. "|r") or "", overLimit(row)))
end

-- Two tickers, and nothing else. Text content and the readout are Lua's whole remaining
-- job here; every pixel that moves is moved by the animation system.
local function textTick()
  if not (panel and panel:IsShown()) then return end
  feedPlain()
  feedSecret()
end

local function readTick()
  if not (panel and panel:IsShown()) then return end
  if InCombatLockdown() then
    if not sec.armed then armSecret() end
  elseif sec.armed then
    disarm("combat ended — out of combat the same call returns a plain string")
  end
  for _, row in ipairs(rows) do readRow(row) end
  C.Caption()
end

-- UI ------------------------------------------------------------------------------

local function pickRow(root, label, names, y, get, set, x0)
  x0 = x0 or 10
  local fs = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  fs:SetPoint("TOPLEFT", root, "TOPLEFT", x0, y - 2)
  fs:SetText(label)
  local out, x = {}, x0 + 46
  for i, name in ipairs(names) do
    local b = ns.UI.button(root, name, 8 * #name + 22, 20, function()
      if get() ~= i then set(i) end
    end)
    b:SetPoint("TOPLEFT", root, "TOPLEFT", x, y)
    x = x + 8 * #name + 26
    out[i] = b
  end
  return out
end

local function markRow(buttons, idx, names)
  for i, b in ipairs(buttons or {}) do
    b.text:SetText(i == idx and ("|cffffd100" .. names[i] .. "|r") or names[i])
  end
end

local function namesOf(list)
  local out = {}
  for i, v in ipairs(list) do out[i] = type(v) == "table" and v.name or tostring(v) end
  return out
end

local MAX_PARAMS = 6

-- ⚠ THE STEPPER HANDLERS ARE REBOUND ON EVERY SELECTION. These rows are pooled across
-- every treatment, so a handler installed at creation would keep the FIRST treatment's
-- param in its closure and step the wrong number forever (Ask.lua's trap).
local function refreshParams()
  local tr = TREATMENTS[selected]
  for i = 1, MAX_PARAMS do
    local w = panel.paramRows[i]
    local p = tr.params[i]
    if not p then
      w.frame:Hide()
    else
      local idx = paramIdx[tr.id]
      local function step(d)
        idx[p.key] = ((idx[p.key] - 1 + d) % #p.values) + 1
        resetAll()
        refreshParams()
      end
      w.frame:Show()
      w.label:SetText(p.label)
      w.value:SetText((p.render or AS_IS)(p.values[idx[p.key]]))
      w.prev:SetScript("OnClick", function() step(-1) end)
      w.next:SetScript("OnClick", function() step(1) end)
    end
  end
end

--- Row geometry, recomputed whenever the backdrop changes the cell height.
local function layoutRows()
  local h, ch = rowH(), cellH()
  local live = abOn and ((abLive == "A") and abA or abB) or nil
  for i, row in ipairs(rows) do
    row:ClearAllPoints()
    local y = (live and i == live) and 0 or -(i - 1) * h
    row:SetPoint("TOPLEFT", content, "TOPLEFT", 0, y)
    row:SetPoint("TOPRIGHT", content, "TOPRIGHT", 0, y)
    row:SetHeight(h - 4)
    for _, col in ipairs(COLUMNS) do
      local cell = row.cells[col.key]
      cell.holder:SetSize(COL_W, ch)
      for _, band in ipairs(cell.bands) do band:SetSize(COL_W / 2, ch) end
    end
  end
  content:SetHeight(math.max(SCROLL_H, #rows * h + 4))
end

-- Within-session A/B, because between-session judgement is sabotaged twice over:
-- dishabituation makes anything new feel better on first sight, and a cue matching a
-- learned template captures better than an objectively stronger unfamiliar one. So the
-- live row is moved to a fixed position and its NAME is withheld while toggling.
local function applyAB()
  local live = abOn and ((abLive == "A") and abA or abB) or nil
  for i, row in ipairs(rows) do
    if live then
      -- Show/Hide, never SetShown: SetShown is IsProtectedFunction and this panel is
      -- meant to be driven mid-pull.
      row.label:SetText(i == live and ("   |cffffd100" .. abLive .. "|r") or "")
      if i == live then row:Show() else row:Hide() end
    else
      row.label:SetText(("%d %s"):format(i, TREATMENTS[i].label))
      row:Show()
    end
  end
  layoutRows()
end

local function selectRow(i)
  selected = i
  for j, row in ipairs(rows) do
    if j == i and not abOn then row.sel:Show() else row.sel:Hide() end
  end
  local tr = TREATMENTS[i]
  local live = tr.liveNote and ("   |cffffffff" .. tr.liveNote(paramsOf(tr)) .. "|r") or ""
  panel.selCaption:SetText(abOn and "|cffffd100A/B running|r — the name is withheld on "
      .. "purpose; press [swap] and judge, then [show all] to see which is which."
    or (("|cffffd100%s|r — %s"):format(tr.label, tr.note or "") .. live))
  refreshParams()
end

function C.Caption()
  if not panel then return end
  local state
  if sec.armed then
    state = ("|cff66ddaaSECRET LIVE|r — %s (%s) via %s%s")
      :format(spellName(sec.spellID) or "?", tostring(sec.spellID), SOURCES[sourceIdx].name,
        sec.bindWhy and ("  |cffff4040binding " .. sec.bindWhy .. "|r") or "")
  else
    state = ("|cffff8844not secret yet|r — %s"):format(tostring(sec.why))
  end
  -- The isolation's positive control: the SetText column must read written, or the seal
  -- is not catching writes and the binding column's `-` proves nothing.
  local ctrl = rows and rows[1] and ((rows[1].cells.settext.fs.written or 0) > 0)
  panel.state:SetText(("%s   |cff808080spell %d/%d, %s · UIParent %s · A/B %s · seal %s|r")
    :format(state, #sec.ids > 0 and sec.idx or 0, #sec.ids, tostring(sec.order or "unordered"),
      ask(UIParent, "IsAnchoringSecret"),
      abOn and ("live " .. abLive) or (abA and abB and "armed, not running" or "unset"),
      ctrl and "control WRITTEN" or "|cffff8844control silent|r"))
  markRow(panel.tintButtons, tintIdx, namesOf(COLOURS))
  markRow(panel.modeButtons, modeIdx, MODES)
  markRow(panel.transButtons, transIdx, namesOf(TRANSIENTS))
  markRow(panel.decayButtons, decayIdx, namesOf(DECAYS))
  markRow(panel.autoButtons, autoIdx, namesOf(AUTOFIRE))
  markRow(panel.motionButtons, motionIdx, namesOf(MOTION))
  markRow(panel.backdropButtons, backdropIdx, BACKDROPS)
  markRow(panel.targetButtons, targetIdx, TARGETS)
  markRow(panel.sourceButtons, sourceIdx, namesOf(SOURCES))
  panel.grey.text:SetText(greyOn and "|cffffd100[x] greyscale|r" or "[ ] greyscale")
end

-- The icon behind the text is the icon of the spell the secret columns are feeding from,
-- so the header and the art can never disagree. GetSpellTexture hands back a fileID or a
-- path; SetTexture takes either.
local function refreshIcon()
  local path
  if GetSpellTexture and sec.spellID then
    local ok, p = pcall(GetSpellTexture, sec.spellID)
    if ok and (type(p) == "string" or type(p) == "number") then path = p end
  end
  for _, row in ipairs(rows or {}) do
    for _, col in ipairs(COLUMNS) do row.cells[col.key].icon = path end
  end
end

local function controlChanged()
  refreshIcon()
  resetAll()
  layoutRows()
  C.Caption()
end

local function buildRows(parent)
  local out = {}
  for i, tr in ipairs(TREATMENTS) do
    local row = CreateFrame("Button", nil, parent)

    row.sel = row:CreateTexture(nil, "BACKGROUND")
    row.sel:SetAllPoints(row)
    row.sel:SetColorTexture(0.20, 0.22, 0.32, 0.9)
    row.sel:Hide()

    row.label = row:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    row.label:SetPoint("LEFT", row, "LEFT", 2, 0)
    row.label:SetWidth(LABEL_W)
    row.label:SetJustifyH("LEFT")
    row.label:SetText(("%d %s"):format(i, tr.label))

    row.cells = {}
    for _, col in ipairs(COLUMNS) do row.cells[col.key] = makeCell(row, col.x) end
    local bcell = row.cells.binding
    bcell.binding, bcell.bindNote = bindingFor(bcell.fs)
    bcell.binding2 = bindingFor(bcell.fs2)

    row.read = row:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
    row.read:SetPoint("LEFT", row, "LEFT", READOUT_X, 0)
    row.read:SetPoint("RIGHT", row, "RIGHT", -2, 0)
    row.read:SetJustifyH("LEFT")
    row.read:SetWordWrap(false)

    row.tr = tr
    row:SetScript("OnClick", function() selectRow(i) end)
    out[i] = row
  end
  return out
end

-- Two steppers per line, so six parameters cost three lines rather than six.
local function buildParamRows(root)
  local out = {}
  for i = 1, MAX_PARAMS do
    local col = (i - 1) % 2
    local f = CreateFrame("Frame", nil, root)
    f:SetPoint("TOPLEFT", root, "TOPLEFT", 10 + col * 370,
      Y_PARAMS - math.floor((i - 1) / 2) * 26)
    f:SetSize(350, 22)
    local label = f:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
    label:SetPoint("LEFT", f, "LEFT", 0, 0)
    label:SetWidth(78)
    label:SetJustifyH("LEFT")
    local prev = ns.UI.button(f, "<", 20, 20, nil)
    prev:SetPoint("LEFT", f, "LEFT", 78, 0)
    local value = f:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    value:SetPoint("LEFT", f, "LEFT", 102, 0)
    value:SetWidth(110)
    value:SetJustifyH("CENTER")
    local nxt = ns.UI.button(f, ">", 20, 20, nil)
    nxt:SetPoint("LEFT", f, "LEFT", 214, 0)
    f:Hide()
    out[i] = { frame = f, label = label, value = value, prev = prev, next = nxt }
  end
  return out
end

local function buildControls(root)
  local UI = ns.UI
  root.tintButtons = pickRow(root, "tint", namesOf(COLOURS), Y_CTRL,
    function() return tintIdx end, function(i) tintIdx = i; controlChanged() end)
  root.grey = UI.button(root, "[ ] greyscale", 94, 20, function()
    greyOn = not greyOn
    controlChanged()
  end)
  root.grey:SetPoint("TOPLEFT", root, "TOPLEFT", 636, Y_CTRL)

  root.modeButtons = pickRow(root, "mode", MODES, Y_CTRL - 26,
    function() return modeIdx end, function(i) modeIdx = i; controlChanged() end)
  root.transButtons = pickRow(root, "transient", namesOf(TRANSIENTS), Y_CTRL - 26,
    function() return transIdx end, function(i) transIdx = i; controlChanged() end, 210)
  root.decayButtons = pickRow(root, "decay", namesOf(DECAYS), Y_CTRL - 26,
    function() return decayIdx end, function(i) decayIdx = i; controlChanged() end, 400)

  root.autoButtons = pickRow(root, "auto", namesOf(AUTOFIRE), Y_CTRL - 52,
    function() return autoIdx end, function(i) autoIdx = i; controlChanged() end)
  UI.button(root, "fire", 60, 20, fireAll)
      :SetPoint("TOPLEFT", root, "TOPLEFT", 250, Y_CTRL - 52)
  root.motionButtons = pickRow(root, "motion", namesOf(MOTION), Y_CTRL - 52,
    function() return motionIdx end, function(i) motionIdx = i; controlChanged() end, 330)

  root.backdropButtons = pickRow(root, "backdrop", BACKDROPS, Y_CTRL - 78,
    function() return backdropIdx end, function(i) backdropIdx = i; controlChanged() end)
  root.targetButtons = pickRow(root, "target", TARGETS, Y_CTRL - 78,
    function() return targetIdx end, function(i) targetIdx = i; controlChanged() end, 250)
  root.sourceButtons = pickRow(root, "source", namesOf(SOURCES), Y_CTRL - 78,
    function() return sourceIdx end,
    function(i) sourceIdx = i; disarm("source changed"); armSecret(); controlChanged() end, 450)

  UI.button(root, "set A", 70, 20, function()
    abA = selected
    C.Caption()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 10, Y_CTRL - 104)
  UI.button(root, "set B", 70, 20, function()
    abB = selected
    C.Caption()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 84, Y_CTRL - 104)
  UI.button(root, "swap", 54, 20, function()
    if not (abA and abB) then
      ns.Print("set A and set B first — select a row, press [set A], select another, press [set B].")
      return
    end
    if abOn then abLive = (abLive == "A") and "B" or "A" else abOn = true end
    applyAB()
    selectRow(selected)
    C.Caption()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 158, Y_CTRL - 104)
  UI.button(root, "show all", 86, 20, function()
    abOn = false
    applyAB()
    selectRow(selected)
    C.Caption()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 216, Y_CTRL - 104)

  UI.button(root, "< spell", 60, 20, function()
    if #sec.ids > 0 then sec.idx = ((sec.idx - 2) % #sec.ids) + 1 end
    disarm("stepping the source spell")
    armSecret()
    controlChanged()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 400, Y_CTRL - 104)
  UI.button(root, "spell >", 60, 20, function()
    if #sec.ids > 0 then sec.idx = (sec.idx % #sec.ids) + 1 end
    disarm("stepping the source spell")
    armSecret()
    controlChanged()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 466, Y_CTRL - 104)
  UI.button(root, "re-arm", 60, 20, function()
    if armSecret() then
      ns.Printf("armed on spell %s — the middle and right columns are a genuine secret now.",
        tostring(sec.spellID))
    else
      ns.Printf("could not arm: %s", tostring(sec.why))
    end
    controlChanged()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 532, Y_CTRL - 104)
end

--- A real Cooldown Manager item frame's size, read out of combat, so a mocked-up cue is
--- the size it will actually sit on rather than a guess. Shared, so there is one answer.
function ns.CDMItemSize()
  for _, name in ipairs(VIEWERS) do
    local viewer = ns.G(name)
    if viewer then
      local ok, list = pcall(viewer.GetItemFrames, viewer)
      if ok and type(list) == "table" and not ns.IsSecretTable(list) then
        for _, f in ipairs(list) do
          local okS, w, h = pcall(f.GetSize, f)
          if okS and type(w) == "number" and w > 8 then
            return math.floor(w + 0.5), math.floor(h + 0.5), "read off a live item frame"
          end
        end
      end
    end
  end
  return 40, 40, "|cffff8844no item frame readable — assumed 40 px|r"
end

local function capsLine()
  local missing = {}
  for _, cap in ipairs(CAPS) do
    if cap[2] == nil then missing[#missing + 1] = cap[1] end
  end
  -- GetFonts is reported, not wired: it returns font NAMES and SetFont takes a font
  -- ASSET path, and whether those are the same namespace is unverified here.
  local fonts = "GetFonts absent"
  if EnumFonts then
    local ok, list = pcall(EnumFonts)
    fonts = (ok and type(list) == "table")
      and ("GetFonts: %d entr(ies), first is a %s"):format(#list, type(list[1]))
      or "GetFonts returned nothing usable"
  end
  return (#missing == 0
    and "|cff808080every probed global resolved.|r  "
    or ("|cffff8844absent on this build:|r " .. table.concat(missing, ", ") .. "  "))
    .. ("|cff808080%s · %s · icon %dx%d, %s|r"):format(
      fonts, bindingReport or "no binding created", iconW, iconH, iconWhy)
end

local function build()
  local UI = ns.UI
  local root = CreateFrame("Frame", nil, UIParent)
  root:SetSize(PANEL_W, PANEL_H)
  root:SetFrameStrata("DIALOG")
  root:SetMovable(true)
  root:EnableMouse(true)
  root:RegisterForDrag("LeftButton")
  root:SetScript("OnDragStart", root.StartMoving)
  root:SetScript("OnDragStop", root.StopMovingOrSizing)

  local bg = root:CreateTexture(nil, "BACKGROUND")
  bg:SetAllPoints(root)
  bg:SetColorTexture(0.08, 0.08, 0.10, 0.96)
  UI.edge(root, 0.45, 0.45, 0.55, 0.9)

  local title = root:CreateFontString(nil, "OVERLAY", "GameFontNormal")
  title:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -10)
  title:SetText("ClientLab — cue treatments")

  UI.button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  local function line(font, y, height)
    local fs = root:CreateFontString(nil, "OVERLAY", font)
    fs:SetPoint("TOPLEFT", root, "TOPLEFT", 10, y)
    fs:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, y)
    fs:SetJustifyH("LEFT")
    fs:SetWordWrap(true)
    if height then fs:SetHeight(height) end
    return fs
  end
  root.state = line("GameFontHighlightSmall", -32)
  root.caps = line("GameFontDisableSmall", -50, 18)

  for _, col in ipairs(COLUMNS) do
    local cap = root:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    cap:SetPoint("TOPLEFT", root, "TOPLEFT", 10 + col.x, -70)
    cap:SetWidth(COL_W)
    cap:SetJustifyH("CENTER")
    cap:SetText(col.caption)
  end
  local readCap = root:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  readCap:SetPoint("TOPLEFT", root, "TOPLEFT", 10 + READOUT_X, -70)
  readCap:SetText("anchoring + animation readout")

  -- The rows scroll, so the panel keeps one height whatever the backdrop does to the
  -- row height and however many treatments there are.
  local scroll = CreateFrame("ScrollFrame", nil, root, "UIPanelScrollFrameTemplate")
  scroll:SetPoint("TOPLEFT", root, "TOPLEFT", 10, SCROLL_TOP)
  scroll:SetSize(PANEL_W - 46, SCROLL_H)
  content = CreateFrame("Frame", nil, scroll)
  content:SetSize(PANEL_W - 46, SCROLL_H)
  scroll:SetScrollChild(content)

  panel = root
  iconW, iconH, iconWhy = ns.CDMItemSize()
  rows = buildRows(content)
  -- After the rows, because the first binding created is what supplies its method list.
  root.caps:SetText(capsLine())

  root.legend = line("GameFontDisableSmall", Y_LEGEND, 34)
  root.legend:SetText("|cff808080s = IsAnchoringSecret then HasSecretAspect(Text) per "
    .. "column · p = the sibling canary on the common holder · a·g / a·p = the animation "
    .. "target, then IsPlaying per column · b = the binding's CanFormatText, "
    .. "CanUpdateFontString, IsEnabled, then |r|cffffffffW|r|cff808080 if any Lua SetText "
    .. "has ever touched that string and |r|cffffffff?|r|cff808080 if the seal did not "
    .. "take · |r|cffffffff+|r|cff808080 yes |r|cffffffff-|r"
    .. "|cff808080 no |r|cffffffffs|r|cff808080 the answer is itself secret |r"
    .. "|cffffffff!|r|cff808080 threw |r|cffffffffx|r|cff808080 absent · |r|cffff8844amber"
    .. "|r|cff808080 = outside the 2 Hz / 65 % text limits, reachable on purpose.|r")

  root.selCaption = line("GameFontHighlightSmall", Y_SEL, 32)

  buildControls(root)
  root.paramRows = buildParamRows(root)

  root.footer = line("GameFontDisableSmall", Y_FOOTER, 46)
  root.footer:SetText("|cff808080Motion is C-side: each treatment is a list of animation "
    .. "descriptors, so |r|cffffffffonset|r|cff808080 is a hold plus a decay at two orders "
    .. "and |r|cffffffffauto|r|cff808080 is an endDelay under REPEAT, with no Lua timer in "
    .. "either. |r|cffffffffsource GCD|r|cff808080 reads the global cooldown, which rolls "
    .. "on every cast — a ready ability's own cooldown is zero and renders nothing. The "
    .. "secret columns are fed only in combat.|r")

  root:SetScript("OnShow", function()
    t0 = GetTime()
    -- Out of combat here, normally — which is the only place the candidates can be
    -- ordered by cooldown length, or an item frame measured.
    refreshIDs()
    if not InCombatLockdown() then
      iconW, iconH, iconWhy = ns.CDMItemSize()
      root.caps:SetText(capsLine())
    end
    armSecret()
    refreshIcon()
    resetAll()
    applyAB()
    selectRow(selected)
    C.Caption()
    textTicker = textTicker or C_Timer.NewTicker(0.1, textTick)
    readTicker = readTicker or C_Timer.NewTicker(0.5, readTick)
  end)
  root:SetScript("OnHide", function()
    if textTicker then textTicker:Cancel(); textTicker = nil end
    if readTicker then readTicker:Cancel(); readTicker = nil end
    for _, row in ipairs(rows) do
      for _, col in ipairs(COLUMNS) do
        for _, g in ipairs(row.cells[col.key].playing or {}) do call(g, "Stop") end
      end
    end
    disarm("panel closed")
  end)
  root:Hide()
  return root
end

function C.Toggle()
  if InCombatLockdown() and not panel then
    ns.Print("can't build the cue panel in combat — open it once out of combat, then it "
      .. "stays usable mid-pull, which is the only time the secret columns are honest.")
    return
  end
  panel = panel or build()
  if panel:IsShown() then
    panel:Hide()
    return false
  end
  panel:ClearAllPoints()
  panel:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
  panel:Show()
  return true
end

ns.Dumps.Register{
  id = "cue",
  label = "cue treatments",
  blurb = function()
    if sec.armed then return ("%d treatments · secret live"):format(#TREATMENTS) end
    return ("%d treatments · %s"):format(#TREATMENTS, tostring(sec.why))
  end,
  capture = function()
    local shown = C.Toggle()
    if shown == nil then return { "refused — the cue panel cannot be built in combat" } end
    return { shown and "opened the cue panel — click a row to steer its parameters, [fire] "
                    .. "to trigger an onset; the secret columns arm about two seconds into a pull"
                   or "closed the cue panel" }
  end,
}

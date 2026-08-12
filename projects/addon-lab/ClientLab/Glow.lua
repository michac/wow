-- RETIRED FROM ClientLab.toc ON 12.1. This settled 12.0 design tool retains and
-- decorates live Cooldown Manager frames, which now participate in secure aura
-- plumbing. Keep this source only as historical design work.
--
-- Glow — a highlight picker. One candidate at a time on a sample square and on the
-- live Cooldown Manager, in cap's tier hues, stepped with next/prev.
--
-- A picker, not a test: it registers no ns.Test{} id, no questions.json row and no
-- capture stream. The output is a decision a person writes down.
--
-- INVARIANT: nothing in a product addon may depend on ClientLab. The glow that wins
-- here gets built into cap by embedding LibOrbitGlow there, not by reaching in here.

local ADDON, ns = ...

ns.Glow = {}
local G = ns.Glow

-- The `LibStub and` guard is a degradation path, not an existence probe: a load failure
-- at file scope would take this file down along with the fallback that reports it.
-- LibStub then hands back whichever copy of the library loaded first, so a standalone
-- install can win over the vendored one and be older than the facade this file drives.
-- Every library entry point the file calls is named in the gate; nothing below re-probes.
local lib = LibStub and LibStub("LibOrbitGlow-1.0", true)
local FACADE = { "Apply", "Hide", "GetGlowList", "GetGlowInfo", "Proc", "Flipbook" }
local ready = lib and lib.Apply and lib.Hide and lib.GetGlowList and lib.GetGlowInfo
    and lib.Proc and lib.Proc.Clear and lib.Flipbook and lib.Flipbook.Show and lib.Flipbook.Hide

if not ready then
  ns.Dumps.Register{
    id = "glow",
    label = "glow palette",
    blurb = function() return "LibOrbitGlow unavailable" end,
    capture = function()
      local out = { "LibOrbitGlow-1.0 did not resolve, or the copy that won LibStub is older",
                    "than the Apply / Hide / GetGlowList / GetGlowInfo / Proc.Clear /",
                    "Flipbook.Show / Flipbook.Hide facade this panel drives.",
                    "LibStub present: " .. tostring(LibStub ~= nil),
                    "library present: " .. tostring(lib ~= nil) }
      if lib then
        for _, fn in ipairs(FACADE) do
          out[#out + 1] = ("  lib.%s: %s"):format(fn, type(lib[fn]))
        end
      end
      return out
    end,
  }
  return
end

-- Published only past the facade gate above, so a consumer that finds it non-nil has a
-- library whose whole entry-point set resolved.
G.lib = lib

-- cap's tier treatment as DATA (Treatment.lua's TIERS): hue plus the alpha band's
-- midpoint, which is what Treatment.Tier draws an ungraded entry at. LOW carries no hue
-- — cap veils the icon and draws no ring — so the picker veils the sample and shows
-- nothing, which is the honest render and the contrast reference for the other two.
local TINTS = {
  { name = "HIGH",   color = { 1.00, 0.92, 0.55, 0.91 }, note = "cap's HIGH hue, ungraded alpha" },
  { name = "MEDIUM", color = { 0.45, 0.70, 0.95, 0.71 }, note = "cap's MEDIUM hue, ungraded alpha" },
  { name = "LOW",    veil = 0.31,                        note = "a veil, no ring — cap draws no glow here" },
  { name = "white",  color = { 1, 1, 1, 1 },             note = "untinted, to judge the shape" },
}

-- cap's own compositing (Overlay.lua): its own frame on UIParent at this strata and
-- level, ANCHORED to the item frame. The library instead reparents the glow onto its
-- host at host level + 8, so a glow judged on the item frame is not the glow cap draws.
local PROXY_STRATA, PROXY_LEVEL = "HIGH", 4
local TARGETS = {
  { name = "proxy",  note = "a UIParent frame at cap's strata, anchored to a shown icon" },
  { name = "direct", note = "a child of the icon at its level + 8, the library's own compositing" },
}

local SIZES = { 32, 48, 64 }
local ENGINES = { "Pixel", "Autocast", "Classic", "Thin", "Thick", "Medium" }

-- How it PLAYS, not which one plays. `speed` multiplies the candidate's declared loop
-- seconds, so 1x is Blizzard's own number and the steps sit either side of it. The two
-- envelopes ride on top of the loop; `depth` sizes both.
local TAU = math.pi * 2
local SPEEDS = { 0.5, 1, 2, 4 }
local BLENDS = { "ADD", "BLEND" }
local ENVELOPES = { { name = "off" }, { name = "0.4s", period = 0.4 },
                    { name = "0.8s", period = 0.8 }, { name = "1.6s", period = 1.6 } }
local DEPTHS = {
  { name = "25%", floor = 0.75, amp = 0.05 },
  { name = "50%", floor = 0.50, amp = 0.10 },
  { name = "80%", floor = 0.20, amp = 0.18 },
}

-- Which candidates the two library-side controls actually reach. An engine glow inside a
-- REGISTERED def reaches neither: ShowProc hands an engine only key/color/frameLevel/scale.
local SPEED_ENGINES = { Thin = true, Thick = true, Medium = true }
local BLEND_ENGINES = { Thin = true, Thick = true, Medium = true, Autocast = true }

-- Expansion capturing attention where contraction does not is a published result WITH a
-- published rebuttal, and whether motion-onset capture needs the motion to be jerky is
-- contested the same way. Both are one toggle each, so both get measured here.
local GROWS = { "expand", "contract" }
local MOTION = { { name = "smooth" }, { name = "17Hz", hz = 17 }, { name = "8Hz", hz = 8 } }

-- Raising contrast from the OTHER side: dim everything not emphasised. No motion, no
-- flash, no seizure exposure, and the only treatment here that structurally cannot
-- produce "everything glows".
local DIMS = { { name = "off" }, { name = "40%", a = 0.40 }, { name = "65%", a = 0.65 } }

local SPEED_NAMES, ENV_NAMES, DEPTH_NAMES, MOTION_NAMES, DIM_NAMES = {}, {}, {}, {}, {}
for i, v in ipairs(SPEEDS) do SPEED_NAMES[i] = v .. "x" end
for i, v in ipairs(ENVELOPES) do ENV_NAMES[i] = v.name end
for i, v in ipairs(DEPTHS) do DEPTH_NAMES[i] = v.name end
for i, v in ipairs(MOTION) do MOTION_NAMES[i] = v.name end
for i, v in ipairs(DIMS) do DIM_NAMES[i] = v.name end
local VIEWERS = {
  "EssentialCooldownViewer", "UtilityCooldownViewer",
  "BuffIconCooldownViewer", "BuffBarCooldownViewer",
}

-- Shipping client flipbook atlases: no dependency and no license question. `name` is the
-- 2x bake, `base` the 1x fallback. NOT handed to lib:RegisterGlow — that registry is
-- shared process-wide through LibStub, so registering would inject ClientLab entries into
-- every other host's picker. rows/cols/frames/secs/scale come from Blizzard's own
-- <FlipBook> declarations, cited per entry; `scale` is the drawn size as a multiple of
-- the HOST, not of the sheet.
local DECLARED, INFERRED, ASSUMED = "declared", "inferred", "assumed"
local ATLASES = {
  { name = "ui-cooldownmanager-alert-flipbook-2x", base = "ui-cooldownmanager-alert-flipbook",
    rows = 11, cols = 2, frames = 22, secs = 0.75, scale = 1.0, how = INFERRED,
    src = "94x517, byte-identical to the GCD sheet, and 2x11 is its only square-cell grid",
    note = "the CDM's own alert art" },
  { name = "ui-hud-actionbar-proc-loop-flipbook-2x", base = "ui-hud-actionbar-proc-loop-flipbook",
    rows = 6, cols = 5, frames = 30, secs = 1.0, scale = 1.4, how = DECLARED,
    src = "ActionButtonSpellAlerts.xml:25 + .lua:20 (setAllPoints on a 1.4x frame)",
    note = "what the lib calls Medium" },
  { name = "ui-hud-actionbar-proc-start-flipbook-2x", base = "ui-hud-actionbar-proc-start-flipbook",
    rows = 6, cols = 5, frames = 30, secs = 0.7, scale = 3.33, how = DECLARED,
    src = "ActionButtonSpellAlerts.xml:29 (fixed 150x150 CENTER over a 45px button)",
    note = "a start phase the lib never uses" },
  { name = "ui-hud-actionbar-gcd-flipbook-2x", base = "ui-hud-actionbar-gcd-flipbook",
    rows = 11, cols = 2, frames = 22, secs = 0.75, scale = 1.0, how = DECLARED,
    src = "CooldownViewer.xml:79 (CooldownFlash anchors to the item frame)",
    note = "the GCD sweep art" },
  { name = "rotationhelper-procloopblue-flipbook-2x", base = "rotationhelper-procloopblue-flipbook",
    rows = 6, cols = 5, frames = 30, secs = 1.0, scale = 1.4, how = INFERRED,
    src = "333x400, byte-identical to proc-loop and ants, both declared 6x5/30",
    note = "what the lib calls Thick" },
  { name = "rotationhelper-procstartblue-flipbook-2x", base = "rotationhelper-procstartblue-flipbook",
    rows = 6, cols = 5, frames = 30, secs = 0.7, scale = 3.33, how = INFERRED,
    src = "2x sheet 1275x1530 divides square only at 5x6; sized as its proc-start sibling",
    note = "its start phase" },
  { name = "rotationhelper_ants_flipbook_2x", base = "rotationhelper_ants_flipbook",
    rows = 6, cols = 5, frames = 30, secs = 1.0, scale = 1.47, how = DECLARED,
    src = "ActionButtonComponentTemplate.xml:80 (66x66 CENTER over a 45px button)",
    note = "what the lib calls Thin" },
  { name = "onebutton_procloop_flipbook_2x", base = "onebutton_procloop_flipbook",
    rows = 6, cols = 5, frames = 30, secs = 1.0, scale = 1.0, how = DECLARED,
    src = "ActionButtonSpellAlerts.lua:32 swaps it onto the .xml:25 ProcLoop declaration; "
       .. "its host is SetAllPoints, not the 1.4x of the standard alert path",
    note = "the assisted-rotation proc loop" },
  { name = "onebutton_procstart_flipbook_2x", base = "onebutton_procstart_flipbook",
    rows = 6, cols = 5, frames = 30, secs = 0.7, scale = 3.33, how = DECLARED,
    src = "ActionButtonSpellAlerts.lua:31 swaps it onto the .xml:29 ProcStart declaration",
    note = "its start phase" },
  { name = "visualalert_ants_flipbook_2x", base = "visualalert_ants_flipbook",
    rows = 6, cols = 5, frames = 30, secs = 1.0, scale = 1.0, how = DECLARED,
    src = "CooldownViewerVisualAlertTemplates.xml:23 (setAllPoints on the item frame)",
    note = "the CDM's marching ants" },
  { name = "transmog-itemslot-flipbook-loop-top-2x", base = "transmog-itemslot-flipbook-loop-top",
    rows = 7, cols = 10, frames = 70, secs = 2.33, scale = 1.0, how = DECLARED,
    src = "Blizzard_TransmogTemplates.xml:938", note = "edge art, top only" },
  { name = "transmog-itemslot-flipbook-loop-bottom-2x", base = "transmog-itemslot-flipbook-loop-bottom",
    rows = 7, cols = 10, frames = 70, secs = 2.33, scale = 1.0, how = DECLARED,
    src = "Blizzard_TransmogTemplates.xml:939", note = "edge art, bottom only" },
  { name = "transmog-itemslot-flipbook-loop-left-2x", base = "transmog-itemslot-flipbook-loop-left",
    rows = 3, cols = 30, frames = 70, secs = 2.33, scale = 1.0, how = DECLARED,
    src = "Blizzard_TransmogTemplates.xml:941", note = "edge art, left only" },
  { name = "transmog-itemslot-flipbook-loop-right-2x", base = "transmog-itemslot-flipbook-loop-right",
    rows = 3, cols = 30, frames = 70, secs = 2.33, scale = 1.0, how = DECLARED,
    src = "Blizzard_TransmogTemplates.xml:940", note = "edge art, right only" },
  { name = "transmog-itemslot-flipbook-sparks-2x", base = "transmog-itemslot-flipbook-sparks",
    rows = 4, cols = 6, frames = 24, secs = 0.8, scale = 1.0, how = INFERRED,
    src = "no declaration; the gearSlot sparks sibling is 4x6/24 and 900x624 divides by it",
    note = "sparks, no ring" },
}

-- The three flipbook engines name their atlas as a constant; the other three draw
-- procedurally. Normalised to the lowercase 1x name so the same art matches whichever
-- of the three groups reached it first. Used only to mark duplicates.
local ENGINE_ATLAS = {
  Thin = "rotationhelper_ants_flipbook",
  Thick = "rotationhelper-procloopblue-flipbook",
  Medium = "ui-hud-actionbar-proc-loop-flipbook",
}

-- The library's own PROC grid. Reached only by a pack glow whose def declares none, and
-- the card marks that card `assumed`.
local FB_COLS, FB_ROWS, FB_FRAMES = 5, 6, 30

-- Blizzard's declaration, reachable from any candidate that resolves to the same art —
-- which is how a card can say the library is drawing the wrong grid for it.
local DECL_BY_ATLAS = {}
for _, e in ipairs(ATLASES) do DECL_BY_ATLAS[e.base] = e end

local function normalAtlas(name)
  return (tostring(name):lower():gsub("[-_]2x$", ""))
end

local FOCUS_KEY, GRID_KEY, CDM_KEY = "labfocus", "labpalette", "labpalettecdm"
local PLATE = { 0.22, 0.22, 0.25 }
local CELL_W, CELL_H, COLS = 104, 108, 5
local GRID_W = 8 + CELL_W * COLS
local PANEL_W, PANEL_H, CARD_X, BOX = 560, 592, 216, 190

local panel, gridWindow, cells
local caption                       -- defined with the card, called from PaintCDM
local tintIdx, sizeIdx, targetIdx = 1, 2, 1
local speedIdx, blendIdx, pulseIdx, breatheIdx, depthIdx = 2, 1, 1, 1, 2
local growIdx, motionIdx, dimIdx, emphOrd = 1, 1, 1, 1
local greyOn = false

-- A dichromat keeps luminance and loses hue, and so does peripheral vision. A tier set
-- that cannot be ranked at zero saturation cannot be ranked by either.
local function tintColor(tint)
  local c = tint.color
  if not c or not greyOn then return c end
  local y = 0.299 * c[1] + 0.587 * c[2] + 0.114 * c[3]
  return { y, y, y, c[4] }
end
local liveCDM, combatNoticed = true, false
local index, selected = 1, nil
local candidates, byId, sections = {}, {}, {}
local kind = {}          -- id -> "engine" | "atlas" | "registry", resolved once at build
local painted = {}       -- { frame, id, proxy, item } — an entry survives a FAILED teardown

-- Playing and stopping ---------------------------------------------------------

-- Three routes, one pairing rule: an atlas candidate drives the raw Flipbook sink, a
-- registered name goes through Proc, an engine type through Show/Hide. Proc:Clear stands
-- in for lib.Remove's Proc:Stop because a picker re-tints constantly and the outro is
-- noise; Stop also defers release into an OnFinished for a pack glow shipping end art,
-- landing after the next Apply on the same key.

--@unverified Classic's teardown plays animOut and releases in its OnFinished; whether
-- that completes on a host hidden or released underneath it has not been observed.
local function stop(frame, id, key)
  if not id then return true end
  local k = kind[id]
  if k == "atlas" then
    return (pcall(lib.Flipbook.Hide, lib.Flipbook, frame, key))
  elseif k == "registry" then
    return (pcall(lib.Proc.Clear, lib.Proc, frame, { glow = id, key = key }))
  end
  return (pcall(lib.Hide, frame, id, key))
end

-- `desaturated` is passed rather than left to default because it is load-bearing: the
-- blue and gold source sheets must be greyed before the tier hue multiplies in, or a
-- tint reads as a multiply against the art's own colour.
local function start(frame, id, color, key)
  local c = byId[id]
  local secs = ((c and c.secs) or 1.0) * SPEEDS[speedIdx]
  local blend = BLENDS[blendIdx]
  if kind[id] == "atlas" then
    return (pcall(lib.Flipbook.Show, lib.Flipbook, frame, {
      key = key, color = color, atlas = c.atlas, blendMode = blend, desaturated = true,
      rows = c.rows, cols = c.cols, frames = c.frames, speed = secs, scale = c.scale,
    }))
  end
  -- Two names for one number: an engine reads `speed`, a registered glow's proc loop
  -- reads `loopDuration`, and neither minds the other being present.
  return (pcall(lib.Apply, frame, id, { key = key, color = color, loop = true,
    speed = secs, loopDuration = secs, blendMode = blend }))
end

-- The candidate run ------------------------------------------------------------

-- What the client says about an atlas, as a MEASUREMENT — it no longer drives anything.
-- GetAtlasInfo is MayReturnNothing, so a nothing return is "not found", never zero; and
-- absent flipBook fields are reported apart from present-but-zero ones, because `0` is
-- truthy in Lua and a library that writes `rows = rows or info.flipBookRows` would take
-- a zero and animate an empty grid.
local function readGrid(atlas)
  local info = C_Texture.GetAtlasInfo(atlas)
  if type(info) ~= "table" then return "atlas not found" end
  local r, c, f = info.flipBookRows, info.flipBookColumns, info.flipBookFrames
  if r == nil and c == nil then return "no flipBook fields" end
  if type(r) ~= "number" or type(c) ~= "number" or r <= 0 or c <= 0 then
    return ("flipBook fields present but empty: rows=%s cols=%s"):format(tostring(r), tostring(c))
  end
  return ("rows=%d cols=%d frames=%s"):format(r, c, tostring(f))
end

local function atlasCandidate(entry)
  local atlas = entry.name
  local read = readGrid(atlas)
  if read == "atlas not found" then
    atlas = entry.base
    read = readGrid(atlas)
  end
  return { id = atlas, group = "Blizzard atlases", atlas = atlas, note = entry.note,
           rows = entry.rows, cols = entry.cols, frames = entry.frames,
           secs = entry.secs, scale = entry.scale, how = entry.how, src = entry.src,
           read = read, sig = "atlas:" .. entry.base }
end

local function registryCandidate(name)
  local def = lib:GetGlowInfo(name) or {}
  local c = { id = name, group = def.source or "Unknown", engine = def.engine }
  if def.engine then
    c.atlas = "engine: " .. def.engine
    c.how, c.src = "n/a", "an engine draws its own geometry"
    c.sig = ENGINE_ATLAS[def.engine] and ("atlas:" .. ENGINE_ATLAS[def.engine]) or ("engine:" .. def.engine)
  elseif def.atlas then
    c.atlas = def.atlas
    c.sig = "atlas:" .. normalAtlas(def.atlas)
    c.read = readGrid(def.atlas)
    local d = DECL_BY_ATLAS[normalAtlas(def.atlas)]
    if d then
      c.rows, c.cols, c.frames, c.secs, c.how = d.rows, d.cols, d.frames, d.secs, d.how
      c.src = d.src .. " — the library instead lets its own default grid stand"
    else
      c.rows, c.cols, c.frames = def.rows, def.cols, def.frames
      c.how, c.src = ASSUMED, "no declaration found for this atlas"
    end
  else
    c.atlas = "texture files: " .. tostring(def.path or "resolver")
    c.rows, c.cols, c.frames = def.rows or FB_ROWS, def.cols or FB_COLS, def.frames or FB_FRAMES
    c.how, c.src = DECLARED, "declared by the pack"
    c.sig = "path:" .. tostring(def.path or name)
  end
  return c
end

-- Four groups in one next/prev sequence. Groups 3 and 4 are derived from GetGlowList,
-- never a hardcoded pack list, with the library's own baselines ahead of installed packs.
local function buildCandidates()
  -- 27 cards cover ~9 distinct looks: the library's baselines re-register art the engine
  -- types and the Blizzard atlases already offer. The duplicates stay in the run, because
  -- the group must keep coming from GetGlowList, but a card says what it repeats.
  local firstBySig = {}
  local function add(c, k)
    kind[c.id] = k
    c.speedReaches = k == "atlas" or (k == "engine" and SPEED_ENGINES[c.id] == true)
      or (k == "registry" and c.engine == nil)
    c.blendReaches = k == "atlas" or (k == "engine" and BLEND_ENGINES[c.id] == true)
    candidates[#candidates + 1] = c
    c.idx = #candidates
    byId[c.id] = c
    local sig = c.sig
    if sig then
      if firstBySig[sig] then c.duplicateOf = firstBySig[sig] else firstBySig[sig] = c.id end
    end
  end
  local function section(group, list)
    local names = {}
    for i, c in ipairs(list) do names[i] = c.id end
    sections[#sections + 1] = { group = group, names = names }
  end

  local engines = {}
  for i, name in ipairs(ENGINES) do
    local art = ENGINE_ATLAS[name]
    local d = art and DECL_BY_ATLAS[art]
    engines[i] = { id = name, group = "engine types", atlas = art or ("engine: " .. name),
                   how = d and d.how or "n/a",
                   src = d and (d.src .. " — the library instead lets its own default grid stand")
                          or "an engine draws its own geometry",
                   rows = d and d.rows, cols = d and d.cols, frames = d and d.frames,
                   secs = d and d.secs, read = art and readGrid(art) or nil,
                   sig = art and ("atlas:" .. art) or ("engine:" .. name) }
    add(engines[i], "engine")
  end
  section("engine types", engines)

  local atlases = {}
  for i, entry in ipairs(ATLASES) do
    atlases[i] = atlasCandidate(entry)
    add(atlases[i], "atlas")
  end
  section("Blizzard atlases", atlases)

  local bySource, sources = {}, {}
  for _, name in ipairs(lib:GetGlowList()) do
    local c = registryCandidate(name)
    if not bySource[c.group] then
      bySource[c.group] = {}
      sources[#sources + 1] = c.group
    end
    local bucket = bySource[c.group]
    bucket[#bucket + 1] = c
  end
  table.sort(sources, function(a, b)
    if (a == "LibOrbitGlow") ~= (b == "LibOrbitGlow") then return a == "LibOrbitGlow" end
    return a < b
  end)
  for _, src in ipairs(sources) do
    for _, c in ipairs(bySource[src]) do add(c, "registry") end
    section(src, bySource[src])
  end
end

-- The live Cooldown Manager ----------------------------------------------------
-- Enumerated the way cap's Bind.lua does, with the viewer globals resolved BY STRING
-- through ns.G. A secret item list is skipped rather than iterated.
local function cdmFrames()
  local out = {}
  for _, name in ipairs(VIEWERS) do
    local viewer = ns.G(name)
    if viewer then
      local ok, list = pcall(viewer.GetItemFrames, viewer)
      if ok and type(list) == "table" and not ns.IsSecretTable(list) then
        for _, f in ipairs(list) do out[#out + 1] = f end
      end
    end
  end
  return out
end

-- cap's Overlay.itemShown, copied whole, including its policy that a REFUSED read
-- draws: an overlay in the wrong place is a visible bug and a silently blank one is not.
local function itemShown(item)
  local ok, shown = pcall(item.IsVisible, item)
  if not ok or shown == nil or ns.IsSecret(shown) then return true end
  return shown and true or false
end

-- Proxies -----------------------------------------------------------------------
-- SetFrameStrata is protected, so a proxy is only ever created and layered from
-- PaintCDM, which refuses in combat.
local proxyFree = {}

local function acquireProxy()
  local p = table.remove(proxyFree)
  if not p then
    p = CreateFrame("Frame", nil, UIParent)
    p:SetFrameStrata(PROXY_STRATA)
    p:SetFrameLevel(PROXY_LEVEL)
    -- Below the library's glow (host level + 8) and above the icon, so an emphasised
    -- glow still reads at full strength over a veiled neighbour.
    p.veil = p:CreateTexture(nil, "BACKGROUND")
    p.veil:SetAllPoints(p)
    p.veil:SetColorTexture(0, 0, 0, 1)
  end
  p.veil:SetAlpha(0)
  p:Show()
  return p
end

local function releaseProxy(p)
  p:Hide()
  p:SetAlpha(1)
  p:ClearAllPoints()
  proxyFree[#proxyFree + 1] = p
end

--- Returns whether the proxy took an anchor. `k == 1` is the plain two-corner pin; a
--- breathing proxy needs an explicit rect, and an item that will not give up a plain
--- size falls back to the pin rather than guessing one.
local function anchorProxy(p, item, k)
  p:ClearAllPoints()
  if k ~= 1 then
    local ok, w, h = pcall(item.GetSize, item)
    if ok and type(w) == "number" and type(h) == "number" and w > 0 and h > 0 then
      p:SetSize(w * k, h * k)
      return (pcall(p.SetPoint, p, "CENTER", item, "CENTER", 0, 0))
    end
  end
  return (pcall(p.SetAllPoints, p, item))
end

-- Envelopes ---------------------------------------------------------------------
-- Plain-number animation of the host the glow hangs on, never of a Blizzard frame — so
-- `direct` mode and the grid run flat, and the panel says so. The library pins the glow
-- to the host's corners with a fixed pad, so a host resize grows it additively.
local envTicker

-- ⚠ THE PHASE OFFSET IS A SAFETY PROPERTY, NOT A STYLE CHOICE — DO NOT "FIX" IT TO SYNC.
-- WCAG 2.3.1's flash threshold is a luminance swing over a 10° field: one 40px icon is
-- ~1,600 px² and trivially compliant, but fourteen flashing IN STEP are one area of
-- ~22,400 px² and are not. MIL-STD-1472 tells you to synchronise warning flashes; the two
-- standards genuinely conflict and this sides with the seizure floor.
local PHASE_STEP = 0.13

local function envValues(offset)
  local d = DEPTHS[depthIdx]
  local hz = MOTION[motionIdx].hz
  local t = GetTime()
  if hz then t = math.floor(t * hz) / hz end
  local pulse, breathe = ENVELOPES[pulseIdx], ENVELOPES[breatheIdx]
  local a, k = 1, 1
  offset = offset or 0
  if pulse.period then
    local u = (1 - math.cos(((t / pulse.period) + offset) % 1 * TAU)) * 0.5
    a = d.floor + (1 - d.floor) * u
  end
  if breathe.period then
    local u = (1 - math.cos(((t / breathe.period) + offset) % 1 * TAU)) * 0.5
    k = 1 + d.amp * u * (GROWS[growIdx] == "contract" and -1 or 1)
  end
  return a, k
end

local function envDrive()
  if panel and panel.sample then
    local a, k = envValues(0)
    panel.sample:SetAlpha(a)
    panel.sample:SetSize(SIZES[sizeIdx] * k, SIZES[sizeIdx] * k)
  end
  local ord = 0
  for _, p in ipairs(painted) do
    if p.proxy and p.item then
      ord = ord + 1
      local a, k = envValues((ord - 1) * PHASE_STEP)
      p.proxy:SetAlpha(a)
      anchorProxy(p.proxy, p.item, k)
    end
  end
end

local function envReset()
  if panel and panel.sample then
    panel.sample:SetAlpha(1)
    panel.sample:SetSize(SIZES[sizeIdx], SIZES[sizeIdx])
  end
  for _, p in ipairs(painted) do
    if p.proxy and p.item then
      p.proxy:SetAlpha(1)
      anchorProxy(p.proxy, p.item, 1)
    end
  end
end

--- Veil every proxy but the emphasised one. It dims by OCCLUSION — the icon underneath is
--- a Blizzard frame this panel never touches — so it is not a test of desaturating the art.
local function applyDim()
  local d, ord = DIMS[dimIdx].a, 0
  for _, p in ipairs(painted) do
    if p.proxy then
      ord = ord + 1
      p.proxy.veil:SetAlpha((d and ord ~= emphOrd) and d or 0)
    end
  end
  return ord
end

local function envStop()
  if envTicker then
    envTicker:Cancel()
    envTicker = nil
  end
  envReset()
end

local function envRefresh()
  applyDim()
  if ENVELOPES[pulseIdx].period or ENVELOPES[breatheIdx].period then
    if not envTicker then envTicker = C_Timer.NewTicker(0.03, envDrive) end
  else
    envStop()
  end
end

-- Anchoring is ONE-DIRECTIONAL: a proxy follows the item's rectangle but not its
-- visibility, and GetItemFrames keeps returning frames from a viewer the player switched
-- off. Direct mode is immune — the library makes the glow a child.
local WATCH_INTERVAL = 0.5
local watcher

local function stopWatching()
  if watcher then
    watcher:Cancel()
    watcher = nil
  end
end

--- Returns (released, still held). A teardown that ERRORED keeps its entry, so the
--- frame stays reachable for the PLAYER_REGEN_ENABLED retry. This sees errors only: a
--- protected call blocked under lockdown refuses without erroring, and nothing here
--- distinguishes that from a release — direct mode is where that gap lives.
function G.ClearCDM()
  local keep = {}
  for _, p in ipairs(painted) do
    if stop(p.frame, p.id, CDM_KEY) then
      if p.proxy then releaseProxy(p.proxy) end
    else
      keep[#keep + 1] = p
    end
  end
  local released = #painted - #keep
  painted = keep
  -- Unconditional, because `painted` is exactly what does NOT empty when a teardown is
  -- refused; PaintCDM re-arms and startWatching's own guard makes that free.
  stopWatching()
  return released, #keep
end

-- Buff rows hide individually and constantly — an aura falling off hides its row while
-- the viewer keeps enumerating it — so a hidden icon drops ITS OWN proxy and nothing
-- else. Dropping the whole paint would blink the palette out mid-judgement.
-- Returns (released, proxies still live).
local function dropHidden()
  local keep, dropped, proxies = {}, 0, 0
  for _, p in ipairs(painted) do
    if p.proxy and p.item and not itemShown(p.item) and stop(p.frame, p.id, CDM_KEY) then
      releaseProxy(p.proxy)
      dropped = dropped + 1
    else
      keep[#keep + 1] = p
      if p.proxy then proxies = proxies + 1 end
    end
  end
  painted = keep
  return dropped, proxies
end

local function startWatching()
  if watcher then return end
  watcher = C_Timer.NewTicker(WATCH_INTERVAL, function()
    local dropped, proxies = dropHidden()
    if dropped > 0 then
      caption()
      ns.Printf("released %d proxy glow(s) — their icon stopped being shown. An anchored "
        .. "proxy keeps the icon's rectangle but not its visibility.", dropped)
    end
    if proxies == 0 then stopWatching() end
  end)
end

--@unverified direct mode reparents a pooled glow frame onto a POOLED CDM item frame;
-- neither that nor its teardown under lockdown (ClearAllPoints is protected) has been
-- observed in the client. Proxy mode, the default, never touches a Blizzard frame.

--- `quiet` is the live-stepping path: it says nothing on success, and announces a combat
--- refusal ONCE per pull rather than on every press of next.
function G.PaintCDM(quiet)
  if InCombatLockdown() then
    if not quiet then
      ns.Print("won't paint the Cooldown Manager in combat — drop combat and press it again.")
    elseif not combatNoticed then
      combatNoticed = true
      ns.Print("in combat — next/prev still steps the card, but |cfffffffflive on CDM|r "
        .. "will not repaint until you drop combat.")
    end
    return
  end
  G.ClearCDM()
  caption()
  local tint, direct = TINTS[tintIdx], TARGETS[targetIdx].name == "direct"
  local dimming = DIMS[dimIdx].a ~= nil
  if not selected then return end
  -- Dimming is a treatment in its own right, so a tint that draws no ring stops being a
  -- reason to paint nothing: the veils still have to go on.
  if not tint.color and not dimming then
    if not quiet then
      ns.Printf("%s draws no ring — switch the tint to HIGH, MEDIUM or white first.", tint.name)
    end
    return
  end
  local frames = cdmFrames()
  if #frames == 0 then
    if not quiet then
      ns.Print("no Cooldown Manager item frames to paint — turn the Cooldown Manager on "
        .. "and make sure a viewer has icons in it.")
    end
    return
  end

  -- An entry ClearCDM could not release still owns its proxy, so re-painting that item
  -- would stack a second glow on one icon.
  local held = {}
  for _, p in ipairs(painted) do
    if p.item then held[p.item] = true end
  end

  local attempted, hidden, skipped, unanchored, ord = 0, 0, 0, 0, 0
  for _, item in ipairs(frames) do
    local target
    if held[item] then
      skipped = skipped + 1
    elseif direct then
      -- Recorded BEFORE the call: Apply shows the acquired frame before the geometry
      -- that can throw, so a throw still leaves something to tear down.
      painted[#painted + 1] = { frame = item, id = selected, item = item }
      target = item
    elseif not itemShown(item) then
      hidden = hidden + 1
    else
      -- The same discipline one step earlier: SetAllPoints is protected and its target
      -- is a Blizzard frame, so a throw must not strand a shown proxy outside both
      -- `painted` and the free list.
      local proxy = acquireProxy()
      ord = ord + 1
      painted[#painted + 1] = { frame = proxy, id = selected, proxy = proxy, item = item }
      if anchorProxy(proxy, item, 1) then
        target = proxy
      else
        unanchored = unanchored + 1
      end
    end
    -- With dimming on, exactly ONE icon carries the glow and the rest carry the veil.
    -- That is the whole treatment: raise contrast from the other side.
    if target and tint.color and not (dimming and not direct and ord ~= emphOrd) then
      attempted = attempted + 1
      start(target, selected, tintColor(tint), CDM_KEY)
    end
  end
  if not direct then startWatching() end
  applyDim()
  caption()

  -- "attempted", not "painted": a clean pcall means Apply did not error, not that any
  -- pixel appeared — an unresolved glow name or a missing texture path both return
  -- normally and draw nothing. Your eye is the oracle.
  if quiet then return end
  local why = {}
  if hidden > 0 then why[#why + 1] = hidden .. " on hidden icons" end
  if skipped > 0 then why[#why + 1] = skipped .. " still held from a refused clear" end
  if unanchored > 0 then why[#why + 1] = unanchored .. " would not anchor" end
  ns.Printf("attempted |cffffffff%s|r at %s on %d of %d Cooldown Manager frame(s), %s%s.",
    selected, tint.name, attempted, #frames, TARGETS[targetIdx].name,
    #why > 0 and (" — skipped: " .. table.concat(why, ", ")) or "")
end

-- The card ---------------------------------------------------------------------

local function reachNote(reaches)
  return reaches and "" or " |cffff8844(not reached)|r"
end

local function markRow(buttons, idx, names)
  for i, b in ipairs(buttons or {}) do
    b.text:SetText(i == idx and ("|cffffd100" .. names[i] .. "|r") or names[i])
  end
end

function caption()
  if not panel then return end
  local tint, c = TINTS[tintIdx], candidates[index]
  panel.caption:SetText(("tint |cffffffff%s|r — %s"):format(tint.name, tint.note))
  panel.envLine:SetText(("|cff808080speed|r %sx%s  |cff808080blend|r %s%s  "
    .. "|cff808080pulse|r %s  |cff808080breathe|r %s %s  |cff808080depth|r %s  "
    .. "|cff808080motion|r %s  |cff808080dim|r %s |cff808080— envelopes move the frame the "
    .. "glow hangs on, so the focus sample and PROXY-painted icons breathe while `direct` "
    .. "and the grid run flat; each icon carries a phase offset so the set never flashes "
    .. "as one area. dim veils by OCCLUSION — the icon art itself is never touched.|r")
    :format(
    SPEEDS[speedIdx], reachNote(not c or c.speedReaches),
    BLENDS[blendIdx], reachNote(not c or c.blendReaches),
    ENVELOPES[pulseIdx].name, ENVELOPES[breatheIdx].name, GROWS[growIdx],
    DEPTHS[depthIdx].name, MOTION[motionIdx].name, DIM_NAMES[dimIdx]))
  local live = #painted
  panel.cdmLine:SetText((live == 0
      and "CDM: |cff808080not painted|r"
      or ("CDM: |cffffffff%d|r frame(s) painted %s"):format(live, TARGETS[targetIdx].name))
    .. "  |cff808080— cleared on combat, a spec or loadout change, any control change and "
    .. "panel close; one proxy drops when its own icon hides.|r")
  for i, b in ipairs(panel.tintButtons) do
    b.text:SetText(i == tintIdx and ("|cffffd100" .. TINTS[i].name .. "|r") or TINTS[i].name)
  end
  for i, b in ipairs(panel.sizeButtons) do
    b.text:SetText(i == sizeIdx and ("|cffffd100" .. SIZES[i] .. "|r") or tostring(SIZES[i]))
  end
  for i, b in ipairs(panel.targetButtons) do
    b.text:SetText(i == targetIdx and ("|cffffd100" .. TARGETS[i].name .. "|r") or TARGETS[i].name)
  end
  markRow(panel.speedButtons, speedIdx, SPEED_NAMES)
  markRow(panel.blendButtons, blendIdx, BLENDS)
  markRow(panel.pulseButtons, pulseIdx, ENV_NAMES)
  markRow(panel.breatheButtons, breatheIdx, ENV_NAMES)
  markRow(panel.depthButtons, depthIdx, DEPTH_NAMES)
  markRow(panel.growButtons, growIdx, GROWS)
  markRow(panel.motionButtons, motionIdx, MOTION_NAMES)
  markRow(panel.dimButtons, dimIdx, DIM_NAMES)
  panel.grey.text:SetText(greyOn and "|cffffd100[x] greyscale|r" or "[ ] greyscale")
  panel.live.text:SetText(liveCDM and "|cffffd100[x] live on CDM|r" or "[ ] live on CDM")
end

local function paintFocus()
  if not panel then return end
  local s, tint, size = panel.sample, TINTS[tintIdx], SIZES[sizeIdx]
  if stop(s, s.painted, FOCUS_KEY) then s.painted = nil end
  s:SetSize(size, size)
  local dim = 1 - (tint.veil or 0)
  panel.plate:SetSize(size, size)
  panel.plate:SetColorTexture(PLATE[1] * dim, PLATE[2] * dim, PLATE[3] * dim, 1)
  local c = candidates[index]
  if c and tint.color then
    s.painted = c.id
    start(s, c.id, tintColor(tint), FOCUS_KEY)
  end
end

-- A grid rendered at a size or tint the card is not wearing would answer a question
-- nobody asked, so both surfaces and the CDM move together.
local function repaintGrid()
  if not cells then return end
  local tint, size = TINTS[tintIdx], SIZES[sizeIdx]
  local dim = 1 - (tint.veil or 0)
  for _, cell in ipairs(cells) do
    if stop(cell.sample, cell.painted, GRID_KEY) then cell.painted = nil end
    cell.sample:SetSize(size, size)
    cell.plate:SetColorTexture(PLATE[1] * dim, PLATE[2] * dim, PLATE[3] * dim, 1)
    if tint.color then
      cell.painted = cell.id
      start(cell.sample, cell.id, tintColor(tint), GRID_KEY)
    end
  end
end

local function clearGrid()
  if not cells then return end
  for _, cell in ipairs(cells) do
    if stop(cell.sample, cell.painted, GRID_KEY) then cell.painted = nil end
  end
end

local HOW_COLOUR = { declared = "ff60c060", inferred = "ffd0b050", assumed = "ffff8844" }

local function refreshCard()
  if not panel then return end
  local c = candidates[index]
  if not c then return end
  panel.name:SetText(c.id)
  panel.meta:SetText(("|cff808080%s|r  ·  %s%s%s"):format(c.group, kind[c.id],
    c.note and ("  ·  " .. c.note) or "",
    c.duplicateOf and ("   |cffff8844same art as " .. c.duplicateOf .. "|r") or ""))
  panel.atlas:SetText("|cff808080" .. tostring(c.atlas) .. "|r")

  local shape = c.cols and ("%d×%d · %d frames%s"):format(c.cols, c.rows, c.frames,
    c.secs and (" · %.2gs → %.2gs"):format(c.secs, c.secs * SPEEDS[speedIdx]) or "") or "no grid"
  local how = c.how or "assumed"
  panel.grid:SetText(("%s   |c%s%s|r |cff808080%s|r"):format(shape,
    HOW_COLOUR[how] or "ffff8844", how, c.src and (" — " .. c.src) or ""))
  panel.read:SetText(c.read
    and ("|cff808080GetAtlasInfo:|r " .. c.read
         .. (c.scale and ("   |cff808080drawn at %.2gx the host|r"):format(c.scale) or ""))
    or "")

  panel.count:SetText(("|cffffffff%d|r / %d"):format(index, #candidates))
  panel.sizeNote:SetText(SIZES[sizeIdx] .. "px")
  for _, cell in ipairs(cells or {}) do
    if cell.id == c.id then cell.sel:Show() else cell.sel:Hide() end
  end
  paintFocus()
  caption()
end

function G.Select(id)
  if not id then return end
  selected = id
  index = (byId[id] and byId[id].idx) or index
  refreshCard()
  if liveCDM and panel and panel:IsShown() then G.PaintCDM(true) end
end

function G.Step(delta)
  if #candidates == 0 then return end
  index = ((index - 1 + delta) % #candidates) + 1
  G.Select(candidates[index].id)
end

-- A control that changed one surface but not the others would leave the card describing
-- a tint the painted icons are not wearing, and the output is a colour judgement.
local function controlChanged()
  G.ClearCDM()
  repaintGrid()
  refreshCard()
  if liveCDM and panel and panel:IsShown() then G.PaintCDM(true) end
  envRefresh()
end

-- The grid window ---------------------------------------------------------------

local function makeCell(parent, id)
  local b = CreateFrame("Button", nil, parent)
  b:SetSize(CELL_W - 6, CELL_H - 6)
  b.id = id

  local sel = b:CreateTexture(nil, "BACKGROUND")
  sel:SetAllPoints(b)
  sel:SetColorTexture(0.28, 0.30, 0.44, 0.95)
  sel:Hide()
  b.sel = sel

  local sample = CreateFrame("Frame", nil, b)
  sample:SetPoint("TOP", b, "TOP", 0, -10)
  sample:SetSize(SIZES[sizeIdx], SIZES[sizeIdx])
  local plate = sample:CreateTexture(nil, "ARTWORK")
  plate:SetAllPoints(sample)
  plate:SetColorTexture(PLATE[1], PLATE[2], PLATE[3], 1)
  b.sample, b.plate = sample, plate

  local fs = b:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  fs:SetPoint("BOTTOMLEFT", b, "BOTTOMLEFT", 2, 4)
  fs:SetPoint("BOTTOMRIGHT", b, "BOTTOMRIGHT", -2, 4)
  fs:SetJustifyH("CENTER")
  fs:SetText(id)
  b:SetScript("OnClick", function() G.Select(id) end)
  return b
end

local function buildGrid(content)
  local y, out = 8, {}
  for _, sec in ipairs(sections) do
    local head = content:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    head:SetPoint("TOPLEFT", content, "TOPLEFT", 8, -y)
    head:SetText(("|cffffd100%s|r  |cff808080(%d)|r"):format(sec.group, #sec.names))
    y = y + 20
    for i, name in ipairs(sec.names) do
      local cell = makeCell(content, name)
      cell:SetPoint("TOPLEFT", content, "TOPLEFT",
        8 + ((i - 1) % COLS) * CELL_W, -(y + math.floor((i - 1) / COLS) * CELL_H))
      out[#out + 1] = cell
    end
    y = y + math.ceil(#sec.names / COLS) * CELL_H + 8
  end
  content:SetSize(GRID_W, y + 8)
  return out
end

local function buildGridWindow()
  local UI = ns.UI
  local root = CreateFrame("Frame", nil, UIParent)
  root:SetSize(GRID_W + 52, 560)
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
  title:SetText("ClientLab — every candidate at once")

  UI.button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  local scroll = CreateFrame("ScrollFrame", nil, root, "UIPanelScrollFrameTemplate")
  scroll:SetPoint("TOPLEFT", root, "TOPLEFT", 10, -34)
  scroll:SetPoint("BOTTOMRIGHT", root, "BOTTOMRIGHT", -30, 10)
  local content = CreateFrame("Frame", nil, scroll)
  content:SetSize(GRID_W, 1)
  scroll:SetScrollChild(content)

  cells = buildGrid(content)
  root:SetScript("OnHide", clearGrid)
  root:SetScript("OnShow", function()
    repaintGrid()
    refreshCard()
  end)
  root:Hide()
  return root
end

local function toggleGrid()
  if InCombatLockdown() and not gridWindow then
    ns.Print("can't build the grid in combat — open it once out of combat.")
    return
  end
  gridWindow = gridWindow or buildGridWindow()
  if gridWindow:IsShown() then
    gridWindow:Hide()
  else
    gridWindow:ClearAllPoints()
    gridWindow:SetPoint("TOPLEFT", panel, "TOPRIGHT", 12, 0)
    gridWindow:Show()
  end
end

-- The focus panel ---------------------------------------------------------------

local function toggleRow(root, label, items, y, get, set, x0)
  x0 = x0 or 10
  local fs = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  fs:SetPoint("TOPLEFT", root, "TOPLEFT", x0, y - 2)
  fs:SetText(label)
  local out, x = {}, x0 + 46
  for i, name in ipairs(items) do
    local b = ns.UI.button(root, name, 8 * #name + 22, 20, function()
      if get() ~= i then set(i); controlChanged() end
    end)
    b:SetPoint("TOPLEFT", root, "TOPLEFT", x, y)
    x = x + 8 * #name + 26
    out[i] = b
  end
  return out, x
end

-- The box is sized for the largest overflow candidate (3.33x a 64px sample); a glow is
-- drawn OUTSIDE the sample frame, so a small box would crop the very art being judged.
local function buildCard(root)
  local box = CreateFrame("Frame", nil, root)
  box:SetPoint("TOPLEFT", root, "TOPLEFT", 14, -34)
  box:SetSize(BOX, BOX)

  -- The plate is a SIBLING of the sample, not its child: an envelope moves the frame the
  -- glow hangs on, and a stand-in icon that breathed with it would be answering a
  -- question nobody asked — cap will not scale the icon.
  root.sample = CreateFrame("Frame", nil, box)
  root.sample:SetPoint("CENTER", box, "CENTER", 0, 0)
  root.sample:SetSize(SIZES[sizeIdx], SIZES[sizeIdx])
  root.plate = box:CreateTexture(nil, "ARTWORK")
  root.plate:SetPoint("CENTER", box, "CENTER", 0, 0)
  root.plate:SetSize(SIZES[sizeIdx], SIZES[sizeIdx])
  root.plate:SetColorTexture(PLATE[1], PLATE[2], PLATE[3], 1)

  root.sizeNote = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
  root.sizeNote:SetPoint("TOP", box, "BOTTOM", 0, -4)

  local function line(font, y, h)
    local fs = root:CreateFontString(nil, "OVERLAY", font)
    fs:SetPoint("TOPLEFT", root, "TOPLEFT", CARD_X, y)
    fs:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, y)
    fs:SetJustifyH("LEFT")
    fs:SetWordWrap(true)
    if h then fs:SetHeight(h) end
    return fs
  end
  root.name = line("GameFontNormal", -36, 32)
  root.meta = line("GameFontDisableSmall", -72)
  root.atlas = line("GameFontDisableSmall", -88)
  root.grid = line("GameFontHighlightSmall", -104, 44)
  root.read = line("GameFontDisableSmall", -150, 28)

  root.count = root:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  root.count:SetPoint("TOPLEFT", root, "TOPLEFT", CARD_X, -178)
end

local function build()
  local UI = ns.UI
  buildCandidates()

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
  title:SetText("ClientLab — glow palette")

  UI.button(root, "×", 20, 20, function() root:Hide() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -8, -8)

  buildCard(root)

  UI.button(root, "< prev", 70, 20, function() G.Step(-1) end)
      :SetPoint("TOPLEFT", root, "TOPLEFT", 14, -246)
  UI.button(root, "next >", 70, 20, function() G.Step(1) end)
      :SetPoint("TOPLEFT", root, "TOPLEFT", 90, -246)
  root.live = UI.button(root, "[x] live on CDM", 132, 20, function()
    liveCDM = not liveCDM
    if liveCDM then controlChanged() else G.ClearCDM(); caption() end
  end)
  root.live:SetPoint("TOPLEFT", root, "TOPLEFT", 172, -246)

  local names = {}
  for i, t in ipairs(TINTS) do names[i] = t.name end
  root.tintButtons = toggleRow(root, "tint", names, -276,
    function() return tintIdx end, function(i) tintIdx = i end)

  local px = {}
  for i, s in ipairs(SIZES) do px[i] = tostring(s) end
  root.sizeButtons = toggleRow(root, "size", px, -302,
    function() return sizeIdx end, function(i) sizeIdx = i end)

  local how = {}
  for i, t in ipairs(TARGETS) do how[i] = t.name end
  root.targetButtons = toggleRow(root, "target", how, -328,
    function() return targetIdx end, function(i) targetIdx = i end)

  UI.button(root, "grid", 54, 20, toggleGrid)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, -328)
  UI.button(root, "paint", 60, 20, function() G.PaintCDM() end)
      :SetPoint("TOPRIGHT", root, "TOPRIGHT", -70, -302)
  UI.button(root, "clear", 60, 20, function()
    local released, held = G.ClearCDM()
    caption()
    ns.Printf("released %d painted frame(s)%s.", released,
      held > 0 and (", " .. held .. " REFUSED — retried when you leave combat") or "")
  end):SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, -302)

  -- How it PLAYS. Speed and blend are handed to the library; the two envelopes are ours
  -- and ride on top, so they reach every candidate where the first two do not.
  root.speedButtons = toggleRow(root, "speed", SPEED_NAMES, -354,
    function() return speedIdx end, function(i) speedIdx = i end)
  root.blendButtons = toggleRow(root, "blend", BLENDS, -354,
    function() return blendIdx end, function(i) blendIdx = i end, 250)
  root.pulseButtons = toggleRow(root, "pulse", ENV_NAMES, -380,
    function() return pulseIdx end, function(i) pulseIdx = i end)
  root.depthButtons = toggleRow(root, "depth", DEPTH_NAMES, -380,
    function() return depthIdx end, function(i) depthIdx = i end, 300)
  root.breatheButtons = toggleRow(root, "breathe", ENV_NAMES, -406,
    function() return breatheIdx end, function(i) breatheIdx = i end)
  root.growButtons = toggleRow(root, "grow", GROWS, -406,
    function() return growIdx end, function(i) growIdx = i end, 300)
  root.dimButtons = toggleRow(root, "dim", DIM_NAMES, -432,
    function() return dimIdx end, function(i) dimIdx = i end)
  UI.button(root, "emph >", 66, 20, function()
    local n = applyDim()
    emphOrd = (n > 0) and (emphOrd % n + 1) or 1
    controlChanged()
  end):SetPoint("TOPLEFT", root, "TOPLEFT", 216, -432)
  root.motionButtons = toggleRow(root, "motion", MOTION_NAMES, -458,
    function() return motionIdx end, function(i) motionIdx = i end)
  root.grey = UI.button(root, "[ ] greyscale", 94, 20, function()
    greyOn = not greyOn
    controlChanged()
  end)
  root.grey:SetPoint("TOPLEFT", root, "TOPLEFT", 452, -458)

  local function note(y, height)
    local fs = root:CreateFontString(nil, "OVERLAY", "GameFontDisableSmall")
    fs:SetPoint("TOPLEFT", root, "TOPLEFT", 10, y)
    fs:SetPoint("TOPRIGHT", root, "TOPRIGHT", -10, y)
    fs:SetJustifyH("LEFT")
    fs:SetWordWrap(true)
    if height then fs:SetHeight(height) end
    return fs
  end
  root.envLine = note(-486, 46)
  root.caption = note(-534)
  root.cdmLine = note(-554)

  panel = root
  -- UIParent hiding fires this too, which is the case a close-button-only teardown misses.
  root:SetScript("OnHide", function()
    if panel.sample.painted and stop(panel.sample, panel.sample.painted, FOCUS_KEY) then
      panel.sample.painted = nil
    end
    if gridWindow then gridWindow:Hide() end
    G.ClearCDM()
    envStop()
  end)
  root:SetScript("OnShow", function()
    refreshCard()
    envRefresh()
  end)
  root:Hide()
  return root
end

function G.Toggle()
  if InCombatLockdown() and not panel then
    ns.Print("can't build the glow palette in combat — open it once out of combat, "
      .. "then it stays usable mid-pull.")
    return
  end
  panel = panel or build()
  if panel:IsShown() then
    panel:Hide()
    return false
  end
  panel:ClearAllPoints()
  panel:SetPoint("CENTER", UIParent, "CENTER", 0, -200)
  panel:Show()
  G.Select(candidates[index] and candidates[index].id)
  return true
end

-- Combat is the moment nobody is looking at the picker and a stranded glow on a Blizzard
-- frame becomes a bug report against the game. Item frames are POOLED, so a spec or
-- loadout change re-uses them for other abilities and would ride the glow across.
local watch = CreateFrame("Frame")
for _, e in ipairs({ "PLAYER_REGEN_DISABLED", "PLAYER_REGEN_ENABLED",
                     "PLAYER_SPECIALIZATION_CHANGED", "TRAIT_CONFIG_UPDATED" }) do
  pcall(watch.RegisterEvent, watch, e)
end
watch:SetScript("OnEvent", function(_, event)
  if event == "PLAYER_REGEN_ENABLED" then combatNoticed = false end
  if #painted == 0 then return end
  local _, held = G.ClearCDM()
  caption()
  if held > 0 then
    ns.Printf("|cffff8844%d painted frame(s) would not release|r — retried when combat ends.", held)
  end
end)

ns.Dumps.Register{
  id = "glow",
  label = "glow palette",
  blurb = function()
    return ("%d engines + %d atlases + %d registered"):format(
      #ENGINES, #ATLASES, #lib:GetGlowList())
  end,
  capture = function()
    local shown = G.Toggle()
    if shown == nil then return { "refused — the glow palette cannot be built in combat" } end
    return { shown and "opened the glow palette — next/prev steps the candidates, "
                    .. "[x] live on CDM repaints the real Cooldown Manager on every step"
                   or "closed the glow palette" }
  end,
}

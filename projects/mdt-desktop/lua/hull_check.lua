-- Runs MDT's OWN hull code over pull vertices and prints the outlines as JSON, so our
-- port can be checked against it rather than trusted.
--
-- This is the same move that validated the forces port — MDT's unmodified Modules/Pulls.lua
-- run over the same decoded pulls — applied to the geometry. Nothing here is edited: the
-- region sliced out of PullOutlines.lua is MDT's source verbatim, loaded as a chunk.
--
-- Usage:
--   mdtdesk pulls <route> --vertices | grep '^v ' | sed 's/^v //' > verts.txt
--   lua hull_check.lua <cache>/mdt/MythicDungeonTools/Modules/PullOutlines.lua < verts.txt
--
-- stdin  : one pull per line, vertices as `x,y,scale` separated by `;`, in MDT's own
--          coordinate space (y negative going down) — which is what `mdtdesk pulls
--          --vertices` prints on its `v` lines, and what getPullVertices collects.
-- stdout : a JSON array of outlines, each an array of [x, y].
--
-- ⚠ It is deliberately NOT an xunit test: it needs a populated dungeon cache and it slices
-- a file MDT can reshape at any release. It is a check you run, and whose result is
-- recorded in backlog.md.

local here = (arg[0] or ''):match('^(.*)[/\\][^/\\]*$') or '.'
package.path = here .. '/?.lua;' .. package.path
local json = require('json')

local path = arg[1]
if not path or path == '' then
  error('usage: hull_check.lua <path to MDT Modules/PullOutlines.lua>', 0)
end

local f = assert(io.open(path, 'rb'), 'could not open ' .. path)
local src = f:read('a')
f:close()

-- convex_hull and expand_polygon are file-locals, so the region holding them is sliced out
-- and re-exported. The bounds are comments either side of it, not line numbers, so an edit
-- above or below does not silently shift the slice.
local from = src:find('-- return true if a is more lower%-left than b')
local to = src:find('---TexturePool')
if not (from and to and to > from) then
  error('could not locate the hull functions in ' .. path .. ' — MDT may have moved them', 0)
end

local slice = src:sub(from, to - 1) ..
  '\nreturn { convex_hull = convex_hull, expand_polygon = expand_polygon }\n'

local mdt = assert(load(slice, 'PullOutlines-slice'))()

local outlines = {}
for line in io.read('a'):gmatch('[^\n]+') do
  local vertices = {}
  for triple in line:gmatch('[^;]+') do
    local x, y, scale = triple:match('([^,]+),([^,]+),([^,]+)')
    if x then vertices[#vertices + 1] = { tonumber(x), tonumber(y), tonumber(scale) } end
  end

  -- MDT's DrawHull pipeline exactly: hull, expand by 30, hull again.
  local hull = mdt.convex_hull(vertices)
  if hull then
    hull = mdt.expand_polygon(hull, 30)
    if hull then hull = mdt.convex_hull(hull) end
  end

  local out = {}
  for i = 1, (hull and #hull or 0) do out[#out + 1] = { hull[i][1], hull[i][2] } end
  outlines[#outlines + 1] = out
end

io.write(json.encode(outlines))

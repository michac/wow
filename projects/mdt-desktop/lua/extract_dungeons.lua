-- Reads MDT's shipped dungeon data with real Lua and emits it as JSON on stdout.
--
-- The data files are plain table literals wrapped in `local _, MDT = ...`, so all
-- they need is a stubbed `MDT` with the tables they assign into. Nothing here
-- parses Lua; the interpreter does that, which is the whole point of the sidecar.
--
-- Usage:  lua extract_dungeons.lua <addonDir>
--         <addonDir> is the extracted MythicDungeonTools folder — the one holding
--         Midnight/ and Locales/.
--
-- The output schema is DELIBERATELY NOT MDT's raw table layout. json.lua encodes a
-- dense 1..n table as an array and anything else as an object, which is right for
-- preserving MDT's data but means a table's JSON *shape* depends on its contents:
-- `enemies` is an array today and would silently become an object the day a dungeon
-- ships a sparse enemy index. So every collection is emitted as an array of objects
-- that carry their own `index`, which is stable whatever the data does.

local here = (arg[0] or ''):match('^(.*)[/\\][^/\\]*$') or '.'
package.path = here .. '/?.lua;' .. package.path

local json = require('json')

local ADDON_NAME = 'MythicDungeonTools'

local root = arg[1]
if not root or root == '' then
  error('usage: extract_dungeons.lua <addonDir>', 0)
end
root = root:gsub('[/\\]+$', '')

local function join(...)
  return table.concat({ ... }, '/')
end

local function read_file(path)
  local f = io.open(path, 'rb')
  if not f then return nil end
  local contents = f:read('a')
  f:close()
  return contents
end

-- `dofile` cannot pass varargs, and every MDT file starts `local _, MDT = ...`.
local function load_chunk(path, mdt)
  local chunk, err = loadfile(path)
  if not chunk then error('could not load ' .. path .. ': ' .. tostring(err), 0) end
  chunk(ADDON_NAME, mdt)
end

--------------------------------------------------------------------------------
-- The MDT stub
--------------------------------------------------------------------------------

local MDT = {
  AddonName = ADDON_NAME,
  L = {},
  dungeonList = {},
  mapInfo = {},
  dungeonMaps = {},
  dungeonSubLevels = {},
  dungeonTotalCount = {},
  dungeonEnemies = {},
  mapPOIs = {},
  zoneIdToDungeonIdx = {},
  scaleMultiplier = {},
}

-- Locales/enUS.lua does `local L = MDT.L; L = L or {}` and then assigns into it,
-- so loading it fills our table with the real English strings. The metatable is
-- attached AFTERWARDS: it makes an unknown key answer with itself, so a data file
-- referencing a string the locale forgot yields "AltarOfFangs" rather than nil.
local enUS = join(root, 'Locales', 'enUS.lua')
if read_file(enUS) then load_chunk(enUS, MDT) end
setmetatable(MDT.L, { __index = function(_, key) return key end })

-- load_midnight.xml is the load ORDER of record. Globbing is not available in
-- stock Lua anyway, and reading the manifest means a dungeon added upstream is
-- picked up without editing this script.
local manifest = read_file(join(root, 'Midnight', 'load_midnight.xml'))
if not manifest then
  error('no Midnight/load_midnight.xml under ' .. root, 0)
end

local files = {}
for file in manifest:gmatch('<Script%s+file%s*=%s*[\'"]([^\'"]+)[\'"]') do
  files[#files + 1] = file
end
if #files == 0 then error('load_midnight.xml listed no scripts', 0) end

for _, file in ipairs(files) do
  load_chunk(join(root, 'Midnight', file), MDT)
end

--------------------------------------------------------------------------------
-- Seasons
--------------------------------------------------------------------------------

-- MDT groups the dungeons into seasons itself, in Modules/DungeonSelect.lua, and that
-- grouping is EXTRACTED rather than hand-listed here — a season rotation upstream then
-- needs no edit on this side, the same principle load_midnight.xml already establishes
-- for the load order.
--
-- The file needs exactly three things beyond the MDT stub, measured against a live
-- release rather than guessed:
--   * `tinsert`   — a WoW client global, absent from stock Lua 5.4.
--   * `LibStub`   — line 2 calls it and only stores the result.
--   * MDT:IsRetail() answering true — it gates the whole do…end block.
-- Everything else in the file is function definitions that do not run at load.
local function extract_seasons()
  local path = join(root, 'Modules', 'DungeonSelect.lua')

  -- A non-retail or reshaped release must still extract. No seasons is a valid answer;
  -- failing to read the dungeons at all is not.
  if not read_file(path) then return {} end

  tinsert = table.insert
  LibStub = function() return {} end
  function MDT:IsRetail() return true end

  MDT.seasonList = {}
  MDT.dungeonSelectionToIndex = {}
  load_chunk(path, MDT)

  local seasons = {}
  for order, name in ipairs(MDT.seasonList) do
    -- Built densely so json.lua gives an array; MDT's own list already is one.
    local dungeons = {}
    for _, idx in ipairs(MDT.dungeonSelectionToIndex[order] or {}) do
      dungeons[#dungeons + 1] = idx
    end
    seasons[#seasons + 1] = { order = order, name = name, dungeons = dungeons }
  end
  return seasons
end

local seasons = extract_seasons()

--------------------------------------------------------------------------------
-- Reshaping
--------------------------------------------------------------------------------

local function sorted_keys(t, filter)
  local keys = {}
  for k in pairs(t) do
    if not filter or filter(k) then keys[#keys + 1] = k end
  end
  table.sort(keys)
  return keys
end

local function is_index(k)
  return math.type(k) == 'integer'
end

-- MDT stores the texture folder as a client path built from the addon name
-- (`Interface\AddOns\MythicDungeonTools\Midnight\Textures\AltarOfFangs`). The tail
-- is NOT derivable from the Lua file name — SeatoftheTriumvirate.lua points at
-- Textures\SeatOfTheTriumvirate — so it is read verbatim and only split, never
-- reconstructed.
local function texture_folder(customTextures)
  if type(customTextures) ~= 'string' then return nil end
  return (customTextures:gsub('[/\\]+$', ''):match('([^/\\]+)$'))
end

local function clone_out(index, clone)
  local patrol = {}
  for _, waypointIdx in ipairs(sorted_keys(clone.patrol or {}, is_index)) do
    local waypoint = clone.patrol[waypointIdx]
    patrol[#patrol + 1] = { index = waypointIdx, x = waypoint.x, y = waypoint.y }
  end

  return {
    index = index,
    x = clone.x,
    y = clone.y,
    sublevel = clone.sublevel,
    g = clone.g,
    scale = clone.scale,
    count = clone.count,          -- a per-clone forces override; 3 exist in shipped data
    patrol = #patrol > 0 and patrol or nil,
  }
end

-- MDT tags a spell with what you can DO about it. These are every flag it ships
-- (`grep` across Midnight/*.lua on 6.2.13: interruptible 133, magic 72, enrage 32,
-- poison 25, bleed 24, curse 10, disease 6) and they are what makes a mob's role
-- readable — an enemy with an interruptible spell is a caster, in the data, not by
-- guess. Only true flags are emitted; an absent key deserializes to false in C#.
local SPELL_FLAGS = {
  'interruptible', 'enrage', 'magic', 'curse', 'poison', 'disease', 'bleed',
}

local function spell_out(spellId, spell)
  local out = { id = spellId }
  for _, flag in ipairs(SPELL_FLAGS) do
    if spell[flag] then out[flag] = true end
  end
  return out
end

local function enemy_out(index, enemy)
  local clones = {}
  for _, cloneIdx in ipairs(sorted_keys(enemy.clones or {}, is_index)) do
    clones[#clones + 1] = clone_out(cloneIdx, enemy.clones[cloneIdx])
  end

  -- Built DENSELY, 1..n, so json.lua emits an array. Keying the outer table by
  -- spell id would make it a JSON object instead — the exact trap this file's
  -- header warns about, since spell ids are neither dense nor 1-based.
  local spells = {}
  for _, spellId in ipairs(sorted_keys(enemy.spells or {}, is_index)) do
    spells[#spells + 1] = spell_out(spellId, enemy.spells[spellId])
  end

  local characteristics = nil
  if enemy.characteristics then
    characteristics = sorted_keys(enemy.characteristics, function(k) return type(k) == 'string' end)
    if #characteristics == 0 then characteristics = nil end
  end

  return {
    index = index,
    name = enemy.name,
    id = enemy.id,
    count = enemy.count,
    health = enemy.health,
    scale = enemy.scale,
    displayId = enemy.displayId,
    creatureType = enemy.creatureType,
    level = enemy.level,
    isBoss = enemy.isBoss,
    encounterId = enemy.encounterID,
    instanceId = enemy.instanceID,
    stealth = enemy.stealth,
    stealthDetect = enemy.stealthDetect,
    spells = #spells > 0 and spells or nil,
    characteristics = characteristics,
    clones = clones,
  }
end

-- POI keys vary by `type` (dungeonEntrance / genericItem / genericAssignablePOI /
-- mapLink), so the shared fields are named and everything else rides along
-- untouched for the C# side to pick up as extension data.
local NAMED_POI_KEYS = { type = true, x = true, y = true }

local function poi_out(sublevel, index, poi)
  local out = {
    sublevel = sublevel,
    index = index,
    type = poi.type,
    x = poi.x,
    y = poi.y,
  }
  for _, key in ipairs(sorted_keys(poi, function(k) return type(k) == 'string' end)) do
    if not NAMED_POI_KEYS[key] then out[key] = poi[key] end
  end
  return out
end

local function dungeon_out(idx)
  local info = MDT.mapInfo[idx] or {}
  local maps = MDT.dungeonMaps[idx] or {}
  local names = MDT.dungeonSubLevels[idx] or {}

  -- dungeonMaps[idx][0] is a legacy slot, always "", and is not a sublevel.
  -- Sublevels are 1..#dungeonMaps-1 (Presets.lua:258-263).
  local subLevels = {}
  for sublevel = 1, #maps do
    local map = maps[sublevel]
    local custom = type(map) == 'table' and map.customTextures or nil
    subLevels[#subLevels + 1] = {
      index = sublevel,
      name = names[sublevel],
      customTextures = custom,
      textureFolder = texture_folder(custom),
    }
  end

  local enemies = {}
  for _, enemyIdx in ipairs(sorted_keys(MDT.dungeonEnemies[idx] or {}, is_index)) do
    enemies[#enemies + 1] = enemy_out(enemyIdx, MDT.dungeonEnemies[idx][enemyIdx])
  end

  local pois = {}
  for _, sublevel in ipairs(sorted_keys(MDT.mapPOIs[idx] or {}, is_index)) do
    for _, poiIdx in ipairs(sorted_keys(MDT.mapPOIs[idx][sublevel], is_index)) do
      pois[#pois + 1] = poi_out(sublevel, poiIdx, MDT.mapPOIs[idx][sublevel][poiIdx])
    end
  end

  local zoneIds = {}
  for zone, dungeonIdx in pairs(MDT.zoneIdToDungeonIdx) do
    if dungeonIdx == idx then zoneIds[#zoneIds + 1] = zone end
  end
  table.sort(zoneIds)

  return {
    index = idx,
    name = MDT.dungeonList[idx],
    englishName = info.englishName,
    shortName = info.shortName,
    mapId = info.mapID,
    teleportId = info.teleportId,
    iconId = info.iconId,
    totalCount = (MDT.dungeonTotalCount[idx] or {}).normal,
    zoneIds = zoneIds,
    subLevels = subLevels,
    enemies = enemies,
    pois = pois,
  }
end

--------------------------------------------------------------------------------
-- Output
--------------------------------------------------------------------------------

-- dungeonList carries placeholder "-" entries left over from an old dropdown, so
-- mapInfo is what says a dungeon is real.
local dungeons = {}
for _, idx in ipairs(sorted_keys(MDT.mapInfo, is_index)) do
  dungeons[#dungeons + 1] = dungeon_out(idx)
end

local toc = read_file(join(root, ADDON_NAME .. '.toc'))
local version = toc and toc:match('##%s*Version:%s*([^\r\n]+)')

io.write(json.encode({
  addonVersion = version and version:gsub('%s+$', '') or nil,
  interfaceVersion = toc and toc:match('##%s*Interface:%s*(%d+)') or nil,
  seasons = seasons,
  dungeons = dungeons,
}))

-- Minimal JSON *encoder*. Hand-rolled so the sidecar vendors nothing: no dkjson,
-- no lua-cjson, no build step. Encoding is all we ever need — C# does the reading.
--
-- Table shape rule: a table encodes as a JSON array ONLY when its keys are exactly
-- the consecutive integers 1..n. Anything else — a sparse array, a mixed table —
-- encodes as an object with stringified keys. That is deliberate and load-bearing:
-- MDT's dungeon indices are sparse (11, 17, 20, 42, 45, 150-155, 160-164) and its
-- pull tables mix integer enemy indices with the string key `color`. Coercing
-- either into a dense array would silently lose data.

local json = {}

local ESCAPES = {
  ['"'] = '\\"', ['\\'] = '\\\\', ['\b'] = '\\b', ['\f'] = '\\f',
  ['\n'] = '\\n', ['\r'] = '\\r', ['\t'] = '\\t',
}

local function escape_char(c)
  return ESCAPES[c] or string.format('\\u%04x', string.byte(c))
end

local function encode_string(s)
  return '"' .. s:gsub('[%z\1-\31\\"]', escape_char) .. '"'
end

local function encode_number(n)
  if n ~= n or n == math.huge or n == -math.huge then
    error('cannot encode non-finite number: ' .. tostring(n))
  end
  if math.type(n) == 'integer' then return string.format('%d', n) end
  -- %.14g round-trips a double without printing 17 digits of float noise.
  local s = string.format('%.14g', n)
  return s
end

-- Returns n when t is the dense array 1..n, otherwise nil.
local function array_length(t)
  local count, max = 0, 0
  for k in pairs(t) do
    if math.type(k) ~= 'integer' or k < 1 then return nil end
    count = count + 1
    if k > max then max = k end
  end
  if count ~= max then return nil end
  return max
end

local encode_value

local function encode_table(t, out, seen)
  if seen[t] then error('cannot encode a table that contains itself') end
  seen[t] = true

  local n = array_length(t)
  if n ~= nil then
    if n == 0 then out[#out + 1] = '[]'
    else
      out[#out + 1] = '['
      for i = 1, n do
        if i > 1 then out[#out + 1] = ',' end
        encode_value(t[i], out, seen)
      end
      out[#out + 1] = ']'
    end
  else
    -- Sort keys so output is byte-stable: a cache file that reshuffles on every
    -- regeneration is useless to diff.
    local keys = {}
    for k in pairs(t) do
      local kt = type(k)
      if kt ~= 'string' and kt ~= 'number' then
        error('cannot encode table key of type ' .. kt)
      end
      keys[#keys + 1] = k
    end
    table.sort(keys, function(a, b)
      if type(a) == type(b) then return a < b end
      return type(a) == 'number'
    end)

    out[#out + 1] = '{'
    for i, k in ipairs(keys) do
      if i > 1 then out[#out + 1] = ',' end
      out[#out + 1] = encode_string(type(k) == 'number' and encode_number(k) or k)
      out[#out + 1] = ':'
      encode_value(t[k], out, seen)
    end
    out[#out + 1] = '}'
  end

  seen[t] = nil
end

encode_value = function(v, out, seen)
  local t = type(v)
  if v == nil then out[#out + 1] = 'null'
  elseif t == 'boolean' then out[#out + 1] = v and 'true' or 'false'
  elseif t == 'number' then out[#out + 1] = encode_number(v)
  elseif t == 'string' then out[#out + 1] = encode_string(v)
  elseif t == 'table' then encode_table(v, out, seen)
  else error('cannot encode value of type ' .. t)
  end
end

function json.encode(value)
  local out = {}
  encode_value(value, out, {})
  return table.concat(out)
end

return json

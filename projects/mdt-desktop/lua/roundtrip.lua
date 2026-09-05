-- The M0 spike: prove the sidecar contract end to end. Text in on stdin,
-- arguments in `...`, JSON out on stdout, and a traceback on stderr when asked
-- to fail. It stays in the tree as the LuaRunner smoke test.

local here = (arg[0] or ''):match('^(.*)[/\\][^/\\]*$') or '.'
package.path = here .. '/?.lua;' .. package.path

local json = require('json')

local args = {}
for i = 1, #arg do args[i] = arg[i] end

if args[1] == 'fail' then
  error('roundtrip.lua was asked to fail')
end

local stdin = io.read('a') or ''

io.write(json.encode({
  lua = _VERSION,
  args = args,
  stdin = stdin,
  stdinBytes = #stdin,
}))

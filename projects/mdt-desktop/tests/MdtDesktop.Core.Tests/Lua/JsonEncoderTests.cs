using MdtDesktop.Core.Lua;

namespace MdtDesktop.Core.Tests.Lua;

/// <summary>
/// Exercises <c>lua/json.lua</c> through the sidecar. Its table-shape rule is
/// load-bearing for M1 and M2 — MDT's dungeon indices are sparse and its pull
/// tables mix integer enemy indices with the string key <c>color</c> — so the
/// rule is pinned here rather than left to be discovered by a wrong map.
/// </summary>
public class JsonEncoderTests
{
    private static async Task<string> EncodeAsync(string luaExpression)
    {
        var source = $"""
            package.path = {ToLuaString(LuaInterpreter.ScriptDirectory)} .. '/?.lua;' .. package.path
            io.write(require('json').encode({luaExpression}))
            """;

        return await new LuaRunner().RunSourceAsync(source);
    }

    private static string ToLuaString(string s) => "'" + s.Replace("\\", "\\\\").Replace("'", "\\'") + "'";

    [Fact]
    public async Task A_dense_one_based_table_is_an_array()
        => Assert.Equal("[10,20,30]", await EncodeAsync("{10, 20, 30}"));

    [Fact]
    public async Task A_sparse_integer_table_is_an_object_keyed_by_index()
    {
        // MDT's real dungeon indices. Losing the index would misfile every dungeon.
        Assert.Equal("""{"11":"a","164":"b"}""", await EncodeAsync("""{[11] = 'a', [164] = 'b'}"""));
    }

    [Fact]
    public async Task A_mixed_table_keeps_both_the_integer_keys_and_the_string_ones()
    {
        // The shape of a pull: enemy indices plus `color`.
        Assert.Equal("""{"3":[1,2],"7":[1],"color":"228b22"}""",
            await EncodeAsync("""{[3] = {1, 2}, [7] = {1}, color = '228b22'}"""));
    }

    [Fact]
    public async Task Object_keys_are_sorted_so_the_cache_file_diffs()
        => Assert.Equal("""{"a":1,"b":2,"c":3}""", await EncodeAsync("{c = 3, a = 1, b = 2}"));

    [Fact]
    public async Task Integers_and_floats_are_distinguished()
    {
        // Coordinates are floats; counts and ids are integers. `1` must not become `1.0`.
        Assert.Equal("""{"count":4,"x":830.73,"y":-550.48}""",
            await EncodeAsync("{count = 4, x = 830.73, y = -550.48}"));
    }

    [Fact]
    public async Task Control_characters_and_quotes_are_escaped()
        => Assert.Equal(""" "a\"b\nc\td\u0001" """.Trim(),
            await EncodeAsync("""'a\"b\nc\td\1'"""));

    [Fact]
    public async Task Booleans_and_nested_tables_survive()
        => Assert.Equal("""{"clones":[{"x":1.5}],"isBoss":true}""",
            await EncodeAsync("{isBoss = true, clones = {{x = 1.5}}}"));
}

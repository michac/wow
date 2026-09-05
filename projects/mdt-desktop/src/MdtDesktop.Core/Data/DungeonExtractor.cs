using System.Text.Json;
using MdtDesktop.Core.Lua;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Data;

/// <summary>
/// Reads MDT's dungeon data out of an extracted release, by running it as Lua.
/// </summary>
/// <remarks>
/// MDT's data files are Lua, so they are read by Lua — <c>lua/extract_dungeons.lua</c> stubs
/// the handful of <c>MDT.*</c> tables they assign into, loads them, and writes JSON. Nothing
/// on this side parses Lua.
/// </remarks>
public sealed class DungeonExtractor(LuaRunner? runner = null)
{
    public const string ScriptName = "extract_dungeons.lua";

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
    };

    private readonly LuaRunner _runner = runner ?? new LuaRunner();

    /// <summary>Runs the sidecar over <paramref name="addonDirectory"/> and returns its JSON.</summary>
    public async Task<string> ExtractJsonAsync(string addonDirectory, CancellationToken ct = default)
    {
        if (!Directory.Exists(addonDirectory))
            throw new DataUpdateException($"No extracted MDT release at {addonDirectory}.");

        return await _runner.RunAsync(
            LuaInterpreter.Script(ScriptName),
            args: [addonDirectory],
            ct: ct).ConfigureAwait(false);
    }

    /// <summary>Runs the sidecar and deserializes the result.</summary>
    public async Task<DungeonData> ExtractAsync(string addonDirectory, CancellationToken ct = default)
        => Parse(await ExtractJsonAsync(addonDirectory, ct).ConfigureAwait(false));

    public static DungeonData Parse(string json)
        => JsonSerializer.Deserialize<DungeonData>(json, JsonOptions)
           ?? throw new DataUpdateException("The extractor produced no dungeon data.");

    public static DungeonData Load(string path)
        => Parse(File.ReadAllText(path));
}

using System.Text.Json;
using System.Text.Json.Serialization;

namespace MdtDesktop.Core.Data;

/// <summary>
/// Where the runtime data lives: the extracted MDT release, the dungeon cache, and the
/// stamp recording which release they came from.
/// </summary>
/// <remarks>
/// None of this is in the repo — it is ~18 MB of map tiles and it is re-derivable from
/// the network. The root is resolved through <see cref="Environment.SpecialFolder.LocalApplicationData"/>
/// rather than a literal <c>%LOCALAPPDATA%</c>, which is what lets the whole update path be
/// exercised from WSL (where it lands in <c>~/.local/share</c>) instead of only on Windows.
/// </remarks>
public sealed class DataCache
{
    public const string CacheFolderName = "MdtDesktop";

    public DataCache(string? root = null)
        => Root = root ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            CacheFolderName);

    public string Root { get; }

    /// <summary>Where the release zip is unpacked. Holds a single <c>MythicDungeonTools/</c> folder.</summary>
    public string ReleaseDirectory => Path.Combine(Root, "mdt");

    /// <summary>The extracted addon folder itself — what the sidecar script is pointed at.</summary>
    public string AddonDirectory => Path.Combine(ReleaseDirectory, "MythicDungeonTools");

    public string DungeonsJsonPath => Path.Combine(Root, "dungeons.json");

    public string VersionJsonPath => Path.Combine(Root, "version.json");

    /// <summary>Absolute path of a sublevel's tile directory, from its <c>TextureFolder</c>.</summary>
    public string TextureDirectory(string textureFolder)
        => Path.Combine(AddonDirectory, "Midnight", "Textures", textureFolder);

    public void EnsureRoot() => Directory.CreateDirectory(Root);

    public CacheStamp? ReadStamp()
    {
        if (!File.Exists(VersionJsonPath)) return null;
        try
        {
            return JsonSerializer.Deserialize<CacheStamp>(
                File.ReadAllText(VersionJsonPath), CacheStamp.JsonOptions);
        }
        catch (JsonException)
        {
            // A half-written stamp means "no usable cache", which is what a null says.
            return null;
        }
    }

    public void WriteStamp(CacheStamp stamp)
    {
        EnsureRoot();
        File.WriteAllText(VersionJsonPath, JsonSerializer.Serialize(stamp, CacheStamp.JsonOptions));
    }
}

/// <summary>Which MDT release the cache was built from, and what came out of it.</summary>
/// <param name="SchemaVersion">
/// The shape <c>dungeons.json</c> was written in. Defaults to 0, which is what an older stamp
/// deserializes to, so a cache from before a schema change is correctly refused.
/// </param>
public sealed record CacheStamp(
    string Tag,
    string? AddonVersion,
    string? InterfaceVersion,
    DateTimeOffset UpdatedUtc,
    int DungeonCount,
    int EnemyCount,
    int CloneCount,
    int SchemaVersion = 0)
{
    /// <summary>
    /// The schema <c>lua/extract_dungeons.lua</c> emits today. Bump it whenever the emitted
    /// shape changes.
    /// </summary>
    /// <remarks>
    /// ⚠ This exists because the failure it prevents is <b>silent</b>. Version 2 replaced
    /// <c>spellIds: [1,2,3]</c> with <c>spells: [{id, flags…}]</c>; a version-1 cache
    /// deserializes against the new model without error, leaving every enemy with an empty
    /// spell list — so every mob classifies as melee, the caster count reads zero, and nothing
    /// anywhere says why. Refusing the old cache turns that into the message every call site
    /// already handles: "run `mdtdesk data update` first".
    /// <para>
    /// Version 3 added <c>seasons</c>, and it is the same failure again: a version-2 cache
    /// deserializes with <c>Seasons</c> empty, so every dungeon falls into the synthetic "Other"
    /// group and the season picker reads as though MDT stopped shipping seasons. A widening is
    /// exactly the change that degrades silently, which is why every one of them bumps this.
    /// </para>
    /// </remarks>
    public const int CurrentSchemaVersion = 3;

    /// <summary>Whether this stamp describes a cache the current code can read.</summary>
    public bool IsCurrentSchema => SchemaVersion == CurrentSchemaVersion;

    internal static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };
}

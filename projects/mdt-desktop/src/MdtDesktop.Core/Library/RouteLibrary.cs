using System.Text.Json;
using System.Text.Json.Serialization;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Library;

/// <summary>
/// The local route library: import a string once, find it again next launch.
/// </summary>
/// <remarks>
/// <para>
/// ⚠ This lives under <see cref="Environment.SpecialFolder.ApplicationData"/>, deliberately
/// <b>not</b> beside the dungeon cache. The cache is derived data and deleting it is a
/// documented recovery step; saved routes are user data and are not re-derivable from anything.
/// Keeping them apart is what stops "clear the cache" eating the library.
/// </para>
/// <para>
/// One JSON file per route, so a corrupt or hand-edited entry costs one route rather than all of
/// them, and the whole library can be managed with a file browser.
/// </para>
/// <para>
/// The app stays read-only toward MDT and the game: it authors no routes and writes nothing back.
/// This writes only our own record of what you imported.
/// </para>
/// </remarks>
public sealed class RouteLibrary
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };

    public RouteLibrary(string? root = null)
        => Root = root ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "MdtDesktop", "routes");

    public string Root { get; }

    /// <summary>Every saved route, newest import first.</summary>
    public IReadOnlyList<SavedRoute> List()
    {
        if (!Directory.Exists(Root)) return [];

        var routes = new List<SavedRoute>();
        foreach (var file in Directory.EnumerateFiles(Root, "*.json"))
        {
            if (TryRead(file) is { } route) routes.Add(route);
            // A file that will not parse is skipped rather than fatal: one bad entry must not
            // make the whole library unreadable.
        }

        return [.. routes.OrderByDescending(r => r.ImportedUtc)];
    }

    public SavedRoute? Find(string id)
        => File.Exists(PathFor(id)) ? TryRead(PathFor(id)) : null;

    /// <summary>
    /// Decodes <paramref name="routeString"/> and saves it, stamping the dungeon's mapping hash.
    /// </summary>
    /// <param name="dungeon">
    /// The route's dungeon from the current cache. When null the route is still saved, but with
    /// no mapping hash — so a later re-map cannot be detected for it.
    /// </param>
    public SavedRoute Save(
        string routeString, Dungeon? dungeon, string? mdtVersion = null, string? name = null)
    {
        var route = RouteDecoder.Decode(routeString);

        var saved = new SavedRoute
        {
            Id = MakeId(route, routeString),
            RouteString = routeString.Trim(),
            Name = name ?? route.Name,
            DungeonIndex = route.DungeonIndex,
            DungeonName = dungeon?.DisplayName,
            PullCount = route.Pulls.Count,
            ImportedUtc = DateTimeOffset.UtcNow,
            ImportedUnderMdtVersion = mdtVersion,
            DungeonMappingHash = dungeon is null ? null : MappingHash.Compute(dungeon),
            AddonVersion = route.AddonVersion,
        };

        Directory.CreateDirectory(Root);
        File.WriteAllText(PathFor(saved.Id), JsonSerializer.Serialize(saved, JsonOptions));
        return saved;
    }

    public bool Remove(string id)
    {
        var path = PathFor(id);
        if (!File.Exists(path)) return false;
        File.Delete(path);
        return true;
    }

    /// <summary>
    /// Whether the route's dungeon has been re-mapped since it was imported.
    /// </summary>
    /// <returns>
    /// Null when it cannot be told — no hash was recorded, or the dungeon is not in the cache.
    /// Null is <b>not</b> "unchanged", and must not be reported as reassurance.
    /// </returns>
    public static bool? HasDungeonChangedSinceImport(SavedRoute saved, Dungeon? dungeon)
        => saved.DungeonMappingHash is null || dungeon is null
            ? null
            : MappingHash.Compute(dungeon) != saved.DungeonMappingHash;

    private string PathFor(string id) => Path.Combine(Root, id + ".json");

    private static SavedRoute? TryRead(string path)
    {
        try { return JsonSerializer.Deserialize<SavedRoute>(File.ReadAllText(path), JsonOptions); }
        catch (JsonException) { return null; }
        catch (IOException) { return null; }
    }

    /// <summary>
    /// MDT's <c>uid</c> when there is one, so re-importing an updated copy of the same route
    /// replaces it rather than piling up duplicates — which is exactly what keystone.guru
    /// intends by emitting a stable uid ("so multiple imports overwrite eachother").
    /// </summary>
    private static string MakeId(Route route, string routeString)
    {
        var uid = Sanitize(route.Uid);
        if (!string.IsNullOrEmpty(uid)) return uid;

        // No uid: fall back to a hash of the string, so saving the same string twice is still
        // idempotent.
        var digest = System.Security.Cryptography.SHA256.HashData(
            System.Text.Encoding.UTF8.GetBytes(routeString.Trim()));
        return "r" + Convert.ToHexStringLower(digest)[..15];
    }

    private static string Sanitize(string? value)
    {
        if (string.IsNullOrWhiteSpace(value)) return "";
        var clean = new string([.. value.Where(c => char.IsAsciiLetterOrDigit(c) || c is '-' or '_')]);
        return clean.Length > 64 ? clean[..64] : clean;
    }
}

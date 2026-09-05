using System.Text.Json.Serialization;

namespace MdtDesktop.Core.Library;

/// <summary>
/// One route kept in the local library, so it survives closing the app.
/// </summary>
/// <remarks>
/// The verbatim <see cref="RouteString"/> is the source of truth — everything else is a decoded
/// convenience that lets the library be listed without the dungeon cache being present, and can
/// always be rebuilt by decoding the string again.
/// </remarks>
public sealed record SavedRoute
{
    /// <summary>Filesystem-safe id. MDT's <c>uid</c> when the string carries one.</summary>
    public required string Id { get; init; }

    /// <summary>The route string exactly as imported.</summary>
    public required string RouteString { get; init; }

    /// <summary>The route's own name, or one the user gave it.</summary>
    public string? Name { get; init; }

    public int DungeonIndex { get; init; }

    /// <summary>Cached so a listing needs no dungeon data.</summary>
    public string? DungeonName { get; init; }

    public int PullCount { get; init; }

    public DateTimeOffset ImportedUtc { get; init; }

    /// <summary>The MDT release the dungeon cache was on when this was imported.</summary>
    public string? ImportedUnderMdtVersion { get; init; }

    /// <summary>
    /// <see cref="Model.MappingHash"/> of the route's dungeon at import time.
    /// </summary>
    /// <remarks>
    /// The point of the library, beyond not re-pasting: with this recorded, a later MDT update
    /// that re-maps the dungeon becomes detectable exactly, for routes that carry no
    /// <c>addonVersion</c> of their own — which is most of them.
    /// </remarks>
    public string? DungeonMappingHash { get; init; }

    /// <summary>The exporting MDT build, when the string declared one.</summary>
    public int? AddonVersion { get; init; }

    [JsonIgnore]
    public string DisplayName => Name ?? Id;
}

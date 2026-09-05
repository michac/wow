using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Routes;

/// <summary>
/// Flags a decoded route that looks like it predates a change to MDT's dungeon data.
/// </summary>
/// <remarks>
/// <para>
/// A route stores enemy and clone <i>indices</i>, nothing that identifies the mobs. When MDT
/// re-maps a dungeon, an old route still decodes cleanly and still counts — against whatever
/// now sits at those indices. That is the one silent failure mode of a route viewer, and it is
/// not rare: MDT corrected Altar of Fangs' enemy data in 6.2.2 and again in 6.2.8, and revised
/// several dungeons' <i>total</i> forces along the way (Temple of Sethraliss went 649 → 689 →
/// 649 → 687 in five weeks).
/// </para>
/// <para>
/// There is <b>one</b> exact signal, when it is present: <see cref="Route.AddonVersion"/>, the
/// MDT build that exported the route. A route exported by an older MDT than the cached data was
/// drawn against different dungeon data, full stop — no heuristic needed. It is often absent
/// though (MDT's party-share path and keystone.guru's exporter both omit it), and even when
/// present it says only that MDT moved, not whether <i>this</i> dungeon did.
/// </para>
/// <para>
/// ⚠ Otherwise these are heuristics and cannot be anything else. MDT stamps no version on a
/// dungeon's data, so there is nothing to compare against. keystone.guru gets this right by
/// content-hashing MDT's mapping per dungeon and minting a new mapping version when the hash
/// changes, then storing each route against the version it was authored on — a database can do
/// that; a pasted string cannot. So: warn, name the reason, and never silently "correct" anything.
/// </para>
/// </remarks>
public static class RouteHealth
{
    /// <param name="importedMappingHash">
    /// The dungeon's <see cref="MappingHash"/> when this route was saved to the library, if it
    /// came from there. This is the strongest signal available — it is exact, it is per-dungeon
    /// rather than per-MDT-release, and unlike <see cref="Route.AddonVersion"/> it works for the
    /// many strings that declare nothing about their own provenance.
    /// </param>
    public static IReadOnlyList<RouteWarning> Check(
        Route route, Dungeon dungeon, IReadOnlyList<PullForces> forces, string? mdtVersion = null,
        string? importedMappingHash = null)
    {
        var warnings = new List<RouteWarning>();
        var version = mdtVersion is null ? "the current MDT data" : $"MDT {mdtVersion}";

        // The best signal, when the route came from our own library: we recorded what the
        // dungeon looked like at import, so this is an exact per-dungeon comparison.
        if (importedMappingHash is not null && MappingHash.Compute(dungeon) != importedMappingHash)
            warnings.Add(new RouteWarning(
                RouteWarningKind.DungeonRemappedSinceImport,
                $"{dungeon.DisplayName} has been re-mapped since this route was imported. " +
                "Its enemy and clone indices may now point at different mobs."));

        // The one exact check the string itself can offer, when the exporter stamped it.
        var cached = PackVersion(mdtVersion);
        if (route.AddonVersion is { } exported && cached is { } current && exported < current)
            warnings.Add(new RouteWarning(
                RouteWarningKind.ExportedByOlderMdt,
                $"The route was exported by MDT {FormatPacked(exported)}, older than the cached " +
                $"{version}. Its enemy and clone indices were drawn against that build's data."));

        var unresolved = forces.Sum(f => f.Unresolved.Count);
        if (unresolved > 0)
            warnings.Add(new RouteWarning(
                RouteWarningKind.UnresolvedReferences,
                $"{unresolved} enemy/clone reference(s) do not exist in {version}. " +
                "The route was drawn against different dungeon data."));

        var total = forces.Count > 0 ? forces[^1].Cumulative : 0;
        if (dungeon.TotalCount > 0 && total < dungeon.TotalCount)
        {
            var percent = 100.0 * total / dungeon.TotalCount;
            warnings.Add(new RouteWarning(
                RouteWarningKind.CannotReachFullForces,
                $"The route totals {total}/{dungeon.TotalCount} ({percent:F2}%) and so cannot " +
                "complete the dungeon. A published route normally reaches 100%, so this one most " +
                $"likely predates a correction to {version} — the indices it names may now point " +
                "at different enemies."));
        }

        return warnings;
    }

    /// <summary>
    /// "6.2.13" -> 6213, matching how MDT packs it (<c>GetAddOnMetadata(…):gsub("%.", "")</c>).
    /// </summary>
    private static int? PackVersion(string? version)
        => version is not null && int.TryParse(version.Replace(".", ""), out var packed)
            ? packed
            : null;

    /// <summary>Best-effort inverse, for a readable message. 6213 -> "6.2.13".</summary>
    private static string FormatPacked(int packed)
    {
        var digits = packed.ToString();
        return digits.Length >= 3
            ? $"{digits[0]}.{digits[1]}.{digits[2..]}"
            : digits;
    }
}

public sealed record RouteWarning(RouteWarningKind Kind, string Message)
{
    public override string ToString() => Message;
}

public enum RouteWarningKind
{
    /// <summary>The dungeon's mapping has changed since this route was saved to the library.</summary>
    DungeonRemappedSinceImport,

    /// <summary>The route string names an MDT build older than the cached dungeon data.</summary>
    ExportedByOlderMdt,

    /// <summary>The route names enemies or clones that are no longer in the data.</summary>
    UnresolvedReferences,

    /// <summary>The route's forces fall short of the dungeon requirement.</summary>
    CannotReachFullForces,
}

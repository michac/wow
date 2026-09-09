namespace MdtDesktop.Core.Library;

/// <summary>
/// Which saved route a dungeon should open with.
/// </summary>
/// <remarks>
/// <para>
/// It is here rather than in the window's code-behind because it is the part that was
/// <b>wrong</b>, and code-behind cannot be tested. The bug it pins: the route picker used to be
/// filtered by nothing and loaded only from WPF's <c>SelectionChanged</c>, so switching dungeon
/// and back left the picker still displaying a route that was no longer loaded — and re-picking
/// it raised no event, because it was already the selected item. The route was unrecoverable
/// without picking a different one first.
/// </para>
/// <para>
/// The fix is that the decision is a function, called directly, rather than something that
/// happens as a side effect of an event the framework may or may not raise.
/// </para>
/// </remarks>
public static class RouteSelection
{
    /// <summary>Every saved route drawn on a given dungeon, in library order.</summary>
    public static IReadOnlyList<SavedRoute> For(IReadOnlyList<SavedRoute> library, int dungeonIndex)
        => [.. library.Where(r => r.DungeonIndex == dungeonIndex)];

    /// <summary>
    /// The route to load for <paramref name="dungeonIndex"/>, or null for "no route".
    /// </summary>
    /// <param name="pendingId">
    /// A route the user just named — imported, or picked in the dropdown. It wins outright:
    /// it is the only id that reflects an action taken this second.
    /// </param>
    /// <param name="rememberedId">
    /// The route last loaded for this dungeon, from settings. Used when nothing is pending,
    /// which is what makes switching away and back come back to the same route.
    /// </param>
    /// <remarks>
    /// An id naming a route that is not in this dungeon's list — removed from the library, or
    /// belonging to another dungeon — falls through to the next rule rather than to nothing.
    /// </remarks>
    public static SavedRoute? Choose(
        IReadOnlyList<SavedRoute> library, int dungeonIndex,
        string? pendingId, string? rememberedId)
    {
        var candidates = For(library, dungeonIndex);
        if (candidates.Count == 0) return null;

        return Match(candidates, pendingId) ?? Match(candidates, rememberedId);
    }

    private static SavedRoute? Match(IReadOnlyList<SavedRoute> candidates, string? id)
        => id is { Length: > 0 }
            ? candidates.FirstOrDefault(r => string.Equals(r.Id, id, StringComparison.Ordinal))
            : null;
}

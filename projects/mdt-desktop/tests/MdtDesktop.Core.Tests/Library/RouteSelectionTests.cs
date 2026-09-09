using MdtDesktop.Core.Library;

namespace MdtDesktop.Core.Tests.Library;

/// <summary>
/// Which route a dungeon opens with.
/// </summary>
/// <remarks>
/// This decision moved out of the window's code-behind because it is the part that was wrong and
/// code-behind cannot be tested. The reported bug is the first test here: load a route, switch
/// dungeons, switch back, and the route was gone with no way to get it back short of picking a
/// different one first.
/// </remarks>
public class RouteSelectionTests
{
    private static SavedRoute Route(string id, int dungeon)
        => new() { Id = id, RouteString = "!~MDT2~", DungeonIndex = dungeon, Name = id };

    private static readonly IReadOnlyList<SavedRoute> Library =
    [
        Route("a1", 164),
        Route("a2", 164),
        Route("b1", 160),
    ];

    // ---- the reported bug -------------------------------------------------------------------

    /// <summary>
    /// ⚠ The whole point. Dungeon A with route R, switch to B, switch back to A — R comes back,
    /// without the user touching the route dropdown.
    /// </summary>
    [Fact]
    public void Switching_away_and_back_returns_the_same_route()
    {
        // On A the user picks a2, and that is what gets remembered for A.
        var picked = RouteSelection.Choose(Library, 164, pendingId: "a2", rememberedId: null);
        Assert.Equal("a2", picked!.Id);

        // Over on B nothing is pending and nothing was ever loaded there.
        Assert.Null(RouteSelection.Choose(Library, 160, null, rememberedId: null));

        // Back on A, from the remembered id alone.
        Assert.Equal("a2", RouteSelection.Choose(Library, 164, null, rememberedId: "a2")!.Id);
    }

    // ---- precedence -------------------------------------------------------------------------

    [Fact]
    public void A_pending_route_beats_the_remembered_one()
    {
        // What the user did this second wins over what they did last time.
        Assert.Equal("a1", RouteSelection.Choose(Library, 164, "a1", "a2")!.Id);
    }

    [Fact]
    public void With_nothing_pending_the_remembered_route_is_used()
        => Assert.Equal("a2", RouteSelection.Choose(Library, 164, null, "a2")!.Id);

    [Fact]
    public void With_neither_it_chooses_no_route()
        => Assert.Null(RouteSelection.Choose(Library, 164, null, null));

    /// <summary>An empty library has nothing to choose, and says so rather than inventing one.</summary>
    [Fact]
    public void An_empty_library_yields_null()
        => Assert.Null(RouteSelection.Choose([], 164, "a1", "a2"));

    // ---- ids that no longer resolve ---------------------------------------------------------

    /// <summary>A remembered route since removed from the library falls through, not to a crash.</summary>
    [Fact]
    public void A_remembered_id_that_is_gone_yields_no_route()
        => Assert.Null(RouteSelection.Choose(Library, 164, null, "deleted"));

    /// <summary>
    /// A route belonging to another dungeon is not a candidate here — which is exactly what the
    /// unfiltered picker used to get wrong.
    /// </summary>
    [Fact]
    public void A_route_for_another_dungeon_is_never_chosen()
    {
        Assert.Null(RouteSelection.Choose(Library, 164, "b1", null));
        Assert.Equal(["b1"], RouteSelection.For(Library, 160).Select(r => r.Id));
    }

    [Fact]
    public void The_candidate_list_is_the_dungeons_own_routes_in_library_order()
        => Assert.Equal(["a1", "a2"], RouteSelection.For(Library, 164).Select(r => r.Id));

    [Fact]
    public void A_dungeon_with_no_routes_has_an_empty_candidate_list()
        => Assert.Empty(RouteSelection.For(Library, 999));
}

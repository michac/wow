using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;
using MdtDesktop.Core.Tests.Data;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The seam WPF draws. Everything asserted here is a decision <c>MapView</c> is not allowed to
/// make for itself, which is the whole reason it lives in <c>Core</c> — none of it can be seen
/// on this machine, so all of it has to be provable.
/// </summary>
/// <remarks>
/// The fixture dungeon (index 4242, 100 forces): enemy 1 at 5 forces with clones 1 and 3 (clone
/// 3 overrides to 42), enemy 2 at 3 forces with clone 1, enemy 3 the boss at 0 with clone 1.
/// </remarks>
public class RouteOverlayTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        var data = await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
        return data.ByIndex[4242];
    }

    private static Route RouteOf(params Pull[] pulls)
        => new() { DungeonIndex = 4242, Pulls = pulls };

    private static Pull PullOf(int number, string? color, params (int Enemy, int[] Clones)[] enemies)
        => new()
        {
            Number = number,
            Color = color,
            Enemies = [.. enemies.Select(e => new PullEnemy(e.Enemy, e.Clones))],
        };

    // ---- the current pull ----------------------------------------------------------------

    /// <summary>
    /// MDT's own answer: <c>NONACTIVE_ALPHA = 0.5</c> (<c>PullOutlines.lua:4</c>). Taking it
    /// rather than inventing an emphasis channel is the point.
    /// </summary>
    [Fact]
    public async Task The_current_pull_draws_solid_and_the_rest_at_MDTs_own_half_alpha()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1])), PullOf(2, null, (2, [1]))),
            await FixtureDungeonAsync(), subLevel: 1, currentPull: 2);

        Assert.Equal(RouteOverlay.NonActiveAlpha, overlay.Pulls[0].Alpha);
        Assert.False(overlay.Pulls[0].IsCurrent);

        Assert.Equal(1, overlay.Pulls[1].Alpha);
        Assert.True(overlay.Pulls[1].IsCurrent);
        Assert.Equal(2, overlay.Current!.Number);
    }

    [Fact]
    public async Task A_cursor_past_the_end_of_the_route_has_no_current_pull_rather_than_throwing()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, currentPull: 99);

        Assert.Null(overlay.Current);
        Assert.All(overlay.Pulls, p => Assert.False(p.IsCurrent));
    }

    // ---- colour ---------------------------------------------------------------------------

    [Fact]
    public async Task A_pull_with_no_colour_gets_MDTs_sentinel_rather_than_null()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        Assert.Equal(Pull.DefaultColor, overlay.Pulls[0].Color);
        // …and it is flagged as not-a-choice, so the UI can tell "green" from "unset green".
        Assert.False(overlay.Pulls[0].HasCustomColor);
    }

    [Fact]
    public async Task A_chosen_colour_is_carried_through_and_marked_as_chosen()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "ff8800", (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        Assert.Equal("ff8800", overlay.Pulls[0].Color);
        Assert.True(overlay.Pulls[0].HasCustomColor);
    }

    [Theory]
    [InlineData("ff8800", 0xFF, 0x88, 0x00)]
    [InlineData("#228B22", 0x22, 0x8B, 0x22)]
    public void A_hex_colour_parses_to_bytes(string hex, byte r, byte g, byte b)
        => Assert.Equal((r, g, b), RouteOverlay.ParseColor(hex));

    /// <summary>A draw loop must not throw over a colour, so junk falls back rather than failing.</summary>
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("red")]
    [InlineData("ff88")]
    [InlineData("gghhii")]
    public void Junk_in_the_colour_field_parses_to_nothing_rather_than_throwing(string? hex)
        => Assert.Null(RouteOverlay.ParseColor(hex));

    // ---- which mob belongs to which pull ---------------------------------------------------

    /// <summary>
    /// This dictionary is the coexistence rule in one line: a mob in it wears its pull's colour,
    /// a mob absent from it wears its role colour. MDT does exactly this — it tints assigned
    /// blips and resets unassigned ones (<c>DungeonEnemies.lua:962,983</c>).
    /// </summary>
    [Fact]
    public async Task A_mob_in_a_pull_is_keyed_to_it_and_a_mob_in_none_is_absent()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "ff8800", (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        var claimed = overlay.RoleByMob[(1, 1)];
        Assert.Equal(1, claimed.PullNumber);
        Assert.Equal("ff8800", claimed.Color);
        Assert.True(claimed.IsCurrent);

        // Enemy 1 clone 3 and the boss are in no pull, so nothing claims them.
        Assert.False(overlay.RoleByMob.ContainsKey((1, 3)));
        Assert.False(overlay.RoleByMob.ContainsKey((3, 1)));
    }

    /// <summary>A blip can only be one colour, so a mob named twice belongs to the earlier pull.</summary>
    [Fact]
    public async Task A_mob_named_by_two_pulls_is_claimed_by_the_first()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "aa0000", (1, [1])), PullOf(2, "00aa00", (1, [1]))),
            await FixtureDungeonAsync(), 1, 1);

        Assert.Equal(1, overlay.RoleByMob[(1, 1)].PullNumber);
    }

    /// <summary>
    /// MDT 6.2.13 deleted a clone a 6.2.12 route can still name. It is skipped in the geometry
    /// for the same reason <c>RouteForces</c> skips it in the arithmetic — and reported there.
    /// </summary>
    [Fact]
    public async Task A_clone_that_no_longer_exists_is_skipped_rather_than_drawn()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1, 2]))),   // clone 2 is absent from the fixture
            await FixtureDungeonAsync(), 1, 1);

        Assert.Single(overlay.Pulls[0].MobKeys);
        Assert.Single(overlay.Pulls[0].Forces!.Unresolved);
    }

    // ---- geometry -------------------------------------------------------------------------

    [Fact]
    public async Task A_pull_gets_an_outline_around_its_mobs_with_its_number_at_the_centre()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1, 3]))), await FixtureDungeonAsync(), 1, 1);

        var pull = overlay.Pulls[0];
        Assert.Equal(2, pull.OnThisSubLevel);
        Assert.True(pull.Outline.Count > 8);

        // Clones 1 and 3 are at (100, -100) and (300, -300), so canvas (100, 100) and (300, 300).
        Assert.Equal(200, pull.Center.X, precision: 6);
        Assert.Equal(200, pull.Center.Y, precision: 6);
    }

    /// <summary>
    /// An off-sublevel mob must not drag the hull across a map it is not drawn on — but it is
    /// still in the pull, and still counts for forces.
    /// </summary>
    [Fact]
    public async Task A_pull_whose_mobs_are_all_on_another_sublevel_draws_nothing_but_still_counts()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), subLevel: 2, currentPull: 1);

        var pull = overlay.Pulls[0];
        Assert.Empty(pull.Outline);
        Assert.Equal(0, pull.OnThisSubLevel);
        Assert.Single(pull.MobKeys);
        Assert.Equal(5, pull.Forces!.Forces);
    }

    // ---- the readout ----------------------------------------------------------------------

    [Fact]
    public async Task The_forces_readout_is_cumulative_to_the_current_pull()
    {
        var route = RouteOf(
            PullOf(1, null, (1, [1])),      // 5
            PullOf(2, null, (2, [1])),      // 3
            PullOf(3, null, (1, [3])));     // 42

        var dungeon = await FixtureDungeonAsync();

        Assert.Equal("5/100 (5.00%)", RouteOverlay.Build(route, dungeon, 1, 1).ForcesReadout);
        Assert.Equal("8/100 (8.00%)", RouteOverlay.Build(route, dungeon, 1, 2).ForcesReadout);
        Assert.Equal("50/100 (50.00%)", RouteOverlay.Build(route, dungeon, 1, 3).ForcesReadout);
    }

    /// <summary>Before the first pull the route is worth nothing, not the whole dungeon.</summary>
    [Fact]
    public async Task A_cursor_before_the_first_pull_reads_zero()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, currentPull: 0);

        Assert.Equal(0, overlay.CumulativeForces);
        Assert.Equal("0/100 (0.00%)", overlay.ForcesReadout);
    }

    /// <summary>The overlay must not become a second, disagreeing forces implementation.</summary>
    [Fact]
    public async Task The_forces_are_the_same_ones_RouteForces_counts()
    {
        var route = RouteOf(PullOf(1, null, (1, [1])), PullOf(2, null, (1, [3]), (3, [1])));
        var dungeon = await FixtureDungeonAsync();

        var expected = RouteForces.Count(route, dungeon);
        var actual = RouteOverlay.Build(route, dungeon, 1, 1).Forces;

        // Field by field: PullForces holds a List<string>, so record equality compares that
        // member by reference and would pass two disagreeing runs off as different.
        Assert.Equal(expected.Count, actual.Count);
        Assert.Equal(
            expected.Select(f => (f.PullNumber, f.Forces, f.Cumulative, f.MobCount, f.DungeonTotal)),
            actual.Select(f => (f.PullNumber, f.Forces, f.Cumulative, f.MobCount, f.DungeonTotal)));
    }
}

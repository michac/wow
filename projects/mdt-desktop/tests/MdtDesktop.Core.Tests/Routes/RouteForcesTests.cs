using MdtDesktop.Core.Data;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;
using MdtDesktop.Core.Tests.Data;

namespace MdtDesktop.Core.Tests.Routes;

/// <summary>
/// The <c>MDT:CountForces</c> port, against the fixture dungeon so the expected numbers are
/// hand-computable rather than copied from a run.
/// </summary>
/// <remarks>
/// The fixture dungeon (index 4242, 100 forces) has: enemy 1 "Sparse Mob" at 5 forces with
/// clones 1 and 3, where clone 3 overrides to 42; enemy 2 "Patrolling Mob" at 3 forces with
/// clone 1; enemy 3 "Test Boss" at 0 forces with clone 1.
/// </remarks>
public class RouteForcesTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        var data = await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
        return data.ByIndex[4242];
    }

    private static Route RouteOf(params (int Enemy, int[] Clones)[][] pulls) => new()
    {
        DungeonIndex = 4242,
        Pulls = [.. pulls.Select((p, i) => new Pull
        {
            Number = i + 1,
            Enemies = [.. p.Select(e => new PullEnemy(e.Enemy, e.Clones))],
        })],
    };

    [Fact]
    public async Task A_pull_sums_the_enemy_count_once_per_clone()
    {
        // Enemy 1 is worth 5; clone 1 has no override.
        var forces = RouteForces.Count(RouteOf([(1, [1])]), await FixtureDungeonAsync());
        Assert.Equal(5, Assert.Single(forces).Forces);
    }

    [Fact]
    public async Task A_clone_count_override_wins_over_the_enemy_count()
    {
        // GetCloneEnemyForces: `clone.count or enemy.count`. Clone 3 overrides 5 -> 42.
        var forces = RouteForces.Count(RouteOf([(1, [1, 3])]), await FixtureDungeonAsync());
        Assert.Equal(47, Assert.Single(forces).Forces);      // 5 + 42, not 5 + 5
    }

    [Fact]
    public async Task Forces_accumulate_across_pulls()
    {
        var route = RouteOf(
            [(1, [1])],             // 5
            [(2, [1])],             // 3
            [(1, [3]), (3, [1])]);  // 42 + 0 (a boss is worth nothing)

        var forces = RouteForces.Count(route, await FixtureDungeonAsync());

        Assert.Equal([5, 3, 42], forces.Select(f => f.Forces));
        Assert.Equal([5, 8, 50], forces.Select(f => f.Cumulative));
        Assert.Equal([5, 8, 50], forces.Select(f => f.CumulativePercent));   // total is 100
        Assert.Equal([1, 1, 2], forces.Select(f => f.MobCount));
    }

    [Fact]
    public async Task A_boss_contributes_no_forces()
    {
        var forces = RouteForces.Count(RouteOf([(3, [1])]), await FixtureDungeonAsync());
        Assert.Equal(0, Assert.Single(forces).Forces);
        Assert.Equal(1, Assert.Single(forces).MobCount);     // still a mob in the pull
    }

    [Fact]
    public async Task Counting_up_to_a_pull_ignores_everything_after_it()
    {
        // MDT breaks out of a `pairs()` loop to do this, which has no guaranteed order; the
        // port filters on the pull number instead. Same answer, no dependence on iteration.
        var route = RouteOf([(1, [1])], [(2, [1])], [(1, [3])]);
        var dungeon = await FixtureDungeonAsync();

        Assert.Equal(5, RouteForces.CountUpTo(route, dungeon, 1));
        Assert.Equal(8, RouteForces.CountUpTo(route, dungeon, 2));
        Assert.Equal(50, RouteForces.CountUpTo(route, dungeon, 3));
        Assert.Equal(50, RouteForces.CountUpTo(route, dungeon, 99));
    }

    [Fact]
    public async Task A_clone_that_no_longer_exists_is_skipped_and_reported()
    {
        // IsCloneIncluded is a bare existence check, and it earns its place: MDT 6.2.13 deleted
        // clone 12 of The Blinding Vale's Radiant Spellsower, so a route drawn on 6.2.12 points
        // at a clone that is gone. The fixture's enemy 1 has no clone 2, standing in for that.
        var forces = Assert.Single(
            RouteForces.Count(RouteOf([(1, [1, 2])]), await FixtureDungeonAsync()));

        Assert.Equal(5, forces.Forces);            // clone 1 only
        Assert.Equal(1, forces.MobCount);
        Assert.Contains("clone 2 no longer exists", Assert.Single(forces.Unresolved));
    }

    [Fact]
    public async Task An_enemy_that_is_not_in_the_dungeon_is_skipped_and_reported()
    {
        var forces = Assert.Single(
            RouteForces.Count(RouteOf([(1, [1]), (99, [1])]), await FixtureDungeonAsync()));

        Assert.Equal(5, forces.Forces);
        Assert.Contains("enemy 99", Assert.Single(forces.Unresolved));
    }

    [Fact]
    public async Task An_empty_route_counts_nothing_rather_than_throwing()
        => Assert.Empty(RouteForces.Count(new Route { DungeonIndex = 4242 }, await FixtureDungeonAsync()));
}

/// <summary>
/// The staleness heuristics. They exist because a route names enemies by <i>index</i>, so one
/// drawn before MDT re-mapped a dungeon decodes cleanly and counts against whatever now sits at
/// those indices — the app's one silent failure mode.
/// </summary>
public class RouteHealthTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        return (await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory)).ByIndex[4242];
    }

    private static Route RouteOf(params (int Enemy, int[] Clones)[][] pulls) => new()
    {
        DungeonIndex = 4242,
        Pulls = [.. pulls.Select((p, i) => new Pull
        {
            Number = i + 1,
            Enemies = [.. p.Select(e => new PullEnemy(e.Enemy, e.Clones))],
        })],
    };

    private static async Task<IReadOnlyList<RouteWarning>> CheckAsync(Route route)
    {
        var dungeon = await FixtureDungeonAsync();
        return RouteHealth.Check(route, dungeon, RouteForces.Count(route, dungeon), "6.2.13");
    }

    [Fact]
    public async Task A_route_short_of_the_full_requirement_is_flagged()
    {
        // The fixture dungeon needs 100; this route is worth 5.
        var warning = Assert.Single(await CheckAsync(RouteOf([(1, [1])])),
            w => w.Kind == RouteWarningKind.CannotReachFullForces);

        Assert.Contains("5/100", warning.Message);
        Assert.Contains("6.2.13", warning.Message);
    }

    [Fact]
    public async Task A_reference_that_no_longer_resolves_is_flagged_separately()
    {
        var warnings = await CheckAsync(RouteOf([(1, [1, 2])]));   // clone 2 does not exist
        Assert.Contains(warnings, w => w.Kind == RouteWarningKind.UnresolvedReferences);
    }

    [Fact]
    public async Task A_route_that_reaches_the_requirement_is_not_flagged()
    {
        // 42 + 5 + 3 = 50 per pull pair... two of them clears 100.
        var route = RouteOf(
            [(1, [1, 3]), (2, [1])],    // 5 + 42 + 3 = 50
            [(1, [1, 3]), (2, [1])]);   // 50 again -> 100, exactly the requirement

        Assert.Empty(await CheckAsync(route));
    }
}

/// <summary>
/// <see cref="Route.AddonVersion"/> — the one exact staleness signal a route string can carry.
/// </summary>
public class RouteAddonVersionTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        return (await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory)).ByIndex[4242];
    }

    private static async Task<IReadOnlyList<RouteWarning>> CheckAsync(int? addonVersion, string cached)
    {
        // A route worth exactly the fixture dungeon's 100 forces, so only the version can warn.
        var route = new Route
        {
            DungeonIndex = 4242,
            AddonVersion = addonVersion,
            Pulls =
            [
                new Pull { Number = 1, Enemies = [new PullEnemy(1, [1, 3]), new PullEnemy(2, [1])] },
                new Pull { Number = 2, Enemies = [new PullEnemy(1, [1, 3]), new PullEnemy(2, [1])] },
            ],
        };

        var dungeon = await FixtureDungeonAsync();
        return RouteHealth.Check(route, dungeon, RouteForces.Count(route, dungeon), cached);
    }

    [Fact]
    public async Task A_route_exported_by_an_older_MDT_is_flagged_exactly()
    {
        // MDT packs its version by stripping the dots: 6.2.2 -> 622, 6.2.13 -> 6213.
        var warning = Assert.Single(await CheckAsync(622, "6.2.13"));

        Assert.Equal(RouteWarningKind.ExportedByOlderMdt, warning.Kind);
        Assert.Contains("6.2.2", warning.Message);
        Assert.Contains("6.2.13", warning.Message);
    }

    [Fact]
    public async Task A_route_exported_by_the_cached_MDT_is_not_flagged()
        => Assert.Empty(await CheckAsync(6213, "6.2.13"));

    [Fact]
    public async Task A_route_exported_by_a_NEWER_MDT_is_not_flagged_as_old()
    {
        // The user updating MDT Desktop's cache is the fix; nothing about the route is stale.
        Assert.DoesNotContain(await CheckAsync(6214, "6.2.13"),
            w => w.Kind == RouteWarningKind.ExportedByOlderMdt);
    }

    [Fact]
    public async Task A_string_with_no_addonVersion_cannot_be_checked_this_way()
    {
        // keystone.guru's exporter and MDT's own party-share path both omit it, so absence is
        // normal and must not be read as "current".
        Assert.Empty(await CheckAsync(null, "6.2.13"));
    }

    [Fact]
    public void The_real_route_carries_no_addonVersion()
    {
        // It was exported by keystone.guru — the `xxKG` uid suffix is their signature — and
        // their exporter omits the field.
        var route = RouteDecoder.Decode(File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "Routes", "Fixtures", "yoda-easy-route.txt")));

        Assert.Null(route.AddonVersion);
        Assert.EndsWith("xxKG", route.Uid);
    }
}

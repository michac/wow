using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Tests.Data;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// Laying the fixture dungeon out. Its four clones between them carry a clone scale override,
/// a per-clone forces override, a patrol and a boss — which is every branch in the layout.
/// </summary>
public class MapLayoutTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        var data = await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
        return data.ByIndex[4242];
    }

    [Fact]
    public async Task Every_clone_on_the_sublevel_becomes_one_blip()
    {
        var blips = MapLayout.Build(await FixtureDungeonAsync(), subLevel: 1);

        // Enemy 1 has clones 1 and 3 (2 is deliberately absent), enemies 2 and 3 have one each.
        Assert.Equal(4, blips.Count);
        Assert.Equal([(1, 1), (1, 3), (2, 1), (3, 1)], blips.Select(b => b.Key));
    }

    [Fact]
    public async Task A_blip_sits_where_its_clone_does_with_y_flipped()
    {
        var blip = Assert.Single(
            MapLayout.Build(await FixtureDungeonAsync(), 1), b => b.Key == (1, 1));

        Assert.Equal(100, blip.X, 6);      // clone.x = 100
        Assert.Equal(100, blip.Y, 6);      // clone.y = -100
    }

    [Fact]
    public async Task A_blip_carries_the_forces_the_clone_is_worth()
    {
        var blips = MapLayout.Build(await FixtureDungeonAsync(), 1).ToDictionary(b => b.Key);

        Assert.Equal(5, blips[(1, 1)].Forces);      // the enemy's own count
        Assert.Equal(42, blips[(1, 3)].Forces);     // clone 3 overrides it
        Assert.Equal(0, blips[(3, 1)].Forces);      // a boss is worth nothing
    }

    [Fact]
    public async Task A_boss_blip_is_flagged_and_drawn_larger()
    {
        var blips = MapLayout.Build(await FixtureDungeonAsync(), 1).ToDictionary(b => b.Key);

        Assert.True(blips[(3, 1)].IsBoss);
        Assert.False(blips[(1, 1)].IsBoss);
        Assert.True(blips[(3, 1)].Size > blips[(1, 1)].Size);
    }

    [Fact]
    public async Task Patrol_waypoints_are_placed_in_the_same_space()
    {
        var blips = MapLayout.Build(await FixtureDungeonAsync(), 1).ToDictionary(b => b.Key);

        Assert.Empty(blips[(1, 1)].Patrol);
        Assert.Equal(
            [new MapPoint(200, 200), new MapPoint(250, 260)],
            blips[(2, 1)].Patrol);
    }

    [Fact]
    public async Task Placing_into_a_bigger_canvas_scales_the_blips_with_it()
    {
        var dungeon = await FixtureDungeonAsync();
        var small = MapLayout.Build(dungeon, 1).ToDictionary(b => b.Key);
        var large = MapLayout.Build(dungeon, 1, widthPx: 1680, heightPx: 1120).ToDictionary(b => b.Key);

        Assert.Equal(small[(1, 1)].X * 2, large[(1, 1)].X, 6);
        Assert.Equal(small[(1, 1)].Y * 2, large[(1, 1)].Y, 6);
        Assert.Equal(small[(1, 1)].Size * 2, large[(1, 1)].Size, 6);
    }

    [Fact]
    public async Task A_sublevel_with_nothing_on_it_lays_out_empty_rather_than_throwing()
        => Assert.Empty(MapLayout.Build(await FixtureDungeonAsync(), subLevel: 2));

    [Fact]
    public async Task The_label_names_the_enemy_and_clone_a_route_would_refer_to()
    {
        var blips = MapLayout.Build(await FixtureDungeonAsync(), 1).ToDictionary(b => b.Key);
        Assert.Equal("Sparse Mob [1.3] — 42 forces", blips[(1, 3)].Label);
        Assert.Equal("Test Boss [3.1] — 0 forces (boss)", blips[(3, 1)].Label);
    }
}

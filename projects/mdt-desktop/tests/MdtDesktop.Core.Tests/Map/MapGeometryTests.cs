using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The map arithmetic. All of it is a restatement of MDT's own, so the tests pin the
/// restatement rather than any number MDT happens to ship.
/// </summary>
public class MapGeometryTests
{
    [Fact]
    public void The_default_space_is_MDTs_own_units_with_only_the_y_sign_flipped()
    {
        // clone.y is negative going down; a screen canvas is positive going down.
        Assert.Equal((100.0, 100.0), MapGeometry.ToCanvas(100, -100));
    }

    [Fact]
    public void The_canvas_extremes_land_on_the_edges()
    {
        Assert.Equal((0.0, 0.0), MapGeometry.ToCanvas(0, 0));
        Assert.Equal((840.0, 560.0), MapGeometry.ToCanvas(840, -560));
    }

    [Fact]
    public void Placing_into_a_bigger_canvas_scales_both_axes()
    {
        var (x, y) = MapGeometry.ToCanvas(420, -280, widthPx: 1680, heightPx: 1120);
        Assert.Equal(840, x, 6);
        Assert.Equal(560, y, 6);
    }

    [Theory]
    [InlineData(1, 1, 1)]
    [InlineData(1, 15, 15)]
    [InlineData(2, 1, 16)]
    [InlineData(10, 15, 150)]
    public void Tiles_are_numbered_row_major_from_one(int row, int column, int expected)
        => Assert.Equal(expected, MapGeometry.TileNumber(row, column));

    [Fact]
    public void A_sublevel_is_a_hundred_and_fifty_tiles_named_sublevel_underscore_number()
    {
        var names = MapGeometry.TileFileNames(1).ToList();
        Assert.Equal(150, names.Count);
        Assert.Equal("1_1.png", names[0]);
        Assert.Equal("1_150.png", names[^1]);

        // The sublevel is the first half of the name, so a second sublevel would be 2_*.
        Assert.Equal("2_16.png", MapGeometry.TileFileName(2, MapGeometry.TileNumber(2, 1)));
    }

    private static Enemy EnemyWith(double scale, bool isBoss = false)
        => new() { Index = 1, Scale = scale, IsBoss = isBoss };

    private static Clone CloneWith(double? scale = null, int? subLevel = 1)
        => new() { Index = 1, Scale = scale, SubLevel = subLevel };

    [Fact]
    public void A_plain_trash_blip_is_the_base_scale()
    {
        // (clone.scale ?? 1) * enemy.scale * 1 * 0.6
        Assert.Equal(0.6, MapGeometry.BlipScale(CloneWith(), EnemyWith(1)), 6);
        Assert.Equal(7.8, MapGeometry.BlipSize(CloneWith(), EnemyWith(1)), 6);
    }

    [Fact]
    public void A_clone_scale_override_multiplies_the_enemy_scale()
        => Assert.Equal(0.9, MapGeometry.BlipScale(CloneWith(1.5), EnemyWith(1)), 6);

    [Fact]
    public void A_boss_is_drawn_one_point_seven_times_the_size()
    {
        // 1 * 2 * 1.7 * 0.6
        Assert.Equal(2.04, MapGeometry.BlipScale(CloneWith(), EnemyWith(2, isBoss: true)), 6);
        Assert.Equal(26.52, MapGeometry.BlipSize(CloneWith(), EnemyWith(2, isBoss: true)), 6);
    }

    [Fact]
    public void A_clone_shows_on_its_own_sublevel_and_a_null_sublevel_shows_everywhere()
    {
        Assert.True(MapGeometry.IsVisibleOn(CloneWith(subLevel: 1), 1));
        Assert.False(MapGeometry.IsVisibleOn(CloneWith(subLevel: 2), 1));

        // MDT's own fallback. No shipped Midnight clone uses it, but an imported preset can.
        Assert.True(MapGeometry.IsVisibleOn(CloneWith(subLevel: null), 1));
        Assert.True(MapGeometry.IsVisibleOn(CloneWith(subLevel: null), 7));
    }
}

using MdtDesktop.Core.Data;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Data;

/// <summary>
/// MDT's season grouping, read out of its own <c>Modules/DungeonSelect.lua</c>.
/// </summary>
/// <remarks>
/// These pin the second stub contract in the sidecar — the three globals that file needs
/// (<c>tinsert</c>, <c>LibStub</c>, <c>MDT:IsRetail()</c>) — and the reason the grouping is
/// extracted rather than listed here: a season rotation upstream must need no edit on this side.
/// </remarks>
public class SeasonTests
{
    private static async Task<DungeonData> ExtractAsync(string? seasonLua, string? extra = null)
    {
        using var fixture = new MdtFixture(seasonLua: seasonLua, extraDungeonLua: extra);
        return await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
    }

    [Fact]
    public async Task Seasons_come_out_in_MDTs_own_declared_order_with_their_index_lists()
    {
        var data = await ExtractAsync(MdtFixture.DefaultSeasons, MdtFixture.ExtraDungeons);

        Assert.Equal(2, data.Seasons.Count);

        // Declared order, not sorted: MDT lists the newest season first and that is its UI.
        Assert.Equal("Fixture Season 2", data.Seasons[0].Name);
        Assert.Equal(1, data.Seasons[0].Order);
        Assert.Equal([4243, 4242], data.Seasons[0].Dungeons);

        Assert.Equal("Fixture Season 1", data.Seasons[1].Name);
        Assert.Equal(2, data.Seasons[1].Order);
        Assert.Equal([4242], data.Seasons[1].Dungeons);
    }

    /// <summary>
    /// ⚠ A release that ships no <c>Modules/DungeonSelect.lua</c> — non-retail, or reshaped —
    /// must still extract. No seasons is a valid answer; failing to read the dungeons is not.
    /// </summary>
    [Fact]
    public async Task A_release_with_no_DungeonSelect_yields_no_seasons_rather_than_failing()
    {
        var data = await ExtractAsync(seasonLua: null);

        Assert.Empty(data.Seasons);
        Assert.Single(data.Dungeons);
    }

    /// <summary>
    /// ⚠ The safety valve. A dungeon MDT ships but files under no season has to stay reachable,
    /// or the season picker becomes a way to hide dungeons from the user.
    /// </summary>
    [Fact]
    public async Task A_dungeon_no_season_names_lands_in_a_synthetic_trailing_group()
    {
        var data = await ExtractAsync(MdtFixture.DefaultSeasons, MdtFixture.ExtraDungeons);
        var groups = data.SeasonsWithOrphans();

        Assert.Equal(3, groups.Count);

        var orphans = groups[^1];
        Assert.Equal(DungeonData.OrphanSeasonName, orphans.Name);
        Assert.Equal(3, orphans.Order);
        Assert.Equal([4244], orphans.Dungeons);
    }

    [Fact]
    public async Task With_every_dungeon_named_no_synthetic_group_appears()
    {
        var data = await ExtractAsync(MdtFixture.DefaultSeasons);

        // Only 4242 is cached here, and both seasons name it.
        Assert.Equal(2, data.SeasonsWithOrphans().Count);
    }

    /// <summary>With nothing declared, one synthetic group holds the lot — the old flat list.</summary>
    [Fact]
    public void With_no_seasons_declared_every_dungeon_falls_into_the_synthetic_group()
    {
        var data = new DungeonData
        {
            Dungeons = [new Dungeon { Index = 7 }, new Dungeon { Index = 9 }],
        };

        var only = Assert.Single(data.SeasonsWithOrphans());
        Assert.Equal(DungeonData.OrphanSeasonName, only.Name);
        Assert.Equal([7, 9], only.Dungeons);
    }

    /// <summary>A dungeon may be in several seasons; MDT wrote the mechanism to allow it.</summary>
    [Fact]
    public async Task A_dungeon_in_two_seasons_is_not_an_orphan_and_is_listed_in_both()
    {
        var data = await ExtractAsync(MdtFixture.DefaultSeasons, MdtFixture.ExtraDungeons);

        Assert.Contains(4242, data.Seasons[0].Dungeons);
        Assert.Contains(4242, data.Seasons[1].Dungeons);
        Assert.DoesNotContain(4242, data.SeasonsWithOrphans()[^1].Dungeons);
    }
}

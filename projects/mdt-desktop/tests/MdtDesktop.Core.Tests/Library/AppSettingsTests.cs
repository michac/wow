using MdtDesktop.Core.Library;

namespace MdtDesktop.Core.Tests.Library;

/// <summary>
/// What the app remembers. The window-restore guard especially: its failure mode is an invisible
/// window on a monitor that no longer exists, which is unrecoverable from inside the app and so
/// has to be right before anybody runs it.
/// </summary>
public class AppSettingsTests
{
    private static string TempPath()
        => Path.Combine(Path.GetTempPath(), "mdtdesk-settings-" + Guid.NewGuid().ToString("N"),
            "settings.json");

    private static WindowPlacement Screen(double l, double t, double w, double h)
        => new(l, t, w, h, false);

    // ---- the file ------------------------------------------------------------------------

    [Fact]
    public void With_no_file_it_loads_the_defaults()
    {
        var settings = new SettingsStore(TempPath()).Load();

        Assert.Equal("F2", settings.NextPullHotKey);
        Assert.Equal("Shift+F2", settings.PreviousPullHotKey);
        Assert.Equal(1, settings.ZoomRelativeToFit);
        Assert.Null(settings.Window);
    }

    [Fact]
    public void It_round_trips()
    {
        var store = new SettingsStore(TempPath());
        var written = new AppSettings
        {
            Window = new WindowPlacement(-1920, -200, 1600, 900, false),
            AlwaysOnTop = true,
            Borderless = true,
            ZoomRelativeToFit = 2.5,
            NextPullHotKey = "Ctrl+F2",
            LastDungeonIndex = 164,
            LastSeasonName = "Midnight Season 2",
            LastRouteByDungeon = new Dictionary<int, string> { [164] = "6lbpOeHxxKG" },
        };

        Assert.True(store.Save(written));

        var read = store.Load();
        Assert.Equal(written.LastSeasonName, read.LastSeasonName);
        Assert.Equal(written.LastRouteByDungeon, read.LastRouteByDungeon);
        Assert.Equal(written.Window, read.Window);
        Assert.Equal(written.NextPullHotKey, read.NextPullHotKey);
    }

    // ---- the per-dungeon route migration ----------------------------------------------------

    /// <summary>
    /// ⚠ Without this the first launch after the per-dungeon change silently forgets the open
    /// route — the same complaint the change exists to fix, arriving once on upgrade.
    /// </summary>
    [Fact]
    public void A_legacy_single_route_id_migrates_into_the_per_dungeon_map()
    {
        var path = TempPath();
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, """
            {"version":1,"lastDungeonIndex":164,"lastRouteId":"6lbpOeHxxKG"}
            """);

        var settings = new SettingsStore(path).Load();

        Assert.Equal("6lbpOeHxxKG", settings.LastRouteByDungeon[164]);
    }

    /// <summary>A legacy id with no dungeon to file it under has nowhere to go, and is dropped.</summary>
    [Fact]
    public void A_legacy_route_id_with_no_remembered_dungeon_migrates_to_nothing()
    {
        var settings = new AppSettings { LastRouteId = "6lbpOeHxxKG" }.Migrated();
        Assert.Empty(settings.LastRouteByDungeon);
    }

    /// <summary>
    /// The migration is one-way and one-shot: once the map has entries the legacy id is inert,
    /// so it cannot resurrect a route the user has since cleared.
    /// </summary>
    [Fact]
    public void The_legacy_id_is_ignored_once_the_per_dungeon_map_has_entries()
    {
        var settings = new AppSettings
        {
            LastDungeonIndex = 164,
            LastRouteId = "old",
            LastRouteByDungeon = new Dictionary<int, string> { [160] = "new" },
        }.Migrated();

        Assert.Equal(new Dictionary<int, string> { [160] = "new" }, settings.LastRouteByDungeon);
    }

    /// <summary>Losing a remembered window position is a shrug; failing to start over one is not.</summary>
    [Fact]
    public void A_corrupt_file_loads_as_the_defaults_rather_than_throwing()
    {
        var path = TempPath();
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, "{ this is not json");

        Assert.Equal(new AppSettings(), new SettingsStore(path).Load());
    }

    /// <summary>
    /// ⚠ It must be a <b>sibling</b> of <c>routes/</c>, never a file inside it —
    /// <see cref="RouteLibrary.List"/> reads every <c>*.json</c> in its own folder as a saved
    /// route, so a settings file in there would be parsed as one and eventually deleted.
    /// </summary>
    [Fact]
    public void It_lives_beside_the_route_library_not_inside_it()
    {
        var settings = new SettingsStore().Path;
        var library = new RouteLibrary().Root;

        Assert.Equal(Path.GetDirectoryName(library), Path.GetDirectoryName(settings));
        Assert.False(settings.StartsWith(library + Path.DirectorySeparatorChar, StringComparison.Ordinal));
    }

    // ---- the restore guard ----------------------------------------------------------------

    [Fact]
    public void A_placement_on_a_screen_that_still_exists_is_left_alone()
    {
        var placement = new WindowPlacement(100, 100, 800, 600, false);
        Assert.Equal(placement, placement.ClampToVisible([Screen(0, 0, 1920, 1080)]));
    }

    [Fact]
    public void A_placement_on_a_monitor_that_is_gone_comes_back_to_the_primary()
    {
        // Remembered on a second monitor to the right that has since been unplugged.
        var placement = new WindowPlacement(2400, 200, 1200, 800, false);
        var clamped = placement.ClampToVisible([Screen(0, 0, 1920, 1080)]);

        Assert.Equal(360, clamped.Left);        // centred: (1920 - 1200) / 2
        Assert.Equal(140, clamped.Top);         // centred: (1080 - 800) / 2
        Assert.Equal(1200, clamped.Width);
    }

    /// <summary>
    /// ⚠ The classic bug in this exact function. A monitor above the primary has a negative Top,
    /// and <c>Math.Max(0, top)</c> would drag the window off it on every launch.
    /// </summary>
    [Fact]
    public void A_negative_position_on_a_real_monitor_is_preserved()
    {
        var placement = new WindowPlacement(-1800, -900, 1600, 800, false);
        var screens = new[] { Screen(0, 0, 1920, 1080), Screen(-1920, -1080, 1920, 1080) };

        Assert.Equal(placement, placement.ClampToVisible(screens));
    }

    /// <summary>A shared edge shows nothing, so touching is not overlapping.</summary>
    [Fact]
    public void A_window_exactly_off_the_edge_is_treated_as_off_screen()
    {
        var placement = new WindowPlacement(1920, 0, 800, 600, false);
        Assert.NotEqual(placement, placement.ClampToVisible([Screen(0, 0, 1920, 1080)]));
    }

    [Fact]
    public void A_window_hanging_partly_off_an_edge_still_counts_as_visible()
    {
        // Most of it is off the right, but enough is on to grab and move.
        var placement = new WindowPlacement(1800, 0, 800, 600, false);
        Assert.Equal(placement, placement.ClampToVisible([Screen(0, 0, 1920, 1080)]));
    }

    [Fact]
    public void A_window_larger_than_the_only_screen_is_shrunk_to_fit_it()
    {
        var placement = new WindowPlacement(5000, 5000, 3000, 2000, false);
        var clamped = placement.ClampToVisible([Screen(0, 0, 1920, 1080)]);

        Assert.Equal(1920, clamped.Width);
        Assert.Equal(1080, clamped.Height);
        Assert.Equal(0, clamped.Left);
    }

    /// <summary>
    /// If we could not ask what monitors exist, the answer is not "assume none" — that would
    /// throw away the user's framing over a failed query.
    /// </summary>
    [Fact]
    public void With_no_screens_reported_the_placement_is_returned_untouched()
    {
        var placement = new WindowPlacement(9999, 9999, 800, 600, false);
        Assert.Equal(placement, placement.ClampToVisible([]));
    }
}

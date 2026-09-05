using MdtDesktop.Core.Data;
using MdtDesktop.Core.Library;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;
using MdtDesktop.Core.Tests.Data;

namespace MdtDesktop.Core.Tests.Library;

/// <summary>
/// The local route library, and the mapping fingerprint that makes a re-map detectable for
/// routes whose strings say nothing about their own provenance.
/// </summary>
public class RouteLibraryTests : IDisposable
{
    private readonly string _root =
        Path.Combine(Path.GetTempPath(), "mdtdesk-lib-" + Guid.NewGuid().ToString("N"));

    private RouteLibrary Library => new(_root);

    private static string RealRoute() => File.ReadAllText(
        Path.Combine(AppContext.BaseDirectory, "Routes", "Fixtures", "yoda-easy-route.txt"));

    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        return (await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory)).ByIndex[4242];
    }

    public void Dispose()
    {
        if (Directory.Exists(_root)) Directory.Delete(_root, recursive: true);
        GC.SuppressFinalize(this);
    }

    [Fact]
    public void An_empty_library_lists_nothing_rather_than_throwing()
        => Assert.Empty(Library.List());

    [Fact]
    public async Task A_saved_route_survives_and_reloads()
    {
        var saved = Library.Save(RealRoute(), await FixtureDungeonAsync(), "6.2.13", name: "My route");

        // A fresh instance, as if the app had been closed and reopened.
        var reloaded = Assert.Single(new RouteLibrary(_root).List());

        Assert.Equal(saved.Id, reloaded.Id);
        Assert.Equal("My route", reloaded.Name);
        Assert.Equal(164, reloaded.DungeonIndex);
        Assert.Equal(18, reloaded.PullCount);
        Assert.Equal("6.2.13", reloaded.ImportedUnderMdtVersion);
    }

    [Fact]
    public async Task The_stored_string_is_verbatim_and_still_decodes()
    {
        // The string is the source of truth; everything else is a decoded convenience.
        var saved = Library.Save(RealRoute(), await FixtureDungeonAsync());
        var route = RouteDecoder.Decode(saved.RouteString);

        Assert.Equal(RealRoute().Trim(), saved.RouteString);
        Assert.Equal("Yoda easy route", route.Name);
        Assert.Equal(18, route.Pulls.Count);
    }

    [Fact]
    public async Task Re_importing_the_same_route_replaces_it_rather_than_duplicating()
    {
        // MDT's uid is stable precisely so repeat imports overwrite each other.
        var dungeon = await FixtureDungeonAsync();
        Library.Save(RealRoute(), dungeon, name: "first");
        Library.Save(RealRoute(), dungeon, name: "second");

        var only = Assert.Single(Library.List());
        Assert.Equal("second", only.Name);
        Assert.Equal("6lbpOeHxxKG", only.Id);
    }

    [Fact]
    public async Task A_route_can_be_removed()
    {
        var saved = Library.Save(RealRoute(), await FixtureDungeonAsync());

        Assert.True(Library.Remove(saved.Id));
        Assert.Empty(Library.List());
        Assert.False(Library.Remove(saved.Id));      // already gone
    }

    [Fact]
    public async Task An_unparseable_file_costs_one_route_not_the_library()
    {
        Library.Save(RealRoute(), await FixtureDungeonAsync());
        File.WriteAllText(Path.Combine(_root, "broken.json"), "{ not json");

        Assert.Single(Library.List());
    }

    // ---- the fingerprint ----------------------------------------------------------------

    [Fact]
    public async Task A_dungeon_that_has_not_moved_reports_no_change()
    {
        var saved = Library.Save(RealRoute(), await FixtureDungeonAsync());
        Assert.False(RouteLibrary.HasDungeonChangedSinceImport(saved, await FixtureDungeonAsync()));
    }

    [Fact]
    public async Task Moving_a_single_clone_is_detected()
    {
        var before = await FixtureDungeonAsync();
        var saved = Library.Save(RealRoute(), before);

        var moved = Move(before, enemyIndex: 1, cloneIndex: 1, dx: 0.1);

        Assert.True(RouteLibrary.HasDungeonChangedSinceImport(saved, moved));
    }

    [Fact]
    public async Task A_changed_forces_total_is_detected()
    {
        // MDT revises dungeonTotalCount on its own, which moves every percentage in a route
        // without touching an enemy — so the denominator is part of the fingerprint.
        var before = await FixtureDungeonAsync();
        var saved = Library.Save(RealRoute(), before);

        var retuned = Clone(before, totalCount: before.TotalCount + 1);

        Assert.True(RouteLibrary.HasDungeonChangedSinceImport(saved, retuned));
    }

    [Fact]
    public async Task Cosmetic_changes_do_not_trip_it()
    {
        // A renamed mob or corrected health invalidates no route, so it must not cry wolf.
        var before = await FixtureDungeonAsync();
        var saved = Library.Save(RealRoute(), before);

        var enemies = before.Enemies
            .Select(e => Clone(e, name: e.Name + " (renamed)", health: e.Health + 1000))
            .ToList();

        Assert.False(RouteLibrary.HasDungeonChangedSinceImport(saved, Clone(before, enemies: enemies)));
    }

    [Fact]
    public async Task Saving_with_no_dungeon_records_no_fingerprint_and_reads_as_unknown()
    {
        var saved = Library.Save(RealRoute(), dungeon: null);

        Assert.Null(saved.DungeonMappingHash);
        // Null means "cannot tell" and must never be reported as "unchanged".
        Assert.Null(RouteLibrary.HasDungeonChangedSinceImport(saved, await FixtureDungeonAsync()));
        Assert.Null(RouteLibrary.HasDungeonChangedSinceImport(saved, null));
    }

    [Fact]
    public async Task A_missing_dungeon_reads_as_unknown_rather_than_changed()
    {
        var saved = Library.Save(RealRoute(), await FixtureDungeonAsync());
        Assert.Null(RouteLibrary.HasDungeonChangedSinceImport(saved, null));
    }

    [Fact]
    public async Task The_fingerprint_is_stable_across_runs()
    {
        Assert.Equal(
            MappingHash.Compute(await FixtureDungeonAsync()),
            MappingHash.Compute(await FixtureDungeonAsync()));
    }

    /// <summary>
    /// The fingerprint must not read spells, and this is the test that keeps it that way.
    /// </summary>
    /// <remarks>
    /// Widening the spell schema changed every enemy in the cached data. If <c>MappingHash</c>
    /// digested spells, that one edit would have moved every fingerprint and every saved route
    /// in the library would have started reporting <i>dungeon re-mapped since import</i> —
    /// loudly, wrongly, and with nothing to point at. Reading the code says it does not; this
    /// says it cannot start.
    /// </remarks>
    [Fact]
    public async Task Editing_a_mobs_spell_list_does_not_move_the_fingerprint()
    {
        var dungeon = await FixtureDungeonAsync();

        var respelled = Clone(dungeon, enemies: [.. dungeon.Enemies.Select(e => Clone(e, spells:
            [new Spell { Id = 999_999, Interruptible = true, Enrage = true, Bleed = true }]))]);

        Assert.Equal(MappingHash.Compute(dungeon), MappingHash.Compute(respelled));
    }

    /// <summary>The other half of the same contract: what a route DOES depend on must move it.</summary>
    [Fact]
    public async Task Moving_a_clone_does_move_the_fingerprint()
    {
        var dungeon = await FixtureDungeonAsync();
        Assert.NotEqual(
            MappingHash.Compute(dungeon),
            MappingHash.Compute(Move(dungeon, enemyIndex: 1, cloneIndex: 1, dx: 0.5)));
    }

    // ---- helpers -------------------------------------------------------------------------

    // The model types are classes with init-only members rather than records, so these stand in
    // for `with`.
    private static Dungeon Clone(
        Dungeon d, int? totalCount = null, IReadOnlyList<Enemy>? enemies = null) => new()
    {
        Index = d.Index, Name = d.Name, EnglishName = d.EnglishName, ShortName = d.ShortName,
        MapId = d.MapId, TeleportId = d.TeleportId, IconId = d.IconId,
        TotalCount = totalCount ?? d.TotalCount,
        ZoneIds = d.ZoneIds, SubLevels = d.SubLevels, Enemies = enemies ?? d.Enemies, Pois = d.Pois,
    };

    private static Enemy Clone(
        Enemy e, string? name = null, long? health = null, IReadOnlyList<Clone>? clones = null,
        IReadOnlyList<Spell>? spells = null) => new()
    {
        Index = e.Index, Name = name ?? e.Name, Id = e.Id, Count = e.Count,
        Health = health ?? e.Health,
        Scale = e.Scale, DisplayId = e.DisplayId, CreatureType = e.CreatureType, Level = e.Level,
        IsBoss = e.IsBoss, EncounterId = e.EncounterId, InstanceId = e.InstanceId,
        Stealth = e.Stealth, StealthDetect = e.StealthDetect, Spells = spells ?? e.Spells,
        Characteristics = e.Characteristics, Clones = clones ?? e.Clones,
    };

    private static Dungeon Move(Dungeon d, int enemyIndex, int cloneIndex, double dx)
    {
        var enemies = d.Enemies.Select(e =>
        {
            if (e.Index != enemyIndex) return e;
            var clones = e.Clones.Select(c => c.Index == cloneIndex
                ? new Clone
                {
                    Index = c.Index, X = c.X + dx, Y = c.Y, SubLevel = c.SubLevel,
                    Group = c.Group, Scale = c.Scale, Count = c.Count, Patrol = c.Patrol,
                }
                : c).ToList();
            return Clone(e, clones: clones);
        }).ToList();

        return Clone(d, enemies: enemies);
    }
}

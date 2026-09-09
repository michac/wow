using MdtDesktop.Core.Data;

namespace MdtDesktop.Core.Tests.Data;

public class DataCacheTests
{
    private static string TempRoot()
        => Path.Combine(Path.GetTempPath(), "mdtdesk-cache-" + Guid.NewGuid().ToString("N"));

    [Fact]
    public void The_default_root_resolves_through_the_platform_local_data_folder()
    {
        // Deliberately not a literal %LOCALAPPDATA%: that form does not exist under WSL, where
        // the whole update path is developed and exercised.
        var expected = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            DataCache.CacheFolderName);

        Assert.Equal(expected, new DataCache().Root);
    }

    [Fact]
    public void The_addon_directory_is_where_the_release_zip_unpacks_to()
    {
        var cache = new DataCache("/tmp/x");
        Assert.Equal(Path.Combine("/tmp/x", "mdt", "MythicDungeonTools"), cache.AddonDirectory);
        Assert.Equal(Path.Combine("/tmp/x", "dungeons.json"), cache.DungeonsJsonPath);
        Assert.Equal(
            Path.Combine("/tmp/x", "mdt", "MythicDungeonTools", "Midnight", "Textures", "AltarOfFangs"),
            cache.TextureDirectory("AltarOfFangs"));
    }

    [Fact]
    public void A_stamp_round_trips()
    {
        var root = TempRoot();
        try
        {
            var cache = new DataCache(root);
            Assert.Null(cache.ReadStamp());

            var stamp = new CacheStamp("6.2.13", "6.2.13", "120100",
                new DateTimeOffset(2026, 9, 4, 12, 0, 0, TimeSpan.Zero), 16, 462, 3065);
            cache.WriteStamp(stamp);

            Assert.Equal(stamp, cache.ReadStamp());
        }
        finally { if (Directory.Exists(root)) Directory.Delete(root, recursive: true); }
    }

    [Fact]
    public void A_corrupt_stamp_reads_as_no_cache_rather_than_throwing()
    {
        var root = TempRoot();
        try
        {
            var cache = new DataCache(root);
            cache.EnsureRoot();
            File.WriteAllText(cache.VersionJsonPath, "{ this is not json");

            // "No usable cache" is exactly what a half-written stamp means, and it makes the
            // next `data update` rebuild instead of failing.
            Assert.Null(cache.ReadStamp());
        }
        finally { if (Directory.Exists(root)) Directory.Delete(root, recursive: true); }
    }

    /// <summary>
    /// A stamp written before <c>schemaVersion</c> existed must read as 0, not as current —
    /// otherwise a pre-widening cache is accepted and every enemy silently loses its spells.
    /// </summary>
    [Fact]
    public void A_stamp_with_no_schema_version_is_not_the_current_schema()
    {
        var root = TempRoot();
        var cache = new DataCache(root);
        cache.EnsureRoot();

        File.WriteAllText(cache.VersionJsonPath, """
            {"tag":"6.2.12","addonVersion":"6.2.12","interfaceVersion":"120100",
             "updatedUtc":"2026-09-01T00:00:00+00:00","dungeonCount":16,
             "enemyCount":462,"cloneCount":3066}
            """);

        var stamp = cache.ReadStamp();
        Assert.NotNull(stamp);
        Assert.Equal(0, stamp.SchemaVersion);
        Assert.False(stamp.IsCurrentSchema);
    }

    /// <summary>
    /// ⚠ Schema 3 added <c>seasons</c>, and a schema-2 cache is refused for the same reason a
    /// schema-1 one is: it deserializes without error and is quietly wrong — every dungeon would
    /// fall into the synthetic "Other" group, reading as though MDT had stopped shipping seasons.
    /// </summary>
    [Fact]
    public void A_schema_2_stamp_is_refused_rather_than_read()
    {
        var root = TempRoot();
        var cache = new DataCache(root);
        cache.EnsureRoot();

        cache.WriteStamp(new CacheStamp(
            "6.2.13", "6.2.13", "120100", DateTimeOffset.UtcNow, 16, 462, 3065, SchemaVersion: 2));

        var stamp = cache.ReadStamp();
        Assert.NotNull(stamp);
        Assert.Equal(2, stamp.SchemaVersion);
        Assert.False(stamp.IsCurrentSchema);
    }

    [Fact]
    public void A_stamp_round_trips_its_schema_version()
    {
        var cache = new DataCache(TempRoot());
        cache.WriteStamp(new CacheStamp(
            "6.2.13", "6.2.13", "120100", DateTimeOffset.UtcNow, 16, 462, 3065,
            CacheStamp.CurrentSchemaVersion));

        Assert.True(cache.ReadStamp()!.IsCurrentSchema);
    }
}

using MdtDesktop.Core.Data;
using MdtDesktop.Core.Lua;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Data;

/// <summary>
/// Runs <c>lua/extract_dungeons.lua</c> over a fixture release. These pin the stub contract —
/// which <c>MDT.*</c> tables the data files need and how the extractor reshapes what lands in
/// them — so a change on either side of the sidecar boundary fails here rather than in a map.
/// </summary>
public class DungeonExtractorTests
{
    private static async Task<MdtDesktop.Core.Model.DungeonData> ExtractAsync(string? dungeonLua = null)
    {
        using var fixture = new MdtFixture(dungeonLua);
        return await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
    }

    [Fact]
    public async Task It_reads_the_addon_version_out_of_the_toc()
    {
        var data = await ExtractAsync();
        Assert.Equal("9.9.9", data.AddonVersion);
        Assert.Equal("120100", data.InterfaceVersion);
    }

    [Fact]
    public async Task A_dungeon_keeps_MDTs_own_index()
    {
        var data = await ExtractAsync();
        var dungeon = Assert.Single(data.Dungeons);
        Assert.Equal(4242, dungeon.Index);
        Assert.Equal(4242, Assert.Single(data.ByIndex.Keys));
        Assert.Equal(100, dungeon.TotalCount);
        Assert.Equal([900, 901], dungeon.ZoneIds);
    }

    [Fact]
    public async Task Locale_strings_are_resolved_from_enUS()
    {
        var dungeon = Assert.Single((await ExtractAsync()).Dungeons);
        Assert.Equal("Test Dungeon", dungeon.Name);      // L["TestDungeon"], not the key
        Assert.Equal("TEST", dungeon.ShortName);
    }

    [Fact]
    public async Task An_unknown_locale_key_falls_back_to_the_key_itself()
    {
        // The stub's L answers a missing key with the key, so a data file can never
        // hand back nil and blank out a dungeon name.
        var lua = MdtFixture.DefaultDungeon
            .Replace("""MDT.dungeonList[dungeonIndex] = L["TestDungeon"]""",
                     """MDT.dungeonList[dungeonIndex] = L["NoSuchString"]""");

        var dungeon = Assert.Single((await ExtractAsync(lua)).Dungeons);
        Assert.Equal("NoSuchString", dungeon.Name);
    }

    [Fact]
    public async Task The_texture_folder_is_split_off_the_path_not_rebuilt_from_the_file_name()
    {
        // MDT ships SeatoftheTriumvirate.lua pointing at Textures\SeatOfTheTriumvirate, so the
        // tail is read verbatim. The fixture's deliberately odd casing stands in for that.
        var sub = Assert.Single(Assert.Single((await ExtractAsync()).Dungeons).SubLevels);
        Assert.Equal(1, sub.Index);
        Assert.Equal("Test Dungeon", sub.Name);
        Assert.Equal("TeStDuNgEoN", sub.TextureFolder);
        Assert.EndsWith(@"Midnight\Textures\TeStDuNgEoN", sub.CustomTextures);
    }

    [Fact]
    public async Task The_legacy_zeroth_map_slot_is_not_a_sublevel()
    {
        // dungeonMaps[idx][0] is always "" and is not a sublevel; sublevels run 1..#dungeonMaps.
        var dungeon = Assert.Single((await ExtractAsync()).Dungeons);
        Assert.Equal([1], dungeon.SubLevels.Select(s => s.Index));
    }

    [Fact]
    public async Task Sparse_clone_indices_survive_extraction()
    {
        // MDT 6.2.13 deleted clone 12 of The Blinding Vale's Radiant Spellsower, leaving it at
        // 1-11, 13-15. Position is not identity, so the index travels with each clone.
        var enemy = Assert.Single((await ExtractAsync()).Dungeons)
            .EnemiesByIndex[1];

        Assert.Equal([1, 3], enemy.Clones.Select(c => c.Index));
        Assert.Equal(2, enemy.ClonesByIndex.Count);
        Assert.Equal(300, enemy.ClonesByIndex[3].X);
    }

    [Fact]
    public async Task A_clone_carries_its_own_count_override()
    {
        var enemy = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[1];
        Assert.Null(enemy.ClonesByIndex[1].Count);        // falls back to enemy.Count
        Assert.Equal(42, enemy.ClonesByIndex[3].Count);
        Assert.Equal(1.5, enemy.ClonesByIndex[3].Scale);
        Assert.Equal(1, enemy.ClonesByIndex[1].Group);    // MDT's `g`
        Assert.Null(enemy.ClonesByIndex[3].Group);
    }

    [Fact]
    public async Task Coordinates_come_across_unchanged_with_y_negative()
    {
        var clone = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[3].Clones[0];
        Assert.Equal(400, clone.X);
        Assert.Equal(-400, clone.Y);
        Assert.Equal(1, clone.SubLevel);
    }

    [Fact]
    public async Task Patrol_waypoints_keep_their_order()
    {
        var clone = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[2].Clones[0];
        Assert.Equal([1, 2], clone.Patrol.Select(p => p.Index));
        Assert.Equal(250, clone.Patrol[1].X);
        Assert.Equal(-260, clone.Patrol[1].Y);
    }

    [Fact]
    public async Task Enemies_without_a_patrol_or_spells_get_empty_lists_not_null()
    {
        var boss = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[3];
        Assert.Empty(boss.Spells);
        Assert.Empty(boss.Characteristics);
        Assert.Empty(boss.Clones[0].Patrol);
    }

    [Fact]
    public async Task Spells_are_sorted_by_id_so_the_cache_file_diffs()
    {
        var enemy = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[1];
        Assert.Equal([10, 20, 30], enemy.Spells.Select(s => s.Id));
        Assert.Equal(["Incapacitate", "Taunt"], enemy.Characteristics);
    }

    /// <summary>
    /// The flags are the whole point of widening the schema — a spell that crosses as a bare id
    /// again would take the role classification with it, silently and without failing anything.
    /// </summary>
    [Fact]
    public async Task Spell_flags_cross_the_sidecar()
    {
        var enemy = Assert.Single((await ExtractAsync()).Dungeons).EnemiesByIndex[1];
        var byId = enemy.Spells.ToDictionary(s => s.Id);

        Assert.True(byId[20].Interruptible);
        Assert.True(byId[20].Poison);
        Assert.True(byId[30].Enrage);

        // Only true flags are emitted, so everything unset must arrive false, not null.
        Assert.False(byId[20].Enrage);
        Assert.False(byId[10].Interruptible);
        Assert.Empty(byId[10].Flags);

        Assert.True(enemy.HasInterruptibleSpell);
        Assert.Equal([SpellFlag.Enrage, SpellFlag.Poison], enemy.SpellFlags);
    }

    [Fact]
    public async Task A_mob_with_no_interruptible_spell_is_not_a_caster()
    {
        var dungeon = Assert.Single((await ExtractAsync()).Dungeons);
        Assert.False(dungeon.EnemiesByIndex[2].HasInterruptibleSpell);
        Assert.False(dungeon.EnemiesByIndex[3].HasInterruptibleSpell);
    }

    [Fact]
    public async Task Boss_and_stealth_flags_come_across()
    {
        var dungeon = Assert.Single((await ExtractAsync()).Dungeons);

        var boss = dungeon.EnemiesByIndex[3];
        Assert.True(boss.IsBoss);
        Assert.Equal(8888, boss.EncounterId);
        Assert.Equal(7777, boss.InstanceId);

        Assert.True(dungeon.EnemiesByIndex[2].Stealth);
        Assert.False(dungeon.EnemiesByIndex[1].Stealth);
        Assert.False(dungeon.EnemiesByIndex[1].IsBoss);
    }

    [Fact]
    public async Task Pois_keep_their_per_type_extras()
    {
        // POI keys vary by type, so only the shared ones are named and the rest ride along.
        var pois = Assert.Single((await ExtractAsync()).Dungeons).Pois;
        Assert.Equal(2, pois.Count);

        var entrance = pois[0];
        Assert.Equal("dungeonEntrance", entrance.Type);
        Assert.Equal(1, entrance.SubLevel);
        Assert.Equal(10.5, entrance.X);
        Assert.Equal(-20.5, entrance.Y);
        Assert.Equal(1.5, entrance.Extra["sizeMult"].GetDouble());

        var item = pois[1];
        Assert.Equal("genericItem", item.Type);
        Assert.Equal(777, item.Extra["info"].GetProperty("spellId").GetInt32());
    }

    [Fact]
    public async Task The_output_is_byte_stable_across_runs()
    {
        // Keys are sorted and collections are index-ordered specifically so the cache file can
        // be diffed between MDT releases.
        using var fixture = new MdtFixture();
        var extractor = new DungeonExtractor();
        Assert.Equal(
            await extractor.ExtractJsonAsync(fixture.AddonDirectory),
            await extractor.ExtractJsonAsync(fixture.AddonDirectory));
    }

    [Fact]
    public async Task A_directory_that_is_not_an_MDT_release_fails_loudly()
    {
        var empty = Path.Combine(Path.GetTempPath(), "mdtdesk-empty-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(empty);
        try
        {
            var ex = await Assert.ThrowsAsync<LuaException>(
                () => new DungeonExtractor().ExtractAsync(empty));
            Assert.Contains("load_midnight.xml", ex.Message);
        }
        finally { Directory.Delete(empty, recursive: true); }
    }

    [Fact]
    public async Task A_missing_directory_fails_before_the_sidecar_runs()
        => await Assert.ThrowsAsync<DataUpdateException>(
            () => new DungeonExtractor().ExtractAsync(
                Path.Combine(Path.GetTempPath(), "mdtdesk-nope-" + Guid.NewGuid().ToString("N"))));
}

namespace MdtDesktop.Core.Tests.Data;

/// <summary>
/// A miniature MDT release on disk: enough of the real layout for the sidecar to load,
/// and shaped to carry the cases the shipped data actually contains.
/// </summary>
/// <remarks>
/// The point of building one rather than pointing at a downloaded release is that the tests
/// then pin the <i>contract</i> — which <c>MDT.*</c> tables the stub must provide, and what
/// the extractor does with sparse indices, a missing locale string and a per-clone override —
/// instead of restating whatever numbers MDT happens to ship this week.
/// </remarks>
internal sealed class MdtFixture : IDisposable
{
    /// <param name="seasonLua">
    /// The contents of <c>Modules/DungeonSelect.lua</c>. Null writes none at all — which is the
    /// case the extractor has to survive, since a non-retail or reshaped release ships no such
    /// file and must still yield its dungeons.
    /// </param>
    /// <param name="extraDungeonLua">
    /// A second data file, added to <c>load_midnight.xml</c> after the first — the manifest is
    /// the load order of record, so a file not listed there is not loaded.
    /// </param>
    public MdtFixture(string? dungeonLua = null, string? seasonLua = null, string? extraDungeonLua = null)
    {
        Root = Path.Combine(Path.GetTempPath(), "mdtdesk-fixture-" + Guid.NewGuid().ToString("N"));
        AddonDirectory = Path.Combine(Root, "MythicDungeonTools");

        Directory.CreateDirectory(Path.Combine(AddonDirectory, "Locales"));
        Directory.CreateDirectory(Path.Combine(AddonDirectory, "Midnight"));
        Directory.CreateDirectory(Path.Combine(AddonDirectory, "Modules"));

        Write("MythicDungeonTools.toc", "## Interface: 120100\n## Version: 9.9.9\n");

        // The real file opens exactly like this, and the `L = L or {}` line is why the stub
        // has to hand over a table rather than nil.
        Write(Path.Combine("Locales", "enUS.lua"), """
            local addonName, MDT = ...
            local L = MDT.L
            L = L or {}
            L["TestDungeon"] = "Test Dungeon"
            L["TestDungeonShortName"] = "TEST"
            """);

        var extraScript = extraDungeonLua is null ? "" : "\n    <Script file='ExtraDungeons.lua'/>";
        Write(Path.Combine("Midnight", "load_midnight.xml"),
            "<Ui xmlns=\"http://www.blizzard.com/wow/ui/\">\n" +
            "    <Script file='TestDungeon.lua'/>" + extraScript + "\n</Ui>\n");

        Write(Path.Combine("Midnight", "TestDungeon.lua"), dungeonLua ?? DefaultDungeon);

        if (extraDungeonLua is not null)
            Write(Path.Combine("Midnight", "ExtraDungeons.lua"), extraDungeonLua);

        if (seasonLua is not null) Write(Path.Combine("Modules", "DungeonSelect.lua"), seasonLua);
    }

    public string Root { get; }
    public string AddonDirectory { get; }

    public void Write(string relativePath, string contents)
        => File.WriteAllText(Path.Combine(AddonDirectory, relativePath), contents);

    public void Dispose()
    {
        try { Directory.Delete(Root, recursive: true); } catch (IOException) { /* best effort */ }
    }

    /// <summary>
    /// A second and third dungeon, so a season can name one and leave another unnamed.
    /// </summary>
    /// <remarks>
    /// Deliberately minimal — the shape a dungeon must have to be listed at all is
    /// <c>mapInfo</c>, which is what the extractor treats as "this one is real".
    /// </remarks>
    public const string ExtraDungeons = """
        local _, MDT = ...
        for _, idx in ipairs({ 4243, 4244 }) do
          MDT.dungeonList[idx] = "Dungeon " .. idx
          MDT.mapInfo[idx] = { englishName = "Dungeon " .. idx, mapID = idx }
          MDT.dungeonMaps[idx] = { [0] = "", [1] = { customTextures = "Textures\\D" .. idx } }
          MDT.dungeonSubLevels[idx] = { [1] = "Floor" }
          MDT.dungeonTotalCount[idx] = { normal = 10 }
          MDT.dungeonEnemies[idx] = {}
        end
        """;

    /// <summary>
    /// The shape of MDT's real <c>Modules/DungeonSelect.lua</c>: two seasons, declared in its
    /// own order, built with the three globals it needs and nothing else.
    /// </summary>
    /// <remarks>
    /// It pins the stub contract for that file the same way <see cref="DefaultDungeon"/> pins it
    /// for the data files — <c>tinsert</c>, <c>LibStub</c> and <c>MDT:IsRetail()</c>. 4244 is
    /// named by neither season on purpose: a dungeon MDT ships but does not file has to stay
    /// reachable.
    /// </remarks>
    public const string DefaultSeasons = """
        local _, MDT = ...
        local AceGUI = LibStub("AceGUI-3.0")
        local L = MDT.L
        MDT.seasonList = {}
        MDT.dungeonSelectionToIndex = {}
        do
          if MDT:IsRetail() then
            tinsert(MDT.seasonList, L["Fixture Season 2"])
            tinsert(MDT.dungeonSelectionToIndex, { 4243, 4242 })
            tinsert(MDT.seasonList, L["Fixture Season 1"])
            tinsert(MDT.dungeonSelectionToIndex, { 4242 })
          end
        end
        function MDT:GetSeasonList() return MDT.seasonList end
        """;

    /// <summary>
    /// Index 4242, one sublevel, three enemies. Between them: a sparse clone index (MDT 6.2.13
    /// ships one), a per-clone <c>count</c> override, a patrol, a boss, a mob with no <c>spells</c>
    /// key at all, a spell carrying <b>flags</b> and one carrying none, a <c>customTextures</c>
    /// tail that differs in case from the file name, and a <c>dungeonList</c> entry whose locale
    /// string exists while another does not.
    /// </summary>
    public const string DefaultDungeon = """
        local _, MDT = ...
        local addonName = MDT.AddonName
        local L = MDT.L
        local dungeonIndex = 4242
        MDT.dungeonList[dungeonIndex] = L["TestDungeon"]
        MDT.mapInfo[dungeonIndex] = {
          teleportId = 111,
          shortName = L["TestDungeonShortName"],
          englishName = "Test Dungeon",
          mapID = 222,
        }

        local zones = { 900, 901 }
        for _, zone in ipairs(zones) do
          MDT.zoneIdToDungeonIdx[zone] = dungeonIndex
        end

        MDT.dungeonMaps[dungeonIndex] = {
          [0] = "",
          [1] = { customTextures = 'Interface\\AddOns\\'..addonName..'\\Midnight\\Textures\\TeStDuNgEoN' },
        }

        MDT.dungeonSubLevels[dungeonIndex] = {
          [1] = L["TestDungeon"],
        }

        MDT.dungeonTotalCount[dungeonIndex] = { normal = 100 }

        MDT.mapPOIs[dungeonIndex] = {
          [1] = {
            [1] = { ["type"] = "dungeonEntrance", ["x"] = 10.5, ["y"] = -20.5, ["sizeMult"] = 1.5 },
            [2] = { ["type"] = "genericItem", ["x"] = 30, ["y"] = -40,
                    ["info"] = { ["spellId"] = 777, ["size"] = 12 } },
          },
        }

        MDT.dungeonEnemies[dungeonIndex] = {
          [1] = {
            ["name"] = "Sparse Mob",
            ["id"] = 1001,
            ["count"] = 5,
            ["health"] = 1000,
            ["scale"] = 1,
            ["displayId"] = 500,
            ["creatureType"] = "Humanoid",
            ["level"] = 90,
            ["spells"] = {
              [30] = { ["enrage"] = true },
              [10] = {},
              [20] = { ["interruptible"] = true, ["poison"] = true },
            },
            ["characteristics"] = { ["Taunt"] = true, ["Incapacitate"] = true },
            ["clones"] = {
              [1] = { ["x"] = 100, ["y"] = -100, ["g"] = 1, ["sublevel"] = 1 },
              -- index 2 is deliberately absent
              [3] = { ["x"] = 300, ["y"] = -300, ["sublevel"] = 1, ["count"] = 42, ["scale"] = 1.5 },
            },
          },
          [2] = {
            ["name"] = "Patrolling Mob",
            ["id"] = 1002,
            ["count"] = 3,
            ["health"] = 2000,
            ["scale"] = 1,
            ["displayId"] = 501,
            ["creatureType"] = "Beast",
            ["level"] = 90,
            ["stealth"] = true,
            ["clones"] = {
              [1] = {
                ["x"] = 200, ["y"] = -200, ["sublevel"] = 1,
                ["patrol"] = { [1] = { ["x"] = 200, ["y"] = -200 }, [2] = { ["x"] = 250, ["y"] = -260 } },
              },
            },
          },
          [3] = {
            ["name"] = "Test Boss",
            ["id"] = 1003,
            ["count"] = 0,
            ["health"] = 9000,
            ["scale"] = 2,
            ["displayId"] = 502,
            ["creatureType"] = "Humanoid",
            ["level"] = 92,
            ["isBoss"] = true,
            ["encounterID"] = 8888,
            ["instanceID"] = 7777,
            ["clones"] = { [1] = { ["x"] = 400, ["y"] = -400, ["sublevel"] = 1 } },
          },
        }
        """;
}

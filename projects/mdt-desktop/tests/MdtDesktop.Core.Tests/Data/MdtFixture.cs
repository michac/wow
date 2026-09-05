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
    public MdtFixture(string? dungeonLua = null)
    {
        Root = Path.Combine(Path.GetTempPath(), "mdtdesk-fixture-" + Guid.NewGuid().ToString("N"));
        AddonDirectory = Path.Combine(Root, "MythicDungeonTools");

        Directory.CreateDirectory(Path.Combine(AddonDirectory, "Locales"));
        Directory.CreateDirectory(Path.Combine(AddonDirectory, "Midnight"));

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

        Write(Path.Combine("Midnight", "load_midnight.xml"), """
            <Ui xmlns="http://www.blizzard.com/wow/ui/">
                <Script file='TestDungeon.lua'/>
            </Ui>
            """);

        Write(Path.Combine("Midnight", "TestDungeon.lua"), dungeonLua ?? DefaultDungeon);
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

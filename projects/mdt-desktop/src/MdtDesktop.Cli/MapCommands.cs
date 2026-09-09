using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Cli;

/// <summary>
/// <c>mdtdesk map …</c> — the headless view of what the WPF map draws.
/// </summary>
/// <remarks>
/// The map itself needs Windows to look at; its <i>arithmetic</i> does not, and the arithmetic
/// is the part that can be wrong. This prints where every blip landed, whether the sublevel's
/// 150 tiles are actually on disk, and a coarse ASCII plot — enough to catch a flipped axis or
/// a dungeon whose tiles never downloaded, from WSL, with no game and no Windows.
/// </remarks>
internal static class MapCommands
{
    public static int Run(string[] args)
    {
        if (args.Length == 0 || !int.TryParse(args[0], out var index))
        {
            Console.Error.WriteLine("Usage: mdtdesk map <dungeonIndex> [--sublevel <n>] [--plot]");
            return 2;
        }

        var subLevel = 1;
        var plot = args.Contains("--plot");
        var at = Array.IndexOf(args, "--sublevel");
        if (at >= 0 && at + 1 < args.Length) int.TryParse(args[at + 1], out subLevel);

        var service = new DungeonDataService();
        if (service.LoadCached() is not { } data)
        {
            Console.Error.WriteLine("No cached dungeon data. Run `mdtdesk data update` first.");
            return 1;
        }

        if (data.Find(index) is not { } dungeon)
        {
            Console.Error.WriteLine($"No dungeon with index {index}. See `mdtdesk data list`.");
            return 1;
        }

        var blips = MapLayout.Build(dungeon, subLevel);
        Console.WriteLine($"[{dungeon.Index}] {dungeon.DisplayName}, sublevel {subLevel}");
        ReportTiles(dungeon, subLevel, service.Cache);

        if (blips.Count == 0)
        {
            Console.WriteLine("  blips     : none on this sublevel");
            return 0;
        }

        ReportBlips(dungeon, blips);
        if (plot) Plot(blips);
        return 0;
    }

    private static void ReportTiles(Dungeon dungeon, int subLevel, DataCache cache)
    {
        var folder = dungeon.SubLevels.FirstOrDefault(s => s.Index == subLevel)?.TextureFolder;
        if (folder is null)
        {
            Console.WriteLine($"  tiles     : no sublevel {subLevel} in this dungeon");
            return;
        }

        var directory = cache.TextureDirectory(folder);
        var present = MapGeometry.TileFileNames(subLevel)
            .Count(name => File.Exists(Path.Combine(directory, name)));

        Console.WriteLine($"  tiles     : {present}/{MapGeometry.TilesPerSubLevel} in {directory}");
    }

    private static void ReportBlips(Dungeon dungeon, IReadOnlyList<MapBlip> blips)
    {
        var forces = blips.Sum(b => b.Forces);

        Console.WriteLine($"  blips     : {blips.Count} ({blips.Count(b => b.IsBoss)} bosses, " +
                          $"{blips.Count(b => b.Patrol.Count > 0)} patrolling)");
        Console.WriteLine($"  forces    : {forces}/{dungeon.TotalCount} placed on the map");
        Console.WriteLine($"  x         : {blips.Min(b => b.X):F2} … {blips.Max(b => b.X):F2} " +
                          $"of {MapGeometry.CanvasWidth}");
        Console.WriteLine($"  y         : {blips.Min(b => b.Y):F2} … {blips.Max(b => b.Y):F2} " +
                          $"of {MapGeometry.CanvasHeight}");
        Console.WriteLine($"  blip size : {blips.Min(b => b.Size):F2} … {blips.Max(b => b.Size):F2} units");

        // A blip off the canvas is either a decode bug or MDT data we are reading wrong; either
        // way it is drawn outside the tiles, so say so rather than letting it vanish.
        var outside = blips.Where(b =>
            b.X < 0 || b.X > MapGeometry.CanvasWidth ||
            b.Y < 0 || b.Y > MapGeometry.CanvasHeight).ToList();

        if (outside.Count > 0)
        {
            Console.WriteLine($"  ⚠ {outside.Count} blip(s) fall outside the canvas:");
            foreach (var blip in outside.Take(10))
                Console.WriteLine($"      {blip.Describe()} at ({blip.X:F2}, {blip.Y:F2})");
        }
    }

    /// <summary>A coarse plot — enough to see the map's shape, and that it is the right way up.</summary>
    private static void Plot(IReadOnlyList<MapBlip> blips)
    {
        const int columns = 78, rows = 26;
        var grid = new char[rows, columns];
        for (var r = 0; r < rows; r++)
            for (var c = 0; c < columns; c++)
                grid[r, c] = '·';

        foreach (var blip in blips)
        {
            var c = Math.Clamp((int)(blip.X / MapGeometry.CanvasWidth * columns), 0, columns - 1);
            var r = Math.Clamp((int)(blip.Y / MapGeometry.CanvasHeight * rows), 0, rows - 1);
            grid[r, c] = blip.IsBoss ? 'B' : grid[r, c] is 'B' ? 'B' : 'o';
        }

        Console.WriteLine();
        for (var r = 0; r < rows; r++)
        {
            var line = new char[columns];
            for (var c = 0; c < columns; c++) line[c] = grid[r, c];
            Console.WriteLine("  " + new string(line));
        }
    }
}

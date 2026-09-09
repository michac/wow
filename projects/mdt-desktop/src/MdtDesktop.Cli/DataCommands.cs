using MdtDesktop.Core.Data;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Cli;

/// <summary>
/// <c>mdtdesk data …</c> — the headless door onto the dungeon cache, so M1 is verifiable
/// with no UI, no game running, and no WoW install anywhere on the machine.
/// </summary>
internal static class DataCommands
{
    public static async Task<int> RunAsync(string[] args)
    {
        var sub = args.Length > 0 ? args[0] : "";
        return sub switch
        {
            "update" => await UpdateAsync(args[1..]),
            "show" => Show(args[1..]),
            "list" => List(),
            _ => Unknown(sub),
        };
    }

    private static int Unknown(string sub)
    {
        Console.Error.WriteLine(
            string.IsNullOrEmpty(sub)
                ? "data needs a subcommand: update, list or show."
                : $"Unknown data subcommand '{sub}'. Try update, list or show.");
        return 2;
    }

    private static async Task<int> UpdateAsync(string[] args)
    {
        var force = args.Contains("--force");
        var service = new DungeonDataService();
        var progress = new Progress<string>(line => Console.WriteLine($"  {line}"));

        Console.WriteLine($"cache : {service.Cache.Root}");

        var result = await service.UpdateAsync(force, progress);
        var stamp = result.Stamp;

        Console.WriteLine();
        Console.WriteLine($"MDT      : {stamp.Tag} (addon {stamp.AddonVersion}, interface {stamp.InterfaceVersion})");
        Console.WriteLine($"dungeons : {stamp.DungeonCount}");
        Console.WriteLine($"enemies  : {stamp.EnemyCount}");
        Console.WriteLine($"clones   : {stamp.CloneCount}");
        Console.WriteLine($"updated  : {stamp.UpdatedUtc:u}{(result.Downloaded ? "" : " (cache was already current)")}");
        return 0;
    }

    private static DungeonData? Cached()
    {
        var data = new DungeonDataService().LoadCached();
        if (data is null)
            Console.Error.WriteLine("No cached dungeon data. Run `mdtdesk data update` first.");
        return data;
    }

    private static int List()
    {
        if (Cached() is not { } data) return 1;

        Console.WriteLine($"MDT {data.AddonVersion} — {data.Dungeons.Count} dungeons");

        // Grouped the way MDT's own dropdown groups them, in its own order — Season 2 first —
        // and never re-sorted, because the ordering is the addon's rather than ours. The
        // trailing "Other" group only appears when a cached dungeon is in no declared season.
        foreach (var season in data.SeasonsWithOrphans())
        {
            Console.WriteLine();
            Console.WriteLine($"{season.DisplayName} — {season.Dungeons.Count} dungeons");
            Console.WriteLine($"{"idx",5}  {"name",-26} {"short",-6} {"forces",6} {"enemies",7} {"clones",6}");

            foreach (var index in season.Dungeons)
            {
                if (data.Find(index) is not { } d)
                {
                    // A season naming a dungeon the release does not ship. Said out loud rather
                    // than skipped: it means the two halves of MDT's own data disagree.
                    Console.WriteLine($"{index,5}  ⚠ named by the season but not in the cache");
                    continue;
                }

                Console.WriteLine(
                    $"{d.Index,5}  {Truncate(d.DisplayName, 26),-26} {d.ShortName,-6} {d.TotalCount,6} " +
                    $"{d.Enemies.Count,7} {d.Enemies.Sum(e => e.Clones.Count),6}");
            }
        }

        return 0;
    }

    private static int Show(string[] args)
    {
        if (args.Length == 0 || !int.TryParse(args[0], out var index))
        {
            Console.Error.WriteLine("Usage: mdtdesk data show <dungeonIndex>   (see `mdtdesk data list`)");
            return 2;
        }

        if (Cached() is not { } data) return 1;

        if (data.Find(index) is not { } dungeon)
        {
            Console.Error.WriteLine($"No dungeon with index {index}. Known: " +
                                    string.Join(", ", data.Dungeons.Select(d => d.Index)));
            return 1;
        }

        var clones = dungeon.Enemies.Sum(e => e.Clones.Count);
        var bosses = dungeon.Enemies.Count(e => e.IsBoss);

        Console.WriteLine($"[{dungeon.Index}] {dungeon.DisplayName}");
        Console.WriteLine($"  english   : {dungeon.EnglishName}");
        Console.WriteLine($"  short     : {dungeon.ShortName}");
        Console.WriteLine($"  mapId     : {dungeon.MapId}   teleport: {dungeon.TeleportId}");
        Console.WriteLine($"  zoneIds   : {string.Join(", ", dungeon.ZoneIds)}");
        Console.WriteLine($"  forces    : dungeonTotalCount.normal == {dungeon.TotalCount}");
        Console.WriteLine($"  enemies   : {dungeon.Enemies.Count} ({bosses} bosses), {clones} clones");
        Console.WriteLine($"  pois      : {dungeon.Pois.Count}");

        Console.WriteLine("  sublevels :");
        foreach (var sub in dungeon.SubLevels)
            Console.WriteLine($"    [{sub.Index}] {sub.Name}  tiles: Midnight/Textures/{sub.TextureFolder}");

        // The forces arithmetic is the thing M2 builds on, so show it summing to the total.
        var trash = dungeon.Enemies
            .SelectMany(e => e.Clones.Select(c => c.Count ?? e.Count))
            .Sum();
        Console.WriteLine($"  every clone summed: {trash} " +
                          $"({(dungeon.TotalCount == 0 ? 0 : 100.0 * trash / dungeon.TotalCount):F1}% of the total)");

        Console.WriteLine();
        Console.WriteLine($"  {"idx",4}  {"enemy",-32} {"count",5} {"clones",6}  flags");
        foreach (var e in dungeon.Enemies)
        {
            var flags = new List<string>();
            if (e.IsBoss) flags.Add("boss");
            if (e.Stealth) flags.Add("stealth");
            if (e.StealthDetect) flags.Add("stealth-detect");
            if (e.Clones.Any(c => c.Patrol.Count > 0)) flags.Add("patrol");
            if (e.Clones.Any(c => c.Count is not null)) flags.Add("count-override");

            Console.WriteLine($"  {e.Index,4}  {Truncate(e.Name ?? "?", 32),-32} {e.Count,5} " +
                              $"{e.Clones.Count,6}  {string.Join(" ", flags)}");
        }

        return 0;
    }

    private static string Truncate(string s, int width)
        => s.Length <= width ? s : s[..(width - 1)] + "…";
}

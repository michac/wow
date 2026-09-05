using MdtDesktop.Core.Data;
using MdtDesktop.Core.Library;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Cli;

/// <summary>
/// <c>mdtdesk pulls …</c> — the route overlay the WPF map draws, printed instead.
/// </summary>
/// <remarks>
/// <see cref="RouteOverlay"/> is what <c>MapView</c> renders, and every decision in it — pull
/// colour, hull, centroid, which mob belongs to which pull, what is dimmed — is made there
/// rather than in WPF. This is how that gets checked on a machine with no Windows: the same
/// object, read out as text, plus a plot that draws each pull's number where its mobs are.
/// </remarks>
internal static class PullCommands
{
    public static int Run(string[] args)
    {
        var input = args.FirstOrDefault(a => !a.StartsWith("--"));
        if (string.IsNullOrWhiteSpace(input))
        {
            Console.Error.WriteLine(
                "Usage: mdtdesk pulls <string>|-|<savedId> [--sublevel <n>] [--current <n>] [--plot]");
            return 2;
        }

        var subLevel = OptionInt(args, "--sublevel");
        var currentPull = OptionInt(args, "--current");

        // An id from the library, a bare string, or `-` for stdin — the same three doors
        // `route show` and `route decode` already offer, so neither has to be preferred.
        var library = new RouteLibrary();
        var saved = library.Find(input);
        var routeString = saved?.RouteString ?? (input == "-" ? Console.In.ReadToEnd() : input);

        var route = RouteDecoder.Decode(routeString);

        var service = new DungeonDataService();
        if (service.LoadCached() is not { } data)
        {
            Console.Error.WriteLine("No cached dungeon data. Run `mdtdesk data update` first.");
            return 1;
        }

        if (data.Find(route.DungeonIndex) is not { } dungeon)
        {
            Console.Error.WriteLine($"Dungeon {route.DungeonIndex} is not in the cache.");
            return 1;
        }

        var level = subLevel ?? route.CurrentSubLevel;
        var current = currentPull ?? route.CurrentPull;
        var overlay = RouteOverlay.Build(route, dungeon, level, current);

        Console.WriteLine($"route     : {route.Name ?? "(unnamed)"}{(saved is null ? "" : $"  [{saved.Id}]")}");
        Console.WriteLine($"dungeon   : [{dungeon.Index}] {dungeon.DisplayName}, sublevel {level}");
        Console.WriteLine($"current   : pull {current}{(overlay.Current is null ? "  ⚠ no such pull" : "")}");
        Console.WriteLine($"forces    : {overlay.ForcesReadout}");
        Console.WriteLine();

        Report(overlay);

        var blips = MapLayout.Build(dungeon, level);
        Summarise(overlay, blips, MobRoleIndex.Build(data));

        if (args.Contains("--plot")) Plot(overlay, blips);
        if (args.Contains("--vertices")) Vertices(route, dungeon, level, overlay);
        return 0;
    }

    /// <summary>
    /// The hull cross-check dump: per pull, a <c>v</c> line of input vertices and an <c>o</c>
    /// line of the outline computed from them, both in <b>MDT's own</b> coordinate space — y
    /// negative going down, unflipped.
    /// </summary>
    /// <remarks>
    /// <para>
    /// The door for checking our geometry against MDT's, the way the forces port was checked
    /// against its unmodified <c>Pulls.lua</c>. It prints MDT's space rather than the canvas one
    /// deliberately: <c>getPullVertices</c> collects exactly these numbers
    /// (<c>PullOutlines.lua:305-323</c>), so MDT's own <c>convex_hull</c> runs over them and the
    /// two outlines compare point for point.
    /// </para>
    /// <para>
    /// The y flip is undone rather than left in, because a mirrored hull is still a correct hull
    /// and comparing mirrored numbers is how a real disagreement gets lost in a sign.
    /// </para>
    /// </remarks>
    private static void Vertices(
        Route route, Dungeon dungeon, int subLevel, RouteOverlayResult overlay)
    {
        Console.WriteLine();
        foreach (var pull in route.Pulls.OrderBy(p => p.Number))
        {
            var parts = new List<string>();

            foreach (var entry in pull.Enemies)
            {
                if (!dungeon.EnemiesByIndex.TryGetValue(entry.EnemyIndex, out var enemy)) continue;

                foreach (var cloneIndex in entry.CloneIndices)
                {
                    if (!enemy.ClonesByIndex.TryGetValue(cloneIndex, out var clone)) continue;
                    if (!MapGeometry.IsVisibleOn(clone, subLevel)) continue;

                    parts.Add($"{clone.X:R},{clone.Y:R},{MapGeometry.BlipScale(clone, enemy):R}");
                }
            }

            Console.WriteLine("v " + string.Join(";", parts));

            var outline = overlay.Pulls.First(p => p.Number == pull.Number).Outline;
            Console.WriteLine("o " + string.Join(";", outline.Select(p => $"{p.X:R},{-p.Y:R}")));
        }
    }

    private static void Report(RouteOverlayResult overlay)
    {
        Console.WriteLine($"{"pull",4} {"mobs",5} {"here",5} {"forces",7} {"cumulative",11} " +
                          $"{"pct",7}  {"colour",-16} {"alpha",5}  {"hull",5}  centroid");

        foreach (var pull in overlay.Pulls)
        {
            var colour = pull.HasCustomColor ? pull.Color : pull.Color + " (default)";
            var f = pull.Forces;

            Console.WriteLine(
                $"{pull.Number,4} {pull.MobKeys.Count,5} {pull.OnThisSubLevel,5} " +
                $"{f?.Forces ?? 0,7} {f?.Cumulative ?? 0,7}/{f?.DungeonTotal ?? 0,-3} " +
                $"{f?.CumulativePercent ?? 0,6:F2}%  {colour,-16} {pull.Alpha,5:F1}  " +
                $"{pull.Outline.Count,5}  ({pull.Center.X,6:F1}, {pull.Center.Y,6:F1})" +
                (pull.IsCurrent ? "  ← current" : ""));

            foreach (var warning in f?.Unresolved ?? [])
                Console.WriteLine($"       ⚠ {warning}");
        }
    }

    /// <summary>
    /// The checks a pair of eyes would otherwise have to make. Each prints its own verdict, so a
    /// run either says every line is fine or says which one is not.
    /// </summary>
    private static void Summarise(
        RouteOverlayResult overlay, IReadOnlyList<MapBlip> blips, MobRoleIndex roles)
    {
        Console.WriteLine();

        var assigned = blips.Where(b => overlay.RoleByMob.ContainsKey(b.Key)).ToList();
        var unassigned = blips.Where(b => !overlay.RoleByMob.ContainsKey(b.Key)).ToList();

        Console.WriteLine($"blips     : {blips.Count} on this sublevel — " +
                          $"{assigned.Count} in a pull (pull colour), " +
                          $"{unassigned.Count} in none (role colour)");

        // The coexistence rule, counted rather than argued: these two sets are disjoint by
        // construction, so the role palette only ever has to work on the second one.
        var histogram = roles.Tally(unassigned.Select(b => b.Enemy).Distinct());
        Console.WriteLine("  unassigned by role : " +
                          string.Join(", ", histogram.Select(kv => $"{kv.Key} {kv.Value}")));

        // A mob in two pulls would be drawn in one colour and counted in two, which is a route
        // MDT allows and nothing downstream could recover from.
        var doubled = overlay.Pulls.SelectMany(p => p.MobKeys)
            .GroupBy(k => k).Where(g => g.Count() > 1).ToList();
        Console.WriteLine(doubled.Count == 0
            ? "  no mob is in two pulls           : ok"
            : $"  ⚠ {doubled.Count} mob(s) appear in more than one pull");

        // A hull legitimately stands off its mobs by up to scale*10 units, so it can overhang
        // the canvas at the map edge. Large overhangs are the thing worth knowing about.
        var overhang = overlay.Pulls
            .SelectMany(p => p.Outline)
            .Select(p => Math.Max(
                Math.Max(-p.X, p.X - MapGeometry.CanvasWidth),
                Math.Max(-p.Y, p.Y - MapGeometry.CanvasHeight)))
            .DefaultIfEmpty(0).Max();

        Console.WriteLine(overhang <= 0
            ? "  every hull inside the canvas     : ok"
            : $"  hulls overhang the canvas by up to {overhang:F1} units " +
              (overhang <= PullHull.RadiusPerScale * 2
                  ? "(within the stand-off, expected at the map edge)"
                  : "⚠ more than the stand-off explains"));

        var empty = overlay.Pulls.Count(p => p.MobKeys.Count > 0 && p.OnThisSubLevel == 0);
        if (empty > 0)
            Console.WriteLine($"  {empty} pull(s) have no mob on this sublevel and draw no outline");
    }

    /// <summary>
    /// Each pull drawn as its own glyph where its mobs stand. The closest thing to seeing the
    /// overlay that a terminal allows: it shows pull adjacency, ordering, and strays.
    /// </summary>
    private static void Plot(RouteOverlayResult overlay, IReadOnlyList<MapBlip> blips)
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

            // 1-9 then a-z, so a 35-pull route still reads. An unassigned mob stays a dot so
            // the pulls are what the eye picks up.
            grid[r, c] = overlay.RoleByMob.TryGetValue(blip.Key, out var role)
                ? Glyph(role.PullNumber)
                : grid[r, c] is '·' ? '.' : grid[r, c];
        }

        Console.WriteLine();
        for (var r = 0; r < rows; r++)
        {
            var line = new char[columns];
            for (var c = 0; c < columns; c++) line[c] = grid[r, c];
            Console.WriteLine("  " + new string(line));
        }
        Console.WriteLine("\n  1-9,a-z = pull number · . = mob in no pull");
    }

    private static char Glyph(int pullNumber) => pullNumber switch
    {
        >= 1 and <= 9 => (char)('0' + pullNumber),
        >= 10 and <= 35 => (char)('a' + pullNumber - 10),
        _ => '#',
    };

    private static int? OptionInt(string[] args, string name)
    {
        var i = Array.IndexOf(args, name);
        return i >= 0 && i + 1 < args.Length && int.TryParse(args[i + 1], out var value)
            ? value
            : null;
    }
}

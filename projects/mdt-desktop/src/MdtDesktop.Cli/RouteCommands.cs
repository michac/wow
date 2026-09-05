using MdtDesktop.Core.Data;
using MdtDesktop.Core.Library;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Cli;

/// <summary>
/// <c>mdtdesk route …</c> — decode a route string, and manage the local library, so both are
/// verifiable before any UI exists.
/// </summary>
internal static class RouteCommands
{
    public static Task<int> RunAsync(string[] args)
    {
        var sub = args.Length > 0 ? args[0] : "";
        return Task.FromResult(sub switch
        {
            "decode" => Decode(args[1..]),
            "save" => Save(args[1..]),
            "list" => ListSaved(),
            "show" => ShowSaved(args[1..]),
            "remove" => RemoveSaved(args[1..]),
            _ => Unknown(sub),
        });
    }

    private static int Unknown(string sub)
    {
        Console.Error.WriteLine(string.IsNullOrEmpty(sub)
            ? "route needs a subcommand: decode, save, list, show or remove."
            : $"Unknown route subcommand '{sub}'. Try decode, save, list, show or remove.");
        return 2;
    }

    // ---- decoding ----------------------------------------------------------------------

    private static int Decode(string[] args)
    {
        if (ReadRouteArg(args, "decode <string>|- [--json]") is not { } routeString) return 2;

        if (args.Contains("--json"))
        {
            // The debugging door: the decoded route verbatim, for diffing against another
            // decoder or feeding to a cross-check.
            Console.WriteLine(System.Text.Json.JsonSerializer.Serialize(
                RouteDecoder.Decode(routeString),
                new System.Text.Json.JsonSerializerOptions { WriteIndented = true }));
            return 0;
        }

        return Report(routeString, saved: null);
    }

    /// <summary>Prints a route: header, per-pull forces, then any staleness warnings.</summary>
    private static int Report(string routeString, SavedRoute? saved)
    {
        var route = RouteDecoder.Decode(routeString);

        var data = new DungeonDataService().LoadCached();
        if (data is null)
        {
            Console.Error.WriteLine("No cached dungeon data. Run `mdtdesk data update` first.");
            return 1;
        }

        var dungeon = data.Find(route.DungeonIndex);

        if (saved is not null)
        {
            Console.WriteLine($"id        : {saved.Id}");
            Console.WriteLine($"imported  : {saved.ImportedUtc:yyyy-MM-dd HH:mm} UTC" +
                              $" under MDT {saved.ImportedUnderMdtVersion ?? "?"}");
        }

        Console.WriteLine($"route     : {route.Name ?? "(unnamed)"}");
        Console.WriteLine($"uid       : {route.Uid}");
        Console.WriteLine($"format    : {RouteDecoder.Classify(routeString)}");
        Console.WriteLine($"dungeon   : [{route.DungeonIndex}] {dungeon?.DisplayName ?? "UNKNOWN — not in the cached data"}");
        Console.WriteLine($"pulls     : {route.Pulls.Count}");
        Console.WriteLine($"exported  : {(route.AddonVersion is { } v ? $"MDT {v}" : "no addonVersion in the string")}");
        Console.WriteLine($"cursor    : currentPull {route.CurrentPull}, sublevel {route.CurrentSubLevel}");

        if (dungeon is null)
        {
            Console.Error.WriteLine($"\nDungeon {route.DungeonIndex} is not in the cache; cannot count forces.");
            return 1;
        }

        Console.WriteLine($"forces    : {dungeon.TotalCount} needed for 100%");
        Console.WriteLine();

        var forces = RouteForces.Count(route, dungeon);

        Console.WriteLine($"{"pull",4} {"mobs",5} {"forces",7} {"cumulative",11} {"pct",7}  color");
        foreach (var p in forces)
        {
            var pull = route.Pulls[p.PullNumber - 1];
            var color = pull.HasCustomColor ? pull.Color : $"{pull.Color ?? "-"} (default)";

            Console.WriteLine($"{p.PullNumber,4} {p.MobCount,5} {p.Forces,7} " +
                              $"{p.Cumulative,7}/{p.DungeonTotal,-3} {p.CumulativePercent,6:F2}%  {color}");

            foreach (var warning in p.Unresolved)
                Console.WriteLine($"       ⚠ {warning}");
        }

        var last = forces.Count > 0 ? forces[^1] : null;
        Console.WriteLine();
        Console.WriteLine($"total     : {last?.Cumulative ?? 0}/{dungeon.TotalCount} " +
                          $"({last?.CumulativePercent ?? 0:F2}%)");

        foreach (var warning in RouteHealth.Check(
                     route, dungeon, forces, data.AddonVersion, saved?.DungeonMappingHash))
        {
            Console.WriteLine();
            Console.WriteLine($"⚠ {warning.Message}");
        }

        var options = route.Pulls.SelectMany(p => p.UnknownOptions).Distinct().ToList();
        if (options.Count > 0)
            Console.WriteLine($"⚠ unrecognised pull option key(s): {string.Join(", ", options)}");

        return 0;
    }

    // ---- the library -------------------------------------------------------------------

    private static int Save(string[] args)
    {
        if (ReadRouteArg(args, "save <string>|- [--name <name>]") is not { } routeString) return 2;

        var data = new DungeonDataService().LoadCached();
        var route = RouteDecoder.Decode(routeString);
        var dungeon = data?.Find(route.DungeonIndex);

        var library = new RouteLibrary();
        var saved = library.Save(routeString, dungeon, data?.AddonVersion, OptionValue(args, "--name"));

        Console.WriteLine($"saved     : {saved.Id}");
        Console.WriteLine($"name      : {saved.DisplayName}");
        Console.WriteLine($"dungeon   : [{saved.DungeonIndex}] {saved.DungeonName ?? "not in the cache"}");
        Console.WriteLine($"pulls     : {saved.PullCount}");
        Console.WriteLine($"library   : {library.Root}");

        if (saved.DungeonMappingHash is null)
            Console.WriteLine("⚠ No dungeon data cached, so no mapping fingerprint was recorded — a " +
                              "later re-map of this dungeon will not be detectable for this route. " +
                              "Run `mdtdesk data update`, then save it again.");
        else
            Console.WriteLine($"mapping   : {saved.DungeonMappingHash} (MDT {saved.ImportedUnderMdtVersion})");

        return 0;
    }

    private static int ListSaved()
    {
        var library = new RouteLibrary();
        var routes = library.List();

        Console.WriteLine($"library : {library.Root}");
        if (routes.Count == 0)
        {
            Console.WriteLine("(empty — add one with `mdtdesk route save <string>|-`)");
            return 0;
        }

        var data = new DungeonDataService().LoadCached();
        Console.WriteLine();
        Console.WriteLine($"{"id",-16} {"route",-28} {"dungeon",-22} {"pulls",5}  {"imported",10}  state");

        foreach (var saved in routes)
        {
            var state = RouteLibrary.HasDungeonChangedSinceImport(saved, data?.Find(saved.DungeonIndex)) switch
            {
                true => "⚠ dungeon re-mapped since import",
                false => "ok",
                // Never say "ok" when we simply cannot tell.
                null => "unknown (no fingerprint / no cache)",
            };

            Console.WriteLine($"{Truncate(saved.Id, 16),-16} {Truncate(saved.DisplayName, 28),-28} " +
                              $"{Truncate(saved.DungeonName ?? $"[{saved.DungeonIndex}]", 22),-22} " +
                              $"{saved.PullCount,5}  {saved.ImportedUtc,10:yyyy-MM-dd}  {state}");
        }

        return 0;
    }

    private static int ShowSaved(string[] args)
    {
        if (args.Length == 0)
        {
            Console.Error.WriteLine("Usage: mdtdesk route show <id>   (see `mdtdesk route list`)");
            return 2;
        }

        var saved = new RouteLibrary().Find(args[0]);
        if (saved is null)
        {
            Console.Error.WriteLine($"No saved route '{args[0]}'. See `mdtdesk route list`.");
            return 1;
        }

        // Decoded fresh from the stored string, which is the source of truth.
        return Report(saved.RouteString, saved);
    }

    private static int RemoveSaved(string[] args)
    {
        if (args.Length == 0)
        {
            Console.Error.WriteLine("Usage: mdtdesk route remove <id>");
            return 2;
        }

        if (!new RouteLibrary().Remove(args[0]))
        {
            Console.Error.WriteLine($"No saved route '{args[0]}'.");
            return 1;
        }

        Console.WriteLine($"removed {args[0]}");
        return 0;
    }

    // ---- helpers -----------------------------------------------------------------------

    /// <summary>
    /// A route string is long and full of characters a shell will fight over, so <c>-</c> reads
    /// it from stdin.
    /// </summary>
    private static string? ReadRouteArg(string[] args, string usage)
    {
        var input = args.FirstOrDefault(a => !a.StartsWith("--"));
        var value = input == "-" ? Console.In.ReadToEnd() : input;

        if (string.IsNullOrWhiteSpace(value))
        {
            Console.Error.WriteLine($"Usage: mdtdesk route {usage}   (- reads stdin)");
            return null;
        }

        return value;
    }

    private static string? OptionValue(string[] args, string name)
    {
        var i = Array.IndexOf(args, name);
        return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
    }

    private static string Truncate(string s, int width)
        => s.Length <= width ? s : s[..(width - 1)] + "…";
}

using System.Text.Json;
using MdtDesktop.Cli;
using MdtDesktop.Core.Data;
using MdtDesktop.Core.Lua;
using MdtDesktop.Core.Routes;

// The headless driver. Every data milestone is verifiable here before any UI
// exists, and it stays useful afterwards as the debugging door into Core.

return await Cli.RunAsync(args);

internal static class Cli
{
    private const string Usage = """
        mdtdesk — MDT Desktop command line

        Usage:
          mdtdesk data update [--force]  Fetch the latest MDT release and rebuild the dungeon cache.
          mdtdesk data list              List the cached dungeons with their MDT indices.
          mdtdesk data show <idx>        Detail one dungeon: forces, sublevels, enemy table.
          mdtdesk map <idx> [--sublevel <n>] [--plot]
                                         Where the map draws a dungeon's blips, headlessly.
          mdtdesk roles [<idx>] [--all]  What role every mob classifies as, and the census.
          mdtdesk pulls <str>|-|<id> [--sublevel <n>] [--current <n>] [--plot]
                                         The route overlay: hulls, colours, forces, per pull.
          mdtdesk route decode <str>|- [--json]
                                         Decode a route string; print its pulls and forces.
          mdtdesk route save <str>|- [--name <n>]
                                         Import a route into the local library.
          mdtdesk route list             List saved routes and whether their dungeon has moved.
          mdtdesk route show <id>        Decode a saved route.
          mdtdesk route remove <id>      Delete a saved route.
          mdtdesk lua-check              Report the resolved Lua interpreter and round-trip a script.
          mdtdesk help                   This text.
        """;

    public static async Task<int> RunAsync(string[] args)
    {
        var command = args.Length > 0 ? args[0] : "help";

        try
        {
            switch (command)
            {
                case "data":
                    return await DataCommands.RunAsync(args[1..]);

                case "map":
                    return MapCommands.Run(args[1..]);

                case "roles":
                    return RoleCommands.Run(args[1..]);

                case "pulls":
                    return PullCommands.Run(args[1..]);

                case "route":
                    return await RouteCommands.RunAsync(args[1..]);

                case "lua-check":
                    return await LuaCheckAsync(args[1..]);

                case "help" or "--help" or "-h":
                    Console.WriteLine(Usage);
                    return 0;

                default:
                    Console.Error.WriteLine($"Unknown command '{command}'.");
                    Console.Error.WriteLine();
                    Console.Error.WriteLine(Usage);
                    return 2;
            }
        }
        catch (LuaException ex)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
        catch (RouteDecodeException ex)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
        catch (DataUpdateException ex)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
        catch (HttpRequestException ex)
        {
            Console.Error.WriteLine($"Could not reach GitHub: {ex.Message}");
            return 1;
        }
    }

    private static async Task<int> LuaCheckAsync(string[] _)
    {
        var runner = new LuaRunner();
        Console.WriteLine($"interpreter : {runner.InterpreterPath}");
        Console.WriteLine($"version     : {await runner.VersionAsync()}");
        Console.WriteLine($"scripts     : {LuaInterpreter.ScriptDirectory}");

        const string probe = "mdt-desktop sidecar probe";
        var stdout = await runner.RunAsync(
            LuaInterpreter.Script("roundtrip.lua"), stdin: probe, args: ["lua-check"]);

        using var document = JsonDocument.Parse(stdout);
        var root = document.RootElement;
        var echoed = root.GetProperty("stdin").GetString();

        Console.WriteLine($"round-trip  : {(echoed == probe ? "ok" : "MISMATCH")} " +
                          $"({root.GetProperty("stdinBytes").GetInt32()} bytes in, " +
                          $"{stdout.Length} bytes of JSON out)");

        return echoed == probe ? 0 : 1;
    }
}

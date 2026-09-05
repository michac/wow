using System.Runtime.InteropServices;

namespace MdtDesktop.Core.Lua;

/// <summary>
/// Locates the Lua 5.4 interpreter the sidecar runs on, and the scripts it runs.
/// </summary>
/// <remarks>
/// The shipped app uses the bundled <c>lua/lua54.exe</c>, which is committed so a
/// first run needs no network and no installed Lua. Development happens under WSL,
/// where that Windows binary does run (binfmt_misc interop translates the script
/// path too — measured, not assumed) but a native <c>lua5.4</c> on PATH is the
/// plainer path and is preferred off-Windows. <c>MDTDESK_LUA</c> overrides both.
/// </remarks>
public static class LuaInterpreter
{
    /// <summary>Environment variable that pins the interpreter explicitly.</summary>
    public const string OverrideVariable = "MDTDESK_LUA";

    private static readonly string[] PathCandidates = ["lua5.4", "lua54", "lua"];

    /// <summary>Directory holding the bundled interpreter and the sidecar scripts.</summary>
    public static string ScriptDirectory { get; } =
        Path.Combine(AppContext.BaseDirectory, "lua");

    /// <summary>Absolute path of a sidecar script shipped in <see cref="ScriptDirectory"/>.</summary>
    public static string Script(string fileName)
    {
        var path = Path.Combine(ScriptDirectory, fileName);
        if (!File.Exists(path))
            throw new FileNotFoundException($"Sidecar script '{fileName}' is not in {ScriptDirectory}.", path);
        return path;
    }

    /// <summary>
    /// Resolves the interpreter to run, or throws with every location that was tried.
    /// </summary>
    public static string Resolve()
    {
        var tried = new List<string>();

        var pinned = Environment.GetEnvironmentVariable(OverrideVariable);
        if (!string.IsNullOrWhiteSpace(pinned))
        {
            if (File.Exists(pinned)) return pinned;
            var onPath = FindOnPath(pinned);
            if (onPath is not null) return onPath;
            throw new LuaException(
                $"{OverrideVariable} is set to '{pinned}', which is neither a file nor on PATH.");
        }

        var bundled = Path.Combine(ScriptDirectory, "lua54.exe");
        var windows = RuntimeInformation.IsOSPlatform(OSPlatform.Windows);

        if (windows)
        {
            if (File.Exists(bundled)) return bundled;
            tried.Add(bundled);
        }

        foreach (var candidate in PathCandidates)
        {
            var found = FindOnPath(candidate);
            if (found is not null) return found;
            tried.Add($"{candidate} (PATH)");
        }

        if (!windows)
        {
            // Last resort off-Windows: the bundled binary runs fine under WSL interop.
            if (File.Exists(bundled)) return bundled;
            tried.Add(bundled);
        }

        throw new LuaException(
            "No Lua 5.4 interpreter found. Tried: " + string.Join(", ", tried) +
            $". Set {OverrideVariable} to pin one.");
    }

    private static string? FindOnPath(string name)
    {
        if (name.Contains(Path.DirectorySeparatorChar) || name.Contains('/')) return null;

        var pathVar = Environment.GetEnvironmentVariable("PATH");
        if (string.IsNullOrEmpty(pathVar)) return null;

        var extensions = RuntimeInformation.IsOSPlatform(OSPlatform.Windows)
            ? new[] { ".exe", ".cmd", ".bat", "" }
            : [""];

        foreach (var dir in pathVar.Split(Path.PathSeparator))
        {
            if (string.IsNullOrWhiteSpace(dir)) continue;
            foreach (var ext in extensions)
            {
                string candidate;
                try { candidate = Path.Combine(dir, name + ext); }
                catch (ArgumentException) { break; }   // a malformed PATH entry
                if (File.Exists(candidate)) return candidate;
            }
        }

        return null;
    }
}

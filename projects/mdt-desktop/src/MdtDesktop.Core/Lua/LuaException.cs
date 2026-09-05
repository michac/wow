namespace MdtDesktop.Core.Lua;

/// <summary>A sidecar invocation that failed, carrying the Lua traceback when there was one.</summary>
public sealed class LuaException : Exception
{
    public LuaException(string message) : base(message) { }

    public LuaException(string message, int exitCode, string stderr, string stdout)
        : base(Compose(message, exitCode, stderr, stdout))
    {
        ExitCode = exitCode;
        StandardError = stderr;
        StandardOutput = stdout;
    }

    /// <summary>Process exit code, or <c>null</c> when the failure was before/around the run.</summary>
    public int? ExitCode { get; }

    /// <summary>Everything the interpreter wrote to stderr — the traceback lives here.</summary>
    public string StandardError { get; } = string.Empty;

    /// <summary>Whatever reached stdout before the failure. Useful when the JSON is truncated.</summary>
    public string StandardOutput { get; } = string.Empty;

    private static string Compose(string message, int exitCode, string stderr, string stdout)
    {
        var text = $"{message} (exit {exitCode})";
        if (!string.IsNullOrWhiteSpace(stderr))
            text += Environment.NewLine + "--- lua stderr ---" + Environment.NewLine + stderr.TrimEnd();
        if (!string.IsNullOrWhiteSpace(stdout))
        {
            var head = stdout.Length > 2000 ? stdout[..2000] + "…" : stdout;
            text += Environment.NewLine + "--- lua stdout ---" + Environment.NewLine + head.TrimEnd();
        }
        return text;
    }
}

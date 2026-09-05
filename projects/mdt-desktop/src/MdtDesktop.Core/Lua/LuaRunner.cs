using System.Diagnostics;
using System.Text;

namespace MdtDesktop.Core.Lua;

/// <summary>
/// Runs a Lua script as a child process: text in on stdin, text out on stdout.
/// </summary>
/// <remarks>
/// This is the whole Lua strategy — option (1), shell out to a real interpreter,
/// so MDT's own data files and (from M5) its own vendored libraries are read by
/// the language that wrote them. Nothing here parses Lua.
/// </remarks>
public sealed class LuaRunner
{
    private static readonly UTF8Encoding Utf8NoBom = new(encoderShouldEmitUTF8Identifier: false);

    /// <param name="interpreterPath">Interpreter to run; defaults to <see cref="LuaInterpreter.Resolve"/>.</param>
    public LuaRunner(string? interpreterPath = null)
        => InterpreterPath = interpreterPath ?? LuaInterpreter.Resolve();

    /// <summary>The resolved interpreter this runner invokes.</summary>
    public string InterpreterPath { get; }

    /// <summary>The interpreter's own version banner, e.g. <c>Lua 5.4.2 …</c>.</summary>
    public async Task<string> VersionAsync(CancellationToken ct = default)
    {
        // `lua -v` prints the banner and exits; 5.4 puts it on stdout, older ones on stderr.
        var result = await ExecuteAsync(["-v"], stdin: null, workingDirectory: null, ct)
            .ConfigureAwait(false);
        if (result.ExitCode != 0)
            throw new LuaException("Could not read the interpreter version",
                result.ExitCode, result.StandardError, result.StandardOutput);

        var banner = result.StandardOutput.Trim();
        return banner.Length > 0 ? banner : result.StandardError.Trim();
    }

    /// <summary>
    /// Runs <paramref name="scriptPath"/> and returns its stdout.
    /// </summary>
    /// <param name="scriptPath">Absolute path to the script.</param>
    /// <param name="stdin">Text fed to the script, or <c>null</c> to close stdin immediately.</param>
    /// <param name="args">Arguments the script sees in <c>...</c>.</param>
    /// <param name="workingDirectory">
    /// Directory to run in. When <c>null</c> a fresh temp directory is created for the
    /// run and removed afterwards, so a script that writes scratch files cannot litter.
    /// </param>
    /// <exception cref="LuaException">
    /// Non-zero exit, or anything on stderr — the traceback is attached to the message.
    /// </exception>
    public async Task<string> RunAsync(
        string scriptPath,
        string? stdin = null,
        IReadOnlyList<string>? args = null,
        string? workingDirectory = null,
        CancellationToken ct = default)
    {
        if (!File.Exists(scriptPath))
            throw new FileNotFoundException($"Lua script not found: {scriptPath}", scriptPath);

        var argv = new List<string> { scriptPath };
        if (args is not null) argv.AddRange(args);

        string? scratch = null;
        if (workingDirectory is null)
        {
            scratch = Path.Combine(Path.GetTempPath(), "mdtdesk-lua-" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(scratch);
            workingDirectory = scratch;
        }

        try
        {
            var result = await ExecuteAsync(argv, stdin, workingDirectory, ct).ConfigureAwait(false);

            if (result.ExitCode != 0 || result.StandardError.Trim().Length > 0)
                throw new LuaException($"Lua script '{Path.GetFileName(scriptPath)}' failed",
                    result.ExitCode, result.StandardError, result.StandardOutput);

            return result.StandardOutput;
        }
        finally
        {
            if (scratch is not null)
                try { Directory.Delete(scratch, recursive: true); } catch (IOException) { /* best effort */ }
        }
    }

    /// <summary>Writes <paramref name="source"/> to a temp file and runs it. For tests and one-liners.</summary>
    public async Task<string> RunSourceAsync(
        string source,
        string? stdin = null,
        IReadOnlyList<string>? args = null,
        CancellationToken ct = default)
    {
        var path = Path.Combine(Path.GetTempPath(), "mdtdesk-" + Guid.NewGuid().ToString("N") + ".lua");
        await File.WriteAllTextAsync(path, source, Utf8NoBom, ct).ConfigureAwait(false);
        try { return await RunAsync(path, stdin, args, workingDirectory: null, ct).ConfigureAwait(false); }
        finally { try { File.Delete(path); } catch (IOException) { /* best effort */ } }
    }

    private readonly record struct ProcessResult(int ExitCode, string StandardOutput, string StandardError);

    private async Task<ProcessResult> ExecuteAsync(
        IReadOnlyList<string> argv, string? stdin, string? workingDirectory, CancellationToken ct)
    {
        var info = new ProcessStartInfo(InterpreterPath)
        {
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            WorkingDirectory = workingDirectory ?? Environment.CurrentDirectory,
            StandardOutputEncoding = Utf8NoBom,
            StandardErrorEncoding = Utf8NoBom,
        };
        foreach (var arg in argv) info.ArgumentList.Add(arg);

        using var process = new Process { StartInfo = info };

        try { process.Start(); }
        catch (Exception ex)
        {
            throw new LuaException($"Could not start the Lua interpreter at '{InterpreterPath}': {ex.Message}");
        }

        // Both pipes are drained concurrently with the write; reading them in
        // sequence deadlocks the moment either fills its buffer.
        var stdoutTask = process.StandardOutput.ReadToEndAsync(ct);
        var stderrTask = process.StandardError.ReadToEndAsync(ct);

        try
        {
            if (stdin is not null)
                await process.StandardInput.WriteAsync(stdin.AsMemory(), ct).ConfigureAwait(false);
        }
        catch (IOException)
        {
            // The script closed stdin early (a `read("l")` that stopped reading). Not an error
            // in itself — whatever it did next decides the exit code.
        }
        finally
        {
            process.StandardInput.Close();
        }

        try
        {
            await process.WaitForExitAsync(ct).ConfigureAwait(false);
        }
        catch (OperationCanceledException)
        {
            try { process.Kill(entireProcessTree: true); } catch (InvalidOperationException) { }
            throw;
        }

        return new ProcessResult(
            process.ExitCode,
            await stdoutTask.ConfigureAwait(false),
            await stderrTask.ConfigureAwait(false));
    }
}

using System.Text.Json;
using MdtDesktop.Core.Lua;

namespace MdtDesktop.Core.Tests.Lua;

public class LuaRunnerTests
{
    private static LuaRunner Runner() => new();

    [Fact]
    public async Task Version_reports_lua_54()
    {
        var version = await Runner().VersionAsync();
        Assert.StartsWith("Lua 5.4", version);
    }

    [Fact]
    public async Task Roundtrip_script_echoes_stdin_and_args_as_json()
    {
        const string payload = "hello \"sidecar\"\nsecond line\tтекст";

        var stdout = await Runner().RunAsync(
            LuaInterpreter.Script("roundtrip.lua"), stdin: payload, args: ["alpha", "beta"]);

        using var document = JsonDocument.Parse(stdout);
        var root = document.RootElement;

        Assert.Equal(payload, root.GetProperty("stdin").GetString());
        Assert.Equal(["alpha", "beta"],
            root.GetProperty("args").EnumerateArray().Select(e => e.GetString()!).ToArray());
        Assert.StartsWith("Lua 5.4", root.GetProperty("lua").GetString());
    }

    [Fact]
    public async Task Empty_stdin_is_not_an_error()
    {
        var stdout = await Runner().RunAsync(LuaInterpreter.Script("roundtrip.lua"), stdin: null);

        using var document = JsonDocument.Parse(stdout);
        Assert.Equal(0, document.RootElement.GetProperty("stdinBytes").GetInt32());
    }

    [Fact]
    public async Task A_failing_script_throws_with_the_traceback_attached()
    {
        var ex = await Assert.ThrowsAsync<LuaException>(() =>
            Runner().RunAsync(LuaInterpreter.Script("roundtrip.lua"), args: ["fail"]));

        Assert.Equal(1, ex.ExitCode);
        Assert.Contains("asked to fail", ex.StandardError);
        Assert.Contains("stack traceback", ex.StandardError);
        Assert.Contains("asked to fail", ex.Message);   // the traceback reaches the message too
    }

    [Fact]
    public async Task A_script_that_only_warns_on_stderr_still_fails_the_run()
    {
        // The contract is strict on purpose: stdout is a JSON channel, and a script
        // that chatters on stderr is a script whose stdout we have not thought about.
        var ex = await Assert.ThrowsAsync<LuaException>(() =>
            Runner().RunSourceAsync("io.stderr:write('a warning\\n') io.write('{}')"));

        Assert.Equal(0, ex.ExitCode);
        Assert.Contains("a warning", ex.StandardError);
    }

    [Fact]
    public async Task Large_output_does_not_deadlock_the_pipes()
    {
        // 4 MB is well past any pipe buffer; the real dungeon JSON will be bigger still.
        var stdout = await Runner().RunSourceAsync(
            "io.write(string.rep('x', 4 * 1024 * 1024))");

        Assert.Equal(4 * 1024 * 1024, stdout.Length);
    }

    [Fact]
    public async Task Cancellation_kills_the_child()
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromMilliseconds(200));

        await Assert.ThrowsAnyAsync<OperationCanceledException>(() =>
            Runner().RunSourceAsync("while true do end", ct: cts.Token));
    }

    [Fact]
    public void A_missing_script_is_a_FileNotFoundException_not_a_lua_failure()
    {
        Assert.Throws<FileNotFoundException>(() => LuaInterpreter.Script("no-such-script.lua"));
    }

    [Fact]
    public void A_pinned_interpreter_that_does_not_exist_is_reported_as_such()
    {
        var previous = Environment.GetEnvironmentVariable(LuaInterpreter.OverrideVariable);
        try
        {
            Environment.SetEnvironmentVariable(LuaInterpreter.OverrideVariable, "/definitely/not/lua");
            var ex = Assert.Throws<LuaException>(LuaInterpreter.Resolve);
            Assert.Contains(LuaInterpreter.OverrideVariable, ex.Message);
        }
        finally
        {
            Environment.SetEnvironmentVariable(LuaInterpreter.OverrideVariable, previous);
        }
    }
}

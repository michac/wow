using System.Text.Json;
using System.Text.Json.Serialization;

namespace MdtDesktop.Core.Library;

/// <summary>
/// What the app remembers between launches: where the window was, how it was framed, and which
/// keys advance the pull.
/// </summary>
/// <remarks>
/// <para>
/// ⚠ This is <b>user data</b>, so it lives under <see cref="Environment.SpecialFolder.ApplicationData"/>
/// beside <c>routes/</c> — never under the dungeon cache, where "delete it and re-fetch" is a
/// documented recovery step that would take these with it.
/// </para>
/// <para>
/// ⚠ And beside <c>routes/</c>, never <b>inside</b> it: <see cref="RouteLibrary.List"/> reads
/// every <c>*.json</c> in its own folder as a saved route, so a settings file dropped in there
/// would be parsed as one, silently skipped, and eventually deleted by a <c>remove</c>.
/// </para>
/// <para>
/// The load/save lives here rather than in the WPF project for the usual reason: it is the part
/// that can be wrong, so it is the part that is tested. <c>App</c> keeps only the window plumbing.
/// </para>
/// </remarks>
public sealed record AppSettings
{
    /// <summary>Schema version, so a later shape change can migrate rather than guess.</summary>
    public int Version { get; init; } = 1;

    public WindowPlacement? Window { get; init; }

    /// <summary>
    /// Zoom as a multiple of "fit to viewport", not an absolute scale.
    /// </summary>
    /// <remarks>
    /// ⚠ An absolute scale means resizing the window silently re-frames the map, because the fit
    /// scale depends on the viewport. 1.0 reproduces the plain fit, which is what the app does
    /// today with nothing remembered.
    /// </remarks>
    public double ZoomRelativeToFit { get; init; } = 1;

    public bool AlwaysOnTop { get; init; }

    /// <summary>Borderless/kiosk — no chrome, for the second monitor.</summary>
    public bool Borderless { get; init; }

    /// <summary>Advance the pull. Parsed by <see cref="HotKeySpec.TryParse"/>.</summary>
    public string NextPullHotKey { get; init; } = "F2";

    /// <summary>Go back a pull.</summary>
    public string PreviousPullHotKey { get; init; } = "Shift+F2";

    /// <summary>The dungeon shown last, so a launch lands where you left it.</summary>
    public int? LastDungeonIndex { get; init; }

    /// <summary>The saved route loaded last.</summary>
    public string? LastRouteId { get; init; }
}

/// <summary>Where the window was. Device-independent WPF units, as <c>Window.Left</c> reports them.</summary>
public readonly record struct WindowPlacement(
    double Left, double Top, double Width, double Height, bool Maximized)
{
    /// <summary>
    /// Nudges a remembered placement back onto a screen that actually exists.
    /// </summary>
    /// <param name="screens">
    /// The current monitors' working areas. Empty means "we could not ask", and the placement is
    /// returned untouched rather than reset — losing the user's framing over a failed query is
    /// worse than the risk it was guarding against.
    /// </param>
    /// <remarks>
    /// ⚠ The failure this prevents is unrecoverable from inside the app: a window restored onto a
    /// monitor that has since been unplugged is invisible, and the only fix is deleting a file
    /// the user does not know exists.
    /// <para>
    /// ⚠ It deliberately does <b>not</b> clamp <see cref="Top"/> to zero. A monitor placed above
    /// the primary one has negative coordinates, and a naive <c>Math.Max(0, top)</c> would drag
    /// the window off it every launch — which is the classic bug in this exact function.
    /// </para>
    /// </remarks>
    public WindowPlacement ClampToVisible(IReadOnlyList<WindowPlacement> screens)
    {
        if (screens.Count == 0) return this;

        // Copied to a local because a struct's members are not reachable from a lambda.
        var me = this;

        // "Visible" means a real overlap, not a shared edge: a window whose right edge touches a
        // monitor's left edge shows nothing at all.
        var visible = screens.Any(s =>
            me.Left < s.Left + s.Width && me.Left + me.Width > s.Left &&
            me.Top < s.Top + s.Height && me.Top + me.Height > s.Top);

        if (visible) return this;

        // The monitor it remembers is gone. Centre it on the first one — the primary, as the
        // caller enumerates them — at a size that fits there.
        var home = screens[0];
        var width = Math.Min(Width, home.Width);
        var height = Math.Min(Height, home.Height);

        return this with
        {
            Left = home.Left + (home.Width - width) / 2,
            Top = home.Top + (home.Height - height) / 2,
            Width = width,
            Height = height,
        };
    }
}

/// <summary>Reads and writes <c>settings.json</c>. Never throws on a bad file.</summary>
public sealed class SettingsStore
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };

    /// <param name="path">
    /// Defaults to <c>%APPDATA%\MdtDesktop\settings.json</c> — a sibling of <c>routes/</c>, not
    /// a file in it.
    /// </param>
    public SettingsStore(string? path = null)
        => Path = path ?? System.IO.Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "MdtDesktop", "settings.json");

    public string Path { get; }

    /// <summary>
    /// The saved settings, or the defaults.
    /// </summary>
    /// <remarks>
    /// A corrupt or unreadable file yields defaults rather than an exception. Losing a remembered
    /// window position is a shrug; failing to start over one is not.
    /// </remarks>
    public AppSettings Load()
    {
        try
        {
            return File.Exists(Path)
                ? JsonSerializer.Deserialize<AppSettings>(File.ReadAllText(Path), JsonOptions) ?? new()
                : new AppSettings();
        }
        catch (Exception ex) when (ex is JsonException or IOException or UnauthorizedAccessException)
        {
            return new AppSettings();
        }
    }

    /// <summary>
    /// Writes the settings, via a temporary file so a crash mid-write cannot leave a torn one.
    /// </summary>
    /// <returns>False when it could not be written — the caller decides whether that is worth saying.</returns>
    public bool Save(AppSettings settings)
    {
        try
        {
            Directory.CreateDirectory(System.IO.Path.GetDirectoryName(Path)!);

            var temp = Path + ".tmp";
            File.WriteAllText(temp, JsonSerializer.Serialize(settings, JsonOptions));
            File.Move(temp, Path, overwrite: true);
            return true;
        }
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException)
        {
            return false;
        }
    }
}

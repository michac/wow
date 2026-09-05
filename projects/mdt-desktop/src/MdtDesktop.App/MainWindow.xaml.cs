using System.Collections.ObjectModel;
using System.IO;
using System.Net.Http;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using MdtDesktop.App.HotKeys;
using MdtDesktop.Core.Data;
using MdtDesktop.Core.Input;
using MdtDesktop.Core.Library;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.App;

/// <summary>
/// The viewer window: pick a dungeon, load a route, advance the pull with a hotkey.
/// </summary>
/// <remarks>
/// It holds no parsing and no arithmetic. <c>Core</c> owns the data, the layout, the forces, the
/// route overlay, the hotkey parsing, the pull cursor and the window-restore guard; this binds
/// them to controls. The same paths are exercised headlessly by <c>mdtdesk pulls</c> and
/// <c>mdtdesk roles</c>, so a disagreement between the two is a UI bug.
/// </remarks>
public partial class MainWindow : Window
{
    private const int HotKeyNext = 1;
    private const int HotKeyPrevious = 2;

    private readonly DungeonDataService _service = new();
    private readonly RouteLibrary _library = new();
    private readonly SettingsStore _settingsStore = new();
    private readonly ObservableCollection<PullRow> _pullRows = [];

    private AppSettings _settings = new();
    private DungeonData? _data;
    private MobRoleIndex? _roles;
    private GlobalHotKey? _hotKeys;

    private SavedRoute? _savedRoute;
    private Route? _route;
    private PullCursor _cursor = new(0);
    private string _hotKeyStatus = "";
    private bool _loading;
    private bool _kiosk;

    public MainWindow()
    {
        InitializeComponent();
        PullList.ItemsSource = _pullRows;
        _settings = _settingsStore.Load();
    }

    /// <summary>Bound to F11, which has to keep working once the toolbar is hidden.</summary>
    public ICommand ToggleKioskCommand => new RelayCommand(() => SetKiosk(!_kiosk));

    private Dungeon? SelectedDungeon => (DungeonPicker.SelectedItem as DungeonChoice)?.Dungeon;

    private int SelectedSubLevel => (SubLevelPicker.SelectedItem as SubLevelChoice)?.Index ?? 1;

    // ---- lifetime --------------------------------------------------------------------------

    /// <summary>
    /// ⚠ Hotkeys register here, not in <c>Loaded</c>: <c>RegisterHotKey</c> needs the window
    /// HWND, and the handle does not exist until the source is initialised.
    /// </summary>
    protected override void OnSourceInitialized(EventArgs e)
    {
        base.OnSourceInitialized(e);

        RestorePlacement();

        try
        {
            _hotKeys = new GlobalHotKey(this);
            _hotKeys.Pressed += OnHotKeyPressed;
            RegisterHotKeys();
        }
        catch (InvalidOperationException ex)
        {
            _hotKeyStatus = $"⚠ Global hotkeys unavailable: {ex.Message}";
        }
    }

    protected override void OnClosed(EventArgs e)
    {
        // ⚠ A leaked registration lives until the process exits and blocks the same combination
        // on the next launch, so the app would refuse its own hotkey after one unclean close.
        _hotKeys?.Dispose();
        base.OnClosed(e);
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        Map.DefaultRelativeZoom = _settings.ZoomRelativeToFit;
        ApplySettingsToChrome();
        LoadCache();
        LoadRouteList();
    }

    private void OnWindowClosing(object sender, System.ComponentModel.CancelEventArgs e)
        => SaveSettings();

    // ---- the dungeon cache -----------------------------------------------------------------

    private void LoadCache()
    {
        _data = _service.LoadCached();

        if (_data is null || _data.Dungeons.Count == 0)
        {
            Map.Clear();
            DungeonPicker.ItemsSource = null;
            Status.Text = $"No dungeon data cached in {_service.Cache.Root}. " +
                          "Press “Update MDT data” to fetch MDT's latest release.";
            return;
        }

        // Built once per cache: the miniboss bar is a median over every dungeon, so it is not a
        // per-dungeon question and must not be recomputed per selection.
        _roles = MobRoleIndex.Build(_data);

        _loading = true;
        DungeonPicker.ItemsSource = _data.Dungeons
            .OrderBy(d => d.DisplayName, StringComparer.CurrentCultureIgnoreCase)
            .Select(d => new DungeonChoice(d))
            .ToList();
        _loading = false;

        var remembered = (DungeonPicker.ItemsSource as IEnumerable<DungeonChoice>)?
            .ToList().FindIndex(c => c.Dungeon.Index == _settings.LastDungeonIndex) ?? -1;

        DungeonPicker.SelectedIndex = remembered >= 0 ? remembered : 0;
    }

    private void OnDungeonChanged(object sender, SelectionChangedEventArgs e)
    {
        if (_loading || SelectedDungeon is not { } dungeon) return;

        _loading = true;
        SubLevelPicker.ItemsSource = dungeon.SubLevels.Select(s => new SubLevelChoice(s)).ToList();
        _loading = false;
        SubLevelPicker.SelectedIndex = 0;

        // Every Midnight dungeon ships exactly one sublevel, so the picker would be a control
        // with nothing to choose. It appears the day one ships two.
        var many = dungeon.SubLevels.Count > 1 ? Visibility.Visible : Visibility.Collapsed;
        SubLevelPicker.Visibility = SubLevelLabel.Visibility = many;

        ShowMap();
    }

    private void OnSubLevelChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_loading) ShowMap();
    }

    private void ShowMap()
    {
        if (SelectedDungeon is not { } dungeon) return;

        var result = Map.Load(dungeon, SelectedSubLevel, _service.Cache, _roles);

        // A route for another dungeon must not stay on screen over this one's mobs.
        if (_route is not null && _route.DungeonIndex != dungeon.Index) ClearRoute();
        else RedrawOverlay();

        var forces = Map.CurrentBlips.Sum(b => b.Forces);
        var tiles = result.TilesFound == MapGeometry.TilesPerSubLevel
            ? ""
            : $"  ⚠ {result.TilesFound}/{MapGeometry.TilesPerSubLevel} map tiles found";

        Status.Text =
            $"[{dungeon.Index}] {dungeon.DisplayName} — {result.BlipCount} mobs, " +
            $"{forces}/{dungeon.TotalCount} forces on the map, " +
            $"{dungeon.Enemies.Count(x => x.IsBoss)} bosses · MDT {_data?.AddonVersion}" +
            $"{tiles}{(_hotKeyStatus.Length > 0 ? "  ·  " + _hotKeyStatus : "")}";
    }

    // ---- routes ----------------------------------------------------------------------------

    private void LoadRouteList()
    {
        _loading = true;
        RoutePicker.ItemsSource = _library.List()
            .Select(r => new RouteChoice(r, _data?.Find(r.DungeonIndex)))
            .ToList();
        _loading = false;

        var remembered = (RoutePicker.ItemsSource as IEnumerable<RouteChoice>)?
            .ToList().FindIndex(c => c.Saved.Id == _settings.LastRouteId) ?? -1;

        if (remembered >= 0) RoutePicker.SelectedIndex = remembered;
    }

    private void OnImportClicked(object sender, RoutedEventArgs e)
    {
        var text = PasteBox.Text;

        // Refuse before decoding, so the message names the format rather than reading as a
        // corrupt string. The wording is Core's, shared with the CLI, so the two cannot drift.
        var format = RouteDecoder.Classify(text);
        if (format != RouteStringFormat.Modern)
        {
            Status.Text = RouteDecoder.DescribeRefusal(format);
            return;
        }

        try
        {
            var route = RouteDecoder.Decode(text);
            var dungeon = _data?.Find(route.DungeonIndex);
            var saved = _library.Save(text, dungeon, _data?.AddonVersion);

            PasteBox.Clear();
            LoadRouteList();

            var index = (RoutePicker.ItemsSource as IEnumerable<RouteChoice>)?
                .ToList().FindIndex(c => c.Saved.Id == saved.Id) ?? -1;
            if (index >= 0) RoutePicker.SelectedIndex = index;

            Status.Text = $"Imported “{saved.DisplayName}” — {saved.PullCount} pulls.";
        }
        catch (RouteDecodeException ex)
        {
            Status.Text = ex.Message;
        }
        // ⚠ RouteLibrary.Save writes a file. The CLI lets these reach a top-level handler; a
        // paste box has no such backstop, and an unhandled exception here kills the app.
        catch (Exception ex) when (ex is IOException or UnauthorizedAccessException)
        {
            Status.Text = $"Could not write to the route library ({_library.Root}): {ex.Message}";
        }
    }

    private void OnRouteChanged(object sender, SelectionChangedEventArgs e)
    {
        if (_loading || RoutePicker.SelectedItem is not RouteChoice choice) return;
        LoadRoute(choice.Saved);
    }

    private void LoadRoute(SavedRoute saved)
    {
        try
        {
            _route = RouteDecoder.Decode(saved.RouteString);
        }
        catch (RouteDecodeException ex)
        {
            Status.Text = $"“{saved.DisplayName}” no longer decodes: {ex.Message}";
            return;
        }

        _savedRoute = saved;
        _cursor = new PullCursor(_route.Pulls.Count);
        _cursor.Reset(_route.Pulls.Count, _route.CurrentPull);

        // Follow the route to its dungeon rather than drawing it over whatever is on screen.
        var index = (DungeonPicker.ItemsSource as IEnumerable<DungeonChoice>)?
            .ToList().FindIndex(c => c.Dungeon.Index == _route.DungeonIndex) ?? -1;

        if (index >= 0 && index != DungeonPicker.SelectedIndex) DungeonPicker.SelectedIndex = index;
        else RedrawOverlay();

        RouteHeader.Text = $"{saved.DisplayName} — {_route.Pulls.Count} pulls";
        RouteState.Text = DescribeState(saved);
    }

    /// <summary>
    /// ⚠ Three states, never two. <see cref="RouteLibrary.HasDungeonChangedSinceImport"/>
    /// returns null for "cannot tell", and rendering that as "ok" is exactly the reassurance
    /// the whole fingerprint exists to avoid giving.
    /// </summary>
    private string DescribeState(SavedRoute saved)
        => RouteLibrary.HasDungeonChangedSinceImport(saved, _data?.Find(saved.DungeonIndex)) switch
        {
            true => "⚠ dungeon re-mapped since import — its enemy and clone indices may now " +
                    "point at different mobs",
            false => "ok — the dungeon is unchanged since this route was imported",
            null => "unknown (no fingerprint / no cache) — a re-map could not be detected for this route",
        };

    private void ClearRoute()
    {
        _route = null;
        _savedRoute = null;
        _cursor = new PullCursor(0);
        _pullRows.Clear();

        Map.ClearOverlay();
        RouteHeader.Text = "No route loaded";
        RouteState.Text = "";
        RouteWarnings.Text = "";
        ForcesReadout.Text = "—";
    }

    private void OnForgetRouteClicked(object sender, RoutedEventArgs e)
    {
        if (_savedRoute is null) { ClearRoute(); return; }

        var name = _savedRoute.DisplayName;
        _library.Remove(_savedRoute.Id);

        ClearRoute();
        LoadRouteList();
        Status.Text = $"Removed “{name}” from the library.";
    }

    // ---- the overlay -----------------------------------------------------------------------

    private void RedrawOverlay()
    {
        if (_route is null || SelectedDungeon is not { } dungeon ||
            dungeon.Index != _route.DungeonIndex)
        {
            Map.ClearOverlay();
            return;
        }

        var overlay = RouteOverlay.Build(_route, dungeon, SelectedSubLevel, _cursor.Current);
        Map.ApplyOverlay(overlay);

        ForcesReadout.Text = overlay.ForcesReadout;
        RebuildPullList(overlay);

        // ⚠ The mapping hash has to be passed or the strongest warning — a dungeon re-mapped
        // since import — simply never fires.
        var warnings = RouteHealth.Check(
            _route, dungeon, overlay.Forces, _data?.AddonVersion, _savedRoute?.DungeonMappingHash);

        RouteWarnings.Text = string.Join("\n\n", warnings.Select(w => "⚠ " + w.Message));
    }

    private void RebuildPullList(RouteOverlayResult overlay)
    {
        _pullRows.Clear();
        foreach (var pull in overlay.Pulls) _pullRows.Add(new PullRow(pull));

        _loading = true;
        PullList.SelectedIndex = _pullRows
            .Select((row, i) => (row, i))
            .FirstOrDefault(x => x.row.Number == _cursor.Current, (null!, -1)).i;
        _loading = false;

        if (PullList.SelectedItem is not null) PullList.ScrollIntoView(PullList.SelectedItem);
    }

    private void OnPullSelected(object sender, SelectionChangedEventArgs e)
    {
        if (_loading || PullList.SelectedItem is not PullRow row) return;
        if (_cursor.MoveTo(row.Number)) RedrawOverlay();
    }

    private void OnNextPullClicked(object sender, RoutedEventArgs e) => Advance(+1);

    private void OnPreviousPullClicked(object sender, RoutedEventArgs e) => Advance(-1);

    private void Advance(int delta)
    {
        // The return value is what stops a keypress at the end of the route repainting 156 blips.
        if (delta > 0 ? _cursor.Next() : _cursor.Previous()) RedrawOverlay();
    }

    // ---- hotkeys ---------------------------------------------------------------------------

    private void RegisterHotKeys()
    {
        if (_hotKeys is null) return;

        var problems = new List<string>();

        Register(HotKeyNext, _settings.NextPullHotKey, "next pull");
        Register(HotKeyPrevious, _settings.PreviousPullHotKey, "previous pull");

        _hotKeyStatus = problems.Count > 0
            ? "⚠ " + string.Join("  ", problems)
            : $"{_settings.NextPullHotKey} next · {_settings.PreviousPullHotKey} previous";

        HotKeyHint.Text = _hotKeyStatus;

        void Register(int id, string binding, string what)
        {
            if (!HotKeySpec.TryParse(binding, out var spec))
            {
                problems.Add($"“{binding}” is not a usable hotkey, so {what} has none.");
                return;
            }

            // ⚠ The failure that matters: another process already owns the combination. It is
            // reported rather than swallowed, because the alternative is a key that silently
            // does nothing and an app that looks fine.
            if (!_hotKeys!.TryRegister(id, spec, out var error)) problems.Add(error!);
        }
    }

    private void OnHotKeyPressed(object? sender, int id) => Advance(id == HotKeyNext ? +1 : -1);

    // ---- chrome ----------------------------------------------------------------------------

    private void ApplySettingsToChrome()
    {
        Topmost = _settings.AlwaysOnTop;
        TopmostToggle.IsChecked = _settings.AlwaysOnTop;
        if (_settings.Borderless) SetKiosk(true);
    }

    private void OnTopmostChanged(object sender, RoutedEventArgs e)
        => Topmost = TopmostToggle.IsChecked == true;

    /// <summary>
    /// Kiosk: no chrome, no panels, just the map — what the second monitor is for.
    /// </summary>
    /// <remarks>
    /// ⚠ F11 is bound at the window, so there is always a way back out. A borderless window with
    /// no visible control and no working key is not recoverable without ending the process.
    /// </remarks>
    private void SetKiosk(bool on)
    {
        _kiosk = on;

        WindowStyle = on ? WindowStyle.None : WindowStyle.SingleBorderWindow;
        ResizeMode = on ? ResizeMode.NoResize : ResizeMode.CanResize;

        Toolbar.Visibility = RoutePanel.Visibility = on ? Visibility.Collapsed : Visibility.Visible;

        // The forces readout is the one thing worth keeping mid-dungeon, so it moves to the
        // status bar rather than disappearing with the panel.
        if (on && _route is not null)
            Status.Text = $"{RouteHeader.Text} · pull {_cursor.Current} · {ForcesReadout.Text} " +
                          $"· {_hotKeyStatus} · F11 to exit kiosk";
    }

    private void OnKioskClicked(object sender, RoutedEventArgs e) => SetKiosk(!_kiosk);

    /// <summary>Back to a plain fit — and it forgets the remembered zoom, which is the point
    /// of pressing it.</summary>
    private void OnFitClicked(object sender, RoutedEventArgs e)
    {
        Map.DefaultRelativeZoom = 1;
        Map.FitToViewport();
    }

    // ---- settings --------------------------------------------------------------------------

    /// <summary>
    /// ⚠ Restores through <see cref="WindowPlacement.ClampToVisible"/>, never raw. A window put
    /// back on a monitor that has since been unplugged is invisible, and the only way out is
    /// deleting a file the user does not know exists.
    /// </summary>
    private void RestorePlacement()
    {
        if (_settings.Window is not { } saved) return;

        var placement = saved.ClampToVisible(CurrentScreens());

        Left = placement.Left;
        Top = placement.Top;
        Width = placement.Width;
        Height = placement.Height;
        if (placement.Maximized) WindowState = WindowState.Maximized;
    }

    /// <summary>
    /// The monitors' working areas in WPF units, primary first.
    /// </summary>
    /// <remarks>
    /// Read through Win32 rather than WinForms so the project stays WPF-only, and scaled by the
    /// window's own DPI transform because <c>Window.Left</c> is in device-independent units
    /// while <c>EnumDisplayMonitors</c> is in pixels. An empty list means "could not ask", which
    /// <c>ClampToVisible</c> reads as "leave the placement alone".
    /// </remarks>
    private IReadOnlyList<WindowPlacement> CurrentScreens()
    {
        var source = PresentationSource.FromVisual(this);
        var toDip = source?.CompositionTarget?.TransformFromDevice ?? Matrix.Identity;

        return [.. Screens.Enumerate().Select(r =>
        {
            var topLeft = toDip.Transform(new Point(r.Left, r.Top));
            var bottomRight = toDip.Transform(new Point(r.Right, r.Bottom));
            return new WindowPlacement(
                topLeft.X, topLeft.Y,
                bottomRight.X - topLeft.X, bottomRight.Y - topLeft.Y, false);
        })];
    }

    private void SaveSettings()
    {
        // RestoreBounds is the non-maximized geometry, which is what should come back when the
        // window is un-maximized later. Left/Top read as the screen edge while maximized.
        var bounds = WindowState == WindowState.Normal
            ? new Rect(Left, Top, Width, Height)
            : RestoreBounds;

        _settings = _settings with
        {
            Window = new WindowPlacement(
                bounds.Left, bounds.Top, bounds.Width, bounds.Height,
                WindowState == WindowState.Maximized),
            ZoomRelativeToFit = Map.ZoomRelativeToFit,
            AlwaysOnTop = Topmost,
            Borderless = _kiosk,
            LastDungeonIndex = SelectedDungeon?.Index,
            LastRouteId = _savedRoute?.Id,
        };

        _settingsStore.Save(_settings);
    }

    // ---- data update -----------------------------------------------------------------------

    private async void OnUpdateClicked(object sender, RoutedEventArgs e)
    {
        UpdateButton.IsEnabled = false;
        var progress = new Progress<string>(line => Status.Text = line);

        try
        {
            var result = await _service.UpdateAsync(progress: progress);
            var stamp = result.Stamp;
            Status.Text = $"MDT {stamp.Tag}: {stamp.DungeonCount} dungeons, " +
                          $"{stamp.EnemyCount} enemies, {stamp.CloneCount} clones.";
            LoadCache();
            LoadRouteList();
        }
        catch (Exception ex) when (ex is DataUpdateException or HttpRequestException or IOException)
        {
            Status.Text = $"Update failed: {ex.Message}";
        }
        finally
        {
            UpdateButton.IsEnabled = true;
        }
    }
}

/// <summary>A dungeon as the picker shows it. The index is on the label because it is the
/// identity a route string uses, so it is what you cross-check against.</summary>
internal sealed record DungeonChoice(Dungeon Dungeon)
{
    public string Label => $"{Dungeon.DisplayName}  ({Dungeon.Index})";
}

internal sealed record SubLevelChoice(SubLevel SubLevel)
{
    public int Index => SubLevel.Index;
    public string Label => SubLevel.Name is { Length: > 0 } name ? name : SubLevel.Index.ToString();
}

/// <summary>
/// A saved route in the picker, carrying its staleness state.
/// </summary>
/// <remarks>
/// ⚠ The null case reads "unknown", never "ok". The same three strings the CLI prints, for the
/// same reason: a route whose provenance cannot be checked must not look like one that passed.
/// </remarks>
internal sealed record RouteChoice(SavedRoute Saved, Dungeon? Dungeon)
{
    public string Label
    {
        get
        {
            var state = RouteLibrary.HasDungeonChangedSinceImport(Saved, Dungeon) switch
            {
                true => "⚠ re-mapped",
                false => "ok",
                null => "unknown",
            };

            return $"{Saved.DisplayName} — {Saved.DungeonName ?? $"[{Saved.DungeonIndex}]"} " +
                   $"({Saved.PullCount} pulls, {state})";
        }
    }
}

/// <summary>One row of the pull list.</summary>
internal sealed class PullRow
{
    public PullRow(PullOverlay pull)
    {
        Number = pull.Number;

        var rgb = RouteOverlay.ParseColor(pull.Color) ?? (0x22, 0x8B, 0x22);
        var brush = new SolidColorBrush(Color.FromRgb(rgb.Item1, rgb.Item2, rgb.Item3));
        brush.Freeze();
        Swatch = brush;

        var forces = pull.Forces;
        var mobs = pull.MobKeys.Count;

        Detail = forces is null
            ? $"{mobs} mobs"
            : $"{mobs} mobs · +{forces.Forces} → {forces.Cumulative}/{forces.DungeonTotal} " +
              $"({forces.CumulativePercent:F1}%)" +
              (forces.Unresolved.Count > 0 ? $"  ⚠ {forces.Unresolved.Count} missing" : "");
    }

    public int Number { get; }
    public Brush Swatch { get; }
    public string Detail { get; }
}

/// <summary>The one command the window needs, so F11 works with the toolbar hidden.</summary>
internal sealed class RelayCommand(Action action) : ICommand
{
    public event EventHandler? CanExecuteChanged { add { } remove { } }
    public bool CanExecute(object? parameter) => true;
    public void Execute(object? parameter) => action();
}

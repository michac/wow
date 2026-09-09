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
    private readonly ObservableCollection<NoteRow> _noteRows = [];

    /// <summary>What the notes tab was last built for — see <see cref="RebuildNoteList"/>.</summary>
    private string? _noteListKey;

    private AppSettings _settings = new();
    private DungeonData? _data;
    private MobRoleIndex? _roles;
    private GlobalHotKey? _hotKeys;

    /// <summary>MDT's seasons plus the synthetic "Other" group, in MDT's own order.</summary>
    private List<Season> _seasons = [];

    /// <summary>The dungeon last shown in each season, so switching back returns to it.</summary>
    private readonly Dictionary<string, int> _dungeonBySeason = [];

    /// <summary>The route last loaded for each dungeon. Persisted; seeded from settings.</summary>
    private readonly Dictionary<int, string> _routeByDungeon = [];

    /// <summary>
    /// A route the user just named — set for the duration of an import, then cleared.
    /// </summary>
    /// <remarks>
    /// It beats the remembered route in <see cref="RouteSelection.Choose"/>, because it is the
    /// only id that reflects something the user did this second.
    /// </remarks>
    private string? _pendingRouteId;

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
        NoteList.ItemsSource = _noteRows;
        _settings = _settingsStore.Load();

        foreach (var (dungeon, route) in _settings.LastRouteByDungeon) _routeByDungeon[dungeon] = route;
    }

    /// <summary>Bound to F11, which has to keep working once the toolbar is hidden.</summary>
    public ICommand ToggleKioskCommand => new RelayCommand(() => SetKiosk(!_kiosk));

    private Season? SelectedSeason => (SeasonPicker.SelectedItem as SeasonChoice)?.Season;

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

        // ⚠ SeasonsWithOrphans, never Seasons: a dungeon MDT ships but files under no season
        // must stay reachable, and with no seasons declared at all the trailing group is the
        // flat list this picker used to be.
        _seasons = [.. _data.SeasonsWithOrphans()];

        _loading = true;
        SeasonPicker.ItemsSource = _seasons.Select(s => new SeasonChoice(s)).ToList();
        SeasonPicker.SelectedIndex = StartingSeasonIndex();
        _loading = false;

        // Seed the per-season memory so the first ApplySeason lands on the remembered dungeon.
        if (SelectedSeason is { } season && _settings.LastDungeonIndex is { } last &&
            season.Dungeons.Contains(last))
        {
            _dungeonBySeason[season.DisplayName] = last;
        }

        ApplySeason();
    }

    /// <summary>
    /// Which season a launch opens on.
    /// </summary>
    /// <remarks>
    /// The remembered <b>dungeon</b> is what resolves it, so the two pickers cannot disagree —
    /// the season is only used to disambiguate when a dungeon is in more than one, which MDT
    /// allows (<c>DungeonSelect.lua:8</c>) though nothing is today.
    /// </remarks>
    private int StartingSeasonIndex()
    {
        if (_seasons.Count == 0) return -1;

        if (_settings.LastDungeonIndex is { } dungeon)
        {
            var preferred = _seasons.FindIndex(
                s => s.DisplayName == _settings.LastSeasonName && s.Dungeons.Contains(dungeon));
            if (preferred >= 0) return preferred;

            var any = _seasons.FindIndex(s => s.Dungeons.Contains(dungeon));
            if (any >= 0) return any;
        }

        return 0;
    }

    private void OnSeasonChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_loading) ApplySeason();
    }

    /// <summary>Rebuilds the dungeon picker from the selected season and lands on a dungeon.</summary>
    /// <remarks>
    /// ⚠ In MDT's own order, never re-sorted. The ordering is the addon's — it is how its own
    /// dropdown reads, and re-alphabetising it would make the two disagree for no gain.
    /// </remarks>
    private void ApplySeason()
    {
        if (_data is null || SelectedSeason is not { } season) return;

        var choices = season.Dungeons
            .Select(i => _data.Find(i))
            .OfType<Dungeon>()
            .Select(d => new DungeonChoice(d))
            .ToList();

        var remembered = _dungeonBySeason.TryGetValue(season.DisplayName, out var index)
            ? choices.FindIndex(c => c.Dungeon.Index == index)
            : -1;

        _loading = true;
        DungeonPicker.ItemsSource = choices;
        DungeonPicker.SelectedIndex = choices.Count == 0 ? -1 : Math.Max(remembered, 0);
        _loading = false;

        ApplyDungeon();
    }

    private void OnDungeonChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_loading) ApplyDungeon();
    }

    /// <summary>
    /// Everything that follows from a dungeon being on screen: sublevels, route, map.
    /// </summary>
    /// <remarks>
    /// ⚠ It calls <see cref="SyncRoutePickerToDungeon"/> <b>directly</b> rather than nudging a
    /// picker and hoping WPF raises <c>SelectionChanged</c>. That indirection is what broke:
    /// re-selecting an already-selected item raises nothing, so a route could become
    /// unrecoverable without first picking a different one.
    /// </remarks>
    private void ApplyDungeon()
    {
        if (SelectedDungeon is not { } dungeon)
        {
            // No dungeon means no routes to offer, so the picker shows the sentinel and nothing
            // else — never another dungeon's list left standing.
            _loading = true;
            RoutePicker.ItemsSource = new List<RouteChoice> { RouteChoice.None };
            _loading = false;

            Map.Clear();
            ClearRoute();
            return;
        }

        if (SelectedSeason is { } season) _dungeonBySeason[season.DisplayName] = dungeon.Index;

        _loading = true;
        SubLevelPicker.ItemsSource = dungeon.SubLevels.Select(s => new SubLevelChoice(s)).ToList();
        SubLevelPicker.SelectedIndex = 0;
        _loading = false;

        // Every Midnight dungeon ships exactly one sublevel, so the picker would be a control
        // with nothing to choose. It appears the day one ships two.
        var many = dungeon.SubLevels.Count > 1 ? Visibility.Visible : Visibility.Collapsed;
        SubLevelPicker.Visibility = SubLevelLabel.Visibility = many;

        SyncRoutePickerToDungeon(dungeon);
        ShowMap();
    }

    /// <summary>
    /// Puts a dungeon on screen by index, switching season when it is not in the one shown.
    /// </summary>
    /// <returns>False when the cache holds no such dungeon, or no season names it.</returns>
    private bool SelectDungeon(int dungeonIndex)
    {
        if (_data?.Find(dungeonIndex) is null) return false;

        var here = (DungeonPicker.ItemsSource as IEnumerable<DungeonChoice>)?
            .ToList().FindIndex(c => c.Dungeon.Index == dungeonIndex) ?? -1;

        if (here >= 0)
        {
            if (here == DungeonPicker.SelectedIndex) return true;

            _loading = true;
            DungeonPicker.SelectedIndex = here;
            _loading = false;
            ApplyDungeon();
            return true;
        }

        var seasonIndex = _seasons.FindIndex(s => s.Dungeons.Contains(dungeonIndex));
        if (seasonIndex < 0) return false;

        _dungeonBySeason[_seasons[seasonIndex].DisplayName] = dungeonIndex;

        _loading = true;
        SeasonPicker.SelectedIndex = seasonIndex;
        _loading = false;
        ApplySeason();
        return true;
    }

    private void OnSubLevelChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_loading) ShowMap();
    }

    private void ShowMap()
    {
        if (SelectedDungeon is not { } dungeon) return;

        var result = Map.Load(dungeon, SelectedSubLevel, _service.Cache, _roles);

        // ⚠ It no longer clears the route when the dungeon does not match. RedrawOverlay already
        // no-ops in exactly that case, and clearing here is what left the picker displaying a
        // route that was no longer loaded — the desync the whole rework exists to kill.
        RedrawOverlay();

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

    /// <summary>
    /// Rebuilds the route picker for one dungeon and loads whatever it lands on.
    /// </summary>
    /// <remarks>
    /// <para>
    /// ⚠ <b>This is the fix.</b> The picker used to list every saved route regardless of dungeon,
    /// and a route was only ever loaded as a side effect of <c>SelectionChanged</c>. So switching
    /// dungeon left the picker displaying a route that had been cleared, and re-picking it raised
    /// no event — because it was already the selected item. The route was unrecoverable without
    /// picking a different one first, or restarting.
    /// </para>
    /// <para>
    /// Two things kill that. The list is filtered to this dungeon and led by an explicit
    /// <b>“— no route —”</b> sentinel, so "no route" is an expressible selection and the picker
    /// can always show the true state instead of lying about it. And the load happens by a direct
    /// call here, decided by <see cref="RouteSelection.Choose"/> in <c>Core</c> where it is
    /// tested, rather than by an event WPF may or may not raise.
    /// </para>
    /// </remarks>
    private void SyncRoutePickerToDungeon(Dungeon dungeon)
    {
        var library = _library.List();
        var candidates = RouteSelection.For(library, dungeon.Index);
        var chosen = RouteSelection.Choose(
            library, dungeon.Index, _pendingRouteId, _routeByDungeon.GetValueOrDefault(dungeon.Index));

        var choices = new List<RouteChoice> { RouteChoice.None };
        choices.AddRange(candidates.Select(r => new RouteChoice(r, dungeon)));

        var index = chosen is null ? 0 : choices.FindIndex(c => c.Saved?.Id == chosen.Id);

        _loading = true;
        RoutePicker.ItemsSource = choices;
        RoutePicker.SelectedIndex = Math.Max(index, 0);
        _loading = false;

        if (chosen is null) ClearRoute(); else LoadRoute(chosen);
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

            // The import follows the route to its dungeon — switching season too, since the
            // dungeon picker is filtered by one. The pending id is what makes the sync land on
            // the route just imported rather than on whatever that dungeon last had.
            _pendingRouteId = saved.Id;
            try
            {
                if (SelectedDungeon is { } current && current.Index == route.DungeonIndex)
                    SyncRoutePickerToDungeon(current);
                else if (!SelectDungeon(route.DungeonIndex))
                    Status.Text = $"Imported “{saved.DisplayName}”, but dungeon " +
                                  $"{route.DungeonIndex} is not in the cache — " +
                                  "press “Update MDT data”.";
            }
            finally { _pendingRouteId = null; }

            if (_savedRoute?.Id == saved.Id)
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

        // The sentinel is a real selection, not an empty one — picking it means "take the route
        // off", which is the thing the picker could not express before.
        if (choice.Saved is null)
        {
            if (SelectedDungeon is { } dungeon) _routeByDungeon.Remove(dungeon.Index);
            ClearRoute();
            return;
        }

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
        _routeByDungeon[saved.DungeonIndex] = saved.Id;

        // No "follow the route to its dungeon" here any more: the only two callers are the sync,
        // where the dungeon is the route's by construction, and the import, which does the
        // switching itself. Doing it from inside a load was the indirection that broke.
        RedrawOverlay();

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
        ClearNoteList();

        // ⚠ The picker follows. Leaving it displaying a route that is no longer loaded is the
        // desync itself — the toolbar claiming a route is on the map when none is.
        if (RoutePicker.ItemsSource is not null)
        {
            _loading = true;
            RoutePicker.SelectedIndex = 0;
            _loading = false;
        }

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
        _routeByDungeon.Remove(_savedRoute.DungeonIndex);

        ClearRoute();
        if (SelectedDungeon is { } dungeon) SyncRoutePickerToDungeon(dungeon);
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
        RebuildNoteList(overlay);

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

    /// <summary>
    /// The notes tab, rebuilt only when the notes themselves change.
    /// </summary>
    /// <remarks>
    /// ⚠ <see cref="RedrawOverlay"/> runs on every pull advance, and rebuilding the list there
    /// would clear the selection — so clicking note 7 and then pressing the next-pull hotkey
    /// would drop the highlight and lose your place. The annotations depend only on the route
    /// and the sublevel, so that pair is the guard.
    /// </remarks>
    private void RebuildNoteList(RouteOverlayResult overlay)
    {
        var notes = overlay.Notes.ToList();
        var key = $"{_route?.Uid}|{SelectedSubLevel}|{notes.Count}";
        if (key == _noteListKey) return;

        _noteListKey = key;
        _noteRows.Clear();
        foreach (var note in notes) _noteRows.Add(new NoteRow(note));

        NotesTab.Header = $"Notes ({notes.Count})";
        NotesEmpty.Visibility = notes.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
        Map.HighlightNote(null);
    }

    private void ClearNoteList()
    {
        _noteListKey = null;
        _noteRows.Clear();
        NotesTab.Header = "Notes (0)";
        NotesEmpty.Visibility = Visibility.Visible;
        Map.HighlightNote(null);
    }

    /// <summary>
    /// Selecting a note highlights its pin — and does nothing else.
    /// </summary>
    /// <remarks>
    /// ⚠ It deliberately does not move the pull cursor, because a note has no pull association
    /// to move it to; and it does not centre or zoom the map, because the map is manual here and
    /// moving the viewport under someone mid-key is the kind of surprise this app avoids.
    /// </remarks>
    private void OnNoteSelected(object sender, SelectionChangedEventArgs e)
        => Map.HighlightNote((NoteList.SelectedItem as NoteRow)?.Number);

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
            LastSeasonName = SelectedSeason?.DisplayName,
            LastRouteByDungeon = new Dictionary<int, string>(_routeByDungeon),

            // ⚠ The legacy single id is deliberately dropped on the way out, so the migration on
            // load cannot fire a second time and resurrect a route the user has since cleared.
            LastRouteId = null,
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

/// <summary>A season as the picker shows it — MDT's own name, with how many dungeons it holds.</summary>
internal sealed record SeasonChoice(Season Season)
{
    public string Label => $"{Season.DisplayName}  ({Season.Dungeons.Count})";
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
internal sealed record RouteChoice(SavedRoute? Saved, Dungeon? Dungeon)
{
    /// <summary>
    /// The sentinel that leads every route list.
    /// </summary>
    /// <remarks>
    /// ⚠ It is not tidiness. It is what makes "no route" an <i>expressible</i> selection, so the
    /// picker can always represent the true state rather than displaying a route that is not
    /// loaded.
    /// </remarks>
    public static readonly RouteChoice None = new(null, null);

    public string Label
    {
        get
        {
            if (Saved is null) return "— no route —";

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

/// <summary>One row of the notes list.</summary>
/// <remarks>
/// The heading/body split is <c>Core</c>'s (<see cref="AnnotationOverlay.Title"/>), so the panel
/// and a future reader of the same note cannot disagree about where the heading ends.
/// </remarks>
internal sealed class NoteRow(AnnotationOverlay note)
{
    public int Number { get; } = note.Number;
    public string Title { get; } = note.Title;
    public string Body { get; } = note.Body;
    public bool HasBody => Body.Length > 0;
}

/// <summary>The one command the window needs, so F11 works with the toolbar hidden.</summary>
internal sealed class RelayCommand(Action action) : ICommand
{
    public event EventHandler? CanExecuteChanged { add { } remove { } }
    public bool CanExecute(object? parameter) => true;
    public void Execute(object? parameter) => action();
}

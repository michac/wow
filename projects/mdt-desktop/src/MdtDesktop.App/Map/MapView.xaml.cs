using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.App.Map;

/// <summary>
/// The map: one sublevel's tiles with a blip on every mob, pannable and zoomable, with the
/// route's pull outlines over it.
/// </summary>
/// <remarks>
/// It holds no arithmetic and no policy of its own. <see cref="MapLayout"/> decides where every
/// blip goes and how big it is; <see cref="RouteOverlay"/> decides which pull owns which mob,
/// what colour it is, where the outline runs and what is dimmed; <see cref="MapPalette"/>
/// decides the role colours. All of that is in <c>Core</c>, where it is tested. This binds,
/// draws and forwards events.
/// </remarks>
public partial class MapView : UserControl
{
    private const double MinZoom = 0.25;
    private const double MaxZoom = 16;
    private const double ZoomStep = 1.15;

    /// <summary>MDT's own hull line weight: <c>sizeMultiplier * 3</c> at 0.8 (<c>PullOutlines.lua:283,299</c>).</summary>
    private const double HullThickness = 2.4;

    // Deliberately not portraits. MDT draws each blip with
    // SetPortraitTextureFromCreatureDisplayID, a client API with no external equivalent, and a
    // coloured disc carrying the forces count is how you read the map at speed anyway.
    private static readonly Brush BlipStroke = Frozen(Color.FromArgb(0xCC, 0x0D, 0x0F, 0x11));
    private static readonly Brush BossStroke = Frozen(Color.FromRgb(0xF5, 0xDC, 0x9A));
    private static readonly Brush LabelBrush = Frozen(Color.FromRgb(0xF2, 0xF5, 0xF8));
    private static readonly Brush BadgeBrush = Frozen(Color.FromArgb(0xDD, 0xE6, 0xEC, 0xF2));
    private static readonly Brush PatrolStroke = Frozen(Color.FromArgb(0x99, 0xE8, 0xD8, 0x8C));
    private static readonly Brush PullNumberBrush = Frozen(Colors.White);

    private static readonly Dictionary<string, Brush> BrushCache = [];

    /// <summary>
    /// The drawn elements, keyed the way a route names a mob.
    /// </summary>
    /// <remarks>
    /// ⚠ Advancing the pull must not rebuild ~200 elements. Keeping the discs here makes
    /// <see cref="ApplyOverlay"/> a sweep of property assignments, so F2 repaints instantly —
    /// which matters because the alternative is a lag nobody could diagnose from a screenshot.
    /// </remarks>
    private readonly Dictionary<(int EnemyIndex, int CloneIndex), DrawnBlip> _drawn = [];

    private MobRoleIndex? _roles;
    private bool _userAdjusted;
    private Point _dragOrigin;
    private Point _panOrigin;

    public MapView() => InitializeComponent();

    /// <summary>
    /// The zoom a fresh <see cref="Load"/> lands on, as a multiple of "fit to viewport".
    /// </summary>
    /// <remarks>
    /// Set from the remembered setting, so a launch frames the map the way it was left — and as
    /// a multiple rather than an absolute scale, so resizing the window does not re-frame it.
    /// </remarks>
    public double DefaultRelativeZoom { get; set; } = 1;

    /// <summary>The blips currently drawn, in the order they were laid out.</summary>
    public IReadOnlyList<MapBlip> CurrentBlips { get; private set; } = [];

    /// <summary>Draws one sublevel of a dungeon. Clears any route overlay.</summary>
    /// <param name="roles">
    /// The role classification, built once per cache. Null falls back to the plain
    /// boss/trash/worthless read, so the map still draws before any data is classified.
    /// </param>
    public MapLoadResult Load(Dungeon dungeon, int subLevel, DataCache cache, MobRoleIndex? roles = null)
    {
        Clear();
        _roles = roles;

        var folder = dungeon.SubLevels.FirstOrDefault(s => s.Index == subLevel)?.TextureFolder;
        var composed = folder is null
            ? new ComposedMap(null, 0)
            : TileComposer.Compose(cache.TextureDirectory(folder), subLevel);

        Tiles.Source = composed.Image;

        CurrentBlips = MapLayout.Build(dungeon, subLevel);
        DrawBlips(CurrentBlips);

        FitToViewport(DefaultRelativeZoom);
        return new MapLoadResult(composed.TilesFound, CurrentBlips.Count);
    }

    public void Clear()
    {
        Tiles.Source = null;
        Blips.Children.Clear();
        Hulls.Children.Clear();
        PullLabels.Children.Clear();
        _drawn.Clear();
        CurrentBlips = [];
    }

    /// <summary>
    /// Puts a route's pulls over the map: outlines, numbers, and pull-coloured blips.
    /// </summary>
    /// <remarks>
    /// ⚠ Role colour and pull colour coexist here rather than competing, which is MDT's own
    /// behaviour: a mob in a pull wears its pull's colour, a mob in none keeps its role colour.
    /// <see cref="MapPalette.For(MobRole, string?, int)"/> is where that is decided; this only
    /// asks it.
    /// </remarks>
    public void ApplyOverlay(RouteOverlayResult overlay)
    {
        Hulls.Children.Clear();
        PullLabels.Children.Clear();

        foreach (var pull in overlay.Pulls)
        {
            if (pull.Outline.Count == 0) continue;

            Hulls.Children.Add(HullShape(pull));
            PullLabels.Children.Add(PullNumber(pull));
        }

        foreach (var (key, drawn) in _drawn)
        {
            var claimed = overlay.RoleByMob.GetValueOrDefault(key);
            Recolour(drawn, claimed?.Color);

            // MDT's NONACTIVE_ALPHA. A mob in no pull is not part of the route's ordering, so
            // it is not dimmed — dimming it would say something untrue about it.
            drawn.Opacity = claimed is null || claimed.IsCurrent ? 1 : RouteOverlay.NonActiveAlpha;
        }
    }

    /// <summary>Takes the route back off the map, leaving role colours.</summary>
    public void ClearOverlay()
    {
        Hulls.Children.Clear();
        PullLabels.Children.Clear();

        foreach (var drawn in _drawn.Values)
        {
            Recolour(drawn, null);
            drawn.Opacity = 1;
        }
    }

    /// <summary>Scales the map to fill the viewport and centres it.</summary>
    /// <param name="relativeZoom">A multiple of the fit scale; 1 is the plain fit.</param>
    public void FitToViewport(double relativeZoom = 1)
    {
        if (Viewport.ActualWidth <= 0 || Viewport.ActualHeight <= 0) return;

        var fit = Math.Min(
            Viewport.ActualWidth / MapGeometry.CanvasWidth,
            Viewport.ActualHeight / MapGeometry.CanvasHeight);

        var scale = Math.Clamp(fit * relativeZoom, MinZoom, MaxZoom);

        Zoom.ScaleX = Zoom.ScaleY = scale;
        Pan.X = (Viewport.ActualWidth - MapGeometry.CanvasWidth * scale) / 2;
        Pan.Y = (Viewport.ActualHeight - MapGeometry.CanvasHeight * scale) / 2;
        _userAdjusted = false;
    }

    /// <summary>
    /// The current zoom as a multiple of "fit", which is what survives a window resize.
    /// </summary>
    /// <remarks>An absolute scale would silently re-frame the map whenever the window changed size.</remarks>
    public double ZoomRelativeToFit
    {
        get
        {
            if (Viewport.ActualWidth <= 0 || Viewport.ActualHeight <= 0) return 1;

            var fit = Math.Min(
                Viewport.ActualWidth / MapGeometry.CanvasWidth,
                Viewport.ActualHeight / MapGeometry.CanvasHeight);

            return fit <= 0 ? 1 : Zoom.ScaleX / fit;
        }
    }

    // ---- drawing ---------------------------------------------------------------------------

    private Polyline HullShape(PullOverlay pull)
    {
        var line = new Polyline
        {
            Stroke = BrushFor(pull.Color),
            StrokeThickness = HullThickness,
            StrokeLineJoin = PenLineJoin.Round,
            StrokeStartLineCap = PenLineCap.Round,
            StrokeEndLineCap = PenLineCap.Round,
            Opacity = pull.Alpha,
            IsHitTestVisible = false,
        };

        foreach (var point in pull.Outline) line.Points.Add(new Point(point.X, point.Y));

        // Closed: MDT draws the last vertex back to the first (PullOutlines.lua:293-296).
        line.Points.Add(new Point(pull.Outline[0].X, pull.Outline[0].Y));
        return line;
    }

    private static TextBlock PullNumber(PullOverlay pull)
    {
        var label = new TextBlock
        {
            Text = pull.Number.ToString(),
            Foreground = PullNumberBrush,
            FontSize = pull.IsCurrent ? 22 : 16,
            FontWeight = FontWeights.Bold,
            TextAlignment = TextAlignment.Center,
            Opacity = pull.Alpha,
            IsHitTestVisible = false,
            // A white number on a light map tile is unreadable, so it carries its own shadow.
            Effect = new System.Windows.Media.Effects.DropShadowEffect
            {
                Color = Colors.Black, BlurRadius = 4, ShadowDepth = 0, Opacity = 0.9,
            },
        };

        label.Measure(new Size(double.PositiveInfinity, double.PositiveInfinity));
        Canvas.SetLeft(label, pull.Center.X - label.DesiredSize.Width / 2);
        Canvas.SetTop(label, pull.Center.Y - label.DesiredSize.Height / 2);
        return label;
    }

    private void DrawBlips(IReadOnlyList<MapBlip> blips)
    {
        // Patrol routes underneath, then trash, then bosses — so the thing you are looking for
        // is never hidden behind the thing you are not.
        foreach (var blip in blips.Where(b => b.Patrol.Count > 0))
            Blips.Children.Add(PatrolLine(blip));

        foreach (var blip in blips.Where(b => !b.IsBoss)) AddBlip(blip);
        foreach (var blip in blips.Where(b => b.IsBoss)) AddBlip(blip);
    }

    private Polyline PatrolLine(MapBlip blip)
    {
        var line = new Polyline
        {
            Stroke = PatrolStroke,
            StrokeThickness = 0.7,
            StrokeDashArray = [3, 3],
            IsHitTestVisible = false,
        };

        // The path starts where the mob stands, then runs through its waypoints.
        line.Points.Add(new Point(blip.X, blip.Y));
        foreach (var point in blip.Patrol) line.Points.Add(new Point(point.X, point.Y));
        return line;
    }

    private void AddBlip(MapBlip blip)
    {
        var role = _roles?.Role(blip.Enemy) ?? (blip.IsBoss ? MobRole.Boss : MobRole.Melee);

        var disc = new Ellipse
        {
            Width = blip.Size,
            Height = blip.Size,
            Fill = BrushFor(MapPalette.For(role, null, blip.Forces)),
            Stroke = blip.IsBoss ? BossStroke : BlipStroke,
            StrokeThickness = blip.IsBoss ? blip.Size * 0.11 : 0.6,
            ToolTip = Tooltip(blip, role),
        };

        Place(disc, blip, blip.Size, blip.Size);
        Blips.Children.Add(disc);

        var drawn = new DrawnBlip(disc, role, blip.Forces);

        // A boss is worth nothing and the two zero-count trash mobs would just read "0", so the
        // label is only drawn where it says something.
        if (blip.Forces > 0)
        {
            var label = new TextBlock
            {
                Text = blip.Forces.ToString(),
                Foreground = LabelBrush,
                FontSize = Math.Max(blip.Size * 0.62, 3),
                FontWeight = FontWeights.SemiBold,
                TextAlignment = TextAlignment.Center,
                Width = blip.Size * 3,          // room for two digits without clipping
                IsHitTestVisible = false,
            };

            label.Measure(new Size(double.PositiveInfinity, double.PositiveInfinity));
            Place(label, blip, label.Width, label.DesiredSize.Height);
            Blips.Children.Add(label);
            drawn.Label = label;
        }

        // Badges under the blip: orthogonal to role, and a mob can carry several, so they are a
        // row of letters rather than a second colour.
        if (MapPalette.Badges(blip.Enemy) is { Length: > 0 } badges)
        {
            var badge = new TextBlock
            {
                Text = badges,
                Foreground = BadgeBrush,
                FontSize = Math.Max(blip.Size * 0.42, 2.6),
                FontWeight = FontWeights.Bold,
                TextAlignment = TextAlignment.Center,
                Width = blip.Size * 3,
                IsHitTestVisible = false,
            };

            badge.Measure(new Size(double.PositiveInfinity, double.PositiveInfinity));
            Canvas.SetLeft(badge, blip.X - badge.Width / 2);
            Canvas.SetTop(badge, blip.Y + blip.Size * 0.45);
            Blips.Children.Add(badge);
            drawn.Badge = badge;
        }

        _drawn[blip.Key] = drawn;
    }

    /// <param name="pullColor">The owning pull's colour, or null to fall back to the role's.</param>
    private static void Recolour(DrawnBlip drawn, string? pullColor)
        => drawn.Disc.Fill = BrushFor(MapPalette.For(drawn.Role, pullColor, drawn.Forces));

    private static string Tooltip(MapBlip blip, MobRole role)
    {
        var lines = new List<string> { $"{blip.Enemy.Name ?? "?"} — {role}" };
        lines.Add($"{blip.Forces} forces · {blip.Enemy.Health:N0} hp · [{blip.Enemy.Index}.{blip.Clone.Index}]");

        if (blip.Enemy.HasInterruptibleSpell) lines.Add("has an interruptible cast");
        if (blip.Enemy.SpellFlags.Count > 0)
            lines.Add("dispel/soothe: " + string.Join(", ", blip.Enemy.SpellFlags).ToLowerInvariant());
        if (blip.Enemy.Stealth) lines.Add("stealthed");

        return string.Join("\n", lines);
    }

    /// <summary>Centres an element on the blip — MDT anchors a blip frame by its centre.</summary>
    private static void Place(UIElement element, MapBlip blip, double width, double height)
    {
        Canvas.SetLeft(element, blip.X - width / 2);
        Canvas.SetTop(element, blip.Y - height / 2);
    }

    // ---- input -----------------------------------------------------------------------------

    private void OnViewportSizeChanged(object sender, SizeChangedEventArgs e)
    {
        // Re-fitting after the user has framed something themselves would undo their work.
        if (!_userAdjusted) FitToViewport(DefaultRelativeZoom);
    }

    private void OnMouseWheel(object sender, MouseWheelEventArgs e)
    {
        var target = Math.Clamp(
            Zoom.ScaleX * (e.Delta > 0 ? ZoomStep : 1 / ZoomStep), MinZoom, MaxZoom);

        var factor = target / Zoom.ScaleX;
        if (Math.Abs(factor - 1) < double.Epsilon) return;

        // Zoom about the cursor: the map point under it must not move. p = m·s + t, so
        // holding m fixed while s changes gives t' = p − (p − t)·(s'/s).
        var cursor = e.GetPosition(Viewport);
        Pan.X = cursor.X - (cursor.X - Pan.X) * factor;
        Pan.Y = cursor.Y - (cursor.Y - Pan.Y) * factor;
        Zoom.ScaleX = Zoom.ScaleY = target;

        _userAdjusted = true;
        e.Handled = true;
    }

    private void OnMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        _dragOrigin = e.GetPosition(Viewport);
        _panOrigin = new Point(Pan.X, Pan.Y);
        Viewport.CaptureMouse();
        Viewport.Cursor = Cursors.ScrollAll;
    }

    private void OnMouseMove(object sender, MouseEventArgs e)
    {
        if (!Viewport.IsMouseCaptured) return;

        var moved = e.GetPosition(Viewport) - _dragOrigin;
        Pan.X = _panOrigin.X + moved.X;
        Pan.Y = _panOrigin.Y + moved.Y;
        _userAdjusted = true;
    }

    private void OnMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        Viewport.ReleaseMouseCapture();
        Viewport.Cursor = Cursors.Arrow;
    }

    // ---- brushes ---------------------------------------------------------------------------

    /// <summary>
    /// A frozen brush per colour, cached — a route recolours 150+ blips on every pull change and
    /// there are only ever a couple of dozen distinct colours.
    /// </summary>
    private static Brush BrushFor(string hex)
    {
        if (BrushCache.TryGetValue(hex, out var cached)) return cached;

        var rgb = RouteOverlay.ParseColor(hex) ?? (0x4C, 0x8D, 0xBE);
        var brush = Frozen(Color.FromRgb(rgb.Item1, rgb.Item2, rgb.Item3));

        BrushCache[hex] = brush;
        return brush;
    }

    private static SolidColorBrush Frozen(Color color)
    {
        var brush = new SolidColorBrush(color);
        brush.Freeze();
        return brush;
    }

    /// <summary>One mob's elements, so a pull change is an assignment rather than a rebuild.</summary>
    private sealed class DrawnBlip(Ellipse disc, MobRole role, int forces)
    {
        public Ellipse Disc { get; } = disc;
        public MobRole Role { get; } = role;
        public int Forces { get; } = forces;
        public TextBlock? Label { get; set; }
        public TextBlock? Badge { get; set; }

        /// <summary>Dims the whole mob — disc, forces label and badges together.</summary>
        public double Opacity
        {
            set
            {
                Disc.Opacity = value;
                if (Label is not null) Label.Opacity = value;
                if (Badge is not null) Badge.Opacity = value;
            }
        }
    }
}

/// <param name="TilesFound">Tiles actually read, of the 150 a sublevel should have.</param>
/// <param name="BlipCount">Mobs drawn.</param>
public readonly record struct MapLoadResult(int TilesFound, int BlipCount);

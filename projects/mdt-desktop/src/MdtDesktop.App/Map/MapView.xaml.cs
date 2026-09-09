using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;

// System.IO.Path and System.Windows.Shapes.Path are both in scope here.
using Path = System.Windows.Shapes.Path;

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

    /// <summary>The tactical ring's diameter, as a multiple of the disc's.</summary>
    private const double RingSizeMultiple = 1.5;

    /// <summary>How far under the blip the badge row sits, as a multiple of the disc's size.</summary>
    /// <remarks>⚠ The ring's outer edge reaches 0.75, so a badge at 0.45 would sit on top of it.</remarks>
    private const double BadgeOffset = 0.45;
    private const double BadgeOffsetUnderRing = 0.80;

    /// <summary>The note pin's diameter in canvas units — MDT's own <c>12 * scale</c>.</summary>
    /// <remarks>
    /// We draw our own pin: MDT uses a numbered quest-pin icon from a 25-entry texture sheet,
    /// which is also why its numbering wraps at 25 and ours does not.
    /// </remarks>
    private const double NotePinSize = 12;

    // Deliberately not portraits. MDT draws each blip with
    // SetPortraitTextureFromCreatureDisplayID, a client API with no external equivalent, and a
    // coloured disc carrying the forces count is how you read the map at speed anyway.
    private static readonly Brush BlipStroke = Frozen(Color.FromArgb(0xCC, 0x0D, 0x0F, 0x11));
    private static readonly Brush BossStroke = Frozen(Color.FromRgb(0xF5, 0xDC, 0x9A));
    private static readonly Brush LabelBrush = Frozen(Color.FromRgb(0xF2, 0xF5, 0xF8));
    private static readonly Brush BadgeBrush = Frozen(Color.FromArgb(0xDD, 0xE6, 0xEC, 0xF2));
    private static readonly Brush PatrolStroke = Frozen(Color.FromArgb(0x99, 0xE8, 0xD8, 0x8C));
    private static readonly Brush PullNumberBrush = Frozen(Colors.White);

    /// <summary>
    /// The note pin: the amber the route panel already uses for warnings, so "the author is
    /// telling you something" reads the same in both places.
    /// </summary>
    private static readonly Brush NotePinBrush = Frozen(Color.FromRgb(0xE0, 0xA4, 0x4A));
    private static readonly Brush NotePinStroke = Frozen(Color.FromArgb(0xCC, 0x0D, 0x0F, 0x11));
    private static readonly Brush NotePinTextBrush = Frozen(Color.FromRgb(0x16, 0x19, 0x1C));

    /// <summary>The highlight a note wears while its row is selected in the panel.</summary>
    private static readonly Brush NotePinSelectedStroke = Frozen(Color.FromRgb(0xF2, 0xF5, 0xF8));

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

    /// <summary>
    /// Tactical rings, parked between the two passes that draw them.
    /// </summary>
    /// <remarks>
    /// A ring is drawn <b>before</b> its disc so it can never cover the disc's edge, and all the
    /// non-boss rings go down before any non-boss disc — so the ring cannot be built in the same
    /// call that builds the disc. It is handed over here instead.
    /// </remarks>
    private readonly Dictionary<(int EnemyIndex, int CloneIndex), Ellipse> _rings = [];

    /// <summary>
    /// The drawn note pins by number, so the panel can highlight one.
    /// </summary>
    /// <remarks>
    /// ⚠ Deliberately NOT the caching <see cref="_drawn"/> is: annotations are rebuilt on every
    /// overlay, and that is fine and should stay fine. <see cref="_drawn"/> exists because 200
    /// blips is a different number from 18 annotations — do not "optimise" this into a sweep.
    /// </remarks>
    private readonly Dictionary<int, Ellipse> _notePins = [];

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
        ClearAnnotations();
        _drawn.Clear();
        _rings.Clear();
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
        DrawAnnotations(overlay.Annotations);

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

            // The one mutable field on the tooltip, assigned in the sweep that was already
            // happening — pull membership changes without the mob changing.
            drawn.Tooltip.Pull = claimed is null ? null : $"pull {claimed.PullNumber}";

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

        // ⚠ Miss this and the previous route's pins stand on the next map, which looks like data
        // corruption rather than a missed line.
        ClearAnnotations();

        foreach (var drawn in _drawn.Values)
        {
            Recolour(drawn, null);
            drawn.Tooltip.Pull = null;
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

    // ---- annotations -------------------------------------------------------------------------

    /// <summary>
    /// Highlights one note's pin, or none.
    /// </summary>
    /// <remarks>
    /// A brighter stroke rather than a pan or a zoom: the map is deliberately manual here, and
    /// moving the viewport under someone mid-key is the kind of surprise this app avoids.
    /// </remarks>
    public void HighlightNote(int? number)
    {
        foreach (var (pinNumber, pin) in _notePins)
        {
            var selected = pinNumber == number;
            pin.Stroke = selected ? NotePinSelectedStroke : NotePinStroke;
            pin.StrokeThickness = selected ? 1.8 : 0.8;
        }
    }

    private void ClearAnnotations()
    {
        Drawings.Children.Clear();
        NotePins.Children.Clear();
        _notePins.Clear();
    }

    /// <summary>
    /// Draws the author's annotations. Everything decided is already decided in <c>Core</c>.
    /// </summary>
    /// <remarks>
    /// ⚠ They do not dim with the pull cursor. Annotations carry no pull association at all, so
    /// fading one on a non-current pull would assert a relationship that is not in the data —
    /// and it would do it to the guidance you can least afford to squint at.
    /// </remarks>
    private void DrawAnnotations(IReadOnlyList<AnnotationOverlay> annotations)
    {
        ClearAnnotations();

        foreach (var annotation in annotations)
        {
            if (annotation.Kind == RouteObjectKind.Note)
            {
                AddNotePin(annotation);
                continue;
            }

            Drawings.Children.Add(StrokeShape(annotation));

            if (annotation.HeadAngleDegrees is { } angle && LastPoint(annotation) is { } tip)
                Drawings.Children.Add(ArrowHead(annotation, tip, angle));
        }
    }

    /// <summary>One <c>Path</c> per annotation, one figure per contiguous run of segments.</summary>
    /// <remarks>
    /// <c>HullShape</c>'s approach with a geometry instead of a single polyline, because a stroke
    /// can legitimately break: <c>l</c> is a list of segments, not a path.
    /// </remarks>
    private static Path StrokeShape(AnnotationOverlay annotation)
    {
        var geometry = new PathGeometry();

        foreach (var figure in annotation.Figures)
        {
            if (figure.Count == 0) continue;

            var path = new PathFigure { StartPoint = new Point(figure[0].X, figure[0].Y) };
            for (var i = 1; i < figure.Count; i++)
                path.Segments.Add(new LineSegment(new Point(figure[i].X, figure[i].Y), true));

            geometry.Figures.Add(path);
        }

        // MDT's `smooth` draws a circle at every joint at the stroke radius, which IS round
        // joins and caps — drawn the long way, because a WoW texture has no cap setting.
        var join = annotation.Smooth ? PenLineJoin.Round : PenLineJoin.Miter;
        var cap = annotation.Smooth ? PenLineCap.Round : PenLineCap.Flat;

        return new Path
        {
            Data = geometry,
            Stroke = BrushFor(annotation.Color),
            StrokeThickness = annotation.Thickness,
            StrokeLineJoin = join,
            StrokeStartLineCap = cap,
            StrokeEndLineCap = cap,
            IsHitTestVisible = false,
        };
    }

    /// <summary>
    /// The arrow head, at the last point of the last figure — MDT's own anchor.
    /// </summary>
    /// <remarks>
    /// ⚠ Which way our triangle points at zero degrees is ours to choose, so it is a
    /// check-on-screen item rather than a claim. The angle itself is <c>Core</c>'s and tested;
    /// only the baseline orientation is decided here.
    /// </remarks>
    private static Polygon ArrowHead(AnnotationOverlay annotation, MapPoint tip, double angle)
    {
        var side = annotation.BrushSize;
        var height = side * Math.Sqrt(3) / 2;

        // An equilateral triangle pointing UP at zero, centred on the origin, so the rotation is
        // the only thing that aims it.
        var head = new Polygon
        {
            Points =
            [
                new Point(0, -height * 2 / 3),
                new Point(-side / 2, height / 3),
                new Point(side / 2, height / 3),
            ],
            Fill = BrushFor(annotation.Color),
            IsHitTestVisible = false,
            RenderTransform = new RotateTransform(angle),
        };

        Canvas.SetLeft(head, tip.X);
        Canvas.SetTop(head, tip.Y);
        return head;
    }

    private static MapPoint? LastPoint(AnnotationOverlay annotation)
        => annotation.Figures.LastOrDefault() is { Count: > 0 } figure ? figure[^1] : null;

    /// <summary>
    /// The note pin: a filled disc carrying the note's number, with the text on hover.
    /// </summary>
    /// <remarks>
    /// We have no WoW quest-pin art and will not fetch any — MDT's pins come from a texture
    /// sheet in the game client.
    /// </remarks>
    private void AddNotePin(AnnotationOverlay note)
    {
        var disc = new Ellipse
        {
            Width = NotePinSize,
            Height = NotePinSize,
            Fill = NotePinBrush,
            Stroke = NotePinStroke,
            StrokeThickness = 0.8,
            // ⚠ A DATA object, not a visual — the same reason MobTooltip is one.
            ToolTip = NoteTooltip.Build(note),
        };

        // A note is prose and must not time out mid-read.
        ToolTipService.SetInitialShowDelay(disc, 250);
        ToolTipService.SetShowDuration(disc, 30_000);

        PlaceAt(disc, note.Position, NotePinSize, NotePinSize);
        NotePins.Children.Add(disc);
        _notePins[note.Number] = disc;

        var label = new TextBlock
        {
            Text = note.Number.ToString(),
            Foreground = NotePinTextBrush,
            FontSize = NotePinSize * 0.62,
            FontWeight = FontWeights.Bold,
            TextAlignment = TextAlignment.Center,
            Width = NotePinSize * 3,
            IsHitTestVisible = false,
        };

        label.Measure(new Size(double.PositiveInfinity, double.PositiveInfinity));
        PlaceAt(label, note.Position, label.Width, label.DesiredSize.Height);
        NotePins.Children.Add(label);
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

        // Rings before the discs they surround, and the whole non-boss layer before the boss
        // layer — preserving "the thing you are looking for is never hidden behind the thing
        // you are not", now that there are four layers rather than two.
        foreach (var blip in blips.Where(b => !b.IsBoss)) AddRing(blip);
        foreach (var blip in blips.Where(b => !b.IsBoss)) AddBlip(blip);
        foreach (var blip in blips.Where(b => b.IsBoss)) AddRing(blip);
        foreach (var blip in blips.Where(b => b.IsBoss)) AddBlip(blip);
    }

    /// <summary>
    /// The tactical ring: what you have to <i>do</i> about the mob.
    /// </summary>
    /// <remarks>
    /// ⚠ It is a ring rather than a fill because <b>fill is spent</b>: under a route a blip wears
    /// its pull's colour, so role colour is gone exactly when the map is most in use. What the
    /// ring means, and why 295 of 462 mobs get none, is <see cref="MapPalette.Ring"/>'s.
    /// </remarks>
    private void AddRing(MapBlip blip)
    {
        if (MapPalette.Ring(blip.Enemy) is not { } cue) return;

        var size = blip.Size * RingSizeMultiple;
        var ring = new Ellipse
        {
            Width = size,
            Height = size,
            Stroke = BrushFor(cue.Color),
            StrokeThickness = Math.Max(blip.Size * 0.14, 0.5),
            // Dashed says "there is more than one axis here" — precedence alone would hide the
            // second, and the tooltip carries the full picture.
            StrokeDashArray = cue.Dashed ? new DoubleCollection([2, 1.6]) : null,
            Fill = null,
            // The disc keeps the tooltip: a ring that swallowed the hover would make the mob
            // harder to interrogate, not easier.
            IsHitTestVisible = false,
        };

        Place(ring, blip, size, size);
        Blips.Children.Add(ring);
        _rings[blip.Key] = ring;
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
        var tooltip = MobTooltip.Build(blip, role);

        var disc = new Ellipse
        {
            Width = blip.Size,
            Height = blip.Size,
            Fill = BrushFor(MapPalette.For(role, null, blip.Forces)),
            Stroke = blip.IsBoss ? BossStroke : BlipStroke,
            StrokeThickness = blip.IsBoss ? blip.Size * 0.11 : 0.6,
            // ⚠ A DATA object, not a visual. 462 pre-built tooltip trees would be paid for at
            // load; a data object plus the DataTemplate in MapView.xaml is materialised lazily,
            // on hover, once.
            ToolTip = tooltip,
        };

        // A long tooltip must not time out mid-read, and it must not appear the instant the
        // cursor crosses a blip on the way to somewhere else.
        ToolTipService.SetInitialShowDelay(disc, 250);
        ToolTipService.SetShowDuration(disc, 30_000);

        Place(disc, blip, blip.Size, blip.Size);
        Blips.Children.Add(disc);

        var drawn = new DrawnBlip(disc, role, blip.Forces, tooltip)
        {
            Ring = _rings.GetValueOrDefault(blip.Key),
        };

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
            Canvas.SetTop(badge, blip.Y + blip.Size *
                (drawn.Ring is null ? BadgeOffset : BadgeOffsetUnderRing));
            Blips.Children.Add(badge);
            drawn.Badge = badge;
        }

        _drawn[blip.Key] = drawn;
    }

    /// <param name="pullColor">The owning pull's colour, or null to fall back to the role's.</param>
    private static void Recolour(DrawnBlip drawn, string? pullColor)
        => drawn.Disc.Fill = BrushFor(MapPalette.For(drawn.Role, pullColor, drawn.Forces));

    /// <summary>Centres an element on the blip — MDT anchors a blip frame by its centre.</summary>
    private static void Place(UIElement element, MapBlip blip, double width, double height)
        => PlaceAt(element, new MapPoint(blip.X, blip.Y), width, height);

    /// <summary>Centres an element on a canvas point.</summary>
    private static void PlaceAt(UIElement element, MapPoint at, double width, double height)
    {
        Canvas.SetLeft(element, at.X - width / 2);
        Canvas.SetTop(element, at.Y - height / 2);
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
    private sealed class DrawnBlip(Ellipse disc, MobRole role, int forces, MobTooltip tooltip)
    {
        public Ellipse Disc { get; } = disc;
        public MobRole Role { get; } = role;
        public int Forces { get; } = forces;

        /// <summary>The live tooltip content — its <c>Pull</c> is re-answered by every overlay.</summary>
        public MobTooltip Tooltip { get; } = tooltip;

        public TextBlock? Label { get; set; }
        public TextBlock? Badge { get; set; }

        /// <summary>The tactical ring, when the mob wears one.</summary>
        public Ellipse? Ring { get; init; }

        /// <summary>Dims the whole mob — ring, disc, forces label and badges together.</summary>
        /// <remarks>
        /// ⚠ The ring belongs in here. Left out, a non-current pull's mobs dim while their rings
        /// stay bright — the one way this feature can look broken rather than merely absent.
        /// </remarks>
        public double Opacity
        {
            set
            {
                Disc.Opacity = value;
                if (Ring is not null) Ring.Opacity = value;
                if (Label is not null) Label.Opacity = value;
                if (Badge is not null) Badge.Opacity = value;
            }
        }
    }
}

/// <param name="TilesFound">Tiles actually read, of the 150 a sublevel should have.</param>
/// <param name="BlipCount">Mobs drawn.</param>
public readonly record struct MapLoadResult(int TilesFound, int BlipCount);

using System.Globalization;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Map;

/// <summary>
/// Everything a route adds on top of the map, resolved once: which mobs belong to which pull,
/// what colour each pull is, the outline round it, and where its number goes.
/// </summary>
/// <remarks>
/// <para>
/// This is the seam that keeps the WPF layer mechanical. <c>MapView</c> draws what comes back
/// and decides nothing — no colour resolution, no hull arithmetic, no "is this the current
/// pull". All of that is a pure function of a decoded route plus a dungeon, so all of it is
/// here where xunit can prove it without Windows.
/// </para>
/// <para>
/// ⚠ Pull colour and role colour are not in competition. MDT tints a blip that belongs to a
/// pull with that pull's colour and resets an unassigned blip to white
/// (<c>DungeonEnemies.lua:962,997</c> and <c>:983</c>), so the two sets are disjoint by
/// construction. <see cref="MapBlipRole.PullColor"/> being null is exactly "this mob is in no
/// pull, colour it by its role".
/// </para>
/// </remarks>
public static class RouteOverlay
{
    /// <summary>
    /// MDT dims every pull that is not the current one (<c>PullOutlines.lua:4</c>,
    /// <c>NONACTIVE_ALPHA = 0.5</c>). That is its own answer to "how do I mark the current pull",
    /// so it is taken rather than reinvented.
    /// </summary>
    public const double NonActiveAlpha = 0.5;

    /// <summary>MDT strokes a drawing at <c>size * 0.3</c> (<c>PresetObjects.lua:211</c>).</summary>
    public const double LineThicknessFactor = 0.3;

    /// <summary>
    /// What a drawing is drawn in when it names no colour, or an unreadable one. MDT does the
    /// same, rewriting a colour it cannot parse to <c>ffffff</c> (<c>PresetObjects.lua:185-189</c>);
    /// both strokes in the real King's Rest route carry <c>ffffff</c> explicitly.
    /// </summary>
    public const string DefaultAnnotationColor = "ffffff";

    /// <summary>
    /// Resolves a route against a dungeon for one sublevel.
    /// </summary>
    /// <param name="currentPull">
    /// The pull to draw at full alpha. MDT's <c>currentPull</c> is a manual cursor, and so is
    /// this — nothing advances it on its own.
    /// </param>
    public static RouteOverlayResult Build(
        Route route, Dungeon dungeon, int subLevel, int currentPull)
    {
        var forces = RouteForces.Count(route, dungeon);
        var forcesByPull = forces.ToDictionary(f => f.PullNumber);

        var pulls = new List<PullOverlay>(route.Pulls.Count);
        var roleByKey = new Dictionary<(int, int), MapBlipRole>();

        foreach (var pull in route.Pulls.OrderBy(p => p.Number))
        {
            var color = pull.HasCustomColor ? pull.Color! : Pull.DefaultColor;
            var isCurrent = pull.Number == currentPull;
            var keys = new List<(int EnemyIndex, int CloneIndex)>();
            var vertices = new List<HullPoint>();

            foreach (var entry in pull.Enemies)
            {
                if (!dungeon.EnemiesByIndex.TryGetValue(entry.EnemyIndex, out var enemy)) continue;

                foreach (var cloneIndex in entry.CloneIndices)
                {
                    if (!enemy.ClonesByIndex.TryGetValue(cloneIndex, out var clone)) continue;

                    var key = (entry.EnemyIndex, cloneIndex);
                    keys.Add(key);

                    // A mob is claimed by the FIRST pull that names it. A route should not name
                    // one twice, but nothing in MDT stops it, and a blip can only be one colour.
                    roleByKey.TryAdd(key, new MapBlipRole(pull.Number, color, isCurrent));

                    // Only mobs on this sublevel shape the outline — an off-sublevel clone would
                    // drag the hull across a map it is not drawn on.
                    if (!MapGeometry.IsVisibleOn(clone, subLevel)) continue;

                    var (x, y) = MapGeometry.ToCanvas(clone.X, clone.Y);
                    vertices.Add(new HullPoint(x, y, MapGeometry.BlipScale(clone, enemy)));
                }
            }

            var outline = PullHull.Outline(vertices);

            pulls.Add(new PullOverlay
            {
                Number = pull.Number,
                Color = color,
                HasCustomColor = pull.HasCustomColor,
                IsCurrent = isCurrent,
                Alpha = isCurrent ? 1 : NonActiveAlpha,
                Outline = outline,
                // The label goes on the hull MDT labels: DrawHullFontString takes the
                // pre-expansion vertices, so a one-mob pull's number sits on the mob.
                Center = PullHull.Centroid(vertices),
                MobKeys = keys,
                OnThisSubLevel = vertices.Count,
                Forces = forcesByPull.GetValueOrDefault(pull.Number),
            });
        }

        return new RouteOverlayResult(
            pulls, roleByKey, forces, currentPull, BuildAnnotations(route, subLevel));
    }

    /// <summary>
    /// The author's annotations, resolved for one sublevel and ready to draw.
    /// </summary>
    /// <remarks>
    /// <para>
    /// ⚠ The filter is an <b>equality</b> test, not <see cref="MapGeometry.IsVisibleOn"/>. That
    /// is clone semantics — a null sublevel means "show everywhere" for a clone — and MDT's rule
    /// for an object is the opposite: <c>if obj.d[3] == currentSublevel and obj.d[4]</c>
    /// (<c>PresetObjects.lua:177</c>), so an object naming no sublevel is drawn on none.
    /// </para>
    /// <para>
    /// ⚠ Annotations carry <b>no pull association</b>, so nothing here dims with the pull
    /// cursor. Fading a note on a non-current pull would assert a relationship that is not in
    /// the data — the same reasoning <see cref="NonActiveAlpha"/> already records for a mob in
    /// no pull.
    /// </para>
    /// </remarks>
    private static List<AnnotationOverlay> BuildAnnotations(Route route, int subLevel)
    {
        // ⚠ Numbered across the whole route rather than within the drawn subset, so a pin, its
        // row in the notes list and `route decode --notes` all say the same number about the
        // same note whichever sublevel is on screen.
        var numbers = new Dictionary<int, int>();
        foreach (var note in route.Objects.Where(o => o.Kind == RouteObjectKind.Note))
            numbers[note.Index] = numbers.Count + 1;

        var drawn = route.Objects
            .Where(o => o.Shown && o.SubLevel == subLevel)
            .OrderBy(o => o.DrawLayer)
            .ThenBy(o => o.Index);

        var annotations = new List<AnnotationOverlay>();

        foreach (var obj in drawn)
        {
            var (x, y) = MapGeometry.ToCanvas(obj.Position.X, obj.Position.Y);

            annotations.Add(new AnnotationOverlay
            {
                Kind = obj.Kind,
                Number = numbers.GetValueOrDefault(obj.Index),
                // MDT's own fallback: an unparseable colour is replaced by white outright
                // (PresetObjects.lua:185-189), so a junk value never reaches a draw loop.
                Color = ParseColor(obj.Color) is null ? DefaultAnnotationColor : obj.Color!,
                // MDT's own factor (PresetObjects.lua:211). `lineFactor` (d[2]) is deliberately
                // ignored: it exists to overlap WoW's square line textures so they do not gap at
                // a joint, and a round-joined path has no such gap.
                Thickness = obj.BrushSize * LineThicknessFactor,
                Smooth = obj.Smooth,
                Text = obj.Text,
                Position = new MapPoint(x, y),
                Figures = Coalesce(obj.Segments),
                HeadAngleDegrees = obj.HeadRotation is { } r ? HeadAngle(r) : null,
                BrushSize = obj.BrushSize,
            });
        }

        return annotations;
    }

    /// <summary>
    /// Segments to figures: contiguous runs become one polyline, a break starts a new one.
    /// </summary>
    /// <remarks>
    /// ⚠ <c>l</c> is a list of segments, so a stroke is only <i>usually</i> contiguous. Both
    /// drawings in the real King's Rest route are — every segment's end is the next one's start
    /// — but the format does not guarantee it and MDT draws them disjoint, so a break stays a
    /// break rather than being closed by an invented segment.
    /// </remarks>
    private static List<IReadOnlyList<MapPoint>> Coalesce(IReadOnlyList<RouteSegment> segments)
    {
        var figures = new List<IReadOnlyList<MapPoint>>();
        List<MapPoint>? current = null;
        MapPoint end = default;

        foreach (var segment in segments)
        {
            if (current is null || segment.From != end)
            {
                current = [Canvas(segment.From)];
                figures.Add(current);
            }

            current.Add(Canvas(segment.To));
            end = segment.To;
        }

        return figures;

        static MapPoint Canvas(MapPoint p)
        {
            var (x, y) = MapGeometry.ToCanvas(p.X, p.Y);
            return new MapPoint(x, y);
        }
    }

    /// <summary>
    /// MDT's stored arrow rotation, in the drawing convention WPF uses.
    /// </summary>
    /// <remarks>
    /// MDT stores <c>t[1] = atan2(starty - y, startx - x)</c> and adds π at draw time
    /// (<c>PresetObjects.lua:225</c> → <c>:479</c>). WoW's <c>SetRotation</c> is
    /// counter-clockwise radians; WPF's <c>RotateTransform</c> is clockwise degrees. It is
    /// arithmetic, so it is decided here where xunit can reach it rather than in a draw loop.
    /// </remarks>
    public static double HeadAngle(double rotation)
    {
        var degrees = -(rotation + Math.PI) * 180 / Math.PI % 360;
        return degrees < 0 ? degrees + 360 : degrees;
    }

    /// <summary>
    /// Six hex digits to bytes. Returns null for anything that is not exactly that, so a route
    /// carrying junk in <c>color</c> falls back rather than throwing in a draw loop.
    /// </summary>
    public static (byte R, byte G, byte B)? ParseColor(string? hex)
    {
        if (hex is null) return null;

        var s = hex.TrimStart('#');
        if (s.Length != 6) return null;

        return byte.TryParse(s[..2], NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var r) &&
               byte.TryParse(s[2..4], NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var g) &&
               byte.TryParse(s[4..], NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var b)
            ? (r, g, b)
            : null;
    }
}

/// <summary>The whole overlay for one sublevel.</summary>
/// <param name="Pulls">Every pull in the route, in order, whether or not it has mobs here.</param>
/// <param name="RoleByMob">
/// Which pull owns each mob, keyed the way a route names one — <c>(enemyIndex, cloneIndex)</c>,
/// the same key <see cref="MapBlip.Key"/> carries. A mob absent from this is in no pull.
/// </param>
/// <param name="Annotations">
/// The author's notes and drawings for this sublevel, in the order they stack. Empty for the
/// common case of a route that carries none.
/// </param>
public sealed record RouteOverlayResult(
    IReadOnlyList<PullOverlay> Pulls,
    IReadOnlyDictionary<(int EnemyIndex, int CloneIndex), MapBlipRole> RoleByMob,
    IReadOnlyList<PullForces> Forces,
    int CurrentPull,
    IReadOnlyList<AnnotationOverlay> Annotations)
{
    /// <summary>The notes among <see cref="Annotations"/>, which is what the panel lists.</summary>
    public IEnumerable<AnnotationOverlay> Notes
        => Annotations.Where(a => a.Kind == RouteObjectKind.Note);

    /// <summary>The pull the cursor is on, or null when it points past the end of the route.</summary>
    public PullOverlay? Current => Pulls.FirstOrDefault(p => p.Number == CurrentPull);

    /// <summary>Cumulative forces at the current pull — the readout's numerator.</summary>
    public int CumulativeForces
        => Forces.LastOrDefault(f => f.PullNumber <= CurrentPull)?.Cumulative ?? 0;

    public int DungeonTotal => Forces.Count > 0 ? Forces[0].DungeonTotal : 0;

    /// <summary>The readout: <c>&lt;cumulative&gt;/&lt;total&gt; (&lt;pct&gt;%)</c>.</summary>
    public string ForcesReadout
    {
        get
        {
            var total = DungeonTotal;
            var percent = total == 0 ? 0 : 100.0 * CumulativeForces / total;
            return $"{CumulativeForces}/{total} ({percent:F2}%)";
        }
    }
}

/// <summary>One pull, ready to draw.</summary>
public sealed record PullOverlay
{
    public required int Number { get; init; }

    /// <summary>Six lowercase hex digits. MDT's <c>228b22</c> when the author picked nothing.</summary>
    public required string Color { get; init; }

    /// <summary>False when <see cref="Color"/> is MDT's default sentinel rather than a choice.</summary>
    public required bool HasCustomColor { get; init; }

    public required bool IsCurrent { get; init; }

    /// <summary>1 for the current pull, <see cref="RouteOverlay.NonActiveAlpha"/> for the rest.</summary>
    public required double Alpha { get; init; }

    /// <summary>The closed outline, in canvas units. Empty when no mob is on this sublevel.</summary>
    public required IReadOnlyList<HullPoint> Outline { get; init; }

    /// <summary>Where the pull number goes.</summary>
    public required HullPoint Center { get; init; }

    /// <summary>Every mob in the pull that resolves, on any sublevel.</summary>
    public required IReadOnlyList<(int EnemyIndex, int CloneIndex)> MobKeys { get; init; }

    /// <summary>How many of them are on the sublevel this overlay was built for.</summary>
    public required int OnThisSubLevel { get; init; }

    /// <summary>What the pull is worth. Null only if the pull is missing from the forces run.</summary>
    public PullForces? Forces { get; init; }

    public override string ToString()
        => $"pull {Number}: {MobKeys.Count} mobs, {Outline.Count} hull points" +
           (IsCurrent ? " (current)" : "");
}

/// <summary>What a pull says about one of its mobs: which pull, what colour, is it the current one.</summary>
public sealed record MapBlipRole(int PullNumber, string Color, bool IsCurrent);

/// <summary>One annotation, resolved: canvas coordinates, a colour, and nothing left to decide.</summary>
/// <remarks>
/// Everything a draw loop would otherwise have to work out is worked out here — the sublevel
/// filter, the y flip, the stroke width, the note's number and the arrow's angle in drawing
/// degrees — because none of it can be seen on this machine and all of it can be proved.
/// </remarks>
public sealed record AnnotationOverlay
{
    public required RouteObjectKind Kind { get; init; }

    /// <summary>A note's number, 1..N across the whole route. Zero for a drawing.</summary>
    /// <remarks>
    /// ⚠ Deviating from MDT, which wraps at 25 (<c>PresetObjects.lua:582,587-588</c>) because
    /// that is how many numbered quest-pin icons its texture sheet has. We draw our own pin, so
    /// wrapping would lose information for nothing.
    /// </remarks>
    public required int Number { get; init; }

    /// <summary>Six hex digits. Resolved, never null.</summary>
    public required string Color { get; init; }

    /// <summary>Stroke width in canvas units.</summary>
    public required double Thickness { get; init; }

    /// <summary>Round joins and caps — which is what MDT's circles-at-every-joint amounts to.</summary>
    public required bool Smooth { get; init; }

    /// <summary>The note's text. Null for a drawing.</summary>
    public string? Text { get; init; }

    /// <summary>The note's pin, in canvas units with y already flipped.</summary>
    public MapPoint Position { get; init; }

    /// <summary>The stroke's contiguous runs, in canvas units. Empty for a note.</summary>
    public IReadOnlyList<IReadOnlyList<MapPoint>> Figures { get; init; } = [];

    /// <summary>An arrow head's angle in clockwise degrees, WPF's convention. Null otherwise.</summary>
    public double? HeadAngleDegrees { get; init; }

    /// <summary>MDT's own <c>d[1]</c>, which is also its arrow-head size (<c>:221-225</c>).</summary>
    public double BrushSize { get; init; }

    /// <summary>The note's first line — its heading, where the author wrote one.</summary>
    /// <remarks>
    /// 12 of the 16 notes in the real King's Rest route open with an em-dash heading
    /// (<c>GOLDEN SERPENT — STACK THE GOLD</c>); where an author wrote none, the first line is
    /// still the best one-line summary available.
    /// </remarks>
    public string Title => Split().Title;

    /// <summary>Everything after the first line, trimmed. Empty when the note is one line.</summary>
    public string Body => Split().Body;

    private (string Title, string Body) Split()
    {
        if (Text is not { Length: > 0 } text) return ("", "");

        var newline = text.IndexOf('\n');
        return newline < 0
            ? (text.Trim(), "")
            : (text[..newline].Trim(), text[(newline + 1)..].Trim());
    }
}

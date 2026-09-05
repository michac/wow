namespace MdtDesktop.Core.Map;

/// <summary>
/// The outline MDT draws around a pull: a convex hull of its mobs, inflated by their size.
/// </summary>
/// <remarks>
/// <para>
/// This is the port of <c>Modules/PullOutlines.lua</c> — hull, then <c>expand_polygon(hull, 30)</c>,
/// then hull again, with the pull number at the centroid. It lives in <c>Core</c> because it is
/// arithmetic, and arithmetic is the part that can be wrong; the WPF layer draws the polygon it
/// gets back and decides nothing.
/// </para>
/// <para>
/// ⚠ MDT's own <c>convex_hull</c> is gift-wrapping with a <c>tries &gt; 100</c> escape hatch and
/// the comment <c>--deadlocked here otherwise?!?</c>. That guard is a workaround for a bug in its
/// own loop, not a property of the problem, so it is deliberately <b>not</b> ported: this uses
/// Andrew's monotone chain, which terminates because it is two sorted sweeps rather than a
/// search, and it is tested on the degenerate inputs the gift-wrapper trips over — collinear
/// points, duplicates, and fewer than three points.
/// </para>
/// </remarks>
public static class PullHull
{
    /// <summary>MDT's own <c>expand_polygon(hull, 30)</c> — the scatter budget per vertex.</summary>
    public const int PointsPerVertex = 30;

    /// <summary>
    /// The scatter radius per unit of a blip's <c>normalScale</c> (<c>PullOutlines.lua:59</c>,
    /// <c>local r = poly[i][3] * 10</c>).
    /// </summary>
    public const double RadiusPerScale = 10;

    /// <summary>
    /// The convex hull of a point set, counter-clockwise, without repeating the first point.
    /// </summary>
    /// <remarks>
    /// Andrew's monotone chain. Degenerate input is returned rather than refused: zero, one or
    /// two distinct points have no area but are still a thing to draw, and a pull of one mob is
    /// the common case at the start of a route.
    /// </remarks>
    public static IReadOnlyList<HullPoint> ConvexHull(IReadOnlyList<HullPoint> points)
    {
        // Duplicates break the collinearity test's tie-breaking, and a pull can hold two mobs
        // standing on the same spot.
        var sorted = points
            .Distinct()
            .OrderBy(p => p.X).ThenBy(p => p.Y)
            .ToList();

        if (sorted.Count <= 2) return sorted;

        var hull = new List<HullPoint>(sorted.Count * 2);

        // Lower chain, then upper, both appended to the one list. A point is popped whenever it
        // is not a left turn, so a run of collinear points collapses to its two extremes — which
        // is the right answer: the hull of a line is that line.
        foreach (var point in sorted) Add(hull, point, 2);

        // The upper chain must not eat into the lower one, so its floor is where the lower ended.
        var upperFloor = hull.Count + 1;
        for (var i = sorted.Count - 2; i >= 0; i--) Add(hull, sorted[i], upperFloor);

        // The upper chain closes on the lower chain's first point, so it is there twice.
        hull.RemoveAt(hull.Count - 1);
        return hull;

        static void Add(List<HullPoint> hull, HullPoint point, int floor)
        {
            while (hull.Count >= floor && Cross(hull[^2], hull[^1], point) <= 0)
                hull.RemoveAt(hull.Count - 1);
            hull.Add(point);
        }
    }

    /// <summary>
    /// MDT's <c>expand_polygon</c>: scatter points on a circle round each vertex, sized by that
    /// vertex's blip scale.
    /// </summary>
    /// <remarks>
    /// Verbatim from <c>PullOutlines.lua:56-70</c> — radius <c>scale * 10</c>, and
    /// <c>max(1, floor(30 * scale))</c> points, so a small blip contributes fewer. The caller
    /// re-hulls the result; that second hull is what turns the scatter into a rounded outline.
    /// </remarks>
    public static IReadOnlyList<HullPoint> Expand(
        IReadOnlyList<HullPoint> polygon, int pointsPerVertex = PointsPerVertex)
    {
        var expanded = new List<HullPoint>(polygon.Count * pointsPerVertex);

        foreach (var vertex in polygon)
        {
            var radius = vertex.Scale * RadiusPerScale;
            var count = Math.Max(1, (int)Math.Floor(pointsPerVertex * vertex.Scale));

            for (var j = 1; j <= count; j++)
            {
                var angle = 2 * Math.PI / count * j;
                expanded.Add(new HullPoint(
                    vertex.X + radius * Math.Cos(angle),
                    vertex.Y + radius * Math.Sin(angle),
                    vertex.Scale));
            }
        }

        return expanded;
    }

    /// <summary>Hull → expand → hull, which is the whole of MDT's <c>DrawHull</c> geometry.</summary>
    public static IReadOnlyList<HullPoint> Outline(
        IReadOnlyList<HullPoint> points, int pointsPerVertex = PointsPerVertex)
    {
        if (points.Count == 0) return [];
        return ConvexHull(Expand(ConvexHull(points), pointsPerVertex));
    }

    /// <summary>
    /// The mean of the points — where MDT puts the pull number (<c>PullOutlines.lua:52-64</c>).
    /// </summary>
    /// <remarks>
    /// ⚠ It is the vertex mean, not the polygon's area centroid. That is MDT's own choice and
    /// matching it is the point: the label lands where MDT's does, which is what makes the two
    /// windows comparable side by side.
    /// </remarks>
    public static HullPoint Centroid(IReadOnlyList<HullPoint> points)
        => points.Count == 0
            ? new HullPoint(0, 0, 0)
            : new HullPoint(points.Average(p => p.X), points.Average(p => p.Y), 0);

    /// <summary>Cross product of <c>ab</c> and <c>ac</c>. Positive when c is left of a→b.</summary>
    private static double Cross(HullPoint a, HullPoint b, HullPoint c)
        => (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X);
}

/// <summary>
/// A hull vertex: a position plus the blip scale that decides how far the outline stands off it.
/// </summary>
/// <remarks>
/// The third component is MDT's <c>blip.normalScale</c> — <c>MapGeometry.BlipScale</c> here —
/// carried through so <see cref="PullHull.Expand"/> can inflate a boss further than a trash mob,
/// exactly as <c>getPullVertices</c> does (<c>PullOutlines.lua:305-323</c>).
/// </remarks>
public readonly record struct HullPoint(double X, double Y, double Scale);

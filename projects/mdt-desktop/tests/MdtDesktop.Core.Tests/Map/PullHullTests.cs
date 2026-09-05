using MdtDesktop.Core.Map;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The pull outline. This is the one piece of M4 geometry nobody can look at yet, so the
/// degenerate cases are pinned here rather than discovered on a map: MDT's own gift-wrapping
/// hull carries a <c>tries &gt; 100</c> escape hatch and the comment
/// <c>--deadlocked here otherwise?!?</c>, and these are the inputs that put it there.
/// </summary>
public class PullHullTests
{
    private static HullPoint P(double x, double y, double scale = 1) => new(x, y, scale);

    private static IReadOnlyList<HullPoint> Hull(params HullPoint[] points)
        => PullHull.ConvexHull(points);

    [Fact]
    public void A_square_hulls_to_its_four_corners()
    {
        var hull = Hull(P(0, 0), P(10, 0), P(10, 10), P(0, 10), P(5, 5));

        Assert.Equal(4, hull.Count);
        Assert.DoesNotContain(P(5, 5), hull);
    }

    /// <summary>The hull of a line is that line — its two extremes, not every point on it.</summary>
    [Fact]
    public void Collinear_points_collapse_to_their_extremes()
    {
        var hull = Hull(P(0, 0), P(1, 1), P(2, 2), P(3, 3));

        Assert.Equal(2, hull.Count);
        Assert.Contains(P(0, 0), hull);
        Assert.Contains(P(3, 3), hull);
    }

    [Fact]
    public void One_point_hulls_to_itself()
        => Assert.Equal([P(4, 7)], Hull(P(4, 7)));

    [Fact]
    public void Two_points_hull_to_both()
        => Assert.Equal(2, Hull(P(0, 0), P(5, 5)).Count);

    [Fact]
    public void No_points_hull_to_nothing()
        => Assert.Empty(Hull());

    /// <summary>Two mobs can stand on the same spot, and a route regularly puts them in one pull.</summary>
    [Fact]
    public void Duplicate_points_do_not_multiply_the_hull()
    {
        var hull = Hull(P(0, 0), P(0, 0), P(10, 0), P(10, 0), P(5, 10));
        Assert.Equal(3, hull.Count);
    }

    [Fact]
    public void All_identical_points_hull_to_one()
        => Assert.Single(Hull(P(3, 3), P(3, 3), P(3, 3), P(3, 3)));

    /// <summary>The bug MDT's <c>tries &gt; 100</c> guard is papering over. This must terminate.</summary>
    [Fact]
    public void A_large_degenerate_set_still_terminates()
    {
        var points = Enumerable.Range(0, 500).Select(i => P(i % 3, i % 3)).ToArray();
        Assert.Equal(2, PullHull.ConvexHull(points).Count);
    }

    [Fact]
    public void Every_input_point_is_inside_or_on_the_hull()
    {
        var random = new Random(20260904);
        var points = Enumerable.Range(0, 200)
            .Select(_ => P(random.NextDouble() * 840, random.NextDouble() * 560))
            .ToArray();

        var hull = PullHull.ConvexHull(points);

        Assert.All(points, p => Assert.True(IsInsideOrOn(hull, p), $"{p} fell outside the hull"));
    }

    // ---- expansion ----------------------------------------------------------------------

    /// <summary>
    /// MDT's own numbers: radius <c>scale * 10</c>, and <c>max(1, floor(30 * scale))</c> points.
    /// </summary>
    [Fact]
    public void Expansion_scatters_MDTs_own_point_count_at_MDTs_own_radius()
    {
        var expanded = PullHull.Expand([P(100, 100, 1)]);

        Assert.Equal(30, expanded.Count);
        Assert.All(expanded, p => Assert.Equal(
            PullHull.RadiusPerScale, Math.Sqrt(Sq(p.X - 100) + Sq(p.Y - 100)), precision: 9));
    }

    [Fact]
    public void A_bigger_blip_is_expanded_further_and_more_finely()
    {
        var boss = PullHull.Expand([P(0, 0, 1.7)]);
        var trash = PullHull.Expand([P(0, 0, 0.6)]);

        Assert.Equal(51, boss.Count);   // floor(30 * 1.7)
        Assert.Equal(18, trash.Count);  // floor(30 * 0.6)
        Assert.True(Radius(boss) > Radius(trash));
    }

    /// <summary>A tiny blip must still contribute a point rather than vanishing from the hull.</summary>
    [Fact]
    public void A_vanishingly_small_blip_still_scatters_one_point()
        => Assert.Single(PullHull.Expand([P(0, 0, 0.001)]));

    // ---- the whole outline --------------------------------------------------------------

    /// <summary>A one-mob pull is the common case at the start of a route, and it must draw.</summary>
    [Fact]
    public void A_single_mob_outlines_to_a_ring_around_it()
    {
        var outline = PullHull.Outline([P(400, 300, 1)]);

        Assert.True(outline.Count > 8, $"a ring of {outline.Count} points is not a ring");
        Assert.All(outline, p => Assert.Equal(
            PullHull.RadiusPerScale, Math.Sqrt(Sq(p.X - 400) + Sq(p.Y - 300)), precision: 9));
    }

    [Fact]
    public void The_outline_stands_off_the_mobs_rather_than_touching_them()
    {
        var mobs = new[] { P(100, 100), P(200, 100), P(150, 180) };
        var outline = PullHull.Outline(mobs);

        // Every mob is strictly inside, because the hull was inflated past all of them.
        Assert.All(mobs, m => Assert.True(IsInsideOrOn(outline, m)));
        Assert.True(outline.Max(p => p.X) > mobs.Max(m => m.X));
        Assert.True(outline.Min(p => p.Y) < mobs.Min(m => m.Y));
    }

    [Fact]
    public void An_empty_pull_outlines_to_nothing()
        => Assert.Empty(PullHull.Outline([]));

    // ---- the label ----------------------------------------------------------------------

    [Fact]
    public void The_centroid_is_the_mean_of_the_points()
    {
        var centre = PullHull.Centroid([P(0, 0), P(10, 0), P(10, 10), P(0, 10)]);
        Assert.Equal(5, centre.X);
        Assert.Equal(5, centre.Y);
    }

    [Fact]
    public void An_empty_set_has_a_centroid_rather_than_a_crash()
        => Assert.Equal(new HullPoint(0, 0, 0), PullHull.Centroid([]));

    // ---- helpers ------------------------------------------------------------------------

    private static double Sq(double v) => v * v;

    private static double Radius(IReadOnlyList<HullPoint> ring)
        => ring.Max(p => Math.Sqrt(Sq(p.X) + Sq(p.Y)));

    /// <summary>
    /// Point-in-convex-polygon by consistent winding: the cross products round the hull must not
    /// change sign. A tolerance is needed because the hull's own vertices sit exactly on an edge.
    /// </summary>
    private static bool IsInsideOrOn(IReadOnlyList<HullPoint> hull, HullPoint point)
    {
        if (hull.Count < 3) return true;

        var sign = 0;
        for (var i = 0; i < hull.Count; i++)
        {
            var a = hull[i];
            var b = hull[(i + 1) % hull.Count];
            var cross = (b.X - a.X) * (point.Y - a.Y) - (b.Y - a.Y) * (point.X - a.X);

            if (Math.Abs(cross) < 1e-9) continue;
            var current = Math.Sign(cross);
            if (sign == 0) sign = current;
            else if (sign != current) return false;
        }

        return true;
    }
}

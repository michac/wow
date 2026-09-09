using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;
using MdtDesktop.Core.Routes;
using MdtDesktop.Core.Tests.Data;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The seam WPF draws. Everything asserted here is a decision <c>MapView</c> is not allowed to
/// make for itself, which is the whole reason it lives in <c>Core</c> — none of it can be seen
/// on this machine, so all of it has to be provable.
/// </summary>
/// <remarks>
/// The fixture dungeon (index 4242, 100 forces): enemy 1 at 5 forces with clones 1 and 3 (clone
/// 3 overrides to 42), enemy 2 at 3 forces with clone 1, enemy 3 the boss at 0 with clone 1.
/// </remarks>
public class RouteOverlayTests
{
    private static async Task<Dungeon> FixtureDungeonAsync()
    {
        using var fixture = new MdtFixture();
        var data = await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);
        return data.ByIndex[4242];
    }

    private static Route RouteOf(params Pull[] pulls)
        => new() { DungeonIndex = 4242, Pulls = pulls };

    private static Pull PullOf(int number, string? color, params (int Enemy, int[] Clones)[] enemies)
        => new()
        {
            Number = number,
            Color = color,
            Enemies = [.. enemies.Select(e => new PullEnemy(e.Enemy, e.Clones))],
        };

    // ---- the current pull ----------------------------------------------------------------

    /// <summary>
    /// MDT's own answer: <c>NONACTIVE_ALPHA = 0.5</c> (<c>PullOutlines.lua:4</c>). Taking it
    /// rather than inventing an emphasis channel is the point.
    /// </summary>
    [Fact]
    public async Task The_current_pull_draws_solid_and_the_rest_at_MDTs_own_half_alpha()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1])), PullOf(2, null, (2, [1]))),
            await FixtureDungeonAsync(), subLevel: 1, currentPull: 2);

        Assert.Equal(RouteOverlay.NonActiveAlpha, overlay.Pulls[0].Alpha);
        Assert.False(overlay.Pulls[0].IsCurrent);

        Assert.Equal(1, overlay.Pulls[1].Alpha);
        Assert.True(overlay.Pulls[1].IsCurrent);
        Assert.Equal(2, overlay.Current!.Number);
    }

    [Fact]
    public async Task A_cursor_past_the_end_of_the_route_has_no_current_pull_rather_than_throwing()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, currentPull: 99);

        Assert.Null(overlay.Current);
        Assert.All(overlay.Pulls, p => Assert.False(p.IsCurrent));
    }

    // ---- colour ---------------------------------------------------------------------------

    [Fact]
    public async Task A_pull_with_no_colour_gets_MDTs_sentinel_rather_than_null()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        Assert.Equal(Pull.DefaultColor, overlay.Pulls[0].Color);
        // …and it is flagged as not-a-choice, so the UI can tell "green" from "unset green".
        Assert.False(overlay.Pulls[0].HasCustomColor);
    }

    [Fact]
    public async Task A_chosen_colour_is_carried_through_and_marked_as_chosen()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "ff8800", (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        Assert.Equal("ff8800", overlay.Pulls[0].Color);
        Assert.True(overlay.Pulls[0].HasCustomColor);
    }

    [Theory]
    [InlineData("ff8800", 0xFF, 0x88, 0x00)]
    [InlineData("#228B22", 0x22, 0x8B, 0x22)]
    public void A_hex_colour_parses_to_bytes(string hex, byte r, byte g, byte b)
        => Assert.Equal((r, g, b), RouteOverlay.ParseColor(hex));

    /// <summary>A draw loop must not throw over a colour, so junk falls back rather than failing.</summary>
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("red")]
    [InlineData("ff88")]
    [InlineData("gghhii")]
    public void Junk_in_the_colour_field_parses_to_nothing_rather_than_throwing(string? hex)
        => Assert.Null(RouteOverlay.ParseColor(hex));

    // ---- which mob belongs to which pull ---------------------------------------------------

    /// <summary>
    /// This dictionary is the coexistence rule in one line: a mob in it wears its pull's colour,
    /// a mob absent from it wears its role colour. MDT does exactly this — it tints assigned
    /// blips and resets unassigned ones (<c>DungeonEnemies.lua:962,983</c>).
    /// </summary>
    [Fact]
    public async Task A_mob_in_a_pull_is_keyed_to_it_and_a_mob_in_none_is_absent()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "ff8800", (1, [1]))), await FixtureDungeonAsync(), 1, 1);

        var claimed = overlay.RoleByMob[(1, 1)];
        Assert.Equal(1, claimed.PullNumber);
        Assert.Equal("ff8800", claimed.Color);
        Assert.True(claimed.IsCurrent);

        // Enemy 1 clone 3 and the boss are in no pull, so nothing claims them.
        Assert.False(overlay.RoleByMob.ContainsKey((1, 3)));
        Assert.False(overlay.RoleByMob.ContainsKey((3, 1)));
    }

    /// <summary>A blip can only be one colour, so a mob named twice belongs to the earlier pull.</summary>
    [Fact]
    public async Task A_mob_named_by_two_pulls_is_claimed_by_the_first()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, "aa0000", (1, [1])), PullOf(2, "00aa00", (1, [1]))),
            await FixtureDungeonAsync(), 1, 1);

        Assert.Equal(1, overlay.RoleByMob[(1, 1)].PullNumber);
    }

    /// <summary>
    /// MDT 6.2.13 deleted a clone a 6.2.12 route can still name. It is skipped in the geometry
    /// for the same reason <c>RouteForces</c> skips it in the arithmetic — and reported there.
    /// </summary>
    [Fact]
    public async Task A_clone_that_no_longer_exists_is_skipped_rather_than_drawn()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1, 2]))),   // clone 2 is absent from the fixture
            await FixtureDungeonAsync(), 1, 1);

        Assert.Single(overlay.Pulls[0].MobKeys);
        Assert.Single(overlay.Pulls[0].Forces!.Unresolved);
    }

    // ---- geometry -------------------------------------------------------------------------

    [Fact]
    public async Task A_pull_gets_an_outline_around_its_mobs_with_its_number_at_the_centre()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1, 3]))), await FixtureDungeonAsync(), 1, 1);

        var pull = overlay.Pulls[0];
        Assert.Equal(2, pull.OnThisSubLevel);
        Assert.True(pull.Outline.Count > 8);

        // Clones 1 and 3 are at (100, -100) and (300, -300), so canvas (100, 100) and (300, 300).
        Assert.Equal(200, pull.Center.X, precision: 6);
        Assert.Equal(200, pull.Center.Y, precision: 6);
    }

    /// <summary>
    /// An off-sublevel mob must not drag the hull across a map it is not drawn on — but it is
    /// still in the pull, and still counts for forces.
    /// </summary>
    [Fact]
    public async Task A_pull_whose_mobs_are_all_on_another_sublevel_draws_nothing_but_still_counts()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), subLevel: 2, currentPull: 1);

        var pull = overlay.Pulls[0];
        Assert.Empty(pull.Outline);
        Assert.Equal(0, pull.OnThisSubLevel);
        Assert.Single(pull.MobKeys);
        Assert.Equal(5, pull.Forces!.Forces);
    }

    // ---- the readout ----------------------------------------------------------------------

    [Fact]
    public async Task The_forces_readout_is_cumulative_to_the_current_pull()
    {
        var route = RouteOf(
            PullOf(1, null, (1, [1])),      // 5
            PullOf(2, null, (2, [1])),      // 3
            PullOf(3, null, (1, [3])));     // 42

        var dungeon = await FixtureDungeonAsync();

        Assert.Equal("5/100 (5.00%)", RouteOverlay.Build(route, dungeon, 1, 1).ForcesReadout);
        Assert.Equal("8/100 (8.00%)", RouteOverlay.Build(route, dungeon, 1, 2).ForcesReadout);
        Assert.Equal("50/100 (50.00%)", RouteOverlay.Build(route, dungeon, 1, 3).ForcesReadout);
    }

    /// <summary>Before the first pull the route is worth nothing, not the whole dungeon.</summary>
    [Fact]
    public async Task A_cursor_before_the_first_pull_reads_zero()
    {
        var overlay = RouteOverlay.Build(
            RouteOf(PullOf(1, null, (1, [1]))), await FixtureDungeonAsync(), 1, currentPull: 0);

        Assert.Equal(0, overlay.CumulativeForces);
        Assert.Equal("0/100 (0.00%)", overlay.ForcesReadout);
    }

    /// <summary>The overlay must not become a second, disagreeing forces implementation.</summary>
    [Fact]
    public async Task The_forces_are_the_same_ones_RouteForces_counts()
    {
        var route = RouteOf(PullOf(1, null, (1, [1])), PullOf(2, null, (1, [3]), (3, [1])));
        var dungeon = await FixtureDungeonAsync();

        var expected = RouteForces.Count(route, dungeon);
        var actual = RouteOverlay.Build(route, dungeon, 1, 1).Forces;

        // Field by field: PullForces holds a List<string>, so record equality compares that
        // member by reference and would pass two disagreeing runs off as different.
        Assert.Equal(expected.Count, actual.Count);
        Assert.Equal(
            expected.Select(f => (f.PullNumber, f.Forces, f.Cumulative, f.MobCount, f.DungeonTotal)),
            actual.Select(f => (f.PullNumber, f.Forces, f.Cumulative, f.MobCount, f.DungeonTotal)));
    }

    // ---- annotations -----------------------------------------------------------------------

    private static RouteObject Note(
        int index, double x, double y, int? subLevel = 1, bool shown = true, string text = "note")
        => new()
        {
            Index = index,
            Kind = RouteObjectKind.Note,
            SubLevel = subLevel,
            Shown = shown,
            Position = new MapPoint(x, y),
            Text = text,
        };

    private static RouteObject Drawing(int index, params (double X1, double Y1, double X2, double Y2)[] segments)
        => new()
        {
            Index = index,
            Kind = RouteObjectKind.Polyline,
            SubLevel = 1,
            Shown = true,
            Color = "ff3eff",
            Segments = [.. segments.Select(s =>
                new RouteSegment(new MapPoint(s.X1, s.Y1), new MapPoint(s.X2, s.Y2)))],
        };

    private static async Task<RouteOverlayResult> OverlayOf(
        IEnumerable<RouteObject> objects, int subLevel = 1)
        => RouteOverlay.Build(
            new Route { DungeonIndex = 4242, Objects = [.. objects] },
            await FixtureDungeonAsync(), subLevel, currentPull: 1);

    /// <summary>
    /// ⚠ The divergence from clones, and the reason <see cref="MapGeometry.IsVisibleOn"/> is not
    /// reused: MDT tests <c>obj.d[3] == currentSublevel</c> (<c>PresetObjects.lua:177</c>), so an
    /// object naming no sublevel matches nothing — where a clone naming none shows everywhere.
    /// </summary>
    [Fact]
    public async Task An_annotation_with_no_sublevel_is_drawn_nowhere_unlike_a_clone_with_none()
    {
        var overlay = await OverlayOf([Note(1, 100, -100, subLevel: null)]);

        Assert.Empty(overlay.Annotations);
    }

    [Fact]
    public async Task An_annotation_on_another_sublevel_or_hidden_is_not_drawn()
    {
        var overlay = await OverlayOf(
        [
            Note(1, 100, -100, subLevel: 2),
            Note(2, 200, -200, shown: false),
            Note(3, 300, -300),
        ]);

        var drawn = Assert.Single(overlay.Annotations);
        Assert.Equal(3, drawn.Number);
        Assert.Equal(300, drawn.Position.X);
    }

    /// <summary>
    /// ⚠ Numbered across the whole route, not within the drawn subset — so a pin, its row in the
    /// notes list and <c>route decode --notes</c> cannot disagree about which note is note 3.
    /// </summary>
    [Fact]
    public async Task Notes_are_numbered_across_the_whole_route_so_a_filtered_one_still_spends_its_number()
    {
        var overlay = await OverlayOf(
        [
            Note(1, 10, -10),
            Note(2, 20, -20, subLevel: 2),      // not drawn here, but still note 2
            Note(3, 30, -30),
        ]);

        Assert.Equal([1, 3], overlay.Notes.Select(n => n.Number));
    }

    [Fact]
    public async Task A_drawing_gets_no_note_number()
    {
        var overlay = await OverlayOf([Drawing(1, (0, 0, 10, -10))]);

        Assert.Equal(0, Assert.Single(overlay.Annotations).Number);
    }

    /// <summary>y is flipped exactly as it is for a blip; x passes straight through.</summary>
    [Fact]
    public async Task An_annotation_is_transformed_into_canvas_space()
    {
        var overlay = await OverlayOf([Note(1, 686.1, -459.4)]);

        var (x, y) = MapGeometry.ToCanvas(686.1, -459.4);
        Assert.Equal(x, Assert.Single(overlay.Annotations).Position.X, 6);
        Assert.Equal(y, Assert.Single(overlay.Annotations).Position.Y, 6);
    }

    /// <summary>
    /// ⚠ <c>l</c> is a list of segments, so contiguity is a fact about the data rather than a
    /// guarantee of the format. A run that chains becomes one round-joined figure; a break stays
    /// a break, because MDT draws it as one.
    /// </summary>
    [Fact]
    public async Task Chained_segments_coalesce_into_one_figure_and_a_break_starts_another()
    {
        var overlay = await OverlayOf([Drawing(1,
            (0, 0, 10, -10),
            (10, -10, 20, -20),     // chains onto the first
            (50, -50, 60, -60))]);  // a deliberate break

        var figures = Assert.Single(overlay.Annotations).Figures;

        Assert.Equal(2, figures.Count);
        Assert.Equal(3, figures[0].Count);   // three points, not two segments
        Assert.Equal(2, figures[1].Count);
    }

    /// <summary>MDT's own factor. <c>lineFactor</c> is deliberately not in it.</summary>
    [Fact]
    public async Task Stroke_thickness_is_MDTs_brush_size_times_its_own_factor()
    {
        var overlay = await OverlayOf([Drawing(1, (0, 0, 10, -10)) with { BrushSize = 9 }]);

        Assert.Equal(
            9 * RouteOverlay.LineThicknessFactor, Assert.Single(overlay.Annotations).Thickness);
    }

    /// <summary>An unreadable colour becomes white, as MDT rewrites it (<c>PresetObjects.lua:185-189</c>).</summary>
    [Fact]
    public async Task A_junk_colour_falls_back_to_white_rather_than_reaching_a_draw_loop()
    {
        var drawing = Drawing(1, (0, 0, 10, -10)) with { Color = "not a colour" };
        var overlay = await OverlayOf([drawing]);

        Assert.Equal("ffffff", Assert.Single(overlay.Annotations).Color);
    }

    [Fact]
    public async Task Draw_layer_orders_annotations_and_wire_order_breaks_the_tie()
    {
        var overlay = await OverlayOf(
        [
            Note(1, 10, -10) with { DrawLayer = 3 },
            Note(2, 20, -20) with { DrawLayer = -8 },
            Note(3, 30, -30) with { DrawLayer = -8 },
        ]);

        Assert.Equal([2, 3, 1], overlay.Annotations.Select(a => a.Number));
    }

    /// <summary>
    /// MDT stores <c>atan2(starty - y, startx - x)</c> and adds π when drawing; WoW rotates
    /// counter-clockwise in radians and WPF clockwise in degrees. Three conventions, so the
    /// conversion is arithmetic in <c>Core</c> rather than a guess in a draw loop.
    /// </summary>
    [Theory]
    [InlineData(0, 180)]
    [InlineData(Math.PI, 0)]
    [InlineData(-Math.PI / 2, 270)]
    [InlineData(Math.PI / 2, 90)]
    public void An_arrows_stored_rotation_becomes_clockwise_degrees(double stored, double expected)
        => Assert.Equal(expected, RouteOverlay.HeadAngle(stored), 6);

    [Fact]
    public async Task An_arrow_carries_its_converted_angle_and_a_drawing_carries_none()
    {
        var arrow = Drawing(1, (0, 0, 10, -10)) with
        {
            Kind = RouteObjectKind.Arrow, HeadRotation = 0,
        };

        var overlay = await OverlayOf([arrow, Drawing(2, (0, 0, 5, -5))]);

        Assert.Equal(180, overlay.Annotations[0].HeadAngleDegrees!.Value, 6);
        Assert.Null(overlay.Annotations[1].HeadAngleDegrees);
    }

    /// <summary>The panel splits a note into a heading and a body; a one-line note has no body.</summary>
    [Fact]
    public async Task A_notes_first_line_is_its_title_and_the_rest_is_its_body()
    {
        var overlay = await OverlayOf(
        [
            Note(1, 10, -10, text: "GOLDEN SERPENT — STACK THE GOLD\nDrop Spit Gold pools together."),
            Note(2, 20, -20, text: "A strong team can chain pull 10 and 11"),
        ]);

        Assert.Equal("GOLDEN SERPENT — STACK THE GOLD", overlay.Annotations[0].Title);
        Assert.Equal("Drop Spit Gold pools together.", overlay.Annotations[0].Body);

        Assert.Equal("A strong team can chain pull 10 and 11", overlay.Annotations[1].Title);
        Assert.Equal("", overlay.Annotations[1].Body);
    }

    /// <summary>The common case: a route with no annotations gets an empty list, not a null.</summary>
    [Fact]
    public async Task A_route_with_no_annotations_has_an_empty_annotation_list()
        => Assert.Empty((await OverlayOf([])).Annotations);
}

using System.Formats.Cbor;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Tests.Routes;

/// <summary>
/// A preset's <c>objects</c> — the author's notes and drawings.
/// </summary>
/// <remarks>
/// The same split the rest of this folder uses: a real exported route pins <b>reality</b>, and
/// synthetic CBOR pins the shapes reality does not happen to contain. The real one here is
/// <c>Fixtures/skandar-kings-rest.txt</c>, a keystone.guru export whose sixteen notes are most
/// of what makes it a tank guide rather than a pull order.
/// <para>
/// ⚠ Nothing here asserts forces. King's Rest is not a Midnight dungeon and these tests are
/// hermetic — no test in this suite reads the downloaded MDT cache — so the route's
/// <c>617/608</c> is verified through <c>mdtdesk route decode</c> instead, which is where a
/// dungeon actually exists.
/// </para>
/// </remarks>
public class RouteObjectTests
{
    private static Route KingsRest() => RouteDecoder.Decode(File.ReadAllText(
        Path.Combine(AppContext.BaseDirectory, "Routes", "Fixtures", "skandar-kings-rest.txt")));

    // ---- the real route -------------------------------------------------------------------

    [Fact]
    public void The_real_route_carries_sixteen_notes_and_two_drawings()
    {
        var route = KingsRest();

        Assert.Equal(18, route.Objects.Count);
        Assert.Equal(0, route.UnreadableObjects);
        Assert.Equal(16, route.Objects.Count(o => o.Kind == RouteObjectKind.Note));
        Assert.Equal(2, route.Objects.Count(o => o.Kind == RouteObjectKind.Polyline));

        // No arrow in this route — which is why the arrow shapes below are synthetic.
        Assert.DoesNotContain(route.Objects, o => o.Kind == RouteObjectKind.Arrow);
    }

    /// <summary>
    /// The pins keystone.guru shows as <c>!</c> markers ARE MDT preset notes, re-skinned — this
    /// text is the popup in its own UI, verbatim.
    /// </summary>
    [Fact]
    public void A_notes_text_survives_decoding_verbatim()
    {
        var note = KingsRest().Objects[5];

        Assert.Equal(6, note.Index);
        Assert.Equal(RouteObjectKind.Note, note.Kind);
        Assert.Equal(1, note.SubLevel);
        Assert.True(note.Shown);
        Assert.StartsWith("GOLDEN SERPENT — STACK THE GOLD", note.Text);
        Assert.Contains("hard-swap to Animated Gold", note.Text);
    }

    /// <summary>⚠ Coordinates cross as STRINGS — <c>str('750.6')</c>, <c>str('-425')</c>.</summary>
    [Fact]
    public void Note_positions_are_read_from_the_strings_they_cross_as()
    {
        var notes = KingsRest().Objects.Where(o => o.Kind == RouteObjectKind.Note).ToList();

        Assert.Equal(750.6, notes[5].Position.X, 3);
        Assert.Equal(-425, notes[5].Position.Y, 3);

        // The measured extremes, inside the project's documented clone+POI range.
        Assert.Equal(102.9, notes.Min(n => n.Position.X), 3);
        Assert.Equal(750.6, notes.Max(n => n.Position.X), 3);
        Assert.Equal(-544.6, notes.Min(n => n.Position.Y), 3);
        Assert.Equal(-129.5, notes.Max(n => n.Position.Y), 3);
    }

    /// <summary>
    /// Both drawings' <c>l</c> are a whole number of four-value segment groups — 24 and 16
    /// values, so 6 and 4 segments. A leftover would show up here as a lost segment.
    /// </summary>
    [Fact]
    public void The_real_routes_drawings_are_whole_segment_quads()
    {
        var drawings = KingsRest().Objects
            .Where(o => o.Kind == RouteObjectKind.Polyline).ToList();

        Assert.Equal([6, 4], drawings.Select(d => d.Segments.Count));
        Assert.All(drawings, d => Assert.Equal("ffffff", d.Color));
        Assert.All(drawings, d => Assert.Equal(5, d.BrushSize));
        Assert.All(drawings, d => Assert.Equal(-8, d.DrawLayer));
        Assert.All(drawings, d => Assert.True(d.Smooth));
    }

    /// <summary>
    /// In practice a pencil stroke IS contiguous — every segment's end is the next one's start.
    /// The format does not guarantee it, which is why the reader stores segments rather than a
    /// path, but the real route is the evidence that the common case looks like a stroke.
    /// </summary>
    [Fact]
    public void The_real_routes_segments_chain_end_to_start()
    {
        foreach (var drawing in KingsRest().Objects.Where(o => o.Kind == RouteObjectKind.Polyline))
            for (var i = 1; i < drawing.Segments.Count; i++)
                Assert.Equal(drawing.Segments[i - 1].To, drawing.Segments[i].From);
    }

    /// <summary>The overwhelmingly common route carries none, and says so rather than throwing.</summary>
    [Fact]
    public void A_route_with_no_objects_decodes_to_an_empty_list()
    {
        var route = RouteDecoder.Decode(File.ReadAllText(
            Path.Combine(AppContext.BaseDirectory, "Routes", "Fixtures", "yoda-easy-route.txt")));

        Assert.Empty(route.Objects);
        Assert.Equal(0, route.UnreadableObjects);
    }

    // ---- the shapes the real route does not contain ---------------------------------------

    /// <summary>
    /// ⚠ <c>objects</c> is a sibling of <c>text</c> and <c>uid</c> on the preset ROOT, not a
    /// member of <c>value</c> where <c>pulls</c> lives. Obvious once, invisible afterwards.
    /// </summary>
    [Fact]
    public void Objects_are_read_from_the_preset_root_rather_than_from_value()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            WriteNote(o, "686.1", "-459.4", 1, true, "on the root");
            o.WriteEndArray();
        }));

        Assert.Single(route.Objects);
        Assert.Equal("on the root", route.Objects[0].Text);
    }

    [Fact]
    public void An_arrow_is_a_stroke_that_also_carries_a_head_rotation()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);

            o.WriteStartMap(3);
            WriteDrawingD(o);
            SyntheticRoute.WriteText(o, "l");
            o.WriteStartArray(4);
            foreach (var n in new[] { "10", "-20", "30", "-40" }) SyntheticRoute.WriteText(o, n);
            o.WriteEndArray();
            // `t` is what makes a stroke an arrow, and t[1] is the head rotation in radians.
            SyntheticRoute.WriteText(o, "t");
            o.WriteStartArray(1); o.WriteDouble(1.25); o.WriteEndArray();
            o.WriteEndMap();

            o.WriteEndArray();
        }));

        var arrow = Assert.Single(route.Objects);
        Assert.Equal(RouteObjectKind.Arrow, arrow.Kind);
        Assert.Equal(1.25, arrow.HeadRotation!.Value, 6);
        Assert.Single(arrow.Segments);
    }

    /// <summary>
    /// ⚠ The likely case, not the exotic one: erasing a drawing leaves a hole, and a Lua table
    /// with a hole serialises as an integer-keyed map rather than an array.
    /// </summary>
    [Fact]
    public void A_sparse_objects_map_is_read_in_key_order()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartMap(2);
            o.WriteInt32(3); o.WriteStartMap(2); WriteNoteD(o, "1", "-1", 1, true, "third"); WriteN(o); o.WriteEndMap();
            o.WriteInt32(1); o.WriteStartMap(2); WriteNoteD(o, "2", "-2", 1, true, "first"); WriteN(o); o.WriteEndMap();
            o.WriteEndMap();
        }));

        Assert.Equal(["first", "third"], route.Objects.Select(o => o.Text));
        // The Lua key is the object's index, so an erased slot does not renumber the survivors.
        Assert.Equal([1, 3], route.Objects.Select(o => o.Index));
    }

    /// <summary>
    /// ⚠ The trap this reader exists for. MDT builds a drawing's <c>d</c> with a literal
    /// <c>nil</c> at index 6 (<c>Toolbar.lua:542-543</c>), so it crosses as a map keyed
    /// 1-5 and 7. Collapsing that hole slides <c>smooth</c> into <c>drawLayer</c>'s slot —
    /// silently, with nothing thrown anywhere.
    /// </summary>
    [Fact]
    public void A_sparse_d_keeps_smooth_at_index_seven_rather_than_sliding_it_into_drawLayer()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            o.WriteStartMap(2);

            SyntheticRoute.WriteText(o, "d");
            o.WriteStartMap(6);                       // keys 1-5 and 7; no key 6
            o.WriteInt32(1); o.WriteInt32(9);         // size
            o.WriteInt32(2); o.WriteInt32(1);         // lineFactor
            o.WriteInt32(3); o.WriteInt32(1);         // sublevel
            o.WriteInt32(4); o.WriteBoolean(true);    // shown
            o.WriteInt32(5); SyntheticRoute.WriteText(o, "ff3eff");
            o.WriteInt32(7); o.WriteBoolean(true);    // smooth
            o.WriteEndMap();

            SyntheticRoute.WriteText(o, "l");
            o.WriteStartArray(4);
            foreach (var n in new[] { "1", "-1", "2", "-2" }) SyntheticRoute.WriteText(o, n);
            o.WriteEndArray();

            o.WriteEndMap();
            o.WriteEndArray();
        }));

        var drawing = Assert.Single(route.Objects);
        Assert.True(drawing.Smooth);          // read from key 7, not from the collapsed position
        Assert.Equal(0, drawing.DrawLayer);   // the hole stays a hole
        Assert.Equal(9, drawing.BrushSize);
        Assert.Equal("ff3eff", drawing.Color);
    }

    /// <summary>MDT rounds coordinates, so a whole number can cross as an int rather than a string.</summary>
    [Fact]
    public void Coordinates_that_cross_as_integers_read_the_same_as_ones_that_cross_as_strings()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            o.WriteStartMap(2);
            SyntheticRoute.WriteText(o, "d");
            o.WriteStartArray(5);
            o.WriteInt32(400); o.WriteInt32(-250); o.WriteInt32(1); o.WriteBoolean(true);
            SyntheticRoute.WriteText(o, "integer coordinates");
            o.WriteEndArray();
            WriteN(o);
            o.WriteEndMap();
            o.WriteEndArray();
        }));

        Assert.Equal(400, route.Objects[0].Position.X);
        Assert.Equal(-250, route.Objects[0].Position.Y);
    }

    /// <summary>Hidden rather than deleted. It decodes; whether it is drawn is the overlay's call.</summary>
    [Fact]
    public void A_hidden_object_still_decodes_and_says_it_is_hidden()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            WriteNote(o, "10", "-10", 1, shown: false, "hidden");
            o.WriteEndArray();
        }));

        Assert.False(Assert.Single(route.Objects).Shown);
    }

    /// <summary>
    /// ⚠ The whole posture: annotations are decoration, so a bad one costs itself and nothing
    /// else. A route that draws one of its two notes beats one that refuses to open.
    /// </summary>
    [Fact]
    public void A_malformed_object_is_skipped_and_counted_while_the_rest_of_the_route_loads()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(3);
            SyntheticRoute.WriteText(o, "not a table at all");
            WriteNote(o, "10", "-10", 1, true, "good");
            // A note with no position: nowhere to put the pin, so there is nothing to draw.
            o.WriteStartMap(2);
            SyntheticRoute.WriteText(o, "d");
            o.WriteStartArray(1); SyntheticRoute.WriteText(o, "no coordinates"); o.WriteEndArray();
            WriteN(o);
            o.WriteEndMap();
            o.WriteEndArray();
        }));

        Assert.Equal("good", Assert.Single(route.Objects).Text);
        Assert.Equal(2, route.UnreadableObjects);
        Assert.Single(route.Pulls);   // the route itself is untouched
    }

    /// <summary>
    /// A truncated final group is missing data, not a corrupt string — so it is dropped, and
    /// the segments that ARE complete still draw.
    /// </summary>
    [Fact]
    public void A_line_list_that_is_not_a_multiple_of_four_keeps_its_complete_segments()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            o.WriteStartMap(2);
            WriteDrawingD(o);
            SyntheticRoute.WriteText(o, "l");
            o.WriteStartArray(6);
            foreach (var n in new[] { "1", "-1", "2", "-2", "3", "-3" }) SyntheticRoute.WriteText(o, n);
            o.WriteEndArray();
            o.WriteEndMap();
            o.WriteEndArray();
        }));

        var drawing = Assert.Single(route.Objects);
        Assert.Single(drawing.Segments);
        Assert.Equal(new MapPointLike(1, -1), Point(drawing.Segments[0].From));
        Assert.Equal(new MapPointLike(2, -2), Point(drawing.Segments[0].To));
    }

    /// <summary>A drawing with nothing left to draw is not an object; MDT deletes such leftovers itself.</summary>
    [Fact]
    public void A_drawing_with_no_readable_segments_is_dropped()
    {
        var route = SyntheticRoute.Decode(w => WriteRoute(w, objects: o =>
        {
            o.WriteStartArray(1);
            o.WriteStartMap(2);
            WriteDrawingD(o);
            SyntheticRoute.WriteText(o, "l"); o.WriteStartArray(0); o.WriteEndArray();
            o.WriteEndMap();
            o.WriteEndArray();
        }));

        Assert.Empty(route.Objects);
        Assert.Equal(1, route.UnreadableObjects);
    }

    // ---- writing helpers -------------------------------------------------------------------

    private readonly record struct MapPointLike(double X, double Y);

    private static MapPointLike Point(Core.Map.MapPoint p) => new(p.X, p.Y);

    /// <summary>A one-pull route with an <c>objects</c> member written by the caller.</summary>
    private static void WriteRoute(CborWriter w, Action<CborWriter> objects)
    {
        w.WriteStartMap(2);

        SyntheticRoute.WriteText(w, "objects");
        objects(w);

        SyntheticRoute.WriteText(w, "value");
        w.WriteStartMap(2);
        SyntheticRoute.WriteText(w, "currentDungeonIdx"); w.WriteInt32(164);
        SyntheticRoute.WriteText(w, "pulls");
        w.WriteStartArray(1);
        w.WriteStartMap(1);
        w.WriteInt32(1); w.WriteStartArray(1); w.WriteInt32(1); w.WriteEndArray();
        w.WriteEndMap();
        w.WriteEndArray();
        w.WriteEndMap();

        w.WriteEndMap();
    }

    private static void WriteNote(
        CborWriter w, string x, string y, int subLevel, bool shown, string text)
    {
        w.WriteStartMap(2);
        WriteNoteD(w, x, y, subLevel, shown, text);
        WriteN(w);
        w.WriteEndMap();
    }

    /// <summary>A note's <c>d</c>: x, y, sublevel, shown, text.</summary>
    private static void WriteNoteD(
        CborWriter w, string x, string y, int subLevel, bool shown, string text)
    {
        SyntheticRoute.WriteText(w, "d");
        w.WriteStartArray(5);
        SyntheticRoute.WriteText(w, x);
        SyntheticRoute.WriteText(w, y);
        w.WriteInt32(subLevel);
        w.WriteBoolean(shown);
        SyntheticRoute.WriteText(w, text);
        w.WriteEndArray();
    }

    /// <summary>A drawing's <c>d</c>, dense: size, lineFactor, sublevel, shown, colour, layer, smooth.</summary>
    private static void WriteDrawingD(CborWriter w)
    {
        SyntheticRoute.WriteText(w, "d");
        w.WriteStartArray(7);
        w.WriteInt32(5); w.WriteInt32(1); w.WriteInt32(1); w.WriteBoolean(true);
        SyntheticRoute.WriteText(w, "ffffff");
        w.WriteInt32(-8); w.WriteBoolean(true);
        w.WriteEndArray();
    }

    /// <summary>The flag that makes an object a note.</summary>
    private static void WriteN(CborWriter w)
    {
        SyntheticRoute.WriteText(w, "n");
        w.WriteBoolean(true);
    }
}

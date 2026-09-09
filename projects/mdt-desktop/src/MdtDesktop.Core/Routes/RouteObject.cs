using MdtDesktop.Core.Map;

namespace MdtDesktop.Core.Routes;

/// <summary>Which of MDT's three stored annotation shapes an object is.</summary>
/// <remarks>
/// MDT's toolbar offers <b>four</b> creating tools — pencil, line, arrow and note
/// (<c>Modules/Toolbar.lua:177-207</c>) — but stores only three shapes: a pencil stroke and a
/// straight line are indistinguishable on the wire, both being a list of segments with no arrow
/// head.
/// </remarks>
public enum RouteObjectKind
{
    /// <summary>A text pin. <c>n = true</c>, and the text lives in <c>d[5]</c>.</summary>
    Note,

    /// <summary>A freehand or straight stroke: segments, a colour and a brush size.</summary>
    Polyline,

    /// <summary>A stroke of exactly one segment with a head rotation in <c>t[1]</c>.</summary>
    Arrow,
}

/// <summary>
/// One entry of a preset's <c>objects</c> array — the author's own annotations over the map.
/// </summary>
/// <remarks>
/// <para>
/// <c>objects</c> is a sibling of <c>text</c> / <c>uid</c> / <c>difficulty</c> on the preset
/// <b>root</b>, not under <c>value</c> where <c>pulls</c> lives. MDT's own schema comment
/// (<c>Modules/PresetObjects.lua:174-175</c>) is the whole format:
/// <code>
/// --d: size,lineFactor,sublevel,shown,colorstring,drawLayer,[smooth]
/// --l: x1,y1,x2,y2,...
/// </code>
/// A note reuses <c>d</c> for something else entirely: <c>x, y, sublevel, shown, text</c>.
/// </para>
/// <para>
/// ⚠ <b>Coordinates and the colour cross as strings</b>, while sublevel, size, lineFactor and
/// drawLayer cross as integers and <c>shown</c> / <c>smooth</c> as booleans — <c>d</c> is a
/// genuinely mixed array. Measured on a real keystone.guru export:
/// <c>NOTE d : str('686.1') str('-459.4') int(1) bool(True) str('OPENING — PURGE…')</c>.
/// </para>
/// <para>
/// One flat record with a kind enum rather than a hierarchy: the three kinds share almost every
/// field, <c>RouteWarningKind</c> already establishes the <c>…Kind</c> naming, and a flat shape
/// keeps <c>route decode --json</c> readable.
/// </para>
/// </remarks>
public sealed record RouteObject
{
    /// <summary>1-based position in the <c>objects</c> array. Also a note's displayed number.</summary>
    /// <remarks>
    /// ⚠ A note's number is <b>positional, not stored</b> — MDT numbers pins in draw order
    /// (<c>PresetObjects.lua:582,587-588</c>).
    /// </remarks>
    public required int Index { get; init; }

    public required RouteObjectKind Kind { get; init; }

    /// <summary>
    /// The sublevel the object is drawn on. ⚠ <b>Null means NOT DRAWN</b>, unlike a
    /// <c>Clone</c>.
    /// </summary>
    /// <remarks>
    /// MDT draws an object only <c>if obj.d[3] == currentSublevel and obj.d[4]</c>
    /// (<c>PresetObjects.lua:177</c>) — an equality test, so a missing sublevel matches nothing.
    /// <c>Clone.SubLevel == null</c> is the opposite, MDT's own "show everywhere", which is why
    /// <see cref="MapGeometry.IsVisibleOn"/> must not be reused for an object.
    /// </remarks>
    public required int? SubLevel { get; init; }

    /// <summary><c>d[4]</c>. False for an object the author hid rather than deleted.</summary>
    public required bool Shown { get; init; }

    /// <summary>The note's text. Null for a drawing.</summary>
    public string? Text { get; init; }

    /// <summary>Where the note pin sits, in the unscaled canvas space clones and POIs use.</summary>
    /// <remarks>
    /// ⚠ A <c>Map</c> type in a <c>Routes</c> model, deliberately: these really are map points,
    /// in the very same space, and a second local struct would be the drift rather than the fix.
    /// Objects are stored divided by <c>MDT:GetScale()</c> and drawn multiplied by it, and
    /// <c>GetScale()</c> is <c>db.scale</c>, a pure UI zoom preference
    /// (<c>MainFrame.lua:229</c>) — the identical treatment <c>mapPOIs</c> gets
    /// (<c>Pointsofinterest.lua:54-58</c>). So <see cref="MapGeometry.ToCanvas"/> applies
    /// directly, with no new arithmetic.
    /// </remarks>
    public MapPoint Position { get; init; }

    /// <summary>
    /// The stroke, as the <b>segments</b> it is stored as. Empty for a note.
    /// </summary>
    /// <remarks>
    /// ⚠ <c>l</c> is <b>not a polyline</b>. <c>Toolbar.lua:640-644</c> appends four numbers per
    /// segment (<c>oldx, oldy, x, y</c>, then <c>lineIdx += 4</c>) and the draw loop
    /// (<c>PresetObjects.lua:194-219</c>) consumes four at a time, resetting all four after
    /// each. So <c>x1,y1,x2,y2, x3,y3,x4,y4</c> is segment (1→2) and segment (3→4), with the
    /// shared endpoint appearing twice. Reading it as a plain polyline would invent segments
    /// MDT does not draw.
    /// </remarks>
    public IReadOnlyList<RouteSegment> Segments { get; init; } = [];

    /// <summary>Six hex digits, no leading <c>#</c>. Null when the object carried none.</summary>
    public string? Color { get; init; }

    /// <summary><c>d[1]</c>. MDT strokes at <c>size * 0.3</c> (<c>PresetObjects.lua:211</c>).</summary>
    public double BrushSize { get; init; } = 5;

    /// <summary>
    /// An arrow's head rotation in radians, exactly as stored (<c>t[1]</c>).
    /// </summary>
    /// <remarks>
    /// MDT stores <c>atan2(starty - y, startx - x)</c> and adds π at draw time
    /// (<c>PresetObjects.lua:225</c> → <c>:479</c>). The conversion into a drawing convention is
    /// <see cref="Map.AnnotationOverlay.HeadAngleDegrees"/>'s, not this model's.
    /// </remarks>
    public double? HeadRotation { get; init; }

    /// <summary><c>d[6]</c>. Orders objects among themselves; lower is further back.</summary>
    public int DrawLayer { get; init; }

    /// <summary>
    /// <c>d[7]</c>. MDT draws circles at every joint when set — round joins and caps.
    /// </summary>
    public bool Smooth { get; init; }

    public override string ToString() => Kind switch
    {
        RouteObjectKind.Note => $"[{Index}] note: {Text?.Split('\n')[0]}",
        _ => $"[{Index}] {Kind.ToString().ToLowerInvariant()}: {Segments.Count} segments",
    };
}

/// <summary>One drawn segment: MDT's four stored numbers, paired.</summary>
public readonly record struct RouteSegment(MapPoint From, MapPoint To);

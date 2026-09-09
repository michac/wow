namespace MdtDesktop.Core.Routes;

/// <summary>A decoded MDT route: which dungeon, and the ordered pulls.</summary>
public sealed class Route
{
    /// <summary>The route's name, as typed in MDT. <c>preset.text</c>.</summary>
    public string? Name { get; init; }

    /// <summary>MDT's own id for the preset.</summary>
    public string? Uid { get; init; }

    /// <summary>The dungeon this route is for — MDT's sparse dungeon index.</summary>
    public int DungeonIndex { get; init; }

    /// <summary>MDT's manual pull cursor at export time. 1-based.</summary>
    public int CurrentPull { get; init; }

    public int CurrentSubLevel { get; init; } = 1;

    /// <summary>Affects displayed enemy health only, never forces.</summary>
    public int? Difficulty { get; init; }

    /// <summary>
    /// The MDT build that exported the route, with the dots stripped — <c>6213</c> for 6.2.13.
    /// Null when the string carries none.
    /// </summary>
    /// <remarks>
    /// MDT's export button sets <c>preset.addonVersion = db.version</c>
    /// (<c>Modules/MainFrame.lua:724</c>, from <c>GetAddOnMetadata(…, "Version"):gsub("%.", "")</c>).
    /// It is the <b>only</b> thing in a route string that says what dungeon data the route was
    /// drawn against, which makes it the difference between a precise staleness check and a guess.
    /// <para>
    /// It is often absent. MDT's own party-share path (<c>Transmission.lua</c>'s
    /// <c>SendToGroup</c>) sets <c>difficulty</c> but not this, and keystone.guru's exporter
    /// omits it too — a KSG-exported string is recognisable by a <c>uid</c> ending <c>xxKG</c>.
    /// </para>
    /// </remarks>
    public int? AddonVersion { get; init; }

    /// <summary>Pulls in order, 1-based via <see cref="Pull.Number"/>.</summary>
    public IReadOnlyList<Pull> Pulls { get; init; } = [];

    /// <summary>
    /// The author's annotations — text notes, strokes and arrows — in the order they were drawn.
    /// </summary>
    /// <remarks>
    /// ⚠ These come off the preset <b>root</b>, not off <c>value</c> where <see cref="Pulls"/>
    /// lives. They carry no pull association whatsoever: a note is about a place on the map, not
    /// about a step in the route.
    /// </remarks>
    public IReadOnlyList<RouteObject> Objects { get; init; } = [];

    /// <summary>
    /// How many entries of <c>objects</c> could not be read at all.
    /// </summary>
    /// <remarks>
    /// Decoding an annotation never throws — a route that draws fifteen of sixteen notes beats
    /// one that refuses to open — so the count is carried instead, and reported rather than
    /// swallowed.
    /// </remarks>
    public int UnreadableObjects { get; init; }
}

/// <summary>
/// One numbered pull: the enemies in it, plus its display colour.
/// </summary>
/// <remarks>
/// On the wire a pull is a single mixed table — integer keys are enemy indices mapping to a
/// list of clone indices, string keys are options. <c>color</c> is the only option key that
/// exists, so "does the key parse as a positive integer" is the whole discrimination.
/// </remarks>
public sealed class Pull
{
    /// <summary>1-based position in the route.</summary>
    public int Number { get; init; }

    /// <summary>Six lowercase hex digits, no leading <c>#</c>. Null when the pull carried none.</summary>
    public string? Color { get; init; }

    /// <summary>
    /// MDT's "no custom colour" sentinel — it writes this in rather than leaving the key unset.
    /// </summary>
    public const string DefaultColor = "228b22";

    /// <summary>True when the author actually picked a colour for this pull.</summary>
    public bool HasCustomColor
        => Color is not null && !Color.Equals(DefaultColor, StringComparison.OrdinalIgnoreCase);

    /// <summary>Enemies in the pull, ordered by enemy index.</summary>
    public IReadOnlyList<PullEnemy> Enemies { get; init; } = [];

    /// <summary>Option keys other than <c>color</c>. Empty in every route seen so far.</summary>
    public IReadOnlyList<string> UnknownOptions { get; init; } = [];

    public override string ToString()
        => $"pull {Number}: {Enemies.Sum(e => e.CloneIndices.Count)} mobs";
}

/// <summary>The clones of one enemy that a pull includes.</summary>
/// <remarks>
/// The clone list can be sparse and out of order after editing, so it is kept exactly as
/// exported rather than sorted or densified.
/// </remarks>
public sealed record PullEnemy(int EnemyIndex, IReadOnlyList<int> CloneIndices);

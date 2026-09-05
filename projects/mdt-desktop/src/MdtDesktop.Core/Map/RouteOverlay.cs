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

        return new RouteOverlayResult(pulls, roleByKey, forces, currentPull);
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
public sealed record RouteOverlayResult(
    IReadOnlyList<PullOverlay> Pulls,
    IReadOnlyDictionary<(int EnemyIndex, int CloneIndex), MapBlipRole> RoleByMob,
    IReadOnlyList<PullForces> Forces,
    int CurrentPull)
{
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

using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Map;

/// <summary>
/// Turns a dungeon's enemy table into the blips to draw for one sublevel.
/// </summary>
/// <remarks>
/// This lives in <c>Core</c> rather than the WPF project on purpose: the arithmetic that
/// decides where a mob lands is the part that can be wrong, so it is the part that is tested.
/// <c>App</c> only draws what comes out.
/// </remarks>
public static class MapLayout
{
    /// <summary>
    /// Every clone that belongs on <paramref name="subLevel"/>, placed and sized.
    /// </summary>
    /// <param name="widthPx">Canvas width to place into; defaults to MDT's own 840 units.</param>
    /// <param name="heightPx">Canvas height to place into; defaults to MDT's own 560 units.</param>
    public static IReadOnlyList<MapBlip> Build(
        Dungeon dungeon, int subLevel,
        double widthPx = MapGeometry.CanvasWidth, double heightPx = MapGeometry.CanvasHeight)
    {
        var blips = new List<MapBlip>();

        foreach (var enemy in dungeon.Enemies)
        {
            foreach (var clone in enemy.Clones)
            {
                if (!MapGeometry.IsVisibleOn(clone, subLevel)) continue;

                var (x, y) = MapGeometry.ToCanvas(clone.X, clone.Y, widthPx, heightPx);

                blips.Add(new MapBlip
                {
                    Enemy = enemy,
                    Clone = clone,
                    X = x,
                    Y = y,
                    Size = MapGeometry.BlipSize(clone, enemy) * (widthPx / MapGeometry.CanvasWidth),
                    Forces = clone.Count ?? enemy.Count,
                    Patrol = [.. clone.Patrol.Select(p =>
                    {
                        var (px, py) = MapGeometry.ToCanvas(p.X, p.Y, widthPx, heightPx);
                        return new MapPoint(px, py);
                    })],
                });
            }
        }

        return blips;
    }
}

/// <summary>One mob on the map: which clone of which enemy, where, how big, and what it is worth.</summary>
public sealed class MapBlip
{
    public required Enemy Enemy { get; init; }
    public required Clone Clone { get; init; }

    /// <summary>Blip <b>centre</b>, not its top-left — MDT anchors the frame by its centre.</summary>
    public required double X { get; init; }
    public required double Y { get; init; }

    /// <summary>Diameter, in the same units as <see cref="X"/>.</summary>
    public required double Size { get; init; }

    /// <summary>What this clone contributes to enemy forces — <c>clone.count ?? enemy.count</c>.</summary>
    public required int Forces { get; init; }

    /// <summary>The clone's patrol waypoints, already placed. Empty for the 3051 that do not patrol.</summary>
    public IReadOnlyList<MapPoint> Patrol { get; init; } = [];

    public bool IsBoss => Enemy.IsBoss;

    /// <summary>How a route names this mob: the enemy index plus the clone index.</summary>
    public (int EnemyIndex, int CloneIndex) Key => (Enemy.Index, Clone.Index);

    /// <summary>What the tooltip says — enough to check a blip against MDT's own window.</summary>
    public string Label
        => $"{Enemy.Name ?? "?"} [{Enemy.Index}.{Clone.Index}] — {Forces} forces" +
           (Enemy.IsBoss ? " (boss)" : "");
}

public readonly record struct MapPoint(double X, double Y);

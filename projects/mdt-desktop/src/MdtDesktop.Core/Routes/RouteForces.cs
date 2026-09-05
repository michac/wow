using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Routes;

/// <summary>
/// The enemy-forces arithmetic — the port of <c>MDT:CountForces</c> (<c>Modules/Pulls.lua</c>).
/// </summary>
/// <remarks>
/// Two details from the original are deliberately not copied:
/// <list type="bullet">
/// <item>
/// MDT's loop <c>break</c>s once <c>pullIdx > currentPull</c>, but it is iterating a
/// <c>pairs()</c> loop, whose order Lua does not guarantee. Here the pulls are simply
/// filtered by number, which is what the break was reaching for.
/// </item>
/// <item>
/// The affix machinery is gone from Midnight MDT — <c>dungeonTotalCount</c> has only
/// <c>normal</c>, and <c>IsCloneIncluded</c> has decayed to a bare existence check. So there
/// is no week, teeming or difficulty filtering to do. Difficulty moves displayed health only.
/// </item>
/// </list>
/// </remarks>
public static class RouteForces
{
    /// <summary>Forces per pull, cumulative, for every pull in the route.</summary>
    public static IReadOnlyList<PullForces> Count(Route route, Dungeon dungeon)
    {
        var results = new List<PullForces>(route.Pulls.Count);
        var cumulative = 0;

        foreach (var pull in route.Pulls.OrderBy(p => p.Number))
        {
            var forces = 0;
            var mobs = 0;
            var unresolved = new List<string>();

            foreach (var entry in pull.Enemies)
            {
                if (!dungeon.EnemiesByIndex.TryGetValue(entry.EnemyIndex, out var enemy))
                {
                    unresolved.Add($"enemy {entry.EnemyIndex} is not in this dungeon");
                    continue;
                }

                foreach (var cloneIndex in entry.CloneIndices)
                {
                    // MDT:IsCloneIncluded is now just "does this clone exist". It still earns
                    // its place: MDT 6.2.13 deleted clone 12 of The Blinding Vale's Radiant
                    // Spellsower, so a route drawn on 6.2.12 references a clone that is gone.
                    if (!enemy.ClonesByIndex.TryGetValue(cloneIndex, out var clone))
                    {
                        unresolved.Add($"{enemy.Name ?? $"enemy {entry.EnemyIndex}"} clone {cloneIndex} no longer exists");
                        continue;
                    }

                    // GetCloneEnemyForces: a clone may award different forces from other
                    // spawns of the same NPC.
                    forces += clone.Count ?? enemy.Count;
                    mobs++;
                }
            }

            cumulative += forces;
            results.Add(new PullForces(pull.Number, forces, cumulative, mobs, dungeon.TotalCount, unresolved));
        }

        return results;
    }

    /// <summary>Cumulative forces up to and including <paramref name="pullNumber"/>.</summary>
    public static int CountUpTo(Route route, Dungeon dungeon, int pullNumber)
        => Count(route, dungeon).Where(p => p.PullNumber <= pullNumber).Sum(p => p.Forces);
}

/// <summary>What one pull is worth, and what it runs the route total to.</summary>
public sealed record PullForces(
    int PullNumber,
    int Forces,
    int Cumulative,
    int MobCount,
    int DungeonTotal,
    IReadOnlyList<string> Unresolved)
{
    /// <summary>Cumulative forces as a percentage of the dungeon's requirement.</summary>
    public double CumulativePercent => DungeonTotal == 0 ? 0 : 100.0 * Cumulative / DungeonTotal;

    /// <summary>This pull's own contribution as a percentage.</summary>
    public double Percent => DungeonTotal == 0 ? 0 : 100.0 * Forces / DungeonTotal;
}

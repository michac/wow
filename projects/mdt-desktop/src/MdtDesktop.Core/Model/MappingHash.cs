using System.Globalization;
using System.Security.Cryptography;
using System.Text;

namespace MdtDesktop.Core.Model;

/// <summary>
/// A fingerprint of one dungeon's mapping — the enemies and clone placements a route's indices
/// refer to.
/// </summary>
/// <remarks>
/// <para>
/// This is what makes "did the ground move under this route?" answerable. A route names enemies
/// by index only, and MDT stamps no version on its dungeon data, so the only way to know a
/// dungeon changed is to have recorded what it looked like before. Stamping a saved route with
/// this hash at import time turns a guess into an exact comparison — the same approach
/// keystone.guru takes with <c>mdt_mapping_hash</c>.
/// </para>
/// <para>
/// It covers what a route actually depends on: the enemy indices, what each is worth, and where
/// its clones stand. Cosmetic churn — a renamed mob, a corrected spell list, an enemy's health —
/// deliberately does not move it, because none of that invalidates a route.
/// </para>
/// <para>
/// ⚠ It answers "has this dungeon changed since import", <b>not</b> "was this route current when
/// imported". A route can arrive already stale, and nothing in a route string can tell us.
/// </para>
/// </remarks>
public static class MappingHash
{
    /// <summary>Hex fingerprint of the dungeon's mapping. Stable across runs and machines.</summary>
    public static string Compute(Dungeon dungeon)
    {
        var sb = new StringBuilder();

        // The denominator is part of the mapping: MDT revises dungeonTotalCount on its own
        // (Temple of Sethraliss went 649 -> 689 -> 649 -> 687 across five weeks), which changes
        // every percentage in a route without touching a single enemy.
        sb.Append(dungeon.Index).Append(':').Append(dungeon.TotalCount).Append('\n');

        foreach (var enemy in dungeon.Enemies.OrderBy(e => e.Index))
        {
            sb.Append(enemy.Index).Append(':')
              .Append(enemy.Id).Append(':')
              .Append(enemy.Count).Append('\n');

            foreach (var clone in enemy.Clones.OrderBy(c => c.Index))
            {
                sb.Append("  ").Append(clone.Index).Append(':')
                  .Append(Number(clone.X)).Append(',')
                  .Append(Number(clone.Y)).Append(':')
                  .Append(clone.SubLevel?.ToString(CultureInfo.InvariantCulture) ?? "-").Append(':')
                  .Append(clone.Count?.ToString(CultureInfo.InvariantCulture) ?? "-").Append('\n');
            }
        }

        var digest = SHA256.HashData(Encoding.UTF8.GetBytes(sb.ToString()));
        // 16 hex characters is 64 bits — ample against accidental collision, and short enough to
        // read in a listing.
        return Convert.ToHexStringLower(digest)[..16];
    }

    /// <summary>Round-trip-exact, culture-invariant, so the hash cannot drift with a locale.</summary>
    private static string Number(double value)
        => value.ToString("G17", CultureInfo.InvariantCulture);
}

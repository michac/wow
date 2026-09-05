namespace MdtDesktop.Core.Model;

/// <summary>
/// What you have to <i>do</i> about a mob. A tactical read, not a taxonomic one.
/// </summary>
/// <remarks>
/// Four values rather than MDT's ten creature types, because a blip is 7.8 map units across
/// for plain trash and a ten-way palette cannot separate at that size. Humanoid vs Undead also
/// tells you nothing you act on; "does it need kicking" does.
/// </remarks>
public enum MobRole
{
    /// <summary>The residual — nothing in the data marks it out.</summary>
    Melee,

    /// <summary>Has at least one spell MDT flags <c>interruptible</c>. Exact, in the data.</summary>
    Caster,

    /// <summary>Worth no forces but far too big to be trash. ⚠ Heuristic — see <see cref="MobRoles"/>.</summary>
    Miniboss,

    /// <summary>MDT's own <c>isBoss</c>. Exact.</summary>
    Boss,
}

/// <summary>
/// Sorts a dungeon's enemies into <see cref="MobRole"/>s.
/// </summary>
/// <remarks>
/// <para>
/// Three of the four rules are read straight out of MDT's data. <b>Only miniboss is invented</b>,
/// because MDT ships no flag for it, and it is the one thing here worth arguing with.
/// </para>
/// <para>
/// The signal it rides on: MDT excludes scripted and encounter mobs from the forces count, so a
/// mob worth <b>zero</b> forces that is nonetheless enormous is not trash the route pulls — it is
/// something the dungeon does to you. Measured on MDT 6.2.13 the trash median health is
/// 1,702,709 and the top zero-forces non-bosses are <c>Infernal</c> 202M, <c>Corewarden
/// Nysarra</c> 72M and <c>Zul'jarra</c> 21M. At <see cref="MinibossHealthMultiple"/> = 3 the rule
/// selects nine mobs across the 16 dungeons.
/// </para>
/// <para>
/// ⚠ <c>scale &gt;= 1.5</c> is deliberately <b>not</b> the rule, though it looks tempting: it
/// covers 128 trash mobs and tracks how the mapper drew the blip rather than what the mob does.
/// </para>
/// <para>
/// The threshold is one named constant on purpose. It cannot be falsified without looking at a
/// rendered map beside the game, so it is built to be moved by one edit rather than tuned blind.
/// </para>
/// </remarks>
public static class MobRoles
{
    /// <summary>
    /// How many times the trash median health a zero-forces mob must have to read as a miniboss.
    /// </summary>
    /// <remarks>⚠ The one invented number in the whole classification. Move this, not the rule.</remarks>
    public const double MinibossHealthMultiple = 3;

    /// <summary>
    /// Classifies one enemy against a health threshold. Precedence: boss, miniboss, caster, melee.
    /// </summary>
    /// <param name="minibossHealth">
    /// The health at or above which a zero-forces mob counts as a miniboss.
    /// <see cref="MobRoleIndex"/> derives it; pass <see cref="double.PositiveInfinity"/> to
    /// switch the heuristic off entirely.
    /// </param>
    public static MobRole Classify(Enemy enemy, double minibossHealth)
    {
        if (enemy.IsBoss) return MobRole.Boss;

        // Zero forces AND far too big to be trash. Both halves matter: plenty of ordinary trash
        // is large, and plenty of zero-forces mobs (Hatchling, and Uncoiled Writhe's small
        // spawns) are trivial. 115 non-boss enemies are worth zero forces; nine clear the bar.
        if (enemy.Count == 0 && enemy.Health >= minibossHealth) return MobRole.Miniboss;

        if (enemy.HasInterruptibleSpell) return MobRole.Caster;

        return MobRole.Melee;
    }
}

/// <summary>
/// The role classification for a whole cache — the miniboss threshold derived once, globally.
/// </summary>
/// <remarks>
/// ⚠ The median is taken across <b>every</b> cached dungeon, not per dungeon. Per-dungeon medians
/// leave 11 of the 16 with no minibosses at all, which reads as a broken feature rather than as a
/// dungeon that happens not to have one; a global bar means "big for trash in this game", which
/// is what the eye is actually asking.
/// </remarks>
public sealed class MobRoleIndex
{
    private MobRoleIndex(double trashMedianHealth)
    {
        TrashMedianHealth = trashMedianHealth;
        MinibossHealth = trashMedianHealth * MobRoles.MinibossHealthMultiple;
    }

    /// <summary>Median health of every non-boss enemy in the cache. 1,702,709 on MDT 6.2.13.</summary>
    public double TrashMedianHealth { get; }

    /// <summary>The derived miniboss bar — the median times <see cref="MobRoles.MinibossHealthMultiple"/>.</summary>
    public double MinibossHealth { get; }

    public static MobRoleIndex Build(DungeonData data)
        => Build(data.Dungeons.SelectMany(d => d.Enemies));

    public static MobRoleIndex Build(IEnumerable<Enemy> enemies)
        => new(Median([.. enemies.Where(e => !e.IsBoss).Select(e => (double)e.Health)]));

    public MobRole Role(Enemy enemy) => MobRoles.Classify(enemy, MinibossHealth);

    /// <summary>How many enemies of a set fall in each role, for a headless sanity check.</summary>
    public IReadOnlyDictionary<MobRole, int> Tally(IEnumerable<Enemy> enemies)
    {
        var tally = Enum.GetValues<MobRole>().ToDictionary(r => r, _ => 0);
        foreach (var enemy in enemies) tally[Role(enemy)]++;
        return tally;
    }

    /// <summary>
    /// The plain median: the mean of the two middle values on an even count.
    /// </summary>
    /// <remarks>
    /// An empty set has no median, and no median means no minibosses — never a bar of zero,
    /// which would promote every zero-forces mob in the game.
    /// </remarks>
    private static double Median(double[] values)
    {
        if (values.Length == 0) return double.PositiveInfinity;

        Array.Sort(values);
        var mid = values.Length / 2;
        return values.Length % 2 == 1
            ? values[mid]
            : (values[mid - 1] + values[mid]) / 2;
    }
}

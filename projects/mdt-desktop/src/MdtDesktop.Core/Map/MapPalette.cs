using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Map;

/// <summary>
/// What colour a blip is, and what badges ride on it.
/// </summary>
/// <remarks>
/// <para>
/// In <c>Core</c> as six hex digits rather than as WPF brushes, for the same reason everything
/// else here is: it can then be printed by the CLI and asserted by a test, and <c>App</c> is
/// left with a hex-to-brush conversion it cannot get wrong.
/// </para>
/// <para>
/// ⚠ <b>Role colour and pull colour coexist.</b> A mob assigned to a pull wears its pull's
/// colour; a mob in no pull wears its role colour. That is not a compromise — it is what MDT
/// itself does (<c>DungeonEnemies.lua:962</c> tints assigned blips from the pull colour,
/// <c>:983</c> resets the rest), and the two sets are disjoint by construction, so the role
/// palette only ever has to separate against itself.
/// </para>
/// <para>
/// ⚠ Whether these four are actually distinguishable at a blip's real size — 7.8 map units for
/// plain trash — cannot be settled here. They are chosen far apart in hue and kept to four for
/// that reason, and two of them are the colours the map already used, so an existing read of it
/// does not reset.
/// </para>
/// </remarks>
public static class MapPalette
{
    /// <summary>Melee — the residual. The blue the map already drew trash in.</summary>
    public const string Melee = "4c8dbe";

    /// <summary>Caster — violet, as far from MDT's <c>228b22</c> pull green as the wheel allows.</summary>
    public const string Caster = "9b6fd8";

    /// <summary>Miniboss — burnt orange: adjacent to the boss gold, because that is the relation.</summary>
    public const string Miniboss = "c2703c";

    /// <summary>Boss — the gold the map already drew bosses in.</summary>
    public const string Boss = "d9a441";

    /// <summary>
    /// A mob worth no forces, whatever its role — it does not move the percentage, so it is
    /// desaturated rather than coloured.
    /// </summary>
    /// <remarks>
    /// Bosses and the two zero-count trash mobs in Altar of Fangs (<c>Hatchling</c>,
    /// <c>Uncoiled Writhe</c>) all land here. Role still wins for a boss or miniboss — being
    /// worth nothing is the normal state for both and says nothing about them.
    /// </remarks>
    public const string NoForces = "5a6570";

    public static string For(MobRole role) => role switch
    {
        MobRole.Boss => Boss,
        MobRole.Miniboss => Miniboss,
        MobRole.Caster => Caster,
        _ => Melee,
    };

    /// <summary>
    /// The fill for one mob: its pull's colour when it is in a pull, otherwise its role's.
    /// </summary>
    /// <param name="pullColor">The pull's colour, or null when the mob is in no pull.</param>
    /// <param name="forces">What the mob is worth. Zero desaturates plain trash.</param>
    public static string For(MobRole role, string? pullColor, int forces)
    {
        if (pullColor is not null) return pullColor;

        // A boss or miniboss is worth nothing by design, so "worth nothing" says nothing about
        // it. For trash it is the whole story: it is not on the route's clock.
        return forces == 0 && role is MobRole.Melee or MobRole.Caster ? NoForces : For(role);
    }

    /// <summary>
    /// A one-character badge per flag, for a row under the blip.
    /// </summary>
    /// <remarks>
    /// Badges rather than fill, because they are orthogonal to role and a mob can carry several
    /// — colour says what a mob <i>is</i>, badges say what can be done <i>to</i> it.
    /// </remarks>
    public static string Badge(SpellFlag flag) => flag switch
    {
        SpellFlag.Enrage => "E",
        SpellFlag.Magic => "M",
        SpellFlag.Curse => "C",
        SpellFlag.Poison => "P",
        SpellFlag.Disease => "D",
        SpellFlag.Bleed => "B",
        _ => "?",
    };

    /// <summary>The badge row for a mob, in the fixed order <see cref="Enemy.SpellFlags"/> gives.</summary>
    public static string Badges(Enemy enemy)
    {
        var badges = string.Concat(enemy.SpellFlags.Select(Badge));
        // Stealth is not a spell flag, but it is the same kind of fact: something you have to
        // do about the mob before you are in range of it.
        if (enemy.Stealth) badges += "s";
        return badges;
    }
}

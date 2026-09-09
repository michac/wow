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

    // ---- the tactical ring -----------------------------------------------------------------

    /// <summary>Interrupt — a kickable cast. The most mandatory and the most time-critical.</summary>
    public const string RingInterrupt = "e34b3f";

    /// <summary>Enrage — soothe it. ⚠ Adjacent in hue to <see cref="Miniboss"/>; see the docs.</summary>
    public const string RingEnrage = "e8892b";

    /// <summary>Crowd control — the mob can be stunned, feared, rooted, silenced, slowed.</summary>
    public const string RingCrowdControl = "3fb8a5";

    /// <summary>
    /// The one <c>characteristics</c> entry that earns no ring.
    /// </summary>
    /// <remarks>
    /// ⚠ Excluded deliberately. It sits on 79 enemies, only 16 of them bosses, so it is not a
    /// boss proxy — but it is not a crowd control that changes how a pull is planned either. It
    /// stays in the tooltip's CC row and out of the ring.
    /// </remarks>
    public const string TauntCharacteristic = "Taunt";

    /// <summary>
    /// A ring around the disc saying what you have to <i>do</i> about the mob, or null for the
    /// 295 that need nothing.
    /// </summary>
    /// <remarks>
    /// <para>
    /// ⚠ This channel exists because <b>fill is spent</b>: under a route a blip wears its pull's
    /// colour, so the role colour is gone exactly when the map is most in use. A ring is the one
    /// channel left that a pull colour cannot overwrite.
    /// </para>
    /// <para>
    /// Measured across all 16 cached dungeons on MDT 6.2.13: 295 of 462 enemies wear no ring,
    /// 111 interrupt, 31 enrage, 49 crowd control. <b>That majority is the point</b> — a ring on
    /// everything is a ring on nothing.
    /// </para>
    /// <para>
    /// Precedence is interrupt → enrage → CC, in the order of how mandatory and how
    /// time-critical the press is. 24 enemies carry two axes and none carries three; those get a
    /// <see cref="RingCue.Dashed"/> ring in the winning colour, which is honest about there
    /// being more without inventing a second channel. The tooltip carries the full picture.
    /// </para>
    /// </remarks>
    public static RingCue? Ring(Enemy enemy)
    {
        var interrupt = enemy.HasInterruptibleSpell;
        var enrage = enemy.Spells.Any(s => s.Enrage);
        var crowdControl = HasCrowdControl(enemy);

        var axes = new List<string>(3);
        if (interrupt) axes.Add("interrupt");
        if (enrage) axes.Add("enrage");
        if (crowdControl) axes.Add("crowd control");

        if (axes.Count == 0) return null;

        var color = interrupt ? RingInterrupt : enrage ? RingEnrage : RingCrowdControl;
        return new RingCue(color, axes.Count > 1, string.Join(" + ", axes));
    }

    /// <summary>Whether the mob is susceptible to anything worth planning a pull around.</summary>
    public static bool HasCrowdControl(Enemy enemy)
        => enemy.Characteristics.Any(
            c => !string.Equals(c, TauntCharacteristic, StringComparison.OrdinalIgnoreCase));
}

/// <summary>
/// The ring one mob wears: its colour, whether it is dashed, and why.
/// </summary>
/// <param name="Color">Six hex digits — the winning axis's colour.</param>
/// <param name="Dashed">True when the mob carries more than one axis, so the ring says so.</param>
/// <param name="Reason">Every axis that matched, in precedence order, for the CLI and the tests.</param>
public sealed record RingCue(string Color, bool Dashed, string Reason);

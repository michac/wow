using System.ComponentModel;
using System.Globalization;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Map;

/// <summary>
/// What a blip's tooltip says, as content rather than as a control.
/// </summary>
/// <remarks>
/// <para>
/// <c>Core</c> owns the content and <c>App</c> owns the look — the same seam
/// <see cref="MapPalette"/> and <see cref="RouteOverlay"/> already establish. That is not only
/// tidiness: a <c>ToolTip</c> is a visual, and building 462 of them at load costs 462 element
/// trees for the two or three a session ever hovers. A data object plus one
/// <c>DataTemplate</c> is materialised lazily, on hover, once.
/// </para>
/// <para>
/// Everything here is offline data. No spell list — ⚠ MDT ships spell <b>ids</b> with no names
/// (<c>[1289416] = {}</c>), so rows would read <c>1289416  interruptible, poison</c>, which is
/// not worth the space — and no wowhead click-through. Both stay parked in <c>backlog.md</c>.
/// </para>
/// </remarks>
public sealed class MobTooltip : INotifyPropertyChanged
{
    private string? _pull;

    /// <summary>The enemy's name.</summary>
    public required string Title { get; init; }

    /// <summary><c>BOSS</c> / <c>MINIBOSS</c> / <c>CASTER</c> / <c>MELEE</c>.</summary>
    public required string RoleLabel { get; init; }

    /// <summary>Creature type and level, e.g. <c>Humanoid · level 90</c>. May be empty.</summary>
    public required string Subtitle { get; init; }

    /// <summary>
    /// The body, in order: stats, tactics, identity.
    /// </summary>
    /// <remarks>
    /// A section with no rows is <b>omitted</b>, so a plain melee mob gets a short tooltip
    /// rather than one padded with empty labels.
    /// </remarks>
    public required IReadOnlyList<TooltipSection> Sections { get; init; }

    /// <summary>
    /// Which pull this mob belongs to under the loaded route, e.g. <c>pull 4</c>, or null.
    /// </summary>
    /// <remarks>
    /// ⚠ <b>The one mutable field, and the reason this is a class rather than a record.</b> Pull
    /// membership changes without the mob changing — loading a route, or clearing one, re-answers
    /// it for every blip on the map — so it cannot be baked into a model built once at
    /// <c>AddBlip</c> time. It is assigned inside the sweep the overlay already performs, and it
    /// is the only property that raises a change notification.
    /// </remarks>
    public string? Pull
    {
        get => _pull;
        set
        {
            if (_pull == value) return;
            _pull = value;
            PropertyChanged?.Invoke(this, PullChanged);
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    private static readonly PropertyChangedEventArgs PullChanged = new(nameof(Pull));

    /// <summary>Builds the whole tooltip for one blip. Everything but <see cref="Pull"/> is final.</summary>
    public static MobTooltip Build(MapBlip blip, MobRole role)
    {
        var enemy = blip.Enemy;

        return new MobTooltip
        {
            Title = enemy.Name ?? "Unknown",
            RoleLabel = role.ToString().ToUpperInvariant(),
            Subtitle = DescribeCreature(enemy),
            Sections = [.. new[] { Stats(blip), Tactics(enemy), Identity(blip) }
                .Where(s => s.Rows.Count > 0)],
        };
    }

    private static string DescribeCreature(Enemy enemy)
    {
        var parts = new List<string>(2);
        if (enemy.CreatureType is { Length: > 0 } type) parts.Add(type);
        if (enemy.Level is { } level) parts.Add($"level {level}");
        return string.Join(" · ", parts);
    }

    private static TooltipSection Stats(MapBlip blip)
    {
        var rows = new List<TooltipRow>(2)
        {
            // Always present, including at zero: "worth nothing" is a fact about the mob, and a
            // missing row would read as "we did not check".
            new("Forces", blip.Forces.ToString(CultureInfo.CurrentCulture)),
        };

        if (blip.Enemy.Health > 0)
            rows.Add(new TooltipRow("Health", blip.Enemy.Health.ToString("N0", CultureInfo.CurrentCulture)));

        return new TooltipSection(rows);
    }

    /// <summary>The three things you can do about a mob, plus the two things it does about you.</summary>
    private static TooltipSection Tactics(Enemy enemy)
    {
        var rows = new List<TooltipRow>(5);

        var kickable = enemy.Spells.Count(s => s.Interruptible);
        if (kickable > 0)
            rows.Add(new TooltipRow("Interrupt", $"{kickable} kickable cast{(kickable == 1 ? "" : "s")}"));

        if (enemy.SpellFlags.Count > 0)
            rows.Add(new TooltipRow(
                "Dispel", string.Join(" · ", enemy.SpellFlags).ToLowerInvariant()));

        // Taunt is listed here even though it earns no ring — the ring is about planning a pull,
        // the tooltip is about knowing what the mob is.
        if (enemy.Characteristics.Count > 0)
            rows.Add(new TooltipRow("CC", string.Join(" · ", enemy.Characteristics)));

        if (enemy.Stealth) rows.Add(new TooltipRow("Stealth", "stealthed"));
        if (enemy.StealthDetect) rows.Add(new TooltipRow("Detects", "sees through stealth"));

        return new TooltipSection(rows);
    }

    /// <summary>
    /// The identity line — how a route names this mob, plus the NPC id.
    /// </summary>
    /// <remarks>
    /// One unlabelled row: the enemy and clone indices are what a route string refers to, so
    /// they are what a blip is cross-checked against MDT's own window with.
    /// </remarks>
    private static TooltipSection Identity(MapBlip blip)
        => new([new TooltipRow(
            "", $"enemy {blip.Enemy.Index} · clone {blip.Clone.Index} · npc {blip.Enemy.Id}")]);
}

/// <param name="Label">Empty for a row that is its own sentence, like the identity line.</param>
public readonly record struct TooltipRow(string Label, string Value);

/// <summary>A group of rows with a rule above it. Never emitted empty.</summary>
public sealed record TooltipSection(IReadOnlyList<TooltipRow> Rows);

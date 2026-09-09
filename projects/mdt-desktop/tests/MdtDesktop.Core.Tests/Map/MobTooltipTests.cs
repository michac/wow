using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// What a blip's tooltip says. The content is in <c>Core</c>; only the look is in <c>App</c>.
/// </summary>
public class MobTooltipTests
{
    private static MapBlip Blip(Enemy enemy, int forces = 7, int cloneIndex = 2)
        => new()
        {
            Enemy = enemy,
            Clone = new Clone { Index = cloneIndex, X = 1, Y = -1 },
            X = 1, Y = 1, Size = 8, Forces = forces,
        };

    private static Enemy Rich => new()
    {
        Index = 3,
        Name = "High Evolutionist",
        Id = 261557,
        Count = 7,
        Health = 2_918_930,
        CreatureType = "Humanoid",
        Level = 90,
        Characteristics = ["Taunt", "Stun", "Fear"],
        Spells =
        [
            new Spell { Id = 1, Interruptible = true },
            new Spell { Id = 2, Interruptible = true, Poison = true },
        ],
    };

    /// <summary>A mob with nothing to say about it beyond its name, forces and index.</summary>
    private static Enemy Plain => new()
    {
        Index = 4, Name = "Plain Mob", Id = 900, Count = 2, Health = 500_000,
        CreatureType = "Beast", Level = 90,
    };

    private static IReadOnlyList<TooltipRow> Rows(MobTooltip tooltip, string label)
        => [.. tooltip.Sections.SelectMany(s => s.Rows).Where(r => r.Label == label)];

    private static string Value(MobTooltip tooltip, string label)
        => Assert.Single(Rows(tooltip, label)).Value;

    // ---- the header -------------------------------------------------------------------------

    [Fact]
    public void The_header_carries_the_name_the_role_and_the_creature_line()
    {
        var tooltip = MobTooltip.Build(Blip(Rich), MobRole.Caster);

        Assert.Equal("High Evolutionist", tooltip.Title);
        Assert.Equal("CASTER", tooltip.RoleLabel);
        Assert.Equal("Humanoid · level 90", tooltip.Subtitle);
    }

    [Fact]
    public void A_nameless_mob_still_gets_a_title()
        => Assert.Equal("Unknown",
            MobTooltip.Build(Blip(new Enemy { Index = 1, Id = 1 }), MobRole.Melee).Title);

    // ---- sections ---------------------------------------------------------------------------

    [Fact]
    public void A_mob_with_tactics_gets_stats_tactics_and_identity()
    {
        var tooltip = MobTooltip.Build(Blip(Rich), MobRole.Caster);

        Assert.Equal(3, tooltip.Sections.Count);
        Assert.Equal("7", Value(tooltip, "Forces"));
        Assert.Equal(2_918_930.ToString("N0"), Value(tooltip, "Health"));
        Assert.Equal("2 kickable casts", Value(tooltip, "Interrupt"));
        Assert.Equal("poison", Value(tooltip, "Dispel"));
        Assert.Equal("Taunt · Stun · Fear", Value(tooltip, "CC"));
    }

    /// <summary>
    /// ⚠ An empty section is omitted, not rendered blank — a plain melee mob gets a short
    /// tooltip rather than one padded with labels that say nothing.
    /// </summary>
    [Fact]
    public void A_mob_with_no_tactics_loses_the_whole_tactics_section()
    {
        var tooltip = MobTooltip.Build(Blip(Plain), MobRole.Melee);

        Assert.Equal(2, tooltip.Sections.Count);
        Assert.Empty(Rows(tooltip, "Interrupt"));
        Assert.Empty(Rows(tooltip, "Dispel"));
        Assert.Empty(Rows(tooltip, "CC"));
    }

    [Fact]
    public void One_kickable_cast_reads_in_the_singular()
    {
        var enemy = new Enemy
        {
            Index = 1, Name = "m", Id = 1, Spells = [new Spell { Id = 1, Interruptible = true }],
        };

        Assert.Equal("1 kickable cast", Value(MobTooltip.Build(Blip(enemy), MobRole.Caster), "Interrupt"));
    }

    /// <summary>Stealth and stealth-detection are the same kind of fact, so they ride along here.</summary>
    [Fact]
    public void Stealth_and_stealth_detection_are_their_own_tactics_rows()
    {
        var enemy = new Enemy
        {
            Index = 1, Name = "m", Id = 1, Stealth = true, StealthDetect = true,
        };
        var tooltip = MobTooltip.Build(Blip(enemy), MobRole.Melee);

        Assert.Equal("stealthed", Value(tooltip, "Stealth"));
        Assert.Equal("sees through stealth", Value(tooltip, "Detects"));
    }

    /// <summary>"Worth nothing" is a fact about the mob; a missing row would read as "unchecked".</summary>
    [Fact]
    public void A_zero_forces_mob_still_gets_a_forces_row()
        => Assert.Equal("0", Value(MobTooltip.Build(Blip(Plain, forces: 0), MobRole.Boss), "Forces"));

    // ---- identity ---------------------------------------------------------------------------

    /// <summary>
    /// One unlabelled row naming the mob the way a route string does, plus the NPC id — which is
    /// what a blip is cross-checked against MDT's own window with.
    /// </summary>
    [Fact]
    public void The_identity_row_names_the_enemy_the_clone_and_the_npc()
    {
        var tooltip = MobTooltip.Build(Blip(Rich, cloneIndex: 2), MobRole.Caster);
        var identity = Assert.Single(tooltip.Sections[^1].Rows);

        Assert.Equal("", identity.Label);
        Assert.Equal("enemy 3 · clone 2 · npc 261557", identity.Value);
    }

    // ---- the one mutable field --------------------------------------------------------------

    /// <summary>
    /// ⚠ Pull membership changes without the mob changing, so it cannot be baked into a model
    /// built once at draw time — it is the one property that moves, and the one that notifies.
    /// </summary>
    [Fact]
    public void Pull_starts_unset_and_raises_a_change_when_it_moves()
    {
        var tooltip = MobTooltip.Build(Blip(Rich), MobRole.Caster);
        Assert.Null(tooltip.Pull);

        var raised = new List<string?>();
        tooltip.PropertyChanged += (_, e) => raised.Add(e.PropertyName);

        tooltip.Pull = "pull 4";
        tooltip.Pull = "pull 4";        // same value: no second notification
        tooltip.Pull = null;

        Assert.Equal(["Pull", "Pull"], raised);
    }
}

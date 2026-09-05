using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Model;

/// <summary>
/// The role classification. Three of the four rules are read out of MDT's data and are pinned
/// here so a schema change cannot quietly drop them; the fourth — miniboss — is invented, and
/// what is pinned about it is that it stays narrow.
/// </summary>
public class MobRoleTests
{
    private const double Bar = 5_000_000;

    private static Enemy Mob(
        int index = 1, int count = 5, long health = 1_000_000, bool boss = false,
        params Spell[] spells) => new()
    {
        Index = index, Name = $"mob {index}", Id = 1000 + index,
        Count = count, Health = health, IsBoss = boss, Spells = spells,
    };

    private static Spell Kickable => new() { Id = 1, Interruptible = true };

    // ---- the three rules that are in the data --------------------------------------------

    [Fact]
    public void MDTs_own_boss_flag_wins_over_everything_else()
    {
        var boss = Mob(count: 0, health: long.MaxValue, boss: true, spells: Kickable);
        Assert.Equal(MobRole.Boss, MobRoles.Classify(boss, Bar));
    }

    [Fact]
    public void One_interruptible_spell_makes_a_caster()
        => Assert.Equal(MobRole.Caster, MobRoles.Classify(
            Mob(spells: [new Spell { Id = 1 }, Kickable]), Bar));

    [Fact]
    public void A_spell_book_with_nothing_interruptible_in_it_is_melee()
        => Assert.Equal(MobRole.Melee, MobRoles.Classify(
            Mob(spells: [new Spell { Id = 1, Poison = true }, new Spell { Id = 2, Enrage = true }]), Bar));

    [Fact]
    public void No_spells_at_all_is_melee()
        => Assert.Equal(MobRole.Melee, MobRoles.Classify(Mob(), Bar));

    // ---- the invented rule ---------------------------------------------------------------

    [Fact]
    public void Zero_forces_and_far_above_the_trash_median_is_a_miniboss()
        => Assert.Equal(MobRole.Miniboss, MobRoles.Classify(Mob(count: 0, health: 200_000_000), Bar));

    /// <summary>
    /// The guard that keeps the rule narrow. 115 non-boss enemies in the shipped data are worth
    /// zero forces — Hatchlings and the like — and only nine clear the health bar. Dropping the
    /// health half would promote all 115.
    /// </summary>
    [Fact]
    public void Zero_forces_alone_is_not_enough()
        => Assert.Equal(MobRole.Melee, MobRoles.Classify(Mob(count: 0, health: 500_000), Bar));

    /// <summary>And dropping the forces half would promote every large piece of ordinary trash.</summary>
    [Fact]
    public void Enormous_health_alone_is_not_enough()
        => Assert.Equal(MobRole.Melee, MobRoles.Classify(Mob(count: 8, health: 900_000_000), Bar));

    [Fact]
    public void Miniboss_outranks_caster_but_the_spell_book_still_says_it_kicks()
    {
        var mob = Mob(count: 0, health: 200_000_000, spells: Kickable);

        Assert.Equal(MobRole.Miniboss, MobRoles.Classify(mob, Bar));
        // The role is one value, so the caster-ness has to survive somewhere else — it does,
        // which is what lets a badge say "and it casts" without a fifth role.
        Assert.True(mob.HasInterruptibleSpell);
    }

    /// <summary>The escape hatch, for deciding whether the heuristic is earning its place at all.</summary>
    [Fact]
    public void An_infinite_bar_turns_the_heuristic_off()
        => Assert.Equal(MobRole.Melee, MobRoles.Classify(
            Mob(count: 0, health: long.MaxValue), double.PositiveInfinity));

    // ---- the derived threshold -----------------------------------------------------------

    [Fact]
    public void The_bar_is_the_trash_median_times_the_multiple()
    {
        var index = MobRoleIndex.Build([
            Mob(1, health: 1_000_000), Mob(2, health: 2_000_000), Mob(3, health: 3_000_000)]);

        Assert.Equal(2_000_000, index.TrashMedianHealth);
        Assert.Equal(2_000_000 * MobRoles.MinibossHealthMultiple, index.MinibossHealth);
    }

    [Fact]
    public void An_even_number_of_mobs_takes_the_mean_of_the_two_middle_ones()
    {
        var index = MobRoleIndex.Build([
            Mob(1, health: 10), Mob(2, health: 20), Mob(3, health: 30), Mob(4, health: 100)]);

        Assert.Equal(25, index.TrashMedianHealth);
    }

    /// <summary>Bosses are the outliers, so including them would drag the trash bar up.</summary>
    [Fact]
    public void Bosses_are_left_out_of_the_median()
    {
        var index = MobRoleIndex.Build([
            Mob(1, health: 100), Mob(2, health: 200), Mob(3, health: 999_999_999, boss: true)]);

        Assert.Equal(150, index.TrashMedianHealth);
    }

    /// <summary>
    /// A bar of zero would make every zero-forces mob a miniboss, which is the loudest possible
    /// way for an empty set to go wrong.
    /// </summary>
    [Fact]
    public void A_set_with_no_trash_in_it_produces_no_minibosses_rather_than_a_bar_of_zero()
    {
        var index = MobRoleIndex.Build([Mob(1, boss: true)]);

        Assert.Equal(double.PositiveInfinity, index.MinibossHealth);
        Assert.Equal(MobRole.Melee, index.Role(Mob(2, count: 0, health: long.MaxValue)));
    }

    [Fact]
    public void The_tally_counts_every_role_including_the_empty_ones()
    {
        var index = MobRoleIndex.Build([Mob(1, health: 1_000_000)]);
        var tally = index.Tally([Mob(1), Mob(2, spells: Kickable), Mob(3, boss: true)]);

        Assert.Equal(1, tally[MobRole.Melee]);
        Assert.Equal(1, tally[MobRole.Caster]);
        Assert.Equal(1, tally[MobRole.Boss]);
        Assert.Equal(0, tally[MobRole.Miniboss]);
    }
}

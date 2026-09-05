using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The colour rule. Whether the four roles are actually <i>distinguishable</i> is a question for
/// eyes on a map; whether the right one is picked is a question for here.
/// </summary>
public class MapPaletteTests
{
    private static Enemy Mob(int forces = 5, bool stealth = false, params Spell[] spells) => new()
    {
        Index = 1, Name = "mob", Id = 1, Count = forces, Health = 1_000_000,
        Stealth = stealth, Spells = spells,
    };

    /// <summary>
    /// The coexistence rule in one assertion: in a pull it wears the pull's colour, out of one
    /// it wears its role's. MDT does exactly this, and dropping either half was the thing the
    /// milestone explicitly refused to do.
    /// </summary>
    [Fact]
    public void A_mob_in_a_pull_wears_the_pull_colour_and_a_mob_in_none_wears_its_role_colour()
    {
        Assert.Equal("ff8800", MapPalette.For(MobRole.Caster, "ff8800", forces: 5));
        Assert.Equal(MapPalette.Caster, MapPalette.For(MobRole.Caster, null, forces: 5));
    }

    /// <summary>Even a boss defers to its pull's colour — MDT tints every assigned blip.</summary>
    [Fact]
    public void The_pull_colour_wins_over_every_role()
    {
        foreach (var role in Enum.GetValues<MobRole>())
            Assert.Equal("123456", MapPalette.For(role, "123456", forces: 0));
    }

    [Fact]
    public void Trash_worth_no_forces_is_desaturated_rather_than_coloured()
        => Assert.Equal(MapPalette.NoForces, MapPalette.For(MobRole.Melee, null, forces: 0));

    /// <summary>
    /// A boss is worth nothing by design, so "worth nothing" says nothing about it — greying one
    /// out would hide the most important blip on the map.
    /// </summary>
    [Theory]
    [InlineData(MobRole.Boss)]
    [InlineData(MobRole.Miniboss)]
    public void A_boss_or_miniboss_keeps_its_colour_despite_being_worth_nothing(MobRole role)
        => Assert.Equal(MapPalette.For(role), MapPalette.For(role, null, forces: 0));

    [Fact]
    public void The_four_roles_are_four_different_colours()
    {
        var colours = Enum.GetValues<MobRole>().Select(MapPalette.For).ToList();
        Assert.Equal(colours.Count, colours.Distinct().Count());
    }

    [Fact]
    public void Every_palette_entry_is_a_parseable_six_digit_hex()
    {
        foreach (var role in Enum.GetValues<MobRole>())
            Assert.NotNull(RouteOverlay.ParseColor(MapPalette.For(role)));

        Assert.NotNull(RouteOverlay.ParseColor(MapPalette.NoForces));
    }

    /// <summary>
    /// ⚠ Never MDT's own pull sentinel. A role colour that happened to be <c>228b22</c> would be
    /// indistinguishable from "in a pull the author never coloured", which is the one confusion
    /// the two-channel scheme cannot survive.
    /// </summary>
    [Fact]
    public void No_role_colour_collides_with_MDTs_default_pull_colour()
    {
        foreach (var role in Enum.GetValues<MobRole>())
            Assert.NotEqual(MdtDesktop.Core.Routes.Pull.DefaultColor, MapPalette.For(role));
    }

    // ---- badges ---------------------------------------------------------------------------

    /// <summary>Badges, not fill: a mob can carry several and they are orthogonal to its role.</summary>
    [Fact]
    public void A_mob_with_several_flags_wears_several_badges()
    {
        var mob = Mob(spells: [
            new Spell { Id = 1, Interruptible = true, Poison = true },
            new Spell { Id = 2, Enrage = true },
            new Spell { Id = 3, Magic = true }]);

        Assert.Equal("EMP", MapPalette.Badges(mob));
    }

    [Fact]
    public void Stealth_rides_as_a_badge_too_even_though_it_is_not_a_spell_flag()
        => Assert.Equal("s", MapPalette.Badges(Mob(stealth: true)));

    [Fact]
    public void A_plain_mob_wears_no_badges()
        => Assert.Equal("", MapPalette.Badges(Mob()));

    /// <summary>
    /// Interruptible is deliberately not a badge: it is the caster role, and saying it twice
    /// spends a badge slot on something the colour already carries.
    /// </summary>
    [Fact]
    public void Interruptible_is_the_role_rather_than_a_badge()
        => Assert.Equal("", MapPalette.Badges(Mob(spells: new Spell { Id = 1, Interruptible = true })));
}

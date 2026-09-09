using MdtDesktop.Core.Data;
using MdtDesktop.Core.Map;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Tests.Map;

/// <summary>
/// The tactical ring — what the mob makes you <i>do</i> about it.
/// </summary>
/// <remarks>
/// It exists because fill is spent: under a route a blip wears its pull's colour, so role colour
/// is gone exactly when the map is most in use. Whether the ring colours <i>separate</i> on a
/// screen is a question for eyes on a map; whether the right one is picked, and whether the
/// channel stays sparse enough to mean anything, is a question for here.
/// </remarks>
public class RingCueTests
{
    private static Enemy Mob(string[]? characteristics = null, params Spell[] spells) => new()
    {
        Index = 1, Name = "mob", Id = 1, Count = 5, Health = 1_000_000,
        Spells = spells, Characteristics = characteristics ?? [],
    };

    private static Spell Kickable => new() { Id = 1, Interruptible = true };
    private static Spell Enraging => new() { Id = 2, Enrage = true };
    private static Spell Plain => new() { Id = 3, Poison = true };

    // ---- the rules --------------------------------------------------------------------------

    [Fact]
    public void A_mob_with_nothing_to_do_about_it_wears_no_ring()
        => Assert.Null(MapPalette.Ring(Mob(spells: Plain)));

    [Fact]
    public void An_interruptible_cast_earns_the_interrupt_ring()
    {
        var cue = MapPalette.Ring(Mob(spells: Kickable));
        Assert.Equal(MapPalette.RingInterrupt, cue!.Color);
        Assert.False(cue.Dashed);
        Assert.Equal("interrupt", cue.Reason);
    }

    [Fact]
    public void An_enrage_with_no_kickable_cast_earns_the_enrage_ring()
        => Assert.Equal(MapPalette.RingEnrage, MapPalette.Ring(Mob(spells: Enraging))!.Color);

    [Fact]
    public void A_characteristic_other_than_Taunt_earns_the_crowd_control_ring()
        => Assert.Equal(MapPalette.RingCrowdControl,
            MapPalette.Ring(Mob(["Stun", "Fear"]))!.Color);

    /// <summary>
    /// ⚠ Excluded deliberately. Taunt sits on 79 enemies and only 16 of them are bosses, so it is
    /// not a boss proxy — but it is not a crowd control that changes how a pull is planned either.
    /// It stays in the tooltip's CC row and out of the ring.
    /// </summary>
    [Fact]
    public void Taunt_alone_earns_no_ring()
        => Assert.Null(MapPalette.Ring(Mob(["Taunt"])));

    [Fact]
    public void Taunt_beside_a_real_crowd_control_still_earns_the_ring()
        => Assert.Equal(MapPalette.RingCrowdControl, MapPalette.Ring(Mob(["Taunt", "Root"]))!.Color);

    // ---- precedence -------------------------------------------------------------------------

    /// <summary>Interrupt → enrage → CC: the order of how mandatory and how time-critical it is.</summary>
    [Fact]
    public void Interrupt_wins_over_both_of_the_others()
    {
        var cue = MapPalette.Ring(Mob(["Stun"], Kickable, Enraging));
        Assert.Equal(MapPalette.RingInterrupt, cue!.Color);
        Assert.Equal("interrupt + enrage + crowd control", cue.Reason);
    }

    [Fact]
    public void Enrage_wins_over_crowd_control()
        => Assert.Equal(MapPalette.RingEnrage, MapPalette.Ring(Mob(["Stun"], Enraging))!.Color);

    /// <summary>
    /// ⚠ Precedence alone would hide the second axis outright. Dashing the winning colour is
    /// honest about there being more, and the tooltip carries the full picture.
    /// </summary>
    [Fact]
    public void A_mob_carrying_two_axes_gets_a_dashed_ring_in_the_winning_colour()
    {
        var cue = MapPalette.Ring(Mob(["Stun"], Kickable));

        Assert.Equal(MapPalette.RingInterrupt, cue!.Color);
        Assert.True(cue.Dashed);
        Assert.Equal("interrupt + crowd control", cue.Reason);
    }

    [Fact]
    public void A_mob_carrying_one_axis_is_not_dashed()
        => Assert.False(MapPalette.Ring(Mob(spells: Kickable))!.Dashed);

    // ---- the census -------------------------------------------------------------------------

    /// <summary>
    /// ⚠ The number that keeps the channel readable: <b>most mobs wear no ring</b>. A ring on
    /// everything is a ring on nothing.
    /// </summary>
    /// <remarks>
    /// Asserted against the fixture, whose three enemies are shaped to carry the cases — one mob
    /// on all three axes at once, and two on none. The real split across MDT's 16 dungeons is a
    /// property of MDT's data rather than of this code, so it is printed by <c>mdtdesk roles</c>
    /// (295 no ring · 111 interrupt · 31 enrage · 49 CC · 24 dashed, on 6.2.15) and argued with
    /// from a terminal, not pinned to a release here.
    /// </remarks>
    [Fact]
    public async Task The_fixture_census_is_one_ring_on_three_mobs()
    {
        using var fixture = new Tests.Data.MdtFixture();
        var data = await new DungeonExtractor().ExtractAsync(fixture.AddonDirectory);

        var cues = data.Dungeons.SelectMany(d => d.Enemies)
            .Select(e => (e.Name, Cue: MapPalette.Ring(e)))
            .ToList();

        Assert.Equal(3, cues.Count);
        Assert.Equal(2, cues.Count(c => c.Cue is null));

        // Sparse Mob carries an interruptible cast, an enrage AND a non-Taunt characteristic.
        var ringed = Assert.Single(cues, c => c.Cue is not null);
        Assert.Equal("Sparse Mob", ringed.Name);
        Assert.Equal(MapPalette.RingInterrupt, ringed.Cue!.Color);
        Assert.True(ringed.Cue.Dashed);
        Assert.Equal("interrupt + enrage + crowd control", ringed.Cue.Reason);
    }
}

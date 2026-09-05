using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Tests.Routes;

/// <summary>
/// The entire behaviour behind the hotkey. Nobody can press F2 on this machine, so what F2 does
/// is tested here instead and <c>App</c> is left with nothing to get wrong but the p/invoke.
/// </summary>
public class PullCursorTests
{
    [Fact]
    public void A_new_cursor_sits_on_the_first_pull()
        => Assert.Equal(1, new PullCursor(18).Current);

    [Fact]
    public void Next_and_previous_walk_the_route()
    {
        var cursor = new PullCursor(3);

        Assert.True(cursor.Next());
        Assert.Equal(2, cursor.Current);
        Assert.True(cursor.Previous());
        Assert.Equal(1, cursor.Current);
    }

    /// <summary>
    /// Clamping, not wrapping. Jumping from pull 18 back to pull 1 on a keypress you cannot see
    /// reads as the app having lost your place; stopping reads as the end of the route.
    /// </summary>
    [Fact]
    public void It_stops_at_both_ends_rather_than_wrapping()
    {
        var cursor = new PullCursor(2);

        Assert.False(cursor.Previous());
        Assert.Equal(1, cursor.Current);

        cursor.Next();
        Assert.False(cursor.Next());
        Assert.Equal(2, cursor.Current);
    }

    [Fact]
    public void A_move_that_changes_nothing_reports_that_it_changed_nothing()
    {
        // The return value is what tells the caller whether to repaint 156 blips.
        var cursor = new PullCursor(1);
        Assert.False(cursor.Next());
        Assert.False(cursor.MoveTo(1));
    }

    [Fact]
    public void Wrapping_is_available_for_anyone_who_wants_it()
    {
        var cursor = new PullCursor(3, wrap: true);

        Assert.True(cursor.Previous());
        Assert.Equal(3, cursor.Current);
        Assert.True(cursor.Next());
        Assert.Equal(1, cursor.Current);
    }

    [Fact]
    public void With_no_route_loaded_nothing_moves_and_nothing_throws()
    {
        var cursor = new PullCursor(0);

        Assert.Equal(0, cursor.Current);
        Assert.False(cursor.Next());
        Assert.False(cursor.Previous());
        Assert.False(cursor.MoveTo(1));
    }

    [Fact]
    public void A_single_pull_route_is_both_first_and_last()
    {
        var cursor = new PullCursor(1);
        Assert.True(cursor.AtFirst);
        Assert.True(cursor.AtLast);
    }

    /// <summary>Clicking a pull that is not there is a bug, so it is refused rather than clamped.</summary>
    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(19)]
    public void MoveTo_refuses_a_pull_that_does_not_exist(int pull)
    {
        var cursor = new PullCursor(18);
        Assert.False(cursor.MoveTo(pull));
        Assert.Equal(1, cursor.Current);
    }

    [Fact]
    public void Loading_a_shorter_route_does_not_leave_the_cursor_past_its_end()
    {
        var cursor = new PullCursor(18);
        cursor.MoveTo(17);

        cursor.Reset(3);
        Assert.Equal(1, cursor.Current);

        cursor.Reset(3, startAt: 99);
        Assert.Equal(3, cursor.Current);
    }

    [Fact]
    public void Resetting_to_no_route_leaves_no_current_pull()
    {
        var cursor = new PullCursor(18);
        cursor.Reset(0);
        Assert.Equal(0, cursor.Current);
    }
}

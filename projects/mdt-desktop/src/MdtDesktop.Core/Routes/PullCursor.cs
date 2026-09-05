namespace MdtDesktop.Core.Routes;

/// <summary>
/// Which pull you are on. The whole behaviour behind the hotkey, in <c>Core</c> where it can be
/// tested — <c>App</c> calls <see cref="Next"/> or <see cref="Previous"/> and repaints.
/// </summary>
/// <remarks>
/// <para>
/// MDT's own <c>currentPull</c> is a manual cursor set by clicking a pull button — there is no
/// combat-log handler and no <c>SCENARIO_CRITERIA_UPDATE</c> subscription anywhere in the addon
/// — so a manual cursor here loses nothing.
/// </para>
/// <para>
/// It <b>clamps rather than wraps</b> by default. Wrapping from the last pull back to the first
/// on a keypress you cannot see — the app is on the other monitor, you are in combat — reads as
/// the app having lost your place. Stopping at the end reads as the end.
/// </para>
/// </remarks>
public sealed class PullCursor(int pullCount, bool wrap = false)
{
    /// <summary>How many pulls the route has. Zero for no route.</summary>
    public int PullCount { get; private set; } = Math.Max(0, pullCount);

    public bool Wrap { get; init; } = wrap;

    /// <summary>The pull, 1-based. Zero when there is no route to be on a pull of.</summary>
    public int Current { get; private set; } = pullCount > 0 ? 1 : 0;

    public bool AtFirst => PullCount == 0 || Current <= 1;
    public bool AtLast => PullCount == 0 || Current >= PullCount;

    /// <returns>True when the cursor actually moved.</returns>
    public bool Next() => Step(+1);

    /// <returns>True when the cursor actually moved.</returns>
    public bool Previous() => Step(-1);

    /// <summary>Jumps to a pull. Out-of-range is refused rather than clamped — a click on a pull
    /// that is not there is a bug, not a nudge.</summary>
    public bool MoveTo(int pullNumber)
    {
        if (pullNumber < 1 || pullNumber > PullCount || pullNumber == Current) return false;
        Current = pullNumber;
        return true;
    }

    /// <summary>Points the cursor at a different route.</summary>
    public void Reset(int newPullCount, int startAt = 1)
    {
        PullCount = Math.Max(0, newPullCount);
        Current = PullCount == 0 ? 0 : Math.Clamp(startAt, 1, PullCount);
    }

    private bool Step(int delta)
    {
        if (PullCount == 0) return false;

        var next = Current + delta;

        if (next < 1) next = Wrap ? PullCount : 1;
        else if (next > PullCount) next = Wrap ? 1 : PullCount;

        if (next == Current) return false;
        Current = next;
        return true;
    }
}

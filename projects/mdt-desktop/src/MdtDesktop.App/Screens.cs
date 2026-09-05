using System.Runtime.InteropServices;

namespace MdtDesktop.App;

/// <summary>
/// The monitors attached right now, in pixels, primary first.
/// </summary>
/// <remarks>
/// <para>
/// Read through Win32 rather than <c>System.Windows.Forms.Screen</c> so the project stays
/// WPF-only — pulling in WinForms for one enumeration would double the framework surface for
/// nothing.
/// </para>
/// <para>
/// ⚠ It returns the <b>working area</b>, not the full monitor bounds, so a restored window is
/// not put under the taskbar. And an empty list means "could not ask", which
/// <c>WindowPlacement.ClampToVisible</c> reads as "leave the placement alone" rather than as
/// "there are no monitors".
/// </para>
/// </remarks>
internal static class Screens
{
    public static IReadOnlyList<MonitorArea> Enumerate()
    {
        var found = new List<(MonitorArea Area, bool Primary)>();

        var ok = EnumDisplayMonitors(IntPtr.Zero, IntPtr.Zero, Callback, IntPtr.Zero);
        if (!ok || found.Count == 0) return [];

        // Primary first, because ClampToVisible falls back to screens[0] when the remembered
        // monitor is gone — and the primary is the one that is certainly there.
        return [.. found.OrderByDescending(f => f.Primary).Select(f => f.Area)];

        bool Callback(IntPtr monitor, IntPtr _, IntPtr __, IntPtr ___)
        {
            var info = new MonitorInfo { cbSize = Marshal.SizeOf<MonitorInfo>() };
            if (GetMonitorInfo(monitor, ref info))
                found.Add((
                    new MonitorArea(
                        info.rcWork.left, info.rcWork.top, info.rcWork.right, info.rcWork.bottom),
                    (info.dwFlags & MonitorPrimary) != 0));

            return true;
        }
    }

    private const int MonitorPrimary = 0x1;

    private delegate bool MonitorEnumProc(IntPtr monitor, IntPtr dc, IntPtr rect, IntPtr data);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool EnumDisplayMonitors(
        IntPtr hdc, IntPtr clip, MonitorEnumProc callback, IntPtr data);

    [DllImport("user32.dll", CharSet = CharSet.Unicode, EntryPoint = "GetMonitorInfoW")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GetMonitorInfo(IntPtr monitor, ref MonitorInfo info);

    [StructLayout(LayoutKind.Sequential)]
    private struct Rect
    {
        public int left, top, right, bottom;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct MonitorInfo
    {
        public int cbSize;
        public Rect rcMonitor;
        public Rect rcWork;
        public int dwFlags;
    }
}

/// <summary>A monitor's working area in physical pixels, as edges rather than a size.</summary>
internal readonly record struct MonitorArea(double Left, double Top, double Right, double Bottom);

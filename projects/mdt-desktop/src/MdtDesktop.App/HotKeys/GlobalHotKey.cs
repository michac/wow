using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;
using MdtDesktop.Core.Input;

namespace MdtDesktop.App.HotKeys;

/// <summary>
/// System-wide hotkeys, so the pull advances while WoW has focus.
/// </summary>
/// <remarks>
/// <para>
/// ⚠ <c>RegisterHotKey</c> means the <b>OS consumes the key and WoW never sees it</b>. That is
/// the whole feature — no alt-tab — and equally the whole cost: whatever is bound here stops
/// working in game for as long as the app runs. F2 is WoW's own default
/// <c>TARGETPARTYMEMBER2</c>, which is why the binding is a setting rather than a constant.
/// </para>
/// <para>
/// ⚠ Registration needs the window <b>handle</b>, which does not exist until
/// <c>OnSourceInitialized</c> — not <c>Loaded</c>, and certainly not the constructor. It must
/// also happen on the thread that owns the window, because that is the thread <c>WM_HOTKEY</c>
/// is posted to.
/// </para>
/// <para>
/// This class holds no policy: <see cref="HotKeySpec"/> parses, <c>PullCursor</c> decides what a
/// press means, and this turns a message into an event.
/// </para>
/// </remarks>
internal sealed class GlobalHotKey : IDisposable
{
    private const int WmHotKey = 0x0312;

    private readonly HwndSource _source;
    private readonly IntPtr _handle;
    private readonly List<int> _registered = [];
    private bool _disposed;

    /// <summary>
    /// Hooks the window's message loop. Call from <c>OnSourceInitialized</c>.
    /// </summary>
    /// <exception cref="InvalidOperationException">The window has no handle yet.</exception>
    public GlobalHotKey(Window window)
    {
        _source = (HwndSource?)PresentationSource.FromVisual(window)
                  ?? throw new InvalidOperationException(
                      "The window has no HWND yet — register hotkeys from OnSourceInitialized.");

        _handle = _source.Handle;
        _source.AddHook(WndProc);
    }

    /// <summary>Raised with the id passed to <see cref="TryRegister"/>.</summary>
    public event EventHandler<int>? Pressed;

    /// <summary>
    /// Registers one hotkey.
    /// </summary>
    /// <param name="error">Why it failed, in words fit for a status bar.</param>
    /// <returns>False when the OS refused it.</returns>
    /// <remarks>
    /// ⚠ The return value is the point. <c>RegisterHotKey</c> fails when another process already
    /// owns the combination (<c>ERROR_HOTKEY_ALREADY_REGISTERED</c>, 1409) and that is the single
    /// most likely way this feature dies — quietly, with the app looking fine and the key doing
    /// nothing. It must reach the user, so it is returned rather than swallowed.
    /// </remarks>
    public bool TryRegister(int id, HotKeySpec spec, out string? error)
    {
        ObjectDisposedException.ThrowIf(_disposed, this);

        // Re-registering over a live id fails, so always give up the old one first.
        Unregister(id);

        if (RegisterHotKey(_handle, id, spec.RegisterHotKeyModifiers, spec.VirtualKey))
        {
            _registered.Add(id);
            error = null;
            return true;
        }

        var code = Marshal.GetLastWin32Error();
        error = code == 1409
            ? $"{spec} is already registered by another application — that pull hotkey is off."
            : $"Windows refused the hotkey {spec} (error {code}).";
        return false;
    }

    public void Unregister(int id)
    {
        if (_registered.Remove(id)) UnregisterHotKey(_handle, id);
    }

    /// <summary>
    /// Gives every registration back.
    /// </summary>
    /// <remarks>
    /// ⚠ A leaked registration lives until the process exits and blocks the same combination on
    /// the next launch — so the app would refuse its own hotkey after one unclean shutdown.
    /// </remarks>
    public void UnregisterAll()
    {
        foreach (var id in _registered) UnregisterHotKey(_handle, id);
        _registered.Clear();
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;

        UnregisterAll();
        _source.RemoveHook(WndProc);
    }

    private IntPtr WndProc(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam, ref bool handled)
    {
        if (msg != WmHotKey) return IntPtr.Zero;

        var id = wParam.ToInt32();
        if (!_registered.Contains(id)) return IntPtr.Zero;

        Pressed?.Invoke(this, id);
        handled = true;
        return IntPtr.Zero;
    }

    // DllImport rather than the source-generated LibraryImport: the generator requires
    // AllowUnsafeBlocks across the whole project, and these two take only blittable arguments,
    // so there is nothing for it to generate that is worth that.
    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);
}

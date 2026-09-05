namespace MdtDesktop.Core.Input;

/// <summary>
/// Win32's <c>MOD_*</c> values, so a parsed hotkey can be handed to <c>RegisterHotKey</c> with
/// no translation on the way.
/// </summary>
/// <remarks>
/// That is the point of putting these in <c>Core</c>: the WPF side stays a p/invoke and a cast,
/// and every question with a right answer — which key is F2, does "Ctrl" mean Control — is
/// settled here, where a test can ask it.
/// </remarks>
[Flags]
public enum HotKeyModifiers
{
    None = 0,
    Alt = 0x0001,
    Control = 0x0002,
    Shift = 0x0004,
    Windows = 0x0008,

    /// <summary>
    /// ⚠ Not optional in practice. Without it, holding the key auto-repeats and walks the whole
    /// route in a second — with the app on another monitor, invisibly.
    /// </summary>
    NoRepeat = 0x4000,
}

/// <summary>
/// A parsed global hotkey — <c>"F2"</c>, <c>"Shift+F2"</c>, <c>"Ctrl+Alt+Numpad3"</c>.
/// </summary>
/// <remarks>
/// ⚠ <c>RegisterHotKey</c> means the OS consumes the key and <b>WoW never sees it</b>. That is
/// the feature — no alt-tab — and also the cost: the default must be a key you have not bound in
/// game. F2 is WoW's own <c>TARGETPARTYMEMBER2</c> by default, so anyone who uses party frames
/// should rebind one side or the other; that is why this is configurable rather than a constant.
/// </remarks>
public sealed record HotKeySpec(HotKeyModifiers Modifiers, uint VirtualKey)
{
    /// <summary>The modifiers as <c>RegisterHotKey</c> wants them, with <c>MOD_NOREPEAT</c> set.</summary>
    public uint RegisterHotKeyModifiers => (uint)(Modifiers | HotKeyModifiers.NoRepeat);

    /// <summary>
    /// Parses <c>"Shift+F2"</c> and friends. Case-insensitive, tolerant of spaces.
    /// </summary>
    /// <remarks>
    /// A modifier on its own is refused: <c>RegisterHotKey</c> with no virtual key registers
    /// nothing useful and reports success, which would be a hotkey that silently never fires.
    /// </remarks>
    public static bool TryParse(string? text, out HotKeySpec spec)
    {
        spec = default!;
        if (string.IsNullOrWhiteSpace(text)) return false;

        var modifiers = HotKeyModifiers.None;
        uint? key = null;

        foreach (var raw in text.Split('+', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
        {
            var part = raw.ToUpperInvariant();
            switch (part)
            {
                case "CTRL" or "CONTROL": modifiers |= HotKeyModifiers.Control; continue;
                case "SHIFT": modifiers |= HotKeyModifiers.Shift; continue;
                case "ALT": modifiers |= HotKeyModifiers.Alt; continue;
                case "WIN" or "WINDOWS": modifiers |= HotKeyModifiers.Windows; continue;
            }

            // Two keys is a typo, not a chord — RegisterHotKey takes exactly one.
            if (key is not null) return false;
            if (VirtualKeys.TryGetValue(part, out var vk)) key = vk;
            else return false;
        }

        if (key is null) return false;

        spec = new HotKeySpec(modifiers, key.Value);
        return true;
    }

    /// <summary>Canonical text, in the order <see cref="TryParse"/> reads back unchanged.</summary>
    public override string ToString()
    {
        var parts = new List<string>(4);
        if (Modifiers.HasFlag(HotKeyModifiers.Control)) parts.Add("Ctrl");
        if (Modifiers.HasFlag(HotKeyModifiers.Shift)) parts.Add("Shift");
        if (Modifiers.HasFlag(HotKeyModifiers.Alt)) parts.Add("Alt");
        if (Modifiers.HasFlag(HotKeyModifiers.Windows)) parts.Add("Win");

        parts.Add(KeyNames.GetValueOrDefault(VirtualKey, $"0x{VirtualKey:X2}"));
        return string.Join("+", parts);
    }

    /// <summary>
    /// The keys worth binding to a pull cursor, by name. Function keys, letters, digits, the
    /// numpad, and the navigation cluster.
    /// </summary>
    private static readonly Dictionary<string, uint> VirtualKeys = Build();

    private static readonly Dictionary<uint, string> KeyNames =
        VirtualKeys.GroupBy(kv => kv.Value).ToDictionary(g => g.Key, g => g.First().Key);

    private static Dictionary<string, uint> Build()
    {
        var keys = new Dictionary<string, uint>(StringComparer.OrdinalIgnoreCase);

        // VK_F1 is 0x70, so F2 is 0x71 — the value README's hotkey note names.
        for (uint i = 1; i <= 24; i++) keys[$"F{i}"] = 0x70 + i - 1;

        // Letters and digits are their own ASCII codes, which is the whole of the VK table here.
        for (var c = 'A'; c <= 'Z'; c++) keys[c.ToString()] = c;
        for (var c = '0'; c <= '9'; c++) keys[c.ToString()] = c;

        for (uint i = 0; i <= 9; i++) keys[$"NUMPAD{i}"] = 0x60 + i;

        keys["INSERT"] = 0x2D;
        keys["DELETE"] = 0x2E;
        keys["HOME"] = 0x24;
        keys["END"] = 0x23;
        keys["PAGEUP"] = 0x21;
        keys["PAGEDOWN"] = 0x22;
        keys["LEFT"] = 0x25;
        keys["UP"] = 0x26;
        keys["RIGHT"] = 0x27;
        keys["DOWN"] = 0x28;
        keys["SPACE"] = 0x20;
        keys["TAB"] = 0x09;
        keys["OEM3"] = 0xC0;      // the ` / ~ key, a common "unbound in game" choice

        return keys;
    }
}

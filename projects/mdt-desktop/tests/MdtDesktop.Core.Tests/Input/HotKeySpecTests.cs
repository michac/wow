using MdtDesktop.Core.Input;

namespace MdtDesktop.Core.Tests.Input;

/// <summary>
/// The hotkey, parsed. Whether <c>RegisterHotKey</c> actually fires cannot be tested from here —
/// but whether "Shift+F2" means <c>MOD_SHIFT</c> and <c>0x71</c> can, and that is the half that
/// would otherwise be wrong silently on the far side of a p/invoke.
/// </summary>
public class HotKeySpecTests
{
    private static HotKeySpec Parse(string text)
    {
        Assert.True(HotKeySpec.TryParse(text, out var spec), $"'{text}' did not parse");
        return spec;
    }

    /// <summary>README names these two exactly: F2 is 0x71, Shift is MOD_SHIFT.</summary>
    [Fact]
    public void The_default_bindings_parse_to_the_Win32_values_README_names()
    {
        Assert.Equal(new HotKeySpec(HotKeyModifiers.None, 0x71), Parse("F2"));
        Assert.Equal(new HotKeySpec(HotKeyModifiers.Shift, 0x71), Parse("Shift+F2"));
    }

    [Theory]
    [InlineData("F1", 0x70)]
    [InlineData("F12", 0x7B)]
    [InlineData("F24", 0x87)]
    [InlineData("A", 0x41)]
    [InlineData("7", 0x37)]
    [InlineData("Numpad3", 0x63)]
    [InlineData("PageDown", 0x22)]
    public void Named_keys_map_to_their_virtual_key_codes(string text, uint vk)
        => Assert.Equal(vk, Parse(text).VirtualKey);

    [Fact]
    public void Modifiers_combine_and_both_spellings_of_Control_work()
    {
        var expected = HotKeyModifiers.Control | HotKeyModifiers.Alt | HotKeyModifiers.Shift;
        Assert.Equal(expected, Parse("Ctrl+Alt+Shift+F2").Modifiers);
        Assert.Equal(expected, Parse("control+alt+shift+f2").Modifiers);
    }

    [Fact]
    public void Spaces_around_the_plus_signs_are_tolerated()
        => Assert.Equal(Parse("Ctrl+F2"), Parse(" ctrl + f2 "));

    [Fact]
    public void The_canonical_text_round_trips()
    {
        foreach (var text in new[] { "F2", "Shift+F2", "Ctrl+Shift+Alt+Win+Numpad3", "A" })
            Assert.Equal(text, Parse(text).ToString(), ignoreCase: true);
    }

    /// <summary>
    /// ⚠ Without <c>MOD_NOREPEAT</c> a held key auto-repeats and walks the whole route in a
    /// second, on a monitor you are not looking at. It is set unconditionally for that reason.
    /// </summary>
    [Fact]
    public void Every_registration_carries_MOD_NOREPEAT()
    {
        Assert.Equal(0x4000u, Parse("F2").RegisterHotKeyModifiers);
        Assert.Equal(0x4004u, Parse("Shift+F2").RegisterHotKeyModifiers);   // NOREPEAT | SHIFT
    }

    /// <summary>
    /// A modifier alone registers something that can never fire, and <c>RegisterHotKey</c> would
    /// report success — a hotkey that is silently dead is worse than one that refuses to be set.
    /// </summary>
    [Theory]
    [InlineData("Shift")]
    [InlineData("Ctrl+Alt")]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    [InlineData("F99")]
    [InlineData("NotAKey")]
    [InlineData("F2+F3")]
    public void Something_that_is_not_a_usable_binding_is_refused(string? text)
        => Assert.False(HotKeySpec.TryParse(text, out _));
}

using System.Formats.Cbor;
using System.IO.Compression;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Tests.Routes;

/// <summary>
/// Decoding is exercised against a real exported route — <c>Fixtures/yoda-easy-route.txt</c>,
/// an 18-pull Altar of Fangs route — plus synthetic strings for the shapes a single real route
/// does not happen to contain.
/// </summary>
/// <remarks>
/// Decoding needs no dungeon data, so all of this is hermetic. Only the forces arithmetic
/// needs a dungeon, and that is covered separately against a fixture dungeon.
/// </remarks>
public class RouteDecoderTests
{
    private static string RealRoute() => File.ReadAllText(
        Path.Combine(AppContext.BaseDirectory, "Routes", "Fixtures", "yoda-easy-route.txt"));

    // ---- the real route -----------------------------------------------------------------

    [Fact]
    public void The_real_route_decodes_to_its_preset_header()
    {
        var route = RouteDecoder.Decode(RealRoute());

        Assert.Equal("Yoda easy route", route.Name);
        Assert.Equal("6lbpOeHxxKG", route.Uid);
        Assert.Equal(164, route.DungeonIndex);      // Altar of Fangs
        Assert.Equal(18, route.Pulls.Count);
        Assert.Equal(1, route.CurrentPull);
        Assert.Equal(1, route.CurrentSubLevel);
    }

    [Fact]
    public void The_real_routes_first_pull_carries_its_enemies_and_colour()
    {
        var pull = RouteDecoder.Decode(RealRoute()).Pulls[0];

        Assert.Equal(1, pull.Number);
        Assert.Equal("ff3eff", pull.Color);
        Assert.True(pull.HasCustomColor);

        // Enemy indices ascending; the clone list stays exactly as exported.
        Assert.Equal([6, 7, 10, 11], pull.Enemies.Select(e => e.EnemyIndex));
        Assert.Equal([6, 5], pull.Enemies[0].CloneIndices);
        Assert.Equal([6, 7, 4, 1, 2, 5, 3], pull.Enemies[1].CloneIndices);
        Assert.Equal([16, 17, 18], pull.Enemies[3].CloneIndices);
    }

    [Fact]
    public void Every_pull_in_the_real_route_has_enemies_and_no_unknown_options()
    {
        var route = RouteDecoder.Decode(RealRoute());

        Assert.All(route.Pulls, p => Assert.NotEmpty(p.Enemies));
        // `color` is the only option key MDT writes.
        Assert.All(route.Pulls, p => Assert.Empty(p.UnknownOptions));
        Assert.All(route.Pulls, p => Assert.Equal(6, p.Color!.Length));
    }

    [Fact]
    public void The_real_route_is_recognised_as_the_modern_format()
        => Assert.Equal(RouteStringFormat.Modern, RouteDecoder.Classify(RealRoute()));

    [Fact]
    public void Leading_and_trailing_whitespace_is_tolerated()
    {
        // Pasted strings pick up newlines.
        var route = RouteDecoder.Decode("\n  " + RealRoute().Trim() + "  \n");
        Assert.Equal(18, route.Pulls.Count);
    }

    // ---- format dispatch ----------------------------------------------------------------

    [Theory]
    [InlineData("!~MDT2~abc", RouteStringFormat.Modern)]
    [InlineData("!abcdef", RouteStringFormat.LegacyDeflate)]
    [InlineData("aBc012XyzaBc012XyzaBc012XyzaBc012Xyz", RouteStringFormat.LegacyCompress)]
    [InlineData("", RouteStringFormat.Empty)]
    public void The_prefix_says_which_vintage_a_string_is(string s, RouteStringFormat expected)
        => Assert.Equal(expected, RouteDecoder.Classify(s));

    /// <summary>
    /// The bare legacy format has no prefix, so "anything else is legacy" is a trap: it tells a
    /// user who pasted a URL that their route is in an obsolete format, which is untrue and
    /// sends them looking in the wrong place.
    /// </summary>
    [Theory]
    [InlineData("https://keystone.guru/practice/1234/altar-of-fangs")]
    [InlineData("abcdef")]                          // print-charset, but far too short
    [InlineData("aBc012XyzaBc012XyzaBc012XyzaBc012Xyz-notprint")]  // long enough, wrong alphabet
    [InlineData("what dungeon is this even")]
    public void Something_that_is_not_a_route_string_is_not_called_a_legacy_one(string s)
    {
        Assert.Equal(RouteStringFormat.NotARouteString, RouteDecoder.Classify(s));

        var ex = Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode(s));
        Assert.DoesNotContain("legacy", ex.Message, StringComparison.OrdinalIgnoreCase);
        Assert.Contains("!~MDT2~", ex.Message, StringComparison.Ordinal);
    }

    [Theory]
    [InlineData("!oldstyle")]
    [InlineData("aBc012XyzaBc012XyzaBc012XyzaBc012Xyz")]
    public void A_legacy_string_is_refused_with_a_reason_rather_than_misparsed(string s)
    {
        var ex = Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode(s));
        Assert.Contains("legacy", ex.Message, StringComparison.OrdinalIgnoreCase);
    }

    /// <summary>The refusal has to name WHICH vintage, or it is no better than "cannot read this".</summary>
    [Fact]
    public void The_refusal_names_the_format_it_is_refusing()
    {
        Assert.Contains("LibDeflate", RouteDecoder.DescribeRefusal(RouteStringFormat.LegacyDeflate));
        Assert.Contains("LibCompress", RouteDecoder.DescribeRefusal(RouteStringFormat.LegacyCompress));
    }

    /// <summary>The paste box and the CLI must not tell the same user different things.</summary>
    [Fact]
    public void The_refusal_wording_is_the_one_the_decoder_throws()
    {
        var ex = Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode("!oldstyle"));
        Assert.Equal(RouteDecoder.DescribeRefusal(RouteStringFormat.LegacyDeflate), ex.Message);
    }

    [Fact]
    public void An_empty_string_is_empty_rather_than_a_broken_route()
    {
        Assert.Equal(RouteStringFormat.Empty, RouteDecoder.Classify("   \n "));
        var ex = Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode("   "));
        Assert.Equal(RouteDecoder.DescribeRefusal(RouteStringFormat.Empty), ex.Message);
    }

    [Fact]
    public void Rubbish_after_the_prefix_fails_as_a_decode_error()
    {
        Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode("!~MDT2~not-base64!!"));
        // Valid base64 that is not deflate.
        Assert.Throws<RouteDecodeException>(() => RouteDecoder.Decode("!~MDT2~AAAAAAAAAAA="));
    }

    // ---- shapes the real route does not contain ------------------------------------------

    [Fact]
    public void A_pull_key_is_an_enemy_index_only_when_it_parses_as_a_positive_integer()
    {
        // MDT discriminates with `tonumber(enemyIdx)`, so a numeric STRING key is an enemy too,
        // while `color` and anything else is an option.
        var route = Decode(w =>
        {
            w.WriteStartMap(1);
            WriteText(w, "value");
            w.WriteStartMap(2);
            WriteText(w, "currentDungeonIdx"); w.WriteInt32(164);
            WriteText(w, "pulls");
            w.WriteStartArray(1);
            w.WriteStartMap(4);
            w.WriteInt32(3); w.WriteStartArray(1); w.WriteInt32(1); w.WriteEndArray();
            WriteText(w, "5"); w.WriteStartArray(1); w.WriteInt32(2); w.WriteEndArray();
            WriteText(w, "color"); WriteText(w, "228b22");
            WriteText(w, "somethingNew"); w.WriteInt32(1);
            w.WriteEndMap();
            w.WriteEndArray();
            w.WriteEndMap();
            w.WriteEndMap();
        });

        var pull = Assert.Single(route.Pulls);
        Assert.Equal([3, 5], pull.Enemies.Select(e => e.EnemyIndex));
        Assert.Equal(["somethingNew"], pull.UnknownOptions);
    }

    [Fact]
    public void The_228b22_colour_is_recognised_as_MDTs_no_custom_colour_sentinel()
    {
        var route = Decode(w => WriteSimpleRoute(w, color: Pull.DefaultColor));
        var pull = Assert.Single(route.Pulls);

        Assert.Equal("228b22", pull.Color);
        Assert.False(pull.HasCustomColor);   // MDT writes it in rather than leaving it unset
    }

    [Fact]
    public void A_pull_with_no_colour_at_all_reports_none()
    {
        var pull = Assert.Single(Decode(w => WriteSimpleRoute(w, color: null)).Pulls);
        Assert.Null(pull.Color);
        Assert.False(pull.HasCustomColor);
    }

    [Fact]
    public void A_clone_list_that_arrives_sparse_is_read_in_key_order()
    {
        // Presets.lua warns a clone array can be sparse after editing, in which case it is a
        // map rather than an array on the wire.
        var route = Decode(w =>
        {
            w.WriteStartMap(1);
            WriteText(w, "value");
            w.WriteStartMap(2);
            WriteText(w, "currentDungeonIdx"); w.WriteInt32(164);
            WriteText(w, "pulls");
            w.WriteStartArray(1);
            w.WriteStartMap(1);
            w.WriteInt32(7);
            w.WriteStartMap(3);
            w.WriteInt32(3); w.WriteInt32(30);
            w.WriteInt32(1); w.WriteInt32(10);
            w.WriteInt32(5); w.WriteInt32(50);
            w.WriteEndMap();
            w.WriteEndMap();
            w.WriteEndArray();
            w.WriteEndMap();
            w.WriteEndMap();
        });

        var enemy = Assert.Single(Assert.Single(route.Pulls).Enemies);
        Assert.Equal(7, enemy.EnemyIndex);
        Assert.Equal([10, 30, 50], enemy.CloneIndices);
    }

    [Fact]
    public void Text_strings_decode_as_well_as_byte_strings()
    {
        // C_EncodingUtil writes Lua strings as CBOR BYTE strings, which is what the real route
        // uses and what the fixture tests above cover. A text string must work too, so a
        // future client change cannot silently break decoding.
        var route = Decode(w =>
        {
            w.WriteStartMap(2);
            w.WriteTextString("text"); w.WriteTextString("Written as text");
            w.WriteTextString("value");
            w.WriteStartMap(2);
            w.WriteTextString("currentDungeonIdx"); w.WriteInt32(164);
            w.WriteTextString("pulls"); w.WriteStartArray(0); w.WriteEndArray();
            w.WriteEndMap();
            w.WriteEndMap();
        });

        Assert.Equal("Written as text", route.Name);
        Assert.Equal(164, route.DungeonIndex);
    }

    [Fact]
    public void A_route_naming_no_dungeon_is_refused()
        => Assert.Throws<RouteDecodeException>(() => Decode(w =>
        {
            w.WriteStartMap(1);
            WriteText(w, "value");
            w.WriteStartMap(1);
            WriteText(w, "pulls"); w.WriteStartArray(0); w.WriteEndArray();
            w.WriteEndMap();
            w.WriteEndMap();
        }));

    // ---- helpers -------------------------------------------------------------------------

    /// <summary>Lua strings cross as CBOR byte strings — see <c>CborTree</c>.</summary>
    private static void WriteText(CborWriter w, string s)
        => w.WriteByteString(System.Text.Encoding.UTF8.GetBytes(s));

    private static void WriteSimpleRoute(CborWriter w, string? color)
    {
        w.WriteStartMap(1);
        WriteText(w, "value");
        w.WriteStartMap(2);
        WriteText(w, "currentDungeonIdx"); w.WriteInt32(164);
        WriteText(w, "pulls");
        w.WriteStartArray(1);
        w.WriteStartMap(color is null ? 1 : 2);
        w.WriteInt32(1); w.WriteStartArray(1); w.WriteInt32(1); w.WriteEndArray();
        if (color is not null) { WriteText(w, "color"); WriteText(w, color); }
        w.WriteEndMap();
        w.WriteEndArray();
        w.WriteEndMap();
        w.WriteEndMap();
    }

    /// <summary>Builds a real <c>!~MDT2~</c> string, so the tests go through the whole pipeline.</summary>
    private static Route Decode(Action<CborWriter> write)
    {
        var writer = new CborWriter();
        write(writer);

        using var buffer = new MemoryStream();
        using (var deflate = new DeflateStream(buffer, CompressionLevel.Optimal, leaveOpen: true))
            deflate.Write(writer.Encode());

        return RouteDecoder.Decode(RouteDecoder.ModernPrefix + Convert.ToBase64String(buffer.ToArray()));
    }
}

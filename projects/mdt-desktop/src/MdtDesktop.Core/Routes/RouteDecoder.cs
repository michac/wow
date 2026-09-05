using System.IO.Compression;

namespace MdtDesktop.Core.Routes;

/// <summary>
/// Turns an MDT route string into a <see cref="Route"/>.
/// </summary>
/// <remarks>
/// MDT has shipped three string vintages and the prefix says which:
/// <list type="bullet">
/// <item><c>!~MDT2~</c> — Base64 → raw Deflate → CBOR. Decoded here.</item>
/// <item><c>!</c> — LibDeflate print-decode → inflate → AceSerializer. <b>Refused by name.</b></item>
/// <item>bare — LibDeflate print-decode → LibCompress → AceSerializer. <b>Refused by name.</b></item>
/// </list>
/// The modern format is built by <c>C_EncodingUtil</c>, a Blizzard <i>client</i> API rather
/// than a vendored library, so the sidecar could not decode it even in principle —
/// <c>C_EncodingUtil</c> does not exist outside the game.
/// <para>
/// The two legacy vintages are out of scope on purpose, not pending: MDT's <c>TableToString</c>
/// has long written only <c>!~MDT2~</c> and keystone.guru exports that too, so no current-season
/// route can be in one. They are still recognised so the refusal can <b>name the format</b>
/// rather than reading as a corrupt string — see <c>README.md</c> § <i>Why the two legacy
/// formats are out of scope</i>.
/// </para>
/// </remarks>
public static class RouteDecoder
{
    public const string ModernPrefix = "!~MDT2~";

    /// <summary>
    /// LibDeflate's print-encoding alphabet — the 64 characters a bare legacy string is built
    /// from (<c>LibDeflate.lua</c>'s <c>_byte_to_6bit_char</c>), plus its <c>(</c>/<c>)</c>
    /// run-length markers.
    /// </summary>
    private const string PrintCharset =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()";

    /// <summary>
    /// Below this many characters a bare string is not a plausible route — the shortest real one
    /// seen is 616. This is a floor against calling a word "a legacy route string", not a limit.
    /// </summary>
    private const int MinimumLegacyLength = 32;

    /// <summary>Which vintage a string is — or that it is not a route string at all.</summary>
    /// <remarks>
    /// ⚠ The bare legacy format has no prefix to test, so "everything else" is <b>not</b> a safe
    /// reading of it: a pasted URL, a keystone.guru page address or a stray word would all come
    /// back as <see cref="RouteStringFormat.LegacyCompress"/> and produce the legacy-format
    /// refusal, which tells the user something untrue about what they pasted. So a bare string
    /// has to look like one — LibDeflate's print alphabet, and long enough to be a route — and
    /// anything else is <see cref="RouteStringFormat.NotARouteString"/>.
    /// </remarks>
    public static RouteStringFormat Classify(string routeString)
    {
        var s = routeString.Trim();
        if (s.Length == 0) return RouteStringFormat.Empty;
        if (s.StartsWith(ModernPrefix, StringComparison.Ordinal)) return RouteStringFormat.Modern;

        // A leading '!' is MDT's own marker for the LibDeflate-plus-AceSerializer vintage, so it
        // is taken at its word even if the body is malformed — it says what it meant to be.
        if (s.StartsWith('!')) return RouteStringFormat.LegacyDeflate;

        return s.Length >= MinimumLegacyLength && s.All(c => PrintCharset.Contains(c))
            ? RouteStringFormat.LegacyCompress
            : RouteStringFormat.NotARouteString;
    }

    /// <summary>
    /// Why a string is being refused, in words fit to put in front of a user.
    /// </summary>
    /// <remarks>
    /// One wording, shared by the paste box and the CLI, so the two cannot drift into telling
    /// the same user different things about the same string.
    /// </remarks>
    public static string DescribeRefusal(RouteStringFormat format) => format switch
    {
        RouteStringFormat.Empty => "Paste an MDT route string.",

        RouteStringFormat.LegacyDeflate =>
            "That is a legacy MDT route string (the '!' LibDeflate + AceSerializer format). " +
            "Only the modern '!~MDT2~' format is supported — MDT has written nothing else for " +
            "a long time, so re-export the route from a current MDT or from keystone.guru.",

        RouteStringFormat.LegacyCompress =>
            "That is a legacy MDT route string (the oldest, unprefixed LibCompress + " +
            "AceSerializer format). Only the modern '!~MDT2~' format is supported — re-export " +
            "the route from a current MDT or from keystone.guru.",

        RouteStringFormat.NotARouteString =>
            "That is not an MDT route string. An MDT route starts with '!~MDT2~' and is a few " +
            "hundred characters long — copy it from MDT's export box, or from keystone.guru's " +
            "“MDT string” button.",

        _ => "That route string cannot be read.",
    };

    /// <summary>Decodes a route string.</summary>
    /// <exception cref="RouteDecodeException">Malformed, or a vintage that is not supported yet.</exception>
    public static Route Decode(string routeString)
    {
        var s = routeString.Trim();
        return Classify(s) switch
        {
            RouteStringFormat.Modern => FromPreset(DecodeModernPayload(s)),
            var format => throw new RouteDecodeException(DescribeRefusal(format)),
        };
    }

    /// <summary>Base64 → raw Deflate → CBOR, returning the raw decoded tree.</summary>
    /// <remarks>
    /// Both halves of this were open questions the research could not settle from source, and
    /// both were measured against a real exported string rather than guessed:
    /// <c>C_EncodingUtil.EncodeBase64</c> is the standard RFC-4648 alphabet with standard
    /// padding, and <c>Enum.CompressionMethod.Deflate</c> is <b>raw</b> deflate — a
    /// zlib-wrapped or gzip read of the same bytes fails the header check.
    /// </remarks>
    internal static object? DecodeModernPayload(string routeString)
    {
        var body = routeString[ModernPrefix.Length..].Trim();

        byte[] compressed;
        try { compressed = Convert.FromBase64String(body); }
        catch (FormatException ex)
        {
            throw new RouteDecodeException("The route string is not valid Base64.", ex);
        }

        byte[] cbor;
        try
        {
            using var source = new MemoryStream(compressed);
            using var inflate = new DeflateStream(source, CompressionMode.Decompress);
            using var buffer = new MemoryStream();
            inflate.CopyTo(buffer);
            cbor = buffer.ToArray();
        }
        catch (InvalidDataException ex)
        {
            throw new RouteDecodeException("The route string did not inflate.", ex);
        }

        return CborTree.Read(cbor);
    }

    private static Route FromPreset(object? decoded)
    {
        if (decoded is not IReadOnlyDictionary<object, object?> preset)
            throw new RouteDecodeException("The decoded route is not a table.");

        if (CborTree.Get(preset, "value") is not IReadOnlyDictionary<object, object?> value)
            throw new RouteDecodeException("The decoded route has no 'value' table.");

        // `week`, `teeming` and `riftOffsets` are still on the wire but carry no meaning: the
        // affix machinery is gone from Midnight MDT, and Presets.lua force-nils `week` on load.
        return new Route
        {
            Name = CborTree.AsString(CborTree.Get(preset, "text")),
            Uid = CborTree.AsString(CborTree.Get(preset, "uid")),
            Difficulty = CborTree.AsInt(CborTree.Get(preset, "difficulty")),
            AddonVersion = CborTree.AsInt(CborTree.Get(preset, "addonVersion")),
            DungeonIndex = CborTree.AsInt(CborTree.Get(value, "currentDungeonIdx"))
                           ?? throw new RouteDecodeException("The route names no dungeon."),
            CurrentPull = CborTree.AsInt(CborTree.Get(value, "currentPull")) ?? 1,
            CurrentSubLevel = CborTree.AsInt(CborTree.Get(value, "currentSublevel")) ?? 1,
            Pulls = ReadPulls(CborTree.Get(value, "pulls")),
        };
    }

    private static List<Pull> ReadPulls(object? raw)
    {
        var pulls = new List<Pull>();
        if (raw is not IReadOnlyList<object?> list) return pulls;

        for (var i = 0; i < list.Count; i++)
        {
            if (list[i] is not IReadOnlyDictionary<object, object?> table)
                throw new RouteDecodeException($"Pull {i + 1} is not a table.");

            var enemies = new List<PullEnemy>();
            string? color = null;
            var unknown = new List<string>();

            foreach (var (key, entry) in table)
            {
                // "Does the key parse as a positive integer" is the whole discrimination
                // between an enemy index and an option key (Pulls.lua's `tonumber(enemyIdx)`).
                if (TryEnemyIndex(key, out var enemyIndex))
                {
                    enemies.Add(new PullEnemy(enemyIndex, ReadCloneIndices(entry)));
                }
                else if (CborTree.AsString(key) is { } option)
                {
                    if (option == "color") color = CborTree.AsString(entry);
                    else unknown.Add(option);
                }
            }

            enemies.Sort((a, b) => a.EnemyIndex.CompareTo(b.EnemyIndex));
            unknown.Sort(StringComparer.Ordinal);

            pulls.Add(new Pull
            {
                Number = i + 1,
                Color = color,
                Enemies = enemies,
                UnknownOptions = unknown,
            });
        }

        return pulls;
    }

    private static bool TryEnemyIndex(object key, out int index)
    {
        index = 0;
        // A Lua table written with integer keys arrives as CBOR integers, but a string key that
        // happens to be numeric counts too — that is what `tonumber` accepts.
        switch (key)
        {
            case long l when l > 0 && l <= int.MaxValue:
                index = (int)l;
                return true;
            case string s when int.TryParse(s, out var parsed) && parsed > 0:
                index = parsed;
                return true;
            default:
                return false;
        }
    }

    private static List<int> ReadCloneIndices(object? raw)
    {
        var indices = new List<int>();
        switch (raw)
        {
            // Dense on the wire: a plain array of clone indices.
            case IReadOnlyList<object?> list:
                foreach (var item in list)
                    if (CborTree.AsInt(item) is { } n) indices.Add(n);
                break;

            // Sparse after editing, so it can arrive keyed instead. Order by key, since the
            // values are the clone indices and the keys are only positions.
            case IReadOnlyDictionary<object, object?> map:
                foreach (var (_, v) in map.OrderBy(kv => CborTree.AsInt(kv.Key) ?? int.MaxValue))
                    if (CborTree.AsInt(v) is { } n) indices.Add(n);
                break;
        }
        return indices;
    }
}

public enum RouteStringFormat
{
    /// <summary>Nothing was pasted.</summary>
    Empty,

    /// <summary><c>!~MDT2~</c> — Base64 → raw Deflate → CBOR. The only one we read.</summary>
    Modern,

    /// <summary><c>!</c> — LibDeflate → AceSerializer. Recognised so it can be refused by name.</summary>
    LegacyDeflate,

    /// <summary>
    /// No prefix — LibDeflate print-decode → LibCompress → AceSerializer. Recognised so it can
    /// be refused by name, and only when the body actually looks like one.
    /// </summary>
    LegacyCompress,

    /// <summary>
    /// A URL, a word, a truncated paste — something that is not a route string in any vintage.
    /// </summary>
    /// <remarks>
    /// This exists because the alternative is worse: without it every unrecognised paste is
    /// called a legacy route, and the user is told their string is an obsolete format when in
    /// fact they copied the wrong thing.
    /// </remarks>
    NotARouteString,
}

public sealed class RouteDecodeException(string message, Exception? inner = null)
    : Exception(message, inner);

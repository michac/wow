using System.Formats.Cbor;
using System.Globalization;
using System.Text;

namespace MdtDesktop.Core.Routes;

/// <summary>
/// Reads CBOR into a plain object tree: maps become dictionaries, arrays become lists, and
/// everything else becomes <c>string</c>, <c>long</c>, <c>double</c>, <c>bool</c> or null.
/// </summary>
/// <remarks>
/// A tree rather than a typed deserialization because a pull is a genuinely mixed table —
/// integer enemy indices alongside the string key <c>color</c> — which no fixed shape models.
/// <para>
/// ⚠ <c>C_EncodingUtil.SerializeCBOR</c> writes Lua strings as CBOR <b>byte</b> strings
/// (major type 2), not text strings (major type 3). Measured against a real exported route:
/// every key in it, <c>"pulls"</c> and <c>"color"</c> included, arrives as a byte string. Both
/// are decoded as UTF-8 text here, so a reader never has to care which one it got.
/// </para>
/// </remarks>
internal static class CborTree
{
    /// <summary>Maximum nesting accepted, so a malformed string cannot recurse without bound.</summary>
    private const int MaxDepth = 64;

    public static object? Read(byte[] cbor)
    {
        var reader = new CborReader(cbor, CborConformanceMode.Lax);
        try
        {
            var value = ReadValue(reader, 0);
            if (reader.BytesRemaining > 0)
                throw new RouteDecodeException(
                    $"{reader.BytesRemaining} unexpected bytes after the decoded route.");
            return value;
        }
        catch (CborContentException ex)
        {
            throw new RouteDecodeException("The route's CBOR payload is malformed.", ex);
        }
        catch (InvalidOperationException ex)
        {
            throw new RouteDecodeException("The route's CBOR payload is malformed.", ex);
        }
    }

    private static object? ReadValue(CborReader reader, int depth)
    {
        if (depth > MaxDepth)
            throw new RouteDecodeException($"The route nests deeper than {MaxDepth} levels.");

        switch (reader.PeekState())
        {
            case CborReaderState.StartMap:
            {
                var count = reader.ReadStartMap();
                var map = new Dictionary<object, object?>();
                while (reader.PeekState() != CborReaderState.EndMap)
                {
                    var key = ReadValue(reader, depth + 1)
                              ?? throw new RouteDecodeException("A route table has a null key.");
                    // Last write wins, matching how a Lua table would end up.
                    map[key] = ReadValue(reader, depth + 1);
                }
                reader.ReadEndMap();
                _ = count;
                return map;
            }

            case CborReaderState.StartArray:
            {
                reader.ReadStartArray();
                var list = new List<object?>();
                while (reader.PeekState() != CborReaderState.EndArray)
                    list.Add(ReadValue(reader, depth + 1));
                reader.ReadEndArray();
                return list;
            }

            case CborReaderState.TextString:
                return reader.ReadTextString();

            case CborReaderState.ByteString:
                // Lua strings land here — see the remarks above.
                return Encoding.UTF8.GetString(reader.ReadByteString());

            case CborReaderState.UnsignedInteger:
            case CborReaderState.NegativeInteger:
                return reader.ReadInt64();

            case CborReaderState.Boolean:
                return reader.ReadBoolean();

            case CborReaderState.Null:
                reader.ReadNull();
                return null;

            case CborReaderState.Undefined:
                reader.ReadSimpleValue();
                return null;

            case CborReaderState.HalfPrecisionFloat:
            case CborReaderState.SinglePrecisionFloat:
            case CborReaderState.DoublePrecisionFloat:
                return reader.ReadDouble();

            default:
                throw new RouteDecodeException($"Unsupported CBOR element: {reader.PeekState()}.");
        }
    }

    public static object? Get(IReadOnlyDictionary<object, object?> map, string key)
        => map.TryGetValue(key, out var value) ? value : null;

    public static string? AsString(object? value) => value as string;

    public static int? AsInt(object? value) => value switch
    {
        long l when l >= int.MinValue && l <= int.MaxValue => (int)l,
        double d when Math.Abs(d % 1) < double.Epsilon
                      && d is >= int.MinValue and <= int.MaxValue => (int)d,
        // ⚠ Invariant, matching AsDouble below: the format writes numbers Lua's way, and a
        // culture-sensitive parse beside a culture-insensitive one is exactly the drift this
        // codebase legislates against.
        string s when int.TryParse(s, NumberStyles.Integer, CultureInfo.InvariantCulture, out var parsed)
            => parsed,
        _ => null,
    };

    /// <summary>
    /// A number, however it crossed the wire.
    /// </summary>
    /// <remarks>
    /// ⚠ Invariant on purpose. A preset object's coordinates arrive as <b>strings</b>
    /// (<c>str('686.1')</c>, <c>str('-459.4')</c>), so this is the parse that decides where a
    /// note lands — under a comma-decimal culture an ambient parse would read <c>686.1</c> as
    /// <c>6861</c> and put the pin off the canvas.
    /// </remarks>
    public static double? AsDouble(object? value) => value switch
    {
        long l => l,
        double d => d,
        string s when double.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out var parsed)
            => parsed,
        _ => null,
    };
}

using System.Formats.Cbor;
using System.IO.Compression;
using MdtDesktop.Core.Routes;

namespace MdtDesktop.Core.Tests.Routes;

/// <summary>
/// Builds a real <c>!~MDT2~</c> string from hand-written CBOR.
/// </summary>
/// <remarks>
/// One builder, shared, so two test files cannot drift on the single most easily forgotten fact
/// about this format — <b>Lua strings cross as CBOR byte strings</b>, not text strings. Going
/// through the whole base64 → deflate → CBOR pipeline is also why <c>CborTree</c> can stay
/// <c>internal</c> with no <c>InternalsVisibleTo</c>: its helpers are exercised the way the
/// decoder actually reaches them.
/// </remarks>
internal static class SyntheticRoute
{
    /// <summary>Lua strings cross as CBOR byte strings — see <c>CborTree</c>.</summary>
    public static void WriteText(CborWriter w, string s)
        => w.WriteByteString(System.Text.Encoding.UTF8.GetBytes(s));

    public static Route Decode(Action<CborWriter> write)
    {
        var writer = new CborWriter();
        write(writer);

        using var buffer = new MemoryStream();
        using (var deflate = new DeflateStream(buffer, CompressionLevel.Optimal, leaveOpen: true))
            deflate.Write(writer.Encode());

        return RouteDecoder.Decode(RouteDecoder.ModernPrefix + Convert.ToBase64String(buffer.ToArray()));
    }
}

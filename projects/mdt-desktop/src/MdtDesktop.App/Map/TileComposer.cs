using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using MdtDesktop.Core.Map;

namespace MdtDesktop.App.Map;

/// <summary>
/// Flattens a sublevel's 150 map tiles into one bitmap.
/// </summary>
/// <remarks>
/// <para>
/// The tiles are 128 px squares named <c>&lt;sublevel&gt;_&lt;n&gt;.png</c>, laid out row-major
/// over 10 rows of 15 (<c>MapView.lua:504-524</c>), so a sublevel composes to 1920 × 1280 px.
/// </para>
/// <para>
/// Flattening rather than laying 150 <c>Image</c> elements side by side is deliberate: adjacent
/// elements land on fractional device pixels once the map is zoomed and leave hairline seams
/// across the whole map. One bitmap cannot. It also makes panning cheap — one visual, not 150.
/// </para>
/// </remarks>
internal static class TileComposer
{
    private static readonly Dictionary<string, ComposedMap> Cache = [];

    /// <summary>
    /// Composes the sublevel, or returns an empty result when the tile folder is not there.
    /// </summary>
    /// <remarks>
    /// A missing tile is skipped rather than fatal, and the count comes back so the caller can
    /// say "132 of 150 tiles" instead of silently drawing a map with holes in it.
    /// </remarks>
    public static ComposedMap Compose(string directory, int subLevel)
    {
        var key = $"{directory}|{subLevel}";
        if (Cache.TryGetValue(key, out var cached)) return cached;

        var composed = Build(directory, subLevel);
        Cache[key] = composed;
        return composed;
    }

    private static ComposedMap Build(string directory, int subLevel)
    {
        if (!Directory.Exists(directory)) return new ComposedMap(null, 0);

        var width = MapGeometry.TileColumns * MapGeometry.TilePixels;
        var height = MapGeometry.TileRows * MapGeometry.TilePixels;

        var visual = new DrawingVisual();
        var found = 0;

        using (var context = visual.RenderOpen())
        {
            for (var row = 1; row <= MapGeometry.TileRows; row++)
            {
                for (var column = 1; column <= MapGeometry.TileColumns; column++)
                {
                    var tile = MapGeometry.TileNumber(row, column);
                    var path = Path.Combine(directory, MapGeometry.TileFileName(subLevel, tile));
                    if (Load(path) is not { } bitmap) continue;

                    found++;
                    context.DrawImage(bitmap, new Rect(
                        (column - 1) * MapGeometry.TilePixels,
                        (row - 1) * MapGeometry.TilePixels,
                        MapGeometry.TilePixels,
                        MapGeometry.TilePixels));
                }
            }
        }

        if (found == 0) return new ComposedMap(null, 0);

        var target = new RenderTargetBitmap(width, height, 96, 96, PixelFormats.Pbgra32);
        target.Render(visual);
        target.Freeze();
        return new ComposedMap(target, found);
    }

    private static BitmapSource? Load(string path)
    {
        if (!File.Exists(path)) return null;

        try
        {
            // OnLoad so the file handle is released immediately — the cache directory is
            // re-extracted wholesale by `data update` while the app may still be open.
            using var stream = File.OpenRead(path);
            var frame = BitmapFrame.Create(stream, BitmapCreateOptions.None, BitmapCacheOption.OnLoad);
            frame.Freeze();
            return frame;
        }
        catch (Exception ex) when (ex is IOException or NotSupportedException or ArgumentException)
        {
            return null;
        }
    }
}

/// <param name="Image">The flattened sublevel, or null when no tile could be read.</param>
/// <param name="TilesFound">How many of the expected 150 tiles were actually there.</param>
internal readonly record struct ComposedMap(BitmapSource? Image, int TilesFound);

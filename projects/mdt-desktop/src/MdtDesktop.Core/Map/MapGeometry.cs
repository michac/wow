using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Map;

/// <summary>
/// The map canvas: how MDT's coordinates, its tile grid and its blip sizes relate.
/// </summary>
/// <remarks>
/// <para>
/// There is no transform to derive. <c>clone.x</c> / <c>clone.y</c> are already in map-canvas
/// units from the canvas top-left, <b>+x right, −y down</b>, and the only factor MDT ever
/// applies is the user's zoom (<c>DungeonEnemies.lua:717-719</c> sets the blip's CENTER at
/// <c>mapPanelTile1</c>'s TOPLEFT plus <c>clone.x * scale</c>, <c>clone.y * scale</c>).
/// </para>
/// <para>
/// ⚠ The canvas is <b>840 × 560</b> units. <c>MainFrame.lua:10-11</c> declares
/// <c>sizey = 555</c>, but the tile grid is 10 rows of 56 units = 560; the five-unit overhang
/// is uncorrected in MDT and we match it rather than "fixing" it, because matching is what
/// makes a blip land where MDT draws it.
/// </para>
/// </remarks>
public static class MapGeometry
{
    /// <summary>Canvas width in map units — the space clone coordinates live in.</summary>
    public const double CanvasWidth = 840;

    /// <summary>Canvas height in map units.</summary>
    public const double CanvasHeight = 560;

    public const int TileRows = 10;
    public const int TileColumns = 15;

    /// <summary>Each tile is 128 px square, so a composed sublevel is 1920 × 1280 px.</summary>
    public const int TilePixels = 128;

    public const int TilesPerSubLevel = TileRows * TileColumns;

    /// <summary>MDT's blip frame is this many units square before the scale chain.</summary>
    public const double BlipFrameSize = 13;

    /// <summary>A boss blip is drawn 1.7× the size of trash.</summary>
    public const double BossScale = 1.7;

    /// <summary>The constant MDT folds into every blip (<c>DungeonEnemies.lua:726-735</c>).</summary>
    public const double BlipBaseScale = 0.6;

    /// <summary>
    /// A clone's position in pixels on a canvas of the given size, as the blip's <b>centre</b>.
    /// </summary>
    /// <remarks>
    /// Defaults to the 840 × 560 unit space, so a WPF canvas laid out at those dimensions
    /// takes the coordinates straight through with only the y sign flipped.
    /// </remarks>
    public static (double X, double Y) ToCanvas(
        double x, double y, double widthPx = CanvasWidth, double heightPx = CanvasHeight)
        => (x / CanvasWidth * widthPx, -y / CanvasHeight * heightPx);

    /// <summary>
    /// The blip scale chain, exactly as MDT builds it.
    /// </summary>
    /// <remarks>
    /// MDT multiplies by <c>MDT.scaleMultiplier[dungeonIndex]</c> and the user's <c>db.scale</c>
    /// too. Neither is in play here: <c>scaleMultiplier</c> is declared and never assigned in
    /// this build, and <c>db.scale</c> is the user's zoom, which is the viewport's job.
    /// </remarks>
    public static double BlipScale(Clone clone, Enemy enemy)
        => (clone.Scale ?? 1) * enemy.Scale * (enemy.IsBoss ? BossScale : 1) * BlipBaseScale;

    /// <summary>The blip's on-canvas diameter in map units.</summary>
    public static double BlipSize(Clone clone, Enemy enemy) => BlipFrameSize * BlipScale(clone, enemy);

    /// <summary>
    /// Whether a clone belongs on the sublevel being drawn (<c>DungeonEnemies.lua:844-846</c>).
    /// </summary>
    /// <remarks>
    /// Every Midnight dungeon ships exactly one sublevel and every shipped clone names it, but
    /// the null case is MDT's own "show everywhere" and an imported preset can still carry it.
    /// </remarks>
    public static bool IsVisibleOn(Clone clone, int subLevel)
        => clone.SubLevel is null || clone.SubLevel == subLevel;

    /// <summary>Tile number for a 1-based row and column. Row-major: 1 is top-left, 150 bottom-right.</summary>
    public static int TileNumber(int row, int column) => (row - 1) * TileColumns + column;

    /// <summary>
    /// A tile's file name inside the sublevel's texture folder — <c>&lt;sublevel&gt;_&lt;n&gt;.png</c>
    /// (<c>MapView.lua:504-524</c>, <c>:592-604</c>).
    /// </summary>
    public static string TileFileName(int subLevel, int tileNumber) => $"{subLevel}_{tileNumber}.png";

    /// <summary>The 150 tile file names of a sublevel, in the row-major order they are laid out in.</summary>
    public static IEnumerable<string> TileFileNames(int subLevel)
    {
        for (var tile = 1; tile <= TilesPerSubLevel; tile++)
            yield return TileFileName(subLevel, tile);
    }
}

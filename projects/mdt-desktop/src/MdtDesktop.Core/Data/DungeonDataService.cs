using MdtDesktop.Core.Model;

namespace MdtDesktop.Core.Data;

/// <summary>
/// Keeps the cached dungeon data in step with MDT's latest release, and hands it out.
/// </summary>
public sealed class DungeonDataService(
    DataCache? cache = null,
    ReleaseFetcher? fetcher = null,
    DungeonExtractor? extractor = null)
{
    private readonly DataCache _cache = cache ?? new DataCache();
    private readonly ReleaseFetcher _fetcher = fetcher ?? new ReleaseFetcher();
    private readonly DungeonExtractor _extractor = extractor ?? new DungeonExtractor();

    public DataCache Cache => _cache;

    /// <summary>
    /// Reads the cached data, or null when there is no cache this code can read.
    /// </summary>
    /// <remarks>
    /// ⚠ A cache written under an older schema is refused rather than read. It would
    /// deserialize perfectly well and be quietly wrong — see
    /// <see cref="CacheStamp.CurrentSchemaVersion"/>.
    /// </remarks>
    public DungeonData? LoadCached()
        => File.Exists(_cache.DungeonsJsonPath) && _cache.ReadStamp() is { IsCurrentSchema: true }
            ? DungeonExtractor.Load(_cache.DungeonsJsonPath)
            : null;

    /// <summary>
    /// Brings the cache up to the latest release, re-extracting the dungeon data.
    /// </summary>
    /// <param name="force">Re-download even when the cache already holds the latest tag.</param>
    public async Task<UpdateResult> UpdateAsync(
        bool force = false, IProgress<string>? progress = null, CancellationToken ct = default)
    {
        var stamp = _cache.ReadStamp();
        var release = await _fetcher.LatestAsync(ct).ConfigureAwait(false);
        progress?.Report($"latest release is {release.Tag}");

        var current = stamp is { IsCurrentSchema: true }
                      && stamp.Tag == release.Tag
                      && File.Exists(_cache.DungeonsJsonPath)
                      && Directory.Exists(_cache.AddonDirectory);

        if (current && !force)
        {
            progress?.Report("cache is already current");
            return new UpdateResult(release.Tag, Downloaded: false, stamp!);
        }

        await _fetcher.DownloadAndExtractAsync(release, _cache, progress, ct).ConfigureAwait(false);

        progress?.Report("reading dungeon data through the Lua sidecar…");
        var json = await _extractor.ExtractJsonAsync(_cache.AddonDirectory, ct).ConfigureAwait(false);
        var data = DungeonExtractor.Parse(json);

        // Written from the extractor's own output, not re-serialized from the model, so the
        // cache file is byte-identical to what the sidecar produced and stays diffable.
        await File.WriteAllTextAsync(_cache.DungeonsJsonPath, json, ct).ConfigureAwait(false);

        var written = new CacheStamp(
            release.Tag,
            data.AddonVersion,
            data.InterfaceVersion,
            DateTimeOffset.UtcNow,
            data.Dungeons.Count,
            data.Dungeons.Sum(d => d.Enemies.Count),
            data.Dungeons.Sum(d => d.Enemies.Sum(e => e.Clones.Count)),
            CacheStamp.CurrentSchemaVersion);

        _cache.WriteStamp(written);
        return new UpdateResult(release.Tag, Downloaded: true, written);
    }
}

public sealed record UpdateResult(string Tag, bool Downloaded, CacheStamp Stamp);

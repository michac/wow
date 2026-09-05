using System.Net.Http.Json;
using System.IO.Compression;
using System.Text.Json.Serialization;

namespace MdtDesktop.Core.Data;

/// <summary>
/// Downloads an MDT release from GitHub and unpacks it into the cache.
/// </summary>
/// <remarks>
/// This is the app's only dependency on anything outside itself, and it is deliberately the
/// whole story: the packaged zip carries the dungeon Lua, all 16 texture folders and MDT's
/// vendored <c>libs/</c> (which M5 needs), so there is no game install to find, no CurseForge
/// API key and no wago.io. The releases endpoint answers unauthenticated.
/// </remarks>
public sealed class ReleaseFetcher
{
    public const string Repository = "Nnoggie/MythicDungeonTools";

    private static readonly Uri LatestReleaseUri =
        new($"https://api.github.com/repos/{Repository}/releases/latest");

    private readonly HttpClient _http;

    public ReleaseFetcher(HttpClient? http = null)
    {
        _http = http ?? new HttpClient();
        // GitHub rejects a request with no User-Agent.
        if (!_http.DefaultRequestHeaders.UserAgent.Any())
            _http.DefaultRequestHeaders.UserAgent.ParseAdd("mdt-desktop");
    }

    /// <summary>Asks GitHub which release is current.</summary>
    public async Task<MdtRelease> LatestAsync(CancellationToken ct = default)
    {
        var release = await _http.GetFromJsonAsync<GitHubRelease>(LatestReleaseUri, ct)
                          .ConfigureAwait(false)
                      ?? throw new DataUpdateException("GitHub returned no release for " + Repository);

        var asset = release.Assets.FirstOrDefault(
                        a => a.Name.EndsWith(".zip", StringComparison.OrdinalIgnoreCase))
                    ?? throw new DataUpdateException(
                        $"Release {release.TagName} carries no .zip asset.");

        return new MdtRelease(release.TagName, asset.Name, asset.Size, new Uri(asset.DownloadUrl));
    }

    /// <summary>
    /// Downloads <paramref name="release"/> and replaces the cache's extracted copy with it.
    /// </summary>
    public async Task DownloadAndExtractAsync(
        MdtRelease release, DataCache cache, IProgress<string>? progress = null,
        CancellationToken ct = default)
    {
        cache.EnsureRoot();

        var zipPath = Path.Combine(cache.Root, release.AssetName + ".part");
        progress?.Report($"downloading {release.AssetName} ({release.Size / 1024 / 1024} MB)…");

        try
        {
            using (var response = await _http
                       .GetAsync(release.DownloadUri, HttpCompletionOption.ResponseHeadersRead, ct)
                       .ConfigureAwait(false))
            {
                response.EnsureSuccessStatusCode();
                await using var source = await response.Content.ReadAsStreamAsync(ct).ConfigureAwait(false);
                await using var destination = File.Create(zipPath);
                await source.CopyToAsync(destination, ct).ConfigureAwait(false);
            }

            // Extract to a scratch directory and swap it in, so a failure part-way leaves the
            // previous cache intact rather than a half-unpacked one that looks complete.
            var staging = cache.ReleaseDirectory + ".new";
            DeleteDirectory(staging);
            progress?.Report("extracting…");
            ZipFile.ExtractToDirectory(zipPath, staging);

            if (!Directory.Exists(Path.Combine(staging, "MythicDungeonTools")))
                throw new DataUpdateException(
                    $"{release.AssetName} has no MythicDungeonTools/ folder at its root.");

            DeleteDirectory(cache.ReleaseDirectory);
            Directory.Move(staging, cache.ReleaseDirectory);
        }
        finally
        {
            // The zip is 14 MB and buys nothing once unpacked.
            try { File.Delete(zipPath); } catch (IOException) { /* best effort */ }
        }
    }

    private static void DeleteDirectory(string path)
    {
        if (Directory.Exists(path)) Directory.Delete(path, recursive: true);
    }

    private sealed record GitHubRelease(
        [property: JsonPropertyName("tag_name")] string TagName,
        [property: JsonPropertyName("assets")] IReadOnlyList<GitHubAsset> Assets);

    private sealed record GitHubAsset(
        [property: JsonPropertyName("name")] string Name,
        [property: JsonPropertyName("size")] long Size,
        [property: JsonPropertyName("browser_download_url")] string DownloadUrl);
}

/// <summary>The release zip to fetch.</summary>
public sealed record MdtRelease(string Tag, string AssetName, long Size, Uri DownloadUri);

/// <summary>A data update could not be completed.</summary>
public sealed class DataUpdateException(string message, Exception? inner = null)
    : Exception(message, inner);

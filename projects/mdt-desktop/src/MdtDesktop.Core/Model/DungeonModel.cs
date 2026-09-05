using System.Text.Json;
using System.Text.Json.Serialization;

namespace MdtDesktop.Core.Model;

/// <summary>
/// MDT's shipped dungeon data, as read out of a release by <c>lua/extract_dungeons.lua</c>.
/// </summary>
/// <remarks>
/// Every collection is an array whose members carry their own <c>index</c> rather than a
/// JSON object keyed by position. MDT's indices are sparse — dungeons are 11, 17, 20, 42,
/// 45, 150-155 and 160-164, and 6.2.13 deleted clone 12 of The Blinding Vale's Radiant
/// Spellsower, leaving that enemy at 1-11, 13-15 — so position never means identity.
/// Look things up through the <c>By…</c> dictionaries, which key on the real index.
/// </remarks>
public sealed class DungeonData
{
    /// <summary>MDT's own <c>## Version</c>, e.g. <c>6.2.13</c>.</summary>
    public string? AddonVersion { get; init; }

    /// <summary>MDT's <c>## Interface</c>, e.g. <c>120100</c>.</summary>
    public string? InterfaceVersion { get; init; }

    public IReadOnlyList<Dungeon> Dungeons { get; init; } = [];

    private Dictionary<int, Dungeon>? _byIndex;

    /// <summary>Dungeons keyed by MDT's real dungeon index.</summary>
    [JsonIgnore]
    public IReadOnlyDictionary<int, Dungeon> ByIndex
        => _byIndex ??= Dungeons.ToDictionary(d => d.Index);

    public Dungeon? Find(int index) => ByIndex.GetValueOrDefault(index);
}

public sealed class Dungeon
{
    /// <summary>MDT's dungeon index — the identity used everywhere, including route strings.</summary>
    public int Index { get; init; }

    /// <summary>Localised name; English here, since the extractor loads <c>Locales/enUS.lua</c>.</summary>
    public string? Name { get; init; }

    public string? EnglishName { get; init; }
    public string? ShortName { get; init; }

    /// <summary>The UiMapID, not the instance id.</summary>
    public int? MapId { get; init; }

    public int? TeleportId { get; init; }
    public int? IconId { get; init; }

    /// <summary>Enemy forces required at 100%. MDT ships only <c>normal</c> — the affix
    /// variants (teeming and friends) are gone from Midnight entirely.</summary>
    public int TotalCount { get; init; }

    public IReadOnlyList<int> ZoneIds { get; init; } = [];
    public IReadOnlyList<SubLevel> SubLevels { get; init; } = [];
    public IReadOnlyList<Enemy> Enemies { get; init; } = [];
    public IReadOnlyList<MapPoi> Pois { get; init; } = [];

    private Dictionary<int, Enemy>? _enemiesByIndex;

    /// <summary>Enemies keyed by MDT's enemy index — what a pull's integer keys refer to.</summary>
    [JsonIgnore]
    public IReadOnlyDictionary<int, Enemy> EnemiesByIndex
        => _enemiesByIndex ??= Enemies.ToDictionary(e => e.Index);

    [JsonIgnore]
    public string DisplayName => Name ?? EnglishName ?? $"Dungeon {Index}";

    public override string ToString() => $"{Index} {DisplayName}";
}

public sealed class SubLevel
{
    public int Index { get; init; }
    public string? Name { get; init; }

    /// <summary>MDT's client-side texture path, read verbatim.</summary>
    public string? CustomTextures { get; init; }

    /// <summary>
    /// The trailing folder of <see cref="CustomTextures"/> — the directory under
    /// <c>Midnight/Textures/</c> holding this sublevel's 150 tiles.
    /// </summary>
    /// <remarks>
    /// It is split off the path, never reconstructed from the Lua file name: MDT ships
    /// <c>SeatoftheTriumvirate.lua</c> pointing at <c>Textures\SeatOfTheTriumvirate</c>.
    /// </remarks>
    public string? TextureFolder { get; init; }
}

public sealed class Enemy
{
    public int Index { get; init; }
    public string? Name { get; init; }

    /// <summary>The creature (NPC) id.</summary>
    public int Id { get; init; }

    /// <summary>Forces this enemy contributes, unless a clone overrides it.</summary>
    public int Count { get; init; }

    public long Health { get; init; }
    public double Scale { get; init; } = 1;
    public int? DisplayId { get; init; }
    public string? CreatureType { get; init; }
    public int? Level { get; init; }
    public bool IsBoss { get; init; }
    public int? EncounterId { get; init; }
    public int? InstanceId { get; init; }
    public bool Stealth { get; init; }
    public bool StealthDetect { get; init; }

    /// <summary>
    /// The mob's spell book, with MDT's per-spell flags. Sorted by id, so the cache diffs.
    /// </summary>
    /// <remarks>
    /// 434 of 462 enemies carry at least one. The flags are what make a mob's <i>role</i>
    /// readable from the data rather than guessed — see <see cref="MobRoles"/>.
    /// </remarks>
    public IReadOnlyList<Spell> Spells { get; init; } = [];

    /// <summary>True when any spell is flagged interruptible — MDT's own "this is a caster".</summary>
    [JsonIgnore]
    public bool HasInterruptibleSpell => Spells.Any(s => s.Interruptible);

    /// <summary>
    /// Every dispel/soothe flag anywhere in the mob's book, deduplicated, in a fixed order.
    /// </summary>
    /// <remarks>A mob can carry several, which is why these are badges rather than a fill colour.</remarks>
    [JsonIgnore]
    public IReadOnlyList<SpellFlag> SpellFlags
        => [.. Spells.SelectMany(s => s.Flags).Distinct().Order()];

    /// <summary>Crowd-control the mob is susceptible to — <c>Taunt</c>, <c>Incapacitate</c>, …</summary>
    public IReadOnlyList<string> Characteristics { get; init; } = [];

    public IReadOnlyList<Clone> Clones { get; init; } = [];

    private Dictionary<int, Clone>? _clonesByIndex;

    /// <summary>Clones keyed by MDT's clone index. Sparse in shipped data — see <see cref="DungeonData"/>.</summary>
    [JsonIgnore]
    public IReadOnlyDictionary<int, Clone> ClonesByIndex
        => _clonesByIndex ??= Clones.ToDictionary(c => c.Index);

    public override string ToString() => $"{Index} {Name} (x{Clones.Count}, {Count} forces)";
}

/// <summary>One placement of an <see cref="Enemy"/> on the map.</summary>
public sealed class Clone
{
    public int Index { get; init; }

    /// <summary>Map-canvas units from the canvas left edge, +x right. Canvas is 840 wide.</summary>
    public double X { get; init; }

    /// <summary>Map-canvas units from the canvas top edge, <b>negative going down</b>. Canvas is 560 tall.</summary>
    public double Y { get; init; }

    /// <summary>The sublevel this clone stands on. Null means "show on every sublevel".</summary>
    public int? SubLevel { get; init; }

    /// <summary>Pull-group id: clones sharing one are linked and pull together.</summary>
    [JsonPropertyName("g")]
    public int? Group { get; init; }

    /// <summary>Per-clone size multiplier feeding the blip-scale chain.</summary>
    public double? Scale { get; init; }

    /// <summary>Per-clone forces override; three exist in the shipped data.</summary>
    public int? Count { get; init; }

    public IReadOnlyList<PatrolPoint> Patrol { get; init; } = [];
}

/// <summary>
/// One spell in an enemy's book, with what MDT says you can do about it.
/// </summary>
/// <remarks>
/// MDT ships exactly these seven flags and nothing else (measured across
/// <c>Midnight/*.lua</c> on 6.2.13: interruptible 133, magic 72, enrage 32, poison 25,
/// bleed 24, curse 10, disease 6). The extractor emits only the true ones, so an absent
/// key arrives here as <c>false</c> without a converter.
/// </remarks>
public sealed class Spell
{
    public int Id { get; init; }

    /// <summary>Kickable. The one flag that is a tactical role rather than a dispel type.</summary>
    public bool Interruptible { get; init; }

    /// <summary>Soothe.</summary>
    public bool Enrage { get; init; }

    public bool Magic { get; init; }
    public bool Curse { get; init; }
    public bool Poison { get; init; }
    public bool Disease { get; init; }
    public bool Bleed { get; init; }

    /// <summary>The dispel/soothe flags this spell carries, in a fixed order, for a badge row.</summary>
    [JsonIgnore]
    public IEnumerable<SpellFlag> Flags
    {
        get
        {
            if (Enrage) yield return SpellFlag.Enrage;
            if (Magic) yield return SpellFlag.Magic;
            if (Curse) yield return SpellFlag.Curse;
            if (Poison) yield return SpellFlag.Poison;
            if (Disease) yield return SpellFlag.Disease;
            if (Bleed) yield return SpellFlag.Bleed;
        }
    }

    public override string ToString()
        => Id + (Interruptible ? " (interruptible)" : "") +
           (Flags.Any() ? " " + string.Join("/", Flags).ToLowerInvariant() : "");
}

/// <summary>What can be removed from a mob — orthogonal to its role, so it rides as a badge.</summary>
public enum SpellFlag
{
    Enrage,
    Magic,
    Curse,
    Poison,
    Disease,
    Bleed,
}

public sealed class PatrolPoint
{
    public int Index { get; init; }
    public double X { get; init; }
    public double Y { get; init; }
}

/// <summary>
/// A point of interest — the dungeon entrance, a usable item, a map link, an assignable marker.
/// </summary>
/// <remarks>
/// Its keys vary by <see cref="Type"/>, so only the shared ones are named and the rest are
/// captured verbatim. The bulk of the per-type detail nests under an <c>info</c> member.
/// </remarks>
public sealed class MapPoi
{
    public int SubLevel { get; init; }
    public int Index { get; init; }
    public string? Type { get; init; }
    public double X { get; init; }
    public double Y { get; init; }

    [JsonExtensionData]
    public IDictionary<string, JsonElement> Extra { get; init; } = new Dictionary<string, JsonElement>();
}

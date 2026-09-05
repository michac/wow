using MdtDesktop.Core.Data;
using MdtDesktop.Core.Model;

namespace MdtDesktop.Cli;

/// <summary>
/// <c>mdtdesk roles …</c> — what the role colouring will say, printed instead of drawn.
/// </summary>
/// <remarks>
/// Three of the four roles are read out of MDT's data and are checkable against numbers taken
/// off the shipped Lua by hand; the fourth is a heuristic that cannot be settled without eyes on
/// a map. So this prints the minibosses it picked <b>by name, with their health and how many
/// times the trash median that is</b> — enough to argue with the rule from a terminal, which is
/// the most that can honestly be done about it here.
/// </remarks>
internal static class RoleCommands
{
    public static int Run(string[] args)
    {
        var service = new DungeonDataService();
        if (service.LoadCached() is not { } data)
        {
            Console.Error.WriteLine("No cached dungeon data. Run `mdtdesk data update` first.");
            return 1;
        }

        var index = MobRoleIndex.Build(data);

        Console.WriteLine($"MDT {data.AddonVersion} — {data.Dungeons.Count} dungeons");
        Console.WriteLine($"trash median health : {index.TrashMedianHealth:N0} " +
                          "(every non-boss enemy in the cache, not per dungeon)");
        Console.WriteLine($"miniboss bar        : {index.MinibossHealth:N0} " +
                          $"({MobRoles.MinibossHealthMultiple}× the median — " +
                          "the one invented number here)");
        Console.WriteLine();

        var scope = args.FirstOrDefault(a => !a.StartsWith("--"));
        if (scope is not null)
        {
            if (!int.TryParse(scope, out var dungeonIndex))
            {
                Console.Error.WriteLine("Usage: mdtdesk roles [<dungeonIndex>] [--all]");
                return 2;
            }

            if (data.Find(dungeonIndex) is not { } dungeon)
            {
                Console.Error.WriteLine($"No dungeon with index {dungeonIndex}. See `mdtdesk data list`.");
                return 1;
            }

            return OneDungeon(dungeon, index, args.Contains("--all"));
        }

        return Census(data, index);
    }

    private static int OneDungeon(Dungeon dungeon, MobRoleIndex index, bool everyMob)
    {
        Console.WriteLine($"[{dungeon.Index}] {dungeon.DisplayName} — {dungeon.Enemies.Count} enemies");
        PrintTally(index.Tally(dungeon.Enemies), dungeon.Enemies.Count);
        Console.WriteLine();

        Console.WriteLine($"{"idx",4}  {"role",-9} {"forces",6} {"health",13} {"×med",6}  " +
                          $"{"kick",4}  {"flags",-28} name");

        var rows = dungeon.Enemies
            .Select(e => (Enemy: e, Role: index.Role(e)))
            .Where(r => everyMob || r.Role != MobRole.Melee)
            .OrderByDescending(r => r.Role)
            .ThenByDescending(r => r.Enemy.Health);

        foreach (var (enemy, role) in rows) PrintEnemy(enemy, role, index);

        if (!everyMob)
            Console.WriteLine("\n(melee omitted — pass --all for every mob)");

        return 0;
    }

    private static int Census(DungeonData data, MobRoleIndex index)
    {
        var all = data.Dungeons.SelectMany(d => d.Enemies).ToList();

        Console.WriteLine($"{"idx",4}  {"dungeon",-24} {"mobs",5} {"melee",6} {"caster",7} " +
                          $"{"mini",5} {"boss",5}");

        foreach (var dungeon in data.Dungeons)
        {
            var tally = index.Tally(dungeon.Enemies);
            Console.WriteLine($"{dungeon.Index,4}  {Truncate(dungeon.DisplayName, 24),-24} " +
                              $"{dungeon.Enemies.Count,5} {tally[MobRole.Melee],6} " +
                              $"{tally[MobRole.Caster],7} {tally[MobRole.Miniboss],5} " +
                              $"{tally[MobRole.Boss],5}");
        }

        Console.WriteLine();
        PrintTally(index.Tally(all), all.Count);

        // The two exact rules, restated as a check. If either of these moves, the extraction is
        // wrong rather than the classification — which is a very different thing to go looking at.
        Console.WriteLine();
        Console.WriteLine($"  enemies carrying ≥1 spell : {all.Count(e => e.Spells.Count > 0)}");
        Console.WriteLine($"  spells flagged in total   : {all.Sum(e => e.Spells.Count(s => s.Interruptible || s.Flags.Any()))}");
        foreach (var flag in Enum.GetValues<SpellFlag>())
            Console.WriteLine($"  mobs with {flag,-8}        : {all.Count(e => e.SpellFlags.Contains(flag))}");

        // ⚠ The heuristic, named in full. Nine mobs is the whole of it, so there is no excuse
        // for not reading the list and deciding whether the rule earned them.
        Console.WriteLine();
        Console.WriteLine("minibosses — ⚠ the one invented rule, listed so it can be argued with:");
        Console.WriteLine($"{"idx",4}  {"dungeon",-24} {"health",13} {"×med",6}  name");

        foreach (var dungeon in data.Dungeons)
            foreach (var enemy in dungeon.Enemies.Where(e => index.Role(e) == MobRole.Miniboss)
                         .OrderByDescending(e => e.Health))
                Console.WriteLine($"{dungeon.Index,4}  {Truncate(dungeon.DisplayName, 24),-24} " +
                                  $"{enemy.Health,13:N0} {enemy.Health / index.TrashMedianHealth,6:F1}  " +
                                  $"{enemy.Name}");

        // The near misses are the useful half of a threshold: they say how much slack there is
        // before moving the constant changes the answer.
        Console.WriteLine();
        Console.WriteLine("nearest misses (zero forces, just under the bar):");
        foreach (var (enemy, dungeon) in data.Dungeons
                     .SelectMany(d => d.Enemies.Select(e => (Enemy: e, Dungeon: d)))
                     .Where(x => !x.Enemy.IsBoss && x.Enemy.Count == 0 &&
                                 x.Enemy.Health < index.MinibossHealth)
                     .OrderByDescending(x => x.Enemy.Health)
                     .Take(5))
            Console.WriteLine($"{dungeon.Index,4}  {Truncate(dungeon.DisplayName, 24),-24} " +
                              $"{enemy.Health,13:N0} {enemy.Health / index.TrashMedianHealth,6:F1}  " +
                              $"{enemy.Name}");

        return 0;
    }

    private static void PrintEnemy(Enemy enemy, MobRole role, MobRoleIndex index)
    {
        var flags = string.Join(",", enemy.SpellFlags).ToLowerInvariant();
        if (enemy.Stealth) flags = Join(flags, "stealth");
        if (enemy.StealthDetect) flags = Join(flags, "detect");

        Console.WriteLine($"{enemy.Index,4}  {role,-9} {enemy.Count,6} {enemy.Health,13:N0} " +
                          $"{enemy.Health / index.TrashMedianHealth,6:F1}  " +
                          $"{(enemy.HasInterruptibleSpell ? "yes" : "-"),4}  " +
                          $"{Truncate(flags, 28),-28} {enemy.Name}");

        static string Join(string a, string b) => a.Length == 0 ? b : a + "," + b;
    }

    private static void PrintTally(IReadOnlyDictionary<MobRole, int> tally, int total)
    {
        foreach (var role in Enum.GetValues<MobRole>())
        {
            var count = tally[role];
            var percent = total == 0 ? 0 : 100.0 * count / total;
            Console.WriteLine($"  {role,-9} {count,4}  {percent,5:F1}%");
        }
    }

    private static string Truncate(string s, int width)
        => s.Length <= width ? s : s[..(width - 1)] + "…";
}

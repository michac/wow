// Compile-time identities for everything the engine tracks.
//
// Using enums (not strings) in M1 buys exhaustive `switch`es in the priority
// logic and keeps the proc/debuff/aura wiring type-safe. M3's JSON loader
// will map template strings onto these enums behind a single seam.

/// Castable abilities in the simplified-Affliction roster.
enum AbilityId {
  agony,
  corruption,
  shadowBolt,
  unstableAffliction,
  haunt,
}

/// Target debuffs (damage-over-time effects + Haunt's damage amp).
enum DebuffId {
  agony,
  corruption,
  haunt,
}

/// Player auras / procs.
enum AuraId {
  nightfall,
}

/// Player resources.
enum ResourceId {
  soulShard,
}

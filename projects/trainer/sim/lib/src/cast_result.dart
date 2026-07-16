/// How an accepted cast resolved.
enum CastResolution { instant, castStarted, channelStarted }

/// Why a cast was rejected. M2 maps these to per-button "why is this dim?"
/// affordances. Backed by the same `_validate` as [CastResult] so `cast()`
/// and `canCast()` can never disagree.
enum CastRejectReason {
  gcdActive,
  alreadyCasting,
  channeling,
  onCooldown,
  insufficientResource,
  unknownAbility,
}

/// Result of attempting a cast. `cast()` never throws — it returns one of
/// [CastAccepted] or [CastRejected].
sealed class CastResult {
  const CastResult();

  bool get accepted => this is CastAccepted;
}

final class CastAccepted extends CastResult {
  const CastAccepted(this.kind);

  final CastResolution kind;

  @override
  String toString() => 'CastAccepted($kind)';
}

final class CastRejected extends CastResult {
  const CastRejected(this.reason);

  final CastRejectReason reason;

  @override
  String toString() => 'CastRejected($reason)';
}

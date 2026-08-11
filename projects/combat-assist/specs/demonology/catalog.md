# Demonology Warlock — pilot catalog

**Applies to:** Demonology (specID 266), Diabolist (hero tree 59), Midnight 12.0.7.
This is a provisional product characterization for play, not a claim that the rules are
universally correct. `../spec.md` §3.4 owns the intended experience.

## Bound abilities

| Key | Ability | Spell ID | Why cap binds it |
| --- | --- | ---: | --- |
| `tyrant` | Summon Demonic Tyrant | `265187` | enhanced entry and independent bar |
| `dreadstalkers` | Call Dreadstalkers | `104316` | readable Tyrant context |
| `grimoire` | Grimoire: Imp Lord / Fel Ravager | `1276452` / `1276467` | readable Tyrant context |
| `demonbolt` | Demonbolt | `264178` | enhanced entry |

Only Tyrant and Demonbolt are enhanced entries. The other two are readable dependencies;
they do not receive cap pixels of their own. All other CDM rows are unclaimed and valid.

## Pilot hypotheses

### Tyrant

- Emphasize while the Tyrant row is readable as ready.
- Show a left blue Dreadstalkers dot while the Dreadstalkers cooldown is running.
- Show a right purple Grimoire dot while its CDM row is transformed.

The dots state only those readable facts. In particular, neither dot claims that a summoned
pet is still active: Dreadstalkers' cooldown outlasts the dogs, and Grimoire's transformed row
outlasts its summon. The flight asks whether these honest commitment facts are useful setup
context or too stale to earn pixels.

### Demonbolt

- Emphasize while Blizzard exposes its proc state as active.
- Vary the one treatment's alpha from readable Soul Shards: fewer shards produces stronger
  emphasis; more shards produces weaker emphasis.

There is no tier threshold. The flight decides whether this adds useful overcap context while
remaining distinguishable from Blizzard's stock proc glow.

### Tyrant bar

One independent bar asks the client to draw Tyrant's remaining cooldown. It does not inherit
the icon's emphasis or either context dot. `../spec.md` §3.3 owns its safe-state semantics.

## Contract boundary

Lua conditions use only `ready`, `proc`, `identity`, and readable Soul Shards. Unknown never
becomes confidence, including through negation. The catalog declares no sealed display form,
silence list, tier, cue, elapsed counter, cast sequence, coverage rule, or future vocabulary.

# Demonology Warlock — pilot catalog

**Applies to:** Demonology (specID 266), Diabolist (hero tree 59), Midnight 12.1.
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

This is the canonical readable-readiness tier example; its dots are the canonical readable
fact-to-marker example.

- Put Tyrant in COOLDOWN while its row is readable as ready.
- Show a left blue Dreadstalkers dot while the Dreadstalkers cooldown is running.
- Show a right purple Grimoire dot while its CDM row is transformed.

The dots state only those readable facts. In particular, neither dot claims that a summoned
pet is still active: Dreadstalkers' cooldown outlasts the dogs, and Grimoire's transformed row
outlasts its summon. The flight asks whether these honest commitment facts are useful setup
context or too stale to earn pixels.

### Demonbolt

This is the canonical readable proc-plus-secondary-resource example.

- Put Demonbolt in ROTATION while Blizzard exposes its proc state as active.
- Use the readable Soul Shard count as a cue that **dims** the proc above three shards, where
  spending it would overcap.

The flight decides whether the discrete dim adds useful overcap context while remaining
distinguishable from Blizzard's stock proc glow.

### Tyrant bar

One independent bar asks the client to draw Tyrant's remaining cooldown. It does not inherit
the icon's emphasis or either context dot. `../spec.md` §3.3 owns its safe-state semantics.

## Contract boundary

Lua conditions use only `ready`, `proc`, `identity`, and readable Soul Shards. Unknown never
becomes confidence, including through negation. The catalog declares no continuous grade,
sealed display form, silence list, cue, elapsed counter, cast sequence, coverage rule, or
future vocabulary.

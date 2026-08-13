# Destruction Warlock — authoring proof catalog

**Applies to:** Destruction (specID 267), Diabolist (hero tree 59), Midnight 12.1.
This is a provisional product characterization for play, not a universal rotation claim.
`../spec.md` §3.5 owns the intended experience.

## Declared abilities

| Key | Ability | Spell ID | Why cap declares it |
| --- | --- | ---: | --- |
| `conflagrate` | Conflagrate | `17962` (`91591` CDM alternative) | enhanced charged entry |
| `backdraft` | Backdraft aura | `117828` | sealed display dependency only |

Only Conflagrate needs a CDM row. Backdraft is selected declaratively by Blizzard's
AuraContainer and never becomes a readable dependency or an enhanced entry.
Blizzard's native Conflagrate count and cooldown swipe remain untouched; the estimate drives
only CAP's broad availability tier.

## Provisional hypotheses

- Put Conflagrate in ROTATION when the charge estimate is above zero.
- Use the readable Soul Shard count as a cue that **dims** it above four shards.
- Withhold the tier entirely when charged readiness is zero or unknown.
- Independently ask Blizzard to display Backdraft's application count at two stacks in a
  static outlined marker. It supplies context and does not change the tier.

The charge estimate starts from exact out-of-combat `currentCharges`, `maxCharges`, and
positive recharge duration. Successful Conflagrate casts debit it; non-duplicate
`ChargeGained` alerts credit it; combat end replaces it with the next exact client seed.
Captures label the exact state `live` and the maintained state `napkin`.

## Contract boundary

Soul Shards and estimated charged readiness are readable tier inputs. Backdraft applications
are sealed: AuraContainer owns acquisition and writes the count to its FontString sink. CAP
does not compare, type-check, read back, or report the secret-driven text.

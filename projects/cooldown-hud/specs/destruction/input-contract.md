# Input contract — Destruction APL evaluator

> **⚠ STATUS: reference / specification.** There is no standalone evaluator module —
> the shipped logic lives in `Coach.lua` (`RankWinner`), and `Coach.Context` is what
> gathers these inputs from the State pulse. Read this as the **specification of the
> inputs** the Destruction priority list needs, exactly as
> `specs/demonology/input-contract.md` does for Demonology. `rotation.md` remains the
> rotation spec of record.

This describes precisely what information the priority list needs, one field per real
rotation fact the list reads. The evaluation is pure: it walks the list in
`rotation.md` top-to-bottom and returns the winner + a second-place recompute. It does
**no** observation of its own — the caller produces every field below from live state.

Design principle: **minimal and rotation-grounded.** Every field maps to exactly one
fact the list reads. No field encodes a Backdraft *count*, a Wither *stack*, or a
*target count* — all three are unreadable (see notes).

## KB grounding

Ability names, shard costs/yields, and the Infernal / Diabolic Ritual / Backdraft
relationships were checked against the WoW knowledge base (not any addon):

- `knowledge/classes/warlock/destruction/rotation.md` — the distilled Tier-1 simc APL:
  the shard economy, Chaos Bolt as the payoff spender, the fire DoT as maintenance,
  Summon Infernal as the burst window everything syncs to, the Diabolist
  Ritual → Art → Ruination cycle, Infernal Bolt as the shard-refill builder.
- `knowledge/classes/warlock/destruction/abilities.md` — canonical names, resource
  costs (CB 2 / RoF 3 / Shadowburn 1), the charge counts on Conflagrate and
  Shadowburn, and the fragment-granularity resource note.
- `wowkb.spec_inventory --spec Destruction` + `raw/wago/SpellName.csv` @ 12.0.7 — the
  spell IDs in `notes.md`, and the two structural findings (Immolate tracked as the
  DoT aura `157736`; Incinerate absent from the union).

## The input table

A single flat table of plain data (numbers / booleans). Fields:

| Field | Type | Default | Meaning / rotation concept | Read by |
|---|---|---|---|---|
| `shards` | number (0–5) | `0` | **Projected** Soul Shards: live count **plus shards in flight** from an unlanded cast. ⚠ Destruction generates in *fragments*; if only the whole-shard read is available this is an integer and the list's rounded gates apply (`rotation.md` → Fragments). | L2, L4, L6, L10, L12 |
| `ruination_up` | boolean | `false` | The Diabolist Ruination proc is armed — it **auto-replaces Chaos Bolt** on the button. "if Ruination" = armed **and** therefore castable. *(Diabolist only.)* | L1 |
| `soulfire_usable` | boolean | `false` | Soul Fire is off cooldown (~45 s) and castable. Talent — `false` on a build without it, which correctly makes L2 dead. | L2 |
| `art_armed` | boolean | `false` | A **Demonic Art** proc is present — the empowerment Chaos Bolt is meant to spend. Presence only; there is no Art *count*. *(Diabolist only.)* | L3 |
| `cb_usable` | boolean | `false` | Chaos Bolt is affordable (2 shards) and not locked out. The list's main spender; appears at **both** L3 and L11, so second-place computation must suppress both. | L3, L11 |
| `conflagrate_usable` | boolean | `false` | Conflagrate has **at least one charge banked** and is castable. ⚠ Until the charge read lands this degrades to plain "off cooldown" — see the notes. | L4 |
| `backdraft_present` | boolean | `false` | A Backdraft buff is present. **Presence, never a count** — the stack count is secret, so L4's simc gate ("not stacked to 2") is approximated by "not present at all". Deliberately stricter than simc. | L4 |
| `infernal_castable` | boolean | `false` | Summon Infernal is off cooldown (120 s base / 90 s with Inferno). The burst window in its entirety — no partner, no lead-time window field (contrast Demonology's `tyrant_window`). | L5 |
| `chaotic_inferno` | boolean | `false` | The Chaotic Inferno buff is present, arming the empowered Incinerate at L6. Presence only. | L6 |
| `incinerate_usable` | boolean | `true` | Incinerate is castable. No cooldown / no cost, so defaults `true`; `false` only if genuinely locked out. It is the list's **floor**. | L6, L13 |
| `shadowburn_usable` | boolean | `false` | Shadowburn has a charge banked and 1 shard is affordable. Same charge caveat as Conflagrate. | L7 |
| `fiendish_cruelty` | boolean | `false` | The Fiendish Cruelty buff is present — one of the two things that make Shadowburn the press. Presence only. | L7 |
| `target_execute` | boolean | `false` | The current target is at **≤ 20 % health** (the Shadowburn execute gate). ⚠ *Not* a Secret Value — ordinary unit data that is simply **not in the State pulse today**. Default `false` = never claims execute. | L7 |
| `dot_refreshable` | boolean | `false` | The maintenance fire DoT (**Immolate**, or **Wither** on Hellcaller) is **missing or inside its pandemic refresh window**. The spec's spine and its biggest open input — blocked on `abilities[base].uptime`. Default `false` means L8 never fires, which is honest but leaves the DoT unmanaged. | L8 |
| `cataclysm_usable` | boolean | `false` | Cataclysm is off cooldown (~30 s) and talented. | L9 |
| `aoe_mode` | boolean | `false` | The manual target-mode toggle (`Mode.lua`: `single`/`multi`/`aoe`) reads AoE. **Stands in for a target count we cannot read** — Rain of Fire's real gate is ~8+ targets (Diabolist) / 5+ (Hellcaller). | L10 |
| `rof_usable` | boolean | `false` | Rain of Fire is affordable (3 shards) and castable. | L10 |
| `ib_usable` | boolean | `false` | Infernal Bolt is armed — the Diabolist **Incinerate** replacement (generates more shards). The list casts it only at `shards <= 3` as the refill. *(Diabolist only.)* | L12 |

Any field omitted takes its default. Omitting a usability boolean therefore means
"that ability is not usable" — the safe reading of an unknown fact.

**Hellcaller:** `ruination_up`, `art_armed` and `ib_usable` are permanently `false`
(those abilities do not exist on the tree), and a `malevolence_castable` field joins
the table beside `infernal_castable`. `dot_refreshable` reads Wither instead of
Immolate — the same field, a different source.

## The derived / ambiguous facts, called out

- **Projected `shards`** — the caller folds *in-flight* shards into the number.
  Destruction's **spender** side is clean whole numbers (CB −2, RoF −3, Shadowburn −1),
  so the negative half of `State.lua`'s in-flight projection and its double-deduction
  guard transfer from Demonology unchanged. The **builder** side is fractional and is
  the part that needs the fragment read before it can be projected honestly.

- **Presence, never counts — three times over.** `backdraft_present`,
  `chaotic_inferno` and `fiendish_cruelty` are all yes/no. Backdraft is the one where
  that costs fidelity (simc wants "not at 2 stacks"); the other two are genuinely
  binary arms, so nothing is lost there.

- **No window field.** Demonology needs `tyrant_window` (a ~3 s lead so the setup
  sequence can run) *and* `tyrant_castable`. Destruction needs **only**
  `infernal_castable`: nothing is staged for the Infernal, nothing is held, so there
  is no setup block to open early. If a "pool shards before Infernal" behaviour is
  ever wanted, that is the field to add — and it should be added deliberately, not
  inferred.

- **`target_execute` is a missing input, not a blind spot.** Worth stating plainly
  because it reads like the Demonology imp-count case and is not: target health
  percent is ordinary readable unit data. It is absent because the State pulse has no
  target channel at all, so adding it is a State change with a real cost (a new
  observed thing, per pulse), not an impossibility.

- **`dot_refreshable` is the one field that gates a whole line to dead.** Defaulting
  it `false` is the honest reading, and it means L8 never fires until
  `abilities[base].uptime` exists. Do **not** approximate it from cast history — a DoT
  refreshed by Soul Fire, spread by Cataclysm, or ticking on a target that died is not
  reconstructible from "I cast Immolate 14 s ago."

- **Havoc is deliberately not a field.** Its gate is `target_if` over a target roster
  with time-to-die, which the pipeline does not have. It should be surfaced the way
  Demonology surfaces Implosion — `judgeable = false` with a stated `secretGate`
  ("which add, and how long it lives — your call"), capping at AVAILABLE and never
  claiming the press. Channel Demonfire is parked the same way pending a settled build.

## Return shape

`evaluate(state)` returns:

```lua
{
  winner = { ability = <string>, rule = <string>, why = <string> },
  second = { ability = <string>, rule = <string>, why = <string> },
}
```

- `ability` — e.g. `"Chaos Bolt"`, `"Summon Infernal"`, `"Incinerate"`.
- `rule` — the matched line identifier (`"L1"`, `"L7"`, `"L11"`, …) so the result is
  auditable, not an oracle.
- `why` — a human-readable reason string.
- **Nothing castable:** if no line fires, that slot is `{ ability = nil, rule = "none",
  why = ... }`. In practice the winner is always castable — Incinerate at L13 is the
  floor — so the nothing-castable result shows up mainly as *second* place.

### Second place — how it is computed

Second place is **not** "the next line after the winner." The evaluator removes the
winner's *ability* from consideration **everywhere it appears** and re-evaluates from
the top. Destruction makes this sharper than Demonology, because two abilities are
each on two lines:

- **Chaos Bolt** at L3 (spend an Art proc) and L11 (the main dump). Removing it must
  suppress both, or a Ruination-less Art press "falls through" to itself.
- **Incinerate** at L6 (Chaotic Inferno) and L13 (the floor). Removing it usually
  leaves *nothing* — which is the correct answer, and exactly the case the
  nothing-castable second place exists for.
- Previously-skipped branches become reachable: if the winner is Chaos Bolt via L3,
  removing it lets L4's Conflagrate (or L12's Infernal Bolt at low shards) surface as
  the honest "what would I press instead."

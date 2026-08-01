# Destruction — spec facts

> The Destruction-specific instantiation of the general design (`docs/design.md`) and
> pipeline (`docs/architecture.md`). The rotation itself is `rotation.md` (the flat
> priority list); this file is the surrounding facts — the tracked set, the resource
> model, the burst window, the transforms, and the blind spots. v1 profile:
> **Diabolist** (Hellcaller deltas are marked inline).

> **⚠ Everything below is DESK-DERIVED, not observed.** Demonology's tracked set was
> confirmed off a live `/cdmp hud status`; no Destruction character has been captured.
> **The IDs here are now shipping** in `SpecDestruction.lua` (2026-07-29) — which makes
> `/cdmp hud layout` on a Destruction character the way to check them, rather than a
> prerequisite for writing them. See `docs/status.md` → *Open items* for that checklist.
>
> **Two predictions below were superseded by the implementation.** The resource section's
> "`resourceDisplay` needs a third member" did **not** happen — State cannot read the
> fraction anyway, so the spec renders `discrete` and projects spenders only. And the
> "`ns.SpecShardDelta` stops being an integer table" worry resolved the other way: the
> table carries **no** `generates` field at all. Details in `docs/status.md`.
> The set below is the **candidate pool** from game data (`wowkb.spec_inventory
> --spec Destruction`, which unions the talent tree ∪ class kit ∪ CooldownSetSpell
> residue) — the *live* set is talent-filtered and will be a strict subset. **Confirm
> with `/cdmp hud status` on a Destruction character before trusting any of it.**

## Candidate tracked set (predicted — verify in game)

Spell IDs are Tier-1: `wowkb.spec_inventory --spec Destruction` reconciled against
`raw/wago/SpellName.csv` @ 12.0.7.

**Essential (the rotation buttons) — the likely core:**
Chaos Bolt `116858`, Conflagrate `17962`, Shadowburn `17877`, Immolate `157736`,
Rain of Fire `5740`, Soul Fire `6353`, Cataclysm `152108`, Summon Infernal `1122`,
Havoc `80240`, Channel Demonfire `196447` · *(Hellcaller)* Malevolence `442726`

**Utility — class-shared with Demonology, so the same seven-ish shape:**
Unending Resolve `104773`, Dark Pact `108416` (defensives); Shadowfury `30283`,
Howl of Terror `5484`, Mortal Coil `6789`, Blight of Tongues `1271802`,
Command Demon `119898` (CC); Demonic Circle: Teleport `48020` (mobility)

**Buffs — the proc/aura inputs:**
Diabolic Ritual `428514`, Backdraft `117828`, Chaotic Inferno `1244860`,
Fiendish Cruelty `1245664`, Alythess's Ire `1244947`, Lake of Fire `1244918`,
Backlash `387384`, Flashpoint `387263`

> **Crashing Chaos `417234` is deliberately NOT in the addon's roster** (removed
> 2026-07-31, roster-state-plan Phase 4). The CDM tracks it in **zero** rows, so there is
> no `IsActive()`, no aura frame and no alert edge — and in combat no fallback channel
> exists either (`C_UnitAuras` is fully secret; `COMBAT_LOG_EVENT_UNFILTERED` errors on
> registration). What it would tell us is a **shard-cost change**, which the brain already
> reads live through `ns.ShardCost`. Redundant rather than blind.

Three facts this already settles:

- **Immolate is tracked as `157736`, the DoT aura — not `348`, the cast.** Both names
  resolve to "Immolate" in `SpellName`. The cooldown-set data carries the aura ID,
  which is *good news*: a tracked aura is where a duration/uptime read would come
  from (see blind spots). But it means the registry entry, the keybind resolution and
  any cue must be keyed off `157736`, and `348` needs mapping as an alias — exactly
  the Imp Lord `1276452` vs `136726` problem `SpecDemonology.lua` already solves.

- **Incinerate is absent from the union entirely.** The spec's *bottom-line filler* —
  the ability the whole priority list falls through to — does not appear in the talent
  tree, the class-kit skill line, or the cooldown-set residue for Destruction. If that
  reflects the live CDM set, then **Destruction's floor press has no icon**, which is
  Demonology's Shadow Bolt situation but on a far more frequently pressed button.
  `@verify-ingame` — this is the single most important thing to check first, and if
  confirmed it is a strong argument for the curated layout override parked in
  `docs/status.md`.

- **The Diabolist proc IDs are NOT Demonology's.** `SpellName` carries three
  "Ruination" IDs (`433885`, `434635`, `434636`) and two "Infernal Bolt" (`433891`,
  `434506`). Demonology **confirmed live** `434635` / `434506` off the probe.
  Destruction's cooldown-set residue names **`433885` / `433891`** — i.e. the entries
  `SpecDemonology.lua` currently labels *"alt ID, unconfirmed"* are most likely the
  **Destruction-side** IDs. A `SpecDestruction.lua` must therefore not inherit Demo's
  confirmed pair. `@verify-ingame`.

## The resource model — fragments, and why it is a different rail

This is the headline difference from Demonology and the reason the backlog called
Destruction "the first real exercise of the general↔spec split."

- Demonology's rail is **5 discrete shards**; every generator pays out whole shards
  (Shadow Bolt +1, Demonbolt +2, Infernal Bolt +3), so `SpecShardDelta` is an integer
  table and the bar is five segments.
- Destruction **spends** in whole shards — Chaos Bolt 2, Rain of Fire 3, Shadowburn 1 —
  but **generates in fragments (tenths)**: Incinerate, Conflagrate, Soul Fire and
  *Immolate ticks* each pay a fraction. The bar is conventionally drawn as 5 segments
  with partial fill. This is why the simc APL gates read `soul_shard<=4.2` /
  `>=3.5` instead of integers.

Two consequences the pipeline has to absorb:

1. **`ns.SpecShardDelta` stops being an integer table.** A Destruction spec table
   either carries fractional `generates` values or declines to project builders at
   all. Note the *spender* side is still clean whole numbers, so the negative half of
   the in-flight projection (the double-deduction guard in `State.lua`) transfers
   unchanged.
2. **`resourceDisplay` needs a third member.** `guidance-contract.json` enumerates
   `discrete` (whole segments) and `percentage` (continuous fill), and explicitly
   leaves the door open: *"Enumerate additional forms as later specs need them."*
   Destruction is that need — segments **with** partial fill is neither existing
   member. This is a contract edit, and it is the one place adding this spec touches
   a **general** artifact rather than staying additive.

Whether the fragment value is even *readable* is a separate question — see
`observability-map.md` → *the fragment read*. Today `State.lua` calls
`UnitPower("player", pt)` with no unmodified flag, which returns whole shards only.

## The burst window = Summon Infernal

Demonology's window is Tyrant + Dreadstalkers as a **common-fate go-gate** — two
buttons that brighten together. Destruction's is **structurally simpler and weaker as
a HUD cue**:

- **Summon Infernal (120s base; 90s with Inferno) is the whole window.** There is no
  second summon to line up with it. Everything that syncs to it — potion, racials,
  trinkets, external Power Infusion — is **off-GCD or not ours to cue**, so a go-gate
  in the Demonology sense has only one member.
- **The alignment rule is "hold for adds", not "hold for a partner."** The KB is
  explicit: if important adds are about to spawn, pool shards and *delay* Infernal.
  That is a fight-knowledge judgment the HUD cannot make, so Infernal should read as a
  strong on-cooldown press and never as a hold.
- ***(Hellcaller)*** **Malevolence (~60s) deliberately does NOT align** with Infernal
  (120s / 90s) — the KB says only line them up on a fight's final casts, and otherwise
  press Malevolence on cooldown. So even on Hellcaller the two burst buttons are two
  independent on-cooldown lines, **not** a paired gate. Do not build a Tyrant-style
  common-fate treatment here; it would be wrong roughly every other window.

The Demonology `stage` bit (hold this so it lands *inside* the window) has **no
Destruction analogue**. Nothing is held for Infernal.

## Transforms, procs and charges

**Demonic Art transforms** (Diabolist), directly observable via
`COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED`:

| base | override | note |
| --- | --- | --- |
| `116858` Chaos Bolt | Ruination (`433885`?) | CB is tracked → **glowable** |
| `29722` Incinerate | Infernal Bolt (`433891`?) | Incinerate appears untracked → **no icon to glow** (blind spot) |

The same asymmetry as Demonology (HoG glows, Shadow Bolt cannot), rotated onto
Destruction's two buttons. Identity keyed on *ability* resolves off the **base**
spellID falling back to the override, never the reverse.

**Procs (presence readable, counts not):**

- **Backdraft `117828`** — faster Incinerate/Chaos Bolt casts, **2 stacks**. Gates
  Conflagrate in the APL. Presence readable, stack count secret.
- **Chaotic Inferno `1244860`** — arms an instant/empowered Incinerate (APL L6).
- **Fiendish Cruelty `1245664`** — arms Shadowburn (APL L7).
- **Diabolic Ritual `428514`** — the Demonic Art container, same as Demonology.
  ⚠ Demo found this tracked **twice** under two cooldownIDs sharing one spellID;
  expect the same, and expect the registry to be keyed on **cooldownID, not spellID**.

**Charges — new to this project.** Conflagrate and Shadowburn are both 2-charge,
~12–13s recharge. Demonology has no charged tracked ability, which is why the
`charge` half of the full-database read sits `@verify-ingame` in `docs/status.md`.
**Capturing a Destruction probe closes that open item** — it is the first spec that
can.

## Colour members (reference — v1 does not colour by group)

v1 colours by **urgency (`emphasis`), not ability group**. Retained only as reference
for a possible future group-colour mode, and to show which Demonology hues carry over:

| Group | Members |
| --- | --- |
| Summon (burst) | Summon Infernal · *(Hellcaller)* Malevolence |
| Core fire damage | Chaos Bolt, Incinerate, Conflagrate, Soul Fire, Immolate/Wither |
| Fel explosion / AoE | Rain of Fire, Cataclysm, Channel Demonfire |
| Proc / resource | Backdraft, Chaotic Inferno, Fiendish Cruelty, Soul Shard rail accent |
| Defensive | Unending Resolve, Dark Pact |
| CC | Shadowfury, Howl of Terror, Mortal Coil, Command Demon |
| Mobility | Demonic Circle: Teleport |

Note the `summon` hue (fel green) carries **one** member here, and the `aoe` hue picks
up three. Demonology's balance was the reverse.

## Blind spots — what we cannot assist for Destruction

Beyond the general Secret-Values wall (`architecture.md` → Blind spots):

- **Immolate / Wither uptime — the spine of the spec.** "Is the DoT up, and is it in
  the pandemic window" is the single most important Destruction call and the pipeline
  does not surface it today. Unlike Demonology's imp count this is **not** a hard
  capability limit: the DoT is tracked as a buff/bar item (`157736`), so a duration
  read is plausible — it is the `abilities[base].uptime` backlog item in
  `docs/status.md`. **Until that lands, L8 cannot fire honestly.**
- **Backdraft stack count** (the Conflagrate gate) — presence readable, count secret.
  Same wall as Demonic Core.
- **Wither stack count** *(Hellcaller)* — the 8-stack Blackened Soul threshold is
  unreadable. Maintenance only; never play around the stacks.
- **Target count** — Rain of Fire's real gate is a target count (~8+ Diabolist, 5+
  Hellcaller). The HUD has only the manual `single`/`aoe` mode toggle, so RoF is
  mode-gated, never count-gated.
- **Havoc's target selection** — `target_if` over a roster with time-to-die. No roster,
  no TTD; Havoc can only ever be a "your call" availability.
- **Charge counts** — pending the `charge` read (above), Conflagrate/Shadowburn read as
  binary off-cooldown, so the HUD will under-press rather than dump a banked charge.
- **Target health % (the 20% execute gate)** — *not* secret, just **not in the State
  pulse**. A missing input, not a blind spot.

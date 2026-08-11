---
title: Vengeance Demon Hunter — Talents & Builds (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes — CLASSES ▶ DEMON HUNTER ▶ Vengeance
  - ../../../_meta/patch-notes/12.1.md  # tier 1, verbatim archive of the above (Vengeance block + the four global CLASSES changes)
  - ./talents.md  # tier 1, generated from Blizzard Game Data API + wago Trait* DB2 @ 12.1.0.68914 — node rows/cols, choice pairs, Sigil of Chains verified ABSENT
  - ./talents.json  # tier 1, same generation — point budgets, granted (free) hero nodes, max_ranks
  - ./ability-inventory.md  # tier 1, wago DB2 + Blizzard spell API @ 12.1.0.69214 — the FRESHEST tooltip text; beats talents.json where they disagree
  - https://maxroll.gg/wow/class-guides/vengeance-demon-hunter-raid-guide  # tier 3 (./maxroll-raid.md) — maxroll_updated 2026-08-11, body carries a 12.1 note block, but the capture's own front matter still reads patch: 12.0.7 (not re-stamped); treat as mixed-era
  - https://maxroll.gg/wow/class-guides/vengeance-demon-hunter-mythic-plus-guide  # tier 3 (./maxroll-mplus.md) — same: maxroll_updated 2026-08-11 with a 12.1 note block, front matter still patch: 12.0.7
  - simc midnight branch profiles/MID1/MID1_Demon_Hunter_Vengeance.simc  # tier 1 but PRE-12.1 (12.0.7) — its talent string predates the 12.1 node moves
  - https://www.method.gg/guides/vengeance-demon-hunter/talents  # tier 3, 12.0.7 — pre-12.1, hero-tree framing only
  - https://www.icy-veins.com/wow/vengeance-demon-hunter-pve-tank-spec-builds-talents  # tier 3, 12.0.7 — pre-12.1
confidence: medium
---

# Vengeance Demon Hunter — talents & builds (Midnight 12.1)

Layers on the generated talent tree in `talents.md` (do not regenerate that
file — this is the narrative on top of it). Node names, spell IDs, ranks and
tree positions live there and in `ability-inventory.md`; **those files are Tier 1
and win over anything below.** Point budget at level 90: **34 class / 34 spec /
13 hero**.

## What 12.1 changed for builds

- **Sigil of Chains is baseline at level 35 and is no longer a talent** —
  verified absent from the live tree in `talents.md`. Its cooldown is **60s (was
  90s)** and it **no longer replaces Sigil of Misery**; **Sigil of Silence**
  replaces Sigil of Misery when you take it. **Improved Sigil of Misery** (class
  tree, 3,6) no longer touches Sigil of Chains — it now cuts **Sigil of
  Silence's cooldown by 15s** when Sigil of Silence is selected. Net: the pull-
  and-grip tool is free, and the Improved-Sigil node only pays off if you spend
  the spec point on Sigil of Silence.
- **Fracture and Soul Cleave now require equipped Warglaives, Axes, Swords or
  Fist Weapons.** A gearing constraint, not a talent one, but it invalidates any
  "just equip whatever" advice (see `gearing.md`).
- **Survivability up across the board** — these shift the value of the sustain
  cluster relative to throughput picks: Soul Cleave, Fel Devastation and **Feast
  of Souls** healing all **+25%**; **Charred Warblades 5%** of Fire damage (was
  4%); **Frailty 10%** of damage dealt to afflicted targets (was 8%); **Revel in
  Pain shields for 6%** of Fire damage (was 5%). ⚠ The Tier-3 maxroll captures
  in this directory still print **Frailty at 8% / 16%** — that is stale; the
  Tier-1 patch notes are the floor.
- ⚠ **Tier-1 vs Tier-1 conflict — Charred Warblades.** The 12.1 patch notes say
  **5% (was 4%)**; the DB2/API tooltip at build **12.1.0.69214**
  (`ability-inventory.md`, spell `213010`, 1 rank) still reads **3%**. We keep the
  **patch-note 5%** — the Tier-1 feed is the floor and the notes are the newer
  statement — but the generated tooltip has not caught up, so the number is not
  yet corroborated by game data. Same shape as the Final Hour 8s-vs-6s and World
  Killer conflicts below. @verify-ingame
- **All damage +5.5%.**
- **Several talents changed tree locations.** Treat every pre-12.1 import string
  as suspect (see the reference-strings section).
- **Global, every spec:** player health **and** creature damage **+25%** at max
  level (health consumables rescaled; several tank healing/absorb effects retuned
  to match — so any absolute HP or heal number written before 2026-08-11 is
  wrong); major DPS cooldowns lowered with steady-state damage raised;
  interrupts now show a **"missed"** visual + sound when the target wasn't
  casting; **diminishing-return categories now reset after 20s (was 16s)** —
  that last one directly changes Chaos Nova / Sigil of Misery / Imprison chaining
  in M+.

## Hero tree: Annihilator is the 12.1 default

Vengeance's two Midnight hero trees are **Aldrachi Reaver** and **Annihilator**.
**Annihilator is Midnight-new** — it replaces The War Within's *Fel-scarred*
tree (Fel-scarred is gone for Vengeance; don't cite pre-Midnight Fel-scarred
guides). The 12.0.7 read was "both close"; the **12.1-era Tier-3 guidance
(maxroll, updated 2026-08-11) recommends Annihilator for both raid and average
Mythic+** — more single-target damage, better overall survivability, easier snap
threat. **No 12.1 sim has been captured**, so treat this as a Tier-3 lean, not a
measured gap. Aldrachi Reaver remains playable and rewards tighter execution.

⚠ **Reading the generated hero-node tooltips.** Both hero trees are shared with a
DPS spec, and the text in `talents.md` / `ability-inventory.md` renders with
**that** spec's ability names: Annihilator nodes read in **Devourer** terms
(Consume, Reap, Void Metamorphosis, Void Ray, Collapsing Star) and Aldrachi
Reaver nodes in **Havoc** terms (Shear, Blade Dance, Chaos Strike). For
Vengeance the mapping is builder = **Fracture** (which replaces Shear), spender =
**Soul Cleave / Spirit Bomb**, and **Metamorphosis** for the Meta lines. The
nodes whose Vengeance-facing wording is *not* obvious from that substitution —
**Meteoric Rise** and **Doomsayer** (Void Ray), **Dark Matter** and
**Otherworldly Focus** (Collapsing Star) — need their Vengeance text read off the
live tooltip. @verify-ingame

- **Aldrachi Reaver** — the **Reaver's Glaive** empower cycle. Consuming 20 Soul
  Fragments, or casting Sigil of Spite, converts your next Throw Glaive into
  **Reaver's Glaive**, which enhances your next **Fracture** and **Soul Cleave**:
  the first enhanced cast deals **+10%**, the second **+20%**. **Reaver's Mark**
  puts a **7% damage-taken debuff for 20s, max 2 stacks**, on the target (an
  extra stack when the enhanced cast follows Soul Cleave). **Aldrachi Tactics**
  shatters an extra fragment on the second enhanced ability; **Thrill of the
  Fight** (after consuming both enhancements) gives **+30% next Reaver's Glaive
  damage and +8% Haste for 30s**. **Art of the Glaive** is granted free (it is
  the tree's entry node). Key picks: Fury of the Aldrachi, Reaver's Mark,
  Aldrachi Tactics, Wounded Quarry, Warblade's Hunger, Incisive Blade, Thrill of
  the Fight; choice nodes **Evasive Action / Unhindered Assault** (Unhindered
  Assault = the Vengeful-Retreat→Felblade reset, the rotational pick) and **Army
  Unto Oneself / Incorruptible Spirit** (Incorruptible Spirit = +15% shield on
  every fragment consumed — the tank pick per maxroll). Nodes **Broken Spirit**,
  **Keen Edge** and **Bladecraft** read in Havoc terms and are Meta-cycle/Physical
  damage adders; confirm their Vengeance wording in game. @verify-ingame

- **Annihilator** — a **Voidfall** stack engine. **Voidfall** (free entry node):
  your builder (**Fracture**) has a **35%** chance to grant a stack; at **3
  stacks** your spender calls down a meteor for Cosmic AoE damage in 8 yards.
  **Meteoric Fall** upgrades that to consuming all 3 stacks for 3 rapid meteors.
  **Catastrophe** makes meteor-struck enemies take **+25% damage over 8s**.
  **World Killer** (capstone): the **third meteor in sequence is larger — +50%
  area, +50% damage, and generates 1 Soul Fragment**. ⚠ The Tier-3 maxroll
  capture instead claims World Killer reduces Metamorphosis' cooldown by 10s per
  third meteor; the Tier-1 tooltip @ 12.1.0.69214 says the bigger-meteor effect,
  and Tier-1 wins — the Meta-CDR line is either stale or a second, unlisted
  effect. @verify-ingame
  Defensive/throughput scaling comes from **Swift Erasure** (+2% Haste per stack)
  and **Phase Shift** (−2% damage taken per stack), held up by **Final Hour**
  (those per-stack bonuses persist **8s** after the stacks are consumed — note
  the 12.1 notes cut Devourer's Final Hour to 6s, but the Vengeance-facing
  tooltip at build 12.1.0.69214 still reads 8s). **Mass Acceleration** grants 3
  stacks + resets the spender on entering Metamorphosis. Choice nodes: **Path to
  Oblivion / State of Matter** and **Doomsayer / Harness the Cosmos** (Harness =
  flat +15% meteor damage, the safe pick). **Otherworldly Focus** is **+30%**
  meteor damage on a single target (was 35% pre-12.1), decaying 5% per extra
  target. Smoother to pilot: keep Fracture on cooldown, spend at 3 stacks, don't
  overcap, and cash the **Untethered Rage** Apex proc.

## The Apex talent — Untethered Rage

**Untethered Rage** (spec tree row 12, col 18, spell **1270444**, **1 rank** — a
Midnight-new **Apex** talent) sits alone at the bottom of the spec tree and is
the standout pick. Live 12.1 tooltip:

> Soul Cleave and Spirit Bomb have a chance per soul fragment consumed to grant
> Untethered Rage, allowing Metamorphosis to be cast without incurring its
> cooldown and lasting 10 sec.

So it is a **free, cooldown-free Metamorphosis** off fragment spending, which is
why the Annihilator loop is built around spending fragments aggressively and
jumping into Meta on the proc. ⚠ The pre-12.1 write-up here described a *rising*
proc chance, a 12s activation window, extra fragments consumed and a fragment
damage bonus at higher ranks — **none of that appears in the 12.1 tooltip and
the talent has only one rank**, so those claims are dropped rather than carried
forward. Whether the proc chance ramps with fragments spent is still unmeasured.
@verify-ingame

## Core spec + class talents (both builds)

The maintenance backbone is shared: the builder/spender core (**Fracture**,
**Spirit Bomb**, **Soul Cleave**), **Immolation Aura**, **Sigil of Flame**,
**Fiery Brand** + **Fiery Demise** (fire-damage amp window), **Fel Devastation**,
**Soul Carver**, **Sigil of Spite**, and the **Demon Spikes** mitigation
package. Near-universal picks:

- **Fragment / spender cluster:** Spirit Bomb, **Feed the Demon** (Demon Spikes
  uptime), **Frailty** + **Soulcrush** + **Painbringer** (mitigation from
  fragments — Frailty is a straight 12.1 buff to 10%), **Fallout** (Immolation
  Aura spawns fragments in AoE), **Soul Barrier / Soul Sigils** choice (spec
  7,20), **Focused Cleave**.
- **Fire / brand cluster:** **Fiery Demise**, **Charred Flesh** (Immolation Aura
  extends Brand — the reason Brand uptime is so high), **Down in Flames** (Fiery
  Brand gets **12s reduced cooldown and 1 additional charge** — the live 12.1
  tooltip, spell `389732`; `abilities.md` renders the result as **2 charges on a
  ~60s recharge**. The "45s cooldown" this file used to print was a pre-12.1
  carry-over from the old 15s-reduction wording and no Tier-1 cooldown datum
  supports it), **Stoke the Flames**, **Burning Blood**,
  **Darkglare Boon** (Fel Devastation cooldown reduction).
- **Sustain / defensive:** **Revel in Pain** (6% Fire→shield), **Roaring Fire**
  (spec 8,18 — Fel Devastation heals **up to 50% more** based on missing health;
  it is a plain passive, **not** a choice node against a sigil), **Ruinous
  Bulwark**, **Feast of Souls** (+25% healing in 12.1 — re-evaluate it, the old
  "underused" read is pre-buff), **Last Resort** (cheat-death), **Calcified
  Spikes** (Demon Spikes DR extension).
- **Class tree:** the mobility/CC/utility spine — **Vengeful Retreat**,
  **Felblade**, **Sigil of Misery**, **Chaos Nova**, **Consume Magic**,
  **Imprison**, **Darkness**, **Charred Warblades** (class 4,6 — 5% of Fire
  damage as healing per the 12.1 notes; ⚠ the 12.1.0.69214 tooltip still reads
  3% — see the conflict flagged above), **Master of the Glaive / Champion of
  the Glaive** (Throw Glaive charges), **Disrupting Fury** (Fury on interrupt),
  **Soul Rending** (2 ranks, leech — extra in Meta), **Blazing Path** (Infernal
  Strike charge).

**Sigil of Chains costs no talent point in 12.1** — it is baseline. Budget the
sigil points around **Sigil of Silence** (spec 6,18; it is the node that replaces
Sigil of Misery), **Chains of Anger** (sigil duration/radius) and **Cycle of
Binding** (−15% sigil cooldowns).

## Build split by content

- **Single target / raid:** lean the fragment-value + fire-amp clusters.
  Annihilator squeezes value from free Meta procs and meteor burst; Aldrachi
  Reaver leans on tight Reaver's Glaive cycles and Reaver's Mark uptime.
- **Mythic+ / AoE:** favor **Fallout** + **Spirit Bomb** throughput, the sigil
  cluster (**Sigil of Silence** for the ranged silence, plus baseline **Sigil of
  Chains** for pull control — now on a 60s cooldown, so it comes up nearly twice
  as often per pull) and **Charred Flesh** for extended Brand windows on big
  packs. Remember DR categories now reset at **20s**, not 16 — stun/disorient
  chains land differently.

## Reference talent strings

⚠ **Every pre-12.1 string is suspect: 12.1 moved talent node locations.** Import
strings encode node order, so a 12.0.7 string may fail to import or silently
land points somewhere else. Nothing here has been import-tested in game.
@verify-ingame

**Annihilator, raid** (Tier 3 — maxroll, 12.1 capture 2026-08-11):

```
CWkAIo1c2KfIEsPoy9fznypG4BAYMzMjZmZkZmZY2MzMjBjZGzYmZGDzYmx2MzsNGAAAAAAAIgZmxGAAAAGMmZmZWabmZGAAAAAgBA
```

**Annihilator, Mythic+** (Tier 3 — maxroll, 12.1 capture 2026-08-11):

```
CWkAIo1c2KfIEsPoy9fznypG4BAMjZmZmhZmMzMYWMzMDmZMzYGzMzYwMzM2mZmtxwAAAAAAAIgZwGAAAAGYmZmZ2abmZGAAAAAgBA
```

**Superseded — the 12.0.7 simc default (Tier 1 but pre-12.1; do not import):**

```
CUkAAAAAAAAAAAAAAAAAAAAAAAAYMzMjhZkZmZGDzMzMDGzMmxMmhxMmZsMmZZMmBAAAAAAAgZmxGAAAAGYmZmZ2abmZGAYAAAAMA
```

This was the Tier-1 reference at 12.0.7. The simc midnight branch has **not**
been re-pulled at 12.1, so there is currently no Tier-1 12.1 talent string for
this spec — the maxroll strings above are the working reference until
`wowkb.simc demon-hunter vengeance` is re-run.

## TODO

- [ ] Re-pull `wowkb.simc demon-hunter vengeance` once the midnight branch
      updates to 12.1, and replace the Tier-3 strings above with the Tier-1 one.
- [ ] Capture an Aldrachi Reaver 12.1 string (both maxroll builds above are
      Annihilator; no AR simc profile exists either).
- [ ] Add measured hero-tree DPS/survivability deltas once a Vengeance sims.md
      exists (mirror the Affliction sims.md pattern) — the Annihilator-over-AR
      call is currently Tier-3 assertion only.
- [ ] Resolve the World Killer conflict (Tier-1 bigger-third-meteor vs Tier-3
      Metamorphosis CDR) and the Final Hour 8s-vs-6s question in game.
- [ ] Resolve the **Charred Warblades** patch-note-5% vs tooltip-3% conflict —
      read the live in-game tooltip, then either confirm 5% or file the DB2
      value as the real one and correct both mentions here.
- [ ] Re-stamp `./maxroll-raid.md` and `./maxroll-mplus.md` — their bodies carry
      12.1 note blocks and `maxroll_updated: 2026-08-11`, but their front matter
      still reads `patch: 12.0.7`, so this file currently describes them as more
      current than they declare themselves to be.
- [ ] Re-run `wowkb.gen_verify` at the end of the sweep — this file's six
      `@verify-ingame` markers are not yet in `_meta/verify-in-game.md`.

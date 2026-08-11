---
title: Destruction Warlock — Ability Inventory (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes (CLASSES ▶ WARLOCK / Destruction), 2026-08-11
  - knowledge/_meta/patch-notes/12.1.md  # tier 1, verbatim archive of the above — lines 1159-1216 are the Warlock + Destruction block, 2026-08-11
  - knowledge/classes/warlock/destruction/ability-inventory.md  # tier 1, generated 12.1 inventory + resolved Blizzard Game Data API tooltips @ 12.1.0.69214, 2026-08-11
  - knowledge/classes/warlock/destruction/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.1.0.69214 — the name/spellID/origin/cooldown/CDM-category floor, 2026-08-11
  - knowledge/classes/warlock/destruction/talents.md  # tier 1, generated talent tree @ 12.1.0.68914 — node placement + choice partners, 2026-08-11
  - knowledge/classes/warlock/demonology/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.1.0.69214 — the cross-spec check on Secrets of the Coven 428518, 2026-08-11
  - knowledge/classes/warlock/destruction/gearing.md  # sibling, 12.1 — the Season 2 (Damned Necrolyte) set bonuses that replaced the Season 1 Conflagrate fragment bonus, 2026-08-11
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1, pet skill lines @ 12.0.7.67808, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warlock_Destruction.simc  # tier 1, simc midnight APL, 2026-07-11 — ⚠ pre-12.1, not yet re-pulled at the 12.1 SHA
  - raw/wago/SpellEffect.csv @ 12.0.7  # tier 1, energize effects -> the fragment yields, 2026-08-01 — carried forward; 12.1 changed no fragment yield
  - https://www.method.gg/guides/destruction-warlock  # tier 3, upd. 2026-06-16, 2026-07-11 — ⚠ pre-12.1
confidence: high
---

# Destruction Warlock — Abilities (Midnight 12.1)

> **12.1 "Curse of Ula'tek" (live 2026-08-11) — what moved on this spec.**
> **Conflagration of Chaos redesigned**: Conflagrate and Shadowburn now have a
> **100 % chance to critically strike, and their damage is increased by your crit
> chance** *[Tier 1, spell 387108 @ 12.1.0.69214]*. All Destruction damage **+4.5 %**,
> **Soul Fire +45 %**, **Chaos Bolt +5 %**. **Havoc now copies 50 %** of a
> single-target spell's damage onto the marked target (**was 60 %**) — a straight
> nerf to the 2-target cleave button. Cooldown Manager: **Shadowburn was ADDED as a
> tracked buff** and **Conflagration of Chaos was REMOVED** — confirmed in game data,
> where Shadowburn's Blizzard category reads `Buff/Essential` and Conflagration of
> Chaos's is now empty. Class-wide: **Drain Life drain +25 %**; **Summon Demonic
> Gateway is a Utility spell by default in the Cooldown Manager**; a large **Soul
> Leech correctness pass** — of the abilities in that list, the ones **Destruction
> actually has** are **Infernal Bolt**, **Wither**, **Avatar of Destruction's
> Chaos Bolt** and **Blackened Soul** (the Hellcaller mechanic, `440043`, on this
> spec's tree *[Tier 1, `ability-inventory.tsv` @ 12.1.0.69214]*), which now *do*
> grant Soul Leech, while **Channel Demonfire no longer erroneously does**. (Wicked Reaping `449631` is on the Affliction and Demonology
> trees only *[Tier 1, 12.1.0.69214]* — it is in the class-wide note but does not
> reach this spec.)
>
> **Four global 12.1 changes that land on every spec, this one included:**
> **(1)** player health **and** creature damage **+25 % at max level**, with health
> consumables rescaled and some DPS/Tank healing + absorb retuned — so *any* absolute
> HP or healing number written before 2026-08-11 is suspect, and the percentage
> healing values below were re-read from 12.1 game data rather than carried over.
> **(2)** Major DPS cooldowns lowered and steady-state damage raised across several
> specs — the burst/sustained split has moved even where per-ability numbers look
> familiar. **(3)** All class interrupts now show a **"missed" visual + sound** when
> fired at a target that was not casting (see the interrupt note below).
> **(4)** Diminishing-return categories now reset after **20 s** (was 16 s) — which
> lengthens the useful window on Shadowfury / Howl of Terror / Fear chains.
>
> ⚠ The 12.1 **PvP snare tier-down** (Curse of Exhaustion and Fel Fissure both to
> 30 %, was 50 %) is **PvP-only** and is deliberately not written into any row below.

## Overview

- **Resource:** **Soul Shards** — displayed 0–5, stored internally as **0–50
  fragments** (10 per shard; confirmed in-client 2026-08-01 via
  `UnitPowerMax("player", SoulShards, true)` = 50 against a displayed 5).
  Builders generate fragments; spenders — **Chaos Bolt** (2 shards / 20 frags),
  **Rain of Fire** (3 / 30), **Shadowburn** (1 / 10) — consume whole shards. The
  whole spec is a shard economy: never overcap, always be casting.

  **Yields, in fragments** (DB2 energize effects + tooltips; **re-checked against
  12.1.0.69214 — 12.1 changed no fragment yield on this spec**). ⚠ The *Modifiers*
  column is a **separate** claim from the yields and is not covered by that
  re-check: a **tier-set** modifier there is only current if `gearing.md`'s
  *Tier set — Midnight Season 2* section still carries it.

  | Ability | Base | On crit | Modifiers |
  |---|---|---|---|
  | Incinerate | 2 | +1 | **Diabolic Embers ×2 → 4** |
  | Conflagrate | 5 | — | — (no current set bonus; see note ↓) |
  | Immolate / Wither tick | 1 | +1 at 50 % | haste-scaled 3 s period |
  | Soul Fire | **10** (a full shard) | — | Havoc copy doubles |
  | Dimensional Rift | **3** | — | Soul Fire's choice partner |
  | Infernal Bolt | **20** (Destro) / 30 (Demo) | — | see below |
  | Shadowburn kill refund | 10 | — | — |
  | Infernal pet / Overfiend | 1 / sec | — | — |

  ⚠ **The Conflagrate `+2` is DEAD — it was the Season 1 (MID1) 4-set.** The
  Midnight **Season 1** Abyssal Immolator 4-piece read *"Conflagrate generates 2
  additional Soul Shard Fragments"*; **Season 2's set is a different set entirely**
  and carries no fragment bonus (Damned Necrolyte — **2-Set** *(Tier 3, from the
  maxroll capture — **not** Tier-1 corroborated; see the open TODO in `gearing.md`)*:
  Incinerate **+25 %** damage and **+10 %** chance to evoke Echo of Sargeras;
  **4-Set** *(Tier 1)*: targets damaged by Echo of Sargeras take **+6 %** damage from
  your spells for 6s, corroborated as **Dark Titan's Mark `1305711`**). See `gearing.md` § *Tier set — Midnight Season 2*. Nothing
  in 12.1 carries the Conflagrate fragment bonus forward, so **Conflagrate is a flat
  5 fragments** at Season 2.

  ⚠ **Infernal Bolt is 20 or 30 on Destruction and the sources disagree** — one
  reading has the spec aura `137046` (effect #13) applying −10 to Demonology's 30.
  **12.1 adds Tier-1 evidence against the "20 on Destro" reading**: the regenerated
  Destruction inventory's API-resolved description for **Secrets of the Coven `428518`**
  reads *"…dealing 5,119 Fire damage to your enemy target and **generating 3 Soul
  Shards**"* — **byte-identical to the Demonology row** for the same spell *[Tier 1,
  12.1.0.69214; `destruction/ability-inventory.tsv:152` vs
  `demonology/ability-inventory.tsv:144`]*. One shared description, one number, and it
  is 3 shards (30 fragments). That is not conclusive — a template redirect could still
  resolve per-spec at cast time, which a static description would never show — so the
  marker stays open, but the burden now sits on the 20 reading.
  @verify-ingame — cast one as Diabolist and watch the bar move 2 shards or 3.
- **Hero trees (Midnight):** **Diabolist** (default — best single target,
  competitive in stacked cleave; builds shards into Chaos Bolt and cycles
  **Diabolic Ritual → Demonic Art → free Ruination**) and **Hellcaller**
  (replaces Immolate with **Wither**, adds the **Malevolence** burst CD, **60s**
  `[T1]`). Choose the tree first — it changes the maintenance DoT and one major
  cooldown.

  ⚠ **12.1 reshaped Hellcaller and the old "sustained-AoE / long-fight pick"
  framing no longer describes it.** **Blackened Soul was redesigned** — on a target
  afflicted by your Wither, **Chaos Bolt and Shadowburn each add a Wither stack**, and
  every stack gain has a chance to *collapse*, consuming one stack per second for
  Shadowflame damage until 1 stack remains. **Blackened Soul damage +45 %** and
  **Wither damage +25 %**; **Mark of Peroth'arn redesigned** so Wither crits deal
  215 % (vs the usual 200 %) and Blackened Soul crits 225 %. Blizzard's stated intent
  is to give Hellcaller a **priority-target** tool rather than one that only excels on
  multiple targets — so it is now a plausible single-target pick, not just the AoE
  tree. **Malevolence is deliberately unchanged.**

  ⚠ **Diabolist: the 12.1 notes file its nerfs under Demonology, but at least one is
  the same spell Destruction uses — treat the Destruction-side impact as OPEN.**
  The notes list **Chaos Salvo / Felseeker / Wicked Cleave / Eye Explosion −20 %** and
  **Flames of Xoroth 3 % (was 4 %)** beneath the *Demonology* heading. However
  **Flames of Xoroth is spell `429657` in BOTH specs' Diabolist trees** *[Tier 1,
  12.1.0.69214]* — one spell, so a change to it cannot be Demonology-only. Likewise
  Chaos Salvo / Felseeker / Wicked Cleave are the attacks of the **Overlord, Mother of
  Chaos and Pit Lord**, and Destruction's Diabolist summons exactly those three demons
  via Demonic Art. ⚠ **Conflict to resolve:** the Blizzard Game Data API tooltip for
  `429657`, fetched 2026-08-11, **still renders 4 %**, against Tier-1 patch notes
  saying 3 %. Per provenance precedence the patch-note value is not discarded — both
  are Tier 1 and they disagree, most likely because the static tooltip lags the build.
  **Do not restate either number as settled.** `@verify-ingame` — read Flames of
  Xoroth's tooltip on a live 12.1 Destruction Diabolist and record which value the
  client shows.

  ⚠ **`builds.md` was rewritten for 12.1 (it carries its own §*What 12.1 changed for
  Destruction*), but its loadout call has not been re-simmed at 12.1** — the tree
  recommendation there still rests on pre-12.1 sims and unchanged maxroll captures.
- **Playstyle:** Chaos Bolt is the payoff button and most of the direct damage;
  a maintained fire DoT (Immolate/Wither) plus a mix of instant Conflagrate and
  Shadowburn keeps Destruction fairly mobile between hard-cast Incinerates.
- **12.1 crit note:** Destruction now has **three** always-crit buttons. Chaos Bolt
  has always been one ("dealing a critical strike … damage is further increased by
  your critical strike chance"), and the redesigned **Conflagration of Chaos**
  talent puts **Conflagrate and Shadowburn** on the same footing — 100 % crit,
  damage scaled by your crit chance. That makes crit a throughput stat for three
  buttons rather than one. `gearing.md` was rewritten for 12.1 and calls this out
  directly in its § *⚠ 12.1: Crit's role changed, and the captures do not reflect it* —
  but **the stat weights themselves have not been re-simmed at 12.1**; they are carried
  from pre-12.1 captures. Do not read that stat priority as settled.

## Ability inventory

> **Tier-1 floor.** Canonical **name, spellID, acquisition origin, base
> cooldown and Cooldown-Manager category** live in `ability-inventory.tsv`
> (regenerated from wago DB2 @ **12.1.0.69214** on 2026-08-11), with resolved
> Blizzard Game Data API tooltips in `ability-inventory.md` beside it — read them
> there rather than trusting a restated number here. This table is for **role and
> rotational context**; on any disagreement the generated files win.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.1.0.69214).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Incinerate | Rotational-builder | — | 2s cast | Core filler; generates **2** fragments (+1 on crit), **doubled to 4 by Diabolic Embers** ("Incinerate now generates 100% additional Soul Shard Fragments" *[Tier 1, 12.1]*). ⚠ **Fire and Brimstone does NOT grant fragments** — its tooltip is still damage-only at 12.1 ("also hits all enemies near your target for 25% damage"); an earlier revision of this line said otherwise. |
| Conflagrate | Rotational-builder | — | Instant · 2 charges, ~13s recharge | Instant fire nuke, generates **5** fragments — flat, at Season 2; the old "7 with the 4-set" was the **Season 1** (MID1, Abyssal Immolator) bonus and **no longer applies**, as the Season 2 Damned Necrolyte set buffs Incinerate and Echo of Sargeras instead (`gearing.md` § *Tier set — Midnight Season 2*). Grants **Backdraft** (next Incinerate / Chaos Bolt / Soul Fire −30 % cast time, max 2 charges *[Tier 1, 12.1]*). Mobile filler. **12.1: with Conflagration of Chaos talented it always crits, and its damage scales with your crit chance.** |
| Immolate | Rotational-builder (DoT) | — | 1.5s cast · DoT | Fire DoT you keep up; each tick generates **1** fragment (+1 at 50 % on a crit tick) and can proc Conflagrate resets. Diabolist maintenance DoT. |
| Wither | Rotational-builder (DoT) | — | 1.5s cast · DoT | **Hellcaller** replacement for Immolate — 18s Shadowflame DoT that Malevolence and Blackened Soul stack/detonate. **12.1: Wither now grants Soul Leech** (it erroneously did not before), and **Blackened Soul was redesigned** so Chaos Bolt and Shadowburn add a Wither stack, each stack gain able to collapse into per-second Shadowflame damage. |
| Chaos Bolt | Rotational-spender | 2 Soul Shards | ~2.5s cast | Primary spender and the bulk of single-target damage. **Always a critical strike, and its damage is further increased by your crit chance** *[Tier 1 tooltip, 12.1]*. **Damage +5 % in 12.1.** For Hellcaller it also feeds Blackened Soul stacks onto a Withered target. |
| Rain of Fire | Rotational-spender (AoE) | 3 Soul Shards | Channeled AoE | Ground-target AoE spender; the shard dump at high target counts (Hellcaller sooner, Diabolist only at ~8+). |
| Shadowburn | Rotational-spender / Execute | 1 Soul Shard | Instant · ⚠ **charges disputed — see below** | Execute spender: **only usable on enemies below 20 % health** *[Tier 1 tooltip, 12.1]*; **restores 1 Soul Shard and clears its own cooldown if the target dies.** **12.1: with Conflagration of Chaos talented it always crits and scales with crit chance, and it is now a tracked BUFF in the Cooldown Manager** (`Buff/Essential` in game data, **was `Essential`**) — it was already a tracked cooldown; what is new is that it now also renders as a **buff**, so a CDM/HUD skin will get an extra Shadowburn entry it did not have before. |
| Soul Fire | Rotational-builder | — | ~4s cast · **45s CD** `[T1]` | Hard-cast that applies Immolate and generates **10 fragments — a full Soul Shard**; best consumed with Backdraft. **Damage +45 % in 12.1** — the single biggest per-ability buff on the spec this patch. **Choice node with Dimensional Rift** *[Tier 1, talents.md 10,15]*. |
| Dimensional Rift | Rotational-builder | — | Instant · charges | "Rips a hole in time and space, opening a portal that damages your target. **Generates 3 Soul Shard Fragments**" *[Tier 1 tooltip, spell 196586 @ 12.1.0.69214]* — a builder, not a spender. **Choice partner to Soul Fire** on the same node. With **Avatar of Destruction**, opening a rift has a chance to summon an **Overfiend** instead (1 fragment/sec + Chaos Bolt at 80 % effectiveness for 8s). Was absent from this table before 2026-08-11 — a pre-existing omission, not a 12.1 addition. |
| Cataclysm | Rotational-builder (AoE) | — | Instant · **30s CD** `[T1]` | Ground AoE dealing Shadowflame damage in 8 yds and afflicting everything hit with **Immolate**; strong opener + AoE setup. |
| Channel Demonfire | Rotational-spender | — | Channeled · **25s CD** `[T1]` | Launches 15 bolts over ~2.7s at random targets afflicted by your Immolate/Wither, each splashing nearby enemies. ⚠ **12.1: Channel Demonfire no longer grants Soul Leech** — it was doing so erroneously, so your passive absorb uptime drops slightly if you channel it on cooldown. Talent. |
| Infernal Bolt | Rotational-builder | — | ~2s cast | **Diabolist** Incinerate replacement that generates **more** shards; appears in the APL as a shard-refill button when low. **12.1: now correctly grants Soul Leech.** Midnight-new. @verify-ingame *(the 20-vs-30-fragment question in the Overview above is still open at 12.1 — but 12.1's Secrets of the Coven `428518` description reads "generating 3 Soul Shards" identically on both Destruction and Demonology, which leans against the 20 reading; see the Overview note)* |
| Ruination | Rotational-spender (proc) | — | Instant (granted) | **Diabolist** free empowered nuke granted by cycling Diabolic Ritual → Demonic Art; press on proc. Midnight-new. @verify-ingame |
| Embers of Nihilam | **Passive** (spec apex talent) | — | — (nothing to press) | ⚠ **Not a button.** The 12.1 tooltip is explicit and now states the odds: **"Casting Incinerate has a 10 % chance to evoke an echo of the Dark Titan's power"**, which hurls **Echo of Sargeras** at the target for Shadowflame damage plus a 10-yd splash (reduced beyond 8 targets) *[Tier 1, spell 1265770 @ 12.1.0.69214]*. The 12.1 notes call out exactly this tooltip change. An earlier revision of this row called it a "situational burst button"; that was wrong, and nothing in the rotation waits on you to press it. ⚠ Note the two generated files disagree on node type — `talents.md` reads `ACTIVE`, `ability-inventory.tsv` reads `talent-passive` / `castable=false`. The **tooltip behaviour is proc-driven**, so treat it as an apex-row throughput passive. |
| Havoc | Utility (cleave) | — | Instant · **30s CD** `[T1]` · 15s duration | Marks a second target; your single-target spells (Chaos Bolt, Shadowburn, etc.) also strike it. ⚠ **12.1 NERF: the copy is 50 % of the damage dealt (was 60 %)** *[Tier 1 tooltip + patch notes]* — the 2-target cleave button is meaningfully weaker, and any pre-12.1 target-count breakpoint that leaned on Havoc should be re-derived rather than trusted. |
| Summon Infernal | Major cooldown | — | Instant · 120s CD (90s w/ Inferno), 30s duration | Meteor + persistent infernal; the primary DPS burst window everything (potion/trinkets/racials) syncs to. Base CD confirmed 120s via DB2 (SpellCooldowns spell 1122) and **re-confirmed unchanged at 12.1.0.69214**; **Inferno** talent −30s → 90s. ⚠ 12.1's global "major DPS cooldowns lowered, steady-state raised" direction did **not** touch Summon Infernal on this spec. |
| Malevolence | Major cooldown | — | **60s CD** *[Tier 1]* | **Hellcaller** burst CD — grants haste and empowers/extends active Withers. Hellcaller-exclusive, and a talent rather than a hero-tree freebie. Midnight-new. |
| Curse of Exhaustion | Utility (slow) | — | Instant | Reduces target movement speed. Curse. |
| Curse of Tongues | Utility (slow-cast) | — | Instant | Slows enemy cast speed. Curse. |
| Curse of Weakness | Utility (debuff) | — | Instant | Reduces target physical damage. Curse. |
| Blight of Weakness | Utility (debuff) | — | Instant (talent) / **120s** `[T1]` | **Hellcaller** curse upgrade (choice with Blight of Tongues) — an **AoE** version of Curse of Weakness: a shadow mist over the target and everything within 10 yds, **+100 % time between their attacks and −10 % crit chance for 12s** *[Tier 1 tooltip, spell 1271748 @ 12.1.0.69214]*. Blights share the one-per-target Curse limit. |
| Drain Life | Defensive (self-heal) | — | Channeled | Channel that damages and **heals you for 500 % of the damage done** *[Tier 1 tooltip, 12.1]*; the core sustain filler when low. **12.1: health drain +25 % class-wide** — with player health also up 25 % at max level, the *relative* sustain is roughly unchanged, which is the point of the retune. **Empowered Drain Life** additionally heals +200 % of damage dealt and grants Soul Leech equal to 10 % of damage dealt. |
| Mortal Coil | CC / Defensive | — | Instant · **45s CD** `[T1]` | Horrifies an enemy into fleeing, incapacitating for **3s**, and heals you for **20 % of maximum health** *[Tier 1 tooltip, 12.1]*. The old "20–25 %" range here was imprecise; re-read at 12.1 after the global health/healing retune. Talent. |
| Shadowfury | CC (AoE stun) | — | Instant / **60s** `[T1]` | AoE stun at a ground location. Choice node with Howl of Terror. |
| Fear | CC | — | 1.5s cast | Single-target fear; breaks on damage. |
| Howl of Terror | CC (AoE) | — | Instant / **40s** `[T1]` (talent) | AoE fear around you; choice node with Shadowfury. |
| Banish | CC | — | 1.5s cast | Incapacitates a Demon or Elemental. Talent. |
| Spell Lock | Interrupt | — | Instant · **24s CD** *[Tier 1]* | A **pet ability on the Felhunter's own skill line**, not a player spell — so it is absent from this spec's `ability-inventory.tsv` by design and lives in `_abilities/pet-family-annex.tsv`. Interrupt + purge; Destruction's kick comes from the pet, which means no Felhunter, no kick. |
| Subjugate Demon | Utility (enslave) | — | 3s cast | Takes control of a target demon. |
| Fel Domination | Pet | — | Instant / **180s** `[T1]` | Next pet summon is instant + free — emergency re-summon. |
| Summon Imp / Summon Voidwalker / Summon Felhunter / Summon Sayaad | Pet | — | Cast | Four separate class-baseline spells, one per pet — there is no generic "Summon Pet" ability, which is how this row read until *[Tier 1, 2026-08-06]*. Pick by utility: Felhunter interrupt/purge (the group-content default), Voidwalker tank, Imp dispel, Sayaad CC. Felguard is Demonology-only — not available to Destruction. |
| Soulstone | Utility (battle rez) | — | 3s cast / **600s** `[T1]` | Combat resurrection; can be pre-applied for a self-rez. |
| Create Healthstone | Defensive (conjure → item heal) | — | Instant / — | The **player ability** is `Create Healthstone` 6201 *[Tier 1]*; "Healthstone" alone names the *item* use (6262), which is not a learned spell — renamed to match affliction and demonology. Conjure out of combat; the stone restores **25 % health** *[Tier 1 tooltip, 12.1]* — re-read after 12.1 rescaled health consumables to the +25 % max-level health pool, replacing the old "~25–30 %" estimate. Reusable in combat with Pact of Gluttony. ⚠ **12.1 also made trinkets, potions, healthstones and racials trackable and pingable in the Cooldown Manager.** |
| Create Soulwell | Utility | — | Cast / **120s** `[T1]` | Places a well for the group to grab Healthstones. |
| Soulburn | Utility (empower) | 1 Soul Shard | Instant · ~30s CD | Empowers your next specific spell (e.g. Soul Fire / Demonic Circle / Healthstone). Talent. |
| Dark Pact | Defensive (absorb) | — | Instant · **60s CD** `[T1]` | Sacrifices **20 % of current health** to shield you for **200 % of the sacrificed health** plus a flat amount, 20s; **usable while suffering control-impairing effects** *[Tier 1 tooltip, 12.1]*. Talent. |
| Unending Resolve | Defensive | — | Instant · **180s CD** `[T1]` | **−25 % damage taken** + immunity to interrupt, silence and pushback, **8s** *[Tier 1 tooltip, 12.1]*. (Strength of Will deepens the reduction; that talent's exact value is not in the base tooltip and is not restated here.) |
| Burning Rush | Movement | — | Toggle | +50% run speed at the cost of health-over-time; the main mobility toggle. |
| Demonic Circle | Movement (utility) | — | Cast to place | Drops a portal; **Demonic Circle: Teleport** returns you to it. Talent. |
| Demonic Circle: Teleport | Movement | — | Instant / **30s** `[T1]` | Teleport to your placed Demonic Circle (also breaks roots). |
| Demonic Gateway | Movement (utility) | — | Cast · **10s CD** `[T1]` | Places a linked portal pair; each player can use a given gateway once per 90s *[Tier 1 tooltip, 12.1]*. ⚠ **12.1: Summon Demonic Gateway is now a Utility spell by default in the Cooldown Manager** — its game-data category reads `Utility`, so it no longer competes for an Essential slot in a CDM-driven HUD. Talent. |
| Grimoire of Sacrifice | Utility (passive buff) | — | Instant (talent) / **30s** `[T1]` | Sacrifices your pet for a personal damage buff + a proc (choice with Summoner's Embrace). |
| Command Demon / pet-specific | Utility | — | Instant | Contextual pet command (Spell Lock, Seduction, Shadow Bulwark, etc. depending on active pet). |

> ⚠ **Shadowburn's "2 charges, ~12s recharge" is contradicted by Tier-1 data
> (2026-07-30) and the contradiction SURVIVES 12.1 (re-checked 2026-08-11).**
> The old row asserted 2 charges. Two independent Tier-1 sources disagree: wago DB2 has
> Shadowburn `17877` with `SpellCategories.ChargeCategory = 0` and
> `SpellCooldowns.RecoveryTime = 0` (against Conflagrate `17962`, which carries
> `ChargeCategory = 672`), and a live in-client capture found Shadowburn raising **no**
> `Available`/`OnCooldown`/`ChargeGained` Cooldown-Manager alerts, i.e. it has no recovery
> event at all — while Conflagrate raised all three. The regenerated 12.1 inventory still
> reads `cooldown = 0` for Shadowburn *[12.1.0.69214]*, and the 12.1 tooltip's only
> cooldown language is **"removes its cooldown if the target dies"** — which implies *a*
> cooldown exists without naming its length or charge count. The likely origin of the old
> claim is a pre-Midnight tooltip. **Not yet corrected outright**, because a talent could
> add charges via an aura effect that base DB2 rows would not show, and because the tsv's
> `cooldown` column is the known-wrong column for charge abilities (see the floor note
> above). `@verify-ingame` — check Shadowburn's tooltip on a live 12.1 Destruction
> character and, if it shows 1 charge and no recharge, delete this note and fix the row.
> ⚠ **12.1 gives a second instrument**: Shadowburn is now a tracked **buff** in the
> Cooldown Manager as well as an Essential cooldown, so a CDM read is a cheap
> cross-check alongside the tooltip.


> **Interrupt note:** Destruction has **no baseline personal interrupt**. Kicks
> come from the **Felhunter's Spell Lock** (or CC via Sayaad's Seduction /
> Shadowfury / Howl of Terror / Mortal Coil). This matters for interrupt
> assignments. **12.1: all class interrupts, Spell Lock included, now show a
> "missed" visual over the target's head and play a distinct sound when fired at a
> target that was not casting** — so a wasted pet kick is now visibly and audibly
> obvious to you and to your group, rather than silent. **12.1 also lengthened
> diminishing-return category resets to 20s (was 16s)**, which widens the window on
> chained Shadowfury / Howl of Terror / Fear before the next application is halved.

> **`Health Funnel` is gone, and is still gone at 12.1.** It had a row here as a
> pet-sustain channel; it is **not acquirable**. No spell of that name attaches to any
> acquisition table in the regenerated inventory — no talent node, no class skill line,
> no spec grant *[Tier 1, re-checked at 12.1.0.69214 on 2026-08-11; first measured at
> 12.0.7.67808]*. Pet healing is the pet's own business; don't plan around funnelling.
> Row deleted rather than left open, because the absence is measured, not merely
> unconfirmed.

> **Seed reconciliation:** the spec seed listed **Summon Felguard** — that is a
> **Demonology** pet and is **not** available to Destruction; corrected above.
> **Curse of Weakness** exists baseline; the Hellcaller talent line is
> **Blight of Weakness / Blight of Tongues** (choice). Names verified vs
> `raw/wago/SpellName.csv` @ 12.0.7 and **re-confirmed against the regenerated
> 12.1.0.69214 inventory** (`Blight of Weakness` 1271748, `Blight of Tongues` 1271802).

> **Cooldown Manager delta for 12.1 — read this before touching any CDM/HUD guidance.**
> The Blizzard-category column in `ability-inventory.tsv` is the authoritative
> tracked-set signal, and three Destruction entries moved this patch:
>
> | Spell | 12.0.7 | 12.1 | Consequence |
> |---|---|---|---|
> | Shadowburn `17877` | `Essential` | **`Buff/Essential`** | **Added as a tracked buff** — it was already an Essential cooldown; the *buff* entry is new, so a skin that assumed no Shadowburn buff will render an extra icon. |
> | Conflagration of Chaos `387108` | `Buff` | **(empty)** | **Removed from the Cooldown Manager** — anything keying off a Conflagration-of-Chaos CDM entry breaks silently and must be re-pointed. |
> | Demonic Gateway `111771` | `Essential` | **`Utility`** | Class-wide 12.1 change: Utility by default, so it stops occupying an Essential slot. |
>
> (12.0.7 column read from the previous generated tsv @ 12.0.7.67808 in git history;
> 12.1 column from the regenerated tsv @ 12.1.0.69214.)
>
> Beyond this spec, 12.1 also made the Cooldown Manager track **trinkets, potions and
> racial cooldowns/durations** and added a **"Short" sounds** category. ⚠ The addon-side
> detail belongs to `knowledge/addon-dev/`, which is swept separately under its own
> evidence rules — do not restate CDM API behaviour from here.

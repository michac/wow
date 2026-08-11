---
title: Demonology Warlock — ability inventory (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11  # 12.1 "Curse of Ula'tek" sweep: Shadow Bolt +45% / Demonbolt +55% / Summon Gloomhound +35%; Diabolist −20% pass; class-wide Drain Life +25% and the Soul Leech correctness pass (Legion Strike LOST it); Demonic Gateway → Utility in the CDM (confirmed in the regenerated tsv's blizz_category); the four not-on-the-tree names re-confirmed against all-talents.tsv @ 12.1.0.69214. Earlier: reconciled against the generated DB2 ability inventory (Summon Doomguard, Spell Lock origin, Create Healthstone); Summon Demonic Tyrant costs 0 shards, not 1; Infernal Bolt yield 2→3 corrected 2026-07-25
sources:
  - knowledge/classes/warlock/demonology/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.1.0.69214 — the name/spellID/origin/cooldown/CDM-category floor, 2026-08-11
  - knowledge/_meta/patch-notes/12.1.md  # tier 1, verbatim 12.1 content-update notes (CLASSES ▶ WARLOCK / Demonology), 2026-08-11
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" Content Update Notes
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1, pet skill lines, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/266  # tier 1, Blizzard Game Data API talent/spell names
  - raw/wago/SpellName.csv  # tier 1, wago.tools SpellName DB2 — name canonicalization
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, PRE-12.1 (upd. 2026-05-19) — roles + cast/CD corroboration only; its numbers predate the 12.1 tuning
  - https://www.wowhead.com/spell=264178/demonbolt  # tier 4, Demonbolt effect corroboration
  - ./talents.md  # local, spec talent tree (regenerated @ 12.1.0.68914)
  - knowledge/classes/_talents/all-talents.tsv  # tier 1, every spec's tree @ 12.1.0.69214 — the four not-on-the-tree names checked across all of them
confidence: medium
---

# Demonology Warlock — ability inventory (Midnight 12.1)

> Companion to `rotation.md` (priority/CDM), `builds.md` (talents/gear), and
> `talents.md` (raw tree). This is the raw ability catalog with game roles —
> not a rotation and not a keybind sheet.

## What 12.1 changed for this spec

12.1 "Curse of Ula'tek" **did not add, remove or move a single Demonology
talent** — `all-talents.tsv` @ `12.1.0.69214` carries the same node set as
12.0.7. Everything below is tuning, a Cooldown-Manager reclassification, or a
Soul Leech bug fix, so the *catalog* is structurally intact.

- **Spec tuning:** Shadow Bolt **+45%**, Demonbolt **+55%**, Summon Gloomhound
  **+35%**. All three are steady-state buttons — this is the game-wide 12.1
  direction of *raising sustained damage* while trimming burst, and Demonology
  got the "raise sustained" half without a Tyrant cooldown change (Summon
  Demonic Tyrant is still **60s** in the regenerated tsv).
- **Diabolist nerfed:** Chaos Salvo, Felseeker, Wicked Cleave and Eye Explosion
  all **−20%**; **Flames of Xoroth** now grants **+3%** Fire damage and demon
  damage (**was 4%**). None of these are rows in the table below (they are hero
  procs) — they live in `diabolist-sequences.md`. ⚠ This file used to call
  Diabolist the **M+ default**; that label predated the nerf and has **not** been
  re-sourced against a post-12.1 sim or guide, so it has been dropped from the
  Overview rather than restated. Treat the hero-tree pick as **open** and read
  `builds.md` — do not lift one from the `maxroll-*.md` captures in this
  directory, which are Tier 3 and still pre-12.1. It is a sim question, not an
  in-game one: it resolves when `sims.md` is re-pulled at a 12.1 SHA.
- **Class-wide:** Drain Life health drain **+25%**.
- **Soul Leech correctness pass** (matters because Soul Leech is the passive
  absorb backbone): Infernal Bolt, **Wild Imp / Imp Gang Boss Fel Firebolt**,
  **Imp Lord's Greater Felbolt**, **Demonic Tyrant's Demonfire**, **Vilefiend's
  Headbutt and Bile Spit** and **Gloomhound's Gloom Slash** now correctly grant
  Soul Leech — i.e. the demon army finally feeds the shield. Going the other
  way, the **Felguard's Legion Strike no longer grants Soul Leech** (it was doing
  so erroneously).
- **Cooldown Manager:** **Summon Demonic Gateway is now a Utility spell by
  default** — visible in the regenerated `ability-inventory.tsv`, where Demonic
  Gateway's `blizz_category` moved `Essential` → `Utility`. (Summon Doomguard's
  category also shifted, `Buff/Essential` → `Essential/Other`.)

Three **global** 12.1 changes also land on rows below: player health and
creature damage are **+25% at max level** with health consumables rescaled to
match (so the percent-of-max-HP heals here still read correctly, but any
*absolute* HP figure from before 2026-08-11 does not); **all interrupts** now
show a "missed" visual and sound when fired at a target that was not casting
(Axe Toss, Spell Lock); and **diminishing-return categories now reset after 20s**
(was 16) — DR takes *longer* to clear, so a repeat Shadowfury / Howl of Terror /
Fear / Mortal Coil on the same target stays reduced across a wider window.

## Overview

- **Hero trees:** **Diabolist** (burst via Demonic Ritual → Overlord / Pit Lord
  summons inside the Tyrant window; **−20% across its damage procs in 12.1**,
  see above) and **Soul Harvester** (ST/raid + solo-survivability alternative;
  its **Mark of Shatug** converts Summon Vilefiend into the **Gloomhound**,
  buffed **+35%** in 12.1). See `builds.md`.
- **Resources:** **Soul Shards** (0–5; builders generate, spent on Hand of
  Gul'dan / Call Dreadstalkers / summons) and **Demonic Core** (a proc/charge
  system, up to 4 stacks, consumed to make **Demonbolt** instant + hard-hitting).
  Mana is effectively a non-constraint.
- **Playstyle:** a builder/spender **pet-army** spec. You bank shards and imps,
  then funnel everything into the 1-minute **Summon Demonic Tyrant** window,
  which empowers and extends every active demon. Most of your damage comes from
  the demons, not your own casts.

## Inventory

`Function` = game role, not a keybind assignment.

> **Tier-1 floor.** Canonical **name, spellID, acquisition origin, base
> cooldown and Cooldown-Manager category** live in `ability-inventory.tsv`
> (regenerated from wago DB2 @ **12.1.0.69214**) — read them there rather than
> trusting a restated number here. This table is for **role and rotational
> context**; on any disagreement the tsv wins.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.1.0.69214;
> every `[T1]` value below re-read unchanged at 12.1).
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
| **Shadow Bolt** | Rotational-builder | Generates 1 Soul Shard | ~2s cast | Baseline single-target filler / shard builder. Chance to grant a Demonic Core. **Damage +45% in 12.1.** **Replaced by Infernal Bolt** when *Demoniac* is talented (the standing build). |
| **Infernal Bolt** | Rotational-builder | Generates 3 Soul Shards | ~2.3s cast | *Demoniac* talent replacement for Shadow Bolt — builds shards ~3× as fast; cast when at ≤2 shards. **12.1: now correctly grants Soul Leech.** |
| **Demonbolt** | Rotational-spender (core) | Consumes 1 Demonic Core; generates 2 Soul Shards | Instant with a Demonic Core (else ~4.5s cast) | Demonic-Core spender — hits hard and refunds 2 shards. **Damage +55% in 12.1** — the single biggest number to move for this spec. Applies **Doom** if talented. Dump cores so they don't overcap. |
| **Hand of Gul'dan** | Rotational-spender (imp generator) | 1–3 Soul Shards | ~1.5s cast | Spend 1–3 shards to summon that many **Wild Imps**. The single most-maximized cast inside the Tyrant window; cast at 4–5 shards, never overcap. |
| **Call Dreadstalkers** | Rotational-summon | 2 Soul Shards (free/instant with *Demonic Calling*) | ~20s CD | Summons **two Dreadstalkers** for ~12s. Refresh just before Tyrant so they're fresh when it empowers them. |
| **Summon Demonic Tyrant** | Major cooldown | **none** | ~1s cast / **60s** `[T1]` | The spec's centerpiece. Empowers and **extends the duration of every active demon** for ~15s and pumps damage. Enter with a full board (Wild Imps + fresh Dreadstalkers + Grimoire demon). 12.1 lowered several specs' major cooldowns — **this one did not move**; it re-reads 60s at `12.1.0.69214`. Its **Demonfire now grants Soul Leech.** |
| **Dominion of Argus** | Major cooldown (apex) | — | active, aligns w/ Tyrant | Apex talent; a large Summon Demonic Tyrant enhancement — the standing build is built around it (see `builds.md`). Untouched by 12.1. @verify-ingame |
| **Implosion** | Rotational-spender (AoE) | — (consumes Wild Imps) | Instant / **15s** `[T1]` | Sacrifices **all Wild Imps**, each flying to the target and exploding for AoE. Press at ~6 imps for cleave; on pure ST only Implode if talented into *To Hell and Back*. Choice-node vs Power Siphon. |
| **Power Siphon** | Utility (core generator) | — (consumes up to 2 Wild Imps) | ~30s CD | Choice-node vs Implosion. Sacrifices up to 2 Wild Imps to grant **2 Demonic Cores** — fuels the next Demonbolt / Hand of Gul'dan chain. |
| **Grimoire: Fel Ravager** | Rotational-summon | Soul Shards | active (choice node) / **120s** `[T1]` | Choice-node vs *Grimoire: Imp Lord*. Summons a **Fel Ravager** demon added to the Tyrant board. 12.1: the **Imp Lord's Greater Felbolt now grants Soul Leech** (so does the Wild Imp / Imp Gang Boss **Fel Firebolt**). |
| **Summon Vilefiend** | Passive summon | — | passive/talent | Talent that summons a **Vilefiend** demon for the rotation/Tyrant board (a passive node in the Midnight tree). Its **Headbutt and Bile Spit now grant Soul Leech** (12.1). Soul Harvester's **Mark of Shatug** converts it to the **Gloomhound** (Gloom Slash — **+35% in 12.1**, and it now grants Soul Leech too); **Mark of F'harg** converts it to the **Charhound**. |
| **Summon Doomguard** | Rotational-summon / cooldown | Soul Shards | **120s CD** *[Tier 1]* | Summons a **Doomguard** demon — a genuine active talent on the deep spec tree (not a passive summon like Vilefiend), so it is a pressed button on a 2-minute cycle: line it up with the Tyrant window rather than pressing it on sight. |
| **Summon Felguard** | Pet | 1 Soul Shard | ~cast, out of combat | Summons the **Felguard**, Demonology's permanent pet (universal in group content). Provides **Axe Toss** interrupt via Command Demon. ⚠ 12.1: its **Legion Strike no longer grants Soul Leech** — it had been doing so erroneously, so your passive shield uptime from pet melee drops. |
| **Command Demon / Axe Toss** | Interrupt | — | ~30s CD (Felguard) | *Command Demon* fires the active pet's special. With the Felguard that's **Axe Toss** — a ranged interrupt + brief stun. 12.1: firing it at a target that was **not** casting now shows a **"missed" visual + sound** over the target (game-wide interrupt change). |
| **Spell Lock** | Interrupt / Dispel | — | **24s CD** *[Tier 1]* | A **pet ability learned on the Felhunter's own skill line**, not a player spell — which is why it is absent from this spec's `ability-inventory.tsv` (it lives in `_abilities/pet-family-annex.tsv`). Interrupt + a purge, fired via Command Demon, and only available if you give up the Felguard's Axe Toss to run the Felhunter. Same 12.1 "missed" feedback as Axe Toss. |
| **Doom** | Passive | — | passive talent | Demonbolt applies **Doom**, a delayed detonation on the target. Build-defining passive, not a pressed button. |
| **Fel Domination** | Utility (pet) | — | **180s** `[T1]` | Your next pet summon within 15s is **instant and free** — the emergency re-summon after a pet dies. |
| **Subjugate Demon** | CC (utility) | — | ~1.5s cast | Enslaves a target demon to fight for you (leveling / niche PvE utility). |
| **Drain Life** | Defensive (self-heal) | — | channel | Channels damage that **heals you** — the low-cost sustain heal; often macro'd with `/cancelaura Burning Rush`. **12.1: health drain +25% (class-wide)**, which makes it a materially better out-of-Tyrant filler when you need to top up. |
| **Mortal Coil** | Defensive / CC | — | **45s** `[T1]` | Horrifies the target (~3s) and heals a **percentage of max HP** (~20–25%). A defensive + single-target peel. Because it heals a %, 12.1's **+25% max health** carries it up automatically — but the DR category it shares now resets after **20s** (was 16). |
| **Dark Pact** | Defensive (absorb) | Sacrifices current HP | **60s** `[T1]` / *Frequent Donor*) | Sacrifices health for a large **absorb shield**; usable while CC'd. |
| **Unending Resolve** | Defensive (major) | — | **180s** `[T1]` | **−25% damage taken** for 8s (−40% with *Strength of Will*) + interrupt/silence immunity — the big personal defensive. |
| **Create Healthstone** | Defensive (conjure → item heal) | — | Instant · no CD | The **player ability** is `Create Healthstone`; "Healthstone" alone names the *item* use, which is not a learned spell — renamed here *[Tier 1, 2026-08-06]*. Conjure pre-combat; using the stone is an instant **~25–30% of max HP** heal, once per combat unless *Pact of Gluttony* is talented. ⚠ 12.1 rescaled health-consumable values against the new (+25%) max-health pool — the *percentage* stands, but any absolute HP figure quoted for a healthstone or health potion before 2026-08-11 is stale. |
| **Soulstone** | Utility (battle-rez) | — | ~2.5s cast / **600s** `[T1]` | Combat resurrection on an ally (self-rez out of combat) — the warlock brez. |
| **Soulburn** | Utility (empower) | 1 Soul Shard | instant | Empowers the **next** spell (e.g. Healthstone/Drain Life/Demonic Circle) with a bonus effect. |
| **Demonic Circle** | Movement (utility) | — | ~0.5s cast | Places a portal on the ground. |
| **Demonic Circle: Teleport** | Movement | — | instant / **30s** `[T1]` | Teleports back to your placed Demonic Circle (kiting / mechanic dodge). |
| **Demonic Gateway** | Movement (utility) | — | ~2s cast / **10s** `[T1]` | Places a two-way gateway allies can use to skip terrain — group mobility/skips. **12.1: "Summon Demonic Gateway" is now a *Utility* spell by default in the Cooldown Manager** (was Essential) — so it drops out of the default essential-cooldown viewer unless you re-file it. Confirmed in the regenerated tsv's `blizz_category`. |
| **Burning Rush** | Movement | Drains health over time | toggle | +50% run speed at the cost of health-per-second; toggle off with `/cancelaura`. |
| **Shadowfury** | CC (AoE) | — | **60s** `[T1]` | Ground-targeted **AoE stun** — the spec's main trash-pack stun. Choice-node vs *Howl of Terror*. 12.1: **DR categories reset after 20s** (was 16), so a repeat stun on the same pack lands at reduced duration for longer. |
| **Howl of Terror** | CC (AoE) | — | ~40s CD | AoE **fear** around you (choice-node vs Shadowfury); Diabolist can grant a stronger 10-target version. Same 12.1 20s DR reset. |
| **Fear** | CC (single) | — | ~1.5s cast | Single-target fear. |
| **Banish** | CC (single) | — | ~1.5s cast | Banishes a Demon/Elemental, removing it from combat temporarily. |
| **Curse of Tongues** | Utility (debuff) | — | ~1.5s cast | Slows the target's cast speed. |
| **Curse of Weakness** | Utility (debuff) | — | instant | Reduces the target's physical damage. |
| **Curse of Exhaustion** | Utility (slow) | — | instant | Reduces the target's movement speed (kite tool). |
| **Blight of Weakness** | Utility (debuff) | — | instant / **120s** `[T1]` | Talent upgrade to Curse of Weakness (choice-node vs *Blight of Tongues*); adds a lingering effect. |
| **Fel Armor / Demon Skin / Soul Leech** | Passive (defensive) | — | passive | The passive absorb/mitigation backbone — Soul Leech shields off damage dealt; Demon Skin/Fel Armor enlarge and refill it. **12.1 reworked which abilities feed it** (see "What 12.1 changed"): the demon army now does (Fel Firebolt, Greater Felbolt, Demonfire, Headbutt / Bile Spit, Gloom Slash) and so does Infernal Bolt, while the **Felguard's Legion Strike no longer does**. Net effect on a Demonology shield is *up*, since the pet board is most of your damage. |

**Notes / canonicalization (Tier-1 game data is the floor):**
- **Shadow Bolt → Infernal Bolt**: with *Demoniac* (the standing build) your
  baseline builder is **Infernal Bolt** (spell 433891), not Shadow Bolt. Both
  names are live; the seed's "Shadow Bolt" is correct as the *untalented*
  builder. ⚠ 12.1 buffed **Shadow Bolt by 45%** and said nothing about Infernal
  Bolt — whether that closes the gap enough to matter to the Demoniac pick is a
  **sim question, not a note-reading one**; do not infer a build change from the
  buff line alone. See `sims.md` / `builds.md`.
- The seed's **"Grimoire: Fel Ravager"** is confirmed live (spell 1276467), a
  choice-node vs **Grimoire: Imp Lord**. The old **Grimoire: Felguard** (111898)
  still exists in game data but is **not** on the Midnight Demo spec tree.
- **Curse of Weakness** and **Blight of Weakness** are distinct: the curse is
  baseline; Blight is the talent upgrade (choice vs Blight of Tongues).
- **Not on the Midnight Demo spec tree** (present in older builds, omitted here):
  **Bilescourge Bombers, Nether Portal, Demonic Strength, Guillotine**. Confirmed
  against the Blizzard Game Data API tree itself — tree 720 / spec 266, whose 147
  talent names contain none of the four, while Hand of Gul'dan, Implosion, Summon
  Demonic Tyrant and Doom are all present as controls. They are absent from
  `all-talents.tsv` for **every** spec, not just this one, so they are not talents
  anywhere. **Re-confirmed at 12.1**: all four (plus the old *Grimoire: Felguard*)
  score zero hits across the regenerated `all-talents.tsv` @ `12.1.0.69214`.
  *[Tier 1, 2026-08-11]*
- **12.1 added and removed nothing on this tree.** The Affliction sibling lost
  *Nocturnal Yield* and *Patient Zero* and gained *Hedonic Gorging* and
  *Impetuous Wrath* in the same node slots; **Demonology's node set is
  unchanged**, so the inventory above needed no additions or deletions this
  patch — only the tuning, CDM and Soul Leech annotations. A node-level diff of
  `all-talents.tsv` across the 12.0.7 → 12.1 regen shows exactly **one**
  substantive Demonology change: the class-tree **Soul Leech** node now points
  at **spell 1311653** (was 108370), which is the data-side face of the Soul
  Leech grant/revoke pass. Everything else is prerequisite-list ordering noise.
  *[Tier 1: patch-notes/12.1.md CLASSES ▶ WARLOCK + `all-talents.tsv`
  @ 12.1.0.69214, 2026-08-11.]*

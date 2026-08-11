---
title: Affliction Warlock — Rotation (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — CLASSES ▶ WARLOCK / Affliction (verbatim in _meta/patch-notes/12.1.md)
  - simc midnight branch profiles/MID1/MID1_Warlock_Affliction.simc  # tier 1 APL, commit 204b88d 2026-06-02, WoW 12.0.5.67823 — PRE-12.1, see the banner
  - https://news.blizzard.com/en-us/article/24287397/hotfixes-june-30-2026  # tier 1, 6/30 hotfix — Seed of Corruption/Nightfall detonation + PvP-only +3%
  - https://www.icy-veins.com/wow/affliction-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, re-fetched 2026-08-11 as a 12.1-labelled guide
  - https://www.wowhead.com/news/affliction-warlock-restoration-druid-and-frost-mage-issues-resolved-midnight-381441  # tier 4, historical 12.0.7 hotfix mechanic fixes
  - Blizzard Game Data API /data/wow/spell/108558  # tier 1, live Nightfall text @ 12.1.0.69214 — via the regenerated ability-inventory.md in this directory
confidence: medium
---

# Affliction Warlock — Rotation (Soul Harvester, Midnight 12.1)

Distilled from the SimulationCraft default APL (tier 1), then patched by hand
for 12.1. The APL branches by hero tree (Soul Harvester / Hellcaller) and enemy
count (1 / 2 / 3+). Soul Harvester lists below — it was the only S1 build (see
`builds.md`), but see the Hellcaller note at the bottom: 12.1 changes that
question.

> **12.1 "Curse of Ula'tek" (live 2026-08-11) — the shard economy changed
> shape, and two talents the old lists leaned on no longer exist.**
>
> - **Shard Instability redesigned.** It is **no longer a stacking bank**.
>   Now: damage dealt by **Shadow Bolt or Drain Soul has a 20% chance** to make
>   your next **Unstable Affliction *or Seed of Corruption*** cost **no Soul
>   Shards and cast instantly**. Every "stack" rule the 12.0.7 notes carried
>   ("one stack per UA", "chain UAs through a multi-stack window", "bank it")
>   is dead — there are no stacks to bank, and Seed is now a legal target for
>   the proc.
> - **Haunt now increases your damage to the target by 16% for 18s** (was 12%).
> - **New talent: Hedonic Gorging** — Drain Life damage +10%; **Siphon Life**
>   additionally increases **Corruption** damage by 10%; **Dark Harvest channels
>   10% faster and deals 15% more damage**.
> - **New talent: Impetuous Wrath** — **Shadow Bolt / Drain Soul / Malefic
>   Grasp +10%, or +20% against a target affected by Haunt**; **Dark Harvest**
>   likewise +10% / +20%. This is the first thing in the spec that pays you
>   directly for keeping Haunt rolling *underneath your filler*, not just for
>   pressing it on cooldown.
> - **Removed entirely: Nocturnal Yield and Patient Zero.** Both are gone from
>   the live tree (confirmed against the regenerated `talents.md` /
>   `talents.json` @ build **12.1.0.68914** — Tier 1 game data, not prose; that
>   is the build the API's `static-12.1.0` namespace reported, and its `Trait*`
>   DB2 is byte-identical to the live 12.1.0.69214 client's, so cite it as
>   68914. Live *ability* text in this directory is 69214). Any
>   rule below that used to key off them has been rewritten, not annotated.
>   Blizzard's own note says the "occasional free Seed of Corruption" feeling
>   was **merged into Shard Instability**, which is why the proc now accepts Seed.
>
> **Warlock-wide (all three specs):** Drain Life health drain **+25%**;
> **Unstable Affliction and Malefic Grasp now correctly grant Soul Leech** (a
> real sustain gain for this spec — UA is the primary spender and Malefic Grasp
> is the Darkglare-window filler, so both were silently missing shields);
> **Summon Demonic Gateway is now a Utility spell by default in the Cooldown
> Manager** (a CDM categorization change, no rotational effect).
>
> **Global, every spec in the game:** max-level **player health and creature
> damage both +25%**, with health consumables rescaled to match — ⚠ **any
> absolute HP / healing / potion number written before 2026-08-11 is stale**;
> **interrupts now show a "missed" visual + sound** when used on a target that
> was not casting (for us that's the pet's Spell Lock / Axe Toss); **diminishing-
> return categories reset after 20s** (was 16s). Blizzard also lowered major DPS
> cooldowns and raised steady-state damage **for several specs** — **Affliction
> is not one of them**: no Affliction cooldown length changed in the 12.1 notes.
>
> ⚠ **Confidence is `medium` this pass, deliberately.** The priority ordering
> below still descends from the **12.0.5** simc APL; simc had **not** published a
> 12.1 MID1 Affliction APL as of 2026-08-11, and a spender redesign plus two
> removed talents is exactly the change that reorders a spender rule. What is
> written here is the old ordering with the dead talents excised and the new
> ones folded in, corroborated where it could be against the Icy Veins page now
> labelled 12.1 (Tier 3 — it may not overwrite anything sourced from the notes).
>
> *(Historical, 12.0.7: the Fatal Echoes free-UA fix and the Soul Swap
> zoning fix still hold. The Shard Instability stack-consumption fix from that
> patch is moot — the talent it fixed no longer works that way.)*

## Pre-combat

- Summon pet; pre-cast **Haunt** (ST) or **Seed of Corruption** (2+ targets).

## Cooldown rules

- Potion/racials **only while Darkglare is active**.
- Trinkets sync to Darkglare windows (don't bank past a lost use).
- **Dark Harvest before Darkglare** — the APL gates Darkglare on Dark
  Harvest already being on cooldown; the pair is the burst window.
- **Get Haunt onto the target before Dark Harvest** if you took Impetuous
  Wrath: Dark Harvest is +20% instead of +10% against a Haunted target, and
  Hedonic Gorging (if taken) shortens the channel 10% and adds another 15% on
  top. In 12.0.7 the Haunt→Dark Harvest ordering was a rounding error; in 12.1
  it is worth playing around.
- <8s left on the fight: dump shards into **UA** (or **Seed** with Sow the
  Seeds on 2+), and spend a pending **Nightfall** proc into your filler rather
  than letting the fight end on it.

## Single target

1. **Haunt** on cooldown — now **+16% damage taken for 18s** (was 12%), and
   with Impetuous Wrath your fillers get **+20% instead of +10%** while it's
   up. Improved Haunt + apex still make it a damage button in its own right.
2. **Agony** if <3s remaining
3. **Corruption** if <3s remaining
4. **Dark Harvest** when **<3 shards** and the channel fits inside both
   Agony and Corruption remaining (it refunds 3 shards — deplete first)
5. **Summon Darkglare** (once Dark Harvest is on CD)
6. On a **Nightfall** proc: spend it on the **next filler you start**.
   Live 12.1 text (spell `108558`, Tier 1): the next **Shadow Bolt** or **Malefic
   Grasp** deals **+25% damage**, Shadow Bolt becoming **instant** and Malefic
   Grasp channelling **50% faster**. **Drain Soul** *replaces* Shadow Bolt when
   talented, so on that build it is the filler that eats the proc — note this is
   an **inference from the replacement**, not a Tier-1 statement: the resolved
   buff string names only the base spell, and the 12.1 developers' note that
   mentions "Shadow Bolt or Drain Soul" is about *Nocturnal Yield*, not Nightfall.
   ⚠ **Whether Nightfall banks to 2 stacks is UNRESOLVED — see the box below.**
   *Malefic Grasp otherwise appears only as the Darkglare-window transform of your
   filler (step 8), not as a standalone button — the Malefic Grasp talent node is
   trap-tier, see `builds.md`.*
7. **Unstable Affliction** with any shard (primary spender; feeds succulent
   shards / Demonic Soul). A **Shard Instability** proc makes the next UA
   **free and instant** — in single target that is where it goes, every time.
   Treat it as a windfall you spend immediately rather than hold — the redesign
   makes it a per-proc effect on the *next* spender, so sitting on it only risks
   the next proc overwriting it.
8. Filler: Malefic Grasp during Darkglare (if talented — Shadow Bolt
   *becomes* Malefic Grasp while Darkglare is active) → **Drain Soul**
   (if a Nightfall proc appears mid-channel, restart the channel so the
   new one consumes the proc — procs only apply to channels *started*
   while the buff is up) → Shadow Bolt

**Nightfall, per the live 12.1 tooltip** (spell `108558`, Tier 1 — Corruption
damage has a chance to proc it; *Ravenous Afflictions* adds a second roll off
Agony/Corruption/UA crits): it empowers the **next** Shadow Bolt or Malefic Grasp
for **+25% damage**, making Shadow Bolt **instant** and Malefic Grasp channel
**50% faster**. *(The **+25%** is a correction: this file previously said +75%,
which the live tooltip contradicts.)*

> ⚠ **OPEN: does Nightfall bank to 2 stacks?** `@verify-ingame`
> **Do not treat either answer as settled.** The pre-12.1 rule was "stacks to 2,
> spend before you overcap, it jumps the priority queue," and that rule still has
> live corroboration on disk — `maxroll-raid.md` ("Be careful to not overcap on
> Nightfall stacks"), captured 2026-08-11 against a guide whose header reads 12.1.
> **Searched 2026-08-11 and NOT FOUND:** a stack count in the resolved buff text
> for spell `108558`, in *Ravenous Afflictions* (`459440`), or anywhere in the
> regenerated `ability-inventory.md`. That is an absence in *tooltip strings*,
> which routinely omit stack counts — **it is not evidence the behaviour changed.**
> **12.1 did not touch Nightfall at all**: the only hit for "Nightfall" in
> `_meta/patch-notes/12.1.md` is the *Nocturnal Yield* developers' note, which
> changes a different talent. The default inference for an ability a patch did not
> touch is **unchanged**, so the stacking rule is more likely live than dead.
> **The instrument that would settle it was not consulted** — the simc MID1
> Affliction APL would express `buff.nightfall.stack` if it stacks, and no
> Affliction `.simc` is cached under `raw/simc/`. Re-pull it
> (`uv run python -m wowkb.simc warlock affliction`) before writing a rule either way.

The one rule that survives unambiguously is the channel one:
the buff applies to a channel *started* while it is up, so if a proc lands
mid-channel, **clip and restart** rather than finishing the unbuffed channel
(Tier 3, corroborated by the maxroll clipping guidance). ⚠ **Nightfall no longer
has anything to do with Seed of Corruption** — that link was Nocturnal Yield,
which 12.1 deleted; the free instant Seed now comes from Shard Instability.

## Cleave (exactly 2)

As ST, plus: Seed to apply Corruption to both; **UA-cycle onto both
targets right before Dark Harvest comes off CD**; spend on Seed if you
took Sow the Seeds and both targets still need Corruption. A **Shard
Instability** proc spent on Seed here covers both targets for free and
instantly — that is usually better than a free UA on one of them.

## AoE (3+)

1. **Haunt** on cooldown (on the priority target — Impetuous Wrath's +20%
   follows Haunt, so it is single-target-shaped even in AoE)
2. **Seed of Corruption** when Corruption is missing/refreshable — never
   double-sow (APL checks in-flight + previous cast)
3. **Dark Harvest** on cooldown
4. **Agony on up to 5 targets** (lowest-remains first; refresh <5s)
5. **Darkglare**
6. Shard spender: **Seed with Sow the Seeds** (or >9 targets without
   Darkglare up); otherwise UA
7. Keep Agonies above 50% duration; Malefic Grasp to carry Darkglare's
   last GCD
8. **Shard Instability procs go to Seed here, not UA** — free *and* instant is
   worth most when it is applying Corruption to the whole pack. Prefer a target
   that does **not** already carry a Seed. ⚠ **Open question, unverified in
   12.1:** a 6/30/2026 hotfix made a Nightfall-consuming Seed cast onto an
   *already-seeded* target **detonate** the preexisting Seed; that line sat in
   the PvP section of the notes and its PvE scope was never resolved, and the
   Nightfall path it described no longer exists. Whether a **Shard Instability**
   free Seed detonates an existing Seed the same way — and what happens to a
   second proc that lands while one is still pending — needs a dummy test.
   @verify-ingame
9. Filler as ST

## Hellcaller

**Re-evaluate this in 12.1 — do not assume the S1 answer holds.** Hellcaller
lists exist in the APL (`HC_st/cleave/aoe` — Wither instead of Corruption,
Malevolence as the 1-min CD) and the tree saw 0/50 usage in top S1 M+, which is
why it was never distilled here. 12.1 buffed it hard: **Blackened Soul
redesigned** (Chaos Bolt / Shadowburn add stacks on a Withered target; stacks
collapse into Shadowflame damage) with **damage +45%**, **Wither damage +25%**,
and **Mark of Peroth'arn redesigned** (Wither crits 215%, Blackened Soul crits
225%). The Icy Veins page now labelled 12.1 lists **Malevolence on cooldown** in
its baseline priority, i.e. it is writing for Hellcaller. Hero-tree selection is
`builds.md`'s call and there is no 12.1 usage or sim data on patch day — but
"Soul Harvester, obviously" is a **12.0.7** conclusion and should not be
repeated as a 12.1 one.

## TODO

- [x] Single-target priority (opener + sustain) — from simc APL 2026-06-03
- [x] Multi-dot / M+ priority — from simc APL 2026-06-03
- [x] Hero talent build used in **S1** — Soul Harvester (see `builds.md`);
      reopened for 12.1 below
- [x] Cooldown usage rules — Dark Harvest→Darkglare pairing, trinket sync
- [ ] Sanity-check the opener against a top WCL log (`wowkb.wcl rankings`
      → `casts`) per the original sourcing plan
- [ ] **Re-distill on a 12.1 simc APL.** 12.1 went live 2026-08-11; the talent
      removals (Nocturnal Yield, Patient Zero), the Shard Instability redesign
      and the two new talents are folded in above **by hand**, but the ordering
      itself is still the 12.0.5 APL's. simc had published no 12.1 MID1
      Affliction profile as of 2026-08-11 (`sims.md` is likewise still on the
      12.0.5 binary). Re-run `wowkb.simc warlock affliction` once the midnight
      branch updates, then re-confirm steps 4–8 of the ST list and step 6/8 of
      the AoE list.
- [ ] **Hero tree for 12.1** — Soul Harvester vs Hellcaller is genuinely open
      after the Blackened Soul / Wither buffs; resolve in `builds.md` off usage
      data once S2 opens (2026-08-18) and distil the `HC_*` lists here if it flips.

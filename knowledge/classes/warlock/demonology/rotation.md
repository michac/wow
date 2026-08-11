---
title: Demonology Warlock — rotation & CDM setup (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, 12.1 "Curse of Ula'tek" content update notes — the Demo/Diabolist/Warlock tuning below (archived verbatim in _meta/patch-notes/12.1.md)
  - simc midnight branch profiles/MID1/MID1_Warlock_Demonology.simc  # tier 1 APL, commit 48103ef 2026-05-18 (distilled — the ST/AoE priority below; NOT yet re-pulled at 12.1)
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-spec-builds-talents  # tier 3, patch 12.1, upd. 2026-08-10 — post-nerf hero-tree split (Soul Harvester ~3% ST, Diabolist for M+)
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, patch 12.1, upd. 2026-08-10 — priority corroboration
  - https://maxroll.gg/wow/class-guides/demonology-warlock-mythic-plus-guide  # tier 3 — ⚠ 12.1 capture still repeats the PRE-nerf "Diabolist better in all scenarios" line
  - https://maxroll.gg/wow/class-guides/demonology-warlock-raid-guide  # tier 3 — same, "almost all scenarios"
  - https://www.method.gg/guides/demonology-warlock/interface-and-macros  # tier 3, upd. 2026-04-26 — CDM tracklist + macros
  - https://www.kalamazi.gg/guides/addons  # tier 3, Demo CDM / Edit Mode / Better CDM imports
  - https://wago.io/browse/cooldown-manager/classes/warlock/demonology
  - https://wago.io/mLLnL5_Jt  # KatUI Demonology Warlock COOLDOWN-MANAGER
confidence: medium
---

# Demonology — rotation & CDM (Midnight 12.1 "Curse of Ula'tek")

> Pairs with `builds.md` (talents/loadouts) and `gearing.md` (stats/trinkets/
> tier set). Live patch **12.1** (went live 2026-08-11; **Season 2 opens
> 2026-08-18** — this file is spec mechanics only and is not season-gated).
> The priority below is **distilled from the Tier-1 SimulationCraft default APL**
> (`MID1_Warlock_Demonology`, commit 48103ef, 2026-05-18) — the same source the
> other warlock/DH rotations use. The default profile is **Diabolist**; the APL
> also ships a `soulharvest` list (see below).
>
> ⚠ **Confidence is `medium`, not `high`, for two reasons:** (1) the simc APL has
> **not** been re-pulled since 12.1 shipped, so the *ordering* below predates the
> tuning pass — the structure is unchanged but the weights behind it moved; and
> (2) 12.1's Diabolist nerf flipped the hero-tree verdict for single target and
> the Tier-3 guides do not yet agree with each other (see below).

## What 12.1 changed for Demonology

Tier-1, from the Curse of Ula'tek content update notes (verbatim in
`_meta/patch-notes/12.1.md`). **All of these are PvE — the PvP snare lines in the
same notes are PvP-only and are deliberately not written into this file.**

**Spec tuning — the filler got much better:**

- **Shadow Bolt +45%**
- **Demonbolt +55%**
- **Summon Gloomhound +35%** (the *Mark of Shatug* half of the Vilefiend choice
  node; *Mark of F'harg* / Charhound was not touched — see `builds.md`)

Net: the two things you cast when nothing else is up are worth substantially
more than they were on 12.0.7. This does **not** reorder the priority — filler
still sits at the bottom — but it raises the cost of *wasting* GCDs and lowers
the relative value of squeezing marginal extra imps out of a ragged Tyrant setup.

**Diabolist hero tree — nerfed:**

- **Chaos Salvo −20%**, **Felseeker −20%** (the Pit Lord's attack), **Wicked
  Cleave −20%**, **Eye Explosion −20%** — i.e. the Demonic-Art summons' payoff
  damage across the board.
- **Flames of Xoroth** now increases Fire damage and your demons' damage by
  **3%** (was 4%).

Ruination itself was not tuned, but everything the Demonic-Ritual → Overlord /
Mother of Chaos / Pit Lord chain lands on is 20% smaller.

**Warlock class-wide (all specs):**

- **Drain Life health drain +25%.**
- **Soul Leech correctness pass.** Several things that *should* have fed Soul
  Leech's absorb now do: **Wild Imp** and **Imp Gang Boss**' Fel Firebolt,
  **Imp Lord's Greater Felbolt**, **Demonic Tyrant's Demonfire**, **Vilefiend's
  Headbutt and Bile Spit**, **Gloomhound's Gloom Slash**, and **Infernal Bolt**.
  For Demo specifically this is a real passive-survivability gain — your absorb
  now scales with the demon army rather than just with your own casts, and it is
  largest exactly when the board is fullest (inside Tyrant).
  Going the other way, **Legion Strike** (Felguard) and **Cunning Cruelty** no
  longer erroneously grant Soul Leech.
- **Summon Demonic Gateway is now a Utility spell by default in the Cooldown
  Manager** — see the CDM section.

**Four global changes that apply to every spec** (they sit above the per-class
lists in the notes and are easy to miss):

1. **Player health and creature damage both +25% at max level**, with health
   consumables rescaled to match and some DPS/Tank healing and absorb spells
   retuned. ⚠ Any absolute HP / heal-for-N number written before 2026-08-11 is
   now wrong. Practically: **Burning Rush and Drain Life self-management are
   tuned against a bigger pool taking bigger hits** — the Burning Rush cancel
   macro below matters more, not less.
2. **Major DPS cooldowns lowered, steady-state damage raised** across several
   specs, as a stated design direction. Demo's own version of this is the
   Shadow Bolt / Demonbolt buff against the Diabolist burst nerf: **less of your
   damage lives inside the Tyrant window than it did on 12.0.7.**
3. **All class interrupts now show a "missed" visual over the target's head and
   play a distinct sound** when used while the target was not casting — this
   applies to **Axe Toss** (Felguard), including the focus macro below.
4. **Diminishing-return categories now reset after 20 seconds** (was 16) — this
   affects **Shadowfury** stun chaining and Axe Toss' stun component.

## Core idea

Demo is a builder/spender pet-army spec. You build **Soul Shards**, spend
them on **Hand of Gul'dan** (summons Wild Imps), and funnel everything
into the **Summon Demonic Tyrant** window (1-min CD), which empowers and
extends every active demon. The single biggest DPS lever is **how many
Hand of Gul'dan casts you fit inside the Tyrant window** — enter it with
demon-generation ready, not starved.

> **12.1 adjusts the emphasis, not the identity.** Tyrant is still the lever, but
> with Diabolist's payoff cut 20% and Shadow Bolt / Demonbolt up 45–55%, a
> *slightly* worse Tyrant that cost you no filler GCDs now beats a *slightly*
> better one you stood still to set up.

## Hero trees — what the APL actually does

The APL branches at the top: `diabolist` (if `talent.diabolic_ritual`) vs
`soulharvest` (if `talent.demonic_soul`). They share the pet-summon core
(Implosion sits on the identical 6-imp / 3+-target gate in both); the difference
is the payoff emphasis:

- **Diabolist — still the M+ / AoE pick, even after the nerf.** Adds
  **Ruination** and front-loads damage through the Demonic-Ritual → Overlord /
  Mother of Chaos / Pit Lord procs, making **burst through Summon Demonic Tyrant
  a lot stronger**. This is the profile's default
  (`MID1_Warlock_Demonology_Diabolist`).
- **Soul Harvester — no longer just the niche pick.** Mechanically it emphasizes
  **Implosion and AoE damage** via the passive **Demonic Soul** line and carries
  **better defensives**. It was behind everywhere on 12.0.7; **12.1's −20% pass
  across the Diabolist demon attacks was explicitly a lever to raise it**, and it
  now edges ahead in pure single target while staying substantially worse at
  cleave.

> ### ⚠ The 12.1 hero-tree verdict is genuinely in flux — read this before picking
>
> **What is Tier 1 and settled:** Diabolist's Chaos Salvo / Felseeker / Wicked
> Cleave / Eye Explosion each lost **20%**, and Flames of Xoroth went 4% → 3%.
> That is a real, sizeable cut to the tree's whole payoff, and nothing comparable
> was done to Soul Harvester. The gap closed.
>
> **What is Tier 3 and not yet agreed:** where it closed *to*.
> - **Icy Veins** (page tagged **12.1**, updated **2026-08-10**) splits them:
>   **Soul Harvester ~3% ahead in pure single target**, but with "substantially
>   worse cleave"; **Diabolist is "the better choice at any key level"** for M+.
> - **maxroll**'s 12.1 captures in this directory (`maxroll-mplus.md`,
>   `maxroll-raid.md`, both re-fetched 2026-08-11) **still carry the pre-nerf
>   line** — "Diabolist performs slightly better in all scenarios" / "almost all
>   scenarios". That text was not rewritten for the nerf; **do not read it as a
>   post-12.1 verdict.** (Expected — the ledger flagged that guide authors would
>   not have updated on day 1.)
>
> **Working guidance until a 12.1 simc APL or logs data lands:** **Diabolist for
> Mythic+ and anything with sustained cleave; Soul Harvester is now a live
> option for pure single-target raid, on a margin (~3%) small enough that
> comfort and its better defensives are a legitimate tiebreaker.** Re-check once
> `sims.md` is re-pulled at 12.1.

## Single-target priority (Diabolist, 12.1)

From `actions.diabolist`, single-target reading. **The ordering is unchanged by
12.1** — the patch tuned damage, not the APL's structure — but see the 12.1 note
under the list, and treat this as pre-12.1-APL until `sims.md` is re-pulled.

1. **Power Siphon** when Demonic Core stacks are low (≤1) — converts 2 Wild Imps
   into Demonic Core charges to fuel the next Demonbolt/Hand of Gul'dan.
2. **Hand of Gul'dan** immediately if **Dominion of Argus** (apex) is up — the
   proc makes it free/empowered.
3. **Grimoire: Fel Ravager** — the single-target grimoire summon (a Fel Ravager
   pet; turns into Devour Magic on cooldown). *This replaces the old "Grimoire:
   Felguard" naming.*
4. **Summon Doomguard** on cooldown — a **new Midnight ~2-min** demon cooldown
   the older guide was missing entirely; a big chunk of burst.
5. **Call Dreadstalkers** — with Reign of Tyranny, timed so the pair lands just
   before Tyrant (cast when Tyrant is ≥~20s away or ≤~12s away, not mid-window).
6. **Summon Demonic Tyrant at 5 Soul Shards** — the primary cooldown; enter it
   with a full board (Dreadstalkers + grimoire demons freshly out, imps banked).
7. **Implosion at ≥6 Wild Imps** *only* if 3+ targets or **To Hell and Back**
   talented (on pure ST without To Hell and Back, let imps keep attacking).
8. **Ruination** (Diabolist burst finisher) when available.
9. **Hand of Gul'dan at ≥3 Soul Shards** (its cost is **3**) when Tyrant is >5s
   away, or at 5 shards to avoid overcapping — your imp generator, maximized
   inside the Tyrant window. *(Old guide said 4–5; the shard cost is 3.)*
10. **Infernal Bolt if <3 Soul Shards** — the shard-refill builder.
11. **Demonbolt** with a **Demonic Core** proc and <4 shards (spend cores so they
    don't overcap; with Doom talented, prefer a target without the Doom debuff).
12. **Shadow Bolt** filler (→ Infernal Bolt) to rebuild shards.

**Tyrant window rule:** go in with **2+ Demonic Core charges** so you can chain
Hand of Gul'dan fast and pump the summon count over the duration.

**12.1 note on the bottom of the list.** Steps 11–12 (**Demonbolt +55%**,
**Shadow Bolt +45%**) are the biggest single-ability buffs in the patch for this
spec, and step 10's **Infernal Bolt now grants Soul Leech** as well. They stay
*last* — you never cast filler over a summon or over Hand of Gul'dan — but the
penalty for a GCD spent badly is now higher, and a clean, uninterrupted filler
stream between cooldowns is worth more of your total damage than it was on
12.0.7. Combined with the Diabolist −20%, **the burst-vs-sustained split has
moved toward sustained**; do not throw away filler GCDs to force a marginally
better Tyrant.

Corroboration (Icy Veins, 12.1, upd. 2026-08-10) reads the same list with two
looser thresholds — Power Siphon at **≤2** Demonic Core with ≥2 Wild Imps out,
Hand of Gul'dan at **4–5** shards, Infernal Bolt at **≤2** shards. Where they
differ, **the simc APL above is the higher-tier source**; the Icy Veins numbers
are the human-playable rounding of the same shape. (Its Hand of Gul'dan "4–5"
is a *hold* threshold, not the spell's cost — the cost is **3**.)

## AoE / Mythic+ priority

The priority is **largely the same** across target counts — Demo is a "passive
cleave" spec; your demons hit everything. The one big addition already sits in
the ST list above:

- **Implosion at ≥6 Wild Imps** (3+ targets) — sacrifices imps for burst AoE;
  on heavy multi-target this beats letting imps keep auto-attacking.
- **Grimoire: Imp Lord** is the **AoE grimoire summon** (vs Fel Ravager for ST) —
  a talent choice; the APL lists both and only the talented one fires.
- **Diabolist** front-loads burst via the Demonic-Ritual → **Overlord / Mother of
  Chaos / Pit Lord** summons inside Tyrant — pop your big AoE on the pull/Tyrant
  overlap. ⚠ **12.1 cut each of those summons' attacks by 20%** (Wicked Cleave,
  Chaos Salvo, Eye Explosion, Felseeker) and Flames of Xoroth 4% → 3%, so this
  spike is meaningfully smaller than on 12.0.7 — **Diabolist is still the M+
  pick** (its cleave lead over Soul Harvester survived the cut), just a flatter
  one.
- Hold **Tyrant** a few seconds for the pull to connect rather than wasting it on
  one target.

## Soul Harvester differences (`actions.soulharvest`)

Same opener (Power Siphon → Dominion-of-Argus Hand of Gul'dan → Grimoire
Fel Ravager/Imp Lord → **Summon Doomguard** → Call Dreadstalkers → Summon
Demonic Tyrant → Implosion gate → Hand of Gul'dan → Infernal Bolt/Demonbolt/
Shadow Bolt), but **no Ruination** and Tyrant/Dreadstalkers are cast plainly on
CD (no Reign-of-Tyranny timing gate). Damage comes from the passive Demonic
Soul line rather than a burst finisher.

**12.1:** Soul Harvester itself was **not tuned** — it gained ground purely by
Diabolist losing 20% off its demon attacks, plus the shared Shadow Bolt /
Demonbolt buffs, which the flatter Soul Harvester profile leans on more. This is
the list to use if you take the single-target-raid branch of the hero-tree
guidance above. Its lack of Ruination means **less to hold for the pull**, which
is also why its cleave stays behind.

## CDM (Cooldown Manager) setup — Midnight 12.1

The built-in **Cooldown Manager** (Blizzard's CDM, expanded in Midnight)
plus the **Better Cooldown Manager** addon are the standard combo. What to
track for Demo (Method, 2026-04-26):

- **Soul Shards** (resource — gates your whole rotation)
- **Demonic Core** procs/stacks (your Demonbolt/Infernal Bolt trigger)
- **Dreadstalkers / Grimoire (Fel Ravager · Imp Lord) / Doomguard / demon durations**
- **Summon Demonic Tyrant** cooldown
- **Diabolist rituals & secondary effects** (Overlord/Pit Lord/Ruination procs)
- Cast bar + player/target frames

### What 12.1 changed in the CDM

- **`Summon Demonic Gateway` is now a Utility spell by default** — Blizzard
  re-categorized it, so it moves out of your cooldown/essential rows into the
  utility row unless you had already overridden it. If your gateway icon "went
  missing" after the patch, this is why; it moved, it was not removed.
- **The CDM now tracks trinkets, potions and racial cooldowns/durations**
  natively, and trinkets / health potions / combat potions / healthstones can be
  **pinged** from it. For Demo this means your on-use trinket and Healthstone no
  longer need a separate tracker.
- New **"Short" sounds** category, and CDM sounds are now usable by the **Combat
  Audio Assist** accessibility feature — useful for Demonic Core procs.
- New ping slash commands **`/pingspell:<id|name>`** and **`/pingitem:<id|name>`**,
  and ping macros accept **`[@cursor]`**.

*(Destruction, not Demo, also got Shadowburn added to and Conflagration of Chaos
removed from the CDM in 12.1 — noted here only so it isn't mistaken for a Demo
change.)*

### Ready-made imports (copy-to-clipboard / wago)

- **Kalamazi addons page** has three Demo imports: **"Demonology CDM"**,
  **"Demonology Edit Mode"**, and **"Demonology Better Cooldown Manager
  (Addon)"** — https://www.kalamazi.gg/guides/addons (most current; matches
  the M+ build in `builds.md`).
- **wago.io Demo cooldown-manager browse:**
  https://wago.io/browse/cooldown-manager/classes/warlock/demonology
- **KatUI Demonology Warlock — COOLDOWN-MANAGER:** https://wago.io/mLLnL5_Jt

> Import strings are copy-button/JS-gated on those pages, so they're not
> cached here — grab them live in-game. Verify the profile's patch tag is
> **12.1 / Midnight** before importing. ⚠ A profile authored on **12.0.x** will
> still place Summon Demonic Gateway by its old category and will not know about
> the new trinket/potion/racial tracking — re-check those two rows after import.

## Useful macros (Method)

- Drain Life + `/cancelaura Burning Rush` (don't bleed out while channel-healing).
  **12.1: Drain Life's health drain is +25%**, against a **+25% larger max-health
  pool taking +25% creature damage** — the macro is more valuable, and the
  self-heal is roughly keeping pace rather than getting ahead.
- `/cast [@focus] Axe Toss` (Felguard interrupt on focus). **12.1: a whiffed
  interrupt now shows a "missed" visual over the target's head and plays a
  distinct sound** — you get immediate feedback that you kicked nothing, so stop
  pre-kicking on cooldown.
- Mouseover cast variants
- `/cast [@cursor] Shadowfury` (instant AoE stun placement). **12.1: DR
  categories now reset after 20s (was 16)** — the stun DR window is 4s longer, so
  Shadowfury/Axe Toss stun chains diminish for longer than they used to.

## Staleness & verification note (12.1)

**No talent was added to or removed from Demonology in 12.1.** The generated
`talents.md` / `talents.json` / `ability-inventory.md` in this directory (Blizzard
Game Data API + wago `Trait*` DB2 @ `12.1.0.69214`) are **Tier 1 and are the
floor** for whether an ability or talent exists; every name used above was
checked against them. Notably still present and unchanged in structure: the
`Implosion / Power Siphon` choice node, `Grimoire: Imp Lord / Grimoire: Fel
Ravager`, `Summon Doomguard`, `To Hell and Back`, `Reign of Tyranny`,
`Dominion of Argus`, `Diabolic Ritual` → `Ruination`, and the
`Mark of Shatug / Mark of F'harg` Vilefiend choice (Shatug = **Gloomhound**, the
one 12.1 buffed by 35%).

**What is *not* re-verified at 12.1:**

- The distilled APL is still **commit 48103ef (2026-05-18)** — a 12.0.5-era pull.
  The simc midnight branch lags live (see `sims.md`, itself flagged for regen).
  12.1's tuning is large enough (Demonbolt +55%, Shadow Bolt +45%, Diabolist
  −20%) that **a re-pull could move thresholds even though it will not reorder
  the list** — this is the main reason this file is `confidence: medium`.
- The **hero-tree verdict** — see the flux box above. Tier-3 sources disagree
  and no 12.1 logs data exists yet on patch day.
- **`sims.md` numbers are pre-12.1 and should not be quoted** for the
  Diabolist/Soul Harvester comparison until regenerated.

**Historical:** 12.0.7's only Demonology tuning was **PvP-only** (Shadow Bolt
+200%, Demonbolt +30% *in PvP combat*). 12.1's Shadow Bolt / Demonbolt buffs are
**not** that — they are unqualified PvE buffs. 12.1's own PvP-only Warlock lines
(the game-wide snare tier-down) are deliberately excluded from this file.

## TODO

- [ ] Capture an actual CDM import string into the KB if one becomes
      cacheable (currently behind copy buttons on Kalamazi/wago).
- [ ] **Re-distill the priority once the simc midnight branch publishes a
      post-12.1 Demo APL** (was: post-12.0.7 — still open, now at a newer patch).
      Same pass should regenerate `sims.md`.
- [ ] **Settle the 12.1 hero-tree verdict** once a 12.1 APL or Season-2 logs data
      lands: does Soul Harvester's ~3% single-target edge (Icy Veins, Tier 3)
      hold, and where exactly does Diabolist's cleave lead reassert? Update the
      flux box above and `builds.md` together.

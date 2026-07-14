---
title: Demonology Warlock — rotation & CDM setup (Midnight S1)
patch: 12.0.7
fetched: 2026-07-14
reviewed: 2026-07-14
sources:
  - simc midnight branch profiles/MID1/MID1_Warlock_Demonology.simc  # tier 1 APL, commit 48103ef 2026-05-18 (distilled — the ST/AoE priority below)
  - https://maxroll.gg/wow/class-guides/demonology-warlock-mythic-plus-guide  # tier 3 — Diabolist "slightly better in all scenarios" (M+ hero-tree verdict)
  - https://maxroll.gg/wow/class-guides/demonology-warlock-raid-guide  # tier 3 — Diabolist "slightly better in almost all scenarios" (raid)
  - https://www.method.gg/guides/demonology-warlock/interface-and-macros  # tier 3, upd. 2026-04-26 — CDM tracklist + macros
  - https://www.kalamazi.gg/guides/addons  # tier 3, Demo CDM / Edit Mode / Better CDM imports
  - https://wago.io/browse/cooldown-manager/classes/warlock/demonology
  - https://wago.io/mLLnL5_Jt  # KatUI Demonology Warlock COOLDOWN-MANAGER
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes  # tier 1, 12.0.7 Demo changes: PvP-only
confidence: high
---

# Demonology — rotation & CDM (Midnight Season 1)

> Pairs with `builds.md` (talents/loadouts) and `gearing.md` (stats/trinkets/
> tier set). Live patch 12.0.7. Priority below is **distilled from the Tier-1
> SimulationCraft default APL** (`MID1_Warlock_Demonology`, commit 48103ef,
> 2026-05-18) — the same source the other warlock/DH rotations use. The default
> profile is **Diabolist**; the APL also ships a `soulharvest` list (see below).

## Core idea

Demo is a builder/spender pet-army spec. You build **Soul Shards**, spend
them on **Hand of Gul'dan** (summons Wild Imps), and funnel everything
into the **Summon Demonic Tyrant** window (1-min CD), which empowers and
extends every active demon. The single biggest DPS lever is **how many
Hand of Gul'dan casts you fit inside the Tyrant window** — enter it with
demon-generation ready, not starved.

## Hero trees — what the APL actually does

The APL branches at the top: `diabolist` (if `talent.diabolic_ritual`) vs
`soulharvest` (if `talent.demonic_soul`). They share the pet-summon core
(Implosion sits on the identical 6-imp / 3+-target gate in both); the difference
is the payoff emphasis:

- **Diabolist — the default for M+ *and* raid.** Adds **Ruination** and
  front-loads damage through the Demonic-Ritual → Overlord / Pit Lord procs,
  making **burst through Summon Demonic Tyrant a lot stronger**. maxroll: Diabolist
  "performs slightly better in **all scenarios**" (M+) / "almost all scenarios"
  (raid), and murlok top-player data agrees — so it's the pick for **M+ and AoE
  too**, not just single target. This is the profile's default
  (`MID1_Warlock_Demonology_Diabolist`).
- **Soul Harvester — Implosion/AoE *emphasis*, but currently behind.**
  Mechanically it "emphasizes Implosion and AoE damage" (maxroll) via the passive
  **Demonic Soul** line and carries **better defensives**, yet it sims slightly
  worse than Diabolist across the board — the niche / solo-defensive alternative,
  not the M+ default (see `builds.md` / `gearing.md`).

> Corrects the earlier write-up's burst attribution: **Diabolist** is the burst
> tree (Ruination) *and* the better performer everywhere per maxroll + murlok.
> Soul Harvester's "AoE" reputation is a mechanical *emphasis* (Implosion), not a
> throughput win — don't route to it for M+/AoE.

## Single-target priority (Diabolist, 12.0.7)

From `actions.diabolist`, single-target reading:

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

## AoE / Mythic+ priority

The priority is **largely the same** across target counts — Demo is a "passive
cleave" spec; your demons hit everything. The one big addition already sits in
the ST list above:

- **Implosion at ≥6 Wild Imps** (3+ targets) — sacrifices imps for burst AoE;
  on heavy multi-target this beats letting imps keep auto-attacking.
- **Grimoire: Imp Lord** is the **AoE grimoire summon** (vs Fel Ravager for ST) —
  a talent choice; the APL lists both and only the talented one fires.
- **Diabolist** front-loads burst via the Demonic-Ritual → **Overlord / Pit
  Lord** summons inside Tyrant — pop your big AoE on the pull/Tyrant overlap.
- Hold **Tyrant** a few seconds for the pull to connect rather than wasting it on
  one target.

## Soul Harvester differences (`actions.soulharvest`)

Same opener (Power Siphon → Dominion-of-Argus Hand of Gul'dan → Grimoire
Fel Ravager/Imp Lord → **Summon Doomguard** → Call Dreadstalkers → Summon
Demonic Tyrant → Implosion gate → Hand of Gul'dan → Infernal Bolt/Demonbolt/
Shadow Bolt), but **no Ruination** and Tyrant/Dreadstalkers are cast plainly on
CD (no Reign-of-Tyranny timing gate). Damage comes from the passive Demonic
Soul line rather than a burst finisher.

## CDM (Cooldown Manager) setup — Midnight

The built-in **Cooldown Manager** (Blizzard's CDM, expanded in Midnight)
plus the **Better Cooldown Manager** addon are the standard combo. What to
track for Demo (Method, 2026-04-26):

- **Soul Shards** (resource — gates your whole rotation)
- **Demonic Core** procs/stacks (your Demonbolt/Infernal Bolt trigger)
- **Dreadstalkers / Grimoire (Fel Ravager · Imp Lord) / Doomguard / demon durations**
- **Summon Demonic Tyrant** cooldown
- **Diabolist rituals & secondary effects** (Overlord/Pit Lord/Ruination procs)
- Cast bar + player/target frames

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
> **12.0.x / Midnight** before importing.

## Useful macros (Method)

- Drain Life + `/cancelaura Burning Rush` (don't bleed out while channel-healing)
- `/cast [@focus] Axe Toss` (Felguard interrupt on focus)
- Mouseover cast variants
- `/cast [@cursor] Shadowfury` (instant AoE stun placement)

## 12.0.7 verification note

Checked against the Revelations (12.0.7) content-update notes: the only
Demonology tuning in 12.0.7 is **PvP-only** — Shadow Bolt +200% and Demonbolt
+30% *in PvP combat* (a freecasting buff so Demo can punish enemies who let it
chain casts). **No PvE rotation, Tyrant-window, or filler-choice change**, so
the priority above stands. Demonbolt vs Infernal Bolt remains a build/talent
choice (see `builds.md`), not something 12.0.7 altered.

> Staleness: the distilled APL is from commit 48103ef (2026-05-18); the simc
> midnight branch can lag the live patch (see `sims.md`). No PvE Demo change
> shipped between then and 12.0.7 live, so the priority is current.

## TODO

- [ ] Capture an actual CDM import string into the KB if one becomes
      cacheable (currently behind copy buttons on Kalamazi/wago).
- [ ] Re-distill if the simc midnight branch publishes a post-12.0.7 Demo APL.

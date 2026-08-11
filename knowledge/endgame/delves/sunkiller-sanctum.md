---
title: Sunkiller Sanctum (delve)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://www.icy-veins.com/wow/sunkiller-sanctum-delve-guide  # upd. 2026-05-19
  - https://www.method.gg/guides/sunkiller-sanctum-delve-guide
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281  # 12.1 Curse of Ula'tek content update notes (Tier 1) — new snake/venom variants; CLASSES preamble global retune
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214  # Tier 1 game data — S2 Mistcrest bands 269-334 vs S1 Dawncrest 224-289
confidence: medium
---

# Sunkiller Sanctum

**Location:** Voidstorm, east side, **next to the Voidspire raid
entrance**. Runs the standard delve tier ladder. ⚠ **How far up that
ladder you can go this pre-season week is an open Tier-1 conflict** —
the Season-1-ending post says tiers **1–11** plus the "?" Nemesis
difficulty, the 12.1 content-update notes read as a **Tier-7** ceiling
until Season 2 opens 2026-08-18. `delves/overview.md` carries the
conflict verbatim and an `@verify-ingame` on it; **check the highest
selectable tier at the entrance before planning around T8+**. Which
tiers/Nemesis rungs are open and what they reward is a *season-wide*
fact, not a property of this delve.

Rolls **one of three story variants** on entry — you don't choose. Two
end in the boss **Esuritus**; one has no boss. Whole delve is
Void/Domanaar themed.

**12.1 (Curse of Ula'tek, 2026-08-11):** there are **no delve-specific
changes here** — neither "Sunkiller Sanctum" nor "Esuritus" appears
anywhere in the 12.1 notes, so the three variants and the boss kit below
still describe the fight. Two things around it did move:

- **Trash:** 12.1 seeds **new snake and venom enemy variants** into the
  existing Midnight delves — expect Coiled-Isle-flavoured serpents mixed
  into the Void/Domanaar packs.
- **Global retune (applies to every spec and every instance, from the
  CLASSES preamble):** **player health and creature damage both +25% at
  max level**, with health consumables rescaled and some DPS/Tank
  healing/absorb spells adjusted; **major DPS cooldowns lowered and
  steady-state damage raised** for several specs; **interrupts now show a
  "missed" visual + sound** when the target wasn't casting (you will see
  this on a mistimed Spell Lock into Calling Bolt); **diminishing-return
  categories reset after 20s** (was 16), which lengthens the gap before
  Shadowfury lands full-duration on the same add cluster again.

Season-wide delve rules live in `delves/overview.md`, not here. The one
that bites this week: **no Bountiful delves and no Coffer Keys until
Season 2 opens 2026-08-18**, so the run's reward ceiling is
**Adventurer 3/6 gear (ilvl 272) + Veteran Mistcrests** no matter which
tier you run (`_meta/moving-values.md`, "Delve rewards (pre-season)").
The tier ceiling itself is the unresolved conflict flagged above.

## The boss: Esuritus (Core of the Problem & The Gravitational Effect)

One mechanic drives the whole fight: **everything he casts spawns
Voidcaller adds**, and the adds cast **Commune with the Void** to
empower him. The fight is **add control**, not a tank-and-spank.

| Ability | What it does | Do |
|---|---|---|
| **Calling Bolt** (a.k.a. Singular Bolt) | Interruptible cast; if it lands, **+1 Voidcaller** | **Interrupt every time** |
| **Coalescing Malediction** | Shadow DoT on you; **+1 Voidcaller** when it expires *or is dispelled* | Just let it run / heal through — note dispelling still spawns the add |
| **Crushing Rift** | Medium AoE ring around him, heavy damage; **+4 Voidcallers** | Move out immediately |
| **Gorge** | He **devours all living Voidcallers**, gaining a stacking damage buff per add eaten (~30s) | **All adds must be dead before this** — or he snowballs |

**The whole game:** interrupt Calling Bolt, kill Voidcallers as they
spawn, and make sure the field is **clear of adds before Gorge**. If
Gorge eats several adds he hits dramatically harder — that's what kills
you at high tiers, not his base damage.

(Source split, doesn't change play: Icy Veins names the interruptible
cast *Calling Bolt* / Method *Singular Bolt*; Gorge buff "~30s per add"
vs "5% per add" — either way, **don't feed Gorge**.)

## The three variants

- **Core of the Problem** — portal network for fast travel; collect
  Energized Cores (orbs grant **Core Empowered**: stacking move speed +
  damage reduction — grab them). Ends on **Esuritus**.
- **The Gravitational Effect** — use micro-singularities to move/stealth;
  collect Singularity Coils + activate stabilizers to **drop the boss's
  shields**, then kill **Esuritus**.
- **Not What I Expected** — **no boss**. Fight Lightbloom + Void enemies;
  objective is to kill **3 Corrupted Umbraroots** (single-pull them).
  This is the easy roll — just clear to completion.

## Delve tips (Affliction warlock)

⚠ **The difficulty calibration below was taken in Season 1 at ~242 ilvl,
where T8 was a comfortable clear and T9 was rough. It has not been
re-flown under 12.1, and T8 may not even be selectable this week** (see
the tier-ceiling conflict above). Two things moved it: the ilvl ladder
shifted +45 (S2 gear runs **269–334** vs S1's 224–289 — Mistcrest bands,
wago `CurrencyTypes` DB2 @ 12.1.0.69214), and the global retune raised
**creature damage +25%** against a **+25%** player health pool. Per-tier
rewards changed shape too — read them off `delves/overview.md`'s table
rather than from any S1 memory, and note its rows above Adventurer 3/6
are **Season 2, Bountiful-only** and unreachable before 2026-08-18.
Re-fly Sunkiller Sanctum at S2 ilvl and re-establish which delve tier is comfortable / which is rough. @verify-ingame

The *shape* of the fight is what's durable: the boss is the only real
check, and it's an interrupt/add fight — which Affliction handles well:

- **Set Valeera to DPS** here (not healer) so she helps interrupt
  Calling Bolt and burns Voidcallers — adds, not raw boss damage, are
  the threat. (Contrast Gulf of Memory's Mul'tha'ul, where you want her
  healing to dispel.)
- **Pet: Felhunter** for the extra interrupt (Spell Lock) on Calling
  Bolt, or **Voidwalker** if you'd rather it tank Voidcallers off you.
- **Seed of Corruption** is ideal for the Voidcaller spawns — pre-seed
  where they appear and they die in the AoE; **Shadowfury** to stun a
  fresh add cluster.
- **Don't bother dispelling Coalescing Malediction** even if you could
  (you can't decurse, but the point stands) — dispel still spawns an
  add; heal/leech through the DoT instead. *(12.1 pushes both sides of
  this: the DoT ticks harder under the +25% creature-damage pass, but
  Drain Life's health drain is **+25%**, Zevrim's Resilience healing
  **+25%**, and Unstable Affliction / Malefic Grasp now correctly grant
  **Soul Leech** — so the sustain is real, just untested here.)*
- **Before he casts Gorge, sweep the field** — make sure no Voidcaller
  is alive. If several slip, kite with Burning Rush and let the buff
  fall off before re-engaging. *(Under the 12.1 retune a fed Gorge hits
  a bigger health pool with bigger swings — assume less slack than the
  S1 note above implies until re-flown.)*
- Grab **Core Empowered** orbs (Core of the Problem variant) — the DR
  stacks are still worth taking, but confirm how much survivability Core Empowered's DR actually buys under the 12.1 +25% creature-damage retune. @verify-ingame

## TODO

- [ ] Trash pack specifics (neither tier-3 source detailed them) — now
  also needs the **12.1 snake/venom variants**: which packs they replaced
  and whether any bring a new interrupt/dispel check. @verify-ingame
- [ ] Confirm Gorge buff magnitude (30s/stack vs 5%/add)

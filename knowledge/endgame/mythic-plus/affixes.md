---
title: M+ Affixes — Midnight Season 1 (Xal'atath's Bargains & Guile)
patch: 12.0.7
fetched: 2026-06-21
sources:
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/
  - https://www.ssegold.com/wow-midnight-season-1-xalatath-bargain-affix-guide
  - https://www.wowhead.com/news/new-lindormis-guidance-mythic-affix-provides-basic-dungeon-route-in-midnight-379948
  - https://raider.io/news/740-midnight-mythic-plus-affixes
confidence: medium   # ladder structure + roles high (Icy Veins anchor + 2 corroborating); exact Bargain buff %s single-sourced (Conquest Capped) — verify in-game
---

# M+ Affixes — Midnight Season 1 (Xal'atath's Bargains & Guile)

This file explains **what each Midnight affix does and how to play around it.**
For the at-a-glance affix-by-key-level table, see
[`season-1-overview.md`](season-1-overview.md#affixes). For how keys
upgrade/deplete, see [`keystones.md`](keystones.md).

Midnight retired the old The War Within / Dragonflight affix pool entirely
(no more Spiteful, Sanguine, Afflicted, Incorporeal, etc.). Season 1 runs a
small, deliberately readable set: a low-key teaching affix, the
Fortified/Tyrannical scaling layer, four rotating **Xal'atath's Bargains**, and
a single high-key punishment affix, **Xal'atath's Guile**.

## How the affix ladder works

Affixes stack on as the key level climbs. The breakpoints (Icy Veins S1 guide,
corroborated by Conquest Capped and Raider.io, and matching this repo's table):

| Key level | What's active |
|-----------|---------------|
| **+2 to +4** | **Lindormi's Guidance** only (the teaching affix) |
| **+5 to +11** | One rotating **Xal'atath's Bargain** (Ascendant / Voidbound / Pulsar / Devour), **plus** Fortified **or** Tyrannical once you hit +7 |
| **+7 to +9** | Fortified **or** Tyrannical (whichever the week rolled) joins the Bargain |
| **+10 and up** | **Both** Fortified **and** Tyrannical active, every week |
| **+12 and up** | **Xal'atath's Guile** *replaces* the Bargain entirely; deaths cost 15s |

Two things rotate weekly: **which Bargain** is up (+5–11), and **which of
Fortified/Tyrannical** comes first at +7 (the other one always joins at +10).

The **+12 Guile breakpoint** is the big wall: the helpful/harmful Bargain
minigame disappears and is swapped for a flat death tax. From +12 up there are
no "tricks" left — just clean execution.

> **Breakpoint caveat:** one secondary snippet phrased it as "Bargain at +4,
> Guidance gone by +6." The Icy Veins anchor guide and this repo's table both
> say **Guidance +2–4, Bargain +5+** — I'm going with that consensus. The exact
> +4-vs-+5 handoff is worth a one-time in-game confirm.

## Each affix — what it does + how to play it

### Lindormi's Guidance (+2 to +4) — the teaching affix
Certain non-boss enemies are marked with **Temporal Sands**: they're visually
highlighted and take **−5% health and −5% damage done**. Killing *only* the
marked enemies fulfills **100% of the Enemy Forces (trash) count** — so the
marks literally draw you a viable route. It also **removes the death-timer
penalty**: deaths still cost you release/run-back time, but they don't add the
systemic timer hit. Counter-play: there's nothing to "beat" — follow the marked
mobs to learn the dungeon's pull order, and don't over-pull unmarked trash.

### Fortified (rotates in at +7)
Non-boss enemies get **roughly +20% health and up to +20% damage done.** Trash
packs become the hard part of the dungeon. Counter-play: interrupts, hard CC,
and tank/healer cooldowns on the big pulls; route around or skip the nastiest
packs since you don't have to kill everything.

### Tyrannical (rotates in at +7)
Bosses get **roughly +30% health and +15% damage done.** Boss fights turn into
DPS/survival checks. Counter-play: save Bloodlust and personal/raid defensives
for boss mechanics, line up burst windows on boss casts, and don't waste
cooldowns on trash you'll want for the boss.

> At **+10+ both are live at once** — every pull *and* every boss is buffed, so
> routes get conservative: smaller pulls, pre-planned CC, no "free" side of the
> dungeon.

### Xal'atath's Bargain (one of four, +5 to +11)
The Bargain is a **risk/reward minigame**: handle the spawned objects correctly
and your *party* gets a temporary buff; ignore them and the *enemies* get
buffed instead. The four variants rotate weekly.

**Ascendant** — Orbs cast **Cosmic Ascension** (~once/minute) that would buff
nearby enemies with **+20% movement speed and +20% Haste**. The absorb shield
on the orb is **too large to simply DPS down** — you must **stop the cast**.
Counter-play: interrupt, displace, purge, or otherwise control each cast; every
*prevented* cast instead grants your party **+2% movement/Haste, stacking to
+20% for 30s.** Bring kicks/stops.

**Voidbound** — A **Void Emissary** spawns and channels **Dark Prayer** to
empower nearby enemies. Counter-play: the whole group **swaps to the Emissary
and burns it down before its window expires, kicking every Dark Prayer cast.**
Kill it in time → party gains **~+30% ability cooldown rate and +20%
Versatility (30s)**; let it finish → enemies get a damage buff + damage
reduction.

**Pulsar** — Orbs **tether to players for ~15s**; the simplest Bargain, with a
generous window. Counter-play: **run to each other and soak/clear the pulsars**
(stacking is fine). Soaked → party gets **Mastery + Leech (30s)**; each unsoaked
orb instead gives enemies **+10% damage and ~20% damage reduction.**

**Devour** — **Devouring Rift** puts shield debuffs on **all five players**.
Counter-play: **remove the shields via healing or dispels** — but note this is
**not purely a healer affix**: traditional healer dispels only clear **two of
the five** shields, so players need to self-clear with personal
defensives/effects (e.g. Stoneform-type effects). Shields removed → that player
gets **+2% max health and +4% Crit (30s)**; shields left up instead **heal
nearby enemies ~10% of their health.**

> **Confidence note on Bargains:** the *roles* (Ascendant = interrupt,
> Voidbound = swap-and-kill, Pulsar = soak/stack, Devour = dispel/self-clear)
> are corroborated across Icy Veins and Conquest Capped. The exact **buff/debuff
> percentages and durations** come mainly from Conquest Capped (single source)
> and should be treated as approximate until confirmed against the in-game
> dungeon journal / wago.tools — hence this file's `confidence: medium`.

### Xal'atath's Guile (+12 and up)
At +12 the Bargain minigame is **gone** — replaced by a flat punishment:
**each player death subtracts 15 seconds directly from the remaining timer**
(up from the standard 5s death tax). The lost time **never comes back**, even
if you recover the pull. Counter-play: pure discipline. A single avoidable death
can effectively cost **50s+** (death + run-back + the 15s deduction), so greedy
pull chains and last-second risks get much more expensive. Play safe, pre-plan
defensive CDs, and treat every death as a timer hit, not just a body to res.

## Sources

- [Icy Veins — Midnight Mythic+ Season 1 Guide](https://www.icy-veins.com/wow/midnight-mythic-season-1-guide) (tier 3, anchor — ladder breakpoints + Bargain roles)
- [Conquest Capped — Midnight M+ Season 1](https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/) (tier 3 — per-Bargain mechanics + buff %s, Fort/Tyr scaling)
- [SSEGold — Xal'atath's Bargain Affix Guide](https://www.ssegold.com/wow-midnight-season-1-xalatath-bargain-affix-guide) (tier 4 — corroboration on Bargain counter-play + Guile 15s)
- [Wowhead — Lindormi's Guidance affix news](https://www.wowhead.com/news/new-lindormis-guidance-mythic-affix-provides-basic-dungeon-route-in-midnight-379948) (tier 3/4 — Guidance details)
- [Raider.io — Mythic+ Affixes (Season 1)](https://raider.io/news/740-midnight-mythic-plus-affixes) (tier 2/3 — breakpoint corroboration)

## TODO

- [ ] Confirm exact **Bargain buff/debuff percentages and durations** against
      the in-game dungeon journal or wago.tools (currently single-sourced from
      Conquest Capped). Bump to `confidence: high` once verified.
- [ ] Confirm the **+4 vs +5** handoff between Guidance and the first Bargain
      in-game.
- [ ] Confirm Fortified/Tyrannical exact scaling %s (trash +20% HP / boss +30%
      HP, +15% dmg) for 12.0.7 — values are standard but unverified vs a
      Midnight-specific tooltip.

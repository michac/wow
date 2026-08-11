---
title: M+ Affixes — Midnight (Season 1 set; Season 2 carry-over unconfirmed)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24271855/12-0-5-content-update-notes
  - https://worldofwarcraft.com/en-us/news/24294369
  - https://www.icy-veins.com/wow/midnight-mythic-season-2-guide
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-2/
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/
  - https://www.ssegold.com/wow-midnight-season-1-xalatath-bargain-affix-guide
  - https://www.wowhead.com/news/new-lindormis-guidance-mythic-affix-provides-basic-dungeon-route-in-midnight-379948
  - https://raider.io/news/740-midnight-mythic-plus-affixes
confidence: medium   # Lindormi's Glow is Tier-1 (12.0.5 notes); S1 ladder + roles high (Icy Veins anchor + 2 corroborating); exact Bargain buff %s single-sourced; the S2 affix set is UNSETTLED — the 12.1 content-update-notes archive has no affix section, while the Tier-1 S2 overview blog says "Season 2 brings about new Affixes" under Prey. Live confirmation once keys drop 2026-08-18
---

# M+ Affixes — Midnight

This file explains **what each Midnight affix does and how to play around it.**
For how keys upgrade/deplete, see [`keystones.md`](keystones.md). The Season 1
at-a-glance table lives in [`season-1-overview.md`](season-1-overview.md#affixes)
(now historical); the Season 2 dungeon pool lives in
[`season-2-overview.md`](season-2-overview.md).

## ⚠ Season status (as of 2026-08-11)

**Midnight Season 1 ended with the week-of-Aug-11 maintenance. Mythic+ Season 2
does not open until the week of 2026-08-18.** During the pre-season week the new
S2 dungeon pool is live on Heroic and Mythic 0 only — **keystones do not drop,
so no M+ affix is active in the game right now.** (Tier 1: the 12.1 content
update notes / S1-ending blue post.)

**The Season 2 affix set is not settled, and the two Tier-1 signals point
opposite ways.** Everything below is the **verified Season 1 set**; its
Season-2 status is as follows:

- **Tier-1, negative:** the **content-update-notes archive**
  (`_meta/patch-notes/12.1.md`) contains **no affix section at all** — zero
  case-insensitive occurrences of "affix", checked 2026-08-11. The notes
  therefore neither confirm nor re-tune an M+ affix set.
- **Tier-1, ambiguous counter-signal:** the **Midnight Season 2 overview blog**
  ([news/24294369](https://worldofwarcraft.com/en-us/news/24294369)) does carry
  one affix sentence — *"Season 2 brings about new Affixes, four new targets in
  Nightmare Mode, and some new hunts on the Coiled Isle in Prey."* It sits under
  the **Prey** heading, so read in place it scopes to Prey's Nightmare affixes
  rather than the Mythic+ ladder — but the wording is loose enough that it may
  cover both. It is **the only Tier-1 affix signal for the season**, and it is a
  counter-signal to "the M+ affixes are unchanged", not a confirmation of a new
  M+ set. ([`season-2-overview.md`](season-2-overview.md#affixes) records the
  same sentence and the same reading.)
- **Tier-3:** two Season 2 guides published shortly before launch (Icy Veins,
  2026-08-05; Conquest Capped, updated 2026-08-02) both describe the **same
  ladder carrying over unchanged** — Lindormi's Guidance on low keys, a rotating
  Xal'atath's Bargain from +5, Fortified/Tyrannical from +7, both at +10,
  Xal'atath's Guile from +12 — and neither lists any **new** M+ affix for S2.
- That is **pre-season reporting, not confirmation**, and it sits against the
  blog line above. Do not answer "the S2 affixes are X" as settled fact — in
  either direction — until the season is live and the ladder has been read off
  the in-game keystone tooltip.
  @verify-ingame Read the Season 2 M+ affix ladder off the in-game keystone tooltip once keys drop (week of 2026-08-18).

## How the affix ladder works

Affixes stack on as the key level climbs. Breakpoints below are the **Season 1**
ladder (Icy Veins S1 guide, corroborated by Conquest Capped and Raider.io); the
S2 guides describe the same ladder.

| Key level | What's active |
|-----------|---------------|
| **+2 to +4** | **Lindormi's Guidance** only (the teaching affix) |
| **+5 to +6** | One rotating **Xal'atath's Bargain** (Ascendant / Voidbound / Pulsar / Devour) |
| **+7 to +9** | The Bargain, **plus** Fortified **or** Tyrannical (whichever the week rolled) |
| **+10 to +11** | The Bargain, plus **both** Fortified **and** Tyrannical, every week |
| **+12 and up** | **Xal'atath's Guile** *replaces* the Bargain entirely; both Fortified and Tyrannical stay; deaths cost 15s |

Two things rotate weekly: **which Bargain** is up (+5–11), and **which of
Fortified/Tyrannical** comes first at +7 (the other one always joins at +10).

The **+12 Guile breakpoint** is the big wall: the helpful/harmful Bargain
minigame disappears and is swapped for a flat death tax. From +12 up there are
no "tricks" left — just clean execution.

> **Breakpoint caveat (still open).** Sources disagree on where Guidance stops.
> Icy Veins (both the S1 and the 2026-08-05 S2 guide) says **+2 to +4**, and
> that's what this table and the repo's S1 table carry. Conquest Capped's S2
> guide instead says Guidance is **removed at +6** — i.e. active +2 through +5,
> overlapping the first Bargain. A third secondary snippet says "Bargain at +4,
> Guidance gone by +6." The exact handoff is worth a one-time in-game confirm
> once keys are live.
>
> @verify-ingame Confirm where Lindormi's Guidance stops (+4 or +5) off the affix's own −5% health / −5% damage tooltip, not off enemy highlighting.
>
> Note that **route highlighting persisting above the Guidance breakpoint is not
> evidence for the later cutoff** — that is **Lindormi's Glow** (Tier 1, shipped
> in 12.0.5, see below), which highlights enemy forces *precisely when Guidance
> is inactive*. Only the affix's own **−5% health / −5% damage** and death-timer
> waiver mark where Guidance actually ends.

## Each affix — what it does + how to play it

> **Season scope for every heading below: this is the Season 1 set** (see the
> season-status banner above). Nothing here is live during the week of Aug 11 —
> keystones do not drop until Aug 18, and the S2 ladder is Tier-3 pre-season
> reporting until read off the in-game tooltip. The key-level ranges in the
> headings are the **Season 1** breakpoints.

> ⚠ **The 12.1 global retune moves the felt difficulty of every one of these,
> even though none of the affix percentages changed.** 12.1 raised **player
> health and creature damage by 25% at max level** (health consumables rescaled;
> some DPS/Tank healing and absorb spells retuned), lowered several specs' major
> DPS cooldowns while raising steady-state damage, added a **"missed" visual and
> sound to interrupts used while the target was not casting**, and moved
> **diminishing-return category resets to 20s (was 16s)**. All four apply in
> every instance. The interrupt and DR changes bear directly on affix
> counter-play (Ascendant's stops, Voidbound's Dark Prayer kicks, Fortified
> trash CC chains); the health/damage rescale means any *absolute* HP or
> healing figure written before 2026-08-11 is stale, though the affixes'
> *relative* multipliers below are unaffected.

### Lindormi's Guidance (Season 1: +2 to +4) — the teaching affix
Certain non-boss enemies are marked with **Temporal Sands**: they're visually
highlighted and take **−5% health and −5% damage done**. Killing *only* the
marked enemies fulfills **100% of the Enemy Forces (trash) count** — so the
marks literally draw you a viable route. It also **removes the death-timer
penalty**: deaths still cost you release/run-back time, but they don't add the
systemic timer hit. Counter-play: there's nothing to "beat" — follow the marked
mobs to learn the dungeon's pull order, and don't over-pull unmarked trash.

#### Lindormi's Glow — the route highlight *without* the affix (Tier 1, since 12.0.5)

**Lindormi's Glow is a shipped feature, not an affix**, added in patch **12.0.5**
and documented verbatim in the Tier-1 archive at
[`_meta/patch-notes/12.0.5.md`](../../_meta/patch-notes/12.0.5.md) (DUNGEONS AND
RAIDS › MYTHIC+). It **highlights select enemy forces
even when the Lindormi's Guidance affix is inactive**, and **defeating all
highlighted enemies completes the enemy-forces requirement** for a Keystone
Dungeon.

*(Reading, not verbatim: "even when Guidance is inactive" is what makes the
route-drawing usable above the Guidance breakpoint. The notes do not state a key
level, so do not write "at any key level" as a Tier-1 fact. Either way the Glow
carries **only** the highlight + enemy-forces credit — never Guidance's
−5%/−5% enemy debuff or its death-timer waiver, which are affix effects.)*

How it turns on (all three lines are verbatim Tier-1 mechanics):

- **Any player whose class supports a tank role specialization** can opt in by
  **speaking with Lindormi** near the Timeways portal, or at the end of a
  Keystone Dungeon.
- It **activates in a Keystone Dungeon if the party's tank has chosen to use the
  feature** — so the *opt-in* is tank-gated, but what activates is the **dungeon's
  highlight**, i.e. party-wide. (The notes describe it as activating in the
  dungeon, not on a player; "every member sees the marked forces" is the natural
  reading, not verbatim.)
- Opt back out by **speaking with Lindormi again**.

*(Do not describe this as a "tank-side highlight" or as an unconfirmed S2 rumor —
both framings were wrong here and are corrected as of 2026-08-11. It is two
patches old and Tier-1, **not season-scoped** — unlike the affix headings around
it, it is not part of the Season 1 set and nothing in the 12.1 notes changes it.)*

### Fortified (Season 1: rotates in at +7)
Non-boss enemies get **roughly +20% health and up to +20% damage done.** Trash
packs become the hard part of the dungeon. Counter-play: interrupts, hard CC,
and tank/healer cooldowns on the big pulls; route around or skip the nastiest
packs since you don't have to kill everything.

### Tyrannical (Season 1: rotates in at +7)
Bosses get **roughly +30% health and +15% damage done.** Boss fights turn into
DPS/survival checks. Counter-play: save Bloodlust and personal/raid defensives
for boss mechanics, line up burst windows on boss casts, and don't waste
cooldowns on trash you'll want for the boss.

> At **+10+ both are live at once** — every pull *and* every boss is buffed, so
> routes get conservative: smaller pulls, pre-planned CC, no "free" side of the
> dungeon.

### Xal'atath's Bargain (Season 1: one of four, +5 to +11)
The Bargain is a **risk/reward minigame**: handle the spawned objects correctly
and your *party* gets a temporary buff; ignore them and the *enemies* get
buffed instead. The four variants rotate weekly.

**Ascendant** — Orbs cast **Cosmic Ascension** (~once/minute) that would buff
nearby enemies with **+20% movement speed and +20% Haste**. The absorb shield
on the orb is **too large to simply DPS down** — you must **stop the cast**.
Counter-play: interrupt, displace, purge, or otherwise control each cast; every
*prevented* cast instead grants your party **+2% movement/Haste, stacking to
+20% for 30s.** Bring kicks/stops. *(Conquest Capped frames the full-credit
objective as stopping **10 Orbs of Ascendance** — single-sourced.)*

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
> are corroborated across Icy Veins and Conquest Capped in both the S1 and S2
> guides. The exact **buff/debuff percentages and durations** come mainly from
> Conquest Capped (single source) and should be treated as approximate until
> confirmed against the in-game dungeon journal / wago.tools —
> hence this file's `confidence: medium`. The Tier-1 12.1 notes contain **no
> affix-specific re-tune** of these numbers, so no S2 re-tune is assumed either
> way — but see the global-retune warning above: 12.1's +25% player health /
> creature damage pass changes how every one of these plays in absolute terms.

@verify-ingame Confirm the Xal'atath's Bargain buff/debuff percentages and durations (Ascendant, Voidbound, Pulsar, Devour) against the in-game dungeon journal.

### Xal'atath's Guile (Season 1: +12 and up)
At +12 the Bargain minigame is **gone** — replaced by a flat punishment:
**each player death subtracts 15 seconds directly from the remaining timer**
(up from the standard 5s death tax). The lost time **never comes back**, even
if you recover the pull. Counter-play: pure discipline. A single avoidable death
can effectively cost **50s+** (death + run-back + the 15s deduction), so greedy
pull chains and last-second risks get much more expensive. Play safe, pre-plan
defensive CDs, and treat every death as a timer hit, not just a body to res.
*(Both S2 guides add that the 15s deduction applies "until the final minute" of
the run — a floor we did not have for S1. Tier-3, unverified.)*

## Sources

- [Icy Veins — Midnight Mythic+ Season 2 Guide](https://www.icy-veins.com/wow/midnight-mythic-season-2-guide) (tier 3, published 2026-08-05 — S2 ladder carry-over; explicitly still awaiting the first weeks' rotation)
- [Conquest Capped — Midnight M+ Season 2](https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-2/) (tier 3, updated 2026-08-02 — S2 breakpoints, Guile final-minute floor. Its Lindormi's Glow mention is *superseded here by the Tier-1 12.0.5 notes*, which also correct its "tank-side" framing)
- [Icy Veins — Midnight Mythic+ Season 1 Guide](https://www.icy-veins.com/wow/midnight-mythic-season-1-guide) (tier 3, anchor — ladder breakpoints + Bargain roles)
- [Conquest Capped — Midnight M+ Season 1](https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/) (tier 3 — per-Bargain mechanics + buff %s, Fort/Tyr scaling)
- [SSEGold — Xal'atath's Bargain Affix Guide](https://www.ssegold.com/wow-midnight-season-1-xalatath-bargain-affix-guide) (tier 4 — corroboration on Bargain counter-play + Guile 15s)
- [Wowhead — Lindormi's Guidance affix news](https://www.wowhead.com/news/new-lindormis-guidance-mythic-affix-provides-basic-dungeon-route-in-midnight-379948) (tier 3/4 — Guidance details)
- [Raider.io — Mythic+ Affixes (Season 1)](https://raider.io/news/740-midnight-mythic-plus-affixes) (tier 2/3 — breakpoint corroboration)
- **Tier 1**: [`_meta/patch-notes/12.0.5.md`](../../_meta/patch-notes/12.0.5.md) (DUNGEONS AND RAIDS › MYTHIC+) — **Lindormi's Glow**, verbatim, including the tank opt-in and the enemy-forces completion rule. Original: [12.0.5 Content Update Notes](https://worldofwarcraft.blizzard.com/en-us/news/24271855/12-0-5-content-update-notes).
- **Tier 1 (negative evidence, scoped to the archive)**: [`_meta/patch-notes/12.1.md`](../../_meta/patch-notes/12.1.md) — the archived **content update notes** contain **no affix section at all** (zero case-insensitive occurrences of "affix", checked 2026-08-11). ⚠ This negative covers **that archive only**. It is not a claim that no Tier-1 12.1 source mentions affixes — see the next entry, which does.
- **Tier 1 (the one positive affix signal)**: [Midnight Season 2 overview](https://worldofwarcraft.com/en-us/news/24294369) — *"Season 2 brings about new Affixes, four new targets in Nightmare Mode, and some new hunts on the Coiled Isle in Prey."* Under the **Prey** heading, so most likely scoped to Prey's Nightmare affixes; ambiguous enough that it may also cover Mythic+. Listed as Tier 1 in [`_meta/changelog-12.1.md`](../../_meta/changelog-12.1.md).

## TODO

- [ ] **Confirm the Season 2 affix set in-game on/after 2026-08-18**, off the
      keystone tooltip / dungeon journal: whether the S1 ladder really carries
      over unchanged, whether any new affix was added, and whether any Bargain
      was re-tuned. This is the open question the two Tier-1 signals leave —
      the content-update-notes archive has no affix section, while the Season 2
      overview blog says "Season 2 brings about new Affixes" under Prey. Until
      then the S2 ladder here is Tier-3 pre-season reporting.
- [ ] Resolve the **Guidance cutoff conflict**: Icy Veins says +2–4, Conquest
      Capped says removed at +6 (active +2–5). Confirm in-game off the affix's
      own **−5% health / −5% damage** tooltip, *not* off whether enemies are
      still highlighted — Lindormi's Glow highlights above the cutoff by design.
      (Marker for this lives on the breakpoint caveat above, not here — one
      marker per claim.)
      *(The "does Lindormi's Glow exist" half of this item is resolved: it is
      Tier-1 from the 12.0.5 notes — see the section above. Removed 2026-08-11.)*
- [ ] Confirm exact **Bargain buff/debuff percentages and durations** against
      the in-game dungeon journal or wago.tools (currently single-sourced from
      Conquest Capped). Bump to `confidence: high` once verified.
- [ ] Confirm Fortified/Tyrannical exact scaling %s (trash +20% HP / boss +30%
      HP, +15% dmg) — values are standard but unverified vs a Midnight-specific
      tooltip.
- [ ] Confirm the **Guile "until the final minute"** floor.

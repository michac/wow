---
id: pvp-conquest
name: Weekly Conquest (rated PvP)
goal: [gearing, rating]
venue: pvp
group: group
cadence: weekly
time: standing
scope: character
status: invalidated   # PRE-SEASON: rated PvP + Conquest do not return until 2026-08-18 — flip back to `active` that reset
gate: { type: manual }
breakpoint: { type: vault, track: pvp, thresholds: [1, 4, 8] }
reward: { type: [power, currency], detail: "Conquest → Champion-track PvP gear + tier; fills the Vault's PvP column (from 2026-08-18)" }
time_blocks: 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281   # 12.1 Content Update Notes, PLAYER VERSUS PLAYER (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 pre-season information (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - knowledge/_meta/patch-notes/12.1.md
  - knowledge/factions/slayers-rise.md                         # game-wide PvP rules + the 12.0.7 +9 as HISTORICAL
  - https://www.icy-veins.com/wow/midnight-pvp-season-2-guide  # Tier 3 — S2 mount thresholds (2300 / 1000), corroborates the Tier-1 mount names
  - https://www.icy-veins.com/wow/midnight-pvp-gearing-guide   # Tier 3 — S1-era rating thresholds (1800 / 1950), not yet re-confirmed for S2
confidence: high
---
⛔ **Not rankable during the 2026-08-11 pre-season week — there is no rated PvP and no
Conquest to earn.** Midnight **Season 1 competitive PvP ended at 22:00 the night before
regional maintenance** the week of Aug 11, and cutoffs were calculated at maintenance.
**All rated PvP — 2v2/3v3 Arena, Solo Shuffle, BG Blitz — and Conquest earning return with
Season 2 the week of 2026-08-18.** This file is `status: invalidated` for exactly that
reason; **flip it back to `active` (and re-run `wowkb.gen_candidates`) on 2026-08-18**.

**What PvP gives you this week instead:** unrated only — Battlegrounds and outdoor-world
PvP, plus the new **Training Grounds: Arenas** (3v3 versus bots, via Group Finder → Player
vs. Player tab), which is the bot-practice sibling of the Training Grounds BGs already
folded into `pvp-honor`. None of it pays Conquest or rating, and with no rated wins the
**PvP column of the Great Vault cannot accrue Season 2 credit this week** even though the
other rows can.

**From 2026-08-18, unchanged in shape:** rated wins pay **Conquest**, which buys
Champion-track PvP gear and converts into tier pieces (rush the 4-set), and **fill the PvP
column of the single Great Vault** — a `breakpoint` here, not a separate row. `goal:rating`
too — score-chasing above the gear payoff, with the Season 2 ladder paying the **Venomous**
title line and two S2-exclusive mounts: the **Venomous Gladiator's Goredrake** (Gladiator —
**50 3v3 wins at Elite / 2300**) and the **Vicious Lightbloom Boar** (Vicious Saddle —
**wins above 1000 rating in any bracket**). Both go away when S2 ends. The other S1 rating
breakpoints this file used to quote (**elite set 1800, weapon illusion 1950**) are
**Season 1 numbers and not re-confirmed for Season 2** — re-check them once the vendors are
live, along with where the Conquest set lands on Season 2's Champion track (**292 at 1/6 →
308 at 6/6**, per the Mistcrest table in `endgame/dawncrests.md`). @verify-ingame

⚠ **Do not carry the +9 forward.** The **+9 PvP ilvl** the KB used to attach to this
activity was **Season 1 / 12.0.7 material**: a one-time bump to the *season baseline* of the
Galactic Gladiator / Aspirant / Warmonger and crafted PvP sets (the 12.0.7 rated-gearing
rework, which also removed the Galactic Voidsliver / Void Matrix upgrade currencies). It was
**not** an ilvl bonus that applies inside rated instances, and it is **superseded by the
Season 2 gear ladder** opening 2026-08-18 — nothing in the 12.1 notes re-confirms it for S2.
See `factions/slayers-rise.md` ("Historical — 12.0.7 PvP gearing changes") and
`_meta/moving-values.md`.

**Conquest cap, and the Spoils of War change.** Season 1's weekly Conquest cap was removed
by hotfix for the rest of that season; Season 2 starts capped again and uncaps later, which
is what the 12.1 buff keys off — **Spoils of War now grants +50% increased Conquest once
Conquest has been uncapped for the season (was 30%)**, explicitly aimed at players gearing
up late in a season. So it is a **late-season catch-up accelerator**, not something that
changes the first weeks of S2.

**Other 12.1 rules that change how rated feels** (all live now, but only biting once rated
opens): **Gladiator's Distinction** gives tank/DPS **+15% primary** (was 12%) and **+5%
Stamina** (was 10%), healers **+10% Stamina** (was 15%); **Battlegrounds give 20% less
healing**; missing a **Solo Shuffle / BG Blitz** queue applies a stacking, **account-wide**
1-minute re-queue debuff; players are no longer knocked back while Feared or Disoriented;
and a game-wide **PvP snare tier-down** (70%→50%, 50%→30%, and so on) hits every class's
auto-applied rotational slows. On top of those, 12.1's **global class retune** lands in
rated too — **max-level player health and creature damage +25%** (so every absolute
burst/healing/consumable number from before 2026-08-11 has moved), several DPS/Tank
healing-and-absorb spells retuned to match, major DPS cooldowns lowered with steady-state
damage raised on several specs, **diminishing-return categories now reset after 20s**
(was 16), and interrupts now show a **"missed" visual + sound** when the target was not
casting. No spec here is "unchanged by 12.1"; there are only specs with no PvP-specific
change. Per-class numbers: `_meta/patch-notes/12.1.md`, CLASSES section.

Vendors cluster in **southwest Silvermoon** (near Falconwing Square). `venue:pvp` default E
(0.4) keeps it deprioritized for this PvE-leaning roster; the per-char rating goal is what
surfaces it for a dedicated pusher. `gate: manual` — no clean conquest-cap signal in the
dump yet (surfaces + self-report).

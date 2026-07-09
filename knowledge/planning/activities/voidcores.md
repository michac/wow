---
id: voidcores
name: Buy + spend 2 Nebulous Voidcores
goal: [gearing]
venue: meta
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: manual }
reward: { type: [power], detail: "guaranteed bonus-roll piece on your best content — HOLD for a +10 M+ key (Myth 272); on delve/prey it's only Hero 259, random slot" }
yields:
  slots:
    # SCORED at the achievable Hero floor (delve/prey), guaranteed piece, RANDOM slot.
    # The Myth-272 upside from a +10 M+ roll is NOT scored as a vector: without
    # content-capability gating (Phase 4) it would rank voidcores #1 for a fresh alt
    # who can't run +10s — the over-recommendation the owner warned against. The
    # "hold for +10" guidance lives in reward.detail + prose until the gate lands.
    - { track: hero, ilvl: 259, chance: 1.0, slots: [all] }
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-09
reviewed: 2026-07-09
sources:
  - knowledge/planning/candidates.json
  - https://www.wowhead.com/guide/midnight/the-voidforge-patch-12-0-5-bonus-loot-rolls-upgrades
  - https://www.method.gg/guides/midnight-nebulous-voidcores-bonus-rolls
  - https://www.icy-veins.com/wow/turboboost-and-bonus-rolls-in-midnight-season-1-the-voidforge
confidence: high
---
Spend your 2 weekly **Nebulous Voidcores** on a bonus loot roll at the end of your
**highest-track content** — a *guaranteed* extra piece, but on a **random slot**.

**Where they come from (corrected):** voidcores are **bought from the vendor Decimus**
(Val/Naigtal base camps) for gold + Voidlight Marl + Veteran Dawncrests — **2 per week**,
and the weekly cap **ramps +2 each week** all season (catch-up-friendly); one extra core
per week for 6 Thalassian Tokens of Merit. Decimus *also* gives the "Knocking Off the Top"
world-boss quest, which is where the "voidcores drop from Decimus" confusion came from —
the cores are a **vendor purchase, not a drop**.

**The roll matches the track the Great Vault would give for that content** (Voidforge,
12.0.5): a core spent on a **+10 Mythic+ (or higher) key → Myth 1/6 (272)**; on a
**+6–9** key, a Bountiful delve, or a Nightmare Prey hunt → **Hero 1/6 (259)** (2 cores on
a raid boss). So the **highest-value spend is a +10 M+** — don't burn cores on delve/prey
random Hero when a +10 key turns the same core into Myth.

**RNG caveat (why it's not a targeted fix):** the roll is a *guaranteed* piece (`chance: 1.0`),
but the **slot is random** — so for closing a *specific* gap a targeted vendor buy (Field
Accolades → Maren, `val-naigtal`) out-ranks a voidcore; cores shine for broad upgrades once
you're running +10s. The two `yields.slots` vectors express the track-by-content split; the
scorer takes the better of the two, i.e. it values the roll at the **best track the char
could earn** — it does not yet gate the Myth vector on whether this char actually runs +10s
(a clean follow-up when content-capability gating lands).

`gate: manual` — no clean weekly signal yet (self-report until the addon can track the
purchase/roll).

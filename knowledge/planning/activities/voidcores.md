---
id: voidcores
name: Spend a Nebulous Voidcore bonus roll
goal: [gearing]
venue: meta
group: solo
cadence: weekly
time: standing
scope: character
# ⏸ NOT DOABLE between 2026-08-11 and the week of 2026-08-25: Season 1 cores were
# converted to gold at the S1 close, and the Season 2 Great Vault does not offer a
# Voidcore until the SECOND vault of S2. Flip back to `active` the week of 2026-08-25.
status: invalidated
gate: { type: manual }
reward: { type: [power], detail: "guaranteed bonus-roll piece at Great-Vault item level for that content — random slot. Raid re-roll costs 1 core (was 2); a Lair takes at most 1 core per week. Unavailable until the week of 2026-08-25 (needs ≥3 vault panes unlocked)" }
yields:
  slots:
    # SCORED at the Season 2 Hero floor we can cite from Tier-1 data (Heroic Lair
    # drops Hero 1/6 = 305); guaranteed piece, RANDOM slot.
    # Blizzard has NOT published the S2 per-content vault-track table, so the
    # "hold it for your highest-track content" upside is deliberately NOT scored
    # as a second vector — without content-capability gating (Phase 4) it would
    # rank voidcores #1 for a fresh alt who cannot run that content, the
    # over-recommendation the owner warned against. Guidance lives in prose.
    - { track: hero, ilvl: 305, chance: 1.0, slots: [all] }
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/candidates.json
  - https://worldofwarcraft.com/en-us/news/24293281
  - https://us.forums.blizzard.com/en/wow/posts/29833350
  - https://www.wowhead.com/guide/midnight/the-voidforge-patch-12-0-5-bonus-loot-rolls-upgrades
confidence: medium
---
⛔ **Not doable right now (checked 2026-08-11).** 12.1 rebuilt this activity end to
end: **Season 1 Nebulous Voidcores were converted to gold** at the close of Season 1
and can no longer be spent on Season 1 content, and the Season 2 replacement —
Voidcores as a **Great Vault reward** — is **not in the first Season 2 vault**. Bonus
rolls return the **week of 2026-08-25** (the second week of Season 2) and can only be
picked by a character with **at least 3 vault panes unlocked**. Until then there is
nothing to buy and nothing to spend; `status: invalidated` reflects that, not a dead
feature.

**Where they come from now (Season 2).** A Voidcore is a **Great Vault selection** —
from the start of Season 2 it sits alongside the gear options, so taking one costs you
that week's vault pick. On top of that, **Orin Straylight** — who **relocated to near
the Catalyst in Silvermoon** — provides **one additional Voidcore per week starting
week 8 of Season 2** (≈ the week of 2026-10-06, if S2 week 1 is the week of Aug 18).
*(Historical, Season 1 / the Voidforge: cores were **bought from the vendor Decimus**
in the Val/Naigtal base camps for gold + Voidlight Marl + Veteran Dawncrests, 2 per
week with the cap ramping +2 each week, plus one extra for 6 Thalassian Tokens of
Merit. Blizzard's notes do not say whether that vendor path survives into Season 2 —
treat the vault as the only confirmed S2 source until someone checks Decimus in game.)*

**What a roll gives.** Unchanged in principle: an item acquired with a Voidcore is
**equivalent to a Great Vault reward in item level** for the content you spend it on —
a *guaranteed* extra piece on a **random slot**. So the value of a core still tracks
the best content you actually clear; Blizzard has **not** republished the per-content
track table for Season 2, so don't quote Season 1's "+10 key → Myth 1/6 (272)" numbers
— those bands are dead (S2 gear runs **269 → 334**; see `endgame/dawncrests.md`).
The scored floor here is the Season 2 **Hero 1/6 = 305** we can cite from the Lairs
reward table.

**Costs and limits (12.1).**
- **Raid re-roll: 1 Voidcore** (was 2).
- **Lairs: at most one Voidcore per week per Lair** — Lair loot is bind-on-pickup on a
  weekly lockout, so the core is the only second bite.
- The **Ritual Sites Tier 6 "Advanced Ritual Studies" quests no longer award a Voidcore
  bonus roll**; they remain completable for the achievement. That removes what used to
  be a reliable off-content source.

**RNG caveat (why it's not a targeted fix).** The roll is a *guaranteed* piece
(`chance: 1.0`), but the **slot is random** — so for closing a *specific* gap a targeted
vendor buy (Field Accolades → the Void-Touched Caches, `val-naigtal`) out-ranks a
Voidcore; cores shine for broad upgrades once you're clearing high-track content. And in
Season 2 the core has a real price even when it's "free": taking it from the vault means
**not** taking that week's gear pane.

`gate: manual` — no clean weekly signal yet (self-report until the addon can track the
vault pick / the roll).

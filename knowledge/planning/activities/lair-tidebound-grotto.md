---
id: lair-tidebound-grotto
name: Tidebound Grotto lair (Nymrissa Wavecaller) — weekly kill
goal: [gearing]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: lockout, name_contains: Tidebound }
reward: { type: [power], detail: "one weekly BoP loot chance off Nymrissa Wavecaller + Mistcrests; World 279 (Veteran 1/6) now, Normal 292 / Heroic 305 / Mythic 318 from 2026-08-18" }
yields:
  slots:
    - { track: veteran, ilvl: 279, chance: 1.0, slots: [all] }   # World difficulty LANDING ilvl (Veteran 1/6 = 279). chance carried for Phase-3 EV, unused in 2a — Blizzard has not published a per-kill drop rate
time_blocks: 1
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24295085   # Lairs preview — difficulties, solo queue, reward table (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 information — pre-season split, BoP, weekly lockout, Voidcore (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281            # Curse of Ula'tek Content Update Notes (tier 1)
  - knowledge/endgame/lairs.md
confidence: high
---
**New in 12.1.** A **Lair** is an instanced world boss — Blizzard's "evolution on world
bosses" — found at a fixed spot in the world with a **summoning stone outside**, like a
Delve, but running a scaling boss encounter on a raid-style reward track. **Tidebound
Grotto** is the first (and so far only) one: **The Coiled Isle**, level 90, one boss —
**Nymrissa Wavecaller**, a naga sorceress. The **entrance is underwater**; swim down into
the waters below the isle (an aquatic mount helps). Full reference:
`knowledge/endgame/lairs.md`.

**This row is rankable TODAY, but only at World difficulty.** 12.1 went live 2026-08-11 in
a **pre-season** state; Season 2 opens **2026-08-18**. Right now the lair offers **World
only** — recommended ilvl **273**, drops **279 (Veteran 1/6)** plus **Veteran Mistcrests**.
**Normal (286 → 292, Champion 1/6), Heroic (299 → 305, Hero 1/6) and Mythic (312 → 318,
Myth 1/6, flexible 15–25)** all unlock with the **week of Aug 18** maintenance. `yields.slots`
therefore carries the **World** landing ilvl only — bump it when the harder difficulties open,
or the ranker will keep valuing a 279 drop for a character who can clear Heroic.

**Why it's `group: flex` at `venue: world` and not `venue: raid`.** World difficulty is
**solo-queueable**: you pick the difficulty and go straight in **alone**, and the instance
**fills with other challengers while you play**. What you play is a **two-part scenario** —
clear elite monsters until the boss appears, then fight the boss — and **the boss scales
5–40 players**, so a solo queuer and a 40-strong pile-in get the same epic loot. That is a
solo-world experience with company, not a group-gated raid, so it should not eat the raid
E-penalty (0.7); it inherits the `world` E of 1.1. Pre-made groups work the other way: the
leader picks the difficulty and enters first, the rest follow in. From Aug 18, Normal+ is a
genuine premade activity — revisit this tag if the harder difficulties become the point.

**Weekly lockout, bind-on-pickup, one Voidcore per lair per week.** Lair gear is **BoP**
like raid gear — *not* warbound-until-equipped the way outdoor rare drops are, so you can't
funnel it to an alt (that's the structural difference from the old world-boss cache this
activity supersedes; see `world-boss.md`). A **Nebulous Voidcore** may be spent **once per
week per lair** — but ⚠ Voidcore bonus rolls are **not available yet**: they return the
**week of Aug 25** and need ≥3 vault panes unlocked (`voidcores.md`).

**No `yields.currencies` yet (needs-first Phase 1).** The kill pays **Veteran Mistcrests**
(the S2 crest line — `endgame/dawncrests.md`), but Blizzard has published **no per-kill
amount**, and `_facets.md` says source amounts, don't fabricate. Value therefore comes from
`yields.slots` alone, which under-counts the row slightly for a crest-hungry character.
Add `veteran_crest: <n>` once the number is observed. @verify-ingame

**Gate resolution.** Uses the plain `lockout` gate (matches any dump lockout whose name
contains "Tidebound"), **not** `raid_weekly` — a lair is instanced and weekly-locked, but
nothing Tier-1 says `GetSavedInstanceInfo` returns it with `isRaid` set, and `raid_weekly`
requires that flag plus `defeated >= 1`. If the lockout doesn't appear in the dump at all
the gate reads `todo` every reset (it never false-"done"s), which is the safe failure.
Confirm the live lockout string after a clear. @verify-ingame

**Great Vault credit is unconfirmed.** No Tier-1 source states which row (if any) a lair
clear fills; a Tier-4 guide claims the Raid row. No `breakpoint:` block is declared here on
purpose — don't plan a vault slot around it until it's seen in the dump. @verify-ingame

`time_blocks: 1` is an estimate: swim to the entrance, queue, clear the elite phase, kill the
boss. It does not model waiting for the instance to fill, which the design says happens while
you're already fighting. Re-time after a real clear. @verify-ingame

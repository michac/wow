---
title: The Dreamrift (Raid — Midnight Season 1, previous tier as of 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.api.blizzard.com/data/wow/journal-instance/1314?namespace=static-12.1.0 (tier 1, authenticated Game Data API)
  - https://us.api.blizzard.com/data/wow/journal-encounter/2795?namespace=static-12.1.0 (tier 1, authenticated Game Data API)
  - https://us.api.blizzard.com/data/wow/item/249347?namespace=static-12.1.0 (tier 1 — Riftbloom = class-set chest token; 249348/249349/249350 likewise)
  - https://worldofwarcraft.com/en-us/news/24293281 (tier 1, 12.1 "Curse of Ula'tek" content update notes)
  - https://us.forums.blizzard.com/en/wow/posts/29833350 (tier 1, Season 1 ending / Season 2 information)
  - https://www.warcraftlogs.com/zone/rankings/46 (tier 2)
confidence: medium
---

# The Dreamrift

Single-boss Midnight raid (Onyxia-style). Journal instance **1314**, map 2939,
location **Harandar**, minimum level **90**.

> ⚠ **Status in 12.1:** the Dreamrift is **previous tier**. Season 1 ended with
> the week of **2026-08-11** maintenance; the current-tier raid is **The Venomous
> Abyss**, which opens the week of **2026-08-18** (`venomous-abyss.md`). The
> Dreamrift is still enterable and its drops are **Season 1 items**.
>
> ⚠ **Whether Season 1 raid gear can still be upgraded at all is not
> established.** Dawncrests were Season 1 only and "have no S2 use"
> (`dawncrests.md`), and 12.1 explicitly froze *world-boss* S1 loot as **no
> longer upgradeable** (`_meta/moving-values.md`) — but the notes say nothing
> either way about S1 **raid** drops. Treat the Season 1 caps as the ceiling and
> don't plan crest spend here until this is checked in game.

**12.1 named no change specific to this instance** (grep of `patch-notes/12.1.md`)
— which is *not* the same as "unchanged". Two 12.1 changes reach the Dreamrift
anyway:

- **The four global class changes**, which apply to every spec in every instance:
  player health **and** creature damage **+25% at max level** (health consumables
  rescaled, and several DPS/Tank healing + absorb spells retuned to keep their
  relative impact); **major DPS cooldowns lowered with steady-state damage raised**
  on several specs; **interrupts now show a "missed" visual + sound** when the
  target was not casting; **diminishing-return categories reset after 20s**
  (was 16s). The first of those retunes this encounter along with everything else.
- **Season 1 Nebulous Voidcores can no longer be used in Season 1 content** (they
  convert to gold at the end of S1), so **the Dreamrift no longer has a bonus
  roll**.

Lore (journal): the Dreamrift lies deep within the **Rift of Aln**, where the
dreams of Aln'hara took form. In her absence the manifestations inside it grew
dark and began devouring one another; Chimaerus is what won that cycle.

## Boss

| Boss | Journal enc. | WCL enc. |
|------|--------------|----------|
| Chimaerus the Undreamt God | 2795 | 3306 |

## Difficulties

| Difficulty | Players |
|---|---|
| Raid Finder | 30 (flex) |
| Normal | 30 (flex) |
| Heroic | 30 (flex) |
| Mythic | 20 (fixed) |

Single boss, so **no LFR wings** — the whole raid is one queue. Standard retail
raid lockouts apply: LFR / Normal / Heroic are loot-based weekly locks, Mythic is
an instance lock, and all four reset at weekly reset.

## Strategy summary (from the in-game Adventure Guide)

⚠ The Adventure Guide lists **abilities, not a timeline**. Section *order* below
follows the journal's own nesting, which is where an ability is scoped — not when
it happens.

**Dissonance** (spell 1267201) has its own top-level journal section sitting
**above Stage One**, i.e. it is scoped to the encounter rather than to either
stage. The journal API exposes **no body text** for it and the spell carries no
player-facing tooltip, so its effect is unstated here — resolve it in game.

**Stage One — Insatiable Hunger.** Chimaerus periodically casts **Alndust
Upheaval**, pulling players into the Rift (**Alnsight**) where they can see and
attack the **Manifestations** — which are shielded by **Alnshroud**. Strip a
Manifestation's shroud and it **emerges into Reality** and walks toward the
**Insatiable** Chimaerus; letting it arrive feeds the boss (**Cannibalized
Essence** / **Consume**). Coalesced Manifestations apply raid-wide **Rift
Sickness**. Three Manifestation types: **Colossal Horror** (Colossal Strikes on
its current target — tank pickup; Discordant Roar), **Haunting Essence**
(Fearsome Cry, Essence Bolt) and **Swarming Shade**. Boss abilities in this
stage: **Rift Madness**, **Consuming Miasma** (leaves **Lingering Miasma**),
**Caustic Phlegm**, **Rending Tear**.

**Stage Two — To The Skies.** At **100 energy** Chimaerus takes flight and
channels **Corrupted Devastation** while summoning Manifestations below, then
**Ravenous Dives** to consume them. Caustic Phlegm and Consuming Miasma continue,
and **Rift Shroud** is also filed under this stage. *(It is the last section
listed, but the journal never says it ends the stage — the previous "Rift Shroud
closes the stage" was an inference from section order and is withdrawn.
**Rift Madness** being Stage One only does hold: the API files it under that
stage.)*

Healer note: players inside the Rift under **Alnsight cannot interact with
allies** — plan cooldowns and dispels around the Upheaval windows.

## Loot (journal-encounter 2795 — 18 entries)

**Very rare / trinket / weapon:**

| Item | ID |
|---|---|
| [Gaze of the Alnseer](https://www.wowhead.com/item=249343) (trinket — ⚠ **Season 1** rankings, now historical: rated BiS-adjacent for several Warlock/DH specs per the Tier-3 Method/maxroll rankings captured in those specs' `gearing.md`. No S2 ranking exists yet) | 249343 |
| [Undreamt God's Oozing Vestige](https://www.wowhead.com/item=249805) | 249805 |
| [Alnscorned Spire](https://www.wowhead.com/item=249278) | 249278 |
| [Tome of Alnscorned Regret](https://www.wowhead.com/item=249922) | 249922 |

**Armor:** Dream-Scorched Striders (249373) · Scorn-Scarred Shul'ka's Belt
(249374) · Scornbane Waistguard (249371) · Greaves of the Unformed (249381).

**Riftbloom set — these ARE class-set tokens, for the CHEST slot.** Verified live
against the item API on 2026-08-11: each is an Epic, non-equippable
Miscellaneous/Junk item requiring level 90, whose use effect reads *"Synthesize a
soulbound set chest item appropriate for your class."*

| Token | ID | Classes |
|---|---|---|
| Alnwoven Riftbloom (cloth) | 249347 | Warlock, Mage, Priest |
| Alncured Riftbloom (leather) | 249348 | Druid, Demon Hunter, Monk, Rogue |
| Alncast Riftbloom (mail) | 249349 | Hunter, Shaman, Evoker |
| Alnforged Riftbloom (plate) | 249350 | Death Knight, Paladin, Warrior |

**Profession / cosmetic / collectible:** Formula: Enchant Weapon — Worldsoul
Cradle (256750) · Pattern: World Tender's Barkclasp (256656) · Eerie Iridescent
Riftshroom (264246, housing decor) · Dreamrift Vanquisher's Argent / Gleaming /
Aureate Trophy (267645 / 266886 / 265950).

⚠ *An earlier revision of this file said "no class tier set drops here — Season 1
tier came from March on Quel'Danas." **Both halves were wrong.** The first
contradicted this file's own loot list (see the tokens above); the second was
uncited — nothing in the 12.1 ledger, `patch-notes/12.1.md` or any other KB file
supports it. `march-on-quel-danas.md` only says the class-set **vendor** Kirana
stood at that raid's entrance, which is a different claim.*

**Which Season 1 raid dropped the other set slots is still unestablished** in this
KB — `the-voidspire.md`'s tier-token TODO is open. All that is confirmed here is
the chest token.

The Season 2 sets come from the Venomous Abyss and from the vendor **Kirana**, who
moved in 12.1 from the March on Quel'Danas entrance to beside the Catalyst in
Silvermoon, where she now also stocks S2 class-set armor for **Slumbering Coil
Curios** (`catalyst.md`).

## TODO

- [ ] Per-difficulty ilvl bands for Dreamrift drops (LFR / N / H / M) — not
      exposed by the journal API; needs a live drop check or a Tier-3
      corroboration. Historical now that Season 1 is over.
- [ ] **Can Season 1 raid drops still be upgraded in Season 2?** Dawncrests are
      dead currency and world-boss S1 loot is explicitly frozen, but no source
      states the rule for S1 *raid* gear either way. @verify-ingame: open a
      Dreamrift drop at the upgrade NPC and see whether an upgrade option exists.
- [ ] Which Season 1 raid dropped the **non-chest** class-set tokens. Only the
      chest token (Riftbloom) is confirmed, and it is here.
- [ ] What **Dissonance** (1267201) actually does — no journal body text, no
      player-facing spell tooltip. @verify-ingame.

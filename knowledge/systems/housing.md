---
title: Player Housing (Midnight)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" content update notes (Tier 1)
  - https://worldofwarcraft.blizzard.com/news/24295382/        # Blueprints preview (Tier 1)
  - https://worldofwarcraft.blizzard.com/news/24296054/        # New neighborhood Endeavors (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://www.icy-veins.com/wow/news/pets-blueprints-and-more-everything-new-for-player-housing-in-patch-12-1/
  - https://www.icy-veins.com/wow/weekly-to-do-list
confidence: high
---

# Player Housing (Midnight)

Housing weekly via Vaeli (Silvermoon bank); Decor Duels and Field Accolade decor feed this system.

## 12.1 "Curse of Ula'tek" changes (live 2026-08-11)

The 12.1 housing pass is the largest since housing shipped: layout export/import,
pets in the home, four new Endeavors, and two more house levels.

### Blueprints — export / import a layout

- **Scope:** a blueprint captures the **whole house (interior + exterior)**, the
  **interior only**, the **exterior only**, or a **single room**.
- **Storage:** **50 save slots** for your own layouts, plus **10 additional
  auto-save slots**. An **auto-save is created automatically when you import**, so
  an import is always revertible.
- **Sharing:** blueprint codes are shareable **cross-region** (China excluded).
  Codes can be **linked in chat and inspected there**, and can be **reported**.
- **Import preview:** before anything is applied you get a list of the **required
  rooms and decor**, the **budget needed**, what you already own and **what is
  missing**.
- **Dyes on import:** the import tries to do the right thing — it prefers
  correctly-dyed items and may dye items for you, but it **never replaces an item
  you have already dyed**.
- **New permission "Export"**, defaulting to **no one**. A visitor who has been
  granted it can import a copy of your layout into their own save slots.
- **New Reset button** — resets the **whole house**, or just the **interior** or
  **exterior**, putting the decor back into storage.
- **Where:** blueprint controls sit at the top of the screen in the House Editor;
  saved blueprints are reachable from the House Chest and from a dedicated tab on
  the House Dashboard (`H`).

### Pet Beds

- A **Pet Bed** decor item lets you station a **non-combat companion pet** in the
  home. Beds can be placed **inside and outside**.
- Caps: **up to 100 beds indoors, up to 25 outdoors.**
  *(Blizzard's notes say 25 outdoors; at least one third-party write-up says 50 —
  the Tier-1 number stands until confirmed in game. `@verify-ingame`)*
- **Indoor** pets can be set **Stationary or Roaming** (roaming uses new pet
  navigation that paths around your decor); **outdoor** pets are **Stationary
  only** for now.
- **A small number of pets cannot be placed** for various reasons.

### Four new neighborhood Endeavors

Neighborhoods now also **show visible results of completed Endeavors**, old ones
as well as new.

| Endeavor | Culture | Vendor | Flavour |
|---|---|---|---|
| **Knock-off Amani** | Amani trolls | Griftah | Griftah's travelling troupe sells "traditional Amani goods" that are obviously not original; residents buy anyway |
| **Candle Culture** | Kobolds (Ringing Deeps) | Timicky | Strange wax deposits appear in the neighborhood; the kobolds are consulted on illumination |
| **Every Bakar Has Its Day** | Ohn'ahran centaur | Roshai Lightstep | Residents want help training their pets; the centaurs share their bakar-bonding know-how |
| **Vacation Season** | Tortollans | Taifa | The tortollans have been vacationing here longer than you have lived here, and share their recreational wisdom |

Each unlocks housing decor across a series of milestones. *(Vendor names and the
milestone/decor detail come from the Tier-1 Endeavors preview article; treat the
per-endeavor reward lists as not-yet-verified in game.)*

### Houses, rooms, dyes, UI

- **Houses can now reach level 12** (was 10), unlocking increased limits, **large
  exteriors**, and more.
- **New Artisanal Rooms** from the **General Contractor** NPC in each
  neighborhood — **four new rooms each** for the **orc, human, night elf and blood
  elf** styles, bought with **Community Coupons**. **Cross-faction room styles must
  be bought from the neighborhood smugglers.** Additional new housing items are
  also available in neighborhoods for Community Coupons.
- **Dye crafting streamlined**, freeing up considerable bag space. **New dye
  colors**, including ones that **replicate the darker appearances from before the
  12.0.5 update**.
- **Two new decor categories:** *Vines and Hanging Plants*, and *Pet Beds*.
- Removed the extra pop-up when deleting a room that has no decor in it.

### Related, filed elsewhere

- **Prey vendors: Anguish costs for housing items substantially reduced**, for
  both Season 1 and Season 2 items — see `endgame/prey.md`.
- Coiled Isle vendors, Zul'jarra's Forces renown, Season 2 dungeons/raid and
  professions all add new decor sources — see `systems/coiled-isle.md` and
  `factions/zuljarras-forces.md`.

## 12.0.7 "Revelations" changes (live 2026-06-16)

- **Outdoor lighting:** lights can now be placed outdoors on your plot (previously
  indoor-only). Outdoor lights have an overlap restriction — two lights cannot
  overlap, and the placement preview shows a **red** radius indicator when they
  are positioned too close together (they become unplaceable in that state).
- **Exterior decor caps raised:**
  - Level 5–6 houses: exterior decor limit **300**.
  - Level 7+ houses: exterior decor limit **350**.
- **New decor:** **over 100 new common decor** items added to existing
  Neighborhood vendors.

## TODO

- [ ] Populate baseline system mechanics (plot acquisition, house levels 1–12,
      interior vs exterior decor caps below Lv5, neighborhood/vendor flow) from
      the Icy Veins / Wowhead system guides. The 12.0.7 and 12.1 deltas above are
      verified Tier-1; the baseline table is still missing.
- [ ] Confirm the **level 10–12 placement budgets**. A pre-release preview quoted
      room/interior budgets of **124 / 5,545 at level 11** and **134 / 5,975 at
      level 12**; these are **not** in the official notes and were never
      corroborated against live data. Do not cite them until measured in game.
      `@verify-ingame`

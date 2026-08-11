---
id: void-assault
name: Void Assault weekly
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: void_assault }
reward: { type: [power, currency, collectible], detail: "Adventurer Mistcrests (Strikes, Incursions and the weekly) + Field Accolades toward Void-Touched Caches + cosmetics; 12.0.7 doubled its XP (leveler-only) and drop rates" }
time_blocks: 1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - knowledge/planning/candidates.json
  - knowledge/systems/void-incursions.md
  - knowledge/endgame/dawncrests.md
  - knowledge/_meta/moving-values.md
confidence: high
---
The Void Assault weekly event — crests, accolades, and cosmetic drops. Gate resolves from
the dump's weekly-quest state. Unaffected by the pre-season split: the loop runs normally
during the week of 2026-08-11.

**12.1 re-pointed the whole event at Season 2 (live 2026-08-11).** Void Strikes, Void
Incursions and the **Weekly Quest** all now award **Adventurer Mistcrests** — the Season 2
Adventurer crest (currency 3437, `CurrencyTypes` DB2 @ 12.1.0.69214), which upgrades
Adventurer-track gear across **ilvl 269–282**. That makes this an **entry-tier crest
engine**, not a Hero/Myth one: for a geared main it is accolade + cosmetic value, and the
crests matter mainly on an undergeared alt.

**Void-Touched Caches were repriced and the Season 1 caches removed** — the old Champion
**75** (random) / **100** (slot-specific) and Hero(ic) **500** (random) / **750**
(slot-specific) menu is gone. The 12.1 shelf is:

| Cache | Field Accolades | Slot | Binding | Drops at |
|---|---|---|---|---|
| Season 2 **Adventurer** | **200** | slot-specific | **Warbound until equipped** | **266** (Adventurer 1/6) |
| Season 2 **Veteran** | **500** | random | **Bind-on-Pickup** | **279** (Veteran 1/6) |
| Season 2 **Veteran** | **750** | slot-specific | **Bind-on-Pickup** | **279** (Veteran 1/6) |

Planning consequence: the alt-gearing move that made this activity attractive in S1 — bank
Accolades on the main, buy a **Warbound** cache, mail it down — now only works at the
**200 Adventurer** tier. Both Veteran caches are **BoP**, so Accolades spent on Veteran
gear are locked to the character that spends them. Score the Veteran spend as
character-local power and the Adventurer cache as warband-portable filler.

**XP is leveler-only (Phase 0, needs-first redesign).** 12.0.7 doubled both XP *and* drop
rates. The **doubled XP is worthless at level cap** — it's only value on a sub-cap roster
member (strong alt-leveling fodder). At cap the draw is the **Adventurer Mistcrests +
accolade caches + cosmetics**, nothing else; don't credit the XP toward the geared main's
value. When XP-bearing needs land (Phase 4 roster/leveler synergy) the XP weight applies
*only* to roster members below cap; here `goal:gearing` scores the at-cap crest/cache
value and the runtime slot-target R deflates it once every slot is above the cache tiers.

⚠ **This event does not pay Nebulous Voidcores** (an earlier revision of this row claimed
"voidcore drops" — `systems/void-incursions.md`'s reward list never had them). From
Season 2, Voidcores are a **Great Vault** reward; see `voidcores.md`.

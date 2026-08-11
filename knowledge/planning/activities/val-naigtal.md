---
id: val-naigtal
name: Val / Naigtal zone content (WQs, rares, events)
goal: [gearing, collectibles]
venue: world
group: flex
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
breakpoint: { type: vault, track: world, thresholds: [1, 4, 8] }
reward: { type: [power, currency, collectible], detail: "12.1: Season 2 Adventurer Mistcrests from WQs/rares/elites (both World Tiers) + Warbound-until-Equipped S2 Adventurer drops (1/6 Normal WT, 4/6 Heroic WT) + Field Accolades toward the re-cut Void-Touched Caches (200 S2 Adventurer Warbound / 500 · 750 S2 Veteran BoP) + Relic Coffer Key shards; fills the World Vault row" }
yields:
  currencies: { field_accolade: 150 }   # zone farm ≈150 Accolades. ⚠ The zone's CREST payout is now **S2 Adventurer Mistcrests**, and `rewards.py` has no canonical `adventurer_crest` key — an unknown key contributes nothing, so it is deliberately not declared here rather than mislabelled as `hero_crest` (which the zone no longer pays at all). Wiring note in the body.
  slots:
    - { track: veteran, ilvl: 279, targeted: true, slots: [all] }    # 750 Field Accolades → slot-SPECIFIC S2 Veteran Void-Touched Cache (Bind-on-Pickup): YOU pick the weak slot. Landing = Veteran 1/6 = 279 (track step inferred from the S2 ladder; Tier 1 states the tier, not the ilvl)
    - { track: adventurer, ilvl: 276, chance: 0.5, slots: [all] }    # rare / WQ / elite Warbound-until-Equipped drop on HEROIC World Tier = S2 Adventurer 4/6 = 276; on Normal WT it lands 1/6 = 266. Random slot.
time_blocks: 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes — VAL AND NAIGTAL / VOID-TOUCHED CACHES (Tier 1)
  - https://wago.tools/db2/CurrencyTypes?build=12.1.0.69214   # Mistcrest currency IDs 3437-3441 + upgrade bands (Tier 1 game data)
  - https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1   # the now-FROZEN Season 1 world-boss drop table (historical)
  - https://www.wowhead.com/news/target-specific-gear-slots-with-hero-track-gear-in-patch-12-0-7-381690   # the 12.0.7 Maren Hero-box stock, REMOVED in 12.1 (historical)
  - https://www.icy-veins.com/wow/news/two-new-world-bosses-and-locations-12-0-7s-val-and-naigtal-rewards-quests-and-more/
  - knowledge/endgame/world-events.md
  - knowledge/endgame/delves/overview.md
  - knowledge/_meta/moving-values.md
confidence: high
---
The ongoing content of the two worlds (**Val**, **Naigtal**) reached via the Voidstorm
portal — only one is up per week (portal rotates every few days). **World quests, rares, and
events** give **direct gear** plus two instrumental currencies: **Field Accolades** and
**Relic Coffer Key shards**. 12.1 kept the loop intact but **re-pointed it at Season 2 at the
bottom of the ladder**: it is now the **entry-tier open-world catch-up farm**, not the
Hero-track engine it was in 12.0.7.

## ⚠ 12.1 retier (live 2026-08-11) — everything here moved down a tier

| Source | 12.1 reward |
|---|---|
| World quests, rares, elites (**crests**) | **Season 2 Adventurer Mistcrests** — in **both** Normal *and* Heroic World Tier |
| Rare equipment drops | still **Warbound Until Equipped**, now **S2 Adventurer 1/6** (Normal WT) / **4/6** (Heroic WT) |
| World Boss + weekly quests (**crests**) | **S2 Adventurer** (Normal WT) / **S2 Veteran** (Heroic WT) |
| World Boss **gear** | ⚠ **frozen Season 1 items, no longer upgradeable** |
| "Knocking off the Top (Heroic)" Mythic reward | ⚠ **frozen Season 1 reward, no longer upgradeable** |

**The scoring consequence is the asymmetry: the crests are current, the world-boss gear is
dead.** Farm this zone for **crests and Warbound Adventurer catch-up pieces**; do *not* let
the ranker value it off the world boss. That row is scored separately and already demoted
(`world-boss.md`, `reward_base: 1`) — a frozen S1 Hero 1/6 (259) that can never take a crest
loses to a free Adventurer 4/6 (276) off a rare in this very zone.

**Landing ilvls** (S2 Adventurer track: 266 · 269 · 272 · 276 · 279 · 282 — see
`endgame/delves/overview.md`; the ladder corroborates exactly against the Tier-1
`CurrencyTypes` bands, but the per-step assignments are Tier-3 and not in-game verified):
- Normal World Tier rare drop → **266**
- Heroic World Tier rare drop → **276** (the number the `yields.slots` vector carries)

## Field Accolades — the vendor was re-cut, the Hero box is gone

⚠ **The 12.0.7 "Accolades → slot-targeted Hero-track gear (~ilvl 259) at Maren Silverwing"
line is dead.** Tier 1: *"The Season 1 gear caches have been removed."* Maren's 12.1 shelf:

| Void-Touched Cache | Field Accolades | Binding |
|---|---|---|
| Season 2 **Adventurer** | **200** | **Warbound** |
| Season 2 **Veteran**, random slot | **500** | Bind-on-Pickup |
| Season 2 **Veteran**, slot-specific | **750** | Bind-on-Pickup |

Deterministic slot-targeting **survived** — it just costs **750** and pays a **Veteran**
piece (~279) instead of a Hero one. That is still the best thing Accolades buy for the
character spending them, and it is the vector `yields.slots` values. The **200 Warbound**
cache is the only warband-portable option left (bank Accolades on the main, mail the cache
to an alt); both Veteran caches are **BoP**, so score them as character-local power.
Accolades also still buy cosmetics / mounts at the Val/Naigtal vendors (the `collectibles`
tag). Full vendor detail: `endgame/world-events.md`.

**Relic Coffer Key shards** still assemble into keys that open **coffers** for more gear.
⚠ 12.1 **retuned shard amounts from multiple sources**, weighted toward Coiled Isle content,
and Blizzard calls the tuning *"ongoing and a work in progress"* — treat any specific shard
number as volatile and don't hard-code one into a yield.

**Rare farming** is unchanged in shape: rares **spawn frequently**, **Warp Riders** and
**Blasktar Legion** enemies remain the dense crest source on Heroic World Tier (now paying
S2 Adventurer like everything else), and **Dark Particles** drop here and **stack to 1000**.

## Ranker wiring — two open items (tooling, not this file)

1. **No `adventurer_crest` canonical key.** `_facets.md`'s key list and
   `tools/wowkb/rewards.py` (`CURRENCY_CONSUMERS` / `CANONICAL_CURRENCY_NAME`) stop at
   `veteran_crest`, and `CREST_CEILING` only knows Champion/Hero/Myth. Until an
   Adventurer key + ceiling exist, this zone's crest yield is **invisible to the currency
   consumer** — which is *approximately* right for a geared main and *wrong* for a fresh
   alt. Declaring the old `hero_crest: 20` would be worse: the zone pays no Hero crest at
   all now.
2. **`FIELD_ACCOLADE_ILVL = 259` is stale.** It encodes the removed S1 Maren Hero box, so
   `_consume_field_accolade` still values Accolades against a 259 sidegrade. The 12.1
   equivalent is the **750-Accolade Veteran slot-specific cache (~279)**; the constant and
   its price gate both need re-fitting. Parked in `_meta/kb-inbox.md`.

**Vault note:** like delves and prey, this content **fills the *World* row of the Great
Vault** — the **same column** `delve-bountiful` advances, not a second one. The `breakpoint`
here marks that it advances that column; the ranker-wiring phase must treat the World row as
one shared counter (don't double-count delve + world progress). ⚠ For the **first Season 2
vault** the World row is capped at **Champion 3/6**, **Hero 1/6** thereafter
(`endgame/great-vault.md`). **Overlap:** the weekly capstone quest lives in
`showdown-weekly`; the world-boss kill itself lives in `world-boss`; Field Accolades are also
earned from `ritual-sites` — this row is the *zone farm* that earns the currency and the
direct WQ/rare drops.

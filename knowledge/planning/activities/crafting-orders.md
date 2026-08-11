---
id: crafting-orders
name: Crafting / patron orders
goal: [professions, gearing]
venue: profession
group: solo
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [currency, power], detail: "Knowledge, optional reagents, augment runes, Artisan's Moxie; fills gear/consumable orders" }
time_blocks: 1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources: ["yt:cpbQXd04ehI", "https://www.icy-veins.com/wow/professions", "https://conquestcapped.com/guides/wow/wow-professions-overview/", "https://worldofwarcraft.com/en-us/news/24293281"]
confidence: medium
---
**Crafting Orders** (unlock at skill 15) and **patron orders** — in Midnight they pay more
than gold: **Knowledge, optional reagents, and augment runes**, making them a real
progression lever, not just an income stream. Filling orders for other players (or your own
warband) is the repeatable profession loop; **patron orders** also feed faction-event
currencies (e.g. Shards of Dundun for Abundant Harvests). The per-profession Midnight
currency is **Artisan's Moxie** (Alchemist's / Blacksmith's / Tailor's / …) — *not*
Dragonflight's Artisan's Mettle.

`goal:[professions, gearing]` — professional power plus the crafted gear that comes out.
`cadence: repeatable` (no reset). Sits alongside `liadrin-spark` (the weekly spark craft) —
that entry owns the Spark; this one owns the order economy. `gate: always` keeps it as
fill-time.

**12.1 (2026-08-11):** the order loop itself is unchanged. What changed around it is demand:
**Crafting Sparks begin dropping during the pre-season week** (the week of Aug 11), so
Season-2 spark-gated orders start flowing before Season 2 opens on **2026-08-18** — expect
the usual season-open order rush. New Coiled Isle recipes unlock through **Zul'jarra's
Forces** renown and cost profession-specific Artisan Moxies; see
`../../systems/professions.md` and `zuljarra-renown` for the detail. Still `gate: always`.

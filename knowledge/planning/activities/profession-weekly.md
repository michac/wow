---
id: profession-weekly
name: Weekly profession knowledge
goal: [professions]
venue: profession
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: profession_knowledge }
reward: { type: [currency], detail: "Knowledge Points (+ Artisan Moxies); permanent profession power" }
time_blocks: 0.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - "yt:cpbQXd04ehI"
  - https://www.icy-veins.com/wow/professions
  - https://dving.net/guides/midnight-profession-changes-guide
  - https://www.icy-veins.com/wow/zuljarras-forces-renown-guide
  - https://www.method.gg/guides/all-profession-changes-and-new-recipes-in-wow-midnight-patch-12-1
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963   # Tier 1 — R5 "Coiled Isle Crafting" (9 named recipes), R6 "Demystifyin' Professions", Jan'sari at Tokka's Landing
  - https://us.forums.blizzard.com/en/wow/posts/29833350
  - https://www.wowhead.com/currency=3261/artisan-scribes-moxie  # game data — Artisan Moxie is the live per-profession family (not DF's Acuity/Mettle)
  - https://www.wowhead.com/item=245757/thalassian-treatise-on-inscription  # game data — Midnight's treatise line exists and is Thalassian-named, not DF's
  - https://www.method.gg/guides/all-profession-knowledge-point-sources-in-midnight  # Tier 3 — treatise/gathering/treasure weekly cadence (unverified in game)
confidence: medium
---
The weekly **profession Knowledge source** quest from each profession trainer (one per known
profession) — the steady drip of **Knowledge Points** that permanently deepen your
specialization trees. `goal:professions` (means-to-an-end, E 0.9). The other repeatable KP
drips fold in here too — Midnight's treatise line is the **Thalassian Treatise on
\<profession\>** (Inscription-crafted, warbound, so order one if you have no scribe), plus
first-of-week gathering and treasure knowledge items. ⚠ The treatises **exist** per game
data (Wowhead items 245757 Inscription / 245759 Enchanting / 245761 Herbalism / 245762
Mining, all Midnight-added) — this is *not* Dragonflight's treatise carried over by
assumption. Their **one-use-per-week, 1 KP** cadence and the gathering/treasure drop rates
are **Tier-3 only** (Method) and unverified in game. None of it is a 12.1 change.
The per-profession currency in Midnight is
**Artisan Moxie** (Artisan Tailor's / Alchemist's / Enchanter's Moxie, …) — *not*
Dragonflight's **Artisan's Acuity** or **Artisan's Mettle**, both of which are two
expansions dead and buy nothing here. Same currency family as `crafting-orders.md` and the
Hara'ti / Silvermoon Court vendors.

Weekly and **easily missed** because the trainer quests are out of the way — a City Guide
addon pins them. `scope:character` (each active char has its own professions). `gate` is
best-effort on the weekly-quest ID; the quest giver rotates per profession so read the log.

## 12.1 "Curse of Ula'tek" — the Coiled Isle adds a second KP faucet

The 12.1 **content update notes** (24293281) contain **no PROFESSIONS section at all** — but
the **Coiled Isle article (24293963) does**, inside the Zul'jarra's Forces renown track, and
that is Tier-1. So the floor here is wider than a first read suggests:

- **Tier-1**: **Jan'sari the Watchful** is the quartermaster at **Tokka's Landing**; the
  faction's currencies are **Voidlight Marl** and **Artisan Moxies**; renown **5** grants
  *"Coiled Isle Crafting"* (nine named recipes) and *"Gone Cursed Fishin'"*; renown **6**
  grants *"Demystifyin' Professions"* (knowledge tomes). Dye-crafting streamline is Tier-1
  from the content notes.
- **Tier-3/4 only** — and marked as such below: every **price**, the profession spread of
  the R5 recipes, the new-mat list, and the one-time knowledge respec.

- **Zul'jarra's Forces renown 5 — "Coiled Isle Crafting"** unlocks **nine purchasable
  recipes** at Jan'sari. The rank name and all nine recipe names are Tier-1 (24293963);
  the table with item ids is in `../../systems/professions.md` — that is the file of
  record, read it rather than a profession-name summary. ⚠ **Don't trust any
  "which six professions" list**, including the one in `../../factions/zuljarras-forces.md`
  — Blizzard names recipes, not professions, and the Tier-3 guides derive different
  spreads from the same nine items. R5 also carries a second unlock, **"Gone Cursed
  Fishin'"** (a Fishing lure recipe).
- **Zul'jarra's Forces renown 6 — "Demystifyin' Professions"** unlocks **profession
  knowledge tomes** from the same vendor. That unlock is Tier-1; **the price is not** —
  Tier-4 guides quote **750 Voidlight Marl + 75 or 150 of the matching Artisan Moxie**
  per tome, and the Tier-1 article gives no price at all. @verify-ingame: read the tome
  prices off Jan'sari at R6 (same open item as `../../systems/professions.md` and
  `../../factions/zuljarras-forces.md` — resolve all three together).
- **Ranking consequence, held loosely until that price is confirmed:** if the quoted cost
  is anywhere near right, a one-off tome purchase beats several weeks of trainer drip —
  the Silvermoon Court "Skill Issue" books are the proven precedent at **10 KP for 75
  Moxie** (`../../systems/tailoring-recipes.md`). So with `goal:professions` live, treat
  `zuljarra-renown.md` as a **plausible** rank-above-this, not a settled one; the
  ordering is only as firm as the unverified number under it.
- New Coiled Isle recipe material: **embellishments and stat-proc enchants across most
  professions**, plus new mats (**Neutralized Venom Clot**, **Cursebound Globe**) from
  specialized isle nodes. So the KP you bank now has a fresh sink.
- **One-time Midnight profession knowledge respec** is reported to be available in 12.1
  — but **recipes unlocked by previously-spent points are unlearned** on respec, so it is
  not free. Tier-3 only, not in the official notes. @verify-ingame
- **Dye crafting was streamlined** (considerably less bag space) and new dye colors added,
  including ones replicating the pre-12.0.5 darker appearances. Tier-1, but it is a
  housing/bag quality-of-life change — it does not move this activity's ranking.

**Pre-season note (week of Aug 11):** **Crafting Sparks begin dropping during the
pre-season week** (Tier-1), so the spark side of the crafting loop is live now — see
`liadrin-spark.md`. Nothing about the weekly trainer-quest cadence itself changed.

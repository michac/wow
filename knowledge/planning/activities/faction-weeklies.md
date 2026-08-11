---
id: faction-weeklies
name: Faction world events (renown + champion gear)
goal: [gearing, collectibles]
venue: world
group: flex
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: faction_events }
reward: { type: [power, currency, collectible], detail: "renown-gated Champion-track slot pieces (helm / neck / belt / trinket — upgraded to Season 2 item levels in 12.1) + pinnacle/apex caches + renown; housing decor" }
yields:
  slots:
    # The renown quartermaster pieces are VENDOR BUYS — you pick the slot, so `targeted: true`,
    # one vector per piece (they are four separate rewards, not a choose-one). Ranks per the
    # Season 2 gearing guide (Tier 3): helm Silvermoon Court R9 · neck Amani Tribe R9 ·
    # belt Hara'ti R8 · trinket The Singularity R7.
    # ilvl: 12.1 upgraded these to Season 2 item levels (Tier 3, Method). 292 = S2 Champion 1/6,
    # the Tier-1 floor value from _meta/moving-values.md; the vendor's exact STEP is not
    # published. @verify-ingame: read the tooltips at the four quartermasters and pin the real
    # ilvl — and whether the S2 stock flipped at 12.1 launch (Aug 11) or waits for Aug 18.
    - { track: champion, ilvl: 292, chance: 1.0, targeted: true, slots: [head] }     # Silvermoon Court R9
    - { track: champion, ilvl: 292, chance: 1.0, targeted: true, slots: [neck] }     # Amani Tribe R9
    - { track: champion, ilvl: 292, chance: 1.0, targeted: true, slots: [waist] }    # The Hara'ti R8
    # The trinket vector names BOTH canonical trinket slots (the dump keys are `trinket1`/
    # `trinket2` — a bare `trinket` matches nothing and is silently skipped); `targeted: true`
    # is correct: you buy one piece and slot it against whichever trinket is weaker.
    - { track: champion, ilvl: 292, chance: 1.0, targeted: true, slots: [trinket1, trinket2] }  # The Singularity R7
    # Zul'jarra's Forces' Champion wrist (R9) is DELIBERATELY not declared here — it belongs to
    # `zuljarra-renown`, which already carries both Cursebreaker's Bracers vectors.
time_blocks: 2
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24293281  # 12.1 "Curse of Ula'tek" Content Update Notes (Tier 1)
  - https://worldofwarcraft.blizzard.com/en-us/news/24293963  # Follow the Snakes to the Coiled Isle (Tier 1)
  - https://www.method.gg/guides/how-to-gear-fast-and-reach-item-level-335-in-wow-midnight-season-2  # renown Champion pieces upgraded to S2 ilvls + rank table (Tier 3)
  - https://www.icy-veins.com/wow/singularity-renown-guide
  - https://www.icy-veins.com/wow/harati-renown-guide
  - "yt:cpbQXd04ehI"
  - "yt:kUP8oqI7Ekc"
  - knowledge/endgame/world-events.md
  - knowledge/factions/zuljarras-forces.md
  - knowledge/_meta/changelog-12.1.md
confidence: medium
---
The rotating **per-faction weekly events** — **Saltheril's Soiree** (Silvermoon Court),
**Abundance** (Amani Tribe), **Legends of the Haranir** (The Hara'ti), **Stormarion Assault** (The
Singularity), each culminating in a pinnacle/apex cache. Renown is **instrumental** here
(`_facets.md`): the payoff is a **renown-gated Champion-track slot piece** from each
quartermaster — helm (Silvermoon Court, renown 9), neck (Amani Tribe, renown 9), belt/waist
(Hara'ti, renown 8), trinket (Singularity, renown 7, *Crucible of Erratic Energies*, gated
behind the Stormarion Assault quest) — hence `goal:gearing`, plus housing-decor and mount
collectibles.

**12.1 re-floored these pieces.** They landed at **ilvl 246** for all of Season 1, which had
zeroed them for any geared character. The Season 2 gearing guidance (Tier 3) says the Champion
neck / helm / belt / trinket **have been upgraded to Season 2 item levels**, so a piece you
never claimed is live gear again rather than vendor trash. The declared **292** is S2
**Champion 1/6** — a Tier-1 value from `_meta/moving-values.md` (the whole ladder shifted
+45: S2 gear spans 269 → 334) — but Blizzard has not published the vendor's exact step, and
whether the upgraded stock is on the vendors **today** or only from **Season 2 on 2026-08-18**
is unconfirmed. Read the tooltips before trusting the number. @verify-ingame

**12.1 adds a fifth renown faction: Zul'jarra's Forces** (the Coiled Isle; 20 ranks,
quartermaster **Jan'sari the Watchful** at **Tokka's Landing**, priced in **Voidlight Marl** —
`factions/zuljarras-forces.md`). ⚠ **It is not a fifth rotating event and this row does not
cover it.** There is no Zul'jarra analogue of Saltheril's Soiree; its renown comes from the
Coiled Isle's standing loop — **Curse Surges** at five rotating locations and the **Vaults of
Atal'Utek** public events — which is `coiled-isle`, while the renown track itself and its
Champion **wrist** (Cursebreaker's Bracers II, R9) are `zuljarra-renown`. Both are live in the
pre-season week. Whether the Coiled Isle joins the **Midnight World Tour** set is unverified.

Completing **all** faction events also finishes the **Midnight World Tour** quest → a second
Spark. **Overlap note (for the future ranker-wiring pass):** `liadrin-spark` picks *one* of
these to satisfy its weekly, and `void-assault` is a Singularity-adjacent event — don't
double-count the shared clears; the same caution now extends to `coiled-isle` /
`zuljarra-renown`, which own the Zul'jarra half of "faction renown this week". This row exists
for the Champion-gear + pinnacle-cache reward those rows don't capture.

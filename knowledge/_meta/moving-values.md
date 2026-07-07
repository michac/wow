---
title: Moving Values — flattened stale-data catcher
patch: 12.0.7
fetched: 2026-07-07
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24244888/revelations-content-update-notes
  - https://us.forums.blizzard.com/t/showdown-reward-changes-june-26-and-june-30/2320707/1  # world-boss loot + rare/crest changes (hotfix 6/26–30)
confidence: high
---

# Moving Values Registry

**A flattened, latest-value-wins list of the facts that change patch-over-patch
*and* are commonly mislabeled on the web.** This is *not* a mirror of the KB —
the `knowledge/` topic files remain the full flattened current state. This file
is a narrow, high-signal oracle for one job:

> When a web source (or your own memory) says "the world boss drops Veteran
> gear," check here first. If the row says the current value is something else,
> the source is **stale** — reject or re-verify it.

## Scope — what belongs here

Only facts that (a) get **re-tuned across patches** and (b) are **frequently
wrong on Wowhead / Reddit / SEO sites** because the internet remembers an older
value. Typical rows:

- reward **quality/track** and **item level** of specific loot (world bosses,
  event vendors, catch-up currencies, raid drops)
- structural counts that keep changing (site rotations, tier counts, caps)
- tuning that **superseded** an earlier published value

**Does NOT belong here:** anything stable across patches, class rotation minutiae
(lives in `classes/`), or volatile *live* data like AH/token prices (never
cached — fetch live). If a fact stops moving, it can graduate out of this file.

## How to read a row

- **Current value** wins. **Was** records the immediately-prior value so you can
  recognize the stale version when you see it in the wild.
- **Set by** is the patch/hotfix that established the current value — the anchor
  for provenance.
- **KB home** is the topic file that carries the full claim + citation. This
  registry defers to it; if they ever disagree, the topic file wins and this
  row is stale.

## Registry

Legend: WT = World Tier · ilvl ranges are the drop/purchase band, not upgrades.

| Fact | Current value | Was | Set by | KB home |
|---|---|---|---|---|
| World boss loot (Val/Naigtal "Midnight" rotation) | **Warbound Heroic 1/6** (Normal WT) / **Warbound Heroic 4/6** (Heroic WT), + per-character **Soulbound** Champion 4/6 (Normal) / Heroic 1/6 (Heroic) | Warbound **Champion** (Normal) / **Hero** (Heroic) | 12.0.7 hotfix (6/30) | endgame/world-events.md |
| Field Accolades — Maren Silverwing vendor | Sells **slot-targeted Hero-track gear (~ilvl 259)** | Accolades = transmog/decor **only** | 12.0.7 | endgame/world-events.md |
| Val/Naigtal rares & Dark Particles | Rares drop **2× crests** + can drop **Heroic Warbound-until-equipped** gear; Void-Touched Heroic Caches now **Warbound**; **Dark Particles** drop in Val/Naigtal, **stack to 1000** | pre-6/26 (1× crests, caches Soulbound) | 12.0.7 hotfix (6/26) | endgame/world-events.md |
| Prey — Nightmare rewards | **Champion-track** gear (~ilvl 259–279) + Veteran Dawncrests | — | 12.0.7 | endgame/prey.md |
| Prey — "Preferential Killing" weekly cap | **Removed** after rank 10 (Custom Hunts repeatable) | Once-per-week cap | 12.0.7 | endgame/prey.md |
| Sporefall raid — gear ilvl band | **259–298** (RF→Mythic) | — (new raid) | 12.0.7 | endgame/raids/sporefall.md |
| Ritual Sites — rotation & tiers | **3-site rotation, 6 tiers** | 2-site rotation, 5 tiers | 12.0.7 | systems/ritual-sites.md |
| Durability | Gear takes **no** durability damage from combat | Combat damaged durability | 12.0.7 | systems/professions.md |
| PvP gear item level | **+9** over previous season baseline | prior baseline | 12.0.7 | factions/slayers-rise.md |
| Crest / Conquest accumulation caps (Season 1) | **Removed** | Weekly accumulation caps | 12.0.7 hotfix (5/19) | endgame/weekly-checklist.md |

> **Maintenance:** `/update-patch` Step 4.5 refreshes this file each patch —
> for every reward/tuning change in the ledger, either update an existing row's
> **Current value** (moving its old value into **Was**) or add a new row. Keep
> it short; prune rows whose value has been stable for two+ patches.

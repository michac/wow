---
title: Holy Paladin — Talents & Builds (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/holy-paladin/talents  # tier 3, 2026-07-11 (12.0.7) — import strings
  - https://www.method.gg/guides/holy-paladin  # tier 3, 2026-07-11 (12.0.5/12.0.7 change notes)
  - https://maxroll.gg/wow/class-guides/holy-paladin-mythic-plus-guide  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/holy-paladin-pve-healing-guide  # tier 3, 2026-07-11
  - knowledge/classes/paladin/holy/talents.md  # tier 1 tree (Blizzard API + wago @ 12.0.7.67808)
confidence: medium
---

# Holy Paladin — Talents & Builds (Midnight S1)

Layered on top of the Tier-1 talent tree in `talents.md` (Blizzard API + wago,
12.0.7.67808). This file is the **narrative**: which hero tree, which loadouts,
and the interactions that matter. Import strings below are from method.gg
(Tier-3); **verify the hero tree loads correctly on import** — one bad character
breaks a string.

## Hero tree

Two hero trees, and they play the **same core rotation** (see `rotation.md`);
the pick changes your on-cooldown throughput button and your utility flavor.

- **Herald of the Sun — the throughput default.** Recommended for **raid** by
  every source, and per **maxroll the stronger M+ tree too** ("Lightsmith seems
  like a perfect choice for Mythic+ but in practice it lacks the healing power
  required in most Midnight dungeons"). Built around **Dawnlight** HoTs seeded by
  **Divine Toll** and **Holy Prism**, amplified during Avenging Wrath / Avenging
  Crusader by **Sun's Avatar** (beam-lines between Dawnlight targets). Highest
  skill-expression, highest healing.
- **Lightsmith — the utility/absorb tree.** Built around **Holy Armaments**
  (alternating **Sacred Weapon** buff / **Holy Bulwark** absorb), **Solidarity**,
  and **Hammer and Anvil** (leans on crit via Judgment). **method.gg leans
  Lightsmith for M+** for its buffs/absorbs and damage profile; **maxroll rates
  its raw HPS below Herald.** Genuine split — treat it as a comfort/utility
  choice rather than a throughput upgrade. 12.0.5 buffed Lightsmith (Holy
  Armaments now generates 3 Holy Power) specifically to make it viable.

> **Hero-tree recommendation is a live Tier-3 disagreement for M+**: method.gg
> → Lightsmith, maxroll → Herald of the Sun. Both agree Herald for raid. Default
> to **Herald of the Sun everywhere** unless you specifically want Lightsmith's
> absorbs/utility. @verify-ingame (which tree parses higher in current keys)

## Import strings (method.gg, 12.0.7)

- **Herald of the Sun (raid / general):**
  `CEEAVg1HmQqr1Dwlv86ljju8vCAAAYBAMDAAsMzMzYGzMzGDGzyYbmZYGNxwYmZYY2yAwAwGYjlZMzysNzMbNAAAALgB2MMmxAAAMzwMGjGA`
- **Lightsmith (M+, method's pick):**
  `CEEAAAAAAAAAAAAAAAAAAAAAAAAAAYBAMDAwglxMzMzYmZWGMGWGbzMLGNxwYmZYY2yAwAwGYzsMzMAIAgZmtlFbzMsxGzMsBMjBAYmBgZMGNA`

> Strings are tree-version-sensitive; re-check against method.gg if the talent
> tree changes in a later patch. @verify-ingame

## Core spec talents (both trees)

Near-universal picks per the Tier-3 guides:

- **Holy Shock** — foundational builder; everything keys off it.
- **Infusion of Light** — Holy Shock crits make the next Flash of Light / Holy
  Light instant and stronger; the whole spot-heal loop depends on it.
- **Light of Dawn** — reworked in Midnight to a **15-yd radius around the
  paladin** (from a frontal cone) — much easier to land; primary AoE spender.
- **Divine Toll** — 5-target Holy Shock burst; mandatory for Herald, strong
  everywhere. (Choice node vs Holy Prism in the class tree — most builds want
  Divine Toll; Holy Prism is also taken via the spec tree.)
- **Aura Mastery** — party ~12% DR (on Devotion Aura); core raid utility.
- **Avenging Wrath vs Avenging Crusader** — choice node. Avenging Wrath is the
  default 2-min throughput/crit CD; Avenging Crusader converts your
  Judgment/Crusader-Strike damage into group healing for players who want to
  stay on-target.

## Flex / choice nodes

- **Beacon: Beacon of Faith vs Beacon of Virtue.** Beacon of Faith is a second
  low-maintenance beacon (easy, cheap); Beacon of Virtue is a higher-ceiling
  burst-AoE beacon window. **Pair Beacon of Virtue with Pillars of Light** when
  you take it.
- **Liberation vs Crusader's Might** — Crusader's Might adds Crusader Strike as
  a builder that shaves Holy Shock / Light of Dawn cooldowns (smoother resource
  flow); Liberation is the alternate, currently strong per method.
- **Beacon of the Savior** (Apex) — passive auto-shield on the lowest-health
  ally roughly every 8s; a strong low-effort throughput/safety pick.
- **Tyr's Deliverance vs Hand of Divinity** — rolling group HoT/heal-amp vs a
  single-target external; pick by content.
- **Sanctified Wrath vs Awakening**, **Golden Path vs Selfless Healer**, and the
  various class-tree defensive choice nodes (Blessing of Freedom vs Steed of
  Liberty, etc.) — tune to the fight (see the full node list in `talents.md`).

## Key interactions

- **Holy Shock crit → Infusion of Light → instant Flash/Holy Light.** The
  spot-heal engine; keeping Holy Shock on cooldown maximizes procs.
- **Herald:** Divine Toll + Holy Prism apply **Dawnlight**; **Sun's Avatar**
  turns Avenging Wrath / Avenging Crusader into beam-line AoE. Press Divine Toll
  and Holy Prism on cooldown to keep Dawnlights out — the bulk of Herald's
  throughput.
- **Lightsmith:** **Holy Armaments** alternates Sacred Weapon / Holy Bulwark and
  (post-12.0.5) generates **3 Holy Power**; **Hammer and Anvil** rewards crit via
  Judgment. Keep Holy Armaments on cooldown.
- **Cooldown stacking:** **Avenging Wrath + Divine Toll** is the premium burst
  window; **avoid Avenging Wrath + Holy Prism** on constant-AoE pulls (overheal
  waste).

## Gaps

- No SimC APL / Tier-1 talent string for a healer spec — all import strings are
  Tier-3 (method.gg). @verify-ingame that each parses to the intended hero tree.
- The M+ hero-tree recommendation is an unresolved Tier-3 split (method →
  Lightsmith, maxroll → Herald). Flagged above.

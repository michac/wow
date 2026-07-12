---
title: Holy Paladin — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/holy-paladin  # tier 3, 2026-07-11 (12.0.7, upd. 2026-06-16)
  - https://www.method.gg/guides/holy-paladin/playstyle-and-rotation  # tier 3, 2026-07-11
  - https://www.icy-veins.com/wow/holy-paladin-pve-healing-rotation-cooldowns-abilities  # tier 3, 2026-07-11
  - https://maxroll.gg/wow/class-guides/holy-paladin-mythic-plus-guide  # tier 3, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1, name canonicalization
confidence: medium
---

# Holy Paladin — Ability Inventory (Midnight S1)

## Overview

Holy Paladin is a **reactive, build-and-spend healer**. The resource is
**Holy Power** (0–5): you *generate* it with a short list of instant abilities
(Holy Shock, Judgment, Crusader Strike, Divine Toll, and — per the Midnight
tier-3 guides — Flash of Light) and *spend* it in 3-Holy-Power chunks on a heal
(Word of Glory / Eternal Flame single-target, Light of Dawn for AoE) or on
**Shield of the Righteous** as a damage/defensive dump when nobody needs
healing. Mana still gates the big direct casts (Flash of Light, Holy Light).
The spec also does meaningful damage — Judgment, Crusader Strike, Hammer of
Wrath and Holy Prism feed Holy Power and, under **Avenging Crusader** or
**Beacon**-conversion, that damage turns into healing.

**Hero trees (Midnight):**
- **Herald of the Sun** — the throughput tree; **Divine Toll** and **Holy
  Prism** seed **Dawnlight** HoTs, and during Avenging Wrath/Avenging Crusader
  those Dawnlights link beam-lines (**Sun's Avatar**) that heal/damage anything
  crossing them. Default for raid, and per maxroll the stronger M+ pick too.
- **Lightsmith** — the utility/absorb tree built around **Holy Armaments**
  (alternating **Sacred Weapon** buff / **Holy Bulwark** absorb), Solidarity,
  and Hammer and Anvil. Method leans Lightsmith for M+; maxroll says it "lacks
  the healing power" most Midnight dungeons demand (see `builds.md`).

> **12.0.5 changes carried into 12.0.7:** Holy-Power spender healing (Light of
> Dawn, Eternal Flame, Word of Glory) up **15%**; **Holy Armaments now
> generates 3 Holy Power**; Lightsmith retuned to be viable. Core build-and-spend
> loop is otherwise unchanged. (method.gg intro, 12.0.7.)

## Inventory

Cooldowns marked @verify-ingame are best-known baseline values that the
tier-3 guides did not state numerically for 12.0.7; confirm the exact number
in-game. Holy Shock's cooldown scales with Haste.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Holy Shock | Rotational-builder | Mana; +1 Holy Power | Instant / ~7.5s (Haste-scaled) | The core builder — instant heal on an ally **or** damage on an enemy; can crit for **Infusion of Light** (next Flash/Holy Light instant & stronger). Press on cooldown. |
| Judgment | Rotational-builder | Mana; +1 Holy Power | Instant / ~6s @verify-ingame | Ranged Holy damage that generates Holy Power (Greater Judgment). In Midnight it is "primarily for damage now" but still a builder; keep it rolling. |
| Crusader Strike | Rotational-builder | Mana; +1 Holy Power | Instant / charges (Crusader's Might) | Melee builder taken via **Crusader's Might**; also shaves time off Holy Shock / Light of Dawn. Optional talent. |
| Hammer of Wrath | Rotational-builder | Mana; +Holy Power | Instant / ~7.5s @verify-ingame | Execute-range ranged strike (target below health threshold, or always usable during Avenging Wrath). Extra builder + damage. |
| Flash of Light | Rotational-builder / spot heal | Mana; +Holy Power @verify-ingame | ~1.5s cast / — | Fast, mana-hungry direct heal; **instant and boosted** under Infusion of Light. Both method.gg and Icy Veins list it as a Holy-Power generator in Midnight — @verify-ingame the Holy-Power gain. |
| Holy Light | Spot heal | Mana | ~2.5s cast / — | Slow, mana-efficient big single-target heal; cast when mana permits and the damage is not urgent. Icy Veins also lists it as a builder — @verify-ingame. |
| Word of Glory | Rotational-spender | 3 Holy Power | Instant / — | Instant single-target Holy-Power heal. Default single-target spender when not talented into Eternal Flame. |
| Eternal Flame | Rotational-spender | 3 Holy Power | Instant / — | Herald talent that **replaces Word of Glory**: same direct heal plus a HoT; the preferred M+ spender and Dawnlight enabler. |
| Light of Dawn | Rotational-spender (AoE) | 3 Holy Power | Instant / — | Instant AoE heal — in Midnight a **15-yd radius around the paladin** (reworked from a frontal cone). Primary raid/AoE spender. |
| Shield of the Righteous | Defensive / Holy-Power dump | 3 Holy Power | Instant / — | Self damage-reduction + Holy damage; the "nothing to heal, don't overcap" spender. |
| Divine Toll | Major cooldown / builder | Mana | Instant / ~1 min | Fires a Holy Shock at up to 5 targets at once — huge burst of healing + Holy Power. Herald's key button (seeds Dawnlight). Keep on cooldown; hold only for imminent damage. |
| Holy Prism | Rotational-spender (CD) | Mana | Instant / ~20s @verify-ingame | Cast on an **enemy** to heal 5 nearby allies, or on an **ally** to damage 5 nearby enemies. Keep on cooldown; also seeds Dawnlight (Herald). |
| Barrier of Faith | Defensive (absorb) | Mana | Instant / ~30s @verify-ingame | Places an absorb shield on an ally that also empowers your next heals on them. Talent. |
| Beacon of Light | Utility (passive link) | Mana | Instant / — | Duplicates a % of your healing onto the beaconed ally. Park on a tank. |
| Beacon of Faith | Utility (2nd beacon) | Mana | Instant / — | A **second** beacon (choice vs Beacon of Virtue); cheaper, low-maintenance. |
| Beacon of Virtue | Rotational-spender (CD) | Mana / 3 Holy Power | Instant / ~15s @verify-ingame | Beacons the target **and** several nearby injured allies for a short window, then heals them from your casts — burst AoE beacon. Time it "right after the first tick of damage." |
| Beacon of the Savior | Passive (Apex) | — | — | Apex talent: auto-shields the lowest-health ally roughly every 8s. |
| Avenging Wrath | Major cooldown | — | Instant / ~2 min | +healing, +damage, +crit for the duration (~20s). Best paired with Divine Toll ("godlike"). Choice vs Avenging Crusader. |
| Avenging Crusader | Major cooldown | — | Instant / ~2 min @verify-ingame | Choice-node alternative to Avenging Wrath: **Judgment and Crusader Strike heal** nearby allies for a large amount during the window — a damage-to-healing throughput CD. |
| Aura Mastery | Major cooldown (raid DR) | Mana | Instant / ~3 min, 8s | Amplifies your active aura; on **Devotion Aura** it becomes party-wide damage reduction (~12%). Pre-cast before scripted raid-wide damage. |
| Tyr's Deliverance | Major cooldown | Mana | Instant / ~90s @verify-ingame | Ground/party HoT window that also empowers your Flash/Holy Light on affected allies. Choice vs Hand of Divinity. |
| Holy Armaments | Major cooldown / builder (Lightsmith) | Mana; +3 Holy Power | Instant / ~1 min @verify-ingame | Lightsmith button; **alternates** between **Sacred Weapon** and **Holy Bulwark** each cast. Now generates 3 Holy Power. Keep on cooldown when playing Lightsmith. |
| Sacred Weapon | Utility buff (Lightsmith) | — | (via Holy Armaments) | Weapon armament: buffs an ally's damage/healing and adds Holy strikes. One half of Holy Armaments. |
| Holy Bulwark | Defensive (absorb, Lightsmith) | — | (via Holy Armaments) | Absorb-shield armament placed on an ally. The other half of Holy Armaments. |
| Rite of Sanctification | Utility (Lightsmith) | Mana | Instant / — | Lightsmith self/party buff (armor/stats). Choice vs Rite of Adjuration. |
| Lay on Hands | Defensive (emergency) | — | Instant / ~10 min | Instantly heals an ally (or self) to full health. The panic button. |
| Blessing of Freedom | Utility (dispel movement) | Mana | Instant / ~25s | Immunity to movement-impairing effects on an ally. |
| Blessing of Protection | Defensive (external) | Mana | Instant / ~5 min | Physical-damage immunity + removes/immunes physical debuffs on an ally. |
| Blessing of Sacrifice | Defensive (external) | Mana | Instant / ~2.5 min @verify-ingame | Redirects a % of damage taken by an ally to you. |
| Divine Protection | Defensive (self) | — | Instant / ~1 min | Self damage reduction for ~8s. |
| Divine Shield | Defensive (immunity) | — | Instant / ~5 min | Full immunity for ~8s; can be used aggressively to free-cast, or as a panic/drop-threat tool. |
| Divine Steed | Movement | — | Instant / ~45s, 2 charges | +100% movement speed for a few seconds (mounted). |
| Hammer of Justice | CC (stun) | Mana | Instant / ~60s | Single-target stun. |
| Blinding Light | CC (AoE disorient) | Mana | Instant / ~90s | Disorients all nearby enemies. Talent. |
| Turn Evil | CC (fear) | Mana | ~1.5s cast / — | Fears an Undead/Demon/Aberration target. |
| Cleanse | Dispel | Mana | Instant / ~8s | Removes Magic (and Poison/Disease) from an ally. |
| Intercession | Utility (combat rez) | Mana | ~2s cast / — | Battle-resurrection: revives a dead ally during combat. |
| Redemption | Utility (rez) | Mana | ~10s cast / — | Out-of-combat resurrection. |
| Hand of Reckoning | Utility (taunt) | Mana | Instant / ~8s | Taunts a target; ranged threat tool. |
| Devotion Aura | Passive (aura) | — | — | Party-wide passive damage reduction aura; the Aura Mastery target. |
| Concentration Aura | Passive (aura) | — | — | Reduces silence/interrupt/school-lock effects for the party. |
| Crusader Aura | Passive (aura) | — | — | +mounted movement speed for the party. |

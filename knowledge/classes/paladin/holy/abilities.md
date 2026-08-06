---
title: Holy Paladin — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/paladin/holy/ability-inventory.tsv  # tier 1, generated from DB2 @ build 12.0.7.67808 — name/spellID/origin/cooldown floor
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
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

**`ability-inventory.tsv` in this directory is the Tier-1 floor** — canonical name,
spellID, origin (class-baseline / talent-active / talent-choice) and baseline cooldown are
regenerated there from DB2 and are not duplicated here. This file is the prose layer: role,
when to press it, and how the hero trees bend it.

A cooldown written **`45s [T1]`** was read off that tsv (DB2 @ build 12.0.7.67808) and is
the baseline before talents and Haste; a `~` value is guide-derived. Holy Shock's cooldown
scales with Haste. `@verify-ingame` marks what Tier 1 could not settle — Holy-Power gains,
effect magnitudes, and charge *recharge* times (the tsv's cooldown column returns 0 or the
GCD for charge-based abilities such as Holy Armaments).

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.0.7.67808).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Holy Shock | Rotational-builder | Mana; +1 Holy Power | Instant / ~7.5s (Haste-scaled) | The core builder — instant heal on an ally **or** damage on an enemy; can crit for **Infusion of Light** (next Flash/Holy Light instant & stronger). Press on cooldown. |
| Judgment | Rotational-builder | Mana; +1 Holy Power | Instant / ~6s @verify-ingame | Ranged Holy damage that generates Holy Power (Greater Judgment). In Midnight it is "primarily for damage now" but still a builder; keep it rolling. |
| Crusader Strike | Rotational-builder | Mana; +1 Holy Power | Instant / charges | **Class-baseline, not a talent [T1]** — what **Crusader's Might** adds is the Holy Shock / Light of Dawn cooldown reduction on it. Melee builder; optional in the priority, not optional in the kit. |
| Hammer of Wrath | Rotational-builder | Mana; +Holy Power | Instant / ~7.5s @verify-ingame | Execute-range ranged strike (target below health threshold, or always usable during Avenging Wrath). Extra builder + damage. |
| Flash of Light | Rotational-builder / spot heal | Mana; +Holy Power @verify-ingame | ~1.5s cast / — | Fast, mana-hungry direct heal; **instant and boosted** under Infusion of Light. Both method.gg and Icy Veins list it as a Holy-Power generator in Midnight — @verify-ingame the Holy-Power gain. |
| Holy Light | Spot heal | Mana | ~2.5s cast / — | Slow, mana-efficient big single-target heal; cast when mana permits and the damage is not urgent. Icy Veins also lists it as a builder — @verify-ingame. |
| Word of Glory | Rotational-spender | 3 Holy Power | Instant / — | Instant single-target Holy-Power heal. Default single-target spender when not talented into Eternal Flame. |
| Eternal Flame | Rotational-spender | 3 Holy Power | Instant / — | Herald talent that **replaces Word of Glory**: same direct heal plus a HoT; the preferred M+ spender and Dawnlight enabler. |
| Light of Dawn | Rotational-spender (AoE) | 3 Holy Power | Instant / — | Instant AoE heal — in Midnight a **15-yd radius around the paladin** (reworked from a frontal cone). Primary raid/AoE spender. |
| Shield of the Righteous | Defensive / Holy-Power dump | 3 Holy Power | Instant / — | Self damage-reduction + Holy damage; the "nothing to heal, don't overcap" spender. |
| Divine Toll | Major cooldown / builder | Mana | Instant / ~1 min | Fires a Holy Shock at up to 5 targets at once — huge burst of healing + Holy Power. Herald's key button (seeds Dawnlight). Keep on cooldown; hold only for imminent damage. |
| Holy Prism | Rotational-spender (CD) | Mana | Instant / 45s [T1] | Cast on an **enemy** to heal 5 nearby allies, or on an **ally** to damage 5 nearby enemies. Keep on cooldown; also seeds Dawnlight (Herald). |
| Beacon of Light | Utility (passive link) | Mana | Instant / — | Duplicates a % of your healing onto the beaconed ally. Park on a tank. |
| Beacon of Faith | Utility (2nd beacon) | Mana | Instant / — | A **second** beacon (choice vs Beacon of Virtue); cheaper, low-maintenance. |
| Beacon of Virtue | Rotational-spender (CD) | Mana / 3 Holy Power | Instant / 15s [T1] | Beacons the target **and** several nearby injured allies for a short window, then heals them from your casts — burst AoE beacon. Time it "right after the first tick of damage." |
| Beacon of the Savior | Passive (Apex) | — | — | Apex talent: auto-shields the lowest-health ally roughly every 8s. |
| Avenging Wrath | Major cooldown | — | Instant / ~2 min | +healing, +damage, +crit for the duration (~20s). Best paired with Divine Toll ("godlike"). Choice vs Avenging Crusader. |
| Avenging Crusader | Major cooldown | — | Instant / 60s [T1] | Choice-node alternative to Avenging Wrath: **Judgment and Crusader Strike heal** nearby allies for a large amount during the window — a damage-to-healing throughput CD. |
| Aura Mastery | Major cooldown (raid DR) | Mana | Instant / ~3 min, 8s | Amplifies your active aura; on **Devotion Aura** it becomes party-wide damage reduction (~12%). Pre-cast before scripted raid-wide damage. |
| Tyr's Deliverance | Major cooldown | Mana | Instant / 90s [T1] (class-baseline) | Ground/party HoT window that also empowers your Flash/Holy Light on affected allies. Choice vs Hand of Divinity. |
| Holy Armaments | Major cooldown / builder (Lightsmith) | Mana; +3 Holy Power | Instant / charges @verify-ingame (recharge) | Lightsmith button, and **the acquisition point for both armaments** — it **alternates** between **Sacred Weapon** and **Holy Bulwark** each cast. Now generates 3 Holy Power. Keep on cooldown when playing Lightsmith. |
| Sacred Weapon | Utility buff (Lightsmith) | — | (output of Holy Armaments) | Weapon armament: buffs an ally's damage/healing and adds Holy strikes. **Not a talent or a button of its own [T1]** — no spell named Sacred Weapon has an acquisition row; the tree node you take is **Holy Armaments** (Lightsmith subtree), which the tsv carries under the `Holy Bulwark ⇄ Holy Armaments` alias. |
| Holy Bulwark | Defensive (absorb, Lightsmith) | — | (via Holy Armaments) | Absorb-shield armament placed on an ally. The other half of Holy Armaments. |
| Rite of Sanctification | Utility (Lightsmith) | Mana | Instant / — | Lightsmith self/party buff (armor/stats). Choice vs Rite of Adjuration. |
| Lay on Hands | Defensive (emergency) | — | Instant / ~10 min | Instantly heals an ally (or self) to full health. The panic button. |
| Blessing of Freedom | Utility (dispel movement) | Mana | Instant / ~25s | Immunity to movement-impairing effects on an ally. |
| Blessing of Protection | Defensive (external) | Mana | Instant / ~5 min | Physical-damage immunity + removes/immunes physical debuffs on an ally. |
| Blessing of Sacrifice | Defensive (external) | Mana | Instant / 120s [T1] | Redirects a % of damage taken by an ally to you. |
| Divine Protection | Defensive (self) | — | Instant / ~1 min | Self damage reduction for ~8s. |
| Divine Shield | Defensive (immunity) | — | Instant / ~5 min | Full immunity for ~8s; can be used aggressively to free-cast, or as a panic/drop-threat tool. |
| Divine Steed | Movement | — | Instant / ~45s, 2 charges | +100% movement speed for a few seconds (mounted). |
| Hammer of Justice | CC (stun) | Mana | Instant / **45s** `[T1]` | Single-target stun. |
| Blinding Light | CC (AoE disorient) | Mana | Instant / ~90s | Disorients all nearby enemies. Talent. |
| Turn Evil | CC (fear) | Mana | ~1.5s cast / **15s** `[T1]` | Fears an Undead/Demon/Aberration target. |
| Cleanse | Dispel | Mana | Instant / ~8s | Removes Magic (and Poison/Disease) from an ally. |
| Intercession | Utility (combat rez) | Mana | ~2s cast / **600s** `[T1]` | Battle-resurrection: revives a dead ally during combat. |
| Redemption | Utility (rez) | Mana | ~10s cast / — | Out-of-combat resurrection. |
| Hand of Reckoning | Utility (taunt) | Mana | Instant / ~8s | Taunts a target; ranged threat tool. |
| Devotion Aura | Passive (aura) | — | — | Party-wide passive damage reduction aura; the Aura Mastery target. |
| Crusader Aura | Passive (aura) | — | — | +mounted movement speed for the party. |

## Reconciliation notes — Tier 1 @ 12.0.7.67808

- **Barrier of Faith is not acquirable at 12.0.7** and the row is deleted. None of the
  spells carrying that name attaches to a trait node, skill line, `SpecializationSpells` or
  `PvpTalent` row, and the live Paladin tree (**790**) carries **Seraphic Barrier** where it
  used to sit. Do not author it as a live talent.
- **Concentration Aura is likewise gone** — row deleted. `Devotion Aura` is still on the
  Paladin skill line and `Aura Mastery` / `Auras of the Resolute` are still on tree 790, so
  the aura *system* is intact; this specific aura is not.
- **Sacred Weapon has no acquisition row of its own.** The talent is **Holy Armaments**;
  Sacred Weapon and Holy Bulwark are its two alternating outputs. The row above is
  re-anchored accordingly (the tsv carries the `Holy Bulwark ⇄ Holy Armaments` alias).
- **Crusader Strike is class-baseline**, not a talent.
- Corrected against guide values: Holy Prism **45s** (was ~20s), Avenging Crusader **60s**
  (was ~2 min), Blessing of Sacrifice **120s** (was ~2.5 min).

---
title: Unmapped / build-variant abilities per spec (companion to seed-edits-proposed.md)
date: 2026-07-14
scope: rotational + important (constant/frequent/cooldown) abilities with no seed bind, all 40 specs
source: per-spec KB priority lists vs the (post Tier-A) seed
---

# Unmapped / build-variant abilities

For every spec, this lists **important** abilities (press-frequency constant / frequent /
cooldown, from the KB `priority` list) whose name is **not** bound anywhere in the current
seed. Each is tagged so we know whether it actually needs a key:

- **override-covered** — a talent/proc *replacement* of an already-bound base ability. WoW
  swaps the button at runtime, so **binding the base is enough** — do NOT add a key. (e.g.
  Infernal Bolt over Shadow Bolt, Wither over Immolate, Black Arrow over Kill Shot.)
- **build-specific** — only exists under a particular hero tree / talent. Safe to place in the
  seed *if* the addon skips it when unlearned (see the addon note below); otherwise a tweak.
- **needs a slot** — a genuine, build-independent ability the seed simply left unbound. These
  are the real candidates for new binds.

## How the addon should absorb build variance (design note)

The seed stores **base / player-agnostic** abilities; the dumper resolves the rest at apply time:
1. **Resolve override base** (`C_Spell.GetOverrideSpell` / `FindBaseSpellByID`) — placing a base
   spell shows its active override automatically, so override pairs need only the base bound.
2. **Skip-if-unknown** (`IsSpellKnown` / `IsPlayerSpell`) — a build-specific ability the player
   hasn't learned is skipped and reported, never a dead key. This is why *build-specific* binds
   are safe to keep in the one universal seed.
So we never need per-build seed variants: base + these two runtime checks cover every case below.

### Death Knight — Blood

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Exterminate | cooldown | build-specific | Deathbringer proc consumed via Marrowrend |
| Vampiric Strike | frequent | build-specific | San'layn proc button; stacks Essence of the Blood Queen |

### Death Knight — Frost

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Chosen of Frostbrood | cooldown | needs a slot | Listed in the inventory as a Midnight-era capstone cooldown tied to the FWF burst window, but the seed assigns it to no bucket at all. If it is an active press it needs a … |

### Death Knight — Unholy

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Raise Abomination | cooldown | needs a slot | ~90s summon (choice vs Army/Gargoyle) |
| Summon Gargoyle | cooldown | needs a slot | Choice-node summon CD |
| Apocalypse Now | cooldown | build-specific | Rider of the Apocalypse hero capstone burst CD (summons all four Horsemen) — a real on-cooldown press for Rider builds, but the seed binds no slot for it. Combat 10/11 (S … |
| Gift of the San'layn | cooldown | build-specific | San'layn hero burst window layered onto Dark Transformation — an active cooldown for San'layn builds, left unbound. Should take a free shift/alt slot for whichever hero t … |
| Necrotic Coil | frequent | override-covered | Replaces Death Coil for 30s after Army (Forbidden Knowledge) |
| Vampiric Strike | frequent | override-covered | San'layn only — replaces Scourge Strikes, builds Blood Queen |

### Demon Hunter — Devourer

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Hungering Slash | frequent | build-specific | Core builder of the Void-Scarred melee-hybrid build (converts Voidblade/The Hunt into slashes; priority: frequent in that build). Not in the seed at all; melee-hybrid pla … |
| Collapsing Star | frequent | override-covered | The in-Meta payoff spender (30 Souls, always crits, ramps per cast; priority: frequent during the burst window) has NO bucket in the seed. Unlike Cull/Devour/Eradicate wh … |
| Cull | frequent | override-covered | Meta-form upgrades of Reap/Consume. They auto-replace their base abilities on the same buttons (Combat 2 and Combat 1), so no new key is required — worth confirming the o … |
| Devour | frequent | override-covered | Meta-form upgrades of Reap/Consume. They auto-replace their base abilities on the same buttons (Combat 2 and Combat 1), so no new key is required — worth confirming the o … |
| Eradicate | frequent | override-covered | The AoE frontal-cone multi-target backbone (replaces Reap after a full Void Ray channel; priority: frequent). It replaces Reap so it can inherit the Reap key (Combat 2/2) … |
| Pierce the Veil | cooldown | override-covered | Void-Scarred's Meta-only empowered Voidblade (triggers Voidsurge). Build-specific; overlays Voidblade (Combat 7/R) in Meta so likely no separate bind, but entirely unment … |

### Demon Hunter — Vengeance

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Reaver's Glaive | frequent | build-specific | Aldrachi Reaver rotational-spender/empower that starts the AR damage cycle (Rending Strike + Glaive Flurry). Marked 'frequent' in the priority list yet has no bucket. AR  … |
| Untethered Rage | cooldown | build-specific | Apex/Annihilator cooldown — activates the granted special Metamorphosis charge on proc (~1/min+), the core Annihilator burst trigger. It is not assigned to any bucket in  … |

### Druid — Balance

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Ascendant Eclipses | cooldown | needs a slot | The new Midnight capstone active burst (spell 1261564) is not bound anywhere. If talented it's a cooldown-frequency press that needs a Shift/Combat slot. |
| Eclipse | frequent | needs a slot | Post-rework, Solar and Lunar Eclipse are separate activated states. The seed binds only Lunar Eclipse (Combat 7), so the Solar side (Wrath-empowered, used ≤3 targets) can … |
| Full Moon | frequent | needs a slot | The Moon-chain builders are unbound. Acceptable given the seed assumes the Force of Nature build (Combat 11), but if the player runs the Moon-chain talent these 'frequent … |
| Half Moon | frequent | needs a slot | The Moon-chain builders are unbound. Acceptable given the seed assumes the Force of Nature build (Combat 11), but if the player runs the Moon-chain talent these 'frequent … |
| Incarnation: Chosen of Elune | cooldown | needs a slot | Preferred M+/council burst; only Celestial Alignment (its base form) is bound. If the Incarnation node is talented, the Combat 9 bind should be Incarnation, not CA. |
| New Moon | frequent | needs a slot | The Moon-chain builders are unbound. Acceptable given the seed assumes the Force of Nature build (Combat 11), but if the player runs the Moon-chain talent these 'frequent … |

### Druid — Feral

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Incarnation: Avatar of Ashamane | cooldown | needs a slot | The choice-node alternative to Convoke; if the player talents Incarnation instead, it has no bucket. Not a hard gap (shares Convoke's node) but should occupy Combat 10 wh … |
| Ravage | frequent | build-specific | Druid of the Claw proc spender, marked 'frequent — reactive, press ASAP' in the priority, but it appears in no bucket. A proc-driven spender you must fire immediately nee … |

### Druid — Guardian

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Incarnation: Guardian of Ursoc | cooldown | needs a slot | The standard tank capstone major CD is unbound. Defensible IF the build took Berserk + Convoke instead (choice node), which the seed appears to assume — but if Incarnatio … |
| Raze | frequent | needs a slot | Frontal AoE rage dump (talent) in cleave/AoE |
| Red Moon | cooldown | needs a slot | Single-target capstone; on CD, Mangle on 2 charges while active |
| Wild Guardian | cooldown | needs a slot | The Midnight-new burst capstone active (spell 1269614, replacing Rage of the Sleeper) is completely absent from the seed. It is a core cooldown fired at max Thrash / duri … |

### Druid — Restoration

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Efflorescence | frequent | needs a slot | Technically placed, but mis-bucketed as a 'Raid Defensive' and buried on a slow Ctrl key despite being a 'frequent' maintained heal — effectively hidden from the fast rot … |
| Flourish | cooldown | needs a slot | HoT-extend cooldown (~90s, huge throughput after a ramp) has no bucket. It is a choice-node vs Inner Peace so may be untalented, but when talented it is an active press w … |
| Convoke the Spirits | cooldown | build-specific | A major cooldown and the Wildstalker default (~1min with Cenarius' Guidance) is unplaced. It is a choice-node vs Incarnation (which the seed did place on Combat 10), so t … |

### Evoker — Devastation

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Azure Sweep | frequent | needs a slot | Its own APL priority entry; fired when available. |
| Firestorm | cooldown | needs a slot | ~20s ground AoE spender talent; when specced it is an active rotational press with no bind. Belongs on an open Combat/Shift slot. |
| Shattering Star | cooldown | needs a slot | ~20s / 2-charge builder granting Essence Burst plus a damage-amp debuff — a core rotational button (frequency: cooldown, but woven often) when specced. The seed binds it  … |
| Engulf | cooldown | build-specific | Flameshaper hero rotational burst button (consumes the Fire Breath DoT, short CD). Unbound; needs a fast slot whenever the Flameshaper build is run. |
| Mass Disintegrate | frequent | build-specific | Scalecommander cleave — chain Disintegrate while stacks are up. |

### Evoker — Preservation

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Merithra's Blessing | frequent | needs a slot | Biggest gap: it is a 'frequent' apex Echo finisher and the strongest heal, pressed whenever available, yet it is not bound to any bucket. It should own a fast unmodified  … |
| Stasis | cooldown | needs a slot | Choice-node options (Stasis vs Dream Flight; Time Spiral vs Spatial Paradox) are unbound. Lower priority since their alternatives are placed, but a Stasis-based build has … |

### Hunter — Beast Mastery

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Nature's Ally | cooldown | needs a slot | Capstone active that empowers Kill Command, pressed on cooldown in the core rotation, but not placed anywhere. Prime fast keys Combat 7/8 sit empty. |
| Wailing Arrow | cooldown | override-covered | Dark Ranger rotational cooldown (guaranteed Deathblow, overlays the Bestial Wrath button after activation) — missing from the map despite being a frequent-tier press in t … |

### Hunter — Marksmanship

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Explosive Shot | frequent | needs a slot | A 'frequent' rotational filler (~20s CD, procs Lock and Load → instant Aimed Shot) is not bound anywhere. Combat 10 (S2) is empty and is the natural shift-layer home for  … |
| Moonlight Chakram | frequent | build-specific | Sentinel's frequent recastable mini-Trueshot (grants free Lock and Load) is unbound. Combat 11 (S3) is empty — ideal for a frequent-but-secondary rotational button on the … |
| Wailing Arrow | cooldown | build-specific | Dark Ranger Trueshot-window cast; generates Deathblow |
| Kill Shot | frequent | override-covered | The baseline/Sentinel execute is left unbound; only Black Arrow (its Dark Ranger replacement) is placed. Build-dependent, but Sentinel/baseline players need Kill Shot bou … |

### Hunter — Survival

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Moonlight Chakram | frequent | build-specific | Sentinel hero-tree rotational button flagged 'frequent' in the priority (thrown inside Tip of the Spear windows) but assigned to no bucket at all. Sentinel players have n … |

### Mage — Arcane

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Touch of the Archmage | cooldown | needs a slot | Spec capstone active (row 11) tied to the burst window, frequency 'cooldown', but it is not assigned to any bucket in the seed. It should occupy one of the free Combat 10 … |

### Mage — Frost

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Glacial Spike | frequent | needs a slot | Frequent rotational spender (on CD / at 5 Icicles) — a core damage button left entirely unbound while a 60s Ray of Frost sits on the prime Q key. Needs a fast unmodified  … |
| Icy Veins | cooldown | needs a slot | Primary ~3min burst/Thermal Void cooldown (verify manual-press status). Not bound anywhere; belongs on a Shift or Alt cooldown slot so the burst window can be triggered. |
| Shifting Power | cooldown | needs a slot | Core M+ cooldown-cycling channel with no bind. Should occupy a Shift/Alt cooldown slot for dungeon play. |
| Comet Storm | cooldown | build-specific | Major ~30s AoE burst, high priority for both Spellslinger and Frostfire trees, and Frostfire's lead burst. Completely unbound — should own the Combat 12 slot currently wa … |

### Monk — Brewmaster

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Celestial Brew | frequent | needs a slot | Absorb; in MoH it discharges the Aspect of Harmony pool. |
| Empty the Cellar | cooldown | needs a slot | Grounding notes it 'appears as its own action in the APL' (Brew CDR value), but the seed gives it no bucket. Minor/optional — mostly passive-adjacent — but worth a slot i … |

### Monk — Mistweaver

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Invoke Yu'lon / Invoke Chi-Ji | cooldown | needs a slot | ~3 min major healing CD; pre-planned to damage events. |
| Vivify | frequent | needs a slot | CRITICAL omission — Vivify (spell 116670) is the core spot heal AND the Renewing Mist cleave-heal payoff, rated 'frequent' in the priority list, yet it is bound to no buc … |

### Monk — Windwalker

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Celestial Conduit | cooldown | needs a slot | Conduit-of-the-Celestials hero cooldown, a channeled nuke pressed in the Zenith window when Heart of the Jade Serpent is down. Unbound; needed for the Conduit build (asse … |
| Rushing Wind Kick | frequent | needs a slot | Priority-list frequency is 'frequent' (talent strike woven high in the rotation), yet it has no bucket at all. A frequent rotational button unbound is the biggest gap — t … |
| Tigereye Brew | cooldown | needs a slot | Spec capstone burst cooldown (stacks from Chi spent, consumed for a crit window) — a real damage cooldown left entirely unbound. Belongs on an open shift slot (Combat 10/ … |

### Paladin — Holy

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Avenging Crusader | cooldown | needs a slot | Choice-node alternative to Avenging Wrath. Not strictly missing (shares Combat 9 with AW as a choice node) but should be noted as the same-slot swap so the S1 binding cov … |
| Beacon of Virtue | cooldown | needs a slot | ~15s burst-AoE beacon spender when talented — pressed on a short cadence right after AoE ticks. Unbound; a Shift or fast slot is warranted when speccing it. |
| Crusader Strike | frequent | needs a slot | Listed 'frequent' when talented (Crusader's Might) — a melee builder that also shaves Holy Shock / Light of Dawn cooldowns. Unbound; needs a fast or Shift-Combat slot whe … |
| Hammer of Wrath | frequent | needs a slot | Listed 'frequent' — a recurring builder+damage button in execute range and during Avenging Wrath. Completely unbound; belongs on a fast unmodified key (e.g. reclaim Comba … |
| Holy Prism | cooldown | needs a slot | ~20s-cooldown spender/Dawnlight seed, priority 'on cooldown'. Unbound; a Shift-Combat slot (S3/S4) fits. |
| Tyr's Deliverance | cooldown | needs a slot | ~90s rolling group-HoT / heal-amp cooldown, priority 'roll on cooldown'. Unbound despite empty Shift and Ctrl slots. |
| Divine Toll | cooldown | build-specific | The single most important omission. It is the Herald's key ~1-min button (fires Holy Shock at up to 5 targets, huge HP+healing burst, seeds Dawnlight), flagged 'keep on c … |
| Holy Armaments | cooldown | build-specific | ~1 min; Lightsmith's on-cooldown button (Sacred Weapon / Holy Bulwark alternation, +3 HP). |
| Eternal Flame | frequent | override-covered | The default Herald single-target Holy-Power spender that REPLACES Word of Glory. The seed binds only WoG (the fallback), so on the recommended build the actual button pre … |

### Paladin — Protection

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Hammer of Wrath | frequent | needs a slot | High-priority execute/Wings builder (Judgment transform) whenever available. |
| Hammer of the Righteous | frequent | needs a slot | Choice-node builder alternative; single-target/Blessed Assurance builds. |
| Avenging Wrath | cooldown | build-specific | The default major offensive CD ('Wings'), +20% dmg/healing on a ~1-min cadence the whole rotation is tuned around, and it converts Judgment to Hammer of Wrath. The seed b … |
| Sacred Weapon | cooldown | build-specific | Lightsmith armament (weapon buff, Holy dmg/healing) that shares the Holy Armaments charge pool with the bound Holy Bulwark and must be refreshed when the buff wanes — a r … |
| Hammer of Light | frequent | override-covered | Templar top-priority spender for 12s after every Divine Toll. Not separately mapped, but it REPLACES Divine Toll on the same button, so it is effectively covered by Comba … |

### Paladin — Retribution

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Hammer of Wrath | frequent | needs a slot | 'Frequent' priority builder (~7.5s): usable sub-20% and on ANY-health target during wings (free/priority with Walk Into Light). A core rotational button that is omitted e … |
| Shield of Vengeance | cooldown | needs a slot | A real personal defensive (absorb + holy-damage reflect) with the Personal Defensive 2 (SZ) slot sitting empty — should be bound there. |
| Templar Strike / Templar Slash | constant | needs a slot | Filler builder (or Crusader Strike / Crusading Strikes autos) — keeps Holy Power flowing between higher priorities. |
| Hammer of Light | frequent | override-covered | 'Frequent' Templar signature spender: replaces Wake of Ashes for 20s after WoA, a 5-HP nuke that is the TOP spend priority when available (fuels Shake the Heavens / Empyr … |

### Priest — Discipline

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Master the Darkness | cooldown | needs a slot | Apex talent active empowering Atonement / upgrading to Void Shield — listed as an active cooldown but given no bind. |
| Mindbender | cooldown | needs a slot | Major pet cooldown (Mindbender ~1min, Shadowfiend ~3min) — a core damage/mana cooldown pressed every window, yet the seed gives it no bind at all. Belongs on a shift/Alt  … |
| Shadowfiend | cooldown | needs a slot | Major pet cooldown (Mindbender ~1min, Shadowfiend ~3min) — a core damage/mana cooldown pressed every window, yet the seed gives it no bind at all. Belongs on a shift/Alt  … |
| Ultimate Penitence | cooldown | needs a slot | 4-min offensive major cooldown (big Atonement-healing burst, choice vs Power Word: Barrier) — completely unbound in the seed. |
| Void Shield | frequent | needs a slot | Upgraded shield (Master the Darkness), multi-target Atonement |
| Premonition | cooldown | build-specific | Oracle hero-talent active on ~60s CD (throughput/defensive) — a frequent, important button for the Oracle build with no bind. |
| Void Torrent | cooldown | build-specific | Voidweaver major channel cooldown driving the Entropic Rift window — unbound; needed for that build. |
| Void Blast | constant | override-covered | Voidweaver's constant filler while Entropic Rift is open (replaces Smite). For Voidweaver builds this is a spam button; the seed provides no explicit slot. |

### Priest — Holy

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Renew | frequent | needs a slot | Frequent instant HoT that feeds Holy Word: Sanctify's cooldown and provides Mastery: Echo of Light top-off — a 'frequent' priority ability left entirely unbound. Combat 1 … |

### Priest — Shadow

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Mind Flay: Insanity | frequent | build-specific | Archon empowered instant filler after Halo. |
| Void Blast | frequent | build-specific | Voidweaver — spends the Entropic Rift window. |
| Void Volley | frequent | override-covered | Frequent short-CD Insanity generator (replaced Void Bolt), HIGH priority to not lose charges — completely unbound in the seed despite three empty shift slots (Combat 10-1 … |

### Rogue — Outlaw

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Ambush | frequent | needs a slot | A rotational builder — the guaranteed stealth/Vanish opener and, in Hidden Opportunity/Audacity builds, a CONSTANT proc-driven builder (priority list flags it 'frequent', … |
| Slice and Dice | cooldown | needs a slot | The self-haste buff maintained in Improved Adrenaline Rush builds ('cooldown' frequency, refreshed periodically). Not bound anywhere; a build-dependent but real maintenan … |
| Coup de Grace | frequent | build-specific | Trickster capstone woven into builder and finisher windows ('frequent') — unbound. It may fire as an automatic empowerment rather than a manual press in the current imple … |

### Rogue — Subtlety

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Coup de Grace | frequent | override-covered | Trickster capstone finisher, listed at 'frequent' and prioritized OVER Eviscerate when up, is not bound to any bucket. On a Trickster build it is a core spammed finisher  … |
| Gloomblade | constant | override-covered | Talent replacement for Backstab (constant single-target builder) is unbound; the seed only placed Backstab on Combat 1. If Gloomblade is talented — common for Sub — key 1 … |

### Shaman — Elemental

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Elemental Blast | frequent | needs a slot | Primary ST Maelstrom spender ('usually the pick' of the Earth Shock choice node) — unbound. The common build has no spender key because only Earth Shock was placed. |
| Fire Elemental | cooldown | needs a slot | ~2.5min burst-pet cooldown, a core DPS CD alongside Stormkeeper/Ascendance — unbound entirely. Should take an open shift slot (Combat 10/11 = S2/S3). |
| Ancestral Swiftness | cooldown | build-specific | Farseer DPS cooldown (~1.5min, instant + haste + summons an ancestor) — unbound; the seed bound the mutually-exclusive Nature's Swiftness instead. Farseer builds want thi … |
| Tempest | frequent | build-specific | Frequent Stormbringer rotational proc-spender (charges from spending Maelstrom, supercharges the next Bolt/CL) — it is completely unbound. A 'frequent'-tier button belong … |
| Voltaic Blaze | frequent | build-specific | Frequent AoE Flame Shock spreader (core in Farseer/M+) — unbound. A 'frequent'-tier rotational button with no key at all. |

### Shaman — Enhancement

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Feral Spirit | cooldown | needs a slot | Major burst-loop cooldown (spirit wolves). Unbound — may be passively granted in the Midnight tree (flagged @verify-ingame); if it remains an active button it needs a shi … |
| Voltaic Blaze | frequent | needs a slot | 'Frequent' builder/Flame Shock refresh (spell 470057) present in the tier-1 APL — the ability that actually maintains the Flame Shock the seed parks on prime key 3, yet i … |
| Tempest | frequent | build-specific | 'Frequent' Stormbringer hero-tree spender (massive nuke replacing a Lightning/Chain cast at 10 stacks). A core spender in the Stormbringer build with no key at all; deser … |
| Ascendance | cooldown | override-covered | ~2-min major burst cooldown (or DRE proc) that REPLACES Doom Winds in that build and enables Windstrike/Thorim's Invocation. Entirely unbound; Combat 10 (S2) is empty and … |
| Primordial Storm | frequent | override-covered | 'Frequent' Totemic hero-tree spender (replaces the lightning nuke in the Totemic loop) — unbound. Central to the raid-preferred Totemic build and needs a real key. |

### Shaman — Restoration

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Downpour | frequent | needs a slot | In the Downpour build this is a frequent burst-AoE spender used before the puddle expires; unbound. Build-conditional, but needed a key if talented. |
| Stormstream Totem | frequent | needs a slot | The apex talent's empowered-HST proc spend (banked by Riptide / Nature's/Ancestral Swiftness) has no key. If specced into the apex, this is an active button pressed when  … |
| Healing Tide Totem | cooldown | build-specific | Totemic's primary raid cooldown is unbound. It is a choice node vs Ascendance, so this is build-conditional — but if you run Totemic instead of Farseer/Ascendance, HTT (n … |
| Surging Totem | frequent | override-covered | Under the Totemic hero build, Surging Totem replaces Healing Rain as the AoE anchor (keep active, reposition via Totemic Projection). The seed binds Healing Rain (Combat  … |

### Warlock — Affliction

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Malefic Grasp | frequent | needs a slot | Listed as a frequent filler channel during every Darkglare window. It transforms from Shadow Bolt in the Darkglare window, but this seed uses Drain Soul as the filler and … |
| Shadow of Nathreza | cooldown | build-specific | The apex spec active and a real part of the meta Darkglare burst (priority: cooldown), but it is bound to no bucket at all. Malevolence (near-dead Hellcaller build) sits  … |
| Shadow Bolt | frequent | override-covered | The alternative Nightfall-proc filler; not bound. Correct to omit IF the Drain Soul filler talent is taken (they are a choice node), but flagged so the build assumption i … |

### Warlock — Demonology

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Dominion of Argus | cooldown | needs a slot | Apex major cooldown that the entire S1 build is constructed around, fired aligned with Summon Demonic Tyrant. The seed binds it nowhere, yet Combat 9-12 (S1-S4) are all e … |

### Warlock — Destruction

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Embers of Nihilam | cooldown | needs a slot | Spec apex active (tree row 12) triggering Echo of Sargeras haste/crit — a cooldown-frequency burst button when talented. Not bound; belongs on a shift/combat-CD key along … |
| Ruination | frequent | build-specific | Diabolist free empowered-nuke proc, listed 'frequent' — a reactive spender that needs a fast unmodified key. Completely absent from the seed; Diabolist players would have … |
| Infernal Bolt | frequent | override-covered | Diabolist Incinerate replacement and the APL shard-refill builder — a 'frequent'/constant press. If playing Diabolist it should own the Combat 1 filler slot; it is bound  … |
| Wither | constant | override-covered | Constant-maintenance DoT and the Hellcaller REPLACEMENT for Immolate — a Hellcaller build needs it on the constant-press key (Combat 3, where Immolate currently sits). No … |

### Warrior — Arms

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Whirlwind | frequent | needs a slot | A 'frequent' AoE spender that consumes Collateral Damage at 3 stacks (and lands a Slam-equivalent on the primary target in the Fervor of Battle build). It is completely u … |
| Ravager | cooldown | build-specific | AoE burst ~45s deployed into Colossus Smash (choice vs Bladestorm). |

### Warrior — Fury

| Ability | Freq | Tag | Note |
|---|---|---|---|
| Thunder Blast | frequent | build-specific | Frequent Mountain Thane press (fire at 2 stacks / during Avatar; extends Avatar and always triggers Lightning Strike). The empowered Thunder Clap has no bucket at all — i … |

## Totals

- **needs a slot** (real bind candidates): 63
- **build-specific** (place + skip-if-unknown): 33
- **override-covered** (bind base, no new key): 22
# BucketBinds Layout v2

> ## ⚠ Half of this document is SHIPPED. Read this box first.
>
> | Section | Status |
> |---|---|
> | §1 The problem | history |
> | **§2 The banding contract** | **SHIPPED v0.10.0** — mirrored in `project-spec.md` |
> | **§3 The key map** | **SHIPPED v0.10.0** — mirrored in `project-spec.md` |
> | §4 Migration summary | §4's eviction list is **pending** (part of §6) |
> | §5 Cross-cutting findings | analysis, still valid |
> | **§6 Per-spec reclassification** | **Demonology done (v0.11.0, floating buckets); 39 specs pending** |
> | §7 Related fixes | **SHIPPED v0.10.0** |
> | §8 Open decisions | 5 of 6 **decided** (§8.6 resolved by floats), struck through below |
> | §9 Implementation checklist | 6 of 11 **done**, ticked below |
> | §10 Grounding quality | analysis — read before acting on §6 |
>
> **The abilities have not moved.** v0.10.0 renamed and re-keyed the bands; every
> spec's abilities still sit in their v1 ordinals. Applying §6 is what actually
> fixes Demonology's Tyrant-on-`2` and its empty Cooldown band.

Authored 2026-07-21 against seed rev "52 buckets / 40 specs / 1538 mappings",
addon v0.9.0, game 12.0.7. §2/§3/§7 shipped the same day as **v0.10.0**
(seed now 58 buckets / 54 placed; 40 specs and 1538 mappings unchanged).

Supersedes nothing yet — read alongside `seed-review.md` (per-spec placement audit),
`seed-edits-proposed.md` (the Tier-A/B correction list) and `unmapped-abilities.md`
(the unbound-ability inventory). Where this doc and those three disagree, this doc is
the newer thinking but the *older* docs carry the citations.

**Provenance:** the per-spec reclassification in §6 was produced by four subagents
reading `knowledge/classes/<class>/<spec>/rotation.md` (all 40 exist) plus, for the
Warlock specs, `diabolist-sequences.md` and the two review docs. That's KB-grounded
but **not in-game verified** — treat every §6 row as a proposal to review, not a
confirmed fact. Confidence: medium. The band *contract* (§2) is the load-bearing
part; individual ability placements are cheap to argue with.

---

## 1. The problem

The bucket ordinals `Combat 1` … `Combat 12` are inherited from Bellular's
spreadsheet and are **semantically empty**. They were never a priority ranking —
they were row numbers. Two consequences compounded:

1. **`Combat 9-12` became a junk drawer.** 38 of 40 specs fill it, and what landed
   there is a mix of genuine burst cooldowns (Avatar, Metamorphosis, Deathmark) and
   things that are not combat abilities at all (Pain Suppression, Guardian Spirit,
   Life Cocoon, Ironbark, Spirit Link Totem, Aura Mastery, Hunter's Mark, Raise Dead).
2. **Two key-layout swaps re-keyed the ordinals without re-auditing them.** The
   2026-07-14 modifier-grouped re-layout and the 2026-07-16 `Q E R F` combat swap both
   edited the `buckets` table only. All 1538 spec→category mappings were silently
   re-keyed. Nobody checked whether "Combat 6" still meant what the new key implied.

The visible symptom that started this: a Demonology warlock found Summon Demonic
Tyrant on `2`, four dead `SHIFT-` keys, and the spec's apex cooldown (Dominion of
Argus) bound nowhere.

### Why the obvious fix is wrong

The tempting fix is to re-key the bands — push `Combat 5-8` to `SHIFT-QERF` and
`Combat 9-12` to `CTRL-QERF`. Scanning what those bands actually hold says don't:

- **`Combat 5-8` is the *more* rotational band.** It holds Death Strike, Execute,
  Ignore Pain, Ironfur, Demon Spikes, Shield Block, Rejuvenation, Regrowth,
  Lifebloom, Swiftmend, Penance, Power Word: Shield, Riptide, Earth Shock, Starsurge,
  Renewing Mist, Fan of Knives. Active mitigation and healer cores. Demoting it to a
  modifier layer is the single most damaging change available.
- **`Combat 9-12` is where the cooldowns already are.** It's already on `SHIFT-QERF`,
  which is the correct tier for a 2-minute button.

**The keys are fine. The labels lie.** So: rename the bands, re-file the abilities,
touch the key map as little as possible.

---

## 2. The banding contract — **SHIPPED v0.10.0**

| Band | Keys | Bar/slots | Contract |
|---|---|---|---|
| **Rotational 1-4** | `Q` `E` `R` `F` | 1 / 1-4 | The four most-pressed buttons. Builders, spenders, core fillers. Ordered by press frequency, most-pressed on `Q`. |
| **Rotational 5-8** | `1` `2` `3` `4` | 1 / 5-8 | Secondary rotation: AoE swaps, active mitigation, maintenance, short-CD (<45s) situational. |
| **Cooldown 1-4** | `SHIFT-Q E R F` | 2 / 1-4 | Major cooldowns ≥45s pressed on CD or inside a burst window. |
| **Overflow 1-6** | `CTRL-R F 1 2 3 4` | 3 / 3-8 | Specs with more real buttons than banded slots (see §8.5). |

Three rules that fall out of the contract:

- **Frequency, not power.** A 30s button pressed twelve times a minute is Rotational
  even if it "feels like" a cooldown (Bestial Wrath, Tiger's Fury, Essence Break,
  Demon Spikes, Empower Rune Weapon). A 45s button held for a window is a Cooldown
  even if it's cheap (Meteor, Volley — though see the exceptions in §6).
- **Externals are not combat abilities.** Single-target and raid-wide defensives cast
  on *other people* belong in `Class 7 (Raid Defensive)`, not in a Cooldown slot.
  They're reactive — they should be on an unmodified key, which §3 provides.
- **Overrides share a key.** Where a talent replaces a spell on the same button
  (Infernal Bolt/Shadow Bolt, Wither/Immolate, Windstrike/Stormstrike, Gloomblade/
  Backstab, Void Blast/Smite), bind the **base** and let the game swap the icon. See
  §7 — this is also an addon bug that was fixed separately.

### Renames

| Old bucket | New bucket |
|---|---|
| `Combat 1` … `Combat 4` | `Rotational 1` … `Rotational 4` |
| `Combat 5` … `Combat 8` | `Rotational 5` … `Rotational 8` |
| `Combat 9` … `Combat 12` | `Cooldown 1` … `Cooldown 4` |
| *(new)* | `Overflow 1` … `Overflow 6` |

This was a seed-wide key rename in `bellular-keybinds.seed.json` (`buckets[].category`
and all 409 affected `specs[].abilities` keys) plus a regen of `Data.lua`. **The rename
is the point** — without it the next editor re-creates the junk drawer. Seed went
52 → 58 buckets (54 placed); no `Combat N` reference remains in hand-written Lua.

---

## 3. The key map — **SHIPPED v0.10.0**

Only bars 4 and 5 move. Bars 1-3 keep the modifier-bar invariant: slot *N* is the
same physical key on every bar, with that bar's modifier.

### Bar 1 — unmod (`ACTIONBUTTON`)

| Slot | Key | Bucket | Change |
|---|---|---|---|
| 1-4 | `Q E R F` | Rotational 1-4 | rename only |
| 5-8 | `1 2 3 4` | Rotational 5-8 | rename only |
| 9 | `Z` | **Class 7 (Raid Defensive)** | ← from `CTRL-3` |
| 10 | `X` | **Self-Heal 1** | ← from key `6` *(v2.1; was Dispel in v2.0)* |
| 11 | `C` | CC | — |
| 12 | `V` | Interrupt | — |

Slots 9/10 were vacated by the 2026-07-17 mouse relocate. Refilling them is **not** a
reversal of that decision: the relocate moved abilities you press *while kiting*.
Purge, dispel and raid-defensives are target-cast reactive presses, so the "hard to
hit while strafing" objection doesn't apply. `Z X C V` becomes a coherent
**react-to-what-just-happened** cluster.

### Bar 2 — Shift (`MULTIACTIONBAR1`)

| Slot | Key | Bucket | Change |
|---|---|---|---|
| 1-4 | `SHIFT-Q E R F` | Cooldown 1-4 | rename only |
| 5 | `SHIFT-1` | Self-Heal 3 (Overflow) | ← from `CTRL-R` |
| 6-8 | `SHIFT-2 3 4` | Class 2/3/4 (CC/Tag/Special) | — |
| 9 | `SHIFT-Z` | **Healthstone/Potion (use)** | ← from key `5` *(v2.1)* |
| 10 | `SHIFT-X` | **Self-Heal 2** | ← from key `7` *(v2.1)* |
| 11 | `SHIFT-C` | CC 2 | — |
| 12 | `SHIFT-V` | Slow | — |

### Bar 3 — Ctrl (`MULTIACTIONBAR2`) — deliberate, never panic

| Slot | Key | Bucket |
|---|---|---|
| 1 | `CTRL-Q` | Focus macro *(prep)*† ← from key `5` |
| 2 | `CTRL-E` | Self-Heal 4 (Overflow) |
| 3-8 | `CTRL-R F 1 2 3 4` | **Overflow 1-6** (per §8.5) |
| 9-11 | `CTRL-Z X C` | PvP 1-3 *(v2.1; Buff/Res moved to the prep band)* |
| 11 | `CTRL-C` | free |
| 12 | `CTRL-V` | Taunt/Quick Access |

Ctrl empties out almost entirely. That's the goal — it's the worst-reach modifier and
should hold only deliberate, out-of-danger presses. The six free slots are where §6's
"Overflow" abilities land.

### Bar 4 — `MULTIACTIONBAR3` ("Right", vertical), top → bottom

| Slot | Key | Bucket |
|---|---|---|
| 1 | `BUTTON3` | Class 1 (Movement) |
| 2 | `BUTTON4` | Movement Ability |
| 3 | `BUTTON5` | Personal Defensive 1 |
| 4 | `5` | **Buff** *(prep band, v2.1)* |
| 5 | `6` | **Mount** *(prep band, v2.1)* |
| 6 | `7` | **Res** *(prep band, v2.1)* |
| 7 | `8` | Trinket Macro |
| 8 | `9` | Racial Ability |
| 9 | `0` | Damage Potion |
| 10-11 | — | Free ×2 (keyless placeholders) |
| 12 | — | unmanaged |

### Bar 5 — `MULTIACTIONBAR4` ("Left", vertical), top → bottom

| Slot | Key | Bucket |
|---|---|---|
| 1 | `SHIFT-BUTTON3` | Immune/Spell Immune/Movement |
| 2 | `SHIFT-BUTTON4` | Movement Ability 2 |
| 3 | `SHIFT-BUTTON5` | Personal Defensive 2 |
| 4 | `ALT-Q` | Flask macro† |
| 5 | `ALT-E` | Buff-food macro† |
| 6 | `ALT-R` | Drinking/Mana Potion Macro |
| 7 | `ALT-F` | Another Combat Item |
| 8-10 | `ALT-Z X C` | **Dispel, Purge, Lust/BRes** *(demoted in v2.1)* |
| 11 | `ALT-V` | free |
| 12 | — | free |

† **Not seed buckets.** The focus, flask and buff-food macros are hardcoded to their
bar+slot in `Macros.lua` (`FOCUS_SLOT = 49`; `PREP.flask = 40`, `PREP.buff = 41`), so
grepping the seed for them finds nothing — by design. Everything else in these tables
*is* a seed bucket. Same caveat for `Trinket Macro` / `Racial Ability`: they are seed
buckets, but their keys (`8`/`9`) are set by both the dump's bind loop and the macro
pass. Bar 3 slot 11 (`CTRL-C`) and bar 4 slot 12 are simply absent from the seed.

Bars 4 and 5 are the two vertical side bars, so slot *N* of each sits side by side.
Rows 1-3 therefore read `M3 / SM3`, `M4 / SM4`, `M5 / SM5` — the mouse cluster lines
up horizontally instead of running bottom-to-top up one bar.

`ALT-1..8` remains the contextual pet/stance bar, bound not placed.

### What this buys

Six reactive buckets come off Ctrl/Alt onto unmodified keys: Healthstone,
Self-Heal 1, Self-Heal 2, Raid Defensive, Dispel, and (to Shift) Purge. Flask and
buff-food — pressed once an hour, out of combat — stop squatting on unmod `8` and `9`.

---

## 4. Migration summary

| | Count |
|---|---|
| Specs re-banded | 40 |
| Abilities evicted from Combat bands entirely | 24 |
| Previously-unbound abilities given a slot | 58 |
| Specs with a genuinely empty Cooldown band | 1 (Hunter BM) |
| Specs that overflow (more buttons than slots) | 7 |

### The eviction list

Everything leaving the Combat bands, with its destination:

| Ability | Spec(s) | → |
|---|---|---|
| Pain Suppression | Priest Disc | Class 7 (Raid Defensive) |
| Power Word: Barrier | Priest Disc | Class 7 |
| Guardian Spirit | Priest Holy | Class 7 |
| Life Cocoon | Monk MW | Class 7 |
| Ironbark | Druid Resto | Class 7 |
| Spirit Link Totem | Shaman Resto | Class 7 |
| Aura Mastery | Paladin Holy | Class 7 |
| Time Dilation | Evoker Pres | Class 7 |
| Hunter's Mark | Hunter ×3 | Class 3 (Tag) |
| Raise Dead | DK ×3 | utility (pre-pull ghoul) |
| Maim | Druid Feral | CC 2 |
| Harpoon | Hunter Surv | Movement Ability |
| Flying Serpent Kick | Monk WW | Movement Ability 2 |
| Blade Rush | Rogue Outlaw | Movement Ability 2 |
| Frost Shock | Shaman Ele/Enh | Slow / movement-instant band |
| Nature's Swiftness | Shaman Enh | Class bucket (off-heal) |
| Lightning Bolt, Lava Burst, Flame Shock, Chain Lightning | Shaman **Resto** | damage-weave band — these held Rotational 1-4 on a healer |
| Wrath, Starfire | Druid **Resto** | Starfire unbind; Wrath → Class 3 or unbanded |
| Azure Strike, Deep Breath | Evoker Pres | drop — absent from the Preservation priority |
| Arcane Explosion | Mage Fire, Mage Frost | drop — not in the 12.0.7 priority |
| Channel Demonfire | Warlock Destro | drop — absent from the simc APL and rotation.md |
| Wild Mushroom | Druid Balance | unbind (Free) |
| Soothing Mist | Monk MW | unbind — displaced by Vivacious Vivification |
| Spinning Crane Kick | Monk BrM | Self-Heal 4 — off the strict priority |

---

## 5. Cross-cutting findings

These are the patterns the 40-spec scan exposed. They matter more than any single
placement.

**The seed is missing core buttons on a majority of specs.** 58 previously-unbound
abilities got a slot in this pass. The worst offenders:

- **DK Unholy** — Death and Decay, the #1 entry in the AoE priority, had no slot at all.
- **Mage Frost** — Glacial Spike, Comet Storm, Icy Veins and Shifting Power all unbound
  despite sitting at the top of the APL. Four of the spec's most-pressed buttons.
- **Priest Shadow** — Void Volley, Void Blast, Power Infusion, Shadowfiend unbound
  while Mind Flay (the terminal filler) held `Combat 1`.
- **Priest Disc** — Ultimate Penitence, Power Infusion, Shadowfiend unbound *while two
  externals occupied Combat slots*.
- **Shaman Resto** — Healing Surge and Healing Stream Totem unbound.
- **Druid Resto** — Efflorescence and Flourish unbound.
- **Paladin Holy** — Divine Toll, the spec's single most important button, absent
  from the seed entirely.
- **DH Devourer** — Collapsing Star, the entire point of a Meta window, unbound.

**Two healers had damage kits in Rotational 1-4.** Resto Shaman (`Lightning Bolt /
Lava Burst / Flame Shock / Chain Lightning`) and Resto Druid (`Wrath / Starfire /
Moonfire / Sunfire`) put their DPS spells on `Q E R F` and their healing kit on the
number row. Both fixed in §6.

**Midnight reworks the seed predates.** Balance's Eclipse is now an activated button,
not a passive state. Brewmaster lost Rising Sun Kick. BM Hunter's Bloodshed and Dire
Beast went passive, leaving the spec with **no offensive cooldown ≥45s at all** — its
Cooldown band is legitimately empty and should be used for trinket/racial/defensive
macros.

**Seven specs overflow.** More real buttons than the 12 banded slots hold. Listed
per-spec in §6; the bar-3 free slots (`CTRL-R F 1 2 3 4`) are the intended landing zone.

---

## 6. Per-spec reclassification — **PENDING (the live work item)**

Format: `key` Ability. `—` = slot intentionally empty. **Was** notes are omitted where
the ability keeps its band.

### Death Knight — Blood
- **Rot 1-4** `Q` Heart Strike · `E` Death Strike *(↑ from 5 — the survival button)* · `R` Blood Boil · `F` Marrowrend
- **Rot 5-8** `1` Death and Decay · `2` Death's Caress · `3` — · `4` —
- **CD 1-4** `S-Q` Dancing Rune Weapon · `S-E` Reaper's Mark *(cast immediately before DRW)* · `S-R` Vampiric Blood *(~60s workhorse, not a panic button)* · `S-F` Consumption
- **Evict** Raise Dead → utility
- **Gaps** Anti-Magic Shell + Icebound Fortitude → Rot 7/8. Gorefiend's Grasp unbound.

### Death Knight — Frost
- **Rot 1-4** `Q` Obliterate · `E` Frost Strike · `R` Howling Blast · `F` Frostscythe
- **Rot 5-8** `1` Glacial Advance · `2` Remorseless Winter · `3` Empower Rune Weapon *(resource valve, pressed several times per Pillar cycle)* · `4` —
- **CD 1-4** `S-Q` Pillar of Frost · `S-E` Breath of Sindragosa · `S-R` Reaper's Mark *(Deathbringer only)* · `S-F` Frostwyrm's Fury
- **Evict** Raise Dead → utility
- **Gaps** Anti-Magic Shell → Rot 8 (the APL uses it proactively as a **Runic Power generator**). Icebound Fortitude, Death Strike unbound.

### Death Knight — Unholy
- **Rot 1-4** `Q` Scourge Strike · `E` Festering Strike · `R` Death Coil · `F` Putrefy
- **Rot 5-8** `1` Epidemic · `2` Outbreak · `3` Soul Reaper *(~6s CD, used well above execute range)* · `4` **Death and Decay** *(NEW)*
- **CD 1-4** `S-Q` Dark Transformation · `S-E` Army of the Dead · `S-R` Summon Gargoyle *(NEW)* · `S-F` Anti-Magic Shell
- **Evict** Raise Dead → utility
- **Gaps** Death and Decay was the #1 AoE entry with **no slot at all**.

### Paladin — Holy
- **Rot 1-4** `Q` Holy Shock · `E` Word of Glory *(↑ from 7 — primary HP spender)* · `R` Judgment · `F` Flash of Light
- **Rot 5-8** `1` Light of Dawn · `2` Holy Light · `3` Shield of the Righteous *(overcap valve)* · `4` Holy Bulwark
- **CD 1-4** `S-Q` Avenging Wrath · `S-E` **Divine Toll** *(NEW)* · `S-R` Holy Prism *(NEW)* · `S-F` Tyr's Deliverance / Beacon of Virtue *(NEW)*
- **Evict** Aura Mastery → Class 7
- **Gaps** Divine Toll was **absent from the seed** and is Herald's most important button. Crusader Strike + Hammer of Wrath still unbound — no rotational room.
- **Overflow** Rotational full at 8.

### Paladin — Protection
- **Rot 1-4** `Q` Blessed Hammer · `E` Shield of the Righteous *(on-GCD spender + mitigation)* · `R` Judgment · `F` Avenger's Shield
- **Rot 5-8** `1` Consecration · `2` Word of Glory · `3` Holy Bulwark · `4` **Hammer of Light** *(NEW — top spend priority in its 12s window)*
- **CD 1-4** `S-Q` Sentinel / Avenging Wrath · `S-E` Divine Toll · `S-R` Ardent Defender *(NEW)* · `S-F` Guardian of Ancient Kings *(NEW)*
- **Gaps** Hammer of Wrath still unbound.
- Ardent Defender / GoAK are **personal tank walls**, not raid externals, so they earn the Cooldown band rather than Class 7.

### Paladin — Retribution
- **Rot 1-4** `Q` Final Verdict · `E` Crusader Strike *(Templar Strike shares)* · `R` Judgment · `F` Blade of Justice
- **Rot 5-8** `1` Divine Storm · `2` **Hammer of Light** *(NEW — jumps the spender queue after Wake of Ashes)* · `3` Hammer of Wrath *(NEW)* · `4` Templar Slash *(NEW, or macro onto Rot 2)*
- **CD 1-4** `S-Q` Avenging Wrath *(skipped on Radiant Glory)* · `S-E` Wake of Ashes · `S-R` Execution Sentence *(cast immediately before WoA)* · `S-F` Divine Toll

### Warrior — Arms
- **Rot 1-4** `Q` Mortal Strike · `E` Overpower *(2 charges — highest raw cast count)* · `R` Execute · `F` Slam
- **Rot 5-8** `1` Cleave · `2` Thunder Clap/Rend · `3` Sweeping Strikes · `4` Ravager *(NEW)*
- **CD 1-4** `S-Q` Colossus Smash *(↓ from Rot 3 — the 45s window everything syncs into)* · `S-E` Avatar · `S-R` Champion's Spear · `S-F` Bladestorm **or** Demolish *(mutually exclusive by hero tree)*
- **Gaps** Heroic Strike, Whirlwind unbound.

### Warrior — Fury
- **Rot 1-4** `Q` Bloodthirst · `E` Rampage *(Enrage upkeep — never let it drop)* · `R` Raging Blow · `F` Execute
- **Rot 5-8** `1` Whirlwind · `2` Thunder Clap/Rend · `3` Odyn's Fury *(45s but tops the Thane list and triggers Enrage)* · `4` **Thunder Blast** *(NEW — Mountain Thane's highest-priority button)*
- **CD 1-4** `S-Q` Recklessness · `S-E` Avatar · `S-R` Bladestorm · `S-F` Champion's Spear
- **Note** the seed had Avatar **and** Bladestorm both on `Combat 9` — a genuine double-booking, split here.
- **Gaps** Storm Bolt, Enraged Regeneration unbound.

### Warrior — Protection
- **Rot 1-4** `Q` Shield Slam · `E` Revenge · `R` Thunder Clap · `F` Execute
- **Rot 5-8** `1` Shield Block · `2` Ignore Pain *(rage-overflow valve)* · `3` Shield Charge · `4` Demoralizing Shout — *on Mountain Thane builds swap Rot 8 → **Thunder Blast***
- **CD 1-4** `S-Q` Avatar · `S-E` Ravager · `S-R` Champion's Spear · `S-F` Demolish *(Colossus only; Thane frees this for Shield Wall / Last Stand)*
- **Overflow** Shield Charge and Demoralizing Shout are both ≥45s but sit in Rotational — they're rage generators woven into the loop, not burst windows. Shield Wall, Last Stand, Spell Reflection, Devastate unbound.

### Evoker — Augmentation
- **Rot 1-4** `Q` Eruption · `E` Ebon Might *(the floor — pandemic-refresh at ~3-4s)* · `R` Prescience *(charges, ~15s)* · `F` Azure Strike
- **Rot 5-8** `1` Living Flame *(Chrono Flame shares)* · `2` Fire Breath · `3` Upheaval · `4` Blistering Scales
- **CD 1-4** `S-Q` Breath of Eons · `S-E` Time Skip · `S-R` **Tip the Scales** *(NEW)* · `S-F` Deep Breath *(NEW)*
- **Evict** Hover → movement/utility, it's off-GCD.

### Evoker — Devastation
- **Rot 1-4** `Q` Disintegrate · `E` Living Flame · `R` Fire Breath · `F` Eternity Surge
- **Rot 5-8** `1` Pyre · `2` Azure Strike *(demoted — lowest-value filler)* · `3` Azure Sweep *(NEW)* · `4` Engulf *(NEW)*
- **CD 1-4** `S-Q` Dragonrage · `S-E` Deep Breath · `S-R` Tip the Scales *(NEW)* · `S-F` — *(use for trinket macro)*
- **Evict** Hover → Movement bucket. Unravel stays unbound (situational).

### Evoker — Preservation
- **Rot 1-4** `Q` Reversion · `E` Echo · `R` **Verdant Embrace** *(NEW)* · `F` **Merithra's Blessing** *(NEW — default Echo finisher)*
- **Rot 5-8** `1` Living Flame · `2` Dream Breath · `3` Temporal Anomaly *("missing casts is the single biggest rotation error")* · `4` **Emerald Blossom** *(NEW)*
- **CD 1-4** `S-Q` Tip the Scales *(NEW)* · `S-E` Dream Flight · `S-R` Stasis *(NEW)* · `S-F` Rewind
- **Evict** Time Dilation → Class 7. Azure Strike, Deep Breath → drop.
- **Overflow** Fire Breath (Chronowarden damage-weave) and Disintegrate (Energy Loop build only) → bar-3 free slots.
- **Note** Rewind stays in-band by exception — the choice node means only 2-3 CDs are ever live.

### Hunter — Beast Mastery
- **Rot 1-4** `Q` Kill Command *(2 charges, ~7.5s)* · `E` Barbed Shot · `R` Cobra Shot · `F` Bestial Wrath *(30s — pressed like a rotational)*
- **Rot 5-8** `1` Wild Thrash · `2` Black Arrow *(Dark Ranger)* · `3` Nature's Ally · `4` Wailing Arrow *(NEW)*
- **CD 1-4** **empty** — see below
- **Evict** Hunter's Mark → Class 3 (Tag)
- **Note** Midnight made Bloodshed and Dire Beast passive. BM has **no offensive cooldown ≥45s**. Give `SHIFT-QERF` to trinket/racial/potion macros or defensives.

### Hunter — Marksmanship
- **Rot 1-4** `Q` Aimed Shot · `E` Arcane Shot · `R` Rapid Fire · `F` Steady Shot *(demoted — pure focus filler)*
- **Rot 5-8** `1` Multi-Shot · `2` Volley *(45s but pressed on CD for Trick Shots)* · `3` Black Arrow / Kill Shot *(mutually exclusive)* · `4` **Moonlight Chakram** *(NEW — Sentinel is the S1 default)*
- **CD 1-4** `S-Q` Trueshot *(becomes Wailing Arrow on Dark Ranger)* · `S-E` Explosive Shot *(NEW)*
- **Evict** Hunter's Mark → Class 3

### Hunter — Survival
- **Rot 1-4** `Q` Kill Command · `E` Raptor Strike *(Raptor Swipe in AoE)* · `R` Wildfire Bomb · `F` Flamefang Pitch
- **Rot 5-8** `1` Boomstick *(60s but explicitly not held for burst)* · `2` Hatchet Toss · `3` **Moonlight Chakram** *(NEW)* · `4` —
- **CD 1-4** `S-Q` Takedown *(the +20% burst anchor)* · `S-E` Aspect of the Eagle
- **Evict** Hunter's Mark → Class 3. Harpoon → Movement Ability *(SV opens with Takedown's charge, so Harpoon is pure gap-closer)*.

### Shaman — Elemental
- **Rot 1-4** `Q` Lightning Bolt · `E` Lava Burst · `R` Earth Shock *(Elemental Blast shares)* · `F` Flame Shock
- **Rot 5-8** `1` Chain Lightning · `2` Earthquake · `3` **Tempest** *(NEW — Stormbringer's proc spender)* · `4` **Voltaic Blaze** *(NEW)*
- **CD 1-4** `S-Q` Ascendance · `S-E` Stormkeeper *(held to pair with Ascendance)* · `S-R` **Fire/Storm Elemental** *(NEW)* · `S-F` Ancestral Swiftness
- **Overflow** Frost Shock → movement-instant/slow band.

### Shaman — Enhancement
- **Rot 1-4** `Q` Stormstrike *(Windstrike overrides in Ascendance)* · `E` Lava Lash · `R` Crash Lightning · `F` Lightning Bolt
- **Rot 5-8** `1` Chain Lightning · `2` **Tempest / Primordial Storm** *(NEW — the hero-tree 10-Maelstrom spender)* · `3` Sundering · `4` **Voltaic Blaze** *(NEW)*
- **CD 1-4** `S-Q` Doom Winds · `S-E` **Ascendance** *(NEW)* · `S-R` Surging Totem · `S-F` **Feral Spirit** *(NEW)*
- **Evict** Nature's Swiftness → Class bucket (it's the instant off-heal). Frost Shock → slow.
- **Overflow** hardcast Flame Shock loses its slot — Voltaic Blaze applies it and hardcast is last-resort filler.

### Shaman — Restoration
- **Rot 1-4** `Q` Riptide · `E` Chain Heal · `R` Healing Wave · `F` **Healing Surge** *(NEW)*
- **Rot 5-8** `1` **Healing Stream Totem** *(NEW)* · `2` Surging Totem / Healing Rain · `3` Unleash Life · `4` **Downpour** *(NEW)*
- **CD 1-4** `S-Q` **Healing Tide Totem** *(NEW — Totemic's raid CD, had no slot)* · `S-E` Ascendance · `S-R` Nature's/Ancestral Swiftness · `S-F` —
- **Evict** Spirit Link Totem → Class 7. **Lightning Bolt / Lava Burst / Flame Shock / Chain Lightning → damage-weave band** — these held Rotational 1-4 on a healer.
- **Gaps** Earth Shield still unplaced (pre-combat maintenance).

### Demon Hunter — Devourer
- **Rot 1-4** `Q` Consume · `E` Void Ray · `R` Reap *(becomes Eradicate after a full Void Ray)* · `F` **Collapsing Star** *(NEW — the entire point of a Meta window, had no binding)*
- **Rot 5-8** `1` Soul Immolation · `2` **Cull / Eradicate** *(NEW)* · `3` Voidblade · `4` Vengeful Retreat *(kept rotational — Voidstep-buffed VR opens the Void-Scarred combo)*
- **CD 1-4** `S-Q` Void Metamorphosis *(fragment-gated, not on a timer)* · `S-E` The Hunt · `S-R` Devour · `S-F` Pierce the Veil

### Demon Hunter — Havoc
- **Rot 1-4** `Q` Chaos Strike *(→ Annihilation in demon form)* · `E` Blade Dance *(→ Death Sweep)* · `R` Eye Beam · `F` Immolation Aura
- **Rot 5-8** `1` Felblade · `2` Vengeful Retreat *(pressed before every Eye Beam for Initiative/Inertia)* · `3` Essence Break *(~40s — under the threshold)* · `4` **Throw Glaive** *(NEW — becomes Reaver's Glaive on Aldrachi Reaver, whose whole loop starts there)*
- **CD 1-4** `S-Q` Metamorphosis · `S-E` The Hunt · `S-R` Fel Barrage *(NEW)* · `S-F` —
- **Gaps** Fel Rush → Movement Ability (Inertia backup consumer).

### Demon Hunter — Vengeance
- **Rot 1-4** `Q` Fracture · `E` Soul Cleave · `R` Spirit Bomb · `F` Immolation Aura
- **Rot 5-8** `1` Demon Spikes *(off-GCD, ~100% uptime target)* · `2` Sigil of Flame · `3` Felblade · `4` Vengeful Retreat *(resets Felblade via Unhindered Assault)*
- **CD 1-4** `S-Q` Metamorphosis · `S-E` Fel Devastation · `S-R` Soul Carver · `S-F` Sigil of Spite
- **Note** Fiery Brand is a genuine offensive CD (opens the Fiery Demise window Soul Carver/Fel Dev line into) but is already on Personal Defensive 1 and no CD slot is free. Leave it; treat that key as rotational.

### Druid — Balance
- **Rot 1-4** `Q` Wrath · `E` Starfire · `R` Starsurge · `F` **Eclipse (Solar/Lunar)** *(Midnight rework — Eclipse is now an activated charged button armed by your last builder, pressed every cycle)*
- **Rot 5-8** `1` Starfall · `2` Moonfire · `3` Sunfire · `4` **Moon chain (New/Half/Full)** *(NEW)*
- **CD 1-4** `S-Q` Celestial Alignment / Incarnation · `S-E` Convoke the Spirits · `S-R` Force of Nature *(fired the GCD before CA so Treants overlap)* · `S-F` Fury of Elune
- **Evict** Wild Mushroom → unbind (#11-12 in every list, talent-optional).

### Druid — Feral
- **Rot 1-4** `Q` Shred · `E` Rake · `R` Rip · `F` Ferocious Bite *(also the Ravage/Apex Predator proc button)*
- **Rot 5-8** `1` Tiger's Fury *(30s snapshot anchor)* · `2` Swipe · `3` Primal Wrath · `4` Moonfire *(Lunar Inspiration)*
- **CD 1-4** `S-Q` Berserk / Incarnation · `S-E` Convoke the Spirits · `S-R` Feral Frenzy · `S-F` — *(Feral genuinely has only three ≥45s presses)*
- **Evict** Maim → CC 2 *(it's a finisher-cost stun, not a damage spender)*.

### Druid — Guardian
- **Rot 1-4** `Q` Mangle · `E` Thrash *(feeds Lunar Beam CDR + Sundering Roar)* · `R` Maul / Raze *(macro both)* · `F` Moonfire *(real filler under Elune's Chosen, the S1 M+ default)*
- **Rot 5-8** `1` Ironfur *(off-GCD active mitigation)* · `2` Frenzied Regeneration *(pressed **before** incoming damage)* · `3` Swipe · `4` Sundering Roar
- **CD 1-4** `S-Q` Berserk / Incarnation · `S-E` Lunar Beam · `S-R` Convoke the Spirits · `S-F` **Wild Guardian** *(NEW — the Midnight capstone active, spell 1269614, absent from the seed entirely)*
- **Overflow** Bristling Fur → Self-Heal 2 (empty for Guardian; it's a "take damage, get rage" reactive press).

### Druid — Restoration
- **Rot 1-4** `Q` Rejuvenation *(the Abundance bed)* · `E` Regrowth · `R` Swiftmend · `F` Wild Growth
- **Rot 5-8** `1` Lifebloom · `2` **Efflorescence** *(NEW — core maintenance, missing entirely)* · `3` Moonfire · `4` Sunfire
- **CD 1-4** `S-Q` Incarnation: Tree of Life · `S-E` **Convoke the Spirits** *(NEW as a healer CD)* · `S-R` Tranquility · `S-F` **Flourish** *(NEW)*
- **Evict** Ironbark → Class 7 *(that bucket is empty for Resto)*. Starfire → unbind (Balance copy-paste).
- **Overflow** Wrath → Class 3 (Tag) or unbanded.

### Monk — Brewmaster
- **Rot 1-4** `Q` Keg Smash *("never miss a Keg Smash")* · `E` Tiger Palm · `R` Blackout Kick · `F` Breath of Fire
- **Rot 5-8** `1` Purifying Brew *(timed off the Stagger pool, not spammed)* · `2` Celestial Brew / Celestial Infusion · `3` Chi Burst *(real rotational under Master of Harmony)* · `4` Rushing Jade Wind
- **CD 1-4** `S-Q` Invoke Niuzao · `S-E` Exploding Keg · `S-R` **Black Ox Brew** *(was buried on Self-Heal 4)* · `S-F` **Empty the Cellar** *(NEW)*
- **Overflow** Spinning Crane Kick → Self-Heal 4 (off the strict priority — no mitigation).
- **Note** Rising Sun Kick is **gone** from Brewmaster in Midnight. Don't re-add it.

### Monk — Mistweaver
KB treats **Fistweaving** as the current build, so the damage kit legitimately holds rotational slots — but Renewing Mist and Vivify are pulled up alongside it.
- **Rot 1-4** `Q` Tiger Palm · `E` Blackout Kick · `R` Rising Sun Kick / Rushing Wind Kick · `F` Renewing Mist *(most-pressed heal)*
- **Rot 5-8** `1` **Vivify** *(↑ from Self-Heal 2 — it's the primary reactive heal, not a personal)* · `2` Enveloping Mist · `3` Spinning Crane Kick · `4` **Thunder Focus Tea** *(↑ from Self-Heal 1 — off-GCD, pressed on its 30s CD)*
- **CD 1-4** `S-Q` Invoke Chi-Ji / Yu'lon · `S-E` Celestial Conduit · `S-R` Revival *(kept in-band — only three true majors exist and its dispel is time-critical)* · `S-F` **Mana Tea** *(↑ from Self-Heal 4)*
- **Evict** Life Cocoon → Class 7; Diffuse Magic → Personal Defensive 2 (empty). Soothing Mist → unbind.
- **Overflow** Sheilun's Gift → the freed Self-Heal 1 key.

### Monk — Windwalker
- **Rot 1-4** `Q` Tiger Palm · `E` Blackout Kick · `R` Rising Sun Kick · `F` Fists of Fury
- **Rot 5-8** `1` Spinning Crane Kick · `2` Whirling Dragon Punch · `3` Strike of the Windlord · `4` **Rushing Wind Kick** *(NEW — sits above RSK in the APL)*
- **CD 1-4** `S-Q` Invoke Xuen · `S-E` Zenith *(↓ from Rot — it's the primary flexible cooldown)* · `S-R` **Celestial Conduit** *(NEW)* · `S-F` **Touch of Death** *(↑ from Class 4)*
- **Evict** Flying Serpent Kick → Movement Ability 2.
- **Overflow** Zenith Stomp, Slicing Winds → freed Class 4 / Self-Heal 3 keys.

### Rogue — Assassination
- **Rot 1-4** `Q` Mutilate · `E` Envenom · `R` Rupture · `F` Garrote
- **Rot 5-8** `1` Fan of Knives · `2` Crimson Tempest · `3` **Slice and Dice** *(NEW — a straight omission)* · `4` Ambush
- **CD 1-4** `S-Q` Deathmark · `S-E` Kingsbane *(↓ from Rot — 1min, synced into Deathmark)* · `S-R` **Vanish** *(↑ from Class 4 — re-applies Improved Garrote into the burst window)* · `S-F` —
- **Note** Shiv stays on Class 5 (Purge); for Deathstalker it's also a 6-CP Darkest Night press, so treat that key as rotational. Thistle Tea stays on Self-Heal 2.

### Rogue — Outlaw
- **Rot 1-4** `Q` Sinister Strike · `E` Dispatch · `R` Pistol Shot *(Fan the Hammer makes this very high frequency)* · `F` Between The Eyes
- **Rot 5-8** `1` Roll the Bones · `2` **Slice and Dice** *(NEW)* · `3` Blade Flurry · `4` **Coup de Grace** *(NEW — Trickster is the S1 hero tree and this is in both its lists)*
- **CD 1-4** `S-Q` Adrenaline Rush · `S-E` Killing Spree · `S-R` Keep It Rolling · `S-F` Preparation
- **Overflow** Blade Rush → Movement Ability 2 (functions as a charge as much as a damage press).

### Rogue — Subtlety
- **Rot 1-4** `Q` Backstab *(Gloomblade overrides)* · `E` Shadowstrike · `R` Eviscerate · `F` Shuriken Storm
- **Rot 5-8** `1` Secret Technique *(45s but gated to every Dance)* · `2` Black Powder · `3` Goremaw's Bite · `4` **Coup de Grace** *(NEW)*
- **CD 1-4** `S-Q` Shadow Dance · `S-E` Shadow Blades · `S-R` **Vanish** *(NEW — used offensively for a second Shadowstrike/Find Weakness)* · `S-F` Thistle Tea
- **Gaps** Slice and Dice → a Buff/maintenance bucket, not a Combat slot.

### Mage — Arcane
- **Rot 1-4** `Q` Arcane Blast · `E` Arcane Barrage · `R` Arcane Orb *(outranks Missiles on the meta Spellslinger build)* · `F` Arcane Missiles
- **Rot 5-8** `1` Arcane Pulse · `2` Presence of Mind *(off-GCD rotational charge-rebuild)* · `3` Mirror Image *(NEW)* · `4` —
- **CD 1-4** `S-Q` Touch of the Magi *(the Miniburn — never delayed)* · `S-E` Arcane Surge · `S-R` Evocation · `S-F` **Shifting Power** *(NEW)*
- **Note** Arcane Explosion left out — niche 4+ filler only when Impetus is untalented.

### Mage — Fire
- **Rot 1-4** `Q` Fireball *(Frostfire Bolt overrides)* · `E` Fire Blast *(off-GCD, pressed mid-cast every Heating Up — needs the fastest key)* · `R` Pyroblast · `F` Scorch
- **Rot 5-8** `1` Flamestrike · `2-4` —
- **CD 1-4** `S-Q` Combustion · `S-E` Meteor *(timed to land inside Combustion)* · `S-R` **Shifting Power** *(NEW)* · `S-F` —
- **Evict** Arcane Explosion → drop.
- **Gaps** Alter Time → Personal Defensive, not a Combat slot.

### Mage — Frost
- **Rot 1-4** `Q` Frostbolt · `E` Ice Lance · `R` Flurry · `F` **Glacial Spike** *(NEW — on cooldown, always; a top-priority press with no bind)*
- **Rot 5-8** `1` **Comet Storm** *(NEW — leads the Spellslinger priority)* · `2` Blizzard · `3` **Cone of Cold** *(NEW)* · `4` **Ice Nova** *(NEW)*
- **CD 1-4** `S-Q` Frozen Orb · `S-E` **Icy Veins** *(NEW)* · `S-R` Ray of Frost · `S-F` **Shifting Power** *(NEW)*
- **Evict** Arcane Explosion → drop.
- **The worst seed gap found.** Four top-of-APL buttons were unbound. Summon Water Elemental → pet/Buff bucket.

### Priest — Discipline
- **Rot 1-4** `Q` Penance *(pressed both offensively and defensively — the most-used button)* · `E` Smite *(Void Blast overrides in the Rift)* · `R` Mind Blast · `F` Power Word: Shield *(↑ from 7 — constant Atonement applier)*
- **Rot 5-8** `1` Flash Heal · `2` Power Word: Radiance · `3` Shadow Word: Pain *(Purge the Wicked overrides)* · `4` Shadow Word: Death
- **CD 1-4** `S-Q` Evangelism · `S-E` **Ultimate Penitence** *(NEW — 4min, cast **on enemies** during a ramp)* · `S-R` **Power Infusion** *(NEW)* · `S-F` **Shadowfiend / Mindbender** *(NEW)*
- **Evict** Pain Suppression → Class 7. Power Word: Barrier → Class 7.
- **Note** three throughput cooldowns were unbound *while two externals sat in Combat slots*. Shadow Mend → a heal bucket.

### Priest — Holy
- **Rot 1-4** `Q` Flash Heal · `E` Holy Word: Serenity *(fire before it banks a 2nd charge)* · `R` Prayer of Mending *(the Oracle engine)* · `F` Prayer of Healing
- **Rot 5-8** `1` Holy Word: Sanctify · `2` Renew · `3` Halo *(40s Archon CD, used liberally)* · `4` **Holy Fire** *(NEW — the damage/AoE engine and Empyreal Blaze payoff)*
- **CD 1-4** `S-Q` Apotheosis · `S-E` Divine Hymn *(**exception** — a planned healing channel lined up before burst, not a reactive external, so it earns the band)* · `S-R` **Power Infusion** *(NEW)* · `S-F` **Symbol of Hope** *(NEW)*
- **Evict** Guardian Spirit → Class 7.
- **Overflow** four don't fit: **Holy Word: Chastise** (30s, leads the damage priority — highest priority of the four), **Smite**, **Holy Nova** (only replaces Smite at 4+), **Circle of Healing** (only if talented — drop Renew from Rot 6 on a Circle build). → bar-3 free slots.

### Priest — Shadow
- **Rot 1-4** `Q` Shadow Word: Madness · `E` Mind Blast · `R` **Void Volley** *(NEW — high-priority Insanity generator with charges)* · `F` Shadow Word: Pain
- **Rot 5-8** `1` **Void Blast** *(NEW — spends the Entropic Rift window)* · `2` Tentacle Slam · `3` Shadow Word: Death · `4` Vampiric Touch
- **CD 1-4** `S-Q` Voidform · `S-E` **Power Infusion** *(NEW)* · `S-R` Void Torrent / Halo *(build-exclusive)* · `S-F` **Shadowfiend / Mindbender** *(NEW)*
- **Overflow** **Mind Flay** (was `Combat 1`!) loses its slot — it's the terminal filler. Give it a bar-3 key. On an **Archon** build it becomes Mind Flay: Insanity and is pressed far more — swap it into Rot 5 in place of Void Blast (Voidweaver-only).

### Warlock — Affliction
- **Rot 1-4** `Q` Unstable Affliction · `E` Drain Soul · `R` Agony · `F` Haunt *(15s CD, pressed on cooldown)*
- **Rot 5-8** `1` Corruption · `2` Seed of Corruption · `3` **Shadow Bolt** *(NEW — the on-the-move filler; becomes **Malefic Grasp** inside Darkglare, which fixes the "no Darkglare-window filler key" gap)* · `4` —
- **CD 1-4** `S-Q` Summon Darkglare · `S-E` Dark Harvest *(cast **before** Darkglare — the APL gates on it)* · `S-R` **Shadow of Nathreza** *(NEW — apex active, bound nowhere)* · `S-F` Malevolence *(Hellcaller only; leave empty on the Soul Harvester meta build)*

### Warlock — Demonology
- **Rot 1-4** `Q` Hand of Gul'dan *(↑ from 3 — Tyrant-window press count is the spec's top DPS lever)* · `E` Demonbolt · `R` **Infernal Bolt** *(relabel — Demoniac replaces Shadow Bolt; same button, stale seed name)* · `F` Call Dreadstalkers *(timed to land just before Tyrant)*
- **Rot 5-8** `1` Implosion · `2` **Power Siphon** *(NEW — leads the APL)* · `3` **Ruination** *(NEW — Diabolist burst proc, reactive, needs an unmodified key)* · `4` —
- **CD 1-4** `S-Q` Summon Demonic Tyrant · `S-E` **Dominion of Argus** *(NEW — the headline fix; apex CD the S1 build is built around, deliberately adjacent to Tyrant)* · `S-R` Summon Doomguard · `S-F` Grimoire: Fel Ravager *(Imp Lord is the AoE override of the same key)*
- **Outside the Combat bands** `Interrupt` must change from Spell Lock → **Axe Toss (Command Demon)** — Demo runs the Felguard, so the bound Spell Lock does nothing.

### Warlock — Destruction
- **Rot 1-4** `Q` Incinerate · `E` Chaos Bolt · `R` Conflagrate · `F` Immolate *(**Wither** overrides the same button on Hellcaller — fixes the missing-Wither gap with no new key)*
- **Rot 5-8** `1` Shadowburn · `2` Soul Fire *(↑ from 8 — sits at #1 in the Diabolist ST list)* · `3` Rain of Fire · `4` **Ruination** *(NEW — free empowered nuke proc, listed 'frequent')*
- **CD 1-4** `S-Q` Summon Infernal · `S-E` Malevolence *(does **not** align with Infernal)* · `S-R` **Embers of Nihilam** *(NEW — apex active)* · `S-F` Havoc *(30s cleave setup, a pre-spender press)*
- **Evict** Channel Demonfire → drop (absent from the 12.0.7 simc APL and rotation.md).
- **Overflow** the most overloaded spec. **Infernal Bolt** (distinct APL shard-refill step) → a bar-3 key next to Incinerate. **Cataclysm** → a slower utility key (talent-gated, used between packs).

---

## 7. Related fixes already made

Two bugs found while diagnosing the Demonology dump that started this. **Both are
released** — the `Dump.lua` fix in addon **v0.10.0**, the `charstate` fix in the wow
repo:

1. **`Dump.lua` placed override spells.** `resolveSpellID` used
   `C_Spell.GetSpellInfo(name)`, which follows whatever override is live *at that
   instant*. Dumping while Grimoire: Fel Ravager was on cooldown baked **Devour Magic**
   onto the key; dumping with the Diabolist Pit Lord art armed baked **Ruination** onto
   Hand of Gul'dan's key. Fixed by folding `normID` (`FindBaseSpellByID`) into
   `resolveSpellID` so placement always uses the base spell and the game re-applies the
   override on the button itself. This is what §2's "overrides share a key" rule
   depends on.
2. **`wowkb.charstate` couldn't parse numeric table keys.** `[11] = 30283` in a
   SavedVariables file crashed the parser, which broke `wowkb.diagnostics` entirely.
   One-character fix in `_number`'s terminator set.

---

## 8. Open decisions — **5 of 6 decided (§8.6 resolved by floats, v0.11.0)**

Struck-through items are decided and shipped. Only §8.3 (healer dispel key)
remains, and it's a play-testing question, not a blocker.

1. ~~**Is the `Z`/`X` refill acceptable?**~~ **DECIDED: yes, refilled.** Raid
   Defensive → `Z`, Dispel → `X`. Rationale kept for the record: The 2026-07-17 mouse relocate deliberately
   vacated them. §3 argues purge/dispel/raid-def are a different category from
   movement+defensives, but it *is* re-litigating a three-day-old decision.
2. ~~**Is splitting the number row across two bars acceptable?**~~ **DECIDED:
   accepted.** `1 2 3 4` on bar 1 and
   `5`-`0` on bar 4 means the physical number row spans two on-screen bars. Functionally
   irrelevant, visually incoherent. Edit Mode can place them adjacently.
3. **Healer Dispel on unmod `X` — enough?** *(still open — resolved for now by
   decision 1, revisit if a healer complains.)* For a healer, dispel is among the most
   reactive presses in the game. `X` is better than `CTRL-2` but is not a premium key.
   No premium key is free.
4. ~~**Do we rename the buckets, or just re-file the abilities?**~~ **DECIDED:
   renamed.** `Rotational 1-8` / `Cooldown 1-4` / `Overflow 1-6` shipped in v0.10.0. Re-filing alone gets
   the immediate win. The rename is what stops the junk drawer from re-forming. It's
   also the bigger diff and touches `Dump.lua`/`Macros.lua`.
5. ~~**Overflow policy.**~~ **DECIDED: a named `Overflow 1-6` band** on
   `CTRL-R F 1 2 3 4`, shipped in v0.10.0. Original framing: Seven specs have more buttons than slots. Current proposal
   scatters them onto bar-3 free keys ad hoc. A named `Overflow 1-6` band on
   `CTRL-R F 1 2 3 4` would be more honest.
6. ~~**Build-conditional bindings.**~~ **RESOLVED by floating buckets (v0.11.0).**
   Several rows are "X on Hellcaller, Y on Diabolist" (Havoc/Demolish on Warrior,
   Void Blast/Mind Flay on Shadow, Thunder Blast on Prot Warrior, Circle of Healing
   on Holy, and the Grimoire: Imp Lord / Fel Ravager pair on Demonology). The seed
   had no concept of build variants. **Floats dissolve this:** a band gets a
   priority-ordered candidate list, and at dump time only the *talented* names
   resolve and get placed, so both sides of a choice node can be listed and exactly
   one lands — no per-spec variant authoring. See the band contract in
   `project-spec.md` and the floats block in the seed (Demonology is the pilot).

---

## 9. Implementation checklist

Ordered so each step is independently shippable.

- [x] **Release the override fix** — shipped inside **v0.10.0** rather than a separate
      v0.9.1 (the layout work landed the same day). Released + `ghaddons update`d.
- [x] Decide §8.1-8.6 — **4 of 6 decided**; §8.3 and §8.6 remain, and both are §6
      problems rather than layout problems.
- [x] Bar 4/5 re-layout in `buckets[]` (mouse rows + `5`-`0` row).
- [x] Move the prep-band + Trinket/Racial bindings in `Macros.lua` to match. (These
      are **hardcoded to bar/slot in code**, not seed-driven — `FOCUS_SLOT`,
      `ITEM_SLOTS`/`ITEM_CMDS`/`ITEM_KEYS`, `PREP`.)
- [x] ~~Add a `0` token to `normKey`~~ — **not needed.** `MODIFIER` only claims
      `S`/`C`/`A`, so a bare `0` falls straight through unchanged. Verified by reading
      `normKey`; no code change made.
- [x] Reactive moves: Healthstone, Self-Heal 1/2, Raid Defensive, Dispel, Purge.
- [x] Bucket rename `Combat N` → `Rotational N` / `Cooldown N` (seed + `Dump.lua` +
      `Macros.lua`). No `Combat N` references remain in hand-written Lua.
- [~] Apply §6 per-spec re-filing. **Demonology done (v0.11.0)** — restructured to
      fixed core + a `floats` block (the pilot for floating buckets), which is also
      how §8.6's build-conditional problem got solved. The other 39 specs are the
      follow-on fan-out (`.claude/workflows/spec-keybind-review.js`), now cheaper
      because each spec produces a priority list, not a 12-slot assignment.
- [x] `python3 tool/gen_data_lua.py`, diff `Data.lua`, luaparser-check. (`--check`
      reports in sync; luaparser clean.)
- [ ] `uv run python tool/check_seed_spells.py` against a fresh `SpellName` dump — the
      58 ability names §6 *adds* have never been name-checked. Expect misses. (Run
      post-rename on 2026-07-21 against `SpellName-12.0.7.68256.csv`: 642 distinct
      names, only the two documented-benign misses `Poisons` + `Res`. Re-run **after**
      §6 lands, when the new names actually arrive.)
- [~] Re-run `/bb dump` + `/bb diagnostics` + `/reload` per spec, read back with
      `uv run python -m wowkb.diagnostics`. **Demonology verified in-game (2026-07-21,
      v0.11.0):** float dump lands the talented candidates in the empty
      Rotational/Cooldown slots and the Grimoire churn test passes (only the one
      Grimoire slot changes on respec). Remaining 39 specs pending.
- [x] Update `project-spec.md`'s layout tables — **done 2026-07-21**, rewritten to v2
      with the v1 combat-key-swap and mouse-relocate history demoted to `### History`
      subsections. Also registered the project in the root `CLAUDE.md`, deduped the
      milestone list (M4/M5 each appeared twice), and renamed the dead `wwt-keyboard`
      workspace references to `wow`.

---

## 10. Grounding quality — how much to trust §6

Audit run 2026-07-21 over all 40 `knowledge/classes/<class>/<spec>/rotation.md`.

**Freshness is fine.** All 40 are `patch: 12.0.7` (live), `reviewed:` 07-11 to 07-14.
Nothing is patch-stale. But 34 of 40 carry the *same* `reviewed: 2026-07-11` stamp —
that's one batch sweep, not 40 independent research passes. Only five files were
touched since: `warlock/{affliction,demonology,destruction}` and
`demon-hunter/{devourer,vengeance}` (07-14). **DH Havoc is not among them.**

**Sourcing is the weakness.**

| | Count |
|---|---|
| Cite a SimulationCraft APL URL | 17 / 40 |
| Pin that APL to a commit SHA | **0 / 40** |
| Tier-3 only (Icy Veins / method.gg / maxroll) | 23 / 40 |
| `confidence: high` / `medium` | 23 / 17 |

`raw/simc/` holds **zero** captures, and no file carries a SHA — so none came through
`wowkb.simc` (which pins SHA+date by design). The Tier-1 APL layer this repo prefers
is effectively absent; the GitHub links that exist are bare.

Several files admit it. Mistweaver: *"No SimulationCraft APL exists for this spec."*
Holy Priest: *"simc ships no `MID1_Priest_Holy`."* Demonology's own note says its
priority is Icy Veins + method.gg, not a Tier-1 APL, and that method.gg's `/abilities`
and `/rotation` subpages 404 — so its cast times and shard costs are approximate.

### The twelve weak specs

Both Tier-3-only **and** `confidence: medium`:

`demon-hunter/devourer` · `druid/restoration` · `evoker/augmentation` ·
`evoker/preservation` · `hunter/beast-mastery` · `hunter/survival` ·
`monk/mistweaver` · `paladin/holy` · `priest/discipline` · `priest/holy` ·
`rogue/subtlety` · `shaman/restoration`

**Seven of the twelve are healers, and that is structural** — simc ships no healer
APLs at all, so no healer spec can *ever* get Tier-1 grounding by that route. The only
real frequency evidence available for healers is Tier-2 WarcraftLogs
(`wowkb.wcl casts`), which nothing here has used.

### Why this matters for §6 specifically

The weak specs correlate almost exactly with where §6 made its **largest structural
changes**: it evicted 8 healer externals, completely reordered Rotational 1-4 on
Resto Shaman and Resto Druid, claimed Divine Toll is absent on Holy Paladin, and
re-filed Vivify / Thunder Focus Tea / Mana Tea on Mistweaver — the spec whose own
doc says no APL exists.

**Treat §6 rows in two tiers:**

- **Act on** the DPS/tank findings backed by `high` + a simc citation, plus anything
  structural that needs no sourcing at all: Mage Frost's four unbound APL-top buttons,
  DK Unholy's missing Death and Decay, Fury Warrior's Avatar/Bladestorm double-booking
  on `Combat 9`, Demonology's unbound Dominion of Argus.
- **Hold** every healer row pending better evidence. Healer keybinds are where being
  wrong gets people killed, and they rest on the thinnest sourcing in the KB.

Three ways forward, increasing cost: ship the 33 DPS/tank specs and leave healers on
v1; re-source the 12 weak specs (`wowkb.simc` where simc covers them, `wowkb.wcl casts`
for the healers); or accept medium confidence and mark the healer rows provisional,
verifying in-game as you play them.

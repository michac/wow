---
title: Demonology Warlock — M+ & Delve builds (talents / loadouts)  (Midnight 12.1)
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - ../../../_meta/patch-notes/12.1.md  # tier 1 VERBATIM archive — the Demo + Diabolist tuning below (CLASSES ▶ WARLOCK, l.1197-1207)
  - https://worldofwarcraft.com/en-us/news/24293281  # tier 1, "Curse of Ula'tek" Content Update Notes (12.1, 2026-08-11)
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-spec-builds-talents  # tier 3, upd. 2026-08-10 for 12.1 — post-nerf hero-tree split + both import strings
  - ./talents.md  # tier 1, generated from Blizzard Game Data API + wago Trait* DB2 @ 12.1.0.68914 — the talent-existence floor
  - ./ability-inventory.md  # tier 1, generated from wago DB2 + Blizzard /data/wow/spell @ 12.1.0.69214 — live 12.1 tooltips
  - simc midnight branch profiles/MID1/MID1_Warlock_Demonology.simc  # tier 1 APL, commit 48103ef 2026-05-18 — ⚠ PRE-12.1, awaiting re-pull
  - https://murlok.io/warlock/demonology/diabolist/m+  # tier 2 top-player aggregation, fetched 2026-06-13 — ⚠ SEASON 1 data
  - https://www.wowhead.com/guide/classes/warlock/demonology/talent-builds-pve-dps  # NotWarlock, upd. 2026-03-30 — stale
  - https://www.method.gg/guides/demonology-warlock/talents
  - https://www.kalamazi.gg/guides/demonology
confidence: medium
---

# Demonology — M+ & Delve builds (12.1 "Curse of Ula'tek")

> **Talents / loadouts / hero-tree only.** Stat priority, trinkets, tier set,
> enchants/gems/consumables now live in `gearing.md`. Rotation is in
> `rotation.md` (Tier-1 APL-distilled).
>
> **Season state (2026-08-11):** 12.1 is live but **Midnight Season 2 does not
> open until 2026-08-18** — this is the pre-season week. Nothing below is
> season-gated, but the Tier-2 murlok top-player aggregation cited here is
> **Season 1 data** and will not re-populate until keys start dropping.

## What 12.1 changed for Demonology builds

**Tier-1 (patch notes, the floor — do not let a guide overwrite these):**

| Change | Direction |
|---|---|
| Shadow Bolt damage | **+45%** |
| Demonbolt damage | **+55%** |
| Summon Gloomhound damage | **+35%** |
| Diabolist: Chaos Salvo / Felseeker / Wicked Cleave / Eye Explosion | **−20% each** |
| Diabolist: Flames of Xoroth | **+3%** Fire and demon damage (was 4%) |
| Warlock-wide: Drain Life health drain | **+25%** |
| Warlock-wide: Summon Demonic Gateway | now **Utility by default** in the Cooldown Manager |

**The shape of it:** Demo's *filler* got a large buff and *Diabolist's demon
payload* got cut. That is a deliberate re-weighting away from the Tyrant-window
burst tree and toward sustained casting — it does **not** change which talents
exist (the generated `talents.md` @ `12.1.0.68914` shows **no Demo node added,
removed or moved** in 12.1, unlike Affliction and both DH specs), but it moves
the hero-tree verdict. See below.

**Soul Leech correctness pass (Warlock-wide, matters most to Demo).** A long
list of pet abilities now **correctly grant Soul Leech** that previously did
not: Wild Imp / Imp Gang Boss **Fel Firebolt**, Imp Lord's **Greater Felbolt**,
Demonic Tyrant's **Demonfire**, Vilefiend's **Headbutt** and **Bile Spit**, and
Gloomhound's **Gloom Slash**. Demonology's damage is overwhelmingly pet damage,
so this is a real, passive increase in Soul Leech absorb uptime for this spec
specifically — it makes the class-tree Soul Leech pick meaningfully better than
its 12.0 value, most noticeably in delves. (Going the other way class-wide, three
abilities that erroneously granted it no longer do: **Legion Strike**, **Cunning
Cruelty** and **Channel Demonfire** — the last is Destro-facing and does not touch
Demo, but the reversal list is those three, not two.)

⚠ **Soul Leech was re-issued a new spell ID in 12.1: `108370` → `1311653`.** The
class-tree node itself is untouched (still position 2,4, still a 1-rank passive,
same prereqs) — this is an ID change, not a talent change, so it does not affect
any import string below. It *does* matter to anything that hardcodes the old ID:
WeakAuras, CDM/Cooldown-Manager entries and addon spell tables keyed on `108370`
will silently stop matching. Per the generated `talents.md` @ `12.1.0.68914`.

**Global 12.1 changes that land on this spec** (they sit in the CLASSES preamble
above the per-class lists and apply to every spec):

- **Player health and creature damage both +25% at max level**, with health
  consumables rescaled and some DPS/Tank healing + absorb retuned. Delve and
  solo pulls hit harder in absolute terms; the survivability levers below still
  work, but any *absolute* HP/healing number written before 2026-08-11 is wrong.
- **Major DPS cooldowns lowered, steady-state damage raised** across several
  specs — the stated design direction that the Shadow Bolt/Demonbolt buffs and
  Diabolist nerfs are Demo's instance of.
- **Diminishing-return categories now reset after 20s (was 16s).** The patch-note
  line is written globally (CLASSES preamble), but its developers' note argues the
  change entirely in **PvP** terms — Season 1 CC monitoring, "increasing the reset
  timer … for Season 2". PvE trash DR does exist, so the plain reading is that a
  second **Shadowfury** or **Howl of Terror** on the same M+ pack now needs a
  20-second gap rather than 16 to land at full duration — but **that PvE
  application is our inference, not a stated Tier-1 fact.** Treat the 20s number
  as certain and the M+ consequence as unconfirmed until someone times it on live
  trash.
- All interrupts now show a **"missed" visual + sound** when used on a
  non-casting target (Spell Lock included).

⚠ The 12.1 Warlock PvP lines (movement-slow tier-down) are **PvP-only** and are
deliberately not reflected in anything below.

## TL;DR

- **Hero tree is no longer one answer.** Post-nerf the two trees have separated:
  **Diabolist for M+ / AoE** (still clearly ahead on cleave and multi-target),
  **Soul Harvester for pure single-target / raid** — Icy Veins (upd. 2026-08-10,
  12.1) has Soul Harvester "tuned around 3% higher than Diabolist in pure
  single-target, but suffers from a substantial lack of cleave in comparison."
  This is a change from 12.0.7, where Diabolist was the answer everywhere.
- **Apex: Dominion of Argus** — big Summon Demonic Tyrant buff; the Diabolist
  build is still constructed around the 1-min Tyrant window (the nerfs reduced
  its size, they did not remove it).
- **Pet: Felguard** for group content. Swap to **Voidwalker** for solo delves
  (tank/taunt).
- **Stats: Mastery ≈ Crit > Haste >> Versatility** — full detail in `gearing.md`.
  ⚠ Not re-simmed for 12.1; the filler buffs plausibly move Haste.

## M+ build (Diabolist)

**Hero tree — Diabolist**, and this is the one place the 12.1 nerfs did *not*
overturn the 12.0.7 verdict. Icy Veins' 12.1 pass still has Diabolist offering
"comparable single-target to Soul Harvester, whilst retaining superior AoE" —
which is exactly the M+ shape. The build is deterministic and burst-leaning,
front-loading damage through the **Diabolic Ritual → Overlord / Mother of Chaos
/ Pit Lord** procs inside the Tyrant window. All 14 Diabolist nodes showed
~49–50/50 adoption in Season 1 — no real choice points, and 12.1 added none.

> ⚠ *(Naming fix, 2026-08-11: this file previously called the proc engine
> "Demonic Rituals". The talent is **Diabolic Ritual** (spell 428514) per the
> generated `talents.md` @ `12.1.0.68914`.)*

**Soul Harvester is now the raid/ST counterpart, not just the defensive
alternative** (damage via Demonic Soul / Wicked Reaping / Soul Anathema, with
better defensives overall). If you play both roles, expect to carry two
loadouts in 12.1 rather than one.

⚠ **The Tier-3 maxroll captures in this directory still read "Diabolist performs
slightly better in (almost) all scenarios"** — that paragraph is a day-0
carryover, not a post-nerf re-evaluation (the raid capture is still labelled
12.0.7 upstream). Icy Veins' 2026-08-10 pass is the fresher Tier-3 read and is
what the split above follows. Do not lift the maxroll hero-tree verdict.

**Spec tree near-universals (murlok top players, S1 data — 12.1 moved no Demo
node):** Hand of Gul'dan, Demoniac, Call Dreadstalkers, Fel Intellect,
Imp-erator, Implosion, Summon Felguard, Rune of Shadows, Demonic Brutality,
Summon Demonic Tyrant, **Dominion of Argus** (apex). Trap picks (~0 usage):
Dominant Hand, Doom, Empowered Felstorm.

**Class tree near-universals:** Fel Domination, Soul Leech, Burning Rush,
Demon Skin, Fel Armor, Demonic Embrace, Demonic Fortitude, Mortal Coil,
Pact of the Annihilan, Demonic Circle, Pact of the Satyr, Dark Pact,
Fortified Soul, Demonic Gateway, Swift Artifice, Soul Link, Pact of
Gluttony, Soulburn.

**M+-specific class swaps (vs raid):** take the AoE-utility nodes —
**Foul Mouth** (Curse of Exhaustion/Tongues/Weakness curses everything in
10 yd), **Curse of Tongues / Blight of Weakness**, and one side of the AoE-CC
choice node.

> **The AoE-CC choice, spelled out** (corrected 2026-08-11 — this file previously
> said "Diabolist also grants a 25-sec Howl of Terror hitting up to 10 targets",
> which read as if the hero tree hands you Howl for free while the same paragraph
> told you to take Shadowfury. Per the generated `talents.md` @ `12.1.0.68914` and
> the 12.1 tooltips in `ability-inventory.md` @ `12.1.0.69214`, it is two picks
> deep and mutually exclusive with Shadowfury):
>
> - Class tree **row 9,6 is a CHOICE node — Howl of Terror (`5484`) *or*
>   Shadowfury (`30283`)**. You get one, not both.
> - Base: **Shadowfury** = 60s CD, stuns everything within 8 yd for 3s.
>   **Howl of Terror** = 40s CD, disorients 5 enemies within 10 yd for 20s
>   (damage breaks it).
> - **Oppressive Darkness** (`1270255`, class tree 10,7, 23 pts, plain passive —
>   not a choice) buffs whichever you took: Shadowfury **−15s CD, +2 yd radius**;
>   Howl **−5s CD, +5 targets**.
> - The **Diabolist** contribution is **Annihilan's Bellow** (`429072`) — Howl
>   **−10s CD, +5 yd range** — and it is the *loser side* of the hero choice node
>   at 9,9 against **Soul-Etched Circles** (`428911`, free Soulburn on Demonic
>   Circle: Teleport).
> - So the "25s / 10 targets" Howl is real (40 − 10 − 5 = **25s**; 5 + 5 = **10
>   targets**, 15 yd range) but costs **three** picks: the Howl side of 9,6,
>   Annihilan's Bellow at 9,9, and Oppressive Darkness.
>
> **Recommendation stands with Shadowfury** for M+: a 3s AoE *stun* on a 45s
> effective CD (60 − 15) is the harder-stopping tool for pull control, it does not
> break on damage, and it leaves the Diabolist 9,9 choice free for Soul-Etched
> Circles. Take the Howl package only if your group specifically wants a long,
> wide, damage-fragile disorient. ⚠ Either way the CC now sits on the **20s** DR
> reset (see the caveat above about that being a PvP-framed note).

**Pet: Felguard** (universal). The Felguard, Dreadstalkers, Tyrant, and
Diabolist demon summons are a large chunk of both ST and cleave — and are the
part 12.1 taxed, so the relative value of *your own* casts is up.

### Import strings

**Tier-3 — Icy Veins M+/AoE (Diabolist), 12.1, upd. 2026-08-10:**
```
CoQAAAAAAAAAAAAAAAAAAAAAAwMjZGNLmxmZGzyAAAAAAAAGzYYBGYb0CNsYMzYZ2mZmxMAwMjZGzMDwYmxMbAAgxMzMzww2MGwA
```

**Tier-3 — Icy Veins single-target / raid (Soul Harvester), 12.1, upd. 2026-08-10:**
```
CoQAAAAAAAAAAAAAAAAAAAAAAwMzMzoZjhZmxsMAAAAAAAjtlBGwAmhtQGbmxmZ2mlZmZMDAYMzMzAMzMmxMDAAwMzMzMjZYZAYA
```

**Tier-1 — simc default APL (Diabolist), commit 48103ef 2026-05-18 —
⚠ PRE-12.1, awaiting re-pull:**
```
CoQAAAAAAAAAAAAAAAAAAAAAAYmxMzoZjZ2mZGzyAAAAAAAAGzYYBGYb0CNsYMGLzyMzMmBAmZMzMzMDgZGzAAAYMzMjhhlZMgB
```
This hash predates 12.1. Because no Demo talent node was added, removed or moved
in 12.1, it should still **import** cleanly — but it encodes the pre-nerf
Diabolist weighting, so treat it as a 12.0.7 artifact until
`uv run python -m wowkb.simc warlock demonology` is re-run at the 12.1 SHA
(that regenerates `sims.md`).

> Paste in-game: Talents UI → Import. Verify the string loads as the hero tree
> you expected — **Diabolist** for the M+ string, **Soul Harvester** for the ST
> string — before keying.

## Delves / solo build

Hero-tree choice is **mostly stylistic** for delves, and 12.1 slightly favours
the defensive side of it:

- **Soul Harvester** = the safer solo pick — better defensives overall:
  stronger multi-use Healthstone, **Gorebound Fortitude**, **Friends In Dark
  Places**. Now also the higher pure-ST tree, so it is no longer a damage
  concession for single-target delve bosses.
- **Diabolist** = more burst to delete dangerous packs fast, though 12.1 cut
  the demon payload by 20%.

**Solo survivability levers** (independent of hero tree):
- **Pet: Voidwalker** for the taunt/tank and shield — standard solo swap
  off Felguard.
- Lean on **Demonic Healthstone** (reusable in combat), **Dark Pact**,
  **Soul Link**, **Mortal Coil** (heal + fear), **Burning Rush** for
  kiting. Demonology lacks an immunity/damage-reversal, so kite + pet
  threat carries solo content.
- **Soul Leech is quietly better in 12.1** — the pet-ability correctness pass
  above means Wild Imp / Tyrant / Vilefiend / Gloomhound damage now feeds the
  absorb. **Drain Life's health drain is also +25%.** (⚠ Same node, **new spell
  ID `1311653`, was `108370`** — re-point any WeakAura or CDM entry that tracked
  the absorb by ID.)
- ⚠ **Creature damage is +25% at max level** (against a +25% larger health
  pool). Health consumables were rescaled to match; ignore any pre-12.1
  absolute healthstone/potion number.

## TODO

- [x] Re-verify vs 12.0.7 (checked 2026-07-07). Confirmed stable for PvE:
      the only Demo tuning in 12.0.7 is **PvP-combat-only** (Shadow Bolt
      +200%, Demonbolt +30% in PvP; freecasting buff for PvP). No PvE
      talent/stat/hero-tree changes.
- [x] Re-verify vs 12.1 (2026-08-11). Tier-1 tuning applied above; hero-tree
      verdict split M+ (Diabolist) vs ST/raid (Soul Harvester) per Icy Veins'
      12.1 pass. Talent existence cross-checked against the generated
      `talents.md` @ `12.1.0.68914` — no Demo node added, removed or moved.
      One class-tree spell **re-ID**: Soul Leech `108370` → `1311653` (node
      position 2,4 unchanged) — recorded above.
- [x] Verifier pass (2026-08-11) — fixed: Channel Demonfire added to the
      Soul-Leech reversal list (patch-notes/12.1.md l.1177-1180 names three, this
      file named two); the 20s DR reset's PvE application marked as inference, not
      Tier 1 (the dev note at l.342 argues it purely in PvP terms); and the
      "Diabolist grants a 25-sec Howl of Terror" line rewritten — it is two choice
      nodes plus Oppressive Darkness deep and mutually exclusive with the
      Shadowfury this file recommends.
- [x] Soul-Harvester ST/raid import string pulled (Icy Veins, 12.1, above) —
      resolves the 2026-07-14 open item.
- [ ] **Re-pull the Tier-1 simc APL + talent hash at the 12.1 SHA**
      (`wowkb.simc warlock demonology`) and replace the pre-12.1 Diabolist
      string above. Until then the only 12.1-current strings here are Tier 3.
- [ ] Confirm the **20s DR reset actually applies to PvE trash** (time two
      Shadowfurys on the same M+ pack). The Tier-1 line is global but its
      developers' note is written entirely about PvP; hedged in the body until
      measured.
- [ ] Re-check the hero-tree verdict once **Season 2 opens (2026-08-18)** and
      murlok/Warcraft Logs repopulate — the Tier-2 adoption data cited here is
      Season 1 and the 12.1 split has not yet been confirmed against real play.
- [x] rotation.md added 2026-06-13 (ST/AoE priority, Tyrant window,
      CDM setup + Kalamazi/wago import pointers). ⚠ Its CDM section needs the
      12.1 note that **Summon Demonic Gateway is now Utility by default**.

---
title: Priest Holy — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/priest/holy/ability-inventory.md  # tier 1, generated from DB2 @ 12.0.7.67808 + Blizzard spell API — name/spellID/origin/cooldown/tooltip
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 adjudication of this file's claims @ 12.0.7.67808
  - knowledge/classes/priest/holy/talents.md  # tier 1, Blizzard talent-tree API @ 12.0.7.67808
  - raw/wago/SpellName.csv  # tier 1, spell-name reconciliation
  - https://www.method.gg/guides/holy-priest/playstyle-and-rotation  # tier 3, 2026-06-16
  - https://www.icy-veins.com/wow/holy-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
confidence: medium
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Priest Holy — Abilities (Midnight S1)

> **This file carries no per-spell facts.** Canonical name, spellID, acquisition
> origin, baseline cooldown, talent/hero placement and the **in-game tooltip
> text** for every ability the spec can have live in **`ability-inventory.md`**
> beside this file — generated from wago DB2 + the Blizzard spell API @
> 12.0.7.67808 and regenerated on patch day.
>
> | Question | Read |
> |---|---|
> | What does X do? Its spellID, cooldown, tooltip? | `ability-inventory.md` |
> | When do I press X? | `rotation.md` |
> | Do I take X? Which hero tree? | `builds.md`, `talents.md` |
> | Why is X missing from the inventory? | `../../_abilities/section-3-corroborated.md`, `section-4-catalogue.md` |
>
> This file is the editorial layer: the resource model, which inventory rows are
> actually buttons, and the judgements game data cannot make.

## Resource model

Holy is Priest's atonement-free, throughput-and-spot-heal spec. It has **no
secondary resource beyond mana** — its rotational engine is **Holy Words**,
gated by cooldown rather than by a bar.

**Serendipity** is the whole loop: casting a normal spell reduces the matching
Holy Word's cooldown. **Flash Heal → Holy Word: Serenity**, **Prayer of Healing
→ Holy Word: Sanctify**, **Smite → Holy Word: Chastise**. So the playstyle is
"cast the right filler to bring the right Holy Word online, then fire it." On
top of that sit two always-on passive-value streams — **Mastery: Echo of Light**
(a HoT behind every direct heal) and **Prayer of Mending** (a bouncing ward kept
on cooldown).

⚠ **The Midnight kit is narrower than most guides describe.** **Heal**,
**Renew** and **Circle of Healing** are not acquirable at 12.0.7 (see the
reconciliation notes), so the Serendipity feeders are Flash Heal and Prayer of
Healing only. Any guide describing a Heal/Renew filler loop is describing The
War Within.

**Hero trees.** `builds.md` owns the pick. Neither adds or removes a button:
**Archon** re-weights the same kit onto Prayer of Healing (Halo becomes a short
cooldown feeding Surge of Light, and Spiritwell redirects those procs into
Prayer of Healing rather than Flash Heal); **Oracle** re-weights it onto Prayer
of Mending. Both share the same Holy Word core and the same damage rotation.

## Inventory

The curated subset: which of the generated inventory's rows are buttons you
actually press, and what each is *for*. **Role only** — no spellID, cooldown,
cast time or mechanics, because all four regenerate one file over. ⚠ This table
is also a **machine input**: `wowkb.gen_abilities` reads its first column to
build the `prose-only` leg of `../../_abilities/section-4-catalogue.md`, so a
name deleted from here silently disappears from that catalogue.

| Ability | Role |
|---|---|
| Holy Word: Serenity | Holy Word engine — single target; the payoff Flash Heal is buying |
| Holy Word: Sanctify | Holy Word engine — group; the payoff Prayer of Healing is buying |
| Holy Word: Chastise | Holy Word engine — damage + CC; the payoff Smite is buying, and the Empyreal Blaze trigger |
| Prayer of Mending | Always-on passive value, kept on cooldown; Oracle's centrepiece |
| Flash Heal | Serendipity feeder — spot heal that buys Serenity and builds Lightweaver |
| Prayer of Healing | Serendipity feeder — group heal that buys Sanctify; Archon's main throughput button |
| Holy Nova | Situational instant heal + damage; a real damage button only with Lightburst |
| Benediction | Passive (apex) — upgrades a Flash Heal off Prayer of Mending |
| Halo | Healing cooldown — Archon's short-cycle throughput engine, feeding Surge of Light |
| Apotheosis | Healing cooldown — the Holy Word amplifier |
| Divine Hymn | Healing cooldown — planned raid channel |
| Guardian Spirit | Healing cooldown — single-target cheat-death, reactive |
| Power Infusion | Throughput cooldown — self or handed to a DPS |
| Desperate Prayer | Personal survival |
| Smite | Serendipity feeder (damage) — single-target filler that buys Chastise |
| Holy Fire | Damage — the AoE damage engine with Burning Vehemence |
| Shadow Word: Death | Damage / execute |
| Power Word: Fortitude | Group buff — maintain |
| Levitate | Utility |
| Leap of Faith | Utility — reposition an ally |
| Angelic Feather | Movement — placed, for the group |
| Fade | Personal survival + threat drop |
| Psychic Scream | Control — AoE fear |
| Shackle Horror | Control — creature-type gated, situational |
| Mind Control | Control — mostly outdoor/PvP |
| Mind Soothe | Utility — skip pulls |
| Purify | Dispel — friendly |
| Dispel Magic | Dispel — offensive |
| Mass Dispel | Dispel — area; the only one that strips normally-undispellable effects |
| Resurrection | Out-of-combat resurrection |
| Mastery: Echo of Light | Passive — the spec's signature always-on throughput. ⚠ **Not in `ability-inventory.tsv`**, see below |
| Surge of Light | Passive (proc) — free Flash Heal, or Prayer of Healing under Archon/Spiritwell |
| Lightweaver | Passive — the Flash Heal → Prayer of Healing coupling; never cast Prayer of Healing cold |
| Empyreal Blaze | Passive — the Chastise → Holy Fire link that makes Holy a real damage dealer |
| Restitution | Passive — death prevention, via Spirit of Redemption |

Also in the inventory and worth knowing you have: **Spirit of Redemption** (what
Restitution and Guardian Angel modify) and **Mass Resurrection**.

⚠ **Holy has no true interrupt and no battle rez.** Silence is Shadow's and
appears in no Holy acquisition row; Resurrection and Mass Resurrection are both
out-of-combat. Holy Word: Chastise's incapacitate is the closest thing — which
is why the BucketBinds seed binds it to the `Interrupt` bucket — but it is a CC,
not a school lockout, and does not answer a "kick this cast" call. Both of these
are **absences**, and a generated inventory structurally cannot state an
absence; they matter for group composition.

## Reconciliation notes — Tier 1 @ 12.0.7.67808

- **Three heals this file used to list are not acquirable at 12.0.7** and are
  gone. Each was checked against every acquisition table — trait nodes on the
  live Priest tree (**795**), `SkillLineAbility` on the Priest line (**804**),
  `SpecializationSpells` and `PvpTalent` — and attaches to none:
  - **Heal** (2060) — the Priest kit carries Flash Heal, Power Word: Shield,
    Prayer of Mending and Smite; it does not carry Heal, and none of the other
    112 spells named "Heal" attaches either.
  - **Renew** (139) — tree 795 has `Renewed Faith`, but no Renew.
  - **Circle of Healing** — no node on tree 795 and no other attachment.

  This is a real narrowing of the spec, not a bookkeeping detail. ⚠ It is also
  the class of claim a generated inventory structurally cannot make: it lists
  what *is*, never what stopped being — so if this section is lost, the KB
  silently re-acquires The War Within's kit the next time someone reads a guide.
  ⚠ **`rotation.md` has not caught up** — its pre-combat step still says
  "pre-apply Prayer of Mending and **Renew**" and its raid priority still lists
  **Circle of Healing** "(if talented)". Those two lines are stale against this
  finding.
- **Mastery: Echo of Light is absent from `ability-inventory.tsv` by tool
  behaviour, not by absence.** It *is* attached (`SpecializationSpells` → Holy,
  spell 77485); it is passive, and the generator drops passive
  `SpecializationSpells` rows, so the inventory carries neither the row nor a
  tooltip and its magnitude has no Tier-1 home. Tool gap, not a stale claim.
  - Mastery: Echo of Light — read the % of the heal it echoes and the HoT duration off the spellbook tooltip. @verify-ingame
- **Charge/recharge times are in neither layer.** The inventory's `cooldown` is
  `SpellCooldowns` at DifficultyID 0, which returns the **GCD** for a charge
  ability — Holy Word: Serenity, Holy Word: Sanctify, Prayer of Mending and
  Shadow Word: Death all read 0 or ~1.5s there, which is not their real
  cooldown. The recharge lives in `SpellCategory.ChargeRecoveryTime`,
  unreachable without breaking the build pin (`reconcile-ledger.md` §5 G6).
  For a healer this is the most load-bearing missing number in the KB: Holy Word
  charge cadence *is* the rotation.
  - Holy Word: Serenity / Sanctify, Prayer of Mending, Shadow Word: Death, Leap of Faith — read baseline cooldown + charge count off each tooltip. @verify-ingame
- **Halo is 60s baseline** (Archon shortens it) — this file previously carried
  Archon's reduced value as the baseline. **Mass Dispel is 120s**, not ~1 min.

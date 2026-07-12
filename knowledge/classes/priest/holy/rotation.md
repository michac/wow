---
title: Priest Holy — Rotation / Healing Priority (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/holy-priest/playstyle-and-rotation  # tier 3, 2026-06-16
  - https://www.method.gg/guides/holy-priest  # tier 3, 2026-06-16
  - https://www.icy-veins.com/wow/holy-priest-pve-healing-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - https://www.wowhead.com/guide/classes/priest/holy/rotation-cooldowns-pve-healer  # tier 4, upd. 2026-04-02 (nav-shell, snippet only)
confidence: medium
---

# Priest Holy — Rotation / Healing Priority (Midnight S1)

Holy has **no SimulationCraft APL** — simc ships no `MID1_Priest_Holy.simc`
profile (only Shadow / Shadow_Archon), so unlike DPS specs this priority is
**distilled from Tier-3 guides (method.gg + Icy Veins), not a Tier-1 APL**.
Treat it as reactive-healer guidance, not a fixed loop: you cast to demand, and
the "rotation" is really *which button wins when several are available*.

The through-line: **your Holy Words are your biggest per-cast heals**, so the
whole game is keeping them off cooldown (via Serendipity) and firing them the
instant they're up, while never overhealing with the filler that feeds them.
Both hero trees share the damage/DPS rotation; they diverge on the heal side
(Archon = Prayer of Healing engine, Oracle = Prayer of Mending engine).

## Pre-combat

- **Power Word: Fortitude** on the group.
- Pre-apply **Prayer of Mending** and **Renew** on the tank(s) so both come in
  with a Holy Word already partway off cooldown.
- Open damage (Smite / Holy Fire) if no immediate healing is needed — this
  brings Holy Word: Chastise online and pre-charges Empyreal Blaze.

## Cooldown rules

- **Apotheosis** is the core throughput cooldown — it triples Holy Word CD
  reduction and empowers them. Reset your Holy Words first, then during the
  window **spam Holy Words** (and, with **Divinity**, instant empowered Prayer
  of Healing). Use it on cooldown into any group-damage window.
- **Halo (Archon)** — a 40s cooldown that grants **4 Surge of Light** procs for
  Prayer of Healing. Fire it just **before Divine Hymn or Apotheosis**; **don't
  hold it longer than ~30s** or you lose healing. Use liberally.
- **Divine Hymn** — big planned raid-wide channel; also buffs healing received
  (~20%). Line up before known burst; don't clip.
- **Guardian Spirit** — reactive cheat-death + ~60% healing-received; save for a
  tank/ally about to eat a lethal hit, or as a raw throughput amp on a tank.
- **Power Infusion** — +25% haste; self-cast for a healing burst (Twins of the
  Sun Priestess also buffs an ally) or hand to a DPS in their window.
- **Desperate Prayer / Fade / Restitution** — personal survival, used reactively.

## Single-target healing priority

**Archon:**
1. **Holy Word: Serenity** — fire before it banks a 2nd charge (don't overcap).
2. **Prayer of Mending** on cooldown (prefer an injured ally).
3. **Benediction** (empowered Flash Heal), when talented/available.
4. Remaining **Holy Words** as they come up.
5. **Holy Nova** if **Lightburst** is talented (fills + damages).
6. **Flash Heal** to spot-heal and build Holy Word: Serenity CD / Lightweaver.

**Oracle:**
1. **Prayer of Mending** at 2 charges (don't overcap; Oracle magnifies its value).
2. **Holy Word: Serenity** before it reaches 2 charges.
3. **Benediction** (empowered Flash Heal).
4. **Prayer of Mending** on cooldown.
5. **Holy Nova** if Lightburst talented.
6. **Holy Word: Serenity** / **Flash Heal** with Surge of Light.

**Holy Word discipline (both):** don't sit on two charges of a Holy Word except
to pre-hold for known incoming burst — a Holy Word cast triggers **Epiphany**
(Prayer of Mending reset) and **Lasting Words** (free Renew), so wasting a
charge wastes those too.

## Raid / AoE healing priority

**Archon** (Prayer of Healing is the strongest button here):
1. **Holy Word: Sanctify** on an injured cluster; **Holy Word: Serenity** on a
   hurt priority target.
2. **Prayer of Mending** on cooldown.
3. **Prayer of Healing** with **Lightweaver** active and/or **Surge of Light**
   procs (from Halo/Spiritwell) — spend all Surge of Light on Prayer of Healing,
   *not* Flash Heal.
4. **Divine Hymn** / **Apotheosis** for scripted burst.
5. **Holy Nova** / **Circle of Healing** (if talented) for instant top-offs and
   while moving.

**Oracle** — same skeleton, but leans harder on **Prayer of Mending** uptime and
bounce efficiency (Guiding Light / Prompt Prognosis) with Prayer of Healing as
supplemental throughput; watch mana.

**Lightweaver management (Archon):** always have ≥1 Lightweaver stack (built by
Flash Heal) before casting Prayer of Healing — never cast Prayer of Healing
"cold."

## Damage rotation (both hero trees)

When healing isn't demanded, Holy does real DPS (and generates Chastise CD +
Empyreal Blaze value). Priority:
1. **Holy Word: Chastise** — triggers **Empyreal Blaze** for an instant/empowered
   Holy Fire (and Divine Image procs).
2. **Holy Fire** on cooldown — with **Burning Vehemence** it cleaves nearby
   enemies; this is the AoE-damage engine.
3. **Shadow Word: Death** as an execute / off-cooldown instant (where talented).
4. **Smite** as the single-target filler (feeds Chastise CD).
5. **Holy Nova** at ~4+ targets instead of Smite.

## Hero-tree branches (summary)

- **Archon** — heal side is **Prayer of Healing + Halo + Spiritwell/Surge of
  Light**; strongest raid-AoE and burst-window healer. Add Halo before Divine
  Hymn/Apotheosis and dump Surge of Light into Prayer of Healing.
- **Oracle** — heal side is **Prayer of Mending-centric passive value**
  (Guiding Light, Piety, Prophet's Insight replacing the old Premonition line);
  smoother, lower-APM, better for sustained spread damage. Same Holy Word core,
  same damage rotation.

## TODO / verify

- No Tier-1 simc APL exists for Holy — re-check each patch whether simc adds a
  `MID1_Priest_Holy` profile for a numeric re-distill. @verify-ingame
- Exact Holy Word cooldowns, reduction-per-cast, Halo/Apotheosis timers, and the
  Benediction effect are Tier-3-sourced — confirm against in-game tooltips.
- Sanity-check the opener + cooldown sequencing against a top Warcraft Logs raid
  parse (`wowkb.wcl`) once a log with a clean Holy Priest is available.

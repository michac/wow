---
title: Voidscar Arena — Midnight S2 M+ dungeon (stub)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24294369   # "Midnight Season 2" overview — S2 dungeon pool (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season schedule (tier 1)
  - https://develop.battle.net/documentation/world-of-warcraft/game-data-apis  # Blizzard journal API: journal-instance/1313 + journal-encounter/2791 (Taz'Rah), /2792 (Atroxus), /2793 (Charonus), namespace static-12.1.0_68914-us (tier 1 game data)
  - https://www.icy-veins.com/wow/dungeons-guide  # (tier 3 — Midnight dungeon index; NO dedicated Voidscar guide as of 2026-08-11)
  - https://warcraft.wiki.gg/wiki/Voidscar_Arena  # (tier 4, corroborating location + boss order only)
confidence: low
---

# Voidscar Arena — Midnight Season 2 Mythic+

> ⚠️ **STUB, written on patch day (2026-08-11).** Everything below comes from
> **Tier-1 game data** (the Blizzard dungeon journal at 12.1) plus the Tier-1
> Season 2 blog. There is **no route, no trash table, no affix guidance and no
> loot table here yet** — those come from play and from Tier-3 guides that do
> not exist on day 1 (Icy Veins' Midnight dungeon index carries a Voidscar
> Arena section but still links **no dedicated guide**). Nothing on this page is
> invented; missing means missing. See `## TODO`.

Three-boss Midnight dungeon in **Voidstorm** (subzone **Slayer's Rise**), level
90. It shipped with the Midnight expansion (journal-expansion/516) but **sat out
Season 1** — 12.1 puts it in the Mythic+ pool for the first time.

Journal blurb: *"The Voidscar Arena awaits worthy challengers! Overseer Charonus
has filled the arena with opponents plucked from across Azeroth, forcing them to
participate in his games."*

Difficulties available: **Normal / Heroic / Mythic / Mythic+** (journal
`modes` at 12.1 — the Mythic+ mode is the 12.1 addition).

## Season 2 availability — dated, not present-tense

| | **Week of 2026-08-11 (live now — pre-season)** | **Week of 2026-08-18 (Season 2 opens)** |
|---|---|---|
| Difficulties in play | Heroic + **Mythic 0 only** | Mythic+ opens |
| M0 lockout | **weekly**, this week only | back to **daily** |
| M0 reward | **Champion 1/6 (292)** | Champion 1/6 (292) |
| Keystones | **do not drop** | Mythic Keystones drop |

Season-wide rules (crests, rating ladder, teleports at +10, vault) live in
[`season-2-overview.md`](season-2-overview.md) — not here.

**Follower Dungeon:** yes. Voidscar Arena is in the Midnight follower-dungeon
pool (carried over from `season-1-overview.md`, verified 2026-06-13), so it can
be walked blind at Normal with AI companions — useful for layout, useless for
affix/tuning practice.

**Unlock:** reaching level 90, or completing *"Voidscar Arena: Breaking the
Triad"* (tier-4 only — warcraft.wiki.gg; the quest has no wiki page, and it is
**not** corroborated by a Tier-1 source). @verify-ingame

## Route

**Not captured.** No pull order, no skip, no pack-by-pack path has been recorded
for this dungeon. Do not infer one from the boss order — the arena layout is
unknown to this KB.

## Trash

**Not captured.** No trash mob, ability or interrupt-priority list exists yet.
This is the single biggest hole in the file: the sibling S1 dungeon files carry
first-class trash tables (mob → ability → see/do → archetype → tier → role) and
this one has nothing to put in them.

## Bosses

Three bosses, journal order: **Taz'Rah → Atroxus → Charonus**.

The tables below are **journal-derived only**. Each row is an ability Blizzard's
dungeon journal lists for that encounter, with the journal's own role split
(Damage Dealers / Healers / Tanks) preserved in the Role column. The
**Archetype** column is a provisional tag against
[the archetype taxonomy](../../systems/mechanic-archetypes.md), read off the
journal wording — it has **not** been confirmed against the fight in play.

⚠️ There is **no "Do" column and no consequence tier** (🔴/🟠/🔵/⚪) in this file.
Those are play-derived judgments in the sibling files; asserting them from
journal text would be fabrication. They land when the dungeon is actually run.

### Taz'Rah <!-- enc:2791 -->

*"The domanaar's prized champion, Taz'Rah, is forced to fight against his will.
Taz'Rah demands his own death from every opponent, hoping each battle will
finally end his suffering."*

| Ability | Journal text | Archetype (provisional) | Role |
|---|---|---|---|
| **Dark Bloom** (1300259) | Heavy Shadow damage to all players; causes **Void Fissures** to erupt | raid-damage | healer |
| **Umbral Rupture** (1296963) → **Void Fissure** (1296967) | The erupting fissures Dark Bloom leaves behind | ground-void-zone | all |
| **Ethereal Shades** (1296889) | Summons **Ethereal Shade** adds | kill-priority-add | all |
| **Nether Dash** (1222098) | An Ethereal Shade periodically targets a random player and damages everything **in a line in front of it**; inflicts Shadow damage over a long duration | frontal-cone | all |
| **Void Blast** (1297017) | Heavy Shadowstrike damage to the tank | tank-buster | tank |

### Atroxus <!-- enc:2792 -->

*"Imprisoned by Charonus, this starving behemoth is hoping for a new victim to
sate his appetite. Atroxus's sheer size is almost as dangerous as the poison he
spews."*

| Ability | Journal text | Archetype (provisional) | Role |
|---|---|---|---|
| **Noxious Breath** (1222724) | High damage **in front of** Atroxus | frontal-cone | all |
| **Monstrous Roar** (1262497) | Heavy physical damage to all players; summons a **Toxic Creeper** that attacks its target | raid-damage; kill-priority-add | all |
| **Fixate** (1283506) — Toxic Creeper | The Creeper locks onto its target | fixate-chase | all |
| **Sickening Bite** (1282892) — Toxic Creeper | Applies **stacking vulnerability to Nature damage** | tank-buster | tank |
| **Toxic Aura** (1222692) — Toxic Creeper | Persistent aura around the add | pulsing-aura | all |
| **Poison Splash** (1226031) → **Poison Pool** (1222484) | Leaves pools; the pool carries **Mind-Numbing Poison** (1263971) | ground-void-zone | all |
| **Hulking Claw** (1222642) | High Nature damage to the primary target | tank-buster | tank; healer |

### Charonus <!-- enc:2793 -->

*"The overly confident and ostentatious owner of the Voidscar Arena, Charonus,
is impressed by the fighting ability of Azerothians and demands them for his
grand collection."*

| Ability | Journal text | Archetype (provisional) | Role |
|---|---|---|---|
| **Unstable Singularity** (1264191) | Shadow damage and **reduced movement speed** to players caught in it; also what **collapses** a Gravitic Orb. Carries **Atomized** (1310026) | ground-void-zone; positional-gimmick | all |
| **Gravitic Orbs** (1223298) | Orbs **continually seek out players** until collapsed by an Unstable Singularity | fixate-chase | all |
| **Condensed Mass** (1263983) | High damage to all players (from the Orbs) | raid-damage | healer |
| **Void Cascade** (1222755) | Journal lists the ability; **no body text published** | — | — |
| **Dark Waves** (1311923) | Journal lists the ability; **no body text published** | — | — |
| **Cosmic Crash** (1227197) | Journal lists the ability; **no body text published** | — | — |

The Orb ⇄ Singularity interaction is the fight's stated core loop: orbs chase,
and a Singularity is what removes them. **How** that is executed (who baits,
where singularities are placed, what happens if an orb connects) is not
recorded — do not guess it.

## Loot

**Not captured.** No dungeon-specific drop list, trinket or tier-adjacent item
has been recorded. Season-wide reward tracks (M0 = Champion 1/6 · 292, crests =
Mistcrests, vault rows) are in [`loot.md`](loot.md),
[`season-2-overview.md`](season-2-overview.md) and
[`../great-vault.md`](../great-vault.md).

## Affixes

Nothing dungeon-specific. The S2 affix ladder itself is **unconfirmed** —
see [`affixes.md`](affixes.md) and the affix note in
[`season-2-overview.md`](season-2-overview.md).

## TODO

Sourcing plan, highest tier first. Nothing here should be filled from an
undated or pre-2026 page, and nothing from the SEO dungeon-guide sites that
already rank for this dungeon (several assert abilities — "Dark Rift", "Cosmic
Spike" — that do **not** appear in the 12.1 journal; treat them as fabricated
until a Tier-1/2 source says otherwise).

- [ ] **Route + trash tables.** Fill from Method (`method.gg/guides/dungeons/…`)
      and Icy Veins once they publish a Voidscar Arena guide — Icy Veins'
      Midnight dungeon index has the section but **no guide link** as of
      2026-08-11. Follow the sibling format: mob → ability → see/do → archetype
      → consequence tier → role. Cross-check anything single-sourced.
- [ ] **Body text for Void Cascade / Dark Waves / Cosmic Crash.** The journal
      lists all three on Charonus with no description. Re-pull
      `journal-encounter/2793` after the next build, and/or read the spell
      tooltips via `wowkb.blizzard spell 1222755 / 1311923 / 1227197`.
- [ ] **Confirm the provisional archetype tags** against the fight in play, then
      add the missing **"Do"** column and **consequence tiers**, and drop the
      "provisional" caveat. `systems/mechanic-archetypes.md` feeds
      `projects/mplus_memory` — untagged/mistagged rows propagate.
- [ ] **@verify-ingame** the unlock condition (*"Voidscar Arena: Breaking the
      Triad"*), which is tier-4 only, and the entrance coordinates
      (53.7, 34.0 in Slayer's Rise — tier-3, Icy Veins index).
- [ ] **Warcraft Logs encounter IDs** for the three bosses, once S2 logs exist
      (the S1 dungeon files carry theirs; tracked as a batch item in
      `season-2-overview.md`).
- [ ] **Dungeon loot table** once M0 drops are observed / the journal's item
      lists are pulled.
- [ ] **Timer / route length** — not published in the 12.1 notes; read it off
      the in-game keystone UI after 2026-08-18.

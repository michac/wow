# Investigation — recovering Adventure Guide ability text

**Question:** the `journal-encounter` API payload maps 1:1 to the in-game
Adventure Guide UI, but the per-ability description text is missing (sections
carry only a spell link, and `/data/wow/spell/{id}` 404s for boss abilities). Is
there a mechanism to actually resolve those hrefs? **Yes — fully solved.**

## What we learned (verified 2026-06-25, patch 12.0.5 / journal pulled at 12.0.7 PTR build)

1. **The Game Data spell endpoint only exposes player-facing spells.** Live
   player spells (Agony 980, Corruption 172, Frostbolt 116) return a full
   `description`. **Boss/NPC ability spells 404** — both Midnight-new IDs
   (Repulsing Slam 474496, Ethereal Shackles 1214038…) *and* old ones (Ranjit's
   Chakram Vortex 156793). Namespace/build doesn't matter; they're simply not in
   the web API's spell coverage. So the hrefs are a dead end for descriptions.

2. **The in-game AG text is NOT the section's own text.** The DB2
   `JournalEncounterSection` table (`BodyText_lang`) is *empty* for these ability
   sections (titles are placeholder "Section 6"). The mechanism the in-game client
   uses: when a section has no BodyText, it **renders the linked spell's name +
   tooltip description** instead. That's the quirk.

3. **The spell tooltip text lives in DB2 `Spell.db2` `Description_lang`**, which
   **wago.tools exposes** (and the project already wraps with `wowkb.wago`). Every
   one of our boss-ability spell IDs resolved there.

4. **The text uses Blizzard's tooltip template syntax**, all resolvable from
   sibling DB2 tables:

   | Token | Meaning | Source table |
   |-------|---------|--------------|
   | `$s1`,`$NNNs2` | effect value (damage/%) | `SpellEffect.EffectBasePointsF` |
   | `$t1` | aura tick period | `SpellEffect.EffectAuraPeriod` |
   | `$d` | duration | `SpellMisc.DurationIndex` → `SpellDuration.Duration` |
   | `$@spellnameN` | another spell's name | `SpellName.Name_lang` |
   | `$@spelldescN` | another spell's full description | recurse into `Spell.db2` |
   | `$?DIFFn[a][b]` | difficulty-conditional text | pick the branch |
   | `$aN` | radius (yards) | `SpellRadius` (not yet wired — minor) |

   This is exactly what Wowhead / wago.tools do; spell-tooltip parsers are a
   well-trodden problem.

## Proof

`scratchpad/resolve_ag.py` joins the journal tree + 6 DB2 tables and emits
[`magisters-terrace.adventure-guide.json`](./magisters-terrace.adventure-guide.json).
Sample (Arcanotron Custos), matching the in-game guide:

- **Refueling Protocol** — "Upon running out of energy Arcanotron Custos begins
  recharging, drawing Energy Orbs toward itself and increasing damage taken by
  **20%** for **20 sec**."
- **Ethereal Shackles** — "…inflicting **9** Arcane damage every **3 sec** and
  rooting them for **15 sec**."
- **Repulsing Slam** — "…inflicting **30** Arcane damage and knocking them back."
- **Arcane Expulsion** — "…creating a pool of **Arcane Residue** at its feet…"
  (cross-ref resolved).

Residual polish (non-blocking): a bare `$t` (no index) and `$aN` radius aren't
resolved yet; `-50%` shows a cosmetic double-negative. All trivial parser fixes.

## The pipeline (for build)

```
journal-encounter/{id}   (wowkb.blizzard, web API)  → section tree, SpellID,
                                                       order, role tips, lore,
                                                       creatures, loot
Spell / SpellName / SpellEffect / SpellMisc /        → resolve every ability's
  SpellDuration / (SpellRadius)  (wowkb.wago, DB2)     name + description text
small template parser                                → render $-tokens
```

DB2 tables now cached in `raw/wago/` (Spell, SpellName, SpellEffect, SpellMisc,
SpellDuration, JournalEncounterSection). wago.tools is a **tier-1** source per
`knowledge/_meta/sources.md`.

## Recommendation

Worth doing. The official text is **authoritative, complete (no per-dungeon
sourcing gaps), and patch-updatable from one pipeline**. But note its limit: a
tooltip says *what the ability does*, **not what you should do** — so keep the
hand-distilled `response`/"Do" text and the API role tips as the strategy layer.
Ideal accordion entry = official description (what) + distilled response (do) +
archetype/tier tags.

**Two ways to use it:**
- **Enrichment** — fold resolved descriptions into the KB / `content.json` as a
  new `ability.officialText`, alongside the existing distilled fields.
- **Validation** — diff official text against the hand-distilled `whatItDoes` to
  catch drift/errors in the current KB (a QA pass).

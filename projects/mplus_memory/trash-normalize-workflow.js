export const meta = {
  name: 'mplus-trash-normalize',
  description: 'Normalize all 8 M+ dungeon trash sections to one table schema + add the Dalaran Gaming video as a corroborating source',
  phases: [{ title: 'Normalize', detail: 'one agent per dungeon: rewrite ## Trash to canonical table + add video source' }],
}

const KB = '/home/mchristiansen/code/fun/wow/knowledge/endgame/mythic-plus'
const VIDEO_SRC = '  - https://www.youtube.com/watch?v=DMcpeEK_tHE  # Dalaran Gaming "How to Master All 8 Dungeons: Midnight S1 M+ Walkthrough", uploaded 2026-03-24 (tier 3, boss corroboration)'

const SLUGS = 'interruptible-cast, ground-void-zone, tank-buster, spread-out, dispel, kill-priority-add, frontal-cone, knockback, soak, raid-damage, stack-up, fixate-chase, purge-soothe, positional-gimmick, heal-absorb, charge, proximity-bait, pulsing-aura, burn-window, balance-kill, flavor'

const FILES = [
  'magisters-terrace', 'maisara-caverns', 'nexus-point-xenas', 'windrunner-spire',
  'algethar-academy', 'seat-of-the-triumvirate', 'skyreach', 'pit-of-saron',
]

const SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    trashRowsBefore: { type: 'integer', description: 'count of distinct trash ABILITIES in the section before the rewrite' },
    trashRowsAfter: { type: 'integer', description: 'count of trash ability rows in the normalized table(s)' },
    lowConfPreserved: { type: 'integer', description: 'how many single-source/low-confidence rows were carried over with their flag' },
    sourceAdded: { type: 'boolean' },
    note: { type: 'string', description: 'anything dropped, merged, or ambiguous' },
  },
  required: ['dungeon', 'trashRowsBefore', 'trashRowsAfter', 'sourceAdded'],
}

function prompt(slug) {
  return `Reformat ONE section of the markdown file ${KB}/${slug}.md. This is a pure-reformatting + source-add task — preserve every fact, change only shape.

TASK A — add a corroborating source. In the YAML front matter \`sources:\` list, append this exact line (keep it under the existing source lines):
${VIDEO_SRC}

TASK B — normalize the \`## Trash\` section to ONE canonical table schema. Today the trash section may be bullet lists or tables with differing columns; rewrite it so every pack uses this exact table:

### <pack / area name>
| Mob | Ability | See → Do | Archetype | Tier | Role |
|---|---|---|---|---|---|
| <mob> | **<ability>** | <what you see → what you do> | <archetype-slug> | <emoji> | <role> |

RULES (critical — do not lose information):
- Keep ALL existing area/pack subheadings (### ...) and a short intro line under \`## Trash\` if one exists (e.g. the confidence rule).
- One row PER ABILITY (if a mob has 2 abilities, that's 2 rows repeating the mob name). Preserve every mob and every ability currently listed.
- **Archetype** column = the bare canonical slug, no backticks. It MUST be one of: ${SLUGS}. Keep whatever slug the row already has; do not retag.
- **Tier** column = the consequence EMOJI only (🔴 / 🟠 / 🔵 / ⚪). If the current row writes "🔵 your job" etc., keep just the emoji.
- **Role** = short (DPS / healer / tank / all / "all (kick)" etc.) — carry over what's there.
- **Provenance MUST survive.** Any row that is currently flagged single-source / Method-only / "confidence: low" must keep that flag: append \` _(single-source)_\` (or \` _(Method-only)_\` if it names the source) to the END of its "See → Do" cell. Rows currently marked "(both)" or unflagged stay unflagged. If the whole section is single-sourced and says so in an intro line, you may keep that intro note instead of per-row flags — but don't silently drop the distinction.
- Do NOT touch the \`## Route\`, \`## Bosses\`, or \`## DPS notes\` sections, or any boss table. Only the front-matter source line and the \`## Trash\` section change.
- Do NOT invent, add, or drop mobs/abilities. Same information, new shape.

Before you finish, count the distinct trash abilities you started with and the rows you ended with — they must match. Save the file.

RETURN: dungeon, trashRowsBefore, trashRowsAfter, lowConfPreserved, sourceAdded, note.`
}

phase('Normalize')
const results = await parallel(FILES.map(slug => () =>
  agent(prompt(slug), { label: `trash:${slug}`, phase: 'Normalize', schema: SCHEMA })
))

const ok = results.filter(Boolean)
const mismatches = ok.filter(r => r.trashRowsBefore !== r.trashRowsAfter)
return {
  normalized: ok.length,
  of: FILES.length,
  sourcesAdded: ok.filter(r => r.sourceAdded).length,
  rowCountMismatches: mismatches.map(r => ({ dungeon: r.dungeon, before: r.trashRowsBefore, after: r.trashRowsAfter, note: r.note })),
  perFile: ok.map(r => ({ dungeon: r.dungeon, before: r.trashRowsBefore, after: r.trashRowsAfter, lowConf: r.lowConfPreserved })),
}

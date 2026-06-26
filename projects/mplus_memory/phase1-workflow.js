export const meta = {
  name: 'mplus-phase1-content',
  description: 'Scrape + distill 8 M+ dungeon guides, derive mechanic-archetype taxonomy, tag every ability',
  phases: [
    { title: 'Distill', detail: 'fetch Method+IcyVeins, corroborate via journal API, write 8 dungeon files' },
    { title: 'Taxonomy', detail: 'cluster full boss+trash ability corpus into ~15-20 archetypes' },
    { title: 'Tag', detail: 'back-fill canonical archetype slugs + assert full coverage per dungeon' },
  ],
}

const REPO = '/home/mchristiansen/code/fun/wow'
const KB = `${REPO}/knowledge/endgame/mythic-plus`
const TAXONOMY_FILE = `${REPO}/knowledge/systems/mechanic-archetypes.md`
const FETCHED = '2026-06-24'

// Tier-1 canonical boss lists (from raw/journal/season1-bosses.json) + verified guide URLs.
const DUNGEONS = [
  { slug: 'magisters-terrace', name: "Magisters' Terrace", inst: 1300,
    bosses: [['Arcanotron Custos',2659],['Seranel Sunlash',2661],['Gemellus',2660],['Degentrius',2662]],
    method: 'https://www.method.gg/guides/dungeons/magisters-terrace',
    icy: 'https://www.icy-veins.com/wow/magisters-terrace-dungeon-guide' },
  { slug: 'maisara-caverns', name: 'Maisara Caverns', inst: 1315,
    bosses: [["Muro'jin and Nekraxx",2810],['Vordaza',2811],["Rak'tul, Vessel of Souls",2812]],
    method: 'https://www.method.gg/guides/dungeons/maisara-caverns',
    icy: 'https://www.icy-veins.com/wow/maisara-caverns-dungeon-guide' },
  { slug: 'nexus-point-xenas', name: 'Nexus-Point Xenas', inst: 1316,
    bosses: [['Chief Corewright Kasreth',2813],['Corewarden Nysarra',2814],['Lothraxion',2815]],
    method: 'https://www.method.gg/guides/dungeons/nexus-point-xenas',
    icy: 'https://www.icy-veins.com/wow/nexus-point-xenas-dungeon-guide' },
  { slug: 'windrunner-spire', name: 'Windrunner Spire', inst: 1299,
    bosses: [['Emberdawn',2655],['Derelict Duo',2656],['Commander Kroluk',2657],['The Restless Heart',2658]],
    method: 'https://www.method.gg/guides/dungeons/windrunner-spire',
    icy: 'https://www.icy-veins.com/wow/windrunner-spire-dungeon-guide' },
  { slug: 'algethar-academy', name: "Algeth'ar Academy", inst: 1201,
    bosses: [['Vexamus',2509],['Overgrown Ancient',2512],['Crawth',2495],['Echo of Doragosa',2514]],
    method: 'https://www.method.gg/guides/dungeons/algethar-academy',
    icy: 'https://www.icy-veins.com/wow/algethar-academy-dungeon-guide' },
  { slug: 'seat-of-the-triumvirate', name: 'Seat of the Triumvirate', inst: 945,
    bosses: [['Zuraal the Ascended',1979],['Saprish',1980],['Viceroy Nezhar',1981],["L'ura",1982]],
    method: 'https://www.method.gg/guides/dungeons/seat-of-the-triumvirate',
    icy: 'https://www.icy-veins.com/wow/seat-of-the-triumvirate-dungeon-guide' },
  { slug: 'skyreach', name: 'Skyreach', inst: 476,
    bosses: [['Ranjit',965],['Araknath',966],['Rukhran',967],['High Sage Viryx',968]],
    method: 'https://www.method.gg/guides/dungeons/skyreach',
    icy: 'https://www.icy-veins.com/wow/skyreach-dungeon-guide' },
  { slug: 'pit-of-saron', name: 'Pit of Saron', inst: 278,
    bosses: [['Forgemaster Garfrost',608],['Ick and Krick',609],['Scourgelord Tyrannus',610]],
    method: 'https://www.method.gg/guides/dungeons/pit-of-saron',
    icy: 'https://www.icy-veins.com/wow/pit-of-saron-dungeon-guide' },
]

const ABILITY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    slug: { type: 'string' },
    fileWritten: { type: 'string', description: 'absolute path of the dungeon .md written' },
    signalsConfirmed: { type: 'boolean', description: 'true if BOTH guides showed Midnight/12.0/2026 signals' },
    bossEncounterIds: { type: 'array', items: { type: 'integer' }, description: 'journal-encounter IDs used to corroborate boss names' },
    confidence: { type: 'string', enum: ['high','medium','low'] },
    notes: { type: 'string', description: 'any source disagreement, missing trash, or low-confidence flags' },
    abilities: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          name: { type: 'string' },
          owner: { type: 'string', description: 'boss name or trash pack/mob name that uses it' },
          source: { type: 'string', enum: ['boss','trash'] },
          mechanicWord: { type: 'string', description: 'provisional 1-3 word descriptor of the mechanic (e.g. "interruptible cast", "frontal cone", "ground void zone", "kill-priority add")' },
          consequenceTier: { type: 'string', enum: ['wipe','death','job','flavor'] },
          role: { type: 'string', description: 'DPS / healer / tank / all' },
        },
        required: ['name','owner','source','mechanicWord','consequenceTier','role'],
      },
    },
  },
  required: ['dungeon','slug','fileWritten','signalsConfirmed','abilities','confidence'],
}

const TABLE_NOTE = `
The boss table shape to use (extends the established \`sunkiller-sanctum.md\` pattern with two columns):
| Ability | What it does | Do | Archetype | Tier |
|---|---|---|---|---|
Consequence-tier emoji: 🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor.

Front matter (exact keys) on the file:
---
title: <Dungeon> — Midnight S1 M+ dungeon guide
patch: 12.0.5
fetched: ${FETCHED}
sources:
  - <Method url>
  - <Icy Veins url>
  - Blizzard journal-instance/<inst id> + journal-encounter/<each boss id> (tier 1, boss-name corroboration)
confidence: high | medium | low
---
`

function distillPrompt(d) {
  const bosses = d.bosses.map(b => `${b[0]} (journal-encounter ${b[1]})`).join('; ')
  return `You are distilling the Midnight Season 1 Mythic+ guide for **${d.name}** into a knowledge-base file for a spaced-repetition M+ trainer. Work in the repo at ${REPO}. Run all python tools from \`${REPO}/tools\` via \`uv run python -m wowkb.<tool>\`.

GROUND TRUTH (Tier-1, already fetched): this dungeon is journal-instance ${d.inst}. Canonical bosses (USE THESE EXACT NAMES): ${bosses}.

STEPS:
1. SCRAPE both guides to raw/pages/ (skip the fetch if the file already exists there, just read it):
   - cd ${REPO}/tools && uv run python -m wowkb.fetch "${d.method}"
   - cd ${REPO}/tools && uv run python -m wowkb.fetch "${d.icy}"
   Then Read the two resulting markdown files in ${REPO}/raw/pages/.
2. STALENESS GATE: confirm BOTH files show Midnight / 12.0 / 2026 signals (Season 1 M+). If a guide reads as War Within / 11.x or shows no Midnight signal, discard it and set confidence accordingly + note it. Set signalsConfirmed=true only if both pass.
3. TIER-1 BOSS CORROBORATION: for each boss id above run \`cd ${REPO}/tools && MSYS_NO_PATHCONV=1 uv run python -m wowkb.blizzard journal-encounter <id>\`. The encounter \`sections\` carry per-ability titles and role text (Damage Dealers / Healers / Tanks) — mine these for canonical ability names and the "what to do". Confirm the guide boss names match the journal; use the journal spelling when they differ.
4. WRITE ${KB}/${d.slug}.md with these sections:
   - **Route** — ordered segments (the spatial spine; number them).
   - **Trash** — FIRST-CLASS, do not skip. Notable packs; for each notable ability give what-you-see → what-you-do, a provisional mechanic word, a consequence emoji, and role. A trash claim should appear in BOTH Method and Icy Veins; flag confidence: low for any single-sourced trash claim.
   - **Bosses** — one subsection per boss, each with the 5-column table below.
   - **DPS notes** (player is DPS) — brief, optional.
5. Provisional Archetype column: put a short descriptive mechanic word (NOT a final slug) in the Archetype column — a later stage canonicalizes these. Keep words consistent (e.g. always "interruptible cast", "frontal cone", "ground void zone", "stack", "spread", "soak", "dispel", "kill-priority add", "tank buster", "knockback", "fixate").
${TABLE_NOTE}

RETURN (structured): the full ability list — EVERY boss AND trash ability you put in the file — each with owner, source (boss|trash), provisional mechanicWord, consequenceTier (wipe|death|job|flavor), and role. This pooled list seeds the archetype taxonomy, so be complete. Also return fileWritten (abs path), signalsConfirmed, bossEncounterIds, confidence, and notes.`
}

phase('Distill')
const distilled = await parallel(DUNGEONS.map(d => () =>
  agent(distillPrompt(d), { label: `distill:${d.slug}`, phase: 'Distill', schema: ABILITY_SCHEMA })
))

const ok = distilled.filter(Boolean)
const allAbilities = ok.flatMap(r => (r.abilities || []).map(a => ({ ...a, dungeon: r.dungeon })))
const bossCount = allAbilities.filter(a => a.source === 'boss').length
const trashCount = allAbilities.filter(a => a.source === 'trash').length
log(`Distill done: ${ok.length}/8 dungeons, ${allAbilities.length} abilities (${bossCount} boss / ${trashCount} trash). Signals confirmed: ${ok.filter(r=>r.signalsConfirmed).length}/8.`)

// ---- BARRIER: derive the taxonomy from the FULL pooled corpus (needs all 8 at once) ----
phase('Taxonomy')
const TAX_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    fileWritten: { type: 'string' },
    archetypes: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          slug: { type: 'string' },
          name: { type: 'string' },
          coveredAbilityCount: { type: 'integer' },
        },
        required: ['slug','name'],
      },
    },
  },
  required: ['fileWritten','archetypes'],
}

const corpus = JSON.stringify(allAbilities, null, 0)
const taxPrompt = `You are deriving an EMPIRICAL mechanic-archetype taxonomy for a Midnight Season 1 Mythic+ trainer, from the ACTUAL abilities found across all 8 dungeons (boss AND trash). Do not invent categories the dungeons don't use; do not miss ones they do. Work in ${REPO}.

Here is the full pooled ability corpus (${allAbilities.length} abilities, each: name, owner, dungeon, source boss|trash, mechanicWord, consequenceTier, role):
${corpus}

TASK:
1. Cluster these into ~15-20 archetypes (the "alphabet"). Merge synonyms from the provisional mechanicWords into one canonical slug each (kebab-case, e.g. interruptible-cast, frontal-cone, ground-void-zone, stack-up, spread-out, soak, dispel, kill-priority-add, tank-buster, knockback, fixate-chase, ...). EVERY ability in the corpus must fall under exactly one archetype — if something doesn't fit the obvious set, make a real archetype for it rather than forcing it.
2. Seed naming/voice from the existing KB: read ${REPO}/knowledge/endgame/delves/sunkiller-sanctum.md and ${REPO}/knowledge/endgame/delves/gulf-of-memory.md for the table voice and the archetype words already in use.
3. WRITE ${TAXONOMY_FILE} with full front matter:
---
title: M+ Mechanic Archetypes (Midnight S1)
patch: 12.0.5
fetched: ${FETCHED}
sources:
  - Derived from the 8 Midnight S1 M+ dungeon files in knowledge/endgame/mythic-plus/ (boss + trash corpus)
confidence: high
---
Then one entry per archetype, each with: \`slug\`, name, **Tell** (what you see), **Response** (default what you do), typical **consequence tier** (🔴 wipe / 🟠 your death / 🔵 your job / ⚪ flavor), **Role** relevance (DPS/healer/tank), and 1-2 real example abilities WITH the dungeon cited (drawn from the corpus). Add a one-line **diagram idea** per archetype (feeds the trainer's visual Archetype mode). Note that trash abilities are first-class — the taxonomy must cover them.
4. Include a short header line stating the taxonomy is derived from the real boss+trash corpus of all 8 S1 dungeons.

RETURN: fileWritten (abs path) and the archetypes list (slug + name + how many corpus abilities each covers). The slugs you choose become canonical for the tagging stage, so make them clean and final.`

const taxonomy = await agent(taxPrompt, { label: 'derive-taxonomy', phase: 'Taxonomy', schema: TAX_SCHEMA })
const slugList = (taxonomy?.archetypes || []).map(a => a.slug).join(', ')
log(`Taxonomy written with ${taxonomy?.archetypes?.length || 0} archetypes: ${slugList}`)

// ---- STAGE 2: back-fill canonical slugs + assert coverage, per dungeon (parallel) ----
phase('Tag')
const COVERAGE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    allMapped: { type: 'boolean' },
    abilityCount: { type: 'integer' },
    unmapped: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: { ability: { type: 'string' }, reason: { type: 'string' } },
        required: ['ability','reason'],
      },
    },
    newArchetypesSuggested: { type: 'array', items: { type: 'string' } },
  },
  required: ['dungeon','allMapped','abilityCount','unmapped'],
}

const tagPrompt = (d) => `Finalize archetype tagging for ${KB}/${d.slug}.md (the ${d.name} M+ file you/another agent just wrote). Work in ${REPO}.

1. Read the canonical taxonomy at ${TAXONOMY_FILE} — the available archetype slugs are: ${slugList}.
2. Read ${KB}/${d.slug}.md. Replace every provisional word in the **Archetype** column (boss tables) AND every trash-ability archetype tag with the matching canonical slug from the taxonomy. Trash abilities are first-class — they must be tagged too, not just bosses.
3. COVERAGE ASSERTION: every distinct ability in the file (boss AND trash) must map to exactly ONE canonical slug. If an ability genuinely fits none, do NOT force it — leave a clearly-marked \`<!-- UNMAPPED: needs archetype -->\` tag next to it and report it in \`unmapped\` + suggest a new archetype slug in \`newArchetypesSuggested\`.
4. Sanity: the file must still have a populated **Trash** section and a **Route** section. If either is missing, report it as an unmapped/structural problem in notes via the unmapped list (reason="structural: missing trash/route").
5. Save the file.

RETURN: dungeon, allMapped (true iff every ability now carries a valid canonical slug), abilityCount, unmapped[], newArchetypesSuggested[].`

const coverage = await parallel(DUNGEONS.map(d => () =>
  agent(tagPrompt(d), { label: `tag:${d.slug}`, phase: 'Tag', schema: COVERAGE_SCHEMA })
))

const cov = coverage.filter(Boolean)
const totalUnmapped = cov.flatMap(c => c.unmapped || [])
const fullyMapped = cov.filter(c => c.allMapped).length

return {
  distilled: ok.map(r => ({ dungeon: r.dungeon, file: r.fileWritten, abilities: r.abilities?.length, signals: r.signalsConfirmed, confidence: r.confidence, notes: r.notes })),
  taxonomy: { file: taxonomy?.fileWritten, archetypeCount: taxonomy?.archetypes?.length, slugs: taxonomy?.archetypes?.map(a => a.slug) },
  coverage: { fullyMapped, of: cov.length, totalAbilities: cov.reduce((s,c)=>s+(c.abilityCount||0),0), unmapped: totalUnmapped, newArchetypesSuggested: [...new Set(cov.flatMap(c=>c.newArchetypesSuggested||[]))] },
}

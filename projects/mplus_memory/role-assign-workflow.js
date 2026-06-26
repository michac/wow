export const meta = {
  name: 'mplus-role-assign',
  description: 'Per-ability role-classification pass over the BOSS tables: blind Sonnet assigns role (all|tank|healer|dps) from the captured "What it does/Do" text + cached Icy Veins/Method guides, Opus adjudicates against the archetype RoleTag prior with a confidence + source quote, emits findings + a low-confidence review report',
  phases: [
    { title: 'Extract', detail: 'one agent per dungeon: read the ## Bosses tables into structured rows' },
    { title: 'Classify', detail: 'one Sonnet agent per dungeon: who reacts? role + optional secondary, grounded in the Do text + the cached guides', model: 'sonnet' },
    { title: 'Adjudicate', detail: 'one Opus agent per dungeon: settle final role vs the archetype RoleTag prior, score confidence', model: 'opus' },
  ],
}

const REPO = '/home/mchristiansen/code/fun/wow'
const KB = `${REPO}/knowledge/endgame/mythic-plus`
const PAGES = `${REPO}/raw/pages`
const TAXONOMY_FILE = `${REPO}/knowledge/systems/mechanic-archetypes.md`

// The legal role enum — matches FilterSheet's buttons + store.settings.role.
const ROLES = 'all, tank, healer, dps'

// Archetype → documented RoleTag prior (mirrors the `- **RoleTag:**` bullets in
// mechanic-archetypes.md). The classifier's evidence (the Do text) overrides
// this; the prior only breaks genuine ties and is the build's blank-cell fallback.
const ROLE_TAG = {
  'interruptible-cast': 'all', 'ground-void-zone': 'all', 'tank-buster': 'tank',
  'spread-out': 'all', 'dispel': 'all', 'kill-priority-add': 'all', 'frontal-cone': 'all',
  'knockback': 'all', 'soak': 'all', 'raid-damage': 'healer', 'stack-up': 'all',
  'fixate-chase': 'all', 'purge-soothe': 'all', 'positional-gimmick': 'all',
  'heal-absorb': 'healer', 'charge': 'all', 'proximity-bait': 'all', 'pulsing-aura': 'all',
  'burn-window': 'dps', 'balance-kill': 'all', 'flavor': 'all',
}
const priorFor = (archetypeCell) => {
  const primary = (archetypeCell || '').split(';')[0].toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
  return ROLE_TAG[primary] || 'all'
}

const DUNGEONS = [
  { slug: 'magisters-terrace', name: "Magisters' Terrace" },
  { slug: 'maisara-caverns', name: 'Maisara Caverns' },
  { slug: 'nexus-point-xenas', name: 'Nexus-Point Xenas' },
  { slug: 'windrunner-spire', name: 'Windrunner Spire' },
  { slug: 'algethar-academy', name: "Algeth'ar Academy" },
  { slug: 'seat-of-the-triumvirate', name: 'Seat of the Triumvirate' },
  { slug: 'skyreach', name: 'Skyreach' },
  { slug: 'pit-of-saron', name: 'Pit of Saron' },
]
const guidesFor = (slug) => [
  `${PAGES}/www-icy-veins-com-wow-${slug}-dungeon-guide.md`,
  `${PAGES}/www-method-gg-guides-dungeons-${slug}.md`,
]

const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
const rowKey = (boss, spell) => `${norm(boss)}::${norm(spell)}`

// ── Phase: Extract — one agent per dungeon reads the ## Bosses tables ─────────
const EXTRACT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    slug: { type: 'string' },
    bosses: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          boss: { type: 'string', description: 'the boss `### <name>` heading this row sits under, with any `<!-- enc:NNN -->` marker stripped, verbatim otherwise' },
          spell: { type: 'string', description: 'Ability cell, verbatim (strip surrounding bold but keep wording incl. any "→"/"/")' },
          whatItDoes: { type: 'string', description: 'the "What it does" cell, verbatim' },
          do: { type: 'string', description: 'the "Do" cell, verbatim — this is the key role evidence (who reacts)' },
          archetype: { type: 'string', description: 'the Archetype cell, verbatim (may be "primary; secondary")' },
          tier: { type: 'string', description: 'the Tier emoji' },
          currentRole: { type: 'string', description: 'the existing Role cell if the row already has one (only Algeth\'ar does), else ""' },
        },
        required: ['boss', 'spell', 'whatItDoes', 'do', 'archetype'],
      },
    },
  },
  required: ['dungeon', 'slug', 'bosses'],
}

const extractPrompt = (d) => `Extract the BOSS ability tables from ${KB}/${d.slug}.md (the ${d.name} M+ file) into structured rows. Pure extraction — copy cells verbatim, classify nothing, change nothing on disk.

Read the file. Under the \`## Bosses\` section there are several \`### <BossName>\` headings, each with a table \`| Ability | What it does | Do | Archetype | Tier |\` (Algeth'ar's rows carry a stray 6th Role cell — capture it as currentRole). For EVERY boss and EVERY ability row return: boss (the \`### <name>\` heading with the \`<!-- enc:NNN -->\` marker removed), spell (Ability cell), whatItDoes, do, archetype, tier, currentRole (the 6th cell if present else "").

Rules:
- Copy text verbatim; you may strip surrounding markdown bold/italic but keep all wording (including "→", "/", parentheticals). Do NOT summarize.
- Ignore the \`## Trash\` section entirely (this pass is bosses only). Include every boss row, including ⚪ flavor rows.

RETURN: dungeon (name), slug, bosses[] each row with boss + spell + whatItDoes + do + archetype + tier + currentRole.`

phase('Extract')
const extracted = await parallel(DUNGEONS.map((d) => () =>
  agent(extractPrompt(d), { label: `extract:${d.slug}`, phase: 'Extract', schema: EXTRACT_SCHEMA })
))

const dungeons = []
for (let i = 0; i < extracted.length; i++) {
  const r = extracted[i]
  if (!r) continue
  dungeons.push({ dungeon: r.dungeon, slug: DUNGEONS[i].slug, name: DUNGEONS[i].name, rows: r.bosses || [] })
}
log(`Extract: ${dungeons.reduce((n, d) => n + d.rows.length, 0)} boss rows across ${dungeons.length}/8 dungeons.`)

// ── Pipeline: Classify (Sonnet, evidence-grounded) → Adjudicate (Opus) ───────
const CLASSIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    tags: {
      type: 'array',
      description: 'one entry per boss ability row',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          boss: { type: 'string', description: 'boss name, copied verbatim from the input' },
          spell: { type: 'string', description: 'ability name, copied verbatim from the input' },
          role: { type: 'string', description: 'the ONE role whose JOB this ability is: all | tank | healer | dps' },
          secondary: {
            type: 'array',
            description: 'rare — a second role that genuinely also has a distinct job here (e.g. a tank-buster the healer must also top). Usually empty. Never include "all".',
            items: { type: 'string' },
          },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'], description: 'low = the source text is silent/ambiguous on who reacts; a human should spot-check' },
          sourceQuote: { type: 'string', description: 'a short phrase quoted from the Do text or a guide that names who reacts (e.g. "Tank presses a defensive", "everyone pre-mitigates", "healers dispel"). "" if you had to infer.' },
          justification: { type: 'string', description: 'one line: why this role' },
        },
        required: ['boss', 'spell', 'role', 'secondary', 'confidence', 'sourceQuote', 'justification'],
      },
    },
  },
  required: ['dungeon', 'tags'],
}

const classifyPrompt = (d) => {
  const rows = d.rows.map((a) => ({ boss: a.boss, spell: a.spell, whatItDoes: a.whatItDoes, do: a.do, archetype: a.archetype, tier: a.tier || '' }))
  const [iv, method] = guidesFor(d.slug)
  return `You assign the player ROLE for each BOSS ability of one M+ dungeon: **${d.name}** (Midnight S1). The role answers "whose JOB is reacting to this?" under a strict drill-your-job model. Legal roles: ${ROLES}.

Role rubric:
- **tank** — the tank is the one who must act: tank-busters, big melee/bleeds aimed at the threat-holder, frontal facing control, an add the tank must grab. (A heavy tank hit the healer must heal *through* still counts as the TANK's mechanic unless the player who acts is genuinely the healer.)
- **healer** — the healer is the one who must act: heavy raid spikes the healer triages, heal-absorbs, lethal dispels the healer cleanses, sustained ramps the healer rides. Use only when reacting is genuinely the healer's job, not just "damage happens and gets healed".
- **dps** — the job lands on DPS specifically: a burn/execute window to pour cooldowns into, a kill-priority swap that is a DPS race.
- **all** — everyone has the same job: dodge the void zone, soak the orb, spread, stack, break LoS, use a personal defensive through unavoidable raid damage, interrupt (anyone with a kick). **This is the default and the most common answer** — most mechanics are everyone's job.

Evidence, in priority order:
1. The **Do** cell — it usually names who reacts ("Tank...", "Healer...", "everyone...", "DPS..."). Quote it.
2. The cached guides for this dungeon (read them, search for the ability + role words): ${iv} and ${method}.
3. Read the taxonomy + each archetype's role intent at ${TAXONOMY_FILE} as background.

Pick the role from the EVIDENCE, not from a per-archetype default — the whole point is to catch per-ability nuance (e.g. a knockback that hits only the tank → tank, while a knockback that hits everyone → all). Prefer **all** whenever more than one role genuinely shares the job. Add a **secondary** role only when a second role has its own distinct, non-trivial job (rare; never "all"). Set confidence **low** when the text is silent on who reacts.

Boss ability rows:
${JSON.stringify(rows, null, 0)}

For EVERY row return: boss (verbatim), spell (verbatim), role, secondary[], confidence, sourceQuote, justification. RETURN: dungeon, tags[].`
}

const ADJ_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    decisions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          boss: { type: 'string' },
          spell: { type: 'string' },
          finalRole: { type: 'string', description: 'the chosen role: all | tank | healer | dps' },
          finalSecondary: { type: 'array', items: { type: 'string' }, description: 'confirmed secondary roles (may be empty; never "all")' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
          changedFromPrior: { type: 'boolean', description: 'true if finalRole differs from the archetype RoleTag prior shown' },
          reason: { type: 'string', description: 'one line: why this role, citing the evidence' },
        },
        required: ['boss', 'spell', 'finalRole', 'finalSecondary', 'confidence', 'changedFromPrior', 'reason'],
      },
    },
  },
  required: ['dungeon', 'decisions'],
}

phase('Classify')
const reviewed = await pipeline(
  dungeons,
  (d) => agent(classifyPrompt(d), { label: `classify:${d.slug}`, phase: 'Classify', model: 'sonnet', schema: CLASSIFY_SCHEMA }),
  async (blind, d) => {
    const byKey = new Map(d.rows.map((a) => [rowKey(a.boss, a.spell), a]))
    const items = []
    for (const t of (blind?.tags || [])) {
      const cur = byKey.get(rowKey(t.boss, t.spell))
      if (!cur) continue
      const prior = priorFor(cur.archetype)
      items.push({
        boss: cur.boss, spell: cur.spell, do: cur.do, archetype: cur.archetype, tier: cur.tier || '',
        archetypeRolePrior: prior,
        sonnetRole: t.role, sonnetSecondary: t.secondary || [], sonnetConfidence: t.confidence,
        sonnetSourceQuote: t.sourceQuote || '', sonnetWhy: t.justification,
      })
    }
    let decisions = []
    if (items.length) {
      const [iv, method] = guidesFor(d.slug)
      const adjPrompt = `You are the adjudicator assigning the player ROLE for the BOSS abilities of **${d.name}** (Midnight S1). A blind classifier proposed a role per ability from the Do text + guides. For each row settle the FINAL role (all | tank | healer | dps), any genuine secondary role, a confidence, and whether it differs from the archetype's documented RoleTag prior.

Each row carries: the Do text, the archetype, the **archetypeRolePrior** (the documented default for that archetype), and the blind classifier's call + its source quote. The prior is only a tie-breaker — when the Do text clearly names who reacts, the EVIDENCE wins even against the prior (that is exactly the per-ability nuance we want, e.g. a knockback that hits only the tank → tank though the prior is "all"; raid damage everyone defensives through → "all" though the prior is "healer"). Reserve **healer**/**dps**/**tank** for abilities whose job genuinely lands on that one role; default to **all** when the job is shared. Set confidence **low** for genuine judgment calls. You may consult ${iv} and ${method} and the taxonomy at ${TAXONOMY_FILE}.

Rows:
${JSON.stringify(items, null, 0)}

For each row return: boss (verbatim), spell (verbatim), finalRole, finalSecondary[], confidence, changedFromPrior, reason. RETURN: dungeon, decisions[].`
      const adj = await agent(adjPrompt, { label: `adjudicate:${d.slug}`, phase: 'Adjudicate', model: 'opus', schema: ADJ_SCHEMA })
      decisions = adj?.decisions || []
    }
    return { ...d, items, decisions }
  }
)

// ── Assemble findings + the report ──────────────────────────────────────────
const ok = reviewed.filter(Boolean)
const decFor = (r, boss, spell) => (r.decisions || []).find((dc) => rowKey(dc.boss, dc.spell) === rowKey(boss, spell))
const code = (s) => `\`${s}\``
const VALID = new Set(['all', 'tank', 'healer', 'dps'])
const cleanRole = (s) => {
  const v = (s || '').toLowerCase().trim()
  return VALID.has(v) ? v : 'all'
}

const findings = [] // flat, drives the apply step: {slug, boss, spell, role, secondary[], confidence, changedFromPrior, prior, source}
let nHigh = 0, nLow = 0, nChanged = 0
const reportRows = [] // low-confidence + changed-from-prior, for human review

for (const d of DUNGEONS) {
  const r = ok.find((x) => x.slug === d.slug)
  if (!r) continue
  for (const it of (r.items || [])) {
    const dec = decFor(r, it.boss, it.spell)
    const role = cleanRole(dec?.finalRole || it.sonnetRole)
    const secondary = (dec?.finalSecondary || it.sonnetSecondary || [])
      .map(cleanRole).filter((s) => s !== 'all' && s !== role)
    const confidence = dec?.confidence || it.sonnetConfidence || 'medium'
    const changedFromPrior = typeof dec?.changedFromPrior === 'boolean' ? dec.changedFromPrior : (role !== it.archetypeRolePrior)
    const source = it.sonnetSourceQuote || ''
    if (confidence === 'high') nHigh++; else nLow++
    if (changedFromPrior) nChanged++
    findings.push({ slug: d.slug, boss: it.boss, spell: it.spell, role, secondary, confidence, changedFromPrior, prior: it.archetypeRolePrior, source, reason: dec?.reason || it.sonnetWhy })
    if (confidence !== 'high' || changedFromPrior) {
      reportRows.push({ slug: d.slug, dungeon: d.name, boss: it.boss, spell: it.spell, role, secondary, prior: it.archetypeRolePrior, confidence, changedFromPrior, source, reason: dec?.reason || it.sonnetWhy })
    }
  }
}

const lines = []
lines.push('# M+ Boss Role-Assignment Report')
lines.push('')
lines.push('_Generated by `role-assign-workflow.js`. Scope: the boss tables of all 8 S1 dungeons (trash roles were normalized deterministically from their existing, already-sourced Role cells; see the plan)._')
lines.push('')
lines.push(`**Summary:** ${findings.length} boss abilities classified · ${nHigh} high-confidence · ${nLow} medium/low (listed below) · ${nChanged} differ from the archetype RoleTag prior.`)
lines.push('')
lines.push('Method: per dungeon, a **blind Sonnet** pass assigned a role from the captured "Do" text + the cached Icy Veins/Method guides; an **Opus** adjudicator settled the final role against the archetype RoleTag prior with a confidence and a source quote. High-confidence rows were applied directly to the KB boss tables. Spot-check the rows below against the cited source before treating the data as final.')
lines.push('')
lines.push('## Rows to review (medium/low confidence, or changed from the archetype prior)')
lines.push('')
lines.push('| Dungeon | Boss | Ability | role (+secondary) | prior | conf | Δprior | source quote / reason | ✓ |')
lines.push('|---|---|---|---|---|---|---|---|---|')
for (const x of reportRows) {
  const roleCell = code(x.role) + (x.secondary.length ? ' · also ' + x.secondary.map(code).join(', ') : '')
  const ev = (x.source ? `"${x.source}" — ` : '') + (x.reason || '')
  lines.push(`| ${x.dungeon} | ${x.boss} | ${x.spell} | ${roleCell} | ${code(x.prior)} | ${x.confidence} | ${x.changedFromPrior ? 'yes' : ''} | ${ev.replace(/\|/g, '\\|')} | [ ] |`)
}
lines.push('')

const reportMarkdown = lines.join('\n') + '\n'
log(`Report assembled: ${findings.length} classified, ${nLow} to review, ${nChanged} changed from prior.`)

return {
  reportMarkdown,
  reportPath: `${REPO}/projects/mplus_memory/role-assign-report.md`,
  findingsPath: `${REPO}/projects/mplus_memory/role-assign-findings.json`,
  findings,
  summary: { classified: findings.length, high: nHigh, lowMed: nLow, changed: nChanged },
}

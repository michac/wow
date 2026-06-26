export const meta = {
  name: 'mplus-reclassify-trash',
  description: 'Per-dungeon second-opinion pass over TRASH tables: blind re-classify every trash ability + flag cast/effect merges, Opus tie-breaks disagreements with a confidence score, emit a markup-ready report',
  phases: [
    { title: 'Extract', detail: 'one agent per dungeon: read the ## Trash tables into structured rows' },
    { title: 'Classify', detail: "one Sonnet agent per dungeon: blind primary + also-valid secondary tags (archetype column stripped) + detect cast/effect merges", model: 'sonnet' },
    { title: 'Adjudicate', detail: 'one Opus agent per dungeon: settle final primary + secondary + confidence for abilities whose primary moved or that gained a secondary', model: 'opus' },
  ],
}

const REPO = '/home/mchristiansen/code/fun/wow'
const KB = `${REPO}/knowledge/endgame/mythic-plus`
const TAXONOMY_FILE = `${REPO}/knowledge/systems/mechanic-archetypes.md`

// The 21 canonical slugs — the only legal archetype values (kept in sync with
// mechanic-archetypes.md; the build asserts every tag ∈ this set).
const SLUGS = 'interruptible-cast, ground-void-zone, tank-buster, spread-out, dispel, kill-priority-add, frontal-cone, knockback, soak, raid-damage, stack-up, fixate-chase, purge-soothe, positional-gimmick, heal-absorb, charge, proximity-bait, pulsing-aura, burn-window, balance-kill, flavor'

// Dungeons (names verbatim from the dungeon files / journal). This pass is the
// trash tables only — the 29 bosses were handled by reclassify-workflow.js.
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

const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
// A trash row is keyed on Mob + Ability (a mob can repeat across wings; an
// ability name can repeat across mobs). Both together are unique per dungeon.
const rowKey = (mob, ability) => `${norm(mob)}::${norm(ability)}`

// ── Phase: Extract — one agent per dungeon reads the ## Trash tables ──────────
const EXTRACT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    slug: { type: 'string' },
    trash: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          wing: { type: 'string', description: 'the `### <wing>` heading this row sits under, verbatim (drop the leading ###)' },
          mob: { type: 'string', description: 'Mob cell, verbatim' },
          ability: { type: 'string', description: 'Ability cell, verbatim (strip surrounding bold but keep wording, incl. any parenthetical)' },
          seeDo: { type: 'string', description: 'the combined "See → Do" cell, verbatim (keep the → and any inline _(… only)_ flag)' },
          tier: { type: 'string', description: 'the Tier emoji (🔴/🟠/🔵/⚪)' },
          role: { type: 'string', description: 'the Role cell, verbatim' },
          currentArchetype: { type: 'string', description: 'the current Archetype cell slug, verbatim' },
        },
        required: ['wing', 'mob', 'ability', 'seeDo', 'currentArchetype'],
      },
    },
  },
  required: ['dungeon', 'slug', 'trash'],
}

const extractPrompt = (d) => `Extract the TRASH ability table from ${KB}/${d.slug}.md (the ${d.name} M+ file) into structured rows. This is pure extraction — copy cells verbatim, classify nothing, change nothing on disk.

Read the file. Under the \`## Trash\` section there are one or more \`### <wing>\` headings, each followed by a 6-column table: \`| Mob | Ability | See → Do | Archetype | Tier | Role |\`. For EVERY wing and EVERY row return: wing (the \`### <wing>\` heading text), mob (Mob cell), ability (Ability cell), seeDo (the combined "See → Do" cell), tier (the Tier emoji), role (Role cell), and currentArchetype (the Archetype cell, e.g. "stack-up").

Rules:
- Copy text verbatim (you may strip surrounding markdown bold/italic from the cell, but keep the wording, including any parenthetical like "(CC-immune)" or any inline \`_(Method-only)_\` flag in the seeDo cell). Do NOT summarize.
- Include ALL trash rows across ALL wings — do not skip "flavor" rows. Ignore the \`## Bosses\` section entirely (this pass is trash only). There are no \`<!-- enc -->\` markers in trash.

RETURN: dungeon (name), slug, trash[] each row with wing + mob + ability + seeDo + tier + role + currentArchetype.`

phase('Extract')
const extracted = await parallel(DUNGEONS.map((d) => () =>
  agent(extractPrompt(d), { label: `extract:${d.slug}`, phase: 'Extract', schema: EXTRACT_SCHEMA })
))

// Build a per-dungeon work-list. Barrier needed: we need every dungeon before
// we pipeline (and the report groups by dungeon).
const dungeons = []
for (let i = 0; i < extracted.length; i++) {
  const r = extracted[i]
  if (!r) continue
  dungeons.push({ dungeon: r.dungeon, slug: DUNGEONS[i].slug, name: DUNGEONS[i].name, rows: r.trash || [] })
}
log(`Extract: ${dungeons.reduce((n, d) => n + d.rows.length, 0)} trash rows across ${dungeons.length}/8 dungeons.`)

// ── Pipeline: Classify (Sonnet, blind) → Adjudicate (Opus, disagreements) ────
const CLASSIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    dungeon: { type: 'string' },
    merges: {
      type: 'array',
      description: 'cast+lingering-effect (or cast+debuff) pairs on the SAME mob that are ONE in-game tell and should become one card (rarer in trash than bosses, but still flag genuine ones)',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          mob: { type: 'string', description: 'the mob these two rows belong to (both rows must be the same mob)' },
          keepCast: { type: 'string', description: 'the ability name to KEEP (the cast / primary tell)' },
          dropRow: { type: 'string', description: 'the ability name to DROP (the lingering zone/DoT row folded away)' },
          mergedSeeDo: { type: 'string', description: "the kept row's See → Do after folding in the dropped row's \"don't stand in it\" response" },
          reason: { type: 'string', description: 'why these are one mechanic' },
        },
        required: ['mob', 'keepCast', 'dropRow', 'mergedSeeDo', 'reason'],
      },
    },
    tags: {
      type: 'array',
      description: 'one entry per trash row — your INDEPENDENT archetype call (primary + any also-valid)',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          mob: { type: 'string', description: 'mob name, copied verbatim from the input' },
          ability: { type: 'string', description: 'ability name, copied verbatim from the input' },
          primary: { type: 'string', description: 'the ONE canonical slug for the response a player reacts to first/most' },
          secondary: {
            type: 'array',
            description: 'also-valid canonical slugs (usually empty) — only genuine co-responses a competent player would actually give; NOT loosely-related slugs',
            items: {
              type: 'object', additionalProperties: false,
              properties: {
                slug: { type: 'string' },
                why: { type: 'string', description: 'the second distinct response this slug captures' },
              },
              required: ['slug', 'why'],
            },
          },
          justification: { type: 'string', description: 'one line: the player RESPONSE that picks the primary slug' },
        },
        required: ['mob', 'ability', 'primary', 'secondary', 'justification'],
      },
    },
  },
  required: ['dungeon', 'merges', 'tags'],
}

const classifyPrompt = (d) => {
  // Strip the current archetype so the classification is genuinely blind.
  const blindRows = d.rows.map((a) => ({
    wing: a.wing, mob: a.mob, ability: a.ability, seeDo: a.seeDo, tier: a.tier || '', role: a.role || '',
  }))
  return `You are giving an INDEPENDENT second opinion on the mechanic archetypes for the TRASH of one M+ dungeon: **${d.name}** (Midnight S1). Read the hardened taxonomy first, then classify — you are NOT shown the existing tags, so call each ability on its own merits.

1. Read the canonical taxonomy + tagging rules at ${TAXONOMY_FILE}. The only legal slugs are: ${SLUGS}. Pay attention to the **Tagging rules** header (cast+effect de-dup; classify by RESPONSE not surface words) and each slug's **Not this if** guard.

Here is the full trash table for this dungeon (all wings, so you can see cast→effect relationships and keep a repeated mob consistent across wings). Each row has: wing, mob, ability, seeDo (the combined "See → Do" cell — trash merges what bosses split into "what it does" + "do"), tier, role. The current Archetype column has been withheld on purpose:
${JSON.stringify(blindRows, null, 0)}

DO TWO THINGS:

A) MERGE DETECTION. Per the cast+effect de-dup rule, find pairs ON THE SAME MOB where a *cast* and a *lingering zone/DoT/pool it creates* are listed as two rows but are really ONE in-game tell. This is rarer in trash than on bosses — only flag genuine cast→its-own-effect pairs on the same mob; do NOT merge two independent abilities or abilities from different mobs. For each: mob, keepCast = the cast/primary tell to keep, dropRow = the lingering-effect row to fold away, mergedSeeDo = the kept row's See → Do with the dropped row's "don't stand in it" instruction folded in (preserve any inline _(… only)_ flag), reason = why they're one mechanic. Return [] if none.

B) BLIND TAGS (multi-tag aware). For EVERY row in the table, assign a **primary** canonical slug — the response a player reacts to first/most — and a one-line justification naming that response. Then, per Tagging rule 3, add **secondary** slugs ONLY when the same tell legitimately demands a second distinct response that forcing one answer would mark wrong. Most abilities have NO secondary — leave secondary=[] unless a second response is one a competent player would genuinely give. Never pad with loosely-related slugs. The role/tier columns are extra signal. Use the mob + ability names verbatim. Tag every row (including ones you proposed to merge — tag them as they stand). Watch for the known defects: pulsing/constant AoEs mis-tagged \`stack-up\` (should usually be \`pulsing-aura\` or \`raid-damage\` — there is no converge-to-split response), and personal stacking DoTs mis-tagged \`stack-up\`.

RETURN: dungeon, merges[], tags[] (one per row, each with mob + ability + primary + secondary[]).`
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
          mob: { type: 'string' },
          ability: { type: 'string' },
          finalPrimary: { type: 'string', description: 'the chosen primary canonical slug' },
          finalSecondary: { type: 'array', items: { type: 'string' }, description: 'confirmed also-valid slugs (may be empty); prune any that are not genuine co-responses' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'], description: 'how confident this final tagging is — low = genuinely ambiguous / a judgment call worth a human spot-check' },
          reason: { type: 'string', description: 'one line: why this primary, and why each secondary survives (or was pruned)' },
        },
        required: ['mob', 'ability', 'finalPrimary', 'finalSecondary', 'confidence', 'reason'],
      },
    },
  },
  required: ['dungeon', 'decisions'],
}

phase('Classify')
const reviewed = await pipeline(
  dungeons,
  // Stage A — blind classify + merge detect (Sonnet)
  (d) => agent(classifyPrompt(d), { label: `classify:${d.slug}`, phase: 'Classify', model: 'sonnet', schema: CLASSIFY_SCHEMA }),
  // Stage B — Opus adjudicates anything "interesting": primary ≠ current, OR a
  // secondary (also-valid) tag was proposed. Pure primary==current & no-secondary
  // rows pass through unchanged.
  async (blind, d) => {
    const byKey = new Map(d.rows.map((a) => [rowKey(a.mob, a.ability), a]))
    const dropped = new Set((blind?.merges || []).map((m) => rowKey(m.mob, m.dropRow)))
    const items = []
    let unchanged = 0
    for (const t of (blind?.tags || [])) {
      const cur = byKey.get(rowKey(t.mob, t.ability))
      if (!cur) continue
      if (dropped.has(rowKey(t.mob, t.ability))) continue // folded away by a merge; tag is moot
      const sec = (t.secondary || [])
      const primaryDiffers = norm(cur.currentArchetype) !== norm(t.primary)
      if (!primaryDiffers && sec.length === 0) { unchanged++; continue }
      items.push({
        mob: cur.mob,
        ability: cur.ability,
        seeDo: cur.seeDo,
        tier: cur.tier || '',
        role: cur.role || '',
        currentTag: cur.currentArchetype,
        blindPrimary: t.primary,
        blindPrimaryWhy: t.justification,
        blindSecondary: sec, // [{slug, why}]
      })
    }

    let decisions = []
    if (items.length) {
      const adjPrompt = `You are the adjudicator on archetype tagging for the TRASH of the M+ dungeon **${d.name}** (Midnight S1). A blind second-opinion classifier (multi-tag aware) proposed a primary archetype and sometimes one or more also-valid secondaries for the trash rows below; each currently carries a single tag. For each row, settle the FINAL tagging: pick the final **primary** slug (the response reacted to first/most — may be the current tag or the blind primary), the final set of **secondary** also-valid slugs (confirm only genuine second responses; prune anything loosely-related or redundant — most rows should end with no secondary), and a **confidence** (high | medium | low) for how sure you are. Use **low** for genuine judgment calls a human should spot-check.

Read the canonical taxonomy + tagging rules at ${TAXONOMY_FILE} (only legal slugs: ${SLUGS}; mind each slug's **Not this if** guard, Tagging rule 3 on multi-tag, and classify by the player RESPONSE not surface words). The seeDo cell is the combined "See → Do" text; role/tier are extra signal.

Rows:
${JSON.stringify(items, null, 0)}

For each row return: mob (verbatim), ability (verbatim), finalPrimary, finalSecondary[] (slugs, possibly empty), confidence (high|medium|low), reason (one line covering the primary choice and why each secondary survives or was pruned). RETURN: dungeon, decisions[].`
      const adj = await agent(adjPrompt, { label: `adjudicate:${d.slug}`, phase: 'Adjudicate', model: 'opus', schema: ADJ_SCHEMA })
      decisions = adj?.decisions || []
    }
    return { ...d, merges: blind?.merges || [], items, decisions, unchanged }
  }
)

// ── Assemble findings + the markup-ready report ─────────────────────────────
const ok = reviewed.filter(Boolean)
const decFor = (r, mob, ability) => (r.decisions || []).find((dc) => rowKey(dc.mob, dc.ability) === rowKey(mob, ability))
const code = (s) => `\`${s}\``

let totalMerges = 0, totalPrimaryChanges = 0, totalMultiTag = 0, totalReviewedNoChange = 0, totalUnchanged = 0

// Resolve each adjudicated item to its final tagging + a display row.
function resolveItem(r, it) {
  const dec = decFor(r, it.mob, it.ability)
  const finalPrimary = dec?.finalPrimary || it.blindPrimary
  const finalSecondary = (dec?.finalSecondary || it.blindSecondary.map((s) => s.slug)).filter((s) => norm(s) !== norm(finalPrimary))
  const primaryChanged = norm(finalPrimary) !== norm(it.currentTag)
  const hasSecondary = finalSecondary.length > 0
  const confidence = dec?.confidence || 'medium'
  return { it, dec, finalPrimary, finalSecondary, primaryChanged, hasSecondary, confidence }
}

const lines = []
lines.push('# M+ Trash Re-classification Report — Second-Opinion Pass (multi-tag)')
lines.push('')
lines.push('_Generated by `reclassify-trash-workflow.js`. Scope: the trash tables of all 8 S1 dungeons (bosses were a prior run)._')
lines.push('')
lines.push('Method: per dungeon, a **blind Sonnet** pass re-tagged every trash row with the')
lines.push('Archetype column withheld — proposing a **primary** archetype plus any')
lines.push('**also-valid** secondaries — and flagged cast+lingering-effect pairs to merge;')
lines.push('an **Opus** adjudicator then settled the final primary + secondary set + a')
lines.push('confidence for every row whose primary moved or that gained a secondary.')
lines.push('')

// findings[] drives the apply step.
const findings = []
for (const d of DUNGEONS) {
  const r = ok.find((x) => x.slug === d.slug)
  if (!r) continue
  const merges = (r.merges || []).map((m) => {
    totalMerges++
    return { mob: m.mob, keepCast: m.keepCast, dropRow: m.dropRow, mergedSeeDo: m.mergedSeeDo, reason: m.reason }
  })
  const dropped = new Set(merges.map((m) => rowKey(m.mob, m.dropRow)))
  const changes = []
  for (const it of (r.items || [])) {
    if (dropped.has(rowKey(it.mob, it.ability))) continue
    const x = resolveItem(r, it)
    if (!x.primaryChanged && !x.hasSecondary) { totalReviewedNoChange++; continue }
    if (x.primaryChanged) totalPrimaryChanges++
    if (x.hasSecondary) totalMultiTag++
    changes.push({
      mob: it.mob, ability: it.ability,
      current: it.currentTag, finalPrimary: x.finalPrimary, finalSecondary: x.finalSecondary,
      confidence: x.confidence, reason: x.dec?.reason || it.blindPrimaryWhy,
    })
  }
  totalUnchanged += r.unchanged || 0
  findings.push({ dungeon: r.dungeon, slug: d.slug, merges, changes, unchanged: r.unchanged || 0 })
}

// Render the report body grouped by dungeon.
for (const f of findings) {
  const dname = DUNGEONS.find((d) => d.slug === f.slug)?.name || f.dungeon
  lines.push(`## ${dname}`)
  lines.push('')

  lines.push('**Merges** (cast + lingering-effect → one card):')
  lines.push('')
  if (f.merges.length) {
    for (const m of f.merges) {
      lines.push(`- [ ] **${m.mob}** — keep **${m.keepCast}** / drop **${m.dropRow}**`)
      lines.push(`  - merged See → Do: ${m.mergedSeeDo}`)
      lines.push(`  - why: ${m.reason}`)
    }
  } else {
    lines.push('_No merges found._')
  }
  lines.push('')

  lines.push('**Tag changes** (primary moved and/or secondary added; Opus-adjudicated):')
  lines.push('')
  if (f.changes.length) {
    lines.push('| Mob | Ability | current → final tags | conf | adjudicator reason | ✓ |')
    lines.push('|---|---|---|---|---|---|')
    for (const c of f.changes) {
      const primaryChanged = norm(c.finalPrimary) !== norm(c.current)
      const head = primaryChanged ? `${code(c.current)} → ${code(c.finalPrimary)}` : `${code(c.finalPrimary)} (kept)`
      const also = (c.finalSecondary || []).length ? ' · also ' + c.finalSecondary.map(code).join(', ') : ''
      const reason = (c.reason || '').replace(/\|/g, '\\|')
      lines.push(`| ${c.mob} | ${c.ability} | ${head}${also} | ${c.confidence} | ${reason} | [ ] |`)
    }
  } else {
    lines.push('_No tag changes._')
  }
  lines.push('')
  lines.push(`_Unchanged: ${f.unchanged} rows held their single tag._`)
  lines.push('')
}

const summary = `${ok.length} dungeons reviewed · ${totalMerges} merges proposed · ${totalPrimaryChanges} primary re-tags · ${totalMultiTag} rows gaining an also-valid secondary · ${totalUnchanged + totalReviewedNoChange} unchanged.`
lines.splice(3, 0, `**Summary:** ${summary}`, '')

const reportMarkdown = lines.join('\n') + '\n'
log(`Report assembled: ${summary}`)

return {
  reportMarkdown,
  reportPath: `${REPO}/projects/mplus_memory/reclassify-trash-report.md`,
  summary: { dungeons: ok.length, merges: totalMerges, primaryChanges: totalPrimaryChanges, multiTag: totalMultiTag, unchanged: totalUnchanged + totalReviewedNoChange },
  findings,
}

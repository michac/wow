export const meta = {
  name: 'mplus-reclassify',
  description: 'Per-boss second-opinion pass: blind re-classify every boss ability + flag cast/effect merges, Opus tie-breaks disagreements, emit a markup-ready report',
  phases: [
    { title: 'Extract', detail: 'one agent per dungeon: read the boss tables into structured rows' },
    { title: 'Classify', detail: 'one Sonnet agent per boss: blind primary + also-valid secondary tags (archetype column stripped) + detect cast/effect merges', model: 'sonnet' },
    { title: 'Adjudicate', detail: 'one Opus agent per boss: settle final primary + secondary set for abilities whose primary moved or that gained a secondary', model: 'opus' },
  ],
}

const REPO = '/home/mchristiansen/code/fun/wow'
const KB = `${REPO}/knowledge/endgame/mythic-plus`
const TAXONOMY_FILE = `${REPO}/knowledge/systems/mechanic-archetypes.md`

// The 21 canonical slugs — the only legal archetype values (kept in sync with
// mechanic-archetypes.md; the build asserts every tag ∈ this set).
const SLUGS = 'interruptible-cast, ground-void-zone, tank-buster, spread-out, dispel, kill-priority-add, frontal-cone, knockback, soak, raid-damage, stack-up, fixate-chase, purge-soothe, positional-gimmick, heal-absorb, charge, proximity-bait, pulsing-aura, burn-window, balance-kill, flavor'

// Boss roster per dungeon (names verbatim from the dungeon files / journal).
// Trash is a deliberate follow-up run — this pass is the 28 bosses only.
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

// ── Phase: Extract — one agent per dungeon reads the boss tables ─────────────
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
          name: { type: 'string', description: 'boss display name exactly as the ### heading reads (drop the <!-- enc --> marker)' },
          abilities: {
            type: 'array',
            items: {
              type: 'object', additionalProperties: false,
              properties: {
                name: { type: 'string', description: 'Ability cell, verbatim' },
                whatItDoes: { type: 'string', description: '"What it does" cell, verbatim' },
                doText: { type: 'string', description: '"Do" cell, verbatim' },
                tier: { type: 'string', description: 'the Tier emoji (🔴/🟠/🔵/⚪)' },
                currentArchetype: { type: 'string', description: 'the current Archetype cell slug, verbatim' },
              },
              required: ['name', 'whatItDoes', 'doText', 'currentArchetype'],
            },
          },
        },
        required: ['name', 'abilities'],
      },
    },
  },
  required: ['dungeon', 'slug', 'bosses'],
}

const extractPrompt = (d) => `Extract the BOSS ability tables from ${KB}/${d.slug}.md (the ${d.name} M+ file) into structured rows. This is pure extraction — copy cells verbatim, classify nothing, change nothing on disk.

Read the file. Under the \`## Bosses\` section, each boss is a \`### <name>\` heading followed by a 5-column table: \`| Ability | What it does | Do | Archetype | Tier |\`. For EVERY boss and EVERY ability row return: name (Ability cell), whatItDoes (What it does cell), doText (Do cell), tier (the Tier emoji), and currentArchetype (the Archetype cell, e.g. "ground-void-zone").

Rules:
- Strip the \`<!-- enc:NNN -->\` marker from boss names; return just the display name.
- Copy text verbatim (you may strip surrounding markdown bold/italic, but keep the wording). Do NOT summarize.
- Include ALL boss rows — do not skip "flavor" rows. Ignore the \`## Trash\` section entirely (this pass is bosses only).

RETURN: dungeon (name), slug, bosses[] each with name + abilities[].`

phase('Extract')
const extracted = await parallel(DUNGEONS.map((d) => () =>
  agent(extractPrompt(d), { label: `extract:${d.slug}`, phase: 'Extract', schema: EXTRACT_SCHEMA })
))

// Flatten to a flat boss work-list. Barrier needed: we need every boss before
// we can pipeline (and the report groups by dungeon).
const bosses = []
for (const r of extracted.filter(Boolean)) {
  for (const b of (r.bosses || [])) {
    bosses.push({ dungeon: r.dungeon, slug: r.slug, boss: b.name, abilities: b.abilities || [] })
  }
}
log(`Extract: ${bosses.length} bosses, ${bosses.reduce((n, b) => n + b.abilities.length, 0)} boss abilities across ${extracted.filter(Boolean).length}/8 dungeons.`)

// ── Pipeline: Classify (Sonnet, blind) → Adjudicate (Opus, disagreements) ────
const CLASSIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    boss: { type: 'string' },
    merges: {
      type: 'array',
      description: 'cast+lingering-effect (or cast+debuff) pairs that are ONE in-game tell and should become one card',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          keepCast: { type: 'string', description: 'the ability name to KEEP (the cast / primary tell)' },
          dropRow: { type: 'string', description: 'the ability name to DROP (the lingering zone/DoT row folded away)' },
          mergedReveal: { type: 'string', description: "the kept card's reveal after folding in the dropped row's \"don't stand in it\" response" },
          reason: { type: 'string', description: 'why these are one mechanic' },
        },
        required: ['keepCast', 'dropRow', 'mergedReveal', 'reason'],
      },
    },
    tags: {
      type: 'array',
      description: 'one entry per ability — your INDEPENDENT archetype call (primary + any also-valid)',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
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
        required: ['ability', 'primary', 'secondary', 'justification'],
      },
    },
  },
  required: ['boss', 'merges', 'tags'],
}

const classifyPrompt = (b) => {
  // Strip the current archetype so the classification is genuinely blind.
  const blindAbilities = b.abilities.map((a) => ({
    name: a.name, whatItDoes: a.whatItDoes, doText: a.doText, tier: a.tier || '',
  }))
  return `You are giving an INDEPENDENT second opinion on the mechanic archetypes for one M+ boss: **${b.boss}** (${b.dungeon}, Midnight S1). Read the hardened taxonomy first, then classify — you are NOT shown the existing tags, so call each ability on its own merits.

1. Read the canonical taxonomy + tagging rules at ${TAXONOMY_FILE}. The only legal slugs are: ${SLUGS}. Pay attention to the **Tagging rules** header (cast+effect de-dup; classify by RESPONSE not surface words) and each slug's **Not this if** guard.

Here is the full ability table for this boss (so you can see cast→effect relationships). The current Archetype column has been withheld on purpose:
${JSON.stringify(blindAbilities, null, 0)}

DO TWO THINGS:

A) MERGE DETECTION. Per the cast+effect de-dup rule, find pairs where a *cast* and a *lingering zone/DoT/pool it creates* are listed as two abilities but are really ONE in-game tell (e.g. a cast that drops a puddle, where the puddle is a separate row). For each: keepCast = the cast/primary tell to keep, dropRow = the lingering-effect row to fold away, mergedReveal = the kept card's response text with the dropped row's "don't stand in it" instruction folded in, reason = why they're one mechanic. Only flag genuine cast→its-own-effect pairs; do NOT merge two independent abilities. Return [] if none.

B) BLIND TAGS (multi-tag aware). For EVERY ability in the table, assign a **primary** canonical slug — the response a player reacts to first/most — and a one-line justification naming that response. Then, per Tagging rule 3, add **secondary** slugs ONLY when the same tell legitimately demands a second distinct response that forcing one answer would mark wrong (e.g. a tank-buster that *also* knocks back, a knockback that is *also* unavoidable raid damage). Most abilities have NO secondary — leave secondary=[] unless a second response is one a competent player would genuinely give. Never pad with loosely-related slugs. Use the ability name verbatim. Tag every row (including ones you proposed to merge — tag them as they stand).

RETURN: boss, merges[], tags[] (one per ability, each with primary + secondary[]).`
}

const ADJ_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    boss: { type: 'string' },
    decisions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          ability: { type: 'string' },
          finalPrimary: { type: 'string', description: 'the chosen primary canonical slug' },
          finalSecondary: { type: 'array', items: { type: 'string' }, description: 'confirmed also-valid slugs (may be empty); prune any that are not genuine co-responses' },
          reason: { type: 'string', description: 'one line: why this primary, and why each secondary survives (or was pruned)' },
        },
        required: ['ability', 'finalPrimary', 'finalSecondary', 'reason'],
      },
    },
  },
  required: ['boss', 'decisions'],
}

phase('Classify')
const reviewed = await pipeline(
  bosses,
  // Stage A — blind classify + merge detect (Sonnet)
  (b) => agent(classifyPrompt(b), { label: `classify:${b.slug}:${norm(b.boss).replace(/ /g, '-')}`, phase: 'Classify', model: 'sonnet', schema: CLASSIFY_SCHEMA }),
  // Stage B — Opus adjudicates anything "interesting": primary ≠ current, OR a
  // secondary (also-valid) tag was proposed. Pure primary==current & no-secondary
  // rows pass through unchanged.
  async (blind, b) => {
    const byName = new Map(b.abilities.map((a) => [norm(a.name), a]))
    const dropped = new Set((blind?.merges || []).map((m) => norm(m.dropRow)))
    const items = []
    let unchanged = 0
    for (const t of (blind?.tags || [])) {
      const cur = byName.get(norm(t.ability))
      if (!cur) continue
      if (dropped.has(norm(t.ability))) continue // folded away by a merge; tag is moot
      const sec = (t.secondary || [])
      const primaryDiffers = norm(cur.currentArchetype) !== norm(t.primary)
      if (!primaryDiffers && sec.length === 0) { unchanged++; continue }
      items.push({
        ability: cur.name,
        whatItDoes: cur.whatItDoes,
        doText: cur.doText,
        currentTag: cur.currentArchetype,
        blindPrimary: t.primary,
        blindPrimaryWhy: t.justification,
        blindSecondary: sec, // [{slug, why}]
      })
    }

    let decisions = []
    if (items.length) {
      const adjPrompt = `You are the adjudicator on archetype tagging for the M+ boss **${b.boss}** (${b.dungeon}). A blind second-opinion classifier (multi-tag aware) proposed a primary archetype and sometimes one or more also-valid secondaries for the abilities below; each currently carries a single tag. For each ability, settle the FINAL tagging: pick the final **primary** slug (the response reacted to first/most — may be the current tag or the blind primary) and the final set of **secondary** also-valid slugs (confirm only genuine second responses; prune anything loosely-related or redundant — most abilities should end with no secondary).

Read the canonical taxonomy + tagging rules at ${TAXONOMY_FILE} (only legal slugs: ${SLUGS}; mind each slug's **Not this if** guard, Tagging rule 3 on multi-tag, and classify by the player RESPONSE not surface words).

Abilities:
${JSON.stringify(items, null, 0)}

For each ability return: ability (verbatim), finalPrimary, finalSecondary[] (slugs, possibly empty), reason (one line covering the primary choice and why each secondary survives or was pruned). RETURN: boss, decisions[].`
      const adj = await agent(adjPrompt, { label: `adjudicate:${b.slug}:${norm(b.boss).replace(/ /g, '-')}`, phase: 'Adjudicate', model: 'opus', schema: ADJ_SCHEMA })
      decisions = adj?.decisions || []
    }
    return { ...b, merges: blind?.merges || [], items, decisions, unchanged }
  }
)

// ── Assemble the markup-ready report ────────────────────────────────────────
const ok = reviewed.filter(Boolean)
const decByAbility = (r, ability) => (r.decisions || []).find((d) => norm(d.ability) === norm(ability))
const code = (s) => `\`${s}\``

let totalMerges = 0, totalPrimaryChanges = 0, totalMultiTag = 0, totalReviewedNoChange = 0, totalUnchanged = 0

// Resolve each adjudicated item to its final tagging + a display row.
function resolveItem(r, it) {
  const dec = decByAbility(r, it.ability)
  const finalPrimary = dec?.finalPrimary || it.blindPrimary
  const finalSecondary = (dec?.finalSecondary || it.blindSecondary.map((s) => s.slug)).filter((s) => norm(s) !== norm(finalPrimary))
  const primaryChanged = norm(finalPrimary) !== norm(it.currentTag)
  const hasSecondary = finalSecondary.length > 0
  return { it, dec, finalPrimary, finalSecondary, primaryChanged, hasSecondary }
}

const lines = []
lines.push('# M+ Ability Re-classification Report — Second-Opinion Pass (multi-tag)')
lines.push('')
lines.push('_Generated by `reclassify-workflow.js`. Scope: the 29 S1 boss encounters (trash is a follow-up run)._')
lines.push('')
lines.push('Method: per boss, a **blind Sonnet** pass re-tagged every ability with the')
lines.push('Archetype column withheld — proposing a **primary** archetype plus any')
lines.push('**also-valid** secondaries — and flagged cast+lingering-effect pairs to merge;')
lines.push('an **Opus** adjudicator then settled the final primary + secondary set for every')
lines.push('ability whose primary moved or that gained a secondary. A card accepts any of its')
lines.push('valid archetypes; the primary drives the reveal. Mark up each item directly:')
lines.push('')
lines.push('- **Merges** — tick `[x]` to accept folding the dropped row into the cast card; strike/annotate to reject.')
lines.push('- **Tag changes** — tick `[x]` to accept; strike/annotate to reject. Cells read `current → primary` with `· also <slug>` for any secondary. Rows where the primary was *upheld* (no change) but a secondary was added, or that the adjudicator reviewed and left as-is, are shown too.')
lines.push('')

for (const d of DUNGEONS) {
  const dungeonBosses = ok.filter((r) => r.slug === d.slug)
  if (!dungeonBosses.length) continue
  lines.push(`## ${d.name}`)
  lines.push('')
  for (const r of dungeonBosses) {
    lines.push(`### ${r.boss}`)
    lines.push('')

    // Merges
    lines.push('**Merges** (cast + lingering-effect → one card):')
    lines.push('')
    if (r.merges.length) {
      for (const m of r.merges) {
        totalMerges++
        lines.push(`- [ ] keep **${m.keepCast}** / drop **${m.dropRow}**`)
        lines.push(`  - merged reveal: ${m.mergedReveal}`)
        lines.push(`  - why: ${m.reason}`)
      }
    } else {
      lines.push('_No merges found._')
    }
    lines.push('')

    // Tag changes (primary moved and/or a secondary added)
    const resolved = (r.items || []).map((it) => resolveItem(r, it))
      .filter((x) => x.primaryChanged || x.hasSecondary) // drop items the adjudicator reduced back to current+no-secondary
    const reviewedNoChange = (r.items || []).length - resolved.length
    totalReviewedNoChange += reviewedNoChange

    lines.push('**Tag changes** (primary moved and/or secondary added; Opus-adjudicated):')
    lines.push('')
    if (resolved.length) {
      lines.push('| Ability | current → final tags | adjudicator reason | ✓ |')
      lines.push('|---|---|---|---|')
      for (const x of resolved) {
        if (x.primaryChanged) totalPrimaryChanges++
        if (x.hasSecondary) totalMultiTag++
        const head = x.primaryChanged
          ? `${code(x.it.currentTag)} → ${code(x.finalPrimary)}`
          : `${code(x.finalPrimary)} (kept)`
        const also = x.hasSecondary ? ' · also ' + x.finalSecondary.map(code).join(', ') : ''
        const reason = (x.dec?.reason || x.it.blindPrimaryWhy || '').replace(/\|/g, '\\|')
        lines.push(`| ${x.it.ability} | ${head}${also} | ${reason} | [ ] |`)
      }
    } else {
      lines.push('_No tag changes._')
    }
    lines.push('')
    totalUnchanged += r.unchanged || 0
    const noteParts = [`${r.unchanged || 0} abilities held their single tag`]
    if (reviewedNoChange) noteParts.push(`${reviewedNoChange} reviewed and left as-is`)
    lines.push(`_Unchanged: ${noteParts.join('; ')}._`)
    lines.push('')
  }
}

const summary = `${ok.length} bosses reviewed · ${totalMerges} merges proposed · ${totalPrimaryChanges} primary re-tags · ${totalMultiTag} abilities gaining an also-valid secondary · ${totalUnchanged + totalReviewedNoChange} unchanged.`
lines.splice(3, 0, `**Summary:** ${summary}`, '')

const reportMarkdown = lines.join('\n') + '\n'
log(`Report assembled: ${summary}`)

return {
  reportMarkdown,
  reportPath: `${REPO}/projects/mplus_memory/reclassify-report.md`,
  summary: { bosses: ok.length, merges: totalMerges, primaryChanges: totalPrimaryChanges, multiTag: totalMultiTag, unchanged: totalUnchanged + totalReviewedNoChange },
  // structured findings, in case the report needs regeneration without re-running agents
  findings: ok.map((r) => ({
    dungeon: r.dungeon, boss: r.boss,
    merges: r.merges,
    changes: (r.items || []).map((it) => {
      const x = resolveItem(r, it)
      return { ability: it.ability, current: it.currentTag, finalPrimary: x.finalPrimary, finalSecondary: x.finalSecondary, reason: x.dec?.reason || it.blindPrimaryWhy }
    }).filter((c) => norm(c.finalPrimary) !== norm(c.current) || (c.finalSecondary || []).length),
    unchanged: r.unchanged,
  })),
}

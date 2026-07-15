export const meta = {
  name: 'spec-keybind-review',
  description: 'Author per-spec ability/rotation/build KB, then have spec-expert agents review the Bellular keybind seed placements (findings only)',
  phases: [
    { title: 'Author', detail: 'write abilities.md + rotation.md + builds.md per spec from method.gg + simc APL, reconciled vs game data' },
    { title: 'Review', detail: 'spec-expert judges each seed bucket placement, press-frequency aware' },
    { title: 'Verify', detail: 'adversarially filter findings; drop weak/hallucinated' },
  ],
}

// args = {
//   repo:     absolute repo root (e.g. "/home/.../wwt-keyboard")
//   patch:    live game version string (e.g. "12.0.7")
//   fetched:  ISO date for front matter (e.g. "2026-07-11")
//   buckets:  the seed's 52-bucket contract [{category, keybind, bar?, slot?}]  (same for every spec)
//   notation: the seed's keybind notation legend {digits, letters, "S<key>", ...}
//   specs:    [{ class, spec, methodSlug?, abilities: {<bucket>: <ability name>} }]
//             abilities is that spec's seed bucket->ability map (from bellular-keybinds.seed.json)
// }
const A = (typeof args === 'string' ? JSON.parse(args) : args) || {}
if (!A.specs || !A.specs.length) {
  log('spec-keybind-review: no args.specs supplied — nothing to do. Pass {repo,patch,fetched,buckets,notation,specs:[{class,spec,abilities}]}.')
  return { error: 'no specs', total: 0 }
}
const REPO = A.repo
const PATCH = A.patch
const FETCHED = A.fetched
const BUCKETS = A.buckets || []
const NOTATION = A.notation || {}

function slug(x) {
  return String(x).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
}
function dirFor(s) {
  return `knowledge/classes/${slug(s.class)}/${slug(s.spec)}`
}

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const AUTHOR_SCHEMA = {
  type: 'object',
  required: ['class', 'spec', 'files', 'abilities', 'priority', 'sourcesUsed', 'confidence', 'gaps'],
  properties: {
    class: { type: 'string' },
    spec: { type: 'string' },
    files: {
      type: 'array',
      description: 'the KB files written or confirmed, repo-relative',
      items: {
        type: 'object',
        required: ['path', 'status'],
        properties: {
          path: { type: 'string' },
          status: { type: 'string', enum: ['written', 'confirmed-existing', 'failed'] },
        },
      },
    },
    abilities: {
      type: 'array',
      description: 'the ability inventory the reviewer will reason over',
      items: {
        type: 'object',
        required: ['name', 'function', 'resource', 'cd', 'desc'],
        properties: {
          name: { type: 'string' },
          function: { type: 'string', description: 'game role: Interrupt, Defensive, Rotational-builder, Rotational-spender, Major cooldown, Movement, CC, Dispel, Utility, Pet, Passive, ...' },
          resource: { type: 'string' },
          cd: { type: 'string', description: 'cast time / cooldown, or "—"' },
          desc: { type: 'string' },
        },
      },
    },
    priority: {
      type: 'array',
      description: 'press-frequency ordering, most-constant to most-situational — feeds button-priority review downstream',
      items: {
        type: 'object',
        required: ['name', 'frequency'],
        properties: {
          name: { type: 'string' },
          frequency: { type: 'string', enum: ['constant', 'frequent', 'cooldown', 'situational', 'reactive', 'rare'] },
          note: { type: 'string' },
        },
      },
    },
    sourcesUsed: { type: 'array', items: { type: 'string' }, description: 'concrete URLs / simc paths actually fetched' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    gaps: { type: ['string', 'null'], description: 'what could not be sourced / had to be flagged (e.g. Devourer no method.gg guide), or null' },
  },
}

const REVIEW_SCHEMA = {
  type: 'object',
  required: ['spec', 'findings', 'missingAbilities', 'notes'],
  properties: {
    spec: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['bucket', 'seedAbility', 'verdict', 'issue', 'suggestion'],
        properties: {
          bucket: { type: 'string', description: 'the seed bucket category, e.g. "Combat 5", "Interrupt"' },
          seedAbility: { type: 'string', description: 'the ability the seed placed there (verbatim, incl. "Free"/"Trinket Macro")' },
          verdict: { type: 'string', enum: ['good', 'weak', 'wrong', 'gap', 'stale-name'] },
          issue: { type: 'string', description: 'what is wrong; reference the rotation/priority or press-frequency where relevant' },
          suggestion: { type: 'string', description: 'the fix, or "" if none' },
        },
      },
    },
    missingAbilities: {
      type: 'array',
      description: 'important abilities the seed leaves out or buries',
      items: {
        type: 'object',
        required: ['ability', 'why'],
        properties: {
          ability: { type: 'string' },
          why: { type: 'string' },
        },
      },
    },
    notes: { type: 'string', description: 'systemic observations for this spec' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['spec', 'findings', 'droppedCount', 'notes'],
  properties: {
    spec: { type: 'string' },
    findings: {
      type: 'array',
      description: 'ONLY findings that survive skeptical re-check',
      items: {
        type: 'object',
        required: ['bucket', 'seedAbility', 'verdict', 'issue', 'suggestion', 'confidence'],
        properties: {
          bucket: { type: 'string' },
          seedAbility: { type: 'string' },
          verdict: { type: 'string', enum: ['good', 'weak', 'wrong', 'gap', 'stale-name'] },
          issue: { type: 'string' },
          suggestion: { type: 'string' },
          confidence: { type: 'string', enum: ['CONFIRMED', 'PLAUSIBLE'] },
        },
      },
    },
    droppedCount: { type: 'integer', description: 'how many review findings were dropped as weak/hallucinated' },
    notes: { type: 'string' },
  },
}

// ---------------------------------------------------------------------------
// Press-frequency framework (from the seed's key layout) — shared context so
// the reviewer can judge "constant-use ability on a slow modified key" etc.
// ---------------------------------------------------------------------------
const KEY_TIERS = `KEY-SPEED TIERS (from the seed's fixed key->slot layout — this is what makes
button-priority review possible):
- Unmodified  1 2 3 4 Q E R F  = buckets Combat 1-8. FASTEST keys. Reserve for
  abilities pressed constantly during the rotation (builders/spenders/short-CD core).
- Shift-layer  S1-S4 SQ SE SR SF = Combat 9-12 + Class 1-4. One modifier, a touch
  slower — frequent-but-not-spam cooldowns and class utility (move/CC/tag/special).
- Ctrl-layer  C1-C4 CQ CE CR CF = Self-Heals + Class 5-8. Reactive: heals,
  purge/dispel/raid-defensive/lust-or-brez.
- Alt-layer  A1-A4 AQ AE AR AF = consumable/trinket/racial/PvP macros. Slowest,
  rarely pressed mid-rotation.
- Single keys  Z / SZ (defensives), X / SX (movement), C / SC (CC), V (interrupt),
  SV (slow) — reachable single presses for reactive buttons.
A MISMATCH worth flagging: a constant-press rotational ability parked on a Ctrl/Alt
key, or a rare 3-min cooldown eating a prime unmodified Combat 1-8 slot.`

// ---------------------------------------------------------------------------
// Prompts
// ---------------------------------------------------------------------------

function authorPrompt(s) {
  const dir = dirFor(s)
  const seedNames = Object.values(s.abilities || {})
    .filter((v) => v && !/^(Free|Trinket Macro|Damage Potion|Racial Ability|Mount|Healthstone\/Potion Macro|Drinking\/Mana Potion Macro|Another Combat Item If Needed)$/i.test(v))
  const isDevourer = /devourer/i.test(s.spec)
  return `You are a World of Warcraft class-knowledge author. Live game version: **Midnight, patch ${PATCH}** (retail only). Repo root: ${REPO}. Front-matter date to stamp: ${FETCHED}.

TARGET SPEC: **${s.spec} ${s.class}**
OUTPUT DIRECTORY: ${REPO}/${dir}/
FILES TO PRODUCE (siblings of the already-generated talents.md / talents.json — do NOT touch those):
  1. ${dir}/abilities.md   — raw ability inventory
  2. ${dir}/rotation.md    — priority / rotation
  3. ${dir}/builds.md      — talents / builds narrative

This is **general-purpose class knowledge** for the WoW Q&A knowledge base — raw
facts, broadly useful. It is NOT a keybind artifact. **The 52-bucket keybind
vocabulary must NEVER appear** — do not write "bucket", "keybind", "Combat 5",
"Self-Heal 1", or any bind opinion anywhere in these files.

REFERENCE FOR FORMAT + DEPTH (read at least one before writing): the Affliction
Warlock set at ${REPO}/knowledge/classes/warlock/affliction/rotation.md and
.../builds.md, and a generated talents.md at ${REPO}/${dir}/talents.md (already exists).

STEPS
1. Load web tools: call ToolSearch with query "select:WebSearch,WebFetch", then use them.
2. CHEAP RE-RUN GUARD: for each of the three target files, Read it first. If it
   already exists AND its front-matter patch is ${PATCH}, DO NOT rewrite it —
   record it as status "confirmed-existing" and still extract its ability list /
   priority into your return. Only author files that are missing or stale.
3. SOURCE (staleness doctrine — ${REPO}/knowledge/_meta/sources.md):
   - method.gg guide for **${s.spec} ${s.class}**${s.methodSlug ? ` (try https://www.method.gg/guides/${s.methodSlug} and its /talents, /rotation, /abilities subpages)` : ' (WebSearch "method.gg <spec> <class> guide midnight")'} — Tier 3.
   - The spec's **SimulationCraft APL** (Tier 1) is the PRIMARY source for rotation.md:
     search GitHub simulationcraft/simc profiles/MID1/MID1_<Class>_<Spec>.simc and the
     spec's APL in the engine. If none exists for this spec, say so in gaps and lean
     on method.gg + Wowhead for priority, flagging lower confidence.
   - method.gg talents page (Tier 3) + simc profile talent strings (Tier 1) for builds.md.
   - REQUIRE "Midnight" / "12.0" / 2026 signals in every page you trust. Reject
     undated or pre-Midnight (11.x / The War Within and earlier) content. If a fetch
     returns only a nav shell (method.gg is JS-rendered), try the sub-URLs, Wowhead,
     or WebSearch snippets instead of inventing content.
${isDevourer ? `   - ⚠ DEVOURER is the Midnight-NEW 4th Demon Hunter spec. method.gg may have NO
     guide yet. Fall back to Wowhead's Devourer page + Blizzard game data. Do NOT
     invent a kit — flag every uncertain claim @verify-ingame, set confidence low,
     and describe the gap in gaps.` : ''}
4. RECONCILE NAMES vs Tier-1 game data (this is the immune system):
   - The seed's ability list for this spec is your starting checklist:
     ${JSON.stringify(seedNames)}
   - Canonicalize any ambiguous / possibly-renamed name against
     ${REPO}/raw/wago/SpellName.csv (grep it) or the Blizzard spell API. Flag
     Midnight-new or renamed abilities in-line. Tier-1 game data is the FLOOR —
     Tier-3/4 guides may ADD abilities but may NEVER overwrite a game-data name.
   - If a seed name looks stale/renamed, note the correct current name in your
     return (the downstream review needs it) but keep authoring from real facts.
5. WRITE the three files with Edit/Write. Each MUST carry standard YAML front matter:
   ---
   title: <Spec Class — <what> (Midnight S1)>
   patch: ${PATCH}
   fetched: ${FETCHED}
   reviewed: ${FETCHED}
   sources:
     - <url or simc path>   # tier N, ${FETCHED}
   confidence: <high|medium|low>
   ---
   (one "# tier N, <date>" comment per source URL). Put @verify-ingame markers on
   any uncertain / low-confidence entry (harvested later by wowkb.gen_verify).

   FILE CONTRACTS:
   - **abilities.md** — (a) Overview: hero trees, resource system, 1-2 lines of
     factual playstyle. (b) An inventory table with columns exactly:
     \`Ability | Function | Resource | Cast / CD | Description\`.
     \`Function\` = the ability's GAME ROLE (Interrupt, Defensive, Rotational-builder,
     Rotational-spender, Major cooldown, Movement, CC, Dispel, Utility, Pet, notable
     Passive) — descriptive, NEVER a keybind/bucket assignment.
   - **rotation.md** — distilled like the Affliction reference: framing paragraph ->
     pre-combat -> cooldown rules -> single-target priority list -> cleave/AoE ->
     hero-tree branches. Cite the simc APL (Tier 1) where one exists; method.gg
     corroborates/adds colour. This is the button-priority backbone.
   - **builds.md** — hero-tree choice, recommended talent loadout(s) and what they
     change, key talent interactions. Layer on top of the existing talents.md /
     talents.json (do NOT regenerate those). method.gg talents (Tier 3) + simc
     talent strings (Tier 1).
6. RETURN the structured result. class="${s.class}", spec="${s.spec}".
   - files: one entry per target file with its status.
   - abilities: the full inventory (name/function/resource/cd/desc) — the reviewer
     reasons over THIS, so be complete and use current names.
   - priority: every notable ability tagged by press-frequency
     (constant|frequent|cooldown|situational|reactive|rare) — most-constant first.
     This is what lets the downstream reviewer judge which abilities deserve the
     fast keys. Include the core rotational buttons AND the utility/defensives.
   - sourcesUsed: the concrete URLs / simc paths you actually fetched.
   - gaps: anything you could not source or had to flag, or null.`
}

function reviewPrompt(s, auth) {
  const seedMap = s.abilities || {}
  return `You are a **${s.spec} ${s.class}** spec expert reviewing a set of recommended
keybind placements for World of Warcraft Midnight (patch ${PATCH}). You have just
been briefed with the spec's real, current kit. Judge the placements on the FACTS,
including press-frequency fit. Findings only — do not edit anything.

YOUR GROUNDING (authored + name-reconciled this run):
${auth ? JSON.stringify({ abilities: auth.abilities, priority: auth.priority, gaps: auth.gaps, confidence: auth.confidence }, null, 1) : '(author stage produced no result — reason from your own spec knowledge and say so in notes)'}

THE KEYBIND SYSTEM. Bellular's planner sorts every ability into one of 52 fixed
"buckets"; each bucket owns one key. The seed maps, for this spec, bucket -> ability:
${JSON.stringify(seedMap, null, 1)}

BUCKET CONTRACT (category -> key; same for all specs):
${JSON.stringify(BUCKETS.map((b) => ({ category: b.category, key: b.keybind })))}

${KEY_TIERS}

JUDGE each bucket the seed assigns for this spec:
- Is the ability CORRECT for that bucket's game role (an Interrupt in Interrupt, a
  real defensive in Personal Defensive, the actual movement ability in Movement)?
- PRESS-FREQUENCY FIT (the reason this review exists): does a constantly-pressed
  rotational ability sit on a fast unmodified key (Combat 1-8) — or is it buried on
  a Ctrl/Alt key? Is a rare long-cooldown eating a prime unmodified slot a spammed
  builder should own? Cross-reference the priority list above.
- STALE / PLACEHOLDER names: flag literal "Free", "Trinket Macro", "Damage Potion",
  "Racial Ability", etc. only if they sit where a real ability belongs; and flag any
  ability name that is renamed/removed in ${PATCH} (use the reconciled inventory).
- Assign a verdict per finding: good | weak | wrong | gap | stale-name.
  (Emit "good" ONLY for placements worth affirming; you need not enumerate every
  obviously-correct slot — focus on what's actionable, but you may confirm the
  load-bearing core placements.)

Also list missingAbilities: important abilities from the inventory the seed leaves
out entirely or buries in a bad slot.

RETURN the structured result. spec="${s.spec}". Ground every finding in the
inventory/priority above — do not invent abilities the spec does not have.`
}

function verifyPrompt(s, auth, rev) {
  return `Adversarially verify a spec-expert's keybind-placement findings for
**${s.spec} ${s.class}** (WoW Midnight ${PATCH}). Default to SKEPTICAL: drop any
finding you cannot substantiate from the grounding. Keep only real, defensible ones.

THE GROUNDING (authoritative ability inventory + press-frequency for this spec):
${auth ? JSON.stringify({ abilities: auth.abilities, priority: auth.priority }, null, 1) : '(no author result)'}

THE SEED PLACEMENTS under review:
${JSON.stringify(s.abilities || {}, null, 1)}

THE REVIEWER'S FINDINGS:
${rev ? JSON.stringify(rev.findings || [], null, 1) : '(no review result)'}
Reviewer's missingAbilities: ${rev ? JSON.stringify(rev.missingAbilities || []) : '[]'}

FOR EACH finding, check:
1. Does the named bucket exist in the seed slice, and is seedAbility what the seed
   actually placed there? (Reject fabricated bucket/ability pairs.)
2. Is the ability the finding talks about actually in the inventory (or genuinely
   absent, for a "gap")? Reject findings that reference abilities this spec lacks.
3. Is the issue TRUE and MATERIAL — a real role mismatch, a real press-frequency
   mismatch backed by the priority list, or a real stale/placeholder name? Reject
   nitpicks, restyling of a defensible choice, or personal preference dressed as fact.
4. Mark each SURVIVING finding CONFIRMED (clearly correct from the grounding) or
   PLAUSIBLE (reasonable but not fully certain). DROP the rest; count them in droppedCount.

Be conservative: a smaller set of solid findings beats a long speculative list.

RETURN the structured result. spec="${s.spec}". findings = only the survivors.`
}

// ---------------------------------------------------------------------------
// Pipeline — each spec independent (distinct output dir, no barrier, no worktree)
// ---------------------------------------------------------------------------

phase('Author')
const results = await pipeline(
  A.specs,
  (s) => agent(authorPrompt(s), { label: `author:${slug(s.spec)}-${slug(s.class)}`, phase: 'Author', schema: AUTHOR_SCHEMA })
    .then((auth) => ({ s, auth })),
  (b) => agent(reviewPrompt(b.s, b.auth), { label: `review:${slug(b.s.spec)}`, phase: 'Review', schema: REVIEW_SCHEMA })
    .then((rev) => ({ ...b, rev })),
  (b) => agent(verifyPrompt(b.s, b.auth, b.rev), { label: `verify:${slug(b.s.spec)}`, phase: 'Verify', schema: VERIFY_SCHEMA })
    .then((ver) => ({ ...b, ver })),
)

const clean = results.filter(Boolean)
return {
  total: A.specs.length,
  completed: clean.length,
  patch: PATCH,
  fetched: FETCHED,
  specs: clean.map((r) => ({
    class: r.s.class,
    spec: r.s.spec,
    dir: dirFor(r.s),
    files: r.auth ? r.auth.files : [],
    confidence: r.auth ? r.auth.confidence : null,
    gaps: r.auth ? r.auth.gaps : null,
    sourcesUsed: r.auth ? r.auth.sourcesUsed : [],
    priority: r.auth ? r.auth.priority : [],
    findings: r.ver ? r.ver.findings : (r.rev ? r.rev.findings : []),
    droppedCount: r.ver ? r.ver.droppedCount : null,
    missingAbilities: r.rev ? r.rev.missingAbilities : [],
    reviewNotes: r.rev ? r.rev.notes : null,
    verifyNotes: r.ver ? r.ver.notes : null,
  })),
  // specs whose author stage failed to write a file, surfaced for the driver
  authoring_failures: clean
    .filter((r) => r.auth && r.auth.files && r.auth.files.some((f) => f.status === 'failed'))
    .map((r) => ({ spec: r.s.spec, files: r.auth.files.filter((f) => f.status === 'failed') })),
}

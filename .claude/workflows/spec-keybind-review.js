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
// Floats mode (args.mode === 'floats'): instead of reviewing the fixed seed,
// PROPOSE the layout-v2 §6 restructure for each spec — a fixed core + per-band
// float lists — then adversarially verify it. Consumed by tool/apply_floats.py.
// ---------------------------------------------------------------------------

const FLOAT_BANDS = ['Rotational', 'Cooldown', 'Overflow']

const PROPOSE_SCHEMA = {
  type: 'object',
  required: ['class', 'spec', 'fixedCore', 'floats', 'outsideBandChanges', 'inventoryGaps', 'notes', 'confidence'],
  properties: {
    class: { type: 'string' },
    spec: { type: 'string' },
    inventoryGaps: {
      type: 'array',
      description: 'Ability names you placed (fixedCore or floats) that are NOT in the Tier-1 inventory but ARE named in this spec\'s rotation.md AND resolve in raw/wago/SpellName.csv. The Blizzard API talent-tree omits some real nodes (e.g. Frost\'s Icy Veins/Glacial Spike/Shifting Power); the addon resolves these by name at runtime. Empty [] if none. This is the follow-up list for topping up the inventory source.',
      items: { type: 'string' },
    },
    fixedCore: {
      type: 'array',
      description: 'ALWAYS-present abilities pinned to numbered Rotational/Cooldown/Overflow buckets. Baseline kit or mandatory-every-build talents ONLY — never a choice node or a build-optional talent. Ordered so the bucket number reflects press frequency (Rotational 1 = most-pressed).',
      items: {
        type: 'object',
        required: ['bucket', 'ability'],
        properties: {
          bucket: { type: 'string', description: 'e.g. "Rotational 1", "Cooldown 1"' },
          ability: { type: 'string', description: 'exact inventory name; bind the BASE of an override (Shadow Bolt not Infernal Bolt)' },
        },
      },
    },
    floats: {
      type: 'object',
      description: 'per-band priority-ordered candidate lists (build-conditional talents). Order = likelihood of being talented, meta first. List BOTH sides of a choice node — exactly one resolves. Names must exist in the inventory.',
      required: ['Rotational', 'Cooldown', 'Overflow'],
      properties: {
        Rotational: { type: 'array', items: { type: 'string' } },
        Cooldown: { type: 'array', items: { type: 'string' } },
        Overflow: { type: 'array', items: { type: 'string' } },
      },
    },
    outsideBandChanges: {
      type: 'array',
      description: 'Re-homes for abilities EVICTED from the Rot/CD/Overflow bands (so they are not left unbound) and gap-fills into non-floating buckets. Each sets abilities[bucket]=ability. Non-floating buckets only (Class N, Self-Heal N, CC, Slow, Movement, Interrupt, ...). Empty array if none.',
      items: {
        type: 'object',
        required: ['bucket', 'ability', 'why'],
        properties: {
          bucket: { type: 'string' },
          ability: { type: 'string' },
          why: { type: 'string' },
        },
      },
    },
    notes: { type: 'string' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
}

const PROPOSE_VERIFY_SCHEMA = {
  type: 'object',
  required: ['class', 'spec', 'fixedCore', 'floats', 'outsideBandChanges', 'inventoryGaps', 'droppedOrFixed', 'verdict', 'notes'],
  properties: {
    class: { type: 'string' },
    spec: { type: 'string' },
    fixedCore: PROPOSE_SCHEMA.properties.fixedCore,
    floats: PROPOSE_SCHEMA.properties.floats,
    outsideBandChanges: PROPOSE_SCHEMA.properties.outsideBandChanges,
    inventoryGaps: PROPOSE_SCHEMA.properties.inventoryGaps,
    droppedOrFixed: { type: 'integer', description: 'how many proposal entries you corrected or removed' },
    verdict: { type: 'string', enum: ['clean', 'amended', 'reject'], description: 'reject only if the proposal is unusable and you could not repair it' },
    notes: { type: 'string' },
  },
}

const INV_JSON = 'projects/keybinder/data/spec-inventory.json'
const SEED_JSON = 'projects/keybinder/data/bellular-keybinds.seed.json'

function extractCmd(s) {
  // one-liner the agent runs to pull JUST this spec's inventory + current abilities
  const key = `${s.class}/${s.spec}`
  return `python3 - <<'PY'\nimport json\nk=${JSON.stringify(key)}\ninv=json.load(open(${JSON.stringify(INV_JSON)}))[k]["abilities"]\nfor a in inv: print(f"{a['name']} [origin={a['origin']}, band={a['band']}, cd={a['cooldown'] or '—'}, mode={a['suggestedMode']}"+(f", seed={a['bucket']}" if a['bucket'] else "")+"]")\nseed=[x for x in json.load(open(${JSON.stringify(SEED_JSON)}))["specs"] if x["class"]+"/"+x["spec"]==k][0]\nprint("\\nCURRENT ABILITIES:", json.dumps(seed["abilities"]))\nPY`
}

function proposePrompt(s) {
  const dir = dirFor(s)
  return `You are re-filing the BucketBinds keybind layout for **${s.spec} ${s.class}** (WoW Midnight ${PATCH}) into the layout-v2 fixed-vs-floating model. Repo: ${REPO}. FINDINGS ONLY — you edit nothing; you return a structured proposal.

GATHER YOUR GROUNDING (run/read these first):
  1. Bash this to get the Tier-1 ability inventory (the ONLY names you may use — each tagged origin/band/cooldown/suggested-mode/current-seed-bucket) AND this spec's current bucket→ability map:
\`\`\`
${extractCmd(s)}
\`\`\`
  2. Read ${REPO}/${dir}/rotation.md — the press-frequency backbone (what is pressed most).
  3. Read the "${s.spec}" row in ${REPO}/projects/keybinder/data/layout-v2-proposal.md §6 — a hand-authored proposal (MEDIUM confidence; a strong prior, not gospel). Skim §2 (band contract) too, and the Demonology floats block in ${SEED_JSON} as the worked example.

Everything in the current abilities map OUTSIDE Rotational/Cooldown/Overflow stays as-is unless you re-home an eviction.

${KEY_TIERS}

PRODUCE the restructure for the THREE floating bands only:
- **fixedCore**: abilities that EVERY build of this spec has — baseline kit (origin=class-baseline) or a mandatory core talent — pinned to numbered buckets (Rotational 1-8, Cooldown 1-4, Overflow 1-6). Order by press frequency (Rotational 1 = most-pressed builder/filler; put ≥45s majors in Cooldown per the band's cd rule). NEVER put a choice-node ability or a build-optional talent here — those float.
- **floats**: per band, the build-conditional talents as a priority list ordered by likelihood-of-being-talented (meta build first). LIST BOTH SIDES of every choice node (origin=talent-choice pairs share a node — exactly one resolves at dump time, so listing both is correct and is the whole point). A band's floats fill only the slots fixedCore leaves empty; keep totals sane (Rot ≤8, CD ≤4, Overflow ≤6 including fixedCore).
- **outsideBandChanges**: if the restructure EVICTS an ability that was in a Combat band (e.g. an external, Hunter's Mark, Raise Dead, Frost Shock), re-home it to the correct NON-floating bucket so it stays bound — per §6. Also any §6 gap-fill into a non-floating bucket. Do NOT touch buckets you are not changing.

HARD RULES:
- Ability names MUST resolve to a real spell — no invented names. PREFER names from the inventory above (the primary anti-hallucination guard). BUT the Tier-1 inventory has known holes: the Blizzard API talent-tree endpoint omits some real nodes (confirmed: Frost's Icy Veins, Glacial Spike, Shifting Power are absent from the inventory yet are core buttons). So you MAY also place an ability that is NOT in the inventory **only if** it satisfies BOTH: (a) it is named in this spec's rotation.md as a real pressed button, AND (b) it resolves in game data — verify with \`grep -F "<name>" ${REPO}/raw/wago/SpellName.csv\` (a hit = real spell; the addon resolves it by name at runtime and drops it if untalented). List every such name in \`inventoryGaps\`. Do NOT use this to add speculative abilities — only ones rotation.md clearly relies on that the inventory dropped.
- Overrides share a key — use the BASE (Shadow Bolt, not Infernal Bolt; Stormstrike, not Windstrike).
- Frequency, not power: a <45s button pressed constantly is Rotational even if it "feels" like a cooldown; a ≥45s window button is Cooldown.
- If §6 and the inventory/rotation.md disagree, the Tier-1 inventory + rotation.md win; note the conflict.

RETURN the structured proposal. class="${s.class}", spec="${s.spec}".`
}

function proposeVerifyPrompt(s, prop) {
  return `Adversarially verify a fixed-core + floats keybind proposal for **${s.spec} ${s.class}** (WoW Midnight ${PATCH}). Repair it where you can; drop what you cannot substantiate. Return the CORRECTED proposal.

Get the authoritative inventory (the ONLY legal names; origin/band/cd/mode/seed) + this spec's current abilities by running:
\`\`\`
${extractCmd(s)}
\`\`\`

THE PROPOSAL under review:
${JSON.stringify(prop ? { fixedCore: prop.fixedCore, floats: prop.floats, outsideBandChanges: prop.outsideBandChanges, notes: prop.notes } : {}, null, 1)}

CHECK and FIX each of:
1. NAMES: every fixedCore.ability, every floats[*] name, every outsideBandChanges.ability either (a) is in the inventory verbatim, OR (b) is listed in inventoryGaps AND is a real spell — spot-check the gap names with \`grep -F "<name>" ${A.repo || ''}/raw/wago/SpellName.csv\` and reject any with no hit. Remove or correct anything that is neither in the inventory nor a SpellName-verified rotation.md ability. Ensure every name you keep that is NOT in the inventory appears in inventoryGaps.
2. FIXED = ALWAYS PRESENT: nothing in fixedCore may be origin=talent-choice or a build-optional talent. If it is, move it into the matching band's floats. Baseline/mandatory-core only.
3. FLOATS = CONDITIONAL + BOTH CHOICE SIDES: for every talent-choice pair in the inventory that belongs to a floating band, BOTH names appear in that band's float list. Order is meta-first but a wrong order is a nit, not a fix.
4. NO DUPLICATION: no ability is both fixedCore and a float, or fixed in two buckets.
5. CAPACITY: fixedCore + resolvable floats do not exceed Rot 8 / CD 4 / Overflow 6.
6. BAND CORRECTNESS: ≥45s → Cooldown, <45s constant-press → Rotational, per the inventory's band tag and §2's documented exceptions.
7. EVICTIONS RE-HOMED: any band ability that got dropped is either genuinely gone from the kit or re-homed via outsideBandChanges — not silently unbound.

Set verdict: clean (no changes), amended (you fixed things — count them in droppedOrFixed), or reject (unusable). Prefer amend over reject.

RETURN the corrected proposal. class="${s.class}", spec="${s.spec}".`
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

if (A.mode === 'floats') {
  phase('Propose')
  const out = await pipeline(
    A.specs,
    (s) => agent(proposePrompt(s), { label: `propose:${slug(s.spec)}-${slug(s.class)}`, phase: 'Propose', schema: PROPOSE_SCHEMA })
      .then((prop) => ({ s, prop })),
    (b) => agent(proposeVerifyPrompt(b.s, b.prop), { label: `verify:${slug(b.s.spec)}-${slug(b.s.class)}`, phase: 'Verify', schema: PROPOSE_VERIFY_SCHEMA })
      .then((ver) => ({ ...b, ver })),
  )
  const done = out.filter(Boolean)
  return {
    mode: 'floats',
    total: A.specs.length,
    completed: done.length,
    patch: PATCH,
    specs: done.map((r) => {
      const v = r.ver || r.prop || {}
      return {
        class: r.s.class,
        spec: r.s.spec,
        fixedCore: v.fixedCore || [],
        floats: v.floats || { Rotational: [], Cooldown: [], Overflow: [] },
        outsideBandChanges: v.outsideBandChanges || [],
        inventoryGaps: v.inventoryGaps || [],
        verdict: r.ver ? r.ver.verdict : 'unverified',
        droppedOrFixed: r.ver ? r.ver.droppedOrFixed : null,
        confidence: r.prop ? r.prop.confidence : null,
        notes: [r.prop && r.prop.notes, r.ver && r.ver.notes].filter(Boolean).join(' | '),
      }
    }),
  }
}

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

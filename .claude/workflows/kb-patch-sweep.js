export const meta = {
  name: 'kb-patch-sweep',
  description: 'Update WoW KB files to a target patch using a change ledger, then adversarially verify each',
  phases: [
    { title: 'Update', detail: 'apply per-file verdict from the change ledger' },
    { title: 'Verify', detail: 'adversarially check each updated file' },
  ],
}

// args = {
//   repo:    absolute repo root (e.g. "/home/.../wow")
//   patch:   target version string (e.g. "12.0.8")
//   build:   client build string or "" (e.g. "12.0.8.xxxxx")
//   fetched: ISO date for front matter (e.g. "2026-09-01")
//   ledger:  absolute path to knowledge/_meta/changelog-<patch>.md
//   items:   [{ file, verdict, why }]  verdict ∈ CHANGED | RESTAMP | NEW
// }
const A = (typeof args === 'string' ? JSON.parse(args) : args) || {}
if (!A.items || !A.items.length) {
  log('kb-patch-sweep: no args.items supplied — nothing to do. Pass {repo,patch,build,fetched,ledger,items}.')
  return { error: 'no items', total: 0 }
}
const REPO = A.repo
const PATCH = A.patch
const BUILD = A.build || ''
const FETCHED = A.fetched
const LEDGER = A.ledger

const UPDATE_SCHEMA = {
  type: 'object',
  required: ['file', 'verdict_applied', 'content_edited', 'front_matter_patch', 'todos_resolved', 'drift_found', 'sources_added', 'summary'],
  properties: {
    file: { type: 'string' },
    verdict_applied: { type: 'string', enum: ['CHANGED', 'RESTAMP', 'NEW'] },
    content_edited: { type: 'boolean', description: 'true if body prose was changed/created, not just front matter' },
    front_matter_patch: { type: 'string', description: 'the patch: value now in the file front matter' },
    todos_resolved: { type: 'boolean' },
    drift_found: { type: ['string', 'null'], description: 'pre-current-expansion stale content found, or null' },
    sources_added: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object',
  required: ['file', 'pass', 'front_matter_current', 'citations_present', 'stale_claims_remaining', 'tier_downgrade', 'issues'],
  properties: {
    file: { type: 'string' },
    pass: { type: 'boolean' },
    front_matter_current: { type: 'boolean' },
    citations_present: { type: 'boolean' },
    stale_claims_remaining: { type: 'array', items: { type: 'string' } },
    tier_downgrade: { type: ['string', 'null'], description: 'a claim this edit regressed from a Tier-1 source (blue post / patch-notes archive / moving-values) to a lower-tier source, or null if none' },
    issues: { type: 'array', items: { type: 'string' } },
  },
}

function updatePrompt(item) {
  return `You are updating a single World of Warcraft knowledge-base file to patch ${PATCH}. Repo root: ${REPO}. Front-matter date to stamp: ${FETCHED}.

YOUR FILE: ${item.file}
LEDGER VERDICT: ${item.verdict} — ${item.why}

STEPS:
1. Read the change ledger at ${LEDGER} in full. Find the row(s) for your file in its "KB file impact map" and the relevant detail sections.
2. ${item.verdict === 'NEW'
    ? `Your file does NOT exist yet — CREATE it. Pull specifics from the ledger; fetch more detail if needed (step 4). Write full YAML front matter (title, patch: ${PATCH}${BUILD ? `, build: ${BUILD}` : ''}, fetched: ${FETCHED}, reviewed: ${FETCHED}, sources, confidence) and a body following the conventions of sibling files in the same directory (Read one first).`
    : `Read your file at ${REPO}/${item.file}.`}
3. Apply the verdict:
   - CHANGED: rewrite the specific claims the ledger says changed; be precise with numbers; fetch detail where the ledger is thin (step 4). Update front matter: patch: ${PATCH}, fetched: ${FETCHED} (you edited content), reviewed: ${FETCHED}, add the real source URL(s) you used, set confidence appropriately.
   - RESTAMP: sanity-read the body. Set patch: ${PATCH} and reviewed: ${FETCHED} (ALWAYS — this records that the file was checked in this sweep). Bump fetched: ${FETCHED} ONLY if you actually changed or re-sourced content; if the body was already accurate and you changed nothing, LEAVE fetched as-is (it marks original sourcing, not this check). If you find drift from an OLDER game version (dead currencies, old level cap, dead seasons/raids), FIX it if you can verify the ${PATCH} truth, else flag it in drift_found and set confidence: low. ${item.file.includes('/characters/') ? 'This is a VOLATILE character file — do NOT fetch a live profile. Just restamp and ensure a note exists that it must be re-fetched live before answering.' : ''}
   - NEW: as in step 2.
4. If you need live facts, FIRST call ToolSearch with query "select:WebSearch,WebFetch" to load those tools, then use them. Prefer Tier-1 (worldofwarcraft.blizzard.com / news.blizzard.com), then Tier-3 (icy-veins.com / wowhead.com — corroborate numbers). REQUIRE the target version / "Midnight" / current-year signals; reject undated or older content.
   PROVENANCE PRECEDENCE (do not skip): before you overwrite any existing numeric/named claim, check whether it is already backed by Tier-1 feed data — the registry ${REPO}/knowledge/_meta/moving-values.md and the verbatim archive ${REPO}/knowledge/_meta/patch-notes/${PATCH}.md (blue-post / hotfix log). A claim backed there is the FLOOR: a lower-tier fetched source (Icy Veins / Wowhead editorial / SEO) may corroborate or ADD but may NOT overwrite it. On disagreement, KEEP the Tier-1 value and note the conflict in summary — never regress authoritative data to match a stale article. Resolve name/proper-noun conflicts via game data (wago.tools DB2 or the Wowhead NPC/item DB page), not editorial prose.
5. Resolve any "## TODO" section the ledger or your fetch answers. If you genuinely cannot, leave it and note so.
6. Preserve the file's structure and voice; keep the front-matter convention exactly. Edit with Edit/Write.

Every knowledge/**.md MUST have at least one source URL in front matter (project doctrine). The only acceptable exception is a self-referential meta registry; if so, say why in summary.

Return the structured result. file must be "${item.file}".`
}

function verifyPrompt(item, upd) {
  return `Adversarially verify a just-updated WoW knowledge-base file. Repo root: ${REPO}. Live patch is ${PATCH}.

FILE: ${item.file}
The updater claimed: ${upd ? JSON.stringify({ verdict: upd.verdict_applied, edited: upd.content_edited, patch: upd.front_matter_patch, summary: upd.summary }) : 'no result (updater failed)'}

CHECK by Reading ${REPO}/${item.file} fresh:
1. Front matter: is patch: ${PATCH} AND is reviewed: ${FETCHED} (this sweep's date — proves the file was checked in this run)? Both required for front_matter_current. (fetched: may legitimately be an older date if the body was unchanged — do NOT fail on that.)
2. Is there at least one source URL in front matter? (citations_present). A self-referential meta registry may legitimately have none — note it in issues but it is not automatically a fail.
3. Scan the BODY for any claim that contradicts ${PATCH} or describes a dead game version (older expansion, old level cap, removed currencies, dead seasons). List each in stale_claims_remaining. Cross-check the ledger at ${LEDGER}. Watch for stale VERSION LABELS in section headings, not just data.
4. For CHANGED/NEW: does the body actually reflect the ${PATCH} changes the ledger names for this file? If it still reads like the old patch with only front matter bumped, that is a FAIL — note in issues.
5. PROVENANCE regression check: cross-check any numeric/named claim this edit changed against ${REPO}/knowledge/_meta/moving-values.md and ${REPO}/knowledge/_meta/patch-notes/${PATCH}.md. If the edit replaced a value backed by that Tier-1 feed data with one sourced from a lower tier (Icy Veins / Wowhead editorial / SEO), record it in tier_downgrade and FAIL. null if none. (A Tier-1-backed claim is the floor; lower tiers may add but never overwrite.)
6. Be skeptical; default to listing a concern rather than passing silently. pass=true only if front matter is current, a citation exists (or justified exception), no stale claims remain, AND tier_downgrade is null.

Return the structured result. file must be "${item.file}".`
}

phase('Update')
const results = await pipeline(
  A.items,
  (item) => agent(updatePrompt(item), { label: `update:${item.file.split('/').pop()}`, phase: 'Update', schema: UPDATE_SCHEMA }),
  (upd, item) => agent(verifyPrompt(item, upd), { label: `verify:${item.file.split('/').pop()}`, phase: 'Verify', schema: VERIFY_SCHEMA })
    .then((v) => ({ item, upd, verify: v })),
)

const clean = results.filter(Boolean)
return {
  total: A.items.length,
  completed: clean.length,
  passed: clean.filter((r) => r.verify && r.verify.pass).length,
  failures: clean.filter((r) => !r.verify || !r.verify.pass).map((r) => ({
    file: r.item.file,
    verdict: r.item.verdict,
    issues: r.verify ? r.verify.issues : ['no verify result'],
    stale: r.verify ? r.verify.stale_claims_remaining : [],
  })),
  drift_flagged: clean.filter((r) => r.upd && r.upd.drift_found).map((r) => ({ file: r.item.file, drift: r.upd.drift_found })),
  tier_downgrades: clean.filter((r) => r.verify && r.verify.tier_downgrade).map((r) => ({ file: r.item.file, downgrade: r.verify.tier_downgrade })),
  new_files: clean.filter((r) => r.item.verdict === 'NEW' && r.upd).map((r) => r.item.file),
}

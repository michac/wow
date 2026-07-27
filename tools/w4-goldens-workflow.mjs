export const meta = {
  name: 'w4-phase2-goldens',
  description: 'Author the W4 Phase-2 State->Guidance golden corpus (derive -> adversarial verify -> synth)',
  phases: [
    { title: 'Derive', detail: 'one agent per scenario: author state/guidance/rationale from the rotation source + contract' },
    { title: 'Verify', detail: 'two adversarial lenses per scenario: rotation-correctness + contract/secrecy' },
    { title: 'Synth', detail: 'coverage report + gaps across the whole corpus' },
  ],
}

// ---------------------------------------------------------------------------
// Shared paths + grounding. Absolute so subagents resolve them regardless of cwd.
const ROOT = '/home/mchristiansen/code/fun/wow'
const PROJ = ROOT + '/projects/cooldown-hud'
const GOLD = PROJ + '/corpus/goldens'
const KB = ROOT + '/knowledge/classes/warlock/demonology'

// The canonical anchor set + readable-combat model + framing rules. Every DERIVE
// agent gets this verbatim so all 18 fixtures share one physics.
const SHARED = `
You are authoring ONE golden test case for the Cooldown HUD's W4 Phase-2 corpus:
an independent \`State -> Guidance\` oracle for a Demonology Warlock (patch 12.0.7).

## READ FIRST (and ONLY these)
- Contract:  ${PROJ}/guidance-contract.json   (the Guidance v1 contract -- source of truth)
- Format README: ${GOLD}/README.md
- Canonical templates (COPY their exact field shape): ${GOLD}/hand-of-guldan/,
  ${GOLD}/demonbolt-proc/, ${GOLD}/implosion/, ${GOLD}/incoming-overcap/  (state.json + guidance.json + rationale.md each)
- Rotation source (the ORACLE): ${KB}/rotation.md  and  ${KB}/diabolist-sequences.md
  (on conflict, diabolist-sequences.md's PARSE DATA wins -- e.g. the only Grimoire in the
   meta build is **Grimoire: Imp Lord**; Fel Ravager / Doomguard / Power Siphon are NOT in it).
- Ability facts if needed: ${KB}/abilities.md

## HARD CONSTRAINT -- oracle independence (build-plan P2)
Reason ONLY from (the State fixture you author) + (the rotation source) + (the contract).
Do **NOT** open, read, grep, or infer from ANY addon code -- especially
${PROJ}/addon/CDMProbe/*.lua (HudBoard.lua, HudScore.lua, SpecDemonology.lua). Reading the
code under test to derive the oracle contaminates it. If you catch yourself wanting to peek at
the scoring, STOP -- the rotation .md files are the only authority for "what is the #1 press."

## THE CDM ANCHOR SET (real cooldownIDs from live captures -- never invent IDs)
| cooldownID | spellID | ability | keybind | notes |
|---|---|---|---|---|
| 2742  | 265187 | Summon Demonic Tyrant | sQ | hard CD ~60s. Its own frame's \`buff.isActive\` = Tyrant window ACTIVE. |
| 671   | 104316 | Call Dreadstalkers | E | hard CD ~20s. |
| 34991 | 105174 | Hand of Gul'dan | R | 3-shard spender. Transforms -> Ruination (set overrideSpellID & liveSpellID = 434635) when Pit-Lord Art armed. |
| 1979  | 264178 | Demonbolt | F | Demonic-Core spender; instant. GLOWS (glow.active) when a Core is up. |
| 34990 | 686    | Shadow Bolt | Q | free builder/filler. Transforms -> Infernal Bolt (set overrideSpellID & liveSpellID = 434506) when Mother-of-Chaos Art armed; IB is a 3-shard builder, self-gated to <3 shards. |
| 149122| 196277 | Implosion | 1 | ~15s CD; real gate = >=6 Wild Imps (SECRET count). |
| 135056| 1276452| Grimoire: Imp Lord | sE | ~2min demon summon, paired with Tyrant. The meta-build grimoire. |
| 777   | 264173 | Demonic Core (TrackedBuff) | (none) | buff.isActive READABLE in combat = a Core is up. STACK COUNT is secret. |
| 9426  | 428514 | Diabolic Ritual (TrackedBuff) | (none) | the ritual/Art tracker; buff.isActive readable. |
| 143038| 296553 | Wild Imp (TrackedBuff) | (none) | buff.isActive readable = imps out; COUNT is secret. |
Resource: \`power.SoulShards = { "value": N, "max": 5, "readable": true }\` (key EXACTLY "SoulShards", capitalized).

## THE READABLE-COMBAT MODEL (architecture.md, verified against real captures) -- get this RIGHT
In COMBAT the game hides live cooldowns. Per pulse field, what is readable:
- \`cd\`  -> **SECRET**. readable:false. Use the NAPKIN:
    * cooling with a live estimate: \`{ "state":"anticipated", "remaining":>0, "readable":false, "source":"napkin", "changedAt":<t> }\`  (SOON is built on this)
    * elapsed / probably-up (the napkin's estimate ran out): \`{ "state":"unknown", "readable":false, "source":"napkin" }\`  (NO "remaining"). This is how a hard-CD reads as "probably ready" in combat.
    * no cd model at all (instant spells like SB/HoG/DB base): \`{ "state":"unknown", "readable":false, "source":"none" }\`.
    * NAPKIN HONESTY: a napkin cd may NEVER be "ready". "ready" is only ever a live read (source:"live"), which does not happen in combat. Anticipated must carry remaining>0; unknown must carry NO remaining.
- \`glow\`  -> **READABLE** (IsSpellOverlayed). The actionable "press this now" / proc glow. It lands on the EMPOWERED spell (e.g. Demonbolt glows when a Core is up; a transformed HoG->Ruination frame glows). Set glow.active:true to justify a proc-driven press.
- \`buff.isActive\`  -> **READABLE** (the TrackedBuff item frame). Proc/buff presence: Core up (777), imps out (143038), ritual armed (9426), Tyrant window active (2742's frame buff).
- \`aura\`  -> **SECRET in combat** (C_UnitAuras). ALWAYS \`{ "readable": false }\` in a combat fixture. It is NEVER the proc source. (Unreadable aura/charge must carry no value -- readable:false and nothing else.)
- \`power.SoulShards.value\`  -> **READABLE**. Shards are always known.

Consequence for the oracle: a drawn cue's justification must trace to a READABLE signal
(shards / glow / buff.isActive / a napkin estimate) -- NEVER to a secret cd or aura. Where the
true rotational gate is a Secret Value (Core STACK count, Wild Imp count), the golden asserts the
readable APPROXIMATION and SOFTENS (informs, doesn't falsely instruct).

## THE GUIDANCE CONTRACT (v1) -- what you emit in guidance.json
- \`resourceBar\`: { "value":N, "max":5, "incoming":M, "display":"discrete", "powerType":"SOUL_SHARDS" }.
    * \`incoming\` = net shard delta of IN-FLIGHT casts (a napkin projection). A Shadow Bolt in flight (history \`start\` for spell 686, no \`succeeded\` yet) => incoming:+1. A spender in flight => negative. The Coach ranks on PROJECTED = value + incoming.
- \`cues\`: an object keyed by cooldownID. **LIST ONLY CUES THAT DRAW.** An unlisted cooldownID = draw:false = AVAILABLE (internal, no cue). Each drawn cue: { "draw":true, "emphasis":<TOKEN>, "transient":<edge|omit>, "note":<pass-through string|omit> }.
- emphasis TOKENS (generic, class-agnostic, NO rgba/pixels): SOON, ROTATION, LATE, JUDGE, SEQUENCE. (AVAILABLE/NEVER are internal -> do not draw.)
- **SINGLE TOP PRESS**: AT MOST ONE drawn cue may be ROTATION *or* LATE (never both, never two). That is the rotation source's #1 READY ability. All other ready abilities cap at AVAILABLE (unlisted). SOON / JUDGE / SEQUENCE and the resourceBar are NOT press claims and MAY coexist with the one ROTATION/LATE.
    * ROTATION = press this now. LATE = the same press, but overdue (you've been sitting on it -- use when readable evidence shows it's been available a while, e.g. shards capped for seconds, or a hard-CD long past due).
    * SOON = anticipating, not yet pressable (a napkin countdown; e.g. Tyrant ~2s out). NOT a press.
    * JUDGE = a your-call availability we can't instruct because the gate is secret (Implosion imp-count; hold-for-burst). Coexists with the ROTATION press.
    * SEQUENCE = attention-redirect: "look at the sequence PANEL." Not a press, not a step. Fires when the panel holds the salient plan (opener active). Coexists.
- \`transient\` (optional per cue, a phase EDGE): cast_started, cast_ended, ready, proc. Justify from history/glow. Omit if steady-state (a persistent proc is NOT a transient -- see demonbolt-proc).
- \`sequence\`: { "show":false } normally. For opener/burst panes: { "show":true, "title":<pass-through>, "cursor":N, "steps":[ { "spellID":..,"label":<pass-through>,"keybind":"..","state":<stepState>,"note":<pass-through|omit> } ] }. stepState: done, active, pending, blocked, skipped.
- Pass-through strings (the ONLY place class vocab may appear): cue.note, sequence.title, step.label, step.note. Everything else is a bounded token.

## STATE FIXTURE RULES (each state.json must be physically realizable)
- Copy the EXACT field structure of the template goldens (every cd entry carries cooldownID, spellID, overrideSpellID, overrideTooltipSpellID, liveSpellID, linkedSpellIDs, category, selfAura, hasAura, charges, isKnown, flags, keybind, cd, charge, aura, glow; TrackedBuff frames also carry buff).
- Carry a DECISION-RELEVANT SUBSET (~6-8 cd entries) -- the rotational buttons + relevant buffs that determine the ranking. Not all 64.
- \`liveSpellID\` must equal \`spellID\` UNLESS a transform: then set overrideSpellID = liveSpellID = the transform target (434635 Ruination on 34991, 434506 Infernal Bolt on 34990). (Identity-coherence invariant.)
- NO spec/rotation vocabulary as State keys (no "role","builder","spender","emphasis","primary","judgeable", etc.). State is spec-agnostic; the rotational MEANING lives only in guidance.json + rationale.md.
- history entries: { "phase":"start"|"succeeded", "spellID":<base>, "base":<base>, "at":<t> }.
- Combat fixtures: set "combat": true, a "combatStartedAt", "mode":"st" (or "aoe" where the scenario needs it). Keep "at" ~1000.0 like the templates.

## OUTPUT -- write THREE files, then return the structured summary
Write (via the Write tool) to ${GOLD}/<SCENARIO>/ :
  1. state.json      -- the synthetic State pulse (valid JSON; _scenario + _note lead keys ok)
  2. guidance.json   -- the expected Coach output (valid JSON; _scenario + _expected lead keys ok)
  3. rationale.md    -- WHY this Guidance follows from the READABLE state + the rotation source:
       the winner's APL/source justification, WHY each loser is demoted (AVAILABLE not drawn),
       the readability caveats (what's secret, what readable signal stands in), and which contract
       invariants the case exercises. Mirror the depth of the template rationale.md files.
Then call StructuredOutput with your summary. Self-check before returning: does EVERY drawn cue
trace to a readable signal? Is there AT MOST ONE ROTATION/LATE? Did you avoid reading addon code?
`

const DERIVE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['scenario', 'wroteAllThree', 'cues', 'resourceBar', 'sequenceShown', 'readableOnlySelfCheck', 'notes'],
  properties: {
    scenario: { type: 'string' },
    wroteAllThree: { type: 'boolean', description: 'state.json + guidance.json + rationale.md all written' },
    resourceBar: {
      type: 'object', additionalProperties: false, required: ['value', 'incoming'],
      properties: { value: { type: 'number' }, incoming: { type: 'number' } },
    },
    cues: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false, required: ['cooldownID', 'emphasis'],
        properties: {
          cooldownID: { type: 'string' },
          emphasis: { type: 'string', enum: ['SOON', 'ROTATION', 'LATE', 'JUDGE', 'SEQUENCE'] },
          transient: { type: ['string', 'null'] },
        },
      },
    },
    sequenceShown: { type: 'boolean' },
    readableOnlySelfCheck: { type: 'string', description: 'Attest: every drawn cue traces to a readable signal (name them); note any secret-gated softening.' },
    notes: { type: 'string' },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['scenario', 'lens', 'verdict', 'issues', 'suggestedFix'],
  properties: {
    scenario: { type: 'string' },
    lens: { type: 'string' },
    verdict: { type: 'string', enum: ['PASS', 'REVISE', 'FAIL'] },
    issues: { type: 'array', items: { type: 'string' } },
    suggestedFix: { type: 'string', description: 'Concrete fix if REVISE/FAIL; empty if PASS.' },
  },
}

// ---------------------------------------------------------------------------
// The 18 remaining scenarios. Each brief states the SITUATION and the EXPECTED
// call at a high level; the agent DERIVES the exact fixture + guidance from the
// source, and must justify (not just transcribe) it.
const SCENARIOS = [
  // A - positive priority (single ROTATION press)
  { name: 'tyrant-ready', brief: `Combat; Tyrant (2742) is off cooldown (napkin probably-up: state unknown/source napkin) with **5 shards** and the summon board fresh (Dreadstalkers 671 + Grimoire Imp Lord 135056 recently out -- buff.isActive true on their frames, or freshly cast per history). Dreadstalkers may also read probably-up but Tyrant is the go. EXPECT: Tyrant ROTATION (5 shards + fresh board = the burst window, source step 6). Others AVAILABLE (unlisted). bar 5/5. NO burst pane here.` },
  { name: 'dreadstalkers', brief: `Combat, OUTSIDE a Tyrant window, Tyrant far away (napkin anticipated, remaining ~35s). Dreadstalkers (671) off cd (napkin probably-up). ~3 shards, no Core. EXPECT: Dreadstalkers ROTATION (press on cd when Tyrant isn't imminent -- source step 5 / "on CD"). Others AVAILABLE. bar 3/5. Contrast with soon-anticipated (where Tyrant NEAR makes you stage instead).` },
  { name: 'shadow-bolt-filler', brief: `Combat; nothing else lit -- no Core (777 buff inactive, no glow on 1979), summons cooling (napkin anticipated), HoG not castable (shards <3), no Art armed. Only Shadow Bolt (34990) is the play (build shards). EXPECT: Shadow Bolt ROTATION (filler, source step 12). bar 1/5. This exercises the base filler when the buckets are empty.` },
  { name: 'ruination', brief: `Combat; Pit-Lord Demonic Art armed (Diabolic Ritual 9426 buff.isActive true; the HoG frame 34991 is TRANSFORMED: overrideSpellID=liveSpellID=434635, and glow.active true on it). 3+ shards so it's castable. EXPECT: Ruination ROTATION on cooldownID 34991 (the transformed HoG -- free triple-imp, source: "when Pit-Lord Art armed, next HoG = Ruination; prefer entering/inside Tyrant"). Note in rationale the source prefers firing it in the Tyrant window, but on-cd it's still the press here. Others AVAILABLE. bar e.g. 4/5.` },
  { name: 'infernal-bolt', brief: `Combat; Mother-of-Chaos Art armed (9426 buff.isActive; SB frame 34990 TRANSFORMED: overrideSpellID=liveSpellID=434506, glow.active true). Shard-STARVED: shards <3 (IB is a 3-shard BUILDER, self-gated to <3). EXPECT: Infernal Bolt ROTATION on cooldownID 34990 -- ranks ABOVE Demonbolt when shard-starved (best builder; source step 10 / "Infernal Bolt if <3 shards"). bar 1/5. Mirror of ruination but on the SB frame.` },
  { name: 'in-tyrant-window', brief: `Combat; **Tyrant window ACTIVE** (2742 frame buff.isActive true = the window is up). Imps out (143038 active). 4 shards. Core up (777 active + glow on 1979). The single most important DPS window. EXPECT: HoG (34991) ROTATION -- flood imps: inside Tyrant, HoG spam is the priority (source SEQUENCE 3 "HoG HoG opens the window", maxroll "cast as many HoG as possible for 15s"). Demonbolt AVAILABLE (dump cores BETWEEN HoGs, not the top press). bar 4/5.` },
  { name: 'implosion-primed', brief: `Combat; Implosion (149122) off cd (napkin probably-up); imps out (143038 active, count SECRET). The imp-NAPKIN is CONFIDENT: history shows >=2 recent FULL Hand-of-Gul'dan casts (spell 105174 succeeded, ~3 imps each), NO Implosion cast since, within a conservative window (mode:aoe or Tyrant-up). EXPECT: Implosion ROTATION -- napkin-confident promote (per the review: promote to ROTATION when the estimate is confident; conservative window under-counts -> errs to JUDGE, so a confident state is a real press). This is the POSITIVE twin of the committed \`implosion\` golden (which stays JUDGE when NOT confident). bar e.g. 2/5. mode:aoe.` },
  // B - negative / must-not-instruct
  { name: 'grimoire-available', brief: `Combat; Grimoire: Imp Lord (135056) off cd (napkin probably-up). Steady state otherwise (a normal build/spend press exists, e.g. HoG at 3 shards). EXPECT: Grimoire draws AVAILABLE -- meaning it is NOT suppressed but is NOT a standalone ROTATION either; the SEQUENCE/pane drives its actual press (paired next to Dreadstalkers before Tyrant, source SEQUENCE 2). Represent this as: Grimoire UNLISTED (draw:false = AVAILABLE internal) while the readable build/spend winner (e.g. HoG) is the one ROTATION. In rationale, explain WHY Grimoire is not independently greened (its correct press is a sequence position, not a lone light). Use mode:aoe (Imp Lord is the meta grimoire).` },
  { name: 'overcap-soften', brief: `Combat; Core up (777 active + glow on 1979) BUT **4 shards** -- casting Demonbolt is fine (instant) yet HoG must dump first or the next builder overcaps. EXPECT: HoG (34991) ROTATION (dump shards first). Demonbolt (1979) drawn AVAILABLE... but AVAILABLE is internal/no-cue -- instead express the SOFTEN as: HoG ROTATION, and Demonbolt gets a cue with note "core up -- spend shards first" but NOT a press emphasis. Since the only non-press coexisting tokens are SOON/JUDGE/SEQUENCE, model the softened Demonbolt as unlisted (AVAILABLE) and carry the "spend first" reasoning in rationale; OR if a visible informational cue is wanted, keep Demonbolt unlisted and let HoG's ROTATION + bar 4/5 carry it. Choose the contract-legal representation and justify it. bar 4/5. (This is also the home for IB's self-gate note.)` },
  { name: 'burst-hold', brief: `Combat; burst branch imminent -- Tyrant ~15s out (napkin anticipated, remaining ~15). Dreadstalkers (671) AND Implosion (149122) both off cd (napkin probably-up). A build/spend ROTATION press still exists underneath (e.g. HoG at shards). EXPECT: Dreadstalkers JUDGE + Implosion JUDGE ("hold for burst -- your call": press on cd, or hold to stage the window), WITH the build/spend ROTATION winner (e.g. HoG) coexisting. This is the ONLY cue-logic change when burst is available (burst model). Two JUDGE + one ROTATION is contract-legal (JUDGE coexists). bar e.g. 3/5.` },
  // C - cross-cutting emphasis edges & channels
  { name: 'overdue-late', brief: `Combat; Dreadstalkers (671) has been ready a while (~6s overdue) AND Tyrant is FAR / long CD (napkin anticipated, remaining large) so you're NOT pooling for it. Readable evidence of overdue: the napkin estimate elapsed a while ago (state unknown/source napkin, changedAt old) -- honest LATE. EXPECT: Dreadstalkers LATE (overdue; the SOLE press winner -- LATE is the single-top-press in its overdue form). Others AVAILABLE. Qualifier in rationale: if Tyrant were NEAR this would be burst-hold JUDGE, not LATE. bar e.g. 3/5.` },
  { name: 'hog-overcap-late', brief: `Combat; **5 shards, capped ~3s** (readable: power value 5, and history shows the last builder landed ~3s ago with no spend since -> you've been sitting at cap). No Core. Summons cooling. EXPECT: HoG (34991) LATE -- the READABLE overdue dump (shards are readable, so this LATE is fully justified, unlike a secret-cd LATE). bar 5/5. Note in rationale: the Demonbolt-at-4-cores LATE is NOT assertable because Core STACK count is secret -- a documented readability limit; this shard-cap LATE is the readable one.` },
  { name: 'soon-anticipated', brief: `Combat; Tyrant (2742) ~2s out (napkin ANTICIPATED: state anticipated, remaining ~2.0, source napkin). Summons not all out yet. Shards being banked (~4) to flood HoG inside the window. EXPECT: the staging press is Dreadstalkers ROTATION (stage/pool before Tyrant -- source SEQUENCE 2 "Dreadstalkers is the last thing before Tyrant"), Tyrant SOON + a countdown-ish note. IMPORTANT correction baked in by the review: pre-Tyrant you do NOT spend HoG (shards banked for the window) -- so HoG is NOT the press here. SOON is not a press and coexists with the one ROTATION. bar 4/5.` },
  { name: 'soon-incoming', brief: `Combat; a SPENDER is anticipated because INCOMING shards will meet its cost -- the REVERSE of the committed incoming-overcap golden. E.g. 2 shards NOW + a Shadow Bolt in flight (history start for 686, no succeeded) -> incoming:+1 -> projected 3, which is exactly HoG's cost. HoG isn't castable yet (only 2 shards in hand) but WILL be the moment the shard lands. EXPECT: HoG (34991) SOON (anticipated -- the incoming shard will make it pressable; do NOT green it early, the shard hasn't landed). The current readable press is Shadow Bolt ROTATION (keep building / the in-flight cast). bar { value:2, incoming:1 }. Exercises incoming driving a SOON anticipation (spender side).` },
  { name: 'opener-midflight', brief: `Combat; the OPENER sequence is active (source SEQUENCE 1). Dreadstalkers + Grimoire Imp Lord already cast (done), cursor ON Tyrant (active), HoG pending after. Include a BLOCKED step (e.g. a step gated on a resource with a note) and a SKIPPED step (a drop-through, e.g. Implosion step only when mode:aoe -- skipped in st) to exercise all stepStates. EXPECT: sequence { show:true, title:"OPENER", cursor:2, steps:[done, done, active(Tyrant), pending(HoG), ...] } AND the active-step cue Tyrant: SEQUENCE (attention-redirect to the panel). Use real spellIDs/keybinds from the anchor table for steps. This is the ONLY scenario exercising the sequence pane + SEQUENCE emphasis + all stepStates.` },
  { name: 'resource-states', brief: `Combat; a resourceBar-focused fixture. Pick the shard value NOT already represented by other goldens to widen coverage -- e.g. **0 shards** with an in-flight Shadow Bolt (incoming:+1) so the bar shows value:0, incoming:1, an empty-but-filling meter. The readable press is Shadow Bolt ROTATION (building from empty). EXPECT: bar { value:0, incoming:1, max:5, display:"discrete", powerType:"SOUL_SHARDS" }, Shadow Bolt ROTATION. In rationale, note the bar renders discrete segments and that Soul Shards are always readable (never secret). Primarily a resourceBar/incoming channel test.` },
  { name: 'transient-edges', brief: `Combat; a fixture whose readable signals justify a transient EDGE on cues. Pick ONE clean, well-justified edge set (don't fake several at once): e.g. a Hand of Gul'dan cast just COMMITTED -> history has a \`start\` for 105174 with no \`succeeded\` -> HoG cue carries transient:"cast_started" (still the ROTATION press or its follow-through). Also justify one \`ready\` edge (a hard-CD whose napkin just flipped to probably-up this pulse -- changedAt == at) and one \`proc\` edge (glow.active on Demonbolt just turned true this pulse -- the ARMING edge, distinct from demonbolt-proc's steady-state). Keep single-top-press. In rationale, explain each edge is fired on the TRANSITION and how the state marks "this pulse" (changedAt/history at == pulse at). This is the transient-channel coverage scenario -- aim to exercise cast_started, ready, and proc (cast_ended can be a second cue or noted).` },
  { name: 'secrecy-combat', brief: `Combat; the readability discipline stress test. ALL cds readable:false (napkin/none); shards readable; Core read via buff.isActive(777)+glow(1979) with aura.readable:false everywhere; Tyrant napkin-anticipated. EXPECT: cues derive from READABLE values ONLY -- e.g. Demonbolt (1979) ROTATION (Core via buff/glow, inherits the demonbolt-proc readable-approx caveat), Tyrant (2742) SOON (napkin). NO cue cites a secret cd or aura. Largely a State-contract + secrecy-gate test: the point is that every drawn cue is traceable to a readable signal despite everything cd-shaped being dark.` },
]

// ---------------------------------------------------------------------------
phase('Derive')
log(`Deriving ${SCENARIOS.length} goldens (1 derive + 2 adversarial verify each)...`)

const results = await pipeline(
  SCENARIOS,
  // Stage 1: DERIVE -- author the three files, return a structured summary.
  (s) => agent(
    `${SHARED}\n\n## YOUR SCENARIO: \`${s.name}\`\nWrite to ${GOLD}/${s.name}/\n\nSITUATION + EXPECTED CALL (derive the exact fixture + guidance from the source; justify, don't just transcribe):\n${s.brief}\n\nRemember: at most ONE ROTATION/LATE; list only cues that DRAW; every drawn cue must trace to a READABLE signal; do NOT read addon code.`,
    { label: `derive:${s.name}`, phase: 'Derive', agentType: 'general-purpose', schema: DERIVE_SCHEMA },
  ),
  // Stage 2: VERIFY -- two adversarial lenses, run concurrently once derive lands.
  (d, s) => parallel([
    () => agent(
      `You are an ADVERSARIAL rotation-correctness reviewer for one Demonology golden. Files: ${GOLD}/${s.name}/state.json, guidance.json, rationale.md. Rotation source (the ONLY authority): ${KB}/rotation.md and ${KB}/diabolist-sequences.md (parse data wins on conflict). Do NOT read any addon code.\n\nSCENARIO INTENT:\n${s.brief}\n\nYour job: try to REFUTE the winner. Read state.json + guidance.json. Ask: is the single ROTATION/LATE cue REALLY the rotation source's #1 READY ability given this readable state? Are the demoted (unlisted/AVAILABLE) abilities correctly NOT the call? Is any SOON/JUDGE/SEQUENCE mis-assigned? Is the shard/incoming math right? Does the pick respect: don't-spend-HoG-pre-Tyrant, IB<3-shards-self-gate, Implosion-secret-gate, in-Tyrant-HoG-flood? Default to flagging if uncertain. Return REVISE/FAIL with a concrete fix if the winner is wrong or a loser is mis-ranked; PASS only if the ranking is defensibly the source's call.`,
      { label: `v-rot:${s.name}`, phase: 'Verify', agentType: 'general-purpose', schema: VERDICT_SCHEMA },
    ),
    () => agent(
      `You are a CONTRACT + SECRECY conformance reviewer for one Demonology golden. Contract: ${PROJ}/guidance-contract.json. Files: ${GOLD}/${s.name}/{state.json,guidance.json,rationale.md}. Do NOT read addon code.\n\nCheck guidance.json against the contract: (1) every emphasis token in {SOON,ROTATION,LATE,JUDGE,SEQUENCE}; every transient in {cast_started,cast_ended,ready,proc}; every stepState in {done,active,pending,blocked,skipped}; display in {discrete,percentage}. (2) NO rgba / pixel arrays anywhere; resourceBar carries powerType token not colour. (3) SINGLE-TOP-PRESS: at most ONE drawn cue is ROTATION or LATE. (4) Every drawn cue's cooldownID is anchored in state.cooldowns. (5) Pass-through strings only in cue.note/sequence.title/step.label/step.note. (6) SECRECY GATE (the crux): since combat:true, NO drawn cue may rest on a secret signal -- verify each drawn cue in the rationale traces to a READABLE signal (power/shards, glow.active, buff.isActive, or a napkin cd estimate) and NOT to a live-readable cd (combat cds must be readable:false) or an aura (must be readable:false in combat). Also sanity-check state.json realism: napkin honesty (no napkin "ready"; anticipated has remaining>0; unknown has none), identity coherence (liveSpellID diverges only via override/transform 434635/434506), no spec-vocab State keys, power keyed "SoulShards". Return REVISE/FAIL with the exact offending field + fix; PASS only if fully conformant.`,
      { label: `v-con:${s.name}`, phase: 'Verify', agentType: 'general-purpose', schema: VERDICT_SCHEMA },
    ),
  ]).then((verdicts) => ({ scenario: s.name, derive: d, verify: verdicts.filter(Boolean) })),
)

// ---------------------------------------------------------------------------
phase('Synth')
const clean = results.filter(Boolean)
const flagged = clean.filter(r => (r.verify || []).some(v => v && v.verdict !== 'PASS'))
log(`Derive+verify done: ${clean.length}/${SCENARIOS.length} scenarios; ${flagged.length} carry a REVISE/FAIL flag.`)

const synth = await agent(
  `You are the coverage SYNTHESIZER for the W4 Phase-2 golden corpus. Read EVERY scenario dir under ${GOLD}/ (there are 4 pre-existing: hand-of-guldan, demonbolt-proc, implosion, incoming-overcap; plus the 18 just authored). For each, read guidance.json.\n\nBuild a coverage report over the contract vocab (${PROJ}/guidance-contract.json): which scenarios exercise each emphasis member (SOON/ROTATION/LATE/JUDGE/SEQUENCE), each transient (cast_started/cast_ended/ready/proc), each stepState (done/active/pending/blocked/skipped), each display (discrete/percentage), and the resourceBar incoming projection (zero / positive / negative). Note any vocab member NOT exercised by any golden (a GAP -- e.g. percentage display has no Demo home; that's an expected gap, say so). Also flag any scenario whose guidance looks malformed.\n\nWrite ${GOLD}/coverage.md: a table (vocab member -> scenarios covering it), a GAPS section (each gap + whether it's expected or a real hole to fill), and a one-line status. Do NOT read addon code. Then return the structured summary.`,
  {
    label: 'synth:coverage', phase: 'Synth', agentType: 'general-purpose',
    schema: {
      type: 'object', additionalProperties: false,
      required: ['scenariosSeen', 'coveredEmphasis', 'coveredTransient', 'coveredStepStates', 'gaps', 'wroteCoverageMd'],
      properties: {
        scenariosSeen: { type: 'number' },
        coveredEmphasis: { type: 'array', items: { type: 'string' } },
        coveredTransient: { type: 'array', items: { type: 'string' } },
        coveredStepStates: { type: 'array', items: { type: 'string' } },
        gaps: { type: 'array', items: { type: 'string' } },
        wroteCoverageMd: { type: 'boolean' },
      },
    },
  },
)

return {
  scenarios: SCENARIOS.length,
  derived: clean.map(r => ({
    scenario: r.scenario,
    wrote: r.derive && r.derive.wroteAllThree,
    verdicts: (r.verify || []).map(v => `${v.lens}:${v.verdict}`),
  })),
  flagged: flagged.map(r => ({
    scenario: r.scenario,
    issues: (r.verify || []).filter(v => v.verdict !== 'PASS').flatMap(v => v.issues.map(i => `[${v.lens}] ${i}`)),
    fixes: (r.verify || []).filter(v => v.verdict !== 'PASS').map(v => v.suggestedFix).filter(Boolean),
  })),
  coverage: synth,
}

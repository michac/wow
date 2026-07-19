# Cooldown HUD — guidance model (what to signal, when, and how)

> The **rotation-helper contract**: the overlay's real job isn't decoration, it's
> guiding the Demonology rotation *within the Secret-Values wall*. This doc turns
> the rotation into a ranked list of salience moments, researches the attention
> mechanisms that can carry them, and maps each moment to a readable signal we can
> actually build. It is the contract M3–M6 widgets implement.
>
> **Doc map (§ cross-refs):** §0 Direction + §3 Design language → `spec.md` ·
> **§0.5 Guidance model → this doc** · §1–§2, §4–§5, §9 (Secret-Values findings /
> architecture / provenance) → `notes.md` · §6 Milestones + §7 Open questions →
> `milestones.md`.
>
> **Scope:** v1 = **Diabolist** Demonology Warlock (the profile default in
> `rotation.md` and `notes.md` §2). Soul Harvester is out of scope for the moment
> list. **Ships no addon code** — this milestone (M0.5) is documentation only.

---

## 0.5 Guidance model

The realization that spawned this doc (2026-07-18): the overlay is a **rotation
helper**, not just a themed skin. A skin makes Blizzard's Cooldown Manager
*prettier*; a rotation helper makes the *next decision* pop. This is not just a
preference — it's the documented lesson of the built-in CDM's own launch, which was
judged "dead on arrival" precisely because it showed every cooldown in an
undifferentiated, uncustomizable order (§0.5.3 [M3]). Our job is the **spec-specific
salience and ordering the raw feature lacks**. Everything below
exists to answer one question per widget — *"what instant does a good Demo player
change behaviour, and what's the cheapest cue that gets their eye/ear there
without them reading?"* — and to answer it **honestly** inside the wall that 12.0
"Secret Values" puts around combat state (`notes.md` §1).

Three layers, coarse-to-fine:

- **§0.5.1** — the *archetype* (why the rotation is shaped this way) and the
  *modes* (the coarse "what phase am I in" states we can compute).
- **§0.5.2** — the *moments* (the fine-grained "what do I press next and why"),
  ranked.
- **§0.5.3–0.5.6** — the *mechanisms* (§0.5.3), the *map* from moment → readable
  signal (§0.5.4), the *blind spots* (§0.5.5), and the *widget backlog* (§0.5.6).
- **§0.5.7** — *open research* the M0.5 fan-out left uncovered (the Strand-B gap).

---

## 0.5.1 Mechanical archetype & rotational modes

### The archetype: builder/spender funnelled into a periodic burst

Demonology is a textbook **builder/spender** (a.k.a. *generate-and-spend*)
resource spec — and, precisely, a **two-overflow-bucket** one
(`diabolist-sequences.md`, mined from the current top-6 parses): you keep two
buckets from spilling and press things on cooldowns.

- **Bucket 1 — Soul Shards** (cap 5; `UnitPower` also exposes fragments 0–50, but
  the actionable unit is the whole shard). Spender: **Hand of Gul'dan** (3 shards →
  Wild Imps). Builder: **Shadow Bolt** (→ **Infernal Bolt**, a free transform, +3
  shards).
- **Bucket 2 — Demonic Core** (cap 4). Spender: **Demonbolt** (instant, hits
  harder). Cores are *Core-rich* — they overflow on their own (~131 procs/fight,
  fed passively by pets), so **Power Siphon is skipped** in the modern build (0
  casts across all six top parses); "Demonbolt when you have a couple" suffices.

Both buckets **funnel into the Summon Demonic Tyrant window** (60 s CD), which
empowers and extends every active demon — so the shards you bank and the imps you
summon are really *staged for a periodic burst payoff*. Overcapping *either* bucket
is a flat DPS loss.

This is the same design pattern as **rogue combo points, monk chi, DK runic power,
paladin holy power**: a resource you accumulate through basic actions and trade in
bulk for a disproportionate reward. Naming the archetype matters because it tells
us **which moments carry tension**, and tension is where salience belongs:

- **Overcap tension (waste-avoidance).** Both buckets punish overcap — generation
  past the cap is *lost value*. So "at cap" is a **hard gate**. Crucially for us the
  two buckets differ in readability: the **Soul Shard count is readable** (`UnitPower`
  — our strongest signal, §0.5.2 #1), whereas the **Demonic Core count is secret**
  (`Applications`), so we can only signal Core *presence*, not "near cap 4" (§0.5.5).
- **Bank-for-burst tension (timing).** The opposite pull: *don't* dump everything
  the instant you can, because Hand of Gul'dan casts are worth far more **inside**
  the Tyrant window (`rotation.md`: "the single biggest DPS lever is how many Hand
  of Gul'dan casts fit inside the Tyrant window"). So the rotation has a
  *rhythm* — build/hold, then spend hard on a ~60 s cadence — and the HUD's job is
  to communicate **which half of that rhythm you're in**. That is exactly what the
  mode model below encodes.

The designer intent, stated plainly: *reward players who manage the waste-vs-hold
tension around a periodic burst.* A rotation helper that only blinked "cooldown
ready" would miss the whole spec — the interesting decision is *when to spend what
you've banked*, and that decision is **computable from data we can read** (shards +
proc presence + napkin timers), which is the good news of this whole milestone.

> This archetype framing is derived from the rotation's own structure
> (`rotation.md`, `notes.md` §2, `diabolist-sequences.md`) and is now backed by the
> Strand-B research (§0.5.3): the cap-as-opportunity-cost and damage-now-vs-later
> tensions are the *designed* engagement drivers **[B1][B2]** — which is exactly why
> the overcap gate and the bank↔spend axis are where salience belongs. (WoW-class-
> resource-*specific* psychology stayed a softer, community-tier source — §0.5.7.)

### The modes: generate → spend → burst (computable, no secret reads)

Because Soul Shards are **readable *and* branchable** in restricted combat
(`notes.md` §1 — our single strongest capability) and proc presence is readable
via `item:IsShown()`, the rotation's *coarse phase* is something we can actually
**compute and surface**. That turns a pile of independent blinkers into a
**rotation-helper spine**: one "what mode am I in" indicator that frames every
finer cue.

Three modes. Every entry/exit trigger below uses **only readable data** — Soul
Shards (`UnitPower`), buff/proc presence (`IsShown`), and player-cast napkin
timers (`UNIT_SPELLCAST_SUCCEEDED` → `GetSpellBaseCooldown`, `notes.md` §1) — so
the indicator is fully ours to drive.

| Mode | Entry trigger (readable) | Exit trigger (readable) | Dominant action |
| --- | --- | --- | --- |
| **GENERATE** | Shards low (`< 3`, can't afford Hand of Gul'dan) **and** Tyrant not imminent (napkin timer `> ~15 s`) | Shards reach `≥ 3`, **or** the burst window opens | Shadow Bolt (→ Infernal Bolt when the Mother-of-Chaos Art is armed, +3 shards) to rebuild — the `SB SB` refill run |
| **SPEND** | Shards `≥ 3` (can afford Hand of Gul'dan) and not in the burst window | Shards drop `< 3`, **or** the burst window opens | The `HoG ↔ DB` alternation: Hand of Gul'dan (dump shards) interleaved with Demonbolt (dump Cores) — plus any armed Demonic Art transform |
| **BURST / TYRANT** | Tyrant napkin timer `≈ 0` (near-ready) **and** the pre-Tyrant summons are staged (Call Dreadstalkers is the *last* cast before Tyrant; Grimoire: Imp Lord beside it when up — tracked off our own casts) | Tyrant napkin window elapses (`~15 s` after the Tyrant cast) | Summon Demonic Tyrant, then open with `HoG HoG` and chain Hand of Gul'dan (Dominion of Argus refunds shards) + Demonbolt; land Ruination here |

**Design notes on the modes:**

- The modes are **ordered by shard fill and Tyrant proximity**, which is why they
  compute cleanly — the two axes we read best (shards, napkin timer) *are* the mode
  axes. GENERATE↔SPEND is essentially a shard threshold; SPEND→BURST is the Tyrant
  timer crossing zero with a staged board.
- **BURST-window readiness is a best-guess, honestly flagged.** A *true* "the
  summon cooldowns are up right now" boolean would require reading their
  cooldown-ready states, which are **secret** (`notes.md` §1). We approximate it
  from **napkin timers off our own casts** (fixed base CDs — Tyrant 60 s,
  Dreadstalkers ~20 s, Imp Lord ~2 min), which **drift** on haste-scaled recharge /
  CDR procs (§0.5.5). So the mode indicator should treat BURST as *"looks ready —
  go"*, not a guarantee, and lean on Blizzard's borrowed swipe/native ready-alert
  for the ground truth of any single cooldown. In practice the anchor is simple:
  **Tyrant is on a fixed 60 s clock and Dreadstalkers is the last cast before it**,
  so the napkin-timed Tyrant countdown carries most of the burst-staging signal.
- The mode indicator is a **first-class output** and its own candidate widget
  (§0.5.6) — it communicates *phase* without text (ambient state colour, §0.5.3),
  and it's the frame the §0.5.2 moments hang on.

---

## 0.5.2 Salience moments (ranked)

The fine grain: the instants a good Diabolist Demo player changes what they press,
distilled from the ST + AoE priority in `rotation.md`, the top-6-parse cast-stream
analysis in `diabolist-sequences.md`, and the salience drivers in `notes.md` §2.
Each moment carries a **trigger**, the **decision** it drives, a
**priority tier**, and the **mode(s)** it lives in. The own/borrow/can't
classification and the chosen attention mechanism are in the §0.5.4 map; the
mechanism rationale is in §0.5.3.

**Priority tiers:** **P0** = hard gate, inaction is strictly wrong (never miss) ·
**P1** = high-value, shapes burst throughput · **P2** = situational / conditional ·
**P3** = ambient / decluttering.

| # | Moment (trigger) | Decision it drives | Tier | Mode(s) |
| --- | --- | --- | --- | --- |
| 1 | **Soul Shards at cap (5)** — `UnitPower == max` | Stop generating; spend a Hand of Gul'dan **or** commit Tyrant. Overcap = wasted generation. | **P0** | SPEND, BURST |
| 2 | **Demonic Core proc present** — buff item `IsShown()` | Cast Demonbolt (spend cores before they overcap; also refills shards). | **P0** | GENERATE, SPEND |
| 3 | **Tyrant ~ready** — napkin timer off our Tyrant cast nearing 0 (fixed 60 s) | Pre-stage the board: fire **Call Dreadstalkers** (+ Grimoire: Imp Lord if up) just *before* Tyrant — Dreadstalkers is the last cast before it. | **P1** | → BURST |
| 4 | **Burst window "all up = go"** — the pre-Tyrant summons available together just before Tyrant | Commit the burst sequence (Tyrant + the demons it empowers), then `HoG HoG`. | **P1** | BURST |
| 5 | **Shards `≥ 3`, Tyrant `> 5 s` away** — `UnitPower ≥ 3` and not bursting | Hand of Gul'dan now (generate imps; don't drift toward overcap). | **P2** | SPEND |
| 6 | **Wild Imps present** — Wild Imp buff-icon `IsShown()` | On 3+ targets, Implosion becomes relevant **at ≥6 imps** (15 s CD). | **P2** | any (AoE) |
| 7 | **Dominion of Argus (apex) up** — buff bar `IsShown()` | Hand of Gul'dan immediately — the proc makes it free/empowered and refunds shards to chain HoG in the Tyrant window. | **P2** | SPEND, BURST |
| 8 | **A tracked cooldown becomes ready** — observed off the hooked ready-alert edge (`TriggerAvailableAlert` / `OnCooldownDone`), *not* a secret read | Use the cooldown per the fixed priority order. | **P1** | any |
| 9 | **Board cleared / all-quiet** — no procs shown, shards low, nothing actionable | Nothing — recede, declutter. "Empty board = nothing to do." | **P3** | GENERATE (idle) |
| 10 | **Demonic Art armed (Diabolic Ritual)** — the ritual/art buff-icon `IsShown()` (tracked buff `428514`, `notes.md` §2) | Take the free transform: next Hand of Gul'dan → **Ruination** (3 free imps — save for the Tyrant window), or next Shadow Bolt → **Infernal Bolt** (+3 shards — take when shard-starved). | **P1** | GENERATE, SPEND, BURST |

**Notes on specific moments:**

- **#1 is the anchor.** It's the P0 waste-gate *and* our strongest capability
  (readable + branchable). If exactly one cue survives every accessibility/mute
  ceiling, it is shard-cap.
- **#2 fuels both halves.** A Demonic Core proc is spent via Demonbolt in GENERATE
  (rebuild shards) and SPEND (avoid core overcap); its *presence* is readable, its
  *stack count* is not (§0.5.5).
- **#6 has a secret gate.** Imp *presence* is readable, but the **≥6-imp Implosion
  threshold** and the 3+-target condition depend on the imp **count** (`Applications`),
  which is **secret** (`notes.md` §1). We can surface presence and enlarge
  Blizzard's own stack text, but we cannot compute "≥6" ourselves — a flagged blind
  spot (§0.5.5).
- **#10 is deterministic-in-order, reactive-in-timing.** The Diabolic Ritual wheel
  turns Overlord → Mother of Chaos → Pit Lord in a *fixed order*, so the active
  ritual stage **predicts** which Art arms next (`diabolist-sequences.md`) — a
  tracked-buff `IsShown` per stage lets us glow the *right* transformed button and
  even pre-warn it. The simple version (glow the transform when its Art is armed) is
  the moment above; the predictive version (surface which Art is coming) is a richer
  M4/M5 elaboration.
- **Power Siphon is intentionally *not* a moment.** The simc APL fires it at low
  Core stacks (≤1), but (a) the stack *count* is secret and (b) the modern Core-rich
  build **skips Power Siphon entirely** (0 casts across the top parses,
  `diabolist-sequences.md`) — so it's doubly not something we signal. See §0.5.5.

---

## 0.5.3 Attention mechanisms (research digest)

Three deep-research fan-outs for M0.5 (multi-source web search → fetch → 3-vote
adversarial verify → cited synthesis). **Pass 1 — Strand A** (perceptual + auditory
+ accessibility science; 24 claims) is thoroughly verified against Tier-1 primary
sources. **Pass 2 — Strand B** (builder/spender *design theory*, text-free
mode/phase communication, CDM prior art, earcon-set ceiling; 8 claims) resolved the
game-design topics the first pass missed — authoritative designer writing +
peer-reviewed auditory science. **Pass 3 — rotation-helper landscape** (Hekili /
MaxDps / Blizzard Assisted Highlight models; 9 claims from addon repos/docs +
Blizzard news). Two residual gaps stay honest in §0.5.7 (WeakAuras' own conventions
and the "tunnel-vision" failure mode were not reached). Principle IDs
(**[V*]**/**[J*]**/**[A*]**/**[X*]** visual+audio+access; **[B*]**/**[M*]**
resource-loop + mode; **[R*]** rotation-helper models) are referenced from the
§0.5.4 map.

### Visual salience toolbox

- **[V1] Glanceability budget ≈ 200–250 ms.** A preattentive cue must be readable in
  a glance shorter than a saccade takes to initiate (~200 ms); an abrupt onset can
  grab the eye as early as ~100 ms. Design every cue to one glance, no fixation.¹
- **[V2] One unique feature, never a conjunction.** A target defined by a *single*
  unique feature (luminance, hue, size, orientation, motion) pops out in near-constant
  time regardless of clutter; a *combination* of features loses pop-out and forces
  slow serial search — fatal in busy combat. Encode each "act now" cue on ONE
  feature.¹ ²
- **[V3] Salience hierarchy: luminance > hue > shape/texture.** Interference is
  asymmetric — luminance swamps hue, hue swamps shape. Put the most important
  attribute (readiness/urgency) on the most salient channel: a **luminance onset beats
  a hue change** for a peripheral "ready" cue.²
- **[V4] Reserve motion + abrupt onset for the single most urgent event.** Motion is
  the strongest grabber and the one feature that survives the periphery (colour/shape
  fall off there) — but travelling motion is measurably irritating, so it carries a
  real cost. Use motion/onset to draw the eye to *the* event (shard-cap, burst-go),
  not to render resting state; prefer a one-shot **anchored** pulse over continuous
  travel.¹ ³
- **[V5] Periphery kills detail, form, and colour (colour worst).** Anything read
  peripherally must ride on luminance/motion, not icon detail, shape, or hue.⁴
- **[V6] Coarse, not graded.** Subtle graded variations (slight size/opacity/intensity
  steps) fail to discriminate — especially when a *single* state is shown in isolation,
  the HUD's normal case. Make each state visibly, categorically different.³
- **[V7] Four glanceable-display principles:** match expectations (semantic mappings,
  red=danger), abstract to essentials, make elements distinct (from each other *and*
  the background), and stay **consistent** — never remap an element's
  position/colour/behaviour between phases; it disorients and slows perception. (This
  is the empirical backing for §3's role-static, never-re-sorted tiers.)³

### Game-feel "juice"

- **[J1] Juice follows an inverted-U.** Moderate-to-high feedback beats both *none* and
  *extreme* on enjoyment, motivation, and performance (N=3,018). Don't max out
  flashes/particles on every cue — **escalate juice with urgency** (subtle for routine
  builders, big for the burst window) and stay off the extreme end.⁵

### Audio / earcon toolbox

- **[A1] Urgency is engineerable, not guessable.** Pitch, tempo, harmonic irregularity,
  amplitude envelope, and repetition each monotonically drive perceived urgency
  (Stevens power-law mappable). Order the set calm→urgent by **raising pitch and
  speeding tempo** — a burst-window earcon should read higher/faster than a routine
  builder earcon.⁶
- **[A2] Keep the set small and maximally varied.** Earcon sets that are too uniform
  (shared pulse count/rhythm — the IEC 60601-1-8 failure) are hard to tell apart; vary
  **timbre AND rhythm AND pitch together**, not one dimension.⁷ The ~5–7 ceiling (the
  §3 "~6 earcons" target) is real for **arbitrary one-off sounds** (absolute
  judgement demands large differences) but is **not** a hard limit for a *structured*
  set encoded by parameter→sound rules — a rule-based 36-earcon set hit 100% ID after
  ~40 min of training.¹⁰ Our ~6 cues sit comfortably inside the easy regime.
- **[A2b] Earcon discrimination hierarchy** (when we do design bundled cues): start
  with **timbre, register, and rhythm** — use subjectively distinct instrument
  timbres ("brass" vs "organ", not "brass1/2"); **different *numbers* of notes per
  rhythm is the strongest discriminator** (similar rhythms confuse even across big
  spectral differences) — then refine with pitch/intensity.¹⁰
- **[A3] Earcons are the weakest brief-alert type — but repetition rescues them.**
  Speech/hybrid > auditory icons > abstract earcons on accuracy, reaction time, and
  liking. For rarely-heard cues prefer a distinct auditory-icon-like sound; for a
  HUD's handful of cues heard thousands of times (a highly-learned regime) earcons are
  viable. Reserve our bundled earcons for the few ours-to-drive events (shard-cap,
  proc-gained); let native alerts carry the rest — which is exactly the §3 audio
  split.⁸ Extra reason to keep it small: abstract earcons cost **>7× more to learn**
  than speech/spearcons and **compete for the same working-memory pool as gameplay**,
  degrading play; intuitive/auditory-icon sounds don't.¹¹

### Accessibility ceilings

- **[X1] Never colour-alone.** Any gameplay-critical state carried by colour must add
  ≥1 redundant non-colour signifier (shape, pattern, icon, position, or text); no key
  element relies on colour alone; make colours reassignable where feasible (Xbox XAG
  103 / WCAG 1.4.1). This is *why* §3's identity encoding is `colour(group) × position
  × 4-letter label` — redundant by design.⁹
- **[X2] Flicker ceiling.** Avoid content that flashes **more than three times in any
  one second** (WCAG 2.3.1) unless it's below the flash thresholds — the one-shot cap
  glitter and any blink cue must respect this. *(The blunt "≤3 flashes/sec, full stop"
  phrasing was refuted in verification — cite WCAG's three-flash guidance with its
  threshold exception, not an absolute.)*⁹

### Resource-loop & mode communication (Strand B)

- **[B1] Overcap = opportunity cost; signal it as a LOSS, not a reserve.** A resource
  cap deliberately turns continued generation into wasted value ("if you have all the
  sticks you'll ever need, why harvest another dirt pile?") — caps exist to stop
  hoarding and force spending. So a full/near-full bucket cue should read as an
  **actionable warning ("spend or waste")**, not a triumphant "full!". This nuances
  §3's celebratory shard-cap glitter — see the moment #1 note in §0.5.4.¹²
- **[B2] Spend satisfaction = damage-now vs damage-later opportunity cost.** The
  interesting decision is committing a banked resource to a larger delayed burst
  instead of cheaper immediate uses — which is exactly Demo's "spend now vs bank for
  the Tyrant window." Resources split into **static** (meant to be banked) vs
  **dynamic** (meant to be actively spent); Soul Shards act static approaching a
  Tyrant, dynamic otherwise. Confirms the mode model's bank↔spend axis is the
  *designed* tension worth surfacing.¹³
- **[M1] A mode reads fastest as a preattentive colour/luminance shift (<500 ms,
  pre-attention).** A full hue/luminance change is the lowest-effort non-text mode
  cue; games already **tint the character itself** to signal combat states (e.g.
  invulnerability). Validates the §0.5.4 "ambient state-colour" mode indicator — and
  that our green icon-tint is a legitimate mode-carrying channel.¹⁴
- **[M2] Blizzard's own Cooldown Manager is direct prior art for text-free phase
  signalling** — it encodes DoT/pandemic timing as **four discrete colour/luminance
  states** (greyscale+countdown → greyscale+white swipe → colourful+swipe → red
  pandemic glow), not numbers. Colour/luminance is the proven phase payload; we're
  extending a pattern Blizzard already ships.¹⁵
- **[M3] The #1 documented failure of the built-in CDM is *undifferentiated,
  uncustomizable ordering*** — the 11.1.5 launch showed every cooldown in an
  arbitrary fixed order, couldn't separate essential from utility, and was judged
  "dead on arrival"; by contrast the Single-Button Assistant (Assisted Combat) drew
  "overwhelmingly positive" feedback. **This is the empirical case for this whole
  project:** the skin's job is to impose the **spec-specific salience and ordering the
  raw feature lacks** (§3's role-static tiers, the burst lane, the mode spine) — not
  to re-skin an undifferentiated column.¹⁶

### Rotation-helper prior art — the three "what to press" models (Strand B, follow-up)

A third research pass resolved the third-party landscape (WeakAuras specifics + the
tunnel-vision failure mode still open — §0.5.7):

- **[R1] Three distinct salience models for "press this next".** **Hekili** = a
  horizontal **queue of predicted future casts** (a larger Primary icon + N smaller
  upcoming icons, re-evaluated live when you deviate; separate ST / AoE / Cooldowns /
  Defensives / Interrupts displays; configurable glow/Spellflash/range-dim). **MaxDps**
  = a **single next-ability highlight drawn onto your real action buttons** (white =
  next offensive, green = important cooldown; jumps to the next on press; **no
  queue**). **Blizzard Assisted Highlight / SBA** (`C_AssistedCombat`) = also
  **single-suggestion, no queue**, framed explicitly as an accessibility/learning aid
  (0.3 s GCD penalty on the auto-cast variant; won't fire majors, mobility, or swap
  targets; Ion Hazzikostas: "the game itself, not add-ons, should be the first answer
  to *how do I get better?*"; the recommendation core was **inspired by Hekili**).
  So **only Hekili shows a queue**; the rest show only "now".¹⁷ ¹⁸ ¹⁹
- **[R2] Overlay-on-the-bar vs dedicated display.** MaxDps and Blizzard draw *onto the
  existing action bars/frames* (no new window); Hekili renders a *separate* display.
  Our overlay is **frame-anchored** (to the CDM viewers, `notes.md` §5) — the
  MaxDps/Blizzard "on the existing UI" side of that split, not a separate predictor
  window.¹⁷ ¹⁸
- **[R3] Where *our* overlay sits — deliberately none of the three.** All three answer
  *"what ability next?"*. Ours answers *"what's my rotational **state**?"* — shards,
  proc presence, mode, burst window — which none of them surface directly and which,
  under Secret Values, is the part we *can* read. Closest kin is a **WeakAuras state
  dashboard**, not a Hekili/MaxDps "press this." This is a feature: a state helper
  sidesteps the single-suggestion "whack-a-glow" stare pattern by design (mitigation
  we already bake in via peripheral, low-motion cues — [V4][V5]), and we can't
  reliably read "the optimal next" under the wall anyway (`notes.md` §1). We *borrow*
  the "highlight on the real frame" convention ([R2]); we *reject* the "one blinking
  next-ability" model ([R3]).

*(Residual gaps — **WeakAuras**' own shared-aura salience conventions and the
**"tunnel-vision / whack-a-glow" over-reliance failure mode** — were not reached
(budget exhausted) and stay open in §0.5.7. Note [R3]'s "whack-a-glow" mitigation
therefore rests on our own [V4]/[V5] reasoning, not a cited failure-mode study.)*

**Sources (verified; Tier-1 unless noted):**
1. Healey & Enns, *Attention and Visual Memory in Visualization and Computer Graphics*
   (IEEE TVCG survey), csc2.ncsu.edu/faculty/healey/PP/ · UC Berkeley EECS-2006-113
   glanceable-displays report.
2. Healey & Enns (above); Treisman Feature Integration Theory / Callaghan psychophysics
   via same.
3. UC Berkeley EECS-2006-113 (Matthews & Forlizzi glanceable-display principles;
   qualitative designer-interview evaluation).
4. Player Research, *Perceiving without looking — designing HUDs for peripheral vision*
   (secondary; underlying physiology textbook-settled).
5. Kao/Hicks et al., *The effects of juiciness in an action RPG*, Entertainment
   Computing (N=3,018), sciencedirect.com/science/article/pii/S1875952118300879.
6. Edworthy, Loxley & Dennis, *Human Factors* (1991); Hellier & Edworthy, *Applied
   Ergonomics* (1997).
7. Edworthy, *Medical audible alarms: a review*, JAMIA (2012), PMC3628049.
8. Nees & Liebman, systematic review/meta-analysis of brief audio alerts (*Auditory
   Perception & Cognition*, 2023).
9. Microsoft Xbox Accessibility Guideline 103 (updated 2026-06-17); WCAG 1.4.1 /
   2.3.1.
10. Brewster et al., *Experimentally derived guidelines for the creation of earcons*
   (HCI'95) + *The Sonification Handbook* ch.14 — structured-set / rule-based earcons,
   discrimination hierarchy.
11. Dingler et al., ICAD 2008 (earcon vs spearcon/speech learning cost); Frontiers in
   Psychology 13:780657 (2022) — auditory-alert working-memory competition.
12. Daniel Cook, *Value Chains* (lostgarden, 2021); Game Maker's Toolkit, *How Video
   Game Economies Are Designed* — resource caps as opportunity cost. *(Designer
   writing, Tier-3; illustrative.)*
13. Dustloop, *Resources in Fighting Games*; In Third Person, *Meter Management* —
   opportunity-cost spend, static-vs-dynamic resources. *(Community-tier, Tier-4;
   illustrative, one sub-claim split 2-1.)*
14. Interaction Design Foundation, *Preattentive Visual Properties* (relaying
   Treisman/Ware/Healey); Game Developer, *The Secrets of Brutality: God of War's
   Combat Design* (character-state tinting). *(Secondary; the <500 ms figure is a
   conservative upper bound.)*
15. Blizzard Watch (2025-07-31) + Wowhead (Midnight Phase-3 dev notes) — CDM's
   four-state colour/luminance pandemic encoding. *(Journalism-tier; patch-current.)*
16. Blizzard Watch (2025-07-31); Wowhead (Single-Button Assistant "overwhelmingly
   positive" feedback, 2025) — the CDM "dead on arrival" ordering critique.
   *(Journalism-tier; patch-current.)*
17. Hekili — GitHub repo + `Getting-Started` wiki (queue model, live re-evaluation,
   context displays, salience layers). *(Primary — addon source/docs.)*
18. MaxDps — GitHub (`kaminaris/MaxDps`) + CurseForge (single-highlight-on-real-bar
   model, white/green colour code). *(Primary — addon source/docs.)*
19. Blizzard news, *Legacy of Arathor — Get an Assist* (Assisted Highlight / SBA
   intent, 0.3 s GCD penalty, limitations); caniplaythat.com + mmorpg.com (Ion
   Hazzikostas framing, Hekili-inspired lineage — the lineage on a single blog,
   split 2-1 vote). *(Tier-1 Blizzard news + Tier-3/4 corroboration.)*

---

## 0.5.4 Moment / mode → signal map

One row per §0.5.2 moment **plus the mode indicator itself**. Each row assigns the
**readable trigger** → the **attention mechanism** (visual and/or audio, drawn from
§0.5.3) → the **three-way classification**:

- **Own** (read & branch): shards, proc *presence* (`IsShown`), player-cast napkin
  timers → we drive arbitrary salience.
- **Borrow** (display only): cooldown swipe, DoT/proc duration bars, native
  ready/pandemic alerts, stack-count text → we restyle, never read.
- **Can't** (flag honestly): secret timers, exact CD remaining, imp/core counts,
  in-pandemic boolean → §0.5.5.

| Moment / element | Readable trigger | Attention mechanism (visual · audio) | Class | Capability (`notes.md` §1) |
| --- | --- | --- | --- | --- |
| **Mode indicator** | Shards + Tyrant napkin timer + proc presence (§0.5.1) | Ambient **state-colour + luminance** of the overlay chrome (GENERATE cool/dim · SPEND active · BURST hot/bright), + a redundant mode glyph/label; steady-state, **no motion**; element positions stay locked across phases `[V3][V6][V7][X1][M1][M2]` | **Own** | shards read+branch; `IsShown`; napkin timer |
| **#1 Shards at cap (5)** | `UnitPower == max` | Rail **luminance flip** + **one-shot anchored glitter (motion onset)**; **earcon**. Frame as an **"act or waste" warning**, not a reward — cap is an opportunity-cost loss if you sit on it `[V3][V4][V6][A1][X2][B1]` | **Own** | Soul Shards read+branch |
| **#2 Demonic Core proc** | buff item `IsShown()` | Demonbolt block **proc-glow / luminance-onset outline** (single feature; redundant with fixed slot + label); optional soft "ding" `[V2][V3][X1][A3]` | **Own** (+ native `OnAuraApplied` for audio) | buff `IsShown` |
| **#3 Tyrant ~ready** | Tyrant napkin timer → 0 | Burst-lane **luminance/size urgency ramp** as timer nears 0 (juice escalates with urgency; motion only at the final ~0) `[V3][J1][V4]` | **Own** (napkin — drift-flagged) | player-cast napkin timer |
| **#4 Burst "all up = go"** | summon CDs staged (own casts) + borrowed swipes | Lane **common-fate brighten** (shared region, synchronized luminance) `[V3][V7]` | **Own** (best-guess) **+ Borrow** (swipe = ground truth) | napkin timers (own) · secure swipe (borrow) |
| **#5 Shards ≥3, Tyrant far** | `UnitPower ≥ 3` and not bursting | Hand of Gul'dan block reads **actionable** (bright vs dim luminance); **no sound** (don't nag a routine action) `[V3][A3]` | **Own** | Soul Shards read+branch |
| **#6 Wild Imps present** | Wild Imp buff-icon `IsShown()` | Implosion block surfaces (luminance); enlarge Blizzard's **stack-count text** + static "/6" — count itself unread `[V3][V6]` | **Own** (presence) **+ Borrow** (stack text); ≥6 gate **Can't** | `IsShown` (presence); `Applications` secret |
| **#7 Dominion of Argus up** | buff bar `IsShown()` | Hand of Gul'dan block flags **empowered** (luminance-onset); borrowed Dominion bar restyled `[V3][X1]` | **Own** (presence) **+ Borrow** (bar) | `IsShown`; secure BuffBar |
| **#8 Cooldown ready** | hooked ready-alert **edge** (observed, not read) | Own "ready settle" **luminance-onset** glow off the edge; **native ready earcon** (distinct timbre) `[V3][A2][A3]` | **Borrow** (native alert) **+ Own** (glow off observed edge) | `TriggerAvailableAlert`/`OnCooldownDone` hook |
| **#9 Board cleared / all-quiet** | no procs shown + shards low | Everything **recedes/dims** (no steady-state animation) — the declutter state `[V4][V6]` | **Own** (composed from readable absence) | shards + `IsShown` |
| **#10 Demonic Art armed** | Diabolic Ritual/Art buff `IsShown()` | **Proc-glow the transformed button** (HoG→Ruination, SB→Infernal Bolt) — luminance-onset, single feature, redundant with the fixed slot + label `[V2][V3][X1]` | **Own** | buff `IsShown` (tracked `428514`) |

Every **Own** row above cites a capability confirmed in `notes.md` §1 (shards
read+branch, `IsShown` presence, player-cast napkin timers, or the observed
hook-edge). The specific *mechanism* choices (why luminance/onset for a peripheral
"ready", why an earcon ceiling, why ambient colour for mode) are grounded in
§0.5.3.

---

## 0.5.5 Blind spots — what we cannot assist (honest list)

The design is honest about its wall. These are the moments/quantities the
Secret-Values rules (`notes.md` §1) put out of reach; we either borrow Blizzard's
own display or flag the gap rather than fake a signal.

| Blind spot | Why it's secret | Best we can do |
| --- | --- | --- |
| **Exact cooldown time-remaining** | `GetSpellCooldown().duration` is `<secret>` | Borrow the secure radial swipe; drive urgency off a **napkin timer** for fixed-CD abilities only |
| **Napkin-timer accuracy** | The *modified* CD (haste-scaled recharge, CDR/reset procs) is secret | Accurate for **fixed-CD** abilities (Tyrant 60 s, Grimoire: Imp Lord ~2 min); **drifts** otherwise — treat as best-guess, never as truth (§0.5.1 BURST caveat) |
| **Wild Imp count (≥6 Implosion gate)** | `Applications` count is displayed but secret | Surface imp *presence*; enlarge Blizzard's own stack text + static "/6"; **cannot compute "≥6"** ourselves |
| **Demonic Core count (near-cap-4 overcap gate)** | `Applications` count is displayed but secret | Surface Core *presence* only (moment #2); **cannot signal "near cap 4"** — the second overflow bucket's waste-gate is invisible to us. (Power Siphon's "≤1 stacks" trigger is doubly moot: the modern build skips it, `diabolist-sequences.md`.) |
| **In-pandemic / refresh-window boolean** | `IsInPandemicTime` is secret-derived | Observe the `PandemicIcon` shown-state **edge** via hook and redraw our own indicator; **cannot poll/branch** the boolean |
| **True "all cooldowns up" for the burst window** | requires reading 3 cooldown-ready states | Approximate via napkin timers (own casts) + the borrowed swipes; flagged best-guess (moment #4) |

---

## 0.5.6 → M3–M6 backlog seed

Each §0.5-derived signal becomes a widget, slotted into the existing milestone
frame (`milestones.md` §6). No signal is orphaned; every milestone has ≥1 signal.

- **M3 — First real skin.**
  - **Shard rail** (moment #1): segmented fill, cap colour-flip + one-shot glitter
    (cap earcon lands in M6). *Own.*
  - **Demonic Core proc-glow on Demonbolt** (moment #2). *Own (`IsShown`).*
  - **Diabolic Ritual / Demonic Art proc-glow on the transformed button** (moment
    #10 — HoG→Ruination, SB→Infernal Bolt). *Own (`IsShown`).* Predictive
    ritual-stage tracking is an M4/M5 elaboration.
  - **Group colour map + generator-vs-consumer batch tint** (§3 / spec.md) — the
    build→spend axis reads preattentively; supports moments #2, #5.
  - **"Ready vs on-cooldown" luminance re-encoding** (moment #8, `notes.md` §9 open
    design decision now that we own the icon colour on every repaint path). This same
    luminance-state encoding gives us the **declutter / empty-board recede** (moment
    #9): not-actionable = dim.
  - **Mode indicator (candidate widget)** — ambient state-colour of the chrome for
    GENERATE/SPEND/BURST (§0.5.1). Could land here (chrome tint) or ride into M4
    with the burst lane; called out as its own candidate.
- **M4 — Burst-window overlay.**
  - **Burst-lane grouping** Tyrant · Call Dreadstalkers · the tracked Grimoire
    summon, shared lane tint + **common-fate brighten** (moment #4). *(Naming: the
    live CDM profile tracks **Grimoire: Fel Ravager** (`notes.md` §2); top parses
    cast **Grimoire: Imp Lord** — bind to whatever's tracked, §M2. **Summon
    Doomguard is neither tracked nor cast** — dropped, per `diabolist-sequences.md`.)*
  - **Tyrant napkin-math timer** urgency ramp (moment #3). *Own (napkin,
    drift-flagged).*
  - **Predictive Diabolic Ritual tracker** (moment #10, richer form): surface which
    Demonic Art arms next from the active ritual stage. *Own (`IsShown` per stage) —*
    *needs the per-stage ritual/art auras in the tracked set (only the `428514`
    container is tracked today, `notes.md` §2); adding them is a layer-① curated
    override (M7).*
- **M5 — Borrowed DoT/proc bars.**
  - Restyle the secure BuffBar viewer for **Demonic Core** and **Dominion of
    Argus** (moments #2, #7). *Borrow.*
  - Enlarge Blizzard's **Wild Imp stack text** + static "/6" (moment #6). *Borrow.*
- **M6 — Audio.**
  - **Shard-cap earcon** (moment #1, ours) + **proc-gained ding** (moment #2, native
    `OnAuraApplied` or `IsShown` edge); **native ready / pandemic alerts** (moment
    #8). Earcon count stays under the §0.5.3 distinctness ceiling; per-event toggles
    + global mute.

*(Second-spec generalization + profile-enforcement UX stay in M7, unchanged.)*

---

## 0.5.7 Open research (residual gaps)

Three research passes are done (§0.5.3): Strand A (perceptual/auditory/accessibility),
Strand B (resource-loop [B1][B2], mode communication [M1][M2], the CDM prior-art/
failure-mode case [M3], earcon ceiling [A2]), and the rotation-helper landscape
([R1][R2][R3] — Hekili/MaxDps/Blizzard models). What the verify passes **did not**
substantiate — the genuine remaining gaps:

1. **WeakAuras' own salience conventions.** The rotation-helper pass covered Hekili,
   MaxDps, and Blizzard's Assisted Highlight ([R1]) but **WeakAuras did not verify** —
   what popular shared "what to press" auras actually use (glow vs icon pulse/zoom vs
   TMW-style bar, sound, dynamic groups; single vs multi-suggestion). Worth a
   dedicated pass on the WeakAuras wiki/GitHub + setup guides. (Less critical, since
   [R3] positions us as a *state* helper, not a WA-style next-ability aura.)
2. **The "tunnel-vision / whack-a-glow" over-reliance failure mode — CLOSED with a
   design note, not researched further.** It stayed unverified (the pass ran out of
   budget before reaching it) and is inherently soft-sourced (community/opinion,
   tier 3–4), so a dedicated pass wasn't worth it. It doesn't need one: the design
   **already sidesteps the pattern** — [R3] makes us a *state dashboard*, not a
   single blinking "press this" to chase, and the mitigation (peripheral, small,
   low-motion, no foveal stare) falls straight out of the Tier-1 perceptual
   principles [V4]/[V5]. So we treat "glow-chasing degrades awareness" as a
   **prudent design assumption we build against**, not an asserted fact — and the
   constraint that follows from it is already cited via [V4]/[V5]/[R3].
3. **WoW-class-resource-specific psychology.** [B1][B2] transfer resource-loop theory
   from economy/fighting-game writing; no WoW-specific primary source confirmed the
   Soul-Shard / Demonic-Core / Tyrant-window payoff behaves the same. Softer sourcing
   (community-tier) — see §0.5.3 sources 12–13.

---

## Provenance

- **Rotation derivation:** `knowledge/classes/warlock/demonology/rotation.md`
  (Diabolist, 12.0.7; distilled from the Tier-1 simc MID1 APL + maxroll/Method/
  Kalamazi) — the ST/AoE priority, the Tyrant-window rule, the shard build/spend
  loop. **Enriched from `diabolist-sequences.md`** (top-6 WCL Mythic parses +
  directly-observed aura/pet streams; the `maxroll-mplus.md` / `maxroll-raid.md`
  verbatim captures behind it) — the two-bucket model, the Diabolic Ritual /
  Demonic Art cycle, the Dreadstalkers→Tyrant entry block, and the corrections
  (Power Siphon skipped, Grimoire: Imp Lord not Doomguard). Cross-checked against
  `notes.md` §2 (the tracked set + salience drivers).
- **Capability wall:** `notes.md` §1 (Secret-Values capability map) — every
  own/borrow/can't verdict traces to it.
- **Attention-mechanism research (§0.5.3):** three M0.5 deep-research fan-outs
  (multi-source web search → fetch → 3-vote adversarial verify → cited synthesis).
  **Pass 1 — Strand A** (24 Tier-1 claims: Healey & Enns; UC Berkeley EECS-2006-113;
  Player Research; Kao/Hicks juiciness study; Edworthy/Hellier auditory-urgency; Nees
  & Liebman meta-analysis; Microsoft XAG 103 / WCAG). **Pass 2 — Strand B** (8 claims:
  Cook/lostgarden + GMTK resource-economy; fighting-game meter writing; IxDF/God-of-War
  mode-tinting; Blizzard Watch/Wowhead CDM prior-art + failure-mode; Brewster/Dingler
  earcon science). **Pass 3 — rotation-helper landscape** (9 claims: Hekili & MaxDps
  repos/docs; Blizzard news on Assisted Highlight/SBA). Full source list at the foot
  of §0.5.3; residual gaps → §0.5.7. Extends — does not discard — the two glanceable-UI
  agent reports already synthesized into `notes.md` §1 / `spec.md` §3 (`notes.md` §8).
- **Visual feasibility sanity check:** the M1 CRT prototype
  (`../prototype/overlay-styles.html`) already demonstrates the proposed cues in the
  chosen treatment — segmented shard rail + cap glitter, proc-icon blink/glow, dim
  vs bright luminance for state — so the signals here are buildable in the v1
  aesthetic.

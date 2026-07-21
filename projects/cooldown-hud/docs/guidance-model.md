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
> `milestones.md` · superseded work → `notes-archive.md`.
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
| 8 | **A tracked cooldown becomes ready** — observed off the hooked ready-alert edge (**`TriggerAlertEvent`**; `OnCooldownDone` is unhookable — `notes.md` §1), *not* a secret read | Use the cooldown per the fixed priority order. | **P1** | any |
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
| **#8 Cooldown ready** | hooked ready-alert **edge** (observed, not read) | Own "ready settle" **luminance-onset** glow off the edge; **native ready earcon** (distinct timbre) `[V3][A2][A3]` | **Borrow** (native alert) **+ Own** (glow off observed edge) | `TriggerAlertEvent` hook |
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
| **Demonic Art on the Shadow Bolt half** (SB → Infernal Bolt) | *not* secret — **Shadow Bolt simply isn't in the tracked set** (`notes.md` §2), so there is no icon to glow | Glow the **HoG → Ruination half only** (#3). The SB half is a v1 blind spot we flag rather than fake; it re-opens only with an M7 curated layout override that adds SB. *(Found in M3b, 2026-07-20 — the only blind spot here caused by the layout rather than by Secret Values.)* |
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

## 0.5.8 The committed v1 indicator set (M2.5)

This is the **settled v1 scope** — the list M3+ builds against 1:1, distilled from
the §0.5.4 signal map and the §0.5.6 backlog. The *what*, not the *how*: no Lua, no
pixel layout, no colour hex (those live in `spec.md` §3 and the M3+ code). Each
indicator carries a **milestone**, an **own/borrow** class, and a **verdict**.

A design session (2026-07-19) sharpened this past the raw §0.5.6 list in two ways:
it added a **cut principle** (below) that sorts the list into load-bearing vs.
droppable, and it surfaced three **cross-cutting dimensions** — a pre-pull
affordance, an anticipation layer, and an escalating burst telegraph — that aren't
single widgets but *behaviours several indicators inherit*. Those are §0.5.8.2;
the flat indicator table is §0.5.8.3; the rough per-signal logic is §0.5.8.4.

### 0.5.8.1 Cut principle & verdict legend

> **v1's hard-committed core = every signal that is (a) *Own* — we drive it, which
> is our whole differentiated value — *and* (b) tied to a *P0/P1* moment, plus the
> borrowed ground-truth those Own signals lean on. Everything else is Stretch or
> Defer.**

The principle sorts almost the whole list on its own; it also auto-answers three
of the four M2.5 open sub-questions (borrowed bars → Stretch, predictive ritual
tracker → Defer, mode-indicator placement → the split in §0.5.8.5).

- **Core** — load-bearing; M3/M4 must ship it. The Own P0/P1 signals + their
  ground-truth borrows.
- **Stretch** — v1 if the core lands clean; **cut without shame** under time
  pressure. Pure-Borrow restyles and the audio layer.
- **Defer** — post-v1 (M7) or dropped: needs a curated layer-① layout override,
  or its readable trigger can't answer the question it exists for.

**Verify contingency — CLOSED 2026-07-20; the `Core*` asterisks are retired.**
The anticipation layer and every napkin countdown depend on reading the **in-flight
/ just-cast spellID in restricted combat**. `UNIT_SPELLCAST_SUCCEEDED` was confirmed
in a delve and `UNIT_SPELLCAST_START` at an open-world dummy (v0.5.3 logs both
per-phase); a raid-boss confirmation was never obtained and **we are no longer
waiting on one**. The design now **assumes both events carry a readable spellID in
all combat contexts**, so rows #7/#8/#10/#11/#12 below are plain **Core**, not
`Core*`. "Cast in flight" is derived from our own START → SUCCEEDED/STOP/INTERRUPTED
bookkeeping rather than `UnitCastingInfo`, so no second untested API is in the path.
The reactive/borrowed fallback (rail fills the instant `UNIT_POWER_UPDATE` lands;
native ready-alert carries "up") is demoted from a planned degradation path to a
contingency we'd build only if the assumption is falsified in play.
`v1 = the M3→M6 arc for Demo` (M7 = second spec + polish = post-v1).

### 0.5.8.2 Three cross-cutting dimensions (new this pass)

**(a) The pre-pull affordance — be richest when we're allowed to be.** Out of
combat the Secret-Values wall isn't up: cooldowns, buffs, everything reads freely.
And the Demo opener is a **mostly-fixed script with a few branches** — the invariant
is **Tyrant at t≈3–5 s off a pre-stacked board** (all six parses,
`diabolist-sequences.md` SEQUENCE 1); the *first-3-GCD ordering varies*
(`DS→TYR` / `DS·GIL·SB→TYR` / `DB·GIL·DS→TYR`), Grimoire: Imp Lord is
conditional ("when off CD"), and the Implosion step is fight-dependent. So the
calmest moment gets the **most** information, and it's the one place we can
legitimately do the queued "press this next" that §0.5.3 [R3] refuses in combat:

- A distinct calm **PREP** chrome tint (a fourth resting state, not GENERATE).
- **Which opener it ghosts matters.** Textbook opener **1b** builds to 5 shards
  pre-pull → the **fill-to marker** ("bank to N before you pull") applies. The
  parse-observed opener **1a** instead enters combat *shard-poor* off a **pre-pull
  demon setup** (pre-pull HoG casts don't appear in the log; the board, not the
  shard bar, is what's "full"). The PREP widget should know which one it's showing —
  the fill-to marker is wrong for 1a.
- A short **opener queue** ghosts the scripted sequence; it drains as you pull.
  Advance it by **matching the ability pressed**, not by strict slot position, so
  the branch orderings above don't desync it (counting our own casts survives the
  wall clamping down — no secret read needed).
- **Opener → sustain handoff:** the queue dissolves when the **first Tyrant window
  closes** (detected off our own Tyrant cast + its ~15 s napkin window). Clean
  boundary, no secret read.

**(b) The anticipation layer — spend cast-time telling me what's coming.** The
model in §0.5.4 is *reactive* (current shards, current procs). This adds an
*anticipatory* layer: while a builder cast is in flight we already know its
**deterministic** result, so we show it early —

- Shadow Bolt in flight → a **ghost segment at the head of the shard rail** ("+1
  incoming"); **Infernal Bolt** in flight → ghost **+3**. **Demonbolt returns +2
  whole shards** (`rotation.md` #11 gates it at `<4` precisely because +2 overcaps
  from 4) — but Core-proc'd Demonbolt is *instant*, so it rarely has in-flight dead
  air to ghost; its +2 still feeds `projected` on any hardcast pre-flip. The shard
  appears *during the cast's dead air*, before it lands.
- If that ghost fill would cross the spend threshold (≥3), the **chrome pre-warms
  toward SPEND** — a predictive mode flip — so by the time the cast completes you're
  already reading "now dump," not reacting a beat late.

**(c) Escalating burst telegraph + short-CD approach pings — one napkin engine,
three consumers.** The napkin-timer machinery (`GetSpellBaseCooldown` counted down
off our own cast, fixed-base only — §0.5.5) drives three "something's coming" cues
at three fidelities, all drift-flagged and all backstopped by the native
ready-alert as ground truth:

| Consumer | Base CD | Cue | Why |
| --- | --- | --- | --- |
| **Summon Demonic Tyrant** — *awareness phase* | 60 s (fixed — our *most reliable* timer) | **WARM-UP tint, ~15 s out.** Low-salience "Tyrant approaching" glow on the burst lane — *awareness only, non-instructional.* Does **not** stop the P0 overcap cue; the player keeps dumping normally. | The user wants an early "it's coming" heads-up ("err early"). Satisfied here — **without** freezing shards. |
| **Summon Demonic Tyrant** — *hold phase* | — | **HOLD/BANK + stage, ~5 s out (≤2 GCDs).** *Now* rail shifts to "hold — save for Tyrant" and the lane brightens to a motion onset at ~0, handing into the common-fate "all up = go." | The real banking window is short: the APL holds Hand of Gul'dan only when Tyrant is **≤5 s** away (`rotation.md` #9), and the pre-Tyrant rebuild is one `SB SB SB` run (~5–7 s), not 15 s. A 15 s freeze **force-overcaps** — Cores proc ~every 3.6 s and Demonbolt refunds +2, so the rail hits cap within ~2 GCDs. HOLD ≈ SEQUENCE 2: Dreadstalkers → [Imp Lord] → Tyrant → HoG HoG. |
| **Call Dreadstalkers** ("hounds") | ~20 s | **Approach ping ~1 GCD out — *suppressed/restyled when Tyrant is imminent*.** When Tyrant is close, the ping becomes a *"stage for Tyrant"* treatment instead of a generic "use it now." | One Dreadstalkers per Tyrant cycle must be **held** so the dogs are fresh *inside* the window (`rotation.md` #5; a DS cast at Tyrant−15 s expires before Tyrant lands). We already own `tyrant_napkin`, so the suppression is free. |
| **Implosion** | 15 s | **AoE weave ping** — same subtle approach cue, only in AoE context. | Lets you pre-weave the cleave button instead of discovering it off cooldown. Two honest caveats: its *value* gate (≥6 imps) stays a **Can't** (§0.5.5) — the ping is "it's available," not "it's worth it"; and the `in_aoe` predicate itself needs a **capability check** (target count / recent multi-hit) — flagged verify-in-game. |

Imprecision is acceptable on the *awareness* cues (the user's call): they're
**attention nudges** ("something's coming off cooldown"), not truth. But the
*instructional* cues — the ~5 s HOLD and the Dreadstalkers-during-hold — must be
**correct**, because they tell the player to stop doing the right thing: they're
tight (≤2 GCDs), Tyrant-gated, and never override the P0 overcap cue. Haste/CDR can
drift the ~15 s / ~20 s ones; the fixed-60 s Tyrant clock is the sturdy anchor.

### 0.5.8.3 The committed indicator table

| # | Indicator | Moment(s) | Tier | Class | Milestone | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Shard rail** — segmented fill, cap flip + one-shot glitter | #1 | P0 | Own | M3 | **Core** |
| 2 | **Demonic Core proc-glow** on Demonbolt | #2 | P0 | Own | M3 | **Core** |
| 3 | **Demonic Art proc-glow** on the transformed button (HoG→Ruination, SB→Infernal Bolt) | #10 | P1 | Own | M3 | **Core** |
| 4 | **Group colour map + generator-vs-consumer batch tint** (the skin itself) | #2,#5 | ambient | Own | M3 | **Core** |
| 5 | **Ready/dim luminance re-encoding + empty-board recede** | #8,#9 | P1/P3 | Own+Borrow | M3 | **Core** |
| 6 | **Mode chrome tint — GENERATE↔SPEND** (pure shard threshold) | mode spine | ambient | Own | M3 | **Core** |
| 7 | **Anticipation: ghost shard-fill + predictive SPEND pre-flip** (in-flight builder) | new (b) | P1 | Own | M3 | **Core** |
| 8 | **Pre-pull affordance** — PREP chrome, opener queue, fill-to marker | new (a) | — | Own | M3 | **Core** |
| 9 | **Burst lane** (Tyrant · Dreadstalkers · Grimoire) + common-fate brighten | #4 | P1 | Own+Borrow | M4 | **Core** |
| 10 | **BURST mode activation** (folds into the lane; the spine's hot state) | mode spine | ambient | Own | M4 | **Core** |
| 11 | **Tyrant HOLD/BANK telegraph + crescendo** (60 s napkin) | #3 | P1 | Own | M4 | **Core** |
| 12 | **Short-CD approach pings** — Dreadstalkers ~20 s, Implosion ~15 s (napkin) | new (c) | P2 | Own | M4 | **Core** |
| 13 | **Borrowed Demonic Core bar** (duration restyle) | #2 | — | Borrow | M5 | **Stretch** |
| 14 | **Borrowed Dominion of Argus bar** (empowered-HoG restyle) | #7 | P2 | Borrow | M5 | **Stretch** |
| 15 | **Shard-cap earcon** (the one must-have sound) | #1 | P0 | Own | M6 | **Stretch** |
| 16 | **Proc-gained ding + native ready/pandemic alerts** | #2,#8 | P1/P2 | Own+Borrow | M6 | **Stretch** |
| 17 | **Wild Imp stack text + "/6"** (the one AoE readout) | #6 | P2 | Borrow | M5 | **Core** |
| 18 | **Predictive Diabolic Ritual tracker** (which Art arms next) | #10 (rich) | P1 | Own | M7 | **Defer** |

**Cut rationale for the non-Core rows.** #13/#14 are pure Borrow — the Own
proc-glows (#2, #3) already carry the *decisions*; the bars only add duration
prettiness, so they're droppable. #15/#16 are the audio milestone, honestly
optional for a first ship (only the shard-cap earcon pairs with our P0 anchor).
#18 needs the per-stage ritual auras added to the tracked set = a curated
**layer-① override** = M7 territory (`notes.md` §2 tracks only the `428514`
container today).

**Why #17 is Core despite being a Borrow (decision 2026-07-19).** Demo's whole AoE
loop hinges on one decision — *≥6 Wild Imps → Implosion* — and Implosion is the
**4th-most-pressed rotational button** (161 pooled casts; 25 for Inphected). We
can't *own* it (imp count is a secret **Can't**), but enlarging Blizzard's own
stack text + a static "/6" is a cheap Borrow that surfaces the count, and it's the
**only** v1 assist for the single biggest AoE call — so it's promoted from Defer to
Core rather than left out. Paired with the #12 Implosion approach ping it makes v1
cover AoE, not just single-target. (Open: the `in_aoe` gate for *when* to surface
these is still a verify-in-game.)

### 0.5.8.4 Rough signal logic

Sketch-level, not code — the trigger → state → cue for each committed signal.
Shards read via `UnitPower` (0–5 whole; fragments 0–50 available). Proc *presence*
via `item:IsShown()`. Napkin timers = `GetSpellBaseCooldown` counted down off our
own `UNIT_SPELLCAST_SUCCEEDED`. "Cast in flight" is tracked from our own
`UNIT_SPELLCAST_START` → `SUCCEEDED`/`STOP`/`INTERRUPTED` bookkeeping (not
`UnitCastingInfo` — one assumed-readable path, not two; §0.5.8.1).

```
WARMUP_LEAD = ~15s    # awareness only (non-instructional)
HOLD_LEAD   = ~5s     # ~2 GCDs — the REAL banking window (rotation.md #9)

# ---- resource + mode spine ----
shards        := UnitPower(SOUL_SHARDS)            # 0..5, readable+branchable
ghost_shards  := deterministic_yield(cast_in_flight)  # SB:+1, InfernalBolt:+3, DB:+2  (from our START/STOP tracking)
projected     := shards + ghost_shards

mode := PREP     if not InCombat                                    # pre-pull affordance
      | BURST    if tyrant_napkin <= HOLD_LEAD and board_staged     # spine hot state (M4) — ~5s, not 15s
      | SPEND    if projected >= 3                                  # predictive pre-flip uses projected, not shards
      | GENERATE otherwise
chrome_tint := colour_of(mode); luminance := level_of(mode)   # ambient, no motion, positions locked

# ---- #1 shard rail ----
rail.fill        = shards / 5
rail.ghost_head  = ghost_shards                    # anticipation: incoming segment during a cast
if shards == 5:  rail.flip_luminance(); rail.glitter_once()   # frame as "act or waste"; P0 — always wins
if mode == BURST and shards < 5: rail.hold_treatment()        # "save for Tyrant" — ONLY at <=5s, never fights the cap cue

# ---- #2 / #3 proc-glows ----
if DemonicCore.IsShown():
    if shards < 4: Demonbolt.block.glow()          # spend cores; count is secret
    else:          Demonbolt.block.soften()        # DB +2 overcaps from >=4; cap-flip outranks the Core glow
if DemonicArt.IsShown():         transformed_button.glow()     # HoG->Ruination or SB->InfernalBolt (buff 428514)

# ---- #4 identity + #5 readiness ----
block.hue        = group_colour(ability)           # identity: hue=group, never per-ability
block.luminance  = BRIGHT if ready else DIM        # readiness pop, independent of hue
batch_tint(builders -> cool/dim, spenders -> warm/bright)      # generate->spend axis reads preattentively
if board_all_quiet(): everything.recede()          # empty board = nothing to do

# ---- #8 pre-pull ----
if mode == PREP:
    opener_queue.show(SCRIPT[opener_variant])       # 1a (demons pre-stacked) vs 1b (bank-to-5)
    if opener_variant == "1b": rail.fill_to_marker(OPENER_BANK_TARGET)   # NOT for 1a (enters shard-poor)
    on our_cast(spell): opener_queue.advance_matching(spell)   # match ability, not slot — tolerates branches
    on first_tyrant_window_close: opener_queue.dissolve()      # handoff to sustain

# ---- #9/#11/#12 napkin engine (one engine, three consumers) ----
on our_cast(spell): napkin[spell] = GetSpellBaseCooldown(spell)   # decremented on a ticker
tyrant_napkin  := napkin[TYRANT]                    # 60s fixed = reliable
tyrant_imminent := tyrant_napkin <= HOLD_LEAD + 1_GCD
if tyrant_napkin <= WARMUP_LEAD: lane.warmup_tint()             # awareness only (does NOT stop dumping)
if tyrant_napkin <= HOLD_LEAD:   burst_telegraph.escalate(tyrant_napkin)   # crescendo, motion only at ~0
if napkin[DREADSTALKERS] <= 1_GCD:
    if tyrant_imminent: Dreadstalkers.block.stage_for_tyrant()  # HOLD one DS for the window (rotation.md #5)
    else:               Dreadstalkers.block.approach_ping()
if in_aoe? and napkin[IMPLOSION] <= 1_GCD: Implosion.block.approach_ping()  # in_aoe = capability to verify
# ground truth always wins:
on native_ready_alert(spell): block.settle_ready()  # borrowed edge overrides the napkin guess

# ---- #9 burst lane common-fate ----
if (TYRANT and DREADSTALKERS) look_ready (napkin) or borrowed_swipe_ready:
    lane.brighten_together()                        # "all up = go" — Tyrant+DS only
    if GRIMOIRE look_ready: lane.grimoire.brighten()  # 2min CD, absent ~half the windows — brighten-if-up, never a gate
```

Guard rails baked in: every napkin cue **rounds down / fires early** and yields to
the native ready-alert; every colour-carried state has a redundant non-colour
signifier ([X1]); motion is reserved for the single most-urgent instant ([V4]).

### 0.5.8.5 Resolved decisions & remaining contingencies

- **A — Mode indicator (open-Q#4): RESOLVED as a split.** GENERATE↔SPEND is a pure
  shard threshold (no drift, no napkin) → **M3 chrome tint (Core)**. BURST needs the
  Tyrant napkin + staged board → **folds into M4 (Core)**. Plus a **predictive
  pre-flip** (uses `projected`, not `shards`) from the anticipation layer.
- **B — Borrowed Core/Dominion bars (open-Q#3): Stretch (M5).** The Own proc-glows
  already carry the decisions; the bars are prettiness, cut-if-short.
- **C — Wild Imp stack text: promoted to Core (M5).** Reversed from Defer
  (2026-07-19): it's the only v1 assist for the ≥6-imp Implosion call — the spec's
  central AoE decision — a cheap Borrow worth shipping even though the count itself
  stays a Can't. See the #17 rationale above.
- **D — Audio: Stretch.** Only the shard-cap earcon is near-essential; rest is
  native/nice-to-have.
- **E — Verify contingency: CLOSED (2026-07-20).** Rows #7, #8, #10, #11, #12 were
  `Core*` pending the in-combat cast-ID read. That verify is now **closed as a
  design assumption** — START and SUCCEEDED are taken to carry a readable spellID in
  all combat contexts (delve + dummy confirmed; raid never tested and no longer
  waited on). The asterisks are **retired**; all five are plain **Core**. See
  §0.5.8.1 and `milestones.md` §7. *If it is ever falsified in play, the fallback
  described there is the recovery — the rows do not become blockers.*
- **F — "v1" = the M3→M6 arc for Demo.** M7 (second spec + enforcement UX +
  cyberpunk polish) is explicitly post-v1.

### 0.5.8.6 Fidelity-review corrections (2026-07-19)

This section was checked against real play before committing — a Fable-model
expert review cross-referencing an independent #1 Demo parse (Inphected, WCL report
`CFdapgHjGx2JDXL4`, Rotmire/Sporefall Mythic) plus `diabolist-sequences.md` and
`rotation.md`. The reviewer confirmed the **skeleton is parse-true** (shard rail
anchor — HoG most-cast at ~1/3.7 s; Core glow #2; Art glow #3; Tyrant-centric
telegraph; Power Siphon correctly excluded; Doomguard correctly dropped; all CD
numbers verified against measured cast spacing). Three **blocking errors** were
found and fixed above:

1. **HOLD/BANK lead was 3× too long** (15 s → **~5 s / ≤2 GCDs**). The APL holds
   HoG only at Tyrant ≤5 s (`rotation.md` #9); a 15 s freeze force-overcaps (Cores
   proc ~every 3.6 s, Demonbolt refunds +2). The ~15 s cue survives as a
   *non-instructional awareness* warm-up only — §0.5.8.2(c).
2. **Burst go-gate wrongly required Grimoire: Imp Lord** (2-min CD → absent ~half
   the windows; 21 GIL vs 48 Tyrant). Gate is now **Tyrant + Dreadstalkers**, GIL
   brighten-if-up.
3. **Demonbolt shard yield** corrected to **+2 whole shards** (not "a fragment or
   two"); the ghost/pre-flip math now balances the Inphected shard economy.

Plus fidelity gaps: the **Dreadstalkers ping now suppresses when Tyrant is imminent**
(one DS/cycle is held for the window), the **Core glow softens at ≥4 shards**, the
**opener is "mostly-fixed with branches"** (queue advances by ability-match; 1a vs
1b differ on the shard entry condition), and the **Implosion/AoE under-service** it
flagged was resolved by **promoting #17 (Wild Imp stack text) into v1 as Core**, so
the spec's central AoE decision has a readout. `in_aoe` is flagged as a capability
to verify-in-game.

---

## 0.5.8.7 Amendment — the dot score, and what it displaces (2026-07-20)

> **Status: this block amends §0.5.8.3–§0.5.8.5.** Where it disagrees with them,
> this wins; the rows themselves are left in place so the change is legible rather
> than silently rewritten (same pattern as §0.5.8.6). Driven by the M3b in-game
> passes (CDMProbe v0.7.0–v0.9.1), a Fable fidelity review, and the design session
> that followed.
>
> **Implementation status (2026-07-20): SHIPPED in CDMProbe v0.10.0 as milestone
> M3c-a — in-game review pending.** §1 (the dot + four-level ladder + anticipation
> as a treatment on NEVER), §2 (#5 re-scoped to CD-bearing buttons), §3 (text
> promoted into the default view), and the signal-bucket rewrite are all live in
> code: `HudScore.lua`, `HudNapkin.lua`, `HudRow.lua`, and the reworked
> `SpecDemonology.lua` / `HudChrome.lua`. §5's scrolling terminal view is **not**
> shipped and stays deferred. What this block does **not** yet carry is what the
> build *learned* — that lands after the pass. See `milestones.md` Status + §6 for
> the outstanding checks, of which the load-bearing ones are **strictness** (1–2
> lit dots, not 4–5) and **napkin readability inside a raid**.

### (0) The governing principle — inform, don't instruct

> *"I'm not looking to check out completely. If imps and dreadstalkers are both
> flagged as available, then I'm ok having to decide which I will hit."*
> *"There will still be decision making, but it will be focused decision making.
> Pick between 2-3 abilities instead of 5."*

**The HUD narrows the field; the player chooses within it.** This is now the
top-level test every indicator must pass, and it resolves several open tensions:

- It **retires the priority-arbitration problem**. §0.5.5 says Wild Imp count is
  secret, so "≥6 imps → Implosion over Hand of Gul'dan" was never computable. It
  no longer needs to be — surfacing both as live candidates *is* the deliverable.
- It **promotes the borrowed readouts**. If the HUD won't rank, the borrowed
  counts become the player's arbitration data, not decoration. §0.5.8.3 **#17
  (Wild Imp stack + "/6") moves from M5 to M3** and is no longer "Core despite
  being a Borrow" — it is Core *because* it is the Borrow that carries the AoE call.
- It puts the **instructional rows on notice**: #8 (opener queue), #11 (HOLD/BANK),
  #12 ("stage for Tyrant"). None are dropped, but each must be re-framed as
  *information* — "Tyrant in ~5s" rather than "stop pressing things". A cue that
  tells the player what to do is only acceptable where it is also *correct*
  (§0.5.8.2(c)); one that merely reports a readable fact is always acceptable.

### (1) The dot score — a new indicator, and the primary "what next" signal

**Why a dot and not another channel.** The review established there is **no free
visual channel**: hue = group, saturation = resource axis, luminance = readiness,
alpha = recede — and [V2] forbids conjunction encodings. A standalone dot beside
the icon sidesteps this entirely: it is a **new object**, not a new channel on a
crowded one. It can also carry its own **confidence**, which a border cannot.

**The level ladder** (the dot's state — an *actionability* scale):

| Level | Meaning |
| --- | --- |
| **NEVER** | on cooldown, or the resource gate is unmet — not pressable |
| **AVAILABLE** | pressable, but unlikely to be the top priority |
| **ROTATION** | what the addon can see suggests this may be next |
| **LATE** | this became actionable ≥3 s ago and still hasn't been cast |

**All four levels are PRECISE — none of them require napkin math.** This is the
load-bearing property and it was not obvious:

- NEVER / AVAILABLE come from the observed ready edge (`TriggerAlertEvent`) and
  readable resource state (`UnitPower`, aura-presence edges, runtime power cost).
- **LATE is measured, not guessed.** For a cooldown, we hold the exact `Available`
  edge and time from it with `GetTime()`. For a resource-gated ability, shards are
  readable. "3 s late" is arithmetic on values we legitimately hold — it is *not*
  the drifting napkin estimate, and it does not inherit the napkin's caveats.

**Anticipation is NOT a fifth level — it is an orthogonal treatment.** "Napkin
says this is coming up soon" is about the *future*; the ladder is about *now*.
Ranking an unpressable ability as ROTATION would make the dot claim pressability
for something the player physically cannot cast — the fastest possible way to
lose trust in the whole HUD. Instead the dot **stays at NEVER and fills/brightens
as the napkin approaches ready**, which is exactly §0.5.8.2(b)'s anticipation
pattern and #11's "WARMUP_LEAD = awareness only, non-instructional". Consequence:
the player never has to filter it out, because it never claimed to be pressable.

**Confidence encoding.** Because the ladder is precise and anticipation is not,
the dot can be honest about the difference: solid = derived only from precise
inputs; hollow/dimmed = leaning on a drifting estimate. Drift becomes visible
rather than silent.

**One proposed input cannot be built.** "Almost capped on Demonic Core" is a
**Secret Value** (§0.5.5 — displayed, unreadable, "cannot signal near cap 4"),
the same wall as imp count: we get *presence*, never *quantity*. A score that
treated "has a Core" as "about to overcap" would be confidently wrong, which
§0.5.8.2(c) forbids. Five of the six proposed inputs survive; the sixth is
covered by the borrowed stack text instead.

### (2) Luminance/readiness (#5) is SHELVED, not fixed

The review's blocking error **B1**: §0.5.8.4 commits `block.luminance = BRIGHT if
ready else DIM` board-wide and `spec.md` §3 promises "bright = ready/actionable" —
but Hand of Gul'dan and Demonbolt have **no cooldown**, never fire a ready edge,
and sit at base luminance permanently. They are the **#1 and #2 most-pressed**
rotational buttons (729 / 541 pooled casts). So the top of the [V3] salience
hierarchy is mute on the buttons the rotation is actually about.

The proposed fix was cadence-routed luminance (gated buttons light at
`shards ≥ cost`). **Decision: shelved in favour of the dot**, which addresses the
same need — "what should I press" — without loading a fifth meaning onto an
already-contested channel.

**But the promise must stop being made.** §0.5.8.3 **#5 is re-scoped in place** to
"ready accent on **CD-bearing buttons only** (burst summons, Implosion, utility)
+ empty-board recede", and `spec.md` §3's unqualified "bright = ready/actionable"
is now **wrong as written** and must be qualified. Shelving the fix is not
permission to keep the overclaim. The M3b tri-state (`ready = nil` is a real
state, never guessed) stands and supersedes §0.5.8.4's binary pseudocode.

*(Reopening path: if the dot proves insufficient, cadence-routed luminance is the
designed answer and §7.1 D1 holds the reasoning.)*

### (3) Text is promoted into the default view — conservatively

§0.5.8 previously **excluded** text from the indicator contract. It is now **in**,
with limits, because always-on identity text makes the colour map self-teaching —
the direct answer to *"yellow, purple etc. don't really have any meaning in
isolation."* Hue-carries-group is ambient **identity**, not instruction; an
arbitrary encoding cannot be read until it has been learned, and a permanent
adjacent label is how it gets learned.

**The split, from §0.5.3's attention research:** reading is *serial and slow*, so

- **text carries identity and reference** — keybind, state words, the reason a dot
  is lit. Absorbed peripherally, over time.
- **preattentive channels carry urgency** — the dot, proc glows, the shard rail,
  the cap cue. These must land without a saccade.

**Conservatively** means: not the full ability name (the icon already says what the
ability is), compact state tokens, and the row reads **dot first, then the reason
for the dot** — so the score is auditable rather than an oracle. Layout: the two
icon columns bracket the character, so the left column's text runs **leftward**.

### (4) The spec table becomes the signal bucket (supersedes the `role` enum)

`SpecDemonology`'s single `role` enum is replaced by the per-ability **signal
bucket** the dot score consumes — `spends` / `generates` / `cadence` /
`burstAlign` / `goGate` / `kind`. Corrections carried from the review: drop
`burst` (redundant with `burstAlign`, and its tint value was already **identical**
to `spender` — it never encoded anything); add `filler` (Shadow Bolt classifies as
nothing else); Grimoire also takes `burstAlign`; **`goGate` is a separate bit**
because the go-gate is Tyrant + Dreadstalkers *only* and without it someone
re-derives the lane from `burstAlign` and re-ships §0.5.8.6 blocking error #2;
`generates` subsumes the existing `ghost` field; aura rows take `kind = "aura"`.

**Costs are not authored into the table.** They are talent-dependent — Demonic
Calling makes Dreadstalkers free, and the Tyrant/Grimoire costs move with the
build — so any hardcoded number is right for one loadout and silently wrong for
every other. Read at runtime via `C_Spell.GetSpellPowerCost` (shipped v0.9.1).

**Blocking error B2 is downgraded, not dismissed.** Demonbolt is `role="builder"`
in code while §0.5.1 calls it a bucket-2 **spender**, so the `HoG ↔ Demonbolt`
alternation — the most common pattern in the parse data (313 + 313 two-grams) —
currently renders at **opposite tint poles**. In a dot-led world the tint matters
less, but the contradiction is still live and the fix is one data edit.

### (5) Deferred, recorded so it isn't lost

A **scrolling terminal view** below the cooldown column — practical readout and
period-appropriate flavour at once, and the natural home for the log-shaped
information the per-icon rows can't hold (edges as they fire, casts, score
changes). Not scheduled. `BucketBinds`' `Console.lua` already solves the
scrollback, geometry persistence and monospace-font handling.

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

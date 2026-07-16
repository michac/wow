---
title: Demonology (Diabolist) — learnable cast sequences from top parses
patch: 12.0.7
fetched: 2026-07-13
reviewed: 2026-07-13
sources:
  - https://www.warcraftlogs.com/  # WCL API — 6 top Demonology parses, Rotmire (Sporefall) Mythic, zone 50 / encounter 3159, bracket 290
  - https://maxroll.gg/wow/class-guides/demonology-warlock-raid-guide  # upd. 2026-06-17 (12.0.7)
  - https://maxroll.gg/wow/class-guides/demonology-warlock-mythic-plus-guide  # upd. 2026-06-29 (12.0.7)
  - https://www.method.gg/guides/demonology-warlock/playstyle-and-rotation  # upd. 2026-06-29 (12.0.7) — page is JS-gated; extraction was partial/unreliable
confidence: medium-high
---

# Demonology (Diabolist) — turning the heuristic into sequences

> **Goal of this doc.** `rotation.md` gives a *priority list* ("HoG at 4–5
> shards, spend Cores, maximize HoG in the Tyrant window"). That's correct but
> vague. This file pulls the **actual cast streams of the current top-6
> Demonology parses**, mines them for repeatable patterns, and reports which
> parts of the rotation are **fixed learnable sequences** and which parts are
> **irreducibly reactive** (and why). Pairs with `rotation.md` + `builds.md`.

## TL;DR — the simplest model

If you read nothing else: the whole spec is **two buckets you keep from
overflowing, plus things on cooldowns.**

> **Don't overcap. Hand of Gul'dan dumps Soul Shards, Demonbolt dumps Demonic
> Cores, Shadow Bolt when you have neither — and press Summon Demonic Tyrant
> every ~60 s with Call Dreadstalkers (+ Grimoire: Imp Lord if up) fresh.**

- Two buckets: **Soul Shards** (cap 5, spend with HoG) and **Demonic Core**
  (cap 4, spend with Demonbolt). Bucket filling up → press its spender.
- **Ruination / Infernal Bolt are free** — they auto-replace HoG / Shadow Bolt
  when armed. Same keybinds; nothing to decide.
- **Cores barely need managing** — they overflow on their own (~131/fight), so
  "Demonbolt when you have a couple" is enough; you're never starved.
- **Everything hard is on a clock:** Tyrant 60 s, Dreadstalkers 20 s, Imp Lord
  2 min, Implosion 15 s (AoE). Press on cooldown.
- **Floor version for your hands:** *alternate HoG and Demonbolt, Shadow Bolt
  when you can't, Tyrant on cooldown.* (That's literally the `HoG DB HoG DB … SB
  SB` pattern the parses converge on.)

The only thing this drops: hold Tyrant a beat so Dreadstalkers/Imp Lord are
freshly summoned *inside* it — that's where the burst comes from. Everything
below is the evidence and the detail behind this box.

## How this was derived (provenance)

- **Data:** the top 6 Demonology Warlock parses on **Rotmire** (Sporefall
  single-boss raid, WCL zone 50 / encounter 3159), all **Mythic** difficulty,
  fights of 417–522 s. Rotmire is a loop/patchwork-style boss → clean,
  minimally-interrupted rotation, ideal for pattern mining.
- **Method:** pulled each player's full time-ordered `Casts` event stream via
  the WCL API, mapped ability IDs → names, dropped non-rotational casts
  (racials, trinkets, potions, defensives, pet dispels), then ran n-gram
  frequency + Tyrant-window segmentation across all six. **Then** pulled the
  **buff/aura event stream + summoned-pet list** for the #1 parse (Grotta) to
  verify the proc mechanics directly instead of inferring them.
- **All six are confirmed Diabolist** (each casts **Ruination** (cast spell
  `434635`) and **Infernal Bolt** (`434506`), and summons the Overlord / Mother
  of Chaos / Pit Lord ritual demons — all Diabolist-only). *(The matching buff
  IDs are Ruination `433885`, Infernal Bolt `433891` — cast ID ≠ aura ID.)*
- Rotation *theory* was also cross-checked against Maxroll (raid + M+) and
  Method (all 12.0.7 / June 2026, Tier-3). **Caveat:** those pages are
  JS-gated; the research pass extracted them imperfectly and injected some
  noise (a garbled "Grimoire: Fel Ravager", a "Summon Doomguard on cooldown"
  line) that the **parse data does not support**. Where guide text and parse
  data disagree, **the parse data wins** and the guide claim is flagged below.

**Confidence: medium-high.** WCL cast data is authoritative for *what was
pressed and in what order*; the aura/pet pull makes the proc mechanics
(Demonic Core, the Diabolic Ritual cycle) **directly observed, not inferred**.
The one remaining inference is exact resource *counts* per GCD (shards in hand),
which the log doesn't expose — cast spacing + buff events pin it closely.

## The whole spec is 9 buttons

Across ~2,600 rotational casts in six parses, the **entire** rotational
vocabulary is:

| Ability | Total casts (6 parses) | Role |
|---|---|---|
| **Hand of Gul'dan** (HoG) | 729 | shard spender → Wild Imps |
| **Demonbolt** (DB) | 541 | Demonic Core spender (instant when proc'd) |
| **Shadow Bolt** (SB) | 463 | shard builder / filler |
| **Implosion** (IMP) | 161 | consume 6 Wild Imps for burst; **15 s CD** (cleave + ST here) |
| **Call Dreadstalkers** (DS) | 139 | demon summon, ~on CD, feeds Tyrant |
| **Infernal Bolt** (IB) | 77 | *transformed* Shadow Bolt (see rituals) |
| **Ruination** (RUIN) | 76 | *transformed* Hand of Gul'dan (see rituals) |
| **Summon Demonic Tyrant** (TYR) | 48 | 60 s burst cooldown |
| **Grimoire: Imp Lord** (GIL) | 21 | 2-min demon summon, paired with Tyrant |

**Categorically absent across all six parses** (0 casts each): **Power Siphon,
Guillotine, Grimoire: Felguard, Summon Vilefiend, Bilescourge Bombers, Demonic
Strength.** See "Divergences" below — this matters, because both guides *and*
our own `rotation.md` still mention some of these.

## The engine you must understand first: Diabolic Ritual

Diabolist's whole identity — and the reason parts of the rotation **cannot** be
a fixed sequence — is the **Diabolic Ritual** cycle. This is **directly observed
in Grotta's aura stream**, not just guide theory. A hidden 3-stage wheel turns in
a fixed order; one stage is "active" for ~13–14 s while you spend shards, then it
expires into an armed proc called a **Demonic Art** that your next matching cast
consumes:

**Overlord → Mother of Chaos → Pit Lord → (back to Overlord)**

| Ritual stage (aura id) | Expires into → Demonic Art (aura id) | Effect on your next cast |
|---|---|---|
| Overlord `431944` | Art: Overlord `428524` | summons an **Overlord** demon *(no button changes)* |
| Mother of Chaos `432815` | Art: Mother of Chaos `432794` | next **Shadow Bolt → Infernal Bolt** (+3 shards) |
| Pit Lord `432816` | Art: Pit Lord `432795` | next **Hand of Gul'dan → Ruination** (3 free Wild Imps, 0 shards) |

**The wheel turning, from Grotta's log** (t = seconds from pull):

```
t=39.1  Diabolic Ritual: Overlord   begins
t=53.0  ...expires → Art: Overlord armed → consumed t=54.3 (summons Overlord demon)
t=54.3  Diabolic Ritual: Mother of Chaos begins
t=67.1  ...expires → Art: Mother of Chaos armed → consumed t=68.8 → Infernal Bolt cast
t=68.8  Diabolic Ritual: Pit Lord   begins  → (…later) → Ruination cast
```

**The counts prove the 1:1:1 mapping** (Grotta, full fight): Diabolic Ritual
Overlord **14** / Mother **13** / Pit Lord **13** → Demonic Art Overlord **13** /
Mother **13** / Pit Lord **13** → **Infernal Bolt cast 13** (= Art: Mother) and
**Ruination cast 13** (= Art: Pit Lord). The chain never desyncs.

Two consequences:

1. **Infernal Bolt and Ruination are not separate buttons you schedule.** They
   are Shadow Bolt / Hand of Gul'dan *wearing a hat* when the matching Art is
   armed. That's why in every parse **IB count ≈ RUIN count** (pooled 77 vs 76;
   Grotta exactly 13 = 13) and both fire at a steady cadence — they track ritual
   completions, not a timer or your intent.
2. **The order is deterministic, the timing is not.** You always get
   Overlord → Mother → Pit Lord in that order, but *when* each completes depends
   on how fast you spend shards. So you can **predict what's next** (keep an eye
   on which ritual is active → you know the next Art) but you **cannot pin it to
   a fixed slot** in a rote loop.

---

## SEQUENCE 1 — Opener (FIXED, learnable)

Two openers exist and they are **different**; pick by fight.

### 1a. What the top parses actually did on Rotmire — "Tyrant-first burst"

All six pressed **Summon Demonic Tyrant within the first 2–4 GCDs**, not after
a long build. Consensus skeleton (in-combat casts; pre-pull casts are not in the
log — see note):

```
[pre-pull: Hand of Gul'dan, then Demonbolt/Shadow Bolt to seed a Core]
1.  Demonbolt / Shadow Bolt      (opening GCD, spends the seeded Core)
2.  Call Dreadstalkers           (summon — will be extended by Tyrant)
3.  Summon Demonic Tyrant        (~t=3 s — extends pre-pull imps + Dreadstalkers)
4.  Grimoire: Imp Lord           (same GCD window as Tyrant, when off CD)
5.  Shadow Bolt
6.  Hand of Gul'dan
7.  Hand of Gul'dan              (flood imps into the Tyrant window)
8.  Implosion                    (Rotmire has adds — burst them; pure ST: skip)
9.  Shadow Bolt × 3              (rebuild shards)
… settle into steady state
```

Observed first-Tyrant timing, all six: `DS→TYR` / `DS·GIL·SB→TYR` /
`DB·GIL·DS→TYR` — Tyrant is pressed at **t ≈ 3–5 s** every time. This is a
front-loaded burst opener: you pre-summon demons before the pull so Tyrant has
a full board to empower immediately.

> **Note.** WCL logs start at the pull, so pre-pull Hand of Gul'dan casts don't
> appear — but Tyrant being worth pressing at t=3 s is only explicable if imps
> were already out, so pre-pull demon setup is assumed. (These parses use **no**
> Power Siphon at all — see Divergences — so the pre-pull is imps, not a Power
> Siphon.)

### 1b. Textbook "build-then-Tyrant" opener (Maxroll M+, verbatim)

Use when you can't pre-stack a burst on the pull:

```
1.  Pre-cast 2× Shadow Bolt / 1× Demonbolt
2.  Call Dreadstalkers
3.  Build to 5 shards with Shadow Bolt (4 if Soul Harvester)
4.  Grimoire: Imp Lord           (if talented)
5.  Build to 5 shards with Shadow Bolt  [Diabolist only]
6.  Summon Demonic Tyrant
7.  Hand of Gul'dan if 3+ shards
8.  Demonbolt with Demonic Core procs, < 3 shards
9.  Shadow Bolt, < 3 shards
```

> **Cleaned of guide-scrape noise.** The raw research pass also listed a "Summon
> Doomguard (if talented)" step and a "Grimoire: Imp Lord / Fel Ravager"
> variant. **Neither survives the parse data:** no parse casts Summon Doomguard
> or summons a Doomguard pet, "Fel Ravager" isn't a real ability here, and the
> only Grimoire used is **Imp Lord**. Those lines were dropped as extraction
> artifacts.

Both openers **agree on the pre-Tyrant demon setup** (Dreadstalkers + Grimoire:
Imp Lord out before Tyrant). They disagree only on *how much you build first*.
Verdict: **learnable as a fixed sequence either way — this is the most
sequence-able part of the spec.**

---

## SEQUENCE 2 — Tyrant entry block (FIXED, recurs every ~60 s)

This is the single most repeatable pattern in the data. Tyrant is cast **8×**
per parse (once per ~59 s = on cooldown), and the **last 2–3 casts before every
Tyrant are nearly identical**:

```
… (rebuild toward ~5 shards) → Call Dreadstalkers → [Grimoire: Imp Lord] → Summon Demonic Tyrant → Hand of Gul'dan → Hand of Gul'dan …
```

Evidence — the cast *immediately* before Tyrant is **Call Dreadstalkers** in
essentially every window across all six parses; **Grimoire: Imp Lord** is
inserted right beside it **when off cooldown** (GIL is a 2-min CD, so it lines up
with ~every other Tyrant — it appears in ~4 of 8 windows, exactly as expected).
The cast *after* Tyrant is almost always **Hand of Gul'dan** (often ×2).

**Learnable rule:** *"Dreadstalkers is the last thing you press before Tyrant.
If Imp Lord is up, press it next to Dreadstalkers. Then Tyrant, then immediately
dump Hand of Gul'dan."* This is a genuine fixed micro-sequence — drill it.

---

## SEQUENCE 3 — Inside the Tyrant window (SEMI-fixed shape)

After each Tyrant, the window has a consistent **shape** even though exact casts
vary. Pooled from all six parses, the dominant post-Tyrant pattern is:

```
TYR → HoG HoG → (DB HoG DB HoG …) with RUIN landing 4–7 casts in → keep HoG spam for ~15 s
```

- **`HoG HoG` opens the window** (flood Wild Imps while Tyrant empowers them).
- Then the **`DB HoG` / `HoG DB` alternation** dominates (see steady state).
- **Ruination** almost always appears once inside or just after the window (the
  Pit Lord art arms from all the shard-spending) — a free triple-imp HoG,
  extremely high value under Tyrant.
- Real timing (grotta, window #3): `TYR → DB(instant) → HoG → DB → HoG → DB DB → HoG → DB → HoG → IMP → HoG` — ~6 Hand of Gul'dan + interleaved instant Demonbolts in 15 s.

Maxroll's only instruction for the window is *"cast as many Hand of Gul'dan as
possible for 15 s"* (Dominion of Argus refunds a shard per cast to sustain it).
The parses confirm there is **no finer fixed inner sequence** — it's HoG-priority
spam with DB dumping Cores between casts. **Learnable as a shape/goal, not a
rote list.**

---

## The steady state is NOT a fixed sequence — and here's why

Outside the Tyrant window, people want a "loop." The data both offers one and
refuses one:

**The emergent loop.** The top pooled n-grams are overwhelmingly the
alternation:

- 5-grams: `HoG DB HoG DB HoG` (30×), `DB HoG DB HoG DB` (24×)
- 2-grams: `HoG DB` (313×) and `DB HoG` (313×) — dead even.

So ~80% of the time the steady state really is **Hand of Gul'dan ↔ Demonbolt,
back and forth.** That's the "loop" your hands learn.

**Why it can't be *only* that.** The alternation is an *emergent* product of
two resource clocks that drift in and out of phase:

- **HoG** needs 3–5 Soul Shards. **DB** needs a **Demonic Core** proc. Cores are
  *abundant* here — Grotta procced Demonic Core **131 times** (buff `264173`,
  stacking to ~4) with **zero Power Siphon**, fed passively by Dreadstalkers and
  Inner Demons. When shards + a Core are both ready you alternate HoG↔DB; when
  neither is, you **fall back to Shadow Bolt** to rebuild.
- The other frequent n-gram is exactly that fallback: `SB SB HoG SB SB` (17×),
  `SB SB SB` (44×) — **Shadow Bolt refill runs** whenever shards/Cores desync.

So the true steady state is a **3-state conditional loop**, not a fixed string:

```
loop:
  if a Demonic Art is armed → press its button now
        (Pit Lord: next HoG = Ruination — take it;
         Mother of Chaos: next SB = Infernal Bolt — take it, +3 shards)
  else if Wild Imps ≥ 6 and Implosion off CD (15 s) and AoE → Implosion
  else if Demonic Core ≥ 2 (or near Core cap)           → Demonbolt
  else if Soul Shards ≥ 3 (never overcap)               → Hand of Gul'dan
  else                                                  → Shadow Bolt (build)
  # …and Call Dreadstalkers whenever it's up and Tyrant isn't imminent
```

Run that loop with real resources and it *produces* the `HoG DB HoG DB … SB SB`
stream you see in the logs. **You memorize the priority + the two "loop"
shortcuts (HoG↔DB when flush, SB↔SB when starved); you cannot memorize a fixed
button string, because shard/Core/ritual state changes every GCD.**

### Could you *pool* to a known state and script it? (Mostly no)

Tempting idea: the only real randomizer is **Demonic Core proc timing** (cores
drop from pet swings on a chance basis, ~1 per 3.6 s). So could you *hold* cores
to a known state — say 3 Cores + low shards — then fire a scripted cycle?

**Where it works: yes, and the pros already do it — but only anchored to a
clock.** Arriving at the 60 s Tyrant at a controlled state (shards high,
Dreadstalkers + Imp Lord fresh, 1–2 cores banked) is exactly why the Tyrant
window's first casts are scriptable. Pool-to-a-clock is real.

**Where it fails: pooling in open filler.** Three reasons:

1. **Cores cap at 4 and the pump never pauses.** Sit at 3 cores waiting to
   "initiate" and the next proc (within ~3.6 s) pushes you to cap; any proc at 4
   is **overcapped = a flat DPS loss**. You can't hold a target state for more
   than a few seconds without bleeding procs.
2. **Holding a core means hardcasting your weaker filler.** A banked Core is an
   instant, harder Demonbolt you're declining so you can cast slow Shadow Bolts
   to build shards. You pay throughput for optionality.
3. **The script is ~5 GCDs and the pump refills mid-script.** From (2 shards,
   3 cores) a scripted `DB DB DB → HoG HoG` is ~7–8 s; during it ~2 more cores
   proc, so you exit already back in an RNG resource state. It doesn't compound.

The RNG you'd spend all that effort to kill is only *"Demonbolt or Shadow Bolt
this GCD?"* — and the reactive rule "core up → DB, else SB" already captures
~100% of that value with zero overcap. Cores aren't a gate you're starved on;
they're an overflowing bucket, and you can't script against a bucket that
refills faster than you can drain it. **Verdict: pool to a clock (Tyrant), don't
try to script the filler.**

---

## How each button comes up (proc taxonomy)

Sorted by *how* the ability becomes available — this is what makes some parts
sequenceable and others not:

- **Hard cooldowns — press on time, no proc:** Summon Demonic Tyrant (60 s),
  Call Dreadstalkers (~20 s), Grimoire: Imp Lord (~2 min), Implosion (**15 s**,
  gated by having ~6 Wild Imps). These drive the fixed sequences (opener, Tyrant
  entry) — the measured cast spacings match the cooldowns exactly (Tyrant min
  61.6 s, Dreadstalkers 20.0 s, Implosion 14.9 s).
- **Resource-gated — press when you have the resource:** Hand of Gul'dan (3+
  Soul Shards → Wild Imps), Demonbolt (a **Demonic Core** stack; instant, hits
  harder). Shadow Bolt is the free builder that refills shards.
- **Proc-transformed — a button you already have *changes on your bar*:** Shadow
  Bolt → **Infernal Bolt** (Art: Mother of Chaos), Hand of Gul'dan →
  **Ruination** (Art: Pit Lord). Same keybind, upgraded effect; the Demonic Art
  buff is the "light-up."
- **Passive / automatic — no button at all:** **Inner Demons** periodically
  spawns Wild Imps + random guest demons (the Gloomhound / Antoran Inquisitor /
  Antoran Jailer pets seen in the logs); during Tyrant, **Dominion of Argus /
  Abyssal Dominion** (`1276166` / `456323`) summon bonus demons (Grand Warlock
  Alythess, Lady Sacrolash) and refund shards so Hand of Gul'dan can chain.

## Ruination & Infernal Bolt — a rule, not a slot

Because the ritual order is deterministic (Overlord → Mother → Pit Lord), you
**can** anticipate them, which is the closest these get to "sequenceable":

- **Watch the ritual tracker** (Method's whole point). You always know which Art
  arms next.
- **When Pit Lord's Art is armed** → your next Hand of Gul'dan is **Ruination**
  (free 3 imps). Prefer to fire it **inside/entering the Tyrant window** for max
  value; the parses cluster RUIN around Tyrant.
- **When Mother of Chaos's Art is armed** → your next Shadow Bolt is **Infernal
  Bolt** (+3 shards). Fire it when **shard-starved** (it's your best builder) —
  Maxroll slots it as "Infernal Bolt if < 3 shards."
- **Overlord's Art** changes no button — it just summons an Overlord demon on
  your next spend.

**Verdict: learnable as a reaction rule keyed to a UI tracker, not a fixed
position.**

---

## Divergences worth flagging (parses vs. guides vs. our KB)

Verified against casts **and** the summoned-pet list across all six parses.

1. **Power Siphon: 0 casts — because it's redundant here, not because a guide is
   wrong.** Power Siphon exists to *manufacture* Demonic Core procs by
   sacrificing Wild Imps. But this build already drowns in Cores — Grotta got
   **131 Core procs** without it (vs 88 Demonbolts spent). Sacrificing imps you
   want alive for Implosion/Tyrant to buy Cores you already have is a net loss,
   so the top players skip it. (My first draft called `rotation.md` step 6
   "suspect" — the accurate framing is "unneeded in a Core-rich build," a
   talent/build choice, not a guide error.)
2. **Grimoire: Felguard / Summon Vilefiend: 0 casts, 0 pets — but these are
   alternate talent picks, not "stale."** All six run **Grimoire: Imp Lord**
   (`1276452`, pet confirmed) as their pre-Tyrant summon. `rotation.md` mentions
   Felguard/Vilefiend because those are *valid other choices*; this particular
   Rotmire build just doesn't take them. (My first draft called the KB "stale
   naming" — overstated. It's a build divergence.)
3. **Summon Doomguard: not used.** No parse casts it (any spell ID) and **no
   Doomguard pet is ever summoned** in any of the six. The "Summon Doomguard on
   cooldown" line in the earlier draft came from unreliable guide extraction and
   is **unsupported by the data** — removed. (The ability exists this patch,
   `1276672`; these players simply don't run it.)
4. **No Guillotine, Bilescourge Bombers, or Demonic Strength.** The lean modern
   Diabolist build drops these entirely (0 casts each, all six).
5. **Tyrant-first opener.** Top players press Tyrant at t≈3 s (burst-on-pull);
   the *written* textbook opener builds to 5 shards twice first. Both are valid;
   the aggressive one requires pre-pull demon setup.

**Demons actually summoned (all six parses):** Demonic Tyrant, Dreadstalkers,
Imp Lord, Wild Imps, the three ritual demons (Overlord / Mother of Chaos / Pit
Lord), plus Inner Demons guests (Antoran Inquisitor/Jailer, some Gloomhound) and
the Dominion of Argus demons (Alythess, Sacrolash). **Never:** Doomguard,
Felguard, Vilefiend.

> **Action for `rotation.md`:** switch the pre-Tyrant summon naming to **Grimoire:
> Imp Lord** (noting Felguard/Vilefiend as alternates), note Power Siphon is
> **build-dependent / skipped in Core-rich builds**, and add the Diabolic Ritual
> cycle as the explanation for Ruination/Infernal Bolt. Left as a follow-up edit
> rather than silently overwriting the priority doc.

---

## Bottom line — the heuristic → sequence map

| Rotation part | Fixed sequence? | What to learn |
|---|---|---|
| **Opener** | ✅ Yes | Drill SEQUENCE 1 (pick 1a burst or 1b textbook). |
| **Tyrant entry** (every 60 s) | ✅ Yes | Drill SEQUENCE 2: `…→ Dreadstalkers → [Imp Lord] → Tyrant → HoG HoG`. |
| **Tyrant window** (15 s) | 🟡 Shape only | HoG-spam; open with `HoG HoG`; DB dumps Cores between; land Ruination here. |
| **Steady state** | ❌ No | Conditional 3-state loop; hands learn `HoG↔DB` (flush) and `SB SB` (starved). Not a fixed string. |
| **Ruination / Infernal Bolt** | ❌ No (but predictable) | Reaction rule on the ritual tracker; order is Overlord→Mother→Pit Lord. |
| **Call Dreadstalkers** | 🟡 Timing rule | On CD, but *hold it to be the last cast before Tyrant*. |
| **Implosion** (AoE) | ✅ Clock | Fixed 15 s CD; press on CD with ~6 imps up. |

**In one line:** the openers and the Tyrant-entry block are genuinely fixed,
memorizable sequences (drill them). Everything else is a resource- and
ritual-gated priority that *emerges* into the `HoG DB HoG DB … SB SB` pattern but
can't be reduced to a rote string — the Diabolic Ritual cycle guarantees the
*order* of your procs but not their *timing*, so the back half of the rotation
is learnable only as rules + shapes, not as a script.

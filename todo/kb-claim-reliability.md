# Claim reliability — why the addon-dev KB anchors agents to wrong answers

**Opened 2026-08-09.** A process revision for `knowledge/addon-dev/`. Sibling doc:
`addon-dev-overhaul.md`, which addresses a *different* disease — accretion, where nothing
is ever removed. This one is about the reliability of what is there.

Written to be executed in a fresh context. Everything needed is in this file.

---

## 1. The problem, in one sentence

**A negative result gets recorded with the same authority as a positive one, and then
every follow-up is framed by it — so the KB reinforces its own wrong answers instead of
testing them.**

## 2. The worked example — Call Dreadstalkers

The case that produced the complaint, and the one to check any proposed fix against.

**What was measured, correctly:** on cooldownID `760` (the Call Dreadstalkers BuffBar row),
`item.auraDataUnit` read `nil` across 13 in-combat samples, and the CDM alert channel raised
**zero** edges of any kind across 1054 recorded edges and 171 casts. Both facts are true
today. Neither has been retracted.

**What was written down:** that a summon binds no aura, so there is nothing to read — a
claim about the whole space of ways to observe the row.

**What was actually true:** the row is **totem-backed**. Blizzard's own buff-item code
checks totems *before* auras — `GetCooldownValues` returns
`totemData.expirationTime, duration, modRate` and only falls through to `GetAuraData()`
when there is no totem `[CooldownViewer.lua:1208-1233]`; `IsExpired` does the same
`[:1167-1184]`. `PLAYER_TOTEM_UPDATE` fires in the same second as the cast.
`GetTotemDuration(slot)` hands back a drawable duration object, and `Bar.Pip:IsShown()` is a
plain boolean that says whether the bar is live.

**So the two instruments were pointed at the wrong subsystem, and the record could not
show that.** "Searched and absent" and "never examined" looked identical.

**The cost.** The claim was corrected once, but the correction went into the Changelog while
the body kept the puzzle framing. The KB's own §7 records that *"three downstream documents
quoted the headline sentence and left the correction behind, and it had to be disproved
three times."* Days of arguing with agents that kept re-anchoring to the line.

## 3. The two mechanisms

**3.1 Negative existentials wear a positive's evidence class.**

`[client YYYY-MM-DD]` means *"we ran code and saw this."* That is right for
*"`auraDataUnit` read nil."* It is wrong for *"there is no way to read this"* — the first
is an observation of a value, the second is a claim about an unbounded space. They carry
the same tag, so they read as equally solid, and the second is the one that anchors agents.
README §0 calls `[client]` the strongest class in the subtree, which makes it the hardest
to dislodge.

**Measured: 64 negative-existential phrasings** across the subtree (`there is no`,
`nothing can`, `no way to`, `cannot be`, `is not possible`, `never fires/answers`), 15 each
in `cooldown-manager.md` and `security-taint-and-restricted-data.md`.

**3.2 The observation loop cannot disconfirm.**

An agent writing an observation has just read the topic file, so the observation inherits
its framing. The observation is then cited back as support for the claim. Nothing in that
loop can produce a disconfirmation, because whatever would disconfirm it was never in the
frame. On cid 760 every follow-up probed *aura* instruments harder, because the file said
the question was about auras.

**Measured: ~334 pointers** from claims into internal artifacts (`OBS-nnn`, `projects/**`,
addon names, capture paths). Draining an observation is supposed to close it, but the
pointers survive the drain and keep the loop alive.

**3.3 Why the existing doctrine did not stop it.**

The KB already contains the fix, in prose, written after the same failure:
*"State the instrument, not the impossibility"* and *"Put the qualification in the
headline."* It happened again anyway. **Doctrine sitting next to a claim does not stop an
agent quoting the headline.** The fix has to be mechanical or structural, not more prose.

---

## 4. The revision

Four changes. 1 and 2 are the core; 3 and 4 close the loop.

### 4.1 Split the marker so a negative cannot wear a positive's clothes

```
[client 2026-08-09]                                 a value was observed. POSITIVES ONLY.
[searched 2026-08-09: aura channel, alert edges]    we looked HERE and found nothing.
```

`[searched]` reads weak by construction and **forces the author to name the space**. On cid
760 it would have read *"searched: aura channel, alert edges"* — and **totems would have
been visibly missing from that list**, to every agent that read the line. That is the whole
fix for the case that burned us.

Rules:
- A claim that something *cannot* be done, or that nothing can read/observe/answer X, takes
  `[searched …]`, never `[client …]`.
- The list names **instruments and subsystems**, not conclusions.
- A `[searched]` claim may never be phrased as an impossibility. "Not found via X, Y" — not
  "there is no way".

### 4.2 Gate it in `kblint`

Two new gates. This workspace's philosophy is that the consuming tool is the test; a rule
nobody can forget beats a rule everyone agrees with.

- **Gate N1 — unqualified negative.** A negative-existential phrasing in a paragraph
  carrying `[client]` but no `[searched: …]` is a finding.
- **Gate N2 — the citation circle.** A topic-file claim citing `OBS-nnn`, a `projects/**`
  path, a capture path (`raw/<addon>-*.log`) or one of our addon names is a finding.
  Queue files (`observations.md`, `mined-pending-verification.md`) are exempt — pointing at
  our work is what they are for.

64 and ~334 sites to triage once, then neither can regrow.

### 4.3 Cut the citation circle

A topic-file claim stands on its own, on what it says. Drain the observation, then delete
the pointer. This is already the intended process — draining is defined as *"edit the
target file's claim, then set `Status: drained`"* — but nothing removes the inline pointer,
so the circle survives.

⚠ **This is NOT the sourcing ban discussed and rejected on 2026-08-09.** wago/DB2, `UI.xsd`,
Blizzard blue posts and the wiki all remain admissible; an audit found that banning them
costs ~52% of the subtree and deletes the ~180 measured facts that are the reason this KB
beats reading the wiki. The target here is the *pointer*, not the *source*.

### 4.4 Evidence that cannot be re-checked must say so

A claim whose capture has rolled off the SavedVariables ring can never be re-verified, and a
claim nobody can re-check is not a strong claim whatever tag it wears. Either archive the
capture (`projects/addon-lab/runs/` exists for this) or state in the claim that its evidence
is gone.

**Worked example of the failure, from the same session:** `observations.md` OBS-064 was
written with an `Observed:` headline, effect figures from a capture that had already rolled
off the ring, and a `sources:` line pointing at logs that show the opposite. It should have
been a source-read claim in the topic file, not an observation.

---

## 5. Execution — ordered, each step bounded

Run each step through write → adversarial review, as the KB edits of 2026-08-09 were.

1. **Triage the 64 negatives.** For each: is it an observation (keep `[client]`, rephrase to
   name the instrument) or an existential (convert to `[searched: …]`, or delete if the
   search space was never established)? Expect a good fraction to be **fine already** — the
   ones that name an instrument. A handful will be real overreaches of the Dreadstalkers
   kind. **Do not batch-rewrite; each one is a judgement.**
2. **Add gates N1 and N2 to `wowkb.kblint`.** Verify the baseline is clean afterwards, i.e.
   step 1 actually closed N1.
3. **Strip the ~334 internal pointers** from topic files, leaving queue files alone.
4. **Update `knowledge/addon-dev/README.md` §0** to define `[searched]` alongside `[client]`,
   and say plainly that a negative existential may not carry `[client]`.
5. **Resolve OBS-064** — delete it, move the reproducible half (the source read at
   `CooldownViewerItemData.lua:449/:454/:482`) into `cooldown-manager.md` §7 next to the
   totem material, where someone about to call a totem getter will meet it.

## 6. Acceptance

- `wowkb.kblint` exits 0 on gates N1 and N2 across the whole subtree.
- Zero `[client]` tags on negative existentials.
- Zero `OBS-nnn` / `projects/**` / capture-path citations in the nine topic files.
- **The Dreadstalkers test:** read `cooldown-manager.md` §7 cold and answer *"can I track a
  summon's duration?"* The file must either answer it or make visible which subsystems were
  searched. If a fresh reader could still conclude "impossible" from a headline, the
  revision has failed.

## 7. Explicitly out of scope

- The sourcing ban (§4.3). Rejected — audit is in the 2026-08-09 session record.
- The accretion problem — `addon-dev-overhaul.md` owns it.
- Anything in `knowledge/` outside `addon-dev/`.

## 8. The habit this is really trying to install

When a measurement comes back empty, the next question is **"which subsystem did I not
point an instrument at?"** — not "how do I probe this one harder?" On cid 760, Blizzard's own
source answered it: `GetCooldownValues` checks totems before auras, in the file we had
already read. The answer was sitting in the source the whole time.

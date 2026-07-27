# burst-hold — rationale

**Situation:** combat, AoE; the **burst branch is imminent** — Summon Demonic Tyrant is
napkin-anticipated **~15 s** out. **Call Dreadstalkers** and **Implosion** are both
napkin-**probably-up** (their cds are secret in combat). **3 soul shards** banked; **no Demonic
Core** (Demonbolt down); **Wild Imps out** (buff active, count secret). A build/spend press exists
underneath the burst setup.

**Oracle (rotation source → expected Guidance):**

- **Hand of Gul'dan is the single `ROTATION` press.** 3 shards banked, no Core (so Demonbolt is not
  a competitor), and Tyrant is **>5 s away** — `rotation.md` step 9 ("Hand of Gul'dan at ≥3 Soul
  Shards when Tyrant is >5 s away") and `diabolist-sequences.md` steady-state loop
  ("else if Soul Shards ≥ 3 → Hand of Gul'dan") both say **press HoG now** at 15 s from Tyrant.
  It is the #1 ready ability → the one steady lit press.

- **Dreadstalkers draws `JUDGE`, not a press.** Off cooldown, but the rotation source's
  Dreadstalkers rule is **timing, not "press on sight"**: *"Dreadstalkers is the last thing you
  press before Tyrant … hold it to be the last cast before Tyrant"* (`diabolist-sequences.md`
  SEQUENCE 2 + the Call-Dreadstalkers timing rule; `rotation.md` step 5 — "cast when Tyrant is
  ≥~20 s away or ≤~12 s away, not mid-window"). With Tyrant ~15 s out, whether to fire it **now**
  or **hold** to stage the window is a genuine your-call — so we **inform, don't instruct**: `JUDGE`
  + a pass-through note, never an auto-green.

- **Implosion draws `JUDGE`, not a press.** Its gate is **≥6 Wild Imps** (`rotation.md` step 7 /
  `diabolist-sequences.md` steady-state loop), and here two secrets compound: the **imp count is a
  Secret Value** (unreadable — `buff.isActive` tells us imps are *out*, not *how many*), and with
  Tyrant ~15 s away those imps may be better **flooded into the Tyrant window** ("flood imps into
  the Tyrant window") than imploded now. Both point to a hold-or-press your-call → `JUDGE` + note.

- **This is the ONLY cue-logic change the burst branch introduces.** Absent the imminent Tyrant,
  Dreadstalkers-off-cd would just be pressed and Implosion would carry the usual imp-count `JUDGE`;
  the burst model demotes *both* to explicit "stage-or-press" `JUDGE`s while the build/spend
  `ROTATION` (HoG) keeps running underneath. Tyrant itself is **not drawn** — at ~15 s it is neither
  pressable nor close enough for `SOON` (which is a ~2 s countdown); it is only the *context* the
  napkin supplies, so it stays an unlisted internal (cooling).

- **Losers demoted:** **Demonbolt** — no Core (`buff.isActive:false`, `glow:false`), not a call
  (unlisted). **Shadow Bolt** — filler, outranked by HoG at 3 shards (unlisted). **Tyrant** —
  cooling/anticipated, not a press (unlisted).

**Readability (the crux):**
- Every drawn cue traces to a **readable** signal. HoG's `ROTATION` rests on **shards**
  (`power.SoulShards.value = 3`, readable) + **no Core** (readable via `buff.isActive` on 777) —
  never on a secret cd. The two `JUDGE`s rest on **napkin probably-up** (`cd.state:"unknown"`,
  `source:"napkin"` — the honesty rule forbids a napkin `"ready"`) **plus** the readable
  burst-context (Tyrant `cd.state:"anticipated", remaining:15, source:"napkin"`) **plus**, for
  Implosion, imps present (`buff.isActive` on 143038). None of these reads a secret cd or the
  secret imp count; where the true gate is secret (DS pre-Tyrant timing, Implosion's ≥6-imp
  threshold), the golden **softens to `JUDGE`** — informs, never falsely instructs.
- `aura` is `readable:false` throughout (C_UnitAuras dark in combat) and is **not** any cue's
  source.

**Contract invariants this exercises:**
- **Single-top-press** — exactly one cue is `ROTATION` (HoG); the two `JUDGE`s are non-press
  your-call signals that legitimately **coexist** with it (the burst-model coexistence case:
  two `JUDGE` + one `ROTATION`).
- **`JUDGE` semantics** — a your-call availability we can't instruct because the gate is secret,
  drawn alongside the single press.
- **Secrecy gate** — no cue leans on a `readable:false` fact.
- **Pass-through strings** — the `note`s are Coach-authored display text (the only place spec
  vocab may appear).
- **Napkin honesty** — the anticipated Tyrant carries `remaining>0`; the probably-up DS/Implosion
  carry `state:"unknown"` with **no** `remaining`; nothing reads `"ready"` in combat.

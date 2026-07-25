# implosion — rationale

**Situation:** combat; Implosion off cooldown; Wild Imps out (buff active, **count secret**);
3 soul shards; Demonic Core down; summons cooling. Cast `history` shows only **one** recent
Hand of Gul'dan.

**Oracle (rotation source → expected Guidance):**
- **HoG is the readable `ROTATION` winner** — 3 shards, primary spender, nothing higher up (same
  logic as the `hand-of-guldan` golden).
- **Implosion draws `JUDGE`, not `ROTATION`.** Its real gate is **≥6 Wild Imps** (`rotation.md`
  step 7 / `maxroll` "always Implode at 6 imps"), and the imp **count is a Secret Value** —
  unreadable. The **imp-napkin** (estimate from cast `history`) is **not confident**: only one
  recent HoG (~3 imps) is well below 6, and one HoG could have been a partial cast. So we
  **inform, don't instruct** — `JUDGE` + a pass-through note, never an auto-green.
- This is the promotion gate's *negative* side. The paired `implosion-primed` scenario (≥2 recent
  full HoGs, no Implosion since, conservative window) is where the napkin **is** confident and
  Implosion promotes to `ROTATION`.

**Contract checks this exercises:**
- **Single-top-press holds** — exactly one cue is `ROTATION` (HoG); `JUDGE` is a non-press signal
  that legitimately **coexists** with it (like `SOON`).
- **Secrecy gate** — no cue leans on a `readable:false` fact. In combat we can't *read* Implosion
  ready (the cd is secret); the napkin says **probably up** (`cd.state:"unknown"`, `source:"napkin"`
  — the honesty rule forbids a napkin `"ready"`). So Implosion's `JUDGE` rests on "napkin
  probably-up + imps present (`buff.isActive`) + history uncertain," none of which reads the secret
  imp count; HoG's `ROTATION` rests on readable shards.
- **Pass-through string** — the `note` is Coach-authored display text (sanctioned).

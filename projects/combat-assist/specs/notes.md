# Combat Assist Plus — notes

**What this file is for:** the running record of what we did — session logs,
decisions and why they went that way, things we tried that didn't work, in-game
observations. Append-only in spirit: this is the file you read to find out how the
project got where it is.

It is deliberately the *loose* one. `spec.md` says what the addon should do and
`backlog.md` says what's left; anything that doesn't fit either — a measurement, a
dead end, a rationale, a "next session, start here" — lands here rather than
getting lost or being forced into a spec line.

Newest session at the top. Date each entry.

⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
`knowledge/addon-dev/` (see the wow-developer skill's "Improve the KB as you go") —
this file records *our* work, not the client's behaviour.

---

## 2026-08-05 — scaffold

Created the project and the addon repo `michac/cap` from scratch.

- `projects/combat-assist/addon/` — own git repo, gitignored by the wow repo, same
  arrangement as CDMProbe / BucketBinds / PlannerState. Pushed, public, MIT.
- `CombatAssistPlus/` — `.toc` (Interface 120007, v0.1.0,
  SavedVariables `CombatAssistPlusDB`) + `Core.lua`: namespace, a defaults merge on
  `ADDON_LOADED` that fills new keys without clobbering saved ones, and the `/cap`
  router built off an `ns.Commands` schema table with exact-match dispatch and a
  prefix-only "did you mean" (house rule 7 — no substring dispatch). `status`,
  `toggle`, `help`. No combat code, no frames.
- Registered as `cap` in `wowkb.addon` (→ `michac/cap` →
  `projects/combat-assist/addon`, confirm hint `/cap status`) and added to
  `addon-manager/config.json`. `release cap --dry-run` runs clean end to end.
- **No release cut**, so `ghaddons` has nothing to install — the addon is not in the
  game folder yet.

Decision: what the addon *does* was left undefined on purpose rather than guessed
at. `spec.md` §6 carries the open questions.

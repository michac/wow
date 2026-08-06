# Combat Assist Plus — spec

**What this file is for:** what the addon is supposed to do. The product
definition, not the implementation. If you're about to build something and this
file doesn't say what it should do, the answer is to write it here first (or ask),
not to infer it from the code.

**Status: undefined.** The addon exists as a scaffold. Nothing below §1 has been
decided yet — the sections are the shape the spec should take, not claims.

## 1. What it is

*(one paragraph: the product, in the user's terms)*

`/cap` — a combat-assistance addon for Retail / Midnight 12.0. Beyond the name,
the scope is open. Sibling projects for reference on where a line might be drawn:
**Cooldown HUD** (`projects/cooldown-hud/`) already owns "what should I press
next" as a skinned overlay on Blizzard's Cooldown Manager, and **BucketBinds**
(`projects/keybinder/`) owns keybind/action-bar placement. Whatever this becomes
should not duplicate either.

## 2. Who it's for and when it runs

*(which specs, which content — raid / M+ / delves / open world; in combat only?)*

## 3. What it does

*(the behaviours, each one testable. A behaviour nobody can check in game or
under `busted` is not yet a spec line.)*

## 4. What it explicitly does NOT do

*(the boundary. Cheaper to write than to argue about later.)*

## 5. Constraints

Two are already fixed by the platform, and both shape the design more than
anything in §3:

- **Secret Values (12.0).** Many combat values are unreadable to addons. Anything
  in §3 that depends on reading a resource, a cast, or an aura has to survive that
  — see `knowledge/addon-dev/` and `projects/cooldown-hud/docs/notes.md`, which is
  the hard-won record of what is and isn't readable.
- **Combat lockdown.** Secure-frame changes are blocked in combat. An assist that
  wants to *do* something rather than *show* something has to prove it can.

House rules for the code itself: `.claude/skills/wow-developer/references/house-rules.md`.

## 6. Open questions

- What does "assist" mean here — display, decision support, or automation?
- One spec first (the Cooldown HUD pattern), or class-agnostic from the start?
- Is there an existing addon that already does this? Worth a `/mine-addon` pass
  before writing §3.

## Milestones

| # | Milestone | Status |
| --- | --- | --- |
| M0 | Scaffold — repo, `.toc`, `/cap` router, registered in `wowkb.addon` | ✅ 2026-08-05 |
| M1 | *(spec §1–§4 written)* | — |
